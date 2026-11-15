#!/usr/bin/env python3
"""Phiếu B ch.VI 9C (13/11/2026) — sửa 5 cảnh báo spec_gate nhỏ, KHÔNG đổi đề/đáp số:
  - sgk_style: Ví dụ 1–3 thiếu câu "Vậy …" ⇒ dòng kết của mỗi ý đổi thành "Vậy …";
    khung NB đi theo (Bài 1, 2, 3 trên lớp + Bài 9, 10, 11 BTVN) đổi cùng kiểu cho khớp "như Ví dụ N".
  - vi_du_gate: Ví dụ 4, 5 ô điền ở trên nhưng dòng dưới in sẵn số đó.
Sinh HAI việc giống hệt nhau, khác model (flash vs hydrogen) để so chất lượng/thời gian/token.

    python3 scripts/gemini/viec_vay_phieu_b_9c.py
    python3 scripts/gemini/tho.py --tien-to vay-9c-ch6-phieu-b- --song-song 2
    python3 scripts/gemini/ap_sua_phieu.py vay-9c-ch6-phieu-b-hydrogen [--ghi]
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json")
LABELS = [f"Ví dụ {i}." for i in range(1, 6)] + ["Bài 1.", "Bài 2.", "Bài 3.", "Bài 9.", "Bài 10.", "Bài 11."]
MODELS = {"flash": "gemini-3.8-flash-high", "hydrogen": "gemini-4-hydrogen-medium"}

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (chương VI, "Phương trình chứa ẩn ở mẫu quy về phương trình bậc hai", SGK Kết nối tri thức, lớp tầng C). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt. Đây là việc SỬA NHỎ: chỉ đổi đúng các dòng được nêu, mọi chữ/công thức khác GIỮ NGUYÊN từng ký tự (kể cả [[br]], \hspace*{1.4em}, \ldots\ldots, nguồn đề).

## Việc 1 — câu kết "Vậy" cho Ví dụ 1, 2, 3 (dòng cuối của MỖI ý phải bắt đầu bằng "Vậy")
- Ví dụ 1 (mỗi ý): dòng "Vì <điều kiện các mẫu>" đổi thành "Ta có <điều kiện các mẫu>." (bỏ chữ "Vì", thêm dấu chấm cuối), dòng "nên ĐKXĐ của phương trình là …" đổi thành "Vậy ĐKXĐ của phương trình là …" (giữ nguyên các ô [[fill:…]]).
- Ví dụ 2: dòng cuối "Phương trình bậc hai nhận được có $a=…$, $b=…$, $c=…$." đổi thành "Vậy phương trình bậc hai nhận được có $a=…$, $b=…$, $c=…$." (giữ ô).
- Ví dụ 3 (mỗi ý): dòng "Ta có $a=…$, $b=…$, $c=…$ và $a+b+c=…=0$" thêm dấu chấm cuối dòng, dòng "nên phương trình có hai nghiệm …" đổi thành "Vậy phương trình có hai nghiệm …" (giữ ô).
- Khung bài NB đi theo ví dụ ("làm đủ các bước như Ví dụ N") đổi CÙNG KIỂU cho khớp, cả "statement" (khung có \ldots\ldots) lẫn "solution":
  Bài 1. và Bài 9. theo Ví dụ 1 · Bài 2. và Bài 10. theo Ví dụ 2 · Bài 3. và Bài 11. theo Ví dụ 3.
  Chỉ đổi chữ nối ("Vì"→"Ta có …." / "nên"→"Vậy" / thêm "Vậy" đầu dòng hệ số). Chỗ chấm, số, nguồn đề giữ nguyên. Ý nào của bài khác mẫu (ví dụ có dòng "Ta có $x^2-16=\ldots\ldots$" phân tích mẫu) thì giữ dòng đó, chỉ đổi hai dòng cuối như trên.

## Việc 2 — Ví dụ 4, 5: ô điền ở trên nhưng dòng dưới in sẵn đúng số đó (lộ đáp án)
- Ví dụ 4: ô "$x\ne [[fill:1]]$" ở dòng ĐKXĐ, nhưng dòng nhẩm in sẵn "$x_1=1$" và dòng đối chiếu in "$x_1=1$".
  Sửa: dòng nhẩm thành "…nên phương trình này có hai nghiệm $x_1=[[fill:1]]$ và $x_2=\dfrac{c}{a}=[[fill:-\dfrac{1}{2}]]$." Dòng đối chiếu thành "Giá trị $x_1$ [[fill:không thỏa mãn]] ĐKXĐ, giá trị $x_2$ [[fill:thỏa mãn]] ĐKXĐ." Các dòng khác giữ nguyên.
- Ví dụ 5: ô "$x\ne [[fill:0]]$" bị lộ bởi "$=0$" của phương trình dưới, ô "$x\ne [[fill:2]]$" bị lộ bởi "$x_1=…=2$" và "Giá trị $x_1=2$".
  Sửa: dòng ĐKXĐ thành "ĐKXĐ: [[fill:$x\ne 0$ và $x\ne 2$]]." Dòng nghiệm thành "nên phương trình có hai nghiệm phân biệt $x_1=\dfrac{-1+3}{1}=[[fill:2]]$ và $x_2=\dfrac{-1-3}{1}=[[fill:-4]]$." Dòng đối chiếu thành "Giá trị $x_1$ [[fill:không thỏa mãn]] ĐKXĐ, giá trị $x_2$ [[fill:thỏa mãn]] ĐKXĐ." Các dòng khác giữ nguyên.

## Tự soát trước khi trả
- So từng khối với bản cũ: chỉ các dòng nêu trên được khác. Mọi dấu $ mở có $ đóng. Không thêm dấu ";".
- Ví dụ: trường "statement" = TOÀN BỘ chuỗi text mới của khối (bắt đầu bằng \textbf{Ví dụ N.}), "solution" = chuỗi rỗng.
- Bài: "statement" và "solution" mới đầy đủ (kể cả phần không đổi).
- Nghi ngờ gì ghi vào "ghi_chu", không tự đổi số.

Đầu ra JSON đúng schema: {"sua": [11 phần tử {"label","statement","solution"}, đủ ''' + ", ".join(LABELS) + r'''], "ghi_chu": "…"}.

## Bản hiện tại
'''


def ban_hien_tai() -> str:
    seed = json.loads((REPO / SEED).read_text())
    out = []
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem" and b.get("label") in LABELS:
                out.append(f'### {b["label"]}\nstatement: {b["statement"]}\nsolution: {b.get("solution","")}')
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m and m.group(1) in LABELS:
                    out.append(f"### {m.group(1)}\ntext: {b['text']}")
    assert len(out) == len(LABELS), len(out)
    return "\n\n".join(out) + "\n"


def main():
    prompt = PROMPT + ban_hien_tai()
    for ten, model in MODELS.items():
        vid = f"vay-9c-ch6-phieu-b-{ten}"
        v = {"id": vid, "model": model, "prompt": prompt, "files": [],
             "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
             "meta": {"loai": "sua-phieu", "seed": SEED, "labels": LABELS}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=2))
        print("→", out.relative_to(REPO), model)


if __name__ == "__main__":
    main()
