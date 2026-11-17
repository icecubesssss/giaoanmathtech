#!/usr/bin/env python3
"""Sơ đồ thay phương trình phiếu F (luyện tập chung) ch.VI 9C — khử trùng đề (15/11/2026).

Soát 15/11: ví dụ F lặp phiếu C/D (VD1 = D Bài 4c, VD2 = C VD5, VD4 = C VD1, VD7 = C Bài 7a) và
nhiều ý không nguồn trùng phương trình phiếu A–D / đề 15 phút. Ý có trích nguồn đề thật GIỮ.
Claude chốt bảng (nhãn ý → phương trình mới), SymPy tính mọi con số; kiểm phương trình mới KHÔNG có ở
bất kì seed nào của chương (A–E, TM, đề KT, de-kiem-tra, de-xuat-cot, và phần GIỮ của chính F), không lặp nhau.

    .venv/bin/python scripts/gemini/so_do_phieu_f_9c_khu_trung.py
"""
import glob
import json
import re
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[2]
D = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
SEED_F = D / "phieu-f-luyen-tap-chung-va-bai-tap-cuoi-chuong-vi.json"
x = sp.symbols("x")

# Viète: (nhãn, (a,b,c), loại, điều kiện, phương trình CŨ, lí do)
#   SQ x1²+x2² · INV 1/x1+1/x2 · CUBE x1³+x2³ · MIX x1²x2+x1x2² · SQINV = SQ + INV · SQCUBE = SQ + CUBE
#   HB hạ bậc (x1², x1³) · ASYM A = x1² + (-b)·x2 · K x1³ - k·x1 + hằng · DELTA dùng Δ hay Δ' · NHAM a+b+c=0
VIETE = [
    ("Ví dụ 1", (1, -8, 4), "SQ", "Delta'", "x^2-6x+2", "= D Bài 4c"),
    ("Ví dụ 2", (1, -1, -7), "HB", "-", "x^2-2x-4", "= C Ví dụ 5"),
    ("Ví dụ 4", (1, -6, -4), "MIX", "ac", "x^2-5x-3", "= C Ví dụ 1"),
    ("Ví dụ 7", (1, -5, -8), "ASYM", "ac", "x^2-3x-1", "= C Bài 7a, 19a, 29a, 31; Bài 25 F giữ (Ứng Hòa)"),
    ("Bài 1a", (3, 8, -3), "DELTA", "-", "x^2-10x+9", "= B Bài 11a; mới = SGK tập hai Bài 19 Luyện tập 6a"),
    ("Bài 2a", (3, -1, -2), "NHAM", "-", "x^2-3x+2", "= A Bài 4a"),
    ("Bài 3", (1, -10, 5), "SQINV", "Delta'", "x^2-4x+1", "= D Ví dụ 9"),
    ("Bài 4", (1, -3, -7), "HB", "-", "x^2-5x+3", "= D Bài 1a"),
    ("Bài 9a", (1, 6, 4), "SQ", "Delta'", "x^2-8x+3", "= D Bài 16b"),
    ("Bài 12", (1, -4, -8), "K", "ac", "x^2-4x-1", "= D Bài 5b"),
    ("Bài 15a", (3, -11, 8), "NHAM", "-", "x^2-7x+6", "= A Bài 18a, C Bài 28b; mới = SGK tập hai Bài 20 Luyện tập 2a"),
    ("Bài 16", (1, -7, 8), "SQCUBE", "Delta", "x^2-5x+2", "= C Ví dụ 3, đề 15 phút"),
    ("Bài 17", (1, -5, -5), "HB", "-", "x^2-3x-2", "= D Bài 3c"),
    ("Bài 22a", (1, 5, 5), "CUBE", "Delta", "x^2-7x+3", "= D Ví dụ 1; đề Chu Văn An (x^2-4√3x+8) đã vào phiếu C"),
    ("Bài 22b", (3, -1, -5), "SQ", "ac", "2x^2-x-5 (Ba Đình)", "= A Bài 7b, C Bài 13b/21b/29b/33"),
    ("Bài 25", (1, 3, -3), "K", "ac", "x^2-3x-1 (Ứng Hòa)", "= C Bài 7a/19a/29a/31, A Bài 4c"),
]
K_HB = {"Bài 12": (24, 2025), "Bài 25": (12, 2026)}  # K = x1^3 - k x1 + hằng

# Biết một nghiệm có căn: (nhãn, b, nghiệm cho sẵn, phương trình CŨ, lí do)
CAN = [
    ("Bài 11", -10, 5 - sp.sqrt(3), "x^2-8x+c, x1=4-sqrt5", "= họ C Bài 32b (x^2-8x+c)"),
    ("Bài 24b", 2, -1 + sp.sqrt(3), "x^2-2x+c, x1=1+sqrt3", "= C Bài 32a (x^2-2x+c)"),
]

# Phương trình chứa ẩn ở mẫu: (nhãn, vế trái, vế phải, mẫu chung, ĐKXĐ, PT bậc hai sau khử mẫu, cũ, lí do)
MAU = [
    ("Ví dụ 3", x / (x - 5) + 2 / (x + 5), 50 / (x**2 - 25), (x - 5) * (x + 5), {5, -5}, x**2 + 7 * x - 60,
     "x/(x-2)+2/(x+2)=8/(x^2-4) -> x^2+4x-12", "chỉ khác B Bài 10a đúng một số (3 -> 2)"),
    ("Bài 8", (x + 2) / (x - 1) - 1 / (x + 1), 6 / (x**2 - 1), (x - 1) * (x + 1), {1, -1}, x**2 + 2 * x - 3,
     "(x+1)/(x-1)-1/(x+1)=4/(x^2-1) -> x^2+x-2", "x^2+x-2 = B Bài 4a (cùng mẫu x^2-1)"),
    ("Bài 21b", x / (x - 3) + 2 / (x + 3), 18 / (x**2 - 9), (x - 3) * (x + 3), {3, -3}, x**2 + 5 * x - 24,
     "x/(x+2)+3/(x-2)=12/(x^2-4) -> x^2+x-6", "x^2+x-6 = C Bài 1c/4c/6c/7c/16/20a/28a, A Bài 4b"),
]

# Bài lời văn lấy đề thật: (nhãn, PT gốc (=0), PT bậc hai, nghiệm, nghiệm nhận)
LOI_VAN = [
    ("Bài 10a", 2 * x * (46 - x) - x * (41 - x) - 560, x**2 - 51 * x + 560, [16, 35], 16),   # Bế Văn Đàn (Đống Đa)
    ("Bài 13", sp.Rational(1100) / x - sp.Rational(1100) / (x + 5) - 2, x**2 + 5 * x - 2750, [-55, 50], 50),  # Lê Ngọc Hân GK2
    ("Bài 26", 144 / (x + 7) + 144 / (x - 7) - 6, x**2 - 48 * x - 49, [-1, 49], 49),  # Tô Vĩnh Diện (Đống Đa); Mỹ Đình 2 xe đạp ra x^2-3x-180 = E Bài 18 ⇒ chuyển sang NB Bài 6a
    ("Bài 7a", 144 / (x - 3) - 144 / x - 4, x**2 - 3 * x - 108, [-9, 12], 12),            # Phương Mai (Đống Đa)
    ("Bài 7b", 88 / x - 90 / (x + 3) - sp.Rational(2, 5), x**2 + 8 * x - 660, [-30, 22], 22),  # Nguyễn Trường Tộ GK1
    ("Bài 20a", 8400 / x - 6416 / (x + 102) - 4, x**2 - 394 * x - 214200, [-306, 700], 700),  # Mỹ Đình 2 thi thử 2026
]

# Nhãn F bị thay (phần còn lại của F tính vào tập "đã dùng")
DOI = {"Ví dụ 1", "Ví dụ 3", "Ví dụ 2", "Ví dụ 4", "Ví dụ 7", "Bài 1", "Bài 2", "Bài 3", "Bài 4", "Bài 8", "Bài 9", "Bài 11",
       "Bài 12", "Bài 15", "Bài 16", "Bài 17", "Bài 21", "Bài 22", "Bài 24",
       "Bài 6", "Bài 7", "Bài 10", "Bài 13", "Bài 19", "Bài 20", "Bài 25", "Bài 26"}


def tex(a, b, c):
    def hs(k, s, dau):
        if k == 0:
            return ""
        sg = "-" if k < 0 else ("+" if dau else "")
        k = abs(k)
        return f"{sg}{'' if (k == 1 and s) else k}{s}"
    return hs(a, "x^2", False) + hs(b, "x", True) + hs(c, "", True)


EQ = re.compile(r"(?<![\w^{}])(\d*x\^2(?:\s*[+-]\s*\d*[a-z]?x?)+)\s*=\s*0")


def _walk(o, lab, out, bo):
    if isinstance(o, dict):
        t = o.get("text") if isinstance(o.get("text"), str) else ""
        m = re.match(r"\\textbf\{(Ví dụ \d+)\.", t)
        lab = o.get("label", "").rstrip(".") if o.get("label") else (m.group(1) if m else lab)
        for v in o.values():
            _walk(v, lab, out, bo)
    elif isinstance(o, list):
        for v in o:
            _walk(v, lab, out, bo)
    elif isinstance(o, str):
        if bo and lab in DOI:
            return
        for mm in re.findall(r"\$([^$]*)\$", o):
            for e in EQ.findall(mm):
                out.setdefault(re.sub(r"\s|\\,", "", e), set()).add(lab or "?")


def da_dung():
    """{phương trình chuẩn hoá (vế trái): {file:nhãn}} cho cả chương, trừ các ý F sắp thay."""
    out = {}
    for f in sorted(glob.glob(str(D / "*.json")) + glob.glob(str(D / "kiem-tra-chuong/*.json"))):
        o = {}
        _walk(json.loads(Path(f).read_text()), None, o, bo=(Path(f) == SEED_F))
        for e, labs in o.items():
            out.setdefault(e, set()).update(f"{Path(f).name[:9]}:{l}" for l in labs)
    return out


def tinh(a, b, c, loai, lab=""):
    S, P = sp.Rational(-b, a), sp.Rational(c, a)
    r = sp.solve(a * x**2 + b * x + c, x)
    d = {"tong": S, "tich": P, "Delta": b * b - 4 * a * c, "ac": a * c}
    if b % 2 == 0:
        d["Delta'"] = (b // 2) ** 2 - a * c
    if loai in ("SQ", "SQINV", "SQCUBE"):
        d["SQ"] = S**2 - 2 * P
    if loai in ("INV", "SQINV"):
        d["INV"] = S / P
    if loai in ("CUBE", "SQCUBE"):
        d["CUBE"] = S**3 - 3 * P * S
    if loai == "MIX":
        d["MIX"] = P * S
    if loai in ("HB", "K"):
        # x1^2 = (-b x1 - c)/a, x1^3 = x1 * x1^2
        x1 = sp.symbols("x_1")
        sq = sp.expand((-b * x1 - c) / a)
        cu = sp.expand(sp.expand(x1 * sq).subs(x1**2, sq))
        d["x1^2"], d["x1^3"] = sq, cu
        if loai == "K":
            k, h = K_HB[lab]
            d["K"] = sp.simplify(cu - k * x1 + h)
    if loai == "ASYM":
        d["ASYM"] = (-b) * S - c  # x1² + (-b)x2 = -b(x1+x2) - c  (a = 1)
    if loai == "NHAM":
        d["nghiem"] = sorted(r)
    # kiểm chéo bằng nghiệm thật
    if len(r) == 2:
        x1, x2 = r
        chk = {"SQ": x1**2 + x2**2, "INV": 1 / x1 + 1 / x2, "CUBE": x1**3 + x2**3, "MIX": x1**2 * x2 + x1 * x2**2,
               "ASYM": x1**2 + (-b) * x2}
        for k, v in chk.items():
            if k in d:
                assert sp.simplify(v - d[k]) == 0, (k, v, d[k])
        if "K" in d:
            k, h = K_HB[lab]
            assert sp.simplify(x1**3 - k * x1 + h - d["K"]) == 0
    return d


def main():
    co = da_dung()
    seen, loi = set(), []
    print("== Viète / hạ bậc / nhẩm")
    for lab, (a, b, c), loai, dk, cu, ly in VIETE:
        e = tex(a, b, c)
        assert e not in seen, e
        seen.add(e)
        d = tinh(a, b, c, loai, lab)
        assert d["Delta"] > 0, lab
        if dk == "ac":
            assert a * c < 0, lab
        if dk == "Delta'":
            assert b % 2 == 0 and d["Delta'"] > 0, lab
        if loai == "NHAM":
            assert a + b + c == 0, lab
        if loai == "DELTA":
            assert b % 2 == 0, lab  # Bài 1a cũ có b chẵn (dùng Δ')
        if loai == "NHAM":
            assert a + b + c == 0
        trung = co.get(e)
        print(f"{lab:8} ${e}=0$  [{cu} {ly}]\n         {d}  trùng={trung or '-'}")
        if trung:
            loi.append(lab)
    print("== Biết một nghiệm có căn")
    for lab, b, r1, cu, ly in CAN:
        r2 = sp.expand(-b - r1)
        c = sp.expand(r1 * r2)
        assert c.is_integer, (lab, c)
        e = tex(1, b, int(c))
        assert e not in seen, e
        seen.add(e)
        assert sp.expand(r1**2 + b * r1 + c) == 0
        par = tex(1, b, 0) + "+c"
        trung = co.get(e) or co.get(par)
        print(f"{lab:8} ${par}=0$, x1={r1}  ⇒ x2={r2}, c={c}  (PT đủ ${e}=0$)  [{cu} {ly}]  trùng={trung or '-'}")
        if trung:
            loi.append(lab)
    print("== Ẩn ở mẫu")
    for lab, trai, phai, mc, dkxd, q, cu, ly in MAU:
        kh = sp.expand(sp.cancel((trai - phai) * mc))
        assert sp.expand(kh - q) == 0, (lab, kh)
        ng = sp.solve(q, x)
        nhan = [v for v in ng if v not in dkxd]
        loai_ = [v for v in ng if v in dkxd]
        assert len(nhan) == 1 and len(loai_) == 1, (lab, ng)
        assert sp.simplify((trai - phai).subs(x, nhan[0])) == 0
        e = sp.latex(q).replace(" ", "").replace("^{2}", "^2")
        trung = co.get(e)
        assert e not in seen
        seen.add(e)
        print(f"{lab:8} {trai} = {phai}  ⇒ ${e}=0$, nghiệm {ng}, loại {loai_}, nhận {nhan}  [{cu} {ly}]  trùng={trung or '-'}")
        if trung:
            loi.append(lab)
    print("== Bài lời văn (đề thật trong ngân hàng ch.VI)")
    for lab, pt, q, nghiem, nhan in LOI_VAN:
        kh = sp.factor(sp.together(pt))
        qq = sp.expand(q)
        assert sp.solve(pt, x) == sorted(sp.solve(qq, x)) or set(sp.solve(pt, x)) <= set(sp.solve(qq, x)), (lab, sp.solve(pt, x))
        assert sorted(sp.solve(qq, x)) == sorted(nghiem), (lab, sp.solve(qq, x))
        e = sp.latex(qq).replace(" ", "").replace("^{2}", "^2")
        trung = co.get(e)
        print(f"{lab:8} {pt} = 0  ⇒ ${e}=0$, nghiệm {nghiem}, nhận {nhan}  trùng={trung or '-'}")
        if trung:
            loi.append(lab)
    assert not loi, f"trùng: {loi}"
    print("OK: không phương trình mới nào có trong chương (kể cả phần giữ của F).")


if __name__ == "__main__":
    main()
