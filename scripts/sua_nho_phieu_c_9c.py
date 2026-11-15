"""Phiếu C (Viète) ch.VI 9C — phiên nhỏ 13/11/2026 theo luật "lý thuyết chỉ là lý thuyết".

Bỏ hộp trap ("mất 0,25 điểm") + hộp target ("Câu III.3 … buổi hôm nay"), viết lại mục 1
đúng chữ SGK Toán 9 tập hai tr.21, bỏ văn nói "kiểm"/"phải thuộc", bỏ nhánh sơ đồ
"Biết tổng S, tích P" (dạng đã cắt), bỏ kí hiệu S, P ở quy trình Bài 16, bỏ "mất điểm"
ở gợi ý Bài 17, sửa ghi chú GV cho khớp bài hiện có. Idempotent.

    python3 scripts/sua_nho_phieu_c_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

SEED = Path("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
            "phieu-c-dinh-li-viete-va-ung-dung.json")


def stage(d, kind):
    return next(s for s in d["stages"] if s["kind"] == kind)


def bai(d, label):
    for s in d["stages"]:
        for b in s["blocks"]:
            if b.get("label") == label:
                return b
    raise KeyError(label)


def main():
    d = json.loads(SEED.read_text(encoding="utf-8"))

    # 1. Chặng Kiến thức: bỏ trap/target, viết lại mục 1, 2.
    c = stage(d, "concept")
    c["blocks"] = [b for b in c["blocks"] if b.get("variant") not in ("trap", "target")]
    paras = [b for b in c["blocks"] if b["type"] == "para"]
    paras[1]["text"] = (
        "Nếu $x_1$, $x_2$ là hai nghiệm của phương trình $ax^2+bx+c=0$ ($a \\ne 0$) thì"
        "[[br]]\\hspace*{1.4em}$\\begin{cases} x_1+x_2=-\\dfrac{b}{a}\\\\ "
        "x_1x_2=\\dfrac{c}{a}\\end{cases}$"
        "[[br]]Định lí chỉ áp dụng khi phương trình có nghiệm, tức là $\\Delta \\ge 0$ "
        "(hoặc $\\Delta' \\ge 0$). Nếu $ac<0$ thì phương trình luôn có hai nghiệm phân biệt."
    )
    paras[2]["text"] = "\\textbf{2. Biểu diễn một số biểu thức theo $x_1+x_2$ và $x_1x_2$}"
    paras[3]["text"] = paras[3]["text"].replace(
        "\\;(phải kiểm $x_1x_2 \\ne 0$ trước)", "\\;(với $x_1x_2 \\ne 0$)")
    c["teacher_note"] = (
        "Các công thức ở mục 2 cho HS chép vào mặt sau vở. Các ví dụ mẫu được đưa xuống "
        "trực tiếp từng phần Luyện tập để GV giảng mẫu đến đâu HS thực hành ngay đến đó.")

    # 2. Opener: "buổi nay" -> "buổi này".
    for b in stage(d, "review")["blocks"]:
        if "text" in b:
            b["text"] = b["text"].replace("dùng suốt buổi nay", "dùng trong buổi này")

    # 3. Luyện tập: ghi chú GV + quy trình Bài 16 + gợi ý Bài 17 + câu kết Ví dụ 8.
    p1 = stage(d, "practice1")
    for b in p1["blocks"]:
        if "text" in b:
            b["text"] = b["text"].replace(
                "Vậy phương trình đã cho vô nghiệm — đây là lí do luôn phải kiểm $\\Delta$ trước.",
                "Vậy phương trình đã cho vô nghiệm nên không áp dụng được định lí Viète.")
    p1["teacher_note"] = (
        "Luyện 48 phút. Mỗi bài NB đi đủ các bước như ví dụ đứng ngay trước: điều kiện "
        "có nghiệm ($\\Delta$ hoặc $ac$), hệ thức Viète, biến đổi, kết luận. "
        "Bài 2c là phương trình vô nghiệm, chữa kĩ.")
    p2 = stage(d, "practice2")
    p2["teacher_note"] = (
        "Luyện 48 phút. Bài 13 có ý phụ \\emph{chứng minh hai nghiệm khác 0} — "
        "đề THCS Cầu Giấy yêu cầu trình bày rõ bước này. "
        "Bài 17 là bài khó nhất buổi, chữa chậm ở bước xét dấu.")
    bai(d, "Bài 16.")["quy_trinh"] = [
        "Kiểm tra điều kiện để phương trình có hai nghiệm ($\\Delta \\ge 0$ hoặc $ac<0$).",
        "Áp dụng định lí Viète: $x_1+x_2=-\\dfrac{b}{a}$ và $x_1x_2=\\dfrac{c}{a}$.",
        "Biến đổi biểu thức cần tính theo $x_1+x_2$ và $x_1x_2$.",
        "Thay giá trị vào biểu thức để tính và kết luận.",
    ]
    bai(d, "Bài 17.")["hints"] = [
        "Xét dấu hai nghiệm trước rồi mới bỏ dấu giá trị tuyệt đối."]

    # 4. Tổng kết: sơ đồ + ghi chú GV.
    r = stage(d, "reflection")
    mm = next(b for b in r["blocks"] if b["type"] == "mindmap")
    for br in mm["branches"]:
        if br["label"] == "Kiểm trước khi dùng":
            br["label"] = "Điều kiện có nghiệm"
        if br["label"] == "Bốn công thức":
            br["label"] = "Biểu thức của hai nghiệm"
        if br["label"] == "Dạng ngược":
            br["label"] = "Biết một nghiệm $x_1$"
            br["children"] = [{"label": "$x_2=[[blank:1.4cm]]-x_1$"}]
    r["teacher_note"] = (
        "Sơ đồ tư duy điền 5 phút cuối buổi — phần biểu thức của hai nghiệm phải điền kín. "
        "BTVN 17 bài $\\approx$ 96 phút; buổi sau chữa Bài 18 và Bài 34 trước.")

    out = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    if "--ghi" in sys.argv:
        SEED.write_text(out, encoding="utf-8")
        print("đã ghi", SEED)
    else:
        print("chạy thử OK (thêm --ghi để ghi)")


if __name__ == "__main__":
    main()
