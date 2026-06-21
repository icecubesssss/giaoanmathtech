"""ThuyetMinhSpec — số câu/thời gian tự tính + render ra LaTeX."""
from src.schema.thuyetminh_spec import (
    ThuyetMinhSpec, SpecPhieu, SpecRow, phieu_totals, phieu_band_counts, rates_for_spec,
)
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


def test_render_produces_latex():
    tex = render_thuyetminh(_spec())
    assert r"\tmtitle{PHIẾU THUYẾT MINH}" in tex
    assert "NHẬN BIẾT" in tex and "TỔNG" in tex
    assert r"\documentclass" in tex  # qua base_thuyetminh.tex.j2
