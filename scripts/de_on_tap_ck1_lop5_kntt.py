#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BỘ ĐỀ ÔN TẬP CUỐI KÌ 1 (CK1) TOÁN 5 KẾT NỐI TRI THỨC (KNTT) - NĂM HỌC 2024-2025 & 2025-2026.
Sinh 3 đề ôn tập (Số 1, Số 2, Số 3) + 3 file Ma trận đề và đáp án chi tiết cho GV
vào inputs/seeds/lop-5/de-cuoi-ki-1/ (theme de_thi, trinh_bay "thoang").

Cấu trúc chuẩn Tiểu học (Thông tư 27, 40 phút, thang 10 điểm):
- PHẦN I. TRẮC NGHIỆM (4,0 điểm): 8 câu x 0,5đ (M1: 3 câu, M2: 4 câu, M3: 1 câu).
- PHẦN II. TỰ LUẬN (6,0 điểm):
  + Bài 1 (1,0đ): Đặt tính rồi tính (4 phép tính số thập phân).
  + Bài 2 (1,0đ): Tính giá trị biểu thức / tính với phân số hoặc số thập phân.
  + Bài 3 (1,0đ): Viết số thích hợp vào chỗ chấm (đổi đơn vị đo độ dài, khối lượng, diện tích).
  + Bài 4 (2,0đ): Bài toán có lời văn thực tế (hình tam giác / hình thang / hình tròn kết hợp diện tích, sản lượng).
  + Bài 5 (1,0đ): Tính bằng cách thuận tiện nhất hoặc câu tư duy nâng cao (M3).
Tỉ lệ mức độ Thông tư 27: M1 (3,5đ - 35%) · M2 (4,0đ - 40%) · M3 (2,5đ - 25%).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "inputs/seeds/lop-5/de-cuoi-ki-1"
OUT.mkdir(parents=True, exist_ok=True)

BR = " [[br]] "

def d(x):
    s = f"{x:g}".replace(".", ",")
    return s if "," in s else s + ",0"

# ─────────────────────────── DỮ LIỆU 3 ĐỀ ÔN TẬP ───────────────────────────
DE = {
    "de1": {
        "slug_de": "de-on-tap-cuoi-ki-1-so-1",
        "slug_mt": "ma-tran-va-dap-an-on-tap-so-1",
        "so": "1",
        "ten": "Đề ôn tập số 1",
        "eyebrow": "LỚP 5 • ĐỀ ÔN TẬP SỐ 1",
        "header_eyebrow": "ĐỀ ÔN TẬP CUỐI HỌC KÌ I · NĂM HỌC 2026 – 2027",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 4", "phut": 1.5,
                "dang": "Phân số thập phân",
                "statement": "Phân số $\\dfrac{7}{25}$ viết thành phân số thập phân có mẫu số $100$ là:",
                "options": ["$\\dfrac{7}{100}$", "$\\dfrac{14}{50}$", "$\\dfrac{28}{100}$", "$\\dfrac{35}{100}$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Ta có $\\dfrac{7}{25} = \\dfrac{7 \\times 4}{25 \\times 4} = \\dfrac{28}{100}$. Phương án B bằng $\\dfrac{7}{25}$ nhưng mẫu số $50$ không phải phân số thập phân.",
                "trap": "Học sinh dễ nhầm phân số có mẫu số 50 hoặc nhân sai tử số."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Cấu tạo số thập phân",
                "statement": "Số thập phân gồm $8$ đơn vị, $5$ phần mười và $6$ phần nghìn được viết là:",
                "options": ["$8,56$", "$8,506$", "$8,056$", "$85,06$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Phần nguyên là $8$; hàng phần mười là $5$, hàng phần trăm là $0$, hàng phần nghìn là $6$: viết là $8,506$.",
                "trap": "Học sinh hay quên chữ số 0 ở hàng phần trăm, viết nhầm thành 8,56."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 26", "phut": 1.5,
                "dang": "Hình thang: nhận biết",
                "statement": "Trong các khẳng định dưới đây, khẳng định nào đúng về hình thang?",
                "options": [
                    "Hình thang có hai cặp cạnh đối diện song song.",
                    "Hình thang có một cặp cạnh đối diện song song.",
                    "Hình thang có bốn góc vuông.",
                    "Hình thang có bốn cạnh bằng nhau."
                ],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Hình thang là hình tứ giác có một cặp cạnh đối diện song song (gọi là hai đáy).",
                "trap": "Học sinh dễ nhầm với hình bình hành (hai cặp cạnh đối song song)."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "So sánh các số thập phân",
                "statement": "Số lớn nhất trong các số thập phân $6,85$; $6,805$; $6,851$; $6,589$ là:",
                "options": ["$6,85$", "$6,805$", "$6,851$", "$6,589$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. So sánh phần nguyên đều bằng $6$. So hàng phần mười: $8 > 5$. So hàng phần trăm: $5 > 0$ nên xét $6,850$ và $6,851$. Vì $1 > 0$ nên $6,851$ lớn nhất.",
                "trap": "Học sinh đếm số chữ số rồi cho rằng số có ít chữ số hơn thì bé hơn."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn số thập phân",
                "statement": "Làm tròn số thập phân $24,675$ đến hàng phần mười ta được số:",
                "options": ["$24,6$", "$24,7$", "$25$", "$24,68$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần trăm là $7 \\ge 5$ nên ta cộng thêm $1$ vào chữ số hàng phần mười: $6 + 1 = 7$, được $24,7$.",
                "trap": "Học sinh làm tròn cắt cụt thành 24,6 (quên xét hàng phần trăm) hoặc làm tròn đến hàng đơn vị thành 25."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 15", "phut": 2.0,
                "dang": "Đổi đơn vị đo diện tích ha, m²",
                "statement": "Số thập phân thích hợp viết vào chỗ chấm để $4\\text{ ha } 250\\text{ m}^2 = \\dots\\dots\\text{ ha}$ là:",
                "options": ["$4,25$", "$4,025$", "$4,250$", "$4,0025$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Vì $1\\text{ ha} = 10\\,000\\text{ m}^2$ nên $250\\text{ m}^2 = \\dfrac{250}{10000}\\text{ ha} = 0,025\\text{ ha}$. Vậy $4\\text{ ha } 250\\text{ m}^2 = 4,025\\text{ ha}$.",
                "trap": "Học sinh chia cho 100 thành 4,25 ha (nhầm 1 ha = 100 m²)."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 23", "phut": 2.0,
                "dang": "Nhân nhẩm số thập phân với 0,1",
                "statement": "Kết quả của phép tính nhẩm $34,8 \\times 0,1$ là:",
                "options": ["$348$", "$3,48$", "$0,348$", "$34,80$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Khi nhân một số thập phân với $0,1$, ta chỉ việc chuyển dấu phẩy của số đó sang bên trái một chữ số: $34,8 \\times 0,1 = 3,48$.",
                "trap": "Học sinh nhầm với nhân 10 chuyển sang phải thành 348."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 20", "phut": 3.0,
                "dang": "Thay đổi thành phần phép trừ",
                "statement": "Hiệu của hai số là $6,8$. Nếu giữ nguyên số bị trừ và thêm vào số trừ $1,5$ thì hiệu mới là:",
                "options": ["$8,3$", "$5,3$", "$6,8$", "$4,3$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Khi giữ nguyên số bị trừ và tăng số trừ thêm $1,5$ đơn vị thì hiệu giảm đi $1,5$ đơn vị: $6,8 - 1,5 = 5,3$.",
                "trap": "Học sinh cộng thêm 1,5 thành 8,3 do nhầm quy tắc số trừ."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $45,76 + 28,5$ [[br]] b) $83,4 - 36,75$ [[br]] c) $14,8 \\times 3,6$ [[br]] d) $75,52 : 3,2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $45,76 + 28,5 = 74,26$ (đặt tính thẳng cột dấu phẩy).",
                    "\\textbf{b) (0,25đ)} $83,40 - 36,75 = 46,65$ (viết thêm chữ số 0 ở hàng phần trăm rồi trừ).",
                    "\\textbf{c) (0,25đ)} $14,8 \\times 3,6 = 53,28$ (tách đúng 2 chữ số ở phần thập phân).",
                    "\\textbf{d) (0,25đ)} $75,52 : 3,2 = 755,2 : 32 = 23,6$ (chuyển dấu phẩy ở cả số chia và số bị chia)."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ. Đặt tính thẳng hàng cột, phép chia gạch dấu phẩy đúng quy tắc."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{2}{3} + \\dfrac{3}{5}$ [[br]] b) $2\\dfrac{1}{4} \\times \\dfrac{8}{9}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số: $\\dfrac{2}{3} + \\dfrac{3}{5} = \\dfrac{10}{15} + \\dfrac{9}{15} = \\dfrac{19}{15}$.",
                    "\\textbf{b) (0,5đ)} Đổi hỗn số ra phân số rồi nhân: $2\\dfrac{1}{4} \\times \\dfrac{8}{9} = \\dfrac{9}{4} \\times \\dfrac{8}{9} = \\dfrac{72}{36} = 2$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ. Kết quả phân số phải rút gọn về tối giản nếu rút gọn được."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $7\\text{ m } 8\\text{ cm} = \\dots\\dots\\dots\\dots\\text{ m}$ [[br]] b) $3\\text{ tấn } 45\\text{ kg} = \\dots\\dots\\dots\\dots\\text{ tấn}$ [[br]] c) $5\\text{ ha } 250\\text{ m}^2 = \\dots\\dots\\dots\\dots\\text{ ha}$ [[br]] d) $4\\text{ km}^2\\ 35\\text{ ha} = \\dots\\dots\\dots\\dots\\text{ km}^2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $7\\text{ m } 8\\text{ cm} = 7,08\\text{ m}$.",
                    "\\textbf{b) (0,25đ)} $3\\text{ tấn } 45\\text{ kg} = 3,045\\text{ tấn}$.",
                    "\\textbf{c) (0,25đ)} $5\\text{ ha } 250\\text{ m}^2 = 5,025\\text{ ha}$.",
                    "\\textbf{d) (0,25đ)} $4\\text{ km}^2\\ 35\\text{ ha} = 4,35\\text{ km}^2$."
                ],
                "note": "Mỗi ý điền đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 26, Bài 9", "phut": 8.0,
                "dang": "Bài toán thực tế hình thang và sản lượng lúa",
                "statement": "\\textbf{(2,0 điểm)} Một thửa ruộng hình thang có đáy lớn $40\\text{ m}$, đáy bé bằng $\\dfrac{3}{4}$ đáy lớn. Chiều cao bằng trung bình cộng của hai đáy. [[br]] a) Tính diện tích thửa ruộng hình thang đó. [[br]] b) Người ta cấy lúa trên thửa ruộng, trung bình cứ $100\\text{ m}^2$ thu hoạch được $65\\text{ kg}$ thóc. Hỏi cả thửa ruộng thu hoạch được bao nhiêu tạ thóc?",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Độ dài đáy bé thửa ruộng là: $40 \\times \\dfrac{3}{4} = 30\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Chiều cao của thửa ruộng là: $(40 + 30) : 2 = 35\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Diện tích thửa ruộng hình thang là: $(40 + 30) \\times 35 : 2 = 1225\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Cả thửa ruộng thu hoạch được số ki-lô-gam thóc là: [[br]] $1225 : 100 \\times 65 = 796,25\\text{ (kg)}$ \\hfill \\textit{(0,50đ)} [[br]] Đổi: $796,25\\text{ kg} = 7,9625\\text{ tạ}$ \\hfill \\textit{(0,25đ)} [[br]] Đáp số: a) $1225\\text{ m}^2$; b) $7,9625\\text{ tạ thóc}$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Đầy đủ lời giải, phép tính, tên đơn vị và đáp số. Đổi đơn vị đúng ở câu b được 0,25đ."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Bài 23", "phut": 4.0,
                "dang": "Tính bằng cách thuận tiện nhất",
                "statement": "\\textbf{(1,0 điểm)} Tính bằng cách thuận tiện nhất: [[br]] $2,65 \\times 63,4 + 2,65 \\times 37,6 - 2,65$",
                "dap_an": [
                    "Ta có: [[br]] $2,65 \\times 63,4 + 2,65 \\times 37,6 - 2,65$ [[br]] $= 2,65 \\times 63,4 + 2,65 \\times 37,6 - 2,65 \\times 1$ \\hfill \\textit{(0,25đ)} [[br]] $= 2,65 \\times (63,4 + 37,6 - 1)$ \\hfill \\textit{(0,25đ)} [[br]] $= 2,65 \\times 100$ \\hfill \\textit{(0,25đ)} [[br]] $= 265$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Học sinh nhận biết $2,65 = 2,65 \\times 1$ và đưa thừa số chung ra ngoài được 0,5đ; tính đúng kết quả cho 0,5đ còn lại. Tính lần lượt từ trái sang phải cho tối đa 0,5đ."
            }
        ]
    },

    "de2": {
        "slug_de": "de-on-tap-cuoi-ki-1-so-2",
        "slug_mt": "ma-tran-va-dap-an-on-tap-so-2",
        "so": "2",
        "ten": "Đề ôn tập số 2",
        "eyebrow": "LỚP 5 • ĐỀ ÔN TẬP SỐ 2",
        "header_eyebrow": "ĐỀ ÔN TẬP CUỐI HỌC KÌ I · NĂM HỌC 2026 – 2027",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Đọc số thập phân",
                "statement": "Số thập phân $40,075$ đọc là:",
                "options": [
                    "Bốn mươi phẩy bảy mươi lăm",
                    "Bốn mươi phẩy không trăm bảy mươi lăm",
                    "Bốn phẩy không bảy mươi lăm",
                    "Bốn mươi phẩy bảy trăm năm mươi"
                ],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Số $40,075$ đọc phần nguyên là “bốn mươi”, dấu phẩy đọc là “phẩy”, phần thập phân gồm 3 chữ số đọc là “không trăm bảy mươi lăm”.",
                "trap": "Học sinh hay bỏ qua chữ số 0 đọc nhầm thành bốn mươi phẩy bảy mươi lăm."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Hàng của số thập phân",
                "statement": "Trong số thập phân $507,239$, chữ số $3$ thuộc hàng nào?",
                "options": ["Hàng phần mười", "Hàng chục", "Hàng phần nghìn", "Hàng phần trăm"],
                "answer": "D",
                "solution": "Chọn \\textbf{D}. Chữ số $2$ thuộc hàng phần mười, chữ số $3$ thuộc hàng phần trăm, chữ số $9$ thuộc hàng phần nghìn.",
                "trap": "Học sinh nhầm thứ tự hàng từ trái sang phải sau dấu phẩy."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 27", "phut": 1.5,
                "dang": "Chu vi hình tròn",
                "statement": "Một hình tròn có bán kính $r = 5\\text{ cm}$. Chu vi của hình tròn đó là:",
                "options": ["$15,7\\text{ cm}$", "$31,4\\text{ cm}$", "$78,5\\text{ cm}$", "$62,8\\text{ cm}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chu vi hình tròn là $C = r \\times 2 \\times 3,14 = 5 \\times 2 \\times 3,14 = 31,4\\text{ cm}$. Phương án C là diện tích.",
                "trap": "Học sinh nhầm công thức chu vi với diện tích (nhân bán kính với bán kính)."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "Sắp xếp số thập phân",
                "statement": "Dãy số thập phân nào dưới đây được sắp xếp theo thứ tự từ bé đến lớn?",
                "options": [
                    "$4,5;\\; 4,15;\\; 4,05;\\; 4,51$",
                    "$4,05;\\; 4,5;\\; 4,15;\\; 4,51$",
                    "$4,05;\\; 4,15;\\; 4,5;\\; 4,51$",
                    "$4,51;\\; 4,5;\\; 4,15;\\; 4,05$"
                ],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Ta viết dưới dạng cùng có 2 chữ số thập phân: $4,05 < 4,15 < 4,50 < 4,51$.",
                "trap": "Học sinh so sánh 4,5 bé hơn 4,15 vì số 5 có 1 chữ số còn 15 có 2 chữ số."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn đến hàng đơn vị",
                "statement": "Làm tròn số $38,472$ đến hàng đơn vị (số tự nhiên gần nhất) thì được số:",
                "options": ["$39$", "$38$", "$38,5$", "$38,4$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần mười là $4 < 5$ nên ta làm tròn xuống, giữ nguyên chữ số hàng đơn vị: $38$.",
                "trap": "Học sinh làm tròn 2 lần (38,47 thành 38,5 rồi thành 39)."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 15", "phut": 2.0,
                "dang": "Đổi ha sang m²",
                "statement": "$2\\text{ ha } 500\\text{ m}^2 = \\dots\\dots\\text{ m}^2$. Số thích hợp viết vào chỗ chấm là:",
                "options": ["$2500$", "$25\\,000$", "$2050$", "$20\\,500$"],
                "answer": "D",
                "solution": "Chọn \\textbf{D}. Vì $1\\text{ ha} = 10\\,000\\text{ m}^2$ nên $2\\text{ ha} = 20\\,000\\text{ m}^2$. Do đó $20\\,000 + 500 = 20\\,500\\text{ m}^2$.",
                "trap": "Học sinh nhân 1 ha = 1000 m² ra 2500 m²."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 20", "phut": 2.0,
                "dang": "Trừ số tự nhiên cho số thập phân",
                "statement": "Kết quả của phép tính $50 - 23,47$ là:",
                "options": ["$26,53$", "$27,53$", "$26,63$", "$73,47$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Đặt tính: $50,00 - 23,47 = 26,53$.",
                "trap": "Học sinh quên hạ nhớ ở phần nguyên, dẫn tới kết quả 27,53."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 21", "phut": 3.0,
                "dang": "Tính chất vị trí dấu phẩy trong phép nhân",
                "statement": "Biết $125 \\times 8 = 1000$. Không đặt tính, kết quả của phép tính $1,25 \\times 0,8$ là:",
                "options": ["$10$", "$0,1$", "$1$", "$100$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Hai thừa số có tất cả $2 + 1 = 3$ chữ số ở phần thập phân. Ta đếm từ phải sang trái 3 chữ số của $1000$ được $1,000 = 1$.",
                "trap": "Học sinh đếm nhầm số chữ số 0, chọn 0,1 hoặc 10."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $136,4 + 58,75$ [[br]] b) $92,3 - 47,68$ [[br]] c) $25,4 \\times 4,5$ [[br]] d) $108,1 : 4,7$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $136,40 + 58,75 = 195,15$.",
                    "\\textbf{b) (0,25đ)} $92,30 - 47,68 = 44,62$.",
                    "\\textbf{c) (0,25đ)} $25,4 \\times 4,5 = 114,30 = 114,3$.",
                    "\\textbf{d) (0,25đ)} $108,1 : 4,7 = 1081 : 47 = 23$."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{5}{6} - \\dfrac{3}{8}$ [[br]] b) $1\\dfrac{2}{5} : \\dfrac{7}{10}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số chung là 24: $\\dfrac{5}{6} - \\dfrac{3}{8} = \\dfrac{20}{24} - \\dfrac{9}{24} = \\dfrac{11}{24}$.",
                    "\\textbf{b) (0,5đ)} $1\\dfrac{2}{5} : \\dfrac{7}{10} = \\dfrac{7}{5} \\times \\dfrac{10}{7} = 2$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $15\\text{ km } 42\\text{ m} = \\dots\\dots\\dots\\dots\\text{ km}$ [[br]] b) $4\\text{ tạ } 8\\text{ kg} = \\dots\\dots\\dots\\dots\\text{ tạ}$ [[br]] c) $12\\text{ m}^2\\ 45\\text{ dm}^2 = \\dots\\dots\\dots\\dots\\text{ m}^2$ [[br]] d) $8\\text{ ha} = \\dots\\dots\\dots\\dots\\text{ m}^2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $15\\text{ km } 42\\text{ m} = 15,042\\text{ km}$.",
                    "\\textbf{b) (0,25đ)} $4\\text{ tạ } 8\\text{ kg} = 4,08\\text{ tạ}$.",
                    "\\textbf{c) (0,25đ)} $12\\text{ m}^2\\ 45\\text{ dm}^2 = 12,45\\text{ m}^2$.",
                    "\\textbf{d) (0,25đ)} $8\\text{ ha} = 80\\,000\\text{ m}^2$."
                ],
                "note": "Mỗi ý đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 25, Bài 9", "phut": 8.0,
                "dang": "Bài toán thực tế tam giác và phân số",
                "statement": "\\textbf{(2,0 điểm)} Một mảnh đất hình tam giác có độ dài cạnh đáy là $36\\text{ m}$, chiều cao tương ứng bằng $\\dfrac{3}{4}$ độ dài cạnh đáy. [[br]] a) Tính diện tích mảnh đất hình tam giác đó. [[br]] b) Người ta sử dụng $\\dfrac{2}{3}$ diện tích mảnh đất để trồng hoa cúc, phần còn lại trồng hoa hồng. Tính diện tích phần đất trồng hoa hồng.",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Chiều cao mảnh đất hình tam giác là: $36 \\times \\dfrac{3}{4} = 27\\text{ (m)}$ \\hfill \\textit{(0,50đ)} [[br]] Diện tích mảnh đất hình tam giác là: $36 \\times 27 : 2 = 486\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Diện tích phần đất trồng hoa cúc là: $486 \\times \\dfrac{2}{3} = 324\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)} [[br]] Diện tích phần đất trồng hoa hồng là: $486 - 324 = 162\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,25đ)} [[br]] (Hoặc tính: $486 \\times (1 - \\frac{2}{3}) = 162\\text{ m}^2$). [[br]] Đáp số: a) $486\\text{ m}^2$; b) $162\\text{ m}^2$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Làm theo cách nào đúng đều cho điểm tối đa."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Bài 19", "phut": 4.0,
                "dang": "Tính thuận tiện nhóm tròn chục",
                "statement": "\\textbf{(1,0 điểm)} Tính bằng cách thuận tiện nhất: [[br]] $14,25 + 8,6 + 5,75 + 11,4$",
                "dap_an": [
                    "Ta có: [[br]] $14,25 + 8,6 + 5,75 + 11,4$ [[br]] $= (14,25 + 5,75) + (8,6 + 11,4)$ \\hfill \\textit{(0,50đ)} [[br]] $= 20 + 20$ \\hfill \\textit{(0,25đ)} [[br]] $= 40$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Nhóm hợp lý được 0,5đ; tính đúng ra 40 được 0,5đ."
            }
        ]
    },

    "de3": {
        "slug_de": "de-on-tap-cuoi-ki-1-so-3",
        "slug_mt": "ma-tran-va-dap-an-on-tap-so-3",
        "so": "3",
        "ten": "Đề ôn tập số 3",
        "eyebrow": "LỚP 5 • ĐỀ ÔN TẬP SỐ 3",
        "header_eyebrow": "ĐỀ ÔN TẬP CUỐI HỌC KÌ I · NĂM HỌC 2026 – 2027",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 7, 10", "phut": 1.5,
                "dang": "Hỗn số sang số thập phân",
                "statement": "Hỗn số $3\\dfrac{5}{100}$ viết dưới dạng số thập phân là:",
                "options": ["$3,5$", "$3,05$", "$3,005$", "$35,0$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Phần nguyên là $3$, phần phân số $\\dfrac{5}{100} = 0,05$ nên viết là $3,05$.",
                "trap": "Học sinh nhầm với 3,5 do quên mẫu số là 100."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Giá trị chữ số theo hàng",
                "statement": "Chữ số $7$ trong số thập phân $24,715$ có giá trị là:",
                "options": ["$7$", "$\\dfrac{7}{10}$", "$\\dfrac{7}{100}$", "$\\dfrac{7}{1000}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số $7$ đứng ngay sau dấu phẩy nên thuộc hàng phần mười, có giá trị $\\dfrac{7}{10}$ (hoặc $0,7$).",
                "trap": "Học sinh chọn 7 hoặc 7/100."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 25", "phut": 1.5,
                "dang": "Diện tích hình tam giác",
                "statement": "Diện tích hình tam giác có độ dài đáy $12\\text{ cm}$ và chiều cao $7\\text{ cm}$ là:",
                "options": ["$84\\text{ cm}^2$", "$42\\text{ cm}^2$", "$21\\text{ cm}^2$", "$42\\text{ cm}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Diện tích hình tam giác là $S = 12 \\times 7 : 2 = 42\\text{ cm}^2$.",
                "trap": "Học sinh quên chia cho 2 ra 84 cm²."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "Tìm số tự nhiên giữa hai số thập phân",
                "statement": "Số tự nhiên $x$ thích hợp điền vào chỗ chấm để $15,8 < x < 16,9$ là:",
                "options": ["$15$", "$16$", "$17$", "$16,5$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. $x$ là số tự nhiên duy nhất thỏa mãn $15,8 < x < 16,9$ là $x = 16$.",
                "trap": "Học sinh chọn 16,5 (không đọc kĩ yêu cầu x là số tự nhiên)."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn đến hàng phần trăm",
                "statement": "Làm tròn số thập phân $17,845$ đến hàng phần trăm ta được số:",
                "options": ["$17,84$", "$17,85$", "$17,8$", "$18$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần nghìn là $5 \\ge 5$ nên cộng thêm $1$ vào hàng phần trăm: $4 + 1 = 5$, ta được $17,85$.",
                "trap": "Học sinh cắt cụt thành 17,84."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 15", "phut": 2.0,
                "dang": "Đổi đơn vị đo diện tích ha",
                "statement": "Số đo bằng $3,5\\text{ ha}$ là:",
                "options": ["$350\\text{ m}^2$", "$3500\\text{ m}^2$", "$35\\,000\\text{ m}^2$", "$350\\,000\\text{ m}^2$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Ta có $1\\text{ ha} = 10\\,000\\text{ m}^2$ nên $3,5\\text{ ha} = 3,5 \\times 10\\,000 = 35\\,000\\text{ m}^2$.",
                "trap": "Học sinh nhân nhầm với 1000 ra 3500 m²."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 23", "phut": 2.0,
                "dang": "Chia nhẩm số thập phân cho 0,1",
                "statement": "Kết quả của phép tính nhẩm $4,85 : 0,1$ là:",
                "options": ["$0,485$", "$48,5$", "$485$", "$4,85$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Khi chia một số thập phân cho $0,1$, ta chuyển dấu phẩy sang bên phải một chữ số: $4,85 : 0,1 = 48,5$.",
                "trap": "Học sinh nhầm với nhân 0,1 chuyển sang trái thành 0,485."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 22", "phut": 3.0,
                "dang": "Thương và số dư trong phép chia số thập phân",
                "statement": "Một phép chia có thương là $3,45$ và số dư là $0,02$. Nếu số bị chia và số chia cùng gấp lên $10$ lần thì:",
                "options": [
                    "Thương là $34,5$, số dư là $0,2$.",
                    "Thương là $3,45$, số dư là $0,02$.",
                    "Thương là $3,45$, số dư là $0,2$.",
                    "Thương là $34,5$, số dư là $0,02$."
                ],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Khi số bị chia và số chia cùng nhân với $10$ thì thương không thay đổi ($3,45$) nhưng số dư gấp lên $10$ lần ($0,02 \\times 10 = 0,2$).",
                "trap": "Học sinh nghĩ số dư cũng không đổi (chọn B) hoặc thương cũng gấp 10 lần (chọn A)."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $78,35 + 46,9$ [[br]] b) $150,2 - 84,65$ [[br]] c) $32,6 \\times 2,8$ [[br]] d) $98,4 : 2,4$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $78,35 + 46,90 = 125,25$.",
                    "\\textbf{b) (0,25đ)} $150,20 - 84,65 = 65,55$.",
                    "\\textbf{c) (0,25đ)} $32,6 \\times 2,8 = 91,28$.",
                    "\\textbf{d) (0,25đ)} $98,4 : 2,4 = 984 : 24 = 41$."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{3}{4} + \\dfrac{1}{6}$ [[br]] b) $3\\dfrac{1}{3} \\times \\dfrac{3}{5}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số chung là 12: $\\dfrac{3}{4} + \\dfrac{1}{6} = \\dfrac{9}{12} + \\dfrac{2}{12} = \\dfrac{11}{12}$.",
                    "\\textbf{b) (0,5đ)} $3\\dfrac{1}{3} \\times \\dfrac{3}{5} = \\dfrac{10}{3} \\times \\dfrac{3}{5} = \\dfrac{30}{15} = 2$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $8\\text{ m } 5\\text{ dm} = \\dots\\dots\\dots\\dots\\text{ m}$ [[br]] b) $6\\text{ tấn } 8\\text{ yến} = \\dots\\dots\\dots\\dots\\text{ tấn}$ [[br]] c) $25\\text{ ha } 40\\text{ m}^2 = \\dots\\dots\\dots\\dots\\text{ ha}$ [[br]] d) $3\\text{ km}^2\\ 12\\text{ ha} = \\dots\\dots\\dots\\dots\\text{ km}^2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $8\\text{ m } 5\\text{ dm} = 8,5\\text{ m}$.",
                    "\\textbf{b) (0,25đ)} $6\\text{ tấn } 8\\text{ yến} = 6,08\\text{ tấn}$.",
                    "\\textbf{c) (0,25đ)} $25\\text{ ha } 40\\text{ m}^2 = 25,004\\text{ ha}$.",
                    "\\textbf{d) (0,25đ)} $3\\text{ km}^2\\ 12\\text{ ha} = 3,12\\text{ km}^2$."
                ],
                "note": "Mỗi ý đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 26, Bài 9", "phut": 8.0,
                "dang": "Bài toán thực tế hình thang và sản lượng bắp cải",
                "statement": "\\textbf{(2,0 điểm)} Một khu đất hình thang có đáy lớn $45\\text{ m}$, đáy bé bằng $\\dfrac{2}{3}$ đáy lớn. Chiều cao kém đáy bé $6\\text{ m}$. [[br]] a) Tính diện tích khu đất hình thang đó. [[br]] b) Người ta trồng bắp cải trên khu đất, trung bình cứ $100\\text{ m}^2$ thu hoạch được $120\\text{ kg}$ bắp cải. Hỏi cả khu đất thu hoạch được bao nhiêu tạ bắp cải?",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Đáy bé của khu đất là: $45 \\times \\dfrac{2}{3} = 30\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Chiều cao của khu đất là: $30 - 6 = 24\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Diện tích khu đất hình thang là: $(45 + 30) \\times 24 : 2 = 900\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Cả khu đất thu hoạch được số ki-lô-gam bắp cải là: [[br]] $900 : 100 \\times 120 = 1080\\text{ (kg)}$ \\hfill \\textit{(0,50đ)} [[br]] Đổi: $1080\\text{ kg} = 10,8\\text{ tạ}$ \\hfill \\textit{(0,25đ)} [[br]] Đáp số: a) $900\\text{ m}^2$; b) $10,8\\text{ tạ bắp cải}$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Đầy đủ câu lời giải, phép tính, đơn vị và đáp số."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Bài 21, 23", "phut": 4.0,
                "dang": "Tính thuận tiện kết hợp nhiều thừa số",
                "statement": "\\textbf{(1,0 điểm)} Tính bằng cách thuận tiện nhất: [[br]] $12,5 \\times 0,25 \\times 8 \\times 4$",
                "dap_an": [
                    "Ta có: [[br]] $12,5 \\times 0,25 \\times 8 \\times 4$ [[br]] $= (12,5 \\times 8) \\times (0,25 \\times 4)$ \\hfill \\textit{(0,50đ)} [[br]] $= 100 \\times 1$ \\hfill \\textit{(0,25đ)} [[br]] $= 100$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Ghép cặp (12,5 x 8) và (0,25 x 4) được 0,5đ; ra kết quả 100 được 0,5đ."
            }
        ]
    }
}

# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────
def format_bai1_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hfill \\textbf{{b)}} {items.get('b)', '')} \\hfill "
        f"\\textbf{{c)}} {items.get('c)', '')} \\hfill \\textbf{{d)}} {items.get('d)', '')}"
    )


def format_bai2_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hspace{{4cm}} \\textbf{{b)}} {items.get('b)', '')}"
    )


def format_bai3_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hfill \\textbf{{b)}} {items.get('b)', '')}\\\\[3pt]\n[[br]]"
        f"\\textbf{{c)}} {items.get('c)', '')} \\hfill \\textbf{{d)}} {items.get('d)', '')}"
    )


def make_de_json(k, D):
    header_box = (
        "\\begin{tabular}{|p{3.2cm}|p{12.4cm}|}\n"
        "\\hline\n"
        "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
        "\\vspace{0.35cm} & \\vspace{0.35cm} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\par\\vspace{2pt}"
    )
    tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}"

    # ── Trang 1: Khung Điểm/Nhận xét + Toàn bộ 8 câu TN ──
    p1_blocks = [
        {"type": "para", "text": header_box},
        {"type": "para", "text": tn_intro}
    ]
    for c in D["tn"]:
        p1_blocks.append({
            "type": "problem",
            "label": f"Câu {c['cau']}.",
            "level": c["level"],
            "statement": c["statement"],
            "options": c["options"],
            "answer": c["answer"],
            "solution": c["solution"],
            "tier": "onclass"
        })

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": "",
        "blocks": p1_blocks,
        "teacher_note": f"{D['ten']} ({D.get('truong', 'KNTT')}) - Trang 1 (Phần I): 8 câu trắc nghiệm (4,0 điểm)."
    }

    # ── Trang 1 (tiếp): Phần II Tự luận + Bài 1 (Đặt tính) kèm ô ly cao 7cm ──
    tl_intro = "\\par\\vspace{2pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
    b1 = D["bai"][0]
    p2_blocks = [
        {"type": "para", "text": tl_intro},
        {
            "type": "problem",
            "label": b1["label"],
            "level": b1["level"],
            "statement": format_bai1_text(b1["statement"]),
            "solution": BR.join(b1["dap_an"]),
            "tier": "onclass"
        },
        # Khung ô ly cao 7cm (28 dòng caro) cho 4 phép tính, vừa vặn Trang 1
        {"type": "writelines", "variant": "oly", "count": 7},
        {"type": "para", "text": "\\newpage"}
    ]

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "",
        "blocks": p2_blocks,
        "teacher_note": "Trang 1 (Phần II): Bài 1 (1,0đ) Đặt tính rồi tính kèm khung ô ly 7cm. Kết thúc Trang 1."
    }

    # ── Trang 2: Bài 2 (Tính + ô ly 3.5cm) + Bài 3 (Điền chỗ chấm) ──
    b2 = D["bai"][1]
    b3 = D["bai"][2]
    stage3 = {
        "kind": "practice1",
        "number": 3,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b2["label"],
                "level": b2["level"],
                "statement": format_bai2_text(b2["statement"]),
                "solution": BR.join(b2["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 4},
            {
                "type": "problem",
                "label": b3["label"],
                "level": b3["level"],
                "statement": format_bai3_text(b3["statement"]),
                "solution": BR.join(b3["dap_an"]),
                "tier": "onclass"
            }
        ],
        "teacher_note": "Trang 2: Bài 2 (1,0đ) phân số/hỗn số (ô ly 4cm) và Bài 3 (1,0đ) đổi đơn vị đo."
    }

    # ── Trang 2 (tiếp): Bài 4 (Toán thực tế + ô ly 6cm) ──
    b4 = D["bai"][3]
    stage4 = {
        "kind": "practice2",
        "number": 4,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b4["label"],
                "level": b4["level"],
                "statement": b4["statement"],
                "solution": BR.join(b4["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 6}
        ],
        "teacher_note": "Trang 2: Bài 4 (2,0đ) Bài toán thực tế hình học kèm khung ô ly 6cm."
    }

    # ── Trang 2 (tiếp): Bài 5 (Toán tư duy + ô ly 3cm) + HẾT & Lời dặn dò ──
    b5 = D["bai"][4]
    het_note = (
        "\\par\\vspace{4pt}\n"
        "\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}\n"
        "\\par\\vspace{2pt}\n"
        "\\centerline{\\textit{\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}"
    )
    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b5["label"],
                "level": b5["level"],
                "statement": b5["statement"],
                "solution": BR.join(b5["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 3},
            {"type": "para", "text": het_note}
        ],
        "teacher_note": "Trang 2: Bài 5 (1,0đ) Vận dụng tư duy cao kèm khung ô ly 3cm và Lời dặn dò."
    }

    title = f"Đề kiểm tra cuối học kì I — Đề {D['so']} (40 phút)" if "Đề" in D.get('ten', '') else f"{D['ten']} (40 phút)"
    return {
        "slug": D["slug_de"],
        "title": title,
        "eyebrow": D["header_eyebrow"],
        "grade_label": "Lớp 5",
        "class_tier": "",
        "theme": "de_thi",
        "stages": [stage1, stage2, stage3, stage4, stage5]
    }


def make_mt_json(k, D):
    # Stage 1: Ma trận đề thi
    rows_tn = ""
    for c in D["tn"]:
        rows_tn += f"Câu {c['cau']} & {c['dang']} ({c['bai']}) & {c['muc']} -- {d(c['diem'])} điểm & {c['phut']} phút \\tabularnewline \\hline\n"

    rows_tl = ""
    for b in D["bai"]:
        rows_tl += f"{b['label']} & {b['dang']} ({b['bai']}) & {b['muc']} -- {d(b['diem'])} điểm & {b['phut']} phút \\tabularnewline \\hline\n"

    table_tn = (
        "\\noindent\\textbf{Bảng phân bố câu hỏi Phần I (Trắc nghiệm):} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{7.5cm}|c|c|}\n"
        "\\hline\n"
        "\\textbf{Phần I} & \\textbf{Dạng bài (bài học trong SGK)} & \\textbf{Mức -- điểm} & \\textbf{Thời lượng} \\tabularnewline\n"
        "\\hline\n"
        + rows_tn +
        "\\multicolumn{2}{|c|}{\\textbf{Cộng Phần I}} & \\textbf{4,0 điểm} & \\textbf{15 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    table_tl = (
        "\\noindent\\textbf{Bảng phân bố câu hỏi Phần II (Tự luận):} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{7.5cm}|c|c|}\n"
        "\\hline\n"
        "\\textbf{Phần II} & \\textbf{Dạng bài (bài học trong SGK)} & \\textbf{Mức -- điểm} & \\textbf{Thời lượng} \\tabularnewline\n"
        "\\hline\n"
        + rows_tl +
        "\\multicolumn{2}{|c|}{\\textbf{Cộng Phần II}} & \\textbf{6,0 điểm} & \\textbf{25 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\multicolumn{2}{|c|}{\\textbf{TỔNG CỘNG TOÀN ĐỀ}} & \\textbf{10,0 điểm} & \\textbf{40 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    truong_str = D.get('truong', 'Ban Chuyên môn Toán Tiểu học MathTech')
    ti_le_tt27 = (
        f"\\textbf{{Xuất xứ nguồn đề:}} {truong_str}. [[br]]"
        "\\textbf{Tỉ lệ mức độ theo Thông tư 27/2020/TT-BGDĐT:}\n"
        "\\begin{itemize}\n"
        "  \\item \\textbf{Mức 1 (Nhận biết):} $3{,}5$ điểm ($35\\%$) -- gồm Câu 1, 2, 3 Trắc nghiệm ($1{,}5$đ) và Bài 1, 2 Tự luận ($2{,}0$đ).\n"
        "  \\item \\textbf{Mức 2 (Thông hiểu / Kết nối):} $4{,}0$ điểm ($40\\%$) -- gồm Câu 4, 5, 6, 7 Trắc nghiệm ($2{,}0$đ), Bài 3 ($1{,}0$đ) và Bài 4 ý a ($1{,}0$đ).\n"
        "  \\item \\textbf{Mức 3 (Vận dụng):} $2{,}5$ điểm ($25\\%$) -- gồm Câu 8 Trắc nghiệm ($0{,}5$đ), Bài 4 ý b ($1{,}0$đ) và Bài 5 ($1{,}0$đ).\n"
        "\\end{itemize}\n"
        "\\textbf{Phạm vi kiến thức:} Chương trình Toán 5 Kết nối tri thức với cuộc sống (tập 1, Bài 1 đến Bài 35): Ôn tập phân số, hỗn số (CĐ1); Số thập phân, cấu tạo, so sánh, làm tròn (CĐ2); Đơn vị đo diện tích $km^2, ha$ (CĐ3); Các phép tính cộng, trừ, nhân, chia số thập phân, tính thuận tiện (CĐ4); Hình tam giác, hình thang, hình tròn (CĐ5); Ôn tập học kì 1 (CĐ6)."
    )

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": f"Ma trận Đề {D['so']}",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{MA TRẬN ĐỀ KIỂM TRA CHÍNH THỨC CUỐI HỌC KÌ I -- TOÁN 5 -- ĐỀ {D['so']}}} [[br]] {truong_str} [[br]] Thời gian làm bài: 40 phút. Thang điểm: 10,0 điểm (8 câu trắc nghiệm 4,0đ và 5 bài tự luận 6,0đ)."},
            {"type": "para", "text": table_tn},
            {"type": "para", "text": table_tl},
            {"type": "para", "text": ti_le_tt27}
        ]
    }

    # Stage 2: Đáp án Trắc nghiệm
    ans_cells = " & ".join(f"\\textbf{{{c['answer']}}}" for c in D["tn"])
    q_cells = " & ".join(f"Câu {c['cau']}" for c in D["tn"])
    ans_table = (
        "\\begin{center}\\small\\renewcommand{\\arraystretch}{1.2}\n"
        "\\begin{tabular}{|c|" + "c|"*len(D["tn"]) + "}\n"
        "\\hline\n"
        + q_cells + " \\tabularnewline\n"
        "\\hline\n"
        + ans_cells + " \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    tn_expl = []
    for c in D["tn"]:
        tn_expl.append(
            f"\\textbf{{Câu {c['cau']} ({d(c['diem'])}đ): Chọn {c['answer']}.}} {c['solution']} [[br]] "
            f"\\textit{{\\footnotesize Phân tích lỗi sai: {c['trap']}}}"
        )

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "Đáp án Phần I — Trắc nghiệm",
        "blocks": [
            {"type": "para", "text": "\\textbf{BẢNG ĐÁP ÁN TRẮC NGHIỆM (4,0 ĐIỂM)}" + BR + ans_table},
            {"type": "para", "text": "\\textbf{GIẢI THÍCH CHI TIẾT VÀ PHÂN TÍCH PHƯƠNG ÁN NHIỄU}" + BR + BR.join(tn_expl)}
        ]
    }

    # Stage 3: Đáp án Bài 1 và Bài 2
    b1 = D["bai"][0]
    b2 = D["bai"][1]
    stage3 = {
        "kind": "practice1",
        "number": 3,
        "title": "Đáp án Bài 1 và Bài 2",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b1['label'].upper()} ({d(b1['diem'])} ĐIỂM) -- {b1['dang'].upper()}}}" + BR + BR.join(b1["dap_an"]) + BR + f"\\textit{{\\footnotesize {b1['note']}}}"},
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b2['label'].upper()} ({d(b2['diem'])} ĐIỂM) -- {b2['dang'].upper()}}}" + BR + BR.join(b2["dap_an"]) + BR + f"\\textit{{\\footnotesize {b2['note']}}}"}
        ]
    }

    # Stage 4: Đáp án Bài 3 và Bài 4
    b3 = D["bai"][2]
    b4 = D["bai"][3]
    stage4 = {
        "kind": "practice2",
        "number": 4,
        "title": "Đáp án Bài 3 và Bài 4",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b3['label'].upper()} ({d(b3['diem'])} ĐIỂM) -- {b3['dang'].upper()}}}" + BR + BR.join(b3["dap_an"]) + BR + f"\\textit{{\\footnotesize {b3['note']}}}"},
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b4['label'].upper()} ({d(b4['diem'])} ĐIỂM) -- {b4['dang'].upper()}}}" + BR + BR.join(b4["dap_an"]) + BR + f"\\textit{{\\footnotesize {b4['note']}}}"}
        ]
    }

    # Stage 5: Đáp án Bài 5, Hướng dẫn chấm và Mẹo sư phạm
    b5 = D["bai"][4]
    huong_dan_cham = (
        "\\textbf{HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM CHI TIẾT (Theo Thông tư 27/2020)} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{7.5cm}|p{7.5cm}|}\n"
        "\\hline\n"
        "\\textbf{Lỗi thường gặp của học sinh} & \\textbf{Quy định chấm và trừ điểm} \\tabularnewline\n"
        "\\hline\n"
        "Đặt tính không thẳng cột dấu phẩy & Chỉ cho điểm kết quả nếu đúng, trừ 0,25đ kĩ năng đặt tính \\tabularnewline \\hline\n"
        "Phép nhân: tách sai số chữ số ở phần thập phân & Không cho điểm phép tính đó \\tabularnewline \\hline\n"
        "Phép chia: quên gạch dấu phẩy ở số chia & Không cho điểm phần đặt tính, chỉ cho nửa điểm nếu kết quả đúng \\tabularnewline \\hline\n"
        "Kết quả phân số chưa rút gọn về tối giản & Trừ 0,25 điểm cho ý đó \\tabularnewline \\hline\n"
        "Bài có lời văn: thiếu câu lời giải hoặc sai lời giải & Trừ 0,25 điểm cho mỗi ý \\tabularnewline \\hline\n"
        "Viết sai hoặc thiếu tên đơn vị trong bài toán & Trừ 0,25 điểm cho mỗi chỗ sai (tối đa không quá 0,5đ toàn bài) \\tabularnewline \\hline\n"
        "Học sinh giải cách khác đúng & Cho điểm tối đa tương ứng từng bước \\tabularnewline \\hline\n"
        "\\end{tabular}\\end{center}\n"
        "\\noindent\\textit{\\footnotesize Điểm toàn bài là số nguyên từ 0 đến 10, nếu điểm là số thập phân thì làm tròn theo Thông tư 27 (tổng điểm lẻ từ 0,5 trở lên làm tròn thành 1).}"
    )

    meo_su_pham = (
        "\\textbf{MẸO SƯ PHẠM ĐIỀU PHỐI (DÀNH CHO GIÁO VIÊN)}\n"
        "\\begin{itemize}\n"
        "  \\item \\textbf{Điều phối giờ làm bài:} Dành đúng 15 phút cho Phần I và 25 phút cho Phần II. Với bài toán lời văn Bài 4, nhắc học sinh vẽ sơ đồ tóm tắt ra nháp trước khi làm.\n"
        "  \\item \\textbf{Kĩ năng dời dấu phẩy (Bài 5):} Nhắc học sinh phân biệt rõ dời dấu phẩy sang phải (gấp lên 10, 100 lần) và dời dấu phẩy sang trái (giảm đi 10, 100 lần).\n"
        "  \\item \\textbf{Đổi đơn vị đo diện tích:} Rèn thói quen kiểm tra bước nhảy đơn vị: mỗi bước diện tích tương ứng 2 chữ số 0 ($1\\text{ ha} = 100\\text{ dam}^2 = 10\\,000\\text{ m}^2$).\n"
        "  \\item \\textbf{Chấm điểm linh hoạt:} Học sinh có thể tính gộp các bước trong bài toán có lời văn, nếu lập luận đúng và kết quả chính xác vẫn cho điểm trọn vẹn.\n"
        "\\end{itemize}"
    )

    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "Đáp án Bài 5, Biểu điểm và Mẹo sư phạm",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b5['label'].upper()} ({d(b5['diem'])} ĐIỂM) -- {b5['dang'].upper()}}}" + BR + BR.join(b5["dap_an"]) + BR + f"\\textit{{\\footnotesize {b5['note']}}}"},
            {"type": "para", "text": huong_dan_cham}
        ],
        "teacher_note": meo_su_pham
    }

    title = f"Ma trận đề và đáp án chi tiết — {D['ten']}"
    return {
        "slug": D["slug_mt"],
        "title": title,
        "eyebrow": f"SỔ TAY GIÁO VIÊN • LỚP 5 • {D['ten'].upper()}",
        "grade_label": "Lớp 5",
        "class_tier": "",
        "theme": "de_thi",
        "trinh_bay": "thoang",
        "stages": [stage1, stage2, stage3, stage4, stage5]
    }


if __name__ == "__main__":
    print("Bắt đầu sinh 3 đề ôn tập Cuối Kì 1 Toán 5 KNTT...")
    for k, D in DE.items():
        p_de = OUT / f"{D['slug_de']}.json"
        p_mt = OUT / f"{D['slug_mt']}.json"
        
        de_data = make_de_json(k, D)
        mt_data = make_mt_json(k, D)
        
        p_de.write_text(json.dumps(de_data, ensure_ascii=False, indent=2), encoding="utf-8")
        p_mt.write_text(json.dumps(mt_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Đã sinh: {p_de.name} và {p_mt.name}")

    print("Hoàn tất sinh 3 đề ôn tập Cuối Kì 1 Toán 5 KNTT.")
