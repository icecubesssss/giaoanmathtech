#!/usr/bin/env python3
"""Phiếu 3 ch.V 9C — sửa theo góp ý Thầy 04/11/2026 (đọc rồi sửa chính JSON, không dựng lại từ đầu).

Góp ý: (1) căn cứ vuông = trung tuyến bằng nửa cạnh tương ứng (SGK Toán 8 KNTT tập 1 tr.66);
(2) thay BTVN Ngọc Lâm, ưu tiên dạng tần suất cao; (3) mỗi bài một đề gốc, không trùng;
(4) ô trống rơi vào từ khoá / chỗ suy ra, dày hơn, không lộ; (5) hình nền đúng thứ tự vẽ.

Đề bốc từ ẢNH: Nguyễn Bỉnh Khiêm 2025 Câu 4.2 · Lômônôxốp 2024 Bài IV.2 · Phan Đình Giót 2024
Bài IV.2 · Đống Đa 2025 Bài IV.2 · Ba Đình 2024 Bài IV.2 · Phúc Đồng 2025 Bài IV.2 ·
STK Trương Ngọc Vỹ Câu 7 tr.232, Câu 13 tr.6–7, Câu 60 tr.252.

Chạy: .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p3_ban2.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from scripts.tikz_geo import Fig, foot, polar, tangent_points  # noqa: E402

D = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D / "phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json"
TM = D / "thuyet-minh.json"
BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"
R = 1.5
KY_HIEU, BIEU_THUC, CUM_TU = "1.1cm", "2.4cm", "3.2cm"


def bl(w=KY_HIEU):
    """Ô trống trong công thức."""
    return f"$[[blank:{w}]]$"


TIEP = f"[[blank:{BIEU_THUC}]]"
CAT = f"[[blank:{BIEU_THUC}]]"
TRUNG_TRUC = f"[[blank:{CUM_TU}]]"
TRUNG_TUYEN = f"[[blank:{CUM_TU}]]"
BAN_KINH = f"[[blank:{BIEU_THUC}]]"
VUONG_GOC = f"[[blank:{BIEU_THUC}]]"


def khung(tz: str) -> str:
    xy = [(float(a), float(b)) for a, b in re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)", tz)]
    xs, ys = [p[0] for p in xy], [p[1] for p in xy]
    return f"  \\path ({min(xs) - 0.15:.4f},{min(ys) - 0.15:.4f}) rectangle ({max(xs) + 0.15:.4f},{max(ys) + 0.15:.4f});"


def nen(f: Fig, day_du: str) -> str:
    return f.tikz().replace("\\end{tikzpicture}", khung(day_du) + "\n\\end{tikzpicture}")


def khac(p, ds):
    """Trả về điểm trong ds không trùng p."""
    return max(ds, key=lambda q: abs(q[0] - p[0]) + abs(q[1] - p[1]))


# ── Hình ───────────────────────────────────────────────────────────────────────
def h_trung_truc_tron():
    f = Fig()
    O, A, B = (0, 0), polar(210, 1.0), polar(330, 1.0)
    f.circle(O, 1.0)
    f.pt("O", O); f.pt("A", A); f.pt("B", B)
    f.seg("A", "B"); f.seg((0, -1.3), (0, 1.3))
    f.text((0.14, 1.2), "$d$")
    # Khung rộng hơn hình: \\figbelow co theo BỀ NGANG, nên hình thấp lại, chú thích khỏi rớt trang.
    return f.tikz().replace("\\end{tikzpicture}", "  \\path (-2.2000,-1.3000) rectangle (2.2000,1.3000);\n\\end{tikzpicture}")


def h_diem_ngoai(ten_m, ten_a, ten_b, ten_h):
    """Hình đầy đủ: hai tiếp tuyến từ một điểm ngoài đường tròn."""
    f = Fig()
    O, M = (0, 0), (3.5, 0)
    a, b = tangent_points(O, R, M)
    if a[1] < b[1]:
        a, b = b, a
    h = foot(a, O, M)
    f.circle(O, R)
    f.pt("O", O); f.pt(ten_m, M); f.pt(ten_a, a); f.pt(ten_b, b); f.pt(ten_h, h)
    for u, v in [(ten_m, ten_a), (ten_m, ten_b), ("O", ten_a), ("O", ten_b), ("O", ten_m), (ten_a, ten_b)]:
        f.seg(u, v)
    f.right(ten_a, O, M); f.right(ten_b, O, M); f.right(ten_h, a, M)
    return f.tikz()


def h_nen_diem_ngoai(ten_m, day_du):
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt(ten_m, (3.5, 0))
    return nen(f, day_du)


def h_ba_dinh():
    f = Fig()
    O, A, B, C = (0, 0), (0, R), (0, -R), (2.9, R)
    Dd = khac(A, tangent_points(O, R, C))
    I = foot(A, O, C)
    f.arc(O, R, -90, 90)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("C", C); f.pt("D", Dd); f.pt("I", I)
    f.pt("x", (3.6, R), dot=False)
    for u, v in [("A", "B"), ("A", "x"), ("C", "D"), ("O", "C"), ("A", "D"), ("B", "D"), ("O", "D")]:
        f.seg(u, v)
    f.right("A", O, C); f.right("D", O, C); f.right("I", A, C); f.right("D", A, B)
    return f.tikz()


def h_nen_duong_kinh_doc(a, b, nua=False, day_du=""):
    f = Fig()
    if nua:
        f.arc((0, 0), R, -90, 90)
    else:
        f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt(a, (0, R)); f.pt(b, (0, -R))
    f.seg(a, b)
    return nen(f, day_du)


def h_nen_duong_kinh_ngang(a, b, day_du):
    f = Fig()
    f.arc((0, 0), R, 0, 180)
    f.pt("O", (0, 0)); f.pt(a, (-R, 0)); f.pt(b, (R, 0))
    f.seg(a, b)
    return nen(f, day_du)


def h_nguyen_binh_khiem():
    """BC nằm ngang, nửa đường tròn phía trên: hình thấp, đủ chỗ vẽ Bx và D."""
    f = Fig()
    O, B, C = (0, 0), (-R, 0), (R, 0)
    A = polar(110, R)
    Dd = (-R, R * math.tan(math.radians(35)))
    K = foot(A, O, Dd)
    f.arc(O, R, 0, 180)
    f.pt("O", O); f.pt("B", B); f.pt("C", C); f.pt("A", A); f.pt("D", Dd)
    f.pt("x", (-R, 2.0), dot=False)
    for u, v in [("B", "C"), ("B", "x"), ("D", "A"), ("O", "D"), ("A", "B"), ("O", "A")]:
        f.seg(u, v)
    f.right("B", O, Dd); f.right("A", O, Dd); f.right(K, A, Dd)
    return f.tikz()


def h_lomonoxop():
    f = Fig()
    O, M, N = (0, 0), (0, R), (0, -R)
    I = polar(-10, R)
    K = (R * math.tan(math.radians(50)), R)
    H = foot(M, O, K)
    f.circle(O, R)
    f.pt("O", O); f.pt("M", M); f.pt("N", N); f.pt("I", I); f.pt("K", K)
    for u, v in [("M", "N"), ("K", "M"), ("K", "I"), ("K", "O"), ("M", "I"), ("N", "I"), ("O", "I")]:
        f.seg(u, v)
    f.right("M", O, K); f.right(H, M, K); f.right("I", M, N)
    return f.tikz()


def h_dong_da():
    f = Fig()
    O, A, B, P = (0, 0), (0, R), (0, -R), (2.9, R)
    M = khac(A, tangent_points(O, R, P))
    H = foot(A, O, P)
    f.circle(O, R)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("P", P); f.pt("M", M)
    f.pt("x", (3.6, R), dot=False)
    for u, v in [("A", "B"), ("A", "x"), ("P", "M"), ("O", "P"), ("A", "M"), ("B", "M"), ("O", "M")]:
        f.seg(u, v)
    f.right("A", O, P); f.right("M", O, P); f.right(H, A, P); f.right("M", A, B)
    return f.tikz()


def h_cau_60():
    f = Fig()
    O, Nn, r = (0, 0), (2.92, 0), 1.0
    c, d = tangent_points(O, r, Nn)
    if c[1] < d[1]:
        c, d = d, c
    f.circle(O, r)
    f.pt("O", O); f.pt("N", Nn); f.pt("C", c); f.pt("D", d)
    for u, v in [("N", "C"), ("N", "D"), ("O", "C"), ("O", "D")]:
        f.seg(u, v)
    f.right("C", O, Nn); f.right("D", O, Nn)
    f.angle("N", "C", "D", r=0.5, text="$40^\\circ$")
    return f.tikz()


# ── Lời giải dùng chung ────────────────────────────────────────────────────────
def khung_bon_diem(s, a, b, o):
    """s: điểm ngoài; a, b: tiếp điểm. Ô rơi vào: tiếp tuyến, tính chất vuông góc, đỉnh vuông, đường kính."""
    return (
        f"Vì ${s}{a}$ là {TIEP} của $(O)$ tại ${a}$ $\\Rightarrow {s}{a} \\perp$ {bl()}{BR}"
        f"$\\Rightarrow \\triangle {s}{a}{o}$ vuông tại {bl()}{BR}"
        f"$\\Rightarrow {s}, {a}, {o}$ cùng thuộc đường tròn đường kính {bl()}.{BR}"
        f"Vì ${s}{b}$ là tiếp tuyến của $(O)$ tại ${b}$ $\\Rightarrow {s}{b} \\perp$ {bl()}{BR}"
        f"$\\Rightarrow \\triangle {s}{b}{o}$ vuông tại {bl()}{BR}"
        f"$\\Rightarrow {s}, {b}, {o}$ cùng thuộc đường tròn đường kính {bl()}.{BR}"
        f"Vậy bốn điểm cùng thuộc đường tròn đường kính {bl()}."
    )


def khung_trung_truc(s, a, b, o, h=""):
    tai = f" tại ${h}$" if h else ""
    return (
        f"Vì ${s}{a}$, ${s}{b}$ là hai {TIEP} của $(O)$ cắt nhau tại ${s}${BR}"
        f"$\\Rightarrow {s}{a} =$ {bl()} (tính chất hai tiếp tuyến {CAT}).{BR}"
        f"Lại có ${o}{a} = {o}{b}$ ({BAN_KINH} của $(O)$){BR}"
        f"$\\Rightarrow {o}{s}$ là {TRUNG_TRUC} của đoạn thẳng ${a}{b}${BR}"
        f"$\\Rightarrow {o}{s} \\perp {a}{b}${tai} (tính chất đường trung trực).{BR}"
        f"Vậy ${o}{s} \\perp {a}{b}${tai}."
    )


def giai_bon_diem(s, a, b, o, ket):
    return (
        f"Vì ${s}{a}$ là tiếp tuyến của $(O)$ tại ${a}${BR}$\\Rightarrow {s}{a} \\perp {o}{a}$ tại ${a}${BR}"
        f"$\\Rightarrow \\triangle {s}{a}{o}$ vuông tại ${a}${BR}"
        f"$\\Rightarrow {s}, {a}, {o}$ cùng thuộc đường tròn đường kính ${s}{o}$.{BR}"
        f"Vì ${s}{b}$ là tiếp tuyến của $(O)$ tại ${b}${BR}$\\Rightarrow {s}{b} \\perp {o}{b}$ tại ${b}${BR}"
        f"$\\Rightarrow \\triangle {s}{b}{o}$ vuông tại ${b}${BR}"
        f"$\\Rightarrow {s}, {b}, {o}$ cùng thuộc đường tròn đường kính ${s}{o}$.{BR}{ket}"
    )


def giai_vuong(c, x, y, o):
    """△xcy, trung tuyến co; x, y là hai đầu đường kính; kết luận cx ⊥ cy."""
    return (
        f"Xét $\\triangle {x}{c}{y}$ có ${c}{o}$ là đường trung tuyến ứng với cạnh ${x}{y}$ "
        f"(${o}$ là trung điểm của ${x}{y}$).{BR}"
        f"${o}{c} = {o}{x} = {o}{y} = R \\Rightarrow {c}{o} = \\dfrac{{{x}{y}}}{{2}}${BR}"
        f"$\\Rightarrow \\triangle {x}{c}{y}$ vuông tại ${c}$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng).{BR}"
        f"$\\Rightarrow {y}{c} \\perp {x}{c}$.{BR}"
    )


def main():
    les = json.loads(PHIEU.read_text(encoding="utf-8"))
    st = {s["title"]: s for s in les["stages"]}

    # ── Thẻ lý thuyết ──────────────────────────────────────────────────────────
    kt = st["Kiến thức trọng tâm"]["blocks"]
    kt[2]["text"] = (
        "\\nhanly{Đường trung trực (Lớp 7):} Điểm cách đều hai đầu mút của một đoạn thẳng thì nằm trên đường "
        "trung trực của đoạn thẳng đó.[[br]]"
        "\\nhanly{Trung tuyến (SGK Toán 8, tập 1, tr.66):} Nếu tam giác có một đường trung tuyến bằng nửa cạnh "
        "tương ứng thì tam giác đó là tam giác vuông.[[br]]"
        "\\nhanly{Từ vuông góc đến song song (Lớp 7):} Hai đường thẳng phân biệt cùng vuông góc với đường thẳng "
        "thứ ba thì song song với nhau."
    )
    kt[5]["text"] = (
        "\\nhanly{Phương pháp.} Chứng minh hai đường thẳng cùng vuông góc với một đường thẳng thứ ba.[[br]]"
        "\\nhanly{Bước 1:} Đường kính $BD$, điểm $C \\in (O)$: $CO$ là đường trung tuyến của $\\triangle BCD$ và "
        "$CO = \\dfrac{BD}{2} \\Rightarrow \\triangle BCD$ vuông tại $C \\Rightarrow CD \\perp BC$.[[br]]"
        "\\nhanly{Bước 2:} Đã có $AO \\perp BC$ (phương pháp ở trên).[[br]]"
        "\\nhanly{Bước 3:} Kết luận $AO \\parallel CD$ (vì cùng vuông góc với $BC$)."
    )

    # ── Luyện tập 1 ────────────────────────────────────────────────────────────
    lt1 = st["Luyện tập 1"]["blocks"]
    bai1 = {
        "type": "problem", "label": "Bài 1.", "level": 1, "tier": "onclass", "dang_id": "NB1",
        "statement": "[NB] Cho hai tiếp tuyến của một đường tròn cắt nhau tại một điểm. Chọn khẳng định \\textbf{sai}?",
        "options": ["Khoảng cách từ điểm đó đến hai tiếp điểm là bằng nhau.",
                    "Tia nối điểm đó tới tâm là tia phân giác của góc tạo bởi hai bán kính.",
                    "Tia nối từ tâm tới điểm đó là tia phân giác của góc tạo bởi hai bán kính.",
                    "Tia nối từ điểm đó tới tâm là tia phân giác của góc tạo bởi hai tiếp tuyến."],
        "figure_given": True, "answer": "B",
    }
    bai2 = {
        "type": "problem", "label": "Bài 2.", "level": 1, "tier": "onclass", "dang_id": "NB2",
        "statement": "[NB] Cho đường tròn tâm $O$ và hai điểm $A$, $B$ thuộc $(O)$. Gọi $d$ là đường trung trực của "
                     "đoạn $AB$ (Hình 3). Khẳng định nào sau đây \\textbf{sai}?",
        "options": ["$OA = OB$.", "Điểm $O$ thuộc đường thẳng $d$.",
                    "Đường thẳng $AB$ là trục đối xứng của đường tròn $(O)$.",
                    "Đường thẳng $d$ là trục đối xứng của đường tròn $(O)$."],
        "figure_given": True, "figure": {"tikz": h_trung_truc_tron(), "caption": "Hình 3", "pos": "right"},
        "answer": "C",
    }

    vd1_gv = h_diem_ngoai("M", "A", "B", "I")
    vidu1 = {
        "type": "noted", "variant": "example",
        "text": ("\\textbf{Ví dụ 1.} (SGK Ví dụ 2 Bài 16) Cho hai tiếp tuyến $MA$ và $MB$ của đường tròn $(O; R)$ "
                 "($A$ và $B$ là hai tiếp điểm) (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề. "
                 f"Chứng minh rằng $OM \\perp AB$.{BR}{LG}{BR}"
                 f"Vì $MA$, $MB$ là hai [[fill:tiếp tuyến]] của $(O)$ cắt nhau tại $M${BR}"
                 f"$\\Rightarrow MA = [[fill:MB]]$ (tính chất hai tiếp tuyến [[fill:cắt nhau]]).{BR}"
                 f"Lại có $OA = OB$ ([[fill:bán kính]] của $(O)$){BR}"
                 f"$\\Rightarrow OM$ là [[fill:đường trung trực]] của đoạn thẳng $AB${BR}"
                 f"$\\Rightarrow OM \\perp AB$ (tính chất đường trung trực).{BR}"
                 f"Vậy $[[fill:OM \\perp AB]]$."),
        "figure": {"tikz": h_nen_diem_ngoai("M", vd1_gv), "tikz_gv": vd1_gv, "caption": "Hình 4", "pos": "right"},
    }

    nbk = h_nguyen_binh_khiem()
    de3 = ("Cho nửa đường tròn $(O; R)$ đường kính $BC$. Trên nửa đường tròn $(O)$ vẽ tiếp tuyến $Bx$ của đường tròn "
           "$(O)$, $A$ là điểm bất kì thuộc nửa đường tròn sao cho $AB < AC$ ($A$ khác $B$, $A$ khác $C$). Tiếp tuyến "
           "tại $A$ của nửa đường tròn $(O)$ cắt tia $Bx$ tại $D$")
    bai3 = {
        "type": "problem", "label": "Bài 3.", "level": 1, "tier": "onclass", "dang_id": "NB4", "ve_tiep": 4,
        "statement": (f"{de3} (Hình 5).{BR}Vẽ tiếp vào Hình 5 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, rồi "
                      f"điền vào chỗ chấm để hoàn thành bài giải:{BR}"
                      f"a) [NB] Chứng minh 4 điểm $A$, $D$, $B$, $O$ cùng thuộc một đường tròn:{BR}"
                      + khung_bon_diem("D", "B", "A", "O") + BR
                      + "b) [NB] Chứng minh $OD \\perp AB$:" + BR + khung_trung_truc("D", "A", "B", "O")),
        "statement_slide": (f"{de3} (Hình 5).{BR}a) [NB] Chứng minh 4 điểm $A$, $D$, $B$, $O$ cùng thuộc một đường tròn."
                            f"{BR}b) [NB] Chứng minh $OD \\perp AB$."),
        "figure_given": True,
        "figure": {"tikz": h_nen_duong_kinh_ngang("B", "C", nbk), "tikz_gv": nbk, "caption": "Hình 5", "pos": "right"},
        "answer": ("a) tiếp tuyến; $OB$; $B$; $DO$; $OA$; $A$; $DO$; $DO$.[[br]]"
                   "b) tiếp tuyến; $DB$; cắt nhau; bán kính; đường trung trực."),
    }

    bd = h_ba_dinh()
    vidu2 = {
        "type": "noted", "variant": "example",
        "text": ("\\textbf{Ví dụ 2.} (Đề Ba Đình 2024) Cho nửa đường tròn $(O)$ đường kính $AB = 2R$. Kẻ tiếp tuyến $Ax$ "
                 "của đường tròn. Trên tia $Ax$ lấy điểm $C$ sao cho $AC > R$. Từ $C$ kẻ tiếp tuyến $CD$ của đường tròn "
                 "$(O)$ ($D$ là tiếp điểm) (Hình 6). Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề.[[br]]"
                 f"Chứng minh $OC$ vuông góc với $AD$ và $OC$ song song với $BD$.{BR}{LG}{BR}"
                 f"Vì $CA$, $CD$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C${BR}"
                 f"$\\Rightarrow CA = [[fill:CD]]$ (tính chất hai tiếp tuyến cắt nhau).{BR}"
                 f"Lại có $OA = OD$ (bán kính của $(O)$){BR}"
                 f"$\\Rightarrow OC$ là [[fill:đường trung trực]] của đoạn thẳng $AD${BR}"
                 f"$\\Rightarrow OC \\perp AD$ (tính chất đường trung trực).{BR}"
                 f"Xét $\\triangle ABD$ có $DO$ là đường [[fill:trung tuyến]] ứng với cạnh $AB$ ($O$ là trung điểm của $AB$).{BR}"
                 f"$OD = OA = OB = R \\Rightarrow DO = \\dfrac{{1}}{{2}}[[fill:AB]]${BR}"
                 f"$\\Rightarrow \\triangle ABD$ vuông tại $[[fill:D]]$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng){BR}"
                 f"$\\Rightarrow BD \\perp AD$.{BR}"
                 f"Vì $OC$ và $BD$ cùng [[fill:vuông góc]] với $AD${BR}"
                 f"$\\Rightarrow OC \\parallel BD$ (hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba).{BR}"
                 f"Vậy $OC \\perp AD$ và $[[fill:OC \\parallel BD]]$."),
        "figure": {"tikz": h_nen_duong_kinh_doc("A", "B", nua=True, day_du=bd), "tikz_gv": bd, "caption": "Hình 6", "pos": "right"},
    }

    lm = h_lomonoxop()
    de4 = ("Cho đường tròn $(O)$, đường kính $MN$. Trên đường tròn $(O)$ lấy điểm $I$. Hai tiếp tuyến của đường tròn "
           "$(O)$ tại $M$ và $I$ cắt nhau ở $K$")
    bai4 = {
        "type": "problem", "label": "Bài 4.", "level": 1, "tier": "onclass", "dang_id": "NB5", "ve_tiep": 3,
        "statement": (f"{de4} (Hình 7).{BR}Vẽ tiếp vào Hình 7 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, rồi "
                      f"điền vào chỗ chấm để hoàn thành bài giải:{BR}"
                      f"a) [NB] Chứng minh $KO$ là đường trung trực của đoạn thẳng $MI$:{BR}"
                      f"Vì $KM$, $KI$ là hai {TIEP} của $(O)$ cắt nhau tại $K${BR}"
                      f"$\\Rightarrow KM =$ {bl()} (tính chất hai tiếp tuyến {CAT}).{BR}"
                      f"Lại có $OM = OI$ ({BAN_KINH} của $(O)$){BR}"
                      f"$\\Rightarrow K$ và $O$ cùng [[blank:{BIEU_THUC}]] hai đầu mút của đoạn thẳng $MI${BR}"
                      f"$\\Rightarrow KO$ là đường trung trực của đoạn thẳng $MI$.{BR}"
                      f"Vậy $KO$ là đường trung trực của đoạn thẳng $MI$.{BR}"
                      f"b) [NB] Từ đó suy ra $KO \\parallel NI$:{BR}"
                      f"Xét $\\triangle MIN$ có $O$ là trung điểm của $MN${BR}"
                      f"$\\Rightarrow IO$ là đường {TRUNG_TUYEN} ứng với cạnh $MN$.{BR}"
                      f"$OI = OM = ON \\Rightarrow IO =$ {bl(BIEU_THUC)}{BR}"
                      f"$\\Rightarrow \\triangle MIN$ vuông tại {bl()} (tam giác có đường trung tuyến bằng nửa cạnh tương ứng){BR}"
                      f"$\\Rightarrow NI \\perp MI$.{BR}"
                      f"Vì $KO$ và $NI$ cùng {VUONG_GOC} với $MI${BR}"
                      f"$\\Rightarrow KO \\parallel NI$ (hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba).{BR}"
                      f"Vậy $KO \\parallel NI$."),
        "statement_slide": (f"{de4} (Hình 7).{BR}a) [NB] Chứng minh $KO$ là đường trung trực của đoạn thẳng $MI$."
                            f"{BR}b) [NB] Từ đó suy ra $KO \\parallel NI$."),
        "figure_given": True,
        "figure": {"tikz": h_nen_duong_kinh_doc("M", "N", day_du=lm), "tikz_gv": lm, "caption": "Hình 7", "pos": "right"},
        "answer": ("a) tiếp tuyến; $KI$; cắt nhau; bán kính; cách đều.[[br]]"
                   "b) trung tuyến; $\\dfrac{MN}{2}$; $I$; vuông góc."),
    }

    dich = lt1[0]
    dich["text"] = ("\\textbf{Đích của buổi học:} Đề thi Học kì I — THCS Phúc Đồng (Long Biên).[[br]]"
                    "Ý a chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn; ý b chứng minh "
                    "$OA \\perp BC$ tại $H$ và $OA \\parallel CD$ (Bài 5). Hai mạch dưới đây sẽ luyện từng bước.")
    tieu_de = lambda t: {"type": "para", "variant": "heading", "text": t}  # noqa: E731
    st["Luyện tập 1"]["blocks"] = [
        dich, tieu_de("Mạch 1. Bốn điểm và chứng minh vuông góc"), bai1, bai2, vidu1, bai3,
        tieu_de("Mạch 2. Góc vuông từ đường kính và chứng minh song song"), vidu2, bai4]

    # ── Luyện tập 2: đề đích giữ đúng hai ý của đề thi ───────────────────────────
    lt2 = st["Luyện tập 2"]["blocks"]
    d = next(b for b in lt2 if b.get("type") == "problem")
    d["label"] = "Bài 5."
    d["level"] = 3
    d["statement"] = ("Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn $(O)$. Từ $A$ vẽ hai tiếp tuyến $AB$ và "
                      "$AC$ của đường tròn $(O)$ ($B$, $C$ là hai tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$. "
                      f"Từ $B$ vẽ đường kính $BD$ của $(O)$.{BR}"
                      f"a) [TH] Chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn. Xác định tâm và bán "
                      f"kính của đường tròn đó.{BR}b) [VD] Chứng minh rằng $OA \\perp BC$ tại $H$ và $OA \\parallel CD$.")
    d["figure"]["caption"] = "Hình 8"
    ket = ("Vậy bốn điểm $A, B, C, O$ cùng thuộc đường tròn đường kính $AO$, tâm là trung điểm của $AO$, "
           "bán kính $\\dfrac{AO}{2}$.")
    d["answer"] = ("a) " + giai_bon_diem("A", "B", "C", "O", ket) + BR
                   + "b) Ta có: $AB = AC$ (tính chất hai tiếp tuyến cắt nhau)" + BR
                   + "và $OB = OC = R$ (bán kính của $(O)$)" + BR
                   + "$\\Rightarrow OA$ là đường trung trực của đoạn thẳng $BC$" + BR
                   + "$\\Rightarrow OA \\perp BC$ tại $H$ (tính chất đường trung trực)." + BR
                   + giai_vuong("C", "B", "D", "O")
                   + f"Vì $OA \\perp BC$ và $CD \\perp BC${BR}$\\Rightarrow OA \\parallel CD$ (vì cùng vuông góc với $BC$).{BR}"
                   + "Vậy $OA \\perp BC$ tại $H$ và $OA \\parallel CD$.")
    d["hints"] = ["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
                  "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $BC$?",
                  "Trong $\\triangle BCD$, đoạn $CO$ có quan hệ gì với cạnh $BD$? Hai đường thẳng nào cùng vuông góc với $BC$?"]
    d["quy_trinh"] = ["Ý a: $AB \\perp OB$, $AC \\perp OC \\Rightarrow A, B, C, O$ cùng thuộc đường tròn đường kính $AO$ (như Bài 3)",
                      "Ý b: $AB = AC$, $OB = OC = R \\Rightarrow OA$ là đường trung trực của $BC \\Rightarrow OA \\perp BC$ tại $H$ (như Ví dụ 1)",
                      "$CO$ là trung tuyến, $CO = \\dfrac{BD}{2} \\Rightarrow \\triangle BCD$ vuông tại $C \\Rightarrow CD \\perp BC$ (như Bài 4)",
                      "$OA \\perp BC$ và $CD \\perp BC \\Rightarrow OA \\parallel CD$ (như Ví dụ 2)"]

    # ── Sơ đồ tư duy + BTVN ──────────────────────────────────────────────────────
    tk = st["Sơ đồ tư duy"]["blocks"]
    mm = next(b for b in tk if b.get("type") == "mindmap")
    mm["branches"][2]["children"][0]["label"] = "$CO$ là trung tuyến, $CO = \\dfrac{BD}{2} \\Rightarrow \\triangle BCD$ vuông tại $C$"
    dd = h_dong_da()
    nen_dd = Fig(); nen_dd.circle((0, 0), R)
    nen_dd.pt("O", (0, 0)); nen_dd.pt("A", (0, R)); nen_dd.pt("B", (0, -R)); nen_dd.seg("A", "B")
    pdg = h_diem_ngoai("M", "A", "B", "H")
    de_pdg = ("Cho đường tròn $(O; R)$ và điểm $M$ ($OM > R$). Vẽ hai tiếp tuyến $MA$, $MB$ với đường tròn $(O)$ "
              "($A$, $B$ là các tiếp điểm). Nối $OM$ cắt đoạn thẳng $AB$ tại điểm $H$")
    btvn = [
        {"type": "problem", "label": "BTVN 1.", "level": 1, "tier": "btvn", "dang_id": "NB3",
         "statement": ("[NB] Cho hai tiếp tuyến tại $C$ và $D$ của đường tròn $(O)$ cắt nhau tại $N$, biết "
                       "$\\widehat{CND} = 40^\\circ$ (Hình 9). Số đo của cung nhỏ $CD$ bằng bao nhiêu độ?[[br]]"
                       "Trả lời: $[[blank:1.6cm]]$"),
         "figure_given": True, "figure": {"tikz": h_cau_60(), "caption": "Hình 9", "pos": "right"},
         "answer": "$140^\\circ$"},
        {"type": "problem", "label": "BTVN 2.", "level": 1, "tier": "btvn", "dang_id": "NB4", "ve_tiep": 3,
         "statement": (f"{de_pdg} (Hình 10).{BR}Vẽ tiếp vào Hình 10 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, "
                       f"rồi điền vào chỗ chấm để hoàn thành bài giải:{BR}"
                       f"a) [NB] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng thuộc một đường tròn:{BR}"
                       + khung_bon_diem("M", "A", "B", "O") + BR
                       + "b) [NB] Chứng minh $OM \\perp AB$:" + BR + khung_trung_truc("M", "A", "B", "O", "H")),
         "statement_slide": (f"{de_pdg} (Hình 10).{BR}a) [NB] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng thuộc một đường tròn."
                             f"{BR}b) [NB] Chứng minh $OM \\perp AB$."),
         "figure_given": True,
         "figure": {"tikz": h_nen_diem_ngoai("M", pdg), "tikz_gv": pdg, "caption": "Hình 10", "pos": "right"},
         "answer": ("a) tiếp tuyến; $OA$; $A$; $MO$; $OB$; $B$; $MO$; $MO$.[[br]]"
                    "b) tiếp tuyến; $MB$; cắt nhau; bán kính; đường trung trực.")},
        {"type": "problem", "label": "BTVN 3.", "level": 3, "tier": "btvn", "dang_id": "TH1+VD1", "draw": True,
         "figure_given": False,
         "statement": ("(Đề Đống Đa 2025) Cho đường tròn $(O; R)$ đường kính $AB$. Kẻ tiếp tuyến $Ax$, lấy $P$ trên $Ax$ "
                       f"($AP > R$). Từ $P$ kẻ tiếp tuyến $PM$ với $(O)$.{BR}"
                       f"a) [TH] Chứng minh bốn điểm $A$, $P$, $M$, $O$ cùng thuộc một đường tròn.{BR}"
                       "b) [VD] Chứng minh $OP \\perp AM$ và $OP \\parallel MB$."),
         "figure": {"tikz": nen(nen_dd, dd), "tikz_gv": dd, "caption": "Hình 11", "pos": "right"},
         "answer": ("a) " + giai_bon_diem("P", "A", "M", "O", "Vậy bốn điểm $A, P, M, O$ cùng thuộc đường tròn đường kính $PO$.") + BR
                    + "b) Ta có: $PA = PM$ (tính chất hai tiếp tuyến cắt nhau)" + BR
                    + "và $OA = OM = R$ (bán kính của $(O)$)" + BR
                    + "$\\Rightarrow OP$ là đường trung trực của đoạn thẳng $AM$" + BR
                    + "$\\Rightarrow OP \\perp AM$ (tính chất đường trung trực)." + BR
                    + giai_vuong("M", "A", "B", "O")
                    + f"Vì $OP \\perp AM$ và $MB \\perp AM${BR}$\\Rightarrow OP \\parallel MB$ (vì cùng vuông góc với $AM$).{BR}"
                    + "Vậy $OP \\perp AM$ và $OP \\parallel MB$."),
         "hints": ["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
                   "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $AM$?",
                   "Trong $\\triangle AMB$, đoạn $MO$ có quan hệ gì với cạnh $AB$?"]},
    ]
    st["Sơ đồ tư duy"]["blocks"] = [b for b in tk if b.get("type") != "problem"] + btvn
    # Bài 1 không có hình (đề gốc không hình) ⇒ đánh lại số từ Hình 2.
    so_hinh = lambda m: f"Hình {int(m.group(1)) - 1}" if int(m.group(1)) >= 3 else m.group(0)  # noqa: E731
    for ten in ("Luyện tập 1", "Luyện tập 2", "Sơ đồ tư duy"):
        st[ten]["blocks"] = json.loads(re.sub(r"Hình (\d+)", so_hinh, json.dumps(st[ten]["blocks"], ensure_ascii=False)))
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Thuyết minh (sửa trước khi build phiếu) ──────────────────────────────────
    tm = json.loads(TM.read_text(encoding="utf-8"))
    tm["kien_thuc_nen"][0] = tm["kien_thuc_nen"][0].replace(
        "Chiều ngược: tam giác có trung tuyến bằng nửa cạnh tương ứng thì vuông — dùng cho",
        "Chiều ngược (SGK Toán 8 tập 1, Bài 13, tr.66): tam giác có trung tuyến bằng nửa cạnh tương ứng thì vuông — dùng cho")
    tm["vidu"] = [("Buổi 3: Hai tiếp tuyến $MA$, $MB$ — $OM \\perp AB$ (SGK Ví dụ 2a). Đề mẫu (Ba Đình 2024): nửa đường tròn, "
                   "tiếp tuyến $Ax$ và $CD$ — $OC \\perp AD$ và $OC \\parallel BD$.") if x.startswith("Buổi 3") else x
                  for x in tm["vidu"]]
    tm["dang_vd"] = [x.replace("BTVN: đề Ngọc Lâm cùng khuôn.", "BTVN: đề Đống Đa 2025.")
                     .replace("đường kính cho góc vuông", "trung tuyến cho góc vuông") if x.startswith("Buổi 3") else x
                     for x in tm["dang_vd"]]
    i = next(k for k, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 3"))
    if "Luyện tập 1 khoảng 46′" in tm["thoiluong"][i + 1]:
        del tm["thoiluong"][i + 1]
    tm["thoiluong"].insert(i + 1, "\\quad Giờ thực lớp C (04/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 46′ "
                                  "(2 trắc nghiệm, 2 ví dụ HS vẽ cùng GV, 2 khung bài giải $+$ vẽ tiếp hình) · Luyện tập 2 "
                                  "khoảng 31′ (đề đích Phúc Đồng, HS tự vẽ) · chữa bài, chốt khoảng 5′ · BTVN khoảng 39′")
    p3 = next(p for p in tm["phieu"] if str(p.get("code")) == "3")
    p3["rows"] = [
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Định lí hai tiếp tuyến cắt nhau: khoảng cách bằng nhau, tia phân giác (trắc nghiệm chọn khẳng định sai)",
         "source_refs": ["stk-b16-I-C7-tr232"], "vidu": 0, "onclass": 1, "btvn": 0, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Đường trung trực của đoạn thẳng (Lớp 7): tâm cách đều hai điểm trên đường tròn nên thuộc đường trung trực (trắc nghiệm)",
         "source_refs": ["stk-b13-I-C13-tr6"], "vidu": 0, "onclass": 1, "btvn": 0, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Tính số đo cung trên hình hai tiếp tuyến cắt nhau (BTVN trả lời ngắn)",
         "source_refs": ["stk-b16-III-C60-tr252"], "vidu": 0, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB ghép bài", "dang": "Khung bài giải: bốn điểm cùng thuộc đường tròn đường kính; đường trung trực $\\Rightarrow$ vuông góc (trên lớp đề Nguyễn Bỉnh Khiêm; BTVN đề Phan Đình Giót)",
         "source_refs": ["ck1-nguyen-binh-khiem-2025-4.2", "ck1-phan-dinh-giot-2024-IV2"], "vidu": 0, "onclass": 2, "btvn": 2, "lythuyet": 0, "decompose": "none", "hinh_san": True, "gian_giao": "dien-khuyet", "khung": True, "ve_tiep": {"onclass": 4, "btvn": 3}},
        {"band": "NB", "loai": "NB tách TH", "dang": "Khung bài giải ý song song: đường trung trực; trung tuyến bằng nửa cạnh tương ứng $\\Rightarrow$ tam giác vuông; cùng vuông góc $\\Rightarrow$ song song (đề Lômônôxốp)",
         "source_refs": ["ck1-lomonoxop-2024-IV2"], "vidu": 0, "onclass": 2, "btvn": 0, "lythuyet": 0, "decompose": "none", "hinh_san": True, "gian_giao": "ve-hinh", "khung": True, "ve_tiep": {"onclass": 3}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Ý a của đề thi: bốn điểm cùng thuộc một đường tròn, xác định tâm và bán kính. Ví dụ mẫu SGK Ví dụ 2; trên lớp đề Phúc Đồng ý a; BTVN đề Đống Đa ý a",
         "source_refs": ["sgk-b16-vd2", "ck1-phuc-dong-IV2.a", "ck1-dong-da-2025-IV2.a"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb", "hinh_san": False, "ve_tiep": {"vidu": 2}, "ve_hinh": {"onclass": 1, "btvn": 1}},
        {"band": "VD", "loai": "VD lẻ", "dang": "Ý b của đề thi (đề Phúc Đồng — đích của buổi): $OA \\perp BC$ tại $H$ và $OA \\parallel CD$. Ví dụ mẫu đề Ba Đình 2024; BTVN đề Đống Đa",
         "source_refs": ["ck1-phuc-dong-IV2.b", "ck1-ba-dinh-2024-IV2", "ck1-dong-da-2025-IV2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "vd", "hinh_san": False, "gian_giao": "ve-hinh", "quy_trinh": d["quy_trinh"], "ve_tiep": {"vidu": 3}},
    ]
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    main()
