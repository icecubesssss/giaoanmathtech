#!/usr/bin/env python3
"""Sơ đồ Phiếu 5 ch.VI 9C bản 2 (17/11/2026) — "Luyện tập chung, bài tập cuối chương VI".

Thầy 17/11 (phiên P5): BỎ HẲN phương trình chứa ẩn ở mẫu (C6-17) như P4 — kiến thức cũ đổi sang hằng đẳng thức
$(a+b)^2$ (bước HS vướng khi tính $x_1^2+x_2^2$); Giảng Võ → Phương Mai ý 1 (C6-05), Nguyễn Trường Tộ → Thịnh Quang
(C6-06); thêm 2 câu NB trắc nghiệm (Lê Ngọc Hân GK2 2024, Đại Áng CK2) đi ngay sau ví dụ năng suất, chuyển động
(vi_du_gate cấm hai ví dụ liền nhau). Mã câu = chon-cau.json (P5), dang_id ↔ dòng TM phiếu 5.

Claude CHỐT ĐỀ từng bài (nguyên văn đề gốc + ý ngắn, luật 17/11 [[cau-hoi-muc-tieu-output]]), thẻ, đáp số (SymPy ở đây).
Gemini chỉ viết lời giải, ví dụ điền khuyết, mở đầu / nhắc lại / ghi chú GV (viec_dung_p5_ch6_9c.py).

    .venv/bin/python scripts/gemini/so_do_p5_ch6_9c.py      # kiểm đáp số + đếm thẻ theo dang_id

Bố cục: LT1 = phương trình bậc hai + Viète (khởi động, Mạch 1 chứng minh có nghiệm + biểu thức đối xứng) ·
LT2 = Mạch 2 lập phương trình (năng suất, chuyển động, lãi suất), Mạch 3 tìm m theo hệ thức (ĐÍCH = Bài 10, đề HK2
Phòng GD&ĐT Hà Đông 2024–2025). BTVN Bài 11–20: NB/TH phương trình, Viète → lập phương trình → VD tìm m.
"""
from __future__ import annotations

import collections
import re
import sys

import sympy as sp

x, m = sp.symbols("x m")
R = sp.Rational
BR = "[[br]]"


def y(*ds):
    return BR + BR.join(ds)


def heso(trai):
    p = sp.Poly(sp.expand(sp.sympify(trai, locals={"m": m, "R": R})), x)
    return [p.coeff_monomial(x**k) for k in (2, 1, 0)]


def kiem():
    loi = []

    def bang(ten, that, mong):
        if sp.simplify(sp.sympify(that) - sp.sympify(mong)) != 0:
            loi.append(f"{ten}: máy ra {sp.simplify(that)}, sơ đồ ghi {mong}")

    def D(ten, trai, mong):
        a, b, c = heso(trai)
        bang(ten + " Δ", sp.expand(b**2 - 4 * a * c), mong)

    def SP(ten, trai, s, p):
        a, b, c = heso(trai)
        bang(ten + " tổng", -b / a, s)
        bang(ten + " tích", c / a, p)

    def nghiem(ten, trai, mong):
        r = sp.solve(sp.expand(sp.sympify(trai)), x)
        if sorted(map(sp.nsimplify, r), key=sp.default_sort_key) != sorted(map(sp.nsimplify, mong), key=sp.default_sort_key):
            loi.append(f"{ten}: nghiệm máy {r}, sơ đồ {mong}")

    def gt(ten, trai, bt, mong):
        """Giá trị biểu thức của hai nghiệm THẬT (bt theo X1, X2)."""
        r = sp.solve(sp.expand(sp.sympify(trai)), x)
        X1, X2 = sp.symbols("X1 X2")
        v = sp.nsimplify(sp.simplify(sp.sympify(bt).subs({X1: r[0], X2: r[1]})))
        bang(ten, v, mong)

    def tim_m(ten, trai, he_thuc, mong, dk_them=lambda v: True):
        """he_thuc theo X1, X2 (=0). Giải đúng trên nghiệm thật (cả hai thứ tự), lọc Δ>0."""
        a, b, c = heso(trai)
        X1, X2 = sp.symbols("X1 X2")
        S, P = -b / a, c / a
        e = sp.sympify(he_thuc)
        # biểu thức đối xứng ⇒ thay theo S, P
        s1, p1 = sp.symbols("s1 p1")
        e_sp = sp.simplify(e.subs({X1: (s1 + sp.sqrt(s1**2 - 4 * p1)) / 2, X2: (s1 - sp.sqrt(s1**2 - 4 * p1)) / 2}))
        e_sp = sp.simplify(e_sp.subs({s1: S, p1: P}))
        ung = [v for v in sp.solve(sp.numer(sp.together(e_sp)), m)
               if v.is_real and sp.expand(b**2 - 4 * a * c).subs(m, v) > 0 and dk_them(v)]
        if sorted(map(sp.nsimplify, ung)) != sorted(map(sp.nsimplify, mong)):
            loi.append(f"{ten}: m máy {ung}, sơ đồ {mong}")

    def pt(ten, trai, phai, dk, mong, bac2=None):
        """Phương trình lập được (có thể có ẩn ở mẫu) → nghiệm nhận theo điều kiện của ẩn."""
        e = sp.sympify(trai, locals={"R": R}) - sp.sympify(phai, locals={"R": R})
        mau = sp.Integer(1)
        for t in sp.Add.make_args(sp.expand(e, deep=False)):
            mau = sp.lcm(mau, sp.denom(sp.together(t)))
        tu = sp.expand(sp.cancel(e * mau))
        if bac2 is not None and not sp.simplify(tu / sp.expand(sp.sympify(bac2))).is_number:
            loi.append(f"{ten}: PT thu gọn máy {sp.factor(tu)}, sơ đồ {bac2}")
        moi = [r for r in sp.solve(tu, x) if r.is_real and mau.subs(x, r) != 0 and dk(r)]
        if sorted(moi) != sorted(map(sp.nsimplify, mong)):
            loi.append(f"{ten}: nghiệm nhận máy {moi}, sơ đồ {mong}")

    duong = lambda r: r > 0
    tn = lambda r: r > 0 and r == int(r)
    # ── LT1 ──
    nghiem("B1 (1)", "2*x**2-5*x+3", [1, R(3, 2)])
    D("B1 (2)", "x**2-5*x-4", 41)
    nghiem("B1 (2)", "x**2-5*x-4", [(5 + sp.sqrt(41)) / 2, (5 - sp.sqrt(41)) / 2])
    SP("B2 6.42", "x**2-38*x+325", 38, 325)
    nghiem("B2 6.42", "x**2-38*x+325", [13, 25])
    D("VD1 Đống Đa", "3*x**2-5*x+1", 13)
    gt("VD1 M", "3*x**2-5*x+1", "X1**2+X2**2-6*X1*X2", R(1, 9))
    D("B4 Phương Mai", "x**2-2*(m+1)*x+m-4", "4*m**2+4*m+20")
    bang("B4 (2m+1)²+19", "(2*m+1)**2+19", "4*m**2+4*m+20")
    D("B5 Đức Giang", "x**2-2*(m+1)*x+m**2+2", "8*m-4")
    gt("B5 A (m=2)", "x**2-6*x+6", "X1/X2+X2/X1", 4)
    # ── LT2 ──
    pt("VD2 Phúc Đồng", "400/x-400/(x+20)", 1, tn, [80], "x**2+20*x-8000")
    pt("B6 Lê Ngọc Hân (chỉ một bước)", "1100/x-1100/(x+5)", 2, tn, [50], "x**2+5*x-2750")
    pt("VD3 Cầu Diễn", "90/x+R(1,2)+90/(x+9)", 5, duong, [36], "x**2-31*x-180")
    pt("B7 Đại Áng (chỉ một bước)", "80/x-80/(x+10)", R(24, 60), duong, [40], "x**2+10*x-2000")
    pt("B8 6.44 (x là chiều dài)", "x*(10-x)", 24, lambda r: 5 <= r < 10, [6], "x**2-10*x+24")
    pt("VD4 lãi kép", "100*(1+x)**2", R(11881, 100), duong, [R(9, 100)], "10000*x**2+20000*x-1881")
    pt("B9 6.51", "100*(1+x)**2+50*(1+x)", 176, duong, [R(1, 10)], "50*x**2+125*x-13")
    D("B9 Δ", "50*x**2+125*x-13", 18225)
    nghiem("VD5a m=3", "x**2-2*(3-2)*x+9-15", [1 + sp.sqrt(7), 1 - sp.sqrt(7)])
    D("VD5b Δ", "x**2-2*(m-2)*x+m**2-5*m", "4*m+16")
    tim_m("VD5b", "x**2-2*(m-2)*x+m**2-5*m", "X1**2+X2**2-X1*X2-46", [6])
    SP("B10 ĐÍCH", "x**2+(m+1)*x-3", "-(m+1)", -3)
    tim_m("B10 ĐÍCH", "x**2+(m+1)*x-3", "1/X1+1/X2-2", [5])
    # ── BTVN ──
    bang("B11 dạng chuẩn", "2*x*(x+3)-x**2+9", "x**2+6*x+9")
    nghiem("B11", "x**2+6*x+9", [-3])
    a_tq = sp.solve(sp.sympify("2*(x-1)**2+2*x-a").subs(x, (1 + sp.sqrt(7)) / 2), sp.Symbol("a"))[0]
    bang("B12 a", a_tq, 5)
    nghiem("B12", "2*x**2-2*x-3", [(1 + sp.sqrt(7)) / 2, (1 - sp.sqrt(7)) / 2])
    a13 = (3 - sp.sqrt(6)) + 3 / (3 - sp.sqrt(6))
    bang("B13 a", a13, 6)
    bang("B13 x2", sp.radsimp(3 / (3 - sp.sqrt(6))), 3 + sp.sqrt(6))
    gt("B13", "x**2-6*x+3", "1/X1**2+1/X2**2", R(10, 3))
    SP("B14 Nguyễn Du", "x**2+4*x-3", -4, -3)
    bang("B14 m", sp.solve(sp.sympify("22-m*(-4)"), m)[0], R(-11, 2))
    pt("B15 trồng cây", "30/x-40/(x+5)", R(20, 60), tn, [10], "x**2+35*x-450")
    pt("B16 Nhật Tân", "60/(x-3)-60/x", 1, lambda r: tn(r) and r > 3, [15], "x**2-3*x-180")
    pt("B17 Nghĩa Tân", "90/x-100/(x+10)", R(15, 60), duong, [40], "x**2+50*x-3600")
    pt("B18 6.52", "1/x+1/(x+1)", 1 / (1 + R(12, 60)), lambda r: r > R(6, 5), [2], "5*x**2-7*x-6")
    SP("B19 Nghĩa Tân III", "x**2-m*x-4", "m", -4)
    tim_m("B19", "x**2-m*x-4", "X1**2+X2**2-9", [1], lambda v: v > 0)
    D("B20 Tây Mỗ", "x**2-3*x+m-2", "17-4*m")
    tim_m("B20", "x**2-3*x+m-2", "X1**2+X2**2-3*X1*X2+1", [4])
    return loi


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
DD = r"đề minh họa tuyển sinh lớp 10, Phòng GD\&ĐT Đống Đa, "
N = {
    "cau-dien-gk2": r"GK2 THCS Cầu Diễn, 2025--2026", "sgk-6.42": r"SGK Toán 9 tập hai, Bài tập 6.42",
    "dd18": DD + r"đề 18, 2025--2026", "pm11": DD + r"đề 11 (THCS Phương Mai), 2025--2026",
    "duc-giang": r"GK2 THCS Đức Giang, 2025--2026", "phuc-dong-ck1": r"HK1 THCS Phúc Đồng, 2025--2026",
    "lnh-gk2": r"GK2 THCS Lê Ngọc Hân, 2024--2025", "cau-dien-ck2": r"HK2 THCS Cầu Diễn, 2025--2026",
    "dai-ang": r"HK2 THCS Đại Áng, 2025--2026", "sgk-6.44": r"SGK Toán 9 tập hai, Bài tập 6.44",
    "sgk-hd": r"SGK Toán 9 tập hai, Bài 21, HĐ1--HĐ3", "sgk-6.51": r"SGK Toán 9 tập hai, Bài tập 6.51",
    "lhp": r"HK2 THCS Lê Hồng Phong (Hà Đông), 2025--2026", "ha-dong": r"HK2 Phòng GD\&ĐT Hà Đông, 2024--2025",
    "ngo-sy-lien": r"GK1 THCS Ngô Sỹ Liên, 2024--2025", "tq16": DD + r"đề 16 (THCS Thịnh Quang), 2025--2026",
    "ld23": r"đề luyện thi vào 10 số 23, Mathtech, 2025--2026", "nguyen-du-ck2": r"HK2 THCS Nguyễn Du, 2025--2026",
    "phuc-dong-ck2": r"HK2 THCS Phúc Đồng, 2024--2025", "nhat-tan": r"GK2 THCS Nhật Tân, 2024--2025",
    "nghia-tan": r"GK2 THCS Nghĩa Tân, 2024--2025", "sgk-6.52": r"SGK Toán 9 tập hai, Bài tập 6.52",
    "tay-mo": r"GK2 THCS Tây Mỗ 3, 2025--2026",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


TH_CUOI = r"[TH] Lập phương trình, giải phương trình và trả lời."
AC = r"[NB] Tính tích $ac$ rồi kết luận số nghiệm của phương trình."

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (đã có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN NGUYÊN VĂN, GHI đáp số cho thợ).
KHOI = [
    # ───────────── LUYỆN TẬP 1 — phương trình bậc hai, định lí Viète ─────────────
    # 17/11 dan_dat_gate: trắc nghiệm đứng TRƯỚC bài tự trình bày trong cùng mạch ⇒ 6.42 là Bài 1
    ("Bài 1.", "practice1", "onclass", "NB4", 1, "sgk-6.42", "", "trac_nghiem",
     r"[NB] Phương trình bậc hai có hai nghiệm $x_1=13$ và $x_2=25$ là" + ng("sgk-6.42"),
     "x₁+x₂=38, x₁x₂=325 nên hai số là nghiệm của x²−38x+325=0. Chọn C. Lời giải 1–2 dòng."),
    ("Bài 2.", "practice1", "onclass", "NB3", 1, "gk2-cau-dien-2025-31", "", "nb_cau",
     r"Giải các phương trình $2x^2-5x+3=0$ (1) và $x^2-5x-4=0$ (2)." + ng("cau-dien-gk2")
     + y(r"a) [NB] Phương trình (1) có $a+b+c=0$. Viết hai nghiệm của phương trình (1).",
         r"b) [NB] Tính $\Delta$ của phương trình (2).",
         r"c) [NB] Viết hai nghiệm của phương trình (2)."),
     "a) a+b+c=2−5+3=0 nên x₁=1, x₂=c/a=3/2 (một dòng). b) Δ=(−5)²−4·1·(−4)=25+16=41. c) Δ=41>0 nên "
     "x₁=(5+√41)/2, x₂=(5−√41)/2."),
    ("Mạch 1. Chứng minh phương trình có hai nghiệm phân biệt, biểu thức đối xứng", "practice1", "heading"),
    # NB kiến thức cũ (TM dòng 1): hằng đẳng thức lớp 8 — bước biến đổi của Bài 5 (Đức Giang) và mọi bài x₁² + x₂²
    ("Bài 3.", "practice1", "onclass", "NB1", 1, "gk2-duc-giang-2025-III2 (bước khai triển)", "", "trac_nghiem",
     r"[NB] Khai triển $(x_1+x_2)^2$, ta được" + r" \textit{(hằng đẳng thức đáng nhớ, Toán 8)}",
     "Kiến thức cũ, MỘT bước: (x₁+x₂)²=x₁²+2x₁x₂+x₂². Chọn B. Lời giải 1 dòng."),
    ("Ví dụ 1.", "practice1", "", "", 0, "v10-dong-da-de18-2025-III3", "", "vi_du",
     r"Cho phương trình $3x^2-5x+1=0$. Chứng minh phương trình luôn có $2$ nghiệm phân biệt $x_1$, $x_2$. Tính giá "
     r"trị biểu thức $M=x_1^2+x_2^2-6x_1x_2$." + ng("dd18"),
     "a=3, b=−5, c=1 · Δ=(−5)²−4·3·1=25−12=13>0 nên phương trình có hai nghiệm phân biệt x₁, x₂ · theo định lí Viète "
     "x₁+x₂=5/3, x₁x₂=1/3 · M=(x₁²+x₂²)−6x₁x₂=(x₁+x₂)²−2x₁x₂−6x₁x₂=(x₁+x₂)²−8x₁x₂ · M=(5/3)²−8·(1/3)=25/9−24/9=1/9 · "
     "Vậy M=1/9. 7–9 ô."),
    ("Bài 4.", "practice1", "onclass", "NB8+TH4", 2, "v10-phuong-mai-2025-III3", "1", "th_dan",
     r"Cho phương trình: $x^2-2(m+1)x+m-4=0$. Chứng minh rằng phương trình luôn có hai nghiệm phân biệt với mọi $m$."
     + ng("pm11")
     + y(r"a) [NB] Chỉ ra các hệ số $a$, $b$, $c$ của phương trình.",
         r"b) [NB] Tính $\Delta$ theo $m$.",
         r"c) [TH] Viết $\Delta$ dưới dạng $(2m+1)^2+k$ với $k$ là một số, rồi kết luận."),
     "a) a=1, b=−2(m+1), c=m−4. b) Δ=[−2(m+1)]²−4·1·(m−4)=4(m+1)²−4(m−4)=4m²+8m+4−4m+16=4m²+4m+20. "
     "c) Theo câu b): Δ=4m²+4m+1+19=(2m+1)²+19 · (2m+1)²≥0 với mọi m nên Δ≥19>0 · Vậy phương trình luôn có hai nghiệm "
     "phân biệt với mọi m."),
    ("Bài 5.", "practice1", "onclass", "NB6+TH3", 2, "gk2-duc-giang-2025-III2", "a-b", "th_dan",
     r"Cho phương trình: $x^2-2(m+1)x+m^2+2=0$ (với $m$ là tham số)." + ng("duc-giang")
     + y(r"a) [NB] Tính $\Delta$ theo $m$.",
         r"b) [TH] Tìm điều kiện của $m$ để phương trình có hai nghiệm phân biệt.",
         r"c) [TH] Với $m=2$, không giải phương trình, tính giá trị biểu thức $A=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$."),
     "a) Δ=4(m+1)²−4(m²+2)=4m²+8m+4−4m²−8=8m−4. b) Theo câu a): phương trình có hai nghiệm phân biệt khi Δ>0 · "
     "8m−4>0 · m>1/2 · Vậy m>1/2. c) Với m=2 (thỏa mãn m>1/2) phương trình là x²−6x+6=0 · theo định lí Viète "
     "x₁+x₂=6, x₁x₂=6 · A=(x₁²+x₂²)/(x₁x₂)=[(x₁+x₂)²−2x₁x₂]/(x₁x₂) · A=(36−12)/6=24/6=4 · Vậy A=4."),
    # ───────────── LUYỆN TẬP 2 — lập phương trình, tìm m theo hệ thức ─────────────
    ("Mạch 2. Giải bài toán bằng cách lập phương trình", "practice2", "heading"),
    ("Ví dụ 2.", "practice2", "", "", 0, "ck1-phuc-dong-2025-III1-md903", "", "vi_du",
     r"Một tổ sản xuất kế hoạch làm $400$ sản phẩm cùng loại trong một số ngày quy định. Thực tế, mỗi ngày tổ làm được "
     r"nhiều hơn $20$ sản phẩm so với số sản phẩm dự định làm trong một ngày theo kế hoạch. Vì thế tổ đã hoàn thành công "
     r"việc sớm hơn kế hoạch $1$ ngày. Hỏi theo kế hoạch, mỗi ngày tổ sản xuất phải làm bao nhiêu sản phẩm? (Giả định "
     r"rằng số sản phẩm mà tổ đó làm được mỗi ngày là bằng nhau)." + ng("phuc-dong-ck1"),
     "Gọi x (sản phẩm) là số sản phẩm tổ phải làm mỗi ngày theo kế hoạch, x∈ℕ* · số ngày theo kế hoạch 400/x · thực "
     "tế mỗi ngày làm x+20 sản phẩm, số ngày 400/(x+20) · sớm hơn 1 ngày nên 400/x−400/(x+20)=1 · khử mẫu (mẫu chung "
     "x(x+20)): 400(x+20)−400x=x(x+20), x²+20x−8000=0 · Δ=400+32000=32400, √Δ=180 · x₁=80, x₂=−100 · x₁=80 thỏa mãn "
     "điều kiện, x₂=−100 không thỏa mãn · Vậy theo kế hoạch mỗi ngày tổ làm 80 sản phẩm. 7–9 ô."),
    ("Bài 6.", "practice2", "onclass", "NB2", 1, "gk2-le-ngoc-han-2024-III1 (bước biểu diễn)", "", "trac_nghiem",
     r"[NB] Một phân xưởng theo kế hoạch cần phải sản xuất $1\,100$ sản phẩm trong một số ngày quy định. Do mỗi ngày "
     r"phân xưởng đó sản xuất vượt mức $5$ sản phẩm nên đã hoàn thành kế hoạch sớm hơn thời gian quy định $2$ ngày. Gọi "
     r"số sản phẩm phân xưởng sản xuất mỗi ngày theo kế hoạch là $x$ ($x\in\mathbb N^*$). Số ngày phân xưởng làm xong "
     r"$1\,100$ sản phẩm trong thực tế là" + ng("lnh-gk2"),
     "MỘT bước: thực tế mỗi ngày làm x+5 sản phẩm nên số ngày là 1100/(x+5). Chọn B. Lời giải 1–2 dòng (không giải "
     "tiếp)."),
    ("Ví dụ 3.", "practice2", "", "", 0, "ck2-cau-dien-2025-III1", "", "vi_du",
     r"Quãng đường từ A đến B dài $90$ km. Một người đi xe máy từ A đến B. Khi đến B, người đó nghỉ $30$ phút rồi quay "
     r"trở về A với vận tốc lớn hơn vận tốc lúc đi là $9$ km/h. Thời gian kể từ lúc bắt đầu đi từ A đến lúc trở về A là "
     r"$5$ giờ. Tính vận tốc xe máy lúc đi từ A đến B." + ng("cau-dien-ck2"),
     "Gọi x (km/h) là vận tốc lúc đi, x>0 · 30 phút = 1/2 giờ · thời gian đi 90/x (giờ) · vận tốc về x+9, thời gian về "
     "90/(x+9) (giờ) · ta có phương trình 90/x+1/2+90/(x+9)=5 · 90/x+90/(x+9)=9/2 · khử mẫu (mẫu chung 2x(x+9)): "
     "180(x+9)+180x=9x(x+9) · 9x²−279x−1620=0, chia 9: x²−31x−180=0 · Δ=961+720=1681, √Δ=41 · x₁=36, x₂=−5 · "
     "x₁=36 thỏa mãn, x₂=−5 không thỏa mãn · Vậy vận tốc lúc đi là 36 km/h. 7–9 ô."),
    ("Bài 7.", "practice2", "onclass", "NB2", 1, "ck2-dai-ang-2025-III1 (bước lập phương trình)", "", "trac_nghiem",
     r"[NB] Hai xe khởi hành cùng một lúc từ A để đi đến B. Vận tốc của xe thứ nhất lớn hơn vận tốc của xe thứ hai là "
     r"$10$ km/h nên xe thứ nhất đến B sớm hơn xe thứ hai là $24$ phút. Biết độ dài quãng đường AB là $80$ km. Gọi vận "
     r"tốc của xe thứ hai là $x$ (km/h, $x>0$), khi đó thời gian xe thứ hai và xe thứ nhất đi hết quãng đường AB lần "
     r"lượt là $\dfrac{80}{x}$ (giờ) và $\dfrac{80}{x+10}$ (giờ). Phương trình lập được là" + ng("dai-ang"),
     "MỘT bước: 24 phút = 2/5 giờ, xe thứ hai đi lâu hơn nên 80/x−80/(x+10)=2/5. Chọn A. Lời giải 1–2 dòng (không "
     "giải tiếp)."),
    ("Bài 8.", "practice2", "onclass", "NB2", 1, "sgk-6.44", "", "trac_nghiem",
     r"[NB] Chiều dài và chiều rộng của hình chữ nhật có chu vi $20$ cm và diện tích $24\ \text{cm}^2$ là"
     + ng("sgk-6.44"),
     "Nửa chu vi 10 cm, tích 24 · chỉ phương án 6 cm và 4 cm có tổng 10, tích 24. Chọn B. Lời giải 1–2 dòng."),
    ("Ví dụ 4.", "practice2", "", "", 0, "sgk-b21-hd1", "HĐ1-HĐ3", "vi_du",
     r"Bác Lan gửi tiết kiệm $100$ triệu đồng vào ngân hàng với kì hạn $12$ tháng theo thể thức lãi kép. Sau năm thứ "
     r"nhất, do chưa có nhu cầu sử dụng nên bác Lan không rút tiền ra mà tiếp tục gửi $12$ tháng nữa, với lãi suất như "
     r"cũ. Sau hai năm bác Lan rút tiền ra thì nhận được $118{,}81$ triệu đồng cả vốn lẫn lãi. Hỏi lãi suất gửi tiết "
     r"kiệm là bao nhiêu?" + ng("sgk-hd"),
     "ĐỌC ẢNH SGK tr.25 (HĐ1–HĐ3). Gọi x là lãi suất (x viết dưới dạng số thập phân, x>0) · sau kì thứ nhất: "
     "100+100x=100(1+x) (triệu đồng) · sau kì thứ hai: 100(1+x)+100(1+x)·x=100(1+x)² (triệu đồng) · ta có phương "
     "trình 100(1+x)²=118,81 · (1+x)²=1,1881 · 1+x>0 nên 1+x=1,09 · x=0,09 thỏa mãn điều kiện · Vậy lãi suất gửi tiết "
     "kiệm là 9% một năm. 7–9 ô."),
    ("Bài 9.", "practice2", "onclass", "NB7+TH2", 2, "sgk-6.51", "", "th_dan",
     r"Bác Hương gửi tiết kiệm ngân hàng $100$ triệu đồng với kì hạn $12$ tháng. Sau một năm, do chưa có nhu cầu sử "
     r"dụng nên bác chưa rút sổ tiết kiệm này ra mà gửi tiếp và gửi thêm một sổ tiết kiệm mới với số tiền $50$ triệu "
     r"đồng, cũng với kì hạn $12$ tháng. Sau hai năm (kể từ khi gửi lần đầu), bác Hương nhận được số tiền cả vốn lẫn "
     r"lãi là $176$ triệu đồng. Tính lãi suất năm của hình thức gửi tiết kiệm này (giả sử lãi suất không đổi trong suốt "
     r"quá trình gửi)." + ng("sgk-6.51")
     + y(r"a) [NB] Gọi lãi suất năm là $x$ ($x$ viết dưới dạng số thập phân, $x>0$). Viết số tiền cả vốn lẫn lãi của "
         r"sổ $100$ triệu đồng sau một năm theo $x$.",
         r"b) [NB] Viết số tiền cả vốn lẫn lãi của sổ $100$ triệu đồng sau hai năm theo $x$.",
         r"c) [NB] Viết số tiền cả vốn lẫn lãi của sổ $50$ triệu đồng khi bác Hương rút tiền theo $x$.",
         "d) " + TH_CUOI),
     "a) 100(1+x) (triệu đồng). b) 100(1+x)² (triệu đồng). c) sổ 50 triệu gửi được một năm: 50(1+x) (triệu đồng). "
     "d) Theo câu b) và c): 100(1+x)²+50(1+x)=176 · 100x²+200x+100+50+50x=176 · 100x²+250x−26=0, chia 2: "
     "50x²+125x−13=0 · Δ=125²−4·50·(−13)=15625+2600=18225, √Δ=135 · x₁=(−125+135)/100=0,1, x₂=(−125−135)/100=−2,6 · "
     "x₁=0,1 thỏa mãn, x₂=−2,6 không thỏa mãn · Vậy lãi suất là 10% một năm."),
    ("Mạch 3. Tìm $m$ theo hệ thức giữa hai nghiệm", "practice2", "heading"),
    ("Ví dụ 5.", "practice2", "", "", 0, "ck2-le-hong-phong-2025-IV", "a-b", "vi_du",
     r"Cho phương trình: $x^2-2(m-2)x+m^2-5m=0$.[[br]]a) Giải phương trình với $m=3$.[[br]]b) Tìm $m$ để phương trình "
     r"có hai nghiệm phân biệt $x_1$, $x_2$ thỏa mãn: $x_1^2+x_2^2=x_1x_2+46$." + ng("lhp"),
     "a) m=3: x²−2x−6=0 · Δ=4+24=28, √Δ=2√7 · x₁=1+√7, x₂=1−√7. b) Δ=4(m−2)²−4(m²−5m)=4m+16 · hai nghiệm phân biệt "
     "khi 4m+16>0, m>−4 · Viète: x₁+x₂=2m−4, x₁x₂=m²−5m · x₁²+x₂²=x₁x₂+46 nên (x₁+x₂)²−3x₁x₂=46 · "
     "(2m−4)²−3(m²−5m)=46 · m²−m−30=0 · m₁=6, m₂=−5 · m₁=6 thỏa mãn m>−4, m₂=−5 không thỏa mãn · Vậy m=6. "
     "Hai ý, mỗi ý 3–4 ô."),
    ("Bài 10.", "practice2", "onclass", "NB5+VD1", 3, "ck2-ha-dong-2024-III2", "a-b", "vd_de",
     r"Cho phương trình $x^2+(m+1)x-3=0$. Chứng tỏ rằng phương trình luôn có $2$ nghiệm phân biệt với mọi giá trị của "
     r"$m$. Gọi $x_1$, $x_2$ là nghiệm của phương trình trên. Tìm giá trị của $m$ để $\dfrac{1}{x_1}+\dfrac{1}{x_2}=2$."
     + ng("ha-dong")
     + y("a) " + AC, r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.", r"c) [VD] Tìm $m$."),
     "BÀI ĐÍCH. a) ac=1·(−3)=−3<0 nên phương trình luôn có hai nghiệm phân biệt với mọi m. b) x₁+x₂=−(m+1), x₁x₂=−3. "
     "c) (chỉ đề) Theo câu b): x₁x₂=−3≠0 · 1/x₁+1/x₂=(x₁+x₂)/(x₁x₂)=(m+1)/3 · (m+1)/3=2 · m=5 · Vậy m=5."),
    # ───────────── BTVN — Bài 11–20 ─────────────
    ("Bài 11.", "reflection", "btvn", "NB11+TH6", 2, "gk1-ngo-sy-lien-2024-I1a", "", "th_dan",
     r"Giải phương trình: $2x(x+3)-x^2+9=0$." + ng("ngo-sy-lien")
     + y(r"a) [NB] Đưa phương trình về dạng $ax^2+bx+c=0$.",
         r"b) [NB] Viết vế trái của phương trình vừa tìm được dưới dạng bình phương của một biểu thức.",
         r"c) [TH] Tìm $x$."),
     "a) 2x²+6x−x²+9=0 · x²+6x+9=0. b) x²+6x+9=(x+3)². c) Theo câu b): (x+3)²=0 · x+3=0 · x=−3 · Vậy phương trình có "
     "nghiệm x=−3."),
    ("Bài 12.", "reflection", "btvn", "NB12+TH7", 2, "v10-thinh-quang-2025-III3", "", "th_dan",
     r"Cho phương trình $2(x-1)^2=-2x+a$ có $1$ nghiệm là $\dfrac{1+\sqrt7}{2}$. Tìm nghiệm còn lại." + ng("tq16")
     + y(r"a) [NB] Khai triển, chuyển vế để đưa phương trình về dạng có vế phải bằng $0$.",
         r"b) [NB] Viết tổng hai nghiệm $x_1+x_2$ theo định lí Viète.",
         r"c) [TH] Theo câu b), tính nghiệm còn lại."),
     "a) 2x²−4x+2+2x−a=0 · 2x²−2x+2−a=0. b) x₁+x₂=−(−2)/2=1. c) x₁=(1+√7)/2 · x₂=1−(1+√7)/2=(1−√7)/2 · Vậy nghiệm "
     "còn lại là (1−√7)/2. (Không cần tìm a; nếu tìm thì a=5, phương trình 2x²−2x−3=0 — KHÔNG ghi vào lời giải.)"),
    ("Bài 13.", "reflection", "btvn", "NB10+TH5", 2, "v10-luyen-de-23-2025-III3", "", "th_dan",
     r"Cho phương trình bậc hai: $x^2-ax+3=0$ có một nghiệm bằng $x=3-\sqrt6$. Tính tổng nghịch đảo bình phương hai "
     r"nghiệm của phương trình trên." + ng("ld23")
     + y(r"a) [NB] Viết tích hai nghiệm $x_1x_2$ theo định lí Viète.",
         r"b) [NB] Biết $x_1=3-\sqrt6$, tìm nghiệm còn lại $x_2$.",
         r"c) [TH] Tính $\dfrac{1}{x_1^2}+\dfrac{1}{x_2^2}$."),
     "a) x₁x₂=3. b) x₂=3/(3−√6)=3(3+√6)/((3−√6)(3+√6))=3(3+√6)/3=3+√6. c) x₁+x₂=6, x₁x₂=3 · "
     "x₁²+x₂²=(x₁+x₂)²−2x₁x₂=36−6=30 · 1/x₁²+1/x₂²=(x₁²+x₂²)/(x₁x₂)²=30/9=10/3 · Vậy tổng bằng 10/3."),
    ("Bài 14.", "reflection", "btvn", "NB9+TH1", 2, "ck2-nguyen-du-2025-III3", "", "th_dan",
     r"Biết rằng phương trình $x^2+4x-3=0$ có hai nghiệm $x_1$, $x_2$. Tìm tất cả giá trị của $m$ thỏa mãn "
     r"$x_2^2-mx_2=x_1(m-x_1)$." + ng("nguyen-du-ck2")
     + y(r"a) [NB] Tính $x_1+x_2$ và $x_1x_2$.",
         r"b) [NB] Chứng tỏ hệ thức đã cho tương đương với $x_1^2+x_2^2=m(x_1+x_2)$.",
         r"c) [TH] Tìm $m$."),
     "a) x₁+x₂=−4, x₁x₂=−3. b) x₂²−mx₂=mx₁−x₁² · x₁²+x₂²=mx₁+mx₂ · x₁²+x₂²=m(x₁+x₂). c) Theo câu a) và b): "
     "x₁²+x₂²=(x₁+x₂)²−2x₁x₂=16+6=22 · 22=−4m · m=−11/2 · Vậy m=−11/2."),
    ("Bài 15.", "reflection", "btvn", "NB7+TH2", 2, "ck2-phuc-dong-2024-901-III1", "", "th_dan",
     r"Hưởng ứng phong trào Tết trồng cây, chi đoàn thanh niên dự định trồng $30$ cây trong một thời gian nhất định. Do "
     r"mỗi giờ chi đoàn trồng nhiều hơn dự định $5$ cây nên đã hoàn thành công việc trước dự định $20$ phút và trồng "
     r"thêm được $10$ cây nữa. Tính số cây mà chi đoàn dự định trồng trong mỗi giờ." + ng("phuc-dong-ck2")
     + y(r"a) [NB] Đổi $20$ phút ra giờ.",
         r"b) [NB] Gọi số cây chi đoàn dự định trồng mỗi giờ là $x$ (cây, $x\in\mathbb N^*$). Viết thời gian dự định "
         r"trồng $30$ cây theo $x$.",
         r"c) [NB] Viết thời gian thực tế chi đoàn trồng $40$ cây theo $x$.", "d) " + TH_CUOI),
     "a) 1/3 giờ. b) 30/x (giờ). c) thực tế mỗi giờ trồng x+5 cây, trồng 30+10=40 cây: 40/(x+5) (giờ). d) Theo câu a), "
     "b), c): 30/x−40/(x+5)=1/3 · khử mẫu (mẫu chung 3x(x+5)): 90(x+5)−120x=x(x+5) · x²+35x−450=0 · "
     "Δ=1225+1800=3025, √Δ=55 · x₁=10, x₂=−45 · nhận x₁=10 · Vậy chi đoàn dự định trồng 10 cây mỗi giờ."),
    ("Bài 16.", "reflection", "btvn", "NB7+TH2", 2, "gk2-nhat-tan-2024-III2", "", "th_dan",
     r"Một đội xe dự định chở $60$ tấn hàng và dùng một số loại xe nhất định. Lúc sắp khởi hành có $3$ xe được điều đi "
     r"làm việc khác nên để chở được hết số hàng đã dự định, mỗi xe còn lại phải chở nhiều hơn $1$ tấn hàng. Tính số xe "
     r"lúc đầu của đội, biết rằng khối lượng hàng mỗi xe phải chở là như nhau." + ng("nhat-tan")
     + y(r"a) [NB] Gọi số xe lúc đầu của đội là $x$ (xe, $x\in\mathbb N$, $x>3$). Viết số tấn hàng mỗi xe phải chở theo "
         r"dự định theo $x$.",
         r"b) [NB] Viết số xe còn lại lúc khởi hành theo $x$.",
         r"c) [NB] Viết số tấn hàng mỗi xe còn lại phải chở theo $x$.", "d) " + TH_CUOI),
     "a) 60/x (tấn). b) x−3 (xe). c) 60/(x−3) (tấn). d) Theo câu a) và c): 60/(x−3)−60/x=1 · khử mẫu "
     "60x−60(x−3)=x(x−3) · x²−3x−180=0 · Δ=9+720=729, √Δ=27 · x₁=15, x₂=−12 · nhận x₁=15 · Vậy lúc đầu đội có 15 xe."),
    ("Bài 17.", "reflection", "btvn", "NB7+TH2", 2, "gk2-nghia-tan-2024-II", "", "th_dan",
     r"Một người đi xe máy từ A đến B trên quãng đường dài $90$ km. Lúc quay lại từ B về A, người đó đi một đường khác "
     r"dài $100$ km với vận tốc lớn hơn vận tốc lúc đi $10$ km/h. Tính vận tốc của người đó lúc đi từ A đến B, biết rằng "
     r"thời gian lúc về ít hơn thời gian lúc đi $15$ phút." + ng("nghia-tan")
     + y(r"a) [NB] Đổi $15$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc lúc đi là $x$ (km/h, $x>0$). Viết thời gian lúc đi theo $x$.",
         r"c) [NB] Viết thời gian lúc về theo $x$.", "d) " + TH_CUOI),
     "a) 1/4 giờ. b) 90/x (giờ). c) 100/(x+10) (giờ). d) Theo câu a), b), c): 90/x−100/(x+10)=1/4 · khử mẫu (mẫu "
     "chung 4x(x+10)): 360(x+10)−400x=x(x+10) · x²+50x−3600=0 · Δ=2500+14400=16900, √Δ=130 · x₁=40, x₂=−90 · nhận "
     "x₁=40 · Vậy vận tốc lúc đi là 40 km/h."),
    ("Bài 18.", "reflection", "btvn", "NB7+TH2", 2, "sgk-6.52", "", "th_dan",
     r"Hai khối học sinh lớp 8 và lớp 9 của một trường trung học cơ sở tham gia lao động. Nếu làm chung thì sẽ hoàn "
     r"thành công việc sau $1$ giờ $12$ phút. Nếu mỗi khối lớp làm riêng thì khối lớp 9 làm xong nhanh hơn khối lớp 8 "
     r"là $1$ giờ. Hỏi nếu mỗi khối lớp làm riêng thì sau bao lâu sẽ hoàn thành công việc?" + ng("sgk-6.52")
     + y(r"a) [NB] Đổi $1$ giờ $12$ phút ra giờ.",
         r"b) [NB] Gọi thời gian khối lớp 9 làm riêng xong công việc là $x$ (giờ, $x>\dfrac65$). Viết phần công việc "
         r"khối lớp 9 làm được trong $1$ giờ theo $x$.",
         r"c) [NB] Viết phần công việc khối lớp 8 làm được trong $1$ giờ theo $x$.", "d) " + TH_CUOI),
     "a) 6/5 giờ. b) 1/x (công việc). c) khối 8 làm riêng mất x+1 giờ nên làm được 1/(x+1) (công việc). d) Trong 1 giờ "
     "cả hai khối làm được 5/6 công việc · 1/x+1/(x+1)=5/6 · khử mẫu (mẫu chung 6x(x+1)): 6(x+1)+6x=5x(x+1) · "
     "5x²−7x−6=0 · Δ=49+120=169, √Δ=13 · x₁=2, x₂=−3/5 · nhận x₁=2 · Vậy khối lớp 9 làm riêng mất 2 giờ, khối lớp 8 "
     "mất 3 giờ."),
    ("Bài 19.", "reflection", "btvn", "NB5+VD1", 3, "gk2-nghia-tan-2024-III2", "a-b", "vd_de",
     r"Cho phương trình $x^2-mx-4=0$ (1). Chứng minh phương trình (1) luôn có hai nghiệm phân biệt với mọi $m$. Tìm tất "
     r"cả giá trị dương của $m$ để phương trình (1) có hai nghiệm phân biệt $x_1$, $x_2$ sao cho $x_1^2+x_2^2=9$."
     + ng("nghia-tan")
     + y("a) " + AC, r"b) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.",
         r"c) [NB] Viết $x_1^2+x_2^2$ theo $x_1+x_2$ và $x_1x_2$.", r"d) [VD] Tìm $m$."),
     "a) ac=1·(−4)=−4<0 nên phương trình (1) luôn có hai nghiệm phân biệt với mọi m. b) x₁+x₂=m, x₁x₂=−4. "
     "c) x₁²+x₂²=(x₁+x₂)²−2x₁x₂. d) (chỉ đề) Theo câu b) và c): x₁²+x₂²=m²+8 · m²+8=9 · m²=1 · m=1 hoặc m=−1 · m>0 "
     "nên m=1 · Vậy m=1."),
    ("Bài 20.", "reflection", "btvn", "NB5+VD1", 3, "gk2-tay-mo-3-2025-III2", "", "vd_de",
     r"Cho phương trình bậc hai $x^2-3x+m-2=0$ ($m$ là tham số). Tìm $m$ để phương trình có hai nghiệm phân biệt "
     r"$x_1$, $x_2$ thỏa mãn $x_1^2+x_2^2-3x_1x_2=-1$." + ng("tay-mo")
     + y(r"a) [NB] Tính $\Delta$.", r"b) [NB] Tìm điều kiện của $m$ để phương trình có hai nghiệm phân biệt.",
         r"c) [NB] Viết $x_1+x_2$ và $x_1x_2$ theo $m$.", r"d) [VD] Tìm $m$."),
     "a) Δ=9−4(m−2)=17−4m. b) Δ>0 · 17−4m>0 · m<17/4. c) x₁+x₂=3, x₁x₂=m−2. d) (chỉ đề) x₁²+x₂²−3x₁x₂"
     "=(x₁+x₂)²−5x₁x₂=9−5(m−2)=19−5m · 19−5m=−1 · m=4 · m=4 thỏa mãn m<17/4 · Vậy m=4."),
]

OPTIONS = {   # đáp án: Bài 1 C · Bài 3 B · Bài 6 B · Bài 7 A · Bài 8 B
    "Bài 1.": [r"$x^2-13x+25=0$", r"$x^2-25x+13=0$", r"$x^2-38x+325=0$", r"$x^2+38x+325=0$"],
    "Bài 3.": [r"$x_1^2+x_2^2$", r"$x_1^2+2x_1x_2+x_2^2$", r"$x_1^2-2x_1x_2+x_2^2$", r"$x_1^2+x_1x_2+x_2^2$"],
    "Bài 6.": [r"$\dfrac{1\,100}{x}$", r"$\dfrac{1\,100}{x+5}$", r"$\dfrac{1\,100}{x-5}$", r"$1\,100(x+5)$"],
    "Bài 7.": [r"$\dfrac{80}{x}-\dfrac{80}{x+10}=\dfrac25$", r"$\dfrac{80}{x+10}-\dfrac{80}{x}=\dfrac25$",
               r"$\dfrac{80}{x}-\dfrac{80}{x+10}=24$", r"$\dfrac{80}{x}+\dfrac{80}{x+10}=\dfrac25$"],
    "Bài 8.": [r"$5$ cm và $4$ cm", r"$6$ cm và $4$ cm", r"$8$ cm và $3$ cm", r"$10$ cm và $2$ cm"],
}

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 5 (17/11 bản bỏ C6-17)
    "NB1": (1, 0), "NB2": (3, 0), "NB3": (3, 0), "NB4": (1, 0), "NB5": (2, 6), "NB6": (1, 0), "NB7": (3, 12),
    "NB8": (2, 0), "NB9": (0, 2), "NB10": (0, 2), "NB11": (0, 2), "NB12": (0, 2),
    "TH1": (0, 1), "TH2": (1, 4), "TH3": (2, 0), "TH4": (1, 0), "TH5": (0, 1), "TH6": (0, 1), "TH7": (0, 1),
    "VD1": (1, 2),
}


def dem_the():
    dem = collections.Counter()
    for k in KHOI:
        if len(k) < 9 or k[7] == "vi_du":
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
