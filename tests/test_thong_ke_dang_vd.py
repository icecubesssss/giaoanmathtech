"""scripts/thong_ke_dang_vd.py — bước 2a: tần suất dạng ý trong đề thật (Thầy 04/11/2026)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "tkdvd", Path(__file__).resolve().parent.parent / "scripts" / "thong_ke_dang_vd.py")
tk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tk)

LUAT = [{"ma": "tiep_tuyen", "ten": "Tiếp tuyến", "re": r"là (một )?tiếp tuyến"},
        {"ma": "vuong_goc", "ten": "Vuông góc", "re": r"⊥|vuông góc"}]


def test_tach_y_lay_muc_tung_y():
    de = "Cho …\na) Chứng minh A.\nb) Chứng minh B.\nc) Chứng minh C."
    ys = tk.tach_y(de, "a) TH · b) VD · c) VDC")
    assert [(n, m) for n, m, _ in ys] == [("a", "TH"), ("b", "VD"), ("c", "VDC")]


def test_chi_doc_phan_cau_hoi_khong_doc_cau_dung_hinh():
    y = "Qua O kẻ đường thẳng vuông góc với BC tại H, cắt MC tại K. Chứng minh KB là tiếp tuyến của (O)."
    assert tk.gan_dang(y, LUAT) == ["tiep_tuyen"]


def test_gop_de_tru_y_cuoi_va_hu_tu():
    a = {"ma": "x", "de": "Cho (O; R) đường kính AB. Lấy C ∈ (O; R).\na) Chứng minh P.\nb) Chứng minh Q.\nc) Chứng minh R."}
    b = {"ma": "y", "de": "Cho đường tròn (O; R), đường kính AB. Lấy điểm C thuộc (O; R).\na) Chứng minh P.\nb) Chứng minh Q.\nc) Tính S."}
    assert tk.gop_trung([a, b])["y"] == "x"


def test_thong_ke_chuong_5_tiep_tuyen_it_hon_bon_diem():
    kq = tk.thong_ke("lop-9", "hinh-hoc", 5)
    ky1 = {b["dang"]: b["pct"] for b in kq["bang"] if b["nhom"].startswith("Kì I")}
    assert ky1["bon_diem"] > ky1["he_thuc_tich"] > ky1["tiep_tuyen"]
    assert kq["trung"].get("ck1-hat-mon-2025-IV2") == "ck1-ai-mo-2"
