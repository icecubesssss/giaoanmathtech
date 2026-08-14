"""de_gate — soi ĐỀ VÔ LÝ trong thuyết minh đề TRƯỚC khi Thầy chốt & người ra đề viết đề.

Cùng triết lí với `thuyetminh_gate`: hằng số lấy từ `config/tier_spec.json` (tier_ratio)
nên đề và phiếu nhất quán tầng.

Hai mức:
  • errors (CHẶN build): Σ điểm lệch thang điểm; Σ phút VƯỢT thời gian làm bài; mã câu
      trùng; band VDC ở tầng cấm VDC; đề rỗng câu.
  • warnings: đề hụt giờ (HS làm xong quá sớm); VD chiếm quá nhiều so với chuẩn tầng;
      đề không có câu NB nào; đề 100% tự luận (AGENTS §4c đòi đan xen hình thức).
"""
from __future__ import annotations

from collections import Counter

from src.schema.de_spec import DeSpec, band_share, de_totals
from src.schema.tier_spec import load_tier_spec, subject_block, tier_ratio

# Σ phút dưới ngưỡng này so với thời gian đề ⇒ đề quá ngắn, HS ngồi chơi.
_MIN_FILL = 0.70
# VD được phép vượt chuẩn tầng bao nhiêu ĐIỂM PHẦN TRĂM (đề kiểm tra dồn VD hơn phiếu).
_VD_SLACK = 10.0
# Sai số điểm cho phép khi cộng (số thực).
_DIEM_EPS = 0.01


def check_de(spec: DeSpec) -> tuple[list[str], list[str]]:
    """Trả (errors, warnings). errors CHẶN build; warnings chỉ cảnh báo."""
    try:
        ts = load_tier_spec()
        block = subject_block(ts, spec.grade, spec.subject)
        ratio_target = tier_ratio(ts, spec.grade, spec.subject, spec.tier)
    except KeyError:
        return [], []  # chưa có chuẩn cho (lớp, môn) này — bỏ qua êm, không phải lỗi

    tier_block = block.get("tiers", {}).get(spec.tier, {})
    vdc_allowed = bool(ratio_target and ratio_target.get("VDC", 0) > 0) and \
        tier_block.get("max_level", 4) >= 4

    errors: list[str] = []
    warnings: list[str] = []

    for de in spec.de:
        tag = f"đề {de.ma}"

        if not de.cau:
            errors.append(f"de: {tag} RỖNG — không có câu nào.")
            continue

        t = de_totals(de)

        # (E) tổng điểm phải khớp thang điểm
        if abs(t["tong_diem"] - de.diem_toi_da) > _DIEM_EPS:
            errors.append(
                f"de: {tag} Σ điểm {t['tong_diem']:.2f} ≠ thang điểm {de.diem_toi_da:.2f} "
                f"— cộng lại điểm từng câu.")

        # (E) HS không thể làm kịp
        if t["tong_phut"] > de.phut:
            errors.append(
                f"de: {tag} Σ phút làm bài {t['tong_phut']:.0f}′ VƯỢT thời gian đề "
                f"{de.phut}′ — HS không làm kịp.")

        # (E) mã câu trùng trong cùng một đề
        trung = sorted(m for m, n in Counter(c.ma for c in de.cau).items() if n > 1)
        if trung:
            errors.append(f"de: {tag} có mã câu TRÙNG: {trung}")

        # (E) VDC ở tầng cấm
        if not vdc_allowed:
            vdc = [c.ma for c in de.cau if c.band == "VDC"]
            if vdc:
                errors.append(
                    f"de: {tag} có câu VDC ({vdc}) nhưng tầng {spec.tier} KHÔNG cho VDC "
                    f"— bỏ hoặc hạ band.")

        # (W) đề quá ngắn so với thời gian cho phép
        if t["tong_phut"] < de.phut * _MIN_FILL:
            warnings.append(
                f"de: {tag} Σ phút {t['tong_phut']:.0f}′ mới bằng "
                f"{t['tong_phut']/de.phut*100:.0f}% thời gian đề {de.phut}′ — đề hơi ngắn.")

        # (W) VD chiếm quá nhiều so với chuẩn tầng
        if ratio_target:
            share = band_share(de)
            tran = ratio_target.get("VD", 0) + _VD_SLACK
            if share["VD"] > tran:
                warnings.append(
                    f"de: {tag} VD chiếm {share['VD']:.0f}% thời gian, vượt trần "
                    f"{tran:.0f}% của tầng {spec.tier} — tầng này ăn điểm ở NB+TH.")

        # (W) không có câu NB — tầng C mất chỗ gỡ điểm
        if not any(c.band == "NB" for c in de.cau):
            warnings.append(f"de: {tag} KHÔNG có câu NB nào — tầng {spec.tier} mất chỗ gỡ điểm.")

        # (W) đề 100% tự luận (AGENTS §4c)
        if all(c.hinh_thuc == "tự luận" for c in de.cau):
            warnings.append(
                f"de: {tag} 100% tự luận — §4c đòi đan xen trắc nghiệm / điền khuyết / "
                f"đúng-sai để soi nhanh khái niệm.")

    return errors, warnings
