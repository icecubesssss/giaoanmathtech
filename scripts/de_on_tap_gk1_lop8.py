#!/usr/bin/env python3
"""BỘ ĐỀ ÔN GK1 LỚP 8 (10/10/2026) — 3 đề ôn + 1 đề GK1 chính thức, theo đúng quy trình
docs/quy-trinh-bo-de-on-tap.md (bản mẫu: bộ đề lớp 9, scripts/de_on_tap_gk1_lop9_v2.py).

Sinh 4 đề HS + 4 file "Ma trận đề và đáp án chi tiết" vào inputs/seeds/lop-8/de-on-tap-giua-ki-1/
(theme de_thi, trinh_bay "thoang").

- Khung đề chốt từ LƯỚI DẠNG GẮN TAY 27 đề GK1 Hà Nội (inputs/refs/de-thi/lop-8/luoi-dang/gk1.json,
  thống kê: scripts/thong_ke_luoi_dang.py --lop 8): trắc nghiệm có ở 63% đề ⇒ giữ Phần I 2,0đ (8 câu);
  tìm x 89%, phép tính/rút gọn 81%, thực tế 67%, hình "tam giác vuông + hình chiếu ⇒ HCN ⇒ HBH" 70–78%.
- Phạm vi = tiến độ nội bộ T8 (GK1 tuần 16–17): Chương I, II (cả phân tích nhân tử) + trọn Chương III
  (đến hình thoi, hình vuông). KHÔNG dùng đường trung bình / Thalès (Chương IV) — đã loại 4 đề có câu đó.
- Mọi câu chép từ ẢNH đề gốc (inputs/refs/de-thi/lop-8/giua-ki-1/). Đáp số đã kiểm SymPy; toạ độ hình
  kiểm tính chất ở scripts/de_on_tap_gk1_lop8_hinh.py.
SỬA ĐỀ THÌ SỬA Ở ĐÂY rồi chạy lại — không sửa tay JSON (sửa tay sẽ bị ghi đè).

Chạy:  .venv/bin/python scripts/de_on_tap_gk1_lop8.py
       .venv/bin/python -m src.main build-folder inputs/seeds/lop-8/de-on-tap-giua-ki-1
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from de_on_tap_gk1_lop8_hinh import TOA_DO as T  # noqa: E402

OUT = Path("inputs/seeds/lop-8/de-on-tap-giua-ki-1")
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem)}đ)}}" if diem else "")


def y(nhan, diem, steps):
    than = BR.join(st(*s) if isinstance(s, tuple) else s for s in steps)
    return (f"\\textbf{{{nhan} ({d(diem)}đ)}}" + BR + than) if nhan else than


# ─────────────────────────── HÌNH ───────────────────────────
def hinh(pts, segs, extra="", scale=1.25, dashed=()):
    s = f"\\begin{{tikzpicture}}[scale={scale},line width=1pt]"
    for k, (xx, yy, pos) in pts.items():
        s += f"\\coordinate ({k}) at ({xx:.3f},{yy:.3f});"
    for a, b in segs:
        s += f"\\draw ({a})--({b});"
    for a, b in dashed:
        s += f"\\draw[dashed] ({a})--({b});"
    s += extra
    for k, (xx, yy, pos) in pts.items():
        s += f"\\fill ({k}) circle (1.6pt);\\node[{pos}] at ({k}) {{${k}$}};"
    return s + "\\end{tikzpicture}"


def vg(P, Q, R, s=0.17):
    """kí hiệu góc vuông tại Q (giữa QP và QR)"""
    (px, py), (qx, qy), (rx, ry) = P, Q, R
    u = (px - qx, py - qy); lu = math.hypot(*u); u = (u[0] / lu * s, u[1] / lu * s)
    v = (rx - qx, ry - qy); lv = math.hypot(*v); v = (v[0] / lv * s, v[1] / lv * s)
    return (f"\\draw[line width=0.5pt] ({qx+u[0]:.3f},{qy+u[1]:.3f})--({qx+u[0]+v[0]:.3f},{qy+u[1]+v[1]:.3f})"
            f"--({qx+v[0]:.3f},{qy+v[1]:.3f});")


def gach(P, Q, n=1, s=0.09):
    """n gạch nhỏ đánh dấu đoạn bằng nhau ở trung điểm PQ"""
    (px, py), (qx, qy) = P, Q
    mx, my = (px + qx) / 2, (py + qy) / 2
    ux, uy = qx - px, qy - py; l = math.hypot(ux, uy); ux, uy = ux / l, uy / l
    nx, ny = -uy * s, ux * s
    out = ""
    for i in range(n):
        o = (i - (n - 1) / 2) * 0.07
        cx, cy = mx + ux * o, my + uy * o
        out += f"\\draw[line width=0.6pt] ({cx-nx:.3f},{cy-ny:.3f})--({cx+nx:.3f},{cy+ny:.3f});"
    return out


c1 = {k: tuple(v) for k, v in T["on1"].items()}
HINH_ON1 = hinh({"A": (*c1["A"], "below left"), "B": (*c1["B"], "above"), "C": (*c1["C"], "below right"),
                 "H": (*c1["H"], "above right"), "M": (*c1["M"], "above right"), "D": (*c1["D"], "left"),
                 "E": (*c1["E"], "below"), "O": (*c1["O"], "left=2pt"), "Q": (*c1["Q"], "below=1pt"),
                 "K": (*c1["K"], "below")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("A", "M"), ("H", "D"), ("H", "E"), ("D", "E"),
                 ("H", "K")],
                extra=vg(c1["B"], c1["A"], c1["C"]) + vg(c1["A"], c1["H"], c1["C"]) + vg(c1["A"], c1["D"], c1["H"])
                + vg(c1["A"], c1["E"], c1["H"]) + gach(c1["A"], c1["E"], 2) + gach(c1["E"], c1["K"], 2), scale=1.75)
c2 = {k: tuple(v) for k, v in T["on2"].items()}
HINH_ON2 = hinh({"A": (*c2["A"], "below left"), "B": (*c2["B"], "above"), "C": (*c2["C"], "below right"),
                 "M": (*c2["M"], "above right"), "D": (*c2["D"], "above left"), "E": (*c2["E"], "above right"),
                 "F": (*c2["F"], "below"), "G": (*c2["G"], "left"), "O": (*c2["O"], "below=2pt"),
                 "H": (*c2["H"], "above right")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("G", "M"), ("M", "F"), ("D", "E"), ("A", "M"), ("A", "F"),
                 ("A", "G"), ("A", "H"), ("D", "H"), ("H", "E")],
                extra=vg(c2["B"], c2["A"], c2["C"]) + vg(c2["A"], c2["D"], c2["M"]) + vg(c2["A"], c2["E"], c2["M"])
                + vg(c2["A"], c2["H"], c2["C"]) + gach(c2["G"], c2["D"]) + gach(c2["D"], c2["M"]), scale=1.45)
c3 = {k: tuple(v) for k, v in T["on3"].items()}
HINH_ON3 = hinh({"A": (*c3["A"], "below left"), "B": (*c3["B"], "left"), "C": (*c3["C"], "below"),
                 "M": (*c3["M"], "right=2pt"), "D": (*c3["D"], "right"), "E": (*c3["E"], "left"),
                 "F": (*c3["F"], "below"), "N": (*c3["N"], "above"), "I": (*c3["I"], "below=2pt")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D"), ("D", "E"), ("D", "F"), ("E", "F"), ("N", "F"),
                 ("E", "N"), ("A", "N"), ("N", "D")],
                extra=vg(c3["B"], c3["A"], c3["C"]) + vg(c3["A"], c3["E"], c3["D"]) + vg(c3["A"], c3["F"], c3["D"])
                + vg(c3["E"], c3["N"], c3["F"]) + gach(c3["B"], c3["M"]) + gach(c3["M"], c3["C"]), scale=1.75)
c4 = {k: tuple(v) for k, v in T["gk"].items()}
HINH_GK = hinh({"A": (*c4["A"], "below left"), "B": (*c4["B"], "above"), "C": (*c4["C"], "below right"),
                "H": (*c4["H"], "above"), "M": (*c4["M"], "left"), "N": (*c4["N"], "below"),
                "I": (*c4["I"], "below=2pt"), "K": (*c4["K"], "right"), "O": (*c4["O"], "left=2pt"),
                "G": (*c4["G"], "below=2pt")},
               [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("M", "K"), ("H", "N"), ("M", "N"), ("A", "K"),
                ("C", "O"), ("K", "C")],
               extra=vg(c4["B"], c4["A"], c4["C"]) + vg(c4["A"], c4["H"], c4["C"]) + vg(c4["A"], c4["M"], c4["H"])
               + vg(c4["A"], c4["N"], c4["H"]) + gach(c4["H"], c4["I"]) + gach(c4["I"], c4["C"]), scale=1.4)

# Hình sân vận động (Văn Yên, Bài III) — lối đi rộng 3 m quanh sân
HINH_SAN = ("\\begin{tikzpicture}[line width=1pt,scale=0.9]"
            "\\draw (0,0) rectangle (3.6,5.0);\\fill[gray!35] (0.5,0.5) rectangle (3.1,4.5);"
            "\\draw (0.5,0.5) rectangle (3.1,4.5);\\draw[line width=0.6pt] (0.5,2.5)--(3.1,2.5);"
            "\\draw[line width=0.6pt] (1.8,2.5) circle (0.45);"
            "\\draw[<->,line width=0.6pt] (0,5.35)--(3.6,5.35);\\node[above] at (1.8,5.35) {$x-y$};"
            "\\draw[<->,line width=0.6pt] (4.75,0)--(4.75,5.0);\\node[right] at (4.75,2.5) {$x+y$};"
            "\\draw[<->,line width=0.5pt] (1.8,4.5)--(1.8,5.0);\\node[right,font=\\small] at (1.8,4.75) {$3$ m};"
            "\\draw[<->,line width=0.5pt] (0,1.3)--(0.5,1.3);\\node[left,font=\\small] at (0,1.3) {$3$ m};"
            "\\draw[<->,line width=0.5pt] (3.1,1.3)--(3.6,1.3);\\node[right,font=\\small] at (3.6,1.3) {$3$ m};"
            "\\draw[<->,line width=0.5pt] (1.8,0)--(1.8,0.5);\\node[right,font=\\small] at (1.8,0.25) {$3$ m};"
            "\\path (-3.2,0) (8.4,0);\\end{tikzpicture}")


def tn(cau, de, options, dap, giai, nd, ch, muc, nguon, level=1):
    return dict(cau=cau, de=de, options=options, dap=dap, giai=giai, nd=nd, ch=ch, muc=muc, nguon=nguon, level=level)


TN_DAU = ("\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \\textit{Mỗi câu 0,25 điểm. Chọn chữ cái đứng trước "
          "câu trả lời đúng rồi ghi vào bài làm (ví dụ: 1 -- A).}")
TL_DAU = "\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm)}"
HINH_DUNG = "\\textit{Vẽ hình đúng đến câu a.}"

# ─────────────────────────── ĐỀ ───────────────────────────
DE = {}

# ═══════════ ĐỀ ÔN 1 — các dạng tần suất cao nhất, bốc nguyên văn ═══════════
DE["on-1"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 1", slug_de="de-on-tap-giua-ki-1-so-1", slug_mt="ma-tran-va-dap-an-on-tap-so-1",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP SỐ 1", ngat=[("tn", 6), ("bai", 4)],
    cach_dung=("Cho HS làm như thi thật 90 phút, không gợi ý. Chữa ngay sau giờ: ưu tiên các ý mất điểm vì trình bày "
               "(quên đổi dấu khi bỏ ngoặc, thiếu câu kết luận, bài hình thiếu căn cứ). Ghi điểm từng bài vào phiếu "
               "theo dõi tiến bộ (file đáp án đề GK1)."),
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 1 -- GIỮA HỌC KÌ I TOÁN 8} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 6 bài tự luận)." + BR +
                "\\textbf{Khung đề:} lấy theo 27 đề GK1 Hà Nội (lưới dạng gắn tay, file Thong-ke-dang-GK1-Toan8-luoi-tay): "
                "trắc nghiệm có ở $63\\%$ số đề, tìm $x$ ở $89\\%$, thực hiện phép tính -- rút gọn $81\\%$, toán thực tế $67\\%$, "
                "bài hình ``tam giác vuông, hình chiếu $\\Rightarrow$ hình chữ nhật $\\Rightarrow$ hình bình hành'' $70$--$78\\%$." + BR +
                "\\textbf{Cách chọn câu:} Đề ôn 1 chỉ lấy các dạng tần suất cao nhất, mỗi câu chép \\textbf{nguyên văn} "
                "từ đề của trường (cột Nguồn). Phạm vi: Chương I, II (đa thức, hằng đẳng thức) và Chương III (tứ giác) -- "
                "không dùng câu có đường trung bình (Chương IV)."),
    tn=[
        tn(1, "Trong các biểu thức sau, đâu là đơn thức?", ["$5-2y$", "$-7x$", "$\\dfrac12x+3$", "$7x^2-2$"], "B",
           "$-7x$ là tích của một số với một biến.", "Nhận biết đơn thức", "ĐS I", "NB", "THCS Nguyễn Huy Tưởng"),
        tn(2, "Bậc của đa thức $M=y^7+x^3y^5-x^2y^4+9$ là", ["$8$", "$7$", "$9$", "$6$"], "A",
           "Hạng tử $x^3y^5$ có bậc $3+5=8$ cao nhất.", "Bậc của đa thức", "ĐS I", "NB", "THCS Tam Khương"),
        tn(3, "Kết quả của phép tính chia $x^3y^2:\\left(-3xy^2\\right)$ là:",
           ["$-3x^2$", "$-\\dfrac13x^2y$", "$-\\dfrac13x^2$", "$-3x^2y$"], "C",
           "$x^3y^2:\\left(-3xy^2\\right)=-\\dfrac13x^2$.", "Chia đơn thức cho đơn thức", "ĐS I", "NB", "THCS Tam Hiệp"),
        tn(4, "Tính $(3a-2)(3a+2)$ được kết quả:", ["$3a^2+4$", "$3a^2-4$", "$9a^2-4$", "$9a^2+4$"], "C",
           "Hiệu hai bình phương: $(3a)^2-2^2=9a^2-4$.", "Hằng đẳng thức hiệu hai bình phương", "ĐS II", "NB", "THCS Phan Đình Giót"),
        tn(5, "Tứ giác $ABCD$ có $\\widehat{A}=65^\\circ$, $\\widehat{B}=117^\\circ$, $\\widehat{C}=71^\\circ$. Số đo góc $D$ là",
           ["$119^\\circ$", "$107^\\circ$", "$63^\\circ$", "$126^\\circ$"], "B",
           "$\\widehat{D}=360^\\circ-65^\\circ-117^\\circ-71^\\circ=107^\\circ$.", "Tổng các góc của tứ giác", "HH III", "TH",
           "THCS Phú Diễn A", level=2),
        tn(6, "Chọn khẳng định \\textbf{sai}.",
           ["Tứ giác có hai cạnh đối song song là hình thang.", "Hình thang có hai góc kề một đáy bằng nhau là hình thang cân.",
            "Hình thang cân có hai cạnh bên bằng nhau.", "Hình thang có hai cạnh bên bằng nhau là hình thang cân."], "D",
           "Hình bình hành là hình thang có hai cạnh bên bằng nhau nhưng không phải hình thang cân.",
           "Dấu hiệu nhận biết hình thang cân", "HH III", "NB", "THCS Lê Lợi"),
        tn(7, "Nếu $ABCD$ là hình bình hành thì", ["$AC=BD$", "$AB=CD$", "$DC=AC$", "$AB=AD$"], "B",
           "Hình bình hành có các cạnh đối bằng nhau.", "Tính chất hình bình hành", "HH III", "NB", "THCS Nguyễn Trường Tộ"),
        tn(8, "Cho tam giác $ABC$ vuông tại $A$ có $BC=10$ cm, đường trung tuyến $AM$. Độ dài $AM$ là:",
           ["$10$ cm", "$8$ cm", "$20$ cm", "$5$ cm"], "D",
           "$\\triangle ABC$ vuông tại $A$, trung tuyến $AM$ $\\Rightarrow AM=\\dfrac{BC}{2}=5$ cm.",
           "Trung tuyến ứng với cạnh huyền", "HH III", "TH", "THCS Tam Hiệp", level=2),
    ],
    bai=[
        dict(label="Bài 1.", level=1,
             statement="\\textbf{(1,0 điểm)} Cho đa thức $A=5x^2y^3-4xy^2-3x^2y^3+4xy^2+3$." + BR +
             "a) Thu gọn đa thức $A$." + BR + "b) Tính giá trị của $A$ khi $x=-2$ và $y=1$.",
             dap_an=[
                 y("a)", 0.5, [("$A=(5x^2y^3-3x^2y^3)+(-4xy^2+4xy^2)+3$", 0.25), ("$A=2x^2y^3+3$.", 0.25)]),
                 y("b)", 0.5, [("Thay $x=-2$, $y=1$ vào $A$: $A=2\\cdot(-2)^2\\cdot 1^3+3$", 0.25),
                               ("$A=8+3=11$.", 0.25)]),
             ],
             mt=[("1a", "Thu gọn đa thức nhiều biến", "ĐS I", "NB", 0.5, 2, "THCS Bát Tràng"),
                 ("1b", "Tính giá trị của đa thức", "ĐS I", "NB", 0.5, 2, "THCS Bát Tràng")],
             note="Ý b: HS hay tính sai $(-2)^2$ thành $-4$; chấm 0,25 bước thay số."),
        dict(label="Bài 2.", level=2,
             statement="\\textbf{(1,5 điểm)} Rút gọn các biểu thức sau:" + BR +
             "a) $A=2x(x-y)+2y(x+y)-(x-y)(x+y)$;" + BR +
             "b) $B=(x-4)^2+(x+2)^2-2x(x-1)$;" + BR +
             "c) $C=(4-x)(4+x)+\\left(3x^4-6x^3+9x^2\\right):\\left(3x^2\\right)$.",
             dap_an=[
                 y("a)", 0.5, [("$A=2x^2-2xy+2xy+2y^2-\\left(x^2-y^2\\right)$", 0.25), ("$A=x^2+3y^2$.", 0.25)]),
                 y("b)", 0.5, [("$B=x^2-8x+16+x^2+4x+4-2x^2+2x$", 0.25), ("$B=-2x+20$.", 0.25)]),
                 y("c)", 0.5, [("$C=16-x^2+x^2-2x+3$", 0.25), ("$C=19-2x$.", 0.25)]),
             ],
             mt=[("2a", "Nhân đa thức, hiệu hai bình phương, rút gọn", "ĐS II", "TH", 0.5, 3, "THCS Nguyễn Du"),
                 ("2b", "Bình phương của một tổng, một hiệu; rút gọn", "ĐS II", "TH", 0.5, 3, "THCS Nguyễn Du"),
                 ("2c", "Chia đa thức cho đơn thức kết hợp hằng đẳng thức", "ĐS II", "TH", 0.5, 3, "THCS Nguyễn Du")],
             note="Lỗi hay gặp: bỏ ngoặc $-\\left(x^2-y^2\\right)$ quên đổi dấu $y^2$ (ý a), khai triển $-2x(x-1)$ sai dấu (ý b)."),
        dict(label="Bài 3.", level=2,
             statement="\\textbf{(1,0 điểm)} Tìm $x$, biết:" + BR +
             "a) $2(x-3)-4x=0$;" + BR + "b) $(3x+2)(2x-3)-(x-2)(3x+5)=4$.",
             dap_an=[
                 y("a)", 0.5, [("$2x-6-4x=0$"), ("$-2x=6$", 0.25), ("$x=-3$.", 0.25)]),
                 y("b)", 0.5, [("$6x^2-9x+4x-6-\\left(3x^2+5x-6x-10\\right)=4$"), ("$3x^2-4x+4=4$"),
                               ("$3x^2-4x=0$", 0.25), ("$x(3x-4)=0$"),
                               ("$x=0$ hoặc $x=\\dfrac43$. Vậy $x\\in\\left\\{0;\\dfrac43\\right\\}$.", 0.25)]),
             ],
             mt=[("3a", "Tìm $x$: bỏ ngoặc, chuyển vế", "ĐS I", "NB", 0.5, 2, "THCS Hoàng Hoa Thám"),
                 ("3b", "Tìm $x$: khai triển rồi đặt nhân tử chung", "ĐS II", "TH", 0.5, 5, "THCS Hoàng Hoa Thám")],
             note="Ý b: HS chia hai vế cho $x$ sẽ mất nghiệm $x=0$ -- chỉ cho 0,25đ."),
        dict(label="Bài 4.", level=3,
             statement="\\textbf{(1,0 điểm)} Ở một siêu thị bán hoa quả, giá của quả nho là $x$ đồng/kg và giá của quả dưa hấu là $y$ đồng/kg." + BR +
             "a) Viết biểu thức biểu thị số tiền bác Hoà mua $3$ chùm nho và $4$ quả dưa hấu. Biết mỗi chùm nho nặng $1{,}2$ kg, "
             "mỗi quả dưa hấu nặng $2$ kg." + BR +
             "b) Tính số tiền bác Hoà trả người bán hàng, biết giá của quả nho là $60\\,000$ đồng/kg và giá của dưa hấu là $25\\,000$ đồng/kg.",
             dap_an=[
                 y("a)", 0.5, [("Khối lượng nho: $3\\cdot 1{,}2=3{,}6$ (kg); khối lượng dưa hấu: $4\\cdot 2=8$ (kg).", 0.25),
                               ("Số tiền bác Hoà mua là: $3{,}6x+8y$ (đồng).", 0.25)]),
                 y("b)", 0.5, [("Thay $x=60\\,000$, $y=25\\,000$: $3{,}6\\cdot 60\\,000+8\\cdot 25\\,000=216\\,000+200\\,000$", 0.25),
                               ("$=416\\,000$ (đồng). Vậy bác Hoà trả $416\\,000$ đồng.", 0.25)]),
             ],
             mt=[("4a", "Viết biểu thức đại số biểu thị số tiền", "ĐS I", "VD", 0.5, 4, "THCS Tam Hiệp"),
                 ("4b", "Tính giá trị biểu thức trong tình huống thực tế", "ĐS I", "VD", 0.5, 3, "THCS Tam Hiệp")],
             note="Ý a: viết $3x+4y$ (quên nhân khối lượng) không cho điểm."),
        dict(label="Bài 5.", level=3, hinh_da=HINH_ON1,
             statement="\\textbf{(3,0 điểm)} Cho $\\triangle ABC$ có $\\widehat{A}=90^\\circ$, có $AH$ là đường cao, đường trung tuyến $AM$. "
             "Kẻ $HD$ vuông góc với $AB$ và $HE$ vuông góc với $AC$ ($D\\in AB$; $E\\in AC$). $DE$ cắt $AH$ ở $O$, $DE$ cắt $AM$ ở $Q$." + BR +
             "a) Tứ giác $ADHE$ là hình gì? Vì sao?" + BR +
             "b) Lấy điểm $K$ sao cho $E$ là trung điểm của $AK$. Chứng minh tứ giác $DHKE$ là hình bình hành." + BR +
             "c) Chứng minh $\\triangle AEQ$ vuông ở $Q$.",
             dap_an=[
                 HINH_DUNG + " \\hfill \\textit{(0,25đ)}",
                 y("a)", 1.0, [("Tứ giác $ADHE$ có $\\widehat{DAE}=90^\\circ$, $\\widehat{ADH}=90^\\circ$ ($HD\\perp AB$), "
                                "$\\widehat{AEH}=90^\\circ$ ($HE\\perp AC$)", 0.5),
                               ("$\\Rightarrow ADHE$ là hình chữ nhật (tứ giác có ba góc vuông).", 0.5)]),
                 y("b)", 1.0, [("$ADHE$ là hình chữ nhật $\\Rightarrow DH\\parallel AE$ và $DH=AE$.", 0.25),
                               ("$E$ là trung điểm của $AK$ $\\Rightarrow AE=EK$ và $K$ thuộc tia $AC$.", 0.25),
                               ("$\\Rightarrow DH\\parallel EK$ và $DH=EK$.", 0.25),
                               ("Tứ giác $DHKE$ có hai cạnh đối $DH$, $EK$ song song và bằng nhau nên $DHKE$ là hình bình hành.", 0.25)]),
                 y("c)", 0.75, [("Xét $\\triangle ABC$ vuông tại $A$, trung tuyến $AM$ $\\Rightarrow AM=\\dfrac{BC}{2}=MC$ "
                                 "$\\Rightarrow \\triangle AMC$ cân tại $M$ $\\Rightarrow \\widehat{MAC}=\\widehat{ACB}$.", 0.25),
                                ("$ADHE$ là hình chữ nhật nên hai đường chéo $AH$, $DE$ bằng nhau và cắt nhau tại trung điểm $O$ "
                                 "của mỗi đường $\\Rightarrow OA=OE$ $\\Rightarrow \\triangle OAE$ cân tại $O$ "
                                 "$\\Rightarrow \\widehat{OEA}=\\widehat{OAE}$, tức là $\\widehat{QEA}=\\widehat{HAC}$.", 0.25),
                                ("$\\triangle AHC$ vuông tại $H$ $\\Rightarrow \\widehat{HAC}+\\widehat{ACB}=90^\\circ$ "
                                 "$\\Rightarrow \\widehat{QEA}+\\widehat{QAE}=90^\\circ$."),
                                ("Xét $\\triangle AEQ$: $\\widehat{AQE}=180^\\circ-\\left(\\widehat{QEA}+\\widehat{QAE}\\right)=90^\\circ$. "
                                 "Vậy $\\triangle AEQ$ vuông ở $Q$.", 0.25)]),
             ],
             mt=[("5a", "Chứng minh hình chữ nhật (tứ giác có ba góc vuông)", "HH III", "NB", 1.25, 7, "THCS Tam Khương"),
                 ("5b", "Chứng minh hình bình hành (cặp cạnh đối song song và bằng nhau)", "HH III", "TH", 1.0, 9, "THCS Tam Khương"),
                 ("5c", "Góc vuông qua trung tuyến ứng với cạnh huyền và tính chất đường chéo hình chữ nhật", "HH III", "VDC", 0.75, 12, "THCS Tam Khương")],
             note="Điểm 5a gồm 0,25đ vẽ hình. Cùng cấu hình này có ở đề Tam Hiệp và Hoàng Hoa Thám 2025--2026 -- là cấu hình hay gặp nhất. "
                  "Ý c: HS chỉ ghi ``$\\widehat{QEA}=\\widehat{HAC}$'' mà không nêu $OA=OE$ thì trừ 0,25đ."),
        dict(label="Bài 6.", level=4,
             statement="\\textbf{(0,5 điểm)} Cho $x$, $y$ là các số thực thỏa mãn $x^2+y^2+xy-3x-3y+3=0$. "
             "Chứng minh biểu thức $P=(3x+2y-6)^{1010}+(x-y+1)^{1011}+2021$ có giá trị là một số nguyên.",
             dap_an=[
                 y("", 0.5, [("Nhân hai vế với $4$: $4x^2+4y^2+4xy-12x-12y+12=0$"),
                             ("$(2x+y-3)^2+3(y-1)^2=0$.", 0.25),
                             ("Mà $(2x+y-3)^2\\ge 0$, $3(y-1)^2\\ge 0$ nên $y-1=0$ và $2x+y-3=0$, tức là $x=y=1$."),
                             ("$P=(-1)^{1010}+1^{1011}+2021=2023$. Vậy $P$ là một số nguyên.", 0.25)]),
             ],
             mt=[("6", "Tổng các bình phương bằng $0$ $\\Rightarrow$ tìm $x$, $y$, tính giá trị", "ĐS II", "VDC", 0.5, 8, "THCS \\& THPT Lương Thế Vinh")],
             note="Khó nhất là tách $4x^2+4y^2+4xy-12x-12y+12=(2x+y-3)^2+3(y-1)^2$; HS tìm đúng $x=y=1$ bằng cách khác vẫn cho đủ điểm."),
    ],
)

# ═══════════ ĐỀ ÔN 2 — giữ dạng, nâng một nấc ═══════════
DE["on-2"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 2", slug_de="de-on-tap-giua-ki-1-so-2", slug_mt="ma-tran-va-dap-an-on-tap-so-2",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP SỐ 2",
    cach_dung=("Làm như thi thật 90 phút. Đề 2 cùng dạng với Đề 1 nhưng mỗi bài nâng một nấc: hằng đẳng thức bậc ba, "
               "tìm $x$ đưa về tích, bài thực tế hai bước, bài hình có ý ``trung tuyến bằng nửa cạnh $\\Rightarrow$ góc vuông''. "
               "So điểm từng bài với Đề 1 để biết HS đã vững dạng chưa."),
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 2 -- GIỮA HỌC KÌ I TOÁN 8} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 6 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} giữ nguyên khung và các dạng tần suất cao của Đề 1, chép nguyên văn từ trường khác, "
                "chọn câu khó hơn một nấc: hằng đẳng thức lập phương ($41\\%$ số đề có rút gọn bằng hằng đẳng thức), "
                "chứng minh biểu thức không phụ thuộc biến ($22\\%$), tìm $x$ dùng hằng đẳng thức ($56\\%$), "
                "câu cuối ba ẩn ``tổng bình phương bằng $0$'' ($48\\%$)."),
    tn=[
        tn(1, "Hai đơn thức \\textbf{không} đồng dạng là:",
           ["$9xy^3$ và $xy^3$", "$8x^4y$ và $8xy^4$", "$15xy$ và $-xy$", "$2025$ và $2026$"], "B",
           "$8x^4y$ và $8xy^4$ có phần biến khác nhau.", "Đơn thức đồng dạng", "ĐS I", "NB", "THCS Chúc Sơn"),
        tn(2, "Bậc của đơn thức $0{,}35xy^2z^4$ là:", ["$6$", "$7$", "$0{,}35$", "$4$"], "B",
           "Bậc là $1+2+4=7$.", "Bậc của đơn thức", "ĐS I", "NB", "THCS Nguyễn Du"),
        tn(3, "Đa thức $7x^3y^2z-2x^4y^3$ chia hết cho đơn thức nào sau đây?",
           ["$3x^4$", "$-3x^4$", "$-2x^3y$", "$2xy^3$"], "C",
           "Số mũ của $x$, $y$ trong $-2x^3y$ không vượt quá số mũ tương ứng ở mọi hạng tử.",
           "Đa thức chia hết cho đơn thức", "ĐS I", "TH", "THCS Phú Diễn A", level=2),
        tn(4, "Khai triển hằng đẳng thức $(x-2y)^3$ ta được",
           ["$x^3+6x^2y+12xy^2+8y^3$", "$x^3-6x^2y+12xy^2-8y^3$", "$x^3-6x^2y+6xy^2-2y^3$", "$x^3-6x^2y+6xy^2-8y^3$"], "B",
           "$(x-2y)^3=x^3-3x^2\\cdot 2y+3x\\cdot 4y^2-8y^3$.", "Lập phương của một hiệu", "ĐS II", "NB", "THCS Nguyễn Trường Tộ"),
        tn(5, "Cho tứ giác $ABCD$ có $\\widehat{A}+\\widehat{B}=140^\\circ$. Khi đó $\\widehat{C}+\\widehat{D}$ bằng",
           ["$200^\\circ$", "$220^\\circ$", "$160^\\circ$", "$130^\\circ$"], "B",
           "$\\widehat{C}+\\widehat{D}=360^\\circ-140^\\circ=220^\\circ$.", "Tổng các góc của tứ giác", "HH III", "TH", "THCS Bát Tràng", level=2),
        tn(6, "Hình bình hành cần thêm điều kiện nào sau đây để thành hình thoi?",
           ["Hai cạnh đối bằng nhau.", "Hai đường chéo bằng nhau.", "Hai đường chéo vuông góc.", "Hai cạnh đối song song."], "C",
           "Hình bình hành có hai đường chéo vuông góc là hình thoi.", "Dấu hiệu nhận biết hình thoi", "HH III", "NB", "THCS Đỗ Ngọc Du"),
        tn(7, "Trong các khẳng định sau, khẳng định \\textbf{sai} là:",
           ["Tứ giác có hai cạnh đối song song và bằng nhau là hình bình hành.", "Hình thang có hai cạnh bên song song là hình bình hành.",
            "Hình thang có hai đường chéo bằng nhau là hình bình hành.",
            "Tứ giác có hai đường chéo cắt nhau tại trung điểm của mỗi đường là hình bình hành."], "C",
           "Hình thang có hai đường chéo bằng nhau là hình thang cân.", "Dấu hiệu nhận biết hình bình hành", "HH III", "NB", "THCS Nguyễn Khê"),
        tn(8, "Cho tam giác $ABC$ vuông tại đỉnh $A$ và trung tuyến $AM$ thỏa mãn $\\widehat{AMC}=110^\\circ$, khi đó số đo $\\widehat{ACB}$ là:",
           ["$35^\\circ$", "$55^\\circ$", "$65^\\circ$", "$70^\\circ$"], "A",
           "$AM=\\dfrac{BC}{2}=MC$ $\\Rightarrow\\triangle AMC$ cân tại $M$ $\\Rightarrow\\widehat{ACB}=\\dfrac{180^\\circ-110^\\circ}{2}=35^\\circ$.",
           "Trung tuyến ứng với cạnh huyền, tam giác cân", "HH III", "VD", "THCS Giảng Võ", level=3),
    ],
    bai=[
        dict(label="Bài 1.", level=2,
             statement="\\textbf{(1,0 điểm)} Cho hai đa thức $A=-x^2-4xy^2z+z^2$; $B=2xy^2z+x^2-z^2$." + BR +
             "a) Hãy tính $M=A+B$." + BR + "b) Tìm đa thức $N$ biết $N:2z^2=M$." + BR +
             "c) Tính giá trị của $N$ khi $x=1$; $y=-3$; $z=-1$.",
             dap_an=[
                 y("a)", 0.5, [("$M=\\left(-x^2+x^2\\right)+\\left(-4xy^2z+2xy^2z\\right)+\\left(z^2-z^2\\right)$", 0.25),
                               ("$M=-2xy^2z$.", 0.25)]),
                 y("b)", 0.25, [("$N=M\\cdot 2z^2=-2xy^2z\\cdot 2z^2=-4xy^2z^3$.", 0.25)]),
                 y("c)", 0.25, [("$N=-4\\cdot 1\\cdot(-3)^2\\cdot(-1)^3=36$.", 0.25)]),
             ],
             mt=[("1a", "Cộng hai đa thức nhiều biến", "ĐS I", "NB", 0.5, 2, "THCS Chu Văn An"),
                 ("1b", "Tìm đa thức bị chia (nhân đơn thức)", "ĐS I", "TH", 0.25, 2, "THCS Chu Văn An"),
                 ("1c", "Tính giá trị của đa thức", "ĐS I", "TH", 0.25, 2, "THCS Chu Văn An")],
             note="Ý b: HS lấy $M:2z^2$ (nhầm chiều) không cho điểm. Ý c: dấu của $(-1)^3$."),
        dict(label="Bài 2.", level=2,
             statement="\\textbf{(1,5 điểm)}" + BR +
             "a) Rút gọn biểu thức $P=(1-2x)(5-3x)+(4-x)^2$." + BR +
             "b) Rút gọn biểu thức $Q=(x+1)^3-(x-4)(x+4)-x^3$." + BR +
             "c) Chứng minh giá trị của biểu thức sau không phụ thuộc vào giá trị của biến: "
             "$A=(x-2y)\\left(x^2+2xy+4y^2\\right)-\\left(x^3-8y^3+15\\right)$.",
             dap_an=[
                 y("a)", 0.5, [("$P=5-3x-10x+6x^2+16-8x+x^2$", 0.25), ("$P=7x^2-21x+21$.", 0.25)]),
                 y("b)", 0.5, [("$Q=x^3+3x^2+3x+1-\\left(x^2-16\\right)-x^3$", 0.25), ("$Q=2x^2+3x+17$.", 0.25)]),
                 y("c)", 0.5, [("$A=x^3-8y^3-x^3+8y^3-15$", 0.25),
                               ("$A=-15$. Vậy giá trị của $A$ không phụ thuộc vào giá trị của biến.", 0.25)]),
             ],
             mt=[("2a", "Nhân đa thức, bình phương của một hiệu", "ĐS II", "TH", 0.5, 3, "THCS Văn Khê"),
                 ("2b", "Lập phương của một tổng, hiệu hai bình phương", "ĐS II", "TH", 0.5, 3, "THCS Văn Khê"),
                 ("2c", "Hiệu hai lập phương: chứng minh không phụ thuộc biến", "ĐS II", "VD", 0.5, 4, "THCS Bát Tràng")],
             note="Ý c: HS nhân phá ngoặc từng hạng tử vẫn đúng nhưng dài; nhận ra hiệu hai lập phương là nhanh nhất."),
        dict(label="Bài 3.", level=3,
             statement="\\textbf{(1,0 điểm)} Tìm $x$, biết:" + BR +
             "a) $(x+1)^3-(3x+1)(2x-2)=x^3+7x-9$;" + BR + "b) $(3x-1)^2-(2x+1)^2=0$.",
             dap_an=[
                 y("a)", 0.5, [("$x^3+3x^2+3x+1-\\left(6x^2-4x-2\\right)=x^3+7x-9$"), ("$-3x^2+7x+3=7x-9$"),
                               ("$3x^2=12$", 0.25), ("$x^2-4=0$"), ("$(x-2)(x+2)=0$"),
                               ("$x=2$ hoặc $x=-2$. Vậy $x\\in\\{2;-2\\}$.", 0.25)]),
                 y("b)", 0.5, [("$(3x-1-2x-1)(3x-1+2x+1)=0$"), ("$(x-2)\\cdot 5x=0$", 0.25),
                               ("$x=2$ hoặc $x=0$. Vậy $x\\in\\{0;2\\}$.", 0.25)]),
             ],
             mt=[("3a", "Tìm $x$: lập phương của một tổng, đưa về hiệu hai bình phương", "ĐS II", "VD", 0.5, 5, "THCS Ba Đình"),
                 ("3b", "Tìm $x$: hiệu hai bình phương bằng $0$", "ĐS II", "TH", 0.5, 3, "THCS Nguyễn Du")],
             note="Ý a: HS ra $x^2=4$ rồi chỉ ghi $x=2$ (thiếu $x=-2$) trừ 0,25đ."),
        dict(label="Bài 4.", level=3,
             statement="\\textbf{(1,0 điểm)} Một sân vận động hình chữ nhật có chiều dài là $(x+y)$ mét và chiều rộng là $(x-y)$ mét. "
             "Người ta làm lối đi rộng $3$ mét xung quanh sân, phần còn lại để trồng cỏ (phần tô đậm trên hình) nhằm phục vụ cho các trận bóng đá.",
             figure=dict(tikz=HINH_SAN, pos="below", rong_da="0.32"),
             sau_hinh="a) Viết biểu thức tính diện tích của sân vận động." + BR +
             "b) Viết biểu thức tính diện tích phần trồng cỏ." + BR +
             "c) Cho $x=40$, $y=6$. Biết $1\\ \\text{m}^2$ trồng cỏ cần số tiền là $100\\,000$ đồng. Tính số tiền trồng cỏ cho mặt sân.",
             dap_an=[
                 y("a)", 0.25, [("Diện tích sân vận động: $(x+y)(x-y)=x^2-y^2\\ (\\text{m}^2)$.", 0.25)]),
                 y("b)", 0.5, [("Phần trồng cỏ là hình chữ nhật có chiều dài $x+y-6$ (m), chiều rộng $x-y-6$ (m).", 0.25),
                               ("Diện tích phần trồng cỏ: $(x+y-6)(x-y-6)=x^2-12x-y^2+36\\ (\\text{m}^2)$.", 0.25)]),
                 y("c)", 0.25, [("Với $x=40$, $y=6$: diện tích trồng cỏ là $40\\cdot 28=1120\\ (\\text{m}^2)$; "
                                 "số tiền là $1120\\cdot 100\\,000=112\\,000\\,000$ (đồng).", 0.25)]),
             ],
             mt=[("4a", "Viết biểu thức diện tích (hiệu hai bình phương)", "ĐS II", "TH", 0.25, 2, "THCS Văn Yên"),
                 ("4b", "Viết biểu thức diện tích phần còn lại", "ĐS II", "VD", 0.5, 4, "THCS Văn Yên"),
                 ("4c", "Tính giá trị, tính tiền", "ĐS I", "VD", 0.25, 2, "THCS Văn Yên")],
             note="Ý b: lối đi bao quanh nên mỗi chiều giảm $2\\cdot 3=6$ m; HS chỉ trừ $3$ m không cho điểm ý b."),
        dict(label="Bài 5.", level=3, hinh_da=HINH_ON2, rong_da="0.6",
             statement="\\textbf{(3,0 điểm)} Cho tam giác $ABC$ vuông tại $A$ $(AB<AC)$, lấy điểm $M$ bất kỳ thuộc $BC$ ($M$ khác $B$; $M$ khác $C$). "
             "Kẻ $MD$ vuông góc với $AB$ tại $D$, $ME$ vuông góc với $AC$ tại $E$." + BR +
             "a) Chứng minh tứ giác $ADME$ là hình chữ nhật." + BR +
             "b) Qua $A$ kẻ tia $Ax$ song song với $DE$; $Ax$ cắt tia $ME$ tại $F$. Trên tia $MD$ lấy điểm $G$ sao cho $D$ là trung điểm của $MG$. "
             "Chứng minh tứ giác $ADEF$ là hình bình hành và $A$ là trung điểm của đoạn thẳng $GF$." + BR +
             "c) $AM$ cắt $DE$ tại $O$, kẻ đường cao $AH$ của tam giác $ABC$. Tính số đo góc $DHE$.",
             dap_an=[
                 HINH_DUNG + " \\hfill \\textit{(0,25đ)}",
                 y("a)", 1.0, [("Tứ giác $ADME$ có $\\widehat{DAE}=90^\\circ$, $\\widehat{ADM}=90^\\circ$ ($MD\\perp AB$), "
                                "$\\widehat{AEM}=90^\\circ$ ($ME\\perp AC$)", 0.5),
                               ("$\\Rightarrow ADME$ là hình chữ nhật (tứ giác có ba góc vuông).", 0.5)]),
                 y("b)", 1.0, [("$ME\\perp AC$, $AB\\perp AC$ $\\Rightarrow ME\\parallel AB$ $\\Rightarrow EF\\parallel AD$. "
                                "Lại có $AF\\parallel DE$ nên tứ giác $ADEF$ là hình bình hành.", 0.25),
                               ("$\\Rightarrow AF\\parallel DE$ và $AF=DE$.", 0.25),
                               ("$ADME$ là hình chữ nhật $\\Rightarrow DM=AE$; $D$ là trung điểm của $MG$ $\\Rightarrow GD=DM=AE$. "
                                "Lại có $GD\\parallel AE$ (cùng vuông góc với $AB$) nên tứ giác $AGDE$ là hình bình hành "
                                "$\\Rightarrow AG\\parallel DE$ và $AG=DE$.", 0.25),
                               ("Qua $A$ có $AG$, $AF$ cùng song song với $DE$ nên $G$, $A$, $F$ thẳng hàng; lại có $AG=AF$ ($=DE$). "
                                "Vậy $A$ là trung điểm của $GF$.", 0.25)]),
                 y("c)", 0.75, [("$ADME$ là hình chữ nhật nên hai đường chéo $AM$, $DE$ bằng nhau và cắt nhau tại trung điểm $O$ "
                                 "của mỗi đường.", 0.25),
                                ("Xét $\\triangle AHM$ vuông tại $H$, trung tuyến $HO$ $\\Rightarrow HO=\\dfrac{AM}{2}=\\dfrac{DE}{2}$.", 0.25),
                                ("$\\triangle DHE$ có $HO$ là đường trung tuyến ($O$ là trung điểm của $DE$) và $HO=\\dfrac{DE}{2}$ "
                                 "nên $\\triangle DHE$ vuông tại $H$. Vậy $\\widehat{DHE}=90^\\circ$.", 0.25)]),
             ],
             mt=[("5a", "Chứng minh hình chữ nhật (tứ giác có ba góc vuông)", "HH III", "NB", 1.25, 7, "THCS Nguyễn Du"),
                 ("5b", "Chứng minh hình bình hành; chứng minh trung điểm qua hai hình bình hành", "HH III", "VD", 1.0, 11, "THCS Nguyễn Du"),
                 ("5c", "Trung tuyến bằng nửa cạnh $\\Rightarrow$ tam giác vuông", "HH III", "VDC", 0.75, 12, "THCS Nguyễn Du")],
             note="Điểm 5a gồm 0,25đ vẽ hình. Trường hợp $M\\equiv H$ thì $\\widehat{DHE}=\\widehat{DME}=90^\\circ$ ngay. "
                  "Ý b: HS chứng minh $AG=AF$ mà không nêu $G$, $A$, $F$ thẳng hàng thì chỉ cho 0,25đ ý cuối."),
        dict(label="Bài 6.", level=4,
             statement="\\textbf{(0,5 điểm)} Cho $a$, $b$, $c$ thỏa mãn đồng thời $a+b+c=6$ và $a^2+b^2+c^2=12$. "
             "Tính giá trị của biểu thức $P=(a-3)^{2023}+(b-3)^{2024}+(c-3)^{2025}$.",
             dap_an=[
                 y("", 0.5, [("$(a-2)^2+(b-2)^2+(c-2)^2=a^2+b^2+c^2-4(a+b+c)+12=12-24+12=0$.", 0.25),
                             ("Mà $(a-2)^2\\ge 0$, $(b-2)^2\\ge 0$, $(c-2)^2\\ge 0$ nên $a=b=c=2$."),
                             ("$P=(-1)^{2023}+(-1)^{2024}+(-1)^{2025}=-1+1-1=-1$.", 0.25)]),
             ],
             mt=[("6", "Tổng ba bình phương bằng $0$ (ba ẩn) $\\Rightarrow$ tính giá trị", "ĐS II", "VDC", 0.5, 8, "THCS Ba Đình")],
             note="Mấu chốt là thêm bớt để có $(a-2)^2+(b-2)^2+(c-2)^2$; nâng một nấc so với câu hai ẩn ở Đề 1."),
    ],
)

# ═══════════ ĐỀ ÔN 3 — các dạng tần suất thứ nhì, mở rộng ═══════════
DE["on-3"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 3", slug_de="de-on-tap-giua-ki-1-so-3", slug_mt="ma-tran-va-dap-an-on-tap-so-3",
    eyebrow="LỚP 8 • ĐỀ ÔN TẬP SỐ 3", ngat=[("bai", 4)],
    cach_dung=("Làm như thi thật 90 phút. Đề 3 đổi sang các dạng ít gặp hơn nhưng vẫn có trong đề trường "
               "(tìm đa thức chưa biết, chia hết, tính nhanh bằng hằng đẳng thức, hình vuông, tối ưu thực tế) -- "
               "để HS không bị bất ngờ khi đề GK1 rơi vào dạng thứ nhì."),
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 3 -- GIỮA HỌC KÌ I TOÁN 8} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 6 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} các dạng tần suất \\textbf{thứ nhì} trong lưới 27 đề: tìm đa thức chưa biết, "
                "tính nhanh bằng hằng đẳng thức ($19\\%$), chia hết với mọi $n$, toán thực tế quãng đường, "
                "hình vuông -- hình thoi ($15\\%$), câu cuối tối ưu thực tế ($27\\%$ đề 2025--2026). "
                "Câu mở rộng ghi ``(mở rộng)'' ở cột Nội dung."),
    tn=[
        tn(1, "Trong các biểu thức sau, biểu thức nào \\textbf{không} là đơn thức?",
           ["$(x+1)y$", "$2x^2\\left(-\\dfrac12\\right)y$", "$x^2zt$", "$0$"], "A",
           "$(x+1)y=xy+y$ là tổng hai đơn thức.", "Nhận biết đơn thức", "ĐS I", "NB", "THCS Lê Lợi"),
        tn(2, "Đa thức $x^3y^5-x^{3-m}y^2$ chia hết cho đơn thức $x^3y^2$. Số tự nhiên $m$ cần tìm là:",
           ["$3$", "$2$", "$1$", "$0$"], "D",
           "Cần $3-m\\ge 3$ nên $m=0$.", "Điều kiện đa thức chia hết cho đơn thức (mở rộng)", "ĐS I", "VD", "THCS Đỗ Ngọc Du", level=3),
        tn(3, "Biểu thức $(x-2)\\left(x^2+2x+a\\right)$ là hiệu hai lập phương khi $a$ bằng",
           ["$4$", "$-4$", "$2$", "$-2$"], "A",
           "$x^3-8=(x-2)\\left(x^2+2x+4\\right)$.", "Hiệu hai lập phương", "ĐS II", "TH", "THCS Chúc Sơn", level=2),
        tn(4, "Giá trị của biểu thức $x\\left(x^2-2y\\right)+y(2x-1)$ tại $x=10$, $y=-1$ là:",
           ["$101$", "$1001$", "$999$", "$99$"], "B",
           "Rút gọn được $x^3-y=1000+1=1001$.", "Rút gọn rồi tính giá trị", "ĐS I", "TH", "THCS Giảng Võ", level=2),
        tn(5, "Chọn phương án \\textbf{đúng} trong các phương án sau:",
           ["Hình bình hành là hình chữ nhật.", "Hình chữ nhật vừa là hình bình hành, vừa là hình thang cân.",
            "Trong hình bình hành có hai đường chéo vuông góc.",
            "Hình bình hành có đường chéo là tia phân giác của một góc là hình chữ nhật."], "B",
           "Hình chữ nhật có các cạnh đối song song, hai đường chéo bằng nhau.", "Quan hệ giữa các tứ giác đặc biệt", "HH III", "TH", "THCS Bát Tràng", level=2),
        tn(6, "Tứ giác có hai đường chéo vuông góc với nhau tại trung điểm của mỗi đường là:",
           ["Hình bình hành", "Hình chữ nhật", "Hình thoi", "Hình vuông"], "C",
           "Hai đường chéo cắt nhau tại trung điểm mỗi đường $\\Rightarrow$ hình bình hành; vuông góc $\\Rightarrow$ hình thoi.",
           "Dấu hiệu nhận biết hình thoi", "HH III", "NB", "THCS Tam Hiệp"),
        tn(7, "Cho hình bình hành $ABCD$ có chu vi bằng $30$ cm, biết chu vi của tam giác $ACD$ bằng $22$ cm. Độ dài đường chéo $AC$ bằng",
           ["$7$ cm", "$8$ cm", "$19$ cm", "$4$ cm"], "A",
           "$AD+DC=15$ cm $\\Rightarrow AC=22-15=7$ cm.", "Tính chất cạnh đối hình bình hành (mở rộng)", "HH III", "VD", "THCS Chúc Sơn", level=3),
        tn(8, "Cho hình bình hành $ABCD$ có $\\widehat{A}=50^\\circ$. Khi đó:",
           ["$\\widehat{C}=50^\\circ$", "$\\widehat{B}=50^\\circ$", "$\\widehat{D}=120^\\circ$", "$\\widehat{C}=120^\\circ$"], "A",
           "Hình bình hành có các góc đối bằng nhau.", "Tính chất góc hình bình hành", "HH III", "NB", "THCS Phan Đình Giót"),
    ],
    bai=[
        dict(label="Bài 1.", level=2,
             statement="\\textbf{(1,0 điểm)} Tìm đa thức $A$, $D$ biết:" + BR +
             "a) $A+x^2(x+1)=x(x+2)+\\left(x^3-2x+2\\right)$;" + BR + "b) $3ab^2-b^2-D=-b^2+2ab^2-5$.",
             dap_an=[
                 y("a)", 0.5, [("$A=x(x+2)+x^3-2x+2-x^2(x+1)$"), ("$A=x^2+2x+x^3-2x+2-x^3-x^2$", 0.25), ("$A=2$.", 0.25)]),
                 y("b)", 0.5, [("$D=3ab^2-b^2-\\left(-b^2+2ab^2-5\\right)$", 0.25), ("$D=ab^2+5$.", 0.25)]),
             ],
             mt=[("1a", "Tìm đa thức chưa biết (mở rộng: kết hợp nhân đơn thức)", "ĐS I", "TH", 0.5, 3, "THCS Vạn Phúc (Hà Đông)"),
                 ("1b", "Tìm đa thức là số trừ", "ĐS I", "TH", 0.5, 2, "THCS Vạn Phúc (Hà Đông)")],
             note="Ý b: $D$ là số trừ nên $D=(3ab^2-b^2)-(-b^2+2ab^2-5)$; HS lấy hiệu ngược chiều không cho điểm."),
        dict(label="Bài 2.", level=3,
             statement="\\textbf{(1,5 điểm)}" + BR +
             "a) Tính giá trị biểu thức $A=x^3+6x^2+12x+8$ tại $x=8$." + BR +
             "b) Chứng minh rằng $(2n+3)^2-(2n-1)^2$ chia hết cho $8$ với mọi $n\\in\\mathbb{Z}$." + BR +
             "c) Chứng minh giá trị của biểu thức sau không phụ thuộc vào biến $x$: $B=(2x+3)^2+(2x+5)^2-2(2x+3)(2x+5)$.",
             dap_an=[
                 y("a)", 0.5, [("$A=x^3+3\\cdot x^2\\cdot 2+3\\cdot x\\cdot 2^2+2^3=(x+2)^3$.", 0.25),
                               ("Tại $x=8$: $A=10^3=1000$.", 0.25)]),
                 y("b)", 0.5, [("$(2n+3)^2-(2n-1)^2=(2n+3-2n+1)(2n+3+2n-1)=4(4n+2)$", 0.25),
                               ("$=8(2n+1)$ chia hết cho $8$ với mọi $n\\in\\mathbb{Z}$.", 0.25)]),
                 y("c)", 0.5, [("$B=\\left[(2x+3)-(2x+5)\\right]^2$", 0.25),
                               ("$B=(-2)^2=4$. Vậy giá trị của $B$ không phụ thuộc vào biến $x$.", 0.25)]),
             ],
             mt=[("2a", "Tính giá trị bằng hằng đẳng thức lập phương", "ĐS II", "TH", 0.5, 3, "THCS Chuyên Mỹ"),
                 ("2b", "Hiệu hai bình phương: chứng minh chia hết (mở rộng)", "ĐS II", "VD", 0.5, 4, "THCS Phú Diễn A"),
                 ("2c", "Bình phương của một hiệu: không phụ thuộc biến", "ĐS II", "VD", 0.5, 4, "THCS Vạn Phúc (Thanh Trì)")],
             note="Ý c: khai triển hết rồi rút gọn vẫn đủ điểm. Ý b: phải viết thành $8\\cdot(\\ldots)$ mới kết luận được."),
        dict(label="Bài 3.", level=2,
             statement="\\textbf{(1,0 điểm)} Tìm $x$, biết:" + BR +
             "a) $x^2-10x=-25$;" + BR + "b) $(x-3)\\left(x^2+3x+9\\right)=x\\left(x^2-8\\right)$.",
             dap_an=[
                 y("a)", 0.5, [("$x^2-10x+25=0$"), ("$(x-5)^2=0$", 0.25), ("$x=5$.", 0.25)]),
                 y("b)", 0.5, [("$x^3-27=x^3-8x$", 0.25), ("$8x=27$"), ("$x=\\dfrac{27}{8}$.", 0.25)]),
             ],
             mt=[("3a", "Tìm $x$: đưa về bình phương của một hiệu", "ĐS II", "TH", 0.5, 3, "THCS Lê Lợi"),
                 ("3b", "Tìm $x$: hiệu hai lập phương", "ĐS II", "TH", 0.5, 4, "THCS Nguyễn Trường Tộ")],
             note="Ý a: HS chuyển vế thành $x^2-10x+25=0$ nhưng không nhận ra $(x-5)^2$ thì chỉ cho 0,25đ khi có kết quả đúng."),
        dict(label="Bài 4.", level=3,
             statement="\\textbf{(1,0 điểm)} Một xe khách đi từ Quảng Ninh lên Hà Nội với vận tốc $(9x+15)$ km/h trong thời gian $(x-2)$ giờ." + BR +
             "a) Viết biểu thức đại số tính quãng đường Quảng Ninh -- Hà Nội theo $x$." + BR +
             "b) Tính quãng đường Quảng Ninh -- Hà Nội khi $x=5$.",
             dap_an=[
                 y("a)", 0.5, [("Quãng đường $=$ vận tốc $\\cdot$ thời gian $=(9x+15)(x-2)$", 0.25),
                               ("$=9x^2-3x-30$ (km).", 0.25)]),
                 y("b)", 0.5, [("Với $x=5$: $9\\cdot 5^2-3\\cdot 5-30=180$.", 0.25),
                               ("Vậy quãng đường Quảng Ninh -- Hà Nội dài $180$ km.", 0.25)]),
             ],
             mt=[("4a", "Viết biểu thức quãng đường (nhân hai đa thức)", "ĐS I", "VD", 0.5, 4, "THCS Phú Diễn A"),
                 ("4b", "Tính giá trị biểu thức trong tình huống thực tế", "ĐS I", "VD", 0.5, 3, "THCS Phú Diễn A")],
             note="Ý b: tính theo $(9\\cdot 5+15)(5-2)=60\\cdot 3$ cũng được."),
        dict(label="Bài 5.", level=3, hinh_da=HINH_ON3,
             statement="\\textbf{(3,0 điểm)} Cho $\\triangle ABC$ vuông cân tại $A$. Gọi $M$ là trung điểm của $BC$. "
             "Trên tia đối của tia $MA$ lấy điểm $D$ bất kì. Từ $D$ kẻ các đường thẳng vuông góc với $AB$, $AC$ lần lượt tại $E$, $F$." + BR +
             "a) Chứng minh $AEDF$ là hình vuông." + BR +
             "b) Chứng minh $EF\\parallel BC$." + BR +
             "c) Qua $E$ kẻ đường thẳng vuông góc với $MF$ tại $N$. Chứng minh $\\widehat{AND}=90^\\circ$.",
             dap_an=[
                 HINH_DUNG + " \\hfill \\textit{(0,25đ)}",
                 y("a)", 1.0, [("Tứ giác $AEDF$ có $\\widehat{EAF}=90^\\circ$, $\\widehat{AED}=90^\\circ$, $\\widehat{AFD}=90^\\circ$ "
                                "$\\Rightarrow AEDF$ là hình chữ nhật.", 0.25),
                               ("$\\triangle ABC$ cân tại $A$, $AM$ là đường trung tuyến nên $AM$ cũng là đường phân giác của $\\widehat{BAC}$.", 0.25),
                               ("$D$ thuộc tia $AM$ nên $AD$ là phân giác của $\\widehat{EAF}$. Hình chữ nhật $AEDF$ có đường chéo $AD$ "
                                "là phân giác của một góc nên $AEDF$ là hình vuông.", 0.5)]),
                 y("b)", 1.0, [("$AEDF$ là hình vuông nên hai đường chéo vuông góc: $EF\\perp AD$.", 0.5),
                               ("$\\triangle ABC$ cân tại $A$, $AM$ là đường trung tuyến nên $AM$ cũng là đường cao: $BC\\perp AD$.", 0.25),
                               ("$EF$ và $BC$ cùng vuông góc với $AD$ nên $EF\\parallel BC$.", 0.25)]),
                 y("c)", 0.75, [("Gọi $I$ là giao điểm của $AD$ và $EF$. $AEDF$ là hình vuông nên $AD=EF$ và $I$ là trung điểm của $AD$, $EF$.", 0.25),
                                ("Xét $\\triangle ENF$ vuông tại $N$, trung tuyến $NI$ $\\Rightarrow NI=\\dfrac{EF}{2}=\\dfrac{AD}{2}$.", 0.25),
                                ("$\\triangle AND$ có $NI$ là đường trung tuyến ($I$ là trung điểm của $AD$) và $NI=\\dfrac{AD}{2}$ "
                                 "nên $\\triangle AND$ vuông tại $N$. Vậy $\\widehat{AND}=90^\\circ$.", 0.25)]),
             ],
             mt=[("5a", "Chứng minh hình vuông (hình chữ nhật có đường chéo là phân giác)", "HH III", "TH", 1.25, 8, "THCS Nguyễn Huy Tưởng"),
                 ("5b", "Chứng minh song song qua tính chất đường chéo hình vuông", "HH III", "TH", 1.0, 8, "THCS Nguyễn Huy Tưởng"),
                 ("5c", "Góc vuông qua trung tuyến bằng nửa cạnh (mở rộng: thêm giao điểm $I$)", "HH III", "VDC", 0.75, 12, "THCS Nguyễn Huy Tưởng")],
             note="Điểm 5a gồm 0,25đ vẽ hình. Ý c: $N$ có thể nằm trên phần kéo dài của đoạn $MF$ -- lời giải không phụ thuộc vị trí đó."),
        dict(label="Bài 6.", level=4,
             statement="\\textbf{(0,5 điểm)} Một nông trại nghiên cứu việc trồng cây ăn quả trên mỗi $100\\ \\text{m}^2$ đất. "
             "Người ta thấy rằng nếu trồng $n$ cây trên $100\\ \\text{m}^2$ thì trung bình mỗi cây sẽ cho năng suất $P(n)=100-2n$ (kg/cây). "
             "Hỏi các bác nông dân nên trồng bao nhiêu cây trên $100\\ \\text{m}^2$ để tổng sản lượng thu hoạch trái cây là lớn nhất?",
             dap_an=[
                 y("", 0.5, [("Tổng sản lượng: $S=n(100-2n)=-2n^2+100n=1250-2\\left(n^2-50n+625\\right)=1250-2(n-25)^2$.", 0.25),
                             ("Vì $(n-25)^2\\ge 0$ nên $S\\le 1250$; dấu ``$=$'' xảy ra khi $n=25$."),
                             ("Vậy nên trồng $25$ cây trên $100\\ \\text{m}^2$, tổng sản lượng lớn nhất là $1250$ kg.", 0.25)]),
             ],
             mt=[("6", "Tối ưu thực tế: đưa về $m-a(x-b)^2$", "ĐS II", "VDC", 0.5, 8, "THCS Chu Văn An")],
             note="Đây là dạng câu cuối mới nổi ($27\\%$ đề 2025--2026). Không dùng công thức đỉnh parabol (lớp 10)."),
    ],
)

# ═══════════ ĐỀ GK1 CHÍNH THỨC — câu trường khác, chưa xuất hiện ở 3 đề ôn ═══════════
DE["gk1"] = dict(
    ten="ĐỀ CHÍNH THỨC", slug_de="de-kiem-tra-giua-ki-1-chinh-thuc", slug_mt="ma-tran-va-dap-an-giua-ki-1-chinh-thuc",
    eyebrow="LỚP 8 • ĐỀ CHÍNH THỨC", ngat=[("tn", 6), ("bai", 4)],
    cach_dung=("Thi như thật 90 phút, không gợi ý. Đề đo lại đúng các dạng của 3 đề ôn bằng câu của trường khác "
               "(đánh giá vì sự tiến bộ: HS đã thành thạo dạng chưa, chứ không đo trí nhớ). Ghi điểm từng bài vào phiếu theo dõi ở cuối file."),
    gioi_thieu=("\\textbf{ĐỀ KIỂM TRA GIỮA HỌC KÌ I TOÁN 8 -- ĐỀ CHÍNH THỨC} (90 phút -- Thang điểm 10 -- 8 câu trắc nghiệm, 6 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} giữ đúng khung của 3 đề ôn; mỗi bài lấy câu của trường \\textbf{chưa dùng} cho bài đó ở 3 đề ôn "
                "(cùng dạng, khác trường) để đo năng lực thật. Mức độ tương đương Đề ôn 2."),
    tn=[
        tn(1, "Kết quả của phép tính $2x^2y+3xy^2-\\left(2xy^2-3x^2y\\right)$ là:",
           ["$6x^2y$", "$5x^2y+xy^2$", "$-x^2y+xy^2$", "$xy^2$"], "B",
           "$2x^2y+3x^2y+3xy^2-2xy^2=5x^2y+xy^2$.", "Cộng, trừ đa thức", "ĐS I", "TH", "THCS \\& THPT Lương Thế Vinh", level=2),
        tn(2, "Bậc của đơn thức $5x^3y^4$ là:", ["$3$", "$4$", "$5$", "$7$"], "D",
           "Bậc là $3+4=7$.", "Bậc của đơn thức", "ĐS I", "NB", "THCS Nguyễn Huy Tưởng"),
        tn(3, "Kết quả của phép chia $\\left(-28x^4y^2+14x^4y\\right):\\left(7x^3y\\right)$ là:",
           ["$-4x+2xy$", "$4xy-2x$", "$-4xy+2$", "$-4xy+2x$"], "D",
           "$-28x^4y^2:7x^3y=-4xy$; $14x^4y:7x^3y=2x$.", "Chia đa thức cho đơn thức", "ĐS I", "TH", "THCS Giảng Võ", level=2),
        tn(4, "Khẳng định nào sau đây là đúng?",
           ["$(x+1)\\left(x^2+x+1\\right)=x^3+1$", "$(x+2)^2=x^2+2x+4$", "$(x-3)^2=x^2+6x+9$", "$(x-2y)(x+2y)=x^2-4y^2$"], "D",
           "Hiệu hai bình phương.", "Nhận biết hằng đẳng thức", "ĐS II", "NB", "THCS Nguyễn Trường Tộ"),
        tn(5, "Cho tứ giác $ABCD$ có $\\widehat{A}=\\widehat{B}=100^\\circ$, $\\widehat{C}=60^\\circ$. Khi đó số đo $\\widehat{D}$ là:",
           ["$100^\\circ$", "$60^\\circ$", "$160^\\circ$", "$50^\\circ$"], "A",
           "$\\widehat{D}=360^\\circ-100^\\circ-100^\\circ-60^\\circ=100^\\circ$.", "Tổng các góc của tứ giác", "HH III", "TH", "THCS Nguyễn Khê", level=2),
        tn(6, "Khẳng định nào sau đây là đúng?",
           ["Hình thang có $2$ cạnh đối bằng nhau là hình thang cân.", "Hình thang có $2$ góc kề một đáy bằng nhau là hình thang cân.",
            "Hình thang cân là tứ giác có $2$ cạnh bên bằng nhau.", "Hình thang cân là tứ giác có $2$ đường chéo bằng nhau."], "B",
           "Định nghĩa hình thang cân.", "Dấu hiệu nhận biết hình thang cân", "HH III", "NB", "THCS Phú Diễn A"),
        tn(7, "Hình bình hành $ABCD$ là hình chữ nhật khi",
           ["$AB=AD$", "$\\widehat{D}=90^\\circ$", "$AB=2AC$", "$\\widehat{A}=\\widehat{C}$"], "B",
           "Hình bình hành có một góc vuông là hình chữ nhật.", "Dấu hiệu nhận biết hình chữ nhật", "HH III", "NB", "THCS Nguyễn Khê"),
        tn(8, "Tứ giác có hai cạnh đối song song và hai đường chéo bằng nhau là:",
           ["Hình thang cân", "Hình bình hành", "Hình chữ nhật", "Hình thoi"], "A",
           "Hình thang có hai đường chéo bằng nhau là hình thang cân.", "Dấu hiệu nhận biết hình thang cân", "HH III", "TH", "THCS Đỗ Ngọc Du", level=2),
    ],
    bai=[
        dict(label="Bài 1.", level=1,
             statement="\\textbf{(1,0 điểm)} Cho các đa thức $A=x^3y^2+4y^2-x^2y$; $B=3x^2y+5y^2+2x^3y^2$." + BR +
             "a) Tìm tổng $A+B$." + BR + "b) Tìm đa thức $C$ sao cho $C+B=A$.",
             dap_an=[
                 y("a)", 0.5, [("$A+B=\\left(x^3y^2+2x^3y^2\\right)+\\left(-x^2y+3x^2y\\right)+\\left(4y^2+5y^2\\right)$", 0.25),
                               ("$A+B=3x^3y^2+2x^2y+9y^2$.", 0.25)]),
                 y("b)", 0.5, [("$C=A-B=x^3y^2+4y^2-x^2y-3x^2y-5y^2-2x^3y^2$", 0.25),
                               ("$C=-x^3y^2-4x^2y-y^2$.", 0.25)]),
             ],
             mt=[("1a", "Cộng hai đa thức nhiều biến", "ĐS I", "NB", 0.5, 2, "THCS Nguyễn Trường Tộ"),
                 ("1b", "Tìm đa thức chưa biết", "ĐS I", "TH", 0.5, 3, "THCS Nguyễn Trường Tộ")],
             note="Ý b: $C=A-B$; dấu từng hạng tử của $B$ phải đổi khi bỏ ngoặc."),
        dict(label="Bài 2.", level=2,
             statement="\\textbf{(1,5 điểm)}" + BR +
             "a) Thực hiện phép tính: $\\left(12x^2y-8xy^2+xy\\right):(4xy)$." + BR +
             "b) Thực hiện phép tính: $(x+2y)\\left(x^2+3y^2\\right)$." + BR +
             "c) Chứng minh rằng giá trị của biểu thức sau không phụ thuộc vào giá trị của biến $x$ và $y$: "
             "$E=(2x-y)^2+(3x+y)^2+2(2x-y)(3x+y)-25(1+x)(x-1)$.",
             dap_an=[
                 y("a)", 0.5, [("$=12x^2y:4xy-8xy^2:4xy+xy:4xy$", 0.25), ("$=3x-2y+\\dfrac14$.", 0.25)]),
                 y("b)", 0.5, [("$=x^3+3xy^2+2x^2y+6y^3$.", 0.5)]),
                 y("c)", 0.5, [("$E=\\left[(2x-y)+(3x+y)\\right]^2-25\\left(x^2-1\\right)=(5x)^2-25x^2+25$", 0.25),
                               ("$E=25$. Vậy giá trị của $E$ không phụ thuộc vào giá trị của biến $x$ và $y$.", 0.25)]),
             ],
             mt=[("2a", "Chia đa thức cho đơn thức", "ĐS I", "NB", 0.5, 2, "THCS Nguyễn Công Trứ"),
                 ("2b", "Nhân đa thức với đa thức", "ĐS I", "TH", 0.5, 3, "THCS Nguyễn Công Trứ"),
                 ("2c", "Bình phương của một tổng, hiệu hai bình phương: không phụ thuộc biến", "ĐS II", "VD", 0.5, 5, "THCS \\& THPT Lương Thế Vinh")],
             note="Ý c: nhận ra $(2x-y)^2+2(2x-y)(3x+y)+(3x+y)^2=(5x)^2$ là then chốt; khai triển hết vẫn đủ điểm."),
        dict(label="Bài 3.", level=2,
             statement="\\textbf{(1,0 điểm)} Tìm $x$, biết:" + BR +
             "a) $x(3x-2)-9x^3:3x=4$;" + BR + "b) $(x-2)(4x-1)-(2x-3)(2x+3)=29$.",
             dap_an=[
                 y("a)", 0.5, [("Điều kiện $x\\ne 0$. $3x^2-2x-3x^2=4$", 0.25), ("$-2x=4$"), ("$x=-2$ (thỏa mãn).", 0.25)]),
                 y("b)", 0.5, [("$4x^2-x-8x+2-\\left(4x^2-9\\right)=29$", 0.25), ("$-9x+11=29$"), ("$x=-2$.", 0.25)]),
             ],
             mt=[("3a", "Tìm $x$: nhân, chia đơn thức rồi chuyển vế", "ĐS I", "TH", 0.5, 3, "THCS Nguyễn Công Trứ"),
                 ("3b", "Tìm $x$: khai triển, hiệu hai bình phương", "ĐS II", "TH", 0.5, 4, "THCS Nguyễn Huy Tưởng")],
             note="Ý a: phép chia $9x^3:3x$ cần $x\\ne 0$; HS không ghi điều kiện vẫn cho đủ điểm nếu kết quả đúng."),
        dict(label="Bài 4.", level=3,
             statement="\\textbf{(1,0 điểm)} Một mảnh vườn hình chữ nhật có chiều dài là $x$ (m), chiều rộng là $y$ (m)." + BR +
             "a) Viết đa thức biểu thị diện tích mảnh vườn." + BR +
             "b) Nếu tăng chiều dài $2$ m, giảm chiều rộng $3$ m thì được mảnh vườn mới. Viết đa thức biểu thị diện tích mảnh vườn mới "
             "và tính diện tích mới nếu $x=10$ (m) và $y=4$ (m).",
             dap_an=[
                 y("a)", 0.25, [("Diện tích mảnh vườn là $xy\\ (\\text{m}^2)$.", 0.25)]),
                 y("b)", 0.75, [("Mảnh vườn mới có chiều dài $x+2$ (m), chiều rộng $y-3$ (m).", 0.25),
                                ("Diện tích mảnh vườn mới: $(x+2)(y-3)=xy-3x+2y-6\\ (\\text{m}^2)$.", 0.25),
                                ("Với $x=10$, $y=4$: $10\\cdot 4-3\\cdot 10+2\\cdot 4-6=12\\ (\\text{m}^2)$.", 0.25)]),
             ],
             mt=[("4a", "Viết biểu thức diện tích", "ĐS I", "NB", 0.25, 1, "THCS Đỗ Ngọc Du"),
                 ("4b", "Viết đa thức diện tích mới (nhân hai đa thức) và tính giá trị", "ĐS I", "VD", 0.75, 6, "THCS Đỗ Ngọc Du")],
             note="Ý b: viết $(x+2)(y-3)$ chưa khai triển vẫn cho 0,25đ thứ hai."),
        dict(label="Bài 5.", level=3, hinh_da=HINH_GK,
             statement="\\textbf{(3,0 điểm)} Cho $\\triangle ABC$ vuông tại $A$ có $AB<AC$, đường cao $AH$. Từ $H$ kẻ $HM\\perp AB$ $(M\\in AB)$. "
             "Kẻ $HN\\perp AC$ $(N\\in AC)$. Gọi $I$ là trung điểm của $HC$. Tia $MH$ cắt tia $AI$ tại $K$." + BR +
             "a) Tứ giác $AMHN$ là hình gì? Vì sao?" + BR +
             "b) Chứng minh tứ giác $AHKC$ là hình bình hành." + BR +
             "c) $MN$ cắt $AH$ tại $O$, $CO$ cắt $AK$ tại $G$. Chứng minh $AK=3AG$.",
             dap_an=[
                 HINH_DUNG + " \\hfill \\textit{(0,25đ)}",
                 y("a)", 1.0, [("Tứ giác $AMHN$ có $\\widehat{MAN}=90^\\circ$, $\\widehat{AMH}=90^\\circ$ ($HM\\perp AB$), "
                                "$\\widehat{ANH}=90^\\circ$ ($HN\\perp AC$)", 0.5),
                               ("$\\Rightarrow AMHN$ là hình chữ nhật (tứ giác có ba góc vuông).", 0.5)]),
                 y("b)", 1.0, [("$AMHN$ là hình chữ nhật $\\Rightarrow MH\\parallel AN$ $\\Rightarrow HK\\parallel AC$.", 0.25),
                               ("Xét $\\triangle IHK$ và $\\triangle ICA$: $\\widehat{HIK}=\\widehat{CIA}$ (đối đỉnh), $IH=IC$ ($I$ là trung điểm của $HC$), "
                                "$\\widehat{IHK}=\\widehat{ICA}$ (so le trong, $HK\\parallel AC$)", 0.25),
                               ("$\\Rightarrow\\triangle IHK=\\triangle ICA$ (g.c.g) $\\Rightarrow IK=IA$.", 0.25),
                               ("Tứ giác $AHKC$ có hai đường chéo $AK$, $HC$ cắt nhau tại trung điểm $I$ của mỗi đường "
                                "nên $AHKC$ là hình bình hành.", 0.25)]),
                 y("c)", 0.75, [("$AMHN$ là hình chữ nhật nên hai đường chéo $MN$, $AH$ cắt nhau tại trung điểm $O$ của mỗi đường "
                                 "$\\Rightarrow O$ là trung điểm của $AH$.", 0.25),
                                ("$\\triangle AHC$ có hai đường trung tuyến $CO$, $AI$ cắt nhau tại $G$ $\\Rightarrow G$ là trọng tâm "
                                 "$\\Rightarrow AG=\\dfrac23 AI$.", 0.25),
                                ("Mà $IK=IA$ nên $AK=2AI$ $\\Rightarrow AG=\\dfrac23\\cdot\\dfrac{AK}{2}=\\dfrac{AK}{3}$. Vậy $AK=3AG$.", 0.25)]),
             ],
             mt=[("5a", "Chứng minh hình chữ nhật (tứ giác có ba góc vuông)", "HH III", "NB", 1.25, 7, "THCS Phan Đình Giót"),
                 ("5b", "Chứng minh hình bình hành (hai đường chéo cắt nhau tại trung điểm)", "HH III", "TH", 1.0, 10, "THCS Phan Đình Giót"),
                 ("5c", "Trọng tâm tam giác kết hợp đường chéo hình chữ nhật, hình bình hành", "HH III", "VDC", 0.75, 12, "THCS Phan Đình Giót")],
             note="Điểm 5a gồm 0,25đ vẽ hình. Ý c dùng trọng tâm tam giác (lớp 7): HS không nêu ``$O$ là trung điểm của $AH$'' thì không có cơ sở gọi $CO$ là trung tuyến -- trừ 0,25đ."),
        dict(label="Bài 6.", level=4,
             statement="\\textbf{(0,5 điểm)} Cho $a^2+b^2+c^2=ab+bc+ca$ và $a+b+c=2022$. Tính $a$, $b$, $c$.",
             dap_an=[
                 y("", 0.5, [("Nhân hai vế với $2$: $2a^2+2b^2+2c^2-2ab-2bc-2ca=0$"),
                             ("$(a-b)^2+(b-c)^2+(c-a)^2=0$.", 0.25),
                             ("Mà mỗi bình phương đều không âm nên $a-b=0$, $b-c=0$, $c-a=0$, tức là $a=b=c$."),
                             ("Kết hợp $a+b+c=2022$: $3a=2022$. Vậy $a=b=c=674$.", 0.25)]),
             ],
             mt=[("6", "Tổng các bình phương bằng $0$ $\\Rightarrow$ $a=b=c$", "ĐS II", "VDC", 0.5, 7, "THCS Phú Diễn A")],
             note="Cùng dạng câu cuối của Đề ôn 1, 2 (tổng bình phương bằng $0$) -- dạng câu cuối hay gặp nhất ($48\\%$ số đề)."),
    ],
)

# Bản đồ dạng qua 4 đề (in ở file đáp án đề GK1)
TIEN_BO = [
    ["Phần I (8 câu)", "Đơn thức, bậc, chia, HĐT; góc tứ giác; HTC, HBH; trung tuyến", "Đồng dạng, chia hết, lập phương; HBH $\\to$ thoi; trung tuyến + tam giác cân",
     "Điều kiện chia hết, tính giá trị; HCN, thoi; chu vi HBH", "Cộng đa thức, chia, HĐT; góc; HTC, HCN"],
    ["Bài 1 -- đa thức", "Thu gọn, tính giá trị (Bát Tràng)", "Cộng đa thức, tìm $N$ (Chu Văn An)", "Tìm đa thức chưa biết (Vạn Phúc)",
     "Cộng, tìm $C$ (Nguyễn Trường Tộ)"],
    ["Bài 2 -- phép tính, HĐT", "Rút gọn bằng HĐT bậc hai (Nguyễn Du)", "HĐT lập phương; không phụ thuộc biến (Văn Khê, Bát Tràng)",
     "Tính nhanh, chia hết, không phụ thuộc biến", "Chia, nhân; không phụ thuộc biến (NCT, LTV)"],
    ["Bài 3 -- tìm $x$", "Chuyển vế; đặt nhân tử chung (Hoàng Hoa Thám)", "Lập phương; hiệu hai bình phương", "Bình phương một hiệu; hiệu hai lập phương",
     "Chia đơn thức; hiệu hai bình phương"],
    ["Bài 4 -- thực tế", "Tiền mua hoa quả (Tam Hiệp)", "Diện tích sân cỏ (Văn Yên)", "Quãng đường (Phú Diễn A)", "Diện tích vườn mới (Đỗ Ngọc Du)"],
    ["Bài 5 -- hình", "HCN $\\to$ HBH $\\to$ góc vuông (Tam Khương)", "HCN $\\to$ HBH, trung điểm $\\to$ góc vuông (Nguyễn Du)",
     "Hình vuông $\\to$ song song $\\to$ góc vuông (Nguyễn Huy Tưởng)", "HCN $\\to$ HBH $\\to$ trọng tâm (Phan Đình Giót)"],
    ["Bài 6 -- câu cuối", "Tổng bình phương hai ẩn (LTV)", "Tổng bình phương ba ẩn (Ba Đình)", "Tối ưu thực tế (Chu Văn An)",
     "Tổng bình phương, $a=b=c$ (Phú Diễn A)"],
]

# ─────────────────────────── NGUỒN: RẢI TRƯỜNG / QUẬN ───────────────────────────
# Quận/huyện CŨ (trước 7/2025) — khớp inputs/refs/de-thi/lop-8/luoi-dang/gk1.json.
# Luật (docs/quy-trinh-bo-de-on-tap.md): mỗi đề >= 4 quận và không quận nào quá 40% điểm đề;
# cả bộ 4 đề không quận nào quá 25%, không trường nào quá 15% tổng điểm.
QUAN = {
    "THCS Nguyễn Huy Tưởng": "Đông Anh", "THCS Tam Khương": "Đống Đa", "THCS Tam Hiệp": "Thanh Trì",
    "THCS Phan Đình Giót": "Thanh Xuân", "THCS Phú Diễn A": "Bắc Từ Liêm", "THCS Lê Lợi": "Hà Đông",
    "THCS Nguyễn Trường Tộ": "Đống Đa", "THCS Bát Tràng": "Gia Lâm", "THCS Nguyễn Du": "Hoàn Kiếm",
    "THCS Hoàng Hoa Thám": "Ba Đình", "THCS \\& THPT Lương Thế Vinh": "Cầu Giấy", "THCS Chúc Sơn": "Chương Mỹ",
    "THCS Đỗ Ngọc Du": "Thanh Trì", "THCS Nguyễn Khê": "Đông Anh", "THCS Giảng Võ": "Ba Đình",
    "THCS Chu Văn An": "Hoàng Mai", "THCS Văn Khê": "Hà Đông", "THCS Ba Đình": "Ba Đình", "THCS Văn Yên": "Hà Đông",
    "THCS Vạn Phúc (Hà Đông)": "Hà Đông", "THCS Chuyên Mỹ": "Phú Xuyên", "THCS Vạn Phúc (Thanh Trì)": "Thanh Trì",
    "THCS Nguyễn Công Trứ": "Ba Đình",
}


def dong_mt(D):
    """mọi dòng ma trận của đề: 8 câu TN + các ý tự luận, dạng (câu, nội dung, chương, mức, điểm, phút, nguồn)"""
    rows = [(f"TN{c['cau']}", c["nd"], c["ch"], c["muc"], 0.25, 1.5, c["nguon"]) for c in D["tn"]]
    return rows + [r for b in D["bai"] for r in b["mt"]]


def kiem_nguon():
    from collections import defaultdict
    tq, tt, bao_cao = defaultdict(float), defaultdict(float), {}
    for k, D in DE.items():
        q = defaultdict(float)
        for r in dong_mt(D):
            q[QUAN[r[6]]] += r[4]; tq[QUAN[r[6]]] += r[4]; tt[r[6]] += r[4]
        assert len(q) >= 4, (k, dict(q))
        assert max(q.values()) <= 4.0 + 1e-9, (k, dict(q))
        truong = {r[6] for r in dong_mt(D)}
        bao_cao[k] = (len(truong), q)
    assert max(tq.values()) <= 10.0 + 1e-9, dict(tq)
    assert max(tt.values()) <= 6.0 + 1e-9, dict(tt)
    return bao_cao, tq


def kiem_diem():
    """tổng điểm = 10; điểm từng ý trong đáp án (\\hfill (xđ)) cộng đúng bằng điểm ý trong ma trận"""
    import re
    for k, D in DE.items():
        assert len(D["tn"]) == 8, k
        assert abs(sum(r[4] for r in dong_mt(D)) - 10) < 1e-9, k
        for b in D["bai"]:
            tong_mt = sum(r[4] for r in b["mt"])
            tong_da = 0.0
            for a in b["dap_an"]:
                tong_da += sum(float(m.replace(",", ".")) for m in re.findall(r"\\hfill \\textit\{\(([\d,]+)đ\)\}", a))
            assert abs(tong_mt - tong_da) < 1e-9, (k, b["label"], tong_mt, tong_da)
        assert "Leftrightarrow" not in json.dumps(D), k


kiem_diem()
NGUON, NGUON_BO = kiem_nguon()
for _k, (_n, _q) in NGUON.items():
    print(_k, _n, "trường,", len(_q), "quận:", ", ".join(f"{a} {d(v)}" for a, v in sorted(_q.items(), key=lambda t: -t[1])))

# ─────────────────────────── DỰNG JSON ───────────────────────────
KIND = ["review", "concept", "practice1", "practice2", "reflection"]
# 5 chặng của khung: Phần I | Bài 1, 2 | Bài 3, 4 | Bài 5 (hình) | Bài 6
NHOM_BAI = [[], [0, 1], [2, 3], [4], [5]]


def bang_mt(rows, tieu_de):
    s = ("\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.12}\n"
         "\\begin{tabular}{|c|p{5.3cm}|c|c|c|c|p{3.4cm}|}\n\\hline\n"
         f"\\multicolumn{{7}}{{|l|}}{{\\textbf{{{tieu_de}}}}} \\\\ \\hline\n"
         "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề} \\\\ \\hline\n")
    tong_d = tong_p = 0
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {d(ph).replace(',0', '')} & {ng} \\\\ \\hline\n"
        tong_d += di; tong_p += ph
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{CỘNG}}}} & \\textbf{{{d(tong_d)}}} & \\textbf{{{d(tong_p).replace(',0', '')}}} & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tong_d, tong_p


def bang_muc(rows):
    muc = {"NB": 0, "TH": 0, "VD": 0, "VDC": 0}
    ds = {"Đại số (Chương I, II)": dict(muc), "Hình học (Chương III)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        ds["Hình học (Chương III)" if ch.startswith("HH") else "Đại số (Chương I, II)"][m] += di
    s = ("\\noindent\\textbf{TỔNG HỢP THEO MẠCH KIẾN THỨC VÀ CẤP ĐỘ (điểm)}\\par\\vspace{-6pt}\n"
         "\\begin{center}\\footnotesize\\linespread{1}\\selectfont\\renewcommand{\\arraystretch}{1.12}\n\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
         "\\textbf{Mạch kiến thức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n")
    tot = dict(muc)
    for k, v in ds.items():
        s += f"{k} & " + " & ".join(d(v[m]) if v[m] else "0" for m in muc) + f" & \\textbf{{{d(sum(v.values()))}}} \\\\ \\hline\n"
        for m in muc:
            tot[m] += v[m]
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tot[m]) if tot[m] else '0'}}}" for m in muc) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{d(tot[m] * 10).replace(',0', '')}\\%" for m in muc) + " & 100\\% \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tot


def bang_dap_an_tn(D):
    s = ("\\begin{center}\\small\\renewcommand{\\arraystretch}{1.2}\n\\begin{tabular}{|l|" + "c|" * 8 + "}\n\\hline\n"
         "\\textbf{Câu} & " + " & ".join(str(c["cau"]) for c in D["tn"]) + " \\\\ \\hline\n"
         "\\textbf{Đáp án} & " + " & ".join(f"\\textbf{{{c['dap']}}}" for c in D["tn"]) + " \\\\ \\hline\n"
         "\\end{tabular}\\end{center}")
    return s


def bang_tien_bo():
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.1}\n"
         "\\begin{tabular}{|p{2.2cm}|p{3.05cm}|p{3.05cm}|p{3.05cm}|p{3.05cm}|}\n\\hline\n"
         "\\textbf{Dạng} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{GK1 chính thức} \\\\ \\hline\n")
    for r in TIEN_BO:
        s += " & ".join(r) + " \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def bang_theo_doi():
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.35}\n"
         "\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
         "\\textbf{Phần (điểm tối đa)} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{GK1} & \\textbf{Tiến bộ?} \\\\ \\hline\n")
    for b in ["Phần I -- trắc nghiệm (2,0)", "Bài 1, 2 -- đa thức, phép tính, HĐT (2,5)", "Bài 3 -- tìm $x$ (1,0)",
              "Bài 4 -- toán thực tế (1,0)", "Bài 5 -- hình học (3,0)", "Bài 6 -- câu cuối (0,5)", "\\textbf{Tổng (10,0)}"]:
        s += b + " & & & & & \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def khoi_tn(c, co_loi_giai=True):
    blk = dict(type="problem", label=f"Câu {c['cau']}.", level=c["level"], statement=c["de"], options=c["options"],
               tier="onclass")
    if co_loi_giai:
        blk["answer"] = c["dap"]
        blk["solution"] = f"Chọn \\textbf{{{c['dap']}}}. " + c["giai"]
    return blk


def khoi_bai(b):
    sol = BR.join(b["dap_an"])
    if b.get("hinh_da"):
        sol = "\\begin{center}\\adjustbox{max width=0.75\\linewidth}{" + b["hinh_da"] + "}\\end{center}" + sol
    blk = dict(type="problem", label=b["label"], level=b["level"], statement=b["statement"], tier="onclass", solution=sol)
    if b.get("figure"):
        blk["figure"] = dict(tikz=b["figure"]["tikz"], pos=b["figure"]["pos"])
    out = [blk]
    if b.get("sau_hinh"):
        out.append(dict(type="para", text=b["sau_hinh"]))
    return out


NGAT = dict(type="para", text="\\newpage")


def de_json(k, D):
    # `ngat`: ngắt trang CHỦ ĐỘNG trước câu TN / bài tự luận mà TeX cắt đôi (phương án trắc nghiệm là các
    # \parbox rời nên TeX được ngắt giữa chúng) — chốt sau khi soát PDF bằng mắt; sửa đề thì soát lại.
    ngat = set(D.get("ngat", []))
    tn_blocks = [dict(type="para", text=TN_DAU)]
    for c in D["tn"]:
        if ("tn", c["cau"]) in ngat:
            tn_blocks.append(NGAT)
        tn_blocks.append(khoi_tn(c))
    stages = [dict(kind="review", number=1, title="",
                   blocks=tn_blocks,
                   teacher_note="Phần I: 8 câu, mỗi câu 0,25 điểm. " + D["cach_dung"])]
    for i in range(1, 5):
        blocks = [dict(type="para", text=TL_DAU)] if i == 1 else []
        for j in NHOM_BAI[i]:
            if ("bai", j + 1) in ngat:
                blocks.append(NGAT)
            blocks += khoi_bai(D["bai"][j])
        if i == 4:
            blocks.append(dict(type="para", text="\\nopagebreak\\centerline{\\textit{$-$ HẾT $-$}}"))
        stages.append(dict(kind=KIND[i], number=i + 1, title="", blocks=blocks,
                           teacher_note=" ".join(D["bai"][j]["note"] for j in NHOM_BAI[i])))
    tit = "Đề kiểm tra giữa học kì I (90 phút)" if k == "gk1" else f"Đề ôn tập giữa học kì I — Số {k[-1]} (90 phút)"
    return dict(slug=D["slug_de"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 8", class_tier="", theme="de_thi",
                trinh_bay="thoang", stages=stages)


def mt_json(k, D):
    rows = dong_mt(D)
    t_tn, d_tn, p_tn = bang_mt(rows[:8], "PHẦN I. TRẮC NGHIỆM (2,0 điểm)")
    t_tl, d_tl, p_tl = bang_mt(rows[8:], "PHẦN II. TỰ LUẬN (8,0 điểm)")
    t2, tot = bang_muc(rows)
    assert abs(d_tn + d_tl - 10) < 1e-9, (k, d_tn + d_tl)
    n_tr, q = NGUON[k]
    nguon = (f"\\textbf{{Nguồn đề:}} câu lấy từ {n_tr} trường thuộc {len(q)} quận/huyện ("
             + "; ".join(f"{a} {d(v)}đ" for a, v in sorted(q.items(), key=lambda t: -t[1]))
             + "). Không quận nào quá $40\\%$ số điểm của đề; cả bộ 4 đề lấy từ "
             + f"{len(NGUON_BO)} quận/huyện, không quận nào quá $25\\%$.")
    tong_p = p_tn + p_tl
    st0 = [dict(type="para", text=D["gioi_thieu"] + BR + nguon), dict(type="para", text=t_tn), dict(type="para", text=t_tl),
           dict(type="para", text=t2),
           dict(type="para", text=f"\\noindent\\textit{{\\footnotesize Tổng thời gian làm bài ước tính: {d(tong_p).replace(',0', '')} phút. "
                                  "Mức NB/TH/VD/VDC chấm theo cách các trường ghi trong ma trận đề gốc.}")]
    stages = [dict(kind="review", number=1, title="Ma trận đề", blocks=st0, teacher_note=D["cach_dung"])]
    # Đáp án Phần I
    tn_blocks = [dict(type="para", text="\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm)} -- mỗi câu đúng 0,25 điểm."),
                 dict(type="para", text=bang_dap_an_tn(D)),
                 dict(type="para", text=BR.join(f"\\textbf{{Câu {c['cau']} -- {c['dap']}.}} {c['giai']}" for c in D["tn"]))]
    grp = [("Đáp án Phần I, Bài 1 và Bài 2", [0, 1]), ("Đáp án Bài 3 và Bài 4", [2, 3]), ("Đáp án Bài 5", [4]),
           ("Đáp án Bài 6 và biểu điểm", [5])]
    for j, (ti, idx) in enumerate(grp, 2):
        blocks = list(tn_blocks) if j == 2 else []
        if j == 2:
            blocks.append(dict(type="para", text="\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm)}"))
        for i in idx:
            b = D["bai"][i]
            diem = sum(r[4] for r in b["mt"])
            blocks.append(dict(type="para", text=f"\\textbf{{{b['label'].upper().replace('.', '')} ({d(diem)} điểm).}}"))
            if b.get("hinh_da"):
                blocks.append(dict(type="figure", tikz=b["hinh_da"], width=b.get("rong_da", "0.75") + "\\linewidth"))
            if b.get("figure"):
                blocks.append(dict(type="figure", tikz=b["figure"]["tikz"], width=b["figure"].get("rong_da", "0.45") + "\\linewidth"))
            for a in b["dap_an"]:
                blocks.append(dict(type="para", text=a))
            blocks.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + b["note"] + "}"))
        if j == 5:
            bd = BR.join([f"\\textbf{{Phần I (2,0đ):}} mỗi câu 0,25đ."] +
                         [f"\\textbf{{{b['label']} ({d(sum(r[4] for r in b['mt']))}đ):}} " +
                          " $-$ ".join(f"{r[0]} {d(r[4])}đ" for r in b["mt"]) for b in D["bai"]])
            blocks.append(dict(type="para", text="\\textbf{BIỂU ĐIỂM TỔNG HỢP}" + BR + bd))
            blocks.append(dict(type="para", text="\\textbf{Tổng: 10,0 điểm.} Điểm toàn bài làm tròn đến $0{,}25$ điểm. "
                                                 "Học sinh giải theo cách khác đúng vẫn cho điểm tối đa từng phần. Bài hình vẽ sai hình không chấm điểm."))
        stages.append(dict(kind=KIND[j - 1], number=j, title=ti, blocks=blocks))
    if k == "gk1":
        stages[-1]["blocks"] += [
            dict(type="para", text="\\textbf{ĐÁNH GIÁ VÌ SỰ TIẾN BỘ -- BẢN ĐỒ DẠNG QUA 4 ĐỀ}" + BR +
                 "Mỗi dạng được ôn ở 3 đề với độ khó tăng dần; đề GK1 đo lại đúng dạng đó bằng câu của trường khác. "
                 "Bài nào HS mất điểm ở GK1 thì tra cột tương ứng để biết cần ôn lại đề nào, câu nào."),
            dict(type="para", text=bang_tien_bo()),
            dict(type="para", text="\\textbf{PHIẾU THEO DÕI TIẾN BỘ (ghi điểm từng phần của mỗi học sinh)}" + BR +
                 "\\textbf{Mức thành thạo:} Phần I $\\ge 1{,}5$ -- Bài 1, 2 $\\ge 2{,}0$ -- Bài 3 đủ $1{,}0$ -- Bài 4 $\\ge 0{,}75$ -- "
                 "Bài 5 $\\ge 2{,}25$ (lấy trọn a, b)." + BR +
                 "Đạt cả năm mức là khoảng $7{,}5$ điểm trở lên. Ý c bài hình và Bài 6 ($1{,}25$ điểm) là phần phân loại học sinh khá -- giỏi." + BR +
                 "Cột \\textit{Tiến bộ?}: so điểm GK1 với điểm cao nhất của phần đó ở 3 đề ôn; phần nào GK1 thấp hơn thì tra bản đồ dạng ở trên để ôn lại."),
            dict(type="para", text=bang_theo_doi()),
        ]
    else:
        so = int(k[-1])
        nxt = {1: "Đề ôn 2 giữ nguyên các dạng nhưng nâng một nấc (hằng đẳng thức lập phương, tìm $x$ đưa về tích, "
                  "bài hình có ý ``trung tuyến bằng nửa cạnh $\\Rightarrow$ tam giác vuông'', câu cuối ba ẩn).",
               2: "Đề ôn 3 chuyển sang các dạng tần suất thứ nhì (tìm đa thức chưa biết, chia hết, tính nhanh, hình vuông, tối ưu thực tế).",
               3: "Đề GK1 chính thức đo lại toàn bộ dạng của 3 đề ôn bằng câu của trường khác -- xem bản đồ tiến bộ trong file đáp án đề GK1."}[so]
        stages[-1]["blocks"].append(dict(type="para", text="\\textbf{SAU ĐỀ NÀY}" + BR + nxt + BR +
                                         "Chữa bài: ưu tiên các ý HS mất điểm vì \\textit{trình bày} (bỏ ngoặc quên đổi dấu, mất nghiệm khi chia hai vế, "
                                         "bài hình thiếu căn cứ) trước, rồi mới tới ý khó -- đó là điểm lấy lại nhanh nhất."))
    tit = ("Ma trận đề và đáp án chi tiết — Đề GK1 chính thức" if k == "gk1" else f"Ma trận đề và đáp án chi tiết — Đề ôn tập số {k[-1]}")
    return dict(slug=D["slug_mt"], title=tit, eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 8 • " + D["ten"], grade_label="Lớp 8",
                class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


for k, D in DE.items():
    (OUT / f"{D['slug_de']}.json").write_text(json.dumps(de_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / f"{D['slug_mt']}.json").write_text(json.dumps(mt_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", k)
