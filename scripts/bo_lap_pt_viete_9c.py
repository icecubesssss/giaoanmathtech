#!/usr/bin/env python3
"""Cắt dạng "lập phương trình bậc hai nhận hai số làm nghiệm" khỏi phiếu C Viète ch.VI 9C,
thay bằng "biết một nghiệm, tìm nghiệm còn lại" (Câu III.3 đề minh họa của Sở GD&ĐT Hà Nội).

Thầy 12/11/2026: "phần lập phương trình bậc 2 có thi không? sao lại cho vào?" — 3 đề Sở
(minh họa, 2025, 2026) không có; lọt vào vì thuyết minh lấy từ bộ đề ôn Phòng GD Đống Đa.
Vị trí giữ nguyên (Bài 8, 15, 26, 32; hai Ví dụ 7; mục 3 Kiến thức cần nhớ) ⇒ không đánh số lại.
Mọi đáp số kiểm bằng SymPy trước khi ghi.

    .venv/bin/python scripts/bo_lap_pt_viete_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[1]
D = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
SEED, TM = D / "phieu-c-dinh-li-viete-va-ung-dung.json", D / "thuyet-minh.json"
x = sp.symbols("x")
T = r"[[br]]\hspace*{1.4em}"
DD = r"\ldots\ldots"


def kiem(pt, x1, x2, c_sym=None, c_val=None):
    """pt = 0 phải nhận x1, x2 làm nghiệm (thay c nếu có)."""
    e = pt.subs(c_sym, c_val) if c_sym is not None else pt
    for r in (x1, x2):
        assert sp.simplify(e.subs(x, r)) == 0, (pt, r)


a_, c_ = sp.symbols("a c")
# ---- kiểm số liệu ----
kiem(x**2 - 7*x + 10, 2, 5)                                      # Ví dụ 7 (LT1)
kiem(x**2 - 7*x + 12, 3, 4); kiem(x**2 + 2*x - 15, 3, -5); kiem(2*x**2 - 7*x + 3, 3, sp.Rational(1, 2))   # Bài 8
kiem(x**2 - 4*x + c_, 2 - sp.sqrt(3), 2 + sp.sqrt(3), c_, 1)     # Ví dụ 7 (LT2)
kiem(x**2 - 3*x + a_, (3 - sp.sqrt(5))/2, (3 + sp.sqrt(5))/2, a_, 1)   # Bài 15a — đề minh họa Sở
kiem(x**2 - 6*x + c_, 3 + sp.sqrt(2), 3 - sp.sqrt(2), c_, 7)     # Bài 15b
kiem(x**2 - 9*x + 14, 2, 7); kiem(x**2 + 3*x - 10, 2, -5); kiem(3*x**2 - 5*x + 2, 1, sp.Rational(2, 3))   # Bài 26
kiem(x**2 - 2*x + c_, 1 + sp.sqrt(5), 1 - sp.sqrt(5), c_, -4)    # Bài 32a
kiem(x**2 - 8*x + c_, 4 - sp.sqrt(7), 4 + sp.sqrt(7), c_, 9)     # Bài 32b

LG = r"{\sffamily\bfseries\color{brand}Lời giải}"
H = r"[[br]]\hspace*{1.4em}"

KT3_TIEU_DE = r"\textbf{3. Biết một nghiệm, tìm nghiệm còn lại}"
KT3_NOI_DUNG = (r"Nếu phương trình $ax^2+bx+c=0$ ($a \ne 0$) có một nghiệm là $x_1$ thì theo định lí Viète, "
                r"nghiệm còn lại là $x_2=-\dfrac{b}{a}-x_1$.[[br]]"
                r"Khi đề còn thiếu một hệ số, dùng tiếp $x_1x_2=\dfrac{c}{a}$ để tìm hệ số đó.")

VD7_LT1 = (r"\textbf{Ví dụ 7.} Biết phương trình $x^2-7x+10=0$ có một nghiệm $x_1=2$. Không giải phương trình, tìm nghiệm còn lại."
           f"[[br]]{LG}"
           f"{H}Vì phương trình có nghiệm $x_1=2$ nên theo định lí Viète, ta có $x_1+x_2=7$."
           f"{H}Suy ra $x_2=7-x_1=7-2=5$."
           f"{H}Vậy nghiệm còn lại của phương trình là $x_2=5$.")

VD7_LT2 = (r"\textbf{Ví dụ 7.} Biết phương trình $x^2-4x+c=0$ có một nghiệm $x_1=2-\sqrt3$. Tìm nghiệm còn lại và giá trị của $c$."
           f"[[br]]{LG}"
           f"{H}Vì phương trình có nghiệm $x_1=2-\\sqrt3$ nên theo định lí Viète, ta có $\\begin{{cases}} x_1+x_2=4\\\\ x_1x_2=c\\end{{cases}}$"
           f"{H}Suy ra $x_2=4-x_1=4-(2-\\sqrt3)=2+\\sqrt3$."
           f"{H}$c=x_1x_2=(2-\\sqrt3)(2+\\sqrt3)=4-3=1$."
           f"{H}Vậy nghiệm còn lại là $x_2=2+\\sqrt3$ và $c=1$.")


def nb_dien(nhan, pt, x1, tong, x2):
    de = (f"{nhan}) [NB] ${pt}$, nghiệm $x_1={x1}$"
          f"{T}Vì phương trình có nghiệm $x_1={x1}$ nên theo định lí Viète, ta có $x_1+x_2={DD}$"
          f"{T}Suy ra $x_2={DD}-{x1}={DD}$"
          f"{T}Vậy nghiệm còn lại là $x_2={DD}$.")
    giai = (f"{nhan}) Vì phương trình có nghiệm $x_1={x1}$ nên theo định lí Viète, ta có $x_1+x_2={tong}$."
            f"{T}Suy ra $x_2={tong}-{x1}={x2}$."
            f"{T}Vậy nghiệm còn lại là $x_2={x2}$.")
    return de, giai


def nb_tu(nhan, pt, x1, tong, x2):
    _, giai = nb_dien(nhan, pt, x1, tong, x2)
    return f"{nhan}) [NB] ${pt}$, nghiệm $x_1={x1}$", giai


def th(nhan, de_dong, x1, tong, x2_bt, x2, he, tich_bt, gia_tri, nguon=""):
    de = f"{nhan}) [TH] {de_dong}{nguon}"
    giai = (f"{nhan}) Vì phương trình có nghiệm $x_1={x1}$ nên theo định lí Viète, ta có "
            f"$\\begin{{cases}} x_1+x_2={tong}\\\\ x_1x_2={he}\\end{{cases}}$"
            f"{T}Suy ra $x_2={tong}-x_1={x2_bt}={x2}$."
            f"{T}${he}=x_1x_2={tich_bt}={gia_tri}$."
            f"{T}Vậy nghiệm còn lại là $x_2={x2}$ và ${he}={gia_tri}$.")
    return de, giai


def ghep(dan, cap):
    return "[[br]]".join([dan] + [d for d, _ in cap]), "[[br]]".join(g for _, g in cap)


BAI = {
    "Bài 8.": ghep(r"Điền vào chỗ chấm để tìm nghiệm còn lại của mỗi phương trình sau khi biết một nghiệm (làm đủ các bước như Ví dụ 7).",
                   [nb_dien("a", "x^2-7x+12=0", "3", "7", "4"),
                    nb_dien("b", "x^2+2x-15=0", "3", "-2", "-5"),
                    nb_dien("c", r"2x^2-7x+3=0", "3", r"\dfrac{7}{2}", r"\dfrac{1}{2}")]),
    "Bài 15.": ghep(r"Tìm nghiệm còn lại của phương trình và giá trị của hệ số còn thiếu.",
                    [th("a", r"Biết phương trình $x^2-3x+a=0$ có một nghiệm là $x_1=\dfrac{3-\sqrt5}{2}$",
                        r"\dfrac{3-\sqrt5}{2}", "3", r"3-\dfrac{3-\sqrt5}{2}", r"\dfrac{3+\sqrt5}{2}", "a",
                        r"\dfrac{3-\sqrt5}{2}\cdot\dfrac{3+\sqrt5}{2}=\dfrac{9-5}{4}", "1",
                        r" \;(đề minh họa Vào 10, Sở GD\&ĐT Hà Nội)"),
                     th("b", r"Biết phương trình $x^2-6x+c=0$ có một nghiệm là $x_1=3+\sqrt2$",
                        r"3+\sqrt2", "6", r"6-(3+\sqrt2)", r"3-\sqrt2", "c",
                        r"(3+\sqrt2)(3-\sqrt2)=9-2", "7")]),
    "Bài 26.": ghep(r"Biết một nghiệm của mỗi phương trình sau. Không giải phương trình, tìm nghiệm còn lại.",
                    [nb_tu("a", "x^2-9x+14=0", "2", "9", "7"),
                     nb_tu("b", "x^2+3x-10=0", "2", "-3", "-5"),
                     nb_tu("c", "3x^2-5x+2=0", "1", r"\dfrac{5}{3}", r"\dfrac{2}{3}")]),
    "Bài 32.": ghep(r"Tìm nghiệm còn lại của phương trình và giá trị của hệ số còn thiếu.",
                    [th("a", r"Biết phương trình $x^2-2x+c=0$ có một nghiệm là $x_1=1+\sqrt5$",
                        r"1+\sqrt5", "2", r"2-(1+\sqrt5)", r"1-\sqrt5", "c", r"(1+\sqrt5)(1-\sqrt5)=1-5", "-4"),
                     th("b", r"Biết phương trình $x^2-8x+c=0$ có một nghiệm là $x_1=4-\sqrt7$",
                        r"4-\sqrt7", "8", r"8-(4-\sqrt7)", r"4+\sqrt7", "c", r"(4-\sqrt7)(4+\sqrt7)=16-7", "9")]),
}


def main():
    d = json.loads(SEED.read_text())
    da = set()
    for s in d["stages"]:
        bl = s["blocks"]
        for i, b in enumerate(bl):
            t = b.get("text", "")
            if t.startswith(r"\textbf{3. Lập phương trình bậc hai"):
                b["text"] = KT3_TIEU_DE
                assert "Hai số $u$" in bl[i + 1]["text"]
                bl[i + 1]["text"] = KT3_NOI_DUNG
                da.add("KT3")
            elif t.startswith(r"\textbf{Ví dụ 7.} Lập phương trình bậc hai nhận $3$"):
                b["text"] = VD7_LT1; da.add("VD7a")
            elif t.startswith(r"\textbf{Ví dụ 7.} Lập phương trình bậc hai nhận $5+"):
                b["text"] = VD7_LT2; da.add("VD7b")
            elif b.get("label") in BAI:
                assert "Lập phương trình" in b["statement"], b["label"]
                b["statement"], b["solution"] = BAI[b["label"]]
                if b.get("hints"):
                    b["hints"] = []
                da.add(b["label"])
    assert da == {"KT3", "VD7a", "VD7b", *BAI}, da
    # Đích "Đích thi Vào 10" / ghi chú GV có nhắc dạng cũ?
    for s in d["stages"]:
        for k in ("teacher_note",):
            if "ập phương trình" in s.get(k, ""):
                print("!! teacher_note còn nhắc:", s[k][:160])

    tm = json.loads(TM.read_text())
    tm["lythuyet"] = [l.replace("Lập phương trình bậc hai khi biết hai nghiệm.", "Biết một nghiệm, tìm nghiệm còn lại.")
                      for l in tm["lythuyet"]]
    tm["dang_vd"] = [l.replace("Câu III.3 — lập phương trình bậc hai nhận hai số chứa căn làm nghiệm, dạng ngược — $0{,}5$ điểm (bộ đề Đống Đa).",
                               "Câu III.3 — biết một nghiệm (chứa căn), tìm nghiệm còn lại và hệ số còn thiếu — $0{,}5$ điểm (đề minh họa của Sở).")
                     for l in tm["dang_vd"]]
    rows = tm["phieu"][2]["rows"]
    for r in rows:
        if r["dang"].startswith("Lập phương trình bậc hai khi biết trước hai nghiệm"):
            r["dang"] = "Biết một nghiệm, tìm nghiệm còn lại bằng tổng hai nghiệm"
            r["source_refs"] = ["so-hn-minhhoa-III3"]
        elif r["dang"].startswith("Lập phương trình bậc hai nhận $2x_1+1$"):
            r["dang"] = "Biết một nghiệm chứa căn, tìm nghiệm còn lại và hệ số còn thiếu"
            r["source_refs"] = ["so-hn-minhhoa-III3"]

    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        TM.write_text(json.dumps(tm, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi seed + thuyết minh")
    else:
        print("Chạy thử OK (thêm --ghi để ghi).")


if __name__ == "__main__":
    main()
