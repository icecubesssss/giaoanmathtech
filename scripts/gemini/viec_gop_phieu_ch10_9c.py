#!/usr/bin/env python3
"""Sinh 2 việc Gemini: GỘP phiếu A (trụ + nón) và phiếu B (cầu) ch.X 9C thành MỘT phiếu 90′.

Thầy (12/11/2026): "Chương X lớp 9C gộp luôn cả 3 công thức dạy trong 1 buổi, rồi thêm 1 buổi
luyện tập + kiểm tra chương". Thuyết minh đã sửa (phiếu A gộp, phiếu C luyện tập + KT).

    python3 scripts/gemini/viec_gop_phieu_ch10_9c.py
    python3 scripts/gemini/tho.py --mot gop-9c-ch10-p1-tren-lop      (song song với)
    python3 scripts/gemini/tho.py --mot gop-9c-ch10-p1-btvn
    python3 scripts/gemini/lap_gop_phieu_ch10_9c.py                  (ráp 2 kết quả → seed)
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien"
MAU = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-09-duong-tron-ngoai-tiep-va-noi-tiep/phieu-a-goc-noi-tiep.json"
CU = "storage/thung-rac/2026-11-12-chuong-10-9c/refs/phieu-cu"  # seed A/B cũ, vẫn còn trong git (commit faf5baad)

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (HÌNH HỌC — chương X: hình trụ, hình nón, hình cầu) cho học sinh lớp 9 TẦNG C (học lực trung bình, ôn thi vào 10 Hà Nội). Làm CẨN THẬN, KHÔNG bịa đề: mọi đề bài lấy từ dữ liệu gốc (phiếu A, phiếu B cũ) theo đúng SƠ ĐỒ LẮP bên dưới; chỉ được đổi số liệu ở chỗ sơ đồ cho phép.

KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt.

## Bối cảnh
Trước đây chương X dạy 2 buổi: phiếu A (Bài 31 hình trụ + hình nón) và phiếu B (Bài 32 hình cầu). Giáo viên chốt GỘP thành MỘT buổi 90 phút (25 phút giáo viên giảng ví dụ + 55 phút học sinh luyện + 10 phút giải lao; bài về nhà 40 phút). Ưu tiên: hình trụ dạy kĩ (có ở 3/3 đề Vào 10), hình cầu đủ cho bài mực nước (đề minh họa của Sở), hình nón chỉ nhận biết + thay số (0/3 đề Vào 10, chỉ đề trường).
Đề ĐÍCH của buổi: Câu IV.1 đề minh họa Vào 10 của Sở (ly nước hình trụ đường kính đáy 5 cm, cao 15 cm, nước cao 10 cm; ý a thể tích nước; ý b thả 5 viên bi, nước dâng đúng miệng ly, tính thể tích mỗi viên bi). Ý a ứng với Mạch 1 (hình trụ), ý b ứng với Mạch 3 (hình cầu và bài mực nước).

## Khuôn JSON (phiếu kiểu mới — xem "Mẫu khối" cuối prompt, lấy từ một phiếu đã duyệt)
- Hình KHÔNG nhúng vào statement nữa. Mỗi bài/ví dụ có hình thì đặt vào trường "figure": {"type": "tikz", "tikz": "\\begin{tikzpicture}…\\end{tikzpicture}", "caption": "Hình N", "pos": "right", "width": "0.30"}. Lấy NGUYÊN mã tikzpicture của bản cũ (nằm trong các minipage/adjustbox của statement/text cũ), chỉ sửa nhãn số đo nếu sơ đồ đổi số liệu. statement/text mới KHÔNG còn \begin{minipage}, \adjustbox, \par\nopagebreak, \hfill, chú thích "Hình N" tự gõ.
- Bài trắc nghiệm: "statement" chỉ là câu hỏi, "options": 4 chuỗi (không ghi "A."), "answer": "A"/"B"/"C"/"D"; KHÔNG kèm \parbox phương án trong statement.
- Bài tự luận / điền: "statement" + "solution" (lời giải đầy đủ, xuống dòng bằng [[br]]). Ô điền dùng [[blank]] (không dùng \ldots).
- Mọi problem có: "type": "problem", "label" ("Bài 1." … hoặc "BTVN 1." …), "tier" ("onclass" hoặc "btvn"), "level" (1 = NB, 2 = TH, 3 = VD), "dang_id" (theo sơ đồ), "figure_given": true nếu hình vẽ sẵn số đo.
- Mỗi ý trong statement mở đầu bằng thẻ mức: "a) [NB] …", "b) [NB] …"; bài một ý thì "[NB] …" / "[TH] …" / "[VD] …" ở đầu statement. SỐ THẺ phải đúng sơ đồ (thẻ = số câu hỏi được tính giờ).
- Ví dụ = khối "noted" variant "example", text bắt đầu "\\textbf{Ví dụ N.}" rồi đề, rồi "[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]" rồi lời giải; hình đặt ở "figure".
- KHÔNG dùng khối "writelines" (học sinh làm vào vở). Không dùng \needspace.

## Luật trình bày (giáo viên đã chốt — vi phạm là bị trả lại)
1. Đề nêu MỤC TIÊU TRƯỚC: "Tính … của …" đứng đầu; mẹo/công thức (nếu có) để sau trong "(Gợi ý: …)".
2. Không văn nói, không xưng hô: cấm "em", "các em", "hôm nay", "ở lớp", "Kiểm" (phải "Kiểm tra"), "Soi". Không viết tắt.
3. Mỗi bài một đề gốc khác nhau, không trùng số liệu với ví dụ hay bài khác trong cùng phiếu; không "làm tiếp Bài N", không dùng hình của bài khác — đề phải ghi ĐỦ giả thiết.
4. Lời giải trình bày như bài thi: viết công thức → thay số → kết quả kèm ĐƠN VỊ → câu "Vậy …". Lấy $\pi \approx 3{,}14$ khi đề yêu cầu số gần đúng. Đơn vị viết cm$^2$, cm$^3$, m$^3$ như bản cũ.
5. Toán trong $…$; số thập phân viết $0{,}4$; giữ escape \% \& \#. JSON hợp lệ (gạch chéo ngược nhân đôi trong chuỗi JSON).
6. TỰ TÍNH LẠI mọi đáp số (Python trong đầu): trụ $S_{xq}=2\pi rh$, $V=\pi r^2h$; nón $S_{xq}=\pi rl$, $V=\frac13\pi r^2h$, $l^2=r^2+h^2$; cầu $S=4\pi R^2$, $V=\frac43\pi R^3$. Nghi sai chỗ nào thì ghi vào "ghi_chu".
'''

VIEC1 = r'''
## Việc của bạn: dựng 4 chặng ĐẦU (Khám phá, Kiến thức trọng tâm, Luyện tập 1, Luyện tập 2)

### Chặng 1 — {"kind":"review","number":1,"title":"Khám phá"}
- opener: viết mới (3–4 câu, không xưng "em"): ba đồ vật quen thuộc — chiếc xô nước (hình trụ), chiếc nón lá (hình nón), quả bóng (hình cầu); câu hỏi gợi mở: muốn biết vật CHỨA được bao nhiêu thì tính gì, muốn biết tốn bao nhiêu VẬT LIỆU thì tính gì. Có thể đặt "tikz" là hình ba khối của Ví dụ 1 phiếu A cũ.
- noted variant "note", title "NHẮC LẠI": từ khối "Nhắc lại Lớp 5 và chương V" của phiếu A cũ (chu vi, diện tích hình tròn; $r=d:2$; đổi đơn vị; Pythagore). Dạng gạch đầu dòng "- …" xuống dòng thật như mẫu.
- noted variant "target", title "MỤC TIÊU BUỔI HỌC": Câu IV.1 đề Vào 10 = 1,0 điểm, ma trận Sở xếp mức nhận biết; trụ 3/3 đề, cầu có ở đề minh họa (bài 5 viên bi), nón chỉ ở đề trường; cuối buổi làm trọn Câu IV.1 đề minh họa.
- teacher_note: một câu điều phối (cầm cái cốc/quả bóng hỏi cả lớp).

### Chặng 2 — {"kind":"concept","number":2,"title":"Kiến thức trọng tâm"}
Bốn thẻ lý thuyết noted variant "theory" (title như dưới), mỗi thẻ có "figure" (pos "right", width "0.28") lấy tikz của bản cũ:
- "1. HÌNH TRỤ": hai đáy là hai hình tròn bằng nhau bán kính $r$, chiều cao $h$; $S_{xq}=2\pi rh$; $V=S_{\text{đáy}}\cdot h=\pi r^2h$. (tikz: hình trụ ở Bài 1 phiếu A cũ)
- "2. HÌNH NÓN": đỉnh, bán kính đáy $r$, chiều cao $h$, đường sinh $l$; $l^2=r^2+h^2$; $S_{xq}=\pi rl$; $V=\frac{1}{3}\pi r^2h$. (tikz: Bài 5 phiếu A cũ)
- "3. HÌNH CẦU": tâm $O$, bán kính $R$; mặt cắt bởi mặt phẳng luôn là hình tròn; $S=4\pi R^2$; $V=\frac{4}{3}\pi R^3$. (tikz: Bài 1 phiếu B cũ)
- "4. BÀI MỰC NƯỚC": thả vật chìm hẳn vào bình nước thì thể tích vật $=$ thể tích phần nước DÂNG THÊM (bình đang đầy thì $=$ nước TRÀN RA); phần nước dâng thêm là hình trụ cùng bán kính đáy, chiều cao $=$ độ dâng. (tikz: Bài 7 phiếu B cũ)
Dùng \nhanly{…} để nhấn tên mục như mẫu (vd "\nhanly{Công thức.}").
- noted variant "trap", title "BẪY THƯỜNG GẶP": gộp bẫy của A và B (đường kính ↔ bán kính; chiều cao theo mực nước; đổi đơn vị; lẫn $S_{xq}$ với $V$; quên $\frac13$ của nón; cầu mũ BA ở thể tích).
- noted variant "tip", title "SÁU CÔNG THỨC VÀ HAI DÒNG BAREM": bảng 6 công thức (từ khối "Sáu công thức" phiếu B) + hai dòng barem (từ khối "Hai dòng chép thuộc" phiếu A).
- teacher_note: nhấn mạnh trụ là trọng tâm, nón chỉ thay số.

### Chặng 3 — {"kind":"practice1","number":3,"title":"Luyện tập 1"} (thứ tự khối đúng như sau)
1. para: "\\textbf{Đích của buổi học:} Câu IV.1 đề minh họa Vào 10 của Sở (Bài 9) — ý a tính thể tích nước trong ly hình trụ (Mạch 1), ý b thả bi hình cầu và tính theo mực nước dâng (Mạch 3). Mạch 2 luyện hình nón cho đề kiểm tra của trường."
2. para variant "heading": "Mạch 1. Hình trụ: đổi đường kính, thay số $S_{xq}$ và $V$"
3. Ví dụ 1 = "Ví dụ 2" phiếu A cũ (đổi đường kính sang bán kính, ly 5 cm và xô 0,4 m), giữ lời giải, hình vào "figure".
4. Bài 1. = Bài 2 phiếu A cũ (đổi $d=8$ cm, $d=0{,}6$ m). dang_id "NB1", 2 thẻ, figure_given true. Câu dẫn: "Tìm bán kính đáy của hình trụ (Hình N) trong mỗi trường hợp sau." Ô điền [[blank]].
5. Bài 2. = GỘP Bài 3 + Bài 4 phiếu A cũ thành MỘT hình trụ $r=5$ cm, $h=10$ cm: "Tính diện tích xung quanh và thể tích của hình trụ ở Hình N. Lấy $\pi \approx 3{,}14$.[[br]]a) [NB] Diện tích xung quanh.[[br]]b) [NB] Thể tích." dang_id "NB2", figure_given true (tikz Bài 3 cũ, nhãn $r=5$ cm, $h=10$ cm). Đáp số a) 314 cm$^2$, b) 785 cm$^3$.
6. para variant "heading": "Mạch 2. Hình nón: phân biệt chiều cao $h$ với đường sinh $l$"
7. Bài 3. TRẮC NGHIỆM 1 thẻ, dang_id "NB3", figure_given true (tikz Bài 6 phiếu A cũ, nhãn $r=3$ cm, $h=4$ cm): "[NB] Hình nón ở Hình N có bán kính đáy $3$ cm và chiều cao $4$ cm. Đường sinh $l$ và diện tích xung quanh $S_{xq}$ của hình nón lần lượt là" — options: "$l=5$ cm; $S_{xq}=15\pi$ cm$^2$" (đúng), "$l=7$ cm; $S_{xq}=21\pi$ cm$^2$", "$l=5$ cm; $S_{xq}=12\pi$ cm$^2$", "$l=4$ cm; $S_{xq}=12\pi$ cm$^2$" (xáo vị trí đáp án đúng, ghi answer) + "solution" ngắn hai dòng.
8. para variant "heading": "Mạch 3. Hình cầu và bài mực nước"
9. Bài 4. = GỘP Bài 3 + Bài 4 phiếu B cũ thành MỘT quả bóng ĐƯỜNG KÍNH $10$ cm: "Một quả bóng hình cầu có đường kính $10$ cm (Hình N). Lấy $\pi \approx 3{,}14$.[[br]]a) [NB] Tính diện tích mặt cầu.[[br]]b) [NB] Tính thể tích quả bóng (làm tròn đến hàng phần trăm)." dang_id "NB4" (tikz Bài 3 phiếu B cũ, nhãn đường kính). Đáp số $R=5$; $S=314$ cm$^2$; $V\approx 523{,}33$ cm$^3$.
10. Bài 5. điền 1 thẻ, dang_id "NB5", không hình: "[NB] Điền vào chỗ trống: $5572$ cm$^3 =$ [[blank]] lít; $\quad 4{,}867$ m$^3 =$ [[blank]] lít." (số liệu Bài 6 phiếu B cũ).
11. Bài 6. VẼ HÌNH 1 thẻ, dang_id "NB6", "draw": true, KHÔNG có figure: "[NB] Một ly nước hình trụ cao $12$ cm, bán kính đáy $3$ cm đang chứa nước cao $8$ cm. Thả vào ly một số viên bi thì nước dâng lên đúng miệng ly. Vẽ phác ly nước vào vở, ghi bán kính đáy, chiều cao ly, mực nước ban đầu và tô phần nước dâng thêm; cho biết phần nước dâng thêm có dạng hình gì và cao bao nhiêu xăng-ti-mét." Lời giải: hình trụ bán kính đáy 3 cm, cao $12-8=4$ cm.
12. Bài 7. KHUNG ĐIỀN KHUYẾT 1 thẻ, dang_id "NB7", figure_given true = Bài 8 phiếu B cũ (quả bóng đường kính $22$ cm, diện tích da): GỘP ba ý cũ thành MỘT bài giải mẫu có ô [[blank]] ở các chỗ cần nhớ (bán kính, công thức, phép thay số, kết quả, đơn vị, câu kết luận) — ít nhất 6 ô; câu dẫn: "[NB] Một quả bóng hình cầu có đường kính $22$ cm (Hình N). Điền vào chỗ trống để hoàn thành bài giải tính diện tích da cần dùng để may quả bóng, lấy $\pi \approx 3{,}14$.[[br]]…các dòng bài giải có [[blank]]…". solution = bài giải đầy đủ (đáp số $1519{,}76$ cm$^2$).
- teacher_note chặng 3: Bài 1 là bẫy đường kính, soi từng em; Bài 3 nón chỉ thay số.

### Chặng 4 — {"kind":"practice2","number":4,"title":"Luyện tập 2"}
1. para variant "heading": "Bậc 1. Bài thực tế một khối"
2. Ví dụ 2 = "Ví dụ 3" phiếu A cũ (Câu IV.1a đề chính thức Vào 10 năm 2026, xô $h=25$, $r=12$), giữ nguyên lời giải; hình vào figure.
3. Bài 8. 1 thẻ, dang_id "TH1", level 2 = Bài 10 phiếu A cũ CHỈ GIỮ phần thể tích + đổi lít: "[TH] Một thùng tôn hình trụ có đường kính đáy $0{,}8$ m và chiều cao $1$ m (Hình N). Tính thể tích của thùng rồi đổi ra lít. Lấy $\pi \approx 3{,}14$." Đáp số $r=0{,}4$; $V\approx 0{,}5024$ m$^3=502{,}4$ lít.
4. para variant "heading": "Bậc 2. Trọn Câu IV.1 đề thi"
5. Ví dụ 3 = "Ví dụ 5" phiếu B cũ (CK2 THCS Chu Văn An — khuôn NƯỚC TRÀN), giữ lời giải; hình vào figure.
6. Bài 9. = Bài 13 phiếu B cũ (Câu IV.1 đề minh họa của Sở) — level 3, dang_id "VD1", MỘT thẻ "[VD]" đặt đầu statement (ý a, ý b viết "a) …", "b) …" KHÔNG gắn thẻ). Giữ "hints" cũ. Viết LẠI "quy_trinh" cho ĐÚNG (bản cũ sai: nói lập phương trình tìm bán kính bi): 4 bước — (1) đổi đường kính đáy ra bán kính $r=2{,}5$ cm; (2) ý a: phần nước là hình trụ cao bằng MỰC NƯỚC $10$ cm, $V=\pi r^2h$; (3) ý b: độ dâng $15-10=5$ cm, tổng thể tích 5 viên bi $=$ thể tích phần nước dâng thêm; (4) chia cho 5, ghi đơn vị và kết luận. Lời giải: a) $196{,}25$ cm$^3$; b) $98{,}125$ cm$^3$ cho 5 viên, mỗi viên $19{,}625$ cm$^3$ (kiểm lại).
- teacher_note chặng 4: Bài 9 chấm chéo theo thang 0,5 + 0,5; trừ điểm thiếu đơn vị, thiếu câu kết luận.

## Đầu ra
JSON đúng schema: {"stages": [4 chặng trên, đúng thứ tự], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''

VIEC2 = r'''
## Việc của bạn: dựng chặng 5 — {"kind":"reflection","number":5,"title":"Sơ đồ tư duy"} (sơ đồ + BÀI TẬP VỀ NHÀ)
Phiếu BTVN in riêng nên KHÔNG cần para "Bài tập về nhà". Thứ tự khối:
1. mindmap (xem mẫu): "root": "Hình trụ $\cdot$ nón $\cdot$ cầu", "caption": "Điền các ô trống rồi ghi nhớ", "size": "small", ba nhánh "Hình trụ", "Hình nón", "Hình cầu", mỗi nhánh 2 con có ô [[blank:1.4cm]] chỗ công thức (vd "$S_{xq} = $ [[blank:1.4cm]]"), nhánh nón thêm "$l^2 =$ [[blank:1.2cm]]". KHÔNG để trống hết — chỉ khoét phần công thức.
2. Các bài BTVN (tier "btvn", label "BTVN 1." …), mỗi bài một đề, hình (nếu có) vào "figure", KHÔNG writelines:
- BTVN 1. = BTVN 2 phiếu A cũ (đổi đường kính sang bán kính, 2 thẻ [NB]), dang_id "NB1".
- BTVN 2. = GỘP BTVN 3 + BTVN 4 phiếu A cũ thành MỘT hình trụ (dùng số liệu của BTVN 3 cũ): "Tính diện tích xung quanh và thể tích của hình trụ …" a) [NB] b) [NB], dang_id "NB2". Tự tính đáp số.
- BTVN 3. = BTVN 17 phiếu A cũ (hình nón $r=4$, $h=3$, tìm đường sinh) dạng TRẮC NGHIỆM 1 thẻ (options/answer), dang_id "NB3".
- BTVN 4. = GỘP BTVN 3 + BTVN 4 phiếu B cũ thành MỘT hình cầu (dùng số liệu bán kính của BTVN 3 cũ): a) [NB] diện tích mặt cầu, b) [NB] thể tích, dang_id "NB4".
- BTVN 5. = BTVN 16 phiếu B cũ (đổi $1000$ cm$^3$ sang lít) trắc nghiệm 1 thẻ, dang_id "NB5".
- BTVN 6. = BTVN 17 phiếu B cũ (thả vật chìm, nước dâng bằng gì) trắc nghiệm 1 thẻ, dang_id "NB6".
- BTVN 7. = BTVN 8 phiếu A cũ, đổi thành KHUNG ĐIỀN KHUYẾT 1 thẻ "[NB]": một bài giải mẫu có ít nhất 6 ô [[blank]] (công thức, thay số, kết quả, đơn vị, kết luận), dang_id "NB7"; solution đầy đủ.
- BTVN 8. = BTVN 10 phiếu A cũ, 1 thẻ "[TH]" (giữ một yêu cầu tính chính có bước đường kính → bán kính và đổi đơn vị nếu có), level 2, dang_id "TH1".
- BTVN 9. = Bài 13 phiếu A cũ (Câu IV.1 đề chính thức Vào 10 năm 2025, thùng nước $r=50$ cm, $h=150$ cm, mực nước hạ $40$ cm) — level 3, dang_id "VD1", MỘT thẻ "[VD]" ở đầu statement, ý a/b không gắn thẻ; bỏ "hints"/"quy_trinh"; giữ lời giải (a) $47\,100$ cm$^2$; b) $314\,000$ cm$^3 = 314$ lít).
- teacher_note chặng 5: BTVN cố ý dôi; nếu cắt thì giữ BTVN 2, 7, 9.

## Đầu ra
JSON đúng schema: {"stages": [chỉ chặng 5], "ghi_chu": "chỗ nghi ngờ hoặc chuỗi rỗng"}.
'''


def mau_khoi():
    d = json.loads((REPO / MAU).read_text())
    out = []
    want = {("concept", "theory"), ("practice1", "problem-options"), ("practice1", "example"),
            ("practice1", "heading"), ("reflection", "mindmap"), ("practice1", "problem-solution")}
    seen = set()
    for s in d["stages"]:
        for b in s["blocks"]:
            k = b["type"]
            if k == "noted":
                k = b.get("variant")
            elif k == "para" and b.get("variant") == "heading":
                k = "heading"
            elif k == "problem":
                k = "problem-options" if b.get("options") else "problem-solution"
            key = (s["kind"], k)
            if key in want and key not in seen:
                seen.add(key)
                out.append(b)
    return out


def main():
    a = json.loads((REPO / CU / "phieu-a-hinh-tru-va-hinh-non.json").read_text())
    b = json.loads((REPO / CU / "phieu-b-hinh-cau.json").read_text())
    du_lieu = ("\n## Mẫu khối (phiếu kiểu mới đã duyệt, chỉ để xem khuôn)\n"
               + json.dumps(mau_khoi(), ensure_ascii=False, indent=1)
               + "\n\n## Dữ liệu gốc — phiếu A cũ (Bài 31)\n" + json.dumps(a["stages"], ensure_ascii=False)
               + "\n\n## Dữ liệu gốc — phiếu B cũ (Bài 32)\n" + json.dumps(b["stages"], ensure_ascii=False) + "\n")
    for vid, phan in (("gop-9c-ch10-p1-tren-lop", VIEC1), ("gop-9c-ch10-p1-btvn", VIEC2)):
        viec = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": CHUNG + phan + du_lieu,
                "files": [], "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1500s",
                "meta": {"loai": "gop-phieu", "seed_dich": f"{D}/phieu-a-hinh-tru-hinh-non-hinh-cau.json"}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(viec['prompt'])//1000}k ký tự)")


if __name__ == "__main__":
    main()
