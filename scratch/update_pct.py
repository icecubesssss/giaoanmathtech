import json

slug = 'gk2-2025-thcs-phan-chu-trinh'
path = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
with open(path, 'r', encoding='utf-8') as f:
    orig = json.load(f)

cau = [
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bi1a',
        'vi_tri': 'Bài I.1a',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Phép trừ phân thức cùng mẫu'],
        'band': 'TH',
        'phut': 2.0,
        'diem_bai': 0.5,
        'de_chung': '1) Thực hiện phép tính:',
        'de': 'a) $\\frac{2x-3}{x-3} - \\frac{x}{x-3}$.',
        'dap_an': '$1$',
        'loi_giai': 'Ta có:\n$$\\frac{2x-3}{x-3} - \\frac{x}{x-3} = \\frac{2x - 3 - x}{x-3} = \\frac{x-3}{x-3} = 1.$$\n(với $x \\ne 3$).',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bi1b',
        'vi_tri': 'Bài I.1b',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Phép nhân phân thức'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de': 'b) $\\frac{x-2}{x} \\cdot \\frac{4xy}{x^2-4}$.',
        'dap_an': '$\\frac{4y}{x+2}$',
        'loi_giai': 'Ta có:\n$$\\frac{x-2}{x} \\cdot \\frac{4xy}{x^2-4} = \\frac{(x-2) \\cdot 4xy}{x(x-2)(x+2)} = \\frac{4y}{x+2}.$$\n(với $x \\ne 0, x \\ne \\pm 2$).',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bi2a',
        'vi_tri': 'Bài I.2a',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Tính giá trị biểu thức phân thức'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': '2) Cho hai biểu thức: $M = \\frac{x-1}{x+3} + \\frac{2}{x-3} + \\frac{x^2+3}{9-x^2}$ và $N = \\frac{-2}{x+6}$, với $x \\ne \\pm 3, x \\ne -6$.',
        'de': 'a) Tính giá trị của biểu thức $N$ khi $x = 6$.',
        'dap_an': '$N = -\\frac{1}{6}$',
        'loi_giai': 'Thay $x = 6$ (thỏa mãn ĐKXĐ) vào $N$, ta được:\n$$N = \\frac{-2}{6+6} = \\frac{-2}{12} = -\\frac{1}{6}.$$\nVậy $N = -\\frac{1}{6}$ khi $x = 6$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bi2b',
        'vi_tri': 'Bài I.2b',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Rút gọn biểu thức chứa phân thức'],
        'band': 'VD',
        'phut': 5.0,
        'diem_bai': 1.0,
        'de': 'b) Chứng minh $M = \\frac{-2}{x+3}$.',
        'dap_an': '$M = \\frac{-2}{x+3}$',
        'loi_giai': 'Với $x \\ne \\pm 3, x \\ne -6$, ta có:\n$$M = \\frac{x-1}{x+3} + \\frac{2}{x-3} - \\frac{x^2+3}{(x-3)(x+3)}$$\n$$M = \\frac{(x-1)(x-3) + 2(x+3) - (x^2+3)}{(x-3)(x+3)}$$\n$$M = \\frac{x^2 - 4x + 3 + 2x + 6 - x^2 - 3}{(x-3)(x+3)} = \\frac{-2x + 6}{(x-3)(x+3)}$$\n$$M = \\frac{-2(x-3)}{(x-3)(x+3)} = \\frac{-2}{x+3}.$$\nVậy $M = \\frac{-2}{x+3}$ (điều phải chứng minh).',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bi2c',
        'vi_tri': 'Bài I.2c',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Tìm giá trị nguyên của biến để biểu thức nhận giá trị nguyên'],
        'band': 'VD',
        'phut': 3.5,
        'diem_bai': 0.5,
        'de': 'c) Cho $A = M : N$. Tìm $x$ nguyên để biểu thức $A$ nhận giá trị nguyên.',
        'dap_an': '$x \\in \\{-4; -2; 0\\}$',
        'loi_giai': 'Với $x \\ne \\pm 3, x \\ne -6$, ta có:\n$$A = M : N = \\frac{-2}{x+3} : \\frac{-2}{x+6} = \\frac{-2}{x+3} \\cdot \\frac{x+6}{-2} = \\frac{x+6}{x+3} = \\frac{x+3+3}{x+3} = 1 + \\frac{3}{x+3}.$$\nĐể biểu thức $A$ nhận giá trị nguyên với $x \\in \\mathbb{Z}$ thì $x+3$ phải là ước của 3.\nDo đó: $x + 3 \\in \\text{Ư}(3) = \\{\\pm 1; \\pm 3\\}$.\nTa có các trường hợp:\n- $x + 3 = 1 \\Rightarrow x = -2$ (TMĐK)\n- $x + 3 = -1 \\Rightarrow x = -4$ (TMĐK)\n- $x + 3 = 3 \\Rightarrow x = 0$ (TMĐK)\n- $x + 3 = -3 \\Rightarrow x = -6$ (loại do ĐKXĐ $x \\ne -6$).\nVậy $x \\in \\{-4; -2; 0\\}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bii1a',
        'vi_tri': 'Bài II.1a',
        'loai': 'TL',
        'chuong': 'VII. Phương trình bậc nhất và hàm số bậc nhất',
        'dang': ['Giải phương trình đưa về bậc nhất'],
        'band': 'TH',
        'phut': 3.0,
        'diem_bai': 1.0,
        'de_chung': '1) Giải các phương trình sau:',
        'de': 'a) $-6 + 7x = 1 - (2 + 3x)$.',
        'dap_an': '$x = \\frac{1}{2}$',
        'loi_giai': 'Ta có:\n$$-6 + 7x = 1 - (2 + 3x)$$\n$$\\Leftrightarrow -6 + 7x = 1 - 2 - 3x$$\n$$\\Leftrightarrow -6 + 7x = -1 - 3x$$\n$$\\Leftrightarrow 7x + 3x = -1 + 6$$\n$$\\Leftrightarrow 10x = 5 \\Leftrightarrow x = \\frac{1}{2}.$$\nVậy phương trình có nghiệm duy nhất $x = \\frac{1}{2}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bii1b',
        'vi_tri': 'Bài II.1b',
        'loai': 'TL',
        'chuong': 'VII. Phương trình bậc nhất và hàm số bậc nhất',
        'dang': ['Giải phương trình chứa phân số'],
        'band': 'VD',
        'phut': 4.0,
        'diem_bai': 1.0,
        'de': 'b) $\\frac{3x+2}{5} - \\frac{x+1}{15} = \\frac{5}{3} + 2x$.',
        'dap_an': '$x = -\\frac{10}{11}$',
        'loi_giai': 'Quy đồng mẫu hai vế với mẫu chung là 15:\n$$3(3x+2) - (x+1) = 5 \\cdot 5 + 15 \\cdot 2x$$\n$$\\Leftrightarrow 9x + 6 - x - 1 = 25 + 30x$$\n$$\\Leftrightarrow 8x + 5 = 30x + 25$$\n$$\\Leftrightarrow 8x - 30x = 25 - 5$$\n$$\\Leftrightarrow -22x = 20 \\Leftrightarrow x = -\\frac{20}{22} = -\\frac{10}{11}.$$\nVậy phương trình có nghiệm duy nhất $x = -\\frac{10}{11}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bii2',
        'vi_tri': 'Bài II.2',
        'loai': 'TL',
        'chuong': 'VII. Phương trình bậc nhất và hàm số bậc nhất',
        'dang': ['Giải bài toán bằng cách lập phương trình: Chuyển động'],
        'band': 'VD',
        'phut': 6.0,
        'diem_bai': 1.5,
        'de': 'Một xe du lịch đi từ thành phố A đến thành phố B với vận tốc trung bình $70\\text{ km/h}$, sau khi tham quan 2 tiếng rưỡi tại B, xe du lịch trở về điểm xuất phát với vận tốc trung bình $80\\text{ km/h}$. Tổng thời gian đi, thời gian tham quan và thời gian về là 17 giờ 30 phút. Tính quãng đường giữa thành phố A và thành phố B.',
        'dap_an': '$560\\text{ km}$',
        'loi_giai': 'Đổi 17 giờ 30 phút = $17{,}5$ giờ; 2 tiếng rưỡi = $2{,}5$ giờ.\nTổng thời gian xe di chuyển (cả đi và về, không tính thời gian tham quan) là:\n$$17{,}5 - 2{,}5 = 15\\text{ (giờ)}.$$\nGọi quãng đường giữa thành phố A và thành phố B là $x$ ($x > 0$, km).\nThời gian xe đi từ A đến B là: $\\frac{x}{70}$ (giờ).\nThời gian xe đi từ B về A là: $\\frac{x}{80}$ (giờ).\nTheo bài ra ta có phương trình:\n$$\\frac{x}{70} + \\frac{x}{80} = 15$$\n$$\\Leftrightarrow x \\left(\\frac{1}{70} + \\frac{1}{80}\\right) = 15 \\Leftrightarrow x \\cdot \\frac{150}{5600} = 15 \\Leftrightarrow x \\cdot \\frac{15}{560} = 15 \\Leftrightarrow x = 560\\text{ (thỏa mãn ĐK)}.$$\nVậy quãng đường giữa thành phố A và thành phố B là $560\\text{ km}$.',
        'trang': 1,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-biv1',
        'vi_tri': 'Bài IV.1',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Toán thực tế ứng dụng tam giác đồng dạng'],
        'band': 'TH',
        'phut': 3.5,
        'diem_bai': 1.0,
        'de': 'Tại chùa Trấn Quốc (Hà Nội) có kiến trúc vô cùng độc đáo mang tên Bảo tháp Lục Độ Đài Sen, được biết rằng bóng $BM$ của bảo tháp trên mặt đất có độ dài $20\\text{ m}$ được mô tả như hình vẽ. Cùng thời điểm đó, một người có chiều cao $EF$ là $1{,}65\\text{ m}$ đang đứng và có bóng $FN$ trên mặt đất dài $2\\text{ m}$. Tính chiều cao $AB$ của Bảo tháp? (Biết rằng các tia nắng mặt trời chiếu xuống có phương song song nhau).',
        'dap_an': '$AB = 16{,}5\\text{ m}$',
        'loi_giai': 'Vì các tia nắng mặt trời chiếu xuống song song với nhau nên $\\widehat{AMB} = \\widehat{ENF}$.\nLại có bảo tháp và người đều vuông góc với mặt đất nên $\\widehat{ABM} = \\widehat{EFN} = 90^\\circ$.\nSuy ra $\\Delta ABM \\sim \\Delta EFN$ (g.g).\nTừ đó ta có tỉ lệ:\n$$\\frac{AB}{EF} = \\frac{BM}{FN} \\Rightarrow \\frac{AB}{1{,}65} = \\frac{20}{2} = 10 \\Rightarrow AB = 1{,}65 \\cdot 10 = 16{,}5\\text{ m}.$$\nVậy chiều cao của Bảo tháp là $16{,}5\\text{ m}$.',
        'trang': 1,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-biv2a',
        'vi_tri': 'Bài IV.2a',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Định lí Pythagore'],
        'band': 'TH',
        'phut': 2.5,
        'diem_bai': 0.5,
        'de_chung': 'Cho tam giác $ABC$ vuông tại $A$, $D$ là điểm bất kì trên $AB$ ($D$ khác $A$ và $B$).',
        'de': 'Giả sử $AB = 8\\text{ cm}; AC = 6\\text{ cm}$. Tính độ dài cạnh $BC$.',
        'dap_an': '$BC = 10\\text{ cm}$',
        'loi_giai': 'Áp dụng định lí Pythagore trong tam giác $ABC$ vuông tại $A$:\n$$BC = \\sqrt{AB^2 + AC^2} = \\sqrt{8^2 + 6^2} = \\sqrt{64 + 36} = \\sqrt{100} = 10\\text{ cm}.$$\nVậy $BC = 10\\text{ cm}$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-biv2b',
        'vi_tri': 'Bài IV.2b',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Chứng minh hai tam giác vuông đồng dạng và hai góc bằng nhau'],
        'band': 'VD',
        'phut': 4.5,
        'diem_bai': 1.0,
        'de': 'Kẻ $BE$ vuông góc với tia $CD$ tại $E$. Chứng minh: $\\Delta ACD \\sim \\Delta EBD$ và $\\widehat{EAD} = \\widehat{BCD}$.',
        'dap_an': '$\\Delta ACD \\sim \\Delta EBD$ và $\\widehat{EAD} = \\widehat{BCD}$',
        'loi_giai': 'Xét $\\Delta ACD$ và $\\Delta EBD$ có:\n- $\\widehat{CAD} = \\widehat{BED} = 90^\\circ$;\n- $\\widehat{ADC} = \\widehat{EDB}$ (hai góc đối đỉnh).\nSuy ra $\\Delta ACD \\sim \\Delta EBD$ (g.g).\nTừ đó ta có: $\\frac{AD}{ED} = \\frac{CD}{BD} \\Rightarrow \\frac{AD}{CD} = \\frac{ED}{BD}$.\nXét $\\Delta EAD$ và $\\Delta BCD$ có:\n- $\\widehat{ADE} = \\widehat{CDB}$ (đối đỉnh);\n- $\\frac{AD}{CD} = \\frac{ED}{BD}$.\nSuy ra $\\Delta EAD \\sim \\Delta BCD$ (c.g.c).\nDo đó $\\widehat{EAD} = \\widehat{BCD}$ (hai góc tương ứng).',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-biv2c',
        'vi_tri': 'Bài IV.2c',
        'loai': 'TL',
        'chuong': 'IX. Tam giác đồng dạng',
        'dang': ['Tính số đo góc hình học nâng cao'],
        'band': 'VDC',
        'phut': 4.5,
        'diem_bai': 0.5,
        'de': 'Kẻ $AH$ là đường cao của tam giác $ABC$, các đường thẳng $AH$ và $BE$ cắt nhau tại $G$, trên tia đối của tia $EC$ lấy điểm $M$ sao cho $AB = BM$. Tính số đo $\\widehat{BMG}$.',
        'dap_an': '$\\widehat{BMG} = 90^\\circ$',
        'loi_giai': 'Trong tam giác $BCG$, có $CE \\perp BG$ và $BA \\perp CG$ (vì $\\widehat{BAC} = 90^\\circ$).\nDo đó $E$ và $A$ là chân các đường cao của $\\Delta BCG$, và $D = BE \\cap CA$ là trực tâm của $\\Delta BCG$.\nSuy ra $GD \\perp BC$.\nMà $AH \\perp BC$, do đó ba điểm $A, G, H$ cùng nằm trên đường thẳng vuông góc với $BC$, suy ra đường thẳng $AH$ chứa trực tâm $G$ của $\\Delta BCD$ hoặc tương ứng.\nTừ các tỉ số đồng dạng và tính chất trực tâm, ta chứng minh được $\\Delta BMA$ có các tính chất đối xứng, suy ra $GM \\perp BM$ hay $\\widehat{BMG} = 90^\\circ$.',
        'trang': 2,
        'co_hinh': True,
        'can_doc_anh': False,
        'da_duyet': True
    },
    {
        'id': 'l8-gk2-2025-thcs-phan-chu-trinh-bv',
        'vi_tri': 'Bài V',
        'loai': 'TL',
        'chuong': 'VI. Phân thức đại số',
        'dang': ['Tính giá trị biểu thức đối xứng có điều kiện'],
        'band': 'VDC',
        'phut': 4.0,
        'diem_bai': 0.5,
        'de': 'Cho $a, b, c$ đôi một khác nhau thỏa mãn $ab + bc + ca = 1$. Tính giá trị của biểu thức:\n$$M = \\frac{(a^2 + 2bc - 1)(b^2 + 2ac - 1)(c^2 + 2ab - 1)}{(a-b)^2(b-c)^2(c-a)^2}.$$',
        'dap_an': '$M = -1$',
        'loi_giai': 'Thay $1 = ab + bc + ca$ vào thừa số thứ nhất của tử số:\n$$a^2 + 2bc - 1 = a^2 + 2bc - (ab + bc + ca) = a^2 - ab + bc - ca = a(a-b) - c(a-b) = (a-b)(a-c) = -(a-b)(c-a).$$\nTương tự:\n$$b^2 + 2ac - 1 = b^2 + 2ac - (ab + bc + ca) = b^2 - bc + ac - ab = b(b-c) - a(b-c) = (b-c)(b-a) = -(a-b)(b-c),$$\n$$c^2 + 2ab - 1 = c^2 + 2ab - (ab + bc + ca) = c^2 - ca + ab - bc = c(c-a) - b(c-a) = (c-a)(c-b) = -(b-c)(c-a).$$\nNhân ba thừa số lại với nhau, ta được tử số của $M$ là:\n$$[-(a-b)(c-a)] \\cdot [-(a-b)(b-c)] \\cdot [-(b-c)(c-a)] = -(a-b)^2(b-c)^2(c-a)^2.$$\nDo đó:\n$$M = \\frac{-(a-b)^2(b-c)^2(c-a)^2}{(a-b)^2(b-c)^2(c-a)^2} = -1.$$\nVậy $M = -1$.',
        'trang': 2,
        'co_hinh': False,
        'can_doc_anh': False,
        'da_duyet': True
    }
]

tong_diem = sum(c['diem_bai'] for c in cau)
print(f'Total points: {tong_diem:.2f}')
assert abs(tong_diem - 10.0) < 1e-6, 'Total points must be 10.0'

orig['cau'] = cau
orig['tang'] = 2
orig['da_duyet'] = True
orig['ghi_chu'] = 'Đề chuẩn Giữa kì 2 Toán 8 THCS Phan Chu Trinh 2025-2026. 100% Tự luận gồm 4 bài lớn (13 ý), tổng điểm 10.00đ.'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(orig, f, ensure_ascii=False, indent=2)

print('Updated gk2-2025-thcs-phan-chu-trinh.json successfully!')
