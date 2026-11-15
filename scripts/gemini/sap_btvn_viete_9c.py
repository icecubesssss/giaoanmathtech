#!/usr/bin/env python3
"""Phần máy móc khi sửa phiếu C Viète ch.VI 9C cho qua dan_dat_gate (Thầy duyệt 12/11/2026).

- BTVN: Bài 27 (điền khuyết cả bài giải) lên đầu phần BTVN, đánh số lại Bài 18–27.
- Ví dụ 6: đổi $x^2-5x+2=0$ (trùng Ví dụ 3) thành $x^2-7x+5=0$, (x1-x2)^2 = 29 (thêm dòng Δ bằng tay sau).
- Bật btvn_phieu_rieng.
Chạy một lần; chạy lại sẽ dừng vì không còn thấy trạng thái cũ.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
P = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
d = json.loads(P.read_text())

# 1. BTVN
st = next(s for s in d["stages"] if s["kind"] == "reflection")
bl = st["blocks"]
i27 = next(i for i, b in enumerate(bl) if b.get("label") == "Bài 27.")
i18 = next(i for i, b in enumerate(bl) if b.get("label") == "Bài 18.")
if "Điền vào chỗ chấm" not in bl[i27]["statement"]:
    sys.exit("Bài 27 không còn là bài điền bài giải — đã chạy rồi?")
b27 = bl.pop(i27)
bl.insert(i18, b27)
so = 18
for b in bl:
    if b.get("type") == "problem" and b.get("tier") == "btvn":
        n = int(b["label"].split()[1].rstrip("."))
        if 18 <= n <= 27:
            b["label"] = f"Bài {so}."
            so += 1
assert so == 28, so
for s in d["stages"]:
    if "teacher_note" in s:
        s["teacher_note"] = s["teacher_note"].replace("chữa Bài 27 và Bài 34", "chữa Bài 18 và Bài 34")

# 2. Ví dụ 6
for s in d["stages"]:
    for b in s["blocks"]:
        t = b.get("text", "")
        if "\\textbf{Ví dụ 6.}" in t:
            moi = (t.replace("$x^2-5x+2=0$", "$x^2-7x+5=0$")
                    .replace("$x_1+x_2=5$; $x_1x_2=2$", "$x_1+x_2=7$; $x_1x_2=5$")
                    .replace("5^2-4\\cdot 2=25-8=17", "7^2-4\\cdot 5=49-20=29")
                    .replace("(x_1-x_2)^2=17$", "(x_1-x_2)^2=29$"))
            assert moi.count("29") == 2 and "x^2-5x+2" not in moi, moi
            b["text"] = moi

# 3. cờ
d["btvn_phieu_rieng"] = True
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("Đã ghi", P.relative_to(REPO))
