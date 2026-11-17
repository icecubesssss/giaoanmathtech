#!/usr/bin/env python3
"""Sơ đồ Phiếu 4 ch.VI 9C bản 2 (17/11/2026) — "Bài 21. Giải bài toán bằng cách lập phương trình".
17/11 lượt 3 (Thầy: phương trình chứa ẩn ở mẫu HS đã thạo, "ôn xong mấy câu dưới có dùng k") ⇒ bỏ hẳn phần ẩn ở mẫu;
kiến thức cũ chỉ còn bước khử mẫu (Bài 1). Thêm Nguyễn Du 2024, Ứng Hòa (trên lớp), Cát Linh, Tây Mỗ 3 (BTVN).

Claude CHỐT ĐỀ từng bài (in nguyên văn, luật 17/11 [[cau-hoi-muc-tieu-output]]), thẻ, dang_id (↔ dòng TM phiếu 4),
đáp số (SymPy kiểm ở đây: giải phương trình chứa ẩn ở mẫu, loại nghiệm theo ĐKXĐ / điều kiện của ẩn).
Gemini chỉ viết lời giải, ví dụ điền khuyết, lý thuyết (viec_dung_p4_ch6_9c.py). Mã câu = chon-cau.json (P4).

    .venv/bin/python scripts/gemini/so_do_p4_ch6_9c.py      # kiểm đáp số + đếm thẻ theo dang_id

Bố cục: LT1 = phương trình chứa ẩn ở mẫu (C6-17, NB1 kiến thức cũ ĐKXĐ đứng đầu) · LT2 = lập phương trình (C6-18)
theo mạch dạng toán: hình chữ nhật, năng suất, chuyển động, làm chung, hai giai đoạn (ĐÍCH = thi thử Tự Lập 2026).
Mỗi ví dụ đứng sát trước bài cùng kiểu (vi_du_gate). BTVN: ẩn ở mẫu → TH lập PT → VD.
17/11 đổi câu so với chọn câu ban đầu (đã sửa scripts/chon_cau_ch6_9c.py + TM): Mai Dịch → Quốc Oai (trùng số liệu
Ví dụ Cầu Diễn), Cầu Giấy → Sơn Đồng 2.2 (cùng PT x²+15x−2700=0 với Thái Thịnh), bể bơi → Nguyễn Bỉnh Khiêm (ví dụ
đi cùng Lômônôxốp), Thọ Lộc ↔ Quốc Oai (làm chung lên lớp đi sau ví dụ làm chung).
"""
from __future__ import annotations

import collections
import re
import sys

import sympy as sp

x = sp.Symbol("x")
R = sp.Rational
BR = "[[br]]"


def y(*ds):
    return BR + BR.join(ds)


def kiem():
    loi = []

    def bang(ten, that, mong):
        if sp.simplify(sp.sympify(that) - sp.sympify(mong)) != 0:
            loi.append(f"{ten}: máy ra {sp.simplify(that)}, sơ đồ ghi {mong}")

    def pt(ten, trai, phai, dk, mong, bac2=None):
        """Phương trình trai = phai (có thể chứa ẩn ở mẫu). dk: hàm lọc nghiệm (ĐKXĐ/điều kiện ẩn).
        mong: nghiệm nhận; bac2: phương trình bậc hai sau khử mẫu (chuỗi, =0), so sai khác hằng số."""
        e = sp.sympify(trai, locals={"R": R}) - sp.sympify(phai, locals={"R": R})
        mau = sp.Integer(1)
        for t in sp.Add.make_args(sp.expand(e, deep=False)):
            mau = sp.lcm(mau, sp.denom(sp.together(t)))
        tu = sp.expand(sp.cancel(e * mau))
        if bac2 is not None:
            q = sp.simplify(tu / sp.expand(sp.sympify(bac2)))
            if not q.is_number:
                loi.append(f"{ten}: PT sau khử mẫu máy {sp.factor(tu)}, sơ đồ {bac2}")
        moi = [r for r in sp.solve(tu, x) if r.is_real and mau.subs(x, r) != 0 and dk(r)]
        if sorted(moi) != sorted(map(sp.nsimplify, mong)):
            loi.append(f"{ten}: nghiệm nhận máy {moi}, sơ đồ {mong}")

    duong = lambda r: r > 0
    tn = lambda r: r > 0 and r == int(r)
    tat = lambda r: True
    pt("B1 khử mẫu", "240/x-240/(x+10)", 2, tn, [30], "x**2+10*x-1200")
    # ── LT2: lập phương trình ──
    pt("VD3 sân bóng", "x*(x+30)", 1800, duong, [30], "x**2+30*x-1800")
    pt("B4 vườn", "x*(x+6)", 280, duong, [14], "x**2+6*x-280")
    pt("VD4 in sách", "2000/x-2000/(x+100)", 1, tn, [400], "x**2+100*x-200000")
    pt("B5 Sở HN", "300/x-300/(x+10)", 1, tn, [50], "x**2+10*x-3000")
    pt("VD5 đội xe", "120/(x-2)-120/x", 3, lambda r: tn(r) and r > 2, [10], "x**2-2*x-80")
    pt("B6 Ba Đình", "60/(x-2)-60/x", 1, lambda r: tn(r) and r > 2, [12], "x**2-2*x-120")
    pt("VD6 tàu", "36/(x+3)+36/(x-3)+R(1,2)", R(11, 2), lambda r: r > 3, [15], "5*x**2-72*x-45")
    pt("B7 ca nô", "30/(x+4)+30/(x-4)", 4, lambda r: r > 4, [16], "x**2-15*x-16")
    pt("B8 máy bay", "1200/x+R(96,60)+1200/(x+100)", 6, duong, [500], "11*x**2-4900*x-300000")
    pt("VD7 hai ô tô", "108/x-108/(x+6)", R(12, 60), duong, [54], "x**2+6*x-3240")
    pt("B7 Nguyễn Du 2024", "120/x-120/(x+20)", R(1, 2), duong, [60], "x**2+20*x-4800")
    pt("B9 Lômônôxốp", "100/x-100/(x+10)", R(30, 60), duong, [40], "x**2+10*x-2000")
    pt("VD8 làm chung", "1/x+1/(x+6)", R(1, 4), lambda r: r > 4, [6], "x**2-2*x-24")
    pt("B10 hai vòi", "1/x+1/(x+4)", 1 / (2 + R(40, 60)), lambda r: r > R(8, 3), [4], "3*x**2-4*x-32")
    pt("B9 Ứng Hòa", "1/x+1/(x+3)", 1 / (3 + R(36, 60)), lambda r: r > R(18, 5), [6], "5*x**2-21*x-54")
    pt("VD9 LNH", "1+R(10,60)+(120-x)/(x+6)", "120/x", lambda r: 0 < r < 120, [48], "x**2+42*x-4320")
    pt("B11 ĐÍCH Tự Lập", "3/x+R(3,60)+9/(x+6)", "12/x", duong, [30], "x**2+6*x-1080")
    bang("B11 tăng tốc", 30 + 6, 36)
    # ── BTVN ──
    pt("B14 vật phóng", "R(196,10)*x-R(49,10)*x**2", 0, duong, [4], "x**2-4*x")
    pt("B15 mảnh đất", "(x+3)*(360/x-4)", 360, lambda r: 0 < r < 90, [15], "x**2+3*x-270")
    pt("B14 Cát Linh", "x*(x+11)", 180, duong, [9], "x**2+11*x-180")
    pt("B16 Sơn Đồng 2.2", "600/x-600/(x+30)", 1, tn, [120], "x**2+30*x-18000")
    pt("B17 Phương Mai", "144/(x-3)-144/x", 4, lambda r: tn(r) and r > 3, [12], "x**2-3*x-108")
    pt("B18 Thái Thịnh CK2", "90/x-90/(x+15)", R(1, 2), duong, [45], "x**2+15*x-2700")
    pt("B19 xe đạp", "36/x-36/(x+3)", R(36, 60), duong, [12], "x**2+3*x-180")
    pt("B19 Tây Mỗ", "150/x-150/(x+25)", 1, duong, [50], "x**2+25*x-3750")
    pt("B20 Thọ Lộc", "480/x-60/x-420/(x+5)", 2, tn, [30], "x**2+5*x-1050")
    pt("B21 Khương Thượng", "180/x-180/(x+5)", R(24, 60), duong, [45], "x**2+5*x-2250")
    return loi


# ── NGUỒN in sau đề ───────────────────────────────────────────────────────────
DD = r"đề minh họa tuyển sinh lớp 10, Phòng GD\&ĐT Đống Đa, "
N = {
    "lang-thuong": r"GK1 THCS Láng Thượng, 2024--2025", "nguyen-du": r"GK1 THCS Nguyễn Du, 2025--2026",
    "dvh": r"GK1 THCS Dịch Vọng Hậu, 2025--2026", "ngoc-lam": r"HK1 THCS Ngọc Lâm, 2025--2026",
    "nhat-tan": r"HK1 THCS Nhật Tân, 2025--2026",
    "sgk-vd1": r"SGK Toán 9 tập hai, Bài 21, Ví dụ 1", "sgk-vd2": r"SGK Toán 9 tập hai, Bài 21, Ví dụ 2",
    "sgk-lt": r"SGK Toán 9 tập hai, Bài 21, Luyện tập", "sgk-6.15": r"SGK Toán 9 tập hai, Bài tập 6.15",
    "sgk-6.31": r"SGK Toán 9 tập hai, Bài tập 6.31", "sgk-6.13": r"SGK Toán 9 tập hai, Bài tập 6.13",
    "sgk-6.28": r"SGK Toán 9 tập hai, Bài tập 6.28",
    "tt14": DD + r"đề 14 (THCS Thái Thịnh), 2025--2026", "tt15": DD + r"đề 15 (THCS Thái Thịnh), 2025--2026",
    "dd18": DD + r"đề 18, 2025--2026", "pm11": DD + r"đề 11 (THCS Phương Mai), 2025--2026",
    "kt07": DD + r"đề 07 (THCS Khương Thượng), 2025--2026",
    "so-hn": r"đề minh họa tuyển sinh lớp 10 THPT, Sở GD\&ĐT Hà Nội",
    "ba-dinh": r"GK2 THCS Ba Đình, 2024--2025", "nbk": r"GK1 THCS Nguyễn Bỉnh Khiêm, 2025--2026",
    "lomo": r"HK2 THCS\&THPT M.V. Lômônôxốp, 2025--2026", "cau-dien": r"HK1 THCS Cầu Diễn, 2025--2026",
    "qo2": r"thi thử vào 10 lần 2, Phòng GD\&ĐT Quốc Oai, 2024--2025", "lnh": r"GK2 THCS Lê Ngọc Hân, 2025--2026",
    "tu-lap": r"thi thử vào 10, THCS Tự Lập, 2025--2026", "tam-hiep": r"GK1 THCS Tam Hiệp, 2025--2026",
    "son-dong": r"GK1 THCS Sơn Đồng, 2024--2025", "tt-ck2": r"HK2 THCS Thái Thịnh, 2025--2026",
    "tl5": r"thi thử vào 10 lần 5, THCS Thọ Lộc, 2025--2026",
    "cau-dien-gk2": r"GK2 THCS Cầu Diễn, 2025--2026", "nguyen-du-gk2": r"GK2 THCS Nguyễn Du, 2024--2025",
    "ung-hoa": r"thi thử vào 10 lần 3, Phòng GD\&ĐT Ứng Hòa, 2024--2025", "cat-linh": DD + r"đề 03 (THCS Cát Linh), 2025--2026",
    "tay-mo": r"GK2 THCS Tây Mỗ 3, 2025--2026",
}


def ng(k):
    return r" \textit{(" + N[k] + ")}"


TH_CUOI = r"[TH] Lập phương trình, giải phương trình và trả lời."
VD_CUOI = r"[VD] Giải bài toán."
DK = r"Nêu điều kiện của $x$."

# ── SƠ ĐỒ KHỐI ────────────────────────────────────────────────────────────────
# Tiêu đề: (chữ, chặng, "heading").
# Ví dụ:  (nhãn, chặng, "", "", 0, mã, "", "vi_du", ĐỀ IN (đã có nguồn), GHI lời giải cho thợ).
# Bài:    (nhãn, chặng, tier, dang_id, level, mã, "", hình thức, ĐỀ IN NGUYÊN VĂN, GHI đáp số cho thợ).
KHOI = [
    # ───────────── LUYỆN TẬP 1 — hình chữ nhật, năng suất ─────────────
    # 17/11 Thầy: phương trình chứa ẩn ở mẫu HS đã thạo (lớp 8, rút gọn biểu thức), các bài dưới không dùng ĐKXĐ /
    # 4 bước ⇒ bỏ Mạch 1 cũ. Kiến thức cũ chỉ ôn đúng bước khử mẫu mà mọi bài lập phương trình đều dùng.
    ("Bài 1.", "practice1", "onclass", "NB1", 1, "gk2-cau-dien-2025-2 (bước khử mẫu)", "", "trac_nghiem",
     r"[NB] Với $x>0$, nhân hai vế của phương trình $\dfrac{240}{x}-\dfrac{240}{x+10}=2$ với $x(x+10)$, ta được "
     r"phương trình" + ng("cau-dien-gk2"),
     "Kiến thức cũ, MỘT bước khử mẫu: 240(x+10)−240x=2x(x+10). Chọn A. Lời giải 1–2 dòng (không giải tiếp)."),
    ("Mạch 1. Bài toán về hình chữ nhật", "practice1", "heading"),
    ("Ví dụ 1.", "practice1", "", "", 0, "sgk-b21-vd1", "", "vi_du",
     r"Một sân bóng đá 7 người có chiều rộng nhỏ hơn chiều dài $30$ m và có diện tích bằng $1\,800\ \text{m}^2$. Tính chiều "
     r"dài và chiều rộng của sân bóng đó." + ng("sgk-vd1"),
     "VÍ DỤ MỞ ĐẦU ba bước SGK. Trước Lời giải có đoạn \"Phân tích\" 3 dòng (đề hỏi gì → chọn ẩn là chiều rộng; chiều "
     "dài biểu diễn theo ẩn; câu nào cho phương trình → diện tích 1 800). Lời giải: Gọi x (m) là chiều rộng, điều kiện "
     "x>0 · chiều dài x+30 (m) · diện tích x(x+30), ta có phương trình x(x+30)=1800 · x²+30x−1800=0, Δ=900+7200=8100, "
     "√Δ=90 · x=30 hoặc x=−60 · x=30 thỏa mãn điều kiện, x=−60 không thỏa mãn · Vậy chiều rộng 30 m, chiều dài 60 m. "
     "7–9 ô."),
    ("Bài 2.", "practice1", "onclass", "NB2+TH1", 2, "sgk-6.15", "", "th_dan",
     r"Một mảnh vườn hình chữ nhật có chiều rộng nhỏ hơn chiều dài $6$ m và có diện tích bằng $280\ \text{m}^2$. Tính các "
     r"kích thước của mảnh vườn đó." + ng("sgk-6.15")
     + y(r"a) [NB] Viết công thức tính diện tích $S$ của hình chữ nhật có chiều dài $a$ và chiều rộng $b$.",
         r"b) [NB] Gọi chiều rộng của mảnh vườn là $x$ (m, $x>0$). Viết chiều dài của mảnh vườn theo $x$.",
         r"c) [NB] Viết diện tích của mảnh vườn theo $x$.", "d) " + TH_CUOI),
     "a) S=a·b (nhắc công thức). b) x+6 (m). c) x(x+6) (m²). d) Theo câu c): x(x+6)=280, x²+6x−280=0 · Δ=36+1120=1156, √Δ=34 · x=14 "
     "hoặc x=−20 · đối chiếu điều kiện x>0 nhận x=14 · Vậy chiều rộng 14 m, chiều dài 20 m."),
    ("Mạch 2. Bài toán năng suất", "practice1", "heading"),
    ("Ví dụ 2.", "practice1", "", "", 0, "v10-thai-thinh-2025-III2", "", "vi_du",
     r"Một xưởng có kế hoạch in xong $2\,000$ quyển sách giống nhau trong một thời gian quy định, biết số quyển sách "
     r"in được trong mỗi ngày là bằng nhau. Để hoàn thành sớm kế hoạch, mỗi ngày xưởng đã in nhiều hơn $100$ quyển "
     r"sách so với số quyển phải in trong một ngày theo kế hoạch nên xưởng đã in xong $2\,000$ quyển sách nói trên sớm "
     r"hơn kế hoạch một ngày. Tính số quyển sách xưởng dự định in trong một ngày theo kế hoạch." + ng("tt14"),
     "Gọi x (quyển) là số sách in mỗi ngày theo kế hoạch, x∈ℕ* · số ngày theo kế hoạch 2000/x · thực tế mỗi ngày in "
     "x+100 quyển, số ngày 2000/(x+100) · sớm hơn một ngày nên 2000/x−2000/(x+100)=1 · khử mẫu (mẫu chung x(x+100)): "
     "2000(x+100)−2000x=x(x+100), x²+100x−200000=0 · Δ=10000+800000=810000, √Δ=900 · x=400 hoặc x=−500 · x=400 "
     "thỏa mãn, x=−500 loại · Vậy theo kế hoạch mỗi ngày in 400 quyển. 7–9 ô."),
    ("Bài 3.", "practice1", "onclass", "NB2+TH1", 2, "so-hn-minhhoa-III2", "", "th_dan",
     r"Một tổ sản xuất có kế hoạch làm $300$ sản phẩm cùng loại trong một số ngày quy định. Thực tế, mỗi ngày tổ đã "
     r"làm được nhiều hơn $10$ sản phẩm so với số sản phẩm dự định làm trong một ngày theo kế hoạch. Vì thế tổ đã hoàn "
     r"thành công việc sớm hơn kế hoạch $1$ ngày. Hỏi theo kế hoạch, mỗi ngày tổ sản xuất phải làm bao nhiêu sản phẩm? "
     r"(Giả định rằng số sản phẩm mà tổ đó làm được trong mỗi ngày là bằng nhau)." + ng("so-hn")
     + y(r"a) [NB] Viết công thức tính thời gian hoàn thành công việc theo khối lượng công việc và năng suất.",
         r"b) [NB] Gọi số sản phẩm tổ phải làm mỗi ngày theo kế hoạch là $x$ (sản phẩm, $x\in\mathbb N^*$). Viết số ngày "
         r"tổ làm xong $300$ sản phẩm theo kế hoạch theo $x$.",
         r"c) [NB] Viết số ngày tổ làm xong $300$ sản phẩm trong thực tế theo $x$.", "d) " + TH_CUOI),
     "a) thời gian = khối lượng công việc : năng suất (nhắc công thức). b) 300/x. c) 300/(x+10). d) Theo câu b) và c): 300/x−300/(x+10)=1 · khử mẫu 300(x+10)−300x=x(x+10), "
     "x²+10x−3000=0 · Δ=100+12000=12100, √Δ=110 · x=50 hoặc x=−60 · nhận x=50 · Vậy mỗi ngày làm 50 sản phẩm."),
    ("Ví dụ 3.", "practice1", "", "", 0, "sgk-b21-lt1", "", "vi_du",
     r"Một đội xe gồm các xe tải cùng loại, cần phải chở $120$ tấn hàng. Tuy nhiên khi làm việc, có hai xe phải điều "
     r"chuyển đi nơi khác nên mỗi xe phải chở thêm $3$ tấn hàng. Hỏi đội xe đó có bao nhiêu chiếc xe tải?"
     + ng("sgk-lt"),
     "Gọi x (xe) là số xe tải của đội, x∈ℕ, x>2 · theo dự định mỗi xe chở 120/x tấn · thực tế còn x−2 xe, mỗi xe chở "
     "120/(x−2) tấn · mỗi xe chở thêm 3 tấn nên 120/(x−2)−120/x=3 · khử mẫu 120x−120(x−2)=3x(x−2), 240=3x²−6x, "
     "x²−2x−80=0 · Δ=4+320=324, √Δ=18 · x=10 hoặc x=−8 · nhận x=10 · Vậy đội có 10 xe tải. 7–9 ô."),
    ("Bài 4.", "practice1", "onclass", "NB2+TH1", 2, "gk2-ba-dinh-2024-III1", "", "th_dan",
     r"Để chở hết $60$ tấn quà tặng đồng bào nghèo ở vùng cao, một đội xe dự định sử dụng một số xe cùng loại. Trước "
     r"khi khởi hành, có $2$ xe phải điều đi làm việc khác. Vì vậy, mỗi xe còn lại phải chở nhiều hơn so với dự định "
     r"$1$ tấn hàng mới hết. Hỏi theo kế hoạch đội dự định sử dụng bao nhiêu xe để vận chuyển?" + ng("ba-dinh")
     + y(r"a) [NB] Có $A$ tấn hàng chia đều cho $k$ xe. Mỗi xe chở bao nhiêu tấn hàng?",
         r"b) [NB] Gọi số xe đội dự định sử dụng là $x$ (xe, $x\in\mathbb N$, $x>2$). Viết số tấn hàng mỗi xe phải chở "
         r"theo dự định theo $x$.",
         r"c) [NB] Viết số tấn hàng mỗi xe còn lại phải chở trong thực tế theo $x$.", "d) " + TH_CUOI),
     "a) A/k (tấn) — nhắc công thức. b) 60/x. c) 60/(x−2). d) Theo câu b) và c): 60/(x−2)−60/x=1 · khử mẫu 60x−60(x−2)=x(x−2), "
     "x²−2x−120=0 · Δ=4+480=484, √Δ=22 · x=12 hoặc x=−10 · nhận x=12 · Vậy đội dự định dùng 12 xe."),
    # ───────────── LUYỆN TẬP 2 — chuyển động, làm chung, hai giai đoạn ─────────────
    ("Mạch 3. Bài toán chuyển động", "practice2", "heading"),
    ("Ví dụ 4.", "practice2", "", "", 0, "sgk-b21-vd2", "", "vi_du",
     r"Khoảng cách giữa hai bến sông A và B là $36$ km. Một tàu du lịch đi từ bến A đến bến B, nghỉ $30$ phút ở bến B "
     r"rồi quay lại bến A. Thời gian kể từ lúc khởi hành đến khi về đến bến A là $5{,}5$ giờ. Hãy tìm vận tốc thực của "
     r"tàu du lịch (tức là vận tốc của tàu khi nước yên lặng), biết rằng vận tốc của dòng nước là $3$ km/h."
     + ng("sgk-vd2"),
     "ĐỌC ẢNH sgk9t2-tr26 để theo đúng cách SGK chọn chiều xuôi/ngược. Gọi x (km/h) là vận tốc thực của tàu, x>3 · "
     "vận tốc xuôi dòng x+3, ngược dòng x−3 · thời gian xuôi 36/(x+3), ngược 36/(x−3) (giờ) · 30 phút = 1/2 giờ · "
     "36/(x+3)+36/(x−3)+1/2=5,5 nên 36/(x+3)+36/(x−3)=5 · khử mẫu 36(x−3)+36(x+3)=5(x²−9), 5x²−72x−45=0 · "
     "Δ=5184+900=6084, √Δ=78 · x=15 hoặc x=−3/5 · nhận x=15 · Vậy vận tốc thực của tàu là 15 km/h. 7–9 ô."),
    ("Bài 5.", "practice2", "onclass", "NB2+TH1", 2, "v10-dong-da-de18-2025-III2", "", "th_dan",
     r"Một ca nô chuyển động xuôi dòng từ bến A đến bến B sau đó chuyển động ngược dòng từ B về A hết tổng thời gian "
     r"là $4$ giờ. Biết quãng đường sông từ A đến B dài $30$ km và vận tốc dòng nước là $4$ km/h. Tính vận tốc của ca "
     r"nô khi nước yên lặng." + ng("dd18")
     + y(r"a) [NB] Viết công thức tính thời gian $t$ khi biết quãng đường $s$ và vận tốc $v$.",
         r"b) [NB] Gọi vận tốc của ca nô khi nước yên lặng là $x$ (km/h, $x>4$). Viết vận tốc xuôi dòng và vận tốc "
         r"ngược dòng của ca nô theo $x$.",
         r"c) [NB] Viết thời gian ca nô xuôi dòng từ A đến B và thời gian ngược dòng từ B về A theo $x$.",
         "d) " + TH_CUOI),
     "a) t=s/v (nhắc công thức). b) x+4 và x−4 (km/h). c) 30/(x+4) và 30/(x−4) (giờ). d) Theo câu c): 30/(x+4)+30/(x−4)=4 · khử mẫu "
     "30(x−4)+30(x+4)=4(x²−16), 4x²−60x−64=0, x²−15x−16=0 · a−b+c=0 hoặc Δ=225+64=289, √Δ=17 · x=16 hoặc x=−1 · "
     "nhận x=16 · Vậy vận tốc ca nô khi nước yên lặng là 16 km/h."),
    ("Bài 6.", "practice2", "onclass", "NB2+TH1", 2, "sgk-6.31", "", "th_dan",
     r"Một máy bay khởi hành từ Hà Nội vào Thành phố Hồ Chí Minh, sau đó nghỉ $96$ phút và tiếp tục bay về Hà Nội với "
     r"vận tốc lớn hơn vận tốc lúc đi là $100$ km/h. Tổng thời gian của cả hành trình, kể từ khi xuất phát từ Hà Nội "
     r"đến khi quay về Hà Nội là $6$ giờ. Tính vận tốc của máy bay lúc đi, biết quãng đường bay Hà Nội -- Thành phố Hồ "
     r"Chí Minh dài khoảng $1\,200$ km." + ng("sgk-6.31")
     + y(r"a) [NB] Đổi $96$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc của máy bay lúc đi là $x$ (km/h, $x>0$). Viết thời gian bay lúc đi theo $x$.",
         r"c) [NB] Viết thời gian bay lúc về theo $x$.", "d) " + TH_CUOI),
     "a) 96 phút = 8/5 giờ. b) 1200/x (giờ). c) 1200/(x+100) (giờ). d) Theo câu a), b), c): 1200/x+8/5+1200/(x+100)=6, "
     "nên 1200/x+1200/(x+100)=22/5 · khử mẫu (mẫu chung 5x(x+100)): 6000(x+100)+6000x=22x(x+100), "
     "22x²−9800x−600000=0, 11x²−4900x−300000=0 · Δ=4900²+4·11·300000=37210000, √Δ=6100 · x=500 hoặc x=−600/11 · "
     "nhận x=500 · Vậy vận tốc lúc đi là 500 km/h."),
    ("Ví dụ 5.", "practice2", "", "", 0, "gk1-nguyen-binh-khiem-2025-II2-md902", "", "vi_du",
     r"Quãng đường AB dài $108$ km. Hai ô tô cùng khởi hành một lúc để đi từ A đến B. Biết ô tô thứ nhất chạy nhanh "
     r"hơn ô tô thứ hai là $6$ km/h nên ô tô thứ hai đến muộn hơn ô tô thứ nhất là $12$ phút. Tính vận tốc của mỗi xe."
     + ng("nbk"),
     "Gọi x (km/h) là vận tốc ô tô thứ hai, x>0 · vận tốc ô tô thứ nhất x+6 · thời gian ô tô thứ hai 108/x, ô tô thứ "
     "nhất 108/(x+6) (giờ) · 12 phút = 1/5 giờ · ô tô thứ hai đến muộn hơn nên 108/x−108/(x+6)=1/5 · khử mẫu (mẫu chung "
     "5x(x+6)): 540(x+6)−540x=x(x+6), x²+6x−3240=0 · Δ=36+12960=12996, √Δ=114 · x=54 hoặc x=−60 · nhận x=54 · Vậy "
     "ô tô thứ hai 54 km/h, ô tô thứ nhất 60 km/h. 7–9 ô."),
    ("Bài 7.", "practice2", "onclass", "NB2+TH1", 2, "gk2-nguyen-du-2024-22", "", "th_dan",
     r"Một ô tô và một xe máy cùng khởi hành để đi từ A đến B. Do vận tốc của ô tô lớn hơn vận tốc xe máy là $20$ km/h "
     r"nên ô tô đến B sớm hơn xe máy $30$ phút. Tính vận tốc mỗi xe biết quãng đường AB dài $120$ km." + ng("nguyen-du-gk2")
     + y(r"a) [NB] Gọi vận tốc của xe máy là $x$ (km/h, $x>0$). Viết vận tốc của ô tô theo $x$.",
         r"b) [NB] Viết thời gian xe máy đi hết quãng đường AB theo $x$.",
         r"c) [NB] Viết thời gian ô tô đi hết quãng đường AB theo $x$.", "d) " + TH_CUOI),
     "a) x+20. b) 120/x. c) 120/(x+20). d) 30 phút = 1/2 giờ · ô tô đến sớm hơn nên 120/x−120/(x+20)=1/2 · khử mẫu "
     "240(x+20)−240x=x(x+20), x²+20x−4800=0 · Δ=400+19200=19600, √Δ=140 · x=60 hoặc x=−80 · nhận x=60 · Vậy xe máy "
     "60 km/h, ô tô 80 km/h."),
    ("Bài 8.", "practice2", "onclass", "NB2+TH1", 2, "ck2-lomonoxop-2025-III2", "", "th_dan",
     r"Một người dự định đi xe máy từ A đến B với quãng đường dài $100$ km. Do có công việc đột xuất ở B nên người đó "
     r"đã tăng vận tốc thêm $10$ km/h và đã đến B sớm hơn dự định $30$ phút. Hỏi người đó dự định đi với vận tốc là "
     r"bao nhiêu km/h?" + ng("lomo")
     + y(r"a) [NB] Đổi $30$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc dự định là $x$ (km/h, $x>0$). Viết thời gian đi theo dự định theo $x$.",
         r"c) [NB] Viết thời gian người đó đã đi trong thực tế theo $x$.", "d) " + TH_CUOI),
     "a) 30 phút = 1/2 giờ. b) 100/x. c) 100/(x+10). d) Theo câu a), b), c): 100/x−100/(x+10)=1/2 · khử mẫu "
     "200(x+10)−200x=x(x+10), x²+10x−2000=0 · Δ=100+8000=8100, √Δ=90 · x=40 hoặc x=−50 · nhận x=40 · Vậy vận tốc "
     "dự định là 40 km/h."),
    ("Mạch 4. Bài toán làm chung, làm riêng", "practice2", "heading"),
    ("Ví dụ 6.", "practice2", "", "", 0, "ck1-cau-dien-2025-3b", "", "vi_du",
     r"Hai đội công nhân cùng làm một công việc thì làm xong trong $4$ giờ. Nếu mỗi đội làm một mình xong công việc đó "
     r"thì đội thứ nhất cần ít thời gian hơn đội thứ hai là $6$ giờ. Hỏi mỗi đội làm một mình xong công việc đó trong "
     r"bao lâu?" + ng("cau-dien"),
     "Gọi x (giờ) là thời gian đội thứ nhất làm một mình xong công việc, x>4 · đội thứ hai làm một mình xong trong x+6 "
     "(giờ) · trong một giờ đội thứ nhất làm được 1/x công việc, đội thứ hai 1/(x+6) công việc, cả hai đội 1/4 công việc "
     "· ta có phương trình 1/x+1/(x+6)=1/4 · khử mẫu (mẫu chung 4x(x+6)): 4(x+6)+4x=x(x+6), x²−2x−24=0 · Δ=4+96=100, "
     "√Δ=10 · x=6 hoặc x=−4 · nhận x=6 · Vậy đội thứ nhất 6 giờ, đội thứ hai 12 giờ. 7–9 ô."),
    ("Bài 9.", "practice2", "onclass", "NB2+TH1", 2, "v10-ung-hoa-lan3-2025-III2", "", "th_dan",
     r"Hai người cùng làm chung một công việc thì sau $3$ giờ $36$ phút làm xong. Nếu làm một mình thì người thứ nhất "
     r"hoàn thành công việc sớm hơn người thứ hai là $3$ giờ. Hỏi nếu mỗi người làm một mình thì bao lâu xong công việc."
     + ng("ung-hoa")
     + y(r"a) [NB] Một người làm một mình xong công việc trong $t$ giờ. Trong $1$ giờ người đó làm được bao nhiêu phần "
         r"công việc?",
         r"b) [NB] Đổi $3$ giờ $36$ phút ra giờ.",
         r"c) [NB] Gọi thời gian người thứ nhất làm một mình xong công việc là $x$ (giờ, $x>\dfrac{18}{5}$). Viết thời gian người thứ "
         r"hai làm một mình xong công việc theo $x$.",
         r"d) [NB] Trong $1$ giờ, cả hai người cùng làm được bao nhiêu phần công việc?", "e) " + TH_CUOI),
     "a) 1/t công việc (nhắc công thức). b) 18/5 giờ. c) x+3. d) 1:(18/5)=5/18 công việc. e) trong 1 giờ người thứ nhất "
     "làm 1/x, người thứ hai 1/(x+3) công việc · theo câu d): 1/x+1/(x+3)=5/18 · khử mẫu (mẫu chung 18x(x+3)): "
     "18(x+3)+18x=5x(x+3), 5x²−21x−54=0 · Δ=441+1080=1521, √Δ=39 · x=6 hoặc x=−9/5 · nhận x=6 · Vậy người thứ nhất 6 "
     "giờ, người thứ hai 9 giờ."),
    ("Bài 10.", "practice2", "onclass", "NB2+VD1", 3, "v10-quoc-oai-l2-2024-2.1", "", "vd_de",
     r"Hai vòi nước cùng chảy vào một bể cạn trong $2$ giờ $40$ phút thì đầy bể. Nếu chảy riêng để đầy bể đó thì vòi I "
     r"chảy đầy bể trước vòi II là $4$ giờ. Hỏi nếu chảy riêng thì mỗi vòi chảy đầy bể trong bao lâu?" + ng("qo2")
     + y(r"a) [NB] Đổi $2$ giờ $40$ phút ra giờ.",
         r"b) [NB] Gọi thời gian vòi I chảy riêng đầy bể là $x$ (giờ). Viết thời gian vòi II chảy riêng đầy bể theo $x$.",
         r"c) [NB] Trong một giờ, cả hai vòi cùng chảy được bao nhiêu phần bể?", "d) " + VD_CUOI),
     "a) 2 giờ 40 phút = 8/3 giờ. b) x+4 (giờ). c) 3/8 bể. d) (chỉ đề) điều kiện x>8/3 · trong một giờ vòi I chảy "
     "1/x bể, vòi II 1/(x+4) bể · theo câu c): 1/x+1/(x+4)=3/8 · khử mẫu (mẫu chung 8x(x+4)): 8(x+4)+8x=3x(x+4), "
     "3x²−4x−32=0 · Δ=16+384=400, √Δ=20 · x=4 hoặc x=−8/3 · nhận x=4 · Vậy vòi I chảy riêng 4 giờ, vòi II 8 giờ."),
    ("Mạch 5. Bài toán hai giai đoạn", "practice2", "heading"),
    ("Ví dụ 7.", "practice2", "", "", 0, "gk2-le-ngoc-han-2025-III1", "", "vi_du",
     r"Một ô tô dự định đi từ A đến B cách nhau $120$ km trong một thời gian quy định. Sau khi đi được $1$ giờ thì ô tô "
     r"bị chặn bởi xe cứu hỏa $10$ phút. Do đó để đến B đúng hạn xe phải tăng vận tốc thêm $6$ km/h trên quãng đường "
     r"còn lại. Tính vận tốc lúc đầu của ô tô." + ng("lnh"),
     "Gọi x (km/h) là vận tốc lúc đầu, 0<x<120 · thời gian dự định 120/x (giờ) · 1 giờ đầu đi được x km, quãng đường "
     "còn lại 120−x (km) đi với vận tốc x+6, hết (120−x)/(x+6) giờ · 10 phút = 1/6 giờ · đến đúng hạn nên "
     "1+1/6+(120−x)/(x+6)=120/x · khử mẫu (mẫu chung 6x(x+6)): 6x(x+6)+x(x+6)+6x(120−x)=720(x+6), x²+42x−4320=0 · "
     "Δ=1764+17280=19044, √Δ=138 · x=48 hoặc x=−90 · nhận x=48 · Vậy vận tốc lúc đầu là 48 km/h. 7–9 ô (thời gian "
     "dự định, quãng đường còn lại, thời gian đi quãng còn lại, đổi 10 phút, phương trình, nghiệm, kết luận)."),
    ("Bài 11.", "practice2", "onclass", "NB2+VD1", 3, "v10-tu-lap-2026-III2 — ĐÍCH", "", "vd_de",
     r"Hàng ngày, bạn Nam đi học từ nhà đến trường trên quãng đường $12$ km bằng xe máy điện với vận tốc không đổi. "
     r"Một hôm, vẫn trên đoạn đường đó, $3$ km đầu bạn Nam đi với vận tốc như thường ngày, sau đó vì xe non hơi nên "
     r"bạn đã dừng lại $3$ phút để bơm. Để đến trường đúng giờ, bạn Nam phải tăng vận tốc lên thêm $6$ km/h. Tính vận "
     r"tốc xe máy điện của bạn Nam khi tăng tốc. Với vận tốc đó, bạn Nam có vi phạm luật giao thông hay không? Tại "
     r"sao? Biết rằng đoạn đường bạn Nam đi giới hạn tốc độ tối đa là $40$ km/h." + ng("tu-lap")
     + y(r"a) [NB] Đổi $3$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc xe máy điện thường ngày của bạn Nam là $x$ (km/h, $x>0$). Viết thời gian bạn Nam đi "
         r"hết $12$ km thường ngày theo $x$.",
         r"c) [NB] Viết thời gian bạn Nam đi $9$ km còn lại sau khi tăng tốc theo $x$.", "d) " + VD_CUOI),
     "BÀI ĐÍCH. a) 3 phút = 1/20 giờ. b) 12/x. c) 9/(x+6). d) (chỉ đề) thời gian hôm nay 3/x+1/20+9/(x+6) bằng thời "
     "gian thường ngày 12/x · 9/x−9/(x+6)=1/20 · khử mẫu (mẫu chung 20x(x+6)): 180(x+6)−180x=x(x+6), x²+6x−1080=0 · "
     "Δ=36+4320=4356, √Δ=66 · x=30 hoặc x=−36 · nhận x=30 · vận tốc khi tăng tốc 30+6=36 km/h · 36<40 nên bạn Nam "
     "không vi phạm luật giao thông · Vậy vận tốc khi tăng tốc là 36 km/h, không vi phạm vì 36<40."),
    # ───────────── BTVN — TH lập PT rồi VD (26 NB + 8 TH + 2 VD) ─────────────
    ("Bài 12.", "reflection", "btvn", "NB2+TH1", 2, "sgk-6.13", "", "th_dan",
     r"Độ cao $h$ (mét) so với mặt đất của một vật được phóng thẳng đứng lên trên từ mặt đất với vận tốc ban đầu "
     r"$v_0=19{,}6$ m/s cho bởi công thức $h=19{,}6t-4{,}9t^2$, ở đó $t$ (giây) là thời gian kể từ khi phóng (theo Vật "
     r"lí đại cương, NXB Giáo dục Việt Nam, 2016). Hỏi sau bao lâu kể từ khi phóng, vật sẽ rơi trở lại mặt đất?"
     + ng("sgk-6.13")
     + y(r"a) [NB] Khi vật rơi trở lại mặt đất thì độ cao $h$ bằng bao nhiêu?",
         r"b) [NB] Viết phương trình ẩn $t$ ứng với lúc vật rơi trở lại mặt đất.",
         r"c) [TH] Giải phương trình ở câu b) và trả lời."),
     "a) h=0. b) 19,6t−4,9t²=0. c) 4,9t(4−t)=0 · t=0 (lúc bắt đầu phóng) hoặc t=4 · Vậy sau 4 giây vật rơi trở lại "
     "mặt đất."),
    ("Bài 13.", "reflection", "btvn", "NB2+TH1", 2, "sgk-6.28", "", "th_dan",
     r"Một mảnh đất hình chữ nhật có diện tích $360\ \text{m}^2$. Nếu tăng chiều rộng $3$ m và giảm chiều dài $4$ m thì diện "
     r"tích mảnh đất không đổi. Tìm các kích thước của mảnh đất đó." + ng("sgk-6.28")
     + y(r"a) [NB] Gọi chiều rộng của mảnh đất là $x$ (m, $x>0$). Viết chiều dài của mảnh đất theo $x$.",
         r"b) [NB] Viết chiều rộng và chiều dài của mảnh đất sau khi thay đổi theo $x$.", "c) " + TH_CUOI),
     "a) 360/x (m). b) x+3 và 360/x−4 (m). c) Theo câu b): (x+3)(360/x−4)=360 · nhân hai vế với x: (x+3)(360−4x)=360x, "
     "4x²+12x−1080=0, x²+3x−270=0 · Δ=9+1080=1089, √Δ=33 · x=15 hoặc x=−18 · nhận x=15 (khi đó chiều dài mới "
     "24−4=20>0) · Vậy chiều rộng 15 m, chiều dài 24 m."),
    ("Bài 14.", "reflection", "btvn", "NB2+TH1", 2, "v10-cat-linh-2025-III1", "", "th_dan",
     r"Một mảnh đất hình chữ nhật có chiều rộng ngắn hơn chiều dài $11$ m và diện tích là $180\ \text{m}^2$. Tính các "
     r"kích thước của mảnh đất đó." + ng("cat-linh")
     + y(r"a) [NB] Gọi chiều rộng của mảnh đất là $x$ (m, $x>0$). Viết chiều dài của mảnh đất theo $x$.",
         r"b) [NB] Viết diện tích của mảnh đất theo $x$.", "c) " + TH_CUOI),
     "a) x+11 (m). b) x(x+11) (m²). c) x(x+11)=180, x²+11x−180=0 · Δ=121+720=841, √Δ=29 · x=9 hoặc x=−20 · nhận x=9 · "
     "Vậy chiều rộng 9 m, chiều dài 20 m."),
    ("Bài 15.", "reflection", "btvn", "NB2+TH1", 2, "gk1-son-dong-2024-22", "", "th_dan",
     r"Một tổ công nhân dự định làm xong $600$ sản phẩm trong một thời gian nhất định. Nhưng khi thực hiện, nhờ cải "
     r"tiến kĩ thuật nên mỗi ngày tổ đã làm tăng thêm $30$ sản phẩm so với dự định. Do đó tổ đã hoàn thành công việc "
     r"sớm hơn dự định $1$ ngày. Hỏi theo kế hoạch, mỗi ngày tổ phải làm được bao nhiêu sản phẩm?" + ng("son-dong")
     + y(r"a) [NB] Viết công thức tính năng suất theo khối lượng công việc và thời gian hoàn thành.",
         r"b) [NB] Gọi số sản phẩm tổ phải làm mỗi ngày theo kế hoạch là $x$ (sản phẩm, $x\in\mathbb N^*$). Viết số ngày "
         r"tổ làm xong $600$ sản phẩm theo kế hoạch theo $x$.",
         r"c) [NB] Viết số ngày tổ làm xong $600$ sản phẩm trong thực tế theo $x$.", "d) " + TH_CUOI),
     "a) năng suất = khối lượng công việc : thời gian (nhắc công thức). b) 600/x. c) 600/(x+30). d) Theo câu b) và c): 600/x−600/(x+30)=1 · khử mẫu 600(x+30)−600x=x(x+30), "
     "x²+30x−18000=0 · Δ=900+72000=72900, √Δ=270 · x=120 hoặc x=−150 · nhận x=120 · Vậy mỗi ngày 120 sản phẩm."),
    ("Bài 16.", "reflection", "btvn", "NB2+TH1", 2, "v10-phuong-mai-2025-III2", "", "th_dan",
     r"Một tổ công nhân phải làm $144$ dụng cụ. Do $3$ công nhân chuyển đi làm việc khác nên mỗi người còn lại phải "
     r"làm thêm $4$ dụng cụ. Tính số công nhân lúc đầu của tổ nếu năng suất của mỗi người là như nhau." + ng("pm11")
     + y(r"a) [NB] Có $A$ dụng cụ chia đều cho $k$ người. Mỗi người phải làm bao nhiêu dụng cụ?",
         r"b) [NB] Gọi số công nhân lúc đầu của tổ là $x$ (người, $x\in\mathbb N$, $x>3$). Viết số dụng cụ mỗi người "
         r"phải làm theo dự định theo $x$.",
         r"c) [NB] Viết số dụng cụ mỗi người còn lại phải làm trong thực tế theo $x$.", "d) " + TH_CUOI),
     "a) A/k — nhắc công thức. b) 144/x. c) 144/(x−3). d) Theo câu b) và c): 144/(x−3)−144/x=4 · khử mẫu 144x−144(x−3)=4x(x−3), "
     "x²−3x−108=0 · Δ=9+432=441, √Δ=21 · x=12 hoặc x=−9 · nhận x=12 · Vậy lúc đầu tổ có 12 công nhân."),
    ("Bài 17.", "reflection", "btvn", "NB2+TH1", 2, "ck2-thai-thinh-2025-III1", "", "th_dan",
     r"Một ô tô và một xe máy khởi hành cùng một lúc để đi từ A đến B. Biết quãng đường AB dài $90$ km và vận tốc của "
     r"ô tô lớn hơn vận tốc xe máy $15$ km/h nên ô tô đến B sớm hơn xe máy $30$ phút (biết vận tốc mỗi xe không đổi "
     r"trên toàn bộ quãng đường). Tính vận tốc mỗi xe?" + ng("tt-ck2")
     + y(r"a) [NB] Đổi $30$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc của xe máy là $x$ (km/h, $x>0$). Viết vận tốc của ô tô theo $x$.",
         r"c) [NB] Viết thời gian xe máy và thời gian ô tô đi hết quãng đường AB theo $x$.", "d) " + TH_CUOI),
     "a) 1/2 giờ. b) x+15. c) 90/x và 90/(x+15). d) Theo câu a) và c): 90/x−90/(x+15)=1/2 · khử mẫu "
     "180(x+15)−180x=x(x+15), x²+15x−2700=0 · Δ=225+10800=11025, √Δ=105 · x=45 hoặc x=−60 · nhận x=45 · Vậy xe máy "
     "45 km/h, ô tô 60 km/h."),
    ("Bài 18.", "reflection", "btvn", "NB2+TH1", 2, "v10-thai-thinh-2025-III2-md2", "", "th_dan",
     r"Một người đi xe đạp từ A đến B cách nhau $36$ km. Khi đi từ B trở về A, người đó tăng vận tốc thêm $3$ km/h, vì "
     r"vậy thời gian về ít hơn thời gian đi là $36$ phút. Tính vận tốc của người đi xe đạp khi đi từ A đến B."
     + ng("tt15")
     + y(r"a) [NB] Đổi $36$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc của người đi xe đạp khi đi từ A đến B là $x$ (km/h, $x>0$). Viết thời gian đi từ A "
         r"đến B theo $x$.",
         r"c) [NB] Viết thời gian về từ B đến A theo $x$.", "d) " + TH_CUOI),
     "a) 3/5 giờ. b) 36/x. c) 36/(x+3). d) Theo câu a), b), c): 36/x−36/(x+3)=3/5 · khử mẫu (mẫu chung 5x(x+3)): "
     "180(x+3)−180x=3x(x+3), x²+3x−180=0 · Δ=9+720=729, √Δ=27 · x=12 hoặc x=−15 · nhận x=12 · Vậy 12 km/h."),
    ("Bài 19.", "reflection", "btvn", "NB2+TH1", 2, "gk2-tay-mo-3-2025-III1", "", "th_dan",
     r"Một ô tô và một xe máy cùng khởi hành để đi từ A đến B. Do vận tốc của ô tô lớn hơn vận tốc của xe máy là $25$ "
     r"km/h nên ô tô đến B sớm hơn xe máy $60$ phút. Tính vận tốc mỗi xe biết quãng đường AB dài $150$ km." + ng("tay-mo")
     + y(r"a) [NB] Gọi vận tốc của xe máy là $x$ (km/h, $x>0$). Viết thời gian xe máy đi hết quãng đường AB theo $x$.",
         r"b) [NB] Viết thời gian ô tô đi hết quãng đường AB theo $x$.", "c) " + TH_CUOI),
     "a) 150/x. b) 150/(x+25). c) 60 phút = 1 giờ · 150/x−150/(x+25)=1 · khử mẫu 150(x+25)−150x=x(x+25), "
     "x²+25x−3750=0 · Δ=625+15000=15625, √Δ=125 · x=50 hoặc x=−75 · nhận x=50 · Vậy xe máy 50 km/h, ô tô 75 km/h."),
    ("Bài 20.", "reflection", "btvn", "NB2+VD1", 3, "v10-tho-loc-l5-2025-III2", "", "vd_de",
     r"Một đội công nhân theo kế hoạch làm $480$ sản phẩm trong một thời gian nhất định. Khi làm được $60$ sản phẩm, "
     r"do yêu cầu đẩy nhanh tiến độ công việc nên mỗi ngày đội đã làm thêm được nhiều hơn dự kiến $5$ sản phẩm, vì vậy "
     r"đội hoàn thành sớm hơn so với dự kiến $2$ ngày. Hỏi ban đầu đội dự định mỗi ngày làm bao nhiêu sản phẩm?"
     + ng("tl5")
     + y(r"a) [NB] Gọi số sản phẩm đội dự định làm mỗi ngày là $x$ ($x\in\mathbb N^*$). Viết số ngày đội dự định "
         r"làm xong $480$ sản phẩm theo $x$.",
         r"b) [NB] Viết số ngày đội làm $60$ sản phẩm đầu tiên theo $x$.",
         r"c) [NB] Viết số ngày đội làm số sản phẩm còn lại theo $x$.", "d) " + VD_CUOI),
     "a) 480/x. b) 60/x. c) 420/(x+5). d) (chỉ đề) 480/x−(60/x+420/(x+5))=2 · 420/x−420/(x+5)=2 · khử mẫu "
     "420(x+5)−420x=2x(x+5), x²+5x−1050=0 · Δ=25+4200=4225, √Δ=65 · x=30 hoặc x=−35 · nhận x=30 · Vậy 30 sản phẩm."),
    ("Bài 21.", "reflection", "btvn", "NB2+VD1", 3, "v10-khuong-thuong-2025-III2", "", "vd_de",
     r"Quãng đường AB dài $180$ km. Một xe máy khởi hành từ A đến B với vận tốc không đổi. Sau đó $24$ phút một ô tô "
     r"cũng khởi hành từ A nhưng đi với vận tốc lớn hơn vận tốc xe máy là $5$ km/h nên đã đến B cùng lúc với xe máy. "
     r"Tính vận tốc của xe máy." + ng("kt07")
     + y(r"a) [NB] Đổi $24$ phút ra giờ.",
         r"b) [NB] Gọi vận tốc của xe máy là $x$ (km/h, $x>0$). Viết thời gian xe máy đi hết quãng đường AB theo $x$.",
         r"c) [NB] Viết thời gian ô tô đi hết quãng đường AB theo $x$.", "d) " + VD_CUOI),
     "a) 2/5 giờ. b) 180/x. c) 180/(x+5). d) (chỉ đề) xe máy đi lâu hơn ô tô 24 phút: 180/x−180/(x+5)=2/5 · khử mẫu "
     "(mẫu chung 5x(x+5)): 900(x+5)−900x=2x(x+5), x²+5x−2250=0 · Δ=25+9000=9025, √Δ=95 · x=45 hoặc x=−50 · nhận "
     "x=45 · Vậy vận tốc xe máy là 45 km/h."),
]

OPTIONS = {"Bài 1.": [r"$240(x+10)-240x=2x(x+10)$", r"$240x-240(x+10)=2x(x+10)$", r"$240(x+10)-240x=2$", r"$240-240=2x(x+10)$"]}   # đáp án A

TM_DANG = {  # dang_id → (onclass, btvn) chốt trong thuyết minh phiếu 4 (17/11 bản bỏ phương trình chứa ẩn ở mẫu)
    "NB1": (1, 0), "NB2": (31, 26), "TH1": (8, 8), "VD1": (2, 2),
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
