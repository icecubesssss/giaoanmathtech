#!/usr/bin/env python3
"""Sơ đồ phiếu B ch.VI 9C — "Phương trình chứa ẩn ở mẫu quy về phương trình bậc hai" (sửa 13/11/2026).

Thầy chốt 13/11: giữ nhẩm nghiệm (SGK Toán 9 tập hai, Bài 20 tr.22) nhưng gọn; bỏ bài lẻ (tính ac, rút gọn căn,
câu kết luận); dồn giờ cho phương trình chứa ẩn ở mẫu (SGK Toán 9 tập một, Bài 4 tr.28–29, 4 bước).
Claude chọn đề + đáp số, kiểm SymPy ở đây; Gemini chỉ viết chữ (viec_sua_phieu_b_9c.py).

    .venv/bin/python scripts/gemini/so_do_phieu_b_9c.py      # kiểm nghiệm + không trùng phương trình

Mỗi ý: (vế trái, vế phải, loại, ghi chú) — chuỗi SymPy theo x.
  "dkxd"  : chỉ tìm điều kiện xác định
  "khu"   : ĐKXĐ + quy đồng, khử mẫu, thu gọn về ax^2+bx+c=0, chỉ ra a, b, c (chưa giải)
  "nham"  : phương trình bậc hai — nhẩm nghiệm a+b+c=0 hoặc a-b+c=0
  "giai4" : giải trọn 4 bước (NB khung điền / ví dụ)
  "giai"  : tự giải (TH)
  "tt"    : bài thực tế, phương trình cho sẵn — giải, đối chiếu điều kiện, trả lời
"""
from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

x = sp.symbols("x")

SO_DO: dict[str, tuple] = {
    # ── LUYỆN TẬP 1 (NB) ──
    "Ví dụ 1.": (0, "vidu", "", [("2*x/(x+3)", "(x-1)/(x-4)", "dkxd", "a"),
                                 ("1/x+3/(x-5)", "(x+2)/(x**2-5*x)", "dkxd", "b")]),
    "Bài 1.": (1, "onclass", "", [("(x+2)/(x-1)", "3/(x+6)", "dkxd", ""),
                                  ("x/(x+4)-2/(x-4)", "(x+8)/(x**2-16)", "dkxd", ""),
                                  ("3/(x-2)+1/x", "(x+6)/(x**2-2*x)", "dkxd", "")]),
    "Ví dụ 2.": (0, "vidu", "", [("x/(x-1)+2/(x+1)", "4/(x**2-1)", "khu", "")]),
    "Bài 2.": (1, "onclass", "", [("x/(x+3)+2/(x-3)", "20/(x**2-9)", "khu", ""),
                                  ("2/x+x/(x-3)", "6/(x**2-3*x)", "khu", ""),
                                  ("10/x-10/(x+1)", "1", "khu", "")]),
    "Ví dụ 3.": (0, "vidu", "", [("2*x**2-9*x+7", "0", "nham", "a"), ("3*x**2+10*x+7", "0", "nham", "b")]),
    "Bài 3.": (1, "onclass", "", [("x**2-8*x+7", "0", "nham", ""), ("x**2+9*x+8", "0", "nham", ""),
                                  ("5*x**2-2*x-3", "0", "nham", "")]),
    "Ví dụ 4.": (0, "vidu", "", [("2*x/(x+3)+1/(x-1)", "4/((x-1)*(x+3))", "giai4", "nhẩm a+b+c, loại x=1")]),
    "Bài 4.": (1, "onclass", "", [("x/(x+1)+2/(x-1)", "4/(x**2-1)", "giai4", "nhẩm a+b+c, loại x=1"),
                                  ("1/x+2/(x+2)", "1", "giai4", "nhẩm a-b+c, nhận cả hai"),
                                  ("x/(x-5)-10/(x+5)", "50/(x**2-25)", "giai4", "khuyết c, loại x=5")]),
    # ── LUYỆN TẬP 2 (TH, VD) ──
    "Ví dụ 5.": (0, "vidu", "", [("(x+4)/(x-2)-2/x", "12/(x**2-2*x)", "giai", "Δ', loại x=2")]),
    "Bài 5.": (2, "onclass", "", [
        ("150/(x-1)-140/x", "5", "giai", "Giữa kì II, xã Đông Anh"),
        ("x/(x-3)-2/(x+1)", "(15-x)/(x**2-2*x-3)", "giai", "Giữa kì I, THCS Dịch Vọng Hậu"),
        ("x/(x+2)+5/(x-2)", "20/(x**2-4)", "giai", ""),
        # 13/11 bù giờ (trên lớp 90′ → ~114′): 4 ý TH đề thật
        ("2*x/(x+1)+(7*x**2-3*x)/(x**2-1)", "(3*x-1)/(x-1)", "giai", "Giữa kì I, THCS Giảng Võ"),
        ("(2*x-2)/(x-3)-(x-5)/(x+3)", "-21/(x**2-9)", "giai", "Học kì I, THCS Nguyễn Trường Tộ")]),
    "Bài 6.": (2, "onclass", "", [("2*x/(x-2)+(x+2)/(2-x)", "x-1", "giai", "đổi dấu mẫu, vô nghiệm"),
                                  ("x/(x-3)+2/(x+1)", "-8/((x-3)*(x+1))", "giai", "nhẩm a-b+c, loại x=-1"),
                                  ("(3*x-1)/(x-2)-(2*x-3)/(x+2)+(2*x**2+7*x-2)/(4-x**2)", "0", "giai",
                                   "Giữa kì I, THCS Nguyễn Trường Tộ"),
                                  ("(x+2)/(x-2)-(x-2)/(2+x)", "(x**2+16)/(x**2-4)", "giai", "Giữa kì I, THCS Ái Mộ")]),
    "Ví dụ 6.": (0, "vidu", "", [("90/x-90/(x+15)", "1", "tt",
                                  "90 km, ô tô nhanh hơn xe máy 15 km/h, đến sớm hơn 1 giờ · x>0 · xe máy 30, ô tô 45")]),
    "Bài 7.": (3, "onclass", "thi thử Vào 10 lần 5, Phòng GD\\&ĐT Chương Mỹ",
               [("50/x-50/(x+20)", "5/12", "tt", "50 km, ô tô nhanh hơn 20 km/h, xe máy đi trước 25 phút · x>0 · 40 và 60")]),
    "Bài 8.": (3, "onclass", "đề minh họa Vào 10, Sở GD\\&ĐT Hà Nội",
               [("300/x-300/(x+10)", "1", "tt", "300 sản phẩm, hơn 10 sp/ngày, sớm 1 ngày · x nguyên dương · 50 sp/ngày, 6 ngày")]),
    # ── BTVN ──
    "Bài 9.": (1, "btvn", "", [("(x-3)/(x+5)", "2/(x-1)", "dkxd", ""),
                               ("x/(x-6)+1/(x+6)", "12/(x**2-36)", "dkxd", ""),
                               ("5/x-2/(x+3)", "(x+1)/(x**2+3*x)", "dkxd", "")]),
    "Bài 10.": (1, "btvn", "", [("x/(x-2)+3/(x+2)", "8/(x**2-4)", "khu", ""),
                                ("12/x-12/(x+1)", "1", "khu", "")]),
    "Bài 11.": (1, "btvn", "", [("x**2-10*x+9", "0", "nham", ""), ("x**2+6*x+5", "0", "nham", ""),
                                ("3*x**2-5*x+2", "0", "nham", "")]),
    "Bài 12.": (1, "btvn", "", [("x/(x-1)+3/(x+3)", "4/((x-1)*(x+3))", "giai4", "nhẩm a+b+c, loại x=1"),
                                ("8/x-3/(x-1)", "1", "giai4", "Δ', nhận cả hai")]),
    "Bài 13.": (2, "btvn", "", [
        ("x/(x+2)+17/(x**2-4)", "4/(x-2)", "giai", "Giữa kì I, THCS Nguyễn Du"),
        ("x/(x+4)+3/(x-4)", "24/(x**2-16)", "giai", ""),
        ("(x+1)/(x-2)-3/x", "6/(x**2-2*x)", "giai", "vô nghiệm"),
        ("1/(x+1)+2/(x-1)", "(x**2+1)/(x**2-1)", "giai", "Giữa kì I, THCS Chuyên Mỹ")]),
    "Bài 14.": (2, "btvn", "", [("4*x/(x-1)+(x+3)/(1-x)", "x", "giai", "đổi dấu mẫu, loại x=1"),
                                ("40/(x-2)-40/x", "1", "giai", ""),
                                ("(2*x-5)/(x+4)+x/(4-x)", "(-17*x+56)/(x**2-16)", "giai", "Giữa kì I, THCS Nguyễn Huy Tưởng")]),
    "Bài 15.": (3, "btvn", "", [("120/x-120/(x+4)", "1", "tt",
                                 "120 cây, mỗi ngày trồng thêm 4 cây, xong sớm 1 ngày · x nguyên dương · 20 cây/ngày, 6 ngày")]),
    "Bài 16.": (3, "btvn", "", [("24/x-24/(x+4)", "1/2", "tt",
                                 "24 km, về nhanh hơn 4 km/h, ít hơn 30 phút · x>0 · 12 km/h")]),
}


# Đề thật: phiếu A chỉ có phương trình bậc hai SAU khử mẫu (A Bài 8b, A Bài 1b), phiếu B luyện bước khử mẫu.
CHO_TRUNG_A = {("Bài 7.", 0), ("Bài 8.", 0), ("Bài 5.", 1),  # Bài 5b: đề thật Dịch Vọng Hậu
               ("Bài 6.", 2), ("Bài 13.", 3)}  # 13/11: đề thật Nguyễn Trường Tộ, Chuyên Mỹ


def _mau(bt):
    """Các giá trị làm một mẫu thức bằng 0."""
    out = set()
    for t in sp.Add.make_args(sp.sympify(bt, evaluate=False)):
        d = sp.denom(sp.factor(t))
        if d.free_symbols:
            out |= set(sp.solve(d, x))
    return out


def _mtc(*bts):
    """Mẫu thức chung = BCNN các mẫu (đã phân tích)."""
    m = sp.Integer(1)
    for bt in bts:
        for t in sp.Add.make_args(sp.sympify(bt, evaluate=False)):
            m = sp.lcm(m, sp.factor(sp.denom(sp.factor(t))))
    return m


def chuan(vt, vp):
    """(ĐKXĐ, đa thức sau khử mẫu đã chuẩn hoá, nghiệm, nghiệm nhận, nghiệm loại)."""
    dk = sorted(_mau(vt) | _mau(vp))
    n = sp.cancel((sp.sympify(vt) - sp.sympify(vp)) * _mtc(vt, vp))
    p = sp.Poly(sp.expand(n), x)
    if p.LC() < 0:
        p = -p
    g = sp.gcd_list(p.all_coeffs())
    p = sp.Poly(p.as_expr() / g, x)
    ng = [r for r in sp.solve(p.as_expr(), x) if r.is_real] if p.degree() <= 2 else []
    ng = sorted(ng, key=lambda r: -float(r))
    nhan = [r for r in ng if r not in dk]
    loai = [r for r in ng if r in dk]
    return dk, p, ng, nhan, loai


def L(r):
    return sp.latex(sp.nsimplify(r))


def mo_ta(vt, vp, loai):
    dk, p, ng, nhan, lo = chuan(vt, vp)
    s = ""
    if dk:
        s += "ĐKXĐ: " + " và ".join(f"x ≠ {L(r)}" for r in dk) + " · "
    if loai == "dkxd":
        return s.rstrip(" ·")
    a, b, c = (p.coeff_monomial(x**k) for k in (2, 1, 0))
    s += f"khử mẫu, thu gọn: {sp.sstr(p.as_expr())} = 0 (a={a}, b={b}, c={c})"
    if loai == "khu":
        return s
    d = b * b - 4 * a * c
    s += f" · Δ={d}"
    if b % 2 == 0:
        s += f", b'={b // 2}, Δ'={(b // 2) ** 2 - a * c}"
    if a + b + c == 0:
        s += " · a+b+c=0"
    if a - b + c == 0:
        s += " · a-b+c=0"
    s += " · nghiệm: " + (", ".join(L(r) for r in ng) or "vô nghiệm")
    if dk:
        s += " · NHẬN: " + (", ".join(L(r) for r in nhan) or "không") + " · LOẠI: " + (", ".join(L(r) for r in lo) or "không")
    return s


def tom_tat():
    """(dict nhãn → các dòng mô tả, danh sách trùng — trong phiếu B và với phiếu A)."""
    tt, gap, trung = {}, {}, []
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from so_do_phieu_a_9c import SO_DO as SO_DO_A, chuan as chuan_a
    for nhan, (_, _, _, y) in SO_DO_A.items():
        for i, (vt, vp, _, _) in enumerate(y):
            p = chuan_a(vt, vp)
            p = sp.Poly(p.as_expr() / sp.gcd_list(p.all_coeffs()), x)
            gap[tuple(p.all_coeffs())] = f"phiếu A {nhan} ý {i + 1}"
    for nhan, (muc, tier, nguon, y) in SO_DO.items():
        dong = []
        for i, (vt, vp, loai, ghi) in enumerate(y):
            _, p, *_ = chuan(vt, vp)
            key = tuple(p.all_coeffs())
            if key in gap and (nhan, i) not in CHO_TRUNG_A:
                trung.append(f"{nhan} ý {i + 1} trùng {gap[key]}")
            gap[key] = f"{nhan} ý {i + 1}"
            ten = chr(ord("a") + i) + ") " if len(y) > 1 else ""
            dong.append(f"{ten}[{loai}] {vt} = {vp} → {mo_ta(vt, vp, loai)}" + (f" · ({ghi})" if ghi else ""))
        tt[nhan] = dong
    return tt, trung


def main():
    tt, trung = tom_tat()
    for k, v in tt.items():
        print(k, f"(nguồn: {SO_DO[k][2]})" if SO_DO[k][2] else "")
        for d in v:
            print("   ", d)
    print("TRÙNG:", trung or "không")
    sys.exit(1 if trung else 0)


if __name__ == "__main__":
    main()
