import json

slug = 'gk2-2025-thcs-van-yen'
path = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
data = json.load(open(path, 'r', encoding='utf-8'))

data['tang'] = 2
data['da_duyet'] = True
data['ghi_chu'] = 'Đề thi giữa kì 2 Toán 8 năm học 2025-2026 THCS Văn Yên (Hà Đông, Hà Nội). Đề 100% tự luận (5 bài: Bài I: 1.5đ, Bài II: 2.0đ, Bài III: 2.0đ, Bài IV: 4.0đ, Bài V: 0.5đ). Tổng 10.00 điểm.'

cau_list = [
    {
        "id": f"l8-{slug}-b1-1",
        "vi_tri": "Bài I.1",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Cộng trừ phân thức đại số"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 0.75,
        "de": "Thực hiện phép tính:\n$$\\frac{x+2}{x-2} - \\frac{x-2}{x+2} + \\frac{16}{x^2-4}$$",
        "dap_an": "ĐKXĐ: $x \\ne \\pm 2$.\n$$\\begin{aligned}\n\\frac{x+2}{x-2} - \\frac{x-2}{x+2} + \\frac{16}{x^2-4} &= \\frac{(x+2)^2 - (x-2)^2 + 16}{(x-2)(x+2)} \\\\\n&= \\frac{(x^2+4x+4) - (x^2-4x+4) + 16}{(x-2)(x+2)} \\\\\n&= \\frac{8x+16}{(x-2)(x+2)} \\\\\n&= \\frac{8(x+2)}{(x-2)(x+2)} = \\frac{8}{x-2}\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b1-2",
        "vi_tri": "Bài I.2",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Nhân chia phân thức đại số"],
        "band": "TH",
        "phut": 3,
        "diem_bai": 0.75,
        "de": "Thực hiện phép tính:\n$$\\frac{4x+8}{(x-10)^2} : \\frac{(x+2)^2}{2x-20}$$",
        "dap_an": "ĐKXĐ: $x \\ne 10, x \\ne -2$.\n$$\\begin{aligned}\n\\frac{4x+8}{(x-10)^2} : \\frac{(x+2)^2}{2x-20} &= \\frac{4(x+2)}{(x-10)^2} \\cdot \\frac{2(x-10)}{(x+2)^2} \\\\\n&= \\frac{8(x+2)(x-10)}{(x-10)^2(x+2)^2} = \\frac{8}{(x-10)(x+2)}\n\\end{aligned}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2-1",
        "vi_tri": "Bài II.1",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tính giá trị biểu thức phân thức"],
        "band": "NB",
        "phut": 2,
        "diem_bai": 0.5,
        "de": "Cho biểu thức $A = \\frac{-5}{x+1}$ và $B = \\frac{1+2x}{x+2} - \\frac{x^2+8}{x^2-4} + \\frac{x}{2-x}$ với $x \\ne -1, x \\ne \\pm 2$.\nTính giá trị của biểu thức $A$ khi $x = 5$.",
        "dap_an": "Thay $x = 5$ (thỏa mãn ĐKXĐ) vào biểu thức $A$, ta được:\n$$A = \\frac{-5}{5+1} = \\frac{-5}{6}$$\nVậy khi $x = 5$ thì $A = -\\frac{5}{6}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2-2",
        "vi_tri": "Bài II.2",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Rút gọn biểu thức chứa phân thức"],
        "band": "TH",
        "phut": 5,
        "diem_bai": 1.0,
        "de": "Chứng minh rằng: $B = \\frac{-5}{x-2}$.",
        "dap_an": "Với $x \\ne -1, x \\ne \\pm 2$, ta có:\n$$\\begin{aligned}\nB &= \\frac{1+2x}{x+2} - \\frac{x^2+8}{(x-2)(x+2)} - \\frac{x}{x-2} \\\\\n&= \\frac{(1+2x)(x-2) - (x^2+8) - x(x+2)}{(x-2)(x+2)} \\\\\n&= \\frac{2x^2 - 3x - 2 - x^2 - 8 - x^2 - 2x}{(x-2)(x+2)} \\\\\n&= \\frac{-5x - 10}{(x-2)(x+2)} = \\frac{-5(x+2)}{(x-2)(x+2)} = \\frac{-5}{x-2}\n\\end{aligned}$$\nVậy $B = \\frac{-5}{x-2}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2-3",
        "vi_tri": "Bài II.3",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tìm x nguyên để biểu thức nhận giá trị nguyên"],
        "band": "VD",
        "phut": 4,
        "diem_bai": 0.5,
        "de": "Biết $P = B : A$. Tìm giá trị nguyên nhỏ nhất của $x$ để $P$ nhận giá trị nguyên.",
        "dap_an": "Ta có:\n$$P = B : A = \\frac{-5}{x-2} : \\frac{-5}{x+1} = \\frac{-5}{x-2} \\cdot \\frac{x+1}{-5} = \\frac{x+1}{x-2}$$\nBiến đổi:\n$$P = \\frac{x-2+3}{x-2} = 1 + \\frac{3}{x-2}$$\nĐể $P$ nhận giá trị nguyên với $x \\in \\mathbb{Z}$ thì $x-2 \\in Ư(3) = \\{\\pm 1; \\pm 3\\}$.\nTa có bảng giá trị:\n- $x - 2 = -3 \\implies x = -1$ (loại do ĐKXĐ $x \\ne -1$)\n- $x - 2 = -1 \\implies x = 1$ (thỏa mãn ĐKXĐ)\n- $x - 2 = 1 \\implies x = 3$ (thỏa mãn ĐKXĐ)\n- $x - 2 = 3 \\implies x = 5$ (thỏa mãn ĐKXĐ)\nCác giá trị nguyên của $x$ để $P$ nguyên là $x \\in \\{1; 3; 5\\}$.\nTrong đó, giá trị nguyên nhỏ nhất của $x$ là $x = 1$.\nVậy $x = 1$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b3-1",
        "vi_tri": "Bài III.1",
        "loai": "TL",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Giải phương trình đưa về dạng ax + b = 0"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 1.0,
        "de": "Giải phương trình:\n$$(x+2)^2 - 8x = x(x-3) - 4$$",
        "dap_an": "$$\\begin{aligned}\n(x+2)^2 - 8x = x(x-3) - 4 &\\iff x^2 + 4x + 4 - 8x = x^2 - 3x - 4 \\\\\n&\\iff x^2 - 4x + 4 = x^2 - 3x - 4 \\\\\n&\\iff -4x + 3x = -4 - 4 \\\\\n&\\iff -x = -8 \\iff x = 8\n\\end{aligned}$$\nVậy tập nghiệm của phương trình là $S = \\{8\\}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b3-2",
        "vi_tri": "Bài III.2",
        "loai": "TL",
        "chuong": "V. Phương trình bậc nhất một ẩn",
        "dang": ["Giải phương trình đưa về dạng ax + b = 0"],
        "band": "TH",
        "phut": 4,
        "diem_bai": 1.0,
        "de": "Giải phương trình:\n$$\\frac{3x+2}{2} - \\frac{3x+1}{6} = \\frac{5}{3} + 2x$$",
        "dap_an": "Quy đồng mẫu số hai vế với mẫu thức chung là $6$:\n$$\\begin{aligned}\n\\frac{3(3x+2)}{6} - \\frac{3x+1}{6} &= \\frac{10}{6} + \\frac{12x}{6} \\\\\n3(3x+2) - (3x+1) &= 10 + 12x \\\\\n9x + 6 - 3x - 1 &= 10 + 12x \\\\\n6x + 5 &= 10 + 12x \\\\\n6x - 12x &= 10 - 5 \\\\\n-6x &= 5 \\iff x = -\\frac{5}{6}\n\\end{aligned}$$\nVậy tập nghiệm của phương trình là $S = \\left\\{-\\frac{5}{6}\\right\\}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-1a",
        "vi_tri": "Bài IV.1a",
        "loai": "TL",
        "chuong": "VII. Định lí Thalès trong tam giác",
        "dang": ["Định lí Pythagore", "Ứng dụng thực tế của định lí Pythagore"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 0.5,
        "de": "Một chiếc thang có chiều dài $AB = 4{,}1\\text{ m}$ đặt cách một bức tường khoảng cách $AC = 0{,}9\\text{ m}$ (tam giác $ABC$ vuông tại $C$).\nTính chiều cao $BC$.",
        "dap_an": "Áp dụng định lí Pythagore cho tam giác $ABC$ vuông tại $C$, ta có:\n$$AB^2 = AC^2 + BC^2 \\implies BC^2 = AB^2 - AC^2 = 4{,}1^2 - 0{,}9^2 = 16{,}81 - 0{,}81 = 16$$\n$$\\implies BC = \\sqrt{16} = 4\\text{ (m)}$$\nVậy chiều cao $BC$ của bức tường là $4\\text{ m}$.",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-1b",
        "vi_tri": "Bài IV.1b",
        "loai": "TL",
        "chuong": "VII. Định lí Thalès trong tam giác",
        "dang": ["Ứng dụng thực tế của định lí Pythagore"],
        "band": "TH",
        "phut": 3,
        "diem_bai": 0.5,
        "de": "Biết rằng khoảng cách “an toàn” khi $2{,}0 < \\frac{BC}{AC} < 2{,}2$. Hỏi khoảng cách đặt thang cách chân tường là $AC = 0{,}9\\text{ m}$ có “an toàn” không?",
        "dap_an": "Ta tính tỉ số:\n$$\\frac{BC}{AC} = \\frac{4}{0{,}9} = \\frac{40}{9} \\approx 4{,}44$$\nVì $4{,}44 > 2{,}2$ nên tỉ số $\\frac{BC}{AC}$ không nằm trong khoảng an toàn $2{,}0 < \\frac{BC}{AC} < 2{,}2$.\nVậy khoảng cách đặt thang cách chân tường $AC = 0{,}9\\text{ m}$ không an toàn.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2a",
        "vi_tri": "Bài IV.2a",
        "loai": "TL",
        "chuong": "VIII. Tam giác đồng dạng",
        "dang": ["Chứng minh tam giác đồng dạng"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 1.0,
        "de": "Cho tam giác $ABC$ vuông tại $A$ có $AB < AC$. Vẽ $AH \\perp BC$ tại $H$. Lấy $D$ trên $HC$ sao cho $HB = HD$.\nChứng minh $\\Delta ABC \\sim \\Delta HBA$.",
        "dap_an": "Xét $\\Delta ABC$ và $\\Delta HBA$ có:\n- $\\widehat{BAC} = \\widehat{BHA} = 90^\\circ$\n- $\\widehat{B}$ là góc chung\nDo đó $\\Delta ABC \\sim \\Delta HBA$ (g.g).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2b",
        "vi_tri": "Bài IV.2b",
        "loai": "TL",
        "chuong": "VIII. Tam giác đồng dạng",
        "dang": ["Tính độ dài đoạn thẳng bằng tam giác đồng dạng", "Hệ thức hình học"],
        "band": "TH",
        "phut": 5,
        "diem_bai": 1.0,
        "de": "Cho $AB = 3\\text{ cm}, AC = 4\\text{ cm}$. Từ $C$ kẻ đường thẳng vuông góc với $AD$ cắt $AD$ tại $E$.\nTính $AH$ và chứng minh $AH \\cdot CD = CE \\cdot AD$.",
        "dap_an": "+ Tính $AH$:\nÁp dụng định lí Pythagore trong $\\Delta ABC$ vuông tại $A$:\n$$BC = \\sqrt{AB^2 + AC^2} = \\sqrt{3^2 + 4^2} = 5\\text{ (cm)}$$\nVì $\\Delta ABC \\sim \\Delta HBA$ (theo câu a) nên:\n$$\\frac{AH}{AC} = \\frac{AB}{BC} \\implies AH = \\frac{AB \\cdot AC}{BC} = \\frac{3 \\cdot 4}{5} = 2{,}4\\text{ (cm)}$$\n+ Chứng minh $AH \\cdot CD = CE \\cdot AD$:\nXét tam giác $ACD$ có $AH \\perp CD$ (do $H \\in BC$) và $CE \\perp AD$ tại $E$.\nDiện tích tam giác $ACD$ được tính theo hai cách:\n$$S_{\\Delta ACD} = \\frac{1}{2} AH \\cdot CD = \\frac{1}{2} CE \\cdot AD$$\nSuy ra: $AH \\cdot CD = CE \\cdot AD$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2c",
        "vi_tri": "Bài IV.2c",
        "loai": "TL",
        "chuong": "VIII. Tam giác đồng dạng",
        "dang": ["Chứng minh tam giác đồng dạng", "Chứng minh tia phân giác"],
        "band": "VD",
        "phut": 6,
        "diem_bai": 1.0,
        "de": "Biết $AH$ cắt $CE$ tại $F$. Tia $FD$ cắt cạnh $AC$ tại $K$.\nChứng minh $\\Delta ABC \\sim \\Delta EDC$ và $KD$ là tia phân giác của $\\widehat{HKE}$.",
        "dap_an": "- Chứng minh $\\Delta ABC \\sim \\Delta EDC$:\nXét $\\Delta ABC$ và $\\Delta EDC$ có:\n- $\\widehat{BAC} = \\widehat{DEC} = 90^\\circ$\n- $\\widehat{C}$ là góc chung\nDo đó $\\Delta ABC \\sim \\Delta EDC$ (g.g).\n\n- Chứng minh $KD$ là tia phân giác của $\\widehat{HKE}$:\nTrong tam giác $ACD$, hai đường cao $AH$ và $CE$ cắt nhau tại $F$ nên $F$ là trực tâm của $\\Delta ACD$.\nSuy ra $DF \\perp AC$ tại $K$, tức $\\widehat{DKC} = 90^\\circ$.\nXét hai điểm $H, K$ cùng nhìn đoạn thẳng $CD$ dưới góc vuông ($\\widehat{DHC} = \\widehat{DKC} = 90^\\circ$), nên bốn điểm $D, H, C, K$ cùng thuộc đường tròn đường kính $CD$.\nSuy ra $\\widehat{DKH} = \\widehat{DCH}$ (hai góc nội tiếp cùng chắn cung $DH$). (1)\nTương tự, hai điểm $E, K$ cùng nhìn $CD$ dưới góc $90^\\circ$ ($\\widehat{DEC} = \\widehat{DKC} = 90^\\circ$), nên bốn điểm $D, K, C, E$ cùng thuộc đường tròn đường kính $CD$.\nSuy ra $\\widehat{DKE} = \\widehat{DCE}$ (hai góc nội tiếp cùng chắn cung $DE$). (2)\nMặt khác, vì $HB = HD$ và $AH \\perp BD$ nên tam giác $ABD$ cân tại $A$, suy ra $\\widehat{ADB} = \\widehat{B}$.\nDo đó $\\widehat{ADH} = \\widehat{B}$. Mà $\\widehat{CDE} = \\widehat{ADH}$ (đối đỉnh) nên $\\widehat{CDE} = \\widehat{B}$.\nTrong $\\Delta CDE$ vuông tại $E$: $\\widehat{DCE} = 90^\\circ - \\widehat{CDE} = 90^\\circ - \\widehat{B}$.\nTrong $\\Delta ABC$ vuông tại $A$: $\\widehat{ACB} = 90^\\circ - \\widehat{B}$.\nSuy ra $\\widehat{DCE} = \\widehat{ACB} = \\widehat{DCH}$. (3)\nTừ (1), (2) và (3) suy ra $\\widehat{DKH} = \\widehat{DKE}$.\nVậy $KD$ là tia phân giác của $\\widehat{HKE}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b5",
        "vi_tri": "Bài V",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tính giá trị biểu thức phân thức đối xứng"],
        "band": "VDC",
        "phut": 6,
        "diem_bai": 0.5,
        "de": "Cho $x \\ne 0, y \\ne 0, z \\ne 0$ và $x+y+z=0$. Tính giá trị của biểu thức:\n$$P = \\frac{1}{z^2+y^2-x^2} + \\frac{1}{y^2+x^2-z^2} + \\frac{1}{x^2+z^2-y^2}$$",
        "dap_an": "Vì $x+y+z=0$ nên $y+z = -x \\implies (y+z)^2 = (-x)^2 \\implies y^2+2yz+z^2 = x^2$.\nSuy ra $z^2 + y^2 - x^2 = -2yz$.\nTương tự, ta có:\n$$y^2 + x^2 - z^2 = -2xy$$\n$$x^2 + z^2 - y^2 = -2xz$$\nThay vào biểu thức $P$, ta được:\n$$\\begin{aligned}\nP &= \\frac{1}{-2yz} + \\frac{1}{-2xy} + \\frac{1}{-2xz} \\\\\n&= -\\frac{1}{2} \\left( \\frac{1}{yz} + \\frac{1}{xy} + \\frac{1}{xz} \\right) \\\\\n&= -\\frac{1}{2} \\cdot \\frac{x+z+y}{xyz}\n\\end{aligned}$$\nVì $x+y+z=0$ nên:\n$$P = -\\frac{1}{2} \\cdot \\frac{0}{xyz} = 0$$\nVậy $P = 0$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    }
]

total = sum(c['diem_bai'] for c in cau_list)
print(f"Total points: {total:.2f}")
data['cau'] = cau_list

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {slug}.json successfully!")
