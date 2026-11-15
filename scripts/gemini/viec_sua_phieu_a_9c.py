#!/usr/bin/env python3
"""Sửa phiếu A ch.VI 9C (13/11/2026) — "Bài 19. Phương trình bậc hai một ẩn".

Lỗi bản cũ: dan_dat_gate chặn (điền khuyết đứng sau tự trình bày, 6 chỗ); 10 ví dụ chưa điền khuyết, nhiều ví dụ
chép y phương trình của bài (VD2 = Bài 5a, VD3 = Bài 6a, VD6 = Bài 7a…), phương trình lặp giữa các bài (Bài 2a = 14a,
Bài 9a = 15a…); lý thuyết có hộp trap "lỗi mất điểm oan" + target "Câu III.3"; "hôm nay"; ~100 dấu ";";
TH thiếu hints; chưa tách phiếu BTVN.
Đề + đáp số: Claude chọn, kiểm SymPy ở so_do_phieu_a_9c.py. Gemini chỉ viết chữ.

    python3 scripts/gemini/viec_sua_phieu_a_9c.py
    python3 scripts/gemini/tho.py --tien-to sua-9c-ch6-phieu-a- --song-song 3
    python3 scripts/gemini/lap_sua_phieu_a_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_phieu_a_9c import tom_tat  # noqa: E402

SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-a-phuong-trinh-bac-hai-mot-an.json"
VID_LT, VID_LOP, VID_BTVN = "sua-9c-ch6-phieu-a-lt", "sua-9c-ch6-phieu-a-lop", "sua-9c-ch6-phieu-a-btvn"

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, Bài 19 "Phương trình bậc hai một ẩn", SGK Kết nối tri thức, Toán 9 tập hai tr.10–16) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). KHÔNG có tham số $m$. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật cứng (vi phạm bị trả lại)
- CẤM chữ/ý: "khuôn", "Câu III", "đề Vào 10 hỏi", điểm số, "mất điểm", "thang điểm", "tầng C", "mẹo", "chìa khóa", "nhanh nhất", "ăn may". Trích nguồn đề trong ngoặc sau đề bài thì GIỮ (đã ghi sẵn ở sơ đồ).
- CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "ép", "nhé", "vừa khít". Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác" — dùng "nên", "$\Rightarrow$", "$\Leftrightarrow$" hoặc xuống dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Hai nghiệm viết "$x_1=…$ và $x_2=…$". Ba hệ số viết "$a=2$, $b=-5$, $c=2$".
- Câu dẫn đề TỰ SOẠN: "Giải phương trình …", "Cho phương trình …". KHÔNG nói trước số nghiệm.
- Lời giải theo NHỊP BÀI THI, đúng cách trình bày SGK, mỗi bước một dòng [[br]], ví dụ và khung điền thụt "\hspace*{1.4em}", "Vậy …" dòng riêng ở cuối. Mẫu theo loại (số chỉ minh họa):
  [heso]  "$(x+1)(x-4)=2x$[[br]]$\Leftrightarrow x^2-3x-4=2x$[[br]]$\Leftrightarrow x^2-5x-4=0$.[[br]]Vậy phương trình đã cho là phương trình bậc hai với $a=1$, $b=-5$, $c=-4$."
          trường hợp mất $x^2$: "… $\Leftrightarrow -x-7=0$.[[br]]Vậy phương trình đã cho không phải là phương trình bậc hai (sau khi thu gọn không còn hạng tử chứa $x^2$)."
  [kc]    "$4x^2+6x=0$[[br]]$\Leftrightarrow 2x(2x+3)=0$[[br]]$\Leftrightarrow x=0$ hoặc $2x+3=0$[[br]]$\Leftrightarrow x=0$ hoặc $x=-\dfrac{3}{2}$.[[br]]Vậy phương trình có hai nghiệm $x_1=0$ và $x_2=-\dfrac{3}{2}$."
  [kb]    "$2x^2-18=0$[[br]]$\Leftrightarrow x^2=9$[[br]]$\Leftrightarrow x=3$ hoặc $x=-3$.[[br]]Vậy phương trình có hai nghiệm $x_1=3$ và $x_2=-3$."
          vô nghiệm: "$x^2+4=0 \Leftrightarrow x^2=-4$.[[br]]Vì $x^2\ge 0$ với mọi $x$ mà $-4<0$ nên phương trình vô nghiệm."
  [delta] "Ta có $a=2$, $b=-5$, $c=2$.[[br]]$\Delta=b^2-4ac=(-5)^2-4\cdot 2\cdot 2=25-16=9>0$.[[br]]Vì $\Delta>0$ nên phương trình có hai nghiệm phân biệt[[br]]$x_1=\dfrac{-b+\sqrt{\Delta}}{2a}=\dfrac{5+3}{4}=2$ và $x_2=\dfrac{-b-\sqrt{\Delta}}{2a}=\dfrac{5-3}{4}=\dfrac{1}{2}$.[[br]]Vậy phương trình có hai nghiệm $x_1=2$ và $x_2=\dfrac{1}{2}$."
          (nghiệm chứa căn thì GIỮ căn, rút gọn nếu được, không làm tròn: $x_1=\dfrac{3+\sqrt{13}}{2}$)
  [so_ng] "Ta có $a=9$, $b=-6$, $c=1$.[[br]]$\Delta=(-6)^2-4\cdot 9\cdot 1=0$.[[br]]Vì $\Delta=0$ nên phương trình có nghiệm kép $x_1=x_2=-\dfrac{b}{2a}=\dfrac{6}{18}=\dfrac{1}{3}$." / "… $\Delta=1^2-4\cdot 1\cdot 3=-11<0$.[[br]]Vì $\Delta<0$ nên phương trình vô nghiệm."
  [dphay] "Ta có $a=1$, $b'=-4$, $c=12$.[[br]]$\Delta'=b'^2-ac=(-4)^2-1\cdot 12=4>0$.[[br]]Vì $\Delta'>0$ nên phương trình có hai nghiệm phân biệt[[br]]$x_1=\dfrac{-b'+\sqrt{\Delta'}}{a}=\dfrac{4+2}{1}=6$ và $x_2=\dfrac{-b'-\sqrt{\Delta'}}{a}=\dfrac{4-2}{1}=2$.[[br]]Vậy …"
  [giai]  tự chọn cách: chuyển vế, thu gọn về $ax^2+bx+c=0$ rồi trình bày như [delta] hoặc [dphay] ($b$ chẵn thì dùng $\Delta'$).
  [tt]    (phương trình đã cho sẵn) giải như [dphay]/[delta] → "Vì $x>0$ nên loại $x_2=-36$, nhận $x=30$." → tính đại lượng đề hỏi → "Vậy …".
          (học sinh tự lập phương trình) "Gọi chiều rộng là $x$ (m, $x>0$).[[br]]Chiều dài là $x+11$ (m).[[br]]Vì diện tích là $180$ m$^2$ nên ta có phương trình $x(x+11)=180$[[br]]$\Leftrightarrow x^2+11x-180=0$.[[br]]…giải…[[br]]Vì $x>0$ nên nhận $x=9$, loại $x=-20$.[[br]]Chiều dài là $9+11=20$ (m).[[br]]Vậy …"
- Thẻ mức đặt ở ĐẦU MỖI Ý: "a) [NB] …". Bài một ý thì thẻ "[TH]"/"[VD]"/"[NB]" đứng đầu đề. Không gắn thẻ ở cả đề lẫn ý.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". MỌI dấu $ mở phải có $ đóng — soát từng dòng.
- Phương trình, hệ số, $\Delta$, nghiệm ở mục "Sơ đồ đề và đáp số" ĐÃ ĐƯỢC MÁY KIỂM (SymPy) — dùng đúng, KHÔNG đổi phương trình, KHÔNG thêm phương trình mới. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số.

## Khuôn khối (JSON)
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"}
- Ví dụ (giáo viên làm cùng lớp, có ô điền): {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …"}
  Ví dụ nhiều ý: "a)" "b)" đầu dòng riêng trong Lời giải. Trong Lời giải khoét 3–6 ô bằng [[fill:đáp án]] ở chỗ then chốt (hệ số sau thu gọn, giá trị $\Delta$, nghiệm, CÂU KẾT LUẬN "Vậy" phải có ô). Ô trong $…$ thì đáp án KHÔNG bọc $ (ví dụ "$\Delta=[[fill:9]]>0$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong (ví dụ "[[fill:$x_1=2$ và $x_2=\dfrac{1}{2}$]]"). KHÔNG để số vừa nằm trong ô lại in sẵn ở dòng dưới hoặc ở đề (lộ đáp án).
- Bài NB điền khuyết = BÀI TRÌNH BÀY HOÀN CHỈNH theo đúng các dòng của ví dụ đứng trước, chỗ HS điền ghi "\\ldots\\ldots". Đề luôn mở bằng: "Điền vào chỗ chấm để hoàn thành bài giải (làm đủ các bước như Ví dụ N)." rồi từng ý:
"a) [NB] $x^2-3x+2=0$[[br]]\\hspace*{1.4em}Ta có $a=\\ldots\\ldots$, $b=\\ldots\\ldots$, $c=\\ldots\\ldots$.[[br]]\\hspace*{1.4em}$\\Delta=b^2-4ac=\\ldots\\ldots=\\ldots\\ldots$.[[br]]\\hspace*{1.4em}Vì $\\Delta\\ldots\\ldots 0$ nên phương trình có hai nghiệm phân biệt[[br]]\\hspace*{1.4em}$x_1=\\ldots\\ldots$ và $x_2=\\ldots\\ldots$.[[br]]\\hspace*{1.4em}Vậy \\ldots\\ldots\\ldots\\ldots[[br]]b) [NB] …"
  Mỗi ý ≥ 3 chỗ chấm, chỗ chấm rơi vào CHỖ PHẢI SUY RA (hệ số, giá trị, nghiệm, kết luận), không rơi vào chữ in sẵn ở dòng khác. Ý nào kết quả khác ví dụ (vô nghiệm, không phải phương trình bậc hai, nghiệm kép) thì KHÔNG in sẵn chữ "vô nghiệm"/"nghiệm kép"/"không phải" — để chỗ chấm cho HS tự kết luận (ví dụ "Vì $\\Delta\\ldots\\ldots 0$ nên phương trình \\ldots\\ldots\\ldots\\ldots"). "solution": lời giải đầy đủ từng ý (a) …[[br]]\\hspace*{1.4em}…[[br]]b) …), điền hết các chỗ chấm.
- Bài TH, VD (tự trình bày): "statement" chỉ có ĐỀ, không chỗ chấm, không khung. "solution": lời giải đầy đủ theo nhịp bài thi. "hints": 1–2 câu hỏi gợi ý kiểu Polya ("Phương trình đã ở dạng $ax^2+bx+c=0$ chưa?", "Hệ số $b$ là số chẵn hay lẻ?", "Đại lượng chưa biết là gì, nó phải thỏa điều kiện nào?") — hỏi, KHÔNG gọi tên công thức, không lộ số, không làm hộ.
- Khối bài: {"type":"problem","label":"Bài N.","level":1|2|3,"tier":"onclass"|"btvn","statement":…,"solution":…,"hints":[…]} (NB level 1 để "hints": []).
'''


def so_do(*nhan):
    tt, trung = tom_tat()
    assert not trung, trung
    return "\n".join(f"- {k}\n" + "\n".join("    " + d for d in tt[k]) for k in nhan)


PROMPT_LT = CHUNG + r'''
## Việc A: viết phần mở đầu, nhắc lại, lý thuyết, sơ đồ tư duy, ghi chú giáo viên
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap","teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

1. "opener_text" (chặng Khám phá): sửa nhẹ đoạn mở đầu cũ (ở cuối prompt) — giữ tình huống mảnh đất của bạn Minh (chiều rộng ngắn hơn chiều dài $11$ m, diện tích $180$ m$^2$), giữ phương trình $x^2+11x-180=0$, giữ ý thử số mất công. Bỏ "vừa khít", bỏ dấu ";", không xưng hô. Kết bằng câu: cần một cách giải mọi phương trình dạng $ax^2+bx+c=0$ — Bài 10 cuối phiếu giải trọn bài toán này.
2. "review_note" (khối "Nhắc lại kiến thức Lớp 8"): hai kĩ năng, mỗi kĩ năng một tiêu đề in đậm + 2 dòng ví dụ:
   (1) Khai triển, thu gọn: $(x-3)(x+2)=x^2-x-6$ và $(x+5)^2=x^2+10x+25$ (viết đủ bước khai triển).
   (2) Phương trình tích: $A\cdot B=0 \Leftrightarrow A=0$ hoặc $B=0$, ví dụ $(x+6)(2x-5)=0 \Leftrightarrow x=-6$ hoặc $x=\dfrac{5}{2}$. Và $A^2=B$ ($B\ge 0$) thì $A=\sqrt{B}$ hoặc $A=-\sqrt{B}$, ví dụ $x^2=16 \Leftrightarrow x=4$ hoặc $x=-4$.
   Dòng cách nhau [[br]], thụt "\quad". Không dấu ";".
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT, đúng chữ SGK Bài 19, mục đánh số "\textbf{N. Tên}" (một khối para tiêu đề + một khối para nội dung), 5 mục:
   1. Định nghĩa — đúng chữ SGK tr.10: "Phương trình bậc hai một ẩn (nói gọn là phương trình bậc hai) là phương trình có dạng $ax^2+bx+c=0$, trong đó $x$ là ẩn, $a$, $b$, $c$ là những số cho trước gọi là hệ số và $a\ne 0$." Thêm một dòng: phương trình chưa ở dạng này thì chuyển vế, thu gọn rồi mới chỉ ra $a$, $b$, $c$.
   2. Phương trình bậc hai dạng khuyết — SGK tr.11: khuyết $c$ ($c=0$): đặt nhân tử chung đưa về phương trình tích $x(ax+b)=0$. Khuyết $b$ ($b=0$): đưa về $x^2=k$ (hoặc vế trái là một bình phương), dùng "Nếu $A^2=B$ ($B\ge 0$) thì $A=\sqrt{B}$ hoặc $A=-\sqrt{B}$". Nếu $k<0$ thì phương trình vô nghiệm.
   3. Công thức nghiệm — đúng khung SGK tr.13: "Xét phương trình bậc hai một ẩn $ax^2+bx+c=0$ ($a\ne 0$). Tính biệt thức $\Delta=b^2-4ac$." ba gạch đầu dòng $\Delta>0$ (hai nghiệm phân biệt $x_1=\dfrac{-b+\sqrt{\Delta}}{2a}$, $x_2=\dfrac{-b-\sqrt{\Delta}}{2a}$), $\Delta=0$ (nghiệm kép $x_1=x_2=-\dfrac{b}{2a}$), $\Delta<0$ (vô nghiệm). Nhận xét: nếu $a$ và $c$ trái dấu thì $ac<0$ nên $\Delta=b^2-4ac>0$, phương trình có hai nghiệm phân biệt.
   4. Công thức nghiệm thu gọn — SGK tr.14: với $b=2b'$, $\Delta'=b'^2-ac$, ba trường hợp $\Delta'>0$ ($x_1=\dfrac{-b'+\sqrt{\Delta'}}{a}$, $x_2=\dfrac{-b'-\sqrt{\Delta'}}{a}$), $\Delta'=0$ ($x_1=x_2=-\dfrac{b'}{a}$), $\Delta'<0$ (vô nghiệm).
   5. Tìm nghiệm bằng máy tính cầm tay — SGK tr.15: sau khi mở máy bấm MODE 5 3 để chuyển về chế độ giải phương trình bậc hai, nhập lần lượt $a$, $b$, $c$ (mỗi số bấm =), máy hiện $x_1$, bấm = hiện $x_2$. Dùng để kiểm tra lại nghiệm, bài thi vẫn phải trình bày lời giải.
   Mỗi gạch đầu dòng viết "$\bullet$\; …", xuống dòng bằng [[br]]. KHÔNG thêm khối trap, target, lỗi hay gặp, cấu trúc đề thi.
4. "mindmap": {"type":"mindmap","caption":"Điền các ô trống để tự tóm tắt cả buổi","root":"Phương trình bậc hai $ax^2+bx+c=0$ ($a\ne 0$)","branches":[4 nhánh: "Dạng khuyết" (con: khuyết $c$: $x(ax+b)=[[blank:1cm]]$, khuyết $b$: $x^2=[[blank:1.2cm]]$), "Công thức nghiệm" (con: $\Delta=[[blank:2cm]]$, $\Delta>0$: $x_{1,2}=[[blank:2.4cm]]$, $\Delta<0$: [[blank:2cm]]), "Công thức nghiệm thu gọn" (con: $b=2b'$, $\Delta'=[[blank:2cm]]$), "Nhận xét" (con: $ac<0$ thì phương trình [[blank:3cm]])]}. Mỗi nhánh {"label":…,"children":[{"label":…}]}.
5. "teacher_notes" (ghi chú giáo viên, ngắn, chỉ cách tổ chức dạy, không "khuôn"/điểm số/"hôm nay"):
   review: mở màn khoảng 8 phút, cho học sinh thử vài giá trị của $x$ để thấy đoán nghiệm mất công, nhắc nhanh hai kĩ năng Lớp 8 trên bảng.
   concept: giảng khoảng 25 phút theo thứ tự mục 1 → 5, mục 5 cho học sinh bấm máy kiểm tra một phương trình.
   practice1: khoảng 55 phút, 4 mạch, mỗi mạch giáo viên làm ví dụ cùng lớp (điền ô) rồi học sinh điền bài ngay sau. Mạch 3 nhấn đọc to "$b$ bình phương trừ bốn $a$ $c$" rồi mới thay số, chú ý dấu khi $b$ hoặc $c$ âm.
   practice2: khoảng 55 phút, Bài 7–8 học sinh tự trình bày (gọi lên bảng theo cặp), Ví dụ 8 → Bài 9 phương trình cho sẵn, Ví dụ 9 → Bài 10 học sinh tự lập phương trình. Bài 10 là đích của buổi, chính là bài toán mở đầu.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 11–20 in thành phiếu riêng, khoảng 85 phút. Buổi sau chữa Bài 17 và Bài 20 trước.

## Đoạn mở đầu cũ (sửa theo mục 1)
'''

PROMPT_LOP = CHUNG + r'''
## Việc B: dựng 2 chặng LUYỆN TẬP trên lớp
Đầu ra JSON {"stages":[{"kind":"practice1",…},{"kind":"practice2",…}],"ghi_chu"}. Mỗi stage có "kind","number","title","teacher_note","blocks" (teacher_note để chuỗi rỗng — máy tự điền).

### Chặng "practice1" — title "Luyện tập 1 — Nhận biết", number 3. Thứ tự khối:
- {"type":"para","text":"\\textbf{Đích của buổi học:} Bài 10 — lập và giải phương trình bậc hai để tìm kích thước mảnh đất (bộ đề Vào 10, Phòng GD\\&ĐT Đống Đa). Mạch 1 luyện bước đưa phương trình về dạng $ax^2+bx+c=0$, Mạch 3 và Mạch 4 luyện hai công thức giải, Mạch 2 giải nhanh các phương trình khuyết."}
- heading "Mạch 1. Đưa về dạng $ax^2+bx+c=0$ và chỉ ra hệ số" → Ví dụ 1 → Bài 1.
- heading "Mạch 2. Phương trình bậc hai dạng khuyết" → Ví dụ 2 → Bài 2. → Ví dụ 3 → Bài 3.
- heading "Mạch 3. Công thức nghiệm" → Ví dụ 4 → Bài 4. → Ví dụ 5 → Bài 5.
- heading "Mạch 4. Công thức nghiệm thu gọn" → Ví dụ 6 → Bài 6.
Yêu cầu từng khối (phương trình lấy ĐÚNG sơ đồ):
- Ví dụ 1: "Mỗi phương trình sau có phải là phương trình bậc hai một ẩn không? Nếu có, chỉ ra các hệ số $a$, $b$, $c$." a), b) theo sơ đồ, lời giải kiểu [heso].
- Bài 1 (NB, 3 ý, khung [heso], ghi nguồn sau phương trình dạng " \;(Giữa kì I, THCS Nguyễn Du)"). Ý c sau khi thu gọn không còn $x^2$ — khung để chỗ chấm cho kết luận, không in sẵn "không phải".
- Ví dụ 2 (giải phương trình khuyết $c$) → Bài 2 (NB, 3 ý, khung [kc]).
- Ví dụ 3 (giải hai phương trình khuyết $b$, ý b vô nghiệm) → Bài 3 (NB, 3 ý, khung [kb], ý c vô nghiệm — để chỗ chấm kết luận).
- Ví dụ 4 (giải bằng công thức nghiệm, kiểu [delta]) → Bài 4 (NB, 3 ý, khung [delta], ý c nghiệm chứa căn).
- Ví dụ 5: "Tính $\Delta$ rồi giải các phương trình sau." a) nghiệm kép, b) vô nghiệm, kiểu [so_ng] → Bài 5 (NB, 3 ý, khung [so_ng]: dòng hệ số, dòng $\Delta$, dòng "Vì $\Delta\ldots\ldots 0$ nên phương trình \ldots\ldots").
- Ví dụ 6 (công thức nghiệm thu gọn, kiểu [dphay]) → Bài 6 (NB, 3 ý, khung [dphay]: dòng $a$, $b'$, $c$, dòng $\Delta'$, dòng nghiệm, Vậy).

### Chặng "practice2" — title "Luyện tập 2 — Thông hiểu \& Vận dụng", number 4. Thứ tự: Ví dụ 7 → Bài 7. → Bài 8. → Ví dụ 8 → Bài 9. → Ví dụ 9 → Bài 10.
- Ví dụ 7: "Giải phương trình $x(x+4)=2x+15$." (khai triển, chuyển vế, thu gọn, rồi $\Delta'$).
- Bài 7 (TH, 3 ý, "Giải các phương trình sau."), nguồn theo sơ đồ. Ý b nghiệm chứa căn, ý c dùng $\Delta'$.
- Bài 8 (TH, 2 ý, "Đưa về dạng $ax^2+bx+c=0$ rồi giải các phương trình sau.").
- Ví dụ 8 (đề thật, phương trình cho sẵn): "Hằng ngày bạn Nam đi học trên quãng đường $12$ km. Một hôm Nam tăng vận tốc thêm $6$ km/h nên đến trường sớm hơn thường ngày $4$ phút. Gọi vận tốc thường ngày của Nam là $x$ (km/h, $x>0$) thì lập được phương trình $x^2+6x-1080=0$. Giải phương trình rồi cho biết vận tốc của Nam hôm tăng tốc. Với vận tốc đó Nam có vượt quá $40$ km/h không? (trích đề thi thử Vào 10, THCS Tự Lập)" — lời giải: $\Delta'=1089$, $x_1=30$, $x_2=-36$ loại, $30+6=36<40$.
- Bài 9 (VD, một bài): "[VD] Để chở hết $60$ tấn hàng, một đội xe dự định dùng một số xe cùng loại. Trước khi khởi hành có hai xe được điều đi làm việc khác nên mỗi xe còn lại phải chở nhiều hơn dự định $1$ tấn. Gọi số xe dự định là $x$ (xe, $x$ nguyên và $x>2$) thì lập được phương trình $x^2-2x-120=0$. Giải phương trình, đối chiếu điều kiện rồi cho biết lúc đầu đội dự định dùng bao nhiêu xe. \;(thi thử Vào 10 lần 4, Phòng GD\&ĐT Chương Mỹ)"
- Ví dụ 9 (HS xem cách tự lập phương trình): "Tìm hai số tự nhiên chẵn liên tiếp, biết tích của chúng bằng $168$." Lời giải: gọi số chẵn nhỏ là $x$ ($x$ chẵn, $x\ge 0$), số kia $x+2$, phương trình $x(x+2)=168 \Leftrightarrow x^2+2x-168=0$, $\Delta'=169$, $x_1=12$, $x_2=-14$ loại, Vậy hai số là $12$ và $14$.
- Bài 10 (VD, một bài, ĐÍCH): "[VD] Một mảnh đất hình chữ nhật có chiều rộng ngắn hơn chiều dài $11$ m và diện tích bằng $180$ m$^2$. Gọi chiều rộng mảnh đất là $x$ (m, $x>0$). Biểu diễn chiều dài theo $x$, lập phương trình rồi tìm chiều rộng và chiều dài của mảnh đất. \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)" — lời giải kiểu [tt] tự lập, $\Delta=841$, $x_1=9$, $x_2=-20$ loại, rộng $9$ m, dài $20$ m.

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Ví dụ {i}." for i in range(1, 10)], *[f"Bài {i}." for i in range(1, 11)]) + "\n"

PROMPT_BTVN = CHUNG + r'''
## Việc C: dựng phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", Bài 11. đến Bài 20.)
Không có ví dụ, không tiêu đề mạch. Trả về MỘT stage {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[10 bài]} và "ghi_chu".
Các bài NB (11–16) là khung điền khuyết, mỗi ý theo đúng các dòng của ví dụ tương ứng trên lớp (đề mở bằng "Điền vào chỗ chấm để hoàn thành bài giải (làm đủ các bước như Ví dụ N)."):
- Bài 11. NB 3 ý — khung [heso] (như Ví dụ 1). Ý c sau khi thu gọn không còn $x^2$ — để chỗ chấm kết luận.
- Bài 12. NB 2 ý — khung [kc] (như Ví dụ 2).
- Bài 13. NB 3 ý — khung [kb] (như Ví dụ 3), ý c vô nghiệm — để chỗ chấm kết luận.
- Bài 14. NB 3 ý — khung [delta] (như Ví dụ 4).
- Bài 15. NB 3 ý — khung [so_ng] (như Ví dụ 5).
- Bài 16. NB 3 ý — khung [dphay] (như Ví dụ 6).
Các bài tự trình bày (statement chỉ có đề, có "hints"):
- Bài 17. TH 3 ý: "Giải các phương trình sau." (như Bài 7).
- Bài 18. TH 2 ý: "Đưa về dạng $ax^2+bx+c=0$ rồi giải các phương trình sau." (như Bài 8).
- Bài 19. VD: "[VD] Một ô tô dự định đi quãng đường dài $100$ km. Nếu mỗi giờ ô tô đi nhanh hơn dự định $10$ km thì sẽ đến nơi sớm hơn dự định $30$ phút. Gọi vận tốc dự định của ô tô là $x$ (km/h, $x>0$) thì lập được phương trình $x^2+10x-2000=0$. Giải phương trình, đối chiếu điều kiện rồi cho biết vận tốc dự định của ô tô." — $\Delta'=2025$, $x_1=40$, $x_2=-50$ loại.
- Bài 20. VD: "[VD] Một khu vườn hình chữ nhật có chu vi $50$ m và diện tích $150$ m$^2$. Gọi chiều rộng khu vườn là $x$ (m). Biểu diễn chiều dài theo $x$, lập phương trình rồi tìm các kích thước của khu vườn." — nửa chu vi $25$, chiều dài $25-x$, $x(25-x)=150 \Leftrightarrow x^2-25x+150=0$, $\Delta=25$, $x_1=15$, $x_2=10$. Hai nghiệm đều thỏa $0<x<25$: nếu $x=15$ thì chiều dài $10<15$ (trái với chiều rộng nhỏ hơn chiều dài) nên chiều rộng $10$ m, chiều dài $15$ m. Viết lời giải gọn: "Vì chiều rộng nhỏ hơn chiều dài nên $x<25-x$, tức là $x<12{,}5$" đặt NGAY ở dòng gọi ẩn ($0<x<12{,}5$), rồi nhận $x=10$, loại $x=15$.

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Bài {i}." for i in range(11, 21)]) + "\n"


def ban_cu():
    f = json.loads((REPO / SEED).read_text())
    st = {s["kind"]: s for s in f["stages"]}
    return next(b["text"] for b in st["review"]["blocks"] if b.get("type") == "opener") + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT + ban_cu(), "scripts/gemini/schema/ly-thuyet-phieu.json"),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/dung-chang-phieu.json"),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/dung-chang-phieu.json")]
    for vid, prompt, schema in viec:
        v = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": prompt, "files": [], "schema": schema,
             "timeout": "1800s", "meta": {"loai": "sua-phieu-a", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
