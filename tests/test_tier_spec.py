"""tier_spec.json — số câu mục tiêu phải reproduce bảng HUONG-DAN-PHAN-TANG-LOP §2."""
from src.schema.tier_spec import (
    draw_minutes, load_tier_spec, target_counts, tier_ratio, rates_for,
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


def test_tier_b_has_vdc_band():
    """Tầng B 30-40-20-10 → có câu VDC ở luyện tập."""
    spec = load_tier_spec()
    tc = target_counts(spec, "lop-9", "dai-so", "B")
    assert tc["onclass"].get("VDC", 0) > 0


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
