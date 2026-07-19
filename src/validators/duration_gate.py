"""duration_gate — kiểm thời lượng & tỉ lệ NB-TH-VD(-VDC) cho phiếu PHÂN TẦNG.

Số liệu (phút/câu, ngân sách, tỉ lệ) NAY đọc từ `config/tier_spec.json` (trước cứng
trong file này). Bảo toàn hành vi tầng C lớp 9 + B/C lớp 8; tổng quát cho mọi tầng
có rate card + thêm band VDC. Tầng chưa chốt tỉ lệ (X) → KHÔNG gate.

Quy ước đếm (Thầy chốt 2026-06-11):
  • "Câu" = ý nhỏ a),b),c)… (mỗi ý 1 câu); bài VD tách thì đếm theo thẻ [NB]/[TH]/
    [VD]/[VDC] đầu mỗi ý. KHÔNG đếm Khám phá/Khái niệm (giờ GV giảng).
  • Phút/câu + ngân sách + tỉ lệ: lấy từ tier_spec theo (lớp, môn, tầng).
  • Tỉ lệ áp cho TỪNG PHIẾU theo THỜI GIAN, sai số ±ratio_tol điểm %, CHỈ phần
    TRÊN LỚP (BTVN không thuộc tỉ lệ — chỉ giữ quỹ phút).
"""
from __future__ import annotations

import re

from src.schema.lesson_package import LessonPackage
from src.schema.tier_spec import load_tier_spec, subject_block, rates_for, tier_ratio

_TAG_RE = re.compile(r"\[(NB|TH|VD|VDC)\]")
# Ý a)…j) ở VỊ TRÍ LIỆT KÊ: chỉ tính khi trước nó là khoảng trắng / `]` (từ [[br]]) /
# `}` (sau minipage) / `>` / đầu chuỗi. Tránh đếm nhầm "b)" trong "(a+b)", "(a-b)"…
_ITEM_RE = re.compile(r"(?<![^\s\]>}])([a-j])\)")
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
    """Gom mỗi `problem` + các `para` đi liền sau thành 1 đơn vị đếm. CHỈ đếm chặng
    luyện tập/tổng kết (review/concept = giờ GV giảng, bỏ)."""
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
                           getattr(b, "level", 0), [b.statement or ""])
            elif typ == "para" and current:
                current[2].append(getattr(b, "text", "") or "")
            elif typ in ("noted", "mindmap"):
                if current:
                    yield current
                    current = None
        if current:
            yield current


def band_counts(lesson: LessonPackage) -> dict[str, dict[str, int]]:
    """Đếm số câu LUYỆN TẬP theo {onclass|btvn: {band: n}} — đơn vị ý nhỏ/thẻ mức.
    Dùng chung cho duration_gate (×rate ra phút) và spec_gate (so với spec)."""
    counts = {"onclass": {b: 0 for b in _BANDS}, "btvn": {b: 0 for b in _BANDS}}
    for seg, level, texts in _problem_units(lesson):
        if seg not in counts:                # extend… không thuộc quỹ giờ
            continue
        text = " ".join(texts)
        tags = _TAG_RE.findall(text)
        if tags:
            for band in tags:
                counts[seg][band] += 1
        else:
            counts[seg][_LEVEL_TO_BAND.get(level, "TH")] += _count_items(text)
    return counts


def _grade_subject(lesson: LessonPackage) -> tuple[str, str]:
    """Suy (lớp, môn) để tra tier_spec. Lesson chỉ có grade_label → phân lớp 8/9;
    phát hiện môn 'hinh-hoc' nếu eyebrow hoặc title chứa chữ 'hình'/'hinh'."""
    gl = getattr(lesson, "grade_label", "") or ""
    grade = "lop-8" if "Lớp 8" in gl else "lop-9"
    eyebrow = getattr(lesson, "eyebrow", "") or ""
    title = getattr(lesson, "title", "") or ""
    text_to_search = (eyebrow + " " + title).lower()
    subject = "hinh-hoc" if "hình" in text_to_search or "hinh" in text_to_search else "dai-so"
    return grade, subject


def check_duration(lesson: LessonPackage) -> list[str]:
    """Cảnh báo khi phiếu tầng lệch quỹ phút hoặc tỉ lệ (đọc chuẩn từ tier_spec)."""
    tier = lesson.class_tier
    if not tier:
        return []
    grade, subject = _grade_subject(lesson)
    try:
        spec = load_tier_spec()
        ratio_target = tier_ratio(spec, grade, subject, tier)
        block = subject_block(spec, grade, subject)
        rates = rates_for(spec, grade, subject)
    except KeyError:
        return []                       # chưa có rate card cho (lớp, môn, tầng)
    if not ratio_target:                # tầng chưa chốt tỉ lệ (vd X chuyên)
        return []

    budgets = block.get("budgets", {})
    budget_tol = block.get("budget_tol", 0.10)
    ratio_tol = block.get("ratio_tol", 5.0)
    seg_rate = {"onclass": rates.get("onclass", {}), "btvn": rates.get("btvn", {})}
    budget_dict = {"onclass": budgets.get("onclass", 0.0), "btvn": budgets.get("btvn", 0.0)}

    counts = band_counts(lesson)        # {onclass|btvn: {band: n}}
    minutes = {seg: {b: counts[seg][b] * seg_rate[seg].get(b, 0.0) for b in _BANDS}
               for seg in budget_dict}

    warns: list[str] = []
    label = {"onclass": "Luyện tập trên lớp", "btvn": "BTVN"}
    for seg, budget in budget_dict.items():
        total = sum(minutes[seg].values())
        if total == 0:
            continue
        c, m = counts[seg], minutes[seg]
        detail = (f"NB {c['NB']} câu/{m['NB']:.0f}′ · TH {c['TH']} câu/{m['TH']:.0f}′ "
                  f"· VD {c['VD']} câu/{m['VD']:.0f}′"
                  + (f" · VDC {c['VDC']} câu/{m['VDC']:.0f}′" if c["VDC"] or m["VDC"] else "")
                  + f" = {total:.0f}′")
        if budget and abs(total - budget) > budget * budget_tol:
            warns.append(
                f"duration: {label[seg]} {total:.0f}′ lệch quỹ {budget:.0f}′ "
                f"quá ±{budget_tol*100:.0f}% — {detail}.")
        if seg != "onclass":            # 40-40-20 là tỉ lệ giờ TRÊN LỚP
            continue
        for band, target in ratio_target.items():
            if target == 0 and minutes[seg].get(band, 0) == 0:
                continue                # band không dùng ở tầng này & không xuất hiện
            share = minutes[seg][band] / total * 100
            if abs(share - target) > ratio_tol:
                warns.append(
                    f"duration: {label[seg]} tỉ lệ {band} = {share:.0f}% lệch chuẩn "
                    f"{target:.0f}% quá ±{ratio_tol:.0f} điểm (tier_spec {tier}) — {detail}.")
    return warns
