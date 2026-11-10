import json

slug = 'gk2-2025-thcs-phuong-liet'
path = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
data = json.load(open(path, 'r', encoding='utf-8'))

data['tang'] = 2
data['da_duyet'] = True
data['ghi_chu'] = 'Đề thi giữa kì 2 Toán 8 năm học 2024-2025 THCS Phương Liệt (Hà Nội). Đề 100% tự luận (5 bài: Bài 1: 2.0đ, Bài 2: 2.0đ, Bài 3: 1.0đ, Bài 4: 4.5đ, Bài 5: 0.5đ). Tổng 10.00 điểm.'

cau_list = [
    {
        "id": f"l8-{slug}-b1a",
        "vi_tri": "Bài 1.a",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Cộng trừ phân thức đại số"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 0.75,
        "de": "Thực hiện phép tính:\n$$\\frac{x^2}{x-7} - \\frac{7x}{x-7}$$",
        "dap_an": "$$\\frac{x^2}{x-7} - \\frac{7x}{x-7} = \\frac{x^2 - 7x}{x-7} = \\frac{x(x-7)}{x-7} = x$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b1b",
        "vi_tri": "Bài 1.b",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Nhân chia phân thức đại số"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 0.75,
        "de": "Thực hiện phép tính:\n$$\\frac{2x+10}{x^2-16} \\cdot \\frac{x-4}{x+5}$$",
        "dap_an": "$$\\frac{2x+10}{x^2-16} \\cdot \\frac{x-4}{x+5} = \\frac{2(x+5)}{(x-4)(x+4)} \\cdot \\frac{x-4}{x+5} = \\frac{2}{x+4}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b1c",
        "vi_tri": "Bài 1.c",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Biểu thức phối hợp các phép tính phân thức"],
        "band": "TH",
        "phut": 4,
        "diem_bai": 0.5,
        "de": "Thực hiện phép tính:\n$$\\left(\\frac{x^2}{x^2+2x} + \\frac{1}{x+2}\\right) : \\frac{x+1}{x}$$",
        "dap_an": "Ta có:\n$$\\frac{x^2}{x^2+2x} + \\frac{1}{x+2} = \\frac{x^2}{x(x+2)} + \\frac{1}{x+2} = \\frac{x}{x+2} + \\frac{1}{x+2} = \\frac{x+1}{x+2}$$\nDo đó:\n$$\\left(\\frac{x^2}{x^2+2x} + \\frac{1}{x+2}\\right) : \\frac{x+1}{x} = \\frac{x+1}{x+2} \\cdot \\frac{x}{x+1} = \\frac{x}{x+2}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2a",
        "vi_tri": "Bài 2.a",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Rút gọn biểu thức chứa phân thức"],
        "band": "TH",
        "phut": 5,
        "diem_bai": 1.0,
        "de": "Cho biểu thức $P = \\frac{x}{x-5} + \\frac{1}{x+5} + \\frac{35-x^2}{x^2-25}$ với $x \\ne \\pm 5$.\nChứng minh rằng $P = \\frac{6}{x-5}$.",
        "dap_an": "Với $x \\ne \\pm 5$, ta có:\n$$\\begin{aligned}\nP &= \\frac{x}{x-5} + \\frac{1}{x+5} + \\frac{35-x^2}{(x-5)(x+5)} \\\\\n&= \\frac{x(x+5) + (x-5) + 35 - x^2}{(x-5)(x+5)} \\\\\n&= \\frac{x^2 + 5x + x - 5 + 35 - x^2}{(x-5)(x+5)} \\\\\n&= \\frac{6x + 30}{(x-5)(x+5)} \\\\\n&= \\frac{6(x+5)}{(x-5)(x+5)} = \\frac{6}{x-5}\n\\end{aligned}$$\nVậy $P = \\frac{6}{x-5}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2b",
        "vi_tri": "Bài 2.b",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tính giá trị biểu thức phân thức"],
        "band": "NB",
        "phut": 2,
        "diem_bai": 0.5,
        "de": "Tính giá trị của biểu thức $P$ khi $x = 2$.",
        "dap_an": "Ta thấy $x = 2$ thỏa mãn ĐKXĐ ($x \\ne \\pm 5$).\nThay $x = 2$ vào biểu thức $P = \\frac{6}{x-5}$, ta được:\n$$P = \\frac{6}{2-5} = \\frac{6}{-3} = -2$$\nVậy với $x = 2$ thì $P = -2$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b2c",
        "vi_tri": "Bài 2.c",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Tìm x để biểu thức nhận giá trị cho trước"],
        "band": "TH",
        "phut": 3,
        "diem_bai": 0.5,
        "de": "Tìm $x$ để $P = \\frac{1}{2}$.",
        "dap_an": "Để $P = \\frac{1}{2}$, ta có:\n$$\\frac{6}{x-5} = \\frac{1}{2} \\implies x - 5 = 12 \\implies x = 17$$\nGiá trị $x = 17$ thỏa mãn ĐKXĐ ($x \\ne \\pm 5$).\nVậy $x = 17$ thì $P = \\frac{1}{2}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b3a",
        "vi_tri": "Bài 3.a",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Bài toán thực tế về phân thức đại số"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 0.5,
        "de": "Một người giao hàng cần giao một bưu phẩm từ bưu cục đến nhà khách hàng cách nhau $12\\text{ km}$. Người đó đi $5\\text{ km}$ đầu tiên bằng xe đạp với vận tốc $x\\text{ (km/h)}$, quãng đường còn lại đi bằng xe máy với vận tốc gấp đôi vận tốc xe đạp.\nViết các phân thức theo $x$ biểu thị thời gian người giao hàng đi mỗi đoạn đường.",
        "dap_an": "- Quãng đường người đó đi xe đạp là $5\\text{ km}$ với vận tốc $x\\text{ (km/h)}$.\nThời gian đi bằng xe đạp là:\n$$\\frac{5}{x}\\text{ (giờ)}$$\n- Quãng đường còn lại đi bằng xe máy là: $12 - 5 = 7\\text{ (km)}$.\nVận tốc xe máy gấp đôi vận tốc xe đạp nên vận tốc xe máy là $2x\\text{ (km/h)}$.\nThời gian đi bằng xe máy là:\n$$\\frac{7}{2x}\\text{ (giờ)}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b3b",
        "vi_tri": "Bài 3.b",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Bài toán thực tế về phân thức đại số"],
        "band": "TH",
        "phut": 4,
        "diem_bai": 0.5,
        "de": "Trong quá trình giao hàng, người giao hàng dừng tại bưu cục trung chuyển để kiểm tra đơn hàng mất $9\\text{ phút}$. Viết phân thức biểu thị tổng thời gian người đó đi từ bưu cục ban đầu đến khi tới nhà khách hàng theo $x$. Tính tổng thời gian đó biết vận tốc xe đạp là $10\\text{ km/h}$.",
        "dap_an": "Đổi $9\\text{ phút} = \\frac{9}{60}\\text{ giờ} = \\frac{3}{20}\\text{ giờ}$.\nPhân thức biểu thị tổng thời gian người đó đi là:\n$$T = \\frac{5}{x} + \\frac{7}{2x} + \\frac{3}{20} = \\frac{10}{2x} + \\frac{7}{2x} + \\frac{3}{20} = \\frac{17}{2x} + \\frac{3}{20}\\text{ (giờ)}$$\nVới $x = 10\\text{ (km/h)}$, tổng thời gian là:\n$$T = \\frac{17}{2 \\cdot 10} + \\frac{3}{20} = \\frac{17}{20} + \\frac{3}{20} = \\frac{20}{20} = 1\\text{ (giờ)} = 60\\text{ phút}$$\nVậy tổng thời gian người đó đi là $1\\text{ giờ}$ (hay $60\\text{ phút}$).",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-1",
        "vi_tri": "Bài 4.1",
        "loai": "TL",
        "chuong": "VII. Định lí Thalès trong tam giác",
        "dang": ["Ứng dụng thực tế của định lí Thalès"],
        "band": "TH",
        "phut": 4,
        "diem_bai": 1.0,
        "de": "Một người cắm một cái cọc $CD$ cao $1{,}5\\text{ m}$ vuông góc với mặt đất sao cho bóng của đỉnh cọc trùng với bóng của đỉnh cây tại điểm $E$ trên mặt đất. Biết khoảng cách từ gốc cây đến chân cọc là $AC = 8\\text{ m}$ và khoảng cách từ chân cọc tới điểm $E$ là $CE = 2\\text{ m}$. Tính chiều cao $AB$ của cây (giả sử cây mọc thẳng đứng vuông góc với mặt đất).",
        "dap_an": "Vì cây $AB$ và cọc $CD$ đều vuông góc với mặt đất nên $AB \\parallel CD$.\nÁp dụng hệ quả của định lí Thalès (hoặc tam giác đồng dạng $\\Delta ECD \\sim \\Delta EAB$), ta có:\n$$\\frac{CD}{AB} = \\frac{EC}{EA}$$\nTa có $EA = EC + CA = 2 + 8 = 10\\text{ (m)}$.\nThay số:\n$$\\frac{1{,}5}{AB} = \\frac{2}{10} = \\frac{1}{5} \\implies AB = 1{,}5 \\cdot 5 = 7{,}5\\text{ (m)}$$\nVậy chiều cao của cây là $7{,}5\\text{ m}$.",
        "trang": 1,
        "co_hinh": True,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2a",
        "vi_tri": "Bài 4.2a",
        "loai": "TL",
        "chuong": "VII. Định lí Thalès trong tam giác",
        "dang": ["Định lí Pythagore"],
        "band": "NB",
        "phut": 3,
        "diem_bai": 1.0,
        "de": "Cho tam giác $ABC$ vuông tại $A$ có $AB < AC$. Kẻ đường cao $AH$ ($H \\in BC$); $AM$ là tia phân giác của góc $A$ ($M \\in BC$). Từ $M$ kẻ $ME$ vuông góc với $AB$ tại $E$.\na) Biết $AB = 3\\text{ cm}, BC = 5\\text{ cm}$. Tính độ dài cạnh $AC$.",
        "dap_an": "Áp dụng định lí Pythagore cho tam giác $ABC$ vuông tại $A$, ta có:\n$$BC^2 = AB^2 + AC^2 \\implies AC^2 = BC^2 - AB^2 = 5^2 - 3^2 = 25 - 9 = 16$$\n$$\\implies AC = \\sqrt{16} = 4\\text{ (cm)}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2b",
        "vi_tri": "Bài 4.2b",
        "loai": "TL",
        "chuong": "VIII. Tam giác đồng dạng",
        "dang": ["Chứng minh tam giác đồng dạng", "Hệ thức hình học"],
        "band": "TH",
        "phut": 5,
        "diem_bai": 1.25,
        "de": "Chứng minh $AB \\cdot BE = MB \\cdot BH$ và $\\widehat{BME} = \\widehat{BAH}$.",
        "dap_an": "Xét $\\Delta BEM$ và $\\Delta BHA$ có:\n- $\\widehat{BEM} = \\widehat{BHA} = 90^\\circ$\n- $\\widehat{B}$ là góc chung\nDo đó $\\Delta BEM \\sim \\Delta BHA$ (g.g).\nSuy ra tỉ số đồng dạng:\n$$\\frac{BE}{BH} = \\frac{BM}{BA} \\implies AB \\cdot BE = MB \\cdot BH$$\nTừ $\\Delta BEM \\sim \\Delta BHA$, suy ra các góc tương ứng bằng nhau:\n$$\\widehat{BME} = \\widehat{BAH}$$",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b4-2c",
        "vi_tri": "Bài 4.2c",
        "loai": "TL",
        "chuong": "VIII. Tam giác đồng dạng",
        "dang": ["Tính chất đường phân giác trong tam giác", "Chứng minh tia phân giác"],
        "band": "VD",
        "phut": 6,
        "diem_bai": 1.25,
        "de": "Chứng minh $HE$ là tia phân giác của $\\widehat{AHB}$.",
        "dap_an": "Vì $AM$ là tia phân giác của góc vuông $\\widehat{BAC}$ nên $\\widehat{BAM} = 45^\\circ$.\nTam giác $AEM$ vuông tại $E$ có $\\widehat{EAM} = 45^\\circ$ nên $\\Delta AEM$ vuông cân tại $E$, suy ra $AE = ME$.\nTheo câu b, $\\Delta BEM \\sim \\Delta BHA$, ta có:\n$$\\frac{BE}{BH} = \\frac{ME}{AH} \\implies \\frac{BE}{BH} = \\frac{AE}{AH} \\implies \\frac{EA}{EB} = \\frac{HA}{HB}$$\nXét tam giác $AHB$, điểm $E$ thuộc cạnh $AB$ thỏa mãn:\n$$\\frac{EA}{EB} = \\frac{HA}{HB}$$\nTheo tính chất đường phân giác đảo, tia $HE$ là tia phân giác của $\\widehat{AHB}$.",
        "trang": 1,
        "co_hinh": False,
        "can_doc_anh": False,
        "da_duyet": True
    },
    {
        "id": f"l8-{slug}-b5",
        "vi_tri": "Bài 5",
        "loai": "TL",
        "chuong": "IV. Phân thức đại số",
        "dang": ["Giá trị biểu thức đối xứng", "Cực trị và hằng số biểu thức"],
        "band": "VDC",
        "phut": 6,
        "diem_bai": 0.5,
        "de": "Cho các biểu thức:\n$$A = \\frac{4yz-x^2}{yz+2x^2}; \\quad B = \\frac{4zx-y^2}{zx+2y^2}; \\quad C = \\frac{4xy-z^2}{xy+2z^2}$$\nChứng minh rằng nếu $x+y+z=0$ và $x, y, z$ đôi một khác nhau thì tích $A \\cdot B \\cdot C$ là một hằng số.",
        "dap_an": "Vì $x+y+z=0$ nên $y+z = -x \\implies (y+z)^2 = x^2$.\nTa biến đổi tử số của $A$:\n$$4yz - x^2 = 4yz - (y+z)^2 = 4yz - (y^2 + 2yz + z^2) = -(y^2 - 2yz + z^2) = -(y-z)^2$$\nBiến đổi mẫu số của $A$:\n$$yz + 2x^2 = yz + 2[-(y+z)]^2 = yz + 2(y^2 + 2yz + z^2) = 2y^2 + 5yz + 2z^2 = (2y+z)(y+2z)$$\nVì $x+y+z=0$ nên:\n- $2y+z = y + (y+z) = y - x = -(x-y)$\n- $y+2z = z + (y+z) = z - x = -(x-z)$\nDo đó:\n$$yz + 2x^2 = [-(x-y)][-(x-z)] = (x-y)(x-z)$$\nSuy ra:\n$$A = \\frac{-(y-z)^2}{(x-y)(x-z)}$$\nHoàn toàn tương tự, ta có:\n$$B = \\frac{-(z-x)^2}{(y-z)(y-x)} = \\frac{(x-z)^2}{(y-z)(x-y)}$$\n$$C = \\frac{-(x-y)^2}{(z-x)(z-y)} = \\frac{-(x-y)^2}{(x-z)(y-z)}$$\nNhân ba biểu thức với nhau, ta được:\n$$A \\cdot B \\cdot C = \\frac{[-(y-z)^2] \\cdot (x-z)^2 \\cdot [-(x-y)^2]}{(x-y)(x-z) \\cdot (y-z)(x-y) \\cdot (x-z)(y-z)} = \\frac{(x-y)^2(y-z)^2(x-z)^2}{(x-y)^2(y-z)^2(x-z)^2} = 1$$\nVì $x, y, z$ đôi một khác nhau nên biểu thức xác định và có giá trị bằng $1$ (hằng số).\nVậy tích $A \\cdot B \\cdot C = 1$ không phụ thuộc vào giá trị của $x, y, z$.",
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
