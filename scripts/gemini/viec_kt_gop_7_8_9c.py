#!/usr/bin/env python3
"""Sinh 2 việc Gemini: ĐỀ KIỂM TRA GỘP CHƯƠNG VII + VIII 9C (45′) — tờ đề + đáp án/barem.

Cuối buổi 31/01/2027 (t33): phiếu 8.2 (135′) + KT gộp VII+VIII (45′).
Claude chốt sơ đồ (mọi câu lấy từ đề THẬT trong ngân hàng, số đã kiểm bằng fractions 15/11/2026),
Gemini viết chữ. Ma trận do lap_kt_gop_7_8_9c.py sinh máy móc từ SO_DO bên dưới.

    python3 scripts/gemini/viec_kt_gop_7_8_9c.py
    python3 scripts/gemini/tho.py --mot kt-9c-ch78-de
    python3 scripts/gemini/tho.py --mot kt-9c-ch78-dap-an
    python3 scripts/gemini/lap_kt_gop_7_8_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co"
MAU = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/kiem-tra-chuong"

# Nguồn (ngân hàng inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-0{7,8}.json, mã câu trong ngoặc)
NGUON = {
    "Câu 1": "Cuối kì II Phòng GD\\&ĐT Hà Đông 2024--2025, Câu I.1a (ck2-ha-dong-2024-I1)",
    "Câu 2": "Cuối kì II Phòng GD\\&ĐT Hà Đông 2024--2025, Câu I.1b (ck2-ha-dong-2024-I1)",
    "Câu 3": "Minh họa vào 10 Phòng GD\\&ĐT Đống Đa 2025--2026, Đề 09 THCS Lý Thường Kiệt, Bài I.1b (v10-ly-thuong-kiet-2025-I1)",
    "Câu 4": "Minh họa vào 10 Phòng GD\\&ĐT Đống Đa 2025--2026, Đề 05 THCS Đống Đa, Câu I.2 (v10-dong-da-2025-I2-md2)",
    "Câu 5": "Giữa kì II THCS Ngọc Lâm 2025--2026, mã đề T901, Bài I.1 (gk2-ngoc-lam-2025-I1) — ý a), c) đặt thêm trên cùng bảng số liệu",
    "Câu 6": "Học kì II THCS Ngô Gia Tự (Việt Hưng) 2025--2026, đề số 2, Bài 2",
    "Câu 7": "Minh họa vào 10 Phòng GD\\&ĐT Đống Đa 2025--2026, Đề 11 THCS Phương Mai, Bài II.2 (v10-phuong-mai-2025-II2) — thêm ý a)",
    "Câu 8": "Giữa kì II THCS Lê Hồng Phong 2025--2026, Bài 2.2 (gk2-le-hong-phong-2025-22)",
}

# (câu, nội dung ma trận, mức, điểm, phút, hình thức, đáp án ngắn) — số đã kiểm bằng fractions 15/11/2026
SO_DO = [
    ("Câu 1", "Bảng tần số (bình chọn cầu thủ): tìm cỡ mẫu", "NB", 0.5, 2, "trắc nghiệm", "$N=500$"),
    ("Câu 2", "Bảng tần số: tần số tương đối của một giá trị", "NB", 0.5, 2, "trắc nghiệm", "$\\dfrac{107}{500}\\cdot 100\\%=21{,}4\\%$"),
    ("Câu 3", "Phép thử chọn một số chính phương: số phần tử của không gian mẫu", "NB", 0.5, 2, "trắc nghiệm", "$\\Omega=\\{16;36;49\\}$, $n(\\Omega)=3$"),
    ("Câu 4", "Gieo một xúc xắc: xác suất mặt có số chấm chia hết cho $3$", "NB", 0.5, 2, "trắc nghiệm", "$\\dfrac{2}{6}=\\dfrac{1}{3}$"),
    ("Câu 5a", "Bảng tần số ghép nhóm: tần số và tần số tương đối của nhóm $[15;20)$ (Câu I.1)", "NB", 1.0, 4, "tự luận", "$12$; $30\\%$"),
    ("Câu 5b", "Lập bảng tần số tương đối ghép nhóm", "TH", 1.0, 5, "tự luận", "$17{,}5\\%$, $25\\%$, $30\\%$, $20\\%$, $7{,}5\\%$"),
    ("Câu 5c", "Gộp hai nhóm liền, kiểm tra một nhận định về tỉ lệ", "VD", 1.0, 4, "tự luận", "$\\dfrac{11}{40}=27{,}5\\%<30\\%$: đúng"),
    ("Câu 6a", "Viết không gian mẫu (viết ngẫu nhiên số có hai chữ số), đếm $n(\\Omega)$", "NB", 0.5, 2, "tự luận", "$\\Omega=\\{10;11;\\ldots;99\\}$, $n(\\Omega)=90$"),
    ("Câu 6b", "Xác suất một hành động: số chia hết cho cả $2$ và $5$ (Câu I.2)", "TH", 1.0, 4, "tự luận", "$\\dfrac{9}{90}=\\dfrac{1}{10}$"),
    ("Câu 7a", "Phép thử hai hành động (hai bạn chọn ngày): lập bảng, đếm $n(\\Omega)$", "NB", 0.5, 4, "tự luận", "$n(\\Omega)=5\\cdot 5=25$"),
    ("Câu 7b", "Xác suất biến cố \\textquotedblleft hai bạn cùng đăng ký một ngày\\textquotedblright", "TH", 1.0, 4, "tự luận", "$\\dfrac{5}{25}=\\dfrac{1}{5}$"),
    ("Câu 8a", "Xác suất một hành động: số là bội của $4$ (Câu I.2)", "TH", 1.0, 4, "tự luận", "$\\dfrac{9}{36}=\\dfrac{1}{4}$"),
    ("Câu 8b", "Biết quan hệ giữa hai xác suất, tìm số quả bóng mỗi màu", "VD", 1.0, 6, "tự luận", "$12$ bóng xanh, $24$ bóng đỏ"),
]

DUNG = {"Câu 1.": "D", "Câu 2.": "B", "Câu 3.": "A", "Câu 4.": "C"}
DIEM_Y = {"5a": 1.0, "5b": 1.0, "5c": 1.0, "6a": 0.5, "6b": 1.0, "7a": 0.5, "7b": 1.0, "8a": 1.0, "8b": 1.0}

BANG_CAU_THU = (r"\par\nopagebreak\begin{center}\footnotesize\renewcommand\arraystretch{1.25}"
                r"\begin{tabular}{|l|c|c|c|c|c|}\hline \textbf{Cầu thủ} & Quang Huy & Đức Minh & Văn Toàn & Hữu Tùng & Đức Thành \\ \hline "
                r"\textbf{Số lượt bình chọn} & $110$ & $91$ & $98$ & $94$ & $107$ \\ \hline \end{tabular}\end{center}")
BANG_HOC_VIEN = (r"\par\nopagebreak\begin{center}\footnotesize\renewcommand\arraystretch{1.25}"
                 r"\begin{tabular}{|l|c|c|c|c|c|c|}\hline \textbf{Số học viên} & $[5;10)$ & $[10;15)$ & $[15;20)$ & $[20;25)$ & $[25;30)$ & \textbf{Cộng} \\ \hline "
                 r"\textbf{Số lớp} & $7$ & $10$ & $12$ & $8$ & $3$ & $N=40$ \\ \hline \end{tabular}\end{center}")

CHUNG = r'''Bạn là thợ soạn đề kiểm tra Toán 9 (ĐẠI SỐ — kiểm tra GỘP chương VII "Tần số và tần số tương đối" và chương VIII "Xác suất của biến cố trong một số mô hình xác suất đơn giản") cho học sinh lớp 9 TẦNG C (học lực trung bình, ôn thi vào 10 Hà Nội). Đề 45 phút, thang 10 điểm. Làm CẨN THẬN, KHÔNG bịa đề: dùng ĐÚNG số liệu và lời đề trong SƠ ĐỒ ĐỀ bên dưới (giáo viên đã chốt từ đề kiểm tra thật, đã kiểm đáp số bằng máy), không đổi số, không thêm bớt câu, ý.

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt.

## SƠ ĐỒ ĐỀ (bất di bất dịch)
PHẦN I. TRẮC NGHIỆM (2,0 điểm) — mỗi câu 0,5 điểm, 4 phương án, đúng MỘT phương án. Câu 1 và Câu 2 dùng chung một bảng, đặt bảng trong MỘT khối para ngay trước Câu 1:
- Para dẫn: "Kết quả bình chọn danh hiệu \textquotedblleft Cầu thủ xuất sắc nhất\textquotedblright{} trong giải bóng đá học sinh của một trường được Ban tổ chức ghi lại trong bảng sau (mỗi người chỉ được bình chọn cho một cầu thủ). Dùng bảng này để trả lời Câu 1 và Câu 2." + bảng (chép NGUYÊN chuỗi LaTeX): <<BANG_CAU_THU>>
- Câu 1. "Số người tham gia bình chọn là:" Phương án theo đúng thứ tự A, B, C, D: $5$ ; $107$ ; $490$ ; $500$. Đúng: D ($110+91+98+94+107=500$).
- Câu 2. "Tần số tương đối của số lượt bình chọn cho cầu thủ Đức Thành là:" Phương án A–D: $10{,}7\%$ ; $21{,}4\%$ ; $20\%$ ; $107\%$. Đúng: B ($\dfrac{107}{500}\cdot 100\%=21{,}4\%$).
- Câu 3. "Chọn ngẫu nhiên một số chính phương có hai chữ số, nhỏ hơn $60$ và không chia hết cho $5$. Số phần tử của không gian mẫu là:" Phương án A–D: $3$ ; $4$ ; $5$ ; $6$. Đúng: A (các số chính phương có hai chữ số nhỏ hơn $60$ là $16$; $25$; $36$; $49$, bỏ $25$ vì chia hết cho $5$ nên $\Omega=\{16;36;49\}$, $n(\Omega)=3$).
- Câu 4. "Gieo ngẫu nhiên một con xúc xắc cân đối, đồng chất một lần. Xác suất của biến cố \textquotedblleft Mặt xuất hiện có số chấm chia hết cho $3$\textquotedblright{} là:" Phương án A–D: $\dfrac{1}{6}$ ; $\dfrac{1}{2}$ ; $\dfrac{1}{3}$ ; $\dfrac{2}{3}$. Đúng: C ($\Omega=\{1;2;3;4;5;6\}$, kết quả thuận lợi $3$; $6$, $P=\dfrac{2}{6}=\dfrac{1}{3}$).

PHẦN II. TỰ LUẬN (8,0 điểm):
- Câu 5 (3,0 điểm). Đề: "Số học viên của $40$ lớp học tại một trung tâm bồi dưỡng văn hóa được ghi lại ở bảng tần số ghép nhóm sau:" + bảng (chép NGUYÊN): <<BANG_HOC_VIEN>>
  a) (1,0 điểm) Tìm tần số và tần số tương đối của nhóm $[15;20)$. ⇒ tần số $m=12$; cỡ mẫu $N=7+10+12+8+3=40$; $f=\dfrac{12}{40}\cdot 100\%=30\%$.
  b) (1,0 điểm) Lập bảng tần số tương đối ghép nhóm của mẫu số liệu trên. ⇒ $f_1=\dfrac{7}{40}\cdot100\%=17{,}5\%$, $f_2=\dfrac{10}{40}\cdot100\%=25\%$, $f_3=30\%$, $f_4=\dfrac{8}{40}\cdot100\%=20\%$, $f_5=\dfrac{3}{40}\cdot100\%=7{,}5\%$ (tổng $100\%$); lời giải phải có BẢNG hai dòng (Số học viên | các nhóm; Tần số tương đối | các %).
  c) (1,0 điểm) "Có ý kiến cho rằng: \textquotedblleft Số lớp có từ $20$ học viên trở lên chiếm chưa đến $30\%$ tổng số lớp\textquotedblright. Ý kiến đó đúng hay sai? Vì sao?" ⇒ các lớp có từ $20$ học viên trở lên thuộc hai nhóm $[20;25)$ và $[25;30)$, có $8+3=11$ lớp; tỉ lệ $\dfrac{11}{40}\cdot100\%=27{,}5\%$ (hoặc $20\%+7{,}5\%=27{,}5\%$); $27{,}5\%<30\%$ nên ý kiến đó ĐÚNG.
- Câu 6 (1,5 điểm). Đề: "Viết ngẫu nhiên một số tự nhiên có hai chữ số."
  a) (0,5 điểm) Viết tập hợp $\Omega$ gồm các kết quả có thể xảy ra đối với số tự nhiên được viết ra và cho biết $\Omega$ có bao nhiêu phần tử. ⇒ $\Omega=\{10;11;12;\ldots;99\}$, $n(\Omega)=99-10+1=90$.
  b) (1,0 điểm) Tính xác suất của biến cố $A$: \textquotedblleft Số tự nhiên được viết ra chia hết cho cả $2$ và $5$\textquotedblright. ⇒ số chia hết cho cả $2$ và $5$ là số có chữ số tận cùng bằng $0$: $10$; $20$; $30$; $40$; $50$; $60$; $70$; $80$; $90$, $n(A)=9$; $P(A)=\dfrac{9}{90}=\dfrac{1}{10}$.
- Câu 7 (1,5 điểm). Đề: "Mỗi học sinh được đăng ký một ngày trong tuần (từ Thứ Hai đến Thứ Sáu) để tự học ở thư viện. Hai bạn Bách và Chi mỗi bạn đăng ký ngẫu nhiên một ngày."
  a) (0,5 điểm) Lập bảng mô tả không gian mẫu của phép thử và cho biết không gian mẫu có bao nhiêu phần tử. ⇒ kí hiệu Thứ Hai, Thứ Ba, Thứ Tư, Thứ Năm, Thứ Sáu lần lượt là $2$, $3$, $4$, $5$, $6$; mỗi kết quả là cặp $(a;b)$, $a$ là ngày Bách chọn, $b$ là ngày Chi chọn; bảng $5$ dòng, $5$ cột (lời giải VẼ bảng tabular 6 cột: ô góc "Bách $\backslash$ Chi", hàng/cột tiêu đề $2;3;4;5;6$, mỗi ô ghi cặp $(a;b)$); $n(\Omega)=5\cdot5=25$.
  b) (1,0 điểm) Tính xác suất của biến cố $B$: \textquotedblleft Hai bạn cùng đăng ký một ngày\textquotedblright. ⇒ kết quả thuận lợi $(2;2)$, $(3;3)$, $(4;4)$, $(5;5)$, $(6;6)$ (đường chéo bảng), $n(B)=5$; $P(B)=\dfrac{5}{25}=\dfrac{1}{5}$.
- Câu 8 (2,0 điểm). Đề: "Một hộp có $36$ quả bóng có kích thước và khối lượng như nhau, mỗi quả bóng được ghi một trong các số $1$; $2$; $3$; $\ldots$; $35$; $36$; hai quả bóng khác nhau thì ghi hai số khác nhau. Xét phép thử \textquotedblleft Lấy ngẫu nhiên một quả bóng trong hộp\textquotedblright."
  a) (1,0 điểm) Tính xác suất của biến cố $C$: \textquotedblleft Số ghi trên quả bóng được lấy ra là bội của $4$\textquotedblright. ⇒ $n(\Omega)=36$; bội của $4$: $4$; $8$; $12$; $16$; $20$; $24$; $28$; $32$; $36$, $n(C)=9$; $P(C)=\dfrac{9}{36}=\dfrac{1}{4}$.
  b) (1,0 điểm) "Mỗi quả bóng trong hộp chỉ có một màu là đỏ hoặc xanh. Biết rằng xác suất của biến cố \textquotedblleft Lấy được quả bóng màu đỏ\textquotedblright{} gấp $2$ lần xác suất của biến cố \textquotedblleft Lấy được quả bóng màu xanh\textquotedblright. Hỏi trong hộp có bao nhiêu quả bóng đỏ, bao nhiêu quả bóng xanh?" ⇒ gọi số bóng xanh là $x$ (quả), $x$ nguyên dương, $x<36$; số bóng đỏ là $36-x$; $P(\text{xanh})=\dfrac{x}{36}$, $P(\text{đỏ})=\dfrac{36-x}{36}$; theo đề $\dfrac{36-x}{36}=2\cdot\dfrac{x}{36}$ ⇒ $36-x=2x$ ⇒ $x=12$ (thỏa mãn); vậy có $12$ quả bóng xanh và $36-12=24$ quả bóng đỏ.

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Đề nêu MỤC TIÊU rõ, ghi ĐỦ giả thiết. Không văn nói, không xưng hô: cấm "em", "các em", "Theo em", "hôm nay", "Kiểm" (phải "Xét"/"Kiểm tra"), "Soi". Không viết tắt.
2. Toán trong $…$ (mọi con số, kể cả số trong câu chữ: "$40$ lớp", "$36$ quả bóng"); số thập phân viết $17{,}5$; phân số dùng \dfrac; phần trăm viết \% (trong chuỗi JSON là \\%). KHÔNG dùng dấu chấm phẩy ";" để nối hai công thức trong lời giải (xuống dòng [[br]] thay vì chấm phẩy); liệt kê dãy số thì MỖI SỐ MỘT cặp $…$ ngăn bằng "; " (vd "$4$; $8$; $12$") để xuống dòng được. Chữ Đ trong công thức viết \text{Đ}. Không dùng \times — dùng \cdot. Không dùng \smallskip. JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi JSON).
3. Lời giải trình bày như bài thi, MỖI BƯỚC MỘT DÒNG ([[br]]), dừng đúng chỗ. Khuôn xác suất ba dòng: "Không gian mẫu $\Omega=\{…\}$, do đó $n(\Omega)=…$." → "Các kết quả thuận lợi cho biến cố $A$ là …, do đó $n(A)=…$." → "$P(A)=\dfrac{n(A)}{n(\Omega)}=…$. Vậy $P(A)=…$." Khuôn tần số tương đối: tần số $m=…$, cỡ mẫu $N=…$, $f=\dfrac{m}{N}\cdot100\%=…$. Kiểm tra nhận định: tính tỉ lệ → so sánh → "Vậy ý kiến đó đúng/sai."
4. TỰ TÍNH LẠI mọi đáp số; thấy sơ đồ sai thì ghi vào "ghi_chu" (KHÔNG tự đổi số).
'''.replace("<<BANG_CAU_THU>>", BANG_CAU_THU).replace("<<BANG_HOC_VIEN>>", BANG_HOC_VIEN)

VIEC_DE = r'''
## Việc của bạn: viết TỜ ĐỀ học sinh (không in đáp án)
Khuôn JSON: y như "Mẫu tờ đề" (đề kiểm tra chương VI lớp 9C đã duyệt) cuối prompt. 5 chặng, "title" để RỖNG "", "teacher_note" để "".
- Chặng {"kind":"review","number":1}: para "\\textbf{PHẦN I. TRẮC NGHIỆM (2,0 điểm).} \\textit{Mỗi câu 0,5 điểm. Chọn phương án đúng.}", rồi para dẫn + bảng cầu thủ, rồi 4 problem Câu 1.–Câu 4.: "type":"problem","label":"Câu 1.","level":1,"tier":"onclass","dang_id":"NB1"…"NB4","statement": câu hỏi,"options": 4 chuỗi ĐÚNG thứ tự trong sơ đồ (không ghi "A."), "answer": chữ cái đúng.
- Chặng {"kind":"concept","number":2}: para "\\textbf{PHẦN II. TỰ LUẬN (8,0 điểm).}" rồi problem "Câu 5." (level 2, dang_id "TH1"), statement bắt đầu "\\textbf{(3,0 điểm)} Số học viên …" + bảng + "a) \\textbf{(1,0 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …[[br]]c) \\textbf{(1,0 điểm)} …" (sau \end{center} viết thẳng "a)", không [[br]] thừa).
- Chặng {"kind":"practice1","number":3}: problem "Câu 6." (level 1, dang_id "NB5", "\\textbf{(1,5 điểm)} …[[br]]a) \\textbf{(0,5 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …") và problem "Câu 7." (level 2, dang_id "TH2", "\\textbf{(1,5 điểm)} …[[br]]a) \\textbf{(0,5 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …").
- Chặng {"kind":"practice2","number":4}: problem "Câu 8." (level 3, dang_id "VD1"), "\\textbf{(2,0 điểm)} Một hộp có …[[br]]a) \\textbf{(1,0 điểm)} …[[br]]b) \\textbf{(1,0 điểm)} …".
- Chặng {"kind":"reflection","number":5}: para "\\begin{center}\\textit{$-$ HẾT $-$}\\end{center}".
Không có "solution", không hình, không writelines, không thẻ [NB]/[TH]/[VD] trong statement, không ghi nguồn đề trong tờ đề.

## Đầu ra
JSON đúng schema: {"stages": [5 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC_DA = r'''
## Việc của bạn: viết ĐÁP ÁN + BAREM (tài liệu giáo viên)
Khuôn: y như các chặng 2–5 của "Mẫu đáp án" (đáp án kiểm tra chương VI lớp 9C đã duyệt) cuối prompt — mỗi khối là "type":"para" với "text". Chặng 1 (ma trận) KHÔNG phải viết, máy tự sinh.
Mỗi bước chấm kết thúc bằng " \\hfill \\textit{(0,25đ)}" (bước 0,5 điểm thì "(0,5đ)"); TỔNG điểm các bước của mỗi ý PHẢI đúng bằng điểm của ý (5a 1,0 · 5b 1,0 · 5c 1,0 · 6a 0,5 · 6b 1,0 · 7a 0,5 · 7b 1,0 · 8a 1,0 · 8b 1,0). Mỗi dòng một bước, ngăn bằng [[br]]. Mỗi ý bắt đầu bằng "[[br]]a) ", "[[br]]b) ", "[[br]]c) " (chữ cái thường, ngay sau [[br]]).
Bảng trong lời giải (Câu 5b, Câu 7a) viết bằng \\begin{center}\\footnotesize\\renewcommand\\arraystretch{1.2}\\begin{tabular}…\\end{tabular}\\end{center}, đặt điểm "(…đ)" ở dòng chữ ngay sau bảng.
Trả về đúng 4 chặng, "teacher_note" để "":
- {"kind":"concept","number":2,"title":"Đáp án Phần I và Câu 5"}: para đáp án Phần I ("\\textbf{PHẦN I (2,0 điểm).} Mỗi câu đúng $0{,}5$ điểm.[[br]]\\textbf{1 – D} (lí do ngắn bằng phép tính) …" — chữ cái PHẢI là 1 – D, 2 – B, 3 – A, 4 – C, mỗi câu một dòng), rồi para "\\textbf{Câu 5 (3,0 điểm).}[[br]]a) …".
- {"kind":"practice1","number":3,"title":"Đáp án Câu 6 và Câu 7"}: para Câu 6 ("\\textbf{Câu 6 (1,5 điểm).}[[br]]a) …"), para Câu 7 ("\\textbf{Câu 7 (1,5 điểm).}[[br]]a) …").
- {"kind":"practice2","number":4,"title":"Đáp án Câu 8"}: para Câu 8 ("\\textbf{Câu 8 (2,0 điểm).}[[br]]a) …").
- {"kind":"reflection","number":5,"title":"Biểu điểm tổng hợp"}: para tóm tắt điểm từng câu/ý (như mẫu), para "\\textbf{Tổng: 10,0 điểm.} Học sinh giải cách khác đúng vẫn cho điểm tối đa từng phần." + lỗi trừ điểm đặc thù: tần số tương đối không ghi \\% hoặc tổng bảng không bằng $100\\%$ trừ $0{,}25$đ; phân số xác suất không rút gọn trừ $0{,}25$đ; không viết không gian mẫu hoặc không nêu $n(\\Omega)$ trước khi tính xác suất trừ $0{,}25$đ; thiếu câu "Vậy" trừ $0{,}25$đ mỗi bài; Câu 8b không đối chiếu điều kiện của ẩn trừ $0{,}25$đ; Câu 7a liệt kê đủ $25$ cặp thay cho bảng vẫn cho đủ điểm.

## Đầu ra
JSON đúng schema: {"stages": [4 chặng], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''


def main():
    de = json.loads((REPO / MAU / "de-kiem-tra-chuong-vi.json").read_text())
    da = json.loads((REPO / MAU / "ma-tran-va-dap-an-kiem-tra-chuong-vi.json").read_text())
    for vid, phan, mau in (
        ("kt-9c-ch78-de", VIEC_DE, "\n\n## Mẫu tờ đề (chương VI 9C, chỉ để xem khuôn JSON — KHÔNG chép nội dung)\n" + json.dumps(de["stages"], ensure_ascii=False)),
        ("kt-9c-ch78-dap-an", VIEC_DA, "\n\n## Mẫu đáp án (chương VI 9C, chỉ để xem khuôn JSON — KHÔNG chép nội dung)\n" + json.dumps(da["stages"][1:], ensure_ascii=False)),
    ):
        viec = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": CHUNG + phan + mau,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1200s",
                "meta": {"loai": "de-kiem-tra", "seed_dich": f"{D}/kiem-tra-chuong/"}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt'])//1000}k ký tự)")


if __name__ == "__main__":
    main()
