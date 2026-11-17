#!/usr/bin/env python3
"""Sinh việc Gemini: KHỬ TRÙNG ĐỀ phiếu F (luyện tập chung) ch.VI 9C — 15/11/2026.

Soát 15/11: ví dụ F lặp phiếu C/D (VD1 = D Bài 4c, VD2 = C VD5, VD4 = C VD1, VD7 = C Bài 7a) và 14 ý
không nguồn trùng phương trình phiếu A–D / đề 15 phút. Ý có trích nguồn đề thật GIỮ (Bài 10a, 10b, 13,
21a, 22b, 23b, 25, 26). Claude chốt bảng thay (SymPy: scripts/gemini/so_do_phieu_f_9c_khu_trung.py),
Gemini viết lại chữ của đúng các khối đó.

    .venv/bin/python scripts/gemini/so_do_phieu_f_9c_khu_trung.py      (kiểm sơ đồ)
    .venv/bin/python scripts/gemini/viec_khu_trung_phieu_f_9c.py
    python3 scripts/gemini/tho.py --mot khu-trung-9c-ch6-phieu-f
    python3 scripts/gemini/ap_sua_phieu.py khu-trung-9c-ch6-phieu-f [--ghi]
    .venv/bin/python scripts/gemini/viec_khu_trung_phieu_f_9c.py --sau [--ghi]   (check, hints Bài 25, ghi chú GV)
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from so_do_phieu_f_9c_khu_trung import main as kiem_so_do  # noqa: E402

SEED = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-f-luyen-tap-chung-va-bai-tap-cuoi-chuong-vi.json"
VID = "khu-trung-9c-ch6-phieu-f"
LABELS = ["Ví dụ 1.", "Ví dụ 2.", "Ví dụ 4.", "Ví dụ 7.", "Bài 1.", "Bài 2.", "Bài 3.", "Bài 4.", "Bài 8.", "Bài 9.",
          "Bài 11.", "Bài 12.", "Bài 15.", "Bài 16.", "Bài 17.", "Bài 21.", "Bài 22.", "Bài 24."]
VID_B = VID + "-loi-van"
LABELS_B = ["Bài 6.", "Bài 7.", "Bài 10.", "Bài 13.", "Bài 19.", "Bài 20.", "Bài 25.", "Bài 26."]

PROMPT = r'''Bạn là thợ sửa phiếu học tập Toán 9 (phiếu luyện tập chung cuối chương VI: phương trình bậc hai, định lí Viète, phương trình chứa ẩn ở mẫu; học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: toàn bộ dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt (trích từ seed phiếu). Mỗi khối có "label", "statement", "solution" (riêng "Ví dụ N." chỉ có "statement" = toàn bộ chữ ví dụ kèm lời giải mẫu). Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; giữ escape \& nếu có.

## Vì sao phải sửa
Phiếu bị TRÙNG ĐỀ với các phiếu khác cùng chương: nhiều ví dụ và ý bài dùng lại đúng phương trình của phiếu khác. Giáo viên đã chọn phương trình MỚI cho từng ý (bảng dưới, mọi con số đã kiểm bằng máy).
   Việc của bạn: thay phương trình ở đúng các ý đó và viết lại các con số đi kèm (dòng điều kiện $\Delta$/$\Delta'$/$ac$, tổng, tích, phép tính, đáp số) trong statement và solution.
   MỌI CHỮ KHÁC GIỮ NGUYÊN Y HỆT: câu dẫn, khung chỗ chấm \ldots\ldots, thẻ [NB]/[TH]/[VD], cách xuống dòng [[br]]\hspace*{1.4em}, tiêu đề "Lời giải", các ý KHÔNG có trong bảng (giữ từng chữ, kể cả chú thích nguồn đề).

## Bảng thay (bất di bất dịch — không đổi số). Mỗi dòng ghi đủ các con số phải xuất hiện.
1. Ví dụ 1 (tính $x_1^2+x_2^2$): $x^2-6x+2=0$ → $x^2-8x+4=0$. $\Delta'=(-4)^2-1\cdot 4=12>0$. Viète: $x_1+x_2=8$, $x_1x_2=4$. $x_1^2+x_2^2=8^2-2\cdot 4=56$. Vậy $x_1^2+x_2^2=56$.
2. Ví dụ 2 (hạ bậc): $x^2-2x-4=0$ → $x^2-x-7=0$. $x_1^2-x_1-7=0$, suy ra $x_1^2=x_1+7$. $x_1^3=x_1\cdot x_1^2=x_1(x_1+7)=x_1^2+7x_1$ [[br]] $=(x_1+7)+7x_1=8x_1+7$. Vậy $x_1^2=x_1+7$ và $x_1^3=8x_1+7$.
3. Ví dụ 4 (tính $x_1^2x_2+x_1x_2^2$): $x^2-5x-3=0$ → $x^2-6x-4=0$. $ac=1\cdot(-4)=-4<0$. Viète: $x_1+x_2=6$, $x_1x_2=-4$. $x_1^2x_2+x_1x_2^2=x_1x_2(x_1+x_2)=(-4)\cdot 6=-24$.
4. Ví dụ 7 (tính $A$): $x^2-3x-1=0$, $A=x_1^2+3x_2$ → $x^2-5x-8=0$, $A=x_1^2+5x_2$. $ac=1\cdot(-8)=-8<0$. $x_1^2-5x_1-8=0$, suy ra $x_1^2=5x_1+8$. $A=x_1^2+5x_2=5x_1+8+5x_2=5(x_1+x_2)+8$. Viète: $x_1+x_2=5$. $A=5\cdot 5+8=33$. Vậy $A=33$.
5. Bài 1 ý a) CHỈ: $x^2-10x+9=0$ → $3x^2+8x-3=0$ \;(SGK Toán 9 tập hai, Bài 19, Luyện tập 6) — thêm đúng chú thích nguồn này ngay sau phương trình. Lời giải: "Ta có $b=8$ là số chẵn." / "Vậy dùng $\Delta'$ với $b'=4$." Ý b) giữ nguyên.
6. Bài 2 ý a) CHỈ: $x^2-3x+2=0$ → $3x^2-x-2=0$. Lời giải: $a+b+c=3-1-2=0$ và $a-b+c=3+1-2=2$. Vậy phương trình có hai nghiệm $x_1=1$ và $x_2=-\dfrac{2}{3}$. Ý b) giữ nguyên.
7. Bài 3: $x^2-4x+1=0$ → $x^2-10x+5=0$. $\Delta'=(-5)^2-1\cdot 5=20>0$. Viète: $x_1+x_2=10$, $x_1x_2=5$. a) $x_1^2+x_2^2=10^2-2\cdot 5=90$. b) $x_1x_2=5\ne 0$; $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{x_1+x_2}{x_1x_2}=\dfrac{10}{5}=2$.
8. Bài 4 (hạ bậc): $x^2-5x+3=0$ → $x^2-3x-7=0$. a) $x_1^2-3x_1-7=0$, vậy $x_1^2=3x_1+7$. b) $x_1^3=x_1\cdot x_1^2=x_1(3x_1+7)=3x_1^2+7x_1$ [[br]] $=3(3x_1+7)+7x_1=16x_1+21$. Vậy $x_1^3=16x_1+21$.
9. Bài 8: $\dfrac{x+1}{x-1}-\dfrac{1}{x+1}=\dfrac{4}{x^2-1}$ → $\dfrac{x+2}{x-1}-\dfrac{1}{x+1}=\dfrac{6}{x^2-1}$. Lời giải: $x^2-1=(x-1)(x+1)$ nên điều kiện xác định là $x\ne 1$ và $x\ne -1$. Khử mẫu: $(x+2)(x+1)-(x-1)=6$ [[br]] $x^2+3x+2-x+1=6$ [[br]] $x^2+2x-3=0$.
   Ta có $a+b+c=1+2-3=0$ nên $x_1=1$ và $x_2=\dfrac{c}{a}=-3$. $x_1=1$ không thỏa mãn điều kiện xác định nên loại. $x_2=-3$ thỏa mãn điều kiện xác định. Vậy phương trình có nghiệm $x=-3$.
10. Bài 9 ý a) CHỈ: $x^2-8x+3=0$ → $x^2+6x+4=0$ (vẫn tính $x_1^2+x_2^2$). $\Delta'=3^2-1\cdot 4=5>0$. Viète: $x_1+x_2=-6$, $x_1x_2=4$. $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=(-6)^2-2\cdot 4=28$. Ý b) giữ nguyên.
11. Bài 11: $x^2-8x+c=0$, $x_1=4-\sqrt5$ → $x^2-10x+c=0$, $x_1=5-\sqrt3$. Viète: $x_1+x_2=10$, $x_1x_2=c$. $x_2=10-x_1=10-(5-\sqrt3)=5+\sqrt3$. $c=x_1x_2=(5-\sqrt3)(5+\sqrt3)=25-3=22$. Vậy nghiệm còn lại là $x_2=5+\sqrt3$ và $c=22$.
12. Bài 12: $x^2-4x-1=0$, $K=x_1^3-17x_1+2025$ → $x^2-4x-8=0$, $K=x_1^3-24x_1+2025$. $ac=1\cdot(-8)=-8<0$. $x_1^2-4x_1-8=0$, suy ra $x_1^2=4x_1+8$. $x_1^3=x_1(4x_1+8)=4x_1^2+8x_1$ [[br]] $=4(4x_1+8)+8x_1=24x_1+32$. $K=(24x_1+32)-24x_1+2025=2057$. Vậy $K=2057$.
13. Bài 15 ý a) CHỈ: $x^2-7x+6=0$ → $3x^2-11x+8=0$ \;(SGK Toán 9 tập hai, Bài 20, Luyện tập 2) — thêm chú thích nguồn ngay sau phương trình. $a+b+c=3-11+8=0$ và $a-b+c=3+11+8=22$. Vậy phương trình có hai nghiệm $x_1=1$ và $x_2=\dfrac{8}{3}$. Ý b) giữ nguyên.
14. Bài 16: $x^2-5x+2=0$ → $x^2-7x+8=0$. $\Delta=(-7)^2-4\cdot 1\cdot 8=17>0$. Viète: $x_1+x_2=7$, $x_1x_2=8$. a) $x_1^2+x_2^2=7^2-2\cdot 8=33$. b) $x_1^3+x_2^3=7^3-3\cdot 8\cdot 7=175$.
15. Bài 17 (hạ bậc): $x^2-3x-2=0$ → $x^2-5x-5=0$. a) $x_1^2-5x_1-5=0$, vậy $x_1^2=5x_1+5$. b) $x_1^3=x_1(5x_1+5)=5x_1^2+5x_1$ [[br]] $=5(5x_1+5)+5x_1=30x_1+25$. Vậy $x_1^3=30x_1+25$.
16. Bài 21 ý b) CHỈ: $\dfrac{x}{x+2}+\dfrac{3}{x-2}=\dfrac{12}{x^2-4}$ → $\dfrac{x}{x-3}+\dfrac{2}{x+3}=\dfrac{18}{x^2-9}$. Lời giải: $x^2-9=(x-3)(x+3)$ nên điều kiện xác định là $x\ne 3$ và $x\ne -3$. Khử mẫu: $x(x+3)+2(x-3)=18$ [[br]] $x^2+3x+2x-6=18$ [[br]] $x^2+5x-24=0$.
   $\Delta=5^2-4\cdot 1\cdot(-24)=121>0$ và $\sqrt{\Delta}=11$. $x_1=\dfrac{-5+11}{2}=3$ (loại vì không thỏa mãn điều kiện xác định). $x_2=\dfrac{-5-11}{2}=-8$ (thỏa mãn điều kiện xác định). Vậy phương trình có nghiệm $x=-8$. Ý a) giữ nguyên từng chữ (kể cả nguồn Thái Thịnh).
17. Bài 22 CẢ HAI Ý. Ý a): $x^2-7x+3=0$ → $x^2-4\sqrt3x+8=0$ \;(Cuối kì II, THCS Chu Văn An, Đà Nẵng) — vẫn tính $x_1^3+x_2^3$, thêm chú thích nguồn này. Lời giải: $\Delta'=(-2\sqrt3)^2-1\cdot 8=4>0$ nên phương trình có hai nghiệm phân biệt. Viète: $x_1+x_2=4\sqrt3$, $x_1x_2=8$.
   $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=(4\sqrt3)^3-3\cdot 8\cdot 4\sqrt3=192\sqrt3-96\sqrt3=96\sqrt3$. Vậy $x_1^3+x_2^3=96\sqrt3$. Ý b): $2x^2-x-5=0$ → $3x^2-x-5=0$ (vẫn tính $x_1^2+x_2^2$) và BỎ chú thích "\;(Cuối kì II, Phòng GD\&ĐT Ba Đình)".
   Lời giải: $ac=3\cdot(-5)=-15<0$ nên phương trình có hai nghiệm phân biệt. Viète: $x_1+x_2=\dfrac{1}{3}$, $x_1x_2=-\dfrac{5}{3}$. $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=\dfrac{1}{9}+\dfrac{10}{3}=\dfrac{31}{9}$. Vậy $x_1^2+x_2^2=\dfrac{31}{9}$.
18. Bài 24 ý b) CHỈ: $x^2-2x+c=0$, $x_1=1+\sqrt3$ → $x^2+2x+c=0$, $x_1=-1+\sqrt3$. Viète: $x_1+x_2=-2$, $x_1x_2=c$. $x_2=-2-x_1=-2-(-1+\sqrt3)=-1-\sqrt3$. $c=x_1x_2=(-1+\sqrt3)(-1-\sqrt3)=1-3=-2$. Vậy nghiệm còn lại là $x_2=-1-\sqrt3$ và $c=-2$. Ý a) giữ nguyên.

## Dặn chung
- Dòng điều kiện giữ ĐÚNG KIỂU như bảng ($\Delta$, $\Delta'$ hoặc $ac$). Trong statement là khung chỗ chấm thì giữ khung (ví dụ "$\Delta'=\ldots\ldots>0$"), chỉ đổi phương trình trong câu dẫn.
- Ví dụ 1, 2, 4, 7: trả về trong "statement" TOÀN BỘ chữ ví dụ mới (giữ "\textbf{Ví dụ N.}" và dòng tiêu đề Lời giải); "solution" để chuỗi rỗng "".
- Không văn nói, không xưng hô ("em", "hôm nay", "Kiểm", "Soi"), không kí hiệu $S$, $P$, không dấu chấm phẩy ";" nối công thức, không thêm câu mới ngoài bảng. Số âm trong phép tính đặt trong ngoặc: $(-4)^2$, $(-4)\cdot 6$. KHÔNG có chấm sau \end{cases}.
- Không đổi "label", không thêm/bớt bài, không đổi số ý, không đổi "hints" (không trả trường hints).

## Kiểm lại trước khi nộp
- Tự tính lại MỌI con số của các ý đã đổi và so với bảng; lệch thì ghi vào "ghi_chu", KHÔNG tự đổi phương trình.
- So từng khối với bản gốc: ngoài số liệu theo bảng, không chữ nào khác bị đổi.
- LaTeX hợp lệ: ngoặc { } cân, $ đủ cặp (đặc biệt $ đóng ở cuối dòng).

## Đầu ra
JSON đúng schema: {"sua": [18 phần tử {"label","statement","solution"}, đủ: {NHAN}], "ghi_chu": "điểm nghi ngờ hoặc chuỗi rỗng"}.
"statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ (kể cả phần không đổi).
'''

PROMPT_B = r'''Bạn là thợ sửa phiếu học tập Toán 9 (phiếu luyện tập chung cuối chương VI; học sinh lớp 9 tầng C — học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.

KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu nằm ở mục "Dữ liệu gốc" cuối prompt (trích từ seed phiếu). Mỗi khối có "label", "statement", "solution", "hints". Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; viết "GD\&ĐT", "THCS\&THPT" với \&.

## Vì sao phải sửa
Các bài lời văn của phiếu bị TRÙNG ĐỀ với phiếu khác cùng chương (đội xe chở $60$ tấn, mảnh đất $11$ m/$180$ m$^2$, bạn Nam đi học $12$ km đã có ở phiếu A, E), và các ý NB "đặt ẩn", "lập phương trình" lại dùng đúng đề của bài TH/VD ngay trong phiếu.
   Giáo viên đã chọn ĐỀ THẬT khác trong ngân hàng (đã kiểm số bằng máy).
   Việc của bạn: viết lại statement + solution các khối dưới theo đúng đề mới, GIỮ NGUYÊN khuôn trình bày của bản cũ (câu dẫn chung của bài, thẻ [NB]/[TH]/[VD], khung chỗ chấm \ldots\ldots, xuống dòng [[br]]\hspace*{1.4em}, cách viết lời giải: "Gọi … là $x$ (đơn vị), điều kiện …" → biểu diễn đại lượng → "Vì … nên ta có phương trình …" → khử mẫu, đưa về bậc hai → "Ta có $\Delta=…$ và $\sqrt{\Delta}=…$" (hoặc $\Delta'$) → hai nghiệm, nghiệm nào thỏa mãn/loại và vì sao → "Vậy …").

Chú thích nguồn đặt cuối đề ý/bài theo kiểu cũ: "\;(nguồn)".

## Đề mới từng khối (bất di bất dịch — không đổi số)
1. Bài 6 (NB đặt ẩn, giữ câu dẫn "Đặt ẩn kèm đơn vị và điều kiện cho mỗi bài toán lời văn. Điền vào chỗ chấm.").
   a) Tìm vận tốc của ca nô khi nước yên lặng, biết vận tốc của dòng nước là $7$ km/h \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa). Khung: "Gọi vận tốc của ca nô khi nước yên lặng là $x$ (\ldots\ldots), điều kiện \ldots\ldots". Lời giải: "Gọi vận tốc của ca nô khi nước yên lặng là $x$ (km/h), điều kiện $x>7$."
   b) Tìm số dãy ghế dự định lúc đầu của một phòng họp, biết số dãy ghế lúc đầu nhiều hơn $20$ dãy \;(Cuối kì II, THCS Chu Văn An, Đà Nẵng). Khung: "Gọi số dãy ghế dự định lúc đầu là $x$ (\ldots\ldots), điều kiện \ldots\ldots".
   Lời giải: "Gọi số dãy ghế dự định lúc đầu là $x$ (dãy), điều kiện $x$ nguyên và $x>20$."
2. Bài 7 (NB lập phương trình từ cụm chữ in nghiêng, giữ câu dẫn).
   a) \emph{Mỗi người còn lại phải làm thêm $4$ dụng cụ}, biết dự định mỗi người làm $\dfrac{144}{x}$ dụng cụ và thực tế mỗi người làm $\dfrac{144}{x-3}$ dụng cụ \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa). Khung "Phương trình: \ldots\ldots". Lời giải: "Phương trình: $\dfrac{144}{x-3}-\dfrac{144}{x}=4$."
   b) \emph{Hoàn thành công việc sớm hơn dự định $24$ phút}, biết thời gian dự định là $\dfrac{88}{x}$ giờ và thời gian thực tế là $\dfrac{90}{x+3}$ giờ \;(Giữa kì I, THCS Nguyễn Trường Tộ). Khung: "Đổi $24$ phút $=\ldots\ldots$ giờ" rồi "Phương trình: \ldots\ldots".
   Lời giải: "Đổi $24$ phút $=\dfrac{2}{5}$ giờ." / "Phương trình: $\dfrac{88}{x}-\dfrac{90}{x+3}=\dfrac{2}{5}$."
3. Bài 10 ý a) CHỈ (ý b về tổ may áo giữ nguyên TỪNG CHỮ, cả đề lẫn lời giải): đề mới "[TH] Một mảnh đất hình chữ nhật có chu vi bằng $82$ m. Nếu tăng chiều dài thêm $5$ m và tăng chiều rộng lên $2$ lần thì diện tích của mảnh đất lúc sau tăng thêm $560$ m$^2$.
   Tính các kích thước của mảnh đất hình chữ nhật đó lúc ban đầu. \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)". Lời giải: Nửa chu vi mảnh đất là $82:2=41$ (m). Gọi chiều rộng mảnh đất là $x$ (m), điều kiện $0<x<20{,}5$. Chiều dài mảnh đất là $41-x$ (m).
   Lúc sau chiều dài là $41-x+5=46-x$ (m), chiều rộng là $2x$ (m). Vì diện tích lúc sau tăng thêm $560$ m$^2$ nên ta có phương trình $2x(46-x)-x(41-x)=560$ [[br]] $92x-2x^2-41x+x^2=560$ [[br]] $x^2-51x+560=0$. Ta có $\Delta=(-51)^2-4\cdot 1\cdot 560=361>0$ và $\sqrt{\Delta}=19$.
   $x_1=\dfrac{51+19}{2}=35$ (loại vì $x<20{,}5$). $x_2=\dfrac{51-19}{2}=16$ (thỏa mãn điều kiện). Vậy mảnh đất có chiều rộng $16$ m và chiều dài $41-16=25$ m.
4. Bài 13 (VD, thay cả đề): "[VD] Một phân xưởng theo kế hoạch cần phải sản xuất $1100$ sản phẩm trong một số ngày quy định. Do mỗi ngày phân xưởng đó sản xuất vượt mức $5$ sản phẩm nên đã hoàn thành kế hoạch sớm hơn thời gian quy định $2$ ngày.
   Hỏi theo kế hoạch, mỗi ngày phân xưởng sản xuất được bao nhiêu sản phẩm? \;(Giữa kì II, THCS Lê Ngọc Hân)". Lời giải: Gọi số sản phẩm phân xưởng sản xuất mỗi ngày theo kế hoạch là $x$ (sản phẩm), điều kiện $x$ nguyên dương.
   Thời gian theo kế hoạch là $\dfrac{1100}{x}$ (ngày). Thực tế mỗi ngày sản xuất được $x+5$ (sản phẩm) nên thời gian thực tế là $\dfrac{1100}{x+5}$ (ngày).
   Vì hoàn thành sớm hơn quy định $2$ ngày nên ta có phương trình $\dfrac{1100}{x}-\dfrac{1100}{x+5}=2$ [[br]] $1100(x+5)-1100x=2x(x+5)$ [[br]] $2x^2+10x-5500=0$ [[br]] $x^2+5x-2750=0$. Ta có $\Delta=5^2-4\cdot 1\cdot(-2750)=11025>0$ và $\sqrt{\Delta}=105$. $x_1=\dfrac{-5+105}{2}=50$ (thỏa mãn điều kiện).
   $x_2=\dfrac{-5-105}{2}=-55$ (loại vì $x>0$). Vậy theo kế hoạch mỗi ngày phân xưởng sản xuất được $50$ sản phẩm.
   Hints mới (2 câu hỏi kiểu Polya, không gọi tên công thức): "Đề hỏi đại lượng nào? Chọn đại lượng đó làm ẩn." và "Thời gian thực tế ít hơn thời gian theo kế hoạch bao nhiêu ngày?".
5. Bài 19 (NB đặt ẩn BTVN, giữ câu dẫn "Đặt ẩn kèm đơn vị và điều kiện cho mỗi bài toán. Điền vào chỗ chấm.").
   a) Tìm khối lượng riêng của miếng kim loại thứ nhất \;(đề tham khảo Vào 10, THCS\&THPT Nguyễn Tất Thành). Khung: "Gọi khối lượng riêng của miếng kim loại thứ nhất là $x$ (\ldots\ldots), điều kiện \ldots\ldots". Lời giải: "Gọi khối lượng riêng của miếng kim loại thứ nhất là $x$ (g/cm$^3$), điều kiện $x>0$."
   b) Tìm số con khỉ trong một bầy khỉ \;(Giữa kì I, THCS Thanh Am). Khung: "Gọi số con khỉ trong bầy là $x$ (\ldots\ldots), điều kiện \ldots\ldots". Lời giải: "Gọi số con khỉ trong bầy là $x$ (con), điều kiện $x$ nguyên dương."
6. Bài 20 ý a) CHỈ (ý b giữ nguyên từng chữ): "\emph{Tổ may xong sớm hơn thời gian quy định $4$ ngày}, biết số ngày theo quy định là $\dfrac{8400}{x}$ và số ngày thực tế là $\dfrac{6416}{x+102}$ \;(thi thử Vào 10, THCS Mỹ Đình 2)". Khung "Phương trình: \ldots\ldots". Lời giải: "Phương trình: $\dfrac{8400}{x}-\dfrac{6416}{x+102}=4$."
7. Bài 25 (VD hạ bậc): "[VD] Cho phương trình $x^2+3x-3=0$. Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức $H=x_1^3-12x_1+2026$." — BỎ chú thích nguồn Ứng Hòa. Lời giải: Ta có $ac=1\cdot(-3)=-3<0$ nên phương trình có hai nghiệm phân biệt.
   Vì $x_1$ là nghiệm của phương trình nên $x_1^2+3x_1-3=0$. Suy ra $x_1^2=-3x_1+3$. $x_1^3=x_1\cdot x_1^2=x_1(-3x_1+3)=-3x_1^2+3x_1$ [[br]] $=-3(-3x_1+3)+3x_1=12x_1-9$. $H=(12x_1-9)-12x_1+2026=2017$. Vậy $H=2017$. KHÔNG trả hints cho Bài 25 (giữ hints cũ).
8. Bài 26 (VD, thay cả đề): "[VD] Một người đi xe đạp từ $A$ đến $B$ với vận tốc không đổi. Khi đi từ $B$ về $A$ người đó giảm vận tốc $3$ km/h so với lúc đi nên thời gian đi ít hơn thời gian về là $6$ phút.
   Tính vận tốc người đi xe đạp lúc đi và lúc về, biết quãng đường $AB$ dài $6$ km. \;(Giữa kì II, THCS Mỹ Đình 2)". Lời giải: Gọi vận tốc người đi xe đạp lúc đi là $x$ (km/h), điều kiện $x>3$. Vận tốc lúc về là $x-3$ (km/h).
   Thời gian đi là $\dfrac{6}{x}$ (giờ), thời gian về là $\dfrac{6}{x-3}$ (giờ). Đổi $6$ phút $=\dfrac{1}{10}$ giờ. Vì thời gian đi ít hơn thời gian về $6$ phút nên ta có phương trình $\dfrac{6}{x-3}-\dfrac{6}{x}=\dfrac{1}{10}$ [[br]] $60x-60(x-3)=x(x-3)$ [[br]] $x^2-3x-180=0$.
   Ta có $\Delta=(-3)^2-4\cdot 1\cdot(-180)=729>0$ và $\sqrt{\Delta}=27$. $x_1=\dfrac{3+27}{2}=15$ (thỏa mãn điều kiện). $x_2=\dfrac{3-27}{2}=-12$ (loại vì $x>3$). Vận tốc lúc về là $15-3=12$ (km/h). Vậy vận tốc người đi xe đạp lúc đi là $15$ km/h và lúc về là $12$ km/h.
   Hints mới: "Lúc về chậm hơn nên thời gian đi hay thời gian về dài hơn?" và "Đổi $6$ phút ra giờ trước khi lập phương trình."

## Dặn chung
- Mỗi dòng lời giải một ý, xuống dòng [[br]] (BTVN/VD dòng sau không thụt, giống bản cũ của chính khối đó; ý a/b thụt [[br]]\hspace*{1.4em} giống bản cũ).
- Không văn nói, không xưng hô ("em", "hôm nay", "Kiểm", "Soi", "mẹo"), không chữ "khuôn", không dấu chấm phẩy ";" nối công thức, không thêm câu ngoài nội dung trên.
- Không đổi "label", không thêm/bớt bài, không đổi số ý. Chỉ trả "hints" cho Bài 13 và Bài 26.

## Kiểm lại trước khi nộp
- Tự giải lại mọi bài lời văn; lệch với số trên thì ghi "ghi_chu", KHÔNG tự đổi số.
- LaTeX hợp lệ: ngoặc { } cân, $ đủ cặp.

## Đầu ra
JSON đúng schema: {"sua": [8 phần tử {"label","statement","solution"[,"hints"]}, đủ: {NHAN}], "ghi_chu": "điểm nghi ngờ hoặc chuỗi rỗng"}.
"statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ (kể cả phần không đổi).
'''

# Sửa cơ học sau khi áp (không phải chữ nội dung mới): check SymPy của bài đổi số, gợi ý Bài 25 trỏ sai bài,
# ghi chú GV tổng kết đếm sai BTVN.
CHECK = {
    "Bài 8.": {"kind": "solveset", "equation": "x**2 + 2*x - 3 = 0", "answer": [1, -3], "symbol": "x"},
    "Bài 11.": {"kind": "solveset", "equation": "x**2 - 10*x + 22 = 0", "answer": ["5+sqrt(3)", "5-sqrt(3)"], "symbol": "x"},
    "Bài 24.": {"kind": "solveset", "equation": "x**2 + 2*x - 2 = 0", "answer": ["-1+sqrt(3)", "-1-sqrt(3)"], "symbol": "x"},
    "Bài 13.": {"kind": "solveset", "equation": "x**2 + 5*x - 2750 = 0", "answer": [50, -55], "symbol": "x"},
    "Bài 26.": {"kind": "solveset", "equation": "x**2 - 48*x - 49 = 0", "answer": [49, -1], "symbol": "x"},
}
TEXT = [  # (cũ, mới) — mỗi cặp phải khớp đúng 1 lần
    ("Viết $x_1^3$ theo $x_1$ như Bài 14.", "Viết $x_1^3$ theo $x_1$ như Bài 17."),
    ("BTVN 14 bài (Bài 16 đến Bài 29)", "BTVN 13 bài (Bài 14 đến Bài 26)"),
    ("Bài 13 (bài toán chở hàng)", "Bài 13 (bài toán năng suất)"),
]


def sau(ghi: bool):
    p = REPO / SEED
    raw = p.read_text()
    for cu, moi in TEXT:
        n = raw.count(json.dumps(cu, ensure_ascii=False)[1:-1])
        if n == 0 and json.dumps(moi, ensure_ascii=False)[1:-1] in raw:
            print("đã sửa:", moi)
            continue
        assert n == 1, (cu, n)
        raw = raw.replace(json.dumps(cu, ensure_ascii=False)[1:-1], json.dumps(moi, ensure_ascii=False)[1:-1])
        print("sửa:", cu, "→", moi)
    seed = json.loads(raw)
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem" and b["label"] in CHECK and b.get("check") != CHECK[b["label"]]:
                print("check", b["label"], b.get("check"), "→", CHECK[b["label"]])
                b["check"] = CHECK[b["label"]]
    if ghi:
        p.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi", SEED)


def ghi_viec(seed, vid, labels, prompt, hints=False):
    goc = []
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem" and b["label"] in labels:
                keys = ("label", "statement", "solution") + (("hints",) if hints else ())
                goc.append({k: b.get(k, []) for k in keys})
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m and m.group(1) in labels:
                    goc.append({"label": m.group(1), "statement": b["text"]})
    assert sorted(x["label"] for x in goc) == sorted(labels), [x["label"] for x in goc]
    viec = {
        "id": vid, "model": "gemini-4-hydrogen-medium",
        "prompt": prompt.replace("{NHAN}", ", ".join(labels))
        + f"\n## Dữ liệu gốc ({len(goc)} khối, JSON)\n" + json.dumps(goc, ensure_ascii=False, indent=1) + "\n",
        "files": [], "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "900s",
        "meta": {"loai": "sua-phieu", "seed": SEED, "labels": labels},
    }
    out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
    out.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
    print("Đã ghi", out.relative_to(REPO))


def main():
    if "--sau" in sys.argv:
        return sau("--ghi" in sys.argv)
    kiem_so_do()
    seed = json.loads((REPO / SEED).read_text())
    if "--dot2" in sys.argv:
        return ghi_viec(seed, VID_2, LABELS_2, PROMPT_2, hints=True)
    ghi_viec(seed, VID, LABELS, PROMPT)
    ghi_viec(seed, VID_B, LABELS_B, PROMPT_B, hints=True)



# ---- Đợt 2 (16/11): giám đốc phiếu C vừa đưa đề Chu Văn An (x^2-4√3x+8) vào phiếu C; Bài 26 Mỹ Đình 2 ra
# x^2-3x-180 trùng phương trình E Bài 18 ⇒ đổi Bài 22a (tự đặt số), Bài 26 = ca nô Tô Vĩnh Diện, Bài 6a = Mỹ Đình 2.
VID_2 = VID + "-2"
LABELS_2 = ["Bài 6.", "Bài 22.", "Bài 26."]
PROMPT_2 = r'''Bạn là thợ sửa phiếu học tập Toán 9 (phiếu luyện tập chung cuối chương VI; học sinh lớp 9 tầng C). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề.
KHÔNG chạy lệnh, KHÔNG mở file: dữ liệu ở mục "Dữ liệu gốc" cuối prompt. Xuống dòng là [[br]]. Toán trong $...$. Viết "GD\&ĐT" với \&.

## Việc (số liệu đã kiểm bằng máy, không đổi số)
1. Bài 6 ý a) CHỈ (ý b giữ nguyên từng chữ). Đề ý a mới: "a) [NB] Tìm vận tốc người đi xe đạp lúc đi, biết lúc về người đó giảm vận tốc $3$ km/h \;(Giữa kì II, THCS Mỹ Đình 2)" rồi dòng khung "\hspace*{1.4em}Gọi vận tốc người đi xe đạp lúc đi là $x$ (\ldots\ldots), điều kiện \ldots\ldots". Lời giải ý a: "a) Gọi vận tốc người đi xe đạp lúc đi là $x$ (km/h), điều kiện $x>3$."
2. Bài 22 ý a) CHỈ (ý b giữ nguyên từng chữ): đề "a) [TH] $x^2+5x+5=0$, tính $x_1^3+x_2^3$." (không chú thích nguồn). Lời giải ý a, giữ đúng cách xuống dòng của ý b: "a) Ta có $\Delta=5^2-4\cdot 1\cdot 5=5>0$ nên phương trình có hai nghiệm phân biệt." / "Theo định lí Viète, ta có $\begin{cases} x_1+x_2=-5\\ x_1x_2=5\end{cases}$" / "$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=(-5)^3-3\cdot 5\cdot(-5)=-125+75=-50$." / "Vậy $x_1^3+x_2^3=-50$."
3. Bài 26 (thay cả đề): "[VD] Một chiếc ca nô chuyển động xuôi dòng từ $A$ đến $B$ sau đó ngược dòng từ $B$ về $A$ hết tổng cộng $6$ giờ. Biết quãng đường sông từ $A$ đến $B$ dài $144$ km và vận tốc của dòng nước là $7$ km/h. Tính vận tốc của ca nô khi nước yên lặng. \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)". Lời giải (mỗi ý một dòng, cách [[br]] như lời giải cũ của Bài 26, không thụt): Gọi vận tốc của ca nô khi nước yên lặng là $x$ (km/h), điều kiện $x>7$. / Vận tốc ca nô khi xuôi dòng là $x+7$ (km/h), khi ngược dòng là $x-7$ (km/h). / Thời gian xuôi dòng là $\dfrac{144}{x+7}$ (giờ), thời gian ngược dòng là $\dfrac{144}{x-7}$ (giờ). / Vì tổng thời gian xuôi dòng và ngược dòng là $6$ giờ nên ta có phương trình $\dfrac{144}{x+7}+\dfrac{144}{x-7}=6$ / $144(x-7)+144(x+7)=6(x+7)(x-7)$ / $288x=6x^2-294$ / $x^2-48x-49=0$. / Ta có $\Delta'=(-24)^2-1\cdot(-49)=625>0$ và $\sqrt{\Delta'}=25$. / $x_1=\dfrac{24+25}{1}=49$ (thỏa mãn điều kiện). / $x_2=\dfrac{24-25}{1}=-1$ (loại vì $x>7$). / Vậy vận tốc của ca nô khi nước yên lặng là $49$ km/h. Hints mới (hỏi kiểu Polya, không gọi tên công thức): "Khi xuôi dòng và ngược dòng, vận tốc ca nô thay đổi thế nào so với khi nước yên lặng?" và "Tổng thời gian đi và về bằng bao nhiêu giờ?".

Không văn nói, không xưng hô, không dấu ";" nối công thức. Không đổi label. Chỉ trả "hints" cho Bài 26.
Tự giải lại; lệch thì ghi "ghi_chu", không tự đổi số.

## Đầu ra
JSON đúng schema: {"sua": [3 phần tử {"label","statement","solution"[,"hints"]} cho {NHAN}], "ghi_chu": ""}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''


# ---- Đợt 3 (16/11): Ví dụ 3 chỉ khác phiếu B Bài 10a đúng một số ⇒ đổi phương trình.
VID_3 = VID + "-3"
LABELS_3 = ["Ví dụ 3."]
PROMPT_3 = r'''Bạn là thợ sửa phiếu học tập Toán 9 (học sinh lớp 9 tầng C). CHỈ sửa đúng phạm vi, KHÔNG bịa đề, KHÔNG chạy lệnh.
Dữ liệu ở mục "Dữ liệu gốc" cuối prompt: khối "Ví dụ 3." có "statement" = toàn bộ chữ ví dụ kèm lời giải mẫu. Xuống dòng là [[br]].

## Việc (số đã kiểm bằng máy)
Ví dụ 3 gần trùng một bài của phiếu khác ⇒ đổi phương trình $\dfrac{x}{x-2}+\dfrac{2}{x+2}=\dfrac{8}{x^2-4}$ thành $\dfrac{x}{x-5}+\dfrac{2}{x+5}=\dfrac{50}{x^2-25}$ và viết lại lời giải theo ĐÚNG khuôn dòng cũ:
"Ta có $x^2-25=(x-5)(x+5)$ nên điều kiện xác định là $x\ne 5$ và $x\ne -5$." / "Quy đồng mẫu hai vế rồi khử mẫu, ta được $x(x+5)+2(x-5)=50$" / "$x^2+5x+2x-10=50$" / "$x^2+7x-60=0$" / "Ta có $\Delta=7^2-4\cdot 1\cdot(-60)=289>0$ và $\sqrt{\Delta}=17$." / "$x_1=\dfrac{-7+17}{2}=5$ (loại vì không thỏa mãn điều kiện xác định)." / "$x_2=\dfrac{-7-17}{2}=-12$ (thỏa mãn điều kiện xác định)." / "Vậy phương trình có nghiệm $x=-12$."
Giữ nguyên "\textbf{Ví dụ 3.}", câu đề, dòng tiêu đề Lời giải, cách xuống dòng [[br]]\hspace*{1.4em}. Không thêm câu.

## Đầu ra
JSON đúng schema: {"sua": [1 phần tử {"label": "Ví dụ 3.", "statement": <toàn bộ chữ ví dụ mới>, "solution": ""}], "ghi_chu": ""}.
'''


if __name__ == "__main__":
    if "--dot3" in sys.argv:
        kiem_so_do()
        ghi_viec(json.loads((REPO / SEED).read_text()), VID_3, LABELS_3, PROMPT_3)
    else:
        main()
