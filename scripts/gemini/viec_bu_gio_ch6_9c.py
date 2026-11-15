#!/usr/bin/env python3
"""Bù giờ phiếu B và D ch.VI 9C (13/11/2026) — Thầy giao Claude tự quyết.

Đo giờ: B trên lớp 90′/120, BTVN 77′/90 · D trên lớp 72′/120, BTVN 78′/90 (C tổng ví dụ + luyện tập
170′ ≈ quỹ 165′ ⇒ giữ nguyên). Đề mới đều là đề thật trong ngân hàng ch.VI, đáp số kiểm ở
so_do_phieu_b_9c.py / so_do_phieu_d_9c.py. Gemini chỉ viết chữ:
  B: Bài 5 thêm d), e) · Bài 6 thêm c), d) · Bài 13 thêm d) · Bài 14 thêm c)  (giữ nguyên ý cũ)
  D: Bài 8 thêm c) · Bài 9 MỚI (TH, 5 ý) · Bài 20 MỚI (TH BTVN, 2 ý)  — D đã đánh số lại bằng doi_so_phieu_d_9c.py

    python3 scripts/gemini/viec_bu_gio_ch6_9c.py
    python3 scripts/gemini/tho.py --tien-to bu-gio-9c-ch6- --song-song 2
    python3 scripts/gemini/ap_sua_phieu.py bu-gio-9c-ch6-b [--ghi]
    python3 scripts/gemini/ap_sua_phieu.py bu-gio-9c-ch6-d [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import so_do_phieu_b_9c as sb  # noqa: E402
import so_do_phieu_d_9c as sd  # noqa: E402
from viec_sua_phieu_b_9c import CHUNG as CHUNG_B  # noqa: E402
from viec_dung_lai_phieu_d_9c import CHUNG as CHUNG_D  # noqa: E402

D_DIR = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
SEED_B = D_DIR + "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json"
SEED_D = D_DIR + "phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json"
MODEL = "gemini-4-hydrogen-medium"

DAU_RA = '''
## Đầu ra
JSON đúng schema: {"sua": [phần tử {"label","statement","solution","hints"} cho ĐÚNG các nhãn: %s], "ghi_chu": "…"}.
"statement" và "solution" là chuỗi ĐẦY ĐỦ của cả bài (ý cũ chép lại NGUYÊN VĂN từng ký tự + ý mới nối vào cuối).
"hints": bài nào giữ gợi ý cũ thì trả mảng rỗng [] (máy giữ nguyên), bài MỚI thì viết 1–2 câu hỏi gợi ý.

## Tự soát trước khi trả
- Ý cũ: so từng ký tự với bản hiện tại, không được khác một dấu.
- Ý mới: tự tính lại từng dòng trung gian, đối chiếu với "Sơ đồ đề và đáp số" (máy đã kiểm). Lệch thì ghi "ghi_chu", không tự đổi số.
- Mọi dấu $ mở có $ đóng. Không dấu ";" (trừ "\\;"). Không "Do đó", "Suy ra", "Như vậy".
'''


def khoi(seed, nhan):
    d = json.loads((REPO / seed).read_text())
    out = []
    for s in d["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem" and b["label"] in nhan:
                out.append(json.dumps({k: b.get(k) for k in ("label", "tier", "level", "statement", "solution",
                                                                "hints")}, ensure_ascii=False, indent=1))
    assert len(out) == len(nhan), (seed, nhan, len(out))
    return "\n".join(out)


def so_do_b(*nhan):
    tt, trung = sb.tom_tat()
    return "\n".join(f"- {k}\n" + "\n".join("    " + x for x in tt[k]) for k in nhan)


# ─────────────────────────── PHIẾU B ───────────────────────────
NHAN_B = ["Bài 5.", "Bài 6.", "Bài 13.", "Bài 14."]
PROMPT_B = CHUNG_B + r'''
## Việc: BÙ GIỜ — nối thêm ý mới vào 4 bài tự trình bày (TH) đang có. Ý cũ GIỮ NGUYÊN từng ký tự.
- Bài 5. (trên lớp): giữ a), b), c), thêm
    d) [TH] $\dfrac{2x}{x+1}+\dfrac{7x^2-3x}{x^2-1}=\dfrac{3x-1}{x-1}$ \;(Giữa kì I, THCS Giảng Võ)
    e) [TH] $\dfrac{2x-2}{x-3}-\dfrac{x-5}{x+3}=\dfrac{-21}{x^2-9}$ \;(Học kì I, THCS Nguyễn Trường Tộ)
- Bài 6. (trên lớp): giữ a), b), thêm
    c) [TH] $\dfrac{3x-1}{x-2}-\dfrac{2x-3}{x+2}+\dfrac{2x^2+7x-2}{4-x^2}=0$ \;(Giữa kì I, THCS Nguyễn Trường Tộ)  — mẫu $4-x^2$ đối với $x^2-4$: dòng riêng "Ta có $\dfrac{2x^2+7x-2}{4-x^2}=-\dfrac{2x^2+7x-2}{x^2-4}$." trước khi quy đồng.
    d) [TH] $\dfrac{x+2}{x-2}-\dfrac{x-2}{2+x}=\dfrac{x^2+16}{x^2-4}$ \;(Giữa kì I, THCS Ái Mộ)  — sau khử mẫu có nghiệm kép, dùng $\Delta'=0$.
- Bài 13. (BTVN): giữ a), b), c), thêm
    d) [TH] $\dfrac{1}{x+1}+\dfrac{2}{x-1}=\dfrac{x^2+1}{x^2-1}$ \;(Giữa kì I, THCS Chuyên Mỹ)  — khuyết $c$, nhận cả hai nghiệm.
- Bài 14. (BTVN): giữ a), b), thêm
    c) [TH] $\dfrac{2x-5}{x+4}+\dfrac{x}{4-x}=\dfrac{-17x+56}{x^2-16}$ \;(Giữa kì I, THCS Nguyễn Huy Tưởng)  — mẫu $4-x$ đối với $x-4$: dòng riêng đổi dấu trước khi quy đồng. Sau khử mẫu khuyết $b$: $x^2=36$.
Thẻ "[TH]" đặt ở đầu mỗi ý mới như ý cũ. Lời giải ý mới đủ 4 bước SGK như các ý cũ của cùng bài (xem phần "solution" hiện tại để bắt chước đúng cách viết, cách xuống dòng, cách đặt "a)", "b)").
Dòng khử mẫu phải hiện phép nhân với mẫu thức chung rồi khai triển, thu gọn như các ý cũ. Hệ số $a$ âm sau thu gọn thì nhân hai vế với $-1$ (viết rõ) để được $a>0$.

## Sơ đồ đề và đáp số (máy đã kiểm — chỉ dùng các ý mới: Bài 5 d, e · Bài 6 c, d · Bài 13 d · Bài 14 c)
''' + so_do_b(*NHAN_B) + '''

## Bản hiện tại của 4 bài
''' + khoi(SEED_B, NHAN_B) + DAU_RA % ", ".join(NHAN_B)


# ─────────────────────────── PHIẾU D ───────────────────────────
NHAN_D = ["Bài 8.", "Bài 9.", "Bài 20."]
PROMPT_D = CHUNG_D + r'''
## Ghi đè luật cũ
Phiếu đã ĐÁNH SỐ LẠI: hai đề thật chép nguyên văn nay là Bài 10 và Bài 11 (không thuộc việc này).
Các ý mới dưới đây đều là ĐỀ THẬT: giữ đúng phương trình, đúng biểu thức, viết lại theo câu dẫn chung của bài, kèm chú thích nguồn ở cuối ý như ghi.

## Việc: BÙ GIỜ phiếu D (ý cũ GIỮ NGUYÊN từng ký tự)
- Bài 8. (trên lớp, TH): giữ a), b), thêm
    c) [TH] $4x^2-2x-1=0$, tính $K=(x_1-x_2)^2-x_1\left(x_1-\dfrac{1}{2}\right)$ \;(cuối kì II, THCS Phúc Đồng)
   Lời giải: kiểm tra $ac<0$ · Viète ($x_1+x_2=\dfrac{1}{2}$, $x_1x_2=-\dfrac{1}{4}$) · hạ bậc: $4x_1^2-2x_1-1=0$ nên $x_1^2-\dfrac{1}{2}x_1=\dfrac{1}{4}$, tức là $x_1\left(x_1-\dfrac{1}{2}\right)=\dfrac{1}{4}$ · $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2=\dfrac{1}{4}+1=\dfrac{5}{4}$ · $K=\dfrac{5}{4}-\dfrac{1}{4}=1$ · "Vậy $K=1$."
- Bài 9. MỚI (trên lớp, TH, level 2, chỗ đang ghi "(chờ Gemini)"): câu dẫn giống Bài 8 ("Với mỗi phương trình sau, gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của mỗi biểu thức sau:"), 5 ý:
    a) [TH] $x^2+4x-6=0$, tính $A=\dfrac{1}{x_1+3}+\dfrac{1}{x_2+3}$ \;(bộ đề Vào 10 Đống Đa, THCS Thái Thịnh)
    b) [TH] $x^2-5x+4=0$, tính $B=\dfrac{5x_1-x_2}{x_1}-\dfrac{x_1-5x_2}{x_2}$ \;(bộ đề Vào 10 Đống Đa, THCS Quang Trung)
    c) [TH] $2x^2-13x-6=0$, tính $C=(x_1+x_2)(x_1+2x_2)-x_2^2$ \;(bộ đề Vào 10 Đống Đa, THCS Tô Vĩnh Diện)
    d) [TH] $x^2-7x-1=0$, tính $D=x_1^2+x_2^2-x_1x_2$ \;(cuối kì II, THCS Thăng Long)
    e) [TH] $x^2-2x-9=0$, tính $E=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$ \;(thi thử Vào 10, THCS Thái Thịnh)
   Lời giải mỗi ý: kiểm tra điều kiện có nghiệm (ý a, c, d, e dùng $ac<0$, ý b dùng $\Delta$) · Viète · điều kiện mẫu khác $0$ khi cần (ý a: $x_1+3\ne 0$, $x_2+3\ne 0$ vì $(x_1+3)(x_2+3)=x_1x_2+3(x_1+x_2)+9=-9\ne 0$ · ý b, e: $x_1x_2\ne 0$) · biến đổi biểu thức về $x_1+x_2$ và $x_1x_2$ (quy đồng hoặc khai triển, mỗi phép một dòng) · thay số · "Vậy …".
   Đáp số: $A=-\dfrac{2}{9}$, $B=\dfrac{23}{4}$, $C=\dfrac{157}{4}$, $D=52$, $E=-\dfrac{22}{9}$.
   hints (2 câu, không lộ số): "Biểu thức có đổi không khi đổi chỗ $x_1$ và $x_2$?" và "Quy đồng hoặc khai triển thì biểu thức viết được theo $x_1+x_2$ và $x_1x_2$ không?"
- Bài 20. MỚI (BTVN, TH, level 2): câu dẫn như Bài 9, 2 ý (không ghi nguồn):
    a) [TH] $x^2-4x-7=0$, tính $T=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}-2$   — đáp số $T=-\dfrac{44}{7}$ (có bước $x_1x_2\ne 0$)
    b) [TH] $2x^2-4x-3=0$, tính $A=(x_1-x_2)^2$   — đáp số $A=10$
   hints: 1–2 câu hỏi như Bài 9.
Lời giải viết theo đúng nhịp của Bài 8 hiện tại (xem "solution" của Bài 8): "a) Ta có …[[br]]\hspace*{1.4em}Theo định lí Viète, ta có $\begin{cases} … \end{cases}$[[br]]\hspace*{1.4em}…[[br]]\hspace*{1.4em}Vậy …[[br]]b) …".

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + "\n".join(f"- {k}\n" + "\n".join("    " + x for x in v) for k, v in sd.tom_tat()[0].items()
                if k in NHAN_D) + '''

## Bản hiện tại của 3 bài
''' + khoi(SEED_D, NHAN_D) + DAU_RA % ", ".join(NHAN_D)


def main():
    for ten, prompt, seed, nhan in (("b", PROMPT_B, SEED_B, NHAN_B), ("d", PROMPT_D, SEED_D, NHAN_D)):
        vid = f"bu-gio-9c-ch6-{ten}"
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": [],
             "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
             "meta": {"loai": "sua-phieu", "seed": seed, "labels": nhan}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=2))
        print("→", out.relative_to(REPO), MODEL, f"{len(prompt) // 1000}k ký tự")


if __name__ == "__main__":
    main()
