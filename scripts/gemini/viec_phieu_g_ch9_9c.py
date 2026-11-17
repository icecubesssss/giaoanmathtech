#!/usr/bin/env python3
"""Việc Gemini: dựng chữ phiếu G ch.IX 9C — buổi 9.6 (t28, 27/12/2026, ca 90′)
"Góc nội tiếp cùng chắn một cung — chứng minh hai góc bằng nhau" (Câu IV.2 ý b, phần góc).

Claude chốt sơ đồ + đề (đã soi ảnh đề gốc) + đường giải (đã kiểm bằng toạ độ ở
hinh_phieu_g_ch9_9c.py). Gemini chỉ viết chữ: đề, lời giải, ví dụ điền khuyết, gợi ý, ghi chú GV.
Hình do lap_phieu_g_ch9_9c.py chèn (thợ KHÔNG viết TikZ).

    python3 scripts/gemini/viec_phieu_g_ch9_9c.py
    python3 scripts/gemini/tho.py --mot dung-9c-ch9-phieu-g
    python3 scripts/gemini/lap_phieu_g_ch9_9c.py [--ghi]
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VID = "dung-9c-ch9-phieu-g"

PROMPT = r'''Bạn là thợ soạn phiếu học tập Toán 9 (HÌNH HỌC — chương IX "Đường tròn ngoại tiếp và đường tròn nội tiếp", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu), buổi 90 phút chỉ luyện GÓC NỘI TIẾP CÙNG CHẮN MỘT CUNG để chứng minh hai góc bằng nhau. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt. Đầu ra là JSON đúng schema {"stages":[…5 chặng…],"ghi_chu":"…"}.

## Học sinh đã học gì (KHÔNG dùng gì ngoài danh sách này)
- Bài 27 Góc nội tiếp (SGK tập hai tr.68–69): định nghĩa, định lí "số đo góc nội tiếp bằng nửa số đo cung bị chắn", Nhận xét: các góc nội tiếp cùng chắn một cung hoặc chắn các cung bằng nhau thì bằng nhau; góc nội tiếp chắn nửa đường tròn là góc vuông.
- Bài 28 (tr.73): đường tròn ngoại tiếp tam giác vuông có tâm là trung điểm cạnh huyền ⇒ đỉnh góc vuông thuộc đường tròn đường kính là cạnh huyền.
- Bài 29: tứ giác nội tiếp (bốn đỉnh cùng thuộc một đường tròn), tổng hai góc đối bằng $180^\circ$.
- Chương V: tiếp tuyến vuông góc với bán kính tại tiếp điểm. Lớp 7: tổng ba góc của tam giác bằng $180^\circ$, tam giác cân, tia phân giác.
- CẤM: góc tạo bởi tia tiếp tuyến và dây cung; tam giác đồng dạng; hệ thức tích (để dành buổi sau); "dấu hiệu nhận biết tứ giác nội tiếp" dạng tổng hai góc đối bằng $180^\circ$ thì nội tiếp (KHÔNG dùng chiều ngược này). Chứng minh bốn điểm cùng thuộc một đường tròn CHỈ bằng một cách: "$\triangle \ldots$ vuông tại $X$ ⇒ $X$ thuộc đường tròn đường kính …" cho từng điểm, rồi "Vậy bốn điểm … cùng thuộc đường tròn đường kính …".

## Luật cứng (vi phạm bị trả lại)
- Nhịp lời giải như bài thi: mỗi bước MỘT dòng ([[br]]), mỗi dòng tối đa MỘT dấu $\Rightarrow$, câu "Vậy …" dòng riêng ở cuối mỗi ý. Mỗi dấu $\Rightarrow$ phải có căn cứ ngắn trong ngoặc (giả thiết, "góc nội tiếp chắn nửa đường tròn", "hai góc nội tiếp cùng chắn cung $ED$", "tiếp tuyến"…). Khi dùng hai góc nội tiếp cùng chắn một cung PHẢI nêu rõ đường tròn nào: "Xét đường tròn đường kính $AB$: …" hoặc "Trong đường tròn $(O)$: …".
- Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác", "Ta thấy". Không dấu chấm phẩy ";". Không chữ "khuôn", "Câu IV", "đề thi có", "điểm", "thang điểm", "bóc tách", "vừa sức", "trọn bộ". Không xưng hô ("em", "các em", "ta cùng", "hôm nay", "ở lớp") trong đề và lời giải.
- Đề ghi ĐẦY ĐỦ giả thiết như mục "Đề và đường giải" (chép nguyên văn phần đề gốc đưa ra, chỉ đổi kí hiệu góc sang $\widehat{ABC}$). Toán trong $…$, góc viết $\widehat{EAD}$, độ $90^\circ$, tam giác $\triangle ABC$, vuông góc $\perp$, thuộc $\in$.
- Thẻ mức đặt ở ĐẦU MỖI Ý kèm sao: "a) [NB] ★ …", "b) [TH] ★★ …", "2) [VD] ★★★ …". Bài trắc nghiệm một câu: "[NB] " đứng đầu statement.
- Ví dụ (noted variant "example"): đề → dòng "{\sffamily\bfseries\color{brand}Lời giải}" → lời giải từng dòng → "Vậy …". Khoét ít nhất 5 ô bằng [[fill:đáp án]] ở chỗ then chốt (góc $90^\circ$, căn cứ "chắn nửa đường tròn", đường kính nào, cung bị chắn, kết luận). Ô nằm TRONG $…$ thì đáp án KHÔNG bọc $ (ví dụ "$\widehat{ADB} = [[fill:90^\circ]]$", "cung $[[fill:ED]]$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong ô ("[[fill:$\widehat{EBD}$]]"). Câu "Vậy …" PHẢI có ít nhất một ô [[fill:…]]. Không để dòng dưới in sẵn đáp án của ô dòng trên. Câu đề ví dụ có thêm câu "Vẽ tiếp vào Hình N các yếu tố còn thiếu theo đề." ngay sau giả thiết (trước ý a).
- Khung điền khuyết trong ĐỀ bài (Bài 2, Bài 3 ý a) dùng [[blank:1.1cm]] (một kí hiệu, số đo), [[blank:2.4cm]] (biểu thức, tên góc), [[blank:3.2cm]] (cụm từ). Câu dẫn PHẢI có cụm "hoàn thành bài giải". Mỗi dòng khung tối đa một $\Rightarrow$, dòng "Vậy …" riêng, khung mỗi ý ≥ 3 dòng. Ô trống rơi vào từ khoá cần nhớ (vuông tại …, đường kính …, cùng chắn cung …, góc nội tiếp chắn nửa đường tròn) hoặc chỗ phải suy ra. Không khoét ô mà đáp án đã in ở đề ý đó hoặc dòng dưới. Trong khung viết nhãn ý là "\textbf{a)}" KHÔNG gắn thêm thẻ lần hai.
- Bài HS tự trình bày (không khung): "answer" là lời giải đầy đủ. Bài mức TH, VD có "hints" 1–2 câu HỎI kiểu Polya (đỉnh góc vuông thuộc đường tròn nào? hai góc này cùng nhìn đoạn nào? góc nào đứng giữa hai góc cần so sánh?) — không gọi tên công cụ, không lộ đáp án.
- Bài khung điền: "answer" = đáp án từng ô, theo thứ tự, gọn (vd "a) $90^\circ$; $AD$; …" — KHÔNG dùng ";" mà dùng dấu phẩy). Thêm "statement_slide": đề rút gọn không khung (giả thiết + các ý a), b) có thẻ).
- Trắc nghiệm: "options" 4 chuỗi (không ghi A./B.), "answer" là một chữ cái. Chép đúng 4 phương án đã cho bên dưới theo đúng thứ tự.
- JSON hợp lệ: mọi gạch chéo ngược nhân đôi trong chuỗi. Không viết TikZ: ở khối cần hình, đặt "figure": "<khoá>" (khoá cho sẵn), máy sẽ thay bằng hình thật. Escape "\&" trong "GD\&ĐT".
- Tự kiểm tra từng dấu $\Rightarrow$ truy ngược về giả thiết. Nghi ngờ gì ghi vào "ghi_chu".

## Khuôn khối JSON (theo phiếu mẫu đã duyệt)
- Thẻ lý thuyết: {"type":"noted","variant":"theory","title":"1. GÓC NỘI TIẾP","text":"\\nhanly{Định nghĩa.} …[[br]]\\nhanly{Định lí.} …[[br]]\\nhanly{Nhận xét.} …","figure":"lt1"}
- Hộp lỗi hay gặp: {"type":"noted","variant":"trap","text":"- …[[br]]- …"}
- Tiêu đề phần: {"type":"para","variant":"part","text":"A. Lý thuyết"}
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"}
- Đoạn đích: {"type":"para","text":"\\textbf{Đích của buổi học:} …"}
- Ví dụ: {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} …","figure":"Ví dụ 1."}
- Bài: {"type":"problem","label":"Bài 2.","statement":"…","answer":"…","hints":[…],"figure":"Bài 2."} (trắc nghiệm thêm "options"; khung thêm "statement_slide"; bài đích thêm "quy_trinh": [4 chuỗi các bước]).
- Sơ đồ tư duy: {"type":"mindmap","caption":"Sơ đồ tư duy: …","root":"…","branches":[{"label":"…","children":[{"label":"…"}]}]} (3 nhánh, mỗi nhánh 2 lá, chữ ngắn).
- Khám phá: {"type":"para","text":"\\textbf{<câu hỏi mở>}"} + {"type":"noted","variant":"note","text":"<SGK Ví dụ 2 tr.70 chia thành các câu hỏi \\textbf{a)} … \\textbf{b)} … \\textbf{c)} …>","figure":"Hình 1"}

## Năm chặng (đúng thứ tự, đúng "kind", "number", "title")
1. {"kind":"review","number":1,"title":"Khám phá"} — tình huống SGK Toán 9 tập hai, Bài 27, Ví dụ 2 (tr.70): "Cho đường tròn $(O)$ và các điểm $A, B, C, D$ trên $(O)$ như Hình 1. Biết rằng $\widehat{BAC} = 60^\circ$" — hỏi a) hai góc $\widehat{BDC}$ và $\widehat{BAC}$ cùng chắn cung nào? b) tính $\widehat{BDC}$, c) tính $\widehat{BOC}$. (Hình 1: $A$, $D$ cùng nằm trên cung lớn $BC$, có $OB$, $OC$ nét đứt.) Ghi nguồn cuối: "(SGK Toán 9 tập hai, Bài 27, Ví dụ 2)". teacher_note ~5 phút: chỉ hỏi đáp miệng; $\widehat{BDC} = \widehat{BAC} = 60^\circ$, $\widehat{BOC} = 120^\circ$.
2. {"kind":"concept","number":2,"title":"Kiến thức cần nhớ"} — khối theo thứ tự:
   para part "A. Lý thuyết" ·
   theory "1. GÓC NỘI TIẾP" (figure "lt1"): định nghĩa, định lí, Nhận xét đúng chữ SGK tr.68–69 (hai ý: cùng chắn một cung thì bằng nhau, chắn nửa đường tròn là góc vuông). Hình lt1: đường tròn $(O)$, các điểm $M, N, P, Q$, hai góc $\widehat{PMQ}$, $\widehat{PNQ}$ cùng chắn cung $PQ$. Ghi "(SGK Toán 9 tập hai, tr.68–69)". ·
   theory "2. ĐỈNH GÓC VUÔNG VÀ ĐƯỜNG TRÒN ĐƯỜNG KÍNH" (figure "lt2"): chép câu SGK tr.73 "Đường tròn ngoại tiếp tam giác vuông có tâm là trung điểm của cạnh huyền và bán kính bằng một nửa cạnh huyền." ⇒ trên hình lt2: $\triangle ACB$ vuông tại $C$, $\triangle ADB$ vuông tại $D$ ⇒ $A, B, C, D$ cùng thuộc đường tròn đường kính $AB$ (tứ giác $ACDB$ nội tiếp — tứ giác có bốn đỉnh cùng thuộc một đường tròn). ·
   para part "B. Phương pháp chứng minh — các dạng quen thuộc" ·
   theory "DẠNG 1. HAI GÓC NỘI TIẾP CÙNG CHẮN MỘT CUNG" (figure "lt3"): \nhanly{Bước 1:} tìm một đường tròn đi qua đỉnh của hai góc và hai đầu mút của cung (đường tròn $(O)$ đề cho, hoặc đường tròn có được ở ý trước nhờ hai góc vuông). \nhanly{Bước 2:} chỉ ra hai góc là góc nội tiếp cùng chắn một cung của đường tròn đó. \nhanly{Bước 3:} kết luận. Minh hoạ theo hình lt3: $\widehat{AEB} = \widehat{ADB} = 90^\circ$ ⇒ $A, B, D, E$ thuộc đường tròn đường kính $AB$ ⇒ $\widehat{EAD} = \widehat{EBD}$ (cùng chắn cung $ED$). ·
   theory "DẠNG 2. BẮC CẦU QUA GÓC THỨ BA" (figure "lt4"): muốn chứng minh $\widehat{X} = \widehat{Y}$ mà hai góc không cùng nằm trong một đường tròn thì tìm góc $\widehat{Z}$ đứng giữa: $\widehat{X} = \widehat{Z}$ (hai góc nội tiếp cùng chắn một cung của đường tròn thứ nhất), $\widehat{Z} = \widehat{Y}$ (cùng chắn một cung của đường tròn thứ hai, hoặc cùng bằng một số đo) ⇒ $\widehat{X} = \widehat{Y}$. Minh hoạ theo hình lt4 (là Hình 5 của Ví dụ 2): $\widehat{ABD} = \widehat{ACD}$ (đường tròn đường kính $BC$), $\widehat{ACD} = \widehat{MED}$ (đường tròn đường kính $MC$). ·
   trap: 3 lỗi hay gặp: viết "cùng chắn cung" mà không nêu đường tròn nào; đọc sai cung bị chắn (cung nằm bên trong góc); dùng hai góc của hai đường tròn khác nhau mà không có góc bắc cầu.
   teacher_note: giảng ~12 phút, đọc lý thuyết đúng chữ SGK, hai dạng chỉ là cách tìm đường tròn, ví dụ mẫu nằm ở đầu từng mạch Luyện tập.
3. {"kind":"practice1","number":3,"title":"Luyện tập 1"} — khối theo thứ tự:
   para đích: "\textbf{Đích của buổi học:} Bài 4 (Đề thi thử vào 10 THPT Sơn Tây, Hà Nội, 2024--2025): ý 1 chứng minh tứ giác nội tiếp bằng hai góc vuông (Mạch 1), ý 2 chứng minh hai góc bằng nhau bằng cách bắc cầu qua một góc thứ ba (Mạch 2)."
   heading "Mạch 1. Hai góc nội tiếp cùng chắn một cung" · Bài 1. · Ví dụ 1. · Bài 2.
   heading "Mạch 2. Bắc cầu qua góc thứ ba" · Ví dụ 2. · Bài 3.
   teacher_note (kịch bản phút lớp C): Bài 1 ~3′ · Ví dụ 1 GV vẽ cùng HS rồi điền ô ~12′ · Bài 2 HS vẽ tiếp $N$, $T$ rồi điền khung ~10′ · Ví dụ 2 ~14′ · Bài 3 vẽ tiếp, điền ý a, tự trình bày ý b vào vở ~16′.
4. {"kind":"practice2","number":4,"title":"Luyện tập 2"} — para heading "Đề thi thử vào 10 — THPT Sơn Tây (Hà Nội) 2024--2025" · Bài 4. (bài đích, HS tự vẽ hình, tự trình bày, có hints + quy_trinh 4 bước).
   teacher_note: ~30′: HS tự vẽ hình ~5′, ý 1 ~10′ (như Bài 2, Bài 3 ý a), ý 2 ~15′ (như Ví dụ 2). GV chấm ý 1 trước.
5. {"kind":"reflection","number":5,"title":"Sơ đồ tư duy"} — mindmap (root "GÓC NỘI TIẾP CÙNG CHẮN MỘT CUNG", nhánh: "TÌM ĐƯỜNG TRÒN" (đường tròn $(O)$ đã cho / hai góc vuông cùng nhìn một đoạn), "CÙNG CHẮN MỘT CUNG" (nêu rõ đường tròn / đọc đúng cung bị chắn), "BẮC CẦU" (tìm góc đứng giữa / mỗi bước một đường tròn)) rồi NGAY SAU là BTVN 1. … BTVN 4. (KHÔNG đặt tiêu đề/para trước BTVN 1).
   teacher_note: BTVN ~55′ (dày hơn quỹ 40′ để HS có thêm bài): BTVN 1–2 trắc nghiệm ~5′, BTVN 3 ~22′, BTVN 4 ~28′ (gồm vẽ hình).

## Đề và đường giải (Claude đã soi ảnh đề gốc và kiểm số đo bằng toạ độ — dùng đúng, không đổi)

### Bài 1. (trắc nghiệm, hình "Bài 1." = Hình 2, tách từ ý b đề giữa học kì II THCS Nhật Tân 2025–2026)
statement: "[NB] Cho $\triangle ABC$ có $AB < AC$, nội tiếp đường tròn $(O)$. Các đường cao $AD$, $BE$ cắt nhau tại $H$ (Hình 2). Biết tứ giác $ABDE$ nội tiếp. Góc nào sau đây bằng góc $\widehat{BED}$?"  options: ["$\widehat{BAE}$","$\widehat{BAD}$","$\widehat{ABE}$","$\widehat{BCA}$"]  answer "B". Thêm cuối statement nguồn: " \;(Tách từ đề giữa học kì II THCS Nhật Tân, 2025--2026)".

### Ví dụ 1. (Đề giữa học kì II THCS Mỹ Đình 2, 2025–2026, Bài 4.2 ý a và phần góc của ý b) — hình "Ví dụ 1." = Hình 3 (HS chỉ thấy $\triangle ABC$ vuông tại $A$)
Đề: "Cho $\triangle ABC$ vuông tại $A$. Gọi $O$ là trung điểm của cạnh $AC$. Đường tròn tâm $O$ đường kính $AC$ cắt cạnh $BC$ tại $D$ ($D$ khác $C$). Kẻ $AE$ vuông góc với $OB$ tại $E$ (Hình 3)." + câu vẽ tiếp + "a) [NB] ★ Chứng minh bốn điểm $A, B, D, E$ cùng thuộc một đường tròn.[[br]]b) [TH] ★★ Chứng minh $\widehat{EAD} = \widehat{EBD}$."
Đường giải: a) $\widehat{ADC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn $(O)$) ⇒ $\widehat{ADB} = 90^\circ$ ⇒ $\triangle ADB$ vuông tại $D$ ⇒ $D$ thuộc đường tròn đường kính $AB$. $AE \perp OB$ tại $E$ ⇒ $\triangle AEB$ vuông tại $E$ ⇒ $E$ thuộc đường tròn đường kính $AB$. Vậy bốn điểm $A, B, D, E$ cùng thuộc đường tròn đường kính $AB$.
b) Xét đường tròn đường kính $AB$ (câu a): $\widehat{EAD}$ và $\widehat{EBD}$ là hai góc nội tiếp cùng chắn cung $ED$. Vậy $\widehat{EAD} = \widehat{EBD}$.

### Bài 2. (Đề kiểm tra học kì II Phòng GD\&ĐT Cầu Giấy, 2024–2025, Câu IV.2 ý a và phần góc của ý b) — hình "Bài 2." = Hình 4 (HS thấy $\triangle ABC$ và đường cao $AD$)
Đề: "Cho tam giác nhọn $ABC$ ($AB < AC$) có đường cao $AD$. Gọi $N$, $T$ lần lượt là chân đường vuông góc kẻ từ $D$ đến $AB$, $AC$ (Hình 4)." + "Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề rồi điền vào chỗ chấm để hoàn thành bài giải:" + "a) [NB] ★ Chứng minh bốn điểm $A, N, D, T$ cùng thuộc một đường tròn." (khung 5 dòng theo đường giải) + "b) [TH] ★★ Chứng minh $\widehat{DNT} = \widehat{DAT}$." (khung 3 dòng).
Đường giải: a) $DN \perp AB$ tại $N$ ⇒ $\triangle AND$ vuông tại $N$ ⇒ $N$ thuộc đường tròn đường kính $AD$. $DT \perp AC$ tại $T$ ⇒ $\triangle ATD$ vuông tại $T$ ⇒ $T$ thuộc đường tròn đường kính $AD$. Vậy bốn điểm $A, N, D, T$ cùng thuộc đường tròn đường kính $AD$.
b) Xét đường tròn đường kính $AD$ (câu a): $\widehat{DNT}$ và $\widehat{DAT}$ là hai góc nội tiếp cùng chắn cung $DT$. Vậy $\widehat{DNT} = \widehat{DAT}$.

### Ví dụ 2. (Đề giữa học kì II THCS Nguyễn Trường Tộ, 2025–2026, Bài 4 ý 1 và phần góc của ý 2) — hình "Ví dụ 2." = Hình 5 (HS chỉ thấy $\triangle ABC$ vuông tại $A$)
Đề: "Cho tam giác $ABC$ vuông tại $A$ ($AB > AC$). Trên cạnh $AC$ lấy điểm $M$ (khác $A$ và $C$). Đường tròn đường kính $MC$ cắt $BC$ tại $E$ và cắt đường thẳng $BM$ tại $D$ ($E$ khác $C$, $D$ khác $M$) (Hình 5)." + câu vẽ tiếp + "a) [NB] ★ Chứng minh tứ giác $ABCD$ nội tiếp.[[br]]b) [VD] ★★★ Chứng minh $\widehat{ABD} = \widehat{MED}$."
Đường giải: a) $\widehat{BAC} = 90^\circ$ (giả thiết) ⇒ $A$ thuộc đường tròn đường kính $BC$. $\widehat{MDC} = 90^\circ$ (góc nội tiếp chắn nửa đường tròn đường kính $MC$) ⇒ $\widehat{BDC} = 90^\circ$ ($D$ thuộc đường thẳng $BM$) ⇒ $D$ thuộc đường tròn đường kính $BC$. ⇒ $A, B, C, D$ cùng thuộc đường tròn đường kính $BC$. Vậy tứ giác $ABCD$ nội tiếp.
b) Xét đường tròn đường kính $BC$: $\widehat{ABD} = \widehat{ACD}$ (hai góc nội tiếp cùng chắn cung $AD$). Xét đường tròn đường kính $MC$: $\widehat{MCD} = \widehat{MED}$ (hai góc nội tiếp cùng chắn cung $MD$). $M$ thuộc cạnh $AC$ ⇒ $\widehat{ACD} = \widehat{MCD}$. Vậy $\widehat{ABD} = \widehat{MED}$.

### Bài 3. (Đề kiểm tra cuối kì II THCS Cầu Diễn, 2025–2026, Bài IV.2 ý a và phần góc của ý b) — hình "Bài 3." = Hình 6 (HS thấy đường tròn $(O)$, hai đường kính $AB$, $CD$)
Đề: "Cho đường tròn $(O)$ có hai đường kính $AB$ và $CD$ vuông góc với nhau tại $O$. Trên tia đối của tia $CA$ lấy điểm $M$ ($M$ khác $C$). Kẻ $CH$ vuông góc với $BM$ tại $H$ (Hình 6)." + "Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề." + "a) [NB] ★ Điền vào chỗ chấm để hoàn thành bài giải chứng minh tứ giác $BOCH$ nội tiếp:" (khung 5 dòng) + "b) [TH] ★★ Chứng minh $HO$ là tia phân giác của góc $\widehat{BHC}$ (trình bày vào vở)."
Đường giải a) $AB \perp CD$ tại $O$ ⇒ $\widehat{BOC} = 90^\circ$ ⇒ $O$ thuộc đường tròn đường kính $BC$. $CH \perp BM$ tại $H$ ⇒ $\widehat{BHC} = 90^\circ$ ⇒ $H$ thuộc đường tròn đường kính $BC$. ⇒ $B, O, C, H$ cùng thuộc đường tròn đường kính $BC$. Vậy tứ giác $BOCH$ nội tiếp.
b) (answer cho ý b) $OB = OC$ (bán kính), $\widehat{BOC} = 90^\circ$ ⇒ $\triangle OBC$ vuông cân tại $O$ ⇒ $\widehat{OBC} = \widehat{OCB} = 45^\circ$. Xét đường tròn đường kính $BC$: $\widehat{BHO} = \widehat{BCO} = 45^\circ$ (hai góc nội tiếp cùng chắn cung $BO$). $\widehat{CHO} = \widehat{CBO} = 45^\circ$ (hai góc nội tiếp cùng chắn cung $CO$). ⇒ $\widehat{BHO} = \widehat{CHO}$, tia $HO$ nằm giữa hai tia $HB$, $HC$. Vậy $HO$ là tia phân giác của góc $\widehat{BHC}$.
"answer" bài này gồm: đáp án các ô ý a + lời giải đầy đủ ý b. hints (cho ý b) 2 câu hỏi.

### Bài 4. (bài đích — Đề thi thử vào 10 lần 1, THPT Sơn Tây, 2024–2025, Bài IV ý 1 và phần góc của ý 2) — hình "Bài 4." = Hình 7
statement: "Cho tam giác $ABC$ ($AB > AC$) nội tiếp đường tròn tâm $O$. Gọi $M$ là trung điểm của đoạn thẳng $BC$; $E$, $F$ lần lượt là chân đường vuông góc kẻ từ $M$ đến các đường thẳng $AB$, $AC$.[[br]]1) [TH] ★★ Chứng minh tứ giác $AEMF$ là tứ giác nội tiếp.[[br]]2) [VD] ★★★ Đường thẳng $AM$ cắt đường tròn $(O)$ tại điểm thứ hai là $K$. Chứng minh $\widehat{KBC} = \widehat{MEF}$." (Lưu ý: dấu ";" trong đề gốc giữ dạng "$BC$, $E$" — thay ";" bằng ". Gọi" nếu cần: viết "…đoạn thẳng $BC$. Gọi $E$, $F$ lần lượt là…".)
Đường giải: 1) $ME \perp AB$ tại $E$ ⇒ $\triangle AEM$ vuông tại $E$ ⇒ $E$ thuộc đường tròn đường kính $AM$. $MF \perp AC$ tại $F$ ⇒ $\triangle AFM$ vuông tại $F$ ⇒ $F$ thuộc đường tròn đường kính $AM$. ⇒ $A, E, M, F$ cùng thuộc đường tròn đường kính $AM$. Vậy tứ giác $AEMF$ nội tiếp.
2) Trong đường tròn $(O)$: $\widehat{KBC} = \widehat{KAC}$ (hai góc nội tiếp cùng chắn cung $KC$). Xét đường tròn đường kính $AM$: $\widehat{MAF} = \widehat{MEF}$ (hai góc nội tiếp cùng chắn cung $MF$). $K$ thuộc tia $AM$, $F$ thuộc tia $AC$ ⇒ $\widehat{KAC} = \widehat{MAF}$. Vậy $\widehat{KBC} = \widehat{MEF}$.
quy_trinh: (1) vẽ hình: tam giác nội tiếp, trung điểm $M$, hai đường vuông góc $ME$, $MF$, tia $AM$ cắt $(O)$ tại $K$ · (2) ý 1: hai góc vuông cùng nhìn $AM$ (như Bài 2) · (3) ý 2: tìm góc đứng giữa $\widehat{KAC}$ · (4) mỗi đẳng thức nêu rõ đường tròn và cung bị chắn (như Ví dụ 2). hints 2 câu hỏi.

### BTVN 1. (trắc nghiệm, hình "BTVN 1." = Hình 8, tách từ ý b đề giữa học kì II xã Đông Anh 2025–2026)
statement: "[NB] Cho $\triangle ABC$ nhọn có $AB < BC$, nội tiếp đường tròn $(O)$. Kẻ đường kính $BK$ của đường tròn $(O)$ cắt cạnh $AC$ tại $Q$ (Hình 8). Góc nào sau đây bằng góc $\widehat{BAC}$? \;(Tách từ đề giữa học kì II xã Đông Anh, 2025--2026)"  options ["$\widehat{KBC}$","$\widehat{BQC}$","$\widehat{BKC}$","$\widehat{ACK}$"]  answer "C".

### BTVN 2. (trắc nghiệm, hình "BTVN 2." = Hình 9, tách từ ý b đề kiểm tra cuối học kì II THCS\&THPT M.V. Lômônôxốp 2024–2025)
statement: "[NB] Cho $\triangle ABC$ nhọn ($AB < AC$) nội tiếp đường tròn $(O)$. Hai đường cao $BE$ và $CF$ cắt nhau tại $H$ (Hình 9). Biết bốn điểm $A, F, H, E$ cùng thuộc đường tròn đường kính $AH$. Góc nào sau đây bằng góc $\widehat{AEF}$? \;(Tách từ đề cuối học kì II THCS\&THPT M.V. Lômônôxốp, 2024--2025)"  options ["$\widehat{AFE}$","$\widehat{AHE}$","$\widehat{BHF}$","$\widehat{AHF}$"]  answer "D".

### BTVN 3. (Đề kiểm tra cuối kỳ II Phòng GD\&ĐT Hà Đông, 2024–2025, Câu IV.2 ý a và phần góc của ý b) — HS tự vẽ hình (hình "BTVN 3." = Hình 10 chỉ là nửa đường tròn nền)
statement: "Cho nửa đường tròn tâm $O$, đường kính $AB$. Lấy điểm $C$ thuộc nửa đường tròn $(O)$ sao cho $CA < CB$ và điểm $D$ thuộc đoạn $OA$ ($D$ khác $O$ và $A$). Đường thẳng qua $C$ vuông góc với $CD$ cắt các tiếp tuyến của nửa đường tròn $(O)$ tại $A$ và $B$ lần lượt tại $E$ và $F$ (Hình 10).[[br]]a) [TH] ★★ Chứng minh bốn điểm $A, C, D, E$ cùng thuộc một đường tròn.[[br]]b) [TH] ★★ Chứng minh $\widehat{CFD} = \widehat{CBA}$."
Đường giải: a) $CE \perp CD$ tại $C$ ⇒ $\triangle DCE$ vuông tại $C$ ⇒ $C$ thuộc đường tròn đường kính $DE$. $EA$ là tiếp tuyến của $(O)$ tại $A$ ⇒ $EA \perp AB$ ⇒ $\triangle DAE$ vuông tại $A$ ⇒ $A$ thuộc đường tròn đường kính $DE$. Vậy bốn điểm $A, C, D, E$ cùng thuộc đường tròn đường kính $DE$.
b) $CF \perp CD$ tại $C$ ⇒ $\triangle DCF$ vuông tại $C$ ⇒ $C$ thuộc đường tròn đường kính $DF$. $FB$ là tiếp tuyến của $(O)$ tại $B$ ⇒ $FB \perp AB$ ⇒ $\triangle DBF$ vuông tại $B$ ⇒ $B$ thuộc đường tròn đường kính $DF$. Xét đường tròn đường kính $DF$: $\widehat{CFD} = \widehat{CBD}$ (hai góc nội tiếp cùng chắn cung $CD$). $D$ thuộc đoạn $OA$ ⇒ tia $BD$ trùng tia $BA$ ⇒ $\widehat{CBD} = \widehat{CBA}$. Vậy $\widehat{CFD} = \widehat{CBA}$.
hints 2 câu hỏi.

### BTVN 4. (Đề thi học kì II THCS Ngọc Thụy (Long Biên), 2024–2025, Đề 1, Bài IV.2 ý a và phần góc của ý b) — HS tự vẽ hình (hình "BTVN 4." = Hình 11 nền: đường tròn và tam giác)
statement: "Cho tam giác $ABC$ có ba góc nhọn nội tiếp đường tròn tâm $O$ bán kính $R$ và $AH$ là đường cao của tam giác $ABC$. Gọi $M$, $N$ lần lượt là chân đường vuông góc kẻ từ $H$ đến $AB$ và $AC$ (Hình 11).[[br]]a) [TH] ★★ Chứng minh bốn điểm $A, M, H, N$ cùng thuộc một đường tròn.[[br]]b) [VD] ★★★ Chứng minh $\widehat{ANM} = \widehat{ABC}$."
Đường giải: a) $HM \perp AB$ tại $M$ ⇒ $\triangle AMH$ vuông tại $M$ ⇒ $M$ thuộc đường tròn đường kính $AH$. $HN \perp AC$ tại $N$ ⇒ $\triangle ANH$ vuông tại $N$ ⇒ $N$ thuộc đường tròn đường kính $AH$. Vậy bốn điểm $A, M, H, N$ cùng thuộc đường tròn đường kính $AH$.
b) Xét đường tròn đường kính $AH$: $\widehat{ANM} = \widehat{AHM}$ (hai góc nội tiếp cùng chắn cung $AM$). $\triangle AMH$ vuông tại $M$ ⇒ $\widehat{AHM} = 90^\circ - \widehat{MAH}$. $\triangle AHB$ vuông tại $H$ ⇒ $\widehat{ABH} = 90^\circ - \widehat{BAH}$. $\widehat{MAH} = \widehat{BAH}$ ($M$ thuộc cạnh $AB$) ⇒ $\widehat{AHM} = \widehat{ABH}$. Vậy $\widehat{ANM} = \widehat{ABC}$.
hints 2 câu hỏi (gợi ý: góc nào đứng giữa? tổng hai góc nhọn của tam giác vuông?).

## Đầu ra
JSON {"stages":[5 chặng],"ghi_chu":"…"}. Không thêm bài nào ngoài danh sách. Trong "ghi_chu" liệt kê mọi chỗ bạn nghi ngờ.
'''


def main():
    v = {"id": VID, "model": "gemini-4-hydrogen-medium", "prompt": PROMPT, "files": [],
         "schema": "scripts/gemini/schema/dung-chang-phieu.json", "timeout": "1800s",
         "meta": {"loai": "dung-chang-phieu", "seed": "phieu-g ch.IX 9C"}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO), f"({len(PROMPT) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
