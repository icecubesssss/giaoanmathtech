#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BỘ ĐỀ KIỂM TRA CHÍNH THỨC CUỐI HỌC KÌ 1 (CK1) TOÁN 5 KẾT NỐI TRI THỨC (KNTT) - NĂM HỌC 2024-2025 & 2025-2026.
Sinh 3 đề kiểm tra chính thức (Đề 1, Đề 2, Đề 3) + 3 file Ma trận đề và đáp án chi tiết cho GV
vào inputs/seeds/lop-5/de-cuoi-ki-1/ (theme de_thi, trinh_bay "thoang").

Cấu trúc chuẩn đề thi Tiểu học (Thông tư 27, 40 phút, thang 10 điểm):
- PHẦN I. TRẮC NGHIỆM (4,0 điểm): 8 câu x 0,5đ (M1: 3 câu, M2: 4 câu, M3: 1 câu nâng cao).
- PHẦN II. TỰ LUẬN (6,0 điểm):
  + Bài 1 (1,0đ): Đặt tính rồi tính (4 phép tính: cộng, trừ, nhân, chia số thập phân).
  + Bài 2 (1,0đ): Tính giá trị biểu thức / tính với phân số hoặc hỗn số.
  + Bài 3 (1,0đ): Viết số thích hợp vào chỗ chấm (đổi đơn vị đo độ dài, khối lượng, diện tích).
  + Bài 4 (2,0đ): Bài toán có lời văn thực tế hình học (hình thang / hình tròn / tam giác).
  + Bài 5 (1,0đ): Bài toán tư duy nâng cao (dời dấu phẩy, cấu tạo số, tính thuận tiện).
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

# ─────────────────────────── DỮ LIỆU 3 ĐỀ CHÍNH THỨC ───────────────────────────
DE = {
    "de1": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-de-1",
        "slug_mt": "ma-tran-va-dap-an-cuoi-ki-1-de-1",
        "so": "1",
        "ten": "Đề kiểm tra cuối học kì I — Đề 1",
        "eyebrow": "LỚP 5 • ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I",
        "header_eyebrow": "ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I · NĂM HỌC 2024 – 2025",
        "truong": "Trường Tiểu học Nghĩa Tân (Cầu Giấy, Hà Nội)",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Giá trị chữ số theo hàng",
                "statement": "Chữ số $4$ trong số thập phân $53,412$ có giá trị là:",
                "options": ["$4$", "$\\dfrac{4}{10}$", "$\\dfrac{4}{100}$", "$\\dfrac{4}{1000}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số $4$ đứng ngay sau dấu phẩy nên thuộc hàng phần mười, có giá trị là $\\dfrac{4}{10}$ (hoặc $0,4$).",
                "trap": "Học sinh chọn 4 hoặc 4/100."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Cấu tạo số thập phân",
                "statement": "Số gồm $3$ chục, $2$ đơn vị, $7$ phần trăm, $6$ phần nghìn được viết là:",
                "options": ["$3,276$", "$32,76$", "$32,076$", "$320,76$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Phần nguyên là $32$. Hàng phần mười không có nên viết chữ số $0$, hàng phần trăm là $7$, hàng phần nghìn là $6$: viết là $32,076$.",
                "trap": "Học sinh quên chữ số 0 ở hàng phần mười nên chọn 32,76."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 27", "phut": 1.5,
                "dang": "Đường kính và bán kính hình tròn",
                "statement": "Đường kính của một hình tròn có bán kính $r = 4,5\\text{ cm}$ là:",
                "options": ["$9\\text{ cm}$", "$2,25\\text{ cm}$", "$14,13\\text{ cm}$", "$28,26\\text{ cm}$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Đường kính hình tròn bằng $2$ lần bán kính: $d = 2 \\times r = 4,5 \\times 2 = 9\\text{ cm}$.",
                "trap": "Học sinh chia 2 ra 2,25 cm hoặc tính nhầm sang chu vi."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "So sánh số thập phân",
                "statement": "Số thập phân nhỏ nhất trong các số $2,454$; $4,743$; $2,345$; $3,542$ là:",
                "options": ["$2,454$", "$4,743$", "$2,345$", "$3,542$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Hai số có phần nguyên bé nhất bằng $2$ là $2,454$ và $2,345$. So hàng phần mười: $3 < 4$ nên $2,345$ nhỏ nhất.",
                "trap": "Học sinh chọn 2,454 do nhìn thoáng qua phần nguyên."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn đến hàng phần mười",
                "statement": "Làm tròn số thập phân $9,385$ đến hàng phần mười ta được số:",
                "options": ["$9,3$", "$9,4$", "$9,38$", "$9,39$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần trăm là $8 \\ge 5$ nên ta cộng thêm $1$ vào hàng phần mười: $3 + 1 = 4$, được $9,4$.",
                "trap": "Học sinh cắt cụt thành 9,3."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 15", "phut": 2.0,
                "dang": "Đổi ha sang m²",
                "statement": "Trong các số dưới đây, số đo bằng $2,45\\text{ ha}$ là:",
                "options": ["$24\\,500\\text{ m}^2$", "$0,245\\text{ km}^2$", "$245\\,000\\text{ m}^2$", "$24\\,500\\text{ dm}^2$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Vì $1\\text{ ha} = 10\\,000\\text{ m}^2$ nên $2,45\\text{ ha} = 2,45 \\times 10\\,000 = 24\\,500\\text{ m}^2$.",
                "trap": "Học sinh nhân 1000 ra 2450 m² hoặc nhầm đơn vị km²."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 23", "phut": 2.0,
                "dang": "Nhân nhẩm số thập phân với 0,001",
                "statement": "Kết quả của phép tính nhẩm $765,9 \\times 0,001$ là:",
                "options": ["$7,659$", "$765\\,900$", "$0,7659$", "$7\\,659\\,000$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Khi nhân một số thập phân với $0,001$, ta chuyển dấu phẩy sang bên trái $3$ chữ số: $765,9 \\times 0,001 = 0,7659$.",
                "trap": "Học sinh chuyển nhầm 2 hàng thành 7,659."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 22", "phut": 3.0,
                "dang": "Xác định số dư trong phép chia số thập phân",
                "statement": "Quan sát phép chia $43,19 : 21$ lấy đến $2$ chữ số ở phần thập phân của thương, ta được thương là $2,05$. Số dư của phép chia đó là:",
                "options": ["$14$", "$1,4$", "$0,14$", "$0,014$"],
                "answer": "D",
                "solution": "Chọn \\textbf{D}. Dóng thẳng hàng dấu phẩy của số bị chia xuống hàng của số dư: chữ số $1$ ở hàng phần trăm, chữ số $4$ ở hàng phần nghìn. Vậy số dư là $0,014$. Thử lại: $21 \\times 2,05 + 0,014 = 43,05 + 0,014 = 43,19$.",
                "trap": "Học sinh nhìn phần dư còn lại 14 mà không dóng dấu phẩy, chọn A hoặc C."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $52,65 + 38,7$ [[br]] b) $104,3 - 58,46$ [[br]] c) $18,5 \\times 4,2$ [[br]] d) $147,6 : 3,6$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $52,65 + 38,70 = 91,35$.",
                    "\\textbf{b) (0,25đ)} $104,30 - 58,46 = 45,84$.",
                    "\\textbf{c) (0,25đ)} $18,5 \\times 4,2 = 77,70 = 77,7$.",
                    "\\textbf{d) (0,25đ)} $147,6 : 3,6 = 1476 : 36 = 41$."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{7}{12} + \\dfrac{5}{8}$ [[br]] b) $2\\dfrac{2}{3} : \\dfrac{8}{9}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số chung là 24: $\\dfrac{7}{12} + \\dfrac{5}{8} = \\dfrac{14}{24} + \\dfrac{15}{24} = \\dfrac{29}{24}$.",
                    "\\textbf{b) (0,5đ)} Chuyển hỗn số ra phân số rồi chia: $2\\dfrac{2}{3} : \\dfrac{8}{9} = \\dfrac{8}{3} \\times \\dfrac{9}{8} = 3$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $9\\text{ m } 25\\text{ mm} = \\dots\\dots\\dots\\dots\\text{ m}$ [[br]] b) $7\\text{ yến } 5\\text{ kg} = \\dots\\dots\\dots\\dots\\text{ yến}$ [[br]] c) $16\\text{ ha } 500\\text{ m}^2 = \\dots\\dots\\dots\\dots\\text{ ha}$ [[br]] d) $5\\text{ km}^2\\ 8\\text{ ha} = \\dots\\dots\\dots\\dots\\text{ km}^2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $9\\text{ m } 25\\text{ mm} = 9,025\\text{ m}$.",
                    "\\textbf{b) (0,25đ)} $7\\text{ yến } 5\\text{ kg} = 7,5\\text{ yến}$.",
                    "\\textbf{c) (0,25đ)} $16\\text{ ha } 500\\text{ m}^2 = 16,05\\text{ ha}$.",
                    "\\textbf{d) (0,25đ)} $5\\text{ km}^2\\ 8\\text{ ha} = 5,08\\text{ km}^2$."
                ],
                "note": "Mỗi ý đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 26, Bài 9", "phut": 8.0,
                "dang": "Bài toán thực tế hình thang và sản lượng lúa",
                "statement": "\\textbf{(2,0 điểm)} Một thửa ruộng hình thang có đáy lớn $50\\text{ m}$, đáy bé bằng $\\dfrac{4}{5}$ đáy lớn. Chiều cao bằng trung bình cộng của hai đáy. [[br]] a) Tính diện tích thửa ruộng hình thang đó. [[br]] b) Người ta trồng lúa trên thửa ruộng, cứ $100\\text{ m}^2$ thu hoạch được $70\\text{ kg}$ thóc. Hỏi cả thửa ruộng thu hoạch được bao nhiêu tạ thóc?",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Đáy bé thửa ruộng là: $50 \\times \\dfrac{4}{5} = 40\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Chiều cao thửa ruộng là: $(50 + 40) : 2 = 45\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Diện tích thửa ruộng hình thang là: $(50 + 40) \\times 45 : 2 = 2025\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Cả thửa ruộng thu hoạch được số ki-lô-gam thóc là: [[br]] $2025 : 100 \\times 70 = 1417,5\\text{ (kg)}$ \\hfill \\textit{(0,50đ)} [[br]] Đổi: $1417,5\\text{ kg} = 14,175\\text{ tạ}$ \\hfill \\textit{(0,25đ)} [[br]] Đáp số: a) $2025\\text{ m}^2$; b) $14,175\\text{ tạ thóc}$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Đầy đủ câu lời giải, phép tính, đơn vị và đáp số."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Bài 23, Cấu tạo số", "phut": 4.0,
                "dang": "Toán tư duy dời dấu phẩy số thập phân",
                "statement": "\\textbf{(1,0 điểm)} Tìm một số thập phân biết rằng nếu dời dấu phẩy của số đó sang bên phải một chữ số thì số đó tăng thêm $175,05$ đơn vị.",
                "dap_an": [
                    "Khi dời dấu phẩy của một số thập phân sang bên phải một chữ số thì số đó gấp lên $10$ lần số ban đầu. \\hfill \\textit{(0,25đ)} [[br]] Coi số ban đầu là $1$ phần thì số mới là $10$ phần như thế. [[br]] Hiệu số phần bằng nhau là: $10 - 1 = 9$ (phần). \\hfill \\textit{(0,25đ)} [[br]] Số thập phân cần tìm là: $175,05 : 9 = 19,45$. \\hfill \\textit{(0,25đ)} [[br]] Đáp số: $19,45$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Lập luận đúng quan hệ gấp 10 lần được 0,25đ; tìm hiệu số phần được 0,25đ; tính ra đáp số 19,45 được 0,5đ."
            }
        ]
    },

    "de2": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-de-2",
        "slug_mt": "ma-tran-va-dap-an-cuoi-ki-1-de-2",
        "so": "2",
        "ten": "Đề kiểm tra cuối học kì I — Đề 2",
        "eyebrow": "LỚP 5 • ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I",
        "header_eyebrow": "ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I · NĂM HỌC 2024 – 2025",
        "truong": "Trường Tiểu học Nam Từ Liêm và TH Kim Đồng (Hà Nội)",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 7", "phut": 1.5,
                "dang": "Nhận biết phần nguyên của hỗn số",
                "statement": "Hỗn số $15\\dfrac{3}{4}$ có phần nguyên là:",
                "options": ["$5$", "$3$", "$15$", "$\\dfrac{3}{4}$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Hỗn số gồm phần nguyên là $15$ và phần phân số là $\\dfrac{3}{4}$.",
                "trap": "Học sinh chọn phần phân số hoặc chỉ lấy chữ số hàng đơn vị."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Giá trị chữ số theo hàng",
                "statement": "Giá trị của chữ số $5$ trong số thập phân $32,456$ là:",
                "options": ["$5$", "$\\dfrac{5}{10}$", "$\\dfrac{5}{100}$", "$\\dfrac{5}{1000}$"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Chữ số $5$ ở hàng phần trăm nên có giá trị là $\\dfrac{5}{100}$ (hoặc $0,05$).",
                "trap": "Học sinh chọn 5/10."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 29", "phut": 1.5,
                "dang": "Diện tích hình tròn",
                "statement": "Một hình tròn có bán kính $r = 6\\text{ cm}$. Diện tích của hình tròn đó là:",
                "options": ["$37,68\\text{ cm}^2$", "$113,04\\text{ cm}^2$", "$18,84\\text{ cm}^2$", "$113,04\\text{ cm}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Diện tích hình tròn là $S = r \\times r \\times 3,14 = 6 \\times 6 \\times 3,14 = 113,04\\text{ cm}^2$.",
                "trap": "Học sinh tính nhầm chu vi ra 37,68 cm² hoặc sai đơn vị đo."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "Sắp xếp số thập phân",
                "statement": "Cho các số thập phân: $5,879$; $5,689$; $5,925$; $5,798$. Sắp xếp các số theo thứ tự từ lớn đến bé là:",
                "options": [
                    "$5,925;\\; 5,879;\\; 5,798;\\; 5,689$",
                    "$5,689;\\; 5,798;\\; 5,879;\\; 5,925$",
                    "$5,925;\\; 5,798;\\; 5,879;\\; 5,689$",
                    "$5,879;\\; 5,925;\\; 5,798;\\; 5,689$"
                ],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Phần nguyên đều bằng $5$. So sánh hàng phần mười: $9 > 8 > 7 > 6$. Thứ tự từ lớn đến bé là $5,925 > 5,879 > 5,798 > 5,689$.",
                "trap": "Học sinh nhầm thứ tự từ bé đến lớn (chọn B)."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn đến số tự nhiên gần nhất",
                "statement": "Làm tròn số $15,48$ đến số tự nhiên gần nhất thì được số:",
                "options": ["$16$", "$15$", "$15,5$", "$15,4$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần mười là $4 < 5$ nên ta làm tròn xuống: $15$.",
                "trap": "Học sinh làm tròn 2 lần: 15,48 thành 15,5 rồi làm tròn thành 16."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 15", "phut": 2.0,
                "dang": "Đổi đơn vị diện tích km², ha",
                "statement": "$12\\text{ km}^2\\ 50\\text{ ha} = \\dots\\dots\\text{ km}^2$. Số thích hợp viết vào chỗ chấm là:",
                "options": ["$12,05$", "$12,5$", "$12,50$", "$1250$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Vì $1\\text{ km}^2 = 100\\text{ ha}$ nên $50\\text{ ha} = 0,5\\text{ km}^2$. Do đó $12\\text{ km}^2\\ 50\\text{ ha} = 12,5\\text{ km}^2$.",
                "trap": "Học sinh nhầm 1 km² = 1000 ha chọn 12,05."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 22", "phut": 2.0,
                "dang": "Toán thực tế diện tích hình chữ nhật",
                "statement": "Một khu đất hình chữ nhật có diện tích $72,8\\text{ m}^2$, chiều dài là $10,4\\text{ m}$. Chiều rộng của khu đất đó là:",
                "options": ["$7\\text{ m}$", "$7,2\\text{ m}$", "$6,5\\text{ m}$", "$8\\text{ m}$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Chiều rộng của khu đất là: $72,8 : 10,4 = 728 : 104 = 7\\text{ (m)}$.",
                "trap": "Học sinh tính nhầm phép chia số thập phân ra 7,2."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 29", "phut": 3.0,
                "dang": "Hình ghép thực tế diện tích hình tròn",
                "statement": "Bạn Việt làm một biển báo giao thông hình tròn bằng bìa có đường kính $40\\text{ cm}$. Ở giữa là hình chữ nhật có diện tích bằng $\\dfrac{1}{5}$ diện tích của biển báo. Diện tích phần hình chữ nhật ở giữa biển báo là:",
                "options": ["$251,2\\text{ cm}^2$", "$251,5\\text{ cm}^2$", "$250\\text{ cm}^2$", "$252,2\\text{ cm}^2$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Bán kính biển báo là $40 : 2 = 20\\text{ (cm)}$. Diện tích biển báo là $20 \\times 20 \\times 3,14 = 1256\\text{ (cm}^2\\text{)}$. Diện tích hình chữ nhật là $1256 : 5 = 251,2\\text{ (cm}^2\\text{)}$.",
                "trap": "Học sinh lấy luôn đường kính 40 nhân 40 dẫn đến kết quả sai gấp 4 lần."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $64,8 + 49,35$ [[br]] b) $120 - 45,68$ [[br]] c) $23,7 \\times 4,6$ [[br]] d) $91,2 : 2,4$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $64,80 + 49,35 = 114,15$.",
                    "\\textbf{b) (0,25đ)} $120,00 - 45,68 = 74,32$.",
                    "\\textbf{c) (0,25đ)} $23,7 \\times 4,6 = 109,02$.",
                    "\\textbf{d) (0,25đ)} $91,2 : 2,4 = 912 : 24 = 38$."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{5}{9} + \\dfrac{1}{6}$ [[br]] b) $1\\dfrac{3}{4} \\times \\dfrac{2}{7}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số chung là 18: $\\dfrac{5}{9} + \\dfrac{1}{6} = \\dfrac{10}{18} + \\dfrac{3}{18} = \\dfrac{13}{18}$.",
                    "\\textbf{b) (0,5đ)} $1\\dfrac{3}{4} \\times \\dfrac{2}{7} = \\dfrac{7}{4} \\times \\dfrac{2}{7} = \\dfrac{14}{28} = \\dfrac{1}{2}$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $12\\text{ dm } 6\\text{ mm} = \\dots\\dots\\dots\\dots\\text{ dm}$ [[br]] b) $5\\text{ tấn } 60\\text{ kg} = \\dots\\dots\\dots\\dots\\text{ tấn}$ [[br]] c) $3\\text{ ha } 45\\text{ m}^2 = \\dots\\dots\\dots\\dots\\text{ ha}$ [[br]] d) $7\\text{ km}^2 = \\dots\\dots\\dots\\dots\\text{ ha}$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $12\\text{ dm } 6\\text{ mm} = 12,06\\text{ dm}$.",
                    "\\textbf{b) (0,25đ)} $5\\text{ tấn } 60\\text{ kg} = 5,06\\text{ tấn}$.",
                    "\\textbf{c) (0,25đ)} $3\\text{ ha } 45\\text{ m}^2 = 3,0045\\text{ ha}$.",
                    "\\textbf{d) (0,25đ)} $7\\text{ km}^2 = 700\\text{ ha}$."
                ],
                "note": "Mỗi ý đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 8, Bài 29", "phut": 8.0,
                "dang": "Bài toán tổng - tỉ và diện tích ao hình tròn",
                "statement": "\\textbf{(2,0 điểm)} Một mảnh đất hình chữ nhật có chu vi là $140\\text{ m}$, chiều rộng bằng $\\dfrac{3}{4}$ chiều dài. [[br]] a) Tính diện tích mảnh đất hình chữ nhật đó. [[br]] b) Ở giữa mảnh đất, người ta đào một cái ao nuôi cá dạng hình tròn có bán kính $r = 5\\text{ m}$. Tính diện tích phần đất còn lại để trồng cây.",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Nửa chu vi mảnh đất là: $140 : 2 = 70\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Chiều rộng mảnh đất là: $70 : (3 + 4) \\times 3 = 30\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Chiều dài mảnh đất là: $70 - 30 = 40\\text{ (m)}$ \\hfill \\textit{(0,25đ)} [[br]] Diện tích mảnh đất hình chữ nhật là: $40 \\times 30 = 1200\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,25đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Diện tích cái ao nuôi cá hình tròn là: $5 \\times 5 \\times 3,14 = 78,5\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)} [[br]] Diện tích phần đất còn lại để trồng cây là: $1200 - 78,5 = 1121,5\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,25đ)} [[br]] Đáp số: a) $1200\\text{ m}^2$; b) $1121,5\\text{ m}^2$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Đầy đủ lời giải, phép tính và đáp số."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Bài 23", "phut": 4.0,
                "dang": "Tính bằng cách thuận tiện nhất",
                "statement": "\\textbf{(1,0 điểm)} Tính bằng cách thuận tiện nhất: [[br]] $3,45 \\times 74 + 3,45 \\times 27 - 3,45$",
                "dap_an": [
                    "Ta có: [[br]] $3,45 \\times 74 + 3,45 \\times 27 - 3,45$ [[br]] $= 3,45 \\times 74 + 3,45 \\times 27 - 3,45 \\times 1$ \\hfill \\textit{(0,25đ)} [[br]] $= 3,45 \\times (74 + 27 - 1)$ \\hfill \\textit{(0,25đ)} [[br]] $= 3,45 \\times 100$ \\hfill \\textit{(0,25đ)} [[br]] $= 345$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Đưa thừa số chung 3,45 ra ngoài được 0,5đ; ra kết quả 345 được 0,5đ."
            }
        ]
    },

    "de3": {
        "slug_de": "de-kiem-tra-cuoi-ki-1-de-3",
        "slug_mt": "ma-tran-va-dap-an-cuoi-ki-1-de-3",
        "so": "3",
        "ten": "Đề kiểm tra cuối học kì I — Đề 3",
        "eyebrow": "LỚP 5 • ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I",
        "header_eyebrow": "ĐỀ KIỂM TRA ĐỊNH KÌ CUỐI HỌC KÌ I · NĂM HỌC 2024 – 2025",
        "truong": "Trường Tiểu học Chu Văn An và Marie Curie (Hà Nội)",
        "tn": [
            {
                "cau": 1, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 4, 10", "phut": 1.5,
                "dang": "Phân số sang số thập phân",
                "statement": "Phân số $\\dfrac{3}{25}$ được viết thành số thập phân là:",
                "options": ["$0,3$", "$0,12$", "$0,06$", "$1,2$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. $\\dfrac{3}{25} = \\dfrac{3 \\times 4}{25 \\times 4} = \\dfrac{12}{100} = 0,12$.",
                "trap": "Học sinh chọn 0,3 do lấy 3 chia 10."
            },
            {
                "cau": 2, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 10", "phut": 1.5,
                "dang": "Hàng của số thập phân",
                "statement": "Chữ số $3$ trong số thập phân $45,389$ thuộc hàng nào?",
                "options": ["Hàng phần mười", "Hàng chục", "Hàng đơn vị", "Hàng phần trăm"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Chữ số $3$ nằm ngay sau dấu phẩy nên thuộc hàng phần mười.",
                "trap": "Học sinh nhầm với hàng phần trăm."
            },
            {
                "cau": 3, "level": 1, "muc": "M1", "diem": 0.5, "bai": "Bài 26", "phut": 1.5,
                "dang": "Diện tích hình thang",
                "statement": "Một hình thang có độ dài hai đáy lần lượt là $12\\text{ cm}$ và $8\\text{ cm}$, chiều cao là $6\\text{ cm}$. Diện tích của hình thang đó là:",
                "options": ["$120\\text{ cm}^2$", "$60\\text{ cm}^2$", "$30\\text{ cm}^2$", "$48\\text{ cm}^2$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Diện tích hình thang là $S = (12 + 8) \\times 6 : 2 = 60\\text{ cm}^2$.",
                "trap": "Học sinh quên chia cho 2 ra 120 cm²."
            },
            {
                "cau": 4, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 11", "phut": 2.0,
                "dang": "Số thập phân bằng nhau",
                "statement": "Điền dấu thích hợp ($>, <, =$) vào chỗ chấm: $4,5 \\dots\\dots 4,500$:",
                "options": ["$>$", "$<$", "$=$", "Không so sánh được"],
                "answer": "C",
                "solution": "Chọn \\textbf{C}. Hai số thập phân bằng nhau vì khi viết thêm hoặc bỏ bớt các chữ số $0$ ở tận cùng bên phải phần thập phân thì giá trị số đó không đổi: $4,5 = 4,500$.",
                "trap": "Học sinh đếm số chữ số thấy 4,500 nhiều chữ số hơn nên chọn <."
            },
            {
                "cau": 5, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 13", "phut": 2.0,
                "dang": "Làm tròn đến hàng phần mười",
                "statement": "Làm tròn số $47,356$ đến hàng phần mười ta được số:",
                "options": ["$47,3$", "$47,4$", "$47,36$", "$47$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Chữ số hàng phần trăm là $5 \\ge 5$ nên ta cộng thêm $1$ vào hàng phần mười: $3 + 1 = 4$, được $47,4$.",
                "trap": "Học sinh giữ nguyên 47,3 (quên cộng 1 khi hàng phần trăm là 5)."
            },
            {
                "cau": 6, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 16", "phut": 2.0,
                "dang": "Đổi m² và dm² sang m²",
                "statement": "$23\\text{ m}^2\\ 45\\text{ dm}^2 = \\dots\\dots\\text{ m}^2$. Số thập phân thích hợp điền vào chỗ chấm là:",
                "options": ["$23,45$", "$23,045$", "$234,5$", "$2,345$"],
                "answer": "A",
                "solution": "Chọn \\textbf{A}. Vì $1\\text{ m}^2 = 100\\text{ dm}^2$ nên $45\\text{ dm}^2 = 0,45\\text{ m}^2$. Do đó $23\\text{ m}^2\\ 45\\text{ dm}^2 = 23,45\\text{ m}^2$.",
                "trap": "Học sinh nhầm 1 m² = 10 dm² chia cho 10 ra 234,5."
            },
            {
                "cau": 7, "level": 2, "muc": "M2", "diem": 0.5, "bai": "Bài 9", "phut": 2.0,
                "dang": "Rút về đơn vị - chuyển động",
                "statement": "Một ô tô đi trong $2$ giờ được $90\\text{ km}$. Hỏi với vận tốc đó, ô tô đi quãng đường $225\\text{ km}$ hết bao nhiêu thời gian?",
                "options": ["$4\\text{ giờ}$", "$5\\text{ giờ}$", "$4,5\\text{ giờ}$", "$5,5\\text{ giờ}$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Trong $1$ giờ ô tô đi được: $90 : 2 = 45\\text{ (km)}$. Thời gian để ô tô đi hết $225\\text{ km}$ là: $225 : 45 = 5\\text{ (giờ)}$.",
                "trap": "Học sinh tính nhầm 225 : 45 ra 4,5."
            },
            {
                "cau": 8, "level": 3, "muc": "M3", "diem": 0.5, "bai": "Bài 23", "phut": 3.0,
                "dang": "Toán tư duy quy tắc dịch dấu phẩy",
                "statement": "Khi nhân một số thập phân với $10$, một bạn học sinh đã sơ ý chuyển dấu phẩy sang bên trái một hàng nên được kết quả là $2,45$. Kết quả đúng của phép nhân đó phải là:",
                "options": ["$24,5$", "$245$", "$0,245$", "$2450$"],
                "answer": "B",
                "solution": "Chọn \\textbf{B}. Khi chuyển dấu phẩy sang trái một hàng, bạn đó đã chia số đó cho $10$. Vậy số thập phân ban đầu là $2,45 \\times 10 = 24,5$. Kết quả đúng của phép nhân là $24,5 \\times 10 = 245$.",
                "trap": "Học sinh mới tìm ra số ban đầu 24,5 đã vội chọn A mà quên nhân tiếp với 10."
            }
        ],
        "bai": [
            {
                "label": "Bài 1.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 19, 20, 21, 22", "phut": 5.0,
                "dang": "Đặt tính rồi tính (4 phép tính số thập phân)",
                "statement": "\\textbf{(1,0 điểm)} Đặt tính rồi tính: [[br]] a) $87,45 + 56,8$ [[br]] b) $135,2 - 68,45$ [[br]] c) $34,8 \\times 2,5$ [[br]] d) $117,8 : 3,8$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $87,45 + 56,80 = 144,25$.",
                    "\\textbf{b) (0,25đ)} $135,20 - 68,45 = 66,75$.",
                    "\\textbf{c) (0,25đ)} $34,8 \\times 2,5 = 87,00 = 87$.",
                    "\\textbf{d) (0,25đ)} $117,8 : 3,8 = 1178 : 38 = 31$."
                ],
                "note": "Mỗi phép tính đúng cho 0,25đ."
            },
            {
                "label": "Bài 2.", "level": 1, "muc": "M1", "diem": 1.0, "bai": "Bài 6, Bài 7", "phut": 4.0,
                "dang": "Tính với phân số và hỗn số",
                "statement": "\\textbf{(1,0 điểm)} Tính: [[br]] a) $\\dfrac{11}{15} - \\dfrac{3}{10}$ [[br]] b) $2\\dfrac{1}{2} : \\dfrac{5}{4}$",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Quy đồng mẫu số chung là 30: $\\dfrac{11}{15} - \\dfrac{3}{10} = \\dfrac{22}{30} - \\dfrac{9}{30} = \\dfrac{13}{30}$.",
                    "\\textbf{b) (0,5đ)} $2\\dfrac{1}{2} : \\dfrac{5}{4} = \\dfrac{5}{2} \\times \\dfrac{4}{5} = 2$."
                ],
                "note": "Mỗi ý đúng cho 0,5đ."
            },
            {
                "label": "Bài 3.", "level": 2, "muc": "M2", "diem": 1.0, "bai": "Bài 12, 15, 16", "phut": 4.0,
                "dang": "Viết số thích hợp vào chỗ chấm",
                "statement": "\\textbf{(1,0 điểm)} Viết số thích hợp vào chỗ chấm: [[br]] a) $18\\text{ m } 4\\text{ cm} = \\dots\\dots\\dots\\dots\\text{ m}$ [[br]] b) $8\\text{ tạ } 15\\text{ kg} = \\dots\\dots\\dots\\dots\\text{ tạ}$ [[br]] c) $4\\text{ km}^2\\ 50\\text{ ha} = \\dots\\dots\\dots\\dots\\text{ km}^2$ [[br]] d) $35\\text{ m}^2\\ 8\\text{ dm}^2 = \\dots\\dots\\dots\\dots\\text{ m}^2$",
                "dap_an": [
                    "\\textbf{a) (0,25đ)} $18\\text{ m } 4\\text{ cm} = 18,04\\text{ m}$.",
                    "\\textbf{b) (0,25đ)} $8\\text{ tạ } 15\\text{ kg} = 8,15\\text{ tạ}$.",
                    "\\textbf{c) (0,25đ)} $4\\text{ km}^2\\ 50\\text{ ha} = 4,5\\text{ km}^2$.",
                    "\\textbf{d) (0,25đ)} $35\\text{ m}^2\\ 8\\text{ dm}^2 = 35,08\\text{ m}^2$."
                ],
                "note": "Mỗi ý đúng cho 0,25đ."
            },
            {
                "label": "Bài 4.", "level": 2, "muc": "M2: 1,0đ + M3: 1,0đ", "diem": 2.0, "bai": "Bài 25, Bài 9", "phut": 8.0,
                "dang": "Bài toán thực tế tam giác và phân số",
                "statement": "\\textbf{(2,0 điểm)} Một mảnh vườn hình tam giác có độ dài cạnh đáy là $48\\text{ m}$, chiều cao tương ứng bằng $\\dfrac{5}{8}$ độ dài đáy. [[br]] a) Tính diện tích mảnh vườn hình tam giác đó. [[br]] b) Người ta dành $\\dfrac{2}{5}$ diện tích mảnh vườn để trồng cây ăn quả, phần diện tích còn lại trồng rau. Tính diện tích phần đất trồng rau.",
                "dap_an": [
                    "\\textbf{a) (1,0 điểm)} [[br]] Chiều cao của mảnh vườn là: $48 \\times \\dfrac{5}{8} = 30\\text{ (m)}$ \\hfill \\textit{(0,50đ)} [[br]] Diện tích mảnh vườn hình tam giác là: $48 \\times 30 : 2 = 720\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)}",
                    "\\textbf{b) (1,0 điểm)} [[br]] Diện tích phần đất trồng rau chiếm số phần là: $1 - \\dfrac{2}{5} = \\dfrac{3}{5}$ (diện tích) \\hfill \\textit{(0,25đ)} [[br]] Diện tích phần đất trồng rau là: $720 \\times \\dfrac{3}{5} = 432\\text{ (m}^2\\text{)}$ \\hfill \\textit{(0,50đ)} [[br]] Đáp số: a) $720\\text{ m}^2$; b) $432\\text{ m}^2$. \\hfill \\textit{(0,25đ)}"
                ],
                "note": "Học sinh tính gián tiếp (tính diện tích trồng cây ăn quả rồi trừ đi) vẫn cho điểm tối đa."
            },
            {
                "label": "Bài 5.", "level": 3, "muc": "M3", "diem": 1.0, "bai": "Cấu tạo số thập phân", "phut": 4.0,
                "dang": "Lập số thập phân thỏa mãn điều kiện",
                "statement": "\\textbf{(1,0 điểm)} Cho bốn chữ số $2, 0, 4, 7$. Mỗi chữ số dùng đúng một lần. [[br]] a) Viết số thập phân lớn nhất có hai chữ số ở phần thập phân. [[br]] b) Viết số thập phân bé nhất có ba chữ số ở phần thập phân.",
                "dap_an": [
                    "\\textbf{a) (0,5đ)} Để số thập phân lớn nhất, phần nguyên phải lớn nhất: chọn hàng chục là $7$, hàng đơn vị là $4$. Phần thập phân chọn các chữ số còn lại theo thứ tự giảm dần: được số $74,20$.",
                    "\\textbf{b) (0,5đ)} Để số thập phân bé nhất, phần nguyên phải bé nhất khác $0$: chọn phần nguyên là $2$. Phần thập phân chọn các chữ số còn lại theo thứ tự tăng dần: được số $2,047$."
                ],
                "note": "Mỗi ý viết đúng và giải thích hợp lý được 0,5đ."
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
    print("Bắt đầu sinh 3 đề kiểm tra chính thức Cuối Kì 1 Toán 5 KNTT...")
    for k, D in DE.items():
        p_de = OUT / f"{D['slug_de']}.json"
        p_mt = OUT / f"{D['slug_mt']}.json"
        
        de_data = make_de_json(k, D)
        mt_data = make_mt_json(k, D)
        
        p_de.write_text(json.dumps(de_data, ensure_ascii=False, indent=2), encoding="utf-8")
        p_mt.write_text(json.dumps(mt_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Đã sinh: {p_de.name} và {p_mt.name}")

    print("Hoàn tất sinh 3 đề kiểm tra chính thức Cuối Kì 1 Toán 5 KNTT.")
