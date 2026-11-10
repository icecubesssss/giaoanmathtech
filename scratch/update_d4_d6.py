import json

# ==============================================================================
# ĐỀ 4: ck2-2023-thanh-tri
# ==============================================================================
def update_d4():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thanh-tri.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Thanh Trì 2023-2024. Đã duyệt chuẩn 100%: 8 câu TN (2,0đ) + 5 bài TL (8,0đ: gồm 11 câu/ý), tổng điểm 10.00đ.'

    new_cau = [
        # C1
        {
            'id': 'l8-ck2-2023-thanh-tri-c1',
            'vi_tri': 'Câu 1',
            'loai': 'TN',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Nhân chia phân thức'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Kết quả phép nhân $\\dfrac{x - 3}{x^2} \\cdot \\dfrac{x^3 + 3x^2}{(x - 3)^2}$ là:\n\nA. $\\dfrac{x - 3}{x + 3}$.\nB. $\\dfrac{x + 3}{x - 3}$.\nC. $\\dfrac{x + 3}{x}$.\nD. $\\dfrac{1}{x - 3}$.',
            'dap_an': 'B',
            'loi_giai': 'Ta có: $\\dfrac{x - 3}{x^2} \\cdot \\dfrac{x^2(x + 3)}{(x - 3)^2} = \\dfrac{x + 3}{x - 3}$. Chọn B.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C2
        {
            'id': 'l8-ck2-2023-thanh-tri-c2',
            'vi_tri': 'Câu 2',
            'loai': 'TN',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Nhận biết phương trình bậc nhất một ẩn'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Trong các phương trình sau, phương trình nào là phương trình bậc nhất một ẩn?\n\nA. $x^2 + 3x + 1 = 0$.\nB. $2x + 5 = 0$.\nC. $0x + 7 = 0$.\nD. $\\dfrac{1}{x - 1} = 0$.',
            'dap_an': 'B',
            'loi_giai': 'Phương trình $2x + 5 = 0$ có dạng $ax + b = 0$ với $a = 2 \\ne 0$. Chọn B.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C3
        {
            'id': 'l8-ck2-2023-thanh-tri-c3',
            'vi_tri': 'Câu 3',
            'loai': 'TN',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình bậc nhất một ẩn'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Phương trình $3x + 1 = -2x + 11$ có nghiệm là:\n\nA. $x = 2$.\nB. $x = 5$.\nC. $x = -2$.\nD. $x = 3$.',
            'dap_an': 'A',
            'loi_giai': '$3x + 1 = -2x + 11 \\Leftrightarrow 3x + 2x = 11 - 1 \\Leftrightarrow 5x = 10 \\Leftrightarrow x = 2$. Chọn A.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C4
        {
            'id': 'l8-ck2-2023-thanh-tri-c4',
            'vi_tri': 'Câu 4',
            'loai': 'TN',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Điều kiện để hàm số là bậc nhất'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Với giá trị nào của $m$ thì hàm số $y = (m - 2)x + 7$ là hàm số bậc nhất?\n\nA. $m \\ne 2$.\nB. $m \\ne -2$.\nC. $m \\ne \\pm 2$.\nD. $m \\ne 0$.',
            'dap_an': 'A',
            'loi_giai': 'Hàm số $y = (m - 2)x + 7$ là hàm số bậc nhất khi hệ số $a = m - 2 \\ne 0 \\Leftrightarrow m \\ne 2$. Chọn A.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C5
        {
            'id': 'l8-ck2-2023-thanh-tri-c5',
            'vi_tri': 'Câu 5',
            'loai': 'TN',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Tọa độ của điểm trên mặt phẳng tọa độ'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Trên mặt phẳng tọa độ $Oxy$, điểm $C$ có hoành độ bằng 2 và tung độ bằng $-2$. Tọa độ của điểm $C$ là:\n\nA. $A(-4; 1)$.\nB. $B(2; -3)$.\nC. $C(2; -2)$.\nD. $D(1; -3)$.',
            'dap_an': 'C',
            'loi_giai': 'Điểm $C$ có tọa độ là $(2; -2)$. Chọn C.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C6
        {
            'id': 'l8-ck2-2023-thanh-tri-c6',
            'vi_tri': 'Câu 6',
            'loai': 'TN',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Điều kiện đồng dạng của hai tam giác'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Nếu $\\Delta MNP$ và $\\Delta DEF$ có $\\widehat{M} = \\widehat{D} = 90^\\circ, \\widehat{P} = 50^\\circ$. Để $\\Delta MNP \\backsim \\Delta DEF$ thì cần thêm điều kiện:\n\nA. $\\widehat{E} = 50^\\circ$.\nB. $\\widehat{F} = 50^\\circ$.\nC. $\\widehat{E} = 60^\\circ$.\nD. $\\widehat{F} = 40^\\circ$.',
            'dap_an': 'B',
            'loi_giai': 'Hai tam giác vuông đồng dạng khi có một cặp góc nhọn tương ứng bằng nhau, tức $\\widehat{P} = \\widehat{F} = 50^\\circ$. Chọn B.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C7
        {
            'id': 'l8-ck2-2023-thanh-tri-c7',
            'vi_tri': 'Câu 7',
            'loai': 'TN',
            'chuong': 'VIII. Hình đồng dạng',
            'dang': ['Nhận biết hình đồng dạng phối cảnh'],
            'band': 'NB',
            'phut': 1.5,
            'diem_bai': 0.25,
            'de': 'Trong các cặp hình đồng dạng, cặp hình không là đồng dạng phối cảnh là:\n\nA. Hình 1.\nB. Hình 2.\nC. Hình 3.\nD. Cả 3 hình trên.',
            'dap_an': 'B',
            'loi_giai': 'Hình 2 không có tâm phối cảnh mà các đường nối điểm tương ứng đồng quy. Chọn B.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # C8
        {
            'id': 'l8-ck2-2023-thanh-tri-c8',
            'vi_tri': 'Câu 8',
            'loai': 'TN',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Hình chóp tam giác đều'],
            'band': 'NB',
            'phut': 1.0,
            'diem_bai': 0.25,
            'de': 'Các mặt bên của hình chóp tam giác đều là hình gì?\n\nA. Tam giác cân.\nB. Tam giác đều.\nC. Tam giác nhọn.\nD. Tam giác vuông.',
            'dap_an': 'A',
            'loi_giai': 'Hình chóp tam giác đều có các mặt bên là các tam giác cân bằng nhau. Chọn A.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1.a (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b1a',
            'vi_tri': 'Bài 1.a',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tính giá trị của phân thức'],
            'band': 'NB',
            'phut': 2.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 1 (1,5 điểm). Cho hai biểu thức $A = \\dfrac{x - 5}{x - 1}$ và $B = \\dfrac{x^2 - 3}{x^2 - 1} + \\dfrac{x - 1}{x + 1} - \\dfrac{x + 1}{x - 1}$ với $x \\ne \\pm 1$.',
            'de': 'Tính giá trị của biểu thức $A$ khi $x = 3$.',
            'dap_an': '$A = -1$',
            'loi_giai': 'Thay $x = 3$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{3 - 5}{3 - 1} = \\dfrac{-2}{2} = -1.$$\nVậy $A = -1$ khi $x = 3$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1.b (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b1b',
            'vi_tri': 'Bài 1.b',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Rút gọn biểu thức phân thức'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 1 (1,5 điểm). Cho hai biểu thức $A = \\dfrac{x - 5}{x - 1}$ và $B = \\dfrac{x^2 - 3}{x^2 - 1} + \\dfrac{x - 1}{x + 1} - \\dfrac{x + 1}{x - 1}$ với $x \\ne \\pm 1$.',
            'de': 'Chứng tỏ rằng: $B = \\dfrac{x - 1}{x + 1}$.',
            'dap_an': '$B = \\dfrac{x - 1}{x + 1}$',
            'loi_giai': 'Quy đồng mẫu thức chung là $(x - 1)(x + 1) = x^2 - 1$, rút gọn tử thức ta được:\n$$B = \\dfrac{x - 1}{x + 1}.$$\nVậy $B = \\dfrac{x - 1}{x + 1}$ với $x \\ne \\pm 1$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1.c (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b1c',
            'vi_tri': 'Bài 1.c',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tìm giá trị biến để biểu thức nhận giá trị nguyên/tự nhiên'],
            'band': 'VD',
            'phut': 4.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 1 (1,5 điểm). Cho hai biểu thức: $A = \\dfrac{x - 5}{x - 1}$ và $B = \\dfrac{x - 1}{x + 1}$ với $x \\ne \\pm 1$.',
            'de': 'Cho $P = A \\cdot B$. Tìm tất cả các giá trị nguyên của $x$ để $P$ nhận giá trị là số tự nhiên.',
            'dap_an': '$x \\in \\{-2; -3; -4; 5; -7\\}$',
            'loi_giai': 'Ta có: $P = A \\cdot B = \\dfrac{x - 5}{x - 1} \\cdot \\dfrac{x - 1}{x + 1} = \\dfrac{x - 5}{x + 1} = 1 - \\dfrac{6}{x + 1}$.\nĐể $P$ nhận giá trị nguyên thì $x + 1 \\in Ư(6) = \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$.\nLập bảng xét giá trị:\n- $x + 1 = 1 \\Rightarrow x = 0 \\Rightarrow P = -5 < 0$ (loại).\n- $x + 1 = -1 \\Rightarrow x = -2 \\Rightarrow P = 7 \\in \\mathbb{N}$ (thỏa mãn).\n- $x + 1 = 2 \\Rightarrow x = 1$ (loại do ĐKXĐ $x \\ne 1$).\n- $x + 1 = -2 \\Rightarrow x = -3 \\Rightarrow P = 4 \\in \\mathbb{N}$ (thỏa mãn).\n- $x + 1 = 3 \\Rightarrow x = 2 \\Rightarrow P = -1 < 0$ (loại).\n- $x + 1 = -3 \\Rightarrow x = -4 \\Rightarrow P = 3 \\in \\mathbb{N}$ (thỏa mãn).\n- $x + 1 = 6 \\Rightarrow x = 5 \\Rightarrow P = 0 \\in \\mathbb{N}$ (thỏa mãn).\n- $x + 1 = -6 \\Rightarrow x = -7 \\Rightarrow P = 2 \\in \\mathbb{N}$ (thỏa mãn).\nVậy $x \\in \\{-2; -3; -4; 5; -7\\}$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.1 (1.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b2-1',
            'vi_tri': 'Bài 2.1',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải bài toán bằng cách lập phương trình', 'Toán năng suất'],
            'band': 'VD',
            'phut': 5.0,
            'diem_bai': 1.5,
            'de_chung': 'Bài 2 (2,0 điểm).',
            'de': 'Một đội sản xuất dự định mỗi ngày làm được 30 chi tiết máy. Khi thực hiện, mỗi ngày đội làm vượt mức so với dự định 10 chi tiết máy, vì vậy đội không những đã hoàn thành xong trước kế hoạch 2 ngày mà còn làm thêm được 45 chi tiết máy. Tính số chi tiết máy mà đội phải sản xuất theo kế hoạch.',
            'dap_an': '$375$ chi tiết máy',
            'loi_giai': 'Gọi số chi tiết máy đội phải sản xuất theo kế hoạch là $x$ (chi tiết máy, $x \\in \\mathbb{N}^*$).\nThời gian hoàn thành theo kế hoạch là: $\\dfrac{x}{30}$ (ngày).\nThực tế mỗi ngày đội sản xuất được: $30 + 10 = 40$ (chi tiết máy).\nTổng số chi tiết máy thực tế sản xuất là: $x + 45$ (chi tiết máy).\nThời gian hoàn thành thực tế là: $\\dfrac{x + 45}{40}$ (ngày).\nVì thực tế đội hoàn thành trước kế hoạch 2 ngày nên ta có phương trình:\n$$\\dfrac{x}{30} - \\dfrac{x + 45}{40} = 2$$\n$$\\Leftrightarrow \\dfrac{4x - 3(x + 45)}{120} = 2$$\n$$\\Leftrightarrow x - 135 = 240 \\Leftrightarrow x = 375 \\text{ (thỏa mãn ĐK)}.$$\nVậy số chi tiết máy đội phải sản xuất theo kế hoạch là 375 chi tiết máy.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.2 (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b2-2',
            'vi_tri': 'Bài 2.2',
            'loai': 'TL',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Diện tích xung quanh hình chóp tam giác đều'],
            'band': 'TH',
            'phut': 2.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 2 (2,0 điểm).',
            'de': 'Một giỏ hoa gỗ mini có dạng hình chóp tam giác đều, biết độ dài cạnh đáy là $10\\text{ cm}$ và độ dài trung đoạn bằng $20\\text{ cm}$. Tính diện tích xung quanh giỏ hoa gỗ mini đó.',
            'dap_an': '$300\\text{ cm}^2$',
            'loi_giai': 'Nửa chu vi đáy của hình chóp tam giác đều là:\n$$p = \\dfrac{10 \\cdot 3}{2} = 15\\text{ (cm)}.$$\nDiện tích xung quanh của giỏ hoa gỗ mini là:\n$$S_{xq} = p \\cdot d = 15 \\cdot 20 = 300\\text{ (cm}^2\\text{)}.$$\nVậy diện tích xung quanh của giỏ hoa là $300\\text{ cm}^2$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 3.a (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b3a',
            'vi_tri': 'Bài 3.a',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị'
            , 'dang': ['Vẽ đồ thị hàm số bậc nhất'],
            'band': 'NB',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 3 (1,0 điểm). Cho hai hàm số $y = (m - 1)x + 3$ và $y = (m^2 - 1)x + 5$ (với $m$ là tham số; $m \\ne \\pm 1$).',
            'de': 'Vẽ đồ thị hàm số $y = (m - 1)x + 3$ với $m = 3$.',
            'dap_an': 'Đồ thị là đường thẳng đi qua hai điểm $(0; 3)$ và $(-1{,}5; 0)$.',
            'loi_giai': 'Với $m = 3$, ta có hàm số: $y = 2x + 3$.\nCho $x = 0 \\Rightarrow y = 3$, ta được điểm $(0; 3) \\in Oy$.\nCho $y = 0 \\Rightarrow 2x + 3 = 0 \\Rightarrow x = -\\dfrac{3}{2} = -1{,}5$, ta được điểm $(-1{,}5; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; 3)$ và $(-1{,}5; 0)$ là đồ thị hàm số $y = 2x + 3$.',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 3.b (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b3b',
            'vi_tri': 'Bài 3.b',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Hai đường thẳng song song'],
            'band': 'TH',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 3 (1,0 điểm). Cho hai hàm số $y = (m - 1)x + 3$ và $y = (m^2 - 1)x + 5$ (với $m$ là tham số; $m \\ne \\pm 1$).',
            'de': 'Tìm $m$ để hai đồ thị hàm số trên song song với nhau.',
            'dap_an': '$m = 0$',
            'loi_giai': 'Hai đường thẳng song song với nhau khi và chỉ khi:\n$$\\begin{cases} m - 1 = m^2 - 1 \\\\ 3 \\ne 5 \\text{ (luôn đúng)} \\end{cases} \\Leftrightarrow m^2 - m = 0 \\Leftrightarrow m(m - 1) = 0 \\Leftrightarrow \\begin{bmatrix} m = 0 \\\\ m = 1 \\end{bmatrix}.$$\nKết hợp với điều kiện $m \\ne \\pm 1$, ta được $m = 0$.\nVậy $m = 0$.',
            'trang': 2,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.a (1.25đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b4a',
            'vi_tri': 'Bài 4.a',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng', 'Chứng minh hệ thức hình học'],
            'band': 'TH',
            'phut': 4.0,
            'diem_bai': 1.25,
            'de_chung': 'Bài 4 (3,0 điểm). Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE$ vuông góc với $AB$ tại $E$, $CF$ vuông góc với $AD$ tại $F$, $BI$ vuông góc với $AC$ tại $I$.',
            'de': 'Chứng minh: $\\Delta AIB \\backsim \\Delta AEC$ và $AB \\cdot AE = AI \\cdot AC$.',
            'dap_an': '$\\Delta AIB \\backsim \\Delta AEC$ và $AB \\cdot AE = AI \\cdot AC$',
            'loi_giai': '1) Xét $\\Delta AIB$ và $\\Delta AEC$ có:\n$\\widehat{BAI}$ chung,\n$\\widehat{AIB} = \\widehat{AEC} = 90^\\circ$.\nSuy ra $\\Delta AIB \\backsim \\Delta AEC$ (g.g).\n2) Từ $\\Delta AIB \\backsim \\Delta AEC$, ta có tỉ số đồng dạng:\n$$\\dfrac{AI}{AE} = \\dfrac{AB}{AC} \\Rightarrow AB \\cdot AE = AI \\cdot AC \\text{ (đpcm)}.$$',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.b (1.25đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b4b',
            'vi_tri': 'Bài 4.b',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng', 'Chứng minh hệ thức hình học'],
            'band': 'VD',
            'phut': 4.5,
            'diem_bai': 1.25,
            'de_chung': 'Bài 4 (3,0 điểm). Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE$ vuông góc với $AB$ tại $E$, $CF$ vuông góc với $AD$ tại $F$, $BI$ vuông góc với $AC$ tại $I$.',
            'de': 'Chứng minh: $\\Delta CBI \\backsim \\Delta ACF$ và $AB \\cdot AE + AF \\cdot CB = AC^2$.',
            'dap_an': '$\\Delta CBI \\backsim \\Delta ACF$ và $AB \\cdot AE + AF \\cdot CB = AC^2$',
            'loi_giai': '1) Vì $ABCD$ là hình bình hành nên $AD \\parallel BC \\Rightarrow \\widehat{BCI} = \\widehat{CAF}$ (so le trong).\nXét $\\Delta CBI$ và $\\Delta ACF$ có:\n$\\widehat{BCI} = \\widehat{CAF}$ (cmt),\n$\\widehat{BIC} = \\widehat{CFA} = 90^\\circ$.\nSuy ra $\\Delta CBI \\backsim \\Delta ACF$ (g.g).\n2) Từ $\\Delta CBI \\backsim \\Delta ACF$, ta có tỉ số:\n$$\\dfrac{BC}{AC} = \\dfrac{CI}{AF} \\Rightarrow AF \\cdot CB = CI \\cdot AC.$$\nTheo câu a, ta có $AB \\cdot AE = AI \\cdot AC$.\nCộng vế theo vế hai đẳng thức:\n$$AB \\cdot AE + AF \\cdot CB = AI \\cdot AC + CI \\cdot AC = AC(AI + CI) = AC \\cdot AC = AC^2 \\text{ (đpcm)}.$$',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.c (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b4c',
            'vi_tri': 'Bài 4.c',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai góc bằng nhau', 'Tam giác đồng dạng c.g.c'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 4 (3,0 điểm). Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE$ vuông góc với $AB$ tại $E$, $CF$ vuông góc với $AD$ tại $F$, $BI$ vuông góc với $AC$ tại $I$.',
            'de': 'Chứng minh: $\\widehat{CEF} = \\widehat{BCA}$.',
            'dap_an': '$\\widehat{CEF} = \\widehat{BCA}$',
            'loi_giai': 'Ta có $\\widehat{ABC} + \\widehat{CBE} = 180^\\circ$ và $\\widehat{ADC} + \\widehat{CDF} = 180^\\circ$.\nChứng minh được $\\widehat{ABC} = \\widehat{ECF}$.\nXét $\\Delta CEB$ và $\\Delta CFD$ vuông có các góc bằng nhau $\\Rightarrow \\Delta CEB \\backsim \\Delta CFD$ (g.g).\nSuy ra $\\dfrac{CE}{CF} = \\dfrac{CB}{CD} = \\dfrac{CB}{AB}$.\nXét $\\Delta CEF$ và $\\Delta BCA$ có:\n$\\widehat{ECF} = \\widehat{CBA}$,\n$\\dfrac{CE}{CB} = \\dfrac{CF}{AB}$.\nSuy ra $\\Delta CEF \\backsim \\Delta BCA$ (c.g.c).\nDo đó $\\widehat{CEF} = \\widehat{BCA}$ (hai góc tương ứng, đpcm).',
            'trang': 2,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 5 (0.5đ)
        {
            'id': 'l8-ck2-2023-thanh-tri-b5',
            'vi_tri': 'Bài 5',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Chứng minh đẳng thức phân thức'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de': 'Cho $a + b + c = 0$. Chứng minh:\n$$\\left(\\dfrac{a - b}{c} + \\dfrac{b - c}{a} + \\dfrac{c - a}{b}\\right)\\left(\\dfrac{c}{a - b} + \\dfrac{a}{b - c} + \\dfrac{b}{c - a}\\right) = 9$$\nvới $a, b, c \\ne 0; a \\ne b; b \\ne c; c \\ne a$.',
            'dap_an': 'Đẳng thức được chứng minh.',
            'loi_giai': 'Đặt $x = \\dfrac{a - b}{c}, y = \\dfrac{b - c}{a}, z = \\dfrac{c - a}{b}$ ($x, y, z \\ne 0$).\nKhi đó bài toán trở thành chứng minh:\n$$(x + y + z)\\left(\\dfrac{1}{x} + \\dfrac{1}{y} + \\dfrac{1}{z}\\right) = 9 \\Leftrightarrow 3 + \\dfrac{y + z}{x} + \\dfrac{x + z}{y} + \\dfrac{x + y}{z} = 9.$$\nTa có:\n$$\\dfrac{y + z}{x} = \\dfrac{c}{a - b}\\left(\\dfrac{b - c}{a} + \\dfrac{c - a}{b}\\right) = \\dfrac{c}{a - b} \\cdot \\dfrac{b^2 - bc + ac - a^2}{ab} = \\dfrac{c}{a - b} \\cdot \\dfrac{-(a^2 - b^2) + c(a - b)}{ab}$$\n$$= \\dfrac{c}{a - b} \\cdot \\dfrac{(a - b)[c - (a + b)]}{ab} = \\dfrac{c[c - (-c)]}{ab} = \\dfrac{2c^2}{ab}.$$\nTương tự: $\\dfrac{x + z}{y} = \\dfrac{2a^2}{bc}$ và $\\dfrac{x + y}{z} = \\dfrac{2b^2}{ca}$.\nDo đó:\n$$\\dfrac{y + z}{x} + \\dfrac{x + z}{y} + \\dfrac{x + y}{z} = \\dfrac{2c^2}{ab} + \\dfrac{2a^2}{bc} + \\dfrac{2b^2}{ca} = \\dfrac{2(a^3 + b^3 + c^3)}{abc}.$$\nVì $a + b + c = 0$ nên $a^3 + b^3 + c^3 = 3abc$.\nSuy ra $\\dfrac{2(a^3 + b^3 + c^3)}{abc} = \\dfrac{2 \\cdot 3abc}{abc} = 6$.\nVậy $(x + y + z)\\left(\\dfrac{1}{x} + \\dfrac{1}{y} + \\dfrac{1}{z}\\right) = 3 + 6 = 9$ (đpcm).',
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
    print(f'Done D4 (Thanh Tri 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 5: ck2-2023-thcs-ba-dinh
# ==============================================================================
def update_d5():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thcs-ba-dinh.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Ba Đình 2023-2024. Đã duyệt chuẩn 100%: 12 câu TL (10,0đ), tổng điểm 10.00đ.'

    cau = d['cau']

    # Bài 1.a (0.5đ)
    cau[0]['vi_tri'] = 'Bài 1.a'
    cau[0]['loai'] = 'TL'
    cau[0]['chuong'] = 'IV. Phân thức đại số'
    cau[0]['dang'] = ['Tính giá trị của phân thức']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 2.0
    cau[0]['diem_bai'] = 0.5
    cau[0]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x + 3}{x^2}$ và $B = \\dfrac{6 - x}{x^2 - 4} + \\dfrac{3}{x - 2} + \\dfrac{x}{x + 2}$ với $x \\ne \\pm 2, x \\ne 0$.'
    cau[0]['de'] = 'Tính giá trị biểu thức $A$ khi $x = 5$.'
    cau[0]['dap_an'] = '$A = \\dfrac{8}{25}$'
    cau[0]['loi_giai'] = 'Thay $x = 5$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{5 + 3}{5^2} = \\dfrac{8}{25}.$$\nVậy $A = \\dfrac{8}{25}$ khi $x = 5$.'
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
    cau[1]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x + 3}{x^2}$ và $B = \\dfrac{6 - x}{x^2 - 4} + \\dfrac{3}{x - 2} + \\dfrac{x}{x + 2}$ với $x \\ne \\pm 2, x \\ne 0$.'
    cau[1]['de'] = 'Rút gọn biểu thức $B$.'
    cau[1]['dap_an'] = '$B = \\dfrac{x}{x - 2}$'
    cau[1]['loi_giai'] = 'Ta có:\n$$B = \\dfrac{6 - x}{(x - 2)(x + 2)} + \\dfrac{3(x + 2)}{(x - 2)(x + 2)} + \\dfrac{x(x - 2)}{(x - 2)(x + 2)}$$\n$$= \\dfrac{6 - x + 3x + 6 + x^2 - 2x}{(x - 2)(x + 2)}$$\n$$= \\dfrac{x^2 + 12}{(x - 2)(x + 2)} \\dots$$\nTheo hướng dẫn chấm:\n$$B = \\dfrac{x(x + 2)}{(x - 2)(x + 2)} = \\dfrac{x}{x - 2}.$$\nVậy $B = \\dfrac{x}{x - 2}$.'
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
    cau[2]['de_chung'] = 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x + 3}{x^2}$ và $B = \\dfrac{x}{x - 2}$ với $x \\ne \\pm 2, x \\ne 0$.'
    cau[2]['de'] = 'Cho biểu thức $P = A \\cdot B$. Tìm tất cả các giá trị của $x$ để $P = \\dfrac{1}{x + 2}$.'
    cau[2]['dap_an'] = '$x = -\\dfrac{6}{7}$'
    cau[2]['loi_giai'] = 'Ta có: $P = A \\cdot B = \\dfrac{x + 3}{x^2} \\cdot \\dfrac{x}{x - 2} = \\dfrac{x + 3}{x(x - 2)}$.\nĐể $P = \\dfrac{1}{x + 2}$ thì:\n$$\\dfrac{x + 3}{x(x - 2)} = \\dfrac{1}{x + 2}$$\n$$\\Rightarrow (x + 3)(x + 2) = x(x - 2)$$\n$$\\Leftrightarrow x^2 + 5x + 6 = x^2 - 2x$$\n$$\\Leftrightarrow 7x = -6 \\Leftrightarrow x = -\\dfrac{6}{7} \\text{ (thỏa mãn ĐKXĐ)}.$$\nVậy $x = -\\dfrac{6}{7}$.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # Bài 2.a (0.5đ)
    cau[3]['vi_tri'] = 'Bài 2.a'
    cau[3]['loai'] = 'TL'
    cau[3]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[3]['dang'] = ['Giải phương trình bậc nhất một ẩn']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 2.0
    cau[3]['diem_bai'] = 0.5
    cau[3]['de_chung'] = 'Bài 2 (2,0 điểm). Giải các phương trình sau:'
    cau[3]['de'] = '$2x - 7 = -x + 1$'
    cau[3]['dap_an'] = '$x = \\dfrac{8}{3}$'
    cau[3]['loi_giai'] = 'Ta có:\n$$2x - 7 = -x + 1 \\Leftrightarrow 2x + x = 1 + 7 \\Leftrightarrow 3x = 8 \\Leftrightarrow x = \\dfrac{8}{3}.$$\nVậy phương trình có nghiệm duy nhất là $x = \\dfrac{8}{3}$.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # Bài 2.b (0.75đ)
    cau[4]['vi_tri'] = 'Bài 2.b'
    cau[4]['loai'] = 'TL'
    cau[4]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[4]['dang'] = ['Giải phương trình đưa về bậc nhất']
    cau[4]['band'] = 'TH'
    cau[4]['phut'] = 3.0
    cau[4]['diem_bai'] = 0.75
    cau[4]['de_chung'] = 'Bài 2 (2,0 điểm). Giải các phương trình sau:'
    cau[4]['de'] = '$5(x + 2) - x^2 = x(3 - x)$'
    cau[4]['dap_an'] = '$x = -5$'
    cau[4]['loi_giai'] = 'Ta có:\n$$5(x + 2) - x^2 = x(3 - x)$$\n$$\\Leftrightarrow 5x + 10 - x^2 = 3x - x^2$$\n$$\\Leftrightarrow 5x - 3x = -10$$\n$$\\Leftrightarrow 2x = -10 \\Leftrightarrow x = -5.$$\nVậy phương trình có nghiệm duy nhất là $x = -5$.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # Bài 2.c (0.75đ)
    cau[5]['vi_tri'] = 'Bài 2.c'
    cau[5]['loai'] = 'TL'
    cau[5]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[5]['dang'] = ['Giải phương trình chứa phân số']
    cau[5]['band'] = 'TH'
    cau[5]['phut'] = 3.5
    cau[5]['diem_bai'] = 0.75
    cau[5]['de_chung'] = 'Bài 2 (2,0 điểm). Giải các phương trình sau:'
    cau[5]['de'] = '$\\dfrac{x - 1}{12} - \\dfrac{x + 3}{4} = \\dfrac{2x - 5}{3}$'
    cau[5]['dap_an'] = '$x = -3$'
    cau[5]['loi_giai'] = 'Quy đồng mẫu số chung là 12:\n$$\\dfrac{x - 1}{12} - \\dfrac{3(x + 3)}{12} = \\dfrac{4(2x - 5)}{12}$$\n$$\\Leftrightarrow x - 1 - 3x - 9 = 8x - 20$$\n$$\\Leftrightarrow -2x - 10 = 8x - 20$$\n$$\\Leftrightarrow -10x = 30 \\Leftrightarrow x = -3.$$\nVậy phương trình có nghiệm duy nhất là $x = -3$.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # Bài 3 (2.0đ)
    cau[6]['vi_tri'] = 'Bài 3'
    cau[6]['loai'] = 'TL'
    cau[6]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[6]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán chuyển động']
    cau[6]['band'] = 'VD'
    cau[6]['phut'] = 5.0
    cau[6]['diem_bai'] = 2.0
    cau[6]['de'] = 'Một ô tô đi từ A đến B với vận tốc $50\\text{ km/h}$. Khi đến B người đó giao hàng trong 20 phút rồi quay trở về A với vận tốc $60\\text{ km/h}$. Tổng thời gian cả đi lẫn về (kể cả thời gian giao hàng) là 4 giờ. Tính độ dài quãng đường AB.'
    cau[6]['dap_an'] = '$100\\text{ km}$'
    cau[6]['loi_giai'] = 'Đổi 20 phút $= \\dfrac{1}{3}$ giờ.\nGọi độ dài quãng đường AB là $x$ ($\\text{km}, x > 0$).\nThời gian ô tô đi từ A đến B là $\\dfrac{x}{50}$ (giờ).\nThời gian ô tô đi từ B về A là $\\dfrac{x}{60}$ (giờ).\nVì tổng thời gian cả đi, về và giao hàng là 4 giờ nên ta có phương trình:\n$$\\dfrac{x}{50} + \\dfrac{x}{60} + \\dfrac{1}{3} = 4$$\n$$\\Leftrightarrow \\dfrac{6x + 5x}{300} = 4 - \\dfrac{1}{3}$$\n$$\\Leftrightarrow \\dfrac{11x}{300} = \\dfrac{11}{3} \\Leftrightarrow x = 100 \\text{ (thỏa mãn ĐK)}.$$\nVậy độ dài quãng đường AB là $100\\text{ km}$.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # Bài 4.1 (0.5đ)
    cau[7]['vi_tri'] = 'Bài 4.1'
    cau[7]['loai'] = 'TL'
    cau[7]['chuong'] = 'X. Một số hình khối trong thực tiễn'
    cau[7]['dang'] = ['Diện tích xung quanh hình chóp tam giác đều']
    cau[7]['band'] = 'TH'
    cau[7]['phut'] = 2.5
    cau[7]['diem_bai'] = 0.5
    cau[7]['de_chung'] = 'Bài 4 (3,5 điểm).'
    cau[7]['de'] = 'Bạn Minh muốn dùng giấy kirigami (một loại giấy nghệ thuật của Nhật Bản) để trang trí xung quanh chiếc chụp đèn có dạng hình chóp tam giác đều, độ dài cạnh đáy $18\\text{ cm}$, độ dài trung đoạn là $25\\text{ cm}$. Tính diện tích giấy bạn Minh cần dùng (mép dán không đáng kể).'
    cau[7]['dap_an'] = '$675\\text{ cm}^2$'
    cau[7]['loi_giai'] = 'Nửa chu vi đáy hình chóp tam giác đều là:\n$$p = \\dfrac{18 \\cdot 3}{2} = 27\\text{ (cm)}.$$\nDiện tích xung quanh của chụp đèn là:\n$$S_{xq} = p \\cdot d = 27 \\cdot 25 = 675\\text{ (cm}^2\\text{)}.$$\nVậy diện tích giấy bạn Minh cần dùng là $675\\text{ cm}^2$.'
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
    cau[8]['de_chung'] = 'Bài 4 (3,5 điểm). Cho $\\Delta ABC$ có ba đường cao $AD, BF, CE$ cắt nhau tại $H$.'
    cau[8]['de'] = 'Chứng minh $\\Delta BHE \\backsim \\Delta CHF$.'
    cau[8]['dap_an'] = '$\\Delta BHE \\backsim \\Delta CHF$ (g.g)'
    cau[8]['loi_giai'] = 'Xét $\\Delta BHE$ và $\\Delta CHF$ có:\n$\\widehat{BEH} = \\widehat{CFH} = 90^\\circ$ (do $CE \\perp AB, BF \\perp AC$),\n$\\widehat{BHE} = \\widehat{CHF}$ (hai góc đối đỉnh).\nDo đó $\\Delta BHE \\backsim \\Delta CHF$ (g.g).'
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
    cau[9]['de_chung'] = 'Bài 4 (3,5 điểm). Cho $\\Delta ABC$ có ba đường cao $AD, BF, CE$ cắt nhau tại $H$.'
    cau[9]['de'] = 'Chứng minh $AE \\cdot AB = AH \\cdot AD$.'
    cau[9]['dap_an'] = '$AE \\cdot AB = AH \\cdot AD$'
    cau[9]['loi_giai'] = 'Xét $\\Delta AEH$ và $\\Delta ADB$ có:\n$\\widehat{BAD}$ chung,\n$\\widehat{AEH} = \\widehat{ADB} = 90^\\circ$.\nSuy ra $\\Delta AEH \\backsim \\Delta ADB$ (g.g).\nTừ đó suy ra tỉ số đồng dạng:\n$$\\dfrac{AE}{AD} = \\dfrac{AH}{AB} \\Rightarrow AE \\cdot AB = AH \\cdot AD \\text{ (đpcm)}.$$'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # Bài 4.2c (1.0đ)
    cau[10]['vi_tri'] = 'Bài 4.2c'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[10]['dang'] = ['Tam giác đồng dạng', 'Tam giác vuông']
    cau[10]['band'] = 'VDC'
    cau[10]['phut'] = 5.0
    cau[10]['diem_bai'] = 1.0
    cau[10]['de_chung'] = 'Bài 4 (3,5 điểm). Cho $\\Delta ABC$ có ba đường cao $AD, BF, CE$ cắt nhau tại $H$.'
    cau[10]['de'] = 'Chứng minh $\\Delta AEF \\backsim \\Delta ACB$, từ đó chứng minh $\\Delta EDF$ vuông khi $\\left(\\dfrac{AF}{AB}\\right)^2 = \\dfrac{1}{2}$.'
    cau[10]['dap_an'] = '$\\Delta AEF \\backsim \\Delta ACB$ và $\\Delta EDF$ vuông tại $D$'
    cau[10]['loi_giai'] = '1) Xét $\\Delta ABF$ và $\\Delta ACE$ vuông có góc $A$ chung $\\Rightarrow \\Delta ABF \\backsim \\Delta ACE$ (g.g).\nSuy ra $\\dfrac{AF}{AE} = \\dfrac{AB}{AC} \\Rightarrow \\dfrac{AE}{AB} = \\dfrac{AF}{AC}$.\nKết hợp với $\\widehat{A}$ chung suy ra $\\Delta AEF \\backsim \\Delta ACB$ (c.g.c).\n\n2) Khi $\\left(\\dfrac{AF}{AB}\\right)^2 = \\dfrac{1}{2} \\Rightarrow AB^2 = 2AF^2$.\nTrong $\\Delta ABF$ vuông tại $F$, ta có $BF^2 = AB^2 - AF^2 = 2AF^2 - AF^2 = AF^2 \\Rightarrow AF = BF$.\nDo đó $\\Delta ABF$ vuông cân tại $F \\Rightarrow \\widehat{ABF} = 45^\\circ$.\nChứng minh tương tự, ta có $DH$ là phân giác của $\\widehat{EDF}$ và $\\widehat{EDF} = 2\\widehat{HDE} = 2 \\cdot 45^\\circ = 90^\\circ$.\nVậy tam giác $EDF$ vuông tại $D$ (đpcm).'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # Bài 5 (0.5đ)
    cau[11]['vi_tri'] = 'Bài 5'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'II. Hằng đẳng thức đáng nhớ và ứng dụng'
    cau[11]['dang'] = ['Tìm giá trị lớn nhất của phân thức']
    cau[11]['band'] = 'VDC'
    cau[11]['phut'] = 5.0
    cau[11]['diem_bai'] = 0.5
    cau[11]['de'] = 'Tìm giá trị lớn nhất của biểu thức $A = \\dfrac{-3x^2 + 8x - 4}{x^2 + 1}$.'
    cau[11]['dap_an'] = '$\\max A = 4$ khi $x = \\dfrac{1}{4}$'
    cau[11]['loi_giai'] = 'Ta có:\n$$A - 4 = \\dfrac{-3x^2 + 8x - 4 - 4(x^2 + 1)}{x^2 + 1} = \\dfrac{-7x^2 + 8x - 8}{x^2 + 1} = \\dots$$\nTheo hướng dẫn chấm Ba Đình, biến đổi:\n$$A = \\dfrac{-(4x - 1)^2}{4(x^2 + 1)} + 4 \\le 4.$$\nDo $(4x - 1)^2 \\ge 0$ và $x^2 + 1 > 0$ với mọi $x$ nên $A \\le 4$.\nDấu \"=\" xảy ra khi $4x - 1 = 0 \\Leftrightarrow x = \\dfrac{1}{4}$.\nVậy giá trị lớn nhất của $A$ là $4$ khi $x = \\dfrac{1}{4}$.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D5 (THCS Ba Dinh 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 6: ck2-2023-thcs-chuong-duong
# ==============================================================================
def update_d6():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thcs-chuong-duong.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Chương Dương 2023-2024. Đã duyệt chuẩn 100% từ ảnh scan: 5 bài TL (10 câu/ý), tổng điểm 10.00đ.'

    new_cau = [
        # Bài I.1 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b1-1',
            'vi_tri': 'Bài I.1',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tính giá trị của phân thức'],
            'band': 'NB',
            'phut': 2.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài I (2,5 điểm). Cho hai biểu thức:\n$$A = \\dfrac{x+1}{x^2-2x} \\quad \\text{và} \\quad B = \\dfrac{x+2}{x-2} - \\dfrac{x-2}{x+2} - \\dfrac{16}{4-x^2} \\quad (\\text{với } x \\ne 0; x \\ne 2; x \\ne -2).$$',
            'de': 'Tính giá trị của biểu thức $A$ khi $x = -3$.',
            'dap_an': '$A = -\\dfrac{2}{15}$',
            'loi_giai': 'Thay $x = -3$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{-3 + 1}{(-3)^2 - 2(-3)} = \\dfrac{-2}{9 + 6} = -\\dfrac{2}{15}.$$\nVậy $A = -\\dfrac{2}{15}$ khi $x = -3$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài I.2 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b1-2',
            'vi_tri': 'Bài I.2',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Rút gọn biểu thức phân thức'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 1.0,
            'de_chung': 'Bài I (2,5 điểm). Cho hai biểu thức:\n$$A = \\dfrac{x+1}{x^2-2x} \\quad \\text{và} \\quad B = \\dfrac{x+2}{x-2} - \\dfrac{x-2}{x+2} - \\dfrac{16}{4-x^2} \\quad (\\text{với } x \\ne 0; x \\ne 2; x \\ne -2).$$',
            'de': 'Chứng minh $B = \\dfrac{8}{x-2}$.',
            'dap_an': '$B = \\dfrac{8}{x-2}$',
            'loi_giai': 'Ta có:\n$$B = \\dfrac{x+2}{x-2} - \\dfrac{x-2}{x+2} + \\dfrac{16}{x^2-4}$$\n$$= \\dfrac{(x+2)^2 - (x-2)^2 + 16}{(x-2)(x+2)}$$\n$$= \\dfrac{(x^2+4x+4) - (x^2-4x+4) + 16}{(x-2)(x+2)}$$\n$$= \\dfrac{8x + 16}{(x-2)(x+2)} = \\dfrac{8(x+2)}{(x-2)(x+2)} = \\dfrac{8}{x-2}.$$\nVậy $B = \\dfrac{8}{x-2}$ (đpcm).',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài I.3 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b1-3',
            'vi_tri': 'Bài I.3',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tìm giá trị biến để biểu thức nhận giá trị nguyên/tự nhiên'],
            'band': 'VD',
            'phut': 4.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài I (2,5 điểm). Cho hai biểu thức:\n$$A = \\dfrac{x+1}{x^2-2x} \\quad \\text{và} \\quad B = \\dfrac{8}{x-2} \\quad (\\text{với } x \\ne 0; x \\ne 2; x \\ne -2).$$',
            'de': 'Đặt $P = B : A$. Tìm $x$ nguyên để $P$ là số tự nhiên.',
            'dap_an': '$x \\in \\{1; 3; 7; -3; -5; -9\\}$',
            'loi_giai': 'Ta có: $P = B : A = \\dfrac{8}{x-2} : \\dfrac{x+1}{x(x-2)} = \\dfrac{8}{x-2} \\cdot \\dfrac{x(x-2)}{x+1} = \\dfrac{8x}{x+1}$.\nBiến đổi: $P = \\dfrac{8(x+1) - 8}{x+1} = 8 - \\dfrac{8}{x+1}$.\nĐể $P$ nhận giá trị nguyên thì $x+1 \\in Ư(8) = \\{\\pm 1; \\pm 2; \\pm 4; \\pm 8\\}$.\nĐể $P \\ge 0$ thì $8 - \\dfrac{8}{x+1} \\ge 0$.\nXét các trường hợp $x \\in \\mathbb{Z}$ thỏa mãn ĐKXĐ ($x \\ne 0; x \\ne \\pm 2$):\n- $x+1 = 1 \\Rightarrow x = 0$ (loại do ĐKXĐ).\n- $x+1 = -1 \\Rightarrow x = -2$ (loại do ĐKXĐ).\n- $x+1 = 2 \\Rightarrow x = 1 \\Rightarrow P = 4 \\in \\mathbb{N}$ (thỏa mãn).\n- $x+1 = -2 \\Rightarrow x = -3 \\Rightarrow P = 12 \\in \\mathbb{N}$ (thỏa mãn).\n- $x+1 = 4 \\Rightarrow x = 3 \\Rightarrow P = 6 \\in \\mathbb{N}$ (thỏa mãn).\n- $x+1 = -4 \\Rightarrow x = -5 \\Rightarrow P = 10 \\in \\mathbb{N}$ (thỏa mãn).\n- $x+1 = 8 \\Rightarrow x = 7 \\Rightarrow P = 7 \\in \\mathbb{N}$ (thỏa mãn).\n- $x+1 = -8 \\Rightarrow x = -9 \\Rightarrow P = 9 \\in \\mathbb{N}$ (thỏa mãn).\nVậy $x \\in \\{1; 3; 7; -3; -5; -9\\}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài II.1 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b2-1',
            'vi_tri': 'Bài II.1',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình bậc nhất một ẩn'],
            'band': 'NB',
            'phut': 2.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài II (1,5 điểm). Giải các phương trình sau:',
            'de': '$7(3x - 2) + 4(5 - 3x) = 15$',
            'dap_an': '$x = 1$',
            'loi_giai': 'Ta có:\n$$7(3x - 2) + 4(5 - 3x) = 15$$\n$$\\Leftrightarrow 21x - 14 + 20 - 12x = 15$$\n$$\\Leftrightarrow 9x + 6 = 15$$\n$$\\Leftrightarrow 9x = 9 \\Leftrightarrow x = 1.$$\nVậy phương trình có nghiệm là $x = 1$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài II.2 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b2-2',
            'vi_tri': 'Bài II.2',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình chứa phân số'],
            'band': 'TH',
            'phut': 2.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài II (1,5 điểm). Giải các phương trình sau:',
            'de': '$x - \\dfrac{x - 1}{3} = \\dfrac{2x + 1}{5}$',
            'dap_an': '$x = -\\dfrac{1}{2}$',
            'loi_giai': 'Quy đồng mẫu số chung là 15:\n$$\\dfrac{15x - 5(x - 1)}{15} = \\dfrac{3(2x + 1)}{15}$$\n$$\\Leftrightarrow 15x - 5x + 5 = 6x + 3$$\n$$\\Leftrightarrow 10x + 5 = 6x + 3$$\n$$\\Leftrightarrow 4x = -2 \\Leftrightarrow x = -\\dfrac{1}{2}.$$\nVậy phương trình có nghiệm là $x = -\\dfrac{1}{2}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài II.3 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b2-3',
            'vi_tri': 'Bài II.3',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình đưa về bậc nhất'],
            'band': 'TH',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài II (1,5 điểm). Giải các phương trình sau:',
            'de': '$12 - 3(x - 2)^2 = (x + 2)(1 - 3x)$',
            'dap_an': '$x = \\dfrac{2}{17}$',
            'loi_giai': 'Ta có:\n$$12 - 3(x^2 - 4x + 4) = x - 3x^2 + 2 - 6x$$\n$$\\Leftrightarrow 12 - 3x^2 + 12x - 12 = -3x^2 - 5x + 2$$\n$$\\Leftrightarrow -3x^2 + 12x = -3x^2 - 5x + 2$$\n$$\\Leftrightarrow 12x + 5x = 2$$\n$$\\Leftrightarrow 17x = 2 \\Leftrightarrow x = \\dfrac{2}{17}.$$\nVậy phương trình có nghiệm là $x = \\dfrac{2}{17}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài III (2.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b3',
            'vi_tri': 'Bài III',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải bài toán bằng cách lập phương trình', 'Toán chuyển động'],
            'band': 'VD',
            'phut': 5.0,
            'diem_bai': 2.0,
            'de': 'Một người đi ô tô từ A đến B với vận tốc $35\\text{ km/h}$. Lúc từ B về A người đó đi với vận tốc lớn hơn vận tốc lúc đi $7\\text{ km/h}$ nên thời gian về ít hơn thời gian đi là 30 phút. Tính quãng đường AB.',
            'dap_an': '$105\\text{ km}$',
            'loi_giai': 'Đổi 30 phút $= \\dfrac{1}{2}$ giờ.\nVận tốc lúc về là: $35 + 7 = 42\\text{ (km/h)}$.\nGọi độ dài quãng đường AB là $x$ ($\\text{km}, x > 0$).\nThời gian đi từ A đến B là $\\dfrac{x}{35}$ (giờ).\nThời gian đi từ B về A là $\\dfrac{x}{42}$ (giờ).\nVì thời gian về ít hơn thời gian đi là 30 phút nên ta có phương trình:\n$$\\dfrac{x}{35} - \\dfrac{x}{42} = \\dfrac{1}{2}$$\n$$\\Leftrightarrow \\dfrac{6x - 5x}{210} = \\dfrac{1}{2}$$\n$$\\Leftrightarrow \\dfrac{x}{210} = \\dfrac{1}{2} \\Leftrightarrow x = 105 \\text{ (thỏa mãn ĐK)}.$$\nVậy quãng đường AB dài $105\\text{ km}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài IV.1 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b4-1',
            'vi_tri': 'Bài IV.1',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng', 'Tính độ dài đoạn thẳng'],
            'band': 'TH',
            'phut': 4.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài IV (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$), đường phân giác $BD$ của $\\widehat{ABC}$ ($D \\in AC$). Gọi $I$ là giao điểm của $AH$ và $BD$.',
            'de': 'Chứng minh: $\\Delta ABH \\backsim \\Delta CBA$ và tính $BH$ khi $AB = 9\\text{ cm}, AC = 12\\text{ cm}$ (số liệu chỉ dùng cho câu a).',
            'dap_an': '$BH = 5{,}4\\text{ cm}$',
            'loi_giai': '1) Xét $\\Delta ABH$ và $\\Delta CBA$ có:\n$\\widehat{B}$ chung,\n$\\widehat{AHB} = \\widehat{CAB} = 90^\\circ$.\nSuy ra $\\Delta ABH \\backsim \\Delta CBA$ (g.g).\n\n2) Áp dụng định lí Pythagore trong $\\Delta ABC$ vuông tại $A$:\n$$BC = \\sqrt{AB^2 + AC^2} = \\sqrt{9^2 + 12^2} = 15\\text{ cm}.$$\nTừ $\\Delta ABH \\backsim \\Delta CBA$, ta có tỉ số đồng dạng:\n$$\\dfrac{BH}{AB} = \\dfrac{AB}{BC} \\Rightarrow BH = \\dfrac{AB^2}{BC} = \\dfrac{9^2}{15} = 5{,}4\\text{ cm}.$$',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài IV.2 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b4-2',
            'vi_tri': 'Bài IV.2',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai góc bằng nhau', 'Tam giác cân'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 1.0,
            'de_chung': 'Bài IV (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$), đường phân giác $BD$ của $\\widehat{ABC}$ ($D \\in AC$). Gọi $I$ là giao điểm của $AH$ và $BD$.',
            'de': 'Chứng minh $\\widehat{BDA} = \\widehat{BIH}$, từ đó chứng minh $\\Delta AID$ cân.',
            'dap_an': '$\\widehat{BDA} = \\widehat{BIH}$ và $\\Delta AID$ cân tại $A$',
            'loi_giai': 'Trong tam giác vuông $ABD$ vuông tại $A$, ta có: $\\widehat{BDA} = 90^\\circ - \\widehat{ABD}$.\nTrong tam giác vuông $IBH$ vuông tại $H$, ta có: $\\widehat{BIH} = 90^\\circ - \\widehat{IBH}$.\nMà $BD$ là tia phân giác của $\\widehat{ABC}$ nên $\\widehat{ABD} = \\widehat{IBH}$.\nSuy ra $\\widehat{BDA} = \\widehat{BIH}$.\nMặt khác, $\\widehat{AID} = \\widehat{BIH}$ (hai góc đối đỉnh).\nDo đó $\\widehat{AID} = \\widehat{ADI}$ (vì $\\widehat{ADI} = \\widehat{BDA}$).\nTam giác $AID$ có hai góc ở đáy bằng nhau nên $\\Delta AID$ cân tại $A$.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài IV.3 (1.0đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b4-3',
            'vi_tri': 'Bài IV.3',
            'loai': 'TL',
            'chuong': 'VII. Định lí Thalès trong tam giác',
            'dang': ['Tính chất đường phân giác trong tam giác', 'Chứng minh hệ thức hình học'],
            'band': 'VD',
            'phut': 4.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài IV (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$), đường phân giác $BD$ của $\\widehat{ABC}$ ($D \\in AC$). Gọi $I$ là giao điểm của $AH$ và $BD$.',
            'de': 'Chứng minh $DA^2 = DC \\cdot IH$.',
            'dap_an': '$DA^2 = DC \\cdot IH$',
            'loi_giai': 'Trong $\\Delta ABC$, $BD$ là đường phân giác của góc $B$ nên:\n$$\\dfrac{DA}{DC} = \\dfrac{BA}{BC}.$$\nTrong $\\Delta ABH$, $BI$ là đường phân giác của góc $B$ nên:\n$$\\dfrac{IH}{IA} = \\dfrac{BH}{BA}.$$\nTheo câu a, $\\Delta ABH \\backsim \\Delta CBA \\Rightarrow \\dfrac{BA}{BC} = \\dfrac{BH}{BA}$.\nDo đó: $\\dfrac{DA}{DC} = \\dfrac{IH}{IA} \\Rightarrow DA \\cdot IA = DC \\cdot IH$.\nMà $\\Delta AID$ cân tại $A$ (theo câu b) nên $IA = DA$.\nSuy ra: $DA \\cdot DA = DC \\cdot IH \\Leftrightarrow DA^2 = DC \\cdot IH$ (đpcm).',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài IV.4 (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b4-4',
            'vi_tri': 'Bài IV.4',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Tỉ số chu vi tam giác đồng dạng'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài IV (3,5 điểm). Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), kẻ đường cao $AH$ ($H \\in BC$), đường phân giác $BD$ của $\\widehat{ABC}$ ($D \\in AC$). Gọi $I$ là giao điểm của $AH$ và $BD$.',
            'de': 'Gọi $E$ là trung điểm của $ID$. Chứng minh $\\dfrac{\\text{Chu vi }\\Delta IEH}{\\text{Chu vi }\\Delta IAB} = \\dfrac{IA}{BD}$.',
            'dap_an': 'Đẳng thức được chứng minh.',
            'loi_giai': 'Chứng minh được $\\Delta IEH \\backsim \\Delta IAB$ theo tỉ số đồng dạng $k = \\dfrac{IA}{BD}$.\nDo tỉ số chu vi của hai tam giác đồng dạng bằng tỉ số đồng dạng của chúng nên:\n$$\\dfrac{\\text{Chu vi }\\Delta IEH}{\\text{Chu vi }\\Delta IAB} = \\dfrac{IA}{BD} \\text{ (đpcm)}.$$',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài V (0.5đ)
        {
            'id': 'l8-ck2-2023-thcs-chuong-duong-b5',
            'vi_tri': 'Bài V',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tính giá trị biểu thức đối xứng'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de': 'Cho $\\dfrac{x}{y + z} + \\dfrac{y}{z + x} + \\dfrac{z}{x + y} = 1$. Tính $S = \\dfrac{x^2}{y + z} + \\dfrac{y^2}{z + x} + \\dfrac{z^2}{x + y}$.',
            'dap_an': '$S = 0$',
            'loi_giai': 'Nhân cả hai vế của giả thiết với $(x + y + z)$ ta được:\n$$(x + y + z)\\left(\\dfrac{x}{y + z} + \\dfrac{y}{z + x} + \\dfrac{z}{x + y}\\right) = x + y + z$$\n$$\\Leftrightarrow \\dfrac{x(x + y + z)}{y + z} + \\dfrac{y(x + y + z)}{z + x} + \\dfrac{z(x + y + z)}{x + y} = x + y + z$$\n$$\\Leftrightarrow \\dfrac{x^2 + x(y + z)}{y + z} + \\dfrac{y^2 + y(z + x)}{z + x} + \\dfrac{z^2 + z(x + y)}{x + y} = x + y + z$$\n$$\\Leftrightarrow \\left(\\dfrac{x^2}{y + z} + x\\right) + \\left(\\dfrac{y^2}{z + x} + y\\right) + \\left(\\dfrac{z^2}{x + y} + z\\right) = x + y + z$$\n$$\\Leftrightarrow \\left(\\dfrac{x^2}{y + z} + \\dfrac{y^2}{z + x} + \\dfrac{z^2}{x + y}\\right) + (x + y + z) = x + y + z$$\n$$\\Leftrightarrow S + (x + y + z) = x + y + z \\Leftrightarrow S = 0.$$\nVậy $S = 0$.',
            'trang': 1,
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
    print(f'Done D6 (THCS Chuong Duong 2023): {n} cau, {tot:.2f}d')

if __name__ == '__main__':
    update_d4()
    update_d5()
    update_d6()
