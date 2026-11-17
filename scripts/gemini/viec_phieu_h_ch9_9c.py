#!/usr/bin/env python3
"""Việc Gemini: dựng chữ phiếu H ch.IX 9C — buổi 9.7 (t29, 03/01/2027, ca 90′)
"Chứng minh hệ thức tích bằng tam giác đồng dạng dựa vào góc nội tiếp" (Câu IV.2 ý b, phần tích).

Claude chốt sơ đồ + đề (đã soi ảnh/chữ đề gốc) + đường giải (đã kiểm bằng toạ độ ở
hinh_phieu_h_ch9_9c.py). Gemini chỉ viết chữ. Hình do lap_phieu_h_ch9_9c.py chèn.

    python3 scripts/gemini/viec_phieu_h_ch9_9c.py
    python3 scripts/gemini/tho.py --mot dung-9c-ch9-phieu-h
    python3 scripts/gemini/lap_phieu_h_ch9_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VID = "dung-9c-ch9-phieu-h"

PROMPT = r'''Bạn là thợ soạn phiếu học tập Toán 9 (HÌNH HỌC — chương IX "Đường tròn ngoại tiếp và đường tròn nội tiếp", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu), buổi 90 phút luyện CHỨNG MINH HỆ THỨC TÍCH bằng hai tam giác đồng dạng, trong đó các cặp góc bằng nhau lấy từ góc nội tiếp (góc nội tiếp chắn nửa đường tròn là góc vuông, hai góc nội tiếp cùng chắn một cung). KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt. Đầu ra là JSON đúng schema {"stages":[…5 chặng…],"ghi_chu":"…"}.

## Học sinh đã học gì (KHÔNG dùng gì ngoài danh sách này)
- Bài 27 Góc nội tiếp (SGK Toán 9 tập hai tr.68–70): định nghĩa, định lí, Nhận xét (cùng chắn một cung thì bằng nhau; chắn nửa đường tròn là góc vuông).
- Bài 28 (tr.73): đường tròn ngoại tiếp tam giác vuông có tâm là trung điểm cạnh huyền ⇒ đỉnh góc vuông thuộc đường tròn đường kính là cạnh huyền. Bài 29: tứ giác nội tiếp = bốn đỉnh cùng thuộc một đường tròn.
- Lớp 8 (SGK Toán 8 tập hai): định nghĩa hai tam giác đồng dạng (tr.79): "Tam giác $A'B'C'$ gọi là đồng dạng với tam giác $ABC$ nếu $\dfrac{A'B'}{AB} = \dfrac{B'C'}{BC} = \dfrac{C'A'}{CA}$ và $\widehat{A'} = \widehat{A}$, $\widehat{B'} = \widehat{B}$, $\widehat{C'} = \widehat{C}$."; Định lí (trường hợp đồng dạng góc – góc) tr.88: "Nếu hai góc của tam giác này lần lượt bằng hai góc của tam giác kia thì hai tam giác đó đồng dạng với nhau."; Bài 36 Định lí 1 tr.98: "Nếu một góc nhọn của tam giác vuông này bằng một góc nhọn của tam giác vuông kia thì hai tam giác vuông đó đồng dạng với nhau."
- Lớp 7 (SGK Toán 7 tập một, Bài 10, Nhận xét tr.53): "Một đường thẳng vuông góc với một trong hai đường thẳng song song thì nó cũng vuông góc với đường thẳng kia." Góc đối đỉnh, hai góc kề bù. Chương V lớp 9: tam giác cân có đường trung tuyến đồng thời là đường cao.
- CẤM: góc tạo bởi tia tiếp tuyến và dây cung; hệ thức lượng trong tam giác vuông dạng $AB^2 = BH \cdot BC$ dùng thẳng (phải đi qua đồng dạng); dấu hiệu "tổng hai góc đối bằng $180^\circ$ thì nội tiếp"; đồng dạng gián tiếp qua đoạn thứ ba. Chứng minh bốn điểm cùng thuộc một đường tròn CHỈ bằng: "$\triangle \ldots$ vuông tại $X$ ⇒ $X$ thuộc đường tròn đường kính …" cho từng điểm, rồi "Vậy …".

## Luật cứng (vi phạm bị trả lại)
- Nhịp lời giải như bài thi: mỗi bước MỘT dòng ([[br]]), mỗi dòng tối đa MỘT dấu $\Rightarrow$, câu "Vậy …" dòng riêng ở cuối mỗi ý. Mỗi dấu $\Rightarrow$ có căn cứ ngắn trong ngoặc. Khi dùng hai góc nội tiếp cùng chắn một cung PHẢI nêu rõ đường tròn: "Xét đường tròn $(O)$: …" hoặc "Xét đường tròn đường kính $AD$: …".
- Trình bày đồng dạng đúng khuôn: "Xét $\triangle ABD$ và $\triangle AKC$ có:[[br]]$\widehat{ADB} = \widehat{ACK} = 90^\circ$ (…)[[br]]$\widehat{ABD} = \widehat{AKC}$ (…)[[br]]$\Rightarrow \triangle ABD \backsim \triangle AKC$ (g.g)[[br]]$\Rightarrow \dfrac{AB}{AK} = \dfrac{AD}{AC}$ (các cạnh tương ứng tỉ lệ)[[br]]Vậy $AB \cdot AC = AK \cdot AD$." Viết hai tam giác ĐÚNG thứ tự đỉnh tương ứng như đường giải đã cho. Kí hiệu đồng dạng là \backsim, phân số trong lời giải dùng \dfrac.
- Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác", "Ta thấy". Không dấu chấm phẩy ";". Không chữ "khuôn", "Câu IV", "đề thi có", "thang điểm", "bóc tách", "vừa sức", "trọn bộ", "mẹo". Không xưng hô ("em", "các em", "ta cùng", "hôm nay", "ở lớp") trong đề và lời giải.
- Đề ghi ĐẦY ĐỦ giả thiết như mục "Đề và đường giải" (chép nguyên văn, chỉ đổi kí hiệu sang LaTeX). Toán trong $…$, góc $\widehat{ABC}$, độ $90^\circ$, tam giác $\triangle ABC$, vuông góc $\perp$, song song $\parallel$, tích $AB \cdot AC$.
- Thẻ mức đặt ở ĐẦU MỖI Ý kèm sao: "a) [NB] ★ …", "b) [TH] ★★ …", "[VD] ★★★ …". Bài trắc nghiệm một câu: "[NB] " đứng đầu statement.
- Ví dụ (noted variant "example"): đề → dòng "{\sffamily\bfseries\color{brand}Lời giải}" → lời giải từng dòng → "Vậy …". Khoét ít nhất 6 ô bằng [[fill:đáp án]] ở chỗ then chốt (góc $90^\circ$, căn cứ "góc nội tiếp chắn nửa đường tròn", "hai góc nội tiếp cùng chắn một cung", tên tam giác đồng dạng, tỉ số, kết luận). Ô nằm TRONG $…$ thì đáp án KHÔNG bọc $ ("$\widehat{IMK} = [[fill:90^\circ]]$", "$\triangle IMK \backsim \triangle [[fill:INC]]$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong ô ("[[fill:$\widehat{DAC}$]]"). Câu "Vậy …" PHẢI có ít nhất một ô [[fill:…]]. Không để dòng dưới in sẵn đáp án của ô dòng trên. Câu đề ví dụ có thêm "Vẽ tiếp vào Hình N các yếu tố còn thiếu theo đề." ngay sau giả thiết.
- Khung điền khuyết trong ĐỀ bài (Bài 2, Bài 3) dùng [[blank:1.1cm]] (một kí hiệu, số đo, tên đoạn), [[blank:2.4cm]] (tên tam giác, tên góc, biểu thức), [[blank:3.2cm]] (cụm từ). Câu dẫn có cụm "hoàn thành bài giải". Mỗi dòng khung tối đa một $\Rightarrow$, dòng "Vậy …" riêng. Ô trống rơi vào từ khoá cần nhớ hoặc chỗ phải suy ra, ít nhất 6 ô cho mỗi 10 dòng. Không khoét ô mà đáp án đã in ở đề ý đó hoặc dòng dưới. Trong khung KHÔNG viết lại nhãn "a)", "b)" lần hai (nhãn ý chỉ có ở dòng đề ý có thẻ).
- Bài HS tự trình bày: "answer" là lời giải đầy đủ. Bài mức TH, VD có "hints" 1–2 câu HỎI kiểu Polya (đổi tích thành tỉ số thì được những đoạn nào? hai đoạn ở vế trái nằm trong tam giác nào? góc vuông có từ đâu? hai góc nào cùng chắn một cung?) — không gọi tên công cụ, không lộ đáp án.
- Bài khung điền: "answer" = đáp án từng ô theo thứ tự, ngăn bằng dấu phẩy (không dùng ";"). Thêm "statement_slide": đề rút gọn không khung (giả thiết + các ý có thẻ).
- Trắc nghiệm: "options" 4 chuỗi (không ghi A./B.), "answer" một chữ cái. Chép đúng 4 phương án đã cho theo đúng thứ tự.
- JSON hợp lệ: mọi gạch chéo ngược nhân đôi trong chuỗi. Không viết TikZ: ở khối cần hình đặt "figure": "<khoá>" (khoá cho sẵn). Escape "\&" trong "GD\&ĐT", "THCS\&THPT".
- Tự kiểm tra từng dấu $\Rightarrow$ truy ngược về giả thiết, điều đã chứng minh, định lí đã học. Điều đọc từ hình (điểm nằm giữa, thuộc đoạn) ghi "(Hình N)". Nghi ngờ gì ghi vào "ghi_chu".

## Khuôn khối JSON (theo phiếu mẫu đã duyệt)
- Thẻ lý thuyết: {"type":"noted","variant":"theory","title":"1. GÓC NỘI TIẾP","text":"\\nhanly{Định nghĩa.} …[[br]]…","figure":"lt1"}
- Hộp lỗi hay gặp: {"type":"noted","variant":"trap","text":"- …[[br]]- …"}
- Tiêu đề phần: {"type":"para","variant":"part","text":"A. Lý thuyết"}
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"}
- Đoạn đích: {"type":"para","text":"\\textbf{Đích của buổi học:} …"}
- Ví dụ: {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} …","figure":"Ví dụ 1."}
- Bài: {"type":"problem","label":"Bài 2.","statement":"…","answer":"…","hints":[…],"figure":"Bài 2."} (trắc nghiệm thêm "options"; khung thêm "statement_slide"; bài đích thêm "quy_trinh": [4 chuỗi]).
- Sơ đồ tư duy: {"type":"mindmap","caption":"Sơ đồ tư duy: …","root":"…","branches":[{"label":"…","children":[{"label":"…"}]}]} (3 nhánh, mỗi nhánh 2 lá, chữ ngắn).
- Khám phá: {"type":"para","text":"\\textbf{<câu hỏi mở>}"} + {"type":"noted","variant":"note","text":"…","figure":"Hình 1"}

## Năm chặng (đúng thứ tự, đúng "kind", "number", "title")
1. {"kind":"review","number":1,"title":"Khám phá"} — para câu hỏi mở: "\textbf{Hai dây cung cắt nhau thì các đoạn thẳng có liên hệ gì?}" + note: chép đề SGK Toán 9 tập hai, Bài 27, Luyện tập (tr.70): "Cho đường tròn tâm $O$ và hai dây cung $AB$, $CD$ cắt nhau tại điểm $X$ nằm trong đường tròn (Hình 1). Chứng minh rằng $\triangle AXC \backsim \triangle DXB$." rồi chia câu hỏi \textbf{a)} Hai góc nội tiếp $\widehat{CAB}$ và $\widehat{CDB}$ cùng chắn cung nào? \textbf{b)} Hai góc $\widehat{AXC}$ và $\widehat{DXB}$ là hai góc gì? \textbf{c)} Từ $\triangle AXC \backsim \triangle DXB$, viết tỉ số các cạnh tương ứng rồi chứng tỏ $XA \cdot XB = XC \cdot XD$. Nguồn cuối: "(SGK Toán 9 tập hai, Bài 27, Luyện tập tr.70 và Bài tập 9.4)". teacher_note ~5 phút hỏi đáp miệng: cùng chắn cung $CB$, đối đỉnh, $\dfrac{XA}{XD} = \dfrac{XC}{XB}$.
2. {"kind":"concept","number":2,"title":"Kiến thức cần nhớ"} — khối theo thứ tự:
   para part "A. Lý thuyết" ·
   theory "1. GÓC NỘI TIẾP" (figure "lt1") — chép NGUYÊN VĂN khối này: "\nhanly{Định nghĩa.} Góc nội tiếp là góc có đỉnh nằm trên đường tròn và hai cạnh chứa hai dây cung của đường tròn đó. Cung nằm bên trong góc được gọi là cung bị chắn.[[br]]\nhanly{Định lí.} Trong một đường tròn, số đo của góc nội tiếp bằng nửa số đo của cung bị chắn.[[br]]\nhanly{Nhận xét.} Đối với các góc nội tiếp của một đường tròn:[[br]]- Các góc nội tiếp bằng nhau chắn các cung bằng nhau.[[br]]- Các góc nội tiếp cùng chắn một cung hoặc chắn các cung bằng nhau thì bằng nhau.[[br]]- Các góc nội tiếp chắn cung nhỏ thì có số đo bằng nửa số đo của góc ở tâm chắn cùng một cung.[[br]]- Góc nội tiếp chắn nửa đường tròn là góc vuông.[[br]](SGK Toán 9 tập hai, tr.68--69)" ·
   theory "2. HAI TAM GIÁC ĐỒNG DẠNG" (không hình): định nghĩa (tr.79), Định lí góc – góc (tr.88), Định lí 1 tam giác vuông (tr.98) — đúng chữ ở mục "Học sinh đã học gì", ghi nguồn "(SGK Toán 8 tập hai, tr.79, tr.88, tr.98)". Thêm một dòng: "Từ tỉ số ra tích: $\dfrac{a}{b} = \dfrac{c}{d} \Rightarrow a \cdot d = b \cdot c$." ·
   para part "B. Phương pháp chứng minh — các dạng quen thuộc" ·
   theory "DẠNG. CHỨNG MINH HỆ THỨC TÍCH BẰNG HAI TAM GIÁC ĐỒNG DẠNG" (không hình): \nhanly{Bước 1 (nháp):} đổi tích thành tỉ số, đọc ra hai tam giác chứa các đoạn thẳng. \nhanly{Bước 2:} tìm hai cặp góc bằng nhau: góc chung hoặc đối đỉnh · góc vuông (đường cao, đường vuông góc, góc nội tiếp chắn nửa đường tròn) · hai góc nội tiếp cùng chắn một cung (nêu rõ đường tròn). \nhanly{Bước 3:} kết luận hai tam giác đồng dạng (g.g), viết tỉ số các cạnh tương ứng rồi nhân chéo. Thêm "Trình bày: mỗi cặp góc một dòng kèm căn cứ, viết hai tam giác đúng thứ tự đỉnh tương ứng." KHÔNG đưa ví dụ cụ thể vào thẻ. ·
   trap: 3 lỗi hay gặp: viết sai thứ tự đỉnh hai tam giác đồng dạng nên lập sai tỉ số · thấy đường kính mà quên góc nội tiếp chắn nửa đường tròn bằng $90^\circ$ · viết "cùng chắn cung" mà không nêu đường tròn nào.
   teacher_note: giảng ~10 phút, đọc lý thuyết đúng chữ SGK, nhấn Bước 1 làm ở nháp.
3. {"kind":"practice1","number":3,"title":"Luyện tập 1"} — khối theo thứ tự:
   para đích: "\textbf{Đích của buổi học:} Bài 4 (Đề thi thử vào 10 lần 5 THCS Thọ Lộc, Hà Nội, 2025--2026): ý a chứng minh bốn điểm cùng thuộc một đường tròn bằng hai góc vuông, ý b chứng minh hệ thức tích bằng hai tam giác đồng dạng có một cặp góc nội tiếp cùng chắn một cung (Mạch 2). Mạch 1 luyện đổi tích thành tỉ số, chọn hai tam giác có góc chung và góc vuông."
   heading "Mạch 1. Góc chung và góc vuông" · Bài 1. · Ví dụ 1. · Bài 2.
   heading "Mạch 2. Hai góc nội tiếp cùng chắn một cung" · Ví dụ 2. · Bài 3.
   teacher_note (kịch bản phút lớp C): Bài 1 ~3′ · Ví dụ 1 GV vẽ cùng HS rồi điền ô ~12′ · Bài 2 vẽ tiếp $BD$, $CE$ rồi điền khung ~12′ · Ví dụ 2 ~12′ · Bài 3 vẽ tiếp rồi điền khung ~14′.
4. {"kind":"practice2","number":4,"title":"Luyện tập 2"} — para heading "Đề thi thử vào 10 lần 5 — THCS Thọ Lộc (Hà Nội) 2025--2026" · Bài 4. (bài đích, HS tự vẽ hình, tự trình bày, có hints + quy_trinh 4 bước).
   teacher_note: ~28′: vẽ hình ~5′, ý a ~10′, ý b ~13′ (như Bài 3 ý b). GV chấm ý a trước.
5. {"kind":"reflection","number":5,"title":"Sơ đồ tư duy"} — mindmap (root "HỆ THỨC TÍCH BẰNG ĐỒNG DẠNG", nhánh "ĐỔI TÍCH THÀNH TỈ SỐ" (tích thành tỉ số / đọc ra hai tam giác), "TÌM HAI CẶP GÓC" (góc chung, góc vuông / cùng chắn một cung), "KẾT LUẬN" (đồng dạng g.g / tỉ số rồi nhân chéo)) rồi NGAY SAU là BTVN 1. … BTVN 4. (KHÔNG đặt tiêu đề/para trước BTVN 1).
   teacher_note: BTVN ~55′ (dày hơn quỹ 40′): BTVN 1 ~10′, BTVN 2 ~15′, BTVN 3 ~12′, BTVN 4 ~18′ (gồm vẽ hình). BTVN 1, 2, 3 đi cùng Mạch 1, BTVN 4 đi cùng Mạch 2.

## Đề và đường giải (Claude đã soi đề gốc và kiểm bằng toạ độ — dùng đúng, không đổi)

### Bài 1. (trắc nghiệm, hình "Bài 1." = Hình 2 in sẵn đủ)
statement: "[NB] Cho tam giác $ABC$ có ba góc nhọn nội tiếp đường tròn tâm $O$ bán kính $R$ và $AH$ là đường cao của tam giác $ABC$. Gọi $M$, $N$ lần lượt là chân đường vuông góc kẻ từ $H$ đến $AB$ và $AC$ (Hình 2). Để chứng minh $AH^2 = AM \cdot AB$, cần chứng minh hai tam giác nào đồng dạng? \;(Tách từ đề học kì II THCS Ngọc Thụy, 2024--2025)"
options ["$\triangle AMH \backsim \triangle ANH$","$\triangle AHB \backsim \triangle AHC$","$\triangle AMH \backsim \triangle AHB$","$\triangle MHB \backsim \triangle NHC$"]  answer "C". answer có thể kèm giải thích ngắn trong "solution": $\dfrac{AH}{AB} = \dfrac{AM}{AH}$.

### Ví dụ 1. (Đề giữa học kì II Ban Mai School, Hà Nội, 2024–2025, Bài 4 ý a, b) — hình "Ví dụ 1." = Hình 3 (HS chỉ thấy đường tròn $(O)$, dây $AB$)
Đề: "Cho đường tròn $(O)$ có dây cung $AB$ cố định ($AB$ không phải là đường kính). Kẻ đường kính $IK$ vuông góc với $AB$ tại $N$ sao cho điểm $I$ thuộc cung lớn $AB$. Lấy điểm $M$ bất kỳ trên cung lớn $AB$, kẻ $MK$ cắt $AB$ tại $D$. Hai đường thẳng $IM$ và $AB$ cắt nhau tại $C$ (Hình 3)." + câu vẽ tiếp + "a) [NB] ★ Chứng minh tứ giác $INDM$ là tứ giác nội tiếp.[[br]]b) [TH] ★★ Chứng minh $IM \cdot IC = IN \cdot IK$."
Đường giải: a) $\widehat{IMK} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$, $IK$ là đường kính) ⇒ $\widehat{IMD} = 90^\circ$ ($D$ thuộc đoạn $MK$) ⇒ $\triangle IMD$ vuông tại $M$ ⇒ $M$ thuộc đường tròn đường kính $ID$. $IK \perp AB$ tại $N$ (giả thiết) ⇒ $\triangle IND$ vuông tại $N$ ⇒ $N$ thuộc đường tròn đường kính $ID$. ⇒ $I, N, D, M$ cùng thuộc đường tròn đường kính $ID$. Vậy tứ giác $INDM$ nội tiếp.
b) Xét $\triangle IMK$ và $\triangle INC$ có: $\widehat{I}$ chung · $\widehat{IMK} = \widehat{INC} = 90^\circ$ (câu a và $IK \perp AB$ tại $N$) ⇒ $\triangle IMK \backsim \triangle INC$ (g.g) ⇒ $\dfrac{IM}{IN} = \dfrac{IK}{IC}$ ⇒ Vậy $IM \cdot IC = IN \cdot IK$.

### Bài 2. (Đề kiểm tra cuối kỳ II Phòng GD\&ĐT Gia Lâm, 2024–2025, Bài IV.2 ý a và phần đầu ý b) — hình "Bài 2." = Hình 4 (HS thấy $\triangle ABC$, đường tròn $(O)$ đường kính $BC$, $E$, $D$)
Đề: "Cho tam giác $ABC$ nhọn. Đường tròn $(O)$ đường kính $BC$ cắt $AB$, $AC$ lần lượt tại $E$ và $D$. $BD$ cắt $CE$ tại $H$ (Hình 4)." + "Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề rồi điền vào chỗ chấm để hoàn thành bài giải:" + "a) [NB] ★ Chứng minh tứ giác $AEHD$ nội tiếp, chỉ rõ vị trí tâm đường tròn." (khung 6 dòng) + "b) [TH] ★★ Chứng minh $AB \cdot AE = AC \cdot AD$." (khung 6 dòng).
Đường giải: a) $\widehat{BEC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$) ⇒ $\widehat{AEH} = 90^\circ$ (kề bù, $H$ thuộc $CE$) ⇒ $E$ thuộc đường tròn đường kính $AH$. $\widehat{BDC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$) ⇒ $\widehat{ADH} = 90^\circ$ ⇒ $D$ thuộc đường tròn đường kính $AH$. Vậy tứ giác $AEHD$ nội tiếp đường tròn đường kính $AH$, tâm là trung điểm của $AH$.
b) $\widehat{ADB} = 90^\circ$, $\widehat{AEC} = 90^\circ$ (câu a). Xét $\triangle ABD$ và $\triangle ACE$ có: $\widehat{A}$ chung · $\widehat{ADB} = \widehat{AEC} = 90^\circ$ ⇒ $\triangle ABD \backsim \triangle ACE$ (g.g) ⇒ $\dfrac{AB}{AC} = \dfrac{AD}{AE}$ ⇒ Vậy $AB \cdot AE = AC \cdot AD$.

### Ví dụ 2. (Đề kiểm tra học kì II Phòng GD\&ĐT Cầu Giấy, 2024–2025, Câu IV.2 phần sau ý b) — hình "Ví dụ 2." = Hình 5 (HS thấy $\triangle ABC$ và đường cao $AD$)
Đề: "Cho tam giác nhọn $ABC$ ($AB < AC$) có đường cao $AD$. Gọi $N$, $T$ lần lượt là chân đường vuông góc kẻ từ $D$ đến $AB$, $AC$. Đường thẳng qua $D$ song song với $AB$ cắt $NT$ tại $E$. Biết bốn điểm $A, N, D, T$ cùng thuộc đường tròn đường kính $AD$ (Hình 5)." + câu vẽ tiếp + "[VD] ★★★ Chứng minh $DN \cdot DC = DE \cdot DA$."
Đường giải: Xét đường tròn đường kính $AD$: $\widehat{DNT} = \widehat{DAT}$ (hai góc nội tiếp cùng chắn cung $DT$). $E$ thuộc đoạn $NT$, $T$ thuộc cạnh $AC$ (Hình 5) ⇒ $\widehat{DNE} = \widehat{DAC}$. $DN \perp AB$, $DE \parallel AB$ ⇒ $DN \perp DE$ (một đường thẳng vuông góc với một trong hai đường thẳng song song thì vuông góc với đường thẳng kia) ⇒ $\widehat{NDE} = 90^\circ$. $AD \perp BC$ ⇒ $\widehat{ADC} = 90^\circ$. Xét $\triangle DNE$ và $\triangle DAC$ có: $\widehat{NDE} = \widehat{ADC} = 90^\circ$ · $\widehat{DNE} = \widehat{DAC}$ ⇒ $\triangle DNE \backsim \triangle DAC$ (g.g) ⇒ $\dfrac{DN}{DA} = \dfrac{DE}{DC}$ ⇒ Vậy $DN \cdot DC = DE \cdot DA$.

### Bài 3. (Đề kiểm tra cuối học kì II THCS Thăng Long, Hà Nội, 2025–2026, Câu IV.2 ý a và phần đầu ý b) — hình "Bài 3." = Hình 6 (HS thấy đường tròn $(O)$, dây $BC$)
Đề: "Cho đường tròn $(O; R)$ và dây $BC$ cố định không đi qua tâm $O$. Gọi $A$ là một điểm bất kì trên cung lớn $BC$ ($A$ khác $B$ và $C$) sao cho tam giác $ABC$ nhọn ($AB < AC$). Kẻ các đường cao $AD$, $BE$ của tam giác $ABC$ (Hình 6)." + "Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề rồi điền vào chỗ chấm để hoàn thành bài giải:" + "a) [NB] ★ Chứng minh tứ giác $AEDB$ nội tiếp đường tròn." (khung 5 dòng) + "b) [TH] ★★ Kẻ đường kính $AK$ của đường tròn tâm $O$. Chứng minh $AB \cdot AC = AK \cdot AD$." (khung 7 dòng, có dòng "Nối $CK$.").
Đường giải: a) $BE \perp AC$ tại $E$ ⇒ $\triangle AEB$ vuông tại $E$ ⇒ $E$ thuộc đường tròn đường kính $AB$. $AD \perp BC$ tại $D$ ⇒ $\triangle ADB$ vuông tại $D$ ⇒ $D$ thuộc đường tròn đường kính $AB$. Vậy tứ giác $AEDB$ nội tiếp đường tròn đường kính $AB$.
b) Nối $CK$. $\widehat{ACK} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$). Xét đường tròn $(O)$: $\widehat{ABC} = \widehat{AKC}$ (hai góc nội tiếp cùng chắn cung $AC$). Xét $\triangle ABD$ và $\triangle AKC$ có: $\widehat{ADB} = \widehat{ACK} = 90^\circ$ · $\widehat{ABD} = \widehat{AKC}$ ⇒ $\triangle ABD \backsim \triangle AKC$ (g.g) ⇒ $\dfrac{AB}{AK} = \dfrac{AD}{AC}$ ⇒ Vậy $AB \cdot AC = AK \cdot AD$.

### Bài 4. (bài đích — Đề thi thử vào 10 lần 5 THCS Thọ Lộc, Hà Nội, 2025–2026, Bài IV.2 ý a và phần đầu ý b) — hình "Bài 4." = Hình 7 (nền: đường tròn, dây $BC$; HS tự vẽ tiếp)
statement: "Cho đường tròn tâm $(O)$ và dây $BC$ cố định không đi qua $O$. Trên cung lớn $BC$ lấy điểm $A$ sao cho $AB < AC$. Kẻ đường kính $AK$, qua $C$ kẻ đường thẳng vuông góc với $AK$ tại $E$, gọi $M$ là trung điểm của $BC$ (Hình 7).[[br]]a) [TH] ★★ Chứng minh bốn điểm $C, E, M, O$ cùng thuộc một đường tròn.[[br]]b) [VD] ★★★ Kẻ $AD$ vuông góc với $BC$ tại $D$. Chứng minh $AD \cdot AK = AB \cdot AC$."
Đường giải: a) $CE \perp AK$ tại $E$, $O$ thuộc $AK$ ⇒ $\triangle OEC$ vuông tại $E$ ⇒ $E$ thuộc đường tròn đường kính $OC$. $OB = OC$ (bán kính) ⇒ $\triangle OBC$ cân tại $O$. $OM$ là đường trung tuyến ($M$ là trung điểm của $BC$) ⇒ $OM$ đồng thời là đường cao ⇒ $OM \perp BC$ ⇒ $\triangle OMC$ vuông tại $M$ ⇒ $M$ thuộc đường tròn đường kính $OC$. Vậy bốn điểm $C, E, M, O$ cùng thuộc đường tròn đường kính $OC$.
b) Nối $CK$. $\widehat{ACK} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$). Xét đường tròn $(O)$: $\widehat{ABC} = \widehat{AKC}$ (hai góc nội tiếp cùng chắn cung $AC$). $D$ thuộc đoạn $BC$ (Hình 7) ⇒ $\widehat{ABD} = \widehat{AKC}$. Xét $\triangle ABD$ và $\triangle AKC$ có: $\widehat{ADB} = \widehat{ACK} = 90^\circ$ · $\widehat{ABD} = \widehat{AKC}$ ⇒ $\triangle ABD \backsim \triangle AKC$ (g.g) ⇒ $\dfrac{AD}{AC} = \dfrac{AB}{AK}$ ⇒ Vậy $AD \cdot AK = AB \cdot AC$.
quy_trinh: (1) vẽ hình: đường tròn, dây $BC$, điểm $A$, đường kính $AK$, $CE \perp AK$, trung điểm $M$, đường cao $AD$, nối $CK$ · (2) ý a: hai góc vuông cùng nhìn $OC$ (như Bài 3 ý a) · (3) ý b: đổi tích thành tỉ số, chọn $\triangle ABD$ và $\triangle AKC$ · (4) hai cặp góc: góc vuông và hai góc nội tiếp cùng chắn cung $AC$ (như Bài 3 ý b). hints 2 câu hỏi.

### BTVN 1. (Đề kiểm tra cuối học kì II THCS\&THPT M.V. Lômônôxốp, 2024–2025, Bài IV.2 phần đầu ý b) — HS tự vẽ (hình "BTVN 1." = Hình 8 nền: đường tròn và tam giác)
statement: "Cho tam giác $ABC$ nhọn ($AB < AC$) nội tiếp đường tròn $(O)$. Hai đường cao $BE$ và $CF$ của tam giác $ABC$ cắt nhau tại điểm $H$ (Hình 8).[[br]][TH] ★★ Chứng minh $AE \cdot AC = AF \cdot AB$."
Đường giải: Xét $\triangle AEB$ và $\triangle AFC$ có: $\widehat{A}$ chung · $\widehat{AEB} = \widehat{AFC} = 90^\circ$ ($BE \perp AC$, $CF \perp AB$) ⇒ $\triangle AEB \backsim \triangle AFC$ (g.g) ⇒ $\dfrac{AE}{AF} = \dfrac{AB}{AC}$ ⇒ Vậy $AE \cdot AC = AF \cdot AB$. hints 2.

### BTVN 2. (Đề giữa học kì II THCS Mai Dịch, Hà Nội, 2024–2025, Bài 4.2 ý a và phần sau ý b) — HS tự vẽ (hình "BTVN 2." = Hình 9 nền: nửa đường tròn)
statement: "Cho nửa đường tròn $(O)$, đường kính $AB$. Trên nửa đường tròn $(O)$ lấy điểm $C$ (khác $A$ và $B$). Trên cung $CB$ của nửa đường tròn $(O)$ lấy điểm $D$ ($D$ khác $C$ và $B$). Kẻ $CH \perp AB$ tại $H$, $CK \perp AD$ tại $K$. Gọi $I$ là giao điểm của hai đoạn thẳng $AD$ và $CH$ (Hình 9).[[br]]a) [TH] ★★ Chứng minh $AHKC$ là tứ giác nội tiếp.[[br]]b) [TH] ★★ Chứng minh $AI \cdot AD = AH \cdot AB$."
Đường giải: a) $CH \perp AB$ tại $H$ ⇒ $\triangle AHC$ vuông tại $H$ ⇒ $H$ thuộc đường tròn đường kính $AC$. $CK \perp AD$ tại $K$ ⇒ $\triangle AKC$ vuông tại $K$ ⇒ $K$ thuộc đường tròn đường kính $AC$. Vậy $AHKC$ là tứ giác nội tiếp đường tròn đường kính $AC$.
b) $\widehat{ADB} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$). Xét $\triangle AHI$ và $\triangle ADB$ có: $\widehat{A}$ chung · $\widehat{AHI} = \widehat{ADB} = 90^\circ$ ⇒ $\triangle AHI \backsim \triangle ADB$ (g.g) ⇒ $\dfrac{AH}{AD} = \dfrac{AI}{AB}$ ⇒ Vậy $AI \cdot AD = AH \cdot AB$. hints 2.

### BTVN 3. (Đề kiểm tra cuối học kỳ II THCS Hát Môn, Hà Nội, 2025–2026, Bài IV.2 ý b) — HS tự vẽ (hình "BTVN 3." = Hình 10 nền: tam giác vuông)
statement: "Cho tam giác $ABC$ vuông tại $A$. Lấy điểm $M$ bất kì trên đoạn $AC$, đường tròn đường kính $CM$ cắt hai đường thẳng $BM$, $BC$ lần lượt tại $D$, $N$ (Hình 10).[[br]][TH] ★★ Chứng minh $BM \cdot BD = BN \cdot BC$."
Đường giải: $\widehat{MNC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn đường kính $CM$) ⇒ $\widehat{BNM} = 90^\circ$ ($N$ thuộc đoạn $BC$, Hình 10). $\widehat{MDC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn đường kính $CM$) ⇒ $\widehat{BDC} = 90^\circ$. Xét $\triangle BNM$ và $\triangle BDC$ có: $\widehat{B}$ chung · $\widehat{BNM} = \widehat{BDC} = 90^\circ$ ⇒ $\triangle BNM \backsim \triangle BDC$ (g.g) ⇒ $\dfrac{BN}{BD} = \dfrac{BM}{BC}$ ⇒ Vậy $BM \cdot BD = BN \cdot BC$. hints 2.

### BTVN 4. (Đề thi thử vào 10 lần 1 THPT Sơn Tây, 2024–2025, Bài IV phần sau ý 2) — HS tự vẽ (hình "BTVN 4." = Hình 11 nền: đường tròn và tam giác)
statement: "Cho tam giác $ABC$ ($AB > AC$) nội tiếp đường tròn tâm $O$. Gọi $M$ là trung điểm của đoạn thẳng $BC$. Gọi $E$, $F$ lần lượt là chân đường vuông góc kẻ từ $M$ đến các đường thẳng $AB$, $AC$. Đường thẳng $AM$ cắt đường tròn $(O)$ tại điểm thứ hai là $K$. Biết bốn điểm $A, E, M, F$ cùng thuộc đường tròn đường kính $AM$ và $\widehat{KBC} = \widehat{MEF}$ (Hình 11).[[br]][VD] ★★★ Chứng minh $BC \cdot ME = EF \cdot BK$."
Đường giải: Xét đường tròn $(O)$: $\widehat{BCK} = \widehat{BAK}$ (hai góc nội tiếp cùng chắn cung $BK$). $E$ thuộc đoạn $AB$, $M$ thuộc đoạn $AK$ (Hình 11) ⇒ $\widehat{BAK} = \widehat{EAM}$. Xét đường tròn đường kính $AM$: $\widehat{EAM} = \widehat{EFM}$ (hai góc nội tiếp cùng chắn cung $EM$). ⇒ $\widehat{BCK} = \widehat{EFM}$. Xét $\triangle BKC$ và $\triangle EMF$ có: $\widehat{KBC} = \widehat{MEF}$ (giả thiết) · $\widehat{BCK} = \widehat{EFM}$ ⇒ $\triangle BKC \backsim \triangle EMF$ (g.g) ⇒ $\dfrac{BC}{EF} = \dfrac{BK}{EM}$ ⇒ Vậy $BC \cdot ME = EF \cdot BK$. hints 2 (gợi ý: hai đoạn $BC$, $BK$ nằm trong tam giác nào? góc nào đứng giữa $\widehat{BCK}$ và $\widehat{EFM}$?).

## Đầu ra
JSON {"stages":[5 chặng],"ghi_chu":"…"}. Không thêm bài nào ngoài danh sách. Trong "ghi_chu" liệt kê mọi chỗ nghi ngờ.
'''


def main():
    v = {"id": VID, "model": "gemini-4-hydrogen-medium", "prompt": PROMPT, "files": [],
         "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1800s",
         "meta": {"loai": "dung-chang-phieu", "seed": "phieu-h ch.IX 9C"}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(PROMPT) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
