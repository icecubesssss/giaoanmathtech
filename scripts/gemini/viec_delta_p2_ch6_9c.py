#!/usr/bin/env python3
"""Việc Gemini đợt 5 — Phiếu 2 ch.VI 9C (17/11/2026): Thầy "Bài 11–16 cần tính Delta xác định nghiệm trước rồi mới
có mấy câu dưới". Đề mới ở viec_clean_p2_ch6_9c.DE_MOI (Claude chốt); Gemini viết lại lời giải 6 bài.

    .venv/bin/python scripts/gemini/viec_delta_p2_ch6_9c.py && python3 scripts/gemini/tho.py --mot delta-p2-ch6-9c
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_clean_p2_ch6_9c import MODEL, PROMPT, REPO, SEED, ban_cu  # noqa: E402

VID = "delta-p2-ch6-9c"
THEM = r'''
### Riêng đợt này (6 bài 11–16)
- Ý "a) Tính $\Delta$." trả lời một dòng: "Ta có $\Delta=…>0$ nên phương trình có hai nghiệm phân biệt $x_1$, $x_2$." (Δ: Bài 11 là $53$, Bài 12 là $8$, Bài 13 là $41$, Bài 14 là $40$, Bài 15 là $29$.) Các ý sau KHÔNG lặp lại điều kiện có nghiệm (Bài 15 bỏ dòng $a\cdot c<0$ ở ý cuối).
- Bài 16: a) thay $x=\dfrac{3-\sqrt5}{2}$: $\left(\dfrac{3-\sqrt5}{2}\right)^2-3\cdot\dfrac{3-\sqrt5}{2}+a=0$, tính ra $\dfrac{7-3\sqrt5}{2}-\dfrac{9-3\sqrt5}{2}+a=0$, $a=1$. b) $a=1$: $\Delta=(-3)^2-4\cdot1\cdot1=5>0$, hai nghiệm phân biệt. c) $x_1+x_2=3$, $x_1x_2=1$. d) Theo câu c), $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=9-2=7$, dòng "Vậy" riêng.
- Đánh nhãn ý đúng như đề mới (a, b, c, d).
'''


def main():
    nh = {f"Bài {i}." for i in range(11, 17)}
    v = {"id": VID, "model": MODEL, "prompt": PROMPT.replace("Trả về MỌI bài có dưới đây.", "Trả về MỌI bài có dưới đây.\n" + THEM)
         + ban_cu(nh) + "\n", "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "delta-p2-ch6-9c", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
