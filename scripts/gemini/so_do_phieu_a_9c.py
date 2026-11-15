#!/usr/bin/env python3
"""Sơ đồ phiếu A ch.VI 9C — "Bài 19. Phương trình bậc hai một ẩn" (sửa 13/11/2026).

Claude chọn đề + đáp số, kiểm SymPy ở đây; Gemini chỉ viết chữ (viec_sua_phieu_a_9c.py).

    .venv/bin/python scripts/gemini/so_do_phieu_a_9c.py      # kiểm nghiệm + không trùng phương trình

Mỗi ý: (vế trái, vế phải, loại) — chuỗi SymPy theo x.
  loại "heso"  : thu gọn về ax^2+bx+c=0, chỉ ra a, b, c (hoặc "không phải phương trình bậc hai")
  loại "kc"    : khuyết c — đặt nhân tử chung
  loại "kb"    : khuyết b — x^2 = k
  loại "delta" : công thức nghiệm Δ
  loại "so_ng" : tính Δ, kết luận số nghiệm (Δ = 0 hoặc Δ < 0)
  loại "dphay" : công thức nghiệm thu gọn Δ'
  loại "giai"  : tự giải (TH)
  loại "tt"    : bài thực tế — nghiệm nhận theo điều kiện ghi ở cột cuối
"""
from __future__ import annotations

import sys

import sympy as sp

x = sp.symbols("x")

# nhãn → (mức, tier, nguồn, [(vt, vp, loại, ghi chú)])
SO_DO: dict[str, tuple] = {
    # ── LUYỆN TẬP 1 (NB, ví dụ điền + khung bài giải) ──
    "Ví dụ 1.": (0, "vidu", "", [("(x+1)*(x-4)", "2*x", "heso", "a"), ("(x+2)*(x-3)", "x**2+1", "heso", "b")]),
    "Bài 1.": (1, "onclass", "", [
        ("x**2-1", "5*(x+1)", "heso", "Giữa kì I, THCS Nguyễn Du"),
        ("x*(x+10)", "3000", "heso", "đề minh họa Vào 10, Sở GD\\&ĐT Hà Nội"),
        ("(x-3)*(x+2)-x**2+9", "0", "heso", "Giữa kì I, THCS Dịch Vọng Hậu")]),
    "Ví dụ 2.": (0, "vidu", "", [("4*x**2+6*x", "0", "kc", "")]),
    "Bài 2.": (1, "onclass", "", [("x**2-7*x", "0", "kc", ""), ("3*x**2-12*x", "0", "kc", ""),
                                  ("2*x**2+5*x", "0", "kc", "")]),
    "Ví dụ 3.": (0, "vidu", "", [("2*x**2-18", "0", "kb", "a"), ("x**2+4", "0", "kb", "b")]),
    "Bài 3.": (1, "onclass", "", [("x**2-25", "0", "kb", ""), ("4*x**2-9", "0", "kb", ""),
                                  ("3*x**2+12", "0", "kb", "")]),
    "Ví dụ 4.": (0, "vidu", "", [("2*x**2-5*x+2", "0", "delta", "")]),
    "Bài 4.": (1, "onclass", "", [
        ("x**2-3*x+2", "0", "delta", ""),
        ("x**2+x-6", "0", "delta", "bộ đề Vào 10, Phòng GD\\&ĐT Đống Đa"),
        ("x**2-3*x-1", "0", "delta", "thi thử Vào 10 lần 3, Phòng GD\\&ĐT Ứng Hòa")]),
    "Ví dụ 5.": (0, "vidu", "", [("9*x**2-6*x+1", "0", "so_ng", "a"), ("x**2+x+3", "0", "so_ng", "b")]),
    "Bài 5.": (1, "onclass", "", [("4*x**2-4*x+1", "0", "so_ng", ""), ("x**2-x+1", "0", "so_ng", ""),
                                  ("2*x**2-3*x+4", "0", "so_ng", "")]),
    "Ví dụ 6.": (0, "vidu", "", [("x**2-8*x+12", "0", "dphay", "")]),
    "Bài 6.": (1, "onclass", "", [
        ("x**2-6*x+5", "0", "dphay", ""),
        ("x**2+10*x+4", "0", "dphay", "thi thử Vào 10, THCS Tự Lập"),
        ("2*x**2-4*x+1", "0", "dphay", "thi thử Vào 10 lần 1, THCS Cầu Giấy")]),
    # ── LUYỆN TẬP 2 (TH tự trình bày, VD) ──
    "Ví dụ 7.": (0, "vidu", "", [("x*(x+4)", "2*x+15", "giai", "")]),
    "Bài 7.": (2, "onclass", "", [
        ("5*x**2-21*x-54", "0", "giai", "thi thử Vào 10 lần 3, Phòng GD\\&ĐT Ứng Hòa"),
        ("2*x**2-x-5", "0", "giai", "Cuối kì II, Phòng GD\\&ĐT Ba Đình"),
        ("6*x**2-4*x-1", "0", "giai", "Giữa kì II, xã Đông Anh"),
        ("3*x**2+5*x-2", "0", "giai", "thêm tay sua_tay_phieu_a_9c.py")]),
    "Bài 8.": (2, "onclass", "", [
        ("(x-1)**2", "x+5", "giai", ""),
        ("x*(x+20)", "2400", "giai", "thi thử Vào 10 lần 5, Phòng GD\\&ĐT Chương Mỹ"),
        ("(x-3)*(x+1)", "2*x+9", "giai", "thêm tay sua_tay_phieu_a_9c.py")]),
    "Ví dụ 8.": (0, "vidu", "", [("x**2+6*x-1080", "0", "tt", "x>0 · vận tốc tăng tốc x+6 = 36 < 40")]),
    "Bài 9.": (3, "onclass", "thi thử Vào 10 lần 4, Phòng GD\\&ĐT Chương Mỹ",
               [("x**2-2*x-120", "0", "tt", "x nguyên, x>2 · 12 xe")]),
    "Ví dụ 9.": (0, "vidu", "", [("x*(x+2)", "168", "tt", "x chẵn, x>=0 · 12 và 14")]),
    "Bài 10.": (3, "onclass", "bộ đề Vào 10, Phòng GD\\&ĐT Đống Đa",
                [("x*(x+11)", "180", "tt", "x>0 · rộng 9 m, dài 20 m")]),
    # ── BTVN ──
    "Bài 11.": (1, "btvn", "", [
        ("(2*x-5)*(x-3)", "0", "heso", "Giữa kì I, THCS Cổ Nhuế 2"),
        ("2*x**2-(x+1)", "x-3", "heso", "Cuối kì II, Hà Nội"),
        ("(x-1)*(x+3)-x**2", "5", "heso", "")]),
    "Bài 12.": (1, "btvn", "", [("3*x**2-9*x", "0", "kc", ""), ("2*x**2+7*x", "0", "kc", "")]),
    "Bài 13.": (1, "btvn", "", [("x**2-49", "0", "kb", ""), ("9*x**2-4", "0", "kb", ""),
                                ("3*x**2+27", "0", "kb", "")]),
    "Bài 14.": (1, "btvn", "", [("x**2-5*x+6", "0", "delta", ""), ("2*x**2-3*x-2", "0", "delta", ""),
                                ("x**2-x-3", "0", "delta", "")]),
    "Bài 15.": (1, "btvn", "", [("25*x**2-10*x+1", "0", "so_ng", ""), ("x**2+x+1", "0", "so_ng", ""),
                                ("3*x**2-x+2", "0", "so_ng", "")]),
    "Bài 16.": (1, "btvn", "", [("x**2-10*x+21", "0", "dphay", ""), ("x**2+4*x-1", "0", "dphay", ""),
                                ("3*x**2-8*x+4", "0", "dphay", "")]),
    "Bài 17.": (2, "btvn", "", [
        ("x**2-8*x-5", "0", "giai", "thi thử Vào 10, cụm THCS công lập Hà Nội"),
        ("2*x**2+5*x-3", "0", "giai", ""), ("x**2-3*x-10", "0", "giai", "")]),
    "Bài 18.": (2, "btvn", "", [("(x-2)**2", "3*x-2", "giai", ""), ("(x+1)*(x+2)", "4*x+8", "giai", "")]),
    "Bài 19.": (3, "btvn", "", [("x**2+10*x-2000", "0", "tt", "x>0 · 100 km, nhanh hơn 10 km/h, sớm 30 phút · vận tốc dự định 40 km/h")]),
    "Bài 20.": (3, "btvn", "", [("x*(25-x)", "150", "tt", "0<x<25 · hai cạnh 10 m và 15 m")]),
}


def chuan(vt, vp):
    """Đa thức chuẩn hoá (hệ số nguyên, a > 0 nếu bậc 2) của vt - vp."""
    p = sp.Poly(sp.expand(sp.sympify(vt) - sp.sympify(vp)), x)
    if p.degree() == 2 and p.LC() < 0:
        p = -p
    return p


def tex_nghiem(r):
    return sp.latex(sp.nsimplify(r))


def mo_ta(vt, vp, loai):
    p = chuan(vt, vp)
    if p.degree() != 2:
        return f"thu gọn: {p.as_expr()} = 0 — KHÔNG phải phương trình bậc hai"
    a, b, c = (p.coeff_monomial(x**k) for k in (2, 1, 0))
    d = b * b - 4 * a * c
    ng = sorted(sp.solve(p.as_expr(), x), key=lambda r: -float(r)) if d >= 0 else []
    s = f"thu gọn: {sp.sstr(p.as_expr())} = 0 · a={a}, b={b}, c={c} · Δ={d}"
    if b % 2 == 0:
        s += f" · b'={b // 2}, Δ'={(b // 2) ** 2 - a * c}"
    if d < 0:
        s += " · vô nghiệm"
    elif d == 0:
        s += f" · nghiệm kép x1 = x2 = {tex_nghiem(ng[0])}"
    else:
        s += " · nghiệm " + ", ".join(tex_nghiem(r) for r in ng)
    return s


def tom_tat():
    """(dict nhãn → các dòng mô tả, danh sách trùng)."""
    tt, gap, trung = {}, {}, []
    for nhan, (muc, tier, nguon, y) in SO_DO.items():
        dong = []
        for i, (vt, vp, loai, ghi) in enumerate(y):
            p = chuan(vt, vp)
            key = tuple(p.all_coeffs())
            if key in gap:
                trung.append(f"{nhan} ý {i + 1} trùng {gap[key]}")
            gap[key] = f"{nhan} ý {i + 1}"
            ten = chr(ord("a") + i) + ") " if len(y) > 1 else ""
            de = f"${sp.latex(sp.sympify(vt, evaluate=False))}={sp.latex(sp.sympify(vp, evaluate=False))}$"
            dong.append(f"{ten}[{loai}] {vt} = {vp} → {mo_ta(vt, vp, loai)}" + (f" · ({ghi})" if ghi else ""))
        tt[nhan] = dong
    return tt, trung


def main():
    tt, trung = tom_tat()
    for k, v in tt.items():
        print(k)
        for d in v:
            print("   ", d)
    print("TRÙNG:", trung or "không")
    sys.exit(1 if trung else 0)


if __name__ == "__main__":
    main()
