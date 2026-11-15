#!/usr/bin/env python3
"""Việc Gemini: viết lại "hints" 8 bài TH/VD phiếu D ch.VI 9C theo Polya §17 (13/11/2026).

Bản Gemini lượt đầu gợi ý LỘ cách giải ("biến đổi −16x₁+5 thành (x₁−3)²", "áp dụng định lí Viète").
    python3 scripts/gemini/viec_goi_y_phieu_d_9c.py
    python3 scripts/gemini/tho.py --mot goi-y-9c-ch6-phieu-d
    python3 scripts/gemini/ap_goi_y_phieu_d_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem.json"
VID = "goi-y-9c-ch6-phieu-d"

PROMPT = r'''Bạn là giáo viên Toán 9 viết GỢI Ý cho học sinh lớp 9 tầng C (học lực trung bình yếu), chủ đề tính giá trị biểu thức chứa hai nghiệm của phương trình bậc hai (Viète, hạ bậc dùng "x_1 là nghiệm", xét dấu nghiệm, sqrt{A^2}=|A|). KHÔNG chạy lệnh, KHÔNG mở file.

Viết lại "hints" cho từng bài dưới đây theo G. Polya, "Giải một bài toán như thế nào?" §17 "Câu hỏi tốt và câu hỏi tồi":
- Mỗi bài 1–2 gợi ý, mỗi gợi ý là MỘT CÂU HỎI ngắn (kết thúc bằng "?").
- Câu hỏi đi từ TỔNG QUÁT tới đặc biệt, DÙNG LẠI ĐƯỢC cho bài khác cùng loại. Ví dụ câu hỏi tốt: "Biểu thức có đổi khi đổi chỗ $x_1$ và $x_2$ không?", "Số $x_1$ thoả mãn đẳng thức nào?", "Bài nào trong phiếu đã gặp biểu thức có dạng giống thế này?", "Biểu thức dưới dấu căn có viết được thành bình phương của một biểu thức không?", "Muốn bỏ dấu giá trị tuyệt đối cần biết điều gì?".
- CẤM: gọi tên công cụ kiểu mệnh lệnh ("Áp dụng định lí Viète", "Dùng tính chất nghiệm để hạ bậc"); viết sẵn phép biến đổi hay kết quả trung gian (CẤM ghi "$(x_1-3)^2$", "$3x_2-1=x_2^2$", "$x_1^3=…$", "$\dfrac{x_1^3+x_2^3}{x_1x_2}$"); con số đáp số; "em", "các em", "hãy"; dấu ";".
- Có thể nhắc "như Ví dụ N" để học sinh tự mở lại ví dụ cùng loại (Ví dụ 6: biểu thức một nghiệm bậc ba · Ví dụ 7: biểu thức không đối xứng · Ví dụ 8: căn bậc hai + dấu nghiệm · Ví dụ 9: phân thức lệch có $x_1x_2=1$).
- Toán trong $…$, chuỗi JSON hợp lệ.

Đầu ra JSON: {"goi_y":[{"label":"Bài 7.","hints":["…","…"]}, … đủ 8 bài], "ghi_chu": ""}.

## Các bài (đề + lời giải để hiểu, KHÔNG chép lời giải vào gợi ý)
'''


def main():
    f = json.loads((REPO / SEED).read_text())
    bai = [{"label": b["label"], "statement": b["statement"], "solution": b["solution"]}
           for s in f["stages"] for b in s["blocks"] if b.get("type") == "problem" and b.get("level", 1) >= 2]
    v = {"id": VID, "model": "gemini-3.8-flash-high",
         "prompt": PROMPT + json.dumps(bai, ensure_ascii=False, indent=1) + "\n", "files": [],
         "schema": "scripts/gemini/schema/goi-y-polya.json", "timeout": "900s",
         "meta": {"loai": "goi-y", "seed": SEED, "labels": [b["label"] for b in bai]}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), [b["label"] for b in bai])


if __name__ == "__main__":
    main()
