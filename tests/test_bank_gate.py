"""Cổng chất lượng tab phân dạng (bank_gate) — Thầy chốt 03/11/2026, mục 8 sheet quy chuẩn."""
from src.validators.bank_gate import check_bank


def _row(ma, de, band="TH", phut=6.0, vai=""):
    return {"ma": ma, "de": de, "band": band, "phut": phut, "vai": vai}


def test_bat_loi_giai_lan_trong_de():
    snap = {"tab": "t", "rows": [_row("a1", "Ví dụ 1. Cho tam giác ABC. Giải Xét tam giác ABC vuông tại B")]}
    loi, _ = check_bank(snap)
    assert any("LỜI GIẢI" in x and "a1" in x for x in loi)


def test_khong_bat_giai_la_yeu_cau_cua_de():
    rows = [_row("b1", "a) Giải tam giác vuông OAD."), _row("b2", "Giải thích vì sao G là tâm."),
            _row("b3", "Giải phương trình x^2 - 4 = 0."), _row("b4", "Giải bài toán bằng cách lập hệ.")]
    loi, _ = check_bank({"tab": "t", "rows": rows})
    assert loi == []


def test_bat_chu_pdftotext():
    loi, _ = check_bank({"tab": "t", "rows": [_row("c1", "Xét ∆𝐴𝐵𝐶 vuông tại B")]})
    assert any("pdftotext" in x for x in loi)


def test_ma_trung_la_loi():
    loi, _ = check_bank({"tab": "t", "rows": [_row("d1", "Đề một"), _row("d1", "Đề hai")]})
    assert any("mã câu trùng" in x for x in loi)


def test_de_trung_nguyen_van_chi_canh_bao():
    loi, cb = check_bank({"tab": "t", "rows": [_row("e1", "Cho  đường tròn (O)."), _row("e2", "Cho đường tròn (O).")]})
    assert loi == [] and any("trùng nguyên văn" in x and "e1 = e2" in x for x in cb)


def test_muc_va_phut_mac_dinh_canh_bao():
    rows = [_row(f"f{i}", f"Đề số {i}", band="TH", phut=6.0, vai="") for i in range(60)]
    _, cb = check_bank({"tab": "t", "rows": rows})
    assert any("cùng mức TH" in x for x in cb)
    assert any("cùng thời lượng" in x for x in cb)
    assert any("Phân loại câu" in x for x in cb)


def test_tab_nho_khong_soi_phan_bo():
    rows = [_row(f"g{i}", f"Đề số {i}") for i in range(10)]
    assert check_bank({"tab": "t", "rows": rows}) == ([], [])
