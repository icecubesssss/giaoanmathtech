"""thuyetminh_gate — soi GIỜ VÔ LÝ trong spec trước khi Thầy chốt."""
from src.schema.thuyetminh_spec import ThuyetMinhSpec, SpecPhieu, SpecRow
from src.validators.thuyetminh_gate import check_thuyetminh


def _spec(rows, grade="lop-9", subject="dai-so", tier="C"):
    return ThuyetMinhSpec(
        slug="tm-test", title="Test", grade=grade, subject=subject, tier=tier, tuan="x",
        phieu=[SpecPhieu(code="A", title="P", rows=rows)],
    )


def test_ok_spec_passes():
    # Lớp 9 C: onclass budget 120′, vidu 45′. Giữ trong quỹ + tỉ lệ ~40-40-20.
    rows = [
        SpecRow(dang="NB", band="NB", vidu=4, onclass=32),   # 32×1.5=48′
        SpecRow(dang="TH", band="TH", vidu=2, onclass=8),    # 8×6=48′
        SpecRow(dang="VD", band="VD", vidu=1, onclass=2),    # 2×12=24′
    ]
    errors, _ = check_thuyetminh(_spec(rows))
    assert errors == [], errors


def test_over_session_budget_blocks():
    # onclass quá lớn → vượt quỹ MỘT BUỔI (165′ trên lớp lớp 9).
    rows = [SpecRow(dang="NB", band="NB", onclass=200)]  # 200×1.5 = 300′
    errors, _ = check_thuyetminh(_spec(rows))
    assert any("VƯỢT quỹ" in e for e in errors)


def test_multi_phieu_not_summed():
    # 2 phiếu mỗi cái ~1 buổi (vừa quỹ) → KHÔNG cộng dồn thành 'vượt buổi'.
    full = [SpecRow(dang="NB", band="NB", onclass=24),
            SpecRow(dang="TH", band="TH", onclass=8),
            SpecRow(dang="VD", band="VD", onclass=2)]
    spec = ThuyetMinhSpec(
        slug="tm", title="t", grade="lop-9", subject="dai-so", tier="C", tuan="x",
        phieu=[SpecPhieu(code="A", title="A", rows=list(full)),
               SpecPhieu(code="B", title="B", rows=list(full))],
    )
    errors, _ = check_thuyetminh(spec)
    assert not any("VƯỢT quỹ" in e for e in errors), errors


def test_single_row_hog_blocks():
    # Một dạng nuốt quá nửa quỹ onclass (120′) — nghi gõ nhầm.
    rows = [
        SpecRow(dang="ngon-het-gio", band="TH", onclass=15),  # 15×6 = 90′ > 0.6×120
        SpecRow(dang="con-lai", band="NB", onclass=10),
    ]
    errors, _ = check_thuyetminh(_spec(rows))
    assert any("nuốt" in e or "nghi gõ nhầm" in e for e in errors)


def test_vdc_in_forbidden_tier_blocks():
    # Tầng C lớp 9: ratio VDC=0 → cấm VDC.
    rows = [SpecRow(dang="vd-cao", band="VDC", onclass=2)]
    errors, _ = check_thuyetminh(_spec(rows, tier="C"))
    assert any("VDC" in e for e in errors)


def test_vdc_allowed_in_tier_b():
    # Tầng B lớp 9 cho VDC (ratio VDC=10) → không lỗi VDC.
    rows = [SpecRow(dang="vd-cao", band="VDC", onclass=1)]
    errors, _ = check_thuyetminh(_spec(rows, tier="B"))
    assert not any("VDC" in e for e in errors)


def test_empty_phieu_blocks():
    rows = [SpecRow(dang="chi-btvn", band="NB", btvn=10)]  # 0 giờ trên lớp
    errors, _ = check_thuyetminh(_spec(rows))
    assert any("RỖNG GIỜ" in e for e in errors)


def test_unknown_grade_subject_skips():
    # (lớp, môn) chưa có rate card → không gate, không lỗi.
    errors, warns = check_thuyetminh(_spec([SpecRow(dang="x", band="NB", onclass=999)],
                                           grade="lop-3", subject="dai-so"))
    assert errors == [] and warns == []


def test_x_tier_no_ratio_skips_ratio_warn():
    # Tầng X chưa chốt tỉ lệ → không cảnh báo tỉ lệ (vẫn có thể chặn quỹ).
    rows = [SpecRow(dang="NB", band="NB", vidu=4, onclass=30)]
    _, warns = check_thuyetminh(_spec(rows, tier="X"))
    assert not any("tỉ lệ" in w for w in warns)


def test_source_ref_band_mismatch_warns():
    # row khai NB nhưng trỏ câu bank VDC (gk1-co-nhue-2-4) → cảnh báo lệch band.
    rows = [SpecRow(dang="x", band="NB", onclass=10, source_refs=["gk1-co-nhue-2-4"])]
    _, warns = check_thuyetminh(_spec(rows, tier="B"))
    assert any("source_refs" in w and "lệch" in w for w in warns)


def test_source_ref_matching_band_no_warn():
    # trỏ câu cùng/sát band (NB câu) → KHÔNG cảnh báo lệch.
    rows = [SpecRow(dang="x", band="NB", onclass=10, source_refs=["gk1-bat-trang-1a"])]
    _, warns = check_thuyetminh(_spec(rows, tier="B"))
    assert not any("source_refs" in w for w in warns)
