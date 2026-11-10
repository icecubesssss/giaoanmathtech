import json

with open('inputs/refs/de-thi/lop-8/exams/ck2-2025-thcs-tam-hung.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

slug = "ck2-2025-thcs-tam-hung"

cau_list = [
    # PHẦN I: TRẮC NGHIỆM (2,0 điểm) - 8 câu x 0.25đ
    {
        "id": f"l8-{slug}-tn-c1",
        "vi_tri": "Câu 1",
        "loai": "TN",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Nhận biết phương trình bậc nhất một ẩn"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Trong các phương trình sau, phương trình bậc nhất một ẩn là:\nA. $x^2 + x = 0$\nB. $x - 3 = 0$\nC. $\\frac{1}{x} - x = \\frac{x}{x+2}$\nD. $2x - 3y = 0$",
        "dap_an": "B",
        "loi_giai": "Phương trình bậc nhất một ẩn có dạng $ax + b = 0$ ($a \\neq 0$). Do đó $x - 3 = 0$ là phương trình bậc nhất một ẩn. Chọn B.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c2",
        "vi_tri": "Câu 2",
        "loai": "TN",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Giải phương trình bậc nhất một ẩn"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Phương trình $4x - 1 = 7$ có nghiệm là:\nA. $x = 2$\nB. $x = 3$\nC. $x = \\frac{2}{3}$\nD. $x = \\frac{3}{2}$",
        "dap_an": "A",
        "loi_giai": "Ta có $4x - 1 = 7 \\Leftrightarrow 4x = 8 \\Leftrightarrow x = 2$. Chọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c3",
        "vi_tri": "Câu 3",
        "loai": "TN",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Tìm tham số để phương trình nhận giá trị cho trước làm nghiệm"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Giá trị của $m$ để phương trình $2x - m = x + 1$ có nghiệm $x = -2$ là:\nA. $m = 1$\nB. $m = -1$\nC. $m = -2$\nD. $m = -3$",
        "dap_an": "D",
        "loi_giai": "Thay $x = -2$ vào phương trình, ta được:\n$2(-2) - m = -2 + 1 \\Leftrightarrow -4 - m = -1 \\Leftrightarrow m = -3$. Chọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c4",
        "vi_tri": "Câu 4",
        "loai": "TN",
        "chuong": "IX. Một số yếu tố xác suất",
        "dang": ["Tính xác suất của biến cố ngẫu nhiên"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Lớp 8C có 40 bạn, trong đó có 19 nữ. Cô giáo chủ nhiệm chọn ngẫu nhiên một bạn làm lớp trưởng. Xác suất cô chọn trúng một bạn nam là:\nA. $\\frac{19}{40}$\nB. $\\frac{19}{59}$\nC. $\\frac{21}{61}$\nD. $\\frac{21}{40}$",
        "dap_an": "D",
        "loi_giai": "Số học sinh nam của lớp 8C là $40 - 19 = 21$ bạn.\nXác suất chọn trúng một bạn nam là $\\frac{21}{40}$. Chọn D.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c5",
        "vi_tri": "Câu 5",
        "loai": "TN",
        "chuong": "VIII. Hình đồng dạng",
        "dang": ["Nhận biết hình đồng dạng phối cảnh"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Trong các hình vẽ đã cho, hình đồng dạng phối cảnh là hình nào?\nA. Hình A\nB. Hình B\nC. Hình C\nD. Hình D",
        "dap_an": "A",
        "loi_giai": "Hình A biểu diễn cặp hình đồng dạng phối cảnh (tâm phối cảnh). Chọn A.",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c6",
        "vi_tri": "Câu 6",
        "loai": "TN",
        "chuong": "VIII. Hình đồng dạng",
        "dang": ["Điều kiện đồng dạng của hai tam giác"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Nếu $\\Delta ABC$ và $\\Delta FED$ có $\\widehat{A} = \\widehat{F}$, cần thêm điều kiện gì dưới đây để $\\Delta ABC \\backsim \\Delta FED$?\nA. $\\widehat{B} = \\widehat{E}$\nB. $\\widehat{C} = \\widehat{E}$\nC. $\\widehat{B} = \\widehat{D}$\nD. $\\widehat{C} = \\widehat{F}$",
        "dap_an": "A",
        "loi_giai": "Theo thứ tự đỉnh tương ứng của hai tam giác đồng dạng $\\Delta ABC \\backsim \\Delta FED$, đỉnh $A$ tương ứng với $F$, đỉnh $B$ tương ứng với $E$, đỉnh $C$ tương ứng với $D$.\nDo đó khi đã có $\\widehat{A} = \\widehat{F}$, cần thêm điều kiện $\\widehat{B} = \\widehat{E}$ (hoặc $\\widehat{C} = \\widehat{D}$). Chọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c7",
        "vi_tri": "Câu 7",
        "loai": "TN",
        "chuong": "X. Một số hình khối trong thực tiễn",
        "dang": ["Nhận biết các yếu tố của hình chóp tứ giác đều"],
        "band": "NB",
        "phut": 1.5,
        "diem_bai": 0.25,
        "de": "Hình chóp tứ giác đều có các mặt bên là:\nA. Tam giác cân\nB. Tam giác đều\nC. Tam giác vuông\nD. Tam giác vuông cân",
        "dap_an": "A",
        "loi_giai": "Hình chóp tứ giác đều có đáy là hình vuông và các mặt bên là các tam giác cân bằng nhau. Chọn A.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tn-c8",
        "vi_tri": "Câu 8",
        "loai": "TN",
        "chuong": "X. Một số hình khối trong thực tiễn",
        "dang": ["Tính thể tích hình chóp tứ giác đều"],
        "band": "TH",
        "phut": 2.0,
        "diem_bai": 0.25,
        "de": "Thể tích của hình chóp tứ giác đều có chiều cao $6\\text{ cm}$, cạnh đáy $4\\text{ cm}$ là:\nA. $32\\text{ cm}^2$\nB. $24\\text{ cm}^3$\nC. $32\\text{ cm}^3$\nD. $96\\text{ cm}^3$",
        "dap_an": "C",
        "loi_giai": "Diện tích đáy hình vuông là $S = 4^2 = 16\\text{ cm}^2$.\nThể tích hình chóp tứ giác đều là: $V = \\frac{1}{3} S \\cdot h = \\frac{1}{3} \\cdot 16 \\cdot 6 = 32\\text{ cm}^3$. Chọn C.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },

    # PHẦN II: TỰ LUẬN (8,0 điểm)
    # Bài I (1.5 điểm)
    {
        "id": f"l8-{slug}-tl-b1-1",
        "vi_tri": "Bài I.1",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tính giá trị của phân thức đại số"],
        "band": "NB",
        "phut": 2.5,
        "diem_bai": 0.5,
        "de": "Cho hai biểu thức $A = \\frac{1}{x+2} - \\frac{2x}{4-x^2} + \\frac{3}{x-2}$ và $B = \\frac{x+2}{3x+2}$ với $x \\neq 2; x \\neq -2; x \\neq -\\frac{2}{3}$.\n1) Tính giá trị của biểu thức $B$ khi $x = -3$.",
        "dap_an": "B = 1/7",
        "loi_giai": "Thay $x = -3$ (thỏa mãn điều kiện xác định) vào biểu thức $B$, ta có:\n$$B = \\frac{-3 + 2}{3 \\cdot (-3) + 2} = \\frac{-1}{-9 + 2} = \\frac{-1}{-7} = \\frac{1}{7}$$\nVậy $B = \\frac{1}{7}$ khi $x = -3$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b1-2",
        "vi_tri": "Bài I.2",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Rút gọn biểu thức chứa phân thức đại số"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 0.5,
        "de": "Cho hai biểu thức $A$ và $B$ như trên.\n2) Rút gọn biểu thức $M = A \\cdot B$.",
        "dap_an": "M = 2/(x-2)",
        "loi_giai": "Với $x \\neq \\pm 2; x \\neq -\\frac{2}{3}$, ta có:\n$$\\begin{aligned} A &= \\frac{1}{x+2} - \\frac{2x}{4-x^2} + \\frac{3}{x-2} = \\frac{1}{x+2} + \\frac{2x}{x^2-4} + \\frac{3}{x-2} \\\\ &= \\frac{x-2}{(x-2)(x+2)} + \\frac{2x}{(x-2)(x+2)} + \\frac{3(x+2)}{(x-2)(x+2)} \\\\ &= \\frac{x - 2 + 2x + 3x + 6}{(x-2)(x+2)} = \\frac{6x + 4}{(x-2)(x+2)} = \\frac{2(3x+2)}{(x-2)(x+2)} \\end{aligned}$$\nKhi đó:\n$$M = A \\cdot B = \\frac{2(3x+2)}{(x-2)(x+2)} \\cdot \\frac{x+2}{3x+2} = \\frac{2}{x-2}$$",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b1-3",
        "vi_tri": "Bài I.3",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tìm giá trị lớn nhất, nhỏ nhất của biểu thức"],
        "band": "VD",
        "phut": 4.5,
        "diem_bai": 0.5,
        "de": "3) Tìm giá trị nhỏ nhất của biểu thức $N = M \\cdot (x^3 - x^2 - 2x)$.",
        "dap_an": "min N = -1/2 khi x = -1/2",
        "loi_giai": "Ta có:\n$$x^3 - x^2 - 2x = x(x^2 - x - 2) = x(x - 2)(x + 1)$$\nSuy ra:\n$$N = M \\cdot (x^3 - x^2 - 2x) = \\frac{2}{x-2} \\cdot x(x-2)(x+1) = 2x(x+1) = 2x^2 + 2x$$\nBiến đổi:\n$$N = 2\\left(x^2 + x + \\frac{1}{4}\\right) - \\frac{1}{2} = 2\\left(x + \\frac{1}{2}\\right)^2 - \\frac{1}{2}$$\nVì $2\\left(x + \\frac{1}{2}\\right)^2 \\ge 0$ với mọi $x$ nên $N \\ge -\\frac{1}{2}$.\nDấu \"=\" xảy ra khi $x + \\frac{1}{2} = 0 \\Leftrightarrow x = -\\frac{1}{2}$ (thỏa mãn ĐKXĐ: $x \\neq \\pm 2; x \\neq -\\frac{2}{3}$).\nVậy giá trị nhỏ nhất của biểu thức $N$ là $-\\frac{1}{2}$ khi $x = -\\frac{1}{2}$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },

    # Bài II (1.5 điểm)
    {
        "id": f"l8-{slug}-tl-b2-1",
        "vi_tri": "Bài II.1",
        "loai": "TL",
        "chuong": "IX. Một số yếu tố xác suất",
        "dang": ["Tính xác suất của biến cố trong trò chơi quay đĩa"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de": "1. Cho một đĩa tròn được chia làm 8 phần bằng nhau và ghi các số tự nhiên từ 1 đến 8. Quay đĩa tròn 1 lần. Tính xác suất của biến cố $A$: \"Chiếc kim chỉ vào hình quạt ghi số chia cho 4 dư 1\".",
        "dap_an": "P(A) = 1/4",
        "loi_giai": "Quay đĩa tròn 1 lần có 8 kết quả có thể xảy ra đối với số ghi trên hình quạt mà chiếc kim chỉ vào là: $\\{1; 2; 3; 4; 5; 6; 7; 8\\}$. Các kết quả này là đồng khả năng.\nTrong các số trên, các số chia cho 4 dư 1 là 1 và 5, nên có 2 kết quả thuận lợi cho biến cố $A$.\nXác suất của biến cố $A$ là:\n$$P(A) = \\frac{2}{8} = \\frac{1}{4}$$",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b2-2a",
        "vi_tri": "Bài II.2a",
        "loai": "TL",
        "chuong": "VI. Hàm số và đồ thị",
        "dang": ["Đường thẳng đi qua điểm cho trước"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de": "2. Cho đường thẳng $(d): y = (m+4)x - m + 6$ ($m$ là tham số và $m \\neq -4$).\na) Tìm $m$ để đường thẳng $(d)$ đi qua điểm $A(-1; 2)$.",
        "dap_an": "m = 0",
        "loi_giai": "Đường thẳng $(d)$ đi qua điểm $A(-1; 2)$ khi và chỉ khi:\n$$(m+4)(-1) - m + 6 = 2 \\Leftrightarrow -m - 4 - m + 6 = 2 \\Leftrightarrow -2m + 2 = 2 \\Leftrightarrow -2m = 0 \\Leftrightarrow m = 0$$\nGiá trị $m = 0$ thỏa mãn điều kiện $m \\neq -4$.\nVậy $m = 0$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b2-2b",
        "vi_tri": "Bài II.2b",
        "loai": "TL",
        "chuong": "VI. Hàm số và đồ thị",
        "dang": ["Hai đường thẳng song song"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de": "b) Tìm $m$ để đường thẳng $(d)$ song song với đường thẳng $y = -2x + 3$.",
        "dap_an": "m = -6",
        "loi_giai": "Để đường thẳng $(d): y = (m+4)x - m + 6$ song song với đường thẳng $y = -2x + 3$, điều kiện là:\n$$\\begin{cases} m + 4 = -2 \\\\ -m + 6 \\neq 3 \\end{cases} \\Leftrightarrow \\begin{cases} m = -6 \\\\ -m \\neq -3 \\end{cases} \\Leftrightarrow \\begin{cases} m = -6 \\\\ m \\neq 3 \\end{cases} \\Rightarrow m = -6$$\nGiá trị $m = -6$ thỏa mãn điều kiện $m \\neq -4$.\nVậy $m = -6$.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },

    # Bài III (2.0 điểm)
    {
        "id": f"l8-{slug}-tl-b3-1",
        "vi_tri": "Bài III.1",
        "loai": "TL",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Giải bài toán bằng cách lập phương trình: năng suất lao động"],
        "band": "VD",
        "phut": 5.0,
        "diem_bai": 1.5,
        "de": "1. Một tổ sản xuất theo kế hoạch mỗi ngày phải sản xuất 30 sản phẩm. Do cải tiến kĩ thuật nên thực tế, mỗi ngày tổ đã sản xuất được 40 sản phẩm. Do đó tổ đã hoàn thành trước kế hoạch 3 ngày và còn vượt mức 20 sản phẩm. Hỏi theo kế hoạch tổ đó phải sản xuất bao nhiêu sản phẩm?",
        "dap_an": "420 sản phẩm",
        "loi_giai": "Gọi số sản phẩm tổ phải sản xuất theo kế hoạch là $x$ ($x \\in \\mathbb{N}^*$, sản phẩm).\nThời gian tổ dự định hoàn thành theo kế hoạch là: $\\frac{x}{30}$ (ngày).\nThực tế, tổng số sản phẩm tổ làm được là: $x + 20$ (sản phẩm).\nThời gian thực tế tổ hoàn thành là: $\\frac{x + 20}{40}$ (ngày).\nVì tổ đã hoàn thành trước kế hoạch 3 ngày nên ta có phương trình:\n$$\\frac{x}{30} - \\frac{x + 20}{40} = 3$$\nQuy đồng mẫu số hai vế với mẫu chung là 120:\n$$4x - 3(x + 20) = 360 \\\\ 4x - 3x - 60 = 360 \\\\ x = 420$$\nGiá trị $x = 420$ thỏa mãn điều kiện của ẩn.\nVậy theo kế hoạch, tổ đó phải sản xuất 420 sản phẩm.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b3-2",
        "vi_tri": "Bài III.2",
        "loai": "TL",
        "chuong": "X. Một số hình khối trong thực tiễn",
        "dang": ["Tính diện tích xung quanh của hình chóp tam giác đều"],
        "band": "TH",
        "phut": 3.0,
        "diem_bai": 0.5,
        "de": "2. Một giỏ hoa gỗ mini có dạng hình chóp tam giác đều có độ dài cạnh đáy là $10\\text{ cm}$ và độ dài trung đoạn bằng $20\\text{ cm}$. Tính diện tích xung quanh giỏ hoa gỗ mini đó.",
        "dap_an": "300 cm^2",
        "loi_giai": "Nửa chu vi đáy của hình chóp tam giác đều là:\n$$p = \\frac{10 \\cdot 3}{2} = 15\\text{ (cm)}$$\nDiện tích xung quanh của giỏ hoa gỗ mini hình chóp tam giác đều là:\n$$S_{xq} = p \\cdot d = 15 \\cdot 20 = 300\\text{ (cm}^2\\text{)}$$\nVậy diện tích xung quanh giỏ hoa gỗ mini là $300\\text{ cm}^2$.",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },

    # Bài IV (2.5 điểm)
    {
        "id": f"l8-{slug}-tl-b4-1",
        "vi_tri": "Bài IV.1",
        "loai": "TL",
        "chuong": "VIII. Hình đồng dạng",
        "dang": ["Chứng minh hai tam giác vuông đồng dạng"],
        "band": "TH",
        "phut": 4.0,
        "diem_bai": 0.75,
        "de": "Cho tam giác $ABC$ nhọn ($AB < AC$) có ba đường cao $AD, BE, CF$ cắt nhau tại $H$.\n1) Chứng minh $\\Delta HFB \\backsim \\Delta HEC$.",
        "dap_an": "tam giác HFB đồng dạng tam giác HEC (g.g)",
        "loi_giai": "Xét $\\Delta HFB$ và $\\Delta HEC$, ta có:\n- $\\widehat{HFB} = \\widehat{HEC} = 90^\\circ$ (do $CF \\perp AB$ và $BE \\perp AC$)\n- $\\widehat{FHB} = \\widehat{EHC}$ (hai góc đối đỉnh)\nSuy ra $\\Delta HFB \\backsim \\Delta HEC$ (g.g).",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b4-2",
        "vi_tri": "Bài IV.2",
        "loai": "TL",
        "chuong": "VIII. Hình đồng dạng",
        "dang": ["Chứng minh hệ thức hình học bằng tam giác đồng dạng"],
        "band": "VD",
        "phut": 4.5,
        "diem_bai": 0.75,
        "de": "2) Chứng minh $BH \\cdot BE = BD \\cdot BC$.",
        "dap_an": "BH . BE = BD . BC",
        "loi_giai": "Xét $\\Delta BHD$ và $\\Delta BCE$, ta có:\n- $\\widehat{EBC}$ là góc chung\n- $\\widehat{BDH} = \\widehat{BEC} = 90^\\circ$ (do $AD \\perp BC$ và $BE \\perp AC$)\nSuy ra $\\Delta BHD \\backsim \\Delta BCE$ (g.g).\nDo đó ta có tỉ số đồng dạng:\n$$\\frac{BH}{BC} = \\frac{BD}{BE} \\Rightarrow BH \\cdot BE = BD \\cdot BC\\text{ (đpcm)}.$$",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-tl-b4-3",
        "vi_tri": "Bài IV.3",
        "loai": "TL",
        "chuong": "VIII. Hình đồng dạng",
        "dang": ["Chứng minh hệ thức hình học tổng các tích"],
        "band": "VD",
        "phut": 5.0,
        "diem_bai": 1.0,
        "de": "3) Chứng minh $BH \\cdot BE + CH \\cdot CF = BC^2$.",
        "dap_an": "BH . BE + CH . CF = BC^2",
        "loi_giai": "Xét $\\Delta CHD$ và $\\Delta CBF$, ta có:\n- $\\widehat{FCB}$ là góc chung\n- $\\widehat{CDH} = \\widehat{CFB} = 90^\\circ$ (do $AD \\perp BC$ và $CF \\perp AB$)\nSuy ra $\\Delta CHD \\backsim \\Delta CBF$ (g.g).\nDo đó ta có tỉ số đồng dạng:\n$$\\frac{CH}{CB} = \\frac{CD}{CF} \\Rightarrow CH \\cdot CF = CD \\cdot CB$$\nTừ kết quả câu 2, ta có: $BH \\cdot BE = BD \\cdot BC$.\nCộng từng vế hai hệ thức trên, ta được:\n$$BH \\cdot BE + CH \\cdot CF = BD \\cdot BC + CD \\cdot CB = (BD + CD) \\cdot BC$$\nVì điểm $D$ thuộc đoạn thẳng $BC$ nên $BD + CD = BC$.\nDo đó:\n$$BH \\cdot BE + CH \\cdot CF = BC \\cdot BC = BC^2\\text{ (đpcm)}.$$",
        "trang": 2,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },

    # Bài V (0.5 điểm)
    {
        "id": f"l8-{slug}-tl-b5",
        "vi_tri": "Bài V",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Biến đổi đẳng thức đại số nâng cao"],
        "band": "VDC",
        "phut": 6.0,
        "diem_bai": 0.5,
        "de": "Cho các số thực $a, b, c$ thỏa mãn $\\frac{1}{a} + \\frac{1}{b} + \\frac{1}{c} = \\frac{1}{a+b+c}$. Chứng minh rằng:\n$$\\frac{1}{a^{2025}} + \\frac{1}{b^{2025}} + \\frac{1}{c^{2025}} = \\frac{1}{a^{2025} + b^{2025} + c^{2025}}$$",
        "dap_an": "Chứng minh (a+b)(b+c)(c+a) = 0",
        "loi_giai": "Từ giả thiết $\\frac{1}{a} + \\frac{1}{b} + \\frac{1}{c} = \\frac{1}{a+b+c}$, ta biến đổi:\n$$\\begin{aligned} &\\left(\\frac{1}{a} + \\frac{1}{b}\\right) + \\left(\\frac{1}{c} - \\frac{1}{a+b+c}\\right) = 0 \\\\ \\Leftrightarrow &\\frac{a+b}{ab} + \\frac{a+b+c-c}{c(a+b+c)} = 0 \\\\ \\Leftrightarrow &\\frac{a+b}{ab} + \\frac{a+b}{c(a+b+c)} = 0 \\\\ \\Leftrightarrow &(a+b) \\left[\\frac{1}{ab} + \\frac{1}{c(a+b+c)}\\right] = 0 \\\\ \\Leftrightarrow &(a+b) \\frac{c(a+b+c) + ab}{abc(a+b+c)} = 0 \\\\ \\Leftrightarrow &(a+b) \\frac{ac + bc + c^2 + ab}{abc(a+b+c)} = 0 \\\\ \\Leftrightarrow &\\frac{(a+b)(b+c)(c+a)}{abc(a+b+c)} = 0 \\\\ \\Leftrightarrow &(a+b)(b+c)(c+a) = 0 \\end{aligned}$$\nSuy ra trong ba số $a+b, b+c, c+a$ phải có ít nhất một số bằng 0.\n- Không mất tính tổng quát, giả sử $a + b = 0 \\Leftrightarrow a = -b$.\nVì 2025 là số nguyên dương lẻ nên $a^{2025} = (-b)^{2025} = -b^{2025}$, do đó $a^{2025} + b^{2025} = 0$.\nKhi đó:\n$$VT = \\frac{1}{a^{2025}} + \\frac{1}{b^{2025}} + \\frac{1}{c^{2025}} = -\\frac{1}{b^{2025}} + \\frac{1}{b^{2025}} + \\frac{1}{c^{2025}} = \\frac{1}{c^{2025}}$$\n$$VP = \\frac{1}{a^{2025} + b^{2025} + c^{2025}} = \\frac{1}{0 + c^{2025}} = \\frac{1}{c^{2025}}$$\nDo đó $VT = VP$.\n- Tương tự với các trường hợp $b = -c$ hoặc $c = -a$, ta đều suy ra được đẳng thức trên.\nVậy đẳng thức được chứng minh.",
        "trang": 2,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    }
]

total_score = sum(c["diem_bai"] for c in cau_list)
assert abs(total_score - 10.0) < 1e-6, f"Total score must be 10.0, got {total_score}"

data["cau"] = cau_list
data["tang"] = 2
data["da_duyet"] = True
data["ghi_chu"] = f"Đề thi cuối kì 2 Toán 8 THCS Tam Hưng 2025-2026. Cấu trúc gồm 8 câu trắc nghiệm (2,0 điểm) và 5 bài tự luận (8,0 điểm). Tổng điểm: {total_score:.2f} điểm. Đã chuẩn hóa toàn diện theo LaTeX."

with open('inputs/refs/de-thi/lop-8/exams/ck2-2025-thcs-tam-hung.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {slug}: {len(cau_list)} cau, total_score = {total_score:.2f}")
