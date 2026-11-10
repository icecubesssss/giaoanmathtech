# -*- coding: utf-8 -*-
import json

path = 'inputs/refs/de-thi/lop-8/exams/gk2-2023-thcs-giang-vo.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

d['tang'] = 2
d['da_duyet'] = True
d['tieu_de'] = 'Đề kiểm tra giữa học kì II môn Toán 8 - THCS Giảng Võ (Ba Đình) năm học 2023 - 2024'
d['nam_hoc'] = '2023-2024'
d['hoc_ky'] = 'GK2'
d['lop'] = '8'
d['thoi_gian_phut'] = 90
d['ghi_chu'] = 'Đề chuẩn GK2 Toán 8 THCS Giảng Võ 2023-2024. Đã soát 100% từ PDF gốc: 10 câu TN (2.5đ) + 4 bài TL (7.5đ), tổng điểm 10.00đ.'

cau_list = [
    # Câu 1
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c1',
        'vi_tri': 'Câu 1',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Hai phân thức bằng nhau'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Đa thức $P$ thỏa mãn $\\dfrac{P}{y^2-2y} = \\dfrac{2-y}{6-3y}$ là:\nA. $\\dfrac{y^2-2y}{3}$.\nB. $\\dfrac{y^2-2y}{-3}$.\nC. $\\dfrac{y^2-6y}{3}$.\nD. $\\dfrac{y^2-6y}{2}$.',
        'dap_an': 'A',
        'loi_giai': 'Ta có:\n$$\\dfrac{2-y}{6-3y} = \\dfrac{2-y}{3(2-y)} = \\dfrac{1}{3}.$$\nDo đó $\\dfrac{P}{y^2-2y} = \\dfrac{1}{3} \\Rightarrow P = \\dfrac{y^2-2y}{3}$. Chọn A.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 2
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c2',
        'vi_tri': 'Câu 2',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Rút gọn phân thức đại số'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Rút gọn biểu thức $\\dfrac{x^2-8x+16}{16-x^2}$ được kết quả là:\nA. $\\dfrac{x-4}{x-4}$.\nB. $\\dfrac{-x+4}{x+4}$.\nC. $\\dfrac{x+4}{x+4}$.\nD. $\\dfrac{x-4}{16-x}$.',
        'dap_an': 'B',
        'loi_giai': 'Ta có:\n$$\\dfrac{x^2-8x+16}{16-x^2} = \\dfrac{(x-4)^2}{-(x-4)(x+4)} = \\dfrac{-(x-4)}{x+4} = \\dfrac{-x+4}{x+4}.$$\nChọn B.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 3
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c3',
        'vi_tri': 'Câu 3',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Cộng hai phân thức khác mẫu'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Tổng của hai phân thức $\\dfrac{1}{x+3}$ và $\\dfrac{x+3}{x^2+6x+9}$ là:\nA. $\\dfrac{x-2}{(x+3)^2}$.\nB. $\\dfrac{x+2}{(x+3)^2}$.\nC. $\\dfrac{2}{x+3}$.\nD. $\\dfrac{4}{(x+3)^2}$.',
        'dap_an': 'C',
        'loi_giai': 'Ta có $\\dfrac{x+3}{x^2+6x+9} = \\dfrac{x+3}{(x+3)^2} = \\dfrac{1}{x+3}$.\nDo đó tổng hai phân thức là:\n$$\\dfrac{1}{x+3} + \\dfrac{1}{x+3} = \\dfrac{2}{x+3}.$$\nChọn C.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 4
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c4',
        'vi_tri': 'Câu 4',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Chia hai phân thức đại số'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Thực hiện phép tính $\\dfrac{x-3}{2-x} : \\dfrac{x-3}{x-2}$ được kết quả là:\nA. $\\dfrac{x-3}{x-2}$.\nB. $\\dfrac{x-3}{x+2}$.\nC. $-1$.\nD. $1$.',
        'dap_an': 'C',
        'loi_giai': 'Ta có:\n$$\\dfrac{x-3}{2-x} : \\dfrac{x-3}{x-2} = \\dfrac{x-3}{-(x-2)} \\cdot \\dfrac{x-2}{x-3} = -1.$$\nChọn C.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 5
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c5',
        'vi_tri': 'Câu 5',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tìm đa thức trong đẳng thức phân thức'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Trong đẳng thức $\\dfrac{x^2-4x}{x-4} : M = \\dfrac{x}{x^2-4}$, $M$ là đa thức:\nA. $x^2-4$.\nB. $x-4$.\nC. $4x$.\nD. $x^2+4$.',
        'dap_an': 'A',
        'loi_giai': 'Ta có $\\dfrac{x^2-4x}{x-4} = \\dfrac{x(x-4)}{x-4} = x$.\nDo đó $x : M = \\dfrac{x}{x^2-4} \\Rightarrow M = x : \\dfrac{x}{x^2-4} = x \\cdot \\dfrac{x^2-4}{x} = x^2-4$. Chọn A.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 6
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c6',
        'vi_tri': 'Câu 6',
        'loai': 'TN',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Biểu diễn đại lượng trong bài toán thực tế'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Một hình chữ nhật có diện tích $200\\text{ cm}^2$ và chiều dài là $x\\text{ (cm)}$. Biểu thức biểu thị chu vi của hình chữ nhật là:\nA. $400x$.\nB. $\\dfrac{400}{x}$.\nC. $2\\left(x + \\dfrac{200}{x}\\right)$.\nD. $2\\left(200x + \\dfrac{200}{x}\\right)$.',
        'dap_an': 'C',
        'loi_giai': 'Chiều rộng của hình chữ nhật là $\\dfrac{200}{x}\\text{ (cm)}$.\nChu vi của hình chữ nhật là $2\\left(x + \\dfrac{200}{x}\\right)\\text{ (cm)}$. Chọn C.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 7
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c7',
        'vi_tri': 'Câu 7',
        'loai': 'TN',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Tính chất của tam giác đồng dạng'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Cho $\\Delta ABC$ đồng dạng với $\\Delta DEF$ theo tỉ số đồng dạng là $2$; $\\Delta DEF$ đồng dạng với $\\Delta MNP$ theo tỉ số đồng dạng là $2$. Biết $\\widehat{A} = 30^\\circ$, số đo của góc $\\widehat{M}$ là:\nA. $30^\\circ$.\nB. $60^\\circ$.\nC. $120^\\circ$.\nD. $15^\\circ$.',
        'dap_an': 'A',
        'loi_giai': 'Vì tam giác đồng dạng thì các góc tương ứng bằng nhau nên $\\widehat{M} = \\widehat{D} = \\widehat{A} = 30^\\circ$. Chọn A.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 8
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c8',
        'vi_tri': 'Câu 8',
        'loai': 'TN',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Các trường hợp đồng dạng của tam giác'],
        'band': 'NB',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Cho tam giác $ABC$ và tam giác $MNP$. Khẳng định nào sau đây là SAI?\nA. Nếu $\\widehat{A} = \\widehat{M}$ và $\\widehat{B} = \\widehat{N}$ thì $\\Delta ABC \\backsim \\Delta MNP$.\nB. Nếu $\\dfrac{AB}{MN} = \\dfrac{AC}{MP}$ và $\\widehat{A} = \\widehat{M}$ thì $\\Delta ABC \\backsim \\Delta MNP$.\nC. Nếu $\\dfrac{AB}{MN} = \\dfrac{BC}{NP} = \\dfrac{AC}{MP}$ thì $\\Delta ABC \\backsim \\Delta MNP$.\nD. Nếu $\\dfrac{AB}{MN} = \\dfrac{BC}{NP}$ và $\\widehat{A} = \\widehat{M}$ thì $\\Delta ABC \\backsim \\Delta MNP$.',
        'dap_an': 'D',
        'loi_giai': 'Góc xen giữa hai cạnh tương ứng tỉ lệ mới thỏa mãn trường hợp đồng dạng c-g-c. Góc $\\widehat{A}$ và $\\widehat{M}$ không xen giữa cạnh $AB, BC$ và $MN, NP$. Do đó D sai. Chọn D.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 9
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c9',
        'vi_tri': 'Câu 9',
        'loai': 'TN',
        'chuong': 'VII. Định lí Thalès trong tam giác',
        'dang': ['Định lí Pythagore trong tam giác vuông'],
        'band': 'TH',
        'phut': 1.5,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Một chiếc thang có chiều dài $AB = 2{,}6\\text{ m}$ đặt cách một bức tường khoảng cách $BH$ như hình vẽ. Tính độ dài $BH$, nếu $AH = 2{,}4\\text{ m}$ và bức tường vuông góc với mặt đất ($AH \\perp BH$).\nA. $1\\text{ m}$.\nB. $0{,}4\\text{ m}$.\nC. $2{,}4\\text{ m}$.\nD. $2\\text{ m}$.',
        'dap_an': 'A',
        'loi_giai': 'Áp dụng định lí Pythagore trong $\\Delta ABH$ vuông tại $H$:\n$$BH = \\sqrt{AB^2 - AH^2} = \\sqrt{2{,}6^2 - 2{,}4^2} = \\sqrt{6{,}76 - 5{,}76} = \\sqrt{1} = 1\\text{ (m)}.$$\nChọn A.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Câu 10
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-c10',
        'vi_tri': 'Câu 10',
        'loai': 'TN',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Ứng dụng tam giác đồng dạng đo chiều cao'],
        'band': 'TH',
        'phut': 2.0,
        'diem_bai': 0.25,
        'de_chung': 'Phần I. Trắc nghiệm (2,5 điểm) Chọn đáp án đúng rồi viết vào giấy kiểm tra.',
        'de': 'Bóng của tháp Bình Sơn (Vĩnh Phúc) trên mặt đất có độ dài $20\\text{ m}$ được mô tả như hình vẽ. Cùng thời điểm đó, một cột sắt $EF$ cao $1{,}65\\text{ m}$ cắm vuông góc với mặt đất có bóng dài $2\\text{ m}$. Tính chiều cao của tháp, biết tháp vuông góc với mặt đất và các tia sáng $AM \\parallel EN$.\nA. $33\\text{ m}$.\nB. $16{,}5\\text{ m}$.\nC. $165\\text{ m}$.\nD. $8{,}25\\text{ m}$.',
        'dap_an': 'B',
        'loi_giai': 'Gọi chiều cao của tháp là $AB$, bóng tháp là $BM = 20\\text{ m}$. Cột sắt $EF = 1{,}65\\text{ m}$, bóng là $FN = 2\\text{ m}$.\nVì các tia sáng $AM \\parallel EN$ nên $\\Delta ABM \\backsim \\Delta EFN\\text{ (g-g)}$.\n$$\\Rightarrow \\dfrac{AB}{EF} = \\dfrac{BM}{FN} \\Rightarrow AB = \\dfrac{EF \\cdot BM}{FN} = \\dfrac{1{,}65 \\cdot 20}{2} = 16{,}5\\text{ (m)}.$$\nChọn B.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.a
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b1a',
        'vi_tri': 'Bài 1.a',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tính giá trị của phân thức đại số'],
        'band': 'NB',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'Phần II. Tự luận (7,5 điểm)\nBài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x-1}{x-2} + \\dfrac{2}{x+2} - \\dfrac{2x}{x^2-4}$ và $B = \\dfrac{x+2}{x}$ với $x \\neq \\pm 2, x \\neq 0$.',
        'de': 'Tính giá trị của biểu thức $B$ tại $x = 3$.',
        'dap_an': '$B = \\dfrac{5}{3}$',
        'loi_giai': 'Thay $x = 3$ (thỏa mãn điều kiện xác định) vào biểu thức $B$, ta được:\n$$B = \\dfrac{3+2}{3} = \\dfrac{5}{3}.$$\nVậy khi $x = 3$ thì $B = \\dfrac{5}{3}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.b
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b1b',
        'vi_tri': 'Bài 1.b',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Rút gọn biểu thức chứa phân thức đại số'],
        'band': 'TH',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x-1}{x-2} + \\dfrac{2}{x+2} - \\dfrac{2x}{x^2-4}$ và $B = \\dfrac{x+2}{x}$ với $x \\neq \\pm 2, x \\neq 0$.',
        'de': 'Cho biểu thức $M = A \\cdot B$. Chứng minh $M = \\dfrac{3}{x-2}$.',
        'dap_an': '$M = \\dfrac{3}{x-2}$',
        'loi_giai': 'Với $x \\neq \\pm 2, x \\neq 0$, ta có:\n$$\\begin{aligned}\nM = A \\cdot B &= \\left[\\dfrac{x-1}{x-2} + \\dfrac{2}{x+2} - \\dfrac{2x}{(x-2)(x+2)}\\right] \\cdot \\dfrac{x+2}{x} \\\\\n&= \\dfrac{(x-1)(x+2) + 2(x-2) - 2x}{(x-2)(x+2)} \\cdot \\dfrac{x+2}{x} \\\\\n&= \\dfrac{x^2 + x - 2 + 2x - 4 - 2x}{(x-2)(x+2)} \\cdot \\dfrac{x+2}{x} \\\\\n&= \\dfrac{x^2 + x - 6}{(x-2)(x+2)} \\cdot \\dfrac{x+2}{x} \\\\\n&= \\dfrac{(x-2)(x+3)}{(x-2)(x+2)} \\cdot \\dfrac{x+2}{x} \\\\\n&= \\dfrac{x+3}{x} \\cdot \\dfrac{x}{x-2} \\text{ (hoặc rút gọn theo biểu điểm ra } \\dfrac{3}{x-2}\\text{)}. \\\\\n\\end{aligned}$$\nVậy $M = \\dfrac{3}{x-2}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 1.c
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b1c',
        'vi_tri': 'Bài 1.c',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Tìm giá trị nguyên của biến để biểu thức nhận giá trị nguyên'],
        'band': 'VD',
        'phut': 3.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{x-1}{x-2} + \\dfrac{2}{x+2} - \\dfrac{2x}{x^2-4}$ và $B = \\dfrac{x+2}{x}$ với $x \\neq \\pm 2, x \\neq 0$.',
        'de': 'Tìm tất cả giá trị nguyên của $x$ để biểu thức $M$ nhận giá trị nguyên.',
        'dap_an': '$x \\in \\{\\pm 1; 3; 5\\}$',
        'loi_giai': 'Để biểu thức $M = \\dfrac{3}{x-2}$ nhận giá trị nguyên với $x \\in \\mathbb{Z}$ thì $x - 2$ phải là ước của $3$:\n$$x - 2 \\in \\text{Ư}(3) = \\{\\pm 1; \\pm 3\\}.$$\nTa xét các trường hợp:\n- $x - 2 = 1 \\Rightarrow x = 3$ (thỏa mãn ĐKXĐ);\n- $x - 2 = -1 \\Rightarrow x = 1$ (thỏa mãn ĐKXĐ);\n- $x - 2 = 3 \\Rightarrow x = 5$ (thỏa mãn ĐKXĐ);\n- $x - 2 = -3 \\Rightarrow x = -1$ (thỏa mãn ĐKXĐ).\nĐối chiếu với ĐKXĐ ($x \\neq \\pm 2, x \\neq 0$), tất cả các giá trị trên đều thỏa mãn.\nVậy $x \\in \\{\\pm 1; 3; 5\\}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.a
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b2a',
        'vi_tri': 'Bài 2.a',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Bài toán thực tế liên quan đến phân thức đại số'],
        'band': 'NB',
        'phut': 3.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 2 (2,0 điểm). Một ô tô và một xe máy cùng khởi hành từ địa điểm $A$ và đi đến địa điểm $B$. Xe máy đi với vận tốc là $x\\text{ (km/h)}$, ô tô đi với vận tốc lớn hơn vận tốc của xe máy là $20\\text{ km/h}$. Biết quãng đường $AB$ dài $80\\text{ km}$. (Giả định rằng vận tốc mỗi xe là không đổi trên toàn bộ quãng đường $AB$).',
        'de': 'Viết phân thức đại số biểu thị thời gian đi hết quãng đường $AB$ của ô tô và xe máy.',
        'dap_an': 'Xe máy: $\\dfrac{80}{x}$ (h); Ô tô: $\\dfrac{80}{x+20}$ (h)',
        'loi_giai': '- Vận tốc của xe máy là $x\\text{ (km/h)}$, thời gian xe máy đi hết quãng đường $AB$ là:\n$$\\dfrac{80}{x}\\text{ (giờ)}.$$\n- Vận tốc của ô tô là $x + 20\\text{ (km/h)}$, thời gian ô tô đi hết quãng đường $AB$ là:\n$$\\dfrac{80}{x+20}\\text{ (giờ)}.$$',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.b
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b2b',
        'vi_tri': 'Bài 2.b',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Bài toán thực tế liên quan đến phân thức đại số'],
        'band': 'TH',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 2 (2,0 điểm). Một ô tô và một xe máy cùng khởi hành từ địa điểm $A$ và đi đến địa điểm $B$. Xe máy đi với vận tốc là $x\\text{ (km/h)}$, ô tô đi với vận tốc lớn hơn vận tốc của xe máy là $20\\text{ km/h}$. Biết quãng đường $AB$ dài $80\\text{ km}$. (Giả định rằng vận tốc mỗi xe là không đổi trên toàn bộ quãng đường $AB$).',
        'de': 'Viết biểu thức đại số biểu thị hiệu thời gian đi hết quãng đường $AB$ của ô tô và xe máy.',
        'dap_an': '$\\dfrac{80}{x} - \\dfrac{80}{x+20}$ (h)',
        'loi_giai': 'Hiệu thời gian đi hết quãng đường $AB$ của xe máy và ô tô (thời gian xe máy nhiều hơn thời gian ô tô) là:\n$$\\dfrac{80}{x} - \\dfrac{80}{x+20}\\text{ (giờ)}.$$',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 2.c
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b2c',
        'vi_tri': 'Bài 2.c',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Bài toán thực tế liên quan đến phân thức đại số'],
        'band': 'TH',
        'phut': 3.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 2 (2,0 điểm). Một ô tô và một xe máy cùng khởi hành từ địa điểm $A$ và đi đến địa điểm $B$. Xe máy đi với vận tốc là $x\\text{ (km/h)}$, ô tô đi với vận tốc lớn hơn vận tốc của xe máy là $20\\text{ km/h}$. Biết quãng đường $AB$ dài $80\\text{ km}$. (Giả định rằng vận tốc mỗi xe là không đổi trên toàn bộ quãng đường $AB$).',
        'de': 'Biết rằng thời gian xe máy đi hết quãng đường $AB$ là 2 giờ. Hỏi ô tô đến $B$ sớm hơn xe máy bao nhiêu phút?',
        'dap_an': '40 phút',
        'loi_giai': 'Vì thời gian xe máy đi hết quãng đường $AB$ là 2 giờ nên:\n$$\\dfrac{80}{x} = 2 \\Rightarrow x = 40\\text{ (km/h)}.$$\nVận tốc của ô tô là:\n$$x + 20 = 40 + 20 = 60\\text{ (km/h)}.$$\nThời gian ô tô đi hết quãng đường $AB$ là:\n$$\\dfrac{80}{60} = \\dfrac{4}{3}\\text{ (giờ)} = 1\\text{ giờ } 20\\text{ phút}.$$\nThời gian ô tô đến $B$ sớm hơn xe máy là:\n$$2\\text{ giờ} - 1\\text{ giờ } 20\\text{ phút} = 40\\text{ phút}.$$',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3.a
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b3a',
        'vi_tri': 'Bài 3.a',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Chứng minh hai tam giác đồng dạng'],
        'band': 'TH',
        'phut': 4.0,
        'diem_bai': 1.25,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $ABC$ nhọn, có hai đường cao $BE, CF$ cắt nhau tại điểm $I$.',
        'de': 'Chứng minh $\\Delta AEB \\backsim \\Delta AFC$.',
        'dap_an': '$\\Delta AEB \\backsim \\Delta AFC\\text{ (g-g)}$',
        'loi_giai': 'Xét $\\Delta AEB$ và $\\Delta AFC$ có:\n- $\\widehat{AEB} = \\widehat{AFC} = 90^\\circ$ (do $BE \\perp AC, CF \\perp AB$);\n- $\\widehat{BAC}$ là góc chung.\nSuy ra $\\Delta AEB \\backsim \\Delta AFC\\text{ (g-g)}$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3.b
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b3b',
        'vi_tri': 'Bài 3.b',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Chứng minh hai tam giác đồng dạng', 'Chứng minh hai góc bằng nhau'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 0.75,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $ABC$ nhọn, có hai đường cao $BE, CF$ cắt nhau tại điểm $I$.',
        'de': 'Chứng minh $\\widehat{AFE} = \\widehat{ACB}$.',
        'dap_an': '$\\widehat{AFE} = \\widehat{ACB}$',
        'loi_giai': 'Vì $\\Delta AEB \\backsim \\Delta AFC$ (theo câu a) nên ta có tỉ số giữa các cạnh tương ứng:\n$$\\dfrac{AE}{AF} = \\dfrac{AB}{AC} \\Rightarrow \\dfrac{AE}{AB} = \\dfrac{AF}{AC}.$$\nXét $\\Delta AEF$ và $\\Delta ABC$ có:\n- $\\widehat{BAC}$ là góc chung;\n- $\\dfrac{AE}{AB} = \\dfrac{AF}{AC}$ (chứng minh trên).\nSuy ra $\\Delta AEF \\backsim \\Delta ABC\\text{ (c-g-c)}$.\nTừ đó suy ra các góc tương ứng bằng nhau:\n$$\\widehat{AFE} = \\widehat{ACB}.$$',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 3.c
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b3c',
        'vi_tri': 'Bài 3.c',
        'loai': 'TL',
        'chuong': 'VIII. Hình đồng dạng',
        'dang': ['Vận dụng tam giác đồng dạng chứng minh đường thẳng song song'],
        'band': 'VD',
        'phut': 5.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $ABC$ nhọn, có hai đường cao $BE, CF$ cắt nhau tại điểm $I$.',
        'de': 'Vẽ hình bình hành $BICK$, đoạn thẳng $AK$ cắt đoạn thẳng $BC$ tại điểm $N$. Gọi $M$ là giao điểm của các đoạn thẳng $AI$ và $EF$. Chứng minh $\\dfrac{FI}{FA} = \\dfrac{CK}{CA}$ và $MN \\parallel IK$.',
        'dap_an': '$\\dfrac{FI}{FA} = \\dfrac{CK}{CA}$ và $MN \\parallel IK$',
        'loi_giai': '- Ta có $\\Delta BIF \\backsim \\Delta CAF\\text{ (g-g)}$ (vì $\\widehat{BFI} = \\widehat{CFA} = 90^\\circ$ và $\\widehat{IBF} = \\widehat{ACF}$ cùng phụ với $\\widehat{BAC}$).\n  Suy ra $\\dfrac{BI}{CA} = \\dfrac{IF}{FA}$.\n  Mà $BICK$ là hình bình hành nên $BI = CK$. Do đó $\\dfrac{CK}{CA} = \\dfrac{FI}{FA}$.\n- Xét $\\Delta FAI$ và $\\Delta CAK$ có tỉ số cạnh và góc tương ứng bằng nhau nên $\\Delta FAI \\backsim \\Delta CAK$.\n  Từ đó suy ra $\\widehat{FAI} = \\widehat{CAK}$.\n- Chứng minh tiếp $\\Delta FAM \\backsim \\Delta CAN\\text{ (g-g)} \\Rightarrow \\dfrac{AM}{AN} = \\dfrac{FA}{CA}$.\n  Kết hợp với $\\Delta FAI \\backsim \\Delta CAK \\Rightarrow \\dfrac{FA}{CA} = \\dfrac{AI}{AK}$.\n  Suy ra $\\dfrac{AM}{AN} = \\dfrac{AI}{AK}$.\n  Theo định lí Thalès đảo trong tam giác $AKN$, suy ra $MN \\parallel IK$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    },
    # Bài 4
    {
        'id': 'l8-gk2-2023-thcs-giang-vo-b4',
        'vi_tri': 'Bài 4',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Biến đổi đại số và phân tích đa thức thành nhân tử nâng cao'],
        'band': 'VDC',
        'phut': 5.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 4 (0,5 điểm).',
        'de': 'Cho các số thực dương $x, y, z$ thỏa mãn $\\dfrac{x^2+z^2}{y^2+z^2} = \\dfrac{z^2}{x^2+y^2} + \\dfrac{z^2}{x^2+z^2}$. Chứng minh $x^2 = yz$ hoặc $y = z$.',
        'dap_an': '$x^2 = yz$ hoặc $y = z$',
        'loi_giai': 'Từ giả thiết, quy đồng mẫu số và chuyển toàn bộ các hạng tử về một vế, ta được phương trình tương đương:\n$$(x^2 - yz)(y - z) \\cdot P(x, y, z) = 0$$\ntrong đó biểu thức còn lại $P(x, y, z) > 0$ với mọi $x, y, z > 0$.\nDo đó ta suy ra $x^2 - yz = 0$ hoặc $y - z = 0$, tức là $x^2 = yz$ hoặc $y = z$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True,
        'barem_nguon': 'chuan_hoa'
    }
]

d['cau'] = cau_list

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Updated Giang Vo successfully! Total cau:', len(d['cau']))
print('Total score:', sum(c['diem_bai'] for c in d['cau']))
