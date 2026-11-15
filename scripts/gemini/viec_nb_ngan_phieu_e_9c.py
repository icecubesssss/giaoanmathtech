#!/usr/bin/env python3
"""Việc Gemini: bài NB phiếu E ch.VI 9C = MỖI ĐỀ HỎI 1–2 CÂU (Thầy chốt 12/11/2026).

Thầy: "NB nó kp như thế? Kiểu có 1 đề xong HS nó phân tích đơn giản để trả lời 1-2 câu thôi … bạn gộp hết thế?"
Gemini dựng lại chặng practice1 (giữ nguyên tiêu đề mạch + 3 ví dụ) và 2 bài NB của BTVN.

    python3 scripts/gemini/viec_nb_ngan_phieu_e_9c.py
    python3 scripts/gemini/tho.py --mot nb-ngan-9c-ch6-phieu-e
    python3 scripts/gemini/lap_nb_ngan_phieu_e_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json"
VID = "nb-ngan-9c-ch6-phieu-e"

PROMPT = r'''Bạn là thợ soạn phiếu Toán 9 (Bài 21 "Giải bài toán bằng cách lập phương trình", học sinh lớp 9 TẦNG C). TUYỆT ĐỐI KHÔNG chạy lệnh, KHÔNG dùng công cụ — tự tính nhẩm. Dữ liệu ở cuối prompt.

## Giáo viên chốt
Bài Nhận biết (NB) KHÔNG phải một khung bài giải dài. NB = MỘT ĐỀ ĐẦY ĐỦ, học sinh chỉ phân tích đơn giản để trả lời 1–2 câu. Các bài NB trong một mạch nối tiếp theo bước giải:
  NB-a: đề đầy đủ, ĐÃ cho sẵn ẩn ("Gọi … là $x$ (…)") → hỏi 1–2 câu BIỂU DIỄN đại lượng theo $x$ (điền chỗ chấm).
  NB-b: đề đầy đủ khác, cho sẵn ẩn và các biểu thức → hỏi 1 câu: câu nào cho quan hệ và viết phương trình.
  NB-c: đề đầy đủ khác, cho sẵn phương trình và điều kiện của ẩn → a) giải phương trình, b) đối chiếu điều kiện và trả lời câu hỏi của đề.
Mỗi bài NB có đề RIÊNG (không trùng ví dụ, không trùng nhau, không trùng các đề dưới mục "Đề đã dùng — CẤM dùng lại"). Đề tự soạn, số đẹp, nghiệm nguyên dương đẹp (hoặc phân số gọn), không ghi nguồn.

## Việc 1 — chặng "practice1" (title "Luyện tập 1 — Nhận biết", number 3)
Giữ NGUYÊN VĂN 3 khối tiêu đề mạch và 3 khối ví dụ ở dữ liệu. Thứ tự:
  heading Mạch 1 → Ví dụ 1 → Bài 1 (NB-a) → Bài 2 (NB-b) → Bài 3 (NB-c)   [năng suất: kế hoạch/thực tế, chở hàng]
  heading Mạch 2 → Ví dụ 2 → Bài 4 (NB-a) → Bài 5 (NB-b) → Bài 6 (NB-c)   [chuyển động]
  heading Mạch 3 → Ví dụ 3 → Bài 7 (NB-a) → Bài 8 (NB-b) → Bài 9 (NB-c)   [làm chung, vòi nước]
teacher_note: khoảng 60 phút. Mỗi mạch giáo viên làm ví dụ cùng lớp, rồi học sinh làm 3 bài NB ngắn (biểu diễn → lập phương trình → giải và trả lời), chữa nhanh từng bài.
## Việc 2 — "btvn_nb": 2 bài NB cho bài tập về nhà (tier "btvn"): một bài NB-b dạng năng suất, một bài NB-c dạng hình chữ nhật (diện tích). Đề khác hết các đề trên.

## Khuôn khối bài
{"type":"problem","label":"Bài N.","level":1,"tier":"onclass" (hoặc "btvn"),"statement":…,"solution":…,"check":…}
- statement: "<đề đầy đủ>[[br]]<câu dẫn cho sẵn ẩn nếu có>[[br]]a) [NB] <câu hỏi> $\ldots\ldots$[[br]]b) [NB] <câu hỏi> $\ldots\ldots$". Bài chỉ 1 câu thì không có "a)", thẻ "[NB]" đứng đầu câu hỏi. Tối đa 2 thẻ [NB] mỗi bài.
- solution: đáp án ngắn từng ý; NB-c viết lời giải: khử mẫu → $…=0$ → $\Delta$ → hai nghiệm → loại → "Vậy …".
- check (CHỈ bài NB-c): {"kind":"solveset","equation":"<phương trình bậc hai sau khử mẫu, cú pháp Python, ví dụ x**2 + 10*x - 3000 = 0>","answer":[nghiệm1, nghiệm2],"symbol":"x"}. Bài khác KHÔNG có "check".
- Toán trong $…$, phân số \dfrac, không ";" (trừ "\;"), không "Do đó/Suy ra", không xưng hô, không "khuôn". Điều kiện viết "$x$ nguyên, $x>2$" hoặc "$x>0$".
- TỰ KIỂM: thế nghiệm vào phương trình gốc (có mẫu) cho đúng; ghi vào "ghi_chu" bảng đề → phương trình → nghiệm của 3 bài NB-c và bài BTVN NB-c.

## Đầu ra
{"stages":[{"kind":"practice1","number":3,"title":…,"teacher_note":…,"blocks":[…]},{"kind":"btvn_nb","number":0,"title":"","teacher_note":"","blocks":[2 bài]}],"ghi_chu":…}
'''


def main():
    f = json.loads((REPO / SEED).read_text())
    st = {s["kind"]: s for s in f["stages"]}
    giu = [b for b in st["practice1"]["blocks"]
           if (b.get("type") == "para" and b.get("variant") == "heading") or b.get("variant") == "example"]
    da_dung = [b["statement"].split("[[br]]")[0][:300] for s in f["stages"] for b in s["blocks"]
               if b.get("type") == "problem"]
    v = {"id": VID, "model": "gemini-3.8-flash-high",
         "prompt": PROMPT + "\n## Dữ liệu — tiêu đề mạch và ví dụ (giữ nguyên)\n" + json.dumps(giu, ensure_ascii=False)
         + "\n\n## Đề đã dùng — CẤM dùng lại\n" + json.dumps(da_dung, ensure_ascii=False, indent=0) + "\n",
         "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1800s",
         "meta": {"loai": "dung-chang-phieu", "seed": SEED}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
