#!/usr/bin/env python3
"""Sửa tay phiếu B ch.VI 9C sau khi ráp Gemini (13/11/2026). Idempotent.

    python3 scripts/gemini/sua_tay_phieu_b_9c.py [--ghi]

- Ô fill lồng $ trong $…$: "$\\Leftrightarrow [[fill:$…$]]$" → "$\\Leftrightarrow [[fill:…]]$", "=[[fill:$…$]]." → "=[[fill:…]]$.".
- Ví dụ 3: bỏ dòng "Vậy …" in lại đúng đáp án vừa khoét (lộ đáp án) — SGK tr.22 Ví dụ 2 cũng không có dòng này.
- Bài 3: bỏ dòng "Vậy …" lặp y dòng trên (khung + lời giải).
- Ví dụ 2: dấu nháy kép thừa cuối dòng.
- Ví dụ 6, Bài 7, Bài 8: "ĐKXĐ: $x>0$" sai khái niệm → ĐKXĐ là các mẫu khác 0 + mẫu thức chung.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = REPO / ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
               "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json")

DKXD = {  # nhãn → (dòng sai, dòng đúng)
    "Ví dụ 6.": ("ĐKXĐ: $x>0$.", "ĐKXĐ: $x\\ne 0$ và $x\\ne -15$.[[br]]\\hspace*{1.4em}Mẫu thức chung là $x(x+15)$."),
    "Bài 7.": ("ĐKXĐ: $x>0$.", "ĐKXĐ: $x\\ne 0$ và $x\\ne -20$."),
    "Bài 8.": ("ĐKXĐ: $x$ nguyên dương.", "ĐKXĐ: $x\\ne 0$ và $x\\ne -10$."),
}


def bo_dong(s, pat):
    return "[[br]]".join(d for d in s.split("[[br]]") if not re.search(pat, d))


def sua_chuoi(s):
    s = re.sub(r"\[\[fill:\$([^$\]]*)\$\]\]\$", r"[[fill:\1]]$", s)          # $… [[fill:$x$]]$
    s = re.sub(r"=\[\[fill:\$([^$\]]*)\$\]\]\.", r"=[[fill:\1]]$.", s)       # $…=[[fill:$x$]].  (thiếu $ đóng)
    s = s.replace("c=[[fill:-6]]$.\"", "c=[[fill:-6]]$.")
    # Ví dụ 5, 6: dòng hệ số ngay dưới lộ ô phương trình thu gọn ⇒ ô chuyển sang Δ', Δ
    s = s.replace("$\\Leftrightarrow [[fill:x^2+2x-8=0]]$", "$\\Leftrightarrow x^2+2x-8=0$")
    s = s.replace("\\Delta'=1^2-1\\cdot(-8)=9>0", "\\Delta'=1^2-1\\cdot(-8)=[[fill:9]]>0")
    s = s.replace("$\\Leftrightarrow [[fill:x^2+15x-1350=0]]$", "$\\Leftrightarrow x^2+15x-1350=0$")
    s = s.replace("=225+5400=5625>0", "=225+5400=[[fill:5625]]>0")
    # ô ngoài $ bọc $ (trinh_bay_gate: math lồng math) ⇒ đưa ô vào trong $
    s = re.sub(r"\[\[fill:\$x=([^$\]]*)\$\]\]", r"$x=[[fill:\1]]$", s)
    s = re.sub(r"\[\[fill:\$(\d+)\$ km/h\]\]", r"$[[fill:\1]]$ km/h", s)
    return s


def main():
    f = json.loads(SEED.read_text())
    doi = 0
    for st in f["stages"]:
        for b in st["blocks"]:
            nh = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, ""])[1]
            for k in ("text", "statement", "solution"):
                if not b.get(k):
                    continue
                v = sua_chuoi(b[k])
                if nh == "Ví dụ 3.":
                    v = bo_dong(v, r"^\\hspace\*\{1\.4em\}Vậy phương trình có hai nghiệm")
                if nh == "Bài 3.":
                    v = bo_dong(v, r"^\\hspace\*\{1\.4em\}Vậy phương trình có hai nghiệm")
                if nh in DKXD and k == "solution" or (nh == "Ví dụ 6." and k == "text"):
                    sai, dung = DKXD[nh]
                    v = v.replace(sai, dung)
                if nh == "Bài 4." and k == "statement":       # dòng nhân tử lộ ô phương trình thu gọn
                    v = v.replace("$\\Leftrightarrow x(x-5)=0$", "$\\Leftrightarrow x(\\ldots\\ldots)=0$")
                if k == "statement" and b.get("level") == 1:   # như phiếu A: cổng mật độ ô chỉ đếm [[blank]]
                    v = re.sub(r"(?:\\ldots)+", lambda m: "[[blank:1.6cm]]" if m.group(0).count(r"\ldots") <= 2
                               else "[[blank:6cm]]", v)
                if v != b[k]:
                    doi += 1
                    b[k] = v
    # soát còn sót
    txt = json.dumps(f, ensure_ascii=False)
    for pat in (r"\[\[fill:\$[^\]]*\$\]\]\$", r"ĐKXĐ: \$x>0\$", r"ĐKXĐ: \$x\$ nguyên"):
        n = len(re.findall(pat, txt))
        if n:
            print("✗ còn", pat, n)
    print("đổi", doi, "trường")
    if "--ghi" in sys.argv:
        SEED.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi")


if __name__ == "__main__":
    main()
