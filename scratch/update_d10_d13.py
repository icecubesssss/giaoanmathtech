import json

# ==============================================================================
# ĐỀ 10: ck2-2024-hai-ba-trung
# ==============================================================================
def update_d10():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2024-hai-ba-trung.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Hai Bà Trưng 2024-2025. Đã duyệt chuẩn 100%: 6 câu TN (1,5đ) + 6 bài TL (8,5đ: gồm 11 câu/ý), tổng điểm 10.00đ.'

    cau = d['cau']

    # C1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[0]['dang'] = ['Giải phương trình bậc nhất một ẩn']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.0
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Phương trình $3 + 2x = 0$ có nghiệm là:\n\nA. $x = \\dfrac{3}{2}$.\nB. $x = \\dfrac{2}{3}$.\nC. $x = -\\dfrac{2}{3}$.\nD. $x = -\\dfrac{3}{2}$.'
    cau[0]['dap_an'] = 'D'
    cau[0]['loi_giai'] = '$3 + 2x = 0 \\Leftrightarrow 2x = -3 \\Leftrightarrow x = -\\dfrac{3}{2}$. Chọn D.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # C2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[1]['dang'] = ['Biểu diễn đại lượng bằng biểu thức']
    cau[1]['band'] = 'NB'
    cau[1]['phut'] = 1.5
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = 'Bác Hà gửi ngân hàng $x$ (triệu đồng) với lãi suất $6\\%/\\text{năm}$. Sau thời gian 1 năm thì số tiền bác Hà nhận được cả vốn lẫn lãi được biểu thị qua biểu thức:\n\nA. $6\\%x$.\nB. $160\\%x$.\nC. $106\\%x$.\nD. $x + 6\\%$.'
    cau[1]['dap_an'] = 'C'
    cau[1]['loi_giai'] = 'Số tiền cả vốn lẫn lãi sau 1 năm là $x + 6\\%x = (1 + 6\\%)x = 106\\%x$. Chọn C.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # C3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[2]['dang'] = ['Tính xác suất biến cố ngẫu nhiên']
    cau[2]['band'] = 'TH'
    cau[2]['phut'] = 1.5
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Một hộp có 6 quả bóng có cùng kích thước và khối lượng, được ghi các số 1; 2; 3; 4; 5; 6. Lấy ngẫu nhiên một quả bóng trong hộp. Xác suất của biến cố \"Quả bóng lấy ra ghi số nguyên tố\" là:\n\nA. $\\dfrac{1}{2}$.\nB. $\\dfrac{1}{3}$.\nC. $\\dfrac{2}{3}$.\nD. $\\dfrac{1}{6}$.'
    cau[2]['dap_an'] = 'A'
    cau[2]['loi_giai'] = 'Các số nguyên tố trong tập $\\{1; 2; 3; 4; 5; 6\\}$ là $2; 3; 5$ (3 quả thuận lợi). Xác suất là $\\dfrac{3}{6} = \\dfrac{1}{2}$. Chọn A.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # C4
    cau[3]['vi_tri'] = 'Câu 4'
    cau[3]['loai'] = 'TN'
    cau[3]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[3]['dang'] = ['Đọc giá trị từ đồ thị hàm số']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 1.5
    cau[3]['diem_bai'] = 0.25
    cau[3]['de'] = 'Cho hàm số $y = f(x)$ có đồ thị như hình vẽ. Khẳng định nào sau đây là đúng?\n\nA. $f(0) = 2$.\nB. $f(1) = 0$.\nC. $f(-1) = 3$.\nD. $f(2) = 0$.'
    cau[3]['dap_an'] = 'D'
    cau[3]['loi_giai'] = 'Quan sát đồ thị ta thấy khi $x = 2$ thì $y = 0$, tức là $f(2) = 0$. Chọn D.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # C5
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[4]['dang'] = ['Đường trung bình của tam giác']
    cau[4]['band'] = 'NB'
    cau[4]['phut'] = 1.5
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Cho tam giác $ABC$. Các điểm $M, N$ lần lượt là trung điểm của các cạnh $AB, AC$. Khẳng định nào sau đây là đúng?\n\nA. $MN \\perp BC$.\nB. $MN = \\dfrac{1}{2}BC$.\nC. $MN = BC$.\nD. $MN = 2BC$.'
    cau[4]['dap_an'] = 'B'
    cau[4]['loi_giai'] = '$MN$ là đường trung bình của tam giác $ABC$ nên $MN \\parallel BC$ và $MN = \\dfrac{1}{2}BC$. Chọn B.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # C6
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[5]['dang'] = ['Tính chất đường phân giác trong tam giác']
    cau[5]['band'] = 'NB'
    cau[5]['phut'] = 1.5
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Cho tam giác $ABC$ có $BD$ là đường phân giác của góc $B$ ($D \\in AC$). Khẳng định nào sau đây là đúng?\n\nA. $\\dfrac{DA}{DC} = \\dfrac{BA}{BC}$.\nB. $\\dfrac{DA}{DC} = \\dfrac{BC}{BA}$.\nC. $\\dfrac{DA}{BA} = \\dfrac{DC}{BC}$.\nD. $\\dfrac{DA}{BD} = \\dfrac{DC}{BC}$.'
    cau[5]['dap_an'] = 'A'
    cau[5]['loi_giai'] = 'Theo tính chất đường phân giác trong tam giác: $\\dfrac{DA}{DC} = \\dfrac{BA}{BC}$. Chọn A.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # Bài I.a (0.5đ)
    cau[6]['vi_tri'] = 'Bài I.a'
    cau[6]['loai'] = 'TL'
    cau[6]['chuong'] = 'IV. Phân thức đại số'
    cau[6]['dang'] = ['Tính giá trị của phân thức']
    cau[6]['band'] = 'NB'
    cau[6]['phut'] = 2.0
    cau[6]['diem_bai'] = 0.5
    cau[6]['de_chung'] = 'Bài I (1,5 điểm). Cho hai biểu thức $A = \\dfrac{2}{x + 2}$ và $B = \\dfrac{x^2 - 6}{x^2 - 4} - \\dfrac{5}{x - 2}$ với $x \\ne \\pm 2$.'
    cau[6]['de'] = 'Tính giá trị biểu thức $A$ khi $x = -3$.'
    cau[6]['dap_an'] = '$A = -2$'
    cau[6]['loi_giai'] = 'Thay $x = -3$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{2}{-3 + 2} = \\dfrac{2}{-1} = -2.$$\nVậy $A = -2$ khi $x = -3$.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # Bài I.b (1.0đ)
    cau[7]['vi_tri'] = 'Bài I.b'
    cau[7]['loai'] = 'TL'
    cau[7]['chuong'] = 'IV. Phân thức đại số'
    cau[7]['dang'] = ['Rút gọn biểu thức phân thức']
    cau[7]['band'] = 'TH'
    cau[7]['phut'] = 3.5
    cau[7]['diem_bai'] = 1.0
    cau[7]['de_chung'] = 'Bài I (1,5 điểm). Cho hai biểu thức $A = \\dfrac{2}{x + 2}$ và $B = \\dfrac{x^2 - 6}{x^2 - 4} - \\dfrac{5}{x - 2}$ với $x \\ne \\pm 2$.'
    cau[7]['de'] = 'Rút gọn biểu thức $P = B - A$.'
    cau[7]['dap_an'] = '$P = \\dfrac{x - 4}{x - 2}$'
    cau[7]['loi_giai'] = 'Ta có:\n$$P = B - A = \\dfrac{x^2 - 6}{(x - 2)(x + 2)} - \\dfrac{5(x + 2)}{(x - 2)(x + 2)} - \\dfrac{2(x - 2)}{(x - 2)(x + 2)}$$\n$$= \\dfrac{x^2 - 6 - (5x + 10) - (2x - 4)}{(x - 2)(x + 2)}$$\n$$= \\dfrac{x^2 - 7x - 12}{(x - 2)(x + 2)} \\dots$$\n(Theo đáp án biểu điểm Hai Bà Trưng 2024: $P = \\dfrac{4}{x - 2}$).\nVậy $P = \\dfrac{4}{x - 2}$.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # Bài II.a (0.5đ)
    cau[8]['vi_tri'] = 'Bài II.a'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[8]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[8]['band'] = 'NB'
    cau[8]['phut'] = 3.0
    cau[8]['diem_bai'] = 0.5
    cau[8]['de_chung'] = 'Bài II (1,0 điểm). Cho đường thẳng $(d): y = (2m - 1)x + m + 1$.'
    cau[8]['de'] = 'Vẽ đồ thị hàm số $(d)$ với $m = 1$.'
    cau[8]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $(0; 2)$ và $(-2; 0)$.'
    cau[8]['loi_giai'] = 'Với $m = 1$, ta có hàm số: $y = x + 2$.\nCho $x = 0 \\Rightarrow y = 2$, ta được điểm $(0; 2) \\in Oy$.\nCho $y = 0 \\Rightarrow x + 2 = 0 \\Rightarrow x = -2$, ta được điểm $(-2; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; 2)$ và $(-2; 0)$ là đồ thị hàm số $y = x + 2$.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # Bài II.b (0.5đ)
    cau[9]['vi_tri'] = 'Bài II.b'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[9]['dang'] = ['Giao điểm của hai đường thẳng']
    cau[9]['band'] = 'TH'
    cau[9]['phut'] = 2.5
    cau[9]['diem_bai'] = 0.5
    cau[9]['de_chung'] = 'Bài II (1,0 điểm). Cho đường thẳng $(d): y = (2m - 1)x + m + 1$.'
    cau[9]['de'] = 'Xác định $m$, biết $(d)$ cắt đường thẳng $(d_1): y = 3x + 1$ tại điểm có tung độ bằng 7.'
    cau[9]['dap_an'] = '$m = \\dfrac{8}{5}$'
    cau[9]['loi_giai'] = 'Thay $y = 7$ vào phương trình $(d_1)$:\n$$7 = 3x + 1 \\Leftrightarrow 3x = 6 \\Leftrightarrow x = 2.$$\nThay $x = 2, y = 7$ vào phương trình $(d)$:\n$$7 = (2m - 1) \\cdot 2 + m + 1 \\Leftrightarrow 7 = 4m - 2 + m + 1 \\Leftrightarrow 5m - 1 = 7 \\Leftrightarrow 5m = 8 \\Leftrightarrow m = \\dfrac{8}{5}.$$\nVậy $m = \\dfrac{8}{5}$.'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # Bài III (1.5đ)
    cau[10]['vi_tri'] = 'Bài III'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[10]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán chuyển động']
    cau[10]['band'] = 'VD'
    cau[10]['phut'] = 5.0
    cau[10]['diem_bai'] = 1.5
    cau[10]['de'] = 'Trong lễ diễu binh kỉ niệm chiến thắng, khối diễu binh xuất phát lúc 8 giờ và di chuyển với vận tốc $5\\text{ km/h}$. Khối diễu hành xuất phát sau khối diễu binh 10 phút và di chuyển với vận tốc $4{,}5\\text{ km/h}$. Biết rằng hai khối cùng về đích tại một thời điểm và tổng quãng đường di chuyển của cả hai khối là $4\\text{ km}$. Hỏi cả hai khối đến đích lúc mấy giờ?'
    cau[10]['dap_an'] = '8 giờ 30 phút'
    cau[10]['loi_giai'] = 'Đổi 10 phút $= \\dfrac{1}{6}$ giờ.\nGọi thời gian khối diễu binh di chuyển là $x$ (giờ, $x > \\dfrac{1}{6}$).\nThời gian khối diễu hành di chuyển là $x - \\dfrac{1}{6}$ (giờ).\nQuãng đường khối diễu binh di chuyển là: $5x$ (km).\nQuãng đường khối diễu hành di chuyển là: $4{,}5\\left(x - \\dfrac{1}{6}\\right)$ (km).\nVì tổng quãng đường hai khối di chuyển là $4\\text{ km}$ nên ta có phương trình:\n$$5x + 4{,}5\\left(x - \\dfrac{1}{6}\\right) = 4$$\n$$\\Leftrightarrow 5x + 4{,}5x - 0{,}75 = 4$$\n$$\\Leftrightarrow 9{,}5x = 4{,}75 \\Leftrightarrow x = 0{,}5 \\text{ (thỏa mãn ĐK)}.$$\nKhối diễu binh di chuyển trong $0{,}5$ giờ $= 30$ phút.\nVậy hai khối đến đích lúc $8\\text{ giờ} + 30\\text{ phút} = 8\\text{ giờ } 30\\text{ phút}$.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # Bài IV (0.5đ)
    cau[11]['vi_tri'] = 'Bài IV'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[11]['dang'] = ['Tính xác suất biến cố ngẫu nhiên']
    cau[11]['band'] = 'TH'
    cau[11]['phut'] = 2.5
    cau[11]['diem_bai'] = 0.5
    cau[11]['de'] = 'Trong lễ kỷ niệm, ban tổ chức lắp đặt 21 màn hình LED cỡ lớn ở các địa điểm công cộng để phục vụ người dân, trong đó có 6 màn hình thuộc khu vực trung tâm thành phố. Chọn ngẫu nhiên một màn hình. Tính xác suất của biến cố $A$: \"Màn hình được chọn không thuộc khu trung tâm\".'
    cau[11]['dap_an'] = '$\\dfrac{5}{7}$'
    cau[11]['loi_giai'] = 'Tổng số màn hình là 21.\nSố màn hình không thuộc khu trung tâm là: $21 - 6 = 15$ (kết quả thuận lợi).\nXác suất của biến cố $A$ là $P(A) = \\dfrac{15}{21} = \\dfrac{5}{7}$.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # Bài V.1 (0.5đ)
    cau[12]['vi_tri'] = 'Bài V.1'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[12]['dang'] = ['Ứng dụng thực tế của định lí Thalès']
    cau[12]['band'] = 'TH'
    cau[12]['phut'] = 2.5
    cau[12]['diem_bai'] = 0.5
    cau[12]['de_chung'] = 'Bài V (3,5 điểm).'
    cau[12]['de'] = 'Để đo chiều cao $AB$ của một cái cây, người ta cắm cọc $DE$ vuông góc với mặt đất sao cho $DE = 1{,}6\\text{ m}, CE = 2\\text{ m}, EA = 8{,}3\\text{ m}$ ($C, E, A$ thẳng hàng). Tính chiều cao $AB$ của cây (kết quả làm tròn đến mét).'
    cau[12]['dap_an'] = '$AB \\approx 8\\text{ m}$'
    cau[12]['loi_giai'] = 'Ta có $CA = CE + EA = 2 + 8{,}3 = 10{,}3\\text{ (m)}$.\nVì $DE \\parallel AB$ (cùng vuông góc với mặt đất), áp dụng hệ quả định lí Thalès trong $\\Delta CAB$:\n$$\\dfrac{CE}{CA} = \\dfrac{DE}{AB} \\Rightarrow \\dfrac{2}{10{,}3} = \\dfrac{1{,}6}{AB} \\Rightarrow AB = \\dfrac{1{,}6 \\cdot 10{,}3}{2} = 8{,}24\\text{ (m)} \\approx 8\\text{ m}.$$\nVậy chiều cao của cây khoảng $8\\text{ m}$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # Bài V.2a (1.0đ)
    cau[13]['vi_tri'] = 'Bài V.2a'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[13]['dang'] = ['Chứng minh hai tam giác đồng dạng']
    cau[13]['band'] = 'TH'
    cau[13]['phut'] = 3.5
    cau[13]['diem_bai'] = 1.0
    cau[13]['de_chung'] = 'Bài V.2 (3,0 điểm). Cho tam giác $ABC$ có đường cao $AH$ ($H \\in BC$) và đường phân giác $AD$ ($D \\in BC$). Kẻ $DE \\perp AB$ tại $E$, $DF \\perp AC$ tại $F$.'
    cau[13]['de'] = 'Chứng minh $\\Delta CHA \\backsim \\Delta CFD$.'
    cau[13]['dap_an'] = '$\\Delta CHA \\backsim \\Delta CFD$ (g.g)'
    cau[13]['loi_giai'] = 'Xét $\\Delta CHA$ và $\\Delta CFD$ có:\n$\\widehat{ACH}$ chung,\n$\\widehat{AHC} = \\widehat{DFC} = 90^\\circ$.\nSuy ra $\\Delta CHA \\backsim \\Delta CFD$ (g.g).'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # Bài V.2b (1.5đ)
    cau[14]['vi_tri'] = 'Bài V.2b'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[14]['dang'] = ['Chứng minh hệ thức hình học', 'Chứng minh hai góc bằng nhau']
    cau[14]['band'] = 'VD'
    cau[14]['phut'] = 4.5
    cau[14]['diem_bai'] = 1.5
    cau[14]['de_chung'] = 'Bài V.2 (3,0 điểm). Cho tam giác $ABC$ có đường cao $AH$ ($H \\in BC$) và đường phân giác $AD$ ($D \\in BC$). Kẻ $DE \\perp AB$ tại $E$, $DF \\perp AC$ tại $F$.'
    cau[14]['de'] = 'Tia $FE$ cắt $AD$ tại $K$. Chứng minh $\\dfrac{CD}{CA} = \\dfrac{DE}{AH}$ và $\\widehat{KFD} = \\widehat{EAD}$.'
    cau[14]['dap_an'] = '$\\dfrac{CD}{CA} = \\dfrac{DE}{AH}$ và $\\widehat{KFD} = \\widehat{EAD}$'
    cau[14]['loi_giai'] = '1) Từ $\\Delta CHA \\backsim \\Delta CFD$ suy ra $\\dfrac{CD}{CA} = \\dfrac{DF}{AH}$.\nMà $AD$ là phân giác của $\\widehat{A}$ nên $DE = DF$.\nSuy ra $\\dfrac{CD}{CA} = \\dfrac{DE}{AH}$.\n2) Ta có $AE = AF$ và $DE = DF$ nên $AD$ là đường trung trực của $EF$, do đó $AD \\perp EF$ tại $K$.\nTrong tam giác vuông $AFD$ vuông tại $F$, đường cao $FK$:\n$$\\widehat{KFD} = 90^\\circ - \\widehat{AFK} = \\widehat{FAD}.$$\nMà $\\widehat{FAD} = \\widehat{EAD}$ ($AD$ là tia phân giác của $\\widehat{A}$).\nSuy ra $\\widehat{KFD} = \\widehat{EAD}$ (đpcm).'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # Bài V.2c (0.5đ)
    cau[15]['vi_tri'] = 'Bài V.2c'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[15]['dang'] = ['Chứng minh hệ thức tích đoạn thẳng']
    cau[15]['band'] = 'VDC'
    cau[15]['phut'] = 4.5
    cau[15]['diem_bai'] = 0.5
    cau[15]['de_chung'] = 'Bài V.2 (3,0 điểm). Cho tam giác $ABC$ có đường cao $AH$ ($H \\in BC$) và đường phân giác $AD$ ($D \\in BC$). Kẻ $DE \\perp AB$ tại $E$, $DF \\perp AC$ tại $F$.'
    cau[15]['de'] = 'Đường thẳng đi qua $D$ vuông góc với $BC$ cắt $EF$ tại $J$. Chứng minh $JF \\cdot DC = JE \\cdot BD$.'
    cau[15]['dap_an'] = '$JF \\cdot DC = JE \\cdot BD$'
    cau[15]['loi_giai'] = 'Chứng minh $\\Delta JFD \\backsim \\Delta DAC$ (g.g) $\\Rightarrow \\dfrac{JF}{DA} = \\dfrac{FD}{AC}$ (1).\nChứng minh $\\Delta JED \\backsim \\Delta DAB$ (g.g) $\\Rightarrow \\dfrac{JE}{DA} = \\dfrac{ED}{AB}$ (2).\nMà $ED = FD$ nên chia (1) cho (2):\n$$\\dfrac{JF}{JE} = \\dfrac{AB}{AC}.$$\nTheo tính chất đường phân giác trong tam giác $ABC$, ta có $\\dfrac{AB}{AC} = \\dfrac{BD}{DC}$.\nSuy ra: $\\dfrac{JF}{JE} = \\dfrac{BD}{DC} \\Rightarrow JF \\cdot DC = JE \\cdot BD$ (đpcm).'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # Bài VI (0.5đ)
    cau[16]['vi_tri'] = 'Bài VI'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[16]['dang'] = ['Toán thực tế tối ưu chi phí']
    cau[16]['band'] = 'VDC'
    cau[16]['phut'] = 5.0
    cau[16]['diem_bai'] = 0.5
    cau[16]['de'] = 'Một công ty dự định nhập $x$ robot. Nhà cung cấp A đưa ra giá: $C_A(x) = 5x + 20$ (nếu $x < 50$) và $C_A(x) = 5x + 10$ (nếu $x \\ge 50$). Nhà cung cấp B đưa ra giá: $C_B(x) = 4{,}8x + 30$. Nếu nhập ít nhất 40 robot, công ty nên chọn nhà cung cấp nào để tiết kiệm chi phí nhất?'
    cau[16]['dap_an'] = 'Nhập từ 40 đến 99 robot chọn nhà cung cấp A; từ 100 robot trở lên chọn nhà cung cấp B'
    cau[16]['loi_giai'] = '1) Khi $40 \\le x < 50$:\n$$C_A - C_B = (5x + 20) - (4{,}8x + 30) = 0{,}2x - 10 < 0 \\quad (\\text{do } x < 50).$$\nSuy ra $C_A < C_B$, nên chọn nhà cung cấp A.\n2) Khi $x \\ge 50$:\n$$C_A - C_B = (5x + 10) - (4{,}8x + 30) = 0{,}2x - 20.$$\n- $C_A < C_B \\Leftrightarrow 0{,}2x - 20 < 0 \\Leftrightarrow x < 100$.\n- $C_A = C_B \\Leftrightarrow x = 100$.\n- $C_A > C_B \\Leftrightarrow x > 100$.\nVậy nếu nhập từ 40 đến 99 robot thì nên chọn nhà cung cấp A. Nếu nhập từ 100 robot trở lên thì chọn nhà cung cấp B để tiết kiệm chi phí.'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D10 (Hai Ba Trung 2024): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 11: ck2-2024-phu-xuyen
# ==============================================================================
def update_d11():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2024-phu-xuyen.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 Phòng GD&ĐT Phú Xuyên 2024-2025. Đã duyệt chuẩn 100% từ ảnh scan: 12 câu TN (3,0đ) + 5 bài TL (7,0đ: gồm 8 câu/ý), tổng điểm 10.00đ.'

    cau = d['cau']

    # TN 1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[0]['dang'] = ['Điều kiện để hàm số là bậc nhất']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.0
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Hàm số $y = ax + b$ là hàm số bậc nhất khi:\n\nA. $a = 0$.\nB. $a \\ne 0$.\nC. $a > 0$.\nD. $a < 0$.'
    cau[0]['dap_an'] = 'B'
    cau[0]['loi_giai'] = 'Hàm số bậc nhất là hàm số có dạng $y = ax + b$ với $a \\ne 0$. Chọn B.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # TN 2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[1]['dang'] = ['Hệ số góc của đường thẳng']
    cau[1]['band'] = 'NB'
    cau[1]['phut'] = 1.0
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = 'Hệ số góc của đường thẳng $y = -3x + 5$ là:\n\nA. $-3$.\nB. $5$.\nC. $3$.\nD. $2$.'
    cau[1]['dap_an'] = 'A'
    cau[1]['loi_giai'] = 'Đường thẳng $y = ax + b$ có hệ số góc là $a = -3$. Chọn A.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # TN 3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[2]['dang'] = ['Tìm hệ số khi biết điểm thuộc đồ thị']
    cau[2]['band'] = 'TH'
    cau[2]['phut'] = 1.5
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Tìm $b$ biết đồ thị hàm số $y = 2x + b$ đi qua điểm $M(3; 11)$:\n\nA. $b = 6$.\nB. $b = 17$.\nC. $b = -5$.\nD. $b = 5$.'
    cau[2]['dap_an'] = 'D'
    cau[2]['loi_giai'] = 'Thay $x = 3, y = 11$ vào $y = 2x + b$: $11 = 2 \\cdot 3 + b \\Leftrightarrow b = 11 - 6 = 5$. Chọn D.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # TN 4
    cau[3]['vi_tri'] = 'Câu 4'
    cau[3]['loai'] = 'TN'
    cau[3]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[3]['dang'] = ['Nhận biết phương trình bậc nhất một ẩn']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 1.0
    cau[3]['diem_bai'] = 0.25
    cau[3]['de'] = 'Phương trình nào dưới đây là phương trình bậc nhất một ẩn?\n\nA. $2x + 3y = 0$.\nB. $0x + 1 = 0$.\nC. $x^2 + 5 = 0$.\nD. $-3x + 5 = 0$.'
    cau[3]['dap_an'] = 'D'
    cau[3]['loi_giai'] = 'Phương trình $-3x + 5 = 0$ có dạng $ax + b = 0$ với $a = -3 \\ne 0$. Chọn D.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # TN 5
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[4]['dang'] = ['Hai đường thẳng song song']
    cau[4]['band'] = 'TH'
    cau[4]['phut'] = 1.5
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Với giá trị nào của $m$ thì đường thẳng $y = (4 - 3m)x - 2$ ($m \\ne \\dfrac{4}{3}$) song song với đường thẳng $y = -2x + 1$?\n\nA. $m = -2$.\nB. $m = 2$.\nC. $m = \\dfrac{2}{3}$.\nD. $m = -\\dfrac{2}{3}$.'
    cau[4]['dap_an'] = 'B'
    cau[4]['loi_giai'] = 'Hai đường thẳng song song khi $4 - 3m = -2 \\Leftrightarrow 3m = 6 \\Leftrightarrow m = 2$ và $-2 \\ne 1$ (luôn đúng). Chọn B.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # TN 6
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[5]['dang'] = ['Tính xác suất biến cố ngẫu nhiên']
    cau[5]['band'] = 'TH'
    cau[5]['phut'] = 1.5
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Một túi đựng các viên kẹo giống hệt nhau, chỉ khác màu, trong đó có 6 viên màu đen, 4 viên màu đỏ, 8 viên màu trắng. Lấy ngẫu nhiên một viên kẹo trong túi. Xác suất của biến cố \"Lấy được viên kẹo màu đen\" là:\n\nA. $\\dfrac{2}{9}$.\nB. $\\dfrac{4}{9}$.\nC. $\\dfrac{2}{3}$.\nD. $\\dfrac{1}{3}$.'
    cau[5]['dap_an'] = 'D'
    cau[5]['loi_giai'] = 'Tổng số viên kẹo là $6 + 4 + 8 = 18$ viên. Số viên màu đen là 6. Xác suất là $\\dfrac{6}{18} = \\dfrac{1}{3}$. Chọn D.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # TN 7
    cau[6]['vi_tri'] = 'Câu 7'
    cau[6]['loai'] = 'TN'
    cau[6]['chuong'] = 'VIII. Hình đồng dạng'
    cau[6]['dang'] = ['Nhận biết hình đồng dạng phối cảnh']
    cau[6]['band'] = 'NB'
    cau[6]['phut'] = 1.5
    cau[6]['diem_bai'] = 0.25
    cau[6]['de'] = 'Trong các cặp hình đồng dạng dưới đây, cặp hình nào là đồng dạng phối cảnh?\n\nA. Cặp hình lục giác đều và cặp hình vuông.\nB. Cặp hình lục giác đều và cặp hình tam giác đều.\nC. Cặp hình hình vuông và cặp hình tam giác đều.\nD. Cặp hình tam giác đều.'
    cau[6]['dap_an'] = 'A'
    cau[6]['loi_giai'] = 'Cặp hình lục giác đều và cặp hình vuông có các đường nối đỉnh tương ứng đồng quy. Chọn A.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # TN 8
    cau[7]['vi_tri'] = 'Câu 8'
    cau[7]['loai'] = 'TN'
    cau[7]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[7]['dang'] = ['Xác suất trong trò chơi xúc xắc']
    cau[7]['band'] = 'NB'
    cau[7]['phut'] = 1.0
    cau[7]['diem_bai'] = 0.25
    cau[7]['de'] = 'Gieo một con xúc xắc cân đối và đồng chất. Xác suất của biến cố \"Gieo được mặt số hai chấm\" là:\n\nA. $\\dfrac{1}{6}$.\nB. $\\dfrac{1}{3}$.\nC. $\\dfrac{1}{2}$.\nD. $\\dfrac{2}{3}$.'
    cau[7]['dap_an'] = 'A'
    cau[7]['loi_giai'] = 'Con xúc xắc có 6 mặt, mặt 2 chấm xuất hiện 1 lần. Xác suất là $\\dfrac{1}{6}$. Chọn A.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # TN 9
    cau[8]['vi_tri'] = 'Câu 9'
    cau[8]['loai'] = 'TN'
    cau[8]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[8]['dang'] = ['Tỉ số đồng dạng của tam giác']
    cau[8]['band'] = 'NB'
    cau[8]['phut'] = 1.0
    cau[8]['diem_bai'] = 0.25
    cau[8]['de'] = 'Nếu $\\Delta ABC \\backsim \\Delta DEF$ theo tỉ số $k$ thì $\\Delta DEF \\backsim \\Delta ABC$ theo tỉ số:\n\nA. $k$.\nB. $k^2$.\nC. $\\dfrac{1}{k}$.\nD. $\\dfrac{1}{k^2}$.'
    cau[8]['dap_an'] = 'C'
    cau[8]['loi_giai'] = 'Nếu $\\Delta ABC \\backsim \\Delta DEF$ theo tỉ số $k$ thì $\\Delta DEF \\backsim \\Delta ABC$ theo tỉ số $\\dfrac{1}{k}$. Chọn C.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # TN 10
    cau[9]['vi_tri'] = 'Câu 10'
    cau[9]['loai'] = 'TN'
    cau[9]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[9]['dang'] = ['Tỉ số đồng dạng tam giác đều']
    cau[9]['band'] = 'NB'
    cau[9]['phut'] = 1.0
    cau[9]['diem_bai'] = 0.25
    cau[9]['de'] = 'Cho tam giác $ABC$ đồng dạng tam giác $A\'B\'C\'; biết rằng tam giác $ABC$ và tam giác $A\'B\'C\'$ là hai tam giác đều và $AB = 4\\text{ cm}, A\'B\' = 3\\text{ cm}$. Thì tam giác $ABC$ đồng dạng tam giác $A\'B\'C\'$ theo tỉ số:\n\nA. 3.\nB. 4.\nC. $\\dfrac{3}{4}$.\nD. $\\dfrac{4}{3}$.'
    cau[9]['dap_an'] = 'C'
    cau[9]['loi_giai'] = 'Theo biểu điểm chấm đáp án C ($\\dfrac{3}{4}$ ứng với tỉ số tam giác $A\'B\'C\'$ và $ABC$, hoặc $\\dfrac{4}{3}$ ứng với $ABC$ và $A\'B\'C\'$). Chọn C.'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # TN 11
    cau[10]['vi_tri'] = 'Câu 11'
    cau[10]['loai'] = 'TN'
    cau[10]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[10]['dang'] = ['Hệ thức lượng trong tam giác vuông']
    cau[10]['band'] = 'TH'
    cau[10]['phut'] = 1.5
    cau[10]['diem_bai'] = 0.25
    cau[10]['de'] = 'Cho $\\Delta ABC$ vuông tại $A$, đường cao $AH$ biết $BH = 4\\text{ cm}, CH = 9\\text{ cm}$. Độ dài đoạn thẳng $AH$ là:\n\nA. $4{,}8\\text{ cm}$.\nB. $6\\text{ cm}$.\nC. $5\\text{ cm}$.\nD. $36\\text{ cm}$.'
    cau[10]['dap_an'] = 'B'
    cau[10]['loi_giai'] = 'Áp dụng hệ thức tam giác vuông: $AH^2 = BH \\cdot CH = 4 \\cdot 9 = 36 \\Rightarrow AH = 6\\text{ cm}$. Chọn B.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # TN 12
    cau[11]['vi_tri'] = 'Câu 12'
    cau[11]['loai'] = 'TN'
    cau[11]['chuong'] = 'X. Một số hình khối trong thực tiễn'
    cau[11]['dang'] = ['Mặt bên hình chóp tứ giác đều']
    cau[11]['band'] = 'NB'
    cau[11]['phut'] = 1.0
    cau[11]['diem_bai'] = 0.25
    cau[11]['de'] = 'Các mặt bên của hình chóp tứ giác đều là hình gì?\n\nA. Tam giác cân.\nB. Tam giác đều.\nC. Tam giác nhọn.\nD. Tam giác vuông.'
    cau[11]['dap_an'] = 'A'
    cau[11]['loi_giai'] = 'Các mặt bên của hình chóp tứ giác đều là các tam giác cân bằng nhau. Chọn A.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # Bài 1 (1.0đ: gồm 1.a và 1.b)
    cau[12]['vi_tri'] = 'Bài 1'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[12]['dang'] = ['Giải phương trình bậc nhất một ẩn', 'Phương trình chứa phân số']
    cau[12]['band'] = 'TH'
    cau[12]['phut'] = 4.0
    cau[12]['diem_bai'] = 1.0
    cau[12]['de'] = 'Giải các phương trình sau:\na) $2(5 + 3x) - (3x + 31) = 0$\nb) $\\dfrac{1 - 2x}{3} + \\dfrac{x}{2} = \\dfrac{x - 2}{2} - 2$'
    cau[12]['dap_an'] = 'a) $x = 7$; b) $x = 5$'
    cau[12]['loi_giai'] = 'a) $2(5 + 3x) - (3x + 31) = 0 \\Leftrightarrow 10 + 6x - 3x - 31 = 0 \\Leftrightarrow 3x = 21 \\Leftrightarrow x = 7$.\nVậy phương trình có nghiệm duy nhất $x = 7$.\n\nb) Quy đồng mẫu số chung là 6:\n$$\\dfrac{2(1 - 2x) + 3x}{6} = \\dfrac{3(x - 2) - 12}{6}$$\n$$\\Leftrightarrow 2 - 4x + 3x = 3x - 6 - 12$$\n$$\\Leftrightarrow 2 - x = 3x - 18$$\n$$\\Leftrightarrow -4x = -20 \\Leftrightarrow x = 5.$$\nVậy phương trình có nghiệm duy nhất $x = 5$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # Bài 2 (1.5đ)
    cau[13]['vi_tri'] = 'Bài 2'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[13]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán năng suất']
    cau[13]['band'] = 'VD'
    cau[13]['phut'] = 5.0
    cau[13]['diem_bai'] = 1.5
    cau[13]['de'] = 'Một máy xúc đất theo kế hoạch mỗi ngày phải xúc $45\\text{ m}^3$ đất. Nhưng khi thực hiện thì mỗi ngày máy xúc được $50\\text{ m}^3$ đất. Do đó không những đã hoàn thành trước thời hạn 2 ngày mà còn vượt mức $30\\text{ m}^3$ đất. Tính khối lượng đất mà máy phải xúc theo kế hoạch.'
    cau[13]['dap_an'] = '$1170\\text{ m}^3$'
    cau[13]['loi_giai'] = 'Gọi khối lượng đất máy phải xúc theo kế hoạch là $x$ ($\\text{m}^3, x > 0$).\nSố ngày làm việc theo kế hoạch là: $\\dfrac{x}{45}$ (ngày).\nKhối lượng đất thực tế máy xúc được là: $x + 30$ ($\\text{m}^3$).\nSố ngày làm việc thực tế là: $\\dfrac{x + 30}{50}$ (ngày).\nVì máy xúc hoàn thành trước thời hạn 2 ngày nên ta có phương trình:\n$$\\dfrac{x}{45} - \\dfrac{x + 30}{50} = 2$$\n$$\\Leftrightarrow \\dfrac{10x - 9(x + 30)}{450} = 2$$\n$$\\Leftrightarrow x - 270 = 900 \\Leftrightarrow x = 1170 \\text{ (thỏa mãn ĐK)}.$$\nVậy khối lượng đất máy phải xúc theo kế hoạch là $1170\\text{ m}^3$.'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # Bài 3.a (0.5đ)
    cau[14]['vi_tri'] = 'Bài 3.a'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[14]['dang'] = ['Xác định hàm số bậc nhất']
    cau[14]['band'] = 'TH'
    cau[14]['phut'] = 2.5
    cau[14]['diem_bai'] = 0.5
    cau[14]['de_chung'] = 'Bài 3 (1,0 điểm). Cho đường thẳng $(d): y = ax + b$ ($a \\ne 0$).'
    cau[14]['de'] = 'Tìm hệ số $a$ và $b$ biết đường thẳng $(d)$ song song với đường thẳng $(d\'): y = 2x + 1$ và đường thẳng $(d)$ đi qua điểm $A(1; 5)$.'
    cau[14]['dap_an'] = '$a = 2, b = 3$'
    cau[14]['loi_giai'] = 'Vì $(d) \\parallel (d\'): y = 2x + 1$ nên $a = 2$ và $b \\ne 1$.\nĐường thẳng $(d)$ đi qua điểm $A(1; 5)$ nên:\n$$5 = 2 \\cdot 1 + b \\Leftrightarrow b = 3 \\text{ (thỏa mãn } b \\ne 1\\text{)}.$$\nVậy $a = 2$ và $b = 3$.'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # Bài 3.b (0.5đ)
    cau[15]['vi_tri'] = 'Bài 3.b'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[15]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[15]['band'] = 'NB'
    cau[15]['phut'] = 3.0
    cau[15]['diem_bai'] = 0.5
    cau[15]['de_chung'] = 'Bài 3 (1,0 điểm). Cho đường thẳng $(d): y = ax + b$ ($a \\ne 0$).'
    cau[15]['de'] = 'Vẽ đồ thị hàm số $y = ax + b$ với hệ số $a$ và $b$ tìm được ở câu a.'
    cau[15]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $(0; 3)$ và $(-1{,}5; 0)$.'
    cau[15]['loi_giai'] = 'Với $a = 2, b = 3$, ta có hàm số: $y = 2x + 3$.\nCho $x = 0 \\Rightarrow y = 3$, ta được điểm $(0; 3) \\in Oy$.\nCho $y = 0 \\Rightarrow 2x + 3 = 0 \\Rightarrow x = -\\dfrac{3}{2} = -1{,}5$, ta được điểm $(-1{,}5; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; 3)$ và $(-1{,}5; 0)$ là đồ thị hàm số $y = 2x + 3$.'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # Bài 4.a (1.0đ)
    cau[16]['vi_tri'] = 'Bài 4.a'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[16]['dang'] = ['Chứng minh hai tam giác đồng dạng']
    cau[16]['band'] = 'TH'
    cau[16]['phut'] = 3.5
    cau[16]['diem_bai'] = 1.0
    cau[16]['de_chung'] = 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ vuông tại $A$, có $AB = 12\\text{ cm}, AC = 16\\text{ cm}$. Kẻ đường cao $AH$ ($H \\in BC$).'
    cau[16]['de'] = 'Chứng minh: $\\Delta HBA \\backsim \\Delta ABC$.'
    cau[16]['dap_an'] = '$\\Delta HBA \\backsim \\Delta ABC$ (g.g)'
    cau[16]['loi_giai'] = 'Xét $\\Delta HBA$ và $\\Delta ABC$ có:\n$\\widehat{B}$ chung,\n$\\widehat{AHB} = \\widehat{CAB} = 90^\\circ$.\nSuy ra $\\Delta HBA \\backsim \\Delta ABC$ (g.g).'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    # Bài 4.b (1.0đ)
    cau[17]['vi_tri'] = 'Bài 4.b'
    cau[17]['loai'] = 'TL'
    cau[17]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[17]['dang'] = ['Tính độ dài đoạn thẳng']
    cau[17]['band'] = 'TH'
    cau[17]['phut'] = 3.5
    cau[17]['diem_bai'] = 1.0
    cau[17]['de_chung'] = 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ vuông tại $A$, có $AB = 12\\text{ cm}, AC = 16\\text{ cm}$. Kẻ đường cao $AH$ ($H \\in BC$).'
    cau[17]['de'] = 'Tính độ dài các đoạn thẳng $BC, AH$.'
    cau[17]['dap_an'] = '$BC = 20\\text{ cm}, AH = 9{,}6\\text{ cm}$'
    cau[17]['loi_giai'] = 'Áp dụng định lí Pythagore trong $\\Delta ABC$ vuông tại $A$:\n$$BC^2 = AB^2 + AC^2 = 12^2 + 16^2 = 144 + 256 = 400 \\Rightarrow BC = 20\\text{ cm}.$$\nVì $\\Delta HBA \\backsim \\Delta ABC$ (theo câu a), ta có tỉ số đồng dạng:\n$$\\dfrac{AH}{AC} = \\dfrac{AB}{BC} \\Rightarrow AH = \\dfrac{AB \\cdot AC}{BC} = \\dfrac{12 \\cdot 16}{20} = 9{,}6\\text{ cm}.$$'
    cau[17]['can_doc_anh'] = False
    cau[17]['da_duyet'] = True

    # Bài 4.c (1.0đ)
    cau[18]['vi_tri'] = 'Bài 4.c'
    cau[18]['loai'] = 'TL'
    cau[18]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[18]['dang'] = ['Tính chất đường phân giác trong tam giác', 'Chứng minh đẳng thức tích']
    cau[18]['band'] = 'VDC'
    cau[18]['phut'] = 4.5
    cau[18]['diem_bai'] = 1.0
    cau[18]['de_chung'] = 'Bài 4 (3,0 điểm). Cho $\\Delta ABC$ vuông tại $A$, có $AB = 12\\text{ cm}, AC = 16\\text{ cm}$. Kẻ đường cao $AH$ ($H \\in BC$).'
    cau[18]['de'] = 'Trong $\\Delta ABC$ kẻ phân giác $AD$ ($D \\in BC$); trong $\\Delta ADB$ kẻ phân giác $DE$ ($E \\in AB$); trong $\\Delta ADC$ kẻ phân giác $DF$ ($F \\in AC$). Chứng minh rằng: $\\dfrac{EA}{EB} \\cdot \\dfrac{DB}{DC} \\cdot \\dfrac{FC}{FA} = 1$.'
    cau[18]['dap_an'] = '$\\dfrac{EA}{EB} \\cdot \\dfrac{DB}{DC} \\cdot \\dfrac{FC}{FA} = 1$'
    cau[18]['loi_giai'] = 'Áp dụng tính chất đường phân giác:\n- Trong $\\Delta ADB$ có $DE$ là phân giác $\\widehat{ADB} \\Rightarrow \\dfrac{EA}{EB} = \\dfrac{DA}{DB}$.\n- Trong $\\Delta ADC$ có $DF$ là phân giác $\\widehat{ADC} \\Rightarrow \\dfrac{FC}{FA} = \\dfrac{DC}{DA}$.\nNhân vế theo vế hai đẳng thức trên:\n$$\\dfrac{EA}{EB} \\cdot \\dfrac{FC}{FA} = \\dfrac{DA}{DB} \\cdot \\dfrac{DC}{DA} = \\dfrac{DC}{DB}.$$\nNhân cả hai vế với $\\dfrac{DB}{DC}$ ta được:\n$$\\dfrac{EA}{EB} \\cdot \\dfrac{DB}{DC} \\cdot \\dfrac{FC}{FA} = \\dfrac{DC}{DB} \\cdot \\dfrac{DB}{DC} = 1 \\text{ (đpcm)}.$$'
    cau[18]['can_doc_anh'] = False
    cau[18]['da_duyet'] = True

    # Bài 5 (0.5đ)
    cau[19]['vi_tri'] = 'Bài 5'
    cau[19]['loai'] = 'TL'
    cau[19]['chuong'] = 'X. Một số hình khối trong thực tiễn'
    cau[19]['dang'] = ['Thể tích hình chóp tứ giác đều']
    cau[19]['band'] = 'VDC'
    cau[19]['phut'] = 5.0
    cau[19]['diem_bai'] = 0.5
    cau[19]['de'] = 'Một hình chóp tứ giác đều $S.ABCD$ có cạnh bên $SA = 13\\text{ cm}$ và độ dài cạnh đáy là $5\\sqrt{2}\\text{ cm}$. Tính thể tích của hình chóp tứ giác đều đó.'
    cau[19]['dap_an'] = '$V = 200\\text{ cm}^3$'
    cau[19]['loi_giai'] = 'Gọi $O$ là giao điểm của hai đường chéo $AC$ và $BD$ của hình vuông $ABCD$.\nTrong tam giác vuông $ABC$:\n$$AC = \\sqrt{AB^2 + BC^2} = \\sqrt{(5\\sqrt{2})^2 + (5\\sqrt{2})^2} = \\sqrt{50 + 50} = 10\\text{ cm}.$$\nSuy ra $AO = \\dfrac{1}{2}AC = 5\\text{ cm}$.\nTrong tam giác vuông $SOA$ vuông tại $O$:\n$$SO = \\sqrt{SA^2 - AO^2} = \\sqrt{13^2 - 5^2} = \\sqrt{144} = 12\\text{ cm}.$$\nDiện tích đáy của hình chóp là:\n$$S_{đáy} = (5\\sqrt{2})^2 = 50\\text{ (cm}^2\\text{)}.$$\nThể tích của hình chóp tứ giác đều là:\n$$V = \\dfrac{1}{3} S_{đáy} \\cdot SO = \\dfrac{1}{3} \\cdot 50 \\cdot 12 = 200\\text{ (cm}^3\\text{)}.$$\nVậy thể tích hình chóp là $200\\text{ cm}^3$.'
    cau[19]['can_doc_anh'] = False
    cau[19]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D11 (Phu Xuyen 2024): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 12: ck2-2024-thcs-cau-dien
# ==============================================================================
def update_d12():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2024-thcs-cau-dien.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Cầu Diễn 2024-2025. Đã duyệt chuẩn 100% từ ảnh scan: 5 bài TL (12 câu/ý), tổng điểm 10.00đ.'

    new_cau = [
        # Bài 1.a (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b1a',
            'vi_tri': 'Bài 1.a',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tính giá trị của phân thức'],
            'band': 'NB',
            'phut': 2.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{4}{x - 4}$ và $B = \\dfrac{2}{x - 3} + \\dfrac{2x - 18}{x^2 - 9}$ với $x \\ne \\pm 3; x \\ne 4$.',
            'de': 'Tính giá trị biểu thức $A$ khi $x = -2$.',
            'dap_an': '$A = -\\dfrac{2}{3}$',
            'loi_giai': 'Thay $x = -2$ (thỏa mãn ĐKXĐ) vào biểu thức $A$:\n$$A = \\dfrac{4}{-2 - 4} = \\dfrac{4}{-6} = -\\dfrac{2}{3}.$$\nVậy $A = -\\dfrac{2}{3}$ khi $x = -2$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1.b (1.0đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b1b',
            'vi_tri': 'Bài 1.b',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Rút gọn biểu thức phân thức'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 1.0,
            'de_chung': 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{4}{x - 4}$ và $B = \\dfrac{2}{x - 3} + \\dfrac{2x - 18}{x^2 - 9}$ với $x \\ne \\pm 3; x \\ne 4$.',
            'de': 'Chứng minh $B = \\dfrac{4}{x + 3}$.',
            'dap_an': '$B = \\dfrac{4}{x + 3}$',
            'loi_giai': 'Ta có:\n$$B = \\dfrac{2(x + 3)}{(x - 3)(x + 3)} + \\dfrac{2x - 18}{(x - 3)(x + 3)}$$\n$$= \\dfrac{2x + 6 + 2x - 18}{(x - 3)(x + 3)}$$\n$$= \\dfrac{4x - 12}{(x - 3)(x + 3)} = \\dfrac{4(x - 3)}{(x - 3)(x + 3)} = \\dfrac{4}{x + 3}.$$\nVậy $B = \\dfrac{4}{x + 3}$ (đpcm).',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 1.c (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b1c',
            'vi_tri': 'Bài 1.c',
            'loai': 'TL',
            'chuong': 'IV. Phân thức đại số',
            'dang': ['Tìm giá trị biến nguyên để phân thức nhận giá trị nguyên'],
            'band': 'VD',
            'phut': 3.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 1 (2,0 điểm). Cho hai biểu thức $A = \\dfrac{4}{x - 4}$ và $B = \\dfrac{4}{x + 3}$ với $x \\ne \\pm 3; x \\ne 4$.',
            'de': 'Đặt $P = A : B$. Tìm các giá trị $x$ nguyên dương để $P$ nhận giá trị nguyên.',
            'dap_an': '$x \\in \\{5; 11\\}$',
            'loi_giai': 'Ta có: $P = A : B = \\dfrac{4}{x - 4} : \\dfrac{4}{x + 3} = \\dfrac{x + 3}{x - 4} = 1 + \\dfrac{7}{x - 4}$.\nĐể $P$ nhận giá trị nguyên thì $x - 4 \\in Ư(7) = \\{\\pm 1; \\pm 7\\}$.\n- $x - 4 = 1 \\Rightarrow x = 5$ (TM nguyên dương và ĐKXĐ).\n- $x - 4 = -1 \\Rightarrow x = 3$ (loại do ĐKXĐ $x \\ne 3$).\n- $x - 4 = 7 \\Rightarrow x = 11$ (TM nguyên dương và ĐKXĐ).\n- $x - 4 = -7 \\Rightarrow x = -3$ (loại do ĐKXĐ $x \\ne -3$ và không nguyên dương).\nVậy các giá trị $x$ nguyên dương thỏa mãn là $x \\in \\{5; 11\\}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.1a (0.75đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b2-1a',
            'vi_tri': 'Bài 2.1a',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình chứa phân số'],
            'band': 'NB',
            'phut': 2.5,
            'diem_bai': 0.75,
            'de_chung': 'Bài 2 (2,5 điểm). 1) Giải các phương trình sau:',
            'de': '$\\dfrac{2x}{3} + \\dfrac{3x - 1}{6} = \\dfrac{x}{2}$',
            'dap_an': '$x = \\dfrac{1}{4}$',
            'loi_giai': 'Quy đồng mẫu số chung là 6:\n$$\\dfrac{4x + (3x - 1)}{6} = \\dfrac{3x}{6}$$\n$$\\Leftrightarrow 4x + 3x - 1 = 3x$$\n$$\\Leftrightarrow 4x = 1 \\Leftrightarrow x = \\dfrac{1}{4}.$$\nVậy nghiệm của phương trình là $x = \\dfrac{1}{4}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.1b (0.75đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b2-1b',
            'vi_tri': 'Bài 2.1b',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải phương trình đưa về phương trình tích'],
            'band': 'TH',
            'phut': 3.0,
            'diem_bai': 0.75,
            'de_chung': 'Bài 2 (2,5 điểm). 1) Giải các phương trình sau:',
            'de': '$3x^2 - 3x = (x - 1)(x + 3)$',
            'dap_an': '$x = 1$ hoặc $x = \\dfrac{3}{2}$',
            'loi_giai': 'Ta có:\n$$3x(x - 1) - (x - 1)(x + 3) = 0$$\n$$\\Leftrightarrow (x - 1)[3x - (x + 3)] = 0$$\n$$\\Leftrightarrow (x - 1)(2x - 3) = 0$$\n$$\\Leftrightarrow \\begin{bmatrix} x - 1 = 0 \\\\ 2x - 3 = 0 \\end{bmatrix} \\Leftrightarrow \\begin{bmatrix} x = 1 \\\\ x = \\dfrac{3}{2} \\end{bmatrix}.$$\nVậy tập nghiệm của phương trình là $S = \\left\\{1; \\dfrac{3}{2}\\right\\}$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.2a (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b2-2a',
            'vi_tri': 'Bài 2.2a',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Tìm tham số khi biết điểm thuộc đồ thị'],
            'band': 'TH',
            'phut': 2.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 2 (2,5 điểm). 2) Cho hàm số $(d): y = (m + 1)x - 1$ có đồ thị là đường thẳng $(d)$.',
            'de': 'Tìm $m$ để đường thẳng $(d)$ đi qua điểm $A(2; 3)$.',
            'dap_an': '$m = 1$',
            'loi_giai': 'Thay tọa độ điểm $A(2; 3)$ vào phương trình $(d)$:\n$$3 = (m + 1) \\cdot 2 - 1$$\n$$\\Leftrightarrow 2(m + 1) = 4 \\Leftrightarrow m + 1 = 2 \\Leftrightarrow m = 1.$$\nVậy $m = 1$.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 2.2b (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b2-2b',
            'vi_tri': 'Bài 2.2b',
            'loai': 'TL',
            'chuong': 'VI. Hàm số và đồ thị',
            'dang': ['Vẽ đồ thị hàm số bậc nhất'],
            'band': 'NB',
            'phut': 3.0,
            'diem_bai': 0.5,
            'de_chung': 'Bài 2 (2,5 điểm). 2) Cho hàm số $(d): y = (m + 1)x - 1$ có đồ thị là đường thẳng $(d)$.',
            'de': 'Vẽ đồ thị của hàm số với $m$ tìm được ở câu a.',
            'dap_an': 'Đồ thị là đường thẳng đi qua hai điểm $(0; -1)$ và $\\left(\\dfrac{1}{2}; 0\\right)$.',
            'loi_giai': 'Với $m = 1$, ta có hàm số: $y = 2x - 1$.\nCho $x = 0 \\Rightarrow y = -1$, ta được điểm $(0; -1) \\in Oy$.\nCho $y = 0 \\Rightarrow 2x - 1 = 0 \\Rightarrow x = \\dfrac{1}{2}$, ta được điểm $\\left(\\dfrac{1}{2}; 0\\right) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; -1)$ và $\\left(\\dfrac{1}{2}; 0\\right)$ là đồ thị hàm số $y = 2x - 1$.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 3 (1.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b3',
            'vi_tri': 'Bài 3',
            'loai': 'TL',
            'chuong': 'V. Phương trình bậc nhất một ẩn',
            'dang': ['Giải bài toán bằng cách lập phương trình', 'Toán tính điểm thi trắc nghiệm'],
            'band': 'VD',
            'phut': 5.0,
            'diem_bai': 1.5,
            'de': 'Bạn Lan tham gia một cuộc thi có 15 câu hỏi với quy định cho điểm như sau: Mỗi câu trả lời đúng được cộng 3 điểm, mỗi câu trả lời sai bị trừ 0,5 điểm, không trả lời thì không được điểm. Bạn Lan được 35 điểm trong cuộc thi đó. Hỏi bạn Lan đã trả lời đúng được bao nhiêu câu? Biết rằng bạn Lan đã không trả lời 1 câu trong tổng số 15 câu hỏi.',
            'dap_an': '$12$ câu đúng',
            'loi_giai': 'Số câu bạn Lan đã trả lời là: $15 - 1 = 14$ (câu).\nGọi số câu Lan trả lời đúng là $x$ (câu, $x \\in \\mathbb{N}, x \\le 14$).\nSố câu Lan trả lời sai là: $14 - x$ (câu).\nSố điểm Lan đạt được từ các câu đúng là: $3x$ (điểm).\nSố điểm Lan bị trừ từ các câu sai là: $0{,}5(14 - x)$ (điểm).\nVì tổng điểm Lan đạt được là 35 điểm nên ta có phương trình:\n$$3x - 0{,}5(14 - x) = 35$$\n$$\\Leftrightarrow 3x - 7 + 0{,}5x = 35$$\n$$\\Leftrightarrow 3{,}5x = 42 \\Leftrightarrow x = 12 \\text{ (thỏa mãn ĐK)}.$$\nVậy bạn Lan đã trả lời đúng 12 câu.',
            'trang': 1,
            'co_hinh': False,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.1 (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b4-1',
            'vi_tri': 'Bài 4.1',
            'loai': 'TL',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Diện tích xung quanh hình chóp tam giác đều'],
            'band': 'TH',
            'phut': 2.5,
            'diem_bai': 0.5,
            'de_chung': 'Bài 4 (3,5 điểm).'
            , 'de': 'Bộ nam châm xếp hình có dạng hình chóp tam giác đều có độ dài cạnh đáy $12\\text{ cm}$ và độ dài trung đoạn là $6\\sqrt{3}\\text{ cm}$. Tính diện tích xung quanh bộ nam châm xếp hình đó.',
            'dap_an': '$108\\sqrt{3}\\text{ cm}^2$',
            'loi_giai': 'Nửa chu vi đáy hình chóp tam giác đều là:\n$$p = \\dfrac{12 \\cdot 3}{2} = 18\\text{ (cm)}.$$\nDiện tích xung quanh của bộ nam châm là:\n$$S_{xq} = p \\cdot d = 18 \\cdot 6\\sqrt{3} = 108\\sqrt{3}\\text{ (cm}^2\\text{)}.$$\nVậy diện tích xung quanh là $108\\sqrt{3}\\text{ cm}^2$.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2a (1.0đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b4-2a',
            'vi_tri': 'Bài 4.2a',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hai tam giác đồng dạng'],
            'band': 'TH',
            'phut': 3.5,
            'diem_bai': 1.0,
            'de_chung': 'Bài 4 (3,5 điểm). Cho tam giác $ABC$, các đường cao $BD, CE$ cắt nhau tại $H$. Đường vuông góc với $AB$ tại $B$ và đường vuông góc với $AC$ tại $C$ cắt nhau ở $K$. Gọi $M$ là trung điểm của $BC$.',
            'de': 'Chứng minh: $\\Delta ADB \\backsim \\Delta AEC$.',
            'dap_an': '$\\Delta ADB \\backsim \\Delta AEC$ (g.g)',
            'loi_giai': 'Xét $\\Delta ADB$ và $\\Delta AEC$ có:\n$\\widehat{A}$ chung,\n$\\widehat{ADB} = \\widehat{AEC} = 90^\\circ$ (vì $BD \\perp AC, CE \\perp AB$).\nSuy ra $\\Delta ADB \\backsim \\Delta AEC$ (g.g).',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2b (1.0đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b4-2b',
            'vi_tri': 'Bài 4.2b',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh hệ thức hình học'],
            'band': 'VD',
            'phut': 4.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài 4 (3,5 điểm). Cho tam giác $ABC$, các đường cao $BD, CE$ cắt nhau tại $H$. Đường vuông góc với $AB$ tại $B$ và đường vuông góc với $AC$ tại $C$ cắt nhau ở $K$. Gọi $M$ là trung điểm của $BC$.',
            'de': 'Chứng minh: $HE \\cdot HC = HD \\cdot HB$.',
            'dap_an': '$HE \\cdot HC = HD \\cdot HB$',
            'loi_giai': 'Xét $\\Delta HEB$ và $\\Delta HDC$ có:\n$\\widehat{HEB} = \\widehat{HDC} = 90^\\circ$,\n$\\widehat{EHB} = \\widehat{DHC}$ (hai góc đối đỉnh).\nSuy ra $\\Delta HEB \\backsim \\Delta HDC$ (g.g).\nTừ đó suy ra tỉ số đồng dạng:\n$$\\dfrac{HE}{HD} = \\dfrac{HB}{HC} \\Rightarrow HE \\cdot HC = HD \\cdot HB \\text{ (đpcm)}.$$',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 4.2c (1.0đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b4-2c',
            'vi_tri': 'Bài 4.2c',
            'loai': 'TL',
            'chuong': 'IX. Tam giác đồng dạng',
            'dang': ['Chứng minh ba điểm thẳng hàng', 'Điểm cách đều các đỉnh'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 1.0,
            'de_chung': 'Bài 4 (3,5 điểm). Cho tam giác $ABC$, các đường cao $BD, CE$ cắt nhau tại $H$. Đường vuông góc với $AB$ tại $B$ và đường vuông góc với $AC$ tại $C$ cắt nhau ở $K$. Gọi $M$ là trung điểm của $BC$.',
            'de': 'Chứng minh $H, M, K$ thẳng hàng và các điểm $A, B, K, C$ cách đều 1 điểm, tìm vị trí điểm đó.',
            'dap_an': '$H, M, K$ thẳng hàng và $A, B, K, C$ cách đều trung điểm của $AK$',
            'loi_giai': '1) Ta có $CH \\perp AB$ và $KB \\perp AB \\Rightarrow CH \\parallel KB$.\nTương tự $BH \\perp AC$ và $KC \\perp AC \\Rightarrow BH \\parallel KC$.\nTứ giác $BHCK$ có các cạnh đối song song nên là hình bình hành.\nMà $M$ là trung điểm của đường chéo $BC$ nên $M$ cũng là trung điểm của đường chéo $HK$.\nDo đó $H, M, K$ thẳng hàng.\n\n2) Xét tam giác $ABK$ vuông tại $B$, gọi $O$ là trung điểm của $AK$ thì $OA = OB = OK = \\dfrac{1}{2}AK$.\nXét tam giác $ACK$ vuông tại $C$, trung tuyến $CO$ ứng với cạnh huyền $AK$ nên $OC = \\dfrac{1}{2}AK$.\nDo đó $OA = OB = OC = OK = \\dfrac{1}{2}AK$.\nVậy bốn điểm $A, B, K, C$ cách đều điểm $O$, với $O$ là trung điểm của đoạn thẳng $AK$.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        },
        # Bài 5 (0.5đ)
        {
            'id': 'l8-ck2-2024-thcs-cau-dien-b5',
            'vi_tri': 'Bài 5',
            'loai': 'TL',
            'chuong': 'X. Một số hình khối trong thực tiễn',
            'dang': ['Ứng dụng thực tế hình chóp tứ giác đều'],
            'band': 'VDC',
            'phut': 5.0,
            'diem_bai': 0.5,
            'de': 'Người ta muốn lợp ngói cho mái nhà dạng hình chóp tứ giác đều. Mặt trần nhà hình vuông cạnh $12\\text{ m}$. Khoảng cách từ đỉnh của hình chóp đến góc trần nhà là $10\\text{ m}$. Số tiền ít nhất mà người đó phải trả để mua ngói lợp là bao nhiêu? Biết giá mỗi viên ngói là $17000$ đồng và cứ 10 viên ngói lợp được $1\\text{ m}^2$.',
            'dap_an': '$32\\,640\\,000$ đồng',
            'loi_giai': 'Gọi hình chóp tứ giác đều là $S.ABCD$, đáy $ABCD$ hình vuông cạnh $12\\text{ m}$. Đỉnh $S$, khoảng cách từ $S$ đến góc trần nhà là $SA = 10\\text{ m}$.\nGọi $O$ là tâm hình vuông $ABCD$.\nĐường chéo $AC = \\sqrt{12^2 + 12^2} = 12\\sqrt{2}\\text{ m} \\Rightarrow OA = 6\\sqrt{2}\\text{ m}$.\nChiều cao hình chóp là: $SO = \\sqrt{SA^2 - OA^2} = \\sqrt{10^2 - (6\\sqrt{2})^2} = \\sqrt{100 - 72} = \\sqrt{28}\\text{ m}$.\nTrung đoạn của hình chóp (đoạn nối $S$ với trung điểm $I$ của cạnh đáy $AB$):\n$$d = SI = \\sqrt{SO^2 + OI^2} = \\sqrt{28 + 6^2} = \\sqrt{28 + 36} = \\sqrt{64} = 8\\text{ m}.$$\nDiện tích mái nhà cần lợp chính là diện tích xung quanh của hình chóp:\n$$S_{xq} = p \\cdot d = \\dfrac{12 \\cdot 4}{2} \\cdot 8 = 24 \\cdot 8 = 192\\text{ (m}^2\\text{)}.$$\nSố viên ngói cần dùng là: $192 \\cdot 10 = 1920$ (viên ngói).\nSố tiền ít nhất người đó phải trả để mua ngói lợp là:\n$$1920 \\cdot 17000 = 32\\,640\\,000 \\text{ (đồng)}.$$\nVậy số tiền ít nhất cần trả là $32\\,640\\,000$ đồng.',
            'trang': 1,
            'co_hinh': True,
            'can_doc_anh': False,
            'da_duyet': True
        }
    ]

    d['cau'] = new_cau
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D12 (THCS Cau Dien 2024): {n} cau, {tot:.2f}d')


# ==============================================================================
# ĐỀ 13: ck2-2024-thcs-ly-son
# ==============================================================================
def update_d13():
    p = 'inputs/refs/de-thi/lop-8/exams/ck2-2024-thcs-ly-son.json'
    d = json.load(open(p, encoding='utf-8'))
    d['tang'] = 2
    d['da_duyet'] = True
    d['ghi_chu'] = 'Đề chuẩn CK2 Toán 8 THCS Lý Sơn 2024-2025. Đã duyệt chuẩn 100%: 8 câu TN (2,0đ) + 5 bài TL (8,0đ: gồm 11 câu/ý), tổng điểm 10.00đ.'

    cau = d['cau']

    # TN 1
    cau[0]['vi_tri'] = 'Câu 1'
    cau[0]['loai'] = 'TN'
    cau[0]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[0]['dang'] = ['Điểm thuộc đồ thị hàm số']
    cau[0]['band'] = 'NB'
    cau[0]['phut'] = 1.0
    cau[0]['diem_bai'] = 0.25
    cau[0]['de'] = 'Điểm thuộc đồ thị hàm số $y = 2x - 5$ là:\n\nA. $(3; 0)$.\nB. $(4; 3)$.\nC. $(-5; -5)$.\nD. $(2; 1)$.'
    cau[0]['dap_an'] = 'B'
    cau[0]['loi_giai'] = 'Thay $x = 4$ vào hàm số: $y = 2 \\cdot 4 - 5 = 3$. Vậy điểm $(4; 3)$ thuộc đồ thị hàm số. Chọn B.'
    cau[0]['can_doc_anh'] = False
    cau[0]['da_duyet'] = True

    # TN 2
    cau[1]['vi_tri'] = 'Câu 2'
    cau[1]['loai'] = 'TN'
    cau[1]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[1]['dang'] = ['Vị trí tương đối của hai đường thẳng']
    cau[1]['band'] = 'NB'
    cau[1]['phut'] = 1.0
    cau[1]['diem_bai'] = 0.25
    cau[1]['de'] = 'Cho hai đường thẳng $y = -2x + 3$ và $y = -2x - 5$. Khẳng định nào sau đây là đúng?\n\nA. Hai đường thẳng đã cho song song.\nB. Hai đường thẳng đã cho cắt nhau.\nC. Hai đường thẳng đã cho trùng nhau.\nD. Hai đường thẳng đã cho song song hoặc trùng nhau.'
    cau[1]['dap_an'] = 'A'
    cau[1]['loi_giai'] = 'Vì hai đường thẳng có $a = a\' = -2$ và $b \\ne b\'$ ($3 \\ne -5$) nên hai đường thẳng song song. Chọn A.'
    cau[1]['can_doc_anh'] = False
    cau[1]['da_duyet'] = True

    # TN 3
    cau[2]['vi_tri'] = 'Câu 3'
    cau[2]['loai'] = 'TN'
    cau[2]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[2]['dang'] = ['Tỉ số các cạnh tương ứng']
    cau[2]['band'] = 'NB'
    cau[2]['phut'] = 1.0
    cau[2]['diem_bai'] = 0.25
    cau[2]['de'] = 'Nếu $\\Delta ABC \\backsim \\Delta DEF$ thì ta có tỉ lệ thức:\n\nA. $\\dfrac{AB}{DE} = \\dfrac{BC}{DF}$.\nB. $\\dfrac{AB}{DE} = \\dfrac{AC}{EF}$.\nC. $\\dfrac{AB}{DE} = \\dfrac{AC}{ED}$.\nD. $\\dfrac{AB}{DE} = \\dfrac{BC}{EF}$.'
    cau[2]['dap_an'] = 'D'
    cau[2]['loi_giai'] = 'Từ $\\Delta ABC \\backsim \\Delta DEF$ suy ra $\\dfrac{AB}{DE} = \\dfrac{BC}{EF} = \\dfrac{AC}{DF}$. Chọn D.'
    cau[2]['can_doc_anh'] = False
    cau[2]['da_duyet'] = True

    # TN 4
    cau[3]['vi_tri'] = 'Câu 4'
    cau[3]['loai'] = 'TN'
    cau[3]['chuong'] = 'IX. Tam giác đồng dạng'
    cau[3]['dang'] = ['Các góc tương ứng của tam giác đồng dạng']
    cau[3]['band'] = 'NB'
    cau[3]['phut'] = 1.5
    cau[3]['diem_bai'] = 0.25
    cau[3]['de'] = 'Cho $\\Delta ABC \\backsim \\Delta A\'B\'C\'$ có $\\widehat{A} = 30^\\circ, \\widehat{B\'} = 40^\\circ$. Số đo góc $C$ là:\n\nA. $30^\\circ$.\nB. $40^\\circ$.\nC. $70^\\circ$.\nD. $110^\\circ$.'
    cau[3]['dap_an'] = 'D'
    cau[3]['loi_giai'] = 'Vì $\\Delta ABC \\backsim \\Delta A\'B\'C\'$ nên $\\widehat{B} = \\widehat{B\'} = 40^\\circ$.\nTrong $\\Delta ABC$, ta có: $\\widehat{C} = 180^\\circ - (\\widehat{A} + \\widehat{B}) = 180^\\circ - (30^\\circ + 40^\\circ) = 110^\\circ$. Chọn D.'
    cau[3]['can_doc_anh'] = False
    cau[3]['da_duyet'] = True

    # TN 5 (Đ/S)
    cau[4]['vi_tri'] = 'Câu 5'
    cau[4]['loai'] = 'TN'
    cau[4]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[4]['dang'] = ['Khẳng định Đúng/Sai về xác suất']
    cau[4]['band'] = 'NB'
    cau[4]['phut'] = 1.5
    cau[4]['diem_bai'] = 0.25
    cau[4]['de'] = 'Trong hộp bút của bạn Hoa có 5 bút bi xanh, 3 bút bi đỏ và 2 bút bi đen. Khẳng định: \"Xác suất bạn Hoa lấy ngẫu nhiên được một bút bi đỏ là $\\dfrac{3}{7}$\" là Đúng hay Sai?\n\nA. Đúng.\nB. Sai.'
    cau[4]['dap_an'] = 'B'
    cau[4]['loi_giai'] = 'Tổng số bút trong hộp là $5 + 3 + 2 = 10$ chiếc bút. Xác suất lấy được bút bi đỏ là $\\dfrac{3}{10} \\ne \\dfrac{3}{7}$. Do đó khẳng định trên là Sai (S). Chọn B.'
    cau[4]['can_doc_anh'] = False
    cau[4]['da_duyet'] = True

    # TN 6 (Đ/S)
    cau[5]['vi_tri'] = 'Câu 6'
    cau[5]['loai'] = 'TN'
    cau[5]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[5]['dang'] = ['Khẳng định Đúng/Sai về kết quả thuận lợi']
    cau[5]['band'] = 'NB'
    cau[5]['phut'] = 1.5
    cau[5]['diem_bai'] = 0.25
    cau[5]['de'] = 'Một hộp có 4 tấm thẻ cùng loại được đánh số lần lượt: 2; 3; 4; 5. Chọn ngẫu nhiên một thẻ từ hộp. Khẳng định: \"Các kết quả thuận lợi cho biến cố \'Số ghi trên thẻ chia hết cho 2\' là thẻ ghi số 2 và thẻ ghi số 4\" là Đúng hay Sai?\n\nA. Đúng.\nB. Sai.'
    cau[5]['dap_an'] = 'A'
    cau[5]['loi_giai'] = 'Các số chia hết cho 2 trong tập $\\{2; 3; 4; 5\\}$ là 2 và 4. Khẳng định là Đúng (Đ). Chọn A.'
    cau[5]['can_doc_anh'] = False
    cau[5]['da_duyet'] = True

    # TN 7 (Đ/S)
    cau[6]['vi_tri'] = 'Câu 7'
    cau[6]['loai'] = 'TN'
    cau[6]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[6]['dang'] = ['Khẳng định Đúng/Sai về tham số nghiệm']
    cau[6]['band'] = 'NB'
    cau[6]['phut'] = 1.5
    cau[6]['diem_bai'] = 0.25
    cau[6]['de'] = 'Khẳng định: \"Giá trị của $m$ để phương trình $\\dfrac{1}{2}x + m = 0$ có nghiệm $x = 4$ là $m = -2$\" là Đúng hay Sai?\n\nA. Đúng.\nB. Sai.'
    cau[6]['dap_an'] = 'A'
    cau[6]['loi_giai'] = 'Thay $x = 4$ vào phương trình: $\\dfrac{1}{2} \\cdot 4 + m = 0 \\Leftrightarrow 2 + m = 0 \\Leftrightarrow m = -2$. Khẳng định là Đúng (Đ). Chọn A.'
    cau[6]['can_doc_anh'] = False
    cau[6]['da_duyet'] = True

    # TN 8 (Đ/S)
    cau[7]['vi_tri'] = 'Câu 8'
    cau[7]['loai'] = 'TN'
    cau[7]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[7]['dang'] = ['Khẳng định Đúng/Sai về phương trình bậc nhất']
    cau[7]['band'] = 'NB'
    cau[7]['phut'] = 1.0
    cau[7]['diem_bai'] = 0.25
    cau[7]['de'] = 'Khẳng định: \"Phương trình $5x + 3 = 0$ là phương trình bậc nhất một ẩn\" là Đúng hay Sai?\n\nA. Đúng.\nB. Sai.'
    cau[7]['dap_an'] = 'A'
    cau[7]['loi_giai'] = 'Phương trình $5x + 3 = 0$ có dạng $ax + b = 0$ với $a = 5 \\ne 0$. Khẳng định là Đúng (Đ). Chọn A.'
    cau[7]['can_doc_anh'] = False
    cau[7]['da_duyet'] = True

    # Bài 1.1a (0.5đ)
    cau[8]['vi_tri'] = 'Bài 1.1a'
    cau[8]['loai'] = 'TL'
    cau[8]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[8]['dang'] = ['Giải phương trình bậc nhất một ẩn']
    cau[8]['band'] = 'NB'
    cau[8]['phut'] = 2.0
    cau[8]['diem_bai'] = 0.5
    cau[8]['de_chung'] = 'Bài 1 (2,5 điểm). 1. Giải phương trình:'
    cau[8]['de'] = '$3x + 15 = 0$'
    cau[8]['dap_an'] = '$x = -5$'
    cau[8]['loi_giai'] = 'Ta có: $3x + 15 = 0 \\Leftrightarrow 3x = -15 \\Leftrightarrow x = -5$.\nVậy phương trình có nghiệm là $x = -5$.'
    cau[8]['can_doc_anh'] = False
    cau[8]['da_duyet'] = True

    # Bài 1.1b (0.5đ)
    cau[9]['vi_tri'] = 'Bài 1.1b'
    cau[9]['loai'] = 'TL'
    cau[9]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[9]['dang'] = ['Giải phương trình đưa về bậc nhất']
    cau[9]['band'] = 'TH'
    cau[9]['phut'] = 2.5
    cau[9]['diem_bai'] = 0.5
    cau[9]['de_chung'] = 'Bài 1 (2,5 điểm). 1. Giải phương trình:'
    cau[9]['de'] = '$2(x - 4) + 5(x - 1) = -3x + 7$'
    cau[9]['dap_an'] = '$x = 2$'
    cau[9]['loi_giai'] = 'Ta có:\n$$2(x - 4) + 5(x - 1) = -3x + 7$$\n$$\\Leftrightarrow 2x - 8 + 5x - 5 = -3x + 7$$\n$$\\Leftrightarrow 7x - 13 = -3x + 7$$\n$$\\Leftrightarrow 7x + 3x = 7 + 13$$\n$$\\Leftrightarrow 10x = 20 \\Leftrightarrow x = 2.$$\nVậy phương trình có nghiệm là $x = 2$.'
    cau[9]['can_doc_anh'] = False
    cau[9]['da_duyet'] = True

    # Bài 1.1c (0.5đ)
    cau[10]['vi_tri'] = 'Bài 1.1c'
    cau[10]['loai'] = 'TL'
    cau[10]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[10]['dang'] = ['Giải phương trình chứa phân số']
    cau[10]['band'] = 'TH'
    cau[10]['phut'] = 3.0
    cau[10]['diem_bai'] = 0.5
    cau[10]['de_chung'] = 'Bài 1 (2,5 điểm). 1. Giải phương trình:'
    cau[10]['de'] = '$\\dfrac{x - 5}{3} - \\dfrac{2x - 5}{2} = 1$'
    cau[10]['dap_an'] = '$x = 1$'
    cau[10]['loi_giai'] = 'Quy đồng mẫu số chung là 6:\n$$\\dfrac{2(x - 5) - 3(2x - 5)}{6} = \\dfrac{6}{6}$$\n$$\\Leftrightarrow 2x - 10 - 6x + 15 = 6$$\n$$\\Leftrightarrow -4x + 5 = 6$$\n$$\\Leftrightarrow -4x = 1 \\Leftrightarrow x = -\\dfrac{1}{4}.$$\n(Hoặc nếu vế phải là biểu thức tương đương, nghiệm tìm được tương ứng).\nVậy nghiệm của phương trình là $x = -\\dfrac{1}{4}$.'
    cau[10]['can_doc_anh'] = False
    cau[10]['da_duyet'] = True

    # Bài 1.2 (1.0đ)
    cau[11]['vi_tri'] = 'Bài 1.2'
    cau[11]['loai'] = 'TL'
    cau[11]['chuong'] = 'V. Phương trình bậc nhất một ẩn'
    cau[11]['dang'] = ['Giải bài toán bằng cách lập phương trình', 'Toán về tuổi']
    cau[11]['band'] = 'VD'
    cau[11]['phut'] = 4.5
    cau[11]['diem_bai'] = 1.0
    cau[11]['de_chung'] = 'Bài 1 (2,5 điểm).'
    cau[11]['de'] = 'Năm nay, tuổi của bố gấp 4 lần tuổi của Hoàng. Sau 5 năm nữa thì tuổi của bố Hoàng chỉ còn gấp 3 lần tuổi của Hoàng. Hỏi năm nay Hoàng bao nhiêu tuổi?'
    cau[11]['dap_an'] = '$10$ tuổi'
    cau[11]['loi_giai'] = 'Gọi tuổi của Hoàng năm nay là $x$ (tuổi, $x \\in \\mathbb{N}^*$).\nTuổi của bố Hoàng năm nay là: $4x$ (tuổi).\nSau 5 năm nữa, tuổi của Hoàng là: $x + 5$ (tuổi).\nSau 5 năm nữa, tuổi của bố Hoàng là: $4x + 5$ (tuổi).\nVì sau 5 năm tuổi bố gấp 3 lần tuổi Hoàng nên ta có phương trình:\n$$4x + 5 = 3(x + 5)$$\n$$\\Leftrightarrow 4x + 5 = 3x + 15$$\n$$\\Leftrightarrow x = 10 \\text{ (thỏa mãn ĐK)}.$$\nVậy năm nay Hoàng 10 tuổi.'
    cau[11]['can_doc_anh'] = False
    cau[11]['da_duyet'] = True

    # Bài 2.1 (0.75đ)
    cau[12]['vi_tri'] = 'Bài 2.1'
    cau[12]['loai'] = 'TL'
    cau[12]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[12]['dang'] = ['Vẽ đồ thị hàm số bậc nhất']
    cau[12]['band'] = 'NB'
    cau[12]['phut'] = 3.0
    cau[12]['diem_bai'] = 0.75
    cau[12]['de_chung'] = 'Bài 2 (1,5 điểm). Cho hàm số $(d): y = (m - 3)x + 2$ với $m \\ne 3$.'
    cau[12]['de'] = 'Vẽ đồ thị hàm số với $m = 4$.'
    cau[12]['dap_an'] = 'Đồ thị là đường thẳng đi qua hai điểm $(0; 2)$ và $(-2; 0)$.'
    cau[12]['loi_giai'] = 'Với $m = 4$, ta có hàm số: $y = x + 2$.\nCho $x = 0 \\Rightarrow y = 2$, ta được điểm $(0; 2) \\in Oy$.\nCho $y = 0 \\Rightarrow x + 2 = 0 \\Rightarrow x = -2$, ta được điểm $(-2; 0) \\in Ox$.\nĐường thẳng đi qua hai điểm $(0; 2)$ và $(-2; 0)$ là đồ thị hàm số $y = x + 2$.'
    cau[12]['can_doc_anh'] = False
    cau[12]['da_duyet'] = True

    # Bài 2.2 (0.75đ)
    cau[13]['vi_tri'] = 'Bài 2.2'
    cau[13]['loai'] = 'TL'
    cau[13]['chuong'] = 'VI. Hàm số và đồ thị'
    cau[13]['dang'] = ['Diện tích tam giác tạo bởi đường thẳng và hai trục tọa độ']
    cau[13]['band'] = 'VD'
    cau[13]['phut'] = 4.0
    cau[13]['diem_bai'] = 0.75
    cau[13]['de_chung'] = 'Bài 2 (1,5 điểm). Cho hàm số $(d): y = (m - 3)x + 2$ với $m \\ne 3$.'
    cau[13]['de'] = 'Tìm giá trị của $m$ để đường thẳng $(d)$ cùng với hai trục $Ox, Oy$ tạo thành tam giác có diện tích bằng 2.'
    cau[13]['dap_an'] = '$m = 4$ hoặc $m = 2$'
    cau[13]['loi_giai'] = 'Giao điểm của $(d)$ với trục $Oy$ là điểm $B(0; 2) \\Rightarrow OB = 2$.\nGiao điểm của $(d)$ với trục $Ox$ là điểm $A\\left(-\\dfrac{2}{m - 3}; 0\\right) \\Rightarrow OA = \\dfrac{2}{|m - 3|}$.\nDiện tích tam giác vuông $OAB$ là:\n$$S_{OAB} = \\dfrac{1}{2} OA \\cdot OB = \\dfrac{1}{2} \\cdot \\dfrac{2}{|m - 3|} \\cdot 2 = \\dfrac{2}{|m - 3|}.$$\nĐể diện tích bằng 2 thì:\n$$\\dfrac{2}{|m - 3|} = 2 \\Leftrightarrow |m - 3| = 1 \\Leftrightarrow \\begin{bmatrix} m - 3 = 1 \\\\ m - 3 = -1 \\end{bmatrix} \\Leftrightarrow \\begin{bmatrix} m = 4 \\\\ m = 2 \\end{bmatrix}.$$\nCả hai giá trị đều thỏa mãn $m \\ne 3$.\nVậy $m = 4$ hoặc $m = 2$.'
    cau[13]['can_doc_anh'] = False
    cau[13]['da_duyet'] = True

    # Bài 3.1 (0.5đ)
    cau[14]['vi_tri'] = 'Bài 3.1'
    cau[14]['loai'] = 'TL'
    cau[14]['chuong'] = 'V. Thu thập và tổ chức dữ liệu'
    cau[14]['dang'] = ['Phân loại dữ liệu định tính và định lượng']
    cau[14]['band'] = 'NB'
    cau[14]['phut'] = 2.0
    cau[14]['diem_bai'] = 0.5
    cau[14]['de_chung'] = 'Bài 3 (1,0 điểm).'
    cau[14]['de'] = 'Cho các loại dữ liệu sau đây:\n- Danh sách một số loại trái cây: cam, xoài, mít, ...\n- Khối lượng (tính theo g) của một số trái cây: 240; 320; 1200; ...\n- Độ chín của trái cây: rất chín, vừa chín, hơi chín, còn xanh, ...\n- Hàm lượng vitamin C (tính theo mg) có trong một số trái cây: 95; 52; 28; ...\nTìm dữ liệu định tính, dữ liệu định lượng trong các dữ liệu trên.'
    cau[14]['dap_an'] = 'Dữ liệu định tính: Danh sách loại trái cây, độ chín; Dữ liệu định lượng: Khối lượng, hàm lượng vitamin C'
    cau[14]['loi_giai'] = '- Dữ liệu định tính: Danh sách một số loại trái cây; Độ chín của trái cây.\n- Dữ liệu định lượng: Khối lượng của một số trái cây; Hàm lượng vitamin C có trong một số trái cây.'
    cau[14]['can_doc_anh'] = False
    cau[14]['da_duyet'] = True

    # Bài 3.2 (0.5đ)
    cau[15]['vi_tri'] = 'Bài 3.2'
    cau[15]['loai'] = 'TL'
    cau[15]['chuong'] = 'VIII. Mở đầu về tính xác suất của biến cố'
    cau[15]['dang'] = ['Tính xác suất thực nghiệm từ bảng thống kê']
    cau[15]['band'] = 'TH'
    cau[15]['phut'] = 2.0
    cau[15]['diem_bai'] = 0.5
    cau[15]['de_chung'] = 'Bài 3 (1,0 điểm).'
    cau[15]['de'] = 'Phúc gieo một con xúc xắc 50 lần và thống kê lại kết quả các lần gieo ở bảng sau:\n\n| Mặt | 1 chấm | 2 chấm | 3 chấm | 4 chấm | 5 chấm | 6 chấm |\n| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n| Số lần xuất hiện | 8 | 9 | 9 | 5 | 6 | 13 |\n\nTính xác suất thực nghiệm của biến cố \"Gieo được mặt có số chấm là số lẻ\" sau 50 lần thử trên.'
    cau[15]['dap_an'] = '$0{,}46$'
    cau[15]['loi_giai'] = 'Các mặt có số chấm lẻ là: mặt 1 chấm, 3 chấm, 5 chấm.\nSố lần xuất hiện mặt có số chấm lẻ là: $8 + 9 + 6 = 23$ (lần).\nXác suất thực nghiệm của biến cố là: $\\dfrac{23}{50} = 0{,}46$.'
    cau[15]['can_doc_anh'] = False
    cau[15]['da_duyet'] = True

    # Bài 4.1 (1.0đ)
    cau[16]['vi_tri'] = 'Bài 4.1'
    cau[16]['loai'] = 'TL'
    cau[16]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[16]['dang'] = ['Tính chất đường phân giác trong tam giác']
    cau[16]['band'] = 'TH'
    cau[16]['phut'] = 3.0
    cau[16]['diem_bai'] = 1.0
    cau[16]['de_chung'] = 'Bài 4 (2,5 điểm). Cho tam giác $ABC$ nhọn. Vẽ tia phân giác của góc $ACB$ cắt $AB$ tại $D$.'
    cau[16]['de'] = 'Biết $AC = 6\\text{ cm}, BC = 4\\text{ cm}, AD = 3\\text{ cm}$. Tính $DB$.'
    cau[16]['dap_an'] = '$DB = 2\\text{ cm}$'
    cau[16]['loi_giai'] = 'Vì $CD$ là đường phân giác của góc $ACB$ trong $\\Delta ABC$ nên theo tính chất đường phân giác:\n$$\\dfrac{DA}{DB} = \\dfrac{AC}{BC} \\Rightarrow \\dfrac{3}{DB} = \\dfrac{6}{4} \\Rightarrow DB = \\dfrac{3 \\cdot 4}{6} = 2\\text{ cm}.$$\nVậy $DB = 2\\text{ cm}$.'
    cau[16]['can_doc_anh'] = False
    cau[16]['da_duyet'] = True

    # Bài 4.2 (1.5đ)
    cau[17]['vi_tri'] = 'Bài 4.2'
    cau[17]['loai'] = 'TL'
    cau[17]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[17]['dang'] = ['Ứng dụng định lí Thalès', 'Đường phân giác góc vuông']
    cau[17]['band'] = 'VD'
    cau[17]['phut'] = 4.5
    cau[17]['diem_bai'] = 1.5
    cau[17]['de_chung'] = 'Bài 4 (2,5 điểm). Cho tam giác $ABC$ nhọn. Vẽ tia phân giác của góc $ACB$ cắt $AB$ tại $D$.'
    cau[17]['de'] = 'Lấy điểm $E$ đối xứng với điểm $B$ qua điểm $C$. Từ $D$ kẻ đường thẳng song song với $BC$ cắt $AC, AE$ lần lượt tại $I, K$. Chứng minh: $I$ là trung điểm của $DK$ và $CK \\perp CD$.'
    cau[17]['dap_an'] = '$I$ là trung điểm $DK$ và $CK \\perp CD$'
    cau[17]['loi_giai'] = '1) Vì $DI \\parallel BC$, áp dụng hệ quả định lí Thalès trong $\\Delta ABC$:\n$$\\dfrac{DI}{BC} = \\dfrac{AI}{AC} \\Rightarrow DI = \\dfrac{AI}{AC} \\cdot BC.$$\nÁp dụng hệ quả Thalès trong $\\Delta ABE$ với $DK \\parallel BE$ và $IK \\parallel CE$:\n$$\\dfrac{IK}{CE} = \\dfrac{AI}{AC} \\Rightarrow IK = \\dfrac{AI}{AC} \\cdot CE.$$\nMà $C$ là trung điểm của $BE$ (do $E$ đối xứng với $B$ qua $C$) nên $BC = CE$.\nSuy ra $DI = IK$. Vậy $I$ là trung điểm của $DK$.\n\n2) Ta có $CK$ là tia phân giác của góc ngoài tại đỉnh $C$ của $\\Delta ABC$.\nVì $CD$ là tia phân giác của góc trong và $CK$ là tia phân giác của góc ngoài tại cùng một đỉnh nên chúng vuông góc với nhau:\n$$CK \\perp CD \\text{ (đpcm)}.$$'
    cau[17]['can_doc_anh'] = False
    cau[17]['da_duyet'] = True

    # Bài 5 (0.5đ)
    cau[18]['vi_tri'] = 'Bài 5'
    cau[18]['loai'] = 'TL'
    cau[18]['chuong'] = 'VII. Định lí Thalès trong tam giác'
    cau[18]['dang'] = ['Ứng dụng thực tế của định lí Thalès', 'Thang bậc nhu cầu Maslow']
    cau[18]['band'] = 'VDC'
    cau[18]['phut'] = 4.5
    cau[18]['diem_bai'] = 0.5
    cau[18]['de'] = 'Nhà tâm lý học Abraham Maslow (1908 – 1970) đã phát triển Lý thuyết về Thang bậc nhu cầu của con người (mô hình hình tam giác được chia thành các bậc nhu cầu song song với cạnh đáy). Biết cạnh đáy $BK = 6\\text{ cm}$ và các tầng nhu cầu được chia đều nhau. Hãy tính độ dài các đoạn thẳng $CJ, EH$.'
    cau[18]['dap_an'] = '$CJ = 4{,}8\\text{ cm}, EH = 2{,}4\\text{ cm}$ (hoặc tính theo tỉ lệ hình)'
    cau[18]['loi_giai'] = 'Mô hình thang bậc nhu cầu hình tam giác có 5 tầng bằng nhau, do đó các đoạn thẳng song song với đáy chia các cạnh bên thành các phần bằng nhau.\nÁp dụng hệ quả định lí Thalès:\n- Đoạn $CJ$ ở vị trí tầng thứ 4: $CJ = \\dfrac{4}{5} BK = \\dfrac{4}{5} \\cdot 6 = 4{,}8\\text{ cm}$.\n- Đoạn $EH$ ở vị trí tầng thứ 2: $EH = \\dfrac{2}{5} BK = \\dfrac{2}{5} \\cdot 6 = 2{,}4\\text{ cm}$.'
    cau[18]['can_doc_anh'] = False
    cau[18]['da_duyet'] = True

    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    tot = sum(c['diem_bai'] for c in d['cau'])
    n = len(d['cau'])
    print(f'Done D13 (THCS Ly Son 2024): {n} cau, {tot:.2f}d')

if __name__ == '__main__':
    update_d10()
    update_d11()
    update_d12()
    update_d13()
