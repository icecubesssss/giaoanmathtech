#!/usr/bin/env python3
"""Dựng lại phiếu D ch.VI 9C (13/11/2026) — "Tính giá trị biểu thức chứa hai nghiệm".

Lỗi bản cũ (10/09): tên "Luyện khuôn Câu III.3"; lý thuyết dạy "khuôn", "mất 0,25 điểm"; bài NB "viết câu kết luận",
"đề hỏi thế này dùng công thức nào"; Bài 2 Viète không có bước Δ; Bài 8 cho sẵn tổng, tích; 10 ví dụ trùng đề với bài;
dấu ";" ngoài công thức; dan_dat_gate chặn (điền khuyết sau tự trình bày); BTVN 100′/90′; chưa tách phiếu BTVN.
Đề + đáp số: Claude chọn, kiểm SymPy ở so_do_phieu_d_9c.py. Gemini chỉ viết chữ.

    python3 scripts/gemini/viec_dung_lai_phieu_d_9c.py
    python3 scripts/gemini/tho.py --mot dung-9c-ch6-phieu-d-lt   (… -lop, … -btvn)
    python3 scripts/gemini/lap_dung_lai_phieu_d_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_phieu_d_9c import tom_tat  # noqa: E402

SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-d-luyen-khuon-cau-iii-3.json"
VID_LT, VID_LOP, VID_BTVN = "dung-9c-ch6-phieu-d-lt", "dung-9c-ch6-phieu-d-lop", "dung-9c-ch6-phieu-d-btvn"

DE_2026 = (r"Biết phương trình bậc hai $x^2-3x+1=0$ có hai nghiệm phân biệt $x_1$ và $x_2$, tính giá trị của biểu "
           r"thức $Q=\dfrac{3x_2-1}{x_1}+\dfrac{3x_1}{x_2}-x_1$.")
DE_TU_LAP = (r"Biết phương trình $x^2+10x+4=0$ có hai nghiệm âm phân biệt $x_1$, $x_2$. Không giải phương trình, hãy "
             r"tính giá trị của biểu thức $A=\sqrt{-16x_1+5}-x_2$.")

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi luyện tập sau Bài 20 "Định lí Viète và ứng dụng", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Chủ đề buổi: TÍNH GIÁ TRỊ BIỂU THỨC CHỨA HAI NGHIỆM — gồm Viète, HẠ BẬC (dùng $x_1$ là nghiệm để viết $x_1^2$, $x_1^3$ theo $x_1$), biểu thức không đối xứng, xét dấu nghiệm và $\sqrt{A^2}=|A|$. KHÔNG có tham số $m$. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật cứng (vi phạm bị trả lại)
- CẤM chữ/ý: "khuôn", "Câu III", "đề Vào 10 hỏi", điểm số, "mất 0,25 điểm", "thang điểm", "tầng C", "bài thi trừ điểm", "mẹo", "chìa khóa". CẤM kí hiệu $S$, $P$ cho tổng, tích (viết $x_1+x_2$, $x_1x_2$). Tên biểu thức dùng đúng chữ cái sơ đồ ghi ($G$, $P$, $H$, $A$, $Q$, …).
- CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "ép", "nhé". Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác" — dùng "nên", "$\Rightarrow$", hoặc xuống dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Hai đẳng thức liền nhau viết bằng "và" hoặc hệ $\begin{cases} … \\ … \end{cases}$.
- Câu dẫn của đề TỰ SOẠN viết "Cho phương trình … . Gọi $x_1$, $x_2$ là hai nghiệm của phương trình." — KHÔNG viết "biết phương trình có hai nghiệm phân biệt" (học sinh phải tự kiểm tra $\Delta$). Riêng hai đề thật (Bài 9, Bài 10) chép NGUYÊN VĂN, giữ chú thích nguồn.
- Lời giải theo NHỊP BÀI THI, mỗi bước một dòng [[br]] có thụt "\hspace*{1.4em}" (ví dụ, khung điền) và "Vậy …" dòng riêng ở cuối:
  (1) "Ta có $\Delta=(-7)^2-4\cdot 1\cdot 3=37>0$ nên phương trình có hai nghiệm phân biệt." (hoặc "Ta có $ac=1\cdot(-7)=-7<0$ nên …", hoặc $\Delta'$ khi $b$ chẵn)
  (2) "Theo định lí Viète, ta có $\begin{cases} x_1+x_2=7\\ x_1x_2=3\end{cases}$" (chỉ viết khi cần dùng)
  (3) hạ bậc: "Vì $x_1$ là nghiệm của phương trình nên $x_1^2-2x_1-5=0$, tức là $x_1^2=2x_1+5$."
      bậc ba: "$x_1^3=x_1\cdot x_1^2=x_1(2x_1+5)=2x_1^2+5x_1=2(2x_1+5)+5x_1=9x_1+10$."
  (4) thay vào, tính: "$P=(5x_1+2)+5x_2-3=5(x_1+x_2)-1=5\cdot 5-1=24$."
  (5) "Vậy $P=24$."
  Xét dấu: "Vì $x_1x_2=2>0$ và $x_1+x_2=-6<0$ nên hai nghiệm cùng âm." Phá căn: "$\sqrt{(x_1-1)^2}=|x_1-1|=1-x_1$ (vì $x_1<0$ nên $x_1-1<0$)."
- Thẻ mức đặt ở ĐẦU MỖI Ý: "a) [NB] …". Bài một ý thì thẻ "[TH]"/"[VD]"/"[NB]" đứng đầu đề. Không gắn thẻ ở cả đề lẫn ý.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT".
- Số liệu và đáp số ở mục "Sơ đồ đề và đáp số" ĐÃ ĐƯỢC MÁY KIỂM (SymPy) — dùng đúng, KHÔNG đổi phương trình, KHÔNG đổi biểu thức. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số.

## Khuôn khối (JSON)
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"}
- Ví dụ (giáo viên làm cùng lớp, có ô điền): {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …"}
  Trong Lời giải khoét 3–6 ô bằng [[fill:đáp án]] ở chỗ then chốt (giá trị $\Delta$, tổng, tích, $x_1^2=$…, kết quả thay số, kết luận). Ô trong $…$ thì đáp án KHÔNG bọc $ (ví dụ "$\Delta=[[fill:37]]>0$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong (ví dụ "[[fill:$1-x_1$]]"). KHÔNG để một số vừa nằm trong ô lại in sẵn ở dòng dưới (lộ đáp án).
- Bài NB điền khuyết = BÀI TRÌNH BÀY HOÀN CHỈNH theo đúng các dòng của ví dụ đứng trước, chỗ HS điền ghi "\\ldots\\ldots". Ví dụ đúng khuôn (bài cũ của phiếu khác):
"Điền vào chỗ chấm để viết tổng và tích hai nghiệm của mỗi phương trình sau (làm đủ các bước như Ví dụ 1).[[br]]a) [NB] $x^2-3x+1=0$[[br]]\\hspace*{1.4em}Ta có $\\Delta=\\ldots\\ldots>0$ nên phương trình có hai nghiệm phân biệt.[[br]]\\hspace*{1.4em}Theo định lí Viète, ta có $\\begin{cases} x_1+x_2=\\ldots\\ldots\\\\ x_1x_2=\\ldots\\ldots\\end{cases}$[[br]]\\hspace*{1.4em}Vậy tổng hai nghiệm bằng \\ldots\\ldots\\ và tích hai nghiệm bằng \\ldots\\ldots.[[br]]b) [NB] …"
  Mỗi ý ≥ 3 chỗ chấm, chỗ chấm rơi vào CHỖ PHẢI SUY RA (giá trị, biểu thức sau hạ bậc, kết quả), không rơi vào chữ in sẵn ở dòng khác. "solution": lời giải đầy đủ từng ý (a) …[[br]]\\hspace*{1.4em}…[[br]]b) …), điền hết các chỗ chấm.
- Bài TH, VD (tự trình bày): "statement" chỉ có ĐỀ, không chỗ chấm, không khung. "solution": lời giải đầy đủ theo nhịp bài thi. "hints": 1–2 câu hỏi gợi ý kiểu Polya ("Biểu thức có chứa $x_1^2$ không? Từ phương trình viết được $x_1^2$ theo $x_1$ không?") — không lộ số, không làm hộ.
- Khối bài: {"type":"problem","label":"Bài N.","level":1|2|3,"tier":"onclass"|"btvn","statement":…,"solution":…,"hints":[…]} (NB level 1 có thể "hints": []).
'''


def so_do(*nhan):
    tt, trung = tom_tat()
    assert not trung, trung
    return "\n".join(f"- {k}\n" + "\n".join("    " + d for d in tt[k]) for k in nhan)


PROMPT_LT = CHUNG + r'''
## Việc A: viết phần mở đầu, lý thuyết, sơ đồ tư duy, ghi chú giáo viên
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap","teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

1. "opener_text" (chặng Khám phá, khoảng 5–7 dòng [[br]]): nêu đề Câu III.3 đề chính thức Vào 10 Hà Nội 2026 (chép nguyên văn ở dưới, trong \emph{\textquotedblleft…\textquotedblright}), chỉ ra biểu thức trông lệch (đổi chỗ $x_1$, $x_2$ là ra biểu thức khác) nhưng tính được ra số nhờ hai việc: dùng định lí Viète và dùng "$x_1$ là nghiệm" để hạ bậc. Kết bằng câu: đây là Bài 10 — bài cuối của phiếu. Không xưng hô, không "hôm nay", không điểm số.
   Đề: ''' + DE_2026 + r'''
2. "review_note" (khối "Nhắc lại" của chặng Khám phá — CHỈ lý thuyết của Bài 20 đã học): một chuỗi gồm định lí Viète (điều kiện có hai nghiệm $\Delta\ge 0$, trường hợp $ac<0$) và bốn công thức $x_1^2+x_2^2$, $\dfrac{1}{x_1}+\dfrac{1}{x_2}$, $x_1^3+x_2^3$, $(x_1-x_2)^2$ theo tổng và tích, mỗi mục một dòng "$\bullet$\; …".
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT, đúng chữ SGK, mục đánh số "\textbf{N. Tên}" (một khối para tiêu đề + một khối para nội dung), 4 mục:
   1. Định lí Viète — phát biểu như SGK Toán 9 tập hai Bài 20: "Nếu $x_1$, $x_2$ là hai nghiệm của phương trình $ax^2+bx+c=0$ ($a\ne 0$) thì $x_1+x_2=-\dfrac{b}{a}$ và $x_1x_2=\dfrac{c}{a}$." kèm: phương trình có hai nghiệm khi $\Delta\ge 0$; nếu $ac<0$ thì phương trình có hai nghiệm trái dấu.
   2. Nghiệm của phương trình — "Số $x_1$ là nghiệm của phương trình $ax^2+bx+c=0$ khi và chỉ khi $ax_1^2+bx_1+c=0$." Từ đó $ax_1^2=-bx_1-c$, và $x_1^3=x_1\cdot x_1^2$ (viết được $x_1^2$, $x_1^3$ theo $x_1$). Một ví dụ số ngắn một dòng với phương trình $x^2-x-2=0$: $x_1^2=x_1+2$.
   3. Biểu thức đối xứng — biểu thức không đổi khi đổi chỗ $x_1$ và $x_2$ (ví dụ $x_1^2+x_2^2$, $x_1x_2$, $\dfrac{1}{x_1}+\dfrac{1}{x_2}$) luôn viết được theo $x_1+x_2$ và $x_1x_2$.
   4. Dấu của hai nghiệm và căn bậc hai của một bình phương — $x_1x_2<0$: trái dấu; $x_1x_2>0$, $x_1+x_2>0$: cùng dương; $x_1x_2>0$, $x_1+x_2<0$: cùng âm. $\sqrt{A^2}=|A|$, với $|A|=A$ khi $A\ge 0$ và $|A|=-A$ khi $A<0$ (SGK Toán 9 tập một, chương III).
   Khối: {"type":"para","text":"\\textbf{1. Định lí Viète}"} rồi {"type":"para","text":"…"}. KHÔNG thêm khối trap, target, mẹo, các bước làm bài, lỗi hay gặp.
4. "mindmap": {"type":"mindmap","caption":"Điền các ô trống để tự tóm tắt cả buổi","root":"Tính giá trị biểu thức chứa hai nghiệm","branches":[4 nhánh: "Định lí Viète" (con: $x_1+x_2=[[blank:1.4cm]]$, $x_1x_2=[[blank:1.2cm]]$, điều kiện $\Delta[[blank:1cm]]0$), "Hạ bậc" (con: $ax_1^2=[[blank:2cm]]$, $x_1^3=x_1\cdot[[blank:1cm]]$), "Biểu thức đối xứng" (con: $x_1^2+x_2^2=[[blank:3cm]]$), "Dấu và căn" (con: $\sqrt{A^2}=[[blank:1cm]]$, $x_1x_2<0$: hai nghiệm [[blank:1.6cm]])]}. Mỗi nhánh {"label":…,"children":[{"label":…}]}.
5. "teacher_notes" (ghi chú giáo viên, ngắn, chỉ cách tổ chức dạy, không "khuôn"/điểm số):
   review: mở màn 8 phút, đọc đề 2026, hỏi đổi chỗ $x_1$, $x_2$ thì $Q$ có đổi không, chưa giải — để dành Bài 10.
   concept: giảng 15 phút, mục 2 (hạ bậc) là kiến thức mới duy nhất, cho học sinh tự viết $x_1^2$ của phương trình $x^2-x-2=0$.
   practice1: khoảng 55 phút, 4 mạch (Viète — hạ bậc — biểu thức không đối xứng — dấu và căn), mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh điền bài ngay sau; Bài 5 là bài giải trọn vẹn đầu tiên, chữa kĩ.
   practice2: khoảng 60 phút, Bài 7–8 mỗi ý khoảng 6 phút, Bài 9 và Bài 10 là hai đề thật (THCS Tự Lập, đề Hà Nội 2026), làm cá nhân rồi gọi lên bảng; Bài 10 là đích của buổi.
   reflection: sơ đồ tư duy 5 phút cuối buổi; Bài tập về nhà Bài 11–20 in thành phiếu riêng, khoảng 85 phút; buổi sau chữa Bài 19 và Bài 20 trước.

## Bản cũ — tham khảo (KHÔNG chép các chỗ vi phạm luật)
'''

PROMPT_LOP = CHUNG + r'''
## Việc B: dựng 2 chặng LUYỆN TẬP trên lớp
Đầu ra JSON {"stages":[{"kind":"practice1",…},{"kind":"practice2",…}],"ghi_chu"}. Mỗi stage có "kind","number","title","teacher_note","blocks" (teacher_note để chuỗi rỗng — máy tự điền).

### Chặng "practice1" — title "Luyện tập 1 — Nhận biết", number 3. Thứ tự khối:
- {"type":"para","text":"\\textbf{Đích của buổi học:} Bài 10 — tính giá trị biểu thức không đối xứng của hai nghiệm (đề chính thức Vào 10 Hà Nội 2026). Mạch 1 và Mạch 2 cho hai việc đầu của lời giải (Viète, hạ bậc), Mạch 3 ghép hai việc đó, Mạch 4 dùng cho Bài 9."}
- heading "Mạch 1. Viết tổng và tích hai nghiệm" → Ví dụ 1 → Bài 1.
- heading "Mạch 2. Hạ bậc" → Ví dụ 2 → Bài 2. → Ví dụ 3 → Bài 3.
- heading "Mạch 3. Biểu thức không đối xứng" → Ví dụ 4 → Bài 4. → Bài 5.
- heading "Mạch 4. Dấu của nghiệm và căn bậc hai" → Ví dụ 5 → Bài 6.
Yêu cầu từng khối:
- Ví dụ 1: đề "Cho phương trình $x^2-7x+3=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Viết tổng và tích hai nghiệm." Lời giải 3 dòng như khuôn trên, ô ở $\Delta$, tổng, tích.
- Bài 1 (NB, 3 ý): như khuôn Bài 1 ở trên với 3 phương trình của sơ đồ. Ý có $ac<0$ (ý b) dùng dòng "Ta có $ac=\ldots\ldots<0$ nên …".
- Ví dụ 2: đề "Cho phương trình $x^2-2x-5=0$ và $x_1$ là một nghiệm của phương trình. Viết $x_1^2$ và $x_1^3$ theo $x_1$." Lời giải: dòng hạ bậc, dòng bậc ba (khai triển đủ), "Vậy …". Ô ở $x_1^2$ và $x_1^3$.
- Bài 2 (NB, 3 ý): "Với mỗi phương trình sau, $x_1$ là một nghiệm. Điền vào chỗ chấm để viết $x_1^2$ và $x_1^3$ theo $x_1$ (làm đủ các bước như Ví dụ 2)." Mỗi ý: dòng "Vì $x_1$ là nghiệm của phương trình nên $\ldots\ldots=0$, tức là $x_1^2=\ldots\ldots$." và dòng "$x_1^3=x_1\cdot x_1^2=\ldots\ldots=\ldots\ldots$."
- Ví dụ 3: "Cho phương trình $x^2-6x+1=0$. Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức $G=x_1^2-6x_1+2026$." Lời giải: kiểm tra $\Delta'$, hạ bậc ra $x_1^2-6x_1=-1$, thay, Vậy.
- Bài 3 (NB, 2 ý): "Điền vào chỗ chấm để tính giá trị của mỗi biểu thức (làm đủ các bước như Ví dụ 3)." a) $K=x_1^2-5x_1+2021$ với $x^2-5x-4=0$; b) $L=x_1^3-2x_1+2024$ với $x^2-x-1=0$ (có thêm dòng bậc ba).
- Ví dụ 4: "Cho phương trình $x^2-5x-2=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức $P=x_1^2+5x_2-3$." Lời giải 5 dòng (Δ, Viète chỉ cần tổng, hạ bậc, thay số, Vậy).
- Bài 4 (NB, 2 ý): "Điền vào chỗ chấm để tính giá trị của mỗi biểu thức (làm đủ các bước như Ví dụ 4)." a) $M=x_1^2+4x_2+1$ với $x^2-4x-6=0$; b) $N=x_1^2+7x_2-10$ với $x^2-7x+4=0$.
- Bài 5 (NB, một bài, thẻ [NB] đầu đề): "Cho phương trình $x^2-2x-7=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Điền vào chỗ chấm để hoàn thành bài giải tính giá trị của biểu thức $B=x_1^2+2x_2+x_1x_2$." rồi khung đủ 5 dòng (Δ hoặc ac, Viète cả tổng và tích, hạ bậc, thay số, Vậy), mỗi dòng có chỗ chấm.
- Ví dụ 5: "Cho phương trình $x^2+6x+2=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Chứng tỏ hai nghiệm đều âm, rồi rút gọn $\sqrt{(x_1-1)^2}$." Lời giải: $\Delta'$, Viète, xét dấu, phá căn, Vậy.
- Bài 6 (NB, 2 ý): "Điền vào chỗ chấm để xét dấu hai nghiệm rồi rút gọn biểu thức (làm đủ các bước như Ví dụ 5)." a) $x^2+5x+3=0$, rút gọn $\sqrt{(x_1-2)^2}$; b) $x^2-9x+5=0$, rút gọn $\sqrt{(x_2+3)^2}$.

### Chặng "practice2" — title "Luyện tập 2 — Thông hiểu \& Vận dụng", number 4. Thứ tự: Ví dụ 6 → Bài 7. → Ví dụ 7 → Bài 8. → Ví dụ 8 → Bài 9. → Ví dụ 9 → Bài 10.
- Ví dụ 6: "Cho phương trình $x^2-3x-3=0$. Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức $H=x_1^3-12x_1+2000$."
- Bài 7 (TH, 2 ý, đề chung "Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức."): a) $x^2-x-3=0$, $E=x_1^3-4x_1+2030$; b) $x^2+2x-1=0$, $F=x_1^3-5x_1+2020$.
- Ví dụ 7: "Cho phương trình $x^2-8x+5=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức $P=x_1^2+8x_2-1$."
- Bài 8 (TH, 2 ý, đề chung "Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức."): a) $x^2-3x-6=0$, $M=x_1^2+3x_2+x_1x_2$; b) $x^2-9x+7=0$, $N=x_1^2+9x_2-20$.
- Ví dụ 8: "Cho phương trình $x^2+8x+3=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Chứng tỏ hai nghiệm đều âm, rồi tính giá trị của biểu thức $A=\sqrt{-12x_1+1}-x_2$." Lời giải: $\Delta'$, Viète, dấu, hạ bậc $x_1^2=-8x_1-3$ nên $-12x_1+1=x_1^2-4x_1+4=(x_1-2)^2$, phá căn $=2-x_1$ (vì $x_1<0$), $A=2-(x_1+x_2)=10$.
- Bài 9 (VD, một bài): "[VD] " + đề Tự Lập NGUYÊN VĂN + " \;(thi thử Vào 10, THCS Tự Lập)".
  Đề: ''' + DE_TU_LAP + r'''
- Ví dụ 9: "Cho phương trình $x^2-4x+1=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức $Q=\dfrac{4x_2-1}{x_1}+\dfrac{4x_1}{x_2}-x_1$." Lời giải: $\Delta'$, Viète ($x_1+x_2=4$, $x_1x_2=1$), hạ bậc $4x_2-1=x_2^2$ và $4x_1=x_1^2+1$, nên $Q=\dfrac{x_2^2}{x_1}+\dfrac{x_1^2+1}{x_2}-x_1=\dfrac{x_2^2}{x_1}+\dfrac{x_1^2}{x_2}+\dfrac{1}{x_2}-x_1$; vì $x_1x_2=1$ nên $\dfrac{1}{x_2}=x_1$; $Q=\dfrac{x_1^3+x_2^3}{x_1x_2}=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=64-12=52$.
- Bài 10 (VD, một bài, ĐÍCH): "[VD] " + đề 2026 NGUYÊN VĂN + " \;(đề chính thức Vào 10, Sở GD\&ĐT Hà Nội, 2026)".
  Đề: ''' + DE_2026 + r'''

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Ví dụ {i}." for i in range(1, 10)], *[f"Bài {i}." for i in range(1, 11)]) + "\n"

PROMPT_BTVN = CHUNG + r'''
## Việc C: dựng phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", Bài 11. đến Bài 20.)
Không có ví dụ, không tiêu đề mạch. Trả về MỘT stage {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[10 bài]} và "ghi_chu".
Các bài NB (11–16) là điền khuyết, mỗi ý theo đúng các dòng của ví dụ tương ứng trên lớp (ghi "(làm đủ các bước như Ví dụ N)"):
- Bài 11. NB 3 ý — viết tổng và tích (như Ví dụ 1). Ý có $ac<0$ (b) dùng dòng $ac$.
- Bài 12. NB 3 ý — viết $x_1^2$, $x_1^3$ theo $x_1$ (như Ví dụ 2).
- Bài 13. NB 3 ý — biểu thức chỉ chứa một nghiệm (như Ví dụ 3): a) $G=x_1^2-7x_1+2026$, b) $K=x_1^2-2x_1+2019$, c) $L=x_1^3-6x_1+2030$.
- Bài 14. NB 3 ý — biểu thức không đối xứng (như Ví dụ 4): a) $M=x_1^2+6x_2+3$, b) $N=x_1^2+10x_2-50$, c) $R=x_1^2+3x_2-2x_1x_2$.
- Bài 15. NB 2 ý — xét dấu rồi rút gọn căn (như Ví dụ 5).
- Bài 16. NB một bài — "Cho phương trình $x^2-6x-5=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Điền vào chỗ chấm để hoàn thành bài giải tính giá trị của biểu thức $B=x_1^2+6x_2+x_1x_2$." khung đủ 5 dòng có chỗ chấm.
Các bài tự trình bày:
- Bài 17. TH 3 ý (đề chung "Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức."): a) $E=x_1^3-5x_1+2021$, b) $F=x_1^3-10x_1+2000$, c) $H=x_1^3-18x_1+2017$.
- Bài 18. TH 3 ý (đề chung "Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức."): a) $M=x_1^2+7x_2+3x_1x_2$, b) $N=x_1^2-6x_2+1$, c) $T=2x_1^2+8x_2+3$.
- Bài 19. VD: "Cho phương trình $x^2+12x+5=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Chứng tỏ hai nghiệm đều âm, rồi tính giá trị của biểu thức $A=\sqrt{-18x_1+4}-x_2$." (lời giải: $-18x_1+4=x_1^2-6x_1+9=(x_1-3)^2$, phá căn $3-x_1$).
- Bài 20. VD: "Cho phương trình $x^2-5x+1=0$. Gọi $x_1$, $x_2$ là hai nghiệm của phương trình. Không giải phương trình, tính giá trị của biểu thức $Q=\dfrac{5x_2-1}{x_1}+\dfrac{5x_1}{x_2}-x_1$." (lời giải như Ví dụ 9 trên lớp, $Q=\dfrac{x_1^3+x_2^3}{x_1x_2}=110$).

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Bài {i}." for i in range(11, 21)]) + "\n"


def ban_cu():
    f = json.loads((REPO / SEED).read_text())
    st = {s["kind"]: s for s in f["stages"]}
    return json.dumps({"review": st["review"]["blocks"], "concept": st["concept"]["blocks"],
                       "mindmap": [b for b in st["reflection"]["blocks"] if b.get("type") == "mindmap"]},
                      ensure_ascii=False, indent=1)


def main():
    viec = [(VID_LT, PROMPT_LT + ban_cu() + "\n", "scripts/gemini/schema/ly-thuyet-phieu.json"),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/dung-chang-phieu.json"),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/dung-chang-phieu.json")]
    for vid, prompt, schema in viec:
        v = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": prompt, "files": [], "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-phieu-d", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
