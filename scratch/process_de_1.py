# -*- coding: utf-8 -*-
"""
Script xử lý và chuẩn hóa Đề 3: gk1-x-de-kiem-tra-giua-ki-1-de-1
"""
import json

def build_de_1():
    data = {
        "xuat_xu": {
            "lop": "8",
            "ky": "GK1",
            "nam": "2023-2024",
            "truong": "MathTech (Đề kiểm tra giữa kì 1 - Đề 1)",
            "nguon": "inputs/refs/de-thi/lop-8/giua-ki-1/kntt/Đề kiểm tra giữa kì 1 - Đề 1.pdf",
            "loai_pdf": "text",
            "co_bieu_diem": True
        },
        "tang": 2,
        "da_duyet": True,
        "ghi_chu": "Đề chuẩn GK1 Toán 8 MathTech Đề 1 (2023-2024). Cấu trúc: Trắc nghiệm 12 câu (3.0đ) + Tự luận 5 bài (10 câu/ý, 7.0đ), tổng điểm chính xác 10.00 điểm kèm đáp án biểu điểm chi tiết.",
        "cau": []
    }

    # PHẦN I: TRẮC NGHIỆM (3,0 điểm) - 12 câu, mỗi câu 0.25đ
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c1",
        "vi_tri": "Câu 1",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 1. Biểu thức nào sau đây không là đơn thức?\nA. $\\sqrt{5}x$.\nB. $xy + y^3$.\nC. $-15$.\nD. $0$.",
        "dap_an": "B",
        "loi_giai": "Biểu thức $xy + y^3$ là tổng của hai đơn thức khác bậc nên là một đa thức nhiều hạng tử, không phải đơn thức.\nCác biểu thức $\\sqrt{5}x$, $-15$, $0$ đều là đơn thức.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c2",
        "vi_tri": "Câu 2",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 2. Hệ số của đơn thức $2x^2y^3 xy^3$ là\nA. $2$.\nB. $3$.\nC. $5$.\nD. $6$.",
        "dap_an": "A",
        "loi_giai": "Thu gọn đơn thức: $2x^2y^3 xy^3 = 2(x^2 \\cdot x)(y^3 \\cdot y^3) = 2x^3y^6$.\nPhần hệ số của đơn thức là $2$.\nChọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c3",
        "vi_tri": "Câu 3",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 3. Đơn thức đồng dạng với đơn thức $-4x^3y^2$ là\nA. $-7x^2y^3$.\nB. $3x^3y^2$.\nC. $2xy^3$.\nD. $-4x^2y$.",
        "dap_an": "B",
        "loi_giai": "Hai đơn thức đồng dạng là hai đơn thức có hệ số khác 0 và có cùng phần biến. Đơn thức $-4x^3y^2$ có phần biến là $x^3y^2$. Trong các phương án đưa ra, đơn thức $3x^3y^2$ có cùng phần biến $x^3y^2$.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c4",
        "vi_tri": "Câu 4",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Tính giá trị của đa thức"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 4. Giá trị của đa thức $\\frac{3}{2}xy^2(-4y) + 1$ tại $x = 1, y = -1$ là\nA. $-18$.\nB. $18$.\nC. $7$.\nD. $-7$.",
        "dap_an": "C",
        "loi_giai": "Thu gọn đa thức:\n$$\\frac{3}{2}xy^2(-4y) + 1 = -6xy^3 + 1.$$\nThay $x = 1$ và $y = -1$ vào đa thức, ta được:\n$$-6 \\cdot 1 \\cdot (-1)^3 + 1 = -6 \\cdot (-1) + 1 = 6 + 1 = 7.$$\nChọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c5",
        "vi_tri": "Câu 5",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Thu gọn đa thức", "Cộng trừ đa thức"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 5. Thu gọn đa thức $(-3x^2y - 2xy^2) + (2x^2y - 5xy^2)$ ta được\nA. $-x^2y - 7xy^2$.\nB. $x^2y + 7xy^2$.\nC. $-8x^2y$.\nD. $4xy^2$.",
        "dap_an": "A",
        "loi_giai": "Ta có:\n$$(-3x^2y - 2xy^2) + (2x^2y - 5xy^2) = (-3x^2y + 2x^2y) + (-2xy^2 - 5xy^2) = -x^2y - 7xy^2.$$\nChọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c6",
        "vi_tri": "Câu 6",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Nhân đơn thức với đa thức"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 6. Kết quả của phép nhân $-\\frac{3}{4}x(4x - 1)$ là\nA. $3x^3 - \\frac{3}{4}x$.\nB. $3x - \\frac{3}{4}x$.\nC. $-3x^2 - \\frac{3}{4}x$.\nD. $-3x^2 + \\frac{3}{4}x$.",
        "dap_an": "D",
        "loi_giai": "Ta có:\n$$-\\frac{3}{4}x(4x - 1) = -\\frac{3}{4}x \\cdot 4x - \\frac{3}{4}x \\cdot (-1) = -3x^2 + \\frac{3}{4}x.$$\nChọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c7",
        "vi_tri": "Câu 7",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Chia đa thức cho đơn thức"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 7. Đa thức $7x^3y^2z - 2x^4y^3$ chia hết cho đơn thức nào sau đây?\nA. $3x^4$.\nB. $-3x^4$.\nC. $-2x^3y$.\nD. $2xy^3$.",
        "dap_an": "C",
        "loi_giai": "Đa thức chia hết cho đơn thức khi mỗi hạng tử của đa thức đều chia hết cho đơn thức đó:\n- Hạng tử $7x^3y^2z$ chia hết cho $-2x^3y$ vì bậc của $x$ là $3 \\ge 3$, bậc của $y$ là $2 \\ge 1$.\n- Hạng tử $-2x^4y^3$ chia hết cho $-2x^3y$ vì bậc của $x$ là $4 \\ge 3$, bậc của $y$ là $3 \\ge 1$.\nDo đó đa thức chia hết cho đơn thức $-2x^3y$.\nChọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c8",
        "vi_tri": "Câu 8",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Tứ giác"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 8. Tứ giác $ABCD$ có $\\widehat{A} = 65^\\circ, \\widehat{B} = 117^\\circ, \\widehat{C} = 71^\\circ$. Số đo góc $D$ là\nA. $119^\\circ$.\nB. $107^\\circ$.\nC. $63^\\circ$.\nD. $126^\\circ$.",
        "dap_an": "B",
        "loi_giai": "Tổng bốn góc của một tứ giác bằng $360^\\circ$, do đó:\n$$\\widehat{D} = 360^\\circ - (\\widehat{A} + \\widehat{B} + \\widehat{C}) = 360^\\circ - (65^\\circ + 117^\\circ + 71^\\circ) = 360^\\circ - 253^\\circ = 107^\\circ.$$\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c9",
        "vi_tri": "Câu 9",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 9. Khẳng định nào sau đây là đúng?\nA. Hình thang có 2 cạnh đối bằng nhau là hình thang cân.\nB. Hình thang có 2 góc kề một đáy bằng nhau là hình thang cân.\nC. Hình thang cân là tứ giác có 2 cạnh bên bằng nhau.\nD. Hình thang cân là tứ giác có 2 đường chéo bằng nhau.",
        "dap_an": "B",
        "loi_giai": "Theo định nghĩa SGK, hình thang có hai góc kề một đáy bằng nhau là hình thang cân.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c10",
        "vi_tri": "Câu 10",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 10. Khẳng định nào sau đây là sai?\nA. Tứ giác có hai cặp cạnh đối song song là hình bình hành.\nB. Hình thang có hai góc kề một đáy bằng nhau là hình bình hành.\nC. Tứ giác có hai cặp cạnh đối bằng nhau là hình bình hành.\nD. Tứ giác có hai cặp góc đối bằng nhau là hình bình hành.",
        "dap_an": "B",
        "loi_giai": "Hình thang có hai góc kề một đáy bằng nhau là hình thang cân, không phải là hình bình hành. Vì vậy khẳng định B là sai.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c11",
        "vi_tri": "Câu 11",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thoi"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Câu 11. Cho tứ giác có bốn cạnh bằng nhau (được đánh dấu bằng một gạch). Chứng minh tứ giác đó là hình thoi theo dấu hiệu nào?\nA. Tứ giác có hai đường chéo vuông góc.\nB. Tứ giác có bốn cạnh bằng nhau.\nC. Hình bình hành có hai đường chéo bằng nhau.\nD. Tứ giác có hai đường chéo giao nhau tại trung điểm mỗi đường.",
        "dap_an": "B",
        "loi_giai": "Tứ giác có bốn cạnh bằng nhau là hình thoi (theo dấu hiệu nhận biết).\nChọn B.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-c12",
        "vi_tri": "Câu 12",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Toán thực tế"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Câu 12. Một mảnh vườn hình chữ nhật, ở bên trong vườn người ta đào 1 cái ao cũng là hình chữ nhật có kích thước như hình vẽ (mảnh vườn có chiều rộng $5y$, chiều dài $2x + 3y$; cái ao có chiều rộng $x$, chiều dài $x + y$), phần đất còn lại dùng để trồng rau (phần tô đậm). Biểu thức tính diện tích phần đất trồng rau là:\nA. $5y(2x + 3y)$\nB. $x(x + y)$\nC. $x(x + y) - 5y(2x + 3y)$\nD. $5y(2x + 3y) - x(x + y)$",
        "dap_an": "D",
        "loi_giai": "Diện tích phần đất trồng rau bằng diện tích mảnh vườn trừ đi diện tích cái ao:\n$$S = 5y(2x + 3y) - x(x + y).$$\nChọn D.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # PHẦN II: TỰ LUẬN (7,0 điểm)
    # Bài 1 (1,75 điểm): 1a: 0.5đ, 1b: 0.5đ, 1c: 0.75đ
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b1a",
        "vi_tri": "Bài 1.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Tính giá trị của đa thức"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 1 (1,75 điểm).",
        "de": "a) Tính giá trị biểu thức: $A = \\frac{1}{2}x^2y^5$ khi $x = -2; y = 1$.",
        "dap_an": "$A = 2$",
        "loi_giai": "Thay $x = -2$ và $y = 1$ vào biểu thức $A$, ta có:\n$$A = \\frac{1}{2} \\cdot (-2)^2 \\cdot 1^5 = \\frac{1}{2} \\cdot 4 \\cdot 1 = 2.$$\nVậy tại $x = -2; y = 1$ thì $A = 2$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b1b",
        "vi_tri": "Bài 1.b",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Cộng trừ đa thức"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài 1 (1,75 điểm).",
        "de": "b) Xác định $M$ để: $M + (5x^2 - 2xy) = 6x^2 + 9xy - y^2$.",
        "dap_an": "$M = x^2 + 11xy - y^2$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\nM + (5x^2 - 2xy) &= 6x^2 + 9xy - y^2 \\\\\nM &= (6x^2 + 9xy - y^2) - (5x^2 - 2xy) \\\\\nM &= 6x^2 + 9xy - y^2 - 5x^2 + 2xy \\\\\nM &= (6x^2 - 5x^2) + (9xy + 2xy) - y^2 \\\\\nM &= x^2 + 11xy - y^2.\n\\end{aligned}$$\nVậy $M = x^2 + 11xy - y^2$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b1c",
        "vi_tri": "Bài 1.c",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Tìm x", "Nhân đa thức với đa thức"],
        "band": "TH",
        "phut": 3.5,
        "diem_bai": 0.75,
        "de_chung": "Bài 1 (1,75 điểm).",
        "de": "c) Tìm $x$, biết: $(8x + 2)(1 - 3x) + (6x - 1)(4x - 10) = -50$.",
        "dap_an": "$x = 1$",
        "loi_giai": "Khai triển các tích ở vế trái:\n$$\\begin{aligned}\n(8x + 2)(1 - 3x) &= 8x - 24x^2 + 2 - 6x = -24x^2 + 2x + 2 \\\\\n(6x - 1)(4x - 10) &= 24x^2 - 60x - 4x + 10 = 24x^2 - 64x + 10.\n\\end{aligned}$$\nCộng lại ta được:\n$$\\begin{aligned}\n(-24x^2 + 2x + 2) + (24x^2 - 64x + 10) &= -50 \\\\\n(-24x^2 + 24x^2) + (2x - 64x) + (2 + 10) &= -50 \\\\\n-62x + 12 &= -50 \\\\\n-62x &= -62 \\\\\nx &= 1.\n\\end{aligned}$$\nVậy $x = 1$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 2 (1,25 điểm): 2a: 0.75đ, 2b: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b2a",
        "vi_tri": "Bài 2.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Rút gọn biểu thức, tính nhanh"],
        "band": "TH",
        "phut": 3.5,
        "diem_bai": 0.75,
        "de_chung": "Bài 2 (1,25 điểm).",
        "de": "a) Chứng minh giá trị của biểu thức $A$ sau đây không phụ thuộc vào giá trị của biến:\n$$A = x(2x - 3) + 2x^2(x - 2) - 2x(x^2 - x + 1) + (5x^2 - 5x) : x.$$",
        "dap_an": "$A = -5$ (không phụ thuộc vào $x$)",
        "loi_giai": "Thực hiện phép tính rút gọn biểu thức $A$ (với điều kiện $x \\ne 0$):\n$$\\begin{aligned}\nA &= x(2x - 3) + 2x^2(x - 2) - 2x(x^2 - x + 1) + (5x^2 - 5x) : x \\\\\n&= (2x^2 - 3x) + (2x^3 - 4x^2) - (2x^3 - 2x^2 + 2x) + (5x - 5) \\\\\n&= 2x^2 - 3x + 2x^3 - 4x^2 - 2x^3 + 2x^2 - 2x + 5x - 5 \\\\\n&= (2x^3 - 2x^3) + (2x^2 - 4x^2 + 2x^2) + (-3x - 2x + 5x) - 5 \\\\\n&= -5.\n\\end{aligned}$$\nVì kết quả rút gọn là hằng số $-5$ nên giá trị của biểu thức $A$ không phụ thuộc vào giá trị của biến $x$ (đpcm).",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b2b",
        "vi_tri": "Bài 2.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "VD",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 2 (1,25 điểm).",
        "de": "b) Chứng minh rằng $(2n + 3)^2 - (2n - 1)^2$ chia hết cho $8$ với mọi $n \\in \\mathbb{Z}$.",
        "dap_an": "$(2n + 3)^2 - (2n - 1)^2 = 8(2n + 1) \\ \\vdots \\ 8$",
        "loi_giai": "Áp dụng hằng đẳng thức hiệu hai bình phương $A^2 - B^2 = (A - B)(A + B)$:\n$$\\begin{aligned}\n(2n + 3)^2 - (2n - 1)^2 &= [(2n + 3) - (2n - 1)][(2n + 3) + (2n - 1)] \\\\\n&= (2n + 3 - 2n + 1)(2n + 3 + 2n - 1) \\\\\n&= 4(4n + 2) \\\\\n&= 8(2n + 1).\n\\end{aligned}$$\nVì $n \\in \\mathbb{Z}$ nên $2n + 1 \\in \\mathbb{Z}$, do đó $8(2n + 1) \\ \\vdots \\ 8$.\nVậy $(2n + 3)^2 - (2n - 1)^2$ chia hết cho $8$ với mọi $n \\in \\mathbb{Z}$ (đpcm).",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 3 (1,0 điểm): 3a: 0.5đ, 3b: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b3a",
        "vi_tri": "Bài 3.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Toán thực tế", "Nhân đa thức với đa thức"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài 3 (1,0 điểm). Một xe khách đi từ Quảng Ninh lên Hà Nội với vận tốc $(9x + 15)\\text{ km/h}$ trong thời gian $(x - 2)$ giờ.",
        "de": "a) Viết biểu thức đại số tính quãng đường Quảng Ninh – Hà Nội theo $x$.",
        "dap_an": "$S = 9x^2 - 3x - 30\\text{ (km)}$",
        "loi_giai": "Biểu thức đại số tính quãng đường Quảng Ninh – Hà Nội là:\n$$S = (9x + 15)(x - 2) = 9x^2 - 18x + 15x - 30 = 9x^2 - 3x - 30\\text{ (km)}.$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b3b",
        "vi_tri": "Bài 3.b",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Toán thực tế", "Tính giá trị của đa thức"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 3 (1,0 điểm). Một xe khách đi từ Quảng Ninh lên Hà Nội với vận tốc $(9x + 15)\\text{ km/h}$ trong thời gian $(x - 2)$ giờ.",
        "de": "b) Tính quãng đường Quảng Ninh – Hà Nội khi $x = 5$.",
        "dap_an": "$180\\text{ km}$",
        "loi_giai": "Thay $x = 5$ vào biểu thức tính quãng đường, ta được:\n$$S = 9 \\cdot 5^2 - 3 \\cdot 5 - 30 = 9 \\cdot 25 - 15 - 30 = 225 - 45 = 180\\text{ (km)}.$$\nVậy quãng đường Quảng Ninh – Hà Nội khi $x = 5$ là $180\\text{ km}$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 4 (2,5 điểm): 4a: 1.0đ, 4b: 1.0đ, 4c: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b4a",
        "vi_tri": "Bài 4.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HP \\perp AB$ ($P \\in AB$), $HQ \\perp AC$ ($Q \\in AC$). Gọi $K$ là trung điểm của $HC$; $O$ là giao điểm của $AH$ và $PQ$.",
        "de": "a) Tứ giác $AQHP$ là hình gì? Vì sao?",
        "dap_an": "$AQHP$ là hình chữ nhật",
        "loi_giai": "Xét tứ giác $AQHP$ có:\n- $\\widehat{PAQ} = 90^\\circ$ (vì tam giác $ABC$ vuông tại $A$);\n- $\\widehat{APH} = 90^\\circ$ (vì $HP \\perp AB$ tại $P$);\n- $\\widehat{AQH} = 90^\\circ$ (vì $HQ \\perp AC$ tại $Q$).\nTứ giác $AQHP$ có ba góc vuông nên là hình chữ nhật.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b4b",
        "vi_tri": "Bài 4.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật", "Tam giác"],
        "band": "TH",
        "phut": 4.5,
        "diem_bai": 1.0,
        "de_chung": "Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HP \\perp AB$ ($P \\in AB$), $HQ \\perp AC$ ($Q \\in AC$). Gọi $K$ là trung điểm của $HC$; $O$ là giao điểm của $AH$ và $PQ$.",
        "de": "b) Chứng minh $\\Delta KQH$ cân và $OK$ là đường trung trực của $HQ$.",
        "dap_an": "$\\Delta KQH$ cân tại $K$ và $OK$ là đường trung trực của $HQ$",
        "loi_giai": "1) Chứng minh tam giác $KQH$ cân:\n- Xét tam giác $HQC$ vuông tại $Q$, có $QK$ là đường trung tuyến ứng với cạnh huyền $HC$ (do $K$ là trung điểm $HC$).\nTheo tính chất đường trung tuyến trong tam giác vuông, ta có:\n$$QK = KH = KC = \\frac{1}{2}HC.$$\nDo $QK = KH$ nên tam giác $KQH$ cân tại $K$.\n\n2) Chứng minh $OK$ là đường trung trực của $HQ$:\n- Vì $AQHP$ là hình chữ nhật (theo câu a) và $O$ là giao điểm hai đường chéo $AH, PQ$ nên $O$ là trung điểm của mỗi đường và hai đường chéo bằng nhau. Do đó:\n$$OA = OH = OP = OQ.$$\nSuy ra $OH = OQ$, tức là điểm $O$ cách đều hai đầu mút $H$ và $Q$.\n- Lại có $KH = KQ$ (do tam giác $KQH$ cân tại $K$), tức là điểm $K$ cũng cách đều hai đầu mút $H$ và $Q$.\nDo đó, đoạn thẳng $OK$ chính là đường trung trực của đoạn thẳng $HQ$ (đpcm).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b4c",
        "vi_tri": "Bài 4.c",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "VD",
        "phut": 4.0,
        "diem_bai": 0.5,
        "de_chung": "Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HP \\perp AB$ ($P \\in AB$), $HQ \\perp AC$ ($Q \\in AC$). Gọi $K$ là trung điểm của $HC$; $O$ là giao điểm của $AH$ và $PQ$.",
        "de": "c) Tìm điều kiện của tam giác $ABC$ để tứ giác $AOKC$ là hình thang cân.",
        "dap_an": "$\\Delta ABC$ vuông cân tại $A$",
        "loi_giai": "- Gọi $I$ là giao điểm của $HQ$ và $OK$.\nTheo câu b, $OK$ là đường trung trực của $HQ$ nên $OK \\perp HQ$ tại $I$.\nLại có $AC \\perp HQ$ tại $Q$.\nSuy ra $OK \\parallel AC$ (cùng vuông góc với $HQ$).\nDo đó tứ giác $AOKC$ là hình thang có hai đáy là $OK$ và $AC$.\n- Để hình thang $AOKC$ là hình thang cân thì hai góc kề đáy $AC$ phải bằng nhau:\n$$\\widehat{OAC} = \\widehat{KCA}.$$\n- Mặt khác, trong tam giác vuông $AHC$ vuông tại $H$, ta có $\\widehat{HAC} + \\widehat{KCA} = 90^\\circ$.\nVì $O$ nằm trên $AH$ nên góc $\\widehat{OAC}$ chính là góc $\\widehat{HAC}$.\nDo đó:\n$$\\widehat{OAC} = \\widehat{KCA} \\iff \\widehat{HAC} = \\widehat{KCA} = 45^\\circ.$$\nKhi $\\widehat{KCA} = \\widehat{C} = 45^\\circ$, tam giác $ABC$ vuông tại $A$ có $\\widehat{C} = 45^\\circ$ nên tam giác $ABC$ là tam giác vuông cân tại $A$.\nVậy điều kiện để tứ giác $AOKC$ là hình thang cân là tam giác $ABC$ vuông cân tại $A$.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài 5 (0,5 điểm)
    data["cau"].append({
        "id": "l8-gk1-x-de-kiem-tra-giua-ki-1-de-1-b5",
        "vi_tri": "Bài 5",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "VD",
        "phut": 4.0,
        "diem_bai": 0.5,
        "de": "Bài 5 (0,5 điểm). Cho $a^2 + b^2 + c^2 = ab + bc + ca$ và $a + b + c = 2022$. Tính $a, b, c$.",
        "dap_an": "$a = b = c = 674$",
        "loi_giai": "Từ đẳng thức đã cho:\n$$a^2 + b^2 + c^2 = ab + bc + ca.$$\nNhân cả hai vế với $2$, ta được:\n$$2a^2 + 2b^2 + 2c^2 = 2ab + 2bc + 2ca.$$\nChuyển vế và nhóm thành các bình phương:\n$$\\begin{aligned}\n(a^2 - 2ab + b^2) + (b^2 - 2bc + c^2) + (c^2 - 2ca + a^2) &= 0 \\\\\n(a - b)^2 + (b - c)^2 + (c - a)^2 &= 0.\n\\end{aligned}$$\nVì $(a - b)^2 \\ge 0$, $(b - c)^2 \\ge 0$, $(c - a)^2 \\ge 0$ với mọi $a, b, c$, nên tổng của chúng bằng $0$ khi và chỉ khi:\n$$\\begin{cases}\na - b = 0 \\\\\nb - c = 0 \\\\\nc - a = 0\n\\end{cases}\n\\iff a = b = c.$$\nMặt khác, theo bài ra $a + b + c = 2022$, suy ra:\n$$3a = 2022 \\iff a = b = c = \\frac{2022}{3} = 674.$$\nVậy $a = b = c = 674$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    return data

if __name__ == "__main__":
    d = build_de_1()
    with open("inputs/refs/de-thi/lop-8/exams/gk1-x-de-kiem-tra-giua-ki-1-de-1.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("Updated gk1-x-de-kiem-tra-giua-ki-1-de-1.json successfully! Cau count:", len(d["cau"]))
