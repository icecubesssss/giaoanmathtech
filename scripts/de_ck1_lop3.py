#!/usr/bin/env python3
"""Sinh 3 ĐỀ CHÍNH THỨC + 3 ĐỀ ÔN TẬP cuối HK1 Toán 3 (KNTT) và MA TRẬN kèm đáp án.

Barem theo đề trung tâm lớp 3 (T3-HKI-KNTT-01, inputs/refs/de-thi/lop-3/de-trung-tam), 40 phút:
  PHẦN I (5đ): Câu 1–4 mỗi câu 1đ (2 ý a, b × 0,5đ), Câu 5–6 mỗi câu 0,5đ.
  PHẦN II (5đ): Câu 7 đặt tính 4 phép (2đ) · Câu 8 bài toán hai bước (2đ) · Câu 9 tư duy 2 ý (1đ).
Chỉ dùng Chủ đề 1–7 (kì I). Câu bốc từ đề TRƯỜNG THẬT trong ngân hàng
inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi; nguồn ghi ở lời giải GV và cột Nguồn của ma trận.
    .venv/bin/python scripts/de_ck1_lop3.py
"""
import copy, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "inputs/seeds/lop-3/de-cuoi-ki-1"
BG = ROOT / "inputs/refs/ngan-hang-sheet/tieu-hoc/lop-3/ban-ghi"
KHUNG = json.loads((ROOT / "config/khung-phan-dang/tieu-hoc-lop-3-kntt.json").read_text(encoding="utf-8"))
BASE = json.loads((ROOT / "inputs/seeds/lop-4/de-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-de-2.json").read_text(encoding="utf-8"))
SKEL_MT = json.loads((ROOT / "inputs/seeds/lop-5/de-cuoi-ki-1/ma-tran-va-dap-an-cuoi-ki-1-de-1.json").read_text(encoding="utf-8"))
NAM = "NĂM HỌC 2026 – 2027"

BANK = {f.stem[3:]: json.loads(f.read_text(encoding="utf-8")) for f in sorted(BG.glob("l3-*.json"))}
CK1 = [k for k in BANK if k.startswith("ck1-")]
TEN_BAI = {b["so"]: b["ten"] for cd in KHUNG["chu_de"] for b in cd["bai"]}
TEN_CD = {cd["so"]: cd["ten"] for cd in KHUNG["chu_de"]}
TEN_CD[0] = "Toán tư duy"


def cau(ref):
    de, c = ref.split("#")
    return next(x for x in BANK[de]["cau"] if x["cau"] == c)


NGUON = {
    "ck1-2425-nguyenbinhkhiem": "Đề CK1 Trường TH\\&THCS Nguyễn Bỉnh Khiêm 2024-2025",
    "ck1-2425-thanhhung2": "Đề CK1 TH Thạnh Hưng 2 2024-2025",
    "ck1-2526-donghoa": "Đề CK1 TH Đồng Hòa, Kiến An, Hải Phòng 2025-2026",
    "ck1-2526-khanhthien": "Đề CK1 Trường TH\\&THCS Khánh Thiện, Lâm Thượng 2025-2026",
    "ck1-2526-nguyenvantroi": "Đề CK1 TH Nguyễn Văn Trỗi, Cát Hải, Hải Phòng 2025-2026",
    "ck1-2526-phuluong": "Đề CK1 TH Phú Lương 2025-2026",
    "ck1-2526-thanhuyen": "Đề CK1 TH Thanh Uyên, Hiền Quan, Phú Thọ 2025-2026",
    "ck1-2526-vinhbao": "Đề CK1 TH Vĩnh Bảo, Hải Phòng 2025-2026",
    "ck2-2425-huuthanhb": "Đề CK2 TH Hựu Thành B, Vĩnh Long 2024-2025 (câu kiến thức kì I)",
    "ck2-2526-tayhung": "Đề CK2 TH Tây Hưng, Hải Phòng 2025-2026 (câu kiến thức kì I)",
    "tt": "Đề trung tâm MathTech T3-HKI-KNTT-01",
}


def ng(ref, note=""):
    de, c = ref.split("#")
    return f"{NGUON[de]}, câu {c}" + (f" ({note})" if note else "")


# ------------------------------------------------------------------ dựng câu
def ops(opts, n=4):
    w = {4: "3.9cm", 3: "5.2cm", 2: "8cm", 1: "16cm"}[n]
    cells = [f"\\textbf{{{'ABCD'[i]}.}} {o}" for i, o in enumerate(opts)]
    rows = [" & ".join(cells[i:i + n]) for i in range(0, len(cells), n)]
    return "\\par\\noindent\\begin{tabular}{@{}" + f"p{{{w}}}" * n + "@{}}" + " \\\\ ".join(rows) + "\\end{tabular}"


def y(letter, text):
    return f"\\par\\noindent\\textbf{{{letter})}} {text}"


def fig(text, tikz, w=0.6):
    return (f"\\par\\noindent\\begin{{minipage}}[c]{{{w}\\linewidth}}\\raggedright {text}\\end{{minipage}}\\hfill"
            f"\\begin{{minipage}}[c]{{{0.97 - w:.2f}\\linewidth}}\\centering {tikz}\\end{{minipage}}")


def Q(label, level, diem, body, ans, sol, src, meta):
    """meta = (nội dung ngắn, [ref bank] | dict thủ công, mức, phút)."""
    return {"blk": {"type": "problem", "label": label + ".", "level": level,
                    "statement": f"\\textbf{{({diem} điểm)}} " + body, "answer": ans,
                    "solution": sol + f" [[br]] \\textit{{(Nguồn: {src}.)}}", "tier": "onclass"},
            "meta": meta, "diem": float(diem.replace(",", ".")), "nguon": src}


def ds(items):
    return "".join(f"\\par\\noindent {chr(97 + i)}) {x} \\hfill $\\square$" for i, x in enumerate(items))


def dien(n=1, dai="\\makebox[3.2cm]{\\dotfill}"):
    return dai


# ------------------------------------------------------------------ hình
def htron(diem_tren, doan, extra=""):
    """Hình tròn tâm O bán kính 1,3; diem_tren = [(tên, góc)], doan = [(tên1, tên2)]."""
    pos = {t: f"({g}:1.3)" for t, g in diem_tren}
    pos["O"] = "(0,0)"
    s = "\\begin{tikzpicture}[scale=0.95]\\draw (0,0) circle (1.3);"
    for a, b in doan:
        s += f"\\draw {pos[a]} -- {pos[b]};"
    s += extra
    for t, g in diem_tren:
        s += f"\\fill {pos[t]} circle (1.3pt) node[shift=({g}:11pt)]{{${t}$}};"
    return s + "\\fill (0,0) circle (1.3pt) node[below left=-1pt]{$O$};\\end{tikzpicture}"


F_DH5 = htron([("J", 150), ("K", 330), ("L", 100), ("N", 20)], [("J", "K"), ("L", "N")],
              "\\fill (0.5,0.86) circle (1.3pt) node[below=1pt]{$M$};")
F_VB2A = htron([("A", 180), ("B", 0), ("M", 70)], [("A", "B"), ("O", "M")])
F_TU1B = htron([("A", 200), ("B", 20), ("M", 120), ("N", 40)], [("A", "B"), ("M", "N")],
               "\\fill (0.17,0.98) circle (1.3pt) node[below=1pt]{$I$};")
F_VB2B = ("\\begin{tikzpicture}[scale=0.85]\\draw (0,0)--(6,0);"
          + "".join(f"\\fill ({x},0) circle (1.5pt) node[below=2pt]{{${t}$}};" for t, x in (("I", 0), ("M", 1.4), ("O", 3), ("K", 6)))
          + "\\node[above] at (1.5,0) {\\small $6$ cm};\\node[above] at (4.5,0) {\\small $6$ cm};\\end{tikzpicture}")


def tugiac(P, doan):
    s = "\\begin{tikzpicture}[scale=0.85]"
    for a, b in doan:
        s += f"\\draw {P[a][0]} -- {P[b][0]};"
    for t, (p, d) in P.items():
        s += f"\\fill {p} circle (1.3pt) node[{d}]{{${t}$}};"
    return s + "\\end{tikzpicture}"


F_VB9 = tugiac({"A": ("(0.8,1.6)", "above"), "N": ("(2,1.6)", "above"), "B": ("(3.2,1.6)", "above"),
                "C": ("(4,0)", "below"), "D": ("(0,0)", "below")},
               [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("N", "D"), ("N", "C")])
F_HCN = tugiac({"A": ("(0,1.7)", "above"), "H": ("(1.4,1.7)", "above"), "B": ("(4,1.7)", "above"),
                "C": ("(4,0)", "below"), "D": ("(0,0)", "below")},
               [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("H", "D"), ("H", "C")])
F_KT1D = tugiac({"A": ("(0,1.4)", "above"), "B": ("(2.6,1.4)", "above"), "E": ("(4.2,1.4)", "above"),
                 "C": ("(2.6,0)", "below"), "D": ("(0,0)", "below")},
                [("A", "E"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "C")])
SODO = ("\\begin{tikzpicture}[b/.style={draw,minimum width=1.1cm,minimum height=0.6cm}]"
        "\\node[b] (a) at (0,0) {$125$};\\node[b] (b) at (3.9,0) {};\\node[b] (c) at (7.8,0) {};\\node[b] (d) at (11.7,0) {};"
        "\\draw[->] (a) -- node[above]{\\footnotesize gấp lên $3$ lần} (b);"
        "\\draw[->] (b) -- node[above]{\\footnotesize bớt đi $3$ đơn vị} (c);"
        "\\draw[->] (c) -- node[above]{\\footnotesize giảm đi $6$ lần} (d);\\end{tikzpicture}")

# ------------------------------------------------------------------ mẫu lời giải TL
def giai(*dong):
    return " [[br]] ".join(dong)


def dat_tinh(cac):
    return "Đặt tính rồi tính: \\par\\noindent\\begin{tabular}{@{}p{3.9cm}p{3.9cm}p{3.9cm}p{3.9cm}@{}}" + " & ".join(
        f"\\textbf{{{'abcd'[i]})}} ${p}$" for i, (p, _) in enumerate(cac)) + "\\end{tabular}"


def dt_sol(cac):
    return giai(*[f"\\textbf{{{'abcd'[i]})}} ${p} = {k}$" for i, (p, k) in enumerate(cac)],
                "Mỗi phép tính $0{,}5$đ: đặt tính đúng $0{,}25$đ, kết quả đúng $0{,}25$đ.")


# =====================================================================
#                              DỮ LIỆU 6 ĐỀ
# =====================================================================
DE = {}

# ---------------------------------------------------------------- ĐỀ 1
DE[1] = ("Đề 1", [
    Q("Câu 1", 1, "1", y("a", "Viết số: [[br]] Số gồm $3$ trăm và $6$ đơn vị: \\makebox[3.2cm]{\\dotfill} \\qquad Số gồm $5$ trăm, $7$ chục và $8$ đơn vị: \\makebox[3.2cm]{\\dotfill}")
      + y("b", "Số chẵn lớn nhất có ba chữ số là:") + ops(["$998$", "$986$", "$999$"], 3),
      "a) 306; 578 – b) A", "a) $306$; $578$ (mỗi số $0{,}25$đ). b) Chọn \\textbf{A}: số lớn nhất có ba chữ số là $999$ (lẻ) nên số chẵn lớn nhất là $998$.",
      "a) " + ng("ck1-2526-donghoa#1a") + "; b) " + ng("ck1-2526-phuluong#2b"),
      ("Viết số theo hàng; số chẵn lớn nhất", ["ck1-2526-donghoa#1a", "ck1-2526-phuluong#2b"], 1, 3)),
    Q("Câu 2", 1, "1", y("a", "$\\frac{1}{4}$ của $16$ là:") + ops(["$3$", "$4$", "$5$", "$6$"])
      + y("b", "Năm nay ông của Nam $70$ tuổi, tuổi của bố Nam bằng tuổi của ông giảm đi $2$ lần. Hỏi năm nay bố của Nam bao nhiêu tuổi?") + ops(["$35$ tuổi", "$72$ tuổi", "$68$ tuổi", "$50$ tuổi"]),
      "a) B – b) A", "a) Chọn \\textbf{B}: $16 : 4 = 4$. b) Chọn \\textbf{A}: $70 : 2 = 35$ (tuổi). \\textit{Bẫy: \"giảm đi 2 lần\" là chia, không phải trừ.}",
      "a) " + ng("ck1-2526-khanhthien#1a") + "; b) " + ng("ck1-2425-nguyenbinhkhiem#6"),
      ("Một phần mấy; giảm một số đi một số lần", ["ck1-2526-khanhthien#1a", "ck1-2425-nguyenbinhkhiem#6"], 1, 3)),
    Q("Câu 3", 2, "1", fig("Quan sát hình bên rồi làm theo yêu cầu:" + y("a", "Kể tên các bán kính có trong hình: [[br]] \\dotfill\\mbox{}")
      + y("b", "Vẽ thêm vào hình bên bán kính $OA$ và đường kính $BC$."), F_DH5),
      "a) OJ, OK – b) HS vẽ", "a) Bán kính: $OJ$, $OK$ ($0{,}5$đ). $LN$ không đi qua tâm $O$ nên $OM$, $LN$ không phải bán kính hay đường kính. b) Vẽ đúng bán kính $OA$ ($A$ trên đường tròn) và đường kính $BC$ (đi qua $O$) ($0{,}5$đ).",
      ng("ck1-2526-donghoa#5", "hình vẽ lại theo đề gốc"),
      ("Hình tròn: tâm, bán kính, đường kính", ["ck1-2526-donghoa#5"], 2, 3)),
    Q("Câu 4", 1, "1", y("a", "Trong phích có $1$ l nước. Rót nước ở phích sang $2$ ca, mỗi ca $200$ ml. Hỏi sau khi rót xong, lượng nước còn lại trong phích là bao nhiêu?") + ops(["$800$ ml", "$400$ ml", "$200$ ml", "$600$ ml"])
      + y("b", "$34$ mm $+ 16$ mm $= \\dots$ cm. Số thích hợp điền vào chỗ chấm là:") + ops(["$50$", "$5$", "$500$", "$100$"]),
      "a) D – b) B", "a) Chọn \\textbf{D}: $1$ l $= 1\\,000$ ml; $1\\,000 - 200 \\times 2 = 600$ (ml). b) Chọn \\textbf{B}: $34 + 16 = 50$ (mm) $= 5$ cm.",
      "a) " + ng("ck1-2526-nguyenvantroi#6b") + "; b) " + ng("ck1-2526-thanhuyen#1a"),
      ("Đơn vị đo: ml, mm – cm", ["ck1-2526-nguyenvantroi#6b", "ck1-2526-thanhuyen#1a"], 1, 3)),
    Q("Câu 5", 2, "0,5", "Giá trị của biểu thức $65 - 12 \\times 3$ là:" + ops(["$29$", "$159$", "$39$", "$19$"]),
      "A", "Chọn \\textbf{A}: nhân trước, trừ sau: $65 - 36 = 29$. \\textit{Bẫy: trừ trước ra $159$.}", ng("ck1-2526-khanhthien#4"),
      ("Tính giá trị biểu thức (nhân trước, trừ sau)", ["ck1-2526-khanhthien#4"], 2, 2)),
    Q("Câu 6", 2, "0,5", "Số dư của phép chia $124 : 3$ là:" + ops(["$1$", "$2$", "$3$", "$4$"]),
      "A", "Chọn \\textbf{A}: $124 = 3 \\times 41 + 1$.", ng("ck1-2526-donghoa#3a"),
      ("Phép chia có dư", ["ck1-2526-donghoa#3a"], 2, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("38 + 548", "586"), ("402 - 256", "146"), ("124 \\times 7", "868"), ("189 : 9", "21")]),
      "586; 146; 868; 21", dt_sol([("38 + 548", "586"), ("402 - 256", "146"), ("124 \\times 7", "868"), ("189 : 9", "21")]),
      ng("ck1-2526-donghoa#7"), ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2526-donghoa#7"], 1, 7)),
    Q("Câu 8", 2, "2", "Để giúp đỡ các bạn học sinh vùng bão lũ, nhà trường phát động học sinh ủng hộ vở. Ngày thứ nhất ủng hộ được $215$ quyển vở, ngày thứ hai ủng hộ được số vở gấp ba lần số vở ngày thứ nhất. Hỏi cả hai ngày các bạn học sinh ủng hộ được bao nhiêu quyển vở?",
      "860 quyển", giai("Ngày thứ hai ủng hộ được số quyển vở là: $215 \\times 3 = 645$ (quyển) \\hfill \\textit{(0,75đ)}",
                        "Cả hai ngày ủng hộ được số quyển vở là: $215 + 645 = 860$ (quyển) \\hfill \\textit{(0,75đ)}",
                        "Đáp số: $860$ quyển vở. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2526-vinhbao#10"), ("Bài toán giải bằng hai bước tính (gấp lên rồi cộng)", ["ck1-2526-vinhbao#10"], 2, 8)),
    Q("Câu 9", 3, "1", y("a", "Trong một cuộc thi đấu cờ, ba bạn Trí, Dũng, Minh đạt cả ba giải cao nhất. Trí không đạt giải nhất, Dũng không đạt giải nhì, Minh không đạt giải nhất và không đạt giải ba. Vậy \\makebox[3.2cm]{\\dotfill} đạt giải nhất, \\makebox[3.2cm]{\\dotfill} đạt giải nhì, \\makebox[3.2cm]{\\dotfill} đạt giải ba.")
      + y("b", "Tìm một số, biết rằng nếu lấy số đó nhân với số lẻ lớn nhất có một chữ số thì được $909$."),
      "a) Dũng – Minh – Trí; b) 101", "a) Minh không nhất, không ba nên Minh đạt giải nhì; Trí không nhất nên Trí đạt giải ba; Dũng đạt giải nhất ($0{,}5$đ). b) Số lẻ lớn nhất có một chữ số là $9$. Số cần tìm là $909 : 9 = 101$ ($0{,}5$đ).",
      "a) " + ng("ck1-2526-donghoa#10b") + "; b) " + ng("ck1-2526-nguyenvantroi#10a"),
      ("Suy luận logic; tìm thừa số", ["ck1-2526-donghoa#10b", "ck1-2526-nguyenvantroi#10a"], 3, 6)),
], "$\\square$ Đã đặt tính thẳng cột (Câu 7) & $\\square$ Câu 8 có câu lời giải và đáp số")

# ---------------------------------------------------------------- ĐỀ 2
DE[2] = ("Đề 2", [
    Q("Câu 1", 1, "1", y("a", "Số \"Chín trăm mười hai\" viết là:") + ops(["$92$", "$902$", "$912$"], 3)
      + y("b", "Chữ số $6$ trong số $461$ có giá trị là:") + ops(["$600$", "$60$", "$61$", "$46$"]),
      "a) C – b) B", "a) Chọn \\textbf{C}: $912$. b) Chọn \\textbf{B}: chữ số $6$ ở hàng chục nên có giá trị $60$.",
      "a) " + ng("ck1-2526-phuluong#1a") + "; b) " + ng("ck1-2526-khanhthien#1b"),
      ("Viết số; giá trị chữ số", ["ck1-2526-phuluong#1a", "ck1-2526-khanhthien#1b"], 1, 3)),
    Q("Câu 2", 1, "1", y("a", "Có $12$ quả dưa hấu. $\\frac{1}{4}$ số quả dưa hấu đó là:") + ops(["$2$ quả", "$3$ quả", "$4$ quả", "$5$ quả"])
      + y("b", "Một cửa hàng có $36$ quả dưa hấu, sau khi đem bán thì số dưa hấu giảm đi $6$ lần. Hỏi cửa hàng còn lại bao nhiêu quả dưa hấu?") + ops(["$30$ quả", "$5$ quả", "$6$ quả", "$42$ quả"]),
      "a) B – b) C", "a) Chọn \\textbf{B}: $12 : 4 = 3$ (quả). b) Chọn \\textbf{C}: $36 : 6 = 6$ (quả). \\textit{Bẫy: $36 - 6 = 30$.}",
      "a) " + ng("ck1-2526-nguyenvantroi#2", "đề gốc cho hình 12 quả, chuyển thành lời") + "; b) " + ng("ck1-2526-khanhthien#1c", "đề gốc in trùng phương án B và D, sửa D thành 42 quả"),
      ("Một phần mấy; giảm một số đi một số lần", ["ck1-2526-nguyenvantroi#2", "ck1-2526-khanhthien#1c"], 1, 3)),
    Q("Câu 3", 2, "1", fig("Hình vẽ bên có mấy hình tứ giác? Hãy kể tên các hình tứ giác đó. [[br]] Trả lời: Có \\makebox[2cm]{\\dotfill} hình tứ giác, đó là: [[br]] \\dotfill\\mbox{}", F_VB9, 0.62),
      "3 hình: ABCD, ANCD, NBCD", "Có $3$ hình tứ giác ($0{,}25$đ): $ABCD$, $ANCD$, $NBCD$ (mỗi tên đúng $0{,}25$đ).",
      ng("ck1-2526-vinhbao#9", "hình vẽ lại theo đề gốc"), ("Đếm hình tứ giác", ["ck1-2526-vinhbao#9"], 2, 3)),
    Q("Câu 4", 1, "1", y("a", "Nhiệt độ cơ thể người bình thường là:") + ops(["$39\\,^\\circ$C", "$37\\,^\\circ$C", "$40\\,^\\circ$C", "$38\\,^\\circ$C"])
      + y("b", "Nhiệt độ không khí tại Hải Phòng vào buổi sáng là $18\\,^\\circ$C, đến buổi trưa nhiệt độ tăng lên thành $25\\,^\\circ$C. Hỏi thời điểm nào thời tiết lạnh hơn?") + ops(["Buổi trưa", "Cả hai như nhau", "Buổi sáng", "Không thể so sánh"], 2),
      "a) B – b) C", "a) Chọn \\textbf{B}: $37\\,^\\circ$C. b) Chọn \\textbf{C}: $18\\,^\\circ$C $< 25\\,^\\circ$C nên buổi sáng lạnh hơn.",
      "a) " + ng("ck1-2526-donghoa#4b") + "; b) " + ng("ck1-2526-nguyenvantroi#6a"),
      ("Nhiệt độ, đơn vị đo nhiệt độ", ["ck1-2526-donghoa#4b", "ck1-2526-nguyenvantroi#6a"], 1, 3)),
    Q("Câu 5", 2, "0,5", "Giá trị của biểu thức $27 : 3 + 45$ là:" + ops(["$57$", "$55$", "$56$", "$54$"]),
      "D", "Chọn \\textbf{D}: $9 + 45 = 54$.", ng("ck1-2526-vinhbao#4b"),
      ("Tính giá trị biểu thức (chia trước, cộng sau)", ["ck1-2526-vinhbao#4b"], 2, 2)),
    Q("Câu 6", 2, "0,5", "Trong những phép chia có số chia là $9$, số dư lớn nhất là:" + ops(["$7$", "$8$", "$9$"], 3),
      "B", "Chọn \\textbf{B}: số dư luôn bé hơn số chia nên số dư lớn nhất là $8$.", ng("ck1-2526-phuluong#4"),
      ("Phép chia có dư", ["ck1-2526-phuluong#4"], 2, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("492 + 359", "851"), ("582 - 265", "317"), ("114 \\times 8", "912"), ("156 : 6", "26")]),
      "851; 317; 912; 26", dt_sol([("492 + 359", "851"), ("582 - 265", "317"), ("114 \\times 8", "912"), ("156 : 6", "26")]),
      ng("ck1-2526-khanhthien#6"), ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2526-khanhthien#6"], 1, 7)),
    Q("Câu 8", 2, "2", "Một cửa hàng có $6$ bao gạo, mỗi bao nặng $50$ kg. Cửa hàng đã bán $235$ kg gạo. Hỏi cửa hàng còn lại bao nhiêu ki-lô-gam gạo?",
      "65 kg", giai("Cửa hàng có số ki-lô-gam gạo là: $50 \\times 6 = 300$ (kg) \\hfill \\textit{(0,75đ)}",
                    "Cửa hàng còn lại số ki-lô-gam gạo là: $300 - 235 = 65$ (kg) \\hfill \\textit{(0,75đ)}",
                    "Đáp số: $65$ kg gạo. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2526-donghoa#9"), ("Bài toán giải bằng hai bước tính (nhân rồi trừ)", ["ck1-2526-donghoa#9"], 2, 8)),
    Q("Câu 9", 3, "1", y("a", "Một phép chia có số bị chia là số tròn chục lớn nhất có hai chữ số, thương bằng số lớn nhất có một chữ số. Tìm số chia.")
      + y("b", "Bạn Mai trang trí một hộp quà dạng khối hộp chữ nhật bằng cách dán $4$ bông hoa vào mỗi mặt của hộp quà. Hỏi bạn Mai đã dán bao nhiêu bông hoa? [[br]] Trả lời: Bạn Mai đã dán \\makebox[3.2cm]{\\dotfill} bông hoa."),
      "a) 10; b) 24", "a) Số bị chia là $90$, thương là $9$. Số chia là $90 : 9 = 10$ ($0{,}5$đ). b) Khối hộp chữ nhật có $6$ mặt nên Mai dán $4 \\times 6 = 24$ (bông hoa) ($0{,}5$đ).",
      "a) " + ng("ck1-2526-khanhthien#9") + "; b) " + ng("ck1-2526-vinhbao#11"),
      ("Tìm số chia; số mặt khối hộp chữ nhật", ["ck1-2526-khanhthien#9", "ck1-2526-vinhbao#11"], 3, 6)),
], "$\\square$ Đã đặt tính thẳng cột (Câu 7) & $\\square$ Câu 8 có câu lời giải và đáp số")

# ---------------------------------------------------------------- ĐỀ 3
DE[3] = ("Đề 3", [
    Q("Câu 1", 1, "1", y("a", "Số $647$ đọc là:") + ops(["Sáu bốn mươi bảy", "Sáu trăm bốn mươi bảy", "Sáu trăm bốn bảy"], 3)
      + y("b", "Các số được xếp theo thứ tự từ lớn đến bé là:") + ops(["$298$; $347$; $365$; $391$", "$347$; $365$; $391$; $298$", "$391$; $365$; $347$; $298$"], 3),
      "a) B – b) C", "a) Chọn \\textbf{B}. b) Chọn \\textbf{C}: so sánh chữ số hàng trăm, rồi hàng chục.",
      "a) " + ng("ck1-2526-phuluong#1b") + " và " + ng("ck1-2425-thanhhung2#2") + "; b) " + ng("ck1-2526-donghoa#3b"),
      ("Đọc số; so sánh, sắp xếp số", ["ck1-2526-phuluong#1b", "ck1-2526-donghoa#3b"], 1, 3)),
    Q("Câu 2", 1, "1", y("a", "Có $15$ quả xoài. $\\frac{1}{3}$ số quả xoài là \\makebox[3.2cm]{\\dotfill} quả xoài.")
      + y("b", "$5$ mm gấp $6$ lần là:") + ops(["$11$ mm", "$20$ mm", "$30$ mm"], 3),
      "a) 5 – b) C", "a) $15 : 3 = 5$ (quả). b) Chọn \\textbf{C}: $5 \\times 6 = 30$ (mm). \\textit{Bẫy: $5 + 6 = 11$.}",
      "a) " + ng("ck1-2526-thanhuyen#3b", "đề gốc cho hình 15 quả, chuyển thành lời") + "; b) " + ng("ck1-2425-thanhhung2#3") + " và " + ng("ck1-2526-phuluong#3"),
      ("Một phần mấy; gấp một số lên một số lần", ["ck1-2526-thanhuyen#3b", "ck1-2425-thanhhung2#3"], 1, 3)),
    Q("Câu 3", 2, "1", fig(y("a", "Hình tròn tâm $O$ (hình 1) có:") + ops(["Bán kính $OA$, đường kính $AM$", "Bán kính $OM$, đường kính $OA$", "Bán kính $AB$, đường kính $OM$", "Bán kính $OM$, đường kính $AB$"], 1),
                           F_VB2A + "\\par\\footnotesize Hình 1", 0.62)
      + fig(y("b", "Trung điểm của đoạn thẳng $IK$ (hình 2) là điểm:") + ops(["$M$", "$O$", "$K$", "$I$"], 2),
            F_VB2B + "\\par\\footnotesize Hình 2", 0.45),
      "a) D – b) B", "a) Chọn \\textbf{D}: $AB$ đi qua tâm $O$ nên là đường kính; $OM$ là bán kính. b) Chọn \\textbf{B}: $O$ nằm giữa $I$, $K$ và $IO = OK = 6$ cm.",
      "a) " + ng("ck1-2526-vinhbao#2a") + "; b) " + ng("ck1-2526-vinhbao#2b") + " (hình vẽ lại theo đề gốc)",
      ("Hình tròn; trung điểm của đoạn thẳng", ["ck1-2526-vinhbao#2a", "ck1-2526-vinhbao#2b"], 2, 3)),
    Q("Câu 4", 1, "1", y("a", "Quả cam cân nặng khoảng:") + ops(["$20$ g", "$2$ g", "$200$ g", "$2$ kg"])
      + y("b", "Một chiếc cân đĩa thăng bằng: đĩa bên trái đặt quả cân $650$ g; đĩa bên phải đặt một túi đường và một hộp bánh nặng $235$ g. Túi đường cân nặng:") + ops(["$885$ g", "$235$ g", "$865$ g", "$415$ g"]),
      "a) C – b) D", "a) Chọn \\textbf{C}. b) Chọn \\textbf{D}: $650 - 235 = 415$ (g).",
      "a) " + ng("ck1-2425-nguyenbinhkhiem#3") + "; b) " + ng("ck1-2526-thanhuyen#2b", "đề gốc cho hình cân, in trùng phương án A và C; chuyển thành lời, sửa C thành 865 g"),
      ("Gam: ước lượng, tính với đơn vị g", ["ck1-2425-nguyenbinhkhiem#3", "ck1-2526-thanhuyen#2b"], 1, 3)),
    Q("Câu 5", 3, "0,5", "Tính nhanh giá trị của biểu thức $(126 + 24) \\times (29 + 7 - 36)$:" + ops(["$36$", "$150$", "$1$", "$0$"]),
      "D", "Chọn \\textbf{D}: $29 + 7 - 36 = 0$ nên tích bằng $0$.", ng("ck1-2526-nguyenvantroi#1b"),
      ("Tính nhanh biểu thức (thừa số bằng 0)", ["ck1-2526-nguyenvantroi#1b"], 3, 2)),
    Q("Câu 6", 1, "0,5", "Trong các phép chia dưới đây, phép chia nào là phép chia có dư?" + ops(["$46 : 5$", "$32 : 8$", "$48 : 6$", "$27 : 3$"]),
      "A", "Chọn \\textbf{A}: $46 : 5 = 9$ (dư $1$).", ng("ck1-2526-vinhbao#1b"),
      ("Phép chia có dư", ["ck1-2526-vinhbao#1b"], 1, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("245 + 318", "563"), ("927 - 256", "671"), ("15 \\times 8", "120"), ("968 : 3", "322 \\text{ (dư } 2)")]),
      "563; 671; 120; 322 dư 2", dt_sol([("245 + 318", "563"), ("927 - 256", "671"), ("15 \\times 8", "120"), ("968 : 3", "322 \\text{ (dư } 2)")]),
      ng("ck1-2526-nguyenvantroi#7"), ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2526-nguyenvantroi#7"], 1, 7)),
    Q("Câu 8", 2, "2", "Thùng thứ nhất đựng được $348$ lít dầu, thùng thứ hai đựng được số dầu bằng $\\frac{1}{4}$ số dầu ở thùng thứ nhất. Hỏi cả hai thùng đựng được bao nhiêu lít dầu?",
      "435 l", giai("Thùng thứ hai đựng được số lít dầu là: $348 : 4 = 87$ (l) \\hfill \\textit{(0,75đ)}",
                    "Cả hai thùng đựng được số lít dầu là: $348 + 87 = 435$ (l) \\hfill \\textit{(0,75đ)}",
                    "Đáp số: $435$ l dầu. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2526-thanhuyen#7"), ("Bài toán giải bằng hai bước tính (một phần mấy rồi cộng)", ["ck1-2526-thanhuyen#7"], 2, 8)),
    Q("Câu 9", 3, "1", y("a", "Tìm một số, biết rằng nếu lấy số đó nhân với $6$ rồi chia cho $5$ thì được kết quả là $66$.")
      + y("b", "Tổng hai số là $628$. Nếu giảm số hạng thứ nhất $75$ đơn vị và tăng số hạng thứ hai $46$ đơn vị thì tổng mới là bao nhiêu?"),
      "a) 55; b) 599", "a) Trước khi chia cho $5$ là $66 \\times 5 = 330$; số cần tìm là $330 : 6 = 55$ ($0{,}5$đ). b) Tổng mới là $628 - 75 + 46 = 599$ ($0{,}5$đ).",
      "a) " + ng("ck1-2526-thanhuyen#8b") + "; b) " + ng("ck1-2526-phuluong#9"),
      ("Tính ngược; tổng thay đổi khi thay đổi số hạng", ["ck1-2526-thanhuyen#8b", "ck1-2526-phuluong#9"], 3, 6)),
], "$\\square$ Đã ghi \"dư\" ở phép chia (Câu 7) & $\\square$ Câu 8 có câu lời giải và đáp số")

# ---------------------------------------------------------------- ÔN 1
DE["on1"] = ("Đề ôn số 1", [
    Q("Câu 1", 1, "1", y("a", "Đọc số: $355$: \\dotfill\\mbox{}")
      + y("b", "Số lớn nhất trong các số $600$; $699$; $599$; $609$ là:") + ops(["$600$", "$699$", "$599$"], 3),
      "a) Ba trăm năm mươi lăm – b) B", "a) Ba trăm năm mươi lăm. b) Chọn \\textbf{B}: $699$.",
      "a) " + ng("ck1-2526-donghoa#1b") + "; b) " + ng("ck1-2526-phuluong#2a"),
      ("Đọc số; so sánh số", ["ck1-2526-donghoa#1b", "ck1-2526-phuluong#2a"], 1, 3)),
    Q("Câu 2", 1, "1", y("a", "Thương của phép chia $72 : 8$ là:") + ops(["$9$", "$8$", "$7$", "$6$"])
      + y("b", "Xếp đều $16$ quả dâu tây vào $4$ hộp. Lấy $3$ hộp như thế có bao nhiêu quả dâu tây?") + ops(["$4$ quả", "$3$ quả", "$12$ quả", "$13$ quả"]),
      "a) A – b) C", "a) Chọn \\textbf{A}: $72 : 8 = 9$. b) Chọn \\textbf{C}: mỗi hộp $16 : 4 = 4$ (quả); $3$ hộp có $4 \\times 3 = 12$ (quả).",
      "a) " + ng("ck1-2526-nguyenvantroi#1a") + "; b) " + ng("ck1-2526-nguyenvantroi#3"),
      ("Bảng chia; bài toán hai bước nhân – chia", ["ck1-2526-nguyenvantroi#1a", "ck1-2526-nguyenvantroi#3"], 1, 3)),
    Q("Câu 3", 2, "1", fig("Quan sát hình bên ($ABCD$ là hình chữ nhật, $H$ nằm trên cạnh $AB$) rồi điền số:"
      + y("a", "Hình bên có \\makebox[3.2cm]{\\dotfill} hình tam giác.") + y("b", "Hình bên có \\makebox[3.2cm]{\\dotfill} hình tứ giác."), F_HCN, 0.58),
      "a) 3 – b) 3", "a) $3$ hình tam giác: $AHD$, $HBC$, $HDC$. b) $3$ hình tứ giác: $ABCD$, $AHCD$, $HBCD$.",
      "a) " + ng("ck1-2425-thanhhung2#4") + "; b) " + ng("ck1-2526-thanhuyen#4a") + " (cùng một hình, vẽ lại theo đề gốc)",
      ("Đếm hình tam giác, tứ giác", ["ck1-2425-thanhhung2#4", "ck1-2526-thanhuyen#4a"], 2, 3)),
    Q("Câu 4", 2, "1", "Đúng ghi Đ, sai ghi S vào ô trống:" + ds(["$9$ kg gấp $4$ lần được $63$ kg.", "$10$ l thêm $5$ l được $50$ l.", "$30$ mm bớt $2$ mm còn $28$ mm.", "$28$ ml giảm $4$ lần còn $7$ ml."]),
      "S – S – Đ – Đ", "a) \\textbf{S} ($9 \\times 4 = 36$ kg); b) \\textbf{S} ($10 + 5 = 15$ l); c) \\textbf{Đ}; d) \\textbf{Đ} ($28 : 4 = 7$). Mỗi ý $0{,}25$đ.",
      ng("ck1-2425-nguyenbinhkhiem#7"), ("Gấp, giảm, thêm, bớt với đơn vị đo", ["ck1-2425-nguyenbinhkhiem#7"], 2, 3)),
    Q("Câu 5", 2, "0,5", "Giá trị của biểu thức $42 : 7 + 10$ là: \\makebox[3.2cm]{\\dotfill}",
      "16", "$42 : 7 + 10 = 6 + 10 = 16$.", ng("ck1-2425-thanhhung2#8", "câu tự luận, chuyển sang điền kết quả"),
      ("Tính giá trị biểu thức (chia trước, cộng sau)", ["ck1-2425-thanhhung2#8"], 2, 2)),
    Q("Câu 6", 1, "0,5", "$45 : \\square = 5$. Số điền vào ô trống là: \\makebox[3.2cm]{\\dotfill}",
      "9", "$45 : 5 = 9$ nên số cần điền là $9$.", ng("ck1-2526-vinhbao#4a"),
      ("Tìm thành phần trong phép chia", ["ck1-2526-vinhbao#4a"], 1, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("165 + 25", "190"), ("230 - 150", "80"), ("203 \\times 4", "812"), ("865 : 5", "173")]),
      "190; 80; 812; 173", dt_sol([("165 + 25", "190"), ("230 - 150", "80"), ("203 \\times 4", "812"), ("865 : 5", "173")]),
      ng("ck1-2425-nguyenbinhkhiem#9"), ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2425-nguyenbinhkhiem#9"], 1, 7)),
    Q("Câu 8", 2, "2", "Trong vườn nhà bác Bình có $120$ cây cam, số cây chanh bằng số cây cam giảm đi $3$ lần. Hỏi trong vườn nhà bác Bình có tất cả bao nhiêu cây cam và cây chanh?",
      "160 cây", giai("Số cây chanh là: $120 : 3 = 40$ (cây) \\hfill \\textit{(0,75đ)}",
                      "Có tất cả số cây cam và cây chanh là: $120 + 40 = 160$ (cây) \\hfill \\textit{(0,75đ)}",
                      "Đáp số: $160$ cây. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2425-nguyenbinhkhiem#10"), ("Bài toán giải bằng hai bước tính (giảm đi rồi cộng)", ["ck1-2425-nguyenbinhkhiem#10"], 2, 8)),
    Q("Câu 9", 3, "1", y("a", "Điền dấu ($+$; $-$; $\\times$; $:$) thích hợp vào ô trống để được phép tính đúng: [[br]] $12 \\;\\square\\; 4 \\;\\square\\; 3 = 51$ \\qquad\\qquad $50 \\;\\square\\; 10 \\;\\square\\; 5 = 48$")
      + y("b", "Số tiếp theo trong dãy số $1$; $4$; $7$; $10$; \\dots\\ là:") + ops(["$15$", "$12$", "$13$", "$11$"]),
      "a) ×, + ; −, : – b) C", "a) $12 \\times 4 + 3 = 51$; $50 - 10 : 5 = 48$ ($0{,}5$đ). b) Chọn \\textbf{C}: hai số liền nhau hơn kém nhau $3$; $10 + 3 = 13$ ($0{,}5$đ).",
      "a) " + ng("ck1-2526-nguyenvantroi#10b") + "; b) " + ng("ck1-2526-thanhuyen#2a"),
      ("Điền dấu phép tính; dãy số theo quy luật", ["ck1-2526-nguyenvantroi#10b", "ck1-2526-thanhuyen#2a"], 3, 6)),
], "$\\square$ Đã đặt tính thẳng cột (Câu 7) & $\\square$ Câu 8 có câu lời giải và đáp số")

# ---------------------------------------------------------------- ÔN 2
DE["on2"] = ("Đề ôn số 2", [
    Q("Câu 1", 1, "1", y("a", "Biết số trừ là $36$, hiệu là $25$, số bị trừ là:") + ops(["$11$", "$61$", "$51$", "$41$"])
      + y("b", "$17 + 13 - 10 = \\dots$ Số điền vào chỗ chấm là:") + ops(["$40$", "$20$", "$30$"], 3),
      "a) B – b) B", "a) Chọn \\textbf{B}: số bị trừ $= 25 + 36 = 61$. b) Chọn \\textbf{B}: $30 - 10 = 20$.",
      "a) " + ng("ck1-2425-nguyenbinhkhiem#1") + "; b) " + ng("ck1-2425-thanhhung2#1"),
      ("Tìm số bị trừ; cộng, trừ trong phạm vi 1000", ["ck1-2425-nguyenbinhkhiem#1", "ck1-2425-thanhhung2#1"], 1, 3)),
    Q("Câu 2", 1, "1", y("a", "Trong phép tính $15 : 3 = 5$, số chia là:") + ops(["$15$", "$3$", "$5$"], 3)
      + y("b", "Có $40$ quả cam xếp vào các đĩa, mỗi đĩa $8$ quả. Hỏi xếp được mấy đĩa cam như vậy? [[br]] Trả lời: Xếp được \\makebox[3.2cm]{\\dotfill} đĩa cam."),
      "a) B – b) 5 đĩa", "a) Chọn \\textbf{B}. b) $40 : 8 = 5$ (đĩa).",
      "a) " + ng("ck1-2526-vinhbao#1a") + "; b) " + ng("ck1-2526-vinhbao#5"),
      ("Thành phần phép chia; bài toán chia", ["ck1-2526-vinhbao#1a", "ck1-2526-vinhbao#5"], 1, 3)),
    Q("Câu 3", 2, "1", y("a", "Hình vuông có bao nhiêu góc vuông?") + ops(["$3$", "$2$", "$4$", "$1$"])
      + fig(y("b", "Hình bên có mấy góc vuông?") + ops(["$3$", "$4$", "$5$", "$6$"], 2), F_KT1D, 0.55),
      "a) C – b) C", "a) Chọn \\textbf{C}. b) Chọn \\textbf{C}: $4$ góc vuông của hình chữ nhật $ABCD$ và góc vuông đỉnh $B$ của tam giác $BEC$.",
      "a) " + ng("ck1-2425-nguyenbinhkhiem#5") + "; b) " + ng("ck1-2526-khanhthien#1d", "hình chữ nhật ghép tam giác vuông, vẽ lại; trùng câu 5 đề TH Nguyễn Văn Trỗi, cùng đáp án 5"),
      ("Góc vuông, góc không vuông", ["ck1-2425-nguyenbinhkhiem#5", "ck1-2526-khanhthien#1d"], 2, 3)),
    Q("Câu 4", 1, "1", y("a", "$5$ cm $= \\dots$ mm. Số thích hợp điền vào chỗ chấm là:") + ops(["$50$ mm", "$5$ mm", "$500$ mm"], 3)
      + y("b", "Điền kết quả vào chỗ chấm: [[br]] $38$ g $+ 29$ g $- 30$ g $= \\makebox[3.2cm]{\\dotfill}$ \\qquad\\qquad $85$ mm $- 25$ mm $+ 20$ mm $= \\makebox[3.2cm]{\\dotfill}$"),
      "a) A – b) 37 g; 80 mm", "a) Chọn \\textbf{A}: $1$ cm $= 10$ mm. b) $37$ g; $80$ mm (ghi đủ đơn vị).",
      "a) " + ng("ck1-2425-thanhhung2#5") + "; b) " + ng("ck1-2526-vinhbao#3"),
      ("Mi-li-mét, gam: đổi và tính", ["ck1-2425-thanhhung2#5", "ck1-2526-vinhbao#3"], 1, 3)),
    Q("Câu 5", 2, "0,5", "Giá trị của biểu thức $118 + 168 - 32$ là: \\makebox[3.2cm]{\\dotfill}",
      "254", "$118 + 168 - 32 = 286 - 32 = 254$.", ng("ck1-2425-nguyenbinhkhiem#8", "ý a, chuyển sang điền kết quả"),
      ("Tính giá trị biểu thức (cộng, trừ)", ["ck1-2425-nguyenbinhkhiem#8"], 2, 2)),
    Q("Câu 6", 3, "0,5", "Biết thương là $5$, số chia là $6$, số dư là số dư lớn nhất có thể. Số bị chia là:" + ops(["$30$", "$11$", "$35$", "$16$"]),
      "C", "Chọn \\textbf{C}: số dư lớn nhất là $5$; số bị chia $= 5 \\times 6 + 5 = 35$.", ng("ck1-2526-donghoa#6b"),
      ("Phép chia có dư (tìm số bị chia)", ["ck1-2526-donghoa#6b"], 3, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("165 + 318", "483"), ("636 - 384", "252"), ("217 \\times 4", "868"), ("675 : 5", "135")]),
      "483; 252; 868; 135", dt_sol([("165 + 318", "483"), ("636 - 384", "252"), ("217 \\times 4", "868"), ("675 : 5", "135")]),
      ng("ck1-2526-phuluong#5"), ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2526-phuluong#5"], 1, 7)),
    Q("Câu 8", 2, "2", "Một cửa hàng gạo có $127$ kg gạo nếp. Số gạo tẻ gấp $3$ lần số gạo nếp. Hỏi cửa hàng có tất cả bao nhiêu ki-lô-gam gạo nếp và gạo tẻ?",
      "508 kg", giai("Cửa hàng có số ki-lô-gam gạo tẻ là: $127 \\times 3 = 381$ (kg) \\hfill \\textit{(0,75đ)}",
                     "Cửa hàng có tất cả số ki-lô-gam gạo là: $127 + 381 = 508$ (kg) \\hfill \\textit{(0,75đ)}",
                     "Đáp số: $508$ kg gạo. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2526-khanhthien#8"), ("Bài toán giải bằng hai bước tính (gấp lên rồi cộng)", ["ck1-2526-khanhthien#8"], 2, 8)),
    Q("Câu 9", 3, "1", y("a", "Lớp 3A tổ chức cho $34$ học sinh đi trải nghiệm bằng xe taxi, mỗi xe chở được $5$ bạn. Vậy lớp 3A phải thuê ít nhất \\makebox[3.2cm]{\\dotfill} xe để chở hết số học sinh đó.")
      + y("b", "Cho ba số $4$, $5$, $20$ và các dấu $\\times$, $:$, $=$. Hãy viết bốn phép tính đúng."),
      "a) 7 – b) 4 phép tính", "a) $34 : 5 = 6$ (dư $4$): $6$ xe chở $30$ bạn, còn $4$ bạn cần thêm $1$ xe. Thuê $7$ xe ($0{,}5$đ). b) $4 \\times 5 = 20$; $5 \\times 4 = 20$; $20 : 4 = 5$; $20 : 5 = 4$ (đủ 4 phép: $0{,}5$đ; 2–3 phép: $0{,}25$đ).",
      "a) " + ng("ck1-2526-donghoa#10a", "thêm chữ \"ít nhất\" cho chặt") + "; b) " + ng("ck2-2526-tayhung#TL4"),
      ("Phép chia có dư trong thực tế; quan hệ nhân – chia", ["ck1-2526-donghoa#10a", "ck2-2526-tayhung#TL4"], 3, 6)),
], "$\\square$ Đã đặt tính thẳng cột (Câu 7) & $\\square$ Câu 8 có câu lời giải và đáp số")

# ---------------------------------------------------------------- ÔN 3
DE["on3"] = ("Đề ôn số 3", [
    Q("Câu 1", 1, "1", y("a", "Đọc số: $509$: \\dotfill\\mbox{}")
      + y("b", "Phép tính nào sau đây có kết quả bé nhất?") + ops(["$4 \\times 3$", "$45 : 5$", "$7 \\times 2$", "$48 : 8$"]),
      "a) Năm trăm linh chín – b) D", "a) Năm trăm linh chín. b) Chọn \\textbf{D}: các kết quả là $12$; $9$; $14$; $6$.",
      "a) " + ng("ck2-2425-huuthanhb#1", "ý viết cách đọc số 509") + "; b) " + ng("ck1-2425-nguyenbinhkhiem#2"),
      ("Đọc số; so sánh kết quả bảng nhân, chia", ["ck2-2425-huuthanhb#1", "ck1-2425-nguyenbinhkhiem#2"], 1, 3)),
    Q("Câu 2", 2, "1", y("a", "Kết quả của phép chia $75 : 3$ là:") + ops(["$24$", "$15$", "$25$"], 3)
      + y("b", "Viết số thích hợp vào ô trống:") + "\\par\\centering " + SODO + "\\par\\raggedright",
      "a) C – b) 375; 372; 62", "a) Chọn \\textbf{C}: $75 : 3 = 25$. b) $125 \\times 3 = 375$; $375 - 3 = 372$; $372 : 6 = 62$ (đủ ba ô: $0{,}5$đ).",
      "a) " + ng("ck1-2425-thanhhung2#6") + "; b) " + ng("ck1-2526-donghoa#2b"),
      ("Chia số có hai chữ số; gấp lên, giảm đi một số lần", ["ck1-2425-thanhhung2#6", "ck1-2526-donghoa#2b"], 2, 3)),
    Q("Câu 3", 2, "1", fig(y("a", "Quan sát hình bên, điền vào chỗ chấm: [[br]] Hình tròn có tâm là \\makebox[3.2cm]{\\dotfill}, đường kính là \\makebox[3.2cm]{\\dotfill}"), F_TU1B, 0.6)
      + y("b", "Khối lập phương và khối hộp chữ nhật có gì giống nhau?") + ops(["Đều có $6$ mặt là hình chữ nhật, $8$ đỉnh, $12$ cạnh", "Đều có $6$ mặt là hình vuông, $8$ đỉnh, $12$ cạnh", "Đều có $6$ mặt, $8$ đỉnh, $12$ cạnh", "Đều có $6$ mặt, $6$ đỉnh, $12$ cạnh"], 1),
      "a) O; AB – b) C", "a) Tâm $O$; đường kính $AB$ ($MN$ không đi qua $O$ nên không phải đường kính). b) Chọn \\textbf{C}.",
      "a) " + ng("ck1-2526-thanhuyen#1b", "hình vẽ lại theo đề gốc") + "; b) " + NGUON["tt"] + ", câu 3a (đề trung tâm, không phải đề trường)",
      ("Hình tròn; khối lập phương, khối hộp chữ nhật", ["ck1-2526-thanhuyen#1b"], 2, 3)),
    Q("Câu 4", 1, "1", "Tính: \\qquad \\textbf{a)} $45$ g $: 5 = \\makebox[3.2cm]{\\dotfill}$ \\qquad\\qquad \\textbf{b)} $24$ ml $: 4 = \\makebox[3.2cm]{\\dotfill}$",
      "a) 9 g – b) 6 ml", "a) $9$ g; b) $6$ ml (thiếu đơn vị: không cho điểm ý đó).", ng("ck1-2526-vinhbao#8"),
      ("Tính với đơn vị gam, mi-li-lít", ["ck1-2526-vinhbao#8"], 1, 3)),
    Q("Câu 5", 2, "0,5", "Giá trị của biểu thức $(124 + 36) \\times 5$ là: \\makebox[3.2cm]{\\dotfill}",
      "800", "$(124 + 36) \\times 5 = 160 \\times 5 = 800$.", ng("ck1-2526-vinhbao#7", "ý a, chuyển sang điền kết quả"),
      ("Tính giá trị biểu thức có ngoặc", ["ck1-2526-vinhbao#7"], 2, 2)),
    Q("Câu 6", 3, "0,5", "Nếu ta gấp một số lên $3$ lần thì được tích của $5$ và $9$. Số đó là:" + ops(["$59$", "$95$", "$45$", "$15$"]),
      "D", "Chọn \\textbf{D}: tích của $5$ và $9$ là $45$; số đó là $45 : 3 = 15$.", ng("ck1-2526-donghoa#6a"),
      ("Gấp một số lên một số lần (tính ngược)", ["ck1-2526-donghoa#6a"], 3, 2)),
    Q("Câu 7", 1, "2", dat_tinh([("188 + 436", "624"), ("971 - 338", "633"), ("171 \\times 4", "684"), ("808 : 8", "101")]),
      "624; 633; 684; 101", dt_sol([("188 + 436", "624"), ("971 - 338", "633"), ("171 \\times 4", "684"), ("808 : 8", "101")]),
      "a, b) " + ng("ck1-2526-thanhuyen#5") + "; c, d) " + ng("ck1-2526-vinhbao#6"),
      ("Đặt tính cộng, trừ, nhân, chia trong phạm vi 1000", ["ck1-2526-thanhuyen#5", "ck1-2526-vinhbao#6"], 1, 7)),
    Q("Câu 8", 2, "2", "Một cửa hàng ngày thứ nhất bán được $84$ quyển sách. Số quyển sách bán được trong ngày thứ hai giảm đi $4$ lần so với ngày thứ nhất. Hỏi cả hai ngày cửa hàng đó bán được bao nhiêu quyển sách?",
      "105 quyển", giai("Ngày thứ hai bán được số quyển sách là: $84 : 4 = 21$ (quyển) \\hfill \\textit{(0,75đ)}",
                        "Cả hai ngày bán được số quyển sách là: $84 + 21 = 105$ (quyển) \\hfill \\textit{(0,75đ)}",
                        "Đáp số: $105$ quyển sách. \\hfill \\textit{(0,5đ)}"),
      ng("ck1-2526-nguyenvantroi#9"), ("Bài toán giải bằng hai bước tính (giảm đi rồi cộng)", ["ck1-2526-nguyenvantroi#9"], 2, 8)),
    Q("Câu 9", 3, "1", "Điền dấu $>$; $<$; $=$ thích hợp vào ô trống:"
      + y("a", "$615 + 121 - 247 \\;\\square\\; 528$") + y("b", "$573 + 505 : 5 \\;\\square\\; 630$"),
      "a) < – b) >", "a) $615 + 121 - 247 = 489$ và $489 < 528$ ($0{,}5$đ). b) $573 + 505 : 5 = 573 + 101 = 674$ và $674 > 630$ ($0{,}5$đ). \\textit{Bẫy ý b: cộng trước rồi chia.}",
      ng("ck1-2526-donghoa#8"), ("So sánh giá trị biểu thức", ["ck1-2526-donghoa#8"], 3, 6)),
], "$\\square$ Đã ghi đơn vị g, ml (Câu 4) & $\\square$ Câu 8 có câu lời giải và đáp số")


# =====================================================================
#                              DỰNG ĐỀ
# =====================================================================
def slug_de(k):
    return f"de-on-tap-cuoi-ki-1-so-{k[2:]}" if isinstance(k, str) else f"de-kiem-tra-cuoi-ki-1-de-{k}"


def dung_de(k):
    ten, qs, kiem = DE[k]
    b = [q["blk"] for q in qs]
    d = copy.deepcopy(BASE)
    on = isinstance(k, str)
    d.update({"slug": slug_de(k), "grade_label": "Lớp 3",
              "title": (f"Đề ôn tập cuối học kì I — {ten} (40 phút)" if on else f"Đề kiểm tra cuối học kì I — {ten} (40 phút)"),
              "eyebrow": ("ĐỀ ÔN TẬP" if on else "ĐỀ KIỂM TRA ĐỊNH KÌ") + f" CUỐI HỌC KÌ I · TOÁN 3 · {NAM}"})
    s = d["stages"]
    the = s[0]["blocks"][0]
    p1 = {"type": "para", "text": "\\textbf{PHẦN I. TRẮC NGHIỆM (5,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng hoặc làm theo yêu cầu.}\\par\\vspace{3pt}"}
    np = {"type": "para", "text": "\\newpage"}
    s[0]["blocks"] = [the, p1] + b[0:3] + [np]
    s[0]["teacher_note"] = "Trang 1: khung Điểm, Câu 1 đến Câu 3 (mỗi câu 2 ý)."
    s[1]["blocks"] = b[3:6] + [{"type": "para", "text": "\\par\\vspace{4pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (5,0 điểm)}"}, b[6],
                               {"type": "writelines", "variant": "oly", "count": 7},
                               {"type": "para", "text": "\\centerline{\\textit{\\footnotesize (Học sinh đặt tính thẳng cột và làm bài vào khung ô ly trên)}}"}, np]
    s[1]["teacher_note"] = "Trang 2: Câu 4 đến Câu 6, Câu 7 đặt tính (ô ly)."
    s[2]["blocks"] = [b[7], {"type": "writelines", "variant": "oly", "count": 12},
                      {"type": "para", "text": "\\centerline{\\textit{\\footnotesize (Học sinh trình bày câu lời giải, phép tính và đáp số vào khung ô ly trên)}}"}, np]
    s[2]["teacher_note"] = "Trang 3: Câu 8 bài toán hai bước (ô ly)."
    s[3]["blocks"] = [{"type": "para", "text": "\\noindent\\textbf{PHẦN II. TỰ LUẬN (tiếp theo)}"}, b[8],
                      {"type": "writelines", "variant": "oly", "count": 8}]
    s[3]["teacher_note"] = "Trang 4: Câu 9 tư duy (ô ly), phiếu tự kiểm tra."
    r = s[4]["blocks"]
    r[0] = dict(r[0], text=r[0]["text"].split("\\begin{tabular}")[0] + "\\begin{tabular}{p{7.5cm}p{7.5cm}}\n"
                + "$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã làm đủ cả hai ý a, b của Câu 1 -- 4 \\\\\n" + kiem + "\n\\end{tabular}\n\\end{tcolorbox}")
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / f"{slug_de(k)}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ ma trận
def pct(refs):
    if not isinstance(refs, list) or not refs:
        return None
    dang = cau(refs[0])["dang"]
    co = sum(1 for de in CK1 if any(x["dang"] == dang for x in BANK[de]["cau"]))
    return round(100 * co / len(CK1)), dang


def so(x):
    return f"{x:g}".replace(".", "{,}")


def tab(rows, head, cols):
    out = ["\\begin{center}\\scriptsize\\renewcommand{\\arraystretch}{1.1}", "\\begin{tabular}{" + cols + "}", "\\hline",
           " & ".join(f"\\textbf{{{h}}}" for h in head) + " \\tabularnewline \\hline"]
    out += [" & ".join(map(str, r)) + " \\tabularnewline \\hline" for r in rows]
    return "\n".join(out + ["\\end{tabular}", "\\end{center}"])


def dung_ma_tran(k):
    ten, qs, _ = DE[k]
    on = isinstance(k, str)
    ten_t = f"Đề ôn tập cuối học kì I — {ten}" if on else f"Đề kiểm tra cuối học kì I — {ten}"
    rows, tong, cds = [], {1: [0, 0], 2: [0, 0], 3: [0, 0]}, {}
    for q in qs:
        nd, refs, muc, ph = q["meta"]
        c0 = cau(refs[0])
        bais = sorted({cau(r)["bai"] for r in refs})
        p = pct(refs)
        lab = q["blk"]["label"].rstrip(".")
        rows.append([lab, f"{nd} (" + ("Bài " + ", ".join(map(str, [x for x in bais if x])) if any(bais) else "") + ("; toán tư duy" if 0 in bais else "") + ")", f"M{muc} -- {so(q['diem'])}đ", f"{so(ph)}′",
                     f"{p[0]}\\%" if p else "--", "\\tiny " + q["nguon"]])
        tong[muc][0] += 1; tong[muc][1] += q["diem"]
        cds.setdefault(c0["cd"], [0, 0]); cds[c0["cd"]][0] += 1; cds[c0["cd"]][1] += q["diem"]
    rows_m = [[f"Mức {m}", c, so(d) + "đ", f"{round(d * 10)}\\%"] for m, (c, d) in tong.items()]
    rows_cd = [[f"CĐ{c} {TEN_CD[c]}" if c else TEN_CD[0], v[0], so(v[1]) + "đ"] for c, v in sorted(cds.items())]
    tg = sum(q["meta"][3] for q in qs)
    head = (f"\\textbf{{MA TRẬN {'ĐỀ ÔN TẬP' if on else 'ĐỀ KIỂM TRA'} CUỐI HỌC KÌ I -- TOÁN 3 -- {ten.upper()}}} [[br]] "
            "Barem theo đề trung tâm lớp 3 (KNTT, T3-HKI-KNTT-01): 40 phút; Phần I $5{,}0$đ (Câu 1--4 mỗi câu 1đ gồm 2 ý; Câu 5--6 mỗi câu $0{,}5$đ); "
            "Phần II $5{,}0$đ (Câu 7 đặt tính 2đ, Câu 8 bài toán hai bước 2đ, Câu 9 tư duy 1đ). Chỉ ra Chủ đề 1--7 (kiến thức kì I). [[br]] "
            f"Cột \\textit{{\\% đề trường}}: tỉ lệ trong {len(CK1)} đề CK1 Toán 3 của các trường (2024--2026) có dạng của ý đầu. Tổng thời lượng ước tính: {so(tg)} phút.")
    s = copy.deepcopy(SKEL_MT)
    slug = (f"ma-tran-va-dap-an-on-tap-cuoi-ki-1-so-{k[2:]}" if on else f"ma-tran-va-dap-an-cuoi-ki-1-de-{k}")
    s.update({"slug": slug, "title": f"Ma trận đề và đáp án — {ten_t}", "grade_label": "Lớp 3",
              "eyebrow": f"SỔ TAY GIÁO VIÊN • LỚP 3 • {ten_t.upper()}"})
    st = s["stages"]
    st[0]["title"] = f"Ma trận {ten}"
    st[0]["blocks"] = [{"type": "para", "text": head + " [[br]] \\textbf{Bảng phân bố câu hỏi:}\n" + tab(rows, ["Câu", "Dạng bài (bài SGK KNTT)", "Mức -- điểm", "Phút", "\\% đề trường", "Nguồn câu"], "|c|p{4.6cm}|c|c|c|p{6.4cm}|")},
        {"type": "para", "text": "\\noindent\\begin{minipage}[t]{0.42\\linewidth}\\textbf{Tổng hợp theo mức (Thông tư 27):}\n" + tab(rows_m, ["Mức", "Số câu", "Điểm", "Tỉ lệ"], "|c|c|c|c|") + "\\end{minipage}\\hfill\\begin{minipage}[t]{0.55\\linewidth}\\textbf{Tổng hợp theo chủ đề SGK (theo ý đầu):}\n" + tab(rows_cd, ["Chủ đề", "Số câu", "Điểm"], "|p{5cm}|c|c|") + "\\end{minipage}"}]
    p1 = [q["blk"] for q in qs[:6]]
    st[1]["title"] = "Đáp án Phần I"
    st[1]["blocks"] = [{"type": "para", "text": "\\textbf{BẢNG ĐÁP ÁN PHẦN I (5,0 ĐIỂM)} [[br]]\n" + tab([[p["label"].rstrip("."), p["answer"].replace("×", "$\\times$").replace("−", "$-$"), so(q["diem"]) + "đ"] for p, q in zip(p1, qs)], ["Câu", "Đáp án", "Điểm"], "|c|p{9cm}|c|")},
        {"type": "para", "text": "\\textbf{GIẢI THÍCH CHI TIẾT} [[br]] " + " [[br]] ".join(f"\\textbf{{{p['label']}}} {p['solution']}" for p in p1)}]
    for i, (a, b) in ((2, (6, 7)), (3, (8, None))):
        st[i]["title"] = "Đáp án Câu 7 và Câu 8" if b else "Đáp án Câu 9"
        st[i]["blocks"] = [{"type": "para", "text": f"\\textbf{{ĐÁP ÁN {qs[x]['blk']['label'].rstrip('.').upper()}.}} {qs[x]['blk']['statement']} [[br]] {qs[x]['blk']['solution']}"} for x in (a, b) if x is not None]
    st[4]["title"] = "Hướng dẫn chấm"
    st[4]["blocks"] = [{"type": "para", "text": "\\textbf{HƯỚNG DẪN CHẤM CHUNG} \\begin{itemize}"
        "\\item Câu 1--4: mỗi ý a, b đúng $0{,}5$đ; ý có nhiều chỗ trống chia đều điểm."
        "\\item Câu 7: mỗi phép tính $0{,}5$đ (đặt tính thẳng cột $0{,}25$đ, kết quả $0{,}25$đ)."
        "\\item Câu 8: câu lời giải sai nhưng phép tính đúng vẫn cho điểm phép tính; thiếu hoặc sai đơn vị ở đáp số: trừ $0{,}25$đ."
        "\\item Câu 9: mỗi ý $0{,}5$đ, chỉ cần kết quả đúng."
        "\\item Điểm toàn bài làm tròn thành số nguyên theo Thông tư 27 ($\\ge 0{,}5$ làm tròn lên)."
        "\\end{itemize}"}]
    (DIR / f"{slug}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    return tong, tg


# ------------------------------------------------------------------ kiểm tra trùng + chạy
dung_ref = {}
for k, (ten, qs, _) in DE.items():
    assert abs(sum(q["diem"] for q in qs) - 10) < 1e-9, (k, sum(q["diem"] for q in qs))
    for q in qs:
        for r in q["meta"][1]:
            cau(r)  # ref phải có trong ngân hàng
            assert r not in dung_ref, f"Câu {r} dùng lại ở {k} và {dung_ref[r]}"
            dung_ref[r] = k
for k in DE:
    dung_de(k)
    tong, tg = dung_ma_tran(k)
    print(f"✓ {DE[k][0]}: M1 {tong[1][1]}đ · M2 {tong[2][1]}đ · M3 {tong[3][1]}đ · {tg} phút")
