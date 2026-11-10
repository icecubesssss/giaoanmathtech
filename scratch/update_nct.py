# -*- coding: utf-8 -*-
import json

data = {
  "xuat_xu": "Đề giữa kì 1 Toán 8 năm học 2024 – 2025 trường THCS Nguyễn Công Trứ – Ba Đình – Hà Nội",
  "tang": "lop-8",
  "da_duyet": True,
  "ghi_chu": "Đã soát toàn diện theo ảnh đề gốc (1 trang duy nhất), sửa triệt để lỗi OCR chữ lặp, chuẩn hóa công thức LaTeX và lời giải chi tiết 100% tự luận.",
  "cau": [
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl1-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 1. (1,5 điểm)\na) Thu gọn và tìm bậc của đơn thức: $A = \\left(\\dfrac{2}{3}x^2y^2\\right) \\cdot \\left(-\\dfrac{5}{4}xy^3\\right)$.",
      "dap_an_kiem": "-5/6 x^3y^5",
      "loi_giai": "Ta có:\n$A = \\left[\\dfrac{2}{3} \\cdot \\left(-\\dfrac{5}{4}\\right)\\right] \\cdot (x^2 \\cdot x) \\cdot (y^2 \\cdot y^3) = -\\dfrac{5}{6}x^3y^5$.\nBậc của đơn thức $A$ là tổng số mũ của các biến: $3 + 5 = 8$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 1.0
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl1-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 1. b) Tính giá trị của $A$ biết $x = 2, y = 1$.",
      "dap_an_kiem": "-20/3",
      "loi_giai": "Thay $x = 2$ và $y = 1$ vào đơn thức thu gọn $A = -\\dfrac{5}{6}x^3y^5$, ta được:\n$A = -\\dfrac{5}{6} \\cdot 2^3 \\cdot 1^5 = -\\dfrac{5}{6} \\cdot 8 = -\\dfrac{20}{3}$.\nVậy giá trị của $A$ tại $x = 2, y = 1$ là $-\\dfrac{20}{3}$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl2-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. (2,0 điểm) Thực hiện phép tính:\na) $(6x^3y + 2xy) \\cdot (xy^2)$.",
      "dap_an_kiem": "6x^4y^3 + 2x^2y^3",
      "loi_giai": "Ta có:\n$(6x^3y + 2xy) \\cdot (xy^2) = 6x^3y \\cdot xy^2 + 2xy \\cdot xy^2 = 6x^4y^3 + 2x^2y^3$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl2-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. Thực hiện phép tính:\nb) $(x + 2y)(x^2 + 3y^2)$.",
      "dap_an_kiem": "x^3 + 2x^2y + 3xy^2 + 6y^3",
      "loi_giai": "Ta có:\n$(x + 2y)(x^2 + 3y^2) = x \\cdot x^2 + x \\cdot 3y^2 + 2y \\cdot x^2 + 2y \\cdot 3y^2 = x^3 + 3xy^2 + 2x^2y + 6y^3$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl2-c",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. Thực hiện phép tính:\nc) $(12x^2y - 8xy^2 + xy) : (4xy)$.",
      "dap_an_kiem": "3x - 2y + 1/4",
      "loi_giai": "Ta có:\n$(12x^2y - 8xy^2 + xy) : (4xy) = (12x^2y : 4xy) - (8xy^2 : 4xy) + (xy : 4xy) = 3x - 2y + \\dfrac{1}{4}$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl2-d",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 2. Thực hiện phép tính:\nd) $(5x^2 - 2xy + 3) + (7 - 10xy + 4x^2)$.",
      "dap_an_kiem": "9x^2 - 12xy + 10",
      "loi_giai": "Ta có:\n$(5x^2 - 2xy + 3) + (7 - 10xy + 4x^2) = (5x^2 + 4x^2) + (-2xy - 10xy) + (3 + 7) = 9x^2 - 12xy + 10$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl3-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 3. (1,5 điểm) Tìm $x$, biết:\na) $x(3x - 2) - 9x^3 : 3x = 4$.",
      "dap_an_kiem": "-2",
      "loi_giai": "Ta có:\n$x(3x - 2) - 9x^3 : 3x = 4$\n$\\iff 3x^2 - 2x - 3x^2 = 4$\n$\\iff -2x = 4$\n$\\iff x = -2$.\nVậy $x = -2$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl3-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 3. Tìm $x$, biết:\nb) $2x(2x + 4) - 4x^2 = 88$.",
      "dap_an_kiem": "11",
      "loi_giai": "Ta có:\n$2x(2x + 4) - 4x^2 = 88$\n$\\iff 4x^2 + 8x - 4x^2 = 88$\n$\\iff 8x = 88$\n$\\iff x = 11$.\nVậy $x = 11$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl3-c",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 3. Tìm $x$, biết:\nc) $x(x + 3) - (x - 3)(x + 5) = 0$.",
      "dap_an_kiem": "-15",
      "loi_giai": "Ta có:\n$x(x + 3) - (x - 3)(x + 5) = 0$\n$\\iff (x^2 + 3x) - (x^2 + 5x - 3x - 15) = 0$\n$\\iff x^2 + 3x - x^2 - 2x + 15 = 0$\n$\\iff x + 15 = 0$\n$\\iff x = -15$.\nVậy $x = -15$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl4-a",
      "loai": "TL",
      "band": "NB",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 4. (1,0 điểm) Trong giờ học Mỹ Thuật, bạn Hạnh dán lên trang vở hai hình vuông có độ dài cạnh lần lượt là $x\\text{ (cm)}$, $y\\text{ (cm)}$.\na) Viết công thức tính tổng diện tích của hai hình vuông đó?",
      "dap_an_kiem": "x^2 + y^2",
      "loi_giai": "Diện tích của hình vuông thứ nhất có cạnh $x\\text{ cm}$ là $S_1 = x^2\\text{ (cm}^2\\text{)}$.\nDiện tích của hình vuông thứ hai có cạnh $y\\text{ cm}$ là $S_2 = y^2\\text{ (cm}^2\\text{)}$.\nTổng diện tích của hai hình vuông là:\n$S = S_1 + S_2 = x^2 + y^2\\text{ (cm}^2\\text{)}$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl4-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương I: Đa thức",
      "de": "Bài 4. b) Tính tổng diện tích của hai hình vuông đó tại $x = 3$ và $y = 5$?",
      "dap_an_kiem": "34",
      "loi_giai": "Thay $x = 3$ và $y = 5$ vào công thức $S = x^2 + y^2$, ta được:\n$S = 3^2 + 5^2 = 9 + 25 = 34\\text{ (cm}^2\\text{)}$.\nVậy tổng diện tích của hai hình vuông là $34\\text{ cm}^2$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl5-a",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 5. (3,5 điểm) Cho tam giác $ABC$ cân tại $A$, đường cao $AH$. Gọi $I$ là trung điểm của $AC$.\na) Giả sử $AC = 6\\text{ cm}$, hãy tính $HI$?",
      "dap_an_kiem": "3",
      "loi_giai": "Vì $AH$ là đường cao của $\\Delta ABC$ nên $AH \\perp BC$ tại $H$, suy ra tam giác $AHC$ vuông tại $H$.\nTrong tam giác vuông $AHC$, $HI$ là đường trung tuyến ứng với cạnh huyền $AC$ (vì $I$ là trung điểm của $AC$).\nDo đó: $HI = \\dfrac{1}{2}AC = \\dfrac{1}{2} \\cdot 6 = 3\\text{ cm}$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 1.0
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl5-b",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 5. b) Trên tia đối của tia $IH$ lấy điểm $K$ sao cho $IK = IH$. Chứng minh rằng: tứ giác $AHCK$ là hình chữ nhật.",
      "dap_an_kiem": "AHCK la hinh chu nhat",
      "loi_giai": "Xét tứ giác $AHCK$, ta có:\n- $I$ là trung điểm của đường chéo $AC$ (giả thiết);\n- $I$ là trung điểm của đường chéo $HK$ (vì $K$ thuộc tia đối của tia $IH$ và $IK = IH$).\nSuy ra tứ giác $AHCK$ là hình bình hành (hai đường chéo cắt nhau tại trung điểm của mỗi đường).\nMặt khác, $\\widehat{AHC} = 90^\\circ$ (vì $AH \\perp BC$ tại $H$).\nHình bình hành $AHCK$ có một góc vuông ($\\widehat{AHC} = 90^\\circ$) nên là hình chữ nhật.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 1.0
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl5-c",
      "loai": "TL",
      "band": "TH",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 5. c) Tứ giác $AKHB$ là hình gì? Vì sao?",
      "dap_an_kiem": "AKHB la hinh binh hanh",
      "loi_giai": "Tam giác $ABC$ cân tại $A$ có $AH$ là đường cao đồng thời là đường trung tuyến, nên $H$ là trung điểm của $BC$, suy ra $HB = HC$.\nVì tứ giác $AHCK$ là hình chữ nhật (theo câu b) nên $AK \\parallel HC$ và $AK = HC$.\nDo $B, H, C$ thẳng hàng nên $AK \\parallel HB$.\nLại có $AK = HC = HB$.\nTứ giác $AKHB$ có cặp cạnh đối $AK$ và $HB$ song song và bằng nhau ($AK \\parallel HB$ và $AK = HB$).\nDo đó tứ giác $AKHB$ là hình bình hành.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.75
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl5-d",
      "loai": "TL",
      "band": "VD",
      "chuong": "Chương III: Tứ giác",
      "de": "Bài 5. d) Gọi $G$ là trung điểm của $AB$, chứng minh $AH, BK, GI$ đồng quy.",
      "dap_an_kiem": "AH, BK, GI dong quy",
      "loi_giai": "Vì tứ giác $AKHB$ là hình bình hành (theo câu c) nên hai đường chéo $AH$ và $BK$ cắt nhau tại trung điểm $O$ của mỗi đường.\nTrong tam giác $ABC$, ta có $G$ là trung điểm của $AB$ và $I$ là trung điểm của $AC$, do đó $GI$ là đường trung bình của tam giác $ABC$, suy ra $GI \\parallel BC$.\nTrong tam giác $ABH$, $G$ là trung điểm của $AB$ và $O$ là trung điểm của $AH$, nên $GO$ là đường trung bình của $\\Delta ABH$, suy ra $GO \\parallel BH$ (tức $GO \\parallel BC$).\nTrong tam giác $AHC$, $O$ là trung điểm của $AH$ và $I$ là trung điểm của $AC$, nên $OI$ là đường trung bình của $\\Delta AHC$, suy ra $OI \\parallel HC$ (tức $OI \\parallel BC$).\nTheo tiên đề Ơ-clit, qua điểm $O$ chỉ có một đường thẳng song song với $BC$, do đó ba điểm $G, O, I$ thẳng hàng, hay đường thẳng $GI$ đi qua điểm $O$.\nVậy ba đường thẳng $AH, BK, GI$ đồng quy tại điểm $O$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.75
    },
    {
      "ma_cau": "gk1-2024-thcs-nguyen-cong-tru-tl6",
      "loai": "TL",
      "band": "VDC",
      "chuong": "Chương II: Hằng đẳng thức đáng nhớ và ứng dụng",
      "de": "Bài 6. (0,5 điểm) Cho $a, b, c \\ne 0$ thỏa mãn $(a + b + c)\\left(\\dfrac{1}{a} + \\dfrac{1}{b} + \\dfrac{1}{c}\\right) = 1$.\nTính giá trị của biểu thức: $P = (a^{2025} + b^{2025})(b^{2023} + c^{2023})(c^{2011} + a^{2011})$.",
      "dap_an_kiem": "0",
      "loi_giai": "Từ giả thiết $(a + b + c)\\left(\\dfrac{1}{a} + \\dfrac{1}{b} + \\dfrac{1}{c}\\right) = 1$, ta có:\n$(a + b + c)\\dfrac{ab + bc + ca}{abc} = 1 \\iff (a + b + c)(ab + bc + ca) - abc = 0$.\nKhai triển và phân tích đa thức thành nhân tử:\n$(a + b + c)(ab + bc + ca) - abc$\n$= a(ab + bc + ca) + b(ab + bc + ca) + c(ab + bc + ca) - abc$\n$= a^2b + abc + ca^2 + ab^2 + b^2c + abc + abc + bc^2 + c^2a - abc$\n$= ab(a + b) + c(a^2 + 2ab + b^2) + c^2(a + b)$\n$= ab(a + b) + c(a + b)^2 + c^2(a + b)$\n$= (a + b)[ab + c(a + b) + c^2]\n= (a + b)(ab + ac + bc + c^2)\n= (a + b)[a(b + c) + c(b + c)]\n= (a + b)(b + c)(c + a) = 0$.\nSuy ra $a + b = 0$ hoặc $b + c = 0$ hoặc $c + a = 0$.\n- Nếu $a + b = 0 \\iff a = -b$: vì $2025$ là số lẻ nên $a^{2025} = (-b)^{2025} = -b^{2025} \\Rightarrow a^{2025} + b^{2025} = 0$, dẫn đến $P = 0$.\n- Nếu $b + c = 0 \\iff b = -c$: vì $2023$ là số lẻ nên $b^{2023} = (-c)^{2023} = -c^{2023} \\Rightarrow b^{2023} + c^{2023} = 0$, dẫn đến $P = 0$.\n- Nếu $c + a = 0 \\iff c = -a$: vì $2011$ là số lẻ nên $c^{2011} = (-a)^{2011} = -a^{2011} \\Rightarrow c^{2011} + a^{2011} = 0$, dẫn đến $P = 0$.\nVậy trong mọi trường hợp, giá trị của biểu thức $P$ bằng $0$.",
      "da_duyet": True,
      "can_doc_anh": False,
      "diem_bai": 0.5
    }
  ]
}

with open('inputs/refs/de-thi/lop-8/exams/gk1-2024-thcs-nguyen-cong-tru.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated nguyen-cong-tru json successfully!')
