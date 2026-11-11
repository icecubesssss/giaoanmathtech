#!/usr/bin/env python3
"""Sinh việc "bóc đề" cho thợ Gemini — dùng chung mọi khối/kì (không cần bản ghi chuẩn).

    python3 scripts/gemini/viec_boc_de.py --lop 7 --ky ck1 \
        --khung config/khung-phan-dang/lop-7-ck1-kntt.json \
        --thu-muc inputs/refs/de-thi/lop-7/cuoi-ki-1 inputs/refs/de-thi-lech-kntt/lop-7/cuoi-ki-1 \
        --nam 2024-2025 2025-2026

Mỗi PDF Hà Nội đúng năm ⇒ một việc storage/gemini/hang-doi/l<lop>-<ky>-<nn>-<truong>.json.
Thầy chạy: python3 scripts/gemini/tho.py --song-song 3
Claude soát: python3 scripts/gemini/soat_boc_de.py --lop 7 --ky ck1 ...
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANG_DOI = REPO / "storage/gemini/hang-doi"
TEN_KY = {"gk1": "giữa học kì I", "ck1": "cuối học kì I", "gk2": "giữa học kì II", "ck2": "cuối học kì II"}

MAU = """Bạn là thợ nhập liệu đề thi Toán. Làm CẨN THẬN, ĐỦ, KHÔNG BỊA.

Trong thư mục làm việc có một đề kiểm tra {ten_ky} Toán {lop} (Hà Nội), có thể kèm
hướng dẫn chấm (HDC), đã tách sẵn thành:
  - ảnh từng trang: trang-1.png, trang-2.png, … (hoặc trang-01.png …) — NGUỒN CHÍNH, hãy MỞ XEM TỪNG ẢNH;
  - {txt}: lớp chữ trích tự động, hay MẤT kí hiệu (ℚ, ℝ, căn, phân số, luỹ thừa) hoặc RỖNG
    với bản scan — chỉ dùng để đối chiếu.
KHÔNG chạy lệnh shell (bị cấm). Chỉ dùng công cụ xem/đọc file.

VIỆC: xem HẾT mọi ảnh trang, rồi ghi MỖI Ý CHẤM ĐIỂM của đề thành một phần tử trong mảng "cau".

QUY TẮC
1. Nhãn "cau":
   - Phần trắc nghiệm (gồm cả câu điền, câu đúng/sai nằm trong phần I): "I.1", "I.2", …
   - Phần tự luận: "II.<bài><ý>", ví dụ "II.1a", "II.2c"; bài có mục con 1), 2): "II.3.1", "II.4.2a".
   - Nếu đề KHÔNG chia phần I/II (toàn tự luận): bỏ tiền tố, ví dụ "1a", "4.2b", "5".
   - Câu đúng/sai có nhiều ý a, b, c, d: mỗi ý một phần tử ("I.9a", "I.9b", …).
   - Mỗi ý nhỏ a), b), c) là MỘT phần tử riêng. Không gộp, không bỏ ý nào.
   - Bài hình: ý "vẽ hình, ghi GT–KL" có điểm riêng thì ghi thành một phần tử riêng (nhãn "II.4hinh").
2. "ht": TN (trắc nghiệm nhiều lựa chọn) | TL (tự luận) | Điền (điền vào chỗ trống) | Đ-S (đúng/sai).
3. "diem": điểm của ý. Lấy từ đề hoặc HDC. Nếu đề chỉ ghi điểm cả bài, chia hợp lí cho các ý và
   đặt "diem_uoc": true. TỔNG ĐIỂM CÁC Ý PHẢI BẰNG 10 — tự cộng lại kiểm tra trước khi trả lời.
   Bài "chọn 1 trong 2" / "học sinh chọn một câu": chỉ ghi MỘT phần tử mang đủ điểm của bài,
   nội dung ghi cả hai lựa chọn, thêm "can_soat": "chọn 1 trong 2".
4. "muc" — KHÔNG nâng mức:
   NB = nhận biết, đọc ra ngay hoặc tính MỘT bước (cộng trừ hai số, tìm x một bước, nhận dạng hình,
        đọc số liệu biểu đồ, kí hiệu tam giác bằng nhau);
   TH = hai–ba bước quen thuộc (biểu thức có ngoặc, tìm x hai bước, chứng minh tam giác bằng nhau trực tiếp);
   VD = nhiều bước, bài thực tế, suy luận hình từ tam giác bằng nhau;
   VDC = câu khó cuối đề, cần ý tưởng riêng (thường 0,5 điểm).
5. "dang": chọn ĐÚNG MỘT mã trong khung dạng dưới đây. Luật phân xử khi hai mã cùng hợp:
   - ý thuộc một BÀI THỰC TẾ (có bối cảnh đời sống) ⇒ dùng mã "bài toán thực tế" của chủ đề đó,
     kể cả khi ý đó chỉ áp công thức;
   - câu VDC cuối đề ⇒ dùng mã VDC, không dùng mã thường;
   - không khớp mã nào ⇒ "D99" và nói lí do trong "can_soat".
6. "nd": chép tóm tắt nội dung ý (đủ để nhận ra câu; trắc nghiệm ghi cả 4 phương án).
   Bài có lời dẫn chung (bài hình, bài thực tế): chép lời dẫn vào ý ĐẦU TIÊN của bài.
7. "dap_an": trắc nghiệm ghi chữ cái A/B/C/D; đúng/sai ghi Đ hoặc S; tự luận ghi đáp số cuối
   (bài chứng minh ghi "chứng minh"). Lấy từ HDC nếu có; không có HDC thì TỰ GIẢI và kiểm tra lại.
   Đề in và HDC lệch nhau ⇒ ghi đáp án theo đề in, nói rõ trong "can_soat". Không chắc ⇒ "can_soat".
8. "co_hinh": true nếu ý dựa vào hình vẽ/biểu đồ trong đề.
9. Đề có nhiều mã đề / phần riêng theo hệ lớp: chỉ ghi mã đề đầu tiên và phần dành cho hệ thường;
   nói rõ trong "ghi_chu_de".
10. "so_trang_da_doc": số ảnh trang bạn đã thực sự mở xem. "de": "{ma}".

KHUNG DẠNG (mã — chương — tên dạng; [ngoài tập 1] = nội dung KNTT học kì II mà một số trường vẫn ra):
{khung}

Chỉ trả về MỘT đối tượng JSON đúng schema, không thêm lời.
"""

BO_TIEN_TO = ["truong-thcs-", "truong-", "phong-gddt-", "xa-", "cum-chuyen-mon-so-", "he-thong-gd-"]


def ma_de(lop: int, ky: str, pdf: Path) -> str | None:
    s = pdf.stem
    if not s.endswith("-ha-noi"):
        return None
    m = re.search(r"nam-(\d{4})-(\d{4})-(.+)-ha-noi$", s)
    if not m:
        return None
    truong = m.group(3)
    for t in BO_TIEN_TO:
        if truong.startswith(t):
            truong = ("cum" if t == "cum-chuyen-mon-so-" else "") + truong[len(t):]
            break
    truong = truong.replace("m-v-lomonoxop", "lomonoxop").replace("ban-mai-school", "banmai").replace("-", "")
    return f"l{lop}-{ky}-{m.group(1)[2:]}{m.group(2)[2:]}-{truong}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True)
    ap.add_argument("--ky", required=True, choices=TEN_KY)
    ap.add_argument("--khung", required=True)
    ap.add_argument("--thu-muc", nargs="+", required=True)
    ap.add_argument("--nam", nargs="+", default=["2024-2025", "2025-2026"])
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()

    khung = json.loads((REPO / a.khung).read_text())
    dong = "\n".join(
        f"{d['ma']} — CĐ{d['cd']} — {d['ten']}" + (" [ngoài tập 1]" if d.get("ngoai_tap_1") else "")
        for d in khung["dang"])
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    ds = []
    for td in a.thu_muc:
        for pdf in sorted((REPO / td).glob("*.pdf")):
            if not any(f"nam-{n}-" in pdf.name for n in a.nam):
                continue
            ma = ma_de(a.lop, a.ky, pdf)
            if not ma:
                continue
            ds.append((ma, pdf))
    trung = {m for m, _ in ds if sum(1 for x, _ in ds if x == m) > 1}
    assert not trung, f"mã đề trùng: {trung}"
    for ma, pdf in ds:
        viec = {
            "id": ma, "model": a.model,
            "prompt": MAU.format(ten_ky=TEN_KY[a.ky], lop=a.lop, txt=pdf.stem + ".txt", ma=ma, khung=dong),
            "files": [str(pdf.relative_to(REPO))],
            "render": True,
            "schema": "scripts/gemini/schema/ban-ghi-de.json",
            "timeout": "900s",
            "meta": {"lop": a.lop, "ky": a.ky, "pdf": pdf.name, "thu_muc": str(pdf.parent.relative_to(REPO)),
                     "khung": a.khung},
        }
        (HANG_DOI / f"{ma}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print(ma)
    print(f"Đã ghi {len(ds)} việc vào {HANG_DOI.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
