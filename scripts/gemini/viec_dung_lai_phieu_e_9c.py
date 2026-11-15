#!/usr/bin/env python3
"""Dựng lại 3 chặng luyện tập phiếu E ch.VI 9C theo MẠCH DẠNG TOÁN (Thầy 12/11/2026).

Thầy: "MẤY CÂU NB TỰ BỊA À??? K CÓ THÔNG TIN HS ĐIỀN KIỂU GÌ???" · "HS cần cách làm, phân tích như thế nào
rồi trình bày được, song song với đó là cách giải phương trình". Chốt: 3 mạch (năng suất / chuyển động / làm chung),
ví dụ phân tích bằng câu hỏi dẫn, bài NB + TH dùng bảng đại lượng. Mọi bài giải đến đáp số.
Đề + đáp số do Claude chọn và kiểm SymPy; Gemini viết chữ.

    python3 scripts/gemini/viec_dung_lai_phieu_e_9c.py
    python3 scripts/gemini/tho.py --mot dung-9c-ch6-phieu-e-lop   (và dung-9c-ch6-phieu-e-btvn)
    python3 scripts/gemini/lap_dung_lai_phieu_e_9c.py [--ghi]
"""
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json"
VID_LOP, VID_BTVN = "dung-9c-ch6-phieu-e-lop", "dung-9c-ch6-phieu-e-btvn"

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, Bài 21 "Giải bài toán bằng cách lập phương trình", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Vì sao dựng lại (giáo viên chê bản cũ)
Bản cũ băm bài lời văn thành mảnh rời KHÔNG CÓ DỮ KIỆN ("Tìm số xe của một đội: Gọi … là x, điều kiện …", "x là số sản phẩm, giải ra 50 và −60", "tính ra x = 50, viết kết luận", "lập phương trình, chưa cần giải"). Học sinh không biết lấy gì để điền và không bao giờ đi trọn một bài. Giáo viên chốt: học sinh cần CÁCH LÀM — PHÂN TÍCH đề thế nào, rồi TRÌNH BÀY được, SONG SONG với GIẢI PHƯƠNG TRÌNH đến đáp số.

## Luật cứng (vi phạm bị trả lại)
- MỌI bài có ĐỀ ĐẦY ĐỦ dữ kiện (chép nguyên đề ở mục "Đề và đáp số"). MỌI bài giải ĐẾN ĐÁP SỐ, không có chữ "chưa cần giải".
- Trình bày theo 3 bước SGK: Bước 1 lập phương trình (chọn ẩn + điều kiện, biểu diễn các đại lượng chưa biết, lập phương trình) → Bước 2 giải phương trình (ẩn ở mẫu: quy đồng mẫu hai vế rồi khử mẫu, đưa về $ax^2+bx+c=0$, tính $\Delta$ hoặc $\Delta'$, hai nghiệm) → Bước 3 trả lời (đối chiếu điều kiện, loại nghiệm, kết luận kèm đơn vị, trả lời ĐỦ điều đề hỏi).
- Lời giải mỗi bước một dòng [[br]], câu "Vậy …" dòng riêng ở cuối. Viết "Ta có $\Delta'=\ldots=2500$, $\sqrt{\Delta'}=50$." (KHÔNG viết "$\Delta'>0$ nên $\sqrt{\Delta'}=$"). Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác".
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Không "khuôn", "Câu III", điểm số, thang điểm. Không xưng hô ("em", "các em", "ta đi", "hôm nay"). Viết "Kiểm tra", không "Kiểm"/"Soi".
- Thẻ mức đặt ở ĐẦU MỖI Ý: "a) [NB] …". Bài TH/VD một ý thì thẻ "[TH]"/"[VD]" đứng đầu đề (sau nhãn, trước chữ). Không gắn thẻ ở cả đề lẫn ý.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy $0{,}5$, nghìn $1\,500$, số bài SGK viết "Bài 6{.}32". Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT".
- Tự tính lại MỌI con số. Số liệu và đáp số ở mục "Đề và đáp số" ĐÃ ĐƯỢC MÁY KIỂM — dùng đúng, không đổi. Nghi ngờ gì ghi vào "ghi_chu".

## Khuôn khối (JSON)
1) Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. Bài toán năng suất"}
2) Ví dụ (giáo viên làm cùng lớp, phân tích bằng CÂU HỎI DẪN):
{"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Phân tích}[[br]]$\\bullet$\\; Đề hỏi gì? <trả lời>[[br]]$\\bullet$\\; Chọn ẩn: <ẩn, đơn vị, điều kiện>[[br]]$\\bullet$\\; Đại lượng nào biểu diễn được qua ẩn? <…>[[br]]$\\bullet$\\; Câu nào trong đề cho quan hệ để lập phương trình? <trích câu> $\\Rightarrow$ <phương trình>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…"}
   Trong phần Lời giải khoét 5–7 ô bằng [[fill:đáp án]] ở chỗ then chốt (biểu thức biểu diễn, phương trình đã khử mẫu, giá trị $\Delta$, hai nghiệm, kết luận). Ô nằm trong $…$ thì đáp án KHÔNG bọc $ (ví dụ "$\Delta'=[[fill:2500]]$"); ô ngoài $…$ có công thức thì bọc $ bên trong (ví dụ "[[fill:$x=50$]]").
3) Bài NB (bài trình bày hoàn chỉnh, điền khuyết) — trường "statement":
"<đề đầy đủ> \\;(<nguồn nếu có>)[[br]]Điền vào chỗ chấm để hoàn thành bài giải.\\par\\nopagebreak\\smallskip\\begin{center}\\footnotesize\\renewcommand\\arraystretch{1.5}\\begin{tabular}{|l|c|c|c|}\\hline & \\textbf{<cột 1>} & \\textbf{<cột 2>} & \\textbf{<cột 3>} \\\\ \\hline <dòng 1> & … & … & … \\\\ \\hline <dòng 2> & … & … & … \\\\ \\hline \\end{tabular}\\end{center}\\smallskip a) [NB] Gọi … là $x$ (…), điều kiện $\\ldots\\ldots$[[br]]b) [NB] <biểu diễn theo bảng: … là $\\ldots\\ldots$ …>[[br]]c) [NB] Vì <câu quan hệ> nên ta có phương trình $\\ldots\\ldots$[[br]]d) [NB] Quy đồng mẫu hai vế rồi khử mẫu, ta được $\\ldots\\ldots$, tức là $\\ldots\\ldots=0$[[br]]e) [NB] Ta có $\\Delta'=\\ldots\\ldots$, $\\sqrt{\\Delta'}=\\ldots$[[br]]f) [NB] $x_1=\\ldots$ (\\ldots\\ldots), $x_2=\\ldots$ (\\ldots\\ldots)[[br]]g) [NB] Vậy \\ldots\\ldots\\ldots\\ldots"
   Bảng: ô học sinh tự điền ghi "$\\ldots\\ldots$", ô đề cho sẵn ghi số. Trong bảng giữ 1–2 ô in sẵn ở dòng đầu làm mồi. Chữ "hoàn thành bài giải" PHẢI có trong statement. "solution": đáp án từng ý a) … g) (kể cả các ô của bảng ở ý a hoặc b), mỗi ý một dòng.
4) Bài TH (tự phân tích, tự trình bày) — "statement": "[TH] <đề đầy đủ> \\;(<nguồn>)[[br]]Kẻ bảng đại lượng rồi giải bài toán.\\par\\nopagebreak\\smallskip\\begin{center}…bảng cùng khuôn nhưng MỌI ô số liệu để TRỐNG bằng \\hspace{2.2cm}, chỉ có tiêu đề cột và tên dòng…\\end{center}" ; "solution": lời giải đầy đủ 3 bước; "hints": 1–2 câu hỏi gợi ý kiểu Polya (đại lượng nào chưa biết, hai đại lượng nào chênh nhau bao nhiêu) — không gọi tên công thức, không lộ số.
5) Bài VD (đề thi, tự làm hết) — "statement": "[VD] <đề đầy đủ> \\;(<nguồn>)" ; "solution" đầy đủ ; "hints": 1–2 câu hỏi.
Khối bài: {"type":"problem","label":"Bài N.","level":1|2|3,"tier":"onclass"|"btvn","statement":…,"solution":…,"hints":[…]}. NB level 1, TH level 2, VD level 3.
'''

PROMPT_LOP = CHUNG + r'''
## Việc: dựng 2 chặng trên lớp
### Chặng "practice1" — title "Luyện tập 1 — Nhận biết", number 3. Thứ tự khối:
- heading "Mạch 1. Bài toán năng suất (kế hoạch và thực tế)" → Ví dụ 1 → Bài 1. (NB)
- heading "Mạch 2. Bài toán chuyển động" → Ví dụ 2 → Bài 2. (NB)
- heading "Mạch 3. Bài toán làm chung, làm riêng" → Ví dụ 3 → Bài 3. (NB)
teacher_note: khoảng 60 phút. Mỗi mạch: giáo viên làm Ví dụ cùng lớp (hỏi lần lượt các câu phân tích, học sinh điền ô), rồi học sinh tự điền bài NB ngay sau; chữa xong mới sang mạch sau. Nhấn: đổi phút ra giờ trước khi lập, đối chiếu điều kiện trước khi kết luận.
### Chặng "practice2" — title "Luyện tập 2 — Thông hiểu \& Vận dụng", number 4. Thứ tự: Bài 4. (TH năng suất), Bài 5. (TH chuyển động), Bài 6. (TH làm chung), Bài 7. (VD), Bài 8. (VD).
teacher_note: khoảng 60 phút. Bài 4–6 học sinh tự kẻ bảng và trình bày (mỗi bài khoảng 10 phút), giáo viên chấm khâu bảng và phương trình trước. Bài 7, 8 khoảng 15 phút mỗi bài. Bài 8 đề hỏi vận tốc lúc tăng tốc $x+6$ và câu hỏi phụ về giới hạn tốc độ.

## Đề và đáp số (đã kiểm bằng máy)
- Ví dụ 1. (năng suất, đề tự soạn, không nguồn): Theo kế hoạch, một xưởng phải may $480$ chiếc áo trong một số ngày. Thực tế mỗi ngày xưởng may ít hơn kế hoạch $8$ chiếc nên hoàn thành chậm hơn $2$ ngày. Hỏi theo kế hoạch mỗi ngày xưởng phải may bao nhiêu chiếc áo? Ẩn $x$ (chiếc), $x$ nguyên, $x>8$. Phương trình $\dfrac{480}{x-8}-\dfrac{480}{x}=2$. Khử mẫu $480x-480(x-8)=2x(x-8)$, tức $x^2-8x-1920=0$. $\Delta'=(-4)^2-1\cdot(-1920)=1936$, $\sqrt{\Delta'}=44$. $x_1=48$ (thoả mãn), $x_2=-40$ (loại). Đáp số $48$ chiếc áo.
- Bài 1. NB (năng suất): đề NGUYÊN VĂN mục "Nguồn — Sở minh họa" bên dưới. Bảng cột "Tổng sản phẩm | Mỗi ngày | Số ngày", dòng "Kế hoạch | $300$ | $x$ | …", "Thực tế | $300$ | … | …". Phương trình $\dfrac{300}{x}-\dfrac{300}{x+10}=1$. Khử mẫu $300(x+10)-300x=x(x+10)$, tức $x^2+10x-3000=0$. $\Delta'=5^2+3000=3025$, $\sqrt{\Delta'}=55$. $x_1=50$ (thoả mãn), $x_2=-60$ (loại). Đáp số $50$ sản phẩm.
- Ví dụ 2. (chuyển động, đề tự soạn): Hai xe máy cùng khởi hành từ $A$ đến $B$, quãng đường $AB$ dài $45$ km. Xe thứ hai đi nhanh hơn xe thứ nhất $15$ km/h nên đến $B$ sớm hơn xe thứ nhất $15$ phút. Tính vận tốc của mỗi xe. Ẩn $x$ km/h, $x>0$. $15$ phút $=\dfrac{1}{4}$ giờ. Phương trình $\dfrac{45}{x}-\dfrac{45}{x+15}=\dfrac{1}{4}$. Khử mẫu $180(x+15)-180x=x(x+15)$, tức $x^2+15x-2700=0$. $\Delta=15^2+4\cdot 2700=11025$, $\sqrt{\Delta}=105$. $x_1=45$, $x_2=-60$ (loại). Đáp số $45$ km/h và $60$ km/h.
- Bài 2. NB (chuyển động): đề NGUYÊN VĂN mục "Nguồn — Chương Mỹ 50 km". Bảng "Quãng đường | Vận tốc | Thời gian", dòng "Xe máy | $50$ | $x$ | …", "Ô tô | $50$ | … | …". $25$ phút $=\dfrac{5}{12}$ giờ. Phương trình $\dfrac{50}{x}-\dfrac{50}{x+20}=\dfrac{5}{12}$. Khử mẫu $600(x+20)-600x=5x(x+20)$, tức $x^2+20x-2400=0$. $\Delta'=10^2+2400=2500$, $\sqrt{\Delta'}=50$. $x_1=40$, $x_2=-60$ (loại). Đáp số xe máy $40$ km/h, ô tô $60$ km/h.
- Ví dụ 3. (làm chung, đề tự soạn): Hai đội công nhân cùng làm một công việc thì sau $2$ giờ $24$ phút xong. Nếu làm riêng thì đội thứ nhất xong sớm hơn đội thứ hai $2$ giờ. Hỏi nếu làm riêng thì mỗi đội hoàn thành công việc trong bao lâu? $2$ giờ $24$ phút $=\dfrac{12}{5}$ giờ. Ẩn $x$ giờ, $x>0$. Phương trình $\dfrac{1}{x}+\dfrac{1}{x+2}=\dfrac{5}{12}$. Khử mẫu $12(x+2)+12x=5x(x+2)$, tức $5x^2-14x-24=0$. $\Delta'=(-7)^2+5\cdot 24=169$, $\sqrt{\Delta'}=13$. $x_1=4$, $x_2=-\dfrac{6}{5}$ (loại). Đáp số $4$ giờ và $6$ giờ.
- Bài 3. NB (làm chung): đề NGUYÊN VĂN mục "Nguồn — Ứng Hòa". Bảng "Thời gian làm riêng | Phần việc làm trong 1 giờ", dòng "Người thứ nhất | $x$ | …", "Người thứ hai | … | …", "Cả hai người | $\dfrac{18}{5}$ | …" (bảng này 2 cột số liệu — tự chỉnh tabular {|l|c|c|}). $3$ giờ $36$ phút $=\dfrac{18}{5}$ giờ. Phương trình $\dfrac{1}{x}+\dfrac{1}{x+3}=\dfrac{5}{18}$. Khử mẫu $18(x+3)+18x=5x(x+3)$, tức $5x^2-21x-54=0$. $\Delta=(-21)^2+4\cdot 5\cdot 54=1521$, $\sqrt{\Delta}=39$. $x_1=\dfrac{21+39}{10}=6$, $x_2=\dfrac{21-39}{10}=-\dfrac{9}{5}$ (loại). Đáp số người thứ nhất $6$ giờ, người thứ hai $9$ giờ.
- Bài 4. TH (năng suất): đề NGUYÊN VĂN mục "Nguồn — Chương Mỹ 60 tấn", thêm câu hỏi "Hỏi lúc đầu đội có bao nhiêu xe?". Ẩn số xe lúc đầu $x$, $x$ nguyên, $x>2$. Phương trình $\dfrac{60}{x-2}-\dfrac{60}{x}=1$, tức $x^2-2x-120=0$. $\Delta'=121$, $x_1=12$, $x_2=-10$ (loại). Đáp số $12$ xe.
- Bài 5. TH (chuyển động): "Một ô tô khách khởi hành từ Hà Nội đi Hải Phòng. Sau đó $30$ phút, một ô tô con xuất phát từ cùng địa điểm ở Hà Nội và cũng đi về Hải Phòng trên cùng tuyến đường, với vận tốc lớn hơn vận tốc của ô tô khách là $20$ km/h. Hai xe đến một địa điểm ở Hải Phòng tại cùng một thời điểm. Hãy tính vận tốc của mỗi ô tô, biết rằng quãng đường Hà Nội – Hải Phòng dài khoảng $120$ km. \;(SGK Toán 9 tập hai, Bài 6{.}32)". Phương trình $\dfrac{120}{x}-\dfrac{120}{x+20}=\dfrac{1}{2}$, tức $x^2+20x-4800=0$. $\Delta'=4900$, $\sqrt{\Delta'}=70$, $x_1=60$, $x_2=-80$ (loại). Đáp số ô tô khách $60$ km/h, ô tô con $80$ km/h.
- Bài 6. TH (làm chung, đề tự soạn, không nguồn): "Hai vòi nước cùng chảy vào một bể cạn thì sau $6$ giờ đầy bể. Nếu chảy riêng thì vòi thứ nhất làm đầy bể nhanh hơn vòi thứ hai $5$ giờ. Hỏi nếu chảy riêng thì mỗi vòi làm đầy bể trong bao lâu?" Phương trình $\dfrac{1}{x}+\dfrac{1}{x+5}=\dfrac{1}{6}$, tức $x^2-7x-30=0$. $\Delta=169$, $x_1=10$, $x_2=-3$ (loại). Đáp số $10$ giờ và $15$ giờ.
- Bài 7. VD: đề NGUYÊN VĂN mục "Nguồn — Đông Anh 140 tấn". Ẩn số ngày theo kế hoạch $x$, $x$ nguyên, $x>1$. Mỗi ngày kế hoạch $\dfrac{140}{x}$ tấn, thực tế $\dfrac{140}{x}+5$ tấn trong $x-1$ ngày, chở được $150$ tấn. Phương trình $\left(\dfrac{140}{x}+5\right)(x-1)=150$, tức $x^2-3x-28=0$. $\Delta=121$, $x_1=7$, $x_2=-4$ (loại). Đáp số $7$ ngày.
- Bài 8. VD: đề NGUYÊN VĂN mục "Nguồn — Tự Lập" (đổi "Hôm nay" thành "Một hôm"). Phương trình $\dfrac{3}{x}+\dfrac{1}{20}+\dfrac{9}{x+6}=\dfrac{12}{x}$, tức $\dfrac{9}{x}-\dfrac{9}{x+6}=\dfrac{1}{20}$, khử mẫu $180(x+6)-180x=x(x+6)$, $x^2+6x-1080=0$, $\Delta'=1089$, $\sqrt{\Delta'}=33$, $x_1=30$, $x_2=-36$ (loại). Vận tốc khi tăng tốc $36$ km/h, $36<40$ nên không vi phạm.

## Đầu ra
JSON schema {"stages":[{"kind":"practice1",…},{"kind":"practice2",…}],"ghi_chu"}. Mỗi stage có "kind","number","title","teacher_note","blocks".
'''

PROMPT_BTVN = CHUNG + r'''
## Việc: dựng phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", đánh số tiếp từ Bài 9.)
Thứ tự: Bài 9. NB, Bài 10. NB, Bài 11. TH, Bài 12. TH, Bài 13. TH, Bài 14. VD, Bài 15. VD. Không có ví dụ, không có tiêu đề mạch.
Trả về MỘT stage {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":<ghi chú>,"blocks":[7 bài]}. teacher_note: sơ đồ tư duy 5 phút cuối buổi; Bài tập về nhà là Bài 9 đến Bài 15, khoảng 85 phút, in thành phiếu riêng; Bài 10 là dạng hình chữ nhật chưa làm trên lớp nên có khung điền đầy đủ; buổi sau chữa Bài 14 và Bài 15 trước.

## Đề và đáp số (đã kiểm bằng máy)
- Bài 9. NB (năng suất): "Một đội xe gồm các xe tải cùng loại, cần phải chở $120$ tấn hàng. Tuy nhiên khi làm việc, có hai xe phải điều chuyển đi nơi khác nên mỗi xe phải chở thêm $3$ tấn hàng. Hỏi đội xe đó có bao nhiêu chiếc xe tải? \;(SGK Toán 9 tập hai, Luyện tập trang 27)". Bảng "Tổng khối lượng | Số xe | Mỗi xe chở", dòng "Dự định | $120$ | $x$ | …", "Thực tế | $120$ | … | …". Ẩn $x$ nguyên, $x>2$. Phương trình $\dfrac{120}{x-2}-\dfrac{120}{x}=3$. Khử mẫu $120x-120(x-2)=3x(x-2)$, tức $x^2-2x-80=0$. $\Delta'=81$, $\sqrt{\Delta'}=9$, $x_1=10$, $x_2=-8$ (loại). Đáp số $10$ xe.
- Bài 10. NB (hình chữ nhật, đề tự soạn): "Một mảnh đất hình chữ nhật có chiều dài hơn chiều rộng $4$ m và diện tích bằng $96$ m$^2$. Tính chiều dài và chiều rộng của mảnh đất." Bảng "Chiều rộng | Chiều dài | Diện tích", MỘT dòng "Mảnh đất | $x$ | … | …". Không có ẩn ở mẫu nên ý d) viết "Khai triển và chuyển vế, ta được $\ldots\ldots=0$". Phương trình $x(x+4)=96$, tức $x^2+4x-96=0$. $\Delta'=100$, $\sqrt{\Delta'}=10$, $x_1=8$, $x_2=-12$ (loại). Đáp số chiều rộng $8$ m, chiều dài $12$ m.
- Bài 11. TH (chuyển động): "Một người đi xe máy từ $A$ đến $B$ với vận tốc $40$ km/h. Lúc về, người đó đi với vận tốc $30$ km/h nên thời gian về nhiều hơn thời gian đi $45$ phút. Tính độ dài quãng đường $AB$. \;(Cuối kì I, THCS Ái Mộ)". Ẩn $s$ km, $s>0$. Phương trình $\dfrac{s}{30}-\dfrac{s}{40}=\dfrac{3}{4}$, khử mẫu $4s-3s=90$, $s=90$. Đáp số $90$ km. (Phương trình bậc nhất — giải bình thường.)
- Bài 12. TH (làm chung, đề tự soạn): "Hai vòi nước cùng chảy vào một bể cạn thì sau $4$ giờ đầy bể. Nếu chảy riêng thì vòi thứ nhất làm đầy bể nhanh hơn vòi thứ hai $6$ giờ. Hỏi nếu chảy riêng thì mỗi vòi làm đầy bể trong bao lâu?" Phương trình $\dfrac{1}{x}+\dfrac{1}{x+6}=\dfrac{1}{4}$, khử mẫu $4(x+6)+4x=x(x+6)$, tức $x^2-2x-24=0$. $\Delta'=25$, $x_1=6$, $x_2=-4$ (loại). Đáp số $6$ giờ và $12$ giờ.
- Bài 13. TH (năng suất): "Một xưởng may phải may $1\,500$ chiếc áo trong thời gian quy định. Để hoàn thành sớm kế hoạch, mỗi ngày xưởng đã may được nhiều hơn $10$ chiếc áo so với số áo phải may trong một ngày theo kế hoạch. Vì thế ba ngày trước khi hết thời hạn, xưởng đã may được $1\,320$ áo. Hỏi theo kế hoạch, mỗi ngày xưởng đó phải may xong bao nhiêu chiếc áo? \;(SGK Toán 9 tập hai, Bài 6{.}33)". Ẩn $x$ nguyên dương. Phương trình $\left(\dfrac{1500}{x}-3\right)(x+10)=1320$. Nhân hai vế với $x$: $(1500-3x)(x+10)=1320x$, tức $x^2-50x-5000=0$. $\Delta'=625+5000=5625$, $\sqrt{\Delta'}=75$, $x_1=100$, $x_2=-50$ (loại). Đáp số $100$ chiếc áo. Bảng "Số áo | Mỗi ngày | Số ngày" dòng "Kế hoạch", "Thực tế (đến 3 ngày trước hạn)".
- Bài 14. VD: đề NGUYÊN VĂN mục "Nguồn — Thanh Oai". Ẩn $x$ sản phẩm/giờ, $x$ nguyên dương. Thời gian dự định $\dfrac{60}{x}$ giờ, thực tế $\dfrac{60}{x}-\dfrac{1}{2}$ giờ, mỗi giờ $x+2$, làm được $63$ sản phẩm. Phương trình $(x+2)\left(\dfrac{60}{x}-\dfrac{1}{2}\right)=63$, tức $x^2+8x-240=0$. $\Delta'=256$, $x_1=12$, $x_2=-20$ (loại). Đáp số $12$ sản phẩm.
- Bài 15. VD: đề NGUYÊN VĂN mục "Nguồn — Chương Dương". Phương trình $\dfrac{60}{x}+\dfrac{1}{2}+\dfrac{60}{x+10}=\dfrac{120}{x}$, tức $\dfrac{60}{x}-\dfrac{60}{x+10}=\dfrac{1}{2}$, khử mẫu $120(x+10)-120x=x(x+10)$, $x^2+10x-1200=0$. $\Delta'=1225$, $\sqrt{\Delta'}=35$, $x_1=30$, $x_2=-40$ (loại). Đáp số vận tốc ban đầu $30$ km/h, lúc sau $40$ km/h.

## Đầu ra
JSON schema {"stages":[{"kind":"reflection",…}],"ghi_chu"}.
'''


def nguon():
    goc = json.loads(subprocess.run(["git", "show", f"HEAD:{SEED}"], cwd=REPO, capture_output=True, text=True,
                                    check=True).stdout)
    k = {}
    for s in goc["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                k[b["label"]] = b["statement"]
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}(.*?)\[\[br\]\]\{\\sffamily", b.get("text", ""), re.S)
                if m:
                    k[m.group(1)] = m.group(2).strip()
    return {
        "Nguồn — Sở minh họa": k["Ví dụ 9."],
        "Nguồn — Chương Mỹ 50 km": k["Ví dụ 10."],
        "Nguồn — Ứng Hòa": k["Ví dụ 8."],
        "Nguồn — Chương Mỹ 60 tấn": k["Ví dụ 5."],
        "Nguồn — Đông Anh 140 tấn": k["Bài 16."],
        "Nguồn — Tự Lập": k["Bài 17."],
        "Nguồn — Thanh Oai": k["Bài 33."],
        "Nguồn — Chương Dương": k["Bài 34."],
    }


def main():
    ng = nguon()
    ghi_ng = ("\n## Nguyên văn đề nguồn (bản cũ — chép đề, bỏ thẻ [VD] cũ, giữ chú thích nguồn ở cuối dạng "
              "\"\\;(…)\", bỏ các yêu cầu kiểu \"Lập phương trình cho bài toán\" và thay bằng câu hỏi tìm đáp số)\n"
              + json.dumps(ng, ensure_ascii=False, indent=1) + "\n")
    for vid, prompt in ((VID_LOP, PROMPT_LOP), (VID_BTVN, PROMPT_BTVN)):
        v = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": prompt + ghi_ng, "files": [],
             "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1800s",
             "meta": {"loai": "dung-chang-phieu", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(v['prompt']) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
