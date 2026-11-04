#!/usr/bin/env python3
"""Dựng lại Phiếu 3 ch.V lớp 9C (Bài 16 SGK: Tính chất hai tiếp tuyến cắt nhau).
Tuân thủ:
- Thang dẫn dắt: Mạch 1 (bốn điểm + OA ⊥ BC) -> Mạch 2 (song song khi có đường kính) -> Đích (đề Phúc Đồng).
- Thẻ lý thuyết Kiến thức trọng tâm chuẩn (4 thẻ theory card với \nhanly).
- Mỗi bài một hình riêng, không mượn hình, không xưng hô "em hãy".
- Khung bài giải điền khuyết chuẩn đi thi (đủ lời dẫn, mỗi dòng 1 =>, kết luận "Vậy ...").
- Khuôn 4 điểm: △ vuông tại A => A, B, C thuộc đường tròn đường kính BC.
- Giảm tải vừa khít 90' cho lớp C (GV 25' + Luyện tập 55' + Giải lao 10' = 90'; BTVN 40').
- btvn_phieu_rieng: True.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.tikz_geo import Fig, polar, tangent_points, foot

BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"
KG = "Điền vào chỗ chấm để hoàn thành bài giải:"


def fig(f: Fig, cap: str) -> dict:
    return {"tikz": f.tikz(), "caption": cap, "pos": "right"}


def mcq(stem: str, opts: list[str], tag: str = "[NB] ", cols: int = 1) -> tuple[str, str]:
    body = "".join(f"\\mcqitem{{{k}}}{{{v}}}" for k, v in zip("ABCD", opts))
    st = f"{tag}{stem} \\begin{{mcq}}{{{cols}}}{body}\\end{{mcq}}"
    sl = f"{tag}{stem}{BR}" + " \\quad ".join(f"\\textbf{{{k}.}} {v}" for k, v in zip("ABCD", opts))
    return st, sl


def P(label: str, dang: str, tier: str, statement: str, answer: str | None = None,
      level: int = 1, figure: dict | None = None, slide: str | None = None,
      draw: bool = False, hints: list[str] | None = None,
      quy_trinh: list[str] | None = None) -> dict:
    b = {
        "type": "problem",
        "label": label,
        "level": level,
        "tier": tier,
        "dang_id": dang,
        "statement": statement,
        "figure_given": not draw,
    }
    if draw:
        b["draw"] = True
    if figure:
        b["figure"] = figure
    if answer:
        b["answer"] = answer
    if slide:
        b["statement_slide"] = slide
    if hints:
        b["hints"] = hints
    if quy_trinh:
        b["quy_trinh"] = quy_trinh
    return b


def card(text: str, cap: str, f: Fig) -> dict:
    return {
        "type": "noted",
        "variant": "theory",
        "text": text,
        "figure": fig(f, cap)
    }


# ===================== TIKZ FIGURES =====================

def h_khampha():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C")
    f.seg("A", "O", style='ink, dashed')
    f.right("B", "A", "O")
    f.right("C", "A", "O")
    return f


def h_concept1():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C)]:
        f.pt(n, p)
    f.circle(O, R)
    f.poly("A", "B", "O", "C")
    f.seg("O", "A")
    f.right("B", "A", "O")
    f.right("C", "A", "O")
    return f


def h_concept2():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    D = (-B[0], -B[1])
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "A"); f.seg("B", "C")
    f.seg("B", "D"); f.seg("C", "D")
    f.right("H", "B", "A")
    f.right("C", "B", "D")
    return f


def h_concept3():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.7, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C")
    f.seg("O", "A"); f.seg("B", "C")
    f.right("H", "B", "A")
    return f


def h_concept4():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.7, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    D = (-B[0], -B[1])
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "A"); f.seg("B", "C")
    f.seg("B", "D"); f.seg("C", "D")
    f.right("H", "B", "A")
    f.right("C", "B", "D")
    return f


def h_bai1():
    f = Fig()
    O, R, M = (0, 0), 1.2, (2.7, 0)
    A, B = tangent_points(O, R, M)
    if A[1] < B[1]: A, B = B, A
    for n, p in [("O", O), ("M", M), ("A", A), ("B", B)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("M", "A"); f.seg("M", "B"); f.seg("O", "A"); f.seg("O", "B"); f.seg("O", "M")
    f.right("A", "M", "O")
    f.right("B", "M", "O")
    return f


def h_bai2():
    f = Fig()
    B, C = (-1.5, 0), (1.5, 0)
    A = (0, 1.8); O = (0, -1.2)
    for n, p in [("B", B), ("C", C), ("A", A), ("O", O)]:
        f.pt(n, p)
    f.seg("B", "C"); f.seg("A", "O")
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C")
    f.right((0, 0), B, A)
    return f


def h_vidu1():
    f = Fig()
    O, R, M = (0, 0), 1.2, (2.8, 0)
    A, B = tangent_points(O, R, M)
    if A[1] < B[1]: A, B = B, A
    I = foot(A, (0, 0), M)
    for n, p in [("O", O), ("M", M), ("A", A), ("B", B), ("I", I)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("M", "A"); f.seg("M", "B"); f.seg("O", "A"); f.seg("O", "B")
    f.seg("O", "M"); f.seg("A", "B")
    f.right("A", "M", "O")
    f.right("I", "A", "M")
    return f


def h_bai3():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C")
    f.seg("O", "A"); f.seg("B", "C")
    f.right("B", "A", "O")
    f.right("C", "A", "O")
    f.right("H", "B", "A")
    return f


def h_vidu2():
    f = Fig()
    O, R = (0, 0), 1.3
    A, B = (-1.3, 0), (1.3, 0)
    C = (-1.3, 2.0)
    tpts = tangent_points(O, R, C)
    D = [p for p in tpts if p[0] > -1.2][0]
    I = foot(D, (0, 0), C)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("D", D), ("I", I)]:
        f.pt(n, p)
    f.arc(O, R, 0, 180)
    f.seg("A", "B")
    f.seg("A", "C")
    f.seg("C", "D")
    f.seg("B", "D")
    f.seg("A", "D")
    f.seg("O", "C")
    f.seg("O", "D")
    f.right("A", (0, 0), C)
    f.right("D", (0, 0), C)
    f.right("I", A, C)
    f.right("D", A, B)
    return f


def h_bai4():
    f = Fig()
    O, R = (0, 0), 1.3
    B, D = (-1.3, 0), (1.3, 0)
    C = polar(60, R, O)
    for n, p in [("O", O), ("B", B), ("D", D), ("C", C)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("B", "D"); f.seg("B", "C"); f.seg("C", "D"); f.seg("O", "C")
    f.right("C", "B", "D")
    return f


def h_bai5():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    D = (-B[0], -B[1])
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "A"); f.seg("B", "C")
    f.seg("B", "D"); f.seg("C", "D")
    f.right("H", "B", "A")
    f.right("C", "B", "D")
    return f


def h_btvn1():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C"); f.seg("O", "A")
    f.right("B", "A", "O")
    f.right("C", "A", "O")
    return f


def h_btvn2():
    f = Fig()
    O, R, S = (0, 0), 1.2, (2.8, 0)
    A, B = tangent_points(O, R, S)
    if A[1] < B[1]: A, B = B, A
    H = foot(A, (0, 0), S)
    for n, p in [("O", O), ("S", S), ("A", A), ("B", B), ("H", H)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("S", "A"); f.seg("S", "B"); f.seg("O", "A"); f.seg("O", "B")
    f.seg("O", "S"); f.seg("A", "B")
    f.right("A", "S", "O")
    f.right("H", "A", "S")
    return f


def khung(tikz: str) -> str:
    xy = [(float(a), float(b)) for a, b in re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)", tikz)]
    xs, ys = [p[0] for p in xy], [p[1] for p in xy]
    return f"  \\path ({min(xs) - 0.15:.4f},{min(ys) - 0.15:.4f}) rectangle ({max(xs) + 0.15:.4f},{max(ys) + 0.15:.4f});"


def h_bai6_gv():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    B, C = tangent_points(O, R, A)
    if B[1] < C[1]: B, C = C, B
    H = foot(B, (0, 0), A)
    D = (-B[0], -B[1])
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C"); f.seg("O", "A"); f.seg("B", "C")
    f.seg("B", "D"); f.seg("C", "D")
    f.right("B", "A", "O")
    f.right("C", "A", "O")
    f.right("H", "B", "A")
    f.right("C", "B", "D")
    return f


def h_bai6_nen():
    f = Fig()
    O, R, A = (0, 0), 1.2, (2.8, 0)
    for n, p in [("O", O), ("A", A)]:
        f.pt(n, p)
    f.circle(O, R)
    gv_tikz = h_bai6_gv().tikz()
    return f.tikz().replace("\\end{tikzpicture}", khung(gv_tikz) + "\n\\end{tikzpicture}")


def h_btvn3_gv():
    f = Fig()
    O, R, S = (0, 0), 1.2, (2.8, 0)
    A, B = tangent_points(O, R, S)
    if A[1] < B[1]: A, B = B, A
    H = foot(A, (0, 0), S)
    D = (-B[0], -B[1])
    for n, p in [("O", O), ("S", S), ("A", A), ("B", B), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.circle(O, R)
    f.seg("S", "A"); f.seg("S", "B"); f.seg("O", "A"); f.seg("O", "B"); f.seg("O", "S"); f.seg("A", "B")
    f.seg("B", "D"); f.seg("A", "D")
    f.right("A", "S", "O")
    f.right("B", "S", "O")
    f.right("H", "A", "S")
    f.right("A", "B", "D")
    return f


def h_btvn3_nen():
    f = Fig()
    O, R, S = (0, 0), 1.2, (2.8, 0)
    for n, p in [("O", O), ("S", S)]:
        f.pt(n, p)
    f.circle(O, R)
    gv_tikz = h_btvn3_gv().tikz()
    return f.tikz().replace("\\end{tikzpicture}", khung(gv_tikz) + "\n\\end{tikzpicture}")


def main():
    phieu = {
        "slug": "phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc",
        "title": "Tính chất hai tiếp tuyến cắt nhau. Chứng minh vuông góc, song song",
        "eyebrow": "PHIẾU 3 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 16",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "btvn_phieu_rieng": True,
        "stages": [
            {
                "kind": "review",
                "number": 1,
                "title": "Khám phá",
                "blocks": [
                    {
                        "type": "para",
                        "text": "\\textbf{Đứng ở một điểm, nhìn sát hai mép bồn hoa tròn}"
                    },
                    {
                        "type": "noted",
                        "variant": "note",
                        "text": "Bạn An đứng ở điểm $A$ ngoài một bồn hoa hình tròn tâm $O$. Hai tia nhìn của An tiếp xúc với mép bồn hoa tại $B$ và $C$ (Hình 1). Coi vành bồn hoa là đường tròn $(O)$, hai tia nhìn $AB$, $AC$ là hai tiếp tuyến của $(O)$.[[br]]Bằng quan sát thực tế và tính chất đối xứng, An nhận thấy khoảng cách từ chỗ đứng đến hai điểm chạm $AB$ và $AC$ bằng nhau; đồng thời hướng nhìn thẳng đến tâm bồn hoa $AO$ chia đôi góc nhìn $\\widehat{BAC}$.",
                        "figure": fig(h_khampha(), "Hình 1")
                    }
                ]
            },
            {
                "kind": "concept",
                "number": 2,
                "title": "Kiến thức trọng tâm",
                "blocks": [
                    {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                    card(
                        "\\nhanly{Định lí (Bài 16 SGK):} Nếu hai tiếp tuyến của đường tròn $(O)$ cắt nhau tại $A$ ($B$, $C$ là hai tiếp điểm) thì:[[br]]"
                        "\\nhanly{1. Hai đoạn tiếp tuyến bằng nhau:} $AB = AC$.[[br]]"
                        "\\nhanly{2. Phân giác góc tại $A$:} Tia $AO$ là tia phân giác của góc $\\widehat{BAC}$ tạo bởi hai tiếp tuyến.[[br]]"
                        "\\nhanly{3. Phân giác góc tại $O$:} Tia $OA$ là tia phân giác của góc $\\widehat{BOC}$ tạo bởi hai bán kính đi qua các tiếp điểm.",
                        "Hai tiếp tuyến cắt nhau tại $A$",
                        h_concept1()
                    ),
                    card(
                        "\\nhanly{Đường trung trực (Lớp 7):} Điểm cách đều hai đầu mút của một đoạn thẳng thì nằm trên đường trung trực của đoạn thẳng đó ($AB = AC$ và $OB = OC \\Rightarrow OA$ là đường trung trực của $BC$).[[br]]"
                        "\\nhanly{Tính chất trung trực:} Nếu $OA$ là đường trung trực của $BC$ thì $OA \\perp BC$ tại trung điểm $H$ của $BC$.[[br]]"
                        "\\nhanly{Từ vuông góc đến song song (Lớp 7):} Hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba thì song song với nhau: $OA \\perp BC$ và $CD \\perp BC \\Rightarrow OA \\parallel CD$.",
                        "$OA$ là trung trực của $BC$ và $OA \\parallel CD$",
                        h_concept2()
                    ),
                    {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                    card(
                        "\\nhanly{Phương pháp.} Chứng minh $AO$ là đường trung trực của đoạn thẳng $BC$.[[br]]"
                        "\\nhanly{Bước 1:} Chỉ ra $AB = AC$ (tính chất hai tiếp tuyến cắt nhau).[[br]]"
                        "\\nhanly{Bước 2:} Chỉ ra $OB = OC = R$ (bán kính của $(O)$).[[br]]"
                        "\\nhanly{Bước 3:} Kết luận $AO$ là đường trung trực của đoạn thẳng $BC \\Rightarrow AO \\perp BC$ tại $H$ (và $H$ là trung điểm của $BC$).",
                        "Chứng minh $AO \\perp BC$ tại $H$",
                        h_concept3()
                    ),
                    card(
                        "\\nhanly{Phương pháp.} Chứng minh hai đường thẳng cùng vuông góc với một đường thẳng thứ ba.[[br]]"
                        "\\nhanly{Bước 1:} Với đường kính $BD$ và $C \\in (O)$: tam giác $\\triangle BCD$ nội tiếp đường tròn có $BD$ là đường kính $\\Rightarrow \\triangle BCD$ vuông tại $C \\Rightarrow CD \\perp BC$.[[br]]"
                        "\\nhanly{Bước 2:} Đã có $AO \\perp BC$ (theo Dạng 1).[[br]]"
                        "\\nhanly{Bước 3:} Kết luận $AO \\parallel CD$ (vì cùng vuông góc với $BC$).",
                        "Chứng minh $AO \\parallel CD$",
                        h_concept4()
                    )
                ]
            },
            {
                "kind": "practice1",
                "number": 3,
                "title": "Luyện tập 1",
                "blocks": [
                    {
                        "type": "para",
                        "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Phúc Đồng) — ý a chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn; ý b chứng minh $OA \\perp BC$ tại $H$ và $OA \\parallel CD$. Hai mạch dưới đây sẽ luyện từng ý."
                    },
                    {
                        "type": "para",
                        "variant": "heading",
                        "text": "Mạch 1. Ý a và ý b1 — Bốn điểm và chứng minh $OA \\perp BC$"
                    },
                    P(
                        "Bài 1.", "NB1", "onclass",
                        mcq(
                            "Cho điểm $M$ nằm ngoài đường tròn $(O)$, kẻ hai tiếp tuyến $MA$ và $MB$ ($A$, $B$ là hai tiếp điểm). Nhận xét nào sau đây \\textbf{sai}?",
                            ["$MA = MB$", "$MO$ là tia phân giác của $\\widehat{AMB}$", "$OM$ là tia phân giác của $\\widehat{AOB}$", "$MO = MA$"],
                            tag="[NB] ", cols=2
                        )[0],
                        answer="D",
                        level=1,
                        figure=fig(h_bai1(), "Hình 2"),
                        slide=mcq(
                            "Cho điểm $M$ nằm ngoài đường tròn $(O)$, kẻ hai tiếp tuyến $MA$ và $MB$ ($A$, $B$ là hai tiếp điểm). Nhận xét nào sau đây \\textbf{sai}?",
                            ["$MA = MB$", "$MO$ là tia phân giác của $\\widehat{AMB}$", "$OM$ là tia phân giác của $\\widehat{AOB}$", "$MO = MA$"],
                            tag="[NB] ", cols=2
                        )[1]
                    ),
                    P(
                        "Bài 2.", "NB2", "onclass",
                        mcq(
                            "Cho đoạn thẳng $BC$. Hai điểm $A$ và $O$ nằm về hai phía của $BC$ sao cho $AB = AC$ và $OB = OC$. Khẳng định nào sau đây \\textbf{đúng}?",
                            ["$AO$ là đường trung trực của đoạn thẳng $BC$", "$BC$ là đường trung trực của đoạn thẳng $AO$", "$AO \\parallel BC$", "$AO = BC$"],
                            tag="[NB] ", cols=2
                        )[0],
                        answer="A",
                        level=1,
                        figure=fig(h_bai2(), "Hình 3"),
                        slide=mcq(
                            "Cho đoạn thẳng $BC$. Hai điểm $A$ và $O$ nằm về hai phía của $BC$ sao cho $AB = AC$ và $OB = OC$. Khẳng định nào sau đây \\textbf{đúng}?",
                            ["$AO$ là đường trung trực của đoạn thẳng $BC$", "$BC$ là đường trung trực của đoạn thẳng $AO$", "$AO \\parallel BC$", "$AO = BC$"],
                            tag="[NB] ", cols=2
                        )[1]
                    ),
                    {
                        "type": "noted",
                        "variant": "example",
                        "text": "\\textbf{Ví dụ 1.} (SGK Ví dụ 2 Bài 16) Cho hai tiếp tuyến $MA$ và $MB$ của đường tròn $(O; R)$ ($A$, $B$ là hai tiếp điểm). Gọi $I$ là giao điểm của $OM$ và $AB$.[[br]]"
                                "Chứng minh rằng $OM \\perp AB$ tại $I$ và $I$ là trung điểm của $AB$.[[br]]"
                                f"{LG}[[br]]"
                                "Vì $MA$ và $MB$ là hai tiếp tuyến của $(O)$ cắt nhau tại $M$[[br]]"
                                "$\\Rightarrow MA = [[fill:MB]]$ (tính chất hai tiếp tuyến cắt nhau).[[br]]"
                                "Lại có $OA = OB = [[fill:R]]$ (bán kính của $(O)$).[[br]]"
                                "$\\Rightarrow OM$ là đường trung trực của đoạn thẳng $[[fill:AB]]$.[[br]]"
                                "$\\Rightarrow OM \\perp AB$ tại $I$ và $I$ là trung điểm của $AB$ (tính chất đường trung trực).[[br]]"
                                "Vậy $OM \\perp AB$ tại $I$ và $I$ là $[[fill:trung điểm]]$ của $AB$.",
                        "figure": fig(h_vidu1(), "Hình 4")
                    },
                    P(
                        "Bài 3.", "NB4", "onclass",
                        "Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là các tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$.[[br]]"
                        f"{KG}[[br]]"
                        "a) [NB] Chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn:[[br]]"
                        "Vì $AB$ là tiếp tuyến của $(O)$ tại $B$ $\\Rightarrow AB \\perp OB$ tại $B$[[br]]"
                        "$\\Rightarrow \\triangle ABO$ vuông tại $B$[[br]]"
                        "$\\Rightarrow A, B, O$ cùng thuộc đường tròn đường kính $[[blank:1.4cm]]$.[[br]]"
                        "Vì $AC$ là tiếp tuyến của $(O)$ tại $C$ $\\Rightarrow AC \\perp OC$ tại $C$[[br]]"
                        "$\\Rightarrow \\triangle ACO$ vuông tại $C$[[br]]"
                        "$\\Rightarrow A, C, O$ cùng thuộc đường tròn đường kính $[[blank:1.4cm]]$.[[br]]"
                        "Vậy bốn điểm $A, B, C, O$ cùng thuộc đường tròn đường kính $[[blank:1.4cm]]$.[[br]]"
                        "b) [NB] Chứng minh $OA \\perp BC$ tại $H$:[[br]]"
                        "Ta có: $AB = AC$ (tính chất hai tiếp tuyến $[[blank:2.0cm]]$)[[br]]"
                        "và $OB = OC = [[blank:1.0cm]]$[[br]]"
                        "$\\Rightarrow OA$ là đường trung trực của đoạn thẳng $[[blank:1.2cm]]$[[br]]"
                        "$\\Rightarrow OA \\perp BC$ tại $H$ và $H$ là trung điểm của $BC$ (tính chất đường trung trực).[[br]]"
                        "Vậy $OA \\perp BC$ tại $H$.",
                        answer="a) $AO$; $AO$; $AO$.[[br]]b) cắt nhau; $R$; $BC$; Vậy $OA \\perp BC$ tại $H$.",
                        level=1,
                        figure=fig(h_bai3(), "Hình 5"),
                        hints=["Góc vuông lấy từ tiếp tuyến vuông góc bán kính tại tiếp điểm", "Điểm cách đều hai đầu mút đoạn thẳng nằm trên đường trung trực"]
                    ),
                    {
                        "type": "para",
                        "variant": "heading",
                        "text": "Mạch 2. Ý b2 — Chứng minh hai đường thẳng song song"
                    },
                    {
                        "type": "noted",
                        "variant": "example",
                        "text": "\\textbf{Ví dụ 2.} (Đề Ba Đình 2024) Cho nửa đường tròn $(O)$ đường kính $AB$. Kẻ tiếp tuyến $Ax$ cùng phía với nửa đường tròn. Lấy điểm $D$ thuộc nửa đường tròn ($D \\neq A, D \\neq B$). Tiếp tuyến tại $D$ của nửa đường tròn cắt $Ax$ tại $C$. Gọi $I$ là giao điểm của $OC$ và $AD$.[[br]]"
                                "Chứng minh rằng $OC \\perp AD$ tại $I$ và $OC \\parallel BD$.[[br]]"
                                f"{LG}[[br]]"
                                "a) Vì $CA$ và $CD$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$[[br]]"
                                "$\\Rightarrow CA = [[fill:CD]]$ và $OA = OD = R$.[[br]]"
                                "$\\Rightarrow OC$ là đường trung trực của đoạn thẳng $[[fill:AD]]$.[[br]]"
                                "$\\Rightarrow OC \\perp AD$ tại trung điểm $I$ của $AD$ (tính chất đường trung trực).[[br]]"
                                "Vậy $OC \\perp AD$ tại $I$.[[br]]"
                                "b) Điểm $D$ thuộc nửa đường tròn đường kính $AB$[[br]]"
                                "$\\Rightarrow \\triangle ABD$ vuông tại $[[fill:D]]$[[br]]"
                                "$\\Rightarrow BD \\perp [[fill:AD]]$.[[br]]"
                                "Lại có $OC \\perp AD$ (theo câu a).[[br]]"
                                "$\\Rightarrow OC \\parallel BD$ (vì cùng vuông góc với $[[fill:AD]]$).[[br]]"
                                "Vậy $[[fill:OC \\parallel BD]]$.",
                        "figure": fig(h_vidu2(), "Hình 6")
                    },
                    P(
                        "Bài 4.", "NB5", "onclass",
                        "Cho đường tròn $(O)$ đường kính $BD$. Lấy điểm $C$ thuộc $(O)$ ($C$ khác $B$ và $D$).[[br]]"
                        f"{KG}[[br]]"
                        "Chứng minh $CD \\perp BC$:[[br]]"
                        "Xét $\\triangle BCD$ có $O$ là trung điểm của đường kính $BD$[[br]]"
                        "và điểm $C \\in (O)$ nên $OC = OB = OD = [[blank:1.0cm]]$[[br]]"
                        "Do đó đường trung tuyến $CO = \\frac{1}{2}BD$[[br]]"
                        "$\\Rightarrow \\triangle BCD$ vuông tại $[[blank:1.1cm]]$[[br]]"
                        "$\\Rightarrow CD \\perp BC$ tại $C$.[[br]]"
                        "Vậy $CD \\perp BC$.",
                        answer="$R$; $C$; Vậy $CD \\perp BC$.",
                        level=1,
                        figure=fig(h_bai4(), "Hình 7"),
                        hints=["Tam giác có đường trung tuyến bằng nửa cạnh huyền là tam giác vuông"]
                    ),
                    P(
                        "Bài 5.", "NB6", "onclass",
                        "Cho đường tròn $(O)$ có hai tiếp tuyến $AB$, $AC$ cắt nhau tại $A$ ($B$, $C$ là hai tiếp điểm), $OA$ cắt $BC$ tại $H$. Kẻ đường kính $BD$. Biết $OA \\perp BC$ tại $H$.[[br]]"
                        f"{KG}[[br]]"
                        "a) [NB] Chứng minh $CD \\perp BC$:[[br]]"
                        "Xét $\\triangle BCD$ nội tiếp đường tròn $(O)$ có đường kính $BD$[[br]]"
                        "$\\Rightarrow \\triangle BCD$ vuông tại $C$[[br]]"
                        "$\\Rightarrow CD \\perp [[blank:1.1cm]]$ tại $C$.[[br]]"
                        "Vậy $CD \\perp BC$.[[br]]"
                        "b) [NB] Chứng minh $OA \\parallel CD$:[[br]]"
                        "Theo giả thiết, ta có: $OA \\perp [[blank:1.1cm]]$ tại $H$.[[br]]"
                        "Lại có $CD \\perp BC$ (theo câu a).[[br]]"
                        "Vì cả $OA$ và $CD$ cùng vuông góc với đoạn thẳng $[[blank:1.1cm]]$[[br]]"
                        "$\\Rightarrow OA \\parallel CD$.[[br]]"
                        "Vậy $OA \\parallel CD$.",
                        answer="a) $BC$; Vậy $CD \\perp BC$.[[br]]b) $BC$; $BC$; Vậy $OA \\parallel CD$.",
                        level=1,
                        figure=fig(h_bai5(), "Hình 8"),
                        hints=["Hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba thì song song"]
                    )
                ]
            },
            {
                "kind": "practice2",
                "number": 4,
                "title": "Luyện tập 2",
                "blocks": [
                    {
                        "type": "para",
                        "variant": "heading",
                        "text": "Đề thi Học kì I — THCS Phúc Đồng (Long Biên)"
                    },
                    P(
                        "Bài 6.", "TH1+VD1", "onclass",
                        "Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn $(O)$. Từ $A$ vẽ hai tiếp tuyến $AB$ và $AC$ của đường tròn $(O)$ ($B$, $C$ là hai tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$. Từ $B$ vẽ đường kính $BD$ của $(O)$.[[br]]"
                        "a) [TH] Chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn.[[br]]"
                        "b) [TH] Chứng minh rằng $OA \\perp BC$ tại $H$.[[br]]"
                        "c) [VD] Chứng minh $OA \\parallel CD$.",
                        answer="a) Vì $AB$ là tiếp tuyến của $(O)$ tại $B$[[br]]"
                               "$\\Rightarrow AB \\perp OB$ tại $B$[[br]]"
                               "$\\Rightarrow \\triangle ABO$ vuông tại $B$[[br]]"
                               "$\\Rightarrow A, B, O$ cùng thuộc đường tròn đường kính $AO$.[[br]]"
                               "Vì $AC$ là tiếp tuyến của $(O)$ tại $C$[[br]]"
                               "$\\Rightarrow AC \\perp OC$ tại $C$[[br]]"
                               "$\\Rightarrow \\triangle ACO$ vuông tại $C$[[br]]"
                               "$\\Rightarrow A, C, O$ cùng thuộc đường tròn đường kính $AO$.[[br]]"
                               "Vậy bốn điểm $A, B, C, O$ cùng thuộc đường tròn đường kính $AO$.[[br]]"
                               "b) Ta có: $AB = AC$ (tính chất hai tiếp tuyến cắt nhau)[[br]]"
                               "và $OB = OC = R$ (bán kính $(O)$)[[br]]"
                               "$\\Rightarrow OA$ là đường trung trực của đoạn thẳng $BC$[[br]]"
                               "$\\Rightarrow OA \\perp BC$ tại $H$ (tính chất đường trung trực).[[br]]"
                               "Vậy $OA \\perp BC$ tại $H$.[[br]]"
                               "c) Xét $\\triangle BCD$ có $O$ là trung điểm của $BD$ (đường kính $BD$)[[br]]"
                               "và $C \\in (O)$ nên $OC = OB = OD = R$[[br]]"
                               "$\\Rightarrow \\triangle BCD$ vuông tại $C$[[br]]"
                               "$\\Rightarrow CD \\perp BC$.[[br]]"
                               "Vì $OA \\perp BC$ (theo câu b) và $CD \\perp BC$[[br]]"
                               "$\\Rightarrow OA \\parallel CD$.[[br]]"
                               "Vậy $OA \\parallel CD$.",
                        level=2,
                        draw=True,
                        figure={
                            "tikz": h_bai6_nen(),
                            "tikz_gv": h_bai6_gv().tikz(),
                            "caption": "Hình 9",
                            "pos": "right"
                        },
                        hints=[
                            "Dùng tam giác vuông nội tiếp đường tròn đường kính cạnh huyền để chứng minh bốn điểm cùng thuộc đường tròn",
                            "Dùng tính chất hai tiếp tuyến cắt nhau để chỉ ra đường trung trực của đoạn thẳng",
                            "Hai đường thẳng phân biệt cùng vuông góc với một đường thẳng thì song song"
                        ],
                        quy_trinh=[
                            "Ý a: $AB \\perp OB, AC \\perp OC \\Rightarrow A, B, C, O$ cùng thuộc đường tròn đường kính $AO$ (như Buổi 2)",
                            "Ý b: $AB = AC, OB = OC = R \\Rightarrow OA$ là đường trung trực của $BC \\Rightarrow OA \\perp BC$ tại $H$ (như Bài 3)",
                            "Ý c: $\\triangle BCD$ có đường kính $BD \\Rightarrow CD \\perp BC$ (như Bài 4)",
                            "Vì $OA \\perp BC$ và $CD \\perp BC \\Rightarrow OA \\parallel CD$ (như Bài 5)"
                        ]
                    )
                ]
            },
            {
                "kind": "reflection",
                "number": 5,
                "title": "Sơ đồ tư duy",
                "blocks": [
                    {
                        "type": "mindmap",
                        "caption": "Sơ đồ tư duy: Tính chất hai tiếp tuyến cắt nhau. Chứng minh vuông góc, song song",
                        "root": "HAI TIẾP TUYẾN CẮT NHAU",
                        "branches": [
                            {
                                "label": "TÍNH CHẤT HAI TIẾP TUYẾN",
                                "children": [
                                    {"label": "Khoảng cách bằng nhau: $AB = AC$"},
                                    {"label": "Tia $AO$ là phân giác $\\widehat{BAC}$"},
                                    {"label": "Tia $OA$ là phân giác $\\widehat{BOC}$"}
                                ]
                            },
                            {
                                "label": "CHỨNG MINH $AO \\perp BC$",
                                "children": [
                                    {"label": "$AB = AC$ (t/c hai tiếp tuyến)"},
                                    {"label": "$OB = OC = R$ (bán kính)"},
                                    {"label": "$AO$ là đường trung trực của $BC$"},
                                    {"label": "Kết luận: $AO \\perp BC$ tại $H$ và $HB = HC$"}
                                ]
                            },
                            {
                                "label": "CHỨNG MINH SONG SONG",
                                "children": [
                                    {"label": "$BD$ là đường kính $\\Rightarrow \\triangle BCD$ vuông tại $C$"},
                                    {"label": "Suy ra $CD \\perp BC$"},
                                    {"label": "Có $AO \\perp BC$ (trung trực)"},
                                    {"label": "Cùng $\\perp BC \\Rightarrow AO \\parallel CD$"}
                                ]
                            }
                        ]
                    },
                    P(
                        "BTVN 1.", "NB3", "btvn",
                        mcq(
                            "Bạn Mai mở chiếc compa vẽ một đường tròn $(O; R)$. Hai chân compa $AB$ và $AC$ tiếp xúc với đường tròn tại $B$ và $C$ tạo thành góc $\\widehat{BAC} = 60^\\circ$ (Hình 10). Khẳng định nào sau đây \\textbf{sai}?",
                            ["$\\widehat{BOC} = 120^\\circ$", "$AO$ là tia phân giác của $\\widehat{BAC}$", "$\\widehat{BAO} = 30^\\circ$", "$\\triangle ABC$ vuông tại $A$"],
                            tag="[NB] ", cols=2
                        )[0],
                        answer="D",
                        level=1,
                        figure=fig(h_btvn1(), "Hình 10"),
                        slide=mcq(
                            "Bạn Mai mở chiếc compa vẽ một đường tròn $(O; R)$. Hai chân compa $AB$ và $AC$ tiếp xúc với đường tròn tại $B$ và $C$ tạo thành góc $\\widehat{BAC} = 60^\\circ$ (Hình 10). Khẳng định nào sau đây \\textbf{sai}?",
                            ["$\\widehat{BOC} = 120^\\circ$", "$AO$ là tia phân giác của $\\widehat{BAC}$", "$\\widehat{BAO} = 30^\\circ$", "$\\triangle ABC$ vuông tại $A$"],
                            tag="[NB] ", cols=2
                        )[1]
                    ),
                    P(
                        "BTVN 2.", "NB6", "btvn",
                        "Cho đường tròn $(O)$ và điểm $S$ nằm ngoài đường tròn. Vẽ hai tiếp tuyến $SA$, $SB$ ($A$, $B$ là hai tiếp điểm). Gọi $H$ là giao điểm của $SO$ và $AB$.[[br]]"
                        f"{KG}[[br]]"
                        "a) [NB] Nêu tính chất hai tiếp tuyến cắt nhau:[[br]]"
                        "Vì $SA$ và $SB$ là hai [[blank:2.0cm]] của $(O)$ cắt nhau tại $S$[[br]]"
                        "$\\Rightarrow SA = [[blank:1.1cm]]$ (tính chất hai tiếp tuyến [[blank:1.8cm]]).[[br]]"
                        "Lại có $OA = OB = [[blank:1.0cm]]$ (bán kính của $(O)$).[[br]]"
                        "Vậy $SA = SB$ và $OA = OB = R$.[[br]]"
                        "b) [NB] Chứng minh $SO$ là đường trung trực của đoạn thẳng $AB$:[[br]]"
                        "Vì $SA = SB$ và $OA = OB$ (theo câu a)[[br]]"
                        "$\\Rightarrow SO$ là đường [[blank:2.2cm]] của đoạn thẳng $[[blank:1.1cm]]$.[[br]]"
                        "Vậy $SO$ là đường trung trực của đoạn thẳng $AB$.[[br]]"
                        "c) [NB] Chứng minh $SO \\perp AB$ tại $H$:[[br]]"
                        "Vì $SO$ là đường trung trực của đoạn thẳng $AB$ (theo câu b)[[br]]"
                        "$\\Rightarrow SO \\perp AB$ tại $H$ và $H$ là [[blank:2.0cm]] của $AB$ (tính chất đường trung trực).[[br]]"
                        "Vậy $SO \\perp AB$ tại $H$.",
                        answer="a) tiếp tuyến; $SB$; cắt nhau; $R$; Vậy $SA = SB$ và $OA = OB = R$.[[br]]b) trung trực; $AB$; Vậy $SO$ là đường trung trực của đoạn thẳng $AB$.[[br]]c) trung điểm; Vậy $SO \\perp AB$ tại $H$.",
                        level=1,
                        figure=fig(h_btvn2(), "Hình 11")
                    ),
                    P(
                        "BTVN 3.", "TH1+VD1", "btvn",
                        "Cho đường tròn tâm $O$ và điểm $S$ nằm ngoài đường tròn, vẽ hai tiếp tuyến $SA$, $SB$ ($A$, $B$ là hai tiếp điểm). $AB$ cắt $SO$ tại $H$, vẽ đường kính $BD$.[[br]]"
                        "a) [TH] Chứng minh bốn điểm $S$, $A$, $B$, $O$ cùng thuộc một đường tròn.[[br]]"
                        "b) [VD] Chứng minh $SO \\perp AB$ tại $H$ và $AD \\parallel SO$.",
                        answer="a) Vì $SA$ là tiếp tuyến của $(O)$ tại $A$[[br]]"
                               "$\\Rightarrow SA \\perp OA$ tại $A$[[br]]"
                               "$\\Rightarrow \\triangle SAO$ vuông tại $A$[[br]]"
                               "$\\Rightarrow S, A, O$ cùng thuộc đường tròn đường kính $SO$.[[br]]"
                               "Vì $SB$ là tiếp tuyến của $(O)$ tại $B$[[br]]"
                               "$\\Rightarrow SB \\perp OB$ tại $B$[[br]]"
                               "$\\Rightarrow \\triangle SBO$ vuông tại $B$[[br]]"
                               "$\\Rightarrow S, B, O$ cùng thuộc đường tròn đường kính $SO$.[[br]]"
                               "Vậy bốn điểm $S, A, B, O$ cùng thuộc đường tròn đường kính $SO$.[[br]]"
                               "b) Ta có: $SA = SB$ (tính chất hai tiếp tuyến cắt nhau)[[br]]"
                               "và $OA = OB = R$ (bán kính của $(O)$)[[br]]"
                               "$\\Rightarrow SO$ là đường trung trực của đoạn thẳng $AB$[[br]]"
                               "$\\Rightarrow SO \\perp AB$ tại $H$ (tính chất đường trung trực).[[br]]"
                               "Xét $\\triangle ABD$ có $O$ là trung điểm của đường kính $BD$ và $A \\in (O)$[[br]]"
                               "$\\Rightarrow \\triangle ABD$ vuông tại $A$[[br]]"
                               "$\\Rightarrow AD \\perp AB$.[[br]]"
                               "Vì $SO \\perp AB$ và $AD \\perp AB$[[br]]"
                               "$\\Rightarrow AD \\parallel SO$.[[br]]"
                               "Vậy $SO \\perp AB$ tại $H$ và $AD \\parallel SO$.",
                        level=2,
                        draw=True,
                        figure={
                            "tikz": h_btvn3_nen(),
                            "tikz_gv": h_btvn3_gv().tikz(),
                            "caption": "Hình 12",
                            "pos": "right"
                        },
                        hints=[
                            "Dùng tam giác vuông nội tiếp đường tròn đường kính cạnh huyền để chứng minh bốn điểm cùng thuộc đường tròn",
                            "Dùng tính chất hai tiếp tuyến cắt nhau để chỉ ra đường trung trực của đoạn thẳng",
                            "Hai đường thẳng phân biệt cùng vuông góc với một đường thẳng thì song song"
                        ]
                    )
                ]
            }
        ]
    }

    out_path = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json"
    out_path.write_text(json.dumps(phieu, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
