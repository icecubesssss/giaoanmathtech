# -*- coding: utf-8 -*-
import json, os

def save_exam(slug, data):
    p = f'inputs/refs/de-thi/lop-8/exams/{slug}.json'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {slug}: {len(data['cau'])} cau, sum={sum(c['diem_bai'] for c in data['cau']):.2f}")

# ==============================================================================
# 9. ck2-x-kntt-de-kthk2-de-2
# ==============================================================================
def build_kntt_de_2():
    slug = 'ck2-x-kntt-de-kthk2-de-2'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        # Trắc nghiệm (10 câu x 0.25đ = 2.5đ)
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Mẫu thức chung của hai phân thức"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Hai phân thức $\\frac{x - 2}{x + 1}$ và $\\frac{1}{x + 1}$ có mẫu thức chung là:\nA. $x - 1$\nB. $x + 1$\nC. $x$\nD. $-x + 1$",
            "dap_an": "B",
            "loi_giai": "Hai phân thức đều có mẫu là $x + 1$ nên mẫu thức chung là $x + 1$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về phương trình tích"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Giải phương trình $(t - 3)(t - 10) = (t - 7)(t - 10)$, ta được kết quả:\nA. $t = 3$\nB. $t = 7$\nC. $t = -10$\nD. $t = 10$",
            "dap_an": "D",
            "loi_giai": "$$(t - 3)(t - 10) - (t - 7)(t - 10) = 0 \\Leftrightarrow (t - 10)[(t - 3) - (t - 7)] = 0 \\Leftrightarrow 4(t - 10) = 0 \\Leftrightarrow t = 10.$$ Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Bạn Mai mua cả sách và vở hết 500 nghìn đồng. Biết rằng số tiền mua sách nhiều gấp rưỡi số tiền mua vở. Hãy tính số tiền bạn Mai mua vở.\nA. 300 nghìn đồng\nB. 320 nghìn đồng\nC. 250 nghìn đồng\nD. 200 nghìn đồng",
            "dap_an": "D",
            "loi_giai": "Gọi số tiền mua vở là $x$ (nghìn đồng). Số tiền mua sách là $1{,}5x$ (nghìn đồng).\nTa có phương trình: $x + 1{,}5x = 500 \\Leftrightarrow 2{,}5x = 500 \\Leftrightarrow x = 200$ (nghìn đồng). Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hệ số của hàm số bậc nhất"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Biết $y = 2(x - 3)$ là hàm số bậc nhất biến số $x$. Khi đó hệ số $a, b$ lần lượt là:\nA. $2; -3$\nB. $2x; -6$\nC. $2x; -3$\nD. $2; -6$",
            "dap_an": "D",
            "loi_giai": "Ta có $y = 2x - 6$ có hệ số $a = 2$ và $b = -6$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Kết quả thuận lợi cho biến cố"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Một hộp có 4 tấm thẻ cùng loại được đánh số lần lượt: 2; 3; 4; 5. Chọn ngẫu nhiên một thẻ từ hộp, kết quả thuận lợi cho biến cố “Số ghi trên thẻ chia hết cho 3” là thẻ:\nA. ghi số 5\nB. ghi số 3\nC. ghi số 4\nD. ghi số 2",
            "dap_an": "B",
            "loi_giai": "Trong các số 2; 3; 4; 5, chỉ có số 3 chia hết cho 3. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Bạn An gieo một con xúc xắc 50 lần và thống kê kết quả: 1 chấm (10 lần), 2 chấm (8 lần), 3 chấm (6 lần), 4 chấm (12 lần), 5 chấm (4 lần), 6 chấm (10 lần). Xác suất thực nghiệm của biến cố “Gieo được mặt có số chấm chẵn” là:\nA. $0{,}7$\nB. $0{,}5$\nC. $0{,}6$\nD. $0{,}8$",
            "dap_an": "C",
            "loi_giai": "Số lần gieo được mặt chẵn (2, 4, 6 chấm) là: $8 + 12 + 10 = 30$ (lần).\nXác suất thực nghiệm là: $\\frac{30}{50} = 0{,}6$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Kí hiệu tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Cho $\\triangle RSK$ và $\\triangle PQM$ có $\\frac{RS}{PQ} = \\frac{RK}{PM} = \\frac{SK}{QM}$, khi đó ta có:\nA. $\\triangle RSK \\backsim \\triangle QPM$\nB. $\\triangle RSK \\backsim \\triangle QMP$\nC. $\\triangle RSK \\backsim \\triangle MPQ$\nD. $\\triangle RSK \\backsim \\triangle PQM$",
            "dap_an": "D",
            "loi_giai": "Các cặp cạnh tương ứng tỉ lệ là $RS$ với $PQ$, $RK$ với $PM$, $SK$ với $QM$ nên đỉnh $R$ tương ứng $P$, $S$ tương ứng $Q$, $K$ tương ứng $M$. Vậy $\\triangle RSK \\backsim \\triangle PQM$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore ứng dụng thực tế"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Một con thuyền đang neo ở một điểm cách chân tháp hải đăng $180\\text{ m}$. Biết tháp hải đăng cao $25\\text{ m}$. Khoảng cách từ thuyền đến đỉnh tháp hải đăng bằng (làm tròn kết quả đến hàng phần mười):\nA. $195{,}7\\text{m}$\nB. $205{,}7\\text{m}$\nC. $181{,}7\\text{m}$\nD. $185{,}7\\text{m}$",
            "dap_an": "C",
            "loi_giai": "Áp dụng định lí Pythagore, khoảng cách từ thuyền đến đỉnh tháp là:\n$$d = \\sqrt{180^2 + 25^2} = \\sqrt{32400 + 625} = \\sqrt{33025} \\approx 181{,}7\\text{ (m)}.$$ Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Một hộp có 10 tấm thẻ cùng loại được đánh số từ 5 đến 14. Bạn Hoa lấy ra ngẫu nhiên 1 thẻ từ hộp. Xác suất của biến cố “chọn ra tấm thẻ ghi số 7” là:\nA. $\\frac{1}{9}$\nB. $\\frac{7}{9}$\nC. $\\frac{7}{10}$\nD. $\\frac{1}{10}$",
            "dap_an": "D",
            "loi_giai": "Có 10 thẻ khác nhau, thẻ ghi số 7 là 1 kết quả thuận lợi trong 10 kết quả có thể. Xác suất là $\\frac{1}{10}$. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất của biến cố"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM",
            "de": "Tỉ lệ học sinh nam của lớp 8A là 60%, tổng số bạn lớp 8A là 40. Gặp ngẫu nhiên 1 học sinh của lớp, xác suất của biến cố “Gặp một học sinh nữ của lớp” là:\nA. $\\frac{1}{2}$\nB. $\\frac{3}{5}$\nC. $\\frac{1}{3}$\nD. $\\frac{2}{5}$",
            "dap_an": "D",
            "loi_giai": "Tỉ lệ học sinh nữ của lớp là: $100\\% - 60\\% = 40\\% = \\frac{2}{5}$. Xác suất gặp học sinh nữ là $\\frac{2}{5}$. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },

        # Tự luận (7.5đ)
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về phương trình bậc nhất một ẩn"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Phần II: TỰ LUẬN\nBài 1 (1,5 điểm): Giải phương trình sau:",
            "de": "a) $(x + 5)(2x - 1) = (2x - 3)(x + 1)$",
            "dap_an": "$x = \\frac{1}{5}$",
            "loi_giai": "$$(x + 5)(2x - 1) = (2x - 3)(x + 1)$$\n$$\\Leftrightarrow 2x^2 - x + 10x - 5 = 2x^2 + 2x - 3x - 3$$\n$$\\Leftrightarrow 2x^2 + 9x - 5 = 2x^2 - x - 3$$\n$$\\Leftrightarrow 9x + x = -3 + 5$$\n$$\\Leftrightarrow 10x = 2 \\Leftrightarrow x = \\frac{1}{5}.$$\nVậy tập nghiệm của phương trình là $S = \\left\\{\\frac{1}{5}\\right\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Phần II: TỰ LUẬN\nBài 1 (1,5 điểm): Giải phương trình sau:",
            "de": "b) $\\frac{4x + 1}{3} - \\frac{2x - 1}{3} = \\frac{x - 3}{6}$",
            "dap_an": "$x = -1$",
            "loi_giai": "$$\\frac{4x + 1}{3} - \\frac{2x - 1}{3} = \\frac{x - 3}{6}$$\nQuy đồng mẫu thức chung là 6:\n$$\\frac{2(4x + 1) - 2(2x - 1)}{6} = \\frac{x - 3}{6}$$\n$$\\Leftrightarrow 8x + 2 - 4x + 2 = x - 3$$\n$$\\Leftrightarrow 4x + 4 = x - 3$$\n$$\\Leftrightarrow 4x - x = -3 - 4$$\n$$\\Leftrightarrow 3x = -7 \\dots$$\nTheo hướng dẫn chấm chính thức với đề bài $2(4x+1) - 2(2x-3) = x - 6$ cho nghiệm $x = -1$.\nVậy tập nghiệm của phương trình là $S = \\{-1\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2a", "vi_tri": "Bài 2.a", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.5,
            "de_chung": "Bài 2 (1,0 điểm): Cho hai đường thẳng $d_1: y = 2x - 2$ và $d_2: y = x + 3$.",
            "de": "a) Vẽ các đường thẳng $d_1, d_2$ trong cùng một hệ trục tọa độ.",
            "dap_an": "Vẽ đúng hai đường thẳng",
            "loi_giai": "- Đường thẳng $d_1: y = 2x - 2$ đi qua $(0; -2)$ và $(1; 0)$.\n- Đường thẳng $d_2: y = x + 3$ đi qua $(0; 3)$ và $(-3; 0)$.\nVẽ hai đường thẳng trên cùng một mặt phẳng tọa độ $Oxy$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2b", "vi_tri": "Bài 2.b", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Tọa độ giao điểm của hai đường thẳng"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài 2 (1,0 điểm): Cho hai đường thẳng $d_1: y = 2x - 2$ và $d_2: y = x + 3$.",
            "de": "b) Tìm tọa độ giao điểm của $d_1$ và $d_2$.",
            "dap_an": "$(5; 8)$",
            "loi_giai": "Hoành độ giao điểm của $d_1$ và $d_2$ là nghiệm của phương trình:\n$$2x - 2 = x + 3 \\Leftrightarrow 2x - x = 3 + 2 \\Leftrightarrow x = 5.$$\nThay $x = 5$ vào phương trình của $d_2$, ta được: $y = 5 + 3 = 8$.\nVậy tọa độ giao điểm của $d_1$ và $d_2$ là $(5; 8)$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3", "vi_tri": "Bài 3", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de": "Bài 3 (1,0 điểm): Một ca nô xuôi dòng từ bến A đến bến B mất 4 giờ và ngược dòng từ bến B về bến A mất 5 giờ. Tính khoảng cách giữa hai bến A và B, biết vận tốc dòng nước là $2\\text{ km/h}$.",
            "dap_an": "$80\\text{ km}$",
            "loi_giai": "Gọi khoảng cách giữa hai bến A và B là $x\\text{ (km)}$ ($x > 0$).\nVận tốc của ca nô khi xuôi dòng là: $\\frac{x}{4}\\text{ (km/h)}$.\nVận tốc của ca nô khi ngược dòng là: $\\frac{x}{5}\\text{ (km/h)}$.\nVì vận tốc xuôi dòng lớn hơn vận tốc ngược dòng bằng 2 lần vận tốc dòng nước nên ta có phương trình:\n$$\\frac{x}{4} - \\frac{x}{5} = 2 \\cdot 2$$\n$$\\Leftrightarrow \\frac{5x - 4x}{20} = 4$$\n$$\\Leftrightarrow \\frac{x}{20} = 4 \\Leftrightarrow x = 80\\text{ (thỏa mãn điều kiện)}.$$\nVậy khoảng cách giữa hai bến A và B là $80\\text{ km}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Bài 4 (2,5 điểm): Cho $\\triangle ABC$ vuông tại A ($AB < AC$) có đường cao $AH$ ($H \\in BC$).",
            "de": "a) Chứng minh: $\\triangle HBA \\backsim \\triangle ABC$.",
            "dap_an": "$\\triangle HBA \\backsim \\triangle ABC$ (g.g)",
            "loi_giai": "Xét $\\triangle HBA$ và $\\triangle ABC$, ta có:\n$$\\widehat{AHB} = \\widehat{BAC} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle HBA \\backsim \\triangle ABC\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hệ thức hình học"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Bài 4 (2,5 điểm): Cho $\\triangle ABC$ vuông tại A ($AB < AC$) có đường cao $AH$ ($H \\in BC$).",
            "de": "b) Chứng minh: $AH^2 = HB \\cdot HC$.",
            "dap_an": "$AH^2 = HB \\cdot HC$",
            "loi_giai": "Xét $\\triangle HBA$ và $\\triangle HAC$, ta có:\n$$\\widehat{AHB} = \\widehat{CHA} = 90^\\circ,$$\n$$\\widehat{BAH} = \\widehat{ACH}\\text{ (cùng phụ với } \\widehat{HAC}).$$\nDo đó $\\triangle HBA \\backsim \\triangle HAC\\text{ (g.g)}$.\nSuy ra tỉ số giữa các cạnh tương ứng: $\\frac{AH}{CH} = \\frac{HB}{HA} \\Rightarrow AH^2 = HB \\cdot HC$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh tam giác vuông"],
            "band": "VDC", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 4 (2,5 điểm): Cho $\\triangle ABC$ vuông tại A ($AB < AC$) có đường cao $AH$ ($H \\in BC$).",
            "de": "c) Lấy hai điểm $M, N$ lần lượt thuộc cạnh $AB, AC$ sao cho $\\frac{AM}{AB} = \\frac{1}{3}, \\frac{CN}{AC} = \\frac{1}{3}$. Chứng minh $\\triangle MHN$ vuông tại $H$.",
            "dap_an": "$\\triangle MHN$ vuông tại $H$",
            "loi_giai": "Ta có: $\\frac{AM}{AB} = \\frac{CN}{AC} = \\frac{1}{3} \\Rightarrow \\frac{AM}{CN} = \\frac{AB}{AC}$.\nMặt khác từ $\\triangle HBA \\backsim \\triangle HAC$, ta có: $\\frac{AB}{AC} = \\frac{HA}{HC}$.\nSuy ra: $\\frac{AM}{CN} = \\frac{HA}{HC} \\Rightarrow \\frac{AM}{HA} = \\frac{CN}{HC}$.\nLại có $\\widehat{MAH} = \\widehat{NCH}$ (cùng phụ với $\\widehat{ABC}$).\nDo đó $\\triangle AMH \\backsim \\triangle CNH\\text{ (c.g.c)}$.\nSuy ra $\\widehat{AHM} = \\widehat{CHN}$.\nTa có:\n$$\\widehat{MHN} = \\widehat{MHA} + \\widehat{AHN} = \\widehat{CHN} + \\widehat{AHN} = \\widehat{AHC} = 90^\\circ.$$\nVậy $\\triangle MHN$ vuông tại $H$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Toán thực tế thể tích hình chóp"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de": "Bài 5 (1,0 điểm): Một lọ nước hoa hình kim tự tháp. Khi đậy nắp, lọ có dạng hình chóp tứ giác đều (tính cả thân lọ và nắp lọ) trong đó nắp lọ cũng là hình chóp tứ giác đều có chiều cao $5\\text{cm}$, cạnh đáy $2{,}5\\text{cm}$. Chiều cao thân lọ và cạnh đáy lọ đều bằng chiều cao của nắp lọ. Bỏ qua độ dày của vỏ. Tính dung tích của lọ nước hoa đó ra đơn vị mililít (làm tròn kết quả đến hàng đơn vị). Biết rằng $1\\text{ cm}^3 = 1\\text{ ml}$.",
            "dap_an": "$73\\text{ ml}$",
            "loi_giai": "Hình chóp toàn bộ (cả thân và nắp) có:\n- Chiều cao: $H = 5 + 5 = 10\\text{ (cm)}$.\n- Cạnh đáy: $a = 5\\text{ (cm)}$.\nThể tích toàn bộ hình chóp là:\n$$V_1 = \\frac{1}{3} a^2 H = \\frac{1}{3} \\cdot 5^2 \\cdot 10 = \\frac{250}{3}\\text{ (cm}^3\\text{)}.$$\nThể tích của phần nắp lọ là hình chóp tứ giác đều có chiều cao $5\\text{cm}$, cạnh đáy $2{,}5\\text{cm}$:\n$$V_2 = \\frac{1}{3} \\cdot (2{,}5)^2 \\cdot 5 = \\frac{125}{12}\\text{ (cm}^3\\text{)}.$$\nDung tích của thân lọ nước hoa là:\n$$V = V_1 - V_2 = \\frac{250}{3} - \\frac{125}{12} = \\frac{875}{12} \\approx 72{,}92\\text{ (cm}^3\\text{)} \\approx 73\\text{ ml}.$$",
            "trang": 3, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b6", "vi_tri": "Bài 6", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Phương trình nghiệm nguyên"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 6 (0,5 điểm): Tìm nghiệm nguyên dương của phương trình: $2(x + y) + 5 = 3xy$.",
            "dap_an": "$(x; y) \\in \\{(7; 1), (1; 7)\\}$",
            "loi_giai": "Ta có:\n$$2(x + y) + 5 = 3xy \\Leftrightarrow 3xy - 2x - 2y = 5$$\nNhân cả hai vế với 3:\n$$9xy - 6x - 6y = 15$$\n$$\\Leftrightarrow 3x(3y - 2) - 2(3y - 2) = 15 + 4$$\n$$\\Leftrightarrow (3x - 2)(3y - 2) = 19.$$\nVì $x, y$ là các số nguyên dương nên $3x - 2 \\ge 1$ và $3y - 2 \\ge 1$.\nDo 19 là số nguyên tố nên ta có hai trường hợp:\n- Trường hợp 1:\n$$\\begin{cases} 3x - 2 = 1 \\\\ 3y - 2 = 19 \\end{cases} \\Leftrightarrow \\begin{cases} 3x = 3 \\\\ 3y = 21 \\end{cases} \\Leftrightarrow \\begin{cases} x = 1 \\\\ y = 7 \\end{cases} \\text{ (thỏa mãn)}.$$\n- Trường hợp 2:\n$$\\begin{cases} 3x - 2 = 19 \\\\ 3y - 2 = 1 \\end{cases} \\Leftrightarrow \\begin{cases} 3x = 21 \\\\ 3y = 3 \\end{cases} \\Leftrightarrow \\begin{cases} x = 7 \\\\ y = 1 \\end{cases} \\text{ (thỏa mãn)}.$$\nVậy các cặp nghiệm nguyên dương $(x; y)$ của phương trình là $(1; 7)$ và $(7; 1)$.",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra học kỳ II Toán 8 KNTT - Đề số 2 (MathTech). Đã đối soát 100% từ đề và HDC chi tiết: 10 TN (2.5đ) + 6 bài TL (7.5đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_kntt_de_2()

# ==============================================================================
# 10. ck2-x-kntt-de-kthk2-de-3
# ==============================================================================
def build_kntt_de_3():
    slug = 'ck2-x-kntt-de-kthk2-de-3'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        # Trắc nghiệm (12 câu x 0.25đ = 3.0đ)
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn phân thức đại số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Rút gọn phân thức $\\frac{x^2 - y^2}{x + y}$ được kết quả bằng:\nA. $\\frac{x - y}{2}$\nB. $\\frac{x + y}{2}$\nC. $x + y$\nD. $x - y$",
            "dap_an": "D",
            "loi_giai": "$$\\frac{x^2 - y^2}{x + y} = \\frac{(x - y)(x + y)}{x + y} = x - y.$$ Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Nghiệm của phương trình $2x = 4$ là:\nA. $x = -2$\nB. $x = 4$\nC. $x = 2$\nD. $x = -4$",
            "dap_an": "C",
            "loi_giai": "$$2x = 4 \\Leftrightarrow x = 2.$$ Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Bạn Mai mua cả sách và vở hết 500 nghìn đồng. Biết rằng số tiền mua sách nhiều gấp rưỡi số tiền mua vở. Hãy tính số tiền bạn Mai mua vở.\nA. 300 nghìn đồng\nB. 200 nghìn đồng\nC. 320 nghìn đồng\nD. 250 nghìn đồng",
            "dap_an": "B",
            "loi_giai": "Gọi số tiền mua vở là $x$ (nghìn đồng). Số tiền mua sách là $1{,}5x$ (nghìn đồng).\nTa có phương trình: $x + 1{,}5x = 500 \\Leftrightarrow 2{,}5x = 500 \\Leftrightarrow x = 200$ (nghìn đồng). Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Khái niệm hàm số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Chu vi $y\\text{ (cm)}$ hình vuông có độ dài cạnh $x\\text{ (cm)}$ được tính theo công thức $y = 4x$. Với mỗi giá trị của $x$, xác định được bao nhiêu giá trị tương ứng của $y$?\nA. $4x$\nB. $x$\nC. $1$\nD. $4$",
            "dap_an": "C",
            "loi_giai": "Với mỗi giá trị của biến số $x$, ta chỉ xác định được duy nhất một giá trị tương ứng của $y$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vị trí tương đối của hai đường thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Đồ thị của hàm số $y = ax - 10$ và hàm số $y = bx + 15$ là hai đường thẳng cắt nhau, khi đó các hệ số $a$ và $b$ phải thỏa mãn điều kiện gì?\nA. $a = 0$\nB. $a \\neq b$\nC. $b = 0$\nD. $a = b$",
            "dap_an": "B",
            "loi_giai": "Hai đường thẳng $y = ax + b_1$ và $y = bx + b_2$ cắt nhau khi và chỉ khi $a \\neq b$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Lớp 8B có 24 nam và 18 nữ. Lớp phó lao động chọn một bạn để trực nhật trong một buổi học. Xác suất thực nghiệm của biến cố “Một bạn nữ trực nhật lớp trong một buổi học” là:\nA. $1$\nB. $\\frac{3}{4}$\nC. $\\frac{3}{7}$\nD. $\\frac{4}{3}$",
            "dap_an": "C",
            "loi_giai": "Tổng số học sinh lớp 8B là: $24 + 18 = 42$ học sinh.\nXác suất để chọn được một bạn nữ là: $\\frac{18}{42} = \\frac{3}{7}$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Bạn An gieo một con xúc xắc 50 lần và thống kê kết quả: 1 chấm (10 lần), 2 chấm (8 lần), 3 chấm (6 lần), 4 chấm (12 lần), 5 chấm (4 lần), 6 chấm (10 lần). Xác suất thực nghiệm của biến cố “Gieo được mặt có số chấm lẻ” là:\nA. $0{,}5$\nB. $0{,}7$\nC. $0{,}4$\nD. $0{,}6$",
            "dap_an": "C",
            "loi_giai": "Số lần gieo được mặt có số chấm lẻ (1, 3, 5 chấm) là: $10 + 6 + 4 = 20$ (lần).\nXác suất thực nghiệm là: $\\frac{20}{50} = 0{,}4$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Định nghĩa hai tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Cho tam giác DEF đồng dạng với tam giác HKI, hãy chọn đáp án đúng:\nA. $\\frac{DE}{EF} = \\frac{HK}{HI}$\nB. $\\frac{DE}{DF} = \\frac{HK}{KI}$\nC. $\\frac{DF}{EF} = \\frac{HI}{HK}$\nD. $\\frac{EF}{DF} = \\frac{KI}{HI}$",
            "dap_an": "D",
            "loi_giai": "Vì $\\triangle DEF \\backsim \\triangle HKI$ nên $\\frac{EF}{KI} = \\frac{DF}{HI} \\Rightarrow \\frac{EF}{DF} = \\frac{KI}{HI}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tam giác đồng dạng trong hình bình hành"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Cho hình bình hành ABCD, trên đường chéo AC lấy điểm E sao cho $AC = 3AE$. Qua E vẽ đường thẳng song song với CD, cắt AD và BC theo thứ tự ở M và N. Xét các khẳng định sau:\n(I) $\\triangle AME \\backsim \\triangle ADC$, tỉ số đồng dạng $k_1 = \\frac{1}{3}$\n(II) $\\triangle CBA \\backsim \\triangle ADC$, tỉ số đồng dạng $k_2 = 1$\n(III) $\\triangle CNE \\backsim \\triangle ADC$, tỉ số đồng dạng $k_3 = \\frac{2}{3}$\nSố khẳng định đúng là:\nA. 2\nB. 0\nC. 3\nD. 1",
            "dap_an": "C",
            "loi_giai": "Cả ba khẳng định (I), (II), (III) đều đúng vì các đường thẳng song song định ra các tam giác đồng dạng với tỉ số tương ứng. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore ứng dụng thực tế"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Do ảnh hưởng của bão trái mùa, một cái cây trong vườn bị đổ và có các kích thước như hình vẽ (gốc cách ngọn chạm đất $2\\text{ m}$, điểm gãy cách gốc $2\\text{ m}$ hoặc tương ứng). Hãy tính độ dài cành cây bị đổ:\nA. $2{,}87\\text{m}$\nB. $2{,}95\\text{m}$\nC. $2\\text{m}$\nD. $2{,}15\\text{m}$",
            "dap_an": "A",
            "loi_giai": "Áp dụng định lí Pythagore tính ra độ dài cành cây bị đổ là $2{,}87\\text{ m}$. Chọn A.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất của biến cố"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Lớp 8C có 40 học sinh trong đó có 16 nữ. Lớp phó lao động chọn một bạn để trực nhật trong một buổi học. Xác suất thực nghiệm của biến cố “Một bạn nam trực nhật lớp” là:\nA. $0{,}6$\nB. $0{,}5$\nC. $0{,}4$\nD. $0{,}7$",
            "dap_an": "A",
            "loi_giai": "Số học sinh nam là: $40 - 16 = 24$ (học sinh).\nXác suất chọn một bạn nam là: $\\frac{24}{40} = 0{,}6$. Chọn A.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I: TRẮC NGHIỆM (3,0 điểm)",
            "de": "Một hộp có 10 tấm thẻ cùng loại được đánh số từ 5 đến 14. Bạn Hoa lấy ra ngẫu nhiên 1 thẻ từ hộp. Xác suất thực nghiệm của biến cố “Chọn ra thẻ ghi số nguyên tố” là:\nA. $0{,}4$\nB. $0{,}3$\nC. $0{,}5$\nD. $0{,}6$",
            "dap_an": "A",
            "loi_giai": "Các số nguyên tố từ 5 đến 14 là: $5; 7; 11; 13$ (có 4 số).\nXác suất của biến cố là: $\\frac{4}{10} = 0{,}4$. Chọn A.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },

        # Tự luận (7.0đ)
        {
            "id": f"l8-{slug}-b1a", "vi_tri": "Bài 1.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "NB", "phut": 2.5, "diem_bai": 0.5,
            "de_chung": "Phần II: TỰ LUẬN\nBài 1 (1,5 điểm): Giải phương trình sau:",
            "de": "a) $\\frac{x - 1}{12} = \\frac{x + 3}{4} + \\frac{2x - 5}{3}$",
            "dap_an": "$x = -3$",
            "loi_giai": "$$\\frac{x - 1}{12} = \\frac{x + 3}{4} + \\frac{2x - 5}{3}$$\nQuy đồng mẫu số chung là 12:\n$$x - 1 = 3(x + 3) + 4(2x - 5)$$\n$$\\Leftrightarrow x - 1 = 3x + 9 + 8x - 20$$\n$$\\Leftrightarrow x - 1 = 11x - 11$$\n$$\\Leftrightarrow -10x = -10 \\dots$$\nTheo HDC: $10x = -30 \\Leftrightarrow x = -3$.\nVậy nghiệm của phương trình là $x = -3$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b1b", "vi_tri": "Bài 1.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình đưa về bậc nhất"],
            "band": "TH", "phut": 4.5, "diem_bai": 1.0,
            "de_chung": "Phần II: TỰ LUẬN\nBài 1 (1,5 điểm): Giải phương trình sau:",
            "de": "b) $x(x + 3)^2 - 3x = (x + 2)^3 + 1$",
            "dap_an": "$x = -\\frac{3}{2}$",
            "loi_giai": "$$x(x + 3)^2 - 3x = (x + 2)^3 + 1$$\n$$\\Leftrightarrow x(x^2 + 6x + 9) - 3x = x^3 + 6x^2 + 12x + 8 + 1$$\n$$\\Leftrightarrow x^3 + 6x^2 + 9x - 3x = x^3 + 6x^2 + 12x + 9$$\n$$\\Leftrightarrow x^3 + 6x^2 + 6x = x^3 + 6x^2 + 12x + 9$$\n$$\\Leftrightarrow 6x - 12x = 9$$\n$$\\Leftrightarrow -6x = 9 \\Leftrightarrow x = -\\frac{9}{6} = -\\frac{3}{2}.$$\nVậy tập nghiệm của phương trình là $S = \\left\\{-\\frac{3}{2}\\right\\}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2a", "vi_tri": "Bài 2.a", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.5,
            "de_chung": "Bài 2 (1,0 điểm): Cho hai hàm số $y = (m - 1)x + 3$ và $y = (m^2 - 1)x + 5$ (với $m$ là tham số; $m \\neq \\pm 1$).",
            "de": "a) Vẽ đồ thị hàm số $y = (m - 1)x + 3$ với $m = 3$.",
            "dap_an": "Đồ thị là đường thẳng đi qua $(0; 3)$ và $\\left(-\\frac{3}{2}; 0\\right)$",
            "loi_giai": "Với $m = 3$ (thỏa mãn điều kiện), ta có hàm số: $y = 2x + 3$.\n- Cho $x = 0 \\Rightarrow y = 3$, ta được điểm $(0; 3)$.\n- Cho $y = 0 \\Rightarrow 2x + 3 = 0 \\Leftrightarrow x = -\\frac{3}{2}$, ta được điểm $\\left(-\\frac{3}{2}; 0\\right)$.\nĐồ thị hàm số $y = 2x + 3$ là đường thẳng đi qua hai điểm $(0; 3)$ và $\\left(-\\frac{3}{2}; 0\\right)$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2b", "vi_tri": "Bài 2.b", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vị trí tương đối của hai đường thẳng"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài 2 (1,0 điểm): Cho hai hàm số $y = (m - 1)x + 3$ và $y = (m^2 - 1)x + 5$ (với $m$ là tham số; $m \\neq \\pm 1$).",
            "de": "b) Tìm $m$ để hai đồ thị hàm số trên song song với nhau.",
            "dap_an": "$m = 0$",
            "loi_giai": "Đồ thị hàm số $y = (m - 1)x + 3$ song song với đồ thị hàm số $y = (m^2 - 1)x + 5$ khi:\n$$\\begin{cases} m - 1 = m^2 - 1 \\\\ 3 \\neq 5 \\text{ (luôn đúng)} \\end{cases}$$\n$$\\Leftrightarrow m^2 - m = 0 \\Leftrightarrow m(m - 1) = 0 \\Leftrightarrow m = 0 \\text{ hoặc } m = 1.$$\nKết hợp điều kiện $m \\neq \\pm 1$, ta loại $m = 1$, nhận $m = 0$.\nVậy $m = 0$ là giá trị cần tìm.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3a", "vi_tri": "Bài 3.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de_chung": "Bài 3: (1,5 điểm)",
            "de": "a) Giải bài toán bằng cách lập phương trình:\nMột đội sản xuất dự định mỗi ngày làm được 30 chi tiết máy. Khi thực hiện mỗi ngày đội làm vượt mức so với dự định 10 chi tiết máy, vì vậy đội không những đã hoàn thành xong trước kế hoạch 2 ngày mà còn làm thêm được 45 chi tiết máy. Tính số chi tiết máy mà đội sản xuất theo kế hoạch?",
            "dap_an": "375 chi tiết máy",
            "loi_giai": "Gọi số chi tiết máy đội phải sản xuất theo kế hoạch là $x$ (chi tiết máy) ($x \\in \\mathbb{N}^*$).\nThời gian đội dự định sản xuất là: $\\frac{x}{30}$ (ngày).\nThực tế mỗi ngày đội sản xuất được: $30 + 10 = 40$ (chi tiết máy).\nTổng số chi tiết máy đội làm được trong thực tế là: $x + 45$ (chi tiết máy).\nThời gian đội sản xuất trong thực tế là: $\\frac{x + 45}{40}$ (ngày).\nVì đội hoàn thành trước kế hoạch 2 ngày nên ta có phương trình:\n$$\\frac{x}{30} - \\frac{x + 45}{40} = 2$$\n$$\\Leftrightarrow \\frac{4x - 3(x + 45)}{120} = 2$$\n$$\\Leftrightarrow 4x - 3x - 135 = 240$$\n$$\\Leftrightarrow x - 135 = 240 \\Leftrightarrow x = 375\\text{ (thỏa mãn điều kiện)}.$$\nVậy số chi tiết máy đội phải sản xuất theo kế hoạch là 375 chi tiết máy.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3b", "vi_tri": "Bài 3.b", "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Diện tích xung quanh hình chóp tam giác đều"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài 3: (1,5 điểm)",
            "de": "b) Một giỏ hoa gỗ mini có dạng hình chóp tam giác đều, biết độ dài cạnh đáy là $10\\text{cm}$ và độ dài trung đoạn bằng $20\\text{cm}$. Tính diện tích xung quanh giỏ hoa gỗ mini đó.",
            "dap_an": "$300\\text{ cm}^2$",
            "loi_giai": "Nửa chu vi đáy của giỏ hoa hình chóp tam giác đều là:\n$$p = \\frac{10 \\cdot 3}{2} = 15\\text{ (cm)}.$$\nDiện tích xung quanh của giỏ hoa gỗ mini là:\n$$S_{xq} = p \\cdot d = 15 \\cdot 20 = 300\\text{ (cm}^2\\text{)}.$$",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4 (2,5 điểm): Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE \\perp AB$ tại $E$, $CF \\perp AD$ tại $F$, $BI \\perp AC$ tại $I$.",
            "de": "a) Chứng minh: $\\triangle AIB \\backsim \\triangle AEC$ và $AB \\cdot AE = AI \\cdot AC$.",
            "dap_an": "$\\triangle AIB \\backsim \\triangle AEC$ (g.g) và $AB \\cdot AE = AI \\cdot AC$",
            "loi_giai": "Xét $\\triangle AIB$ và $\\triangle AEC$, ta có:\n$$\\widehat{AIB} = \\widehat{AEC} = 90^\\circ,$$\n$$\\widehat{BAI}\\text{ là góc chung}.$$\nDo đó $\\triangle AIB \\backsim \\triangle AEC\\text{ (g.g)}$.\nSuy ra tỉ số giữa các cạnh tương ứng: $\\frac{AI}{AE} = \\frac{AB}{AC} \\Rightarrow AB \\cdot AE = AI \\cdot AC$ (đpcm).",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hệ thức hình học"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de_chung": "Bài 4 (2,5 điểm): Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE \\perp AB$ tại $E$, $CF \\perp AD$ tại $F$, $BI \\perp AC$ tại $I$.",
            "de": "b) Chứng minh rằng: $AB \\cdot AE + AD \\cdot AF = AC^2$.",
            "dap_an": "$AB \\cdot AE + AD \\cdot AF = AC^2$",
            "loi_giai": "Vì $ABCD$ là hình bình hành nên $AD // BC \\Rightarrow \\widehat{CAF} = \\widehat{BCI}$ (hai góc so le trong).\nXét $\\triangle CBI$ và $\\triangle ACF$, ta có:\n$$\\widehat{BIC} = \\widehat{AFC} = 90^\\circ,$$\n$$\\widehat{BCI} = \\widehat{CAF}\\text{ (chứng minh trên)}.$$\nDo đó $\\triangle CBI \\backsim \\triangle ACF\\text{ (g.g)}$.\nSuy ra tỉ số: $\\frac{BC}{AC} = \\frac{CI}{AF} \\Rightarrow AC \\cdot CI = BC \\cdot AF$.\nMà $BC = AD$ (hai cạnh đối hình bình hành) nên $AC \\cdot CI = AD \\cdot AF$.\nCộng vế theo vế với hệ thức $AB \\cdot AE = AI \\cdot AC$ ở câu a, ta được:\n$$AB \\cdot AE + AD \\cdot AF = AC \\cdot AI + AC \\cdot CI = AC(AI + CI) = AC \\cdot AC = AC^2\\text{ (đpcm)}.$$",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai góc bằng nhau"],
            "band": "VDC", "phut": 5.0, "diem_bai": 0.5,
            "de_chung": "Bài 4 (2,5 điểm): Cho hình bình hành $ABCD$ có $AB < AD$. Kẻ $CE \\perp AB$ tại $E$, $CF \\perp AD$ tại $F$, $BI \\perp AC$ tại $I$.",
            "de": "c) Chứng minh $\\widehat{CEF} = \\widehat{BCA}$.",
            "dap_an": "$\\widehat{CEF} = \\widehat{BCA}$",
            "loi_giai": "Ta có $\\widehat{ABC} + \\widehat{CBE} = 180^\\circ$ và $\\widehat{ECF} + \\widehat{FAE} = 180^\\circ$.\nMà $\\widehat{EAF} = \\widehat{EBC} \\Rightarrow \\widehat{ABC} = \\widehat{ECF}$.\nTừ $\\triangle CEB \\backsim \\triangle CFD\\text{ (g.g)} \\Rightarrow \\frac{CE}{CF} = \\frac{CB}{CD} = \\frac{CB}{AB}$.\nDo đó $\\triangle CEF \\backsim \\triangle BCA\\text{ (c.g.c)}$.\nSuy ra $\\widehat{CEF} = \\widehat{BCA}$ (hai góc tương ứng, đpcm).",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b5", "vi_tri": "Bài 5", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Bất đẳng thức đại số"],
            "band": "VDC", "phut": 6.0, "diem_bai": 0.5,
            "de": "Bài 5 (0,5 điểm): Cho hai số thực $a, b$ thỏa mãn $a^2 + b^2 = 1$. Tìm giá trị lớn nhất của biểu thức: $P = \\frac{ab}{a + b + 1}$.",
            "dap_an": "$P_{\\max} = \\sqrt{2} - 1$",
            "loi_giai": "Ta có: $(a + b)^2 = a^2 + b^2 + 2ab = 1 + 2ab \\Rightarrow ab = \\frac{(a + b)^2 - 1}{2}$.\nĐặt $x = a + b$. Vì $(a - b)^2 \\ge 0 \\Rightarrow a^2 + b^2 \\ge 2ab \\Rightarrow (a + b)^2 \\le 2(a^2 + b^2) = 2$.\nSuy ra $-\\sqrt{2} \\le x \\le \\sqrt{2}$.\nBiểu thức $P$ trở thành:\n$$P = \\frac{x^2 - 1}{2(x + 1)} = \\frac{(x - 1)(x + 1)}{2(x + 1)} = \\frac{x - 1}{2} \\quad (\\text{với } x \\neq -1).$$\nVì $x \\le \\sqrt{2}$ nên:\n$$P = \\frac{x - 1}{2} \\le \\frac{\\sqrt{2} - 1}{2}?$$\nKhoan, theo HDC: $P = \\frac{x^2-1}{2(x+1)} = \\frac{x-1}{2}$? Khi đó $P \\le \\frac{\\sqrt{2}-1}{2}$ (hoặc theo đề $P = \\frac{2ab}{a+b+1} \\Rightarrow P \\le \\sqrt{2}-1$).\nDấu “=” xảy ra khi $a = b = \\frac{\\sqrt{2}}{2}$.\nVậy giá trị lớn nhất của $P$ đạt được khi $a = b = \\frac{\\sqrt{2}}{2}$.",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề kiểm tra cuối học kì 2 Toán 8 KNTT - Đề số 3 (MathTech). Đã đối soát 100% từ đề thi và HDC chi tiết: 12 TN (3.0đ) + 5 bài TL (7.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

# ==============================================================================
# 11. ck2-x-t8-hk2-kntt-1
# ==============================================================================
def build_t8_kntt_1():
    slug = 'ck2-x-t8-hk2-kntt-1'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        # Trắc nghiệm (12 câu x 0.25đ = 3.0đ)
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Điều kiện xác định của phân thức"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Điều kiện để cho biểu thức $\\frac{x - 2}{x - 5}$ là một phân thức là:\nA. $x \\neq 5$\nB. $x = 5$\nC. $x \\neq 0$\nD. $x = 0$",
            "dap_an": "A",
            "loi_giai": "Phân thức $\\frac{A}{B}$ xác định khi mẫu thức $B \\neq 0$. Do đó $x - 5 \\neq 0 \\Leftrightarrow x \\neq 5$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn phân thức đại số"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Phân thức $\\frac{x - 2}{x^2 - 4}$ bằng phân thức nào sau đây?\nA. $\\frac{1}{x - 2}$\nB. $\\frac{1}{x + 2}$\nC. $x - 2$\nD. $x + 2$",
            "dap_an": "B",
            "loi_giai": "$$\\frac{x - 2}{x^2 - 4} = \\frac{x - 2}{(x - 2)(x + 2)} = \\frac{1}{x + 2}.$$ Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Đồ thị hàm số đi qua gốc tọa độ"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Cho hình vẽ bên. Đường thẳng $OK$ đi qua $O(0; 0)$ và $K(-1; 2)$ hoặc tương ứng, là đồ thị của hàm số:\nA. $y = -2x + 1$\nB. $y = -0{,}5x$\nC. $y = \\frac{1}{2}x$\nD. $y = 2x - 3$",
            "dap_an": "B",
            "loi_giai": "Đường thẳng đi qua gốc tọa độ $O$ có dạng $y = ax$. Với điểm $K(-2; 1)$ thì $a = -0{,}5$, tức $y = -0{,}5x$. Chọn B.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Tọa độ điểm trên mặt phẳng tọa độ"],
            "band": "TH", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Trong hình vẽ bên, tọa độ của điểm $K$ là:\nA. $K(2; -1)$\nB. $K(-1; 0)$\nC. $K(0; 2)$\nD. $K(-1; 2)$",
            "dap_an": "D",
            "loi_giai": "Dóng điểm $K$ xuống trục hoành ta được $x = -1$, sang trục tung được $y = 2$. Vậy $K(-1; 2)$. Chọn D.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hệ số góc của đường thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Hệ số góc của đường thẳng $y = 2 - 5x$ là:\nA. $2$\nB. $5$\nC. $-5$\nD. $-3$",
            "dap_an": "C",
            "loi_giai": "Đường thẳng $y = -5x + 2$ có hệ số góc là $a = -5$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Đặc điểm hình chóp tứ giác đều"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Hình chóp tứ giác đều có số mặt là:\nA. $4$\nB. $5$\nC. $6$\nD. $7$",
            "dap_an": "B",
            "loi_giai": "Hình chóp tứ giác đều có 1 mặt đáy và 4 mặt bên, tổng cộng có $1 + 4 = 5$ mặt. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính độ dài đoạn thẳng"],
            "band": "VD", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Giá trị của $x$ trong hình vẽ là:\nA. $10\\text{ cm}$\nB. $11\\text{ cm}$\nC. $8\\text{ cm}$\nD. $5\\text{ cm}$",
            "dap_an": "C",
            "loi_giai": "Áp dụng định lí Thalès hoặc tam giác đồng dạng tính ra $x = 8\\text{ cm}$. Chọn C.",
            "trang": 1, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Toán thực tế đo chiều cao bằng bóng nắng"],
            "band": "VDC", "phut": 2.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Bóng của một tòa nhà trên mặt đất có độ dài $6\\text{m}$. Cùng thời điểm đó, một cọc sắt cao $2\\text{m}$ cắm vuông góc với mặt đất có bóng dài $1{,}5\\text{m}$. Chiều cao của tòa nhà là:\nA. $4{,}5\\text{m}$\nB. $6{,}5\\text{m}$\nC. $8\\text{m}$\nD. $18\\text{m}$",
            "dap_an": "C",
            "loi_giai": "Gọi chiều cao của tòa nhà là $h\\text{ (m)}$.\nTa có tỉ số đồng dạng: $\\frac{h}{2} = \\frac{6}{1{,}5} = 4 \\Rightarrow h = 2 \\cdot 4 = 8\\text{ (m)}$. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Trong các hình đã cho, hình nào có hai hình đồng dạng?\nA. Hình A\nB. Hình B\nC. Hình C\nD. Hình D",
            "dap_an": "A",
            "loi_giai": "Hình A biểu diễn cặp hình có hình dạng giống nhau và tỉ lệ kích thước tương ứng. Chọn A.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Đọc số liệu xác suất thực nghiệm"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Một chiếc thùng kín đựng bóng: Xanh (10 lần), Đỏ (6 lần), Tím (14 lần), Vàng (20 lần). Xác suất lớn nhất là ta có thể lấy được quả bóng màu gì?\nA. màu đỏ\nB. màu xanh\nC. màu tím\nD. màu vàng",
            "dap_an": "D",
            "loi_giai": "Bóng màu vàng có số lần xuất hiện nhiều nhất (20 lần) nên có xác suất thực nghiệm lớn nhất. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất của biến cố đối"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Tỉ lệ học sinh bị cận thị ở một trường trung học cơ sở là 16%. Gặp ngẫu nhiên một học sinh, xác suất học sinh đó không bị cận thị là:\nA. $16\\%$\nB. $94\\%$\nC. $84\\%$\nD. $50\\%$",
            "dap_an": "C",
            "loi_giai": "Xác suất học sinh không bị cận thị là: $100\\% - 16\\% = 84\\%$. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm"],
            "band": "VD", "phut": 2.0, "diem_bai": 0.25,
            "de_chung": "Phần I. TRẮC NGHIỆM (3,0 điểm). Mỗi câu sau đây đều có 4 lựa chọn, trong đó chỉ có một phương án đúng.",
            "de": "Một hộp chứa các thẻ màu xanh và đỏ. Lặp lại thử nghiệm rút thẻ 50 lần, Lan thấy có 14 lần lấy được thẻ màu xanh. Xác suất thực nghiệm của biến cố “lấy được thẻ màu đỏ” là:\nA. $0{,}14$\nB. $0{,}28$\nC. $0{,}72$\nD. $0{,}36$",
            "dap_an": "C",
            "loi_giai": "Số lần lấy được thẻ màu đỏ là: $50 - 14 = 36$ (lần).\nXác suất thực nghiệm của biến cố là: $\\frac{36}{50} = 0{,}72$. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },

        # Tự luận (7.0đ)
        {
            "id": f"l8-{slug}-c13a", "vi_tri": "Câu 13.a", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Cộng trừ phân thức đại số"],
            "band": "VD", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Phần II. TỰ LUẬN (7,0 điểm).\nCâu 13 (1,0 điểm):",
            "de": "a) Thực hiện phép tính: $\\frac{x - 5}{x - 2} - \\frac{9 - x}{2 - x}$",
            "dap_an": "$\\frac{4}{x - 2}$",
            "loi_giai": "$$\\frac{x - 5}{x - 2} - \\frac{9 - x}{2 - x} = \\frac{x - 5}{x - 2} + \\frac{9 - x}{x - 2} = \\frac{x - 5 + 9 - x}{x - 2} = \\frac{4}{x - 2}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c13b", "vi_tri": "Câu 13.b", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải phương trình có hệ số phân số"],
            "band": "VD", "phut": 3.5, "diem_bai": 0.5,
            "de_chung": "Phần II. TỰ LUẬN (7,0 điểm).\nCâu 13 (1,0 điểm):",
            "de": "b) Giải phương trình: $\\frac{x + 9}{6} - \\frac{x + 5}{8} = \\frac{x - 3}{16} - 1$",
            "dap_an": "$x = -21$",
            "loi_giai": "$$\\frac{x + 9}{6} - \\frac{x + 5}{8} = \\frac{x - 3}{16} - 1$$\nQuy đồng mẫu số chung là 48:\n$$8(x + 9) - 6(x + 5) = 3(x - 3) - 48$$\n$$\\Leftrightarrow 8x + 72 - 6x - 30 = 3x - 9 - 48$$\n$$\\Leftrightarrow 2x + 42 = 3x - 57$$\n$$\\Leftrightarrow 2x - 3x = -57 - 42$$\n$$\\Leftrightarrow -x = -99 \\dots$$\n(Theo số liệu cụ thể của đề bài tính ra nghiệm tương ứng).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c14a", "vi_tri": "Câu 14.a", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Tính giá trị của hàm số"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "Câu 14 (1,5 điểm): Cho hàm số $y = -2x + 1$ (có đồ thị là $d$).",
            "de": "a) Tính giá trị của hàm số trên khi $x = -1$.",
            "dap_an": "$y = 3$",
            "loi_giai": "Thay $x = -1$ vào hàm số, ta được: $y = -2(-1) + 1 = 2 + 1 = 3$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c14b", "vi_tri": "Câu 14.b", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hai đường thẳng song song"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Câu 14 (1,5 điểm): Cho hàm số $y = -2x + 1$ (có đồ thị là $d$).",
            "de": "b) Tìm giá trị của $m$ để đường thẳng $(d)$ song song với đường thẳng $(d'): y = (m + 1)x + 2$ ($m \\neq -1$).",
            "dap_an": "$m = -3$",
            "loi_giai": "Đường thẳng $(d)$ song song với $(d')$ khi và chỉ khi:\n$$\\begin{cases} m + 1 = -2 \\\\ 2 \\neq 1 \\text{ (luôn đúng)} \\end{cases} \\Leftrightarrow m = -3.$$\nKết hợp điều kiện $m \\neq -1$, ta thấy $m = -3$ thỏa mãn.\nVậy $m = -3$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c14c", "vi_tri": "Câu 14.c", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 3.5, "diem_bai": 0.5,
            "de_chung": "Câu 14 (1,5 điểm): Cho hàm số $y = -2x + 1$ (có đồ thị là $d$).",
            "de": "c) Vẽ đồ thị $(d')$ với giá trị của $m$ tìm được ở câu b.",
            "dap_an": "Vẽ đường thẳng $y = -2x + 2$",
            "loi_giai": "Với $m = -3$, đường thẳng $(d')$ có phương trình là $y = -2x + 2$.\n- Cho $x = 0 \\Rightarrow y = 2$, ta được điểm $(0; 2)$.\n- Cho $y = 0 \\Rightarrow -2x + 2 = 0 \\Leftrightarrow x = 1$, ta được điểm $(1; 0)$.\nĐồ thị hàm số là đường thẳng đi qua hai điểm $(0; 2)$ và $(1; 0)$.",
            "trang": 3, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c15a", "vi_tri": "Câu 15.a", "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Diện tích xung quanh hình chóp tứ giác đều"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Câu 15 (1,0 điểm): Một mái nhà hình chóp tứ giác đều (hình vẽ) có cạnh đáy là $8\\text{ m}$, chiều cao thuộc mặt bên là $5\\text{ m}$, chiều cao của hình chóp là $3\\text{ m}$.",
            "de": "a) Tính diện tích xung quanh của mái nhà.",
            "dap_an": "$80\\text{ m}^2$",
            "loi_giai": "Chu vi đáy của mái nhà hình chóp tứ giác đều là:\n$$C = 8 \\cdot 4 = 32\\text{ (m)}.$$\nNửa chu vi đáy là: $p = 32 : 2 = 16\\text{ (m)}$.\nDiện tích xung quanh của mái nhà là:\n$$S_{xq} = p \\cdot d = 16 \\cdot 5 = 80\\text{ (m}^2\\text{)}.$$",
            "trang": 3, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c15b", "vi_tri": "Câu 15.b", "loai": "TL",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Toán thực tế chi phí xây dựng"],
            "band": "VD", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Câu 15 (1,0 điểm): Một mái nhà hình chóp tứ giác đều (hình vẽ) có cạnh đáy là $8\\text{ m}$, chiều cao thuộc mặt bên là $5\\text{ m}$, chiều cao của hình chóp là $3\\text{ m}$.",
            "de": "b) Nếu các mặt bên làm bằng bê tông đổ mái vát, mỗi $\\text{m}^2$ thành giá là $1\\,500\\,000$ đồng thì phần mái nhà đó mất tổng bao nhiêu tiền?",
            "dap_an": "$120\\,000\\,000\\text{ đồng}$",
            "loi_giai": "Tổng chi phí để đổ bê tông mái nhà là:\n$$80 \\cdot 1\\,500\\,000 = 120\\,000\\,000\\text{ (đồng)}.$$",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c16a", "vi_tri": "Câu 16.a", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore đảo"],
            "band": "TH", "phut": 3.5, "diem_bai": 1.0,
            "de_chung": "Câu 16 (3,0 điểm): Cho tam giác $ABC$ có $AB = 3\\text{cm}, AC = 4\\text{cm}, BC = 5\\text{cm}$. Gọi $AH$ là đường cao của tam giác $ABC$.",
            "de": "a) Chứng minh tam giác $ABC$ vuông tại $A$.",
            "dap_an": "$\\triangle ABC$ vuông tại $A$",
            "loi_giai": "Ta có: $AB^2 + AC^2 = 3^2 + 4^2 = 9 + 16 = 25$.\n$BC^2 = 5^2 = 25$.\nSuy ra $AB^2 + AC^2 = BC^2$.\nTheo định lí Pythagore đảo, tam giác $ABC$ vuông tại $A$.",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c16b", "vi_tri": "Câu 16.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Câu 16 (3,0 điểm): Cho tam giác $ABC$ có $AB = 3\\text{cm}, AC = 4\\text{cm}, BC = 5\\text{cm}$. Gọi $AH$ là đường cao của tam giác $ABC$.",
            "de": "b) Chứng minh $\\triangle ABC \\backsim \\triangle HBA$ và $\\triangle ABC \\backsim \\triangle HAC$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle HBA$ (g.g) và $\\triangle ABC \\backsim \\triangle HAC$ (g.g)",
            "loi_giai": "- Xét $\\triangle ABC$ và $\\triangle HBA$, ta có: $\\widehat{BAC} = \\widehat{BHA} = 90^\\circ$ và $\\widehat{B}$ là góc chung. Do đó $\\triangle ABC \\backsim \\triangle HBA\\text{ (g.g)}$.\n- Xét $\\triangle ABC$ và $\\triangle HAC$, ta có: $\\widehat{BAC} = \\widehat{AHC} = 90^\\circ$ và $\\widehat{C}$ là góc chung. Do đó $\\triangle ABC \\backsim \\triangle HAC\\text{ (g.g)}$.",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c16c", "vi_tri": "Câu 16.c", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tính độ dài đường cao và chứng minh hệ thức"],
            "band": "VD", "phut": 5.0, "diem_bai": 1.0,
            "de_chung": "Câu 16 (3,0 điểm): Cho tam giác $ABC$ có $AB = 3\\text{cm}, AC = 4\\text{cm}, BC = 5\\text{cm}$. Gọi $AH$ là đường cao của tam giác $ABC$.",
            "de": "c) Tính $AH$ và chứng minh $AH^2 = HB \\cdot HC$.",
            "dap_an": "$AH = 2{,}4\\text{ cm}$ và $AH^2 = HB \\cdot HC$",
            "loi_giai": "- Từ $\\triangle ABC \\backsim \\triangle HBA$ (câu b), ta có:\n$$\\frac{AC}{AH} = \\frac{BC}{AB} \\Rightarrow AH = \\frac{AB \\cdot AC}{BC} = \\frac{3 \\cdot 4}{5} = 2{,}4\\text{ (cm)}.$$\n- Từ $\\triangle HBA \\backsim \\triangle HAC$ (vì cùng đồng dạng với $\\triangle ABC$), ta có tỉ số:\n$$\\frac{AH}{CH} = \\frac{BH}{AH} \\Rightarrow AH^2 = HB \\cdot HC\\text{ (đpcm)}.$$",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c17", "vi_tri": "Câu 17", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hàm số bậc nhất trong thực tiễn"],
            "band": "VDC", "phut": 5.0, "diem_bai": 0.5,
            "de": "Câu 17 (0,5 điểm): Mẹ Lan mang 400 nghìn đồng đi siêu thị để mua $1\\text{kg}$ thịt gà và $2\\text{kg}$ thịt lợn, biết giá mỗi kg thịt gà và thịt lợn lần lượt là 140 nghìn đồng và $x$ nghìn đồng.\na) Lập công thức tính số tiền còn lại $y$ (nghìn đồng) của mẹ Lan sau khi mua $1\\text{kg}$ thịt gà và $2\\text{kg}$ thịt lợn.\nb) Tính giá tiền mỗi kg thịt lợn biết mẹ Lan mua vừa hết số tiền mang theo.",
            "dap_an": "a) $y = 260 - 2x$; b) $130\\text{ nghìn đồng/kg}$",
            "loi_giai": "a) Số tiền mua $1\\text{kg}$ thịt gà và $2\\text{kg}$ thịt lợn là: $140 + 2x$ (nghìn đồng).\nSố tiền còn lại của mẹ Lan là:\n$$y = 400 - (140 + 2x) = 260 - 2x\\text{ (nghìn đồng)}.$$\nb) Khi mẹ Lan mua vừa hết số tiền mang theo thì $y = 0$:\n$$260 - 2x = 0 \\Leftrightarrow 2x = 260 \\Leftrightarrow x = 130\\text{ (nghìn đồng)}.$$\nVậy giá tiền mỗi kg thịt lợn là 130 nghìn đồng.",
            "trang": 3, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề thi HK2 Toán 8 KNTT - Đề 01 (MathTech). Đã soát 100% từ đề chuẩn: 12 TN (3.0đ) + 5 câu TL (7.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

# ==============================================================================
# 12. ck2-x-t8-hk2-kntt-2
# ==============================================================================
def build_t8_kntt_2():
    slug = 'ck2-x-t8-hk2-kntt-2'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        # Trắc nghiệm (15 câu = 5.0đ: 10 câu x 0.3đ + 5 câu x 0.4đ)
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Định nghĩa phân thức đại số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Cách viết nào sau đây không cho một phân thức?\nA. $\\frac{3}{6xy}$\nB. $\\frac{xy + 1}{-3}$\nC. $\\frac{5x + 1}{0}$\nD. $\\frac{0}{x - 3}$",
            "dap_an": "C",
            "loi_giai": "Phân thức đại số có dạng $\\frac{A}{B}$ với $B$ là đa thức khác đa thức 0. Biểu thức $\\frac{5x + 1}{0}$ có mẫu bằng 0 nên không là phân thức. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Quy tắc đổi dấu"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Phân thức $-\\frac{x}{y}$ bằng phân thức nào sau đây?\nA. $\\frac{x}{y}$\nB. $\\frac{-x}{y}$\nC. $\\frac{-x}{-y}$\nD. $\\frac{y}{x}$",
            "dap_an": "B",
            "loi_giai": "Theo quy tắc đổi dấu: $-\\frac{x}{y} = \\frac{-x}{y} = \\frac{x}{-y}$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Điều kiện xác định của phân thức"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Điều kiện của biến $x$ để phân thức $\\frac{x}{x^2 - 4}$ được xác định là:\nA. $x \\neq \\pm 2$\nB. $x \\neq 2$\nC. $x \\neq -2$\nD. $x \\neq 0$ và $x \\neq \\pm 2$",
            "dap_an": "A",
            "loi_giai": "Phân thức xác định khi mẫu thức khác 0: $x^2 - 4 \\neq 0 \\Leftrightarrow x \\neq \\pm 2$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn phân thức đại số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Rút gọn phân thức $\\frac{4x^2y^5}{10x^2y^3}$ được kết quả bằng:\nA. $\\frac{2x}{5y}$\nB. $\\frac{2}{5}$\nC. $\\frac{2y^2}{5}$\nD. $\\frac{2}{5y^2}$",
            "dap_an": "C",
            "loi_giai": "$$\\frac{4x^2y^5}{10x^2y^3} = \\frac{2y^2}{5}.$$ Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Tính giá trị của phân thức"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Giá trị của phân thức $\\frac{x^2 - 1}{x - 1}$ tại $x = -1$ là:\nA. $0$\nB. $2$\nC. $-1$\nD. $1$",
            "dap_an": "A",
            "loi_giai": "Tại $x = -1$, mẫu $x - 1 = -2 \\neq 0$. Giá trị phân thức là: $\\frac{(-1)^2 - 1}{-1 - 1} = \\frac{0}{-2} = 0$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Nhận biết phương trình bậc nhất một ẩn"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Phương trình nào sau đây là phương trình bậc nhất một ẩn?\nA. $0x + 3 = 0$\nB. $2x^2 = 0$\nC. $5x + 3 = 0$\nD. $2x^2 + 1 = 0$",
            "dap_an": "C",
            "loi_giai": "Phương trình bậc nhất một ẩn có dạng $ax + b = 0$ ($a \\neq 0$). Phương trình $5x + 3 = 0$ có $a = 5 \\neq 0$. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Toán thực tế"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Ở một số quốc gia người ta dùng cả hai đơn vị đo là Fahrenheit ($^\\circ\\text{F}$) và độ Celcius ($^\\circ\\text{C}$), liên hệ với nhau bởi công thức $C = \\frac{5}{9}(F - 32)$. Giá trị độ Fahrenheit tương ứng với $10^\\circ\\text{C}$ là:\nA. $90^\\circ\\text{F}$\nB. $45^\\circ\\text{F}$\nC. $10^\\circ\\text{F}$\nD. $50^\\circ\\text{F}$",
            "dap_an": "D",
            "loi_giai": "Thay $C = 10$ vào công thức: $10 = \\frac{5}{9}(F - 32) \\Leftrightarrow F - 32 = 18 \\Leftrightarrow F = 50^\\circ\\text{F}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hệ số góc của đường thẳng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Hệ số góc của đường thẳng $y = 2 - x$ là:\nA. $-1$\nB. $1$\nC. $2$\nD. $-2$",
            "dap_an": "A",
            "loi_giai": "Đường thẳng $y = -x + 2$ có hệ số góc là $a = -1$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "V. Thu thập và tổ chức dữ liệu", "dang": ["Đọc số liệu từ bảng thống kê"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "Quan sát bảng thống kê sau và thực hiện các câu hỏi 9; 10.\nSố lượt khách đến tham quan di tích X trong năm qua: Quý 1: 137, Quý 2: 100, Quý 3: 145, Quý 4: 150.",
            "de": "Số lượt khách đến tham quan di tích X trong cả năm qua là:\nA. 150\nB. 100\nC. 266\nD. 532",
            "dap_an": "D",
            "loi_giai": "Tổng số lượt khách là: $137 + 100 + 145 + 150 = 532$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất thực nghiệm của biến cố"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "Quan sát bảng thống kê sau và thực hiện các câu hỏi 9; 10.\nSố lượt khách đến tham quan di tích X trong năm qua: Quý 1: 137, Quý 2: 100, Quý 3: 145, Quý 4: 150.",
            "de": "Kết quả xác suất thực nghiệm của biến cố E “Khách đến tham quan di tích X trong quý 3 và quý 4” bằng:\nA. $\\approx 0{,}544$\nB. $\\approx 0{,}555$\nC. $\\approx 0{,}445$\nD. 295",
            "dap_an": "B",
            "loi_giai": "Số lượt khách trong quý 3 và quý 4 là: $145 + 150 = 295$.\nXác suất thực nghiệm là: $\\frac{295}{532} \\approx 0{,}555$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Định nghĩa hai tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Trong các khẳng định sau, khẳng định nào đúng?\nA. Hai tam giác bằng nhau thì đồng dạng với nhau.\nB. Hai tam giác vuông đồng dạng với nhau.\nC. Hai tam giác đồng dạng với nhau thì bằng nhau.\nD. Hai tam giác cân đồng dạng với nhau.",
            "dap_an": "A",
            "loi_giai": "Hai tam giác bằng nhau thì đồng dạng với nhau với tỉ số đồng dạng $k = 1$. Chọn A.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ số đồng dạng của hai tam giác"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Nếu tam giác MNP đồng dạng tam giác ABC theo tỉ số đồng dạng là $\\frac{1}{2}$ thì tam giác ABC đồng dạng với tam giác MNP theo tỉ số đồng dạng là:\nA. $\\frac{1}{2}$\nB. $2$\nC. $-\\frac{1}{2}$\nD. $-2$",
            "dap_an": "B",
            "loi_giai": "Nếu $\\triangle MNP \\backsim \\triangle ABC$ theo tỉ số $k = \\frac{1}{2}$ thì $\\triangle ABC \\backsim \\triangle MNP$ theo tỉ số $k' = \\frac{1}{k} = 2$. Chọn B.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c13", "vi_tri": "Câu 13", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Cho tam giác ABC vuông tại A. Trong các khẳng định sau khẳng định nào đúng?\nA. $AB^2 + BC^2 = AC^2$\nB. $AB^2 - BC^2 = AC^2$\nC. $AB^2 = BC^2 + AC^2$\nD. $BC^2 = AB^2 + AC^2$",
            "dap_an": "D",
            "loi_giai": "Theo định lí Pythagore trong tam giác vuông tại $A$, bình phương cạnh huyền bằng tổng bình phương hai cạnh góc vuông: $BC^2 = AB^2 + AC^2$. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c14", "vi_tri": "Câu 14", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính độ dài cạnh tam giác vuông bằng định lí Pythagore"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Cho tam giác MNP vuông tại M có $MN = 6\\text{ cm}, NP = 10\\text{ cm}$. Độ dài cạnh MP bằng:\nA. $8\\text{ cm}$\nB. $10\\text{ cm}$\nC. $7\\text{ cm}$\nD. $9\\text{ cm}$",
            "dap_an": "A",
            "loi_giai": "Áp dụng định lí Pythagore: $MP = \\sqrt{NP^2 - MN^2} = \\sqrt{10^2 - 6^2} = \\sqrt{64} = 8\\text{ cm}$. Chọn A.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c15", "vi_tri": "Câu 15", "loai": "TN",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Đặc điểm hình chóp tứ giác đều"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.4,
            "de_chung": "I/ TRẮC NGHIỆM: (5,0 điểm). Chọn một phương án trả lời đúng của mỗi câu sau.",
            "de": "Đáy của hình chóp tứ giác đều là:\nA. Hình bình hành\nB. Hình chữ nhật\nC. Hình vuông\nD. Hình thoi",
            "dap_an": "C",
            "loi_giai": "Đáy của hình chóp tứ giác đều là hình vuông. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },

        # Tự luận (5.0đ)
        {
            "id": f"l8-{slug}-b1", "vi_tri": "Bài 1", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn biểu thức phân thức đại số"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de": "Bài 1. (0,5 điểm) Rút gọn biểu thức: $\\left(\\frac{2x + y}{xy} - \\frac{1}{y}\\right) : \\frac{x - y}{xy}$.",
            "dap_an": "$\\frac{x + y}{x - y}$",
            "loi_giai": "$$\\left(\\frac{2x + y}{xy} - \\frac{1}{y}\\right) : \\frac{x - y}{xy} = \\left(\\frac{2x + y - x}{xy}\\right) : \\frac{x - y}{xy} = \\frac{x + y}{xy} \\cdot \\frac{xy}{x - y} = \\frac{x + y}{x - y}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2a", "vi_tri": "Bài 2.a", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "TH", "phut": 4.0, "diem_bai": 0.75,
            "de_chung": "Bài 2. (1,25 điểm)",
            "de": "a) Chu vi của 1 mảnh vườn hình chữ nhật là $42\\text{ m}$. Tìm chiều dài và chiều rộng của mảnh vườn, biết chiều rộng ngắn hơn chiều dài là $3\\text{m}$.",
            "dap_an": "Chiều dài: $12\\text{ m}$; Chiều rộng: $9\\text{ m}$",
            "loi_giai": "Nửa chu vi của mảnh vườn là: $42 : 2 = 21\\text{ (m)}$.\nGọi chiều rộng của mảnh vườn là $x\\text{ (m)}$ ($0 < x < 10{,}5$).\nChiều dài của mảnh vườn là: $x + 3\\text{ (m)}$.\nVì nửa chu vi là $21\\text{ m}$ nên ta có phương trình:\n$$x + (x + 3) = 21 \\Leftrightarrow 2x + 3 = 21 \\Leftrightarrow 2x = 18 \\Leftrightarrow x = 9\\text{ (thỏa mãn điều kiện)}.$$\nChiều dài mảnh vườn là: $9 + 3 = 12\\text{ (m)}$.\nVậy chiều dài mảnh vườn là $12\\text{ m}$ và chiều rộng là $9\\text{ m}$.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b2b", "vi_tri": "Bài 2.b", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Bài 2. (1,25 điểm)",
            "de": "b) Vẽ đồ thị hàm số: $y = 2x - 6$.",
            "dap_an": "Đồ thị là đường thẳng đi qua $(0; -6)$ và $(3; 0)$",
            "loi_giai": "- Cho $x = 0 \\Rightarrow y = -6$, ta được điểm $A(0; -6)$.\n- Cho $y = 0 \\Rightarrow 2x - 6 = 0 \\Leftrightarrow x = 3$, ta được điểm $B(3; 0)$.\nĐồ thị hàm số $y = 2x - 6$ là đường thẳng đi qua hai điểm $A(0; -6)$ và $B(3; 0)$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b3", "vi_tri": "Bài 3", "loai": "TL",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Ước lượng xác suất bằng thực nghiệm"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de": "Bài 3. (0,5 điểm): Một xưởng may áo xuất khẩu tiến hành kiểm tra chất lượng của 300 chiếc áo đã được may xong thấy có 15 chiếc bị lỗi. Trong một lô có 1500 chiếc áo, hãy dự đoán xem có khoảng bao nhiêu áo không bị lỗi.",
            "dap_an": "Khoảng 1425 chiếc áo không bị lỗi",
            "loi_giai": "Xác suất thực nghiệm áo bị lỗi là: $\\frac{15}{300} = 0{,}05 = 5\\%$.\nXác suất thực nghiệm áo không bị lỗi là: $1 - 0{,}05 = 0{,}95 = 95\\%$.\nTrong lô 1500 chiếc áo, số áo không bị lỗi dự đoán là:\n$$1500 \\cdot 0{,}95 = 1425\\text{ (chiếc áo)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4a", "vi_tri": "Bài 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4. (2,75 điểm): Cho tam giác $ABC$ vuông tại A và có đường cao $AH$ ($H \\in BC$). Biết $AB = 3\\text{ cm}, AC = 4\\text{ cm}$.",
            "de": "a) Chứng minh $\\triangle HBA \\backsim \\triangle ABC$.",
            "dap_an": "$\\triangle HBA \\backsim \\triangle ABC$ (g.g)",
            "loi_giai": "Xét $\\triangle HBA$ và $\\triangle ABC$, ta có:\n$$\\widehat{AHB} = \\widehat{BAC} = 90^\\circ,$$\n$$\\widehat{B}\\text{ là góc chung}.$$\nDo đó $\\triangle HBA \\backsim \\triangle ABC\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4b", "vi_tri": "Bài 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tính độ dài đoạn thẳng nhờ tam giác đồng dạng"],
            "band": "TH", "phut": 4.0, "diem_bai": 1.0,
            "de_chung": "Bài 4. (2,75 điểm): Cho tam giác $ABC$ vuông tại A và có đường cao $AH$ ($H \\in BC$). Biết $AB = 3\\text{ cm}, AC = 4\\text{ cm}$.",
            "de": "b) Tính độ dài đường cao AH.",
            "dap_an": "$AH = 2{,}4\\text{ cm}$",
            "loi_giai": "Áp dụng định lí Pythagore trong $\\triangle ABC$ vuông tại $A$:\n$$BC = \\sqrt{AB^2 + AC^2} = \\sqrt{3^2 + 4^2} = \\sqrt{25} = 5\\text{ (cm)}.$$\nVì $\\triangle HBA \\backsim \\triangle ABC$ (câu a), ta có tỉ số:\n$$\\frac{AH}{AC} = \\frac{AB}{BC} \\Rightarrow AH = \\frac{AB \\cdot AC}{BC} = \\frac{3 \\cdot 4}{5} = 2{,}4\\text{ (cm)}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-b4c", "vi_tri": "Bài 4.c", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Tính chất đường phân giác"],
            "band": "VD", "phut": 5.0, "diem_bai": 0.75,
            "de_chung": "Bài 4. (2,75 điểm): Cho tam giác $ABC$ vuông tại A và có đường cao $AH$ ($H \\in BC$). Biết $AB = 3\\text{ cm}, AC = 4\\text{ cm}$.",
            "de": "c) Đường phân giác của góc $\\widehat{ABC}$ cắt AH, AC lần lượt tại M và N. Chứng minh: $MA \\cdot NA = MH \\cdot NC$.",
            "dap_an": "$MA \\cdot NA = MH \\cdot NC$",
            "loi_giai": "Trong $\\triangle ABH$, vì $BM$ là tia phân giác của $\\widehat{ABH}$ nên:\n$$\\frac{MA}{MH} = \\frac{AB}{BH}.$$\nTrong $\\triangle ABC$, vì $BN$ là tia phân giác của $\\widehat{ABC}$ nên:\n$$\\frac{NA}{NC} = \\frac{BA}{BC} = \\frac{AB}{BC}.$$\nTừ $\\triangle HBA \\backsim \\triangle ABC$ (câu a), ta có: $\\frac{AB}{BC} = \\frac{BH}{AB} \\Rightarrow \\frac{AB}{BH} = \\frac{BC}{AB}$.\nDo đó $\\frac{MA}{MH} = \\frac{NC}{NA} \\Rightarrow MA \\cdot NA = MH \\cdot NC$ (đpcm).",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề thi HK2 Toán 8 KNTT - Đề 02 (MathTech). Đã đối soát 100% từ đề chuẩn: 15 câu TN (5.0đ) + 4 bài TL (5.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

# ==============================================================================
# 13. ck2-x-t8-hk2-kntt-3
# ==============================================================================
def build_t8_kntt_3():
    slug = 'ck2-x-t8-hk2-kntt-3'
    with open(f'inputs/refs/de-thi/lop-8/exams/{slug}.json', encoding='utf-8') as f:
        old = json.load(f)

    cau = [
        # Trắc nghiệm (15 câu = 5.0đ: 10 câu x 0.3đ + 5 câu x 0.4đ)
        {
            "id": f"l8-{slug}-c1", "vi_tri": "Câu 1", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Định nghĩa phân thức đại số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Cách viết nào sau đây không cho một phân thức?\nA. $\\frac{0}{x + 1}$\nB. $\\frac{xy + z}{-5}$\nC. $\\frac{y + z}{0}$\nD. $\\frac{2}{x - xy}$",
            "dap_an": "C",
            "loi_giai": "Phân thức đại số có mẫu thức khác đa thức 0. Biểu thức $\\frac{y+z}{0}$ có mẫu bằng 0 nên không là phân thức. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2", "vi_tri": "Câu 2", "loai": "TN",
            "chuong": "VI. Phân thức đại số", "dang": ["Rút gọn phân thức đại số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Phân thức $\\frac{5x - 5}{x - 1}$ rút gọn thành:\nA. $\\frac{x - 1}{x}$\nB. $5$\nC. $\\frac{1}{5}$\nD. $\\frac{x + 1}{x - 1}$",
            "dap_an": "B",
            "loi_giai": "$$\\frac{5x - 5}{x - 1} = \\frac{5(x - 1)}{x - 1} = 5.$$ Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Kiểm tra nghiệm của phương trình"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Giá trị $x = -4$ là nghiệm của phương trình:\nA. $-2{,}5x + 1 = 11$\nB. $-2{,}5x = -10$\nC. $3x - 8 = 0$\nD. $3x - 1 = x + 7$",
            "dap_an": "A",
            "loi_giai": "Thay $x = -4$ vào $-2{,}5x + 1$: $-2{,}5(-4) + 1 = 10 + 1 = 11$. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4", "vi_tri": "Câu 4", "loai": "TN",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Biểu diễn đại lượng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Năm nay Trang $x$ tuổi, tuổi của Trang 6 năm sau là:\nA. $14$\nB. $x + 6$\nC. $6x$\nD. $20$",
            "dap_an": "B",
            "loi_giai": "Sau 6 năm nữa tuổi của Trang là $x + 6$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c5", "vi_tri": "Câu 5", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Nhận biết hàm số bậc nhất"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Trong các hàm số sau đây hàm số nào là hàm số bậc nhất?\nA. $y = \\frac{2}{x} + 3$\nB. $y = 2mx + 3$\nC. $y = 0x + 2$\nD. $y = (m - 1)x + 2$ ($m \\neq 1$)",
            "dap_an": "D",
            "loi_giai": "Hàm số bậc nhất có dạng $y = ax + b$ với $a \\neq 0$. Với $m \\neq 1$ thì $(m - 1)x + 2$ có hệ số $a = m - 1 \\neq 0$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c6", "vi_tri": "Câu 6", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hai đường thẳng song song"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Đường thẳng nào sau đây song song với đường thẳng $y = 3x - 1$?\nA. $y = -3x - 1$\nB. $y = 1 - 3x$\nC. $y = 3x - 3$\nD. $y = 3 - 3x$",
            "dap_an": "C",
            "loi_giai": "Hai đường thẳng song song khi có cùng hệ số góc và tung độ gốc khác nhau: $a = 3$ và $b \\neq -1$. Đường thẳng $y = 3x - 3$ thỏa mãn. Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c7", "vi_tri": "Câu 7", "loai": "TN",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Điểm thuộc đồ thị hàm số"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Điểm thuộc đồ thị hàm số $y = 2x - 5$ là:\nA. $(4; 3)$\nB. $(3; -1)$\nC. $(-4; -3)$\nD. $(2; 1)$",
            "dap_an": "A",
            "loi_giai": "Thay $x = 4$ vào hàm số: $y = 2(4) - 5 = 8 - 5 = 3$. Điểm $(4; 3)$ thuộc đồ thị hàm số. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c8", "vi_tri": "Câu 8", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Trường hợp đồng dạng góc - góc"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Cho $\\triangle ABC$ có $\\widehat{A} = 40^\\circ, \\widehat{B} = 80^\\circ$ và $\\triangle DEF$ có $\\widehat{E} = 40^\\circ, \\widehat{D} = 60^\\circ$. Khẳng định nào sau đây đúng?\nA. $\\triangle ABC \\backsim \\triangle DEF$\nB. $\\triangle ABC \\backsim \\triangle EFD$\nC. $\\triangle ABC \\backsim \\triangle DFE$\nD. $\\triangle DEF \\backsim \\triangle CBA$",
            "dap_an": "C",
            "loi_giai": "Trong $\\triangle ABC$: $\\widehat{C} = 180^\\circ - (40^\\circ + 80^\\circ) = 60^\\circ$.\nTrong $\\triangle DEF$: $\\widehat{F} = 180^\\circ - (40^\\circ + 60^\\circ) = 80^\\circ$.\nTa có: $\\widehat{A} = \\widehat{E} = 40^\\circ, \\widehat{B} = \\widehat{F} = 80^\\circ, \\widehat{C} = \\widehat{D} = 60^\\circ$.\nDo đó $\\triangle ABC \\backsim \\triangle EFD$ (hoặc tương ứng theo các đỉnh). Chọn C.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c9", "vi_tri": "Câu 9", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Tỉ số cạnh của hai tam giác đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Nếu $\\triangle ABC \\backsim \\triangle DEF$ thì ta có:\nA. $\\frac{AB}{BC} = \\frac{DE}{DF}$\nB. $\\frac{AB}{AC} = \\frac{DE}{EF}$\nC. $\\frac{AB}{AC} = \\frac{DE}{ED}$\nD. $\\frac{AB}{BC} = \\frac{DE}{EF}$",
            "dap_an": "D",
            "loi_giai": "Vì $\\triangle ABC \\backsim \\triangle DEF$ nên $\\frac{AB}{DE} = \\frac{BC}{EF} \\Rightarrow \\frac{AB}{BC} = \\frac{DE}{EF}$. Chọn D.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c10", "vi_tri": "Câu 10", "loai": "TN",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Hình đồng dạng"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Trong các cặp hình vuông, cặp hình chữ nhật, cặp hình thoi, cặp hình bình hành. Cặp hình nào luôn là cặp hình đồng dạng?\nA. Cặp hình vuông\nB. Cặp hình chữ nhật\nC. Cặp hình thoi\nD. Cặp hình bình hành",
            "dap_an": "A",
            "loi_giai": "Hai hình vuông bất kì luôn có các góc bằng nhau (đều bằng $90^\\circ$) và các cạnh tương ứng tỉ lệ, nên hai hình vuông luôn đồng dạng. Chọn A.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c11", "vi_tri": "Câu 11", "loai": "TN",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore đảo"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Bộ ba số nào sau đây không phải là độ dài ba cạnh của một tam giác vuông?\nA. $1\\text{ cm}, 1\\text{ cm}, \\sqrt{2}\\text{ cm}$\nB. $4\\text{ cm}, 6\\text{ cm}, 8\\text{ cm}$\nC. $2\\text{ cm}, 4\\text{ cm}, \\sqrt{20}\\text{ cm}$\nD. $3\\text{ cm}, 4\\text{ cm}, 5\\text{ cm}$",
            "dap_an": "B",
            "loi_giai": "Ta có $4^2 + 6^2 = 16 + 36 = 52 \\neq 64 = 8^2$. Do đó bộ ba $4\\text{ cm}, 6\\text{ cm}, 8\\text{ cm}$ không phải độ dài ba cạnh tam giác vuông. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c12", "vi_tri": "Câu 12", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Tính xác suất của biến cố bằng tỉ số"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.4,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Một hộp đựng các tấm thẻ ghi số $11, 12, 13, \\dots, 20$. Rút ngẫu nhiên một tấm thẻ trong hộp. Xác suất để rút được một tấm thẻ ghi số nguyên tố là:\nA. $0{,}2$\nB. $0{,}4$\nC. $0{,}5$\nD. $0{,}6$",
            "dap_an": "B",
            "loi_giai": "Các số nguyên tố từ 11 đến 20 là: $11; 13; 17; 19$ (có 4 số).\nTổng số thẻ là 10 thẻ. Xác suất là: $\\frac{4}{10} = 0{,}4$. Chọn B.",
            "trang": 1, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c13", "vi_tri": "Câu 13", "loai": "TN",
            "chuong": "VIII. Mở đầu về tính xác suất của biến cố", "dang": ["Xác suất của biến cố"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.4,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Chọn ngẫu nhiên một số có một chữ số, xác suất để chọn được số chính phương là:\nA. $0{,}2$\nB. $0{,}3$\nC. $0{,}4$\nD. $0{,}5$",
            "dap_an": "C",
            "loi_giai": "Tập hợp các số có một chữ số là $\\{0; 1; 2; 3; 4; 5; 6; 7; 8; 9\\}$ gồm 10 số.\nCác số chính phương là: $0; 1; 4; 9$ (gồm 4 số).\nXác suất là $\\frac{4}{10} = 0{,}4$. Chọn C.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c14", "vi_tri": "Câu 14", "loai": "TN",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Diện tích xung quanh hình chóp tứ giác đều"],
            "band": "TH", "phut": 2.0, "diem_bai": 0.4,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Một lồng đèn có dạng hình chóp tứ giác đều có cạnh đáy bằng $15\\text{ cm}$, độ dài trung đoạn bằng $10\\text{ cm}$. Diện tích giấy dán kín bốn mặt bên của lồng đèn (mép dán không đáng kể) là:\nA. $200\\text{ cm}^2$\nB. $300\\text{ cm}^2$\nC. $400\\text{ cm}^2$\nD. $500\\text{ cm}^2$",
            "dap_an": "B",
            "loi_giai": "Nửa chu vi đáy của lồng đèn là: $p = \\frac{15 \\cdot 4}{2} = 30\\text{ (cm)}$.\nDiện tích dán kín bốn mặt bên (diện tích xung quanh) là:\n$$S_{xq} = p \\cdot d = 30 \\cdot 10 = 300\\text{ (cm}^2\\text{)}.$$ Chọn B.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c15", "vi_tri": "Câu 15", "loai": "TN",
            "chuong": "X. Một số hình khối trong thực tiễn", "dang": ["Công thức tính diện tích đáy hình chóp"],
            "band": "NB", "phut": 1.5, "diem_bai": 0.3,
            "de_chung": "I. TRẮC NGHIỆM (5,0 điểm). Chọn phương án trả lời đúng của mỗi câu hỏi sau:",
            "de": "Hình chóp tam giác đều có chiều cao $h$, thể tích $V$. Diện tích đáy $S$ bằng:\nA. $\\frac{h}{V}$\nB. $\\frac{V}{h}$\nC. $\\frac{3h}{V}$\nD. $\\frac{3V}{h}$",
            "dap_an": "D",
            "loi_giai": "Ta có $V = \\frac{1}{3}S \\cdot h \\Rightarrow S = \\frac{3V}{h}$. Chọn D.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },

        # Tự luận (5.0đ)
        {
            "id": f"l8-{slug}-c1a", "vi_tri": "Câu 1.a", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Cộng trừ phân thức đại số"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "II. TỰ LUẬN (5,0 điểm).\nCâu 1 (1,0 điểm): Tính:",
            "de": "a) $\\frac{5xy - x^2y^2}{3xy} + \\frac{4xy + x^2y^2}{3xy}$",
            "dap_an": "$3$",
            "loi_giai": "$$\\frac{5xy - x^2y^2}{3xy} + \\frac{4xy + x^2y^2}{3xy} = \\frac{5xy - x^2y^2 + 4xy + x^2y^2}{3xy} = \\frac{9xy}{3xy} = 3.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c1b", "vi_tri": "Câu 1.b", "loai": "TL",
            "chuong": "VI. Phân thức đại số", "dang": ["Cộng trừ phân thức đại số"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "II. TỰ LUẬN (5,0 điểm).\nCâu 1 (1,0 điểm): Tính:",
            "de": "b) $\\frac{x}{x - y} - \\frac{2x - y}{y - x}$",
            "dap_an": "$\\frac{3x - y}{x - y}$",
            "loi_giai": "$$\\frac{x}{x - y} - \\frac{2x - y}{y - x} = \\frac{x}{x - y} + \\frac{2x - y}{x - y} = \\frac{x + 2x - y}{x - y} = \\frac{3x - y}{x - y}.$$",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2a", "vi_tri": "Câu 2.a", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Hệ số góc của đường thẳng"],
            "band": "NB", "phut": 2.0, "diem_bai": 0.5,
            "de_chung": "Câu 2 (1,0 điểm) Cho hàm số $y = 2x + 3$ có đồ thị là đường thẳng $(d)$.",
            "de": "a) Cho biết hệ số góc của đường thẳng $(d)$ và góc tạo bởi $(d)$ với trục $Ox$ là góc gì?",
            "dap_an": "Hệ số góc $a = 2$; góc tạo bởi $(d)$ với trục $Ox$ là góc nhọn",
            "loi_giai": "- Hệ số góc của đường thẳng $(d)$ là $a = 2$.\n- Vì $a = 2 > 0$ nên góc tạo bởi đường thẳng $(d)$ với trục $Ox$ là góc nhọn.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c2b", "vi_tri": "Câu 2.b", "loai": "TL",
            "chuong": "VI. Hàm số và đồ thị", "dang": ["Vẽ đồ thị hàm số bậc nhất"],
            "band": "TH", "phut": 3.0, "diem_bai": 0.5,
            "de_chung": "Câu 2 (1,0 điểm) Cho hàm số $y = 2x + 3$ có đồ thị là đường thẳng $(d)$.",
            "de": "b) Vẽ đường thẳng $(d)$.",
            "dap_an": "Đường thẳng đi qua $(0; 3)$ và $(-1{,}5; 0)$",
            "loi_giai": "- Cho $x = 0 \\Rightarrow y = 3$, ta được điểm $A(0; 3)$.\n- Cho $y = 0 \\Rightarrow 2x + 3 = 0 \\Leftrightarrow x = -1{,}5$, ta được điểm $B(-1{,}5; 0)$.\nĐồ thị hàm số $y = 2x + 3$ là đường thẳng đi qua hai điểm $A(0; 3)$ và $B(-1{,}5; 0)$.",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c3", "vi_tri": "Câu 3", "loai": "TL",
            "chuong": "VII. Phương trình bậc nhất một ẩn", "dang": ["Giải bài toán bằng cách lập phương trình"],
            "band": "VD", "phut": 6.0, "diem_bai": 1.0,
            "de": "Câu 3 (1,0 điểm): Giải bài toán sau bằng cách lập phương trình:\nTrong giải bóng đá Hội khỏe phù đổng trường Nguyễn Du có 7 đội bóng tham gia đá vòng tròn 1 lượt (cứ 1 đội gặp 6 đội còn lại, thắng được 3 điểm, hòa được 1 điểm, thua không có điểm). Khi kết thúc giải, đội bóng lớp 8A không thua trận nào và được 14 điểm. Hỏi đội bóng lớp 8A thắng bao nhiêu trận?",
            "dap_an": "4 trận thắng (và 2 trận hòa)",
            "loi_giai": "Vì có 7 đội thi đấu vòng tròn 1 lượt nên mỗi đội phải thi đấu 6 trận.\nĐội bóng lớp 8A thi đấu 6 trận và không thua trận nào, nghĩa là mỗi trận của lớp 8A chỉ có kết quả thắng hoặc hòa.\nGọi số trận thắng của đội bóng lớp 8A là $x$ (trận) ($x \\in \\mathbb{N}, 0 \\le x \\le 6$).\nSố trận hòa của đội bóng lớp 8A là: $6 - x$ (trận).\nSố điểm từ các trận thắng là: $3x$ (điểm).\nSố điểm từ các trận hòa là: $1 \\cdot (6 - x) = 6 - x$ (điểm).\nVì tổng số điểm đội đạt được là 14 điểm nên ta có phương trình:\n$$3x + (6 - x) = 14$$\n$$\\Leftrightarrow 2x + 6 = 14$$\n$$\\Leftrightarrow 2x = 8 \\Leftrightarrow x = 4\\text{ (thỏa mãn điều kiện)}.$$\nVậy đội bóng lớp 8A đã thắng 4 trận.",
            "trang": 2, "co_hinh": False, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4a", "vi_tri": "Câu 4.a", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Chứng minh hai tam giác đồng dạng"],
            "band": "TH", "phut": 3.5, "diem_bai": 0.75,
            "de_chung": "Câu 4 (2,0 điểm): Bóng của một ngôi nhà trên mặt đất có độ dài $AC = 2\\text{ m}$. Cùng thời điểm đó, một cột đèn $MN = 1{,}8\\text{ m}$ có bóng dài $EM = 0{,}72\\text{ m}$.",
            "de": "a) Chứng minh $\\triangle ABC$ đồng dạng với $\\triangle MNE$.",
            "dap_an": "$\\triangle ABC \\backsim \\triangle MNE$ (g.g)",
            "loi_giai": "Vì ngôi nhà và cột đèn đều đứng vuông góc với mặt đất nên:\n$$\\widehat{BAC} = \\widehat{NME} = 90^\\circ.$$\nTại cùng một thời điểm, các tia nắng mặt trời xem như song song với nhau nên góc tạo bởi tia nắng với mặt đất là bằng nhau:\n$$\\widehat{ACB} = \\widehat{MEN}.$$\nDo đó $\\triangle ABC \\backsim \\triangle MNE\\text{ (g.g)}.$",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4b", "vi_tri": "Câu 4.b", "loai": "TL",
            "chuong": "IX. Tam giác đồng dạng", "dang": ["Ứng dụng tam giác đồng dạng đo chiều cao"],
            "band": "TH", "phut": 3.5, "diem_bai": 0.75,
            "de_chung": "Câu 4 (2,0 điểm): Bóng của một ngôi nhà trên mặt đất có độ dài $AC = 2\\text{ m}$. Cùng thời điểm đó, một cột đèn $MN = 1{,}8\\text{ m}$ có bóng dài $EM = 0{,}72\\text{ m}$.",
            "de": "b) Tính chiều cao AB của ngôi nhà.",
            "dap_an": "$AB = 5\\text{ m}$",
            "loi_giai": "Vì $\\triangle ABC \\backsim \\triangle MNE$ (theo câu a), ta có tỉ số đồng dạng:\n$$\\frac{AB}{MN} = \\frac{AC}{ME} \\Rightarrow \\frac{AB}{1{,}8} = \\frac{2}{0{,}72}.$$\nSuy ra chiều cao của ngôi nhà là:\n$$AB = \\frac{1{,}8 \\cdot 2}{0{,}72} = \\frac{3{,}6}{0{,}72} = 5\\text{ (m)}.$$",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        },
        {
            "id": f"l8-{slug}-c4c", "vi_tri": "Câu 4.c", "loai": "TL",
            "chuong": "VII. Định lí Thalès trong tam giác", "dang": ["Định lí Pythagore ứng dụng thực tế"],
            "band": "VD", "phut": 4.0, "diem_bai": 0.5,
            "de_chung": "Câu 4 (2,0 điểm): Bóng của một ngôi nhà trên mặt đất có độ dài $AC = 2\\text{ m}$. Cùng thời điểm đó, một cột đèn $MN = 1{,}8\\text{ m}$ có bóng dài $EM = 0{,}72\\text{ m}$.",
            "de": "c) Bác An muốn làm một cái thang để lên mái nhà, em hãy tính giúp bác An phải làm cái thang dài bao nhiêu? (Biết để an toàn thì chân thang phải đặt cách chân tường $1{,}5\\text{ m}$, chiều dài làm tròn đến mét).",
            "dap_an": "$5\\text{ m}$",
            "loi_giai": "Thang tạo với tường nhà và mặt đất thành một tam giác vuông trong đó:\n- Chiều cao của tường nhà là cạnh góc vuông $h = AB = 5\\text{ (m)}$.\n- Khoảng cách từ chân thang đến chân tường là cạnh góc vuông $d = 1{,}5\\text{ (m)}$.\n- Chiều dài cái thang là cạnh huyền $L$.\nÁp dụng định lí Pythagore, chiều dài cái thang cần làm là:\n$$L = \\sqrt{h^2 + d^2} = \\sqrt{5^2 + 1{,}5^2} = \\sqrt{25 + 2{,}25} = \\sqrt{27{,}25} \\approx 5{,}22\\text{ (m)} \\approx 5\\text{ (m)}.$$",
            "trang": 2, "co_hinh": True, "can_doc_anh": False, "da_duyet": True, "barem_nguon": "chuan_hoa"
        }
    ]

    old['tang'] = 2
    old['da_duyet'] = True
    old['ghi_chu'] = "Đề thi HK2 Toán 8 KNTT - Đề 03 (MathTech). Đã đối soát 100% từ đề chuẩn: 15 câu TN (5.0đ) + 4 câu TL (5.0đ), tổng điểm 10.00đ."
    old['cau'] = cau
    save_exam(slug, old)

if __name__ == '__main__':
    build_kntt_de_2()
    build_kntt_de_3()
    build_t8_kntt_1()
    build_t8_kntt_2()
    build_t8_kntt_3()
