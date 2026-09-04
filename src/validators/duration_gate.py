"""duration_gate — kiểm thời lượng & tỉ lệ NB-TH-VD(-VDC) cho phiếu PHÂN TẦNG.

Số liệu (phút/câu, ngân sách, tỉ lệ) NAY đọc từ `config/tier_spec.json` (trước cứng
trong file này). Bảo toàn hành vi tầng C lớp 9 + B/C lớp 8; tổng quát cho mọi tầng
có rate card + thêm band VDC. Tầng chưa chốt tỉ lệ (X) → KHÔNG gate.

Quy ước đếm (Thầy chốt 2026-06-11):
  • "Câu" = ý nhỏ a),b),c)… (mỗi ý 1 câu); bài VD tách thì đếm theo thẻ [NB]/[TH]/
    [VD]/[VDC] đầu mỗi ý. KHÔNG đếm Khám phá/Khái niệm (giờ GV giảng).
  • Phút/câu + ngân sách + tỉ lệ: lấy từ tier_spec theo (lớp, môn, tầng).
  • Bài HÌNH khai `draw: true` (HS phải tự vẽ hình) cộng thêm `draw_minutes` (5′,
    Thầy chốt 2026-07-26) — cộng MỘT LẦN cho cả bài, vào band theo `level` của bài.
  • Tỉ lệ áp cho TỪNG PHIẾU theo THỜI GIAN, sai số ±ratio_tol điểm %, CHỈ phần
    TRÊN LỚP (BTVN không thuộc tỉ lệ — chỉ giữ quỹ phút).
"""
from __future__ import annotations

import re

from src.schema.lesson_package import LessonPackage
from src.schema.tier_spec import (
    chuong_co_vd, draw_minutes, gop_vd_vdc, load_tier_spec, quick_minutes, subject_block,
    rates_for, so_ca_yeu_cau, tier_ratio,
)

_TAG_RE = re.compile(r"\[(NB|TH|VD|VDC)\]")
# Ý a)…j) ở VỊ TRÍ LIỆT KÊ: chỉ tính khi trước nó là khoảng trắng / `]` (từ [[br]]) /
# `}` (sau minipage) / `>` / đầu chuỗi. Tránh đếm nhầm "b)" trong "(a+b)", "(a-b)"…
_ITEM_RE = re.compile(r"(?<![^\s\]>}])([a-z])\)")
_BULLET_RE = re.compile(r"\\bullet")

_LEVEL_TO_BAND = {1: "NB", 2: "TH", 3: "VD", 4: "VDC"}
_BANDS = ("NB", "TH", "VD", "VDC")


def _count_items(text: str) -> int:
    """Đếm số "câu" trong bài KHÔNG gắn thẻ mức: mỗi ý a),b)… = 1 câu; ý liệt kê
    bullet con thì đếm theo số bullet (vd "b) thử 3 BPT" = 3 câu)."""
    marks = list(_ITEM_RE.finditer(text))
    if not marks:
        return max(1, len(_BULLET_RE.findall(text)))
    total = 0
    for i, m in enumerate(marks):
        chunk = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        bullets = len(_BULLET_RE.findall(chunk))
        total += bullets if bullets else 1
    return total


def _problem_units(lesson: LessonPackage):
    """Gom mỗi `problem` + các `para` đi liền sau thành 1 đơn vị đếm, trả
    (đoạn, level, [text…], phải-tự-vẽ-hình, hình-vẽ-sẵn). CHỈ đếm chặng luyện tập/
    tổng kết (review/concept = giờ GV giảng, bỏ)."""
    for stage in lesson.stages:
        if stage.kind in ("review", "concept"):
            continue
        current = None
        for b in stage.blocks:
            typ = getattr(b, "type", "")
            if typ == "problem":
                if current:
                    yield current
                current = (getattr(b, "tier", "") or "onclass",
                           getattr(b, "level", 0), [b.statement or ""],
                           bool(getattr(b, "draw", False)),
                           bool(getattr(b, "figure_given", False)))
            elif typ == "para" and current:
                current[2].append(getattr(b, "text", "") or "")
            elif typ in ("noted", "mindmap"):
                if current:
                    yield current
                    current = None
        if current:
            yield current


def _count_by_band(lesson: LessonPackage, only_figure_given: bool = False) -> dict[str, dict[str, int]]:
    counts = {"onclass": {b: 0 for b in _BANDS}, "btvn": {b: 0 for b in _BANDS}}
    for seg, level, texts, _draw, fig in _problem_units(lesson):
        if seg not in counts:                # extend… không thuộc quỹ giờ
            continue
        if only_figure_given and not fig:
            continue
        text = " ".join(texts)
        tags = _TAG_RE.findall(text)
        if tags:
            for band in tags:
                counts[seg][band] += 1
        else:
            counts[seg][_LEVEL_TO_BAND.get(level, "TH")] += _count_items(text)
    return counts


def band_counts(lesson: LessonPackage) -> dict[str, dict[str, int]]:
    """Đếm số câu LUYỆN TẬP theo {onclass|btvn: {band: n}} — đơn vị ý nhỏ/thẻ mức.
    Dùng chung cho duration_gate (×rate ra phút) và spec_gate (so với spec)."""
    return _count_by_band(lesson)


def figure_given_counts(lesson: LessonPackage) -> dict[str, dict[str, int]]:
    """Trong số câu trên, bao nhiêu câu làm trên HÌNH VẼ SẴN (`figure_given`) —
    những câu này tính NỬA phút/câu (xem ProblemBlock.figure_given)."""
    return _count_by_band(lesson, only_figure_given=True)


def draw_counts(lesson: LessonPackage) -> dict[str, dict[str, int]]:
    """Đếm số BÀI phải TỰ VẼ HÌNH theo {onclass|btvn: {band: n}} — mỗi bài 1 hình
    (không nhân theo ý a,b,c). Band lấy theo `level` của bài; bài chưa chấm level
    thì lấy band CAO NHẤT trong các thẻ của bài (độ khó thật của bài)."""
    counts = {"onclass": {b: 0 for b in _BANDS}, "btvn": {b: 0 for b in _BANDS}}
    for seg, level, texts, draw, _fig in _problem_units(lesson):
        if not draw or seg not in counts:
            continue
        band = _LEVEL_TO_BAND.get(level)
        if band is None:
            tags = _TAG_RE.findall(" ".join(texts))
            band = max(tags, key=_BANDS.index) if tags else "TH"
        counts[seg][band] += 1
    return counts


def check_vdc_cuoi_bai(lesson: LessonPackage) -> list[str]:
    """VDC chỉ được nằm ở Ý CUỐI của bài — mỗi bài tối đa MỘT thẻ [VDC].

    Thầy chốt 04/09/2026: "bài VDC thì chỉ câu cuối mới tính thôi". Kho đề xác nhận:
    bài hình a),b),c) thì chỉ ý c) là câu phân loại, hai ý trước là TH/VD. Gắn [VDC]
    cho nhiều ý trong một bài vừa thổi phồng quỹ phút (VDC 18′/câu so với TH 6′) vừa
    làm phiếu khó sai mức so với đề thật.
    """
    warns: list[str] = []
    for stage in lesson.stages:
        if stage.kind in ("review", "concept"):
            continue
        nhan, texts = None, []

        def _soi(nhan: str | None, texts: list[str]) -> None:
            if not nhan:
                return
            tags = _TAG_RE.findall(" ".join(texts))
            if "VDC" not in tags:
                return
            ten = nhan or "(không nhãn)"
            if tags.count("VDC") > 1:
                warns.append(
                    f"duration: bài '{ten}' gắn {tags.count('VDC')} thẻ [VDC] — mỗi bài chỉ "
                    f"được MỘT ý mức VDC (Thầy chốt 04/09/2026). Hạ các ý trước xuống [TH]/[VD].")
            elif tags[-1] != "VDC":
                sau = ", ".join(f"[{t}]" for t in tags[tags.index("VDC") + 1:])
                warns.append(
                    f"duration: bài '{ten}' có thẻ [VDC] nhưng SAU nó còn {sau} — VDC phải là "
                    f"Ý CUỐI của bài (Thầy chốt 04/09/2026). Đổi thứ tự ý hoặc hạ mức.")

        for b in stage.blocks:
            typ = getattr(b, "type", "")
            if typ == "problem":
                _soi(nhan, texts)
                nhan, texts = getattr(b, "label", "") or "", [b.statement or ""]
            elif typ == "para" and nhan is not None:
                texts.append(getattr(b, "text", "") or "")
            elif typ in ("noted", "mindmap"):
                _soi(nhan, texts)
                nhan, texts = None, []
        _soi(nhan, texts)
    return warns


def _grade_subject(lesson: LessonPackage) -> tuple[str, str]:
    """Suy (lớp, môn) để tra tier_spec. Lesson chỉ có grade_label → phân lớp 8/9;
    phát hiện môn 'hinh-hoc' nếu eyebrow hoặc title chứa chữ 'hình'/'hinh'."""
    gl = getattr(lesson, "grade_label", "") or ""
    grade = "lop-8" if "Lớp 8" in gl else "lop-9"
    eyebrow = getattr(lesson, "eyebrow", "") or ""
    title = getattr(lesson, "title", "") or ""
    # Soi cả `grade_label` (vd "Lớp 9 • Hình học") — trước chỉ soi eyebrow+title nên
    # phiếu hình đặt tiêu đề không có chữ "hình" bị chấm nhầm sang rate card đại số.
    text_to_search = (eyebrow + " " + title + " " + gl).lower()
    subject = "hinh-hoc" if "hình" in text_to_search or "hinh" in text_to_search else "dai-so"
    return grade, subject


def _luat_tang_b(lesson: LessonPackage, spec: dict, grade: str, subject: str,
                 tier: str, tier_block: dict) -> list[str]:
    """Luật riêng của tầng B (Thầy + anh An chốt 30/08/2026), soi trên PHIẾU THẬT:
    phải khai `chuong`; chương không có VD-VDC thì gộp 2 phiếu; bài VẬN DỤNG phải in
    sẵn quy trình giải."""
    if not tier_block.get("ratio_variants"):
        return []
    warns: list[str] = []
    chuong = getattr(lesson, "chuong", "") or ""
    co_vd = chuong_co_vd(grade, chuong)

    if not chuong:
        warns.append(
            f"duration: phiếu tầng {tier} chưa khai `chuong` — ĐÃ BỎ cổng tỉ lệ NB-TH-VD "
            f"và cổng gộp phiếu. Thêm \"chuong\": \"<slug>\" (xem config/ban_do_vd_vdc.json).")
    elif co_vd is None:
        warns.append(
            f"duration: không tìm thấy chương '{chuong}' của {grade} trong "
            f"config/ban_do_vd_vdc.json — ĐÃ BỎ cổng tỉ lệ NB-TH-VD.")
    elif co_vd == "bien":
        warns.append(
            f"duration: chương '{chuong}' ({grade}) còn để 'bien' trong ban_do_vd_vdc.json — "
            f"THẦY CHƯA CHỐT có bài VD/VDC hay không, chưa nên soạn phiếu chương này.")

    # (W) GỘP PHIẾU: chương không có VD-VDC thì hai buổi dùng chung một phiếu.
    ca_yc = so_ca_yeu_cau(spec, grade, subject, tier, chuong)
    ca = max(1, getattr(lesson, "so_ca", 1) or 1)
    if ca_yc and ca != ca_yc:
        warns.append(
            f"duration: phiếu khai `so_ca` = {ca} nhưng chương '{chuong}' "
            + ("KHÔNG có bài VD-VDC nên phải GỘP 2 PHIẾU THÀNH 1 (`so_ca: 2`)"
               if ca_yc == 2 else "CÓ bài VD-VDC nên mỗi phiếu chỉ một buổi (`so_ca: 1`)")
            + " — anh An chốt 30/08/2026.")

    # (W) QUY TRÌNH GIẢI BÀI in ngay tại từng bài VẬN DỤNG (level 3).
    thieu = [b.label for st in lesson.stages for b in st.blocks
             if getattr(b, "type", "") == "problem"
             and getattr(b, "level", 0) == 3 and not getattr(b, "quy_trinh", None)]
    if thieu:
        warns.append(
            f"duration: {len(thieu)} bài VẬN DỤNG chưa có `quy_trinh` ({', '.join(thieu[:6])}"
            + ("…" if len(thieu) > 6 else "")
            + ") — Thầy chốt 30/08/2026: dạng VD phải in QUY TRÌNH GIẢI BÀI ngay tại bài.")
    return warns


def check_duration(lesson: LessonPackage) -> list[str]:
    """Cảnh báo khi phiếu tầng lệch quỹ phút hoặc tỉ lệ (đọc chuẩn từ tier_spec)."""
    vdc_warns = check_vdc_cuoi_bai(lesson)
    tier = lesson.class_tier
    if not tier:
        return vdc_warns
    grade, subject = _grade_subject(lesson)
    try:
        spec = load_tier_spec()
        ratio_target = tier_ratio(spec, grade, subject, tier, getattr(lesson, "chuong", ""))
        block = subject_block(spec, grade, subject)
        rates = rates_for(spec, grade, subject)
    except KeyError:
        return vdc_warns                # chưa có rate card cho (lớp, môn, tầng)
    tier_block = block.get("tiers", {}).get(tier, {})
    warns_b = _luat_tang_b(lesson, spec, grade, subject, tier, tier_block)
    if not ratio_target:                # tầng chưa chốt tỉ lệ (X chuyên, hoặc tầng B
        return vdc_warns + warns_b      # chọn tỉ lệ theo chương mà phiếu chưa khai `chuong`)
    gop = gop_vd_vdc(spec, grade, subject, tier)

    budgets = block.get("budgets", {})
    budget_tol = block.get("budget_tol", 0.10)
    ratio_tol = block.get("ratio_tol", 5.0)
    seg_rate = {"onclass": rates.get("onclass", {}), "btvn": rates.get("btvn", {})}
    # Phiếu cố ý trải nhiều CA thì quỹ nhân lên bấy nhiêu (xem LessonPackage.so_ca),
    # không thì phiếu 2 ca nào cũng kêu "lệch quỹ" dù soạn đúng.
    ca = max(1, getattr(lesson, "so_ca", 1) or 1)
    budget_dict = {"onclass": budgets.get("onclass", 0.0) * ca,
                   "btvn": budgets.get("btvn", 0.0) * ca}

    counts = band_counts(lesson)        # {onclass|btvn: {band: n}}
    draws = draw_counts(lesson)         # {onclass|btvn: {band: số BÀI phải tự vẽ hình}}
    figs = figure_given_counts(lesson)  # {onclass|btvn: {band: số câu trên hình VẼ SẴN}}
    dm = draw_minutes(spec)
    qm = quick_minutes(spec)
    # Phút mỗi band = số câu × rate, trong đó câu trên HÌNH VẼ SẴN: band NB tính
    # quick_minutes (1′/câu), band khác chỉ tính nửa rate; cộng phút tự vẽ hình.
    def _band_minutes(seg: str, b: str) -> float:
        rate = seg_rate[seg].get(b, 0.0)
        n_fig = figs[seg][b]
        per_fig = qm if b == "NB" else rate * 0.5
        return (counts[seg][b] - n_fig) * rate + n_fig * per_fig + draws[seg][b] * dm

    minutes = {seg: {b: _band_minutes(seg, b) for b in _BANDS} for seg in budget_dict}

    warns: list[str] = vdc_warns + list(warns_b)
    label = {"onclass": "Luyện tập trên lớp", "btvn": "BTVN"}
    for seg, budget in budget_dict.items():
        total = sum(minutes[seg].values())
        if total == 0:
            continue
        c, m = counts[seg], minutes[seg]
        n_draw = sum(draws[seg].values())
        detail = (f"NB {c['NB']} câu/{m['NB']:.0f}′ · TH {c['TH']} câu/{m['TH']:.0f}′ "
                  f"· VD {c['VD']} câu/{m['VD']:.0f}′"
                  + (f" · VDC {c['VDC']} câu/{m['VDC']:.0f}′" if c["VDC"] or m["VDC"] else "")
                  + (f" (gồm {n_draw} bài tự vẽ hình ×{dm:.0f}′)" if n_draw else "")
                  + f" = {total:.0f}′")
        if budget and abs(total - budget) > budget * budget_tol:
            warns.append(
                f"duration: {label[seg]} {total:.0f}′ lệch quỹ {budget:.0f}′ "
                f"quá ±{budget_tol*100:.0f}% — {detail}.")
        if seg != "onclass":            # 40-40-20 là tỉ lệ giờ TRÊN LỚP
            continue
        seg_min = dict(minutes[seg])
        if gop:      # Thầy chốt 30/08/2026: tầng B soi VD và VDC như MỘT khối
            seg_min["VD"] = seg_min.get("VD", 0.0) + seg_min.pop("VDC", 0.0)
        for band, target in ratio_target.items():
            if target == 0 and seg_min.get(band, 0) == 0:
                continue                # band không dùng ở tầng này & không xuất hiện
            share = seg_min.get(band, 0.0) / total * 100
            if abs(share - target) > ratio_tol:
                ten = "VD+VDC" if (gop and band == "VD") else band
                warns.append(
                    f"duration: {label[seg]} tỉ lệ {ten} = {share:.0f}% lệch chuẩn "
                    f"{target:.0f}% quá ±{ratio_tol:.0f} điểm (tier_spec {tier}) — {detail}.")
    return warns
