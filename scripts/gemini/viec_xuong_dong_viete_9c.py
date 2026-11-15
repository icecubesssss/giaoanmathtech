#!/usr/bin/env python3
"""Sinh việc Gemini: trình bày lại phiếu C Viète ch.VI 9C — bỏ chấm phẩy, mỗi bước một dòng.

Thầy 12/11/2026: "Trình bày đang khá bị ríu rít, cần căn chỉnh lại như văn bản thông thường,
căn lề khi viết công thức, căn dòng lại; các phần trình bày cần xuống dòng thì xuống dòng,
đừng chấm phẩy."

    python3 scripts/gemini/viec_xuong_dong_viete_9c.py
    python3 scripts/gemini/tho.py --mot dong-9c-ch6-phieu-c-viete
    python3 scripts/gemini/ap_sua_phieu.py dong-9c-ch6-phieu-c-viete [--ghi]
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
VID = "dong-9c-ch6-phieu-c-viete"
CHAM_PHAY = re.compile(r"(?<!\\);")

PROMPT = r'''Bạn là thợ dàn trang phiếu học tập Toán 9 (định lí Viète). Việc lần này CHỈ là TRÌNH BÀY LẠI: không đổi đề, không đổi số, không đổi đáp số, không thêm/bớt ý, không đổi lời văn ngoài những chỗ luật dưới cho phép.

KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu ở cuối prompt. Xuống dòng là [[br]]. Toán trong $...$. Giữ nguyên thẻ [NB]/[TH]/[VD], chú thích nguồn "\;(…)" (lưu ý "\;" là lệnh khoảng trắng LaTeX, KHÔNG phải dấu chấm phẩy — giữ nguyên), "GD\&ĐT", phần "{\sffamily\bfseries\color{brand}Lời giải}".

## Góp ý của Thầy
"Trình bày đang khá bị ríu rít, cần căn chỉnh lại như văn bản thông thường, căn lề khi viết công thức, căn dòng lại; các phần trình bày cần xuống dòng thì xuống dòng, đừng chấm phẩy."

## Luật
L1. KHÔNG còn dấu ";" nối các bước, các ô điền, các kết quả (ngoài công thức). Mỗi bước / mỗi ô điền / mỗi kết quả sang DÒNG RIÊNG.
L2. Dòng con của một ý a), b), c) (trong đề HOẶC trong solution) bắt đầu bằng "[[br]]\hspace*{1.4em}" để thẳng cột, thụt vào so với "a)". Dòng "a) …" chỉ chứa phương trình/dữ kiện của ý đó (kèm chú thích nguồn nếu có), bỏ dấu ":" ở cuối dòng.
   Ví dụ (đề Bài 5):
   a) [NB] $2x^2-4x+1=0$ \;(thi thử Vào 10 lần 1, THCS Cầu Giấy)[[br]]\hspace*{1.4em}$x_1+x_2=\ldots\ldots$[[br]]\hspace*{1.4em}$x_1x_2=\ldots\ldots$[[br]]\hspace*{1.4em}$\dfrac{1}{x_1}+\dfrac{1}{x_2}=\ldots\ldots$
   Ví dụ (đề Bài 4 — dữ kiện là tổng và tích):
   a) [NB] $x_1+x_2=3$ và $x_1x_2=1$[[br]]\hspace*{1.4em}$x_1^2+x_2^2=\ldots\ldots$
   (bỏ chữ "thì"; hai dữ kiện ngắn nối bằng "và" trên cùng dòng a) là được)
   Ví dụ (solution một ý NB):
   a) $x_1+x_2=2$[[br]]\hspace*{1.4em}$x_1x_2=\dfrac{1}{2} \ne 0$[[br]]\hspace*{1.4em}$\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{2}{\frac12}=4$.
L3. Trong LỜI GIẢI (ví dụ mẫu và solution có các dòng "\hspace*{1.4em}…" hoặc "Ta có …"), câu Viète viết bằng dấu ngoặc hệ, đúng khuôn:
   "Theo định lí Viète, ta có $\begin{cases} x_1+x_2=7\\ x_1x_2=5\end{cases}$"
   (thay số tương ứng; giữ "\ne 0" nếu bản gốc có; không thêm dấu chấm sau ngoặc hệ trừ khi đó là hết câu.)
   Các dòng lời giải khác giữ nguyên, mỗi bước vẫn một dòng; nếu một dòng đang dồn 2 bước bằng ";" thì tách thành 2 dòng, mỗi dòng mở đầu như dòng gốc (ví dụ "[[br]]\hspace*{1.4em}" trong ví dụ mẫu, "[[br]]" trong solution TH/VD).
L4. Bài lập phương trình: "Tổng $=…$; tích $=…$ nên phương trình là …" → tách: "Tổng $=…$" / "Tích $=…$" / "Phương trình cần lập là …" mỗi cái một dòng (dòng con theo L2).
L5. Bài 2/Bài 20 dạng "…$ac=\ldots\ldots$ nên phương trình \ldots\ldots; \ldots\ldots dùng định lí Viète.": tách thành 2 dòng con "$ac=\ldots\ldots$ nên phương trình \ldots\ldots" và "Phương trình \ldots\ldots dùng định lí Viète."; solution tương ứng cũng 2 dòng. Bài điền cả bài giải (Bài 10, Bài 18): mỗi ô/mỗi bước một dòng con theo L2.
L6. Bài "Xét dấu" (Bài 11): "$x_1x_2=\ldots\ldots$; $x_1+x_2=\ldots\ldots$ nên hai nghiệm \ldots\ldots" → mỗi phần một dòng con.
L7. Dòng mở đầu đề (câu dẫn), dòng "(Gợi ý: …)" giữ nguyên. Không dùng "\\", "\newline", "\quad" để xuống dòng — chỉ "[[br]]".
L8. Khối "Ví dụ N." (label bắt đầu "Ví dụ"): trường "statement" là TOÀN BỘ nội dung khối (đề + lời giải), sửa theo L3; "solution" để chuỗi rỗng "". Câu đề ví dụ có "a) …; b) …" trên cùng dòng thì đổi thành "a) …" và "b) …" ở hai dòng riêng (dùng [[br]]).

## Kiểm lại trước khi nộp
- Không còn ";" ngoài công thức (trừ "\;").
- Mọi công thức, số, đáp số giữ y nguyên (chỉ được đổi cách xuống dòng, bỏ "thì", thêm "và", thêm "ta có", dùng ngoặc hệ cho cặp Viète).
- { } cân, $ đủ cặp, mỗi \begin{cases} có \end{cases}.

## Đầu ra
JSON đúng schema: {"sua": [mỗi khối ở "Dữ liệu gốc" một phần tử {"label","statement","solution"}, ĐỦ và ĐÚNG label], "ghi_chu": "..."}. Chuỗi là bản HOÀN CHỈNH thay bản cũ.
'''


def khoi_can_sua(seed: dict) -> list[dict]:
    out = []
    for s in seed["stages"]:
        if s["kind"] in ("review", "concept"):
            continue
        for b in s["blocks"]:
            if b.get("type") == "problem":
                if CHAM_PHAY.search(b["statement"]) or CHAM_PHAY.search(b.get("solution", "")):
                    out.append({"label": b["label"], "statement": b["statement"], "solution": b.get("solution", "")})
            elif b.get("type") == "noted" and CHAM_PHAY.search(b.get("text", "")):
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b["text"])
                if m:
                    out.append({"label": m.group(1), "statement": b["text"], "solution": ""})
    return out


def main():
    seed = json.loads((REPO / SEED).read_text())
    goc = khoi_can_sua(seed)
    viec = {
        "id": VID, "model": "gemini-3.8-flash-high",
        "prompt": PROMPT + f"\n## Dữ liệu gốc ({len(goc)} khối)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
        "meta": {"loai": "sua-phieu", "seed": SEED, "labels": [g["label"] for g in goc]},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), "—", len(goc), "khối")


if __name__ == "__main__":
    main()
