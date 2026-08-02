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

from src.schema.tier_spec import (
    BANDS, draw_minutes, load_tier_spec, quick_minutes, rates_for, subject_block,
)

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
    # Bài HÌNH đề không cho sẵn hình ⇒ HS phải tự vẽ, tốn thêm `draw_minutes` (5′).
    # Đếm theo BÀI (một bài vẽ một hình dùng cho mọi ý), KHÔNG theo ý a),b),c…
    ve_hinh: dict[str, int] = Field(
        default_factory=dict,
        description="Số HÌNH HS phải tự vẽ mỗi đoạn, vd {'onclass': 2, 'btvn': 1}; mỗi hình +draw_minutes",
    )
    # Dòng dạng gồm câu TRẮC NGHIỆM / ĐIỀN KHUYẾT trên hình VẼ SẴN (Thầy chốt
    # 2026-07-27). Rate hình ×2 trả cho khâu dựng hình + trình bày; những câu này
    # không có hai khâu đó nên phút/câu về lại mức đại số (×0,5). Không áp cho dòng
    # có `ve_hinh` (mâu thuẫn: vừa vẽ sẵn vừa bắt HS vẽ).
    hinh_san: bool = Field(
        False, description="Dạng trắc nghiệm/điền khuyết trên hình vẽ sẵn → phút/câu ×0,5"
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
    thoiluong: list[str] = Field(
        default_factory=list,
        description="THỜI LƯỢNG đối chiếu SGK/PPCT, vd 'Buổi 1 — Bài 7 + Bài 8: 1 ca'; "
                    "bản mẫu Thầy duyệt (lớp 7) luôn có mục này để thấy lệch bao nhiêu tiết",
    )
    lythuyet: list[str] = Field(default_factory=list, description="Bullet lý thuyết trọng tâm")
    vidu: list[str] = Field(default_factory=list, description="Bullet ví dụ GV làm mẫu")
    dang_vd: list[str] = Field(default_factory=list, description="Các dạng VẬN DỤNG trong đề")
    loisai: list[str] = Field(default_factory=list, description="Lỗi sai thường gặp")
    kienthuc_nb: list[str] = Field(default_factory=list, description="Kiến thức NHẬN BIẾT cần nhớ")
    phieu: list[SpecPhieu] = Field(default_factory=list)


# ── Tính toán thời gian / tổng từ tier_spec (renderer dùng) ──────────────────

_SEG_ATTRS = ("vidu", "onclass", "btvn")  # cột có band-rate; lythuyet tính theo vidu-rate


def row_minutes(row: SpecRow, rates: dict) -> dict[str, float]:
    """Phút mỗi đoạn của 1 dòng = số câu × phút/câu(đoạn, band) + số hình HS tự vẽ
    × `draw_minutes` (bài hình vẽ hình tốn thêm — Thầy chốt 2026-07-26).

    Dòng khai `hinh_san` (trắc nghiệm/điền khuyết trên hình vẽ sẵn): band NB tính
    `quick_minutes` (1′/câu — Thầy chốt 2026-07-27), band TH/VD chỉ giảm NỬA rate
    (tự luận điền khuyết vẫn phải tính toán, chỉ đỡ khâu dựng hình)."""
    ts = load_tier_spec()
    dm = draw_minutes(ts)

    def per_cau(seg: str) -> float:
        rate = rates.get(seg, {}).get(row.band, 0.0)
        if not row.hinh_san:
            return rate
        return quick_minutes(ts) if row.band == "NB" else rate * 0.5

    return {seg: getattr(row, seg) * per_cau(seg) + row.ve_hinh.get(seg, 0) * dm
            for seg in _SEG_ATTRS}


def phieu_band_counts(phieu: SpecPhieu) -> dict[str, dict[str, int]]:
    """Tổng số câu theo {đoạn: {band: count}} của 1 phiếu (để so spec_gate sau)."""
    out = {seg: {b: 0 for b in BANDS} for seg in _SEG_ATTRS}
    for r in phieu.rows:
        for seg in _SEG_ATTRS:
            out[seg][r.band] += getattr(r, seg)
    return out


def phieu_band_minutes(phieu: SpecPhieu, rates: dict) -> dict[str, dict[str, float]]:
    """Phút theo {đoạn: {band: phút}} — ĐÃ gồm phút vẽ hình (`ve_hinh`), cộng vào
    band của chính dòng dạng. Dùng để soi tỉ lệ NB-TH-VD, cho khớp `duration_gate`
    (bên đó phút vẽ hình cũng tính vào band của bài)."""
    out = {seg: {b: 0.0 for b in BANDS} for seg in _SEG_ATTRS}
    for r in phieu.rows:
        m = row_minutes(r, rates)
        for seg in _SEG_ATTRS:
            out[seg][r.band] += m[seg]
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
