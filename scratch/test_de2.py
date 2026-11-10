import json
import re
from pathlib import Path

p = Path("inputs/seeds/lop-5/de-cuoi-ki-1/de-kiem-tra-cuoi-ki-1-de-2.json")
data = json.loads(p.read_text(encoding="utf-8"))

# Compact header box
header_box = (
    "\\begin{tabular}{|p{3.2cm}|p{12.4cm}|}\n"
    "\\hline\n"
    "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
    "\\vspace{0.2cm} & \\vspace{0.2cm} \\tabularnewline\n"
    "\\hline\n"
    "\\end{tabular}\n"
    "\\par\\vspace{1pt}"
)
tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Khoanh vào chữ cái đặt trước câu trả lời đúng:}"

data["stages"][0]["blocks"][0]["text"] = header_box
data["stages"][0]["blocks"][1]["text"] = tn_intro

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Updated de-2 with compact header!")

