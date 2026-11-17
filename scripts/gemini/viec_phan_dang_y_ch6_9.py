#!/usr/bin/env python3
"""Sinh việc Gemini: PHÂN DẠNG LẠI tab "Phân dạng Ch.VI lớp 9C" theo danh mục dạng đóng (Thầy 16/11/2026).

Mỗi câu của ngân hàng (snapshot repo) được TÁCH Ý, mỗi ý gán đúng một mã dạng trong
`danh_muc_dang` của khung chương (scripts/danh_muc_dang_ch6_9.py) + mức + biến thể.
Schema ép mã ∈ danh mục ⇒ không còn tên dạng viết tự do.

    .venv/bin/python scripts/danh_muc_dang_ch6_9.py --ghi          (danh mục vào khung)
    .venv/bin/python scripts/gemini/viec_phan_dang_y_ch6_9.py       (sinh việc vào hàng đợi)
    python3 scripts/gemini/tho.py --tien-to pd-y-ch6-9- --song-song 4
    .venv/bin/python scripts/gom_phan_dang_y.py                     (gom + kiểm + thống kê)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-06.json"
BANK = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06.json"
SCHEMA_GOC = REPO / "scripts/gemini/schema/phan-dang-y.json"
TIEN_TO = "pd-y-ch6-9-"
CO_LO = 40

PROMPT = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm, làm việc PHÂN DẠNG ngân hàng câu hỏi chương VI Đại số 9 (KNTT: hàm số y = ax², phương trình bậc hai, định lí Viète, giải bài toán bằng cách lập phương trình). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật phân dạng (bắt buộc)
- MỘT DẠNG = MỘT PHƯƠNG PHÁP GIẢI (một chuỗi bước). Hai ý cùng dạng khi học sinh giải bằng cùng các bước, chỉ khác số liệu, bối cảnh hoặc hình thức (trắc nghiệm/tự luận). Bối cảnh, hình thức, đặc điểm số liệu ghi vào "bien_the", KHÔNG tạo dạng mới.
- Chỉ được dùng mã trong "Danh mục dạng" dưới đây. Ý không thuộc chương VI (rút gọn căn, thể tích hình trụ, hệ phương trình bậc nhất…) ghi mã "NGOAI".
- Đọc kỹ CÁCH LÀM của từng dạng rồi chọn dạng có chuỗi bước khớp nhất với LỜI GIẢI của ý (không chọn theo từ khoá bề mặt). Ví dụ: "A = (x₁ + x₂)(x₁ + 2x₂) − x₂²" khai triển ra đối xứng ⇒ VI-23, không phải hạ bậc. "A = x₁² + 3x₂" phải thay x₁² theo phương trình ⇒ VI-30. "Q = (3x₂ − 1)/x₁ + 3x₁/x₂ − x₁" (đề Sở 2026) cần hạ bậc ⇒ VI-30/VI-31 theo bậc cao nhất phải hạ.
- Câu có vỏ parabol/đường thẳng mà ý hỏi hệ thức của hoành độ giao điểm x₁, x₂ ⇒ gán DẠNG VIÈTE tương ứng, bien_the "vỏ parabol". Chỉ ý hỏi toạ độ giao điểm/tiếp xúc mới là VI-49.
- "Giải phương trình khi m = …" là VI-08 (không phải VI-04).

## Tách ý
- Mỗi yêu cầu riêng (a), b), c)… hoặc 1), 2)…, hoặc các câu hỏi nối nhau trong cùng đề) là MỘT Ý. Câu không chia ý ⇒ một ý, nhan = "".
- Nhiều phương trình/số liệu cùng MỘT yêu cầu và CÙNG DẠNG (vd "Giải các phương trình a) … h) …" đều dùng công thức nghiệm) ⇒ GỘP thành một ý, nhan ghi gộp "a–h". Nếu trong đó có ý khác dạng (vd a) khuyết c, b) đầy đủ) ⇒ tách theo dạng, nhan ghi "a, c" / "b".
- "tom_tat": tối đa 15 chữ, nói ý đó hỏi gì (vd "Tìm m để x₁² + x₂² = 2025").

## Chấm mức (cho học sinh học lực trung bình–khá)
- Mặc định lấy MỨC GỐC của dạng. Chỉ đổi khi ý thật sự dễ/khó hơn chuỗi bước chuẩn của dạng, và PHẢI ghi "ly_do_muc" (tối đa 15 chữ). Mức bằng mức gốc thì ly_do_muc = "".
- Không đổi mức chỉ vì số to, hệ số chứa căn, hay vì nằm trong đề thi vào 10.
- Đổi hợp lệ, ví dụ: VI-28 chỉ hỏi "trái dấu" (ac < 0) ⇒ TH, hỏi "hai nghiệm dương phân biệt" ⇒ VD; VI-15 cho hiệu (hoặc tổng bình phương) và tích ⇒ VD; VI-22 phân thức nhiều tầng ⇒ VD; VI-26 hệ thức phải biến đổi nhiều bước hoặc phải loại nghiệm theo điều kiện phức tạp ⇒ VDC.
- Mức chỉ là NB, TH, VD, VDC.

## Danh mục dạng (mã | mức gốc | tên | cách làm | dấu hiệu)
{DANH_MUC}

## Kiểm lại trước khi nộp
- Đủ MỌI câu trong dữ liệu (đúng "ma"), mỗi câu ít nhất một ý; mọi ý có mã thuộc danh mục hoặc "NGOAI".
- Đọc lại các ý đã gán VI-18…VI-34: dạng có khớp CÁCH LÀM không (đối xứng sẵn / khai triển ra đối xứng / phải hạ bậc / phải xét dấu)?
- Ý nào phân vân giữa hai dạng thì chọn một và ghi vào "ghi_chu" của câu (vd "phân vân VI-22/VI-30"). Không chắc thì cũng ghi.

## Đầu ra
JSON đúng schema: {"cau": [{"ma": …, "y": [{"nhan","tom_tat","ma_dang","muc","bien_the","ly_do_muc"}], "ghi_chu": ""}], "ghi_chu": ""}.
Các cột "dang_cu", "muc_y_cu" trong dữ liệu là nhãn CŨ (viết tự do, nhiều chỗ sai) — chỉ để tham khảo cách tách ý, KHÔNG chép.

## Dữ liệu ({SO} câu, JSON)
'''


def bang_danh_muc(dm):
    dong = []
    for d in dm["dang"]:
        dong.append(f"- {d['ma']} | {d['muc_goc']} | {d['ten']} | {d['cach_lam']} | {d['dau_hieu']}")
    return "\n".join(dong)


def ghi_schema(dm):
    mas = [d["ma"] for d in dm["dang"]] + ["NGOAI"]
    y = {"type": "object", "required": ["nhan", "tom_tat", "ma_dang", "muc", "bien_the", "ly_do_muc"],
         "properties": {"nhan": {"type": "string"}, "tom_tat": {"type": "string"},
                        "ma_dang": {"type": "string", "enum": mas},
                        "muc": {"type": "string", "enum": ["NB", "TH", "VD", "VDC"]},
                        "bien_the": {"type": "string"}, "ly_do_muc": {"type": "string"}}}
    schema = {"type": "object", "required": ["cau", "ghi_chu"],
              "properties": {"cau": {"type": "array", "items": {
                  "type": "object", "required": ["ma", "y", "ghi_chu"],
                  "properties": {"ma": {"type": "string"}, "y": {"type": "array", "minItems": 1, "items": y},
                                 "ghi_chu": {"type": "string"}}}},
                  "ghi_chu": {"type": "string"}}}
    SCHEMA_GOC.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n")


def main():
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]
    ghi_schema(dm)
    rows = json.loads(BANK.read_text())["rows"]
    lo = [rows[i:i + CO_LO] for i in range(0, len(rows), CO_LO)]
    tom = PROMPT.replace("{DANH_MUC}", bang_danh_muc(dm))
    for k, chunk in enumerate(lo, 1):
        data = [{"ma": r["ma"], "de": r["de"], "nguon": r["nguon"], "bai_sgk": r["bai"],
                 "dang_cu": r["dang"], "muc_y_cu": r["muc_y"]} for r in chunk]
        vid = f"{TIEN_TO}{k:02d}"
        viec = {"id": vid, "model": "gemini-4-hydrogen-medium",
                "prompt": tom.replace("{SO}", str(len(data))) + json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                "files": [], "schema": str(SCHEMA_GOC.relative_to(REPO)), "timeout": "1200s",
                "meta": {"loai": "phan-dang-y", "chuong": "lop-9-dai-so-06", "ma": [r["ma"] for r in chunk]}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        if "--thu" not in sys.argv:
            out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(vid, len(data), "câu", len(viec["prompt"]), "kí tự")


if __name__ == "__main__":
    main()
