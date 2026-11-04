# Bốc + chấm câu chương V 9C (quy trình 03/11/2026). Chạy: python3 chon.py <repo>
# Mỗi dòng: (phiếu, vai trò, loại §4b, mã, dòng ý, mức, hình thức, [T1..T8], loại ngay, lí do)
import json, re, sys

W = [3, 1, 2, 1, 2, 2, 2, 0]  # lớp C
TL = "Tự luận trình bày (HS tự vẽ hình)"
DK = "Điền khuyết (hình in sẵn)"
TN = "Trắc nghiệm A–D"
DS = "Đúng/Sai (4 ý, hình in sẵn)"
TLN = "Trả lời ngắn"

R = [
# ---------------- P1 (đã duyệt 22/10 — giữ nguyên) ----------------
("P1","Trên lớp + Ví dụ + BTVN","VD lẻ","ck1-ai-mo-1","","VD","Trả lời ngắn có hình",[2,2,2,1,2,2,2,0],"","GIỮ (đã duyệt). Bò buộc ở góc vườn: một phần tư hình tròn r = 1,5 m rồi lấy phần còn lại ≈ 23,23 m² — thực tế, hai bước, bẫy lấy cả hình tròn."),
("P1","Trên lớp","TH tách VD","ck1-trung-vuong-III","1-2","TH","Trả lời ngắn có hình",[2,2,2,1,2,2,2,0],"","GIỮ (đã duyệt). Con lắc 60 cm, 30°: tính cung rồi bài toán ngược (339,12 cm ⇒ lệch bao nhiêu độ) — ý toán thật, không thay số máy móc."),
("P1","Trên lớp","TH ghép bài","ck1-cau-dien-41","a-b","TH","Điền khuyết",[2,1,2,1,2,2,2,0],"","GIỮ (đã duyệt). Khăn d = 160, bàn d = 108: a đổi ra bán kính (bẫy dùng đường kính) → b vành khuyên."),
("P1","Trên lớp","TH ghép bài","ck1-tan-trieu-41","","TH","Trả lời ngắn",[2,1,2,0,2,2,2,0],"","GIỮ (đã duyệt). Hồ R = 50 m, lối đi rộng 5 m: vành khuyên R = 55, r = 50 (bẫy lấy R = 5)."),
("P1","Trên lớp","TH lẻ LT","ck1-chu-van-an-IV1","a-b","TH","Trả lời ngắn có hình",[2,1,2,1,2,2,2,0],"","GIỮ (đã duyệt). Quạt giấy nửa hình tròn 2,2 dm; phần giấy là vành khuyên của quạt (2,2 và 0,6 dm) — bẫy lấy cả quạt."),
("P1","Trên lớp","TH lẻ LT","ck1-dich-vong-41","a-b","TH","Trả lời ngắn",[2,1,2,1,1,2,2,0],"","GIỮ (đã duyệt). Pizza d = 20 cm cắt 8 miếng: quạt 45°, rồi đổi ra gam sốt — gần gũi."),
("P1","Trên lớp","NB tách TH","ck1-ngoc-lam-IV1","a-b","TH","Điền khuyết",[2,1,2,1,2,2,2,0],"","GIỮ (đã duyệt). Mặt bàn d = 150 cm, khăn rủ 20 cm: a NB diện tích hình tròn, b vành khuyên."),
("P1","Trên lớp","NB ghép bài","ck1-phuc-dong-IV1","","NB","Trả lời ngắn",[2,0,2,0,1,2,2,0],"","GIỮ (đã duyệt). Đĩa CD r = 1,5 và 6 cm: một bước công thức vành khuyên."),
("P1","Trên lớp","NB tách TH","ck1-ly-thanh-tong-5","a-b","NB","Trả lời ngắn có hình",[2,0,1,1,1,2,2,0],"","GIỮ (đã duyệt). Quạt r = 2 dm, 150°: thay vào hai công thức diện tích quạt và độ dài cung."),
("P1","BTVN","NB kiến thức cũ","sgk-5.1","","NB","Trắc nghiệm A–D",[1,0,1,0,1,2,1,0],"","GIỮ (đã duyệt). Vị trí điểm so với (O; √5) — điểm sát ngưỡng 5 vì T1 chỉ phục vụ nền; Thầy muốn thay thì lấy stk-b13-I-C7-tr5."),

# ---------------- P2: bốn điểm + chứng minh tiếp tuyến ----------------
("P2","Trên lớp","VD lẻ","ck1-chuong-my-2024-4.2","a-b-c","VD",TL,[2,1,1,2,2,2,2,0],"","Đề CK1 Chương Mỹ: a bốn điểm A, E, H, D tâm O (đúng khuôn Câu IV.2a, 38/46 đề) → b AD·AB = AE·AC bằng hệ thức lượng (ôn ch.IV) → c IE là tiếp tuyến: cộng hai góc của hai tam giác cân — đỉnh VD vừa sức lớp C, ba ý nối nhau."),
("P2","Ví dụ","VD lẻ","ck1-ai-mo-2","a-b","VD",DK,[2,2,1,2,2,2,2,0],"","Đề CK1 Ái Mộ 2025–2026: b DF tiếp tuyến vì AB là trung trực của CD ⇒ ΔOCF = ΔODF — mẫu 'tiếp tuyến = góc 90° chuyển qua hai tam giác bằng nhau'. Cấu hình khác bài trên lớp. Ý c VDC bỏ."),
("P2","BTVN","VD lẻ","ck1-hoai-duc-2024-4.2","a-b-c","VD",TL,[2,1,1,2,2,2,2,0],"","Gương của bài trên lớp: a bốn điểm B, E, D, C tâm I → c OE là tiếp tuyến của (I), cùng nếp cộng góc nhưng hình hai đường cao. Ý b (đồng dạng) là bước nền cho buổi 4."),
("P2","Trên lớp","TH ghép bài","ck1-hoang-liet-2025-4.2","a","TH",TL,[2,1,1,0,2,2,2,0],"","Bốn điểm A, M, O, B: một góc vuông do d ⊥ OA, một góc vuông do tiếp tuyến ⊥ bán kính — luyện đúng câu 'xét hai tam giác vuông chung cạnh huyền OM'. Sinh NB tách: '∠OBM = 90° vì …'."),
("P2","Trên lớp","TH ghép bài","gk1-trung-vuong-2025-IV","1","TH",TL,[2,1,1,0,1,2,2,0],"","Cấu hình khác hẳn (tam giác vuông + hai hình chiếu), tâm là trung điểm AH — để HS không học thuộc một hình. Ý 2–3 là ch.IV, không lấy."),
("P2","Trên lớp","TH lẻ LT","sgk-b16-vd1","","TH","Tự luận ngắn có khung điền",[2,2,1,0,2,2,1,0],"","Ví dụ 1 SGK Bài 16: OC ⊥ AB ⇒ OC là trung trực AB ⇒ ΔOAC = ΔOBC ⇒ ∠OBC = 90°. Khuôn gốc của mọi ý 'chứng minh tiếp tuyến'."),
("P2","Trên lớp","TH tách VD","v10-dong-da-de04-IV2","a-b","TH",TL,[2,1,1,1,2,2,2,0],"","a DO ⊥ BC qua tam giác OBC cân (không cần định lí dây), ΔABC vuông → b DC là tiếp tuyến — a dẫn thẳng vào b. Ý c thẳng hàng bỏ."),
("P2","Ví dụ","TH ghép bài","ck1-tan-trieu-42","a-b","TH",DK,[2,1,1,1,2,2,2,0],"","Mẫu cho cả hai dạng của buổi trên một hình: a bốn điểm O, A, C, M; b OH = ½AM (đường trung bình) và BD là tiếp tuyến. Trùng đề HBT 2024 (đã gạt)."),
("P2","Ví dụ","TH lẻ LT","sgk-5.21","","TH",DK,[2,2,1,0,1,2,1,0],"","SGK: tam giác cân nội tiếp ⇒ OA ⊥ BC ⇒ đường qua A song song BC là tiếp tuyến. Cấu hình khác Ví dụ 1."),
("P2","BTVN","TH ghép bài","gk1-luong-the-vinh-2025-4.2","a","TH",TL,[2,1,1,0,1,2,2,0],"","Gương bài 'hai hình chiếu' (A, E, D, F), thêm yêu cầu chỉ rõ tâm, bán kính."),
("P2","BTVN","TH ghép bài","ck1-chu-van-an-2024-IV2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"","a giải tam giác vuông (ôn ch.IV) → b DB là tiếp tuyến: gương của Ví dụ 1 SGK. Ý c bỏ."),
("P2","Dự phòng","TH ghép bài","v10-dong-da-de08-IV2","a","TH",TL,[2,1,1,0,1,2,2,0],"","Bốn điểm B, K, H, N (hai đường cao) — cùng nếp bài Trưng Vương; ý b, c có góc nội tiếp (ch.IX)."),
("P2","Dự phòng","TH lẻ LT","sgk-5.22","","TH",TL,[2,1,1,0,1,2,1,0],"","SGK: OA, OB là hai tiếp tuyến của (M; MA) — hay nhưng lời giải dài, để dự phòng."),
("P2","Ví dụ","NB kiến thức cũ","sgk-b13-lt1","","NB",DK,[2,1,1,0,1,2,2,0],"","Nền lớp 8: trung tuyến ứng với cạnh huyền bằng nửa cạnh huyền ⇒ A thuộc đường tròn đường kính BC — viên gạch của mọi ý a."),
("P2","Trên lớp","NB kiến thức cũ","tl-1-21","","NB",TN,[2,1,1,0,2,2,1,0],"","Pythagore 3–4–5 rồi R = BC : 2; phương án 5 cm bẫy HS quên chia đôi."),
("P2","Trên lớp","NB lẻ LT","stk-b13-I-C17-tr8","","NB",TN,[2,0,1,0,2,2,1,0],"","Ba phương án đặt đường kính sai cạnh — bẫy chọn nhầm cạnh huyền."),
("P2","Trên lớp","NB lẻ LT","tl-1-19","","NB",TN,[2,1,1,0,2,2,2,0],"","Hai đường cao BD, CE ⇒ B, E, D, C cùng thuộc một đường tròn; phương án 'năm điểm kể cả A' là bẫy. Đúng nếp ý a đề thi."),
("P2","BTVN","NB lẻ LT","stk-b13-III-C33-tr13","","NB",TLN,[2,0,1,0,1,2,2,0],"","BC = 2026 mm ⇒ R = 1013 mm; gương của câu trên (hai đường cao)."),
("P2","BTVN","NB lẻ LT","stk-b13-I-C7-tr5","","NB",TN,[2,0,1,0,1,2,1,0],"","Vị trí điểm theo OM so với R; OD = R là bẫy (điểm trên, không phải trong)."),
("P2","BTVN","NB lẻ LT","tl-3b-7","","NB","Điền bảng",[2,0,1,0,1,2,1,0],"","Bảng d – R năm dòng: một câu ôn trọn ba vị trí tương đối, trực quan."),
("P2","Trên lớp","NB lẻ LT","sgk-5.20","","NB","Trắc nghiệm / điền bảng",[2,1,2,0,1,2,1,0],"","Thực tế: dán bốn hình tròn r = 4, 6, 7, 8 cm, tâm trên b, a cách b 6 cm — so d với R."),
("P2","Trên lớp","NB lẻ LT","stk-b16-I-C4-tr232","","NB",TN,[2,0,1,0,2,2,2,0],"","Tiếp tuyến ⊥ bán kính TẠI TIẾP ĐIỂM; phương án 'tại O' đúng lỗi HS hay viết. (Đã soi ảnh tr.232: phương án B là d ≡ OA.)"),
("P2","Trên lớp","NB lẻ LT","sgk-5.35","","NB",TN,[2,0,1,0,1,2,1,0],"","SGK: (O) cắt a₁, tiếp xúc a₂ ⇒ d₁ < R, d₂ = R."),
("P2","Trên lớp","NB lẻ LT","sgk-b16-lt1","a-b-c","NB",TN,[2,0,1,0,1,2,1,0],"","SGK: d = 4 cm với R = 3, 5, 4 cm — đổi thành trắc nghiệm ba ý."),
("P2","BTVN","NB kiến thức cũ","stk-b16-I-C17-tr234","","NB",TN,[2,1,1,0,1,2,1,0],"","Tiếp tuyến ⊥ bán kính rồi Pythagore 3–4–5 ⇒ AB = 4 cm."),
("P2","Trên lớp","NB ghép bài","ck1-ly-son-2025-IV2","a","NB",DK,[2,1,1,0,2,2,2,0],"","Đề CK1, hình in sẵn: HS điền '∠MAO = 90° vì Ax là tiếp tuyến', '∠MCO = 90° vì …', 'tâm là trung điểm của MO' — ý a chia thành ba ô."),
("P2","Dự phòng","NB lẻ LT","stk-b16-I-C26-tr237","","NB",TN,[2,1,1,0,1,2,1,0],"","HK là tiếp tuyến của đường tròn đường kính AI: sách xếp NB nhưng thực chất là TH — để BTVN nâng cao nếu cần."),
("P2","Loại","VD lẻ","ck1-hat-mon-2025-IV2","a-b","VD",TL,[2,2,1,2,2,2,2,0],"L5","Trùng đề Ái Mộ 2025 Bài 4.2 (đã dùng làm Ví dụ)."),
("P2","Loại","NB lẻ LT","stk-b13-I-C19-tr8","","NB",TN,[2,0,1,0,1,2,1,0],"L3","Phương án C mất số (R = 6,5 cm) khi trích chữ — muốn dùng phải soi ảnh tr.8."),

# ---------------- P3: hai tiếp tuyến cắt nhau ----------------
("P3","Trên lớp","VD lẻ","ck1-phuc-dong-IV2","a-b-c","VD",TL,[2,2,1,2,2,2,2,0],"","Đề CK1 Phúc Đồng: a bốn điểm → b OA ⊥ BC và OA ∥ CD (đúng dạng IV.2b) → c OA = 2R ⇒ ∠BOC = 120°, ∠COD = 60° ⇒ S quạt = πR²/6: nối Bài 15, trọn vẹn, vừa sức C."),
("P3","Ví dụ","VD lẻ","ck1-ban-mai-2024-3","a-b-c","VD",DK,[2,2,1,2,1,2,2,0],"","c OAHB là hình thoi (AC ∥ OB, BD ∥ OA, OA = OB) — chứng minh bằng kiến thức lớp 8, đẹp; b OI·OM = R² làm cầu sang buổi 4."),
("P3","BTVN","VD lẻ","ck1-ngo-si-lien-2024-7","a-b-c","VD",TL,[2,2,1,2,2,2,2,0],"","b MB ⊥ OD và MB ∥ OC (nhịp trung trực) đúng dạng buổi; c BK là phân giác ∠MBD: cộng góc trong tam giác cân OBK, vừa sức. Ý d (giả sử hình thoi) bỏ."),
("P3","Trên lớp","TH tách VD","ck1-dong-da-2025-IV2","a-b","TH",TL,[2,1,1,1,2,2,2,0],"","Nửa đường tròn, tiếp tuyến tại A và tại M: OP ⊥ AM, OP ∥ MB — cùng dạng bài VD nhưng khác cấu hình. Ý c (VDC thật) bỏ."),
("P3","Trên lớp","TH lẻ LT","sgk-5.23","a","TH","Tự luận ngắn / điền",[2,2,1,0,2,2,1,0],"","Chu vi ΔSEF = SA + SB: áp hai lần tính chất hai tiếp tuyến — ý toán gọn, đẹp."),
("P3","Trên lớp","TH ghép bài","ck1-phuc-tho-2024-5","a-b","TH",DK,[2,1,1,1,1,2,2,0],"","OI = 2R ⇒ sin∠OIA = ½ ⇒ ∠OIA = 30°, ΔIAB đều — tính góc trên hình hai tiếp tuyến, trực quan. Ý c bỏ."),
("P3","Ví dụ","TH lẻ LT","sgk-b16-hd4","a-b-c","TH",DK,[2,1,1,1,1,2,2,0],"","Hình thành định lí hai tiếp tuyến cắt nhau bằng ΔOMA = ΔOMB (SGK HĐ4)."),
("P3","Ví dụ","TH lẻ LT","sgk-b16-vd2","a-b","TH",DK,[2,1,1,1,1,2,2,0],"","Ví dụ 2 SGK: OM ⊥ AB (qua trung trực) và tính MA = 2√3 cm — mẫu chứng minh vuông góc."),
("P3","BTVN","TH tách VD","ck1-lomonoxop-2024-IV2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"","Gương bài Đống Đa: KO là trung trực MI ⇒ KO ∥ NI."),
("P3","BTVN","TH tách VD","ck1-ngoc-lam-IV2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"","Gương 1–1 của bài VD trên lớp (SO ⊥ AB, AD ∥ SO). Trên lớp thì trùng (L5) nên chỉ để BTVN. Ý c bỏ."),
("P3","Trên lớp","NB kiến thức cũ","stk-b13-I-C13-tr6","","NB",TN,[2,0,1,0,1,2,1,0],"","Ôn đường trung trực (lớp 7): O cách đều A, B ⇒ O thuộc trung trực AB — nền của 'OA là trung trực BC'."),
("P3","Trên lớp","NB lẻ LT","stk-b16-I-C7-tr232","","NB",TN,[2,0,1,0,2,2,1,0],"","Chọn khẳng định sai: lẫn 'góc tạo bởi hai bán kính' với 'góc tạo bởi hai tiếp tuyến' — đúng chỗ HS hay nhầm."),
("P3","BTVN","NB lẻ LT","stk-b16-I-C8-tr232","","NB",TN,[2,0,1,0,2,2,1,0],"","Gương của câu trên dạng điền cụm từ."),
("P3","Trên lớp","NB lẻ LT","stk-b16-I-C19-tr235","","NB",TN,[2,1,1,0,2,2,1,0],"","∠AMB = 50° ⇒ ∠AMO = 25°, ∠MOB = 65°; các phương án đảo cặp số."),
("P3","Trên lớp","NB lẻ LT","stk-b16-III-C60-tr252","","NB",TLN,[2,1,1,0,1,2,1,0],"","∠CND = 40° ⇒ sđ cung nhỏ CD = 140°: nối với số đo cung (buổi 1)."),
("P3","BTVN","NB lẻ LT","stk-b16-III-C58-tr252","","NB",TLN,[2,1,1,0,1,2,1,0],"","∠CND = 60° ⇒ ∠DON = 60°."),
("P3","BTVN","NB kiến thức cũ","stk-b16-I-C21-tr235","","NB",TN,[2,1,1,0,1,2,1,0],"","OM = 2R ⇒ cos∠AOM = ½ ⇒ 60°, cung nhỏ AB = 120° — ôn tỉ số lượng giác, chuẩn bị ý c bài VD."),
("P3","Trên lớp","NB lẻ LT","stk-b16-II-C30-tr239","","NB",DS,[2,1,1,1,2,2,1,0],"","AM = AN (Đ), OA ⊥ MN (Đ), ∠AON > ∠MCO (S, bằng nhau vì MC ∥ OA), chu vi ΔAMN = 52/5 (S, đúng là 64/5) — bẫy tính MN = 2MH. Đã soi ảnh tr.239, chép lại mũ góc."),
("P3","Trên lớp","NB ghép bài","ck1-giang-vo-2025-IV2","a","NB",DK,[2,1,1,0,2,2,2,0],"","Đề CK1, hình in sẵn: điền AB = AC (hai tiếp tuyến), OB = OC ⇒ OA là trung trực BC — ý a chia thành ô trống."),
("P3","Loại","TH lẻ LT","stk-b16-II-C29-tr238","","TH",DS,[2,1,1,1,1,2,1,0],"L5","Cùng ý chu vi ΔSEF với SGK 5.23 (đã chọn trên lớp)."),
("P3","Loại","VD lẻ","ck1-dong-anh-2024-IV2","a-b","VD",TL,[2,1,1,1,1,2,2,0],"L5","Trùng đề Ngọc Thụy 2025 III.2 (dùng ở buổi 4)."),

# ---------------- P4: hệ thức tích bằng đồng dạng ----------------
("P4","Trên lớp","VD lẻ","ck1-nhat-tan-2024-4.2","1-2-3","VD",TL,[2,2,1,2,2,2,2,0],"","1 bốn điểm → 2 MA² = MH·MO (ΔMAH ∽ ΔMOA) → 3 MA² = MC·MD và ΔMBD ∽ ΔMCB (c.g.c): chuỗi tích bắc cầu qua MA² — đích của buổi, không ý nào quá tầm C."),
("P4","Ví dụ","VD lẻ","ck1-ngoc-thuy-III2","a-b","VD",DK,[2,2,1,1,2,2,2,0],"","AM·AN = AH·AO: giải được bằng đại số (AO − R)(AO + R) = AO² − R² = AB² — ý toán hay, khác cấu hình bài trên lớp (cát tuyến qua tâm). Ý c bỏ."),
("P4","BTVN","VD lẻ","ck1-ta-quang-buu-2025-IV2","a-b","VD",TL,[2,2,1,1,2,2,2,0],"","Gương ý 3 bài trên lớp: AB ⊥ OM và MH·MO = MC·MD (bắc cầu qua MA²). Ý c bỏ."),
("P4","Trên lớp","TH tách VD","ck1-ngo-gia-tu-2025-IV2","a-b","TH",TL,[2,1,1,1,2,2,2,0],"","OA ⊥ BC và OH·OA = R²: khuôn ý b phổ biến nhất (Ngô Gia Tự, Marie Curie, Phan Đình Giót, Giang Biên, phường Ba Đình… chọn 1 trên lớp). Ý c bỏ."),
("P4","Trên lớp","TH tách VD","ck1-thanh-tri-2024-IV2","a-b","TH",TL,[2,2,1,1,2,2,2,0],"","Nửa đường tròn: CE·CB = CA² (tam giác vuông + đường cao) rồi CD = CA ⇒ ΔCDE ∽ ΔCBD (c.g.c) — luyện chiều 'từ tích ra đồng dạng'."),
("P4","Trên lớp","TH tách VD","ck1-cau-giay-2024-IV2","a-b","TH",TL,[2,1,1,1,2,2,2,0],"","ΔOHC ∽ ΔABC (chung góc C) ⇒ CH·CA = CO·CB = 2R²: tiếp tuyến + đường kính, khác hình hai tiếp tuyến."),
("P4","Ví dụ","TH tách VD","ck1-cum-14-2025-4.2","a-b","TH",DK,[2,1,1,1,1,2,2,0],"","Ví dụ cho dạng OH·OA = R² trên hình nửa đường tròn (OH·OD = R²) kèm DB là tiếp tuyến — khác cấu hình bài Ngô Gia Tự."),
("P4","Ví dụ","TH tách VD","ck1-dich-vong-42","a-b","TH",DK,[2,1,1,1,1,2,2,0],"","ΔAKB vuông (K trên đường tròn đường kính AB) rồi BK·BC = AB² = 4R² — ví dụ cho bài Cầu Giấy."),
("P4","BTVN","TH tách VD","ck1-gia-lam-2024-4.2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"","Gương 1–1 bài Ngô Gia Tự (AB ⊥ OM, OA² = OH·OM)."),
("P4","BTVN","TH tách VD","ck1-nguyen-binh-khiem-2025-4.2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"","Gương bài Dịch Vọng: OD ⊥ AB và CA·CE = 4R²."),
("P4","Trên lớp","NB kiến thức cũ","stk-b16-II-C35-tr241","","NB",DS,[2,1,1,1,2,2,1,0],"","Hai tam giác vuông chung góc nhọn ⇒ đồng dạng (lớp 8): ΔOIC ∽ ΔOCE (Đ), OI·OE = 2R (S, đúng là R²), ∠ODE = 90° (Đ), ∠DOF = 180° (Đ). Đã soi ảnh tr.241."),
("P4","Trên lớp","NB lẻ LT","stk-b16-II-C33-tr240","","NB",DS,[2,2,1,1,2,2,1,0],"","AC = 6, AB = 8: BC = 10 (Đ), BM = 6 (S, bằng 4 vì CM = CA), ΔBMO ∽ ΔBAC (Đ), R = 4 (S, bằng 3) — gom tính chất hai tiếp tuyến, đồng dạng, Pythagore."),
("P4","BTVN","NB lẻ LT","stk-b16-II-C49-tr248","","NB",DS,[2,1,1,1,1,2,1,0],"","AC ⊥ MO, OH·OM = R², ΔODM ∽ ΔOHD… — chữ trích mất số mũ, chép lại theo ảnh tr.248 trước khi dùng."),
("P4","Trên lớp","NB ghép bài","ck1-ngoi-sao-2024-4.2","a-b","NB",DK,[2,1,1,0,2,2,2,0],"","Đề CK1, hình in sẵn: điền cặp góc bằng nhau để ra ΔDBC ∽ ΔBAH — đúng chỗ HS hay viết sai thứ tự đỉnh."),
("P4","BTVN","NB ghép bài","ck1-marie-curie-2025-4","a-b","NB",DK,[2,1,1,0,1,2,2,0],"","Cùng khuôn Ngô Gia Tự (trên lớp thì L5) — chỉ để BTVN điền khuyết."),
("P4","Loại","TH tách VD","ck1-ha-dong-2024-4.2","a-b","TH",TL,[2,1,1,1,1,2,2,0],"L5","Gần trùng đề Ngô Gia Tự 2025 (đã chọn)."),
("P4","Loại","TH tách VD","ck1-nguyen-du-2025-4.2","a-b","TH",TL,[1,1,1,1,1,2,2,0],"L4","FC² = FB·FA cần góc tạo bởi tia tiếp tuyến và dây (ch.IX)."),

# ---------------- P5: luyện tập chung — ba tiếp tuyến + đo lường thực tế ----------------
("P5","Trên lớp","VD lẻ","ck1-ly-thanh-tong-7","a-b-c","VD",TL,[2,2,1,2,2,2,2,0],"","Gom cả chương trên một hình: DB ∥ OA, AB² = AH·AO (buổi 3–4), AC là tiếp tuyến (buổi 2), c diện tích giới hạn bởi hai tiếp tuyến và cung nhỏ = S(ABOC) − S quạt ≈ 17,1 cm² (buổi 1). Đề trường TP.HCM — ghi rõ nguồn."),
("P5","Ví dụ","VD lẻ","stk-b16-III-C56-tr251","","VD","Điền khuyết (thực tế)",[2,1,2,1,2,2,1,0],"","Tầm nhìn từ độ cao 5 m: AC = √(6400,005² − 6400²) ≈ 8 km — tiếp tuyến ⊥ bán kính + Pythagore, số đẹp; bẫy quên đổi 5 m ra km."),
("P5","BTVN","VD lẻ","stk-b16-III-C57-tr252","","VD",TLN,[2,1,2,1,2,2,1,0],"","Gương treo bằng hai dây tiếp xúc, tổng dây 6 dm, góc 60° ⇒ R = 3·tan30° ≈ 1,73 dm — bài ngược của bài gương trên lớp."),
("P5","Dự phòng","VD lẻ","ck1-marie-curie-2025-5.2","","VD","Trả lời ngắn",[2,1,2,1,1,1,1,0],"","Vệ tinh địa tĩnh: cùng dạng tầm nhìn nhưng số 5 chữ số (42186² − 6400²), dưới ngưỡng VD vì T6."),
("P5","Trên lớp","TH tách VD","ck1-cau-dien-42","a-b","TH",TL,[2,2,1,1,2,2,2,0],"","Ba tiếp tuyến: CD = AC + BD (định lí hai tiếp tuyến hai lần) → OC ∥ MB, ME·MB = AH·AB (cùng bằng AM², hai lần hệ thức lượng). Ý c (phân giác) bỏ."),
("P5","Trên lớp","TH lẻ LT","ck1-phuong-ba-dinh-2025-IV1","","TH","Trả lời ngắn có hình",[2,1,2,0,2,2,2,0],"","Thực tế: treo gương bằng hai dây tiếp xúc viền, OA = 25 cm, ∠AMO = 30° ⇒ MA = 25√3 ≈ 43 cm — tiếp tuyến ⊥ bán kính + tỉ số lượng giác, rất trực quan."),
("P5","Trên lớp","TH ghép bài","gk2-nam-tu-liem-2025-IV1","a-b","TH","Trả lời ngắn có hình",[2,1,2,1,2,2,2,0],"","Câu IV.1: bồn cây R = 15 m, quạt 120° — hàng rào = cung + hai bán kính (bẫy quên hai bán kính), diện tích lát gạch = phần còn lại."),
("P5","Ví dụ","TH tách VD","sgk-5.30","a-b","TH",DK,[2,1,1,1,1,2,2,0],"","SGK: MN = MA + NB; Q là trung điểm MN — cùng dạng ba tiếp tuyến, câu b khác bài trên lớp."),
("P5","BTVN","TH tách VD","ck1-marie-curie-2024-4","a-b","TH",TL,[2,2,1,1,1,2,2,0],"","AC + BD = CD và OC·OD/CD = R (hai cách tính diện tích ΔCOD) — gương bài Cầu Diễn, có ý toán."),
("P5","BTVN","TH ghép bài","v10-tho-loc-3-2025-IV1","a-b","TH","Trả lời ngắn có hình",[2,1,2,1,1,2,1,0],"","Công viên hình quạt 50 m, 72°: hàng rào + 30% diện tích — gương bài bồn cây."),
("P5","Trên lớp","NB kiến thức cũ","stk-b16-II-C31-tr239","","NB",DS,[2,1,1,1,2,2,1,0],"","Hai tia phân giác của hai góc kề bù vuông góc (lớp 7): ∠AOM = ∠COM (Đ), ∠MON = 80° (S, = 90°), MN = AM + BN (Đ), AM·BN = √2025 (S, = R² = 2025). Đã soi ảnh tr.239."),
("P5","BTVN","NB lẻ LT","stk-b16-II-C50-tr249","","NB",DS,[2,1,1,1,2,2,1,0],"","∠COD = 90° (Đ), MC·MD = 2OM² (S), BD = √3R, AC = √3R/3 (Đ), MC·MD = 20 (S, = 25). Chữ trích mất công thức — chép lại theo ảnh tr.249 (ý thứ tư in nhầm nhãn 'c)')."),
("P5","Trên lớp","NB lẻ LT","ck1-ban-mai-2024-6a","","NB",TN,[2,0,1,0,1,2,2,0],"","Quạt r = 4 cm, 72°: một bước công thức — khởi động Câu IV.1."),
("P5","Trên lớp","NB lẻ LT","ck1-hai-ba-trung-2024-IV1","","NB","Trả lời ngắn có hình",[2,0,2,0,2,2,2,0],"","Con lắc 1,2 m, 60°: độ dài cung (bẫy dùng công thức diện tích quạt)."),
("P5","BTVN","NB lẻ LT","ck1-ngoi-sao-2024-4.1","","NB",TLN,[2,0,2,0,2,2,2,0],"","Đèn vành khuyên đường kính 90 và 60 cm ⇒ đổi ra bán kính (bẫy dùng đường kính)."),
("P5","Trên lớp","NB lẻ LT","stk-b16-I-C20-tr235","","NB",TN,[2,1,1,0,1,2,1,0],"","∠AMB = 50° ⇒ cung nhỏ AB = 130°, cung lớn 230° — nối hai tiếp tuyến với số đo cung."),
("P5","Trên lớp","NB ghép bài","ck1-quoc-oai-2024-4.2","a","NB",DK,[2,1,1,0,1,2,2,0],"","Đề CK1, hình nửa đường tròn in sẵn: điền hai góc vuông ⇒ bốn điểm A, O, M, C — ôn nhanh ý a trước bài ba tiếp tuyến."),
("P5","Loại","TH ghép bài","gk2-chuong-duong-2024-IV1","a-b","TH","Trả lời ngắn có hình",[2,1,2,1,2,2,2,0],"L5","Trùng đề Nam Từ Liêm 2025 IV.1 (đã chọn)."),

# ---------------- P6: bài tập cuối chương 45′ (+ kiểm tra 45′) ----------------
("P6","Trên lớp","VD lẻ","ck1-nguyen-truong-to-2025-IV","1-2-3","VD",DK,[2,1,1,2,1,2,2,0],"","Trọn một đề Câu IV.2 trong 45′: bốn điểm → OA ⊥ BC, OA·OH = R² → AM·AN = AH·AO. Ý 3 cùng nếp Ví dụ buổi 4 (Ngọc Thụy) — buổi ôn nên giữ; Thầy muốn khác thì đổi Xuân La. Ý 4 bỏ."),
("P6","BTVN","VD lẻ","ck1-xuan-la-2024-4.2","a-b","VD",TL,[2,2,1,1,2,2,2,0],"","OA ⊥ MN và AH·AO = AB·AC (bắc cầu qua AM²). Ý c (phân giác) bỏ."),
("P6","Trên lớp","TH ghép bài","gk1-thanh-quan-2024-IV","1-2","TH",TL,[2,1,1,1,1,2,2,0],"","Tam giác hai đường cao: bốn điểm B, E, D, C (tâm O trung điểm BC) và AB·AE = AC·AD. Ý 3 dài, bỏ."),
("P6","Trên lớp","TH ghép bài","v10-chuong-my-l4-2025-IV1","a-b","TH","Trả lời ngắn có hình",[2,1,2,1,2,2,2,0],"","Câu IV.1: long đen AB = 1,8 cm, CD = 2,4 cm — diện tích lỗ và vành khuyên; thực tế cơ khí, bẫy dùng đường kính."),
("P6","BTVN","TH ghép bài","ck1-cum-14-2025-4.1","","TH",TLN,[2,1,2,0,2,2,2,0],"","Khăn trải bàn rủ 40 cm, bàn d = 120 cm ⇒ R khăn = 100 cm."),
("P6","Trên lớp","NB lẻ LT","sgk-5.32","","NB",TN,[2,0,1,0,1,2,1,0],"","SGK: OA = √15 < 4, OB = 4 ⇒ A trong, B trên."),
("P6","Trên lớp","NB lẻ LT","stk-b16-I-C9-tr232","","NB",TN,[2,0,1,0,1,2,1,0],"","R = 5, d = 4 ⇒ cắt nhau."),
("P6","Trên lớp","NB lẻ LT","sgk-5.33","","NB",TN,[2,1,1,0,2,2,1,0],"","SGK: BD đường kính, ∠AOB = 40°, ∠BOC = 100° ⇒ sđ cung DC, AD — ôn số đo cung."),
("P6","Trên lớp","NB lẻ LT","stk-b16-I-C25-tr237","","NB",TN,[2,1,1,0,1,2,1,0],"","IK ∥ OA ⇒ ∠KIO = ∠IOA = ∠IOK ⇒ KI = KO — vận dụng nhẹ tính chất hai tiếp tuyến."),
("P6","BTVN","NB lẻ LT","stk-b16-I-C18-tr234","","NB",TN,[2,1,1,0,1,2,1,0],"","R = 6, OA = 10 ⇒ AB = 8 cm."),
("P6","BTVN","NB lẻ LT","stk-b13-I-C20-tr8","","NB",TN,[2,0,1,0,1,2,1,0],"","Hình chữ nhật 12 × 5 ⇒ R = 6,5 cm."),
]

# ---- Sửa 03/11 lượt 2: bám đúng "Dạng VẬN DỤNG trong đề" của thuyết minh 26/10 ----
SUA = {
 # ma: (phieu, vai, loai, dong, muc, hinh_thuc, T, loai_ngay, ly_do)  — None = giữ nguyên
 "ck1-ai-mo-2": ("P2","Trên lớp","VD lẻ",None,"VD",TL,None,"","ĐÚNG BÀI VD THUYẾT MINH BUỔI 2 (đề CK1 Ái Mộ 2025–2026): a bốn điểm A, C, M, O → b DF là tiếp tuyến: AB là trung trực CD ⇒ FC = FD ⇒ ΔOCF = ΔODF ⇒ ∠ODF = ∠OCF = 90° — đúng nhịp 'tam giác cân → hai tam giác bằng nhau → dấu hiệu nhận biết'. Ý c VDC bỏ."),
 "ck1-tan-trieu-42": ("P2","Ví dụ","TH ghép bài",None,"TH",DK,None,"","Ví dụ đề mẫu cho bài Ái Mộ, cùng cách chứng minh tiếp tuyến nhưng khác hình: a bốn điểm O, A, C, M; b OD là trung trực MB ⇒ ΔOMD = ΔOBD ⇒ BD là tiếp tuyến (bước OH = ½AM là đường trung bình, lớp 8). Trùng đề HBT 2024 (đã gạt)."),
 "ck1-hat-mon-2025-IV2": ("P2","BTVN","VD lẻ",None,"VD",TL,None,"","Đề song song với bài Ái Mộ trên lớp (gần trùng nguyên văn) — trên lớp thì L5, nhưng BTVN gương 1–1 được phép (quy chuẩn mục 1). Ý c bỏ."),
 "ck1-chuong-my-2024-4.2": ("P2","Dự phòng","VD lẻ",None,"VD",TL,None,"","Hay nhưng lệch mục tiêu buổi 2: ý c chứng minh tiếp tuyến bằng cộng hai góc (không qua hai tam giác bằng nhau), ý b là hệ thức lượng. Để dành cho buổi ôn/đề kiểm tra."),
 "ck1-hoai-duc-2024-4.2": ("P2","Dự phòng","VD lẻ",None,"VD",TL,None,"","Cùng khuôn Chương Mỹ (hai đường cao, cộng góc), ý b đồng dạng thuộc buổi 4 — dự phòng."),
 "ck1-ban-mai-2024-3": ("P6","BTVN","VD lẻ",None,"VD",TL,None,"","ĐÚNG BTVN THUYẾT MINH BUỔI 6: ôn trọn bốn điểm → OI·OM = R² (buổi 4) → c OAHB là hình thoi (AC ∥ OB, BD ∥ OA, OA = OB) — chứng minh bằng kiến thức lớp 8, vừa sức C. (Trước để Ví dụ buổi 3 là dùng trước kiến thức buổi 4.)"),
 "ck1-dong-da-2025-IV2": ("P3","BTVN",None,None,None,None,None,"","Gương của Ví dụ Ba Đình (nửa đường tròn, tiếp tuyến tại A và M): OP ⊥ AM, OP ∥ MB. Cùng hình với ví dụ nên để BTVN. Ý c bỏ."),
 "ck1-lomonoxop-2024-IV2": ("P3","Dự phòng",None,None,None,None,None,"","Cùng hình Ba Đình/Đống Đa (KO trung trực MI ⇒ KO ∥ NI) — dự phòng."),
 "ck1-ngoc-lam-IV2": ("P3","BTVN","VD lẻ",None,"VD",TL,None,"","ĐÚNG BÀI VD THUYẾT MINH BUỔI 3 (đề CK1 Ngọc Lâm): bốn điểm S, A, B, O; SO ⊥ AB tại H, AD ∥ SO (trung trực → đường kính cho góc vuông → cùng vuông góc). Cặp với Phúc Đồng trên lớp, đúng như thuyết minh. Ý c bỏ."),
 "ck1-ngo-si-lien-2024-7": ("P5","Trên lớp","VD lẻ",None,"VD",TL,None,"","ĐÚNG BÀI VD THUYẾT MINH BUỔI 5 (hình ba tiếp tuyến của nửa đường tròn): a bốn điểm C, M, O, A thuộc đường tròn đường kính OC → b MB ⊥ OD và MB ∥ OC (hai lần trung trực, một lần đường kính) → c BK là phân giác ∠MBD (cộng góc trong tam giác cân OBK), vừa sức C. Ý d bỏ."),
 "ck1-ly-thanh-tong-7": ("P5","BTVN",None,None,None,None,None,"","BTVN luyện tập chung + đo lường: DB ∥ OA, AB² = AH·AO, AC là tiếp tuyến, c diện tích giới hạn bởi hai tiếp tuyến và cung nhỏ = S(ABOC) − S quạt ≈ 17,1 cm². Đề trường TP.HCM — ghi rõ nguồn."),
 "stk-b16-III-C57-tr252": ("P5","BTVN","TH lẻ LT",None,"TH",TLN,None,"","Gương treo bằng hai dây tiếp xúc, tổng dây 6 dm, góc 60° ⇒ R = 3·tan30° ≈ 1,73 dm — bài ngược của bài gương trên lớp, một bước tỉ số lượng giác."),
 "ck1-ta-quang-buu-2025-IV2": ("P4","Trên lớp","VD lẻ",None,"VD",TL,None,"","ĐÚNG BÀI VD THUYẾT MINH BUỔI 4 (đề Tạ Quang Bửu): a bốn điểm M, A, O, B → b AB ⊥ OM và MH·MO = MC·MD — hai cặp tam giác đồng dạng, bắc cầu qua MA². Ví dụ Ngọc Thụy khác hình (cát tuyến qua tâm). Ý c bỏ."),
 "ck1-nhat-tan-2024-4.2": ("P4","Dự phòng","VD lẻ",None,"VD",TL,None,"","Cùng hình Tạ Quang Bửu; ý 3 thêm ΔMBD ∽ ΔMCB (c.g.c từ đẳng thức tích) — vượt mục tiêu buổi 4 lớp C, để dự phòng."),
 "ck1-xuan-la-2024-4.2": ("P4","BTVN","VD lẻ",None,"VD",TL,None,"","ĐÚNG BTVN THUYẾT MINH BUỔI 4: OA ⊥ MN và AH·AO = AB·AC (bắc cầu qua AM²) — gương của bài Tạ Quang Bửu. Ý c (phân giác) bỏ."),
 "ck1-nguyen-truong-to-2025-IV": (None,None,None,None,None,None,None,"","ĐÚNG ĐỀ MẪU THUYẾT MINH BUỔI 6 (hình in sẵn, điền khuyết): bốn điểm → OA ⊥ BC, OA·OH = R² → AM·AN = AH·AO. Ý 3 cùng nếp Ví dụ buổi 4 (Ngọc Thụy) — buổi ôn nên chấp nhận. Ý 4 bỏ."),
}
THEM = [
 ("P3","Ví dụ","TH tách VD","ck1-ba-dinh-2024-IV2","a-b","TH",DK,[2,1,1,1,2,2,2,0],"","Ví dụ đề mẫu cho bài Phúc Đồng, khác hình (nửa đường tròn, tiếp tuyến tại A và D): OC là trung trực AD ⇒ OC ⊥ AD; BD ⊥ AD (đường kính AB) ⇒ OC ∥ BD — đúng dòng TH 'song song khi có đường kính đi qua tiếp điểm' của thuyết minh. Ý c bỏ."),
 ("P2","Trên lớp","NB lẻ LT","stk-b16-II-C45-tr246","","NB",DS,[2,1,1,1,2,2,1,0],"","Hình hai đường cao in sẵn: E thuộc (O) đường kính AH (Đ), BD = CD (Đ), DE > ½BC (S, DE = ½BC), DE là tiếp tuyến (Đ) — gom bốn điểm + tiếp tuyến trong một câu Đ/S. Đã soi ảnh tr.246 (chữ trích mất phân số ½)."),
]
R2 = []
for (p, vai, loai, ma, dong, muc, ht, T, ln, ld) in R:
    if ma in SUA:
        n = SUA[ma]
        p = n[0] or p; vai = n[1] or vai; loai = n[2] or loai; dong = n[3] if n[3] is not None else dong
        muc = n[4] or muc; ht = n[5] or ht; T = n[6] or T; ln = n[7]; ld = n[8] or ld
    R2.append((p, vai, loai, ma, dong, muc, ht, T, ln, ld))
R = R2 + THEM

# ---- Sửa 03/11 lượt 3: luật 09/10 "phiếu chứng minh thuần chứng minh, không bài tính độ dài" ----
L09 = "Luật 09/10: phiếu dạy chứng minh không có bài thay số tính độ dài (Pythagore, tỉ số lượng giác) — chuyển dự phòng."
SUA3 = {
 "tl-1-21": ("P2","Dự phòng",None,None,None,None,None,"", "Pythagore 3–4–5 rồi R = BC : 2. " + L09),
 "stk-b13-I-C17-tr8": ("P2","Trên lớp","NB kiến thức cũ",None,None,None,None,"", "Nền lớp 8 (trung tuyến ứng với cạnh huyền): tam giác vuông tại A ⇒ A thuộc đường tròn đường kính BC; ba phương án đặt đường kính sai cạnh — bẫy chọn nhầm cạnh huyền."),
 "stk-b16-I-C17-tr234": ("P2","Dự phòng",None,None,None,None,None,"", "Tiếp tuyến ⊥ bán kính rồi Pythagore ⇒ AB = 4 cm. " + L09),
 "sgk-5.22": ("P3","Trên lớp","TH lẻ LT",None,"TH",TL,None,"", "SGK 5.22: M trên phân giác, MA ⊥ Ox ⇒ ΔOAM = ΔOBM ⇒ MB ⊥ Oy, MA = MB ⇒ OA, OB là hai tiếp tuyến cắt nhau của (M; MA) — chứng minh thuần, dùng đúng dấu hiệu tiếp tuyến + định lí hai tiếp tuyến (thay bài Phúc Thọ có tính góc bằng sin)."),
 "ck1-phuc-dong-IV2": (None,None,None,"a-b",None,None,None,"", "Đề CK1 Phúc Đồng: a bốn điểm → b OA ⊥ BC và OA ∥ CD (đúng dạng IV.2b: trung trực → đường kính cho góc vuông → cùng vuông góc). Ý c (tính diện tích quạt theo R) bỏ theo luật 09/10 phiếu chứng minh thuần."),
 "ck1-phuc-tho-2024-5": ("P3","Dự phòng",None,None,None,None,None,"", "OI = 2R ⇒ sin∠OIA = ½ ⇒ 30°, ΔIAB đều. " + L09),
 "stk-b16-I-C21-tr235": ("P3","Dự phòng",None,None,None,None,None,"", "OM = 2R ⇒ cos∠AOM = ½ ⇒ 60°. " + L09),
 "sgk-b16-vd2": (None,None,None,"a",None,None,None,"", "Ví dụ 2 SGK ý a: MA = MB, OA = OB ⇒ OM là trung trực AB ⇒ OM ⊥ AB — mẫu chứng minh vuông góc. Ý b (tính MA) bỏ theo luật 09/10."),
 "stk-b16-II-C33-tr240": ("P4","Dự phòng",None,None,None,None,None,"", "Đ/S có số (BC = 10, BM, R = 3). " + L09),
 "stk-b16-II-C49-tr248": (None,None,None,None,None,None,None,"", "Đã soi ảnh tr.248: AC ⊥ MO (Đ), OH·OM = R² (Đ), ΔODM ∽ ΔOHD (Đ, c.g.c từ OD² = OH·OM), I trung điểm MH (Đ — khó, chỉ để BTVN). Sách không in hình — vẽ thêm."),
 "sgk-5.30": ("P5","Ví dụ","TH tách VD",None,"TH",DK,None,"", "Ví dụ đề mẫu cho bài Ngô Sĩ Liên (cùng hình ba tiếp tuyến, khác câu hỏi): MN = MA + NB (định lí hai tiếp tuyến hai lần); Q là trung điểm MN (đường trung bình hình thang)."),
 "stk-b16-III-C56-tr251": ("P5","Ví dụ","TH lẻ LT",None,"TH","Điền khuyết (thực tế, hình in sẵn)",None,"", "Ví dụ đi cùng bài gương treo (phần đo lường thực tế): tầm nhìn từ độ cao 5 m, AC ⊥ OC ⇒ AC = √(6400,005² − 6400²) ≈ 8 km; bẫy quên đổi 5 m ra km."),
 "stk-b16-I-C18-tr234": ("P6","Dự phòng",None,None,None,None,None,"", "R = 6, OA = 10 ⇒ AB = 8 cm (Pythagore). " + L09),
 "stk-b13-I-C20-tr8": ("P6","Dự phòng",None,None,None,None,None,"", "Hình chữ nhật 12 × 5 ⇒ R = 6,5 cm (Pythagore). " + L09),
}
THEM3 = [
 ("P3","BTVN","TH lẻ LT","sgk-5.39","a-b","TH",TL,[2,2,1,1,1,2,1,0],"","SGK 5.39: hai đường tròn (B; BA), (C; CA) cắt nhau tại A, A' ⇒ ΔBAC = ΔBA'C ⇒ BA, BA' là hai tiếp tuyến cắt nhau của (C; CA) — gương bài 5.22, thuần chứng minh."),
 ("P4","Trên lớp","NB lẻ LT","stk-b16-II-C47-tr247","","NB",DS,[2,1,1,1,2,2,1,0],"","Hai tiếp tuyến, đường kính AC, BK ⊥ AC: bốn điểm (Đ), ∠BCK = ∠AOM = ∠BOM (Đ, OM ∥ BC), MB·BC = BK·MO (Đ, ΔMBO ∽ ΔBKC), BI < BK (Đ) — Đ/S không số, đúng nhịp đồng dạng ⇒ tích. Soi ảnh tr.247 khi dựng phiếu."),
 ("P6","BTVN","NB lẻ LT","stk-b16-I-C10-tr233","","NB",TN,[2,0,1,0,1,2,1,0],"","R = 3, d = 5 ⇒ không cắt — gương câu C9 trên lớp."),
 ("P6","BTVN","NB lẻ LT","tl-1-35","","NB",TN,[2,0,1,0,1,2,1,0],"","Đường tròn có vô số trục đối xứng (mọi đường kính) — ôn Bài 13."),
]
R3 = []
for (p, vai, loai, ma, dong, muc, ht, T, ln, ld) in R:
    if ma in SUA3:
        n = SUA3[ma]
        p = n[0] or p; vai = n[1] or vai; loai = n[2] or loai; dong = n[3] if n[3] is not None else dong
        muc = n[4] or muc; ht = n[5] or ht; T = n[6] or T; ln = n[7]; ld = n[8] or ld
    R3.append((p, vai, loai, ma, dong, muc, ht, T, ln, ld))
R = R3 + THEM3

SUA4 = {"ck1-dong-da-2025-IV2": ["P3", "Trên lớp", "Gương của Ví dụ Ba Đình nhưng làm trên lớp ngay sau ví dụ SGK 2a: OP ⊥ AM, OP ∥ MB (nửa đường tròn). Ý c bỏ."], "ck1-lomonoxop-2024-IV2": ["P3", "BTVN", "BTVN gương bài Đống Đa: KO là trung trực MI ⇒ KO ∥ NI."], "ck1-thanh-tri-2024-IV2": ["P4", "BTVN", "BTVN: CE·CB = CA² rồi ΔCDE ∽ ΔCBD (c.g.c) — gương bài Cầu Giấy (cân quỹ phút: trên lớp chỉ giữ một bài đường kính)."], "ck1-nguyen-binh-khiem-2025-4.2": ["P4", "Dự phòng", "Gương Dịch Vọng (CA·CE = 4R²) — dư quỹ BTVN, để dự phòng."], "ck1-chuong-my-2024-4.2": ["P6", "BTVN", "BTVN bài tập cuối chương: hai đường cao — bốn điểm, AD·AB = AE·AC, IE là tiếp tuyến (cộng góc). Lệch mục tiêu buổi 2 nhưng hợp ôn tổng hợp."], "ck1-hoai-duc-2024-4.2": ["P6", "BTVN", "BTVN bài tập cuối chương: bốn điểm B, E, D, C; AE·AB = AD·AC; OE là tiếp tuyến của (I)."], "ck1-ngoi-sao-2024-4.1": ["P5", "Trên lớp", "Câu IV.1 khởi động trên lớp: đèn vành khuyên đường kính 90 và 60 cm ⇒ đổi ra bán kính (bẫy dùng đường kính)."]}
R = [((SUA4[r[3]][0], SUA4[r[3]][1]) + r[2:9] + (SUA4[r[3]][2],)) if r[3] in SUA4 else r for r in R]

def ydong(de, dong):
    """Lấy phần dẫn + các ý trong dòng cộng dồn."""
    if not dong:
        return de
    labs = dong.split('-')
    lines = de.split('\n')
    out = []
    pat = re.compile(r'^\s*([a-z]|[0-9])[\)\./]|^\s*([0-9])\.\s')
    cur = None
    for ln in lines:
        m = re.match(r'^\s*(\d|[a-z])\s*[\)\./]\s', ln) or re.match(r'^\s*(\d|[a-z])[\)]', ln)
        if m:
            cur = m.group(1)
            if cur in labs:
                out.append(ln)
            continue
        if cur is None or cur in labs:
            out.append(ln)
    return '\n'.join(out)

def main(repo):
    bank = {r['ma']: r for r in json.load(open(f'{repo}/inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-05.json'))['rows']}
    out = []
    seen = {}
    for (p, vai, loai, ma, dong, muc, ht, T, ln, ld) in R:
        r = bank.get(ma)
        if r is None:
            raise SystemExit(f'MÃ KHÔNG CÓ TRONG TAB: {ma}')
        if vai not in ('Loại',):
            if ma in seen:
                raise SystemExit(f'BÀI GỐC BỐC HAI LẦN: {ma} ({seen[ma]} và {p})')
            seen[ma] = p
        diem = round(sum(t * w for t, w in zip(T, W)) / (2 * sum(W)) * 10, 1)
        nguong = {'VD': 7, 'TH': 6}.get(muc, 5)
        src = 'Đề thi' if r['uu'].startswith('Ưu tiên 1') else ('SGK' if r['uu'].startswith('Ưu tiên 2') else 'STK')
        out.append(dict(phieu=p, vai=vai, loai=loai, ma=ma, dong=dong, muc=muc, hinh_thuc=ht,
                        de=ydong(r['de'], dong), nguon=r['nguon'], loai_nguon=src, loai_ngay=ln,
                        T=T, diem=diem, nguong=nguong, ly_do=ld, muc_y_goc=r['muc_y']))
    return out

if __name__ == '__main__':
    rows = main(sys.argv[1])
    json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    import collections
    for p in ['P1','P2','P3','P4','P5','P6']:
        rs = [r for r in rows if r['phieu'] == p and r['vai'] not in ('Loại','Dự phòng')]
        low = [(r['ma'], r['diem'], r['nguong']) for r in rs if r['diem'] < r['nguong']]
        lop = [r for r in rs if 'Trên lớp' in r['vai']]
        c = collections.Counter(r['loai_nguon'] for r in lop)
        print(p, len(rs), 'dưới ngưỡng:', low, '| nguồn trên lớp:', dict(c))
