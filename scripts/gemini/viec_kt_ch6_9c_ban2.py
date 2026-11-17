#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐỀ KIỂM TRA CHƯƠNG VI 9C — BẢN 2 (90 phút, 17/11/2026, phiên Phiếu 5) — sơ đồ + SymPy + 2 việc Gemini.

Thầy 16/11 chốt kế hoạch: đề KT chương 90′, làm ở phiên P5; 17/11: bỏ hẳn phương trình chứa ẩn ở mẫu (C6-17).
Câu lấy từ chon-cau.json (vai "KT chương", P5): Claude chốt số liệu + điểm + đáp số (SymPy ở dưới), Gemini viết
tờ đề + đáp án/barem. Ma trận do lap_kt_ch6_9c_ban2.py sinh máy móc từ SO_DO (một nguồn số liệu).

    .venv/bin/python scripts/gemini/viec_kt_ch6_9c_ban2.py          # kiểm SymPy + ghi 2 việc
    python3 scripts/gemini/tho.py --song-song 2                       (kt2-9c-ch6-de / kt2-9c-ch6-dap-an)
    .venv/bin/python scripts/gemini/lap_kt_ch6_9c_ban2.py [--ghi]
"""
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
MAU = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/kiem-tra-chuong"
P5 = f"{D}/phieu-5-luyen-tap-chung-bai-tap-cuoi-chuong-vi.json"
VID_DE, VID_DA = "kt2-9c-ch6-de", "kt2-9c-ch6-dap-an"

# (câu, nội dung ma trận, mức, điểm, phút, hình thức, đáp án ngắn, mã nguồn) — số đã kiểm SymPy (kiem() dưới)
SO_DO = [
    ("Câu 1", "Nhận biết phương trình bậc hai một ẩn", "NB", 0.5, 3, "trắc nghiệm", "$4x-7=0$ không phải", "tl-ptb2-01-tr1"),
    ("Câu 2", "Tổng và tích hai nghiệm của $4x^2-5x-3=0$ (định lí Viète)", "NB", 0.5, 3, "trắc nghiệm",
     "$x_1+x_2=\\dfrac54$, $x_1x_2=-\\dfrac34$", "tl-viete-15-tr3"),
    ("Câu 3", "Tính $\\Delta$ của $-2x^2+5x-4=0$, kết luận số nghiệm", "NB", 0.5, 3, "trắc nghiệm",
     "$\\Delta=-7<0$: vô nghiệm", "tl-ptb2-03-tr4"),
    ("Câu 4", "Nhẩm nghiệm $x^2-9x+8=0$ nhờ $a+b+c=0$", "NB", 0.5, 3, "trắc nghiệm", "$1$ và $8$",
     "tl-viete-02-tr1"),
    ("Câu 5a", "Giải phương trình $x^2-3x+2=0$", "NB", 0.5, 4, "tự luận", "$x_1=1$, $x_2=2$", "gk2-co-dong-2024-III1"),
    ("Câu 5b", "Giải phương trình $2x^2+5x+3=0$", "NB", 0.5, 4, "tự luận", "$x_1=-1$, $x_2=-\\dfrac32$",
     "gk2-ban-mai-2024-6a"),
    ("Câu 6", "Chứng minh $x^2+(m+1)x+2m-2=0$ luôn có hai nghiệm với mọi $m$", "TH", 1.0, 8, "tự luận",
     "$\\Delta=(m-3)^2\\ge0$", "v10-nguyen-tat-thanh-2025-cau8"),
    ("Câu 7a", "Chứng minh $4x^2+8x-15=0$ có hai nghiệm phân biệt", "NB", 0.5, 3, "tự luận", "$ac=-60<0$",
     "ck2-lomonoxop-2025-III3"),
    ("Câu 7b", "Tính $M=x_1^2+x_2^2-5x_1x_2$ theo tổng và tích hai nghiệm", "TH", 1.0, 7, "tự luận",
     "$M=(x_1+x_2)^2-7x_1x_2=\\dfrac{121}{4}$", "ck2-lomonoxop-2025-III3"),
    ("Câu 8", "Biết một nghiệm $x=\\dfrac{3+\\sqrt{21}}{2}$ của $x^2-ax-3=0$, tính bình phương hiệu hai nghiệm", "TH",
     1.0, 8, "tự luận", "$x_2=\\dfrac{3-\\sqrt{21}}{2}$, $(x_1-x_2)^2=21$", "ck2-phuc-dong-2024-901-III2"),
    ("Câu 9a", "Giải $x^2-2x+m-1=0$ với $m=0$", "NB", 0.5, 4, "tự luận", "$x=1\\pm\\sqrt2$", "gk2-ba-dinh-2025-III2"),
    ("Câu 9b", "Tìm $m$ để hai nghiệm phân biệt thỏa mãn $\\dfrac{3}{x_1x_2}-x_1-x_2=2$", "VD", 1.0, 10, "tự luận",
     "$m<2$, $m\\ne1$, $m=\\dfrac74$", "gk2-ba-dinh-2025-III2"),
    ("Câu 10", "Giải bài toán bằng cách lập phương trình (năng suất): $300$ sản phẩm, mỗi giờ thêm $5$, sớm $2$ giờ",
     "TH", 1.0, 14, "tự luận", "$x^2+5x-750=0$, $x=25$", "ck2-hai-ba-trung-2024-III1"),
    ("Câu 11", "Giải bài toán bằng cách lập phương trình (hai lần thay đổi): $40$ tấn, thêm $14$ tấn, thêm $2$ xe, mỗi "
     "xe thêm $0{,}5$ tấn", "VD", 1.0, 14, "tự luận", "$x^2-26x+160=0$, $x=10$ (loại $16>15$)", "v10-tho-loc-l4-2026-III1"),
]
DUNG = {"Câu 1.": "C", "Câu 2.": "A", "Câu 3.": "D", "Câu 4.": "B"}
DIEM_Y = {"5a": 0.5, "5b": 0.5, "6": 1.0, "7a": 0.5, "7b": 1.0, "8": 1.0, "9a": 0.5, "9b": 1.0, "10": 1.0, "11": 1.0}


def kiem():
    x, m, a = sp.symbols("x m a")
    R = sp.Rational
    loi = []

    def bang(ten, that, mong):
        if sp.simplify(sp.sympify(that) - sp.sympify(mong)) != 0:
            loi.append(f"{ten}: máy {sp.simplify(that)} ≠ {mong}")

    def ng(ten, e, mong):
        r = sp.solve(sp.sympify(e), x)
        if sorted(r, key=sp.default_sort_key) != sorted(map(sp.nsimplify, mong), key=sp.default_sort_key):
            loi.append(f"{ten}: nghiệm máy {r} ≠ {mong}")

    bang("Câu 2 tổng", R(5, 4), R(5, 4)); bang("Câu 2 tích", R(-3, 4), R(-3, 4))
    bang("Câu 2 Δ", 25 + 48, 73); assert 25 + 48 > 0
    bang("Câu 3 Δ", 25 - 4 * (-2) * (-4), -7)
    ng("Câu 4", "x**2-9*x+8", [1, 8])
    ng("Câu 5a", "x**2-3*x+2", [1, 2])
    ng("Câu 5b", "2*x**2+5*x+3", [-1, R(-3, 2)])
    bang("Câu 6 Δ", sp.expand((m + 1) ** 2 - 4 * (2 * m - 2)), sp.expand((m - 3) ** 2))
    r = sp.solve(4 * x**2 + 8 * x - 15, x)
    bang("Câu 7b M", sp.simplify(r[0] ** 2 + r[1] ** 2 - 5 * r[0] * r[1]), R(121, 4))
    x1 = (3 + sp.sqrt(21)) / 2
    av = sp.solve((x**2 - a * x - 3).subs(x, x1), a)[0]
    bang("Câu 8 a", av, 3)
    r = sp.solve(x**2 - av * x - 3, x)
    bang("Câu 8 (x1−x2)²", sp.expand((r[0] - r[1]) ** 2), 21)
    ng("Câu 9a", "x**2-2*x-1", [1 + sp.sqrt(2), 1 - sp.sqrt(2)])
    S, P = 2, m - 1
    ung = [v for v in sp.solve(3 / P - S - 2, m) if (4 - 4 * (m - 1)).subs(m, v) > 0 and P.subs(m, v) != 0]
    bang("Câu 9b m", ung[0] if len(ung) == 1 else "nhiều", R(7, 4))
    e = sp.together(300 / x - 300 / (x + 5) - 2)
    r = [v for v in sp.solve(sp.numer(e), x) if v > 0]
    bang("Câu 10", r[0], 25)
    bang("Câu 10 PT", sp.expand(-sp.numer(e) / 2), "x**2+5*x-750")
    e = sp.together(54 / (x + 2) - 40 / x - R(1, 2))
    r = [v for v in sp.solve(sp.numer(e), x) if v > 0]
    if sorted(r) != [10, 16]:
        loi.append(f"Câu 11 hai nghiệm: máy {r} ≠ [10, 16]")
    assert abs(sum(c[3] for c in SO_DO) - 10) < 1e-9, "tổng điểm ≠ 10"
    assert sum(c[4] for c in SO_DO) <= 90, "quá 90 phút"
    return loi


CHUNG = r'''Bạn là thợ soạn đề kiểm tra Toán 9 (ĐẠI SỐ — chương VI: phương trình bậc hai một ẩn, định lí Viète, giải bài toán bằng cách lập phương trình) cho học sinh lớp 9 TẦNG C (học lực trung bình, ôn thi vào 10 Hà Nội). Đề 90 phút, thang 10 điểm. Làm CẨN THẬN, KHÔNG bịa đề: dùng ĐÚNG số liệu và câu chữ trong SƠ ĐỒ ĐỀ bên dưới (giáo viên đã chốt, đề lấy nguyên từ đề kiểm tra các trường, đáp số đã kiểm bằng máy), không đổi số, không thêm bớt câu.

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt.

## SƠ ĐỒ ĐỀ (bất di bất dịch)
PHẦN I. TRẮC NGHIỆM (2,0 điểm) — mỗi câu 0,5 điểm, 4 phương án, đúng MỘT phương án. Phương án ghi đúng thứ tự A, B, C, D như dưới:
- Câu 1. "Phương trình nào sau đây \textbf{không} phải là phương trình bậc hai một ẩn?" A. $x^2-3x+5=0$ · B. $-y^2+0{,}5y=0$ · C. $4x-7=0$ · D. $2t^2-\sqrt3=0$. Đúng: C.
- Câu 2. "Phương trình $4x^2-5x-3=0$ có hai nghiệm $x_1$, $x_2$. Khi đó $x_1+x_2$ và $x_1x_2$ lần lượt bằng" A. $\dfrac54$ và $-\dfrac34$ · B. $-\dfrac54$ và $-\dfrac34$ · C. $\dfrac54$ và $\dfrac34$ · D. $-\dfrac34$ và $\dfrac54$. Đúng: A ($ac=-12<0$ nên có hai nghiệm, Viète).
- Câu 3. "Số nghiệm của phương trình $-2x^2+5x-4=0$ là" A. $2$ · B. $1$ · C. vô số · D. $0$. Đúng: D ($\Delta=5^2-4\cdot(-2)\cdot(-4)=-7<0$).
- Câu 4. "Hai nghiệm của phương trình $x^2-9x+8=0$ là" A. $-1$ và $-8$ · B. $1$ và $8$ · C. $1$ và $-8$ · D. $-1$ và $8$. Đúng: B ($a+b+c=1-9+8=0$ nên $x_1=1$, $x_2=8$).

PHẦN II. TỰ LUẬN (8,0 điểm):
- Câu 5 (1,0 điểm). Giải các phương trình: a) (0,5 điểm) $x^2-3x+2=0$, $a+b+c=0$ (hoặc $\Delta=1$) nên $x_1=1$, $x_2=2$. b) (0,5 điểm) $2x^2+5x+3=0$, $a-b+c=2-5+3=0$ (hoặc $\Delta=1$) nên $x_1=-1$, $x_2=-\dfrac32$.
- Câu 6 (1,0 điểm). "Cho phương trình $x^2+(m+1)x+2m-2=0$ với $m$ là tham số. Chứng minh rằng phương trình luôn có hai nghiệm $x_1$, $x_2$ với mọi $m$." Lời giải: $\Delta=(m+1)^2-4(2m-2)=m^2+2m+1-8m+8=m^2-6m+9=(m-3)^2\ge0$ với mọi $m$ nên phương trình luôn có hai nghiệm (có thể trùng nhau khi $m=3$).
- Câu 7 (1,5 điểm). "Cho phương trình bậc hai $4x^2+8x-15=0$." a) (0,5 điểm) "Chứng minh rằng phương trình có hai nghiệm phân biệt $x_1$, $x_2$." ($ac=4\cdot(-15)=-60<0$). b) (1,0 điểm) "Không giải phương trình, hãy tính giá trị biểu thức $M=x_1^2+x_2^2-5x_1x_2$." (Viète $x_1+x_2=-2$, $x_1x_2=-\dfrac{15}4$; $M=(x_1+x_2)^2-7x_1x_2=4+\dfrac{105}{4}=\dfrac{121}{4}$).
- Câu 8 (1,0 điểm). "Biết rằng phương trình bậc hai $x^2-ax-3=0$ có một nghiệm là $x_1=\dfrac{3+\sqrt{21}}{2}$.
  Tìm bình phương của hiệu hai nghiệm của phương trình trên."
  Lời giải (KHÔNG viết "$a=1, b=-a, c=-3$" vì $a$ là tham số của đề):
  phương trình có hệ số của $x^2$ là $1$ và hệ số tự do là $-3$, tích $1\cdot(-3)=-3<0$ nên có hai nghiệm phân biệt ·
  theo định lí Viète, tích hai nghiệm là $x_1x_2=-3$, nên
  $x_2=\dfrac{-3}{x_1}=\dfrac{-6}{3+\sqrt{21}}=\dfrac{-6(\sqrt{21}-3)}{21-9}=\dfrac{3-\sqrt{21}}{2}$ ·
  $x_1-x_2=\sqrt{21}$, nên $(x_1-x_2)^2=21$.
- Câu 9 (1,5 điểm). "Cho phương trình bậc hai $x^2-2x+m-1=0$ ($m$ là tham số)."
  a) (0,5 điểm) "Giải phương trình với $m=0$." ($x^2-2x-1=0$, $\Delta=8$, $x=1\pm\sqrt2$).
  b) (1,0 điểm) "Tìm $m$ để phương trình có hai nghiệm phân biệt $x_1$, $x_2$ thỏa mãn $\dfrac{3}{x_1x_2}-x_1-x_2=2$."
  ($\Delta=4-4(m-1)=8-4m>0$, tức $m<2$ · Viète $x_1+x_2=2$, $x_1x_2=m-1$ ·
  cần $x_1x_2\ne0$ nên $m\ne1$ · $\dfrac{3}{m-1}-2=2$, nên $m-1=\dfrac34$, tức $m=\dfrac74$, thỏa mãn $m<2$ và $m\ne1$).
- Câu 10 (1,0 điểm). Đề: "Một tổ sản xuất được giao nhiệm vụ hoàn thành $300$ sản phẩm trong một thời gian quy định.
  Khi thực hiện, tổ làm được nhiều hơn $5$ sản phẩm so với số sản phẩm dự định làm trong mỗi giờ theo kế hoạch.
  Tổ sản xuất đã hoàn thành công việc sớm hơn kế hoạch $2$ giờ. Hỏi theo kế hoạch, mỗi giờ tổ sản xuất làm bao nhiêu sản phẩm?"
  Lời giải: gọi $x$ (sản phẩm) là số sản phẩm mỗi giờ theo kế hoạch, $x\in\mathbb N^*$ ·
  thời gian kế hoạch $\dfrac{300}{x}$ (giờ), thực tế $\dfrac{300}{x+5}$ (giờ) · $\dfrac{300}{x}-\dfrac{300}{x+5}=2$ ·
  khử mẫu $300(x+5)-300x=2x(x+5)$, thu gọn được $x^2+5x-750=0$ ·
  $\Delta=25+3000=3025$, $\sqrt\Delta=55$ · $x_1=25$ (thỏa mãn), $x_2=-30$ (không thỏa mãn) · vậy mỗi giờ $25$ sản phẩm.
- Câu 11 (1,0 điểm). Đề: "Một đoàn xe vận tải dự định điều một số xe cùng loại để vận chuyển $40$ tấn hàng.
  Lúc sắp khởi hành, đoàn được giao thêm $14$ tấn nữa. Do đó phải điều thêm $2$ xe cùng loại trên và mỗi xe phải chở
  thêm $0{,}5$ tấn so với ban đầu. Tính số lượng xe dự định phải điều ban đầu. Biết rằng mỗi xe đều chở số lượng hàng
  như nhau và số xe ban đầu của đoàn không quá $15$ xe."
  Lời giải: gọi $x$ (xe) là số xe dự định, $x\in\mathbb N^*$, $x\le15$ ·
  mỗi xe dự định chở $\dfrac{40}{x}$ (tấn), thực tế $x+2$ xe chở $54$ tấn, mỗi xe $\dfrac{54}{x+2}$ (tấn) ·
  $\dfrac{54}{x+2}-\dfrac{40}{x}=\dfrac12$ · khử mẫu (mẫu chung $2x(x+2)$): $108x-80(x+2)=x(x+2)$,
  thu gọn được $x^2-26x+160=0$ · $\Delta=676-640=36$, $\sqrt\Delta=6$ · $x_1=16$, $x_2=10$ ·
  $x_1=16>15$ không thỏa mãn, $x_2=10$ thỏa mãn · vậy dự định điều $10$ xe.

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Đề chép ĐÚNG câu chữ trong ngoặc kép ở sơ đồ. Không văn nói, không xưng hô: cấm "em", "các em", "hôm nay", "Kiểm" (phải "Xét"/"Kiểm tra"), "Soi". Không viết tắt.
2. TUYỆT ĐỐI không dùng kí hiệu $S$, $P$ cho tổng, tích hai nghiệm — viết thẳng $x_1+x_2$, $x_1x_2$. KHÔNG dùng $\Delta'$, $b'$. KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$ trong lời giải: mỗi phép biến đổi xuống một dòng, nối bằng "nên".
3. Toán trong $…$; số thập phân viết $0{,}5$; phân số dùng \dfrac; KHÔNG dấu chấm phẩy ";" nối hai công thức (xuống dòng [[br]]). Giữ escape \% \& \#. JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi JSON).
4. Lời giải trình bày như bài thi, MỖI BƯỚC MỘT DÒNG ([[br]]), dừng đúng chỗ, theo khuôn các ví dụ của phiếu luyện tập (cuối prompt): bài có định lí Viète thì dòng xét $\Delta$ hoặc $ac$ trước → "Theo định lí Viète, ta có $x_1+x_2=…$, $x_1x_2=…$." → biến đổi → "Vậy …". Bài lời văn: gọi ẩn + đơn vị + điều kiện → biểu diễn các đại lượng → lập phương trình → giải → đối chiếu điều kiện → "Vậy …".
5. TỰ TÍNH LẠI mọi đáp số; thấy sơ đồ sai thì ghi vào "ghi_chu" (KHÔNG tự đổi số).
'''

VIEC_DE = r'''
## Việc của bạn: viết TỜ ĐỀ học sinh (không in đáp án)
Khuôn JSON: y như "Mẫu tờ đề" (đề kiểm tra chương X đã duyệt) cuối prompt. 5 chặng, "title" để RỖNG "", "teacher_note" để "".
- Chặng {"kind":"review","number":1}: para "\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \\textit{Mỗi câu 0,5 điểm. Chọn phương án đúng.}" rồi 4 problem Câu 1.–Câu 4.: "type":"problem","label":"Câu 1.","level":1,"tier":"onclass","dang_id":"NB1"…"NB4","statement": câu hỏi,"options": 4 chuỗi đúng thứ tự A–D của sơ đồ (không ghi "A."), "answer": chữ cái đúng.
- Chặng {"kind":"concept","number":2}: para "\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm).}" rồi problem "Câu 5." (level 1, dang_id "NB5"), statement "\\textbf{(1,0 điểm)} Giải các phương trình:[[br]]a) \\textbf{(0,5 điểm)} $…$[[br]]b) \\textbf{(0,5 điểm)} $…$", rồi problem "Câu 6." (level 2, dang_id "TH1").
- Chặng {"kind":"practice1","number":3}: problem "Câu 7." (level 2, dang_id "TH2", "\\textbf{(1,5 điểm)} Cho …[[br]]a) \\textbf{(0,5 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …"), problem "Câu 8." (level 2, dang_id "TH3"), problem "Câu 9." (level 3, dang_id "VD1", hai ý a, b có điểm như Câu 7).
- Chặng {"kind":"practice2","number":4}: problem "Câu 10." (level 2, dang_id "TH4") và problem "Câu 11." (level 3, dang_id "VD2"), statement mở đầu "\\textbf{(1,0 điểm)} Giải bài toán sau bằng cách lập phương trình: …".
- Chặng {"kind":"reflection","number":5}: para "\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}".
Không có "solution", không hình, không writelines, không thẻ [NB]/[TH]/[VD] trong statement.

## Đầu ra
JSON đúng schema: {"stages": [5 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC_DA = r'''
## Việc của bạn: viết ĐÁP ÁN + BAREM (tài liệu giáo viên)
Khuôn: y như các chặng 2–5 của "Mẫu đáp án" (đáp án kiểm tra chương X đã duyệt) cuối prompt — mỗi khối là "type":"para" với "text". Chặng 1 (ma trận) KHÔNG phải viết, máy tự sinh.
Mỗi bước chấm kết thúc bằng " \\hfill \\textit{(0,25đ)}" (bước 0,5 điểm thì "(0,5đ)"); TỔNG điểm các bước của mỗi ý PHẢI đúng bằng điểm của ý (Câu 5a 0,5 · 5b 0,5 · Câu 6 1,0 · 7a 0,5 · 7b 1,0 · Câu 8 1,0 · 9a 0,5 · 9b 1,0 · Câu 10 1,0 · Câu 11 1,0). Mỗi dòng một bước, ngăn bằng [[br]]. Câu có ý a, b thì ý b mở đầu bằng "[[br]]b)" (dòng mới bắt đầu bằng "b)").
Trả về đúng 4 chặng, "teacher_note" để "":
- {"kind":"concept","number":2,"title":"Đáp án Phần I, Câu 5 và Câu 6"}: para đáp án Phần I ("\\textbf{PHẦN I (2,0 điểm).} Mỗi câu đúng $0{,}5$ điểm.[[br]]\\textbf{1 – C} (lí do ngắn) …" — chữ cái PHẢI khớp sơ đồ: 1 – C, 2 – A, 3 – D, 4 – B), rồi para "\\textbf{Câu 5 (1,0 điểm).}[[br]]a) …", para "\\textbf{Câu 6 (1,0 điểm).}[[br]]…".
- {"kind":"practice1","number":3,"title":"Đáp án Câu 7, Câu 8 và Câu 9"}: mỗi câu một para mở đầu "\\textbf{Câu N (… điểm).}".
- {"kind":"practice2","number":4,"title":"Đáp án Câu 10 và Câu 11"}: mỗi câu một para.
- {"kind":"reflection","number":5,"title":"Biểu điểm tổng hợp"}: para tóm tắt điểm từng câu/ý (như mẫu), para "\\textbf{Tổng: 10,0 điểm.} Học sinh giải cách khác đúng vẫn cho điểm tối đa từng phần." + lỗi trừ điểm đặc thù chương này: thiếu bước xét $\Delta$ (hoặc $ac$) trước khi dùng định lí Viète trừ $0{,}25$đ; Câu 9b không đối chiếu điều kiện của $m$ (cả $m<2$ lẫn $m\ne1$) trừ $0{,}25$đ; bài lập phương trình không đối chiếu điều kiện của ẩn trừ $0{,}25$đ; thiếu câu "Vậy" trừ $0{,}25$đ mỗi bài; Câu 7b nếu học sinh giải phương trình ra nghiệm rồi thay số đúng chỉ cho tối đa $0{,}25$đ (do đề yêu cầu không giải phương trình); Câu 8 tìm $a$ rồi giải phương trình tính $(x_1-x_2)^2$ đúng vẫn cho đủ điểm.

## Đầu ra
JSON đúng schema: {"stages": [4 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''


def khuon_p5():
    d = json.loads((REPO / P5).read_text())
    out = []
    for s in d["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "noted" and b.get("variant") == "example":
                out.append(b["text"])
    return out[:5]


def main():
    loi = kiem()
    for l in loi:
        print("✗", l)
    if loi:
        sys.exit(1)
    print("SymPy SẠCH · điểm", sum(c[3] for c in SO_DO), "· phút", sum(c[4] for c in SO_DO))
    de = json.loads((REPO / MAU / "de-kiem-tra-chuong-x.json").read_text())
    da = json.loads((REPO / MAU / "ma-tran-va-dap-an-kiem-tra-chuong-x.json").read_text())
    f = "\n\n## Khuôn lời giải phiếu luyện tập (ví dụ của Phiếu 5 chương VI)\n" + "\n---\n".join(khuon_p5())
    for vid, phan, mau in (
        (VID_DE, VIEC_DE, "\n\n## Mẫu tờ đề (chương X, chỉ để xem khuôn — KHÔNG chép nội dung)\n" + json.dumps(de["stages"], ensure_ascii=False)),
        (VID_DA, VIEC_DA, "\n\n## Mẫu đáp án (chương X, chỉ để xem khuôn — KHÔNG chép nội dung)\n" + json.dumps(da["stages"][1:], ensure_ascii=False) + f),
    ):
        viec = {"id": vid, "model": "gemini-4-hydrogen-medium", "prompt": CHUNG + phan + mau,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1200s",
                "meta": {"loai": "de-kiem-tra", "seed_dich": f"{D}/kiem-tra-chuong/"}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
