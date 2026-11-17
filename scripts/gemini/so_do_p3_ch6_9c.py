#!/usr/bin/env python3
"""Sơ đồ Phiếu 3 ch.VI 9C bản 2 (17/11/2026) — "Bài 20 (tiếp). Định lí Viète — biểu thức không đối xứng".

Claude CHỐT ĐỀ từng bài (DE — in nguyên văn, luật 17/11 [[cau-hoi-muc-tieu-output]]), thẻ, dang_id (↔ dòng TM
phiếu 3), đáp số (SymPy kiểm ở đây trên nghiệm thật, hệ thức không đối xứng xét cả hai thứ tự nghiệm).
Gemini chỉ viết lời giải, ví dụ điền khuyết, lý thuyết (viec_dung_p3_ch6_9c.py). Mã câu = chon-cau.json (P3).

    .venv/bin/python scripts/gemini/so_do_p3_ch6_9c.py      # kiểm đáp số + đếm thẻ theo dang_id

Bố cục: LT1 = hệ thức bậc nhất (C6-15, NB1 ôn giải hệ đứng đầu) · LT2 = hạ bậc (C6-13), căn/|x| (C6-14),
tìm m hạ bậc (C6-16), hai đề tuyển sinh Hà Nội (2025 C6-16, 2026 = ĐÍCH C6-13) · BTVN ôn P2 → hạ bậc → C6-11 → VD.
Bài làm thêm C6-28 (parabol) tier "extend", không tính giờ.
"""
from __future__ import annotations

import collections
import re
import sys

import sympy as sp

x, m, X1, X2 = sp.symbols("x m x1 x2")
BR = "[[br]]"


def y(*ds):
    return BR + BR.join(ds)


def heso(trai):
    p = sp.Poly(sp.expand(sp.sympify(trai)), x)
    return [p.coeff_monomial(x**k) for k in (2, 1, 0)]


def hai_nghiem(trai):
    r = sp.solve(sp.expand(sp.sympify(trai)), x)
    return (r[0], r[0]) if len(r) == 1 else (r[0], r[1])


def kiem():
    loi = []

    def bang(ten, that, mong):
        if sp.simplify(sp.sympify(that) - sp.sympify(mong)) != 0:
            loi.append(f"{ten}: máy ra {sp.simplify(that)}, sơ đồ ghi {mong}")

    def D(ten, trai, mong):
        a, b, c = heso(trai)
        bang(ten + " Δ", sp.expand(b**2 - 4 * a * c), mong)

    def SP(ten, trai, s=None, p=None):
        a, b, c = heso(trai)
        if s is not None:
            bang(ten + " S", -b / a, s)
        if p is not None:
            bang(ten + " P", c / a, p)

    def gt(ten, trai, bt, mong, thu_tu=None):
        """Giá trị biểu thức trên nghiệm thật. thu_tu: hàm chọn (x1, x2) từ hai nghiệm; None ⇒ cả hai thứ tự."""
        r1, r2 = hai_nghiem(trai)
        cap = [thu_tu(r1, r2)] if thu_tu else [(r1, r2), (r2, r1)]
        for a1, a2 in cap:
            bang(ten, sp.sympify(bt).subs({X1: a1, X2: a2}), mong)

    def tim_m(ten, trai, he_thuc, mong, dk):
        """Hệ thức (=0) không đối xứng: m thỏa khi CÓ một thứ tự nghiệm thỏa. Giải tích hai thứ tự (đối xứng)."""
        r1, r2 = hai_nghiem(trai)
        h = sp.sympify(he_thuc)
        e = sp.simplify(sp.expand(h.subs({X1: r1, X2: r2}) * h.subs({X1: r2, X2: r1})))
        ung = set()
        for v in sp.solve(sp.numer(sp.together(e)), m):
            if v.is_real is False or abs(sp.im(sp.N(v))) > 1e-12:
                continue
            v = sp.nsimplify(sp.re(sp.N(v, 30)), rational=True) if not v.is_Rational else v
            a, b, c = (t.subs(m, v) for t in heso(trai))
            if not dk(sp.expand(b**2 - 4 * a * c)):
                continue
            q1, q2 = hai_nghiem(sp.expand(sp.sympify(trai).subs(m, v)))
            if any(abs(sp.N(h.subs({X1: u1, X2: u2}).subs(m, v), 30)) < 1e-20 for u1, u2 in ((q1, q2), (q2, q1))):
                ung.add(sp.nsimplify(v))
        if ung != set(map(sp.nsimplify, mong)):
            loi.append(f"{ten}: m máy {sorted(ung)}, sơ đồ {mong}")

    def chua(ten, trai, a1, a2):
        """Hai nghiệm cho trước là nghiệm thật."""
        for v in (a1, a2):
            bang(ten + f" x={v}", sp.sympify(trai).subs(x, v), 0)

    am = lambda r1, r2: (min(r1, r2, key=float), max(r1, r2, key=float))     # x1 < x2
    lon = lambda r1, r2: (max(r1, r2, key=float), min(r1, r2, key=float))    # x1 > x2
    # ── LT1: hệ thức bậc nhất ──
    s = sp.solve([X1 + X2 - 3, 2 * X1 - 5 * X2 + 8], [X1, X2]); bang("B1 x1", s[X1], 1); bang("B1 x2", s[X2], 2)
    tim_m("VD1a", "x**2-4*x+m", "x1-x2-4", [0], lambda d: d >= 0)
    tim_m("VD1b", "x**2+2*x+m", "3*x1+2*x2-1", [-35], lambda d: d >= 0)
    D("VD1c", "x**2-2*(m-1)*x+2*m-3", "4*(m-2)**2")
    tim_m("VD1c", "x**2-2*(m-1)*x+2*m-3", "x1-3*x2", [3, sp.Rational(5, 3)], lambda d: d > 0)
    D("B2", "x**2-3*x+m", "9-4*m"); tim_m("B2", "x**2-3*x+m", "x1-2*x2-6", [-4], lambda d: d > 0)
    D("B3", "x**2-3*x+m-1", "13-4*m"); tim_m("B3", "x**2-3*x+m-1", "2*x1-5*x2+8", [3], lambda d: d >= 0)
    D("B4", "x**2+(m+2)*x+2*m", "(m-2)**2"); SP("B4", "x**2+(m+2)*x+2*m", "-m-2", "2*m")
    tim_m("B4", "x**2+(m+2)*x+2*m", "2*x1+3*x2-1", [sp.Rational(-5, 3), sp.Rational(-7, 2)], lambda d: d >= 0)
    s = sp.solve([X1 + X2 + m + 2, 2 * X1 + 3 * X2 - 1], [X1, X2]); bang("B4 x1", s[X1], "-3*m-7"); bang("B4 x2", s[X2], "2*m+5")
    # ── LT2: kiến thức cũ, hạ bậc, căn, tìm m ──
    xx = sp.Symbol("xx", negative=True); bang("B4", sp.sqrt((xx - 3)**2), 3 - xx)
    gt("VD2", "4*x**2-2*x-1", "(x1-x2)**2-x1*(x1-1/2)", 1)
    gt("B5", "x**2-3*x-5", "x1**2+3*x2", 14)
    gt("B6", "x**2-3*x-1", "x1**3+10*x2-30", 3)
    gt("VD3", "x**2-3*x-2025", "sqrt(x1+2026)-Abs(x2+2027)", -2029, am)
    gt("B7", "x**2+10*x+4", "sqrt(-16*x1+5)-x2", 13)
    bang("B7 bình phương", sp.expand((X1 - 3)**2 - (-16 * X1 + 5)).subs(X1**2, -10 * X1 - 4), 0)
    gt("B8", "x**2-8*x-5", "(Abs(x1)-Abs(x2))/(x1**2+x2**2)", sp.Rational(4, 37), lon)
    D("VD4", "x**2-2*m*x-4*m-5", "4*m**2+16*m+20")
    tim_m("VD4", "x**2-2*m*x-4*m-5", "x1**2-2*(m-1)*x1+2*x2-4*m-5-2*x1*x2", [sp.Rational(-5, 6)], lambda d: d >= 0)
    D("B9", "x**2-2*m*x+m-1", "4*m**2-4*m+4")
    tim_m("B9", "x**2-2*m*x+m-1", "x1**2*x2+m*x2-x2-4", [2, -1], lambda d: d > 0)
    tim_m("B10", "x**2+8*x-6", "(70-m*x1**2)-x2*(x1+m*x2)", [1], lambda d: d > 0)
    gt("B10 tổng bình phương", "x**2+8*x-6", "x1**2+x2**2", 76)
    gt("B11 ĐÍCH", "x**2-3*x+1", "(3*x2-1)/x1+3*x1/x2-x1", 18)
    # ── BTVN ──
    x1 = (1 - sp.sqrt(5)) / 2; bang("B12 x2", -1 / x1, "(1+sqrt(5))/2"); bang("B12", x1**3 + (-1 / x1)**3, 4)
    x1 = (3 - sp.sqrt(13)) / 2; bang("B13 x2", 3 - x1, "(3+sqrt(13))/2"); bang("B13", (x1 - (3 - x1))**2, 13)
    tim_m("B14", "x**2-2*x-2", "m/(x1+x2)+x1/x2+x2/x1-6", [20], lambda d: d > 0)
    k_ = sp.Symbol("k")
    kv = [v for v in sp.solve(k_**2 - 2 * (1 - 5 * k_) - 73, k_) if v > 0]; bang("B15 k", kv[0] if len(kv) == 1 else kv, 5)
    D("B15", "x**2+5*x-24", 121); gt("B15", "x**2+5*x-24", "x1**3+x2**3", -485)
    tim_m("B16", "x**2-2*x-1", "x1**2+(m-2)*x1+m*x2-9", [4], lambda d: d > 0)
    # B17: tham số a — tìm a rồi K
    a_ = sp.Symbol("a")
    r1, r2 = sp.solve(2 * x**2 - a_ * x - 6, x)
    av = [v for v in sp.solve(sp.expand((-3 * r1 + r1 * r2**2 - sp.Rational(9, 2)) * (-3 * r2 + r2 * r1**2 - sp.Rational(9, 2))), a_) if v.is_real]
    bang("B17 a", av[0] if len(set(av)) == 1 else av, -3)
    q1, q2 = sp.solve(2 * x**2 + 3 * x - 6, x); bang("B17 K", 1 / q1 + 1 / q2, sp.Rational(1, 2))
    D("B18", "x**2-6*x+m-1", "40-4*m")
    tim_m("B18", "x**2-6*x+m-1", "x1*x2+1-1/x1-1/x2", [3, -2], lambda d: d > 0)
    D("B19", "x**2-(2*m-1)*x-m", "4*m**2+1")
    tim_m("B19", "x**2-(2*m-1)*x-m", "1/x1+1/x2-x1*x2", [1], lambda d: d >= 0)
    gt("B19 A", "x**2-x-1", "x1/x2+x2/x1", -3)
    D("B20", "x**2-(2*m+3)*x+2*(m+1)", "(2*m+1)**2")
    tim_m("B20", "x**2-(2*m+3)*x+2*(m+1)", "x1-4*x2", [1, sp.Rational(-7, 8)], lambda d: d > 0)
    # B21: bất phương trình ẩn m — hệ số của m và vế phải
    for a1, a2 in (hai_nghiem("x**2-4*x+2"), hai_nghiem("x**2-4*x+2")[::-1]):
        e = sp.expand(m * a1 * (a1 - 3) + 5 - (14 - m * (a2**2 + 3 * a1 - 15)))
        bang("B21 hệ số m", sp.simplify(e.coeff(m)), -3); bang("B21 tự do", sp.simplify(e.subs(m, 0)), -9)
    # Làm thêm
    bang("B22 m", sp.solve(4 * (m - 2) - 8, m)[0], 4); chua("B22", "2*x**2+x-3", 1, sp.Rational(-3, 2))
    D("B23", "x**2-4*x-2*m", "16+8*m")
    chua("B24a", "x**2-2*x+1", 1, 1)
    tim_m("B24b", "x**2-(m-1)*x+m-2", "x1**2+(m-1)*x2-7", [-1, 4], lambda d: d >= 0)   # 4 bị loại ở đk ac<0
    return loi


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
N = {
    "ba-dinh-24": r"GK2 THCS Ba Đình, 2024--2025", "mai-dich": r"GK2 THCS Mai Dịch, 2025--2026",
    "lnh": r"GK2 THCS Lê Ngọc Hân, 2024--2025", "van-dien": r"HK2 THCS Thị trấn Văn Điển, 2024--2025",
    "my-dinh-2": r"thi thử vào 10, THCS Mỹ Đình 2, 2026--2027", "tu-lap": r"thi thử vào 10, THCS Tự Lập, 2025--2026",
    "cum": r"thi thử vào 10, Cụm trường THCS công lập, 2026--2027",
    "ld8": r"đề luyện thi vào 10 số 8, Mathtech, 2025--2026",
    "hn25": r"đề tuyển sinh lớp 10 THPT Hà Nội, 2025--2026", "hn26": r"đề tuyển sinh lớp 10 THPT Hà Nội, 2026--2027",
    "phuc-dong": r"HK2 THCS Phúc Đồng, 2025--2026", "tl4": r"thi thử vào 10 lần 4, THCS Thọ Lộc, 2026--2027",
    "tl5": r"thi thử vào 10 lần 5, THCS Thọ Lộc, 2025--2026",
    "qo1": r"thi thử vào 10 lần 1, Phòng GD\&ĐT Quốc Oai, 2024--2025",
    "qo2": r"thi thử vào 10 lần 2, Phòng GD\&ĐT Quốc Oai, 2024--2025",
    "ld6": r"đề luyện thi vào 10 số 6, Mathtech, 2025--2026", "ld17": r"đề luyện thi vào 10 số 17, Mathtech, 2025--2026",
    "ld20": r"đề luyện thi vào 10 số 20, Mathtech, 2025--2026", "ld19": r"đề luyện thi vào 10 số 19, Mathtech, 2025--2026",
    "ld3": r"đề luyện thi vào 10 số 3, Mathtech, 2025--2026", "tv-gk": r"GK2 THCS Trưng Vương, 2025--2026",
    "cau-giay": r"GK2 THCS Cầu Giấy, 2024--2025", "tv-ck": r"HK2 THCS Trưng Vương, 2025--2026",
    "nghia-tan": r"HK2 THCS Nghĩa Tân, 2025--2026", "ngoc-lam": r"HK2 THCS Ngọc Lâm, 2024--2025", "ba-dinh-25": r"GK2 THCS Ba Đình, 2025--2026",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


HE_B1 = r"$\begin{cases}x_1+x_2=3\\2x_1-5x_2=-8\end{cases}$"

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (đã có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN NGUYÊN VĂN, GHI đáp số cho thợ).
KHOI = [
    # ───────────── LUYỆN TẬP 1 — hệ thức bậc nhất giữa hai nghiệm ─────────────
    # 17/11 Thầy: "ôn giải hpt làm chi" ⇒ bỏ bài giải hệ; kiến thức cũ = √(A²)=|A| (Bài 4, đầu LT2).
    ("Mạch 1. Hệ thức bậc nhất giữa hai nghiệm", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "tl-viete-40-tr6 + tl-viete-35-tr6", "", "vi_du",
     r"a) Tìm $m$ để phương trình $x^2-4x+m=0$ có hai nghiệm $x_1$, $x_2$ thỏa mãn $x_1-x_2=4$." + BR
     + r"b) Tìm $m$ để phương trình $x^2+2x+m=0$ có hai nghiệm $x_1$, $x_2$ thỏa mãn $3x_1+2x_2=1$.",
     'Mỗi ý 5 bước, mỗi bước một dòng: điều kiện Δ theo m → Viète → lập hệ (hệ thức đề cho + tổng) → giải hệ ra x1, x2  → thay vào tích tìm m, đối chiếu điều kiện → Vậy.  a) Δ=16−4m≥0, m≤4 · x1+x2=4, x1x2=m · hệ x1+x2=4, x1−x2=4 · x1=4, x2=0 · m=x1x2=0, thỏa m≤4 · Vậy m=0.  b) Δ=4−4m≥0, m≤1 · x1+x2=−2, x1x2=m · hệ x1+x2=−2, 3x1+2x2=1 · x1=5, x2=−7 · m=−35, thỏa · Vậy m=−35.  Ô fill: giá trị Δ/điều kiện, tổng, hệ, x1, x2, m.'),
    ("Bài 1.", "practice1", "onclass", "NB4+TH1", 2, "gk2-ba-dinh-2024-III2 (ý b)", "", "th_dan",
     r"Cho phương trình bậc hai $x^2-3x+m=0$. Tìm $m$ để phương trình có hai nghiệm phân biệt thỏa mãn $x_1-2x_2=6$."
     + ng("ba-dinh-24") + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
                            r"c) [NB] Từ câu b) và hệ thức $x_1-2x_2=6$, lập hệ phương trình ẩn $x_1$, $x_2$.",
                            r"d) [TH] Tìm $m$."),
     "a) Δ=9−4m. b) 3 và m. c) hệ x1+x2=3, x1−2x2=6. d) Theo câu a): hai nghiệm phân biệt khi 9−4m>0, m<9/4 · giải "
     "hệ câu c): x2=−1, x1=4 · m=x1x2=−4 · đối chiếu m<9/4 thỏa · Vậy m=−4."),
    ("Bài 2.", "practice1", "onclass", "NB4+TH1", 2, "gk2-mai-dich-2025-32", "", "th_dan",
     r"Cho phương trình $x^2-3x+m-1=0$. Tìm $m$ để phương trình có hai nghiệm $x_1$, $x_2$ thỏa mãn $2x_1-5x_2=-8$."
     + ng("mai-dich") + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
                          r"c) [NB] Từ câu b) và hệ thức $2x_1-5x_2=-8$, lập hệ phương trình ẩn $x_1$, $x_2$.",
                          r"d) [TH] Tìm $m$."),
     "a) Δ=9−4(m−1)=13−4m. b) 3 và m−1. c) hệ x1+x2=3, 2x1−5x2=−8. d) có nghiệm khi 13−4m≥0, m≤13/4 · giải hệ "
     "câu c) (thế x1=3−x2: 2(3−x2)−5x2=−8, x2=2, x1=1) · x1x2=m−1 nên m−1=2, m=3 · thỏa m≤13/4 · Vậy m=3."),
    # Tách 17/11 (soi PDF: Ví dụ 1 ba ý quá dài, đẩy trang): ý c (tổng phụ thuộc m) đứng ngay trước Bài 4 cùng kiểu.
    ("Ví dụ 2.", "practice1", "", "", 0, "v10-quoc-oai-l1-2024-3.2 (ý b)", "", "vi_du",
     r"Cho phương trình $x^2-2(m-1)x+2m-3=0$ ($m$ là tham số). Tìm $m$ để phương trình có hai nghiệm phân biệt "
     r"$x_1$, $x_2$ thỏa mãn $x_1=3x_2$." + ng("qo1"),
     'Mỗi ý 5 bước, mỗi bước một dòng: điều kiện Δ theo m → Viète → lập hệ (hệ thức đề cho + tổng) → giải hệ ra x1, x2  → thay vào tích tìm m, đối chiếu điều kiện → Vậy.  Δ=[−2(m−1)]²−4(2m−3)=4m²−16m+16=4(m−2)², hai nghiệm phân biệt khi m≠2 · x1+x2=2(m−1), x1x2=2m−3 ·  thay x1=3x2 vào tổng: 4x2=2(m−1), x2=(m−1)/2, x1=3(m−1)/2 · thay vào tích: 3(m−1)²/4=2m−3, 3m²−14m+15=0,  m=3 hoặc m=5/3 · cả hai thỏa m≠2 · Vậy m=3 hoặc m=5/3. Ô fill: giá trị Δ/điều kiện, tổng, hệ, x1, x2, m.'),
    ("Bài 3.", "practice1", "onclass", "NB4+TH1", 2, "gk2-le-ngoc-han-2024-III2 (ý b)", "", "th_dan",
     r"Cho phương trình bậc hai (ẩn $x$): $x^2+(m+2)x+2m=0$. Tìm $m$ biết rằng phương trình có hai nghiệm $x_1$, $x_2$ "
     r"thỏa mãn $2x_1+3x_2=1$." + ng("lnh")
     + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
         r"c) [NB] Từ câu b) và hệ thức $2x_1+3x_2=1$, lập hệ phương trình ẩn $x_1$, $x_2$.", r"d) [TH] Tìm $m$."),
     "a) Δ=(m+2)²−8m=(m−2)². b) −(m+2) và 2m. c) hệ x1+x2=−m−2, 2x1+3x2=1. d) Δ=(m−2)²≥0 với mọi m nên phương trình "
     "luôn có nghiệm · giải hệ: x2=2m+5, x1=−3m−7 · thay vào tích: (−3m−7)(2m+5)=2m, 6m²+31m+35=0, Δ_m=121, "
     "m=−5/3 hoặc m=−7/2 · Vậy m=−5/3 hoặc m=−7/2. (Gọi biệt thức của phương trình ẩn m là Δ₁ để khỏi trùng chữ.)"),
    # ───────────── LUYỆN TẬP 2 — hạ bậc, căn, tìm m, đề Hà Nội ─────────────
    ("Mạch 2. Ôn căn bậc hai", "practice2", "heading"),
    ("Bài 4.", "practice2", "onclass", "NB1", 1, "v10-tu-lap-2026-III3 (bước bỏ căn)", "", "trac_nghiem",
     r"[NB] Với $x<0$, biểu thức $\sqrt{(x-3)^2}$ bằng",
     "Kiến thức cũ (chương III, SGK tập một tr.47), MỘT bước: √(A²)=|A| nên √((x−3)²)=|x−3|, x<0 nên x−3<0, "
     "|x−3|=3−x. Chọn A. Lời giải 1–2 dòng."),
    ("Mạch 3. Hạ bậc nhờ nghiệm của phương trình", "practice2", "heading"),
    ("Ví dụ 3.", "practice2", "", "", 0, "ck2-phuc-dong-2025-III2", "", "vi_du",
     r"Cho phương trình $4x^2-2x-1=0$ có hai nghiệm là $x_1$, $x_2$. Không giải phương trình, hãy tính giá trị của "
     r"biểu thức $A=(x_1-x_2)^2-x_1\left(x_1-\dfrac12\right)$." + ng("phuc-dong"),
     "a·c=−4<0 nên hai nghiệm phân biệt · Viète x1+x2=1/2, x1x2=−1/4 · x1 là nghiệm nên 4x1²−2x1−1=0, 4x1²−2x1=1, "
     "x1(x1−1/2)=x1²−x1/2=1/4 · (x1−x2)²=(x1+x2)²−4x1x2=1/4+1=5/4 · A=5/4−1/4=1 · Vậy A=1. 7–9 ô."),
    ("Bài 5.", "practice2", "onclass", "NB2+TH2", 2, "ck2-van-dien-2024-III2", "", "th_dan",
     r"Cho phương trình $x^2-3x-5=0$. Chứng minh phương trình luôn có hai nghiệm phân biệt $x_1$, $x_2$ và không giải "
     r"phương trình, tính giá trị của biểu thức $A=x_1^2+3x_2$." + ng("van-dien")
     + y("a) [NB] Vì sao phương trình có hai nghiệm phân biệt?", r"b) [NB] Tính $x_1+x_2$.",
         r"c) [NB] Vì $x_1$ là nghiệm của phương trình, viết $x_1^2$ theo $x_1$.", r"d) [TH] Tính $A$."),
     "a) a·c=−5<0. b) x1+x2=3. c) x1²−3x1−5=0 nên x1²=3x1+5. d) Theo câu c), A=3x1+5+3x2=3(x1+x2)+5 · theo câu b) "
     "A=3·3+5=14 · Vậy A=14."),
    ("Bài 6.", "practice2", "onclass", "NB2+TH2", 2, "v10-my-dinh-2-2026-III3", "", "th_dan",
     r"Cho phương trình $x^2-3x-1=0$ có hai nghiệm phân biệt $x_1$, $x_2$. Không giải phương trình, hãy tính giá trị "
     r"của biểu thức $A=x_1^3+10x_2-30$." + ng("my-dinh-2")
     + y(r"a) [NB] Tính $x_1+x_2$.", r"b) [NB] Viết $x_1^2$ theo $x_1$.",
         r"c) [NB] Nhân hai vế của đẳng thức ở câu b) với $x_1$, viết $x_1^3$ theo $x_1^2$ và $x_1$.", r"d) [TH] Tính $A$."),
     "a) 3. b) x1²=3x1+1. c) x1³=3x1²+x1. d) Theo câu b) và c), x1³=3(3x1+1)+x1=10x1+3 · A=10x1+3+10x2−30="
     "10(x1+x2)−27=30−27=3 · Vậy A=3."),
    ("Mạch 4. Biểu thức chứa căn, giá trị tuyệt đối", "practice2", "heading"),
    ("Ví dụ 4.", "practice2", "", "", 0, "v10-tho-loc-l4-2026-III3", "", "vi_du",
     r"Cho phương trình $x^2-3x-2025=0$ có hai nghiệm $x_1$, $x_2$ thỏa mãn $x_1<x_2$. Tính giá trị biểu thức "
     r"$P=\sqrt{x_1+2026}-|x_2+2027|$." + ng("tl4"),
     "a·c=−2025<0 nên hai nghiệm trái dấu, mà x1<x2 nên x1<0<x2 · Viète x1+x2=3 · x1 là nghiệm nên x1²=3x1+2025, "
     "x1+2026=x1²−2x1+1=(x1−1)² · √(x1+2026)=|x1−1|=1−x1 (vì x1<0 nên x1−1<0) · x2>0 nên x2+2027>0, "
     "|x2+2027|=x2+2027 · P=1−x1−x2−2027=−2026−(x1+x2)=−2029 · Vậy P=−2029. Dùng hằng đẳng thức √(A²)=|A| (SGK tập "
     "một tr.47). 7–9 ô."),
    ("Bài 7.", "practice2", "onclass", "NB3+TH3", 2, "v10-tu-lap-2026-III3", "", "th_dan",
     r"Biết phương trình $x^2+10x+4=0$ có hai nghiệm âm phân biệt $x_1$, $x_2$. Không giải phương trình, hãy tính giá "
     r"trị của biểu thức $A=\sqrt{-16x_1+5}-x_2$." + ng("tu-lap")
     + y(r"a) [NB] Viết $x_1^2$ theo $x_1$.", r"b) [NB] Dùng câu a), chứng tỏ $(x_1-3)^2=-16x_1+5$.",
         r"c) [TH] Tính $A$."),
     "a) x1²=−10x1−4. b) (x1−3)²=x1²−6x1+9=−10x1−4−6x1+9=−16x1+5. c) Theo câu b), √(−16x1+5)=√((x1−3)²)=|x1−3| · "
     "x1<0 nên x1−3<0, |x1−3|=3−x1 (như Bài 4) · A=3−x1−x2=3−(x1+x2) · Viète x1+x2=−10 · A=13 · Vậy A=13."),
    ("Bài 8.", "practice2", "onclass", "NB3+TH3", 2, "v10-cum-thcs-cong-lap-2026-III3", "", "th_dan",
     r"Cho phương trình $x^2-8x-5=0$ có hai nghiệm $x_1>x_2$. Không giải phương trình tính giá trị biểu thức "
     r"$T=\dfrac{|x_1|-|x_2|}{x_1^2+x_2^2}$." + ng("cum")
     + y("a) [NB] Hai nghiệm cùng dấu hay trái dấu? Vì sao?", r"b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
         r"c) [NB] Vì $x_1>0>x_2$, viết $|x_1|-|x_2|$ không còn dấu giá trị tuyệt đối.", r"d) [TH] Tính $T$."),
     "a) trái dấu vì a·c=−5<0. b) 8 và −5. c) |x1|−|x2|=x1−(−x2)=x1+x2. d) Theo câu c) tử =x1+x2=8 · "
     "x1²+x2²=(x1+x2)²−2x1x2=64+10=74 · T=8/74=4/37 · Vậy T=4/37."),
    ("Mạch 5. Tìm $m$ bằng cách hạ bậc", "practice2", "heading"),
    ("Ví dụ 5.", "practice2", "", "", 0, "v10-tho-loc-l5-2025-III3", "", "vi_du",
     r"Tìm các giá trị của tham số $m$ sao cho phương trình $x^2-2mx-4m-5=0$ có hai nghiệm $x_1$, $x_2$ thỏa mãn "
     r"$x_1^2-2(m-1)x_1+2x_2-4m=5+2x_1x_2$." + ng("tl5"),
     "Δ=4m²+16m+20=4[(m+2)²+1]>0 với mọi m · Viète x1+x2=2m, x1x2=−4m−5 · x1 là nghiệm nên x1²=2mx1+4m+5 · vế trái "
     "=2mx1+4m+5−2mx1+2x1+2x2−4m=2(x1+x2)+5=4m+5 · vế phải =5+2(−4m−5)=−8m−5 · 4m+5=−8m−5, m=−5/6 · Vậy m=−5/6. 7–9 ô."),
    ("Bài 9.", "practice2", "onclass", "NB5+TH4", 2, "v10-luyen-de-8-2025-III3", "", "th_dan",
     r"Cho phương trình $x^2-2mx+m-1=0$ ($m$ là tham số). Tìm $m$ để phương trình có hai nghiệm phân biệt $x_1$, $x_2$ "
     r"thỏa mãn hệ thức $x_1^2x_2+mx_2-x_2=4$." + ng("ld8")
     + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1x_2$ theo $m$.",
         r"c) [NB] Vì $x_1$ là nghiệm của phương trình, viết $x_1^2$ theo $x_1$ và $m$.", r"d) [TH] Tìm $m$."),
     "a) Δ=4m²−4m+4. b) m−1. c) x1²=2mx1−m+1. d) Δ=(2m−1)²+3>0 với mọi m nên luôn có hai nghiệm phân biệt · theo "
     "câu c) x1²x2=2mx1x2−(m−1)x2 · vế trái =2mx1x2−(m−1)x2+(m−1)x2=2mx1x2=2m(m−1) · 2m(m−1)=4, m²−m−2=0, m=2 hoặc "
     "m=−1 · Vậy m=2 hoặc m=−1."),
    ("Mạch 6. Đề tuyển sinh lớp 10 Hà Nội", "practice2", "heading"),
    ("Bài 10.", "practice2", "onclass", "NB5+VD4", 3, "so-hn-2025-III3", "", "vd_de",
     r"Biết phương trình bậc hai $x^2+8x-6=0$ có hai nghiệm $x_1$ và $x_2$, tìm tất cả giá trị của $m$ thỏa mãn "
     r"$\dfrac{70-mx_1^2}{x_2}=x_1+mx_2$." + ng("hn25")
     + y("a) [NB] Vì sao phương trình có hai nghiệm phân biệt?", r"b) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
         r"c) [NB] Vì sao $x_2\ne0$?", r"d) [NB] Viết $x_1^2+x_2^2$ theo $x_1+x_2$ và $x_1x_2$.", r"e) [VD] Tìm $m$."),
     "a) a·c=−6<0. b) −8 và −6. c) x1x2=−6≠0. d) (x1+x2)²−2x1x2. e) (chỉ đề) nhân hai vế với x2≠0: "
     "70−mx1²=x1x2+mx2² · 70=x1x2+m(x1²+x2²) · x1²+x2²=64+12=76 · 70=−6+76m, m=1 · Vậy m=1."),
    ("Bài 11.", "practice2", "onclass", "NB2+VD1", 3, "so-hn-2026-III3 — ĐÍCH", "", "vd_de",
     r"Biết phương trình bậc hai $x^2-3x+1=0$ có hai nghiệm phân biệt $x_1$ và $x_2$, tính giá trị của biểu thức "
     r"$Q=\dfrac{3x_2-1}{x_1}+\dfrac{3x_1}{x_2}-x_1$." + ng("hn26")
     + y(r"a) [NB] Tính $x_1+x_2$ và $x_1x_2$.", r"b) [NB] Vì sao $x_1$, $x_2$ khác $0$?",
         r"c) [NB] Vì $x_2$ là nghiệm của phương trình, viết $3x_2-1$ theo $x_2$.",
         r"d) [NB] Viết $x_1^3+x_2^3$ theo $x_1+x_2$ và $x_1x_2$.", r"e) [VD] Tính $Q$."),
     "BÀI ĐÍCH. a) 3 và 1. b) x1x2=1≠0. c) 3x2−1=x2². d) (x1+x2)³−3x1x2(x1+x2). e) (chỉ đề) theo câu c) "
     "(3x2−1)/x1=x2²/x1 · 3x1/x2−x1=(3x1−x1x2)/x2=(3x1−1)/x2=x1²/x2 (vì x1x2=1 và x1²=3x1−1) · "
     "Q=x2²/x1+x1²/x2=(x1³+x2³)/(x1x2) · x1³+x2³=27−9=18 · Q=18 · Vậy Q=18."),
    # ───────────── BTVN — ôn P2, hạ bậc, tìm tham số; TH rồi VD (26 NB + 8 TH + 2 VD) ─────────────
    ("Bài 12.", "reflection", "btvn", "NB8+TH7", 2, "v10-luyen-de-6-2025-III3", "", "th_dan",
     r"Cho phương trình bậc hai (ẩn $x$): $x^2-mx-1=0$ có một nghiệm là $x=\dfrac{1-\sqrt5}{2}$. Tính tổng lập phương "
     r"hai nghiệm của phương trình trên." + ng("ld6")
     + y(r"a) [NB] Tích hai nghiệm bằng bao nhiêu? Tích đó có phụ thuộc $m$ không?", "b) [NB] Tìm nghiệm còn lại.",
         "c) [TH] Tính tổng lập phương hai nghiệm."),
     "a) x1x2=−1, không phụ thuộc m. b) x2=−1/x1=(1+√5)/2. c) x1+x2=1 · x1³+x2³=(x1+x2)³−3x1x2(x1+x2)=1+3=4 · Vậy 4."),
    ("Bài 13.", "reflection", "btvn", "NB8+TH7", 2, "v10-luyen-de-17-2025-III3", "", "th_dan",
     r"Cho phương trình $x^2-3x+m=0$ ($x$ là ẩn, $m$ là tham số) có một nghiệm là $x=\dfrac{3-\sqrt{13}}{2}$. Tính bình "
     r"phương hiệu các nghiệm của phương trình đó." + ng("ld17")
     + y("a) [NB] Tìm nghiệm còn lại.", "b) [TH] Tính bình phương hiệu các nghiệm."),
     "a) x1+x2=3 nên x2=(3+√13)/2. b) (x1−x2)²=(−√13)²=13 · Vậy 13."),
    ("Bài 14.", "reflection", "btvn", "NB7+TH6", 2, "v10-luyen-de-20-2025-III3", "", "th_dan",
     r"Cho phương trình $x^2-2x-2=0$ có hai nghiệm $x_1$, $x_2$. Tìm tất cả các giá trị của $m$ thỏa mãn "
     r"$\dfrac{m}{x_1+x_2}+\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}=6$." + ng("ld20")
     + y(r"a) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
         r"b) [NB] Viết $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$ theo $x_1+x_2$ và $x_1x_2$.", r"c) [TH] Tìm $m$."),
     "a) 2 và −2 (lời giải có dòng a·c=−2<0). b) ((x1+x2)²−2x1x2)/(x1x2). c) x1/x2+x2/x1=(4+4)/(−2)=−4 · m/2−4=6 · "
     "m=20 · Vậy m=20."),
    # 17/11 Thầy "chọn lại": bỏ luyện đề 19 (trùng phương trình đề đích) ⇒ đề thi Ngọc Lâm T901 (C6-11).
    ("Bài 15.", "reflection", "btvn", "NB6+TH5", 2, "ck2-ngoc-lam-2024-T901-III2", "", "th_dan",
     r"Cho phương trình bậc hai (ẩn $x$): $x^2+kx+1-5k=0$ ($k>0$), biết rằng phương trình có hai nghiệm $x_1$, $x_2$ "
     r"thỏa mãn $x_1^2+x_2^2=73$. Tính giá trị biểu thức $B=x_1^3+x_2^3$." + ng("ngoc-lam")
     + y(r"a) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $k$.", r"b) [NB] Viết $x_1^2+x_2^2$ theo $x_1+x_2$ và $x_1x_2$.",
         r"c) [NB] Viết $x_1^3+x_2^3$ theo $x_1+x_2$ và $x_1x_2$.", r"d) [TH] Tính $B$."),
     "a) x1+x2=−k, x1x2=1−5k. b) (x1+x2)²−2x1x2. c) (x1+x2)³−3x1x2(x1+x2). d) Theo câu a) và b): k²−2(1−5k)=73, "
     "k²+10k−75=0, k=5 hoặc k=−15 · vì k>0 nên k=5 (khi đó Δ=k²−4(1−5k)=121>0, phương trình có hai nghiệm phân biệt) · "
     "x1+x2=−5, x1x2=−24 · theo câu c) B=(−5)³−3·(−24)·(−5)=−125−360=−485 · Vậy B=−485."),
    ("Bài 16.", "reflection", "btvn", "NB5+TH4", 2, "v10-luyen-de-3-2025-III3", "", "th_dan",
     r"Cho phương trình $x^2-2x-1=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Tìm $m$ sao cho "
     r"$x_1^2+(m-2)x_1+mx_2=9$." + ng("ld3")
     + y("a) [NB] Vì sao phương trình có hai nghiệm phân biệt?", r"b) [NB] Tính $x_1+x_2$.",
         r"c) [NB] Viết $x_1^2$ theo $x_1$.", r"d) [TH] Tìm $m$."),
     "a) a·c=−1<0. b) 2. c) x1²=2x1+1. d) vế trái =2x1+1+(m−2)x1+mx2=1+m(x1+x2)=1+2m · 1+2m=9 · m=4 · Vậy m=4."),
    ("Bài 17.", "reflection", "btvn", "NB6+TH5", 2, "gk2-trung-vuong-2025-III2", "", "th_dan",
     r"Cho phương trình bậc hai $2x^2-ax-6=0$, biết rằng phương trình có hai nghiệm $x_1$, $x_2$ thỏa mãn "
     r"$-3x_1+x_1x_2^2=\dfrac92$. Tính giá trị biểu thức $K=\dfrac{1}{x_1}+\dfrac{1}{x_2}$." + ng("tv-gk")
     + y(r"a) [NB] Tính $x_1x_2$.", r"b) [NB] Dùng câu a), viết $x_1x_2^2$ theo $x_2$.", r"c) [NB] Viết $x_1+x_2$ theo $a$.",
         r"d) [TH] Tính $K$."),
     "Chữ a là THAM SỐ, không gọi là hệ số. a) x1x2=−6/2=−3. b) x1x2²=(x1x2)x2=−3x2. c) x1+x2=a/2. d) Theo câu b) "
     "hệ thức thành −3x1−3x2=9/2 nên x1+x2=−3/2 (khi đó a=−3) · K=(x1+x2)/(x1x2)=(−3/2):(−3)=1/2 · Vậy K=1/2."),
    ("Bài 18.", "reflection", "btvn", "NB6+TH5", 2, "gk2-cau-giay-2024-II3", "", "th_dan",
     r"Cho phương trình $x^2-6x+m-1=0$ với $m$ là tham số. Tìm tất cả các giá trị của $m$ để phương trình có hai nghiệm "
     r"phân biệt thỏa mãn $x_1x_2+1=\dfrac{1}{x_1}+\dfrac{1}{x_2}$." + ng("cau-giay")
     + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
         r"c) [NB] Để $\dfrac{1}{x_1}$, $\dfrac{1}{x_2}$ có nghĩa thì $x_1x_2$ phải thỏa mãn điều kiện gì?",
         r"d) [TH] Tìm $m$."),
     "a) Δ=36−4(m−1)=40−4m. b) 6 và m−1. c) x1x2≠0. d) điều kiện 40−4m>0, m<10 và m−1≠0, m≠1 · hệ thức thành "
     "m=6/(m−1) · m²−m−6=0 · m=3 hoặc m=−2 · đối chiếu cả hai thỏa · Vậy m=3 hoặc m=−2."),
    ("Bài 19.", "reflection", "btvn", "NB6+TH5", 2, "ck2-trung-vuong-2025-III3", "", "th_dan",
     r"Cho biết phương trình $x^2-(2m-1)x-m=0$ có hai nghiệm $x_1$, $x_2$ thỏa mãn $\dfrac{1}{x_1}+\dfrac{1}{x_2}=x_1x_2$. "
     r"Tính giá trị của biểu thức $A=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$." + ng("tv-ck")
     + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
         r"c) [NB] Viết $\dfrac{1}{x_1}+\dfrac{1}{x_2}$ theo $x_1+x_2$ và $x_1x_2$.", r"d) [TH] Tính $A$."),
     "a) Δ=(2m−1)²+4m=4m²+1>0 với mọi m. b) 2m−1 và −m. c) (x1+x2)/(x1x2). d) cần x1x2≠0, m≠0 · (2m−1)/(−m)=−m · "
     "m²−2m+1=0 · m=1 (thỏa) · khi đó x1+x2=1, x1x2=−1 · A=((x1+x2)²−2x1x2)/(x1x2)=3/(−1)=−3 · Vậy A=−3."),
    ("Bài 20.", "reflection", "btvn", "NB4+VD3", 3, "tl-viete-38-tr6", "", "vd_de",
     r"Cho phương trình $x^2-(2m+3)x+2(m+1)=0$ (ẩn $x$, tham số $m$). Tìm $m$ để phương trình có hai nghiệm phân biệt "
     r"mà nghiệm này gấp $4$ lần nghiệm kia."
     + y(r"a) [NB] Tính $\Delta$ theo $m$.", r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
         r"c) [NB] Viết điều kiện \textquotedblleft nghiệm này gấp $4$ lần nghiệm kia\textquotedblright\ thành một hệ "
         r"thức giữa $x_1$ và $x_2$.", r"d) [VD] Tìm $m$."),
     "a) Δ=(2m+3)²−8(m+1)=4m²+4m+1=(2m+1)². b) 2m+3 và 2(m+1). c) x1=4x2. d) (chỉ đề) hai nghiệm phân biệt khi "
     "m≠−1/2 · thay x1=4x2 vào tổng: 5x2=2m+3, x2=(2m+3)/5, x1=4(2m+3)/5 · thay vào tích: 4(2m+3)²/25=2(m+1), "
     "8m²−m−7=0, m=1 hoặc m=−7/8 · cả hai thỏa m≠−1/2 · Vậy m=1 hoặc m=−7/8."),
    ("Bài 21.", "reflection", "btvn", "NB2+VD1", 3, "ck2-nghia-tan-2025-III2", "", "vd_de",
     r"Cho phương trình bậc hai $x^2-4x+2=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, "
     r"hãy tìm các giá trị của tham số $m$ thỏa mãn bất phương trình $mx_1(x_1-3)+5>14-m(x_2^2+3x_1-15)$."
     + ng("nghia-tan")
     + y(r"a) [NB] Tính $x_1+x_2$.", r"b) [NB] Viết $x_1^2$ theo $x_1$.", r"c) [NB] Viết $x_2^2$ theo $x_2$.",
         r"d) [VD] Tìm $m$."),
     "a) 4 (lời giải có dòng Δ=8>0). b) x1²=4x1−2. c) x2²=4x2−2. d) (chỉ đề) x1(x1−3)=x1−2 · x2²+3x1−15=3x1+4x2−17 · "
     "bất phương trình thành m(x1−2)+5>14−m(3x1+4x2−17) · m(4x1+4x2−19)>9 · m(16−19)>9 · −3m>9 · m<−3 · Vậy m<−3."),
    # ───────────── BÀI LÀM THÊM (tier extend, không tính giờ — TM dòng TH8, TH9, VD5) ─────────────
    ("Bài 22.", "reflection", "extend", "TH8", 2, "gk2-ba-dinh-2025-I", "", "th_dan",
     r"Cho hàm số $y=(m-2)x^2$ (với $m\ne2$) có đồ thị là parabol $(P)$." + ng("ba-dinh-25")
     + y(r"a) Tìm $m$ để $(P)$ đi qua điểm $A(-2;\,8)$.",
         r"b) Với $m$ tìm được ở câu a), tìm tọa độ giao điểm của $(P)$ với đường thẳng $(d)\colon y=-x+3$."),
     "a) 8=(m−2)·4, m=4 (thỏa m≠2). b) y=2x² · phương trình hoành độ 2x²=−x+3, 2x²+x−3=0 · a+b+c=0 nên x=1 hoặc "
     "x=−3/2 · giao điểm (1; 2) và (−3/2; 9/2)."),
    ("Bài 23.", "reflection", "extend", "TH9", 2, "tl-ptb2-23-tr8", "", "th_dan",
     r"Tìm tham số $m$ để đường thẳng $(d)\colon y=2x+m$ cắt parabol $(P)\colon y=\dfrac12x^2$ tại hai điểm phân biệt.",
     "phương trình hoành độ (1/2)x²=2x+m, x²−4x−2m=0 · Δ=16+8m>0 · m>−2 · Vậy m>−2."),
    ("Bài 24.", "reflection", "extend", "VD5", 3, "v10-quoc-oai-l2-2024-3.2", "", "vd_de",
     r"Trong mặt phẳng tọa độ $Oxy$, cho parabol $(P)\colon y=x^2$ và đường thẳng $(d)\colon y=(m-1)x-m+2$ (với $m$ là "
     r"tham số)." + ng("qo2")
     + y(r"a) Tìm tọa độ giao điểm của $(d)$ và $(P)$ khi $m=3$.",
         r"b) Tìm $m$ để $(d)$ cắt $(P)$ tại hai điểm nằm về hai phía của trục tung và có hoành độ $x_1$, $x_2$ thỏa "
         r"mãn $x_1^2+(m-1)x_2=7$."),
     "a) x²=2x−1, (x−1)²=0, x=1 · giao điểm (1; 1). b) x²−(m−1)x+m−2=0 · hai phía trục tung khi a·c=m−2<0, m<2 · "
     "x1²=(m−1)x1−m+2 · vế trái =(m−1)(x1+x2)−m+2=(m−1)²−m+2=m²−3m+3 · m²−3m+3=7, m²−3m−4=0, m=−1 hoặc m=4 · "
     "đối chiếu m<2: m=−1 · Vậy m=−1."),
]

OPTIONS = {"Bài 4.": [r"$3-x$", r"$x-3$", r"$x+3$", r"$-x-3$"]}   # trắc nghiệm, đáp án A

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 3
    "NB1": (1, 0), "NB2": (10, 3), "NB3": (5, 0), "NB4": (9, 3), "NB5": (7, 3), "NB6": (0, 12), "NB7": (0, 2),
    "NB8": (0, 3), "TH1": (3, 0), "TH2": (2, 0), "TH3": (2, 0), "TH4": (1, 1), "TH5": (0, 4), "TH6": (0, 1),
    "TH7": (0, 2), "TH8": (0, 0), "TH9": (0, 0), "VD1": (1, 1), "VD2": (0, 0), "VD3": (0, 1), "VD4": (1, 0),
    "VD5": (0, 0),
}


def dem_the():
    dem = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du" or k[2] == "extend":
            continue
        _, _, tier, dang, *_ = k
        ma = dang.split("+")
        for t in re.findall(r"\[(NB|TH|VD)\]", k[8]):
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
