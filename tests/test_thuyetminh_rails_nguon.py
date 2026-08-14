"""Hai luật Thầy chốt 14/08/2026 (rút từ bản mẫu chương IV lớp 7 tầng C):

  1. Mỗi phiếu phải có giàn giáo NB 'vẽ hình + đánh dấu' (môn hình) và
     'điền khuyết bài giải/chứng minh mẫu'.
  2. MỌI dòng dạng phải trỏ nguồn (`source_refs`).

Cả hai đang ở mức CẢNH BÁO (repo mới có 10% dòng gắn nguồn, 0 spec có 'điền khuyết').
Test cũng khoá lại việc cổng NỘI DUNG phải chạy KỂ CẢ khi tier_spec chưa có tầng đó.
"""
from __future__ import annotations

from src.schema.thuyetminh_spec import SpecPhieu, SpecRow, ThuyetMinhSpec
from src.validators.thuyetminh_gate import (
    check_scaffold_rails, check_source_refs, check_thuyetminh,
)


def _spec(rows: list[SpecRow], subject: str = "hinh-hoc", tier: str = "C") -> ThuyetMinhSpec:
    return ThuyetMinhSpec(
        slug="tm-test", title="Test", grade="lop-7", subject=subject, tier=tier,
        phieu=[SpecPhieu(code="A", title="Phiếu A", rows=rows)],
    )


def _day_du() -> list[SpecRow]:
    """Bộ dòng ĐẠT chuẩn: có cả hai giàn giáo, mọi dòng đều trỏ nguồn."""
    return [
        SpecRow(dang="Tính góc còn lại khi biết hai góc", band="NB", onclass=3,
                source_refs=["sgk-t7-b12-1"]),
        SpecRow(dang="Vẽ hình từ giả thiết và đánh dấu dữ kiện vào hình", band="NB",
                onclass=3, source_refs=["sgk-t7-b12-2"]),
        SpecRow(dang="Điền khuyết bài giải mẫu tính góc", band="NB", onclass=3,
                source_refs=["sgk-t7-b12-3"]),
    ]


# ── Giàn giáo ────────────────────────────────────────────────────────────────

def test_du_hai_gian_giao_thi_sach():
    assert check_scaffold_rails(_spec(_day_du())) == []


def test_thieu_dien_khuyet_thi_keu():
    rows = [r for r in _day_du() if "Điền khuyết" not in r.dang]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "điền khuyết" in errs[0] and "vẽ hình" not in errs[0]


def test_thieu_ca_hai_thi_keu_ca_hai():
    rows = [_day_du()[0]]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "vẽ hình" in errs[0] and "điền khuyết" in errs[0]


def test_mon_dai_so_khong_doi_ve_hinh():
    """Phiếu đại số không có hình để vẽ ⇒ chỉ đòi 'điền khuyết'."""
    rows = [r for r in _day_du() if "Vẽ hình" not in r.dang]
    assert check_scaffold_rails(_spec(rows, subject="dai-so")) == []


def test_gian_giao_chi_tinh_dong_band_nb():
    """Dạng 'vẽ hình' nằm ở band TH không thay được giàn giáo NB."""
    rows = [
        SpecRow(dang="Tính góc", band="NB", onclass=3),
        SpecRow(dang="Vẽ hình từ giả thiết rồi chứng minh", band="TH", onclass=2),
        SpecRow(dang="Điền khuyết bài giải mẫu", band="NB", onclass=3),
    ]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "vẽ hình" in errs[0]


# ── Nguồn câu ────────────────────────────────────────────────────────────────

def test_moi_dong_co_nguon_thi_sach():
    assert check_source_refs(_spec(_day_du())) == []


def test_thieu_nguon_thi_keu_dung_so_dong():
    rows = _day_du()
    rows[1] = rows[1].model_copy(update={"source_refs": []})
    errs = check_source_refs(_spec(rows))
    assert len(errs) == 1 and "1/3 dòng" in errs[0]


# ── Cổng nội dung phải chạy kể cả khi CHƯA có chuẩn giờ ──────────────────────

def test_chua_co_tang_trong_tier_spec_van_soi_noi_dung():
    """Đây chính là lỗ hổng làm bản mẫu chương IV lớp 7 tầng C không bị soi:
    tier_spec thiếu tầng ⇒ trước đây trả [], [] và im hoàn toàn."""
    spec = _spec([SpecRow(dang="Tính góc", band="NB", onclass=3)], tier="Z")
    errors, warns = check_thuyetminh(spec)
    assert errors == []
    assert any("CHƯA có chuẩn giờ" in w for w in warns)
    assert any("giàn giáo" in w for w in warns)
    assert any("source_refs" in w for w in warns)


def test_lop_7_hinh_tang_C_da_co_chuan_gio():
    """Sau khi thêm tầng C vào tier_spec, spec lớp 7 hình tầng C phải được soi giờ."""
    _, warns = check_thuyetminh(_spec(_day_du()))
    assert not any("CHƯA có chuẩn giờ" in w for w in warns)
