#!/usr/bin/env python3
"""Dựng lại khung điền khuyết (NB) + lời giải theo ĐÚNG các bước của ví dụ mẫu — phiếu C Viète ch.VI 9C.

Thầy 12/11/2026: "VD mẫu đang không giống cách trình bày của điền khuyết, HS bị quên bước xét Delta
hoặc tính ac < 0 để kết luận". Mỗi ý giờ đi đủ 4 bước như ví dụ:
    (1) Ta có ac … < 0 / Δ … > 0 nên phương trình có hai nghiệm phân biệt.
    (2) Theo định lí Viète, ta có {x1+x2 = …, x1x2 = …}
    (3) tính biểu thức          (4) Vậy …
Số liệu tính bằng SymPy (không gõ tay). Bài trên lớp: khung điền; BTVN: chỉ đề, lời giải đủ bước.

    .venv/bin/python scripts/khung_viete_9c.py [--ghi]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[1]
SEED = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
r2, r3, r5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
D = r"\ldots\ldots"
T = r"[[br]]\hspace*{1.4em}"


def L(v) -> str:
    v = sp.nsimplify(v) if v.is_Rational else v
    if isinstance(v, sp.Add):  # hạng tử dương (căn) trước, hằng âm sau: √3 − 1, không −1 + √3
        terms = sorted(v.as_ordered_terms(), key=lambda t: (t.could_extract_minus_sign(), t.is_Number))
        s = ""
        for t in terms:
            lt = L(-t) if t.could_extract_minus_sign() else L(t)
            s += ("-" if t.could_extract_minus_sign() else ("+" if s else "")) + lt
        return s
    s = sp.latex(v)
    s = s.replace(r"\frac", r"\dfrac").replace(r"\sqrt{2}", r"\sqrt2").replace(r"\sqrt{3}", r"\sqrt3").replace(r"\sqrt{5}", r"\sqrt5")
    return re.sub(r"\s+", "", s)


def P(v) -> str:
    """Số trong biểu thức: bọc ngoặc khi âm hoặc là tổng/phân số."""
    s = L(v)
    if (v.is_number and v.is_negative) or isinstance(v, sp.Add) or (v.is_Rational and not v.is_Integer):
        return rf"\left({s}\right)" if r"\dfrac" in s else f"({s})"
    return s


def dieu_kien(a, b, c, dien: bool) -> str:
    ac = sp.simplify(a * c)
    if ac.is_negative:
        if dien:
            return rf"Ta có $ac={D}<0$ nên phương trình có hai nghiệm phân biệt."
        return rf"Ta có $ac={P(a) if a != 1 else '1'}\cdot{P(c)}={L(ac)}<0$ nên phương trình có hai nghiệm phân biệt."
    delta = sp.expand(b**2 - 4 * a * c)
    assert delta.is_positive, (a, b, c, delta)
    if dien:
        return rf"Ta có $\Delta={D}>0$ nên phương trình có hai nghiệm phân biệt."
    vi = ""
    if not delta.is_Rational:  # 7-4√3 …: chỉ rõ vì sao dương
        vi = {sp.expand(7 - 4 * r3): r" (vì $4\sqrt3=\sqrt{48}<\sqrt{49}=7$)",
              sp.expand(28 - 16 * r3): r" (vì $16\sqrt3=\sqrt{768}<\sqrt{784}=28$)"}[delta]
    return rf"Ta có $\Delta={P(b)}^2-4\cdot{P(a)}\cdot{P(c)}={L(delta)}>0$ nên phương trình có hai nghiệm phân biệt{vi}."


def viete(S, Pp, dien: bool) -> str:
    s, p = (D, D) if dien else (L(S), L(Pp))
    return rf"Theo định lí Viète, ta có $\begin{{cases}} x_1+x_2={s}\\ x_1x_2={p}\end{{cases}}$"


def buoc(kind, S, Pp, dien: bool) -> list[str]:
    v = lambda x: D if dien else x
    if kind == "tongtich":
        return [rf"Vậy tổng hai nghiệm bằng {D if dien else '$' + L(S) + '$'} và tích hai nghiệm bằng {D if dien else '$' + L(Pp) + '$'}."]
    if kind == "binhphuong":
        val = sp.simplify(S**2 - 2 * Pp)
        return [rf"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2={v(P(S) + '^2-2' + chr(92) + 'cdot' + P(Pp) + '=' + L(val))}$",
                rf"Vậy $x_1^2+x_2^2={v(L(val))}$."]
    if kind == "lapphuong":
        val = sp.simplify(S**3 - 3 * Pp * S)
        return [rf"$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)={v(P(S) + '^3-3' + chr(92) + 'cdot' + P(Pp) + chr(92) + 'cdot' + P(S) + '=' + L(val))}$",
                rf"Vậy $x_1^3+x_2^3={v(L(val))}$."]
    if kind == "hieubp":
        val = sp.simplify(S**2 - 4 * Pp)
        return [rf"$(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2={v(P(S) + '^2-4' + chr(92) + 'cdot' + P(Pp) + '=' + L(val))}$",
                rf"Vậy $(x_1-x_2)^2={v(L(val))}$."]
    if kind == "nghichdao":
        val = sp.simplify(S / Pp)
        ts, ms = L(S).replace(r"\dfrac", r"\frac"), L(Pp).replace(r"\dfrac", r"\frac")
        mid = rf"\dfrac{{{ts}}}{{{ms}}}"
        if not (S.is_Integer and Pp.is_Integer and sp.gcd(S, Pp) == 1 and Pp > 0):
            mid += f"={L(val)}"
        return [rf"Vì $x_1x_2={v(L(Pp))}\ne 0$ nên $x_1\ne 0$ và $x_2\ne 0$.",
                rf"$\dfrac{{1}}{{x_1}}+\dfrac{{1}}{{x_2}}=\dfrac{{x_1+x_2}}{{x_1x_2}}={v(mid)}$",
                rf"Vậy $\dfrac{{1}}{{x_1}}+\dfrac{{1}}{{x_2}}={v(L(val))}$."]
    if kind == "xetdau":
        if Pp < 0:
            return [rf"Vì $x_1x_2{D if dien else '<'}0$ nên hai nghiệm {D if dien else 'trái dấu'}."]
        dau = "cùng dương" if S > 0 else "cùng âm"
        return [rf"Vì $x_1x_2{D if dien else '>'}0$ và $x_1+x_2{D if dien else ('>' if S > 0 else '<')}0$ nên hai nghiệm {D if dien else dau}."]
    raise ValueError(kind)


def y(nhan, header, abc, kind, dien):
    a, b, c = (sp.nsimplify(t) for t in abc)
    S, Pp = sp.simplify(-b / a), sp.simplify(c / a)
    dong = [dieu_kien(a, b, c, dien), viete(S, Pp, dien)] + buoc(kind, S, Pp, dien)
    return header, (f"{nhan}) " + T.join(dong))


# (label, câu dẫn, kind, trên lớp?, [(dòng a) giữ nguyên nguồn, (a, b, c))])
NB = "[NB] "
BAI = [
    ("Bài 1.", r"Điền vào chỗ chấm để viết tổng và tích hai nghiệm của mỗi phương trình sau (làm đủ các bước như Ví dụ 1).",
     "tongtich", True, [("$x^2-3x+1=0$", (1, -3, 1)), ("$2x^2-4x+1=0$", (2, -4, 1)), ("$x^2+x-6=0$", (1, 1, -6))]),
    ("Bài 3.", r"Điền vào chỗ chấm để viết tổng và tích hai nghiệm $x_1, x_2$ của mỗi phương trình sau.[[br]](Gợi ý: chú ý dấu của $b$ và $c$.)",
     "tongtich", True, [("$x^2-3x-5=0$", (1, -3, -5)), (r"$x^2-8x-5=0$ \;(thi thử Vào 10, cụm THCS công lập Hà Nội)", (1, -8, -5)),
                        ("$x^2-10x+4=0$", (1, -10, 4))]),
    ("Bài 4.", r"Điền vào chỗ chấm để tính $x_1^2+x_2^2$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau (làm đủ các bước như Ví dụ 3).",
     "binhphuong", True, [("$x^2-3x+1=0$", (1, -3, 1)), ("$x^2-8x-5=0$", (1, -8, -5)), ("$x^2+x-6=0$", (1, 1, -6))]),
    ("Bài 5.", r"Tính giá trị biểu thức $\dfrac{1}{x_1}+\dfrac{1}{x_2}$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 4).",
     "nghichdao", True, [(r"$2x^2-4x+1=0$ \;(thi thử Vào 10 lần 1, THCS Cầu Giấy)", (2, -4, 1)), ("$x^2-7x+2=0$", (1, -7, 2)),
                         ("$x^2-6x+3=0$", (1, -6, 3))]),
    ("Bài 6.", r"Điền vào chỗ chấm để tính $x_1^3+x_2^3$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau (làm đủ các bước như Ví dụ 5).",
     "lapphuong", True, [("$x^2-3x-5=0$", (1, -3, -5)), ("$x^2-3x+1=0$", (1, -3, 1)), ("$x^2+x-6=0$", (1, 1, -6))]),
    ("Bài 7.", r"Tính giá trị biểu thức $(x_1-x_2)^2$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 6).",
     "hieubp", True, [(r"$x^2-3x-1=0$ \;(thi thử Vào 10 lần 3, Phòng GD\&ĐT Ứng Hòa)", (1, -3, -1)), ("$x^2-3x+1=0$", (1, -3, 1)),
                      ("$x^2+x-6=0$", (1, 1, -6))]),
    ("Bài 9.", r"Điền vào chỗ chấm để viết tổng và tích hai nghiệm của mỗi phương trình sau (hệ số chứa căn, làm đủ các bước như Ví dụ 1).",
     "tongtich", True, [(r"$x^2+x-2+\sqrt2=0$ \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)", (1, 1, -2 + r2)),
                        (r"$x^2-2\sqrt5\,x+4=0$", (1, -2 * r5, 4)),
                        (r"$x^2-\sqrt3\,x+\sqrt3-1=0$ \;(Giữa kì II, xã Đông Anh)", (1, -r3, r3 - 1))]),
    ("Bài 11.", r"Điền vào chỗ chấm để xét dấu hai nghiệm của mỗi phương trình sau mà không giải phương trình.",
     "xetdau", True, [("$x^2-8x-5=0$", (1, -8, -5)), (r"$x^2+10x+4=0$ \;(thi thử Vào 10, THCS Tự Lập)", (1, 10, 4))]),
    # BTVN: HS tự trình bày, đề nhắc kiểm tra điều kiện; lời giải đủ 4 bước
    ("Bài 19.", r"Kiểm tra điều kiện có hai nghiệm rồi viết tổng và tích hai nghiệm của mỗi phương trình.",
     "tongtich", False, [(r"$x^2-3x-1=0$ \;(thi thử Vào 10 lần 3, Phòng GD\&ĐT Ứng Hòa)", (1, -3, -1)),
                         (r"$x^2+10x+4=0$ \;(thi thử Vào 10, THCS Tự Lập)", (1, 10, 4)), ("$5x^2-21x-54=0$", (5, -21, -54))]),
    ("Bài 21.", r"Kiểm tra điều kiện có hai nghiệm rồi viết tổng và tích hai nghiệm.",
     "tongtich", False, [("$x^2-3x-1=0$", (1, -3, -1)), (r"$2x^2-x-5=0$ \;(Cuối kì II, Phòng GD\&ĐT Ba Đình)", (2, -1, -5))]),
    ("Bài 22.", r"Không giải phương trình, tính $x_1^2+x_2^2$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau.",
     "binhphuong", False, [("$x^2-3x-1=0$", (1, -3, -1)), ("$2x^2-x-5=0$", (2, -1, -5))]),
    ("Bài 23.", r"Tính tổng nghịch đảo hai nghiệm $\dfrac{1}{x_1}+\dfrac{1}{x_2}$ của mỗi phương trình sau (kiểm tra điều kiện có hai nghiệm và $x_1x_2 \ne 0$ trước).",
     "nghichdao", False, [("$x^2-3x-5=0$", (1, -3, -5)), ("$2x^2-x-5=0$", (2, -1, -5))]),
    ("Bài 24.", r"Không giải phương trình, tính $x_1^3+x_2^3$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau.",
     "lapphuong", False, [("$x^2-3x-1=0$", (1, -3, -1)), ("$x^2+3x+1=0$", (1, 3, 1))]),
    ("Bài 25.", r"Không giải phương trình, tính $(x_1-x_2)^2$, trong đó $x_1, x_2$ là hai nghiệm của mỗi phương trình sau.",
     "hieubp", False, [("$x^2-8x-5=0$", (1, -8, -5)), ("$2x^2-4x+1=0$", (2, -4, 1))]),
    ("Bài 27.", r"Kiểm tra điều kiện có hai nghiệm rồi viết tổng và tích hai nghiệm (hệ số chứa căn).",
     "tongtich", False, [(r"$x^2-2\sqrt3\,x+2=0$", (1, -2 * r3, 2)), (r"$x^2+4x+4\sqrt3-3=0$ \;(Giữa kì II, xã Đông Anh)", (1, 4, 4 * r3 - 3)),
                         (r"$x^2-\sqrt2\,x-1=0$", (1, -r2, -1))]),
    ("Bài 28.", r"Xét dấu hai nghiệm mà không giải phương trình (kiểm tra điều kiện có hai nghiệm trước).",
     "xetdau", False, [("$x^2+x-6=0$", (1, 1, -6)), ("$x^2-7x+6=0$", (1, -7, 6))]),
]


def dung(label, dan, kind, tren_lop, ds):
    st, so = [dan], []
    for i, (hd, abc) in enumerate(ds):
        n = "abc"[i]
        _, de = y(n, hd, abc, kind, dien=True)
        _, giai = y(n, hd, abc, kind, dien=False)
        st.append(f"{n}) {NB}{hd}" + (T + de.split(") ", 1)[1] if tren_lop else ""))
        so.append(giai)
    return "[[br]]".join(st), "[[br]]".join(so)


def main():
    d = json.loads(SEED.read_text())
    blocks = {b["label"]: b for s in d["stages"] for b in s["blocks"] if b.get("type") == "problem"}
    for label, dan, kind, tren_lop, ds in BAI:
        b = blocks[label]
        b["statement"], b["solution"] = (re.sub(r"\\ldots\\ldots (?=[^\s$\[\\])", r"\\ldots\\ldots\\ ", x) for x in dung(label, dan, kind, tren_lop, ds))
    # Ví dụ 1: bước điều kiện cùng khuôn với khung
    for s in d["stages"]:
        for b in s["blocks"]:
            t = b.get("text", "")
            if t.startswith(r"\textbf{Ví dụ 1.}"):
                cu = re.search(r"Ta có \$a=1\$.*?phân biệt\.", t)
                if cu:
                    b["text"] = t.replace(cu.group(0), r"Ta có $ac=1\cdot(-3)=-3<0$ nên phương trình có hai nghiệm phân biệt.")
    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi", SEED.relative_to(REPO))
    else:
        for label, *_ in BAI[:1] + BAI[3:4] + BAI[6:8]:
            print(label, blocks[label]["statement"], "\nSOL:", blocks[label]["solution"], "\n")


if __name__ == "__main__":
    main()
