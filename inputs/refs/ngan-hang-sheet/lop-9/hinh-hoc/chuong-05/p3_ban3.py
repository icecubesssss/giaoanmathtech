#!/usr/bin/env python3
"""Phiếu 3 ch.V 9C — dựng lại theo bản mẫu phiếu 2 (sơ đồ ngược, Thầy giao 05/11/2026).

Đề soi từ ẢNH: Phúc Đồng 2025 IV.2 a, b · Nguyễn Bỉnh Khiêm 2025 Câu 4.2 phần OD ⊥ AB của ý b ·
Lômônôxốp 2024 (Đề 2) IV.2 ý b · Ba Đình 2024 IV.2 ý b · Đống Đa 2025 IV.2 a, b · Phan Đình Giót 2024
IV.2 a, phần OM ⊥ AB của b · Xuân La 2024 Câu 4.2 phần OA ⊥ MN của ý b · Cầu Diễn 2025 Câu 4.2 phần OC ∥ MB của ý b ·
SGK KNTT 9 tập 1 tr.102 (Định lí 2, Ví dụ 2a) · STK Trương Ngọc Vỹ C7 tr.232, C13 tr.6, C60 tr.252.

Ghi đè seed phiếu 3 và dòng phiếu 3 trong thuyết minh, chạy lại được:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p3_ban3.py
Sau đó chạy scripts/phut_so_do.py <phiếu> --ghi rồi chép số phút vào PHUT dưới đây nếu đề đổi.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from p3_ban2 import (  # noqa: E402
    R, h_ba_dinh, h_cau_60, h_dong_da, h_lomonoxop, h_nen_duong_kinh_doc, h_nen_duong_kinh_ngang,
    h_nguyen_binh_khiem, h_nen_diem_ngoai, h_trung_truc_tron, nen,
)
from scripts.tikz_geo import Fig, foot, polar, tangent_points  # noqa: E402

D = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D / "phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json"
TM = D / "thuyet-minh.json"
BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"
R_THE = 1.2

# Phút có sơ đồ (scripts/phut_so_do.py), chưa gồm vẽ.
PHUT = {"Bài 3": 0, "Bài 4": 0, "BTVN 3": 0, "BTVN 4": 0}
if PHIEU.exists():
    for _st in json.loads(PHIEU.read_text("utf-8"))["stages"]:
        for _b in _st["blocks"]:
            if _b.get("phut_so_do"):
                PHUT[_b["label"].rstrip(".")] = _b["phut_so_do"]


GHI_CHU_LT1 = (
    "Hai ví dụ: GV vẽ trên bảng, HS vẽ cùng vào hình nền trên phiếu (Ví dụ 1: hai tiếp tuyến, các đoạn $OA$, $OB$, $OM$, $AB$; "
    "Ví dụ 2: tia $Ax$, điểm $C$, tiếp tuyến $CD$, các đoạn $OC$, $OD$, $AD$, $BD$). Khoảng 57 phút với lớp C: 2 trắc nghiệm ~5′, "
    "2 ví dụ GV giảng và cùng HS điền sơ đồ ngược ~22′ (gồm 5′ vẽ), Bài 3 HS vẽ tiếp, đọc sơ đồ ngược rồi trình bày vào vở ~12′, "
    "Bài 4 cùng cách ~18′."
)
GHI_CHU_LT2 = (
    "Khoảng 21 phút với lớp C: HS tự vẽ hình đề Phúc Đồng (~5′), tự trình bày ý b như Ví dụ 1, Bài 3 rồi Ví dụ 2, Bài 4 (~16′). "
    "Ý a đã học ở Phiếu 2, GV chữa ở phần chữa bài cuối buổi."
)
GHI_CHU_BTVN = (
    "BTVN khoảng 66 phút với lớp C, dày hơn quỹ 40 phút để HS có thêm bài: BTVN 1 trả lời ngắn (~3′), BTVN 2 vẽ tiếp hình rồi điền khung (~9′), "
    "BTVN 3 tự vẽ hình, đọc sơ đồ ngược rồi trình bày vào vở (~14′), BTVN 4 cùng cách, chứng minh song song (~14′), "
    "BTVN 5 tự vẽ hình, tự trình bày như Bài 5 (~28′)."
)
GIO_THUC_TM = [
    "\\quad Giờ thực lớp C (05/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 57′ (2 trắc nghiệm, 2 ví dụ HS vẽ cùng GV và điền sơ đồ ngược, "
    "2 bài theo sơ đồ ngược HS trình bày vào vở $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 21′ (đề đích Phúc Đồng ý b, HS tự vẽ) · chữa bài (có ý a đề đích), chốt khoảng 5′ · BTVN khoảng 66′ (quỹ 40′, cố ý dày hơn)",
]


# ── Sơ đồ ngược ────────────────────────────────────────────────────────────────
HEAD = (
    "\\begin{tikzpicture}[font=\\small, >={Latex[length=1.8mm]},\n"
    "  o/.style={draw=stage2!70, fill=white, rounded corners=1.5pt, line width=0.5pt, inner sep=2pt, "
    "minimum height=0.5cm, align=center},\n"
    "  dich/.style={o, draw=stage2, fill=stage2!14},\n"
    "  gt/.style={o, draw=black!45, fill=black!8},\n"
    "  m/.style={->, line width=0.6pt, draw=stage2!80!black}]\n"
)
END = "\\end{tikzpicture}"


def sd_trung_truc(dich: str, giua: str, trai: str, phai: str) -> str:
    """Đích ⊥ ← đường trung trực ← hai ô xám."""
    return (
        HEAD
        + f"  \\node[dich] (g) at (0,0) {{{dich}}};\n"
        + f"  \\node[o] (a) at (0,-0.85) {{{giua}}};\n"
        + f"  \\node[gt] (l) at (-2.3,-1.85) {{{trai}}};\n  \\node[gt] (r) at (2.3,-1.85) {{{phai}}};\n"
        + "  \\draw[m] (a) -- (g);\n"
        + "  \\draw[m] (l.north) -- (l.north |- a.south);\n  \\draw[m] (r.north) -- (r.north |- a.south);\n"
        + END
    )


def sd_song_song(dich, trai1, trai2, trai_xam, phai1, phai2, phai3, phai_xam) -> str:
    """Đích ∥ ← hai đường cùng vuông góc. Nhánh trái: đường trung trực; nhánh phải: trung tuyến cho góc vuông."""
    return (
        HEAD
        + f"  \\node[dich] (g) at (0,0) {{{dich}}};\n"
        + f"  \\node[o] (a1) at (-2.5,-0.8) {{{trai1}}};\n  \\node[o] (b1) at (2.5,-0.8) {{{phai1}}};\n"
        + f"  \\node[o] (a2) at (-2.5,-1.75) {{{trai2}}};\n  \\node[o] (b2) at (2.5,-1.6) {{{phai2}}};\n"
        + f"  \\node[gt] (a3) at (-2.5,-3.05) {{{trai_xam}}};\n  \\node[o] (b3) at (2.5,-2.6) {{{phai3}}};\n"
        + f"  \\node[gt] (b4) at (2.5,-3.8) {{{phai_xam}}};\n"
        + "  \\draw[m] (a1.north) |- (g.west);\n  \\draw[m] (b1.north) |- (g.east);\n"
        + "  \\draw[m] (a2) -- (a1);\n  \\draw[m] (b2) -- (b1);\n"
        + "  \\draw[m] (a3) -- (a2);\n  \\draw[m] (b3) -- (b2);\n  \\draw[m] (b4) -- (b3);\n"
        + END
    )


def xam_tiep_tuyen(a, b, c, o="O"):
    return f"${a}{b} = {a}{c}$ (tính chất hai\\\\tiếp tuyến cắt nhau)", f"${o}{b} = {o}{c} = R$\\\\(bán kính của $(O)$)"


# ── Hình ───────────────────────────────────────────────────────────────────────
def hai_tt(ten_m, ten_a, ten_b, ten_h=None, r=R, xa=3.5, day_cung=True):
    """Hai tiếp tuyến từ điểm ngoài đường tròn; `ten_h` rỗng thì chân đường vuông góc không đặt tên."""
    f = Fig()
    O, M = (0, 0), (xa, 0)
    a, b = tangent_points(O, r, M)
    if a[1] < b[1]:
        a, b = b, a
    h = foot(a, O, M)
    f.circle(O, r)
    f.pt("O", O); f.pt(ten_m, M); f.pt(ten_a, a); f.pt(ten_b, b)
    if ten_h:
        f.pt(ten_h, h)
    for u, v in [(ten_m, ten_a), (ten_m, ten_b), ("O", ten_a), ("O", ten_b), ("O", ten_m)]:
        f.seg(u, v)
    if day_cung:
        f.seg(ten_a, ten_b)
        f.right(h, a, M)
    f.right(ten_a, O, M); f.right(ten_b, O, M)
    return f.tikz()


def h_kham_pha():
    f = Fig()
    O, A = (0, 0), (2.8, 0)
    b, c = tangent_points(O, R_THE, A)
    if b[1] < c[1]:
        b, c = c, b
    f.circle(O, R_THE)
    f.pt("O", O); f.pt("A", A); f.pt("B", b); f.pt("C", c)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("O", "B"); f.seg("O", "C")
    f.seg("A", "O", style="ink, dashed")
    return f.tikz()


def h_the_duong_kinh():
    """Thẻ Dạng 2 và kiến thức lớp dưới: đường kính BD, AO ⊥ BC tại H, CD ⊥ BC."""
    f = Fig()
    O, A = (0, 0), (2.8, 0)
    b, c = tangent_points(O, R_THE, A)
    if b[1] < c[1]:
        b, c = c, b
    h = foot(b, O, A)
    d = (-b[0], -b[1])
    f.circle(O, R_THE)
    f.pt("O", O); f.pt("A", A); f.pt("B", b); f.pt("C", c); f.pt("H", h); f.pt("D", d)
    for u, v in [("A", "B"), ("A", "C"), ("O", "A"), ("B", "C"), ("B", "D"), ("C", "D"), ("O", "C")]:
        f.seg(u, v)
    f.right(h, b, A); f.right("C", b, d)
    return f.tikz()


def h_phuc_dong():
    f = Fig()
    O, A = (0, 0), (3.5, 0)
    b, c = tangent_points(O, R, A)
    if b[1] < c[1]:
        b, c = c, b
    h = foot(b, O, A)
    d = (-b[0], -b[1])
    f.circle(O, R)
    f.pt("O", O); f.pt("A", A); f.pt("B", b); f.pt("C", c); f.pt("H", h); f.pt("D", d)
    for u, v in [("A", "B"), ("A", "C"), ("O", "C"), ("O", "A"), ("B", "C"), ("B", "D"), ("C", "D")]:
        f.seg(u, v)
    f.right("B", O, A); f.right("C", O, A); f.right(h, b, A); f.right("C", b, d)
    return f.tikz()


def _cau_dien_diem():
    O, A, B = (0.0, 0.0), (-R, 0.0), (R, 0.0)
    M = polar(120, R)
    y = lambda x: M[1] + (M[0] / M[1]) * (M[0] - x)  # noqa: E731  (tiếp tuyến tại M: OM·(P−M) = 0)
    C, Dd = (-R, y(-R)), (R, y(R))
    return O, A, B, M, C, Dd


def h_cau_dien():
    O, A, B, M, C, Dd = _cau_dien_diem()
    f = Fig()
    h = foot(M, O, C)
    f.circle(O, R)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("M", M); f.pt("C", C); f.pt("D", Dd)
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("O", "C"), ("O", "M"), ("A", "M"), ("M", "B")]:
        f.seg(u, v)
    f.right("A", O, C); f.right("M", O, C); f.right(h, A, C); f.right("M", A, B)
    return f.tikz()


def h_nen_tron_ngang(a, b, day_du):
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt(a, (-R, 0)); f.pt(b, (R, 0))
    f.seg(a, b)
    return nen(f, day_du)


_SO = r"\(\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\)"
_DOAN = re.compile(rf"\\draw\[[^\]]*\] {_SO} -- {_SO};")
_O_VUONG = re.compile(rf"^\s*\\draw\[ink\] {_SO} -- {_SO} -- {_SO};\n", re.M)


def bo_goc_bi_cat(tz: str) -> str:
    """Quy chuẩn hình 09/09/2026 mục 4: bỏ ô góc vuông bị một đoạn khác đi xuyên qua."""
    doan = [tuple(map(float, m.groups())) for m in _DOAN.finditer(tz)]

    def bi_cat(m) -> bool:
        x1, y1, x2, y2, x3, y3 = map(float, m.groups())
        vx, vy = x1 + x3 - x2, y1 + y3 - y2             # đỉnh góc: p1, p3 là hai chân, p2 là góc ngoài
        ux, uy, wx, wy = x1 - vx, y1 - vy, x3 - vx, y3 - vy
        det = ux * wy - uy * wx
        for a, b, c, d in doan:
            for ex, ey, fx, fy in ((a, b, c, d), (c, d, a, b)):
                # đoạn đi ra từ đỉnh, hoặc đoạn đi qua đỉnh
                tich = (vx - ex) * (fx - ex) + (vy - ey) * (fy - ey)
                cheo = (vx - ex) * (fy - ey) - (vy - ey) * (fx - ex)
                if abs(cheo) > 1e-3 or (tich < -1e-3):
                    continue
                dx, dy = ex - vx, ey - vy
                if math.hypot(dx, dy) < 1e-3:
                    dx, dy = fx - vx, fy - vy
                al = (dx * wy - dy * wx) / det
                be = (ux * dy - uy * dx) / det
                if al > 1e-3 and be > 1e-3:
                    return True
        return False

    return _O_VUONG.sub(lambda m: "" if bi_cat(m) else m.group(0), tz)


def gon_hinh(les: dict) -> dict:
    for st in les["stages"]:
        for b in st["blocks"]:
            fig = b.get("figure")
            if fig:
                for k in ("tikz", "tikz_gv"):
                    if fig.get(k):
                        fig[k] = bo_goc_bi_cat(fig[k])
    return les


def kiem_toan_do():
    """Kiểm hình bằng toạ độ: kết luận của đề phải đúng trên chính hình vẽ."""
    O, A, B, M, C, Dd = _cau_dien_diem()
    assert abs((C[0] - M[0]) * M[0] + (C[1] - M[1]) * M[1]) < 1e-9                 # CM ⊥ OM
    assert abs((Dd[0] - M[0]) * M[0] + (Dd[1] - M[1]) * M[1]) < 1e-9               # DM ⊥ OM
    assert abs(C[0] * (B[1] - M[1]) - C[1] * (B[0] - M[0])) < 1e-9                 # OC ∥ MB
    assert math.hypot(M[0] - A[0], M[1] - A[1]) < math.hypot(M[0] - B[0], M[1] - B[1])   # MA < MB
    assert abs(math.hypot(C[0] - A[0], C[1] - A[1]) - math.hypot(C[0] - M[0], C[1] - M[1])) < 1e-9  # CA = CM


# ── Đề, lời giải ───────────────────────────────────────────────────────────────
def giai_trung_truc(s, a, b, o="O", ket="", duong=""):
    duong = duong or f"{o}{s}"
    return (
        f"${s}{a}$, ${s}{b}$ là hai tiếp tuyến của $(O)$ cắt nhau tại ${s}$ $\\Rightarrow {s}{a} = {s}{b}$.{BR}"
        f"${o}{a} = {o}{b}$ (bán kính của $(O)$){BR}"
        f"$\\Rightarrow {duong}$ là đường trung trực của đoạn thẳng ${a}{b}${ket}"
    )


def giai_vuong(c, x, y, o="O"):
    return (
        f"Xét $\\triangle {x}{c}{y}$ có ${c}{o}$ là đường trung tuyến ứng với cạnh ${x}{y}$ "
        f"(${o}$ là trung điểm của ${x}{y}$).{BR}"
        f"${o}{c} = {o}{x} = {o}{y} = R \\Rightarrow {c}{o} = \\dfrac{{{x}{y}}}{{2}}${BR}"
        f"$\\Rightarrow \\triangle {x}{c}{y}$ vuông tại ${c}$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng){BR}"
        f"$\\Rightarrow {y}{c} \\perp {x}{c}$.{BR}"
    )


def giai_bon_diem(s, a, b, o="O"):
    return (
        f"${s}{a}$ là tiếp tuyến của $(O)$ tại ${a}$ $\\Rightarrow \\triangle {s}{a}{o}$ vuông tại ${a}${BR}"
        f"$\\Rightarrow {s}, {a}, {o}$ cùng thuộc đường tròn đường kính ${s}{o}$.{BR}"
        f"${s}{b}$ là tiếp tuyến của $(O)$ tại ${b}$ $\\Rightarrow \\triangle {s}{b}{o}$ vuông tại ${b}${BR}"
        f"$\\Rightarrow {s}, {b}, {o}$ cùng thuộc đường tròn đường kính ${s}{o}$.{BR}"
    )


def bai(label, level, tier, dang, statement, answer, **k):
    return {"type": "problem", "label": label, "level": level, "tier": tier, "dang_id": dang,
            "statement": statement, "answer": answer, **k}


def theo_so_do(n):
    return f"Vẽ tiếp vào Hình {n} các yếu tố còn thiếu theo đề, rồi dựa vào sơ đồ ngược để trình bày bài giải vào vở."


def lesson() -> dict:
    # ── Thẻ phương pháp ────────────────────────────────────────────────────────
    t1, t2 = xam_tiep_tuyen("A", "B", "C")
    the_dang_1 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 1. CHỨNG MINH VUÔNG GÓC BẰNG ĐƯỜNG TRUNG TRỰC",
        "text": "\\nhanly{Phương pháp.} dùng tính chất hai tiếp tuyến cắt nhau và đường trung trực.[[br]]"
                "\\nhanly{Bước 1:} Chỉ ra $AB = AC$ (tính chất hai tiếp tuyến cắt nhau).[[br]]"
                "\\nhanly{Bước 2:} Chỉ ra $OB = OC = R$ (bán kính của $(O)$).[[br]]"
                "\\nhanly{Bước 3:} Kết luận $OA$ là đường trung trực của đoạn thẳng $BC$ $\\Rightarrow OA \\perp BC$ tại $H$.",
        "figure": {"tikz": hai_tt("A", "B", "C", "H", r=R_THE, xa=2.8),
                   "caption": "$OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$ tại $H$", "pos": "right"},
        "so_do_nguoc": sd_trung_truc("$OA \\perp BC$ tại $H$", "$OA$ là đường trung trực của $BC$", t1, t2),
    }
    the_dang_2 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 2. CHỨNG MINH SONG SONG BẰNG HAI ĐƯỜNG CÙNG VUÔNG GÓC",
        "text": "\\nhanly{Phương pháp.} chỉ ra hai đường thẳng cùng vuông góc với một đường thẳng thứ ba.[[br]]"
                "\\nhanly{Bước 1:} Chỉ ra $OA \\perp BC$ (Dạng 1).[[br]]"
                "\\nhanly{Bước 2:} Chỉ ra $CD \\perp BC$. Góc vuông lấy từ đường kính $BD$: đường trung tuyến "
                "$CO = \\dfrac{BD}{2}$ $\\Rightarrow \\triangle BCD$ vuông tại $C$.[[br]]"
                "\\nhanly{Bước 3:} Kết luận $OA \\parallel CD$ (cùng vuông góc với $BC$).",
        "figure": {"tikz": h_the_duong_kinh(), "caption": "$OA$ và $CD$ cùng vuông góc với $BC$ $\\Rightarrow OA \\parallel CD$",
                   "pos": "right"},
        "so_do_nguoc": sd_song_song(
            "$OA \\parallel CD$", "$OA \\perp BC$", "$OA$ là đường trung trực\\\\của $BC$",
            "$AB = AC$; $OB = OC = R$\\\\(như Dạng 1)",
            "$CD \\perp BC$", "$\\triangle BCD$ vuông tại $C$", "$CO = \\dfrac{BD}{2}$",
            "$CO$ là đường trung tuyến;\\\\$OB = OC = OD = R$"),
    }

    # ── Ví dụ 1: SGK Ví dụ 2a ──────────────────────────────────────────────────
    vd1_gv = hai_tt("M", "A", "B")
    vi_du_1 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 1.} Cho hai tiếp tuyến $MA$ và $MB$ của đường tròn $(O; R)$ ($A$ và $B$ là hai tiếp điểm) (Hình 3). "
                "Vẽ tiếp vào Hình 3 các yếu tố còn thiếu theo đề. Chứng minh rằng $OM \\perp AB$."
                f"{BR}{LG}{BR}"
                f"$MA$, $MB$ là hai tiếp tuyến của $(O)$ cắt nhau tại $M$ $\\Rightarrow MA = [[fill:MB]]$.{BR}"
                f"$OA = OB$ ([[fill:bán kính]] của $(O)$){BR}"
                f"$\\Rightarrow OM$ là [[fill:đường trung trực]] của đoạn thẳng $AB$.{BR}"
                "Vậy $OM \\perp AB$ (tính chất [[fill:đường trung trực]]).",
        "figure": {"tikz": h_nen_diem_ngoai("M", vd1_gv), "tikz_gv": vd1_gv, "caption": "Hình 3", "pos": "right"},
        "so_do_nguoc": sd_trung_truc(
            "$OM \\perp AB$", "$OM$ là [[fill:đường trung trực|2.6cm]] của $AB$",
            "$MA = [[fill:MB]]$ (tính chất hai\\\\tiếp tuyến cắt nhau)", "$OA = OB$\\\\([[fill:bán kính|1.4cm]] của $(O)$)"),
    }

    # ── Bài 3: Nguyễn Bỉnh Khiêm, phần OD ⊥ AB của ý b ─────────────────────────
    nbk = h_nguyen_binh_khiem()
    t1, t2 = xam_tiep_tuyen("D", "A", "B")
    bai_3 = bai(
        "Bài 3.", 2, "onclass", "TH2",
        "[TH] Cho nửa đường tròn $(O; R)$ đường kính $BC$. Trên nửa đường tròn $(O)$ vẽ tiếp tuyến $Bx$ của đường tròn $(O)$, "
        "$A$ là điểm bất kì thuộc nửa đường tròn sao cho $AB < AC$ ($A$ khác $B$, $A$ khác $C$). Tiếp tuyến tại $A$ của nửa "
        f"đường tròn $(O)$ cắt tia $Bx$ tại $D$ (Hình 4). Chứng minh rằng $OD \\perp AB$. {theo_so_do(4)}",
        giai_trung_truc("D", "A", "B", ket=f".{BR}Vậy $OD \\perp AB$ (tính chất đường trung trực)."),
        figure={"tikz": h_nen_duong_kinh_ngang("B", "C", nbk), "tikz_gv": nbk, "caption": "Hình 4", "pos": "right"},
        so_do_nguoc=sd_trung_truc("$OD \\perp AB$", "$OD$ là đường trung trực của $AB$", t1, t2),
        phut_so_do=PHUT["Bài 3"], ve_tiep=3,
    )

    # ── Ví dụ 2: Ba Đình ý b ───────────────────────────────────────────────────
    bd = h_ba_dinh()
    vi_du_2 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 2.} Cho nửa đường tròn $(O)$ đường kính $AB = 2R$. Kẻ tiếp tuyến $Ax$ của đường tròn. Trên tia $Ax$ "
                "lấy điểm $C$ sao cho $AC > R$. Từ $C$ kẻ tiếp tuyến $CD$ của đường tròn $(O)$ ($D$ là tiếp điểm) (Hình 5). "
                "Vẽ tiếp vào Hình 5 các yếu tố còn thiếu theo đề. Chứng minh $OC$ vuông góc với $AD$ và $OC$ song song với $BD$."
                f"{BR}{LG}{BR}"
                f"$CA$, $CD$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$ $\\Rightarrow CA = [[fill:CD]]$.{BR}"
                f"$OA = OD$ ([[fill:bán kính]] của $(O)$){BR}"
                f"$\\Rightarrow OC$ là [[fill:đường trung trực]] của đoạn thẳng $AD${BR}"
                f"$\\Rightarrow OC \\perp AD$.{BR}"
                f"Xét $\\triangle ABD$ có $DO$ là đường [[fill:trung tuyến]] ứng với cạnh $AB$ ($O$ là trung điểm của $AB$).{BR}"
                f"$OD = OA = OB = R \\Rightarrow DO = \\dfrac{{1}}{{2}}[[fill:AB]]${BR}"
                f"$\\Rightarrow \\triangle ABD$ vuông tại $[[fill:D]]$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng){BR}"
                f"$\\Rightarrow BD \\perp AD$.{BR}"
                "Vậy $OC \\perp AD$ và $OC \\parallel BD$ (hai đường thẳng phân biệt cùng [[fill:vuông góc]] với $AD$).",
        "figure": {"tikz": h_nen_duong_kinh_doc("A", "B", nua=True, day_du=bd), "tikz_gv": bd, "caption": "Hình 5", "pos": "right"},
        "so_do_nguoc": sd_song_song(
            "$OC \\parallel BD$", "$OC \\perp AD$", "$OC$ là [[fill:đường trung trực|2.6cm]]\\\\của $AD$",
            "$CA = [[fill:CD]]$;\\\\$OA = OD$ ([[fill:bán kính|1.4cm]])",
            "$BD \\perp AD$", "$\\triangle ABD$ vuông tại $[[fill:D]]$", "$DO = \\dfrac{1}{2}[[fill:AB]]$",
            "$DO$ là đường [[fill:trung tuyến|1.8cm]];\\\\$OD = OA = OB = R$"),
    }

    # ── Bài 4: Lômônôxốp ý b ───────────────────────────────────────────────────
    lm = h_lomonoxop()
    bai_4 = bai(
        "Bài 4.", 2, "onclass", "TH3",
        "[TH] Cho đường tròn $(O)$, đường kính $MN$. Trên đường tròn $(O)$ lấy điểm $I$. Hai tiếp tuyến của đường tròn $(O)$ tại "
        f"$M$ và $I$ cắt nhau ở $K$ (Hình 6). Chứng minh $KO$ là đường trung trực của đoạn thẳng $MI$. Từ đó suy ra $KO \\parallel NI$. {theo_so_do(6)}",
        giai_trung_truc("K", "M", "I", duong="KO", ket=f"{BR}$\\Rightarrow KO \\perp MI$.{BR}")
        + giai_vuong("I", "M", "N")
        + "Vậy $KO \\parallel NI$ (hai đường thẳng phân biệt cùng vuông góc với $MI$).",
        figure={"tikz": h_nen_duong_kinh_doc("M", "N", day_du=lm), "tikz_gv": lm, "caption": "Hình 6", "pos": "right"},
        so_do_nguoc=sd_song_song(
            "$KO \\parallel NI$", "$KO \\perp MI$", "$KO$ là đường trung trực\\\\của $MI$",
            "$KM = KI$;\\\\$OM = OI = R$",
            "$NI \\perp MI$", "$\\triangle MIN$ vuông tại $I$", "$IO = \\dfrac{MN}{2}$",
            "$IO$ là đường trung tuyến;\\\\$OI = OM = ON = R$"),
        phut_so_do=PHUT["Bài 4"], ve_tiep=3,
    )

    # ── Bài 5: đích Phúc Đồng a, b ─────────────────────────────────────────────
    pd = h_phuc_dong()
    bai_5 = bai(
        "Bài 5.", 3, "onclass", "TH1+VD1",
        "Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn $(O)$. Từ $A$ vẽ hai tiếp tuyến $AB$ và $AC$ của đường tròn $(O)$ "
        "($B$, $C$ là hai tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$. Từ $B$ vẽ đường kính $BD$ của $(O)$.[[br]]"
        "a) [TH] Chứng minh bốn điểm $A$, $B$, $C$, $O$ cùng thuộc một đường tròn. Xác định tâm và bán kính của đường tròn đó.[[br]]"
        "b) [VD] Chứng minh rằng $OA \\perp BC$ tại $H$ và $OA \\parallel CD$.",
        "a) " + giai_bon_diem("A", "B", "C")
        + f"Vậy bốn điểm $A, B, C, O$ cùng thuộc đường tròn đường kính $AO$, tâm là trung điểm của $AO$, bán kính $\\dfrac{{AO}}{{2}}$.{BR}"
        + "b) " + giai_trung_truc("A", "B", "C", ket=f"{BR}$\\Rightarrow OA \\perp BC$ tại $H$.{BR}")
        + giai_vuong("C", "B", "D")
        + "Vậy $OA \\perp BC$ tại $H$ và $OA \\parallel CD$ (hai đường thẳng phân biệt cùng vuông góc với $BC$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_diem_ngoai("A", pd), "tikz_gv": pd, "caption": "Hình 7", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $BC$?",
               "Trong $\\triangle BCD$, đoạn $CO$ có quan hệ gì với cạnh $BD$?"],
        quy_trinh=["Vẽ tiếp hình: hai tiếp tuyến $AB$, $AC$; đoạn $OA$, $BC$ cắt nhau tại $H$; đường kính $BD$, đoạn $CD$; đánh dấu các góc vuông",
                   "Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $AO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $AO$",
                   "Ý b: $AB = AC$, $OB = OC = R$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$ tại $H$ (như Ví dụ 1, Bài 3)",
                   "$CO$ là đường trung tuyến, $CO = \\dfrac{BD}{2}$ $\\Rightarrow \\triangle BCD$ vuông tại $C$ $\\Rightarrow CD \\perp BC$ (như Ví dụ 2, Bài 4)",
                   "$OA$ và $CD$ cùng vuông góc với $BC$ $\\Rightarrow OA \\parallel CD$"],
    )

    # ── BTVN ───────────────────────────────────────────────────────────────────
    pdg = hai_tt("M", "A", "B", "H")
    khung = (
        "Vì $MA$ là [[blank:2.4cm]] của $(O)$ tại $A$ $\\Rightarrow \\triangle MAO$ vuông tại $[[blank:1.1cm]]$[[br]]"
        "$\\Rightarrow M, A, O$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "Vì $MB$ là tiếp tuyến của $(O)$ tại $B$ $\\Rightarrow \\triangle MBO$ vuông tại $[[blank:1.1cm]]$[[br]]"
        "$\\Rightarrow M, B, O$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "Vậy bốn điểm $M, A, O, B$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "b) [NB] Chứng minh $OM \\perp AB$:[[br]]"
        "$MA$, $MB$ là hai tiếp tuyến của $(O)$ cắt nhau tại $M$ $\\Rightarrow MA = [[blank:1.1cm]]$.[[br]]"
        "$OA = OB$ ([[blank:2.4cm]] của $(O)$)[[br]]"
        "$\\Rightarrow OM$ là [[blank:3.2cm]] của đoạn thẳng $AB$.[[br]]"
        "Vậy $OM \\perp AB$ (tính chất [[blank:3.2cm]])."
    )
    btvn_2 = bai(
        "BTVN 2.", 1, "btvn", "NB4",
        "Cho đường tròn $(O; R)$ và điểm $M$ ($OM > R$). Vẽ hai tiếp tuyến $MA$, $MB$ với đường tròn $(O)$ ($A$, $B$ là các tiếp điểm). "
        "Nối $OM$ cắt đoạn thẳng $AB$ tại điểm $H$ (Hình 9).[[br]]"
        "Vẽ tiếp vào Hình 9 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, rồi điền vào chỗ chấm để hoàn thành bài giải:[[br]]"
        "a) [NB] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng thuộc một đường tròn:[[br]]" + khung,
        "a) tiếp tuyến; $A$; $MO$; $B$; $MO$; $MO$.[[br]]b) $MB$; bán kính; đường trung trực; đường trung trực.",
        statement_slide="Cho đường tròn $(O; R)$ và điểm $M$ ($OM > R$). Vẽ hai tiếp tuyến $MA$, $MB$ với đường tròn $(O)$ ($A$, $B$ là các "
                        "tiếp điểm). Nối $OM$ cắt đoạn thẳng $AB$ tại điểm $H$ (Hình 9).[[br]]a) [NB] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng "
                        "thuộc một đường tròn.[[br]]b) [NB] Chứng minh $OM \\perp AB$.",
        figure_given=True, ve_tiep=3,
        figure={"tikz": h_nen_diem_ngoai("M", pdg), "tikz_gv": pdg, "caption": "Hình 9", "pos": "right"},
    )

    xl = hai_tt("A", "M", "N", "H", xa=3.4)
    t1, t2 = xam_tiep_tuyen("A", "M", "N")
    btvn_3 = bai(
        "BTVN 3.", 2, "btvn", "TH2",
        "[TH] Cho đường tròn $(O; R)$ và một điểm $A$ nằm bên ngoài đường tròn sao cho $OA > 2R$. Qua $A$ kẻ hai tiếp tuyến $AM$, $AN$ với "
        f"đường tròn $(O)$ ($M$, $N$ là hai tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $MN$ (Hình 10). Chứng minh $OA \\perp MN$. {theo_so_do(10)}",
        giai_trung_truc("A", "M", "N", ket=f".{BR}Vậy $OA \\perp MN$ (tính chất đường trung trực)."),
        draw=True, phut_so_do=PHUT["BTVN 3"],
        figure={"tikz": h_nen_diem_ngoai("A", xl), "tikz_gv": xl, "caption": "Hình 10", "pos": "right"},
        so_do_nguoc=sd_trung_truc("$OA \\perp MN$", "$OA$ là đường trung trực của $MN$", t1, t2),
    )

    cd = h_cau_dien()
    btvn_4 = bai(
        "BTVN 4.", 2, "btvn", "TH3",
        "[TH] Cho đường tròn $(O; R)$, đường kính $AB$. Trên đường tròn $(O)$ lấy điểm $M$ ($MA < MB$). Tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ "
        f"và $B$ lần lượt là $C$ và $D$ (Hình 11). Chứng minh $OC \\parallel MB$. {theo_so_do(11)}",
        giai_trung_truc("C", "A", "M", ket=f"{BR}$\\Rightarrow OC \\perp AM$.{BR}")
        + giai_vuong("M", "A", "B")
        + "Vậy $OC \\parallel MB$ (hai đường thẳng phân biệt cùng vuông góc với $AM$).",
        draw=True, phut_so_do=PHUT["BTVN 4"],
        figure={"tikz": h_nen_tron_ngang("A", "B", cd), "tikz_gv": cd, "caption": "Hình 11", "pos": "right"},
        so_do_nguoc=sd_song_song(
            "$OC \\parallel MB$", "$OC \\perp AM$", "$OC$ là đường trung trực\\\\của $AM$",
            "$CA = CM$;\\\\$OA = OM = R$",
            "$MB \\perp AM$", "$\\triangle AMB$ vuông tại $M$", "$MO = \\dfrac{AB}{2}$",
            "$MO$ là đường trung tuyến;\\\\$OM = OA = OB = R$"),
    )

    dd = h_dong_da()
    btvn_5 = bai(
        "BTVN 5.", 3, "btvn", "TH1+VD1",
        "Cho đường tròn $(O; R)$ đường kính $AB$. Kẻ tiếp tuyến $Ax$, lấy $P$ trên $Ax$ ($AP > R$). Từ $P$ kẻ tiếp tuyến $PM$ với $(O)$.[[br]]"
        "a) [TH] Chứng minh bốn điểm $A$, $P$, $M$, $O$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Chứng minh $OP \\perp AM$ và $OP \\parallel MB$.",
        "a) " + giai_bon_diem("P", "A", "M")
        + f"Vậy bốn điểm $A, P, M, O$ cùng thuộc đường tròn đường kính $PO$.{BR}"
        + "b) " + giai_trung_truc("P", "A", "M", ket=f"{BR}$\\Rightarrow OP \\perp AM$.{BR}")
        + giai_vuong("M", "A", "B")
        + "Vậy $OP \\perp AM$ và $OP \\parallel MB$ (hai đường thẳng phân biệt cùng vuông góc với $AM$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_duong_kinh_doc("A", "B", day_du=dd), "tikz_gv": dd, "caption": "Hình 12", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $AM$?",
               "Trong $\\triangle AMB$, đoạn $MO$ có quan hệ gì với cạnh $AB$?"],
    )

    return {
        "slug": PHIEU.stem,
        "title": "Tính chất hai tiếp tuyến cắt nhau. Chứng minh vuông góc, song song",
        "eyebrow": "PHIẾU 3 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 16",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "btvn_phieu_rieng": True,
        "stages": [
            {"kind": "review", "number": 1, "title": "Khám phá",
             "teacher_note": "Cho HS dùng thước và thước đo góc đo trực tiếp trên Hình 1. Chưa nêu định lí, để HS tự nói hai đoạn bằng nhau, "
                             "hai góc bằng nhau rồi mới đọc Định lí ở mục 1.",
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đứng ở một điểm, nhìn sát hai mép bồn hoa tròn}"},
                 {"type": "noted", "variant": "note",
                  "text": "Bạn An đứng ở điểm $A$ ngoài một bồn hoa hình tròn tâm $O$. Hai tia nhìn của An chạm sát mép bồn hoa tại $B$ và $C$ (Hình 1).[[br]]"
                          "\\textbf{a)} Dùng thước đo độ dài hai đoạn $AB$, $AC$ trên hình rồi so sánh.[[br]]"
                          "\\textbf{b)} Dùng thước đo góc đo hai góc $\\widehat{BAO}$, $\\widehat{CAO}$ rồi so sánh.[[br]]"
                          "\\textbf{c)} Dùng thước đo góc đo hai góc $\\widehat{BOA}$, $\\widehat{COA}$ rồi so sánh.",
                  "figure": {"tikz": h_kham_pha(), "caption": "Hình 1", "pos": "right"}},
             ]},
            {"kind": "concept", "number": 2, "title": "Kiến thức trọng tâm",
             "teacher_note": "Phần A đọc đúng lời SGK (Định lí 2, tr.102). Phần B là phương pháp cho hai dạng của ý b Câu IV.2: "
                             "vuông góc (39\\% đề Kì I) và song song; ví dụ của từng dạng nằm ngay ở Luyện tập 1.",
             "blocks": [
                 {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                 {"type": "noted", "variant": "theory", "title": "1. TÍNH CHẤT HAI TIẾP TUYẾN CẮT NHAU",
                  "text": "\\nhanly{Định lí.} Nếu hai tiếp tuyến của đường tròn $(O)$ cắt nhau tại điểm $M$ thì:[[br]]"
                          "\\nhanly{Thứ nhất:} điểm $M$ cách đều hai tiếp điểm.[[br]]"
                          "\\nhanly{Thứ hai:} $MO$ là tia phân giác của góc tạo bởi hai tiếp tuyến.[[br]]"
                          "\\nhanly{Thứ ba:} $OM$ là tia phân giác của góc tạo bởi hai bán kính qua hai tiếp điểm.",
                  "figure": {"tikz": hai_tt("M", "A", "B", r=R_THE, xa=2.8, day_cung=False),
                             "caption": "Hai tiếp tuyến $MA$, $MB$ cắt nhau tại $M$", "pos": "right"}},
                 {"type": "noted", "variant": "theory", "title": "2. KIẾN THỨC LỚP DƯỚI THƯỜNG DÙNG",
                  "text": "\\nhanly{Đường trung trực (Lớp 7):} Điểm cách đều hai đầu mút của một đoạn thẳng thì nằm trên đường trung trực của đoạn thẳng đó.[[br]]"
                          "\\nhanly{Trung tuyến (SGK Toán 8, tập 1, tr.66):} Nếu tam giác có một đường trung tuyến bằng nửa cạnh tương ứng thì tam giác đó là tam giác vuông.[[br]]"
                          "\\nhanly{Từ vuông góc đến song song (Lớp 7):} Hai đường thẳng phân biệt cùng vuông góc với đường thẳng thứ ba thì song song với nhau.",
                  "figure": {"tikz": h_the_duong_kinh(), "caption": "$OC = OB = OD$ $\\Rightarrow \\triangle BCD$ vuông tại $C$", "pos": "right"}},
                 {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                 the_dang_1,
                 the_dang_2,
             ]},
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "teacher_note": GHI_CHU_LT1,
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Phúc Đồng) ở Bài 5: ý a chứng minh bốn điểm cùng thuộc một đường "
                                          "tròn (đã học ở Phiếu 2), ý b chứng minh vuông góc và song song."},
                 {"type": "para", "variant": "heading", "text": "Mạch 1. Ý b — Chứng minh vuông góc bằng đường trung trực"},
                 bai("Bài 1.", 1, "onclass", "NB1", "[NB] Cho hai tiếp tuyến của một đường tròn cắt nhau tại một điểm. Chọn khẳng định \\textbf{sai}?", "B",
                     options=["Khoảng cách từ điểm đó đến hai tiếp điểm là bằng nhau.",
                              "Tia nối điểm đó tới tâm là tia phân giác của góc tạo bởi hai bán kính.",
                              "Tia nối từ tâm tới điểm đó là tia phân giác của góc tạo bởi hai bán kính.",
                              "Tia nối từ điểm đó tới tâm là tia phân giác của góc tạo bởi hai tiếp tuyến."],
                     figure_given=True),
                 bai("Bài 2.", 1, "onclass", "NB2",
                     "[NB] Cho đường tròn tâm $O$ và hai điểm $A$, $B$ thuộc $(O)$. Gọi $d$ là đường trung trực của đoạn $AB$ (Hình 2). Khẳng định nào sau đây \\textbf{sai}?", "C",
                     options=["$OA = OB$.", "Điểm $O$ thuộc đường thẳng $d$.",
                              "Đường thẳng $AB$ là trục đối xứng của đường tròn $(O)$.",
                              "Đường thẳng $d$ là trục đối xứng của đường tròn $(O)$."],
                     figure_given=True,
                     figure={"tikz": h_trung_truc_tron(), "caption": "Hình 2", "pos": "right"}),
                 vi_du_1,
                 bai_3,
                 {"type": "para", "variant": "heading", "text": "Mạch 2. Ý b — Chứng minh song song bằng hai đường cùng vuông góc"},
                 vi_du_2,
                 bai_4,
             ]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "teacher_note": GHI_CHU_LT2,
             "blocks": [
                 {"type": "para", "variant": "heading", "text": "Đề thi Học kì I — THCS Phúc Đồng (Long Biên)"},
                 bai_5,
             ]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
             "teacher_note": GHI_CHU_BTVN,
             "blocks": [
                 {"type": "mindmap", "caption": "Sơ đồ tư duy: Tính chất hai tiếp tuyến cắt nhau. Chứng minh vuông góc, song song",
                  "root": "HAI TIẾP TUYẾN CẮT NHAU",
                  "branches": [
                      {"label": "TÍNH CHẤT", "children": [{"label": "Điểm đó cách đều hai tiếp điểm"},
                                                           {"label": "$MO$ là phân giác góc tạo bởi hai tiếp tuyến"},
                                                           {"label": "$OM$ là phân giác góc tạo bởi hai bán kính"}]},
                      {"label": "CHỨNG MINH VUÔNG GÓC", "children": [{"label": "$AB = AC$ (hai tiếp tuyến cắt nhau)"},
                                                                       {"label": "$OB = OC = R$ (bán kính)"},
                                                                       {"label": "$OA$ là đường trung trực của $BC$"},
                                                                       {"label": "$OA \\perp BC$ tại $H$"}]},
                      {"label": "CHỨNG MINH SONG SONG", "children": [{"label": "$CO$ là trung tuyến, $CO = \\dfrac{BD}{2}$"},
                                                                       {"label": "$\\triangle BCD$ vuông tại $C$"},
                                                                       {"label": "$OA$, $CD$ cùng vuông góc với $BC$"},
                                                                       {"label": "$OA \\parallel CD$"}]},
                  ]},
                 bai("BTVN 1.", 1, "btvn", "NB3",
                     "[NB] Cho hai tiếp tuyến tại $C$ và $D$ của đường tròn $(O)$ cắt nhau tại $N$, biết $\\widehat{CND} = 40^\\circ$ (Hình 8). Số đo của cung nhỏ $CD$ bằng bao nhiêu độ?[[br]]Trả lời: $[[blank:1.6cm]]$",
                     "$140^\\circ$", figure_given=True,
                     figure={"tikz": h_cau_60().replace("\\end{tikzpicture}", "  \\path (-2.6000,-1.3000) rectangle (5.3000,1.3000);\n\\end{tikzpicture}"), "caption": "Hình 8", "pos": "right"}),
                 btvn_2, btvn_3, btvn_4, btvn_5,
             ]},
        ],
    }


# ── Thuyết minh ────────────────────────────────────────────────────────────────
def dong_tm(phut) -> list[dict]:
    return [
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Định lí hai tiếp tuyến cắt nhau: cách đều hai tiếp điểm, tia phân giác (trắc nghiệm chọn khẳng định sai)",
         "source_refs": ["stk-b16-I-C7-tr232"], "vidu": 0, "onclass": 1, "btvn": 0, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Đường trung trực của đoạn thẳng (Lớp 7): tâm cách đều hai điểm trên đường tròn nên thuộc đường trung trực (trắc nghiệm)",
         "source_refs": ["stk-b13-I-C13-tr6"], "vidu": 0, "onclass": 1, "btvn": 0, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Tính số đo cung trên hình hai tiếp tuyến cắt nhau (BTVN trả lời ngắn)",
         "source_refs": ["stk-b16-III-C60-tr252"], "vidu": 0, "onclass": 0, "btvn": 1, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB ghép bài", "dang": "Vẽ tiếp hình nền, điền khung bài giải: bốn điểm cùng thuộc đường tròn đường kính; đường trung trực $\\Rightarrow$ vuông góc (BTVN đề Phan Đình Giót ý a, phần $OM \\perp AB$ của ý b)",
         "source_refs": ["ck1-phan-dinh-giot-2024-IV2.a", "ck1-phan-dinh-giot-2024-IV2.b"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "none",
         "hinh_san": True, "gian_giao": "dien-khuyet", "khung": True, "ve_tiep": {"btvn": 3}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Ý a của đề thi: bốn điểm cùng thuộc một đường tròn, xác định tâm và bán kính, HS tự vẽ hình, tự trình bày (đề đích Phúc Đồng ý a; BTVN đề Đống Đa 2025 ý a)",
         "source_refs": ["ck1-phuc-dong-IV2.a", "ck1-dong-da-2025-IV2.a"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_hinh": {"onclass": 1, "btvn": 1}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ý b đề thi, chứng minh vuông góc: hai tiếp tuyến cắt nhau $\\to$ đường trung trực. Ví dụ mẫu SGK Ví dụ 2a; HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (trên lớp đề Nguyễn Bỉnh Khiêm, phần $OD \\perp AB$; BTVN đề Xuân La, phần $OA \\perp MN$ của ý b)",
         "source_refs": ["sgk-b16-vd2.a", "ck1-nguyen-binh-khiem-2025-4.2.b", "ck1-xuan-la-2024-4.2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"vidu": 2, "onclass": 3}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"onclass": phut["Bài 3"], "btvn": phut["BTVN 3"]}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ý b đề thi, chứng minh song song: đường trung trực $\\to$ trung tuyến bằng nửa cạnh cho góc vuông $\\to$ cùng vuông góc. HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (trên lớp đề Lômônôxốp ý b; BTVN đề Cầu Diễn, phần $OC \\parallel MB$ của ý b)",
         "source_refs": ["ck1-lomonoxop-2024-IV2.b", "ck1-cau-dien-42.b"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"onclass": 3}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"onclass": phut["Bài 4"], "btvn": phut["BTVN 4"]}},
        {"band": "VD", "loai": "VD lẻ", "dang": "Ý b của đề thi (đề Phúc Đồng, đích của buổi): $OA \\perp BC$ tại $H$ và $OA \\parallel CD$. Ví dụ mẫu đề Ba Đình 2024 ý b; BTVN đề Đống Đa 2025 ý b",
         "source_refs": ["ck1-phuc-dong-IV2.b", "ck1-ba-dinh-2024-IV2.b", "ck1-dong-da-2025-IV2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "vd",
         "hinh_san": False, "gian_giao": "ve-hinh", "ve_tiep": {"vidu": 3},
         "quy_trinh": ["Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $AO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $AO$",
                       "Ý b: $AB = AC$, $OB = OC = R$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$ tại $H$ (như Ví dụ 1, Bài 3)",
                       "$CO$ là đường trung tuyến, $CO = \\dfrac{BD}{2}$ $\\Rightarrow \\triangle BCD$ vuông tại $C$ $\\Rightarrow CD \\perp BC$ (như Ví dụ 2, Bài 4)",
                       "$OA$ và $CD$ cùng vuông góc với $BC$ $\\Rightarrow OA \\parallel CD$"]},
    ]


def main():
    kiem_toan_do()
    les = gon_hinh(lesson())
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2) + "\n", "utf-8")
    tm = json.loads(TM.read_text("utf-8"))
    p3 = next(p for p in tm["phieu"] if p["code"] == "3")
    p3["rows"] = dong_tm(PHUT)
    i = next(i for i, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 3"))
    j = next(j for j, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 4"))
    tm["thoiluong"][i + 1:j] = GIO_THUC_TM
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), "utf-8")
    print("ghi xong", PHIEU.name)


if __name__ == "__main__":
    main()
