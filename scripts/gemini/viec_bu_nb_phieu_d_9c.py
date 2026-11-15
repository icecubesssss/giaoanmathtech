#!/usr/bin/env python3
"""Phiếu D ch.VI 9C (13/11/2026) — lượt 2 bù giờ: sau lượt 1 (viec_bu_gio_ch6_9c.py) trên lớp 105′ nhưng
tỉ lệ NB 20% / TH 57% (chuẩn tầng C 40-40-20). Bài 9e đã chuyển xuống BTVN (Bài 20c), thêm 7 ý NB điền khuyết
theo đúng khung ví dụ: Bài 1d, 2d, 3c, 4c, 6c, Bài 5 thành 3 ý (khung bài giải). Đáp số ở so_do_phieu_d_9c.py.

    python3 scripts/gemini/viec_bu_nb_phieu_d_9c.py
    python3 scripts/gemini/tho.py --mot bu-nb-9c-ch6-d
    python3 scripts/gemini/ap_sua_phieu.py bu-nb-9c-ch6-d [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import so_do_phieu_d_9c as sd  # noqa: E402
from viec_bu_gio_ch6_9c import CHUNG_D, DAU_RA, SEED_D, khoi  # noqa: E402

NHAN = ["Bài 1.", "Bài 2.", "Bài 3.", "Bài 4.", "Bài 5.", "Bài 6.", "Bài 20."]
PROMPT = CHUNG_D + r'''
## Việc: nối thêm ý vào các bài (ý cũ GIỮ NGUYÊN từng ký tự, trừ Bài 5 đổi câu dẫn như hướng dẫn)
Ý mới chép ĐÚNG khung của ý cũ cùng bài (cùng câu chữ, cùng vị trí chỗ chấm [[blank:1.6cm]] hoặc \ldots\ldots như ý cũ đang dùng), chỉ thay số theo sơ đồ. Thẻ "[NB]" đầu mỗi ý. "solution" nối lời giải ý mới theo đúng cách viết ý cũ.
- Bài 1. thêm d) phương trình $x^2+6x-2=0$.
- Bài 2. thêm d) phương trình $x^2+5x-1=0$.
- Bài 3. thêm c) phương trình $x^2-3x-2=0$, biểu thức $x_1^2-3x_1+2023$ (đặt tên biểu thức theo cách ý a, b đang đặt, không trùng chữ cái đã dùng trong bài).
- Bài 4. thêm c) phương trình $x^2-6x+2=0$, biểu thức $x_1^2+6x_2-5$ (đặt tên như trên).
- Bài 6. thêm c) phương trình $x^2+9x+4=0$, xét dấu hai nghiệm (cùng âm) rồi rút gọn $\sqrt{(x_2-1)^2}=1-x_2$.
- Bài 5. đổi thành bài 3 ý, mỗi ý là một KHUNG BÀI GIẢI giống hệt khung hiện tại:
    câu dẫn mới: "Điền vào chỗ chấm để hoàn thành bài giải tính giá trị của mỗi biểu thức sau.[[br]]a) [NB] Cho phương trình $x^2-2x-7=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Tính $B=x_1^2+2x_2+x_1x_2$.[[br]]<các dòng khung hiện tại, nguyên văn>[[br]]b) [NB] Cho phương trình $x^2-4x-1=0$. … Tính $M=x_1^2+4x_2+x_1x_2$.[[br]]<khung như a, đổi số>[[br]]c) [NB] Cho phương trình $x^2-8x-3=0$. … Tính $N=x_1^2+8x_2+x_1x_2$.[[br]]<khung như a, đổi số>"
    PHẢI giữ cụm chữ "hoàn thành bài giải" trong câu dẫn. "solution": "a) …[[br]]…[[br]]b) …[[br]]…[[br]]c) …" (ý a là lời giải hiện tại nguyên văn).
- Bài 20. (BTVN, TH) thêm c) [TH] $x^2-2x-9=0$, tính $E=\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$ \;(thi thử Vào 10, THCS Thái Thịnh) — lời giải có bước $x_1x_2\ne 0$, đáp số $E=-\dfrac{22}{9}$.

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + "\n".join(f"- {k}\n" + "\n".join("    " + x for x in v) for k, v in sd.tom_tat()[0].items()
                if k in NHAN) + '''

## Bản hiện tại
''' + khoi(SEED_D, NHAN) + DAU_RA % ", ".join(NHAN)


def main():
    vid = "bu-nb-9c-ch6-d"
    v = {"id": vid, "model": "gemini-4-hydrogen-medium", "prompt": PROMPT, "files": [],
         "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "sua-phieu", "seed": SEED_D, "labels": NHAN}}
    out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=2))
    print("→", out.relative_to(REPO), f"{len(PROMPT) // 1000}k ký tự")


if __name__ == "__main__":
    main()
