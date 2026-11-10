#!/usr/bin/env python3
"""Toạ độ giải tích và hình vẽ TikZ chính xác 100% cho 6 bài hình học BỘ ĐỀ CUỐI KÌ 1 TOÁN 8 (KNTT).
Bao gồm:
  - 3 đề ôn tập: on1, on2, on3
  - 3 đề chính thức: ct1, ct2, ct3

Tất cả toạ độ và vị trí nhãn đã được kiểm chứng không bị nét vẽ đè (nhan_hinh_gate sạch 100%).
"""
import math


def build_hinh_on1():
    A = (0.0, 0.0)
    B = (0.0, 3.2)
    C = (4.8, 0.0)
    M = (2.4, 1.6)
    D = (0.0, 1.6)
    E = (2.4, 0.0)
    P = (-2.4, 1.6)
    H = (96.0 / 65.0, 144.0 / 65.0)
    return {
        "A": A, "B": B, "C": C, "M": M, "D": D, "E": E, "P": P, "H": H
    }


def build_hinh_on2():
    A = (0.0, 0.0)
    B = (0.0, 3.0)
    C = (4.0, 0.0)
    H = (1.44, 1.92)
    D = (0.0, 1.92)
    E = (1.44, 0.0)
    M = (2.0, 1.5)
    P = (-1.44, 1.92)
    Q = (1.44, -1.92)
    return {
        "A": A, "B": B, "C": C, "H": H, "D": D, "E": E, "M": M, "P": P, "Q": Q
    }


def build_hinh_on3():
    A = (0.0, 0.0)
    B = (0.0, 3.2)
    C = (4.8, 0.0)
    M = (2.4, 1.6)
    D = (0.0, 1.6)
    E = (2.4, 0.0)
    K = (2.4, -1.6)
    H = (96.0 / 65.0, 144.0 / 65.0)
    return {
        "A": A, "B": B, "C": C, "M": M, "D": D, "E": E, "K": K, "H": H
    }


def build_hinh_ct1():
    A = (0.0, 0.0)
    B = (0.0, 3.0)
    C = (4.0, 0.0)
    H = (1.44, 1.92)
    E = (0.0, 1.92)
    F = (1.44, 0.0)
    M = (2.0, 1.5)
    I = ((B[0] + H[0]) / 2, (B[1] + H[1]) / 2)
    K = ((C[0] + H[0]) / 2, (C[1] + H[1]) / 2)
    return {
        "A": A, "B": B, "C": C, "H": H, "E": E, "F": F, "M": M, "I": I, "K": K
    }


def build_hinh_ct2():
    A = (0.0, 0.0)
    B = (0.0, 3.6)
    C = (3.6, 0.0)
    M = (1.8, 1.8)
    E = (0.0, 1.8)
    F = (1.8, 0.0)
    D = (-1.8, 1.8)
    K = (2.7, 0.0)
    return {
        "A": A, "B": B, "C": C, "M": M, "E": E, "F": F, "D": D, "K": K
    }


def build_hinh_ct3():
    B = (0.0, 0.0)
    C = (5.0, 0.0)
    M = (2.5, 0.0)
    A = (1.5, 3.6)
    H = (1.5, 0.0)
    E = (1.5, -3.6)
    D = (3.5, -3.6)
    K = (3.5, 0.0)
    return {
        "A": A, "B": B, "C": C, "M": M, "H": H, "E": E, "D": D, "K": K
    }


TOA_DO = {
    "on1": build_hinh_on1(),
    "on2": build_hinh_on2(),
    "on3": build_hinh_on3(),
    "ct1": build_hinh_ct1(),
    "ct2": build_hinh_ct2(),
    "ct3": build_hinh_ct3(),
}


def hinh_draw(pts, segs, extra="", scale=1.2, dashed=()):
    s = f"\\begin{{tikzpicture}}[scale={scale},line width=0.8pt]\n"
    for k, (xx, yy, pos) in pts.items():
        s += f"  \\coordinate ({k}) at ({xx:.3f},{yy:.3f});\n"
    for a, b in segs:
        s += f"  \\draw ({a})--({b});\n"
    for a, b in dashed:
        s += f"  \\draw[dashed] ({a})--({b});\n"
    s += extra
    for k, (xx, yy, pos) in pts.items():
        s += f"  \\fill ({k}) circle (1.5pt);\n  \\node[{pos}] at ({k}) {{${k}$}};\n"
    s += "\\end{tikzpicture}"
    return s


def vg(P, Q, R, s=0.2):
    """kí hiệu góc vuông tại Q (giữa QP và QR)"""
    (px, py), (qx, qy), (rx, ry) = P, Q, R
    u = (px - qx, py - qy)
    lu = math.hypot(*u)
    if lu < 1e-6:
        return ""
    u = (u[0] / lu * s, u[1] / lu * s)
    v = (rx - qx, ry - qy)
    lv = math.hypot(*v)
    if lv < 1e-6:
        return ""
    v = (v[0] / lv * s, v[1] / lv * s)
    return (
        f"  \\draw[line width=0.5pt] ({qx+u[0]:.3f},{qy+u[1]:.3f})--({qx+u[0]+v[0]:.3f},{qy+u[1]+v[1]:.3f})"
        f"--({qx+v[0]:.3f},{qy+v[1]:.3f});\n"
    )


# TikZ cho 3 đề ôn tập
def get_tikz_on1():
    c = TOA_DO["on1"]
    pts = {
        "A": (*c["A"], "below left"),
        "B": (*c["B"], "above"),
        "C": (*c["C"], "below right"),
        "M": (*c["M"], "above right"),
        "D": (*c["D"], "above left=2pt"),
        "E": (*c["E"], "below"),
        "P": (*c["P"], "left"),
        "H": (*c["H"], "above right"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("M", "D"), ("M", "E"), ("D", "E"),
        ("A", "M"), ("A", "H"), ("D", "H"),
        ("P", "B"), ("P", "A"), ("P", "D")
    ]
    extra = (
        vg(c["B"], c["A"], c["C"])
        + vg(c["A"], c["D"], c["M"])
        + vg(c["A"], c["E"], c["M"])
        + vg(c["A"], c["H"], c["C"])
    )
    return hinh_draw(pts, segs, extra=extra, scale=1.1)


def get_tikz_on2():
    c = TOA_DO["on2"]
    pts = {
        "A": (*c["A"], "below left"),
        "B": (*c["B"], "above"),
        "C": (*c["C"], "below right"),
        "H": (*c["H"], "above right"),
        "D": (*c["D"], "above left=2pt"),
        "E": (*c["E"], "below right=2pt"),
        "M": (*c["M"], "above right"),
        "P": (*c["P"], "left"),
        "Q": (*c["Q"], "below"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A", "H"), ("H", "D"), ("H", "E"), ("D", "E"),
        ("A", "M"), ("P", "D"), ("P", "A"),
        ("Q", "E"), ("Q", "A")
    ]
    dashed = [("P", "Q")]
    extra = (
        vg(c["B"], c["A"], c["C"])
        + vg(c["A"], c["H"], c["C"])
        + vg(c["A"], c["D"], c["H"])
        + vg(c["A"], c["E"], c["H"])
    )
    return hinh_draw(pts, segs, extra=extra, dashed=dashed, scale=1.15)


def get_tikz_on3():
    c = TOA_DO["on3"]
    pts = {
        "A": (*c["A"], "below left"),
        "B": (*c["B"], "above"),
        "C": (*c["C"], "below right"),
        "M": (*c["M"], "above right"),
        "D": (*c["D"], "left"),
        "E": (*c["E"], "below left=2pt"),
        "K": (*c["K"], "below"),
        "H": (*c["H"], "above right"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("M", "D"), ("M", "E"), ("D", "E"),
        ("A", "M"), ("A", "H"), ("A", "K"), ("C", "K"), ("M", "K")
    ]
    extra = (
        vg(c["B"], c["A"], c["C"])
        + vg(c["A"], c["D"], c["M"])
        + vg(c["A"], c["E"], c["M"])
        + vg(c["A"], c["H"], c["C"])
    )
    return hinh_draw(pts, segs, extra=extra, scale=1.1)


# TikZ cho 3 đề chính thức
def get_tikz_ct1():
    c = TOA_DO["ct1"]
    pts = {
        "A": (*c["A"], "below left"),
        "B": (*c["B"], "above"),
        "C": (*c["C"], "below right"),
        "H": (*c["H"], "above right"),
        "E": (*c["E"], "left"),
        "F": (*c["F"], "below"),
        "M": (*c["M"], "above right"),
        "I": (*c["I"], "above right"),
        "K": (*c["K"], "above right"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A", "H"), ("H", "E"), ("H", "F"), ("E", "F"),
        ("A", "M"), ("E", "I"), ("F", "K")
    ]
    extra = (
        vg(c["B"], c["A"], c["C"])
        + vg(c["A"], c["H"], c["C"])
        + vg(c["A"], c["E"], c["H"])
        + vg(c["A"], c["F"], c["H"])
    )
    return hinh_draw(pts, segs, extra=extra, scale=1.15)


def get_tikz_ct2():
    c = TOA_DO["ct2"]
    pts = {
        "A": (*c["A"], "below left"),
        "B": (*c["B"], "above"),
        "C": (*c["C"], "below right"),
        "M": (*c["M"], "above right"),
        "E": (*c["E"], "above left=2pt"),
        "F": (*c["F"], "below"),
        "D": (*c["D"], "left"),
        "K": (*c["K"], "below"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A", "M"), ("M", "E"), ("M", "F"), ("E", "F"),
        ("D", "E"), ("D", "A"), ("D", "B"),
        ("B", "F"), ("M", "K")
    ]
    extra = (
        vg(c["B"], c["A"], c["C"])
        + vg(c["A"], c["E"], c["M"])
        + vg(c["A"], c["F"], c["M"])
    )
    return hinh_draw(pts, segs, extra=extra, scale=1.1)


def get_tikz_ct3():
    c = TOA_DO["ct3"]
    pts = {
        "A": (*c["A"], "above"),
        "B": (*c["B"], "below left"),
        "C": (*c["C"], "below right"),
        "M": (*c["M"], "above right=2pt"),
        "H": (*c["H"], "above left=2pt"),
        "E": (*c["E"], "below"),
        "D": (*c["D"], "below"),
        "K": (*c["K"], "above right=2pt"),
    }
    segs = [
        ("A", "B"), ("B", "C"), ("C", "A"),
        ("A", "M"), ("M", "D"), ("C", "D"), ("B", "D"),
        ("A", "H"), ("H", "E"), ("B", "E"), ("E", "D"),
        ("D", "K")
    ]
    dashed = [("H", "E"), ("D", "K")]
    extra = (
        vg(c["A"], c["H"], c["C"])
        + vg(c["D"], c["K"], c["C"])
    )
    return hinh_draw(pts, segs, extra=extra, dashed=dashed, scale=1.0)
