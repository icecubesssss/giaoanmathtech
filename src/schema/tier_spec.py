"""Đọc `config/tier_spec.json` — RATE CARD cố định theo tầng lớp.

Nguồn sự thật máy-đọc cho số câu NB/TH/VD/VDC (trước đây cứng trong duration_gate
+ văn bản HUONG-DAN-PHAN-TANG-LOP §2). Dùng bởi: duration_gate (Bước 4), spec_builder
(Bước 3), spec_gate. Công thức số câu mục tiêu mỗi band/đoạn:

    count = round( budget_phút(đoạn) × tỉ_lệ(band)/100 ÷ phút_mỗi_câu(đoạn, band) )
"""
from __future__ import annotations

import json
from pathlib import Path

from config import settings

__all__ = [
    "load_tier_spec", "subject_block", "rates_for", "tier_ratio",
    "target_counts", "draw_minutes", "BANDS",
    "load_ban_do", "chuong_co_vd", "gop_vd_vdc", "so_ca_yeu_cau",
    "phan_bo_vdc", "muc_tieu_vdc",
]

BANDS = ("NB", "TH", "VD", "VDC")
_DEFAULT_PATH = settings.CONFIG_DIR / "tier_spec.json"
_BAN_DO_PATH = settings.CONFIG_DIR / "ban_do_vd_vdc.json"
_CACHE: dict[str, dict] = {}


def load_tier_spec(path: Path | None = None) -> dict:
    """Đọc (và cache) tier_spec.json."""
    p = path or _DEFAULT_PATH
    key = str(p)
    if key not in _CACHE:
        _CACHE[key] = json.loads(p.read_text(encoding="utf-8"))
    return _CACHE[key]


def subject_block(spec: dict, grade: str, subject: str) -> dict:
    """Khối cấu hình của (lớp, môn), vd ('lop-9','dai-so'). KeyError nếu chưa khai báo."""
    return spec["grades"][grade][subject]


def rates_for(spec: dict, grade: str, subject: str) -> dict:
    """Phút/câu mỗi đoạn×band cho (lớp, môn): gộp `rates` toàn cục với
    `rates_override` của khối (override thắng theo từng đoạn)."""
    block = subject_block(spec, grade, subject)
    merged = {seg: dict(bands) for seg, bands in spec["rates"].items() if not seg.startswith("_")}
    for seg, bands in block.get("rates_override", {}).items():
        merged.setdefault(seg, {}).update(bands)
    return merged


def draw_minutes(spec: dict) -> float:
    """Phút CỘNG THÊM cho mỗi hình HS phải TỰ VẼ (Thầy chốt 2026-07-26: 5′).

    Cộng theo BÀI (một bài chỉ vẽ hình một lần) chứ không theo ý a),b),c…"""
    return float(spec.get("draw_minutes", 0.0))


def quick_minutes(spec: dict) -> float:
    """Phút/câu cho câu NHẬN BIẾT trắc nghiệm / điền chỗ chấm trên HÌNH VẼ SẴN
    (Thầy chốt 2026-07-27: 1′ — "với mức độ này thì hs vẫn dùng 1p thôi").

    Thay hẳn rate của band NB, KHÔNG nhân rate hình ×2. Band TH/VD có khai hình
    vẽ sẵn thì vẫn phải tính toán nên chỉ giảm nửa rate, không dùng hằng số này."""
    return float(spec.get("quick_minutes", 0.0)) or 1.0


def load_ban_do(path: Path | None = None) -> dict:
    """Đọc (và cache) `config/ban_do_vd_vdc.json` — chương nào CÓ bài VD/VDC trong đề."""
    p = path or _BAN_DO_PATH
    key = "bando:" + str(p)
    if key not in _CACHE:
        _CACHE[key] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"khoi": {}}
    return _CACHE[key]


def _chuong_entry(grade: str, chuong: str) -> dict | None:
    """Bản ghi chương trong `config/ban_do_vd_vdc.json`; None nếu không tra ra.

    `chuong` khớp `slug`, `ma` (I, II, …) hoặc một trong `slug_khac` — cây seeds có
    nhiều biến thể tên folder cho cùng một chương."""
    if not chuong:
        return None
    khoi = load_ban_do().get("khoi", {}).get(grade)
    if not khoi:
        return None
    for c in khoi.get("chuong", []):
        if chuong in (c.get("slug"), c.get("ma"), *(c.get("slug_khac") or [])):
            return c
    return None


def phan_bo_vdc(grade: str, chuong: str) -> dict | None:
    """Chia khối 55% VD+VDC theo TẦN SUẤT VDC của chương (Thầy chốt 04/09/2026).

    Trả {"VD": .., "VDC": ..} lấy từ `vdc.phan_bo_55` của bản đồ; None khi chương chưa
    đo được tần suất (khối 6/7/8) ⇒ người gọi giữ nguyên tỉ lệ mặc định của tầng."""
    c = _chuong_entry(grade, chuong)
    if not c:
        return None
    pb = (c.get("vdc") or {}).get("phan_bo_55")
    if not pb or "VD" not in pb or "VDC" not in pb:
        return None
    return {"VD": int(pb["VD"]), "VDC": int(pb["VDC"])}


def muc_tieu_vdc(grade: str, chuong: str) -> tuple[str | None, float | None]:
    """(mục tiêu VDC, trần điểm) của chương — "an-tron" cho kỳ I (trần 10,0),
    "cham-diem-tung-phan" cho ý cuối bài hình kỳ II (trần 9,5). (None, None) nếu chưa đo."""
    c = _chuong_entry(grade, chuong)
    v = (c or {}).get("vdc") or {}
    return v.get("muc_tieu_vdc"), v.get("tran_diem")


def chuong_co_vd(grade: str, chuong: str) -> bool | str | None:
    """Chương này có bài VD/VDC trong đề kiểm tra định kì không?

    True / False = đã chốt · "bien" = Thầy CHƯA chốt · None = không tìm thấy chương.
    `chuong` khớp `slug` hoặc `ma` (I, II, …) trong config/ban_do_vd_vdc.json."""
    if not chuong:
        return None
    khoi = load_ban_do().get("khoi", {}).get(grade)
    if not khoi:
        return None
    for c in khoi.get("chuong", []):
        # `slug_khac`: cây seeds có nhiều biến thể tên folder cho cùng một chương
        # (chuong-1-he-pt / chuong-01-phuong-trinh-va-he-…), tra được cả hai.
        if chuong in (c.get("slug"), c.get("ma"), *(c.get("slug_khac") or [])):
            return c.get("co_vd")
    return None


def so_ca_yeu_cau(spec: dict, grade: str, subject: str, tier: str,
                  chuong: str | None = None) -> int | None:
    """Số CA (buổi) mà một phiếu của tầng này phải trải, theo chương.

    Anh An chốt 30/08/2026: chương KHÔNG có bài VD/VDC thì GỘP 2 PHIẾU THÀNH 1
    (so_ca = 2, mỗi buổi gánh 15% NB $+$ 35% TH); chương CÓ VD/VDC vẫn 1 phiếu 1 buổi.
    None = tầng không ràng buộc, hoặc chưa tra ra chương."""
    try:
        variants = subject_block(spec, grade, subject)["tiers"][tier].get("so_ca_variants")
    except KeyError:
        return None
    if not variants:
        return None
    co_vd = chuong_co_vd(grade, chuong or "")
    if co_vd is True:
        return variants.get("co_vd")
    if co_vd is False:
        return variants.get("khong_vd")
    return None


def gop_vd_vdc(spec: dict, grade: str, subject: str, tier: str) -> bool:
    """Tầng này soi tỉ lệ với VD và VDC GỘP làm một khối (Thầy chốt 30/08/2026)?"""
    try:
        return bool(subject_block(spec, grade, subject)["tiers"][tier].get("gop_vd_vdc"))
    except KeyError:
        return False


def tier_ratio(spec: dict, grade: str, subject: str, tier: str,
               chuong: str | None = None) -> dict | None:
    """Tỉ lệ NB-TH-VD-VDC (%) của tầng; None nếu tầng chưa chốt (vd X chuyên).

    Tầng khai `ratio_variants` (tầng B từ 30/08/2026) thì tỉ lệ phụ thuộc CHƯƠNG:
    tra `config/ban_do_vd_vdc.json` xem chương có bài VD/VDC trong đề hay không.
    Chưa biết chương, hoặc chương còn 'bien' (Thầy chưa chốt) ⇒ None để cổng KHÔNG
    gate bừa — thà không soi còn hơn soi theo tỉ lệ sai."""
    tier_block = subject_block(spec, grade, subject)["tiers"][tier]
    variants = tier_block.get("ratio_variants")
    if not variants:
        return tier_block.get("ratio")
    co_vd = chuong_co_vd(grade, chuong or "")
    if co_vd is True:
        ratio = variants.get("co_vd")
        # Thầy chốt 04/09/2026: khối 55% VD+VDC chia theo TẦN SUẤT VDC của chương —
        # chương nào VDC hay ra thì VDC được nhiều phút hơn. Chương chưa đo được tần
        # suất (khối 6/7/8) giữ nguyên biến thể mặc định.
        pb = phan_bo_vdc(grade, chuong or "")
        if ratio and pb:
            ratio = {**ratio, "VD": pb["VD"], "VDC": pb["VDC"]}
        return ratio
    if co_vd is False:
        return variants.get("khong_vd")
    return None


def target_counts(spec: dict, grade: str, subject: str, tier: str,
                  chuong: str | None = None) -> dict:
    """Số câu MỤC TIÊU mỗi đoạn×band cho (lớp, môn, tầng). {} nếu tầng chưa có tỉ lệ.

    Trả {seg: {band: int}} chỉ gồm band/đoạn > 0 — đây là 'hợp đồng' số câu mà
    phiếu phải khớp (±spec_count_tol). `chuong` cần cho tầng khai `ratio_variants`."""
    block = subject_block(spec, grade, subject)
    ratio = tier_ratio(spec, grade, subject, tier, chuong)
    if not ratio:
        return {}
    rates = rates_for(spec, grade, subject)
    out: dict[str, dict[str, int]] = {}
    for seg, budget in block["budgets"].items():
        if not budget or budget <= 0:
            continue
        seg_rates = rates.get(seg, {})
        seg_out: dict[str, int] = {}
        for band in BANDS:
            pct = ratio.get(band, 0)
            rate = seg_rates.get(band, 0)
            if pct <= 0 or rate <= 0:
                continue
            seg_out[band] = round(budget * pct / 100 / rate)
        if seg_out:
            out[seg] = seg_out
    return out
