#!/usr/bin/env python3
"""Sinh việc Gemini: PHÂN DẠNG LẠI tab "Phân dạng Ch.VIII lớp 9C" theo danh mục dạng đóng.

Cùng quy trình chương VI & VII: mỗi câu TÁCH Ý, mỗi ý gán đúng một mã kỹ thuật trong
`danh_muc_dang` của khung (scripts/danh_muc_dang_ch8_9.py) + mức + biến thể. Schema ép mã ∈ danh mục.

    .venv/bin/python scripts/danh_muc_dang_ch8_9.py --ghi
    .venv/bin/python scripts/gemini/viec_phan_dang_y_ch8_9.py [--thu]
    python3 scripts/gemini/tho.py --mot pd-y-ch8-9-01
    python3 scripts/gemini/tho.py --tien-to pd-y-ch8-9- --song-song 3
    .venv/bin/python scripts/gom_phan_dang_y.py --chuong 08 [--ghi]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_phan_dang_y_ch6_9 import bang_danh_muc  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-08.json"
BANK = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08.json"
SCHEMA = REPO / "scripts/gemini/schema/phan-dang-y-ch8.json"
TIEN_TO = "pd-y-ch8-9-"
CO_LO = 35

PROMPT = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm, làm việc PHÂN DẠNG ngân hàng câu hỏi chương VIII Đại số 9 (KNTT: Bài 25 Phép thử ngẫu nhiên và không gian mẫu, Bài 26 Xác suất của biến cố liên quan tới phép thử). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật phân dạng (bắt buộc)
- MỘT MÃ = MỘT PHƯƠNG PHÁP GIẢI (một chuỗi bước). Hai ý cùng mã khi học sinh giải bằng cùng các bước, chỉ khác số liệu, bối cảnh (rút thẻ, lấy bóng/bi, quay đĩa, gieo xúc xắc, chọn sách/người), điều kiện số (chia hết, chia dư, nguyên tố, chính phương, biến cố "không"), hay hình thức (trắc nghiệm/đúng sai/tự luận). Những khác biệt đó ghi vào "bien_the", KHÔNG tạo mã mới.
- Chỉ được dùng mã trong "Danh mục" dưới đây. Ý thuần thống kê chương VII (cỡ mẫu, tần số, tần số tương đối như ý a của ck2-doan-thi-diem-2025-3) ghi mã "NGOAI".
- Đọc CÁCH LÀM của từng mã rồi chọn mã khớp nhất với lời giải của ý:
  · Ý hỏi "Phép thử là gì?", "Kết quả của phép thử là gì?", "Có phải phép thử ngẫu nhiên không?", "Có đồng khả năng không?", "Biến cố nào xảy ra?" ⇒ VIII-01. (Nếu một ý ghép "Phép thử và kết quả là gì?" thì gộp vào 1 ý VIII-01; nếu đề tách riêng "a) Phép thử là gì? b) Mô tả không gian mẫu" thì tách rõ.)
  · Ý chỉ hỏi viết/đếm không gian mẫu một hành động (chưa tính xác suất): tập nền cho sẵn (thẻ/bi 1..n, đĩa quay, xúc xắc, danh sách) ⇒ VIII-02; tự liệt kê từ điều kiện số ("số có hai chữ số < 30", "số lẻ hai chữ số", "số chính phương < 60") ⇒ VIII-03.
  · Ý chỉ hỏi liệt kê / đếm kết quả thuận lợi (chưa hỏi xác suất) ⇒ VIII-04.
  · Ý hỏi mô tả không gian mẫu / số phần tử n(Ω) của phép thử HAI hành động độc lập / có hoàn lại (bảng hai chiều / sơ đồ cây) mà chưa tính xác suất ⇒ VIII-05. (Nếu hai hành động LẤY LẦN LƯỢT KHÔNG HOÀN LẠI như sgk-b25-vd2, sgk-8.2, tl-ptnn-xsbc-9, 10 ⇒ VIII-12; nếu XẾP THỨ TỰ 3–4 người như sgk-8.4, tl-ptnn-xsbc-6 ⇒ VIII-11; nếu ĐỒNG THỜI 2 vật như tl-ptnn-xsbc-15a, 47a ⇒ VIII-10.)
  · Tính xác suất 1 hành động: tập nền cho sẵn (thẻ, bi/bóng, đĩa quay, 1 xúc xắc, chọn 1 quyển sách/người) ⇒ VIII-06; phải tự liệt kê tập nền từ mô tả điều kiện số (viết/chọn số tự nhiên có 2 chữ số, số lẻ < 40…) ⇒ VIII-07 (kể cả khi ý a đã liệt kê Ω ở bài tự luận); chọn 1 đối tượng từ bảng thống kê / biểu đồ / tỉ lệ phần trăm cho sẵn ⇒ VIII-08.
  · Lưu ý câu lặp phép thử N lần: "Nếu lặp lại 120 lần thì có bao nhiêu lần..." dựa vào xác suất lý thuyết vừa tính (như v10-tho-loc-l2-2025-I2) thuộc VIII-06 (ghi bien_the "kèm ước lượng số lần lặp 120 lần"); chỉ khi đề cho kết quả đã thực nghiệm N lần và hỏi xác suất thực nghiệm / ước lượng ngược số bi (như v10-to-vinh-dien-2025-I1, v10-cat-linh-2025-I2) mới là VIII-15.
  · Tính xác suất 2 hành động độc lập / có hoàn lại (2 xúc xắc, 2 túi thẻ, đồng xu + thẻ/xúc xắc, quay đĩa 2 lần, 2 người chọn ngày/quán, giới tính 2 con, lai gene, tung đồng xu 2 lần, chọn 1 điểm đỏ + 1 điểm xanh) ⇒ VIII-09.
  · Lấy ĐỒNG THỜI / cùng lúc 2 vật từ cùng 1 hộp/nhóm (không hoàn lại, không phân biệt thứ tự) ⇒ VIII-10.
  · Xếp thứ tự / hoán vị 3–4 đối tượng (ghế, thanh toán, thứ tự làm bài, rút hết 3 bi) ⇒ VIII-11.
  · Lấy lần lượt KHÔNG hoàn lại (người 1 lấy trước, không trả lại; hoặc đề ghi rõ "lần lượt không trả lại") ⇒ VIII-12. (Chú ý tl-ptnn-xsbc-25, 29 hai bạn lần lượt lấy từ 1 hộp/giá: nếu là lấy lần lượt không trả lại ⇒ VIII-12.)
  · Biết xác suất (hoặc tỉ lệ hai xác suất) tìm số phần tử / số bóng / số thẻ ⇒ VIII-13.
  · Phép thử ≥ 3 hành động (tung đồng xu 3 lần, 3 hộp thẻ, vé 4 chữ số) hoặc bài đếm tổ hợp/hình học nâng cao (3 đoạn thẳng lập tam giác, điểm nguyên Oxy, bài toán chia 3 số dư hoặc tìm số cá bằng lập phương trình rồi liệt kê Ω) ⇒ VIII-14.
  · So sánh khả năng xảy ra của các biến cố (chỉ hỏi biến cố nào khả năng cao hơn) ⇒ VIII-16.

## Tách ý
- Mỗi yêu cầu riêng (a), b), c)… hoặc 1), 2)… hoặc A), B), E), F), G)… hoặc các biến cố độc lập nối nhau trong cùng đề) là MỘT Ý. Câu không chia ý ⇒ một ý, nhan = "".
- Nếu 1 câu tự luận hỏi gộp "a) Tính xác suất của các biến cố E, F, G" không đánh nhãn phụ cho câu khác, hoặc mỗi biến cố E/F/G là 1 phép tính xác suất riêng: tách từng biến cố E, F, G thành từng ý (nhan = "E", "F", "G") nếu đó là các câu hỏi tính xác suất riêng; ngược lại nếu đề trắc nghiệm đúng/sai 4 ý a,b,c,d thì tách đủ 4 ý. Nếu câu a) là một biểu thức hỏi cả hai việc "Viết tập hợp Ω và tìm n(Ω)" thì giữ 1 ý ("a").
- "tom_tat": tối đa 15 chữ, nói ý đó hỏi gì (vd "Xác suất chọn được thẻ chia 6 dư 2").

## Chấm mức (cho học sinh học lực trung bình–khá)
- Mặc định lấy MỨC GỐC của mã. Chỉ đổi khi ý thật sự dễ/khó hơn chuỗi bước chuẩn, và PHẢI ghi "ly_do_muc" (tối đa 15 chữ). Mức bằng mức gốc thì ly_do_muc = "".
- Quy tắc quan trọng cho VIII-06 (mức gốc TH — khớp chuẩn Câu I.2 của Sở HN):
  · Hạ NB hợp lệ khi chỉ cần 1 bước trực tiếp: tính theo nhóm màu/loại cho sẵn không phải lọc số (vd "lấy bi đỏ trong 800 đỏ / 2025 bi", "chọn sách Toán trong 3 Toán, 3 Văn, 2 Anh"), hoặc gieo 1 xúc xắc / quay đĩa ≤ 10 phần / rút thẻ với 1 điều kiện sơ cấp đếm thẳng (chẵn, lẻ, lớn hơn k, chia hết trong dãy nhỏ ≤ 10), hoặc câu trắc nghiệm 1 bước.
  · Giữ TH khi phải viết đủ lập luận trình bày tự luận (khuôn Câu I.2 Sở HN) hoặc phải xét tính chất số (số nguyên tố, số chính phương, chia k dư r, ghép 2 điều kiện "và"/"hoặc", hoặc tự cộng các nhóm).
- Hạ NB hợp lệ cho VIII-08: bảng thống kê / tỉ lệ % đọc trực tiếp 1 con số (vd 35% ⇒ 0,35, hoặc 1 bảng 1 giá trị).
- Nâng VD hợp lệ: VIII-09 khi là trò chơi so sánh hai tập 36 ô (sgk-8.17), tính điểm nhiều bước trên kết quả (v10-tho-loc-l3-2026-I2b), biến cố phức tạp cần phần bù trên nhiều điều kiện hoặc tung 2 xúc xắc trắc nghiệm đúng/sai ý tổng hợp; VIII-11 khi xếp 4 đối tượng (24 hoán vị); VIII-10 khi có nhiều biến cố phức tạp.
- Hạ TH hợp lệ cho VIII-13: biết tổng số vật N và xác suất P, chỉ cần nhân N·P (như tl-ptnn-xsbc-75).
- Mức chỉ là NB, TH, VD, VDC.

## Danh mục (mã | mức gốc | tên | cách làm | dấu hiệu)
{DANH_MUC}

## Kiểm lại trước khi nộp
- Đủ MỌI câu trong dữ liệu (đúng "ma"), mỗi câu ít nhất một ý; mọi ý có mã thuộc danh mục hoặc "NGOAI".
- Ý phân vân giữa hai mã thì chọn một và ghi vào "ghi_chu" của câu (vd "phân vân VIII-06/VIII-07").

## Đầu ra
JSON đúng schema: {"cau": [{"ma": …, "y": [{"nhan","tom_tat","ma_dang","muc","bien_the","ly_do_muc"}], "ghi_chu": ""}], "ghi_chu": ""}.
Các cột "dang_cu", "muc_y_cu" trong dữ liệu là nhãn CŨ — chỉ để tham khảo, KHÔNG chép.

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
                "meta": {"loai": "phan-dang-y", "chuong": "lop-9-dai-so-08", "ma": [r["ma"] for r in chunk]}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if "--thu" not in sys.argv:
            out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(vid, len(data), "câu", len(viec["prompt"]), "kí tự")


if __name__ == "__main__":
    main()
