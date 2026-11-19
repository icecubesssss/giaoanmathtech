#!/usr/bin/env python3
"""Sinh việc Gemini: PHÂN DẠNG LẠI tab "Phân dạng Ch.X lớp 9C" theo danh mục dạng đóng.

Cùng quy trình chương VI, VII, VIII: mỗi câu TÁCH Ý, mỗi ý gán đúng một mã kỹ thuật trong
`danh_muc_dang` của khung (scripts/danh_muc_dang_ch10_9.py) + mức + biến thể. Schema ép mã ∈ danh mục.

    .venv/bin/python scripts/danh_muc_dang_ch10_9.py --ghi
    .venv/bin/python scripts/gemini/viec_phan_dang_y_ch10_9.py [--thu]
    python3 scripts/gemini/tho.py --tien-to pd-y-ch10-9- --song-song 3
    .venv/bin/python scripts/gom_phan_dang_y.py --chuong 10 [--ghi]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_phan_dang_y_ch6_9 import bang_danh_muc  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KHUNG = REPO / "config/khung-phan-dang/lop-9-hinh-hoc-chuong-10.json"
BANK = REPO / "inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10.json"
SCHEMA = REPO / "scripts/gemini/schema/phan-dang-y-ch10.json"
TIEN_TO = "pd-y-ch10-9-"
CO_LO = 37

PROMPT = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm, làm việc PHÂN DẠNG ngân hàng câu hỏi chương X Hình học 9 (KNTT: Bài 31 Hình trụ và hình nón, Bài 32 Hình cầu — khuôn Câu IV.1 đề vào 10 Hà Nội). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật phân dạng (bắt buộc)
- MỘT MÃ = MỘT PHƯƠNG PHÁP GIẢI (một chuỗi bước). Hai ý cùng mã khi học sinh giải bằng cùng các bước, chỉ khác số liệu, bối cảnh (bồn nước, lon, khúc gỗ, quả bóng…), đơn vị, hay hình thức (trắc nghiệm/điền khuyết/tự luận). Những khác biệt đó ghi vào "bien_the", KHÔNG tạo mã mới. Ghi vào bien_the cả các BẪY nếu có: "cho đường kính", "đổi đơn vị lít/m³", "làm tròn lên", "phần trăm".
- Chỉ được dùng mã trong "Danh mục" dưới đây. Ý thuần kiến thức NGOÀI chương X (chỉ hình hộp chữ nhật / lập phương / lăng trụ / chóp của lớp 7–8, chỉ diện tích hình tròn / hình quạt phẳng của chương V, chỉ giải phương trình đại số) ghi mã "NGOAI".
- Đọc CÁCH LÀM của từng mã rồi chọn mã khớp nhất với LỜI GIẢI của ý (không theo bối cảnh):
  · Chỉ gọi tên / chỉ ra bán kính, chiều cao, đường sinh, tâm (kể cả "quay hình chữ nhật quanh cạnh AB thì bán kính đáy là?") ⇒ X-01.
  · Cho sẵn đủ kích thước, thay thẳng MỘT công thức, KHÔNG có bối cảnh thực tế cần đổi đơn vị / tính tiền / phần trăm ⇒ X-02 (trụ), X-03 (nón, đã cho l hoặc h phù hợp), X-04 (cầu). Có bối cảnh thực tế nhưng chỉ hỏi đúng một phép thay công thức (vd "tính thể tích lon nước bán kính 3 cm, cao 12 cm") vẫn có thể là X-02/X-03/X-04 mức NB; nếu phải đổi đơn vị, nhân giá, phần trăm, chọn phần bề mặt ⇒ nhóm thực tế X-08…X-11.
  · Hình nón phải dùng Pythagore tìm l hoặc h trước khi tính, và KHÔNG có bối cảnh thực tế ⇒ X-05; có bối cảnh thực tế (nón lá, ốc quế…) ⇒ X-10 (ghi bien_the "Pythagore tìm l").
  · Biết diện tích / thể tích / chu vi / diện tích mặt cắt / quan hệ h = k·r, tìm ngược r, h, R ⇒ X-06 (cả trong bối cảnh thực tế, nếu bước chính là giải ngược; ghi bien_the).
  · Cuộn tấm phẳng thành trụ / nón, chu vi đáy = độ dài mép ⇒ X-07.
  · Thực tế trụ: hỏi DIỆN TÍCH (sơn, lăn, vỏ hộp, vải, tôn) ⇒ X-08; hỏi THỂ TÍCH / lít / khối lượng / tiền theo thể tích ⇒ X-09. Nón thực tế ⇒ X-10. Cầu thực tế ⇒ X-11.
  · Rót từ vật này sang vật kia, số cốc / số lần đổ / có tràn không / đúc lại khối khác cùng thể tích ⇒ X-12.
  · Thả vật chìm vào bình (nước dâng hoặc tràn), tìm mực dâng / thể tích vật / bán kính bi ⇒ X-13. Ý chỉ hỏi thể tích của viên bi (công thức cầu) ở câu a) trước khi thả thì là X-04 hoặc X-11; ý hỏi nước dâng là X-13.
  · Lật ngược chai, mực nước còn lại sau khi tháo / dùng, chiều cao mực nước khác chiều cao bình ⇒ X-14 (chỉ khi phải lập luận phần nước / phần trống; "bồn chứa nước đến 3/4" chỉ nhân phân số thì vẫn X-09).
  · Vật gồm nhiều khối ghép (cộng) ⇒ X-15; phần còn lại / vỏ / ống / hộp chứa khít các quả cầu (trừ) ⇒ X-16. Quay tam giác quanh cạnh huyền, quay hai tam giác chung đỉnh ⇒ X-15.
  · Mặt nước trong cốc / phễu hình NÓN (r tỉ lệ h, Thales) ⇒ X-17.
  · Khối nội / ngoại tiếp lập phương, chóp, tam giác đều, hình vuông, tính theo tham số ⇒ X-18.
  · Cực trị, Cô-si, lập hệ theo hiệu bán kính, quay hình chữ nhật biết chu vi và diện tích, bồn nằm ngang có viên phân ⇒ X-19.

## Tách ý
- Mỗi yêu cầu riêng (a), b), c)… hoặc 1), 2)…; hoặc các câu hỏi nối nhau trong cùng đề như "tính thể tích … Hỏi cần bao nhiêu tiền") là MỘT Ý khi lời giải cần một kết luận riêng. Bài toán thực tế chỉ có một câu hỏi cuối mà các phép tính trung gian chỉ phục vụ câu đó ⇒ MỘT ý (nhan = ""), chọn mã theo bước quyết định của lời giải.
- Bảng điền nhiều ô (hoàn thành bảng r, h, S, V): mỗi bảng một ý; nếu có cả ô thuận và ô ngược thì chọn X-06 và ghi bien_the "bảng có ô tính ngược".
- "tom_tat": tối đa 15 chữ, nói ý đó hỏi gì (vd "Số ly nước rót được từ bình").

## Chấm mức (cho học sinh học lực trung bình–khá, lớp C)
- Mặc định lấy MỨC GỐC của mã. Chỉ đổi khi ý thật sự dễ/khó hơn chuỗi bước chuẩn, và PHẢI ghi "ly_do_muc" (tối đa 15 chữ). Mức bằng mức gốc thì ly_do_muc = "".
- Hạ NB hợp lệ cho X-08…X-11, X-13: chỉ một phép thay công thức, không đổi đơn vị, không tính tiền, không phần trăm (vd "thả viên bi thể tích cho sẵn 20 cm³, nước dâng bao nhiêu" chỉ một phép chia).
- Nâng VD hợp lệ cho X-08…X-13: chuỗi ≥ 4 bước tính có cả đổi đơn vị lẫn phần trăm / làm tròn theo ngữ cảnh; X-13 khi phải giải R³ để tìm bán kính bi từ mực dâng và đổi đơn vị; X-15, X-16 khi ghép ≥ 3 khối hoặc tính diện tích bề mặt ghép phải bỏ phần tiếp giáp, hoặc tính theo tham số.
- Ma trận đề Sở Hà Nội: Câu IV.1 thường là TH (hai ý NB + TH). Không nâng VD chỉ vì bài dài nhưng mỗi bước đều là thay công thức.
- Mức chỉ là NB, TH, VD, VDC.

## Danh mục (mã | mức gốc | tên | cách làm | dấu hiệu)
{DANH_MUC}

## Kiểm lại trước khi nộp
- Đủ MỌI câu trong dữ liệu (đúng "ma"), mỗi câu ít nhất một ý; mọi ý có mã thuộc danh mục hoặc "NGOAI".
- Ý phân vân giữa hai mã thì chọn một và ghi vào "ghi_chu" của câu (vd "phân vân X-09/X-12").

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
                "meta": {"loai": "phan-dang-y", "chuong": "lop-9-hinh-hoc-10", "ma": [r["ma"] for r in chunk]}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        if "--thu" not in sys.argv:
            out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(vid, len(data), "câu", len(viec["prompt"]), "kí tự")


if __name__ == "__main__":
    main()
