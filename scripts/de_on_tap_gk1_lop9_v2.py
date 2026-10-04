#!/usr/bin/env python3
"""BỘ ĐỀ ÔN GK1 LỚP 9 — PHIÊN BẢN 2 (03/10/2026: rải nguồn theo trường/quận, lưới dạng gắn tay 54 đề;
bản 1 giữ nguyên ở scripts/de_on_tap_gk1_lop9.py). Sinh 4 đề (Ôn 1, Ôn 2, Ôn 3, GK1 chính thức) + 4 file "Ma trận đề và
đáp án chi tiết" vào inputs/seeds/lop-9/de-on-tap-giua-ki-1-v2/ (khung đề tháng 9, theme de_thi,
trinh_bay "thoang"). Quy trình đầy đủ: docs/quy-trinh-bo-de-on-tap.md.

Mọi câu chép từ ẢNH đề gốc (KHÔNG từ ngân hàng — ngân hàng có câu chép sai). Đáp số đã kiểm SymPy.
SỬA ĐỀ THÌ SỬA Ở ĐÂY rồi chạy lại — không sửa tay JSON (sửa tay sẽ bị ghi đè).

Chạy:  .venv/bin/python scripts/de_on_tap_gk1_lop9_v2.py
       .venv/bin/python -m src.main build-folder inputs/seeds/lop-9/de-on-tap-giua-ki-1-v2
"""
import json
from pathlib import Path

OUT = Path("inputs/seeds/lop-9/de-on-tap-giua-ki-1-v2")
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem).rstrip('0').rstrip(',') if False else d(diem)}đ)}}" if diem else "")



import re as _re


def bo_tuong_duong(t):
    """HS đi thi KHÔNG dùng dấu ⇔ (Thầy 01/10/2026): mỗi phép biến đổi xuống một dòng.
    Cắt mọi đoạn toán $…$ tại \Leftrightarrow ở mức ngoặc 0, ngoài \begin…\end; bỏ dấu ⇔ đầu đoạn."""
    out = []
    for seg in _re.split(r"(\$[^$]*\$)", t):
        if not (seg.startswith("$") and seg.endswith("$") and len(seg) > 1):
            # câu văn mới (sau ". " hoặc ": " mà chữ kế là chữ HOA) xuống dòng
            seg = _re.sub(r"(?<=[.])\s+(?=[A-ZĐÂĂÊÔƠƯ])", BR, seg)
            out.append(seg); continue
        m = seg[1:-1]
        parts, depth, env, last, i = [], 0, 0, 0, 0
        while i < len(m):
            if m.startswith("\\begin", i): env += 1
            elif m.startswith("\\end", i): env -= 1
            c = m[i]
            if c == "{": depth += 1
            elif c == "}": depth -= 1
            elif depth == 0 and env == 0 and m.startswith("\\Leftrightarrow", i):
                parts.append(m[last:i]); i += len("\\Leftrightarrow"); last = i; continue
            i += 1
        parts.append(m[last:])
        parts = [p.strip() for p in parts if p.strip()]
        out.append(BR.join("$" + p + "$" for p in parts))
    s = "".join(out).strip()
    return _re.sub(r"^(?:\s*\[\[br\]\]\s*)+", "", s)


def y(nhan, diem, steps):
    than = BR.join(bo_tuong_duong(st(*s) if isinstance(s, tuple) else s) for s in steps)
    return (f"\\textbf{{{nhan} ({d(diem)}đ)}}" + BR + than) if nhan else than


# ─────────────────────────── HÌNH ───────────────────────────
def goc(cx, cy, a0, a1, r, nhan, rn):
    return (f"\\draw[line width=0.7pt] ({cx},{cy}) ++({a0}:{r}) arc ({a0}:{a1}:{r});"
            f"\\node at ($({cx},{cy})+({(a0+a1)/2}:{rn})$) {{{nhan}}};")


def vuong(x, y, dx, dy, s=0.3):
    """kí hiệu góc vuông tại (x,y), hai cạnh theo hướng (dx,0) và (0,dy)"""
    return f"\\draw[line width=0.6pt] ({x+dx*s},{y})--({x+dx*s},{y+dy*s})--({x},{y+dy*s});"


NEN = "\\foreach \\x in {{-0.3,0.0,...,{w}}} {{\\draw[gray!70,line width=0.5pt] (\\x,0)--(\\x-0.22,-0.22);}}"
# Hình bài III vẽ theo KÍCH THƯỚC THẬT (cm, scale=1): template co về 0,6 bề ngang / cao tối đa 7 cm
# nên hình thiết kế sẵn cỡ đó thì nhãn chữ giữ đúng cỡ chữ thường, không bị co li ti.
TIKZ_CAY = ("\\begin{tikzpicture}[line width=1pt,scale=0.55]"
            "\\coordinate (H) at (0,0);\\coordinate (B) at (3.4,0);\\coordinate (A) at (0,4.86);"
            "\\draw (-0.6,0)--(4.2,0);\\draw (H)--(A)--(B);" + vuong(0, 0, 1, 1)
            + goc(3.4, 0, 125, 180, 0.85, "$55^\\circ$", 1.4) +
            "\\node[left] at (A) {$A$};\\node[below left] at (H) {$H$};\\node[below right] at (B) {$B$};"
            "\\node[below=3pt] at (1.7,0) {$14{,}25$ m};\\path (-6.5,0) (10.9,0);\\end{tikzpicture}")
TIKZ_TAUNGAM = ("\\begin{tikzpicture}[line width=1pt]"
                "\\fill[gray!12] (-0.6,0) rectangle (6.8,-3.0);"
                "\\coordinate (A) at (0,0);\\coordinate (B) at (6,0);\\coordinate (C) at (6,-2.55);"
                "\\draw (-0.6,0)--(6.8,0);\\draw (A)--(C)--(B);" + vuong(6, 0, -1, -1)
                + goc(0, 0, -23, 0, 1.6, "$23^\\circ$", 2.15) +
                "\\node[above left] at (A) {$A$};\\node[above right] at (B) {$B$};\\node[below right] at (C) {$C$};"
                "\\node[right] at (6,-1.27) {$220$ m};\\end{tikzpicture}")
TIKZ_HACANH_TV = ("\\begin{tikzpicture}[line width=1.4pt,font=\\Large]"
                  "\\coordinate (H) at (0,0);\\coordinate (A) at (0,1.3);\\coordinate (B) at (9,0);"
                  "\\draw (-0.3,0)--(9.8,0);\\draw (A)--(B);\\draw[dashed] (A)--(H);" + vuong(0, 0, 1, 1, 0.3)
                  + goc(9, 0, 171.8, 180, 2.4, "$3^\\circ$", 3.0) +
                  "\\fill (A) circle (2.5pt);\\node[above left] at (A) {$A$};\\node[below left] at (H) {$H$};"
                  "\\node[below] at (B) {$B$};\\node[left] at (0,0.65) {$5$ km};\\path (-2.6,0) (11.6,0);\\end{tikzpicture}")
TIKZ_LOTTE = ("\\begin{tikzpicture}[line width=1pt,scale=0.7]"
              "\\coordinate (B) at (0,0);\\coordinate (A) at (1.15,0);\\coordinate (C) at (1.15,6.52);"
              "\\fill[gray!12] (1.15,0) rectangle (2.6,6.52);\\draw[gray!70,line width=0.6pt] (1.15,0) rectangle (2.6,6.52);"
              "\\foreach \\y in {1,...,12} {\\draw[gray!45,line width=0.5pt] (1.35,{\\y*0.5}) -- (2.4,{\\y*0.5});}"
              "\\draw (-0.6,0)--(3.2,0);\\draw (B)--(C)--(A);" + vuong(1.15, 0, -1, 1, 0.25)
              + goc(0, 0, 0, 80, 0.6, "", 1) +
              "\\node at (0.72,0.98) {$80^\\circ$};"
              "\\node[below left] at (B) {$B$};\\node[below] at (A) {$A$};\\node[above] at (C) {$C$};"
              "\\draw[<->,line width=0.6pt] (0,-0.75)--(1.15,-0.75);\\node[below] at (0.575,-0.75) {$48$ m};"
              "\\end{tikzpicture}")


def hinh(pts, segs, ticks=(), extra="", scale=1.7, dashed=()):
    s = f"\\begin{{tikzpicture}}[scale={scale},line width=1pt]"
    for k, (x, yy, pos) in pts.items():
        s += f"\\coordinate ({k}) at ({x:.3f},{yy:.3f});"
    for a, b in segs:
        s += f"\\draw ({a})--({b});"
    for a, b in dashed:
        s += f"\\draw[dashed] ({a})--({b});"
    s += extra
    for k, (x, yy, pos) in pts.items():
        s += f"\\fill ({k}) circle (1.8pt);\\node[{pos}] at ({k}) {{${k}$}};"
    return s + "\\end{tikzpicture}"


def vg(P, Q, R, s=0.16):
    """kí hiệu góc vuông tại Q (giữa QP và QR) — vẽ theo toạ độ"""
    import math
    (px, py), (qx, qy), (rx, ry) = P, Q, R
    u = ((px - qx), (py - qy)); lu = math.hypot(*u); u = (u[0] / lu * s, u[1] / lu * s)
    v = ((rx - qx), (ry - qy)); lv = math.hypot(*v); v = (v[0] / lv * s, v[1] / lv * s)
    return (f"\\draw[line width=0.5pt] ({qx+u[0]:.3f},{qy+u[1]:.3f})--({qx+u[0]+v[0]:.3f},{qy+u[1]+v[1]:.3f})"
            f"--({qx+v[0]:.3f},{qy+v[1]:.3f});")


import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
from de_on_tap_gk1_lop9_hinh_v2 import TOA_DO as T  # noqa: E402
c1 = {k: tuple(v) for k, v in T["on1"].items()}
HINH_ON1 = hinh({"A": (*c1["A"], "left"), "B": (*c1["B"], "above"), "C": (*c1["C"], "right"),
                 "H": (*c1["H"], "above right"), "M": (*c1["M"], "left"), "N": (*c1["N"], "below"),
                 "K": (*c1["K"], "below"), "I": (*c1["I"], "left")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("H", "M"), ("H", "N"), ("M", "N"),
                 ("A", "K"), ("C", "K"), ("B", "K")],
                extra=vg(c1["B"], c1["A"], c1["C"]) + vg(c1["A"], c1["H"], c1["C"]) + vg(c1["A"], c1["M"], c1["H"])
                + vg(c1["A"], c1["N"], c1["H"]))
c2 = {k: tuple(v) for k, v in T["on2"].items()}
HINH_ON2 = hinh({"A": (*c2["A"], "below left"), "B": (*c2["B"], "above"), "C": (*c2["C"], "below right"),
                 "H": (*c2["H"], "above right"), "D": (*c2["D"], "below left"), "K": (*c2["K"], "left"),
                 "M": (*c2["M"], "below"), "I": (*c2["I"], "above right")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("B", "M"), ("C", "M"), ("M", "I")],
                extra=vg(c2["B"], c2["A"], c2["C"]) + vg(c2["A"], c2["H"], c2["C"]) + vg(c2["B"], c2["M"], c2["C"]))
c3 = {k: (tuple(v) if isinstance(v, list) else v) for k, v in T["on3"].items()}
HINH_ON3 = hinh({"A": (*c3["A"], "below left"), "B": (*c3["B"], "above left"), "C": (*c3["C"], "below right"),
                 "M": (*c3["M"], "below"), "H": (*c3["H"], "above right"), "D": (*c3["D"], "right=2pt"),
                 "N": (*c3["N"], "above=2pt"), "E": (*c3["E"], "right")},
                [("A", "B"), ("B", "C"), ("C", "A"), ("A", "H"), ("B", "M"), ("A", "E"), ("C", "E"), ("M", "N")],
                dashed=[("N", "E")],
                extra=f"\\draw[gray] ({c3['O'][0]:.3f},{c3['O'][1]:.3f}) circle ({c3['r']:.3f});"
                + vg(c3["B"], c3["A"], c3["C"]) + vg(c3["A"], c3["H"], c3["C"]) + vg(c3["A"], c3["D"], c3["M"])
                + vg(c3["M"], c3["N"], c3["C"]) + vg(c3["A"], c3["C"], c3["E"]))
c4 = {k: tuple(v) for k, v in T["gk"].items()}
HINH_GK = hinh({"M": (*c4["M"], "below left"), "N": (*c4["N"], "above"), "P": (*c4["P"], "below right"),
                "H": (*c4["H"], "above right"), "E": (*c4["E"], "left"), "F": (*c4["F"], "below"),
                "Q": (*c4["Q"], "below"), "I": (*c4["I"], "right")},
               [("M", "N"), ("N", "P"), ("P", "M"), ("M", "H"), ("H", "E"), ("H", "F"), ("E", "F"),
                ("N", "Q"), ("M", "I")],
               dashed=[("H", "I")],
               extra=vg(c4["N"], c4["M"], c4["P"]) + vg(c4["M"], c4["H"], c4["P"]) + vg(c4["M"], c4["I"], c4["Q"]))


# ─────────────────────────── ĐỀ ───────────────────────────
# Mỗi bài: label, level, statement, figure(optional), dap_an (list ý), meta ma trận (list dòng)
DE = {}

DE["on-1"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 1", cach_dung="Cho HS làm như thi thật 90 phút, không gợi ý. Chữa ngay sau giờ: ưu tiên các ý mất điểm vì trình bày (ĐKXĐ, đơn vị, câu kết luận). Ghi điểm từng bài vào phiếu theo dõi tiến bộ (file đáp án đề GK1).", slug_de="de-on-tap-giua-ki-1-so-1-v2", slug_mt="ma-tran-va-dap-an-on-tap-so-1-v2",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP SỐ 1", ngat_truoc_III=True,
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 1 -- GIỮA HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} chỉ lấy các dạng có mặt ở hầu hết đề GK1 Hà Nội (thống kê gắn tay 54 đề, xem file "
                "Thong-ke-dang-GK1-Toan9-luoi-tay): PT tích ($90\\%$ số đề 2025--2026), PT chứa ẩn ở mẫu ($100\\%$), BPT ($69\\%$), "
                "hệ PT ($79\\%$), hai bài lập hệ ($100\\%$), tỉ số lượng giác thực tế ($93\\%$), hình tam giác vuông, câu tối ưu cuối đề ($90\\%$). "
                "Dạng lập BPT chỉ có ở khoảng một nửa số đề nên để ở Đề ôn 2 và đề GK1. "
                "Mỗi câu chép \\textbf{nguyên văn} từ đề của trường (ghi ở cột Nguồn)."),
    bai=[
        dict(label="Bài I.", level=2,
             statement="\\textbf{(3,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:" + BR +
             "a) \\textbf{(0,75 điểm)} $(2x-1)(x+5)=0$" + BR +
             "b) \\textbf{(0,75 điểm)} $\\dfrac{4}{x+3}+\\dfrac{x-1}{x-3}=\\dfrac{x^2+x}{x^2-9}$" + BR +
             "c) \\textbf{(0,75 điểm)} $4x-3>3(x-2)$" + BR +
             "d) \\textbf{(0,75 điểm)} $\\begin{cases}4x+y=9\\\\ x-y=6\\end{cases}$",
             dap_an=[
                 y("a)", 0.75, [("$(2x-1)(x+5)=0$"), ("$\\Leftrightarrow 2x-1=0$ hoặc $x+5=0$", 0.25),
                                ("$\\Leftrightarrow x=\\dfrac12$ hoặc $x=-5$.", 0.25),
                                ("Vậy phương trình có hai nghiệm $x=\\dfrac12$; $x=-5$.", 0.25)]),
                 y("b)", 0.75, [("ĐKXĐ: $x\\ne 3$; $x\\ne -3$. Mẫu chung $x^2-9=(x-3)(x+3)$.", 0.25),
                                ("Quy đồng, khử mẫu: $4(x-3)+(x-1)(x+3)=x^2+x$"),
                                ("$\\Leftrightarrow 4x-12+x^2+2x-3=x^2+x$"),
                                ("$\\Leftrightarrow 5x=15\\Leftrightarrow x=3$.", 0.25),
                                ("$x=3$ không thoả mãn ĐKXĐ. Vậy phương trình vô nghiệm.", 0.25)]),
                 y("c)", 0.75, [("$4x-3>3(x-2)\\Leftrightarrow 4x-3>3x-6$", 0.25), ("$\\Leftrightarrow 4x-3x>-6+3$", 0.25),
                                ("$\\Leftrightarrow x>-3$."),
                                ("Vậy nghiệm của bất phương trình là $x>-3$.", 0.25)]),
                 y("d)", 0.75, [("Cộng từng vế hai phương trình: $5x=15$", 0.25),
                                ("$\\Leftrightarrow x=3\\Rightarrow y=x-6=-3$.", 0.25),
                                ("Vậy hệ có nghiệm duy nhất $(x;y)=(3;-3)$.", 0.25)]),
             ],
             mt=[("Ia", "Giải phương trình tích $(ax+b)(cx+d)=0$", "ĐS II", "NB", 0.75, 4, "THCS Đền Lừ"),
                 ("Ib", "PT chứa ẩn ở mẫu (nghiệm bị loại $\\Rightarrow$ vô nghiệm)", "ĐS II", "TH", 0.75, 7, "THCS Ngô Gia Tự"),
                 ("Ic", "Giải BPT bậc nhất (bỏ ngoặc, chuyển vế)", "ĐS II", "NB", 0.75, 4, "THCS Đại Áng"),
                 ("Id", "Giải hệ hai PT bậc nhất hai ẩn (cộng đại số)", "ĐS I", "NB", 0.75, 5, "THCS Chúc Sơn")],
             note="Ý b là bẫy ĐKXĐ: HS giải ra $x=3$ mà quên loại sẽ mất 0,25đ cuối. Ý c: chấm việc chuyển vế đổi dấu ($-3$ sang vế phải thành $+3$)."),
        dict(label="Bài II.", level=3,
             statement="\\textbf{(3,0 điểm)} \\textit{Giải các bài toán sau bằng cách lập hệ phương trình.}" + BR +
             "1) \\textbf{(1,5 điểm)} Bạn Khánh đến cửa hàng mua hai cuốn sách với tổng giá niêm yết là $460$ nghìn đồng. Vì bạn Khánh đến mua "
             "đúng dịp cửa hàng có chương trình khuyến mại nên khi thanh toán giá cuốn sách thứ nhất giảm $20\\%$ so với "
             "giá niêm yết; giá cuốn sách thứ hai giảm $25\\%$ so với giá niêm yết. Do đó bạn chỉ phải trả $358$ nghìn đồng. "
             "Hỏi giá niêm yết của hai cuốn sách bạn Khánh mua là bao nhiêu tiền?" + BR +
             "2) \\textbf{(1,5 điểm)} Hai lớp $9A$ và $9B$ có tổng số $93$ học sinh. Hưởng ứng phong trào ``Kế hoạch nhỏ'', mỗi học sinh "
             "lớp $9A$ thu gom được trung bình $3$ kg giấy vụn, mỗi học sinh lớp $9B$ thu gom được trung bình $2$ kg giấy vụn. "
             "Kết thúc đợt, cả hai lớp đã thu gom được tổng cộng $231$ kg giấy vụn. Hỏi mỗi lớp có bao nhiêu học sinh?",
             dap_an=[
                 y("1)", 1.5, [("Gọi giá niêm yết của cuốn sách thứ nhất, thứ hai lần lượt là $x$, $y$ (nghìn đồng; $0<x,y<460$).", 0.25),
                               ("Tổng giá niêm yết là $460$ nghìn đồng: $x+y=460$ \\quad (1)", 0.25),
                               ("Giá sau giảm: cuốn thứ nhất còn $80\\%$ là $0{,}8x$; cuốn thứ hai còn $75\\%$ là $0{,}75y$."),
                               ("Bạn trả $358$ nghìn đồng: $0{,}8x+0{,}75y=358$ \\quad (2)", 0.25),
                               ("Từ (1): $y=460-x$. Thay vào (2): $0{,}8x+0{,}75(460-x)=358$"),
                               ("$\\Leftrightarrow 0{,}05x=13\\Leftrightarrow x=260$ (TMĐK) $\\Rightarrow y=200$ (TMĐK).", 0.5),
                               ("Vậy giá niêm yết cuốn thứ nhất là $260$ nghìn đồng, cuốn thứ hai là $200$ nghìn đồng.", 0.25)]),
                 y("2)", 1.5, [("Gọi số học sinh lớp $9A$, $9B$ lần lượt là $x$, $y$ (học sinh; $x,y\\in\\mathbb N^*$; $x,y<93$).", 0.25),
                               ("Hai lớp có $93$ học sinh: $x+y=93$ \\quad (1)", 0.25),
                               ("Hai lớp thu gom được $231$ kg giấy vụn: $3x+2y=231$ \\quad (2)", 0.25),
                               ("Từ (1): $y=93-x$. Thay vào (2): $3x+2(93-x)=231$"),
                               ("$\\Leftrightarrow x=45$ (TMĐK) $\\Rightarrow y=48$ (TMĐK).", 0.5),
                               ("Vậy lớp $9A$ có $45$ học sinh, lớp $9B$ có $48$ học sinh.", 0.25)]),
             ],
             mt=[("II.1", "Lập hệ PT -- mua bán có khuyến mại $\\%$", "ĐS I", "TH", 1.5, 12, "THCS Bát Tràng"),
                 ("II.2", "Lập hệ PT -- tổng số lượng, tổng khối lượng", "ĐS I", "TH", 1.5, 10, "THCS Giảng Võ")],
             note="Ý 1: lỗi hay gặp là viết giá sau giảm $0{,}2x$ thay vì $0{,}8x$. Ý 2 là khuôn lập hệ cơ bản nhất -- HS phải lấy trọn $1{,}5$đ, mất điểm thường do thiếu điều kiện $x,y\\in\\mathbb N^*$ hoặc thiếu câu trả lời."),
        dict(label="Bài III.", level=2,
             statement="\\textbf{(1,0 điểm)} Tại một thời điểm trong ngày, các tia nắng mặt trời tạo với mặt đất một góc bằng $55^\\circ$, "
             "bóng của một cây xanh trên mặt đất dài $14{,}25$ m. Tính chiều cao của cây (làm tròn kết quả đến chữ số thập phân thứ hai).",
             figure=dict(tikz=TIKZ_CAY, pos="right"),
             dap_an=[y("", 1.0, [("Gọi $AH$ là chiều cao cây, $HB=14{,}25$ m là bóng cây; $\\triangle AHB$ vuông tại $H$, $\\widehat{ABH}=55^\\circ$.", 0.25),
                                 ("$AH=HB\\cdot\\tan B=14{,}25\\cdot\\tan 55^\\circ\\approx 20{,}35$ (m).", 0.5),
                                 ("Vậy cây cao khoảng $20{,}35$ m.", 0.25)])],
             mt=[("III", "Ứng dụng tỉ số lượng giác: tính chiều cao (dùng $\\tan$)", "HH IV", "TH", 1.0, 5, "THCS Chuyên Mỹ")],
             note="Dạng một bước: chọn đúng tỉ số $\\tan$ (cạnh đối/cạnh kề) là lấy đủ điểm. Nhắc HS đặt máy tính ở chế độ độ (D)."),
        dict(label="Bài IV.", level=3,
             statement="\\textbf{(2,5 điểm)} Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$ ($H$ thuộc $BC$)." + BR +
             "a) \\textbf{(1,0 điểm)} Giả sử $AB=9$ cm, $\\tan C=\\dfrac34$. Giải tam giác $ABC$ (số đo góc làm tròn đến độ)." + BR +
             "b) \\textbf{(1,0 điểm)} Gọi $M$ và $N$ lần lượt là chân các đường vuông góc kẻ từ điểm $H$ đến các đường thẳng $AB$ và $AC$. "
             "Chứng minh rằng $HN\\cdot AC=HA\\cdot HC$ và $HN=AB\\cdot\\sin^2 B$." + BR +
             "c) \\textbf{(0,5 điểm)} Đường thẳng đi qua điểm $A$ và song song với đường thẳng $MN$ cắt đường thẳng đi qua điểm $C$ "
             "và song song với đường thẳng $AH$ tại điểm $K$. Gọi $I$ là giao điểm của $AH$ và $BK$. Chứng minh ba điểm $M$, $I$, $N$ thẳng hàng.",
             hinh_da=HINH_ON1,
             dap_an=[
                 y("a)", 1.0, [("Vẽ hình đúng (như hình vẽ).", 0.25),
                               ("Xét $\\triangle ABC$ vuông tại $A$: $AC=\\dfrac{AB}{\\tan C}=9:\\dfrac34=12$ (cm).", 0.25),
                               ("Theo định lí Pythagore: $BC=\\sqrt{AB^2+AC^2}=\\sqrt{81+144}=15$ (cm).", 0.25),
                               ("$\\tan C=\\dfrac34\\Rightarrow\\widehat{C}\\approx 37^\\circ\\Rightarrow\\widehat{B}=90^\\circ-\\widehat{C}\\approx 53^\\circ$.", 0.25),
                               ("Vậy $AC=12$ cm, $BC=15$ cm, $\\widehat{C}\\approx 37^\\circ$, $\\widehat{B}\\approx 53^\\circ$.")]),
                 y("b)", 1.0, [("Xét $\\triangle CNH$ và $\\triangle CHA$: $\\widehat{CNH}=\\widehat{CHA}=90^\\circ$, $\\widehat{ACH}$ chung"),
                               ("$\\Rightarrow\\triangle CNH\\backsim\\triangle CHA$ (g.g) $\\Rightarrow\\dfrac{HN}{AH}=\\dfrac{HC}{AC}\\Rightarrow HN\\cdot AC=HA\\cdot HC$.", 0.5),
                               ("$\\widehat{HAC}=\\widehat{ABC}$ (cùng phụ $\\widehat{ACB}$)."),
                               ("Xét $\\triangle AHB$ vuông tại $H$: $AH=AB\\cdot\\sin B$.", 0.25),
                               ("Xét $\\triangle ANH$ vuông tại $N$: $HN=AH\\cdot\\sin\\widehat{HAN}=AH\\cdot\\sin B=AB\\cdot\\sin^2 B$.", 0.25)]),
                 y("c)", 0.5, [("Tứ giác $AMHN$ có ba góc vuông $\\Rightarrow$ là hình chữ nhật. Gọi $O$ là giao điểm của $AH$ và $MN$"),
                               ("$\\Rightarrow OA=ON\\Rightarrow\\widehat{ANM}=\\widehat{OAN}=\\widehat{HAC}=\\widehat{ABC}$."),
                               ("$AK\\,/\\!/\\,MN\\Rightarrow\\widehat{KAC}=\\widehat{ANM}=\\widehat{ABC}$ (so le trong)."),
                               ("$CK\\,/\\!/\\,AH$, $AH\\perp BC\\Rightarrow CK\\perp BC\\Rightarrow\\widehat{ACK}=90^\\circ-\\widehat{ACB}=\\widehat{ABC}$."),
                               ("$\\Rightarrow\\triangle KAC$ cân tại $K$. Gọi $P$ là trung điểm của $AC$ $\\Rightarrow KP\\perp AC$"),
                               ("$\\Rightarrow KC=\\dfrac{CP}{\\cos\\widehat{KCA}}=\\dfrac{AC}{2\\cos B}$.", 0.25),
                               ("$IH\\,/\\!/\\,KC$ (cùng vuông góc với $BC$) $\\Rightarrow\\dfrac{IH}{KC}=\\dfrac{BH}{BC}$ (định lí Thalès)."),
                               ("$\\triangle ABH$ vuông tại $H$: $BH=AB\\cdot\\cos B$ $\\Rightarrow IH=\\dfrac{AC}{2\\cos B}\\cdot\\dfrac{AB\\cdot\\cos B}{BC}=\\dfrac{AB\\cdot AC}{2BC}$."),
                               ("Xét $\\triangle HBA$ và $\\triangle ABC$: $\\widehat{AHB}=\\widehat{CAB}=90^\\circ$, $\\widehat{B}$ chung $\\Rightarrow\\triangle HBA\\backsim\\triangle ABC$ (g.g)"),
                               ("$\\Rightarrow\\dfrac{AH}{CA}=\\dfrac{AB}{CB}\\Rightarrow AH=\\dfrac{AB\\cdot AC}{BC}\\Rightarrow IH=\\dfrac{AH}{2}$."),
                               ("$\\Rightarrow I$ là trung điểm của $AH$, tức $I\\equiv O$ $\\Rightarrow$ ba điểm $M$, $I$, $N$ thẳng hàng.", 0.25)]),
             ],
             mt=[("IVa", "Giải tam giác vuông biết một cạnh và $\\tan$ một góc", "HH IV", "TH", 1.0, 8, "THCS Văn Yên"),
                 ("IVb", "Đồng dạng g.g $\\Rightarrow$ hệ thức tích; hệ thức có $\\sin^2$", "HH IV", "VD", 1.0, 8, "THCS Văn Yên"),
                 ("IVc", "Tam giác cân + Thalès $\\Rightarrow$ trung điểm $\\Rightarrow$ thẳng hàng", "HH IV", "VDC", 0.5, 9, "THCS Văn Yên")],
             note="Ý c: mắt xích then chốt là nhìn ra $I$ chính là giao điểm hai đường chéo của hình chữ nhật $AMHN$, nên chỉ cần chứng minh $I$ là trung điểm $AH$. HS chưa làm được ý c vẫn cần lấy trọn a, b (2,0đ)."),
        dict(label="Bài V.", level=4,
             statement="\\textbf{(0,5 điểm)} Một cửa hàng chuyên kinh doanh máy tính tại Hà Nội. Một loại máy tính có giá nhập vào một chiếc "
             "là $18$ triệu đồng và bán ra với giá $22$ triệu đồng. Với giá bán như trên thì một năm số lượng máy tính bán được dự kiến "
             "là $500$ chiếc. Để tăng thêm lượng tiêu thụ dòng máy tính này, chủ cửa hàng dự định giảm giá bán và ước lượng cứ giảm "
             "$200$ nghìn đồng một chiếc thì số lượng máy tính bán ra trong năm sẽ tăng $50$ chiếc. Vậy cửa hàng phải bán với giá bao nhiêu "
             "để sau khi giảm giá lợi nhuận thu được sẽ cao nhất?",
             dap_an=[y("", 0.5, [("Gọi số lần giảm giá là $x$ ($x\\in\\mathbb N$, $x<20$). Đổi $200$ nghìn đồng $=0{,}2$ triệu đồng."),
                                 ("Lợi nhuận mỗi chiếc: $22-0{,}2x-18=4-0{,}2x$ (triệu đồng); số máy bán được: $500+50x$ (chiếc)."),
                                 ("Lợi nhuận một năm: $L=(4-0{,}2x)(500+50x)=-10x^2+100x+2000$"),
                                 ("$L=2250-10(x-5)^2\\le 2250$.", 0.25),
                                 ("Dấu ``$=$'' xảy ra khi $x=5$ $\\Rightarrow$ giá bán $22-0{,}2\\cdot 5=21$ (triệu đồng)."),
                                 ("Vậy cửa hàng bán mỗi chiếc $21$ triệu đồng thì lợi nhuận cao nhất ($2250$ triệu đồng một năm).", 0.25)])],
             mt=[("V", "Bài toán tối ưu thực tế: lợi nhuận (giảm giá -- tăng lượng bán)", "ĐS II", "VDC", 0.5, 8, "THCS Xuân Phương (2024--2025)")],
             note="Chấm theo đường hằng đẳng thức $2250-10(x-5)^2$; HS dùng công thức đỉnh parabol $x=-\\tfrac{b}{2a}$ là kiến thức lớp 10, nhắc lại cách trình bày lớp 9. Lỗi hay gặp: lấy giá bán thay vì lợi nhuận mỗi chiếc."),
    ])

DE["on-2"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 2", cach_dung="Làm sau khi đã chữa Đề ôn 1. So điểm từng bài với Đề ôn 1: bài nào không tăng thì cho HS làm lại đúng câu tương ứng ở Đề ôn 1 trước khi sang Đề ôn 3.", slug_de="de-on-tap-giua-ki-1-so-2-v2", slug_mt="ma-tran-va-dap-an-on-tap-so-2-v2",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP SỐ 2",
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 2 -- GIỮA HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} cùng các dạng tần suất cao như Đề ôn 1 nhưng \\textbf{khác bối cảnh và nâng một nấc suy luận}: "
                "BPT khai triển ra vô nghiệm, lập hệ theo năng suất tăng $\\%$, \\textbf{thêm dạng lập BPT} (có ở khoảng 1/2 đề trường), tỉ số lượng giác hai bước (quãng đường rồi thời gian), "
                "bài hình có tính chất đường phân giác và chứng minh trung điểm. Mỗi câu chép nguyên văn từ đề của trường."),
    bai=[
        dict(label="Bài I.", level=2,
             statement="\\textbf{(3,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:" + BR +
             "a) \\textbf{(0,75 điểm)} $(2x-5)(x-3)=0$" + BR +
             "b) \\textbf{(0,75 điểm)} $\\dfrac{x}{x-3}+\\dfrac{1}{x^2-3x}=\\dfrac{x-1}{x}$" + BR +
             "c) \\textbf{(0,75 điểm)} $3x(x-1)-(x+2)(2-x)>(2x+1)^2-7x$" + BR +
             "d) \\textbf{(0,75 điểm)} $\\begin{cases}4x-3y=7\\\\ x-2y=3\\end{cases}$",
             dap_an=[
                 y("a)", 0.75, [("$(2x-5)(x-3)=0\\Leftrightarrow 2x-5=0$ hoặc $x-3=0$", 0.25),
                                ("$\\Leftrightarrow x=\\dfrac52$ hoặc $x=3$.", 0.25),
                                ("Vậy phương trình có hai nghiệm $x=\\dfrac52$; $x=3$.", 0.25)]),
                 y("b)", 0.75, [("ĐKXĐ: $x\\ne 0$; $x\\ne 3$. Mẫu chung $x^2-3x=x(x-3)$.", 0.25),
                                ("Quy đồng, khử mẫu: $x\\cdot x+1=(x-1)(x-3)$"),
                                ("$\\Leftrightarrow x^2+1=x^2-4x+3\\Leftrightarrow 4x=2\\Leftrightarrow x=\\dfrac12$ (TMĐK).", 0.25),
                                ("Vậy phương trình có nghiệm $x=\\dfrac12$.", 0.25)]),
                 y("c)", 0.75, [("$3x(x-1)-(x+2)(2-x)>(2x+1)^2-7x$"),
                                ("$\\Leftrightarrow 3x^2-3x-(4-x^2)>4x^2+4x+1-7x$", 0.25),
                                ("$\\Leftrightarrow 4x^2-3x-4>4x^2-3x+1$"),
                                ("$\\Leftrightarrow 0\\cdot x>5$ (vô lí với mọi $x$).", 0.25),
                                ("Vậy bất phương trình vô nghiệm.", 0.25)]),
                 y("d)", 0.75, [("Từ phương trình thứ hai: $x=2y+3$.", 0.25),
                                ("Thế vào phương trình thứ nhất: $4(2y+3)-3y=7\\Leftrightarrow 5y=-5\\Leftrightarrow y=-1\\Rightarrow x=1$.", 0.25),
                                ("Vậy hệ có nghiệm duy nhất $(x;y)=(1;-1)$.", 0.25)]),
             ],
             mt=[("Ia", "Giải phương trình tích", "ĐS II", "NB", 0.75, 4, "THCS Cổ Nhuế 2"),
                 ("Ib", "PT chứa ẩn ở mẫu (phải phân tích mẫu $x^2-3x$)", "ĐS II", "TH", 0.75, 7, "THCS Trưng Vương"),
                 ("Ic", "BPT phải khai triển -- dạng bẫy vô nghiệm", "ĐS II", "TH", 0.75, 6, "THCS Trưng Vương"),
                 ("Id", "Giải hệ hai PT bậc nhất hai ẩn", "ĐS I", "NB", 0.75, 5, "THCS Cổ Nhuế 2")],
             note="Ý c: HS hay kết luận ``$x>\\ldots$'' vì quen tay. Rèn thói quen: thấy $0\\cdot x>5$ thì dừng lại kết luận vô nghiệm."),
        dict(label="Bài II.", level=3,
             statement="\\textbf{(3,0 điểm)}" + BR +
             "1) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập hệ phương trình.}" + BR +
             "Hai tổ sản xuất được giao kế hoạch làm $500$ bộ quần áo trong một thời gian nhất định. Do số lượng đơn hàng nhiều nên "
             "khi thực hiện, tổ I đã tăng năng suất thêm $15\\%$, tổ II tăng thêm $25\\%$ so với dự định. Vì vậy trong thời gian "
             "quy định, họ đã vượt chỉ tiêu $95$ bộ quần áo. Tính số bộ quần áo mỗi tổ phải làm theo kế hoạch ban đầu." + BR +
             "2) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập bất phương trình.}" + BR +
             "Trong đợt quyên góp ủng hộ các bạn học sinh bị lũ lụt, bạn Quân đã dùng $600\\,000$ đồng tiền tiết kiệm để mua "
             "$2$ loại vở. Biết một quyển vở Tiểu học giá $8\\,000$ đồng, một quyển vở Trung học giá $12\\,000$ đồng. "
             "Hỏi sau khi mua $40$ quyển vở Tiểu học thì bạn Quân mua được nhiều nhất bao nhiêu quyển vở Trung học?",
             dap_an=[
                 y("1)", 1.5, [("Gọi số bộ quần áo tổ I, tổ II phải làm theo kế hoạch lần lượt là $x$, $y$ (bộ; $x,y\\in\\mathbb N^*$; $x,y<500$).", 0.25),
                               ("Theo kế hoạch: $x+y=500$ \\quad (1)", 0.25),
                               ("Thực tế tổ I làm thêm $0{,}15x$ bộ, tổ II làm thêm $0{,}25y$ bộ; tổng số bộ làm thêm là $95$:"),
                               ("$0{,}15x+0{,}25y=95$ \\quad (2)", 0.25),
                               ("Từ (1): $y=500-x$. Thay vào (2): $0{,}15x+0{,}25(500-x)=95\\Leftrightarrow 0{,}1x=30$"),
                               ("$\\Leftrightarrow x=300$ (TMĐK) $\\Rightarrow y=200$ (TMĐK).", 0.5),
                               ("Vậy theo kế hoạch tổ I làm $300$ bộ, tổ II làm $200$ bộ quần áo.", 0.25)]),
                 y("2)", 1.5, [("Gọi số quyển vở Trung học bạn Quân mua được là $x$ (quyển, $x\\in\\mathbb N$).", 0.25),
                               ("Số tiền mua $40$ quyển vở Tiểu học: $40\\cdot 8\\,000=320\\,000$ (đồng).", 0.25),
                               ("Tổng số tiền không vượt quá $600\\,000$ đồng: $320\\,000+12\\,000x\\le 600\\,000$", 0.25),
                               ("$\\Leftrightarrow 12\\,000x\\le 280\\,000\\Leftrightarrow x\\le\\dfrac{70}{3}\\approx 23{,}3$.", 0.25),
                               ("$x$ là số tự nhiên lớn nhất thoả mãn $\\Rightarrow x=23$.", 0.25),
                               ("Vậy bạn Quân mua được nhiều nhất $23$ quyển vở Trung học.", 0.25)]),
             ],
             mt=[("II.1", "Lập hệ PT -- năng suất tăng $\\%$, vượt chỉ tiêu", "ĐS I", "TH", 1.5, 12, "THCS Cổ Nhuế 2"),
                 ("II.2", "Lập BPT thực tế -- ngân sách ``nhiều nhất bao nhiêu''", "ĐS II", "TH", 1.5, 8, "THCS Trưng Vương")],
             note="Ý 1 khác Đề ôn 1 ở chỗ phần trăm là phần TĂNG ($0{,}15x$), không phải phần còn lại. Ý 2 làm tròn XUỐNG (nhiều nhất), ngược Đề ôn 1."),
        dict(label="Bài III.", level=2,
             statement="\\textbf{(1,0 điểm)} Một chiếc tàu ngầm ở trên mặt biển lặn xuống và di chuyển theo một đường thẳng tạo với "
             "mặt nước biển một góc $23^\\circ$ (hình vẽ bên).",
             sau_hinh="1) \\textbf{(0,5 điểm)} Khi tàu ở độ sâu $BC=220$ m so với mặt nước biển thì tàu đã đi được quãng đường $AC$ "
             "dài bao nhiêu mét? (làm tròn đến hàng đơn vị của mét)" + BR +
             "2) \\textbf{(0,5 điểm)} Giả sử vận tốc của tàu là $18$ km/h. Hỏi tàu đi hết quãng đường $AC$ trong thời gian bao nhiêu giây?",
             figure=dict(tikz=TIKZ_TAUNGAM, pos="right"),
             dap_an=[y("1)", 0.5, [("Xét $\\triangle ABC$ vuông tại $B$: $AC=\\dfrac{BC}{\\sin A}=\\dfrac{220}{\\sin 23^\\circ}\\approx 563$ (m).", 0.25),
                                   ("Vậy tàu đã đi được quãng đường khoảng $563$ m.", 0.25)]),
                     y("2)", 0.5, [("Đổi $18$ km/h $=5$ m/s. Thời gian: $t=\\dfrac{AC}{5}=\\dfrac{220}{5\\sin 23^\\circ}\\approx 112{,}6$ (giây).", 0.25),
                                   ("Vậy tàu đi hết quãng đường $AC$ trong khoảng $113$ giây.", 0.25)])],
             mt=[("III.1", "Tỉ số lượng giác thực tế: tính quãng đường (dùng $\\sin$)", "HH IV", "TH", 0.5, 4, "THCS Tam Hiệp"),
                 ("III.2", "Ghép quãng đường -- thời gian, đổi km/h ra m/s", "HH IV", "VD", 0.5, 5, "THCS Tam Hiệp")],
             note="Ý 2 là bước tiến so với Đề ôn 1: phải đổi đơn vị ($18$ km/h $=5$ m/s) và ghép $t=\\dfrac{s}{v}$ sau khi tính cạnh. Dùng $AC\\approx 563$ m hay giá trị chưa làm tròn đều ra khoảng $112{,}6$ giây."),
        dict(label="Bài IV.", level=3,
             statement="\\textbf{(2,5 điểm)} Cho tam giác $ABC$ vuông tại $A$ ($AB<AC$)." + BR +
             "a) \\textbf{(0,75 điểm)} Khi $AB=6$ cm, $\\widehat{ABC}=53^\\circ$. Giải tam giác vuông $ABC$ "
             "(làm tròn kết quả độ dài đến chữ số thập phân thứ hai; số đo góc làm tròn đến độ)." + BR +
             "b) \\textbf{(0,75 điểm)} Kẻ đường cao $AH$ ($H\\in BC$) của tam giác $ABC$. Chứng minh: "
             "$BC=AB\\cdot\\cos\\widehat{ABC}+AC\\cdot\\cos\\widehat{ACB}$." + BR +
             "c) \\textbf{(0,5 điểm)} Kẻ phân giác $BD$ của $\\widehat{ABC}$ ($D\\in AC$). Gọi $K$ là giao điểm của $BD$ và $AH$. "
             "Chứng minh: $KH=AK\\cdot\\sin\\widehat{ACB}$." + BR +
             "d) \\textbf{(0,5 điểm)} Gọi $M$ là hình chiếu của $C$ trên đường thẳng $BD$. Qua $M$ kẻ đường thẳng vuông góc với $AC$, "
             "đường thẳng này cắt $BC$ tại $I$. Chứng minh: $I$ là trung điểm của $BC$.",
             hinh_da=HINH_ON2,
             dap_an=[
                 y("a)", 0.75, [("Xét $\\triangle ABC$ vuông tại $A$: $AC=AB\\cdot\\tan B=6\\cdot\\tan 53^\\circ\\approx 7{,}96$ (cm).", 0.25),
                                ("$BC=\\dfrac{AB}{\\cos B}=\\dfrac{6}{\\cos 53^\\circ}\\approx 9{,}97$ (cm).", 0.25),
                                ("$\\widehat{ACB}=90^\\circ-53^\\circ=37^\\circ$.", 0.25)]),
                 y("b)", 0.75, [("$\\widehat{B}$, $\\widehat{C}$ nhọn $\\Rightarrow H$ nằm giữa $B$ và $C$ $\\Rightarrow BC=BH+CH$."),
                                ("Xét $\\triangle ABH$ vuông tại $H$: $BH=AB\\cdot\\cos\\widehat{ABC}$.", 0.25),
                                ("Xét $\\triangle ACH$ vuông tại $H$: $CH=AC\\cdot\\cos\\widehat{ACB}$.", 0.25),
                                ("Vậy $BC=AB\\cdot\\cos\\widehat{ABC}+AC\\cdot\\cos\\widehat{ACB}$.", 0.25)]),
                 y("c)", 0.5, [("$BK$ là phân giác của $\\widehat{ABH}$ trong $\\triangle ABH$ $\\Rightarrow\\dfrac{KH}{AK}=\\dfrac{BH}{AB}$ (tính chất đường phân giác)."),
                               ("Xét $\\triangle ABH$ vuông tại $H$: $\\dfrac{BH}{AB}=\\cos\\widehat{ABC}$.", 0.25),
                               ("$\\widehat{ABC}+\\widehat{ACB}=90^\\circ\\Rightarrow\\cos\\widehat{ABC}=\\sin\\widehat{ACB}$"),
                               ("$\\Rightarrow\\dfrac{KH}{AK}=\\sin\\widehat{ACB}\\Rightarrow KH=AK\\cdot\\sin\\widehat{ACB}$.", 0.25)]),
                 y("d)", 0.5, [("$MI\\perp AC$, $AB\\perp AC$ $\\Rightarrow MI\\,/\\!/\\,AB\\Rightarrow\\widehat{IMB}=\\widehat{MBA}$ (so le trong)."),
                               ("Mà $\\widehat{MBA}=\\widehat{MBI}$ ($BD$ là phân giác) $\\Rightarrow\\widehat{IMB}=\\widehat{IBM}\\Rightarrow\\triangle IBM$ cân tại $I\\Rightarrow IB=IM$.", 0.25),
                               ("$\\triangle BMC$ vuông tại $M$: $\\widehat{IMC}=90^\\circ-\\widehat{IMB}=90^\\circ-\\widehat{IBM}=\\widehat{ICM}$"),
                               ("$\\Rightarrow\\triangle IMC$ cân tại $I\\Rightarrow IM=IC$. Vậy $IB=IC$, tức $I$ là trung điểm của $BC$.", 0.25)]),
             ],
             mt=[("IVa", "Giải tam giác vuông biết một cạnh và một góc", "HH IV", "TH", 0.75, 6, "THCS Bát Tràng"),
                 ("IVb", "Chứng minh hệ thức cạnh -- góc ($\\cos$)", "HH IV", "VD", 0.75, 6, "THCS Bát Tràng"),
                 ("IVc", "Tính chất đường phân giác + góc phụ nhau", "HH IV", "VD", 0.5, 6, "THCS Bát Tràng"),
                 ("IVd", "Chứng minh trung điểm qua hai tam giác cân", "HH IV", "VDC", 0.5, 7, "THCS Bát Tràng")],
             note="Ý c dùng lại tính chất đường phân giác (lớp 8). Nhắc HS: $\\sin$ góc này $=\\cos$ góc kia khi hai góc phụ nhau."),
        dict(label="Bài V.", level=4,
             statement="\\textbf{(0,5 điểm)} Một người nông dân muốn rào một khu đất hình chữ nhật có chu vi $60$ m để xây dựng một "
             "vườn hoa. Với chiều rộng của khu đất là $x$ (m), tìm $x$ để diện tích vườn hoa xây được lớn nhất.",
             dap_an=[y("", 0.5, [("Nửa chu vi là $30$ m $\\Rightarrow$ chiều dài khu đất là $30-x$ (m), điều kiện $0<x<30$."),
                                 ("Diện tích: $S=x(30-x)=-x^2+30x=225-(x-15)^2\\le 225$.", 0.25),
                                 ("Dấu ``$=$'' xảy ra khi $x=15$ (TMĐK)."),
                                 ("Vậy $x=15$ m thì diện tích vườn hoa lớn nhất là $225\\ \\text{m}^2$.", 0.25)])],
             mt=[("V", "Bài toán tối ưu: diện tích lớn nhất khi chu vi cố định", "ĐS II", "VDC", 0.5, 6, "THCS Ngô Gia Tự")],
             note="Cùng khuôn ``đưa về $m-(x-a)^2$'' như Đề ôn 1 nhưng bối cảnh hình học."),
    ])

DE["on-3"] = dict(
    ten="ĐỀ ÔN TẬP SỐ 3", cach_dung="Đề mở rộng sang dạng tần suất thứ nhì -- điểm thường thấp hơn Đề ôn 1, 2 là bình thường. Mục tiêu là HS không bị bất ngờ trước dạng lạ, chưa phải điểm cao.", slug_de="de-on-tap-giua-ki-1-so-3-v2", slug_mt="ma-tran-va-dap-an-on-tap-so-3-v2",
    eyebrow="LỚP 9 • ĐỀ ÔN TẬP SỐ 3",
    gioi_thieu=("\\textbf{ĐỀ ÔN TẬP SỐ 3 -- GIỮA HỌC KÌ I TOÁN 9} (90 phút -- Thang điểm 10 -- 5 bài tự luận)." + BR +
                "\\textbf{Cách chọn câu:} các dạng xuất hiện \\textbf{ít hơn nhưng vẫn có trong đề trường} (tần suất thứ nhì): "
                "PT đưa về tích bằng hằng đẳng thức, hệ đặt ẩn phụ, so sánh từ bất đẳng thức, lập hệ chuyển động, lập PT năng suất, "
                "tỉ số lượng giác góc rất nhỏ hai bước, bốn điểm cùng thuộc đường tròn, tối ưu hai ràng buộc. "
                "Câu \\textbf{I.3 được mở rộng} thêm ý tìm nghiệm nguyên so với đề gốc."),
    bai=[
        dict(label="Bài I.", level=2,
             statement="\\textbf{(3,0 điểm)}" + BR +
             "1) \\textbf{(0,75 điểm)} Giải phương trình: $x^2-1=5(x+1)$." + BR +
             "2) \\textbf{(0,75 điểm)} Giải hệ phương trình: $\\begin{cases}\\dfrac{3}{x+1}-\\dfrac{2y}{y-2}=-1\\\\[6pt] \\dfrac{2}{x+1}+\\dfrac{y}{y-2}=4\\end{cases}$" + BR +
             "3) \\textbf{(1,0 điểm)} Giải bất phương trình $\\dfrac{3x+5}{2}-1\\le\\dfrac{x+2}{3}+x$, "
             "rồi tìm nghiệm nguyên lớn nhất của bất phương trình đó." + BR +
             "4) \\textbf{(0,5 điểm)} Cho $a<b$, hãy so sánh: $-4a+3$ và $-4b+3$.",
             dap_an=[
                 y("1)", 0.75, [("$x^2-1=5(x+1)\\Leftrightarrow (x-1)(x+1)-5(x+1)=0$", 0.25),
                                ("$\\Leftrightarrow (x+1)(x-6)=0\\Leftrightarrow x=-1$ hoặc $x=6$.", 0.25),
                                ("Vậy phương trình có hai nghiệm $x=-1$; $x=6$.", 0.25)]),
                 y("2)", 0.75, [("ĐKXĐ: $x\\ne -1$; $y\\ne 2$. Đặt $u=\\dfrac{1}{x+1}$, $v=\\dfrac{y}{y-2}$, hệ trở thành $\\begin{cases}3u-2v=-1\\\\2u+v=4\\end{cases}$", 0.25),
                                ("Từ phương trình thứ hai: $v=4-2u$. Thế vào: $3u-8+4u=-1\\Leftrightarrow u=1\\Rightarrow v=2$.", 0.25),
                                ("$\\dfrac{1}{x+1}=1\\Rightarrow x=0$; $\\dfrac{y}{y-2}=2\\Rightarrow y=2y-4\\Rightarrow y=4$ (TMĐK)."),
                                ("Vậy hệ có nghiệm duy nhất $(x;y)=(0;4)$.", 0.25)]),
                 y("3)", 1.0, [("$\\dfrac{3x+5}{2}-1\\le\\dfrac{x+2}{3}+x\\Leftrightarrow 3(3x+5)-6\\le 2(x+2)+6x$", 0.25),
                               ("$\\Leftrightarrow 9x+9\\le 8x+4$", 0.25),
                               ("$\\Leftrightarrow x\\le -5$. Vậy nghiệm của bất phương trình là $x\\le -5$.", 0.25),
                               ("Nghiệm nguyên lớn nhất của bất phương trình là $x=-5$.", 0.25)]),
                 y("4)", 0.5, [("$a<b\\Rightarrow -4a>-4b$ (nhân hai vế với $-4<0$, đổi chiều).", 0.25),
                               ("$\\Rightarrow -4a+3>-4b+3$ (cộng $3$ vào hai vế). Vậy $-4a+3>-4b+3$.", 0.25)]),
             ],
             mt=[("I.1", "PT đưa về tích bằng hằng đẳng thức $x^2-1$", "ĐS II", "TH", 0.75, 5, "THCS Nguyễn Du"),
                 ("I.2", "Hệ PT đặt ẩn phụ", "ĐS I", "VD", 0.75, 8, "THCS Dịch Vọng Hậu"),
                 ("I.3", "BPT có mẫu + \\textit{(mở rộng)} nghiệm nguyên lớn nhất", "ĐS II", "TH", 1.0, 7, "THCS Giảng Võ (2024--2025)"),
                 ("I.4", "So sánh từ bất đẳng thức cho trước", "ĐS II", "NB", 0.5, 3, "THCS Nguyễn Bỉnh Khiêm")],
             note="Ý 1: lỗi kinh điển là chia hai vế cho $x+1$ làm mất nghiệm $x=-1$. Ý 2: bắt buộc ghi ĐKXĐ trước khi đặt ẩn phụ."),
        dict(label="Bài II.", level=3,
             statement="\\textbf{(3,0 điểm)}" + BR +
             "1) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập hệ phương trình.}" + BR +
             "Một ô tô dự định đi từ A đến B trong khoảng thời gian nhất định. Nếu ô tô chạy nhanh $10$ km mỗi giờ thì đến nơi "
             "sớm hơn dự định là $3$ giờ. Nếu ô tô chạy chậm lại $10$ km mỗi giờ thì đến nơi chậm hơn so với dự định là $5$ giờ. "
             "Tính độ dài quãng đường AB." + BR +
             "2) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập phương trình.}" + BR +
             "Một tổ dự định mỗi ngày may $50$ cái áo. Khi thực hiện, do cải tiến kĩ thuật, mỗi ngày tổ may được $55$ chiếc áo. "
             "Vì vậy tổ đã may xong trước thời hạn $2$ ngày và còn dư ra $15$ chiếc áo. Tính số áo mà tổ phải may theo dự định.",
             dap_an=[
                 y("1)", 1.5, [("Gọi vận tốc dự định là $x$ (km/h, $x>10$) và thời gian dự định là $y$ (giờ, $y>3$). Quãng đường AB là $xy$ (km).", 0.25),
                               ("Nhanh hơn $10$ km/h thì đến sớm $3$ giờ: $(x+10)(y-3)=xy\\Leftrightarrow -3x+10y=30$ \\quad (1)", 0.25),
                               ("Chậm hơn $10$ km/h thì đến muộn $5$ giờ: $(x-10)(y+5)=xy\\Leftrightarrow 5x-10y=50$ \\quad (2)", 0.25),
                               ("Cộng (1) và (2): $2x=80\\Leftrightarrow x=40$ (TMĐK) $\\Rightarrow 10y=30+3\\cdot 40=150\\Rightarrow y=15$ (TMĐK).", 0.5),
                               ("Vậy quãng đường AB dài $40\\cdot 15=600$ (km).", 0.25)]),
                 y("2)", 1.5, [("Gọi số áo tổ phải may theo dự định là $x$ (chiếc, $x\\in\\mathbb N^*$). Thực tế tổ may được $x+15$ (chiếc).", 0.25),
                               ("Thời gian dự định: $\\dfrac{x}{50}$ (ngày); thời gian thực tế: $\\dfrac{x+15}{55}$ (ngày).", 0.25),
                               ("Xong trước thời hạn $2$ ngày: $\\dfrac{x}{50}-\\dfrac{x+15}{55}=2$", 0.25),
                               ("$\\Leftrightarrow 11x-10(x+15)=1100\\Leftrightarrow x=1250$ (TMĐK).", 0.5),
                               ("Vậy theo dự định tổ phải may $1250$ chiếc áo.", 0.25)]),
             ],
             mt=[("II.1", "Lập hệ PT -- chuyển động (dự định/thực tế, biến đổi tích)", "ĐS I", "VD", 1.5, 14, "THCS Vạn Phúc (2024--2025)"),
                 ("II.2", "Lập PT -- năng suất, thời gian dự định/thực tế", "ĐS II", "VD", 1.5, 12, "THCS Ngô Gia Tự")],
             note="Cả hai ý đều có hai ẩn ``ẩn trong ẩn'' (vận tốc nhân thời gian, số áo chia năng suất) — bước nâng tư duy mô hình hoá so với Đề ôn 1, 2."),
        dict(label="Bài III.", level=3,
             statement="\\textbf{(1,0 điểm)} Một chiếc máy bay bắt đầu quy trình hạ cánh tại điểm $A$, khi đang ở độ cao $5$ km "
             "so với mặt đất, và hạ xuống điểm $B$ trên đường băng. Đường hạ cánh $AB$ của máy bay là đường thẳng tạo với mặt đất "
             "một góc $3^\\circ$ (hình vẽ minh hoạ không đúng tỉ lệ).",
             sau_hinh="1) \\textbf{(0,5 điểm)} Hãy tính độ dài quãng đường hạ cánh $AB$ của máy bay (làm tròn kết quả đến km)." + BR +
             "2) \\textbf{(0,5 điểm)} Sau khi tiếp đất tại điểm $B$, máy bay di chuyển thẳng đến khu vực trả khách với vận tốc "
             "trung bình $45$ km/h. Biết rằng tổng quãng đường từ điểm $A$ (bắt đầu hạ cánh) đến khu vực trả khách là $102$ km, "
             "hãy tính xem hành khách phải chờ bao nhiêu phút kể từ lúc máy bay bắt đầu tiếp đất cho đến khi về tới khu vực trả khách "
             "(làm tròn kết quả đến phút).",
             figure=dict(tikz=TIKZ_HACANH_TV, pos="below"),
             dap_an=[y("1)", 0.5, [("Xét $\\triangle AHB$ vuông tại $H$: $AB=\\dfrac{AH}{\\sin\\widehat{ABH}}=\\dfrac{5}{\\sin 3^\\circ}\\approx 95{,}5$ (km).", 0.25),
                                   ("Vậy quãng đường hạ cánh dài khoảng $96$ km.", 0.25)]),
                     y("2)", 0.5, [("Gọi $C$ là khu vực trả khách. Đổi $45$ km/h $=0{,}75$ km/phút."),
                                   ("$BC=102-AB=102-\\dfrac{5}{\\sin 3^\\circ}\\approx 6{,}46$ (km).", 0.25),
                                   ("Thời gian: $6{,}46:0{,}75\\approx 8{,}6\\approx 9$ (phút). Vậy hành khách phải chờ khoảng $9$ phút.", 0.25)])],
             mt=[("III.1", "Tỉ số lượng giác thực tế -- góc rất nhỏ (dùng $\\sin$)", "HH IV", "TH", 0.5, 4, "THCS Trưng Vương"),
                 ("III.2", "Ghép quãng đường -- thời gian, KHÔNG làm tròn giữa chừng", "HH IV", "VD", 0.5, 6, "THCS Trưng Vương")],
             note="Ý 2 là điểm phân loại: HS dùng $AB=96$ (đã làm tròn) sẽ ra $8$ phút -- sai. Hướng dẫn chấm gốc dùng giá trị chưa làm tròn, ra $9$ phút."),
        dict(label="Bài IV.", level=3,
             statement="\\textbf{(2,5 điểm)} Cho tam giác $ABC$ vuông tại $A$ và đường cao $AH$." + BR +
             "a) \\textbf{(1,0 điểm)} Biết $\\widehat{B}=60^\\circ$, $AC=7$ cm. Tính độ dài cạnh $AB$, $BC$ và $AH$ (kết quả làm tròn đến hàng đơn vị)." + BR +
             "b) \\textbf{(1,0 điểm)} Gọi $M$ là trung điểm của $AC$, kẻ $AD\\perp BM$ ($D\\in BM$). Chứng minh bốn điểm $A$, $B$, $H$, $D$ "
             "cùng thuộc một đường tròn và $\\sin^2\\widehat{ABM}=\\dfrac{DM}{BM}$." + BR +
             "c) \\textbf{(0,5 điểm)} Gọi $N$ là hình chiếu của $M$ trên $BC$. Tia $AD$ cắt đường thẳng qua $C$ và vuông góc với $AC$ tại $E$. "
             "Chứng minh ba điểm $M$, $N$, $E$ thẳng hàng.",
             hinh_da=HINH_ON3,
             dap_an=[
                 y("a)", 1.0, [("Vẽ hình đúng (như hình vẽ).", 0.25),
                               ("Xét $\\triangle ABC$ vuông tại $A$: $AB=\\dfrac{AC}{\\tan B}=\\dfrac{7}{\\tan 60^\\circ}\\approx 4$ (cm).", 0.25),
                               ("$BC=\\dfrac{AC}{\\sin B}=\\dfrac{7}{\\sin 60^\\circ}\\approx 8$ (cm).", 0.25),
                               ("$\\widehat{C}=90^\\circ-60^\\circ=30^\\circ$. Xét $\\triangle AHC$ vuông tại $H$: $AH=AC\\cdot\\sin C=7\\cdot\\sin 30^\\circ=3{,}5\\approx 4$ (cm).", 0.25)]),
                 y("b)", 1.0, [("$\\widehat{AHB}=90^\\circ\\Rightarrow H$ thuộc đường tròn đường kính $AB$; $\\widehat{ADB}=90^\\circ\\Rightarrow D$ thuộc đường tròn đường kính $AB$.", 0.25),
                               ("Vậy bốn điểm $A$, $B$, $H$, $D$ cùng thuộc đường tròn đường kính $AB$.", 0.25),
                               ("Xét $\\triangle MDA$ và $\\triangle MAB$: $\\widehat{MDA}=\\widehat{MAB}=90^\\circ$, $\\widehat{AMB}$ chung"),
                               ("$\\Rightarrow\\triangle MDA\\backsim\\triangle MAB$ (g.g) $\\Rightarrow\\dfrac{MD}{MA}=\\dfrac{MA}{MB}\\Rightarrow MA^2=MD\\cdot MB$.", 0.25),
                               ("Xét $\\triangle ABM$ vuông tại $A$: $\\sin\\widehat{ABM}=\\dfrac{AM}{BM}\\Rightarrow\\sin^2\\widehat{ABM}=\\dfrac{AM^2}{BM^2}=\\dfrac{MD\\cdot MB}{BM^2}=\\dfrac{DM}{BM}$.", 0.25)]),
                 y("c)", 0.5, [("Gọi $E'$ là giao điểm của đường thẳng $MN$ với đường thẳng qua $C$ vuông góc với $AC$."),
                               ("Xét $\\triangle MNC$ và $\\triangle MCE'$: $\\widehat{MNC}=\\widehat{MCE'}=90^\\circ$, $\\widehat{CME'}$ chung"),
                               ("$\\Rightarrow\\triangle MNC\\backsim\\triangle MCE'$ (g.g) $\\Rightarrow\\dfrac{MN}{MC}=\\dfrac{MC}{ME'}\\Rightarrow MC^2=MN\\cdot ME'$."),
                               ("$MA=MC$, kết hợp b) $\\Rightarrow MD\\cdot MB=MN\\cdot ME'\\Rightarrow\\dfrac{MD}{MN}=\\dfrac{ME'}{MB}$.", 0.25),
                               ("Xét $\\triangle MDE'$ và $\\triangle MNB$: $\\dfrac{MD}{MN}=\\dfrac{ME'}{MB}$, $\\widehat{BMN}$ chung"),
                               ("$\\Rightarrow\\triangle MDE'\\backsim\\triangle MNB$ (c.g.c) $\\Rightarrow\\widehat{MDE'}=\\widehat{MNB}=90^\\circ\\Rightarrow DE'\\perp BM$."),
                               ("Mà $AD\\perp BM$ $\\Rightarrow A$, $D$, $E'$ thẳng hàng $\\Rightarrow E'\\equiv E$. Vậy ba điểm $M$, $N$, $E$ thẳng hàng.", 0.25)]),
             ],
             mt=[("IV.a", "Giải tam giác vuông biết một cạnh và một góc", "HH IV", "TH", 1.0, 7, "THCS Đền Lừ"),
                 ("IV.b", "Bốn điểm cùng thuộc đường tròn (góc vuông); hệ thức $\\sin^2$ qua đồng dạng", "HH V", "VD", 1.0, 8, "THCS Đền Lừ"),
                 ("IV.c", "Chứng minh thẳng hàng qua đồng dạng c.g.c", "HH IV", "VDC", 0.5, 9, "THCS Đền Lừ")],
             note="Ý a: $AH=3{,}5$ cm đúng tuyệt đối, làm tròn theo yêu cầu đề thành $4$ cm; HS ghi $3{,}5$ cm vẫn cho đủ điểm. Dạng ``bốn điểm cùng thuộc một đường tròn'' có ở khoảng 1/4 đề GK1 2025--2026 (trường dạy sớm phần đầu chương V). Ý c: dựng điểm phụ $E'$ rồi chứng minh $E'\\equiv E$."),
        dict(label="Bài V.", level=4,
             statement="\\textbf{(0,5 điểm)} Một hộ nông dân dự định trồng hai loại hoa màu là đậu và cà trên diện tích $800\\ \\text{m}^2$. "
             "Biết rằng cứ $100\\ \\text{m}^2$ trồng đậu cần $10$ công và lãi $7$ triệu đồng, còn $100\\ \\text{m}^2$ trồng cà cần "
             "$15$ công và lãi $9$ triệu đồng. Hỏi cần trồng mỗi loại cây trên diện tích bao nhiêu để thu được tiền lãi cao nhất, "
             "biết rằng tổng số công không vượt quá $90$? \\textit{(một công được hiểu là tiền lương trung bình chi trả cho một người "
             "lao động làm việc trong một ngày)}",
             dap_an=[y("", 0.5, [("Gọi diện tích trồng đậu, cà lần lượt là $x$, $y$ (đơn vị $100\\ \\text{m}^2$; $x,y\\ge 0$)."),
                                 ("Ràng buộc: $x+y\\le 8$; $10x+15y\\le 90\\Leftrightarrow 2x+3y\\le 18$. Tiền lãi: $T=7x+9y$ (triệu đồng)."),
                                 ("$T=3(x+y)+2(2x+3y)\\le 3\\cdot 8+2\\cdot 18=60$.", 0.25),
                                 ("Dấu ``$=$'' xảy ra khi $x+y=8$ và $2x+3y=18\\Leftrightarrow x=6$, $y=2$."),
                                 ("Vậy trồng đậu trên $600\\ \\text{m}^2$, trồng cà trên $200\\ \\text{m}^2$ thì lãi cao nhất là $60$ triệu đồng.", 0.25)])],
             mt=[("V", "Tối ưu tuyến tính hai ràng buộc (tách $T$ theo hai ràng buộc)", "ĐS II", "VDC", 0.5, 9, "THCS Trưng Vương")],
             note="Kĩ thuật then chốt: viết $7x+9y=3(x+y)+2(2x+3y)$ để dùng cả hai ràng buộc -- khác khuôn ``$m-(x-a)^2$'' của Đề ôn 1, 2."),
    ])

DE["gk1"] = dict(
    ten="ĐỀ KIỂM TRA GIỮA HỌC KÌ I", cach_dung="Đề chốt: làm như thi thật, chấm theo đúng biểu điểm. Không chữa trước khi chấm xong cả lớp. Dùng phiếu theo dõi tiến bộ ở cuối file này để trả kết quả cho HS theo từng bài.", slug_de="de-kiem-tra-giua-ki-1-chinh-thuc-v2", slug_mt="ma-tran-va-dap-an-giua-ki-1-chinh-thuc-v2",
    eyebrow="LỚP 9 • ĐỀ CHÍNH THỨC",
    gioi_thieu=("\\textbf{ĐỀ KIỂM TRA GIỮA HỌC KÌ I -- TOÁN 9 (ĐỀ CHỐT)} (90 phút -- Thang điểm 10 -- 5 bài tự luận)." + BR +
                "\\textbf{Mục đích:} đánh giá vì sự tiến bộ -- đo xem HS đã \\textbf{thành thạo} các dạng đã ôn ở 3 đề chưa. "
                "Khung đề, phân bố điểm và độ khó \\textbf{bám đúng đề GK1 của các trường Hà Nội} (I: 3,0 -- II: 3,0 -- III: 1,0 -- IV: 2,5 -- V: 0,5). "
                "Câu hỏi lấy từ đề thật của trường \\textbf{chưa dùng trong 3 đề ôn} (cùng dạng, khác số liệu và bối cảnh) để đo đúng năng lực, "
                "không đo trí nhớ."),
    bai=[
        dict(label="Bài I.", level=2,
             statement="\\textbf{(3,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:" + BR +
             "a) \\textbf{(0,75 điểm)} $(x+3)(2x-5)=0$" + BR +
             "b) \\textbf{(0,75 điểm)} $\\dfrac{1}{x(x-2)}+\\dfrac{2}{4-x^2}=\\dfrac{x-4}{x(x+2)}$" + BR +
             "c) \\textbf{(0,75 điểm)} $\\dfrac{3x-1}{3}-\\dfrac{x}{6}>\\dfrac{x+1}{2}$" + BR +
             "d) \\textbf{(0,75 điểm)} $\\begin{cases}x-2y=-5\\\\ 2x+3y=4\\end{cases}$",
             dap_an=[
                 y("a)", 0.75, [("$(x+3)(2x-5)=0\\Leftrightarrow x+3=0$ hoặc $2x-5=0$", 0.25),
                                ("$\\Leftrightarrow x=-3$ hoặc $x=\\dfrac52$.", 0.25),
                                ("Vậy phương trình có hai nghiệm $x=-3$; $x=\\dfrac52$.", 0.25)]),
                 y("b)", 0.75, [("ĐKXĐ: $x\\ne 0$; $x\\ne 2$; $x\\ne -2$. Ta có $\\dfrac{2}{4-x^2}=\\dfrac{-2}{(x-2)(x+2)}$.", 0.25),
                                ("Mẫu chung $x(x-2)(x+2)$. Quy đồng, khử mẫu: $(x+2)-2x=(x-4)(x-2)$"),
                                ("$\\Leftrightarrow 2-x=x^2-6x+8\\Leftrightarrow x^2-5x+6=0\\Leftrightarrow (x-2)(x-3)=0$.", 0.25),
                                ("$x=2$ (không TMĐK) hoặc $x=3$ (TMĐK). Vậy phương trình có nghiệm $x=3$.", 0.25)]),
                 y("c)", 0.75, [("$\\dfrac{3x-1}{3}-\\dfrac{x}{6}>\\dfrac{x+1}{2}\\Leftrightarrow 2(3x-1)-x>3(x+1)$", 0.25),
                                ("$\\Leftrightarrow 6x-2-x>3x+3\\Leftrightarrow 2x>5$", 0.25),
                                ("$\\Leftrightarrow x>\\dfrac52$. Vậy nghiệm của bất phương trình là $x>\\dfrac52$.", 0.25)]),
                 y("d)", 0.75, [("Từ phương trình thứ nhất: $x=2y-5$.", 0.25),
                                ("Thế vào phương trình thứ hai: $2(2y-5)+3y=4\\Leftrightarrow 7y=14\\Leftrightarrow y=2\\Rightarrow x=-1$.", 0.25),
                                ("Vậy hệ có nghiệm duy nhất $(x;y)=(-1;2)$.", 0.25)]),
             ],
             mt=[("Ia", "Giải phương trình tích", "ĐS II", "NB", 0.75, 4, "THCS Thanh Quan (2024--2025)"),
                 ("Ib", "PT chứa ẩn ở mẫu: mẫu đổi dấu $4-x^2$, có nghiệm bị loại", "ĐS II", "VD", 0.75, 9, "THCS Giảng Võ (2024--2025)"),
                 ("Ic", "BPT có mẫu số", "ĐS II", "TH", 0.75, 5, "THCS Thanh Quan (2024--2025)"),
                 ("Id", "Giải hệ hai PT bậc nhất hai ẩn", "ĐS I", "NB", 0.75, 5, "THCS Thái Thịnh")],
             note="Ý b gộp hai bẫy của Ôn 1 (nghiệm bị loại) và Ôn 2 (phân tích mẫu)."),
        dict(label="Bài II.", level=3,
             statement="\\textbf{(3,0 điểm)}" + BR +
             "1) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập hệ phương trình.}" + BR +
             "Nhân dịp khai trương, một cửa hàng điện tử giảm giá $15\\%$ cho mỗi chiếc tai nghe và $20\\%$ cho mỗi chiếc chuột máy tính. "
             "Chú Hà mua $3$ chiếc tai nghe và $2$ chiếc chuột máy tính, sau khi giảm giá chú phải trả $701\\,600$ đồng. "
             "Biết rằng tổng số tiền chú Hà phải trả nếu không được giảm giá là $832\\,000$ đồng. "
             "Tính giá niêm yết (giá ban đầu khi chưa giảm) của mỗi chiếc tai nghe và mỗi chiếc chuột máy tính." + BR +
             "2) \\textbf{(1,5 điểm)} \\textit{Giải bài toán bằng cách lập bất phương trình.}" + BR +
             "Bạn Lâm muốn mua một khối rubik lập phương $3\\times 3\\times 3$ trị giá $1\\,200\\,000$ đồng. Tính đến nay, Lâm đã tiết kiệm "
             "được $300\\,000$ đồng. Sau đó, mỗi tháng Lâm tiết kiệm tiền tiêu vặt được $130\\,000$ đồng. "
             "Hỏi sau ít nhất bao nhiêu tháng bạn Lâm có thể mua được khối rubik đó?",
             dap_an=[
                 y("1)", 1.5, [("Gọi giá niêm yết mỗi chiếc tai nghe, mỗi chiếc chuột lần lượt là $x$, $y$ (đồng; $x,y>0$).", 0.25),
                               ("Không giảm giá: $3x+2y=832\\,000$ \\quad (1)", 0.25),
                               ("Sau giảm giá, mỗi tai nghe còn $0{,}85x$, mỗi chuột còn $0{,}8y$:"),
                               ("$3\\cdot 0{,}85x+2\\cdot 0{,}8y=701\\,600\\Leftrightarrow 2{,}55x+1{,}6y=701\\,600$ \\quad (2)", 0.25),
                               ("Từ (1): $1{,}6y=0{,}8\\,(832\\,000-3x)=665\\,600-2{,}4x$. Thay vào (2): $0{,}15x=36\\,000$"),
                               ("$\\Leftrightarrow x=240\\,000$ (TMĐK) $\\Rightarrow y=\\dfrac{832\\,000-720\\,000}{2}=56\\,000$ (TMĐK).", 0.5),
                               ("Vậy giá niêm yết mỗi chiếc tai nghe là $240\\,000$ đồng, mỗi chiếc chuột là $56\\,000$ đồng.", 0.25)]),
                 y("2)", 1.5, [("Gọi số tháng để bạn Lâm mua được khối rubik là $x$ (tháng, $x\\in\\mathbb N^*$).", 0.25),
                               ("Số tiền tiết kiệm thêm sau $x$ tháng: $130\\,000x$ (đồng).", 0.25),
                               ("Theo bài: $300\\,000+130\\,000x\\ge 1\\,200\\,000$", 0.25),
                               ("$\\Leftrightarrow 130\\,000x\\ge 900\\,000\\Leftrightarrow x\\ge\\dfrac{90}{13}\\approx 6{,}9$.", 0.25),
                               ("$x$ là số tự nhiên nhỏ nhất thoả mãn $\\Rightarrow x=7$.", 0.25),
                               ("Vậy sau ít nhất $7$ tháng bạn Lâm mua được khối rubik.", 0.25)]),
             ],
             mt=[("II.1", "Lập hệ PT -- khuyến mại $\\%$ với số lượng nhiều chiếc", "ĐS I", "VD", 1.5, 13, "THCS Thanh Quan (2024--2025)"),
                 ("II.2", "Lập BPT thực tế -- tiết kiệm ``ít nhất bao nhiêu tháng''", "ĐS II", "TH", 1.5, 8, "THCS Giảng Võ (2024--2025)")],
             note="Ý 1 nâng so với Ôn 1: giá còn lại phải nhân thêm số lượng ($3\\cdot 0{,}85x$). Ý 2: làm tròn LÊN như Ôn 1."),
        dict(label="Bài III.", level=2,
             statement="\\textbf{(1,0 điểm)} Lotte Center là toà cao ốc cao thứ hai tại Hà Nội. Toà nhà có $65$ tầng, được lấy cảm hứng "
             "từ tà áo dài truyền thống của người Việt Nam. Tại một thời điểm trong ngày, tia nắng mặt trời tạo với mặt đất một góc "
             "xấp xỉ $80^\\circ$ và bóng của toà nhà đó trên mặt đất dài $48$ m. Hỏi toà nhà cao bao nhiêu mét? (Kết quả làm tròn đến mét).",
             figure=dict(tikz=TIKZ_LOTTE, pos="right"),
             dap_an=[y("", 1.0, [("Từ hình vẽ: $AC$ là chiều cao toà nhà, $AB=48$ m là bóng toà nhà, $\\widehat{ABC}=80^\\circ$ là góc tạo bởi tia nắng với mặt đất.", 0.25),
                                 ("Xét $\\triangle ABC$ vuông tại $A$: $AC=AB\\cdot\\tan\\widehat{ABC}=48\\cdot\\tan 80^\\circ\\approx 272$ (m).", 0.5),
                                 ("Vậy toà nhà Lotte cao khoảng $272$ m.", 0.25)])],
             mt=[("III", "Ứng dụng tỉ số lượng giác: tính chiều cao (dùng $\\tan$)", "HH IV", "TH", 1.0, 5, "THCS Giảng Võ (2024--2025)")],
             note="Đo lại đúng dạng Ôn 1 -- Bài III. HS lấy trọn 1,0đ là đã thành thạo dạng này."),
        dict(label="Bài IV.", level=3,
             statement="\\textbf{(2,5 điểm)} Cho tam giác $MNP$ vuông tại $M$, đường cao $MH$. Gọi $E$, $F$ theo thứ tự là hình chiếu "
             "của $H$ trên $MN$ và $MP$." + BR +
             "a) \\textbf{(1,0 điểm)} Tính độ dài $NP$, $MH$ và số đo $\\widehat{MNP}$ (làm tròn đến độ) biết $MN=6$ cm, $MP=8$ cm." + BR +
             "b) \\textbf{(1,0 điểm)} Chứng minh $ME\\cdot MN=MF\\cdot MP$ và $\\widehat{MEF}=\\widehat{MPN}$." + BR +
             "c) \\textbf{(0,5 điểm)} Lấy điểm $Q$ nằm giữa $M$ và $P$, kẻ $MI$ vuông góc với $NQ$ tại $I$. "
             "Chứng minh $\\sin\\widehat{MQN}\\cdot\\cos\\widehat{MNP}=\\dfrac{HI}{QP}$.",
             hinh_da=HINH_GK,
             dap_an=[
                 y("a)", 1.0, [("Vẽ hình đúng (như hình vẽ).", 0.25),
                               ("$\\triangle MNP$ vuông tại $M$: $NP=\\sqrt{MN^2+MP^2}=\\sqrt{36+64}=10$ (cm).", 0.25),
                               ("Xét $\\triangle MHN$ và $\\triangle PMN$: $\\widehat{MHN}=\\widehat{PMN}=90^\\circ$, $\\widehat{MNP}$ chung"),
                               ("$\\Rightarrow\\triangle MHN\\backsim\\triangle PMN$ (g.g) $\\Rightarrow\\dfrac{MH}{PM}=\\dfrac{MN}{PN}$"),
                               ("$\\Rightarrow MH=\\dfrac{MN\\cdot MP}{NP}=\\dfrac{6\\cdot 8}{10}=4{,}8$ (cm).", 0.25),
                               ("$\\sin\\widehat{MNP}=\\dfrac{MP}{NP}=0{,}8\\Rightarrow\\widehat{MNP}\\approx 53^\\circ$.", 0.25),
                               ("Vậy $NP=10$ cm, $MH=4{,}8$ cm, $\\widehat{MNP}\\approx 53^\\circ$.")]),
                 y("b)", 1.0, [("Xét $\\triangle MEH$ và $\\triangle MHN$: $\\widehat{MEH}=\\widehat{MHN}=90^\\circ$, $\\widehat{HMN}$ chung"),
                               ("$\\Rightarrow\\triangle MEH\\backsim\\triangle MHN$ (g.g) $\\Rightarrow\\dfrac{ME}{MH}=\\dfrac{MH}{MN}\\Rightarrow ME\\cdot MN=MH^2$. \\quad (1)", 0.25),
                               ("Xét $\\triangle MFH$ và $\\triangle MHP$: $\\widehat{MFH}=\\widehat{MHP}=90^\\circ$, $\\widehat{HMP}$ chung"),
                               ("$\\Rightarrow\\triangle MFH\\backsim\\triangle MHP$ (g.g) $\\Rightarrow\\dfrac{MF}{MH}=\\dfrac{MH}{MP}\\Rightarrow MF\\cdot MP=MH^2$. \\quad (2)", 0.25),
                               ("Từ (1), (2) $\\Rightarrow ME\\cdot MN=MF\\cdot MP$."),
                               ("$\\Rightarrow\\dfrac{ME}{MP}=\\dfrac{MF}{MN}$; xét $\\triangle MEF$ và $\\triangle MPN$ có $\\widehat{NMP}$ chung"),
                               ("$\\Rightarrow\\triangle MEF\\backsim\\triangle MPN$ (c.g.c) $\\Rightarrow\\widehat{MEF}=\\widehat{MPN}$.", 0.5)]),
                 y("c)", 0.5, [("Xét $\\triangle NIM$ và $\\triangle NMQ$: $\\widehat{NIM}=\\widehat{NMQ}=90^\\circ$, $\\widehat{MNQ}$ chung $\\Rightarrow\\triangle NIM\\backsim\\triangle NMQ$ (g.g)"),
                               ("$\\Rightarrow\\dfrac{NI}{NM}=\\dfrac{NM}{NQ}\\Rightarrow NI\\cdot NQ=MN^2$."),
                               ("Tương tự, $\\triangle NHM\\backsim\\triangle NMP$ (g.g, $\\widehat{NHM}=\\widehat{NMP}=90^\\circ$, $\\widehat{MNP}$ chung) $\\Rightarrow NH\\cdot NP=MN^2$."),
                               ("$\\Rightarrow NI\\cdot NQ=NH\\cdot NP\\Rightarrow\\dfrac{NI}{NP}=\\dfrac{NH}{NQ}$; $\\widehat{N}$ chung $\\Rightarrow\\triangle NIH\\backsim\\triangle NPQ$ (c.g.c)"),
                               ("$\\Rightarrow\\dfrac{HI}{QP}=\\dfrac{NH}{NQ}$. \\quad (1)", 0.25),
                               ("$\\sin\\widehat{MQN}=\\dfrac{MN}{NQ}$; $\\cos\\widehat{MNP}=\\dfrac{MN}{NP}$ $\\Rightarrow\\sin\\widehat{MQN}\\cdot\\cos\\widehat{MNP}=\\dfrac{MN^2}{NQ\\cdot NP}=\\dfrac{NH\\cdot NP}{NQ\\cdot NP}=\\dfrac{NH}{NQ}$. \\quad (2)"),
                               ("Từ (1), (2): $\\sin\\widehat{MQN}\\cdot\\cos\\widehat{MNP}=\\dfrac{HI}{QP}$.", 0.25)]),
             ],
             mt=[("IVa", "Tính cạnh, đường cao, góc trong tam giác vuông", "HH IV", "TH", 1.0, 8, "THCS Cổ Nhuế 2"),
                 ("IVb", "Hai cặp đồng dạng g.g $\\Rightarrow$ đồng dạng c.g.c $\\Rightarrow$ góc bằng nhau", "HH IV", "VD", 1.0, 9, "THCS Cổ Nhuế 2"),
                 ("IVc", "Biến đổi tích tỉ số lượng giác qua đồng dạng c.g.c", "HH IV", "VDC", 0.5, 9, "THCS Cổ Nhuế 2")],
             note="Ý b dùng đúng kĩ thuật Ôn 3 -- IV.2 (hai cặp đồng dạng g.g cho $=MH^2$ $\\Rightarrow$ đồng dạng c.g.c). HS không được dùng hệ thức lượng trực tiếp -- phải chứng minh đồng dạng. Ý c ghép kĩ thuật Ôn 1 -- IVc (tỉ số $\\Rightarrow$ đồng dạng) với biến đổi $\\sin$, $\\cos$ như Ôn 2."),
        dict(label="Bài V.", level=4,
             statement="\\textbf{(0,5 điểm)} Một rạp chiếu phim có $120$ ghế, giá vé hiện tại là $100$ nghìn đồng mỗi vé. Với giá vé này, "
             "tất cả các ghế đều được bán hết cho mỗi suất chiếu. Ban quản lý rạp phim đang xem xét việc tăng giá vé để tối ưu hoá "
             "doanh thu. Sau khi thử nghiệm, rạp phim nhận thấy cứ mỗi lần tăng giá thêm $5$ nghìn đồng, số ghế bị bỏ trống sẽ tăng "
             "thêm $4$ ghế. Hỏi mức giá vé mới là bao nhiêu để rạp phim đạt doanh thu lớn nhất?",
             dap_an=[y("", 0.5, [("Gọi số lần tăng giá là $x$ ($x\\in\\mathbb N$, $x\\le 30$). Giá vé: $100+5x$ (nghìn đồng); số ghế bán được: $120-4x$."),
                                 ("Doanh thu: $T=(100+5x)(120-4x)=-20x^2+200x+12\\,000$"),
                                 ("$T=12\\,500-20(x-5)^2\\le 12\\,500$.", 0.25),
                                 ("Dấu ``$=$'' xảy ra khi $x=5$ $\\Rightarrow$ giá vé mới $100+5\\cdot 5=125$ (nghìn đồng)."),
                                 ("Vậy giá vé mới là $125$ nghìn đồng thì doanh thu lớn nhất ($12\\,500$ nghìn đồng mỗi suất).", 0.25)])],
             mt=[("V", "Bài toán tối ưu thực tế: doanh thu (tăng giá -- bớt khách)", "ĐS II", "VDC", 0.5, 8, "THCS Thanh Quan (2024--2025)")],
             note="Cùng khuôn Ôn 1 -- Bài V, khác hệ số ($-20(x-5)^2$): đo việc HS tự đưa về hằng đẳng thức, không thuộc lòng đáp số."),
    ])

# ─────────────────────────── BẢN ĐỒ TIẾN BỘ ───────────────────────────
TIEN_BO = [
    ("PT tích", "Ia: tích hai nhân tử", "Ia: tương tự", "I.1: tự đặt nhân tử chung $x+1$", "Ia: tích hai nhân tử"),
    ("PT chứa ẩn ở mẫu", "Ib: nghiệm bị loại $\\Rightarrow$ vô nghiệm", "Ib: phân tích mẫu $x^2-3x$", "I.2: hệ có ẩn ở mẫu, đặt ẩn phụ", "Ib: mẫu đổi dấu $4-x^2$ + nghiệm bị loại"),
    ("Bất phương trình", "Ic: bỏ ngoặc, chuyển vế", "Ic: khai triển $\\Rightarrow$ vô nghiệm", "I.3: có mẫu + nghiệm nguyên", "Ic: có mẫu số"),
    ("Hệ PT", "Id: cộng đại số", "Id: phương pháp thế", "I.2: đặt ẩn phụ", "Id: phương pháp thế"),
    ("Lập hệ PT", "II.1: khuyến mại hai mức $\\%$; II.2: tổng số lượng -- tổng khối lượng", "II.1: năng suất tăng $\\%$", "II.1: chuyển động, biến đổi tích", "II.1: khuyến mại $\\%$ $\\times$ số lượng"),
    ("Lập BPT / lập PT", "(chưa ôn -- dạng có ở khoảng 1/2 đề trường)", "II.2: lập BPT ``nhiều nhất'' -- làm tròn xuống", "II.2: lập PT năng suất", "II.2: lập BPT ``ít nhất'' -- làm tròn lên"),
    ("Tỉ số lượng giác thực tế", "III: $\\tan$, một bước", "III: $\\sin$ + thời gian (đổi km/h ra m/s)", "III: góc $3^\\circ$, không làm tròn giữa chừng", "III: $\\tan$, một bước"),
    ("Hình tam giác vuông", "IV: giải tam giác từ $\\tan$; $\\sin^2$; trung điểm $\\Rightarrow$ thẳng hàng", "IV: $\\cos$, phân giác, trung điểm", "IV: 4 điểm đường tròn; $\\sin^2$; thẳng hàng qua c.g.c", "IV: đồng dạng g.g $\\Rightarrow$ c.g.c; $\\sin\\cdot\\cos$"),
    ("Câu tối ưu cuối đề", "V: lợi nhuận $2250-10(x-5)^2$", "V: diện tích $225-(x-15)^2$", "V: hai ràng buộc tuyến tính", "V: doanh thu $12\\,500-20(x-5)^2$"),
]

# ─────────────────────────── NGUỒN: RẢI TRƯỜNG / QUẬN ───────────────────────────
# Quận/huyện CŨ (trước 7/2025) đọc từ header đề — khớp inputs/refs/de-thi/lop-9/luoi-dang/gk1.json.
# Luật (03/10/2026, sau góp ý "đề toàn khu vực LB - Gia Lâm"): mỗi đề >= 4 quận và không quận nào quá 40% điểm đề;
# cả bộ 4 đề không quận nào quá 25% và không trường nào quá 15% tổng điểm.
QUAN = {
    "THCS Đền Lừ": "Hoàng Mai", "THCS Ngô Gia Tự": "Long Biên", "THCS Đại Áng": "Thanh Trì", "THCS Chúc Sơn": "Chương Mỹ",
    "THCS Bát Tràng": "Gia Lâm", "THCS Giảng Võ": "Ba Đình", "THCS Chuyên Mỹ": "Phú Xuyên", "THCS Văn Yên": "Hà Đông",
    "THCS Xuân Phương (2024--2025)": "Nam Từ Liêm", "THCS Cổ Nhuế 2": "Bắc Từ Liêm", "THCS Trưng Vương": "Hoàn Kiếm",
    "THCS Tam Hiệp": "Thanh Trì", "THCS Nguyễn Du": "Hoàn Kiếm", "THCS Dịch Vọng Hậu": "Cầu Giấy",
    "THCS Giảng Võ (2024--2025)": "Ba Đình", "THCS Nguyễn Bỉnh Khiêm": "Long Biên", "THCS Ái Mộ": "Long Biên",
    "THCS Nhật Tân": "Tây Hồ", "THCS Vạn Phúc (2024--2025)": "Hà Đông", "THCS Thanh Quan (2024--2025)": "Hoàn Kiếm", "THCS Thái Thịnh": "Đống Đa",
}


def kiem_nguon():
    from collections import defaultdict
    tq, tt, bao_cao = defaultdict(float), defaultdict(float), {}
    for k, D in DE.items():
        q = defaultdict(float)
        for b in D["bai"]:
            for r in b["mt"]:
                q[QUAN[r[6]]] += r[4]; tq[QUAN[r[6]]] += r[4]; tt[r[6]] += r[4]
        assert len(q) >= 4, (k, dict(q))
        assert max(q.values()) <= 4.0 + 1e-9, (k, dict(q))
        truong = {r[6] for b in D["bai"] for r in b["mt"]}
        bao_cao[k] = (len(truong), q)
    assert max(tq.values()) <= 10.0 + 1e-9, dict(tq)
    assert max(tt.values()) <= 6.0 + 1e-9, dict(tt)
    return bao_cao, tq


NGUON, NGUON_BO = kiem_nguon()
for _k, (_n, _q) in NGUON.items():
    print(_k, _n, "trường,", len(_q), "quận:", ", ".join(f"{a} {d(v)}" for a, v in sorted(_q.items(), key=lambda t: -t[1])))

# ─────────────────────────── DỰNG JSON ───────────────────────────
KIND = ["review", "concept", "practice1", "practice2", "reflection"]


def bang_mt(rows):
    s = ("\\vspace{-6pt}\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n"
         "\\begin{tabular}{|c|p{5.4cm}|c|c|c|c|p{2.9cm}|}\n\\hline\n"
         "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Chương} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} & \\textbf{Nguồn đề} \\\\ \\hline\n")
    tong_d = tong_p = 0
    for c, nd, ch, m, di, ph, ng in rows:
        s += f"{c} & {nd} & {ch} & {m} & {d(di)} & {ph} & {ng} \\\\ \\hline\n"
        tong_d += di; tong_p += ph
    s += f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{TỔNG CỘNG}}}} & \\textbf{{{d(tong_d)}}} & \\textbf{{{tong_p}}} & \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tong_d, tong_p


def bang_muc(rows):
    muc = {"NB": 0, "TH": 0, "VD": 0, "VDC": 0}
    ds = {"Đại số (Chương I, II)": dict(muc), "Hình học (Chương IV, V)": dict(muc)}
    for c, nd, ch, m, di, ph, ng in rows:
        ds["Hình học (Chương IV, V)" if ch.startswith("HH") else "Đại số (Chương I, II)"][m] += di
    s = ("\\noindent\\textbf{TỔNG HỢP THEO MẠCH KIẾN THỨC VÀ CẤP ĐỘ (điểm)}\\par\\vspace{-6pt}\n"
         "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.05}\n\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
         "\\textbf{Mạch kiến thức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{VDC} & \\textbf{Tổng} \\\\ \\hline\n")
    tot = dict(muc)
    for k, v in ds.items():
        s += f"{k} & " + " & ".join(d(v[m]) if v[m] else "0" for m in muc) + f" & \\textbf{{{d(sum(v.values()))}}} \\\\ \\hline\n"
        for m in muc:
            tot[m] += v[m]
    s += "\\textbf{Tổng điểm} & " + " & ".join(f"\\textbf{{{d(tot[m]) if tot[m] else '0'}}}" for m in muc) + " & \\textbf{10,0} \\\\ \\hline\n"
    s += "\\textbf{Tỉ lệ} & " + " & ".join(f"{round(tot[m]*10)}\\%" for m in muc) + " & 100\\% \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s, tot


def bang_tien_bo(gk=False):
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.1}\n"
         "\\begin{tabular}{|p{2.4cm}|p{3.0cm}|p{3.0cm}|p{3.0cm}|p{3.0cm}|}\n\\hline\n"
         "\\textbf{Dạng} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{GK1 chính thức} \\\\ \\hline\n")
    for r in TIEN_BO:
        s += " & ".join(r) + " \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def bang_theo_doi():
    s = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.35}\n"
         "\\begin{tabular}{|l|c|c|c|c|c|}\n\\hline\n"
         "\\textbf{Bài (điểm tối đa)} & \\textbf{Đề ôn 1} & \\textbf{Đề ôn 2} & \\textbf{Đề ôn 3} & \\textbf{GK1} & \\textbf{Tiến bộ?} \\\\ \\hline\n")
    for b in ["Bài I -- phương trình, BPT, hệ (3,0)", "Bài II -- lập hệ / lập BPT (3,0)", "Bài III -- lượng giác thực tế (1,0)",
              "Bài IV -- hình học (2,5)", "Bài V -- câu tối ưu (0,5)", "\\textbf{Tổng (10,0)}"]:
        s += b + " & & & & & \\\\ \\hline\n"
    return s + "\\end{tabular}\\end{center}"


def de_json(k, D):
    stages = []
    for i, b in enumerate(D["bai"]):
        sol = BR.join(b["dap_an"])
        if b.get("hinh_da"):
            sol = ("\\begin{center}\\adjustbox{max width=0.62\\linewidth}{" + b["hinh_da"] + "}\\end{center}" + sol)
        blk = dict(type="problem", label=b["label"], level=b["level"], statement=b["statement"], tier="onclass",
                   solution=sol)
        if b.get("figure"):
            blk["figure"] = dict(tikz=b["figure"]["tikz"], pos=b["figure"]["pos"])
        blocks = [blk]
        if D.get("ngat_truoc_III") and i == 1:
            blocks.append(dict(type="para", text="\\newpage"))
        if b.get("sau_hinh"):
            blocks.append(dict(type="para", text=b["sau_hinh"]))
        if i == len(D["bai"]) - 1:
            blocks.append(dict(type="para", text="\\nopagebreak\\centerline{\\textit{$-$ HẾT $-$}}"))
        stages.append(dict(kind=KIND[i], number=i + 1, title="", blocks=blocks, teacher_note=b["note"]))
    tit = "Đề kiểm tra giữa học kì I (90 phút)" if k == "gk1" else f"Đề ôn tập giữa học kì I — Số {k[-1]} (90 phút)"
    return dict(slug=D["slug_de"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 9", class_tier="", theme="de_thi", trinh_bay="thoang",
                stages=stages)


def mt_json(k, D):
    rows = [r for b in D["bai"] for r in b["mt"]]
    t1, td, tp = bang_mt(rows)
    t2, tot = bang_muc(rows)
    assert abs(td - 10) < 1e-9, (k, td)
    n_tr, q = NGUON[k]
    nguon = (f"\\textbf{{Nguồn đề:}} câu lấy từ {n_tr} trường thuộc {len(q)} quận/huyện ("
             + "; ".join(f"{a} {d(v)}đ" for a, v in sorted(q.items(), key=lambda t: -t[1]))
             + "). Không quận nào quá $40\\%$ số điểm của đề; cả bộ 4 đề lấy từ "
             + f"{len(NGUON_BO)} quận/huyện, không quận nào quá $25\\%$.")
    st0 = [dict(type="para", text=D["gioi_thieu"] + BR + nguon), dict(type="para", text=t1), dict(type="para", text=t2),
           dict(type="para", text=f"\\noindent\\textit{{\\footnotesize Tổng thời gian làm bài ước tính: {tp} phút. "
                                  "Các con số NB/TH/VD/VDC chấm theo cách trường ghi trong ma trận đề gốc.}")]
    stages = [dict(kind="review", number=1, title="Ma trận đề", blocks=st0,
                   teacher_note=D["cach_dung"])]
    # đáp án: gộp như đề tháng 9
    grp = [("Đáp án Bài I", [0]), ("Đáp án Bài II", [1]), ("Đáp án Bài III và Bài IV", [2, 3]), ("Đáp án Bài V và biểu điểm", [4])]
    for j, (ti, idx) in enumerate(grp, 2):
        blocks = []
        for i in idx:
            b = D["bai"][i]
            diem = sum(r[4] for r in b["mt"])
            tieu_de = f"\\textbf{{{b['label'].upper().replace('.', '')} ({d(diem)} điểm).}}"
            blocks.append(dict(type="para", text=tieu_de))
            if b.get("hinh_da"):
                blocks.append(dict(type="figure", tikz=b["hinh_da"], width="0.66\\linewidth"))
            if b.get("figure"):
                blocks.append(dict(type="figure", tikz=b["figure"]["tikz"], width="0.5\\linewidth"))
            for a in b["dap_an"]:
                blocks.append(dict(type="para", text=a))
            blocks.append(dict(type="para", text="\\textit{\\footnotesize Lưu ý chấm: " + b["note"] + "}"))
        if j == 5:
            bd = BR.join(f"\\textbf{{{b['label']} ({d(sum(r[4] for r in b['mt']))}đ):}} " +
                         " $-$ ".join(f"{r[0]} {d(r[4])}đ" for r in b["mt"]) for b in D["bai"])
            blocks.append(dict(type="para", text="\\textbf{BIỂU ĐIỂM TỔNG HỢP}" + BR + bd))
            blocks.append(dict(type="para", text="\\textbf{Tổng: 10,0 điểm.} Điểm toàn bài làm tròn đến $0{,}25$ điểm. "
                                                 "Học sinh giải theo cách khác đúng vẫn cho điểm tối đa từng phần. Bài hình vẽ sai hình không chấm điểm."))
        stages.append(dict(kind=KIND[j - 1], number=j, title=ti, blocks=blocks))
    if k == "gk1":
        stages[-1]["blocks"] += [
            dict(type="para", text="\\textbf{ĐÁNH GIÁ VÌ SỰ TIẾN BỘ -- BẢN ĐỒ DẠNG QUA 4 ĐỀ}" + BR +
                 "Mỗi dạng được ôn ở 3 đề với độ khó tăng dần một nấc; đề GK1 đo lại đúng dạng đó bằng câu của trường khác. "
                 "Bài nào HS mất điểm ở GK1 thì tra cột tương ứng để biết cần ôn lại đề nào, câu nào."),
            dict(type="para", text=bang_tien_bo()),
            dict(type="para", text="\\textbf{PHIẾU THEO DÕI TIẾN BỘ (ghi điểm từng bài của mỗi học sinh)}" + BR +
                 "\\textbf{Mức thành thạo:} Bài I $\\ge 2{,}5$ -- Bài II $\\ge 2{,}5$ -- Bài III đủ $1{,}0$ -- Bài IV $\\ge 2{,}0$ (lấy trọn a, b)." + BR +
                 "Đạt cả bốn mức là khoảng $8{,}0$ điểm trở lên. Câu V và ý c bài hình ($1{,}0$ điểm) là phần phân loại học sinh khá -- giỏi." + BR +
                 "Cột \\textit{Tiến bộ?}: so điểm GK1 với điểm cao nhất của bài đó ở 3 đề ôn; bài nào GK1 thấp hơn thì tra bản đồ dạng ở trên để ôn lại."),
            dict(type="para", text=bang_theo_doi()),
        ]
    else:
        so = int(k[-1])
        nxt = {1: "Đề ôn 2 giữ nguyên các dạng nhưng nâng một nấc suy luận (BPT ra vô nghiệm, lượng giác hai bước, phân giác -- trung điểm) và thêm dạng lập bất phương trình.",
               2: "Đề ôn 3 chuyển sang các dạng tần suất thứ nhì (đặt ẩn phụ, lập hệ chuyển động, bốn điểm cùng thuộc đường tròn, tối ưu hai ràng buộc).",
               3: "Đề GK1 chính thức đo lại toàn bộ dạng của 3 đề ôn bằng câu của trường khác -- xem bản đồ tiến bộ trong file đáp án đề GK1."}[so]
        stages[-1]["blocks"].append(dict(type="para", text="\\textbf{SAU ĐỀ NÀY}" + BR + nxt + BR +
                                         "Chữa bài: ưu tiên các ý HS mất điểm vì \\textit{trình bày} (thiếu ĐKXĐ, thiếu đơn vị, thiếu câu kết luận) "
                                         "trước, rồi mới tới ý khó -- đó là điểm lấy lại nhanh nhất."))
    tit = ("Ma trận đề và đáp án chi tiết — Đề GK1 chính thức" if k == "gk1" else f"Ma trận đề và đáp án chi tiết — Đề ôn tập số {k[-1]}")
    return dict(slug=D["slug_mt"], title=tit, eyebrow="TÀI LIỆU GIÁO VIÊN • LỚP 9 • " + D["ten"], grade_label="Lớp 9",
                class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


for k, D in DE.items():
    (OUT / f"{D['slug_de']}.json").write_text(json.dumps(de_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / f"{D['slug_mt']}.json").write_text(json.dumps(mt_json(k, D), ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", k)
