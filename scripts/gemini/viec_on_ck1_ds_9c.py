#!/usr/bin/env python3
"""Sinh 3 việc Gemini: PHIẾU ÔN TẬP CUỐI KÌ I — ĐẠI SỐ, lớp 9C (tầng C), CN 22/11/2026 (tuần 23), 180′.

Tiến độ Thầy: "Rà dạng ĐS (đủ dạng mỗi buổi): tính toán với căn (20′) · PT chứa căn đơn giản (20′)
· rút gọn + câu hỏi phụ (70′) · toán lời văn lập hệ, lập PT, BPT (70′)". BTVN 6 bài đủ dạng.

Claude chốt sơ đồ (đề đã soi PDF gốc, đáp số kiểm SymPy 15/11/2026), Gemini viết chữ:
    python3 scripts/gemini/viec_on_ck1_ds_9c.py
    python3 scripts/gemini/tho.py --tien-to on-ck1-9c-ds --song-song 3
    (Claude ráp 3 kết quả → seed, soát, validate, build)
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/on-tap-cuoi-ki-1/phieu-a-on-tap-cuoi-ki-1-dai-so.json"
D6 = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
MODEL = "gemini-4-hydrogen-medium"

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 cho học sinh lớp 9 TẦNG C (học lực trung bình–yếu, ôn thi cuối học kì I, Hà Nội, sách Kết nối tri thức). Phiếu: "Ôn tập cuối học kì I — Đại số", buổi 180 phút, học sinh làm vào VỞ (phiếu không chừa chỗ trống, không dòng kẻ).
Phạm vi kiến thức CHỈ học kì I: chương I (phương trình, hệ hai phương trình bậc nhất hai ẩn, giải bài toán bằng cách lập hệ), chương II (phương trình quy về bậc nhất, bất đẳng thức, bất phương trình bậc nhất một ẩn), chương III (căn bậc hai, căn thức, biến đổi, rút gọn). CẤM dùng phương trình bậc hai, công thức nghiệm, $\Delta$, định lí Viète (chưa học).

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt này.
KHÔNG bịa đề: dùng ĐÚNG đề, ĐÚNG số liệu trong SƠ ĐỒ (giáo viên đã soi đề gốc và kiểm đáp số bằng máy). Không đổi số, không thêm bớt bài, không đổi thứ tự. Thấy sơ đồ sai thì ghi vào "ghi_chu", KHÔNG tự sửa số.

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Văn toán, không văn nói, không xưng hô: cấm "em", "các em", "hôm nay", "Kiểm" (dùng "Xét"/"Kiểm tra"), "Soi", "nhé", "nào", chữ IN HOA để nhấn, "khuôn", "mẹo", "bẫy", "mất điểm", "thang điểm", "cấu trúc đề". Không viết tắt (ĐKXĐ chỉ dùng sau khi đã viết đủ "điều kiện xác định" một lần trong cùng bài).
2. Đề nêu dữ kiện trước, yêu cầu sau, giống đề thi. Nguồn đề ghi cuối đề bằng " \textit{(…)}" đúng như sơ đồ.
3. Lời giải như bài thi: MỖI phép biến đổi MỘT dòng, ngăn bằng [[br]]; dòng con thụt vào bằng "\hspace*{1.4em}". KHÔNG dùng dấu $\Leftrightarrow$ (học sinh đi thi không dùng, chỉ xuống dòng). Một dòng tối đa một dấu $\Rightarrow$. Không nối hai công thức bằng dấu chấm phẩy. Kết thúc mỗi bài/ý bằng một dòng "Vậy …".
4. Bài giải bằng cách lập hệ/lập phương trình/lập bất phương trình đi đủ 3 bước của SGK: Bước 1 lập (gọi ẩn, ĐƠN VỊ, ĐIỀU KIỆN; biểu diễn các đại lượng chưa biết qua ẩn; lập hệ/phương trình/bất phương trình), Bước 2 giải (giải đến nghiệm, từng dòng), Bước 3 đối chiếu điều kiện rồi trả lời "Vậy …" có đơn vị. Đổi phút ra giờ bằng phân số ($45$ phút $=\dfrac{3}{4}$ giờ). Phần trăm viết $20\%$ trong toán thì là $20\%$ với dấu \% (escape \%).
5. Bài rút gọn: dòng đầu "Với $x\ge0$, $x\ne4$, ta có" (đúng điều kiện của đề) → quy đồng (viết mẫu chung dạng tích) → thu gọn tử → phân tích tử → rút gọn → "Vậy …". Tính giá trị tại $x=x_0$: "Thay $x=16$ (thỏa mãn điều kiện) vào $A$, ta được" → tính → "Vậy …". Câu phụ bất phương trình: chuyển vế về dạng $\dfrac{\ldots}{\ldots}<0$, nêu dấu của mẫu (vì $\sqrt{x}+2>0$), suy ra tử, KẾT HỢP điều kiện ban đầu rồi mới kết luận.
6. Phương trình chứa căn: nêu điều kiện xác định → biến đổi (đưa thừa số ra ngoài dấu căn, thu gọn) → bình phương khi hai vế không âm → đối chiếu điều kiện → "Vậy …". Với $\sqrt{A^2}=B$: dùng $\sqrt{A^2}=|A|$ rồi xét hai trường hợp.
7. Toán trong $…$; số thập phân $0{,}5$; nghìn: $44\,500\,000$; phân số dùng \dfrac. Giữ escape \% \& \#. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi trong JSON). KHÔNG dùng kí tự toán Unicode (√, ≤, ≥, ≠, ⇒, …) ngoài $…$ — luôn viết lệnh LaTeX trong $…$.
8. TỰ TÍNH LẠI mọi đáp số trước khi trả; ghi nghi ngờ vào "ghi_chu".

## Kí hiệu ô trống (bắt buộc đúng cú pháp)
- Trong VÍ DỤ (khối "noted", variant "example"): ô trống có đáp án = [[fill:đáp án]]. Mỗi ví dụ ≥ 3 ô, khoét ở MẮT XÍCH THEN CHỐT (chỗ áp dụng công thức, chỗ lập phương trình, chỗ đối chiếu điều kiện), không khoét con số cuối cho có. Ô nằm trong $…$ thì đáp án KHÔNG bọc $ (vd "$\sqrt{48}=[[fill:4\sqrt{3}]]$"); ô nằm ngoài $…$ thì đáp án là chữ thường hoặc tự bọc $ (vd "[[fill:thỏa mãn]]"). Đáp án không chứa ký tự "]" hay "|".
- Trong BÀI điền khuyết (khối "problem"): ô trống = [[blank:1.6cm]] (ô ngắn, một số/biểu thức gọn) hoặc [[blank:4cm]] (ô dài). Không ghi đáp án vào ô; đáp án đầy đủ viết ở "solution". Mật độ ≥ 6 ô / 10 dòng khung. Đáp án của một ô KHÔNG được lộ ở dòng ngay dưới.
'''

KHUON_CHUNG = r'''
## Khuôn JSON từng loại khối
- Tiêu đề dạng (chỉ trong Luyện tập 1): {"type":"para","variant":"heading","text":"Dạng 1. Tính giá trị biểu thức chứa căn bậc hai"}
- Ví dụ: {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} <đề> \\textit{(nguồn)}[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]<từng dòng lời giải có [[fill:…]]>[[br]]Vậy …"}
  Ví dụ bài lời văn thêm phần phân tích TRƯỚC "Lời giải": "{\\sffamily\\bfseries\\color{brand}Phân tích}[[br]]" + các câu hỏi dẫn ngắn (Đề hỏi gì? Chọn ẩn là gì? Đại lượng nào biểu diễn qua ẩn? Câu nào cho quan hệ để lập phương trình?) + BẢNG ĐẠI LƯỢNG LaTeX: "\\par\\nopagebreak\\smallskip\\begin{center}\\footnotesize\\renewcommand\\arraystretch{1.5}\\begin{tabular}{|l|c|c|c|}\\hline … \\\\ \\hline \\end{tabular}\\end{center}\\smallskip".
- Bài: {"type":"problem","label":"Bài 1.","statement":"…","tier":"onclass","level":1,"dang_id":"D11","solution":"…","hints":[]}
  ("tier":"btvn" cho bài tập về nhà; "level" 1 = nhận biết, 2 = thông hiểu, 3 = vận dụng — ghi theo sơ đồ; "hints" luôn [] vì đây là phiếu ôn tập cuối kì, học sinh làm như đi thi.)
- Thẻ mức đặt ở đầu TỪNG ý: "a) [NB] …", "2) [TH] …", "3) [VD] …"; bài một ý thì đặt ngay đầu statement: "[TH] Giải phương trình …". Trong khung điền khuyết của bài lời văn, mỗi bước gắn một thẻ: "[NB] \\textbf{Bước 1.} …".
- "solution": lời giải ĐẦY ĐỦ như bài thi (bài điền khuyết thì là khung đã điền đủ), từng dòng [[br]].
'''

SO_DO_A = r'''
## Việc của bạn (việc A): chặng 1 "Khám phá", chặng 2 "Kiến thức cần nhớ", và sơ đồ tư duy của chặng 5 "Tổng kết"
Trả về đúng 3 chặng:
1) {"kind":"review","number":1,"title":"Khám phá","teacher_note":…,"blocks":[1 khối opener]}
   Khối opener: {"type":"opener","text":"…"} — 2–3 câu ngắn, giọng trung tính (không xưng hô): buổi ôn tập rà lại bốn dạng bài đại số của học kì I: tính giá trị biểu thức chứa căn, giải phương trình chứa căn, rút gọn biểu thức chứa căn và câu hỏi phụ, giải bài toán bằng cách lập hệ phương trình, lập phương trình, lập bất phương trình. KHÔNG nói về cấu trúc đề thi, điểm số. Kèm "tikz": sơ đồ 4 ô nối mũi tên dùng style có sẵn flownode/flowkey/flowarrow, ví dụ:
   "\\begin{tikzpicture}[node distance=4mm and 5mm, font=\\small]\n \\node[flownode](a){Tính giá trị\\\\biểu thức\\\\chứa căn};\n \\node[flownode,right=of a](b){Phương trình\\\\chứa căn};\n \\node[flownode,right=of b](c){Rút gọn\\\\và câu hỏi phụ};\n \\node[flowkey,right=of c](d){Bài toán\\\\lời văn};\n \\draw[flowarrow](a)--(b);\n \\draw[flowarrow](b)--(c);\n \\draw[flowarrow](c)--(d);\n\\end{tikzpicture}"
   teacher_note: 5 phút, giới thiệu 4 dạng; nhắc học sinh mở vở.
2) {"kind":"concept","number":2,"title":"Kiến thức cần nhớ","teacher_note":…,"blocks":[…]}
   CHỈ là lý thuyết SGK Toán 9 Kết nối tri thức (định nghĩa, công thức, các bước giải đúng chữ SGK), tổng hợp lý thuyết đại số học kì I. Mỗi mục = 2 khối para: {"type":"para","text":"\\textbf{N. Tên mục}"} rồi {"type":"para","text":"nội dung, gạch đầu dòng $\\bullet$\\; …, mỗi ý một dòng [[br]]"}. Đúng 8 mục theo thứ tự:
   1. Căn bậc hai, căn thức bậc hai: căn bậc hai số học của $a\ge0$ là $\sqrt{a}$; $\sqrt{A}$ xác định khi $A\ge0$; $\sqrt{A^2}=|A|$ (tức là $\sqrt{A^2}=A$ nếu $A\ge0$, $\sqrt{A^2}=-A$ nếu $A<0$).
   2. Khai phương một tích, một thương: $\sqrt{AB}=\sqrt{A}\cdot\sqrt{B}$ ($A\ge0$, $B\ge0$); $\sqrt{\dfrac{A}{B}}=\dfrac{\sqrt{A}}{\sqrt{B}}$ ($A\ge0$, $B>0$).
   3. Đưa thừa số ra ngoài, vào trong dấu căn: $\sqrt{A^2B}=|A|\sqrt{B}$ ($B\ge0$); với $A\ge0$, $B\ge0$ thì $A\sqrt{B}=\sqrt{A^2B}$; với $A<0$, $B\ge0$ thì $A\sqrt{B}=-\sqrt{A^2B}$.
   4. Trục căn thức ở mẫu: $\dfrac{A}{\sqrt{B}}=\dfrac{A\sqrt{B}}{B}$ ($B>0$); $\dfrac{C}{\sqrt{A}+\sqrt{B}}=\dfrac{C(\sqrt{A}-\sqrt{B})}{A-B}$, $\dfrac{C}{\sqrt{A}-\sqrt{B}}=\dfrac{C(\sqrt{A}+\sqrt{B})}{A-B}$ ($A\ge0$, $B\ge0$, $A\ne B$); tương tự với $\dfrac{C}{\sqrt{A}\pm B}$.
   5. Rút gọn biểu thức chứa căn: tìm điều kiện xác định; phân tích mẫu thành nhân tử (chú ý $x-4=(\sqrt{x}-2)(\sqrt{x}+2)$ với $x\ge0$, $x+2\sqrt{x}=\sqrt{x}(\sqrt{x}+2)$); quy đồng, thu gọn tử, rút gọn nhân tử chung.
   6. Giải hệ hai phương trình bậc nhất hai ẩn: phương pháp thế (từ một phương trình biểu diễn một ẩn theo ẩn kia, thế vào phương trình còn lại, giải phương trình một ẩn, suy ra ẩn còn lại) và phương pháp cộng đại số (nhân hai vế mỗi phương trình với số thích hợp để hệ số của một ẩn bằng nhau hoặc đối nhau, cộng hoặc trừ từng vế…).
   7. Giải bài toán bằng cách lập hệ phương trình (hoặc lập phương trình): Bước 1. Lập hệ phương trình: chọn ẩn và đặt điều kiện thích hợp cho ẩn; biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết; lập hệ phương trình biểu thị mối quan hệ giữa các đại lượng. Bước 2. Giải hệ phương trình. Bước 3. Kiểm tra xem trong các nghiệm của hệ, nghiệm nào thỏa mãn điều kiện của ẩn rồi trả lời bài toán.
   8. Bất phương trình bậc nhất một ẩn: dạng $ax+b<0$ (hoặc $>$, $\le$, $\ge$), $a\ne0$; chuyển vế đổi dấu; nhân (chia) hai vế với số dương thì giữ chiều, với số âm thì ĐỔI chiều bất phương trình (viết "đổi chiều", không viết hoa).
   KHÔNG thêm mục "bẫy", "lưu ý thi", "cấu trúc đề", không thêm ví dụ trong chặng này.
   teacher_note: 10 phút, học sinh đọc lại; giáo viên hỏi nhanh 3–4 công thức (nêu cụ thể).
3) {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":…,"blocks":[1 khối mindmap]}
   Khối mindmap: {"type":"mindmap","root":"Đại số học kì I","caption":"Điền các ô trống để tự tổng kết bốn dạng bài","branches":[4 nhánh, mỗi nhánh {"label":…,"children":[3 {"label":…}]}]}. 4 nhánh: "Tính giá trị biểu thức chứa căn", "Phương trình chứa căn", "Rút gọn và câu hỏi phụ", "Bài toán lời văn". Mỗi lá có một ô [[blank:1.2cm]] (hoặc 1.6cm) điền đúng thứ đã dạy ở chặng 2 (ví dụ "$\\sqrt{A^2}=[[blank:1.2cm]]$", "Bước 1: tìm [[blank:1.6cm]]", "Chọn ẩn, đơn vị, [[blank:1.4cm]]").
   teacher_note: 5 phút tổng kết; nhắc Phiếu bài tập về nhà 6 bài (Bài 15–20) in riêng, đủ bốn dạng, làm trước buổi luyện đề ôn tập số 1.

## Đầu ra
JSON đúng schema: {"stages":[3 chặng như trên], "ghi_chu":"…"}.
'''

SO_DO_B = r'''
## Việc của bạn (việc B): chặng 3 "Luyện tập 1 — Nhận biết" (toàn bộ là ví dụ điền khuyết + bài điền khuyết khung bài giải)
Trả về đúng 1 chặng: {"kind":"practice1","number":3,"title":"Luyện tập 1 — Nhận biết","teacher_note":…,"blocks":[…]}
teacher_note dạng dàn ý điều phối, xuống dòng [[br]], khoảng 60 phút: Dạng 1 (8′), Dạng 2 (8′), Dạng 3 (22′), Dạng 4 (22′); mỗi dạng: DẠNG \& MỨC / KHI HỌC SINH BÍ (1–2 câu hỏi gợi mở) — ngắn.

Mỗi bài điền khuyết: statement = đề nguyên văn (dữ kiện + yêu cầu, có thẻ mức ở từng ý) → nguồn → dòng "[[br]](Điền vào chỗ chấm để hoàn thành bài giải, làm đủ các bước như Ví dụ N.)" → khung bài giải in sẵn, mỗi bước một dòng, ô [[blank:…]] ở mắt xích then chốt. Cụm "hoàn thành bài giải" là BẮT BUỘC (máy đếm giờ nhận theo cụm này). Khung đi CÙNG NHỊP với ví dụ đứng trước.

THỨ TỰ KHỐI (bất di bất dịch):

[heading] "Dạng 1. Tính giá trị biểu thức chứa căn bậc hai"
[Ví dụ 1] Đề: Tính $\sqrt{12}-10\sqrt{\dfrac{3}{25}}+\sqrt{75}$. Nguồn: \textit{(Đề cuối kì I, THCS Ngọc Lâm, 2025--2026)}. Đáp số $5\sqrt{3}$ ($\sqrt{12}=2\sqrt{3}$; $10\sqrt{\dfrac{3}{25}}=10\cdot\dfrac{\sqrt{3}}{5}=2\sqrt{3}$; $\sqrt{75}=5\sqrt{3}$).
[Bài 1.] level 1, dang_id "D11". Đề: "Tính giá trị của các biểu thức sau:[[br]]a) [NB] $A=2\sqrt{48}+4\sqrt{27}+\sqrt{75}+2\sqrt{3}$ \textit{(Đề học kì I, THCS Marie Curie, 2024--2025)}[[br]]b) [NB] $B=\sqrt{(1-\sqrt{3})^2}-\sqrt{(1+\sqrt{3})^2}$ \textit{(Đề cuối kì I, Phòng GD\&ĐT Quốc Oai, 2024--2025)}" rồi dòng điền khuyết (như Ví dụ 1) và khung cho cả a) và b). Đáp số: a) $8\sqrt{3}+12\sqrt{3}+5\sqrt{3}+2\sqrt{3}=27\sqrt{3}$. b) $|1-\sqrt{3}|-|1+\sqrt{3}|=(\sqrt{3}-1)-(1+\sqrt{3})=-2$ (vì $1<\sqrt{3}$ nên $1-\sqrt{3}<0$). Khung b) phải có ô cho dấu so sánh hoặc lý do "$1-\sqrt{3}\;[[blank:1cm]]\;0$".

[heading] "Dạng 2. Giải phương trình chứa căn"
[Ví dụ 2] Đề: Giải phương trình $\sqrt{4x+8}-\sqrt{x+2}+\dfrac{3}{2}\sqrt{16x+32}=14$. Nguồn: \textit{(Đề cuối kì I, THCS Giang Biên, 2025--2026)}. Lời giải: điều kiện xác định $x\ge-2$; $\sqrt{4x+8}=2\sqrt{x+2}$, $\dfrac{3}{2}\sqrt{16x+32}=\dfrac{3}{2}\cdot4\sqrt{x+2}=6\sqrt{x+2}$; $2\sqrt{x+2}-\sqrt{x+2}+6\sqrt{x+2}=14$; $7\sqrt{x+2}=14$; $\sqrt{x+2}=2$; $x+2=4$; $x=2$ (thỏa mãn). Vậy $x=2$.
[Bài 2.] level 1, dang_id "D13". Đề: "Giải các phương trình sau:[[br]]a) [NB] $\sqrt{x-3}=2$ \textit{(Đề học kì I, THCS Marie Curie, 2024--2025)}[[br]]b) [NB] $\sqrt{x^2+4x+4}=3$ \textit{(Đề học kì I, THCS Ngô Sĩ Liên, 2024--2025)}" + dòng điền khuyết (như Ví dụ 2) + khung. Đáp số: a) điều kiện $x\ge3$; $x-3=4$; $x=7$ (thỏa mãn). b) $\sqrt{(x+2)^2}=3$; $|x+2|=3$; $x+2=3$ hoặc $x+2=-3$; $x=1$ hoặc $x=-5$. Vậy $x\in\{1;-5\}$.

[heading] "Dạng 3. Rút gọn biểu thức chứa căn và câu hỏi phụ"
[Ví dụ 3] Đề: "Cho hai biểu thức $A=\dfrac{\sqrt{x}+4}{\sqrt{x}}$ và $B=\dfrac{2}{\sqrt{x}+2}+\dfrac{x+4}{x-4}$ với $x>0$, $x\ne4$.[[br]]1) Tính giá trị của biểu thức $A$ khi $x=9$.[[br]]2) Chứng minh $B=\dfrac{\sqrt{x}}{\sqrt{x}-2}$.[[br]]3) Đặt $P=A\cdot B$. Tìm các giá trị của $x$ để $P=3$." Nguồn: \textit{(Đề học kì I, THCS Nhật Tân, 2024--2025)}. Lời giải: 1) $x=9$ thỏa mãn, $\sqrt{9}=3$, $A=\dfrac{3+4}{3}=\dfrac{7}{3}$. 2) mẫu chung $(\sqrt{x}-2)(\sqrt{x}+2)$; $B=\dfrac{2(\sqrt{x}-2)+x+4}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{x+2\sqrt{x}}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{\sqrt{x}(\sqrt{x}+2)}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{\sqrt{x}}{\sqrt{x}-2}$. 3) $P=\dfrac{\sqrt{x}+4}{\sqrt{x}}\cdot\dfrac{\sqrt{x}}{\sqrt{x}-2}=\dfrac{\sqrt{x}+4}{\sqrt{x}-2}$; $P=3$ khi $\sqrt{x}+4=3(\sqrt{x}-2)$; $\sqrt{x}+4=3\sqrt{x}-6$; $2\sqrt{x}=10$; $\sqrt{x}=5$; $x=25$ (thỏa mãn). Vậy $x=25$.
[Bài 3.] level 1, dang_id "D15". Đề: "Cho hai biểu thức $A=\dfrac{2\sqrt{x}-1}{\sqrt{x}+1}$ và $B=\dfrac{2\sqrt{x}+5}{\sqrt{x}+1}-\dfrac{\sqrt{x}}{\sqrt{x}-1}+\dfrac{6}{x-1}$ với $x\ge0$, $x\ne1$.[[br]]1) [NB] Tìm giá trị của $A$ tại $x=4$.[[br]]2) [NB] Chứng minh $B=\dfrac{\sqrt{x}+1}{\sqrt{x}-1}$.[[br]]3) [NB] Đặt $P=A\cdot B$. Tìm tất cả các giá trị của $x$ thỏa mãn $P=\dfrac{9}{4}$." Nguồn: \textit{(Đề học kì I, THCS Nguyễn Trường Tộ, 2025--2026)}. + dòng điền khuyết (như Ví dụ 3) + khung 3 ý. Đáp số: 1) $A=\dfrac{2\cdot2-1}{2+1}=1$. 2) $B=\dfrac{(2\sqrt{x}+5)(\sqrt{x}-1)-\sqrt{x}(\sqrt{x}+1)+6}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{2x+3\sqrt{x}-5-x-\sqrt{x}+6}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{x+2\sqrt{x}+1}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{(\sqrt{x}+1)^2}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{\sqrt{x}+1}{\sqrt{x}-1}$. 3) $P=\dfrac{2\sqrt{x}-1}{\sqrt{x}-1}=\dfrac{9}{4}$; $4(2\sqrt{x}-1)=9(\sqrt{x}-1)$; $8\sqrt{x}-4=9\sqrt{x}-9$; $\sqrt{x}=5$; $x=25$ (thỏa mãn).
[Bài 4.] level 1, dang_id "D16". Đề: "Cho hai biểu thức $A=\dfrac{\sqrt{x}+2}{\sqrt{x}-3}$ và $B=\dfrac{\sqrt{x}}{\sqrt{x}+2}+\dfrac{4\sqrt{x}+4}{x+2\sqrt{x}}$ với $x>0$, $x\ne9$.[[br]]1) [NB] Tính giá trị của biểu thức $A$ với $x=25$.[[br]]2) [NB] Chứng minh $B=\dfrac{\sqrt{x}+2}{\sqrt{x}}$.[[br]]3) [NB] Cho $P=A:B$. Tìm số nguyên $x$ nhỏ nhất để $2P>1$." Nguồn: \textit{(Đề học kì I, Phòng Văn hóa -- Xã hội phường Ba Đình, 2025--2026)}. + dòng "(Điền vào chỗ chấm để hoàn thành bài giải, ý 1 và ý 2 làm như Ví dụ 3.)" + khung 3 ý (ý 3 khung đầy đủ các bước vì chưa có ví dụ: tính $P$, chuyển vế, xét dấu mẫu, kết hợp điều kiện). Đáp số: 1) $A=\dfrac{5+2}{5-3}=\dfrac{7}{2}$. 2) $x+2\sqrt{x}=\sqrt{x}(\sqrt{x}+2)$; $B=\dfrac{x+4\sqrt{x}+4}{\sqrt{x}(\sqrt{x}+2)}=\dfrac{(\sqrt{x}+2)^2}{\sqrt{x}(\sqrt{x}+2)}=\dfrac{\sqrt{x}+2}{\sqrt{x}}$. 3) $P=\dfrac{\sqrt{x}+2}{\sqrt{x}-3}\cdot\dfrac{\sqrt{x}}{\sqrt{x}+2}=\dfrac{\sqrt{x}}{\sqrt{x}-3}$; $2P>1$ khi $\dfrac{2\sqrt{x}}{\sqrt{x}-3}-1>0$; $\dfrac{\sqrt{x}+3}{\sqrt{x}-3}>0$; vì $\sqrt{x}+3>0$ nên $\sqrt{x}-3>0$; $\sqrt{x}>3$; $x>9$; kết hợp điều kiện, số nguyên $x$ nhỏ nhất là $x=10$.

[heading] "Dạng 4. Giải bài toán bằng cách lập hệ phương trình, lập phương trình"
[Ví dụ 4] (có Phân tích + bảng) Đề: "Một nhà hàng buffet có giá vé cho người lớn và giá vé cho trẻ em theo bảng giá quy định. Gia đình ông Hải gồm hai người lớn và bốn trẻ em thanh toán hết $1\,400\,000$ đồng, gia đình chị Hương gồm ba người lớn và hai trẻ em thanh toán hết $1\,300\,000$ đồng. Hỏi giá vé buffet của mỗi người lớn và mỗi trẻ em là bao nhiêu?" Nguồn: \textit{(Đề cuối kì I, THCS và THPT M.V. Lômônôxốp, 2024--2025)}. Lời giải: gọi giá vé người lớn $x$ (nghìn đồng), trẻ em $y$ (nghìn đồng), $x>0$, $y>0$; hệ $\begin{cases}2x+4y=1400\\3x+2y=1300\end{cases}$; giải bằng cộng đại số (nhân phương trình thứ hai với 2 rồi trừ): $4x-2x=2600-1400$... ra $x=300$, $y=200$ (thỏa mãn). Vậy người lớn $300\,000$ đồng, trẻ em $200\,000$ đồng.
[Bài 5.] level 1, dang_id "D04". Đề: "Tại một buổi biểu diễn nhằm gây quỹ từ thiện, ban tổ chức đã bán được $500$ vé. Trong đó có hai loại vé: vé loại I giá $100\,000$ đồng; vé loại II giá $75\,000$ đồng. Tổng số tiền thu được từ bán vé là $44\,500\,000$ đồng. Tính số vé bán ra của mỗi loại." Nguồn: \textit{(Đề cuối kì I, THCS Hoàng Liệt, 2025--2026)}. + dòng điền khuyết (như Ví dụ 4) + BẢNG ĐẠI LƯỢNG có ô [[blank:…]] (cột: Số vé, Giá một vé (nghìn đồng), Số tiền (nghìn đồng); hàng: Loại I, Loại II, Tổng) + khung 3 bước, mỗi bước một thẻ: "[NB] \textbf{Bước 1.} …", "[NB] \textbf{Bước 2.} …", "[NB] \textbf{Bước 3.} …". Đáp số: $\begin{cases}x+y=500\\100x+75y=44\,500\end{cases}$; $x=280$, $y=220$. Vậy $280$ vé loại I, $220$ vé loại II.
[Ví dụ 5] (có Phân tích + bảng: Quãng đường, Vận tốc, Thời gian × Lúc đi, Lúc về) Đề: "Một xe máy đi từ A đến B với vận tốc $45$ km/h, lúc đi từ B về A người đó đi với vận tốc nhanh hơn vận tốc ban đầu là $5$ km/h nên thời gian về ít hơn thời gian đi là $12$ phút. Tính quãng đường AB." Nguồn: \textit{(Đề cuối kì I, THCS Lý Sơn, 2025--2026)}. Lời giải: gọi quãng đường AB là $x$ (km), $x>0$; vận tốc về $50$ km/h; thời gian đi $\dfrac{x}{45}$ (giờ), về $\dfrac{x}{50}$ (giờ); $12$ phút $=\dfrac{1}{5}$ giờ; phương trình $\dfrac{x}{45}-\dfrac{x}{50}=\dfrac{1}{5}$; nhân hai vế với $450$: $10x-9x=90$; $x=90$ (thỏa mãn). Vậy quãng đường AB dài $90$ km.
[Bài 6.] level 1, dang_id "D04". Đề: "Một người đi xe đạp từ A đến B với tốc độ trung bình $15$ km/h. Lúc về người đó chỉ đi với tốc độ $12$ km/h, nên thời gian về nhiều hơn thời gian đi là $45$ phút. Tính quãng đường AB." Nguồn: \textit{(Đề cuối kì I, THCS Phúc Đồng, 2025--2026)}. + dòng điền khuyết (như Ví dụ 5) + bảng có ô trống + khung 3 bước gắn thẻ [NB] từng bước. Đáp số: $\dfrac{x}{12}-\dfrac{x}{15}=\dfrac{3}{4}$; nhân hai vế với $60$: $5x-4x=45$; $x=45$ (thỏa mãn). Vậy AB dài $45$ km.

Tổng thẻ [NB] của chặng phải đúng 16: Bài 1 (2), Bài 2 (2), Bài 3 (3), Bài 4 (3), Bài 5 (3), Bài 6 (3). Ví dụ KHÔNG gắn thẻ.

## Đầu ra
JSON đúng schema: {"stages":[1 chặng], "ghi_chu":"…"}.
'''

SO_DO_C = r'''
## Việc của bạn (việc C): chặng 4 "Luyện tập 2 — Thông hiểu \& Vận dụng" và 6 bài tập về nhà
Học sinh TỰ TRÌNH BÀY vào vở (không khung, không ô trống, không gợi ý). Mọi bài có "solution" đầy đủ như bài thi.
Trả về đúng 2 chặng:
(1) {"kind":"practice2","number":4,"title":"Luyện tập 2 — Thông hiểu \\& Vận dụng","teacher_note":…,"blocks":[…]} — teacher_note dàn ý điều phối [[br]], khoảng 60 phút: thông hiểu Bài 7–12 (36′), vận dụng Bài 13–14 (24′); DẠNG \& MỨC / KHI HỌC SINH BÍ (câu hỏi gợi mở từng nấc, không gọi tên công cụ) / chữa chấm chéo.
(2) {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[6 bài tier "btvn"]} — KHÔNG thêm para tiêu đề (máy tự in tiêu đề phiếu bài tập về nhà).

THỨ TỰ KHỐI chặng 4 (bất di bất dịch; không có heading):
[Bài 7.] level 2, dang_id "D12". "[TH] Tính giá trị biểu thức $\dfrac{2}{\sqrt{3}-1}-\sqrt{(\sqrt{3}-1)^2}$." \textit{(Đề học kì I, Cụm chuyên môn số 14 Hà Nội, 2025--2026)}. Đáp: $\dfrac{2(\sqrt{3}+1)}{(\sqrt{3}-1)(\sqrt{3}+1)}=\dfrac{2(\sqrt{3}+1)}{2}=\sqrt{3}+1$; $\sqrt{(\sqrt{3}-1)^2}=|\sqrt{3}-1|=\sqrt{3}-1$ (vì $\sqrt{3}>1$); kết quả $2$.
[Bài 8.] level 2, dang_id "D13". "[TH] Giải phương trình $\sqrt{4x+4}-2\sqrt{9x+9}=\sqrt{x+1}-15$." \textit{(Đề cuối kì I, THCS Cầu Diễn, 2025--2026)}. Đáp: điều kiện $x\ge-1$; $2\sqrt{x+1}-6\sqrt{x+1}-\sqrt{x+1}=-15$; $-5\sqrt{x+1}=-15$; $\sqrt{x+1}=3$; $x+1=9$; $x=8$ (thỏa mãn).
[Bài 9.] level 2, dang_id "D15". "Cho biểu thức $A=\dfrac{\sqrt{x}+1}{\sqrt{x}-2}+\dfrac{2\sqrt{x}}{\sqrt{x}+2}+\dfrac{2+5\sqrt{x}}{4-x}$ với $x\ge0$, $x\ne4$.[[br]]a) [TH] Rút gọn biểu thức $A$.[[br]]b) [TH] Tìm $x$ để $A=\dfrac{1}{2}$." \textit{(Đề cuối kì I, Phòng GD\&ĐT Hoài Đức, 2024--2025)}. Đáp: đổi $\dfrac{2+5\sqrt{x}}{4-x}=-\dfrac{2+5\sqrt{x}}{x-4}$; $A=\dfrac{(\sqrt{x}+1)(\sqrt{x}+2)+2\sqrt{x}(\sqrt{x}-2)-(2+5\sqrt{x})}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{3x-6\sqrt{x}}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{3\sqrt{x}(\sqrt{x}-2)}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{3\sqrt{x}}{\sqrt{x}+2}$. b) $6\sqrt{x}=\sqrt{x}+2$; $5\sqrt{x}=2$; $\sqrt{x}=\dfrac{2}{5}$; $x=\dfrac{4}{25}$ (thỏa mãn).
[Bài 10.] level 2, dang_id "D04". "[TH] Giải bài toán sau bằng cách lập hệ phương trình: Trong đầu tháng 10 vừa qua, để chở hàng hóa ủng hộ đồng bào Thái Nguyên sau cơn bão số 11, một xí nghiệp đã huy động $20$ xe tải gồm hai loại: xe cỡ lớn với tải trọng $10$ tấn và xe cỡ nhỏ với tải trọng $5$ tấn tham gia vận chuyển. Do mỗi xe đều chở đủ tải trọng nên xí nghiệp đã vận chuyển được tổng cộng $140$ tấn hàng hóa. Tính số xe mỗi loại của xí nghiệp." \textit{(Đề cuối kì I, THCS Giang Biên, 2025--2026)}. Đáp: $\begin{cases}x+y=20\\10x+5y=140\end{cases}$ ($x,y\in\mathbb{N}^*$); $x=8$, $y=12$.
[Bài 11.] level 2, dang_id "D04". "[TH] Giải bài toán bằng cách lập phương trình hoặc lập hệ phương trình: Trong một xưởng có hai chiếc máy sản xuất cốc giấy. Mỗi giờ máy thứ nhất làm được nhiều hơn máy thứ hai $100$ chiếc cốc giấy. Nếu máy thứ nhất làm trong $3$ giờ và máy thứ hai làm trong $4$ giờ thì cả hai máy làm được $1700$ cốc giấy. Hỏi mỗi giờ mỗi máy làm được bao nhiêu chiếc cốc giấy?" \textit{(Đề học kì I, Phòng Văn hóa -- Xã hội phường Ba Đình, 2025--2026)}. Đáp: $\begin{cases}x-y=100\\3x+4y=1700\end{cases}$; $x=300$, $y=200$.
[Ví dụ 6] (có Phân tích ngắn) "Trong một cuộc thi Olympic, ban tổ chức quy định mỗi thí sinh phải trả lời hết $20$ câu hỏi, mỗi câu trả lời đúng được cộng $5$ điểm, mỗi câu trả lời sai bị trừ $2$ điểm. Thí sinh được ít nhất $30$ điểm mới được vào vòng tiếp theo. Hỏi thí sinh cần trả lời đúng ít nhất bao nhiêu câu thì được vào vòng tiếp theo?" \textit{(Đề học kì I, Cụm chuyên môn số 14 Hà Nội, 2025--2026)}. Lời giải: gọi số câu trả lời đúng là $x$ (câu), $x\in\mathbb{N}$, $x\le20$; số câu sai $20-x$; "ít nhất $30$ điểm" nên $5x-2(20-x)\ge30$; $5x-40+2x\ge30$; $7x\ge70$; $x\ge10$. Vậy cần trả lời đúng ít nhất $10$ câu. Có ≥ 3 ô [[fill:…]] (dấu $\ge$, biểu thức số câu sai, nghiệm).
[Bài 12.] level 2, dang_id "D09". "[TH] Giải bài toán bằng cách lập bất phương trình: Trong đợt bán nhà giá rẻ cho người lao động có thu nhập thấp, nhà bạn Tùng đã được chọn mua căn hộ chung cư với giá $790$ triệu đồng và được ưu đãi trả góp không lãi suất. Gia đình Tùng đã tiết kiệm được số tiền là $300$ triệu đồng. Sau thời điểm đó, mỗi tháng gia đình Tùng đều trả góp trung bình được $20$ triệu đồng. Hỏi sau ít nhất bao nhiêu tháng gia đình Tùng có thể trả hết số tiền mua căn hộ đó?" \textit{(Đề cuối kì I, THCS Giang Biên, 2025--2026)}. Đáp: gọi số tháng $x$ ($x\in\mathbb{N}^*$); $300+20x\ge790$; $20x\ge490$; $x\ge24{,}5$; $x$ nguyên nên ít nhất $25$ tháng.
[Ví dụ 7] "Cho hai biểu thức $A=\dfrac{\sqrt{x}-5}{3}$ và $B=\dfrac{3}{\sqrt{x}+2}$ với $x\ge0$, $x\ne4$. Cho $P=A\cdot B$. Tìm số nguyên $x$ lớn nhất để $P<\dfrac{1}{2}$." \textit{(Trích Bài 2 đề cuối kì I, Phòng GD\&ĐT Quốc Oai, 2024--2025; biểu thức $B$ đã rút gọn)}. Lời giải: $P=\dfrac{\sqrt{x}-5}{\sqrt{x}+2}$; $P<\dfrac12$ khi $\dfrac{\sqrt{x}-5}{\sqrt{x}+2}-\dfrac{1}{2}<0$; $\dfrac{2(\sqrt{x}-5)-(\sqrt{x}+2)}{2(\sqrt{x}+2)}<0$; $\dfrac{\sqrt{x}-12}{2(\sqrt{x}+2)}<0$; vì $2(\sqrt{x}+2)>0$ nên $\sqrt{x}-12<0$; $\sqrt{x}<12$; $x<144$; kết hợp điều kiện $0\le x<144$, $x\ne4$; số nguyên lớn nhất $x=143$. Ô [[fill:…]] ở: tử sau quy đồng, dấu của mẫu, kết hợp điều kiện, đáp số.
[Bài 13.] level 3, dang_id "D16". "Cho hai biểu thức $A=\dfrac{\sqrt{x}}{3\sqrt{x}+1}$ và $B=\dfrac{x+3}{x-9}+\dfrac{2}{\sqrt{x}+3}+\dfrac{1}{\sqrt{x}-3}$ với $x>0$, $x\ne9$.[[br]]1) [NB] Tính giá trị của biểu thức $A$ khi $x=16$.[[br]]2) [TH] Chứng minh $B=\dfrac{\sqrt{x}}{\sqrt{x}-3}$.[[br]]3) [VD] Cho $P=B:A$. Tìm $x$ nguyên lớn nhất để $P<3$." \textit{(Đề cuối kì I, THCS Tân Triều, 2025--2026)}. Đáp: 1) $A=\dfrac{4}{13}$. 2) $B=\dfrac{x+3+2(\sqrt{x}-3)+\sqrt{x}+3}{(\sqrt{x}-3)(\sqrt{x}+3)}=\dfrac{x+3\sqrt{x}}{(\sqrt{x}-3)(\sqrt{x}+3)}=\dfrac{\sqrt{x}}{\sqrt{x}-3}$. 3) $P=\dfrac{\sqrt{x}}{\sqrt{x}-3}\cdot\dfrac{3\sqrt{x}+1}{\sqrt{x}}=\dfrac{3\sqrt{x}+1}{\sqrt{x}-3}$; $P-3=\dfrac{10}{\sqrt{x}-3}<0$; $\sqrt{x}<3$; $x<9$; kết hợp $x>0$: $0<x<9$; $x$ nguyên lớn nhất là $8$.
[Ví dụ 8] (có Phân tích + bảng: Kế hoạch, Thực tế) "Theo kế hoạch hai tổ sản xuất $700$ sản phẩm. Nhưng khi thực hiện, tổ thứ nhất vượt mức $20\%$, tổ thứ hai giảm mức $10\%$ so với kế hoạch. Vì vậy hai tổ sản xuất được $720$ sản phẩm. Hỏi theo kế hoạch mỗi tổ sản xuất bao nhiêu sản phẩm?" \textit{(Đề cuối kì I, THCS Lý Sơn, 2025--2026; Phòng GD\&ĐT Thanh Trì, 2024--2025)}. Lời giải: $\begin{cases}x+y=700\\1{,}2x+0{,}9y=720\end{cases}$ ($x,y\in\mathbb{N}^*$, $x,y<700$); thế $y=700-x$: $1{,}2x+630-0{,}9x=720$; $0{,}3x=90$; $x=300$; $y=400$. Ô [[fill:…]] ở: $120\%x$ hay $1{,}2x$, $90\%y$ hay $0{,}9y$, phương trình thứ hai, nghiệm.
[Bài 14.] level 3, dang_id "D04". "[VD] Giải bài toán sau bằng cách lập phương trình hoặc hệ phương trình: Hai xí nghiệp theo kế hoạch phải làm tổng cộng $350$ dụng cụ. Nhờ sắp xếp hợp lí dây chuyền sản xuất nên xí nghiệp I đã vượt mức $20\%$ kế hoạch, xí nghiệp II đã vượt mức $10\%$ kế hoạch, do đó cả hai xí nghiệp đã làm thêm được $50$ dụng cụ. Tìm số dụng cụ mỗi xí nghiệp phải làm theo kế hoạch." \textit{(Đề cuối kì I, THCS Ngô Gia Tự, 2025--2026)}. Đáp: $\begin{cases}x+y=350\\0{,}2x+0{,}1y=50\end{cases}$; $x=150$, $y=200$.

6 BÀI TẬP VỀ NHÀ (chặng 5, "tier":"btvn"), đúng thứ tự:
[Bài 15.] level 2, dang_id "D11". "Tính giá trị của các biểu thức sau:[[br]]a) [TH] $2\sqrt{20}+5\sqrt{45}-3\sqrt{5}$ \textit{(Đề cuối kì I, Phòng GD\&ĐT Chương Mỹ, 2024--2025)}[[br]]b) [TH] $\dfrac{2}{\sqrt{3}+1}+\sqrt{(1-\sqrt{3})^2}$ \textit{(Đề học kì I, THCS Ngô Sĩ Liên, 2024--2025)}[[br]]c) [TH] $3\sqrt{2}-4\sqrt{18}+2\sqrt{32}-\sqrt{50}$ \textit{(Đề học kì I, THCS Xuân La, 2024--2025)}". Đáp: a) $16\sqrt{5}$; b) $(\sqrt{3}-1)+(\sqrt{3}-1)=2\sqrt{3}-2$; c) $3\sqrt{2}-12\sqrt{2}+8\sqrt{2}-5\sqrt{2}=-6\sqrt{2}$.
[Bài 16.] level 2, dang_id "D13". "Giải các phương trình sau:[[br]]a) [TH] $\sqrt{9x-18}-6\sqrt{x-2}=-12$ \textit{(Đề cuối kì I, Phòng GD\&ĐT Hà Đông, 2024--2025)}[[br]]b) [TH] $2\sqrt{x-1}-\dfrac{1}{4}\sqrt{4x-4}+\dfrac{1}{2}\sqrt{9x-9}=3$ \textit{(Đề cuối kì I, THCS Phúc Đồng, 2025--2026)}[[br]]c) [TH] $\sqrt{x-2}+\sqrt{4x-8}=6$ \textit{(Đề cuối kì I, THCS và THPT M.V. Lômônôxốp, 2024--2025)}". Đáp: a) $3\sqrt{x-2}-6\sqrt{x-2}=-12$; $\sqrt{x-2}=4$; $x=18$. b) $2\sqrt{x-1}-\dfrac12\sqrt{x-1}+\dfrac32\sqrt{x-1}=3$; $3\sqrt{x-1}=3$; $x=2$. c) $3\sqrt{x-2}=6$; $\sqrt{x-2}=2$; $x=6$. (Mỗi ý nêu điều kiện xác định, đối chiếu.)
[Bài 17.] level 3, dang_id "D16". "Cho hai biểu thức $A=\dfrac{\sqrt{x}-2}{\sqrt{x}-3}$ và $B=\dfrac{-9\sqrt{x}+10}{x-4}+\dfrac{3}{\sqrt{x}+2}+\dfrac{\sqrt{x}}{\sqrt{x}-2}$ với $x\ge0$, $x\ne4$, $x\ne9$.[[br]]1) [NB] Tính giá trị của biểu thức $A$ khi $x=16$.[[br]]2) [TH] Chứng minh $B=\dfrac{\sqrt{x}-2}{\sqrt{x}+2}$.[[br]]3) [VD] Đặt $P=B:A$. Tìm tất cả các giá trị của $x$ để $P<\dfrac{1}{2}$." \textit{(Đề cuối kì I, Phòng GD\&ĐT Thanh Trì, 2024--2025)}. Đáp: 1) $A=2$. 2) $B=\dfrac{-9\sqrt{x}+10+3(\sqrt{x}-2)+\sqrt{x}(\sqrt{x}+2)}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{x-4\sqrt{x}+4}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{(\sqrt{x}-2)^2}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{\sqrt{x}-2}{\sqrt{x}+2}$. 3) $P=\dfrac{\sqrt{x}-3}{\sqrt{x}+2}$; $P-\dfrac12=\dfrac{\sqrt{x}-8}{2(\sqrt{x}+2)}<0$; $\sqrt{x}<8$; $x<64$; kết hợp: $0\le x<64$, $x\ne4$, $x\ne9$.
[Bài 18.] level 3, dang_id "D16". "Cho hai biểu thức $A=\dfrac{3}{\sqrt{x}-2}-\dfrac{\sqrt{x}+10}{x-4}$ và $B=\dfrac{\sqrt{x}+2}{\sqrt{x}-2}$ với $x\ge0$, $x\ne4$.[[br]]1) [NB] Tính giá trị của biểu thức $B$ khi $x=1$.[[br]]2) [TH] Rút gọn biểu thức $A$.[[br]]3) [VD] Đặt $P=A\cdot B$. Tìm các giá trị nguyên của $x$ để $P<-1$." \textit{(Đề cuối kì I, THCS Lý Sơn, 2025--2026)}. Đáp: 1) $B=\dfrac{1+2}{1-2}=-3$. 2) $A=\dfrac{3(\sqrt{x}+2)-(\sqrt{x}+10)}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{2\sqrt{x}-4}{(\sqrt{x}-2)(\sqrt{x}+2)}=\dfrac{2}{\sqrt{x}+2}$. 3) $P=\dfrac{2}{\sqrt{x}-2}$; $P+1=\dfrac{\sqrt{x}}{\sqrt{x}-2}<0$; vì $\sqrt{x}\ge0$ và $P+1\ne0$ nên $\sqrt{x}>0$ và $\sqrt{x}-2<0$; $0<x<4$; $x$ nguyên: $x\in\{1;2;3\}$.
[Bài 19.] level 3, dang_id "D04". "[VD] Giải bài toán bằng cách lập phương trình: Hằng ngày, Hải thường đạp xe với vận tốc $8$ km/h trên cung đường từ nhà đến trường để vừa kịp giờ vào lớp. Sáng nay, vì muốn tranh thủ ôn bài đầu giờ, Hải dự định đạp xe nhanh hơn $4$ km/h so với mọi ngày để đến sớm $10$ phút. Hỏi quãng đường từ nhà Hải đến trường dài bao nhiêu km?" \textit{(Đề cuối kì I, THCS Ngô Sĩ Liên, 2025--2026)}. Đáp: $\dfrac{x}{8}-\dfrac{x}{12}=\dfrac{1}{6}$; nhân $24$: $3x-2x=4$; $x=4$ km.
[Bài 20.] level 3, dang_id "D04". "[VD] Giải bài toán bằng cách lập hệ phương trình: Để chuẩn bị trao thưởng cho học sinh giỏi cuối năm học, một trường THCS cần mua $2000$ quyển vở và $400$ cây bút để làm phần thưởng. Nhà trường dự tính để mua với giá niêm yết sẽ cần $18$ triệu $400$ nghìn đồng. Vì mua với số lượng lớn nên đại lý bán quyết định giảm giá $5\%$ cho mỗi quyển vở và $6\%$ cho mỗi cây bút, vì thế nhà trường chỉ cần trả $17$ triệu $456$ nghìn đồng. Tính giá tiền niêm yết của mỗi quyển vở và mỗi cây bút." \textit{(Đề cuối kì I, Phòng GD\&ĐT Hà Đông, 2024--2025)}. Đáp (đơn vị nghìn đồng): $\begin{cases}2000x+400y=18\,400\\1900x+376y=17\,456\end{cases}$; $x=8$, $y=6$. Vậy vở $8\,000$ đồng, bút $6\,000$ đồng.

## Đầu ra
JSON đúng schema: {"stages":[2 chặng], "ghi_chu":"…"}.
'''


def mau():
    """Hai khối đã duyệt (phiếu B, E chương VI 9C) để Gemini xem khuôn — không chép nội dung."""
    out = []
    b = json.loads((REPO / D6 / "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json").read_text())
    for x in b["stages"][2]["blocks"]:
        if x.get("variant") == "example" and "Ví dụ 4" in x.get("text", ""):
            out.append(x)
        if x.get("label") == "Bài 4.":
            y = dict(x)
            y["statement"] = y["statement"].split("b) [NB]")[0]
            y["solution"] = y["solution"].split("[[br]]b)")[0]
            out.append(y)
    e = json.loads((REPO / D6 / "phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json").read_text())
    for s in e["stages"]:
        for x in s["blocks"]:
            if x.get("variant") == "example" and "Phân tích" in x.get("text", ""):
                out.append(x)
                break
        if len(out) >= 3:
            break
    return ("\n\n## Mẫu khối đã duyệt (chương VI — CHỈ xem khuôn JSON, cách đặt ô, nhịp xuống dòng; "
            "KHÔNG chép nội dung; lưu ý mẫu cũ còn dùng dấu $\\Leftrightarrow$ — phiếu này KHÔNG dùng)\n"
            + json.dumps(out, ensure_ascii=False, indent=0))


def main():
    m = mau()
    hd = REPO / "storage/gemini/hang-doi"
    hd.mkdir(parents=True, exist_ok=True)
    for vid, phan in (("on-ck1-9c-ds-a", SO_DO_A), ("on-ck1-9c-ds-b", SO_DO_B), ("on-ck1-9c-ds-c", SO_DO_C)):
        viec = {"id": vid, "model": MODEL, "prompt": CHUNG + KHUON_CHUNG + phan + m,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1500s",
                "meta": {"loai": "phieu-on-tap", "seed_dich": SEED}}
        out = hd / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt'])//1000}k ký tự)")


if __name__ == "__main__":
    main()


# ── Lượt 2 (15/11): sửa ô trống của 8 ví dụ theo cảnh báo vi_du_gate / dan_dat_gate ──
SUA_VI_DU = r'''
## Việc của bạn (lượt 2): sửa Ô TRỐNG [[fill:…]] của 8 ví dụ dưới đây. KHÔNG đổi đề, KHÔNG đổi số, KHÔNG đổi nhịp xuống dòng, KHÔNG thêm "suy ra", "Do đó", KHÔNG thêm \hspace* trước dòng "Vậy" (dòng "Vậy" bắt đầu sát lề).
Máy soát đã báo, phải sửa hết:
(a) Câu kết luận "Vậy …" đang in sẵn đáp số ⇒ khoét đáp số trong câu "Vậy" bằng [[fill:…]] (ví dụ "Vậy quãng đường AB dài $[[fill:90]]$ km.").
(b) "Ô ở trên, phía dưới in sẵn đáp án": nếu một ô [[fill:X]] mà dòng phía dưới lại in sẵn X thì KHOÉT LUÔN chỗ dưới (cũng [[fill:X]]) hoặc đổi chỗ khoét — không để dòng dưới lộ đáp án ô trên. Các trường hợp đã báo: Ví dụ 1 ($2\sqrt{3}$, $5\sqrt{3}$ hiện lại ở dòng dưới), Ví dụ 4 ($200$), Ví dụ 5 ($90$), Ví dụ 6 ($10$), Ví dụ 8 ($300$).
(c) Mật độ ô: mỗi ví dụ ≥ 6 ô trên 10 dòng lời giải. Thêm ô ở mắt xích then chốt: điều kiện xác định, phép đưa thừa số ra ngoài dấu căn, mẫu chung, tử sau khi quy đồng, nhân tử chung, phương trình lập được, đơn vị/điều kiện của ẩn, đổi phút ra giờ, chữ "thỏa mãn"/"không thỏa mãn". Hiện: Ví dụ 2 có 5 ô/9 dòng, Ví dụ 3 5 ô/19 dòng, Ví dụ 5 3 ô/9 dòng, Ví dụ 6 3 ô/11 dòng, Ví dụ 7 4 ô/11 dòng, Ví dụ 8 4 ô/15 dòng.
Cú pháp ô: trong $…$ thì đáp án không bọc $; ngoài $…$ thì chữ thường. Đáp án không chứa "]" hay "|". Ô không được nằm trong bảng tabular của phần Phân tích (bảng giữ nguyên).
Giữ nguyên "trẻ~em" (dấu ~ là có chủ ý).

Đầu ra: JSON đúng schema {"sua":[8 phần tử {"label":"Ví dụ N.","statement": <TOÀN BỘ trường text mới của ví dụ, bắt đầu bằng \textbf{Ví dụ N.}>, "solution":""}], "ghi_chu":"…"}.

## 8 ví dụ hiện tại (JSON)
'''


def viec_sua_vi_du():
    seed = json.loads((REPO / SEED).read_text())
    vd = [b["text"] for s in seed["stages"] for b in s["blocks"]
          if b.get("type") == "noted" and b.get("variant") == "example"]
    labels = [f"Ví dụ {i}." for i in range(1, len(vd) + 1)]
    viec = {"id": "on-ck1-9c-ds-sua-vd", "model": MODEL, "prompt": CHUNG + SUA_VI_DU + json.dumps(vd, ensure_ascii=False, indent=0),
            "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
            "meta": {"loai": "sua-bai", "seed": SEED, "labels": labels}}
    out = REPO / "storage/gemini/hang-doi" / f"{viec['id']}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))


# ── Lượt 3 (15/11): thay Bài 4 (Phương Ba Đình) — ý 1 trùng Bài 12b phiếu B ch.III ⇒ đề Hát Môn ──
SUA_BAI_4 = r'''
## Việc của bạn (lượt 3): VIẾT LẠI "Bài 4." (bài điền khuyết khung bài giải, Dạng 3, mức nhận biết) với ĐỀ MỚI dưới đây. Giữ đúng khuôn của Bài 4 cũ (kèm cuối prompt): statement = đề + nguồn + dòng "(Điền vào chỗ chấm để hoàn thành bài giải, ý 1 và ý 2 làm như Ví dụ 3.)" + khung 3 ý (ô [[blank:1.6cm]] / [[blank:4cm]], mật độ ≥ 6 ô/10 dòng, đáp án ô không lộ ở dòng dưới); "solution" = khung đã điền đủ. Thẻ [NB] ở từng ý 1), 2), 3) trong ĐỀ (không gắn thẻ trong khung). Dòng "Vậy" sát lề (không \hspace* trước "Vậy"). Không dùng "suy ra", "Do đó", $\Leftrightarrow$.
ĐỀ (nguyên văn, không đổi số): "Cho hai biểu thức $A=\dfrac{\sqrt{x}-2}{\sqrt{x}-1}$ và $B=\dfrac{x-5}{x-1}-\dfrac{2}{\sqrt{x}+1}+\dfrac{4}{\sqrt{x}-1}$ với $x\ge0$, $x\ne1$.[[br]]1) [NB] Tính giá trị của biểu thức $A$ tại $x=25$.[[br]]2) [NB] Chứng minh rằng $B=\dfrac{\sqrt{x}+1}{\sqrt{x}-1}$.[[br]]3) [NB] Đặt $P=\dfrac{A}{B}$. Tìm giá trị $x$ là số nguyên tố lớn nhất để $P<\dfrac{1}{2}$." Nguồn: \textit{(Đề cuối kì I, THCS Hát Môn, 2025--2026)}.
ĐÁP SỐ (đã kiểm bằng máy): 1) $x=25$ thỏa mãn, $\sqrt{25}=5$, $A=\dfrac{5-2}{5-1}=\dfrac{3}{4}$. 2) mẫu chung $(\sqrt{x}-1)(\sqrt{x}+1)$; $B=\dfrac{x-5-2(\sqrt{x}-1)+4(\sqrt{x}+1)}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{x+2\sqrt{x}+1}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{(\sqrt{x}+1)^2}{(\sqrt{x}-1)(\sqrt{x}+1)}=\dfrac{\sqrt{x}+1}{\sqrt{x}-1}$. 3) $P=\dfrac{\sqrt{x}-2}{\sqrt{x}-1}\cdot\dfrac{\sqrt{x}-1}{\sqrt{x}+1}=\dfrac{\sqrt{x}-2}{\sqrt{x}+1}$; $P<\dfrac12$ khi $\dfrac{\sqrt{x}-2}{\sqrt{x}+1}-\dfrac{1}{2}<0$; $\dfrac{2(\sqrt{x}-2)-(\sqrt{x}+1)}{2(\sqrt{x}+1)}<0$; $\dfrac{\sqrt{x}-5}{2(\sqrt{x}+1)}<0$; vì $2(\sqrt{x}+1)>0$ nên $\sqrt{x}-5<0$; $\sqrt{x}<5$; $x<25$; kết hợp điều kiện: $0\le x<25$, $x\ne1$; số nguyên tố lớn nhất nhỏ hơn $25$ là $23$. Vậy $x=23$.

Đầu ra: JSON đúng schema {"sua":[{"label":"Bài 4.","statement":"…","solution":"…","hints":[]}], "ghi_chu":"…"}.

## Bài 4 cũ (chỉ xem khuôn — KHÔNG giữ nội dung)
'''


def viec_sua_bai_4():
    seed = json.loads((REPO / SEED).read_text())
    cu = next(b for s in seed["stages"] for b in s["blocks"] if b.get("label") == "Bài 4.")
    viec = {"id": "on-ck1-9c-ds-sua-b4", "model": MODEL,
            "prompt": CHUNG + SUA_BAI_4 + json.dumps({"statement": cu["statement"], "solution": cu["solution"]}, ensure_ascii=False),
            "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
            "meta": {"loai": "sua-bai", "seed": SEED, "labels": ["Bài 4."]}}
    out = REPO / "storage/gemini/hang-doi" / f"{viec['id']}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))
