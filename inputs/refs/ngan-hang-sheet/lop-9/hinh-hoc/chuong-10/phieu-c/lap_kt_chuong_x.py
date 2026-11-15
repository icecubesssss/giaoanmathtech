"""Đề kiểm tra chương X lớp 9C (45′) — dựng 12/11/2026 cùng phiếu C (Thầy: "làm luôn đề KT").

Ghi 3 file: de-kiem-tra.json (ma trận DeSpec) + kiem-tra-chuong/{tờ đề, ma trận–đáp án} (theme de_thi).
Không trùng đề nào của phiếu A, phiếu C. Chạy từ gốc repo.
"""
from __future__ import annotations

import json
from math import isclose
from pathlib import Path

DIR = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien")
KT = DIR / "kiem-tra-chuong"
KT.mkdir(exist_ok=True)
PI = 3.14

# ── kiểm đáp số ──────────────────────────────────────────────────────────────
assert 2 * 4 * 6 == 48 and 3**2 * 5 == 45                       # C1, C2 (π)
assert (13**2 - 12**2) == 25 and 5 * 13 == 65                   # C3
assert isclose(4 / 3 * 27, 36) and 2500 == 2.5 * 1000          # C4, C5
assert 4 * 12**2 == 576                                         # C6
assert (26**2 - 10**2) == 24**2                                 # C7 h = 24
assert isclose(PI * 260, 816.4) and isclose(PI * 100 * 24 / 3, 2512)
assert isclose(PI * 9 * 11.7, 330.642) and isclose(5 * 330.642, 1653.21)     # C8
assert isclose(PI * 9 * 15, 423.9) and isclose(PI * 9 * 2, 56.52)           # C9
R3 = 18 * 3 / 4
assert isclose(R3, 13.5) and abs(R3 ** (1 / 3) - 2.381) < 1e-3

HEAD = "\\begin{tikzpicture}[line width=0.8pt, font=\\small]\n"
TAIL = "\\end{tikzpicture}"


def tru(rx, h, nuoc=None, top=None, right=None, left=None, bi=False):
    ry = round(0.32 * rx, 3)
    s = ""
    if nuoc is not None:
        s += (f"  \\fill[info!25] (-{rx},{nuoc}) -- (-{rx},0) arc (180:360:{rx} and {ry}) -- ({rx},{nuoc}) "
              f"arc (0:180:{rx} and {ry}) -- cycle;\n  \\draw[ink] (0,{nuoc}) ellipse ({rx} and {ry});\n")
    s += (f"  \\draw[ink] (0,{h}) ellipse ({rx} and {ry});\n  \\draw[ink] (-{rx},0) arc (180:360:{rx} and {ry});\n"
          f"  \\draw[ink, dashed] (-{rx},0) arc (180:0:{rx} and {ry});\n"
          f"  \\draw[ink] (-{rx},0) -- (-{rx},{h});\n  \\draw[ink] ({rx},0) -- ({rx},{h});\n")
    if top:
        s += (f"  \\draw[ink, <->] (-{rx},{h}) -- ({rx},{h});\n"
              f"  \\node[anchor=center, font=\\scriptsize, fill=white, inner sep=1pt] at (0,{h}) {{{top}}};\n")
    if right:
        s += (f"  \\draw[ink, <->] ({rx + 0.3},0) -- ({rx + 0.3},{h});\n"
              f"  \\node[right, font=\\scriptsize] at ({rx + 0.35},{h / 2}) {{{right}}};\n")
    if left and nuoc is not None:
        s += (f"  \\draw[ink, <->] (-{rx + 0.3},{nuoc - 0.45}) -- (-{rx + 0.3},{nuoc});\n"
              f"  \\node[left, font=\\scriptsize] at (-{rx + 0.35},{nuoc - 0.22}) {{{left}}};\n")
    if bi:
        s += "  \\draw[ink, fill=gold!40] (0,0.3) circle (0.3);\n"
    return s


hinh_non = (HEAD + "  \\draw[ink] (0,0) ellipse (1.0 and 0.32);\n  \\draw[ink] (-1.0,0) -- (0,2.3) -- (1.0,0);\n"
            "  \\draw[ink, dashed] (0,0) -- (0,2.3);\n  \\draw[ink, <->] (-1.0,0) -- (1.0,0);\n"
            "  \\node[below, font=\\scriptsize] at (0,-0.34) {$20$ cm};\n"
            "  \\node[right, font=\\scriptsize] at (0.55,1.2) {$26$ cm};\n" + TAIL)
hinh_lon = HEAD + tru(0.7, 2.0, top="$6$ cm", right="$11{,}7$ cm") + TAIL
hinh_coc = HEAD + tru(0.9, 2.4, nuoc=1.55, top="$6$ cm", right="$15$ cm", left="$2$ cm", bi=True) + TAIL


def fig(t, cap, w="0.22"):
    return {"type": "tikz", "tikz": t, "pos": "right", "width": w, "caption": cap}


def p(label, level, dang, stmt, **kw):
    b = {"type": "problem", "label": label, "level": level, "tier": "onclass", "dang_id": dang, "statement": stmt}
    b.update(kw)
    return b


TN = [
    p("Câu 1.", 1, "NB1", "Hình trụ có bán kính đáy $4$ cm, chiều cao $6$ cm. Diện tích xung quanh của hình trụ là:",
      options=["$24\\pi$ cm$^2$", "$48\\pi$ cm$^2$", "$96\\pi$ cm$^2$", "$192\\pi$ cm$^2$"]),
    p("Câu 2.", 1, "NB1", "Hình trụ có bán kính đáy $3$ cm, chiều cao $5$ cm. Thể tích của hình trụ là:",
      options=["$15\\pi$ cm$^3$", "$30\\pi$ cm$^3$", "$45\\pi$ cm$^3$", "$75\\pi$ cm$^3$"]),
    p("Câu 3.", 1, "NB1", "Hình nón có độ dài đường sinh $13$ cm và chiều cao $12$ cm. Diện tích xung quanh của hình nón là:",
      options=["$60\\pi$ cm$^2$", "$65\\pi$ cm$^2$", "$156\\pi$ cm$^2$", "$25\\pi$ cm$^2$"]),
    p("Câu 4.", 1, "NB1", "Thể tích của hình cầu có bán kính $3$ cm là:",
      options=["$12\\pi$ cm$^3$", "$27\\pi$ cm$^3$", "$36\\pi$ cm$^3$", "$108\\pi$ cm$^3$"]),
    p("Câu 5.", 1, "NB1", "$2{,}5$ m$^3$ bằng bao nhiêu lít?",
      options=["$25$ lít", "$250$ lít", "$2500$ lít", "$25\\,000$ lít"]),
    p("Câu 6.", 1, "NB1", "Quả bóng rổ có dạng hình cầu với đường kính $24$ cm. Diện tích bề mặt quả bóng là:",
      options=["$144\\pi$ cm$^2$", "$576\\pi$ cm$^2$", "$2304\\pi$ cm$^2$", "$288\\pi$ cm$^2$"]),
]
C7 = p("Câu 7.", 2, "TH1",
       "\\textbf{(2,0 điểm)} Một chiếc mũ sinh nhật dạng hình nón có đường kính đáy là $20$ cm, độ dài đường sinh là $26$ cm (Hình 1). Lấy $\\pi \\approx 3{,}14$.[[br]]a) \\textbf{(1,0 điểm)} Tính diện tích xung quanh của chiếc mũ.[[br]]b) \\textbf{(1,0 điểm)} Tính thể tích của chiếc mũ.",
       figure=fig(hinh_non, "Hình 1", "0.13"))
C8 = p("Câu 8.", 2, "TH2",
       "\\textbf{(2,0 điểm)} Một lon nước ngọt hình trụ có chiều cao là $11{,}7$ cm, đường kính đáy bằng $6$ cm (Hình 2). Lấy $\\pi \\approx 3{,}14$.[[br]]a) \\textbf{(1,0 điểm)} Tính thể tích của một lon nước ngọt (làm tròn kết quả đến hàng phần trăm).[[br]]b) \\textbf{(1,0 điểm)} Hỏi $5$ lon nước ngọt như vậy có đổ đầy một chai có thể tích $1{,}5$ lít không? (Biết $1$ lít $= 1000$ cm$^3$.)",
       figure=fig(hinh_lon, "Hình 2", "0.13"))
C9 = p("Câu 9.", 3, "VD1",
       "\\textbf{(3,0 điểm)} Một cốc nước thủy tinh hình trụ có đường kính đáy $6$ cm, chiều cao $15$ cm, đang đựng một lượng nước. Lấy $\\pi \\approx 3{,}14$.[[br]]a) \\textbf{(1,0 điểm)} Tính thể tích của cốc thủy tinh.[[br]]b) \\textbf{(2,0 điểm)} Người ta thả một viên bi thủy tinh dạng hình cầu vào cốc nước, viên bi chìm hoàn toàn xuống đáy cốc làm cột nước dâng cao thêm $2$ cm và nước không tràn ra ngoài (Hình 3). Tính bán kính của viên bi (làm tròn đến chữ số thập phân thứ hai).",
       figure=fig(hinh_coc, "Hình 3", "0.17"))

de = {
    "slug": "de-kiem-tra-chuong-x-lop-9c",
    "title": "Đề kiểm tra Chương X — Một số hình khối trong thực tiễn (45 phút)",
    "eyebrow": "LỚP 9C • KIỂM TRA CHƯƠNG X",
    "grade_label": "Lớp 9 • Hình học",
    "class_tier": "C",
    "theme": "de_thi",
    "stages": [
        {"kind": "review", "number": 1, "title": "", "blocks": [
            {"type": "para", "text": "\\textbf{PHẦN I. TRẮC NGHIỆM (3,0 điểm).} \\textit{Mỗi câu 0,5 điểm. Chọn phương án đúng.}"}] + TN},
        {"kind": "concept", "number": 2, "title": "", "blocks": [
            {"type": "para", "text": "\\textbf{PHẦN II. TỰ LUẬN (7,0 điểm).}"}, C7]},
        {"kind": "practice1", "number": 3, "title": "", "blocks": [C8]},
        {"kind": "practice2", "number": 4, "title": "", "blocks": [C9]},
        {"kind": "reflection", "number": 5, "title": "", "blocks": [
            {"type": "para", "text": "\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}"}]},
    ],
}

# ── ma trận + đáp án ─────────────────────────────────────────────────────────
ROWS = [  # (câu, nội dung, mức, điểm, phút, hình thức, đáp án ngắn)
    ("Câu 1", "Diện tích xung quanh hình trụ $r = 4$ cm, $h = 6$ cm (SGK bài 10.1)", "NB", 0.5, 2, "trắc nghiệm", "B. $48\\pi$ cm$^2$"),
    ("Câu 2", "Thể tích hình trụ $r = 3$ cm, $h = 5$ cm (SGK bài 10.1)", "NB", 0.5, 2, "trắc nghiệm", "C. $45\\pi$ cm$^3$"),
    ("Câu 3", "Diện tích xung quanh hình nón $l = 13$ cm, $h = 12$ cm: tìm $r$ bằng Pythagore (SGK Luyện tập 4 Bài 31)", "TH", 0.5, 2, "trắc nghiệm", "B. $65\\pi$ cm$^2$"),
    ("Câu 4", "Thể tích hình cầu bán kính $3$ cm (SGK, bảng hình cầu)", "NB", 0.5, 2, "trắc nghiệm", "C. $36\\pi$ cm$^3$"),
    ("Câu 5", "Đổi $2{,}5$ m$^3$ ra lít (kiến thức cũ)", "NB", 0.5, 2, "trắc nghiệm", "C. $2500$ lít"),
    ("Câu 6", "Diện tích mặt cầu đường kính $24$ cm, bẫy đường kính (SGK bài 10.24)", "NB", 0.5, 2, "trắc nghiệm", "B. $576\\pi$ cm$^2$"),
    ("Câu 7a", "$S_{xq}$ mũ sinh nhật hình nón, đề cho đường kính và đường sinh (CK2 THCS Lê Hồng Phong)", "NB", 1.0, 3, "tự luận", "$260\\pi \\approx 816{,}4$ cm$^2$"),
    ("Câu 7b", "Thể tích hình nón: tìm chiều cao bằng Pythagore rồi thay số", "TH", 1.0, 5, "tự luận", "$h = 24$ cm; $V = 800\\pi \\approx 2512$ cm$^3$"),
    ("Câu 8a", "Thể tích lon nước ngọt hình trụ, đề cho đường kính (minh hoạ vào 10 Đống Đa, THCS Cát Linh)", "NB", 1.0, 3, "tự luận", "$\\approx 330{,}64$ cm$^3$"),
    ("Câu 8b", "So sánh thể tích $5$ lon với chai $1{,}5$ lít (đổi đơn vị)", "TH", 1.0, 5, "tự luận", "$1653{,}21$ cm$^3 > 1500$ cm$^3$: đổ đầy được"),
    ("Câu 9a", "Thể tích cốc hình trụ, đề cho đường kính (CK2 THCS Nguyễn Du)", "NB", 1.0, 3, "tự luận", "$423{,}9$ cm$^3$"),
    ("Câu 9b", "Bài toán mực nước dâng: thể tích bi $=$ phần nước dâng thêm, rồi tìm bán kính từ $V = \\dfrac{4}{3}\\pi R^3$", "VD", 2.0, 11, "tự luận", "$V_{\\text{bi}} = 18\\pi$; $R = \\sqrt[3]{13{,}5} \\approx 2{,}38$ cm"),
]
assert isclose(sum(r[3] for r in ROWS), 10.0) and sum(r[4] for r in ROWS) <= 45


def so(x):
    s = f"{x:g}".replace(".", "{,}")
    return s


bang = ("\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{8.6cm}|c|c|c|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} \\\\ \\hline\n"
        + "".join(f"{c.replace('Câu ', '')} & {nd} & {m} & ${so(d)}$ & ${so(ph)}$ \\\\ \\hline\n" for c, nd, m, d, ph, _h, _a in ROWS)
        + "\\end{tabular}\\end{center}")
tong = {}
for _c, _n, m, d, ph, _h, _a in ROWS:
    a = tong.setdefault(m, [0, 0]); a[0] += d; a[1] += ph
bang_tong = ("\\begin{center}\\footnotesize\n\\begin{tabular}{|l|c|c|c|c|}\n\\hline\n"
             "\\textbf{Mức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{Tổng} \\\\ \\hline\n"
             f"Điểm & ${so(tong['NB'][0])}$ & ${so(tong['TH'][0])}$ & ${so(tong['VD'][0])}$ & \\textbf{{10}} \\\\ \\hline\n"
             f"Phút & ${so(tong['NB'][1])}$ & ${so(tong['TH'][1])}$ & ${so(tong['VD'][1])}$ & \\textbf{{{so(sum(v[1] for v in tong.values()))}}} \\\\ \\hline\n"
             "\\end{tabular}\\end{center}")

D = "\\hfill \\textit{(0,25đ)}"
DA_TN = ("\\textbf{PHẦN I (3,0 điểm).} Mỗi câu đúng $0{,}5$ điểm.[[br]]"
         "\\textbf{1 – B} ($S_{xq} = 2\\pi\\cdot 4\\cdot 6 = 48\\pi$); \\textbf{2 – C} ($V = \\pi\\cdot 3^2\\cdot 5 = 45\\pi$); "
         "\\textbf{3 – B} ($r = \\sqrt{13^2 - 12^2} = 5$, $S_{xq} = \\pi\\cdot 5\\cdot 13 = 65\\pi$);[[br]]"
         "\\textbf{4 – C} ($V = \\dfrac{4}{3}\\pi\\cdot 3^3 = 36\\pi$); \\textbf{5 – C} ($1$ m$^3 = 1000$ lít); "
         "\\textbf{6 – B} ($R = 12$, $S = 4\\pi\\cdot 12^2 = 576\\pi$).")
DA_7 = ("\\textbf{Câu 7 (2,0 điểm).}[[br]]"
        f"a) Bán kính đáy của chiếc mũ là $r = 20 : 2 = 10$ (cm). {D}[[br]]"
        f"Diện tích xung quanh của chiếc mũ là $S_{{xq}} = \\pi rl \\approx 3{{,}}14\\cdot 10\\cdot 26$ {D}[[br]]"
        f"$= 816{{,}}4$ (cm$^2$). {D}[[br]]"
        f"Vậy diện tích xung quanh của chiếc mũ khoảng $816{{,}}4$ cm$^2$. {D}[[br]]"
        f"b) Xét tam giác vuông tạo bởi chiều cao, bán kính đáy và đường sinh, theo định lí Pythagore:[[br]]$h^2 = l^2 - r^2 = 26^2 - 10^2 = 576$, nên $h = 24$ (cm). {D}[[br]]"
        f"Thể tích của chiếc mũ là $V = \\dfrac{{1}}{{3}}\\pi r^2h$ {D}[[br]]"
        f"$\\approx \\dfrac{{1}}{{3}}\\cdot 3{{,}}14\\cdot 10^2\\cdot 24 = 2512$ (cm$^3$). {D}[[br]]"
        f"Vậy thể tích của chiếc mũ khoảng $2512$ cm$^3$. {D}")
DA_8 = ("\\textbf{Câu 8 (2,0 điểm).}[[br]]"
        f"a) Bán kính đáy của lon là $r = 6 : 2 = 3$ (cm). {D}[[br]]"
        f"Thể tích của một lon là $V = \\pi r^2h \\approx 3{{,}}14\\cdot 3^2\\cdot 11{{,}}7$ {D}[[br]]"
        f"$= 330{{,}}642 \\approx 330{{,}}64$ (cm$^3$). {D}[[br]]"
        f"Vậy thể tích của một lon khoảng $330{{,}}64$ cm$^3$. {D}[[br]]"
        f"b) Đổi $1{{,}}5$ lít $= 1500$ cm$^3$. {D}[[br]]"
        f"Thể tích của $5$ lon là $5\\cdot 330{{,}}642 = 1653{{,}}21$ (cm$^3$). {D}[[br]]"
        f"Vì $1653{{,}}21 > 1500$ nên $5$ lon đủ đổ đầy chai. {D}[[br]]"
        f"Vậy $5$ lon nước ngọt đổ đầy được chai $1{{,}}5$ lít. {D}")
DA_9 = ("\\textbf{Câu 9 (3,0 điểm).}[[br]]"
        f"a) Bán kính đáy của cốc là $r = 6 : 2 = 3$ (cm). {D}[[br]]"
        f"Thể tích của cốc là $V = \\pi r^2h$ {D}[[br]]"
        f"$\\approx 3{{,}}14\\cdot 3^2\\cdot 15 = 423{{,}}9$ (cm$^3$). {D}[[br]]"
        f"Vậy thể tích của cốc thủy tinh là $423{{,}}9$ cm$^3$. {D}[[br]]"
        "b) Viên bi chìm hẳn và nước không tràn nên thể tích viên bi bằng thể tích phần nước dâng thêm. \\hfill \\textit{(0,5đ)}[[br]]"
        f"Phần nước dâng thêm là hình trụ bán kính đáy $3$ cm, cao $2$ cm, nên $V_{{\\text{{bi}}}} = \\pi\\cdot 3^2\\cdot 2 = 18\\pi$ (cm$^3$). \\hfill \\textit{{(0,5đ)}}[[br]]"
        f"Gọi $R$ (cm) là bán kính viên bi. Ta có $\\dfrac{{4}}{{3}}\\pi R^3 = 18\\pi$ {D}[[br]]"
        f"nên $R^3 = 18\\cdot \\dfrac{{3}}{{4}} = 13{{,}}5$. {D}[[br]]"
        f"Suy ra $R = \\sqrt[3]{{13{{,}}5}} \\approx 2{{,}}38$ (cm). {D}[[br]]"
        f"Vậy bán kính của viên bi khoảng $2{{,}}38$ cm. {D}")


def figblk(t):
    return {"type": "figure", "tikz": t}


ma_tran = {
    "slug": "ma-tran-va-dap-an-kiem-tra-chuong-x-lop-9c",
    "title": "Ma trận và đáp án — Kiểm tra Chương X",
    "eyebrow": "TÀI LIỆU GIÁO VIÊN • LỚP 9C • KIỂM TRA CHƯƠNG X",
    "grade_label": "Lớp 9 • Hình học",
    "class_tier": "C",
    "theme": "de_thi",
    "stages": [
        {"kind": "review", "number": 1, "title": "Ma trận đề", "blocks": [
            {"type": "para", "text": "\\textbf{ĐỀ KIỂM TRA CHƯƠNG X — MỘT SỐ HÌNH KHỐI TRONG THỰC TIỄN (LỚP 9C)} ($45$ phút, thang điểm $10$). \\textbf{Phạm vi:} hai buổi đã dạy — sáu công thức trụ, nón, cầu (buổi 1) và luyện tập Câu IV.1 (buổi 2). Câu 7–9 bám Câu IV.1 đề vào 10 Hà Nội: ý a thay số một công thức, ý b một bước thực tế. Không câu nào trùng đề của phiếu A, phiếu C."},
            {"type": "para", "text": bang},
            {"type": "para", "text": bang_tong}]},
        {"kind": "concept", "number": 2, "title": "Đáp án Phần I và Câu 7", "blocks": [
            {"type": "para", "text": DA_TN}, figblk(hinh_non), {"type": "para", "text": DA_7}]},
        {"kind": "practice1", "number": 3, "title": "Đáp án Câu 8", "blocks": [
            figblk(hinh_lon), {"type": "para", "text": DA_8}]},
        {"kind": "practice2", "number": 4, "title": "Đáp án Câu 9", "blocks": [
            figblk(hinh_coc), {"type": "para", "text": DA_9}]},
        {"kind": "reflection", "number": 5, "title": "Biểu điểm tổng hợp", "blocks": [
            {"type": "para", "text": "\\textbf{Phần I (3,0đ):} 6 câu $\\times$ $0{,}5$đ.[[br]]\\textbf{Câu 7 (2,0đ):} a) $1{,}0$đ $-$ b) $1{,}0$đ. \\quad \\textbf{Câu 8 (2,0đ):} a) $1{,}0$đ $-$ b) $1{,}0$đ. \\quad \\textbf{Câu 9 (3,0đ):} a) $1{,}0$đ $-$ b) $2{,}0$đ."},
            {"type": "para", "text": "\\textbf{Tổng: 10,0 điểm.} Học sinh giải cách khác đúng vẫn cho điểm tối đa từng phần. Thay đường kính vào chỗ bán kính: không cho điểm phần thay số và kết quả của ý đó. Thiếu đơn vị hoặc thiếu câu \\textquotedblleft Vậy\\textquotedblright{} trừ $0{,}25$đ mỗi ý. Làm tròn ngay ở bước giữa làm lệch kết quả cuối: trừ $0{,}25$đ, \textbf{trừ hai trường hợp được cho trọn điểm}: Câu 8b dùng số đã làm tròn ở 8a ($5\\cdot 330{,}64 = 1653{,}2$ cm$^3 > 1500$ cm$^3$); Câu 9b thay $\\pi \\approx 3{,}14$ ($V_{\\text{bi}} \\approx 56{,}52$ cm$^3$, vẫn ra $R \\approx 2{,}38$ cm)."}]},
    ],
}

spec = json.loads((DIR / "de-kiem-tra.json").read_text(encoding="utf-8"))
spec["title"] = "Chương X. Một số hình khối trong thực tiễn • kiểm tra chương (buổi 2)"
spec["ghi_chu"] = [
    "Luật cứng (Thầy chốt 26/09/2026): cuối MỖI chương có bài kiểm tra 45 phút. Từ 12/11/2026 chương X còn 2 buổi: kiểm tra ở nửa sau buổi 2 (tuần 33) — buổi 2 $=$ 45 phút luyện tập (phiếu C) $+$ 45 phút kiểm tra.",
    "Phạm vi trọn chương: Bài 31 (hình trụ, hình nón) và Bài 32 (hình cầu), bám Câu IV.1 đề thi Vào 10. Câu tự luận chia ý a (thay số một công thức) $+$ ý b (một bước thực tế) như barem của Sở.",
    "Đề KHÔNG trùng bài nào của phiếu A, phiếu C; nguồn: SGK (Phần I), CK2 THCS Lê Hồng Phong, đề minh hoạ Đống Đa (THCS Cát Linh), CK2 THCS Nguyễn Du.",
    "Tờ đề HS không in đáp số; ma trận $+$ đáp án ở tài liệu riêng (kiem-tra-chuong/).",
]
spec["de"] = [{
    "ma": "KT-X", "ten": "Đề kiểm tra Chương X — Một số hình khối trong thực tiễn (45 phút)",
    "tuan": 33, "phut": 45, "diem_toi_da": 10.0,
    "pham_vi": "Bài 31 – Bài 32 SGK Toán 9 KNTT: hình trụ, hình nón, hình cầu và bài thực tế Câu IV.1.",
    "cau": [{"ma": c, "dang": nd, "band": m, "diem": d, "phut": ph, "hinh_thuc": h, "dap_an": a}
            for c, nd, m, d, ph, h, a in ROWS],
}]

(DIR / "de-kiem-tra.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(KT / "de-kiem-tra-chuong-x.json").write_text(json.dumps(de, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(KT / "ma-tran-va-dap-an-kiem-tra-chuong-x.json").write_text(json.dumps(ma_tran, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ghi 3 file", {k: v for k, v in tong.items()})
