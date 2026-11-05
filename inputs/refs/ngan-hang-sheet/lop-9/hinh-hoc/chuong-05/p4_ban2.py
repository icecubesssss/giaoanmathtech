#!/usr/bin/env python3
"""Phiếu 4 ch.V 9C — dựng lại theo bản mẫu phiếu 2, 3 (sơ đồ ngược, Thầy giao 05/11/2026).

Đề soi từ ẢNH: Tạ Quang Bửu 2025 IV.2 a, b · Ngô Gia Tự 2025 Câu IV.2 ý b · Chương Mỹ 2024 Bài 4.2 ý b ·
Dịch Vọng 2025 Câu 4.2 ý b · Thanh Trì 2024 Bài IV.2 ý a, phần CE.CB = CA² của ý b · Nghĩa Tân GK1 2025 Bài IV ý 1, phần BE.BA = BH.BD của ý 2 ·
Cầu Giấy 2024 Câu IV.2 ý b · Long Biên 2024 Câu IV.2 phần AI.AN = AH.AB của ý b · Xuân La 2024 Bài 4.2 a, b ·
STK Trương Ngọc Vỹ C44 tr.246 (a, b) · đề lớp 8: Thanh Trì CK2 2023 Câu 6, Đan Phượng CK2 2023 Câu 8, Mai Dịch GK2 2025 Câu 8.

Ghi đè seed phiếu 4 và dòng phiếu 4 trong thuyết minh, chạy lại được:
    .venv/bin/python inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05/p4_ban2.py
Sau đó chạy scripts/phut_so_do.py <phiếu> --ghi rồi chạy lại script này để chép phút vào thuyết minh.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from p3_ban2 import R, h_nen_diem_ngoai, h_nen_duong_kinh_doc, h_nen_duong_kinh_ngang, nen  # noqa: E402
from p3_ban3 import END, HEAD, bai, giai_bon_diem, giai_trung_truc, gon_hinh, hai_tt, theo_so_do  # noqa: E402
from scripts.tikz_geo import Fig, foot, polar, tangent_points  # noqa: E402

D_ = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"
PHIEU = D_ / "phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json"
TM = D_ / "thuyet-minh.json"
BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"
R_THE = 1.2
R_NHO = 1.2

# Phút có sơ đồ (scripts/phut_so_do.py), chưa gồm vẽ.
PHUT = {"Bài 8": 0, "Bài 9": 0, "BTVN 3": 0, "BTVN 4": 0}
if PHIEU.exists():
    for _st in json.loads(PHIEU.read_text("utf-8"))["stages"]:
        for _b in _st["blocks"]:
            if _b.get("phut_so_do"):
                PHUT[_b["label"].rstrip(".")] = _b["phut_so_do"]

GHI_CHU_LT1 = (
    "Hai ví dụ: GV vẽ trên bảng, HS vẽ cùng vào hình nền trên phiếu (Ví dụ 1: đường cao $AH$, các đoạn $HD$, $HE$; "
    "Ví dụ 2: tiếp tuyến $AC$, $CM$, đoạn $CB$, điểm $K$, các đoạn $KO$, $AK$). Khoảng 65 phút với lớp C theo định mức: Bài 1 đến Bài 4 đổi tích ra tỉ lệ thức rồi đọc ra hai tam giác (tử số cùng một tam giác, mẫu số cùng một tam giác) ~10′, Bài 5 đến Bài 7 trắc nghiệm đồng dạng ~8′, "
    "2 ví dụ GV giảng và cùng HS điền sơ đồ ngược ~22′ (gồm 5′ vẽ), Bài 8 HS vẽ tiếp, đọc sơ đồ ngược rồi trình bày vào vở ~13′, "
    "Bài 9 cùng cách ~12′."
)
GHI_CHU_LT2 = (
    "Khoảng 21 phút với lớp C theo định mức: HS tự vẽ hình đề Tạ Quang Bửu (~5′), tự trình bày ý b (~16′): phần vuông góc như Phiếu 3, "
    "$MA^2 = MH \\cdot MO$ như Bài 8, $MA^2 = MC \\cdot MD$ như Bài 9, bắc cầu như Ví dụ 1. "
    "Ý a đã học ở Phiếu 2, GV chữa ở phần chữa bài cuối buổi."
)
GHI_CHU_BTVN = (
    "BTVN khoảng 72 phút với lớp C, dày hơn quỹ 40 phút để HS có thêm bài: BTVN 1 Đúng/Sai (~4′), BTVN 2 vẽ tiếp hình rồi điền khung (~9′), "
    "BTVN 3 tự vẽ hình, đọc sơ đồ ngược rồi trình bày vào vở (~16′), BTVN 4 cùng cách (~15′), "
    "BTVN 5 tự vẽ hình, tự trình bày như Bài 10 (~28′)."
)


# ── Sơ đồ ngược ────────────────────────────────────────────────────────────────
def cao(o: str) -> float:
    return 0.15 * (("\\\\" in o) + ("dfrac" in o))


def so_do(dich: str, song: list[str], trai: list[str], phai: list[str], rong=2.7, buoc=0.75, ben="", ben_x=0.0) -> str:
    """Ô đích trên cùng; `song` là cột giữa đi xuống; hai nhánh trái, phải đi lên ô cuối cột giữa.

    Ô cuối mỗi nhánh là ô xám (điều có ngay từ giả thiết). `ben`: ô xám nối thẳng vào ô đích, vd "$R = OB$" (Thầy 05/11/2026).
    """
    out = [HEAD, f"  \\node[dich] (g) at (0,0) {{{dich}}};\n"]
    if ben:
        out.append(f"  \\node[gt] (b) at ({ben_x or rong + 0.7:.2f},-0.85) {{{ben}}};\n  \\draw[m] (b.north) |- (g.east);\n")
    tren, y = "g", 0.0
    for i, s in enumerate(song):
        y -= 0.85
        out.append(f"  \\node[o] (s{i}) at (0,{y:.2f}) {{{s}}};\n")
        out.append(f"  \\draw[m] (s{i}) -- ({tren});\n")
        tren = f"s{i}"
    y0 = y - 1.0
    for ten, ds, x, canh in (("l", trai, -rong, "west"), ("r", phai, rong, "east")):
        yy = y0
        for i, s in enumerate(ds):
            kieu = "gt" if i == len(ds) - 1 else "o"
            if i:  # ô hai dòng hoặc có phân số cao hơn, phải giãn thêm để mũi tên không bị che
                yy -= buoc + cao(ds[i - 1]) + cao(s)
            out.append(f"  \\node[{kieu}] ({ten}{i}) at ({x:.2f},{yy:.2f}) {{{s}}};\n")
            if i:
                out.append(f"  \\draw[m] ({ten}{i}) -- ({ten}{i - 1});\n")
        if ds:
            out.append(f"  \\draw[m] ({ten}0.north) |- ({tren}.{canh});\n")
    out.append(END)
    return "".join(out)


# ── Toạ độ ─────────────────────────────────────────────────────────────────────
def giao_thu_hai(p, q, r):
    """p nằm trên đường tròn tâm gốc bán kính r; trả về giao điểm thứ hai của đường thẳng pq với đường tròn."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t = -2 * (p[0] * dx + p[1] * dy) / (dx * dx + dy * dy)
    return (p[0] + t * dx, p[1] + t * dy)


def giao(a, b, c, d):
    x1, y1, x2, y2, x3, y3, x4, y4 = *a, *b, *c, *d
    m = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / m
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def d(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def chuong_my():
    a, b, c = (1.2, 2.1), (0.0, 0.0), (4.2, 0.0)
    h = foot(a, b, c)
    return a, b, c, h, foot(h, a, b), foot(h, a, c)


def dich_vong():
    a, b, c = (0.0, R), (0.0, -R), (2.9, R)
    p, q = tangent_points((0, 0), R, c)
    m = max((p, q), key=lambda u: abs(u[0] - a[0]) + abs(u[1] - a[1]))
    return a, b, c, m, giao_thu_hai(b, c, R)


def thanh_tri():
    a, b, dd = (-R, 0.0), (R, 0.0), polar(78, R)
    c = (-R, (R * R + R * dd[0]) / dd[1])
    return a, b, dd, c, giao_thu_hai(b, c, R)


def ta_quang_buu():
    o, m = (0.0, 0.0), (3.5, 0.0)
    a, b = tangent_points(o, R, m)
    if a[1] < b[1]:
        a, b = b, a
    dd = (-a[0], -a[1])
    return m, a, b, foot(a, o, m), dd, giao_thu_hai(dd, m, R)


def cau_giay():
    o, a = (0.0, 0.0), (3.4, 0.0)
    b = max(tangent_points(o, R, a), key=lambda u: u[1])
    c = (-b[0], -b[1])
    return a, b, c, giao_thu_hai(c, a, R), foot(o, c, a)


def long_bien():
    a, b, m, n = (-R, 0.0), (R, 0.0), polar(125, R), polar(45, R)
    h = (m[0], 0.0)
    return a, b, m, n, h, giao(a, n, m, h)


def xuan_la():
    o, a = (0.0, 0.0), (3.5, 0.0)
    m, n = tangent_points(o, R, a)
    if m[1] < n[1]:
        m, n = n, m
    c = (-m[0], -m[1])
    return a, m, n, foot(m, o, a), c, giao_thu_hai(c, a, R)


def kiem_toan_do():
    """Kết luận của đề phải đúng trên chính hình vẽ."""
    O = (0.0, 0.0)
    a, b, c, h, dd, e = chuong_my()
    assert abs(d(a, dd) * d(a, b) - d(a, e) * d(a, c)) < 1e-9 and abs(d(a, h) ** 2 - d(a, dd) * d(a, b)) < 1e-9
    a, b, c, m, k = dich_vong()
    assert abs(d(b, k) * d(b, c) - 4 * R * R) < 1e-9
    a, b, dd, c, e = thanh_tri()
    assert abs(d(c, e) * d(c, b) - d(c, a) ** 2) < 1e-9 and abs(d(c, dd) - d(c, a)) < 1e-9
    assert (e[0] - a[0]) * (e[0] - b[0]) + (e[1] - a[1]) * (e[1] - b[1]) < 1e-9
    m, a, b, h, dd, c = ta_quang_buu()
    assert abs(d(m, h) * d(m, O) - d(m, c) * d(m, dd)) < 1e-9 and abs(d(m, a) ** 2 - d(m, c) * d(m, dd)) < 1e-9
    a, b, c, dd, h = cau_giay()
    assert abs(d(c, h) * d(c, a) - 2 * R * R) < 1e-9
    a, b, m, n, h, i = long_bien()
    assert abs(d(a, i) * d(a, n) - d(a, h) * d(a, b)) < 1e-9 and i[1] > 0 and i[1] < m[1]
    a, b, c, dd, e, h = nghia_tan()
    assert d(a, b) < d(a, c) and abs(d(b, e) * d(b, a) - d(b, h) * d(b, dd)) < 1e-9
    a, m, n, h, c, b = xuan_la()
    assert abs(d(a, h) * d(a, O) - d(a, b) * d(a, c)) < 1e-9 and d(a, O) > 2 * R
    assert abs((m[0] - b[0]) * (c[0] - b[0]) + (m[1] - b[1]) * (c[1] - b[1])) < 1e-9


# ── Hình ───────────────────────────────────────────────────────────────────────
def rong(tz, x0, y0, x1, y1):
    """\\figbelow co hình theo BỀ NGANG: khung rộng hơn hình để hình thấp lại, bớt chỗ."""
    return tz.replace("\\end{tikzpicture}", f"  \\path ({x0:.4f},{y0:.4f}) rectangle ({x1:.4f},{y1:.4f});\n\\end{{tikzpicture}}")


def h_kham_pha():
    f = Fig()
    O, A, B, H = (0, 0), (3.4, 0), (0.7529, 1.4118), (0.7529, 0)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("H", H)
    f.seg("O", "A"); f.seg("A", "B"); f.seg("O", "B"); f.seg("B", "H")
    f.right("B", O, A); f.right("H", B, A)
    return f.tikz()


def h_the_duong_kinh():
    """Thẻ Dạng 2: hai tiếp tuyến, đường kính BD, AD cắt đường tròn tại E."""
    f = Fig()
    O, A = (0, 0), (2.8, 0)
    b, c = tangent_points(O, R_THE, A)
    if b[1] < c[1]:
        b, c = c, b
    dd = (-b[0], -b[1])
    e = giao_thu_hai(dd, A, R_THE)
    f.circle(O, R_THE)
    f.pt("O", O); f.pt("A", A); f.pt("B", b); f.pt("D", dd); f.pt("E", e)
    for u, v in [("A", "B"), ("B", "D"), ("A", "D"), ("B", "E"), ("O", "E")]:
        f.seg(u, v)
    f.right("B", O, A); f.right("E", A, b)
    return f.tikz()


def h_tich_cu():
    """Thẻ kiến thức lớp dưới: đường kính BC, A thuộc đường tròn."""
    f = Fig()
    O, B, C, A = (0, 0), (-R_THE, 0), (R_THE, 0), polar(115, R_THE)
    f.circle(O, R_THE)
    f.pt("O", O); f.pt("B", B); f.pt("C", C); f.pt("A", A)
    f.seg("B", "C"); f.seg("A", "B"); f.seg("A", "C"); f.seg("A", "O")
    f.right("A", B, C)
    return f.tikz()


def h_mai_dich():
    f = Fig()
    C, B, A, H = (0.0, 0.0), (4.0, 0.0), (1.3, math.sqrt(1.3 * 2.7)), (1.3, 0.0)
    f.pt("A", A); f.pt("B", B); f.pt("C", C); f.pt("H", H)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("A", "H")]:
        f.seg(u, v)
    f.right("H", A, B)
    return f.tikz()


def h_c44():
    f = Fig()
    r = R_NHO
    O, A, B, C = (0, 0), (-r, 0), (r, 0), polar(115, r)
    M = giao(B, C, A, (-r, 3.0))
    f.circle(O, r)
    f.pt("O", O); f.pt("A", A); f.pt("B", B); f.pt("C", C); f.pt("M", M)
    for u, v in [("A", "B"), ("A", "M"), ("B", "M"), ("A", "C")]:
        f.seg(u, v)
    f.right("A", O, M)
    return f.tikz()


def h_chuong_my():
    a, b, c, h, dd, e = chuong_my()
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("H", h); f.pt("D", dd); f.pt("E", e)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("A", "H"), ("H", "D"), ("H", "E")]:
        f.seg(u, v)
    f.right("H", a, c); f.right("D", b, h); f.right("E", c, h)
    return f.tikz()


def h_nen_chuong_my(day_du):
    a, b, c, *_ = chuong_my()
    f = Fig()
    f.pt("A", a); f.pt("B", b); f.pt("C", c)
    f.seg("A", "B"); f.seg("B", "C"); f.seg("A", "C")
    return nen(f, day_du)


def h_dich_vong():
    a, b, c, m, k = dich_vong()
    f = Fig()
    f.arc((0, 0), R, -90, 90)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("M", m); f.pt("K", k)
    for u, v in [("A", "B"), ("A", "C"), ("C", "M"), ("O", "M"), ("B", "C"), ("O", "K"), ("A", "K")]:
        f.seg(u, v)
    f.right("A", (0, 0), c); f.right("M", (0, 0), c); f.right("K", a, b)
    return f.tikz()


def h_thanh_tri():
    a, b, dd, c, e = thanh_tri()
    f = Fig()
    f.arc((0, 0), R, 0, 180)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("D", dd); f.pt("C", c); f.pt("E", e)
    for u, v in [("A", "B"), ("A", "C"), ("C", "D"), ("O", "D"), ("B", "C"), ("O", "E"), ("A", "E")]:
        f.seg(u, v)
    f.right("A", (0, 0), c); f.right("D", (0, 0), c); f.right("E", a, b)
    return f.tikz()


def h_ta_quang_buu():
    m, a, b, h, dd, c = ta_quang_buu()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("M", m); f.pt("A", a); f.pt("B", b); f.pt("H", h); f.pt("D", dd); f.pt("C", c)
    for u, v in [("M", "A"), ("M", "B"), ("O", "B"), ("O", "M"), ("A", "B"), ("A", "D"), ("M", "D"), ("A", "C"), ("O", "C")]:
        f.seg(u, v)
    f.right("A", (0, 0), m); f.right("B", (0, 0), m); f.right(h, a, m); f.right("C", a, m)
    return f.tikz()


def h_cau_giay():
    a, b, c, dd, h = cau_giay()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("H", h)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("O", "H")]:
        f.seg(u, v)
    f.right("B", (0, 0), a); f.right("H", (0, 0), c)
    return f.tikz()


def h_long_bien():
    a, b, m, n, h, i = long_bien()
    f = Fig()
    f.arc((0, 0), R, 0, 180)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("M", m); f.pt("N", n); f.pt("H", h); f.pt("I", i)
    for u, v in [("A", "B"), ("A", "N"), ("N", "B"), ("M", "H"), ("O", "N")]:
        f.seg(u, v)
    f.right("N", a, b); f.right(h, m, b)
    return f.tikz()


def nghia_tan():
    a, b, c = polar(105, R), polar(205, R), polar(335, R)
    dd, e = foot(b, a, c), foot(c, a, b)
    return a, b, c, dd, e, giao(b, dd, c, e)


def h_nghia_tan():
    a, b, c, dd, e, h = nghia_tan()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("C", c); f.pt("D", dd); f.pt("E", e); f.pt("H", h)
    for u, v in [("A", "B"), ("B", "C"), ("A", "C"), ("B", "D"), ("C", "E")]:
        f.seg(u, v)
    f.right("D", a, b); f.right("E", a, c)
    return f.tikz()


def h_nen_nghia_tan(day_du):
    a, b, c, *_ = nghia_tan()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("B", b); f.pt("C", c)
    f.seg("A", "B"); f.seg("B", "C"); f.seg("A", "C")
    return nen(f, day_du)


def h_xuan_la():
    a, m, n, h, c, b = xuan_la()
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0)); f.pt("A", a); f.pt("M", m); f.pt("N", n); f.pt("H", h); f.pt("C", c); f.pt("B", b)
    for u, v in [("A", "M"), ("A", "N"), ("O", "A"), ("M", "N"), ("M", "C"), ("A", "C"), ("M", "B"), ("O", "B")]:
        f.seg(u, v)
    f.right("M", (0, 0), a); f.right(h, m, a); f.right("B", m, a)
    return f.tikz()


def h_nen_tron(day_du):
    """Đề "Cho đường tròn (O). Từ điểm A …": điểm A dựng ở bước đầu, hình nền chỉ có đường tròn."""
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0))
    return nen(f, day_du)


# ── Lời giải ───────────────────────────────────────────────────────────────────
def xet(t1, t2, goc, ly_do, chung, ti, tich):
    return (
        f"Xét $\\triangle {t1}$ và $\\triangle {t2}$ có:{BR}"
        f"${goc} = 90^\\circ$ ({ly_do}){BR}"
        f"${chung}$ chung{BR}"
        f"$\\Rightarrow \\triangle {t1} \\backsim \\triangle {t2}$ (g.g){BR}"
        f"$\\Rightarrow {ti}${BR}"
        f"$\\Rightarrow {tich}$"
    )


def goc(s):
    return f"\\widehat{{{s}}}"


def giai_vuong(c, x, y, o="O", ban_kinh="= R", ket=""):
    """Tam giác có đường trung tuyến bằng nửa cạnh tương ứng; `ban_kinh` rỗng khi đề không đặt tên R."""
    tiep = f"{o}{c} = {o}{x} = {o}{y} {ban_kinh}".strip()
    ly_do = "" if ban_kinh else " (bán kính)"
    return (
        f"Xét $\\triangle {x}{c}{y}$ có ${c}{o}$ là đường trung tuyến ứng với cạnh ${x}{y}$ "
        f"(${o}$ là trung điểm của ${x}{y}$).{BR}"
        f"${tiep}${ly_do} $\\Rightarrow {c}{o} = \\dfrac{{{x}{y}}}{{2}}${BR}"
        f"$\\Rightarrow \\triangle {x}{c}{y}$ vuông tại ${c}$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng).{BR}"
        + (f"$\\Rightarrow {ket}$.{BR}" if ket else "")
    )


def lesson() -> dict:
    # ── Thẻ phương pháp ────────────────────────────────────────────────────────
    the_dang_1 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 1. ĐẲNG THỨC TÍCH TỪ HAI TAM GIÁC VUÔNG CHUNG GÓC NHỌN",
        "text": "\\nhanly{Phương pháp.} đưa về hai tam giác đồng dạng.[[br]]"
                "\\nhanly{Bước 1 (nháp):} Đổi tích thành tỉ số $\\dfrac{OH}{OB} = \\dfrac{OB}{OA}$, đọc ra $\\triangle OHB$ và $\\triangle OBA$.[[br]]"
                "\\nhanly{Bước 2:} Chỉ ra góc vuông và góc nhọn chung (g.g).[[br]]"
                "\\nhanly{Bước 3:} Viết tỉ số cạnh tương ứng $\\Rightarrow$ đẳng thức tích.[[br]]"
                "\\nhanly{Hai tích khác nhau:} bắc cầu qua đại lượng thứ ba.",
        "figure": {"tikz": hai_tt("A", "B", "C", "H", r=R_THE, xa=2.8),
                   "caption": "$\\triangle OHB$ và $\\triangle OBA$ vuông, chung góc $O$", "pos": "right"},
        "so_do_nguoc": so_do(
            "$OH \\cdot OA = R^2$", ["$OH \\cdot OA = OB^2$", "$\\triangle OHB \\backsim \\triangle OBA$ (g.g)"],
            ["$OA \\perp BC$ tại $H$", "$OA$ là đường trung trực của $BC$:\\\\$AB = AC$; $OB = OC = R$"],
            [f"${goc('OBA')} = 90^\\circ$ ($AB$ là tiếp tuyến);\\\\${goc('AOB')}$ chung"], rong=2.9, ben="$R = OB$ (bán kính)"),
    }
    the_dang_2 = {
        "type": "noted", "variant": "theory", "title": "DẠNG 2. CÓ ĐƯỜNG KÍNH: TAM GIÁC VUÔNG RỒI ĐẲNG THỨC TÍCH",
        "text": "\\nhanly{Phương pháp.} lấy góc vuông từ đường kính.[[br]]"
                "\\nhanly{Bước 1:} Đường kính $BD$, $AD$ cắt $(O)$ tại $E$: đường trung tuyến $EO = \\dfrac{BD}{2}$ "
                "$\\Rightarrow \\triangle BED$ vuông tại $E$ $\\Rightarrow BE \\perp AD$.[[br]]"
                "\\nhanly{Bước 2:} Xét hai tam giác vuông chung góc nhọn: $\\triangle AEB \\backsim \\triangle ABD$ (g.g).[[br]]"
                "\\nhanly{Bước 3:} Viết tỉ số cạnh tương ứng $\\Rightarrow AE \\cdot AD = AB^2$.",
        "figure": {"tikz": h_the_duong_kinh(), "caption": "$\\triangle AEB$ và $\\triangle ABD$ vuông, chung góc $A$", "pos": "right"},
        "so_do_nguoc": so_do(
            "$AE \\cdot AD = AB^2$", ["$\\triangle AEB \\backsim \\triangle ABD$ (g.g)"],
            ["$BE \\perp AD$ ($\\triangle BED$ vuông tại $E$)", "$EO$ là đường trung tuyến,\\\\$EO = \\dfrac{BD}{2}$ ($OE = OB = OD$)"],
            [f"${goc('ABD')} = 90^\\circ$ ($AB$ là tiếp tuyến);\\\\${goc('BAD')}$ chung"], rong=2.9),
    }

    # ── Bài 1–4: đẳng thức tích → tỉ lệ thức → cặp tam giác (Thầy 05/11/2026) ──
    ti_1 = bai(
        "Bài 1.", 1, "onclass", "NB1",
        "[NB] Đẳng thức $OH \\cdot OA = OB^2$ có được từ tỉ lệ thức nào?",
        "B",
        options=["$\\dfrac{OH}{OA} = \\dfrac{OA}{OB}$.", "$\\dfrac{OH}{OB} = \\dfrac{OB}{OA}$.",
                 "$\\dfrac{OH}{OB} = \\dfrac{OA}{OB}$.", "$\\dfrac{OB}{OA} = \\dfrac{OA}{OH}$."],
        figure_given=True,
    )
    ti_2 = bai(
        "Bài 2.", 1, "onclass", "NB1",
        "[NB] Để có tỉ lệ thức $\\dfrac{OH}{OB} = \\dfrac{OB}{OA}$, cần chứng minh hai tam giác nào đồng dạng?",
        "C",
        options=["$\\triangle OHB \\backsim \\triangle OAB$.\\phantom{xxxxx}", "$\\triangle OHB \\backsim \\triangle BOA$.",
                 "$\\triangle OHB \\backsim \\triangle OBA$.", "$\\triangle HOB \\backsim \\triangle OBA$."],
        figure_given=True,
    )
    ti_3 = bai(
        "Bài 3.", 1, "onclass", "NB1",
        "[NB] Đẳng thức $CH \\cdot CA = CO \\cdot CB$ có được từ tỉ lệ thức nào?",
        "C",
        options=["$\\dfrac{CH}{CO} = \\dfrac{CA}{CB}$.", "$\\dfrac{CH}{CB} = \\dfrac{CA}{CO}$.",
                 "$\\dfrac{CH}{CB} = \\dfrac{CO}{CA}$.", "$\\dfrac{CA}{CB} = \\dfrac{CH}{CO}$."],
        figure_given=True,
    )
    ti_4 = bai(
        "Bài 4.", 1, "onclass", "NB1",
        "[NB] Để có tỉ lệ thức $\\dfrac{CH}{CB} = \\dfrac{CO}{CA}$, cần chứng minh hai tam giác nào đồng dạng?",
        "B",
        options=["$\\triangle CHO \\backsim \\triangle CAB$.\\phantom{xxxxx}", "$\\triangle CHO \\backsim \\triangle CBA$.",
                 "$\\triangle HCO \\backsim \\triangle CBA$.", "$\\triangle CHO \\backsim \\triangle BCA$."],
        figure_given=True,
    )

    # ── Bài 5–7: trắc nghiệm chứng minh đồng dạng (đề lớp 8 Hà Nội, Thầy 05/11/2026) ──
    tn_1 = bai(
        "Bài 5.", 1, "onclass", "NB2",
        "[NB] Nếu $\\triangle MNP$ và $\\triangle DEF$ có $\\widehat{M} = \\widehat{D} = 90^\\circ$, $\\widehat{P} = 50^\\circ$. "
        "Để $\\triangle MNP \\backsim \\triangle DEF$ thì cần thêm điều kiện",
        "B",
        options=["$\\widehat{E} = 50^\\circ$.", "$\\widehat{F} = 50^\\circ$.", "$\\widehat{E} = 60^\\circ$.", "$\\widehat{F} = 40^\\circ$."],
        figure_given=True,
    )
    tn_2 = bai(
        "Bài 6.", 1, "onclass", "NB2",
        "[NB] Nếu $\\triangle ABC$ và $\\triangle MNP$ có $\\widehat{BAC} = \\widehat{NPM}$, $\\widehat{ACB} = \\widehat{MNP}$, cách viết nào sau đây đúng?",
        "B",
        options=["$\\triangle ABC \\backsim \\triangle MNP$.\\phantom{xxxxx}", "$\\triangle ABC \\backsim \\triangle PMN$.",
                 "$\\triangle ABC \\backsim \\triangle PNM$.", "$\\triangle ABC \\backsim \\triangle NMP$."],
        figure_given=True,
    )
    tn_3 = bai(
        "Bài 7.", 1, "onclass", "NB2",
        "[NB] Cho $\\triangle ABC$ vuông tại $A$, đường cao $AH$ (Hình 2). Trong hình có những cặp tam giác đồng dạng là",
        "D",
        options=["$\\triangle HBA \\backsim \\triangle ABC$.", "$\\triangle HAC \\backsim \\triangle ABC$.",
                 "$\\triangle HAC \\backsim \\triangle HBA$.", "Cả ba câu A, B, C đều đúng."],
        figure_given=True, figure={"tikz": h_mai_dich(), "caption": "Hình 2", "pos": "right"},
    )

    # ── Ví dụ 1: Chương Mỹ ý b ─────────────────────────────────────────────────
    cm = h_chuong_my()
    ti = "\\dfrac{AD}{AH} = [[fill:\\dfrac{AH}{AB}|1.3cm]]"
    vi_du_1 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 1.} Cho $\\triangle ABC$ có $3$ góc nhọn, đường cao $AH$, kẻ $HE \\perp AC$ tại $E$, $HD \\perp AB$ tại $D$ (Hình 3). "
                "Vẽ tiếp vào Hình 3 các yếu tố còn thiếu theo đề. Chứng minh rằng $AD \\cdot AB = AE \\cdot AC$."
                f"{BR}{LG}{BR}"
                + xet("ADH", "AHB", f"{goc('ADH')} = {goc('AHB')}", "$HD \\perp AB$, $AH \\perp BC$", "[[fill:\\widehat{BAH}]]", ti, "[[fill:AH^2]] = AD \\cdot AB")
                .replace("\\triangle AHB$ (g.g)", "\\triangle [[fill:AHB]]$ (g.g)") + f".{BR}"
                + f"Tương tự, $\\triangle AEH$ và $\\triangle AHC$ có ${goc('AEH')} = {goc('AHC')} = 90^\\circ$, $[[fill:\\widehat{{HAC}}]]$ chung{BR}"
                f"$\\Rightarrow \\triangle AEH \\backsim \\triangle [[fill:AHC]]$ (g.g){BR}"
                f"$\\Rightarrow [[fill:AH^2]] = AE \\cdot AC$.{BR}"
                "Vậy $AD \\cdot AB = AE \\cdot AC$ (cùng bằng $[[fill:AH^2]]$).",
        "figure": {"tikz": h_nen_chuong_my(cm), "tikz_gv": cm, "caption": "Hình 3", "pos": "right"},
        "so_do_nguoc": so_do(
            "$AD \\cdot AB = AE \\cdot AC$", [],
            ["$[[fill:AH^2]] = AD \\cdot AB$", "$\\triangle ADH \\backsim \\triangle [[fill:AHB]]$ (g.g)",
             f"${goc('ADH')} = {goc('AHB')} = 90^\\circ$;\\\\$[[fill:\\widehat{{BAH}}]]$ chung"],
            ["$[[fill:AH^2]] = AE \\cdot AC$", "$\\triangle AEH \\backsim \\triangle [[fill:AHC]]$ (g.g)",
             f"${goc('AEH')} = {goc('AHC')} = 90^\\circ$;\\\\$[[fill:\\widehat{{HAC}}]]$ chung"]),
    }

    # ── Bài 8: Ngô Gia Tự ý b ──────────────────────────────────────────────────
    ngt = hai_tt("A", "B", "C", "H")
    bai_2 = bai(
        "Bài 8.", 2, "onclass", "TH2",
        "[TH] Cho đường tròn $(O; R)$. Từ điểm $A$ nằm ngoài đường tròn kẻ các tiếp tuyến $AB$, $AC$ với đường tròn ($B$, $C$ là các tiếp điểm). "
        f"Gọi $H$ là giao điểm của $OA$ và $BC$ (Hình 4). Chứng minh $OA \\perp BC$ và $OH \\cdot OA = R^2$. {theo_so_do(4)}",
        giai_trung_truc("A", "B", "C", ket=f"{BR}$\\Rightarrow OA \\perp BC$ tại $H$.{BR}")
        + xet("OHB", "OBA", f"{goc('OHB')} = {goc('OBA')}", "$OA \\perp BC$ tại $H$, $AB$ là tiếp tuyến của $(O)$ tại $B$", goc("AOB"),
              "\\dfrac{OH}{OB} = \\dfrac{OB}{OA}", "OH \\cdot OA = OB^2 = R^2") + f".{BR}"
        + "Vậy $OA \\perp BC$ và $OH \\cdot OA = R^2$.",
        figure={"tikz": h_nen_tron(ngt), "tikz_gv": ngt, "caption": "Hình 4", "pos": "right"},
        so_do_nguoc=so_do(
            "$OH \\cdot OA = R^2$", ["$OH \\cdot OA = OB^2$", "$\\triangle OHB \\backsim \\triangle OBA$ (g.g)"],
            ["$OA \\perp BC$ tại $H$", "$OA$ là đường trung trực của $BC$", "$AB = AC$; $OB = OC = R$"],
            [f"${goc('OBA')} = 90^\\circ$ ($AB$ là tiếp tuyến);\\\\${goc('AOB')}$ chung"], ben="$R = OB$ (bán kính)"),
        phut_so_do=PHUT["Bài 8"], ve_tiep=3,
    )

    # ── Ví dụ 2: Dịch Vọng ý b ─────────────────────────────────────────────────
    dv = h_dich_vong()
    vi_du_2 = {
        "type": "noted", "variant": "example",
        "text": "\\textbf{Ví dụ 2.} Cho nửa đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $M$ bất kì thuộc nửa $(O; R)$, tiếp tuyến tại $A$ và $M$ "
                "của nửa đường tròn $(O; R)$ cắt nhau tại $C$ ($M$, $A$ là $2$ tiếp điểm). Đoạn thẳng $CB$ cắt nửa đường tròn tại $K$ ($K \\ne B$) (Hình 5). "
                "Vẽ tiếp vào Hình 5 các yếu tố còn thiếu theo đề. Chứng minh $\\triangle AKB$ vuông và $BK \\cdot BC = 4R^2$."
                f"{BR}{LG}{BR}"
                f"Xét $\\triangle AKB$ có $KO$ là đường [[fill:trung tuyến]] ứng với cạnh $AB$ ($O$ là trung điểm của $AB$).{BR}"
                f"$OK = OA = OB = R \\Rightarrow KO = \\dfrac{{1}}{{2}}[[fill:AB]]${BR}"
                f"$\\Rightarrow \\triangle AKB$ vuông tại $[[fill:K]]$ (tam giác có đường trung tuyến bằng nửa cạnh tương ứng).{BR}"
                f"Xét $\\triangle BKA$ và $\\triangle BAC$ có:{BR}"
                f"${goc('BKA')} = {goc('BAC')} = 90^\\circ$ ($\\triangle AKB$ vuông, $AC$ là [[fill:tiếp tuyến]] của $(O)$ tại $A$){BR}"
                f"$[[fill:\\widehat{{ABC}}]]$ chung{BR}"
                f"$\\Rightarrow \\triangle BKA \\backsim \\triangle [[fill:BAC]]$ (g.g){BR}"
                f"$\\Rightarrow \\dfrac{{BK}}{{BA}} = [[fill:\\dfrac{{BA}}{{BC}}|1.3cm]]${BR}"
                f"$\\Rightarrow BK \\cdot BC = [[fill:BA^2]]$.{BR}"
                "Vậy $\\triangle AKB$ vuông và $BK \\cdot BC = 4R^2$ (vì $BA = [[fill:2R]]$).",
        "figure": {"tikz": h_nen_duong_kinh_doc("A", "B", nua=True, day_du=dv), "tikz_gv": dv, "caption": "Hình 5", "pos": "right"},
        "so_do_nguoc": so_do(
            "$BK \\cdot BC = 4R^2$", ["$BK \\cdot BC = [[fill:BA^2|1.1cm]]$", "$\\triangle BKA \\backsim \\triangle [[fill:BAC]]$ (g.g)"],
            ["$\\triangle AKB$ vuông tại $[[fill:K]]$", "$KO = \\dfrac{1}{2}[[fill:AB]]$", "$KO$ là đường [[fill:trung tuyến|1.8cm]];\\\\$OK = OA = OB = R$"],
            [f"${goc('BAC')} = 90^\\circ$ ($AC$ là [[fill:tiếp tuyến|1.8cm]]);\\\\$[[fill:\\widehat{{ABC}}]]$ chung"], ben="$BA = [[fill:2R|0.9cm]]$ (đường kính)", ben_x=4.4),
    }

    # ── Bài 9: Thanh Trì ý a, phần CE.CB = CA² ─────────────────────────────────
    tt = h_thanh_tri()
    bai_3 = bai(
        "Bài 9.", 2, "onclass", "TH3",
        "[TH] Cho nửa đường tròn $(O)$, đường kính $AB$. Trên nửa đường tròn $(O)$ lấy một điểm $D$ ($D$ khác $A$ và $B$). Tiếp tuyến của nửa đường tròn "
        f"$(O)$ tại $A$ và $D$ cắt nhau ở điểm $C$. Tia $BC$ cắt nửa đường tròn $(O)$ tại $E$ (Hình 6). Chứng minh $\\triangle AEB$ vuông và $CE \\cdot CB = CA^2$. {theo_so_do(6)}",
        giai_vuong("E", "A", "B", ban_kinh="", ket="AE \\perp BC$ tại $E")
        + xet("CEA", "CAB", f"{goc('CEA')} = {goc('CAB')}", "$AE \\perp BC$ tại $E$, $CA$ là tiếp tuyến của $(O)$ tại $A$", goc("ACB"),
              "\\dfrac{CE}{CA} = \\dfrac{CA}{CB}", "CE \\cdot CB = CA^2") + f".{BR}"
        + "Vậy $\\triangle AEB$ vuông và $CE \\cdot CB = CA^2$.",
        figure={"tikz": h_nen_duong_kinh_ngang("A", "B", tt), "tikz_gv": tt, "caption": "Hình 6", "pos": "right"},
        so_do_nguoc=so_do(
            "$CE \\cdot CB = CA^2$", ["$\\triangle CEA \\backsim \\triangle CAB$ (g.g)"],
            ["$AE \\perp BC$ ($\\triangle AEB$ vuông tại $E$)", "$EO = \\dfrac{AB}{2}$", "$EO$ là đường trung tuyến;\\\\$OE = OA = OB$ (bán kính)"],
            [f"${goc('CAB')} = 90^\\circ$ ($CA$ là tiếp tuyến);\\\\${goc('ACB')}$ chung"]),
        phut_so_do=PHUT["Bài 9"], ve_tiep=3,
    )

    # ── Bài 10: đích Tạ Quang Bửu a, b ──────────────────────────────────────────
    tqb = h_ta_quang_buu()
    bai_4 = bai(
        "Bài 10.", 3, "onclass", "TH1+VD1",
        "Cho đường tròn $(O; R)$ và điểm $M$ nằm ngoài đường tròn. Qua $M$ kẻ hai tiếp tuyến $MA$, $MB$ với đường tròn ($A$, $B$ là các tiếp điểm). "
        "Đoạn thẳng $OM$ cắt đoạn thẳng $AB$ tại $H$.[[br]]"
        "a) [TH] Chứng minh bốn điểm $M$, $A$, $O$, $B$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Kẻ đường kính $AD$ của đường tròn $(O; R)$. Đoạn thẳng $MD$ cắt đường tròn tại điểm $C$ khác $D$. "
        "Chứng minh $AB \\perp OM$ và $MH \\cdot MO = MC \\cdot MD$.",
        "a) " + giai_bon_diem("M", "A", "B")
        + f"Vậy bốn điểm $M, A, O, B$ cùng thuộc đường tròn đường kính $MO$.{BR}"
        + "b) " + giai_trung_truc("M", "A", "B", ket=f"{BR}$\\Rightarrow AB \\perp OM$ tại $H$.{BR}")
        + xet("MHA", "MAO", f"{goc('MHA')} = {goc('MAO')}", "$AB \\perp OM$ tại $H$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AMO"),
              "\\dfrac{MH}{MA} = \\dfrac{MA}{MO}", "MA^2 = MH \\cdot MO") + f". (1){BR}"
        + giai_vuong("C", "A", "D", ket="AC \\perp MD$ tại $C")
        + xet("MCA", "MAD", f"{goc('MCA')} = {goc('MAD')}", "$AC \\perp MD$ tại $C$, $MA$ là tiếp tuyến của $(O)$ tại $A$", goc("AMD"),
              "\\dfrac{MC}{MA} = \\dfrac{MA}{MD}", "MA^2 = MC \\cdot MD") + f". (2){BR}"
        + "Vậy $AB \\perp OM$ và từ (1), (2) có $MH \\cdot MO = MC \\cdot MD$ (cùng bằng $MA^2$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_diem_ngoai("M", tqb), "tikz_gv": tqb, "caption": "Hình 7", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $AB$?",
               "Trong $\\triangle ACD$, đoạn $CO$ có quan hệ gì với cạnh $AD$?",
               "Hai tích $MH \\cdot MO$ và $MC \\cdot MD$ cùng bằng đại lượng nào?"],
        quy_trinh=["Vẽ tiếp hình: hai tiếp tuyến $MA$, $MB$; đoạn $OM$, $AB$ cắt nhau tại $H$; đường kính $AD$, đoạn $MD$, điểm $C$; đánh dấu các góc vuông",
                   "Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$",
                   "Ý b: $MA = MB$, $OA = OB = R$ $\\Rightarrow OM$ là đường trung trực của $AB$ $\\Rightarrow AB \\perp OM$ tại $H$",
                   "$\\triangle MHA \\backsim \\triangle MAO$ (g.g) $\\Rightarrow MA^2 = MH \\cdot MO$ (như Bài 8)",
                   "$CO = \\dfrac{AD}{2}$ $\\Rightarrow \\triangle ACD$ vuông tại $C$ $\\Rightarrow AC \\perp MD$; $\\triangle MCA \\backsim \\triangle MAD$ (g.g) $\\Rightarrow MA^2 = MC \\cdot MD$ (như Ví dụ 2, Bài 9)",
                   "Hai tích cùng bằng $MA^2$ $\\Rightarrow MH \\cdot MO = MC \\cdot MD$ (như Ví dụ 1)"],
    )

    # ── BTVN ───────────────────────────────────────────────────────────────────
    btvn_1 = bai(
        "BTVN 1.", 1, "btvn", "NB3",
        "Cho đường tròn $(O; R)$, đường kính $AB$. Lấy $C$ thuộc đường tròn $(O)$ ($C$ khác $A$ và $B$). Tiếp tuyến tại $A$ của đường tròn $(O)$ "
        "cắt đường thẳng $BC$ tại $M$ (Hình 8). Mỗi khẳng định sau đúng hay sai?",
        "a) Đ · b) Đ",
        dung_sai=["$\\triangle ABC$ vuông tại $C$.", "$BC \\cdot BM = 4R^2$."],
        figure_given=True, figure={"tikz": rong(h_c44(), -4.6, -1.4, 4.6, 1.9), "caption": "Hình 8", "pos": "right"},
    )

    nt = h_nghia_tan()
    khung_nt = (
        "Vì $CE \\perp AB$ tại $E$ $\\Rightarrow \\triangle BEC$ vuông tại $[[blank:1.1cm]]$[[br]]"
        "$\\Rightarrow B, E, C$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "Vì $BD \\perp AC$ tại $D$ $\\Rightarrow \\triangle BDC$ vuông tại $[[blank:1.1cm]]$[[br]]"
        "$\\Rightarrow B, D, C$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "Vậy bốn điểm $B, E, D, C$ cùng thuộc đường tròn đường kính $[[blank:1.1cm]]$.[[br]]"
        "b) [NB] Chứng minh $BE \\cdot BA = BH \\cdot BD$:[[br]]"
        "Xét $\\triangle BEH$ và $\\triangle BDA$ có:[[br]]"
        "$\\widehat{BEH} = \\widehat{BDA} = [[blank:1.1cm]]$ ($CE \\perp AB$, $BD \\perp AC$)[[br]]"
        "$[[blank:1.6cm]]$ chung[[br]]"
        "$\\Rightarrow \\triangle BEH \\backsim \\triangle [[blank:1.6cm]]$ (g.g)[[br]]"
        "$\\Rightarrow \\dfrac{BE}{BD} = [[blank:1.6cm]]$[[br]]"
        "Vậy $BE \\cdot BA = BH \\cdot BD$."
    )
    btvn_2 = bai(
        "BTVN 2.", 1, "btvn", "NB4",
        "Cho $\\triangle ABC$ nhọn có ba đỉnh nằm trên $(O)$ và $AB < AC$. Các đường cao $BD$, $CE$ cắt nhau tại $H$ (Hình 9).[[br]]"
        "Vẽ tiếp vào Hình 9 các yếu tố còn thiếu theo đề, đánh dấu các góc vuông, rồi điền vào chỗ chấm để hoàn thành bài giải:[[br]]"
        "a) [NB] Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn:[[br]]" + khung_nt,
        "a) $E$; $BC$; $D$; $BC$; $BC$.[[br]]b) $90^\\circ$; $\\widehat{ABD}$; $BDA$; $\\dfrac{BH}{BA}$.",
        statement_slide="Cho $\\triangle ABC$ nhọn có ba đỉnh nằm trên $(O)$ và $AB < AC$. Các đường cao $BD$, $CE$ cắt nhau tại $H$ (Hình 9).[[br]]"
                        "a) [NB] Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn.[[br]]b) [NB] Chứng minh $BE \\cdot BA = BH \\cdot BD$.",
        figure_given=True, ve_tiep=3,
        figure={"tikz": h_nen_nghia_tan(nt), "tikz_gv": nt, "caption": "Hình 9", "pos": "right"},
    )

    cg = h_cau_giay()
    btvn_3 = bai(
        "BTVN 3.", 2, "btvn", "TH2",
        "[TH] Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Từ $A$ kẻ tiếp tuyến $AB$ với đường tròn $(O)$ ($B$ là tiếp điểm). "
        "Kẻ đường kính $BC$ của đường tròn $(O)$, đoạn thẳng $AC$ cắt đường tròn $(O)$ tại điểm thứ hai $D$. Kẻ $OH \\perp CD$ ($H \\in CD$) (Hình 10). "
        f"Chứng minh $\\triangle OHC$ đồng dạng với $\\triangle ABC$ và $CH \\cdot CA = 2R^2$. {theo_so_do(10)}",
        xet("OHC", "ABC", f"{goc('OHC')} = {goc('ABC')}", "$OH \\perp CD$, $AB$ là tiếp tuyến của $(O)$ tại $B$", goc("ACB"),
            "\\dfrac{CH}{CB} = \\dfrac{CO}{CA}", "CH \\cdot CA = CO \\cdot CB") + f".{BR}"
        + f"$CO = R$, $CB = 2R$ (đường kính) $\\Rightarrow CH \\cdot CA = R \\cdot 2R = 2R^2$.{BR}"
        + "Vậy $\\triangle OHC$ đồng dạng với $\\triangle ABC$ và $CH \\cdot CA = 2R^2$.",
        draw=True, phut_so_do=PHUT["BTVN 3"],
        figure={"tikz": h_nen_diem_ngoai("A", cg), "tikz_gv": cg, "caption": "Hình 10", "pos": "right"},
        so_do_nguoc=so_do(
            "$CH \\cdot CA = 2R^2$", ["$CH \\cdot CA = CO \\cdot CB$", "$\\triangle OHC \\backsim \\triangle ABC$ (g.g)"],
            [f"${goc('OHC')} = 90^\\circ$ ($OH \\perp CD$)"],
            [f"${goc('ABC')} = 90^\\circ$ ($AB$ là tiếp tuyến);\\\\${goc('ACB')}$ chung"], rong=3.0, ben="$CO = R$; $CB = 2R$"),
    )

    lb = h_long_bien()
    btvn_4 = bai(
        "BTVN 4.", 2, "btvn", "TH3",
        "[TH] Cho nửa đường tròn $(O)$, đường kính $AB$. Trên nửa đường tròn $(O)$ lấy điểm $M$ ($M$ khác $A$ và $B$). Trên cung $MB$ của nửa đường tròn $(O)$ "
        "lấy điểm $N$ ($N$ khác $M$ và $B$). Gọi $H$ là hình chiếu của điểm $M$ trên đoạn thẳng $AB$; $I$ là giao điểm của hai đoạn thẳng $AN$ và $MH$ (Hình 11). "
        f"Chứng minh $AI \\cdot AN = AH \\cdot AB$. {theo_so_do(11)}",
        giai_vuong("N", "A", "B", ban_kinh="")
        + xet("AHI", "ANB", f"{goc('AHI')} = {goc('ANB')}", "$MH \\perp AB$ tại $H$, $\\triangle ANB$ vuông tại $N$", goc("NAB"),
              "\\dfrac{AH}{AN} = \\dfrac{AI}{AB}", "AI \\cdot AN = AH \\cdot AB") + f".{BR}"
        + "Vậy $AI \\cdot AN = AH \\cdot AB$.",
        draw=True, phut_so_do=PHUT["BTVN 4"],
        figure={"tikz": h_nen_duong_kinh_ngang("A", "B", lb), "tikz_gv": lb, "caption": "Hình 11", "pos": "right"},
        so_do_nguoc=so_do(
            "$AI \\cdot AN = AH \\cdot AB$", ["$\\triangle AHI \\backsim \\triangle ANB$ (g.g)"],
            ["$\\triangle ANB$ vuông tại $N$", "$NO = \\dfrac{AB}{2}$", "$NO$ là đường trung tuyến;\\\\$ON = OA = OB$ (bán kính)"],
            [f"${goc('AHI')} = 90^\\circ$ ($MH \\perp AB$);\\\\${goc('NAB')}$ chung"]),
    )

    xl = h_xuan_la()
    btvn_5 = bai(
        "BTVN 5.", 3, "btvn", "TH1+VD1",
        "Cho đường tròn $(O; R)$ và một điểm $A$ nằm bên ngoài đường tròn sao cho $OA > 2R$. Qua $A$ kẻ hai tiếp tuyến $AM$, $AN$ với đường tròn $(O)$ "
        "($M$, $N$ là hai tiếp điểm). Vẽ đường kính $MC$ của đường tròn $(O)$, $AC$ cắt đường tròn $(O)$ tại điểm thứ hai là $B$ ($B$ khác $C$).[[br]]"
        "a) [TH] Chứng minh bốn điểm $A$, $M$, $O$, $N$ cùng thuộc một đường tròn.[[br]]"
        "b) [VD] Gọi $H$ là giao điểm của $OA$ và $MN$. Chứng minh $OA \\perp MN$ và $AH \\cdot AO = AB \\cdot AC$.",
        "a) " + giai_bon_diem("A", "M", "N")
        + f"Vậy bốn điểm $A, M, O, N$ cùng thuộc đường tròn đường kính $AO$.{BR}"
        + "b) " + giai_trung_truc("A", "M", "N", ket=f"{BR}$\\Rightarrow OA \\perp MN$ tại $H$.{BR}")
        + xet("AHM", "AMO", f"{goc('AHM')} = {goc('AMO')}", "$OA \\perp MN$ tại $H$, $AM$ là tiếp tuyến của $(O)$ tại $M$", goc("MAO"),
              "\\dfrac{AH}{AM} = \\dfrac{AM}{AO}", "AM^2 = AH \\cdot AO") + f". (1){BR}"
        + giai_vuong("B", "M", "C", ket="MB \\perp AC$ tại $B")
        + xet("ABM", "AMC", f"{goc('ABM')} = {goc('AMC')}", "$MB \\perp AC$ tại $B$, $AM$ là tiếp tuyến của $(O)$ tại $M$", goc("MAC"),
              "\\dfrac{AB}{AM} = \\dfrac{AM}{AC}", "AM^2 = AB \\cdot AC") + f". (2){BR}"
        + "Vậy $OA \\perp MN$ và từ (1), (2) có $AH \\cdot AO = AB \\cdot AC$ (cùng bằng $AM^2$).",
        figure_given=False, draw=True,
        figure={"tikz": h_nen_diem_ngoai("A", xl), "tikz_gv": xl, "caption": "Hình 12", "pos": "right"},
        hints=["Đỉnh góc vuông thuộc đường tròn đường kính nào?",
               "Hai điểm nào cùng cách đều hai đầu mút của đoạn thẳng $MN$?",
               "Trong $\\triangle MBC$, đoạn $BO$ có quan hệ gì với cạnh $MC$?",
               "Hai tích $AH \\cdot AO$ và $AB \\cdot AC$ cùng bằng đại lượng nào?"],
    )

    return {
        "slug": PHIEU.stem,
        "title": "Chứng minh đẳng thức tích bằng tam giác đồng dạng",
        "eyebrow": "PHIẾU 4 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 16 (LUYỆN TẬP)",
        "grade_label": "Lớp 9 • Hình học",
        "class_tier": "C",
        "btvn_phieu_rieng": True,
        "stages": [
            {"kind": "review", "number": 1, "title": "Khám phá",
             "teacher_note": "Không tính bằng số (góp ý 09/10): câu a, b dẫn vào trường hợp đồng dạng g.g của hai tam giác vuông (Lớp 8), công cụ duy nhất của buổi này. "
                             "Hệ thức lượng đã giảm tải, HS không được dùng thẳng. Câu c cho đẳng thức tích đầu tiên $AB^2 = AH \\cdot AO$.",
             "blocks": [
                 {"type": "para", "text": "\\textbf{Hai tích bằng nhau — trùng hợp hay có lí do?}"},
                 {"type": "noted", "variant": "note",
                  "text": "Tam giác $ABO$ vuông tại $B$, đường cao $BH$ (Hình 1).[[br]]"
                          "\\textbf{a)} Hai tam giác vuông $AHB$ và $ABO$ có chung góc nào?[[br]]"
                          "\\textbf{b)} Hai tam giác đó có đồng dạng không? Viết các tỉ số cạnh tương ứng bằng nhau.[[br]]"
                          "\\textbf{c)} Từ tỉ số $\\dfrac{AH}{AB} = \\dfrac{AB}{AO}$ rút ra được đẳng thức nào giữa $AB$, $AH$, $AO$?",
                  "figure": {"tikz": h_kham_pha(), "caption": "Hình 1", "pos": "right"}},
             ]},
            {"kind": "concept", "number": 2, "title": "Kiến thức trọng tâm",
             "teacher_note": "Phần A đọc đúng lời SGK Toán 8 tập 2 (Bài 56, Định lí 1, tr.98). Phần B là phương pháp cho vế tích của ý b Câu IV.2: "
                             "đẳng thức tích có ở 59\\% đề Kì I. Hệ thức lượng đã giảm tải nên mọi đẳng thức tích phải đi qua tam giác đồng dạng; "
                             "ví dụ của từng dạng nằm ngay ở Luyện tập 1.",
             "blocks": [
                 {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
                 {"type": "noted", "variant": "theory", "title": "1. HAI TAM GIÁC VUÔNG ĐỒNG DẠNG (LỚP 8)",
                  "text": "\\nhanly{Định lí.} Nếu một góc nhọn của tam giác vuông này bằng một góc nhọn của tam giác vuông kia thì hai tam giác vuông đó đồng dạng với nhau.[[br]]"
                          "\\nhanly{Từ tỉ số ra tích:} $\\triangle AHB \\backsim \\triangle ABO \\Rightarrow \\dfrac{AH}{AB} = \\dfrac{AB}{AO} \\Rightarrow AB^2 = AH \\cdot AO$.[[br]]"
                          "\\nhanly{Chú ý:} viết hai tam giác đúng thứ tự đỉnh tương ứng: đỉnh góc vuông ứng với đỉnh góc vuông, đỉnh góc chung ứng với đỉnh góc chung.",
                  "figure": {"tikz": h_kham_pha(), "caption": "$\\triangle AHB$ và $\\triangle ABO$ vuông, chung góc $A$", "pos": "below"}},
                 {"type": "noted", "variant": "theory", "title": "2. KIẾN THỨC ĐÃ HỌC THƯỜNG DÙNG",
                  "text": "\\nhanly{Tiếp tuyến (Bài 16):} Tiếp tuyến vuông góc với bán kính đi qua tiếp điểm.[[br]]"
                          "\\nhanly{Hai tiếp tuyến (Phiếu 3):} $AB = AC$, $OB = OC$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$.[[br]]"
                          "\\nhanly{Trung tuyến (SGK Toán 8, tập 1, tr.66):} Nếu tam giác có một đường trung tuyến bằng nửa cạnh tương ứng thì tam giác đó là tam giác vuông.",
                  "figure": {"tikz": h_tich_cu(), "caption": "$AO = OB = OC$ $\\Rightarrow \\triangle ABC$ vuông tại $A$", "pos": "below"}},
                 {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
                 the_dang_1,
                 the_dang_2,
             ]},
            {"kind": "practice1", "number": 3, "title": "Luyện tập 1",
             "teacher_note": GHI_CHU_LT1,
             "blocks": [
                 {"type": "para", "text": "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Tạ Quang Bửu) ở Bài 10: ý a chứng minh bốn điểm cùng thuộc một đường "
                                          "tròn (đã học ở Phiếu 2), ý b chứng minh vuông góc (đã học ở Phiếu 3) và đẳng thức tích."},
                 {"type": "para", "variant": "heading", "text": "Mạch 1. Ý b — Đẳng thức tích từ hai tam giác vuông chung góc nhọn"},
                 ti_1, ti_2, ti_3, ti_4, tn_1, tn_2, tn_3, vi_du_1, bai_2,
                 {"type": "para", "variant": "heading", "text": "Mạch 2. Ý b — Có đường kính: tam giác vuông rồi đẳng thức tích"},
                 vi_du_2, bai_3,
             ]},
            {"kind": "practice2", "number": 4, "title": "Luyện tập 2",
             "teacher_note": GHI_CHU_LT2,
             "blocks": [
                 {"type": "para", "variant": "heading", "text": "Đề thi Học kì I — THCS \\& THPT Tạ Quang Bửu"},
                 bai_4,
             ]},
            {"kind": "reflection", "number": 5, "title": "Sơ đồ tư duy",
             "teacher_note": GHI_CHU_BTVN,
             "blocks": [
                 {"type": "mindmap", "caption": "Sơ đồ tư duy: Chứng minh đẳng thức tích bằng tam giác đồng dạng",
                  "root": "ĐẲNG THỨC TÍCH",
                  "branches": [
                      {"label": "CÔNG CỤ", "children": [{"label": "Hai tam giác vuông có một góc nhọn bằng nhau thì đồng dạng"},
                                                         {"label": "Tỉ số cạnh tương ứng $\\Rightarrow$ tích"}]},
                      {"label": "CHUNG GÓC NHỌN", "children": [{"label": "$\\triangle OHB \\backsim \\triangle OBA$ $\\Rightarrow OH \\cdot OA = R^2$"},
                                                                 {"label": "Hai tích: cùng bằng đại lượng thứ ba"}]},
                      {"label": "CÓ ĐƯỜNG KÍNH", "children": [{"label": "Trung tuyến bằng nửa cạnh $\\Rightarrow$ tam giác vuông"},
                                                                {"label": "$\\triangle MCA \\backsim \\triangle MAD$ $\\Rightarrow MA^2 = MC \\cdot MD$"}]},
                  ]},
                 btvn_1, btvn_2, btvn_3, btvn_4, btvn_5,
             ]},
        ],
    }


# ── Thuyết minh ────────────────────────────────────────────────────────────────
GIO_THUC_TM = [
    "\\quad Giờ thực lớp C (05/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 65′ (7 câu trắc nghiệm, 2 ví dụ HS vẽ cùng GV và điền sơ đồ ngược, "
    "2 bài theo sơ đồ ngược HS trình bày vào vở $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 21′ (đề đích Tạ Quang Bửu ý b, HS tự vẽ) · chữa bài (có ý a đề đích), chốt khoảng 5′ · BTVN khoảng 72′ (quỹ 40′, cố ý dày hơn)",
]
DANG_VD_4 = ("Buổi 4 — Câu IV.2 hai ý (đề Tạ Quang Bửu): bốn điểm $M$, $A$, $O$, $B$; $AB \\perp OM$ và $MH \\cdot MO = MC \\cdot MD$ "
             "(hai cặp tam giác đồng dạng, bắc cầu qua $MA^2$). BTVN: đề Xuân La.")
VIDU_4 = ("Buổi 4: Đề mẫu (Chương Mỹ): tam giác có đường cao $AH$, $HD \\perp AB$, $HE \\perp AC$ — $AD \\cdot AB = AE \\cdot AC$ (hai cặp đồng dạng, bắc cầu qua $AH^2$). "
          "Đề mẫu (Dịch Vọng): $\\triangle AKB$ vuông, $BK \\cdot BC = 4R^2$.")


def dong_tm(phut) -> list[dict]:
    return [
        {"band": "NB", "loai": "NB tách TH", "dang": "Trắc nghiệm: đổi đẳng thức tích thành tỉ lệ thức, từ tỉ lệ thức đọc ra hai tam giác cần chứng minh đồng dạng ($OH \\cdot OA = OB^2$ tách từ đề Ngô Gia Tự ý b; $CH \\cdot CA = CO \\cdot CB$ tách từ đề Cầu Giấy ý b)",
         "source_refs": ["ck1-ngo-gia-tu-2025-IV2.b", "ck1-cau-giay-2024-IV2.b"], "vidu": 0, "onclass": 4, "btvn": 0, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB kiến thức cũ", "dang": "Chứng minh hai tam giác đồng dạng (Lớp 8), trắc nghiệm: thêm điều kiện góc cho g.g (đề Thanh Trì); viết đúng thứ tự đỉnh (đề Đan Phượng); các cặp đồng dạng trong tam giác vuông có đường cao (đề Mai Dịch)",
         "source_refs": ["l8-ck2-2023-thanh-tri-c6", "l8-ck2-x-2023-2024-de-thi-hk2-gddt-dan-phuong-hn-c8", "l8-gk2-2025-thcs-mai-dich-c8"], "vidu": 0, "onclass": 3, "btvn": 0, "lythuyet": 1, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB lẻ LT", "dang": "Đúng/Sai trên hình có đường kính in sẵn: $\\triangle ABC$ vuông tại $C$, $BC \\cdot BM = 4R^2$ (BTVN)",
         "source_refs": ["stk-b16-II-C44-tr246.a", "stk-b16-II-C44-tr246.b"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "none", "hinh_san": True},
        {"band": "NB", "loai": "NB ghép bài", "dang": "Vẽ tiếp hình nền, điền khung bài giải: bốn điểm cùng thuộc đường tròn đường kính $BC$; $\\triangle BEH \\backsim \\triangle BDA$ $\\Rightarrow BE \\cdot BA = BH \\cdot BD$ (BTVN đề Nghĩa Tân GK1 ý 1, phần đẳng thức tích của ý 2)",
         "source_refs": ["gk1-nghia-tan-2025-IV.a", "gk1-nghia-tan-2025-IV.b"], "vidu": 0, "onclass": 0, "btvn": 2, "lythuyet": 0, "decompose": "none",
         "hinh_san": True, "gian_giao": "dien-khuyet", "khung": True, "ve_tiep": {"btvn": 3}},
        {"band": "TH", "loai": "TH ghép bài", "dang": "Ý a của đề thi, HS tự vẽ hình, tự trình bày: bốn điểm cùng thuộc một đường tròn (đề đích Tạ Quang Bửu ý a); bốn điểm $A$, $M$, $O$, $N$ (BTVN đề Xuân La ý a)",
         "source_refs": ["ck1-ta-quang-buu-2025-IV2.a", "ck1-xuan-la-2024-4.2.a"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_hinh": {"onclass": 1, "btvn": 1}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ý b đề thi, một cặp tam giác vuông chung góc nhọn: $OA \\perp BC$ và $OH \\cdot OA = R^2$. HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (trên lớp đề Ngô Gia Tự ý b; BTVN đề Cầu Giấy ý b, $CH \\cdot CA = 2R^2$). Ví dụ mẫu ở dòng VD",
         "source_refs": ["ck1-ngo-gia-tu-2025-IV2.b", "ck1-cau-giay-2024-IV2.b"], "vidu": 0, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"onclass": 3}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"onclass": phut["Bài 8"], "btvn": phut["BTVN 3"]}},
        {"band": "TH", "loai": "TH tách VD", "dang": "Ý b đề thi, có đường kính: trung tuyến bằng nửa cạnh cho tam giác vuông rồi đẳng thức tích. Ví dụ mẫu đề Dịch Vọng ý b ($BK \\cdot BC = 4R^2$); HS vẽ tiếp hình nền, đọc sơ đồ ngược rồi tự trình bày vào vở (trên lớp đề Thanh Trì ý a, phần $CE \\cdot CB = CA^2$ của ý b; BTVN đề Long Biên, phần $AI \\cdot AN = AH \\cdot AB$ của ý b)",
         "source_refs": ["ck1-dich-vong-42.b", "ck1-thanh-tri-2024-IV2.a", "ck1-thanh-tri-2024-IV2.b", "ck1-long-bien-2024-IV2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "th2nb",
         "hinh_san": False, "ve_tiep": {"vidu": 3, "onclass": 3}, "ve_hinh": {"btvn": 1},
         "phut_so_do": {"onclass": phut["Bài 9"], "btvn": phut["BTVN 4"]}},
        {"band": "VD", "loai": "VD lẻ", "dang": "Ý b của đề thi (đề Tạ Quang Bửu, đích của buổi): $AB \\perp OM$ và $MH \\cdot MO = MC \\cdot MD$ (hai cặp tam giác đồng dạng, bắc cầu qua $MA^2$). Ví dụ mẫu đề Chương Mỹ ý b (bắc cầu qua $AH^2$); BTVN đề Xuân La, phần $AH \\cdot AO = AB \\cdot AC$ của ý b",
         "source_refs": ["ck1-ta-quang-buu-2025-IV2.b", "ck1-chuong-my-2024-4.2.b", "ck1-xuan-la-2024-4.2.b"], "vidu": 1, "onclass": 1, "btvn": 1, "lythuyet": 0, "decompose": "vd",
         "hinh_san": False, "gian_giao": "ve-hinh", "ve_tiep": {"vidu": 2},
         "quy_trinh": ["Ý a: hai góc vuông tại hai tiếp điểm có chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$",
                       "Ý b: $MA = MB$, $OA = OB$ $\\Rightarrow OM$ là đường trung trực của $AB$ $\\Rightarrow AB \\perp OM$ tại $H$",
                       "$\\triangle MHA \\backsim \\triangle MAO$ (g.g) $\\Rightarrow MA^2 = MH \\cdot MO$ (như Bài 8)",
                       "$CO = \\dfrac{AD}{2}$ $\\Rightarrow \\triangle ACD$ vuông tại $C$ $\\Rightarrow AC \\perp MD$; $\\triangle MCA \\backsim \\triangle MAD$ (g.g) $\\Rightarrow MA^2 = MC \\cdot MD$ (như Ví dụ 2, Bài 9)",
                       "Hai tích cùng bằng $MA^2$ (như Ví dụ 1)"]},
    ]


def main():
    kiem_toan_do()
    les = gon_hinh(lesson())
    PHIEU.write_text(json.dumps(les, ensure_ascii=False, indent=2) + "\n", "utf-8")
    tm = json.loads(TM.read_text("utf-8"))
    p4 = next(p for p in tm["phieu"] if p["code"] == "4")
    p4["rows"] = dong_tm(PHUT)
    i = next(i for i, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 4"))
    j = next(j for j, x in enumerate(tm["thoiluong"]) if x.startswith("Buổi 5"))
    tm["thoiluong"][i + 1:j] = GIO_THUC_TM
    tm["dang_vd"] = [DANG_VD_4 if x.startswith("Buổi 4") else x for x in tm["dang_vd"]]
    tm["vidu"] = [VIDU_4 if x.startswith("Buổi 4") else x for x in tm["vidu"]]
    TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2), "utf-8")
    print("ghi xong", PHIEU.name)


if __name__ == "__main__":
    main()
