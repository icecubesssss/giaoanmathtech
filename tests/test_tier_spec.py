"""tier_spec.json — số câu mục tiêu phải reproduce bảng HUONG-DAN-PHAN-TANG-LOP §2."""
from src.schema.tier_spec import (
    chuong_co_vd, draw_minutes, load_tier_spec, so_ca_yeu_cau, target_counts, tier_ratio,
    rates_for,
)


def test_tier_c_reproduces_section2_table():
    """Tầng C lớp 9 đại số: Ví dụ 18/4/1 · Luyện 32/8/2 · BTVN 28/7/2 → tổng ~78/19/5."""
    spec = load_tier_spec()
    tc = target_counts(spec, "lop-9", "dai-so", "C")
    assert tc["vidu"] == {"NB": 18, "TH": 4, "VD": 1}
    assert tc["onclass"] == {"NB": 32, "TH": 8, "VD": 2}
    assert tc["btvn"] == {"NB": 28, "TH": 7, "VD": 2}
    # Tầng C KHÔNG có VDC.
    assert all("VDC" not in seg for seg in tc.values())
    totals = {b: sum(seg.get(b, 0) for seg in tc.values()) for b in ("NB", "TH", "VD")}
    assert totals == {"NB": 78, "TH": 19, "VD": 5}


# ── Tầng B: tỉ lệ chọn THEO CHƯƠNG (Thầy chốt 30/08/2026) ───────────────────

_CH4 = "chuong-04-he-thuc-luong-tam-giac-vuong"   # lớp 9: CÓ bài VD/VDC trong đề


def test_tier_b_ratio_theo_chuong_co_vd():
    """Chương có VD/VDC trong đề → 15-30-55 (VD đã gộp cả VDC)."""
    spec = load_tier_spec()
    assert chuong_co_vd("lop-9", _CH4) is True
    assert tier_ratio(spec, "lop-9", "hinh-hoc", "B", _CH4) == {
        "NB": 15, "TH": 30, "VD": 55, "VDC": 0}


_CH8 = "chuong-08-xac-suat-cua-bien-co"       # lớp 9: KHÔNG có bài VD/VDC trong đề


def test_tier_b_ratio_theo_chuong_khong_vd():
    """Chương KHÔNG có VD/VDC trong đề → 30-70 (quy ước anh An 30/08/2026: câu thực tế
    2-3 bước như tính xác suất chỉ là Thông hiểu)."""
    spec = load_tier_spec()
    assert chuong_co_vd("lop-9", _CH8) is False
    assert tier_ratio(spec, "lop-9", "dai-so", "B", _CH8) == {
        "NB": 30, "TH": 70, "VD": 0, "VDC": 0}


def test_tier_b_gop_2_phieu_khi_chuong_khong_co_vd():
    """Chương không có VD-VDC thì GỘP 2 PHIẾU THÀNH 1 (so_ca 2); chương có VD thì 1."""
    spec = load_tier_spec()
    assert so_ca_yeu_cau(spec, "lop-9", "dai-so", "B", _CH8) == 2
    assert so_ca_yeu_cau(spec, "lop-9", "hinh-hoc", "B", _CH4) == 1
    assert so_ca_yeu_cau(spec, "lop-9", "hinh-hoc", "B") is None      # chưa khai chương
    assert so_ca_yeu_cau(spec, "lop-9", "hinh-hoc", "C", _CH4) is None  # tầng khác không ràng buộc


def test_tier_b_chua_khai_chuong_thi_khong_gate():
    """Thiếu `chuong` → None: thà KHÔNG soi còn hơn soi theo tỉ lệ sai."""
    spec = load_tier_spec()
    assert tier_ratio(spec, "lop-9", "hinh-hoc", "B") is None
    assert chuong_co_vd("lop-9", "chuong-khong-co-that") is None
    assert tier_ratio(spec, "lop-9", "dai-so", "B", "chuong-khong-co-that") is None


def test_tier_b_target_counts_theo_chuong():
    """Số câu mục tiêu suy được khi đã khai chương (lớp 9 hình, onclass 55′)."""
    tc = target_counts(load_tier_spec(), "lop-9", "hinh-hoc", "B", _CH4)
    assert tc["onclass"]["VD"] > 0 and tc["onclass"]["NB"] > 0
    assert target_counts(load_tier_spec(), "lop-9", "hinh-hoc", "B") == {}


def test_tier_x_placeholder_no_targets():
    """X (chuyên) chưa chốt tỉ lệ → không sinh số câu (không gate cứng)."""
    spec = load_tier_spec()
    assert tier_ratio(spec, "lop-9", "dai-so", "X") is None
    assert target_counts(spec, "lop-9", "dai-so", "X") == {}


def test_lop8_rates_override_applied():
    """Lớp 8 đại số override phút/câu onclass NB=0,5 (khác lớp 9 = 1,5)."""
    spec = load_tier_spec()
    assert rates_for(spec, "lop-8", "dai-so")["onclass"]["NB"] == 0.5
    assert rates_for(spec, "lop-9", "dai-so")["onclass"]["NB"] == 1.5


def test_lop8_hinh_hoc_rates_are_double():
    """Thầy chốt 2026-07-26: bài HÌNH lớp 8 tốn GẤP ĐÔI thời gian mỗi câu."""
    spec = load_tier_spec()
    r = rates_for(spec, "lop-8", "hinh-hoc")
    assert r["vidu"] == {"NB": 2.0, "TH": 8.0, "VD": 16.0, "VDC": 24.0}
    assert r["onclass"] == {"NB": 2.5, "TH": 9.0, "VD": 20.0, "VDC": 30.0}
    assert r["btvn"] == {"NB": 2.0, "TH": 8.0, "VD": 17.0, "VDC": 25.0}


def test_draw_minutes_is_five():
    """Câu phải TỰ VẼ HÌNH cộng thêm 5′ (ngoài phút/câu theo band)."""
    assert draw_minutes(load_tier_spec()) == 5.0
