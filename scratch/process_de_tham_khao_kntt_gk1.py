# -*- coding: utf-8 -*-
"""
Script xử lý và chuẩn hóa Đề 5: gk1-x-de-tham-khao-kntt-de-gk1
(Đề kiểm tra giữa học kì 1 - Đề số 4 KNTT 2023-2024)
"""
import json

def build_de_gk1_so_4():
    data = {
        "xuat_xu": {
            "lop": "8",
            "ky": "GK1",
            "nam": "2023-2024",
            "truong": "KNTT - Đề tham khảo số 4",
            "nguon": "inputs/refs/de-thi/lop-8/giua-ki-1/kntt/(Đề tham khảo) KNTT - Đề GK1.pdf",
            "loai_pdf": "text",
            "co_bieu_diem": True
        },
        "tang": 2,
        "da_duyet": True,
        "ghi_chu": "Đề chuẩn GK1 Toán 8 KNTT Đề số 4 (2023-2024). Cấu trúc: Trắc nghiệm 8 câu (2.0đ) + Tự luận 5 bài (11 câu/ý, 8.0đ), tổng điểm chính xác 10.00 điểm kèm đáp án biểu điểm chi tiết.",
        "cau": []
    }

    # I. PHẦN TRẮC NGHIỆM (2,0 ĐIỂM) - 8 câu, mỗi câu 0.25đ
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c1",
        "vi_tri": "Câu 1",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Chia đa thức cho đơn thức"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 1. Kết quả phép tính $5x^4 : x^2$ bằng\nA. $5x^3$\nB. $x^2$\nC. $5x^2$\nD. $5x$",
        "dap_an": "C",
        "loi_giai": "Ta có: $5x^4 : x^2 = 5x^{4 - 2} = 5x^2$.\nChọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c2",
        "vi_tri": "Câu 2",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 2. Tứ giác có hai cạnh đối song song và bằng nhau là:\nA. Hình chữ nhật\nB. Hình bình hành\nC. Hình thoi\nD. Hình vuông",
        "dap_an": "B",
        "loi_giai": "Theo dấu hiệu nhận biết, tứ giác có hai cạnh đối song song và bằng nhau là hình bình hành.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c3",
        "vi_tri": "Câu 3",
        "loai": "TN",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 3. Phân tích $8x^3 + 36x^2y + 54xy^2 + 27y^3$ thành hằng đẳng thức ta được:\nA. $(2x + 3y)^2$\nB. $(3x + 2y)^3$\nC. $(2x - 3y)(4x^2 + 6xy + 9y^2)$\nD. $(2x + 3y)^3$",
        "dap_an": "D",
        "loi_giai": "Ta có:\n$$8x^3 + 36x^2y + 54xy^2 + 27y^3 = (2x)^3 + 3 \\cdot (2x)^2 \\cdot (3y) + 3 \\cdot (2x) \\cdot (3y)^2 + (3y)^3 = (2x + 3y)^3.$$\nChọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c4",
        "vi_tri": "Câu 4",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 4. Chọn khẳng định sai trong các khẳng định sau:\nA. Hình bình hành có hai cạnh kề bằng nhau là hình thoi;\nB. Hình thang có hai góc vuông là hình chữ nhật;\nC. Hình bình hành có một đường chéo là đường phân giác của một góc là hình thoi;\nD. Hình chữ nhật có hai đường chéo vuông góc với nhau là hình vuông.",
        "dap_an": "B",
        "loi_giai": "Hình thang có hai góc kề một cạnh bên vuông góc là hình thang vuông, không nhất thiết là hình chữ nhật (hình chữ nhật là tứ giác có 4 góc vuông). Do đó khẳng định B là sai.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c5",
        "vi_tri": "Câu 5",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 5. Biểu thức nào dưới đây không là đơn thức\nA. $1$\nB. $\\frac{3}{8}x$\nC. $2x$\nD. $x + 1$",
        "dap_an": "D",
        "loi_giai": "Biểu thức $x + 1$ là tổng của hai đơn thức khác bậc, do đó nó là một đa thức nhiều hơn một hạng tử, không phải đơn thức.\nChọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c6",
        "vi_tri": "Câu 6",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 6. Cho hình bình hành $ABCD$ có $\\widehat{D} - \\widehat{C} = 30^\\circ$. Khi đó số đo góc $A$ bằng:\nA. $\\widehat{A} = 75^\\circ$\nB. $\\widehat{A} = 70^\\circ$\nC. $\\widehat{A} = 55^\\circ$\nD. $\\widehat{A} = 80^\\circ$",
        "dap_an": "A",
        "loi_giai": "Trong hình bình hành $ABCD$, hai góc kề một cạnh bù nhau nên $\\widehat{D} + \\widehat{C} = 180^\\circ$.\nKết hợp với $\\widehat{D} - \\widehat{C} = 30^\\circ$, ta có:\n$$\\widehat{C} = \\frac{180^\\circ - 30^\\circ}{2} = 75^\\circ.$$\nVì hai góc đối bằng nhau nên $\\widehat{A} = \\widehat{C} = 75^\\circ$.\nChọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c7",
        "vi_tri": "Câu 7",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thoi"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 7. Hình nào dưới đây vừa có tâm đối xứng vừa có trục đối xứng:\nA. Hình bình hành.\nB. Hình thoi.\nC. Hình thang vuông.\nD. Hình thang cân.",
        "dap_an": "B",
        "loi_giai": "Hình thoi có tâm đối xứng là giao điểm của hai đường chéo và có hai trục đối xứng là hai đường thẳng chứa hai đường chéo.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-c8",
        "vi_tri": "Câu 8",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 8. Cho hình thang cân $ABCD$ ($AB \\parallel CD$). Khẳng định nào dưới đây là sai?\nA. $AC = BD$\nB. $\\widehat{D} = \\widehat{C}$\nC. $AB = CD$\nD. $AD = BC$",
        "dap_an": "C",
        "loi_giai": "Trong hình thang cân $ABCD$ ($AB \\parallel CD$), hai đường chéo bằng nhau ($AC = BD$), hai góc kề một đáy bằng nhau ($\\widehat{D} = \\widehat{C}$), hai cạnh bên bằng nhau ($AD = BC$). Hai cạnh đáy $AB$ và $CD$ không nhất thiết bằng nhau. Do đó khẳng định $AB = CD$ là sai.\nChọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # II. PHẦN TỰ LUẬN (8,0 ĐIỂM)
    # Bài 1 (1,5 điểm): 1a: 0.5đ, 1b: 0.5đ, 1c: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b1a",
        "vi_tri": "Bài 1.a",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Những hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 1 (1,5 điểm). Rút gọn biểu thức:",
        "de": "a) $(x - 3)(x + 3) - (x + 2)^2$.",
        "dap_an": "$-4x - 13$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(x - 3)(x + 3) - (x + 2)^2 &= (x^2 - 9) - (x^2 + 4x + 4) \\\\\n&= x^2 - 9 - x^2 - 4x - 4 \\\\\n&= -4x - 13.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b1b",
        "vi_tri": "Bài 1.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Những hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 1 (1,5 điểm). Rút gọn biểu thức:",
        "de": "b) $(x - 2)(x^2 + 2x + 4) - x(x^2 + 1)$.",
        "dap_an": "$-x - 8$",
        "loi_giai": "Áp dụng hằng đẳng thức $(x - 2)(x^2 + 2x + 4) = x^3 - 8$:\n$$\\begin{aligned}\n(x - 2)(x^2 + 2x + 4) - x(x^2 + 1) &= (x^3 - 8) - (x^3 + x) \\\\\n&= x^3 - 8 - x^3 - x \\\\\n&= -x - 8.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b1c",
        "vi_tri": "Bài 1.c",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Chia đa thức cho đơn thức"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài 1 (1,5 điểm). Rút gọn biểu thức:",
        "de": "c) $(3x^4y^2 + 6x^2y^3 - 12x^2y^2) : 3x^2y^2$.",
        "dap_an": "$x^2 + 2y - 4$",
        "loi_giai": "Chia từng hạng tử của đa thức cho đơn thức $3x^2y^2$:\n$$\\begin{aligned}\n(3x^4y^2 + 6x^2y^3 - 12x^2y^2) : 3x^2y^2 &= (3x^4y^2 : 3x^2y^2) + (6x^2y^3 : 3x^2y^2) - (12x^2y^2 : 3x^2y^2) \\\\\n&= x^2 + 2y - 4.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 2 (1,5 điểm): 2a: 0.5đ, 2b: 0.5đ, 2c: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b2a",
        "vi_tri": "Bài 2.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Phân tích đa thức thành nhân tử", "Đặt nhân tử chung"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 2 (1,5 điểm). Phân tích các đa thức sau thành nhân tử:",
        "de": "a) $(x + 3)(x - 2) - (3 + x)(2 - 4x)$.",
        "dap_an": "$(x + 3)(5x - 4)$",
        "loi_giai": "Nhận thấy $3 + x = x + 3$, ta đặt nhân tử chung $(x + 3)$:\n$$\\begin{aligned}\n(x + 3)(x - 2) - (3 + x)(2 - 4x) &= (x + 3)[(x - 2) - (2 - 4x)] \\\\\n&= (x + 3)(x - 2 - 2 + 4x) \\\\\n&= (x + 3)(5x - 4).\n\\end{aligned}$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b2b",
        "vi_tri": "Bài 2.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Phân tích đa thức thành nhân tử", "Hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài 2 (1,5 điểm). Phân tích các đa thức sau thành nhân tử:",
        "de": "b) $x^2 - 10x + 25 - 4y^2$.",
        "dap_an": "$(x - 5 - 2y)(x - 5 + 2y)$",
        "loi_giai": "Nhóm ba hạng tử đầu thành bình phương của một hiệu:\n$$\\begin{aligned}\nx^2 - 10x + 25 - 4y^2 &= (x^2 - 10x + 25) - 4y^2 \\\\\n&= (x - 5)^2 - (2y)^2 \\\\\n&= (x - 5 - 2y)(x - 5 + 2y).\n\\end{aligned}$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b2c",
        "vi_tri": "Bài 2.c",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Phân tích đa thức thành nhân tử"],
        "band": "VD",
        "phut": 3.5,
        "diem_bai": 0.5,
        "de_chung": "Bài 2 (1,5 điểm). Phân tích các đa thức sau thành nhân tử:",
        "de": "c) $x^6y - x^4y^3 - x^3y^4 + xy^6$.",
        "dap_an": "$xy(x - y)^2(x + y)(x^2 + xy + y^2)$",
        "loi_giai": "Đặt nhân tử chung $xy$ ra ngoài, rồi nhóm các hạng tử thích hợp:\n$$\\begin{aligned}\nx^6y - x^4y^3 - x^3y^4 + xy^6 &= xy(x^5 - x^3y^2 - x^2y^3 + y^5) \\\\\n&= xy[x^3(x^2 - y^2) - y^3(x^2 - y^2)] \\\\\n&= xy(x^2 - y^2)(x^3 - y^3) \\\\\n&= xy(x - y)(x + y)(x - y)(x^2 + xy + y^2) \\\\\n&= xy(x - y)^2(x + y)(x^2 + xy + y^2).\n\\end{aligned}$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 3 (1,0 điểm): 3a: 0.5đ, 3b: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b3a",
        "vi_tri": "Bài 3.a",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tìm x", "Phân tích đa thức thành nhân tử"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 3 (1,0 điểm). Tìm $x$, biết:",
        "de": "a) $x^2(x - 2) - 9(x - 2) = 0$.",
        "dap_an": "$x \\in \\{-3; 2; 3\\}$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\nx^2(x - 2) - 9(x - 2) &= 0 \\\\\n(x - 2)(x^2 - 9) &= 0 \\\\\n(x - 2)(x - 3)(x + 3) &= 0 \\\\\n\\left[\\begin{aligned}\nx - 2 &= 0 \\\\\nx - 3 &= 0 \\\\\nx + 3 &= 0\n\\end{aligned}\\right. &\\iff \\left[\\begin{aligned}\nx &= 2 \\\\\nx &= 3 \\\\\nx &= -3.\n\\end{aligned}\\right.\n\\end{aligned}$$\nVậy $x \\in \\{-3; 2; 3\\}$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b3b",
        "vi_tri": "Bài 3.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tìm x", "Hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 3 (1,0 điểm). Tìm $x$, biết:",
        "de": "b) $3x^2(x + 4) - x^2(3x + 11) + 4 + 4x = 0$.",
        "dap_an": "$x = -2$",
        "loi_giai": "Khai triển và thu gọn vế trái:\n$$\\begin{aligned}\n3x^2(x + 4) - x^2(3x + 11) + 4 + 4x &= 0 \\\\\n3x^3 + 12x^2 - 3x^3 - 11x^2 + 4x + 4 &= 0 \\\\\nx^2 + 4x + 4 &= 0 \\\\\n(x + 2)^2 &= 0 \\\\\nx + 2 &= 0 \\\\\nx &= -2.\n\\end{aligned}$$\nVậy $x = -2$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 4 (3,5 điểm): 4a: 1.0đ, 4b: 1.0đ, 4c: 1.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b4a",
        "vi_tri": "Bài 4.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Gọi $M, N$ lần lượt là trung điểm của $BC$ và $AC$. Lấy điểm $I$ đối xứng với điểm $N$ qua $M$.",
        "de": "a) Chứng minh tứ giác $BICN$ là hình bình hành.",
        "dap_an": "$BICN$ là hình bình hành",
        "loi_giai": "- Vì điểm $I$ đối xứng với điểm $N$ qua $M$ nên $M$ là trung điểm của đoạn thẳng $NI$.\n- Xét tứ giác $BICN$, ta có:\n  + $M$ là trung điểm của đường chéo $BC$ (theo giả thiết);\n  + $M$ là trung điểm của đường chéo $NI$.\nTứ giác $BICN$ có hai đường chéo $BC$ và $NI$ cắt nhau tại trung điểm $M$ của mỗi đường nên $BICN$ là hình bình hành (theo dấu hiệu nhận biết).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b4b",
        "vi_tri": "Bài 4.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Gọi $M, N$ lần lượt là trung điểm của $BC$ và $AC$. Lấy điểm $I$ đối xứng với điểm $N$ qua $M$.",
        "de": "b) Tứ giác $ABIN$ là hình gì? Vì sao?",
        "dap_an": "$ABIN$ là hình chữ nhật",
        "loi_giai": "- Do $BICN$ là hình bình hành (theo câu a) nên $IB \\parallel CN$ và $IB = CN$.\n- Mặt khác, $N$ là trung điểm của $AC$ nên $NA = NC = \\frac{1}{2}AC$.\nSuy ra $IB \\parallel NA$ (vì $A, N, C$ thẳng hàng) và $IB = NA$.\n- Tứ giác $ABIN$ có một cặp cạnh đối song song và bằng nhau ($IB \\parallel NA$ và $IB = NA$) nên $ABIN$ là hình bình hành.\n- Lại có $\\widehat{NAB} = \\widehat{CAB} = 90^\\circ$ (vì $\\Delta ABC$ vuông tại $A$).\nHình bình hành $ABIN$ có một góc vuông nên $ABIN$ là hình chữ nhật.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b4c",
        "vi_tri": "Bài 4.c",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật", "Tam giác"],
        "band": "VD",
        "phut": 5.0,
        "diem_bai": 1.5,
        "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Gọi $M, N$ lần lượt là trung điểm của $BC$ và $AC$. Lấy điểm $I$ đối xứng với điểm $N$ qua $M$.",
        "de": "c) Qua $C$ vẽ đường thẳng song song với $IN$ cắt tia $BI$ tại $F$. $NF$ cắt $BC$ tại $G$. Chứng minh $IC = 3GN$.",
        "dap_an": "$IC = 3GN$",
        "loi_giai": "1) Chứng minh $INCF$ là hình chữ nhật:\n- Vì $ABIN$ là hình chữ nhật nên $AB \\parallel NI$.\n- Theo giả thiết $CF \\parallel IN$, do đó $CF \\parallel AB$.\n- Xét tứ giác $ABFC$ có $AB \\parallel CF$ và $AC \\parallel BF$ (do $AC \\parallel BI$). Suy ra $ABFC$ là hình bình hành.\n  Mà $\\widehat{BAC} = 90^\\circ$ nên $ABFC$ là hình chữ nhật.\n- Trong hình chữ nhật $ABFC$, hai đường chéo $BC$ và $AF$ cắt nhau tại trung điểm của mỗi đường.\n  Mà $M$ là trung điểm của $BC$, suy ra $M$ cũng là trung điểm của $AF$.\n- Tứ giác $INCF$ có $IN \\parallel CF$ và $IF \\parallel NC$ nên là hình bình hành. Lại có $\\widehat{INC} = 90^\\circ$ nên $INCF$ là hình chữ nhật.\n  Suy ra hai đường chéo bằng nhau: $NF = IC$.\n\n2) Chứng minh $IC = 3GN$:\n- Xét tam giác $ACF$, ta có:\n  + $N$ là trung điểm của $AC$ nên $FN$ là đường trung tuyến;\n  + $M$ là trung điểm của $AF$ nên $CM$ là đường trung tuyến.\n- Hai đường trung tuyến $FN$ và $CM$ cắt nhau tại $G$ (vì $G = NF \\cap BC$ và $M \\in BC$).\n  Suy ra $G$ là trọng tâm của tam giác $ACF$.\n- Theo tính chất trọng tâm, ta có:\n$$GN = \\frac{1}{3}NF.$$\n- Thay $NF = IC$ vào, ta được:\n$$GN = \\frac{1}{3}IC \\iff IC = 3GN\\text{ (đpcm)}.$$",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 5 (0,5 điểm)
    data["cau"].append({
        "id": "l8-gk1-x-de-tham-khao-kntt-de-gk1-b5",
        "vi_tri": "Bài 5",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "VDC",
        "phut": 5.0,
        "diem_bai": 0.5,
        "de": "Bài 5 (0,5 điểm). Cho các số $a, b$ dương thoả mãn $a^3 + b^3 = 3ab - 1$. Chứng minh rằng $a^{2022} + b^{2023} = 2$.",
        "dap_an": "$a = b = 1 \\implies a^{2022} + b^{2023} = 2$",
        "loi_giai": "Biến đổi giả thiết:\n$$\\begin{aligned}\na^3 + b^3 &= 3ab - 1 \\\\\na^3 + b^3 + 1 - 3ab &= 0 \\\\\n(a + b)^3 - 3ab(a + b) + 1 - 3ab &= 0 \\\\\n[(a + b)^3 + 1] - 3ab(a + b + 1) &= 0 \\\\\n(a + b + 1)[(a + b)^2 - (a + b) + 1] - 3ab(a + b + 1) &= 0 \\\\\n(a + b + 1)(a^2 + 2ab + b^2 - a - b + 1 - 3ab) &= 0 \\\\\n(a + b + 1)(a^2 + b^2 - ab - a - b + 1) &= 0.\n\\end{aligned}$$\nVì $a > 0$ và $b > 0$ nên $a + b + 1 > 0$. Do đó:\n$$a^2 + b^2 - ab - a - b + 1 = 0.$$\nNhân cả hai vế với $2$:\n$$\\begin{aligned}\n2a^2 + 2b^2 - 2ab - 2a - 2b + 2 &= 0 \\\\\n(a^2 - 2ab + b^2) + (a^2 - 2a + 1) + (b^2 - 2b + 1) &= 0 \\\\\n(a - b)^2 + (a - 1)^2 + (b - 1)^2 &= 0.\n\\end{aligned}$$\nVì $(a - b)^2 \\ge 0$, $(a - 1)^2 \\ge 0$, $(b - 1)^2 \\ge 0$ với mọi $a, b$, nên:\n$$\\begin{cases}\na - b = 0 \\\\\na - 1 = 0 \\\\\nb - 1 = 0\n\\end{cases}\n\\iff a = b = 1.$$\nThay $a = 1, b = 1$ vào biểu thức, ta được:\n$$a^{2022} + b^{2023} = 1^{2022} + 1^{2023} = 1 + 1 = 2\\text{ (đpcm)}.$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    return data

if __name__ == "__main__":
    d = build_de_gk1_so_4()
    with open("inputs/refs/de-thi/lop-8/exams/gk1-x-de-tham-khao-kntt-de-gk1.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("Updated gk1-x-de-tham-khao-kntt-de-gk1.json successfully! Cau count:", len(d["cau"]))
