#!/usr/bin/env python3
"""Việc Gemini: bốc thêm bài cho phiếu E ch.VI 9C đủ giờ, tỉ lệ 40-40-20 (Thầy 13/11/2026: "bốc thêm bài thôi").

Đích (rate lớp 9 ĐS): trên lớp NB ~32 thẻ / TH 8 / VD 2 (120′); BTVN NB ~22 / TH 8 / VD 2 (90′).
Hiện có: trên lớp NB 15 thẻ (9 bài), TH 3, VD 2; BTVN NB 3 thẻ (2 bài), TH 3, VD 2.

    python3 scripts/gemini/viec_boc_them_phieu_e_9c.py
    python3 scripts/gemini/tho.py --mot boc-them-9c-ch6-phieu-e-lop   (và -btvn)
    python3 scripts/gemini/lap_boc_them_phieu_e_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json"
VID_LOP, VID_BTVN = "boc-them-9c-ch6-phieu-e-lop", "boc-them-9c-ch6-phieu-e-btvn"

CHUNG = r'''Bạn là thợ soạn phiếu Toán 9 (Bài 21 "Giải bài toán bằng cách lập phương trình", học sinh lớp 9 TẦNG C). TUYỆT ĐỐI KHÔNG chạy lệnh, KHÔNG dùng công cụ — tự tính nhẩm. Dữ liệu ở cuối prompt.

## Việc chung: soạn THÊM bài mới cho đủ giờ. Ba dạng (mạch): "nang-suat" (kế hoạch/thực tế, chở hàng, may áo, trồng cây…), "chuyen-dong" (hai xe, đi–về, xuôi–ngược dòng…), "lam-chung" (hai vòi, hai tổ/đội).
Mọi đề MỚI, tự soạn, không ghi nguồn, KHÔNG trùng nhau và KHÔNG trùng các đề ở mục "Đề đã dùng" (khác bối cảnh hoặc khác cấu hình, không chỉ đổi số). Số đẹp: nghiệm nguyên dương (hoặc phân số gọn), nghiệm còn lại âm để học sinh loại.

## Ba kiểu bài NB (level 1) — mỗi bài 1 đề đầy đủ, hỏi 1–2 câu, tối đa 2 thẻ [NB] (y khuôn các bài mẫu ở dữ liệu):
  NB-a: đề + "Gọi … là $x$ (…), điều kiện …" → hỏi 1–2 câu biểu diễn đại lượng theo $x$ (chỗ chấm $\ldots\ldots$).
  NB-b: đề + ẩn + các biểu thức cho sẵn → "[NB] Chỉ ra câu văn … từ đó viết phương trình lập được."
  NB-c: đề + "Gọi … là $x$ (…)." + "Biết phương trình của bài toán là … với điều kiện …" → a) [NB] Giải phương trình trên. b) [NB] Đối chiếu điều kiện và trả lời câu hỏi của đề bài.
## Bài TH (level 2) — y khuôn bài TH mẫu: "[TH] <đề đầy đủ>[[br]]Kẻ bảng đại lượng rồi giải bài toán.\par\nopagebreak\smallskip\begin{center}…bảng tiêu đề cột + tên dòng, ô số liệu \hspace{2.2cm}…\end{center}", "solution" theo 3 bước (\textbf{Bước 1.} Lập phương trình … \textbf{Bước 2.} Giải phương trình … \textbf{Bước 3.} Trả lời), "hints": 2 câu hỏi gợi ý (không gọi tên công thức, không lộ số).
## Trường bắt buộc thêm cho MỌI bài NB-c và TH:
  "check": {"kind":"solveset","equation":"<PT bậc hai sau khử mẫu, cú pháp Python, ví dụ x**2 + 10*x - 3000 = 0>","answer":[n1, n2],"symbol":"x"}
  "pt_goc": "<phương trình GỐC còn mẫu, cú pháp Python, ví dụ 300/x - 300/(x+10) = 1>"
  "mach": "nang-suat" | "chuyen-dong" | "lam-chung"
Bài NB-a, NB-b cũng ghi "mach". Toán trong $…$, \dfrac, không ";" (trừ "\;"), không "Do đó/Suy ra", không xưng hô, không "khuôn". Điều kiện viết "$x$ nguyên, $x>2$" hoặc "$x>0$". Label tạm "Bài X." (giáo viên tự đánh số).
TỰ KIỂM: thế nghiệm dương vào pt_goc phải đúng.
'''

PROMPT_LOP = CHUNG + r'''
## Việc: bài thêm cho TRÊN LỚP ("tier":"onclass")
- 6 bài NB: mỗi mạch 2 bài — 1 bài NB-a và 1 bài NB-b (các mạch đã có sẵn đủ NB-c).
- 5 bài TH: nang-suat 2 bài, chuyen-dong 2 bài, lam-chung 1 bài.
## Đầu ra
{"stages":[{"kind":"them_lop","number":0,"title":"","teacher_note":"","blocks":[11 bài]}],"ghi_chu":"<bảng tự kiểm: bài → pt_goc → nghiệm>"}
'''

PROMPT_BTVN = CHUNG + r'''
## Việc: bài thêm cho BÀI TẬP VỀ NHÀ ("tier":"btvn")
- 9 bài NB: nang-suat 3 (NB-a, NB-b, NB-c), chuyen-dong 3 (NB-a, NB-b, NB-c), lam-chung 3 (NB-a, NB-b, NB-c).
- 5 bài TH: nang-suat 2, chuyen-dong 2, lam-chung 1.
## Đầu ra
{"stages":[{"kind":"them_btvn","number":0,"title":"","teacher_note":"","blocks":[14 bài]}],"ghi_chu":"<bảng tự kiểm: bài → pt_goc → nghiệm>"}
'''


def main():
    f = json.loads((REPO / SEED).read_text())
    bai = [b for s in f["stages"] for b in s["blocks"] if b.get("type") == "problem"]
    mau = {lb: next(b for b in bai if b["label"] == lb) for lb in ("Bài 1.", "Bài 2.", "Bài 3.", "Bài 10.")}
    da_dung = [b["statement"].split("[[br]]")[0][:260] for b in bai]
    vd = [b["text"].split("[[br]]")[0][:260] for s in f["stages"] for b in s["blocks"] if b.get("variant") == "example"]
    du_lieu = ("\n## Bài mẫu (NB-a = Bài 1, NB-b = Bài 2, NB-c = Bài 3, TH = Bài 10)\n" + json.dumps(mau, ensure_ascii=False)
               + "\n\n## Đề đã dùng — CẤM dùng lại\n" + json.dumps(da_dung + vd, ensure_ascii=False, indent=0) + "\n")
    for vid, pr in ((VID_LOP, PROMPT_LOP), (VID_BTVN, PROMPT_BTVN)):
        v = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": pr + du_lieu, "files": [],
             "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1800s",
             "meta": {"loai": "dung-chang-phieu", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
