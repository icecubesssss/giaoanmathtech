#!/usr/bin/env python3
"""Sơ đồ thay phương trình phiếu C (Viète) ch.VI 9C — khử trùng đề (15/11/2026).

Claude chốt bảng THAY (nhãn ý → phương trình mới, loại câu hỏi), SymPy tính Δ/ac, tổng, tích, đáp số;
kiểm phương trình mới KHÔNG có ở seed khác của chương (A, B, D, E, F, TM, đề KT, de-kiem-tra/de-xuat-cot)
và không lặp nhau.  Chạy: .venv/bin/python scripts/gemini/so_do_phieu_c_9c_khu_trung.py
"""
import glob, json, re
from pathlib import Path
import sympy as sp

REPO = Path(__file__).resolve().parents[2]
D = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
x = sp.symbols("x")

# (nhãn, (a,b,c), loại, kiểu điều kiện, lí do)
THAY = [
    ("Bài 1a", (1, -7, 7), "SP", "Delta", "x^2-3x+1 = đích D; 6 lần trong C"),
    ("Bài 3a", (1, -5, -7), "SP", "ac", "x^2-3x-5 trùng D Bài 15 + đề KT ma trận"),
    ("Bài 4a", (1, -6, 7), "SQ", "Delta", "= Bài 10 = Bài 12a"),
    ("Bài 4b", (1, -6, -2), "SQ", "ac", "= Bài 12b"),
    ("Bài 5a", (2, -8, 1), "INV", "Delta", "= Bài 13a (giữ 13a có nguồn)"),
    ("Bài 6a", (1, -2, -1), "CUBE", "ac", "= Bài 14a = Bài 18"),
    ("Bài 6b", (1, -6, 6), "CUBE", "Delta", "x^2-3x+1 = đích D"),
    ("Bài 7b", (1, -8, 9), "DIFF2", "Delta", "x^2-3x+1 = đích D"),
    ("Bài 10", (1, -5, 5), "SQ", "Delta", "= Bài 4a = Bài 12a (giữ 12a có nguồn)"),
    ("Bài 11b", (1, 7, 3), "SIGN", "Delta", "= bước đầu Bài 34 (giữ 34 có nguồn)"),
    ("Bài 18", (1, -4, -4), "CUBE", "ac", "= Bài 14a (giữ 14a có nguồn)"),
    ("Bài 21a", (1, 5, -2), "SP", "ac", "= Bài 19a (giữ 19a có nguồn)"),
    ("Bài 22a", (1, -7, -3), "SQ", "ac", "= Bài 29a (giữ 29 có nguồn)"),
    ("Bài 22b", (2, -3, -1), "SQ", "ac", "= Bài 29b"),
    ("Bài 23a", (1, 6, -3), "INV", "ac", "= Bài 30a (giữ 30a có nguồn)"),
    ("Bài 23b", (3, -5, -1), "INV", "ac", "= Bài 13b (giữ 13b có nguồn)"),
    ("Bài 24a", (1, -1, -5), "CUBE", "ac", "= Bài 31a"),
    ("Bài 24b", (1, 4, 2), "CUBE", "Delta", "= Bài 31b"),
    ("Bài 30b", (1, -9, 3), "INV", "Delta", "x^2-7x+3 trùng ví dụ D + F Bài 22"),
    ("Ví dụ 4", (3, -12, 4), "INV", "Delta'", "3x^2-6x+2 trùng D Bài 12"),
    ("Ví dụ 10", (1, -8, 2), "RATIO", "Delta'", "x^2-4x+1 trùng ví dụ D + F Bài 3"),
]

# Đợt 2 (cùng phiên): hai ý "biết một nghiệm" lặp đề 15 phút số 13 (de-kiem-tra.json). (nhãn, hệ số, loại, nghiệm cho sẵn, lí do)
THAY2 = [
    ("Bài 8a", (1, -11, 24), "ROOT", 3, "x^2-7x+12 = Câu 1 đề 15 phút số 13"),
    ("Bài 26c", (3, -7, 4), "ROOT", 1, "3x^2-5x+2 = Câu 2 đề 15 phút số 13 (nhẩm a+b+c=0), phiếu B Bài 11"),
]


def tex(a, b, c):
    def hs(k, s, dau):
        if k == 0: return ""
        sg = "-" if k < 0 else ("+" if dau else "")
        k = abs(k)
        return f"{sg}{'' if (k == 1 and s) else k}{s}"
    return hs(a, "x^2", False) + hs(b, "x", True) + hs(c, "", True) + "=0"


def norm(e):
    return e.replace("\\,", "").replace(" ", "")


def eq_chuong():
    out = {}
    for f in glob.glob(str(D / "*.json")) + glob.glob(str(D / "kiem-tra-chuong/*.json")):
        if Path(f).name.startswith("phieu-c-"):
            continue  # trùng trong phiếu C soát riêng (đề + câu hỏi), ở đây chỉ so với phiếu khác
        s = Path(f).read_text()
        for m in re.findall(r"(?<![\w^{])(\d*x\^2[^$\"]*?=\s*0)", s):
            out.setdefault(norm(m.replace("\\\\", "\\")), set()).add(Path(f).name[:14])
    return out


def main():
    co = eq_chuong()
    seen = set()
    loi = []
    for lab, (a, b, c), loai, dk, ly in THAY:
        e = tex(a, b, c)
        assert e not in seen, e; seen.add(e)
        trung = co.get(norm(e))
        S, P = sp.Rational(-b, a), sp.Rational(c, a)
        Dl = b * b - 4 * a * c
        assert Dl > 0
        if dk == "ac": assert a * c < 0
        r = sp.solve(a * x**2 + b * x + c, x)
        x1, x2 = r
        val = {"SP": None, "SQ": S**2 - 2 * P, "INV": S / P, "CUBE": S**3 - 3 * P * S,
               "DIFF2": S**2 - 4 * P, "SIGN": "cùng âm" if (P > 0 and S < 0) else ("trái dấu" if P < 0 else "cùng dương"),
               "RATIO": (S**2 - 2 * P) / P}[loai]
        # kiểm chéo bằng nghiệm thật
        chk = {"SQ": x1**2 + x2**2, "INV": 1 / x1 + 1 / x2, "CUBE": x1**3 + x2**3, "DIFF2": (x1 - x2)**2,
               "RATIO": x1 / x2 + x2 / x1}.get(loai)
        if chk is not None:
            assert sp.simplify(chk - val) == 0, (lab, chk, val)
        Dp = f", Δ'={(b//2)**2 - a*c}" if b % 2 == 0 else ""
        print(f"{lab:9} ${e}$  {loai:5} Δ={Dl}{Dp} ac={a*c} tổng={S} tích={P} đáp={val}  trùng={trung or '-'}")
        if trung: loi.append(lab)
    assert not loi, f"trùng: {loi}"
    for lab, (a, b, c), loai, x1, ly in THAY2:
        e = tex(a, b, c)
        assert e not in seen, e; seen.add(e)
        assert a * x1**2 + b * x1 + c == 0, lab
        x2 = sp.Rational(-b, a) - x1
        assert sp.expand(a * (x - x1) * (x - x2) - (a * x**2 + b * x + c)) == 0
        trung = co.get(norm(e))
        print(f"{lab:9} ${e}$  {loai:5} x1={x1} tổng={sp.Rational(-b, a)} x2={x2}  trùng={trung or '-'}")
        if trung: loi.append(lab)
    assert not loi, f"trùng: {loi}"
    print("OK: không phương trình mới nào có trong chương.")


if __name__ == "__main__" and "--dot3" not in __import__("sys").argv:
    main()  # đợt 1–2 (đã áp; nay TM chứa Ví dụ 4 nên sẽ báo trùng thuyet-minh — bình thường)


# ───── Đợt 3 (15/11 tối, Thầy: "không thiếu ngân hàng câu nên cứ đổi hết") ─────
# Thay số tự đặt + ý bỏ nguồn bằng phương trình THẬT trong ngân hàng ch.VI
# (inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06.json, mã câu ở cột 6), và bỏ x^2+x-6 ở 6 ý (giữ Bài 16).
# (nhãn, (a, b, c) dạng chuỗi SymPy, loại, điều kiện, x1 cho sẵn | None, mã ngân hàng | None, nguồn in trên đề | "")
S3 = "sqrt(3)"
THAY3 = [
    ("Bài 1a", ("1", "-12", "8"), "SP", "Delta", None, "sgk-6.23", "SGK Toán 9 tập hai, Bài tập 6.23"),
    ("Bài 1c", ("1", "8", "-6"), "SP", "ac", None, "so-hn-2025-III3", "đề chính thức Vào 10 Hà Nội 2025"),
    ("Bài 3a", ("2", "11", "-5"), "SP", "ac", None, "sgk-6.23", "SGK Toán 9 tập hai, Bài tập 6.23"),
    ("Bài 4a", ("1", "-11", "30"), "SQ", "Delta", None, "sgk-6.48", "SGK Toán 9 tập hai, Bài tập 6.48"),
    ("Bài 4b", ("4", "8", "-15"), "SQ", "ac", None, "ck2-lomonoxop-2025-III3", "Cuối kì II, THCS M.V. Lômônôxốp"),
    ("Bài 4c", ("1", "-1", "-10"), "SQ", "ac", None, "tl-viete-04-tr2", ""),
    ("Bài 5a", ("1", "-9", "8"), "INV", "Delta", None, "tl-viete-02-tr1", ""),
    ("Bài 6a", ("1", "-3", "-8"), "CUBE", "ac", None, "ck2-phan-dinh-phung-2025-TL3", "Cuối kì II, THCS Phan Đình Phùng, Đà Nẵng"),
    ("Bài 6b", ("1", f"-4*{S3}", "8"), "CUBE", "Delta", None, "ck2-chu-van-an-dn-2025-2", "Cuối kì II, THCS Chu Văn An, Đà Nẵng"),
    ("Bài 6c", ("1", "4", "-3"), "CUBE", "ac", None, "ck2-nguyen-du-2025-III3", "Cuối kì II, THCS Nguyễn Du"),
    ("Bài 7b", ("2", "11", "7"), "DIFF2", "Delta", None, "sgk-b20-vd1", "SGK Toán 9 tập hai, Bài 20, Ví dụ 1"),
    ("Bài 7c", ("1", "5", "-7"), "DIFF2", "ac", None, "ck2-phuc-loi-2024-3-2", "Cuối kì II, THCS Phúc Lợi"),
    ("Bài 10", ("3", "-5", "1"), "SQ", "Delta", None, "v10-dong-da-de18-2025-III3", "bộ đề Vào 10, Phòng GD\\&ĐT Đống Đa"),
    ("Bài 11b", ("1", "7", "12"), "SIGN", "Delta", None, "sgk-6.41", "SGK Toán 9 tập hai, Bài tập 6.41"),
    ("Bài 18", ("1", "-3", "-40"), "CUBE", "ac", None, "tl-viete-07-tr3", ""),
    ("Bài 20a", ("2", "7", "5"), "COND", "Delta", None, "tl-viete-77-tr13", ""),
    ("Bài 21a", ("4", "-5", "-3"), "SP", "ac", None, "tl-viete-15-tr3", ""),
    ("Bài 22a", ("3", "4", "-6"), "SQ", "ac", None, "tl-viete-76-tr13", ""),
    ("Bài 23a", ("1", "-1", "-10"), "INV", "ac", None, "tl-viete-04-tr2", ""),
    ("Bài 23b", ("4", "15", "11"), "INV", "Delta", None, "sgk-b20-lt2", "SGK Toán 9 tập hai, Bài 20, Luyện tập 2"),
    ("Bài 24a", ("1", "-11", "30"), "CUBE", "Delta", None, "sgk-6.48", "SGK Toán 9 tập hai, Bài tập 6.48"),
    ("Bài 28a", ("1", "-3", "-2025"), "SIGN", "ac", None, "v10-tho-loc-l4-2026-III3", "thi thử Vào 10 lần 4, THCS Thọ Lộc"),
    ("Bài 8a", ("2", "-7", "5"), "ROOT", None, 1, "sgk-b20-hd3", "SGK Toán 9 tập hai, Bài 20, HĐ3"),
    ("Bài 26c", ("7", "-15", "2"), "ROOT", None, 2, "sgk-6.24", "SGK Toán 9 tập hai, Bài tập 6.24"),
]
# Giữ số tự đặt (ngân hàng hết câu cùng dạng chưa dùng trong chương): 22b, 24b, 30b, Ví dụ 4, Ví dụ 10.


def kiem_dot3():
    import json as _j
    bank = {r["ma"]: r for r in _j.loads((REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06.json").read_text())["rows"]}
    co = eq_chuong()
    loi, bang = [], []
    for lab, (sa, sb, sc), loai, dk, x1, ma, nguon in THAY3:
        a, b, c = (sp.nsimplify(sp.sympify(t)) for t in (sa, sb, sc))
        if ma:
            assert ma in bank, ma
        Dl = sp.simplify(b * b - 4 * a * c)
        S, P = sp.simplify(-b / a), sp.simplify(c / a)
        r = sp.solve(a * x**2 + b * x + c, x)
        if loai == "ROOT":
            assert sp.simplify(a * x1**2 + b * x1 + c) == 0, lab
            val = sp.simplify(S - x1)
        else:
            if dk == "ac": assert a * c < 0, lab
            if loai != "COND": assert Dl > 0, lab
            x1_, x2_ = r
            val = {"SP": (S, P), "SQ": S**2 - 2 * P, "INV": S / P, "CUBE": S**3 - 3 * P * S, "DIFF2": S**2 - 4 * P,
                   "SIGN": "trái dấu" if P < 0 else ("cùng âm" if S < 0 else "cùng dương"),
                   "COND": "dùng được" if Dl >= 0 else "không dùng được"}[loai]
            chk = {"SQ": x1_**2 + x2_**2, "INV": 1 / x1_ + 1 / x2_, "CUBE": x1_**3 + x2_**3, "DIFF2": (x1_ - x2_)**2}.get(loai)
            if chk is not None:
                assert sp.simplify(chk - val) == 0, (lab, chk, val)
        e = sp.latex(sp.expand(a * x**2 + b * x + c)).replace("x^{2}", "x^2") + "=0"
        e = norm(e).replace("\\sqrt{3}x", "\\sqrt3x")
        trung = co.get(e) or co.get(e.replace("\\sqrt3", "\\sqrt{3}"))
        if trung: loi.append((lab, trung))
        bang.append((lab, e, loai, dk, sp.latex(Dl), sp.latex(S), sp.latex(P), val if isinstance(val, str) else sp.latex(val) if not isinstance(val, tuple) else f"{sp.latex(val[0])}; {sp.latex(val[1])}", x1, ma, nguon))
        print(f"{lab:8} ${e}$ {loai:5} Δ={Dl} tổng={S} tích={P} đáp={val} x1={x1} [{ma}] trùng={trung or '-'}")
    assert not loi, loi
    print("OK đợt 3")
    return bang


if __name__ == "__main__" and "--dot3" in __import__("sys").argv:
    kiem_dot3()
