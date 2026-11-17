#!/usr/bin/env python3
"""Sửa tay sau soát đầu ra Gemini — phiếu G ch.IX 9C (mỗi thay thế assert khớp đúng 1 lần)."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lap_phieu_h_ch9_9c import REPO, SEED  # noqa: E402

SUA = [  # (nhãn khối hoặc title, trường, cũ, mới)
    ("Bài 2.", "statement", "(kề bù, $H$ thuộc $CE$, Hình 4)",
     "($\\widehat{AEC}$ kề bù với $\\widehat{BEC}$, $H$ thuộc đoạn $CE$, Hình 4)"),
    ("Bài 2.", "statement", "(kề bù, $H$ thuộc $BD$, Hình 4)",
     "($\\widehat{ADB}$ kề bù với $\\widehat{BDC}$, $H$ thuộc đoạn $BD$, Hình 4)"),
    ("Bài 2.", "statement", "$\\Rightarrow E$ thuộc đường tròn đường kính $AH$.",
     "$\\Rightarrow E$ thuộc đường tròn đường kính $[[blank:1.1cm]]$."),
    ("Bài 2.", "statement", "Vậy tứ giác $AEHD$ nội tiếp đường tròn đường kính $AH$, tâm là [[blank:3.2cm]] của $AH$.",
     "Vậy tứ giác $AEHD$ nội tiếp đường tròn đường kính $[[blank:1.1cm]]$, tâm là [[blank:3.2cm]] của đoạn thẳng đó."),
    ("Bài 2.", "answer", "góc nội tiếp chắn nửa đường tròn, $90^\\circ$, $90^\\circ$, $AH$, trung điểm,",
     "a) góc nội tiếp chắn nửa đường tròn, $90^\\circ$, $AH$, $90^\\circ$, $AH$, $AH$, trung điểm, b)"),
    ("Bài 3.", "statement", "$(O; R)$", "$(O;R)$"),
    ("Bài 3.", "statement_slide", "$(O; R)$", "$(O;R)$"),
    ("Bài 3.", "statement", "$\\Rightarrow D$ thuộc đường tròn đường kính $AB$.",
     "$\\Rightarrow D$ thuộc đường tròn đường kính $[[blank:1.1cm]]$."),
    ("Bài 3.", "answer", "vuông, $AB$, $AB$, $90^\\circ$,", "a) vuông, $AB$, $AB$, $AB$, b) $90^\\circ$,"),
    ("BTVN 3.", "answer", "(kề bù, $N$ thuộc đoạn $BC$, Hình 10)",
     "(kề bù với $\\widehat{MNC}$, $N$ thuộc đoạn $BC$, Hình 10)"),
    ("BTVN 3.", "answer", "(kề bù, $D$ thuộc đường thẳng $BM$, Hình 10)", "($M$ thuộc đoạn $BD$, Hình 10)"),
    ("Ví dụ 2.", "text", "(Hình 5) $\\Rightarrow \\widehat{DNE} = \\widehat{DAC}$.",
     "(Hình 5) $\\Rightarrow \\widehat{DNE} = \\widehat{DAC}$ (dòng trên)."),
    ("Bài 4.", "statement", "gọi $M$ là trung điểm của $BC$", "gọi trung điểm của $BC$ là $M$"),
    ("BTVN 4.", "statement", "Gọi $M$ là trung điểm của đoạn thẳng $BC$.", "Gọi trung điểm của đoạn thẳng $BC$ là $M$."),
    ("Ví dụ 2.", "text", "[[fill:hai góc nội tiếp cùng chắn cung $DT$]]", "[[fill:hai góc nội tiếp cùng chắn một cung]]"),
    ("Bài 4.", "answer", "b) Nối $CK$. $\\widehat{ACK}", "b) Nối $CK$.[[br]]$\\widehat{ACK}"),
    ("Ví dụ 1.", "text", "$\\Rightarrow M$ thuộc đường tròn đường kính $ID$.", "$\\Rightarrow M$ thuộc đường tròn đường kính $[[fill:ID]]$."),
]


def main():
    p = REPO / SEED
    f = json.loads(p.read_text())
    for nh, k, cu, moi in SUA:
        hit = 0
        for s in f["stages"]:
            for b in s["blocks"]:
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                ten = b.get("label") or b.get("title") or (m.group(1) if m else "")
                if ten.strip() != nh:
                    continue
                n = (b.get(k) or "").count(cu)
                if n:
                    b[k] = b[k].replace(cu, moi)
                    hit += n
        assert hit == 1, f"{nh}/{k}: khớp {hit} lần — {cu[:50]}"
    p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("đã sửa", len(SUA), "chỗ")


if __name__ == "__main__":
    main()
