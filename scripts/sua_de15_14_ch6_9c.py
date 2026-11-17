#!/usr/bin/env python3
"""Đề 15 phút số 14 (de-kiem-tra.json, ch.VI 9C) đang dùng lại đúng Bài 13a (Cầu Giấy) và Bài 14a (Đống Đa)
của phiếu C ⇒ Thầy (15/11/2026): giữ phiếu C, đổi câu ở đề 15′. Câu 1 ($x^2-5x+2$ = Ví dụ 3 phiếu C) đổi theo luật "trùng thì đổi hết". Số liệu lấy từ ngân hàng ch.VI, SymPy kiểm.

    .venv/bin/python scripts/sua_de15_14_ch6_9c.py [--ghi]      (idempotent)
"""
import json, sys
from pathlib import Path
import sympy as sp

P = Path("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/de-kiem-tra.json")
x = sp.symbols("x")
r3 = sp.solve(-3 * x**2 + x + 1, x); assert sp.simplify(1 / r3[0] + 1 / r3[1]) == -1
r1 = sp.solve(25 * x**2 - 20 * x + 4, x); assert r1 == [sp.Rational(2, 5)]  # nghiệm kép, Δ = 0
r4 = sp.solve(x**2 - 6 * x - 14, x); assert sp.simplify(r4[0]**3 + r4[1]**3) == 468
MOI = {
    # Câu 1 cũ $x^2-5x+2$ trùng Ví dụ 3 phiếu C ⇒ SGK Toán 9 tập hai, Bài 20, Luyện tập 1b (tr.22), đúng dạng câu hỏi
    "Câu 1": dict(dang="Xét $\\Delta$ của $25x^2-20x+4=0$ rồi viết tổng và tích hai nghiệm (SGK Toán 9 tập hai, Bài 20, Luyện tập 1)",
                  dap_an="$\\Delta=0$: nghiệm kép; tổng $=\\dfrac{4}{5}$; tích $=\\dfrac{4}{25}$"),
    "Câu 3": dict(dang="Chứng minh hai nghiệm khác 0 rồi tính tổng nghịch đảo hai nghiệm của $-3x^2+x+1=0$ (bộ đề Vào 10 Phòng GD\\&ĐT Đống Đa, đề 10 THCS Nguyễn Trường Tộ)",
                  dap_an="$ac=-3<0$; tổng $\\dfrac{1}{3}$, tích $-\\dfrac{1}{3}\\ne 0$ nên kết quả $=-1$"),
    "Câu 4": dict(dang="Tính tổng các lập phương hai nghiệm của $x^2-6x-14=0$ (Cuối kì II, Phòng GD\\&ĐT Ba Đình)",
                  dap_an="$6^3-3 \\cdot (-14) \\cdot 6 = 468$"),
}
d = json.loads(P.read_text())
de = next(t for t in d["de"] if t["ma"] == "15-14")
PHAM_VI = ("Ba bước tính biểu thức của hai nghiệm (Câu III.3): xét $\\Delta$, viết tổng và tích hai nghiệm, "
           "ép biểu thức về tổng và tích. Nguồn: Câu 1 SGK Toán 9 tập hai, Bài 20, Luyện tập 1b (tr.22); "
           "Câu 2 công thức SGK Bài 20; Câu 3 bộ đề Vào 10 Phòng GD\\&ĐT Đống Đa, đề 10 THCS Nguyễn Trường Tộ (2025-2026); "
           "Câu 4 đề cuối kì II Phòng GD\\&ĐT Ba Đình (2024-2025).")
if de["pham_vi"] != PHAM_VI:
    print(f"pham_vi:\n  - {de['pham_vi']}\n  + {PHAM_VI}")
    de["pham_vi"] = PHAM_VI
for c in de["cau"]:
    if c["ma"] in MOI:
        for k, v in MOI[c["ma"]].items():
            if c[k] != v:
                print(f"{c['ma']} {k}:\n  - {c[k]}\n  + {v}")
                c[k] = v
if "--ghi" in sys.argv:
    P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print("Đã ghi", P)
