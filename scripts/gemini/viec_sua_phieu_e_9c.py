#!/usr/bin/env python3
"""Sinh 2 việc Gemini sửa phiếu E ch.VI 9C (Bài 21. Giải bài toán bằng cách lập phương trình) — 12/11/2026.

Lỗi đã soát (Claude):
  - validate CHẶN: điền khuyết đứng sau tự trình bày (Bài 2,3,4,8 trên lớp; Bài 19,20,21,25 BTVN), "Hôm nay" ở Bài 17,
    chưa `btvn_phieu_rieng`.
  - vi phạm [[ly-thuyet-chi-la-ly-thuyet]]: "khuôn Câu III.1", "thang điểm của Sở", "mất 0,25 điểm", thẻ "lấy chắc";
    lý thuyết dạy "4 bước" trong khi SGK KNTT 9 tập 2 tr.25 ghi 3 bước.
  - luật cứng "mỗi bài một đề gốc": 6 ví dụ chép y bài, 4 cặp bài trên lớp ↔ BTVN trùng đề.
  - 80 dấu ";" nối công thức.

Việc A (sua-9c-ch6-phieu-e-a): opener, nhắc lại, Kiến thức cần nhớ (SGK), sơ đồ, ghi chú GV, đề NB đổi sang điền khuyết.
Việc B (sua-9c-ch6-phieu-e-b): 10 ví dụ đề mới (số Claude chọn, SymPy đã kiểm), 4 bài thay đề, dàn dòng, gợi ý TH.

    python3 scripts/gemini/viec_sua_phieu_e_9c.py
    python3 scripts/gemini/tho.py --mot sua-9c-ch6-phieu-e-a   (và -b)
    python3 scripts/gemini/lap_sua_phieu_e_9c.py [--ghi]
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
SEED = f"{D}/phieu-e-giai-bai-toan-bang-cach-lap-phuong-trinh.json"
VID_A, VID_B = "sua-9c-ch6-phieu-e-a", "sua-9c-ch6-phieu-e-b"
LABELS_A = ["Bài 1.", "Bài 2.", "Bài 3.", "Bài 4.", "Bài 8.", "Bài 10.", "Bài 17.",
            "Bài 19.", "Bài 20.", "Bài 21.", "Bài 25."]
LABELS_B = [f"Ví dụ {i}." for i in range(1, 11)] + [
    "Bài 12.", "Bài 13.", "Bài 14.", "Bài 15.", "Bài 16.", "Bài 27.", "Bài 29.", "Bài 30.",
    "Bài 31.", "Bài 32.", "Bài 33.", "Bài 34."]
CO_GOI_Y = ["Bài 12.", "Bài 13.", "Bài 14.", "Bài 15.", "Bài 29.", "Bài 30.", "Bài 31.", "Bài 32."]

CHUNG = r'''Bạn là thợ sửa phiếu học tập Toán 9 (ĐẠI SỐ — chương VI, Bài 21 "Giải bài toán bằng cách lập phương trình", SGK Kết nối tri thức) cho học sinh lớp 9 TẦNG C (học lực trung bình). Làm CẨN THẬN, CHỈ sửa đúng phạm vi được giao, KHÔNG bịa đề thi, KHÔNG bịa nguồn.
KHÔNG chạy lệnh, KHÔNG mở file: mọi dữ liệu nằm cuối prompt (trích từ seed phiếu). Xuống dòng trong chuỗi là [[br]]. Toán viết LaTeX trong $...$; phân số \dfrac; giữ escape \& (ví dụ "GD\&ĐT"); JSON hợp lệ.

## Luật giáo viên đã chốt (vi phạm là bị trả lại)
- BỎ HẾT chữ/ý "khuôn", "Câu III", cấu trúc đề thi, thang điểm, "mất 0,25 điểm", "ăn điểm", "lấy chắc", "tầng C". Trích nguồn đề dạng "\;(thi thử Vào 10 lần 4, Phòng GD\&ĐT Chương Mỹ)" sau đề bài thì GIỮ NGUYÊN.
- Không văn nói, không xưng hô: cấm "em", "các em", "ta đi", "hôm nay", "Hôm nay", "việc của ta", "Kiểm" (viết "Kiểm tra"), "Soi". Đề viết như đề thi.
- KHÔNG dùng dấu chấm phẩy ";" (trừ "\;" là khoảng trắng LaTeX). Hai công thức/hai ý thì xuống dòng [[br]] hoặc nối bằng chữ "và", hoặc dấu phẩy.
- Lời giải theo nhịp đi thi: mỗi bước một dòng (ngăn bằng [[br]]), căn cứ trước kết quả sau, câu "Vậy …" đứng dòng riêng ở cuối. Không dùng "Do đó", "Suy ra", "suy ra", "Như vậy", "Mặt khác" (thay bằng xuống dòng, hoặc "nên", hoặc "Theo đề bài, ta có phương trình").
- Giữ nguyên thẻ mức "[NB]", "[TH]", "[VD]" ở đầu mỗi ý a), b)… (bài VD một ý thì thẻ "[VD]" ở đầu đề). Không thêm/bớt ý, không đổi "label".
- Tự tính lại MỌI đáp số mình viết. Thấy chỗ nào nghi sai thì ghi vào "ghi_chu".
'''

PROMPT_A = CHUNG + r'''
## Việc 1 — "opener_text" (đoạn mở màn, hình vẽ giữ nguyên: xe máy $x$ km/h, ô tô $x+20$ km/h, quãng đường $50$ km)
2–3 câu, không xưng hô, không "hôm nay", không "ta": nêu tình huống (bố chở Nam bằng xe máy, các bạn đi ô tô nhanh hơn $20$ km/h, quãng đường $50$ km, bố Nam phải xuất phát trước $25$ phút để đến cùng lúc) rồi đặt câu hỏi: đại lượng nào chưa biết, và thời gian đi của hai xe chênh nhau bao nhiêu.

## Việc 2 — "review_note" (thẻ "Nhắc lại kiến thức đã học", một chuỗi)
Hai gạch đầu dòng "$\bullet$\; ", xuống dòng [[br]], KHÔNG chấm phẩy:
- Công thức chuyển động $s=v\cdot t$, $t=\dfrac{s}{v}$, $v=\dfrac{s}{t}$ (nối bằng dấu phẩy hoặc "và"). Bài năng suất: khối lượng công việc $=$ năng suất $\times$ thời gian.
- Các bước giải phương trình chứa ẩn ở mẫu: tìm điều kiện xác định, quy đồng mẫu hai vế rồi khử mẫu, giải phương trình nhận được, đối chiếu điều kiện rồi kết luận.

## Việc 3 — "concept_blocks" (chặng "Kiến thức cần nhớ" — CHỈ LÀ LÝ THUYẾT)
Khuôn trình bày: cặp {"type":"para","text":"\\textbf{N. Tên mục}"} rồi {"type":"para","text": nội dung}. Đúng 3 mục:
1. "\textbf{1. Các bước giải bài toán bằng cách lập phương trình}" — CHÉP ĐÚNG CHỮ SGK (tr.25):
   \textit{Bước 1.} Lập phương trình:[[br]]$-$ Chọn ẩn số và đặt điều kiện thích hợp cho ẩn số.[[br]]$-$ Biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết.[[br]]$-$ Lập phương trình biểu thị mối quan hệ giữa các đại lượng.[[br]]\textit{Bước 2.} Giải phương trình.[[br]]\textit{Bước 3.} Trả lời: Kiểm tra xem trong các nghiệm của phương trình, nghiệm nào thoả mãn điều kiện của ẩn, nghiệm nào không, rồi kết luận.
2. "\textbf{2. Một số công thức thường dùng}" — gạch đầu dòng "$\bullet$\; ": chuyển động $s=v\cdot t$ (quãng đường, vận tốc, thời gian) và $t=\dfrac{s}{v}$; năng suất: khối lượng công việc $=$ năng suất $\times$ thời gian; làm chung: làm xong một công việc trong $a$ giờ thì mỗi giờ làm được $\dfrac{1}{a}$ công việc; hình chữ nhật: diện tích $=$ chiều dài $\times$ chiều rộng; đổi đơn vị: $m$ phút $=\dfrac{m}{60}$ giờ (ví dụ $30$ phút $=\dfrac{1}{2}$ giờ).
3. "\textbf{3. Điều kiện của ẩn}" — số sản phẩm, số xe, số ngày, số người là số nguyên dương. Vận tốc, độ dài, diện tích, thời gian là số dương. Nếu ẩn nằm ở mẫu thì mẫu phải khác $0$.
KHÔNG thêm thẻ bẫy, thẻ mục tiêu, mẹo "dịch lời văn", bảng điểm hay bất cứ thứ gì khác.

## Việc 4 — "mindmap" (sơ đồ tư duy điền khuyết theo 3 bước SGK)
{"type":"mindmap","caption":"Điền các ô trống để tự tổng kết các bước giải bài toán bằng cách lập phương trình","root":"Giải bài toán bằng cách lập phương trình","branches":[…]} — đúng 3 nhánh "Bước 1. Lập phương trình", "Bước 2. Giải phương trình", "Bước 3. Trả lời"; nhánh 1 có 3 con (chọn ẩn và [[blank:1.6cm]], biểu diễn đại lượng chưa biết theo [[blank:1.2cm]], lập phương trình biểu thị [[blank:1.6cm]]), nhánh 2 có 1–2 con (ví dụ "Ẩn ở mẫu: tìm [[blank:1.6cm]] trước"), nhánh 3 có 2 con (đối chiếu nghiệm với [[blank:1.6cm]], kết luận kèm [[blank:1.2cm]]). Mỗi con ngắn dưới 40 kí tự hiển thị.

## Việc 5 — "teacher_notes" (ghi chú giáo viên, bỏ hết "khuôn", "Câu III", điểm số; giữ nhịp thời gian bản cũ)
Khoá: "review" (mở màn 8 phút, chỉ hỏi ẩn là gì và chênh nhau bao nhiêu, quay lại ở Bài 13a), "concept" (giảng 45 phút: đọc 3 bước SGK, kẻ bảng đại lượng lên bảng giữ suốt buổi, Ví dụ 5 và 6 chỉ dừng ở khâu lập phương trình, ví dụ mồi pizza làm trước Ví dụ 8), "practice1" (48 phút: Bài 3 và Bài 4 điền trước, chữa xong mới sang Bài 7; Bài 11b nhấn đề hỏi vận tốc MỖI xe thì phải trả lời đủ hai xe), "practice2" (48 phút: Bài 12, 13 chỉ lập phương trình, chấm riêng khâu lập; Bài 17 đề hỏi vận tốc lúc tăng tốc $x+6$ chứ không phải $x$, và còn câu hỏi phụ về giới hạn tốc độ), "reflection" (sơ đồ tư duy 5 phút cuối buổi; Bài tập về nhà là Bài 18–Bài 33, khoảng 95 phút, in thành phiếu riêng; buổi sau chữa Bài 32 và Bài 33 trước).

## Việc 6 — "sua": sửa đề + lời giải 11 bài NB (dữ liệu gốc ở cuối)
Mục tiêu: MỌI bài NB thành bài ĐIỀN KHUYẾT — mỗi ý a), b), c) phải có chỗ chấm \ldots\ldots để học sinh điền (bảng đại lượng bị bỏ, giáo viên tự kẻ lên bảng).
- Bài 1.: "Điền vào chỗ chấm để hoàn thành các bước giải bài toán bằng cách lập phương trình." Ba ý theo đúng 3 bước SGK: a) [NB] Bước 1. Lập phương trình: chọn ẩn số và \ldots\ldots, biểu diễn \ldots\ldots, lập phương trình \ldots\ldots b) [NB] Bước 2. \ldots\ldots c) [NB] Bước 3. Trả lời: kiểm tra xem \ldots\ldots, rồi kết luận. solution là phần chữ SGK cần điền.
- Bài 2.: giữ nguyên 3 ý và nguồn, mỗi ý thêm khung "Gọi \ldots\ldots là $x$ (\ldots), điều kiện \ldots\ldots". solution giữ đáp án cũ.
- Bài 3., Bài 4., Bài 20., Bài 21.: đề bỏ chữ "Điền vào bảng dưới", mỗi ý thành "a) [NB] Số ngày theo kế hoạch: \ldots\ldots (ngày)" (đơn vị đúng từng ý). Bỏ ";" trong đề Bài 3 (dùng dấu phẩy hoặc tách câu). solution giữ đáp án cũ.
- Bài 8., Bài 25.: đề "Quy đồng mẫu hai vế rồi khử mẫu, điền vào chỗ chấm để đưa phương trình về dạng $ax^2+bx+c=0$ (chưa cần giải)." mỗi ý thành dòng có chỗ chấm, ví dụ "a) [NB] $\dfrac{300}{x}-\dfrac{300}{x+10}=1$[[br]]\hspace*{1.4em}$300(x+10)-300x=\ldots\ldots$[[br]]\hspace*{1.4em}$\ldots\ldots=0$". solution: hai dòng tương ứng, đúng đáp số cũ (kiểm lại bằng tay).
- Bài 10.: bỏ chữ "Câu III.1" (viết "hoàn thành bài giải bài toán sau"), bỏ mọi ";" ở đề và solution (mỗi chỗ chấm một dòng). Giữ số liệu và đáp số.
- Bài 17.: đổi "Hôm nay $3$ km đầu" thành "Một hôm, $3$ km đầu". Bỏ ";" ở đề (tách câu). solution viết lại theo nhịp đi thi (mỗi bước một dòng, "Vậy" dòng riêng, trả lời đủ hai câu hỏi). Đáp số đúng: vận tốc thường ngày $x=30$ km/h, lúc tăng tốc $36$ km/h, $36<40$ nên Nam không vi phạm.
- Bài 19.: giữ nguyên 3 ý và nguồn, thêm khung "Gọi \ldots\ldots là $x$ (\ldots), điều kiện \ldots\ldots" như Bài 2.

## Đầu ra
JSON đúng schema: {"opener_text","review_note","concept_blocks","mindmap","teacher_notes":{"review","concept","practice1","practice2","reflection"},"sua":[11 phần tử {"label","statement","solution","hints":[]}],"ghi_chu"}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''

PROMPT_B = CHUNG + r'''
## Vì sao phải sửa
Luật cứng: mỗi bài, mỗi ví dụ, mỗi bài tập về nhà phải là MỘT ĐỀ GỐC KHÁC NHAU. Bản cũ có 6 ví dụ chép y đề bài (Ví dụ 3 = Bài 4, Ví dụ 5 = Bài 12a, Ví dụ 6 = Bài 13b, Ví dụ 8 = Bài 15a, Ví dụ 9 = Bài 10, Ví dụ 10 = Bài 13a) và 4 cặp bài trên lớp ↔ về nhà trùng đề. Giáo viên đã chọn đề mới (số liệu dưới đây ĐÃ KIỂM bằng máy — dùng đúng số này, không đổi).

## Việc 1 — viết lại 10 ví dụ (label "Ví dụ N.", trường "statement" = TOÀN BỘ text của thẻ, "solution" để chuỗi rỗng)
Khuôn text giữ y bản cũ: "\textbf{Ví dụ N.} <đề>[[br]]{\sffamily\bfseries\color{brand}Lời giải}[[br]]\hspace*{1.4em}<dòng 1>[[br]]\hspace*{1.4em}<dòng 2>…". Mỗi bước một dòng, "Vậy …" dòng cuối riêng. Ví dụ mới KHÔNG ghi nguồn đề thi (đề tự soạn).
- Ví dụ 1.: Một xưởng may theo kế hoạch phải may $480$ chiếc áo. Đặt ẩn và nêu điều kiện cho câu hỏi "theo kế hoạch mỗi ngày xưởng may bao nhiêu chiếc áo". Lời giải: Gọi số áo mỗi ngày theo kế hoạch là $x$ (chiếc), $x$ nguyên dương (thêm $x>8$ không cần ở ví dụ này).
- Ví dụ 2.: Vẫn xưởng may trên, thực tế mỗi ngày may ÍT hơn kế hoạch $8$ chiếc. Biểu diễn theo $x$: số ngày theo kế hoạch $\dfrac{480}{x}$, số áo mỗi ngày thực tế $x-8$ (điều kiện thêm $x>8$), số ngày thực tế $\dfrac{480}{x-8}$.
- Ví dụ 3.: Hai xe máy cùng khởi hành từ $A$ đến $B$, quãng đường $AB$ dài $45$ km. Xe thứ nhất đi với vận tốc $x$ km/h, xe thứ hai nhanh hơn xe thứ nhất $15$ km/h. Biểu diễn thời gian đi của mỗi xe theo $x$: $\dfrac{45}{x}$ giờ và $\dfrac{45}{x+15}$ giờ.
- Ví dụ 4.: Đổi $15$ phút và $40$ phút sang giờ ($\dfrac{1}{4}$ và $\dfrac{2}{3}$), rồi viết hệ thức cho câu "xe thứ hai đến $B$ sớm hơn xe thứ nhất $15$ phút" (bài Ví dụ 3): $\dfrac{45}{x}-\dfrac{45}{x+15}=\dfrac{1}{4}$.
- Ví dụ 5. (chỉ LẬP phương trình): Một đội xe dự định dùng một số xe cùng loại để chở hết $36$ tấn hàng. Khi chở, đội được bổ sung thêm $3$ xe cùng loại nên mỗi xe chở ít hơn dự định $1$ tấn. Lập phương trình để tìm số xe dự định. Lời giải: gọi số xe dự định là $x$ (xe), $x$ nguyên dương. Mỗi xe dự định chở $\dfrac{36}{x}$ tấn, số xe thực tế $x+3$, mỗi xe thực tế chở $\dfrac{36}{x+3}$ tấn. Phương trình $\dfrac{36}{x}-\dfrac{36}{x+3}=1$.
- Ví dụ 6. (chỉ LẬP phương trình): Quãng đường $AB$ dài $60$ km. Một người đi xe máy từ $A$ đến $B$, lúc về người đó đi chậm hơn lúc đi $5$ km/h nên thời gian về nhiều hơn thời gian đi $24$ phút. Lập phương trình để tìm vận tốc lúc đi. Lời giải: gọi vận tốc lúc đi là $x$ (km/h), $x>5$. Thời gian đi $\dfrac{60}{x}$ giờ, vận tốc lúc về $x-5$, thời gian về $\dfrac{60}{x-5}$ giờ, $24$ phút $=\dfrac{2}{5}$ giờ. Phương trình $\dfrac{60}{x-5}-\dfrac{60}{x}=\dfrac{2}{5}$.
- Ví dụ 7. (lập và giải): Một mảnh vườn hình chữ nhật có chu vi $34$ m và diện tích $60$ m$^2$. Tính chiều dài và chiều rộng. Lời giải: nửa chu vi $17$ m. Gọi chiều rộng là $x$ (m), $0<x<\dfrac{17}{2}$. Chiều dài $17-x$ (m). Phương trình $x(17-x)=60$, tức $x^2-17x+60=0$. $\Delta=(-17)^2-4\cdot 1\cdot 60=49$, $\sqrt{\Delta}=7$. $x_1=\dfrac{17+7}{2}=12$ (loại vì $12>\dfrac{17}{2}$), $x_2=\dfrac{17-7}{2}=5$ (thoả mãn). Vậy chiều rộng $5$ m, chiều dài $12$ m.
- Ví dụ 8. (lập và giải): Hai đội công nhân cùng làm một công việc thì sau $2$ giờ $24$ phút xong. Nếu làm riêng thì đội thứ nhất xong sớm hơn đội thứ hai $2$ giờ. Hỏi làm riêng thì mỗi đội mất bao lâu? Lời giải: $2$ giờ $24$ phút $=\dfrac{12}{5}$ giờ. Gọi thời gian đội thứ nhất làm riêng là $x$ (giờ), $x>0$. Đội thứ hai $x+2$ (giờ). Mỗi giờ đội thứ nhất làm $\dfrac{1}{x}$, đội thứ hai $\dfrac{1}{x+2}$, cả hai $\dfrac{5}{12}$ công việc. Phương trình $\dfrac{1}{x}+\dfrac{1}{x+2}=\dfrac{5}{12}$. Khử mẫu: $12(x+2)+12x=5x(x+2)$, tức $5x^2-14x-24=0$. $\Delta'=(-7)^2-5\cdot(-24)=169$, $\sqrt{\Delta'}=13$. $x_1=\dfrac{7+13}{5}=4$ (thoả mãn), $x_2=\dfrac{7-13}{5}=-\dfrac{6}{5}$ (loại). Vậy đội thứ nhất $4$ giờ, đội thứ hai $6$ giờ.
- Ví dụ 9. (lập và giải): Theo kế hoạch, một xưởng phải may $480$ chiếc áo trong một số ngày. Thực tế mỗi ngày xưởng may ít hơn kế hoạch $8$ chiếc nên hoàn thành chậm hơn $2$ ngày. Hỏi theo kế hoạch mỗi ngày xưởng phải may bao nhiêu chiếc áo? Lời giải: gọi $x$ (chiếc) là số áo mỗi ngày theo kế hoạch, $x$ nguyên, $x>8$. Phương trình $\dfrac{480}{x-8}-\dfrac{480}{x}=2$. Khử mẫu: $480x-480(x-8)=2x(x-8)$, tức $x^2-8x-1920=0$. $\Delta'=(-4)^2+1920=1936$, $\sqrt{\Delta'}=44$. $x_1=4+44=48$ (thoả mãn), $x_2=4-44=-40$ (loại). Vậy theo kế hoạch mỗi ngày xưởng may $48$ chiếc áo.
- Ví dụ 10. (lập và giải, cùng bài Ví dụ 3, 4): Hai xe máy cùng khởi hành từ $A$ đến $B$ dài $45$ km. Xe thứ hai đi nhanh hơn xe thứ nhất $15$ km/h nên đến $B$ sớm hơn xe thứ nhất $15$ phút. Tính vận tốc mỗi xe. Lời giải: gọi vận tốc xe thứ nhất là $x$ (km/h), $x>0$. Phương trình $\dfrac{45}{x}-\dfrac{45}{x+15}=\dfrac{1}{4}$. Khử mẫu: $180(x+15)-180x=x(x+15)$, tức $x^2+15x-2700=0$. $\Delta=15^2+4\cdot 2700=11025$, $\sqrt{\Delta}=105$. $x_1=\dfrac{-15+105}{2}=45$ (thoả mãn), $x_2=\dfrac{-15-105}{2}=-60$ (loại). Vậy xe thứ nhất $45$ km/h, xe thứ hai $60$ km/h.

## Việc 2 — 4 bài thay đề (giữ thẻ mức, giữ ý còn lại)
- Bài 12.: GIỮ ý a). Ý b) thay bằng: "[TH] Một xưởng may phải may $1\,500$ chiếc áo trong thời gian quy định. Để hoàn thành sớm kế hoạch, mỗi ngày xưởng đã may được nhiều hơn $10$ chiếc áo so với số áo phải may trong một ngày theo kế hoạch. Vì thế ba ngày trước khi hết thời hạn, xưởng đã may được $1\,320$ áo. \;(SGK Toán 9 tập hai, Bài 6.33)". Lời giải b) chỉ lập: gọi $x$ (chiếc) là số áo mỗi ngày theo kế hoạch, $x$ nguyên dương. Thời gian quy định $\dfrac{1500}{x}$ ngày, số ngày thực tế đã may $\dfrac{1500}{x}-3$, mỗi ngày thực tế $x+10$ chiếc. Phương trình $\left(\dfrac{1500}{x}-3\right)(x+10)=1320$.
- Bài 27.: thay bài toán thành "mảnh đất hình chữ nhật có chiều dài hơn chiều rộng $4$ m và diện tích $96$ m$^2$. Tính hai kích thước." (BỎ nguồn Đống Đa). Giữ khung điền khuyết như cũ nhưng mỗi chỗ chấm một dòng, không ";". Đáp số: điều kiện $x>0$, chiều dài $x+4$, phương trình $x(x+4)=96$ tức $x^2+4x-96=0$, $x=8$ và $x=-12$, loại $x=-12$, vậy rộng $8$ m, dài $12$ m.
- Bài 29.: GIỮ ý b). Ý a) thay bằng: "[TH] Một đội xe gồm các xe tải cùng loại cần phải chở $120$ tấn hàng. Khi làm việc, có hai xe phải điều chuyển đi nơi khác nên mỗi xe phải chở thêm $3$ tấn hàng. Tìm số xe tải của đội. \;(SGK Toán 9 tập hai, Luyện tập trang 27)". Lời giải a) chỉ lập: gọi số xe của đội là $x$ (xe), $x$ nguyên, $x>2$. Mỗi xe dự định chở $\dfrac{120}{x}$, thực tế $\dfrac{120}{x-2}$ tấn. Phương trình $\dfrac{120}{x-2}-\dfrac{120}{x}=3$.
- Bài 30.: GIỮ ý b). Ý a) thay bằng: "[TH] Một ô tô khách khởi hành từ Hà Nội đi Hải Phòng. Sau đó $30$ phút, một ô tô con xuất phát từ cùng địa điểm ở Hà Nội và cũng đi về Hải Phòng trên cùng tuyến đường, với vận tốc lớn hơn vận tốc của ô tô khách là $20$ km/h. Hai xe đến Hải Phòng cùng một thời điểm. Quãng đường Hà Nội – Hải Phòng dài khoảng $120$ km. Tìm vận tốc mỗi ô tô. \;(SGK Toán 9 tập hai, Bài 6.32)". Lời giải a) chỉ lập: gọi vận tốc ô tô khách là $x$ (km/h), $x>0$. Ô tô con $x+20$. Phương trình $\dfrac{120}{x}-\dfrac{120}{x+20}=\dfrac{1}{2}$.

## Việc 3 — dàn dòng các bài còn lại (Bài 13., 14., 15., 16., 31., 32., 33., 34. và phần GIỮ của Bài 12., 29., 30.)
Giữ nguyên đề và số liệu. Chỉ: bỏ ";" (ở cả đề lẫn lời giải), viết lời giải theo nhịp đi thi (mỗi bước một dòng, "Vậy" dòng riêng, bỏ "Do đó/suy ra"). Bài nhiều ý thì dòng con thụt "\hspace*{1.4em}" như bản cũ. Tự tính lại từng đáp số.

## Việc 4 — "hints" cho 8 bài Thông hiểu: Bài 12., 13., 14., 15., 29., 30., 31., 32.
Mỗi bài 1–2 câu gợi ý định hướng dạng CÂU HỎI (kiểu Polya: "Đại lượng nào chưa biết?", "Hai thời gian chênh nhau bao nhiêu giờ?", "Mỗi giờ mỗi vòi chảy được bao nhiêu phần bể?"), không gọi tên công thức, không lộ đáp số. Các bài khác "hints": [].

## Đầu ra
JSON đúng schema: {"sua":[22 phần tử {"label","statement","solution","hints"}, đủ Ví dụ 1.–Ví dụ 10. và Bài 12., 13., 14., 15., 16., 27., 29., 30., 31., 32., 33., 34.],"ghi_chu"}. "statement"/"solution" là chuỗi HOÀN CHỈNH thay bản cũ.
'''


def khoi(seed):
    out = {}
    for s in seed["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                out[b["label"]] = b
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m:
                    out[m.group(1)] = b
    return out


def goc(seed, labels):
    k = khoi(seed)
    ds = []
    for lb in labels:
        b = k[lb]
        if b["type"] == "problem":
            ds.append({"label": lb, "statement": b["statement"], "solution": b.get("solution", ""),
                       "hints": b.get("hints") or []})
        else:
            ds.append({"label": lb, "statement": b["text"], "solution": "", "hints": []})
    return ds


def main():
    seed = json.loads((REPO / SEED).read_text())
    st = {s["kind"]: s for s in seed["stages"]}
    cu = {"opener": st["review"]["blocks"][0]["text"], "review_note": st["review"]["blocks"][2]["text"],
          "concept_cu_BO": st["concept"]["blocks"], "mindmap_cu": st["reflection"]["blocks"][0],
          "teacher_notes_cu": {k: st[k].get("teacher_note", "") for k in st}}
    viec = [
        (VID_A, PROMPT_A + "\n## Dữ liệu gốc — bản cũ (chỉ để biết đã có gì)\n" + json.dumps(cu, ensure_ascii=False)
         + "\n\n## Dữ liệu gốc — 11 bài cần sửa\n" + json.dumps(goc(seed, LABELS_A), ensure_ascii=False, indent=1),
         LABELS_A),
        (VID_B, PROMPT_B + "\n## Dữ liệu gốc — 22 khối cần sửa\n" + json.dumps(goc(seed, LABELS_B), ensure_ascii=False, indent=1),
         LABELS_B),
    ]
    for vid, prompt, labels in viec:
        v = {"id": vid, "model": "gemini-3.8-flash-high", "prompt": prompt + "\n", "files": [],
             "schema": "scripts/gemini/schema/sua-phieu-tong.json", "timeout": "1500s",
             "meta": {"loai": "sua-phieu-tong", "seed": SEED, "labels": labels}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự)")


if __name__ == "__main__":
    main()
