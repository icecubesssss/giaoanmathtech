# -*- coding: utf-8 -*-
import json

data = {
  "xuat_xu": "Đề giữa kì 1 Toán 8 năm học 2024 – 2025 trường THCS Phúc Lợi – Long Biên – Hà Nội (Đề số 1)",
  "tang": "lop-8",
  "da_duyet": True,
  "ghi_chu": "Đã soát toàn diện theo ảnh đề gốc (2 trang), sửa triệt để lỗi OCR, chuẩn hóa công thức LaTeX và lời giải chi tiết.",
  "cau": [
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn1",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương I: Đa thức",
      "de": "Trong những cặp đơn thức dưới đây, cặp đơn thức đồng dạng là:",
      "options": [
        "A. $7x^3y$ và $\\dfrac{1}{15}xy^3$",
        "B. $-\\dfrac{1}{8}(xy)^2x^2$ và $32x^2y^3$",
        "C. $5x^2y^2$ và $-2x^2y^2$",
        "D. $4x^2y$ và $2xy^2$"
      ],
      "dap_an_kiem": "C",
      "loi_giai": "Hai đơn thức $5x^2y^2$ và $-2x^2y^2$ có hệ số khác $0$ và có cùng phần biến $x^2y^2$ nên là hai đơn thức đồng dạng.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn2",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương I: Đa thức",
      "de": "Hệ số và phần biến của đơn thức $-3x^2yz^3$ lần lượt là:",
      "options": [
        "A. $3x^2$ và $yz^3$",
        "B. $-3x^2y$ và $z^3$",
        "C. $-3$ và $x^2yz^3$",
        "D. $x^2yz^3$ và $3$"
      ],
      "dap_an_kiem": "C",
      "loi_giai": "Đơn thức $-3x^2yz^3$ có hệ số là $-3$ và phần biến là $x^2yz^3$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn3",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Hằng đẳng thức bình phương của một tổng là:",
      "options": [
        "A. $(A + B)^2 = A^2 - 2AB + B^2$",
        "B. $(A + B)^2 = A^2 + AB + B^2$",
        "C. $(A + B)^2 = A^2 + 2AB + B^2$",
        "D. $(A + B)^2 = A^2 + B^2$"
      ],
      "dap_an_kiem": "C",
      "loi_giai": "Hằng đẳng thức bình phương của một tổng: $(A + B)^2 = A^2 + 2AB + B^2$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn4",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Điền vào chỗ trống sau: $x^2 - \\boxed{\\quad} = (x - 4)(x + 4)$.",
      "options": [
        "A. $2$",
        "B. $4$",
        "C. $6$",
        "D. $16$"
      ],
      "dap_an_kiem": "D",
      "loi_giai": "Áp dụng hằng đẳng thức hiệu hai bình phương: $(x - 4)(x + 4) = x^2 - 4^2 = x^2 - 16$. Vậy số cần điền là $16$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn5",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương IV: Một số hình khối trong thực tiễn",
      "de": "Cho hình chóp tam giác đều $A.BCD$ có $M$ là trung điểm của cạnh đáy $BC$. Đoạn thẳng nào là trung đoạn của hình chóp?",
      "options": [
        "A. $AP$",
        "B. $AB$",
        "C. $AM$",
        "D. $BN$"
      ],
      "dap_an_kiem": "C",
      "loi_giai": "Trung đoạn của hình chóp đều là đường cao của mặt bên xuất phát từ đỉnh, tức đoạn thẳng nối đỉnh $A$ với trung điểm $M$ của cạnh đáy $BC$. Do đó $AM$ là trung đoạn.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn6",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương IV: Một số hình khối trong thực tiễn",
      "de": "Trong các hình sau, hình nào là hình chóp tứ giác?\n- Hình 1: Hình lăng trụ đứng lục giác\n- Hình 2: Hình chóp ngũ giác\n- Hình 3: Hình chóp tam giác\n- Hình 4: Hình chóp tứ giác",
      "options": [
        "A. Hình 1",
        "B. Hình 2",
        "C. Hình 3",
        "D. Hình 4"
      ],
      "dap_an_kiem": "D",
      "loi_giai": "Hình 4 có đáy là một tứ giác và 4 mặt bên là các tam giác có chung đỉnh, nên là hình chóp tứ giác.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn7",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương III: Tứ giác",
      "de": "Theo định lí Pythagore: Trong tam giác vuông, bình phương cạnh huyền bằng:",
      "options": [
        "A. Tổng bình phương hai cạnh góc vuông",
        "B. Tổng hai cạnh góc vuông",
        "C. Hiệu bình phương hai cạnh góc vuông",
        "D. Hiệu hai cạnh góc vuông"
      ],
      "dap_an_kiem": "A",
      "loi_giai": "Định lý Pythagore: Trong một tam giác vuông, bình phương cạnh huyền bằng tổng bình phương của hai cạnh góc vuông.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tn8",
      "loai": "TN",
      "band": "NB",
      "chuong": "Chương III: Tứ giác",
      "de": "Tam giác nào là tam giác vuông trong các tam giác có độ dài ba cạnh như sau:",
      "options": [
        "A. $5\\text{ cm}; 5\\text{ cm}; 7\\text{ cm}$",
        "B. $3\\text{ cm}; 4\\text{ cm}; 5\\text{ cm}$",
        "C. $6\\text{ cm}; 8\\text{ cm}; 9\\text{ cm}$",
        "D. $2\\text{ dm}; 3\\text{ dm}; 4\\text{ dm}$"
      ],
      "dap_an_kiem": "B",
      "loi_giai": "Ta có $3^2 + 4^2 = 9 + 16 = 25 = 5^2$. Theo định lý Pythagore đảo, tam giác có ba cạnh $3\\text{ cm}; 4\\text{ cm}; 5\\text{ cm}$ là tam giác vuông.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.25
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl1-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 1. (1,5 điểm) Nhà bác Minh có mảnh đất có dạng hình chữ nhật với chiều dài là $3y\\text{ (m)}$ và chiều rộng là $2x\\text{ (m)}$, ($x, y > 0$). Bác Minh đã chia mảnh đất thành hai phần, phần hình vuông để trồng hoa và phần còn lại để lát gạch như hình vẽ (phần trắng).\na) Viết đa thức $A$ biểu thị diện tích mảnh đất nhà bác Minh và viết đa thức $B$ biểu thị diện tích phần trồng hoa.",
      "dap_an_kiem": "A = 6xy, B = 4x^2",
      "loi_giai": "- Diện tích mảnh đất hình chữ nhật nhà bác Minh là:\n$A = 2x \\cdot 3y = 6xy\\text{ (m}^2\\text{)}$.\n- Phần hình vuông trồng hoa có cạnh bằng chiều rộng mảnh đất là $2x\\text{ (m)}$, nên diện tích là:\n$B = (2x)^2 = 4x^2\\text{ (m}^2\\text{)}$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 1.0
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl1-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 1. b) Tính diện tích phần lát gạch biết $x = 12, y = 21$.",
      "dap_an_kiem": "936",
      "loi_giai": "Diện tích phần đất lát gạch là:\n$S = A - B = 6xy - 4x^2$.\nThay $x = 12$ và $y = 21$ vào biểu thức, ta được:\n$S = 6 \\cdot 12 \\cdot 21 - 4 \\cdot 12^2 = 1512 - 4 \\cdot 144 = 1512 - 576 = 936\\text{ (m}^2\\text{)}$.\nVậy diện tích phần lát gạch là $936\\text{ m}^2$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl2-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. (1,5 điểm) Thu gọn các biểu thức sau:\na) $A = x(2 - x) + x^2$.",
      "dap_an_kiem": "2x",
      "loi_giai": "Ta có:\n$A = 2x - x^2 + x^2 = 2x$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl2-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 2. Thu gọn các biểu thức sau:\nb) $B = (x + 2)(x - 2) - (x^2 - 14)$.",
      "dap_an_kiem": "10",
      "loi_giai": "Ta có:\n$B = (x^2 - 4) - (x^2 - 14) = x^2 - 4 - x^2 + 14 = 10$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl2-c",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. Thu gọn các biểu thức sau:\nc) $C = \\left(2x^2y - \\dfrac{4}{3}xy^3 + \\dfrac{3}{2}x^3y^3\\right) : \\left(\\dfrac{2}{3}xy\\right) - x^2y^2$.",
      "dap_an_kiem": "3x - 2y^2 + 5/4 x^2y^2",
      "loi_giai": "Ta có:\n$\\left(2x^2y - \\dfrac{4}{3}xy^3 + \\dfrac{3}{2}x^3y^3\\right) : \\left(\\dfrac{2}{3}xy\\right)$\n$= \\left(2x^2y : \\dfrac{2}{3}xy\\right) - \\left(\\dfrac{4}{3}xy^3 : \\dfrac{2}{3}xy\\right) + \\left(\\dfrac{3}{2}x^3y^3 : \\dfrac{2}{3}xy\\right)$\n$= 3x - 2y^2 + \\dfrac{9}{4}x^2y^2$.\nDo đó:\n$C = 3x - 2y^2 + \\dfrac{9}{4}x^2y^2 - x^2y^2 = 3x - 2y^2 + \\dfrac{5}{4}x^2y^2$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl3-a",
      "loai": "TL",
      "band": "NB",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 3. (1,5 điểm) Phân tích mỗi đa thức sau thành nhân tử:\na) $x^3 + 3x^2 + 3x + 1$.",
      "dap_an_kiem": "(x + 1)^3",
      "loi_giai": "Ta có: $x^3 + 3x^2 + 3x + 1 = x^3 + 3 \\cdot x^2 \\cdot 1 + 3 \\cdot x \\cdot 1^2 + 1^3 = (x + 1)^3$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl3-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 3. Phân tích mỗi đa thức sau thành nhân tử:\nb) $x^2 + 2xy + y^2 - 16x - 16y$.",
      "dap_an_kiem": "(x + y)(x + y - 16)",
      "loi_giai": "Ta có:\n$x^2 + 2xy + y^2 - 16x - 16y = (x^2 + 2xy + y^2) - (16x + 16y)$\n$= (x + y)^2 - 16(x + y) = (x + y)(x + y - 16)$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl3-c",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 3. Phân tích mỗi đa thức sau thành nhân tử:\nc) $x^2 - 4y^2 - 10x + 25$.",
      "dap_an_kiem": "(x - 2y - 5)(x + 2y - 5)",
      "loi_giai": "Ta có:\n$x^2 - 4y^2 - 10x + 25 = (x^2 - 10x + 25) - 4y^2$\n$= (x - 5)^2 - (2y)^2 = (x - 2y - 5)(x + 2y - 5)$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl4-1a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương IV: Một số hình khối trong thực tiễn",
      "de": "Bài 4. (3,0 điểm)\n1) Một hộp quà có dạng hình chóp tứ giác đều có độ dài cạnh đáy là $13\\text{ cm}$, chiều cao là $6\\text{ cm}$, trung đoạn là $8\\text{ cm}$.\na) Tính thể tích của hộp quà.",
      "dap_an_kiem": "338",
      "loi_giai": "Diện tích đáy của hình chóp tứ giác đều là:\n$S_{\\text{đáy}} = 13^2 = 169\\text{ cm}^2$.\nThể tích của hộp quà là:\n$V = \\dfrac{1}{3} \\cdot S_{\\text{đáy}} \\cdot h = \\dfrac{1}{3} \\cdot 169 \\cdot 6 = 338\\text{ cm}^3$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl4-1b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương IV: Một số hình khối trong thực tiễn",
      "de": "Bài 4. 1) b) Người ta muốn bọc hộp quà đó bằng giấy màu. Tính diện tích giấy cần dùng (coi các mép nối là không đáng kể).",
      "dap_an_kiem": "377",
      "loi_giai": "Nửa chu vi đáy của hình chóp là: $p = \\dfrac{4 \\cdot 13}{2} = 26\\text{ cm}$.\nDiện tích xung quanh của hộp quà là:\n$S_{xq} = p \\cdot d = 26 \\cdot 8 = 208\\text{ cm}^2$.\nDiện tích toàn phần cần bọc giấy (gồm cả mặt đáy) là:\n$S_{tp} = S_{xq} + S_{\\text{đáy}} = 208 + 169 = 377\\text{ cm}^2$.\n*(Nếu không tính đáy, diện tích giấy cần dùng là $208\\text{ cm}^2$)*.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl4-2a",
      "loai": "TL",
      "band": "NB",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 4. 2) Cho tam giác nhọn $ABC$ có $AB < AC$. Các đường cao $BE, CF$ cắt nhau tại $H$. Đường thẳng đi qua $A$, song song với $BC$ cắt $BE$ tại $D$.\na) Tứ giác $ABCD$ là hình gì? Vì sao?",
      "dap_an_kiem": "ABCD la hinh thang",
      "loi_giai": "Theo giả thiết, đường thẳng đi qua $A$ song song với $BC$ cắt $BE$ tại $D$ nên $AD \\parallel BC$.\nTứ giác $ABCD$ có cặp cạnh đối $AD \\parallel BC$ nên $ABCD$ là hình thang.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl4-2b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 4. 2) b) Gọi $M$ là trung điểm của $BC$. Trên tia đối của $MH$ lấy điểm $K$ sao cho $HM = MK$. Chứng minh: $CH \\parallel BK$.",
      "dap_an_kiem": "CH // BK",
      "loi_giai": "Xét tứ giác $BHCK$, ta có:\n- $M$ là trung điểm của $BC$ (giả thiết);\n- $M$ là trung điểm của $HK$ (vì $K$ thuộc tia đối của tia $MH$ và $HM = MK$).\nSuy ra tứ giác $BHCK$ có hai đường chéo cắt nhau tại trung điểm của mỗi đường, nên $BHCK$ là hình bình hành.\nDo đó các cạnh đối song song: $CH \\parallel BK$ (và $BH \\parallel CK$).",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.75
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl4-2c",
      "loai": "TL",
      "band": "VD",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 4. 2) c) Vẽ điểm $I$ sao cho $BC$ là đường trung trực của $HI$. Chứng minh: Tứ giác $BIKC$ là hình thang cân.",
      "dap_an_kiem": "BIKC la hinh thang can",
      "loi_giai": "Gọi $P$ là giao điểm của $HI$ và $BC$. Vì $BC$ là đường trung trực của $HI$ nên $P$ là trung điểm của $HI$ và $HI \\perp BC$.\nTrong $\\Delta HIK$, có $P$ là trung điểm của $HI$ và $M$ là trung điểm của $HK$ (theo câu b), nên $PM$ là đường trung bình của $\\Delta HIK$.\nSuy ra $PM \\parallel IK$, hay $BC \\parallel IK$. Do đó tứ giác $BIKC$ là hình thang.\nMặt khác, vì $BC$ là đường trung trực của $HI$ nên $CI = CH$.\nTheo câu b, $BHCK$ là hình bình hành nên $BK = CH$.\nSuy ra $BK = CI$.\nLại có $\\Delta HIC$ cân tại $C$ có $CP$ vừa là đường cao vừa là phân giác nên $\\widehat{HCB} = \\widehat{ICB}$.\nMà $BK \\parallel CH$ nên $\\widehat{KBC} = \\widehat{HCB}$ (hai góc so le trong).\nDo đó $\\widehat{KBC} = \\widehat{ICB}$.\nHình thang $BIKC$ có hai góc kề một đáy bằng nhau ($\\widehat{KBC} = \\widehat{ICB}$) nên là hình thang cân.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.75
    },
    {
      "ma_cau": "gk1-2024-thcs-phuc-loi-tl5",
      "loai": "TL",
      "band": "VDC",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 5. (0,5 điểm) Tìm giá trị nhỏ nhất của biểu thức: $M = x^2 + y^2 - xy - x - y + 2026$.",
      "dap_an_kiem": "2025",
      "loi_giai": "Nhân cả hai vế với $2$, ta có:\n$2M = 2x^2 + 2y^2 - 2xy - 2x - 2y + 4052$\n$= (x^2 - 2xy + y^2) + (x^2 - 2x + 1) + (y^2 - 2y + 1) + 4050$\n$= (x - y)^2 + (x - 1)^2 + (y - 1)^2 + 4050$.\nVì $(x - y)^2 \\ge 0$, $(x - 1)^2 \\ge 0$, $(y - 1)^2 \\ge 0$ với mọi $x, y$,\nnên $2M \\ge 4050 \\iff M \\ge 2025$.\nDấu \"=\" xảy ra khi và chỉ khi:\n$\\begin{cases} x - y = 0 \\\\ x - 1 = 0 \\\\ y - 1 = 0 \\end{cases} \\iff x = y = 1$.\nVậy giá trị nhỏ nhất của biểu thức $M$ là $2025$, đạt được khi $x = y = 1$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    }
  ]
}

with open('inputs/refs/de-thi/lop-8/exams/gk1-2024-thcs-phuc-loi.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated phuc-loi json successfully!')
