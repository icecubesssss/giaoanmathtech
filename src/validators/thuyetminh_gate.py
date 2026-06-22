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

from src.schema.thuyetminh_spec import (
    ThuyetMinhSpec,
    phieu_band_counts,
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

    [] / [] khi không gate được (tầng/lớp chưa có chuẩn) — không phải lỗi."""
    try:
        ts = load_tier_spec()
        block = subject_block(ts, spec.grade, spec.subject)
        rates = rates_for_spec(spec)
        ratio_target = tier_ratio(ts, spec.grade, spec.subject, spec.tier)
    except KeyError:
        return [], []  # chưa có rate card cho (lớp, môn) hoặc tầng này

    info = session_info(spec)
    session = info.get("session_minutes") or 0
    brk = info.get("break_minutes") or 0
    budgets = info.get("budgets", {})
    budget_tol = block.get("budget_tol", 0.10)
    ratio_tol = block.get("ratio_tol", 5.0)

    onclass_budget = budgets.get("onclass", 0.0)
    vidu_budget = budgets.get("vidu", 0.0)
    btvn_budget = budgets.get("btvn", 0.0)
    usable = (session - brk) if session else 0  # quỹ phút THỰC trên lớp cả buổi

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
        tag = f"phiếu {p.code}"
        m = phieu_totals(p, rates)["minutes"]
        on_min = m.get("onclass", 0.0)
        vidu_min = m.get("vidu", 0.0)
        btvn_min = m.get("btvn", 0.0)

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
            bc = phieu_band_counts(p)["onclass"]
            on_rate = rates.get("onclass", {})
            band_min = {b: bc.get(b, 0) * on_rate.get(b, 0.0) for b in BANDS}
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
                f"luyện tập {on_min:.0f}′) VƯỢT quỹ MỘT BUỔI {usable:.0f}′ "
                f"({session}′ − giải lao {brk}′) quá ±{budget_tol*100:.0f}% — không dạy kịp.")

        # (W) lệch quỹ phiếu (vidu / onclass / btvn-hụt)
        _budget_warn(tag, "ví dụ GV giảng", vidu_min, vidu_budget)
        _budget_warn(tag, "luyện tập trên lớp", on_min, onclass_budget)
        if btvn_budget and btvn_min < btvn_budget * (1 - budget_tol):
            warnings.append(
                f"thuyetminh: {tag} BTVN {btvn_min:.0f}′ HỤT quỹ {btvn_budget:.0f}′ "
                f"(>{budget_tol*100:.0f}%) — BTVN nên thừa hơn thiếu.")

    return errors, warnings
