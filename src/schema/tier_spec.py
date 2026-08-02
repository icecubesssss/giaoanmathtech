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
]

BANDS = ("NB", "TH", "VD", "VDC")
_DEFAULT_PATH = settings.CONFIG_DIR / "tier_spec.json"
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


def tier_ratio(spec: dict, grade: str, subject: str, tier: str) -> dict | None:
    """Tỉ lệ NB-TH-VD-VDC (%) của tầng; None nếu tầng chưa chốt (vd X chuyên)."""
    return subject_block(spec, grade, subject)["tiers"][tier].get("ratio")


def target_counts(spec: dict, grade: str, subject: str, tier: str) -> dict:
    """Số câu MỤC TIÊU mỗi đoạn×band cho (lớp, môn, tầng). {} nếu tầng chưa có tỉ lệ.

    Trả {seg: {band: int}} chỉ gồm band/đoạn > 0 — đây là 'hợp đồng' số câu mà
    phiếu phải khớp (±spec_count_tol)."""
    block = subject_block(spec, grade, subject)
    ratio = tier_ratio(spec, grade, subject, tier)
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
