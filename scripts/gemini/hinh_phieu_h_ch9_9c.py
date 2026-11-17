#!/usr/bin/env python3
"""Hình (TikZ, toạ độ TÍNH) cho phiếu H ch.IX 9C — buổi 9.7
"Chứng minh hệ thức tích bằng tam giác đồng dạng dựa vào góc nội tiếp".

Mỗi hình dựng bằng scripts/tikz_geo.Fig và tự kiểm KẾT LUẬN của đề bằng số:
góc bằng nhau (±0,01°) và đẳng thức tích (sai số tương đối < 1e-9).
Phương án trắc nghiệm: kiểm phương án đúng ĐÚNG, ba phương án nhiễu SAI.

    python3 scripts/gemini/hinh_phieu_h_ch9_9c.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scripts.tikz_geo import Fig, add, dist, foot, mul, polar, sub  # noqa: E402
from hinh_phieu_g_ch9_9c import giao_dt, giao_tron, goc, khung, lt_goc_noi_tiep  # noqa: E402

R = 1.5
KIEM: list[str] = []


def bang(ten, g1, g2):
    assert abs(g1 - g2) < 0.01, f"{ten}: {g1:.4f} ≠ {g2:.4f}"
    KIEM.append(f"{ten}: {g1:.3f}° = {g2:.3f}°")


def tich(ten, a, b):
    assert abs(a - b) / max(a, b) < 1e-9, f"{ten}: {a:.6f} ≠ {b:.6f}"
    KIEM.append(f"{ten}: {a:.4f} = {b:.4f}")


def dong_dang(P, t1, t2):
    """△t1 ∽ △t2 theo đúng thứ tự đỉnh (so ba góc)."""
    a = [goc(P[t1[1]], P[t1[0]], P[t1[2]]), goc(P[t1[0]], P[t1[1]], P[t1[2]]), goc(P[t1[0]], P[t1[2]], P[t1[1]])]
    b = [goc(P[t2[1]], P[t2[0]], P[t2[2]]), goc(P[t2[0]], P[t2[1]], P[t2[2]]), goc(P[t2[0]], P[t2[2]], P[t2[1]])]
    return all(abs(x - y) < 0.01 for x, y in zip(a, b))


def giua(p, a, b):
    """p nằm giữa a và b (trên đoạn ab)."""
    return abs(dist(a, p) + dist(p, b) - dist(a, b)) < 1e-9


# ─────────────────────────── Khám phá: SGK Luyện tập tr.70 (H.9.6) ───────────────────────────
def kham_pha():
    A, B, C, D = polar(165, R), polar(15, R), polar(80, R), polar(228, R)
    X = giao_dt(A, B, C, D)
    P = dict(A=A, B=B, C=C, D=D, X=X)
    assert giua(X, A, B) and giua(X, C, D)
    bang("KP CAX=XDB", goc(C, A, X), goc(X, D, B))
    assert dong_dang(P, "AXC", "DXB")
    tich("KP XA.XB=XC.XD", dist(X, A) * dist(X, B), dist(X, C) * dist(X, D))
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0))
    for n in "ABCDX":
        f.pt(n, P[n])
    f.seg("A", "B"); f.seg("C", "D"); f.seg("A", "C"); f.seg("D", "B")
    return f.tikz()


# ─────────────────────────── Bài 1: Ngọc Thụy (TN) ───────────────────────────
def bai1_ngoc_thuy():
    A, B, C = polar(100, R), polar(208, R), polar(-32, R)
    H = foot(A, B, C)
    M = foot(H, A, B)
    N = foot(H, A, C)
    P = dict(A=A, B=B, C=C, H=H, M=M, N=N)
    tich("B1 AH²=AM.AB", dist(A, H) ** 2, dist(A, M) * dist(A, B))
    assert dong_dang(P, "AMH", "AHB")                       # A đúng
    assert not dong_dang(P, "AMH", "ANH")                   # nhiễu
    assert not dong_dang(P, "AHB", "AHC")
    assert not dong_dang(P, "MHB", "NHC")
    f = Fig()
    f.circle((0, 0), R)
    f.pt("O", (0, 0))
    for n in "ABCHMN":
        f.pt(n, P[n])
    f.poly("A", "B", "C"); f.seg("A", "H"); f.seg("H", "M"); f.seg("H", "N")
    f.right("H", "A", "C"); f.right("M", "H", "A"); f.right("N", "H", "C")
    return f.tikz()


# ─────────────────────────── Ví dụ 1: Ban Mai GK2 2024–2025 ───────────────────────────
def vd1_ban_mai():
    O = (0, 0)
    yN = -0.3
    xa = math.sqrt(R * R - yN * yN)
    A, B, N = (-xa, yN), (xa, yN), (0, yN)
    I, K = (0, R), (0, -R)
    M = polar(168, R)
    D = giao_dt(M, K, A, B)
    C = giao_dt(I, M, A, B)
    P = dict(O=O, A=A, B=B, N=N, I=I, K=K, M=M, D=D, C=C)
    assert M[1] > yN                                         # M thuộc cung lớn AB
    assert giua(D, A, B)
    assert dist(I, C) > dist(I, M)                           # C trên tia IM, sau M
    bang("VD1 IMK=90", goc(I, M, K), 90)
    bang("VD1 INC=90", goc(I, N, C), 90)
    assert dong_dang(P, "IMK", "INC")
    tich("VD1 IM.IC=IN.IK", dist(I, M) * dist(I, C), dist(I, N) * dist(I, K))

    def ve(full):
        f = Fig()
        f.circle(O, R)
        f.pt("O", O); f.pt("A", A); f.pt("B", B)
        f.seg("A", "B")
        if full:
            for n in "IKNMDC":
                f.pt(n, P[n])
            f.seg("I", "K"); f.seg("M", "K"); f.seg("I", "C"); f.seg("C", "A"); f.seg("N", "C", style="ink")
            f.right("N", "B", "I"); f.right("M", "I", "K")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()), ve(False).tikz()), gv.tikz()


# ─────────────────────────── Bài 2: Gia Lâm CK2 2024–2025 ───────────────────────────
def bai2_gia_lam():
    B, C = (0, 0), (4.0, 0)
    O = (2.0, 0)
    A = (1.45, 3.1)
    E = foot(C, A, B)
    D = foot(B, A, C)
    H = giao_dt(B, D, C, E)
    P = dict(A=A, B=B, C=C, O=O, E=E, D=D, H=H)
    assert abs(dist(O, E) - 2) < 1e-9 and abs(dist(O, D) - 2) < 1e-9
    assert giua(E, A, B) and giua(D, A, C) and dist(O, A) > 2
    assert dong_dang(P, "ABD", "ACE")
    tich("B2 AB.AE=AC.AD", dist(A, B) * dist(A, E), dist(A, C) * dist(A, D))
    I = mul(add(A, H), 0.5)
    assert abs(dist(I, E) - dist(I, A)) < 1e-9 and abs(dist(I, D) - dist(I, A)) < 1e-9

    def ve(full):
        f = Fig()
        f.circle(O, 2.0)
        for n in "ABCOED":
            f.pt(n, P[n])
        f.poly("A", "B", "C")
        if full:
            f.pt("H", H)
            f.seg("B", "D"); f.seg("C", "E"); f.seg("A", "H", style="ink, dashed")
            f.right("E", "A", "C"); f.right("D", "A", "B")
        return f
    gv = ve(True)
    return ve(False).tikz(), gv.tikz()


# ─────────────────────────── Ví dụ 2: Cầu Giấy CK2 2024–2025 (phần tích ý b) ───────────────────────────
def vd2_cau_giay():
    B, C, A = (0, 0), (4.3, 0), (1.3, 2.9)
    D = foot(A, B, C)
    N = foot(D, A, B)
    T = foot(D, A, C)
    E = giao_dt(D, add(D, sub(B, A)), N, T)
    P = dict(A=A, B=B, C=C, D=D, N=N, T=T, E=E)
    assert dist(A, B) < dist(A, C)
    assert dist(N, E) > 0 and abs(goc(T, N, E)) < 0.01      # E thuộc tia NT
    bang("VD2 DNT=DAT", goc(D, N, T), goc(D, A, T))
    bang("VD2 DNE=DAC", goc(D, N, E), goc(D, A, C))
    bang("VD2 NDE=90", goc(N, D, E), 90)
    assert dong_dang(P, "DNE", "DAC")
    tich("VD2 DN.DC=DE.DA", dist(D, N) * dist(D, C), dist(D, E) * dist(D, A))

    def ve(full):
        f = Fig()
        for n in "ABCD":
            f.pt(n, P[n])
        f.poly("A", "B", "C"); f.seg("A", "D"); f.right("D", "A", "C")
        if full:
            f.pt("N", N); f.pt("T", T); f.pt("E", E)
            f.seg("D", "N"); f.seg("D", "T"); f.seg("N", "E" if dist(N, E) > dist(N, T) else "T"); f.seg("D", "E")
            f.right("N", "D", "B"); f.right("T", "D", "C")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()), ve(False).tikz()), gv.tikz(), giua(E, N, T)


# ─────────────────────────── Bài 3: Thăng Long CK2 2025–2026 ───────────────────────────
def bai3_thang_long():
    O = (0, 0)
    A, B, C = polar(103, R), polar(207, R), polar(-27, R)
    K = mul(A, -1)
    D = foot(A, B, C)
    E = foot(B, A, C)
    P = dict(O=O, A=A, B=B, C=C, K=K, D=D, E=E)
    assert dist(A, B) < dist(A, C)
    for v in ("ABC", "BCA", "CAB"):
        assert goc(P[v[0]], P[v[1]], P[v[2]]) < 90
    bang("B3 ACK=90", goc(A, C, K), 90)
    bang("B3 ABD=AKC", goc(A, B, D), goc(A, K, C))
    assert dong_dang(P, "ABD", "AKC")
    tich("B3 AB.AC=AK.AD", dist(A, B) * dist(A, C), dist(A, K) * dist(A, D))

    def ve(full):
        f = Fig()
        f.circle(O, R)
        f.pt("O", O); f.pt("B", B); f.pt("C", C)
        f.seg("B", "C")
        if full:
            for n in "AKDE":
                f.pt(n, P[n])
            f.seg("A", "B"); f.seg("A", "C"); f.seg("A", "D"); f.seg("B", "E"); f.seg("A", "K"); f.seg("C", "K")
            f.right("D", "A", "C"); f.right("E", "B", "C"); f.right("C", "A", "K")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), gv.tikz()


# ─────────────────────────── Bài 4 (đích): Thọ Lộc thi thử lần 5 2025–2026 ───────────────────────────
def bai4_tho_loc():
    O = (0, 0)
    A, B, C = polar(98, R), polar(205, R), polar(-25, R)
    K = mul(A, -1)
    E = foot(C, A, K)
    M = mul(add(B, C), 0.5)
    D = foot(A, B, C)
    P = dict(O=O, A=A, B=B, C=C, K=K, E=E, M=M, D=D)
    assert dist(A, B) < dist(A, C)
    bang("B4 OEC=90", goc(O, E, C), 90)
    bang("B4 OMC=90", goc(O, M, C), 90)
    bang("B4 ABD=AKC", goc(A, B, D), goc(A, K, C))
    assert dong_dang(P, "ABD", "AKC")
    tich("B4 AD.AK=AB.AC", dist(A, D) * dist(A, K), dist(A, B) * dist(A, C))
    assert dist(E, O) > 0.15 and dist(M, D) > 0.15

    def ve(full):
        f = Fig()
        f.circle(O, R)
        f.pt("O", O); f.pt("B", B); f.pt("C", C)
        f.seg("B", "C")
        if full:
            for n in "AKEMD":
                f.pt(n, P[n])
            f.seg("A", "B"); f.seg("A", "C"); f.seg("A", "K"); f.seg("C", "E"); f.seg("O", "M"); f.seg("A", "D")
            f.seg("C", "K")
            f.right("E", "C", "O"); f.right("M", "O", "C"); f.right("D", "A", "C")
        return f
    gv = ve(True)
    return khung(list(gv.P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), gv.tikz()


# ─────────────────────────── BTVN 1: Lômônôxốp CK2 2024–2025 ───────────────────────────
def btvn1_lomonoxop():
    O = (0, 0)
    A, B, C = polar(97, R), polar(212, R), polar(-28, R)
    E = foot(B, A, C)
    F = foot(C, A, B)
    H = giao_dt(B, E, C, F)
    P = dict(A=A, B=B, C=C, E=E, F=F, H=H)
    assert dist(A, B) < dist(A, C)
    assert dong_dang(P, "AEB", "AFC")
    tich("BTVN1 AE.AC=AF.AB", dist(A, E) * dist(A, C), dist(A, F) * dist(A, B))

    def ve(full):
        f = Fig()
        f.circle(O, R)
        f.pt("O", O)
        for n in "ABC":
            f.pt(n, P[n])
        f.poly("A", "B", "C")
        if full:
            f.pt("E", E); f.pt("F", F); f.pt("H", H)
            f.seg("B", "E"); f.seg("C", "F")
            f.right("E", "B", "C"); f.right("F", "C", "B")
        return f
    return khung(list(ve(True).P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), ve(True).tikz()


# ─────────────────────────── BTVN 2: Mai Dịch GK2 2024–2025 ───────────────────────────
def btvn2_mai_dich():
    O = (0, 0)
    A, B = (-R, 0), (R, 0)
    C, D = polar(118, R), polar(48, R)
    H = foot(C, A, B)
    K = foot(C, A, D)
    I = giao_dt(A, D, C, H)
    P = dict(O=O, A=A, B=B, C=C, D=D, H=H, K=K, I=I)
    assert giua(I, A, D) and giua(I, C, H) and giua(K, A, D)
    bang("BTVN2 ADB=90", goc(A, D, B), 90)
    assert dong_dang(P, "AHI", "ADB")
    tich("BTVN2 AI.AD=AH.AB", dist(A, I) * dist(A, D), dist(A, H) * dist(A, B))
    bang("BTVN2 AHC=AKC", goc(A, H, C), goc(A, K, C))

    def ve(full):
        f = Fig()
        f.arc(O, R, 0, 180)
        f.pt("O", O); f.pt("A", A); f.pt("B", B)
        f.seg("A", "B")
        if full:
            for n in "CDHKI":
                f.pt(n, P[n])
            f.seg("A", "C"); f.seg("A", "D"); f.seg("D", "B"); f.seg("C", "H"); f.seg("C", "K")
            f.right("H", "C", "B"); f.right("K", "C", "D"); f.right("D", "A", "B")
        return f
    return khung(list(ve(True).P.values()) + [(-R, R)], ve(False).tikz()), ve(True).tikz()


# ─────────────────────────── BTVN 3: Hát Môn CK2 2025–2026 ───────────────────────────
def btvn3_hat_mon():
    A, B, C = (0, 0), (3.1, 0), (0, 2.7)
    M = (0, 1.0)
    I = (0, (1.0 + 2.7) / 2)
    r = (2.7 - 1.0) / 2
    N = foot(M, B, C)
    D = foot(C, B, M)
    P = dict(A=A, B=B, C=C, M=M, N=N, D=D)
    assert abs(dist(I, N) - r) < 1e-9 and abs(dist(I, D) - r) < 1e-9
    assert dist(B, D) > dist(B, M) and giua(N, B, C)
    assert dong_dang(P, "BNM", "BDC")
    assert dong_dang(P, "BDN", "BCM")                       # đường thứ hai (cùng chắn cung MN)
    tich("BTVN3 BM.BD=BN.BC", dist(B, M) * dist(B, D), dist(B, N) * dist(B, C))

    def ve(full):
        f = Fig()
        for n in "ABC":
            f.pt(n, P[n])
        f.poly("A", "B", "C"); f.right("A", "B", "C")
        if full:
            f.circle(I, r)
            f.pt("M", M); f.pt("N", N); f.pt("D", D)
            f.seg("B", "D"); f.seg("C", "D"); f.seg("M", "N")
            f.right("D", "M", "C"); f.right("N", "M", "C")
        return f
    pts = list(ve(True).P.values()) + [(I[0] - r, I[1]), (I[0], I[1] + r)]
    return khung(pts, ve(False).tikz()), ve(True).tikz()


# ─────────────────────────── BTVN 4: Sơn Tây thi thử lần 1 2024–2025 (phần tích ý 2) ───────────────────────────
def btvn4_son_tay():
    O = (0, 0)
    A, B, C = polar(70, R), polar(200, R), polar(-20, R)
    M = mul(add(B, C), 0.5)
    E = foot(M, A, B)
    F = foot(M, A, C)
    K = giao_tron(A, M, O, R)
    P = dict(O=O, A=A, B=B, C=C, M=M, E=E, F=F, K=K)
    assert dist(A, B) > dist(A, C)
    assert giua(E, A, B) and giua(F, A, C)
    bang("BTVN4 KBC=MEF", goc(K, B, C), goc(M, E, F))
    bang("BTVN4 BCK=BAK", goc(B, C, K), goc(B, A, K))
    bang("BTVN4 EAM=EFM", goc(E, A, M), goc(E, F, M))
    assert dong_dang(P, "BKC", "EMF")
    tich("BTVN4 BC.ME=EF.BK", dist(B, C) * dist(M, E), dist(E, F) * dist(B, K))

    def ve(full):
        f = Fig()
        f.circle(O, R)
        f.pt("O", O)
        for n in "ABC":
            f.pt(n, P[n])
        f.poly("A", "B", "C")
        if full:
            for n in "MEFK":
                f.pt(n, P[n])
            f.seg("M", "E"); f.seg("M", "F"); f.seg("E", "F"); f.seg("A", "K"); f.seg("B", "K"); f.seg("C", "K")
            f.right("E", "M", "A"); f.right("F", "M", "C")
        return f
    return khung(list(ve(True).P.values()) + [(-R, -R), (R, R)], ve(False).tikz()), ve(True).tikz()


def tat_ca():
    out = {}
    out["lt1"] = {"tikz": lt_goc_noi_tiep(), "caption": "$\\widehat{PMQ}$, $\\widehat{PNQ}$ cùng chắn cung $PQ$",
                  "pos": "right"}
    out["Hình 1"] = {"tikz": kham_pha(), "caption": "Hình 1", "pos": "right"}
    out["Bài 1."] = {"tikz": bai1_ngoc_thuy(), "caption": "Hình 2", "pos": "right"}
    n, gv = vd1_ban_mai()
    out["Ví dụ 1."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 3", "pos": "right"}
    n, gv = bai2_gia_lam()
    out["Bài 2."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 4", "pos": "right"}
    n, gv, _ = vd2_cau_giay()
    out["Ví dụ 2."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 5", "pos": "right"}
    n, gv = bai3_thang_long()
    out["Bài 3."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 6", "pos": "right"}
    n, gv = bai4_tho_loc()
    out["Bài 4."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 7", "pos": "right"}
    n, gv = btvn1_lomonoxop()
    out["BTVN 1."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 8", "pos": "right"}
    n, gv = btvn2_mai_dich()
    out["BTVN 2."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 9", "pos": "right"}
    n, gv = btvn3_hat_mon()
    out["BTVN 3."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 10", "pos": "right"}
    n, gv = btvn4_son_tay()
    out["BTVN 4."] = {"tikz": n, "tikz_gv": gv, "caption": "Hình 11", "pos": "right"}
    return out


if __name__ == "__main__":
    h = tat_ca()
    for x in KIEM:
        print("  ✓", x)
    print("E nằm giữa N và T (VD2):", vd2_cau_giay()[2])
    print("Dựng", len(h), "hình.")
