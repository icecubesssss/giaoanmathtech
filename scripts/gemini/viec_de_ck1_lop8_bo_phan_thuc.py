#!/usr/bin/env python3
"""6 việc Gemini: DỰNG LẠI 6 đề CK1 lớp 8 (3 ôn + 3 chính thức) theo khung đề thật, BỎ PHÂN THỨC.

Thầy chốt 13/11/2026: phân thức (KNTT Ch.VI, trung tâm dạy t28–32) không thuộc CK1 — 25/26 đề HN đúng
tiến độ không có. Khung mới (đo từ 26 đề, inputs/refs/ngan-hang-sheet/lop-8/ck1/ban-ghi):
  TN 8 câu 2,0 · Bài 1 (1,5) phép tính/HĐT/phân tích 3 ý · Bài 2 (1,0) tìm x 2 ý · Bài 3 (1,0) thống kê ·
  Bài 4 (1,0) Thalès thực tế (có hình) · Bài 5 (3,0) hình tứ giác · Bài 6 (0,5) VDC.
Claude chọn câu thật (KE_HOACH); Gemini chép nguyên văn từ ảnh PDF, viết lời giải/barem, tự tính lại.
Kết quả ⇒ scripts/ck1_lop8_phu_dang.json (Claude soát) ⇒ scripts/ck1_lop8_phu_dang.py vá DE.

    python3 scripts/gemini/viec_de_ck1_lop8_bo_phan_thuc.py
    python3 scripts/gemini/tho.py --tien-to de8-ck1- --song-song 3
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts/gemini"))
from viec_boc_de import ma_de  # noqa: E402
import de_ck1_lop8_hinh as H  # noqa: E402

THU_MUC = REPO / "inputs/refs/de-thi/lop-8/cuoi-ki-1"
PDF = {ma_de(8, "ck1", p): p for p in THU_MUC.glob("*.pdf") if ma_de(8, "ck1", p)}

# Mỗi câu mới: (mã đề ngân hàng, vị trí trong đề gốc, tóm tắt để tìm, đáp số theo bản bóc)
KE_HOACH = {
    "on-1": dict(script="scripts/de_on_tap_ck1_lop8.py", hinh="get_tikz_on1", ke="""
TRẮC NGHIỆM (8 câu): GIỮ câu 1, 3, 5, 6, 7 hiện tại (giu=true). THAY:
 - Câu 2 ⇒ dạng D26: [2324-thanhtri] Câu I.5 «dữ liệu nào không phải là dữ liệu số» (đáp án C).
 - Câu 4 ⇒ dạng D22: [2324-mydinh1] Câu I.8 «BC = 8 cm, M, N trung điểm AB, AC; MN = ?» (đáp án B).
 - Câu 8 ⇒ dạng D23: [2324-unghoa] Câu I.9 «BD là phân giác trong góc B thì …» (đáp án C).
BÀI 1 (1,5đ, 3 ý × 0,5): a) GIỮ ý a hiện tại (D03); b) MỚI D06 [2324-nghiatan] Bài 1 c) «(x + 3)² − (x − 2)(x + 2)» (= 6x + 13); c) GIỮ ý b hiện tại (D08). Barem mỗi ý còn 0,5.
BÀI 2 (1,0đ) «Tìm x, biết:» a) D09 [2526-tantrieu] 2.2a «x(2x − 3) − 2x² = 12» (x = −4); b) D10 [2425-phandinhgiot] 2.2b «2x(x − 7) + 4(7 − x) = 0» (x = 7; x = 2).
BÀI 3 (1,0đ) thống kê: GIỮ NGUYÊN Bài 3 hiện tại.
BÀI 4 (1,0đ) MỚI D24, CÓ HÌNH: [2324-phanchutrinh] Bài 4 ý 1) a) + b) (con đò trên khúc sông BE, AB // EF, AF = 60 m, FC = 30 m, EC = 45 m; a) độ dài BE? = 90 m; b) tiền dầu = 20 250 đồng). Mỗi ý 0,5. hinh = "moi".
BÀI 5 (3,0đ) hình: GIỮ giả thiết, ý a), ý c) và hình (hinh = "giu_hinh_cu"). THAY ý b) (bỏ hình thang cân) bằng: "b) \\textbf{(1,0 điểm)} Chứng minh tứ giác $BDEM$ là hình bình hành." — lời giải: chứng minh D, E là trung điểm của AB, AC (lấy các dòng đang có ở ý b hiện tại) ⇒ DE là đường trung bình ⇒ $DE \\parallel BM$ và $DE = \\dfrac{1}{2}BC = BM$ ⇒ hình bình hành. Ý c) hiện tại dùng "D là trung điểm AB (câu b)" — vẫn đúng. Mã dạng ý b: D15.
BÀI 6 (0,5đ) VDC: GIỮ NGUYÊN Bài 5 hiện tại (đổi nhãn thành Bài 6)."""),
    "on-2": dict(script="scripts/de_on_tap_ck1_lop8.py", hinh="get_tikz_on2", ke="""
TRẮC NGHIỆM: GIỮ câu 1, 3, 5, 7 hiện tại. THAY:
 - Câu 2 ⇒ D07: [2526-dongmy] Câu I.3 «giá trị x³ + 3x² + 3x + 1 tại x = 19» (đáp án B: 8 000).
 - Câu 4 ⇒ D21: [2425-giangvo2] Câu I.5 «DE // BC, AE = 6, EC = 3, AD = 4; DB = ?» (đáp án A: 2).
 - Câu 6 ⇒ D26: [2526-nguyentruongto] Câu I.5 «dữ liệu nào là số liệu rời rạc» (đáp án D).
 - Câu 8 ⇒ D23: [2526-luongthevinh] Câu I.6 «MK phân giác, MN = 8, MP = 12; KN/KP = ?» (đáp án A).
BÀI 1 (1,5đ, 3 ý × 0,5): a) GIỮ ý a hiện tại (D03, chia đa thức); b) MỚI D06 [2425-phandinhgiot] Bài 1 a) «(x + 2)² − (x + 3)(x − 3) + 10» (= 4x + 23); c) MỚI D08 [2526-luongthevinh] Bài 1 b) «x² − 4x + 4 − y²».
BÀI 2 (1,0đ) «Tìm x, biết:» a) GIỮ ý tìm x hiện đang là Bài 1 ý b (D09), barem về 0,5; b) MỚI D10 [2526-thanglong] Bài 3 c) «3x(x + 5) − x − 5 = 0» (x = 1/3; x = −5).
BÀI 3 (1,0đ) MỚI thống kê D27 + D28: [2526-tantrieu] Bài 3 a) + b) (lớp trưởng 8A thống kê sở thích môn thể thao). Mỗi ý 0,5. Chép bảng/dữ liệu bằng tabular như Bài 3 đề ôn 1. Không có biểu đồ phải vẽ sẵn (nếu ý nào yêu cầu HS VẼ biểu đồ thì giữ yêu cầu đó, lời giải mô tả biểu đồ bằng bảng).
BÀI 4 (1,0đ) = Bài 3 HIỆN TẠI (D24, đường trung bình thực tế) — GIỮ NGUYÊN đề + lời giải, đổi nhãn "Bài 4.". Nếu đề hiện tại có hình/nhắc "hình vẽ" mà chưa có hình thì hinh = "moi" và vẽ; nếu không cần hình thì "khong".
BÀI 5 (3,0đ) = Bài 4 hình hiện tại, hinh = "giu_hinh_cu". GIỮ giả thiết và ý a). Thay MỘT trong hai ý b), c) (ý nào ít liên quan ý sau hơn) bằng ý chứng minh một tứ giác là HÌNH BÌNH HÀNH (dạng D15) — CHỈ dùng các điểm đã có trên hình (xem TikZ bên dưới), phát biểu đúng với toạ độ, chứng minh từ giả thiết. Ý còn lại giữ nguyên; nếu ý giữ lại dùng kết quả của ý bị thay thì phải chứng minh lại phần đó bên trong nó. Ghi rõ vào ghi_chu ý nào do bạn đặt (không chép đề).
BÀI 6 (0,5đ): GIỮ NGUYÊN Bài 5 hiện tại."""),
    "on-3": dict(script="scripts/de_on_tap_ck1_lop8.py", hinh="get_tikz_on3", ke="""
TRẮC NGHIỆM: GIỮ câu 1, 3, 5, 7 hiện tại. THAY:
 - Câu 2 ⇒ D02: [2425-phanchutrinh] Câu I.2 «hiệu của xy³ − 2x²y² − 2 và xy³ + x²y² + 1» (đáp án D).
 - Câu 4 ⇒ D21: [2526-nguyentruongto] Câu I.8 «MN // BC, AM = 2MB, AN = 6 cm; NC = ?» (đáp án A: 3 cm).
 - Câu 6 ⇒ D22: [2425-phucdien] Câu I.8 «E, K trung điểm MN, MP; NP = 6 cm; EK = ?» (đáp án C: 3 cm). Đề gốc có hình: nếu chép được bằng lời đủ dữ kiện thì bỏ chữ "hình vẽ".
 - Câu 8 ⇒ D26: [2526-dongmy] Câu I.4 «An đứng từ xa quan sát … phương pháp thu thập» (đáp án A).
BÀI 1 (1,5đ, 3 ý × 0,5): a) MỚI D03 [2324-unghoa] Bài II.1 a/ «2x(3x − 1) − 6x(x − 2)» (= 10x); b) = ý a hiện tại (D06); c) = ý b hiện tại (D08). Barem mỗi ý 0,5.
BÀI 2 (1,0đ) «Tìm x, biết:» a) D09 [2526-dongmy] II.2b «(x + 2)² − x(x + 6) = 10» (x = −3); b) D10 [2324-lequydon] 2.2a «25x³ − 16x = 0» (x ∈ {0; ±4/5}).
BÀI 3 (1,0đ): GIỮ NGUYÊN Bài 3 hiện tại.
BÀI 4 (1,0đ) MỚI D24, CÓ HÌNH: [2526-phanchutrinh] Bài III 1) + 2) (đo chiều cao AB toà nhà, DE // BC, AE = 1,5 m, EC = 21 m, AD = 3,2 m; 1) AB = 48 m; 2) lau kính từ B đến D, 0,16 m/phút ⇒ 280 phút). Mỗi ý 0,5. hinh = "moi".
BÀI 5 (3,0đ) = Bài 4 hình hiện tại, hinh = "giu_hinh_cu". GIỮ giả thiết, ý a) (hình chữ nhật), ý b) (hình thoi). THAY ý c) bằng ý chứng minh một tứ giác là HÌNH BÌNH HÀNH (dạng D15) — CHỈ dùng các điểm đã có trên hình (xem TikZ), đúng với toạ độ, chứng minh từ giả thiết và các ý trước. Ghi vào ghi_chu đây là ý do bạn đặt.
BÀI 6 (0,5đ) MỚI VDC D30 (THAY bài phân thức hiện tại): [2526-tantrieu] Bài 5 «a² + b² + c² = ab + bc + ca và a + b + c = 2025. Tính a, b, c» (a = b = c = 675)."""),
    "ct-1": dict(script="scripts/de_chinh_thuc_ck1_lop8.py", hinh="get_tikz_ct1", ke="""
TRẮC NGHIỆM: GIỮ câu 1, 2, 3, 5, 7. THAY:
 - Câu 4 ⇒ D22: [2324-thuongtin] Câu I.11 «D, E trung điểm AB, BC, AC = 7 cm; DE = ?» (đáp án D). Bỏ "như hình vẽ" nếu lời đủ dữ kiện.
 - Câu 6 ⇒ D23: [2324-thanhtri] Câu I.7 «AD phân giác góc BAC, AB = 6, AC = 8, CD = 3; BD = ?» (đáp án D).
 - Câu 8 ⇒ D26: [2324-giangvo] Câu I.7 «dữ liệu nào là số liệu liên tục» (đáp án D).
BÀI 1 (1,5đ, 3 ý × 0,5): a) MỚI D03 [2324-thanhoai] Bài 1.1 b) «3x(5x² − 2x − 1) − 15x³» (= −6x² − 3x); b) = ý a hiện tại (D06); c) = ý b hiện tại (D08).
BÀI 2 (1,0đ) MỚI (thay phân thức) «Tìm x, biết:» a) D09 [2526-nguyentruongto] Bài 2 a) «x(x² + 2) − x³ = 8» (x = 4); b) D10 [2526-dongmy] II.2a «18x² − 6x = 0» (x = 0; x = 1/3).
BÀI 3 (1,0đ) MỚI (thay phân thức thực tế) thống kê D27 + D28: [2324-nghiatan] Bài 3 a) + b) (bảng hỏi môn thể thao yêu thích). Mỗi ý 0,5.
BÀI 4 (1,0đ) MỚI D24, CÓ HÌNH: [2324-tamhiep] Bài II.12 (tấm phủ hồ bơi, EF = 4,5 m … AB = 9 m). hinh = "moi". Hai mốc 0,25 + 0,25 + 0,5 hoặc theo HDC gốc.
BÀI 5 (3,0đ) = Bài 4 hình hiện tại, GIỮ NGUYÊN, hinh = "giu_hinh_cu".
BÀI 6 (0,5đ) = Bài 5 hiện tại, GIỮ NGUYÊN."""),
    "ct-2": dict(script="scripts/de_chinh_thuc_ck1_lop8.py", hinh="get_tikz_ct2", ke="""
TRẮC NGHIỆM: GIỮ câu 1, 2, 3, 5, 7. THAY:
 - Câu 4 ⇒ D21: [2425-phanchutrinh] Câu I.6 «DE // BC, AD = 2, BD = 4, AE = 3; EC = ?» (đáp án B: 6 cm). Bỏ "Cho hình bên" nếu lời đủ dữ kiện.
 - Câu 6 ⇒ D26: [2425-giangvo2] Câu I.8 «dữ liệu nào là số liệu liên tục» (đáp án B).
 - Câu 8 ⇒ D23: [2526-hatmon] Câu I.12 «AD phân giác, AB = 10, AC = 19, BD = 5; CD = ?» (đáp án C).
BÀI 1 (1,5đ, 3 ý × 0,5): a) MỚI D03 [2324-tamhiep] II.9 b) «3x(x − 2) − 5x(1 − x) − 8(x² − 3)» (= −11x + 24); b) = ý a hiện tại (D06); c) MỚI D08 [2425-nguyencongtru] II.1 c) «2x² + 6x − xy − 3y» (= (x + 3)(2x − y)).
BÀI 2 (1,0đ) «Tìm x, biết:» a) MỚI D09 [2526-phanchutrinh] 2.3a «6x² − (2x + 1)(3x − 2) = 1» (x = −1); b) = ý b Bài 1 hiện tại (D10), barem 0,5.
BÀI 3 (1,0đ) = Bài 3 hiện tại (thống kê), GIỮ NGUYÊN.
BÀI 4 (1,0đ) MỚI D24, CÓ HÌNH: [2425-nguyencongtru] II.4.1 (đo khoảng cách A, B bị vật cản, M, N trung điểm … AB = 90 m). hinh = "moi".
BÀI 5 = Bài 4 hình hiện tại, GIỮ NGUYÊN, hinh = "giu_hinh_cu". BÀI 6 = Bài 5 hiện tại, GIỮ NGUYÊN."""),
    "ct-3": dict(script="scripts/de_chinh_thuc_ck1_lop8.py", hinh="get_tikz_ct3", ke="""
TRẮC NGHIỆM: GIỮ câu 1, 2, 3, 5, 6, 7. THAY:
 - Câu 4 ⇒ D21: [2324-thuongtin] Câu I.8 «DE // BC, AD = 5, DB = 2, AE = 6, EC = x» (đáp án B: 12/5).
 - Câu 8 ⇒ D22: [2324-unghoa] Câu I.10 «D, E trung điểm AB, AC; DE = 5, BC = 2x − 1; x = ?» (đáp án A: 5,5).
BÀI 1 (1,5đ, 3 ý × 0,5): a) MỚI D03 [2324-nghiatan] Bài 1 a) «2xy(3x − 2) − 6x²y + 5xy» (= xy); b) = ý a hiện tại (D06); c) = ý b hiện tại (D08).
BÀI 2 (1,0đ) MỚI «Tìm x, biết:» a) D09 [2324-tayho] II.3 b) «(3x − 1)(2x + 1) − (x + 1)² = 5x²» (x = −2); b) D10 [2324-tayho] II.3 a) «2x(x − 3) − x + 3 = 0» (x = 3; x = 1/2). Đặt b) trước a) theo thứ tự đề: a) D09, b) D10.
BÀI 3 (1,0đ) = Bài 3 hiện tại, GIỮ NGUYÊN.
BÀI 4 (1,0đ) MỚI D24, CÓ HÌNH: [2526-thanglong] Bài 5.1 (chiều rộng khúc sông, BB' = 30 m, CC' = 40 m … x = 67,5 m). hinh = "moi".
BÀI 5 = Bài 4 hình hiện tại, GIỮ NGUYÊN, hinh = "giu_hinh_cu". BÀI 6 = Bài 5 hiện tại, GIỮ NGUYÊN."""),
}

LUAT = r"""## Luật (giáo viên đã chốt — vi phạm bị trả lại)
- PHẠM VI: chỉ kiến thức KNTT Toán 8 tập 1 (đa thức, hằng đẳng thức, tứ giác, Thalès + đường trung bình + phân giác, dữ liệu–biểu đồ). CẤM phân thức, phương trình bậc nhất (tên gọi), tam giác đồng dạng, Pythagore. Tìm x: biến đổi rồi tìm x như lớp 7 ("$2x = 6$ nên $x = 3$"), tích bằng 0: "$A \cdot B = 0$ nên $A = 0$ hoặc $B = 0$".
- "GIỮ" / "GIỮ NGUYÊN" = chép Y HỆT chuỗi hiện tại (chỉ đổi nhãn, số câu, điểm ghi đầu ý, và chia lại mốc barem nếu điểm ý đổi). TN giữ ⇒ giu = true, chép nguyên mọi trường.
- Câu MỚI: chép NGUYÊN VĂN từ ẢNH đề gốc (thư mục làm việc có ảnh <tên-pdf>-trang-N.png + .txt của từng đề nguồn). Tóm tắt ở kế hoạch chỉ để tìm câu. Ảnh lệch tóm tắt ⇒ theo ảnh, ghi ghi_chu. Câu TN mới: options là 4 chuỗi KHÔNG có "A." ở đầu; "dap" là chữ cái; "giai" một–hai câu giải thích có tính toán.
- "nguon": đúng dạng tên trường như các dòng hiện tại, ví dụ "THCS Phan Chu Trinh", "THCS Tân Triều", "Phòng GD\\&ĐT Thanh Trì", "THCS \\& THPT Lương Thế Vinh", "Quận Tây Hồ". Ứng Hoà/Thường Tín/Thanh Oai/Thanh Trì (2324, 2425 mã thanhtri) là đề PHÒNG: "Phòng GD\\&ĐT Ứng Hòa" …
- Đề (statement): mở đầu "\\textbf{(1,5 điểm)}" rồi " [[br]] a) \\textbf{(0,5 điểm)} …"; nối dòng bằng " [[br]] ". Bài 2 mở đầu "\\textbf{(1,0 điểm)} Tìm $x$, biết: [[br]] a) …".
- Lời giải (dap_an): mỗi phần tử là MỘT ý, dạng "\\textbf{a) (0,5đ)} [[br]] dòng [[br]] dòng \\hfill \\textit{(0,25đ)} [[br]] …" — y như chuỗi hiện tại. Mốc " \\hfill \\textit{(0,25đ)}" cuối dòng; TỔNG mốc trong ý = đúng điểm ý. Bài một ý (Bài 6) nhãn rỗng: bắt đầu thẳng vào dòng đầu.
- Mỗi phép biến đổi một dòng, KHÔNG dùng $\Leftrightarrow$, không nêu kết luận trước khi chứng minh, "Vậy …" đúng một lần cuối ý. Không văn nói, không xưng hô, không viết tắt (trừ ĐKXĐ). Toán trong $…$, số thập phân $4{,}5$, phân số \dfrac, giữ escape \% \& \#.
- Bài hình (Bài 4, Bài 5): mỗi suy luận có căn cứ trong ngoặc (định lí Thalès, tính chất đường trung bình, dấu hiệu nhận biết …).
- "mt": mỗi ý một dòng {ma, nd, chu_de, muc, diem, phut, nguon, dang}. ma: "Bài 1.a", "Bài 2.b", "Bài 4.a" (bài một ý: "Bài 6"). chu_de ∈ "ĐS I", "ĐS II", "HH III", "HH IV", "TK V". muc ∈ NB/TH/VD/VDC. dang = mã khung (D01…D30). phut (phút HS trung bình làm): ý 0,5 đại số 3–5; tìm x 4–5; thống kê 0,5 khoảng 4; Thalès thực tế 1,0 khoảng 8–10; ý hình 1,0 khoảng 8–10; VDC 6. MỤC TIÊU tổng phút cả đề (TN tính 2′/câu) trong khoảng 80–90.
- "label": "Bài 1." … "Bài 6."; level: 2 (Bài 6 level 3).
- HÌNH Bài 4 (hinh = "moi"): "tikz" là \begin{tikzpicture}[scale=…]…\end{tikzpicture} THUẦN TikZ (không pgfplots, không thư viện lạ ngoài calc, angles, quotes), mô phỏng hình đề gốc: điểm có nhãn, đoạn song song/thẳng hàng đúng như giả thiết, toạ độ khớp số đo (tỉ lệ đúng Thalès), ghi số đo đã cho lên cạnh nếu đề gốc ghi. Rộng ≤ 6 cm. Đề nói "như hình bên/hình vẽ" thì giữ.
- Bài 5 hình cũ: hinh = "giu_hinh_cu", không trả tikz.
- "gioi_thieu": viết lại theo cấu trúc mới (một dòng "\\textbf{ĐỀ … -- CUỐI HỌC KÌ I TOÁN 8 (KNTT)} (90 phút -- 8 câu trắc nghiệm, 6 bài tự luận)." + " [[br]] \\textbf{Cấu trúc:} Phần I … · Bài 1 … · … · Bài 6 …"), KHÔNG còn chữ phân thức.
- "cach_dung": một–hai câu như hiện tại, bỏ mọi nhắc phân thức/ĐKXĐ.
- "bay": 5 dòng bẫy {vi_tri, noi_dung, loi, cach} khớp đề mới (vi_tri như "Câu 4", "Bài 2.b", "Bài 5.b"); dòng cũ của ý còn giữ thì chép lại, đổi vi_tri.
- TỰ TÍNH LẠI mọi đáp số (cả câu giữ). Lệch đáp số kế hoạch/đề gốc ⇒ ghi ghi_chu, không tự đổi đề.
- "ghi_chu": liệt kê ý bạn đặt (không chép đề), chỗ đề gốc lệch, nghi ngờ. Chuỗi JSON: gạch chéo ngược nhân đôi.
"""


def doan_de(script: str, k: str) -> str:
    src = (REPO / script).read_text()
    s = src.index(f'DE["{k}"] = dict(')
    m = re.search(r'\n(DE\["|# =+\n# ĐỀ|KIND = |def )', src[s + 10:])
    return src[s: s + 10 + m.start()] if m else src[s:]


def main():
    for k, kh in KE_HOACH.items():
        mas = sorted(set(re.findall(r"\[(\d{4}-[a-z0-9]+)\]", kh["ke"])))
        thieu = [m for m in mas if f"l8-ck1-{m}" not in PDF]
        assert not thieu, (k, thieu)
        files = [str(PDF[f"l8-ck1-{m}"].relative_to(REPO)) for m in mas]
        ds_nguon = "\n".join(f"- [{m}] ⇒ file {PDF[f'l8-ck1-{m}'].name}" for m in mas)
        tikz = getattr(H, kh["hinh"])()
        loai = "ĐỀ ÔN TẬP" if k.startswith("on") else "ĐỀ KIỂM TRA CHÍNH THỨC"
        prompt = f"""Bạn là thợ sửa {loai} CUỐI KÌ 1 Toán 8 (Hà Nội, sách Kết nối tri thức) — mã {k}. Làm CẨN THẬN, ĐỦ, KHÔNG BỊA. KHÔNG chạy lệnh shell (bị cấm): dữ liệu nằm trong prompt và ảnh/text đề gốc trong thư mục làm việc.

## Vì sao sửa
Đề hiện tại có 2,25–3,25 điểm PHÂN THỨC — học sinh chưa học trước kì thi (25/26 đề trường Hà Nội không có). Giáo viên chốt khung mới theo 26 đề thật:
TN 8 câu × 0,25 = 2,0 · Bài 1 (1,5) 3 ý × 0,5: nhân/chia đa thức, rút gọn có hằng đẳng thức, phân tích thành nhân tử · Bài 2 (1,0) tìm x 2 ý · Bài 3 (1,0) thống kê · Bài 4 (1,0) Thalès/đường trung bình thực tế có hình · Bài 5 (3,0) hình tứ giác · Bài 6 (0,5) VDC. Tổng 10.

## Kế hoạch (bất di bất dịch — mã [nnnn-truong] là đề gốc)
{kh["ke"]}

## File đề gốc
{ds_nguon}

{LUAT}
## ĐỀ HIỆN TẠI (mã Python; tn(cau, de, options, dap, giai, nd, ch, muc, nguon); mt = (ma, nd, chu_de, muc, diem, phut, nguon); y(nhan, diem, [dòng hoặc (dòng, mốc)]) sinh chuỗi lời giải — khi chép ý GIỮ, hãy viết ra chuỗi lời giải đã sinh theo dạng "\\textbf{{a) (0,5đ)}} [[br]] dòng [[br]] dòng \\hfill \\textit{{(0,25đ)}}")
```python
{doan_de(kh["script"], k)}
```

## TikZ hình bài hình hiện tại (để biết các điểm có trên hình)
```latex
{tikz}
```

## Đầu ra
MỘT đối tượng JSON đúng schema: gioi_thieu, cach_dung, bay[5], tn[8] (đủ 8, theo thứ tự câu), bai[6] (Bài 1 … Bài 6), ghi_chu.
"""
        viec = {
            "id": f"de8-ck1-{k}",
            "model": "gemini-3.8-flash-high",
            "prompt": prompt,
            "files": files,
            "render": True,
            "schema": "scripts/gemini/schema/de-ck1-lop8.json",
            "timeout": "1800s",
            "meta": {"loai": "de-ck1-lop8-bo-phan-thuc", "de": k, "nguon": mas},
        }
        p = REPO / "storage/gemini/hang-doi" / f"{viec['id']}.json"
        p.write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        print("ghi", p.relative_to(REPO), "| nguồn", len(mas), "| prompt", len(prompt), "kí tự")


if __name__ == "__main__":
    main()
