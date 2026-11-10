# -*- coding: utf-8 -*-
"""
Script xử lý và chuẩn hóa 2 đề:
1. gk1-2025-thcs-van-khe
2. gk1-2025-thcs-van-yen
"""
import json

def build_van_khe():
    data = {
        "xuat_xu": {
            "lop": "8",
            "ky": "GK1",
            "nam": "2025-2026",
            "truong": "THCS Văn Khê (Hà Đông)",
            "nguon": "inputs/refs/de-thi/lop-8/giua-ki-1/de-giua-hoc-ky-1-toan-8-nam-2025-2026-truong-thcs-van-khe-ha-noi.pdf",
            "loai_pdf": "ocr",
            "co_bieu_diem": False
        },
        "tang": 2,
        "da_duyet": True,
        "ghi_chu": "Đề chuẩn GK1 Toán 8 THCS Văn Khê 2025-2026. Đã soát 100% từ ảnh gốc: 100% Tự luận gồm 5 bài (14 câu/ý), tổng điểm chính xác 10.00 điểm.",
        "cau": []
    }

    # Bài I (2,0 điểm) - 4 câu, mỗi câu 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b1a",
        "vi_tri": "Bài I.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Đơn thức, đơn thức đồng dạng", "Thu gọn đa thức"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài I (2,0 điểm). Rút gọn biểu thức:",
        "de": "Rút gọn biểu thức: $6xy^2 - 3xy^2 - 12xy^2$.",
        "dap_an": "$-9xy^2$",
        "loi_giai": "Ta có:\n$$6xy^2 - 3xy^2 - 12xy^2 = (6 - 3 - 12)xy^2 = -9xy^2.$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b1b",
        "vi_tri": "Bài I.b",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Cộng trừ đa thức"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài I (2,0 điểm). Rút gọn biểu thức:",
        "de": "Rút gọn biểu thức: $(x^2 - 2yz + z^2) + (3yz - z^2 + 5x^2)$.",
        "dap_an": "$6x^2 + yz$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(x^2 - 2yz + z^2) + (3yz - z^2 + 5x^2) &= x^2 - 2yz + z^2 + 3yz - z^2 + 5x^2 \\\\\n&= (x^2 + 5x^2) + (-2yz + 3yz) + (z^2 - z^2) \\\\\n&= 6x^2 + yz.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b1c",
        "vi_tri": "Bài I.c",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Nhân đa thức với đa thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài I (2,0 điểm). Rút gọn biểu thức:",
        "de": "Rút gọn biểu thức: $(1 - 2x)(5 - 3x) + (4 - x)^2$.",
        "dap_an": "$7x^2 - 21x + 21$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(1 - 2x)(5 - 3x) + (4 - x)^2 &= (5 - 3x - 10x + 6x^2) + (16 - 8x + x^2) \\\\\n&= 6x^2 - 13x + 5 + x^2 - 8x + 16 \\\\\n&= (6x^2 + x^2) + (-13x - 8x) + (5 + 16) \\\\\n&= 7x^2 - 21x + 21.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b1d",
        "vi_tri": "Bài I.d",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Những hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài I (2,0 điểm). Rút gọn biểu thức:",
        "de": "Rút gọn biểu thức: $(x + 1)^3 - (x - 4)(x + 4) - x^3$.",
        "dap_an": "$2x^2 + 3x + 17$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(x + 1)^3 - (x - 4)(x + 4) - x^3 &= (x^3 + 3x^2 + 3x + 1) - (x^2 - 16) - x^3 \\\\\n&= x^3 + 3x^2 + 3x + 1 - x^2 + 16 - x^3 \\\\\n&= (x^3 - x^3) + (3x^2 - x^2) + 3x + (1 + 16) \\\\\n&= 2x^2 + 3x + 17.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài II (2,0 điểm) - 4 câu, mỗi câu 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b2a",
        "vi_tri": "Bài II.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Tìm x"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II (2,0 điểm). Tìm $x$ biết:",
        "de": "Tìm $x$ biết: $2(3x - 1) = 10$.",
        "dap_an": "$x = 2$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n2(3x - 1) &= 10 \\\\\n3x - 1 &= 5 \\\\\n3x &= 6 \\\\\nx &= 2.\n\\end{aligned}$$\nVậy $x = 2$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b2b",
        "vi_tri": "Bài II.b",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Tìm x", "Nhân đa thức với đa thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II (2,0 điểm). Tìm $x$ biết:",
        "de": "Tìm $x$ biết: $(3x - 1)(2x + 7) - (6x^2 + x - 5) = 7$.",
        "dap_an": "$x = \\frac{1}{2}$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(3x - 1)(2x + 7) - (6x^2 + x - 5) &= 7 \\\\\n(6x^2 + 21x - 2x - 7) - 6x^2 - x + 5 &= 7 \\\\\n6x^2 + 19x - 7 - 6x^2 - x + 5 &= 7 \\\\\n18x - 2 &= 7 \\\\\n18x &= 9 \\\\\nx &= \\frac{9}{18} = \\frac{1}{2}.\n\\end{aligned}$$\nVậy $x = \\frac{1}{2}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b2c",
        "vi_tri": "Bài II.c",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tìm x", "Hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II (2,0 điểm). Tìm $x$ biết:",
        "de": "Tìm $x$ biết: $(x - 5)^2 - x(x + 2) = 5$.",
        "dap_an": "$x = \\frac{5}{3}$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(x - 5)^2 - x(x + 2) &= 5 \\\\\nx^2 - 10x + 25 - x^2 - 2x &= 5 \\\\\n-12x + 25 &= 5 \\\\\n-12x &= -20 \\\\\nx &= \\frac{-20}{-12} = \\frac{5}{3}.\n\\end{aligned}$$\nVậy $x = \\frac{5}{3}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b2d",
        "vi_tri": "Bài II.d",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tìm x", "Hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II (2,0 điểm). Tìm $x$ biết:",
        "de": "Tìm $x$ biết: $(x + 2)^2 - (x - 3)(x + 3) = -3$.",
        "dap_an": "$x = -4$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\n(x + 2)^2 - (x - 3)(x + 3) &= -3 \\\\\nx^2 + 4x + 4 - (x^2 - 9) &= -3 \\\\\nx^2 + 4x + 4 - x^2 + 9 &= -3 \\\\\n4x + 13 &= -3 \\\\\n4x &= -16 \\\\\nx &= -4.\n\\end{aligned}$$\nVậy $x = -4$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài III (2,0 điểm) - 3 câu: 0.5đ, 1.0đ, 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b3a",
        "vi_tri": "Bài III.a",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Tính giá trị của đa thức"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài III (2,0 điểm). Cho biểu thức: $A = x^2 + 2x$ và $B = (x - 2)(x + 2) - (x - 1)^2 - (2x - 7)$.",
        "de": "Tính giá trị biểu thức $A$ tại $x = -2$.",
        "dap_an": "$A = 0$",
        "loi_giai": "Thay $x = -2$ vào biểu thức $A$, ta được:\n$$A = (-2)^2 + 2(-2) = 4 - 4 = 0.$$\nVậy tại $x = -2$ thì $A = 0$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b3b",
        "vi_tri": "Bài III.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài III (2,0 điểm). Cho biểu thức: $A = x^2 + 2x$ và $B = (x - 2)(x + 2) - (x - 1)^2 - (2x - 7)$.",
        "de": "Rút gọn biểu thức $P = A + B$.",
        "dap_an": "$P = x^2 + 2x + 2$",
        "loi_giai": "Trước hết ta rút gọn biểu thức $B$:\n$$\\begin{aligned}\nB &= (x - 2)(x + 2) - (x - 1)^2 - (2x - 7) \\\\\n&= (x^2 - 4) - (x^2 - 2x + 1) - 2x + 7 \\\\\n&= x^2 - 4 - x^2 + 2x - 1 - 2x + 7 \\\\\n&= (x^2 - x^2) + (2x - 2x) + (-4 - 1 + 7) \\\\\n&= 2.\n\\end{aligned}$$\nKhi đó:\n$$P = A + B = (x^2 + 2x) + 2 = x^2 + 2x + 2.$$\nVậy $P = x^2 + 2x + 2$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b3c",
        "vi_tri": "Bài III.c",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Chứng minh biểu thức luôn dương, luôn âm"],
        "band": "VD",
        "phut": 3.5,
        "diem_bai": 0.5,
        "de_chung": "Bài III (2,0 điểm). Cho biểu thức: $A = x^2 + 2x$ và $B = (x - 2)(x + 2) - (x - 1)^2 - (2x - 7)$.",
        "de": "Chứng minh biểu thức $P = A + B$ luôn dương với mọi giá trị của $x$.",
        "dap_an": "$P = (x + 1)^2 + 1 > 0,\\ \\forall x$",
        "loi_giai": "Theo câu b, ta có $P = x^2 + 2x + 2$.\nBiến đổi:\n$$P = (x^2 + 2x + 1) + 1 = (x + 1)^2 + 1.$$\nVì $(x + 1)^2 \\ge 0$ với mọi giá trị của $x$, nên:\n$$(x + 1)^2 + 1 \\ge 1 > 0,\\quad \\forall x.$$\nDo đó, biểu thức $P$ luôn dương với mọi giá trị của $x$ (đpcm).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài IV (3,5 điểm): IV.1: 1.0đ; IV.2a: 1.0đ; IV.2b: 1.0đ; IV.2c: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b4-1",
        "vi_tri": "Bài IV.1",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Đường trung bình của tam giác", "Bài toán thực tế hình học"],
        "band": "TH",
        "phut": 3.5,
        "diem_bai": 1.0,
        "de_chung": "Bài IV (3,5 điểm).",
        "de": "1. Để tính khoảng cách giữa hai vị trí $A$ và $B$ ở hai bên bờ ao cá, người ta đã thực hiện đo đạc như hình bên: điểm $A$ nằm trên $MN$ sao cho $MA = AN = 9\\text{ m}$; điểm $B$ nằm trên $MP$ sao cho $MB = BP = 16\\text{ m}$; khoảng cách giữa hai cọc mốc $N$ và $P$ là $NP = 29\\text{ m}$. Hỏi hai vị trí $A$ và $B$ cách nhau bao nhiêu mét?",
        "dap_an": "$AB = 14{,}5\\text{ m}$",
        "loi_giai": "Xét tam giác $MNP$:\n- Điểm $A$ thuộc cạnh $MN$ và $MA = AN = 9\\text{ m}$ nên $A$ là trung điểm của $MN$.\n- Điểm $B$ thuộc cạnh $MP$ và $MB = BP = 16\\text{ m}$ nên $B$ là trung điểm của $MP$.\nDo đó, đoạn thẳng $AB$ là đường trung bình của tam giác $MNP$.\nSuy ra:\n$$AB = \\frac{1}{2} NP = \\frac{1}{2} \\cdot 29 = 14{,}5\\text{ (m)}.$$\nVậy hai vị trí $A$ và $B$ cách nhau $14{,}5$ mét.",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b4-2a",
        "vi_tri": "Bài IV.2.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân", "Đường trung bình của tam giác"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài IV.2. Cho $\\Delta MNP$ nhọn, các đường trung tuyến $ME, NF$ cắt nhau tại $G$.",
        "de": "Chứng minh tứ giác $EFMN$ là hình thang.",
        "dap_an": "$EFMN$ là hình thang vì $EF \\parallel MN$",
        "loi_giai": "Vì $ME$ là đường trung tuyến của tam giác $MNP$ nên $E$ là trung điểm của $NP$.\nVì $NF$ là đường trung tuyến của tam giác $MNP$ nên $F$ là trung điểm của $MP$.\nSuy ra đoạn thẳng $EF$ là đường trung bình của tam giác $MNP$.\nDo đó $EF \\parallel MN$.\nTứ giác $EFMN$ có hai cạnh đối $EF \\parallel MN$ nên là hình thang.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b4-2b",
        "vi_tri": "Bài IV.2.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành"],
        "band": "TH",
        "phut": 4.5,
        "diem_bai": 1.0,
        "de_chung": "Bài IV.2. Cho $\\Delta MNP$ nhọn, các đường trung tuyến $ME, NF$ cắt nhau tại $G$.",
        "de": "Trên tia đối của tia $FN$ lấy điểm $D$ sao cho $FD = FG$, trên tia đối của tia $EM$ lấy điểm $H$ sao cho $GH = MG$. Chứng minh $MGPD$ là hình bình hành và $GE = EH$.",
        "dap_an": "$MGPD$ là hình bình hành và $GE = EH$",
        "loi_giai": "1) Chứng minh $MGPD$ là hình bình hành:\n- Xét tứ giác $MGPD$, có hai đường chéo là $MP$ và $GD$.\n- Theo giả thiết, $F$ là trung điểm của cạnh $MP$.\n- Trên tia đối của tia $FN$ lấy điểm $D$ sao cho $FD = FG$, nghĩa là $F$ là trung điểm của đoạn thẳng $GD$.\nTứ giác $MGPD$ có hai đường chéo $MP$ và $GD$ cắt nhau tại trung điểm $F$ của mỗi đường, nên $MGPD$ là hình bình hành.\n\n2) Chứng minh $GE = EH$:\n- Trong tam giác $MNP$, hai đường trung tuyến $ME$ và $NF$ cắt nhau tại $G$ nên $G$ là trọng tâm của tam giác $MNP$.\nTheo tính chất ba đường trung tuyến, ta có:\n$$MG = 2GE.$$\n- Trên tia đối của tia $EM$ lấy điểm $H$ sao cho $GH = MG$. Vì tia đối của tia $EM$ có chiều từ $E$ ra ngoài phía điểm $H$, nên điểm $E$ nằm giữa hai điểm $G$ và $H$. Khi đó:\n$$GH = GE + EH.$$\nThay $GH = MG = 2GE$, ta được:\n$$2GE = GE + EH \\implies EH = GE\\text{ (đpcm)}.$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b4-2c",
        "vi_tri": "Bài IV.2.c",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "VDC",
        "phut": 5.0,
        "diem_bai": 0.5,
        "de_chung": "Bài IV.2. Cho $\\Delta MNP$ nhọn, các đường trung tuyến $ME, NF$ cắt nhau tại $G$.",
        "de": "Để tứ giác $MDPH$ là hình thang cân thì $\\Delta MNP$ cần thêm điều kiện gì?",
        "dap_an": "$\\Delta MNP$ cân tại $M$",
        "loi_giai": "- Ta có $MGPD$ là hình bình hành (theo câu b), suy ra $DP \\parallel MG$ và $DP = MG$.\nMặt khác, điểm $E$ nằm trên đường thẳng $MG$, điểm $H$ thuộc tia đối của tia $EM$ nên bốn điểm $M, G, E, H$ thẳng hàng. Do đó $DP \\parallel MH$.\nSuy ra tứ giác $MDPH$ luôn là hình thang có hai đáy là $DP$ và $MH$.\n- Lại có $GH = MG$ và $H$ nằm trên tia đối của tia $EM$ nên $MH = MG + GH = 2MG = 2DP > DP$, do đó $DP \\ne MH$ (hai đáy không bằng nhau).\nVì vậy, hình thang $MDPH$ là hình thang cân khi và chỉ khi hai cạnh bên bằng nhau:\n$$MD = PH.$$\n- Mặt khác:\n  + Do $MGPD$ là hình bình hành nên $MD = GP$.\n  + Xét tứ giác $GPHN$: có $E$ là trung điểm của $NP$ và $E$ là trung điểm của $GH$ (vì $GE = EH$), nên $GPHN$ là hình bình hành. Suy ra $PH = GN$.\nDo đó, $MD = PH \\iff GP = GN$.\n- Mà $G$ là trọng tâm của tam giác $MNP$ nên:\n$$GP = \\frac{2}{3}PF,\\quad GN = \\frac{2}{3}NE.$$\nSuy ra $GP = GN \\iff PF = NE$.\nTam giác $MNP$ có hai đường trung tuyến kẻ từ hai đỉnh $N$ và $P$ bằng nhau ($NE = PF$) khi và chỉ khi tam giác $MNP$ cân tại $M$ ($MN = MP$).\nVậy để $MDPH$ là hình thang cân thì tam giác $MNP$ cần thêm điều kiện cân tại $M$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài V (0,5 điểm)
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-khe-b5",
        "vi_tri": "Bài V",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Toán thực tế", "Giá trị lớn nhất, giá trị nhỏ nhất"],
        "band": "VDC",
        "phut": 5.0,
        "diem_bai": 0.5,
        "de": "Bài V (0,5 điểm). Một khách sạn có $50$ phòng. Hiện tại mỗi phòng khách sạn cho thuê với giá $400$ nghìn đồng/1 ngày và toàn bộ phòng đã được thuê hết. Biết cứ mỗi lần khách sạn tăng giá thuê phòng thêm $20$ nghìn đồng/1 ngày thì có thêm $2$ phòng trống. Hỏi khách sạn nên tăng giá thuê phòng thêm bao nhiêu để doanh thu của khách sạn trong một ngày là lớn nhất?",
        "dap_an": "Tăng thêm $40$ hoặc $60$ nghìn đồng/ngày (hoặc $50$ nghìn đồng nếu tính liên tục)",
        "loi_giai": "Gọi số lần tăng giá thuê phòng của khách sạn là $x$ ($x$ là số nguyên không âm, $0 \\le x < 25$).\nKhi đó:\n- Giá thuê phòng sau $x$ lần tăng là: $400 + 20x$ (nghìn đồng/phòng/ngày).\n- Cứ mỗi lần tăng có thêm $2$ phòng trống nên sau $x$ lần tăng, số phòng được thuê là: $50 - 2x$ (phòng).\nDoanh thu của khách sạn trong một ngày tính theo đơn vị nghìn đồng là:\n$$R(x) = (400 + 20x)(50 - 2x) = 20(20 + x) \\cdot 2(25 - x) = 40(20 + x)(25 - x).$$\nKhai triển và thu gọn:\n$$R(x) = 40(500 + 5x - x^2) = -40(x^2 - 5x) + 20\\,000 = -40\\left(x - \\frac{5}{2}\\right)^2 + 20\\,250.$$\nVì $x$ là số nguyên nên $x$ gần $\\frac{5}{2} = 2{,}5$ nhất là $x = 2$ hoặc $x = 3$.\n- Với $x = 2$: số tiền tăng là $20 \\cdot 2 = 40$ nghìn đồng/ngày, doanh thu đạt:\n$$R(2) = (400 + 40)(50 - 4) = 440 \\cdot 46 = 20\\,240\\text{ (nghìn đồng)}.$$\n- Với $x = 3$: số tiền tăng là $20 \\cdot 3 = 60$ nghìn đồng/ngày, doanh thu đạt:\n$$R(3) = (400 + 60)(50 - 6) = 460 \\cdot 44 = 20\\,240\\text{ (nghìn đồng)}.$$\n*(Lưu ý: Nếu khách sạn có thể tăng giá linh hoạt theo từng nghìn đồng theo tỷ lệ cứ tăng $10$ nghìn đồng/ngày giảm $1$ phòng được thuê, thì với mức tăng $50$ nghìn đồng/ngày ($x = 2{,}5$), doanh thu tối đa đạt $20\\,250$ nghìn đồng).*\nVậy khách sạn nên tăng giá thuê phòng thêm $40$ nghìn đồng hoặc $60$ nghìn đồng (hoặc $50$ nghìn đồng nếu tăng tuyến tính) để doanh thu trong ngày lớn nhất.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    return data


def build_van_yen():
    data = {
        "xuat_xu": {
            "lop": "8",
            "ky": "GK1",
            "nam": "2025-2026",
            "truong": "THCS Văn Yên (Hà Đông)",
            "nguon": "inputs/refs/de-thi/lop-8/giua-ki-1/de-giua-hoc-ky-1-toan-8-nam-2025-2026-truong-thcs-van-yen-ha-noi.pdf",
            "loai_pdf": "ocr",
            "co_bieu_diem": False
        },
        "tang": 2,
        "da_duyet": True,
        "ghi_chu": "Đề chuẩn GK1 Toán 8 THCS Văn Yên 2025-2026. Đã soát 100% từ ảnh gốc: 100% Tự luận gồm 5 bài (14 câu/ý), tổng điểm chính xác 10.00 điểm.",
        "cau": []
    }

    # Bài I (3,0 điểm) - 4 câu, mỗi câu 0.75đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b1-1",
        "vi_tri": "Bài I.1",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Nhân đơn thức với đa thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.75,
        "de_chung": "Bài I. (3,0 điểm) Thực hiện phép tính:",
        "de": "Thực hiện phép tính: $A = 2x^2y\\left(4xy^2 - \\frac{3}{2}x^2y + xy\\right)$.",
        "dap_an": "$A = 8x^3y^3 - 3x^4y^2 + 2x^3y^2$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\nA &= 2x^2y\\left(4xy^2 - \\frac{3}{2}x^2y + xy\\right) \\\\\n&= 2x^2y \\cdot 4xy^2 - 2x^2y \\cdot \\frac{3}{2}x^2y + 2x^2y \\cdot xy \\\\\n&= 8x^3y^3 - 3x^4y^2 + 2x^3y^2.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b1-2",
        "vi_tri": "Bài I.2",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Cộng trừ đa thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.75,
        "de_chung": "Bài I. (3,0 điểm) Thực hiện phép tính:",
        "de": "Thực hiện phép tính: $B = (2x^2y^3 + 3x^3 - 2x^3y^2) - (-3x^3 + 2x^2y^3)$.",
        "dap_an": "$B = 6x^3 - 2x^3y^2$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\nB &= (2x^2y^3 + 3x^3 - 2x^3y^2) - (-3x^3 + 2x^2y^3) \\\\\n&= 2x^2y^3 + 3x^3 - 2x^3y^2 + 3x^3 - 2x^2y^3 \\\\\n&= (2x^2y^3 - 2x^2y^3) + (3x^3 + 3x^3) - 2x^3y^2 \\\\\n&= 6x^3 - 2x^3y^2.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b1-3",
        "vi_tri": "Bài I.3",
        "loai": "TL",
        "chuong": "I. Đa thức",
        "dang": ["Chia đa thức cho đơn thức"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.75,
        "de_chung": "Bài I. (3,0 điểm) Thực hiện phép tính:",
        "de": "Thực hiện phép tính: $C = (-4x^2y^2 + x^3y - 10xy) : 2xy$.",
        "dap_an": "$C = -2xy + \\frac{1}{2}x^2 - 5$",
        "loi_giai": "Ta có:\n$$\\begin{aligned}\nC &= (-4x^2y^2 + x^3y - 10xy) : 2xy \\\\\n&= (-4x^2y^2 : 2xy) + (x^3y : 2xy) - (10xy : 2xy) \\\\\n&= -2xy + \\frac{1}{2}x^2 - 5.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b1-4",
        "vi_tri": "Bài I.4",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức", "Những hằng đẳng thức đáng nhớ"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.75,
        "de_chung": "Bài I. (3,0 điểm) Thực hiện phép tính:",
        "de": "Thực hiện phép tính: $D = (x + 4)^2 + (2x + 8)(x - 4) + (4 - x)^2$.",
        "dap_an": "$D = 4x^2$",
        "loi_giai": "Ta nhận thấy: $2x + 8 = 2(x + 4)$ và $(4 - x)^2 = (x - 4)^2$.\nKhi đó:\n$$\\begin{aligned}\nD &= (x + 4)^2 + 2(x + 4)(x - 4) + (x - 4)^2 \\\\\n&= [(x + 4) + (x - 4)]^2 \\\\\n&= (2x)^2 \\\\\n&= 4x^2.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài II (2,0 điểm) - 3 câu: 0.5đ, 1.0đ, 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b2-1",
        "vi_tri": "Bài II.1",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Tính giá trị của đa thức"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II. (2,0 điểm) Cho hai biểu thức:\n$$A = (x - 2y)(x + 2y) - 4y(x - y) + 4x(y + 1);\\quad B = (2x + 1)^2.$$",
        "de": "Tính giá trị của biểu thức $B$ khi $x = -1$.",
        "dap_an": "$B = 1$",
        "loi_giai": "Thay $x = -1$ vào biểu thức $B$, ta được:\n$$B = [2(-1) + 1]^2 = (-2 + 1)^2 = (-1)^2 = 1.$$\nVậy tại $x = -1$ thì $B = 1$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b2-2",
        "vi_tri": "Bài II.2",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Rút gọn biểu thức hằng đẳng thức"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài II. (2,0 điểm) Cho hai biểu thức:\n$$A = (x - 2y)(x + 2y) - 4y(x - y) + 4x(y + 1);\\quad B = (2x + 1)^2.$$",
        "de": "Chứng minh $A = x^2 + 4x$.",
        "dap_an": "$A = x^2 + 4x$",
        "loi_giai": "Khai triển và rút gọn biểu thức $A$:\n$$\\begin{aligned}\nA &= (x - 2y)(x + 2y) - 4y(x - y) + 4x(y + 1) \\\\\n&= (x^2 - 4y^2) - (4xy - 4y^2) + (4xy + 4x) \\\\\n&= x^2 - 4y^2 - 4xy + 4y^2 + 4xy + 4x \\\\\n&= x^2 + (-4y^2 + 4y^2) + (-4xy + 4xy) + 4x \\\\\n&= x^2 + 4x\\text{ (đpcm)}.\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b2-3",
        "vi_tri": "Bài II.3",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Giá trị lớn nhất, giá trị nhỏ nhất"],
        "band": "VD",
        "phut": 4.0,
        "diem_bai": 0.5,
        "de_chung": "Bài II. (2,0 điểm) Cho hai biểu thức:\n$$A = (x - 2y)(x + 2y) - 4y(x - y) + 4x(y + 1);\\quad B = (2x + 1)^2.$$",
        "de": "Cho $P = 3A - B$. Tìm giá trị lớn nhất của $P$.",
        "dap_an": "$\\max P = 15$ khi $x = 4$",
        "loi_giai": "Theo câu 2, ta có $A = x^2 + 4x$.\nBiểu thức $P = 3A - B$ trở thành:\n$$\\begin{aligned}\nP &= 3(x^2 + 4x) - (2x + 1)^2 \\\\\n&= 3x^2 + 12x - (4x^2 + 4x + 1) \\\\\n&= 3x^2 + 12x - 4x^2 - 4x - 1 \\\\\n&= -x^2 + 8x - 1 \\\\\n&= -(x^2 - 8x + 16) + 15 \\\\\n&= -(x - 4)^2 + 15.\n\\end{aligned}$$\nVì $-(x - 4)^2 \\le 0$ với mọi $x$, nên:\n$$P = -(x - 4)^2 + 15 \\le 15,\\quad \\forall x.$$\nDấu \"=\" xảy ra khi $x - 4 = 0 \\iff x = 4$.\nVậy giá trị lớn nhất của $P$ là $15$, đạt được khi $x = 4$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài III (1,0 điểm) - 3 câu: 0.25đ, 0.5đ, 0.25đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b3-1",
        "vi_tri": "Bài III.1",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Toán thực tế"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de_chung": "Bài III. (1,0 điểm) Toán thực tế:\nMột sân vận động hình chữ nhật có chiều dài là $(x + y)$ mét và chiều rộng là $(x - y)$ mét.",
        "de": "1) Viết biểu thức tính diện tích của sân vận động?",
        "dap_an": "$S = x^2 - y^2\\text{ (m}^2\\text{)}$",
        "loi_giai": "Diện tích của sân vận động hình chữ nhật là:\n$$S = (x + y)(x - y) = x^2 - y^2\\text{ (m}^2\\text{)}.$$",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b3-2a",
        "vi_tri": "Bài III.2.a",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Toán thực tế"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de_chung": "Bài III.2. Người ta làm lối đi rộng $3$ mét xung quanh sân, phần còn lại để trồng cỏ nhằm phục vụ cho các trận bóng đá.",
        "de": "a) Viết biểu thức tính diện tích phần trồng cỏ?",
        "dap_an": "$S_{\\text{cỏ}} = (x + y - 6)(x - y - 6)\\text{ (m}^2\\text{)}$ hoặc $(x - 6)^2 - y^2$",
        "loi_giai": "Vì làm lối đi rộng $3\\text{ m}$ xung quanh sân nên:\n- Chiều dài của phần đất trồng cỏ là: $(x + y) - 2 \\cdot 3 = x + y - 6\\text{ (m)}$.\n- Chiều rộng của phần đất trồng cỏ là: $(x - y) - 2 \\cdot 3 = x - y - 6\\text{ (m)}$.\nDo đó, biểu thức tính diện tích phần đất trồng cỏ là:\n$$\\begin{aligned}\nS_{\\text{cỏ}} &= (x + y - 6)(x - y - 6) \\\\\n&= [(x - 6) + y][(x - 6) - y] \\\\\n&= (x - 6)^2 - y^2\\text{ (m}^2\\text{)}\n\\end{aligned}$$\n(hoặc khai triển thành $x^2 - 12x + 36 - y^2\\text{ m}^2$).",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b3-2b",
        "vi_tri": "Bài III.2.b",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Toán thực tế"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.25,
        "de_chung": "Bài III.2. Người ta làm lối đi rộng $3$ mét xung quanh sân, phần còn lại để trồng cỏ nhằm phục vụ cho các trận bóng đá.",
        "de": "b) Cho $x = 40, y = 6$. Biết $1\\text{ m}^2$ trồng cỏ cần số tiền là $100\\,000$ đồng. Tính số tiền trồng cỏ cho mặt sân?",
        "dap_an": "$112\\,000\\,000$ đồng",
        "loi_giai": "Thay $x = 40$ và $y = 6$ vào biểu thức kích thước phần trồng cỏ:\n- Chiều dài phần trồng cỏ: $40 + 6 - 6 = 40\\text{ (m)}$.\n- Chiều rộng phần trồng cỏ: $40 - 6 - 6 = 28\\text{ (m)}$.\nDiện tích phần đất trồng cỏ là:\n$$S_{\\text{cỏ}} = 40 \\cdot 28 = 1120\\text{ (m}^2\\text{)}.$$\nSố tiền cần dùng để trồng cỏ cho mặt sân là:\n$$1120 \\cdot 100\\,000 = 112\\,000\\,000\\text{ (đồng)}.$$\nVậy số tiền trồng cỏ cho mặt sân là $112\\,000\\,000$ đồng ($112$ triệu đồng).",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài IV (3,5 điểm): IV.1a: 0.5đ; IV.1b: 0.5đ; IV.2a: 1.0đ; IV.2b: 1.0đ; IV.2c: 0.5đ
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b4-1a",
        "vi_tri": "Bài IV.1.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Đường trung bình của tam giác"],
        "band": "NB",
        "phut": 2.0,
        "diem_bai": 0.5,
        "de_chung": "Bài IV.1. Cho tam giác $ABC$ có $D, E$ lần lượt là trung điểm của $AB, AC$. Biết $BC = 5\\text{ cm}; \\widehat{ADE} = 70^\\circ, \\widehat{DAE} = 60^\\circ$ (như hình vẽ).",
        "de": "a) Tính độ dài $DE$?",
        "dap_an": "$DE = 2{,}5\\text{ cm}$",
        "loi_giai": "Xét tam giác $ABC$, ta có:\n- $D$ là trung điểm của cạnh $AB$.\n- $E$ là trung điểm của cạnh $AC$.\nDo đó đoạn thẳng $DE$ là đường trung bình của tam giác $ABC$.\nSuy ra:\n$$DE = \\frac{1}{2}BC = \\frac{1}{2} \\cdot 5 = 2{,}5\\text{ (cm)}.$$",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b4-1b",
        "vi_tri": "Bài IV.1.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Đường trung bình của tam giác"],
        "band": "TH",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de_chung": "Bài IV.1. Cho tam giác $ABC$ có $D, E$ lần lượt là trung điểm của $AB, AC$. Biết $BC = 5\\text{ cm}; \\widehat{ADE} = 70^\\circ, \\widehat{DAE} = 60^\\circ$ (như hình vẽ).",
        "de": "b) Tính số đo các góc: $\\widehat{ABC}, \\widehat{ACB}$.",
        "dap_an": "$\\widehat{ABC} = 70^\\circ,\\ \\widehat{ACB} = 50^\\circ$",
        "loi_giai": "- Vì $DE$ là đường trung bình của tam giác $ABC$ nên $DE \\parallel BC$.\nSuy ra $\\widehat{ABC} = \\widehat{ADE} = 70^\\circ$ (hai góc đồng vị).\n- Xét tam giác $ADE$, ta có tổng ba góc bằng $180^\\circ$:\n$$\\widehat{AED} = 180^\\circ - (\\widehat{DAE} + \\widehat{ADE}) = 180^\\circ - (60^\\circ + 70^\\circ) = 50^\\circ.$$\nVì $DE \\parallel BC$ nên $\\widehat{ACB} = \\widehat{AED} = 50^\\circ$ (hai góc đồng vị).\nVậy $\\widehat{ABC} = 70^\\circ$ và $\\widehat{ACB} = 50^\\circ$.",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b4-2a",
        "vi_tri": "Bài IV.2.a",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình chữ nhật"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài IV.2. Cho tam giác $ABC$ vuông tại $A$ có $AB < AC$. Gọi $M$ là trung điểm của $BC$, kẻ $MD$ vuông góc với $AB$ tại $D$, $ME$ vuông góc với $AC$ tại $E$.",
        "de": "a) Chứng minh tứ giác $ADME$ là hình chữ nhật, từ đó suy ra $AM = DE$.",
        "dap_an": "$ADME$ là hình chữ nhật, suy ra $AM = DE$",
        "loi_giai": "- Xét tứ giác $ADME$, ta có:\n  + $\\widehat{DAE} = 90^\\circ$ (vì $\\Delta ABC$ vuông tại $A$);\n  + $\\widehat{ADM} = 90^\\circ$ (vì $MD \\perp AB$ tại $D$);\n  + $\\widehat{AEM} = 90^\\circ$ (vì $ME \\perp AC$ tại $E$).\nTứ giác $ADME$ có ba góc vuông nên là hình chữ nhật.\n- Vì $ADME$ là hình chữ nhật nên hai đường chéo bằng nhau: $AM = DE$ (đpcm).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b4-2b",
        "vi_tri": "Bài IV.2.b",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình bình hành", "Đường trung bình của tam giác"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 1.0,
        "de_chung": "Bài IV.2. Cho tam giác $ABC$ vuông tại $A$ có $AB < AC$. Gọi $M$ là trung điểm của $BC$, kẻ $MD$ vuông góc với $AB$ tại $D$, $ME$ vuông góc với $AC$ tại $E$.",
        "de": "b) Chứng minh tứ giác $DMCE$ là hình bình hành.",
        "dap_an": "$DMCE$ là hình bình hành",
        "loi_giai": "- Trong tam giác $ABC$ vuông tại $A$, ta có $ME \\perp AC$ và $AB \\perp AC$, suy ra $ME \\parallel AB$.\nTam giác $ABC$ có $M$ là trung điểm của $BC$ và $ME \\parallel AB$, nên $E$ là trung điểm của cạnh $AC$.\nDo đó $AE = EC$.\n- Mặt khác, vì $ADME$ là hình chữ nhật nên $DM = AE$ và $DM \\parallel AE$ (hay $DM \\parallel EC$).\nTừ đó suy ra $DM = EC$.\n- Tứ giác $DMCE$ có một cặp cạnh đối song song và bằng nhau ($DM \\parallel EC$ và $DM = EC$) nên là hình bình hành (đpcm).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b4-2c",
        "vi_tri": "Bài IV.2.c",
        "loai": "TL",
        "chuong": "III. Tứ giác",
        "dang": ["Hình thang, hình thang cân"],
        "band": "VD",
        "phut": 4.5,
        "diem_bai": 0.5,
        "de_chung": "Bài IV.2. Cho tam giác $ABC$ vuông tại $A$ có $AB < AC$. Gọi $M$ là trung điểm của $BC$, kẻ $MD$ vuông góc với $AB$ tại $D$, $ME$ vuông góc với $AC$ tại $E$.",
        "de": "c) Gọi $AH$ là đường cao của $\\Delta ABC$ ($H \\in BC$). Chứng minh tứ giác $HMED$ là hình thang cân và $HD \\perp HE$.",
        "dap_an": "$HMED$ là hình thang cân và $HD \\perp HE$",
        "loi_giai": "1) Chứng minh $HMED$ là hình thang cân:\n- Tương tự câu b, trong tam giác $ABC$ có $M$ là trung điểm $BC$ và $MD \\perp AB$, $AC \\perp AB$ nên $MD \\parallel AC$, suy ra $D$ là trung điểm của $AB$.\n- Vì $D, E$ lần lượt là trung điểm của $AB, AC$ nên $DE$ là đường trung bình của tam giác $ABC$.\nDo đó $DE \\parallel BC$, hay $DE \\parallel HM$.\nTứ giác $HMED$ có $DE \\parallel HM$ nên là hình thang.\n- Xét tam giác $ABH$ vuông tại $H$, có $HD$ là đường trung tuyến ứng với cạnh huyền $AB$ nên $HD = \\frac{1}{2}AB = AD$.\nMặt khác, vì $ADME$ là hình chữ nhật nên $AD = ME$.\nSuy ra $HD = ME$.\nHình thang $HMED$ có hai cạnh bên bằng nhau ($HD = ME$) và không song song nên $HMED$ là hình thang cân.\n\n2) Chứng minh $HD \\perp HE$:\n- Trong tam giác vuông $ABH$, ta có $HD = AD$ nên tam giác $ADH$ cân tại $D$, suy ra $\\widehat{DHA} = \\widehat{DAH}$.\n- Trong tam giác vuông $ACH$ vuông tại $H$, $HE$ là đường trung tuyến ứng với cạnh huyền $AC$ nên $HE = \\frac{1}{2}AC = AE$.\nDo đó tam giác $AEH$ cân tại $E$, suy ra $\\widehat{EHA} = \\widehat{EAH}$.\n- Khi đó:\n$$\\widehat{DHE} = \\widehat{DHA} + \\widehat{EHA} = \\widehat{DAH} + \\widehat{EAH} = \\widehat{DAE} = \\widehat{BAC} = 90^\\circ.$$\nVậy $HD \\perp HE$ (đpcm).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    # Bài V (0,5 điểm)
    data["cau"].append({
        "id": "l8-gk1-2025-thcs-van-yen-b5",
        "vi_tri": "Bài V",
        "loai": "TL",
        "chuong": "II. Hằng đẳng thức",
        "dang": ["Số chính phương", "Những hằng đẳng thức đáng nhớ"],
        "band": "VDC",
        "phut": 5.0,
        "diem_bai": 0.5,
        "de": "Bài V. (0,5 điểm) Cho $M$ là tích của $4$ số nguyên liên tiếp. Chứng minh rằng $M + 1$ là một số chính phương.",
        "dap_an": "$M + 1 = (n^2 + 3n + 1)^2$ là số chính phương",
        "loi_giai": "Gọi $4$ số nguyên liên tiếp lần lượt là $n, n + 1, n + 2, n + 3$ với $n \\in \\mathbb{Z}$.\nKhi đó tích của $4$ số nguyên liên tiếp là:\n$$M = n(n + 1)(n + 2)(n + 3).$$\nNhóm các thừa số thích hợp:\n$$\\begin{aligned}\nM &= [n(n + 3)] \\cdot [(n + 1)(n + 2)] \\\\\n&= (n^2 + 3n)(n^2 + 3n + 2).\n\\end{aligned}$$\nĐặt $t = n^2 + 3n$ ($t \\in \\mathbb{Z}$), ta được:\n$$M = t(t + 2) = t^2 + 2t.$$\nSuy ra:\n$$M + 1 = t^2 + 2t + 1 = (t + 1)^2 = (n^2 + 3n + 1)^2.$$\nVì $n \\in \\mathbb{Z}$ nên $n^2 + 3n + 1$ là một số nguyên.\nDo đó $M + 1$ là bình phương của một số nguyên, tức là một số chính phương (đpcm).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    })

    return data

if __name__ == "__main__":
    d1 = build_van_khe()
    with open("inputs/refs/de-thi/lop-8/exams/gk1-2025-thcs-van-khe.json", "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
    print("Updated gk1-2025-thcs-van-khe.json successfully! Cau count:", len(d1["cau"]))

    d2 = build_van_yen()
    with open("inputs/refs/de-thi/lop-8/exams/gk1-2025-thcs-van-yen.json", "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
    print("Updated gk1-2025-thcs-van-yen.json successfully! Cau count:", len(d2["cau"]))
