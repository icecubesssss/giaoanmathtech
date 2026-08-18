"""Hai luật Thầy chốt 14/08/2026 (rút từ bản mẫu chương IV lớp 7 tầng C):

  1. Mỗi phiếu phải có giàn giáo NB 'vẽ hình + đánh dấu' (môn hình) và
     'điền khuyết bài giải/chứng minh mẫu'.
  2. MỌI dòng dạng phải trỏ nguồn (`source_refs`).

Thầy làm rõ 14/08/2026: chỉ loại "NB lẻ LT" (hỏi thẳng lý thuyết) được tự soạn, còn lại
NGHIÊM CẤM BỊA. Cả hai luật là lỗi CHẶN build.
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
                loai="NB lẻ LT"),                      # miễn nguồn: hỏi thẳng lý thuyết
        SpecRow(dang="Vẽ hình từ giả thiết và đánh dấu dữ kiện", band="NB", onclass=3,
                loai="NB lẻ LT", gian_giao="ve-hinh"),
        SpecRow(dang="Điền khuyết bài giải mẫu tính góc", band="NB", onclass=3,
                loai="NB tách TH", gian_giao="dien-khuyet", source_refs=["sgk-t7-b12-3"]),
    ]


# ── Giàn giáo ────────────────────────────────────────────────────────────────

def test_du_hai_gian_giao_thi_sach():
    assert check_scaffold_rails(_spec(_day_du())) == []


def test_thieu_dien_khuyet_thi_keu():
    rows = [r for r in _day_du() if r.gian_giao != "dien-khuyet"]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "dien-khuyet" in errs[0] and "ve-hinh" not in errs[0]


def test_thieu_ca_hai_thi_keu_ca_hai():
    rows = [_day_du()[0]]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "ve-hinh" in errs[0] and "dien-khuyet" in errs[0]


def test_mon_dai_so_khong_doi_ve_hinh():
    """Phiếu đại số không có hình để vẽ ⇒ chỉ đòi 'điền khuyết'."""
    rows = [r for r in _day_du() if r.gian_giao != "ve-hinh"]
    assert check_scaffold_rails(_spec(rows, subject="dai-so")) == []


def test_gian_giao_chi_tinh_dong_band_nb():
    """Dạng 'vẽ hình' nằm ở band TH không thay được giàn giáo NB."""
    rows = [
        SpecRow(dang="Tính góc", band="NB", onclass=3, loai="NB lẻ LT"),
        SpecRow(dang="Vẽ hình rồi chứng minh", band="TH", onclass=2, gian_giao="ve-hinh"),
        SpecRow(dang="Điền khuyết bài giải mẫu", band="NB", onclass=3,
                gian_giao="dien-khuyet"),
    ]
    errs = check_scaffold_rails(_spec(rows))
    assert len(errs) == 1 and "ve-hinh" in errs[0]


# ── Nguồn câu ────────────────────────────────────────────────────────────────

def test_moi_dong_co_nguon_thi_sach():
    assert check_source_refs(_spec(_day_du())) == []


def test_thieu_nguon_thi_keu_dung_so_dong():
    """Dòng KHÔNG phải 'NB lẻ LT' mà trống nguồn ⇒ tính là BỊA ĐỀ."""
    rows = _day_du()
    rows[2] = rows[2].model_copy(update={"source_refs": []})
    errs = check_source_refs(_spec(rows))
    assert len(errs) == 1 and "1/3 dòng" in errs[0] and "BỊA ĐỀ" in errs[0]


def test_nb_le_lt_duoc_mien_trich_dan():
    """'NB lẻ LT' hỏi thẳng lý thuyết vừa học ⇒ tự soạn được, không cần nguồn."""
    rows = [SpecRow(dang="Phát biểu định lý", band="NB", onclass=3, loai="NB lẻ LT")]
    assert check_source_refs(_spec(rows)) == []


def test_nb_tach_th_khong_duoc_mien():
    """'NB tách TH' là bước đệm cắt ra từ bài TH ⇒ phải trỏ chính bài gốc đó."""
    rows = [SpecRow(dang="Bước đệm", band="NB", onclass=3, loai="NB tách TH")]
    assert len(check_source_refs(_spec(rows))) == 1


# ── Cổng nội dung phải chạy kể cả khi CHƯA có chuẩn giờ ──────────────────────

def test_chua_co_tang_trong_tier_spec_van_soi_noi_dung():
    """Đây chính là lỗ hổng làm bản mẫu chương IV lớp 7 tầng C không bị soi:
    tier_spec thiếu tầng ⇒ trước đây trả [], [] và im hoàn toàn."""
    spec = _spec([SpecRow(dang="Tính góc", band="NB", onclass=3)], tier="Z")
    errors, warns = check_thuyetminh(spec)
    assert any("CHƯA có chuẩn giờ" in w for w in warns)   # cổng giờ bị bỏ qua
    assert any("giàn giáo" in e for e in errors)          # nhưng nội dung vẫn chặn
    assert any("BỊA ĐỀ" in e for e in errors)
    assert any("CHƯA khai" in e for e in errors)


def test_lop_7_hinh_tang_C_da_co_chuan_gio():
    """Sau khi thêm tầng C vào tier_spec, spec lớp 7 hình tầng C phải được soi giờ."""
    _, warns = check_thuyetminh(_spec(_day_du()))
    assert not any("CHƯA có chuẩn giờ" in w for w in warns)


def test_spec_khong_phai_cap_chuong_thi_chan():
    """Thầy chốt: TỪ GIỜ CHỈ LÀM THUYẾT MINH CẤP CHƯƠNG, mọi khối."""
    from src.validators.thuyetminh_gate import check_chuong_level
    spec = _spec(_day_du())
    assert len(check_chuong_level(spec)) == 1          # slug 'tm-test' → không phải chương
    assert check_chuong_level(spec.model_copy(update={"slug": "tm-chuong-04"})) == []
