#!/usr/bin/env python3
"""Sinh 24 việc chạy thử cho thợ Gemini: bóc lại đề CK1 Toán 6 Hà Nội.

Bản ghi chuẩn (Claude đã đọc ảnh, soát tay): inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi/*.json
Thợ KHÔNG được thấy bản ghi chuẩn — chỉ thấy PDF + khung dạng D01–D27.
Chấm bằng scripts/gemini/cham_ck1_lop6.py.

    python3 scripts/gemini/viec_ck1_lop6.py [--model gemini-3.8-flash-high] [--chi l6-ck1-2425-banmai]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BAN_GHI = REPO / "inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi"
KHO_PDF = REPO / "inputs/refs/de-thi/lop-6/cuoi-ki-1"
KHUNG = REPO / "config/khung-phan-dang/lop-6-ck1-kntt.json"
HANG_DOI = REPO / "storage/gemini/hang-doi"

MAU = """Bạn là thợ nhập liệu đề thi Toán. Làm CẨN THẬN, ĐỦ, KHÔNG BỊA.

Trong thư mục làm việc có một đề kiểm tra cuối học kì I Toán 6 (Hà Nội), có thể kèm
hướng dẫn chấm (HDC), đã tách sẵn thành:
  - ảnh từng trang: trang-1.png, trang-2.png, … (hoặc trang-01.png …) — NGUỒN CHÍNH, hãy MỞ XEM TỪNG ẢNH;
  - {txt}: lớp chữ trích tự động, hay MẤT kí hiệu (ℕ, ℤ, phân số, luỹ thừa) — chỉ dùng để đối chiếu.
KHÔNG chạy lệnh shell (bị cấm). Chỉ dùng công cụ xem/đọc file.

VIỆC: xem HẾT mọi ảnh trang, rồi ghi MỖI Ý CHẤM ĐIỂM của đề thành một phần tử trong mảng "cau".

QUY TẮC
1. Nhãn "cau":
   - Phần trắc nghiệm (gồm cả câu điền, câu đúng/sai nằm trong phần I): "I.1", "I.2", …
   - Phần tự luận: "II.<bài><ý>", ví dụ "II.1a", "II.2c"; bài có mục con 1), 2): "II.3.1", "II.4.2a".
   - Nếu đề KHÔNG chia phần I/II (toàn tự luận): bỏ tiền tố, ví dụ "1a", "4.2b", "5".
   - Mỗi ý nhỏ a), b), c) là MỘT phần tử riêng. Không gộp, không bỏ ý nào.
2. "ht": TN (trắc nghiệm nhiều lựa chọn) | TL (tự luận) | Điền (điền vào chỗ trống) | Đ-S (đúng/sai).
3. "diem": điểm của ý. Lấy từ đề hoặc HDC. Nếu đề chỉ ghi điểm cả bài, chia hợp lý cho các ý và
   đặt "diem_uoc": true. TỔNG ĐIỂM CÁC Ý PHẢI BẰNG 10 — tự cộng lại kiểm tra trước khi trả lời.
4. "muc": NB (nhận biết: nhớ, đọc ra ngay) | TH (thông hiểu: làm 1–2 bước quen thuộc) |
   VD (vận dụng: nhiều bước, bài toán thực tế) | VDC (vận dụng cao: câu khó cuối đề, cần suy luận riêng).
5. "dang": chọn ĐÚNG MỘT mã trong khung dạng dưới đây (mã gần nhất nếu không khớp hoàn toàn).
6. "nd": chép tóm tắt nội dung ý (đủ để nhận ra câu; trắc nghiệm ghi cả 4 phương án).
7. "dap_an": trắc nghiệm ghi chữ cái A/B/C/D; tự luận ghi đáp số cuối. Lấy từ HDC nếu có;
   không có HDC thì TỰ GIẢI và kiểm tra lại. Không chắc ⇒ ghi vào "can_soat".
8. "co_hinh": true nếu ý dựa vào hình vẽ trong đề.
9. Đề có nhiều mã đề / phần riêng theo hệ lớp: chỉ ghi mã đề đầu tiên và phần dành cho hệ thường;
   nói rõ trong "ghi_chu_de".
10. "so_trang_da_doc": số trang PDF bạn đã thực sự đọc. "de": "{ma}".

KHUNG DẠNG (mã — chủ đề — tên dạng):
{khung}

Chỉ trả về MỘT đối tượng JSON đúng schema, không thêm lời.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    ap.add_argument("--chi", nargs="*", help="chỉ sinh các mã đề này")
    a = ap.parse_args()
    khung = json.loads(KHUNG.read_text())
    dong = "\n".join(f"{d['ma']} — CĐ{d['cd']} — {d['ten']}" for d in khung["dang"])
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(BAN_GHI.glob("*.json")):
        bg = json.loads(f.read_text())
        if a.chi and bg["de"] not in a.chi:
            continue
        pdf = KHO_PDF / bg["pdf"]
        assert pdf.exists(), pdf
        viec = {
            "id": bg["de"],
            "model": a.model,
            "prompt": MAU.format(txt=pdf.stem + ".txt", ma=bg["de"], khung=dong),
            "files": [str(pdf.relative_to(REPO))],
            "render": True,
            "schema": "scripts/gemini/schema/ban-ghi-de.json",
            "timeout": "900s",
        }
        (HANG_DOI / f"{bg['de']}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        n += 1
    print(f"Đã ghi {n} việc vào {HANG_DOI.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
