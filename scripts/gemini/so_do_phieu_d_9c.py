#!/usr/bin/env python3
"""Sơ đồ phiếu D ch.VI 9C — "Tính giá trị biểu thức chứa hai nghiệm" (dựng lại 13/11/2026).

Claude chọn đề + đáp số, kiểm SymPy ở đây; Gemini chỉ viết chữ (viec_dung_lai_phieu_d_9c.py).

    .venv/bin/python scripts/gemini/so_do_phieu_d_9c.py      # kiểm mọi đáp số + không trùng phương trình

Mỗi mục: (nhãn, mức, tier, nguồn, (a, b, c), [(loại, biểu thức, mô tả)])
  loại "viete"  : Δ/ac + tổng + tích
  loại "ha_bac" : x1^2 và x1^3 theo x1
  loại "gt"     : giá trị biểu thức (chuỗi SymPy theo x1, x2) — phải bằng nhau khi đổi vai hai nghiệm
  loại "dau"    : dấu hai nghiệm
  loại "can"    : rút gọn √((x_i ± t)^2) theo dấu nghiệm (biểu thức sympy, nghiệm áp dụng)
"""
from __future__ import annotations

import sys

import sympy as sp

x, x1, x2 = sp.symbols("x x1 x2")

NGUON_2026 = "đề chính thức Vào 10, Sở GD\\&ĐT Hà Nội, 2026"
NGUON_TU_LAP = "thi thử Vào 10, THCS Tự Lập"

# ── LUYỆN TẬP 1 (NB, điền khuyết) ───────────────────────────────────────────
VI_DU = {
    "Ví dụ 1.": ((1, -7, 3), [("viete", None, "Viết tổng và tích hai nghiệm (đủ bước kiểm tra Δ)")]),
    "Ví dụ 2.": ((1, -2, -5), [("ha_bac", None, "Gọi x1 là một nghiệm, viết x1^2 và x1^3 theo x1")]),
    "Ví dụ 3.": ((1, -6, 1), [("gt", "x1**2 - 6*x1 + 2026", "Tính G = x1^2 - 6x1 + 2026")]),
    "Ví dụ 4.": ((1, -5, -2), [("gt", "x1**2 + 5*x2 - 3", "Tính P = x1^2 + 5x2 - 3")]),
    "Ví dụ 5.": ((1, 6, 2), [("dau", None, "Chứng tỏ hai nghiệm cùng âm"),
                             ("can", ("sqrt((x1-1)**2)", "x1"), "rút gọn √((x1-1)^2)")]),
    # LT2
    "Ví dụ 6.": ((1, -3, -3), [("gt", "x1**3 - 12*x1 + 2000", "Tính H = x1^3 - 12x1 + 2000")]),
    "Ví dụ 7.": ((1, -8, 5), [("gt", "x1**2 + 8*x2 - 1", "Tính P = x1^2 + 8x2 - 1")]),
    "Ví dụ 8.": ((1, 8, 3), [("dau", None, "hai nghiệm cùng âm"),
                             ("gt", "sqrt(-12*x1 + 1) - x2", "Tính A = √(-12x1 + 1) - x2")]),
    "Ví dụ 9.": ((1, -4, 1), [("gt", "(4*x2 - 1)/x1 + 4*x1/x2 - x1", "Tính Q = (4x2-1)/x1 + 4x1/x2 - x1")]),
}

BAI = [
    # nhãn, mức, tier, nguồn, phương trình, các ý
    ("Bài 1.", 1, "onclass", "", None, [
        ("viete", (1, -5, 3), "a"), ("viete", (1, 4, -7), "b"), ("viete", (2, -6, 1), "c"),
        ("viete", (1, 6, -2), "d")]),   # 13/11 bù NB
    ("Bài 2.", 1, "onclass", "", None, [
        ("ha_bac", (1, -4, 2), "a"), ("ha_bac", (1, 3, -2), "b"), ("ha_bac", (1, -6, -3), "c"),
        ("ha_bac", (1, 5, -1), "d")]),
    ("Bài 3.", 1, "onclass", "", None, [
        ("gt", (1, -5, -4), "x1**2 - 5*x1 + 2021"), ("gt", (1, -1, -1), "x1**3 - 2*x1 + 2024"),
        ("gt", (1, -3, -2), "x1**2 - 3*x1 + 2023")]),
    ("Bài 4.", 1, "onclass", "", None, [
        ("gt", (1, -4, -6), "x1**2 + 4*x2 + 1"), ("gt", (1, -7, 4), "x1**2 + 7*x2 - 10"),
        ("gt", (1, -6, 2), "x1**2 + 6*x2 - 5")]),
    ("Bài 6.", 1, "onclass", "", None, [
        ("can", (1, 5, 3), ("sqrt((x1-2)**2)", "x1")), ("can", (1, -9, 5), ("sqrt((x2+3)**2)", "x2")),
        ("can", (1, 9, 4), ("sqrt((x2-1)**2)", "x2"))]),
    ("Bài 5.", 1, "onclass", "", None, [   # khung bài giải đủ bước, 13/11 thành 3 ý
        ("gt", (1, -2, -7), "x1**2 + 2*x2 + x1*x2"), ("gt", (1, -4, -1), "x1**2 + 4*x2 + x1*x2"),
        ("gt", (1, -8, -3), "x1**2 + 8*x2 + x1*x2")]),   # khung bài giải đủ bước
    # LT2 — tự trình bày
    ("Bài 7.", 2, "onclass", "", None, [
        ("gt", (1, -1, -3), "x1**3 - 4*x1 + 2030"), ("gt", (1, 2, -1), "x1**3 - 5*x1 + 2020")]),
    ("Bài 8.", 2, "onclass", "", None, [
        ("gt", (1, -3, -6), "x1**2 + 3*x2 + x1*x2"), ("gt", (1, -9, 7), "x1**2 + 9*x2 - 20"),
        ("gt", (4, -2, -1), "(x1 - x2)**2 - x1*(x1 - 1/2)")]),   # 13/11: cuối kì II THCS Phúc Đồng
    # 13/11 bù giờ: bài TH mới, 5 ý đề thật (biểu thức đối xứng sau khi biến đổi)
    ("Bài 9.", 2, "onclass", "", None, [
        ("gt", (1, 4, -6), "1/(x1 + 3) + 1/(x2 + 3)"),            # thi thử Vào 10 THCS Thái Thịnh 2025
        ("gt", (1, -5, 4), "(5*x1 - x2)/x1 - (x1 - 5*x2)/x2"),    # bộ đề Vào 10 THCS Quang Trung
        ("gt", (2, -13, -6), "(x1 + x2)*(x1 + 2*x2) - x2**2"),    # bộ đề Vào 10 THCS Tô Vĩnh Diện
        ("gt", (1, -7, -1), "x1**2 + x2**2 - x1*x2")]),            # cuối kì II THCS Thăng Long
    ("Bài 10.", 3, "onclass", NGUON_TU_LAP, (1, 10, 4), [("gt", None, "sqrt(-16*x1 + 5) - x2")]),
    ("Bài 11.", 3, "onclass", NGUON_2026, (1, -3, 1), [("gt", None, "(3*x2 - 1)/x1 + 3*x1/x2 - x1")]),
    # BTVN
    ("Bài 12.", 1, "btvn", "", None, [
        ("viete", (1, -9, 2), "a"), ("viete", (1, 5, -3), "b"), ("viete", (3, -6, 2), "c")]),
    ("Bài 13.", 1, "btvn", "", None, [
        ("ha_bac", (1, -2, -2), "a"), ("ha_bac", (1, 4, 1), "b"), ("ha_bac", (1, -5, -1), "c")]),
    ("Bài 14.", 1, "btvn", "", None, [
        ("gt", (1, -7, 1), "x1**2 - 7*x1 + 2026"), ("gt", (1, -2, -6), "x1**2 - 2*x1 + 2019"),
        ("gt", (1, 1, -5), "x1**3 - 6*x1 + 2030")]),
    ("Bài 15.", 1, "btvn", "", None, [
        ("gt", (1, -6, -1), "x1**2 + 6*x2 + 3"), ("gt", (1, -10, 8), "x1**2 + 10*x2 - 50"),
        ("gt", (1, -3, -5), "x1**2 + 3*x2 - 2*x1*x2")]),
    ("Bài 16.", 1, "btvn", "", None, [
        ("can", (1, 7, 5), ("sqrt((x1-4)**2)", "x1")), ("can", (1, -8, 3), ("sqrt((x2+1)**2)", "x2"))]),
    ("Bài 17.", 1, "btvn", "", (1, -6, -5), [("gt", None, "x1**2 + 6*x2 + x1*x2")]),   # khung bài giải đủ bước
    ("Bài 18.", 2, "btvn", "", None, [
        ("gt", (1, -1, -4), "x1**3 - 5*x1 + 2021"), ("gt", (1, 3, -1), "x1**3 - 10*x1 + 2000"),
        ("gt", (1, -4, -2), "x1**3 - 18*x1 + 2017")]),
    ("Bài 19.", 2, "btvn", "", None, [
        ("gt", (1, -7, -2), "x1**2 + 7*x2 + 3*x1*x2"), ("gt", (1, 6, -4), "x1**2 - 6*x2 + 1"),
        ("gt", (2, -8, 3), "2*x1**2 + 8*x2 + 3")]),
    # 13/11 bù giờ BTVN: bài TH mới (tài liệu Mathtech ch.VI "Định lí Viète")
    ("Bài 20.", 2, "btvn", "", None, [
        ("gt", (1, -4, -7), "x1/x2 + x2/x1 - 2"), ("gt", (2, -4, -3), "(x1 - x2)**2"),
        ("gt", (1, -2, -9), "x1/x2 + x2/x1")]),   # thi thử Vào 10 THCS Thái Thịnh 2026 (chuyển từ Bài 9e)
    ("Bài 21.", 3, "btvn", "", (1, 12, 5), [("gt", None, "sqrt(-18*x1 + 4) - x2")]),
    ("Bài 22.", 3, "btvn", "", (1, -5, 1), [("gt", None, "(5*x2 - 1)/x1 + 5*x1/x2 - x1")]),
]


def pt(abc):
    a, b, c = abc
    return a * x**2 + b * x + c


def viete(abc):
    a, b, c = abc
    d = b * b - 4 * a * c
    out = {"Delta": d, "ac": a * c, "tong": sp.Rational(-b, a), "tich": sp.Rational(c, a)}
    if b % 2 == 0:
        out["Delta_phay"] = (b // 2) ** 2 - a * c
    assert d > 0, f"{abc}: Δ = {d} ≤ 0"
    return out


def ha_bac(abc):
    a, b, c = abc
    x1sq = sp.expand((-b * x1 - c) / a)
    x1cu = sp.expand(sp.expand(x1 * x1sq).subs(x1**2, x1sq))
    r = sp.solve(pt(abc), x)
    for v in r:   # kiểm số
        assert sp.simplify(v**2 - x1sq.subs(x1, v)) == 0 and sp.simplify(v**3 - x1cu.subs(x1, v)) == 0
    return {"x1^2": x1sq, "x1^3": x1cu}


def gia_tri(abc, bt):
    r = sp.solve(pt(abc), x)
    e = sp.sympify(bt, locals={"x1": x1, "x2": x2})
    v1 = sp.nsimplify(sp.simplify(e.subs({x1: r[0], x2: r[1]})))
    v2 = sp.nsimplify(sp.simplify(e.subs({x1: r[1], x2: r[0]})))
    assert sp.simplify(v1 - v2) == 0, f"{abc} {bt}: đổi vai hai nghiệm ra {v1} ≠ {v2}"
    return sp.simplify(v1)


def dau(abc):
    v = viete(abc)
    if v["tich"] < 0:
        return "trái dấu"
    return "cùng dương" if v["tong"] > 0 else "cùng âm"


def can(abc, bt_nghiem):
    bt, ng = bt_nghiem
    r = sp.solve(pt(abc), x)
    dd = dau(abc)
    assert dd != "trái dấu", f"{abc}: hai nghiệm trái dấu, √ không xác định dấu theo một nghiệm"
    sym = {"x1": x1, "x2": x2}[ng]
    e = sp.sympify(bt, locals={"x1": x1, "x2": x2})
    inner = sp.sqrt(e**2).args[0] if False else None   # noqa
    ket = []
    for v in r:
        ket.append(sp.simplify(e.subs(sym, v)))
    # dạng rút gọn: thử hai ứng viên ±(trong căn)
    base = sp.sympify(bt.replace("sqrt(", "(").replace("**2)", ")"), locals={"x1": x1, "x2": x2})
    for cand in (base, -base):
        if all(sp.simplify(cand.subs(sym, v) - k) == 0 for v, k in zip(r, ket)):
            return dd, sp.expand(cand)
    raise AssertionError(f"{abc} {bt}: không rút gọn được")


def tom_tat():
    """Trả về dict nhãn → danh sách dòng đáp số (chuỗi) để nhúng vào prompt Gemini."""
    out = {}
    dung = {}
    def ghi_pt(abc, nhan):
        k = tuple(abc)
        dung.setdefault(k, []).append(nhan)

    for nhan, (abc, viec) in VI_DU.items():
        ghi_pt(abc, nhan)
        dong = [f"Phương trình {sp.sstr(pt(abc))} = 0"]
        for loai, bt, mo_ta in viec:
            dong.append(f"  {mo_ta}: " + _dap(loai, abc, bt))
        out[nhan] = dong
    for nhan, muc, tier, nguon, abc0, y in BAI:
        dong = []
        for i, (loai, abc, bt) in enumerate(y):
            abc = abc or abc0
            ghi_pt(abc, nhan)
            ten = "abcdef"[i] + ") " if len(y) > 1 else ""
            bt_hien = None if loai in ("viete", "ha_bac") else bt
            dong.append(f"{ten}{sp.sstr(pt(abc))} = 0" + (f", biểu thức {bt_hien}" if bt_hien and loai == "gt" else "")
                        + (f", rút gọn {bt[0]}" if loai == "can" else "") + " → " + _dap(loai, abc, bt))
        out[nhan] = dong
    trung = {k: v for k, v in dung.items() if len(v) > 1}
    return out, trung


def _dap(loai, abc, bt):
    if loai == "viete":
        v = viete(abc)
        s = f"Δ = {v['Delta']}" + (f", Δ' = {v['Delta_phay']}" if "Delta_phay" in v else "") + f", ac = {v['ac']}"
        return s + f", x1 + x2 = {v['tong']}, x1x2 = {v['tich']}"
    if loai == "ha_bac":
        h = ha_bac(abc)
        return f"x1^2 = {h['x1^2']}, x1^3 = {h['x1^3']}  (Δ = {viete(abc)['Delta']})"
    if loai == "gt":
        v = viete(abc)
        return f"= {gia_tri(abc, bt)}  (Δ = {v['Delta']}, tổng {v['tong']}, tích {v['tich']})"
    if loai == "dau":
        return dau(abc)
    if loai == "can":
        dd, rg = can(abc, bt)
        return f"hai nghiệm {dd} ⇒ {bt[0]} = {rg}"
    raise ValueError(loai)


if __name__ == "__main__":
    tt, trung = tom_tat()
    for k, v in tt.items():
        print(k)
        for d in v:
            print("   ", d)
    if trung:
        print("\n✗ PHƯƠNG TRÌNH TRÙNG:", trung)
        sys.exit(1)
    print("\n✓ mọi đáp số đã kiểm, không phương trình nào lặp trong phiếu")
