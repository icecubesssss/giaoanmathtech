#!/usr/bin/env python3
"""Sinh việc Gemini: sửa đề "ngược" + đáp án sai ở phiếu C (Viète) ch.VI 9C.

Góp ý GV (12/11/2026): Bài 5 nêu công thức trước, mục tiêu sau ⇒ đề ngược;
phải "Tính giá trị biểu thức … với các phương trình sau". Soát thêm thấy
đáp án Bài 5b,c và Bài 3c sai, Bài 5c trùng Ví dụ 4.

    python3 scripts/gemini/viec_sua_phieu_viete_9c.py
    python3 scripts/gemini/tho.py --mot sua-9c-ch6-phieu-c-viete
    python3 scripts/gemini/ap_sua_phieu.py sua-9c-ch6-phieu-c-viete [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-c-dinh-li-viete-va-ung-dung.json"
LABELS = ["Bài 2.", "Bài 3.", "Bài 4.", "Bài 5.", "Bài 6.", "Bài 7.", "Bài 19.", "Bài 22."]
VID = "sua-9c-ch6-phieu-c-viete"

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (định lí Viète, học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: toàn bộ dữ liệu cần sửa nằm ở mục "Dữ liệu gốc" cuối prompt (trích từ seed phiếu). Mỗi bài có "label" (ví dụ "Bài 5."), "statement", "solution". Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; giữ escape \& (ví dụ "GD\&ĐT"). Giữ nguyên thẻ mức [NB] đầu mỗi ý và giữ nguyên chú thích nguồn dạng "\;(thi thử Vào 10 lần 1, THCS Cầu Giấy)" trừ khi được dặn bỏ.

## Vì sao phải sửa (góp ý của giáo viên dạy)
Đề Bài 5 hiện là: "Biết mỗi phương trình sau có hai nghiệm phân biệt x1, x2. Kiểm x1x2 ≠ 0 rồi dùng 1/x1 + 1/x2 = (x1+x2)/(x1x2) để tính." rồi mới liệt kê 3 phương trình.
=> Câu hỏi bị NGƯỢC: học sinh đọc hết một công thức dài mới biết "tính" cái gì, rồi 3 ý lại chỉ là 3 phương trình. Phải đổi thành: NÓI MỤC TIÊU TRƯỚC ("Tính giá trị biểu thức ... với mỗi phương trình sau"), công thức gợi ý để SAU, trong ngoặc. Không dùng văn nói/từ tắt ("Kiểm" → "Kiểm tra", "Soi" → "Chú ý").

## Việc cụ thể (chỉ 8 bài sau)

1) Bài 5. — statement mới theo khung (giữ nguyên các dòng ý a/b sau [[br]], thay ý c):
   "Tính giá trị biểu thức $\dfrac{1}{x_1}+\dfrac{1}{x_2}$, trong đó $x_1, x_2$ là hai nghiệm phân biệt của mỗi phương trình sau.[[br]](Gợi ý: kiểm tra $x_1x_2 \ne 0$ rồi dùng $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{x_1+x_2}{x_1x_2}$.)[[br]]a) ..."
   - Ý c) hiện là $3x^2-6x+2=0$ — TRÙNG phương trình của Ví dụ 4 ngay phía trên (đã có lời giải) ⇒ thay bằng: c) [NB] $x^2-6x+3=0$
   - solution hiện SAI ở b) và c) (chép nhầm số của bài khác). Viết lại cả 3 ý, cùng một khuôn: tổng, tích, tích ≠ 0, kết quả. Đáp số ĐÚNG: a) $4$ ; b) $\dfrac{5}{2}$ (vì $x_1+x_2=5$, $x_1x_2=2$) ; c) $2$ (vì $x_1+x_2=6$, $x_1x_2=3$).
   Mẫu một ý: "a) $x_1+x_2=2$; $x_1x_2=\dfrac{1}{2} \ne 0$ nên $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{2}{\frac12}=4$."

2) Bài 7. — cùng kiểu Bài 5:
   "Tính giá trị biểu thức $(x_1-x_2)^2$, trong đó $x_1, x_2$ là hai nghiệm phân biệt của mỗi phương trình sau.[[br]](Gợi ý: dùng $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2$.)[[br]]a) ..."
   Giữ nguyên 3 ý. solution: viết đủ tổng, tích cho CẢ 3 ý (hiện b, c thiếu). Đáp số: a) 13 ; b) 5 ; c) 25.

3) Bài 4. — đề không có phương trình, chỉ cho tổng và tích:
   "Tính $x_1^2+x_2^2$ khi biết tổng và tích của hai nghiệm $x_1, x_2$ như sau.[[br]](Gợi ý: dùng $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$.)[[br]]a) ..."
   Giữ nguyên số liệu 3 ý và chỗ chấm "thì $x_1^2+x_2^2=\ldots\ldots$". solution giữ nguyên (7; 74; 13).

4) Bài 6. — giống Bài 4, với $x_1^3+x_2^3$ và gợi ý $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$. solution giữ nguyên (72; 18; −19).

5) Bài 3. — statement mới:
   "Viết tổng và tích hai nghiệm $x_1, x_2$ của mỗi phương trình sau (biết mỗi phương trình có hai nghiệm phân biệt).[[br]](Gợi ý: chú ý dấu của $b$ và $c$.)[[br]]a) ..."
   - Ý c) $x^2-10x+4=0$: BỎ chú thích nguồn "\;(thi thử Vào 10, THCS Tự Lập)" vì đề gốc Tự Lập là $x^2+10x+4=0$ (đã dùng ở bài khác) — giữ phương trình $x^2-10x+4=0$.
   - solution c) hiện SAI ("$x_1+x_2=-1$; $x_1x_2=-6$"). Đúng: c) $x_1+x_2=10$; $x_1x_2=4$. Ý a, b giữ nguyên.

6) Bài 2. và Bài 19. — chỉ đổi "Kiểm điều kiện" thành "Kiểm tra điều kiện". solution giữ nguyên.

7) Bài 22. — statement mới:
   "Tính tổng nghịch đảo hai nghiệm $\dfrac{1}{x_1}+\dfrac{1}{x_2}$ của mỗi phương trình sau (kiểm tra $x_1x_2 \ne 0$ trước).[[br]]a) ..." — giữ nguyên ý a, b và solution.

## Kiểm lại trước khi nộp
- Tự tính lại MỌI đáp số trong solution của 8 bài (Viète: $x_1+x_2=-\frac{b}{a}$, $x_1x_2=\frac{c}{a}$). Thấy chỗ nào nghi sai thì ghi vào "ghi_chu", không tự đổi đề ngoài phạm vi trên.
- Không đổi "label", không thêm/bớt bài, không đổi số ý.
- LaTeX hợp lệ: ngoặc { } cân, $ đủ cặp, dùng \dfrac như bản gốc.

## Đầu ra
JSON đúng schema: {"sua": [8 phần tử {"label","statement","solution"}, đủ Bài 2., Bài 3., Bài 4., Bài 5., Bài 6., Bài 7., Bài 19., Bài 22.], "ghi_chu": "điểm nghi ngờ hoặc chuỗi rỗng"}.
"statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ (kể cả phần không đổi).
'''


def main():
    seed = json.loads((REPO / SEED).read_text())
    goc = [{k: b[k] for k in ("label", "statement", "solution")}
           for s in seed["stages"] for b in s.get("blocks", [])
           if b.get("type") == "problem" and b["label"] in LABELS]
    assert len(goc) == len(LABELS), goc
    viec = {
        "id": VID, "model": "gemini-3.8-flash-high",
        "prompt": PROMPT + "\n## Dữ liệu gốc (8 bài, JSON)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "600s",
        "meta": {"loai": "sua-phieu", "seed": SEED, "labels": LABELS},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))


if __name__ == "__main__":
    main()
