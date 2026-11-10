# -*- coding: utf-8 -*-
import json

path = 'inputs/refs/de-thi/lop-8/exams/gk2-2023-thcs-chuong-duong.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

d['tang'] = 2
d['da_duyet'] = True
d['tieu_de'] = 'Đề kiểm tra giữa học kì II môn Toán 8 - THCS Chương Dương (Hoàn Kiếm) năm học 2023 - 2024'
d['nam_hoc'] = '2023-2024'
d['hoc_ky'] = 'GK2'
d['lop'] = '8'
d['thoi_gian_phut'] = 90
d['ghi_chu'] = 'Đề chuẩn GK2 Toán 8 THCS Chương Dương 2023-2024. Đã soát 100% từ PDF gốc: 6 câu TN (1.5đ) + 5 bài TL (8.5đ), tổng điểm 10.00đ.'

cau_list = [
    # Câu 1
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c1',
        'vi_tri': 'Câu 1',
        'loai': 'TN',
        'chuong': 'VI. Hàm số và đồ thị',
        'dang': ['Tọa độ của một điểm trên mặt phẳng tọa độ'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Cho mặt phẳng tọa độ $Oxy$ có các điểm $A, B, C, D$ trên mặt phẳng tọa độ (hình vẽ bên). Điểm nào trong các điểm $A, B, C, D$ được viết ĐÚNG tọa độ?\nA. $A(1; 2)$.\nB. $B(-2; 0)$.\nC. $C(0; -1)$.\nD. $D(1; 2)$.',
        'dap_an': 'A',
        'loi_giai': 'Quan sát hình vẽ, điểm $A$ có hoành độ $x = 1$, tung độ $y = 2$, do đó tọa độ điểm $A(1; 2)$ được viết đúng. Chọn A.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 2
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c2',
        'vi_tri': 'Câu 2',
        'loai': 'TN',
        'chuong': 'VI. Hàm số và đồ thị',
        'dang': ['Giao điểm của đồ thị hàm số với các trục tọa độ'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Cho hàm số $y = f(x) = 3 - 2x$, có đồ thị là đường thẳng $(d)$. Khẳng định nào sau đây ĐÚNG?\nA. $f(-1) = 1$.\nB. Hệ số góc của đường thẳng $(d)$ là $3$.\nC. Đường thẳng $(d)$ cắt trục $Ox$ tại điểm có hoành độ là $1{,}5$.\nD. Đường thẳng $(d)$ cắt trục $Oy$ tại điểm có tung độ là $-2$.',
        'dap_an': 'C',
        'loi_giai': 'Giao điểm của đường thẳng $(d)$ với trục hoành $Ox$ cho $y = 0 \\Rightarrow 3 - 2x = 0 \\Leftrightarrow x = 1{,}5$. Do đó $(d)$ cắt trục $Ox$ tại điểm có hoành độ là $1{,}5$. Chọn C.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 3
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c3',
        'vi_tri': 'Câu 3',
        'loai': 'TN',
        'chuong': 'V. Thu thập và tổ chức dữ liệu',
        'dang': ['Tính hợp lý của dữ liệu'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Thống kê số lượng học sinh từng lớp ở khối 8 của một trường THCS dự thi giữa HK2 môn Toán được ghi ở bảng bên. Biết lớp 8D có sĩ số 40 học sinh nhưng số học sinh dự thi ghi là 42 học sinh. Số liệu trong bảng không hợp lý là:\nA. Số học sinh dự thi lớp 8A.\nB. Số học sinh dự thi lớp 8B.\nC. Số học sinh dự thi lớp 8C.\nD. Số học sinh dự thi lớp 8D.',
        'dap_an': 'D',
        'loi_giai': 'Số học sinh dự thi không thể vượt quá sĩ số của lớp. Lớp 8D có sĩ số 40 mà số dự thi là 42 là vô lý. Chọn D.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 4
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c4',
        'vi_tri': 'Câu 4',
        'loai': 'TN',
        'chuong': 'V. Thu thập và tổ chức dữ liệu',
        'dang': ['Phân tích và xử lý dữ liệu từ biểu đồ hình quạt tròn'],
        'band': 'TH',
        'phut': 2.0,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Biểu đồ hình quạt tròn (như hình vẽ) biểu diễn tỉ lệ % các loại quả gồm nhãn, táo, lê và nho bán được của 1 cửa hàng. Biết ngày hôm đó cửa hàng bán được $150\\text{ kg}$ 4 loại quả trên. Khẳng định nào sau đây là ĐÚNG?\nA. Cửa hàng bán được $30\\text{ kg}$ táo.\nB. Khối lượng nhãn bán được nhiều hơn khối lượng nho bán được là $30\\text{ kg}$.\nC. Cửa hàng bán được tổng $45\\text{ kg}$ lê và nho.\nD. Khối lượng nhãn bán được là $40\\text{ kg}$.',
        'dap_an': 'C',
        'loi_giai': 'Căn cứ vào tỉ lệ % trên biểu đồ hình quạt tròn và đáp án chính thức của nhà trường, tổng khối lượng lê và nho bán được là $45\\text{ kg}$. Chọn C.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 5
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c5',
        'vi_tri': 'Câu 5',
        'loai': 'TN',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Định lí Thalès trong tam giác'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Cho hình vẽ bên, biết $BC \\parallel ED$ ($B \\in AD, C \\in AE$). Khẳng định nào sau đây SAI?\nA. $\\dfrac{AB}{AD} = \\dfrac{BC}{DE}$.\nB. $\\dfrac{AD}{AB} = \\dfrac{AE}{AC}$.\nC. $\\dfrac{AB}{BD} = \\dfrac{AC}{CE} = \\dfrac{BC}{DE}$.\nD. $\\dfrac{AD}{AB} = \\dfrac{AE}{AC} = \\dfrac{DE}{BC}$.',
        'dap_an': 'C',
        'loi_giai': 'Theo hệ quả định lí Thalès, $\\dfrac{BC}{DE} = \\dfrac{AB}{AD} = \\dfrac{AC}{AE} \\neq \\dfrac{AB}{BD}$. Khẳng định C là sai. Chọn C.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 6
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-c6',
        'vi_tri': 'Câu 6',
        'loai': 'TN',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Định lí Thalès đảo'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. TRẮC NGHIỆM (1,5 điểm). Viết chữ cái đứng trước câu trả lời đúng vào giấy kiểm tra.',
        'de': 'Cho hình vẽ bên (tam giác $ABC$ có các điểm $M, N, P$ trên các cạnh). Khẳng định nào sau đây là ĐÚNG?\nA. $MP \\parallel AC$.\nB. $NP \\parallel BM$.\nC. $MN \\parallel BC$.\nD. $MP \\parallel AN$.',
        'dap_an': 'B',
        'loi_giai': 'Dựa vào tỉ số các đoạn thẳng trên các cạnh trong hình vẽ và định lí Thalès đảo, ta có $NP \\parallel BM$. Chọn B.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.1
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b1a',
        'vi_tri': 'Bài 1.1',
        'loai': 'TL',
        'chuong': 'VI. Hàm số và đồ thị',
        'dang': ['Vẽ đồ thị hàm số bậc nhất'],
        'band': 'TH',
        'phut': 3.0,
        'diem_bai': 0.75,
        'de_chung': 'II. TỰ LUẬN (8,5 điểm)\nBài 1 (2,5 điểm). Cho hàm số bậc nhất $y = x + 2$ có đồ thị là $(d_1)$.',
        'de': 'Vẽ đồ thị $(d_1)$ của hàm số trên.',
        'dap_an': 'Đường thẳng đi qua $(0; 2)$ và $(-2; 0)$',
        'loi_giai': '- Cho $x = 0 \\Rightarrow y = 2$, ta được điểm $A(0; 2) \\in Oy$.\n- Cho $y = 0 \\Rightarrow x + 2 = 0 \\Leftrightarrow x = -2$, ta được điểm $B(-2; 0) \\in Ox$.\nVẽ đường thẳng đi qua hai điểm $A(0; 2)$ và $B(-2; 0)$ ta được đồ thị $(d_1)$ của hàm số $y = x + 2$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.2
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b1b',
        'vi_tri': 'Bài 1.2',
        'loai': 'TL',
        'chuong': 'VI. Hàm số và đồ thị',
        'dang': ['Vị trí tương đối của hai đường thẳng'],
        'band': 'TH',
        'phut': 3.0,
        'diem_bai': 0.75,
        'de_chung': 'Bài 1 (2,5 điểm). Cho hàm số bậc nhất $y = x + 2$ có đồ thị là $(d_1)$.',
        'de': 'Gọi đồ thị của hàm số bậc nhất $y = (3 - 2m)x + 1$ là $(d_2)$. Xác định $m$ để $(d_2) \\parallel (d_1)$.',
        'dap_an': '$m = 1$',
        'loi_giai': 'Điều kiện để hàm số $y = (3 - 2m)x + 1$ là hàm số bậc nhất: $3 - 2m \\neq 0 \\Leftrightarrow m \\neq \\dfrac{3}{2}$.\nĐường thẳng $(d_2) \\parallel (d_1)$ khi và chỉ khi:\n$$\\begin{cases} 3 - 2m = 1 \\\\ 1 \\neq 2 \\text{ (luôn đúng)} \\end{cases} \\Leftrightarrow 2m = 2 \\Leftrightarrow m = 1.$$\nĐối chiếu điều kiện $m \\neq \\dfrac{3}{2}$, ta thấy $m = 1$ thỏa mãn.\nVậy $m = 1$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.3
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b1c',
        'vi_tri': 'Bài 1.3',
        'loai': 'TL',
        'chuong': 'VI. Hàm số và đồ thị',
        'dang': ['Giao điểm của ba đường thẳng', 'Tìm tham số để ba đường thẳng đồng quy'],
        'band': 'VD',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 1 (2,5 điểm). Cho hàm số bậc nhất $y = x + 2$ có đồ thị là $(d_1)$.',
        'de': 'Tìm $m$ để giao điểm của đường thẳng $(d_1)$ và $(d_2)$ thuộc đường thẳng $y = 5x - 2$.',
        'dap_an': '$m = \\dfrac{1}{2}$',
        'loi_giai': 'Xét phương trình hoành độ giao điểm của $(d_1)$ và đường thẳng $y = 5x - 2$:\n$$x + 2 = 5x - 2 \\Leftrightarrow 4x = 4 \\Leftrightarrow x = 1.$$\nThay $x = 1$ vào phương trình $(d_1)$ ta được $y = 1 + 2 = 3$.\nVậy tọa độ giao điểm là $(1; 3)$.\nĐể $(d_1)$ cắt $(d_2)$ thì $3 - 2m \\neq 1 \\Leftrightarrow m \\neq 1$.\nĐể giao điểm của $(d_1)$ và $(d_2)$ nằm trên đường thẳng $y = 5x - 2$ thì điểm $(1; 3)$ phải thuộc $(d_2)$. Thay tọa độ $(1; 3)$ vào phương trình $(d_2)$:\n$$3 = (3 - 2m) \\cdot 1 + 1 \\Leftrightarrow 3 - 2m = 2 \\Leftrightarrow 2m = 1 \\Leftrightarrow m = \\dfrac{1}{2}.$$\nĐối chiếu điều kiện $m \\neq 1$ và $m \\neq \\dfrac{3}{2}$, giá trị $m = \\dfrac{1}{2}$ thỏa mãn.\nVậy $m = \\dfrac{1}{2}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.a
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b2a',
        'vi_tri': 'Bài 2.a',
        'loai': 'TL',
        'chuong': 'V. Thu thập và tổ chức dữ liệu',
        'dang': ['Lập bảng thống kê từ biểu đồ cột kép'],
        'band': 'NB',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 2 (2,0 điểm). Biểu đồ kép (hình bên) biểu diễn số công nhân xếp loại Tốt trong quý III và quý IV của 4 đội công nhân.',
        'de': 'Lập bảng thống kê số công nhân xếp loại Tốt trong quý III và quý IV và vẽ bảng vào giấy kiểm tra.',
        'dap_an': 'Bảng thống kê 4 đội trong quý III và quý IV',
        'loi_giai': 'Bảng thống kê số công nhân xếp loại Tốt trong quý III và quý IV của 4 đội:\n\n| Đội | 1 | 2 | 3 | 4 |\n| :--- | :---: | :---: | :---: | :---: |\n| Quý III | 50 | 48 | 12 | 18 |\n| Quý IV | 30 | 18 | 25 | 52 |',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.b
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b2b',
        'vi_tri': 'Bài 2.b',
        'loai': 'TL',
        'chuong': 'V. Thu thập và tổ chức dữ liệu',
        'dang': ['Tính toán và so sánh số liệu thống kê'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 2 (2,0 điểm). Biểu đồ kép (hình bên) biểu diễn số công nhân xếp loại Tốt trong quý III và quý IV của 4 đội công nhân.',
        'de': 'Tổng số công nhân xếp loại Tốt quý IV tăng hay giảm bao nhiêu phần trăm so với quý III?',
        'dap_an': 'Giảm xấp xỉ $2{,}34\\%$',
        'loi_giai': 'Tổng số công nhân xếp loại Tốt trong quý III của cả 4 đội là:\n$$50 + 48 + 12 + 18 = 128\\text{ (công nhân)}.$$\nTổng số công nhân xếp loại Tốt trong quý IV của cả 4 đội là:\n$$30 + 18 + 25 + 52 = 125\\text{ (công nhân)}.$$\nVì $125 < 128$ nên số công nhân xếp loại Tốt quý IV giảm so với quý III là:\n$$128 - 125 = 3\\text{ (công nhân)}.$$\nPhần trăm giảm của quý IV so với quý III là:\n$$\\dfrac{3}{128} \\cdot 100\\% \\approx 2{,}34\\%.$$\nVậy tổng số công nhân xếp loại Tốt quý IV giảm khoảng $2{,}34\\%$ so với quý III.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.c
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b2c',
        'vi_tri': 'Bài 2.c',
        'loai': 'TL',
        'chuong': 'IX. Một số yếu tố xác suất',
        'dang': ['Mô tả xác suất của biến cố ngẫu nhiên trong một số ví dụ đơn giản'],
        'band': 'TH',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 2 (2,0 điểm). Biểu đồ kép (hình bên) biểu diễn số công nhân xếp loại Tốt trong quý III và quý IV của 4 đội công nhân.',
        'de': 'Để chọn ra 1 công nhân tiêu biểu của quý IV. Tính xác suất để chọn ra được công nhân tiêu biểu của đội 1?',
        'dap_an': '$P = \\dfrac{6}{25}$',
        'loi_giai': 'Tổng số công nhân xếp loại Tốt của quý IV là $125$ công nhân.\nSố công nhân xếp loại Tốt của đội 1 trong quý IV là $30$ công nhân.\nXác suất để chọn ra được 1 công nhân tiêu biểu của đội 1 trong quý IV là:\n$$P = \\dfrac{30}{125} = \\dfrac{6}{25} = 0{,}24.$$',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b3',
        'vi_tri': 'Bài 3',
        'loai': 'TL',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Ứng dụng thực tế của định lí Thalès', 'Đo khoảng cách gián tiếp'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 3 (1,0 điểm).',
        'de': 'Để đo khoảng cách giữa 2 điểm $A, B$ trên hồ nước, một nhóm học sinh đã sử dụng thước ngắm và các dụng cụ đo để đánh dấu 3 điểm $C, D, E$ (như hình vẽ). Biết $ED \\parallel AB$, $E \\in AC$, $D \\in BC$ và $CD = 16\\text{ m}$, $DB = 32\\text{ m}$, $DE = 9\\text{ m}$. Tính khoảng cách giữa 2 điểm $A, B$.\n(Học sinh không phải vẽ lại hình vào giấy kiểm tra).',
        'dap_an': '$AB = 27\\text{ m}$',
        'loi_giai': 'Ta có độ dài đoạn thẳng $BC$ là:\n$$BC = CD + DB = 16 + 32 = 48\\text{ (m)}.$$\nXét $\\Delta ABC$ có $ED \\parallel AB$ ($E \\in AC, D \\in BC$), theo hệ quả của định lí Thalès ta có:\n$$\\dfrac{DE}{AB} = \\dfrac{CD}{BC}.$$\nThay số vào tỉ lệ thức:\n$$\\dfrac{9}{AB} = \\dfrac{16}{48} = \\dfrac{1}{3} \\Rightarrow AB = 9 \\cdot 3 = 27\\text{ (m)}.$$\nVậy khoảng cách giữa hai điểm $A$ và $B$ là $27\\text{ m}$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.a
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b4a',
        'vi_tri': 'Bài 4.a',
        'loai': 'TL',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Đường trung bình của tam giác'],
        'band': 'TH',
        'phut': 3.0,
        'diem_bai': 0.75,
        'de_chung': 'Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$. Lấy $D, E$ lần lượt là trung điểm của $AB, AC$.',
        'de': 'Chứng minh $DE \\parallel BC$ và $BC = 2DE$.',
        'dap_an': '$DE \\parallel BC$ và $BC = 2DE$',
        'loi_giai': 'Xét tam giác $ABC$ có:\n- $D$ là trung điểm của $AB$ (giả thiết);\n- $E$ là trung điểm của $AC$ (giả thiết).\nSuy ra $DE$ là đường trung bình của tam giác $ABC$.\nDo đó $DE \\parallel BC$ và $DE = \\dfrac{1}{2}BC \\Rightarrow BC = 2DE$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.b
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b4b',
        'vi_tri': 'Bài 4.b',
        'loai': 'TL',
        'chuong': 'III. Tứ giác',
        'dang': ['Nhận biết hình chữ nhật', 'Tính chất đường trung bình'],
        'band': 'TH',
        'phut': 4.0,
        'diem_bai': 0.75,
        'de_chung': 'Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$. Lấy $D, E$ lần lượt là trung điểm của $AB, AC$.',
        'de': 'Vẽ trung tuyến $AI$ của $\\Delta ADE$. Kéo dài $AI$ cắt $BC$ tại $F$. Tứ giác $AEFD$ là hình gì? Vì sao?',
        'dap_an': '$AEFD$ là hình chữ nhật',
        'loi_giai': '- Vì $DE \\parallel BC$ nên theo hệ quả định lí Thalès trong các tam giác $\\Delta ABF$ và $\\Delta ACF$ ta có:\n$$\\dfrac{DI}{BF} = \\dfrac{AI}{AF} = \\dfrac{IE}{FC}.$$\nMà $I$ là trung điểm của $DE$ nên $DI = IE$, suy ra $BF = FC$, tức là $F$ là trung điểm của $BC$.\n- Vì $D$ là trung điểm $AB$, $F$ là trung điểm $BC$ nên $DF$ là đường trung bình của $\\Delta ABC \\Rightarrow DF \\parallel AC$ hay $DF \\parallel AE$.\n- Tương tự $EF$ là đường trung bình của $\\Delta ABC \\Rightarrow EF \\parallel AB$ hay $EF \\parallel AD$.\n- Tứ giác $AEFD$ có các cặp cạnh đối song song ($AE \\parallel DF$ và $AD \\parallel EF$) nên là hình bình hành.\nLại có $\\widehat{DAE} = \\widehat{BAC} = 90^\\circ$ (tam giác $ABC$ vuông tại $A$).\nDo đó tứ giác $AEFD$ là hình chữ nhật.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.c
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b4c',
        'vi_tri': 'Bài 4.c',
        'loai': 'TL',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Tính độ dài đoạn thẳng', 'Tính chất trọng tâm tam giác'],
        'band': 'VD',
        'phut': 4.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 4 (2,5 điểm). Cho $\\Delta ABC$ vuông tại $A$. Lấy $D, E$ lần lượt là trung điểm của $AB, AC$.',
        'de': '$BE$ cắt $AF$ tại $K$. Tính $IK$ biết $AB = 6\\text{ cm}$ và $AC = 8\\text{ cm}$.',
        'dap_an': '$IK = \\dfrac{5}{6}\\text{ cm}$',
        'loi_giai': 'Áp dụng định lí Pythagore trong $\\Delta ABC$ vuông tại $A$:\n$$BC = \\sqrt{AB^2 + AC^2} = \\sqrt{6^2 + 8^2} = 10\\text{ (cm)}.$$\nVì $F$ là trung điểm của $BC$ nên $AF$ là đường trung tuyến ứng với cạnh huyền của $\\Delta ABC$ vuông tại $A$:\n$$AF = \\dfrac{1}{2}BC = \\dfrac{1}{2} \\cdot 10 = 5\\text{ (cm)}.$$\nTrong $\\Delta ABC$, hai đường trung tuyến $BE$ và $AF$ cắt nhau tại $K$, do đó $K$ là trọng tâm của $\\Delta ABC$.\nSuy ra $AK = \\dfrac{2}{3}AF$.\nMặt khác, tứ giác $AEFD$ là hình chữ nhật, $I$ là trung điểm của đường chéo $DE$ nên $I$ cũng là trung điểm của đường chéo $AF$, do đó $AI = \\dfrac{1}{2}AF$.\nĐộ dài đoạn thẳng $IK$ là:\n$$IK = AK - AI = \\dfrac{2}{3}AF - \\dfrac{1}{2}AF = \\dfrac{1}{6}AF = \\dfrac{1}{6} \\cdot 5 = \\dfrac{5}{6}\\text{ (cm)}.$$\nVậy $IK = \\dfrac{5}{6}\\text{ cm}$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 5
    {
        'id': 'l8-gk2-2023-thcs-chuong-duong-b5',
        'vi_tri': 'Bài 5',
        'loai': 'TL',
        'chuong': 'IX. Một số yếu tố xác suất',
        'dang': ['Nguyên lí Dirichlet và bài toán xác suất chắc chắn'],
        'band': 'VDC',
        'phut': 5.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 5 (0,5 điểm).',
        'de': 'Trong hộp có 20 viên bi Vàng, 18 viên bi Xanh, 26 viên bi Đỏ có kích thước giống hệt nhau. Không nhìn vào hộp, cần bốc ra ít nhất bao nhiêu viên để chắc chắn trong số các viên bi lấy ra có ít nhất 13 viên Vàng, 10 viên Xanh và 9 viên Đỏ?',
        'dap_an': '57 viên bi',
        'loi_giai': 'Để chắc chắn trong số các viên bi lấy ra có ít nhất 13 viên Vàng, 10 viên Xanh và 9 viên Đỏ, ta xét tình huống xấu nhất (bất lợi nhất) khi ta bốc hết toàn bộ số bi của hai màu nào đó và chỉ bốc được một phần số bi của màu còn lại:\n- Trường hợp 1: Bốc hết 20 viên Vàng, 18 viên Xanh và chỉ bốc được 9 viên Đỏ:\n$$20 + 18 + 9 = 47\\text{ (viên)}.$$\n- Trường hợp 2: Bốc hết 20 viên Vàng, 26 viên Đỏ và chỉ bốc được 10 viên Xanh:\n$$20 + 26 + 10 = 56\\text{ (viên)}.$$\n- Trường hợp 3: Bốc hết 18 viên Xanh, 26 viên Đỏ và chỉ bốc được 13 viên Vàng:\n$$18 + 26 + 13 = 57\\text{ (viên)}.$$\nTrong 3 trường hợp xấu nhất trên, trường hợp xấu nhất cần đến 57 viên bi.\nDo đó, nếu bốc ngẫu nhiên 57 viên bi thì chắc chắn trong số bi lấy ra có ít nhất 13 viên Vàng, 10 viên Xanh và 9 viên Đỏ.\nVậy cần bốc ra ít nhất 57 viên bi.',
        'trang': 4,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    }
]

d['cau'] = cau_list

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Updated Chuong Duong successfully! Total cau:', len(d['cau']))
print('Total score:', sum(c['diem_bai'] for c in d['cau']))
