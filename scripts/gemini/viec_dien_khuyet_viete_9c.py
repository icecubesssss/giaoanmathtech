#!/usr/bin/env python3
"""Sinh việc Gemini: đưa NB Luyện tập 1 phiếu C Viète (ch.VI 9C) về điền khuyết.

Thầy duyệt 12/11/2026: dan_dat_gate chặn vì Bài 4, 6, 10, 11 (điền) đứng sau bài
tự trình bày cùng mạch ⇒ đưa cả 11 bài NB LT1 về điền khuyết (Bài 1, 4, 6, 10, 11 đã là điền).

    python3 scripts/gemini/viec_dien_khuyet_viete_9c.py
    python3 scripts/gemini/tho.py --mot dien-9c-ch6-phieu-c-viete
    python3 scripts/gemini/ap_sua_phieu.py dien-9c-ch6-phieu-c-viete [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
LABELS = ["Bài 2.", "Bài 3.", "Bài 5.", "Bài 7.", "Bài 8.", "Bài 9."]
MAU = ["Bài 1.", "Bài 4."]
VID = "dien-9c-ch6-phieu-c-viete"

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (định lí Viète, học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề, KHÔNG đổi số liệu.

KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu nằm ở cuối prompt. Mỗi bài có "label", "statement", "solution". Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; giữ escape \& (ví dụ "GD\&ĐT"). Giữ nguyên thẻ [NB] đầu mỗi ý và chú thích nguồn dạng "\;(thi thử Vào 10, ...)".

## Mục tiêu
Phần Nhận biết của phiếu phải là ĐIỀN KHUYẾT: mỗi ý học sinh chỉ điền vào chỗ chấm, không tự trình bày. Chỗ điền viết đúng một kiểu: $\ldots\ldots$ (nằm trong công thức) hoặc \ldots\ldots (trong lời). Hai bài MẪU đã đúng kiểu (Bài 1., Bài 4.) — bắt chước đúng cách đặt chỗ chấm của chúng.
Câu dẫn giữ kiểu "nêu mục tiêu trước, gợi ý sau" như bản hiện tại; chỉ thay câu dẫn khi cần thêm chữ "Điền vào chỗ chấm".

## Việc cụ thể (6 bài)
1) Bài 2. — câu dẫn: "Kiểm tra điều kiện rồi điền vào chỗ chấm để cho biết phương trình nào được phép dùng định lí Viète." Mỗi ý theo khung (dùng $ac$ khi $ac<0$, dùng $\Delta$ khi $ac>0$, đúng như solution hiện có):
   "a) [NB] $x^2-3x-5=0$ \;(nguồn giữ nguyên): $ac=\ldots\ldots$ nên phương trình \ldots\ldots; \ldots\ldots dùng định lí Viète."
   "c) [NB] $x^2-x+1=0$: $\Delta=\ldots\ldots$ nên phương trình \ldots\ldots; \ldots\ldots dùng định lí Viète."
   solution: điền đủ, ví dụ "a) $ac=-5<0$ nên phương trình có hai nghiệm phân biệt; được dùng định lí Viète." / "c) $\Delta=-3<0$ nên phương trình vô nghiệm; không được dùng định lí Viète."
2) Bài 3. — giữ câu dẫn và dòng gợi ý; mỗi ý thêm ": $x_1+x_2=\ldots\ldots$; $x_1x_2=\ldots\ldots$" sau phương trình (sau cả chú thích nguồn nếu có) — đúng như Bài 1. solution giữ nguyên.
3) Bài 5. — giữ câu dẫn và dòng gợi ý; mỗi ý thêm ": $x_1+x_2=\ldots\ldots$; $x_1x_2=\ldots\ldots$; $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\ldots\ldots$". solution giữ nguyên (đáp số 4; 5/2; 2).
4) Bài 7. — tương tự Bài 5 với "$(x_1-x_2)^2=\ldots\ldots$". solution giữ nguyên (13; 5; 25).
5) Bài 8. — mỗi ý: "a) [NB] $3$ và $-5$: tổng $=\ldots\ldots$; tích $=\ldots\ldots$; phương trình cần lập: \ldots\ldots". solution giữ nguyên.
6) Bài 9. — giữ câu dẫn (có thể bỏ cụm "khi hệ số chứa căn" nếu muốn câu gọn, nhưng giữ ý nói hệ số chứa căn); mỗi ý thêm ": $x_1+x_2=\ldots\ldots$; $x_1x_2=\ldots\ldots$". solution giữ nguyên.

## Kiểm lại trước khi nộp
- Mỗi ý của 6 bài đều có ít nhất một chỗ chấm \ldots. Không còn ý nào bắt học sinh tự viết lời giải.
- Không đổi label, không đổi phương trình/số liệu, không thêm/bớt ý.
- Đáp số solution khớp đề (tự tính lại bằng Viète); thấy nghi ngờ ghi vào "ghi_chu".
- LaTeX hợp lệ: { } cân, $ đủ cặp.

## Đầu ra
JSON đúng schema: {"sua": [6 phần tử {"label","statement","solution"} cho Bài 2., Bài 3., Bài 5., Bài 7., Bài 8., Bài 9.], "ghi_chu": "..."}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''


def main():
    seed = json.loads((REPO / SEED).read_text())
    probs = {b["label"]: {k: b[k] for k in ("label", "statement", "solution")}
             for s in seed["stages"] for b in s.get("blocks", []) if b.get("type") == "problem"}
    viec = {
        "id": VID, "model": "gemini-3.8-flash-high",
        "prompt": PROMPT
        + "\n## Bài MẪU (chỉ để bắt chước, KHÔNG nộp lại)\n" + json.dumps([probs[x] for x in MAU], ensure_ascii=False, indent=1)
        + "\n## Dữ liệu gốc (6 bài cần sửa)\n" + json.dumps([probs[x] for x in LABELS], ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "600s",
        "meta": {"loai": "sua-phieu", "seed": SEED, "labels": LABELS},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))


if __name__ == "__main__":
    main()
