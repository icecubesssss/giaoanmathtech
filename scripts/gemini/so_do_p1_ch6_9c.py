#!/usr/bin/env python3
"""Sơ đồ Phiếu 1 ch.VI 9C bản 2 (16/11/2026) — "Bài 19. Phương trình bậc hai một ẩn — biện luận số nghiệm".

Claude chốt: thứ tự khối, mã dạng (dang_id ↔ dòng TM phiếu A), thẻ từng ý, đáp số (SymPy kiểm ở đây).
Gemini chỉ viết chữ (viec_dung_p1_ch6_9c.py). Mã câu = chon-cau.json (Thầy tick tab 9064).

    .venv/bin/python scripts/gemini/so_do_p1_ch6_9c.py      # kiểm đáp số + đếm thẻ theo dang_id

Luật 16/11: NB = câu nhỏ (trắc nghiệm / Đúng–Sai / trả lời ngắn) · TH = bài gọn + câu hỏi dẫn `a) [NB] …`
rồi ý [TH] HS tự trình bày · không VD (khuôn khong_vd) · điền khuyết CHỈ ở Ví dụ.
"""
from __future__ import annotations

import collections
import sys

import sympy as sp

x, m = sp.symbols("x m")


def pt(trai, phai=0):
    """(a, b, c, Δ, tập nghiệm thực) của phương trình bậc hai trai = phai (ẩn x)."""
    e = sp.expand(sp.sympify(trai) - sp.sympify(phai))
    a, b, c = (sp.Poly(e, x).coeff_monomial(x**k) for k in (2, 1, 0))
    d = sp.expand(b**2 - 4 * a * c)
    return a, b, c, d, set(sp.solveset(e, x, sp.S.Reals)) if not e.free_symbols - {x} else None


def kiem():
    loi = []

    def bang(ten, that, mong):
        if isinstance(mong, (tuple, set)):
            ok = (set(map(sp.nsimplify, that)) == set(map(sp.nsimplify, mong)) if isinstance(mong, set)
                  else all(sp.simplify(sp.sympify(u) - sp.sympify(v)) == 0 for u, v in zip(that, mong)))
        else:
            ok = sp.simplify(sp.sympify(that) - sp.sympify(mong)) == 0
        if not ok:
            loi.append(f"{ten}: máy ra {that}, sơ đồ ghi {mong}")

    def nghiem(ten, trai, phai, mong):
        r = pt(trai, phai)[4]
        if {sp.nsimplify(v) for v in r} != {sp.nsimplify(sp.sympify(v)) for v in mong}:
            loi.append(f"{ten}: nghiệm máy {r}, sơ đồ {mong}")

    def delta(ten, trai, phai, mong):
        bang(ten + " Δ", pt(trai, phai)[3], mong)

    # ── Ví dụ ──
    nghiem("VD2", "2*x**2-4*x", 0, [0, 2])
    nghiem("VD3a", "x**2-9", 0, [3, -3])
    nghiem("VD3b", "(x+1)**2", 3, ["-1+sqrt(3)", "-1-sqrt(3)"])
    delta("VD4", "3*x**2+7*x-1", 0, 61)
    nghiem("VD4", "3*x**2+7*x-1", 0, ["(-7+sqrt(61))/6", "(-7-sqrt(61))/6"])
    delta("VD5a", "x**2-6*x+9", 0, 0)
    nghiem("VD5a", "x**2-6*x+9", 0, [3])
    delta("VD5b", "2*x**2+3*x+5", 0, -31)
    nghiem("VD6", "(x+1)**2-3*(x-2)", 7, [0, 1])
    nghiem("VD7", "x**2-1", "5*(x+1)", [-1, 6])
    delta("VD8", "x**2-2*(m+3)*x+m**2-5", 0, "24*m+56")
    delta("VD9", "x**2+(2*m+3)*x+3*m", 0, "4*m**2+9")
    bang("VD9 m", sp.solve(sp.sympify("x**2+(2*m+3)*x+3*m").subs(x, 3), m)[0], -2)
    nghiem("VD9 m=-2", "x**2-x-6", 0, [3, -2])
    delta("VD10", "x**2+m*x-1", 0, "m**2+4")   # đề gốc tham số tên a; phiếu giữ chữ a
    # ── Luyện tập 1 ──
    bang("B1a", pt("3*x**2+2*x-1", "x**2-x")[:3], (2, 3, -1))
    bang("B1b", pt("(2*x+1)**2", "x**2+1")[:3], (3, 4, 0))
    delta("B3a", "11*x**2+13*x-1", 0, 213)
    delta("B3b", "9*x**2+42*x+49", 0, 0)
    delta("B3c", "x**2-2*x+3", 0, -8)
    nghiem("B5", "x**2+7*x+12", 0, [-3, -4])
    nghiem("B6", "x**2-2*x", 0, [0, 2])
    nghiem("B7a", "8*x**2-4*x", 0, [0, sp.Rational(1, 2)])
    nghiem("B7b", "x**2-25", 0, [5, -5])
    nghiem("B7c", "(x+3)**2", 5, ["-3+sqrt(5)", "-3-sqrt(5)"])
    nghiem("B7d", "x**2-15", "3*(x-5)", [0, 3])
    nghiem("B8a", "2*x**2-9*x+7", 0, [1, sp.Rational(7, 2)])
    nghiem("B8b", "3*x**2+11*x+8", 0, [-1, sp.Rational(-8, 3)])
    # ── Luyện tập 2 ──
    delta("B9", "3*x**2-4*x+5", 0, -44)
    delta("B10", "x**2-6*x-14", 0, 92)
    nghiem("B10", "x**2-6*x-14", 0, ["3+sqrt(23)", "3-sqrt(23)"])
    delta("B11", "5*x**2+2*sqrt(10)*x+2", 0, 0)
    nghiem("B11", "5*x**2+2*sqrt(10)*x+2", 0, ["-sqrt(10)/5"])
    delta("B12a", "6*x**2-4*x-1", 0, 40)
    nghiem("B12a", "6*x**2-4*x-1", 0, ["(2+sqrt(10))/6", "(2-sqrt(10))/6"])
    nghiem("B12c", "x**2-sqrt(3)*x+sqrt(3)-1", 0, [1, "sqrt(3)-1"])
    bang("B13 dạng chuẩn", pt("(x+2)*(x-10)", -36)[:3], (1, -8, 16))
    nghiem("B13", "(x+2)*(x-10)", -36, [4])
    delta("B14", "x**2-(2*m-1)*x+m**2-1", 0, "-4*m+5")
    delta("B15", "x**2-(2*m-1)*x+m**2-2", 0, "-4*m+9")
    bang("B16a x=3", sp.expand(sp.sympify("x**2+(m-5)*x-3*(m-2)").subs(x, 3)), 0)
    delta("B16", "x**2+(m-5)*x-3*(m-2)", 0, "(m+1)**2")
    bang("B17 x=1 ⇒ m", sp.solve(sp.sympify("x**2+x+m").subs(x, 1), m)[0], -2)
    nghiem("B17 m=-2", "x**2+x-2", 0, [1, -2])
    bang("B17 A", 2024 * 1 + 2025 * (-2), -2026)
    bang("B18 ac", 1 * -1, -1)
    nghiem("B19a m=5", "x**2+2*(5-3)*x-2*5+5", 0, [1, -5])
    delta("B19", "x**2+2*(m-3)*x-2*m+5", 0, "4*(m-2)**2")
    # ── BTVN ──
    nghiem("B22b", "2*x**2+7*x", 0, [0, sp.Rational(-7, 2)])
    bang("B23 a+b+c", 2 - 7 + 5, 0)
    nghiem("B24a", "2*x**2+6*x", 0, [0, -3])
    nghiem("B24b", "5*x**2+11*x", 0, [0, sp.Rational(-11, 5)])
    nghiem("B24c", "2*x**2+x/3", 0, [0, sp.Rational(-1, 6)])
    nghiem("B24d", "(3*x+2)**2", 5, ["(-2+sqrt(5))/3", "(-2-sqrt(5))/3"])
    nghiem("B25a", "x**2-6*x+5", 0, [1, 5])
    nghiem("B25b", "5*x**2+14*x+9", 0, [-1, sp.Rational(-9, 5)])
    nghiem("B25c", "3*x**2-x-2", 0, [1, sp.Rational(-2, 3)])
    nghiem("B25d", "-4*x**2+x+5", 0, [-1, sp.Rational(5, 4)])
    nghiem("B25e", "x**2-(1+sqrt(2))*x+sqrt(2)", 0, [1, "sqrt(2)"])
    delta("B26", "3*x**2+7*x+2", 0, 25)
    nghiem("B26", "3*x**2+7*x+2", 0, [-2, sp.Rational(-1, 3)])
    delta("B27", "3*x**2-x-5", 0, 61)
    nghiem("B27", "3*x**2-x-5", 0, ["(1+sqrt(61))/6", "(1-sqrt(61))/6"])
    nghiem("B28", "x**2+3*x+2", 0, [-1, -2])
    bang("B29 dạng chuẩn", pt("2*x**2-(x+1)**2", "x-3")[:3], (1, -3, 2))
    nghiem("B29", "2*x**2-(x+1)**2", "x-3", [1, 2])
    bang("B30 dạng chuẩn", pt("(2*x+3)**2", "(x-5)**2")[:3], (3, 22, -16))
    nghiem("B30", "(2*x+3)**2", "(x-5)**2", [sp.Rational(2, 3), -8])
    bang("B31 dạng chuẩn", pt("4*x**2", "(x-12)**2")[:3], (3, 24, -144))
    nghiem("B31", "4*x**2", "(x-12)**2", [4, -12])
    delta("B32", "4*x**2+4*m*x+m+6", 0, "16*(m**2-m-6)")
    bang("B32 m", set(sp.solve(sp.sympify("m**2-m-6"), m)), {3, -2})
    delta("B33", "x**2-2*(m+3)*x+m**2+3", 0, "24*m+24")
    delta("B35", "x**2-m*x+m-1", 0, "(m-2)**2")
    return loi


# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# (nhãn, chặng, tier, dang_id, level, mã câu + ý, nguồn in sau đề ("" = không in), hình thức, nội dung)
# Ví dụ: tier "" , dang_id "" (ví dụ không đếm), hình thức "vi_du".
NG_NTT = "GK2 THCS Nguyễn Trường Tộ, 2025--2026"
KHOI = [
    # ───────────── LUYỆN TẬP 1 — chỉ NB (15 thẻ) ─────────────
    ("Mạch 1. Nhận biết phương trình bậc hai, hệ số và số nghiệm", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "sgk-b19-vd1 (ý a, c)", "SGK Ví dụ 1 tr.11", "vi_du",
     "Trong hai phương trình a) $2x^2-3x+1=0$, c) $\\left(\\dfrac{1}{x}\\right)^2+3\\cdot\\dfrac{1}{x}+2=0$, phương trình nào "
     "là phương trình bậc hai ẩn $x$? Chỉ rõ hệ số $a$, $b$, $c$. Đáp: a) là PT bậc hai, $a=2$, $b=-3$, $c=1$. "
     "c) không phải PT bậc hai ẩn $x$ (có $\\dfrac{1}{x}$, ẩn ở mẫu). Ô điền: $a$, $b$, $c$ của a), chữ \"không phải\" ở c)."),
    ("Bài 1.", "practice1", "onclass", "NB2", 1, "sgk-b19-tl1", "", "dung_sai",
     "[NB] Một khẳng định Đúng/Sai: \"Với $m$ là một số cho trước, phương trình (ẩn $x$) $mx^2+2x+1=0$ là phương trình "
     "bậc hai với $a=m$, $b=2$, $c=1$.\" Đáp: SAI — chỉ là phương trình bậc hai khi $m\\ne 0$ (với $m=0$ là $2x+1=0$)."),
    ("Bài 2.", "practice1", "onclass", "NB2", 1, "sgk-b19-tt1", "", "trac_nghiem",
     "[NB] Trắc nghiệm: phương trình bậc hai $ax^2+bx+c=0$ có $a$ và $c$ trái dấu thì: A. vô nghiệm · B. có nghiệm kép · "
     "C. có hai nghiệm phân biệt · D. chưa kết luận được. Đáp C ($ac<0$ ⇒ $-4ac>0$ ⇒ $\\Delta=b^2-4ac>0$)."),
    ("Bài 3.", "practice1", "onclass", "NB2", 1, "sgk-6.41", "SGK 6.41", "trac_nghiem",
     "[NB] Chép NGUYÊN VĂN SGK 6.41: \"Các nghiệm của phương trình $x^2+7x+12=0$ là\" A. $x_1=3$, $x_2=4$ · "
     "B. $x_1=-3$, $x_2=-4$ · C. $x_1=3$, $x_2=-4$ · D. $x_1=-3$, $x_2=4$. Đáp B."),
    ("Bài 4.", "practice1", "onclass", "NB1", 1, "sgk-6.8 (a, b)", "", "tra_loi_ngan",
     "Yêu cầu: đưa về dạng $ax^2+bx+c=0$ rồi xác định $a$, $b$, $c$. a) [NB] $3x^2+2x-1=x^2-x$ "
     "⇒ $2x^2+3x-1=0$: $a=2$, $b=3$, $c=-1$. b) [NB] $(2x+1)^2=x^2+1$ ⇒ $3x^2+4x=0$: $a=3$, $b=4$, $c=0$."),
    ("Bài 5.", "practice1", "onclass", "NB2", 1, "sgk-6.10 (a, b, c)", "", "tra_loi_ngan",
     "Yêu cầu (không giải): xác định $a$, $b$, $c$, tính $\\Delta$, cho biết số nghiệm. a) [NB] $11x^2+13x-1=0$: "
     "$\\Delta=213>0$, hai nghiệm phân biệt. b) [NB] $9x^2+42x+49=0$: $\\Delta=0$, nghiệm kép. c) [NB] $x^2-2x+3=0$: "
     "$\\Delta=-8<0$, vô nghiệm."),
    ("Mạch 2. Phương trình khuyết $b$, khuyết $c$", "practice1", "heading"),
    ("Ví dụ 2.", "practice1", "", "", 0, "sgk-b19-vd2 (ý a) + sgk-b19-vd3 (a, b)", "SGK Ví dụ 2 tr.11, Ví dụ 3 tr.12", "vi_du",
     "GỘP hai ví dụ SGK thành một: \"Giải các phương trình sau: a) $2x^2-4x=0$, b) $x^2-9=0$, c) $(x+1)^2=3$.\" "
     "a) $2x(x-2)=0$, nên $x=0$ hoặc $x=2$. b) $x^2=9$, $x=3$ hoặc $x=-3$. c) $x+1=\\sqrt3$ hoặc $x+1=-\\sqrt3$, "
     "nên $x=-1+\\sqrt3$ hoặc $x=-1-\\sqrt3$. Mỗi ý kết bằng dòng \"Vậy …\"."),
    ("Bài 6.", "practice1", "onclass", "NB3", 1, "ck2-phan-dinh-phung-2025-TN2", "CK2 THCS Phan Đình Phùng, Đà Nẵng, 2025--2026",
     "trac_nghiem",
     "[NB] Chép NGUYÊN VĂN: \"Phương trình $x^2-2x=0$ có các nghiệm là:\" A. $x_1=0$, $x_2=-\\dfrac12$ · B. $x_1=0$, "
     "$x_2=-2$ · C. $x_1=0$, $x_2=2$ · D. $x_1=0$, $x_2=\\dfrac12$. Đáp C."),
    ("Bài 7.", "practice1", "onclass", "NB3", 1,
     "gk1-thach-ban-2024-IIa + sgk-b19-lt3 (a, b) + gk1-nghia-tan-2025-I1b", "", "tra_loi_ngan",
     "Một yêu cầu \"Giải các phương trình sau:\" 4 ý, nguồn đề thi ghi nhỏ sau ý: a) [NB] $8x^2-4x=0$ (GK1 THCS Thạch Bàn, "
     "2024--2025) ⇒ $x=0$; $x=\\dfrac12$. b) [NB] $x^2-25=0$ ⇒ $x=5$; $x=-5$. c) [NB] $(x+3)^2=5$ ⇒ $x=-3+\\sqrt5$; "
     "$x=-3-\\sqrt5$. d) [NB] $x^2-15=3(x-5)$ (GK1 THCS Nghĩa Tân, 2025--2026) ⇒ $x^2-3x=0$ ⇒ $x=0$; $x=3$ "
     "(lỗi hay gặp: chia hai vế cho $x$ làm mất nghiệm $x=0$)."),
    ("Mạch 3. Nhận xét để kiểm tra nghiệm nhanh", "practice1", "heading"),
    ("Bài 8.", "practice1", "onclass", "NB4", 1, "sgk-6.24 (a, b)", "", "tra_loi_ngan",
     "Yêu cầu: tính $a+b+c$ hoặc $a-b+c$ rồi viết hai nghiệm (dùng nhận xét ở Kiến thức cần nhớ). a) [NB] $2x^2-9x+7=0$: "
     "$a+b+c=0$ ⇒ $x_1=1$, $x_2=\\dfrac72$. b) [NB] $3x^2+11x+8=0$: $a-b+c=0$ ⇒ $x_1=-1$, $x_2=-\\dfrac83$."),
    # ───────────── LUYỆN TẬP 2 — TH (12 thẻ) + câu dẫn NB tách (17 thẻ) ─────────────
    ("Đích + Mạch 4. Giải phương trình bằng công thức nghiệm", "practice2", "heading"),
    ("Ví dụ 3.", "practice2", "", "", 0, "sgk-b19-vd5 + sgk-b19-vd6 (a, b)", "SGK Ví dụ 5, Ví dụ 6 tr.14", "vi_du",
     "GỘP ba trường hợp của $\\Delta$ thành một ví dụ: \"Giải các phương trình sau bằng công thức nghiệm: a) $3x^2+7x-1=0$, "
     "b) $x^2-6x+9=0$, c) $2x^2+3x+5=0$.\" a) $a=3$, $b=7$, $c=-1$, $\\Delta=61>0$, $x_1=\\dfrac{-7+\\sqrt{61}}{6}$, "
     "$x_2=\\dfrac{-7-\\sqrt{61}}{6}$. b) $\\Delta=0$, nghiệm kép $x_1=x_2=3$. c) $\\Delta=-31<0$, vô nghiệm."),
    ("Bài 9.", "practice2", "onclass", "NB5+TH1", 2, "ck2-hat-mon-2025-II1", "CK2 THCS Hát Môn, 2025--2026", "th_dan",
     "Đề gốc: \"Chỉ rõ các hệ số $a$, $b$, $c$ và giải phương trình bậc hai $3x^2-4x+5=0$.\" Tách: a) [NB] Chỉ rõ $a$, $b$, $c$ "
     "($3$; $-4$; $5$). b) [NB] Tính $\\Delta$ và so sánh với $0$ ($\\Delta=-44<0$). c) [TH] Giải phương trình (vô nghiệm)."),
    ("Bài 10.", "practice2", "onclass", "NB5+TH1", 2, "ck2-ba-dinh-2024-II2", "HK2 Phòng GD\\&ĐT Ba Đình, 2024--2025", "th_dan",
     "Đề: \"Sử dụng công thức nghiệm để giải phương trình $x^2-6x-14=0$.\" a) [NB] Tính $\\Delta$ ($92$, $\\sqrt{92}=2\\sqrt{23}$). "
     "b) [TH] Giải: $x_1=3+\\sqrt{23}$, $x_2=3-\\sqrt{23}$."),
    ("Bài 11.", "practice2", "onclass", "NB5+TH1", 2, "gk2-phan-dinh-giot-2024-2 (ý c)", "GK2 THCS Phan Đình Giót, 2024--2025",
     "th_dan",
     "Đề: \"Giải phương trình $5x^2+2\\sqrt{10}\\,x+2=0$.\" a) [NB] Tính $\\Delta$ ($=40-40=0$). b) [TH] Giải: nghiệm kép "
     "$x_1=x_2=-\\dfrac{\\sqrt{10}}{5}$."),
    ("Bài 12.", "practice2", "onclass", "NB5+TH1", 2, "gk2-dong-anh-2025-12 (a, b)", "GK2 xã Đông Anh, 2025--2026", "th_dan",
     "Đề: \"Giải các phương trình: (1) $6x^2-4x-1=0$, (2) $x^2-\\sqrt3\\,x+\\sqrt3-1=0$.\" Tách: a) [NB] Tính $\\Delta$ của (1) "
     "($40$). b) [TH] Giải (1): $x=\\dfrac{2+\\sqrt{10}}{6}$; $x=\\dfrac{2-\\sqrt{10}}{6}$. c) [NB] Tính $a+b+c$ của (2) rồi "
     "viết hai nghiệm ($a+b+c=0$ ⇒ $x_1=1$, $x_2=\\sqrt3-1$)."),
    ("Ví dụ 4.", "practice2", "", "", 0, "gk1-giang-vo-2024-Ia + gk1-nguyen-du-2025-1-3",
     "a) GK1 THCS Giảng Võ, 2024--2025 · b) GK1 THCS Nguyễn Du, 2025--2026", "vi_du",
     "GỘP: \"Giải các phương trình sau: a) $(x+1)^2-3(x-2)=7$, b) $x^2-1=5(x+1)$.\" a) $x^2-x=0$, $x(x-1)=0$, $x=0$ hoặc "
     "$x=1$. b) $x^2-5x-6=0$, $\\Delta=49$, $x_1=6$, $x_2=-1$. Nguồn ghi nhỏ sau từng ý."),
    ("Bài 13.", "practice2", "onclass", "NB5+TH1", 2, "gk1-thanh-cong-2025-II2", "GK1 THCS Thành Công, 2025--2026", "th_dan",
     "Đề: \"Giải phương trình $(x+2)(x-10)=-36$.\" a) [NB] Đưa về dạng $ax^2+bx+c=0$ ($x^2-8x+16=0$). "
     "b) [TH] Giải (nghiệm kép $x=4$)."),
    ("Mạch 5. Tìm $m$ theo số nghiệm của phương trình", "practice2", "heading"),
    ("Ví dụ 5.", "practice2", "", "", 0, "tl-ptb2-07-tr5 (ý b)", "", "vi_du",
     "Cho $x^2-2(m+3)x+m^2-5=0$. Với giá trị nào của $m$ thì phương trình có hai nghiệm phân biệt, có nghiệm kép, vô nghiệm? "
     "$a=1$, $b=-2(m+3)$, $c=m^2-5$; $\\Delta=4(m+3)^2-4(m^2-5)=24m+56$. Hai nghiệm phân biệt khi $24m+56>0$, tức $m>-\\dfrac73$. "
     "Nghiệm kép khi $m=-\\dfrac73$. Vô nghiệm khi $m<-\\dfrac73$."),
    ("Bài 14.", "practice2", "onclass", "NB6+TH2", 2, "ck2-cau-dien-2025-III2 (ý a)", "CK2 THCS Cầu Diễn, 2025--2026", "th_dan",
     "Cho $x^2-(2m-1)x+m^2-1=0$. a) [NB] Phương trình có hai nghiệm phân biệt khi $\\Delta$ thoả điều kiện gì? ($\\Delta>0$) "
     "b) [NB] Tính $\\Delta$ theo $m$ ($-4m+5$). c) [TH] Tìm $m$ để phương trình có hai nghiệm phân biệt ($m<\\dfrac54$)."),
    ("Bài 15.", "practice2", "onclass", "NB6+TH2", 2, "v10-tam-khuong-2025-III3 (ý a)",
     "đề minh hoạ tuyển sinh 10, THCS Tam Khương, 2025--2026", "th_dan",
     "Cho $x^2-(2m-1)x+m^2-2=0$. a) [NB] Phương trình vô nghiệm khi $\\Delta$ thoả điều kiện gì? ($\\Delta<0$) "
     "b) [TH] Tìm $m$ để phương trình vô nghiệm ($\\Delta=-4m+9<0$, $m>\\dfrac94$)."),
    ("Bài 16.", "practice2", "onclass", "NB6+TH2", 2, "tl-ptb2-16-tr6 (a, b)", "", "th_dan",
     "Cho $x^2+(m-5)x-3(m-2)=0$. a) [NB] Thay $x=3$ vào vế trái, rút gọn được gì? (bằng $0$ với mọi $m$, nên $x=3$ luôn là "
     "nghiệm). b) [NB] Phương trình có nghiệm kép khi $\\Delta$ thoả điều kiện gì? ($\\Delta=0$) c) [TH] Tìm $m$ để phương trình "
     "có nghiệm kép ($\\Delta=(m+1)^2$, $m=-1$)."),
    ("Mạch 6. Biết một nghiệm, tìm $m$", "practice2", "heading"),
    ("Ví dụ 6.", "practice2", "", "", 0, "tl-ptb2-14-tr6 (a, b)", "", "vi_du",
     "Cho $x^2+(2m+3)x+3m=0$. a) Tìm $m$ để phương trình có nghiệm $x=3$: thay $x=3$: $9+3(2m+3)+3m=0$, $9m+18=0$, $m=-2$; "
     "khi đó $x^2-x-6=0$ có hai nghiệm $x=3$; $x=-2$. b) Chứng minh phương trình luôn có nghiệm với mọi $m$: "
     "$\\Delta=(2m+3)^2-12m=4m^2+9>0$ với mọi $m$."),
    ("Bài 17.", "practice2", "onclass", "NB8+TH4", 2, "gk2-phan-dinh-giot-2024-33", "GK2 THCS Phan Đình Giót, 2024--2025",
     "th_dan",
     "Đề: \"Biết rằng phương trình bậc hai $x^2+x+m=0$ có hai nghiệm là $x_1=1$ và $x_2$. Tính giá trị của biểu thức "
     "$A=2024x_1+2025x_2$.\" a) [NB] Thay $x=1$ vào phương trình, tìm $m$ ($m=-2$). b) [TH] Tìm $x_2$ rồi tính $A$ "
     "($x^2+x-2=0$, $x_2=-2$, $A=-2026$)."),
    ("Mạch 7. Chứng minh phương trình luôn có nghiệm", "practice2", "heading"),
    ("Ví dụ 7.", "practice2", "", "", 0, "ck2-hai-ba-trung-2024-III2 (ý a)", "HK2 Phòng GD\\&ĐT Hai Bà Trưng, 2024--2025",
     "vi_du",
     "Cho $x^2+ax-1=0$ ($a$ là số thực). Chứng minh phương trình có hai nghiệm phân biệt: tích hệ số $1\\cdot(-1)=-1<0$ "
     "(hệ số của $x^2$ và hệ số tự do trái dấu) nên phương trình luôn có hai nghiệm phân biệt. Cách khác: $\\Delta=a^2+4>0$. "
     "LƯU Ý chữ $a$ ở đây là THAM SỐ (hệ số của $x$), không phải hệ số của $x^2$ — lời giải nói rõ."),
    ("Bài 18.", "practice2", "onclass", "NB7+TH3", 2, "ck2-xuan-dinh-2025-III2 (ý a)", "HK2 THCS Xuân Đỉnh, 2025--2026",
     "th_dan",
     "Cho $x^2-2mx-1=0$ ($m$ là tham số). a) [NB] Tích $a\\cdot c$ bằng bao nhiêu, dấu thế nào? ($-1<0$) "
     "b) [TH] Chứng minh phương trình luôn có hai nghiệm phân biệt với mọi $m$."),
    ("Bài 19.", "practice2", "onclass", "NB7+TH3", 2, "gk2-nguyen-truong-to-2025-2 (a, b) — ĐÍCH", NG_NTT, "th_dan",
     "BÀI ĐÍCH. Cho $x^2+2(m-3)x-2m+5=0$. a) [NB] Thay $m=5$, được phương trình nào? ($x^2+4x-5=0$) b) [TH] Giải phương "
     "trình với $m=5$ ($x=1$; $x=-5$). c) [NB] Tính $\\Delta$ theo $m$ ($4(m-2)^2$). d) [NB] Vì $(m-2)^2\\ge 0$ với mọi $m$, "
     "kết luận gì về $\\Delta$? ($\\Delta\\ge 0$) e) [TH] Chứng minh phương trình luôn có hai nghiệm với mọi $m$ "
     "(bẫy: $\\Delta\\ge0$ chỉ cho \"có nghiệm\", không cho \"hai nghiệm phân biệt\"; đề viết \"hai nghiệm\" — lời giải kết "
     "luận \"luôn có nghiệm (hai nghiệm, có thể trùng nhau khi $m=2$)\")."),
    # ───────────── BTVN — NB rồi TH (26 NB + 10 TH) ─────────────
    ("Bài 20.", "reflection", "btvn", "NB2", 1, "sgk-b19-lt1 (a–d)", "", "tra_loi_ngan",
     "Phương trình nào là phương trình bậc hai ẩn $x$? Chỉ rõ $a$, $b$, $c$. a) [NB] $x^2+5=0$ ($1$; $0$; $5$). b) [NB] "
     "$2x^2+7x=0$ ($2$; $7$; $0$). c) [NB] $\\dfrac{x^2-2x+5}{x}=0$ (không phải). d) [NB] $0{,}5x^2=0$ ($0{,}5$; $0$; $0$)."),
    ("Bài 21.", "reflection", "btvn", "NB2", 1, "sgk-b20-hd3 (a, b)", "", "tra_loi_ngan",
     "Cho $2x^2-7x+5=0$. a) [NB] Xác định $a$, $b$, $c$ rồi tính $a+b+c$ ($0$). b) [NB] Chứng tỏ $x=1$ là một nghiệm "
     "(thay vào: $2-7+5=0$)."),
    ("Bài 22.", "reflection", "btvn", "NB3", 1, "sgk-b19-lt2 (a, b) + sgk-6.9 (a, b)", "", "tra_loi_ngan",
     "Giải các phương trình: a) [NB] $2x^2+6x=0$ ($0$; $-3$). b) [NB] $5x^2+11x=0$ ($0$; $-\\dfrac{11}{5}$). c) [NB] "
     "$2x^2+\\dfrac13x=0$ ($0$; $-\\dfrac16$). d) [NB] $(3x+2)^2=5$ ($\\dfrac{-2+\\sqrt5}{3}$; $\\dfrac{-2-\\sqrt5}{3}$)."),
    ("Bài 23.", "reflection", "btvn", "NB4", 1, "sgk-b20-vd2 (a, b) + tl-viete-47-tr8 (1, 2, 8)", "", "tra_loi_ngan",
     "Tính nhẩm nghiệm (tính $a+b+c$ hoặc $a-b+c$): a) [NB] $x^2-6x+5=0$ ($1$; $5$). b) [NB] $5x^2+14x+9=0$ ($-1$; "
     "$-\\dfrac95$). c) [NB] $3x^2-x-2=0$ ($1$; $-\\dfrac23$). d) [NB] $-4x^2+x+5=0$ ($-1$; $\\dfrac54$). e) [NB] "
     "$x^2-(1+\\sqrt2)x+\\sqrt2=0$ ($1$; $\\sqrt2$)."),
    ("Bài 24.", "reflection", "btvn", "NB5+TH1", 2, "gk2-ban-mai-2025-6a", "GK2 Ban Mai School, 2025--2026", "th_dan",
     "Giải $3x^2+7x+2=0$. a) [NB] Tính $\\Delta$ ($25$). b) [TH] Giải ($x=-\\dfrac13$; $x=-2$)."),
    ("Bài 25.", "reflection", "btvn", "NB5+TH1", 2, "gk2-tay-mo-3-2025-II (ý b)", "GK2 THCS Tây Mỗ 3, 2025--2026", "th_dan",
     "Giải $3x^2-x-5=0$. a) [NB] Tính $\\Delta$ ($61$). b) [TH] Giải ($x=\\dfrac{1\\pm\\sqrt{61}}{6}$ — viết hai nghiệm riêng)."),
    ("Bài 26.", "reflection", "btvn", "NB5+TH1", 2, "ck2-be-van-dan-2025-III2 (ý a)", "CK2 THCS Bế Văn Đàn, 2025--2026",
     "th_dan",
     "Cho $x^2+3x+m=0$. a) [NB] Thay $m=2$, được phương trình nào? ($x^2+3x+2=0$) b) [TH] Giải phương trình khi $m=2$ "
     "($x=-1$; $x=-2$)."),
    ("Bài 27.", "reflection", "btvn", "NB5+TH1", 2, "gk2-ban-mai-2025-6b", "GK2 Ban Mai School, 2025--2026", "th_dan",
     "Giải $2x^2-(x+1)^2=x-3$. a) [NB] Đưa về dạng $ax^2+bx+c=0$ ($x^2-3x+2=0$). b) [TH] Giải ($x=1$; $x=2$)."),
    ("Bài 28.", "reflection", "btvn", "NB5+TH1", 2, "gk1-thach-ban-2024-IIc", "GK1 THCS Thạch Bàn, 2024--2025", "th_dan",
     "Giải $(2x+3)^2=(x-5)^2$. a) [NB] Đưa về dạng $ax^2+bx+c=0$ ($3x^2+22x-16=0$). b) [TH] Giải ($\\Delta=676$, "
     "$x=\\dfrac23$; $x=-8$)."),
    ("Bài 29.", "reflection", "btvn", "NB5+TH1", 2, "gk1-giang-vo-2024-Ib", "GK1 THCS Giảng Võ, 2024--2025", "th_dan",
     "Giải $4x^2=(x-12)^2$. a) [NB] Đưa về dạng $ax^2+bx+c=0$ ($3x^2+24x-144=0$, hay $x^2+8x-48=0$). b) [TH] Giải "
     "($x=4$; $x=-12$)."),
    ("Bài 30.", "reflection", "btvn", "NB6+TH2", 2, "tl-ptb2-08-tr6", "", "th_dan",
     "Cho $4x^2+4mx+m+6=0$. a) [NB] Phương trình có nghiệm kép khi $\\Delta$ thoả điều kiện gì? b) [NB] Tính $\\Delta$ theo $m$ "
     "($16(m^2-m-6)$). c) [TH] Tìm $m$ để phương trình có nghiệm kép ($m=3$; $m=-2$)."),
    ("Bài 31.", "reflection", "btvn", "NB6+TH2", 2, "tl-ptb2-18-tr6 (ý c)", "", "th_dan",
     "Cho $x^2-2(m+3)x+m^2+3=0$. a) [NB] Tính $\\Delta$ theo $m$ ($24m+24$). b) [TH] Tìm $m$ để phương trình có hai nghiệm "
     "phân biệt ($m>-1$)."),
    ("Bài 32.", "reflection", "btvn", "NB7+TH3", 2, "gk2-cau-dien-2025-32 (ý a)", "GK2 THCS Cầu Diễn, 2025--2026", "th_dan",
     "Cho $x^2-2mx-3=0$. a) [NB] Tích $a\\cdot c$ bằng bao nhiêu, dấu thế nào? ($-3<0$) b) [TH] Chứng minh phương trình luôn "
     "có hai nghiệm phân biệt với mọi $m$."),
    ("Bài 33.", "reflection", "btvn", "NB7+TH3", 2, "v10-thanh-oai-l1-2024-III2 (ý a)",
     "thi thử vào 10 lần 1, Phòng GD\\&ĐT Thanh Oai, 2024--2025", "th_dan",
     "Cho $x^2-mx+m-1=0$. a) [NB] Tính $\\Delta$ theo $m$ và viết thành một bình phương ($(m-2)^2$). b) [TH] Chứng minh "
     "phương trình luôn có nghiệm với mọi $m$."),
]

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu A
    "NB1": (2, 0), "NB2": (6, 6), "NB3": (5, 4), "NB4": (2, 5), "NB5": (7, 6), "NB6": (5, 3), "NB7": (4, 2),
    "NB8": (1, 0), "TH1": (5, 6), "TH2": (3, 2), "TH3": (3, 2), "TH4": (1, 0),
}


def dem_the():
    import re
    dem = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du":
            continue
        _, _, tier, dang, *_ , noi = k
        ma = dang.split("+")
        tags = re.findall(r"\[(NB|TH|VD)\]", noi)
        for t in tags:
            dich = next(mm for mm in ma if mm.startswith(t))
            dem[(dich, tier)] += 1
    loi = []
    for d, (lop, btvn) in TM_DANG.items():
        for tier, want in (("onclass", lop), ("btvn", btvn)):
            if dem[(d, tier)] != want:
                loi.append(f"{d} {tier}: sơ đồ {dem[(d, tier)]} thẻ, TM {want}")
    tong = collections.Counter()
    for (d, tier), n in dem.items():
        tong[(d[:2], tier)] += n
    return loi, dict(tong)


if __name__ == "__main__":
    l1 = kiem()
    l2, tong = dem_the()
    print("thẻ:", tong)
    for l in l1 + l2:
        print("✗", l)
    print("SẠCH" if not (l1 + l2) else f"{len(l1 + l2)} lỗi")
    sys.exit(1 if (l1 + l2) else 0)
