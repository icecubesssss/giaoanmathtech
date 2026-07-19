# -*- coding: utf-8 -*-
"""Tiến độ tầng C — Lớp 9. Đại số 180′ · Hình học 90′.
v5 (2026-07-16): xếp lại theo MA TRẬN ĐỀ VÀO 10 HÀ NỘI (3 đề gốc: minh họa + 2025 + 2026).
 - Thầy chốt: Thống kê–Xác suất 3 buổi · Hình khối 3 buổi ("nó có mấy ý đi thi thôi")
 - Tỉ số lượng giác (Ch IV): 2 buổi, đủ GK1 trường, không quay lại
 - BĐT/BPT · đồ thị y=ax² · đa giác đều · vị trí 2 đường tròn: giảm mạnh, giữ tối thiểu
 - Giờ tiết kiệm dồn sang căn thức (Câu II) + đường tròn (Câu IV.2) + luyện đề
 - HẾT CHƯƠNG TRÌNH tuần 30 → 18 buổi luyện đề
"""
from datetime import date, timedelta

START = date(2026, 6, 21)
TET_OFF = {date(2027, 2, 7), date(2027, 2, 14)}

COLS = ["Tuần", "Tiến độ trung tâm", "Bài SGK (KNTT)", "Tiết SGK (PPCT)", "Mức dạy", "Deadline dạy",
        "Thời lượng (phút)", "Hạng mục", "Loại kiểm tra", "Ưu tiên", "Câu vào 10",
        "Nội dung đưa cho HS", "Ghi chú",
        "Trạng thái", "Deadline L0", "Deadline L2", "Deadline L3", "Deadline L4",
        "Người sản xuất", "ND chiếu màn hình"]
CORE_N = 13

CH1 = "CHƯƠNG I. PHƯƠNG TRÌNH VÀ HỆ HAI PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN"
CH2 = "CHƯƠNG II. PHƯƠNG TRÌNH VÀ BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN"
CH3 = "CHƯƠNG III. CĂN BẬC HAI VÀ CĂN BẬC BA"
CH4 = "CHƯƠNG IV. HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG"
CH5 = "CHƯƠNG V. ĐƯỜNG TRÒN"
CH6 = "CHƯƠNG VI. HÀM SỐ y = ax² (a ≠ 0). PHƯƠNG TRÌNH BẬC HAI MỘT ẨN"
CH7 = "CHƯƠNG VII. TẦN SỐ VÀ TẦN SỐ TƯƠNG ĐỐI"
CH8 = "CHƯƠNG VIII. XÁC SUẤT CỦA BIẾN CỐ"
CH9 = "CHƯƠNG IX. ĐƯỜNG TRÒN NGOẠI TIẾP VÀ ĐƯỜNG TRÒN NỘI TIẾP"
CH10 = "CHƯƠNG X. MỘT SỐ HÌNH KHỐI TRONG THỰC TIỄN"
HE = "ÔN TẬP HÈ – NỀN LỚP 8"
OGK1, OCK1, OGK2, OCK2 = ("ÔN TẬP GIỮA HỌC KÌ I", "ÔN TẬP HỌC KÌ I",
                          "ÔN TẬP GIỮA HỌC KÌ II", "ÔN TẬP CUỐI KÌ II")
LD = "LUYỆN ĐỀ – ÔN THI VÀO 10"

# --- TÀI LIỆU LUYỆN DẠNG (Thầy chốt 2026-07-17: xong kiến thức câu nào thì luyện ngay
# dạng câu đó, KHÔNG dồn xuống pha sau Tết). Thầy chốt KHÔNG dùng kho đề cũ trong repo
# (chương trình cũ, lệch cấu trúc) — lấy đề thi thử 2025–2026 trên mạng, fetch bổ sung sau. ---
KHO_CU = "TÀI LIỆU: câu tương ứng cắt từ đề thi thử vào 10 Hà Nội 2025–2026 (sưu tầm — chưa có trong repo)."
KHO_MOI = ("TÀI LIỆU MỎNG: chương trình cũ không dạy phần này nên đề cũ không có. "
           "Nguồn hiện chỉ 3 đề mới (minh họa + 2025 + 2026) + đề thi thử 2025–2026 sưu tầm.")

A = "A – Trọng tâm vào 10"
B = "B – Nền, cần cho thi trường"
C = "C – Tối thiểu"

# ĐIỂM LẤY TỪ THANG ĐIỂM CHÍNH THỨC CỦA SỞ GD&ĐT HÀ NỘI (đề 2025 — file
# `dap-an-thang-diem-CHINH-THUC-so-gddt-ha-noi-2025.pdf` trong inputs/seeds/lop-9/de-thi-vao-10/).
# TRƯỚC ĐÂY LÀ SỐ AI TỰ ĐOÁN và sai gần hết — Thầy bắt sửa 2026-07-17.
Q_I1 = "Câu I.1 (1,0đ)"        # tần số + tần số tương đối ghép nhóm — ý NB ĐẮT NHẤT đề
Q_I2 = "Câu I.2 (0,5đ)"        # xác suất biến cố
Q_II = "Câu II (1,5đ)"
Q_II1 = "Câu II.1 (0,25đ)"     # tính giá trị biểu thức — ý RẺ NHẤT đề
Q_II2 = "Câu II.2 (0,75đ)"     # chứng minh rút gọn
Q_II3 = "Câu II.3 (0,5đ)"      # câu phụ sau rút gọn — 3/3 đề đều cần BĐT/BPT
Q_III1 = "Câu III.1 (1,0đ)"    # giải bài toán bằng cách lập PT
Q_III2 = "Câu III.2 (1,0đ)"    # giải bài toán bằng cách lập hệ PT
Q_III3 = "Câu III.3 (0,5đ)"    # Viète
Q_IV1 = "Câu IV.1 (1,0đ)"      # hình khối: 1a Sxq 0,5 + 1b thể tích 0,5
Q_IV2 = "Câu IV.2 (3,0đ)"      # 2a 1,0 + 2b 1,5 + 2c 0,5
Q_IV2a = "Câu IV.2a (1,0đ)"    # chứng minh 4 điểm cùng thuộc một đường tròn
Q_IV2b = "Câu IV.2b (1,5đ)"    # Ý ĐẮT NHẤT ĐỀ. Thang điểm Sở KHÔNG tách 2 vế
Q_V = "Câu V (0,5đ – VDC)"
Q_NO = "— không có trong đề"


def t15(what, n):
    return (f"KT 15′ – {what}", "", "", 15, "Test", "15 phút", "", "", f"Đề 15′ số {n}", "")


def kt45(ch):
    return [(f"Kiểm tra 1 tiết – Chương {ch}", "", "", 45, "Test", "1 tiết", "", "", f"Đề 1 tiết – Chương {ch}", ""),
            (f"Chữa đề kiểm tra 1 tiết – Chương {ch}", "", "", 45, "KT", "", "", "", "", "")]


# (tiến độ, bài SGK, số tiết, phút, hạng mục, loại KT, ưu tiên, câu vào 10, nội dung HS, ghi chú)
DAI_SO = {
 1: [("Ôn tập nền Lớp 8 (1): Đa thức nhiều biến · Hằng đẳng thức · Phân tích đa thức thành nhân tử", "Ôn tập đầu năm", "", 135, "KT", "", B, "", HE, "Nền tính toán cho căn thức + PT bậc hai"),
     ("PP Hồi tưởng chủ động", "", "", 30, "NT-PP", "", "", "", "", "")],
 2: [("Ôn tập nền Lớp 8 (2): Phân thức đại số · Phương trình bậc nhất một ẩn", "Ôn tập đầu năm", "", 135, "KT", "", B, "", HE, ""),
     ("PP Lặp lại ngắt quãng", "", "", 30, "NT-PP", "", "", "", "", "")],
 3: [("Ôn tập nền Lớp 8 (3): Hàm số bậc nhất và đồ thị", "Ôn tập đầu năm", "", 90, "KT", "", C, "", HE, ""),
     ("Khảo sát chất lượng đầu vào", "", "", 60, "Test", "Khảo sát", "", "", "Đề khảo sát đầu vào", "Rà lại phân tầng HS"),
     ("Học toán để làm gì – Phần 1", "", "", 15, "ĐL-CH", "", "", "", "", "")],
 # ===== Chương I (12 tiết) — 3 buổi · Thầy chốt: buổi 3 tiếng dạy hết cả 2 PP giải hệ =====
 4: [("Bài 1. Khái niệm PT & hệ hai PT bậc nhất hai ẩn + Bài 2. Giải hệ – PP thế và PP cộng đại số", "Bài 1 + Bài 2", 6, 165, "KT", "", B, "", CH1, "Thầy chốt: 1 buổi 3 tiếng dạy hết cả PP thế lẫn PP cộng đại số. File cũ (90′/buổi) dùng 240′ cho cả Bài 1+2", "Chỉ ý vào đề")],
 5: [t15("Bài 2: Giải hệ bằng PP thế và PP cộng đại số", 1),
     ("Luyện tập chung Chương I + Bài 3. Giải bài toán bằng cách lập hệ phương trình", "Luyện tập chung + Bài 3", 4, 150, "KT", "", A, Q_III2, CH1, "Thầy chốt: tuần kế tiếp là vào luôn giải toán bằng cách lập hệ")],
 6: [t15("Bài 3: Giải bài toán bằng cách lập hệ phương trình", 2),
     ("LUYỆN DẠNG Câu III.2 ngay sau khi xong Chương I – lập hệ (mua bán, lãi suất, năng suất) + BT cuối chương I", "Bài tập cuối chương I", 2, 120, "KT", "", A, Q_III2, CH1, "TRỌNG TÂM – 3/3 đề đều có. Thang điểm Sở 1,0đ, ngang lập PT. " + KHO_CU),
     ("PP Hack não năng suất", "", "", 30, "NT-PP", "", "", "", "", "")],
 # ===== Chương II (12 tiết) — 4 buổi · BĐT/BPT là NỀN của Câu II.3 (Thầy chỉ ra 2026-07-16) =====
 7: [("Bài 4. Phương trình quy về phương trình bậc nhất một ẩn (PT tích · PT chứa ẩn ở mẫu)", "Bài 4", 3, 165, "KT", "", B, "", CH2, "Vào 10 không hỏi trực tiếp, NHƯNG đề GK1 của trường hỏi 100% (10/10 đề)")],
 8: [t15("Bài 4: PT tích · PT chứa ẩn ở mẫu", 3),
     ("Bài 5. Bất đẳng thức và tính chất", "Bài 5", 2, 150, "KT", "", A, Q_II3, CH2, "NÂNG HẠNG – 3/3 đề Câu II ý 3 đều cần BĐT: minh họa 'chứng minh P < P²' · 2025 'tìm x lớn nhất để A/B < 1/2' · 2026 'tìm x để P nguyên' (chặn khoảng)")],
 9: [t15("Bài 5: Bất đẳng thức và tính chất", 4),
     ("Bài 6. Bất phương trình bậc nhất một ẩn", "Bài 6", 3, 150, "KT", "", A, Q_II3, CH2, "NÂNG HẠNG – nền để giải câu phụ dạng 'tìm x để P > k'. Đề GK1 trường cũng hỏi 90%")],
 10:[t15("Bài 6: Giải bất phương trình bậc nhất một ẩn", 5),
     ("Luyện tập chung + Bài tập cuối chương II", "Luyện tập chung + BT cuối chương II", 4, 120, "KT", "", B, "", CH2, ""),
     ("Khám phá Toán học – 1", "", "", 30, "DL", "", "", "", "", "")],
 # ===== Chương III (13 tiết) — 7 buổi · TRỌNG TÂM Câu II (1,5đ) =====
 11:[("Bài 7. Căn bậc hai và căn thức bậc hai", "Bài 7", 2, 165, "KT", "", A, Q_II, CH3, "Buổi mở chương – chưa có KT 15′")],
 12:[t15("Bài 7: Căn bậc hai và căn thức bậc hai", 6),
     ("Bài 8. Khai căn bậc hai với phép nhân và phép chia", "Bài 8", 2, 150, "KT", "", A, Q_II, CH3, "")],
 13:[t15("Bài 8: Khai căn bậc hai với phép nhân và phép chia", 7),
     ("Luyện tập chung Chương III", "Luyện tập chung", 2, 150, "KT", "", A, Q_II, CH3, "")],
 14:[("Ôn tập giữa học kì I (Chương I + Chương II + Bài 7–8)", "Ôn tập GHK I", "", 165, "KT", "", "", "", OGK1, "")],
 15:[("Kiểm tra giữa học kì I", "", "", 90, "Test", "Giữa kì", "", "", "Đề giữa kì 1", "Lần 2–4 giao về nhà"),
     ("Chữa đề giữa học kì I", "", "", 75, "KT", "", "", "", "", "")],
 16:[t15("Luyện tập chung Chương III", 8),
     ("Bài 9. Biến đổi đơn giản biểu thức chứa căn thức bậc hai", "Bài 9 (1/2)", 2, 150, "KT", "", A, Q_II, CH3, "SGV: Bài 9 = 3 tiết → tách 2 buổi")],
 17:[t15("Bài 9: Biến đổi đơn giản biểu thức chứa căn", 9),
     ("Bài 9. Rút gọn biểu thức chứa căn thức bậc hai", "Bài 9 (2/2)", 1, 75, "KT", "", A, Q_II2, CH3, "TRỌNG TÂM NHẤT của Câu II – 3/3 đề đều rút gọn A, B rồi hỏi câu phụ"),
     ("Bài 10. Căn bậc ba và căn thức bậc ba", "Bài 10", 1, 75, "KT", "", C, "", CH3, "")],
 18:[t15("Bài 9: Rút gọn biểu thức chứa căn thức bậc hai", 10),
     ("Câu II ý c – KHUÔN 1: tìm x để P nhận GIÁ TRỊ NGUYÊN (chặn khoảng P rồi xét ước)", "Bài 9 + Bài 5 (ráp)", "", 75, "KT", "", A, Q_II3, CH3, "BUỔI BẢN LỀ 7→8 ĐIỂM. Khuôn phổ biến nhất: 2/3 đề hỏi (2026 'tìm x để P = A.B nguyên'; 2025 'tìm x nguyên dương lớn nhất'). Cần căn thức + BĐT nên xếp sau khi học xong cả hai. " + KHO_CU),
     ("Câu II ý c – KHUÔN 2: so sánh P với một số / giải BPT chứa căn (P > k, P < k, P < P²)", "Bài 9 + Bài 6 (ráp)", "", 75, "KT", "", A, Q_II3, CH3, "2/3 đề hỏi: minh họa 'chứng minh P < P²' · 2025 'tìm x lớn nhất để A/B < 1/2'. " + KHO_CU)],
 19:kt45("III") + [("Luyện tập chung + Bài tập cuối chương III", "Luyện tập chung + BT cuối chương III", 3, 75, "KT", "", A, Q_II, CH3, "")],
 20:[("Ôn tập học kì I – Đại số: Hệ PT · PT quy về bậc nhất · Căn thức", "Ôn tập CHK I", "", 165, "KT", "", "", "", OCK1, "")],
 21:[("Kiểm tra cuối học kì I", "", "", 90, "Test", "Cuối kì", "", "", "Đề cuối kì 1", "Lần 2–4 giao về nhà"),
     ("Chữa đề cuối học kì I", "", "", 75, "KT", "", "", "", "", "")],
 # ===== Chương VI (16 tiết) — 6 buổi · Bài 18 CẮT HẲN (Thầy chốt) → chỉ dạy 13 tiết =====
 22:[("Bài 19. Phương trình bậc hai một ẩn – Khái niệm và công thức nghiệm", "Bài 19", 3, 165, "KT", "", A, Q_III3, CH6, "Buổi mở chương – chưa có KT 15′. Vào thẳng Bài 19 vì Bài 18 (đồ thị y=ax²) đã cắt")],
 23:[t15("Bài 19: Công thức nghiệm của phương trình bậc hai", 11),
     ("Luyện tập chung Chương VI", "Luyện tập chung", 2, 150, "KT", "", A, Q_III3, CH6, "")],
 24:[t15("Luyện tập chung Chương VI", 12),
     ("Bài 20. Định lí Viète và ứng dụng", "Bài 20", 2, 150, "KT", "", A, Q_III3, CH6, "TRỌNG TÂM – 3/3 đề đều hỏi Viète")],
 25:[t15("Bài 20: Định lí Viète và ứng dụng", 13),
     ("Câu III.3 – luyện KHUÔN Viète: biểu thức đối xứng của hai nghiệm, tìm m thoả điều kiện", "Bài 20 (luyện khuôn)", "", 150, "KT", "", A, Q_III3, CH6, "BUỔI BẢN LỀ 7→8 ĐIỂM – đúng dạng Câu III.3 của 3/3 đề. Tiết SGK Bài 20 đã tính ở tuần 24. " + KHO_CU)],
 26:[t15("Câu III.3: Viète – biểu thức đối xứng, tìm m", 14),
     ("Bài 21. Giải bài toán bằng cách lập phương trình + LUYỆN DẠNG Câu III.1 ngay", "Bài 21", 2, 150, "KT", "", A, Q_III1, CH6, "TRỌNG TÂM – 3/3 đề: năng suất, chuyển động. Thang điểm Sở 1,0đ. " + KHO_CU)],
 27:kt45("VI") + [("Luyện tập chung + Bài tập cuối chương VI", "Luyện tập chung + BT cuối chương VI", 4, 75, "KT", "", A, Q_III1, CH6, "")],
 # ===== Chương VII + VIII (18 tiết) — 3 buổi · Thầy chốt: chỉ luyện ý vào đề =====
 28:[("Bài 22. Bảng tần số và biểu đồ tần số + Bài 23. Bảng tần số tương đối và biểu đồ", "Bài 22 + Bài 23", 4, 165, "KT", "", B, "", CH7, "Nền để vào Bài 24 – ý thật sự đi thi", "Chỉ ý vào đề")],
 29:[t15("Bài 22–23: Bảng tần số · Tần số tương đối", 15),
     ("Bài 24. Bảng tần số, tần số tương đối GHÉP NHÓM và biểu đồ + BT cuối chương VII", "Bài 24 + BT cuối chương VII", 6, 150, "KT", "", A, Q_I1, CH7, "TRỌNG TÂM – 3/3 đề hỏi ĐÚNG ý này (thang điểm Sở 1,0đ – ý NB đắt nhất đề): cho bảng/biểu đồ ghép nhóm → tìm tần số + tần số tương đối. " + KHO_MOI, "Chỉ ý vào đề")],
 30:[t15("Bài 24: Tần số, tần số tương đối ghép nhóm", 16),
     ("Bài 25. Phép thử ngẫu nhiên, không gian mẫu + Bài 26. Xác suất của biến cố + BT cuối chương VIII", "Bài 25 + Bài 26 + BT cuối chương VIII", 8, 150, "KT", "", A, Q_I2, CH8, "TRỌNG TÂM – 3/3 đề: 1 phép thử đơn giản (đĩa quay/thẻ/bóng) → tính xác suất. Mức NB/TH. HẾT CHƯƠNG TRÌNH SGK. " + KHO_MOI, "Chỉ ý vào đề")],
 # ===== LUYỆN ĐỀ — 18 buổi =====
 31:[("ÔN LẠI + nâng dạng Câu I – Thống kê ghép nhóm + Xác suất (lần đầu luyện ở tuần 29–30)", "", "", 165, "KT", "", A, "Câu I (1,5đ)", LD, "1,5đ toàn NB/TH – phần DỄ ĂN NHẤT đề (riêng I.1 đã 1,0đ). Lặp ngắt quãng sau 3 tuần, KHÔNG dạy lại từ đầu")],
 32:[("ÔN LẠI + nâng dạng Câu II – Rút gọn biểu thức chứa căn (lần đầu luyện ở tuần 16–19)", "", "", 165, "KT", "", A, Q_II, LD, "Lặp ngắt quãng — nâng độ khó biểu thức, KHÔNG dạy lại từ đầu")],
 33:[("Luyện đề Câu II ý c – KHUÔN 3: GTLN – GTNN của P + ráp cả 3 khuôn (nguyên · so sánh · GTLN-GTNN)", "", "", 165, "KT", "", A, Q_II3, LD, "GTLN–GTNN KHÔNG xuất hiện ở 3/3 đề chính thức (minh họa · 2025 · 2026) nhưng là khuôn kinh điển và có trong đề thi thử → vẫn luyện, xếp sau 2 khuôn kia. Buổi cuối trước Tết")],
 34:[("ÔN LẠI + nâng dạng Câu III.1 – Lập phương trình (lần đầu luyện ở tuần 26)", "", "", 165, "KT", "", A, Q_III1, LD, "Lặp ngắt quãng — đổi bối cảnh bài toán, KHÔNG dạy lại từ đầu")],
 35:[("ÔN LẠI + nâng dạng Câu III.2 – Lập hệ phương trình (lần đầu luyện ở tuần 6 — cách 29 tuần, PHẢI ôn kỹ)", "", "", 165, "KT", "", A, Q_III2, LD, "KHOẢNG CÁCH XA NHẤT: học tuần 4–6, tới đây mới gặp lại → tầng C gần như quên hết, coi như dạy lại có giàn giáo")],
 36:[("ÔN LẠI + nâng dạng Câu III.3 – Viète (lần đầu luyện ở tuần 25)", "", "", 165, "KT", "", A, Q_III3, LD, "Lặp ngắt quãng, KHÔNG dạy lại từ đầu")],
 37:[("Thi thử vào 10 – lần 1: ĐỀ MINH HỌA của Sở GD&ĐT Hà Nội (8/2024)", "", "", 90, "Test", "Thi thử", "", "", "ĐỀ MINH HỌA của Sở GD&ĐT Hà Nội (8/2024)", "Thi chung toàn hệ thống"),
     ("Chữa đề thi thử lần 1", "", "", 75, "KT", "", "", "", "", "")],
 38:[("Ôn tập giữa học kì II", "Ôn tập GHK II", "", 165, "KT", "", "", "", OGK2, "")],
 39:[("Kiểm tra giữa học kì II", "", "", 90, "Test", "Giữa kì", "", "", "Đề giữa kì 2", "Lần 2–4 giao về nhà"),
     ("Chữa đề giữa học kì II", "", "", 75, "KT", "", "", "", "", "")],
 40:[("Thi thử vào 10 – lần 2: ĐỀ CHÍNH THỨC vào 10 Hà Nội 2025 (thi 08/6/2025)", "", "", 90, "Test", "Thi thử", "", "", "ĐỀ CHÍNH THỨC vào 10 Hà Nội 2025 (thi 08/6/2025)", ""),
     ("Chữa đề thi thử lần 2", "", "", 75, "KT", "", "", "", "", "")],
 41:[("Luyện đề Câu I + Câu II – gói điểm chắc 3,0đ của tầng C", "", "", 165, "KT", "", A, "Câu I + II (3,0đ)", LD, "Gói điểm mục tiêu của lớp C")],
 42:[("Thi thử vào 10 – lần 3: ĐỀ CHÍNH THỨC vào 10 Hà Nội 2026 (thi 31/5/2026)", "", "", 90, "Test", "Thi thử", "", "", "ĐỀ CHÍNH THỨC vào 10 Hà Nội 2026 (thi 31/5/2026)", ""),
     ("Chữa đề thi thử lần 3", "", "", 75, "KT", "", "", "", "", "")],
 43:[("Ôn tập cuối kì II – Đại số (gồm Thống kê – Xác suất)", "Ôn tập CK II", "", 135, "KT", "", "", "", OCK2, "Bù lại phần TK–XS đã nén"),
     ("Bài 18. Hàm số y = ax² – nhắc lại mức nhận biết, chỉ để qua đề CK của trường", "Bài 18", 3, 30, "KT", "", C, Q_NO, OCK2, "Thầy chốt CẮT HẲN: 3/3 đề vào 10 không hỏi vẽ đồ thị / tương giao parabol–đường thẳng. Không có buổi riêng, chỉ nhắc ở đây", "Bỏ – chỉ nhắc")],
 44:[("Kiểm tra cuối kì II", "", "", 90, "Test", "Cuối kì", "", "", "Đề cuối kì 2", "Lần 2–4 giao về nhà"),
     ("Chữa đề cuối kì II", "", "", 75, "KT", "", "", "", "", "")],
 45:[("Thi thử vào 10 – lần 4: Đề thi thử phòng GD&ĐT Hà Nội (Đống Đa / Thanh Oai) 2025–2026", "", "", 90, "Test", "Thi thử", "", "", "Đề thi thử phòng GD&ĐT Hà Nội (Đống Đa / Thanh Oai) 2025–2026", ""),
     ("Chữa đề thi thử lần 4", "", "", 75, "KT", "", "", "", "", "")],
 46:[("Thi thử vào 10 – lần 5: Đề thi thử phòng GD&ĐT Hà Nội (Hà Đông / Chương Mỹ) 2025–2026", "", "", 90, "Test", "Thi thử", "", "", "Đề thi thử phòng GD&ĐT Hà Nội (Hà Đông / Chương Mỹ) 2025–2026", ""),
     ("Chữa đề thi thử lần 5", "", "", 75, "KT", "", "", "", "", "")],
 47:[("Thi thử vào 10 – lần 6: Đề thi thử trường (Nguyễn Tất Thành / THCS Thái Thịnh) 2026", "", "", 90, "Test", "Thi thử", "", "", "Đề thi thử trường (Nguyễn Tất Thành / THCS Thái Thịnh) 2026", ""),
     ("Chữa đề thi thử lần 6", "", "", 75, "KT", "", "", "", "", "")],
 48:[("Thi thử vào 10 – lần 7: Đề TỔNG DUYỆT – trung tâm tự ra theo ma trận Sở", "", "", 90, "Test", "Thi thử", "", "", "Đề TỔNG DUYỆT – trung tâm tự ra theo ma trận Sở", ""),
     ("Chữa đề thi thử lần 7", "", "", 75, "KT", "", "", "", "", "")],
}

HINH_HOC = {
 1: [("Ôn tập nền Lớp 8 – Hình (1): Định lí Pythagore · Tứ giác", "Ôn tập đầu năm", "", 90, "KT", "", B, "", HE, "Nền cho tam giác vuông + đường tròn")],
 2: [("Ôn tập nền Lớp 8 – Hình (2): Hình thang cân · Hình bình hành", "Ôn tập đầu năm", "", 70, "KT", "", B, "", HE, ""),
     ("PP Lặp lại ngắt quãng", "", "", 20, "NT-PP", "", "", "", "", "")],
 3: [("Ôn tập nền Lớp 8 – Hình (3): Tam giác đồng dạng", "Ôn tập đầu năm", "", 70, "KT", "", A, Q_IV2, HE, "Công cụ chính để chứng minh hệ thức ở Câu IV.2"),
     ("Hoạt động phát triển tư duy", "", "", 20, "NT-TD", "", "", "", "", "")],
 # ===== Chương IV (11 tiết) — 3 buổi · Thầy chốt 2026-07-16: nâng từ 2 lên 3, đủ GK1 trường =====
 4: [("Bài 11. Tỉ số lượng giác của góc nhọn (khái niệm · góc đặc biệt · MTCT)", "Bài 11", 4, 90, "KT", "", C, Q_NO, CH4, "Không câu nào ở 3/3 đề vào 10. Dạy đủ qua GK1 trường (đề GK1 hỏi 90%), sau đó KHÔNG quay lại", "Tối thiểu")],
 5: [t15("Bài 11: Tỉ số lượng giác của góc nhọn", 1),
     ("Bài 12. Hệ thức giữa cạnh và góc trong tam giác vuông", "Bài 12", 3, 75, "KT", "", C, Q_NO, CH4, "Mức đủ GK1 trường", "Tối thiểu")],
 6: [t15("Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông", 2),
     ("Luyện tập chung + Bài tập cuối chương IV", "Luyện tập chung + BT cuối chương IV", 4, 75, "KT", "", C, Q_NO, CH4, "Buổi Thầy chốt thêm — đưa Chương IV từ 0,33× lên 0,44×", "Tối thiểu")],
 # ===== Chương V (15 tiết) — 7 buổi · TRỌNG TÂM Câu IV.2 =====
 7: [("Bài 13. Mở đầu về đường tròn", "Bài 13", 2, 90, "KT", "", A, Q_IV2, CH5, "Buổi mở chương – chưa có KT 15′")],
 8: [t15("Bài 13: Mở đầu về đường tròn", 3),
     ("Bài 14. Cung và dây của một đường tròn", "Bài 14", 2, 55, "KT", "", A, Q_IV2, CH5, ""),
     ("PP Hack não năng suất", "", "", 20, "NT-PP", "", "", "", "", "")],
 9: [t15("Bài 14: Cung và dây của một đường tròn", 4),
     ("Bài 15. Độ dài cung tròn. Diện tích hình quạt tròn và hình vành khuyên", "Bài 15", 2, 75, "KT", "", A, Q_IV1, CH5, "NÂNG HẠNG – Thầy chỉ ra: bài này CÓ trong đề thi thử và CÓ THỂ THAY hình khối ở Câu IV.1 (cùng là ý đo lường, mức NB/TH). Không được xem là phần bỏ đi. " + KHO_MOI)],
 10:[t15("Bài 15: Độ dài cung · Diện tích hình quạt, vành khuyên", 5),
     ("Luyện tập chung Chương V", "Luyện tập chung", 2, 75, "KT", "", A, Q_IV2, CH5, "")],
 11:[t15("Luyện tập chung Chương V", 6),
     ("Bài 16. Vị trí tương đối của đường thẳng và đường tròn – TIẾP TUYẾN", "Bài 16", 2, 75, "KT", "", A, Q_IV2, CH5, "TRỌNG TÂM – tiếp tuyến là công cụ thường trực của Câu IV.2")],
 12:[t15("Bài 16: Tiếp tuyến của đường tròn", 7),
     ("Bài 17. Vị trí tương đối của hai đường tròn – SƠ ĐỒ TỔNG QUAN (không luyện sâu)", "Bài 17", 2, 30, "KT", "", C, Q_NO, CH5, "Thầy chốt: tỉ trọng thấp, HS ít áp dụng → vẽ nhanh 1 sơ đồ tổng quan cho HS hiểu, KHÔNG bắt nhớ nhiều. Vẫn cho vào chứ không cắt", "Tối thiểu"),
     ("Luyện tập chung Chương V", "Luyện tập chung", 2, 45, "KT", "", A, Q_IV2, CH5, "")],
 13:[t15("Luyện tập chung Chương V", 8),
     ("Bài tập cuối chương V + LUYỆN DẠNG Câu IV.2 phần đường tròn – tiếp tuyến", "Bài tập cuối chương V", 1, 75, "KT", "", A, Q_IV2, CH5, "Xong Chương V là luyện ngay phần đường tròn của Câu IV.2. " + KHO_CU)],
 14:[("Ôn tập giữa học kì I – Hình (Chương IV + Bài 13–16)", "Ôn tập GHK I", "", 90, "KT", "", "", "", OGK1, "")],
 15:[("Kiểm tra giữa học kì I", "", "", 90, "Test", "Giữa kì", "", "", "Đề giữa kì 1", "Lần 2–4 giao về nhà")],
 16:[("Chữa đề giữa học kì I", "", "", 90, "KT", "", "", "", "", "")],
 17:[("Tam giác đồng dạng – ôn SÂU: công cụ chính để chứng minh hệ thức ở Câu IV.2 ý b", "Ôn nền Lớp 8 (nâng)", "", 90, "KT", "", A, Q_IV2b, CH9, "Thay cho KT 1 tiết Chương V (đã bị Giữa kì I ở tuần 15 kiểm tra trùng). Câu IV.2b là Ý ĐẮT NHẤT ĐỀ (1,5đ) và chạy hoàn toàn bằng tam giác đồng dạng — công cụ Lớp 8, chỗ HS nền yếu hổng nhất, mà trước đó chỉ có 70′ ở tuần 3")],
 # ===== Chương IX (12 tiết) — 6 buổi · TRỌNG TÂM Câu IV.2 =====
 18:[("Bài 27. Góc nội tiếp", "Bài 27", 1, 90, "KT", "", A, Q_IV2, CH9, "TRỌNG TÂM – 3/3 đề đều dùng góc nội tiếp")],
 19:[t15("Bài 27: Góc nội tiếp", 9),
     ("Bài 28. Đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác", "Bài 28", 2, 75, "KT", "", A, Q_IV2, CH9, "")],
 20:[("Ôn tập học kì I – Hình: Hệ thức lượng · Đường tròn · Góc nội tiếp", "Ôn tập CHK I", "", 90, "KT", "", "", "", OCK1, "")],
 21:[("Kiểm tra cuối học kì I", "", "", 90, "Test", "Cuối kì", "", "", "Đề cuối kì 1", "Lần 2–4 giao về nhà")],
 22:[("Chữa đề cuối học kì I", "", "", 90, "KT", "", "", "", "", "")],
 23:[t15("Bài 28: Đường tròn ngoại tiếp, nội tiếp tam giác", 10),
     ("Luyện tập chung Chương IX", "Luyện tập chung", 2, 75, "KT", "", A, Q_IV2, CH9, "")],
 24:[t15("Luyện tập chung Chương IX", 11),
     ("Bài 29. Tứ giác nội tiếp", "Bài 29", 2, 75, "KT", "", A, Q_IV2a, CH9, "TRỌNG TÂM NHẤT – 3/3 đề đều mở đầu Câu IV.2 bằng 'chứng minh 4 điểm cùng thuộc một đường tròn'")],
 25:[t15("Bài 29: Tứ giác nội tiếp", 12),
     ("Câu IV.2 ý a – luyện KHUÔN 'chứng minh 4 điểm cùng thuộc một đường tròn' + Luyện tập chung IX", "Bài 29 (luyện khuôn) + LTC", 2, 75, "KT", "", A, Q_IV2a, CH9, "Ý a của 3/3 đề — tầng C PHẢI lấy bằng được, thang điểm Sở 1,0đ mức TH. " + KHO_CU)],
 26:[t15("Câu IV.2a: chứng minh 4 điểm cùng thuộc một đường tròn", 13),
     ("Câu IV.2 ý b – luyện KHUÔN 'chứng minh hệ thức bằng tam giác đồng dạng' + BT cuối chương IX", "Bài 29 + đồng dạng (ráp) + BTCC IX", 1, 75, "KT", "", A, Q_IV2b, CH9, "BUỔI BẢN LỀ 7→8 ĐIỂM – Ý ĐẮT NHẤT ĐỀ (1,5đ theo thang điểm Sở). Ý b của 3/3 đề đều có 2 vế, vế đầu là hệ thức qua tam giác đồng dạng — DẠNG CÓ KHUÔN, tầng C ăn được điểm thành phần. " + KHO_CU)],
 27:kt45("IX"),
 # ===== Chương X (7 tiết) — 3 buổi · Thầy chốt =====
 28:[("Bài 31. Hình trụ và hình nón", "Bài 31", 2, 90, "KT", "", A, Q_IV1, CH10, "TRỌNG TÂM – 3/3 đề đều có hình trụ ở Câu IV.1 (thang điểm Sở: 1a Sxq 0,5đ + 1b thể tích 0,5đ). Chỉ áp công thức, mức NB – dễ ăn điểm. " + KHO_MOI)],
 29:[t15("Bài 31: Hình trụ và hình nón", 14),
     ("Bài 32. Hình cầu", "Bài 32", 2, 75, "KT", "", A, Q_IV1, CH10, "Đề minh họa có hình cầu (5 viên bi thả vào ly nước)")],
 30:[t15("Bài 32: Hình cầu", 15),
     ("Luyện tập chung + Bài tập cuối chương X", "Luyện tập chung + BT cuối chương X", 3, 75, "KT", "", A, Q_IV1, CH10, "LUYỆN DẠNG Câu IV.1 ngay sau khi xong Chương X. HẾT CHƯƠNG TRÌNH SGK. " + KHO_MOI)],
 # ===== LUYỆN ĐỀ — 18 buổi =====
 31:[("Luyện đề Câu IV.1 – Hình trụ · Hình nón · Hình cầu", "", "", 90, "KT", "", A, Q_IV1, LD, "~1,0đ chỉ áp công thức – phần dễ ăn điểm của tầng C")],
 32:[("Luyện đề Câu IV.2 ý a – Chứng minh 4 điểm cùng thuộc một đường tròn", "", "", 90, "KT", "", A, Q_IV2, LD, "Ý a của 3/3 đề – tầng C phải lấy bằng được ý này")],
 33:[("Luyện đề Câu IV.2 ý a – Tứ giác nội tiếp (luyện tiếp)", "", "", 90, "KT", "", A, Q_IV2, LD, "Buổi cuối trước Tết")],
 34:[("Luyện đề Câu IV.2 ý b – Chứng minh hệ thức bằng tam giác đồng dạng", "", "", 90, "KT", "", A, Q_IV2, LD, "")],
 35:[("Luyện đề Câu IV.2 ý b – Góc nội tiếp · Tiếp tuyến", "", "", 90, "KT", "", A, Q_IV2, LD, "")],
 36:[("Luyện đề hình tổng hợp – ráp cả Câu IV", "", "", 90, "KT", "", A, Q_IV2, LD, "")],
 37:[("Thi thử vào 10 – lần 1 (phần Hình): ĐỀ MINH HỌA của Sở GD&ĐT Hà Nội (8/2024)", "", "", 45, "Test", "Thi thử", "", "", "ĐỀ MINH HỌA của Sở GD&ĐT Hà Nội (8/2024)", "Thi chung toàn hệ thống"),
     ("Chữa đề thi thử lần 1 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 38:[("Ôn tập giữa học kì II – Hình", "Ôn tập GHK II", "", 90, "KT", "", "", "", OGK2, "")],
 39:[("Kiểm tra giữa học kì II", "", "", 90, "Test", "Giữa kì", "", "", "Đề giữa kì 2", "Lần 2–4 giao về nhà")],
 40:[("Thi thử vào 10 – lần 2 (phần Hình): ĐỀ CHÍNH THỨC vào 10 Hà Nội 2025 (thi 08/6/2025)", "", "", 45, "Test", "Thi thử", "", "", "ĐỀ CHÍNH THỨC vào 10 Hà Nội 2025 (thi 08/6/2025)", ""),
     ("Chữa đề thi thử lần 2 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 41:[("Luyện đề Câu IV.1 + IV.2 ý a – gói điểm chắc phần hình của tầng C", "", "", 90, "KT", "", A, "Câu IV.1 + IV.2a", LD, "Gói điểm mục tiêu phần hình của lớp C")],
 42:[("Thi thử vào 10 – lần 3 (phần Hình): ĐỀ CHÍNH THỨC vào 10 Hà Nội 2026 (thi 31/5/2026)", "", "", 45, "Test", "Thi thử", "", "", "ĐỀ CHÍNH THỨC vào 10 Hà Nội 2026 (thi 31/5/2026)", ""),
     ("Chữa đề thi thử lần 3 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 43:[("Ôn tập cuối kì II – Hình", "Ôn tập CK II", "", 70, "KT", "", "", "", OCK2, ""),
     ("Bài 30. Đa giác đều – nhắc lại mức nhận biết, chỉ để qua đề CK của trường", "Bài 30", 2, 20, "KT", "", C, Q_NO, OCK2, "Thầy chốt CẮT HẲN: không đề nào trong 3/3 hỏi đa giác đều. Không có buổi riêng, chỉ nhắc ở đây", "Bỏ – chỉ nhắc")],
 44:[("Kiểm tra cuối kì II", "", "", 90, "Test", "Cuối kì", "", "", "Đề cuối kì 2", "Lần 2–4 giao về nhà")],
 45:[("Thi thử vào 10 – lần 4 (phần Hình): Đề thi thử phòng GD&ĐT Hà Nội (Đống Đa / Thanh Oai) 2025–2026", "", "", 45, "Test", "Thi thử", "", "", "Đề thi thử phòng GD&ĐT Hà Nội (Đống Đa / Thanh Oai) 2025–2026", ""),
     ("Chữa đề thi thử lần 4 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 46:[("Thi thử vào 10 – lần 5 (phần Hình): Đề thi thử phòng GD&ĐT Hà Nội (Hà Đông / Chương Mỹ) 2025–2026", "", "", 45, "Test", "Thi thử", "", "", "Đề thi thử phòng GD&ĐT Hà Nội (Hà Đông / Chương Mỹ) 2025–2026", ""),
     ("Chữa đề thi thử lần 5 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 47:[("Thi thử vào 10 – lần 6 (phần Hình): Đề thi thử trường (Nguyễn Tất Thành / THCS Thái Thịnh) 2026", "", "", 45, "Test", "Thi thử", "", "", "Đề thi thử trường (Nguyễn Tất Thành / THCS Thái Thịnh) 2026", ""),
     ("Chữa đề thi thử lần 6 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
 48:[("Thi thử vào 10 – lần 7 (phần Hình): Đề TỔNG DUYỆT – trung tâm tự ra theo ma trận Sở", "", "", 45, "Test", "Thi thử", "", "", "Đề TỔNG DUYỆT – trung tâm tự ra theo ma trận Sở", ""),
     ("Chữa đề thi thử lần 7 – phần Hình", "", "", 45, "KT", "", "", "", "", "")],
}


def sundays(n):
    out, d = [], START
    while len(out) < n:
        if d not in TET_OFF:
            out.append(d)
        d += timedelta(weeks=1)
    return out
