"""15/11/2026 — Đề KT chương VI 9C, Câu 7 trùng Ví dụ phiếu E (cùng x^2+15x-2700=0, đáp số 45).
Đổi số liệu: 180 km, về tăng 5 km/h, sớm 30 phút ⇒ x^2+5x-1800=0, Δ=7225, x=40 (loại -45).
Idempotent: chạy lại không đổi gì. Chạy: .venv/bin/python scripts/sua_kt_cau7_ch6_9c.py [--ghi]"""
import json, sys, sympy as sp
from pathlib import Path
D = Path("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/kiem-tra-chuong")
x = sp.Symbol("x")
assert sp.solve(sp.Eq(180/x - 180/(x+5), sp.Rational(1, 2)), x) == [-45, 40]
assert sp.expand(360*(x+5) - 360*x - x*(x+5)) == -(x**2 + 5*x - 1800) and 5**2 + 4*1800 == 85**2

DE = [("cách nhau $90$ km. Lúc về, ô tô tăng vận tốc thêm $15$ km/h",
       "cách nhau $180$ km. Lúc về, ô tô tăng vận tốc thêm $5$ km/h")]
MT_ROW = [("ô tô đi $90$ km, lúc về tăng $15$ km/h", "ô tô đi $180$ km, lúc về tăng $5$ km/h")]
MT_LG = [
    (r"$x + 15$ (km/h)", r"$x + 5$ (km/h)"),
    (r"\dfrac{90}{x + 15}", r"\dfrac{180}{x + 5}"),
    (r"\dfrac{90}{x}", r"\dfrac{180}{x}"),
    (r"$180(x + 15) - 180x = x(x + 15)$", r"$360(x + 5) - 360x = x(x + 5)$"),
    (r"$180x + 2700 - 180x = x^2 + 15x$", r"$360x + 1800 - 360x = x^2 + 5x$"),
    (r"$x^2 + 15x - 2700 = 0$", r"$x^2 + 5x - 1800 = 0$"),
    (r"15^2 - 4\cdot 1\cdot (-2700) = 11025", r"5^2 - 4\cdot 1\cdot (-1800) = 7225"),
    (r"\sqrt{\Delta} = 105", r"\sqrt{\Delta} = 85"),
    (r"\dfrac{-15 + 105}{2} = 45", r"\dfrac{-5 + 85}{2} = 40"),
    (r"\dfrac{-15 - 105}{2} = -60", r"\dfrac{-5 - 85}{2} = -45"),
    (r"lúc đi là $45$ km/h", r"lúc đi là $40$ km/h"),
]

def sua(path, rules, chi_khoi=None):
    d = json.loads(path.read_text())
    n = 0
    for st in d["stages"]:
        for b in st["blocks"]:
            for k in ("text", "statement"):
                t = b.get(k)
                if not t or (chi_khoi and chi_khoi not in t):
                    continue
                for a, c in rules:
                    if a in t:
                        t = t.replace(a, c); n += 1
                b[k] = t
    return d, n

ghi = "--ghi" in sys.argv
for name, rules, khoi in [("de-kiem-tra-chuong-vi.json", DE, None),
                          ("ma-tran-va-dap-an-kiem-tra-chuong-vi.json", MT_ROW, None),
                          ("ma-tran-va-dap-an-kiem-tra-chuong-vi.json", MT_LG, r"\textbf{Câu 7 (2,5 điểm).}")]:
    p = D / name
    d, n = sua(p, rules, khoi)
    print(name, "thay", n)
    if ghi and n:
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
s = "".join(open(D / f).read() for f in ("de-kiem-tra-chuong-vi.json", "ma-tran-va-dap-an-kiem-tra-chuong-vi.json"))
if ghi:
    for bad in ("2700", "11025", "$90$ km", "x + 15"):
        assert bad not in s, bad
    print("không còn số liệu cũ")
