"""thuyetminh_gate — soi GIỜ VÔ LÝ trong phiếu THUYẾT MINH (spec) TRƯỚC khi Thầy chốt.

`duration_gate` chỉ soi phiếu JSON đã điền; còn spec (hợp đồng số câu) trước nay chỉ
có hàm TÍNH giờ (`thuyetminh_spec.phieu_totals`) chứ không có ai gác. Gate này lấp chỗ
đó: dùng ĐÚNG hằng số `config/tier_spec.json` mà duration_gate dùng (budgets / rates /
tier_ratio / tolerance) nên spec và phiếu nhất quán.

Hai mức:
  • errors (CHẶN build): giờ BẤT KHẢ THI / gần như chắc gõ nhầm số — soi TỪNG PHIẾU
      (mỗi phiếu = 1 buổi, khớp duration_gate; unit ≥2 phiếu = ≥2 buổi, KHÔNG cộng dồn):
      giờ trên lớp một phiếu > quỹ buổi (session − break); một dạng nuốt cả quỹ
      onclass; band VDC ở tầng cấm VDC; phiếu rỗng giờ.
  • warnings (KHÔNG chặn): mất cân — lệch quỹ/tỉ lệ quá ±tol, BTVN hụt quỹ.

Tầng chưa chốt tỉ lệ (X chuyên) hoặc (lớp, môn) chưa có rate card → bỏ qua êm.
"""
from __future__ import annotations

import re

from src.schema.thuyetminh_spec import (
    META_MARK_BEGIN,
    META_MARK_END,
    ThuyetMinhSpec,
    phieu_band_minutes,
    phieu_totals,
    rates_for_spec,
    row_minutes,
    session_info,
)
from src.schema.exam_bank import lookup as bank_lookup
from src.schema.tier_spec import BANDS, load_tier_spec, subject_block, tier_ratio

# Một dạng (row) chiếm quá tỉ lệ này của quỹ onclass cả buổi ⇒ nghi gõ nhầm số câu.
_ROW_HOG_FRAC = 0.60
_BAND_RANK = {b: i for i, b in enumerate(BANDS)}


def _source_ref_band_warnings(spec_rows, tag: str) -> list[str]:
    """Cảnh báo khi source_refs trỏ câu bank lệch band ≥2 mức so với band row khai
    (vd row 'NB' nhưng trỏ câu 'VDC'). An toàn: bỏ qua id không khớp/không có band."""
    warns: list[str] = []
    for i, r in enumerate(spec_rows):
        refs = getattr(r, "source_refs", None) or []
        if not refs:
            continue
        # Dòng loại "… tách …" / "… ghép bài" CỐ Ý trỏ về bài GỐC khó hơn: 'NB tách TH'
        # là bước đệm cắt ra từ chính bài TH/VD đó, nên lệch band là ĐÚNG chứ không sai.
        # Không bỏ qua thì mỗi phiếu dựng theo §4b đều kêu oan hàng loạt.
        lab = (getattr(r, "loai", "") or "").strip()
        if "tách" in lab or "ghép" in lab:
            continue
        for cid, rec in bank_lookup(refs):
            cb = rec.get("band")
            if cb not in _BAND_RANK:
                continue
            if abs(_BAND_RANK[cb] - _BAND_RANK[r.band]) >= 2:
                warns.append(
                    f"thuyetminh: {tag} dạng [{i}] khai band {r.band} nhưng source_refs "
                    f"'{cid}' là band {cb} (lệch ≥2 mức) — soát lại band/nguồn.")
    return warns


def check_thuyetminh(spec: ThuyetMinhSpec) -> tuple[list[str], list[str]]:
    """Trả (errors, warnings). errors CHẶN build; warnings chỉ cảnh báo.

    Tầng/lớp chưa có chuẩn giờ ⇒ bỏ phần soi GIỜ, nhưng vẫn soi phần NỘI DUNG
    (§4b, giàn giáo, nguồn câu) — xem _noi_dung_warnings."""
    # Soi NỘI DUNG trước và LUÔN LUÔN chạy. Trước 14/08/2026 mấy cổng này nằm sau
    # `return [], []` ở dưới nên hễ (lớp, môn, tầng) chưa có trong tier_spec là im
    # hoàn toàn — chính vì vậy bản mẫu chương IV lớp 7 tầng C (tier_spec chỉ có tầng B)
    # đi qua mà KHÔNG một cổng nào lên tiếng.
    noi_dung = _noi_dung_errors(spec)

    try:
        ts = load_tier_spec()
        block = subject_block(ts, spec.grade, spec.subject)
        rates = rates_for_spec(spec)
        ratio_target = tier_ratio(ts, spec.grade, spec.subject, spec.tier)
    except KeyError:
        return noi_dung, [
            f"thuyetminh: CHƯA có chuẩn giờ cho {spec.grade}/{spec.subject} tầng "
            f"{spec.tier} trong tier_spec.json — ĐÃ BỎ QUA toàn bộ cổng giờ/tỉ lệ "
            f"(quỹ buổi, tỉ lệ NB-TH-VD). Thêm tầng vào tier_spec để được soi."]

    info = session_info(spec)
    session = info.get("session_minutes") or 0
    brk = info.get("break_minutes") or 0
    budgets = info.get("budgets", {})
    budget_tol = block.get("budget_tol", 0.10)
    ratio_tol = block.get("ratio_tol", 5.0)

    # Quỹ giờ được nhân theo `so_ca` của TỪNG phiếu ngay trong vòng lặp dưới.
    tier_block = block.get("tiers", {}).get(spec.tier, {})
    vdc_allowed = bool(ratio_target and ratio_target.get("VDC", 0) > 0) and \
        tier_block.get("max_level", 4) >= 4

    errors: list[str] = []
    warnings: list[str] = []

    # Budget + tỉ lệ áp cho TỪNG PHIẾU — mỗi phiếu = 1 BUỔI (khớp duration_gate;
    # unit nhiều tuần như tuần 6-7 hay [C]tuần 10-11 có ≥2 phiếu = ≥2 buổi, KHÔNG cộng dồn).
    def _budget_warn(tag: str, label: str, total: float, budget: float):
        if budget and abs(total - budget) > budget * budget_tol:
            warnings.append(
                f"thuyetminh: {tag} {label} {total:.0f}′ lệch quỹ {budget:.0f}′ "
                f"quá ±{budget_tol*100:.0f}%.")

    for p in spec.phieu:
        # Phiếu cố ý trải nhiều CA (vd 1 phiếu dày dạy trong 2 buổi) thì quỹ giờ nhân
        # lên bấy nhiêu — không thì mọi phiếu ≥2 ca đều bị chặn oan "vượt quỹ MỘT BUỔI".
        ca = max(1, getattr(p, "so_ca", 1) or 1)
        onclass_budget = budgets.get("onclass", 0.0) * ca
        vidu_budget = budgets.get("vidu", 0.0) * ca
        btvn_budget = budgets.get("btvn", 0.0) * ca
        usable = ((session - brk) * ca) if session else 0

        tag = f"phiếu {p.code}" + (f" ({ca} ca)" if ca > 1 else "")
        m = phieu_totals(p, rates)["minutes"]
        on_min = m.get("onclass", 0.0)
        btvn_min = m.get("btvn", 0.0)
        # GV giảng = LÝ THUYẾT + ví dụ, đúng như dòng "Cân buổi" in trên PDF. Trước
        # 14/08/2026 chỉ so phần ví dụ nên phiếu chất 21′ lý thuyết vẫn qua cổng êm,
        # còn PDF thì hiện "GV giảng ≈46′ (quỹ 25′)" — Thầy đọc thấy vô lý mà gate im.
        lt_min = sum(r.lythuyet * rates.get("vidu", {}).get(r.band, 0.0) for r in p.rows)
        vidu_min = m.get("vidu", 0.0) + lt_min

        # (E) phiếu rỗng giờ — không có gì để dạy/làm
        if on_min == 0 and vidu_min == 0:
            errors.append(f"thuyetminh: {tag} RỖNG GIỜ — không có ví dụ lẫn bài luyện tập trên lớp.")
            continue

        # (E) một DẠNG nuốt quá nửa quỹ onclass ⇒ gần như chắc gõ nhầm số câu
        if onclass_budget:
            for i, r in enumerate(p.rows):
                rm = row_minutes(r, rates).get("onclass", 0.0)
                if rm > onclass_budget * _ROW_HOG_FRAC:
                    errors.append(
                        f"thuyetminh: {tag} dạng [{i}] '{r.dang[:40]}' chiếm {rm:.0f}′ "
                        f"= {rm/onclass_budget*100:.0f}% quỹ onclass {onclass_budget:.0f}′ "
                        f"(onclass={r.onclass} câu) — nghi gõ nhầm số câu.")

        # (W) source_refs trỏ câu bank lệch band so với row khai
        warnings.extend(_source_ref_band_warnings(p.rows, tag))

        # (E) band VDC ở tầng cấm VDC
        if not vdc_allowed:
            vdc_rows = [i for i, r in enumerate(p.rows) if r.band == "VDC"]
            if vdc_rows:
                errors.append(
                    f"thuyetminh: {tag} có dạng VDC (row {vdc_rows}) nhưng tầng {spec.tier} "
                    f"({spec.grade}/{spec.subject}) KHÔNG cho VDC — bỏ hoặc hạ band.")

        # (W) tỉ lệ NB-TH-VD(-VDC) trên lớp lệch chuẩn tầng
        if ratio_target and on_min > 0:
            band_min = phieu_band_minutes(p, rates)["onclass"]   # gồm cả phút vẽ hình
            for band, target in ratio_target.items():
                share = band_min.get(band, 0.0) / on_min * 100
                if target == 0 and band_min.get(band, 0.0) == 0:
                    continue
                if abs(share - target) > ratio_tol:
                    warnings.append(
                        f"thuyetminh: {tag} tỉ lệ {band} = {share:.0f}% lệch chuẩn {target:.0f}% "
                        f"quá ±{ratio_tol:.0f} điểm (tier_spec {spec.tier}).")

        # (E) phiếu (1 buổi) vượt quỹ giờ trên lớp
        on_class = vidu_min + on_min
        if usable and on_class > usable * (1 + budget_tol):
            errors.append(
                f"thuyetminh: {tag} giờ TRÊN LỚP {on_class:.0f}′ (ví dụ {vidu_min:.0f}′ + "
                f"luyện tập {on_min:.0f}′) VƯỢT quỹ {'MỘT BUỔI' if ca == 1 else f'{ca} BUỔI'} "
                f"{usable:.0f}′ ({ca}×({session}′ − giải lao {brk}′)) quá "
                f"±{budget_tol*100:.0f}% — không dạy kịp.")

        # (W) lệch quỹ phiếu (vidu / onclass / btvn-hụt)
        _budget_warn(tag, "ví dụ GV giảng", vidu_min, vidu_budget)
        _budget_warn(tag, "luyện tập trên lớp", on_min, onclass_budget)
        if btvn_budget and btvn_min < btvn_budget * (1 - budget_tol):
            warnings.append(
                f"thuyetminh: {tag} BTVN {btvn_min:.0f}′ HỤT quỹ {btvn_budget:.0f}′ "
                f"(>{budget_tol*100:.0f}%) — BTVN nên thừa hơn thiếu.")

    errors += noi_dung
    return errors, warnings


# ── Giàn giáo NB bắt buộc + nguồn câu (Thầy chốt 14/08/2026) ────────────────
# Rút từ BẢN MẪU ĐÃ DUYỆT: thuyết minh chương IV lớp 7 tầng C (6 phiếu).
#   • "Vẽ hình từ giả thiết + đánh dấu dữ kiện": có ở 6/6 phiếu — dạng NB này không
#     dạy thêm kiến thức, nó gác khâu HS hay mất điểm nhất là dựng hình.
#   • "Điền khuyết bài giải/chứng minh mẫu": bản mẫu mới có ở 3/6 phiếu, nhưng Thầy
#     chốt BẮT BUỘC cả hai ⇒ 3 phiếu kia coi như còn sót.
# Nhận dạng theo TỪ KHOÁ trong `dang` vì đó đúng là ngôn ngữ bản mẫu đang dùng.
# Giàn giáo "vẽ hình" chỉ bắt buộc với môn HÌNH — phiếu đại số không có hình để vẽ.
_SUBJ_CAN_HINH = ("hinh-hoc",)
# Loại §4b DUY NHẤT được phép tự soạn (Thầy chốt: "NB lẻ dạng lý thuyết thì được,
# còn lại thì nghiêm cấm bịa, phải trích dẫn ngay trong phiếu thuyết minh").
LOAI_MIEN_TRICH_DAN = "NB lẻ LT"


def check_scaffold_rails(spec: ThuyetMinhSpec) -> list[str]:
    """Mỗi phiếu phải có ĐỦ hai giàn giáo NB: 've-hinh' (môn hình) và 'dien-khuyet'.
    Khai bằng trường `gian_giao` của dòng, không dò từ khoá."""
    out: list[str] = []
    can_hinh = spec.subject in _SUBJ_CAN_HINH
    for p in spec.phieu:
        co = {r.gian_giao for r in p.rows if r.band == "NB"}
        thieu = []
        if can_hinh and "ve-hinh" not in co:
            thieu.append("'ve-hinh' (vẽ hình từ giả thiết + đánh dấu dữ kiện)")
        if "dien-khuyet" not in co:
            thieu.append("'dien-khuyet' (điền khuyết bài giải/chứng minh mẫu)")
        if thieu:
            out.append(
                f"thuyetminh: phiếu {p.code} THIẾU giàn giáo NB bắt buộc: "
                f"{' và '.join(thieu)} — mỗi phiếu phải có đủ (bản mẫu lớp 7 chương IV). "
                f"Khai bằng trường `gian_giao` ở dòng NB tương ứng.")
    return out


def check_source_refs(spec: ThuyetMinhSpec) -> list[str]:
    """KHÔNG BỊA ĐỀ: mọi dòng phải trỏ nguồn, TRỪ dòng loại 'NB lẻ LT' (câu hỏi thẳng
    lý thuyết vừa học — được tự soạn).

    Dòng 'NB tách TH' / 'TH tách VD' / '… ghép bài' thì trỏ chính BÀI GỐC mà nó cắt
    bước ra hoặc là một ý của nó."""
    out: list[str] = []
    for p in spec.phieu:
        thieu = [f"{r.band}{i}" for i, r in enumerate(p.rows, 1)
                 if not r.source_refs and (r.loai or "").strip() != LOAI_MIEN_TRICH_DAN]
        if thieu:
            out.append(
                f"thuyetminh: phiếu {p.code} — {len(thieu)}/{len(p.rows)} dòng BỊA ĐỀ "
                f"(chưa trỏ nguồn `source_refs`, mà loại không phải "
                f"'{LOAI_MIEN_TRICH_DAN}'): {', '.join(thieu[:8])}"
                + (" …" if len(thieu) > 8 else ""))
    return out


def check_chuong_level(spec: ThuyetMinhSpec) -> list[str]:
    """Thầy chốt 14/08/2026: TỪ GIỜ CHỈ LÀM THUYẾT MINH CẤP CHƯƠNG, mọi khối.
    Nhận biết qua slug/tiêu đề có chữ 'chuong'/'chương' (spec theo tuần thì không)."""
    dau = f"{spec.slug} {spec.title}".lower()
    if "chuong" in dau or "chương" in dau:
        return []
    return [f"thuyetminh: spec '{spec.slug}' KHÔNG phải cấp CHƯƠNG — từ 14/08/2026 chỉ "
            f"làm thuyết minh cấp chương (mọi khối). Gộp các buổi của cả chương vào "
            f"MỘT spec, mỗi buổi là một phiếu."]


def _noi_dung_errors(spec: ThuyetMinhSpec) -> list[str]:
    """Cổng NỘI DUNG — CHẶN build (Thầy yêu cầu 'codebase NGHIÊM NGẶT' 14/08/2026).
    Không phụ thuộc chuẩn giờ nên luôn chạy được. `--force` vẫn qua để build nháp."""
    return (check_chuong_level(spec) + check_loai_4b(spec)
            + check_scaffold_rails(spec) + check_source_refs(spec))


# ── Cổng XUỐNG DÒNG cho BẢNG ĐẦU (Tên bài / Thời gian / Thời lượng) ─────────
# Thầy phản hồi 14/08/2026: "bảng đầu để khá ríu rít… có dấu bullet mà lại không
# xuống dòng, thành ra RẤT KHÓ ĐỌC". Nguyên nhân: renderer nối 6 phiếu bằng ';' và
# nối `thoiluong` bằng '$\bullet$' NẰM NGANG trong ô p{22,4cm} → cả ô là một đoạn văn.
# Cổng này soi LaTeX ĐÃ RENDER (không soi spec) vì lỗi nằm ở khâu render.

# Số ký tự NHÌN THẤY tối đa của một đoạn không ngắt dòng trong ô bảng đầu.
# Một dòng phiếu dài nhất hiện nay ~80 ký tự; dòng "Thời gian" ~90 → 220 vẫn rộng cửa,
# mà đoạn dồn 6 phiếu (~500) thì trượt.
_MAX_RUN_CHARS = 220
_META_ROW = re.compile(r"^(?P<lbl>[^&]+?)\s*&\s*(?P<val>.*?)\s*\\\\\s*\\hline\s*$")
_TEX_CMD = re.compile(r"\\[A-Za-z@]+\s*|\\[^A-Za-z]")
# Mọi cách ngắt dòng hợp lệ bên trong một ô p{}
_BREAKS = (r"\newline", r"\par", r"\item", r"\\")


def _visible_len(tex: str) -> int:
    """Số ký tự Thầy THỰC SỰ nhìn thấy (bỏ lệnh LaTeX, ngoặc, $, ~)."""
    s = _TEX_CMD.sub(" ", tex)
    s = re.sub(r"[{}$~^_&]", "", s)
    return len(re.sub(r"\s+", " ", s).strip())


def check_meta_wrap(tex: str) -> list[str]:
    """Soi BẢNG ĐẦU của thuyết minh ĐÃ RENDER: ô nào nhiều mục mà không xuống dòng,
    hoặc có đoạn liền quá dài → RẤT KHÓ ĐỌC. Trả danh sách lỗi (CHẶN build).

    Không thấy mốc META (bản render cũ / template khác) ⇒ trả [] chứ không báo lỗi."""
    i, j = tex.find(META_MARK_BEGIN), tex.find(META_MARK_END)
    if i < 0 or j < 0 or j < i:
        return []

    out: list[str] = []
    for line in tex[i:j].splitlines():
        m = _META_ROW.match(line.strip())
        if not m:
            continue
        label = re.sub(r"\s+", " ", _TEX_CMD.sub("", m.group("lbl"))).strip() or "(không tên)"
        val = m.group("val")

        n_items = val.count(r"$\bullet$")
        n_breaks = sum(val.count(b) for b in _BREAKS)
        if n_items >= 2 and n_breaks == 0:
            out.append(
                f"thuyetminh: bảng đầu — ô '{label}' có {n_items} mục (chấm đầu dòng) "
                f"nhưng KHÔNG xuống dòng: cả ô dồn thành một đoạn, Thầy đọc rất khó. "
                f"Dùng _cell_lines() để mỗi mục một dòng.")
            continue

        # Đoạn liền dài nhất giữa hai chỗ ngắt dòng
        chunks = re.split(r"\\newline|\\par\b|\\item|\\\\", val)
        worst = max((_visible_len(c) for c in chunks), default=0)
        if worst > _MAX_RUN_CHARS:
            out.append(
                f"thuyetminh: bảng đầu — ô '{label}' có đoạn liền {worst} ký tự "
                f"(quá {_MAX_RUN_CHARS}) không xuống dòng — RẤT KHÓ ĐỌC. "
                f"Tách thành nhiều mục, mỗi mục một dòng.")
    return out


# Bảy loại câu hỏi §4b (HUONG-DAN-THUYET-MINH-LOP-C §4b, Thầy chốt 2026-08-05).
# Tên file có chữ "LOP-C" nhưng luật áp cho MỌI tầng, MỌI khối.
LOAI_4B = ("NB lẻ LT", "NB tách TH", "NB ghép bài",
           "TH lẻ LT", "TH ghép bài", "TH tách VD", "VD lẻ")


def check_loai_4b(spec: ThuyetMinhSpec) -> list[str]:
    """Cảnh báo dòng spec chưa khai `loai`, hoặc khai nhãn không thuộc 7 loại §4b,
    hoặc nhãn lệch band của chính dòng đó ('TH lẻ LT' nằm ở dòng band NB).

    VÌ SAO CÓ HÀM NÀY: trước 2026-08-12 `loai` chỉ được ĐỌC ở renderer để quyết định
    có in cột hay không — không khai thì cột lặng lẽ biến mất, gate im, PDF vẫn đẹp.
    Luật nằm ngoài code nên không thành quy trình; 39/41 spec trong repo bỏ trống."""
    out: list[str] = []
    for phieu in spec.phieu:
        thieu, sai, lech = [], [], []
        for i, r in enumerate(phieu.rows, 1):
            lab = (r.loai or "").strip()
            if not lab or lab.startswith("TODO"):
                thieu.append(f"{r.band}{i}")
            elif lab not in LOAI_4B:
                sai.append(f"{r.band}{i}='{lab}'")
            # §4b chỉ có nhãn cho NB/TH/VD — không có nhãn nào cho VDC. Dòng band VDC
            # (hợp lệ ở tầng B lớp 9, ratio VDC=10%) coi 'VD lẻ' là đúng, nếu không mọi
            # dòng VDC đều bị chặn oan khi §4b thành lỗi chặn (14/08/2026).
            elif lab.split()[0] != ("VD" if r.band == "VDC" else r.band):
                lech.append(f"{r.band}{i}='{lab}'")
        tag = f"phiếu {phieu.code}"
        if thieu:
            out.append(f"thuyetminh: {tag} — {len(thieu)}/{len(phieu.rows)} dòng CHƯA khai "
                       f"`loai` (§4b: {' | '.join(LOAI_4B)}): {', '.join(thieu[:8])}"
                       + (" …" if len(thieu) > 8 else ""))
        if sai:
            out.append(f"thuyetminh: {tag} — nhãn `loai` không thuộc 7 loại §4b: {', '.join(sai)}")
        if lech:
            out.append(f"thuyetminh: {tag} — nhãn `loai` lệch band của dòng: {', '.join(lech)}")
    return out
