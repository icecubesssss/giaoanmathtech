"""Tỉ lệ nguồn lớp C THCS (Thầy chốt 03/11/2026, mục 5 sheet quy chuẩn): đề thi ≥50% · SGK ≥20% · STK ≤30%."""
from src.schema import ngan_hang_sheet as nhs
from src.schema.thuyetminh_spec import ThuyetMinhSpec, SpecPhieu, SpecRow
from src.validators.thuyetminh_gate import check_ti_le_nguon

UU = {1: "Ưu tiên 1: Đề thi chính thức", 2: "Ưu tiên 2: SGK", 3: "Ưu tiên 3: nguồn khác"}


def _snap(nguon):
    return {"tab": "t", "rows": [{"ma": ma, "uu": UU[u], "de": ma, "band": "TH"} for ma, u in nguon]}


def _spec(refs, tier="C", grade="lop-9"):
    rows = [SpecRow(dang=f"d{i}", band="TH", onclass=1, source_refs=[r]) for i, r in enumerate(refs)]
    return ThuyetMinhSpec(slug="tm-9c-chuong-09-test", title="Chương IX", grade=grade, subject="hinh-hoc",
                          tier=tier, tuan="x", phieu=[SpecPhieu(code="A", title="P", rows=rows)])


def test_lech_ti_le_canh_bao(monkeypatch):
    nguon = [("d1", 1), ("s1", 2), ("t1", 3), ("t2", 3), ("t3", 3), ("t4", 3)]
    monkeypatch.setattr(nhs, "load", lambda *a, **k: _snap(nguon))
    out = check_ti_le_nguon(_spec([m for m, _ in nguon]))
    assert out and "đề thi 17% < 50%" in out[0] and "sách tham khảo 67% > 30%" in out[0]


def test_dat_chuan_im(monkeypatch):
    nguon = [("d1", 1), ("d2", 1), ("d3", 1), ("s1", 2), ("s2", 2), ("t1", 3)]
    monkeypatch.setattr(nhs, "load", lambda *a, **k: _snap(nguon))
    assert check_ti_le_nguon(_spec([m for m, _ in nguon])) == []


def test_tinh_theo_bai_goc_y_con_khong_dem_hai_lan(monkeypatch):
    nguon = [("d1", 1), ("d2", 1), ("d3", 1), ("s1", 2), ("s2", 2), ("t1", 3)]
    monkeypatch.setattr(nhs, "load", lambda *a, **k: _snap(nguon))
    # t1.a và t1.b là hai ý của CÙNG một bài gốc ⇒ vẫn chỉ 1/6 sách tham khảo.
    refs = ["d1", "d2", "d3", "s1", "s2", "t1.a", "t1.b"]
    assert check_ti_le_nguon(_spec(refs)) == []


def test_chi_ap_lop_c_thcs(monkeypatch):
    nguon = [(f"t{i}", 3) for i in range(6)]
    monkeypatch.setattr(nhs, "load", lambda *a, **k: _snap(nguon))
    refs = [m for m, _ in nguon]
    assert check_ti_le_nguon(_spec(refs, tier="B")) == []
    assert check_ti_le_nguon(_spec(refs, grade="lop-5")) == []
    assert check_ti_le_nguon(_spec(refs))  # lớp C lớp 9 thì có cảnh báo
