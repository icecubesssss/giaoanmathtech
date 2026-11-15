# -*- coding: utf-8 -*-
"""Lượt 2 phiếu F ch.VI 9C (12/11/2026): cắt ~20′ cho vừa 135′ (buổi có KT chương 45′).

- Thêm `kiem_tra_phut: 45` (thiếu ⇒ cổng giờ tính quỹ 120′ như buổi không kiểm tra).
- Bỏ Ví dụ 1–3 (nhận khuôn, Δ hay Δ', nhẩm nghiệm): GV hỏi miệng, ghi vào teacher_note.
- Đánh số lại ví dụ 4..10 → 1..7 và mọi chỗ "như Ví dụ n".
- Bỏ ý c của Bài 1, 2, 3, 4, 6, 7, 8 (trên lớp): BTVN đã có bài cùng dạng.
Chạy trên bản sau scripts/dung_lai_phieu_f_9c.py.
"""
import json, re, sys

P = sys.argv[1]
d = json.load(open(P, encoding="utf-8"))
if d.get("kiem_tra_phut"):
    sys.exit("đã chạy rồi")

CAT_Y_C = {"Bài 1.", "Bài 2.", "Bài 3.", "Bài 4.", "Bài 6.", "Bài 7.", "Bài 8."}


def bo_y_c(s):
    """Cắt từ '[[br]]c) ' đến hết (ý c luôn là ý cuối)."""
    i = s.find("[[br]]c) ")
    return s if i < 0 else s[:i]


lt1 = d["stages"][2]
moi = []
for b in lt1["blocks"]:
    t = b.get("text", "")
    if b.get("type") == "noted" and re.match(r"\\textbf\{Ví dụ [123]\.\}", t):
        continue
    if b.get("label") in CAT_Y_C:
        b["statement"] = bo_y_c(b["statement"])
        b["solution"] = bo_y_c(b["solution"])
    moi.append(b)
lt1["blocks"] = moi
lt1["teacher_note"] = (
    r"Luyện khoảng 35 phút. Mở đầu 5 phút hỏi miệng, không ghi bảng: "
    r"(1) \emph{Giải phương trình $x^2-8x+15=0$} thuộc khuôn nào? "
    r"(2) $3x^2+6x-2=0$ dùng $\Delta$ hay $\Delta'$? "
    r"(3) Nhẩm nghiệm $2x^2-5x+3=0$. Rồi cho HS làm Bài 1, Bài 2, Bài 3. "
    r"Bài 4, Bài 5 điền đủ các bước như Ví dụ 1, Ví dụ 2 (xét $\Delta$ hoặc $ac$ trước khi dùng định lí Viète). "
    r"Bài 9 là bài về \emph{cách ăn điểm}, chữa miệng 1 phút.")


def doi_so(s):
    return re.sub(r"Ví dụ (\d+)", lambda m: f"Ví dụ {int(m.group(1)) - 3}" if int(m.group(1)) >= 4 else m.group(0), s)


def di(o):
    if isinstance(o, dict):
        return {k: di(v) for k, v in o.items()}
    if isinstance(o, list):
        return [di(v) for v in o]
    if isinstance(o, str):
        return doi_so(o)
    return o


d["stages"] = di(d["stages"])
d["stages"][2]["teacher_note"] = lt1["teacher_note"]  # giữ số 1, 2 vừa viết
d["stages"][3]["teacher_note"] = (
    r"Luyện khoảng 60 phút. Bài 14 và Bài 15 là hai khuôn Câu III.3 và Câu III.1 của đề Vào 10. "
    r"Dành 25 phút cuối cho hai bài này, chấm chéo theo thang điểm để HS thấy mỗi câu trình bày đáng $0{,}25$ điểm. "
    r"Phần còn lại của buổi (45 phút) là bài kiểm tra chương.")

out = {}
for k, v in d.items():
    out[k] = v
    if k == "btvn_phieu_rieng":
        out["kiem_tra_phut"] = 45
json.dump(out, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a", encoding="utf-8").write("\n")
print("ok")
