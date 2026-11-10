# -*- coding: utf-8 -*-
"""
Script xử lý và chuẩn hóa Đề 6: gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2
(MathTech Đề đánh giá giữa học kì I - Lần 2, 2023-2024)
"""
import json

def build_de_2_mathtech():
    data = {
        "xuat_xu": {
            "lop": "8",
            "ky": "GK1",
            "nam": "2023-2024",
            "truong": "MathTech (Đề đánh giá giữa kì 1 - Lần 2)",
            "nguon": "inputs/refs/de-thi/lop-8/giua-ki-1/kntt/T8 - KNTT - Đề kiểm tra giữa kỳ 1 - đề 2.pdf",
            "loai_pdf": "text",
            "co_bieu_diem": True
        },
        "tang": 2,
        "da_duyet": True,
        "ghi_chu": "Đề chuẩn GK1 Toán 8 MathTech Đề 2 (2023-2024). Cấu trúc: Trắc nghiệm 6 câu (3.0đ) + Tự luận 4 câu (9 câu/ý, 7.0đ), tổng điểm chính xác 10.00 điểm kèm lời giải chi tiết chuẩn LaTeX.",
        "cau": []
    }

    # PHẦN I. TRẮC NGHIỆM (3,0 điểm) - 6 câu, mỗi câu 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c1",
        "vi_tri": "Câu 1",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.5,
        "de": "Câu 1. Biểu thức nào KHÔNG LÀ đa thức?\nA. $9x^2y$\nB. $2xy + xy^2$\nC. $-2x^2z$\nD. $3x - 2\\sqrt{xy}$",
        "dap_an": "D",
        "loi_giai": "Đa thức là tổng của những đơn thức. Biểu thức $3x - 2\\sqrt{xy}$ chứa căn bậc hai của các biến $\\sqrt{xy}$ nên không phải là đơn thức, do đó biểu thức này không phải là đa thức.\nChọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c2",
        "vi_tri": "Câu 2",
        "loai": "TN",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.5,
        "de": "Câu 2. Phần hệ số và phần biến của đơn thức $-x^2y$ là:\nA. Hệ số là $-1$, phần biến là $x, y$.\nB. Hệ số là $-1$, phần biến là $x^2y$.\nC. Hệ số là $1$, phần biến là $x^2y$.\nD. Hệ số là $-1$, phần biến là $xy^2$.",
        "dap_an": "B",
        "loi_giai": "Đơn thức $-x^2y = -1 \\cdot x^2y$ có phần hệ số là $-1$ và phần biến là $x^2y$.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c3",
        "vi_tri": "Câu 3",
        "loai": "TN",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.5,
        "de": "Câu 3. Biểu thức $(x - y)^2$ có kết quả của khai triển là:\nA. $x^2 + 2xy - y^2$\nB. $x^2 + 2xy + y^2$\nC. $x^2 - 2xy + y^2$\nD. $x^2 + xy + y^2$",
        "dap_an": "C",
        "loi_giai": "Áp dụng hằng đẳng thức bình phương của một hiệu: $(x - y)^2 = x^2 - 2xy + y^2$.\nChọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c4",
        "vi_tri": "Câu 4",
        "loai": "TN",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.5,
        "de": "Câu 4. Cho biểu thức $x^2 - y^2 = (\\dots)(x + y)$, điền vào chỗ \"$\\dots$\" để được hằng đẳng thức đúng:\nA. $x - y$\nB. $x + y$\nC. $xy$\nD. $2xy$",
        "dap_an": "A",
        "loi_giai": "Áp dụng hằng đẳng thức hiệu hai bình phương: $x^2 - y^2 = (x - y)(x + y)$.\nDo đó chỗ \"$\\dots$\" cần điền là $x - y$.\nChọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c5",
        "vi_tri": "Câu 5",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de": "Câu 5. Cho hình thang cân $ABCD$ ($AB \\parallel CD$) có $\\widehat{A} = 70^\\circ$. Số đo góc $C$ là:\nA. $\\widehat{C} = 70^\\circ$\nB. $\\widehat{C} = 110^\\circ$\nC. $\\widehat{C} = 80^\\circ$\nD. $\\widehat{C} = 140^\\circ$",
        "dap_an": "B",
        "loi_giai": "Vì $AB \\parallel CD$ nên hai góc trong cùng phía bù nhau: $\\widehat{A} + \\widehat{D} = 180^\\circ \\implies \\widehat{D} = 180^\\circ - 70^\\circ = 110^\\circ$.\nVì $ABCD$ là hình thang cân ($AB \\parallel CD$) nên hai góc kề đáy $CD$ bằng nhau: $\\widehat{C} = \\widehat{D} = 110^\\circ$.\nChọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c6",
        "vi_tri": "Câu 6",
        "loai": "TN",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.5,
        "de": "Câu 6. Cho hình chữ nhật $ABCD$ có $O$ là giao điểm hai đường chéo. Khẳng định nào sau đây SAI:\nA. $AB = CD$\nB. $AD \\parallel BC$\nC. $OC = CD$\nD. $OA > OC$",
        "dap_an": "D",
        "loi_giai": "Trong hình chữ nhật $ABCD$, hai đường chéo $AC$ và $BD$ bằng nhau và cắt nhau tại trung điểm $O$ của mỗi đường, nên $OA = OC = OB = OD = \\frac{1}{2}AC$.\nDo đó khẳng định $OA > OC$ là SAI.\nChọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # PHẦN II. TỰ LUẬN (7,0 điểm)
    # Câu 7 (1,0 điểm): 7.1: 0.5đ, 7.2: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c7-1",
        "vi_tri": "Câu 7.1",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Câu 7 (1,0 điểm).",
        "de": "1. Viết hằng đẳng thức diễn tả theo lời văn: Bình phương một tổng của hai số $x$ và $y$.",
        "dap_an": "$(x + y)^2 = x^2 + 2xy + y^2$",
        "loi_giai": "Hằng đẳng thức bình phương một tổng của hai số $x$ và $y$ là:\n$$(x + y)^2 = x^2 + 2xy + y^2.$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c7-2",
        "vi_tri": "Câu 7.2",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Phân tích đa thức thành nhân tử", "Hằng đẳng thức đáng nhớ"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Câu 7 (1,0 điểm).",
        "de": "2. Viết đa thức sau dưới dạng tích: $x^2 - 25$.",
        "dap_an": "$(x - 5)(x + 5)$",
        "loi_giai": "Áp dụng hằng đẳng thức hiệu hai bình phương:\n$$x^2 - 25 = x^2 - 5^2 = (x - 5)(x + 5).$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Câu 8 (2,0 điểm): 8.1: 0.75đ, 8.2: 0.75đ, 8.3: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c8-1",
        "vi_tri": "Câu 8.1",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Chia đa thức cho đơn thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.75,
        "de_chung": "Câu 8 (2,0 điểm).",
        "de": "1. Thực hiện phép chia đa thức $A = 5x^3y^2 - 3x^2y + xy$ cho đơn thức $xy$.",
        "dap_an": "$5x^2y - 3x + 1$",
        "loi_giai": "Chia từng hạng tử của đa thức $A$ cho đơn thức $xy$:\n$$\\begin{aligned}\nA : xy &= (5x^3y^2 - 3x^2y + xy) : xy \\\\\n&= (5x^3y^2 : xy) - (3x^2y : xy) + (xy : xy) \\\\\n&= 5x^2y - 3x + 1.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c8-2",
        "vi_tri": "Câu 8.2",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Cộng trừ đa thức"],
        "band": "TH",
        "phut": 3.5,
        "diem_bai": 0.75,
        "de_chung": "Câu 8 (2,0 điểm).",
        "de": "2. Cho đa thức $M = x^3 - x^2y + 2xy + 3$ và $P = 3x^3 - 2x^2y - xy + 3$. Tìm đa thức $A$ biết: $A + 2M = P$.",
        "dap_an": "$A = x^3 - 5xy - 3$",
        "loi_giai": "Từ $A + 2M = P$, suy ra $A = P - 2M$.\nTa tính:\n$$\\begin{aligned}\n2M &= 2(x^3 - x^2y + 2xy + 3) = 2x^3 - 2x^2y + 4xy + 6. \\\\\nA &= P - 2M \\\\\n&= (3x^3 - 2x^2y - xy + 3) - (2x^3 - 2x^2y + 4xy + 6) \\\\\n&= 3x^3 - 2x^2y - xy + 3 - 2x^3 + 2x^2y - 4xy - 6 \\\\\n&= (3x^3 - 2x^3) + (-2x^2y + 2x^2y) + (-xy - 4xy) + (3 - 6) \\\\\n&= x^3 - 5xy - 3.\n\\end{aligned}$$\nVậy $A = x^3 - 5xy - 3$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c8-3",
        "vi_tri": "Câu 8.3",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tính giá trị của đa thức", "Những hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Câu 8 (2,0 điểm).",
        "de": "3. Tính giá trị của đa thức $N$ biết: $N = 9x^2 - 12x + 4$ tại $x = \\frac{2}{3}$.",
        "dap_an": "$N = 0$",
        "loi_giai": "Thu gọn đa thức $N$ bằng hằng đẳng thức:\n$$N = 9x^2 - 12x + 4 = (3x)^2 - 2 \\cdot 3x \\cdot 2 + 2^2 = (3x - 2)^2.$$\nThay $x = \\frac{2}{3}$ vào biểu thức thu gọn, ta được:\n$$N = \\left(3 \\cdot \\frac{2}{3} - 2\\right)^2 = (2 - 2)^2 = 0^2 = 0.$$\nVậy tại $x = \\frac{2}{3}$ thì $N = 0$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Câu 9 (3,0 điểm): 9a: 1.0đ, 9b: 1.0đ, 9c: 1.0đ
    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c9a",
        "vi_tri": "Câu 9.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Câu 9 (3,0 điểm). Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $BE$ và $CF$ cắt nhau tại $H$. Qua $C, B$ kẻ các đường thẳng vuông góc với $AC, AB$ cắt nhau tại $K$.",
        "de": "a) Tứ giác $BHCK$ là hình gì? Vì sao?",
        "dap_an": "$BHCK$ là hình bình hành",
        "loi_giai": "- Ta có $BE \\perp AC$ (do $BE$ là đường cao) và $CK \\perp AC$ (theo giả thiết).\n  Suy ra $BE \\parallel CK$, hay $BH \\parallel CK$.\n- Tương tự, $CF \\perp AB$ (do $CF$ là đường cao) và $BK \\perp AB$ (theo giả thiết).\n  Suy ra $CF \\parallel BK$, hay $CH \\parallel BK$.\n- Tứ giác $BHCK$ có các cặp cạnh đối song song ($BH \\parallel CK$ và $CH \\parallel BK$) nên $BHCK$ là hình bình hành (theo dấu hiệu nhận biết).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c9b",
        "vi_tri": "Câu 9.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Câu 9 (3,0 điểm). Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $BE$ và $CF$ cắt nhau tại $H$. Qua $C, B$ kẻ các đường thẳng vuông góc với $AC, AB$ cắt nhau tại $K$.",
        "de": "b) Gọi $M$ là trung điểm của $BC$. Chứng minh $H, M, K$ thẳng hàng.",
        "dap_an": "$H, M, K$ thẳng hàng",
        "loi_giai": "- Theo câu a, tứ giác $BHCK$ là hình bình hành.\n- Do đó hai đường chéo $BC$ và $HK$ cắt nhau tại trung điểm của mỗi đường.\n- Mà $M$ là trung điểm của $BC$ (theo giả thiết), nên $M$ cũng là trung điểm của $HK$.\nVậy ba điểm $H, M, K$ thẳng hàng (đpcm).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c9c",
        "vi_tri": "Câu 9.c",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "VD",
        "phut": 4.5,
        "diem_bai": 1.0,
        "de_chung": "Câu 9 (3,0 điểm). Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $BE$ và $CF$ cắt nhau tại $H$. Qua $C, B$ kẻ các đường thẳng vuông góc với $AC, AB$ cắt nhau tại $K$.",
        "de": "c) Từ $H$ kẻ $HG \\perp BC$ ($G \\in BC$). Lấy điểm $I$ thuộc tia đối của tia $GH$ sao cho $GH = GI$. Chứng minh: $BCKI$ là hình thang cân.",
        "dap_an": "$BCKI$ là hình thang cân",
        "loi_giai": "1) Chứng minh $BCKI$ là hình thang:\n- Xét tam giác $HIK$, ta có:\n  + $G$ là trung điểm của $HI$ (vì $I$ thuộc tia đối của $GH$ và $GH = GI$);\n  + $M$ là trung điểm của $HK$ (theo câu b).\n- Do đó đoạn thẳng $GM$ là đường trung bình của tam giác $HIK$.\n  Suy ra $GM \\parallel IK$.\n- Vì $G \\in BC$ và $M \\in BC$ nên đường thẳng $GM$ trùng với đường thẳng $BC$.\n  Suy ra $BC \\parallel IK$.\n- Tứ giác $BCKI$ có $BC \\parallel IK$ nên là hình thang.\n\n2) Chứng minh hình thang $BCKI$ là hình thang cân:\n- Vì $HG \\perp BC$ tại $G$ và $G$ là trung điểm của đoạn thẳng $HI$ nên $BC$ là đường trung trực của đoạn thẳng $HI$.\n  Do điểm $C$ nằm trên đường trung trực của $HI$ nên $CI = CH$.\n- Mặt khác, vì $BHCK$ là hình bình hành nên hai cạnh đối bằng nhau: $BK = CH$.\n- Từ đó suy ra: $BK = CI$.\n- Hình thang $BCKI$ có hai đường chéo bằng nhau ($BK = CI$) nên $BCKI$ là hình thang cân (đpcm).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Câu 10 (1,0 điểm)
    data["cau"].append({
        "id": "l8-gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2-c10",
        "vi_tri": "Câu 10",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Những hằng đẳng thức đáng nhớ"],
        "band": "VD",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de": "Câu 10 (1,0 điểm). Chứng minh đa thức sau không phụ thuộc vào $x$:\n$$C = (x^2 - 1)(x^2 + 1)(x^4 + 1)(x^8 + 1)(x^{16} + 1)(x^{32} + 1) - x^{64}.$$",
        "dap_an": "$C = -1$ (không phụ thuộc vào $x$)",
        "loi_giai": "Áp dụng hằng đẳng thức hiệu hai bình phương $(A - B)(A + B) = A^2 - B^2$ liên tiếp:\n$$\\begin{aligned}\n(x^2 - 1)(x^2 + 1) &= (x^2)^2 - 1 = x^4 - 1 \\\\\n(x^4 - 1)(x^4 + 1) &= (x^4)^2 - 1 = x^8 - 1 \\\\\n(x^8 - 1)(x^8 + 1) &= (x^8)^2 - 1 = x^{16} - 1 \\\\\n(x^{16} - 1)(x^{16} + 1) &= (x^{16})^2 - 1 = x^{32} - 1 \\\\\n(x^{32} - 1)(x^{32} + 1) &= (x^{32})^2 - 1 = x^{64} - 1.\n\\end{aligned}$$\nKhi đó biểu thức $C$ trở thành:\n$$C = (x^{64} - 1) - x^{64} = -1.$$\nVì kết quả rút gọn là một hằng số $-1$ nên giá trị của đa thức $C$ không phụ thuộc vào biến $x$ (đpcm).",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    return data

if __name__ == "__main__":
    d = build_de_2_mathtech()
    with open("inputs/refs/de-thi/lop-8/exams/gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("Updated gk1-x-t8-kntt-de-kiem-tra-giua-ky-1-de-2.json successfully! Cau count:", len(d["cau"]))
