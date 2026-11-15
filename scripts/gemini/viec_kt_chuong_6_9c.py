#!/usr/bin/env python3
"""Sinh 2 việc Gemini: ĐỀ KIỂM TRA CHƯƠNG VI 9C (45′) — tờ đề + đáp án/barem.

Thầy (12/11/2026): "làm đề kiểm tra chương VI 9C" — Claude chốt sơ đồ (số liệu đã kiểm SymPy),
Gemini viết chữ. Ma trận do lap_kt_chuong_6_9c.py sinh máy móc từ SO_DO bên dưới.

    python3 scripts/gemini/viec_kt_chuong_6_9c.py
    python3 scripts/gemini/tho.py --mot kt-9c-ch6-de        (song song với)
    python3 scripts/gemini/tho.py --mot kt-9c-ch6-dap-an
    python3 scripts/gemini/lap_kt_chuong_6_9c.py             (ráp → seed + de-kiem-tra.json)
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
MAU = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/kiem-tra-chuong"
F = f"{D}/phieu-f-luyen-tap-chung-va-bai-tap-cuoi-chuong-vi.json"

# (câu, nội dung ma trận, mức, điểm, phút, hình thức, đáp án ngắn) — số đã kiểm SymPy 12/11/2026
SO_DO = [
    ("Câu 1", "Tính $\\Delta$ của $x^2-5x+7=0$, kết luận số nghiệm", "NB", 0.5, 2, "trắc nghiệm", "$\\Delta=-3<0$: vô nghiệm"),
    ("Câu 2", "Tổng và tích hai nghiệm của $x^2-8x+6=0$ (định lí Viète)", "NB", 0.5, 2, "trắc nghiệm", "tổng $8$, tích $6$"),
    ("Câu 3", "Nhẩm nghiệm $5x^2-8x+3=0$ nhờ $a+b+c=0$", "NB", 0.5, 2, "trắc nghiệm", "$x=1$; $x=\\dfrac35$"),
    ("Câu 4", "Điều kiện xác định của $\\dfrac{3}{x-2}+\\dfrac{x}{x+5}=1$", "NB", 0.5, 2, "trắc nghiệm", "$x\\ne 2$ và $x\\ne -5$"),
    ("Câu 5a", "Giải phương trình khuyết $b$: $3x^2-48=0$", "NB", 1.0, 3, "tự luận", "$x=4$; $x=-4$"),
    ("Câu 5b", "Giải $x^2-9x+18=0$ bằng công thức nghiệm", "NB", 1.0, 4, "tự luận", "$\\Delta=9$; $x=6$; $x=3$"),
    ("Câu 6", "Giải phương trình chứa ẩn ở mẫu $\\dfrac{1}{x}+\\dfrac{1}{x+3}=\\dfrac{1}{2}$ đủ các bước", "TH", 1.5, 8, "tự luận", "$x^2-x-6=0$; $x=3$; $x=-2$ (đều thỏa mãn)"),
    ("Câu 7", "Giải bài toán bằng cách lập phương trình (Câu III.1): ô tô đi $180$ km, lúc về tăng $5$ km/h nên về sớm $30$ phút — tìm vận tốc lúc đi", "TH", 2.5, 12, "tự luận", "$\\dfrac{180}{x}-\\dfrac{180}{x+5}=\\dfrac12$; $x^2+5x-1800=0$; $x=40$ km/h (loại $-45$)"),
    ("Câu 8a", "Chứng minh $x^2-4x-3=0$ có hai nghiệm phân biệt, viết tổng và tích hai nghiệm", "NB", 0.5, 2, "tự luận", "$ac=-3<0$; tổng $4$, tích $-3$"),
    ("Câu 8b", "Định lí Viète, hạ bậc (Câu III.3): tính $B=x_1^2+4x_2+2x_1x_2$", "VD", 1.5, 7, "tự luận", "$x_1^2=4x_1+3$ nên $B=4\\cdot4+3+2\\cdot(-3)=13$"),
]

CHUNG = r'''Bạn là thợ soạn đề kiểm tra Toán 9 (ĐẠI SỐ — chương VI: phương trình bậc hai một ẩn, định lí Viète, phương trình chứa ẩn ở mẫu, giải bài toán bằng cách lập phương trình) cho học sinh lớp 9 TẦNG C (học lực trung bình, ôn thi vào 10 Hà Nội). Đề 45 phút, thang 10 điểm. Làm CẨN THẬN, KHÔNG bịa đề: dùng ĐÚNG số liệu trong SƠ ĐỒ ĐỀ bên dưới (giáo viên đã chốt và đã kiểm đáp số bằng máy), không đổi số, không thêm bớt câu.

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt.

## SƠ ĐỒ ĐỀ (bất di bất dịch)
PHẦN I. TRẮC NGHIỆM (2,0 điểm) — mỗi câu 0,5 điểm, 4 phương án, đúng MỘT phương án:
- Câu 1. Phương trình $x^2-5x+7=0$: hỏi số nghiệm. Đáp án đúng: vô nghiệm ($\Delta=-3<0$). Phương án nhiễu: có nghiệm kép; có hai nghiệm phân biệt; có vô số nghiệm.
- Câu 2. Phương trình $x^2-8x+6=0$ có hai nghiệm $x_1$, $x_2$. Hỏi $x_1+x_2$ và $x_1x_2$. Đúng: $x_1+x_2=8$; $x_1x_2=6$. Nhiễu: ($-8$; $6$), ($8$; $-6$), ($6$; $8$).
- Câu 3. Phương trình $5x^2-8x+3=0$ có hai nghiệm là: Đúng: $x_1=1$; $x_2=\dfrac35$. Nhiễu: ($-1$; $-\dfrac35$), ($1$; $-\dfrac35$), ($-1$; $\dfrac35$).
- Câu 4. Điều kiện xác định của phương trình $\dfrac{3}{x-2}+\dfrac{x}{x+5}=1$ là: Đúng: $x\ne 2$ và $x\ne -5$. Nhiễu: $x\ne -2$ và $x\ne 5$; $x\ne 2$; $x\ne 0$, $x\ne 2$ và $x\ne -5$.
Xếp đáp án đúng ở các vị trí KHÁC NHAU (gợi ý: Câu 1 – C, Câu 2 – A, Câu 3 – D, Câu 4 – B) và ghi đúng thứ tự đó trong đáp án.

PHẦN II. TỰ LUẬN (8,0 điểm):
- Câu 5 (2,0 điểm). Giải các phương trình: a) (1,0 điểm) $3x^2-48=0$ ⇒ $x=4$; $x=-4$. b) (1,0 điểm) $x^2-9x+18=0$ ⇒ $\Delta=81-72=9>0$, $\sqrt\Delta=3$, $x_1=\dfrac{9+3}{2}=6$, $x_2=\dfrac{9-3}{2}=3$.
- Câu 6 (1,5 điểm). Giải phương trình $\dfrac{1}{x}+\dfrac{1}{x+3}=\dfrac{1}{2}$ ⇒ ĐKXĐ $x\ne0$, $x\ne-3$; mẫu chung $2x(x+3)$; khử mẫu $2(x+3)+2x=x(x+3)$ ⇒ $x^2-x-6=0$ ⇒ $\Delta=25$ ⇒ $x_1=3$, $x_2=-2$, cả hai thỏa mãn ĐKXĐ.
- Câu 7 (2,5 điểm). Đề: "Một ô tô đi từ A đến B cách nhau $180$ km. Lúc về, ô tô tăng vận tốc thêm $5$ km/h nên thời gian về ít hơn thời gian đi $30$ phút. Tính vận tốc của ô tô lúc đi." Lời giải: gọi vận tốc lúc đi là $x$ (km/h), $x>0$; thời gian đi $\dfrac{180}{x}$ (giờ), thời gian về $\dfrac{180}{x+5}$ (giờ); đổi $30$ phút $=\dfrac12$ giờ; phương trình $\dfrac{180}{x}-\dfrac{180}{x+5}=\dfrac12$; khử mẫu $360(x+5)-360x=x(x+5)$ ⇒ $x^2+5x-1800=0$; $\Delta=5^2+4\cdot1800=7225$, $\sqrt\Delta=85$; $x_1=\dfrac{-5+85}{2}=40$ (thỏa mãn), $x_2=\dfrac{-5-85}{2}=-45$ (loại); vậy vận tốc lúc đi là $40$ km/h (đổi số 15/11: bản cũ trùng Ví dụ phiếu E).
- Câu 8 (2,0 điểm). Cho phương trình $x^2-4x-3=0$. a) (0,5 điểm) Chứng minh phương trình có hai nghiệm phân biệt $x_1$, $x_2$; tính $x_1+x_2$ và $x_1x_2$. b) (1,5 điểm) Không giải phương trình, tính giá trị của biểu thức $B=x_1^2+4x_2+2x_1x_2$. Lời giải: a) $ac=1\cdot(-3)=-3<0$ ⇒ hai nghiệm phân biệt; Viète $x_1+x_2=4$, $x_1x_2=-3$. b) $x_1$ là nghiệm nên $x_1^2-4x_1-3=0$ ⇒ $x_1^2=4x_1+3$; $B=4x_1+3+4x_2+2x_1x_2=4(x_1+x_2)+2x_1x_2+3=4\cdot4+2\cdot(-3)+3=13$.

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Đề nêu MỤC TIÊU rõ, ghi ĐỦ giả thiết. Không văn nói, không xưng hô: cấm "em", "các em", "hôm nay", "Kiểm" (phải "Xét"/"Kiểm tra"), "Soi". Không viết tắt (trừ ĐKXĐ trong lời giải đã viết đủ một lần "điều kiện xác định").
2. TUYỆT ĐỐI không dùng kí hiệu $S$, $P$ cho tổng, tích hai nghiệm — viết thẳng $x_1+x_2$, $x_1x_2$. Không có tham số $m$.
3. Toán trong $…$; số thập phân viết $0{,}5$; phân số dùng \dfrac; KHÔNG dùng dấu chấm phẩy ";" để nối hai công thức trong lời giải (xuống dòng [[br]] thay vì chấm phẩy). Giữ escape \% \& \#. JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi JSON).
4. Lời giải trình bày như bài thi, MỖI BƯỚC MỘT DÒNG ([[br]]), dừng đúng chỗ, theo KHUÔN các ví dụ của phiếu luyện tập (xem "Khuôn lời giải phiếu F" cuối prompt): Viète thì dòng xét $\Delta$ hoặc $ac$ trước → "Theo định lí Viète, ta có $\begin{cases}…\end{cases}$" → biến đổi → "Vậy …". Phương trình chứa ẩn ở mẫu: điều kiện xác định → quy đồng, khử mẫu → giải → đối chiếu điều kiện từng nghiệm → "Vậy …". Bài lời văn: gọi ẩn + đơn vị + điều kiện → biểu diễn các đại lượng → lập phương trình → giải → đối chiếu điều kiện → "Vậy …".
5. TỰ TÍNH LẠI mọi đáp số; thấy sơ đồ sai thì ghi vào "ghi_chu" (KHÔNG tự đổi số).
'''

VIEC_DE = r'''
## Việc của bạn: viết TỜ ĐỀ học sinh (không in đáp án)
Khuôn JSON: y như "Mẫu tờ đề" (đề kiểm tra chương X đã duyệt) cuối prompt. 5 chặng, "title" để RỖNG "", "teacher_note" để "".
- Chặng {"kind":"review","number":1}: para "\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \\textit{Mỗi câu 0,5 điểm. Chọn phương án đúng.}" rồi 4 problem Câu 1.–Câu 4.: "type":"problem","label":"Câu 1.","level":1,"tier":"onclass","dang_id":"NB1"…"NB4","statement": câu hỏi,"options": 4 chuỗi (không ghi "A."), "answer": "A"/"B"/"C"/"D".
- Chặng {"kind":"concept","number":2}: para "\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm).}" rồi problem "Câu 5." (level 1, dang_id "NB5"), statement bắt đầu "\\textbf{(2,0 điểm)} Giải các phương trình:[[br]]a) \\textbf{(1,0 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …".
- Chặng {"kind":"practice1","number":3}: problem "Câu 6." (level 2, dang_id "TH1", "\\textbf{(1,5 điểm)} …") và problem "Câu 7." (level 2, dang_id "TH2", "\\textbf{(2,5 điểm)} …").
- Chặng {"kind":"practice2","number":4}: problem "Câu 8." (level 3, dang_id "VD1"), "\\textbf{(2,0 điểm)} Cho phương trình …[[br]]a) \\textbf{(0,5 điểm)} …[[br]]b) \\textbf{(1,5 điểm)} …".
- Chặng {"kind":"reflection","number":5}: para "\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}".
Không có "solution", không hình, không writelines, không thẻ [NB]/[TH]/[VD] trong statement.

## Đầu ra
JSON đúng schema: {"stages": [5 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC_DA = r'''
## Việc của bạn: viết ĐÁP ÁN + BAREM (tài liệu giáo viên)
Khuôn: y như các chặng 2–5 của "Mẫu đáp án" (đáp án kiểm tra chương X đã duyệt) cuối prompt — mỗi khối là "type":"para" với "text". Chặng 1 (ma trận) KHÔNG phải viết, máy tự sinh.
Mỗi bước chấm kết thúc bằng " \\hfill \\textit{(0,25đ)}" (bước 0,5 điểm thì "(0,5đ)"); TỔNG điểm các bước của mỗi ý PHẢI đúng bằng điểm của ý (Câu 5a 1,0 · 5b 1,0 · Câu 6 1,5 · Câu 7 2,5 · Câu 8a 0,5 · 8b 1,5). Mỗi dòng một bước, ngăn bằng [[br]].
Trả về đúng 4 chặng, "teacher_note" để "":
- {"kind":"concept","number":2,"title":"Đáp án Phần I và Câu 5"}: para đáp án Phần I ("\\textbf{PHẦN I (2,0 điểm).} Mỗi câu đúng $0{,}5$ điểm.[[br]]\\textbf{1 – C} (lí do ngắn bằng công thức) …" — chữ cái PHẢI khớp vị trí gợi ý trong sơ đồ), rồi para "\\textbf{Câu 5 (2,0 điểm).}[[br]]a) …".
- {"kind":"practice1","number":3,"title":"Đáp án Câu 6 và Câu 7"}: para Câu 6, para Câu 7.
- {"kind":"practice2","number":4,"title":"Đáp án Câu 8"}: para Câu 8.
- {"kind":"reflection","number":5,"title":"Biểu điểm tổng hợp"}: para tóm tắt điểm từng câu/ý (như mẫu), para "\\textbf{Tổng: 10,0 điểm.} Học sinh giải cách khác đúng vẫn cho điểm tối đa từng phần." + lỗi trừ điểm đặc thù chương này: thiếu bước xét $\Delta$ (hoặc $ac$) trước khi dùng định lí Viète trừ $0{,}25$đ; không đối chiếu điều kiện xác định / điều kiện của ẩn trừ $0{,}25$đ; thiếu câu "Vậy" trừ $0{,}25$đ mỗi bài; Câu 8b giải phương trình ra nghiệm rồi thay số đúng vẫn cho tối đa $0{,}5$đ.

## Đầu ra
JSON đúng schema: {"stages": [4 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''


def khuon_f():
    d = json.loads((REPO / F).read_text())
    out = []
    for s in d["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "noted" and b.get("variant") == "example":
                t = b["text"]
                if any(k in t for k in ("Viète", "điều kiện xác định", "km/h", "Gọi")):
                    out.append(t)
    return out[:6]


def main():
    de = json.loads((REPO / MAU / "de-kiem-tra-chuong-x.json").read_text())
    da = json.loads((REPO / MAU / "ma-tran-va-dap-an-kiem-tra-chuong-x.json").read_text())
    f = "\n\n## Khuôn lời giải phiếu F (ví dụ đã duyệt của chương VI)\n" + "\n---\n".join(khuon_f())
    for vid, phan, mau in (
        ("kt-9c-ch6-de", VIEC_DE, "\n\n## Mẫu tờ đề (chương X, chỉ để xem khuôn — KHÔNG chép nội dung)\n" + json.dumps(de["stages"], ensure_ascii=False)),
        ("kt-9c-ch6-dap-an", VIEC_DA, "\n\n## Mẫu đáp án (chương X, chỉ để xem khuôn — KHÔNG chép nội dung)\n" + json.dumps(da["stages"][1:], ensure_ascii=False) + f),
    ):
        viec = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": CHUNG + phan + mau,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1200s",
                "meta": {"loai": "de-kiem-tra", "seed_dich": f"{D}/kiem-tra-chuong/"}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt'])//1000}k ký tự)")


if __name__ == "__main__":
    main()
