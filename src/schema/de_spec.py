"""THUYẾT MINH ĐỀ KIỂM TRA (đặc tả đề) — artifact MÁY-ĐỌC, chốt cấu trúc đề TRƯỚC khi ra đề.

Song song với `thuyetminh_spec` (chốt số câu của PHIẾU), file này chốt **ma trận đề**:
mỗi đề gồm những câu nào, dạng gì, mức nào, mấy điểm, học sinh làm mấy phút. Thầy đọc
PDF rồi chỉnh & khoá, người ra đề mới bám theo mà viết đề thật.

VÌ SAO TÁCH KHỎI ThuyetMinhSpec: bảng của phiếu có 4 cột đoạn (Lý thuyết / Ví dụ /
BT trên lớp / BTVN) và tự tính giờ theo rate — đề kiểm tra không có đoạn nào trong số
đó, mà cần ĐIỂM và PHÚT LÀM BÀI do người ra đề quyết. Nhét vào cùng schema thì mọi
con số trên bảng đều sai nghĩa.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from src.schema.tier_spec import BANDS

Band = Literal["NB", "TH", "VD", "VDC"]

# Hình thức câu hỏi (AGENTS §4c — cấm đề 100% tự luận tính toán thuần).
HINH_THUC = ("trắc nghiệm", "điền khuyết", "đúng/sai", "nối cột", "tự luận")


class DeCau(BaseModel):
    """Một câu (hoặc một ý) trong đề — đơn vị chấm điểm."""
    ma: str = Field(..., description="Mã câu in trên đề, vd 'Câu 1' / 'Câu 4a'")
    dang: str = Field(..., description="Dạng bài + nguồn, vd 'Giải PT khuyết $c$ (khuôn Câu III.3 đề 2026)'")
    band: Band = Field(..., description="Mức nhận thức: NB/TH/VD/VDC")
    diem: float = Field(..., gt=0, description="Điểm của câu")
    phut: float = Field(..., gt=0, description="Phút HS làm bài (người ra đề ước)")
    hinh_thuc: str = Field("tự luận", description=f"Một trong: {', '.join(HINH_THUC)}")
    dap_an: str = Field("", description="Đáp số rút gọn để Thầy soát nhanh")


class De(BaseModel):
    """Một đề kiểm tra."""
    ma: str = Field(..., description="Mã đề, vd '15-11' hoặc '1tiet-VI'")
    ten: str = Field(..., description="Tên đề in trên đầu bài")
    tuan: int = Field(..., ge=1, description="Tuần dùng đề")
    phut: int = Field(..., gt=0, description="Thời gian làm bài (phút)")
    diem_toi_da: float = Field(10.0, gt=0, description="Thang điểm")
    pham_vi: str = Field("", description="Phạm vi kiến thức đề soi")
    cau: list[DeCau] = Field(default_factory=list)


class DeSpec(BaseModel):
    """Đặc tả TOÀN BỘ đề kiểm tra của một chương."""
    slug: str
    title: str
    grade: str = Field("lop-9", description="vd lop-9")
    subject: str = Field("dai-so", description="vd dai-so")
    tier: str = Field("C", description="Tầng lớp A/B/C/X")
    chuong: str = Field("", description="vd 'Chương VI'")
    ghi_chu: list[str] = Field(default_factory=list, description="Nguyên tắc ra đề Thầy chốt")
    de: list[De] = Field(default_factory=list)


# ── Tính toán tổng (renderer + gate dùng chung) ─────────────────────────────

def de_totals(de: De) -> dict:
    """Tổng điểm / phút của một đề, kèm phân rã theo band."""
    diem = {b: 0.0 for b in BANDS}
    phut = {b: 0.0 for b in BANDS}
    for c in de.cau:
        diem[c.band] += c.diem
        phut[c.band] += c.phut
    return {
        "diem": diem, "phut": phut,
        "tong_diem": sum(diem.values()), "tong_phut": sum(phut.values()),
    }


def band_share(de: De) -> dict[str, float]:
    """Tỉ trọng % mỗi band theo PHÚT làm bài (khớp cách soi tỉ lệ của phiếu)."""
    t = de_totals(de)
    tong = t["tong_phut"]
    if not tong:
        return {b: 0.0 for b in BANDS}
    return {b: t["phut"][b] / tong * 100 for b in BANDS}
