"""ThuyetMinhSpec — số câu/thời gian tự tính + render ra LaTeX."""
from src.schema.thuyetminh_spec import (
    ThuyetMinhSpec, SpecPhieu, SpecRow, phieu_totals, phieu_band_counts, rates_for_spec,
    row_minutes,
)
from src.schema.tier_spec import load_tier_spec, rates_for
from src.compiler.thuyetminh_renderer import render_thuyetminh


def _spec():
    return ThuyetMinhSpec(
        slug="tm-test", title="BPT test", grade="lop-9", subject="dai-so", tier="C", tuan="10-11",
        lythuyet=["Khái niệm $ax+b>0$."],
        phieu=[SpecPhieu(code="A", title="Giải BPT", rows=[
            SpecRow(dang="Nhận biết (Bài 1)", band="NB", lythuyet=1, vidu=1, onclass=10, btvn=12),
            SpecRow(dang="Giải BPT có mẫu", band="TH", lythuyet=1, vidu=1, onclass=2),
            SpecRow(dang="Tìm số nguyên", band="VD", onclass=2, btvn=2, decompose="vd"),
        ])],
    )


def test_band_counts_and_minutes():
    spec = _spec()
    rates = rates_for_spec(spec)
    counts = phieu_band_counts(spec.phieu[0])
    assert counts["onclass"] == {"NB": 10, "TH": 2, "VD": 2, "VDC": 0}
    tot = phieu_totals(spec.phieu[0], rates)
    # onclass: NB 10×1,5 + TH 2×6 + VD 2×12 = 15+12+24 = 51′
    assert tot["counts"]["onclass"] == 14
    assert round(tot["minutes"]["onclass"]) == 51


def test_ve_hinh_adds_draw_minutes_per_segment():
    """Dòng dạng khai `ve_hinh` → cộng 5′/hình vào đúng đoạn (bài HÌNH lớp 8)."""
    row = SpecRow(dang="Chứng minh hình thang cân", band="TH", onclass=2, btvn=2,
                  ve_hinh={"onclass": 2, "btvn": 1})
    rates = rates_for(load_tier_spec(), "lop-8", "hinh-hoc")
    m = row_minutes(row, rates)
    assert m["onclass"] == 2 * 9.0 + 2 * 5.0     # 18′ làm bài + 10′ vẽ 2 hình
    assert m["btvn"] == 2 * 8.0 + 1 * 5.0        # 16′ làm bài + 5′ vẽ 1 hình
    assert m["vidu"] == 0.0                      # đoạn không khai ve_hinh → không cộng


def test_render_produces_latex():
    tex = render_thuyetminh(_spec())
    assert r"\tmtitle{PHIẾU THUYẾT MINH}" in tex
    assert "NHẬN BIẾT" in tex and "TỔNG" in tex
    assert r"\documentclass" in tex  # qua base_thuyetminh.tex.j2


def test_hinh_san_tinh_nua_phut_moi_cau():
    """Dạng trắc nghiệm/điền khuyết trên HÌNH VẼ SẴN chỉ tốn nửa phút/câu
    (Thầy chốt 2026-07-27: vẽ sẵn hình để trừ khâu dựng hình + trình bày)."""
    rates = rates_for(load_tier_spec(), "lop-8", "hinh-hoc")   # hình lớp 8: rate ×2 (NB 2,5′)
    thuong = SpecRow(dang="Nhận diện cạnh đối", band="NB", onclass=4)
    ve_san = SpecRow(dang="Trắc nghiệm trên hình vẽ sẵn", band="NB", onclass=4, hinh_san=True)
    assert row_minutes(thuong, rates)["onclass"] == 4 * rates["onclass"]["NB"]
    # NB trên hình vẽ sẵn: 1′/câu (quick_minutes), KHÔNG theo rate của band.
    assert row_minutes(ve_san, rates)["onclass"] == 4 * 1.0
    # TH điền khuyết vẫn phải tính toán ⇒ chỉ giảm nửa rate.
    th_san = SpecRow(dang="Điền khuyết giải tam giác vuông", band="TH", onclass=2, hinh_san=True)
    assert row_minutes(th_san, rates)["onclass"] == 2 * rates["onclass"]["TH"] * 0.5


def test_hinh_san_khong_dung_cham_phut_ve_hinh():
    """`ve_hinh` (+5′/hình) vẫn cộng nguyên, không bị ×0,5 theo `hinh_san`."""
    rates = rates_for(load_tier_spec(), "lop-8", "hinh-hoc")
    row = SpecRow(dang="Vừa vẽ sẵn vừa có hình tự vẽ", band="NB", onclass=2,
                  hinh_san=True, ve_hinh={"onclass": 1})
    assert row_minutes(row, rates)["onclass"] == 2 * 1.0 + 5.0
