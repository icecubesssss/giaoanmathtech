"""PHIẾU THUYẾT MINH (spec) — artifact MÁY-ĐỌC, là HỢP ĐỒNG chốt số câu trước khi soạn.

Quy trình mới (Thầy chốt): dựng spec này TRƯỚC → render PDF cho Thầy đọc & chỉnh &
KHOÁ → rồi mới 'bốc câu' theo spec. Số câu mỗi band do Thầy chốt ở đây; thời gian +
tổng do renderer TỰ TÍNH từ `config/tier_spec.json` (không gõ tay như script cũ).

Đơn vị 'câu' = ý nhỏ (đếm giờ), khớp duration_gate. `decompose` khai mức cắt bước
(scaffold-decompose) cho dòng bài giàu: vdc/vd/th2nb (xem AGENTS scaffold-decompose).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from src.schema.tier_spec import BANDS, load_tier_spec, rates_for, subject_block

Band = Literal["NB", "TH", "VD", "VDC"]


class SpecRow(BaseModel):
    """Một DẠNG bài trong phiếu, gắn band + số câu mỗi đoạn. Thời gian tự tính."""
    dang: str = Field(..., description="Mô tả dạng + nguồn, vd 'Giải BPT một bước (Bài 2 / BTVN 12)'")
    band: Band = Field(..., description="Mức nhận thức của dạng: NB/TH/VD/VDC")
    lythuyet: int = Field(0, ge=0, description="Số MỤC lý thuyết (GV chốt)")
    vidu: int = Field(0, ge=0, description="Số câu ví dụ mẫu (GV giảng)")
    onclass: int = Field(0, ge=0, description="Số câu luyện tập TRÊN LỚP")
    btvn: int = Field(0, ge=0, description="Số câu BÀI TẬP VỀ NHÀ")
    source_refs: list[str] = Field(default_factory=list, description="id câu bank để bốc, vd ['gk1-bat-trang-2c']")
    decompose: Literal["none", "vdc", "vd", "th2nb"] = Field(
        "none", description="Mức cắt bước: vdc→NB/TH/VD/VDC, vd→NB/TH, th2nb→2 NB; none=giữ nguyên"
    )


class SpecPhieu(BaseModel):
    """Một phiếu trong buổi (A = kỹ thuật, B = thực tế…)."""
    code: str = Field(..., description="Mã phiếu: A/B/C/D")
    title: str = Field(..., description="Tên phiếu")
    rows: list[SpecRow] = Field(default_factory=list)


class ThuyetMinhSpec(BaseModel):
    """Đặc tả 1 buổi học (≥1 phiếu) — hợp đồng số câu + nội dung khung."""
    slug: str
    title: str
    grade: str = Field("lop-9", description="vd lop-9")
    subject: str = Field("dai-so", description="vd dai-so")
    tier: str = Field("C", description="Tầng lớp A/B/C/X")
    tuan: str = Field("", description="vd '10-11'")
    lythuyet: list[str] = Field(default_factory=list, description="Bullet lý thuyết trọng tâm")
    vidu: list[str] = Field(default_factory=list, description="Bullet ví dụ GV làm mẫu")
    dang_vd: list[str] = Field(default_factory=list, description="Các dạng VẬN DỤNG trong đề")
    loisai: list[str] = Field(default_factory=list, description="Lỗi sai thường gặp")
    kienthuc_nb: list[str] = Field(default_factory=list, description="Kiến thức NHẬN BIẾT cần nhớ")
    phieu: list[SpecPhieu] = Field(default_factory=list)


# ── Tính toán thời gian / tổng từ tier_spec (renderer dùng) ──────────────────

_SEG_ATTRS = ("vidu", "onclass", "btvn")  # cột có band-rate; lythuyet tính theo vidu-rate


def row_minutes(row: SpecRow, rates: dict) -> dict[str, float]:
    """Phút mỗi đoạn của 1 dòng = số câu × phút/câu(đoạn, band)."""
    return {seg: getattr(row, seg) * rates.get(seg, {}).get(row.band, 0.0) for seg in _SEG_ATTRS}


def phieu_band_counts(phieu: SpecPhieu) -> dict[str, dict[str, int]]:
    """Tổng số câu theo {đoạn: {band: count}} của 1 phiếu (để so spec_gate sau)."""
    out = {seg: {b: 0 for b in BANDS} for seg in _SEG_ATTRS}
    for r in phieu.rows:
        for seg in _SEG_ATTRS:
            out[seg][r.band] += getattr(r, seg)
    return out


def phieu_totals(phieu: SpecPhieu, rates: dict) -> dict:
    """Tổng số câu + phút mỗi đoạn của phiếu."""
    counts = {seg: 0 for seg in _SEG_ATTRS}
    minutes = {seg: 0.0 for seg in _SEG_ATTRS}
    for r in phieu.rows:
        m = row_minutes(r, rates)
        for seg in _SEG_ATTRS:
            counts[seg] += getattr(r, seg)
            minutes[seg] += m[seg]
    return {"counts": counts, "minutes": minutes}


def rates_for_spec(spec: ThuyetMinhSpec) -> dict:
    """Phút/câu áp cho spec này (theo lớp/môn của spec)."""
    return rates_for(load_tier_spec(), spec.grade, spec.subject)


def session_info(spec: ThuyetMinhSpec) -> dict:
    """Thông tin buổi (phút buổi, giải lao, ngân sách) từ tier_spec."""
    block = subject_block(load_tier_spec(), spec.grade, spec.subject)
    return {
        "session_minutes": block.get("session_minutes"),
        "break_minutes": block.get("break_minutes"),
        "budgets": block.get("budgets", {}),
    }
