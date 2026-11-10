# -*- coding: utf-8 -*-
import json

path = 'inputs/refs/de-thi/lop-8/exams/gk2-2023-thcs-nam-trung-yen.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

d['tang'] = 2
d['da_duyet'] = True
d['tieu_de'] = 'Đề kiểm tra giữa học kỳ II môn Toán 8 - THCS Nam Trung Yên (Cầu Giấy) năm học 2023 - 2024'
d['nam_hoc'] = '2023-2024'
d['hoc_ky'] = 'GK2'
d['lop'] = '8'
d['thoi_gian_phut'] = 90
d['ghi_chu'] = 'Đề chuẩn GK2 Toán 8 THCS Nam Trung Yên 2023-2024. Đã soát 100% từ ảnh scan: 4 câu TN (1.0đ) + 5 bài TL (9.0đ), tổng điểm 10.00đ.'

cau_list = [
    # Câu 1
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-c1',
        'vi_tri': 'Câu 1',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Điều kiện xác định của phân thức đại số'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. Trắc nghiệm (1,0 điểm) Chọn chữ cái đứng trước câu trả lời đúng.',
        'de': 'Điều kiện xác định của phân thức $\\dfrac{x-1}{x-2}$ là:\nA. $x = 1$.\nB. $x \\neq 1$.\nC. $x = 2$.\nD. $x \\neq 2$.',
        'dap_an': 'D',
        'loi_giai': 'Phân thức $\\dfrac{x-1}{x-2}$ xác định khi và chỉ khi mẫu thức khác $0$, tức là $x - 2 \\neq 0 \\Leftrightarrow x \\neq 2$. Chọn D.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 2
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-c2',
        'vi_tri': 'Câu 2',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Hai phân thức bằng nhau'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. Trắc nghiệm (1,0 điểm) Chọn chữ cái đứng trước câu trả lời đúng.',
        'de': 'Đa thức $M$ thỏa mãn $\\dfrac{M}{x^2-16} = \\dfrac{x}{x-4}$ là:\nA. $x^2+4$.\nB. $x^2+4x$.\nC. $x^2-4$.\nD. $x^2-4x$.',
        'dap_an': 'B',
        'loi_giai': 'Ta có:\n$$M = \\dfrac{x(x^2-16)}{x-4} = \\dfrac{x(x-4)(x+4)}{x-4} = x(x+4) = x^2+4x.$$\nChọn B.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 3
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-c3',
        'vi_tri': 'Câu 3',
        'loai': 'TN',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Định nghĩa hai tam giác đồng dạng'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. Trắc nghiệm (1,0 điểm) Chọn chữ cái đứng trước câu trả lời đúng.',
        'de': 'Cho $\\Delta RSK$ và $\\Delta PQM$ có $\\dfrac{RS}{PQ} = \\dfrac{SK}{QM} = \\dfrac{RK}{PM}$. Khẳng định nào dưới đây đúng?\nA. $\\Delta RSK \\backsim \\Delta PQM$.\nB. $\\Delta RSK \\backsim \\Delta QPM$.\nC. $\\Delta RSK \\backsim \\Delta MPQ$.\nD. $\\Delta RSK \\backsim \\Delta QMP$.',
        'dap_an': 'A',
        'loi_giai': 'Từ tỉ lệ các cạnh tương ứng $\\dfrac{RS}{PQ} = \\dfrac{SK}{QM} = \\dfrac{RK}{PM}$ suy ra các đỉnh tương ứng là $R \\leftrightarrow P, S \\leftrightarrow Q, K \\leftrightarrow M$. Do đó $\\Delta RSK \\backsim \\Delta PQM$. Chọn A.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 4
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-c4',
        'vi_tri': 'Câu 4',
        'loai': 'TN',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Định lí Pythagore trong tam giác vuông'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'I. Trắc nghiệm (1,0 điểm) Chọn chữ cái đứng trước câu trả lời đúng.',
        'de': 'Cho tam giác $MNP$ vuông tại $P$ có $MN = 17\\text{ cm}, NP = 8\\text{ cm}$, độ dài cạnh $MP$ là:\nA. $15\\text{ cm}$.\nB. $9\\text{ cm}$.\nC. $\\sqrt{353}\\text{ cm}$.\nD. $25\\text{ cm}$.',
        'dap_an': 'A',
        'loi_giai': 'Áp dụng định lí Pythagore trong $\\Delta MNP$ vuông tại $P$:\n$$MP = \\sqrt{MN^2 - NP^2} = \\sqrt{17^2 - 8^2} = \\sqrt{289 - 64} = \\sqrt{225} = 15\\text{ (cm)}.$$\nChọn A.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.a
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b1a',
        'vi_tri': 'Bài 1.a',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Cộng hai phân thức cùng mẫu'],
        'band': 'NB',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'II. Tự luận (9,0 điểm)\nBài 1 (1,5 điểm). Thực hiện các phép tính sau:',
        'de': '$\\dfrac{4x}{x+5} + \\dfrac{20}{x+5}$.',
        'dap_an': '$4$',
        'loi_giai': 'Ta có:\n$$\\dfrac{4x}{x+5} + \\dfrac{20}{x+5} = \\dfrac{4x+20}{x+5} = \\dfrac{4(x+5)}{x+5} = 4.$$',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.b
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b1b',
        'vi_tri': 'Bài 1.b',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Cộng, trừ phân thức đại số', 'Quy tắc đổi dấu'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (1,5 điểm). Thực hiện các phép tính sau:',
        'de': '$\\dfrac{3+2x}{x^2-y^2} - \\dfrac{2y-3}{y^2-x^2}$.',
        'dap_an': '$\\dfrac{2}{x-y}$',
        'loi_giai': 'Áp dụng quy tắc đổi dấu ở phân thức thứ hai:\n$$\\begin{aligned}\n\\dfrac{3+2x}{x^2-y^2} - \\dfrac{2y-3}{y^2-x^2} &= \\dfrac{3+2x}{x^2-y^2} + \\dfrac{2y-3}{x^2-y^2} \\\\\n&= \\dfrac{3+2x+2y-3}{x^2-y^2} \\\\\n&= \\dfrac{2(x+y)}{(x-y)(x+y)} = \\dfrac{2}{x-y}.\n\\end{aligned}$$',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.c
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b1c',
        'vi_tri': 'Bài 1.c',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Nhân hai phân thức đại số'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (1,5 điểm). Thực hiện các phép tính sau:',
        'de': '$\\dfrac{x-2}{x} \\cdot \\dfrac{4xy}{x^2-4}$.',
        'dap_an': '$\\dfrac{4y}{x+2}$',
        'loi_giai': 'Ta có:\n$$\\dfrac{x-2}{x} \\cdot \\dfrac{4xy}{x^2-4} = \\dfrac{(x-2) \\cdot 4xy}{x(x-2)(x+2)} = \\dfrac{4y}{x+2}.$$',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.a
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b2a',
        'vi_tri': 'Bài 2.a',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tính giá trị của phân thức đại số'],
        'band': 'NB',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 2 (2,5 điểm). Cho hai biểu thức $A = \\dfrac{x}{x-3}$ và $B = \\dfrac{3x+15}{x^2-9} + \\dfrac{1}{x+3} - \\dfrac{2}{x-3}$ với $x \\neq \\pm 3$.',
        'de': 'Tính giá trị biểu thức $A$ tại $x = 5$.',
        'dap_an': '$A = \\dfrac{5}{2}$',
        'loi_giai': 'Thay $x = 5$ (thỏa mãn điều kiện $x \\neq \\pm 3$) vào biểu thức $A$, ta được:\n$$A = \\dfrac{5}{5-3} = \\dfrac{5}{2}.$$\nVậy khi $x = 5$ thì $A = \\dfrac{5}{2}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.b
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b2b',
        'vi_tri': 'Bài 2.b',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Rút gọn biểu thức chứa phân thức đại số'],
        'band': 'TH',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 2 (2,5 điểm). Cho hai biểu thức $A = \\dfrac{x}{x-3}$ và $B = \\dfrac{3x+15}{x^2-9} + \\dfrac{1}{x+3} - \\dfrac{2}{x-3}$ với $x \\neq \\pm 3$.',
        'de': 'Chứng minh rằng $B = \\dfrac{2}{x-3}$.',
        'dap_an': '$B = \\dfrac{2}{x-3}$',
        'loi_giai': 'Với $x \\neq \\pm 3$, ta có:\n$$\\begin{aligned}\nB &= \\dfrac{3x+15}{(x-3)(x+3)} + \\dfrac{x-3}{(x-3)(x+3)} - \\dfrac{2(x+3)}{(x-3)(x+3)} \\\\\n&= \\dfrac{3x+15 + x-3 - 2x-6}{(x-3)(x+3)} \\\\\n&= \\dfrac{2x+6}{(x-3)(x+3)} \\\\\n&= \\dfrac{2(x+3)}{(x-3)(x+3)} = \\dfrac{2}{x-3}.\n\\end{aligned}$$\nVậy $B = \\dfrac{2}{x-3}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.c
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b2c',
        'vi_tri': 'Bài 2.c',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tìm giá trị nguyên của biến để biểu thức nhận giá trị nguyên'],
        'band': 'VD',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 2 (2,5 điểm). Cho hai biểu thức $A = \\dfrac{x}{x-3}$ và $B = \\dfrac{3x+15}{x^2-9} + \\dfrac{1}{x+3} - \\dfrac{2}{x-3}$ với $x \\neq \\pm 3$.',
        'de': 'Tìm giá trị nguyên của $x$ để biểu thức $C = A : B$ nhận giá trị nguyên.',
        'dap_an': '$x$ là số nguyên chẵn',
        'loi_giai': 'Ta có:\n$$C = A : B = \\dfrac{x}{x-3} : \\dfrac{2}{x-3} = \\dfrac{x}{x-3} \\cdot \\dfrac{x-3}{2} = \\dfrac{x}{2}.$$\nĐể biểu thức $C$ nhận giá trị nguyên với $x \\in \\mathbb{Z}$ thì $x$ phải chia hết cho 2, tức là $x$ là số nguyên chẵn ($x = 2k, k \\in \\mathbb{Z}$).\nĐối chiếu điều kiện xác định $x \\neq \\pm 3$, vì $x$ chẵn nên luôn khác $\\pm 3$.\nVậy $x$ là số nguyên chẵn bất kì thì $C$ nhận giá trị nguyên.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3.a
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b3a',
        'vi_tri': 'Bài 3.a',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Bài toán thực tế liên quan đến phân thức đại số'],
        'band': 'NB',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 3 (1,0 điểm). Một người đi từ $A$ đến $B$ cách nhau $20\\text{ km}$ với vận tốc $x\\text{ (km/h)}$. Khi từ $B$ về $A$ đường vắng hơn nên người đó đi với vận tốc lớn hơn vận tốc lúc đi là $5\\text{ km/h}$.',
        'de': 'Viết các phân thức theo $x$ biểu thị thời gian lúc đi, thời gian lúc về.',
        'dap_an': 'Thời gian đi: $\\dfrac{20}{x}$ (h); Thời gian về: $\\dfrac{20}{x+5}$ (h)',
        'loi_giai': '- Thời gian lúc đi từ $A$ đến $B$ là: $\\dfrac{20}{x}\\text{ (giờ)}$.\n- Vận tốc lúc về là $x + 5\\text{ (km/h)}$, thời gian lúc về từ $B$ về $A$ là: $\\dfrac{20}{x+5}\\text{ (giờ)}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3.b
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b3b',
        'vi_tri': 'Bài 3.b',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Bài toán thực tế liên quan đến phân thức đại số'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 3 (1,0 điểm). Một người đi từ $A$ đến $B$ cách nhau $20\\text{ km}$ với vận tốc $x\\text{ (km/h)}$. Khi từ $B$ về $A$ đường vắng hơn nên người đó đi với vận tốc lớn hơn vận tốc lúc đi là $5\\text{ km/h}$.',
        'de': 'Tính tổng thời gian người đó di chuyển cả đi và về, biết vận tốc khi đi là $25\\text{ km/h}$.',
        'dap_an': '$\\dfrac{22}{15}$ giờ ($1$ giờ $28$ phút)',
        'loi_giai': 'Vận tốc khi đi là $25\\text{ km/h}$, do đó $x = 25$.\nTổng thời gian di chuyển cả đi và về là:\n$$T = \\dfrac{20}{25} + \\dfrac{20}{25+5} = \\dfrac{4}{5} + \\dfrac{20}{30} = \\dfrac{4}{5} + \\dfrac{2}{3} = \\dfrac{12+10}{15} = \\dfrac{22}{15}\\text{ (giờ)}.$$\nĐổi: $\\dfrac{22}{15}\\text{ giờ} = 1\\text{ giờ } 28\\text{ phút}$.\nVậy tổng thời gian di chuyển là $1$ giờ $28$ phút.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.1
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b4a',
        'vi_tri': 'Bài 4.1',
        'loai': 'TL',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Ứng dụng thực tế của định lí Thalès', 'Đo chiều cao vật thể'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 4 (3,5 điểm).',
        'de': '4.1. Một người cắm một cái cọc $CD$ vuông góc với mặt đất sao cho bóng của đỉnh cọc trùng với bóng của ngọn cây (như hình vẽ). Biết cọc $CD = 1{,}5\\text{ m}$, chân cọc cách gốc cây $AC = 8\\text{ m}$ và cách bóng của đỉnh cọc $CE = 2\\text{ m}$. Tính chiều cao $AB$ của cây.',
        'dap_an': '$AB = 7{,}5\\text{ m}$',
        'loi_giai': 'Vì cọc $CD$ và cây $AB$ đều vuông góc với mặt đất nên $CD \\parallel AB$.\nKhoảng cách từ gốc cây đến bóng ngọn cây là $AE = AC + CE = 8 + 2 = 10\\text{ m}$.\nÁp dụng hệ quả định lí Thalès trong tam giác $EAB$ với $CD \\parallel AB$:\n$$\\dfrac{AB}{CD} = \\dfrac{AE}{CE} \\Rightarrow AB = \\dfrac{CD \\cdot AE}{CE} = \\dfrac{1{,}5 \\cdot 10}{2} = 7{,}5\\text{ (m)}.$$\nVậy chiều cao của cây là $7{,}5\\text{ m}$.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.2.a
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b4b1',
        'vi_tri': 'Bài 4.2.a',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Chứng minh hai tam giác đồng dạng'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de_chung': 'Bài 4 (3,5 điểm). 4.2. Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Kẻ tia phân giác của góc $B$ cắt $AC$ tại $E$. Từ $C$ kẻ $CD$ vuông góc với tia $BE$ ($D$ thuộc tia $BE$).',
        'de': 'Chứng minh $\\Delta ABE \\backsim \\Delta DCE$.',
        'dap_an': '$\\Delta ABE \\backsim \\Delta DCE\\text{ (g-g)}$',
        'loi_giai': 'Xét $\\Delta ABE$ và $\\Delta DCE$ có:\n- $\\widehat{BAE} = \\widehat{CDE} = 90^\\circ$ (do tam giác $ABC$ vuông tại $A$ và $CD \\perp BE$);\n- $\\widehat{AEB} = \\widehat{DEC}$ (hai góc đối đỉnh).\nSuy ra $\\Delta ABE \\backsim \\Delta DCE\\text{ (g-g)}$.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.2.b
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b4b2',
        'vi_tri': 'Bài 4.2.b',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Chứng minh hai góc bằng nhau', 'Chứng minh đẳng thức tích'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 0.75,
        'de_chung': 'Bài 4 (3,5 điểm). 4.2. Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Kẻ tia phân giác của góc $B$ cắt $AC$ tại $E$. Từ $C$ kẻ $CD$ vuông góc với tia $BE$ ($D$ thuộc tia $BE$).',
        'de': 'Chứng minh $\\widehat{DCE} = \\widehat{DBC}$ từ đó chứng minh $DC^2 = DB \\cdot DE$.',
        'dap_an': '$\\widehat{DCE} = \\widehat{DBC}$ và $DC^2 = DB \\cdot DE$',
        'loi_giai': '- Vì $\\Delta ABE \\backsim \\Delta DCE$ (theo câu a) nên $\\widehat{ABE} = \\widehat{DCE}$.\n  Mặt khác, $BE$ là tia phân giác của $\\widehat{B}$ nên $\\widehat{ABE} = \\widehat{DBC}$.\n  Suy ra $\\widehat{DCE} = \\widehat{DBC}$.\n- Xét $\\Delta DCE$ và $\\Delta DBC$ có:\n  + $\\widehat{D}$ là góc chung;\n  + $\\widehat{DCE} = \\widehat{DBC}$ (chứng minh trên).\n  Suy ra $\\Delta DCE \\backsim \\Delta DBC\\text{ (g-g)}$.\n  Do đó ta có tỉ số cạnh tương ứng:\n  $$\\dfrac{DC}{DB} = \\dfrac{DE}{DC} \\Rightarrow DC^2 = DB \\cdot DE.$$',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4.2.c
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b4b3',
        'vi_tri': 'Bài 4.2.c',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Chứng minh tam giác cân'],
        'band': 'VD',
        'phut': 4.0,
        'diem_bai': 0.75,
        'de_chung': 'Bài 4 (3,5 điểm). 4.2. Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$). Kẻ tia phân giác của góc $B$ cắt $AC$ tại $E$. Từ $C$ kẻ $CD$ vuông góc với tia $BE$ ($D$ thuộc tia $BE$).',
        'de': 'Chứng minh $\\Delta DAC$ cân.',
        'dap_an': '$\\Delta DAC$ cân tại $D$',
        'loi_giai': 'Kéo dài $BA$ và $CD$ cắt nhau tại $K$.\nXét tam giác $KBC$ có $BD$ vừa là đường phân giác vừa là đường cao nên $\\Delta KBC$ cân tại $B$.\nSuy ra $BD$ cũng là đường trung tuyến của tam giác $KBC$, do đó $D$ là trung điểm của $KC$.\nTam giác $KAC$ vuông tại $A$ có $AD$ là đường trung tuyến ứng với cạnh huyền $KC$ nên:\n$$AD = \\dfrac{1}{2}KC = DC.$$\nDo đó tam giác $DAC$ có $DA = DC$ nên là tam giác cân tại $D$.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 5
    {
        'id': 'l8-gk2-2023-thcs-nam-trung-yen-b5',
        'vi_tri': 'Bài 5',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tính giá trị biểu thức đối xứng có điều kiện'],
        'band': 'VDC',
        'phut': 5.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 5 (0,5 điểm).',
        'de': 'Cho $x, y, z \\neq 0$ và $x + y + z = 0$. Tính giá trị của biểu thức:\n$$A = \\dfrac{xy}{x^2+y^2-z^2} + \\dfrac{yz}{y^2+z^2-x^2} + \\dfrac{zx}{z^2+x^2-y^2}.$$',
        'dap_an': '$A = -\\dfrac{3}{2}$',
        'loi_giai': 'Từ giả thiết $x + y + z = 0 \\Rightarrow x + y = -z$.\nBình phương hai vế:\n$$(x+y)^2 = (-z)^2 \\Leftrightarrow x^2 + 2xy + y^2 = z^2 \\Leftrightarrow x^2 + y^2 - z^2 = -2xy.$$\nDo $x, y \\neq 0$ nên:\n$$\\dfrac{xy}{x^2+y^2-z^2} = \\dfrac{xy}{-2xy} = -\\dfrac{1}{2}.$$\nChứng minh hoàn toàn tương tự, ta có:\n$$\\dfrac{yz}{y^2+z^2-x^2} = -\\dfrac{1}{2} \\quad \\text{và} \\quad \\dfrac{zx}{z^2+x^2-y^2} = -\\dfrac{1}{2}.$$\nThay vào biểu thức $A$, ta được:\n$$A = \\left(-\\dfrac{1}{2}\\right) + \\left(-\\dfrac{1}{2}\\right) + \\left(-\\dfrac{1}{2}\\right) = -\\dfrac{3}{2}.$$\nVậy $A = -\\dfrac{3}{2}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    }
]

d['cau'] = cau_list

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Updated Nam Trung Yen successfully! Total cau:', len(d['cau']))
print('Total score:', sum(c['diem_bai'] for c in d['cau']))
