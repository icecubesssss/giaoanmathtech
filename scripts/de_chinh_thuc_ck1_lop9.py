#!/usr/bin/env python3
"""3 ĐỀ KIỂM TRA CUỐI HỌC KÌ I CHÍNH THỨC — TOÁN 9 (90 PHÚT)
Sinh 3 đề kiểm tra chính thức (Đề 1, Đề 2, Đề 3) + 3 file Ma trận đề và đáp án chi tiết
vào inputs/seeds/lop-9/bo-de/de-on-tap-cuoi-ki-1/.
Tất cả các đề bốc từ đề thi thật của các trường/quận Hà Nội chưa dùng ở 3 đề ôn tập.
Tỉ lệ: NB 20% · TH 55-60% · VD 17-20% · VDC 5% (bám sát thống kê 11 đề CK1 Hà Nội 2025-2026).
Đề HS căn chỉnh đúng 2 trang (Trang 1: Bài I, II, III; Trang 2: Bài IV, V).
"""
import json
import re as _re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from de_chinh_thuc_ck1_lop9_hinh import TOA_DO as T  # noqa: E402

OUT = ROOT / "inputs/seeds/lop-9/de-on-tap-cuoi-ki-1"
OUT.mkdir(parents=True, exist_ok=True)
BR = " [[br]] "


def d(x):  # 0.25 -> "0,25"
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"


def st(text, diem=None):
    return text + (f" \\hfill \\textit{{({d(diem)}đ)}}" if diem else "")


def bo_tuong_duong(t):
    out = []
    for seg in _re.split(r"(\$[^$]*\$)", t):
        if not (seg.startswith("$") and seg.endswith("$") and len(seg) > 1):
            seg = _re.sub(r"(?<=[.])\s+(?=[A-ZĐÂĂÊÔƠƯ])", BR, seg)
            out.append(seg)
            continue
        m = seg[1:-1]
        m = _re.sub(r"\\Leftrightarrow", f"${BR}$", m)
        m = _re.sub(r"^\\Leftrightarrow\s*", "", m)
        out.append(f"${m}$")
    return "".join(out)


def y(ten, diem, buoc):
    r = [f"\\textbf{{{ten} ({d(diem)}đ)}}"] if ten else []
    for b in buoc:
        if isinstance(b, tuple):
            txt, sc = b
            r.append(bo_tuong_duong(txt) + f" \\hfill \\textit{{({d(sc)}đ)}}")
        else:
            r.append(bo_tuong_duong(b))
    return BR.join(r)


# Hình vẽ thực tế
TIKZ_CAU = (
    "\\begin{tikzpicture}[line width=0.8pt,scale=0.65]\n"
    "  \\coordinate (B) at (0,0);\\coordinate (C) at (4.2,0);\\coordinate (A) at (0,3.5);\n"
    "  \\draw (-0.5,0)--(5.0,0);\\draw[line width=1.4pt,green!50!black] (B)--(A);\n"
    "  \\draw (A)--(C);\\draw (B)--(C);\n"
    "  \\draw[line width=0.5pt] (0.25,0)--(0.25,0.25)--(0,0.25);\n"
    "  \\draw[line width=0.6pt] (C) ++(180:0.6) arc (180:140:0.6);\n"
    "  \\node at (3.2,0.25) {$55^\\circ$};\n"
    "  \\node[left] at (A) {$A$};\\node[below left] at (B) {$B$};\\node[below right] at (C) {$C$};\n"
    "  \\draw[<->,line width=0.5pt] (0,-0.35)--(4.2,-0.35);\\node[below=2pt] at (2.1,-0.35) {$6$ m};\n"
    "\\end{tikzpicture}"
)

TIKZ_MAYBAY = (
    "\\begin{tikzpicture}[line width=0.8pt,scale=0.65]\n"
    "  \\coordinate (A) at (0,0);\\coordinate (B) at (5.0,0);\\coordinate (C) at (5.0,2.23);\n"
    "  \\draw (-0.5,0)--(5.8,0);\\draw (A)--(C)--(B);\n"
    "  \\draw[line width=0.5pt] (5.0,0.25)--(4.75,0.25)--(4.75,0);\n"
    "  \\draw[line width=0.6pt] (A) ++(0:0.8) arc (0:24:0.8);\n"
    "  \\node at (1.2,0.25) {$24^\\circ$};\n"
    "  \\node[below left] at (A) {$A$};\\node[below] at (B) {$B$};\\node[above right] at (C) {$C$};\n"
    "  \\node[above left] at (2.5,1.2) {$12$ km};\n"
    "\\end{tikzpicture}"
)

TIKZ_HAIDANG = (
    "\\begin{tikzpicture}[line width=0.8pt,scale=0.65]\n"
    "  \\coordinate (B) at (0,0);\\coordinate (A) at (0,3.0);\\coordinate (C) at (4.5,0);\n"
    "  \\draw (-0.5,0)--(5.2,0);\\draw[line width=1.5pt] (B)--(A);\n"
    "  \\draw (A)--(C);\\draw (B)--(C);\n"
    "  \\draw[line width=0.5pt] (0.25,0)--(0.25,0.25)--(0,0.25);\n"
    "  \\draw[dashed] (A)--(2.5,3.0);\n"
    "  \\draw[line width=0.6pt] (A) ++(0:0.7) arc (0:-33.7:0.7);\n"
    "  \\node at (1.1,2.8) {$28^\\circ$};\n"
    "  \\node[left] at (A) {$A$};\\node[below left] at (B) {$B$};\\node[below right] at (C) {$C$};\n"
    "  \\node[left] at (0,1.5) {$45$ m};\n"
    "\\end{tikzpicture}"
)


def hinh_ct1_da():
    return (
        "\\begin{tikzpicture}[scale=1.1,line width=0.8pt]\n"
        "  \\coordinate (O) at (0,0);\\coordinate (A) at (-2,0);\\coordinate (B) at (2,0);\n"
        "  \\coordinate (C) at (1,1.732);\\coordinate (H) at (1,0);\\coordinate (M) at (-2,3.464);\n"
        "  \\coordinate (K) at (1,0.866);\n"
        "  \\draw (-2.5,0)--(2.5,0);\\draw (A)--(M)--(C)--(B);\\draw (O)--(C);\\draw (M)--(B);\n"
        "  \\draw (C)--(H);\\draw[dashed] (O)--(M);\n"
        "  \\draw[gray!60] (0,0) circle (2.0);\n"
        "  \\draw[line width=0.5pt] (-2,0.2)--(-1.8,0.2)--(-1.8,0);\n"
        "  \\draw[line width=0.5pt] (1,0.2)--(0.8,0.2)--(0.8,0);\n"
        "  \\fill (O) circle (1.5pt);\\node[below] at (O) {$O$};\n"
        "  \\fill (A) circle (1.5pt);\\node[below left] at (A) {$A$};\n"
        "  \\fill (B) circle (1.5pt);\\node[below right] at (B) {$B$};\n"
        "  \\fill (C) circle (1.5pt);\\node[above right] at (C) {$C$};\n"
        "  \\fill (H) circle (1.5pt);\\node[below] at (H) {$H$};\n"
        "  \\fill (M) circle (1.5pt);\\node[above left] at (M) {$M$};\n"
        "  \\fill (K) circle (1.5pt);\\node[right=2pt] at (K) {$K$};\n"
        "\\end{tikzpicture}"
    )


def hinh_ct2_da():
    return (
        "\\begin{tikzpicture}[scale=1.1,line width=0.8pt]\n"
        "  \\coordinate (O) at (0,0);\\coordinate (A) at (-3.8,0);\n"
        "  \\coordinate (B) at (-1.0,1.732);\\coordinate (C) at (-1.0,-1.732);\n"
        "  \\coordinate (H) at (-1.0,0);\\coordinate (I) at (-2.0,0);\n"
        "  \\coordinate (D) at (1.0,-1.732);\\coordinate (K) at (0.5,-0.866);\n"
        "  \\draw (A)--(B)--(D)--(C)--(A);\\draw (O)--(B);\\draw (O)--(C);\\draw (A)--(O);\n"
        "  \\draw (B)--(C);\\draw (C)--(K);\n"
        "  \\draw[gray!60] (0,0) circle (2.0);\n"
        "  \\draw[line width=0.5pt] (-1.139,1.652)--(-1.059,1.513)--(-0.920,1.593);\n"
        "  \\draw[line width=0.5pt] (-1.139,-1.652)--(-1.059,-1.513)--(-0.920,-1.593);\n"
        "  \\draw[line width=0.5pt] (-1.15,0)--(-1.15,0.15)--(-1.0,0.15);\n"
        "  \\fill (O) circle (1.5pt);\\node[above right] at (O) {$O$};\n"
        "  \\fill (A) circle (1.5pt);\\node[left] at (A) {$A$};\n"
        "  \\fill (B) circle (1.5pt);\\node[above] at (B) {$B$};\n"
        "  \\fill (C) circle (1.5pt);\\node[below] at (C) {$C$};\n"
        "  \\fill (H) circle (1.5pt);\\node[above right] at (H) {$H$};\n"
        "  \\fill (I) circle (1.5pt);\\node[above right=3pt] at (I) {$I$};\n"
        "  \\fill (D) circle (1.5pt);\\node[below right] at (D) {$D$};\n"
        "  \\fill (K) circle (1.5pt);\\node[above right] at (K) {$K$};\n"
        "\\end{tikzpicture}"
    )


def hinh_ct3_da():
    return (
        "\\begin{tikzpicture}[scale=1.1,line width=0.8pt]\n"
        "  \\coordinate (O) at (0,0);\\coordinate (A) at (-3.8,0);\n"
        "  \\coordinate (B) at (-1.0,1.732);\\coordinate (C) at (-1.0,-1.732);\n"
        "  \\coordinate (D) at (1.0,-1.732);\\coordinate (E) at (-2.0,0);\n"
        "  \\coordinate (M) at (-2.4,0.866);\\coordinate (H) at (-1.0,0);\n"
        "  \\draw (A)--(B)--(D)--(C)--(A);\\draw (O)--(B);\\draw (O)--(C);\\draw (A)--(O);\n"
        "  \\draw (B)--(C);\\draw (C)--(E)--(M);\\draw (B)--(D);\n"
        "  \\draw[gray!60] (0,0) circle (2.0);\n"
        "  \\draw[line width=0.5pt] (-1.15,0)--(-1.15,0.15)--(-1.0,0.15);\n"
        "  \\fill (O) circle (1.5pt);\\node[above right] at (O) {$O$};\n"
        "  \\fill (A) circle (1.5pt);\\node[left] at (A) {$A$};\n"
        "  \\fill (B) circle (1.5pt);\\node[above] at (B) {$B$};\n"
        "  \\fill (C) circle (1.5pt);\\node[below] at (C) {$C$};\n"
        "  \\fill (D) circle (1.5pt);\\node[below right] at (D) {$D$};\n"
        "  \\fill (E) circle (1.5pt);\\node[below left] at (E) {$E$};\n"
        "  \\fill (M) circle (1.5pt);\\node[above left] at (M) {$M$};\n"
        "\\end{tikzpicture}"
    )


# ─────────────────────────── NGUỒN VÀ LUẬT ───────────────────────────
QUAN = {
    "THCS Dịch Vọng (2025–2026)": "Cầu Giấy",
    "THCS Chu Văn An (2025–2026)": "Tây Hồ",
    "THCS Phương Hà Đông (2025–2026)": "Hà Đông",
    "THCS Thái Thịnh (2025–2026)": "Đống Đa",
    "THCS Cầu Diễn (2025–2026)": "Nam Từ Liêm",
    "THCS Phúc Đồng (2025–2026)": "Long Biên",
    "THCS Trưng Vương (2025–2026)": "Hoàn Kiếm",
    "THCS Tân Triều (2025–2026)": "Thanh Trì",
    "THCS Ba Đình (2025–2026)": "Ba Đình",
    "THCS Ngọc Lâm (2025–2026)": "Long Biên",
    "THCS Đống Đa (2025–2026)": "Đống Đa",
    "THCS Ngọc Thụy (2025–2026)": "Long Biên",
    "THCS Lý Thánh Tông (2025–2026)": "Gia Lâm",
    "THCS Ngô Sĩ Liên (2025–2026)": "Hoàn Kiếm",
}


def kiem_nguon():
    from collections import defaultdict

    tq, tt, bao_cao = defaultdict(float), defaultdict(float), {}
    for k, D in DE_CT.items():
        q = defaultdict(float)
        for b in D["bai"]:
            for r in b["mt"]:
                src = r[6]
                assert src in QUAN, f"Chưa khai báo quận cho trường: {src}"
                dist = QUAN[src]
                q[dist] += r[4]
                tq[dist] += r[4]
                tt[src] += r[4]
        assert len(q) >= 4, f"Đề {k} chỉ có {len(q)} quận ({dict(q)}), yêu cầu >= 4 quận!"
        assert max(q.values()) <= 4.0 + 1e-9, f"Đề {k} có quận chiếm quá 40% ({dict(q)})!"
        truong = {r[6] for b in D["bai"] for r in b["mt"]}
        bao_cao[k] = (len(truong), q)
    assert max(tq.values()) <= 7.5 + 1e-9, f"Cả bộ có quận chiếm quá 25% ({dict(tq)})!"
    assert max(tt.values()) <= 4.5 + 1e-9, f"Cả bộ có trường chiếm quá 15% ({dict(tt)})!"
    return bao_cao, tq


# ─────────────────────────── NỘI DUNG 3 ĐỀ CHÍNH THỨC ───────────────────────────
DE_CT = {
    "ct1": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-1",
        "slug_mt": "ma-tran-va-dap-an-ck1-chinh-thuc-so-1",
        "eyebrow": "LỚP 9 • ĐỀ CHÍNH THỨC SỐ 1",
        "bai": [
            {
                "label": "Bài I.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Cho hai biểu thức: "
                    + BR
                    + "$A = \\dfrac{\\sqrt{x}}{\\sqrt{x}+3}$ và $B = \\dfrac{x+9}{x-9} - \\dfrac{3}{\\sqrt{x}-3}$ với $x \\ge 0; x \\ne 9$."
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 4 - 2\\sqrt{3}$."
                    + BR
                    + "2) \\textbf{(1,0 điểm)} Rút gọn biểu thức $B$."
                    + BR
                    + "3) \\textbf{(0,5 điểm)} Cho $P = A \\cdot B$. Tìm các giá trị của $x$ để $P = \\dfrac{1}{4}$."
                ),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Ta có: $x = 4 - 2\\sqrt{3} = 3 - 2\\sqrt{3} + 1 = (\\sqrt{3}-1)^2$ (thoả mãn điều kiện)."),
                        ("Suy ra $\\sqrt{x} = \\sqrt{(\\sqrt{3}-1)^2} = |\\sqrt{3}-1| = \\sqrt{3}-1$ (do $\\sqrt{3} > 1$).", 0.25),
                        ("Thay vào biểu thức $A$: $A = \\dfrac{\\sqrt{3}-1}{\\sqrt{3}-1+3} = \\dfrac{\\sqrt{3}-1}{\\sqrt{3}+2} = \\dfrac{(\\sqrt{3}-1)(2-\\sqrt{3})}{(2+\\sqrt{3})(2-\\sqrt{3})} = 3\\sqrt{3}-5$."),
                        ("Vậy khi $x = 4 - 2\\sqrt{3}$ thì $A = 3\\sqrt{3}-5$.", 0.25),
                    ]),
                    y("2)", 1.0, [
                        ("Với $x \\ge 0, x \\ne 9$, ta có mẫu chung là $x - 9 = (\\sqrt{x}-3)(\\sqrt{x}+3)$."),
                        ("$B = \\dfrac{x + 9 - 3(\\sqrt{x}+3)}{(\\sqrt{x}-3)(\\sqrt{x}+3)}$", 0.25),
                        ("$B = \\dfrac{x + 9 - 3\\sqrt{x} - 9}{(\\sqrt{x}-3)(\\sqrt{x}+3)} = \\dfrac{x - 3\\sqrt{x}}{(\\sqrt{x}-3)(\\sqrt{x}+3)}$", 0.25),
                        ("$B = \\dfrac{\\sqrt{x}(\\sqrt{x}-3)}{(\\sqrt{x}-3)(\\sqrt{x}+3)} = \\dfrac{\\sqrt{x}}{\\sqrt{x}+3}$", 0.25),
                        ("Vậy $B = \\dfrac{\\sqrt{x}}{\\sqrt{x}+3}$.", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("Ta có: $P = A \\cdot B = \\dfrac{\\sqrt{x}}{\\sqrt{x}+3} \\cdot \\dfrac{\\sqrt{x}}{\\sqrt{x}+3} = \\left(\\dfrac{\\sqrt{x}}{\\sqrt{x}+3}\\right)^2$"),
                        ("Để $P = \\dfrac{1}{4}$ thì $\\dfrac{\\sqrt{x}}{\\sqrt{x}+3} = \\dfrac{1}{2}$ (vì $\\sqrt{x} \\ge 0$)", 0.25),
                        ("$2\\sqrt{x} = \\sqrt{x} + 3 \\Rightarrow \\sqrt{x} = 3 \\Rightarrow x = 9$ (không thoả mãn ĐKXĐ $x \\ne 9$, loại)."),
                        ("Vậy không tồn tại giá trị nào của $x$ để $P = \\dfrac{1}{4}$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("Ia", "Tính giá trị biểu thức căn tại $x = 4 - 2\\sqrt{3}$", "ĐS III", "NB", 0.5, 4, "THCS Dịch Vọng (2025–2026)"),
                    ("Ib", "Rút gọn phân thức chứa căn bậc hai", "ĐS III", "TH", 1.0, 9, "THCS Dịch Vọng (2025–2026)"),
                    ("Ic", "Giải phương trình $P = k$ có bẫy loại nghiệm ĐKXĐ", "ĐS III", "VD", 0.5, 6, "THCS Dịch Vọng (2025–2026)"),
                ],
                "note": "Bẫy loại nghiệm: giải ra $x = 9$ phải đối chiếu ĐKXĐ để kết luận không có $x$ thoả mãn.",
            },
            {
                "label": "Bài II.",
                "level": 3,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                    + BR
                    + "Trong đợt tham quan học tập trải nghiệm, một trường THCS có $510$ người gồm học sinh và cán bộ nhà trường tham gia. "
                    "Nhà trường dự định thuê hai loại xe ô tô: xe loại $45$ chỗ và xe loại $30$ chỗ. "
                    "Biết rằng số xe loại $45$ chỗ nhiều hơn số xe loại $30$ chỗ là $3$ xe và tất cả các xe đều chở vừa đủ số người theo quy định. "
                    "Hỏi nhà trường đã thuê bao nhiêu xe mỗi loại?"
                ),
                "dap_an": [
                    y("", 2.0, [
                        ("Gọi số xe loại $45$ chỗ là $x$ (xe) và số xe loại $30$ chỗ là $y$ (xe).", 0.25),
                        ("Điều kiện: $x, y \\in \\mathbb{N}^*$ và $x > 3$."),
                        ("Vì số xe $45$ chỗ nhiều hơn số xe $30$ chỗ là $3$ xe nên ta có phương trình: $x - y = 3$ (1)", 0.5),
                        ("Tổng số người đi tham quan là $510$ người nên ta có phương trình: $45x + 30y = 510$ (2)", 0.5),
                        ("Từ (1) suy ra: $x = y + 3$. Thế vào (2): $45(y + 3) + 30y = 510$"),
                        ("$75y + 135 = 510 \\Rightarrow 75y = 375 \\Rightarrow y = 5$ (thoả mãn).", 0.5),
                        ("Suy ra $x = 5 + 3 = 8$ (thoả mãn)."),
                        ("Vậy nhà trường đã thuê $8$ xe loại $45$ chỗ và $5$ xe loại $30$ chỗ.", 0.25),
                    ])
                ],
                "mt": [("II", "Toán thực tế số lượng xe vận chuyển (lập hệ phương trình bậc nhất hai ẩn)", "ĐS I", "TH", 2.0, 15, "THCS Phương Hà Đông (2025–2026)")],
                "note": "Học sinh chú ý điều kiện nguyên dương của số xe.",
            },
            {
                "label": "Bài III.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                    + BR
                    + "1) \\textbf{(0,75 điểm)} $\\begin{cases} 2x + 3y = 8 \\\\ 3x - y = 1 \\end{cases}$"
                    + BR
                    + "2) \\textbf{(0,75 điểm)} $\\dfrac{2x}{x+1} - \\dfrac{3}{x-2} = 2$"
                    + BR
                    + "3) \\textbf{(0,5 điểm)} $\\dfrac{2x-3}{4} - 1 \\le \\dfrac{x+1}{3}$"
                ),
                "dap_an": [
                    y("1)", 0.75, [
                        ("Ta có: từ phương trình thứ hai suy ra $y = 3x - 1$."),
                        ("Thế vào phương trình thứ nhất: $2x + 3(3x - 1) = 8$", 0.25),
                        ("$11x - 3 = 8 \\Rightarrow 11x = 11 \\Rightarrow x = 1$", 0.25),
                        ("Thay $x = 1$ vào $y = 3(1) - 1 = 2$."),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = (1; 2)$.", 0.25),
                    ]),
                    y("2)", 0.75, [
                        ("Điều kiện xác định: $x \\ne -1$ và $x \\ne 2$."),
                        ("Quy đồng khử mẫu: $2x(x-2) - 3(x+1) = 2(x+1)(x-2)$", 0.25),
                        ("$2x^2 - 4x - 3x - 3 = 2(x^2 - x - 2)$"),
                        ("$2x^2 - 7x - 3 = 2x^2 - 2x - 4$"),
                        ("$-5x = -1 \\Rightarrow x = \\dfrac{1}{5}$", 0.25),
                        ("Giá trị $x = \\dfrac{1}{5}$ thoả mãn ĐKXĐ. Vậy nghiệm của phương trình là $x = \\dfrac{1}{5}$.", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("Mẫu chung là $12$. Quy đồng khử mẫu: $3(2x-3) - 12 \\le 4(x+1)$"),
                        ("$6x - 9 - 12 \\le 4x + 4$", 0.25),
                        ("$2x \\le 25 \\Rightarrow x \\le 12{,}5$"),
                        ("Vậy nghiệm của bất phương trình là $x \\le 12{,}5$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IIIa", "Giải hệ phương trình bậc nhất hai ẩn", "ĐS I", "TH", 0.75, 6, "THCS Thái Thịnh (2025–2026)"),
                    ("IIIb", "Giải phương trình chứa ẩn ở mẫu quy về bậc nhất", "ĐS I", "TH", 0.75, 8, "THCS Thái Thịnh (2025–2026)"),
                    ("IIIc", "Giải bất phương trình bậc nhất một ẩn", "ĐS II", "NB", 0.5, 5, "THCS Cầu Diễn (2025–2026)"),
                ],
                "note": "Phương trình chứa ẩn ở mẫu luôn phải có bước đối chiếu ĐKXĐ.",
            },
            {
                "label": "Bài IV.",
                "level": 3,
                "statement": (
                    "\\textbf{(3,5 điểm)} "
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Một cây cau có bóng in trên mặt đất dài $6$ m khi tia nắng mặt trời tạo với mặt đất một góc $55^\\circ$. "
                    "Tính chiều cao của cây cau (kết quả làm tròn đến chữ số thập phân thứ nhất)."
                    + BR
                    + "2) \\textbf{(3,0 điểm)} Cho đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $C$ trên nửa đường tròn sao cho $AC < BC$. "
                    "Kẻ $CH \\perp AB$ tại $H$. Tiếp tuyến tại $A$ và tiếp tuyến tại $C$ của $(O)$ cắt nhau tại điểm $M$."
                    + BR
                    + "a) \\textbf{(1,0 điểm)} Chứng minh bốn điểm $M, A, O, C$ cùng thuộc một đường tròn."
                    + BR
                    + "b) \\textbf{(1,0 điểm)} Chứng minh $OM \\perp AC$ và $MC^2 = MH \\cdot MO$."
                    + BR
                    + "c) \\textbf{(1,0 điểm)} Đoạn thẳng $MB$ cắt $CH$ tại $K$. Chứng minh rằng $K$ là trung điểm của $CH$."
                ),
                "figure": {"tikz": TIKZ_CAU, "caption": "Minh hoạ Bài IV.1"},
                "hinh_da": hinh_ct1_da(),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Gọi $AB$ là chiều cao cây cau ($AB \\perp BC$), $BC$ là bóng trên mặt đất ($BC = 6$ m)."),
                        ("Góc tia nắng với mặt đất là $\\widehat{ACB} = 55^\\circ$."),
                        ("Xét tam giác $ABC$ vuông tại $B$: $AB = BC \\cdot \\tan \\widehat{ACB} = 6 \\cdot \\tan 55^\\circ$", 0.25),
                        ("$AB \\approx 6 \\cdot 1{,}4281 \\approx 8{,}6$ (m)."),
                        ("Vậy cây cau cao khoảng $8{,}6$ mét.", 0.25),
                    ]),
                    y("2a)", 1.0, [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Vì $MA$ là tiếp tuyến tại $A$ nên $MA \\perp OA \\Rightarrow \\widehat{MAO} = 90^\\circ$."),
                        ("Vì $MC$ là tiếp tuyến tại $C$ nên $MC \\perp OC \\Rightarrow \\widehat{MCO} = 90^\\circ$.", 0.25),
                        ("Xét tam giác $MAO$ vuông tại $A \\Rightarrow M, A, O$ thuộc đường tròn đường kính $MO$."),
                        ("Xét tam giác $MCO$ vuông tại $C \\Rightarrow M, C, O$ thuộc đường tròn đường kính $MO$.", 0.25),
                        ("Do đó bốn điểm $M, A, O, C$ cùng thuộc đường tròn đường kính $MO$.", 0.25),
                    ]),
                    y("2b)", 1.0, [
                        ("Ta có $MA = MC$ (tính chất hai tiếp tuyến cắt nhau) và $OA = OC = R$."),
                        ("Suy ra $OM$ là đường trung trực của $AC$, do đó $OM \\perp AC$ tại trung điểm $I$.", 0.25),
                        ("Xét tam giác $MCO$ vuông tại $C$, có đường cao $CI$: $MC^2 = MI \\cdot MO$ (hệ quả tam giác đồng dạng)."),
                        ("Xét $\\triangle MCI$ và $\\triangle MOC$: có $\\widehat{MCI} = \\widehat{MOC}$ và $\\widehat{M}$ chung $\\Rightarrow \\triangle MCI \\backsim \\triangle MOC$ (g.g).", 0.25),
                        ("Suy ra $\\dfrac{MC}{MO} = \\dfrac{MI}{MC} \\Rightarrow MC^2 = MI \\cdot MO$.", 0.5),
                    ]),
                    y("2c)", 1.0, [
                        ("Vì $MA \\perp AB$ và $CH \\perp AB$ nên $CH \\parallel MA$."),
                        ("Trong $\\triangle MAB$, vì $CK \\parallel MA$ (do $K \\in CH$) nên theo hệ quả định lí Thalès:"),
                        ("$\\dfrac{CK}{MA} = \\dfrac{BK}{BM}$ (1)"),
                        ("Kéo dài $BC$ cắt $MA$ tại $E$. Tam giác $ABC$ vuông tại $C$ có $AC \\perp BE$."),
                        ("Chứng minh được $M$ là trung điểm của $AE$.", 0.25),
                        ("Trong tam giác $EBA$, vì $CK \\parallel EA$ nên $\\dfrac{CK}{EA} = \\dfrac{BK}{BE}$.", 0.25),
                        ("Áp dụng định lí Thalès cho $KH$ và $CK$ suy ra $CK = KH$.", 0.25),
                        ("Vậy $K$ là trung điểm của $CH$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IVa", "Toán thực tế tỉ số lượng giác tan tính chiều cao cây cau", "HH IV", "NB", 0.5, 5, "THCS Cầu Diễn (2025–2026)"),
                    ("IVb1", "Bốn điểm cùng thuộc một đường tròn", "HH V", "TH", 1.0, 7, "THCS Phúc Đồng (2025–2026)"),
                    ("IVb2", "Đường trung trực và hệ thức tiếp tuyến", "HH V", "TH", 1.0, 10, "THCS Dịch Vọng (2025–2026)"),
                    ("IVb3", "Chứng minh trung điểm bằng hệ quả định lí Thalès", "HH V", "VD", 1.0, 12, "THCS Phúc Đồng (2025–2026)"),
                ],
                "note": "Câu c là bài toán kinh điển về tỉ số Thalès và trung điểm trong hình học đường tròn.",
            },
            {
                "label": "Bài V.",
                "level": 4,
                "statement": (
                    "\\textbf{(0,5 điểm)} Một người nông dân có một tấm tôn phẳng hình chữ nhật dài $3$ m và rộng $60$ cm. "
                    "Người đó muốn gập hai bên mép tấm tôn lên một góc $90^\\circ$ để tạo thành một máng dẫn nước có mặt cắt ngang là hình chữ nhật. "
                    "Hỏi người đó phải gập mỗi bên mép lên một đoạn có chiều cao bằng bao nhiêu centimet để diện tích mặt cắt ngang của máng đạt giá trị lớn nhất?"
                ),
                "dap_an": [
                    y("", 0.5, [
                        ("Gọi chiều cao mỗi bên mép gập lên là $x$ (cm)."),
                        ("Điều kiện: $0 < x < 30$."),
                        ("Khi đó chiều rộng của đáy máng là: $60 - 2x$ (cm)."),
                        ("Diện tích mặt cắt ngang của máng là: $S = x(60 - 2x) = 60x - 2x^2$ ($cm^2$).", 0.25),
                        ("Ta có: $S = -2(x^2 - 30x) = -2(x^2 - 30x + 225) + 450 = 450 - 2(x - 15)^2 \\le 450$."),
                        ("Dấu bằng xảy ra khi $x - 15 = 0 \\Rightarrow x = 15$ (thoả mãn điều kiện)."),
                        ("Vậy người đó cần gập mỗi bên mép lên $15$ cm để diện tích mặt cắt ngang lớn nhất (đạt $450\\text{ cm}^2$).", 0.25),
                    ])
                ],
                "mt": [("V", "Bài toán thực tế cực trị: Gập tôn làm máng nước diện tích lớn nhất", "ĐS II", "VDC", 0.5, 7, "THCS Cầu Diễn (2025–2026)")],
                "note": "Học sinh sử dụng biến đổi hằng đẳng thức lớp 8-9 để tìm GTLN của tam thức bậc hai.",
            },
        ],
        "bay": [
            ("Bài I.1", "Khai căn HĐT $4 - 2\\sqrt{3}$", "Bấm máy ra số thập phân hoặc không viết bước $|\\sqrt{3}-1| = \\sqrt{3}-1$.", "Viết rõ $4 - 2\\sqrt{3} = (\\sqrt{3}-1)^2$, do $\\sqrt{3} > 1$ nên $|\\sqrt{3}-1| = \\sqrt{3}-1$."),
            ("Bài I.3", "Phương trình phân thức vô nghiệm (TỬ HUYỆT)", "Giải ra $x = 9$ hớn hở nhận nghiệm (bị 0đ do $x = 9$ trùng ĐKXĐ).", "ĐKXĐ $x \\ne 9$, nghiệm $x = 9$ bị LOẠI. Kết luận: không có giá trị nào của $x$ thoả mãn."),
            ("Bài II", "Điều kiện nguyên dương số xe", "Đặt điều kiện $x, y > 0$ chung chung mà quên điều kiện nguyên dương $x, y \\in \\mathbb{N}^*$.", "Số xe phải là số nguyên dương: $x, y \\in \\mathbb{N}^*$ và $x > 3$."),
            ("Bài III.2", "Phương trình chứa ẩn ở mẫu", "Quy đồng quên đóng mở ngoặc $-(x-2)$ dẫn tới sai dấu tử số.", "ĐKXĐ $x \\ne -1, x \\ne 2$. Quy đồng cẩn thận từng bước và đối chiếu nghiệm."),
            ("Bài IV.2a", "Bốn điểm cùng thuộc đường tròn", "Ghi tứ giác nội tiếp do tổng hai góc đối bằng $180^\\circ$ (bị 0đ).", "HK1 bắt buộc chứng minh qua hai tam giác vuông cùng chung cạnh huyền $MO$."),
            ("Bài IV.2b", "Hệ thức tiếp tuyến $MC^2 = MI \\cdot MO$", "Áp dụng trực tiếp công thức mà không chứng minh qua tam giác đồng dạng.", "Bắt buộc chứng minh $\\triangle MCI \\backsim \\triangle MOC$ (g.g) để suy ra hệ thức tích."),
        ],
    },
    "ct2": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-2",
        "slug_mt": "ma-tran-va-dap-an-ck1-chinh-thuc-so-2",
        "eyebrow": "LỚP 9 • ĐỀ CHÍNH THỨC SỐ 2",
        "bai": [
            {
                "label": "Bài I.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Cho hai biểu thức: "
                    + BR
                    + "$A = \\dfrac{\\sqrt{x}+1}{\\sqrt{x}-2}$ và $B = \\dfrac{\\sqrt{x}}{\\sqrt{x}+2} + \\dfrac{4\\sqrt{x}}{x-4}$ với $x \\ge 0; x \\ne 4$."
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 25$."
                    + BR
                    + "2) \\textbf{(1,0 điểm)} Rút gọn biểu thức $B$."
                    + BR
                    + "3) \\textbf{(0,5 điểm)} Cho biểu thức $P = \\dfrac{B}{A}$. Tìm tất cả các giá trị nguyên của $x$ để $P \\le \\dfrac{1}{2}$."
                ),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Thay $x = 25$ (thoả mãn ĐKXĐ) vào biểu thức $A$:"),
                        ("$A = \\dfrac{\\sqrt{25}+1}{\\sqrt{25}-2} = \\dfrac{5+1}{5-2} = \\dfrac{6}{3} = 2$", 0.25),
                        ("Vậy khi $x = 25$ thì $A = 2$.", 0.25),
                    ]),
                    y("2)", 1.0, [
                        ("Với $x \\ge 0; x \\ne 4$, ta có mẫu chung là $x - 4 = (\\sqrt{x}-2)(\\sqrt{x}+2)$."),
                        ("$B = \\dfrac{\\sqrt{x}(\\sqrt{x}-2) + 4\\sqrt{x}}{(\\sqrt{x}-2)(\\sqrt{x}+2)}$", 0.25),
                        ("$B = \\dfrac{x - 2\\sqrt{x} + 4\\sqrt{x}}{(\\sqrt{x}-2)(\\sqrt{x}+2)} = \\dfrac{x + 2\\sqrt{x}}{(\\sqrt{x}-2)(\\sqrt{x}+2)}$", 0.25),
                        ("$B = \\dfrac{\\sqrt{x}(\\sqrt{x}+2)}{(\\sqrt{x}-2)(\\sqrt{x}+2)} = \\dfrac{\\sqrt{x}}{\\sqrt{x}-2}$", 0.25),
                        ("Vậy $B = \\dfrac{\\sqrt{x}}{\\sqrt{x}-2}$.", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("Ta có: $P = \\dfrac{B}{A} = \\dfrac{\\sqrt{x}}{\\sqrt{x}-2} : \\dfrac{\\sqrt{x}+1}{\\sqrt{x}-2} = \\dfrac{\\sqrt{x}}{\\sqrt{x}+1}$"),
                        ("Để $P \\le \\dfrac{1}{2}$ thì $\\dfrac{\\sqrt{x}}{\\sqrt{x}+1} \\le \\dfrac{1}{2} \\Rightarrow 2\\sqrt{x} \\le \\sqrt{x} + 1$", 0.25),
                        ("$\\sqrt{x} \\le 1 \\Rightarrow 0 \\le x \\le 1$."),
                        ("Vì $x$ nguyên và kết hợp ĐKXĐ $x \\ge 0, x \\ne 4$, suy ra $x \\in \\{0; 1\\}$."),
                        ("Vậy các giá trị nguyên cần tìm là $x \\in \\{0; 1\\}$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("Ia", "Tính giá trị biểu thức căn bậc hai tại $x = 25$", "ĐS III", "NB", 0.5, 4, "THCS Chu Văn An (2025–2026)"),
                    ("Ib", "Quy đồng và rút gọn phân thức căn bậc hai", "ĐS III", "TH", 1.0, 9, "THCS Chu Văn An (2025–2026)"),
                    ("Ic", "Giải bất phương trình $P \\le k$ tìm nghiệm nguyên", "ĐS III", "VD", 0.5, 6, "THCS Chu Văn An (2025–2026)"),
                ],
                "note": "Học sinh nhớ lấy nghiệm $x = 0$ (thoả mãn điều kiện không âm).",
            },
            {
                "label": "Bài II.",
                "level": 3,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                    + BR
                    + "Hai tổ công nhân cùng làm chung một đoạn đường thì sau $12$ ngày sẽ hoàn thành. "
                    "Nếu tổ I làm một mình trong $4$ ngày, rồi tổ II làm tiếp một mình trong $10$ ngày thì cả hai tổ hoàn thành được $\\dfrac{7}{12}$ đoạn đường. "
                    "Hỏi nếu mỗi tổ làm một mình thì sau bao nhiêu ngày sẽ hoàn thành đoạn đường đó? (Gợi ý mồi: Coi toàn bộ đoạn đường cần làm là $1$ công việc)."
                ),
                "dap_an": [
                    y("", 2.0, [
                        ("Gọi thời gian tổ I làm một mình xong đoạn đường là $x$ (ngày), tổ II là $y$ (ngày).", 0.25),
                        ("Điều kiện: $x, y > 12$."),
                        ("Trong một ngày, tổ I làm được $\\dfrac{1}{x}$ đoạn đường, tổ II làm được $\\dfrac{1}{y}$ đoạn đường."),
                        ("Vì hai tổ cùng làm thì $12$ ngày xong nên ta có phương trình: $\\dfrac{1}{x} + \\dfrac{1}{y} = \\dfrac{1}{12}$ (1)", 0.5),
                        ("Tổ I làm $4$ ngày, tổ II làm $10$ ngày được $\\dfrac{7}{12}$ đoạn đường: $\\dfrac{4}{x} + \\dfrac{10}{y} = \\dfrac{7}{12}$ (2)", 0.5),
                        ("Đặt $u = \\dfrac{1}{x}, v = \\dfrac{1}{y}$ ($u, v > 0$)."),
                        ("Hệ trở thành: $\\begin{cases} u + v = \\dfrac{1}{12} \\\\ 4u + 10v = \\dfrac{7}{12} \\end{cases}$"),
                        ("Giải hệ ta được: $u = \\dfrac{1}{24}$ và $v = \\dfrac{1}{24}$."),
                        ("Do đó $x = 24, y = 24$ (thoả mãn điều kiện).", 0.5),
                        ("Vậy mỗi tổ làm một mình đều hoàn thành đoạn đường trong $24$ ngày.", 0.25),
                    ])
                ],
                "mt": [("II", "Toán năng suất làm chung làm riêng (lập hệ phương trình mồi)", "ĐS I", "TH", 2.0, 15, "THCS Trưng Vương (2025–2026)")],
                "note": "Dạng toán năng suất làm chung làm riêng có câu hỏi mồi quy ước toàn bộ công việc là 1.",
            },
            {
                "label": "Bài III.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                    + BR
                    + "1) \\textbf{(0,75 điểm)} $\\begin{cases} 3(x+1) - 2(y-2) = 5 \\\\ 2x - 3y = -1 \\end{cases}$"
                    + BR
                    + "2) \\textbf{(0,75 điểm)} $(2x-5)(x+3) = 0$"
                    + BR
                    + "3) \\textbf{(0,5 điểm)} $3x - 4 < 5(x-2)$"
                ),
                "dap_an": [
                    y("1)", 0.75, [
                        ("Phương trình thứ nhất tương đương: $3x + 3 - 2y + 4 = 5 \\Rightarrow 3x - 2y = -2$."),
                        ("Ta có hệ phương trình: $\\begin{cases} 3x - 2y = -2 \\\\ 2x - 3y = -1 \\end{cases}$", 0.25),
                        ("Nhân phương trình đầu với $3$, phương trình hai với $2$: $\\begin{cases} 9x - 6y = -6 \\\\ 4x - 6y = -2 \\end{cases}$"),
                        ("Trừ hai phương trình: $5x = -4 \\Rightarrow x = -\\dfrac{4}{5}$", 0.25),
                        ("Thay vào tìm được $y = -\\dfrac{1}{5}$."),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = \\left(-\\dfrac{4}{5}; -\\dfrac{1}{5}\\right)$.", 0.25),
                    ]),
                    y("2)", 0.75, [
                        ("$(2x-5)(x+3) = 0$"),
                        ("$2x - 5 = 0$ hoặc $x + 3 = 0$", 0.25),
                        ("$2x = 5$ hoặc $x = -3$"),
                        ("$x = \\dfrac{5}{2}$ hoặc $x = -3$", 0.25),
                        ("Vậy phương trình có hai nghiệm $x = \\dfrac{5}{2}$ và $x = -3$.", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("$3x - 4 < 5x - 10$"),
                        ("$3x - 5x < -10 + 4$", 0.25),
                        ("$-2x < -6 \\Rightarrow x > 3$ (chia hai vế cho $-2 < 0$, đổi chiều)."),
                        ("Vậy nghiệm của bất phương trình là $x > 3$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IIIa", "Giải hệ phương trình sau khi khai triển đưa về dạng chuẩn", "ĐS I", "TH", 0.75, 6, "THCS Phúc Đồng (2025–2026)"),
                    ("IIIb", "Giải phương trình tích bậc hai", "ĐS I", "NB", 0.75, 5, "THCS Tân Triều (2025–2026)"),
                    ("IIIc", "Giải bất phương trình bậc nhất có đổi chiều", "ĐS II", "NB", 0.5, 5, "THCS Phúc Đồng (2025–2026)"),
                ],
                "note": "Bất phương trình: lưu ý chia số âm đổi chiều.",
            },
            {
                "label": "Bài IV.",
                "level": 3,
                "statement": (
                    "\\textbf{(3,5 điểm)} "
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Một chiếc máy bay cất cánh tạo với phương nằm ngang một góc $24^\\circ$. "
                    "Hỏi sau khi bay được quãng đường $12$ km theo đường bay thì máy bay đạt độ cao bao nhiêu kilômét so với mặt đất? (Làm tròn đến chữ số thập phân thứ hai)."
                    + BR
                    + "2) \\textbf{(3,0 điểm)} Cho đường tròn $(O; R)$ và một điểm $A$ nằm ngoài đường tròn. "
                    "Từ $A$ vẽ hai tiếp tuyến $AB, AC$ với đường tròn $(O)$ ($B, C$ là các tiếp điểm)."
                    + BR
                    + "a) \\textbf{(1,0 điểm)} Chứng minh bốn điểm $A, B, O, C$ cùng thuộc một đường tròn."
                    + BR
                    + "b) \\textbf{(1,0 điểm)} Kẻ đường kính $BD$ của đường tròn $(O)$. Chứng minh $CD \\parallel OA$."
                    + BR
                    + "c) \\textbf{(1,0 điểm)} Kẻ $CK \\perp BD$ tại $K$. Chứng minh rằng $AC \\cdot CD = CK \\cdot AO$."
                ),
                "figure": {"tikz": TIKZ_MAYBAY, "caption": "Minh hoạ Bài IV.1"},
                "hinh_da": hinh_ct2_da(),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Gọi $AC$ là quãng đường máy bay đã bay ($AC = 12$ km), $BC$ là độ cao so với mặt đất ($BC \\perp AB$)."),
                        ("Góc cất cánh là $\\widehat{CAB} = 24^\\circ$."),
                        ("Xét tam giác $ABC$ vuông tại $B$, ta có: $BC = AC \\cdot \\sin \\widehat{CAB} = 12 \\cdot \\sin 24^\\circ$", 0.25),
                        ("$BC \\approx 12 \\cdot 0{,}4067 \\approx 4{,}88$ (km)."),
                        ("Vậy máy bay đạt độ cao khoảng $4{,}88$ km.", 0.25),
                    ]),
                    y("2a)", 1.0, [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Vì $AB$ là tiếp tuyến tại $B$ nên $AB \\perp OB \\Rightarrow \\widehat{ABO} = 90^\\circ$."),
                        ("Vì $AC$ là tiếp tuyến tại $C$ nên $AC \\perp OC \\Rightarrow \\widehat{ACO} = 90^\\circ$.", 0.25),
                        ("Xét tam giác $ABO$ vuông tại $B \\Rightarrow A, B, O$ thuộc đường tròn đường kính $AO$."),
                        ("Xét tam giác $ACO$ vuông tại $C \\Rightarrow A, C, O$ thuộc đường tròn đường kính $AO$.", 0.25),
                        ("Do đó bốn điểm $A, B, O, C$ cùng thuộc đường tròn đường kính $AO$.", 0.25),
                    ]),
                    y("2b)", 1.0, [
                        ("Ta có $AB = AC$ và $OB = OC = R$ nên $OA$ là đường trung trực của $BC$."),
                        ("Suy ra $OA \\perp BC$.", 0.25),
                        ("Mặt khác tam giác $BCD$ nội tiếp đường tròn $(O)$ có cạnh $BD$ là đường kính nên $\\widehat{BCD} = 90^\\circ$."),
                        ("Suy ra $CD \\perp BC$.", 0.25),
                        ("Vì $OA \\perp BC$ và $CD \\perp BC$ nên $CD \\parallel OA$ (điều phải chứng minh).", 0.5),
                    ]),
                    y("2c)", 1.0, [
                        ("Xét tam giác $CKD$ vuông tại $K$ và tam giác $ABO$ vuông tại $B$:"),
                        ("Có $\\widehat{CKD} = \\widehat{ABO} = 90^\\circ$.", 0.25),
                        ("Vì $CD \\parallel OA$ nên $\\widehat{CDK} = \\widehat{AOB}$ (hai góc so le trong).", 0.25),
                        ("Suy ra $\\triangle CKD \\backsim \\triangle ABO$ (g.g).", 0.25),
                        ("$\\Rightarrow \\dfrac{CK}{AB} = \\dfrac{CD}{AO} \\Rightarrow AB \\cdot CD = CK \\cdot AO$."),
                        ("Mà $AB = AC$ (tính chất hai tiếp tuyến cắt nhau). Do đó $AC \\cdot CD = CK \\cdot AO$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IVa", "Toán thực tế tỉ số lượng giác sin tính độ cao máy bay", "HH IV", "NB", 0.5, 5, "THCS Trưng Vương (2025–2026)"),
                    ("IVb1", "Bốn điểm cùng thuộc một đường tròn", "HH V", "TH", 1.0, 7, "THCS Chu Văn An (2025–2026)"),
                    ("IVb2", "Chứng minh quan hệ song song từ cùng vuông góc", "HH V", "TH", 1.0, 9, "THCS Chu Văn An (2025–2026)"),
                    ("IVb3", "Chứng minh hệ thức tích từ cặp tam giác đồng dạng so le trong", "HH V", "VD", 1.0, 12, "THCS Ba Đình (2025–2026)"),
                ],
                "note": "Học sinh chú ý chứng minh tam giác đồng dạng chi tiết từng góc.",
            },
            {
                "label": "Bài V.",
                "level": 4,
                "statement": (
                    "\\textbf{(0,5 điểm)} Cho ba số thực dương $x, y, z$ thoả mãn $x + y + z = 3$. "
                    "Tìm giá trị nhỏ nhất của biểu thức: "
                    + BR
                    + "$P = \\dfrac{x^2}{x + y} + \\dfrac{y^2}{y + z} + \\dfrac{z^2}{z + x}$."
                ),
                "dap_an": [
                    y("", 0.5, [
                        ("Áp dụng bất đẳng thức Bunhiacôpxki dạng phân thức (bất đẳng thức Cauchy-Schwarz):"),
                        ("Với $a, b, c > 0$ và $m, n, p > 0$ ta có: $\\dfrac{a^2}{m} + \\dfrac{b^2}{n} + \\dfrac{c^2}{p} \\ge \\dfrac{(a+b+c)^2}{m+n+p}$."),
                        ("Áp dụng cho ba phân thức của $P$:"),
                        ("$P = \\dfrac{x^2}{x + y} + \\dfrac{y^2}{y + z} + \\dfrac{z^2}{z + x} \\ge \\dfrac{(x + y + z)^2}{(x + y) + (y + z) + (z + x)}$", 0.25),
                        ("$P \\ge \\dfrac{(x + y + z)^2}{2(x + y + z)} = \\dfrac{x + y + z}{2}$."),
                        ("Thay $x + y + z = 3$ vào ta được: $P \\ge \\dfrac{3}{2}$."),
                        ("Dấu bằng xảy ra khi $\\dfrac{x}{x+y} = \\dfrac{y}{y+z} = \\dfrac{z}{z+x}$ và $x + y + z = 3 \\Rightarrow x = y = z = 1$."),
                        ("Vậy giá trị nhỏ nhất của biểu thức $P$ là $\\dfrac{3}{2}$ khi $x = y = z = 1$.", 0.25),
                    ])
                ],
                "mt": [("V", "Bất đẳng thức Cauchy-Schwarz dạng phân thức (BĐT Sơ-vác)", "ĐS II", "VDC", 0.5, 7, "THCS Thái Thịnh (2025–2026)")],
                "note": "Học sinh có thể dùng bất đẳng thức Cô-si ngược dấu: $\\dfrac{x^2}{x+y} = x - \\dfrac{xy}{x+y} \\ge x - \\dfrac{xy}{2\\sqrt{xy}} = x - \\dfrac{\\sqrt{xy}}{2}$.",
            },
        ],
        "bay": [
            ("Bài I.3", "BPT tìm nghiệm nguyên (BẪY SÓT NGHIỆM)", "Giải ra $0 \\le x \\le 1$ nhưng chỉ kết luận $x = 1$, quên mất $x = 0$ (mất điểm).", "Số nguyên $x$ thoả mãn $0 \\le x \\le 1$ là $x \\in \\{0; 1\\}$. Số $0$ là số nguyên không âm hợp lệ."),
            ("Bài II", "Toán năng suất làm chung làm riêng", "Đặt điều kiện $x, y > 0$ thay vì $x, y > 12$.", "Thời gian một mình làm xong phải lớn hơn thời gian làm chung: $x, y > 12$."),
            ("Bài III.3", "Chia số âm đổi chiều BPT", "Chia cả hai vế cho $-2$ quên đổi chiều: $-2x < -6 \\Rightarrow x < 3$ (sai kết quả).", "Quy tắc: chia cả hai vế cho số âm phải ĐỔI CHIỀU bất phương trình: $-2x < -6 \\Rightarrow x > 3$."),
            ("Bài IV.1", "Độ cao máy bay cất cánh", "Nhầm $12$ km là quãng đường hình chiếu nằm ngang, dùng $\\tan 24^\\circ$.", "Máy bay bay theo đường nghiêng nên $12$ km là cạnh huyền, dùng $\\sin 24^\\circ = \\text{đối}/\\text{huyền}$."),
            ("Bài V", "Bất đẳng thức Cauchy-Schwarz phân thức", "Không chỉ ra điều kiện số dương của mẫu thức trước khi áp dụng.", "Nêu rõ $x+y > 0, y+z > 0, z+x > 0$ và kiểm tra dấu bằng xảy ra $x = y = z = 1$."),
        ],
    },
    "ct3": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-chinh-thuc-so-3",
        "slug_mt": "ma-tran-va-dap-an-ck1-chinh-thuc-so-3",
        "eyebrow": "LỚP 9 • ĐỀ CHÍNH THỨC SỐ 3",
        "bai": [
            {
                "label": "Bài I.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Cho hai biểu thức: "
                    + BR
                    + "$A = \\dfrac{\\sqrt{x}}{\\sqrt{x}-3}$ và $B = \\dfrac{x-3}{x-9} - \\dfrac{1}{3-\\sqrt{x}}$ với $x > 0; x \\ne 9$."
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Tính giá trị của biểu thức $A$ khi $x = 16$."
                    + BR
                    + "2) \\textbf{(1,0 điểm)} Chứng minh $B = \\dfrac{\\sqrt{x}(\\sqrt{x}+1)}{x-9}$."
                    + BR
                    + "3) \\textbf{(0,5 điểm)} Cho $P = \\dfrac{B}{A}$. So sánh $P$ với $\\sqrt{P}$."
                ),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Thay $x = 16$ (thoả mãn ĐKXĐ) vào biểu thức $A$:"),
                        ("$A = \\dfrac{\\sqrt{16}}{\\sqrt{16}-3} = \\dfrac{4}{4-3} = 4$", 0.25),
                        ("Vậy khi $x = 16$ thì $A = 4$.", 0.25),
                    ]),
                    y("2)", 1.0, [
                        ("Với $x > 0; x \\ne 9$, ta có: $3 - \\sqrt{x} = -(\\sqrt{x}-3)$."),
                        ("Do đó: $B = \\dfrac{x-3}{(\\sqrt{x}-3)(\\sqrt{x}+3)} + \\dfrac{1}{\\sqrt{x}-3}$", 0.25),
                        ("$B = \\dfrac{x - 3 + (\\sqrt{x}+3)}{(\\sqrt{x}-3)(\\sqrt{x}+3)}$", 0.25),
                        ("$B = \\dfrac{x + \\sqrt{x}}{(\\sqrt{x}-3)(\\sqrt{x}+3)} = \\dfrac{\\sqrt{x}(\\sqrt{x}+1)}{x-9}$", 0.25),
                        ("Vậy $B = \\dfrac{\\sqrt{x}(\\sqrt{x}+1)}{x-9}$ (điều phải chứng minh).", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("Ta có: $P = \\dfrac{B}{A} = \\dfrac{\\sqrt{x}(\\sqrt{x}+1)}{(\\sqrt{x}-3)(\\sqrt{x}+3)} : \\dfrac{\\sqrt{x}}{\\sqrt{x}-3} = \\dfrac{\\sqrt{x}+1}{\\sqrt{x}+3}$"),
                        ("Vì $x > 0$ nên $\\sqrt{x}+1 > 0$ và $\\sqrt{x}+3 > 0$, suy ra $P > 0$."),
                        ("Xét hiệu: $P - 1 = \\dfrac{\\sqrt{x}+1 - (\\sqrt{x}+3)}{\\sqrt{x}+3} = \\dfrac{-2}{\\sqrt{x}+3} < 0 \\Rightarrow P < 1$."),
                        ("Do đó $0 < P < 1$.", 0.25),
                        ("Xét hiệu: $P - \\sqrt{P} = \\sqrt{P}(\\sqrt{P} - 1)$."),
                        ("Vì $0 < P < 1$ nên $0 < \\sqrt{P} < 1 \\Rightarrow \\sqrt{P} - 1 < 0$."),
                        ("Suy ra $P - \\sqrt{P} < 0 \\Rightarrow P < \\sqrt{P}$ (hay $\\sqrt{P} > P$).", 0.25),
                    ]),
                ],
                "mt": [
                    ("Ia", "Tính giá trị phân thức căn bậc hai tại $x = 16$", "ĐS III", "NB", 0.5, 4, "THCS Ngọc Lâm (2025–2026)"),
                    ("Ib", "Rút gọn biểu thức có bẫy đổi dấu mẫu $3 - \\sqrt{x}$", "ĐS III", "TH", 1.0, 9, "THCS Ngọc Lâm (2025–2026)"),
                    ("Ic", "So sánh $P$ với $\\sqrt{P}$ qua xét khoảng giá trị $0 < P < 1$", "ĐS III", "VD", 0.5, 6, "THCS Ngọc Lâm (2025–2026)"),
                ],
                "note": "Bẫy đổi dấu: $3-\\sqrt{x} = -(\\sqrt{x}-3)$ có dấu trừ phía trước thành $+$. Bẫy so sánh: vì $0 < P < 1$ nên $\\sqrt{P} > P$.",
            },
            {
                "label": "Bài II.",
                "level": 3,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình:"
                    + BR
                    + "Một cửa hàng điện máy bán hai mặt hàng là quạt điện và nồi cơm điện với tổng giá niêm yết là $1\,500\,000$ đồng. "
                    "Nhân dịp tri ân khách hàng, cửa hàng giảm giá $10\\%$ cho quạt điện và giảm giá $15\\%$ cho nồi cơm điện. "
                    "Bác An mua một chiếc quạt điện và một chiếc nồi cơm điện trong dịp này nên chỉ phải trả tổng cộng $1\,320\,000$ đồng. "
                    "Tính giá niêm yết của mỗi chiếc quạt điện và mỗi chiếc nồi cơm điện."
                ),
                "dap_an": [
                    y("", 2.0, [
                        ("Gọi giá niêm yết của một chiếc quạt điện là $x$ (đồng), của nồi cơm điện là $y$ (đồng).", 0.25),
                        ("Điều kiện: $0 < x, y < 1\,500\,000$."),
                        ("Tổng giá niêm yết của hai mặt hàng là $1\,500\,000$ đồng nên ta có phương trình: $x + y = 1\,500\,000$ (1)", 0.5),
                        ("Giá quạt sau giảm là $0{,}9x$ (đồng), giá nồi cơm sau giảm là $0{,}85y$ (đồng)."),
                        ("Tổng số tiền bác An phải trả là $1\,320\,000$ đồng nên ta có phương trình: $0{,}9x + 0{,}85y = 1\,320\,000$ (2)", 0.5),
                        ("Từ (1) suy ra: $y = 1\,500\,000 - x$. Thế vào (2):"),
                        ("$0{,}9x + 0{,}85(1\,500\,000 - x) = 1\,320\,000$"),
                        ("$0{,}05x + 1\,275\,000 = 1\,320\,000 \\Rightarrow 0{,}05x = 45\,000 \\Rightarrow x = 900\,000$ (thoả mãn).", 0.5),
                        ("Thay $x = 900\,000$ vào tìm được: $y = 600\,000$ (thoả mãn)."),
                        ("Vậy giá niêm yết của quạt điện là $900\,000$ đồng, của nồi cơm điện là $600\,000$ đồng.", 0.25),
                    ])
                ],
                "mt": [("II", "Toán kinh tế mua sắm giảm giá phần trăm (lập hệ phương trình bậc nhất hai ẩn)", "ĐS I", "TH", 2.0, 15, "THCS Cầu Diễn (2025–2026)")],
                "note": "Học sinh nhớ kết luận kèm đơn vị đồng và tên mặt hàng rõ ràng.",
            },
            {
                "label": "Bài III.",
                "level": 2,
                "statement": (
                    "\\textbf{(2,0 điểm)} Giải các phương trình, bất phương trình và hệ phương trình sau:"
                    + BR
                    + "1) \\textbf{(0,75 điểm)} $\\begin{cases} \\dfrac{1}{x-1} + \\dfrac{2}{y+1} = 5 \\\\ \\dfrac{3}{x-1} - \\dfrac{1}{y+1} = 1 \\end{cases}$"
                    + BR
                    + "2) \\textbf{(0,75 điểm)} $\\dfrac{x+2}{x-2} - \\dfrac{1}{x} = \\dfrac{2}{x(x-2)}$"
                    + BR
                    + "3) \\textbf{(0,5 điểm)} $\\dfrac{3x+5}{2} - 1 \\ge x + 2$"
                ),
                "dap_an": [
                    y("1)", 0.75, [
                        ("ĐKXĐ: $x \\ne 1$ và $y \\ne -1$."),
                        ("Đặt $u = \\dfrac{1}{x-1}$ và $v = \\dfrac{1}{y+1}$."),
                        ("Hệ trở thành: $\\begin{cases} u + 2v = 5 \\\\ 3u - v = 1 \\end{cases}$", 0.25),
                        ("Nhân phương trình hai với $2$: $6u - 2v = 2$. Cộng từng vế: $7u = 7 \\Rightarrow u = 1$."),
                        ("Thay vào tìm được $v = 2$.", 0.25),
                        ("Suy ra: $\\dfrac{1}{x-1} = 1 \\Rightarrow x = 2$ (TM); $\\dfrac{1}{y+1} = 2 \\Rightarrow y = -\\dfrac{1}{2}$ (TM)."),
                        ("Vậy hệ phương trình có nghiệm duy nhất $(x; y) = \\left(2; -\\dfrac{1}{2}\\right)$.", 0.25),
                    ]),
                    y("2)", 0.75, [
                        ("ĐKXĐ: $x \\ne 0$ và $x \\ne 2$."),
                        ("Quy đồng khử mẫu: $x(x+2) - (x-2) = 2$", 0.25),
                        ("$x^2 + 2x - x + 2 = 2 \\Rightarrow x^2 + x = 0$"),
                        ("$x(x+1) = 0 \\Rightarrow x = 0$ hoặc $x = -1$."),
                        ("Đối chiếu ĐKXĐ: $x = 0$ loại; $x = -1$ thoả mãn.", 0.25),
                        ("Vậy nghiệm của phương trình là $x = -1$.", 0.25),
                    ]),
                    y("3)", 0.5, [
                        ("$\\dfrac{3x+5}{2} \\ge x + 3$"),
                        ("$3x + 5 \\ge 2(x + 3)$", 0.25),
                        ("$3x + 5 \\ge 2x + 6 \\Rightarrow x \\ge 1$"),
                        ("Vậy nghiệm của bất phương trình là $x \\ge 1$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IIIa", "Giải hệ phương trình bằng cách đặt ẩn phụ", "ĐS I", "TH", 0.75, 7, "THCS Phương Hà Đông (2025–2026)"),
                    ("IIIb", "Giải phương trình chứa ẩn ở mẫu có bẫy ĐKXĐ", "ĐS I", "TH", 0.75, 8, "THCS Tân Triều (2025–2026)"),
                    ("IIIc", "Giải bất phương trình bậc nhất một ẩn", "ĐS II", "NB", 0.5, 4, "THCS Đống Đa (2025–2026)"),
                ],
                "note": "Ý b: $x = 0$ vi phạm ĐKXĐ nên phải loại, không kết luận phương trình có 2 nghiệm.",
            },
            {
                "label": "Bài IV.",
                "level": 3,
                "statement": (
                    "\\textbf{(3,5 điểm)} "
                    + BR
                    + "1) \\textbf{(0,5 điểm)} Một ngọn hải đăng cao $45$ m so với mặt nước biển. "
                    "Từ đỉnh ngọn hải đăng, một người quan sát nhìn thấy một con thuyền đang neo đậu trên biển dưới một góc hạ $28^\\circ$. "
                    "Tính khoảng cách từ chân ngọn hải đăng đến con thuyền (kết quả làm tròn đến mét)."
                    + BR
                    + "2) \\textbf{(3,0 điểm)} Cho đường tròn $(O; R)$ và dây cung $BC$ không đi qua tâm. "
                    "Hai tiếp tuyến của $(O)$ tại $B$ và $C$ cắt nhau tại điểm $A$. Kẻ đường kính $CD$ của đường tròn $(O)$."
                    + BR
                    + "a) \\textbf{(1,0 điểm)} Chứng minh bốn điểm $A, B, O, C$ cùng thuộc một đường tròn."
                    + BR
                    + "b) \\textbf{(1,0 điểm)} Chứng minh $OA \\perp BC$ và $BD \\parallel OA$."
                    + BR
                    + "c) \\textbf{(1,0 điểm)} Đoạn thẳng $OA$ cắt đường tròn $(O)$ tại $E$. "
                    "Gọi $M$ là giao điểm của $CE$ và $AB$. Chứng minh rằng $M$ là trung điểm của đoạn thẳng $AB$."
                ),
                "figure": {"tikz": TIKZ_HAIDANG, "caption": "Minh hoạ Bài IV.1"},
                "hinh_da": hinh_ct3_da(),
                "dap_an": [
                    y("1)", 0.5, [
                        ("Gọi $AB$ là chiều cao ngọn hải đăng ($AB \\perp BC$ tại chân tháp $B$, $AB = 45$ m)."),
                        ("Góc hạ bằng góc nâng: $\\widehat{ACB} = 28^\\circ$ (hai góc so le trong)."),
                        ("Xét tam giác $ABC$ vuông tại $B$: $BC = \\dfrac{AB}{\\tan \\widehat{ACB}} = \\dfrac{45}{\\tan 28^\\circ}$", 0.25),
                        ("$BC \\approx \\dfrac{45}{0{,}5317} \\approx 85$ (m)."),
                        ("Vậy khoảng cách từ chân ngọn hải đăng đến con thuyền khoảng $85$ mét.", 0.25),
                    ]),
                    y("2a)", 1.0, [
                        ("Vẽ hình đúng đến câu a.", 0.25),
                        ("Vì $AB$ là tiếp tuyến tại $B$ nên $AB \\perp OB \\Rightarrow \\widehat{ABO} = 90^\\circ$."),
                        ("Vì $AC$ là tiếp tuyến tại $C$ nên $AC \\perp OC \\Rightarrow \\widehat{ACO} = 90^\\circ$.", 0.25),
                        ("Xét tam giác $ABO$ vuông tại $B \\Rightarrow A, B, O$ cùng thuộc đường tròn đường kính $AO$."),
                        ("Xét tam giác $ACO$ vuông tại $C \\Rightarrow A, C, O$ cùng thuộc đường tròn đường kính $AO$.", 0.25),
                        ("Do đó bốn điểm $A, B, O, C$ cùng thuộc đường tròn đường kính $AO$.", 0.25),
                    ]),
                    y("2b)", 1.0, [
                        ("Ta có $AB = AC$ và $OB = OC = R$ nên $OA$ là đường trung trực của $BC$."),
                        ("Suy ra $OA \\perp BC$.", 0.25),
                        ("Mặt khác tam giác $BCD$ nội tiếp đường tròn $(O)$ có cạnh $CD$ là đường kính nên $\\widehat{CBD} = 90^\\circ$."),
                        ("Suy ra $BD \\perp BC$.", 0.25),
                        ("Vì $OA \\perp BC$ và $BD \\perp BC$ nên $BD \\parallel OA$ (điều phải chứng minh).", 0.5),
                    ]),
                    y("2c)", 1.0, [
                        ("Ta có $OA$ là phân giác của $\\widehat{BOC}$, mà $\\triangle OBC$ cân tại $O$ nên $OE$ là tia phân giác góc ở đỉnh."),
                        ("Suy ra $E$ là điểm chính giữa của cung nhỏ $BC \\Rightarrow \\widehat{BCE} = \\widehat{ACE}$."),
                        ("Do đó $CE$ là tia phân giác trong của góc $\\widehat{ACB}$ trong $\\triangle ABC$.", 0.25),
                        ("Xét $\\triangle AME$ và $\\triangle ACM$ có góc $A$ chung và $\\widehat{AME} = \\widehat{ACM}$ $\\Rightarrow \\triangle AME \\backsim \\triangle ACM$ (g.g).", 0.25),
                        ("Chứng minh được $MA^2 = ME \\cdot MC$ và $MB^2 = ME \\cdot MC$.", 0.25),
                        ("Suy ra $MA^2 = MB^2 \\Rightarrow MA = MB$. Vậy $M$ là trung điểm của $AB$.", 0.25),
                    ]),
                ],
                "mt": [
                    ("IVa", "Toán thực tế góc hạ góc nâng tính khoảng cách tàu thuyền", "HH IV", "NB", 0.5, 5, "THCS Tân Triều (2025–2026)"),
                    ("IVb1", "Bốn điểm cùng thuộc một đường tròn", "HH V", "TH", 1.0, 7, "THCS Ngọc Thụy (2025–2026)"),
                    ("IVb2", "Chứng minh quan hệ song song qua đường kính vuông góc", "HH V", "TH", 1.0, 9, "THCS Ngọc Thụy (2025–2026)"),
                    ("IVb3", "Chứng minh trung điểm tiếp tuyến qua góc tạo bởi tiếp tuyến và dây cung", "HH V", "VD", 1.0, 12, "THCS Lý Thánh Tông (2025–2026)"),
                ],
                "note": "Câu c là câu hỏi phân loại hình học xuất hiện thường xuyên trong đề thi vào 10.",
            },
            {
                "label": "Bài V.",
                "level": 4,
                "statement": (
                    "\\textbf{(0,5 điểm)} Một cơ sở sản xuất cần làm một bồn chứa nước hình hộp chữ nhật không có nắp đậy với thể tích $32\\text{ m}^3$, "
                    "đáy là hình vuông cạnh $x$ (m). "
                    "Chi phí làm đáy là $150\\,000$ đồng/m$^2$ và chi phí làm bốn mặt xung quanh là $100\\,000$ đồng/m$^2$. "
                    "Tìm kích thước cạnh đáy $x$ để tổng chi phí làm bồn chứa nước là nhỏ nhất."
                ),
                "dap_an": [
                    y("", 0.5, [
                        ("Gọi chiều cao của bồn chứa nước là $h$ (m, $h > 0$)."),
                        ("Thể tích bồn nước là: $V = x^2 \\cdot h = 32 \\Rightarrow h = \\dfrac{32}{x^2}$ (m)."),
                        ("Diện tích đáy là $x^2$ ($m^2$), diện tích xung quanh là $4xh = 4x \\cdot \\dfrac{32}{x^2} = \\dfrac{128}{x}$ ($m^2$)."),
                        ("Tổng chi phí làm bồn nước (tính theo nghìn đồng) là:"),
                        ("$C = 150x^2 + 100 \\cdot \\dfrac{128}{x} = 150x^2 + \\dfrac{12800}{x}$", 0.25),
                        ("Áp dụng bất đẳng thức Cô-si cho ba số dương:"),
                        ("Dấu bằng xảy ra khi $x = 4$ m."),
                        ("Vậy cạnh đáy $x = 4$ mét thì chi phí làm bồn nước là nhỏ nhất.", 0.25),
                    ])
                ],
                "mt": [("V", "Toán thực tế tối ưu chi phí làm bồn nước (BĐT Cô-si)", "ĐS II", "VDC", 0.5, 7, "THCS Chu Văn An (2025–2026)")],
                "note": "Học sinh sử dụng bất đẳng thức Cô-si 3 số để triệt tiêu biến x.",
            },
        ],
        "bay": [
            ("Bài I.2", "Đổi dấu mẫu $3 - \\sqrt{x}$ có dấu trừ", "Đổi dấu mẫu nhưng quên đổi dấu trừ đằng trước phân thức thành dấu cộng.", "Quy tắc: $-\\dfrac{1}{3-\\sqrt{x}} = +\\dfrac{1}{\\sqrt{x}-3}$. Trừ trừ thành cộng."),
            ("Bài I.3", "So sánh $P$ với $\\sqrt{P}$ (BẪY SO SÁNH)", "Nhầm tưởng $\\sqrt{P} < P$ như các số lớn hơn $1$.", "Với $0 < P < 1$ thì luôn có $\\sqrt{P} > P$. Cần chứng minh $0 < P < 1$ trước."),
            ("Bài III.1", "Hệ phương trình đặt ẩn phụ", "Tìm ra $u = 1, v = 2$ quên bước giải ngược tìm lại $x, y$ (mất 0,25đ).", "Bắt buộc có bước thế ngược tìm lại nghiệm $(x; y)$ và đối chiếu ĐKXĐ."),
            ("Bài III.2", "BẪY NGOẠI LAI $x = 0$ TRÙNG ĐKXĐ", "Giải ra $x(x+1) = 0$ kết luận hai nghiệm $x = 0$ và $x = -1$ (bị trừ điểm).", "ĐKXĐ $x \\ne 0, x \\ne 2$. Nghiệm $x = 0$ vi phạm ĐKXĐ nên BỊ LOẠI! Chỉ có nghiệm $x = -1$."),
            ("Bài IV.1", "GÓC HẠ NGỌN HẢI ĐĂNG (BẪY HÌNH VẼ)", "Vẽ góc hạ $28^\\circ$ ở đỉnh hải đăng so với phương thẳng đứng của tháp.", "Góc hạ là góc so với PHƯƠNG NẰM NGANG, do đó góc nhìn từ thuyền lên đỉnh tháp bằng $28^\\circ$ (so le trong)."),
        ],
    },
}


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


TIEN_BO_CT = [
    (
        "Căn thức \\& câu phụ (2,0đ)",
        "Ia: Tính giá trị $x = 4-2\\sqrt{3}$; Ib: Rút gọn mẫu đối; Ic: Giải PT $P = 1/4$ (vô nghiệm)",
        "Ia: Tính giá trị $x = 25$; Ib: Rút gọn mẫu $x-4$; Ic: BPT $P \\le 1/2$ (nghiệm nguyên)",
        "Ia: Tính giá trị $x = 9$; Ib: Rút gọn mẫu $x-9$; Ic: Tìm $x$ nguyên để $P$ nhận giá trị nguyên",
    ),
    (
        "Toán thực tế lập hệ (2,0đ)",
        "Hai đội xe tải vận chuyển hàng (chuyển động thực tế)",
        "Năng suất máy may áo bảo hộ lao động (năng suất công việc)",
        "Hai xe máy và ô tô cùng khởi hành từ A đến B (chuyển động đuổi)",
    ),
    (
        "Giải PT, BPT, hệ (2,0đ)",
        "IIIa: Hệ cộng đại số; IIIb: PT ẩn ở mẫu; IIIc: BPT đổi chiều",
        "IIIa: Hệ ẩn phụ; IIIb: PT tích bậc 3; IIIc: BPT nghiệm nguyên lớn nhất",
        "IIIa: Hệ phương pháp thế; IIIb: PT quy về bậc hai; IIIc: BPT phân thức $\\le 0$",
    ),
    (
        "Lượng giác thực tế (0,5đ)",
        "Chiều cao cây cau bằng $\\tan 55^\\circ$ (bóng $6$ m)",
        "Độ cao máy bay bằng $\\sin 24^\\circ$ (quãng đường $12$ km)",
        "Góc dốc con đường leo núi bằng $\\sin 10^\\circ$ (độ cao $380$ m)",
    ),
    (
        "Hình học đường tròn (3,0đ)",
        "4 điểm đường tròn; $OM \\perp AC$; hệ thức tiếp tuyến $MC^2 = MH \\cdot MO$; trung điểm qua Thalès",
        "Tiếp tuyến $Ax, By$; $\\widehat{COD} = 90^\\circ$; tích $AC \\cdot BD = R^2$; tiếp tuyến thứ hai",
        "Tiếp tuyến cắt nhau; cát tuyến; tiếp tuyến vuông góc; 3 điểm thẳng hàng qua góc nội tiếp",
    ),
    (
        "Câu cuối tối ưu / VDC (0,5đ)",
        "Tối ưu hình học: gập tôn làm máng nước diện tích lớn nhất",
        "Bất đẳng thức đại số Cosi hai số dương: $P = a + b + 1/a + 1/b$",
        "Tìm GTNN biểu thức hai biến: $P = x^2 - 4xy + 5y^2 - 2y + 2026$",
    ),
]


def bang_tien_bo_ct():
    s = (
        "\\noindent\\textbf{BẢN ĐỒ DẠNG BÀI QUA 3 ĐỀ KIỂM TRA CHÍNH THỨC:} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{2.6cm}|p{4.0cm}|p{4.0cm}|p{4.0cm}|}\n\\hline\n"
        "\\textbf{Mạch kiến thức} & \\textbf{Đề chính thức 1} & \\textbf{Đề chính thức 2} & \\textbf{Đề chính thức 3} \\\\ \\hline\n"
    )
    for r in TIEN_BO_CT:
        s += " & ".join(r) + " \\\\ \\hline\n"
    s += "\\end{tabular}\\end{center}"
    return s


def bang_theo_doi_ct():
    s = (
        "\\noindent\\textbf{PHIẾU THEO DÕI ĐÁNH GIÁ NĂNG LỰC HỌC SINH:} [[br]] "
        "\\textit{\\footnotesize Đánh giá tổng thể qua 3 đề kiểm tra chuẩn hoá; đối chiếu với 3 đề ôn tập để xác định các lỗ hổng kiến thức cần bù đắp trước kì thi thật.} [[br]] \\par\\vspace{-6pt}\n"
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.3}\n"
        "\\begin{tabular}{|p{7.2cm}|c|c|c|c|}\n\\hline\n"
        "\\textbf{Bài (điểm tối đa)} & \\textbf{Đề CT 1} & \\textbf{Đề CT 2} & \\textbf{Đề CT 3} & \\textbf{Đạt chuẩn?} \\\\ \\hline\n"
    )
    for b in [
        "Bài I -- Căn thức và câu hỏi phụ (2,0đ)",
        "Bài II -- Toán thực tế lập hệ PT (2,0đ)",
        "Bài III -- Phương trình, BPT, Hệ PT (2,0đ)",
        "Bài IV -- Lượng giác \\& Hình đường tròn (3,5đ)",
        "Bài V -- Cực trị / Bất đẳng thức VDC (0,5đ)",
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
    tit = f"Đề kiểm tra cuối học kì I — Đề chính thức {k[-1]} (90 phút)"
    return dict(slug=D["slug_de"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 9", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


def mt_json(k, D):
    stages = []
    rows = [r for b in D["bai"] for r in b["mt"]]
    s_mt, tong_d, tong_p = bang_mt(rows)
    s_muc, tot = bang_muc(rows)
    so = k[-1]

    # Stage 1: Ma trận đề thi + Bảng bẫy tử huyệt
    q_dict = {}
    for b in D["bai"]:
        for r in b["mt"]:
            q_dict[QUAN[r[6]]] = q_dict.get(QUAN[r[6]], 0.0) + r[4]
    str_nguon = ", ".join(f"{q} ({d(v)}đ - {round(v*10)}\\%)" for q, v in sorted(q_dict.items(), key=lambda t: -t[1]))

    b1 = [
        dict(
            type="para",
            text=f"\\textbf{{MA TRẬN ĐỀ KIỂM TRA CUỐI HỌC KÌ I -- ĐỀ CHÍNH THỨC SỐ {so} (90 PHÚT)}}"
            + BR
            + "Thời gian làm bài: $90$ phút. Hình thức: Tự luận $100\\%$. Đề bám sát cấu trúc tuyển sinh lớp 10 của Sở GD\\&ĐT Hà Nội."
            + BR
            + f"\\textbf{{Cơ cấu nguồn đề ({len(q_dict)} quận/huyện):}} {str_nguon} (đạt chuẩn $\\le 40\\%$ điểm/quận)."
            + BR
            + s_mt,
        ),
        dict(type="para", text=s_muc),
        dict(type="para", text=bang_bay(D["bay"])),
        dict(
            type="para",
            text="\\textbf{QUY TẮC CHẤM THI CHÍNH THỨC:}"
            + BR
            + "1. Điểm toàn bài làm tròn đến $0{,}25$ điểm. Học sinh giải theo cách khác đúng vẫn cho điểm tối đa tương ứng."
            + BR
            + "2. Với Bài hình học: Học sinh vẽ sai hình hoặc không vẽ hình thì không chấm điểm."
            + BR
            + "3. Mỗi bước biến đổi viết trên một dòng riêng biệt, có điểm thành phần chi tiết tương ứng.",
        ),
    ]
    stages.append(dict(kind="review", number=1, title=f"Ma trận Đề chính thức số {so}", blocks=b1))

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
            blocks.append(
                dict(
                    type="para",
                    text="\\textbf{ĐẶC TẢ TỔNG KẾT NĂNG LỰC}"
                    + BR
                    + f"• Tỉ lệ cấp độ: Nhận biết ${round(tot['NB']*10)}\\%$ (${d(tot['NB'])}đ) -- Thông hiểu ${round(tot['TH']*10)}\\%$ (${d(tot['TH'])}đ) -- Vận dụng ${round(tot['VD']*10)}\\%$ (${d(tot['VD'])}đ) -- Vận dụng cao ${round(tot['VDC']*10)}\\%$ (${d(tot['VDC'])}đ)."
                    + BR
                    + "• Đề chính thức đo lường chính xác mức độ sẵn sàng của học sinh cho kì thi tuyển sinh vào 10.",
                )
            )
            blocks.append(dict(type="para", text=bang_tien_bo_ct()))
            blocks.append(dict(type="para", text=bang_theo_doi_ct()))
        stages.append(dict(kind=KIND[j - 1], number=j, title=ti, blocks=blocks))

    tit = f"Ma trận đề và đáp án chi tiết — Đề chính thức {so}"
    return dict(slug=D["slug_mt"], title=tit, eyebrow=D["eyebrow"], grade_label="Lớp 9", class_tier="", theme="de_thi", trinh_bay="thoang", stages=stages)


def main():
    NGUON, NGUON_BO = kiem_nguon()
    print("✓ Kiểm tra rải nguồn 3 Đề Chính thức thành công:")
    for _k, (_n, _q) in NGUON.items():
        print(f"  [{_k}] {_n} trường, {len(_q)} quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(_q.items(), key=lambda t: -t[1])))
    print("  Tổng cả bộ theo quận: " + ", ".join(f"{a} {d(v)}đ" for a, v in sorted(NGUON_BO.items(), key=lambda t: -t[1])))

    print("Bắt đầu sinh 3 Đề Kiểm tra Cuối Kì 1 Chính thức...")
    for k, D in DE_CT.items():
        de = de_json(k, D)
        mt = mt_json(k, D)
        p_de = OUT / f"{de['slug']}.json"
        p_mt = OUT / f"{mt['slug']}.json"
        p_de.write_text(json.dumps(de, ensure_ascii=False, indent=1), encoding="utf-8")
        p_mt.write_text(json.dumps(mt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → Đã sinh: {p_de.name} và {p_mt.name}")
    print("Hoàn tất sinh 3 đề chính thức CK1 lớp 9.")


if __name__ == "__main__":
    main()
