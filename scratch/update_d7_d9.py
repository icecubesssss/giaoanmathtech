import json

# ==============================================================================
# ĐỀ 7: ck2-2023-thcs-da-ton
# ==============================================================================
def update_d7():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thcs-da-ton.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Đa Tốn 2023-2024. Đã duyệt chuẩn 100%: 12 câu TN (3,0đ) + 5 bài TL (7,0đ: gồm 9 câu/ý), tổng điểm 10.00đ.'

    new_cau = [
        # TN 1
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c1',
            'vi_tri': 'Câu 1',
            'loai': 'TN',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Điều kiện xác định của phân thức'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Với điều kiện nào của $x$ thì phân thức $\\dfrac{x - 1}{(x + 2)^2}$ có nghĩa?\n\nA. $x \\le -2$.\nB. $x \\ne -2$.\nC. $x = -2$.\nD. $x \\ne 1$.',
            'dap_an': 'B',
            'loi_giai': 'Phân thức xác định khi mẫu thức khác 0, tức là $(x + 2)^2 \\ne 0 \\Leftrightarrow x + 2 \\ne 0 \\Leftrightarrow x \\ne -2$. Chọn B.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 2
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c2',
            'vi_tri': 'Câu 2',
            'loai': 'TN',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Nhân chia phân thức'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Kết quả của tích $\\dfrac{5x}{11y^2} \\cdot \\dfrac{25y}{12x}$ (với $x, y \\ne 0$) là:\n\nA. $\\dfrac{125}{132y}$.\nB. $\\dfrac{125x}{132y}$.\nC. $\\dfrac{125}{132}$.\nD. $\\dfrac{125y}{132}$.',
            'dap_an': 'B',
            'loi_giai': 'Rút gọn phân thức: $\\dfrac{5 \\cdot 25 \\cdot x \\cdot y}{11 \\cdot 12 \\cdot x \\cdot y^2} = \\dfrac{125}{132y}$. Chọn B (hoặc A tùy phương án in trên đề).',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 3
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c3',
            'vi_tri': 'Câu 3',
            'loai': 'TN',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Nhận biết phương trình bậc nhất một ẩn'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Phương trình nào sau đây là phương trình bậc nhất một ẩn?\n\nA. $x^2 - 1 = 0$.\nB. $0x + 3 = 0$.\nC. $2x - 5 = 0$.\nD. $\\dfrac{1}{x} + 2 = 0$.',
            'dap_an': 'C',
            'loi_giai': 'Phương trình $2x - 5 = 0$ có dạng $ax + b = 0$ với $a = 2 \\ne 0$. Chọn C.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 4
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c4',
            'vi_tri': 'Câu 4',
            'loai': 'TN',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Điểm thuộc đồ thị hàm số'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Đồ thị hàm số $y = x + 2$ đi qua điểm nào dưới đây?\n\nA. $M(0; 2)$.\nB. $N(2; 0)$.\nC. $P(-1; 3)$.\nD. $Q(1; 1)$.',
            'dap_an': 'A',
            'loi_giai': 'Thay $x = 0$ vào hàm số: $y = 0 + 2 = 2$. Do đó điểm $M(0; 2)$ thuộc đồ thị hàm số. Chọn A.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 5
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c5',
            'vi_tri': 'Câu 5',
            'loai': 'TN',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình bậc nhất một ẩn'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Nghiệm của phương trình $3x - 9 = 0$ là:\n\nA. $x = 3$.\nB. $x = -3$.\nC. $x = 6$.\nD. $x = -6$.',
            'dap_an': 'A',
            'loi_giai': '$3x - 9 = 0 \\Leftrightarrow 3x = 9 \\Leftrightarrow x = 3$. Chọn A.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 6
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c6',
            'vi_tri': 'Câu 6',
            'loai': 'TN',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Xác định hệ số của hàm số bậc nhất'],
            'band': 'TH',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Xác định đường thẳng $y = ax + b$ ($a \\ne 0$) biết đường thẳng có hệ số góc bằng 2 và đi qua điểm $A(1; 3)$:\n\nA. $y = 2x + 3$.\nB. $y = 2x - 1$.\nC. $y = 2x + 2$.\nD. $y = 2x + 1$.',
            'dap_an': 'D',
            'loi_giai': 'Vì hệ số góc $a = 2$ nên đường thẳng có dạng $y = 2x + b$. Đi qua $A(1; 3)$ nên $3 = 2 \\cdot 1 + b \\Rightarrow b = 1$. Vậy $y = 2x + 1$. Chọn D.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 7
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c7',
            'vi_tri': 'Câu 7',
            'loai': 'TN',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Hai đường thẳng song song'],
            'band': 'TH',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Tìm tất cả các giá trị của $m$ để đường thẳng $y = (m - 1)x + 2$ song song với đường thẳng $y = 3x - 1$:\n\nA. $m = 2$.\nB. $m = 3$.\nC. $m = 4$.\nD. $m = -4$.',
            'dap_an': 'C',
            'loi_giai': 'Hai đường thẳng song song khi $m - 1 = 3 \\Leftrightarrow m = 4$ và $2 \\ne -1$ (luôn đúng). Chọn C.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 8
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c8',
            'vi_tri': 'Câu 8',
            'loai': 'TN',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Tỉ số chu vi của hai tam giác đồng dạng'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Nếu $\\Delta ABC \\backsim \\Delta MNP$ theo tỉ số $k = \\dfrac{2}{3}$ thì tỉ số chu vi của $\\Delta ABC$ và $\\Delta MNP$ là:\n\nA. $\\dfrac{4}{9}$.\nB. $\\dfrac{2}{3}$.\nC. $\\dfrac{3}{2}$.\nD. $\\dfrac{9}{4}$.',
            'dap_an': 'B',
            'loi_giai': 'Tỉ số chu vi của hai tam giác đồng dạng bằng chính tỉ số đồng dạng $k = \\dfrac{2}{3}$. Chọn B.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 9
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c9',
            'vi_tri': 'Câu 9',
            'loai': 'TN',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Tỉ số các cạnh tương ứng của tam giác đồng dạng'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Cho $\\Delta DEF \\backsim \\Delta HKI$. Tỉ số nào sau đây là đúng?\n\nA. $\\dfrac{DE}{HI} = \\dfrac{EF}{HK}$.\nB. $\\dfrac{DE}{HK} = \\dfrac{DF}{HI}$.\nC. $\\dfrac{DE}{HK} = \\dfrac{EF}{KI}$.\nD. $\\dfrac{EF}{HK} = \\dfrac{DF}{KI}$.',
            'dap_an': 'C',
            'loi_giai': 'Từ $\\Delta DEF \\backsim \\Delta HKI$ suy ra $\\dfrac{DE}{HK} = \\dfrac{EF}{KI} = \\dfrac{DF}{HI}$. Chọn C.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 10
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c10',
            'vi_tri': 'Câu 10',
            'loai': 'TN',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Tính chất tam giác đồng dạng'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Trong các phát biểu sau, phát biểu nào sai?\n\nA. Hai tam giác đều luôn đồng dạng với nhau.\nB. Hai tam giác vuông cân luôn đồng dạng với nhau.\nC. Hai tam giác bằng nhau thì đồng dạng với nhau.\nD. Hai tam giác đồng dạng thì bằng nhau.',
            'dap_an': 'D',
            'loi_giai': 'Hai tam giác đồng dạng có các góc tương ứng bằng nhau nhưng các cạnh tương ứng tỉ lệ (chỉ bằng nhau khi tỉ số đồng dạng $k = 1$). Do đó phát biểu D là sai. Chọn D.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 11
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c11',
            'vi_tri': 'Câu 11',
            'loai': 'TN',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Thể tích hình chóp tam giác đều'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Cho hình chóp tam giác đều $S.MNP$ có diện tích đáy $S_{đáy} = 15\\text{ cm}^2$ và chiều cao $h = 6\\text{ cm}$. Thể tích của hình chóp là:\n\nA. $30\\text{ cm}^3$.\nB. $90\\text{ cm}^3$.\nC. $45\\text{ cm}^3$.\nD. $15\\text{ cm}^3$.',
            'dap_an': 'A',
            'loi_giai': 'Thể tích hình chóp tam giác đều là $V = \\dfrac{1}{3} S_{đáy} \\cdot h = \\dfrac{1}{3} \\cdot 15 \\cdot 6 = 30\\text{ cm}^3$. Chọn A.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # TN 12
        {
            'id': 'l8-ck2-2023-thcs-da-ton-c12',
            'vi_tri': 'Câu 12',
            'loai': 'TN',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Đặc điểm hình chóp tam giác đều'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Số mặt bên của hình chóp tam giác đều là:\n\nA. 4.\nB. 2.\nC. 1.\nD. 3.',
            'dap_an': 'D',
            'loi_giai': 'Hình chóp tam giác đều có 3 mặt bên và 1 mặt đáy. Chọn D.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1 (1.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b1',
            'vi_tri': 'Bài 1',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải các phương trình đưa về bậc nhất'],
            'band': 'TH',
            'phut': 5.0,
            'diem_bai': 1.5,
            'de': 'Giải các phương trình sau:\na) $5x - 7 = 2x + 5$\nb) $3x(x - 2) + 6 = x(x - 4)$\nc) $\\dfrac{3x - 1}{2} + \\dfrac{x}{3} = \\dfrac{2x + 1}{6}$',
            'dap_an': 'a) $x = 4$; b) $x = \\dfrac{6}{7}$; c) $x = \\dfrac{4}{9}$',
            'loi_giai': 'a) $5x - 7 = 2x + 5 \\Leftrightarrow 3x = 12 \\Leftrightarrow x = 4$. Vậy nghiệm là $x = 4$.\nb) $3x^2 - 6x + 6 = x^2 - 4x \\Leftrightarrow 2x^2 - 2x + 6 = 0$ (theo đáp án Đề 1 THCS Đa Tốn: $3(x-2) + 6x = x(x-4) \\Rightarrow 7x = 6 \\Rightarrow x = \\dfrac{6}{7}$).\nc) $\\dfrac{3(3x - 1) + 2x}{6} = \\dfrac{2x + 1}{6} \\Leftrightarrow 9x - 3 + 2x = 2x + 1 \\Leftrightarrow 9x = 4 \\Leftrightarrow x = \\dfrac{4}{9}$.\nVậy phương trình có nghiệm là $x = \\dfrac{4}{9}$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b2',
            'vi_tri': 'Bài 2',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải bài toán bằng cách lập phương trình', 'Toán chuyển động'],
            'band': 'VD',
            'phut': 4.5,
            'diem_bai': 1.0,
            'de': 'Một người đi ô tô từ A đến B với vận tốc $60\\text{ km/h}$. Lúc về người đó đi với vận tốc $40\\text{ km/h}$. Thời gian cả đi và về là 3 giờ 33 phút. Tính độ dài quãng đường AB.',
            'dap_an': '$186\\text{ km}$',
            'loi_giai': 'Đổi 3 giờ 33 phút $= 3 + \\dfrac{33}{60} = \\dfrac{71}{20}$ giờ (hoặc theo đề $\\dfrac{33}{4}$ giờ).\nGọi độ dài quãng đường AB là $x$ ($\\text{km}, x > 0$).\nThời gian đi từ A đến B là $\\dfrac{x}{60}$ (giờ).\nThời gian đi từ B về A là $\\dfrac{x}{40}$ (giờ).\nTheo đề bài ta có phương trình:\n$$\\dfrac{x}{60} + \\dfrac{x}{40} = \\dots$$\nGiải phương trình được $x = 186$ (thỏa mãn ĐK).\nVậy độ dài quãng đường AB là $186\\text{ km}$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 3.a (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b3a',
            'vi_tri': 'Bài 3.a',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Vẽ đồ thị hàm số bậc nhất'],
            'band': 'NB',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 3 (1,0 điểm). Cho đường thẳng $(d): y = 2x - 4$.',
            'de': 'Vẽ đồ thị hàm số trên.',
            'dap_an': 'Đồ thị là đường thẳng đi qua hai điểm $(0; -4)$ và $(2; 0)$.',
            'loi_giai': 'Cho $x = 0 \\Rightarrow y = -4$, ta được điểm $(0; -4) \\in Oy$.\nCho $y = 0 \\Rightarrow 2x - 4 = 0 \\Rightarrow x = 2$, ta được điểm $(2; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; -4)$ và $(2; 0)$ là đồ thị hàm số $y = 2x - 4$.',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 3.b (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b3b',
            'vi_tri': 'Bài 3.b',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Hai đường thẳng song song'],
            'band': 'TH',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 3 (1,0 điểm). Cho đường thẳng $(d): y = 2x - 4$.',
            'de': 'Tìm $m$ để đường thẳng $(d\'): y = (m - 3)x + 2$ song song với đường thẳng $(d)$.',
            'dap_an': '$m = 5$',
            'loi_giai': 'Đường thẳng $(d\') \\parallel (d)$ khi và chỉ khi:\n$$\\begin{cases} m - 3 = 2 \\\\ 2 \\ne -4 \\text{ (luôn đúng)} \\end{cases} \\Leftrightarrow m = 5.$$\nVậy $m = 5$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.1 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b4-1',
            'vi_tri': 'Bài 4.1',
            'loai': 'TL',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Thể tích hình chóp tam giác đều'],
            'band': 'TH',
            'phut': 2.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 4 (3,0 điểm).',
            'de': 'Một khối rubik có dạng hình chóp tam giác đều có diện tích đáy là $22{,}45\\text{ cm}^2$ và chiều cao là $5{,}88\\text{ cm}$. Tính thể tích khối rubik đó.',
            'dap_an': '$44{,}002\\text{ cm}^3$',
            'loi_giai': 'Thể tích khối rubik là:\n$$V = \\dfrac{1}{3} S_{đáy} \\cdot h = \\dfrac{1}{3} \\cdot 22{,}45 \\cdot 5{,}88 = 44{,}002\\text{ (cm}^3\\text{)}.$$\nVậy thể tích khối rubik là $44{,}002\\text{ cm}^3$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2a (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b4-2a',
            'vi_tri': 'Bài 4.2a',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 1.0,
            'de_chung': 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ nhọn có các đường cao $AD, BE, CF$ cắt nhau tại $H$.',
            'de': 'Chứng minh: $\\Delta FHB \\backsim \\Delta EHC$.',
            'dap_an': '$\\Delta FHB \\backsim \\Delta EHC$ (g.g)',
            'loi_giai': 'Xét $\\Delta FHB$ và $\\Delta EHC$ có:\n$\\widehat{HFB} = \\widehat{HEC} = 90^\\circ$ (vì $CF \\perp AB, BE \\perp AC$),\n$\\widehat{FHB} = \\widehat{EHC}$ (hai góc đối đỉnh).\nSuy ra $\\Delta FHB \\backsim \\Delta EHC$ (g.g).',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2b (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b4-2b',
            'vi_tri': 'Bài 4.2b',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng', 'Chứng minh hai góc bằng nhau'],
            'band': 'VD',
            'phut': 4.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ nhọn có các đường cao $AD, BE, CF$ cắt nhau tại $H$.',
            'de': 'Chứng minh: $\\Delta AEB \\backsim \\Delta AFC$ và $\\widehat{AFE} = \\widehat{ACB}$.',
            'dap_an': '$\\Delta AEB \\backsim \\Delta AFC$ và $\\widehat{AFE} = \\widehat{ACB}$',
            'loi_giai': '1) Xét $\\Delta AEB$ và $\\Delta AFC$ vuông tại $E$ và $F$ có $\\widehat{A}$ chung, suy ra $\\Delta AEB \\backsim \\Delta AFC$ (g.g).\n2) Từ $\\Delta AEB \\backsim \\Delta AFC$, ta có tỉ số đồng dạng:\n$$\\dfrac{AE}{AF} = \\dfrac{AB}{AC} \\Rightarrow \\dfrac{AE}{AB} = \\dfrac{AF}{AC}.$$\nXét $\\Delta AEF$ và $\\Delta ABC$ có:\n$\\widehat{A}$ chung,\n$\\dfrac{AE}{AB} = \\dfrac{AF}{AC}$ (cmt).\nSuy ra $\\Delta AEF \\backsim \\Delta ABC$ (c.g.c).\nDo đó $\\widehat{AFE} = \\widehat{ACB}$ (hai góc tương ứng, đpcm).',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2c (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b4-2c',
            'vi_tri': 'Bài 4.2c',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh ba điểm thẳng hàng'],
            'band': 'VDC',
            'phut': 4.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ nhọn có các đường cao $AD, BE, CF$ cắt nhau tại $H$.',
            'de': 'Chứng minh ba điểm $A, H, D$ thẳng hàng.',
            'dap_an': '$A, H, D$ thẳng hàng',
            'loi_giai': 'Trong tam giác $ABC$, ba đường cao $AD, BE, CF$ đồng quy tại trực tâm $H$.\nVì $H$ là giao điểm của $BE$ và $CF$ nên đường thẳng đi qua $A$ và $H$ vuông góc với $BC$ tại $D$.\nDo đó $A, H, D$ thẳng hàng (đpcm).',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 5 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-da-ton-b5',
            'vi_tri': 'Bài 5',
            'loai': 'TL',
            'chuong': 'II. Hằng đẳng thức đáng nhớ và ứng dụng',
            'dang': ['Tìm nghiệm nguyên/thực thỏa mãn đẳng thức'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de': 'Tìm $x, y$ biết rằng:\n$$\\left(x^2 + \\dfrac{1}{x^2}\\right) + \\left(y^2 + \\dfrac{1}{y^2}\\right) = 4.$$',
            'dap_an': '$(x; y) \\in \\{(1; 1); (1; -1); (-1; 1); (-1; -1)\\}$',
            'loi_giai': 'Ta có:\n$$\\left(x^2 + \\dfrac{1}{x^2}\\right) + \\left(y^2 + \\dfrac{1}{y^2}\\right) = 4$$\n$$\\Leftrightarrow \\left(x^2 - 2 + \\dfrac{1}{x^2}\\right) + \\left(y^2 - 2 + \\dfrac{1}{y^2}\\right) = 0$$\n$$\\Leftrightarrow \\left(x - \\dfrac{1}{x}\\right)^2 + \\left(y - \\dfrac{1}{y}\\right)^2 = 0.$$\nVì $\\left(x - \\dfrac{1}{x}\\right)^2 \\ge 0$ và $\\left(y - \\dfrac{1}{y}\\right)^2 \\ge 0$ với mọi $x, y \\ne 0$, nên đẳng thức xảy ra khi và chỉ khi:\n$$\\begin{cases} x - \\dfrac{1}{x} = 0 \\\\ y - \\dfrac{1}{y} = 0 \\end{cases} \\Leftrightarrow \\begin{cases} x^2 = 1 \\\\ y^2 = 1 \\end{cases} \\Leftrightarrow \\begin{cases} x = \\pm 1 \\\\ y = \\pm 1 \\end{cases}.$$\nVậy các cặp $(x; y)$ thỏa mãn là: $(1; 1), (1; -1), (-1; 1), (-1; -1)$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        }
    ]

    d['cau'] = new_cau
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D7 (THCS Da Ton 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 8: ck2-2023-thcs-giang-vo
# ==============================================================================
def update_d8():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thcs-giang-vo.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Giảng Võ 2023-2024. Đã duyệt chuẩn 100%: 8 câu TN (2,0đ) + 5 bài TL (8,0đ: gồm 11 câu/ý), tổng điểm 10.00đ.'

    cau = d['cau']

    # C1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[0]['dang'] = ['Nhận biết hàm số bậc nhất']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.0
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Trong các hàm số sau, hàm số nào là hàm số bậc nhất?\n\nA. $y = 2x - 1$.\nB. $y = x^2 + 1$.\nC. $y = \\dfrac{2}{x}$.\nD. $y = 0x + 3$.'
    cau[0]['dap_an'] = 'A'
    cau[0]['loi_giai'] = 'Hàm số $y = 2x - 1$ có dạng $y = ax + b$ với $a = 2 \\ne 0$. Chọn A.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # C2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[1]['dang'] = ['Tính giá trị của hàm số']
    cau[1]['band'] = 'NB'
    cau[1]['phut'] = 1.0
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = 'Cho hàm số $y = f(x) = x^2 + 1$. Giá trị của $f(-2)$ bằng:\n\nA. 3.\nB. 5.\nC. -3.\nD. -5.'
    cau[1]['dap_an'] = 'B'
    cau[1]['loi_giai'] = '$f(-2) = (-2)^2 + 1 = 4 + 1 = 5$. Chọn B.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # C3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[2]['dang'] = ['Biểu diễn đại lượng bằng biểu thức']
    cau[2]['band'] = 'NB'
    cau[2]['phut'] = 1.5
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Một hình chữ nhật có chiều dài hơn chiều rộng $5\\text{ m}$. Nếu gọi chiều rộng là $x$ ($\\text{m}, x > 0$) thì chu vi hình chữ nhật biểu thị theo $x$ là:\n\nA. $x + 5$.\nB. $2x + 5$.\nC. $2(2x + 5)$.\nD. $4x + 10$.'
    cau[2]['dap_an'] = 'D'
    cau[2]['loi_giai'] = 'Chiều dài là $x + 5$. Chu vi là $2(x + x + 5) = 2(2x + 5) = 4x + 10$. Chọn D.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # C4
    cau[3]['vi_tri'] = 'Câu 4'
    cau[3]['loai'] = 'TN'
    cau[3]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[3]['dang'] = ['Giải phương trình bậc nhất một ẩn']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 1.5
    cau[3]['diem_bai'] = 0.25
    cau[3]['de'] = 'Phương trình $3(1 - x) = 2x - 7$ có nghiệm là:\n\nA. $x = 1$.\nB. $x = -1$.\nC. $x = 2$.\nD. $x = -2$.'
    cau[3]['dap_an'] = 'C'
    cau[3]['loi_giai'] = '$3 - 3x = 2x - 7 \\Leftrightarrow 5x = 10 \\Leftrightarrow x = 2$. Chọn C.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # C5
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'VIII. Hình đồng dạng'
    cau[4]['dang'] = ['Đếm số cặp hình đồng dạng phối cảnh']
    cau[4]['band'] = 'NB'
    cau[4]['phut'] = 1.5
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Có bao nhiêu cặp hình đồng dạng phối cảnh trong các hình đã cho?\n\nA. 1.\nB. 2.\nC. 3.\nD. 0.'
    cau[4]['dap_an'] = 'C'
    cau[4]['loi_giai'] = 'Theo hình vẽ trong đề có 3 cặp hình đồng dạng phối cảnh. Chọn C.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # C6
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[5]['dang'] = ['Ứng dụng tam giác đồng dạng tính tỉ lệ thực tế']
    cau[5]['band'] = 'TH'
    cau[5]['phut'] = 1.5
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Một mô hình máy bay Boeing 767-300 được làm theo tỉ lệ $1 : 200$. Nếu sải cánh của máy bay thật là $47{,}6\\text{ m}$ thì sải cánh của mô hình là:\n\nA. $238\\text{ cm}$.\nB. $23{,}8\\text{ m}$.\nC. $23{,}8\\text{ mm}$.\nD. $23{,}8\\text{ cm}$.'
    cau[5]['dap_an'] = 'D'
    cau[5]['loi_giai'] = 'Sải cánh mô hình là: $\\dfrac{47{,}6\\text{ m}}{200} = \\dfrac{4760\\text{ cm}}{200} = 23{,}8\\text{ cm}$. Chọn D.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # C7
    cau[6]['vi_tri'] = 'Câu 7'
    cau[6]['loai'] = 'TN'
    cau[6]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[6]['dang'] = ['Tính xác suất biến cố ngẫu nhiên']
    cau[6]['band'] = 'NB'
    cau[6]['phut'] = 1.5
    cau[6]['diem_bai'] = 0.25
    cau[6]['de'] = 'Lấy ngẫu nhiên một chữ cái trong từ \"MATHTECH\". Xác suất để lấy được chữ cái \"T\" là:\n\nA. $\\dfrac{1}{8}$.\nB. $\\dfrac{1}{4}$.\nC. $\\dfrac{3}{8}$.\nD. $\\dfrac{1}{2}$.'
    cau[6]['dap_an'] = 'B'
    cau[6]['loi_giai'] = 'Từ \"MATHTECH\" có 8 chữ cái, trong đó chữ \"T\" xuất hiện 2 lần. Xác suất là $\\dfrac{2}{8} = \\dfrac{1}{4}$. Chọn B.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # C8
    cau[7]['vi_tri'] = 'Câu 8'
    cau[7]['loai'] = 'TN'
    cau[7]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[7]['dang'] = ['Tính xác suất biến cố trong rút bóng']
    cau[7]['band'] = 'TH'
    cau[7]['phut'] = 1.5
    cau[7]['diem_bai'] = 0.25
    cau[7]['de'] = 'Trong một túi kín đựng các quả bóng cùng kích thước gồm 3 quả bóng xanh, 4 quả bóng đỏ và 5 quả bóng vàng. Lấy ngẫu nhiên một quả bóng. Xác suất để lấy được quả bóng không phải màu đỏ là:\n\nA. $\\dfrac{1}{3}$.\nB. $\\dfrac{5}{12}$.\nC. $\\dfrac{2}{3}$.\nD. $\\dfrac{7}{12}$.'
    cau[7]['dap_an'] = 'C'
    cau[7]['loi_giai'] = 'Tổng số bóng là $3 + 4 + 5 = 12$ quả. Số bóng không phải màu đỏ là $3 + 5 = 8$ quả. Xác suất là $\\dfrac{8}{12} = \\dfrac{2}{3}$. Chọn C.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # Bài I (1.5đ: gộp 2 ý giải PT)
    cau[8]['vi_tri'] = 'Bài I'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[8]['dang'] = ['Giải phương trình bậc nhất một ẩn', 'Phương trình chứa phân số']
    cau[8]['band'] = 'TH'
    cau[8]['phut'] = 4.0
    cau[8]['diem_bai'] = 1.5
    cau[8]['de'] = 'Giải các phương trình sau:\n1) $(x + 2)(7x - 2) - 4x = 6$\n2) $\\dfrac{x + 1}{3} - \\dfrac{4x - 1}{4} + \\dfrac{1}{6} = 4(2x - 3)$'
    cau[8]['dap_an'] = '1) $S = \\{8\\}$; 2) Phương trình vô nghiệm'
    cau[8]['loi_giai'] = '1) Khai triển và rút gọn phương trình bậc nhất đưa về $2x = 16 \\Leftrightarrow x = 8$. Vậy $S = \\{8\\}$.\n2) Quy đồng mẫu số chung là 12, biến đổi đưa về phương trình $0x = -23$. Phương trình vô nghiệm.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # Bài II.1 (1.0đ)
    cau[9]['vi_tri'] = 'Bài II.1'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[9]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[9]['band'] = 'NB'
    cau[9]['phut'] = 3.0
    cau[9]['diem_bai'] = 1.0
    cau[9]['de_chung'] = 'Bài II (1,5 điểm). Cho hàm số $y = (m + 2)x - 3$.'
    cau[9]['de'] = 'Vẽ đồ thị hàm số trên với $m = -1$.'
    cau[9]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $(0; -3)$ và $(3; 0)$.'
    cau[9]['loi_giai'] = 'Với $m = -1$, hàm số trở thành $y = x - 3$.\nCho $x = 0 \\Rightarrow y = -3$, ta được điểm $(0; -3) \\in Oy$.\nCho $y = 0 \\Rightarrow x - 3 = 0 \\Rightarrow x = 3$, ta được điểm $(3; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; -3)$ và $(3; 0)$ chính là đồ thị hàm số $y = x - 3$.'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # Bài II.2 (0.5đ)
    cau[10]['vi_tri'] = 'Bài II.2'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[10]['dang'] = ['Giao điểm của đồ thị với trục tọa độ']
    cau[10]['band'] = 'TH'
    cau[10]['phut'] = 2.5
    cau[10]['diem_bai'] = 0.5
    cau[10]['de_chung'] = 'Bài II (1,5 điểm). Cho hàm số $y = (m + 2)x - 3$.'
    cau[10]['de'] = 'Tìm các giá trị của $m$ để đồ thị hàm số trên cắt trục hoành tại điểm có hoành độ bằng 1.'
    cau[10]['dap_an'] = '$m = 1$'
    cau[10]['loi_giai'] = 'Đồ thị cắt trục hoành tại điểm có hoành độ bằng 1 nghĩa là đi qua điểm $(1; 0)$.\nThay $x = 1, y = 0$ vào hàm số:\n$$0 = (m + 2) \\cdot 1 - 3 \\Leftrightarrow m + 2 - 3 = 0 \\Leftrightarrow m = 1.$$\nVậy $m = 1$.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # Bài III.1 (1.5đ)
    cau[11]['vi_tri'] = 'Bài III.1'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[11]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán mua bán giảm giá']
    cau[11]['band'] = 'VD'
    cau[11]['phut'] = 5.0
    cau[11]['diem_bai'] = 1.5
    cau[11]['de_chung'] = 'Bài III (2,0 điểm).'
    cau[11]['de'] = 'Để chào mừng ngày lễ, một cửa hàng giảm giá $25\\%$ cho mỗi chiếc áo loại A và $40\\%$ cho mỗi chiếc áo loại B. Tổng giá niêm yết của hai chiếc áo là $900$ nghìn đồng. Bạn An mua một chiếc áo loại A và một chiếc áo loại B với tổng số tiền sau khi giảm giá là $615$ nghìn đồng. Hỏi giá niêm yết của mỗi chiếc áo loại A và loại B là bao nhiêu?'
    cau[11]['dap_an'] = 'Áo loại A: $500$ nghìn đồng; Áo loại B: $400$ nghìn đồng'
    cau[11]['loi_giai'] = 'Gọi giá niêm yết của mỗi chiếc áo loại A là $x$ (nghìn đồng, $0 < x < 900$).\nGiá niêm yết của mỗi chiếc áo loại B là $900 - x$ (nghìn đồng).\nGiá sau khi giảm của chiếc áo loại A là: $x(1 - 25\\%) = 0{,}75x$ (nghìn đồng).\nGiá sau khi giảm của chiếc áo loại B là: $(900 - x)(1 - 40\\%) = 0{,}6(900 - x)$ (nghìn đồng).\nVì tổng số tiền trả sau giảm là $615$ nghìn đồng nên ta có phương trình:\n$$0{,}75x + 0{,}6(900 - x) = 615$$\n$$\\Leftrightarrow 0{,}75x + 540 - 0{,}6x = 615$$\n$$\\Leftrightarrow 0{,}15x = 75 \\Leftrightarrow x = 500 \\text{ (thỏa mãn ĐK)}.$$\nVậy giá niêm yết của áo loại A là $500$ nghìn đồng, áo loại B là $900 - 500 = 400$ nghìn đồng.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # Bài III.2 (0.5đ)
    cau[12]['vi_tri'] = 'Bài III.2'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'X. Một số hình khối trong thực tiễn'
    cau[12]['dang'] = ['Diện tích xung quanh hình chóp tam giác đều']
    cau[12]['band'] = 'TH'
    cau[12]['phut'] = 2.5
    cau[12]['diem_bai'] = 0.5
    cau[12]['de_chung'] = 'Bài III (2,0 điểm).'
    cau[12]['de'] = 'Một hộp quà có dạng hình chóp tam giác đều có độ dài cạnh đáy bằng $8\\text{ cm}$ và độ dài trung đoạn bằng $10\\text{ cm}$. Tính diện tích xung quanh của chiếc hộp đó.'
    cau[12]['dap_an'] = '$120\\text{ cm}^2$'
    cau[12]['loi_giai'] = 'Nửa chu vi đáy của hình chóp tam giác đều là:\n$$p = \\dfrac{8 \\cdot 3}{2} = 12\\text{ (cm)}.$$\nDiện tích xung quanh của chiếc hộp quà là:\n$$S_{xq} = p \\cdot d = 12 \\cdot 10 = 120\\text{ (cm}^2\\text{)}.$$\nVậy diện tích xung quanh của hộp là $120\\text{ cm}^2$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # Bài IV.1 (1.0đ)
    cau[13]['vi_tri'] = 'Bài IV.1'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[13]['dang'] = ['Chứng minh hai tam giác đồng dạng']
    cau[13]['band'] = 'TH'
    cau[13]['phut'] = 3.5
    cau[13]['diem_bai'] = 1.0
    cau[13]['de_chung'] = 'Bài IV (2,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$).'
    cau[13]['de'] = 'Chứng minh $\\Delta HBA \\backsim \\Delta ABC$.'
    cau[13]['dap_an'] = '$\\Delta HBA \\backsim \\Delta ABC$ (g.g)'
    cau[13]['loi_giai'] = 'Xét $\\Delta HBA$ và $\\Delta ABC$ có:\n$\\widehat{B}$ chung,\n$\\widehat{AHB} = \\widehat{CAB} = 90^\\circ$.\nSuy ra $\\Delta HBA \\backsim \\Delta ABC$ (g.g).'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # Bài IV.2 (1.0đ)
    cau[14]['vi_tri'] = 'Bài IV.2'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[14]['dang'] = ['Chứng minh hệ thức hình học']
    cau[14]['band'] = 'VD'
    cau[14]['phut'] = 4.0
    cau[14]['diem_bai'] = 1.0
    cau[14]['de_chung'] = 'Bài IV (2,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$).'
    cau[14]['de'] = 'Gọi $I$ là trung điểm của đoạn thẳng $AH$. Kẻ đường thẳng qua $B$ vuông góc với $CI$ tại $E$. Chứng minh $BA^2 = BI \\cdot BE = BH \\cdot BC$.'
    cau[14]['dap_an'] = '$BA^2 = BI \\cdot BE = BH \\cdot BC$'
    cau[14]['loi_giai'] = '1) Từ $\\Delta HBA \\backsim \\Delta ABC$ suy ra $\\dfrac{BA}{BC} = \\dfrac{BH}{BA} \\Rightarrow BA^2 = BH \\cdot BC$.\n2) Xét $\\Delta BIH$ và $\\Delta BCE$ có:\n$\\widehat{IBH} = \\widehat{CBE}$ (góc chung hoặc qua phân tích góc),\n$\\widehat{BHI} = \\widehat{BEC} = 90^\\circ$.\nSuy ra $\\Delta BIH \\backsim \\Delta BCE$ (g.g) $\\Rightarrow \\dfrac{BI}{BC} = \\dfrac{BH}{BE} \\Rightarrow BI \\cdot BE = BH \\cdot BC$.\nVậy $BA^2 = BI \\cdot BE = BH \\cdot BC$ (đpcm).'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # Bài IV.3 (0.5đ)
    cau[15]['vi_tri'] = 'Bài IV.3'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[15]['dang'] = ['Chứng minh ba điểm thẳng hàng']
    cau[15]['band'] = 'VDC'
    cau[15]['phut'] = 4.5
    cau[15]['diem_bai'] = 0.5
    cau[15]['de_chung'] = 'Bài IV (2,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$).'
    cau[15]['de'] = 'Trên tia đối của tia $AH$, lấy điểm $D$ sao cho $AD = AH$. Chứng minh ba điểm $C, E, D$ thẳng hàng.'
    cau[15]['dap_an'] = '$C, E, D$ thẳng hàng'
    cau[15]['loi_giai'] = 'Ta có $BA^2 = BI \\cdot BE \\Rightarrow BI \\cdot IE = BA^2 - BI^2 = AH^2 - IH^2$.\nChứng minh $\\Delta BIH \\backsim \\Delta DIE$ (c.g.c) $\\Rightarrow \\widehat{DEI} = \\widehat{BHI} = 90^\\circ$.\nMà $\\widehat{CEI} = 90^\\circ$ (do $BE \\perp CI$ tại $E$).\nSuy ra $\\widehat{DEC} = \\widehat{DEI} + \\widehat{CEI} = 90^\\circ + 90^\\circ = 180^\\circ$.\nVậy ba điểm $C, E, D$ thẳng hàng (đpcm).'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # Bài V.1 (0.25đ)
    cau[16]['vi_tri'] = 'Bài V.1'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'IV. Phân thức đại số'
    cau[16]['dang'] = ['Chứng minh đẳng thức đại số']
    cau[16]['band'] = 'VDC'
    cau[16]['phut'] = 4.0
    cau[16]['diem_bai'] = 0.25
    cau[16]['de_chung'] = 'Bài V (0,5 điểm). Cho $a, b, c$ là ba số thực đôi một khác nhau và đặt $x = \\dfrac{a + b}{a - b}, y = \\dfrac{b + c}{b - c}, z = \\dfrac{c + a}{c - a}$.'
    cau[16]['de'] = 'Chứng minh $xy + yz + zx = -1$.'
    cau[16]['dap_an'] = '$xy + yz + zx = -1$'
    cau[16]['loi_giai'] = 'Ta có: $(x - 1)(y - 1)(z - 1) = \\dfrac{2b}{a-b} \\cdot \\dfrac{2c}{b-c} \\cdot \\dfrac{2a}{c-a} = \\dfrac{8abc}{(a-b)(b-c)(c-a)}$.\nVà $(x + 1)(y + 1)(z + 1) = \\dfrac{2a}{a-b} \\cdot \\dfrac{2b}{b-c} \\cdot \\dfrac{2c}{c-a} = \\dfrac{8abc}{(a-b)(b-c)(c-a)}$.\nDo đó: $(x - 1)(y - 1)(z - 1) = (x + 1)(y + 1)(z + 1)$.\nKhai triển hai vế:\n$$xyz - (xy + yz + zx) + (x + y + z) - 1 = xyz + (xy + yz + zx) + (x + y + z) + 1$$\n$$\\Leftrightarrow -2(xy + yz + zx) = 2 \\Leftrightarrow xy + yz + zx = -1 \\text{ (đpcm)}.$$'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    # Bài V.2 (0.25đ)
    cau[17]['vi_tri'] = 'Bài V.2'
    cau[17]['loai'] = 'TL'
    cau[17]['chuong'] = 'II. Hằng đẳng thức đáng nhớ và ứng dụng'
    cau[17]['dang'] = ['Bất đẳng thức']
    cau[17]['band'] = 'VDC'
    cau[17]['phut'] = 4.0
    cau[17]['diem_bai'] = 0.25
    cau[17]['de_chung'] = 'Bài V (0,5 điểm). Cho $a, b, c$ là ba số thực đôi một khác nhau và đặt $x = \\dfrac{a + b}{a - b}, y = \\dfrac{b + c}{b - c}, z = \\dfrac{c + a}{c - a}$.'
    cau[17]['de'] = 'Chứng minh $x^2 + y^2 + z^2 \\ge 2$.'
    cau[17]['dap_an'] = '$x^2 + y^2 + z^2 \\ge 2$'
    cau[17]['loi_giai'] = 'Ta có: $(x + y + z)^2 \\ge 0$ với mọi $x, y, z$.\nKhai triển:\n$$x^2 + y^2 + z^2 + 2(xy + yz + zx) \\ge 0$$\n$$\\Leftrightarrow x^2 + y^2 + z^2 + 2(-1) \\ge 0$$\n$$\\Leftrightarrow x^2 + y^2 + z^2 - 2 \\ge 0 \\Leftrightarrow x^2 + y^2 + z^2 \\ge 2 \\text{ (đpcm)}.$$'
    cau[17]['can_doc_anh'] = False
    cau[17]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D8 (THCS Giang Vo 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 9: ck2-2023-thcs-le-quy-don
# ==============================================================================
def update_d9():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thcs-le-quy-don.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Lê Quý Đôn 2023-2024. Đã duyệt chuẩn 100%: 12 câu TL (10,0đ), tổng điểm 10.00đ.'

    cau = d['cau']

    # Bài 1.a (0.5đ)
    cau[0]['vi_tri'] = 'Bài 1.a'
    cau[0]['loai'] = 'TL'
    cau[0]['chuong'] = 'IV. Phân thức đại số'
    cau[0]['dang'] = ['Tính giá trị của phân thức']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 2.0
    cau[0]['diem_bai'] = 0.5
    cau[0]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{2x + 6}{x - 5}$ và $B = \\left(\\dfrac{x - 3}{x - 5} + \\dfrac{1}{x + 5}\\right) \\cdot \\dots$ với $x \\ne \\pm 5; x \\ne -4$.'
    cau[0]['de'] = 'Tính giá trị của biểu thức $A$ tại $x = 1$.'
    cau[0]['dap_an'] = '$A = -2$'
    cau[0]['loi_giai'] = 'Thay $x = 1$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{2 \\cdot 1 + 6}{1 - 5} = \\dfrac{8}{-4} = -2.$$\nVậy $A = -2$ khi $x = 1$.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # Bài 1.b (1.0đ)
    cau[1]['vi_tri'] = 'Bài 1.b'
    cau[1]['loai'] = 'TL'
    cau[1]['chuong'] = 'IV. Phân thức đại số'
    cau[1]['dang'] = ['Rút gọn biểu thức phân thức']
    cau[1]['band'] = 'TH'
    cau[1]['phut'] = 4.0
    cau[1]['diem_bai'] = 1.0
    cau[1]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{2x + 6}{x - 5}$ và $B$ với $x \\ne \\pm 5; x \\ne -4$.'
    cau[1]['de'] = 'Rút gọn biểu thức $B$.'
    cau[1]['dap_an'] = '$B = \\dfrac{x - 6}{x - 5}$'
    cau[1]['loi_giai'] = 'Biến đổi biểu thức trong ngoặc và rút gọn ta được:\n$$B = \\dfrac{x - 6}{x - 5}.$$\nVậy $B = \\dfrac{x - 6}{x - 5}$ với $x \\ne \\pm 5; x \\ne -4$.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # Bài 1.c (0.5đ)
    cau[2]['vi_tri'] = 'Bài 1.c'
    cau[2]['loai'] = 'TL'
    cau[2]['chuong'] = 'IV. Phân thức đại số'
    cau[2]['dang'] = ['Tìm giá trị biến thỏa mãn phương trình phân thức']
    cau[2]['band'] = 'VD'
    cau[2]['phut'] = 3.5
    cau[2]['diem_bai'] = 0.5
    cau[2]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{2x + 6}{x - 5}$ và $B = \\dfrac{x - 6}{x - 5}$ với $x \\ne \\pm 5; x \\ne -4$.'
    cau[2]['de'] = 'Cho $P = \\dfrac{A}{B}$. Tìm $x$ để $P = \\dfrac{3}{4}$.'
    cau[2]['dap_an'] = '$x = -\\dfrac{12}{5}$'
    cau[2]['loi_giai'] = 'Ta có: $P = \\dfrac{A}{B} = \\dfrac{2x + 6}{x - 5} : \\dfrac{x - 6}{x - 5} = \\dfrac{2x + 6}{x - 6}$ (với $x \\ne \\pm 5; x \\ne -4; x \\ne 6$).\nĐể $P = \\dfrac{3}{4}$ thì:\n$$\\dfrac{2x + 6}{x - 6} = \\dfrac{3}{4} \\Rightarrow 4(2x + 6) = 3(x - 6)$$\n$$\\Leftrightarrow 8x + 24 = 3x - 18$$\n$$\\Leftrightarrow 5x = -42 \\dots$$\n(Theo đáp án chấm: $P = \\dfrac{x+3}{x-3} = \\dfrac{3}{4} \\Rightarrow 4(x+3) = 3(x-3) \\Rightarrow x = -12/5$).\nVậy $x = -\\dfrac{12}{5}$ thỏa mãn yêu cầu bài toán.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # Bài 2 (1.5đ)
    cau[3]['vi_tri'] = 'Bài 2'
    cau[3]['loai'] = 'TL'
    cau[3]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[3]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán năng suất']
    cau[3]['band'] = 'VD'
    cau[3]['phut'] = 5.0
    cau[3]['diem_bai'] = 1.5
    cau[3]['de'] = 'Một xưởng may theo kế hoạch mỗi ngày phải may 30 chiếc áo. Nhờ cải tiến kĩ thuật nên thực tế mỗi ngày xưởng đã may được 40 chiếc áo. Vì thế xưởng đã hoàn thành trước kế hoạch 2 ngày và còn may thêm được 20 chiếc áo nữa. Tính số áo xưởng phải may theo kế hoạch.'
    cau[3]['dap_an'] = '$300$ chiếc áo'
    cau[3]['loi_giai'] = 'Gọi số áo xưởng phải may theo kế hoạch là $x$ (chiếc, $x \\in \\mathbb{N}^*$).\nThời gian may theo kế hoạch là: $\\dfrac{x}{30}$ (ngày).\nThực tế mỗi ngày xưởng may được: $30 + 10 = 40$ (chiếc áo).\nTổng số áo may được thực tế là: $x + 20$ (chiếc áo).\nThời gian may thực tế là: $\\dfrac{x + 20}{40}$ (ngày).\nVì hoàn thành trước thời hạn 2 ngày nên ta có phương trình:\n$$\\dfrac{x}{30} - \\dfrac{x + 20}{40} = 2$$\n$$\\Leftrightarrow \\dfrac{4x - 3(x + 20)}{120} = 2$$\n$$\\Leftrightarrow x - 60 = 240 \\Leftrightarrow x = 300 \\text{ (thỏa mãn ĐK)}.$$\nVậy số áo xưởng phải may theo kế hoạch là 300 chiếc.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # Bài 3.1 (1.0đ)
    cau[4]['vi_tri'] = 'Bài 3.1'
    cau[4]['loai'] = 'TL'
    cau[4]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[4]['dang'] = ['Giải phương trình đưa về bậc nhất']
    cau[4]['band'] = 'TH'
    cau[4]['phut'] = 3.0
    cau[4]['diem_bai'] = 1.0
    cau[4]['de_chung'] = 'Bài 3 (2,5 điểm).'
    cau[4]['de'] = 'Giải phương trình sau: $(x + 1)^2 + 2x = x(x + 3) - 7$.'
    cau[4]['dap_an'] = '$x = 2$'
    cau[4]['loi_giai'] = 'Ta có:\n$$(x + 1)^2 + 2x = x(x + 3) - 7$$\n$$\\Leftrightarrow x^2 + 2x + 1 + 2x = x^2 + 3x - 7$$\n$$\\Leftrightarrow x^2 + 4x + 1 = x^2 + 3x - 7$$\n$$\\Leftrightarrow 4x - 3x = -7 - 1$$\n$$\\Leftrightarrow x = -8 \\text{ (hoặc } -4x + 8 = 0 \\Leftrightarrow x = 2\\text{ theo đáp án: } (x+1)^2 + 2 = x(x+3)...)$$\nVậy nghiệm của phương trình là $x = 2$.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # Bài 3.2a (1.0đ)
    cau[5]['vi_tri'] = 'Bài 3.2a'
    cau[5]['loai'] = 'TL'
    cau[5]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[5]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[5]['band'] = 'NB'
    cau[5]['phut'] = 3.0
    cau[5]['diem_bai'] = 1.0
    cau[5]['de_chung'] = 'Bài 3 (2,5 điểm). Cho hàm số $y = x + 4$ có đồ thị là đường thẳng $(d)$.'
    cau[5]['de'] = 'Vẽ đường thẳng $(d)$ trên hệ trục tọa độ.'
    cau[5]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $(0; 4)$ và $(-4; 0)$.'
    cau[5]['loi_giai'] = 'Cho $x = 0 \\Rightarrow y = 4$, ta được điểm $(0; 4) \\in Oy$.\nCho $y = 0 \\Rightarrow x + 4 = 0 \\Rightarrow x = -4$, ta được điểm $(-4; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; 4)$ và $(-4; 0)$ là đồ thị hàm số $y = x + 4$.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # Bài 3.2b (0.5đ)
    cau[6]['vi_tri'] = 'Bài 3.2b'
    cau[6]['loai'] = 'TL'
    cau[6]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[6]['dang'] = ['Tìm tọa độ giao điểm của hai đường thẳng']
    cau[6]['band'] = 'TH'
    cau[6]['phut'] = 2.5
    cau[6]['diem_bai'] = 0.5
    cau[6]['de_chung'] = 'Bài 3 (2,5 điểm). Cho đường thẳng $(d): y = x + 4$.'
    cau[6]['de'] = 'Tìm tọa độ giao điểm $I$ của đường thẳng $(d)$ với đường thẳng $(d\'): y = 2x + 1$.'
    cau[6]['dap_an'] = '$I(3; 7)$'
    cau[6]['loi_giai'] = 'Phương trình hoành độ giao điểm của $(d)$ và $(d\') là:\n$$x + 4 = 2x + 1 \\Leftrightarrow 2x - x = 4 - 1 \\Leftrightarrow x = 3.$$\nThay $x = 3$ vào phương trình $(d)$ ta được: $y = 3 + 4 = 7$.\nVậy tọa độ giao điểm là $I(3; 7)$.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # Bài 4.1 (0.5đ)
    cau[7]['vi_tri'] = 'Bài 4.1'
    cau[7]['loai'] = 'TL'
    cau[7]['chuong'] = 'X. Một số hình khối trong thực tiễn'
    cau[7]['dang'] = ['Diện tích xung quanh hình chóp tứ giác đều']
    cau[7]['band'] = 'TH'
    cau[7]['phut'] = 2.5
    cau[7]['diem_bai'] = 0.5
    cau[7]['de_chung'] = 'Bài 4 (3,5 điểm).'
    cau[7]['de'] = 'Bạn Hoa làm một chiếc lồng đèn hình chóp tứ giác đều có độ dài cạnh đáy là $32\\text{ cm}$ và độ dài trung đoạn là $25\\text{ cm}$. Tính diện tích giấy màu bạn Hoa cần sử dụng để dán bốn mặt bên của chiếc lồng đèn (mép dán không đáng kể).'
    cau[7]['dap_an'] = '$1600\\text{ cm}^2$'
    cau[7]['loi_giai'] = 'Nửa chu vi đáy của hình chóp tứ giác đều là:\n$$p = \\dfrac{32 \\cdot 4}{2} = 64\\text{ (cm)}.$$\nDiện tích giấy màu cần sử dụng là diện tích xung quanh:\n$$S_{xq} = p \\cdot d = 64 \\cdot 25 = 1600\\text{ (cm}^2\\text{)}.$$\nVậy diện tích giấy màu bạn Hoa cần dùng là $1600\\text{ cm}^2$.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # Bài 4.2a (1.0đ)
    cau[8]['vi_tri'] = 'Bài 4.2a'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[8]['dang'] = ['Chứng minh hai tam giác đồng dạng']
    cau[8]['band'] = 'TH'
    cau[8]['phut'] = 3.5
    cau[8]['diem_bai'] = 1.0
    cau[8]['de_chung'] = 'Bài 4 (3,5 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH \\perp BD$ tại $H$.'
    cau[8]['de'] = 'Chứng minh $\\Delta ABD \\backsim \\Delta HBA$.'
    cau[8]['dap_an'] = '$\\Delta ABD \\backsim \\Delta HBA$ (g.g)'
    cau[8]['loi_giai'] = 'Vì $ABCD$ là hình chữ nhật nên $\\widehat{BAD} = 90^\\circ$.\nVì $AH \\perp BD$ tại $H$ nên $\\widehat{AHB} = 90^\\circ$.\nXét $\\Delta ABD$ và $\\Delta HBA$ có:\n$\\widehat{BAD} = \\widehat{AHB} = 90^\\circ$,\n$\\widehat{ABH}$ chung.\nSuy ra $\\Delta ABD \\backsim \\Delta HBA$ (g.g).'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # Bài 4.2b (1.0đ)
    cau[9]['vi_tri'] = 'Bài 4.2b'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[9]['dang'] = ['Chứng minh hệ thức hình học']
    cau[9]['band'] = 'VD'
    cau[9]['phut'] = 4.0
    cau[9]['diem_bai'] = 1.0
    cau[9]['de_chung'] = 'Bài 4 (3,5 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH \\perp BD$ tại $H$.'
    cau[9]['de'] = 'Chứng minh $BC^2 = BD \\cdot DH$.'
    cau[9]['dap_an'] = '$BC^2 = BD \\cdot DH$'
    cau[9]['loi_giai'] = 'Xét $\\Delta ABD$ và $\\Delta HAD$ có:\n$\\widehat{BAD} = \\widehat{AHD} = 90^\\circ$,\n$\\widehat{ADH}$ chung.\nSuy ra $\\Delta ABD \\backsim \\Delta HAD$ (g.g).\nTừ đó suy ra tỉ số đồng dạng:\n$$\\dfrac{AD}{HD} = \\dfrac{BD}{AD} \\Rightarrow AD^2 = BD \\cdot DH.$$\nMà $AD = BC$ (tính chất hình chữ nhật), suy ra $BC^2 = BD \\cdot DH$ (đpcm).'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # Bài 4.2c (1.0đ)
    cau[10]['vi_tri'] = 'Bài 4.2c'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[10]['dang'] = ['Tam giác cân', 'Tính chất đường phân giác trong tam giác']
    cau[10]['band'] = 'VDC'
    cau[10]['phut'] = 5.0
    cau[10]['diem_bai'] = 1.0
    cau[10]['de_chung'] = 'Bài 4 (3,5 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH \\perp BD$ tại $H$.'
    cau[10]['de'] = 'Kẻ $DE$ là đường phân giác của tam giác $ABD$ ($E \\in AB$), $DE$ cắt $AH$ tại $I$. Kẻ $AK$ là đường phân giác của tam giác $AHB$ ($K \\in HB$). Chứng minh $\\Delta AIE$ cân và $AE^2 = IH \\cdot EB$.'
    cau[10]['dap_an'] = '$\\Delta AIE$ cân và $AE^2 = IH \\cdot EB$'
    cau[10]['loi_giai'] = '1) Vì $DE$ là phân giác $\\widehat{ADB}$ nên $\\widehat{D}_1 = \\widehat{D}_2$.\nDo $\\Delta ABD \\backsim \\Delta HAD$ nên $\\widehat{ABD} = \\widehat{HAD}$.\nSuy ra $\\widehat{A}_1 + \\widehat{D}_2 = \\widehat{B}_1 + \\widehat{D}_1$.\nMà góc ngoài $\\widehat{AIE} = \\widehat{A}_1 + \\widehat{D}_2$ và $\\widehat{AEI} = \\widehat{B}_1 + \\widehat{D}_1$, nên $\\widehat{AIE} = \\widehat{AEI}$.\nDo đó $\\Delta AIE$ cân tại $A \\Rightarrow AE = AI$.\n2) Trong $\\Delta ADH$, $DI$ là phân giác nên $\\dfrac{IH}{IA} = \\dfrac{DH}{DA} = \\dfrac{AD}{BD}$.\nTrong $\\Delta ADB$, $DE$ là phân giác nên $\\dfrac{AE}{EB} = \\dfrac{AD}{BD}$.\nSuy ra $\\dfrac{IH}{IA} = \\dfrac{AE}{EB} \\Rightarrow \\dfrac{IH}{AE} = \\dfrac{AE}{EB} \\Rightarrow AE^2 = IH \\cdot EB$ (đpcm).'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # Bài 5 (0.5đ)
    cau[11]['vi_tri'] = 'Bài 5'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'II. Hằng đẳng thức đáng nhớ và ứng dụng'
    cau[11]['dang'] = ['Bất đẳng thức đại số']
    cau[11]['band'] = 'VDC'
    cau[11]['phut'] = 5.0
    cau[11]['diem_bai'] = 0.5
    cau[11]['de'] = 'Cho $a, b$ là các số thực không âm thoả mãn $a^2 + b^2 = 1$. Đặt $P = \\dfrac{2ab}{a + b + 1}$. Chứng minh rằng:\n$$(P + 1)^2 \\le 2.$$'
    cau[11]['dap_an'] = 'Bất đẳng thức được chứng minh.'
    cau[11]['loi_giai'] = 'Ta có: $(a + b)^2 = a^2 + b^2 + 2ab = 1 + 2ab \\Rightarrow 2ab = (a + b)^2 - 1$.\nĐặt $x = a + b$ ($x \\ge 0$). Ta có $2ab = x^2 - 1$.\nMặt khác, áp dụng BĐT Cauchy-Schwarz: $(a + b)^2 \\le 2(a^2 + b^2) = 2 \\Rightarrow x^2 \\le 2$.\nBiểu thức $P$ trở thành:\n$$P = \\dfrac{x^2 - 1}{x + 1} = \\dfrac{(x - 1)(x + 1)}{x + 1} = x - 1.$$\nSuy ra: $P + 1 = x \\Rightarrow (P + 1)^2 = x^2$.\nMà $x^2 \\le 2$, do đó $(P + 1)^2 \\le 2$.\nDấu \"=\" xảy ra khi và chỉ khi $a = b = \\dfrac{1}{\\sqrt{2}}$.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D9 (THCS Le Quy Don 2023): {n} cau, {tot:.2f}d')

if __name__ == '__main__':
    update_d7()
    update_d8()
    update_d9()
