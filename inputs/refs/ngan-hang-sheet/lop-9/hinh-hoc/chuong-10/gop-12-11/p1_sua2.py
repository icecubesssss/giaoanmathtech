#!/usr/bin/env python3
"""Bước 2 (sau p1_sua.py): nhãn hình BTVN 5 (ly r=4, nước 12, bỏ chiều cao ly) và BTVN 6 (trụ r=6, h=15)."""
import json
from pathlib import Path
P = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/phieu-a-hinh-tru-hinh-non-hinh-cau.json")
d = json.loads(P.read_text())
bt = {b.get("label"): b for b in d["stages"][4]["blocks"]}
f = bt["BTVN 5."]["figure"]
assert "{$2{,}5$}" in f["tikz"]
f["tikz"] = (f["tikz"].replace("  \\node[right, font=\\scriptsize] at (0.12,1) {$15$};\n", "")
             .replace("{$2{,}5$}", "{$4$ cm}").replace("{$10$}", "{$12$ cm}"))
f = bt["BTVN 6."]["figure"]
assert "{$25$}" in f["tikz"]
f["tikz"] = (f["tikz"].replace("\\node[right, font=\\scriptsize] at (0.12,1) {$25$};", "\\node[right, font=\\scriptsize] at (1.02,1) {$15$ cm};")
             .replace("{$12$}", "{$6$ cm}"))
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("ok")
# bổ sung: nhãn 4 cm Bài 3 tách khỏi trục nét đứt
d = json.loads(P.read_text())
b3 = next(b for b in d["stages"][2]["blocks"] if b.get("label") == "Bài 3.")
b3["figure"]["tikz"] = b3["figure"]["tikz"].replace("at (0.02,0.42) {$4$ cm}", "at (0.1,0.38) {$4$ cm}")
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
# bổ sung: \nhanly chỉ định nghĩa cho thẻ theory (slide nổ Undefined control sequence) ⇒ hộp khác dùng \textbf
d = json.loads(P.read_text())
for s in d["stages"]:
    for b in s["blocks"]:
        if b.get("type") == "noted" and b.get("variant") != "theory" and "\\nhanly{" in b.get("text", ""):
            b["text"] = b["text"].replace("\\nhanly{", "\\textbf{")
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
# bổ sung: đề ghi đủ số đo; khung vẽ đúng câu dẫn; Ví dụ 3 thêm ô điền
d = json.loads(P.read_text())
lt1 = {b.get("label"): b for b in d["stages"][2]["blocks"]}
b = lt1["Bài 2."]
b["statement"] = b["statement"].replace("của hình trụ ở Hình 7.", "của hình trụ có bán kính đáy $5$ cm, chiều cao $10$ cm (Hình 7).")
b = lt1["Bài 7."]
b["statement"] = b["statement"].replace("Vẽ phác ly nước vào vở,", "Vẽ phác ly nước vào khung dưới đây,")
x = next(x for x in d["stages"][3]["blocks"] if x.get("variant") == "example" and x["text"].startswith("\\textbf{Ví dụ 3.}"))
for a, z in (("$V_{\\text{cốc}} = \\pi r^2h", "$V_{\\text{cốc}} = [[fill:\\pi r^2h]]"), ("$R = 4 : 2 = 2$", "$R = 4 : 2 = [[fill:2]]$")):
    assert a in x["text"], a
    x["text"] = x["text"].replace(a, z, 1)
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
