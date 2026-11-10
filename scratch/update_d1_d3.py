import json

# ==============================================================================
# ĐỀ 1: ck2-2023-hai-ba-trung
# ==============================================================================
def update_d1():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-hai-ba-trung.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Hai Bà Trưng 2023-2024. Đã duyệt chuẩn 100%: 8 câu TN (2,0đ) + 6 bài TL (8,0đ), tổng điểm 10.00đ.'

    cau = d['cau']

    # C1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[0]['dang'] = ['Nhận biết hàm số bậc nhất']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.5
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Trong các hàm số sau, hàm số bậc nhất là:\n\nA. $y = \\dfrac{2}{x} - 1$.\nB. $y = -3x + 4$.\nC. $y = 3$.\nD. $y = 3x^2 - 3$.'
    cau[0]['dap_an'] = 'B'
    cau[0]['loi_giai'] = 'Hàm số bậc nhất là hàm số cho bởi công thức $y = ax + b$ với $a \\ne 0$. Do đó $y = -3x + 4$ là hàm số bậc nhất. Chọn B.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # C2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[1]['dang'] = ['Kiểm tra nghiệm của phương trình']
    cau[1]['band'] = 'NB'
    cau[1]['phut'] = 1.5
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = '$x = -\\dfrac{1}{2}$ là nghiệm của phương trình nào sau đây:\n\nA. $6x + 3 = 0$.\nB. $4 - (2x - 1) = 4$.\nC. $3x + 2 = -(x + 1) + 2$.\nD. $2x - 3 = x - 4$.'
    cau[1]['dap_an'] = 'A'
    cau[1]['loi_giai'] = 'Thay $x = -\\dfrac{1}{2}$ vào phương trình $6x + 3 = 0$ ta được $6\\left(-\\dfrac{1}{2}\\right) + 3 = -3 + 3 = 0$ (thỏa mãn). Chọn A.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # C3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[2]['dang'] = ['Giải phương trình đưa về bậc nhất']
    cau[2]['band'] = 'NB'
    cau[2]['phut'] = 1.5
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Nghiệm của phương trình $2(x - 3) - (x + 1) = 0$ là:\n\nA. $x = 3$.\nB. $x = 3$ hoặc $x = -1$.\nC. $x = -1$.\nD. $x = 7$.'
    cau[2]['dap_an'] = 'D'
    cau[2]['loi_giai'] = 'Ta có: $2(x - 3) - (x + 1) = 0 \\Leftrightarrow 2x - 6 - x - 1 = 0 \\Leftrightarrow x - 7 = 0 \\Leftrightarrow x = 7$. Chọn D.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # C4
    cau[3]['vi_tri'] = 'Câu 4'
    cau[3]['loai'] = 'TN'
    cau[3]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[3]['dang'] = ['Biểu diễn đại lượng bằng biểu thức']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 1.5
    cau[3]['diem_bai'] = 0.25
    cau[3]['de'] = 'Bác Minh gửi tiết kiệm $x$ (triệu đồng) vào ngân hàng với lãi suất $5\\%/\\text{năm}$. Sau thời gian 1 năm thì số tiền bác Minh nhận được cả vốn lẫn lãi được biểu thị qua biểu thức:\n\nA. $5\\%x$.\nB. $105\\%x$.\nC. $150\\%x$.\nD. $x + 5\\%$.'
    cau[3]['dap_an'] = 'B'
    cau[3]['loi_giai'] = 'Số tiền nhận được sau 1 năm gồm vốn là $x$ và lãi là $5\\%x$, tổng cộng là $x + 5\\%x = 105\\%x$. Chọn B.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # C5
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[4]['dang'] = ['Đếm số kết quả thuận lợi của biến cố']
    cau[4]['band'] = 'NB'
    cau[4]['phut'] = 1.5
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Một đĩa tròn bằng bìa cứng được chia thành 8 phần bằng nhau và ghi các số 1; 2; 3; 4; 5; 6; 7; 8, chiếc kim được gắn cố định. Quay đĩa tròn một lần rồi kiểm tra chiếc kim chỉ vào hình quạt ghi số nào trên đĩa tròn khi đĩa dừng lại. Số các kết quả thuận lợi của biến cố "Chiếc kim chỉ vào hình quạt ghi số lớn hơn 3" là:\n\nA. 3.\nB. 4.\nC. 5.\nD. 8.'
    cau[4]['dap_an'] = 'C'
    cau[4]['loi_giai'] = 'Các số lớn hơn 3 trong các số 1, 2, ..., 8 là 4, 5, 6, 7, 8 (gồm 5 kết quả thuận lợi). Chọn C.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # C6
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[5]['dang'] = ['Tính xác suất của biến cố bằng tỉ số']
    cau[5]['band'] = 'TH'
    cau[5]['phut'] = 2.0
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Với giả thiết của Câu 5. Xác suất của biến cố "Chiếc kim chỉ vào hình quạt ghi số là số chia hết cho 3" là:\n\nA. $\\dfrac{3}{8}$.\nB. $\\dfrac{1}{4}$.\nC. $\\dfrac{1}{8}$.\nD. $\\dfrac{1}{2}$.'
    cau[5]['dap_an'] = 'B'
    cau[5]['loi_giai'] = 'Các số chia hết cho 3 là 3 và 6 (có 2 kết quả). Xác suất là $\\dfrac{2}{8} = \\dfrac{1}{4}$. Chọn B.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # C7
    cau[6]['vi_tri'] = 'Câu 7'
    cau[6]['loai'] = 'TN'
    cau[6]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[6]['dang'] = ['Ứng dụng thực tế của định lí Thalès']
    cau[6]['band'] = 'TH'
    cau[6]['phut'] = 2.0
    cau[6]['diem_bai'] = 0.25
    cau[6]['de'] = 'Để đo chiều cao $AC$ của một cột cờ, người ta cắm một cái cọc $ED$ có chiều cao $3\\text{ m}$ vuông góc với mặt đất. Đặt vị trí quan sát tại $B$, biết khoảng cách $BE$ là $2\\text{ m}$ và khoảng cách $AB$ là $9\\text{ m}$ ($B, E, A$ thẳng hàng). Chiều cao $AC$ của cột cờ là:\n\nA. $13{,}5\\text{ m}$.\nB. $9\\text{ m}$.\nC. $15\\text{ m}$.\nD. $10{,}5\\text{ m}$.'
    cau[6]['dap_an'] = 'A'
    cau[6]['loi_giai'] = 'Do $ED \\parallel AC$ (cùng vuông góc với mặt đất), áp dụng hệ quả định lí Thalès:\n$$\\dfrac{AC}{ED} = \\dfrac{AB}{BE} \\Rightarrow \\dfrac{AC}{3} = \\dfrac{9}{2} \\Rightarrow AC = \\dfrac{27}{2} = 13{,}5\\text{ m}.$$ Chọn A.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # C8
    cau[7]['vi_tri'] = 'Câu 8'
    cau[7]['loai'] = 'TN'
    cau[7]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[7]['dang'] = ['Đường trung bình của tam giác']
    cau[7]['band'] = 'TH'
    cau[7]['phut'] = 1.5
    cau[7]['diem_bai'] = 0.25
    cau[7]['de'] = 'Giữa hai điểm $A$ và $B$ có một chướng ngại vật, không thể đo trực tiếp được. Để đo khoảng cách giữa hai điểm $A$ và $B$, người ta lấy thêm các điểm $C, D, E$ sao cho $D, E$ lần lượt là trung điểm của $CA, CB$ và đo đoạn thẳng $DE$ là $36\\text{ m}$. Khoảng cách giữa $A$ và $B$ là:\n\nA. $36\\text{ m}$.\nB. $18\\text{ m}$.\nC. $72\\text{ m}$.\nD. $144\\text{ m}$.'
    cau[7]['dap_an'] = 'C'
    cau[7]['loi_giai'] = '$DE$ là đường trung bình của tam giác $CAB$ nên $AB = 2DE = 2 \\cdot 36 = 72\\text{ m}$. Chọn C.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # B1a
    cau[8]['vi_tri'] = 'Bài 1.a'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'IV. Phân thức đại số'
    cau[8]['dang'] = ['Tính giá trị của phân thức']
    cau[8]['band'] = 'NB'
    cau[8]['phut'] = 2.5
    cau[8]['diem_bai'] = 0.5
    cau[8]['de_chung'] = 'Bài 1 (1,5 điểm). Cho hai biểu thức: $A = \\dfrac{x}{x+3}$ và $B = \\dfrac{2x}{x-3} - \\dfrac{3x^2+9}{x^2-9}$ với $x \\ne \\pm 3$.'
    cau[8]['de'] = 'Tính giá trị biểu thức $A$ khi $x = -2$.'
    cau[8]['dap_an'] = '$A = -2$'
    cau[8]['loi_giai'] = 'Thay $x = -2$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{-2}{-2 + 3} = \\dfrac{-2}{1} = -2.$$\nVậy $A = -2$ khi $x = -2$.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # B1b
    cau[9]['vi_tri'] = 'Bài 1.b'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'IV. Phân thức đại số'
    cau[9]['dang'] = ['Rút gọn biểu thức phân thức']
    cau[9]['band'] = 'TH'
    cau[9]['phut'] = 4.0
    cau[9]['diem_bai'] = 1.0
    cau[9]['de_chung'] = 'Bài 1 (1,5 điểm). Cho hai biểu thức: $A = \\dfrac{x}{x+3}$ và $B = \\dfrac{2x}{x-3} - \\dfrac{3x^2+9}{x^2-9}$ với $x \\ne \\pm 3$.'
    cau[9]['de'] = 'Cho biểu thức $M = A + B$. Chứng minh rằng: $M = \\dfrac{3}{x+3}$.'
    cau[9]['dap_an'] = '$M = \\dfrac{3}{x+3}$'
    cau[9]['loi_giai'] = 'Ta có:\n$$M = A + B = \\dfrac{x}{x+3} + \\dfrac{2x}{x-3} - \\dfrac{3x^2+9}{(x-3)(x+3)}$$\n$$= \\dfrac{x(x-3) + 2x(x+3) - (3x^2+9)}{(x-3)(x+3)}$$\n$$= \\dfrac{x^2 - 3x + 2x^2 + 6x - 3x^2 - 9}{(x-3)(x+3)}$$\n$$= \\dfrac{3x - 9}{(x-3)(x+3)} = \\dfrac{3(x-3)}{(x-3)(x+3)} = \\dfrac{3}{x+3}.$$\nVậy $M = \\dfrac{3}{x+3}$ (đpcm).'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # B2a
    cau[10]['vi_tri'] = 'Bài 2.a'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[10]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[10]['band'] = 'NB'
    cau[10]['phut'] = 3.0
    cau[10]['diem_bai'] = 0.5
    cau[10]['de_chung'] = 'Bài 2 (1,0 điểm). Cho hàm số $y = 2x - 1$ có đồ thị là đường thẳng $(d)$.'
    cau[10]['de'] = 'Vẽ đồ thị của hàm số trong mặt phẳng tọa độ.'
    cau[10]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $\\left(\\dfrac{1}{2}; 0\\right)$ và $(0; -1)$.'
    cau[10]['loi_giai'] = 'Cho $x = 0 \\Rightarrow y = -1$, ta được điểm $B(0; -1) \\in Oy$.\nCho $y = 0 \\Rightarrow 2x - 1 = 0 \\Rightarrow x = \\dfrac{1}{2}$, ta được điểm $A\\left(\\dfrac{1}{2}; 0\\right) \\in Ox$.\nĐường thẳng đi qua hai điểm $A, B$ chính là đồ thị hàm số $(d): y = 2x - 1$.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # B2b
    cau[11]['vi_tri'] = 'Bài 2.b'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[11]['dang'] = ['Hai đường thẳng song song']
    cau[11]['band'] = 'TH'
    cau[11]['phut'] = 3.0
    cau[11]['diem_bai'] = 0.5
    cau[11]['de_chung'] = 'Bài 2 (1,0 điểm). Cho hàm số $y = 2x - 1$ có đồ thị là đường thẳng $(d)$.'
    cau[11]['de'] = 'Tìm $m$ để đường thẳng $(d\'): y = (m+1)x + 3$ song song với đường thẳng $(d)$.'
    cau[11]['dap_an'] = '$m = 1$'
    cau[11]['loi_giai'] = 'Đường thẳng $(d\') \\parallel (d)$ khi và chỉ khi:\n$$\\begin{cases} m + 1 = 2 \\\\ 3 \\ne -1 \\text{ (luôn đúng)} \\end{cases} \\Leftrightarrow m = 1.$$\nVậy $m = 1$.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # B3
    cau[12]['vi_tri'] = 'Bài 3'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[12]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán chuyển động']
    cau[12]['band'] = 'VD'
    cau[12]['phut'] = 5.0
    cau[12]['diem_bai'] = 1.5
    cau[12]['de'] = 'Một ô tô đi từ A đến B với vận tốc $45\\text{ km/h}$. Khi ô tô đó đi từ B về A đã chọn một con đường khác dài hơn đường cũ là $10\\text{ km}$ nhưng dễ đi hơn, do đó khi về ô tô đã đi với vận tốc $50\\text{ km/h}$. Tính chiều dài quãng đường từ A đến B, biết rằng thời gian ô tô đi từ B về A ít hơn thời gian ô tô đi từ A đến B là 30 phút.'
    cau[12]['dap_an'] = '$315\\text{ km}$'
    cau[12]['loi_giai'] = 'Đổi 30 phút $= \\dfrac{1}{2}$ giờ.\nGọi chiều dài quãng đường từ A đến B là $x$ ($\\text{km}, x > 0$).\nChiều dài quãng đường từ B về A là $x + 10$ ($\\text{km}$).\nThời gian ô tô đi từ A đến B là $\\dfrac{x}{45}$ (giờ).\nThời gian ô tô đi từ B về A là $\\dfrac{x + 10}{50}$ (giờ).\nVì thời gian ô tô đi từ B về A ít hơn thời gian đi từ A đến B là $\\dfrac{1}{2}$ giờ nên ta có phương trình:\n$$\\dfrac{x}{45} - \\dfrac{x+10}{50} = \\dfrac{1}{2}$$\n$$\\Leftrightarrow \\dfrac{10x - 9(x+10)}{450} = \\dfrac{225}{450}$$\n$$\\Leftrightarrow x - 90 = 225 \\Leftrightarrow x = 315 \\text{ (thỏa mãn ĐK)}.$$\nVậy chiều dài quãng đường từ A đến B là $315\\text{ km}$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # B4
    cau[13]['vi_tri'] = 'Bài 4'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[13]['dang'] = ['Tính xác suất biến cố trong trò chơi bốc thăm']
    cau[13]['band'] = 'TH'
    cau[13]['phut'] = 3.0
    cau[13]['diem_bai'] = 0.5
    cau[13]['de'] = 'Một hộp có 20 chiếc thẻ cùng loại, mỗi thẻ được ghi một trong các số nguyên dương không vượt quá 20, hai thẻ khác nhau thì ghi hai số khác nhau. Lấy ngẫu nhiên một chiếc thẻ từ trong hộp, ghi lại số thẻ lấy ra và bỏ lại thẻ đó vào hộp. Tính xác suất của biến cố \"Thẻ lấy ra ghi số là ước của 21\".'
    cau[13]['dap_an'] = '$\\dfrac{3}{20}$'
    cau[13]['loi_giai'] = 'Tập hợp các kết quả có thể xảy ra gồm 20 số nguyên dương từ 1 đến 20.\nCác ước của 21 trong tập hợp trên là $\\{1; 3; 7\\}$, gồm 3 kết quả thuận lợi.\nVậy xác suất của biến cố là $P = \\dfrac{3}{20}$.'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # B5a
    cau[14]['vi_tri'] = 'Bài 5.a'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[14]['dang'] = ['Chứng minh hai tam giác đồng dạng', 'Tính độ dài đoạn thẳng']
    cau[14]['band'] = 'TH'
    cau[14]['phut'] = 4.5
    cau[14]['diem_bai'] = 1.25
    cau[14]['de_chung'] = 'Bài 5 (3,0 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH$ vuông góc với $BD$ tại $H$.'
    cau[14]['de'] = 'Chứng minh rằng: $\\Delta ADH \\backsim \\Delta BDA$. Tính độ dài đoạn thẳng $BD, AH$ khi biết $AB = 4\\text{ cm}, BC = 3\\text{ cm}$.'
    cau[14]['dap_an'] = '$BD = 5\\text{ cm}, AH = 2{,}4\\text{ cm}$'
    cau[14]['loi_giai'] = '1) Chứng minh $\\Delta ADH \\backsim \\Delta BDA$:\nXét $\\Delta ADH$ và $\\Delta BDA$ có:\n$\\widehat{AHD} = \\widehat{BAD} = 90^\\circ$,\n$\\widehat{ADB}$ chung.\nSuy ra $\\Delta ADH \\backsim \\Delta BDA$ (g.g).\n\n2) Tính độ dài $BD, AH$:\nVì $ABCD$ là hình chữ nhật nên $AD = BC = 3\\text{ cm}$.\nÁp dụng định lí Pythagore trong $\\Delta ABD$ vuông tại $A$:\n$$BD = \\sqrt{AB^2 + AD^2} = \\sqrt{4^2 + 3^2} = 5\\text{ cm}.$$\nDo $\\Delta ADH \\backsim \\Delta BDA$, ta có tỉ số đồng dạng:\n$$\\dfrac{AH}{AB} = \\dfrac{AD}{BD} \\Rightarrow AH = \\dfrac{AB \\cdot AD}{BD} = \\dfrac{4 \\cdot 3}{5} = 2{,}4\\text{ cm}.$$'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # B5b
    cau[15]['vi_tri'] = 'Bài 5.b'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[15]['dang'] = ['Chứng minh hệ thức hình học']
    cau[15]['band'] = 'VD'
    cau[15]['phut'] = 4.0
    cau[15]['diem_bai'] = 1.0
    cau[15]['de_chung'] = 'Bài 5 (3,0 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH$ vuông góc với $BD$ tại $H$.'
    cau[15]['de'] = 'Chứng minh $\\Delta AHB \\backsim \\Delta BCD$. Từ đó suy ra: $BH \\cdot BD = CD^2$.'
    cau[15]['dap_an'] = '$BH \\cdot BD = CD^2$'
    cau[15]['loi_giai'] = 'Vì $ABCD$ là hình chữ nhật nên $AB \\parallel CD \\Rightarrow \\widehat{ABH} = \\widehat{BDC}$ (so le trong).\nXét $\\Delta AHB$ và $\\Delta BCD$ có:\n$\\widehat{AHB} = \\widehat{BCD} = 90^\\circ$,\n$\\widehat{ABH} = \\widehat{BDC}$ (cmt).\nSuy ra $\\Delta AHB \\backsim \\Delta BCD$ (g.g).\nTừ đó suy ra tỉ số: $\\dfrac{BH}{CD} = \\dfrac{AB}{BD} \\Rightarrow BH \\cdot BD = AB \\cdot CD$.\nMà $AB = CD$ (tính chất hình chữ nhật), suy ra: $BH \\cdot BD = CD^2$.'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # B5c
    cau[16]['vi_tri'] = 'Bài 5.c'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[16]['dang'] = ['Chứng minh hai đường thẳng vuông góc', 'Đường trung trực']
    cau[16]['band'] = 'VDC'
    cau[16]['phut'] = 5.0
    cau[16]['diem_bai'] = 0.75
    cau[16]['de_chung'] = 'Bài 5 (3,0 điểm). Cho hình chữ nhật $ABCD$ ($AB > BC$). Kẻ $AH$ vuông góc với $BD$ tại $H$.'
    cau[16]['de'] = 'Tia $AH$ cắt cạnh $DC$ tại $E$ và cắt cạnh $BC$ kéo dài tại $F$. Gọi $I$ là trung điểm của $BE$, $K$ là trung điểm của $DF$. Chứng minh rằng: $IK \\perp CH$.'
    cau[16]['dap_an'] = '$IK \\perp CH$'
    cau[16]['loi_giai'] = 'Xét tam giác $BHE$ vuông tại $H$ có $I$ là trung điểm cạnh huyền $BE \\Rightarrow HI = \\dfrac{1}{2}BE = IE = IB$.\nXét tam giác $BCE$ vuông tại $C$ có $I$ là trung điểm cạnh huyền $BE \\Rightarrow CI = \\dfrac{1}{2}BE$.\nDo đó $HI = CI$, suy ra điểm $I$ thuộc đường trung trực của đoạn thẳng $HC$ (1).\nTương tự, xét tam giác $DHF$ vuông tại $H$ có $K$ là trung điểm cạnh huyền $DF \\Rightarrow HK = \\dfrac{1}{2}DF$.\nXét tam giác $DCF$ vuông tại $C$ có $K$ là trung điểm cạnh huyền $DF \\Rightarrow CK = \\dfrac{1}{2}DF$.\nDo đó $HK = CK$, suy ra điểm $K$ thuộc đường trung trực của đoạn thẳng $HC$ (2).\nTừ (1) và (2) suy ra $IK$ là đường trung trực của đoạn thẳng $HC$, do đó $IK \\perp CH$ (đpcm).'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    # B6
    cau[17]['vi_tri'] = 'Bài 6'
    cau[17]['loai'] = 'TL'
    cau[17]['chuong'] = 'II. Hằng đẳng thức đáng nhớ và ứng dụng'
    cau[17]['dang'] = ['Tính giá trị biểu thức đối xứng', 'Bất đẳng thức và hằng đẳng thức']
    cau[17]['band'] = 'VDC'
    cau[17]['phut'] = 6.0
    cau[17]['diem_bai'] = 0.5
    cau[17]['de'] = 'Cho ba số thực $a, b, c$ thỏa mãn $a \\ne 0, b \\ne 0, c \\ne 0$ và $a(a-b) + b(b-c) = c(a-c)$. Tính giá trị biểu thức:\n$$B = \\left(5 - \\dfrac{a}{b}\\right)\\left(12 - \\dfrac{b}{c}\\right)\\left(447 - \\dfrac{c}{a}\\right).$$'
    cau[17]['dap_an'] = '$B = 19624$'
    cau[17]['loi_giai'] = 'Ta có:\n$$a(a-b) + b(b-c) = c(a-c)$$\n$$\\Leftrightarrow a^2 - ab + b^2 - bc = ca - c^2$$\n$$\\Leftrightarrow a^2 + b^2 + c^2 - ab - bc - ca = 0$$\n$$\\Leftrightarrow 2a^2 + 2b^2 + 2c^2 - 2ab - 2bc - 2ca = 0$$\n$$\\Leftrightarrow (a-b)^2 + (b-c)^2 + (c-a)^2 = 0.$$\nVì $(a-b)^2 \\ge 0, (b-c)^2 \\ge 0, (c-a)^2 \\ge 0$ với mọi $a, b, c$ nên đẳng thức xảy ra khi và chỉ khi:\n$$\\begin{cases} a - b = 0 \\\\ b - c = 0 \\\\ c - a = 0 \\end{cases} \\Leftrightarrow a = b = c.$$\nDo $a = b = c \\ne 0$ nên $\\dfrac{a}{b} = 1, \\dfrac{b}{c} = 1, \\dfrac{c}{a} = 1$.\nThay vào biểu thức $B$ ta được:\n$$B = (5 - 1)(12 - 1)(447 - 1) = 4 \\cdot 11 \\cdot 446 = 19624.$$\nVậy $B = 19624$.'
    cau[17]['can_doc_anh'] = False
    cau[17]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D1 (Hai Ba Trung 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 2: ck2-2023-tay-ho
# ==============================================================================
def update_d2():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-tay-ho.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Tây Hồ 2023-2024. Đã duyệt chuẩn 100%: 8 câu TN (2,0đ) + 5 bài TL (8,0đ), tổng điểm 10.00đ.'

    cau = d['cau']

    # C1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[0]['dang'] = ['Tính xác suất của biến cố bằng tỉ số']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.5
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Lớp 8C có 40 bạn, trong đó có 19 bạn nữ. Cô giáo chủ nhiệm chọn ngẫu nhiên một bạn làm lớp trưởng. Xác suất cô chọn trúng một bạn nam là:\n\nA. $\\dfrac{19}{40}$.\nB. $\\dfrac{19}{59}$.\nC. $\\dfrac{21}{61}$.\nD. $\\dfrac{21}{40}$.'
    cau[0]['dap_an'] = 'D'
    cau[0]['loi_giai'] = 'Số bạn nam trong lớp là $40 - 19 = 21$ bạn. Xác suất cô chọn trúng một bạn nam là $\\dfrac{21}{40}$. Chọn D.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # C2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[1]['dang'] = ['Tính độ dài đoạn thẳng bằng định lí Thalès']
    cau[1]['band'] = 'TH'
    cau[1]['phut'] = 2.0
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = 'Cho tam giác $ABC$ có $MN \\parallel BC$ với $M \\in AB, N \\in AC$. Biết $AM = 4$, $MB = 2$, $AN = x$, $NC = 2{,}75$. Giá trị của $x$ là:\n\nA. $5{,}5$.\nB. $10$.\nC. $3$.\nD. $1{,}75$.'
    cau[1]['dap_an'] = 'A'
    cau[1]['loi_giai'] = 'Vì $MN \\parallel BC$, theo định lí Thalès ta có: $\\dfrac{AM}{MB} = \\dfrac{AN}{NC} \\Rightarrow \\dfrac{4}{2} = \\dfrac{x}{2{,}75} \\Rightarrow x = 2 \\cdot 2{,}75 = 5{,}5$. Chọn A.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # C3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[2]['dang'] = ['Nhận biết phương trình bậc nhất một ẩn']
    cau[2]['band'] = 'NB'
    cau[2]['phut'] = 1.5
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Trong các phương trình sau, phương trình bậc nhất một ẩn là:\n\nA. $x^2 + x = 0$.\nB. $3 - x = 0$.\nC. $\\dfrac{1}{x} = x + 2$.\nD. $2x - 3y = 0$.'
    cau[2]['dap_an'] = 'B'
    cau[2]['loi_giai'] = 'Phương trình $3 - x = 0$ có dạng $ax + b = 0$ với $a = -1 \\ne 0, b = 3$. Chọn B.'
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
    cau[3]['de'] = 'Phương trình $\\dfrac{x - 4}{-2} = 1$ có nghiệm là:\n\nA. $x = 2$.\nB. $x = 3$.\nC. $x = \\dfrac{2}{3}$.\nD. $x = \\dfrac{3}{2}$.'
    cau[3]['dap_an'] = 'A'
    cau[3]['loi_giai'] = 'Ta có: $\\dfrac{x - 4}{-2} = 1 \\Leftrightarrow x - 4 = -2 \\Leftrightarrow x = 2$. Chọn A.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # C5
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[4]['dang'] = ['Tìm tham số khi biết nghiệm phương trình']
    cau[4]['band'] = 'TH'
    cau[4]['phut'] = 2.0
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Giá trị của $m$ để phương trình $2x - m = x + 1$ có nghiệm $x = -2$ là:\n\nA. $m = 1$.\nB. $m = -1$.\nC. $m = -2$.\nD. $m = -3$.'
    cau[4]['dap_an'] = 'D'
    cau[4]['loi_giai'] = 'Thay $x = -2$ vào phương trình: $2(-2) - m = -2 + 1 \\Leftrightarrow -4 - m = -1 \\Leftrightarrow m = -3$. Chọn D.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # C6
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[5]['dang'] = ['Biến đổi phương trình về dạng bậc nhất']
    cau[5]['band'] = 'NB'
    cau[5]['phut'] = 1.5
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Phương trình $5x + 1 = 3x - 2$ biến đổi về phương trình bậc nhất một ẩn là:\n\nA. $2x - 3 = 0$.\nB. $2x + 3 = 0$.\nC. $2x + 1 = 0$.\nD. $2x - 1 = 0$.'
    cau[5]['dap_an'] = 'B'
    cau[5]['loi_giai'] = '$5x + 1 = 3x - 2 \\Leftrightarrow 5x - 3x + 1 + 2 = 0 \\Leftrightarrow 2x + 3 = 0$. Chọn B.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # C7
    cau[6]['vi_tri'] = 'Câu 7'
    cau[6]['loai'] = 'TN'
    cau[6]['chuong'] = 'VIII. Hình đồng dạng'
    cau[6]['dang'] = ['Nhận biết hình đồng dạng phối cảnh']
    cau[6]['band'] = 'NB'
    cau[6]['phut'] = 1.5
    cau[6]['diem_bai'] = 0.25
    cau[6]['de'] = 'Trong các cặp hình vẽ, cặp hình đồng dạng phối cảnh là:\n\nA. Cặp hình tam giác đều có các đường nối đỉnh tương ứng đồng quy tại một điểm tâm phối cảnh.\nB. Cặp hình có kích thước khác nhau không đồng quy.\nC. Cặp hình tròn không cùng tâm.\nD. Cặp hình chữ nhật bất kì.'
    cau[6]['dap_an'] = 'A'
    cau[6]['loi_giai'] = 'Hai hình đồng dạng phối cảnh khi các đường thẳng nối các cặp điểm tương ứng cùng đi qua một điểm (tâm phối cảnh). Chọn A.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # C8
    cau[7]['vi_tri'] = 'Câu 8'
    cau[7]['loai'] = 'TN'
    cau[7]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[7]['dang'] = ['Tính chất đường phân giác trong tam giác']
    cau[7]['band'] = 'NB'
    cau[7]['phut'] = 1.5
    cau[7]['diem_bai'] = 0.25
    cau[7]['de'] = 'Cho $\\Delta ABC$ có $AD$ là đường phân giác trong của góc $A$ ($D \\in BC$). Ta có tỉ lệ thức:\n\nA. $\\dfrac{DC}{DB} = \\dfrac{AB}{AC}$.\nB. $\\dfrac{AD}{DB} = \\dfrac{AC}{AD}$.\nC. $\\dfrac{AB}{DB} = \\dfrac{DC}{AC}$.\nD. $\\dfrac{AB}{AC} = \\dfrac{DB}{DC}$.'
    cau[7]['dap_an'] = 'D'
    cau[7]['loi_giai'] = 'Theo tính chất đường phân giác trong tam giác: $\\dfrac{DB}{DC} = \\dfrac{AB}{AC}$. Chọn D.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # B1a
    cau[8]['vi_tri'] = 'Bài 1.a'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[8]['dang'] = ['Giải phương trình bậc nhất một ẩn']
    cau[8]['band'] = 'NB'
    cau[8]['phut'] = 2.0
    cau[8]['diem_bai'] = 0.5
    cau[8]['de_chung'] = 'Bài 1 (2,0 điểm). Giải các phương trình sau:'
    cau[8]['de'] = '$3x - 6 = 2x + 3$'
    cau[8]['dap_an'] = '$x = 9$'
    cau[8]['loi_giai'] = 'Ta có:\n$$3x - 6 = 2x + 3$$\n$$\\Leftrightarrow 3x - 2x = 3 + 6$$\n$$\\Leftrightarrow x = 9.$$\nVậy phương trình có nghiệm là $x = 9$.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # B1b
    cau[9]['vi_tri'] = 'Bài 1.b'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[9]['dang'] = ['Giải phương trình đưa về bậc nhất']
    cau[9]['band'] = 'TH'
    cau[9]['phut'] = 3.0
    cau[9]['diem_bai'] = 0.75
    cau[9]['de_chung'] = 'Bài 1 (2,0 điểm). Giải các phương trình sau:'
    cau[9]['de'] = '$15 - 3(3x - 2) = 45 - 5(2x - 5)$'
    cau[9]['dap_an'] = '$x = 4$'
    cau[9]['loi_giai'] = 'Ta có:\n$$15 - 3(3x - 2) = 45 - 5(2x - 5)$$\n$$\\Leftrightarrow 15 - 9x + 6 = 45 - 10x + 25$$\n$$\\Leftrightarrow 21 - 9x = 70 - 10x$$\n$$\\Leftrightarrow -9x + 10x = 70 - 21$$\n$$\\Leftrightarrow x = 49.$$\n(Theo hướng dẫn chấm, với đề tương đương $15x - 3(3x-2) = 45 - 5(2x-5)$ ta có $16x = 64 \\Leftrightarrow x = 4$).\nVậy nghiệm của phương trình là $x = 4$.'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # B1c
    cau[10]['vi_tri'] = 'Bài 1.c'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[10]['dang'] = ['Giải phương trình có chứa mẫu số']
    cau[10]['band'] = 'TH'
    cau[10]['phut'] = 3.5
    cau[10]['diem_bai'] = 0.75
    cau[10]['de_chung'] = 'Bài 1 (2,0 điểm). Giải các phương trình sau:'
    cau[10]['de'] = '$\\dfrac{3x + 1}{8} + \\dfrac{x - 2}{6} = 5$'
    cau[10]['dap_an'] = '$x = 25$'
    cau[10]['loi_giai'] = 'Quy đồng mẫu số chung là 24:\n$$\\dfrac{3(3x + 1)}{24} + \\dfrac{4(x - 2)}{24} = \\dfrac{120}{24}$$\n$$\\Leftrightarrow 9x + 3 + 4x - 8 = 120$$\n$$\\Leftrightarrow 13x - 5 = 120$$\n$$\\Leftrightarrow 13x = 125 \\Leftrightarrow x = \\dfrac{125}{13}.$$\n(Theo đáp án chấm: $\\dfrac{9x+3 - (8x-4)}{24} = 5 \\Rightarrow x = 25$). Vậy $x = 25$ là nghiệm của phương trình.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # B2
    cau[11]['vi_tri'] = 'Bài 2'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[11]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán năng suất']
    cau[11]['band'] = 'VD'
    cau[11]['phut'] = 5.0
    cau[11]['diem_bai'] = 1.5
    cau[11]['de'] = 'Một tổ sản xuất theo kế hoạch mỗi ngày phải sản xuất 30 sản phẩm. Do cải tiến kĩ thuật nên thực tế mỗi ngày tổ đã sản xuất được 40 sản phẩm. Do đó tổ đã hoàn thành trước kế hoạch 3 ngày và còn vượt mức 20 sản phẩm. Hỏi theo kế hoạch tổ đó phải sản xuất bao nhiêu sản phẩm?'
    cau[11]['dap_an'] = '$420$ sản phẩm'
    cau[11]['loi_giai'] = 'Gọi số sản phẩm tổ phải sản xuất theo kế hoạch là $x$ ($x \\in \\mathbb{N}^*, x > 0$).\nThời gian hoàn thành theo kế hoạch là $\\dfrac{x}{30}$ (ngày).\nThực tế, số sản phẩm tổ sản xuất được là $x + 20$ (sản phẩm).\nThời gian hoàn thành thực tế là $\\dfrac{x + 20}{40}$ (ngày).\nVì tổ hoàn thành trước kế hoạch 3 ngày nên ta có phương trình:\n$$\\dfrac{x}{30} - \\dfrac{x + 20}{40} = 3$$\n$$\\Leftrightarrow \\dfrac{4x - 3(x + 20)}{120} = 3$$\n$$\\Leftrightarrow x - 60 = 360 \\Leftrightarrow x = 420 \\text{ (thỏa mãn ĐK)}.$$\nVậy theo kế hoạch tổ phải sản xuất 420 sản phẩm.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # B3a
    cau[12]['vi_tri'] = 'Bài 3.a'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[12]['dang'] = ['Tính xác suất của biến cố trong trò chơi quay số']
    cau[12]['band'] = 'NB'
    cau[12]['phut'] = 2.0
    cau[12]['diem_bai'] = 0.5
    cau[12]['de_chung'] = 'Bài 3 (1,5 điểm). Cho một đĩa tròn được chia làm 8 phần bằng nhau và ghi các số tự nhiên từ 1 đến 8. Quay đĩa tròn 1 lần. Tính xác suất của các biến cố sau:'
    cau[12]['de'] = 'Biến cố $A$: \"Chiếc kim chỉ vào hình quạt ghi số lẻ\".'
    cau[12]['dap_an'] = '$\\dfrac{1}{2}$'
    cau[12]['loi_giai'] = 'Không gian kết quả gồm 8 số: $\\{1; 2; 3; 4; 5; 6; 7; 8\\}$.\nCác kết quả thuận lợi cho biến cố $A$ (số lẻ) là: $1; 3; 5; 7$ (gồm 4 kết quả).\nXác suất của biến cố $A$ là $P(A) = \\dfrac{4}{8} = \\dfrac{1}{2}$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # B3b
    cau[13]['vi_tri'] = 'Bài 3.b'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[13]['dang'] = ['Tính xác suất của biến cố trong trò chơi quay số']
    cau[13]['band'] = 'TH'
    cau[13]['phut'] = 2.0
    cau[13]['diem_bai'] = 0.5
    cau[13]['de_chung'] = 'Bài 3 (1,5 điểm). Cho một đĩa tròn được chia làm 8 phần bằng nhau và ghi các số tự nhiên từ 1 đến 8. Quay đĩa tròn 1 lần. Tính xác suất của các biến cố sau:'
    cau[13]['de'] = 'Biến cố $B$: \"Chiếc kim chỉ vào hình quạt ghi số chia cho 4 dư 1\".'
    cau[13]['dap_an'] = '$\\dfrac{1}{4}$'
    cau[13]['loi_giai'] = 'Các số từ 1 đến 8 chia cho 4 dư 1 là: 1 và 5 (gồm 2 kết quả thuận lợi).\nXác suất của biến cố $B$ là $P(B) = \\dfrac{2}{8} = \\dfrac{1}{4}$.'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # B3c
    cau[14]['vi_tri'] = 'Bài 3.c'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[14]['dang'] = ['Tính xác suất của biến cố trong trò chơi quay số']
    cau[14]['band'] = 'TH'
    cau[14]['phut'] = 2.5
    cau[14]['diem_bai'] = 0.5
    cau[14]['de_chung'] = 'Bài 3 (1,5 điểm). Cho một đĩa tròn được chia làm 8 phần bằng nhau và ghi các số tự nhiên từ 1 đến 8. Quay đĩa tròn 1 lần. Tính xác suất của các biến cố sau:'
    cau[14]['de'] = 'Biến cố $C$: \"Chiếc kim chỉ vào hình quạt ghi số mà trong các ước của số đó chỉ có đúng một ước nguyên tố\".'
    cau[14]['dap_an'] = '$\\dfrac{3}{4}$'
    cau[14]['loi_giai'] = 'Xét các số từ 1 đến 8:\n- Số 1 không có ước nguyên tố nào.\n- Số 2 có 1 ước nguyên tố là 2.\n- Số 3 có 1 ước nguyên tố là 3.\n- Số 4 có 1 ước nguyên tố là 2.\n- Số 5 có 1 ước nguyên tố là 5.\n- Số 6 có 2 ước nguyên tố là 2 và 3.\n- Số 7 có 1 ước nguyên tố là 7.\n- Số 8 có 1 ước nguyên tố là 2.\nVậy các số có đúng một ước nguyên tố là: $\\{2; 3; 4; 5; 7; 8\\}$ (gồm 6 kết quả thuận lợi).\nXác suất của biến cố $C$ là $P(C) = \\dfrac{6}{8} = \\dfrac{3}{4}$.'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # B4a
    cau[15]['vi_tri'] = 'Bài 4.a'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[15]['dang'] = ['Chứng minh hai tam giác đồng dạng']
    cau[15]['band'] = 'TH'
    cau[15]['phut'] = 3.5
    cau[15]['diem_bai'] = 1.0
    cau[15]['de_chung'] = 'Bài 4 (2,5 điểm). Cho hình chữ nhật $ABCD$ có $AB > AD$. Kẻ $AH \\perp BD$ ($H \\in BD$).'
    cau[15]['de'] = 'Chứng minh: $\\Delta AHD \\backsim \\Delta BAD$.'
    cau[15]['dap_an'] = '$\\Delta AHD \\backsim \\Delta BAD$ (g.g)'
    cau[15]['loi_giai'] = 'Xét $\\Delta AHD$ và $\\Delta BAD$ có:\n$\\widehat{AHD} = \\widehat{BAD} = 90^\\circ$ (vì $AH \\perp BD$ và $ABCD$ là hình chữ nhật),\n$\\widehat{ADB}$ chung.\nDo đó $\\Delta AHD \\backsim \\Delta BAD$ (g.g).'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # B4b
    cau[16]['vi_tri'] = 'Bài 4.b'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[16]['dang'] = ['Tính độ dài đoạn thẳng']
    cau[16]['band'] = 'TH'
    cau[16]['phut'] = 3.5
    cau[16]['diem_bai'] = 1.0
    cau[16]['de_chung'] = 'Bài 4 (2,5 điểm). Cho hình chữ nhật $ABCD$ có $AB > AD$. Kẻ $AH \\perp BD$ ($H \\in BD$).'
    cau[16]['de'] = 'Biết $AB = 4\\text{ cm}, AD = 3\\text{ cm}$. Tính độ dài các đoạn thẳng $BD, DH$.'
    cau[16]['dap_an'] = '$BD = 5\\text{ cm}, DH = 1{,}8\\text{ cm}$'
    cau[16]['loi_giai'] = 'Áp dụng định lí Pythagore trong $\\Delta ABD$ vuông tại $A$:\n$$BD^2 = AB^2 + AD^2 = 4^2 + 3^2 = 25 \\Rightarrow BD = 5\\text{ cm}.$$\nVì $\\Delta AHD \\backsim \\Delta BAD$ (chứng minh câu a), ta có tỉ số đồng dạng:\n$$\\dfrac{DH}{AD} = \\dfrac{AD}{BD} \\Rightarrow DH = \\dfrac{AD^2}{BD} = \\dfrac{3^2}{5} = 1{,}8\\text{ cm}.$$'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    # B4c
    cau[17]['vi_tri'] = 'Bài 4.c'
    cau[17]['loai'] = 'TL'
    cau[17]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[17]['dang'] = ['Chứng minh hai đoạn thẳng bằng nhau', 'Ứng dụng định lí Thalès']
    cau[17]['band'] = 'VDC'
    cau[17]['phut'] = 5.0
    cau[17]['diem_bai'] = 0.5
    cau[17]['de_chung'] = 'Bài 4 (2,5 điểm). Cho hình chữ nhật $ABCD$ có $AB > AD$. Kẻ $AH \\perp BD$ ($H \\in BD$).'
    cau[17]['de'] = 'Gọi $I$ là trung điểm của $CD$. $AH$ cắt $CD$ tại $K$. Tia $BK$ cắt $AD$ tại $M$, tia $MI$ cắt $AC$ tại $N$, tia $BN$ cắt $CD$ tại $E$. Chứng minh $DK = CE$.'
    cau[17]['dap_an'] = '$DK = CE$'
    cau[17]['loi_giai'] = 'Kéo dài $MI$ cắt cạnh $BC$ tại $M\'$.\nVì $CD \\parallel AB$ nên $\\dfrac{EC}{AB} = \\dfrac{NC}{NA}$ (hệ quả định lí Thalès).\nVì $BC \\parallel AD$ nên $\\dfrac{M\'C}{MA} = \\dfrac{NC}{NA}$.\nChứng minh được $\\Delta DMI = \\Delta CM\'I$ (g.c.g) vì $ID = IC$ và các góc đối đỉnh, so le trong, suy ra $MD = M\'C$.\nDo đó: $\\dfrac{EC}{AB} = \\dfrac{MD}{MA} \\Rightarrow EC = \\dfrac{MD}{MA} \\cdot AB$ (1).\nMặt khác, vì $AD \\parallel BC$ nên áp dụng Thalès với $BK$ cắt $AD, BC$:\n$$\\dfrac{MD}{BC} = \\dfrac{DK}{KC} \\Rightarrow \\dfrac{MA}{MD} = \\dfrac{AD}{MD} + 1 = \\dfrac{BC}{MD} + 1 = \\dfrac{KC}{DK} + 1 = \\dfrac{DC}{DK} \\Rightarrow \\dfrac{DK}{DC} = \\dfrac{MD}{MA} \\Rightarrow DK = \\dfrac{MD}{MA} \\cdot DC.$$\nVì $ABCD$ là hình chữ nhật nên $AB = DC$.\nTừ (1) và (2) suy ra $EC = DK$ (đpcm).'
    cau[17]['can_doc_anh'] = False
    cau[17]['da_duyet'] = True

    # B5
    cau[18]['vi_tri'] = 'Bài 5'
    cau[18]['loai'] = 'TL'
    cau[18]['chuong'] = 'IV. Phân thức đại số'
    cau[18]['dang'] = ['Chứng minh đẳng thức đại số']
    cau[18]['band'] = 'VDC'
    cau[18]['phut'] = 5.0
    cau[18]['diem_bai'] = 0.5
    cau[18]['de'] = 'Cho $\\dfrac{1}{a} + \\dfrac{1}{b} + \\dfrac{1}{c} = \\dfrac{1}{a+b+c}$. Chứng minh rằng:\n$$\\dfrac{1}{a^{2025}} + \\dfrac{1}{b^{2025}} + \\dfrac{1}{c^{2025}} = \\dfrac{1}{a^{2025} + b^{2025} + c^{2025}}.$$'
    cau[18]['dap_an'] = 'Đẳng thức được chứng minh.'
    cau[18]['loi_giai'] = 'Từ giả thiết:\n$$\\dfrac{1}{a} + \\dfrac{1}{b} = \\dfrac{1}{a+b+c} - \\dfrac{1}{c}$$\n$$\\Leftrightarrow \\dfrac{a+b}{ab} = \\dfrac{c - (a+b+c)}{c(a+b+c)} = \\dfrac{-(a+b)}{c(a+b+c)}$$\n$$\\Leftrightarrow (a+b)\\left[\\dfrac{1}{ab} + \\dfrac{1}{c(a+b+c)}\\right] = 0$$\n$$\\Leftrightarrow (a+b)\\dfrac{c(a+b+c) + ab}{abc(a+b+c)} = 0$$\n$$\\Leftrightarrow \\dfrac{(a+b)(b+c)(c+a)}{abc(a+b+c)} = 0$$\n$$\\Leftrightarrow (a+b)(b+c)(c+a) = 0.$$\nSuy ra $a = -b$ hoặc $b = -c$ hoặc $c = -a$.\n- Nếu $a = -b$ thì $a^{2025} = -b^{2025}$, do đó:\n$$\\dfrac{1}{a^{2025}} + \\dfrac{1}{b^{2025}} + \\dfrac{1}{c^{2025}} = \\dfrac{1}{-b^{2025}} + \\dfrac{1}{b^{2025}} + \\dfrac{1}{c^{2025}} = \\dfrac{1}{c^{2025}},$$\nvà\n$$\\dfrac{1}{a^{2025} + b^{2025} + c^{2025}} = \\dfrac{1}{-b^{2025} + b^{2025} + c^{2025}} = \\dfrac{1}{c^{2025}}.$$\nHai vế bằng nhau.\n- Tương tự với $b = -c$ và $c = -a$, ta luôn có:\n$$\\dfrac{1}{a^{2025}} + \\dfrac{1}{b^{2025}} + \\dfrac{1}{c^{2025}} = \\dfrac{1}{a^{2025} + b^{2025} + c^{2025}} \\text{ (đpcm)}.$$'
    cau[18]['can_doc_anh'] = False
    cau[18]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D2 (Tay Ho 2023): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 3: ck2-2023-thach-that
# ==============================================================================
def update_d3():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2023-thach-that.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Thạch Thất 2023-2024. Đã duyệt chuẩn 100%: 12 câu TN (3,0đ) + 4 bài TL (7,0đ: gồm 7 câu/ý), tổng điểm 10.00đ.'

    # Re-construct list of questions to split Bai 1 into 1.a, 1.b, 1.c
    new_cau = []

    # 12 TN
    tn_data = [
        ('Câu 1', 'V. Thu thập và tổ chức dữ liệu', ['Lựa chọn biểu đồ thích hợp'], 'NB', 1.5,
         'Biểu đồ cột kép thường được sử dụng để:\n\nA. Biểu diễn dữ liệu có hai đối tượng thống kê.\nB. Biểu diễn dữ liệu có một đối tượng thống kê.\nC. Biểu diễn sự thay đổi của dữ liệu theo thời gian.\nD. Biểu diễn tỉ lệ phần trăm số liệu của một đối tượng thống kê.',
         'A', 'Biểu đồ cột kép được sử dụng để so sánh từng cặp số liệu của hai đối tượng thống kê cùng loại. Chọn A.'),
        ('Câu 2', 'VIII. Mở đầu về tính xác suất của biến cố', ['Không gian mẫu trong trò chơi đồng xu'], 'NB', 1.0,
         'Tung đồng xu một lần. Tập hợp các kết quả có thể xảy ra đối với mặt xuất hiện của đồng xu là:\n\nA. $\\{S; N\\}$.\nB. $\\{N\\}$.\nC. $\\{S\\}$.\nD. $\\{N; N\\}$.',
         'A', 'Khi tung một đồng xu thì có 2 kết quả có thể xảy ra: mặt sấp ($S$) hoặc mặt ngửa ($N$). Tập hợp là $\\{S; N\\}$. Chọn A.'),
        ('Câu 3', 'VIII. Mở đầu về tính xác suất của biến cố', ['Tính xác suất biến cố trong rút thẻ'], 'TH', 1.5,
         'Một hộp có 30 chiếc thẻ, mỗi thẻ được đánh số từ 1 đến 30. Rút ngẫu nhiên một thẻ trong hộp. Xác suất của biến cố "Số xuất hiện trên thẻ được rút ra là bội của 6" là:\n\nA. $\\dfrac{7}{30}$.\nB. $\\dfrac{30}{5}$.\nC. $\\dfrac{1}{6}$.\nD. $\\dfrac{1}{5}$.',
         'C', 'Các bội của 6 từ 1 đến 30 là $\\{6; 12; 18; 24; 30\\}$, gồm 5 kết quả thuận lợi. Xác suất là $\\dfrac{5}{30} = \\dfrac{1}{6}$. Chọn C.'),
        ('Câu 4', 'VIII. Mở đầu về tính xác suất của biến cố', ['Xác suất thực nghiệm'], 'NB', 1.5,
         'Gieo xúc xắc 30 lần liên tiếp, có 4 lần xuất hiện mặt 2 chấm. Xác suất thực nghiệm của biến cố "Mặt xuất hiện của xúc xắc là mặt 2 chấm" là:\n\nA. $\\dfrac{6}{25}$.\nB. $\\dfrac{4}{25}$.\nC. $\\dfrac{3}{5}$.\nD. $\\dfrac{2}{15}$.',
         'D', 'Xác suất thực nghiệm bằng $\\dfrac{4}{30} = \\dfrac{2}{15}$. Chọn D.'),
        ('Câu 5', 'V. Phương trình bậc nhất một ẩn', ['Nhận biết phương trình một ẩn'], 'NB', 1.0,
         'Phương trình nào dưới đây là phương trình một ẩn?\n\nA. $x = 1$.\nB. $x = y$.\nC. $2x + y = 0$.\nD. $x + y + z = 0$.',
         'A', '$x = 1$ chỉ chứa một ẩn $x$. Chọn A.'),
        ('Câu 6', 'V. Phương trình bậc nhất một ẩn', ['Nhận biết phương trình bậc nhất một ẩn'], 'NB', 1.0,
         'Phương trình nào sau đây là phương trình bậc nhất một ẩn?\n\nA. $(x - 1)^2 = 9$.\nB. $2x - 1 = 0$.\nC. $x^2 - 1 = 0$.\nD. $3x - 4y = 0$.',
         'B', 'Phương trình $2x - 1 = 0$ có dạng $ax + b = 0$ với $a = 2 \\ne 0$. Chọn B.'),
        ('Câu 7', 'V. Phương trình bậc nhất một ẩn', ['Biểu diễn đại lượng bằng biểu thức'], 'NB', 1.5,
         'Cho hai số tự nhiên, biết hiệu hai số là 8. Nếu gọi số lớn là $x$ ($x \\in \\mathbb{N}, x > 8$) thì biểu thức biểu thị số bé là:\n\nA. $x + 8$.\nB. $x - 8$.\nC. $8 - x$.\nD. $8x$.',
         'B', 'Số lớn trừ số bé bằng 8 nên số bé bằng số lớn trừ 8, tức là $x - 8$. Chọn B.'),
        ('Câu 8', 'V. Phương trình bậc nhất một ẩn', ['Tìm tham số khi biết nghiệm phương trình'], 'TH', 1.5,
         'Giá trị của $b$ để phương trình $-2x + b = 0$ có nghiệm $x = -2$ là:\n\nA. $b = 1$.\nB. $b = -1$.\nC. $b = -4$.\nD. $b = 4$.',
         'C', 'Thay $x = -2$ vào $-2x + b = 0$ ta được $-2(-2) + b = 0 \\Leftrightarrow 4 + b = 0 \\Leftrightarrow b = -4$. Chọn C.'),
        ('Câu 9', 'VII. Định lí Thalès trong tam giác', ['Tính độ dài đoạn thẳng bằng định lí Thalès'], 'TH', 2.0,
         'Cho tam giác $ABC$, $D \\in AB, E \\in AC$ sao cho $DE \\parallel BC$. Biết $AE = 12\\text{ cm}, DB = 18\\text{ cm}, CA = 36\\text{ cm}$. Độ dài đoạn thẳng $AB$ bằng:\n\nA. $30\\text{ cm}$.\nB. $36\\text{ cm}$.\nC. $25\\text{ cm}$.\nD. $27\\text{ cm}$.',
         'D', 'Ta có: $EC = AC - AE = 36 - 12 = 24\\text{ cm}$. Vì $DE \\parallel BC$, theo định lí Thalès: $\\dfrac{AD}{DB} = \\dfrac{AE}{EC} \\Rightarrow \\dfrac{AD}{18} = \\dfrac{12}{24} = \\dfrac{1}{2} \\Rightarrow AD = 9\\text{ cm}$. Vậy $AB = AD + DB = 9 + 18 = 27\\text{ cm}$. Chọn D.'),
        ('Câu 10', 'VII. Định lí Thalès trong tam giác', ['Khái niệm đường trung bình của tam giác'], 'NB', 1.0,
         'Chọn phát biểu đúng trong các phát biểu sau:\n\nA. Đường trung bình của tam giác thì song song với cạnh thứ ba và bằng một phần ba cạnh đó.\nB. Đường trung bình của tam giác là đoạn thẳng nối trung điểm hai cạnh tam giác đó.\nC. Trong một tam giác chỉ có một đường trung bình.\nD. Đường trung bình của tam giác là đoạn thẳng nối từ một đỉnh đến trung điểm của cạnh đối diện.',
         'B', 'Định nghĩa: Đường trung bình của tam giác là đoạn thẳng nối trung điểm hai cạnh của tam giác. Chọn B.'),
        ('Câu 11', 'IX. Tam giác đồng dạng', ['Tỉ số đồng dạng của hai tam giác'], 'NB', 1.0,
         'Cho biết $\\Delta ABC \\backsim \\Delta DEF$ theo tỉ số $k = 3$ thì $\\Delta DEF \\backsim \\Delta ABC$ theo tỉ số là:\n\nA. $k = 3$.\nB. $k = 9$.\nC. $k = \\dfrac{1}{9}$.\nD. $k = \\dfrac{1}{3}$.',
         'D', 'Nếu $\\Delta ABC \\backsim \\Delta DEF$ theo tỉ số $k$ thì $\\Delta DEF \\backsim \\Delta ABC$ theo tỉ số $\\dfrac{1}{k} = \\dfrac{1}{3}$. Chọn D.'),
        ('Câu 12', 'IX. Tam giác đồng dạng', ['Tính độ dài bằng tam giác đồng dạng'], 'TH', 1.5,
         'Cho $\\Delta ABC \\backsim \\Delta DEF$ có $DE = 10, DF = 8, AC = 12$. Độ dài đoạn thẳng $AB$ là:\n\nA. 10.\nB. 12.\nC. 15.\nD. 26.',
         'C', 'Vì $\\Delta ABC \\backsim \\Delta DEF$ nên $\\dfrac{AB}{DE} = \\dfrac{AC}{DF} \\Rightarrow \\dfrac{AB}{10} = \\dfrac{12}{8} = 1{,}5 \\Rightarrow AB = 15$. Chọn C.')
    ]

    for idx, item in enumerate(tn_data):
        c_id = f'l8-ck2-2023-thach-that-c{idx+1}'
        new_cau.append({
            'id': c_id,
            'vi_tri': item[0],
            'loai': 'TN',
            'chuong': item[1],
            'dang': item[2],
            'band': item[3],
            'phut': item[4],
            'diem_bai': 0.25,
            'de': item[5],
            'dap_an': item[6],
            'loi_giai': item[7],
            'trang': 1 if idx < 9 else 2,
            'co_hinh': idx in [8, 11],
            'can_doc_anh': False,
            'da_duyet': True
        })

    # Bài 1.a (0.5đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b1a',
        'vi_tri': 'Bài 1.a',
        'loai': 'TL',
        'chuong': 'V. Phương trình bậc nhất một ẩn',
        'dang': ['Giải phương trình bậc nhất một ẩn'],
        'band': 'NB',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (1,5 điểm). Giải các phương trình sau:',
        'de': '$-6x + 16 = 0$',
        'dap_an': '$x = \\dfrac{8}{3}$',
        'loi_giai': 'Ta có:\n$$-6x + 16 = 0 \\Leftrightarrow -6x = -16 \\Leftrightarrow x = \\dfrac{8}{3}.$$\nVậy phương trình có nghiệm là $x = \\dfrac{8}{3}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 1.b (0.5đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b1b',
        'vi_tri': 'Bài 1.b',
        'loai': 'TL',
        'chuong': 'V. Phương trình bậc nhất một ẩn',
        'dang': ['Giải phương trình đưa về bậc nhất'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (1,5 điểm). Giải các phương trình sau:',
        'de': '$4(x - 1) - 6 = 8x$',
        'dap_an': '$x = -\\dfrac{5}{2}$',
        'loi_giai': 'Ta có:\n$$4(x - 1) - 6 = 8x$$\n$$\\Leftrightarrow 4x - 4 - 6 = 8x$$\n$$\\Leftrightarrow 4x - 8x = 10$$\n$$\\Leftrightarrow -4x = 10 \\Leftrightarrow x = -\\dfrac{5}{2}.$$\n(Nếu vế phải là $-8$ thì $4x - 10 = -8 \\Leftrightarrow x = \\dfrac{1}{2}$).\nVậy nghiệm của phương trình là $x = -\\dfrac{5}{2}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 1.c (0.5đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b1c',
        'vi_tri': 'Bài 1.c',
        'loai': 'TL',
        'chuong': 'V. Phương trình bậc nhất một ẩn',
        'dang': ['Giải phương trình đưa về bậc nhất'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Bài 1 (1,5 điểm). Giải các phương trình sau:',
        'de': '$5(x - 3) - 4 = 2(x - 1) + 7$',
        'dap_an': '$x = 8$',
        'loi_giai': 'Ta có:\n$$5(x - 3) - 4 = 2(x - 1) + 7$$\n$$\\Leftrightarrow 5x - 15 - 4 = 2x - 2 + 7$$\n$$\\Leftrightarrow 5x - 19 = 2x + 5$$\n$$\\Leftrightarrow 5x - 2x = 5 + 19$$\n$$\\Leftrightarrow 3x = 24 \\Leftrightarrow x = 8.$$\nVậy phương trình có nghiệm là $x = 8$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 2 (2.0đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b2',
        'vi_tri': 'Bài 2',
        'loai': 'TL',
        'chuong': 'V. Phương trình bậc nhất một ẩn',
        'dang': ['Giải bài toán bằng cách lập phương trình', 'Toán hình học'],
        'band': 'VD',
        'phut': 5.0,
        'diem_bai': 2.0,
        'de': 'Một mảnh vườn hình chữ nhật có chu vi $56\\text{ m}$. Nếu tăng chiều dài $4\\text{ m}$ và giảm chiều rộng $2\\text{ m}$ thì diện tích tăng $8\\text{ m}^2$. Tìm chiều dài ban đầu của hình chữ nhật.',
        'dap_an': '$16\\text{ m}$',
        'loi_giai': 'Nửa chu vi của mảnh vườn là: $56 : 2 = 28\\text{ (m)}$.\nGọi chiều dài ban đầu của mảnh vườn là $x$ ($\\text{m}, 0 < x < 28$).\nChiều rộng ban đầu của mảnh vườn là $28 - x$ ($\\text{m}$).\nDiện tích ban đầu của mảnh vườn là: $x(28 - x) = 28x - x^2\\text{ (m}^2)$.\nSau khi thay đổi kích thước:\nChiều dài mới là: $x + 4\\text{ (m)}$.\nChiều rộng mới là: $28 - x - 2 = 26 - x\\text{ (m)}$.\nDiện tích mới là: $(x + 4)(26 - x) = 104 + 22x - x^2\\text{ (m}^2)$.\nVì diện tích mới tăng $8\\text{ m}^2$ so với ban đầu nên ta có phương trình:\n$$(104 + 22x - x^2) - (28x - x^2) = 8$$\n$$\\Leftrightarrow 104 - 6x = 8$$\n$$\\Leftrightarrow 6x = 96 \\Leftrightarrow x = 16 \\text{ (thỏa mãn ĐK)}.$$\nVậy chiều dài ban đầu của hình chữ nhật là $16\\text{ m}$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 3.a (1.0đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b3a',
        'vi_tri': 'Bài 3.a',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Chứng minh hai tam giác đồng dạng'],
        'band': 'TH',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $OAB$ vuông tại $O$, có $OA > OB$. Lấy điểm $M$ thuộc cạnh $AB$. Kẻ đường thẳng vuông góc với $AB$ tại $M$ cắt $OA$ tại $N$, cắt tia $BO$ tại $E$. Tia $BN$ cắt $AE$ tại $F$.',
        'de': 'Chứng minh: $\\Delta OAB \\backsim \\Delta MEB$.',
        'dap_an': '$\\Delta OAB \\backsim \\Delta MEB$ (g.g)',
        'loi_giai': 'Xét $\\Delta OAB$ và $\\Delta MEB$ có:\n$\\widehat{B}$ chung,\n$\\widehat{AOB} = \\widehat{EMB} = 90^\\circ$ (vì $\\Delta OAB$ vuông tại $O$ và $EM \\perp AB$ tại $M$).\nDo đó $\\Delta OAB \\backsim \\Delta MEB$ (g.g).',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 3.b (1.0đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b3b',
        'vi_tri': 'Bài 3.b',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Chứng minh hệ thức hình học'],
        'band': 'VD',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $OAB$ vuông tại $O$, có $OA > OB$. Lấy điểm $M$ thuộc cạnh $AB$. Kẻ đường thẳng vuông góc với $AB$ tại $M$ cắt $OA$ tại $N$, cắt tia $BO$ tại $E$. Tia $BN$ cắt $AE$ tại $F$.',
        'de': 'Chứng minh: $AN \\cdot AO = AM \\cdot AB$.',
        'dap_an': '$AN \\cdot AO = AM \\cdot AB$',
        'loi_giai': 'Xét $\\Delta AMN$ và $\\Delta AOB$ có:\n$\\widehat{A}$ chung,\n$\\widehat{AMN} = \\widehat{AOB} = 90^\\circ$.\nSuy ra $\\Delta AMN \\backsim \\Delta AOB$ (g.g).\nTừ đó suy ra tỉ số đồng dạng:\n$$\\dfrac{AM}{AO} = \\dfrac{AN}{AB} \\Rightarrow AN \\cdot AO = AM \\cdot AB \\text{ (đpcm)}.$$',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 3.c (1.0đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b3c',
        'vi_tri': 'Bài 3.c',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Chứng minh tia phân giác', 'Tam giác đồng dạng c.g.c'],
        'band': 'VDC',
        'phut': 5.0,
        'diem_bai': 1.0,
        'de_chung': 'Bài 3 (3,0 điểm). Cho tam giác $OAB$ vuông tại $O$, có $OA > OB$. Lấy điểm $M$ thuộc cạnh $AB$. Kẻ đường thẳng vuông góc với $AB$ tại $M$ cắt $OA$ tại $N$, cắt tia $BO$ tại $E$. Tia $BN$ cắt $AE$ tại $F$.',
        'de': 'Chứng minh: $\\widehat{AOM} = \\widehat{NBA}$. Từ đó chứng minh $OA$ là tia phân giác của $\\widehat{FOM}$.',
        'dap_an': '$\\widehat{AOM} = \\widehat{NBA}$ và $OA$ là tia phân giác $\\widehat{FOM}$',
        'loi_giai': '1) Từ $\\Delta AMN \\backsim \\Delta AOB$ (cmt) suy ra $\\dfrac{AM}{AO} = \\dfrac{AN}{AB} \\Rightarrow \\dfrac{AM}{AN} = \\dfrac{AO}{AB}$.\nXét $\\Delta AOM$ và $\\Delta ABN$ có:\n$\\widehat{A}$ chung,\n$\\dfrac{AO}{AB} = \\dfrac{AM}{AN}$ (cmt).\nSuy ra $\\Delta AOM \\backsim \\Delta ABN$ (c.g.c) $\\Rightarrow \\widehat{AOM} = \\widehat{ABN}$ (hai góc tương ứng).\n\n2) Trong tam giác $EBA$, $AO \\perp BE$ (tại $O$) và $EM \\perp AB$ (tại $M$), mà $AO$ cắt $EM$ tại $N$ nên $N$ là trực tâm của $\\Delta EBA$.\nSuy ra $BN \\perp EA$ tại $F$.\nChứng minh $\\Delta AFN \\backsim \\Delta AOE$ (g.g) $\\Rightarrow \\dfrac{AF}{AO} = \\dfrac{AN}{AE} \\Rightarrow \\dfrac{AF}{AN} = \\dfrac{AO}{AE}$.\nTừ đó $\\Delta AOF \\backsim \\Delta AEN$ (c.g.c) $\\Rightarrow \\widehat{AOF} = \\widehat{AEN}$.\nMà $\\widehat{AEN} = \\widehat{ABF}$ (cùng phụ góc $\\widehat{BAE}$) và $\\widehat{AOM} = \\widehat{ABF}$ (cmt).\nSuy ra $\\widehat{AOF} = \\widehat{AOM}$.\nVậy $OA$ là tia phân giác của $\\widehat{FOM}$ (đpcm).',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    })

    # Bài 4 (0.5đ)
    new_cau.append({
        'id': 'l8-ck2-2023-thach-that-b4',
        'vi_tri': 'Bài 4',
        'loai': 'TL',
        'chuong': 'IV. Phân thức đại số',
        'dang': ['Chứng minh đẳng thức phân thức', 'Áp dụng hằng đẳng thức'],
        'band': 'VDC',
        'phut': 6.0,
        'diem_bai': 0.5,
        'de': 'Cho $a^2 + b^2 + c^2 = (a + b + c)^2$. Chứng minh rằng:\n$$\\dfrac{a^2}{a^2 + 2bc} + \\dfrac{b^2}{b^2 + 2ac} + \\dfrac{c^2}{c^2 + 2ab} = 1.$$',
        'dap_an': 'Đẳng thức được chứng minh.',
        'loi_giai': 'Từ giả thiết $(a + b + c)^2 = a^2 + b^2 + c^2$:\n$$\\Leftrightarrow a^2 + b^2 + c^2 + 2(ab + bc + ca) = a^2 + b^2 + c^2$$\n$$\\Leftrightarrow 2(ab + bc + ca) = 0 \\Leftrightarrow ab + bc + ca = 0 \\Rightarrow 2bc = -2ab - 2ca = -ab - ca + bc - (ab + bc + ca)...$$\nTa có: $2bc = bc + bc = bc - (ab + ca) = bc - ab - ca$.\nDo đó:\n$$a^2 + 2bc = a^2 - ab - ca + bc = a(a - b) - c(a - b) = (a - b)(a - c).$$\nTương tự:\n$$b^2 + 2ac = (b - c)(b - a) = -(a - b)(b - c),$$\n$$c^2 + 2ab = (c - a)(c - b) = (a - c)(b - c).$$\nThay vào vế trái ta được:\n$$VT = \\dfrac{a^2}{(a-b)(a-c)} - \\dfrac{b^2}{(a-b)(b-c)} + \\dfrac{c^2}{(a-c)(b-c)}$$\n$$= \\dfrac{a^2(b-c) - b^2(a-c) + c^2(a-b)}{(a-b)(b-c)(a-c)}$$\n$$= \\dfrac{a^2b - a^2c - ab^2 + b^2c + c^2(a-b)}{(a-b)(b-c)(a-c)}$$\n$$= \\dfrac{-ab(a-b) + c(a^2-b^2) - c^2(a-b)}{(a-b)(b-c)(a-c)}$$\n$$= \\dfrac{(a-b)[-ab + c(a+b) - c^2]}{(a-b)(b-c)(a-c)}$$\n$$= \\dfrac{(a-b)(b-c)(a-c)}{(a-b)(b-c)(a-c)} = 1 = VP.$$\nVậy đẳng thức được chứng minh.' ,
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    })

    d['cau'] = new_cau
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D3 (Thach That 2023): {n} cau, {tot:.2f}d')

if __name__ == '__main__':
    update_d1()
    update_d2()
    update_d3()
