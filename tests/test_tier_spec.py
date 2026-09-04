"""tier_spec.json — số câu mục tiêu phải reproduce bảng HUONG-DAN-PHAN-TANG-LOP §2."""
from src.schema.tier_spec import (
    phan_bo_vdc, muc_tieu_vdc,
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
    """Chương có VD/VDC trong đề → NB 15 · TH 30 · (VD+VDC) 55.

    Từ 04/09/2026 khối 55% được CHIA theo tần suất VDC của chương: chương IV có VDC ở
    ý cuối bài hình trong 9/9 đề GK1 (p = 1,00, nhóm 'cao') nên VD 35 · VDC 20 —
    tổng vẫn 55."""
    spec = load_tier_spec()
    assert chuong_co_vd("lop-9", _CH4) is True
    r = tier_ratio(spec, "lop-9", "hinh-hoc", "B", _CH4)
    assert r == {"NB": 15, "TH": 30, "VD": 35, "VDC": 20}
    assert r["VD"] + r["VDC"] == 55


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


# ── Ưu tiên VDC theo TẦN SUẤT (Thầy chốt 04/09/2026) ─────────────────────────

_CH2 = "chuong-02-bat-dang-thuc-bat-phuong-trinh"   # cực trị = câu cuối 15/21 đề
_CH3 = "chuong-03-can-bac-hai-can-bac-ba"          # chỉ 1/21 đề → nhóm "thấp"
_CH1 = "chuong-01-phuong-trinh-va-he-hai-phuong-trinh-bac-nhat-hai-an"
_CH9 = "chuong-09-duong-tron-ngoai-tiep-va-noi-tiep"


def test_phan_bo_55_theo_tan_suat():
    """Chương VDC hay ra được nhiều phút VDC hơn; chương hiếm thì gần như chỉ VD."""
    assert phan_bo_vdc("lop-9", _CH2) == {"VD": 35, "VDC": 20}   # p = 0,71 → cao
    assert phan_bo_vdc("lop-9", _CH3) == {"VD": 50, "VDC": 5}    # p = 0,05 → thấp
    # Chương I có bài VD (lập hệ PT) nhưng KHÔNG có VDC: hai câu "tăng/giảm giá" từng
    # bị gán cho nó nay về chương II vì giải bằng hằng đẳng thức (Thầy chốt 04/09/2026).
    assert phan_bo_vdc("lop-9", _CH1) == {"VD": 55, "VDC": 0}
    for ch in (_CH1, _CH2, _CH3, _CH9):
        pb = phan_bo_vdc("lop-9", ch)
        assert pb["VD"] + pb["VDC"] == 55, "tổng khối VD+VDC luôn là 55%"


def test_tier_ratio_nhan_phan_bo_cua_chuong():
    spec = load_tier_spec()
    assert tier_ratio(spec, "lop-9", "dai-so", "B", _CH3) == {
        "NB": 15, "TH": 30, "VD": 50, "VDC": 5}


def test_muc_tieu_vdc_va_tran_diem():
    """Kỳ I dạy để ăn trọn 10,0; kỳ II nhường 0,5đ ở ý cuối bài hình → trần 9,5."""
    assert muc_tieu_vdc("lop-9", _CH2) == ("an-tron", 10.0)
    assert muc_tieu_vdc("lop-9", _CH9) == ("cham-diem-tung-phan", 9.5)


def test_chuong_khoi_khac_chua_do_thi_giu_ti_le_mac_dinh():
    """Khối 6/7/8 chưa đo tần suất ⇒ phan_bo_vdc = None, tỉ lệ giữ nguyên 15-30-55."""
    spec = load_tier_spec()
    ch = "chuong-02-hang-dang-thuc-dang-nho-va-ung-dung"
    assert phan_bo_vdc("lop-8", ch) is None
    r = tier_ratio(spec, "lop-8", "dai-so", "B", ch)
    if r:                      # lớp 8 đã khai rate card thì phải rơi về biến thể gốc
        assert (r["VD"], r["VDC"]) == (55, 0)
