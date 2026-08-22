# Lớp 9 — GIẢI BÀI TOÁN BẰNG CÁCH LẬP HỆ PHƯƠNG TRÌNH

> Người 1: **ThaiTD** · Người 2: BichVN · Deadline 22/8
> Nguồn dữ liệu: `inputs/refs/de-thi/lop-9/exams/` — 45 đề Hà Nội 2025–2026 (10 GK1, 11 CK1, 10 CK2, 3 GK2, 11 Vào 10).

---

## 0. Vì sao dạng này đáng đầu tư nhất

| Kỳ thi | Tần suất | Điểm trung bình |
|---|---|---|
| Giữa kì I | **10/10 đề (100%)** — 12 câu | ~1,85đ |
| Cuối kì I | **9/11 đề (82%)** — 9 câu (+3 câu ghi "lập PT **hoặc** hệ PT") | ~1,5đ |
| Vào 10 | **9/11 đề (82%)** — Câu III.1, khuôn "lập PT hoặc hệ PT" | **1,0đ cố định của Sở** |

→ Tổng **34 câu / 45 đề**. Đây là dạng có **tỉ lệ xuất hiện cao nhất toàn bộ ngân hàng** và là câu ăn điểm chắc nhất khối Vận dụng.

**Điểm mấu chốt:** trong đề Vào 10, đề luôn cho phép chọn "lập phương trình **hoặc** hệ phương trình". Dạy hệ 2 ẩn là **an toàn hơn** cho HS trung bình vì mỗi dữ kiện của đề biến thành đúng một phương trình — không phải tự biểu diễn đại lượng thứ hai qua ẩn thứ nhất.

---

## 1. LIỆT KÊ TOÀN BỘ CÂU TRONG NGÂN HÀNG ĐỀ

### 1.1. Nhóm A — Lập hệ phương trình (mã `DS-THUCTE-LAPHE`, 22 câu)

| # | Mã câu | Trường / Kỳ | Điểm | Mô-típ | Đáp số |
|---|---|---|---|---|---|
| 1 | `ck1-chu-van-an-III` | Chu Văn An · CK1 | 2,0 | Giá niêm yết – giảm % (1400 vở + 700 bút, giảm 5%/10%) | Vở 12 000đ; bút 8 000đ |
| 2 | `ck1-phuc-dong-III2` | Phúc Đồng · CK1 | 1,0 | Giá niêm yết – giảm % (tivi 20%, máy giặt 25%) | 12,5 tr; 16 tr |
| 3 | `gk1-bat-trang-3-1` | Bát Tràng · GK1 | 1,5 | Giá niêm yết – giảm % (2 cuốn sách 20%/25%) | 260; 200 nghìn |
| 4 | `gk1-dvhau-2-1` | Dịch Vọng Hậu · GK1 | 1,5 | Giá niêm yết – giảm % (sách Toán 20%, Văn 10%) | 250 000đ; 200 000đ |
| 5 | `gk1-ngo-gia-tu-3-2` | Ngô Gia Tự · GK1 | 1,5 | Giá niêm yết – giảm % (bàn là 10%, quạt 20%) ⚠️ *HDC gốc tự mâu thuẫn* | **500; 250 nghìn** (HDC ghi 400; 300) |
| 6 | `gk1-nbk-2-1` | Nguyễn Bỉnh Khiêm · GK1 | 1,5 | Giá niêm yết – giảm % (bánh nướng 20%, bánh dẻo 25%) | 90; 60 nghìn |
| 7 | `gk1-van-yen-2-1` | Vân Yên · GK1 | 1,5 | Giá niêm yết – giảm % (10 bút + 20 vở) ⚠️ *đã sửa lại đề* | Bút 3 500đ; vở 8 000đ |
| 8 | `v10-dong-da-01-III2` | PGD Đống Đa · Vào 10 | 1,0 | Giá niêm yết – giảm % (bàn là 10%, quạt 20%) | 450; 400 nghìn |
| 9 | `ck1-dich-vong-III` | Dịch Vọng · CK1 | 2,0 | Hai loại đối tượng (xe 45 chỗ / 30 chỗ, 615 người) | 11 xe; 4 xe |
| 10 | `ck1-ly-thanh-tong-4` | Lý Thánh Tông · CK1 | 1,0 | Hai loại đối tượng (tờ 10k / 20k, 32 tờ) | 12 tờ; 20 tờ |
| 11 | `ck1-phuong-ha-dong-3` | Phương Hà Đông · CK1 | 1,5 | Hai loại đối tượng (vé 100k / 70k, 575 vé) | 250; 325 vé |
| 12 | `gk1-thai-thinh-3` | Thái Thịnh · GK1 | 2,0 | Hai loại đối tượng + giảm 5% vé trẻ em ⚠️ *đã sửa đáp án* | 10 người lớn; 240 trẻ em |
| 13 | `ck1-ai-mo-3-1` | Ái Mộ · CK1 | 2,0 | Công việc chung – riêng (2 thợ sơn, 6 ngày) | 9 ngày; 18 ngày |
| 14 | `gk1-phu-dien-3-1` | Phú Diễn · GK1 | 1,0 | Công việc chung – riêng (2 đội xe, 8 ngày) ⚠️ *đã sửa đáp án* | Đội I 24 ngày; đội II 12 ngày |
| 15 | `ck1-trung-vuong-II2` | Trưng Vương · CK1 | 1,5 | Chuyển động xuôi / ngược dòng (2 tour du thuyền) | v riêng 15 km/h; v nước 5 km/h |
| 16 | `gk1-nbk-2-2` | Nguyễn Bỉnh Khiêm · GK1 | 2,0 | Chuyển động 2 xe (hơn 15 km/h, đến trước 30′) | 60 và 75 km/h |
| 17 | `gk1-van-yen-2-2` | Vân Yên · GK1 | 1,5 | Chuyển động sớm 1h / muộn 1h ⚠️ *đã bổ sung đáp án* | AB = 300 km (v = 60, t = 5) |
| 18 | `gk1-co-nhue-2-2-1` | Cổ Nhuế 2 · GK1 | 1,5 | Năng suất – kế hoạch (tăng 15%/25%, vượt 95 bộ) | Tổ I 300; tổ II 200 bộ |
| 19 | `gk1-nguyen-du-2-1` | Nguyễn Du · GK1 | 1,5 | Hình học (HCN, dài hơn rộng 5m, S giảm 180 m²) | 25 m; 20 m |
| 20 | `gk1-trung-vuong-2-2` | Trưng Vương · GK1 | 1,5 | Hai giả thiết lệch (đọc thêm 9 trang / bớt 12 trang) | 360 trang |
| 21 | `ck1-tan-trieu-31` | Tân Triều · CK1 | 1,0 | Số có hai chữ số (tổng 12, đảo lớn hơn 54) | 39 |
| 22 | `ck1-ngoc-thuy-II` | Ngọc Thụy · CK1 | 2,0 | Lãi suất – đầu tư (5%/năm và 7%/năm) | 125 tr; 125 tr |

**Phân bố mô-típ:** giá niêm yết – giảm % **8/22 câu (36%)** · hai loại đối tượng 4 · chuyển động 3 · công việc 2 · năng suất 1 · hình học 1 · hai giả thiết lệch 1 · số 2 chữ số 1 · lãi suất 1.

### 1.2. Nhóm B — Đề ghi "lập PT **hoặc** hệ PT" (mã `DS-THUCTE-LAPPT`, 3 câu CK1)

| # | Mã câu | Trường | Điểm | Mô-típ | Đáp số |
|---|---|---|---|---|---|
| 23 | `ck1-cau-dien-3B` | Cầu Diễn | 1,5 | Công việc chung – riêng (4 giờ; lệch 6 giờ) | 6 giờ; 12 giờ |
| 24 | `ck1-ngoc-lam-III` | Ngọc Lâm | 1,5 | Hình học (HCN, dài hơn rộng 5m, S tăng 91 m²) | 15 m; 20 m |
| 25 | `ck1-phuc-dong-III1` | Phúc Đồng | 1,0 | Chuyển động đi – về (15 và 12 km/h, lệch 45′) | AB = 45 km |

### 1.3. Nhóm C — Khuôn Câu III.1 của đề Vào 10 (mã `DS-THUCTE-LAPPT-BAC2`, 9 câu)

> Đây là **câu 1,0đ cố định** trong cấu trúc của Sở. Đề luôn viết "Giải bài toán bằng cách lập phương trình hoặc hệ phương trình".

| # | Mã câu | Nguồn | Mô-típ | Phương trình lập được | Đáp số |
|---|---|---|---|---|---|
| 26 | `v10-so-2025-III1` | **Sở Hà Nội 2025 (chính thức)** | Chuyển động đi – về | s/40 − s/60 = 1 | 120 km |
| 27 | `v10-so-2026-III1` | **Sở Hà Nội 2026 (chính thức)** | Năng suất – kế hoạch (3 ngày + 7 ngày) | 3x + 7(x+5) = 335 | 30 áo/ngày |
| 28 | `v10-so-minh-hoa-III2` | **Sở Hà Nội (minh họa)** | Năng suất – kế hoạch (300 SP, sớm 1 ngày) | 300/x − 300/(x+10) = 1 | 50 SP/ngày |
| 29 | `v10-dong-da-01-III1` | PGD Đống Đa | Hình học (HCN, S = 180 m²) | x(x+11) = 180 | 9 m và 20 m |
| 30 | `v10-chuong-my-4-III2` | PGD Chương Mỹ (thử 4) | Năng suất (60 tấn, bớt 2 xe) | 60/(x−2) − 60/x = 1 | 12 xe |
| 31 | `v10-chuong-my-5-III1` | PGD Chương Mỹ (thử 5) | Chuyển động (lệch 25′, hơn 20 km/h) | 50/x − 50/(x+20) = 5/12 | 40 và 60 km/h |
| 32 | `v10-thanh-oai-III2` | PGD Thanh Oai (thử 2) | Năng suất (sớm 30′ **và** vượt 3 SP) | 60/x − 63/(x+2) = 1/2 | 12 SP/giờ |
| 33 | `v10-tu-lap-III2` | THCS Tự Lập | Chuyển động (3 km đầu + dừng 3′) | 12/x = 3/x + 1/20 + 9/(x+6) | 36 km/h — không vi phạm |
| 34 | `v10-ung-hoa-III2` | PGD Ứng Hòa | Công việc chung – riêng (3h36′; lệch 3h) | 1/x + 1/(x+3) = 5/18 | 6 giờ; 9 giờ |

### 1.4. Ghi chú kiểm chứng

Trong quá trình rà, **4 câu trong ngân hàng chép sai** đã được sửa (đối chiếu ảnh PDF gốc, commit cùng tài liệu này):

| Mã câu | Sai ở bản cũ | Đã sửa thành |
|---|---|---|
| `gk1-van-yen-2-1` | "12 cây bút bi" | 10 cây bút bi → nghiệm đẹp 3 500đ / 8 000đ |
| `gk1-van-yen-2-2` | Bỏ trống đáp số | AB = 300 km |
| `gk1-thai-thinh-3` | "nghiệm không nguyên, cần Thầy xác nhận" | Nghiệm nguyên: 10 người lớn, 240 trẻ em |
| `gk1-phu-dien-3-1` | Đáp án **đảo** (I 12 ngày, II 24 ngày) | Đội I 24 ngày, đội II 12 ngày |
| `gk1-ngo-gia-tu-3-2` | Chép theo HDC gốc (400; 300) trong khi HDC tự mâu thuẫn | Theo đề (750 nghìn): **500; 250 nghìn** |

---

## 2. QUY TẮC & CÁCH GIẢI MẪU CHUNG

### 2.1. Khung 5 bước bất biến (dùng cho **mọi** mô-típ)

```
B1. ĐẶT ẨN   : Gọi <đại lượng đề hỏi> là x, y — kèm ĐƠN VỊ và ĐIỀU KIỆN.
B2. DỊCH     : Mỗi câu dữ kiện của đề → một dòng biểu thức theo x, y.
B3. LẬP HỆ   : Gom đúng 2 dòng "cân bằng" thành hệ 2 phương trình.
B4. GIẢI     : Thế hoặc cộng đại số → (x; y).
B5. KẾT      : Đối chiếu điều kiện → câu "Vậy ..." trả lời ĐÚNG câu hỏi của đề.
```

**Quy tắc vàng số 1 — "Đề hỏi gì thì gọi cái đó là ẩn."**
Đúng với 21/22 câu nhóm A. Ngoại lệ duy nhất: `v10-dong-da-01-III2` hỏi *số tiền chênh lệch* — vẫn gọi ẩn là giá niêm yết, rồi tính thêm một dòng ở B5.

**Quy tắc vàng số 2 — "Đếm dữ kiện số: có đúng 2 con số 'tổng' thì lập được đúng 2 phương trình."**
Trong toàn bộ 22 câu, hai phương trình luôn đến từ hai câu khác nhau của đề, không bao giờ từ cùng một câu.

**Quy tắc vàng số 3 — Bảng dịch đề (công cụ chống "không biết bắt đầu từ đâu"):**

| Mô-típ | Ẩn nên gọi | PT (1) — dữ kiện "gộp" | PT (2) — dữ kiện "lệch" |
|---|---|---|---|
| Giá niêm yết – giảm % | x, y = giá niêm yết mỗi loại | x + y = tổng niêm yết | (1−a)x + (1−b)y = tổng thực trả |
| Hai loại đối tượng | x, y = số lượng mỗi loại | x + y = tổng số lượng | px + qy = tổng giá trị |
| Năng suất – kế hoạch | x, y = số SP theo kế hoạch | x + y = tổng kế hoạch | ax + by = phần vượt/thiếu |
| Công việc chung – riêng | x, y = số ngày làm **một mình** | 1/x + 1/y = 1/(số ngày chung) | m/x + n/y = 1 (hoặc phần việc đã làm) |
| Chuyển động | x = vận tốc, y = thời gian (hoặc s) | quãng đường: x·y = s | quãng đường ở tình huống 2 bằng s |
| Xuôi – ngược dòng | x = v riêng, y = v dòng nước | s₁/(x+y) + s₂/(x−y) = t₁ | s₃/(x+y) + s₄/(x−y) = t₂ |
| Hình học (HCN) | x = dài, y = rộng | x − y = độ lệch | (x±m)(y±n) = xy ± ΔS |
| Số có hai chữ số | x = chữ số hàng chục, y = hàng đơn vị | x + y = tổng chữ số | (10y+x) − (10x+y) = lệch |

### 2.2. Bài giải mẫu — mô-típ chiếm 36% (giá niêm yết – giảm %)

> **Đề** (`gk1-nbk-2-1`, Nguyễn Bỉnh Khiêm GK1, 1,5đ): Tổng giá niêm yết của một chiếc bánh nướng và một chiếc bánh dẻo là 150 nghìn đồng. Dịp Tết, bánh nướng được giảm 20% và bánh dẻo được giảm 25% so với giá niêm yết nên cô Liên mua cả hai chiếc hết 117 nghìn đồng. Tính giá niêm yết của mỗi loại bánh.

**Lời giải**

Gọi giá niêm yết của một chiếc bánh nướng là *x* (nghìn đồng) và của một chiếc bánh dẻo là *y* (nghìn đồng); điều kiện 0 < x < 150, 0 < y < 150.

Vì tổng giá niêm yết của hai chiếc bánh là 150 nghìn đồng nên

&nbsp;&nbsp;&nbsp;&nbsp;**x + y = 150**&nbsp;&nbsp;(1)

Bánh nướng được giảm 20% nên giá phải trả là 80%·x = 0,8x (nghìn đồng).
Bánh dẻo được giảm 25% nên giá phải trả là 75%·y = 0,75y (nghìn đồng).
Vì cô Liên mua cả hai chiếc hết 117 nghìn đồng nên

&nbsp;&nbsp;&nbsp;&nbsp;**0,8x + 0,75y = 117**&nbsp;&nbsp;(2)

Từ (1) và (2) ta có hệ phương trình

&nbsp;&nbsp;&nbsp;&nbsp;{ x + y = 150 ; 0,8x + 0,75y = 117 }

Từ (1) suy ra y = 150 − x. Thay vào (2):

&nbsp;&nbsp;&nbsp;&nbsp;0,8x + 0,75(150 − x) = 117
&nbsp;&nbsp;&nbsp;&nbsp;0,8x + 112,5 − 0,75x = 117
&nbsp;&nbsp;&nbsp;&nbsp;0,05x = 4,5
&nbsp;&nbsp;&nbsp;&nbsp;x = 90 ⟹ y = 150 − 90 = 60

Ta thấy x = 90 và y = 60 đều thỏa mãn điều kiện.

**Vậy** giá niêm yết của bánh nướng là 90 nghìn đồng và của bánh dẻo là 60 nghìn đồng.

> **Bản đối chiếu — biến thể "được giảm" thay vì "phải trả"** (`v10-dong-da-01-III2`): tổng niêm yết 850 nghìn, bàn là giảm 10%, quạt giảm 20%, **người mua trả ít hơn 125 nghìn đồng**. Khi đó phương trình (2) đổi thành **0,1x + 0,2y = 125** (số tiền *được giảm*, không phải số tiền *phải trả*) → x = 450, y = 400. Hai biến thể này chỉ khác nhau đúng một dòng — nên dạy liền nhau trong cùng một buổi để HS phân biệt.

### 2.3. Ba cái bẫy lặp lại nhiều nhất trong 34 câu

| Bẫy | Xuất hiện ở | Cách chặn |
|---|---|---|
| **"Được giảm 100 nghìn" ≠ "phải trả 100 nghìn"** | #5, #8 (giảm) vs #1, #2, #3, #4, #6 (phải trả) | Bắt HS gạch chân từ khóa và viết ra vế phải trước khi viết vế trái |
| **Đổi đơn vị thời gian** | #16 (30 phút), #17, #25 (45 phút), #31 (25 phút), #32 (30 phút), #34 (3 giờ 36 phút) | Luật: mọi thời gian đổi về **giờ dạng phân số** ngay ở B1 |
| **Quên điều kiện / quên loại nghiệm âm** | Toàn bộ nhóm C (PT bậc hai luôn có 1 nghiệm âm) | ĐK viết ngay dòng B1, không để đến cuối |

---

## 3. BẢNG SCAFFOLDING — TỪNG BƯỚC & LÝ DO

Ký hiệu cột **"Trong bài thi"**: bước này có được **viết ra giấy và ăn điểm barem** hay chỉ là thao tác nháp.

| Bước | HS làm gì | **Vì sao phải làm bước này** | Trong bài thi? |
|---|---|---|---|
| **S0. Đọc – gạch chân** | Gạch chân (a) đại lượng đề **hỏi**, (b) mọi con số, (c) từ khóa quan hệ: *tổng, hơn, kém, giảm, vượt, sớm, muộn*. | Sai đề gần như luôn bắt nguồn từ đọc sót một từ quan hệ. Gạch chân biến "đọc hiểu" thành thao tác cơ học, HS yếu vẫn làm được. | ❌ Nháp — nhưng là bước quyết định 100% các bước sau |
| **S1. Gọi ẩn + đơn vị + điều kiện** | Viết đúng 1 câu: *"Gọi … là x (đơn vị), … là y (đơn vị); điều kiện …"* | Ẩn không có đơn vị thì không kiểm tra được tính hợp lý; không có ĐK thì mất điểm ở bước đối chiếu cuối. Đây cũng là **điểm thành phần đầu tiên** trong mọi HDC. | ✅ **Có — 0,25đ** (HDC Ngô Sĩ Liên, Lê Ngọc Hân, Ngô Gia Tự đều tách riêng dòng này) |
| **S2. Dịch dữ kiện thứ nhất** | Viết PT (1) — luôn là dữ kiện "gộp" (tổng số lượng / tổng tiền niêm yết / làm chung). | Dữ kiện gộp bao giờ cũng đơn giản nhất → HS có ngay một phương trình đúng, tạo đà tâm lý và **ăn được điểm thành phần dù bài chưa xong**. | ✅ **Có — 0,25đ** |
| **S3. Dịch dữ kiện thứ hai** | Viết PT (2) — dữ kiện "lệch" (sau giảm giá / vượt chỉ tiêu / chênh thời gian). | Đây là bước duy nhất thật sự khó. Tách riêng khỏi S2 để HS chỉ phải nghĩ **một** ý tại một thời điểm. | ✅ **Có — 0,25đ đến 0,5đ** (câu đắt nhất của bài) |
| **S4. Viết hệ** | Gộp (1), (2) vào dấu ngoặc nhọn. | Hình thức, nhưng HDC chấm theo "lập được hệ" — thiếu dấu ngoặc nhọn nhiều giám khảo vẫn trừ. | ✅ **Có** — thường gộp điểm với S3 |
| **S5. Giải hệ** | Thế hoặc cộng đại số. | Kỹ năng đã học ở Bài "Giải hệ hai PT bậc nhất hai ẩn" — **không dạy lại ở đây**, chỉ nhắc chọn phương pháp: có hệ số 1 → thế; hệ số đối nhau → cộng. | ✅ **Có — 0,5đ** |
| **S6. Đối chiếu điều kiện** | Viết *"x = …, y = … thỏa mãn điều kiện."* | Ở nhóm C (Vào 10) luôn có nghiệm âm bị loại; ở nhóm A đảm bảo nghiệm có nghĩa thực tế (số xe nguyên dương…). | ✅ **Có — 0,25đ** (một số HDC ghi rõ *"HS không kiểm tra ĐK không trừ điểm"* — nhưng đa số có trừ) |
| **S7. Câu trả lời** | Viết *"Vậy …"* **lặp lại đúng câu hỏi của đề**, kèm đơn vị. | HS thường dừng ở "x = 400" mà không trả lời "bàn là 400 nghìn đồng". Đây là mất điểm oan phổ biến nhất. | ✅ **Có — 0,25đ**; HDC Lê Ngọc Hân ghi rõ *"thiếu đơn vị trừ 0,25 điểm"* |

**Trả lời trực tiếp câu hỏi "có giải thích được trong các bài thi không?"**
→ **Có, và giải thích được từng đồng điểm.** 7/8 bước scaffolding trên đều tương ứng một dòng trong hướng dẫn chấm của đề thật. Bài 2,0đ thường được chẻ thành 0,25 (gọi ẩn) + 0,25 (PT 1) + 0,5 (PT 2) + 0,5 (giải) + 0,25 (đối chiếu) + 0,25 (kết luận). Nghĩa là **HS lập được hệ mà giải sai vẫn ăn ~1,0/2,0đ** — đây là lập luận thuyết phục nhất để bắt HS yếu phải viết đủ bước.

**Bằng chứng barem — chép nguyên văn từ HDC Ngô Gia Tự GK1 2025–2026 (Bài 2, 3,0đ):**

| Dòng trong hướng dẫn chấm | Điểm | Ứng với bước |
|---|---|---|
| "Gọi số áo mà tổ phải may theo dự định là x (x ∈ N*) (cái áo)" | 0,25 | S1 |
| "Số áo mà tổ phải may theo thực tế là x + 15 (cái áo)" | 0,25 | S2 |
| "Thời gian hoàn thành theo dự định là x/50 (ngày)" | 0,25 | S2 |
| "Thời gian hoàn thành theo thực tế là (x+15)/55 (ngày)" | 0,25 | S2 |
| "Theo giả thiết, ta có phương trình: x/50 − (x+15)/55 = 2" | 0,25 | S3–S4 |
| "Giải đúng: x = 1250 (TM)" | 0,25 | S5–S6 |
| "Kết luận: số áo mà tổ phải may theo dự định là 1250 cái áo" | 0,25 | S7 |

→ **HS chỉ viết được 4 dòng đầu (chưa lập nổi phương trình) đã có 1,0/3,0đ.** Đây là con số nên nói thẳng với HS yếu.

### 3.1. Lộ trình luyện (thứ tự dạy đề xuất)

| Buổi | Mô-típ | Lý do xếp thứ tự này |
|---|---|---|
| 1 | Hai loại đối tượng (#9, #10, #11) | Hệ đẹp nhất: x + y = tổng, px + qy = tổng tiền. Không có %, không có mẫu. |
| 2 | Giá niêm yết – giảm % (#1→#8) | Chiếm 36% đề. Chỉ thêm một kỹ năng mới: dịch "%". |
| 3 | Năng suất – kế hoạch (#18, #27, #28, #30, #32) | Cùng cấu trúc buổi 2, thay "tiền" bằng "sản phẩm". |
| 4 | Chuyển động (#15, #16, #17, #26, #31, #33) | Xuất hiện mẫu số → khó hơn hẳn, cần công cụ bảng s–v–t. |
| 5 | Công việc chung – riêng (#13, #14, #23, #34) | Khó nhất: ẩn nằm ở mẫu, phải đặt ẩn phụ 1/x. |
| 6 | Còn lại: hình học, số 2 chữ số, lãi suất, hai giả thiết lệch (#19, #20, #21, #22, #24, #29) | Mỗi mô-típ 1–2 bài, chỉ cần nhận diện. |

---

## 4. CHECKLIST & RUBRIC

### 4.1. Checklist HS tự kiểm (in ở góc phiếu, HS tự tick trước khi nộp)

- [ ] Tôi đã **gọi ẩn đúng thứ đề hỏi**, có **đơn vị**, có **điều kiện**.
- [ ] Mọi thời gian trong bài đã đổi về **cùng một đơn vị** (giờ hoặc phút, không lẫn).
- [ ] Tôi đã dùng **hết** các con số của đề (không thừa, không thiếu con số nào).
- [ ] Tôi phân biệt được đề cho **"được giảm bao nhiêu"** hay **"phải trả bao nhiêu"**.
- [ ] Hệ của tôi có đúng **2 phương trình, 2 ẩn**.
- [ ] Tôi đã **thay nghiệm ngược lại đề** để thử (không phải thay vào hệ).
- [ ] Tôi đã viết dòng **"thỏa mãn điều kiện"**.
- [ ] Câu **"Vậy…"** của tôi trả lời **đúng thứ đề hỏi**, có **đơn vị**.

### 4.2. Rubric chấm — thang 4 mức (dùng cho GV chấm phiếu & đánh giá năng lực)

| Tiêu chí | Mức 1 — Chưa đạt | Mức 2 — Đạt | Mức 3 — Khá | Mức 4 — Tốt |
|---|---|---|---|---|
| **T1. Đặt ẩn** | Không gọi ẩn, hoặc gọi ẩn không phải thứ đề hỏi | Gọi đúng ẩn nhưng thiếu đơn vị **hoặc** thiếu điều kiện | Đủ ẩn + đơn vị + điều kiện | Đủ, và điều kiện *chặt* (VD: x ∈ ℕ*, x > 8) |
| **T2. Dịch dữ kiện "gộp" → PT(1)** | Không lập được | Lập được với gợi ý | Tự lập đúng | Tự lập đúng ở mô-típ **chưa từng gặp** |
| **T3. Dịch dữ kiện "lệch" → PT(2)** | Không lập được | Lập được sau khi GV chỉ ra từ khóa | Tự lập đúng ở mô-típ quen | Tự lập đúng cả khi có % / mẫu số / đổi đơn vị |
| **T4. Giải hệ** | Sai kỹ thuật cơ bản | Giải đúng khi hệ đã ở dạng chuẩn | Tự chọn được phương pháp phù hợp | Giải gọn, biết đặt ẩn phụ 1/x khi cần |
| **T5. Đối chiếu & kết luận** | Không có | Có "Vậy…" nhưng thiếu đơn vị hoặc thiếu đối chiếu | Đủ cả hai | Đủ, và **thử lại vào đề** để tự phát hiện sai |
| **T6. Trình bày** | Rời rạc, không thành bài | Đủ ý nhưng lộn xộn | Theo đúng 5 bước | Theo đúng 5 bước, câu văn toán học chuẩn |

**Ngưỡng kết luận "HS làm được dạng này":**
- **Đạt tối thiểu** = T1, T2, T5 ở mức ≥ 2 và T4 ở mức ≥ 2 → ăn được ~50% điểm câu.
- **Đạt chuẩn thi** = **tất cả** tiêu chí ở mức ≥ 3 trên **2 mô-típ khác nhau**, làm trong ≤ 12 phút.
- **Vững** = T3 mức 4 (tự lập được PT lệch ở mô-típ lạ) → đủ sức ăn trọn 1,0đ Câu III.1 đề Vào 10.

### 4.3. Bộ 3 câu kiểm tra nhanh (15 phút, dùng để chốt "HS có làm được không")

| Câu | Lấy từ | Kiểm tra tiêu chí |
|---|---|---|
| 1 | `gk1-ngo-gia-tu-3-2` (giá niêm yết – giảm %) | T1, T2, T3 mô-típ quen |
| 2 | `v10-so-2026-III1` (năng suất, đề Sở 2026) | T3 mô-típ biến thể + T5 |
| 3 | `gk1-phu-dien-3-1` (công việc chung – riêng) | T4 (ẩn ở mẫu) + T3 mức 4 |

> HS làm đúng câu 1 và 2 → **đủ điểm Câu III.1 Vào 10**. Đúng cả câu 3 → vững dạng.
