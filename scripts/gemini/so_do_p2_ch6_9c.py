#!/usr/bin/env python3
"""Sơ đồ Phiếu 2 ch.VI 9C bản 2 (16/11/2026) — "Bài 20. Định lí Viète — biểu thức đối xứng của hai nghiệm".

Claude chốt: thứ tự khối, mã dạng (dang_id ↔ dòng TM phiếu B), thẻ từng ý, đáp số (SymPy kiểm ở đây).
Gemini chỉ viết chữ (viec_dung_p2_ch6_9c.py). Mã câu = chon-cau.json (tab 9064, phiếu P2).

    .venv/bin/python scripts/gemini/so_do_p2_ch6_9c.py      # kiểm đáp số + đếm thẻ theo dang_id

Luật 16/11: NB = câu nhỏ · TH = bài gọn + câu dẫn `a) [NB] …` rồi ý [TH] · VD = ý [VD] chỉ đề (câu [NB]
trước nó là câu nhỏ tách theo TM dòng NB8, ý [VD] không có gợi ý) · điền khuyết CHỈ ở Ví dụ.
Một bài chỉ khai MỘT mã mỗi band (spec_gate dồn thẻ cùng band về mã đầu) ⇒ NB kiến thức cũ là bài riêng.
"""
from __future__ import annotations

import collections
import re
import sys

import sympy as sp

x, m, X1, X2 = sp.symbols("x m x1 x2")


def nghiem(trai):
    e = sp.expand(sp.sympify(trai))
    return sp.solve(e, x)


def gt(trai, bieu_thuc):
    """Giá trị biểu thức của hai nghiệm (tính trên nghiệm thật, không qua Viète)."""
    r = nghiem(trai)
    if len(r) == 1:
        r = [r[0], r[0]]
    return sp.nsimplify(sp.simplify(sp.sympify(bieu_thuc).subs({X1: r[0], X2: r[1]})))


def kiem():
    loi = []

    def bang(ten, that, mong):
        if sp.simplify(sp.sympify(that) - sp.sympify(mong)) != 0:
            loi.append(f"{ten}: máy ra {that}, sơ đồ ghi {mong}")

    def SP(ten, trai, s, p):
        a, b, c = (sp.Poly(sp.expand(sp.sympify(trai)), x).coeff_monomial(x**k) for k in (2, 1, 0))
        bang(ten + " S", -b / a, s)
        bang(ten + " P", c / a, p)

    def D(ten, trai, mong):
        a, b, c = (sp.Poly(sp.expand(sp.sympify(trai)), x).coeff_monomial(x**k) for k in (2, 1, 0))
        bang(ten + " Δ", sp.expand(b**2 - 4 * a * c), mong)

    def tim_m(ten, trai, he_thuc, mong, dk):
        """Giải hệ thức trên nghiệm thật theo m, lọc điều kiện Δ (dk: biểu thức Δ>0/≥0)."""
        a, b, c = (sp.Poly(sp.expand(sp.sympify(trai)), x).coeff_monomial(x**k) for k in (2, 1, 0))
        S, P = -b / a, c / a
        e = sp.sympify(he_thuc, locals={"S": sp.Symbol("S"), "P": sp.Symbol("P")}).subs({sp.Symbol("S"): S, sp.Symbol("P"): P})
        ung = [v for v in sp.solve(e, m) if dk(sp.expand(b**2 - 4 * a * c).subs(m, v))]
        if set(map(sp.nsimplify, ung)) != set(map(sp.nsimplify, mong)):
            loi.append(f"{ten}: m máy {ung}, sơ đồ {mong}")

    # ── Ví dụ ──
    D("VD1a", "2*x**2+11*x+7", 65); SP("VD1a", "2*x**2+11*x+7", "-11/2", "7/2")
    D("VD1b", "4*x**2-12*x+9", 0); SP("VD1b", "4*x**2-12*x+9", 3, "9/4")
    D("VD2a", "x**2-7*x+5", 29); bang("VD2a A", gt("x**2-7*x+5", "x1**2+x2**2"), 39)
    D("VD2b", "x**2-5*x+3", 13); bang("VD2b", gt("x**2-5*x+3", "(x1-x2)**2"), 13)
    bang("VD3a A", gt("x**2-x-10", "x1**2+x2**2"), 21); bang("VD3a B", gt("x**2-x-10", "1/x1+1/x2"), "-1/10")
    bang("VD3b", gt("x**2+x-6", "x1/x2+x2/x1"), "-13/6")
    bang("VD4", gt("-3*x**2+x+1", "x2/(x1+3)+x1/(x2+3)"), "16/87")
    bang("VD5a", gt("x**2-11*x+30", "x1**3+x2**3"), 341)
    bang("VD5b", gt("x**2-5*x+4", "(5*x1-x2)/x1-(x1-5*x2)/x2"), "23/4")
    # VD6: x²−2x+m−3=0 có nghiệm 1−√2 ⇒ nghiệm kia 1+√2, tổng bình phương 6
    x1 = 1 - sp.sqrt(2); bang("VD6 x2", 2 - x1, "1+sqrt(2)"); bang("VD6", sp.expand(x1**2 + (2 - x1)**2), 6)
    tim_m("VD7", "x**2+(1-m)*x-m", "S**2-2*P-5", [2, -2], lambda d: d > 0)
    D("VD7", "x**2+(1-m)*x-m", "(m+1)**2")
    # ── Luyện tập 1 ──
    bang("B3", gt("x**2-5*x+6", "x1**2+x2**2"), 13)
    D("B4a", "x**2-12*x+8", 112); SP("B4a", "x**2-12*x+8", 12, 8)
    SP("B4b", "2*x**2+11*x-5", "-11/2", "-5/2")
    SP("B4c", "3*x**2-10", 0, "-10/3")
    D("B4d", "x**2-x+3", -11)
    D("B1", "x**2-x+1", -3); D("B2", "x**2+x+1", -3)
    bang("B5", gt("x**2+3*x-5", "x1+x2-x1*x2"), 2)
    bang("B7", sp.Rational(1) * 2 / (-sp.sqrt(2)), "-sqrt(2)")
    # ── Luyện tập 2 ──
    D("B10", "x**2-5*x+2", 17); bang("B10", gt("x**2-5*x+2", "x1**2+x2**2"), 21)
    bang("B11", gt("x**2-7*x-1", "x1**2+x2**2-x1*x2"), 52)
    D("B12", "2*x**2-4*x+1", 8); bang("B12", gt("2*x**2-4*x+1", "1/x1+1/x2"), 4)
    bang("B13", gt("2*x**2-x-5", "x1/x2+x2/x1"), "-21/10")
    bang("B14", gt("x**2+4*x-6", "1/(x1+3)+1/(x2+3)"), "-2/9")
    bang("B15", gt("x**2+5*x-1", "x1**3+x2**3"), -140)
    x1 = (3 - sp.sqrt(5)) / 2; bang("B16 x2", 3 - x1, "(3+sqrt(5))/2")
    bang("B16", sp.expand(x1**2 + (3 - x1)**2), 7)
    D("B17", "x**2+3*x+m", "9-4*m")
    tim_m("B17", "x**2+3*x+m", "S**2-2*P-2025", [-1008], lambda d: d >= 0)
    bang("B18a", nghiem("x**2-4*x+4")[0], 2)
    D("B18", "x**2-(m+2)*x+2*m", "(m-2)**2")
    tim_m("B18", "x**2-(m+2)*x+2*m", "S**2-3*P-7", [-1, 3], lambda d: d >= 0)
    tim_m("B19", "x**2+m*x-6", "S**2-3*P-22", [2, -2], lambda d: d > 0)
    # ── BTVN ──
    D("B20a", "2*x**2-7*x+3", 25); SP("B20a", "2*x**2-7*x+3", "7/2", "3/2")
    D("B20b", "25*x**2-20*x+4", 0); SP("B20b", "25*x**2-20*x+4", "4/5", "4/25")
    SP("B20c", "2*sqrt(2)*x**2-4", 0, "-sqrt(2)")
    D("B21", "2*x**2-7*x+6", 1); SP("B21", "2*x**2-7*x+6", "7/2", 3)
    for ten, tr, mong in (("B22a", "sqrt(2)*x**2-(sqrt(2)+1)*x+1", [1, sp.sqrt(2) / 2]),
                          ("B22b", "2*x**2+(sqrt(3)-1)*x-3+sqrt(3)", [-1, (3 - sp.sqrt(3)) / 2])):
        for v in mong:
            bang(ten + f" x={v}", sp.sympify(tr).subs(x, v), 0)
    D("B24", "x**2-4*sqrt(3)*x+8", 16); bang("B24", gt("x**2-4*sqrt(3)*x+8", "x1**3+x2**3"), "96*sqrt(3)")
    bang("B25", gt("x**2-2*x-9", "x1/x2+x2/x1"), "-22/9")
    bang("B26", gt("x**2-5*x-3", "1/(x1-1)+1/(x2-1)"), "-3/7")
    bang("B27", gt("2*x**2-13*x-6", "(x1+x2)*(x1+2*x2)-x2**2"), "157/4")
    bang("B27 khai triển", sp.expand("(x1+x2)*(x1+2*x2)-x2**2-(x1**2+x2**2+3*x1*x2)"), 0)
    bang("B28", gt("x**2+5*x-7", "x1**2+x2**2-2*x1*x2"), 53)
    x1 = (-sp.sqrt(13) - 5) / 2; bang("B29 x2", -5 - x1, "(-5+sqrt(13))/2")
    bang("B29", sp.expand(x1**2 + (-5 - x1)**2), 19)
    x1 = (1 + sp.sqrt(13)) / 2; x2 = 1 - x1
    bang("B30 x2", x2, "(1-sqrt(13))/2"); bang("B30", sp.expand(3 * x1**2 * x2 + 3 * x1 * x2**2), -9)
    x1 = -sp.sqrt(3); x2 = -4 - x1
    bang("B31 x2", x2, "-4+sqrt(3)"); bang("B31", sp.radsimp(1 / x1 + 1 / x2), "-(16*sqrt(3)+12)/39")
    D("B32", "x**2-6*x-2*m+3", "8*m+24")
    tim_m("B32", "x**2-6*x-2*m+3", "S**2-2*P-20", [sp.Rational(-5, 2)], lambda d: d > 0)
    D("B33", "x**2-2*m*x+4*m-4", "4*(m-2)**2")
    tim_m("B33", "x**2-2*m*x+4*m-4", "S**2-2*P-8", [0, 2], lambda d: d >= 0)
    return loi


# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# (nhãn, chặng, tier, dang_id, level, mã câu + ý, nguồn in sau đề ("" = không in), hình thức, nội dung)
NG_LMN = "HK2 THCS\\&THPT M.V. Lômônôxốp, 2024--2025"
KHOI = [
    # ───────────── LUYỆN TẬP 1 — chỉ NB (12 thẻ) ─────────────
    ("Mạch 1. Tổng và tích hai nghiệm", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "sgk-b20-vd1 (a, b)", "SGK Ví dụ 1 tr.21", "vi_du",
     "Đề SGK (BỎ chữ \"(hoặc $\\Delta'$)\"): \"Không giải phương trình, hãy tính biệt thức $\\Delta$ để kiểm tra điều kiện "
     "có nghiệm, rồi tính tổng và tích các nghiệm của các phương trình: a) $2x^2+11x+7=0$, b) $4x^2-12x+9=0$.\" "
     "a) $\\Delta=11^2-4\\cdot2\\cdot7=65>0$, hai nghiệm phân biệt, $x_1+x_2=-\\dfrac{11}{2}$, $x_1x_2=\\dfrac72$. "
     "b) $\\Delta=(-12)^2-4\\cdot4\\cdot9=0$, hai nghiệm trùng nhau, $x_1+x_2=3$, $x_1x_2=\\dfrac94$ (SGK dùng $\\Delta'$ — "
     "ở đây tính bằng $\\Delta$)."),
    # 17/11 lượt 3 (Thầy: "clean lại những lời thừa … mục đích ra đề hướng tới việc gì, HS ra output ntn"):
    # mỗi câu ghi MỤC TIÊU → OUTPUT; bỏ dữ kiện không dùng; cho sẵn tiền đề khi câu không kiểm tra tiền đề đó.
    ("Bài 1.", "practice1", "onclass", "NB2", 1, "sgk-b20-tl1", "", "dung_sai",
     "[NB] Mục tiêu: Viète chỉ dùng khi phương trình có nghiệm → output: Sai + lí do $\\Delta<0$. Câu dẫn: \"Khẳng định "
     "sau đúng hay sai? Vì sao?\" Khẳng định: \"Tổng và tích hai nghiệm của phương trình $x^2-x+1=0$ đều bằng $1$.\""),
    ("Bài 2.", "practice1", "onclass", "NB2", 1, "sgk-6.43 (bước đầu)", "", "trac_nghiem",
     "[NB] Mục tiêu: nhớ công thức → output: chọn A. Đề: \"Biểu thức $x_1^2+x_2^2$ viết theo $x_1+x_2$ và $x_1x_2$ "
     "là\" A. $(x_1+x_2)^2-2x_1x_2$ · B. $(x_1+x_2)^2+2x_1x_2$ · C. $(x_1+x_2)^2-x_1x_2$ · D. $(x_1+x_2)^2-4x_1x_2$."),
    ("Bài 3.", "practice1", "onclass", "NB2", 1, "sgk-b20-tt1", "", "tra_loi_ngan",
     "[NB] Mục tiêu: như Bài 1, chiều ngược → output: Không + lí do. Đề: \"Phương trình $x^2+x+1=0$ có tổng và tích các "
     "nghiệm là hai số đối nhau không? Vì sao?\" (Không: $\\Delta=-3<0$, vô nghiệm.)"),
    ("Bài 4.", "practice1", "onclass", "NB2", 1, "sgk-6.23 (a–c)", "SGK 6.23", "tra_loi_ngan",
     "Mục tiêu: đọc đúng tổng, tích theo hệ số (dấu của $-\\dfrac ba$) → output: hai số mỗi ý. Tiền đề cho sẵn (không bắt "
     "kiểm tra $\\Delta$): \"Các phương trình sau đều có hai nghiệm phân biệt. Tính tổng và tích các nghiệm của mỗi "
     "phương trình.\" a) [NB] $x^2-12x+8=0$ ($12$ và $8$) b) [NB] $2x^2+11x-5=0$ ($-\\dfrac{11}{2}$ và $-\\dfrac52$) "
     "c) [NB] $3x^2-10=0$ ($0$ và $-\\dfrac{10}{3}$). (Bỏ ý d vô nghiệm — Bài 1, Bài 3 đã kiểm tra điều đó.)"),
    ("Bài 5.", "practice1", "onclass", "NB2", 1, "ck2-gia-lam-2024-III2", "HK2 Phòng GD\\&ĐT Gia Lâm, 2024--2025",
     "tra_loi_ngan",
     "Mục tiêu: chuỗi ba bước một của đề thi → output mỗi ý một kết quả. Đề gốc ở thân: \"Cho phương trình $x^2+3x-5=0$. "
     "Chứng minh rằng phương trình có hai nghiệm phân biệt $x_1$, $x_2$. Tính $x_1+x_2-x_1x_2$.\" a) [NB] Vì sao phương "
     "trình có hai nghiệm phân biệt? ($a\\cdot c=-5<0$) b) [NB] Tính $x_1+x_2$ và $x_1x_2$ ($-3$ và $-5$) c) [NB] Tính "
     "$x_1+x_2-x_1x_2$ ($2$)."),
    ("Mạch 2. Biết một nghiệm, hai nghiệm trái dấu", "practice1", "heading"),
    ("Bài 6.", "practice1", "onclass", "NB4", 1, "tl-viete-56-tr10 (ý a)", "", "dung_sai",
     "[NB] Đúng/Sai: \"Phương trình $x^2-2x+m=0$ có hai nghiệm trái dấu khi $m<0$.\" Đáp: ĐÚNG — hai nghiệm trái dấu "
     "khi $a\\cdot c<0$, tức $1\\cdot m<0$, $m<0$ (khi đó $x_1x_2=m<0$)."),
    ("Bài 7.", "practice1", "onclass", "NB3", 1, "sgk-b20-lt2 (ý c)", "", "tra_loi_ngan",
     "[NB] Phương trình $x^2+2\\sqrt2\\,x+2=0$ có một nghiệm là $x=-\\sqrt2$. Dùng tích hai nghiệm, tìm nghiệm còn lại. "
     "Đáp: $x_1x_2=2$ nên $x_2=\\dfrac{2}{-\\sqrt2}=-\\sqrt2$ (hai nghiệm trùng nhau)."),
    ("Bài 8.", "practice1", "onclass", "NB4", 1, "tl-viete-58-tr11 (ý a)", "", "tra_loi_ngan",
     "[NB] Tìm $m$ để phương trình $x^2+4x+m=0$ có hai nghiệm trái dấu. Đáp: $a\\cdot c=m<0$, vậy $m<0$."),
    ("Mạch 3. Ôn quy đồng mẫu", "practice1", "heading"),
    ("Bài 9.", "practice1", "onclass", "NB1", 1, "v10-thai-thinh-2025-III3 (bước quy đồng)", "", "tra_loi_ngan",
     "[NB] Kiến thức lớp 8, MỘT bước: quy đồng mẫu rồi cộng hai phân thức $\\dfrac{1}{x_1+3}+\\dfrac{1}{x_2+3}$ "
     "($x_1\\ne-3$, $x_2\\ne-3$). Đáp: $\\dfrac{x_2+3+x_1+3}{(x_1+3)(x_2+3)}=\\dfrac{x_1+x_2+6}{(x_1+3)(x_2+3)}$. "
     "KHÔNG khai triển mẫu, KHÔNG viết theo tổng tích (việc đó thuộc Bài 14)."),
    ("Đích + Mạch 4. Tổng các bình phương", "practice2", "heading"),
    ("Ví dụ 2.", "practice2", "", "", 0, "sgk-ltc2-vd1 (a, b) + sgk-6.35 (ý b)", "SGK Ví dụ 1 tr.28, Bài 6.35 tr.29", "vi_du",
     "GỘP: \"a) Cho phương trình $x^2-7x+5=0$. Chứng minh phương trình có hai nghiệm phân biệt $x_1$, $x_2$ và tính "
     "$A=x_1^2+x_2^2$. b) Gọi $x_1$, $x_2$ là hai nghiệm của phương trình $x^2-5x+3=0$. Không giải phương trình, hãy "
     "tính $B=(x_1-x_2)^2$.\" a) $\\Delta=29>0$, $x_1+x_2=7$, $x_1x_2=5$, $A=(x_1+x_2)^2-2x_1x_2=7^2-2\\cdot5=39$. "
     "b) $\\Delta=13>0$, $x_1+x_2=5$, $x_1x_2=3$, $B=(x_1+x_2)^2-4x_1x_2=25-12=13$."),
    ("Bài 10.", "practice2", "onclass", "NB6+TH1", 2, "gk2-co-dong-2024-III2", "GK2 THCS Cổ Đông, 2024--2025", "th_dan",
     "Đề: \"Cho phương trình $x^2-5x+2=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, "
     "hãy tính giá trị biểu thức $A=x_1^2+x_2^2$.\" a) [NB] Tính $\\Delta$, phương trình có hai nghiệm không? "
     "($17>0$) b) [NB] $x_1+x_2=?$, $x_1x_2=?$ ($5$ và $2$) c) [TH] Tính $A$ ($A=21$)."),
    ("Bài 11.", "practice2", "onclass", "NB6+TH1", 2, "ck2-thang-long-2025-III3", "HK2 THCS Thăng Long, 2025--2026",
     "th_dan",
     "Đề: \"Cho phương trình $x^2-7x-1=0$ có hai nghiệm là $x_1$, $x_2$. Không giải phương trình, hãy tính giá trị "
     "của biểu thức $A=x_1^2+x_2^2-x_1x_2$.\" (17/11 Thầy: tính Δ trước) a0) [NB] Tính $\\Delta$ (Δ>0 nên có hai nghiệm phân biệt). a) [NB] Tính $x_1+x_2$ và $x_1x_2$ ($7$ và $-1$) b) [NB] Viết $A$ theo "
     "$x_1+x_2$ và $x_1x_2$ ($A=(x_1+x_2)^2-3x_1x_2$) c) [TH] Tính $A$ ($A=52$). (Đề đã cho có hai nghiệm; lời giải "
     "vẫn ghi một dòng $a\\cdot c=-1<0$.)"),
    ("Mạch 5. Biểu thức chứa phân thức", "practice2", "heading"),
    ("Ví dụ 3.", "practice2", "", "", 0, "tl-viete-04-tr2 + v10-ly-thuong-kiet-2025-III3",
     "b) đề minh hoạ tuyển sinh 10, THCS Lý Thường Kiệt, 2025--2026", "vi_du",
     "GỘP: \"a) Cho phương trình $x^2-x-10=0$. Chứng tỏ phương trình có hai nghiệm phân biệt $x_1$, $x_2$ và tính "
     "$x_1^2+x_2^2$ và $\\dfrac1{x_1}+\\dfrac1{x_2}$. b) Cho phương trình $x^2+x-6=0$. Gọi $x_1$, $x_2$ là hai nghiệm "
     "của phương trình. Không giải phương trình, hãy tính $A=\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$.\" a) $a\\cdot c=-10<0$, "
     "tổng $1$, tích $-10$, $x_1^2+x_2^2=1+20=21$, $\\dfrac1{x_1}+\\dfrac1{x_2}=\\dfrac{x_1+x_2}{x_1x_2}=-\\dfrac1{10}$. "
     "b) $a\\cdot c<0$, tổng $-1$, tích $-6$, $A=\\dfrac{x_1^2+x_2^2}{x_1x_2}=\\dfrac{1+12}{-6}=-\\dfrac{13}{6}$. "
     "Nhấn: tích khác $0$ nên chia được."),
    ("Bài 12.", "practice2", "onclass", "NB6+TH1", 2, "v10-cau-giay-lan1-2026-III3",
     "thi thử vào 10 lần 1, THCS Cầu Giấy, 2025--2026", "th_dan",
     "Đề: \"Biết phương trình bậc hai $2x^2-4x+1=0$ có hai nghiệm $x_1$ và $x_2$. Chứng minh $x_1$, $x_2$ khác $0$ và "
     "tính tổng nghịch đảo hai nghiệm.\" (17/11 Thầy: tính Δ trước) a0) [NB] Tính $\\Delta$ (Δ>0 nên có hai nghiệm phân biệt). a) [NB] Tính $x_1+x_2$ và $x_1x_2$ ($2$ và $\\dfrac12$) b) [NB] Viết "
     "$\\dfrac1{x_1}+\\dfrac1{x_2}$ theo tổng và tích ($\\dfrac{x_1+x_2}{x_1x_2}$) c) [TH] Chứng minh $x_1$, $x_2$ khác $0$ "
     "và tính tổng nghịch đảo hai nghiệm (tích $\\dfrac12\\ne0$, kết quả $4$)."),
    ("Bài 13.", "practice2", "onclass", "NB6+TH1", 2, "ck2-ba-dinh-2024-II3", "HK2 Phòng GD\\&ĐT Ba Đình, 2024--2025",
     "th_dan",
     "Đề: \"Gọi $x_1$, $x_2$ là hai nghiệm của phương trình $2x^2-x-5=0$. Không giải phương trình, hãy tính giá trị "
     "biểu thức $\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$.\" (17/11 Thầy: tính Δ trước) a0) [NB] Tính $\\Delta$ (Δ>0 nên có hai nghiệm phân biệt). a) [NB] Tính $x_1+x_2$ và $x_1x_2$ (một bước; lời giải "
     "vẫn ghi dòng $a\\cdot c=-10<0$; $\\dfrac12$ và $-\\dfrac52$) b) [NB] Quy đồng $\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$ "
     "($\\dfrac{x_1^2+x_2^2}{x_1x_2}$) c) [TH] Tính giá trị biểu thức ($x_1^2+x_2^2=\\dfrac{21}{4}$, kết quả "
     "$-\\dfrac{21}{10}$)."),
    ("Ví dụ 4.", "practice2", "", "", 0, "v10-nguyen-truong-to-2025-III3",
     "đề minh hoạ tuyển sinh 10, THCS Nguyễn Trường Tộ, 2025--2026", "vi_du",
     "\"Cho phương trình $-3x^2+x+1=0$. Gọi $x_1$, $x_2$ là các nghiệm của phương trình, không giải phương trình, hãy "
     "tính giá trị của biểu thức $A=\\dfrac{x_2}{x_1+3}+\\dfrac{x_1}{x_2+3}$.\" $a\\cdot c=-3<0$, tổng $\\dfrac13$, tích "
     "$-\\dfrac13$. Quy đồng: tử $x_2(x_2+3)+x_1(x_1+3)=x_1^2+x_2^2+3(x_1+x_2)=\\dfrac79+1=\\dfrac{16}{9}$ "
     "($x_1^2+x_2^2=\\dfrac19+\\dfrac23=\\dfrac79$), mẫu $(x_1+3)(x_2+3)=x_1x_2+3(x_1+x_2)+9=-\\dfrac13+1+9=\\dfrac{29}{3}$, "
     "$A=\\dfrac{16}{9}:\\dfrac{29}{3}=\\dfrac{16}{87}$. Ghi chú $x=-3$ không là nghiệm nên mẫu khác $0$."),
    ("Bài 14.", "practice2", "onclass", "NB6+TH1", 2, "v10-thai-thinh-2025-III3",
     "đề minh hoạ tuyển sinh 10, THCS Thái Thịnh, 2025--2026", "th_dan",
     "Đề: \"Cho phương trình $x^2+4x-6=0$, gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Tính giá trị của biểu thức "
     "$A=\\dfrac{1}{x_1+3}+\\dfrac{1}{x_2+3}$.\" (17/11 Thầy: tính Δ trước) a0) [NB] Tính $\\Delta$ (Δ>0 nên có hai nghiệm phân biệt). a) [NB] Tính $x_1+x_2$ và $x_1x_2$ "
     "(lời giải ghi dòng $a\\cdot c<0$; $-4$ và $-6$) b) [TH] Tính $A$ (dùng kết quả quy đồng ở Bài 9, khai triển mẫu: "
     "$A=\\dfrac{-4+6}{-6-12+9}=-\\dfrac29$)."),
    ("Mạch 6. Tổng lập phương, biểu thức cần biến đổi", "practice2", "heading"),
    ("Ví dụ 5.", "practice2", "", "", 0, "sgk-6.48 (ý b) + v10-quang-trung-2025-III3",
     "b) đề minh hoạ tuyển sinh 10, THCS Quang Trung, 2025--2026", "vi_du",
     "GỘP: \"a) Cho phương trình $x^2-11x+30=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương "
     "trình, hãy tính $x_1^3+x_2^3$. b) Cho phương trình $x^2-5x+4=0$. Không giải phương trình, hãy tính giá trị của "
     "biểu thức $A=\\dfrac{5x_1-x_2}{x_1}-\\dfrac{x_1-5x_2}{x_2}$.\" a) $\\Delta=1>0$, tổng $11$, tích $30$, "
     "$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=1331-990=341$. b) $\\Delta=9>0$, tổng $5$, tích $4$ (khác $0$), tách "
     "$A=5-\\dfrac{x_2}{x_1}-\\dfrac{x_1}{x_2}+5=10-\\dfrac{x_1^2+x_2^2}{x_1x_2}=10-\\dfrac{17}{4}=\\dfrac{23}{4}$."),
    ("Bài 15.", "practice2", "onclass", "NB6+TH1", 2, "v10-thai-thinh-2025-III3-md2",
     "đề minh hoạ tuyển sinh 10, THCS Thái Thịnh, 2025--2026", "th_dan",
     "Đề: \"Cho phương trình $x^2+5x-1=0$. Tính tổng lập phương hai nghiệm của phương trình.\" (17/11 Thầy: tính Δ trước) a0) [NB] Tính $\\Delta$ (Δ>0 nên có hai nghiệm phân biệt). a) [NB] Tính $x_1+x_2$ và $x_1x_2$ "
     "(lời giải ghi dòng $a\\cdot c=-1<0$; $-5$ và $-1$) b) [TH] Tính $x_1^3+x_2^3$ "
     "($(-5)^3-3\\cdot(-1)\\cdot(-5)=-125-15=-140$)."),
    ("Mạch 7. Biết một nghiệm, tính biểu thức", "practice2", "heading"),
    ("Ví dụ 6.", "practice2", "", "", 0, "ck2-phuc-dong-2024-902-III2", "HK2 THCS Phúc Đồng, 2024--2025", "vi_du",
     "\"Cho phương trình $x^2-2x+m-3=0$. Biết rằng phương trình có một nghiệm bằng $1-\\sqrt2$. Tính tổng bình phương "
     "các nghiệm của phương trình trên.\" Gọi $x_1=1-\\sqrt2$. Theo Viète $x_1+x_2=2$ (không phụ thuộc $m$) nên "
     "$x_2=2-(1-\\sqrt2)=1+\\sqrt2$. $x_1^2+x_2^2=(1-\\sqrt2)^2+(1+\\sqrt2)^2=3-2\\sqrt2+3+2\\sqrt2=6$. Không cần tìm $m$."),
    ("Bài 16.", "practice2", "onclass", "NB7+TH2", 2, "so-hn-minhhoa-III3",
     "đề minh hoạ tuyển sinh 10, Sở GD\\&ĐT Hà Nội", "th_dan",
     "Đề: \"Biết rằng phương trình bậc hai $x^2-3x+a=0$ có một nghiệm là $x=\\dfrac{3-\\sqrt5}{2}$. Tìm tổng bình phương "
     "hai nghiệm của phương trình trên.\" (17/11 Thầy: tính Δ trước — theo đáp án Sở: thay nghiệm tìm $a=1$, $\\Delta=5>0$) a0) [NB] Thay nghiệm, tìm $a$ ($a=1$). a1) [NB] Tính $\\Delta$ ($5$). a) [NB] Tổng hai nghiệm bằng bao nhiêu, có phụ thuộc $a$ không? ($3$, không) "
     "(bỏ câu nghiệm còn lại) c) [TH] Tính tổng bình phương hai nghiệm ($7$; có thể tính tích "
     "$\\dfrac{9-5}{4}=1$ rồi $3^2-2\\cdot1=7$). LƯU Ý chữ $a$ là tham số, không phải hệ số của $x^2$."),
    ("Mạch 8. Tìm $m$ theo hệ thức đối xứng", "practice2", "heading"),
    ("Ví dụ 7.", "practice2", "", "", 0, "v10-be-van-dan-2025-III3",
     "đề minh hoạ tuyển sinh 10, THCS Bế Văn Đàn, 2025--2026", "vi_du",
     "\"Cho phương trình $x^2+(1-m)x-m=0$ ($m$ là tham số). Tìm $m$ để phương trình có hai nghiệm phân biệt $x_1$, $x_2$ "
     "thỏa mãn $x_1^2+x_2^2=5$.\" Bốn bước, mỗi bước một dòng: $\\Delta=(1-m)^2+4m=(m+1)^2$, hai nghiệm phân biệt khi "
     "$m\\ne-1$. Viète $x_1+x_2=m-1$, $x_1x_2=-m$. $x_1^2+x_2^2=(m-1)^2+2m=m^2+1$. $m^2+1=5$, $m=2$ hoặc $m=-2$. Đối chiếu "
     "$m\\ne-1$: cả hai thỏa mãn. Vậy $m=2$ hoặc $m=-2$."),
    ("Bài 17.", "practice2", "onclass", "NB8+TH3", 2, "ck2-thai-thinh-2025-III2", "HK2 THCS Thái Thịnh, 2025--2026",
     "th_dan",
     "Đề: \"Cho phương trình $x^2+3x+m=0$ ($m$ là tham số). Tìm các giá trị của $m$ để phương trình có hai nghiệm thỏa "
     "mãn $x_1^2+x_2^2=2025$.\" a) [NB] Tính $\\Delta$ theo $m$ ($9-4m$) b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$ "
     "($-3$ và $m$) c) [TH] Tìm $m$ (lời giải đủ: điều kiện $9-4m\\ge0$, $m\\le\\dfrac94$ · $x_1^2+x_2^2=9-2m$ · "
     "$9-2m=2025$, $m=-1008$ · đối chiếu thỏa)."),
    ("Bài 18.", "practice2", "onclass", "NB8+VD1", 3, "ck2-hoai-duc-2024-III2 (ý b)", "HK2 Phòng GD\\&ĐT Hoài Đức, 2024--2025",
     "vd_de",
     "SỬA 17/11: BỎ ý a đề gốc (giải với $m=2$ — nhiều bước). Cho phương trình $x^2-(m+2)x+2m=0$ ($m$ là tham số). "
     "a) [NB] Tính $\\Delta$ theo $m$ ($(m-2)^2$). b) [NB] Vì $(m-2)^2\\ge0$ với mọi $m$, phương trình có nghiệm với mọi $m$ "
     "không? (có) c) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$ ($m+2$ và $2m$). d) [VD] Tìm $m$ để phương trình có hai "
     "nghiệm $x_1$, $x_2$ thỏa mãn $x_1^2+x_2^2=7+x_1x_2$ (CHỈ ĐỀ: $(m+2)^2-3\\cdot2m=7$, $m^2-2m-3=0$, $m=-1$ hoặc "
     "$m=3$, cả hai thỏa mãn)."),
    ("Bài 19.", "practice2", "onclass", "NB8+VD1", 3, "ck2-lomonoxop-2024-III2 (a, b) — ĐÍCH", NG_LMN, "vd_de",
     "BÀI ĐÍCH. Cho phương trình $x^2+mx-6=0$. a) [NB] Chứng minh rằng phương trình luôn có hai nghiệm phân biệt "
     "$x_1$, $x_2$ với mọi giá trị của $m$ (ý a của đề: $a\\cdot c=-6<0$). b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$ "
     "($-m$ và $-6$). c) [VD] Tìm giá trị của $m$ để phương trình có hai nghiệm $x_1$, $x_2$ thỏa mãn "
     "$x_1^2+x_2^2-x_1x_2=22$ (ý b của đề, CHỈ ĐỀ: $m^2+18=22$, $m=2$ hoặc $m=-2$)."),
    # ───────────── BTVN — NB rồi TH rồi VD (26 NB + 8 TH + 2 VD) ─────────────
    ("Bài 20.", "reflection", "btvn", "NB2", 1, "sgk-b20-lt1 (a–c)", "", "tra_loi_ngan",
     "Như Bài 4 (tiền đề cho sẵn): \"Các phương trình sau đều có nghiệm. Tính tổng và tích các nghiệm của mỗi phương "
     "trình.\" a) [NB] $2x^2-7x+3=0$ ($\\dfrac72$, $\\dfrac32$). b) [NB] $25x^2-20x+4=0$ ($\\dfrac45$, $\\dfrac{4}{25}$). "
     "c) [NB] $2\\sqrt2\\,x^2-4=0$ (tổng $0$, tích $-\\sqrt2$)."),
    ("Bài 21.", "reflection", "btvn", "NB2", 1, "tl-viete-01-tr1", "", "tra_loi_ngan",
     "Cho phương trình $2x^2-7x+6=0$. a) [NB] Không giải phương trình, chứng minh phương trình có hai nghiệm phân biệt "
     "($\\Delta=1>0$). b) [NB] Tính tổng và tích các nghiệm ($\\dfrac72$ và $3$)."),
    ("Bài 22.", "reflection", "btvn", "NB5", 1, "sgk-6.34 (a, b)", "", "tra_loi_ngan",
     "Tính nhẩm nghiệm: a) [NB] $\\sqrt2\\,x^2-(\\sqrt2+1)x+1=0$ ($a+b+c=0$, $x_1=1$, $x_2=\\dfrac{1}{\\sqrt2}=\\dfrac{\\sqrt2}{2}$). "
     "b) [NB] $2x^2+(\\sqrt3-1)x-3+\\sqrt3=0$ ($a-b+c=0$, $x_1=-1$, $x_2=\\dfrac{3-\\sqrt3}{2}$)."),
    ("Bài 23.", "reflection", "btvn", "NB4", 1, "tl-viete-60-tr11 (ý a)", "", "tra_loi_ngan",
     "[NB] Tìm $m$ để phương trình $x^2-2(m-1)x+m+1=0$ có hai nghiệm trái dấu ($m+1<0$, $m<-1$)."),
    ("Bài 24.", "reflection", "btvn", "NB6+TH1", 2, "ck2-chu-van-an-dn-2025-2 (ý b)",
     "HK2 THCS Chu Văn An, Đà Nẵng, 2025--2026", "th_dan",
     "Gọi $x_1$, $x_2$ là hai nghiệm của $x^2-4\\sqrt3\\,x+8=0$. Không giải phương trình, tính $Q=x_1^3+x_2^3$. "
     "a) [NB] Tính $\\Delta$ ($48-32=16>0$) b) [NB] Tính tổng và tích ($4\\sqrt3$ và $8$) c) [TH] Tính $Q$ ($96\\sqrt3$)."),
    ("Bài 25.", "reflection", "btvn", "NB6+TH1", 2, "v10-thai-thinh-2026-III3", "thi thử vào 10, THCS Thái Thịnh, 2026--2027",
     "th_dan",
     "Cho $x^2-2x-9=0$ có hai nghiệm $x_1$, $x_2$ khác $0$. Không giải phương trình, tính $A=\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$. "
     "a) [NB] Tổng và tích ($2$ và $-9$) b) [NB] Quy đồng $A$ ($\\dfrac{x_1^2+x_2^2}{x_1x_2}$) c) [TH] Tính $A$ "
     "($-\\dfrac{22}{9}$)."),
    ("Bài 26.", "reflection", "btvn", "NB6+TH1", 2, "gk2-nguyen-du-2024-32", "GK2 THCS Nguyễn Du, 2024--2025", "th_dan",
     "Cho $x^2-5x-3=0$, biết phương trình có hai nghiệm $x_1$, $x_2$. Không giải phương trình, tính "
     "$A=\\dfrac{1}{x_1-1}+\\dfrac{1}{x_2-1}$. a) [NB] Tổng và tích ($5$ và $-3$) b) [NB] Quy đồng mẫu $A$, "
     "MỘT bước ($\\dfrac{x_1+x_2-2}{(x_1-1)(x_2-1)}$, không khai triển mẫu) c) [TH] Tính $A$ (khai triển mẫu "
     "$x_1x_2-(x_1+x_2)+1$, kết quả $-\\dfrac37$)."),
    ("Bài 27.", "reflection", "btvn", "NB6+TH1", 2, "v10-to-vinh-dien-2025-III3",
     "đề minh hoạ tuyển sinh 10, THCS Tô Vĩnh Diện, 2025--2026", "th_dan",
     "Cho $2x^2-13x-6=0$ với $x_1$, $x_2$ là nghiệm. Không giải phương trình, tính $A=(x_1+x_2)(x_1+2x_2)-x_2^2$. "
     "a) [NB] Tổng và tích ($\\dfrac{13}{2}$ và $-3$) b) [NB] Khai triển, rút gọn $A$ ($x_1^2+x_2^2+3x_1x_2$) "
     "c) [TH] Tính $A$ ($(x_1+x_2)^2+x_1x_2=\\dfrac{169}{4}-3=\\dfrac{157}{4}$)."),
    ("Bài 28.", "reflection", "btvn", "NB6+TH1", 2, "ck2-phuc-loi-2024-3-2 (a, b)", "HK2 THCS Phúc Lợi, 2024--2025",
     "th_dan",
     "Cho $x^2+5x-7=0$. a) [NB] Chứng minh phương trình có hai nghiệm phân biệt $x_1$, $x_2$ ($a\\cdot c=-7<0$) "
     "b) [NB] Tổng và tích ($-5$ và $-7$) c) [TH] Tính $A=x_1^2+x_2^2-2x_1x_2$ ($(x_1+x_2)^2-4x_1x_2=25+28=53$)."),
    ("Bài 29.", "reflection", "btvn", "NB7+TH2", 2, "v10-tho-loc-l3-2025-III3", "thi thử vào 10 lần 3, THCS Thọ Lộc, 2025--2026",
     "th_dan",
     "Cho $x^2+5x+m=0$, biết một nghiệm là $\\dfrac{-\\sqrt{13}-5}{2}$. Tìm tổng bình phương hai nghiệm. a) [NB] Tổng hai "
     "nghiệm ($-5$) b) [NB] Nghiệm còn lại ($\\dfrac{-5+\\sqrt{13}}{2}$) c) [TH] Tổng bình phương ($19$)."),
    ("Bài 30.", "reflection", "btvn", "NB7+TH2", 2, "ck2-dai-ang-2025-III2", "HK2 THCS Đại Áng, 2025--2026", "th_dan",
     "Cho $x^2-x+m=0$ có hai nghiệm $x_1$, $x_2$ và $x_1=\\dfrac{1+\\sqrt{13}}{2}$. Tính $A=3x_1^2x_2+3x_1x_2^2$. "
     "a) [NB] Tìm $x_2$ ($\\dfrac{1-\\sqrt{13}}{2}$) b) [TH] Tính $A$ ($x_1x_2=-3$, $A=3x_1x_2(x_1+x_2)=-9$)."),
    ("Bài 31.", "reflection", "btvn", "NB7+TH2", 2, "gk2-dong-anh-2025-33", "GK2 xã Đông Anh, 2025--2026", "th_dan",
     "Cho $x^2+4x+m=0$ có hai nghiệm phân biệt $x_1$, $x_2$, trong đó $x_1=-\\sqrt3$. Tính tổng nghịch đảo hai nghiệm. "
     "a) [NB] Tìm $x_2$ ($-4+\\sqrt3$) b) [TH] Tính tổng nghịch đảo ($x_1x_2=4\\sqrt3-3$, "
     "$\\dfrac{-4}{4\\sqrt3-3}=-\\dfrac{16\\sqrt3+12}{39}$)."),
    ("Bài 32.", "reflection", "btvn", "NB8+VD1", 3, "gk2-mai-dich-2024-32", "GK2 THCS Mai Dịch, 2024--2025", "vd_de",
     "Cho $x^2-6x-2m+3=0$. a) [NB] Tính $\\Delta$ theo $m$ ($8m+24$ — chỉ tính, điều kiện $m>-3$ "
     "để vào lời giải ý cuối) b) [NB] Viết tổng và tích theo $m$ ($6$ và $-2m+3$) c) [VD] Tìm $m$ để phương trình có hai "
     "nghiệm phân biệt $x_1$, $x_2$ thỏa mãn $x_1^2+x_2^2=20$ (CHỈ ĐỀ: $36+4m-6=20$, $m=-\\dfrac52$, thỏa $m>-3$)."),
    ("Bài 33.", "reflection", "btvn", "NB8+VD1", 3, "v10-thanh-oai-l2-2025-III3",
     "thi thử vào 10 lần 2, Phòng GD\\&ĐT Thanh Oai, 2025--2026", "vd_de",
     "Cho $x^2-2mx+4m-4=0$. a) [NB] Tính $\\Delta$ theo $m$ ($4(m-2)^2$ — chỉ tính, nhận xét luôn có nghiệm để vào "
     "lời giải ý cuối) b) [NB] Viết tổng và tích "
     "theo $m$ ($2m$ và $4m-4$) c) [VD] Tìm tất cả các giá trị của $m$ để phương trình có hai nghiệm $x_1$, $x_2$ thỏa "
     "mãn $x_1^2+x_2^2-8=0$ (CHỈ ĐỀ: $4m^2-8m+8=8$, $m=0$ hoặc $m=2$)."),
]

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu B
    "NB1": (1, 0), "NB2": (9, 5), "NB3": (1, 0), "NB4": (2, 1), "NB5": (0, 2), "NB6": (15, 10), "NB7": (3, 4),
    "NB8": (7, 4), "TH1": (6, 5), "TH2": (1, 3), "TH3": (1, 0), "VD1": (2, 2),
}


def dem_the():
    dem = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du":
            continue
        _, _, tier, dang, *_, noi = k
        ma = dang.split("+")
        for t in re.findall(r"\[(NB|TH|VD)\]", noi):
            dem[(next(mm for mm in ma if re.match(rf"{t}\d", mm)), tier)] += 1
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
