#!/usr/bin/env python3
"""KẾ HOẠCH Ô — 3 đề ÔN TẬP + 3 đề CHÍNH THỨC cuối HK1 Toán 5 KNTT (Claude chốt 15/11/2026).

Khung (từ 8 đề CK1 trường 2024-2026 + mẫu "Đề ôn tập số 1 – T5 HK I" của trung tâm, 12/2025), 40 phút:
  PHẦN I (4đ): Câu 1–8 × 0,5đ
    C1 đọc/viết/giá trị chữ số STP (D01) · C2 so sánh, sắp xếp (D02) · C3 làm tròn (D03)
    C4 nhân, chia nhẩm 10/0,1 (D13) · C5 đổi đơn vị diện tích (D05) · C6 hình tam giác/hình phẳng (D18)
    C7 hình tròn (D20) · C8 ô xoay vòng (phân số thập phân, hỗn số, đơn vị đo phù hợp, thời gian…)
  PHẦN II (6đ): Bài 1 đặt tính + − × : (2đ) · Bài 2 viết số đo dạng STP 4 ý (1đ)
    · Bài 3 a) biểu thức b) tìm x / thuận tiện (1đ) · Bài 4 bài toán thực tế diện tích (1,5đ) · Bài 5 tư duy (0,5đ)
Luật cổng phủ dạng (Thầy 12/11): mỗi đề ôn đủ dạng dễ ≥30% đề thật; cả bộ ôn đủ dạng dễ ≥10% (≥2 đề).
Tham chiếu "ck1-2526-vinhbao#1a" = inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi/l5-ck1-2526-vinhbao.json, ý "1a".
Mỗi tham chiếu chỉ dùng MỘT lần trong cả 6 đề (đề chính thức không lặp câu đề ôn).
Dùng: scripts/de_ck1_lop5.py (dựng đề), scripts/gemini/viec_de_ck1_lop5.py (giao Gemini chép + giải).
"""

# (ô, [ref …], ghi chú cho thợ)
DE = {}
DE["on1"] = [
    ("C1", ["ck1-2526-vinhbao#1a"], ""),
    ("C2", ["ck1-2425-khanhthuy#2b"], ""),
    ("C3", ["ck1-2425-chiengen#3"], ""),
    ("C4", ["ck1-2425-lienhiep#I.2"], ""),
    ("C5", ["ck1-2425-chiengen#4"], ""),
    ("C6", ["ck1-2425-khanhthuy#3a"], "đổi thành trắc nghiệm 4 phương án (đáp án 29,7 cm2; phương án nhiễu: quên chia 2 = 59,4 …)"),
    ("C7", ["ck1-2526-vinhbao#5"], "có hình tròn bán kính 6 cm (TikZ)"),
    ("C8", ["ck1-2526-donghoa#1a"], ""),
    ("B1", ["ck1-2425-chiengen#7a", "ck1-2425-chiengen#7b", "ck1-2425-chiengen#7c", "ck1-2425-chiengen#7d"], ""),
    ("B2", ["ck1-2425-lienhiep#II.1a", "ck1-2425-lienhiep#II.1b", "ck1-2425-lienhiep#II.1c", "ck1-2425-lienhiep#II.1d"], ""),
    ("B3", ["ck1-2425-chiengen#8a", "ck1-2425-lienhiep#II.6a"], "a) biểu thức, b) tìm x"),
    ("B4", ["ck1-2526-vinhbao#10a", "ck1-2526-vinhbao#10b"], "2 ý a) 0,75đ b) 0,75đ; có hình thang ABCD như đề gốc"),
    ("B5", ["ck1-2526-myanhung#9"], ""),
]
DE["on2"] = [
    ("C1", ["ck1-2425-tanhoa#2"], ""),
    ("C2", ["ck1-2526-donghoa#2b"], ""),
    ("C3", ["ck1-2526-vinhbao#4a"], "đổi thành trắc nghiệm 4 phương án"),
    ("C4", ["ck1-2526-vinhbao#2"], ""),
    ("C5", ["ck1-2526-nguyenvantroi#4"], ""),
    ("C6", ["ck1-2526-myanhung#4a", "ck1-2526-myanhung#4b"], "Đúng/Sai 2 ý × 0,25đ; vẽ tam giác ABC trên lưới ô vuông, đường cao AH như đề gốc"),
    ("C7", ["ck1-2425-lienhiep#I.4"], "thêm phương án D cho đủ 4 (đề gốc in lỗi), giữ đáp án 27,632 dm"),
    ("C8", ["gk1-2526-chuvanan#3"], ""),
    ("B1", ["ck1-2425-khanhthuy#5a", "ck1-2425-khanhthuy#5b", "ck1-2425-khanhthuy#5c", "ck1-2425-tanhoa#8b"], ""),
    ("B2", ["ck1-2526-myanhung#7a", "ck1-2526-myanhung#7b", "ck1-2526-myanhung#7c", "ck1-2526-myanhung#7d"], ""),
    ("B3", ["ck1-2526-nguyenvantroi#7a", "ck1-2526-donghoa#8a"], "a) biểu thức, b) tính thuận tiện"),
    ("B4", ["ck1-2526-myanhung#8"], "1,5đ, tách 2 ý a) diện tích vườn b) phần còn lại"),
    ("B5", ["ck1-2425-lienhiep#II.6"], ""),
]
DE["on3"] = [
    ("C1", ["ck1-2526-donghoa#1b"], ""),
    ("C2", ["ck1-2526-nguyenvantroi#2a"], ""),
    ("C3", ["ck1-2526-donghoa#2a"], "giữ dạng điền 2 chỗ (hàng phần trăm, hàng phần mười), mỗi chỗ 0,25đ"),
    ("C4", ["ck1-2526-myanhung#1"], ""),
    ("C5", ["gk1-2425-minhkhai#5b"], ""),
    ("C6", ["ck1-2526-myanhung#2"], ""),
    ("C7", ["ck1-2526-vinhbao#6"], "đổi thành trắc nghiệm 4 phương án (nhiễu: dùng d làm r, quên nhân 3,14 …)"),
    ("C8", ["ck1-2425-khanhthuy#2c"], ""),
    ("B1", ["ck1-2425-lienhiep#II.2a", "ck1-2425-lienhiep#II.2b", "ck1-2425-lienhiep#II.2c", "ck1-2425-lienhiep#II.2d"], ""),
    ("B2", ["ck1-2526-nguyenvantroi#9a", "ck1-2526-nguyenvantroi#9b", "ck1-2526-nguyenvantroi#9c", "ck1-2526-nguyenvantroi#9d"], ""),
    ("B3", ["ck1-2526-vinhbao#9", "ck1-2425-lienhiep#II.6b"], "a) biểu thức, b) tìm x"),
    ("B4", ["ck1-2425-khanhthuy#6"], "1,5đ"),
    ("B5", ["gk1-2425-hongquang#II.4"], "0,5đ"),
]
DE["ct1"] = [
    ("C1", ["ck1-2526-nguyenvantroi#1a"], ""),
    ("C2", ["ck1-2425-lienhiep#I.3a"], "đổi thành trắc nghiệm: chọn dãy xếp đúng từ lớn đến bé"),
    ("C3", ["gk1-2526-nguyenvantroi#2b"], ""),
    ("C4", ["ck1-2425-tanhoa#5"], ""),
    ("C5", ["gk1-2526-ngoclam#4b"], ""),
    ("C6", ["ck1-2526-donghoa#4b", "ck1-2526-donghoa#4c"], "điền công thức diện tích hình tam giác và hình thang (mỗi ý 0,25đ), có hình nhỏ"),
    ("C7", ["ck1-2425-khanhthuy#3b"], "trắc nghiệm, có hình nửa hình tròn đường kính 6 cm; chu vi = nửa đường tròn + đường kính"),
    ("C8", ["gk1-2526-nguyenvantroi#2a"], ""),
    ("B1", ["ck1-2526-donghoa#5a", "ck1-2526-donghoa#5b", "ck1-2526-donghoa#5c", "ck1-2526-donghoa#5d"], ""),
    ("B2", ["ck1-2526-vinhbao#8"], "4 ô × 0,25đ"),
    ("B3", ["ck1-2425-chiengen#8b", "gk1-2526-nguyetduc#9b"], "a) biểu thức, b) tìm x"),
    ("B4", ["ck1-2526-donghoa#6"], "1,5đ"),
    ("B5", ["ck1-2526-vinhbao#11b"], "vẽ lại hình: AB = 24 m, 4 nửa đường tròn nối tiếp"),
]
DE["ct2"] = [
    ("C1", ["ck1-2526-vinhbao#1b"], ""),
    ("C2", ["gk1-2425-longbien#I.1c"], ""),
    ("C3", ["gk1-2425-longbien#I.1d"], ""),
    ("C4", ["ck1-2526-nguyenvantroi#5b"], "đổi thành trắc nghiệm chọn dấu >, <, ="),
    ("C5", ["gk1-2425-hongquang#I.3"], ""),
    ("C6", ["gk1-2526-ngoclam#5"], ""),
    ("C7", ["ck1-2526-donghoa#4d"], "trắc nghiệm: công thức tính diện tích hình tròn bán kính r"),
    ("C8", ["gk1-2526-chuvanan#7a", "gk1-2526-chuvanan#7b"], "Đúng/Sai 2 ý × 0,25đ"),
    ("B1", ["ck1-2526-myanhung#6a", "ck1-2526-myanhung#6b", "ck1-2526-nguyenvantroi#6a", "ck1-2526-myanhung#6c"], ""),
    ("B2", ["gk1-2425-longbien#II.3a", "gk1-2425-longbien#II.3b", "gk1-2425-longbien#II.3c", "gk1-2425-longbien#II.3d"], ""),
    ("B3", ["ck1-2526-nguyenvantroi#7b", "gk1-2526-donghoa#8a"], "a) biểu thức, b) tính thuận tiện"),
    ("B4", ["gk1-2425-longbien#II.5a", "gk1-2425-longbien#II.5b"], "a) 0,75đ b) 0,75đ"),
    ("B5", ["ck1-2526-donghoa#8b"], ""),
]
DE["ct3"] = [
    ("C1", ["ck1-2425-tanhoa#1"], ""),
    ("C2", ["ck1-2526-vinhbao#4b"], "đổi thành trắc nghiệm 4 phương án"),
    ("C3", ["gk1-2526-ngoclam#3a"], ""),
    ("C4", ["ck1-2526-nguyenvantroi#5a"], "đổi thành trắc nghiệm chọn dấu >, <, ="),
    ("C5", ["gk1-2526-nguyetduc#3"], ""),
    ("C6", ["ck1-2425-lienhiep#I.5"], "thêm phương án D cho đủ 4"),
    ("C7", ["gk1-2425-longbien#I.1e"], ""),
    ("C8", ["gk1-2425-minhkhai#2b"], ""),
    ("B1", ["ck1-2526-vinhbao#7a", "ck1-2526-vinhbao#7b", "ck1-2526-vinhbao#7c", "ck1-2526-vinhbao#7d"], ""),
    ("B2", ["ck1-2526-donghoa#3"], "4 ô × 0,25đ"),
    ("B3", ["ck1-2526-vinhbao#11a", "gk1-2526-nguyenthaihoci#12a"], "a) b) đều tính thuận tiện"),
    ("B4", ["ck1-2425-lienhiep#II.5"], "1,5đ, tách a) diện tích vườn b) diện tích còn lại"),
    ("B5", ["gk1-2425-hongquang#II.5"], ""),
]

DIEM = {"C1": 0.5, "C2": 0.5, "C3": 0.5, "C4": 0.5, "C5": 0.5, "C6": 0.5, "C7": 0.5, "C8": 0.5,
        "B1": 2.0, "B2": 1.0, "B3": 1.0, "B4": 1.5, "B5": 0.5}
MUC = {"C1": 1, "C2": 1, "C3": 1, "C4": 1, "C5": 2, "C6": 2, "C7": 2, "C8": 1,
       "B1": 1, "B2": 2, "B3": 2, "B4": 3, "B5": 3}
PHUT = {"C1": 1.5, "C2": 1.5, "C3": 1.5, "C4": 1.5, "C5": 2, "C6": 2, "C7": 2, "C8": 1.5,
        "B1": 8, "B2": 4, "B3": 4, "B4": 8, "B5": 3}

if __name__ == "__main__":
    dung = {}
    for k, ds in DE.items():
        assert [o for o, _, _ in ds] == list(DIEM), k
        for o, refs, _ in ds:
            for r in refs:
                assert r not in dung, f"{r} dùng lại ở {k} và {dung[r]}"
                dung[r] = k
    print(f"OK: {len(DE)} đề, {len(dung)} tham chiếu, không trùng; tổng điểm {sum(DIEM.values())}")
