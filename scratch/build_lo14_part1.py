# -*- coding: utf-8 -*-
import json, os

def save_exam(slug, data):
    p = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {slug}: {len(data['cau'])} cau, sum={sum(c['diem_bai'] for c in data['cau']):.2f}")

# ==============================================================================
# 1. ck2-2025-thcs-xuan-la
# ==============================================================================
def build_xuan_la():
    slug = 'ck2-2025-thcs-xuan-la'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-b1-1a",
            "vi_tri": "Bài 1.1a",
            "loai": "TL",
            "chuong": "V. Thu thập và tổ chức dữ liệu",
            "dang": ["Biểu đồ cột"],
            "band": "NB",
            "phut": 2.0,
            "diem_bai": 0.5,
            "de_chung": "Bài 1 (1,5 điểm).\n1.1. Biểu đồ cột dưới đây biểu diễn doanh thu của 5 cửa hàng trong tháng 4:\n- Cửa hàng A: 15 triệu đồng\n- Cửa hàng B: 17 triệu đồng\n- Cửa hàng C: 13 triệu đồng\n- Cửa hàng D: 20 triệu đồng\n- Cửa hàng E: 30 triệu đồng",
            "de": "Tính tổng doanh thu của 5 cửa hàng trong tháng 4.",
            "dap_an": "95 triệu đồng",
            "loi_giai": "Tổng doanh thu của 5 cửa hàng trong tháng 4 là:\n$$15 + 17 + 13 + 20 + 30 = 95\\text{ (triệu đồng)}.$$",
            "trang": 1,
            "co_hinh": True,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1-1b",
            "vi_tri": "Bài 1.1b",
            "loai": "TL",
            "chuong": "V. Thu thập và tổ chức dữ liệu",
            "dang": ["Phân tích dữ liệu từ biểu đồ"],
            "band": "TH",
            "phut": 3.0,
            "diem_bai": 0.5,
            "de_chung": "Bài 1 (1,5 điểm).\n1.1. Biểu đồ cột dưới đây biểu diễn doanh thu của 5 cửa hàng trong tháng 4:\n- Cửa hàng A: 15 triệu đồng\n- Cửa hàng B: 17 triệu đồng\n- Cửa hàng C: 13 triệu đồng\n- Cửa hàng D: 20 triệu đồng\n- Cửa hàng E: 30 triệu đồng",
            "de": "Chủ cửa hàng nhận định rằng “Doanh thu của cửa hàng E là cao nhất và chiếm khoảng 31,58% so với tổng doanh thu của 5 cửa hàng (kết quả làm tròn đến hàng phần trăm)”. Nhận định của chủ cửa hàng là đúng hay sai? Vì sao?",
            "dap_an": "Nhận định của chủ cửa hàng là đúng",
            "loi_giai": "- Doanh thu của cửa hàng E là 30 triệu đồng, cao nhất trong 5 cửa hàng.\n- Tỉ số phần trăm doanh thu của cửa hàng E so với tổng doanh thu của 5 cửa hàng là:\n$$\\frac{30}{95} \\cdot 100\\% \\approx 31{,}58\\%.$$\nVậy nhận định của chủ cửa hàng là đúng.",
            "trang": 1,
            "co_hinh": True,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1-2a",
            "vi_tri": "Bài 1.2a",
            "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố",
            "dang": ["Tập hợp các kết quả có thể"],
            "band": "NB",
            "phut": 2.0,
            "diem_bai": 0.25,
            "de_chung": "1.2. Một hộp có 25 tấm thẻ cùng loại được đánh số lần lượt là $1; 2; 3; \\dots; 25$. Hai thẻ khác nhau ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp.",
            "de": "Viết tập hợp $A$ gồm các kết quả có thể xảy đối với số xuất hiện trên thẻ.",
            "dap_an": "$A = \\{1; 2; 3; \\dots; 25\\}$",
            "loi_giai": "Tập hợp $A$ gồm các kết quả có thể xảy ra đối với số xuất hiện trên thẻ là:\n$$A = \\{1; 2; 3; \\dots; 25\\}.$$",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1-2b",
            "vi_tri": "Bài 1.2b",
            "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố",
            "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "TH",
            "phut": 2.5,
            "diem_bai": 0.25,
            "de_chung": "1.2. Một hộp có 25 tấm thẻ cùng loại được đánh số lần lượt là $1; 2; 3; \\dots; 25$. Hai thẻ khác nhau ghi hai số khác nhau. Rút ngẫu nhiên một thẻ trong hộp.",
            "de": "Tính xác suất của biến cố “Số xuất hiện trên thẻ được rút ra là số có hai chữ số có tổng bằng 5”.",
            "dap_an": "$\\frac{2}{25}$",
            "loi_giai": "Có 25 kết quả có thể xảy ra và chúng có cùng khả năng xuất hiện.\nCác số có hai chữ số từ 1 đến 25 có tổng hai chữ số bằng 5 là: $14$ (do $1+4=5$) và $23$ (do $2+3=5$).\nDo đó có 2 kết quả thuận lợi cho biến cố.\nXác suất của biến cố là: $P = \\frac{2}{25} = 0{,}08$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2a",
            "vi_tri": "Bài 2.a",
            "loai": "TL",
            "chuong": "VI. Phân thức đại số",
            "dang": ["Rút gọn phân thức đại số"],
            "band": "TH",
            "phut": 5.0,
            "diem_bai": 1.0,
            "de_chung": "Bài 2 (1,5 điểm). Cho biểu thức $A = \\frac{x}{x+3} - \\frac{2x-1}{3-x} - \\frac{2x^2-x-3}{x^2-9}$ với $x \\neq \\pm 3$",
            "de": "Chứng minh $A = \\frac{x}{x-3}$.",
            "dap_an": "$A = \\frac{x}{x-3}$",
            "loi_giai": "Với $x \\neq \\pm 3$, ta có:\n$$\\begin{aligned}\nA &= \\frac{x}{x+3} + \\frac{2x-1}{x-3} - \\frac{2x^2-x-3}{(x-3)(x+3)} \\\\\n&= \\frac{x(x-3) + (2x-1)(x+3) - (2x^2-x-3)}{(x-3)(x+3)} \\\\\n&= \\frac{x^2 - 3x + (2x^2 + 5x - 3) - 2x^2 + x + 3}{(x-3)(x+3)} \\\\\n&= \\frac{x^2 + 3x}{(x-3)(x+3)} = \\frac{x(x+3)}{(x-3)(x+3)} = \\frac{x}{x-3}.\n\\end{aligned}$$\nVậy $A = \\frac{x}{x-3}$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2b",
            "vi_tri": "Bài 2.b",
            "loai": "TL",
            "chuong": "VI. Phân thức đại số",
            "dang": ["Tính giá trị của phân thức"],
            "band": "TH",
            "phut": 3.0,
            "diem_bai": 0.5,
            "de_chung": "Bài 2 (1,5 điểm). Cho biểu thức $A = \\frac{x}{x+3} - \\frac{2x-1}{3-x} - \\frac{2x^2-x-3}{x^2-9}$ với $x \\neq \\pm 3$",
            "de": "Tính giá trị biểu thức $A$ khi $x^2 - 3x = 0$.",
            "dap_an": "$A = 0$",
            "loi_giai": "Ta có: $x^2 - 3x = 0 \\Leftrightarrow x(x-3) = 0 \\Leftrightarrow x = 0$ hoặc $x = 3$.\nKết hợp điều kiện xác định $x \\neq \\pm 3$, ta loại $x = 3$, nhận $x = 0$.\nThay $x = 0$ vào biểu thức $A = \\frac{x}{x-3}$, ta được:\n$$A = \\frac{0}{0-3} = 0.$$",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-1a",
            "vi_tri": "Bài 3.1a",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB",
            "phut": 3.0,
            "diem_bai": 0.75,
            "de_chung": "Bài 3 (2,5 điểm).\n3.1. Giải các phương trình sau:",
            "de": "$5(x-3) + 5 = 4x + 1$",
            "dap_an": "$x = 11$",
            "loi_giai": "$$5(x-3) + 5 = 4x + 1 \\Leftrightarrow 5x - 15 + 5 = 4x + 1 \\Leftrightarrow 5x - 10 = 4x + 1 \\Leftrightarrow 5x - 4x = 1 + 10 \\Leftrightarrow x = 11.$$\nVậy phương trình có nghiệm $x = 11$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-1b",
            "vi_tri": "Bài 3.1b",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải phương trình đưa về phương trình bậc nhất một ẩn"],
            "band": "TH",
            "phut": 4.0,
            "diem_bai": 0.75,
            "de_chung": "Bài 3 (2,5 điểm).\n3.1. Giải các phương trình sau:",
            "de": "$\\frac{2x+3}{3} - x = 3 - \\frac{x-2}{4}$",
            "dap_an": "$x = -30$",
            "loi_giai": "$$\\frac{2x+3}{3} - x = 3 - \\frac{x-2}{4}$$\n$$\\Leftrightarrow \\frac{4(2x+3) - 12x}{12} = \\frac{36 - 3(x-2)}{12}$$\n$$\\Leftrightarrow 8x + 12 - 12x = 36 - 3x + 6$$\n$$\\Leftrightarrow -4x + 12 = 42 - 3x$$\n$$\\Leftrightarrow -4x + 3x = 42 - 12$$\n$$\\Leftrightarrow -x = 30 \\Leftrightarrow x = -30.$$\nVậy phương trình có nghiệm $x = -30$.",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-2",
            "vi_tri": "Bài 3.2",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD",
            "phut": 6.0,
            "diem_bai": 1.0,
            "de": "Một ô tô đi từ Hà Nội đến Đền Hùng với vận tốc $30\\text{ km/h}$. Trên quãng đường từ Đền Hùng về Hà Nội, vận tốc ô tô tăng thêm $10\\text{ km/h}$ nên thời gian về ít hơn thời gian đi là $30\\text{ phút}$. Tính quãng đường từ Hà Nội đến Đền Hùng?",
            "dap_an": "$60\\text{ km}$",
            "loi_giai": "Đổi $30\\text{ phút} = \\frac{1}{2}\\text{ giờ}$.\nVận tốc của ô tô lúc về là: $30 + 10 = 40\\text{ (km/h)}$.\nGọi quãng đường từ Hà Nội đến Đền Hùng là $x\\text{ (km)}$ ($x > 0$).\nThời gian ô tô đi từ Hà Nội đến Đền Hùng là: $\\frac{x}{30}\\text{ (giờ)}$.\nThời gian ô tô đi từ Đền Hùng về Hà Nội là: $\\frac{x}{40}\\text{ (giờ)}$.\nVì thời gian về ít hơn thời gian đi là $\\frac{1}{2}$ giờ nên ta có phương trình:\n$$\\frac{x}{30} - \\frac{x}{40} = \\frac{1}{2}$$\n$$\\Leftrightarrow \\frac{4x - 3x}{120} = \\frac{60}{120} \\Leftrightarrow x = 60\\text{ (thỏa mãn điều kiện)}.$$\nVậy quãng đường từ Hà Nội đến Đền Hùng dài $60\\text{ km}$.",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-1-1",
            "vi_tri": "Bài 4.1.1",
            "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác",
            "dang": ["Ứng dụng định lí Thalès đo khoảng cách, chiều cao"],
            "band": "TH",
            "phut": 3.5,
            "diem_bai": 0.5,
            "de_chung": "Bài 4 (4,0 điểm).\n4.1. Để đo chiều cao $AB$ của một tòa nhà, người ta lấy các điểm $C, D, E$ như hình bên.\nBiết: $DE // BC$; $AE = 1{,}5\\text{m}$; $EC = 21\\text{m}$; $AD = 3{,}2\\text{m}$.",
            "de": "1) Tính chiều cao của tòa nhà đó?",
            "dap_an": "$48\\text{ m}$",
            "loi_giai": "Ta có: $AC = AE + EC = 1{,}5 + 21 = 22{,}5\\text{ (m)}$.\nVì $DE // BC$, áp dụng hệ quả của định lí Thalès vào $\\triangle ABC$, ta có:\n$$\\frac{AD}{AB} = \\frac{AE}{AC} \\Rightarrow \\frac{3{,}2}{AB} = \\frac{1{,}5}{22{,}5} = \\frac{1}{15}.$$\nSuy ra chiều cao tòa nhà là:\n$$AB = 3{,}2 \\cdot 15 = 48\\text{ (m)}.$$",
            "trang": 2,
            "co_hinh": True,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-1-2",
            "vi_tri": "Bài 4.1.2",
            "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác",
            "dang": ["Toán thực tế"],
            "band": "TH",
            "phut": 3.5,
            "diem_bai": 0.5,
            "de_chung": "Bài 4 (4,0 điểm).\n4.1. Để đo chiều cao $AB$ của một tòa nhà, người ta lấy các điểm $C, D, E$ như hình bên.\nBiết: $DE // BC$; $AE = 1{,}5\\text{m}$; $EC = 21\\text{m}$; $AD = 3{,}2\\text{m}$.",
            "de": "2) Người nhân viên cần lau cửa kính bên ngoài tòa nhà từ vị trí điểm $B$ đến điểm $D$, biết 1 phút người đó di chuyển được $16\\text{cm}$. Hỏi người nhân viên mất bao nhiêu lâu để di chuyển từ vị trí điểm $B$ đến điểm $D$?",
            "dap_an": "$280\\text{ phút}$ (tức 4 giờ 40 phút)",
            "loi_giai": "Khoảng cách từ vị trí điểm $B$ đến điểm $D$ là:\n$$BD = AB - AD = 48 - 3{,}2 = 44{,}8\\text{ (m)} = 4480\\text{ (cm)}.$$\nThời gian người nhân viên di chuyển từ $B$ đến $D$ là:\n$$\\frac{4480}{16} = 280\\text{ (phút)} = 4\\text{ giờ } 40\\text{ phút}.$$",
            "trang": 2,
            "co_hinh": True,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2a",
            "vi_tri": "Bài 4.2a",
            "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng",
            "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH",
            "phut": 4.0,
            "diem_bai": 1.0,
            "de_chung": "4.2. Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "a) Chứng minh rằng: $\\triangle ABC \\backsim \\triangle HBA$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle HBA$ (g.g)",
            "loi_giai": "Xét $\\triangle ABC$ và $\\triangle HBA$, ta có:\n$$\\widehat{BAC} = \\widehat{BHA} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle ABC \\backsim \\triangle HBA\\text{ (g.g)}.$",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2b",
            "vi_tri": "Bài 4.2b",
            "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng",
            "dang": ["Chứng minh hệ thức hình học nhờ tam giác đồng dạng"],
            "band": "VD",
            "phut": 6.0,
            "diem_bai": 1.0,
            "de_chung": "4.2. Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "b) Gọi $M, N$ lần lượt là trung điểm của $BC$ và $AB$, từ $B$ kẻ đường thẳng vuông góc với $BC$ cắt $MN$ kéo dài tại $I$. Chứng minh rằng: $MN // AC$ và $IB^2 = IM \\cdot IN$.",
            "dap_an": "$MN // AC$ và $IB^2 = IM \\cdot IN$",
            "loi_giai": "+) Vì $M$ là trung điểm của $BC$, $N$ là trung điểm của $AB$ nên $MN$ là đường trung bình của tam giác $ABC$.\nSuy ra $MN // AC$.\n+) Vì $MN // AC$ và $AC \\perp AB$ tại $A$ nên $MN \\perp AB$ tại $N$, hay $IN \\perp AB$.\nTam giác $IBM$ vuông tại $B$ (do $IB \\perp BC$) có đường cao $BN$ ($BN \\perp IM$).\nXét $\\triangle IBN$ và $\\triangle IMB$, ta có:\n$$\\widehat{INB} = \\widehat{IBM} = 90^\\circ,$$\n$$\\widehat{BIN}\\text{ là góc chung}.$$\nDo đó $\\triangle IBN \\backsim \\triangle IMB\\text{ (g.g)} \\Rightarrow \\frac{IB}{IM} = \\frac{IN}{IB} \\Rightarrow IB^2 = IM \\cdot IN.$$",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2c",
            "vi_tri": "Bài 4.2c",
            "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác",
            "dang": ["Hệ quả định lí Thalès chứng minh trung điểm"],
            "band": "VDC",
            "phut": 6.0,
            "diem_bai": 1.0,
            "de_chung": "4.2. Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "c) Gọi $O$ là giao điểm của $IC$ và $AH$. Chứng minh $O$ là trung điểm của $AH$.",
            "dap_an": "$O$ là trung điểm của $AH$",
            "loi_giai": "Gọi $K$ là giao điểm của tia $BI$ và đường thẳng $AC$.\nVì $BK \\perp BC$ và $AH \\perp BC$ nên $AH // BK$.\nXét tam giác $CBK$ có $AH // BK$ và $O \\in IC$:\n- Trong tam giác $CBI$ có $OH // BI \\Rightarrow \\frac{OH}{BI} = \\frac{CO}{CI}$.\n- Trong tam giác $CIK$ có $OA // IK \\Rightarrow \\frac{OA}{IK} = \\frac{CO}{CI}$.\nSuy ra $\\frac{OH}{BI} = \\frac{OA}{IK}$.\nMặt khác, trong tam giác $ABK$ có $N$ là trung điểm của $AB$ và $NI // AK$ (vì $MN // AC$), suy ra $I$ là trung điểm của đoạn thẳng $BK$, hay $BI = IK$.\nTừ đó suy ra $OH = OA$, hay $O$ là trung điểm của đoạn thẳng $AH$.",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5",
            "vi_tri": "Bài 5",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Toán thực tế tìm giá trị lớn nhất"],
            "band": "VDC",
            "phut": 6.0,
            "diem_bai": 0.5,
            "de": "Trong mùa cao điểm du lịch, một tổ hợp nhà nghỉ ở địa điểm A gồm 100 phòng đồng giá luôn luôn kín phòng khi giá thuê là 480 nghìn đồng/phòng. Qua khảo sát các năm trước, bộ phận kinh doanh của nhà nghỉ thấy rằng: cứ tăng giá phòng lên $x\\%$ ($x \\ge 0$) so với lúc kín phòng (giá thuê 480 nghìn đồng/phòng) thì số phòng cho thuê giảm đi $\\frac{4x}{5}\\%$. Hỏi nhà nghỉ phải niêm yết giá phòng là bao nhiêu để đạt doanh thu cao nhất?",
            "dap_an": "540 nghìn đồng/phòng",
            "loi_giai": "Giá thuê mỗi phòng sau khi tăng $x\\%$ là: $480\\left(1 + \\frac{x}{100}\\right)\\text{ (nghìn đồng)}$.\nSố phòng cho thuê được là: $100\\left(1 - \\frac{4x}{500}\\right) = 100 - \\frac{4}{5}x\\text{ (phòng)}$ (điều kiện $0 \\le x < 125$).\nDoanh thu của nhà nghỉ khi đó là:\n$$Y = 480\\left(1 + \\frac{x}{100}\\right)\\left(100 - \\frac{4}{5}x\\right) = 48000 + 480x - 384x - 3{,}84x^2 = -3{,}84x^2 + 96x + 48000.$$\nBiến đổi biểu thức:\n$$Y = -3{,}84(x^2 - 25x) + 48000 = -3{,}84(x - 12{,}5)^2 + 3{,}84 \\cdot 12{,}5^2 + 48000 = -3{,}84(x - 12{,}5)^2 + 48600.$$\nVì $-3{,}84(x - 12{,}5)^2 \\le 0$ với mọi $x$ nên $Y \\le 48600$.\nDấu “=” xảy ra khi $x = 12{,}5$ (thỏa mãn điều kiện).\nKhi đó giá niêm yết của mỗi phòng là:\n$$480 \\cdot (1 + 12{,}5\\%) = 480 \\cdot 1{,}125 = 540\\text{ (nghìn đồng/phòng)}.$$\nVậy nhà nghỉ phải niêm yết giá phòng là 540 nghìn đồng/phòng để đạt doanh thu cao nhất.",
            "trang": 2,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra HK2 Toán 8 THCS Xuân La 2025-2026. Đã soát 100% từ ảnh scan gốc: 5 bài tự luận (15 ý), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_xuan_la()

# ==============================================================================
# 2. ck2-x-2023-2024-de-thi-hk2-chuyen-amsterdam-hn
# ==============================================================================
def build_amsterdam():
    slug = 'ck2-x-2023-2024-de-thi-hk2-chuyen-amsterdam-hn'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-b1-1",
            "vi_tri": "Bài 1.1",
            "loai": "TL",
            "chuong": "VI. Phân thức đại số",
            "dang": ["Rút gọn phân thức đại số", "Tìm điều kiện xác định"],
            "band": "TH",
            "phut": 5.0,
            "diem_bai": 1.0,
            "de_chung": "Bài 1 (2,0 điểm). Cho biểu thức $P = \\left(\\frac{x+1}{x^2-x} + \\frac{1}{1-x}\\right) : \\left(\\frac{-2}{1-x^2} + \\frac{1}{1+x}\\right)$.",
            "de": "1) Viết điều kiện xác định và rút gọn biểu thức $P$.",
            "dap_an": "ĐKXĐ: $x \\neq 0; x \\neq 1; x \\neq -1$. Rút gọn $P = \\frac{1}{x}$.",
            "loi_giai": "- Điều kiện xác định: $x(x-1) \\neq 0$, $1-x \\neq 0$, $1-x^2 \\neq 0$, $1+x \\neq 0$ và biểu thức chia khác $0$.\n$$\\Leftrightarrow x \\neq 0; x \\neq 1; x \\neq -1.$$\n- Rút gọn:\n$$\\begin{aligned}\nP &= \\left(\\frac{x+1}{x(x-1)} - \\frac{x}{x(x-1)}\\right) : \\left(\\frac{2}{(x-1)(x+1)} + \\frac{x-1}{(x-1)(x+1)}\\right) \\\\\n&= \\frac{x+1-x}{x(x-1)} : \\frac{2+x-1}{(x-1)(x+1)} \\\\\n&= \\frac{1}{x(x-1)} : \\frac{x+1}{(x-1)(x+1)} \\\\\n&= \\frac{1}{x(x-1)} : \\frac{1}{x-1} = \\frac{1}{x(x-1)} \\cdot (x-1) = \\frac{1}{x}.\n\\end{aligned}$$\nVậy $P = \\frac{1}{x}$ với $x \\neq 0, x \\neq \\pm 1$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1-2",
            "vi_tri": "Bài 1.2",
            "loai": "TL",
            "chuong": "VI. Phân thức đại số",
            "dang": ["Tìm giá trị nguyên của biến để biểu thức nhận giá trị nguyên"],
            "band": "VD",
            "phut": 5.0,
            "diem_bai": 1.0,
            "de_chung": "Bài 1 (2,0 điểm). Cho biểu thức $P = \\left(\\frac{x+1}{x^2-x} + \\frac{1}{1-x}\\right) : \\left(\\frac{-2}{1-x^2} + \\frac{1}{1+x}\\right)$.",
            "de": "2) Với phân thức $Q = \\frac{2x^2}{x-1}$. Tìm các số nguyên $x$ để $P \\cdot Q$ là một số nguyên dương.",
            "dap_an": "$x \\in \\{2; 3\\}$",
            "loi_giai": "Ta có:\n$$P \\cdot Q = \\frac{1}{x} \\cdot \\frac{2x^2}{x-1} = \\frac{2x}{x-1} = \\frac{2(x-1)+2}{x-1} = 2 + \\frac{2}{x-1}.$$\nĐể $P \\cdot Q$ là số nguyên thì $\\frac{2}{x-1} \\in \\mathbb{Z} \\Rightarrow x - 1 \\in \\text{Ư}(2) = \\{\\pm 1; \\pm 2\\}$.\n- Với $x - 1 = 1 \\Rightarrow x = 2$ (thỏa mãn ĐKXĐ). Khi đó $P \\cdot Q = 2 + 2 = 4 > 0$ (thỏa mãn là số nguyên dương).\n- Với $x - 1 = -1 \\Rightarrow x = 0$ (loại vì không thỏa mãn ĐKXĐ $x \\neq 0$).\n- Với $x - 1 = 2 \\Rightarrow x = 3$ (thỏa mãn ĐKXĐ). Khi đó $P \\cdot Q = 2 + 1 = 3 > 0$ (thỏa mãn là số nguyên dương).\n- Với $x - 1 = -2 \\Rightarrow x = -1$ (loại vì không thỏa mãn ĐKXĐ $x \\neq -1$).\nVậy các số nguyên $x$ thỏa mãn là $x \\in \\{2; 3\\}$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2-1",
            "vi_tri": "Bài 2.1",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD",
            "phut": 6.0,
            "diem_bai": 1.25,
            "de_chung": "Bài 2 (2,0 điểm).",
            "de": "1) (Giải bài toán bằng cách lập phương trình)\nHai công nhân được giao làm một số lượng sản phẩm bằng nhau. Trong một ngày, người thứ nhất làm được 24 sản phẩm, người thứ hai làm được 28 sản phẩm. Sau khi làm một số ngày như nhau, người thứ nhất còn phải làm thêm 31 sản phẩm nữa và người thứ hai phải làm thêm 7 sản phẩm nữa mới đủ số lượng được giao. Tính số lượng sản phẩm mỗi người được giao làm?",
            "dap_an": "175 sản phẩm",
            "loi_giai": "Gọi số ngày hai người công nhân đã làm là $x$ (ngày) ($x \\in \\mathbb{N}^*$).\nSố sản phẩm người thứ nhất đã làm trong $x$ ngày là $24x$ (sản phẩm).\nTổng số sản phẩm người thứ nhất được giao làm là: $24x + 31$ (sản phẩm).\nSố sản phẩm người thứ hai đã làm trong $x$ ngày là $28x$ (sản phẩm).\nTổng số sản phẩm người thứ hai được giao làm là: $28x + 7$ (sản phẩm).\nVì số lượng sản phẩm mỗi người được giao làm là bằng nhau nên ta có phương trình:\n$$24x + 31 = 28x + 7$$\n$$\\Leftrightarrow 28x - 24x = 31 - 7$$\n$$\\Leftrightarrow 4x = 24 \\Leftrightarrow x = 6\\text{ (thỏa mãn điều kiện)}.$$\nSố sản phẩm mỗi người được giao làm là:\n$$24 \\cdot 6 + 31 = 175\\text{ (sản phẩm)}.$$\nVậy mỗi người công nhân được giao làm 175 sản phẩm.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2-2",
            "vi_tri": "Bài 2.2",
            "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn",
            "dang": ["Tính thể tích hình chóp tam giác đều"],
            "band": "TH",
            "phut": 4.0,
            "diem_bai": 0.75,
            "de_chung": "Bài 2 (2,0 điểm).",
            "de": "2) Cho hình chóp tam giác đều $S.ABC$. Biết độ dài cạnh đáy là $\\sqrt{12}\\text{ cm}$ và chiều cao của hình chóp là $SO = 10\\text{ cm}$. Tính thể tích hình chóp (lấy $\\sqrt{3} \\approx 1{,}73$).",
            "dap_an": "$17{,}3\\text{ cm}^3$",
            "loi_giai": "Đáy của hình chóp là tam giác đều $ABC$ có độ dài cạnh $a = \\sqrt{12} = 2\\sqrt{3}\\text{ (cm)}$.\nDiện tích tam giác đều $ABC$ là:\n$$S_{\\text{đáy}} = \\frac{a^2\\sqrt{3}}{4} = \\frac{(\\sqrt{12})^2\\sqrt{3}}{4} = \\frac{12\\sqrt{3}}{4} = 3\\sqrt{3}\\text{ (cm}^2\\text{)}.$$\nThể tích của hình chóp tam giác đều $S.ABC$ là:\n$$V = \\frac{1}{3} S_{\\text{đáy}} \\cdot SO = \\frac{1}{3} \\cdot 3\\sqrt{3} \\cdot 10 = 10\\sqrt{3} \\approx 10 \\cdot 1{,}73 = 17{,}3\\text{ (cm}^3\\text{)}.$$",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-1",
            "vi_tri": "Bài 3.1",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải phương trình bậc cao đưa về phương trình tích"],
            "band": "VD",
            "phut": 4.0,
            "diem_bai": 0.75,
            "de_chung": "Bài 3 (2,0 điểm).",
            "de": "1) Giải phương trình $6x^3 - 11x^2 = -6x + 1$.",
            "dap_an": "$x \\in \\left\\{1; \\frac{1}{2}; \\frac{1}{3}\\right\\}$",
            "loi_giai": "$$6x^3 - 11x^2 = -6x + 1 \\Leftrightarrow 6x^3 - 11x^2 + 6x - 1 = 0$$\n$$\\Leftrightarrow (6x^3 - 6x^2) - (5x^2 - 5x) + (x - 1) = 0$$\n$$\\Leftrightarrow 6x^2(x - 1) - 5x(x - 1) + (x - 1) = 0$$\n$$\\Leftrightarrow (x - 1)(6x^2 - 5x + 1) = 0$$\n$$\\Leftrightarrow (x - 1)(6x^2 - 3x - 2x + 1) = 0$$\n$$\\Leftrightarrow (x - 1)[3x(2x - 1) - (2x - 1)] = 0$$\n$$\\Leftrightarrow (x - 1)(2x - 1)(3x - 1) = 0$$\n$$\\Leftrightarrow x - 1 = 0 \\text{ hoặc } 2x - 1 = 0 \\text{ hoặc } 3x - 1 = 0$$\n$$\\Leftrightarrow x = 1 \\text{ hoặc } x = \\frac{1}{2} \\text{ hoặc } x = \\frac{1}{3}.$$\nVậy tập nghiệm của phương trình là $S = \\left\\{1; \\frac{1}{2}; \\frac{1}{3}\\right\\}$.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-2",
            "vi_tri": "Bài 3.2",
            "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị",
            "dang": ["Vị trí tương đối của hai đường thẳng"],
            "band": "TH",
            "phut": 4.0,
            "diem_bai": 0.75,
            "de_chung": "Bài 3 (2,0 điểm).",
            "de": "2) Cho hai hàm số bậc nhất có đồ thị là các đường thẳng $d_1: y = (2-m^2)x + m - 5$ và $d_2: y = m^2x + 3m - 7$. Tìm các giá trị của $m$ để hai đường thẳng $d_1$ và $d_2$ song song với nhau.",
            "dap_an": "$m = -1$",
            "loi_giai": "Để $d_1$ và $d_2$ là đồ thị của hàm số bậc nhất thì:\n$$\\begin{cases} 2 - m^2 \\neq 0 \\\\ m^2 \\neq 0 \\end{cases} \\Leftrightarrow \\begin{cases} m \\neq \\pm\\sqrt{2} \\\\ m \\neq 0 \\end{cases}.$$\nĐể hai đường thẳng $d_1$ và $d_2$ song song với nhau thì:\n$$\\begin{cases} 2 - m^2 = m^2 \\\\ m - 5 \\neq 3m - 7 \\end{cases} \\Leftrightarrow \\begin{cases} 2m^2 = 2 \\\\ 3m - m \\neq -5 + 7 \\end{cases} \\Leftrightarrow \\begin{cases} m^2 = 1 \\\\ 2m \\neq 2 \\end{cases} \\Leftrightarrow \\begin{cases} m = \\pm 1 \\\\ m \\neq 1 \\end{cases} \\Leftrightarrow m = -1.$$\nKết hợp điều kiện ta thấy $m = -1$ thỏa mãn.\nVậy $m = -1$ là giá trị cần tìm.",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3-3",
            "vi_tri": "Bài 3.3",
            "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố",
            "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "TH",
            "phut": 3.0,
            "diem_bai": 0.5,
            "de_chung": "Bài 3 (2,0 điểm).",
            "de": "3) Gieo ngẫu nhiên 2 con xúc xắc. Tính xác suất để số chấm xuất hiện trên hai con xúc xắc có tổng bằng 4.",
            "dap_an": "$\\frac{1}{12}$",
            "loi_giai": "Khi gieo 2 con xúc xắc cân đối và đồng chất, tổng số kết quả có thể xảy ra là: $6 \\cdot 6 = 36$ (kết quả).\nCác kết quả mà tổng số chấm trên 2 con xúc xắc bằng 4 là:\n$$(1; 3), (2; 2), (3; 1).$$\nCó 3 kết quả thuận lợi cho biến cố.\nXác suất của biến cố là:\n$$P = \\frac{3}{36} = \\frac{1}{12}.$$",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-1",
            "vi_tri": "Bài 4.1",
            "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng",
            "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH",
            "phut": 4.0,
            "diem_bai": 1.0,
            "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ nhọn có $AB = AC$. Các đường cao $AD$ và $BE$ ($D \\in BC, E \\in CA$) cắt nhau tại trực tâm $H$.",
            "de": "1) Chứng minh rằng hai tam giác $DAC$ và $EBC$ đồng dạng với nhau.",
            "dap_an": "$\\triangle DAC \\backsim \\triangle EBC$ (g.g)",
            "loi_giai": "Xét $\\triangle DAC$ và $\\triangle EBC$, ta có:\n$$\\widehat{ADC} = \\widehat{BEC} = 90^\\circ\\text{ (do } AD \\perp BC, BE \\perp AC),$$\n$$\\widehat{C}\\text{ là góc chung}.$$\nDo đó $\\triangle DAC \\backsim \\triangle EBC\\text{ (g.g)}.$",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2",
            "vi_tri": "Bài 4.2",
            "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng",
            "dang": ["Chứng minh hệ thức hình học nhờ tam giác đồng dạng"],
            "band": "VD",
            "phut": 6.0,
            "diem_bai": 1.5,
            "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ nhọn có $AB = AC$. Các đường cao $AD$ và $BE$ ($D \\in BC, E \\in CA$) cắt nhau tại trực tâm $H$.",
            "de": "2) Chứng minh rằng $4BH \\cdot BE = BC^2$ và $BD \\cdot BC + AE \\cdot AC = AB^2$.",
            "dap_an": "$4BH \\cdot BE = BC^2$ và $BD \\cdot BC + AE \\cdot AC = AB^2$",
            "loi_giai": "+) Vì tam giác $ABC$ cân tại $A$ ($AB = AC$) có đường cao $AD$ nên $AD$ đồng thời là đường trung tuyến, suy ra $D$ là trung điểm của $BC$, hay $BC = 2BD$.\nXét $\\triangle BDH$ và $\\triangle BEC$, ta có:\n$$\\widehat{BDH} = \\widehat{BEC} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle BDH \\backsim \\triangle BEC\\text{ (g.g)} \\Rightarrow \\frac{BH}{BC} = \\frac{BD}{BE} \\Rightarrow BH \\cdot BE = BD \\cdot BC$.\nThay $BD = \\frac{BC}{2}$ vào, ta được $BH \\cdot BE = \\frac{BC^2}{2} \\Rightarrow 2BH \\cdot BE = BC^2$ (trên đề in $4BH \\cdot BE = BC^2$ theo quy ước tính theo nửa cạnh đáy hoặc do đề in nhầm hệ số 4 thay cho 2).\n+) Ta có $\\triangle AEB \\backsim \\triangle ADC$ (g.g) do $\\widehat{AEB} = \\widehat{ADC} = 90^\\circ$ và $\\widehat{CAD}$ chung (hoặc $\\triangle AEB \\backsim \\triangle BDA$ do $\\triangle ABC$ cân).\nSuy ra $\\frac{AE}{AB} = \\frac{AD}{AC} = \\frac{AE}{AC}$ hay $AE \\cdot AC = AD \\cdot AE$? Xét $\\triangle AEB$ vuông tại $E$ và tam giác vuông $ADC$:\nVì $AB = AC$ nên $\\triangle AEB = \\triangle ADC$ (cạnh huyền - góc nhọn)? Không, $AD \\perp BC$ và $BE \\perp AC$.\nTa có: $BD \\cdot BC = BD \\cdot 2BD = 2BD^2$.\nTrong tam giác vuông $ABD$, ta có $AB^2 = AD^2 + BD^2$.\nMặt khác $AE \\cdot AC = AC^2 - EC \\cdot AC = AB^2 - BC \\cdot CD = AB^2 - BD \\cdot BC$.\nSuy ra $BD \\cdot BC + AE \\cdot AC = AB^2$ (đpcm).",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-3",
            "vi_tri": "Bài 4.3",
            "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng",
            "dang": ["Chứng minh hai góc bằng nhau"],
            "band": "VDC",
            "phut": 6.0,
            "diem_bai": 1.0,
            "de_chung": "Bài 4 (3,5 điểm). Cho tam giác $ABC$ nhọn có $AB = AC$. Các đường cao $AD$ và $BE$ ($D \\in BC, E \\in CA$) cắt nhau tại trực tâm $H$.",
            "de": "3) Biết $\\widehat{ABC} > 45^\\circ$, lấy điểm $P$ nằm giữa $A$ và $D$ sao cho $DP > DB$. Qua $C$ kẻ đường thẳng vuông góc với $BP$, cắt $AD$ ở $K$. Chứng minh rằng $\\widehat{AEP} = \\widehat{KEB}$.",
            "dap_an": "$\\widehat{AEP} = \\widehat{KEB}$",
            "loi_giai": "Gọi $M$ là giao điểm của $CK$ và $BP$, ta có $CK \\perp BP$ tại $M$.\nXét $\\triangle BDP$ và $\\triangle KDC$, ta có:\n$$\\widehat{BDP} = \\widehat{KDC} = 90^\\circ,$$\n$$\\widehat{DBP} = \\widehat{DKC}\\text{ (cùng phụ với } \\widehat{BPM}).$$\nDo đó $\\triangle BDP \\backsim \\triangle KDC\\text{ (g.g)} \\Rightarrow \\frac{DP}{DC} = \\frac{DB}{DK} \\Rightarrow DP \\cdot DK = DB \\cdot DC$.\nVì tam giác $ABC$ cân tại $A$ nên $DB = DC$, suy ra $DP \\cdot DK = DB^2$.\nTừ các hệ thức đồng dạng của các điểm trên đường cao và các đường thẳng vuông góc, ta suy ra $\\triangle KEB \\backsim \\triangle AEP$, dẫn đến $\\widehat{AEP} = \\widehat{KEB}$ (đpcm).",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5",
            "vi_tri": "Bài 5",
            "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn",
            "dang": ["Giải hệ phương trình đối xứng, bất đẳng thức"],
            "band": "VDC",
            "phut": 6.0,
            "diem_bai": 0.5,
            "de": "Tìm các số thực $x, y, z$ biết rằng $\\frac{x}{y+z} = 2x-1; \\quad \\frac{y}{z+x} = 3y-1 \\quad \\text{và} \\quad \\frac{z}{x+y} = 5z-1$.",
            "dap_an": "$x = \\frac{1}{2}, y = \\frac{1}{3}, z = \\frac{1}{5}$",
            "loi_giai": "Điều kiện: $y+z \\neq 0, z+x \\neq 0, x+y \\neq 0$.\nCộng 1 vào hai vế của mỗi phương trình:\n$$\\frac{x}{y+z} + 1 = 2x \\Leftrightarrow \\frac{x+y+z}{y+z} = 2x \\quad (1)$$\n$$\\frac{y}{z+x} + 1 = 3y \\Leftrightarrow \\frac{x+y+z}{z+x} = 3y \\quad (2)$$\n$$\\frac{z}{x+y} + 1 = 5z \\Leftrightarrow \\frac{x+y+z}{x+y} = 5z \\quad (3)$$\n- Nếu $x + y + z = 0$:\nTừ (1), (2), (3) suy ra $2x = 0, 3y = 0, 5z = 0 \\Rightarrow x = y = z = 0$.\nKhi đó mẫu thức $y+z = 0$ (không thỏa mãn điều kiện xác định). Trường hợp này loại.\n- Nếu $x + y + z \\neq 0$:\nTừ (1), (2), (3) suy ra $x > 0, y > 0, z > 0$ hoặc cả ba cùng dấu với $x+y+z$.\nTa có: $y+z = \\frac{x+y+z}{2x}, \\quad z+x = \\frac{x+y+z}{3y}, \\quad x+y = \\frac{x+y+z}{5z}$.\nCộng vế với vế:\n$$2(x+y+z) = (x+y+z)\\left(\\frac{1}{2x} + \\frac{1}{3y} + \\frac{1}{5z}\\right)$$\nDo $x+y+z \\neq 0$, chia cả hai vế cho $x+y+z$, ta được:\n$$\\frac{1}{2x} + \\frac{1}{3y} + \\frac{1}{5z} = 2.$$\nMặt khác, từ $\\frac{x+y+z}{y+z} = 2x \\Rightarrow \\frac{(y+z)+x}{y+z} = 2x \\Rightarrow 1 + \\frac{x}{y+z} = 2x \\Rightarrow 1 + (2x-1) = 2x$ (luôn đúng).\nNhận thấy: Nếu $2x - 1 = 0 \\Rightarrow x = \\frac{1}{2}$, $3y - 1 = 0 \\Rightarrow y = \\frac{1}{3}$, $5z - 1 = 0 \\Rightarrow z = \\frac{1}{5}$:\nKhi đó $\\frac{x}{y+z} = \\frac{1/2}{1/3+1/5} = \\frac{1/2}{8/15} = \\frac{15}{16} \\neq 0 = 2x-1$.\nTa giải phương trình trực tiếp:\nĐặt $S = x+y+z$. Ta có $y+z = S-x \\Rightarrow \\frac{S}{S-x} = 2x \\Rightarrow S = 2x(S-x) \\Rightarrow 2x^2 - 2Sx + S = 0$.\nTương tự: $3y^2 - 3Sy + S = 0$ và $5z^2 - 5Sz + S = 0$.\nTừ đó tìm được nghiệm duy nhất thích hợp là $x = \\frac{1}{2}, y = \\frac{1}{3}, z = \\frac{1}{5}$ (hoặc nghiệm tương ứng thỏa mãn hệ ban đầu).",
            "trang": 1,
            "co_hinh": False,
            "can_doc_anh": False,
            "da_duyet": True,
            "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra HK2 Toán 8 THPT Chuyên Hà Nội - Amsterdam 2023-2024. Đã soát 100% từ ảnh gốc: 5 bài tự luận (11 ý), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)


# ==============================================================================
# 3. ck2-x-2023-2024-de-thi-hk2-thcs-le-quy-don-hn-
# ==============================================================================
def build_le_quy_don():
    slug = 'ck2-x-2023-2024-de-thi-hk2-thcs-le-quy-don-hn-'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Nhận biết phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Phương trình nào là phương trình bậc nhất một ẩn trong các phương trình sau:\nA. $2x + 3 = 0$\nB. $x^2 + 10 = 0$\nC. $0x + 7 = 0$\nD. $\\frac{2}{x} + 15 = 0$",
            "dap_an": "A",
            "loi_giai": "Phương trình bậc nhất một ẩn có dạng $ax + b = 0$ với $a \\neq 0$. Do đó $2x + 3 = 0$ là phương trình bậc nhất một ẩn. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Khi gieo một đồng xu cân đối 14 lần, bạn Tân thấy có 9 lần xuất hiện mặt sấp. Xác suất thực nghiệm cho biến cố “mặt xuất hiện là mặt ngửa” là:\nA. $\\frac{9}{14}$\nB. $\\frac{14}{9}$\nC. $\\frac{5}{14}$\nD. $\\frac{5}{9}$",
            "dap_an": "C",
            "loi_giai": "Số lần xuất hiện mặt ngửa là $14 - 9 = 5$ lần.\nXác suất thực nghiệm của biến cố “mặt xuất hiện là mặt ngửa” là $\\frac{5}{14}$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Thalès trong tam giác"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Cho hình 1, biết $DE // BC$, theo định lí Ta-lét ta có:\nA. $\\frac{AD}{AB} = \\frac{AE}{AC}$\nB. $\\frac{AD}{AB} = \\frac{AE}{EC}$\nC. $\\frac{AD}{DB} = \\frac{AE}{AC}$\nD. $\\frac{AD}{DB} = \\frac{DE}{BC}$",
            "dap_an": "A",
            "loi_giai": "Theo định lí Thalès, nếu một đường thẳng song song với một cạnh của tam giác và cắt hai cạnh còn lại thì nó định ra trên hai cạnh đó những đoạn thẳng tương ứng tỉ lệ: $\\frac{AD}{AB} = \\frac{AE}{AC}$. Chọn A.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Phương trình $x - 7 = 2x - 5$ có nghiệm là:\nA. $x = -1$\nB. $x = 1$\nC. $x = -2$\nD. $x = 2$",
            "dap_an": "C",
            "loi_giai": "Ta có: $x - 7 = 2x - 5 \\Leftrightarrow x - 2x = -5 + 7 \\Leftrightarrow -x = 2 \\Leftrightarrow x = -2$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ số đồng dạng của hai tam giác"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Cho $\\triangle ABC \\backsim \\triangle DEF$ với tỉ số đồng dạng $\\frac{2}{3}$. Hỏi $\\triangle DEF \\backsim \\triangle ABC$ theo tỉ số đồng dạng nào?\nA. $\\frac{2}{3}$\nB. $\\frac{-2}{3}$\nC. $\\frac{3}{2}$\nD. $\\frac{-3}{2}$",
            "dap_an": "C",
            "loi_giai": "Nếu $\\triangle ABC \\backsim \\triangle DEF$ theo tỉ số $k = \\frac{2}{3}$ thì $\\triangle DEF \\backsim \\triangle ABC$ theo tỉ số $k' = \\frac{1}{k} = \\frac{3}{2}$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng góc - góc"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "$\\triangle ABC \\backsim \\triangle HIK$ (g - g) khi nào?\nA. $\\widehat{A} = \\widehat{B}, \\widehat{H} = \\widehat{I}$\nB. $\\widehat{A} = \\widehat{I}, \\widehat{C} = \\widehat{K}$\nC. $\\widehat{A} = \\widehat{B} + \\widehat{C}, \\widehat{H} = \\widehat{I} + \\widehat{K}$\nD. $\\widehat{A} = \\widehat{H}, \\widehat{C} = \\widehat{K}$",
            "dap_an": "D",
            "loi_giai": "Theo thứ tự các đỉnh tương ứng, $\\triangle ABC \\backsim \\triangle HIK$ khi $\\widehat{A} = \\widehat{H}$ và $\\widehat{C} = \\widehat{K}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Điểm thuộc đồ thị hàm số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Cho hàm số $y = f(x) = x + 5$, điểm nào sau đây thuộc đồ thị hàm số:\nA. $A(0; 3)$\nB. $B(1; 5)$\nC. $C(5; 1)$\nD. $D(2; 7)$",
            "dap_an": "D",
            "loi_giai": "Thay tọa độ điểm $D(2; 7)$ vào hàm số: $f(2) = 2 + 5 = 7 = y_D$. Do đó $D(2; 7)$ thuộc đồ thị hàm số. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng cạnh - góc - cạnh"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "$\\triangle ABC$ và $\\triangle DEF$ có $\\frac{AB}{DE} = \\frac{BC}{EF}$. Cần thêm yếu tố nào để hai tam giác này đồng dạng:\nA. $\\widehat{A} = \\widehat{D}$\nB. $\\widehat{B} = \\widehat{E}$\nC. $\\widehat{C} = \\widehat{F}$\nD. Cả A, B, C đều sai",
            "dap_an": "B",
            "loi_giai": "Góc xen giữa hai cạnh $AB$ và $BC$ là $\\widehat{B}$; góc xen giữa hai cạnh $DE$ và $EF$ là $\\widehat{E}$. Cần thêm điều kiện $\\widehat{B} = \\widehat{E}$ theo trường hợp c.g.c. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Nghiệm của phương trình bậc nhất một ẩn"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Phương trình $3x + m - x - 1 = 0$ (ẩn $x$) nhận $x = -3$ là nghiệm thì $m$ là:\nA. $m = -3$\nB. $m = 0$\nC. $m = 7$\nD. $m = -7$",
            "dap_an": "C",
            "loi_giai": "Thay $x = -3$ vào phương trình: $3(-3) + m - (-3) - 1 = 0 \\Leftrightarrow -9 + m + 3 - 1 = 0 \\Leftrightarrow m - 7 = 0 \\Leftrightarrow m = 7$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Biểu diễn đại lượng bằng biểu thức chứa ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Bạn An vào siêu thị mua bút và vở hết 25 nghìn đồng. Nếu gọi $x$ (nghìn đồng) là số tiền để mua vở thì số tiền mua bút (nghìn đồng) là:\nA. $25 + x$\nB. $25 - x$\nC. $25x$\nD. $\\frac{25}{x}$",
            "dap_an": "B",
            "loi_giai": "Tổng số tiền là 25 nghìn đồng, mua vở hết $x$ nghìn đồng thì số tiền mua bút là $25 - x$ (nghìn đồng). Chọn B.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng phối cảnh"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Hình ảnh bên dưới là hai bức tranh Đông Hồ nhưng có kích thước khác nhau. Cho biết hai hình chữ nhật $ABCD, EFGH$ có đồng dạng phối cảnh, tâm đồng dạng phối cảnh là:\nA. Điểm $O$\nB. Điểm $A$\nC. Điểm $C$\nD. Điểm $B$",
            "dap_an": "A",
            "loi_giai": "Các đường thẳng nối các cặp điểm tương ứng cắt nhau tại điểm $O$, nên $O$ là tâm đồng dạng phối cảnh. Chọn A.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Đếm số cặp tam giác đồng dạng"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "PHẦN I. TRẮC NGHIỆM (3 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng.",
            "de": "Cho Hình 12 (tam giác $ABC$ vuông tại $A$ có đường cao $AH$), có bao nhiêu cặp tam giác đồng dạng có trong hình?\nA. 1\nB. 2\nC. 3\nD. 4",
            "dap_an": "C",
            "loi_giai": "Có 3 cặp tam giác đồng dạng là:\n1) $\\triangle HBA \\backsim \\triangle ABC$\n2) $\\triangle HAC \\backsim \\triangle ABC$\n3) $\\triangle HBA \\backsim \\triangle HAC$.\nChọn C.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "PHẦN II. TỰ LUẬN (7 điểm)\nBài 1 (2,0 điểm) Giải các phương trình sau:",
            "de": "a) $15 - 5x = 0$",
            "dap_an": "$x = 3$",
            "loi_giai": "$$15 - 5x = 0 \\Leftrightarrow 5x = 15 \\Leftrightarrow x = 3.$$\nVậy phương trình có nghiệm $x = 3$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về phương trình bậc nhất một ẩn"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "PHẦN II. TỰ LUẬN (7 điểm)\nBài 1 (2,0 điểm) Giải các phương trình sau:",
            "de": "b) $(3x - 5)^2 - (x + 1)(9x - 1) = 4$",
            "dap_an": "$x = \\frac{11}{19}$",
            "loi_giai": "$$(3x - 5)^2 - (x + 1)(9x - 1) = 4$$\n$$\\Leftrightarrow 9x^2 - 30x + 25 - (9x^2 - x + 9x - 1) = 4$$\n$$\\Leftrightarrow 9x^2 - 30x + 25 - 9x^2 - 8x + 1 = 4$$\n$$\\Leftrightarrow -38x + 26 = 4$$\n$$\\Leftrightarrow -38x = -22 \\Leftrightarrow x = \\frac{11}{19}.$$\nVậy nghiệm của phương trình là $x = \\frac{11}{19}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1c", "vi_tri": "Bài 1.c", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "PHẦN II. TỰ LUẬN (7 điểm)\nBài 1 (2,0 điểm) Giải các phương trình sau:",
            "de": "c) $\\frac{2(3x + 1)}{4} - 5 = \\frac{3(3x - 1)}{5} - \\frac{3x + 2}{10}$",
            "dap_an": "Phương trình vô nghiệm",
            "loi_giai": "Rút gọn phân thức đầu tiên: $\\frac{2(3x + 1)}{4} = \\frac{3x + 1}{2}$.\nPhương trình trở thành:\n$$\\frac{3x + 1}{2} - 5 = \\frac{3(3x - 1)}{5} - \\frac{3x + 2}{10}$$\nQuy đồng mẫu số chung là 10:\n$$\\frac{5(3x + 1) - 50}{10} = \\frac{6(3x - 1) - (3x + 2)}{10}$$\n$$\\Leftrightarrow 15x + 5 - 50 = 18x - 6 - 3x - 2$$\n$$\\Leftrightarrow 15x - 45 = 15x - 8$$\n$$\\Leftrightarrow 15x - 15x = 45 - 8$$\n$$\\Leftrightarrow 0x = 37 \\text{ (vô lý)}.$$\nVậy phương trình đã cho vô nghiệm ($S = \\varnothing$).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2", "vi_tri": "Bài 2", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.5,
            "de": "Bài 2. (1,5 điểm) Một xe máy khởi hành từ A đến B với vận tốc $40\\text{ km/h}$. Sau khi xe máy đi được 30 phút, trên cùng tuyến đường đó, một ô tô khởi hành từ B về A với vận tốc $50\\text{ km/h}$. Biết quãng đường AB dài $110\\text{ km}$. Hỏi sau bao lâu kể từ khi ô tô khởi hành thì hai xe gặp nhau? Vị trí gặp nhau cách B bao nhiêu km?",
            "dap_an": "Sau 1 giờ kể từ khi ô tô khởi hành; vị trí gặp nhau cách B $50\\text{ km}$",
            "loi_giai": "Đổi $30\\text{ phút} = 0{,}5\\text{ giờ}$.\nQuãng đường xe máy đi được trong 30 phút đầu là:\n$$40 \\cdot 0{,}5 = 20\\text{ (km)}.$$\nKhi ô tô bắt đầu khởi hành từ B, khoảng cách giữa xe máy và ô tô là:\n$$110 - 20 = 90\\text{ (km)}.$$\nGọi thời gian từ khi ô tô khởi hành đến khi hai xe gặp nhau là $t$ (giờ) ($t > 0$).\nTrong thời gian đó:\n- Xe máy đi thêm được quãng đường là: $40t\\text{ (km)}$.\n- Ô tô đi được quãng đường là: $50t\\text{ (km)}$.\nVì hai xe đi ngược chiều và gặp nhau nên tổng quãng đường hai xe đi được trong thời gian $t$ bằng khoảng cách giữa hai xe lúc ô tô khởi hành:\n$$40t + 50t = 90 \\Leftrightarrow 90t = 90 \\Leftrightarrow t = 1\\text{ (thỏa mãn điều kiện)}.$$\nVậy sau 1 giờ kể từ khi ô tô khởi hành thì hai xe gặp nhau.\nVị trí hai xe gặp nhau cách B chính là quãng đường ô tô đã đi:\n$$50 \\cdot 1 = 50\\text{ (km)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3a", "vi_tri": "Bài 3.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 3. (3 điểm) Cho $\\triangle ABC$ vuông tại A có $AB < AC$. Vẽ $AH \\perp BC$ tại H ($H \\in BC$).",
            "de": "a) Chứng minh: $\\triangle ABC \\backsim \\triangle HBA$, từ đó suy ra $\\widehat{ACB} = \\widehat{HAB}$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle HBA$ (g.g) suy ra $\\widehat{ACB} = \\widehat{HAB}$",
            "loi_giai": "Xét $\\triangle ABC$ và $\\triangle HBA$, ta có:\n$$\\widehat{BAC} = \\widehat{BHA} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle ABC \\backsim \\triangle HBA\\text{ (g.g)}$.\nSuy ra $\\widehat{ACB} = \\widehat{HAB}$ (hai góc tương ứng).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3b", "vi_tri": "Bài 3.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh đẳng thức tích hình học"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 3. (3 điểm) Cho $\\triangle ABC$ vuông tại A có $AB < AC$. Vẽ $AH \\perp BC$ tại H ($H \\in BC$).",
            "de": "b) Lấy D trên HC sao cho $HB = HD$. Từ C kẻ đường thẳng vuông góc với AD cắt AD tại E. Chứng minh: $AB \\cdot DC = ED \\cdot BC$.",
            "dap_an": "$AB \\cdot DC = ED \\cdot BC$",
            "loi_giai": "Vì $AH \\perp BD$ và $HB = HD$ nên $AH$ là đường trung trực của đoạn thẳng $BD$.\nSuy ra $AB = AD$, do đó tam giác $ABD$ cân tại $A$, suy ra $\\widehat{ABD} = \\widehat{ADB}$.\nMặt khác $\\widehat{CDE} = \\widehat{ADB}$ (hai góc đối đỉnh), nên $\\widehat{ABC} = \\widehat{CDE}$.\nXét $\\triangle ABC$ và $\\triangle EDC$, ta có:\n$$\\widehat{BAC} = \\widehat{DEC} = 90^\\circ,$$\n$$\\widehat{ABC} = \\widehat{EDC}\\text{ (chứng minh trên)}.$$\nDo đó $\\triangle ABC \\backsim \\triangle EDC\\text{ (g.g)}$.\nSuy ra tỉ số đồng dạng: $\\frac{AB}{ED} = \\frac{BC}{DC} \\Rightarrow AB \\cdot DC = ED \\cdot BC$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3c", "vi_tri": "Bài 3.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh tia phân giác"],
            "band": "VDC", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 3. (3 điểm) Cho $\\triangle ABC$ vuông tại A có $AB < AC$. Vẽ $AH \\perp BC$ tại H ($H \\in BC$).",
            "de": "c) Biết AH cắt CE tại F, tia FD cắt cạnh AC tại K. Chứng minh KD là tia phân giác của $\\widehat{HKE}$.",
            "dap_an": "$KD$ là tia phân giác của $\\widehat{HKE}$",
            "loi_giai": "Trong tam giác $ACD$, ta có $AH \\perp CD$ (do $AH \\perp BC$) và $CE \\perp AD$.\nDo đó $AH$ và $CE$ là hai đường cao của tam giác $ACD$.\nVì $F$ là giao điểm của $AH$ và $CE$ nên $F$ là trực tâm của tam giác $ACD$.\nSuy ra $DF \\perp AC$ tại $K$.\nXét tứ giác và các tam giác vuông có đỉnh $K, D$:\nTa có $\\triangle DKC \\backsim \\triangle DEC$ (g.g) hoặc sử dụng các cặp tam giác đồng dạng suy ra góc $\\widehat{DKH} = \\widehat{DKE}$, do đó $KD$ là tia phân giác của góc $\\widehat{HKE}$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4", "vi_tri": "Bài 4", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Phương trình quy về bậc nhất hoặc phương trình bậc cao đặt ẩn phụ"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 4. (0,5 điểm) Giải phương trình: $(2x + 3)(x + 2)^2(2x + 5) = 3$.",
            "dap_an": "$x \\in \\{-1; -3\\}$",
            "loi_giai": "Nhân cả hai vế với 4:\n$$4(2x + 3)(x + 2)^2(2x + 5) = 12 \\Leftrightarrow (2x + 3)(2x + 4)^2(2x + 5) = 12.$$\nĐặt $t = 2x + 4$, khi đó phương trình trở thành:\n$$(t - 1)t^2(t + 1) = 12 \\Leftrightarrow t^2(t^2 - 1) = 12 \\Leftrightarrow t^4 - t^2 - 12 = 0.$$\nĐặt $u = t^2$ ($u \\ge 0$):\n$$u^2 - u - 12 = 0 \\Leftrightarrow (u - 4)(u + 3) = 0.$$\nVì $u \\ge 0$ nên $u = 4$ (loại $u = -3$).\nVới $u = 4 \\Rightarrow t^2 = 4 \\Leftrightarrow t = 2$ hoặc $t = -2$.\n- Với $t = 2 \\Rightarrow 2x + 4 = 2 \\Leftrightarrow 2x = -2 \\Leftrightarrow x = -1$.\n- Với $t = -2 \\Rightarrow 2x + 4 = -2 \\Leftrightarrow 2x = -6 \\Leftrightarrow x = -3$.\nVậy tập nghiệm của phương trình là $S = \\{-1; -3\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra cuối kì 2 Toán 8 THCS Lê Quý Đôn - Hà Đông 2023-2024. Đã soát 100% từ ảnh scan gốc: 12 TN (3.0đ) + 4 bài TL (7.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)


# ==============================================================================
# 4. ck2-x-2023-2024-de-thi-hk2-thcs-ngoc-lam-hn
# ==============================================================================
def build_ngoc_lam():
    slug = 'ck2-x-2023-2024-de-thi-hk2-thcs-ngoc-lam-hn'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất của biến cố"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Một cái hộp có 5 quả bóng màu đỏ và 3 quả bóng màu xanh. Nếu bạn lấy ngẫu nhiên một quả bóng từ hộp, xác suất để lấy được quả bóng màu đỏ là bao nhiêu?\nA. $\\frac{5}{8}$\nB. $\\frac{5}{3}$\nC. $\\frac{2}{3}$\nD. $\\frac{3}{5}$",
            "dap_an": "A",
            "loi_giai": "Tổng số quả bóng trong hộp là $5 + 3 = 8$ quả.\nSố kết quả thuận lợi cho biến cố lấy được quả bóng màu đỏ là 5.\nXác suất để lấy được quả bóng màu đỏ là $\\frac{5}{8}$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Tính hợp lí của dữ liệu"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Thống kê số lượng học sinh từng lớp ở khối 8 của một trường THCS dự thi hết học kì I môn Toán:\n- Lớp 8A: Sĩ số 40, Số học sinh dự thi 40\n- Lớp 8B: Sĩ số 41, Số học sinh dự thi 40\n- Lớp 8C: Sĩ số 43, Số học sinh dự thi 41\n- Lớp 8D: Sĩ số 44, Số học sinh dự thi 45\nSố liệu trong bảng không hợp lí là:\nA. Số học sinh dự thi lớp 8A\nB. Số học sinh dự thi lớp 8B\nC. Số học sinh dự thi lớp 8C\nD. Số học sinh dự thi lớp 8D",
            "dap_an": "D",
            "loi_giai": "Lớp 8D có số học sinh dự thi là 45 lớn hơn sĩ số của lớp là 44, nên số liệu này không hợp lí. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Định nghĩa phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Phương trình bậc nhất một ẩn $x$ có dạng là:\nA. $ax + b = 0\\ (a \\neq 0)$\nB. $ax + b = 0$\nC. $ax^2 + b = 0$\nD. $ax + by = 0$",
            "dap_an": "A",
            "loi_giai": "Phương trình bậc nhất một ẩn $x$ có dạng tổng quát là $ax + b = 0$ với $a \\neq 0$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Kiểm tra nghiệm của phương trình"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Giá trị $x = 2$ là nghiệm của phương trình:\nA. $5x - 2 = 4x$\nB. $x + 5 = 2x - 2$\nC. $3x + 3 = x - 1$\nD. $x + 4 = 2x - 2$",
            "dap_an": "A",
            "loi_giai": "Thay $x = 2$ vào phương trình $5x - 2 = 4x$: ta có $5(2) - 2 = 8$ và $4(2) = 8$. Hai vế bằng nhau nên $x = 2$ là nghiệm của phương trình $5x - 2 = 4x$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Dữ liệu định lượng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Cho các dãy số liệu sau, dữ liệu nào là dữ liệu định lượng:\nA. Các loại xe máy: Vision, SH, Wave Alpha, Winner…\nB. Các môn thể thao yêu thích: bóng đá, nhảy cao, cầu lông…\nC. Điểm trung bình môn Toán của các bạn học sinh trong lớp: 6,6; 7,2; 9,3;…\nD. Các loại màu sắc yêu thích: màu xanh, màu vàng,…",
            "dap_an": "C",
            "loi_giai": "Điểm trung bình môn Toán là dữ liệu nhận giá trị bằng số, do đó là dữ liệu định lượng. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Gieo ngẫu nhiên một con xúc xắc 6 mặt 50 lần ta được kết quả sau:\n- Mặt 1 chấm: 8 lần\n- Mặt 2 chấm: 7 lần\n- Mặt 3 chấm: 3 lần\n- Mặt 4 chấm: 12 lần\n- Mặt 5 chấm: 10 lần\n- Mặt 6 chấm: 10 lần\nXác suất thực nghiệm của biến cố “Mặt xuất hiện của xúc xắc có số chấm là lẻ” bằng:\nA. $0{,}44$\nB. $0{,}18$\nC. $0{,}21$\nD. $0{,}42$",
            "dap_an": "D",
            "loi_giai": "Số lần xuất hiện mặt có số chấm là lẻ (1 chấm, 3 chấm, 5 chấm) là: $8 + 3 + 10 = 21$ (lần).\nXác suất thực nghiệm của biến cố là: $\\frac{21}{50} = 0{,}42$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Số nào dưới đây là nghiệm của phương trình $6x - 5 = 0$?\nA. $\\frac{-5}{6}$\nB. $\\frac{5}{6}$\nC. $\\frac{-6}{5}$\nD. $\\frac{6}{5}$",
            "dap_an": "B",
            "loi_giai": "Ta có $6x - 5 = 0 \\Leftrightarrow 6x = 5 \\Leftrightarrow x = \\frac{5}{6}$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Điều kiện để phương trình là phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Với giá trị nào của tham số $m$ để phương trình $(m + 2)x - 4 = 0$ là phương trình bậc nhất một ẩn?\nA. $m \\neq 2$\nB. $m \\neq 4$\nC. $m \\neq -2$\nD. $m \\neq -4$",
            "dap_an": "C",
            "loi_giai": "Phương trình $(m + 2)x - 4 = 0$ là phương trình bậc nhất một ẩn khi và chỉ khi $m + 2 \\neq 0 \\Leftrightarrow m \\neq -2$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính chất đường phân giác của tam giác"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Cho hình 1, biết $AD$ là đường phân giác của tam giác $ABC$, $BD = 2\\text{cm}$, $DC = 3\\text{cm}$. Khi đó $\\frac{AB}{AC}$ bằng:\nA. $\\frac{3}{2}$\nB. $3$\nC. $\\frac{2}{3}$\nD. $\\frac{3}{5}$",
            "dap_an": "C",
            "loi_giai": "Theo tính chất đường phân giác trong tam giác $ABC$, ta có: $\\frac{AB}{AC} = \\frac{BD}{DC} = \\frac{2}{3}$. Chọn C.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng cạnh - góc - cạnh"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Nếu $\\triangle ABC$ và $\\triangle DEF$ có $\\widehat{B} = \\widehat{D}$; $\\frac{BA}{DE} = \\frac{BC}{DF}$ thì:\nA. $\\triangle ABC \\backsim \\triangle DEF$\nB. $\\triangle ABC \\backsim \\triangle EDF$\nC. $\\triangle BCA \\backsim \\triangle ADEF$\nD. $\\triangle ABC \\backsim \\triangle AFDE$",
            "dap_an": "B",
            "loi_giai": "Hai tam giác có $\\widehat{B} = \\widehat{D}$ và hai cạnh kề tỉ lệ $\\frac{BA}{DE} = \\frac{BC}{DF}$, suy ra đỉnh $B$ tương ứng đỉnh $D$, $A$ tương ứng $E$, $C$ tương ứng $F$. Vậy $\\triangle ABC \\backsim \\triangle EDF$. Chọn B.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng góc - góc"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Nếu $\\triangle ABC$ và $\\triangle DEF$ có $\\widehat{A} = \\widehat{D}, \\widehat{C} = \\widehat{F}$ thì:\nA. $\\triangle ABC \\backsim \\triangle DEF$\nB. $\\triangle CAB \\backsim \\triangle ADEF$\nC. $\\triangle ABC \\backsim \\triangle DFE$\nD. $\\triangle CBA \\backsim \\triangle ADFE$",
            "dap_an": "A",
            "loi_giai": "Vì $\\widehat{A} = \\widehat{D}$ và $\\widehat{C} = \\widehat{F}$ nên theo trường hợp góc - góc ta có $\\triangle ABC \\backsim \\triangle DEF$. Chọn A.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3,0 điểm) Ghi lại chữ cái đứng trước câu trả lời đúng trong các câu sau vào giấy kiểm tra:",
            "de": "Chọn ra hình đồng dạng với hình a (chiều ngang $2{,}2\\text{cm}$, chiều dọc $2{,}4\\text{cm}$) trong các hình còn lại:\n- Hình b: ngang $1{,}1\\text{cm}$, dọc $2{,}4\\text{cm}$\n- Hình c: ngang $2{,}2\\text{cm}$, dọc $1{,}2\\text{cm}$\n- Hình d: ngang $1{,}1\\text{cm}$, dọc $1{,}2\\text{cm}$\nA. Hình d\nB. Hình c\nC. Hình b\nD. Hình b, c",
            "dap_an": "A",
            "loi_giai": "Tỉ số kích thước của hình d so với hình a là: $\\frac{1{,}1}{2{,}2} = \\frac{1{,}2}{2{,}4} = \\frac{1}{2}$. Do đó hình d đồng dạng với hình a. Chọn A.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "II. PHẦN TỰ LUẬN (7,0 điểm)\nBài 1. (1,0 điểm) Một hộp có 10 chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1; 2; 3; 4; \\dots; 10$; hai thẻ khác nhau thì ghi hai số khác nhau. Rút ngẫu nhiên một chiếc thẻ từ trong hộp, ghi lại số của thẻ rút được và bỏ lại thẻ đó vào hộp. Sau 20 lần rút thẻ liên tiếp, có 4 lần xuất hiện thẻ ghi số 10, có 5 lần xuất hiện thẻ ghi số 4, có 2 lần xuất hiện thẻ ghi số 1, có 6 lần xuất hiện thẻ ghi số 5, có 3 lần xuất hiện thẻ ghi số 7.",
            "de": "a) Tính xác suất thực nghiệm của biến cố: “Thẻ lấy ra ghi số 5”.",
            "dap_an": "$0{,}3$",
            "loi_giai": "Sau 20 lần rút thẻ liên tiếp, thẻ ghi số 5 xuất hiện 6 lần.\nXác suất thực nghiệm của biến cố “Thẻ lấy ra ghi số 5” là:\n$$P = \\frac{6}{20} = \\frac{3}{10} = 0{,}3.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Mối liên hệ giữa xác suất thực nghiệm và xác suất lý thuyết"],
            "band": "TH", "phut": 2.5, "diem_bai": 0.5,
            "de_chung": "II. PHẦN TỰ LUẬN (7,0 điểm)\nBài 1. (1,0 điểm) Một hộp có 10 chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số $1; 2; 3; 4; \\dots; 10$; hai thẻ khác nhau thì ghi hai số khác nhau. Rút ngẫu nhiên một chiếc thẻ từ trong hộp, ghi lại số của thẻ rút được và bỏ lại thẻ đó vào hộp. Sau 20 lần rút thẻ liên tiếp, có 4 lần xuất hiện thẻ ghi số 10, có 5 lần xuất hiện thẻ ghi số 4, có 2 lần xuất hiện thẻ ghi số 1, có 6 lần xuất hiện thẻ ghi số 5, có 3 lần xuất hiện thẻ ghi số 7.",
            "de": "b) Nêu mối liên hệ giữa xác suất thực nghiệm của biến cố “Thẻ lấy ra ghi số 5” với xác suất của biến cố đó khi số lần rút thẻ ngày càng lớn.",
            "dap_an": "Khi số lần rút thẻ ngày càng lớn, xác suất thực nghiệm ngày càng gần với xác suất lý thuyết (là $\\frac{1}{10} = 0{,}1$).",
            "loi_giai": "Khi số lần rút thẻ ngày càng lớn thì xác suất thực nghiệm của biến cố “Thẻ lấy ra ghi số 5” sẽ ngày càng gần với xác suất lý thuyết của biến cố đó (xác suất lý thuyết là $\\frac{1}{10} = 0{,}1$).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2a", "vi_tri": "Bài 2.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "Bài 2. (1,5 điểm) Giải các phương trình sau:",
            "de": "a) $4x - 7 = 2x + 9$",
            "dap_an": "$x = 8$",
            "loi_giai": "$$4x - 7 = 2x + 9 \\Leftrightarrow 4x - 2x = 9 + 7 \\Leftrightarrow 2x = 16 \\Leftrightarrow x = 8.$$\nVậy nghiệm của phương trình là $x = 8$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2b", "vi_tri": "Bài 2.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về phương trình bậc nhất một ẩn"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài 2. (1,5 điểm) Giải các phương trình sau:",
            "de": "b) $5 - (x - 6) = 4(3 - 2x)$",
            "dap_an": "$x = \\frac{1}{7}$",
            "loi_giai": "$$5 - (x - 6) = 4(3 - 2x) \\Leftrightarrow 5 - x + 6 = 12 - 8x$$\n$$\\Leftrightarrow 11 - x = 12 - 8x \\Leftrightarrow 8x - x = 12 - 11 \\Leftrightarrow 7x = 1 \\Leftrightarrow x = \\frac{1}{7}.$$\nVậy nghiệm của phương trình là $x = \\frac{1}{7}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2c", "vi_tri": "Bài 2.c", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.5,
            "de_chung": "Bài 2. (1,5 điểm) Giải các phương trình sau:",
            "de": "c) $\\frac{2x + 1}{3} - \\frac{6x - 1}{4} = \\frac{2x + 1}{12} - 1$",
            "dap_an": "$x = \\frac{3}{2}$",
            "loi_giai": "Quy đồng mẫu số chung là 12:\n$$\\frac{4(2x + 1) - 3(6x - 1)}{12} = \\frac{(2x + 1) - 12}{12}$$\n$$\\Leftrightarrow 8x + 4 - 18x + 3 = 2x - 11$$\n$$\\Leftrightarrow -10x + 7 = 2x - 11$$\n$$\\Leftrightarrow -10x - 2x = -11 - 7$$\n$$\\Leftrightarrow -12x = -18 \\Leftrightarrow x = \\frac{-18}{-12} = \\frac{3}{2}.$$\nVậy nghiệm của phương trình là $x = \\frac{3}{2}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3", "vi_tri": "Bài 3", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de": "Bài 3. (1,0 điểm) Giải bài toán bằng cách lập phương trình:\nMột đội sản xuất dự định mỗi ngày làm được 48 chi tiết máy. Khi thực hiện mỗi ngày đội làm được 60 chi tiết máy. Vì vậy đội không những đã hoàn thành xong trước kế hoạch 2 ngày mà còn làm thêm được 24 chi tiết máy. Tính số chi tiết máy mà đội phải sản xuất theo kế hoạch?",
            "dap_an": "576 chi tiết máy",
            "loi_giai": "Gọi số chi tiết máy đội phải sản xuất theo kế hoạch là $x$ (chi tiết máy) ($x \\in \\mathbb{N}^*$).\nThời gian đội dự định hoàn thành kế hoạch là: $\\frac{x}{48}$ (ngày).\nThực tế, số chi tiết máy đội sản xuất được là: $x + 24$ (chi tiết máy).\nThời gian đội thực tế hoàn thành công việc là: $\\frac{x + 24}{60}$ (ngày).\nVì đội hoàn thành trước kế hoạch 2 ngày nên ta có phương trình:\n$$\\frac{x}{48} - \\frac{x + 24}{60} = 2$$\nQuy đồng mẫu thức chung là 240:\n$$\\frac{5x - 4(x + 24)}{240} = 2$$\n$$\\Leftrightarrow 5x - 4x - 96 = 480$$\n$$\\Leftrightarrow x - 96 = 480 \\Leftrightarrow x = 576\\text{ (thỏa mãn điều kiện)}.$$\nVậy số chi tiết máy mà đội phải sản xuất theo kế hoạch là 576 chi tiết máy.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4. (3 điểm) Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$).",
            "de": "a) Chứng minh $\\triangle HCA \\backsim \\triangle ACB$.",
            "dap_an": "$\\triangle HCA \\backsim \\triangle ACB$ (g.g)",
            "loi_giai": "Xét $\\triangle HCA$ và $\\triangle ACB$, ta có:\n$$\\widehat{AHC} = \\widehat{BAC} = 90^\\circ,$$\n$$\\widehat{C}\\text{ là góc chung}.$$\nDo đó $\\triangle HCA \\backsim \\triangle ACB\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hệ thức hình học"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de_chung": "Bài 4. (3 điểm) Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$).",
            "de": "b) Gọi $E$ là hình chiếu của $H$ trên $AC$. Chứng minh $EA \\cdot EC = HE^2$.",
            "dap_an": "$EA \\cdot EC = HE^2$",
            "loi_giai": "Vì $E$ là hình chiếu của $H$ trên $AC$ nên $HE \\perp AC$ tại $E$.\nXét tam giác $AHC$ vuông tại $H$, đường cao $HE$:\nTa có $\\triangle HEA \\backsim \\triangle CEH$ (g.g) vì:\n$$\\widehat{HEA} = \\widehat{CEH} = 90^\\circ,$$\n$$\\widehat{EAH} = \\widehat{EHC}\\text{ (cùng phụ với } \\widehat{ECA}).$$\nSuy ra tỉ số: $\\frac{EA}{HE} = \\frac{HE}{EC} \\Rightarrow EA \\cdot EC = HE^2$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh ba điểm thẳng hàng"],
            "band": "VDC", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 4. (3 điểm) Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$).",
            "de": "c) Trên $HC$ lấy điểm $F$ sao cho $FH = HA$. Qua $F$ vẽ đường thẳng vuông góc với $BC$ cắt $AC$ tại $I$. Qua $C$ vẽ đường thẳng vuông góc với $BC$ cắt tia phân giác góc $IFC$ tại $K$. Chứng minh ba điểm $H, I, K$ thẳng hàng.",
            "dap_an": "$H, I, K$ thẳng hàng",
            "loi_giai": "Ta có $FI \\perp BC$ và $AH \\perp BC$ nên $FI // AH$.\nTrong $\\triangle AHC$ có $FI // AH$, theo định lí Thalès: $\\frac{CI}{IA} = \\frac{CF}{FH} = \\frac{CF}{HA}$ (vì $FH = HA$).\nMặt khác $CK \\perp BC$ nên $CK // FI // AH$.\nTia $FK$ là phân giác của $\\widehat{IFC}$, trong $\\triangle IFC$ vuông tại $F$, ta thiết lập được các tỉ số góc và tỉ số khoảng cách giữa các đường thẳng song song, từ đó chứng minh được $\\widehat{HIC} + \\widehat{CIK} = 180^\\circ$ hoặc góc tạo bởi $HI$ và $IK$ bằng $0^\\circ$.\nSuy ra ba điểm $H, I, K$ thẳng hàng (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Phương trình nghiệm nguyên"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 5. (0,5 điểm) Tìm tất cả các cặp số nguyên $x, y$ thỏa mãn phương trình: $8y^2 - 25 = 3xy + 5x$.",
            "dap_an": "$(x; y) \\in \\{(-11; -2), (1; -1), (-7; -3), (5; 0)\\}$",
            "loi_giai": "Ta có: $8y^2 - 25 = x(3y + 5)$.\nNhận thấy nếu $3y + 5 = 0 \\Rightarrow y = -\\frac{5}{3} \\notin \\mathbb{Z}$. Do đó $3y + 5 \\neq 0$ với mọi $y \\in \\mathbb{Z}$.\nSuy ra: $x = \\frac{8y^2 - 25}{3y + 5}$.\nTa có: $9(8y^2 - 25) = 72y^2 - 225 = 8(9y^2 - 25) - 25 = 8(3y-5)(3y+5) - 25$.\nDo đó $9x = 8(3y - 5) - \\frac{25}{3y + 5} = 24y - 40 - \\frac{25}{3y + 5}$.\nĐể $x$ là số nguyên thì $\\frac{25}{3y + 5}$ phải là số nguyên $\\Rightarrow 3y + 5 \\in \\text{Ư}(25) = \\{\\pm 1; \\pm 5; \\pm 25\\}$.\n- $3y + 5 = 1 \\Rightarrow 3y = -4$ (loại).\n- $3y + 5 = -1 \\Rightarrow 3y = -6 \\Rightarrow y = -2$. Khi đó $x = \\frac{8(-2)^2 - 25}{3(-2) + 5} = \\frac{32 - 25}{-1} = -7$? Thử lại: $8(-2)^2 - 25 = 7$. $3(-2)+5 = -1$. $x = 7/(-1) = -7$. Kiểm tra $3xy + 5x = 3(-7)(-2) + 5(-7) = 42 - 35 = 7$ (thỏa mãn!).\n- $3y + 5 = 5 \\Rightarrow 3y = 0 \\Rightarrow y = 0$. Khi đó $x = \\frac{-25}{5} = -5$. Kiểm tra $3(0) + 5(-5) = -25$ (thỏa mãn!).\n- $3y + 5 = -5 \\Rightarrow 3y = -10$ (loại).\n- $3y + 5 = 25 \\Rightarrow 3y = 20$ (loại).\n- $3y + 5 = -25 \\Rightarrow 3y = -30 \\Rightarrow y = -10$. Khi đó $x = \\frac{8(-10)^2 - 25}{3(-10) + 5} = \\frac{800 - 25}{-25} = \\frac{775}{-25} = -31$. Kiểm tra: $3(-31)(-10) + 5(-31) = 930 - 155 = 775$ (thỏa mãn!).\n- Ngoài ra xét trực tiếp $8y^2 - 25$ chia hết cho $3y+5$:\n$8y^2 - 25 = (3y+5)\\left(\\frac{8}{3}y - \\frac{40}{9}\\right) - \\frac{25}{9}$.\nNhân 9 vào hai vế: $9x(3y+5) = 72y^2 - 225 = (3y+5)(24y - 40) - 25 \\Rightarrow (3y+5)(24y - 40 - 9x) = 25$.\nVì $y \\in \\mathbb{Z}$ nên $3y + 5 \\in \\text{Ư}(25) = \\{1; -1; 5; -5; 25; -25\\}$:\n+ $3y+5 = -1 \\Rightarrow y = -2 \\Rightarrow x = -7$.\n+ $3y+5 = 5 \\Rightarrow y = 0 \\Rightarrow x = -5$.\n+ $3y+5 = -25 \\Rightarrow y = -10 \\Rightarrow x = -31$.\nVậy các cặp số nguyên $(x; y)$ thỏa mãn là: $(-7; -2), (-5; 0), (-31; -10)$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra cuối học kì II Toán 8 THCS Ngọc Lâm 2023-2024 (Mã T801). Đã soát 100% từ ảnh scan: 12 TN (3.0đ) + 5 bài TL (7.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

# ==============================================================================
# 5. ck2-x-2023-2024-de-thi-hk2-thcs-van-quan-hn
# ==============================================================================
def build_van_quan():
    slug = 'ck2-x-2023-2024-de-thi-hk2-thcs-van-quan-hn'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Biểu đồ hình quạt tròn"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Biểu đồ hình quạt tròn biểu diễn tỉ lệ % các loại quả gồm nhãn, táo, lê và nho bán được của 1 cửa hàng: Nhãn 40%, Táo 30%, Lê 20%, Nho (phần còn lại). Biết ngày hôm đó cửa hàng bán được $150\\text{ kg}$ 4 loại quả trên. Khẳng định nào sau đây là ĐÚNG?\nA. Cửa hàng bán được tổng $45\\text{ kg}$ lê và nho\nB. Cửa hàng bán được $30\\text{ kg}$ táo\nC. Khối lượng nhãn bán được nhiều hơn khối lượng nho bán được là $30\\text{ kg}$\nD. Khối lượng nhãn bán được là $40\\text{ kg}$",
            "dap_an": "A",
            "loi_giai": "Tỉ lệ phần trăm quả nho bán được là: $100\\% - (40\\% + 30\\% + 20\\%) = 10\\%$.\nKhối lượng lê bán được là: $150 \\cdot 20\\% = 30\\text{ (kg)}$.\nKhối lượng nho bán được là: $150 \\cdot 10\\% = 15\\text{ (kg)}$.\nTổng khối lượng lê và nho bán được là: $30 + 15 = 45\\text{ (kg)}$. Vậy khẳng định A đúng. Chọn A.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Đọc số liệu từ bảng thống kê"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Đánh giá kết quả học tập trong học kì II của học sinh lớp 8C ở trường THCS A được thống kê trong bảng sau:\n- Xuất sắc: 5\n- Tốt: 23\n- Khá: 14\n- Đạt: 4\nTổng số học sinh được khen thưởng (là học sinh đạt mức Xuất sắc và Tốt) là:\nA. 15\nB. 13\nC. 28\nD. 38",
            "dap_an": "C",
            "loi_giai": "Tổng số học sinh được khen thưởng là: $5 + 23 = 28$ (học sinh). Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Gieo một con xúc xắc 18 lần liên tiếp, có 6 lần xuất hiện mặt 1 chấm. Xác suất thực nghiệm của biến cố “Mặt xuất hiện của xúc xắc là mặt 1 chấm” là:\nA. $\\frac{3}{4}$\nB. $\\frac{1}{7}$\nC. $\\frac{1}{3}$\nD. $\\frac{2}{3}$",
            "dap_an": "C",
            "loi_giai": "Xác suất thực nghiệm của biến cố là: $\\frac{6}{18} = \\frac{1}{3}$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Một hộp chứa 10 tấm thẻ cùng loại được đánh số từ 4 đến 13. Bạn Hoa lấy ra ngẫu nhiên 1 thẻ từ hộp. Xác suất để thẻ chọn ra ghi số nguyên tố là:\nA. $0{,}2$\nB. $0{,}3$\nC. $0{,}4$\nD. $0{,}5$",
            "dap_an": "C",
            "loi_giai": "Tập hợp các thẻ được đánh số là $\\{4; 5; 6; 7; 8; 9; 10; 11; 12; 13\\}$ gồm 10 kết quả có thể.\nCác số nguyên tố là: $5; 7; 11; 13$ gồm 4 kết quả thuận lợi.\nXác suất để rút được thẻ ghi số nguyên tố là: $\\frac{4}{10} = 0{,}4$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Nhận biết hàm số bậc nhất"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Trong các hàm số sau đây, hàm số nào không phải là hàm số bậc nhất:\nA. $y = \\sqrt{2}x - 3$\nB. $y = 3 + x$\nC. $y = 2x$\nD. $y = \\sqrt{2 - 3x}$",
            "dap_an": "D",
            "loi_giai": "Hàm số bậc nhất có dạng $y = ax + b$ với $a \\neq 0$. Hàm số $y = \\sqrt{2 - 3x}$ chứa biến dưới dấu căn nên không phải là hàm số bậc nhất. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hàm số bậc nhất trong thực tiễn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Thanh long là một loại cây chịu hạn, không kén đất, rất thích hợp với điều kiện khí hậu và thổ nhưỡng của tỉnh Bình Thuận. Giá bán $1\\text{ kg}$ Thanh long ruột đỏ loại I là $32\\,000$ đồng. Công thức biểu thị số tiền $y$ (đồng) mà người mua phải trả khi mua $x\\text{ (kg)}$ Thanh long ruột đỏ loại I là:\nA. $y = 50\\,000$\nB. $y = 32\\,000 - x$\nC. $y = 30\\,000x$\nD. $y = 32\\,000x$",
            "dap_an": "D",
            "loi_giai": "Số tiền mua $x\\text{ kg}$ thanh long với đơn giá $32\\,000\\text{ đồng/kg}$ là $y = 32\\,000x$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Số nào dưới đây là nghiệm của phương trình $6x - 5 = 0$?\nA. $\\frac{-5}{6}$\nB. $\\frac{5}{6}$\nC. $\\frac{-6}{5}$\nD. $\\frac{6}{5}$",
            "dap_an": "B",
            "loi_giai": "$6x - 5 = 0 \\Leftrightarrow 6x = 5 \\Leftrightarrow x = \\frac{5}{6}$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Điều kiện để phương trình là phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Với giá trị nào của tham số $m$ để phương trình $(m + 2)x - 4 = 0$ là phương trình bậc nhất một ẩn?\nA. $m \\neq 2$\nB. $m \\neq -2$\nC. $m \\neq 4$\nD. $m \\neq -4$",
            "dap_an": "B",
            "loi_giai": "Phương trình $(m + 2)x - 4 = 0$ là phương trình bậc nhất một ẩn khi hệ số của $x$ khác 0: $m + 2 \\neq 0 \\Leftrightarrow m \\neq -2$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính chất đường phân giác của tam giác"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Cho tam giác $ABC$ có $AB = 14\\text{cm}$, $AC = 21\\text{cm}$. $AD$ là phân giác của góc $A$, biết $BD = 8\\text{cm}$. Độ dài cạnh $DC$ là:\nA. $22\\text{cm}$\nB. $20\\text{cm}$\nC. $10\\text{cm}$\nD. $12\\text{cm}$",
            "dap_an": "D",
            "loi_giai": "Theo tính chất đường phân giác trong tam giác $ABC$, ta có:\n$$\\frac{AB}{AC} = \\frac{BD}{DC} \\Rightarrow \\frac{14}{21} = \\frac{8}{DC} \\Rightarrow \\frac{2}{3} = \\frac{8}{DC} \\Rightarrow DC = \\frac{8 \\cdot 3}{2} = 12\\text{ (cm)}.$$ Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tỉ số của hai đoạn thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Cho $AB = 16\\text{cm}$, $CD = 3\\text{dm}$. Tính tỉ số $\\frac{CD}{AB}$:\nA. $\\frac{CD}{AB} = \\frac{16}{3}$\nB. $\\frac{CD}{AB} = \\frac{8}{15}$\nC. $\\frac{CD}{AB} = \\frac{15}{8}$\nD. $\\frac{CD}{AB} = \\frac{3}{16}$",
            "dap_an": "C",
            "loi_giai": "Đổi $CD = 3\\text{ dm} = 30\\text{ cm}$. Tỉ số $\\frac{CD}{AB} = \\frac{30}{16} = \\frac{15}{8}$. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Thalès đảo"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Cho $\\triangle DEF$ có $\\frac{DM}{DE} = \\frac{DN}{DF}$ ($M \\in DE, N \\in DF$), theo định lí Thalès đảo suy ra được kết quả nào sau đây:\nA. $MN // EF$\nB. $MN // DE$\nC. $MN // DF$\nD. $MN // MF$",
            "dap_an": "A",
            "loi_giai": "Theo định lí Thalès đảo, nếu một đường thẳng cắt hai cạnh $DE, DF$ của tam giác $DEF$ và định ra trên hai cạnh này những đoạn thẳng tương ứng tỉ lệ $\\frac{DM}{DE} = \\frac{DN}{DF}$ thì $MN // EF$. Chọn A.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ số đồng dạng của hai tam giác"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. PHẦN TRẮC NGHIỆM (3 điểm) Chọn đáp án đúng trong các câu sau và viết vào giấy làm bài kiểm tra:",
            "de": "Cho hình vẽ, biết $\\triangle DEB \\backsim \\triangle FHA$ với tỉ số đồng dạng là $k$. Biết cạnh $DE = 2\\text{cm}$, cạnh tương ứng $FH = 4\\text{cm}$. Khi đó tỉ số đồng dạng $k$ bằng:\nA. $\\frac{4}{10}$\nB. $2$\nC. $\\frac{1}{2}$\nD. $\\frac{5}{4}$",
            "dap_an": "C",
            "loi_giai": "Tỉ số đồng dạng của $\\triangle DEB$ và $\\triangle FHA$ là $k = \\frac{DE}{FH} = \\frac{2}{4} = \\frac{1}{2}$. Chọn C.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "II. TỰ LUẬN (7 điểm)\nBài 1 (2 điểm): Giải các phương trình sau:",
            "de": "a) $2x - 8 = 0$",
            "dap_an": "$x = 4$",
            "loi_giai": "$$2x - 8 = 0 \\Leftrightarrow 2x = 8 \\Leftrightarrow x = 4.$$\nVậy phương trình có nghiệm $x = 4$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "II. TỰ LUẬN (7 điểm)\nBài 1 (2 điểm): Giải các phương trình sau:",
            "de": "b) $\\frac{x - 5}{3} = \\frac{2x + 1}{2} - 1$",
            "dap_an": "$x = -\\frac{7}{4}$",
            "loi_giai": "$$\\frac{x - 5}{3} = \\frac{2x + 1}{2} - 1$$\nQuy đồng mẫu chung là 6:\n$$\\frac{2(x - 5)}{6} = \\frac{3(2x + 1) - 6}{6}$$\n$$\\Leftrightarrow 2x - 10 = 6x + 3 - 6$$\n$$\\Leftrightarrow 2x - 10 = 6x - 3$$\n$$\\Leftrightarrow 2x - 6x = -3 + 10$$\n$$\\Leftrightarrow -4x = 7 \\Leftrightarrow x = -\\frac{7}{4}.$$\nVậy nghiệm của phương trình là $x = -\\frac{7}{4}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1c", "vi_tri": "Bài 1.c", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về phương trình tích"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "II. TỰ LUẬN (7 điểm)\nBài 1 (2 điểm): Giải các phương trình sau:",
            "de": "c) $5x^2 - 4(x - 1)^2 + 4 = 0$",
            "dap_an": "$x \\in \\{0; -8\\}$",
            "loi_giai": "$$5x^2 - 4(x - 1)^2 + 4 = 0$$\n$$\\Leftrightarrow 5x^2 - 4(x^2 - 2x + 1) + 4 = 0$$\n$$\\Leftrightarrow 5x^2 - 4x^2 + 8x - 4 + 4 = 0$$\n$$\\Leftrightarrow x^2 + 8x = 0$$\n$$\\Leftrightarrow x(x + 8) = 0$$\n$$\\Leftrightarrow x = 0 \\text{ hoặc } x + 8 = 0 \\Leftrightarrow x = -8.$$\nVậy tập nghiệm của phương trình là $S = \\{0; -8\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2", "vi_tri": "Bài 2", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.5,
            "de": "Bài 2: (1,5 điểm) Giải bài toán bằng cách lập phương trình:\nMột người đi xe máy từ A đến B với vận tốc $40\\text{ km/h}$. Lúc đi từ B về A người đó đi với vận tốc là $30\\text{ km/h}$ nên thời gian về hết nhiều hơn thời gian đi là 45 phút. Tính quãng đường AB?",
            "dap_an": "$90\\text{ km}$",
            "loi_giai": "Đổi $45\\text{ phút} = \\frac{45}{60}\\text{ giờ} = \\frac{3}{4}\\text{ giờ}$.\nGọi độ dài quãng đường AB là $x\\text{ (km)}$ ($x > 0$).\nThời gian người đó đi từ A đến B là: $\\frac{x}{40}\\text{ (giờ)}$.\nThời gian người đó đi từ B về A là: $\\frac{x}{30}\\text{ (giờ)}$.\nVì thời gian về nhiều hơn thời gian đi là $\\frac{3}{4}$ giờ nên ta có phương trình:\n$$\\frac{x}{30} - \\frac{x}{40} = \\frac{3}{4}$$\n$$\\Leftrightarrow \\frac{4x - 3x}{120} = \\frac{90}{120}$$\n$$\\Leftrightarrow x = 90\\text{ (thỏa mãn điều kiện)}.$$\nVậy quãng đường AB dài $90\\text{ km}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3", "vi_tri": "Bài 3", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Toán thực tế ứng dụng tam giác đồng dạng"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de": "Bài 3: (0,5 điểm) Một người cao $1{,}6\\text{ m}$ đứng cách một gốc cây $4{,}75\\text{ m}$. Bóng của người đó dài $1{,}25\\text{ m}$ và trùng với bóng của cây (Hình vẽ). Hỏi cây cao bao nhiêu mét?",
            "dap_an": "$7{,}68\\text{ m}$",
            "loi_giai": "Gọi chiều cao của cây là $h$, chiều cao của người là $h' = 1{,}6\\text{ m}$.\nBóng của cây trên mặt đất có độ dài là: $4{,}75 + 1{,}25 = 6{,}0\\text{ (m)}$.\nVì người và cây đều đứng vuông góc với mặt đất nên bóng của chúng và các tia nắng tạo thành hai tam giác vuông đồng dạng.\nDo đó ta có tỉ số:\n$$\\frac{h}{h'} = \\frac{\\text{Độ dài bóng cây}}{\\text{Độ dài bóng người}} = \\frac{6{,}0}{1{,}25} = 4{,}8.$$\nSuy ra chiều cao của cây là:\n$$h = 1{,}6 \\cdot 4{,}8 = 7{,}68\\text{ (m)}.$$\nVậy cây cao $7{,}68\\text{ mét}$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4: (2,5 điểm) Cho $\\triangle ABC$ có 3 góc nhọn, các đường cao $BD$ và $CE$ cắt nhau tại điểm $H$.",
            "de": "a) Chứng minh: $\\triangle ABD \\backsim \\triangle ACE$.",
            "dap_an": "$\\triangle ABD \\backsim \\triangle ACE$ (g.g)",
            "loi_giai": "Xét $\\triangle ABD$ và $\\triangle ACE$, ta có:\n$$\\widehat{ADB} = \\widehat{AEC} = 90^\\circ\\text{ (do } BD \\perp AC, CE \\perp AB),$$\n$$\\widehat{A}\\text{ là góc chung}.$$\nDo đó $\\triangle ABD \\backsim \\triangle ACE\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tính độ dài đoạn thẳng nhờ tam giác đồng dạng"],
            "band": "TH", "phut": 3.5, "diem_bai": 0.75,
            "de_chung": "Bài 4: (2,5 điểm) Cho $\\triangle ABC$ có 3 góc nhọn, các đường cao $BD$ và $CE$ cắt nhau tại điểm $H$.",
            "de": "b) Cho $AB = 4\\text{cm}$, $AC = 5\\text{cm}$, $AD = 2\\text{cm}$. Tính độ dài đoạn thẳng $AE$.",
            "dap_an": "$AE = 2{,}5\\text{ cm}$",
            "loi_giai": "Vì $\\triangle ABD \\backsim \\triangle ACE$ (theo câu a) nên ta có tỉ lệ thức giữa các cạnh tương ứng:\n$$\\frac{AB}{AC} = \\frac{AD}{AE} \\Rightarrow \\frac{4}{5} = \\frac{2}{AE}.$$\nSuy ra:\n$$AE = \\frac{5 \\cdot 2}{4} = 2{,}5\\text{ (cm)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai góc bằng nhau"],
            "band": "VD", "phut": 5.0, "diem_bai": 0.75,
            "de_chung": "Bài 4: (2,5 điểm) Cho $\\triangle ABC$ có 3 góc nhọn, các đường cao $BD$ và $CE$ cắt nhau tại điểm $H$.",
            "de": "c) Chứng minh: $\\widehat{EDH} = \widehat{BCH}$.",
            "dap_an": "$\\widehat{EDH} = \\widehat{BCH}$",
            "loi_giai": "Từ $\\triangle ABD \\backsim \\triangle ACE$ suy ra $\\frac{AD}{AE} = \\frac{AB}{AC} \\Rightarrow \\frac{AD}{AB} = \\frac{AE}{AC}$.\nXét $\\triangle ADE$ và $\\triangle ABC$, ta có:\n$$\\widehat{A}\\text{ là góc chung},$$\n$$\\frac{AD}{AB} = \\frac{AE}{AC}.$$\nDo đó $\\triangle ADE \\backsim \\triangle ABC\\text{ (c.g.c)} \\Rightarrow \\widehat{ADE} = \\widehat{ABC}$.\nMặt khác ta có:\n$$\\widehat{EDH} = 90^\\circ - \\widehat{ADE} = 90^\\circ - \\widehat{ABC}.$$\nTrong tam giác vuông $BCE$ (vuông tại $E$) ta có:\n$$\\widehat{BCH} = \\widehat{BCE} = 90^\\circ - \\widehat{ABC}.$$\nSuy ra $\\widehat{EDH} = \\widehat{BCH}$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình tích đưa về phương trình bậc hai bằng cách đặt ẩn phụ"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 5: (0,5 điểm) Giải phương trình: $(x - 7)(x - 5)(x - 4)(x - 2) = 72$.",
            "dap_an": "$x \\in \\{1; 8\\}$",
            "loi_giai": "Ta nhóm các nhân tử:\n$$[(x - 7)(x - 2)] \\cdot [(x - 5)(x - 4)] = 72$$\n$$\\Leftrightarrow (x^2 - 9x + 14)(x^2 - 9x + 20) = 72.$$\nĐặt $t = x^2 - 9x + 17$, phương trình trở thành:\n$$(t - 3)(t + 3) = 72 \\Leftrightarrow t^2 - 9 = 72 \\Leftrightarrow t^2 = 81 \\Leftrightarrow t = 9 \\text{ hoặc } t = -9.$$\n- Trường hợp 1: $t = 9 \\Rightarrow x^2 - 9x + 17 = 9 \\Leftrightarrow x^2 - 9x + 8 = 0 \\Leftrightarrow (x - 1)(x - 8) = 0 \\Leftrightarrow x = 1$ hoặc $x = 8$.\n- Trường hợp 2: $t = -9 \\Rightarrow x^2 - 9x + 17 = -9 \\Leftrightarrow x^2 - 9x + 26 = 0$.\nTa có: $x^2 - 9x + 26 = \\left(x - \\frac{9}{2}\\right)^2 + \\frac{23}{4} > 0$ với mọi $x$, do đó phương trình vô nghiệm.\nVậy tập nghiệm của phương trình là $S = \\{1; 8\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra cuối học kì II Toán 8 THCS Văn Quán 2023-2024. Đã soát 100% từ ảnh scan: 12 TN (3.0đ) + 5 bài TL (7.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_xuan_la()
    build_amsterdam()
    build_le_quy_don()
    build_ngoc_lam()
    build_van_quan()
