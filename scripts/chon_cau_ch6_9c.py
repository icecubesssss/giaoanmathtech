# Chọn câu cả chương VI lớp 9C bản 2 (Thầy chốt kế hoạch 16/11/2026, Phiên 1).
# Luật: AGENTS.md "LUẬT HÌNH THỨC CÂU + BẢN CHẤT 40-40-20" + docs/quy-chuan-hoc-lieu.md §15.
#   NB = câu nhỏ gắn với đề (1,5′) · TH = bài gọn + câu hỏi gợi ý bước (6′) · VD = chỉ đề (12′)
#   Bài đã tách: giờ = tổng câu nhỏ. Quỹ 120′ = 32 NB + 8 TH + 2 VD (P1: 32 NB + 12 TH).
# Chạy:  python3 scripts/chon_cau_ch6_9c.py            (in bảng phút + kiểm trùng)
#        python3 scripts/chon_cau_ch6_9c.py --ghi      (ghi chon-cau.json + chon-cau.tsv)
import json, re, sys, collections, unicodedata

GOC = "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06"
W = [3, 1, 2, 1, 2, 2, 2, 0]          # trọng số lớp C (T1..T8), tổng 13
NGUONG = {"NB": 5, "TH": 6, "VD": 7}
RATE = {  # phút/câu theo vai (config/tier_spec.json, đại số lớp 9)
    "Ví dụ": {"NB": 1.0, "TH": 4.0, "VD": 8.0},
    "Trên lớp": {"NB": 1.5, "TH": 6.0, "VD": 12.0},
    "BTVN": {"NB": 1.3, "TH": 5.2, "VD": 10.4},
}
TN, DS, TLN = "Trắc nghiệm A–D", "Đúng/Sai", "Trả lời ngắn"
TH_GY = "Tự luận + câu hỏi gợi ý bước"
VD_DE = "Chỉ đề, HS tự giải"
VDK = "Ví dụ điền khuyết"
PHIEU = {
    "P1": "Phiếu 1 — PT bậc hai, biện luận nghiệm theo Δ",
    "P2": "Phiếu 2 — Viète, biểu thức đối xứng, tìm m theo hệ thức đối xứng",
    "P3": "Phiếu 3 — Viète, biểu thức không đối xứng và các dạng VD khác",
    "P4": "Phiếu 4 — Giải bài toán bằng cách lập PT",
    "P5": "Phiếu 5 — Luyện tập chung + kiểm tra chương 90′",
}

# (phiếu, vai, dạng, mức, số ý ở mức đó, số câu NB, loại §4b, mã, ý, hình thức, [T1..T7], lí do)
# Mức NB: số ý = 0, "số câu NB" là số câu nhỏ. Mức TH/VD: "số câu NB" là câu NB tách từ chính đề đó.
R = [
# ======================= P1 — PT bậc hai, biện luận Δ (không VD) =======================
# --- Ví dụ (GV làm mẫu) ---
("P1","Ví dụ","C6-01","NB",0,2,"NB lẻ LT","sgk-b19-vd1","a, c",VDK,[2,1,1,0,2,2,1],"Định nghĩa PT bậc hai + hệ số; ý c (ẩn 1/x) là bẫy 'không phải PT bậc hai'."),
("P1","Ví dụ","C6-02","NB",0,2,"NB lẻ LT","sgk-b19-vd3","a-b",VDK,[2,1,1,0,2,2,0],"Khuyết b: x² = 9 và (x + 1)² = 3 — mẫu hai kiểu khuyết b (lấy căn hai vế)."),
("P1","Ví dụ","C6-02","NB",0,1,"NB lẻ LT","sgk-b19-vd2","a",VDK,[2,1,1,0,1,2,0],"Khuyết c: 2x² − 4x = 0, đặt nhân tử chung."),
("P1","Ví dụ","C6-01","TH",1,0,"TH lẻ LT","sgk-b19-vd5","a-b-c",VDK,[2,1,1,2,1,1,2],"Mẫu đủ 3 bước: a, b, c → Δ → công thức nghiệm (nghiệm chứa căn)."),
("P1","Ví dụ","C6-01","TH",2,0,"TH lẻ LT","sgk-b19-vd6","a-b",VDK,[2,1,1,1,2,2,2],"Nghiệm kép (x² − 6x + 9) và vô nghiệm (2x² + 3x + 5) — đủ ba trường hợp của Δ cùng Ví dụ 5."),
# Thầy 16/11 tick "Không hay" tl-ptb2-11-tr6 (đề ghi Δ′) ⇒ thay tl-ptb2-07-tr5 ý b (cùng khuôn ba trường hợp, đề không có Δ′)
("P1","Ví dụ","C6-04","TH",1,0,"TH tách VD","tl-ptb2-07-tr5","b",VDK,[2,2,1,1,2,1,0],"Δ = 24m + 56 theo m rồi ba trường hợp: m > −7/3 hai nghiệm phân biệt, m = −7/3 nghiệm kép, m < −7/3 vô nghiệm — mẫu biện luận. Ý a (Δ = 104, nghiệm xấu), c bỏ."),
("P1","Ví dụ","C6-05","TH",1,0,"TH lẻ LT","ck2-hai-ba-trung-2024-III2","a",VDK,[2,2,1,0,2,2,1],"x² + ax − 1 = 0: Δ = a² + 4 > 0 (hoặc ac < 0) — mẫu 'luôn có hai nghiệm phân biệt'. Ý b (Viète) bỏ."),
("P1","Ví dụ","C6-06","TH",2,0,"TH ghép bài","tl-ptb2-14-tr6","a-b",VDK,[2,2,1,1,1,2,0],"Thay x = 3 tìm m rồi giải lại PT; b Δ = 4m² + 9 > 0 — mẫu 'biết một nghiệm' chưa cần Viète."),
("P1","Ví dụ","C6-01","TH",1,0,"TH lẻ LT","gk1-giang-vo-2024-Ia","",VDK,[2,2,1,0,2,2,2],"Đề GK1: (x + 1)² − 3(x − 2) = 7 ⇒ x² − x = 0 — mẫu biến đổi về dạng chuẩn rồi mới chọn cách giải."),
("P1","Ví dụ","C6-01","TH",1,0,"TH lẻ LT","gk1-nguyen-du-2025-1-3","",VDK,[2,1,1,0,2,2,2],"Đề GK1: x² − 1 = 5(x + 1) ⇒ x² − 5x − 6 = 0 — mẫu khai triển, chuyển vế."),
# --- Trên lớp: NB lẻ ---
("P1","Trên lớp","C6-01","NB",0,1,"NB lẻ LT","sgk-b19-tl1","",DS,[2,1,1,0,2,2,0],"Đ/S: mx² + 2x + 1 = 0 là PT bậc hai? — bẫy quên a ≠ 0."),
("P1","Trên lớp","C6-01","NB",0,2,"NB lẻ LT","sgk-6.8","a-b",TLN,[2,1,1,0,2,2,1],"Chuyển vế, thu gọn rồi đọc a, b, c — bước đầu của mọi bài 'biến đổi về dạng chuẩn'."),
("P1","Trên lớp","C6-01","NB",0,3,"NB lẻ LT","sgk-6.10","a-b-c",TLN,[2,1,1,0,2,2,1],"Tính Δ, kết luận số nghiệm (không giải) cho ba PT: hai nghiệm / kép / vô nghiệm."),
("P1","Trên lớp","C6-01","NB",0,1,"NB lẻ LT","sgk-b19-tt1","",DS,[2,2,1,0,2,2,1],"a và c trái dấu ⇒ PT luôn có hai nghiệm phân biệt — nhận xét dùng lại ở dạng 'chứng minh luôn có nghiệm'."),
("P1","Trên lớp","C6-01","NB",0,1,"NB lẻ LT","sgk-6.41","",TN,[2,1,1,0,2,2,1],"Trắc nghiệm nghiệm của x² + 7x + 12 = 0; các phương án đảo dấu."),
("P1","Trên lớp","C6-02","NB",0,1,"NB lẻ LT","ck2-phan-dinh-phung-2025-TN2","",TN,[2,1,1,0,2,2,0],"Đề CK2: x² − 2x = 0, phương án bẫy x = −2, x = 1/2."),
("P1","Trên lớp","C6-02","NB",0,1,"NB lẻ LT","gk1-thach-ban-2024-IIa","",TLN,[2,1,1,0,1,2,0],"Đề GK1: 8x² − 4x = 0 (khuyết c)."),
("P1","Trên lớp","C6-02","NB",0,2,"NB lẻ LT","sgk-b19-lt3","a-b",TLN,[2,1,1,0,2,2,0],"x² − 25 = 0 và (x + 3)² = 5 — bẫy quên nghiệm âm."),
("P1","Trên lớp","C6-02","NB",0,1,"NB tách TH","gk1-nghia-tan-2025-I1b","",TLN,[2,1,1,0,2,2,0],"Đề GK1: x² − 15 = 3(x − 5) ⇒ x² − 3x = 0; bẫy chia hai vế cho x."),
("P1","Trên lớp","C6-03","NB",0,2,"NB lẻ LT","sgk-6.24","a-b",TLN,[2,1,1,0,1,2,1],"Nhẩm nghiệm a + b + c = 0, a − b + c = 0 — nói như nhận xét khi kiểm nghiệm bằng máy tính (Thầy 16/11). Ý c (Viète) để P2."),
# --- Trên lớp: TH (bài gọn + gợi ý bước) ---
("P1","Trên lớp","C6-01","TH",1,2,"TH lẻ LT","ck2-hat-mon-2025-II1","",TH_GY,[2,1,1,1,2,2,2],"Đề CK2: chỉ rõ a, b, c rồi giải 3x² − 4x + 5 = 0 (vô nghiệm). NB tách: a, b, c; Δ < 0 ⇒ kết luận gì."),
("P1","Trên lớp","C6-01","TH",1,1,"TH lẻ LT","ck2-ba-dinh-2024-II2","",TH_GY,[2,1,1,0,1,1,2],"Đề CK2: x² − 6x − 14 = 0, Δ = 92 — nghiệm chứa căn. NB tách: tính Δ."),
("P1","Trên lớp","C6-01","TH",1,1,"TH lẻ LT","gk2-phan-dinh-giot-2024-2","c",TH_GY,[2,1,1,0,2,1,2],"Đề GK2: 5x² + 2√10x + 2 = 0 (nghiệm kép, hệ số chứa căn). Ý a trùng SGK, ý b nhẩm — bỏ."),
("P1","Trên lớp","C6-01","TH",1,2,"TH ghép bài","gk2-dong-anh-2025-12","a-b",TH_GY,[2,1,1,1,1,1,2],"Đề GK2: a 6x² − 4x − 1 = 0 (Δ = 40); b x² − √3x + √3 − 1 = 0 nhẩm a + b + c = 0 (NB). NB tách: tính Δ ở ý a."),
("P1","Trên lớp","C6-01","TH",1,1,"TH lẻ LT","gk1-thanh-cong-2025-II2","",TH_GY,[2,2,1,0,2,2,2],"Đề GK1: (x + 2)(x − 10) = −36 ⇒ x² − 8x + 16 = 0 (kép x = 4). NB tách: đưa về dạng chuẩn."),
("P1","Trên lớp","C6-04","TH",1,2,"TH tách VD","ck2-cau-dien-2025-III2","a",TH_GY,[2,2,1,0,2,2,0],"Đề CK2: Δ = −4m + 5 > 0 ⇒ m < 5/4. NB tách: 'hai nghiệm phân biệt ⇔ ?', Δ theo m. Ý b để dự phòng (không bốc hai lần)."),
("P1","Trên lớp","C6-04","TH",1,1,"TH tách VD","v10-tam-khuong-2025-III3","a",TH_GY,[2,2,1,0,2,2,0],"Đề minh họa Vào 10: tìm m để PT vô nghiệm (Δ = −4m + 9 < 0). NB tách: vô nghiệm ⇔ ?"),
("P1","Trên lớp","C6-05","TH",2,3,"TH ghép bài","gk2-nguyen-truong-to-2025-2","a-b",TH_GY,[2,2,1,2,2,2,1],"Đề GK2: a giải với m = 5; b Δ = 4(m − 2)² ≥ 0 ⇒ luôn có nghiệm (bẫy ≥ với >). NB tách: thay m, Δ theo m, bình phương ≥ 0. Ý c bỏ."),
("P1","Trên lớp","C6-05","TH",1,1,"TH tách VD","ck2-xuan-dinh-2025-III2","a",TH_GY,[2,2,1,0,1,2,1],"Đề CK2: x² − 2mx − 1 = 0, ac < 0 ⇒ luôn hai nghiệm phân biệt. NB tách: dấu của ac."),
("P1","Trên lớp","C6-06","TH",1,1,"TH lẻ LT","gk2-phan-dinh-giot-2024-33","",TH_GY,[2,2,1,0,1,2,0],"Đề GK2: x₁ = 1 ⇒ m = −2 ⇒ x₂ = −2 ⇒ A = −2026. NB tách: thay x = 1."),
("P1","Trên lớp","C6-04","TH",1,2,"TH tách VD","tl-ptb2-16-tr6","a-b",TH_GY,[2,2,1,2,1,2,0],"a thay x = 3 thấy luôn bằng 0 (NB tách — nghiệm không phụ thuộc m); b Δ = (m + 1)² = 0 ⇒ nghiệm kép khi m = −1. NB tách: thay x = 3, kép ⇔ Δ = 0."),
# --- BTVN ---
("P1","BTVN","C6-01","NB",0,4,"NB lẻ LT","sgk-b19-lt1","a-b-c-d",TN,[2,1,1,0,2,2,0],"Nhận biết PT bậc hai, hệ số; ý c (ẩn ở mẫu) là bẫy."),
("P1","BTVN","C6-02","NB",0,2,"NB lẻ LT","sgk-b19-lt2","a-b",TLN,[2,1,1,0,1,2,0],"Khuyết c: 2x² + 6x = 0, 5x² + 11x = 0."),
("P1","BTVN","C6-02","NB",0,2,"NB lẻ LT","sgk-6.9","a-b",TLN,[2,1,1,0,2,1,0],"2x² + x/3 = 0 và (3x + 2)² = 5."),
("P1","BTVN","C6-03","NB",0,2,"NB lẻ LT","sgk-b20-vd2","a-b",TLN,[2,1,1,0,1,2,1],"Nhẩm nghiệm x² − 6x + 5, 5x² + 14x + 9."),
("P1","BTVN","C6-03","NB",0,3,"NB lẻ LT","tl-viete-47-tr8","1, 2, 8",TLN,[2,1,1,0,1,2,1],"Ba PT nhẩm nghiệm (có một PT hệ số chứa √2)."),
("P1","BTVN","C6-01","NB",0,2,"NB lẻ LT","sgk-b20-hd3","a-b",TLN,[2,1,1,0,1,2,0],"Tính a + b + c, chứng tỏ x = 1 là nghiệm. Ý c (Viète) bỏ."),
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","gk2-ban-mai-2025-6a","",TH_GY,[2,1,1,0,1,2,2],"Đề GK2: 3x² + 7x + 2 = 0."),
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","gk2-ban-mai-2025-6b","",TH_GY,[2,2,1,0,2,2,2],"Đề GK2: 2x² − (x + 1)² = x − 3 ⇒ đưa về dạng chuẩn rồi giải."),
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","gk2-tay-mo-3-2025-II","b",TH_GY,[2,1,1,0,1,1,2],"Đề GK2: b 3x² − x − 5 (Δ = 61, nghiệm chứa căn). NB tách: tính Δ. Ý a bỏ (trùng 2x² − 9x + 7 = 0 của SGK 6.24 trên lớp)."),
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","gk1-thach-ban-2024-IIc","",TH_GY,[2,2,1,0,2,2,2],"Đề GK1: (2x + 3)² = (x − 5)² — chuyển vế, hằng đẳng thức hoặc khai triển."),
# Thầy 16/11 tick "Không hay" gk2-my-dinh-2-2025-21 (ý a trùng SGK b20-vd2) ⇒ thay đề thi cùng dạng (giữ tỉ lệ đề thi ≥ 50%)
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","ck2-be-van-dan-2025-III2","a",TH_GY,[2,1,1,0,1,2,2],"Đề CK2: thay m = 2 được x² + 3x + 2 = 0 (Δ = 1, x = −1; x = −2). NB tách: thay m = 2 được phương trình nào. Ý b (Viète) bỏ."),
("P1","BTVN","C6-01","TH",1,1,"TH lẻ LT","gk1-giang-vo-2024-Ib","",TH_GY,[2,2,1,0,2,2,2],"Đề GK1: 4x² = (x − 12)²."),
("P1","BTVN","C6-04","TH",1,2,"TH lẻ LT","tl-ptb2-08-tr6","",TH_GY,[2,2,1,0,2,2,0],"Nghiệm kép: Δ = 16(m² − m − 6) = 0 ⇒ m = 3, m = −2."),
("P1","BTVN","C6-04","TH",1,1,"TH tách VD","tl-ptb2-18-tr6","c",TH_GY,[2,1,1,0,2,2,0],"Hai nghiệm phân biệt: Δ = 24m + 24 > 0 ⇒ m > −1. Ý a, b bỏ (ý b nghiệm xấu)."),
("P1","BTVN","C6-05","TH",1,1,"TH tách VD","gk2-cau-dien-2025-32","a",TH_GY,[2,2,1,0,1,2,1],"Đề GK2: x² − 2mx − 3 = 0, ac < 0. Ý b để dự phòng."),
("P1","BTVN","C6-05","TH",1,1,"TH tách VD","v10-thanh-oai-l1-2024-III2","a",TH_GY,[2,2,1,0,2,2,1],"Đề thi thử Vào 10: Δ = (m − 2)² ≥ 0 ⇒ luôn có nghiệm. Ý b VDC bỏ (lớp C)."),

# ======================= P2 — Viète, đối xứng, tìm m đối xứng =======================
("P2","Ví dụ","C6-07","NB",0,2,"NB lẻ LT","sgk-b20-vd1","a-b",VDK,[2,1,1,0,2,2,1],"Kiểm Δ rồi mới viết tổng, tích (Ví dụ SGK) — bước bắt buộc trước Viète."),
("P2","Ví dụ","C6-07","TH",1,1,"TH ghép bài","sgk-ltc2-vd1","a-b",VDK,[2,1,1,1,1,2,1],"a chứng minh hai nghiệm phân biệt, b x₁² + x₂² — khuôn Bài III.3 đề thi."),
("P2","Ví dụ","C6-07","TH",2,0,"TH lẻ LT","tl-viete-04-tr2","",VDK,[2,1,1,1,1,2,1],"x₁² + x₂² và 1/x₁ + 1/x₂ trên cùng một PT: hai công thức gốc."),
("P2","Ví dụ","C6-07","TH",1,0,"TH lẻ LT","sgk-6.48","b",VDK,[2,1,1,0,1,2,1],"x₁³ + x₂³ = (x₁ + x₂)³ − 3x₁x₂(x₁ + x₂)."),
("P2","Ví dụ","C6-07","TH",1,0,"TH lẻ LT","sgk-6.35","b",VDK,[2,1,1,0,2,2,1],"(x₁ − x₂)² = (x₁ + x₂)² − 4x₁x₂."),
("P2","Ví dụ","C6-08","TH",1,0,"TH lẻ LT","ck2-phuc-dong-2024-902-III2","",VDK,[2,2,1,0,2,2,0],"Biết một nghiệm 1 − √2: không cần tìm m, dùng tổng hai nghiệm — mẫu cho đề minh họa Sở."),
("P2","Ví dụ","C6-07","TH",1,0,"TH lẻ LT","v10-ly-thuong-kiet-2025-III3","",VDK,[2,1,1,0,2,2,1],"Đề minh họa Vào 10: x₁/x₂ + x₂/x₁ — quy đồng về (x₁² + x₂²)/(x₁x₂)."),
("P2","Ví dụ","C6-07","TH",1,0,"TH lẻ LT","v10-nguyen-truong-to-2025-III3","",VDK,[2,2,1,0,1,2,1],"Đề minh họa Vào 10: x₂/(x₁ + 3) + x₁/(x₂ + 3) — mẫu quy đồng, khai triển hai vế."),
("P2","Ví dụ","C6-07","TH",1,0,"TH lẻ LT","v10-quang-trung-2025-III3","",VDK,[2,2,1,0,2,2,1],"Đề minh họa Vào 10: (5x₁ − x₂)/x₁ − (x₁ − 5x₂)/x₂ — rút gọn trước khi dùng Viète."),
("P2","Ví dụ","C6-11","VD",1,0,"VD lẻ","v10-be-van-dan-2025-III3","",VDK,[2,2,1,1,2,2,2],"Δ = (m + 1)² ⇒ điều kiện m ≠ −1; Viète ⇒ m = ±2 — mẫu đủ 4 bước tìm m."),
# NB lẻ
("P2","Trên lớp","C6-07","NB",0,4,"NB lẻ LT","sgk-6.23","a-b-c-d",TLN,[2,1,1,0,2,2,1],"Tổng, tích bốn PT; ý d (x² − x + 3) vô nghiệm — bẫy viết Viète khi không có nghiệm."),
("P2","Trên lớp","C6-07","NB",0,1,"NB lẻ LT","sgk-b20-tl1","",DS,[2,2,1,0,2,2,1],"x² − x + 1 = 0 'tổng, tích đều bằng 1' — Đ/S, bẫy quên Δ."),
("P2","Trên lớp","C6-07","NB",0,1,"NB lẻ LT","sgk-b20-tt1","",DS,[2,1,1,0,2,2,0],"Tổng và tích đối nhau: x² + x + 1 = 0 vô nghiệm — cùng bẫy, khác chiều."),
("P2","Trên lớp","C6-07","NB",0,2,"NB tách TH","ck2-gia-lam-2024-III2","",TLN,[2,1,1,1,1,2,1],"Đề CK2: chứng minh có hai nghiệm phân biệt, tính x₁ + x₂ − x₁x₂."),
("P2","Trên lớp","C6-07","NB",0,1,"NB lẻ LT","sgk-6.43","",TN,[2,1,1,0,1,2,1],"Trắc nghiệm x₁² + x₂² của x² − 5x + 6."),
("P2","Trên lớp","C6-06","NB",0,1,"NB lẻ LT","sgk-b20-lt2","c",TLN,[2,1,1,0,1,1,0],"Biết nghiệm −√2, tìm nghiệm còn lại bằng tích hai nghiệm (Viète). Ý a, b (nhẩm nghiệm) bỏ — P1 đã luyện nhẩm."),
("P2","Trên lớp","C6-10","NB",0,1,"NB lẻ LT","tl-viete-58-tr11","a",TLN,[2,1,1,0,2,2,0],"Hai nghiệm trái dấu ⇔ ac < 0 (x² + 4x + m ⇒ m < 0). Chỉ lấy ý trái dấu (dạng C6-10 lớp C)."),
("P2","Trên lớp","C6-10","NB",0,1,"NB lẻ LT","tl-viete-56-tr10","a",DS,[2,1,1,0,2,2,0],"Đ/S: x² − 2x + m có hai nghiệm trái dấu khi m < 0 — chống nhầm 'trái dấu' với 'Δ > 0'."),
# TH
("P2","Trên lớp","C6-07","TH",1,2,"TH lẻ LT","gk2-co-dong-2024-III2","",TH_GY,[2,1,1,0,1,2,1],"Đề GK2: x² − 5x + 2, x₁² + x₂². NB tách: Δ, tổng-tích."),
("P2","Trên lớp","C6-07","TH",1,3,"TH lẻ LT","ck2-thang-long-2025-III3","",TH_GY,[2,1,1,0,1,2,1],"Đề CK2: x² − 7x − 1, x₁² + x₂² − x₁x₂. NB tách: Δ (17/11 thêm theo ý Thầy), tổng-tích, viết biểu thức theo S, P."),
("P2","Trên lớp","C6-07","TH",1,3,"TH lẻ LT","v10-cau-giay-lan1-2026-III3","",TH_GY,[2,2,1,0,2,2,1],"Thi thử Vào 10 2026: tính Δ (17/11 thêm theo ý Thầy), tổng-tích, viết theo S, P rồi chứng minh x₁, x₂ ≠ 0, tổng nghịch đảo."),
("P2","Trên lớp","C6-07","TH",1,2,"TH lẻ LT","v10-thai-thinh-2025-III3-md2","",TH_GY,[2,1,1,0,1,2,1],"Đề minh họa Vào 10: tổng lập phương x² + 5x − 1. NB tách: Δ (17/11 thêm theo ý Thầy), tổng-tích."),
("P2","Trên lớp","C6-07","TH",1,3,"TH lẻ LT","ck2-ba-dinh-2024-II3","",TH_GY,[2,1,1,0,1,2,1],"Đề CK2: x₁/x₂ + x₂/x₁ với 2x² − x − 5. NB tách: Δ (17/11 thêm theo ý Thầy), tổng-tích, quy đồng."),
("P2","Trên lớp","C6-07","TH",1,3,"TH lẻ LT","v10-thai-thinh-2025-III3","",TH_GY,[2,2,1,0,1,2,1],"Đề minh họa Vào 10: 1/(x₁ + 3) + 1/(x₂ + 3) — quy đồng, khai triển. NB tách: Δ (17/11 thêm theo ý Thầy), tổng-tích (+ 1 câu NB ôn lớp 8)."),
("P2","Trên lớp","C6-08","TH",1,3,"TH lẻ LT","so-hn-minhhoa-III3","",TH_GY,[2,2,1,0,2,2,1],"Đề minh họa Sở HN: biết nghiệm (3 − √5)/2, tổng bình phương. NB tách: tìm a, tính Δ (17/11 thêm theo ý Thầy), tổng hai nghiệm = ?."),
("P2","Trên lớp","C6-11","TH",1,2,"TH tách VD","ck2-thai-thinh-2025-III2","",TH_GY,[2,2,1,1,2,2,2],"Đề CK2: x² + 3x + m, x₁² + x₂² = 2025 — VD hạ TH bằng câu hỏi định hướng (đk Δ ⇒ m ≤ 9/4; viết hệ thức theo tổng-tích; giải; đối chiếu)."),
# VD
("P2","Trên lớp","C6-11","VD",1,3,"VD lẻ","ck2-hoai-duc-2024-III2","a-b",VD_DE,[2,2,1,2,2,2,2],"Đề CK2: a giải với m = 2 (NB tách), b x₁² + x₂² = 7 + x₁x₂ ⇒ m = −1, m = 3; Δ = (m − 2)² ≥ 0."),
("P2","Trên lớp","C6-11","VD",1,2,"VD lẻ","ck2-lomonoxop-2024-III2","a-b",VD_DE,[2,2,1,2,2,2,2],"Đề CK2: a ac < 0 (NB tách), b x₁² + x₂² − x₁x₂ = 22 ⇒ m = ±2."),
# BTVN
("P2","BTVN","C6-07","NB",0,3,"NB lẻ LT","sgk-b20-lt1","a-b-c",TLN,[2,1,1,0,2,2,1],"Kiểm Δ = b² − 4ac rồi tính tổng, tích ba PT."),
("P2","BTVN","C6-07","NB",0,2,"NB lẻ LT","tl-viete-01-tr1","",TLN,[2,1,1,0,1,2,1],"Chứng minh hai nghiệm phân biệt, tính tổng-tích."),
("P2","BTVN","C6-03","NB",0,2,"NB lẻ LT","sgk-6.34","a-b",TLN,[2,1,1,0,1,1,0],"Nhẩm nghiệm hệ số chứa căn."),
("P2","BTVN","C6-10","NB",0,1,"NB lẻ LT","tl-viete-60-tr11","a",TLN,[2,1,1,0,2,2,0],"Hai nghiệm trái dấu: m + 1 < 0. Ý b–d bỏ (dấu nghiệm cùng dương: lớp C không làm)."),
("P2","BTVN","C6-07","TH",1,2,"TH lẻ LT","ck2-chu-van-an-dn-2025-2","b",TH_GY,[2,1,1,0,1,2,1],"x² − 4√3x + 8: x₁³ + x₂³. Ý a trùng PT x² + x − 6 (bỏ)."),
("P2","BTVN","C6-07","TH",1,2,"TH lẻ LT","v10-thai-thinh-2026-III3","",TH_GY,[2,1,1,0,1,2,1],"Thi thử Vào 10 2026: x² − 2x − 9, x₁/x₂ + x₂/x₁."),
("P2","BTVN","C6-07","TH",1,2,"TH lẻ LT","gk2-nguyen-du-2024-32","",TH_GY,[2,2,1,0,1,2,1],"Đề GK2: 1/(x₁ − 1) + 1/(x₂ − 1)."),
("P2","BTVN","C6-07","TH",1,2,"TH lẻ LT","v10-to-vinh-dien-2025-III3","",TH_GY,[2,2,1,0,1,2,1],"Đề minh họa Vào 10: khai triển (x₁ + x₂)(x₁ + 2x₂) − x₂² về đối xứng."),
("P2","BTVN","C6-07","TH",1,2,"TH ghép bài","ck2-phuc-loi-2024-3-2","a-b",TH_GY,[2,1,1,1,1,2,1],"Đề CK2: a chứng minh có nghiệm (NB), b x₁² + x₂² − 2x₁x₂."),
("P2","BTVN","C6-08","TH",1,2,"TH lẻ LT","v10-tho-loc-l3-2025-III3","",TH_GY,[2,1,1,0,2,2,1],"Thi thử Vào 10: nghiệm (−√13 − 5)/2, tổng bình phương."),
("P2","BTVN","C6-08","TH",1,1,"TH lẻ LT","ck2-dai-ang-2025-III2","",TH_GY,[2,1,1,0,2,2,0],"Đề CK2: nghiệm (1 + √13)/2, 3x₁²x₂ + 3x₁x₂²."),
("P2","BTVN","C6-08","TH",1,1,"TH lẻ LT","gk2-dong-anh-2025-33","",TH_GY,[2,1,1,0,2,2,0],"Đề GK2: nghiệm −√3 của x² + 4x + m, tổng nghịch đảo."),
("P2","BTVN","C6-11","VD",1,2,"VD lẻ","gk2-mai-dich-2024-32","",VD_DE,[2,2,1,1,2,2,2],"Đề GK2: Δ = 8m + 24 > 0; x₁² + x₂² = 20 ⇒ m = −5/2 (đối chiếu điều kiện)."),
("P2","BTVN","C6-11","VD",1,2,"VD lẻ","v10-thanh-oai-l2-2025-III3","",VD_DE,[2,2,1,1,2,2,2],"Thi thử Vào 10: Δ = 4(m − 2)² ≥ 0; x₁² + x₂² = 8 ⇒ m = 0, m = 2."),

# ======================= P3 — Viète không đối xứng + VD khác =======================
("P3","Ví dụ","C6-13","VD",1,0,"VD lẻ","ck2-phuc-dong-2025-III2","",VDK,[2,2,1,0,2,2,1],"Hạ bậc 4x₁² = 2x₁ + 1 rồi về Viète (trùng đề LNH 2025, tl-viete-41, luyện đề 18 — chỉ bốc một)."),
("P3","Ví dụ","C6-14","VD",1,0,"VD lẻ","v10-tho-loc-l4-2026-III3","",VDK,[2,2,1,1,2,2,0],"x₁ + 2026 = (x₁ − 1)² ⇒ căn = |x₁ − 1|; xét dấu hai nghiệm trước — mẫu dạng căn/trị tuyệt đối."),
("P3","Ví dụ","C6-15","VD",1,0,"VD lẻ","tl-viete-35-tr6","",VDK,[2,2,1,1,2,2,1],"3x₁ + 2x₂ = 1 kết hợp x₁ + x₂ = −2 ⇒ hệ ⇒ x₁, x₂ ⇒ m — mẫu hệ thức bậc nhất."),
("P3","Ví dụ","C6-16","VD",1,0,"VD lẻ","v10-tho-loc-l5-2025-III3","",VDK,[2,2,1,1,2,2,0],"Thay x₁² = 2mx₁ + 4m + 5 rồi về Viète ⇒ m = −5/6 — mẫu tìm m bằng hạ bậc."),
("P3","Ví dụ","C6-15","VD",1,0,"VD lẻ","v10-quoc-oai-l1-2024-3.2","b",VDK,[2,2,1,1,2,2,1],"x₁ = 3x₂ ⇒ biểu diễn theo Viète; điều kiện hai nghiệm phân biệt (Δ = 4(m − 2)² > 0)."),
("P3","Ví dụ","C6-15","TH",1,0,"TH tách VD","tl-viete-40-tr6","",VDK,[2,1,1,0,2,2,1],"x₁ − x₂ = 4 kết hợp x₁ + x₂ = 4 ⇒ x₁, x₂ ⇒ m — ví dụ nhẹ trước khi vào hệ số khác 1."),
("P3","Trên lớp","C6-13","TH",1,3,"TH tách VD","ck2-van-dien-2024-III2","a-b",TH_GY,[2,2,1,1,2,2,1],"Đề CK2: a chứng minh có nghiệm (NB), b A = x₁² + 3x₂ ⇒ x₁² = 3x₁ + 5 ⇒ A = 14. NB tách: x₁ là nghiệm ⇒ x₁² = ?"),
("P3","Trên lớp","C6-13","TH",1,3,"TH tách VD","v10-my-dinh-2-2026-III3","",TH_GY,[2,2,1,1,1,2,1],"Thi thử Vào 10 2026: x₁³ = 10x₁ + 3 ⇒ A = 3 (hạ bậc ba hai lần). Trùng PT với Ứng Hòa lần 3 — chỉ bốc Mỹ Đình."),
("P3","Trên lớp","C6-14","TH",1,3,"TH tách VD","v10-tu-lap-2026-III3","",TH_GY,[2,2,1,1,2,2,0],"Thi thử Vào 10 2026: hai nghiệm âm; −16x₁ + 5 = (x₁ − 3)² ⇒ A = 3 − x₁ − x₂ = 13."),
("P3","Trên lớp","C6-14","TH",1,3,"TH tách VD","v10-cum-thcs-cong-lap-2026-III3","",TH_GY,[2,2,1,1,2,2,0],"Thi thử Vào 10 2026: x₁ > 0 > x₂ ⇒ |x₁| − |x₂| = x₁ + x₂ = 8; T = 4/37."),
("P3","Trên lớp","C6-15","TH",1,3,"TH tách VD","gk2-ba-dinh-2024-III2","a-b",TH_GY,[2,2,1,2,2,2,1],"Đề GK2: a giải với m = 1 (NB tách), b x₁ − 2x₂ = 6 ⇒ x₂ = −1, x₁ = 4 ⇒ m = −4."),
("P3","Trên lớp","C6-15","TH",1,3,"TH tách VD","gk2-mai-dich-2025-32","",TH_GY,[2,2,1,1,2,2,1],"Đề GK2: 2x₁ − 5x₂ = −8 ⇒ x₁ = 1, x₂ = 2 ⇒ m = 3; đối chiếu Δ."),
("P3","Trên lớp","C6-15","TH",1,3,"TH tách VD","gk2-le-ngoc-han-2024-III2","a-b",TH_GY,[2,2,1,2,2,2,1],"Đề GK2: a biết nghiệm x = 3 tìm nghiệm còn lại (ôn P1, NB tách), b 2x₁ + 3x₂ = 1."),
("P3","Trên lớp","C6-16","TH",1,3,"TH tách VD","v10-luyen-de-8-2025-III3","",TH_GY,[2,2,1,1,2,2,0],"Luyện đề Mathtech: x₁²x₂ + mx₂ − x₂ = 4 ⇒ hạ bậc x₁² ⇒ 2m(m − 1) = 4 ⇒ m = 2, m = −1."),
("P3","Trên lớp","C6-13","VD",1,4,"VD lẻ","so-hn-2026-III3","",VD_DE,[2,2,1,1,2,2,1],"ĐÍCH: đề Sở HN 2026 — Q = (3x₂ − 1)/x₁ + 3x₁/x₂ − x₁ (thay 3x₂ − 1 = x₂², quy đồng)."),
("P3","Trên lớp","C6-16","VD",1,4,"VD lẻ","so-hn-2025-III3","",VD_DE,[2,2,1,1,2,2,0],"Đề Sở HN 2025: (70 − mx₁²)/x₂ = x₁ + mx₂ ⇒ quy đồng, về tổng-tích ⇒ m."),
("P3","BTVN","C6-13","VD",1,3,"VD lẻ","ck2-nghia-tan-2025-III2","",VD_DE,[2,2,1,1,2,2,1],"Đề CK2: hạ bậc trong bất phương trình ẩn m (trùng luyện đề 21 — chỉ bốc Nghĩa Tân)."),
("P3","BTVN","C6-15","VD",1,3,"VD lẻ","tl-viete-38-tr6","",VD_DE,[2,2,1,1,2,2,1],"Nghiệm này gấp 4 lần nghiệm kia; điều kiện hai nghiệm phân biệt."),
# Sửa chọn câu 16/11 đêm (Thầy: STK P3 ≤ 30%): bỏ tl-viete-39 (đề thiếu m — Gemini bắt), tl-viete-37,
# luyện đề 5; tab hết đề thi chưa dùng ở C6-13…16 ⇒ thay bằng 3 đề thi C6-11 có 1/x, hệ thức lệch.
("P3","BTVN","C6-11","TH",1,3,"TH tách VD","gk2-trung-vuong-2025-III2","",TH_GY,[2,2,1,1,2,2,1],"Đề GK2: x₁x₂ = −3 nên x₁x₂² = −3x₂ ⇒ hệ thức lệch −3x₁ + x₁x₂² thành −3(x₁ + x₂) = 9/2 ⇒ a = −3 ⇒ K = 1/2 (dùng tích để đưa về tổng)."),
("P3","BTVN","C6-11","TH",1,3,"TH tách VD","gk2-cau-giay-2024-II3","",TH_GY,[2,2,1,1,2,2,2],"Đề GK2: Δ = 40 − 4m > 0, x₁x₂ = m − 1 ≠ 0; x₁x₂ + 1 = m, 1/x₁ + 1/x₂ = 6/(m − 1) ⇒ m² − m − 6 = 0 ⇒ m = 3, m = −2 (đều nhận)."),
("P3","BTVN","C6-11","TH",1,3,"TH tách VD","ck2-trung-vuong-2025-III3","",TH_GY,[2,2,1,1,2,2,1],"Đề CK2: 1/x₁ + 1/x₂ = x₁x₂ ⇒ (2m − 1)/(−m) = −m ⇒ m = 1; Δ = 4m² + 1 > 0; A = x₁/x₂ + x₂/x₁ = −3."),
("P3","BTVN","C6-16","TH",1,3,"TH tách VD","v10-luyen-de-3-2025-III3","",TH_GY,[2,2,1,1,2,2,0],"Luyện đề: x₁² + (m − 2)x₁ + mx₂ = 9 ⇒ hạ bậc ⇒ m = 4."),
# 17/11 Thầy ("chọn lại"): luyện đề 19 trùng phương trình đề đích x²−3x+1 ⇒ bỏ. Tab hết câu C6-13 không trùng
# (LNH 2025, tl-viete-41 = Ví dụ Phúc Đồng; Ứng Hòa = PT Mỹ Đình 2) ⇒ lấy đề thi C6-11 Ngọc Lâm (T902 sinh đôi, không bốc).
("P3","BTVN","C6-11","TH",1,3,"TH tách VD","ck2-ngoc-lam-2024-T901-III2","",TH_GY,[2,2,1,1,2,2,1],"Đề CK2: x₁² + x₂² = 73 ⇒ k² + 10k − 75 = 0, k > 0 ⇒ k = 5 ⇒ x₁ + x₂ = −5, x₁x₂ = −24 ⇒ B = x₁³ + x₂³ = −485."),
("P3","BTVN","C6-07","TH",1,2,"TH lẻ LT","v10-luyen-de-20-2025-III3","",TH_GY,[2,1,1,0,1,2,1],"Luyện đề: m/(x₁ + x₂) + x₁/x₂ + x₂/x₁ = 6 ⇒ m = 20 (ôn đối xứng trong PT ẩn m)."),
("P3","BTVN","C6-08","TH",1,2,"TH lẻ LT","v10-luyen-de-6-2025-III3","",TH_GY,[2,1,1,0,2,2,0],"Luyện đề: nghiệm (1 − √5)/2, tổng lập phương (ôn P2)."),
("P3","BTVN","C6-08","TH",1,1,"TH lẻ LT","v10-luyen-de-17-2025-III3","",TH_GY,[2,1,1,0,2,2,0],"Luyện đề: nghiệm (3 − √13)/2, bình phương hiệu (ôn P2)."),
# Bài làm thêm C6-28 — Thầy 16/11: ghi vào TM, KHÔNG tính giờ, GV tùy chọn, không ưu tiên
("P3","Làm thêm","C6-28","TH",1,0,"TH lẻ LT","gk2-ba-dinh-2025-I","a-b",TH_GY,[1,1,1,1,1,2,1],"Tìm m để (P) qua A rồi tìm giao điểm với d — PT hoành độ giao điểm là PT bậc hai."),
("P3","Làm thêm","C6-28","TH",1,0,"TH lẻ LT","tl-ptb2-23-tr8","",TH_GY,[1,1,1,0,2,2,1],"d cắt (P) tại hai điểm phân biệt ⇔ PT hoành độ có Δ > 0."),
("P3","Làm thêm","C6-28","VD",1,0,"VD lẻ","v10-quoc-oai-l2-2024-3.2","a-b",VD_DE,[1,2,1,2,1,2,1],"a giao điểm khi m = 3; b hai điểm khác phía trục tung (ac < 0) + x₁² + (m − 1)x₂ = 7 (hạ bậc)."),

# ======================= P4 — lập phương trình (đã bỏ C6-17 ngày 17/11) =======================
("P4","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","sgk-b21-vd1","",VDK,[2,1,2,0,1,2,2],"Hình học: sân bóng — mẫu 3 bước SGK (lập PT, giải, trả lời)."),
("P4","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","sgk-b21-vd2","",VDK,[2,2,2,0,2,2,2],"Chuyển động trên dòng nước có nghỉ 30 phút — mẫu bảng v, t, s."),
("P4","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","sgk-b21-lt1","",VDK,[2,1,2,0,2,2,2],"Năng suất kiểu 'bớt xe, mỗi xe chở thêm' — mẫu bảng số xe, khối lượng/xe."),
("P4","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","v10-thai-thinh-2025-III2","",VDK,[2,1,2,0,2,2,2],"Đề minh họa Vào 10: in 2000 quyển, mỗi ngày thêm 100, sớm 1 ngày ⇒ x² + 100x − 200 000 = 0 ⇒ 400 quyển/ngày — mẫu năng suất 'xong sớm hơn kế hoạch' (thay sgk-6.33: tab trùng nguyên văn tl-lpt-41-tr9, Thầy 16/11 'bốc lại')."),
("P4","Ví dụ","C6-18","VD",1,0,"VD lẻ","gk2-le-ngoc-han-2025-III1","",VDK,[2,2,2,1,2,2,2],"Chia hai giai đoạn, dừng 10 phút, tăng vận tốc (trùng đề Phan Đình Giót 2024 — chỉ bốc LNH)."),
("P4","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","gk1-nguyen-binh-khiem-2025-II2-md902","",VDK,[2,1,2,0,2,2,2],"Đề GK1: 108 km, xe I nhanh hơn 6 km/h, xe II đến muộn 12 phút ⇒ x² + 6x − 3240 = 0 ⇒ 54 và 60 km/h — mẫu 'cùng quãng đường, hơn vận tốc, đến sớm hơn' đi cùng bài Lômônôxốp (thay sgk-b19-vdg1 ngày 17/11: bể bơi không có bài hình học đi cùng trên lớp, vi_du_gate)."),
("P4","Ví dụ","C6-18","VD",1,0,"VD lẻ","ck1-cau-dien-2025-3b","",VDK,[2,2,2,1,2,2,1],"Làm chung – làm riêng: mẫu “một giờ làm được 1/x công việc”."),
("P4","Trên lớp","C6-18","NB",0,1,"NB lẻ LT","gk2-cau-dien-2025-2","",TN,[2,1,1,0,2,2,1],"NB kiến thức cũ (17/11, Thầy: ôn phải là thứ các bài dưới dùng): chỉ bước khử mẫu 240/x − 240/(x + 10) = 2 ⇒ 240(x + 10) − 240x = 2x(x + 10) — thao tác có ở mọi bài lập PT; thay ĐKXĐ Láng Thượng (phương trình chứa ẩn ở mẫu HS đã thạo từ lớp 8, cắt khỏi P4)."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","ck2-lomonoxop-2025-III2","",TH_GY,[2,1,2,0,2,2,2],"Đề CK2: dự định 100 km, tăng 10 km/h, sớm 30 phút ⇒ 40 km/h. NB tách: t = s/v, đổi 30 phút, PT."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","v10-dong-da-de18-2025-III2","",TH_GY,[2,1,2,0,2,2,2],"Đề minh họa Vào 10: ca nô 30 km, dòng 4 km/h, tổng 4 giờ. NB tách: v xuôi, v ngược."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","so-hn-minhhoa-III2","",TH_GY,[2,1,2,0,2,2,2],"Đề minh họa Sở HN: 300 sản phẩm, thêm 10/ngày, sớm 1 ngày. NB tách: số ngày theo kế hoạch/thực tế."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","gk2-ba-dinh-2024-III1","",TH_GY,[2,1,2,0,2,2,2],"Đề GK2: 60 tấn, bớt 2 xe, mỗi xe thêm 1 tấn ⇒ 12 xe."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","sgk-6.15","",TH_GY,[2,1,2,0,1,2,2],"SGK: vườn HCN rộng kém dài 6 m, S = 280 m² ⇒ 14 m, 20 m (thay đề Cát Linh cùng khuôn để đủ SGK ≥ 20%)."),
("P4","BTVN","C6-18","TH",1,2,"TH lẻ LT","v10-cat-linh-2025-III1","",TH_GY,[2,1,2,0,1,2,2],"Đề minh họa Vào 10: HCN rộng kém dài 11 m, S = 180 m² — cùng khuôn SGK 6.15, dự phòng ⇒ 17/11 lên BTVN thay bài phương trình chứa ẩn ở mẫu ⇒ 9 m và 20 m."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","sgk-6.31","",TH_GY,[2,1,2,0,2,2,1],"SGK: máy bay Hà Nội – TP HCM 1 200 km, nghỉ 96 phút, về nhanh hơn 100 km/h, tổng 6 giờ ⇒ 11v² − 4900v − 300 000 = 0 ⇒ v = 500 km/h (thay sgk-6.29: tab trùng nguyên văn tl-lpt-03-tr2, Thầy 16/11 'bốc lại'; biến thể % chuyển sang P5 bằng SGK 6.51)."),
("P4","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","gk2-nguyen-du-2024-22","",TH_GY,[2,1,2,0,2,2,2],"Đề GK2: ô tô – xe máy 120 km, hơn 20 km/h, sớm 30 phút ⇒ x² + 20x − 4800 = 0 ⇒ 60 và 80 km/h — đi cùng Ví dụ hai ô tô (17/11 thay phần phương trình chứa ẩn ở mẫu)."),
("P4","Trên lớp","C6-18","TH",1,4,"TH lẻ LT","v10-ung-hoa-lan3-2025-III2","",TH_GY,[2,1,2,0,2,2,2],"Thi thử Vào 10: làm chung 3 giờ 36 phút, người I nhanh hơn 3 giờ ⇒ 5x² − 21x − 54 = 0 ⇒ 6 giờ và 9 giờ — làm chung mức TH có câu dẫn trước bài VD Quốc Oai (17/11 thay phần phương trình chứa ẩn ở mẫu)."),
("P4","Trên lớp","C6-18","VD",1,3,"VD lẻ","v10-tu-lap-2026-III2","",VD_DE,[2,2,2,1,2,2,2],"Thi thử Vào 10 2026: 12 km, 3 km đầu như thường, dừng sửa xe rồi tăng tốc — chuyển động hai giai đoạn."),
("P4","Trên lớp","C6-18","VD",1,3,"VD lẻ","v10-quoc-oai-l2-2024-2.1","",VD_DE,[2,2,2,1,2,2,1],"Thi thử Vào 10: hai vòi chảy chung 2 giờ 40 phút, vòi I đầy trước 4 giờ ⇒ 3x² − 4x − 32 = 0 ⇒ 4 giờ và 8 giờ (17/11: thay ck2-mai-dich-2025-3-2 — trùng số liệu với Ví dụ Cầu Diễn — rồi lên lớp đổi chỗ Thọ Lộc để đi ngay sau ví dụ làm chung)."),
("P4","BTVN","C6-18","TH",1,3,"TH lẻ LT","ck2-thai-thinh-2025-III1","",TH_GY,[2,1,2,0,2,2,2],"Đề CK2: ô tô – xe máy 90 km, hơn 15 km/h, sớm 30 phút."),
("P4","BTVN","C6-18","TH",1,3,"TH lẻ LT","v10-thai-thinh-2025-III2-md2","",TH_GY,[2,1,2,0,2,2,2],"Đề minh họa Vào 10: xe đạp 36 km, về nhanh hơn 3 km/h, ít hơn 36 phút."),
("P4","BTVN","C6-18","TH",1,2,"TH lẻ LT","gk2-tay-mo-3-2025-III1","",TH_GY,[2,1,2,0,2,2,2],"Đề GK2: ô tô – xe máy 150 km, hơn 25 km/h, sớm 60 phút ⇒ x² + 25x − 3750 = 0 ⇒ 50 và 75 km/h (17/11 thay bài phương trình chứa ẩn ở mẫu)."),
("P4","BTVN","C6-18","TH",1,3,"TH lẻ LT","gk1-son-dong-2024-22","",TH_GY,[2,1,2,0,2,2,2],"Đề GK1: 600 sản phẩm, thêm 30/ngày, sớm 1 ngày ⇒ x² + 30x − 18 000 = 0 ⇒ 120 (thay ck2-cau-giay-2024-III1 ngày 17/11: cùng phương trình x² + 15x − 2700 = 0, đáp số 45 với Thái Thịnh CK2 trong BTVN)."),
("P4","BTVN","C6-18","TH",1,3,"TH lẻ LT","v10-phuong-mai-2025-III2","",TH_GY,[2,1,2,0,2,2,2],"Đề minh họa Vào 10: 144 dụng cụ, 3 công nhân chuyển đi, mỗi người thêm 4."),
("P4","BTVN","C6-18","TH",1,2,"TH lẻ LT","sgk-6.28","",TH_GY,[2,1,2,0,2,2,2],"SGK: HCN 360 m², rộng +3, dài −4, diện tích không đổi."),
("P4","BTVN","C6-18","TH",1,2,"TH lẻ LT","sgk-6.13","",TH_GY,[2,1,2,0,1,2,1],"SGK: mô hình h = 19,6t − 4,9t² (cho sẵn công thức)."),
("P4","BTVN","C6-18","VD",1,3,"VD lẻ","v10-tho-loc-l5-2025-III2","",VD_DE,[2,2,2,1,2,2,2],"Thi thử Vào 10: 480 sản phẩm, làm 60 rồi tăng 5/ngày, sớm hơn — năng suất hai giai đoạn. (17/11 xuống BTVN, đổi chỗ Quốc Oai lên lớp đi cùng ví dụ làm chung)."),
("P4","BTVN","C6-18","VD",1,3,"VD lẻ","v10-khuong-thuong-2025-III2","",VD_DE,[2,2,2,1,2,2,2],"Đề minh họa Vào 10: xe máy đi trước 24 phút, ô tô nhanh hơn 5 km/h, đến cùng lúc."),

# ======================= P5 — Luyện tập chung (~90′) + KT 90′ =======================
("P5","Ví dụ","C6-07","TH",1,1,"TH ghép bài","v10-dong-da-de18-2025-III3","",VDK,[2,1,1,1,1,2,1],"Đề minh họa Vào 10: chứng minh hai nghiệm phân biệt + M = x₁² + x₂² − 6x₁x₂ — chữa mẫu Bài III.3."),
("P5","Ví dụ","C6-11","VD",1,1,"VD lẻ","ck2-le-hong-phong-2025-IV","a-b",VDK,[2,2,1,2,2,2,2],"Đề CK2: a giải với m = 3, b hai nghiệm phân biệt + x₁² + x₂² = x₁x₂ + 46 — chữa mẫu Bài III.2b."),
("P5","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","ck1-phuc-dong-2025-III1-md903","",VDK,[2,1,2,0,2,2,2],"Đề CK1: 400 sản phẩm, thêm 20/ngày — chữa mẫu năng suất."),
("P5","Ví dụ","C6-18","TH",1,0,"TH lẻ LT","ck2-cau-dien-2025-III1","",VDK,[2,1,2,0,2,2,2],"Đề CK2: 90 km, nghỉ 30 phút, về nhanh hơn 9 km/h — chữa mẫu chuyển động."),
("P5","Ví dụ","C6-18","NB",0,2,"NB lẻ LT","sgk-b21-hd1","HĐ1-HĐ2",VDK,[2,1,2,0,2,2,1],"SGK Bài 21 HĐ1–HĐ2: biểu thị tiền sau kì 1 là 100(1 + x), sau kì 2 là 100(1 + x)² — mẫu lãi kép dẫn vào SGK 6.51 trên lớp (bù 2′ ví dụ, Thầy 16/11); HĐ3: 100(1 + x)² = 118,81 ⇒ x = 9%."),
("P5","Trên lớp","C6-11","VD",1,2,"VD lẻ","ck2-ha-dong-2024-III2","a-b",VD_DE,[2,2,1,2,2,2,2],"Đề CK2: a luôn hai nghiệm phân biệt (NB tách), b 1/x₁ + 1/x₂ = 2."),
("P5","Trên lớp","C6-04","TH",2,2,"TH ghép bài","gk2-duc-giang-2025-III2","a-b",TH_GY,[2,2,1,2,2,2,1],"Đề GK2: a điều kiện hai nghiệm phân biệt (m > 1/2), b với m = 2 tính x₁/x₂ + x₂/x₁."),
("P5","Trên lớp","C6-18","TH",1,3,"TH lẻ LT","sgk-6.51","",TH_GY,[2,1,2,0,2,2,1],"SGK bài tập cuối chương: gửi 100 triệu, năm sau gửi thêm 50 triệu, sau hai năm 176 triệu ⇒ 100(1 + x)² + 50(1 + x) = 176 ⇒ x = 10% (thay luyện đề 14 — P5 SGK lên ≥ 20%, Thầy 16/11)."),
# 17/11 phiên P5 (Thầy: bỏ hẳn C6-17 — HS đã thạo PT chứa ẩn ở mẫu từ lớp 8): Giảng Võ, Chuyên Mỹ → Phương Mai ý 1
("P5","Trên lớp","C6-05","TH",1,2,"TH lẻ LT","v10-phuong-mai-2025-III3","1",TH_GY,[2,2,1,0,2,2,1],"Đề minh họa Vào 10 (Phương Mai): x² − 2(m + 1)x + m − 4 = 0, Δ = 4m² + 4m + 20 = (2m + 1)² + 19 > 0 ⇒ luôn hai nghiệm phân biệt. Chỉ ý 1 (ý 2 'không phụ thuộc m' là C6-12, Thầy bỏ). NB tách: a, b, c; Δ theo m."),
("P5","Trên lớp","C6-01","NB",0,3,"NB lẻ LT","gk2-cau-dien-2025-31","a-b",TLN,[2,1,1,0,1,2,2],"Đề GK2: a nhẩm 2x² − 5x + 3, b x² − 5x − 4 (Δ = 41) — khởi động."),
("P5","Trên lớp","C6-07","NB",0,1,"NB lẻ LT","sgk-6.42","",TN,[2,1,1,0,2,2,1],"Trắc nghiệm: PT có hai nghiệm 13 và 25 (tổng 38, tích 325) — đọc ngược Viète, không thành dạng 'lập PT'."),
# 17/11 phiên P5: ví dụ năng suất, chuyển động phải có bài đi ngay sau (vi_du_gate) ⇒ 2 câu NB trắc nghiệm bước biểu diễn đại lượng
("P5","Trên lớp","C6-18","NB",0,1,"NB lẻ LT","gk2-le-ngoc-han-2024-III1","",TN,[2,1,2,0,2,2,1],"Đề GK2: 1 100 sản phẩm, vượt mức 5/ngày, sớm 2 ngày — chỉ hỏi bước biểu diễn số ngày thực tế 1100/(x + 5) (đi sau ví dụ năng suất Phúc Đồng)."),
("P5","Trên lớp","C6-18","NB",0,1,"NB lẻ LT","ck2-dai-ang-2025-III1","",TN,[2,1,2,0,2,2,1],"Đề CK2: AB 80 km, xe thứ nhất nhanh hơn 10 km/h, sớm 24 phút — chỉ hỏi bước lập phương trình 80/x − 80/(x + 10) = 2/5 (đi sau ví dụ chuyển động Cầu Diễn)."),
("P5","Trên lớp","C6-18","NB",0,1,"NB lẻ LT","sgk-6.44","",TN,[2,1,2,0,2,2,1],"Trắc nghiệm HCN chu vi 20, diện tích 24."),
("P5","BTVN","C6-11","VD",1,3,"VD lẻ","gk2-nghia-tan-2024-III2","a-b",VD_DE,[2,2,1,2,2,2,2],"Đề GK2: a luôn hai nghiệm phân biệt, b m > 0 và x₁² + x₂² = 9 ⇒ m = 1."),
("P5","BTVN","C6-11","VD",1,3,"VD lẻ","gk2-tay-mo-3-2025-III2","",VD_DE,[2,2,1,1,2,2,2],"Đề GK2: x₁² + x₂² − 3x₁x₂ = −1 ⇒ m = 4; Δ = 17 − 4m > 0."),
("P5","BTVN","C6-18","TH",1,3,"TH lẻ LT","ck2-phuc-dong-2024-901-III1","",TH_GY,[2,1,2,0,2,2,2],"Đề CK2: trồng 30 cây, mỗi giờ thêm 5 cây."),
("P5","BTVN","C6-18","TH",1,3,"TH lẻ LT","gk2-nhat-tan-2024-III2","",TH_GY,[2,1,2,0,2,2,2],"Đề GK2: 60 tấn, 3 xe điều đi, mỗi xe thêm 1 tấn."),
("P5","BTVN","C6-18","TH",1,3,"TH lẻ LT","gk2-nghia-tan-2024-II","",TH_GY,[2,1,2,0,2,2,2],"Đề GK2: đi 90 km, về đường khác 100 km nhanh hơn 10 km/h."),
("P5","BTVN","C6-18","TH",1,3,"TH tách VD","sgk-6.52","",TH_GY,[2,2,2,0,2,2,1],"SGK bài tập cuối chương: làm chung 1 giờ 12 phút, lớp 9 nhanh hơn 1 giờ ⇒ 5x² − 7x − 6 = 0 ⇒ 2 giờ và 3 giờ (thay luyện đề 5 — P5 SGK lên ≥ 20%, Thầy 16/11)."),
("P5","BTVN","C6-07","TH",1,2,"TH lẻ LT","ck2-nguyen-du-2025-III3","",TH_GY,[2,2,1,0,1,2,1],"Đề CK2: x₂² − mx₂ = x₁(m − x₁) ⇒ x₁² + x₂² = m(x₁ + x₂) ⇒ m = −11/2."),
("P5","BTVN","C6-08","TH",1,2,"TH lẻ LT","v10-luyen-de-23-2025-III3","",TH_GY,[2,1,1,0,2,2,0],"Luyện đề: nghiệm 3 − √6, tổng nghịch đảo bình phương."),
("P5","BTVN","C6-01","TH",1,2,"TH lẻ LT","gk1-ngo-sy-lien-2024-I1a","",TH_GY,[2,1,1,0,2,2,2],"Đề GK1: 2x(x + 3) − x² + 9 = 0 ⇒ (x + 3)² = 0."),
("P5","BTVN","C6-06","TH",1,2,"TH lẻ LT","v10-thinh-quang-2025-III3","",TH_GY,[2,1,1,0,2,2,1],"Đề minh họa Vào 10 (Thịnh Quang): 2(x − 1)² = −2x + a có nghiệm (1 + √7)/2 ⇒ 2x² − 2x + 2 − a = 0, x₁ + x₂ = 1 ⇒ nghiệm còn lại (1 − √7)/2 (thay Nguyễn Trường Tộ C6-17, 17/11). NB tách: đưa về dạng chuẩn; tổng hai nghiệm."),
# --- Đề kiểm tra chương 90′ (đề xuất câu; ma trận làm ở phiên P5) ---
# 17/11 phiên P5: Phần I trắc nghiệm 4 câu NB lấy từ tab (không tự đặt số)
("P5","KT chương","C6-01","NB",0,1,"NB lẻ LT","tl-ptb2-01-tr1","a-d",TN,[2,1,1,0,1,2,1],"Trắc nghiệm: phương trình nào KHÔNG phải phương trình bậc hai (4x − 7 = 0) — giữ nguyên bốn phương trình của đề."),
("P5","KT chương","C6-07","NB",0,1,"NB lẻ LT","tl-viete-15-tr3","",TN,[2,1,1,0,1,2,1],"Trắc nghiệm: 4x² − 5x − 3 = 0 (ac < 0), tổng 5/4, tích −3/4 — chỉ phần tổng, tích của đề (Đoàn Thị Điểm 2025-2 cùng nhóm trùng với Cổ Đông III2 đã bốc)."),
("P5","KT chương","C6-01","NB",0,1,"NB lẻ LT","tl-ptb2-03-tr4","d",TN,[2,1,1,0,1,2,1],"Trắc nghiệm: số nghiệm của −2x² + 5x − 4 = 0 (Δ = −7 < 0, vô nghiệm)."),
# 17/11 đổi từ gk2-mai-dich-2024-31 (trùng nguyên PT 2x² − 9x + 7 = 0 với sgk-6.24 ở P1) sang tl-viete-02-tr1
("P5","KT chương","C6-03","NB",0,1,"NB lẻ LT","tl-viete-02-tr1","a",TN,[2,1,1,0,1,2,1],"Trắc nghiệm: nhẩm nghiệm x² − 9x + 8 = 0 (a + b + c = 0 ⇒ 1 và 8)."),
("P5","KT chương","C6-01","NB",0,2,"NB lẻ LT","gk2-co-dong-2024-III1","",TLN,[2,1,1,0,1,2,2],"Câu giải PT cơ bản x² − 3x + 2 = 0."),
("P5","KT chương","C6-01","NB",0,1,"NB lẻ LT","gk2-ban-mai-2024-6a","",TH_GY,[2,1,1,0,1,2,2],"2x² + 5x + 3 = 0."),
("P5","KT chương","C6-07","TH",1,0,"TH lẻ LT","ck2-lomonoxop-2025-III3","",TH_GY,[2,1,1,0,1,2,1],"Đề CK2: 4x² + 8x − 15, M = x₁² + x₂² − 5x₁x₂."),
("P5","KT chương","C6-08","TH",1,0,"TH lẻ LT","ck2-phuc-dong-2024-901-III2","",TH_GY,[2,2,1,0,2,2,0],"Đề CK2: nghiệm (3 + √21)/2, bình phương hiệu hai nghiệm."),
("P5","KT chương","C6-11","VD",1,0,"VD lẻ","gk2-ba-dinh-2025-III2","a-b",VD_DE,[2,2,1,2,2,2,2],"Đề GK2: a giải m = 0, b 3/(x₁x₂) − x₁ − x₂ = 2 ⇒ m = 7/4."),
("P5","KT chương","C6-05","TH",1,0,"TH lẻ LT","v10-nguyen-tat-thanh-2025-cau8","1",TH_GY,[2,2,1,0,2,2,1],"Đề tham khảo Vào 10 (Nguyễn Tất Thành): Δ = (m + 1)² − 4(2m − 2) = (m − 3)² ≥ 0 ⇒ luôn có hai nghiệm. Chỉ ý 1 (ý 2 √x₁ < x₂² là VDC). Thay Long Biên C6-17 (17/11)."),
# 17/11 phiên P5: bỏ Chương Dương (60/x − 60/(x + 10) = 1/2 ⇒ x² + 10x − 1200 = 0, trùng phương trình Bài 1 Phiếu 4)
("P5","KT chương","C6-18","TH",1,0,"TH lẻ LT","ck2-hai-ba-trung-2024-III1","",TH_GY,[2,1,2,0,2,2,2],"Đề CK2: 300 sản phẩm, thêm 5/giờ."),
("P5","KT chương","C6-18","VD",1,0,"VD lẻ","v10-tho-loc-l4-2026-III1","",VD_DE,[2,2,2,1,2,2,2],"Thi thử Vào 10: 40 tấn, thêm 14 tấn, thêm 2 xe, mỗi xe thêm 0,5 tấn."),
]

# Bài gốc trùng đề (cùng PT/cùng bài, mã khác) — bốc một thì cái kia phải nằm ngoài
TRUNG = [
    {"ck2-phuc-dong-2025-III2","gk2-le-ngoc-han-2025-III2","tl-viete-41-tr7","v10-luyen-de-18-2025-III3"},
    {"v10-my-dinh-2-2026-III3","v10-ung-hoa-lan3-2025-III3"},
    {"ck2-nghia-tan-2025-III2","v10-luyen-de-21-2025-III3"},
    {"gk2-le-ngoc-han-2025-III1","gk2-phan-dinh-giot-2024-31"},
    {"v10-dong-da-de18-2025-III3","tl-viete-11-tr3"},
    {"ck2-hoai-duc-2024-III2","tl-viete-34-tr5"},
    {"ck2-ha-dong-2024-III2","tl-viete-19-tr4"},
    {"v10-be-van-dan-2025-III3","tl-viete-25-tr4"},
    {"so-hn-minhhoa-III3","tl-viete-50-tr9"},
    {"v10-tho-loc-l3-2025-III3","tl-viete-51-tr9"},
    {"ck2-lomonoxop-2025-III2","v10-luyen-de-23-2025-III2"},
    {"gk2-phan-dinh-giot-2024-2","sgk-b19-lt6"},
    {"gk2-mai-dich-2024-31","sgk-b19-lt6"},
    {"sgk-6.24","gk2-mai-dich-2024-31"},
    {"ck2-chu-van-an-dn-2025-2","tl-viete-14-tr3"},
    {"v10-huy-van-2024-III3","tl-viete-09-tr3"},
    {"v10-ly-thuong-kiet-2025-III3","tl-viete-10-tr3"},
    {"v10-phuong-mai-2025-III3","tl-viete-26-tr4"},
    {"gk2-co-dong-2024-III2","ck2-doan-thi-diem-2025-2"},
    {"ck2-gia-lam-2024-III2","v10-cat-linh-2025-III3"},
    {"sgk-b19-vdg1","sgk-b19-hd1"},
    {"ck1-ngoc-lam-2025-I3","ck1-ngoc-lam-2025-I3-md2"},
    {"so-hn-minhhoa-III2","gk1-ngoc-thuy-2025-III"},
    {"gk1-chu-van-an-2024-1b","gk1-nguyen-huy-tuong-2025-1b"},
    {"ck2-lomonoxop-2024-III1","gk1-ly-nam-de-2024-III"},
    # 17/11 (Phiếu 4): làm chung cùng số liệu 4 giờ – chênh 6 giờ ⇒ chỉ bốc một bài
    {"ck1-cau-dien-2025-3b","ck2-mai-dich-2025-3-2","ck2-chu-van-an-2024-III2","tl-lpt-51-tr11"},
    # 3 cặp trùng nguyên văn bank_gate kêu (Thầy 16/11 "bốc lại": không bốc bản nào; bản phái sinh ghi Bỏ)
    {"sgk-6.33","tl-lpt-41-tr9"},
    {"sgk-6.29","tl-lpt-03-tr2"},
    {"gk1-chu-van-an-2024-1b","gk1-nguyen-huy-tuong-2025-1b"},
]
# Thầy 16/11: hai bản của mỗi cặp trùng trên đều không bốc
KHONG_BOC = {"sgk-6.33", "tl-lpt-41-tr9", "sgk-6.29", "tl-lpt-03-tr2",
             "gk1-chu-van-an-2024-1b", "gk1-nguyen-huy-tuong-2025-1b"}


def _bank():
    b = {r["ma"]: {"de": r["de"], "nguon": r["nguon"], "uu": r["uu"]}
         for r in json.load(open(f"{GOC}.json"))["rows"]}
    for r in json.load(open(f"{GOC}/bank-them-tab-ngan-hang.json")):
        r = r + [""] * 13
        b.setdefault(r[12], {"de": r[0], "nguon": r[1], "uu": r[4]})
    return b


def loai_nguon(uu, ma):
    if ma.startswith("sgk-"):
        return "SGK"
    if "luyen-de" in ma:          # đề luyện thi Mathtech: tài liệu, không phải đề chính thức
        return "Sách tham khảo"
    if uu.startswith("Ưu tiên 1"):
        return "Đề thi"
    return "Sách tham khảo"


def phut(vai, muc, n, nb):
    if vai in ("Làm thêm", "KT chương", "Dự phòng"):
        return 0.0
    r = RATE[vai]
    if vai == "Ví dụ":
        return r["NB"] * nb if muc == "NB" else r[muc] * n
    return r["NB"] * nb + (r[muc] * n if muc != "NB" else 0)


def dung():
    bank = _bank()
    out, loi = [], []
    for (p, vai, dang, muc, n, nb, loai, ma, y, ht, T, ly) in R:
        if ma not in bank:
            loi.append(f"thiếu mã trong ngân hàng: {ma}")
            continue
        q = bank[ma]
        T8 = list(T) + [0]
        diem = round(sum(t * w for t, w in zip(T8, W)) / (2 * sum(W)) * 10, 1)
        ng = NGUONG[muc]
        out.append({
            "phieu": p, "vai": vai, "dang": dang, "muc": muc, "so_y": n, "so_nb": nb,
            "phut": round(phut(vai, muc, n, nb), 1), "loai": loai, "ma": ma, "y": y,
            "hinh_thuc": ht, "de": q["de"], "nguon": q["nguon"],
            "loai_nguon": loai_nguon(q["uu"], ma), "T": T8, "diem": diem, "nguong": ng,
            "ket_luan": ("Làm thêm" if vai == "Làm thêm" else ("Đạt" if diem >= ng else "Dưới ngưỡng")), "ly_do": ly,
        })
    # mỗi bài gốc chỉ bốc một dòng
    dem = collections.Counter(r["ma"] for r in out)
    loi += [f"bốc hai lần: {m}" for m, k in dem.items() if k > 1]
    chon = set(dem)
    loi += [f"bốc câu Thầy cấm (cặp trùng): {m}" for m in sorted(chon & KHONG_BOC)]
    for nhom in TRUNG:
        g = nhom & chon
        if len(g) > 1:
            loi.append(f"trùng đề: {sorted(g)}")
    return out, loi


def bao_cao(out):
    print(f"{'Phiếu':5} {'Vai':10} {'NB':>4} {'TH':>4} {'VD':>4} {'phút':>6}")
    for p in PHIEU:
        for vai in ("Ví dụ", "Trên lớp", "BTVN", "Làm thêm", "KT chương"):
            rs = [r for r in out if r["phieu"] == p and r["vai"] == vai]
            if not rs:
                continue
            nb = sum(r["so_nb"] for r in rs if vai != "Ví dụ" or r["muc"] == "NB")
            th = sum(r["so_y"] for r in rs if r["muc"] == "TH")
            vd = sum(r["so_y"] for r in rs if r["muc"] == "VD")
            ph = sum(r["phut"] for r in rs)
            print(f"{p:5} {vai:10} {nb:4} {th:4} {vd:4} {ph:6.1f}")
        tl = [r for r in out if r["phieu"] == p and r["vai"] == "Trên lớp"]
        if tl:
            src = collections.Counter(r["loai_nguon"] for r in tl)
            tong = sum(src.values())
            print("      nguồn trên lớp (bài gốc): " +
                  ", ".join(f"{k} {v}/{tong} = {round(100*v/tong)}%" for k, v in src.items()))
    duoi = [r for r in out if r["ket_luan"] == "Dưới ngưỡng"]
    print("Dưới ngưỡng:", [(r["phieu"], r["ma"], r["diem"]) for r in duoi])


if __name__ == "__main__":
    out, loi = dung()
    bao_cao(out)
    if loi:
        print("LỖI:\n  " + "\n  ".join(loi))
        sys.exit(1)
    if "--ghi" in sys.argv:
        json.dump(out, open(f"{GOC}/chon-cau.json", "w"), ensure_ascii=False, indent=1)
        print(f"Đã ghi {GOC}/chon-cau.json ({len(out)} dòng)")
