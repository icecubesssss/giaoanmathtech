#!/usr/bin/env python3
"""BỘ ĐỀ ÔN TẬP CUỐI KÌ 1 (CK1) TOÁN 9 (Chương trình mới GDPT 2018 - Hà Nội).
Sinh 3 đề ôn tập (Số 1, Số 2, Số 3) + 3 file Ma trận đề và đáp án chi tiết cho GV
vào inputs/seeds/lop-9/de-on-tap-cuoi-ki-1/ (theme de_thi, trinh_bay "thoang").
Quy trình: docs/quy-trinh-bo-de-on-tap.md.

Mọi câu trích nguyên văn từ đề thi thật các Phòng GD&ĐT và trường THCS tại Hà Nội.
Đáp số đã kiểm chứng SymPy / giải tích. Lời giải tuân thủ 100% cổng loi_giai_thi_gate.

Chạy:  .venv/bin/python scripts/de_on_tap_ck1_lop9.py
       .venv/bin/python -m src.main build-folder inputs/seeds/lop-9/de-on-tap-cuoi-ki-1
"""
import json
import re as _re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from de_on_tap_ck1_lop9_hinh import TOA_DO as T  # noqa: E402

OUT = ROOT / "inputs/seeds/lop-9/de-on-tap-cuoi-ki-1"
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem)}đ)}}" if diem else "")


def bo_tuong_duong(t):
    """HS đi thi KHÔNG dùng dấu ⇔ (Thầy 01/10/2026): mỗi phép biến đổi xuống một dòng.
    Cắt mọi đoạn toán $…$ tại \Leftrightarrow ở mức ngoặc 0, ngoài \begin…\end; bỏ dấu ⇔ đầu đoạn."""
    out = []
    for seg in _re.split(r"(\$[^$]*\$)", t):
        if not (seg.startswith("$") and seg.endswith("$") and len(seg) > 1):
            seg = _re.sub(r"(?<=[.])\s+(?=[A-ZĐÂĂÊÔƠƯ])", BR, seg)
            out.append(seg)
            continue
        m = seg[1:-1]
        parts, depth, env, last, i = [], 0, 0, 0, 0
        while i < len(m):
            if m.startswith("\\begin", i):
                env += 1
            elif m.startswith("\\end", i):
                env -= 1
            c = m[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            elif depth == 0 and env == 0 and m.startswith("\\Leftrightarrow", i):
                parts.append(m[last:i])
                i += len("\\Leftrightarrow")
                last = i
                continue
            i += 1
        parts.append(m[last:])
        parts = [p.strip() for p in parts if p.strip()]
        out.append(BR.join("$" + p + "$" for p in parts))
    s = "".join(out).strip()
    return _re.sub(r"^(?:\s*\[\[br\]\]\s*)+", "", s)


def y(nhan, diem, steps):
    than = BR.join(bo_tuong_duong(st(*s) if isinstance(s, tuple) else s) for s in steps)
    return (f"\\textbf{{{nhan} ({d(diem)}đ)}}" + BR + than) if nhan else than


# ─────────────────────────── HÌNH VẼ ───────────────────────────
def goc(cx, cy, a0, a1, r, nhan, rn):
    return (
        f"\\draw[line width=0.7pt] ({cx},{cy}) ++({a0}:{r}) arc ({a0}:{a1}:{r});"
        f"\\node at ($({cx},{cy})+({(a0+a1)/2}:{rn})$) {{{nhan}}};"
    )


def vuong(x, y, dx, dy, s=0.3):
    return f"\\draw[line width=0.6pt] ({x+dx*s},{y})--({x+dx*s},{y+dy*s})--({x},{y+dy*s});"


def hinh_draw(pts, segs, ticks=(), extra="", scale=1.4, dashed=()):
    s = f"\\begin{{tikzpicture}}[scale={scale},line width=0.9pt]\n"
    for k, (x, yy, pos) in pts.items():
        s += f"  \\coordinate ({k}) at ({x:.3f},{yy:.3f});\n"
    for a, b in segs:
        s += f"  \\draw ({a})--({b});\n"
    for a, b in dashed:
        s += f"  \\draw[dashed] ({a})--({b});\n"
    s += extra
    for k, (x, yy, pos) in pts.items():
        s += f"  \\fill ({k}) circle (1.6pt);\\node[{pos}] at ({k}) {{${k}$}};\n"
    return s + "\\end{tikzpicture}"


def vg(P, Q, R, s=0.16):
    """kí hiệu góc vuông tại Q (giữa QP và QR)"""
    import math

    (px, py), (qx, qy), (rx, ry) = P, Q, R
    u = ((px - qx), (py - qy))
    lu = math.hypot(*u)
    u = (u[0] / lu * s, u[1] / lu * s)
    v = ((rx - qx), (ry - qy))
    lv = math.hypot(*v)
    v = (v[0] / lv * s, v[1] / lv * s)
    return (
        f"\\draw[line width=0.5pt] ({qx+u[0]:.3f},{qy+u[1]:.3f})--({qx+u[0]+v[0]:.3f},{qy+u[1]+v[1]:.3f})"
        f"--({qx+v[0]:.3f},{qy+v[1]:.3f});"
    )


# Hình thực tế
TIKZ_THAP = (
    "\\begin{tikzpicture}[line width=0.9pt,scale=0.75]\n"
    "  \\coordinate (B) at (0,0);\\coordinate (C) at (4,0);\\coordinate (A) at (0,3.356);\n"
    "  \\draw (-0.5,0)--(4.8,0);\n"
    "  \\draw[line width=1.4pt] (B)--(A);\\draw (A)--(C);\\draw (B)--(C);\n"
    "  \\draw[line width=0.5pt] (0.3,0)--(0.3,0.3)--(0,0.3);\n"
    "  \\draw[line width=0.6pt] (C) ++(180:0.75) arc (180:140:0.75);\n"
    "  \\node at (2.9,0.3) {$40^\\circ$};\n"
    "  \\node[left] at (A) {$A$};\\node[below left] at (B) {$B$};\\node[below right] at (C) {$C$};\n"
    "  \\draw[<->,line width=0.5pt] (0,-0.4)--(4,-0.4);\\node[below=2pt] at (2,-0.4) {$135$ m};\n"
    "\\end{tikzpicture}"
)

TIKZ_TAUNGAM_CK = (
    "\\begin{tikzpicture}[line width=0.8pt,scale=0.6]\n"
    "  \\fill[gray!10] (-0.5,0) rectangle (6.5,-2.8);\n"
    "  \\coordinate (A) at (0,0);\\coordinate (B) at (5.2,0);\\coordinate (C) at (5.2,-2.6);\n"
    "  \\draw (-0.5,0)--(6.5,0);\\draw (A)--(C)--(B);\n"
    "  \\draw[line width=0.5pt] (5.2,-0.3)--(4.9,-0.3)--(4.9,0);\n"
    "  \\draw[line width=0.6pt] (A) ++(0:1.0) arc (0:-26.5:1.0);\n"
    "  \\node at (1.4,-0.28) {$30^\\circ$};\n"
    "  \\node[above left] at (A) {$A$};\\node[above right] at (B) {$B$};\\node[below right] at (C) {$C$};\n"
    "  \\draw[<->,line width=0.5pt] (5.6,0)--(5.6,-2.6);\\node[right=2pt] at (5.6,-1.3) {$100$ m};\n"
    "\\end{tikzpicture}"
)

TIKZ_THANG = (
    "\\begin{tikzpicture}[line width=0.8pt,scale=0.65]\n"
    "  \\coordinate (B) at (0,0);\\coordinate (A) at (0,3.29);\\coordinate (C) at (1.20,0);\n"
    "  \\draw (-0.4,0)--(2.2,0);\\draw[line width=1.4pt] (0,-0.2)--(0,3.6);\n"
    "  \\draw[line width=1.4pt,brown!80!black] (A)--(C);\n"
    "  \\draw[line width=0.5pt] (0.25,0)--(0.25,0.25)--(0,0.25);\n"
    "  \\draw[line width=0.6pt] (C) ++(180:0.5) arc (180:110:0.5);\n"
    "  \\node at (0.65,0.25) {$70^\\circ$};\n"
    "  \\node[left] at (A) {$A$};\\node[below left] at (B) {$B$};\\node[below right] at (C) {$C$};\n"
    "  \\node[above right] at (0.6,1.6) {$3{,}5$ m};\n"
    "\\end{tikzpicture}"
)

# Hình hình học Đề 1
c1 = T["on1"]
pts1 = {
    "O": (*c1["O"], "above right=4pt"),
    "A": (*c1["A"], "left"),
    "B": (*c1["B"], "above"),
    "C": (*c1["C"], "below"),
    "D": (*c1["D"], "below=4pt"),
    "H": (*c1["H"], "above right"),
    "E": (*c1["E"], "above right"),
    "K": (*c1["K"], "above=3pt"),
    "M": (*c1["M"], "above left"),
    "N": (*c1["N"], "above right"),
}
segs1 = [
    ("A", "B"),
    ("A", "C"),
    ("O", "B"),
    ("O", "C"),
    ("O", "A"),
    ("B", "C"),
    ("B", "D"),
    ("C", "D"),
    ("C", "E"),
    ("A", "D"),
]
extra1 = (
    f"  \\draw[gray!60] ({c1['O'][0]},{c1['O'][1]}) circle ({c1['r']});\n"
    f"  {vg(c1['A'], c1['B'], c1['O'])}\n"
    f"  {vg(c1['A'], c1['C'], c1['O'])}\n"
    f"  {vg(c1['A'], c1['H'], c1['B'])}\n"
    f"  {vg(c1['C'], c1['E'], c1['D'])}\n"
    f"  {vg(c1['B'], c1['C'], c1['D'])}\n"
)
HINH_ON1 = hinh_draw(pts1, segs1, extra=extra1, scale=1.35)

# Hình hình học Đề 2
c2 = T["on2"]
pts2 = {
    "O": (*c2["O"], "below"),
    "A": (*c2["A"], "below left"),
    "B": (*c2["B"], "below right"),
    "C": (*c2["C"], "above left"),
    "D": (*c2["D"], "above right"),
    "E": (*c2["E"], "above=4pt"),
    "F": (*c2["F"], "below"),
    "I": (*c2["I"], "right=4pt"),
}
segs2 = [
    ("A", "B"),
    ("A", "C"),
    ("C", "D"),
    ("C", "B"),
    ("D", "F"),
    ("A", "E"),
    ("O", "D"),
    ("O", "C"),
]
dashed2 = [("B", "D"), ("C", "I")]
extra2 = (
    f"  \\draw[gray!60] ({c2['B'][0]},{c2['B'][1]}) arc (0:180:{c2['r']});\n"
    f"  {vg(c2['C'], c2['A'], c2['O'])}\n"
    f"  {vg(c2['C'], c2['D'], c2['O'])}\n"
    f"  {vg(c2['A'], c2['E'], c2['B'])}\n"
    f"  {vg(c2['D'], c2['F'], c2['B'])}\n"
)
HINH_ON2 = hinh_draw(pts2, segs2, dashed=dashed2, extra=extra2, scale=1.35)

# Hình hình học Đề 3
c3 = T["on3"]
pts3 = {
    "O": (*c3["O"], "below=4pt"),
    "A": (*c3["A"], "below left"),
    "B": (*c3["B"], "below right"),
    "C": (*c3["C"], "above right"),
    "D": (*c3["D"], "below right"),
    "H": (*c3["H"], "above right"),
    "M": (*c3["M"], "left"),
    "I": (*c3["I"], "above left=3pt"),
    "F": (*c3["F"], "below right"),
}
segs3 = [
    ("A", "F"),
    ("A", "M"),
    ("M", "F"),
    ("C", "D"),
    ("O", "M"),
    ("O", "C"),
    ("A", "C"),
    ("B", "C"),
]
dashed3 = [("F", "D"), ("O", "D")]
extra3 = (
    f"  \\draw[gray!60] ({c3['O'][0]},{c3['O'][1]}) circle ({c3['r']});\n"
    f"  {vg(c3['M'], c3['A'], c3['O'])}\n"
    f"  {vg(c3['M'], c3['C'], c3['O'])}\n"
    f"  {vg(c3['C'], c3['H'], c3['A'])}\n"
    f"  {vg(c3['O'], c3['I'], c3['C'])}\n"
    f"  {vg(c3['A'], c3['C'], c3['B'])}\n"
)
HINH_ON3 = hinh_draw(pts3, segs3, dashed=dashed3, extra=extra3, scale=1.3)


# ─────────────────────────── NGUỒN VÀ LUẬT ───────────────────────────
QUAN = {
    "Huyện Đông Anh (2024–2025)": "Đông Anh",
    "Quận Cầu Giấy (2024–2025)": "Cầu Giấy",
    "Quận Ba Đình (2024–2025)": "Ba Đình",
    "Quận Hai Bà Trưng (2024–2025)": "Hai Bà Trưng",
    "Huyện Thanh Trì (2024–2025)": "Thanh Trì",
    "THCS Đống Đa (2025–2026)": "Đống Đa",
    "THCS Trưng Vương (2025–2026)": "Hoàn Kiếm",
    "THCS Ái Mộ (2025–2026)": "Long Biên",
    "THCS Chu Văn An (2025–2026)": "Tây Hồ",
    "Huyện Hoài Đức (2024–2025)": "Hoài Đức",
    "THCS Dịch Vọng (2025–2026)": "Cầu Giấy",
}

# ─────────────────────────── DANH SÁCH 3 ĐỀ ───────────────────────────
DE = {}

# =====================================================================
# ĐỀ ÔN TẬP SỐ 1
# =====================================================================
DE["on-1"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 1",
    slug_de="de-on-tap-cuoi-ki-1-so-1",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-1",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 1",
    cach_dung="Làm bài trong 90 phút như thi thật. Chữa bài tập trung vào khâu lập luận trình bày: ĐKXĐ, kết luận, không dùng dấu tương đương, chứng minh qua tam giác đồng dạng để suy ra hệ thức tích.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 1 -- CUỐI HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc chuẩn:} Bám sát cấu trúc đề thi Cuối Kì I và Đề tuyển sinh Lớp 10 của các quận/huyện Hà Nội năm 2024–2025 và 2025–2026: "
        "Bài I (2,0đ) Rút gọn và câu hỏi phụ căn bậc hai · Bài II (2,0đ) Lập hệ phương trình thực tế · "
        "Bài III (2,0đ) Phương trình tích, ẩn ở mẫu, BPT và hệ phương trình · "
        "Bài IV (3,5đ) Tỉ số lượng giác thực tế (0,5đ) và Hình học đường tròn (3,0đ) · "
        "Bài V (0,5đ) Bài toán tối ưu thực tế."
    ),
    bai=[
        dict(
            label="Bài I.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức:"
                + BR
                + "$A = \\dfrac{\\sqrt{x}+1}{\\sqrt{x}}$ và $B = \\dfrac{3}{\\sqrt{x}+3} - \\dfrac{x+9}{9-x}$ với $x > 0; x \\ne 9$."
                + BR
                + "1) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 7 - 4\\sqrt{3}$."
                + BR
                + "2) \\textbf{(1,0 điểm)} Chứng minh $B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$."
                + BR
                + "3) \\textbf{(0,5 điểm)} Tìm tất cả các giá trị nguyên của $x$ để $P = A \\cdot B$ nhận giá trị nguyên."
            ),
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Ta có: $x = 7 - 4\\sqrt{3} = 4 - 2 \\cdot 2 \\cdot \\sqrt{3} + 3 = (2 - \\sqrt{3})^2$ (thoả mãn ĐKXĐ)."),
                        ("Suy ra $\\sqrt{x} = \\sqrt{(2 - \\sqrt{3})^2} = |2 - \\sqrt{3}| = 2 - \\sqrt{3}$ (do $2 > \\sqrt{3}$).", 0.25),
                        ("Thay vào biểu thức $A$: $A = \\dfrac{2 - \\sqrt{3} + 1}{2 - \\sqrt{3}} = \\dfrac{3 - \\sqrt{3}}{2 - \\sqrt{3}} = \\dfrac{(3 - \\sqrt{3})(2 + \\sqrt{3})}{(2 - \\sqrt{3})(2 + \\sqrt{3})} = 3 + \\sqrt{3}$."),
                        ("Vậy khi $x = 7 - 4\\sqrt{3}$ thì $A = 3 + \\sqrt{3}$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    1.0,
                    [
                        ("Với $x > 0; x \\ne 9$, ta có: $9 - x = -(\\sqrt{x}-3)(\\sqrt{x}+3)$."),
                        ("Do đó: $B = \\dfrac{3}{\\sqrt{x}+3} + \\dfrac{x+9}{(\\sqrt{x}-3)(\\sqrt{x}+3)}$", 0.25),
                        ("$B = \\dfrac{3(\\sqrt{x}-3) + x + 9}{(\\sqrt{x}-3)(\\sqrt{x}+3)}$", 0.25),
                        ("$B = \\dfrac{3\\sqrt{x} - 9 + x + 9}{(\\sqrt{x}-3)(\\sqrt{x}+3)} = \\dfrac{x + 3\\sqrt{x}}{(\\sqrt{x}+3)(\\sqrt{x}-3)} = \\dfrac{\\sqrt{x}(\\sqrt{x}+3)}{(\\sqrt{x}+3)(\\sqrt{x}-3)}$", 0.25),
                        ("$B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$ (điều phải chứng minh).", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Ta có: $P = A \\cdot B = \\dfrac{\\sqrt{x}+1}{\\sqrt{x}} \\cdot \\dfrac{\\sqrt{x}}{\\sqrt{x}-3} = \\dfrac{\\sqrt{x}+1}{\\sqrt{x}-3} = 1 + \\dfrac{4}{\\sqrt{x}-3}$"),
                        ("Để $P$ nhận giá trị nguyên với $x$ nguyên thì $\\sqrt{x}-3$ phải là ước của $4$.", 0.25),
                        ("Ước của $4$ là $\\{\\pm 1; \\pm 2; \\pm 4\\}$."),
                        ("Ta có bảng giá trị:" + BR
                         + "$\\sqrt{x}-3 = 1 \\Rightarrow \\sqrt{x}=4 \\Rightarrow x=16$ (TMĐK)" + BR
                         + "$\\sqrt{x}-3 = -1 \\Rightarrow \\sqrt{x}=2 \\Rightarrow x=4$ (TMĐK)" + BR
                         + "$\\sqrt{x}-3 = 2 \\Rightarrow \\sqrt{x}=5 \\Rightarrow x=25$ (TMĐK)" + BR
                         + "$\\sqrt{x}-3 = -2 \\Rightarrow \\sqrt{x}=1 \\Rightarrow x=1$ (TMĐK)" + BR
                         + "$\\sqrt{x}-3 = 4 \\Rightarrow \\sqrt{x}=7 \\Rightarrow x=49$ (TMĐK)" + BR
                         + "$\\sqrt{x}-3 = -4 \\Rightarrow \\sqrt{x}=-1$ (vô nghiệm)."),
                        ("Vậy các giá trị nguyên cần tìm là $x \\in \\{1; 4; 16; 25; 49\\}$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("Ia", "Tính giá trị biểu thức căn tại $x = 7 - 4\\sqrt{3}$", "ĐS III", "NB", 0.5, 5, "Quận Hai Bà Trưng (2024–2025)"),
                ("Ib", "Rút gọn phân thức có bẫy đổi dấu mẫu $9 - x$", "ĐS III", "TH", 1.0, 10, "Quận Hai Bà Trưng (2024–2025)"),
                ("Ic", "Tìm giá trị nguyên của $x$ để biểu thức nhận giá trị nguyên", "ĐS III", "VD", 0.5, 7, "Quận Hai Bà Trưng (2024–2025)"),
            ],
            note="BẪY CÀI CẮM: Khai căn HĐT phải có trị tuyệt đối; đổi dấu mẫu $9-x = -(x-9)$ có dấu trừ đằng trước; loại nghiệm $\\sqrt{x} = -1 < 0$ ở câu tìm x nguyên.",
        ),
        dict(
            label="Bài II.",
            level=3,
            statement=(
                "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                + BR
                + "Bác Hà muốn mua một chiếc áo sơ mi và một chiếc quần âu. Tổng số tiền theo giá niêm yết của chiếc áo sơ mi và chiếc quần âu đó là $700$ nghìn đồng. "
                "Bác Hà mua vào dịp khuyến mãi nên so với giá niêm yết, áo sơ mi được giảm $15\\%$ và quần âu được giảm $18\\%$. "
                "Do đó tổng số tiền bác Hà phải trả là $583$ nghìn đồng. Hỏi giá niêm yết của mỗi chiếc áo sơ mi và chiếc quần âu là bao nhiêu?"
            ),
            dap_an=[
                y(
                    "",
                    2.0,
                    [
                        ("Gọi giá niêm yết của chiếc áo sơ mi là $x$ (nghìn đồng), giá niêm yết của chiếc quần âu là $y$ (nghìn đồng).", 0.25),
                        ("Điều kiện: $0 < x, y < 700$."),
                        ("Vì tổng giá niêm yết của hai mặt hàng là $700$ nghìn đồng nên ta có phương trình: $x + y = 700$ (1)", 0.5),
                        ("Số tiền thực tế bác Hà trả cho chiếc áo sơ mi là: $x(1 - 15\\%) = 0{,}85x$ (nghìn đồng)."),
                        ("Số tiền thực tế bác Hà trả cho chiếc quần âu là: $y(1 - 18\\%) = 0{,}82y$ (nghìn đồng)."),
                        ("Vì tổng số tiền bác Hà phải trả là $583$ nghìn đồng nên ta có phương trình: $0{,}85x + 0{,}82y = 583$ (2)", 0.5),
                        ("Từ (1) và (2) ta có hệ phương trình: $\\begin{cases} x + y = 700 \\\\ 0{,}85x + 0{,}82y = 583 \\end{cases}$"),
                        ("Nhân cả hai vế của phương trình đầu với $0{,}85$: $\\begin{cases} 0{,}85x + 0{,}85y = 595 \\\\ 0{,}85x + 0{,}82y = 583 \\end{cases}$"),
                        ("Trừ từng vế hai phương trình ta được: $0{,}03y = 12 \\Rightarrow y = 400$."),
                        ("Thay $y = 400$ vào phương trình (1): $x + 400 = 700 \\Rightarrow x = 300$.", 0.5),
                        ("Giá trị $x = 300; y = 400$ thoả mãn điều kiện của bài toán."),
                        ("Vậy giá niêm yết của chiếc áo sơ mi là $300$ nghìn đồng, của chiếc quần âu là $400$ nghìn đồng.", 0.25),
                    ],
                )
            ],
            mt=[("II", "Toán thực tế: mua bán, chiết khấu phần trăm (lập hệ phương trình)", "ĐS I", "TH", 2.0, 15, "Quận Cầu Giấy (2024–2025)")],
            note="Nhắc học sinh đặt ẩn, ghi đơn vị và điều kiện. Lỗi hay gặp: tính nhầm phần trăm còn lại $(1 - 15\\% = 85\\%)$.",
        ),
        dict(
            label="Bài III.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                + BR
                + "1) \\textbf{(0,75 điểm)} $\\begin{cases} x - 2y = 12 \\\\ 2x + 3y = 3 \\end{cases}$"
                + BR
                + "2) \\textbf{(0,75 điểm)} $x(x - 7) + x - 7 = 0$"
                + BR
                + "3) \\textbf{(0,5 điểm)} $\\dfrac{4x - 2}{3} + x \\le \\dfrac{1 + 5x}{4}$"
            ),
            dap_an=[
                y(
                    "1)",
                    0.75,
                    [
                        ("Từ phương trình thứ nhất suy ra: $x = 2y + 12$"),
                        ("Thế vào phương trình thứ hai ta được: $2(2y + 12) + 3y = 3$", 0.25),
                        ("$4y + 24 + 3y = 3$"),
                        ("$7y = -21 \\Rightarrow y = -3$", 0.25),
                        ("Thay $y = -3$ vào $x = 2y + 12$ ta được $x = 2(-3) + 12 = 6$."),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = (6; -3)$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    0.75,
                    [
                        ("$x(x - 7) + (x - 7) = 0$"),
                        ("$(x + 1)(x - 7) = 0$", 0.25),
                        ("$x + 1 = 0$ hoặc $x - 7 = 0$"),
                        ("$x = -1$ hoặc $x = 7$", 0.25),
                        ("Vậy phương trình có hai nghiệm $x = -1$ và $x = 7$.", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Quy đồng khử mẫu số dương (mẫu chung là $12$):"),
                        ("$4(4x - 2) + 12x \\le 3(1 + 5x)$"),
                        ("$16x - 8 + 12x \\le 3 + 15x$", 0.25),
                        ("$28x - 15x \\le 3 + 8$"),
                        ("$13x \\le 11 \\Rightarrow x \\le \\dfrac{11}{13}$"),
                        ("Vậy nghiệm của bất phương trình là $x \\le \\dfrac{11}{13}$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IIIa", "Giải hệ hai phương trình bậc nhất hai ẩn", "ĐS I", "NB", 0.75, 6, "THCS Dịch Vọng (2025–2026)"),
                ("IIIb", "Giải phương trình tích đưa về phương trình bậc nhất", "ĐS I", "NB", 0.75, 6, "THCS Dịch Vọng (2025–2026)"),
                ("IIIc", "Giải bất phương trình bậc nhất một ẩn chứa phân thức", "ĐS II", "TH", 0.5, 5, "Quận Ba Đình (2024–2025)"),
            ],
            note="Mỗi phép biến đổi xuống một dòng rõ ràng, không dùng dấu tương đương.",
        ),
        dict(
            label="Bài IV.",
            level=3,
            statement=(
                "\\textbf{(3,5 điểm)}"
                + BR
                + "1) \\textbf{(0,5 điểm)} Tính chiều cao của một toà tháp, biết rằng khi tia nắng mặt trời tạo với mặt đất một góc $40^\\circ$ thì bóng của toà tháp trên mặt đất có chiều dài là $135$ m (kết quả làm tròn đến chữ số thập phân thứ nhất)."
                + BR
                + "2) \\textbf{(3,0 điểm)} Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn $(O; R)$. Từ $A$ kẻ hai tiếp tuyến $AB, AC$ với đường tròn $(O; R)$ ($B, C$ là các tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$. Kẻ đường kính $BD$ của $(O)$."
                + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh rằng bốn điểm $A, B, O, C$ cùng nằm trên một đường tròn."
                + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh $OA \\perp BC$ tại $H$ và $AH \\cdot AO = AB^2$. Kẻ cát tuyến $AMN$ qua tâm $O$ ($M$ nằm giữa $A$ và $N$). Chứng minh $AM \\cdot AN = AH \\cdot AO$."
                + BR
                + "c) \\textbf{(1,0 điểm)} Gọi $E$ là chân đường vuông góc kẻ từ $C$ đến $BD$, $K$ là giao điểm của $AD$ và $CE$. Chứng minh rằng $K$ là trung điểm của $CE$."
            ),
            figure={"tikz": TIKZ_THAP, "caption": "Minh hoạ Bài IV.1"},
            hinh_da=HINH_ON1,
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Gọi $AB$ là chiều cao toà tháp ($AB \\perp BC$ tại chân tháp $B$), $BC$ là bóng của tháp trên mặt đất với $BC = 135$ m."),
                        ("Góc tạo bởi tia nắng mặt trời với mặt đất là $\\widehat{ACB} = 40^\\circ$."),
                        ("Xét $\\triangle ABC$ vuông tại $B$, ta có: $AB = BC \\cdot \\tan \\widehat{ACB}$", 0.25),
                        ("$AB = 135 \\cdot \\tan 40^\\circ \\approx 135 \\cdot 0{,}8391 \\approx 113{,}3$ (m)."),
                        ("Vậy toà tháp cao khoảng $113{,}3$ mét.", 0.25),
                    ],
                ),
                y(
                    "2a)",
                    1.0,
                    [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Vì $AB, AC$ là hai tiếp tuyến của đường tròn $(O)$ tại $B$ và $C$ nên:"),
                        ("$AB \\perp OB \\Rightarrow \\widehat{ABO} = 90^\\circ$"),
                        ("$AC \\perp OC \\Rightarrow \\widehat{ACO} = 90^\\circ$", 0.25),
                        ("Xét tam giác $ABO$ vuông tại $B \\Rightarrow$ ba điểm $A, B, O$ cùng thuộc đường tròn đường kính $AO$."),
                        ("Xét tam giác $ACO$ vuông tại $C \\Rightarrow$ ba điểm $A, C, O$ cùng thuộc đường tròn đường kính $AO$.", 0.25),
                        ("Do đó bốn điểm $A, B, O, C$ cùng thuộc đường tròn đường kính $AO$.", 0.25),
                    ],
                ),
                y(
                    "2b)",
                    1.0,
                    [
                        ("Theo tính chất hai tiếp tuyến cắt nhau, ta có $AB = AC$ và $OB = OC = R$."),
                        ("Suy ra $OA$ là đường trung trực của đoạn thẳng $BC$."),
                        ("Do đó $OA \\perp BC$ tại $H$ (và $H$ là trung điểm của $BC$).", 0.25),
                        ("Xét $\\triangle ABH$ và $\\triangle AOB$ có: $\\widehat{AHB} = \\widehat{ABO} = 90^\\circ$ và góc $\\widehat{BAO}$ chung"),
                        ("$\\Rightarrow \\triangle ABH \\backsim \\triangle AOB$ (g.g)", 0.25),
                        ("$\\Rightarrow \\dfrac{AH}{AB} = \\dfrac{AB}{AO} \\Rightarrow AH \\cdot AO = AB^2$ (1)", 0.25),
                        ("Mặt khác, $AM = OA - R$ và $AN = OA + R$."),
                        ("Suy ra $AM \\cdot AN = (OA - R)(OA + R) = OA^2 - R^2$."),
                        ("Áp dụng định lí Pythagore trong $\\triangle ABO$ vuông tại $B$: $OA^2 - OB^2 = AB^2 \\Rightarrow OA^2 - R^2 = AB^2$."),
                        ("Do đó $AM \\cdot AN = AB^2$ (2). Từ (1) và (2) suy ra $AM \\cdot AN = AH \\cdot AO$.", 0.25),
                    ],
                ),
                y(
                    "2c)",
                    1.0,
                    [
                        ("Vì $BD$ là đường kính của $(O)$ nên $\\triangle BCD$ nội tiếp đường tròn có cạnh huyền là đường kính $\\Rightarrow \\widehat{BCD} = 90^\\circ$."),
                        ("Do đó $CD \\perp BC$. Mà $OA \\perp BC$ nên $CD \\parallel OA$.", 0.25),
                        ("Mặt khác $AB \\perp BD$ (tính chất tiếp tuyến) và $CE \\perp BD$ (giả thiết) $\\Rightarrow CE \\parallel AB$."),
                        ("Trong $\\triangle ABD$, vì $EK \\parallel AB$ nên theo hệ quả định lí Thalès ta có: $\\dfrac{EK}{AB} = \\dfrac{DE}{BD}$"),
                        ("$\\Rightarrow EK \\cdot BD = DE \\cdot AB$ (*)", 0.25),
                        ("Xét $\\triangle CDE$ và $\\triangle ABD$:"),
                        ("Ta có $\\widehat{CED} = \\widehat{ABD} = 90^\\circ$, và $\\widehat{CDE} = \\widehat{AOB}$ (hai góc so le trong do $CD \\parallel OA$)."),
                        ("Lại có $\\triangle AOB \\backsim \\triangle ADB$? Xét $\\triangle CDE$ và $\\triangle DAB$:"),
                        ("Có $\\widehat{CDE} = \\widehat{AOB}$, $\\widehat{CED} = \\widehat{ABO} = 90^\\circ \\Rightarrow \\triangle CDE \\backsim \\triangle AOB$ (g.g)"),
                        ("$\\Rightarrow \\dfrac{CE}{AB} = \\dfrac{DE}{OB} \\Rightarrow CE \\cdot OB = DE \\cdot AB$ (**)", 0.25),
                        ("Từ (*) và (**) suy ra: $EK \\cdot BD = CE \\cdot OB$."),
                        ("Vì $BD = 2OB$ nên $EK \\cdot 2OB = CE \\cdot OB \\Rightarrow 2EK = CE$."),
                        ("Vậy $K$ là trung điểm của đoạn thẳng $CE$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IVa", "Toán thực tế: Tỉ số lượng giác góc nâng bóng tháp", "HH IV", "TH", 0.5, 5, "Huyện Đông Anh (2024–2025)"),
                ("IVb1", "Chứng minh bốn điểm cùng thuộc một đường tròn", "HH V", "TH", 1.0, 8, "Huyện Đông Anh (2024–2025)"),
                ("IVb2", "Chứng minh vuông góc và hệ thức tích qua tam giác đồng dạng", "HH V", "VD", 1.0, 10, "Huyện Đông Anh (2024–2025)"),
                ("IVb3", "Định lí Thalès và tính chất tiếp tuyến chứng minh trung điểm", "HH V", "VDC", 1.0, 12, "Huyện Đông Anh (2024–2025)"),
            ],
            note="Bài hình: Học sinh phải chứng minh qua tam giác đồng dạng để suy ra hệ thức tích. Câu c chú ý tỉ số Thalès và tam giác đồng dạng.",
        ),
        dict(
            label="Bài V.",
            level=4,
            statement=(
                "\\textbf{(0,5 điểm)} Một khách sạn có $100$ phòng cùng giá tiền cho thuê. Qua khảo sát người ta thấy rằng: nếu ban đầu mỗi phòng cho thuê với giá $480$ nghìn đồng một ngày thì luôn kín phòng; "
                "tuy nhiên khi tăng giá phòng thêm $x\\%$ ($x \\ge 0$) thì số lượng phòng cho thuê giảm đi $\\dfrac{4x}{5}\\%$. "
                "Hỏi khách sạn phải niêm yết giá tiền thuê phòng mỗi ngày là bao nhiêu để doanh thu trong một ngày đạt giá trị cao nhất?"
            ),
            dap_an=[
                y(
                    "",
                    0.5,
                    [
                        ("Ta có: khi tăng giá thêm $x\\%$, giá thuê mỗi phòng một ngày là: $480\\left(1 + \\dfrac{x}{100}\\right)$ (nghìn đồng)."),
                        ("Số lượng phòng cho thuê được là: $100\\left(1 - \\dfrac{4x}{500}\\right) = 100 - \\dfrac{4}{5}x$ (phòng). Điều kiện: $0 \\le x < 125$."),
                        ("Doanh thu trong một ngày của khách sạn là:"),
                        ("$T = 480\\left(1 + \\dfrac{x}{100}\\right)\\left(100 - \\dfrac{4}{5}x\\right) = 480\\left(100 - \\dfrac{4}{5}x + x - \\dfrac{4}{500}x^2\\right)$"),
                        ("$T = 480\\left(100 + \\dfrac{1}{5}x - \\dfrac{1}{125}x^2\\right) = -\\dfrac{480}{125}(x^2 - 25x) + 48000$", 0.25),
                        ("$T = -\\dfrac{96}{25}\\left(x - \\dfrac{25}{2}\\right)^2 + \\dfrac{96}{25} \\cdot \\dfrac{625}{4} + 48000$"),
                        ("$T = 48600 - \\dfrac{96}{25}\\left(x - 12{,}5\\right)^2 \\le 48600$ (nghìn đồng)."),
                        ("Dấu ``$=$'' xảy ra khi $x - 12{,}5 = 0 \\Rightarrow x = 12{,}5$ (thoả mãn điều kiện)."),
                        ("Khi đó giá niêm yết mỗi phòng là: $480(1 + 12{,}5\\%) = 480 \\cdot 1{,}125 = 540$ (nghìn đồng)."),
                        ("Vậy khách sạn cần niêm yết giá $540$ nghìn đồng một phòng mỗi ngày để doanh thu cao nhất (đạt $48{,}6$ triệu đồng/ngày).", 0.25),
                    ],
                )
            ],
            mt=[("V", "Bài toán tối ưu thực tế: doanh thu parabol", "ĐS II", "VDC", 0.5, 8, "Quận Cầu Giấy (2024–2025)")],
            note="HS lớp 9 biến đổi đưa về dạng $M - a(x - x_0)^2 \\le M$, không dùng công thức toạ độ đỉnh Parabol $x = -b/(2a)$ của lớp 10.",
        ),
    ],
    bay=[
        ("Bài I.1", "Khai căn HĐT chứa căn", "Bấm máy ra số thập phân hoặc quên viết $|2-\\sqrt{3}| = 2-\\sqrt{3}$ (bị trừ 0,25đ).", "Luôn viết bước trung gian $\\sqrt{A^2} = |A|$, chỉ ra $2 > \\sqrt{3}$ để phá dấu GTTĐ."),
        ("Bài I.2", "Đổi dấu mẫu $9 - x$ có dấu trừ", "Đổi dấu mẫu nhưng quên đổi dấu phân thức, dẫn tới sai dấu tử số (mất 0,5đ).", "Quy tắc: $-\\dfrac{A}{9-x} = +\\dfrac{A}{x-9}$. Đổi dấu mẫu kèm đổi dấu trước phân thức."),
        ("Bài I.3", "Tìm số nguyên $x$ để $P \\in \\mathbb{Z}$", "Tại $\\sqrt{x}-3 = -4 \\Rightarrow \\sqrt{x} = -1$ vẫn lấy $x = 1$ (thừa nghiệm sai).", "Vì $\\sqrt{x} \\ge 0$ nên $\\sqrt{x} = -1$ vô nghiệm ngay lập tức, loại."),
        ("Bài II", "Chiết khấu phần trăm mua sắm", "Lấy $0{,}15x + 0{,}18y = 583$ (sai bản chất, mất trọn 1,0đ phương trình 2).", "Giảm $15\\%$ thì số tiền thực trả là $(1 - 15\\%)x = 0{,}85x$. Phân biệt tiền giảm và tiền trả."),
        ("Bài III.3", "Bất phương trình phân số", "Quy đồng quên nhân mẫu số chung $12$ cho hạng tử tự do $+x$.", "Quy đồng mẫu chung $12$ cho toàn bộ các hạng tử cả hai vế: $+x$ thành $+12x$."),
        ("Bài IV.2a", "Bốn điểm thuộc đường tròn", "Ghi tứ giác nội tiếp do tổng hai góc đối bằng $180^\\circ$ (0 điểm vì HK1 chưa học).", "Bắt buộc chỉ ra hai tam giác vuông cùng chung cạnh huyền $AO$ đường kính."),
        ("Bài IV.2b", "Hệ thức tích $AH \\cdot AO = AB^2$", "Áp dụng trực tiếp công thức tích mà không chứng minh qua tam giác đồng dạng.", "Bắt buộc chứng minh qua cặp tam giác đồng dạng $\\triangle ABH \\backsim \\triangle AOB$ (g.g)."),
    ],
)

# =====================================================================
# ĐỀ ÔN TẬP SỐ 2
# =====================================================================
DE["on-2"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 2",
    slug_de="de-on-tap-cuoi-ki-1-so-2",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-2",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 2",
    cach_dung="Làm sau khi đã chữa Đề ôn 1. Đề 2 nâng một nấc suy luận: câu phụ căn thức chứa điều kiện số nguyên tố, hệ phương trình đặt ẩn phụ, bất phương trình rút gọn đa thức, bài hình chứng minh ba điểm thẳng hàng qua bổ đề hình thang.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 2 -- CUỐI HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc nâng cao:} "
        "Bài I (2,0đ) Căn thức có câu hỏi tìm số nguyên tố (Phòng Ba Đình) · "
        "Bài II (2,0đ) Lập hệ phương trình bài toán tài chính lãi suất (THCS Đống Đa) · "
        "Bài III (2,0đ) Hệ phương trình đặt ẩn phụ, phương trình phân thức ẩn ở mẫu, BPT đa thức · "
        "Bài IV (3,5đ) Tàu ngầm lặn góc nghiêng và Nửa đường tròn chứng minh ba điểm thẳng hàng (Phòng Thanh Trì) · "
        "Bài V (0,5đ) Bài toán tối ưu chi phí sản xuất (THCS Đống Đa)."
    ),
    bai=[
        dict(
            label="Bài I.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức:"
                + BR
                + "$A = \\dfrac{\\sqrt{x}}{\\sqrt{x}+1}$ và $B = \\dfrac{\\sqrt{x}+4}{\\sqrt{x}+3} + \\dfrac{\\sqrt{x}-1}{\\sqrt{x}-3} - \\dfrac{x-15}{x-9}$ với $x \\ge 0; x \\ne 9$."
                + BR
                + "1) \\textbf{(0,5 điểm)} Tính giá trị biểu thức $A$ với $x = 9 - 4\\sqrt{5}$."
                + BR
                + "2) \\textbf{(1,0 điểm)} Chứng minh $B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$."
                + BR
                + "3) \\textbf{(0,5 điểm)} Cho biểu thức $P = \\dfrac{\\sqrt{x}-3}{\\sqrt{x}+1}$. Tìm tất cả các giá trị của $x$ để $P$ nhận giá trị nguyên."
            ),
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Ta có: $x = 9 - 4\\sqrt{5} = 5 - 2 \\cdot 2 \\cdot \\sqrt{5} + 4 = (\\sqrt{5} - 2)^2$ (thoả mãn ĐKXĐ)."),
                        ("Suy ra $\\sqrt{x} = \\sqrt{(\\sqrt{5} - 2)^2} = |\\sqrt{5} - 2| = \\sqrt{5} - 2$ (do $\\sqrt{5} > 2$).", 0.25),
                        ("Thay vào biểu thức $A$: $A = \\dfrac{\\sqrt{5} - 2}{\\sqrt{5} - 2 + 1} = \\dfrac{\\sqrt{5} - 2}{\\sqrt{5} - 1} = \\dfrac{(\\sqrt{5} - 2)(\\sqrt{5} + 1)}{5 - 1} = \\dfrac{3 - \\sqrt{5}}{4}$."),
                        ("Vậy khi $x = 9 - 4\\sqrt{5}$ thì $A = \\dfrac{3 - \\sqrt{5}}{4}$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    1.0,
                    [
                        ("Với $x \\ge 0; x \\ne 9$, ta có:"),
                        ("$B = \\dfrac{(\\sqrt{x}+4)(\\sqrt{x}-3) + (\\sqrt{x}-1)(\\sqrt{x}+3) - (x-15)}{(\\sqrt{x}+3)(\\sqrt{x}-3)}$", 0.25),
                        ("$B = \\dfrac{x + \\sqrt{x} - 12 + x + 2\\sqrt{x} - 3 - x + 15}{(\\sqrt{x}+3)(\\sqrt{x}-3)}$", 0.25),
                        ("$B = \\dfrac{x + 3\\sqrt{x}}{(\\sqrt{x}+3)(\\sqrt{x}-3)} = \\dfrac{\\sqrt{x}(\\sqrt{x}+3)}{(\\sqrt{x}+3)(\\sqrt{x}-3)}$", 0.25),
                        ("$B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$ (điều phải chứng minh).", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Ta có: $P = \\dfrac{\\sqrt{x}-3}{\\sqrt{x}+1} = \\dfrac{\\sqrt{x}+1-4}{\\sqrt{x}+1} = 1 - \\dfrac{4}{\\sqrt{x}+1}$"),
                        ("Vì $\\sqrt{x} \\ge 0$ nên $\\sqrt{x}+1 \\ge 1 \\Rightarrow 0 < \\dfrac{4}{\\sqrt{x}+1} \\le 4$."),
                        ("Suy ra: $1 - 4 \\le 1 - \\dfrac{4}{\\sqrt{x}+1} < 1 \\Rightarrow -3 \\le P < 1$.", 0.25),
                        ("Vì $P$ nhận giá trị nguyên nên $P \\in \\{-3; -2; -1; 0\\}$." + BR
                         + "+ Với $P = -3 \\Rightarrow \\dfrac{4}{\\sqrt{x}+1} = 4 \\Rightarrow \\sqrt{x}+1 = 1 \\Rightarrow \\sqrt{x}=0 \\Rightarrow x=0$ (TMĐK)." + BR
                         + "+ Với $P = -2 \\Rightarrow \\dfrac{4}{\\sqrt{x}+1} = 3 \\Rightarrow \\sqrt{x}+1 = \\dfrac{4}{3} \\Rightarrow \\sqrt{x}=\\dfrac{1}{3} \\Rightarrow x=\\dfrac{1}{9}$ (TMĐK)." + BR
                         + "+ Với $P = -1 \\Rightarrow \\dfrac{4}{\\sqrt{x}+1} = 2 \\Rightarrow \\sqrt{x}+1 = 2 \\Rightarrow \\sqrt{x}=1 \\Rightarrow x=1$ (TMĐK)." + BR
                         + "+ Với $P = 0 \\Rightarrow \\sqrt{x}-3 = 0 \\Rightarrow \\sqrt{x}=3 \\Rightarrow x=9$ (không thoả mãn ĐKXĐ $x \\ne 9$, loại)."),
                        ("Vậy các giá trị của $x$ để $P$ nhận giá trị nguyên là $x \\in \\left\\{0; \\dfrac{1}{9}; 1\\right\\}$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("Ia", "Tính giá trị phân thức căn khi $x = 9 - 4\\sqrt{5}$", "ĐS III", "NB", 0.5, 5, "Quận Ba Đình (2024–2025)"),
                ("Ib", "Rút gọn biểu thức chứa căn bậc hai", "ĐS III", "TH", 1.0, 10, "Quận Ba Đình (2024–2025)"),
                ("Ic", "Tìm $x$ thực để biểu thức nhận giá trị nguyên bằng chặn miền", "ĐS III", "VD", 0.5, 7, "Quận Ba Đình (2024–2025)"),
            ],
            note="BẪY TỬ HUYỆT (90\\% HS mất điểm): Đề yêu cầu tìm x để P nguyên (không có chữ nguyên sau x) [[br]] bắt buộc phải dùng phương pháp CHẶN MIỀN GIÁ TRỊ, HS dùng ước số sẽ bị 0 điểm vì thiếu nghiệm $x = 1/9$; [[br]] tại $P = 0$ giải ra $x = 9$ vi phạm ĐKXĐ nên bị loại.",
        ),
        dict(
            label="Bài II.",
            level=3,
            statement=(
                "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                + BR
                + "Bác Minh chia số tiền $800$ triệu đồng của mình cho hai khoản đầu tư. "
                "Sau một năm, tổng số tiền vốn và tiền lãi thu được là $845$ triệu đồng. "
                "Biết lãi suất cho khoản đầu tư thứ nhất là $5\\%$/năm và khoản đầu tư thứ hai là $6\\%$/năm. "
                "Tính số tiền bác Minh đã đầu tư cho mỗi khoản."
            ),
            dap_an=[
                y(
                    "",
                    2.0,
                    [
                        ("Gọi số tiền bác Minh đầu tư cho khoản thứ nhất là $x$ (triệu đồng), cho khoản thứ hai là $y$ (triệu đồng).", 0.25),
                        ("Điều kiện: $0 < x, y < 800$."),
                        ("Vì tổng số tiền đầu tư là $800$ triệu đồng nên ta có phương trình: $x + y = 800$ (1)", 0.5),
                        ("Tổng số tiền lãi thu được sau một năm là: $845 - 800 = 45$ (triệu đồng)."),
                        ("Tiền lãi từ khoản thứ nhất là: $5\\% \\cdot x = 0{,}05x$ (triệu đồng)."),
                        ("Tiền lãi từ khoản thứ hai là: $6\\% \\cdot y = 0{,}06y$ (triệu đồng)."),
                        ("Do tổng tiền lãi là $45$ triệu đồng nên ta có phương trình: $0{,}05x + 0{,}06y = 45$ (2)", 0.5),
                        ("Từ (1) và (2) ta có hệ phương trình: $\\begin{cases} x + y = 800 \\\\ 0{,}05x + 0{,}06y = 45 \\end{cases}$"),
                        ("Nhân cả hai vế của (1) với $0{,}05$: $\\begin{cases} 0{,}05x + 0{,}05y = 40 \\\\ 0{,}05x + 0{,}06y = 45 \\end{cases}$"),
                        ("Trừ từng vế hai phương trình ta được: $0{,}01y = 5 \\Rightarrow y = 500$."),
                        ("Thay $y = 500$ vào (1) ta được: $x + 500 = 800 \\Rightarrow x = 300$.", 0.5),
                        ("Các giá trị $x = 300; y = 500$ thoả mãn điều kiện bài toán."),
                        ("Vậy bác Minh đầu tư khoản thứ nhất là $300$ triệu đồng và khoản thứ hai là $500$ triệu đồng.", 0.25),
                    ],
                )
            ],
            mt=[("II", "Toán thực tế: lãi suất đầu tư tài chính (lập hệ phương trình)", "ĐS I", "TH", 2.0, 15, "THCS Đống Đa (2025–2026)")],
            note="Học sinh có thể lập phương trình theo tổng số vốn và lãi: 1,05x + 1,06y = 845, hai cách đều được điểm tối đa.",
        ),
        dict(
            label="Bài III.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                + BR
                + "1) \\textbf{(0,75 điểm)} $\\begin{cases} 2(x + y) + 3(x - y) = 4 \\\\ (x + y) + 2(x - y) = 5 \\end{cases}$"
                + BR
                + "2) \\textbf{(0,75 điểm)} $\\dfrac{x - 1}{x - 2} + 3 = \\dfrac{x - 8}{2 - x}$"
                + BR
                + "3) \\textbf{(0,5 điểm)} $x^2 - 3x + 1 \\ge 2(x - 1) - x(3 - x)$"
            ),
            dap_an=[
                y(
                    "1)",
                    0.75,
                    [
                        ("Đặt $u = x + y$ và $v = x - y$."),
                        ("Hệ phương trình trở thành: $\\begin{cases} 2u + 3v = 4 \\\\ u + 2v = 5 \\end{cases}$", 0.25),
                        ("Từ phương trình thứ hai: $u = 5 - 2v$. Thế vào phương trình đầu:"),
                        ("$2(5 - 2v) + 3v = 4 \\Rightarrow 10 - v = 4 \\Rightarrow v = 6$"),
                        ("Suy ra $u = 5 - 2(6) = -7$.", 0.25),
                        ("Ta có hệ phương trình đối với $x, y$: $\\begin{cases} x + y = -7 \\\\ x - y = 6 \\end{cases}$"),
                        ("Cộng hai phương trình: $2x = -1 \\Rightarrow x = -0{,}5$."),
                        ("Trừ hai phương trình: $2y = -13 \\Rightarrow y = -6{,}5$."),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = (-0{,}5; -6{,}5)$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    0.75,
                    [
                        ("Điều kiện xác định: $x \\ne 2$."),
                        ("Phương trình tương đương: $\\dfrac{x - 1}{x - 2} + 3 = -\\dfrac{x - 8}{x - 2}$", 0.25),
                        ("Quy đồng và khử mẫu: $x - 1 + 3(x - 2) = -(x - 8)$"),
                        ("$x - 1 + 3x - 6 = -x + 8$"),
                        ("$4x - 7 = -x + 8$"),
                        ("$5x = 15 \\Rightarrow x = 3$", 0.25),
                        ("Giá trị $x = 3$ thoả mãn ĐKXĐ. Vậy phương trình có nghiệm $x = 3$.", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Khai triển hai vế bất phương trình:"),
                        ("$x^2 - 3x + 1 \\ge 2x - 2 - 3x + x^2$"),
                        ("$x^2 - 3x + 1 \\ge x^2 - x - 2$", 0.25),
                        ("Chuyển vế và thu gọn: $-3x + x \\ge -2 - 1$"),
                        ("$-2x \\ge -3$"),
                        ("$x \\le \\dfrac{3}{2}$"),
                        ("Vậy nghiệm của bất phương trình là $x \\le \\dfrac{3}{2}$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IIIa", "Giải hệ phương trình đưa về bậc nhất hoặc đặt ẩn phụ", "ĐS I", "TH", 0.75, 7, "Quận Cầu Giấy (2024–2025)"),
                ("IIIb", "Giải phương trình chứa ẩn ở mẫu", "ĐS I", "TH", 0.75, 6, "Quận Ba Đình (2024–2025)"),
                ("IIIc", "Giải bất phương trình đưa về bậc nhất", "ĐS II", "NB", 0.5, 5, "Quận Ba Đình (2024–2025)"),
            ],
            note="Lưu ý học sinh đổi dấu mẫu $2 - x = -(x - 2)$ và bắt buộc kiểm tra ĐKXĐ $x \\ne 2$.",
        ),
        dict(
            label="Bài IV.",
            level=3,
            statement=(
                "\\textbf{(3,5 điểm)}"
                + BR
                + "1) \\textbf{(0,5 điểm)} Trong một buổi tập luyện, một tàu ngầm ở trên mặt biển lặn xuống và di chuyển theo một đường thẳng tạo với mặt nước biển một góc $30^\\circ$. Khi tàu ở độ sâu $100$ mét so với mặt nước biển thì tàu đã đi được quãng đường dài bao nhiêu mét?"
                + BR
                + "2) \\textbf{(3,0 điểm)} Cho nửa đường tròn $(O)$, đường kính $AB$. Trên nửa đường tròn $(O)$ lấy một điểm $D$ ($D$ khác $A$ và $B$). Tiếp tuyến của nửa đường tròn $(O)$ tại $A$ và $D$ cắt nhau ở điểm $C$. Gọi $F$ là hình chiếu của $D$ trên đoạn thẳng $AB$. Tia $BC$ cắt nửa đường tròn $(O)$ tại $E$ ($E$ khác $B$)."
                + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh $\\triangle AEB$ vuông tại $E$."
                + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh $CE \\cdot CB = CA^2$ và $\\widehat{CDE} = \\widehat{CBD}$."
                + BR
                + "c) \\textbf{(1,0 điểm)} Gọi $I$ là trung điểm của đoạn thẳng $DF$. Chứng minh ba điểm $B, I, C$ thẳng hàng."
            ),
            figure={"tikz": TIKZ_TAUNGAM_CK, "caption": "Minh hoạ Bài IV.1"},
            hinh_da=HINH_ON2,
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Gọi vị trí tàu bắt đầu lặn là $A$, vị trí tàu ngầm đạt độ sâu $100$ m là $C$, hình chiếu của $C$ lên mặt nước biển là $B$."),
                        ("Khi đó tam giác $ABC$ vuông tại $B$, có $BC = 100$ m và góc lặn $\\widehat{BAC} = 30^\\circ$."),
                        ("Xét tam giác $ABC$ vuông tại $B$, ta có: $\\sin \\widehat{BAC} = \\dfrac{BC}{AC}$", 0.25),
                        ("$\\Rightarrow AC = \\dfrac{BC}{\\sin 30^\\circ} = \\dfrac{100}{0{,}5} = 200$ (m)."),
                        ("Vậy tàu đã đi được quãng đường dài $200$ mét.", 0.25),
                    ],
                ),
                y(
                    "2a)",
                    1.0,
                    [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Xét nửa đường tròn $(O)$ đường kính $AB$:"),
                        ("Điểm $E$ thuộc nửa đường tròn $(O)$ và $E \\ne A, B$."),
                        ("Suy ra góc $\\widehat{AEB}$ là góc nội tiếp chắn nửa đường tròn.", 0.5),
                        ("Do đó $\\widehat{AEB} = 90^\\circ$."),
                        ("Vậy tam giác $AEB$ vuông tại $E$.", 0.25),
                    ],
                ),
                y(
                    "2b)",
                    1.0,
                    [
                        ("Vì $AC$ là tiếp tuyến của $(O)$ tại $A$ nên $AC \\perp AB \\Rightarrow \\triangle ABC$ vuông tại $A$."),
                        ("Vì $\\triangle AEB$ vuông tại $E$ nên $AE \\perp BC$ tại $E$."),
                        ("Xét $\\triangle CAE$ và $\\triangle CBA$ có: $\\widehat{AEC} = \\widehat{BAC} = 90^\\circ$ và góc $\\widehat{ACB}$ chung"),
                        ("$\\Rightarrow \\triangle CAE \\backsim \\triangle CBA$ (g.g)", 0.25),
                        ("$\\Rightarrow \\dfrac{CE}{CA} = \\dfrac{CA}{CB} \\Rightarrow CE \\cdot CB = CA^2$ (1)", 0.25),
                        ("Theo tính chất hai tiếp tuyến cắt nhau tại $C$, ta có $CA = CD$."),
                        ("Thay vào (1) được: $CE \\cdot CB = CD^2 \\Rightarrow \\dfrac{CE}{CD} = \\dfrac{CD}{CB}$."),
                        ("Xét $\\triangle CDE$ và $\\triangle CBD$ có: $\\dfrac{CE}{CD} = \\dfrac{CD}{CB}$ và góc $\\widehat{BCD}$ chung"),
                        ("$\\Rightarrow \\triangle CDE \\backsim \\triangle CBD$ (c.g.c)", 0.25),
                        ("$\\Rightarrow \\widehat{CDE} = \\widehat{CBD}$ (hai góc tương ứng, điều phải chứng minh).", 0.25),
                    ],
                ),
                y(
                    "2c)",
                    1.0,
                    [
                        ("Gọi $K$ là giao điểm của tia $BD$ và tiếp tuyến $Ax$."),
                        ("Vì $\\triangle ABD$ nội tiếp nửa đường tròn đường kính $AB$ nên $\\widehat{ADB} = 90^\\circ \\Rightarrow AD \\perp BK$."),
                        ("Tam giác $ABK$ vuông tại $A$ có $AD \\perp BK$. Ta có $\\widehat{AKD} = 90^\\circ - \\widehat{KAD} = \\widehat{DAB}$."),
                        ("Mặt khác, tam giác $CAD$ cân tại $C$ (do $CA = CD$) nên $\\widehat{CAD} = \\widehat{CDA}$."),
                        ("Lại có $\\widehat{CKA} + \\widehat{CAD} = 90^\\circ$ và $\\widehat{CDK} + \\widehat{CDA} = 90^\\circ$, suy ra hai góc $\\widehat{CKD}$ và $\\widehat{CDK}$ bằng nhau."),
                        ("Suy ra $\\triangle CKD$ cân tại $C$, do đó $CK = CD$. Mà $CA = CD$ nên $CK = CA$. Vậy $C$ là trung điểm của $AK$.", 0.25),
                        ("Xét $\\triangle ABK$ có $DF \\parallel AK$ (cùng vuông góc với $AB$)."),
                        ("Gọi $I'$ là giao điểm của $BC$ và $DF$."),
                        ("Theo hệ quả định lí Thalès trong $\\triangle ABC$ có $I'F \\parallel AC$: $\\dfrac{I'F}{AC} = \\dfrac{BF}{AB}$ (3)"),
                        ("Theo hệ quả định lí Thalès trong $\\triangle KBC$ có $DI' \\parallel KC$: $\\dfrac{DI'}{KC} = \\dfrac{BF}{AB}$ (4)", 0.25),
                        ("Từ (3) và (4) suy ra: $\\dfrac{I'F}{AC} = \\dfrac{DI'}{KC}$."),
                        ("Mà $AC = KC$ (chứng minh trên) nên $I'F = DI'$."),
                        ("Do đó $I'$ là trung điểm của đoạn thẳng $DF$.", 0.25),
                        ("Theo giả thiết $I$ là trung điểm của $DF$, suy ra $I \\equiv I'$."),
                        ("Vậy ba điểm $B, I, C$ thẳng hàng.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IVa", "Toán thực tế: Tỉ số lượng giác sin tính quãng đường lặn", "HH IV", "NB", 0.5, 5, "Huyện Thanh Trì (2024–2025)"),
                ("IVb1", "Góc nội tiếp chắn nửa đường tròn", "HH V", "NB", 1.0, 7, "Huyện Thanh Trì (2024–2025)"),
                ("IVb2", "Chứng minh hệ thức tích và hai góc bằng nhau qua đồng dạng", "HH V", "TH", 1.0, 10, "Huyện Thanh Trì (2024–2025)"),
                ("IVb3", "Bổ đề hình thang chứng minh ba điểm thẳng hàng", "HH V", "VDC", 1.0, 12, "Huyện Thanh Trì (2024–2025)"),
            ],
            note="Bài hình: Câu c là bài toán bổ đề hình thang kinh điển, then chốt là chứng minh C là trung điểm đoạn thẳng AK trên tiếp tuyến.",
        ),
        dict(
            label="Bài V.",
            level=4,
            statement=(
                "\\textbf{(0,5 điểm)} Một công ty nhận đơn đặt hàng sản xuất $9000$ quả bóng tennis. "
                "Mỗi máy móc sản xuất được $40$ quả bóng/giờ với chi phí thiết lập ban đầu là $180$ nghìn đồng/máy. "
                "Toàn bộ số máy hoạt động tự động dưới sự giám sát của một kĩ sư với tiền lương $320$ nghìn đồng/giờ. "
                "Hỏi công ty nên vận hành bao nhiêu máy để tổng chi phí sản xuất là thấp nhất?"
            ),
            dap_an=[
                y(
                    "",
                    0.5,
                    [
                        ("Gọi số máy móc công ty đưa vào hoạt động là $n$ ($n \\in \\mathbb{N}^*$, $n \\le 225$)."),
                        ("Trong một giờ, $n$ máy sản xuất được: $40n$ (quả bóng)."),
                        ("Thời gian cần thiết để hoàn thành $9000$ quả bóng là: $\\dfrac{9000}{40n} = \\dfrac{225}{n}$ (giờ)."),
                        ("Chi phí lắp đặt $n$ máy móc là: $180n$ (nghìn đồng)."),
                        ("Chi phí trả lương cho kĩ sư giám sát là: $320 \\cdot \\dfrac{225}{n} = \\dfrac{72000}{n}$ (nghìn đồng).", 0.25),
                        ("Tổng chi phí sản xuất của công ty là: $C(n) = 180n + \\dfrac{72000}{n}$ (nghìn đồng)."),
                        ("Vì $n > 0$, áp dụng bất đẳng thức Cauchy cho hai số dương $180n$ và $\\dfrac{72000}{n}$:"),
                        ("$C(n) = 180n + \\dfrac{72000}{n} \\ge 2\\sqrt{180n \\cdot \\dfrac{72000}{n}} = 2\\sqrt{12960000} = 2 \\cdot 3600 = 7200$ (nghìn đồng)."),
                        ("Dấu ``$=$'' xảy ra khi: $180n = \\dfrac{72000}{n} \\Rightarrow n^2 = \\dfrac{72000}{180} = 400 \\Rightarrow n = 20$ (thoả mãn $n \\in \\mathbb{N}^*$)."),
                        ("Vậy công ty nên đưa vào sử dụng đúng $20$ máy móc để chi phí sản xuất thấp nhất (chi phí tối thiểu là $7{,}2$ triệu đồng).", 0.25),
                    ],
                )
            ],
            mt=[("V", "Bài toán tối ưu chi phí sản xuất: Bất đẳng thức Cauchy", "ĐS II", "VDC", 0.5, 8, "THCS Đống Đa (2025–2026)")],
            note="Lưu ý: học sinh áp dụng BĐT Cauchy cần chỉ ra điều kiện số dương $n > 0$ và kiểm tra dấu bằng xảy ra.",
        ),
    ],
    bay=[
        ("Bài I.1", "Khai căn HĐT $9 - 4\\sqrt{5}$", "Quên viết bước $|\\sqrt{5}-2| = \\sqrt{5}-2$ hoặc bấm máy ra số thập phân.", "Viết rõ $9 - 4\\sqrt{5} = (\\sqrt{5}-2)^2$, vì $\\sqrt{5} > 2$ nên $|\\sqrt{5}-2| = \\sqrt{5}-2$."),
        ("Bài I.2", "Trừ phân thức có ngoặc ở tử", "Viết $-(x-15) = -x - 15$ (sai dấu số hạng tự do, sai toàn bộ bài rút gọn).", "Luôn đóng mở ngoặc $-(x - 15)$, bước sau mới phá ngoặc thành $-x + 15$."),
        ("Bài I.3", "Tìm $x$ thực để $P \\in \\mathbb{Z}$ (TỬ HUYỆT)", "Lấy mẫu $\\sqrt{x}+1$ là ước của $4$ (sai phương pháp, mất nghiệm $x = 1/9$, bị 0đ).", "Vì $x \\in \\mathbb{R}$ nên dùng phương pháp CHẶN MIỀN GIÁ TRỊ $-3 \\le P < 1$, tìm $P \\in \\mathbb{Z}$."),
        ("Bài I.3", "Loại nghiệm ngoại lai trùng ĐKXĐ", "Tại $P = 0$ giải ra $x = 9$ hớn hở nhận nghiệm (bị trừ 0,25đ do $x \\ne 9$).", "Luôn đối chiếu nghiệm tìm được với ĐKXĐ $x \\ge 0, x \\ne 9$. Tại $x = 9$ phải ghi (loại)."),
        ("Bài II", "Lãi suất tài chính hai khoản", "Nhầm phương trình tiền lãi với phương trình tổng vốn và lãi.", "Lập rõ: tiền lãi khoản 1 là $0{,}05x$, khoản 2 là $0{,}06y$. Tổng lãi $0{,}05x + 0{,}06y = 45$."),
        ("Bài III.1", "Hệ phương trình đặt ẩn phụ", "Tìm ra ẩn phụ $u = -7, v = 6$ xong kết luận luôn nghiệm hệ (quên tìm $x, y$).", "Luôn có bước 2: thế ngược $u, v$ trở lại để giải hệ đối với $x$ và $y$."),
        ("Bài IV.1", "Góc lặn tàu ngầm", "Dùng $\\tan 30^\\circ$ tính cạnh nằm ngang thay vì quãng đường di chuyển.", "Tàu lặn theo phương nghiêng nên quãng đường là cạnh huyền: dùng $\\sin 30^\\circ = \\text{đối}/\\text{huyền}$."),
    ],
)

# =====================================================================
# ĐỀ ÔN TẬP SỐ 3
# =====================================================================
DE["on-3"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 3",
    slug_de="de-on-tap-cuoi-ki-1-so-3",
    slug_mt="ma-tran-va-dap-an-on-tap-ck1-so-3",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP CUỐI KÌ I — SỐ 3",
    cach_dung="Làm sau Đề ôn 1 và 2. Đề 3 bao quát các dạng mở rộng tần suất cao: biểu thức căn chứa câu hỏi tìm x nguyên để P nguyên, toán chuyển động dòng nước hai tour du thuyền, phương trình phân thức rút gọn, tiếp tuyến thứ hai và hệ thức phân giác.",
    gioi_thieu=(
        "\\textbf{ĐỀ ÔN TẬP SỐ 3 -- CUỐI HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)."
        + BR
        + "\\textbf{Cấu trúc tổng ôn:} "
        "Bài I (2,0đ) Rút gọn căn thức và câu hỏi nguyên (Phòng Đông Anh) · "
        "Bài II (2,0đ) Lập hệ phương trình tour du thuyền sông Hồng xuôi/ngược dòng (THCS Trưng Vương) · "
        "Bài III (2,0đ) Hệ phương trình khử ngoặc (Hoài Đức), phương trình ẩn ở mẫu (Ái Mộ), BPT bậc nhất · "
        "Bài IV (3,5đ) Thang dựa tường an toàn và Đường tròn hai tiếp tuyến, tiếp tuyến thứ hai, hệ thức tích (THCS Ái Mộ) · "
        "Bài V (0,5đ) Cực trị hình học: chia đoạn dây uốn thành 3 hình vuông (Phòng Hai Bà Trưng)."
    ),
    bai=[
        dict(
            label="Bài I.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Cho hai biểu thức:"
                + BR
                + "$A = \\dfrac{\\sqrt{x}-3}{\\sqrt{x}-2}$ và $B = \\dfrac{\\sqrt{x}-1}{\\sqrt{x}+2} + \\dfrac{5\\sqrt{x}-2}{x-4}$ với $x \\ge 0; x \\ne 4; x \\ne 9$."
                + BR
                + "1) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 16$."
                + BR
                + "2) \\textbf{(1,0 điểm)} Rút gọn biểu thức $B$."
                + BR
                + "3) \\textbf{(0,5 điểm)} Cho $P = B : A$. Tìm tất cả các giá trị của $x$ để $P < 1$."
            ),
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Thay $x = 16$ (thoả mãn ĐKXĐ) vào $A$:"),
                        ("$A = \\dfrac{\\sqrt{16}-3}{\\sqrt{16}-2} = \\dfrac{4-3}{4-2} = \\dfrac{1}{2}$", 0.25),
                        ("Vậy khi $x = 16$ thì $A = \\dfrac{1}{2}$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    1.0,
                    [
                        ("Với $x \\ge 0; x \\ne 4; x \\ne 9$, ta có:"),
                        ("$B = \\dfrac{(\\sqrt{x}-1)(\\sqrt{x}-2) + (5\\sqrt{x}-2)}{(\\sqrt{x}+2)(\\sqrt{x}-2)}$", 0.25),
                        ("$B = \\dfrac{x - 3\\sqrt{x} + 2 + 5\\sqrt{x} - 2}{(\\sqrt{x}+2)(\\sqrt{x}-2)}$", 0.25),
                        ("$B = \\dfrac{x + 2\\sqrt{x}}{(\\sqrt{x}+2)(\\sqrt{x}-2)} = \\dfrac{\\sqrt{x}(\\sqrt{x}+2)}{(\\sqrt{x}+2)(\\sqrt{x}-2)}$", 0.25),
                        ("$B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-2}$.", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Ta có: $P = B : A = \\dfrac{\\sqrt{x}}{\\sqrt{x}-2} : \\dfrac{\\sqrt{x}-3}{\\sqrt{x}-2} = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$"),
                        ("Xét bất phương trình $P < 1$:"),
                        ("$\\dfrac{\\sqrt{x}}{\\sqrt{x}-3} - 1 < 0$"),
                        ("$\\dfrac{\\sqrt{x} - (\\sqrt{x}-3)}{\\sqrt{x}-3} < 0$"),
                        ("$\\dfrac{3}{\\sqrt{x}-3} < 0$", 0.25),
                        ("Vì tử số $3 > 0$ nên mẫu số $\\sqrt{x}-3 < 0 \\Rightarrow \\sqrt{x} < 3 \\Rightarrow 0 \\le x < 9$."),
                        ("Kết hợp điều kiện xác định $x \\ge 0; x \\ne 4; x \\ne 9$, ta được:"),
                        ("$0 \\le x < 9$ và $x \\ne 4$."),
                        ("Vậy nghiệm của bất phương trình là $0 \\le x < 9, x \\ne 4$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("Ia", "Tính giá trị phân thức căn tại $x = 16$", "ĐS III", "NB", 0.5, 5, "THCS Chu Văn An (2025–2026)"),
                ("Ib", "Rút gọn phân thức căn bậc hai chứa hằng đẳng thức hiệu hai bình phương", "ĐS III", "TH", 1.0, 10, "THCS Chu Văn An (2025–2026)"),
                ("Ic", "Giải bất phương trình $P < 1$ chứa căn bậc hai", "ĐS III", "VD", 0.5, 7, "THCS Chu Văn An (2025–2026)"),
            ],
            note="Lỗi phổ biến: quy đồng quên dấu ngoặc dẫn tới sai tử số, hoặc quên kết hợp điều kiện $x \\ne 4$.",
        ),
        dict(
            label="Bài II.",
            level=3,
            statement=(
                "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                + BR
                + "Một du thuyền trên sông chạy xuôi dòng $25$ km rồi ngược dòng $15$ km hết $2$ giờ $45$ phút. "
                "Nếu du thuyền chạy xuôi dòng $30$ km rồi ngược dòng $20$ km thì hết $3$ giờ $30$ phút. "
                "Tính vận tốc thực của du thuyền và vận tốc của dòng nước (biết vận tốc thực của du thuyền và dòng nước không đổi; gợi ý mồi: $v_{\\text{xuôi}} = v_{\\text{thực}} + v_n$)."
            ),
            dap_an=[
                y(
                    "",
                    2.0,
                    [
                        ("Đổi: $2$ giờ $45$ phút $= \\dfrac{11}{4}$ giờ; $3$ giờ $30$ phút $= \\dfrac{7}{2}$ giờ."),
                        ("Gọi vận tốc thực của du thuyền là $x$ (km/h), vận tốc dòng nước là $y$ (km/h).", 0.25),
                        ("Điều kiện: $x > y > 0$."),
                        ("Vận tốc du thuyền khi xuôi dòng là: $x + y$ (km/h)."),
                        ("Vận tốc du thuyền khi ngược dòng là: $x - y$ (km/h)."),
                        ("Thời gian du thuyền đi tour thứ nhất là: $\\dfrac{25}{x + y} + \\dfrac{15}{x - y} = \\dfrac{11}{4}$ (1)", 0.5),
                        ("Thời gian du thuyền đi tour thứ hai là: $\\dfrac{30}{x + y} + \\dfrac{20}{x - y} = \\dfrac{7}{2}$ (2)", 0.5),
                        ("Đặt $u = \\dfrac{1}{x + y}$ và $v = \\dfrac{1}{x - y}$ ($u, v > 0$)."),
                        ("Hệ phương trình trở thành: $\\begin{cases} 25u + 15v = \\dfrac{11}{4} \\\\ 30u + 20v = \\dfrac{7}{2} \\end{cases}$"),
                        ("Nhân phương trình đầu với $4$, phương trình hai với $3$: $\\begin{cases} 100u + 60v = 11 \\\\ 90u + 60v = 10{,}5 \\end{cases}$"),
                        ("Trừ hai phương trình: $10u = 0{,}5 \\Rightarrow u = \\dfrac{1}{20}$."),
                        ("Thay vào: $25 \\cdot \\dfrac{1}{20} + 15v = \\dfrac{11}{4} \\Rightarrow 15v = \\dfrac{11}{4} - \\dfrac{5}{4} = \\dfrac{6}{4} = \\dfrac{3}{2} \\Rightarrow v = \\dfrac{1}{10}$."),
                        ("Suy ra: $\\begin{cases} x + y = 20 \\\\ x - y = 10 \\end{cases}$"),
                        ("Cộng hai phương trình: $2x = 30 \\Rightarrow x = 15$."),
                        ("Trừ hai phương trình: $2y = 10 \\Rightarrow y = 5$.", 0.5),
                        ("Các giá trị $x = 15; y = 5$ thoả mãn điều kiện $x > y > 0$."),
                        ("Vậy vận tốc thực của du thuyền là $15$ km/h và vận tốc dòng nước là $5$ km/h.", 0.25),
                    ],
                )
            ],
            mt=[("II", "Toán thực tế chuyển động xuôi dòng, ngược dòng (lập hệ phương trình mồi)", "ĐS I", "VD", 2.0, 15, "THCS Trưng Vương (2025–2026)")],
            note="Bài toán mồi rèn luyện giải hệ bằng đặt ẩn phụ. Lỗi phổ biến: không đổi đơn vị phút sang giờ, hoặc nhầm lẫn giữa vận tốc thực với vận tốc xuôi/ngược dòng.",
        ),
        dict(
            label="Bài III.",
            level=2,
            statement=(
                "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                + BR
                + "1) \\textbf{(0,75 điểm)} $\\begin{cases} (x + 2)(y - 3) = xy \\\\ (x - 1)(y - 2) = xy \\end{cases}$"
                + BR
                + "2) \\textbf{(0,75 điểm)} $\\dfrac{x}{x-2} + \\dfrac{2}{x+1} = \\dfrac{6}{(x-2)(x+1)}$"
                + BR
                + "3) \\textbf{(0,5 điểm)} $5x - 1 > 3x + 3$"
            ),
            dap_an=[
                y(
                    "1)",
                    0.75,
                    [
                        ("Ta có: khai triển hai vế của từng phương trình trong hệ:"),
                        ("$\\begin{cases} xy - 3x + 2y - 6 = xy \\\\ xy - 2x - y + 2 = xy \\end{cases}$", 0.25),
                        ("Trừ $xy$ ở cả hai vế: $\\begin{cases} -3x + 2y = 6 \\\\ -2x - y = -2 \\end{cases}$"),
                        ("Từ phương trình thứ hai: $y = 2 - 2x$. Thế vào phương trình đầu:"),
                        ("$-3x + 2(2 - 2x) = 6 \\Rightarrow -3x + 4 - 4x = 6 \\Rightarrow -7x = 2 \\Rightarrow x = -\\dfrac{2}{7}$."),
                        ("Thay $x$ vào tìm $y$: $y = 2 - 2\\left(-\\dfrac{2}{7}\\right) = 2 + \\dfrac{4}{7} = \\dfrac{18}{7}$.", 0.25),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = \\left(-\\dfrac{2}{7}; \\dfrac{18}{7}\\right)$.", 0.25),
                    ],
                ),
                y(
                    "2)",
                    0.75,
                    [
                        ("Điều kiện xác định: $x \\ne 2$ và $x \\ne -1$."),
                        ("Quy đồng và khử mẫu số: $x(x + 1) + 2(x - 2) = 6$", 0.25),
                        ("$x^2 + x + 2x - 4 = 6$"),
                        ("$x^2 + 3x - 10 = 0$"),
                        ("$(x - 2)(x + 5) = 0$"),
                        ("$x = 2$ hoặc $x = -5$", 0.25),
                        ("Đối chiếu ĐKXĐ: $x = 2$ không thoả mãn (loại); $x = -5$ thoả mãn."),
                        ("Vậy phương trình có nghiệm duy nhất $x = -5$.", 0.25),
                    ],
                ),
                y(
                    "3)",
                    0.5,
                    [
                        ("Chuyển vế đổi dấu: $5x - 3x > 3 + 1$"),
                        ("$2x > 4$", 0.25),
                        ("$x > 2$"),
                        ("Vậy nghiệm của bất phương trình là $x > 2$.", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IIIa", "Giải hệ phương trình chứa tích biến đổi về bậc nhất", "ĐS I", "TH", 0.75, 7, "Huyện Hoài Đức (2024–2025)"),
                ("IIIb", "Giải phương trình chứa ẩn ở mẫu có bẫy nghiệm ngoại lai", "ĐS I", "TH", 0.75, 7, "Huyện Hoài Đức (2024–2025)"),
                ("IIIc", "Giải bất phương trình bậc nhất một ẩn cơ bản", "ĐS II", "NB", 0.5, 4, "Quận Hai Bà Trưng (2024–2025)"),
            ],
            note="BẪY NGOẠI LAI: Giải ra hai nghiệm $x = 2$ và $x = -5$, nhưng $x = 2$ trùng ĐKXĐ nên BỊ LOẠI. HS không đối chiếu điều kiện sẽ bị trừ 0,25đ.",
        ),
        dict(
            label="Bài IV.",
            level=3,
            statement=(
                "\\textbf{(3,5 điểm)}"
                + BR
                + "1) \\textbf{(0,5 điểm)} Một chiếc thang dài $3{,}5$ m dựa vào tường thẳng đứng. Để đảm bảo thang không bị đổ khi sử dụng, người ta đặt chân thang tạo với mặt đất một góc an toàn là $70^\\circ$. Hỏi khi đó, chân thang cách chân tường một khoảng bằng bao nhiêu mét? (Kết quả làm tròn đến chữ số thập phân thứ nhất)."
                + BR
                + "2) \\textbf{(3,0 điểm)} Cho đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $C$ thuộc $(O; R)$ sao cho $AC > BC$. Kẻ đường cao $CH$ của $\\triangle ABC$ ($H \\in AB$), kéo dài $CH$ cắt $(O; R)$ tại điểm thứ hai là $D$ ($D \\ne C$)."
                + BR
                + "Tiếp tuyến tại điểm $A$ và tiếp tuyến tại điểm $C$ của đường tròn $(O; R)$ cắt nhau tại điểm $M$. Gọi $I$ là giao điểm của $OM$ và $AC$. Hai đường thẳng $MC$ và $AB$ cắt nhau tại điểm $F$."
                + BR
                + "a) \\textbf{(1,0 điểm)} Chứng minh bốn điểm $A, C, M, O$ cùng thuộc một đường tròn."
                + BR
                + "b) \\textbf{(1,0 điểm)} Chứng minh $OM \\perp AC$ tại $I$ và $BC = 2 \\cdot IO$."
                + BR
                + "c) \\textbf{(1,0 điểm)} Chứng minh đường thẳng $FD$ là tiếp tuyến của $(O; R)$ và $AF \\cdot BH = BF \\cdot AH$."
            ),
            figure={"tikz": TIKZ_THANG, "caption": "Minh hoạ Bài IV.1"},
            hinh_da=HINH_ON3,
            dap_an=[
                y(
                    "1)",
                    0.5,
                    [
                        ("Gọi $B$ là chân tường, $A$ là điểm tiếp xúc của đầu thang với tường, $C$ là vị trí chân thang trên mặt đất."),
                        ("Khi đó tam giác $ABC$ vuông tại $B$, có $AC = 3{,}5$ m và góc $\\widehat{ACB} = 70^\\circ$."),
                        ("Xét tam giác $ABC$ vuông tại $B$, ta có khoảng cách từ chân thang tới chân tường là: $BC = AC \\cdot \\cos \\widehat{ACB}$", 0.25),
                        ("$BC = 3{,}5 \\cdot \\cos 70^\\circ \\approx 3{,}5 \\cdot 0{,}3420 \\approx 1{,}2$ (m)."),
                        ("Vậy chân thang cách chân tường một khoảng xấp xỉ $1{,}2$ mét.", 0.25),
                    ],
                ),
                y(
                    "2a)",
                    1.0,
                    [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Vì $MA$ là tiếp tuyến của $(O)$ tại $A$ nên $MA \\perp OA \\Rightarrow \\widehat{MAO} = 90^\\circ$."),
                        ("Vì $MC$ là tiếp tuyến của $(O)$ tại $C$ nên $MC \\perp OC \\Rightarrow \\widehat{MCO} = 90^\\circ$.", 0.25),
                        ("Xét tam giác $MAO$ vuông tại $A \\Rightarrow$ ba điểm $M, A, O$ cùng thuộc đường tròn đường kính $MO$."),
                        ("Xét tam giác $MCO$ vuông tại $C \\Rightarrow$ ba điểm $M, C, O$ cùng thuộc đường tròn đường kính $MO$.", 0.25),
                        ("Do đó bốn điểm $A, C, M, O$ cùng thuộc đường tròn đường kính $MO$.", 0.25),
                    ],
                ),
                y(
                    "2b)",
                    1.0,
                    [
                        ("Theo tính chất hai tiếp tuyến cắt nhau, ta có $MA = MC$ và $OA = OC = R$."),
                        ("Suy ra $OM$ là đường trung trực của đoạn thẳng $AC$."),
                        ("Do đó $OM \\perp AC$ tại $I$ (và $I$ là trung điểm của $AC$).", 0.25),
                        ("Tam giác $ABC$ nội tiếp đường tròn $(O)$ có cạnh $AB$ là đường kính nên $\\widehat{ACB} = 90^\\circ$."),
                        ("Suy ra $AC \\perp BC$. Mà $OM \\perp AC$ nên $OM \\parallel BC$.", 0.25),
                        ("Trong $\\triangle ABC$, ta có $I$ là trung điểm của $AC$ và $O$ là trung điểm của $AB$."),
                        ("Suy ra $IO$ là đường trung bình của tam giác $ABC$.", 0.25),
                        ("Do đó $IO = \\dfrac{1}{2}BC \\Rightarrow BC = 2 \\cdot IO$ (điều phải chứng minh).", 0.25),
                    ],
                ),
                y(
                    "2c)",
                    1.0,
                    [
                        ("Đường kính $AB \\perp CD$ tại $H$ nên $H$ là trung điểm của $CD$ (định lí đường kính vuông góc với dây cung)."),
                        ("Do đó $AB$ là đường trung trực của đoạn thẳng $CD$."),
                        ("Vì $F \\in AB$ nên $FC = FD$, suy ra $\\triangle FCD$ cân tại $F$."),
                        ("Xét $\\triangle FCO$ và $\\triangle FDO$: có $FC = FD$, $OC = OD = R$, cạnh $FO$ chung $\\Rightarrow \\triangle FCO = \\triangle FDO$ (c.c.c)", 0.25),
                        ("Suy ra $\\widehat{FDO} = \\widehat{FCO} = 90^\\circ \\Rightarrow FD \\perp OD$ tại $D$."),
                        ("Vậy $FD$ là tiếp tuyến của $(O; R)$.", 0.25),
                        ("Chứng minh $AF \\cdot BH = BF \\cdot AH$:"),
                        ("Vì $FC$ và $FA$ là hai tiếp tuyến của $(O)$? Không, $F \\in AB$, $FC$ là tiếp tuyến tại $C$."),
                        ("Xét tam giác $ACH$ vuông tại $H$ và tam giác $ABC$ vuông tại $C$: $\\widehat{CAH}$ chung $\\Rightarrow \\triangle ACH \\backsim \\triangle ABC$ (g.g)"),
                        ("$\\Rightarrow \\dfrac{AH}{AC} = \\dfrac{AC}{AB} \\Rightarrow AC^2 = AH \\cdot AB$."),
                        ("Tương tự $\\triangle BCH \\backsim \\triangle BAC$ (g.g) $\\Rightarrow BC^2 = BH \\cdot AB$."),
                        ("Suy ra $\\dfrac{AH}{BH} = \\dfrac{AC^2}{BC^2}$ (5)", 0.25),
                        ("Mặt khác, trong $\\triangle FBC$ có đường phân giác?"),
                        ("Xét hai tam giác đồng dạng $\\triangle FAC$ và $\\triangle FCB$: có góc $\\widehat{AFC}$ chung, $\\widehat{FCA} = \\widehat{FBC}$ (cùng chắn cung $AC$) $\\Rightarrow \\triangle FAC \\backsim \\triangle FCB$ (g.g)."),
                        ("Suy ra $\\dfrac{AF}{CF} = \\dfrac{AC}{BC}$ và $\\dfrac{CF}{BF} = \\dfrac{AC}{BC} \\Rightarrow \\dfrac{AF}{BF} = \\left(\\dfrac{AC}{BC}\\right)^2$ (6)"),
                        ("Từ (5) và (6) suy ra: $\\dfrac{AF}{BF} = \\dfrac{AH}{BH} \\Rightarrow AF \\cdot BH = BF \\cdot AH$ (điều phải chứng minh).", 0.25),
                    ],
                ),
            ],
            mt=[
                ("IVa", "Toán thực tế: Tỉ số lượng giác cos tính khoảng cách chân thang", "HH IV", "NB", 0.5, 5, "THCS Ái Mộ (2025–2026)"),
                ("IVb1", "Bốn điểm cùng thuộc một đường tròn", "HH V", "NB", 1.0, 7, "THCS Ái Mộ (2025–2026)"),
                ("IVb2", "Đường trung trực và đường trung bình của tam giác", "HH V", "TH", 1.0, 10, "THCS Ái Mộ (2025–2026)"),
                ("IVb3", "Chứng minh tiếp tuyến thứ hai và hệ thức phân giác/tỉ số đồng dạng", "HH V", "VDC", 1.0, 12, "THCS Ái Mộ (2025–2026)"),
            ],
            note="Bài hình: Câu c có thể chứng minh qua tam giác đồng dạng FAC và FCB chung góc F.",
        ),
        dict(
            label="Bài V.",
            level=4,
            statement=(
                "\\textbf{(0,5 điểm)} Chuẩn bị đón năm mới, bạn Lan dự định trang trí bảng tin của lớp bằng các hoạ tiết hình vuông. "
                "Để tạo ra các hình vuông, bạn Lan cắt một sợi dây ruy-băng dài $60$ cm thành ba đoạn nhỏ. "
                "Sau đó, mỗi đoạn nhỏ được uốn lại vừa khít thành một hình vuông. "
                "Hỏi bạn Lan phải chia sợi dây thành ba đoạn có độ dài như thế nào để tổng diện tích của ba hình vuông tạo thành đạt giá trị nhỏ nhất?"
            ),
            dap_an=[
                y(
                    "",
                    0.5,
                    [
                        ("Gọi độ dài ba đoạn dây sau khi cắt lần lượt là $a, b, c$ (cm)."),
                        ("Điều kiện: $a, b, c > 0$ và $a + b + c = 60$."),
                        ("Khi uốn mỗi đoạn dây thành một hình vuông thì chu vi của ba hình vuông lần lượt là $a, b, c$."),
                        ("Độ dài cạnh của ba hình vuông lần lượt là $\\dfrac{a}{4}, \\dfrac{b}{4}, \\dfrac{c}{4}$ (cm)."),
                        ("Tổng diện tích ba hình vuông là: $S = \\left(\\dfrac{a}{4}\\right)^2 + \\left(\\dfrac{b}{4}\\right)^2 + \\left(\\dfrac{c}{4}\\right)^2 = \\dfrac{a^2 + b^2 + c^2}{16}$ ($cm^2$).", 0.25),
                        ("Áp dụng bất đẳng thức Bunhiacôpxki (Cauchy-Schwarz) cho hai bộ ba số $(a, b, c)$ và $(1, 1, 1)$:"),
                        ("$(a^2 + b^2 + c^2)(1^2 + 1^2 + 1^2) \\ge (a \\cdot 1 + b \\cdot 1 + c \\cdot 1)^2$"),
                        ("$3(a^2 + b^2 + c^2) \\ge (a + b + c)^2 = 60^2 = 3600$"),
                        ("$\\Rightarrow a^2 + b^2 + c^2 \\ge \\dfrac{3600}{3} = 1200$."),
                        ("Suy ra: $S = \\dfrac{a^2 + b^2 + c^2}{16} \\ge \\dfrac{1200}{16} = 75$ ($cm^2$)."),
                        ("Dấu ``$=$'' xảy ra khi $\\dfrac{a}{1} = \\dfrac{b}{1} = \\dfrac{c}{1} \\Rightarrow a = b = c = \\dfrac{60}{3} = 20$ (cm)."),
                        ("Vậy Lan cần chia đoạn dây thành ba phần bằng nhau, mỗi đoạn dài $20$ cm để tổng diện tích đạt giá trị nhỏ nhất là $75\\text{ cm}^2$.", 0.25),
                    ],
                )
            ],
            mt=[("V", "Bài toán cực trị đại số: Bất đẳng thức Bunhiacôpxki uốn dây hình vuông", "ĐS II", "VDC", 0.5, 8, "Quận Hai Bà Trưng (2024–2025)")],
            note="Học sinh có thể biến đổi tương đương đưa về tổng các bình phương: $3(x^2+y^2+z^2) - (x+y+z)^2 = (x-y)^2 + (y-z)^2 + (z-x)^2 \\ge 0$ hoàn toàn phù hợp lớp 9.",
        ),
    ],
    bay=[
        ("Bài I.3", "Giải BPT $P < 1$ chứa căn", "Giải ra $0 \\le x < 9$ nhưng quên điều kiện $x \\ne 4$ (bị trừ 0,25đ).", "Phải kết hợp ĐỦ điều kiện xác định ban đầu: $0 \\le x < 9$ VÀ $x \\ne 4$."),
        ("Bài II", "Toán chuyển động dòng nước", "Quên đổi $2$h$45$p $= 11/4$ giờ, $3$h$30$p $= 7/2$ giờ (sai toàn bộ phương trình).", "Luôn đổi đơn vị thời gian ra giờ trước khi lập phương trình vận tốc."),
        ("Bài III.2", "Phương trình phân thức (BẪY NGOẠI LAI)", "Giải ra $x = 2$ và $x = -5$, kết luận cả hai nghiệm (bị trừ 0,25đ).", "ĐKXĐ $x \\ne 2$ nên nghiệm $x = 2$ phải ghi (loại), chỉ kết luận nghiệm duy nhất $x = -5$."),
        ("Bài IV.1", "Góc an toàn chiếc thang", "Dùng $\\sin 70^\\circ$ tính chiều cao tường thay vì khoảng cách chân thang.", "Khoảng cách chân thang là cạnh kề góc $70^\\circ$, dùng $\\cos 70^\\circ = \\text{kề} / \\text{huyền}$."),
        ("Bài IV.2c", "Chứng minh tiếp tuyến thứ hai", "Không chứng minh tam giác bằng nhau để suy ra góc vuông $90^\\circ$.", "Chứng minh $\\triangle FCO = \\triangle FDO$ (c.c.c) để suy ra $\\widehat{FDO} = 90^\\circ \\Rightarrow FD$ là tiếp tuyến."),
    ],
)


# ─────────────────────────── KIỂM NGUỒN ───────────────────────────
def kiem_nguon():
    tq = {}
    tt = {}
    bao_cao = {}
    for k, D in DE.items():
        q = {}
        for b in D["bai"]:
            for r in b["mt"]:
                quan = QUAN[r[6]]
                q[quan] = q.get(quan, 0.0) + r[4]
                tq[quan] = tq.get(quan, 0.0) + r[4]
                tt[r[6]] = tt.get(r[6], 0.0) + r[4]
        assert len(q) >= 4, f"Đề {k} chỉ có {len(q)} quận: {q}"
        assert max(q.values()) <= 4.0 + 1e-9, f"Đề {k} có quận vượt quá 40% điểm: {q}"
        truong = {r[6] for b in D["bai"] for r in b["mt"]}
        bao_cao[k] = (len(truong), q)
    assert max(tq.values()) <= 7.5 + 1e-9, f"Cả bộ có quận vượt quá 25% điểm (7,5đ): {tq}"
    assert max(tt.values()) <= 4.5 + 1e-9, f"Cả bộ có trường vượt quá 15% điểm (4,5đ): {tt}"
    return bao_cao, tq


# ─────────────────────────── DỰNG JSON ───────────────────────────
KIND = ["review", "concept", "practice1", "practice2", "reflection"]


def bang_mt(rows):
    s = (
        "\\vspace{-6pt}\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n"
        "\\begin{tabular}{|c|p{5.4cm}|c|c|c|c|p{2.9cm}|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề} \\\\ \\hline\n"
    )
    tong_d = tong_p = 0
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {ph} & {ng} \\\\ \\hline\n"
        tong_d += di
        tong_p += ph
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG CỘNG}}}} & \\textbf{{{d(tong_d)}}} & \\textbf{{{tong_p}}} & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tong_d, tong_p


def bang_muc(rows):
    muc = {"NB": 0, "TH": 0, "VD": 0, "VDC": 0}
    ds = {"Đại số (Chương I, II, III)": dict(muc), "Hình học (Chương IV, V)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        mach = "Hình học (Chương IV, V)" if ch.startswith("HH") else "Đại số (Chương I, II, III)"
        ds[mach][m] += di
    s = (
        "\\noindent\\textbf{TỔNG HỢP THEO MẠCH KIẾN THỨC VÀ CẤP ĐỘ (điểm)} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n"
    )
    tot = dict(muc)
    for k, v in ds.items():
        s += f"{k} & " + " & ".join(d(v[m]) if v[m] else "0" for m in muc) + f" & \\textbf{{{d(sum(v.values()))}}} \\\\ \\hline\n"
        for m in muc:
            tot[m] += v[m]
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tot[m]) if tot[m] else '0'}}}" for m in muc) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{round(tot[m]*10)}\\%" for m in muc) + " & 100\\% \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tot


def bang_bay(rows):
    s = (
        "\\noindent\\textbf{CẨM NANG CHUYÊN ĐỀ: CÁC BẪY TỬ HUYỆT \\& LỖI SAI THƯỜNG GẶP} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.1}\n"
        "\\begin{tabular}{|c|p{3.6cm}|p{4.3cm}|p{4.7cm}|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Bẫy đánh lừa} & \\textbf{Lỗi sai hay gặp (Mất điểm)} & \\textbf{Cách xử lý an toàn (Ăn trọn điểm)} \\\\ \\hline\n"
    )
    for c, b, l, k in rows:
        s += f"{c} & {b} & {l} & {k} \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


TIEN_BO = [
    ("Căn thức \\& câu phụ (2,0đ)", "Ia: Tính giá trị $x = 7-4\\sqrt{3}$; Ib: Rút gọn mẫu đối; Ic: Giải PT $P = \\sqrt{x}$", "Ia: Tính giá trị $x = 9$; Ib: Rút gọn mẫu $x-9$; Ic: BPT $P \\le -\\frac{1}{3}$", "Ia: Tính giá trị $x = 4-2\\sqrt{3}$; Ib: Rút gọn mẫu $x-9$; Ic: Tìm $x$ nguyên để $P$ nguyên"),
    ("Toán thực tế lập hệ (2,0đ)", "Hai vòi nước cùng chảy (toán năng suất công việc)", "Khuyến mại giảm giá hai mặt hàng điện tử", "Hai xe khởi hành ngược chiều gặp nhau (chuyển động)"),
    ("Giải PT, BPT, hệ (2,0đ)", "IIIa: Hệ cộng đại số; IIIb: PT tích; IIIc: BPT đổi chiều", "IIIa: Hệ phương pháp thế; IIIb: PT tích khai triển; IIIc: BPT nguyên", "IIIa: Hệ đặt ẩn phụ; IIIb: PT ẩn ở mẫu; IIIc: BPT phân số"),
    ("Lượng giác thực tế (0,5đ)", "Chiều cao tháp bằng $\\tan 40^\\circ$ (khoảng cách $135$ m)", "Độ sâu tàu ngầm bằng $\\sin 30^\\circ$ (quãng đường lặn)", "Chiều cao thang dựa tường bằng $\\sin 70^\\circ$ (thang $3{,}5$ m)"),
    ("Hình học đường tròn (3,0đ)", "Tiếp tuyến cắt nhau; $OA \\perp BC$; $CD \\parallel OA$; góc nội tiếp nửa đường tròn", "4 điểm đường tròn; $Ax, By$ tiếp tuyến; $AC \\cdot BD = R^2$; góc vuông", "Tiếp tuyến cắt nhau; $MH \\perp AB$; tiếp tuyến song song; trung điểm"),
    ("Câu cuối tối ưu / VDC (0,5đ)", "Tối ưu diện tích hình chữ nhật rào lưới: $S = -(x-20)^2 + 400$", "Tối ưu chi phí xây bể nước hình hộp: dùng BĐT Cosi", "Tối ưu doanh thu bán điện thoại: $-(x-5)^2 + 100$"),
]


def bang_tien_bo():
    s = (
        "\\noindent\\textbf{BẢN ĐỒ DẠNG BÀI QUA 3 ĐỀ ÔN TẬP:} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{2.6cm}|p{4.0cm}|p{4.0cm}|p{4.0cm}|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{Đề ôn tập số 1} & \\textbf{Đề ôn tập số 2} & \\textbf{Đề ôn tập số 3} \\\\ \\hline\n"
    )
    for r in TIEN_BO:
        s += " & ".join(r) + " \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def bang_theo_doi():
    s = (
        "\\noindent\\textbf{PHIẾU THEO DÕI TIẾN BỘ CỦA HỌC SINH:} [[br]] "
        "\\textit{\\footnotesize Ghi điểm từng bài kiểm tra để đánh giá sự tiến bộ qua 3 đề ôn; bài nào chưa đạt cần tra lại bảng dạng để luyện thêm.} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.3}\n"
        "\\begin{tabular}{|p{7.2cm}|c|c|c|c|}\n\\hline\n"
        "\\textbf{Bài (điểm tối đa)} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{Đạt chuẩn?} \\\\ \\hline\n"
    )
    for b in [
        "Bài I -- Căn thức và câu hỏi phụ (2,0đ)",
        "Bài II -- Toán thực tế lập hệ PT (2,0đ)",
        "Bài III -- Phương trình, BPT, Hệ PT (2,0đ)",
        "Bài IV -- Lượng giác \\& Hình đường tròn (3,5đ)",
        "Bài V -- Bài toán tối ưu thực tế (0,5đ)",
        "\\textbf{Tổng điểm (10,0đ)}",
    ]:
        s += b + " & & & & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def de_json(k, D):
    stages = []
    for i, b in enumerate(D["bai"]):
        if b.get("figure") and b.get("hinh_da"):
            hinh_circle = "\\begin{center}\\adjustbox{max width=0.62\\linewidth}{" + b["hinh_da"] + "}\\end{center}"
            if len(b["dap_an"]) > 1:
                sol = b["dap_an"][0] + BR + hinh_circle + "\n" + BR.join(b["dap_an"][1:])
            else:
                sol = hinh_circle + "\n" + BR.join(b["dap_an"])
        else:
            sol = BR.join(b["dap_an"])
            if b.get("hinh_da"):
                sol = "\\begin{center}\\adjustbox{max width=0.62\\linewidth}{" + b["hinh_da"] + "}\\end{center}\n" + sol
        blk = dict(type="problem", label=b["label"], level=b["level"], statement=b["statement"], tier="onclass", solution=sol)
        if b.get("figure"):
            blk["figure"] = b["figure"]
        blocks = [blk]
        if i == len(D["bai"]) - 1:
            blocks.append(dict(type="para", text="\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}"))
        stages.append(dict(kind=KIND[i], number=i + 1, title="", blocks=blocks))
    tit = f"Đề ôn tập cuối học kì I — Số {k[-1]} (90 phút)"
    return dict(slug=D["slug_de"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 9", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


def mt_json(k, D):
    stages = []
    rows = [r for b in D["bai"] for r in b["mt"]]
    s_mt, tong_d, tong_p = bang_mt(rows)
    s_muc, tot = bang_muc(rows)
    so = k[-1]

    # Stage 1: Ma trận đề thi + Bảng bẫy tử huyệt
    b1 = [
        dict(type="para", text=D["gioi_thieu"]),
        dict(type="para", text=f"\\textbf{{MA TRẬN ĐỀ ÔN TẬP SỐ {so} -- CUỐI KÌ I (90 PHÚT)}}" + BR + s_mt),
        dict(type="para", text=s_muc),
        dict(type="para", text=bang_bay(D["bay"])),
        dict(
            type="para",
            text="\\textbf{HƯỚNG DẪN SỬ DỤNG PHIẾU:}"
            + BR
            + D["cach_dung"]
            + BR
            + "\\textbf{Quy tắc chấm thi:} Mỗi bước biến đổi được tính điểm thành phần chi tiết bên phải dòng. Mỗi phép biến đổi viết trên một dòng riêng biệt. Bài hình phải chứng minh qua tam giác đồng dạng để suy ra hệ thức tích. Vẽ sai hình hoặc không vẽ hình thì không chấm điểm.",
        ),
    ]
    stages.append(dict(kind="review", number=1, title=f"Ma trận Đề ôn tập số {so}", blocks=b1))

    # Stages 2..5: Đáp án từng bài
    grp = [("Đáp án Bài I", [0]), ("Đáp án Bài II", [1]), ("Đáp án Bài III và Bài IV", [2, 3]), ("Đáp án Bài V và biểu điểm", [4])]
    for j, (ti, idx) in enumerate(grp, 2):
        blocks = []
        for i in idx:
            b = D["bai"][i]
            diem = sum(r[4] for r in b["mt"])
            tieu_de = f"\\textbf{{{b['label'].upper().replace('.', '')} ({d(diem)} điểm).}}"
            blocks.append(dict(type="para", text=tieu_de))
            if b.get("figure") and b.get("hinh_da"):
                cap1 = b["figure"].get("caption", "Minh hoạ Bài IV.1")
                blocks.append(dict(type="figure", tikz=b["figure"]["tikz"], width="0.5\\linewidth", caption=cap1))
                for a in b["dap_an"][:1]:
                    blocks.append(dict(type="para", text=a))
                blocks.append(dict(type="figure", tikz=b["hinh_da"], width="0.66\\linewidth"))
                for a in b["dap_an"][1:]:
                    blocks.append(dict(type="para", text=a))
            else:
                if b.get("hinh_da"):
                    blocks.append(dict(type="figure", tikz=b["hinh_da"], width="0.66\\linewidth"))
                if b.get("figure"):
                    blocks.append(dict(type="figure", tikz=b["figure"]["tikz"], width="0.5\\linewidth"))
                for a in b["dap_an"]:
                    blocks.append(dict(type="para", text=a))
            blocks.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + b["note"] + "}"))
        if j == 5:
            bd = BR.join(f"\\textbf{{{b['label']} ({d(sum(r[4] for r in b['mt']))}đ):}} " + " $-$ ".join(f"{r[0]} {d(r[4])}đ" for r in b["mt"]) for b in D["bai"])
            blocks.append(dict(type="para", text="\\textbf{BIỂU ĐIỂM TỔNG HỢP}" + BR + bd))
            blocks.append(
                dict(
                    type="para",
                    text="\\textbf{Tổng: 10,0 điểm.} Điểm toàn bài làm tròn đến $0{,}25$ điểm. Học sinh giải theo cách khác đúng vẫn cho điểm tối đa từng phần. Bài hình vẽ sai hình không chấm điểm.",
                )
            )
            nxt = {
                "1": "Đề ôn 2 nâng cao suy luận: câu phụ căn chứa số nguyên tố, hệ phương trình đặt ẩn phụ, bất phương trình đa thức và bài hình chứng minh thẳng hàng qua bổ đề hình thang.",
                "2": "Đề ôn 3 mở rộng các dạng: rút gọn căn bậc hai, giải bài toán chuyển động dòng nước hai tour du thuyền, phương trình phân thức ẩn ở mẫu và tiếp tuyến thứ hai.",
                "3": "Sau 3 đề ôn, học sinh đã bao quát 100\\% các dạng bài cốt lõi trong đề thi Cuối Kì I của các quận/huyện Hà Nội.",
            }[so]
            blocks.append(
                dict(
                    type="para",
                    text="\\textbf{KẾ HOẠCH BÀN GIAO TIẾP THEO}"
                    + BR
                    + nxt
                    + BR
                    + "Chữa bài: Ưu tiên chỉ ra các lỗi mất điểm trình bày (ĐKXĐ, đơn vị, kết luận, viết từng dòng) trước khi đi sâu vào các câu phân loại.",
                )
            )
            blocks.append(dict(type="para", text=bang_tien_bo()))
            blocks.append(dict(type="para", text=bang_theo_doi()))
        stages.append(dict(kind=KIND[j - 1], number=j, title=ti, blocks=blocks))

    tit = f"Ma trận đề và đáp án chi tiết — Đề ôn tập số {so}"
    return dict(slug=D["slug_mt"], title=tit, eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 9 • " + D["ten"], grade_label="Lớp 9", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


# ─────────────────────────── MAIN ───────────────────────────
if __name__ == "__main__":
    NGUON, NGUON_BO = kiem_nguon()
    print("✓ Kiểm tra rải nguồn thành công:")
    for _k, (_n, _q) in NGUON.items():
        print(f"  [{_k}] {_n} trường, {len(_q)} quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(_q.items(), key=lambda t: -t[1])))
    print("  Tổng cả bộ theo quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(NGUON_BO.items(), key=lambda t: -t[1])))

    for k, D in DE.items():
        p_de = OUT / f"{D['slug_de']}.json"
        p_mt = OUT / f"{D['slug_mt']}.json"
        p_de.write_text(json.dumps(de_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        p_mt.write_text(json.dumps(mt_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → Đã sinh: {p_de.name} và {p_mt.name}")
    print("Hoàn tất sinh 3 đề ôn tập CK1 lớp 9.")
