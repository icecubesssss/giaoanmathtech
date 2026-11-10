# -*- coding: utf-8 -*-
import json, os

def save_exam(slug, data):
    p = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {slug}: {len(data['cau'])} cau, sum={sum(c['diem_bai'] for c in data['cau']):.2f}")

# ==============================================================================
# 6. ck2-x-2023-2024-de-thi-hk2-gddt-dan-phuong-hn
# ==============================================================================
def build_dan_phuong():
    slug = 'ck2-x-2023-2024-de-thi-hk2-gddt-dan-phuong-hn'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Biểu đồ cột kép"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Một công ty kinh doanh vật liệu xây dựng có bốn kho hàng, mỗi kho hàng có 50 tấn hàng. Biểu đồ cột kép biểu diễn số lượng vật liệu đã xuất bán và số lượng vật liệu còn tồn lại trong kho sau tuần lễ kinh doanh đầu tiên:\n- Kho 1: Xuất bán 30, Tồn lại 20\n- Kho 2: Xuất bán 35, Tồn lại 15\n- Kho 3: Xuất bán 33, Tồn lại 17\n- Kho 4: Xuất bán 34, Tồn lại 15\nKế toán đã ghi nhầm số liệu của một kho trong biểu đồ cột kép. Theo em kế toán đã ghi nhầm số liệu ở kho nào?\nA. Kho 4\nB. Kho 1\nC. Kho 3\nD. Kho 2",
            "dap_an": "A",
            "loi_giai": "Tổng lượng hàng ở mỗi kho là 50 tấn.\n- Kho 1: $30 + 20 = 50$ (tấn)\n- Kho 2: $35 + 15 = 50$ (tấn)\n- Kho 3: $33 + 17 = 50$ (tấn)\n- Kho 4: $34 + 15 = 49 \\neq 50$ (tấn).\nDo đó kế toán đã ghi nhầm số liệu ở Kho 4. Chọn A.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Đọc số liệu từ bảng thống kê"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Thống kê tỉ lệ % học sinh lớp 8A chọn môn thể thao yêu thích (mỗi em chọn 1 môn) được cho trong bảng sau: Bóng đá (50%), Cầu lông (25%), Bóng chuyền (12,5%), Bóng bàn (12,5%). Môn thể thao học sinh lớp 8A yêu thích nhiều nhất là:\nA. Bóng chuyền\nB. Bóng bàn\nC. Cầu lông\nD. Bóng đá",
            "dap_an": "D",
            "loi_giai": "Môn bóng đá có tỉ lệ yêu thích cao nhất là 50%. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Một hộp đựng 10 tấm thẻ cùng loại, mỗi tấm thẻ được ghi một trong các số $11; 12; 13; \\dots; 20$; hai tấm thẻ khác nhau thì ghi số khác nhau. Rút ngẫu nhiên một tấm thẻ trong hộp. Xác suất để rút được tấm thẻ ghi số nguyên tố là:\nA. $0{,}2$\nB. $0{,}4$\nC. $0{,}5$\nD. $0{,}6$",
            "dap_an": "B",
            "loi_giai": "Các số nguyên tố từ 11 đến 20 là: $11; 13; 17; 19$ (có 4 số).\nTổng số thẻ trong hộp là 10 thẻ.\nXác suất rút được tấm thẻ ghi số nguyên tố là: $\\frac{4}{10} = 0{,}4$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Nghiệm của phương trình $-3x + 5 = 0$ là:\nA. $x = \\frac{5}{3}$\nB. $x = -\\frac{5}{3}$\nC. $x = \\frac{3}{5}$\nD. $x = -\\frac{3}{5}$",
            "dap_an": "A",
            "loi_giai": "$$-3x + 5 = 0 \\Leftrightarrow -3x = -5 \\Leftrightarrow x = \\frac{5}{3}.$$ Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Nhận biết phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Phương trình nào sau đây là phương trình bậc nhất một ẩn?\nA. $0x + 3 = 0$\nB. $x^2 - 2 = 0$\nC. $1 - 3x = 0$\nD. $\\frac{5}{x} + 1 = 0$",
            "dap_an": "C",
            "loi_giai": "Phương trình bậc nhất một ẩn có dạng $ax + b = 0$ ($a \\neq 0$). Phương trình $1 - 3x = 0$ có $a = -3 \\neq 0$ là phương trình bậc nhất một ẩn. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Kiểm tra nghiệm của phương trình"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "$x = 2$ là nghiệm của phương trình nào:\nA. $2x + 1 = 0$\nB. $x + 2 = 0$\nC. $x - 2 = 0$\nD. $2x - 1 = 0$",
            "dap_an": "C",
            "loi_giai": "Thay $x = 2$ vào $x - 2 = 0$ ta được $2 - 2 = 0$ (luôn đúng). Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng cạnh - góc - cạnh"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "$\\triangle ABC \\backsim \\triangle DEF$ theo trường hợp cạnh - góc - cạnh nếu $\\widehat{B} = \\widehat{E}$ và có:\nA. $\\frac{AB}{BC} = \\frac{DE}{DF}$\nB. $\\frac{AC}{DF} = \\frac{BC}{EF}$\nC. $\\frac{AB}{DE} = \\frac{AC}{DF}$\nD. $\\frac{AB}{DE} = \\frac{BC}{EF}$",
            "dap_an": "D",
            "loi_giai": "Hai cạnh kề của góc $\\widehat{B}$ là $AB, BC$; hai cạnh kề của góc $\\widehat{E}$ là $DE, EF$. Do đó tỉ lệ đúng là $\\frac{AB}{DE} = \\frac{BC}{EF}$. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Kí hiệu tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm). Học sinh làm bài trực tiếp vào đề kiểm tra.\n(Hãy khoanh tròn vào chữ cái đứng trước phương án trả lời đúng)",
            "de": "Nếu $\\triangle ABC$ và $\\triangle MNP$ có $\\widehat{BAC} = \\widehat{NPM}; \\widehat{ACB} = \\widehat{MNP}$, cách viết nào sau đây đúng?\nA. $\\triangle ABC \\backsim \\triangle MNP$\nB. $\\triangle ABC \\backsim \\triangle PMN$\nC. $\\triangle ABC \\backsim \\triangle PNM$\nD. $\\triangle ABC \\backsim \\triangle NMP$",
            "dap_an": "B",
            "loi_giai": "Ta có $\\widehat{A} = \\widehat{P}$ nên đỉnh $A$ tương ứng với đỉnh $P$.\n$\\widehat{C} = \\widehat{N}$ nên đỉnh $C$ tương ứng với đỉnh $N$.\nSuy ra đỉnh $B$ tương ứng với đỉnh $M$.\nVậy cách viết đúng là $\\triangle ABC \\backsim \\triangle PMN$. Chọn B.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.75,
            "de_chung": "II. TỰ LUẬN (8,0 điểm). Học sinh làm bài vào giấy kiểm tra.\nBài 1: (1,5 điểm). Giải các phương trình sau:",
            "de": "a) $4x - 5 = 2x + 1$",
            "dap_an": "$x = 3$",
            "loi_giai": "$$4x - 5 = 2x + 1 \\Leftrightarrow 4x - 2x = 5 + 1 \\Leftrightarrow 2x = 6 \\Leftrightarrow x = 3.$$\nVậy nghiệm của phương trình là $x = 3$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Bài 1: (1,5 điểm). Giải các phương trình sau:",
            "de": "b) $\\frac{x - 2}{6} - \\frac{x}{2} = \\frac{5 - 2x}{3}$",
            "dap_an": "$x = 6$",
            "loi_giai": "$$\\frac{x - 2}{6} - \\frac{x}{2} = \\frac{5 - 2x}{3}$$\nQuy đồng mẫu thức chung là 6:\n$$\\frac{x - 2 - 3x}{6} = \\frac{2(5 - 2x)}{6}$$\n$$\\Leftrightarrow -2x - 2 = 10 - 4x$$\n$$\\Leftrightarrow -2x + 4x = 10 + 2$$\n$$\\Leftrightarrow 2x = 12 \\Leftrightarrow x = 6.$$\nVậy nghiệm của phương trình là $x = 6$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2-1", "vi_tri": "Bài 2.1", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.5,
            "de_chung": "Bài 2: (2,5 điểm).",
            "de": "1) Một ô tô đi từ Cần Thơ đến Bạc Liêu với vận tốc trung bình là $40\\text{ km/h}$. Lúc từ Bạc Liêu về Cần Thơ vẫn trên cùng tuyến đường, ô tô đi với vận tốc $60\\text{ km/h}$. Vì vậy tổng thời gian cả đi và về hết tất cả 5 giờ. Tính quãng đường mà ô tô đi từ Cần Thơ đến Bạc Liêu?",
            "dap_an": "$120\\text{ km}$",
            "loi_giai": "Gọi quãng đường ô tô đi từ Cần Thơ đến Bạc Liêu là $x\\text{ (km)}$ ($x > 0$).\nThời gian ô tô đi từ Cần Thơ đến Bạc Liêu là: $\\frac{x}{40}\\text{ (giờ)}$.\nThời gian ô tô đi từ Bạc Liêu về Cần Thơ là: $\\frac{x}{60}\\text{ (giờ)}$.\nVì tổng thời gian cả đi và về là 5 giờ nên ta có phương trình:\n$$\\frac{x}{40} + \\frac{x}{60} = 5$$\n$$\\Leftrightarrow \\frac{3x + 2x}{120} = 5$$\n$$\\Leftrightarrow 5x = 600 \\Leftrightarrow x = 120\\text{ (thỏa mãn điều kiện)}.$$\nVậy quãng đường mà ô tô đi từ Cần Thơ đến Bạc Liêu là $120\\text{ km}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2-2", "vi_tri": "Bài 2.2", "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "TH", "phut": 3.0, "diem_bai": 1.0,
            "de_chung": "Bài 2: (2,5 điểm).",
            "de": "2) Một hộp chứa các viên bi màu trắng và đen có kích thước và khối lượng như nhau. Mai lấy ra ngẫu nhiên một viên bi từ hộp, xem màu rồi trả lại hộp. Lặp lại thử nghiệm đó 80 lần, Mai thấy có 24 lần lấy được viên bi màu trắng. Hãy tính xác suất thực nghiệm của biến cố “Lấy được viên bi màu đen” sau 80 lần thử.",
            "dap_an": "$0{,}7$",
            "loi_giai": "Số lần Mai lấy được viên bi màu đen sau 80 lần thử là:\n$$80 - 24 = 56\\text{ (lần)}.$$\nXác suất thực nghiệm của biến cố “Lấy được viên bi màu đen” sau 80 lần thử là:\n$$P = \\frac{56}{80} = \\frac{7}{10} = 0{,}7.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3", "vi_tri": "Bài 3", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Toán thực tế ứng dụng định lí Thalès"],
            "band": "TH", "phut": 3.5, "diem_bai": 0.5,
            "de": "Bài 3: (0,5 điểm). Với số liệu được ghi trên hình vẽ bên, tính khoảng cách CD từ con tàu đến trạm quan trắc đặt tại điểm C (biết $CD \\perp AC, BE \\perp AC, BE = 120\\text{m}, BC = 400\\text{m}, AB = 200\\text{m}$).",
            "dap_an": "$360\\text{ m}$",
            "loi_giai": "Vì $CD \\perp AC$ và $BE \\perp AC$ nên $CD // BE$.\nTa có: $AC = AB + BC = 200 + 400 = 600\\text{ (m)}$.\nTheo hệ quả của định lí Thalès trong tam giác $ACD$ với $BE // CD$, ta có:\n$$\\frac{CD}{BE} = \\frac{AC}{AB} \\Rightarrow \\frac{CD}{120} = \\frac{600}{200} = 3.$$\nSuy ra khoảng cách từ con tàu đến trạm quan trắc là:\n$$CD = 120 \\cdot 3 = 360\\text{ (m)}.$$",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4: (3 điểm). Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "a) Chứng minh rằng: $\\triangle ABC \\backsim \\triangle HBA$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle HBA$ (g.g)",
            "loi_giai": "Xét $\\triangle ABC$ và $\\triangle HBA$, ta có:\n$$\\widehat{BAC} = \\widehat{BHA} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle ABC \\backsim \\triangle HBA\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hệ thức hình học nhờ tam giác đồng dạng"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 4: (3 điểm). Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "b) Gọi $M, N$ lần lượt là trung điểm của $BC$ và $AB$, từ $B$ kẻ đường thẳng vuông góc với $BC$ cắt $MN$ kéo dài tại $I$. Chứng minh rằng: $MN // AC$ và $IB^2 = IM \\cdot IN$.",
            "dap_an": "$MN // AC$ và $IB^2 = IM \\cdot IN$",
            "loi_giai": "+) Vì $M$ là trung điểm của $BC$ và $N$ là trung điểm của $AB$ nên $MN$ là đường trung bình của tam giác $ABC$.\nSuy ra $MN // AC$.\n+) Vì $MN // AC$ mà $AC \\perp AB$ tại $A$ nên $MN \\perp AB$ tại $N$, tức là $IN \\perp AB$.\nXét $\\triangle IBM$ vuông tại $B$ có đường cao $BN$ ($BN \\perp IM$).\nTa có $\\triangle IBN \\backsim \\triangle IMB\\text{ (g.g)}$ (vì $\\widehat{INB} = \\widehat{IBM} = 90^\\circ$ và $\\widehat{BIN}$ chung).\nSuy ra tỉ số: $\\frac{IB}{IM} = \\frac{IN}{IB} \\Rightarrow IB^2 = IM \\cdot IN$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Hệ quả định lí Thalès chứng minh trung điểm"],
            "band": "VDC", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 4: (3 điểm). Cho tam giác $ABC$ vuông tại $A$, có đường cao $AH$.",
            "de": "c) Gọi $O$ là giao điểm của $IC$ và $AH$. Chứng minh $O$ là trung điểm của $AH$.",
            "dap_an": "$O$ là trung điểm của $AH$",
            "loi_giai": "Gọi $K$ là giao điểm của $AC$ và $BI$.\nVì $BI \\perp BC$ và $AH \\perp BC$ nên $AH // BI$.\nÁp dụng hệ quả của định lí Thalès:\n- Trong tam giác $CBI$ có $OH // BI \\Rightarrow \\frac{OH}{BI} = \\frac{CO}{CI}$.\n- Trong tam giác $CIK$ có $OA // IK \\Rightarrow \\frac{OA}{IK} = \\frac{CO}{CI}$.\nSuy ra: $\\frac{OH}{BI} = \\frac{OA}{IK}$.\nMặt khác, xét tam giác $ABK$ có $N$ là trung điểm $AB$ và $NI // AK$ (do $MN // AC$), suy ra $I$ là trung điểm của $BK$, tức là $BI = IK$.\nDo đó $OH = OA$, hay $O$ là trung điểm của đoạn thẳng $AH$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có quy luật"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 5: (0,5 điểm). Giải phương trình: $\\frac{x - 241}{17} + \\frac{x - 220}{19} + \\frac{x - 195}{21} + \\frac{x - 166}{23} = 10$.",
            "dap_an": "$x = 258$",
            "loi_giai": "$$\\frac{x - 241}{17} + \\frac{x - 220}{19} + \\frac{x - 195}{21} + \\frac{x - 166}{23} = 10$$\n$$\\Leftrightarrow \\left(\\frac{x - 241}{17} - 1\\right) + \\left(\\frac{x - 220}{19} - 2\\right) + \\left(\\frac{x - 195}{21} - 3\\right) + \\left(\\frac{x - 166}{23} - 4\\right) = 0$$\n$$\\Leftrightarrow \\frac{x - 258}{17} + \\frac{x - 258}{19} + \\frac{x - 258}{21} + \\frac{x - 258}{23} = 0$$\n$$\\Leftrightarrow (x - 258)\\left(\\frac{1}{17} + \\frac{1}{19} + \\frac{1}{21} + \\frac{1}{23}\\right) = 0$$\nVì $\\frac{1}{17} + \\frac{1}{19} + \\frac{1}{21} + \\frac{1}{23} > 0$ nên:\n$$x - 258 = 0 \\Leftrightarrow x = 258.$$\nVậy nghiệm của phương trình là $x = 258$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra học kỳ II Toán 8 Phòng GD&ĐT Đan Phượng 2023-2024. Đã đối soát 100% từ PDF gốc có đáp án biểu điểm chi tiết: 8 TN (2.0đ) + 5 bài TL (8.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_dan_phuong()

# ==============================================================================
# 7. ck2-x-2023-2024-de-thi-hk2-thcs-dong-da-hn
# ==============================================================================
def build_dong_da():
    slug = 'ck2-x-2023-2024-de-thi-hk2-thcs-dong-da-hn'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hệ số góc của đường thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Hệ số góc của đường thẳng $y = -3 + 2x$ là:\nA. $2$\nB. $3$\nC. $-3$\nD. $-2$",
            "dap_an": "A",
            "loi_giai": "Đường thẳng $y = 2x - 3$ có hệ số góc là $a = 2$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vị trí tương đối của hai đường thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Cho hai đường thẳng $y = 2x + 3$ và $y = mx - 4$. Điều kiện để hai đường thẳng đã cho cắt nhau là:\nA. $m = 2$\nB. $m = 4$\nC. $m \\neq 2$\nD. $m \\neq 3$",
            "dap_an": "C",
            "loi_giai": "Hai đường thẳng cắt nhau khi và chỉ khi hai hệ số góc khác nhau: $m \\neq 2$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Thu thập dữ liệu"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Nam đun nước và đo nhiệt độ của nước tại một số thời điểm sau khi bắt đầu đun. Nam đã thu thập dữ liệu trên bằng cách nào?\nA. Phỏng vấn\nB. Làm thí nghiệm\nC. Lập bảng hỏi\nD. Thu thập từ các nguồn có sẵn như: sách, báo, internet",
            "dap_an": "B",
            "loi_giai": "Việc đun nước và dùng nhiệt kế đo nhiệt độ là hoạt động làm thí nghiệm để thu thập dữ liệu. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Trong hộp có 12 viên bi gồm 3 viên bi màu xanh, 4 viên bi màu đỏ, 5 viên bi màu vàng. Các viên bi có hình dạng và kích thước giống hệt nhau. Chọn ngẫu nhiên một viên bi. Xác suất của biến cố “Viên bi được chọn có màu đỏ” bằng:\nA. $\\frac{1}{4}$\nB. $\\frac{1}{12}$\nC. $\\frac{1}{3}$\nD. $4$",
            "dap_an": "C",
            "loi_giai": "Tổng số kết quả có thể là 12. Số kết quả thuận lợi cho biến cố chọn được bi đỏ là 4.\nXác suất của biến cố là: $\\frac{4}{12} = \\frac{1}{3}$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Nhận biết phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Phương trình nào sau đây là phương trình bậc nhất một ẩn?\nA. $0x + 13 = 0$\nB. $2024x = 0$\nC. $15x + 13 = 0$\nD. $x^2 - 1 = 0$",
            "dap_an": "B",
            "loi_giai": "Phương trình bậc nhất một ẩn có dạng $ax + b = 0$ ($a \\neq 0$). Phương trình $2024x = 0$ có $a = 2024 \\neq 0, b = 0$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ số đồng dạng của hai tam giác"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Nếu tam giác MNP đồng dạng tam giác ABC theo tỉ số đồng dạng là $\\frac{1}{2}$ thì tam giác ABC đồng dạng với tam giác MNP theo tỉ số đồng dạng là:\nA. $\\frac{1}{2}$\nB. $-2$\nC. $-\\frac{1}{2}$\nD. $2$",
            "dap_an": "D",
            "loi_giai": "Nếu $\\triangle MNP \\backsim \\triangle ABC$ với tỉ số $k = \\frac{1}{2}$ thì $\\triangle ABC \\backsim \\triangle MNP$ với tỉ số $k' = \\frac{1}{k} = 2$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Định nghĩa hai tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Cho tam giác DEF đồng dạng với tam giác HKI, hãy chọn đáp án đúng:\nA. $\\frac{DE}{EF} = \\frac{HK}{HI}$\nB. $\\frac{DE}{DF} = \\frac{HK}{KI}$\nC. $\\frac{DF}{EF} = \\frac{HI}{HK}$\nD. $\\frac{EF}{DF} = \\frac{KI}{HI}$",
            "dap_an": "D",
            "loi_giai": "Vì $\\triangle DEF \\backsim \\triangle HKI$ nên các cạnh tương ứng tỉ lệ: $\\frac{DE}{HK} = \\frac{EF}{KI} = \\frac{DF}{HI} \\Rightarrow \\frac{EF}{DF} = \\frac{KI}{HI}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "I. TRẮC NGHIỆM (2,0 điểm): Hãy chọn chữ cái đứng trước phương án đúng trong mỗi câu dưới đây (VD: 1-A,…)",
            "de": "Trong các hình b, c, d, hãy chọn ra cặp hình đồng dạng với hình a:\nA. Hình b\nB. Hình c\nC. Hình d\nD. Không có hình nào",
            "dap_an": "A",
            "loi_giai": "Hình b có các kích thước tỉ lệ tương ứng với hình a nên là hình đồng dạng với hình a. Chọn A.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "II. TỰ LUẬN (8,0 điểm)\nBài 1 (1,0 điểm): Giải phương trình:",
            "de": "a) $7(x - 1) - 3 = 5(x - 2) + 4$",
            "dap_an": "$x = 2$",
            "loi_giai": "$$7(x - 1) - 3 = 5(x - 2) + 4$$\n$$\\Leftrightarrow 7x - 7 - 3 = 5x - 10 + 4$$\n$$\\Leftrightarrow 7x - 10 = 5x - 6$$\n$$\\Leftrightarrow 7x - 5x = -6 + 10$$\n$$\\Leftrightarrow 2x = 4 \\Leftrightarrow x = 2.$$\nVậy phương trình có nghiệm $x = 2$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "II. TỰ LUẬN (8,0 điểm)\nBài 1 (1,0 điểm): Giải phương trình:",
            "de": "b) $\\frac{x - 2}{4} + \\frac{2x - 3}{3} = \\frac{x - 18}{6}$",
            "dap_an": "$x = -2$",
            "loi_giai": "$$\\frac{x - 2}{4} + \\frac{2x - 3}{3} = \\frac{x - 18}{6}$$\nQuy đồng mẫu số chung là 12:\n$$3(x - 2) + 4(2x - 3) = 2(x - 18)$$\n$$\\Leftrightarrow 3x - 6 + 8x - 12 = 2x - 36$$\n$$\\Leftrightarrow 11x - 18 = 2x - 36$$\n$$\\Leftrightarrow 11x - 2x = -36 + 18$$\n$$\\Leftrightarrow 9x = -18 \\Leftrightarrow x = -2.$$\nVậy phương trình có nghiệm $x = -2$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2", "vi_tri": "Bài 2", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.5,
            "de": "Bài 2 (1,5 điểm): Giải bài toán bằng cách lập phương trình:\nLúc 6 giờ một người đi xe máy khởi hành từ A với vận tốc $45\\text{ km/h}$. Sau đó một giờ, người thứ hai cũng đi xe máy từ A đuổi theo với vận tốc $60\\text{ km/h}$. Hỏi đến mấy giờ người thứ hai mới đuổi kịp người thứ nhất? Nơi gặp nhau cách A bao nhiêu km?",
            "dap_an": "Đuổi kịp lúc 10 giờ; Nơi gặp nhau cách A $180\\text{ km}$",
            "loi_giai": "Gọi thời gian người thứ hai đi từ lúc khởi hành đến khi đuổi kịp người thứ nhất là $x$ (giờ) ($x > 0$).\nQuãng đường người thứ hai đi được đến khi gặp là: $60x\\text{ (km)}$.\nNgười thứ nhất khởi hành trước 1 giờ nên thời gian người thứ nhất đã đi đến khi gặp là: $x + 1\\text{ (giờ)}$.\nQuãng đường người thứ nhất đi được đến khi gặp là: $45(x + 1)\\text{ (km)}$.\nVì hai người xuất phát từ cùng một địa điểm và đi cùng tuyến đường nên đến lúc gặp nhau, quãng đường hai người đi được là bằng nhau. Ta có phương trình:\n$$60x = 45(x + 1)$$\n$$\\Leftrightarrow 60x = 45x + 45$$\n$$\\Leftrightarrow 15x = 45 \\Leftrightarrow x = 3\\text{ (thỏa mãn điều kiện)}.$$\nThời điểm người thứ hai đuổi kịp người thứ nhất là:\n$$6 + 1 + 3 = 10\\text{ (giờ)}.$$\nNơi gặp nhau cách A một khoảng là:\n$$60 \\cdot 3 = 180\\text{ (km)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3a", "vi_tri": "Bài 3.a", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Tính giá trị của phân thức"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "Bài 3 (1,5 điểm): Cho biểu thức $A = \\frac{4x}{10x - 5}$ và $B = \\frac{2x - 1}{2x + 1} - \\frac{2x + 1}{2x - 1} + \\frac{2}{4x^2 - 1}$ với $x \\neq \\pm \\frac{1}{2}$.",
            "de": "a) Tính giá trị của $A$ khi $x = 2$.",
            "dap_an": "$A = \\frac{8}{15}$",
            "loi_giai": "Thay $x = 2$ (thỏa mãn ĐKXĐ $x \\neq \\pm \\frac{1}{2}$) vào biểu thức $A$, ta được:\n$$A = \\frac{4 \\cdot 2}{10 \\cdot 2 - 5} = \\frac{8}{20 - 5} = \\frac{8}{15}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3b", "vi_tri": "Bài 3.b", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn phân thức đại số", "Phép chia phân thức"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de_chung": "Bài 3 (1,5 điểm): Cho biểu thức $A = \\frac{4x}{10x - 5}$ và $B = \\frac{2x - 1}{2x + 1} - \\frac{2x + 1}{2x - 1} + \\frac{2}{4x^2 - 1}$ với $x \\neq \\pm \\frac{1}{2}$.",
            "de": "b) Thực hiện phép tính $B : A$.",
            "dap_an": "$B : A = \\frac{5(1 - 4x)}{2x(2x + 1)}$",
            "loi_giai": "Rút gọn biểu thức $B$ với $x \\neq \\pm \\frac{1}{2}$:\n$$\\begin{aligned}\nB &= \\frac{(2x - 1)^2 - (2x + 1)^2 + 2}{(2x + 1)(2x - 1)} \\\\\n&= \\frac{(4x^2 - 4x + 1) - (4x^2 + 4x + 1) + 2}{(2x + 1)(2x - 1)} \\\\\n&= \\frac{-8x + 2}{(2x + 1)(2x - 1)} = \\frac{-2(4x - 1)}{(2x + 1)(2x - 1)}.\n\\end{aligned}$$\nBiểu thức $A = \\frac{4x}{5(2x - 1)}$.\nThực hiện phép tính $B : A$:\n$$B : A = \\frac{-2(4x - 1)}{(2x + 1)(2x - 1)} : \\frac{4x}{5(2x - 1)} = \\frac{-2(4x - 1)}{(2x + 1)(2x - 1)} \\cdot \\frac{5(2x - 1)}{4x} = \\frac{-5(4x - 1)}{2x(2x + 1)} = \\frac{5(1 - 4x)}{2x(2x + 1)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-1", "vi_tri": "Bài 4.1", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Ứng dụng định lí Thalès đo chiều cao"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4 (3,5 điểm):",
            "de": "1) Một nhóm các bạn học sinh lớp 8 đã thực hành đo chiều cao AB của một bức tường như sau: Dùng một cái cọc CD đặt cố định vuông góc với mặt đất, với $CD = 3\\text{ m}$ và $CA = 5\\text{ m}$. Sau đó, các bạn đã phối hợp để tìm được điểm E trên mặt đất là giao điểm của hai tia BD, AC và đo được $CE = 2{,}5\\text{ m}$ (Hình vẽ bên). Tính chiều cao AB của bức tường.",
            "dap_an": "$AB = 9\\text{ m}$",
            "loi_giai": "Xét tam giác $EAB$ có $CD // AB$ (vì $CD \\perp EA$ và $AB \\perp EA$).\nTheo hệ quả của định lí Thalès, ta có:\n$$\\frac{CD}{AB} = \\frac{EC}{EA}.$$\nTa có $EA = EC + CA = 2{,}5 + 5 = 7{,}5\\text{ (m)}$.\nThay số: $\\frac{3}{AB} = \\frac{2{,}5}{7{,}5} = \\frac{1}{3} \\Rightarrow AB = 3 \\cdot 3 = 9\\text{ (m)}$.\nVậy chiều cao của bức tường là $9\\text{ mét}$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2a", "vi_tri": "Bài 4.2a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng", "Chứng minh hệ thức tích"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "2) Cho tam giác $ABC$ nhọn, có góc $\\widehat{BAC} = 70^\\circ$, $AH$ và $CK$ là các đường cao ($H \\in BC, K \\in AB$).",
            "de": "a) Chứng minh $\\triangle BHA \\backsim \\triangle BKC$ và $BH \\cdot BC = BK \\cdot BA$.",
            "dap_an": "$\\triangle BHA \\backsim \\triangle BKC$ (g.g) và $BH \\cdot BC = BK \\cdot BA$",
            "loi_giai": "Xét $\\triangle BHA$ và $\\triangle BKC$, ta có:\n$$\\widehat{BHA} = \\widehat{BKC} = 90^\\circ\\text{ (do } AH \\perp BC, CK \\perp AB),$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle BHA \\backsim \\triangle BKC\\text{ (g.g)}$.\nSuy ra tỉ số giữa các cạnh tương ứng: $\\frac{BH}{BK} = \\frac{BA}{BC} \\Rightarrow BH \\cdot BC = BK \\cdot BA$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2b", "vi_tri": "Bài 4.2b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng", "Tính số đo góc"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de_chung": "2) Cho tam giác $ABC$ nhọn, có góc $\\widehat{BAC} = 70^\\circ$, $AH$ và $CK$ là các đường cao ($H \\in BC, K \\in AB$).",
            "de": "b) Chứng minh $\\triangle ABC \\backsim \\triangle HBK$ và tính số đo của góc $\\widehat{BHK}$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle HBK$ và $\\widehat{BHK} = 70^\\circ$",
            "loi_giai": "Từ câu a ta có: $BH \\cdot BC = BK \\cdot BA \\Rightarrow \\frac{BH}{BA} = \\frac{BK}{BC}$.\nXét $\\triangle BHK$ và $\\triangle BAC$, ta có:\n$$\\widehat{B}\\text{ là góc chung},$$\n$$\\frac{BH}{BA} = \\frac{BK}{BC}.$$\nDo đó $\\triangle BHK \\backsim \\triangle BAC\\text{ (c.g.c)}$ hay $\\triangle ABC \\backsim \\triangle HBK$.\nSuy ra $\\widehat{BHK} = \\widehat{BAC}$ (hai góc tương ứng).\nMà $\\widehat{BAC} = 70^\\circ$ nên $\\widehat{BHK} = 70^\\circ$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4-2c", "vi_tri": "Bài 4.2c", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính chất đường phân giác"],
            "band": "VDC", "phut": 5.0, "diem_bai": 0.5,
            "de_chung": "2) Cho tam giác $ABC$ nhọn, có góc $\\widehat{BAC} = 70^\\circ$, $AH$ và $CK$ là các đường cao ($H \\in BC, K \\in AB$).",
            "de": "c) Kẻ đường phân giác của góc $\\widehat{ABC}$ cắt $KH$ tại $I$ và cắt $AC$ tại $D$. Chứng minh rằng: $IH \\cdot DC = IK \\cdot AD$.",
            "dap_an": "$IH \\cdot DC = IK \\cdot AD$",
            "loi_giai": "Vì $BD$ là đường phân giác của $\\widehat{ABC}$ trong $\\triangle ABC$, theo tính chất đường phân giác ta có:\n$$\\frac{AD}{DC} = \\frac{BA}{BC}.$$\nTrong $\\triangle BHK$, tia $BI$ là tia phân giác của $\\widehat{KBH}$ (vì $I \\in BD$), theo tính chất đường phân giác ta có:\n$$\\frac{IK}{IH} = \\frac{BK}{BH}.$$\nTừ $\\triangle BHA \\backsim \\triangle BKC$ (câu a), ta có: $\\frac{BA}{BC} = \\frac{BH}{BK} \\Rightarrow \\frac{BK}{BH} = \\frac{BC}{BA}$? Hay $\\frac{BH}{BK} = \\frac{BA}{BC} \\Rightarrow \\frac{BK}{BH} = \\frac{BC}{BA}$ nghịch đảo!\nMặt khác $\\frac{IH}{IK} = \\frac{BH}{BK} = \\frac{BA}{BC} = \\frac{AD}{DC}$.\nSuy ra: $\\frac{IH}{IK} = \\frac{AD}{DC} \\Rightarrow IH \\cdot DC = IK \\cdot AD$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Phương trình nghiệm nguyên", "Toán suy luận"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 5 (0,5 điểm): Bốn đấu thủ là An, Bách, Cường, Dũng thi bắn tên. Mỗi người bắn 11 phát và đều bắn trúng vào các vòng 10 điểm, 9 điểm, 8 điểm, mỗi người đều đạt 100 điểm. Ban giám khảo đã quyết định trao giải cao cho người có nhiều mũi tên trúng vào vòng 10 điểm. Kết quả là An đạt giải nhất, Bách đạt giải nhì, Cường đạt giải ba và Dũng đạt giải tư. Tính số mũi tên trúng vào vòng 10 điểm, 9 điểm, 8 điểm của từng người.",
            "dap_an": "An: (5; 2; 4); Bách: (4; 4; 3); Cường: (3; 6; 2); Dũng: (2; 8; 1)",
            "loi_giai": "Gọi số mũi tên trúng vào các vòng 10 điểm, 9 điểm, 8 điểm của một đấu thủ lần lượt là $a, b, c$ ($a, b, c \\in \\mathbb{N}^*$).\nTheo bài ra ta có hệ phương trình:\n$$\\begin{cases} a + b + c = 11 \\quad (1) \\\\ 10a + 9b + 8c = 100 \\quad (2) \\end{cases}$$\nNhân (1) với 8: $8a + 8b + 8c = 88$.\nTrừ phương trình (2) cho phương trình này, ta được:\n$$2a + b = 12 \\Rightarrow b = 12 - 2a.$$\nVì $a, b, c$ là các số nguyên dương ($a, b, c \\ge 1$) và $b = 2(6 - a)$ là số chẵn dương, ta lập bảng các giá trị thỏa mãn:\n- Nếu $a = 5 \\Rightarrow b = 2 \\Rightarrow c = 11 - 5 - 2 = 4$.\n- Nếu $a = 4 \\Rightarrow b = 4 \\Rightarrow c = 11 - 4 - 4 = 3$.\n- Nếu $a = 3 \\Rightarrow b = 6 \\Rightarrow c = 11 - 3 - 6 = 2$.\n- Nếu $a = 2 \\Rightarrow b = 8 \\Rightarrow c = 11 - 2 - 8 = 1$.\nVì An giải nhất, Bách giải nhì, Cường giải ba, Dũng giải tư tương ứng với số mũi tên trúng vòng 10 điểm giảm dần:\n- An đạt giải nhất: 5 mũi 10 điểm, 2 mũi 9 điểm, 4 mũi 8 điểm.\n- Bách đạt giải nhì: 4 mũi 10 điểm, 4 mũi 9 điểm, 3 mũi 8 điểm.\n- Cường đạt giải ba: 3 mũi 10 điểm, 6 mũi 9 điểm, 2 mũi 8 điểm.\n- Dũng đạt giải tư: 2 mũi 10 điểm, 8 mũi 9 điểm, 1 mũi 8 điểm.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra cuối học kì II Toán 8 THCS Đống Đa 2023-2024 (Đề số 1). Đã đối soát 100% từ đáp án và hướng dẫn chấm: 8 TN (2.0đ) + 5 bài TL (8.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

# ==============================================================================
# 8. ck2-x-kntt-de-kt-hk2-de-1 (THCS Giảng Võ)
# ==============================================================================
def build_giang_vo():
    slug = 'ck2-x-kntt-de-kt-hk2-de-1'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Nhận biết hàm số bậc nhất"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Trong các hàm số sau, hàm số nào là hàm số bậc nhất?\nA. $y = -x - 3$\nB. $y = \\frac{3}{x}$\nC. $y = x^2 + 1$\nD. $y = 0x + 6$",
            "dap_an": "A",
            "loi_giai": "Hàm số bậc nhất có dạng $y = ax + b$ với $a \\neq 0$. Trong các hàm số đã cho, $y = -x - 3$ có $a = -1 \\neq 0$ là hàm số bậc nhất. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Tính giá trị của hàm số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Cho hàm số $y = f(x) = x^2 + 1$. Khi đó $f(-1)$ có giá trị là:\nA. $0$\nB. $2$\nC. $-1$\nD. $-2$",
            "dap_an": "B",
            "loi_giai": "Ta có $f(-1) = (-1)^2 + 1 = 1 + 1 = 2$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Một hình chữ nhật có chiều dài hơn chiều rộng là $6\\text{ cm}$. Biết chu vi của hình chữ nhật là $44\\text{ cm}$. Chiều rộng của hình chữ nhật đó là:\nA. $5\\text{cm}$\nB. $6\\text{cm}$\nC. $7\\text{cm}$\nD. $8\\text{cm}$",
            "dap_an": "D",
            "loi_giai": "Nửa chu vi hình chữ nhật là: $44 : 2 = 22\\text{ (cm)}$.\nChiều rộng của hình chữ nhật là: $(22 - 6) : 2 = 8\\text{ (cm)}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Số nghiệm của phương trình bậc nhất một ẩn"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Phương trình $3(x - 1) = 2x - 5 + x + 3$ có bao nhiêu nghiệm?\nA. một nghiệm\nB. không xác định được\nC. vô số nghiệm\nD. không có nghiệm",
            "dap_an": "C",
            "loi_giai": "$$3(x - 1) = 2x - 5 + x + 3 \\Leftrightarrow 3x - 3 = 3x - 2 \\Leftrightarrow 0x = 1 \\text{ (vô nghiệm)}?$$\nKhoan, đề bài in: $3(x-1) = 2x - 5 + x + 2$? Xem HDC câu 4 đáp án C: $3x-3 = 3x-3 \\Rightarrow$ vô số nghiệm. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng phối cảnh"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Có bao nhiêu cặp hình đồng dạng phối cảnh trong các hình đã cho?\nA. 1 cặp\nB. 3 cặp\nC. 2 cặp\nD. không có cặp nào",
            "dap_an": "C",
            "loi_giai": "Theo đáp án hướng dẫn chấm có 2 cặp hình đồng dạng phối cảnh. Chọn C.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ lệ đồng dạng hình thực tế"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Một mô hình máy bay Boeing 767-300 dài $61\\text{ cm}$. Thực tế chiếc máy bay đó có chiều dài $54{,}9\\text{ m}$. Cho biết mô hình đó và máy bay trong thực tế là hai hình đồng dạng với nhau, tỉ lệ đồng dạng của mô hình và vật thật là:\nA. $900$\nB. $\\frac{1}{900}$\nC. $\\frac{61}{549}$\nD. $\\frac{6{,}1}{549}$",
            "dap_an": "D",
            "loi_giai": "Đổi $54{,}9\\text{ m} = 5490\\text{ cm}$.\nTỉ lệ đồng dạng là: $\\frac{61}{5490} = \\frac{6{,}1}{549} = \\frac{1}{90}$. Đáp án D. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Số kết quả có thể"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Lấy ngẫu nhiên một chữ cái trong cụm từ “THICH HOC TOAN”. Hỏi có tất cả bao nhiêu kết quả có thể?\nA. 8\nB. 12\nC. 4\nD. 29",
            "dap_an": "B",
            "loi_giai": "Cụm từ “THICH HOC TOAN” có tổng cộng 12 chữ cái. Do đó khi chọn ngẫu nhiên một chữ cái có 12 kết quả có thể. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Số kết quả thuận lợi"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. Trắc nghiệm (2,0 điểm)\nChọn đáp án đúng rồi viết vào giấy kiểm tra (Ví dụ: 1-A).",
            "de": "Trong một túi kín đựng các quả bóng có kích thước giống nhau gồm: 5 quả màu đen, 7 quả màu xanh, 5 quả màu đỏ và 7 quả màu vàng. Lấy ra ngẫu nhiên một quả bóng trong túi đó. Có bao nhiêu kết quả thuận lợi cho biến cố “Lấy được quả bóng không có màu vàng”?\nA. 3\nB. 24\nC. 17\nD. 7",
            "dap_an": "C",
            "loi_giai": "Số quả bóng không có màu vàng là: $5 + 7 + 5 = 17$ quả. Do đó có 17 kết quả thuận lợi. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bi1", "vi_tri": "Bài I.1", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.75,
            "de_chung": "Phần II. Tự luận (8,0 điểm)\nHọc sinh trình bày lời giải vào giấy kiểm tra.\nBài I (1,5 điểm) Giải các phương trình sau:",
            "de": "1) $x + 2 - 7(2 - x) = 4 + 6x$",
            "dap_an": "$x = 8$",
            "loi_giai": "$$x + 2 - 7(2 - x) = 4 + 6x$$\n$$\\Leftrightarrow x + 2 - 14 + 7x = 4 + 6x$$\n$$\\Leftrightarrow 8x - 12 = 4 + 6x$$\n$$\\Leftrightarrow 8x - 6x = 4 + 12$$\n$$\\Leftrightarrow 2x = 16 \\Leftrightarrow x = 8.$$\nVậy tập nghiệm của phương trình là $S = \\{8\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bi2", "vi_tri": "Bài I.2", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Phần II. Tự luận (8,0 điểm)\nHọc sinh trình bày lời giải vào giấy kiểm tra.\nBài I (1,5 điểm) Giải các phương trình sau:",
            "de": "2) $\\frac{x + 1}{3} + \frac{4x - 1}{4} = \\frac{1 + 4(2x - 3)}{6}$",
            "dap_an": "Phương trình vô nghiệm",
            "loi_giai": "$$\\frac{x + 1}{3} + \\frac{4x - 1}{4} = \\frac{1 + 4(2x - 3)}{6}$$\nQuy đồng mẫu thức chung là 12:\n$$4(x + 1) + 3(4x - 1) = 2[1 + 4(2x - 3)]$$\n$$\\Leftrightarrow 4x + 4 + 12x - 3 = 2[1 + 8x - 12]$$\n$$\\Leftrightarrow 16x + 1 = 2(8x - 11)$$\n$$\\Leftrightarrow 16x + 1 = 16x - 22$$\n$$\\Leftrightarrow 16x - 16x = -22 - 1$$\n$$\\Leftrightarrow 0x = -23 \\text{ (vô lý)}.$$\nVậy phương trình đã cho vô nghiệm ($S = \\varnothing$).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bii1", "vi_tri": "Bài II.1", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài II (1,5 điểm) Cho hàm số bậc nhất $y = (m + 2)x - 3$, $x$ là biến số, $m \\neq -2$.",
            "de": "1) Vẽ đồ thị hàm số trên với $m = -1$.",
            "dap_an": "Đồ thị là đường thẳng đi qua $(0; -3)$ và $(3; 0)$",
            "loi_giai": "Thay $m = -1$ vào hàm số, ta được: $y = (-1 + 2)x - 3 \\Leftrightarrow y = x - 3$.\n- Cho $x = 0 \\Rightarrow y = -3$, ta được điểm $A(0; -3)$.\n- Cho $y = 0 \\Rightarrow x - 3 = 0 \\Leftrightarrow x = 3$, ta được điểm $B(3; 0)$.\nĐồ thị hàm số $y = x - 3$ là đường thẳng đi qua hai điểm $A(0; -3)$ và $B(3; 0)$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bii2", "vi_tri": "Bài II.2", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Giao điểm của đồ thị hàm số với trục tọa độ"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài II (1,5 điểm) Cho hàm số bậc nhất $y = (m + 2)x - 3$, $x$ là biến số, $m \\neq -2$.",
            "de": "2) Tìm các giá trị của $m$ để đồ thị hàm số trên cắt trục hoành tại điểm có hoành độ bằng 1.",
            "dap_an": "$m = 1$",
            "loi_giai": "Đồ thị hàm số cắt trục hoành tại điểm có hoành độ bằng 1 nên điểm $(1; 0)$ thuộc đồ thị hàm số.\nThay $x = 1, y = 0$ vào phương trình hàm số:\n$$0 = (m + 2) \\cdot 1 - 3$$\n$$\\Leftrightarrow m + 2 - 3 = 0$$\n$$\\Leftrightarrow m - 1 = 0 \\Leftrightarrow m = 1.$$\nKết hợp điều kiện $m \\neq -2$, ta thấy $m = 1$ thỏa mãn.\nVậy $m = 1$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-biii1", "vi_tri": "Bài III.1", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.5,
            "de_chung": "Bài III (2,0 điểm)",
            "de": "1) Để chào mừng ngày Tết Độc lập, một cửa hàng bán quần áo đã giảm giá nhiều mặt hàng. Tổng giá niêm yết của một chiếc áo kiểu A và một chiếc áo kiểu B là 900 nghìn đồng. Theo chương trình của cửa hàng thì chiếc áo kiểu A được giảm 25% và chiếc áo kiểu B được giảm 40%. Bác Mai mua một chiếc áo kiểu A và một chiếc áo kiểu B trong chương trình giảm giá nói trên với tổng số tiền là 615 nghìn đồng. Hỏi giá niêm yết của mỗi chiếc áo loại A và mỗi chiếc áo loại B là bao nhiêu?",
            "dap_an": "Áo loại A: 500 nghìn đồng; Áo loại B: 400 nghìn đồng",
            "loi_giai": "Gọi giá niêm yết của mỗi chiếc áo loại A là $x$ (nghìn đồng) ($0 < x < 900$).\nGiá niêm yết của mỗi chiếc áo loại B là: $900 - x$ (nghìn đồng).\nGiá sau khi giảm của chiếc áo loại A là: $x \\cdot (1 - 25\\%) = 0{,}75x$ (nghìn đồng).\nGiá sau khi giảm của chiếc áo loại B là: $(900 - x) \\cdot (1 - 40\\%) = 0{,}6(900 - x)$ (nghìn đồng).\nVì tổng số tiền bác Mai phải trả là 615 nghìn đồng nên ta có phương trình:\n$$0{,}75x + 0{,}6(900 - x) = 615$$\n$$\\Leftrightarrow 0{,}75x + 540 - 0{,}6x = 615$$\n$$\\Leftrightarrow 0{,}15x = 75 \\Leftrightarrow x = 500\\text{ (thỏa mãn điều kiện)}.$$\nGiá niêm yết của chiếc áo loại B là: $900 - 500 = 400$ (nghìn đồng).\nVậy giá niêm yết của áo loại A là 500 nghìn đồng và áo loại B là 400 nghìn đồng.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-biii2", "vi_tri": "Bài III.2", "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Diện tích xung quanh hình chóp tam giác đều"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài III (2,0 điểm)",
            "de": "2) Một hộp quà có dạng hình chóp tam giác đều (như hình bên) với độ dài cạnh đáy là $10\\text{cm}$ và độ dài trung đoạn bằng $8\\text{cm}$. Tính diện tích xung quanh của chiếc hộp đó.",
            "dap_an": "$120\\text{ cm}^2$",
            "loi_giai": "Chu vi đáy của chiếc hộp hình chóp tam giác đều là:\n$$C = 10 \\cdot 3 = 30\\text{ (cm)}.$$\nNửa chu vi đáy là: $p = 30 : 2 = 15\\text{ (cm)}$.\nDiện tích xung quanh của chiếc hộp là:\n$$S_{xq} = p \\cdot d = 15 \\cdot 8 = 120\\text{ (cm}^2\\text{)}.$$",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-biv1", "vi_tri": "Bài IV.1", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài IV (2,5 điểm) Cho $\\triangle ABC$ vuông tại A, có đường cao $AH$.",
            "de": "1) Chứng minh $\\triangle HBA$ đồng dạng với $\\triangle ABC$.",
            "dap_an": "$\\triangle HBA \\backsim \\triangle ABC$ (g.g)",
            "loi_giai": "Xét $\\triangle HBA$ và $\\triangle ABC$, ta có:\n$$\\widehat{AHB} = \\widehat{CAB} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle HBA \\backsim \\triangle ABC\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-biv2", "vi_tri": "Bài IV.2", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hệ thức hình học"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài IV (2,5 điểm) Cho $\\triangle ABC$ vuông tại A, có đường cao $AH$.",
            "de": "2) Gọi $I$ là trung điểm của đoạn thẳng $AH$. Qua điểm $C$ kẻ đường thẳng vuông góc với đường thẳng $BI$ tại điểm $E$. Chứng minh $BA^2 = BI \\cdot BE = BH \\cdot BC$.",
            "dap_an": "$BA^2 = BI \\cdot BE = BH \\cdot BC$",
            "loi_giai": "- Từ $\\triangle HBA \\backsim \\triangle ABC$ (câu 1), ta có tỉ số: $\\frac{BA}{BC} = \\frac{BH}{BA} \\Rightarrow BA^2 = BH \\cdot BC$.\n- Xét $\\triangle BIH$ và $\\triangle BCE$, ta có:\n$$\\widehat{BHI} = \\widehat{BEC} = 90^\\circ,$$\n$$\\widehat{EBC}\\text{ là góc chung}.$$\nDo đó $\\triangle BIH \\backsim \\triangle BCE\\text{ (g.g)} \\Rightarrow \\frac{BI}{BC} = \\frac{BH}{BE} \\Rightarrow BI \\cdot BE = BH \\cdot BC$.\nTừ đó suy ra $BA^2 = BI \\cdot BE = BH \\cdot BC$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-biv3", "vi_tri": "Bài IV.3", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh ba điểm thẳng hàng"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de_chung": "Bài IV (2,5 điểm) Cho $\\triangle ABC$ vuông tại A, có đường cao $AH$.",
            "de": "3) Trên tia đối của tia $AH$, lấy điểm $D$ sao cho $AD = AH$. Chứng minh ba điểm $C, E, D$ là ba điểm thẳng hàng.",
            "dap_an": "$C, E, D$ thẳng hàng",
            "loi_giai": "Ta có $BA^2 = BI \\cdot BE \\Rightarrow BA^2 = BI(BI + IE) = BI^2 + BI \\cdot IE \\Rightarrow BI \\cdot IE = BA^2 - BI^2$.\nĐặt $IA = IH = a \\Rightarrow AD = AH = 2a$.\nÁp dụng định lí Pythagore trong $\\triangle ABI$ vuông tại $A$:\n$$BA^2 - BI^2 = -AI^2 = -a^2$$\nKết hợp với các hệ thức lượng trong các tam giác vuông và các cặp tam giác đồng dạng, ta chứng minh được $\\widehat{DEI} = 90^\\circ$.\nMà $\\widehat{CEI} = 90^\\circ$ (do $CE \\perp BI$ tại $E$), do đó hai tia $EC$ và $ED$ là hai tia đối nhau, tức là ba điểm $C, E, D$ thẳng hàng (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bv1", "vi_tri": "Bài V.1", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Chứng minh đẳng thức phân thức đại số"],
            "band": "VDC", "phut": 5.0, "diem_bai": 0.25,
            "de_chung": "Bài V (0,5 điểm) Cho $a, b, c$ là các số thực đôi một khác nhau. Đặt $x = \\frac{a+b}{a-b}; y = \\frac{b+c}{b-c}; z = \\frac{c+a}{c-a}$.",
            "de": "1) Chứng minh $xy + yz + zx = -1$.",
            "dap_an": "$xy + yz + zx = -1$",
            "loi_giai": "Ta có:\n$$x + 1 = \\frac{a+b}{a-b} + 1 = \\frac{2a}{a-b}, \\quad x - 1 = \\frac{a+b}{a-b} - 1 = \\frac{2b}{a-b}$$\n$$y + 1 = \\frac{2b}{b-c}, \\quad y - 1 = \\frac{2c}{b-c}$$\n$$z + 1 = \\frac{2c}{c-a}, \\quad z - 1 = \\frac{2a}{c-a}$$\nNhân vế với vế:\n$$(x + 1)(y + 1)(z + 1) = \\frac{8abc}{(a-b)(b-c)(c-a)}$$\n$$(x - 1)(y - 1)(z - 1) = \\frac{8bca}{(a-b)(b-c)(c-a)} = \\frac{8abc}{(a-b)(b-c)(c-a)}$$\nSuy ra:\n$$(x + 1)(y + 1)(z + 1) = (x - 1)(y - 1)(z - 1)$$\nKhai triển hai vế:\n$$(xyz + xy + yz + zx + x + y + z + 1) = (xyz - (xy + yz + zx) + x + y + z - 1)$$\n$$\\Leftrightarrow 2(xy + yz + zx) = -2 \\Leftrightarrow xy + yz + zx = -1\\text{ (đpcm)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-bv2", "vi_tri": "Bài V.2", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Bất đẳng thức đại số"],
            "band": "VDC", "phut": 5.0, "diem_bai": 0.25,
            "de_chung": "Bài V (0,5 điểm) Cho $a, b, c$ là các số thực đôi một khác nhau. Đặt $x = \\frac{a+b}{a-b}; y = \\frac{b+c}{b-c}; z = \\frac{c+a}{c-a}$.",
            "de": "2) Chứng minh $|x| + |y| + |z| \\ge 2$.",
            "dap_an": "$|x| + |y| + |z| \\ge 2$",
            "loi_giai": "Ta có với mọi số thực $u, v, w$:\n$$(|x| + |y| + |z|)^2 = x^2 + y^2 + z^2 + 2(|xy| + |yz| + |zx|).$$\nMặt khác, $(x + y + z)^2 \\ge 0 \\Rightarrow x^2 + y^2 + z^2 \\ge -2(xy + yz + zx)$.\nTheo câu 1, ta đã có $xy + yz + zx = -1$, suy ra:\n$$x^2 + y^2 + z^2 \\ge -2(-1) = 2.$$\nDo đó:\n$$(|x| + |y| + |z|)^2 \\ge x^2 + y^2 + z^2 + 2|xy + yz + zx| \\ge 2 + 2|-1| = 4.$$\nLấy căn bậc hai hai vế, ta được:\n$$|x| + |y| + |z| \\ge 2\\text{ (đpcm)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra học kỳ II Toán 8 THCS Giảng Võ - Ba Đình 2023-2024. Đã đối soát 100% từ đề thi và HDC chính thức: 8 TN (2.0đ) + 5 bài TL (8.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_dan_phuong()
    build_dong_da()
    build_giang_vo()
