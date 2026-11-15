#!/usr/bin/env python3
"""Việc Gemini: đưa phiếu E ch.VI 9C về MỘT bộ xương "bảng phân tích → Bước 1 → Bước 2 → Bước 3" (Thầy chốt 12/11/2026).

Thầy: "Phiếu vẫn lộn xộn quá? Bạn định dạy như thế này á???" — chẩn đoán: một nội dung lặp 3 lần (phân tích văn xuôi →
lời giải → bảng + khung a–g), bài NB băm 7 câu, không thấy ranh giới lập / giải / trả lời. Thầy chọn khuôn "Bảng → 3 bước".

    python3 scripts/gemini/viec_khuon_3_buoc_phieu_e_9c.py
    python3 scripts/gemini/tho.py --mot khuon-3-buoc-9c-ch6-phieu-e
    python3 scripts/gemini/ap_sua_phieu.py khuon-3-buoc-9c-ch6-phieu-e [--ghi]
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json"
VID = "khuon-3-buoc-9c-ch6-phieu-e"
LABELS = ["Ví dụ 1.", "Ví dụ 2.", "Ví dụ 3."] + [f"Bài {i}." for i in range(1, 16)]

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (Bài 21 "Giải bài toán bằng cách lập phương trình", học sinh lớp 9 TẦNG C). KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu ở cuối prompt (18 khối: Ví dụ 1–3, Bài 1–15). Đề, số liệu, đáp số GIỮ NGUYÊN (đã kiểm bằng máy) — chỉ đổi CÁCH TRÌNH BÀY.

## Vì sao sửa
Giáo viên chê phiếu "lộn xộn": một nội dung bị viết 3 lần (phân tích văn xuôi → lời giải chép lại → bảng + khung a)–g) hỏi lại đúng các ô của bảng), bài nhận biết bị băm thành 7 câu a)–g), học sinh không nhìn ra 3 bước SGK. Giáo viên chốt MỘT bộ xương dùng cho MỌI bài trong phiếu:
  Phân tích = MỘT bảng đại lượng + MỘT dòng "Quan hệ" → Bước 1. Lập phương trình → Bước 2. Giải phương trình → Bước 3. Trả lời.
Ví dụ: ít ô trống (giáo viên giảng). Bài NB: nhiều chỗ chấm (học sinh điền). Bài TH, VD: đề + bảng trống (giữ nguyên đề), lời giải đáp án viết theo cùng bộ xương.

## Luật
- KHÔNG có chữ "a)", "b)"… trong khung bài NB và trong lời giải (trừ khi đề gốc có nhiều câu hỏi). KHÔNG đoạn "Phân tích" văn xuôi kiểu "Đề hỏi gì? … Chọn ẩn: …" — bỏ hẳn.
- Bảng phân tích là NHÁP: dòng "Quan hệ" chỉ ghi câu trích đề và hiệu/tổng đại lượng bằng LỜI, KHÔNG viết sẵn phương trình (phương trình chỉ xuất hiện MỘT lần, ở Bước 1).
- Bước 1 trình bày như đi thi: gọi ẩn + đơn vị + điều kiện, biểu diễn các đại lượng (một dòng gọn, chép từ bảng), "Theo đề bài, ta có phương trình …". Bước 2: quy đồng mẫu hai vế rồi khử mẫu (hoặc khai triển) → $…=0$ → $\Delta$ hoặc $\Delta'$ và căn → $x_1$, $x_2$. Bước 3: đối chiếu từng nghiệm với điều kiện, "Vậy …" trả lời ĐỦ điều đề hỏi, có đơn vị.
- Không ";" (trừ "\;"), không "Do đó/Suy ra/suy ra/Như vậy", không xưng hô, không "khuôn", không "$\Delta'>0$ nên". Điều kiện viết "$x$ nguyên, $x>8$" hoặc "$x>0$" (KHÔNG dùng $\mathbb{N}^*$).
- Toán trong $…$, ô [[fill:…]] trong $…$ thì đáp án không bọc $. JSON hợp lệ.

## Khuôn VÍ DỤ (trường "statement" = toàn bộ text thẻ, "solution" = "")
\textbf{Ví dụ N.} <đề giữ nguyên>[[br]]{\sffamily\bfseries\color{brand}Phân tích}\par\nopagebreak\smallskip\begin{center}\footnotesize\renewcommand\arraystretch{1.5}\begin{tabular}{|l|c|c|c|}\hline & \textbf{…} & \textbf{…} & \textbf{…} \\ \hline <dòng 1> & $…$ & $…$ & $…$ \\ \hline <dòng 2> & $…$ & $…$ & $…$ \\ \hline \end{tabular}\end{center}\smallskip Quan hệ: \textquotedblleft <trích câu đề>\textquotedblright{} nên <đại lượng A> $-$ <đại lượng B> $=$ <số> (bằng lời).[[br]]{\sffamily\bfseries\color{brand}Lời giải}[[br]]\textbf{Bước 1.} Gọi … là $x$ (…), điều kiện ….[[br]]\hspace*{1.4em}<biểu diễn, một dòng>[[br]]\hspace*{1.4em}Theo đề bài, ta có phương trình $…$.[[br]]\textbf{Bước 2.} Quy đồng mẫu hai vế rồi khử mẫu, ta được $…$, tức là $…=0$.[[br]]\hspace*{1.4em}Ta có $\Delta'=[[fill:…]]$, $\sqrt{\Delta'}=…$.[[br]]\hspace*{1.4em}Phương trình có hai nghiệm $x_1=[[fill:…]]$, $x_2=[[fill:…]]$.[[br]]\textbf{Bước 3.} $x_1=…$ thoả mãn điều kiện, $x_2=…$ không thoả mãn điều kiện nên loại.[[br]]\hspace*{1.4em}Vậy [[fill:<câu trả lời có $…$ nếu có công thức>]].
Bảng ví dụ in ĐỦ mọi ô (không chấm). Ví dụ 3 (làm chung) bảng 2 cột số liệu "Thời gian làm riêng (giờ) | Làm được trong 1 giờ (công việc)", dòng Đội thứ nhất / Đội thứ hai / Cả hai đội — dùng {|l|c|c|}.

## Khuôn BÀI NB (Bài 1, 2, 3, 9, 10) — "statement":
<đề giữ nguyên kể cả nguồn>[[br]]Điền vào chỗ chấm để hoàn thành bài giải.[[br]]\textit{Phân tích:}\par\nopagebreak\smallskip\begin{center}…bảng cùng khuôn: dòng đầu in sẵn 1–2 ô mồi (như bản cũ), các ô còn lại "$\ldots\ldots$"…\end{center}\smallskip Quan hệ: \textquotedblleft <trích câu đề>\textquotedblright{} nên \ldots\ldots\ldots\ldots[[br]]\textbf{Bước 1.} [NB] Gọi … là $x$ (…), điều kiện $\ldots\ldots$[[br]]\hspace*{1.4em}[NB] <biểu diễn có chỗ chấm $\ldots\ldots$>[[br]]\hspace*{1.4em}[NB] Theo đề bài, ta có phương trình $\ldots\ldots$[[br]]\textbf{Bước 2.} [NB] Quy đồng mẫu hai vế rồi khử mẫu, ta được $\ldots\ldots=0$ (Bài 10 không có mẫu: "Khai triển và chuyển vế, ta được $\ldots\ldots=0$")[[br]]\hspace*{1.4em}[NB] $\Delta'=\ldots\ldots$, $\sqrt{\Delta'}=\ldots$, $x_1=\ldots$, $x_2=\ldots$[[br]]\textbf{Bước 3.} [NB] $x_1=\ldots$ (\ldots\ldots), $x_2=\ldots$ (\ldots\ldots)[[br]]\hspace*{1.4em}Vậy \ldots\ldots\ldots\ldots
(Chữ "hoàn thành bài giải" phải có. Đúng 6 thẻ [NB].) "solution": lời giải đầy đủ theo đúng bộ xương Bước 1/2/3 (không bảng).
## BÀI TH, VD (Bài 4–8, 11–15): "statement" TRẢ NGUYÊN VĂN như dữ liệu. "solution" viết lại theo bộ xương \textbf{Bước 1.} / \textbf{Bước 2.} / \textbf{Bước 3.} (không bảng, không a/b), cùng số liệu và đáp số bản cũ. Bài 11 là phương trình bậc nhất: Bước 2 khử mẫu rồi tìm $s$.

## Đầu ra
{"sua":[mỗi khối trong dữ liệu một phần tử {"label","statement","solution"}],"ghi_chu"}. Tự tính lại mọi số; nghi ngờ ghi "ghi_chu".
'''


NHOM = {"khuon-3-buoc-9c-ch6-phieu-e-a": ["Ví dụ 1.", "Ví dụ 2.", "Ví dụ 3.", "Bài 1.", "Bài 2.", "Bài 3.", "Bài 9.", "Bài 10."],
        "khuon-3-buoc-9c-ch6-phieu-e-b": ["Bài 4.", "Bài 5.", "Bài 6.", "Bài 7.", "Bài 8.", "Bài 11.", "Bài 12.", "Bài 13.",
                                          "Bài 14.", "Bài 15."]}
CAM_LENH = ("\n## TUYỆT ĐỐI KHÔNG chạy lệnh, KHÔNG dùng công cụ (bị chặn ⇒ việc hỏng). Tự tính nhẩm — đáp số đã có sẵn "
            "trong dữ liệu. Chỉ sửa các khối có trong dữ liệu dưới đây; đầu ra \"sua\" đúng bằng số khối đó.\n")


def main():
    seed = json.loads((REPO / SEED).read_text())
    ds = []
    for s in seed["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                ds.append({"label": b["label"], "statement": b["statement"], "solution": b.get("solution", "")})
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m:
                    ds.append({"label": m.group(1), "statement": b["text"], "solution": ""})
    assert sorted(x["label"] for x in ds) == sorted(LABELS), [x["label"] for x in ds]
    for vid, lb in NHOM.items():
        con = [x for x in ds if x["label"] in lb]
        v = {"id": vid, "model": "gemini-3.8-flash-high",
             "prompt": PROMPT.replace("18 khối: Ví dụ 1–3, Bài 1–15", f"{len(con)} khối") + CAM_LENH
             + "\n## Dữ liệu (JSON)\n" + json.dumps(con, ensure_ascii=False, indent=1) + "\n",
             "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1800s",
             "meta": {"loai": "sua-phieu", "seed": SEED, "labels": lb}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")
    return
    v = {"id": VID, "model": "gemini-3.8-flash-high",
         "prompt": PROMPT + "\n## Dữ liệu (18 khối, JSON)\n" + json.dumps(ds, ensure_ascii=False, indent=1) + "\n",
         "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1800s",
         "meta": {"loai": "sua-phieu", "seed": SEED, "labels": LABELS}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
