#!/usr/bin/env python3
"""Sinh việc Gemini: PHÂN DẠNG LẠI tab "Phân dạng Ch.VII lớp 9C" theo danh mục dạng đóng.

Cùng quy trình chương VI (viec_phan_dang_y_ch6_9.py): mỗi câu TÁCH Ý, mỗi ý gán đúng một mã kỹ thuật
trong `danh_muc_dang` của khung (scripts/danh_muc_dang_ch7_9.py) + mức + biến thể. Schema ép mã ∈ danh mục.

    .venv/bin/python scripts/danh_muc_dang_ch7_9.py --ghi
    .venv/bin/python scripts/gemini/viec_phan_dang_y_ch7_9.py [--thu]
    python3 scripts/gemini/tho.py --tien-to pd-y-ch7-9- --song-song 3
    .venv/bin/python scripts/gom_phan_dang_y.py --chuong 07 [--ghi]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_phan_dang_y_ch6_9 import bang_danh_muc  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-07.json"
BANK = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07.json"
SCHEMA = REPO / "scripts/gemini/schema/phan-dang-y-ch7.json"
TIEN_TO = "pd-y-ch7-9-"
CO_LO = 36

PROMPT = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm, làm việc PHÂN DẠNG ngân hàng câu hỏi chương VII Đại số 9 (KNTT: Bài 22 bảng tần số và biểu đồ tần số, Bài 23 bảng tần số tương đối và biểu đồ tần số tương đối, Bài 24 bảng tần số, tần số tương đối ghép nhóm và biểu đồ). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật phân dạng (bắt buộc)
- MỘT MÃ = MỘT PHƯƠNG PHÁP GIẢI (một chuỗi bước). Hai ý cùng mã khi học sinh giải bằng cùng các bước, chỉ khác số liệu, bối cảnh, có/không ghép nhóm, hay hình thức (trắc nghiệm/tự luận). Những khác biệt đó ghi vào "bien_the" (vd "ghép nhóm, từ biểu đồ cột", "trắc nghiệm", "dữ liệu chữ"), KHÔNG tạo mã mới.
- Chỉ được dùng mã trong "Danh mục" dưới đây. Ý không thuộc chương VII (xác suất cổ điển của chương VIII, số trung bình/trung vị/mốt, rút gọn căn…) ghi mã "NGOAI".
- Đọc CÁCH LÀM của từng mã rồi chọn mã có chuỗi bước khớp nhất với LỜI GIẢI của ý, không chọn theo từ khoá bề mặt. Phân biệt kỹ:
  · VII-04 chỉ hỏi tần số tương đối của MỘT giá trị/MỘT nhóm (khuôn Câu I.1 đề Sở: "xác định tần số và tần số tương đối của nhóm [a; b)"). Hỏi cả bảng ⇒ VII-05.
  · Nhiều nhóm/giá trị phải CỘNG lại (dưới, trên, ít nhất, không quá, từ … đến …, "hoàn thành trước khi hết giờ trên 20 phút") ⇒ VII-07.
  · Biết % và cỡ mẫu ⇒ tìm số đối tượng (hoặc biết số đối tượng và % ⇒ cỡ mẫu) ⇒ VII-08. Giả sử tỉ lệ không đổi để ước lượng cho mẫu khác, hoặc ước lượng xác suất bằng tần số tương đối ⇒ VII-09.
  · "Lập bảng tần số ghép nhóm từ biểu đồ" là ĐỌC biểu đồ ⇒ VII-02. Chỉ khi phải xếp từng số liệu thô vào nhóm mới là VII-10.
  · Biểu đồ số liệu không phải tần số (doanh thu, sản lượng theo năm, cột kép so sánh hai đại lượng) ⇒ VII-16.
  · Câu hỏi "giá trị/nhóm có tần số lớn nhất" đi kèm bảng/biểu đồ: gộp vào ý đọc/lập bảng cùng câu (VII-01/VII-02), không tách riêng trừ khi là yêu cầu riêng a), b).
- Ý vẽ biểu đồ: cột/đoạn thẳng ⇒ VII-12; hình quạt tròn ⇒ VII-13. Ý vừa lập bảng vừa vẽ mà đề tách a) b) ⇒ hai ý.

## Tách ý
- Mỗi yêu cầu riêng (a), b), c)… hoặc 1), 2)…, hoặc các câu hỏi nối nhau trong cùng đề) là MỘT Ý. Câu không chia ý ⇒ một ý, nhan = "".
- "tom_tat": tối đa 15 chữ, nói ý đó hỏi gì (vd "Tần số tương đối nhóm [12; 16)").

## Chấm mức (cho học sinh học lực trung bình–khá)
- Mặc định lấy MỨC GỐC của mã. Chỉ đổi khi ý thật sự dễ/khó hơn chuỗi bước chuẩn, và PHẢI ghi "ly_do_muc" (tối đa 15 chữ). Mức bằng mức gốc thì ly_do_muc = "".
- Ma trận đề tuyển sinh 10 Hà Nội cho mạch Thống kê KHÔNG có câu vận dụng; Câu I.1 (đọc tần số, tính tần số tương đối một nhóm) là NB. Vì vậy chỉ chấm VD khi ý thật sự phải suy luận nhiều bước KHÔNG có trong chuỗi bước của mã (vd phải dựng lại số liệu từ nhiều điều kiện ràng buộc, so sánh hai mẫu khác cỡ rồi lập luận). Đếm theo điều kiện, ước lượng theo tỉ lệ, tính ngược n = f·N là TH, KHÔNG phải VD.
- Hạ NB hợp lệ: VII-05 bảng chỉ 2–3 giá trị, số chia tròn; VII-07 chỉ cộng 2 nhóm kề nhau đã cho sẵn tần số. Nâng TH hợp lệ: VII-04 khi phải tự đếm cỡ mẫu từ biểu đồ nhiều cột rồi mới tính.
- Mức chỉ là NB, TH, VD, VDC.

## Danh mục (mã | mức gốc | tên | cách làm | dấu hiệu)
{DANH_MUC}

## Kiểm lại trước khi nộp
- Đủ MỌI câu trong dữ liệu (đúng "ma"), mỗi câu ít nhất một ý; mọi ý có mã thuộc danh mục hoặc "NGOAI".
- Mọi ý chấm VD: đọc lại luật chấm mức, nếu thực chất là đếm theo điều kiện / ước lượng theo tỉ lệ thì hạ về TH.
- Ý nào phân vân giữa hai mã thì chọn một và ghi vào "ghi_chu" của câu (vd "phân vân VII-04/VII-07").

## Đầu ra
JSON đúng schema: {"cau": [{"ma": …, "y": [{"nhan","tom_tat","ma_dang","muc","bien_the","ly_do_muc"}], "ghi_chu": ""}], "ghi_chu": ""}.
Các cột "dang_cu", "muc_y_cu" trong dữ liệu là nhãn CŨ (viết tự do, nhiều chỗ sai) — chỉ để tham khảo cách tách ý, KHÔNG chép.

## Dữ liệu ({SO} câu, JSON)
'''


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
    SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n")


def main():
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]
    ghi_schema(dm)
    rows = json.loads(BANK.read_text())["rows"]
    lo = [rows[i:i + CO_LO] for i in range(0, len(rows), CO_LO)]
    tom = PROMPT.replace("{DANH_MUC}", bang_danh_muc(dm))
    for k, chunk in enumerate(lo, 1):
        data = [{"ma": r["ma"], "de": r["de"], "nguon": r["nguon"], "bai_sgk": r["bai"], "ghi_chu_tab": r.get("note", ""),
                 "dang_cu": r["dang"], "muc_y_cu": r["muc_y"]} for r in chunk]
        vid = f"{TIEN_TO}{k:02d}"
        viec = {"id": vid, "model": "gemini-4-hydrogen-medium",
                "prompt": tom.replace("{SO}", str(len(data))) + json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                "files": [], "schema": str(SCHEMA.relative_to(REPO)), "timeout": "1200s",
                "meta": {"loai": "phan-dang-y", "chuong": "lop-9-dai-so-07", "ma": [r["ma"] for r in chunk]}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        if "--thu" not in sys.argv:
            out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(vid, len(data), "câu", len(viec["prompt"]), "kí tự")


if __name__ == "__main__":
    main()
