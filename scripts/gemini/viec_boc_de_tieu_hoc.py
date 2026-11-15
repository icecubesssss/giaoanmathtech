#!/usr/bin/env python3
"""Sinh việc "bóc đề" TIỂU HỌC cho thợ Gemini (khởi đầu: lớp 5, 15/11/2026).

    python3 scripts/gemini/viec_boc_de_tieu_hoc.py --lop 5 --ky ck1 gk1
    python3 scripts/gemini/tho.py --song-song 3          # Claude tự chạy (allowed_domains googleapis)

Khác bản THCS (viec_boc_de.py): đề mọi tỉnh (luật tiểu học 10/11), bản ghi có thêm "cd" (chủ đề SGK) và
"bai" (số bài SGK KNTT) như ngân hàng lớp 3, 4; mã dạng lấy từ config/khung-phan-dang/tieu-hoc-lop-N-kntt.json.
Kết quả thợ ⇒ soát rồi ghi vào inputs/refs/ngan-hang-sheet/tieu-hoc/lop-N/ban-ghi/<ma>.json
(scripts/gemini/ap_boc_de_tieu_hoc.py).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANG_DOI = REPO / "storage/gemini/hang-doi"
THU_MUC = {"gk1": "giua-ki-1", "ck1": "cuoi-ki-1", "gk2": "giua-ki-2", "ck2": "cuoi-ki-2"}
TEN_KY = {"gk1": "giữa học kì I", "ck1": "cuối học kì I", "gk2": "giữa học kì II", "ck2": "cuối học kì II"}

MAU = """Bạn là thợ nhập liệu đề kiểm tra Toán TIỂU HỌC. Làm CẨN THẬN, ĐỦ, KHÔNG BỊA.

Trong thư mục làm việc có MỘT đề kiểm tra {ten_ky} Toán lớp {lop} của một trường tiểu học (ảnh chụp đề gốc),
đã tách sẵn thành ảnh từng trang trang-1.png, trang-2.png, … — NGUỒN DUY NHẤT, hãy MỞ XEM TỪNG ẢNH.
(File .txt nếu có thường RỖNG vì là ảnh chụp.) KHÔNG chạy lệnh shell (bị cấm). Chỉ dùng công cụ xem/đọc file.

VIỆC: xem HẾT mọi ảnh trang, rồi ghi MỖI Ý CHẤM ĐIỂM của đề thành một phần tử trong mảng "cau".

QUY TẮC
1. Nhãn "cau": đánh như đề in. Đề chia phần trắc nghiệm / tự luận: "I.1", "I.2", … và "II.1a", "II.2b"…;
   đề đánh số liền "Câu 1 … Câu 10": "1", "2", … ý nhỏ "7a", "7b". Câu Đúng/Sai nhiều ý: mỗi ý một phần tử ("4a", "4b").
   Mỗi ý nhỏ a), b), c), d) là MỘT phần tử riêng. Không gộp, không bỏ ý nào. Câu nối/điền nhiều ô: một phần tử.
2. "ht": TN (khoanh/chọn A B C D) | TL (tự luận, đặt tính, bài giải) | Điền (điền chỗ chấm, nối) | Đ-S (đúng/sai).
3. "diem": điểm của ý, lấy từ đề hoặc hướng dẫn chấm. Đề chỉ ghi điểm cả bài ⇒ chia đều cho các ý,
   đặt "diem_uoc": true. TỔNG ĐIỂM CÁC Ý PHẢI BẰNG 10 — tự cộng lại kiểm tra.
4. "muc" (Thông tư 27 đổi sang): NB = M1 (nhận biết, một bước: đọc số, giá trị chữ số, nhận dạng hình, đổi đơn vị một bước,
   đặt tính một phép); TH = M2 (hai–ba bước quen thuộc: biểu thức, tìm x, diện tích áp công thức, đổi đơn vị hai bước);
   VD = M3 (bài toán có lời văn nhiều bước, bài thực tế); VDC = câu tư duy cuối đề (thường 0,5–1 điểm, cần mẹo).
   Đề có ghi mức M1/M2/M3 thì theo đề. KHÔNG nâng mức.
5. "cd" và "bai": số CHỦ ĐỀ và số BÀI trong SGK Toán {lop} Kết nối tri thức (mục lục bên dưới) mà ý đó thuộc về.
   Đề trường dùng bộ sách khác vẫn phải gán vào bài KNTT gần nhất. Nội dung chỉ có ở kì II (tỉ số phần trăm, thể tích,
   vận tốc, thống kê…) ⇒ gán đúng chủ đề kì II và mã dạng D90.
6. "dang": chọn ĐÚNG MỘT mã trong KHUNG DẠNG. Ý thuộc BÀI CÓ LỜI VĂN / bối cảnh thực tế: diện tích ruộng, vườn ⇒ D22;
   tiền, khối lượng, rút về đơn vị ⇒ D23. Câu tư duy cuối đề ⇒ D25. Không khớp mã nào ⇒ "D99" và nói lí do trong "can_soat".
7. "nd": chép nội dung ý đủ để nhận ra câu, GIỮ NGUYÊN SỐ LIỆU (dấu phẩy thập phân viết "," như đề);
   trắc nghiệm ghi cả 4 phương án "A. … B. … C. … D. …". Bài có lời dẫn chung: chép lời dẫn vào ý ĐẦU TIÊN của bài.
   Phân số viết a/b, hỗn số "2 3/4", mũ viết m2, km2.
8. "dap_an": TN ghi chữ cái; Đ-S ghi Đ hoặc S; tự luận ghi đáp số cuối. Không có hướng dẫn chấm thì TỰ GIẢI và kiểm tra lại.
   Đề in sai/thiếu dữ kiện, hoặc HDC lệch đề ⇒ ghi theo đề in và nói rõ trong "can_soat". Không chắc ⇒ "can_soat".
9. "co_hinh": true nếu ý dựa vào hình vẽ trong đề (mô tả hình ngắn gọn trong "nd").
10. Đề có hai mã A/B: chỉ ghi mã đề đầu tiên, nói rõ trong "ghi_chu_de". "ghi_chu_de" ghi thêm: tên trường, tỉnh,
    thời gian làm bài, cấu trúc điểm (ví dụ "TN 8 câu × 0,5 = 4đ; TL 6đ: …").
11. "so_trang_da_doc": số ảnh trang bạn đã thực sự mở xem. "de": "{ma}".

MỤC LỤC SGK TOÁN {lop} KNTT (CĐ — bài):
{muc_luc}

KHUNG DẠNG (mã — CĐ — tên dạng):
{khung}

Chỉ trả về MỘT đối tượng JSON đúng schema, không thêm lời.
"""

BO_TIEN_TO = ["tieu-hoc-", "ptdtbt-th-thcs-", "th-thcs-", "ubnd-xa-", "ubnd-phuong-", "thdl-", "th-"]


def ma_de(lop: int, ky: str, pdf: Path) -> str | None:
    m = re.search(r"nam-(\d{4})-(\d{4})-(.+)$", pdf.stem)
    if not m:
        return None
    truong = m.group(3)
    for t in BO_TIEN_TO:
        if truong.startswith(t):
            truong = truong[len(t):]
            break
    # bỏ tên tỉnh ở đuôi (giữ 1 từ đặc trưng trường)
    truong = re.sub(r"-(son-la|ninh-binh|ha-noi|long-an|hai-phong|dong-thap|thanh-hoa|hung-yen|quang-ngai|lam-dong|"
                    r"vinh-phuc|phu-tho)$", "", truong)
    return f"l{lop}-{ky}-{m.group(1)[2:]}{m.group(2)[2:]}-{truong.replace('-', '')}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True)
    ap.add_argument("--ky", nargs="+", required=True, choices=TEN_KY)
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    a = ap.parse_args()

    kp = f"config/khung-phan-dang/tieu-hoc-lop-{a.lop}-kntt.json"
    khung = json.loads((REPO / kp).read_text())
    dong = "\n".join(f"{d['ma']} — CĐ{d['cd']} — {d['ten']}" for d in khung["dang"])
    muc = "\n".join(f"CĐ{c['so']} {c['ten']} ({c['hoc_ki_sgk']}): " +
                    "; ".join(f"B{b['so']} {b['ten']}" for b in c["bai"]) for c in khung["chu_de"])
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    n = 0
    for ky in a.ky:
        for pdf in sorted((REPO / f"inputs/refs/de-thi/lop-{a.lop}/{THU_MUC[ky]}").glob("*.pdf")):
            ma = ma_de(a.lop, ky, pdf)
            if not ma:
                continue
            viec = {
                "id": ma, "model": a.model,
                "prompt": MAU.format(ten_ky=TEN_KY[ky], lop=a.lop, ma=ma, muc_luc=muc, khung=dong),
                "files": [str(pdf.relative_to(REPO))],
                "render": True,
                "schema": "scripts/gemini/schema/ban-ghi-de-tieu-hoc.json",
                "timeout": "1200s",
                "meta": {"lop": a.lop, "ky": ky, "pdf": str(pdf.relative_to(REPO)), "khung": kp},
            }
            (HANG_DOI / f"{ma}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
            print(ma)
            n += 1
    print(f"Đã ghi {n} việc vào {HANG_DOI.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
