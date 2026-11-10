import json
import re
import sys
sys.path.insert(0, ".")

from pathlib import Path
from scripts.de_chinh_thuc_ck1_lop5_kntt import DE, make_mt_json

D = DE["de1"]
source_p = Path("inputs/seeds/lop-5/de-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-de-1.json")

# ─────────────────── TRANG 1: Top Card + Điểm + Câu 1..6 ───────────────────
header_box = (
    "\\begin{tabular}{|p{3.5cm}|p{12.2cm}|}\n"
    "\\hline\n"
    "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
    "\\vspace{2.0cm} & \\vspace{2.0cm} \\tabularnewline\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\par\\vspace{8pt}"
)
tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}\\par\\vspace{3pt}"

p1_blocks = [
    {"type": "para", "text": header_box},
    {"type": "para", "text": tn_intro}
]
for c in D["tn"][:6]:
    p1_blocks.append({
        "type": "problem",
        "label": f"Câu {c['cau']}.",
        "level": c["level"],
        "statement": c["statement"] + "\\par\\vspace{2pt}",
        "options": c["options"],
        "answer": c["answer"],
        "solution": c["solution"],
        "tier": "onclass"
    })
p1_blocks.append({"type": "para", "text": "\\newpage"})

stage1 = {
    "kind": "review",
    "number": 1,
    "title": "",
    "blocks": p1_blocks,
    "teacher_note": "Trang 1: Top Card, khung Điểm và 6 câu trắc nghiệm (Câu 1 đến Câu 6)."
}

# ─────────────────── TRANG 2: Câu 7, 8 + Bài 1 (Lưới ô ly to 12cm) ───────────────────
p2_blocks = []
for c in D["tn"][6:]:
    p2_blocks.append({
        "type": "problem",
        "label": f"Câu {c['cau']}.",
        "level": c["level"],
        "statement": c["statement"] + "\\par\\vspace{2pt}",
        "options": c["options"],
        "answer": c["answer"],
        "solution": c["solution"],
        "tier": "onclass"
    })

p2_blocks.append({
    "type": "para",
    "text": "\\par\\vspace{4pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
})

# Bài 1: Đặt tính rồi tính in 2 dòng thoáng
b1 = D["bai"][0]
parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", b1["statement"])
intro = parts[0].strip()
items = {}
for i in range(1, len(parts), 2):
    items[parts[i].strip()] = parts[i+1].strip()

b1_statement_4page = (
    f"{intro} [[br]]\n"
    f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{a)}} {items.get('a)', '')} \\\\[5pt]\n"
    f"\\textbf{{c)}} {items.get('c)', '')}\n"
    f"\\end{{minipage}}\\hfill\n"
    f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{b)}} {items.get('b)', '')} \\\\[5pt]\n"
    f"\\textbf{{d)}} {items.get('d)', '')}\n"
    f"\\end{{minipage}}"
)

p2_blocks.append({
    "type": "problem",
    "label": b1["label"],
    "level": b1["level"],
    "statement": b1_statement_4page,
    "solution": " [[br]] ".join(b1["dap_an"]),
    "tier": "onclass"
})
# Khung ô ly 12cm
p2_blocks.append({"type": "writelines", "variant": "oly", "count": 12})
p2_blocks.append({
    "type": "para",
    "text": "\\centerline{\\textit{\\footnotesize (Học sinh đặt tính thẳng hàng dấu phẩy và làm bài vào khung ô ly trên)}}"
})
p2_blocks.append({"type": "para", "text": "\\newpage"})

stage2 = {
    "kind": "concept",
    "number": 2,
    "title": "",
    "blocks": p2_blocks,
    "teacher_note": "Trang 2: Câu 7, Câu 8 và Bài 1 Đặt tính rồi tính với khung ô ly 12cm."
}

# ─────────────────── TRANG 3: Bài 2 + Bài 3 + Bài 4 (Lưới ô ly 8cm) ───────────────────
b2 = D["bai"][1]
parts2 = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", b2["statement"])
intro2 = parts2[0].strip()
items2 = {}
for i in range(1, len(parts2), 2):
    items2[parts2[i].strip()] = parts2[i+1].strip()

b2_statement_4page = (
    f"{intro2} [[br]]\n"
    f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{a)}} {items2.get('a)', '')}\n"
    f"\\end{{minipage}}\\hfill\n"
    f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{b)}} {items2.get('b)', '')}\n"
    f"\\end{{minipage}}"
)

b3 = D["bai"][2]
parts3 = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", b3["statement"])
intro3 = parts3[0].strip()
items3 = {}
for i in range(1, len(parts3), 2):
    items3[parts3[i].strip()] = parts3[i+1].strip()

b3_statement_4page = (
    f"{intro3} [[br]]\n"
    f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{a)}} {items3.get('a)', '')} [[br]]\n"
    f"\\textbf{{b)}} {items3.get('b)', '')}\n"
    f"\\end{{minipage}}\\hfill\n"
    f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
    f"\\textbf{{c)}} {items3.get('c)', '')} [[br]]\n"
    f"\\textbf{{d)}} {items3.get('d)', '')}\n"
    f"\\end{{minipage}}"
)

b4 = D["bai"][3]

p3_blocks = [
    {
        "type": "problem",
        "label": b2["label"],
        "level": b2["level"],
        "statement": b2_statement_4page,
        "solution": " [[br]] ".join(b2["dap_an"]),
        "tier": "onclass"
    },
    {"type": "writelines", "variant": "oly", "count": 4},
    {
        "type": "problem",
        "label": b3["label"],
        "level": b3["level"],
        "statement": b3_statement_4page,
        "solution": " [[br]] ".join(b3["dap_an"]),
        "tier": "onclass"
    },
    {
        "type": "problem",
        "label": b4["label"],
        "level": b4["level"],
        "statement": b4["statement"],
        "solution": " [[br]] ".join(b4["dap_an"]),
        "tier": "onclass"
    },
    {"type": "writelines", "variant": "oly", "count": 8},
    {
        "type": "para",
        "text": "\\centerline{\\textit{\\footnotesize (Học sinh trình bày câu lời giải, phép tính và đáp số vào khung ô ly trên)}}"
    },
    {"type": "para", "text": "\\newpage"}
]

stage3 = {
    "kind": "practice1",
    "number": 3,
    "title": "",
    "blocks": p3_blocks,
    "teacher_note": "Trang 3: Bài 2 (ô ly 4cm), Bài 3 (điền khuyết) và Bài 4 (ô ly 8cm)."
}

# ─────────────────── TRANG 4: Bài 5 + Bảng tự kiểm tra + HẾT ───────────────────
b5 = D["bai"][4]
checklist_box = (
    "\\par\\vspace{8pt}\n"
    "\\noindent\\begin{tcolorbox}[enhanced, colback=neutral!30, colframe=brand!60, boxrule=0.6pt, arc=3pt, left=8pt, right=8pt, top=5pt, bottom=5pt]\n"
    "\\small\n"
    "\\textbf{PHIẾU TỰ KIỂM TRA BÀI LÀM TRƯỚC KHI NỘP} [[br]]\n"
    "\\textit{(Em tự đánh dấu $\\checkmark$ vào ô vuông sau khi hoàn thành):} \\par\\vspace{3pt}\n"
    "\\begin{tabular}{p{7.5cm}p{7.5cm}}\n"
    "$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã khoanh đủ 8 câu trắc nghiệm \\\\\n"
    "$\\square$ Đã đặt tính thẳng hàng dấu phẩy (Bài 1) & $\\square$ Đã rút gọn kết quả phân số (Bài 2) \\\\\n"
    "$\\square$ Đã điền đủ đơn vị ở Bài 3 và Bài 4 & $\\square$ Đã kiểm tra lại phép tính Bài 5\n"
    "\\end{tabular}\n"
    "\\end{tcolorbox}"
)

het_note = (
    "\\par\\vspace{8pt}\n"
    "\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}\n"
    "\\par\\vspace{3pt}\n"
    "\\centerline{\\textit{\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}"
)

p4_blocks = [
    {
        "type": "para",
        "text": "\\noindent\\textbf{PHẦN II. TỰ LUẬN (tiếp theo)}"
    },
    {
        "type": "problem",
        "label": b5["label"],
        "level": b5["level"],
        "statement": b5["statement"],
        "solution": " [[br]] ".join(b5["dap_an"]),
        "tier": "onclass"
    },
    {"type": "writelines", "variant": "oly", "count": 9}
]

stage4 = {
    "kind": "practice2",
    "number": 4,
    "title": "",
    "blocks": p4_blocks,
    "teacher_note": "Trang 4: Bài 5 (ô ly 9cm)."
}

p5_blocks = [
    {"type": "para", "text": checklist_box},
    {"type": "para", "text": het_note}
]

stage5 = {
    "kind": "reflection",
    "number": 5,
    "title": "",
    "blocks": p5_blocks,
    "teacher_note": "Trang 4: Bảng tự kiểm tra bài làm và Lời chúc kết bài."
}

test_data = {
    "slug": D["slug_de"],
    "title": f"Đề kiểm tra cuối học kì I — Đề {D['so']} (40 phút)",
    "eyebrow": D["header_eyebrow"],
    "grade_label": "Lớp 5",
    "class_tier": "",
    "theme": "de_thi",
    "stages": [stage1, stage2, stage3, stage4, stage5]
}

source_p.write_text(json.dumps(test_data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Wrote tuned test 4-page layout!")
