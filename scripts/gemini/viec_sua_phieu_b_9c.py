#!/usr/bin/env python3
"""Sửa phiếu B ch.VI 9C (13/11/2026) — "Phương trình chứa ẩn ở mẫu quy về phương trình bậc hai".

Lỗi bản cũ: dan_dat_gate chặn; lý thuyết có hộp trap "mất 0,25 điểm" + target "Câu III.1", mục "tiết kiệm nửa thời
gian"; "hôm nay"/"buổi này"; ~80 dấu ";"; 4 ví dụ chép y bài; bài NB lẻ (tính ac, rút gọn căn, câu kết luận) — Thầy
chốt 13/11 bỏ; nhẩm nghiệm giữ nhưng gọn.
Đề + đáp số: Claude chọn, kiểm SymPy ở so_do_phieu_b_9c.py. Gemini chỉ viết chữ.

    python3 scripts/gemini/viec_sua_phieu_b_9c.py
    python3 scripts/gemini/tho.py --tien-to sua-9c-ch6-phieu-b- --song-song 3
    python3 scripts/gemini/lap_sua_phieu_b_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_phieu_b_9c import tom_tat  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/"
        "phieu-b-phuong-trinh-chua-an-o-mau-quy-ve-bac-hai.json")
VID_LT, VID_LOP, VID_BTVN = "sua-9c-ch6-phieu-b-lt", "sua-9c-ch6-phieu-b-lop", "sua-9c-ch6-phieu-b-btvn"

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, buổi 2 "Phương trình chứa ẩn ở mẫu quy về phương trình bậc hai", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Học sinh ĐÃ học Bài 19 (công thức nghiệm $\Delta$, $\Delta'$, phương trình khuyết) và phương trình chứa ẩn ở mẫu ở chương II (SGK Toán 9 tập một, Bài 4). CHƯA học định lí Viète — nhẩm nghiệm chỉ dùng như một quy tắc. KHÔNG có tham số $m$. KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm trong prompt.

## Luật cứng (vi phạm bị trả lại)
- CẤM chữ/ý: "khuôn", "Câu III", "đề Vào 10 hỏi", điểm số, "mất điểm", "thang điểm", "tầng C", "mẹo", "chìa khóa", "nhanh nhất", "tiết kiệm", "ăn may". Trích nguồn đề trong ngoặc sau đề bài thì GIỮ (đã ghi sẵn ở sơ đồ).
- CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "ép", "nhé", "vừa khít". Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác" — dùng "nên", "$\Rightarrow$", "$\Leftrightarrow$" hoặc xuống dòng.
- KHÔNG dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Hai nghiệm viết "$x_1=…$ và $x_2=…$". Ba hệ số viết "$a=2$, $b=-5$, $c=2$". ĐKXĐ viết "$x\ne 1$ và $x\ne -3$".
- Câu dẫn đề TỰ SOẠN: "Giải phương trình …", "Tìm điều kiện xác định của phương trình …". KHÔNG nói trước số nghiệm, không nói trước nghiệm nào bị loại.
- Lời giải theo NHỊP BÀI THI, đúng cách trình bày SGK, mỗi bước một dòng [[br]], ví dụ và khung điền thụt "\hspace*{1.4em}", "Vậy …" dòng riêng ở cuối. Viết tắt "ĐKXĐ" được (SGK dùng). Mẫu theo loại (số chỉ minh họa):
  [dkxd]  (như SGK tr.28 Ví dụ 3) "Vì $x-1\ne 0$ khi $x\ne 1$ và $x+3\ne 0$ khi $x\ne -3$[[br]]nên ĐKXĐ của phương trình là $x\ne 1$ và $x\ne -3$."
          mẫu cần phân tích: "Ta có $x^2-5x=x(x-5)$.[[br]]Vì $x\ne 0$ và $x-5\ne 0$ khi $x\ne 5$[[br]]nên ĐKXĐ của phương trình là $x\ne 0$ và $x\ne 5$."
  [khu]   "ĐKXĐ: $x\ne 1$ và $x\ne -1$.[[br]]Mẫu thức chung là $(x-1)(x+1)$.[[br]]Quy đồng mẫu hai vế rồi khử mẫu, ta được[[br]]$x(x+1)+2(x-1)=4$[[br]]$\Leftrightarrow x^2+x+2x-2-4=0$[[br]]$\Leftrightarrow x^2+3x-6=0$.[[br]]Phương trình bậc hai nhận được có $a=1$, $b=3$, $c=-6$."
  [nham]  (như SGK tr.22 Ví dụ 2) "Ta có $a=2$, $b=-9$, $c=7$ và $a+b+c=2+(-9)+7=0$[[br]]nên phương trình có hai nghiệm $x_1=1$ và $x_2=\dfrac{c}{a}=\dfrac{7}{2}$." / với $a-b+c=0$: "… $a-b+c=3-10+7=0$[[br]]nên phương trình có hai nghiệm $x_1=-1$ và $x_2=-\dfrac{c}{a}=-\dfrac{7}{3}$."
  [giai4]/[giai] đủ 4 bước SGK, không ghi chữ "Bước 1…" trong lời giải: "ĐKXĐ: …[[br]]Quy đồng mẫu hai vế rồi khử mẫu, ta được[[br]]…[[br]]$\Leftrightarrow 2x^2-x-1=0$.[[br]]Ta có $a+b+c=2+(-1)+(-1)=0$ nên phương trình này có hai nghiệm $x_1=1$ và $x_2=\dfrac{c}{a}=-\dfrac{1}{2}$.[[br]]Giá trị $x_1=1$ không thỏa mãn ĐKXĐ, giá trị $x_2=-\dfrac{1}{2}$ thỏa mãn ĐKXĐ.[[br]]Vậy phương trình đã cho có nghiệm $x=-\dfrac{1}{2}$."
          Phương trình bậc hai sau khử mẫu: có $a+b+c=0$ hoặc $a-b+c=0$ (sơ đồ ghi sẵn) thì NHẨM, không thì dùng $\Delta$ ($b$ lẻ) hoặc $\Delta'$ ($b$ chẵn) như Bài 19: "Ta có $\Delta'=1^2-1\cdot(-8)=9>0$, $\sqrt{\Delta'}=3$[[br]]nên phương trình có hai nghiệm phân biệt $x_1=\dfrac{-1+3}{1}=2$ và $x_2=\dfrac{-1-3}{1}=-4$." Khuyết $c$ thì đặt nhân tử chung. Khuyết $b$ thì $x^2=k$. Nghiệm kép: "$\Delta'=0$ nên phương trình có nghiệm kép $x_1=x_2=3$". Cả hai bị loại: "Cả hai giá trị đều không thỏa mãn ĐKXĐ.[[br]]Vậy phương trình đã cho vô nghiệm."
          Mẫu đối nhau (như $x-2$ và $2-x$): dòng riêng "Ta có $\dfrac{x+2}{2-x}=-\dfrac{x+2}{x-2}$." trước khi quy đồng.
  [tt]    (phương trình cho sẵn) ĐKXĐ → khử mẫu → thu gọn → giải → "Vì $x>0$ nên loại $x_2=-45$, nhận $x_1=30$." → tính đại lượng đề hỏi → "Vậy …".
- Thẻ mức đặt ở ĐẦU MỖI Ý: "a) [NB] …". Bài một ý thì thẻ "[TH]"/"[VD]"/"[NB]" đứng đầu đề. Không gắn thẻ ở cả đề lẫn ý.
- Toán trong $…$, phân số \dfrac, số thập phân dấu phẩy. Chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". MỌI dấu $ mở phải có $ đóng — soát từng dòng.
- Phương trình, ĐKXĐ, phương trình sau khử mẫu, $\Delta$, nghiệm, nghiệm NHẬN/LOẠI ở mục "Sơ đồ đề và đáp số" ĐÃ ĐƯỢC MÁY KIỂM (SymPy) — dùng đúng, KHÔNG đổi phương trình, KHÔNG thêm phương trình mới. Viết đề dạng LaTeX: "2*x/(x+3)" là "$\dfrac{2x}{x+3}$", "(x-1)*(x+3)" là "$(x-1)(x+3)$". Phương trình sau khử mẫu ở sơ đồ có thể đã chia hai vế cho một số — khi viết lời giải phải hiện bước chia đó. Vẫn tự tính lại từng dòng trung gian; thấy lệch thì ghi vào "ghi_chu", không tự sửa số.

## Khuôn khối (JSON)
- Tiêu đề mạch: {"type":"para","variant":"heading","text":"Mạch 1. …"}
- Ví dụ (giáo viên làm cùng lớp, có ô điền): {"type":"noted","variant":"example","text":"\\textbf{Ví dụ 1.} <đề>[[br]]{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …"}
  Ví dụ nhiều ý: "a)" "b)" đầu dòng riêng trong Lời giải. Trong Lời giải khoét 3–6 ô bằng [[fill:đáp án]] ở chỗ then chốt (giá trị bị loại trong ĐKXĐ, phương trình sau thu gọn, nghiệm, chữ "thỏa mãn"/"không thỏa mãn", CÂU KẾT LUẬN "Vậy" phải có ô). Ô trong $…$ thì đáp án KHÔNG bọc $ (ví dụ "$x\ne [[fill:1]]$"). Ô ngoài $…$ chứa công thức thì bọc $ bên trong (ví dụ "[[fill:$x=-\dfrac{1}{2}$]]"). KHÔNG để số vừa nằm trong ô lại in sẵn ở dòng dưới hoặc ở đề (lộ đáp án).
- Bài NB điền khuyết = BÀI TRÌNH BÀY HOÀN CHỈNH theo đúng các dòng của ví dụ đứng trước, chỗ HS điền ghi "\\ldots\\ldots". Đề luôn mở bằng: "Điền vào chỗ chấm để hoàn thành bài giải (làm đủ các bước như Ví dụ N)." rồi từng ý: "a) [NB] $<phương trình>$[[br]]\\hspace*{1.4em}<dòng 1 có chỗ chấm>[[br]]\\hspace*{1.4em}…[[br]]b) [NB] …"
  Mỗi ý ≥ 3 chỗ chấm, chỗ chấm rơi vào CHỖ PHẢI SUY RA (giá trị bị loại, mẫu thức chung, hạng tử sau khai triển, hệ số, nghiệm, thỏa mãn hay không, kết luận), không rơi vào chữ in sẵn ở dòng khác. Ý nào kết quả khác ví dụ (nhận cả hai nghiệm, khuyết $c$) thì KHÔNG in sẵn "không thỏa mãn"/"loại" — để chỗ chấm cho HS tự kết luận ("Giá trị $x_1=\\ldots\\ldots$ \\ldots\\ldots\\ldots ĐKXĐ"). "solution": lời giải đầy đủ từng ý (a) …[[br]]\\hspace*{1.4em}…[[br]]b) …), điền hết các chỗ chấm.
- Bài TH, VD (tự trình bày): "statement" chỉ có ĐỀ, không chỗ chấm, không khung. "solution": lời giải đầy đủ theo nhịp bài thi. "hints": 1–2 câu hỏi gợi ý kiểu Polya ("Mẫu nào cần phân tích thành nhân tử trước?", "Giá trị nào làm một mẫu bằng $0$?", "Phương trình bậc hai nhận được có nhẩm nghiệm được không?", "Nghiệm tìm được có thỏa mãn mọi điều kiện của đề không?") — hỏi, KHÔNG gọi tên công thức, không lộ số, không làm hộ.
- Khối bài: {"type":"problem","label":"Bài N.","level":1|2|3,"tier":"onclass"|"btvn","statement":…,"solution":…,"hints":[…]} (NB level 1 để "hints": []).
'''


def so_do(*nhan):
    tt, trung = tom_tat()
    assert not trung, trung
    return "\n".join(f"- {k}\n" + "\n".join("    " + d for d in tt[k]) for k in nhan)


PROMPT_LT = CHUNG + r'''
## Việc A: viết phần mở đầu, nhắc lại, lý thuyết, sơ đồ tư duy, ghi chú giáo viên
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap","teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

1. "opener_text" (chặng Khám phá, có hình hai tổ vẽ sẵn): sửa nhẹ đoạn mở đầu cũ (ở cuối prompt) — giữ tình huống hai tổ cùng làm $300$ sản phẩm, tổ B mỗi ngày làm nhiều hơn tổ A $10$ sản phẩm nên xong sớm hơn $1$ ngày, giữ hai phân thức $\dfrac{300}{x}$, $\dfrac{300}{x+10}$ và phương trình $\dfrac{300}{x}-\dfrac{300}{x+10}=1$. Bỏ dấu ";", bỏ "hôm nay", không xưng hô, không nhắc đề thi. Hai câu hỏi gợi mở: $x$ được phép nhận giá trị nào? khử mẫu xong được phương trình gì? Kết bằng câu: Bài 8 cuối phiếu giải trọn phương trình này.
2. "review_note" (khối "Nhắc lại kiến thức đã học"): ba kĩ năng, mỗi kĩ năng một tiêu đề in đậm + 1–2 dòng ví dụ:
   (1) Phân tích mẫu thức thành nhân tử (Lớp 8): $x^2-16=(x-4)(x+4)$ và $x^2+3x=x(x+3)$.
   (2) Mẫu thức chung: mẫu thức chung của $\dfrac{1}{x-4}$, $\dfrac{1}{x+4}$, $\dfrac{1}{x^2-16}$ là $(x-4)(x+4)$.
   (3) Công thức nghiệm (Bài 19): $\Delta=b^2-4ac$, $\Delta>0$ thì $x_1=\dfrac{-b+\sqrt{\Delta}}{2a}$, $x_2=\dfrac{-b-\sqrt{\Delta}}{2a}$ (b chẵn dùng $\Delta'=b'^2-ac$).
   Dòng cách nhau [[br]], thụt "\quad". Không dấu ";".
3. "concept_blocks" (chặng Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT, đúng chữ SGK, mục đánh số "\textbf{N. Tên}" (một khối para tiêu đề + một khối para nội dung), 3 mục:
   1. Điều kiện xác định của phương trình — đúng chữ SGK Toán 9 tập một tr.28: "Đối với phương trình chứa ẩn ở mẫu, ta thường đặt điều kiện cho ẩn để tất cả các mẫu thức trong phương trình đều khác $0$ và gọi đó là điều kiện xác định (viết tắt là ĐKXĐ) của phương trình." Thêm một dòng ví dụ: phương trình $\dfrac{1}{x+1}=1+\dfrac{1}{x-2}$ có ĐKXĐ là $x\ne -1$ và $x\ne 2$.
   2. Cách giải phương trình chứa ẩn ở mẫu — đúng chữ SGK Toán 9 tập một tr.29: "\emph{Bước 1.} Tìm điều kiện xác định của phương trình.[[br]]\emph{Bước 2.} Quy đồng mẫu hai vế của phương trình rồi khử mẫu.[[br]]\emph{Bước 3.} Giải phương trình vừa tìm được.[[br]]\emph{Bước 4 (Kết luận).} Trong các giá trị tìm được của ẩn ở Bước 3, giá trị nào thỏa mãn điều kiện xác định chính là nghiệm của phương trình đã cho." Thêm một dòng: phương trình nhận được ở Bước 3 có thể là phương trình bậc hai — giải bằng công thức nghiệm (Bài 19) hoặc nhẩm nghiệm (mục 3).
   3. Nhẩm nghiệm của phương trình bậc hai — đúng chữ SGK Toán 9 tập hai tr.22: "Xét phương trình $ax^2+bx+c=0$ ($a\ne 0$).[[br]]$\bullet$\; Nếu $a+b+c=0$ thì phương trình có một nghiệm là $x_1=1$, còn nghiệm kia là $x_2=\dfrac{c}{a}$.[[br]]$\bullet$\; Nếu $a-b+c=0$ thì phương trình có một nghiệm là $x_1=-1$, còn nghiệm kia là $x_2=-\dfrac{c}{a}$." Thêm một dòng: quy tắc này được chứng minh ở Bài 20 (định lí Viète). Có thể thay $x=1$ (hoặc $x=-1$) vào phương trình để thấy đó là một nghiệm.
   KHÔNG thêm khối trap, target, lỗi hay gặp, cấu trúc đề thi.
4. "mindmap": {"type":"mindmap","caption":"Điền các ô trống để tự tóm tắt cả buổi","root":"Phương trình chứa ẩn ở mẫu","branches":[4 nhánh theo 4 bước: "Bước 1" (con: "Mọi mẫu thức [[blank:1.4cm]] $0$"), "Bước 2" (con: "Quy đồng mẫu hai vế rồi [[blank:1.4cm]]"), "Bước 3" (con: "$a+b+c=0$: $x_1=[[blank:0.8cm]]$, $x_2=[[blank:1cm]]$", "$a-b+c=0$: $x_1=[[blank:0.8cm]]$, $x_2=[[blank:1cm]]$", "Không nhẩm được: tính [[blank:1.2cm]]"), "Bước 4" (con: "Giá trị nào thỏa mãn [[blank:1.4cm]] là nghiệm")]}. Mỗi nhánh {"label":…,"children":[{"label":…}]}.
5. "teacher_notes" (ghi chú giáo viên, ngắn, chỉ cách tổ chức dạy, không "khuôn"/điểm số/"hôm nay"):
   review: mở màn khoảng 8 phút, cho học sinh đọc hai phân thức và trả lời $x$ được nhận giá trị nào, nhắc nhanh ba kĩ năng trên bảng.
   concept: giảng khoảng 30 phút theo thứ tự mục 1 → 3, viết 4 bước lên góc bảng giữ suốt buổi, mục 3 cho học sinh thay $x=1$ vào một phương trình để thấy quy tắc đúng.
   practice1: khoảng 55 phút, 4 mạch, mỗi mạch giáo viên làm ví dụ cùng lớp (điền ô) rồi học sinh điền bài ngay sau. Mạch 4 ghép đủ 4 bước, nhấn bước đối chiếu ĐKXĐ.
   practice2: khoảng 55 phút, Ví dụ 5 rồi Bài 5–6 học sinh tự trình bày (gọi lên bảng theo cặp, Bài 6a chú ý mẫu đối nhau), Ví dụ 6 → Bài 7 → Bài 8 phương trình cho sẵn từ bài toán thực tế. Bài 8 là đích của buổi, chính là bài toán mở đầu.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 9–16 in thành phiếu riêng, khoảng 90 phút. Buổi sau chữa Bài 13 và Bài 16 trước.

## Đoạn mở đầu cũ (sửa theo mục 1)
'''

PROMPT_LOP = CHUNG + r'''
## Việc B: dựng 2 chặng LUYỆN TẬP trên lớp
Đầu ra JSON {"stages":[{"kind":"practice1",…},{"kind":"practice2",…}],"ghi_chu"}. Mỗi stage có "kind","number","title","teacher_note","blocks" (teacher_note để chuỗi rỗng — máy tự điền).

### Chặng "practice1" — title "Luyện tập 1 — Nhận biết", number 3. Thứ tự khối:
- {"type":"para","text":"\\textbf{Đích của buổi học:} Bài 8 — giải phương trình $\\dfrac{300}{x}-\\dfrac{300}{x+10}=1$ của bài toán hai tổ sản xuất (đề minh họa Vào 10, Sở GD\\&ĐT Hà Nội). Mạch 1 và Mạch 2 luyện Bước 1, Bước 2, Mạch 3 luyện nhẩm nghiệm cho Bước 3, Mạch 4 ghép đủ bốn bước."}
- heading "Mạch 1. Tìm điều kiện xác định" → Ví dụ 1 → Bài 1.
- heading "Mạch 2. Quy đồng mẫu và khử mẫu" → Ví dụ 2 → Bài 2.
- heading "Mạch 3. Nhẩm nghiệm của phương trình bậc hai" → Ví dụ 3 → Bài 3.
- heading "Mạch 4. Giải trọn phương trình chứa ẩn ở mẫu" → Ví dụ 4 → Bài 4.
Yêu cầu từng khối (phương trình lấy ĐÚNG sơ đồ):
- Ví dụ 1: "Tìm điều kiện xác định của mỗi phương trình sau." a), b), lời giải kiểu [dkxd] (ý b phân tích mẫu $x^2-5x$).
- Bài 1 (NB, 3 ý, khung [dkxd] — ý có mẫu $x^2-16$, $x^2-2x$ thì có dòng "Ta có … = \ldots\ldots").
- Ví dụ 2: "Cho phương trình … Tìm ĐKXĐ, quy đồng mẫu rồi khử mẫu để đưa phương trình về dạng $ax^2+bx+c=0$ và chỉ ra các hệ số $a$, $b$, $c$." Lời giải kiểu [khu].
- Bài 2 (NB, 3 ý, khung [khu]: dòng ĐKXĐ, dòng mẫu thức chung, dòng sau khử mẫu, dòng thu gọn, dòng hệ số). Đề Bài 2 viết "(chưa cần giải)".
- Ví dụ 3: "Nhẩm nghiệm của các phương trình sau." a) $a+b+c=0$, b) $a-b+c=0$, kiểu [nham].
- Bài 3 (NB, 3 ý, khung [nham]: dòng hệ số, dòng tính $a+b+c$ hoặc $a-b+c$ với chỗ chấm, dòng nghiệm). Ý nào dùng $a+b+c$ hay $a-b+c$ thì KHÔNG in sẵn — khung để "$a\\ldots b+c=\\ldots\\ldots$" cho HS tự chọn.
- Ví dụ 4: "Giải phương trình …" kiểu [giai4] (nhẩm $a+b+c=0$, loại $x=1$).
- Bài 4 (NB, 3 ý, khung [giai4] đủ 4 bước). Ý a nhẩm $a+b+c$, ý b nhẩm $a-b+c$ và nhận cả hai, ý c khuyết $c$ (đặt nhân tử chung) — khung từng ý theo đúng cách giải của ý đó, không in sẵn chữ "loại"/"không thỏa mãn".

### Chặng "practice2" — title "Luyện tập 2 — Thông hiểu \& Vận dụng", number 4. Thứ tự: Ví dụ 5 → Bài 5. → Bài 6. → Ví dụ 6 → Bài 7. → Bài 8.
- Ví dụ 5: "Giải phương trình …" (mẫu $x^2-2x$ phân tích, sau khử mẫu dùng $\Delta'$, loại $x=2$).
- Bài 5 (TH, 3 ý, "Giải các phương trình sau."), nguồn theo sơ đồ. Ý b mẫu $x^2-2x-3=(x-3)(x+1)$ — đề GIỮ nguyên dạng $x^2-2x-3$, lời giải có dòng phân tích $x^2-2x-3=x^2-3x+x-3=(x-3)(x+1)$.
- Bài 6 (TH, 2 ý, "Giải các phương trình sau."). Ý a có hai mẫu đối nhau $x-2$ và $2-x$. Ý b mẫu vế phải viết $(x-3)(x+1)$.
- Ví dụ 6 (bài thực tế, phương trình cho sẵn): "Quãng đường từ A đến B dài $90$ km. Một xe máy và một ô tô cùng khởi hành từ A đi B, vận tốc ô tô lớn hơn vận tốc xe máy $15$ km/h nên ô tô đến B sớm hơn xe máy $1$ giờ. Gọi vận tốc xe máy là $x$ (km/h, $x>0$) thì lập được phương trình $\dfrac{90}{x}-\dfrac{90}{x+15}=1$. Giải phương trình rồi tính vận tốc mỗi xe." — lời giải [tt]: khử mẫu $90(x+15)-90x=x(x+15)$, $x^2+15x-1350=0$, $\Delta=5625$, $x_1=30$, $x_2=-45$ loại, ô tô $45$ km/h.
- Bài 7 (VD, một bài): "[VD] Bố chở Nam đi từ trường đến khu du lịch cách đó $50$ km bằng xe máy. Các bạn trong lớp đi ô tô với vận tốc lớn hơn vận tốc xe máy $20$ km/h nên bố Nam phải xuất phát trước $25$ phút để hai xe đến nơi cùng lúc. Gọi vận tốc xe máy là $x$ (km/h, $x>0$) thì lập được phương trình $\dfrac{50}{x}-\dfrac{50}{x+20}=\dfrac{5}{12}$. Giải phương trình rồi cho biết vận tốc mỗi xe. \;(thi thử Vào 10 lần 5, Phòng GD\&ĐT Chương Mỹ)" — mẫu thức chung $12x(x+20)$, $600(x+20)-600x=5x(x+20)$, chia $5$: $x^2+20x-2400=0$, $\Delta'=2500$, $x=40$, ô tô $60$ km/h.
- Bài 8 (VD, một bài, ĐÍCH): "[VD] Hai tổ sản xuất cùng phải làm $300$ sản phẩm. Mỗi ngày tổ B làm nhiều hơn tổ A $10$ sản phẩm nên tổ B hoàn thành sớm hơn tổ A $1$ ngày. Gọi số sản phẩm tổ A làm mỗi ngày là $x$ ($x$ nguyên dương) thì lập được phương trình $\dfrac{300}{x}-\dfrac{300}{x+10}=1$. Giải phương trình rồi cho biết mỗi tổ làm xong trong bao nhiêu ngày. \;(đề minh họa Vào 10, Sở GD\&ĐT Hà Nội)" — $300(x+10)-300x=x(x+10)$, $x^2+10x-3000=0$, $\Delta'=3025$, $x_1=50$, $x_2=-60$ loại, tổ A $6$ ngày, tổ B $5$ ngày.

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Ví dụ {i}." for i in range(1, 7)], *[f"Bài {i}." for i in range(1, 9)]) + "\n"

PROMPT_BTVN = CHUNG + r'''
## Việc C: dựng phần BÀI TẬP VỀ NHÀ (mọi bài "tier":"btvn", Bài 9. đến Bài 16.)
Không có ví dụ, không tiêu đề mạch. Trả về MỘT stage {"kind":"reflection","number":5,"title":"Tổng kết","teacher_note":"","blocks":[8 bài]} và "ghi_chu".
Các bài NB (9–12) là khung điền khuyết, mỗi ý theo đúng các dòng của ví dụ tương ứng trên lớp (đề mở bằng "Điền vào chỗ chấm để hoàn thành bài giải (làm đủ các bước như Ví dụ N)."):
- Bài 9. NB 3 ý — khung [dkxd] (như Ví dụ 1).
- Bài 10. NB 2 ý — khung [khu] (như Ví dụ 2), "(chưa cần giải)".
- Bài 11. NB 3 ý — khung [nham] (như Ví dụ 3), không in sẵn dấu của $a\pm b+c$.
- Bài 12. NB 2 ý — khung [giai4] (như Ví dụ 4). Ý b nhận cả hai nghiệm — không in sẵn chữ "loại".
Các bài tự trình bày (statement chỉ có đề, có "hints"):
- Bài 13. TH 3 ý: "Giải các phương trình sau." Ý a nguồn theo sơ đồ.
- Bài 14. TH 2 ý: "Giải các phương trình sau." Ý a có hai mẫu đối nhau $x-1$ và $1-x$.
- Bài 15. VD: "[VD] Một đội trồng cây phải trồng $120$ cây. Thực tế mỗi ngày đội trồng nhiều hơn kế hoạch $4$ cây nên hoàn thành sớm hơn kế hoạch $1$ ngày. Gọi số cây đội trồng mỗi ngày theo kế hoạch là $x$ ($x$ nguyên dương) thì lập được phương trình $\dfrac{120}{x}-\dfrac{120}{x+4}=1$. Giải phương trình rồi cho biết theo kế hoạch đội trồng xong trong bao nhiêu ngày." — $x^2+4x-480=0$, $\Delta'=484$, $x_1=20$, $x_2=-24$ loại, $120:20=6$ ngày.
- Bài 16. VD: "[VD] Một người đi xe đạp từ A đến B cách nhau $24$ km. Lúc về, người đó đi với vận tốc lớn hơn lúc đi $4$ km/h nên thời gian về ít hơn thời gian đi $30$ phút. Gọi vận tốc lúc đi là $x$ (km/h, $x>0$) thì lập được phương trình $\dfrac{24}{x}-\dfrac{24}{x+4}=\dfrac{1}{2}$. Giải phương trình rồi cho biết vận tốc lúc đi và lúc về." — mẫu thức chung $2x(x+4)$, $48(x+4)-48x=x(x+4)$, $x^2+4x-192=0$, $\Delta'=196$, $x_1=12$, $x_2=-16$ loại, lúc về $16$ km/h.

## Sơ đồ đề và đáp số (máy đã kiểm)
''' + so_do(*[f"Bài {i}." for i in range(9, 17)]) + "\n"


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
             "timeout": "1800s", "meta": {"loai": "sua-phieu-b", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
