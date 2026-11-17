#!/usr/bin/env python3
"""Hình (TikZ, toạ độ TÍNH) cho phiếu G ch.IX 9C — buổi 9.6 "Góc nội tiếp cùng chắn một cung".

Mỗi hình dựng bằng scripts/tikz_geo.Fig (nhãn tự đặt, tự kiểm nét đè) và tự kiểm KẾT LUẬN
của đề bằng số (hai góc cần chứng minh bằng nhau thì đo ra phải bằng nhau, ±0,01°).

    python3 scripts/gemini/hinh_phieu_g_ch9_9c.py      # dựng + kiểm, in bảng góc
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from scripts.tikz_geo import Fig, add, dist, foot, mul, norm, polar, sub  # noqa: E402

R = 1.5


def goc(a, v, b):
    """Số đo góc a-v-b (độ)."""
    u, w = sub(a, v), sub(b, v)
    c = (u[0] * w[0] + u[1] * w[1]) / (math.hypot(*u) * math.hypot(*w))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def giao_dt(p1, p2, p3, p4):
    """Giao điểm hai đường thẳng p1p2, p3p4."""
    d1, d2 = sub(p2, p1), sub(p4, p3)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
    return add(p1, mul(d1, t))


def giao_tron(p, q, c, r):
    """Giao điểm thứ hai (khác p) của đường thẳng pq với đường tròn (c, r); p nằm trên đường tròn."""
    d = sub(q, p)
    f = sub(p, c)
    a = d[0] ** 2 + d[1] ** 2
    b = 2 * (f[0] * d[0] + f[1] * d[1])
    t = -b / a
    return add(p, mul(d, t))


def khung(tz_gv_pts, tikz):
    """Chèn \\path rectangle phủ khung của hình đầy đủ vào hình nền (giữ chỗ cho HS vẽ tiếp)."""
    xs = [p[0] for p in tz_gv_pts]
    ys = [p[1] for p in tz_gv_pts]
    rect = f"  \\path ({min(xs) - 0.35:.4f},{min(ys) - 0.35:.4f}) rectangle ({max(xs) + 0.35:.4f},{max(ys) + 0.35:.4f});"
    return tikz.replace("\\end{tikzpicture}", rect + "\n\\end{tikzpicture}")


KIEM: list[tuple[str, float, float]] = []


def bang(ten, g1, g2):
    KIEM.append((ten, g1, g2))
    assert abs(g1 - g2) < 0.01, f"{ten}: {g1:.3f} ≠ {g2:.3f}"


# ─────────────────────────── lý thuyết ───────────────────────────
def lt_goc_noi_tiep():
    f = Fig()
    O = (0, 0)
    M, N, B, C = polar(150, R), polar(35, R), polar(-120, R), polar(-40, R)
    f.circle(O, R)
    f.pt("O", O)
    for n, p in (("M", M), ("N", N), ("P", B), ("Q", C)):
        f.pt(n, p)
    f.seg("M", "P"); f.seg("M", "Q"); f.seg("N", "P"); f.seg("N", "Q")
    f.angle(M, B, C, r=0.35)
    f.angle(N, B, C, r=0.35)
    f.arc(O, R, -120, -40, style="brand, line width=1.6pt")
    bang("LT1 MPQ=NPQ", goc(B, M, C), goc(B, N, C))
    return f.tikz()


def lt_bon_diem():
    f = Fig()
    A, B = (0, 0), (3.2, 0)
    I = (1.6, 0)
    C = add(I, polar(118, 1.6))
    D = add(I, polar(62, 1.6))
    f.circle(I, 1.6, style="brand, dashed")
    for n, p in (("A", A), ("B", B), ("C", C), ("D", D)):
        f.pt(n, p)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("C", "B"); f.seg("A", "D"); f.seg("D", "B")
    f.right("C", "A", "B"); f.right("D", "A", "B")
    return f.tikz()


def lt_dang1():
    """Bốn điểm A, B, D, E (hai góc vuông nhìn AB) ⇒ góc EAD = góc EBD (cùng chắn ED)."""
    f = Fig()
    A, B = (0, 0), (3.2, 0)
    I = (1.6, 0)
    E = add(I, polar(128, 1.6))
    D = add(I, polar(50, 1.6))
    f.circle(I, 1.6, style="brand, dashed")
    for n, p in (("A", A), ("B", B), ("E", E), ("D", D)):
        f.pt(n, p)
    f.seg("A", "B"); f.seg("A", "D"); f.seg("B", "E"); f.seg("E", "D")
    f.seg("A", "E"); f.seg("B", "D")
    f.right("E", "A", "B"); f.right("D", "A", "B")
    f.angle(A, D, E, r=0.45); f.angle(B, D, E, r=0.45)
    bang("LT3 EAD=EBD", goc(E, A, D), goc(E, B, D))
    return f.tikz()


def lt_dang2():
    """Bắc cầu: góc ABD = góc ACD (đường tròn đường kính BC), góc ACD = góc MED (đường tròn đường kính MC)."""
    return vd2_nguyen_truong_to()[1]


# ─────────────────────────── Khám phá: SGK Ví dụ 2 tr.70 ───────────────────────────
def kham_pha():
    f = Fig()
    O = (0, 0)
    A, B, C, D = polar(160, R), polar(60, R), polar(-60, R), polar(-150, R)
    f.circle(O, R)
    f.pt("O", O)
    for n, p in (("A", A), ("B", B), ("C", C), ("D", D)):
        f.pt(n, p)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("D", "B"); f.seg("D", "C")
    f.seg("O", "B", style="ink, dashed"); f.seg("O", "C", style="ink, dashed")
    f.angle(A, C, B, r=0.42)
    f.text(add(A, polar(-12, 0.75)), "$60^\\circ$")
    bang("KP BDC=BAC", goc(B, D, C), goc(B, A, C))
    assert abs(goc(B, A, C) - 60) < 1e-6
    return f.tikz()


# ─────────────────────────── Bài 1: Nhật Tân (TN) ───────────────────────────
def bai1_nhat_tan():
    f = Fig()
    O = (0, 0)
    A, B, C = polar(110, R), polar(205, R), polar(-25, R)
    D = foot(A, B, C)
    E = foot(B, A, C)
    H = giao_dt(A, D, B, E)
    f.circle(O, R)
    f.pt("O", O)
    for n, p in (("A", A), ("B", B), ("C", C), ("D", D), ("E", E), ("H", H)):
        f.pt(n, p)
    f.poly("A", "B", "C")
    f.seg("A", "D"); f.seg("B", "E"); f.seg("D", "E", style="ink, dashed")
    f.right("D", "A", "C"); f.right("E", "B", "C")
    bang("B1 BED=BAD", goc(B, E, D), goc(B, A, D))
    return f.tikz(), {"BED": goc(B, E, D), "BAE": goc(B, A, E), "ABE": goc(A, B, E), "ADE": goc(A, D, E),
                      "BCA": goc(B, C, A), "BHD": goc(B, H, D)}


# ─────────────────────────── Ví dụ 1: Mỹ Đình 2 ───────────────────────────
def vd1_my_dinh_2():
    A, B, C = (0, 0), (0, 2.4), (3.2, 0)
    O = (1.6, 0)
    D = foot(A, B, C)
    E = foot(A, O, B)
    assert abs(dist(O, D) - 1.6) < 1e-9
    bang("VD1 EAD=EBD", goc(E, A, D), goc(E, B, D))

    def ve(full):
        f = Fig()
        f.pt("A", A); f.pt("B", B); f.pt("C", C)
        f.poly("A", "B", "C")
        f.right("A", "B", "C")
        if full:
            f.circle(O, 1.6)
            f.pt("O", O); f.pt("D", D); f.pt("E", E)
            f.seg("O", "B"); f.seg("A", "E"); f.seg("A", "D")
            f.right("E", "A", "O"); f.right("D", "A", "C")
        return f
    gv = ve(True)
    pts = list(gv.P.values()) + [(O[0] - 1.6, -1.6), (O[0] + 1.6, 1.6)]
    return khung(pts, ve(False).tikz()), gv.tikz()


# ─────────────────────────── Bài 2: Cầu Giấy ───────────────────────────
def bai2_cau_giay():
    B, C, A = (0, 0), (4.0, 0), (1.4, 2.6)
    D = foot(A, B, C)
    N = foot(D, A, B)
    T = foot(D, A, C)
    bang("B2 DNT=DAT", goc(D, N, T), goc(D, A, T))

    def ve(full):
        f = Fig()
        for n, p in (("A", A), ("B", B), ("C", C), ("D", D)):
            f.pt(n, p)
        f.poly("A", "B", "C"); f.seg("A", "D"); f.right("D", "A", "C")
        if full:
            f.pt("N", N); f.pt("T", T)
            f.seg("D", "N"); f.seg("D", "T"); f.seg("N", "T")
            f.right("N", "D", "B"); f.right("T", "D", "C")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()), ve(False).tikz()), gv.tikz()


# ─────────────────────────── Ví dụ 2: Nguyễn Trường Tộ ───────────────────────────
def vd2_nguyen_truong_to():
    A, B, C = (0, 0), (3.4, 0), (0, 2.4)
    M = (0, 0.7)
    I = (0, (0.7 + 2.4) / 2)
    r = (2.4 - 0.7) / 2
    E = foot(M, B, C)
    D = foot(C, B, M)
    assert abs(dist(I, E) - r) < 1e-9 and abs(dist(I, D) - r) < 1e-9
    assert dist(B, D) > dist(B, M)      # D nằm trên tia BM, sau M
    bang("VD2 ABD=ACD", goc(A, B, D), goc(A, C, D))
    bang("VD2 ACD=MED", goc(A, C, D), goc(M, E, D))
    bang("VD2 ABD=MED", goc(A, B, D), goc(M, E, D))

    def ve(full):
        f = Fig()
        for n, p in (("A", A), ("B", B), ("C", C)):
            f.pt(n, p)
        f.poly("A", "B", "C"); f.right("A", "B", "C")
        if full:
            f.circle(I, r)
            f.pt("M", M); f.pt("E", E); f.pt("D", D)
            f.seg("B", "D"); f.seg("C", "D"); f.seg("A", "D")
            f.seg("M", "E"); f.seg("E", "D")
            f.right("D", "M", "C")
        return f
    gv = ve(True)
    pts = list(gv.P.values()) + [(I[0] - r, I[1]), (I[0], I[1] + r)]
    return khung(pts, ve(False).tikz()), gv.tikz()


# ─────────────────────────── Bài 3: Cầu Diễn ───────────────────────────
def bai3_cau_dien():
    O = (0, 0)
    A, B, C, D = (-R, 0), (R, 0), (0, R), (0, -R)
    M = add(C, mul(sub(C, A), 0.6))
    H = foot(C, B, M)
    bang("B3 BHO=BCO", goc(B, H, O), goc(B, C, O))
    bang("B3 CHO=CBO", goc(C, H, O), goc(C, B, O))
    bang("B3 BHO=CHO", goc(B, H, O), goc(C, H, O))
    assert abs(goc(B, H, O) + goc(O, H, C) - goc(B, H, C)) < 1e-6   # tia HO nằm giữa

    def ve(full):
        f = Fig()
        f.circle(O, R)
        for n, p in (("O", O), ("A", A), ("B", B), ("C", C), ("D", D)):
            f.pt(n, p)
        f.seg("A", "B"); f.seg("C", "D"); f.right("O", "B", "C")
        if full:
            f.pt("M", M); f.pt("H", H)
            f.seg("A", "M"); f.seg("B", "M"); f.seg("C", "H"); f.seg("C", "B"); f.seg("O", "H")
            f.right("H", "C", "B")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), gv.tikz()


# ─────────────────────────── Bài 4 (đích): Sơn Tây ───────────────────────────
def son_tay_fig(full=True, cung=True):
    O = (0, 0)
    A, B, C = polar(75, R), polar(205, R), polar(-25, R)
    M = mul(add(B, C), 0.5)
    E = foot(M, A, B)
    F = foot(M, A, C)
    K = giao_tron(A, M, O, R)
    f = Fig()
    f.circle(O, R)
    f.pt("O", O)
    for n, p in (("A", A), ("B", B), ("C", C)):
        f.pt(n, p)
    f.poly("A", "B", "C")
    if full:
        f.pt("M", M); f.pt("E", E); f.pt("F", F); f.pt("K", K)
        f.seg("M", "E"); f.seg("M", "F"); f.seg("E", "F"); f.seg("A", "K"); f.seg("B", "K")
        f.right("E", "M", "A"); f.right("F", "M", "C")
    return f, dict(O=O, A=A, B=B, C=C, M=M, E=E, F=F, K=K)


def bai4_son_tay():
    gvf, P = son_tay_fig(True)
    A, B, C, M, E, F, K = (P[k] for k in "ABCMEFK")
    assert dist(A, B) > dist(A, C)
    bang("B4 KBC=KAC", goc(K, B, C), goc(K, A, C))
    bang("B4 MAF=MEF", goc(M, A, F), goc(M, E, F))
    bang("B4 KBC=MEF", goc(K, B, C), goc(M, E, F))
    nen, _ = son_tay_fig(False)
    pts = list(gvf.P.values()) + [(-R, -R), (R, R)]
    return khung(pts, nen.tikz()), gvf.tikz()


# ─────────────────────────── BTVN 1: Đông Anh (TN) ───────────────────────────
def btvn1_dong_anh():
    f = Fig()
    O = (0, 0)
    A, B, C = polar(120, R), polar(220, R), polar(-20, R)
    K = polar(40, R)
    Q = giao_dt(B, K, A, C)
    f.circle(O, R)
    for n, p in (("O", O), ("A", A), ("B", B), ("C", C), ("K", K), ("Q", Q)):
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("B", "K"); f.seg("K", "C")
    bang("BTVN1 BKC=BAC", goc(B, K, C), goc(B, A, C))
    return f.tikz(), {"BAC": goc(B, A, C), "KBC": goc(K, B, C), "BQC": goc(B, Q, C), "ACK": goc(A, C, K),
                      "BCK": goc(B, C, K)}


# ─────────────────────────── BTVN 2: Lômônôxốp (TN) ───────────────────────────
def btvn2_lomonoxop():
    f = Fig()
    O = (0, 0)
    A, B, C = polar(100, R), polar(210, R), polar(-30, R)
    E = foot(B, A, C)
    F = foot(C, A, B)
    H = giao_dt(B, E, C, F)
    f.circle(O, R)
    for n, p in (("A", A), ("B", B), ("C", C), ("E", E), ("F", F), ("H", H)):
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("B", "E"); f.seg("C", "F"); f.seg("E", "F"); f.seg("A", "H", style="ink, dashed")
    f.right("E", "B", "C"); f.right("F", "C", "B")
    assert dist(A, B) < dist(A, C)
    bang("BTVN2 AEF=AHF", goc(A, E, F), goc(A, H, F))
    return f.tikz(), {"AEF": goc(A, E, F), "AHF": goc(A, H, F), "AFE": goc(A, F, E), "AHE": goc(A, H, E),
                      "BHF": goc(B, H, F), "ABE": goc(A, B, E), "ACF": goc(A, C, F)}


# ─────────────────────────── BTVN 3: Hà Đông ───────────────────────────
def btvn3_ha_dong():
    O = (0, 0)
    A, B = (-R, 0), (R, 0)
    C = polar(125, R)
    D = (-0.7, 0)
    u = norm(sub(C, D))
    v = (-u[1], u[0])                         # hướng đường thẳng qua C, ⊥ CD
    E = giao_dt(C, add(C, v), A, add(A, (0, 1)))
    F = giao_dt(C, add(C, v), B, add(B, (0, 1)))
    assert dist(C, A) < dist(C, B)
    bang("BTVN3 CFD=CBD", goc(C, F, D), goc(C, B, D))
    bang("BTVN3 CBD=CBA", goc(C, B, D), goc(C, B, A))

    def ve(full):
        f = Fig()
        f.arc(O, R, 0, 180)
        for n, p in (("O", O), ("A", A), ("B", B)):
            f.pt(n, p)
        f.seg("A", "B")
        if full:
            f.pt("C", C); f.pt("D", D); f.pt("E", E); f.pt("F", F)
            f.seg("A", "E"); f.seg("B", "F"); f.seg("E", "F"); f.seg("C", "D"); f.seg("C", "B"); f.seg("D", "F"); f.seg("D", "E")
            f.right("C", "D", "F"); f.right("A", "B", "E"); f.right("B", "F", "A")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()) + [(-R, R)], ve(False).tikz()), gv.tikz()


# ─────────────────────────── BTVN 4: Ngọc Thụy ───────────────────────────
def btvn4_ngoc_thuy():
    O = (0, 0)
    A, B, C = polar(95, R), polar(215, R), polar(-35, R)
    H = foot(A, B, C)
    M = foot(H, A, B)
    N = foot(H, A, C)
    bang("BTVN4 ANM=AHM", goc(A, N, M), goc(A, H, M))
    bang("BTVN4 AHM=ABC", goc(A, H, M), goc(A, B, C))

    def ve(full):
        f = Fig()
        f.circle(O, R)
        for n, p in (("O", O), ("A", A), ("B", B), ("C", C)):
            f.pt(n, p)
        f.poly("A", "B", "C")
        if full:
            f.pt("H", H); f.pt("M", M); f.pt("N", N)
            f.seg("A", "H"); f.seg("H", "M"); f.seg("H", "N"); f.seg("M", "N")
            f.right("H", "A", "C"); f.right("M", "H", "A"); f.right("N", "H", "C")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), gv.tikz()


def tat_ca():
    """{khoá: figure dict} — khoá = nhãn khối trong phiếu."""
    out = {}
    out["lt1"] = {"tikz": lt_goc_noi_tiep(), "caption": "$\\widehat{PMQ}$, $\\widehat{PNQ}$ cùng chắn cung $PQ$", "pos": "right"}
    out["lt2"] = {"tikz": lt_bon_diem(), "caption": "$C$, $D$ thuộc đường tròn đường kính $AB$", "pos": "right"}
    out["lt3"] = {"tikz": lt_dang1(), "caption": "$\\widehat{EAD}$, $\\widehat{EBD}$ cùng chắn cung $ED$", "pos": "right"}
    out["lt4"] = {"tikz": lt_dang2(), "caption": "Bắc cầu qua $\\widehat{ACD}$", "pos": "right"}
    out["Hình 1"] = {"tikz": kham_pha(), "caption": "Hình 1", "pos": "right"}
    tz, g = bai1_nhat_tan()
    out["Bài 1."] = {"tikz": tz, "caption": "Hình 2", "pos": "right", "_goc": g}
    n, gv = vd1_my_dinh_2()
    out["Ví dụ 1."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 3", "pos": "right"}
    n, gv = bai2_cau_giay()
    out["Bài 2."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 4", "pos": "right"}
    n, gv = vd2_nguyen_truong_to()
    out["Ví dụ 2."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 5", "pos": "right"}
    n, gv = bai3_cau_dien()
    out["Bài 3."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 6", "pos": "right"}
    n, gv = bai4_son_tay()
    out["Bài 4."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 7", "pos": "right"}
    tz, g = btvn1_dong_anh()
    out["BTVN 1."] = {"tikz": tz, "caption": "Hình 8", "pos": "right", "_goc": g}
    tz, g = btvn2_lomonoxop()
    out["BTVN 2."] = {"tikz": tz, "caption": "Hình 9", "pos": "right", "_goc": g}
    n, gv = btvn3_ha_dong()
    out["BTVN 3."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 10", "pos": "right"}
    n, gv = btvn4_ngoc_thuy()
    out["BTVN 4."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 11", "pos": "right"}
    return out


if __name__ == "__main__":
    h = tat_ca()
    for t, a, b in KIEM:
        print(f"  ✓ {t}: {a:.3f}° = {b:.3f}°")
    for k in ("Bài 1.", "BTVN 1.", "BTVN 2."):
        print(k, {n: round(v, 2) for n, v in h[k]["_goc"].items()})
    print("Dựng", len(h), "hình — sạch nhãn đè.")
