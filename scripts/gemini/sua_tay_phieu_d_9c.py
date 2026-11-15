#!/usr/bin/env python3
"""Sửa máy móc sau khi ráp phiếu D ch.VI 9C (13/11/2026) — lỗi Gemini để lại, không đổi nội dung toán.

    .venv/bin/python scripts/gemini/sua_tay_phieu_d_9c.py [--ghi]

1. Dòng có số `$` lẻ (quên `$` đóng sau ô `[[fill:…]]` hoặc `\\ldots\\ldots` cuối dòng) ⇒ thêm `$` trước dấu chấm cuối.
2. `[[fill:$X$]]` ngoài công thức ⇒ `$[[fill:X]]$` (trinh_bay_gate: math lồng math làm Tectonic chết).
3. "Cho phương trình đã cho. " (câu vô nghĩa ở đề chung Bài 7, 8) ⇒ "Với mỗi phương trình sau, g…".
4. "…$, nên $…" (hai chữ "nên" một dòng) ⇒ tách dòng "Ta có $…".
6. Bài NB: `\\ldots\\ldots` ⇒ `[[blank:1.6cm]]` (luật 09/10: mọi ô đi qua \\blank, chấm đậm in được).
7. Ví dụ: ô [[fill:X]] (X chứa $x_1$) mà dòng dưới in lại "(X)" ⇒ khoét luôn "([[fill:X]])".
8. Dòng "Nhắc lại kiến thức của Bài 20." mồ côi cuối trang 1 ⇒ gộp vào đầu hộp note.
5. Ví dụ 5, 8, 9: bỏ ô ở dòng Viète vì dòng dưới in lại đúng số đó (vi_du_gate: lộ đáp án).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = REPO / "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json"
THUT = r"\hspace*{1.4em}"


def so_dola(s):
    return len(re.findall(r"(?<!\\)\$", s))


def sua_dong(line):
    if so_dola(line) % 2 == 0:
        return line
    m = re.match(r"^(.*?)(\.?)(\s*)$", line, re.S)
    return m.group(1) + "$" + m.group(2) + m.group(3)


def sua_chuoi(s, nhan):
    cu = s
    s = "[[br]]".join(sua_dong(l) for l in s.split("[[br]]"))
    s = re.sub(r"\[\[fill:\$([^$\]]*)\$\]\]", r"$[[fill:\1]]$", s)
    s = s.replace("Cho phương trình đã cho. Gọi", "Với mỗi phương trình sau, gọi")
    s = s.replace("$, nên $", f"$.[[br]]{THUT}Ta có $")
    s = re.sub(r"\\ldots\\ldots(\\ )?", "[[blank:1.6cm]]", s)
    if nhan in ("Ví dụ 5.", "Ví dụ 8.", "Ví dụ 9."):
        s = re.sub(r"(\\begin\{cases\}.*?\\end\{cases\})",
                   lambda m: re.sub(r"\[\[fill:([^\]]*)\]\]", r"\1", m.group(1)), s, count=1, flags=re.S)
    if nhan.startswith("Ví dụ"):
        for X in set(re.findall(r"\[\[fill:([^\]]*x_1[^\]]*)\]\]", s)):
            s = s.replace(f"({X})", f"([[fill:{X}]])")
    return s, s != cu


def main():
    f = json.loads(SEED.read_text())
    n = 0
    rv = f["stages"][0]
    hd = [b for b in rv["blocks"] if b.get("type") == "para" and "Nhắc lại kiến thức" in b.get("text", "")]
    if hd:
        note = next(b for b in rv["blocks"] if b.get("type") == "noted")
        note["text"] = hd[0]["text"] + "[[br]]" + note["text"]
        rv["blocks"].remove(hd[0])
        print("gộp tiêu đề Nhắc lại vào hộp")
    for st in f["stages"]:
        for b in st["blocks"]:
            nhan = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, ""])[1]
            for k in ("text", "statement", "solution"):
                if isinstance(b.get(k), str):
                    b[k], doi = sua_chuoi(b[k], nhan)
                    if doi:
                        n += 1
                        print("sửa", nhan, k)
                    for i, l in enumerate(b[k].split("[[br]]")):
                        if so_dola(l) % 2:
                            print("  ✗ còn $ lẻ:", nhan, k, i, l[-80:])
    print(f"{n} trường đã sửa")
    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED.relative_to(REPO))


if __name__ == "__main__":
    main()
