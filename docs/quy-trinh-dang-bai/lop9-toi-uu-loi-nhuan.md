# Lớp 9 — GIẢI BÀI TOÁN TỐI ƯU LỢI NHUẬN

> Người 1: **ThaiTD** · Người 2: BichVN · Deadline 22/8
> Nguồn dữ liệu: `inputs/refs/de-thi/lop-9/exams/` — mã dạng `DS-CUCTRI`, `DS-PT-THUCTE`, `DS-BĐT-COSI`.

---

## 0. Vị trí của dạng trong đề thi

| Kỳ thi | Tần suất | Điểm | Vị trí |
|---|---|---|---|
| Giữa kì I | **9/10 đề (90%)** — 9 câu | **0,5đ** | Câu cuối đề (Bài V / Bài 5) |
| Cuối kì I | **6/11 đề (55%)** — 8 câu | **0,5đ** | Câu cuối đề |
| Vào 10 | 0/11 | — | **KHÔNG có** trong cấu trúc của Sở |

**Kết luận nghiệp vụ quan trọng:** đây là **câu 0,5đ vận dụng cao cuối đề kiểm tra trường**, không phải nội dung thi Vào 10. Với lớp tầng C, đây là câu **được phép bỏ**; với lớp A/B, đây là câu **phân loại**. Cần nói rõ điều này khi phân bổ thời lượng — 17 câu trong ngân hàng nhưng tổng trọng số chỉ ~0,5đ/đề.

---

## 1. LIỆT KÊ TOÀN BỘ CÂU TRONG NGÂN HÀNG ĐỀ

### 1.1. Nhóm 1 — Tối ưu doanh thu / lợi nhuận theo khuôn "mỗi lần tăng a thì giảm b" (5 câu — **đúng trọng tâm dòng này**)

| # | Mã câu | Trường / Kỳ | Đề tóm tắt | Hàm lập được | Đáp số |
|---|---|---|---|---|---|
| 1 | `ck1-chu-van-an-V` | Chu Văn An · CK1 · 0,5đ | Điện thoại nhập 14 tr, bán 16 tr, bán 50 chiếc/tháng; **giảm** 100 000đ/chiếc thì bán thêm 5 chiếc. Tìm mức giảm để **lợi nhuận** lớn nhất | P(x) = (2 − 0,1x)(50 + 5x) = −0,5x² + 5x + 100 (triệu) | Giảm **500 000đ**/chiếc (x = 5); lợi nhuận max 112,5 tr |
| 2 | `ck1-tan-trieu-5` | Tân Triều · CK1 · 0,5đ | Rạp 120 ghế, vé 100 nghìn bán hết; **tăng** 5 nghìn thì trống thêm 4 ghế. Giá vé mới để **doanh thu** lớn nhất | R(x) = (100 + 5x)(120 − 4x) = −20x² + 200x + 12000 | Vé **125 nghìn** (x = 5); doanh thu 12 500 nghìn |
| 3 | `gk1-nguyen-du-5` | Nguyễn Du · GK1 · 0,5đ | 40 căn hộ, thuê 5 tr/tháng thì kín; **tăng** 500 nghìn thì trống 2 căn | R(x) = (5 + 0,5x)(40 − 2x) = −x² + 10x + 200 (triệu) | **7,5 tr/căn** (x = 5); doanh thu 225 tr |
| 4 | `gk1-thai-thinh-5` | Thái Thịnh · GK1 · 0,5đ | Nhà hát 150 ghế, vé 120 nghìn bán hết; **tăng** 5 nghìn thì trống thêm 3 ghế ⚠️ *đã chép lại đề đầy đủ* | R(x) = (120 + 5x)(150 − 3x) = −15x² + 390x + 18000 | Vé **185 nghìn** (x = 13); doanh thu 20 535 nghìn |
| 5 | `gk1-trung-vuong-5` | Trưng Vương · GK1 · 0,5đ | 800 m² trồng đậu/cà; 100 m² đậu cần 10 công lãi 7 tr, 100 m² cà cần 15 công lãi 9 tr, tổng công ≤ 90. Diện tích để **lãi** cao nhất | Gọi a, b là số đơn vị 100 m² đậu, cà: a + b = 8; 10a + 15b ≤ 90 ⟹ b ≤ 2; Lãi = 7a + 9b = 56 + 2b ⟹ lớn nhất khi b = 2 | Đậu **600 m²**, cà **200 m²**; lãi 60 tr |

### 1.2. Nhóm 2 — Tối ưu diện tích / chi phí vật liệu (7 câu)

| # | Mã câu | Trường / Kỳ | Đề tóm tắt | Công cụ | Đáp số |
|---|---|---|---|---|---|
| 6 | `gk1-ngo-gia-tu-6` | Ngô Gia Tự · GK1 | HCN chu vi 60 m, chiều rộng x. Tìm x để S lớn nhất | S = x(30 − x) ≤ 225 | x = **15 m**, S = 225 m² |
| 7 | `gk1-nbk-3-2` | Nguyễn Bỉnh Khiêm · GK1 | HCN chu vi 800 m, chọn kích thước để S canh tác lớn nhất | S = x(400 − x) ≤ 40 000 | **Hình vuông cạnh 200 m** |
| 8 | `ck1-dich-vong-V` | Dịch Vọng · CK1 | Tấm tôn rộng 60 cm, bẻ hai mép cao x thành máng. Tìm x để mặt cắt lớn nhất | S = x(60 − 2x) = 2·x(30 − x) ≤ 450 | x = **15 cm**, S = 450 cm² |
| 9 | `ck1-phuc-dong-V` | Phúc Đồng · CK1 | Trang chữ 384 cm², lề trên/dưới 3 cm, trái/phải 2 cm. Kích thước trang để S trang nhỏ nhất | S = 408 + 6a + 4b ≥ 408 + 2√(24·384) = 600 | **20 cm × 30 cm** |
| 10 | `gk1-co-nhue-2-4` | Cổ Nhuế 2 · GK1 | Ảnh 384 cm², viền 3 cm và 2 cm — **cùng bài với #9** | như trên | Ảnh 16 × 24 → bìa **20 × 30 cm** |
| 11 | `gk1-phu-dien-5` | Phú Diễn · GK1 | Ảnh 384 cm², lề 3 cm và 2 cm — **cùng bài với #9** | như trên | Trang **20 × 30 cm**, S = 600 cm² |
| 12 | `ck1-ngoc-lam-5` | Ngọc Lâm · CK1 | Bể hộp chữ nhật không nắp V = 400 m³, đáy dài gấp 4 lần rộng. Chiều rộng để chi phí (diện tích) nhỏ nhất | S = 4x² + 500/x + 500/x ≥ 3∛(10⁶) = 300 — **AM-GM ba số** | Rộng **5 m**, S = 300 m² |

> ⚠️ **Cảnh báo về #12:** lời giải dùng bất đẳng thức Cô-si cho **ba** số — vượt chuẩn KNTT lớp 9 (SGK chỉ nêu Cô-si hai số ở mức giới thiệu). Đây là bài của lớp chuyên/nâng cao; **không đưa vào phiếu tầng B/C**.
> ⚠️ **#9, #10, #11 là cùng một bài** xuất hiện ở ba trường khác nhau — bằng chứng rõ nhất cho thấy đây là dạng "học tủ được".

### 1.3. Nhóm 3 — Tối ưu trên tập số nguyên / có ràng buộc (3 câu)

| # | Mã câu | Trường / Kỳ | Đề tóm tắt | Đáp số |
|---|---|---|---|---|
| 13 | `gk1-van-yen-5` | Vân Yên · GK1 | 645 người; xe 35 chỗ giá 3,5 tr, xe 50 chỗ giá 5,2 tr. Thuê thế nào để chi phí ít nhất? ⚠️ *đã chép lại đề + giải* | **17 xe 35 chỗ + 1 xe 50 chỗ = 64,7 tr** |
| 14 | `ck1-trung-vuong-V` | Trưng Vương · CK1 | Vườn 20 × 15 m, hai ô vuông ở hai góc, mỗi ô ≥ 1 m², tổng 5 m²; viền hoa 30 000đ/m và 70 000đ/m. Chi phí dao động từ đâu đến đâu? | Từ **520 000đ** đến **680 000đ** |
| 15 | `gk1-dvhau-4` / `ck1-phuong-ha-dong-5` | Dịch Vọng Hậu · GK1 / Phương Hà Đông · CK1 | Vườn (bếp) hình chữ U/N, A cố định trên MN với MA = 4, AN = 1; tìm B, C để tam giác vuông ABC có S nhỏ nhất | B cách M 4 m, C cách N 1 m — **bài cực trị hình học, cần Thầy xác nhận HDC** |

### 1.4. Ghi chú kiểm chứng

| Mã câu | Sai ở bản cũ | Đã sửa thành |
|---|---|---|
| `gk1-thai-thinh-5` | Đề bị cắt giữa chừng, không có đáp án | Đề đầy đủ (tăng 5 nghìn → trống 3 ghế); đáp số **185 nghìn đồng** |
| `gk1-van-yen-5` | Ghi "xe loại 16 chỗ", thiếu giá thuê | Xe 50 chỗ, 5,2 tr/xe; đáp số **17 + 1 xe = 64,7 tr** |

---

## 2. QUY TẮC & CÁCH GIẢI MẪU CHUNG

### 2.1. Công thức tổng quát của khuôn "mỗi lần tăng a thì giảm b"

**Toàn bộ nhóm 1 là MỘT bài toán duy nhất.** Nếu:
- giá ban đầu là **p**, số lượng ban đầu là **q**;
- mỗi lần tăng giá thêm **a** thì số lượng bán được giảm **b**;
- **x** = số lần tăng giá (x ∈ ℕ),

thì doanh thu là

&nbsp;&nbsp;&nbsp;&nbsp;**R(x) = (p + ax)(q − bx) = −ab·x² + (aq − bp)·x + pq**

&nbsp;&nbsp;&nbsp;&nbsp;**R(x) đạt giá trị lớn nhất khi x = (aq − bp) / (2ab)**

**Kiểm chứng lại toàn bộ 4 bài của nhóm 1:**

| Bài | p | q | a | b | x* = (aq − bp)/(2ab) | Kết quả |
|---|---|---|---|---|---|---|
| #2 Tân Triều | 100 | 120 | 5 | 4 | (600 − 400)/40 = **5** | vé 125 nghìn ✓ |
| #3 Nguyễn Du | 5 | 40 | 0,5 | 2 | (20 − 10)/2 = **5** | 7,5 tr ✓ |
| #4 Thái Thịnh | 120 | 150 | 5 | 3 | (750 − 360)/30 = **13** | vé 185 nghìn ✓ |
| #1 Chu Văn An — **giảm** giá | lãi/chiếc 2 tr | 50 | 0,1 (giảm) | 5 (tăng SL) | đối xứng: (5·2 − 0,1·50)/(2·0,1·5) = **5** | giảm 500 000đ ✓ |

> **Bài #1 là biến thể "giảm giá":** giá **giảm** a mỗi lần thì số lượng **tăng** b mỗi lần, tức R(x) = (p − ax)(q + bx). Cùng một cấu trúc, chỉ đảo dấu — đỉnh ở x = (bp − aq)/(2ab).
>
> **Lưu ý sư phạm:** KHÔNG dạy HS công thức x* = (aq − bp)/(2ab) như một mẹo. Dạy **cách lập** R(x); công thức này chỉ dùng cho GV **soát đáp án nhanh** khi ra đề.

### 2.2. Ba công cụ tìm GTLN/GTNN được phép dùng ở lớp 9 KNTT

| Công cụ | Dạng biểu thức | Cách viết | Dùng ở bài |
|---|---|---|---|
| **C1. Hằng đẳng thức (đưa về bình phương)** | Bậc hai: −kx² + mx + n | −k(x − h)² + M ≤ M, dấu "=" khi x = h | #1–#4, #6, #7, #8 — **chủ lực** |
| **C2. Cô-si hai số** (u, v > 0) | Tổng hai số có **tích không đổi** | u + v ≥ 2√(uv), dấu "=" khi u = v | #9, #10, #11 |
| **C3. Chặn trên/dưới + duyệt số nguyên** | Ràng buộc + nghiệm nguyên | Chặn bằng bất đẳng thức rồi thử hữu hạn trường hợp | #5, #13, #14 |

**C1 là công cụ phải thành thạo** — nó phủ 7/15 bài và toàn bộ nhóm doanh thu/lợi nhuận.

### 2.3. Bài giải mẫu — khuôn chuẩn nhất

> **Đề** (`gk1-thai-thinh-5`, 0,5đ): Một nhà hát có 150 ghế, giá vé hiện tại là 120 nghìn đồng mỗi vé. Với giá vé này, tất cả các ghế đều được bán hết. Ban quản lý nhận thấy cứ mỗi lần tăng giá thêm 5 nghìn đồng thì số ghế bị bỏ trống sẽ tăng thêm 3 ghế. Hỏi mức giá vé mới là bao nhiêu để nhà hát đạt doanh thu cao nhất?

**Lời giải**

Gọi *x* là số lần tăng giá vé thêm 5 nghìn đồng, x ∈ ℕ và 0 ≤ x ≤ 50 (để số ghế bán được không âm).

Khi đó giá vé mới là 120 + 5x (nghìn đồng) và số ghế bán được là 150 − 3x (ghế).

Doanh thu của nhà hát là

&nbsp;&nbsp;&nbsp;&nbsp;R(x) = (120 + 5x)(150 − 3x) = 18 000 + 750x − 360x − 15x²
&nbsp;&nbsp;&nbsp;&nbsp;R(x) = −15x² + 390x + 18 000

Ta biến đổi

&nbsp;&nbsp;&nbsp;&nbsp;R(x) = −15(x² − 26x) + 18 000 = −15(x² − 26x + 169) + 15·169 + 18 000
&nbsp;&nbsp;&nbsp;&nbsp;R(x) = −15(x − 13)² + 20 535

Vì (x − 13)² ≥ 0 với mọi x nên −15(x − 13)² ≤ 0, do đó **R(x) ≤ 20 535** với mọi x.

Dấu "=" xảy ra khi và chỉ khi x − 13 = 0, tức x = 13 (thỏa mãn điều kiện).

Khi đó giá vé mới là 120 + 5·13 = **185 nghìn đồng**, số ghế bán được là 150 − 39 = 111 ghế.

**Vậy** nhà hát nên bán vé với giá 185 nghìn đồng, khi đó doanh thu lớn nhất là 20 535 nghìn đồng.

### 2.4. Bốn cái bẫy chết người

| Bẫy | Biểu hiện | Cách chặn |
|---|---|---|
| **Nhầm "lợi nhuận" với "doanh thu"** | Bài #1 hỏi **lợi nhuận** → phải trừ giá nhập (lãi 2 tr/chiếc), không lấy giá bán 16 tr | Bắt HS viết một dòng: *"Lợi nhuận mỗi chiếc = giá bán − giá nhập = …"* trước khi lập hàm |
| **Đặt ẩn là "giá mới" thay vì "số lần tăng"** | Hàm ra hệ số xấu, HS bỏ cuộc | Luật: **luôn gọi x là SỐ LẦN tăng/giảm**. Đến bước cuối mới quy đổi ra giá |
| **Quên điều kiện x ∈ ℕ** | Đỉnh parabol ra số lẻ (VD x = 6,5) mà HS vẫn trả lời | Nếu x* không nguyên → so sánh R tại hai số nguyên kề. *(Trong 4 bài của ngân hàng, x\* đều nguyên — nhưng phải dạy HS biết trường hợp này tồn tại)* |
| **Kết luận "x = 13" thay vì "giá vé 185 nghìn"** | Mất trọn 0,5đ vì không trả lời câu hỏi | Câu "Vậy…" phải chứa **đơn vị tiền**, không chứa chữ x |

---

## 3. BẢNG SCAFFOLDING — TỪNG BƯỚC & LÝ DO

| Bước | HS làm gì | **Vì sao phải làm bước này** | Trong bài thi? |
|---|---|---|---|
| **S0. Nhận diện** | Trả lời 2 câu: *đề hỏi lớn nhất hay nhỏ nhất?* và *đại lượng cần tối ưu được tạo bởi tích của hai thứ nào?* | Cả 15 bài đều là "tích của hai đại lượng biến thiên ngược chiều". Nhận ra cấu trúc này là 80% bài toán. | ❌ Nháp |
| **S1. Gọi ẩn = SỐ LẦN thay đổi** | *"Gọi x là số lần tăng giá thêm 5 nghìn đồng, x ∈ ℕ, 0 ≤ x ≤ 50."* | Nếu gọi ẩn là giá mới thì hệ số phân số, HS mất phương hướng. Gọi theo "số lần" giữ mọi hệ số nguyên. | ✅ Có |
| **S2. Lập BẢNG hai dòng** | Dòng 1: giá mới = p + ax. Dòng 2: số lượng = q − bx. | Tách phần "tăng" và phần "giảm" thành hai dòng riêng chống nhầm dấu — lỗi phổ biến nhất là viết q + bx. | ✅ Có (được tính vào điểm lập biểu thức) |
| **S3. Viết hàm mục tiêu** | R(x) = (p + ax)(q − bx), **khai triển và thu gọn**. | Phải khai triển thì bước hằng đẳng thức mới làm được. Đây là chỗ HS hay dừng lại. | ✅ Có — **nửa số điểm nằm ở đây** |
| **S4. Đưa về dạng −k(x − h)² + M** | Rút hệ số −k, thêm bớt để có hằng đẳng thức. | Đây là kỹ thuật **duy nhất** lớp 9 có để tìm GTLN của tam thức (chưa học đỉnh parabol, chưa học đạo hàm). | ✅ Có |
| **S5. Lập luận chặn** | *"Vì (x − h)² ≥ 0 nên R(x) ≤ M."* | **Bắt buộc viết ra.** Không có câu này thì bài chỉ là biến đổi đại số, chưa chứng minh được điều gì — giám khảo trừ điểm. | ✅ Có — dòng ăn điểm quan trọng |
| **S6. Dấu "=" xảy ra khi nào** | *"Dấu = xảy ra ⟺ x = h (thỏa mãn điều kiện)."* | Không chỉ ra dấu "=" thì chưa khẳng định M **đạt được**, mới chỉ là chặn trên. Đây là lỗi lập luận, không phải lỗi tính. | ✅ Có |
| **S7. Quy đổi & trả lời** | Từ x = h tính ra **giá / kích thước / diện tích** mà đề hỏi. | Đề không bao giờ hỏi x. Xem bẫy #4 ở trên. | ✅ Có |

**Trả lời trực tiếp câu hỏi "có giải thích được trong các bài thi không?"**

→ **Có — nhưng cần nói rõ giới hạn.** Câu này chỉ 0,5đ và **không tách barem thành phần** ở phần lớn HDC (chấm "đúng thì cho, sai thì không"). Vì vậy lập luận với HS phải khác dạng lập hệ:

- Với **lập hệ phương trình**: "viết được bước nào ăn điểm bước đó".
- Với **tối ưu**: "làm được thì ăn trọn 0,5đ, làm dở dang gần như không có điểm" → nên **chỉ đầu tư khi đã chắc 9,0đ còn lại**.

Đây cũng là căn cứ để **cắt dạng này khỏi phiếu tầng C**: chi phí thời gian ~14 phút cho 0,5đ, trong khi cùng 14 phút luyện lập hệ thì ăn chắc 1,0–2,0đ.

### 3.1. Lộ trình luyện (chỉ dành cho lớp A/B)

| Buổi | Nội dung | Bài lấy từ ngân hàng |
|---|---|---|
| 1 | Kỹ thuật nền: đưa −kx² + mx + n về −k(x−h)² + M | Bài tập thuần đại số, chưa có lời văn |
| 2 | Hình học đơn giản (tích hai số có tổng không đổi) | #6, #7, #8 |
| 3 | **Doanh thu — khuôn "mỗi lần tăng a giảm b"** | #2, #3, #4 |
| 4 | **Lợi nhuận** (thêm bước trừ giá vốn) | #1 |
| 5 | Cô-si hai số (tổng hai số có tích không đổi) | #9 / #10 / #11 |
| 6 | Ràng buộc + nghiệm nguyên | #5, #13 |

---

## 4. CHECKLIST & RUBRIC

### 4.1. Checklist HS tự kiểm

- [ ] Tôi gọi ẩn là **số lần** tăng/giảm (không phải giá mới), có **điều kiện x ∈ ℕ** và chặn trên.
- [ ] Tôi phân biệt được đề hỏi **doanh thu** (giá bán × số lượng) hay **lợi nhuận** (lãi mỗi đơn vị × số lượng).
- [ ] Dòng "số lượng" của tôi có dấu **trừ** (bán ít đi khi tăng giá).
- [ ] Tôi đã **khai triển và thu gọn** trước khi làm hằng đẳng thức.
- [ ] Tôi có dòng **"Vì (x − h)² ≥ 0 nên R(x) ≤ M"**.
- [ ] Tôi có dòng **"Dấu = xảy ra khi x = …"** và đã đối chiếu điều kiện.
- [ ] Câu "Vậy…" của tôi trả lời bằng **giá tiền / kích thước**, không phải bằng x.
- [ ] Tôi đã thử lại: thay x = h − 1 và x = h + 1 xem R có nhỏ hơn M không.

### 4.2. Rubric chấm — thang 4 mức

| Tiêu chí | Mức 1 — Chưa đạt | Mức 2 — Đạt | Mức 3 — Khá | Mức 4 — Tốt |
|---|---|---|---|---|
| **T1. Nhận diện cấu trúc** | Không thấy đây là bài tối ưu | Nhận ra khi GV nhắc | Tự nhận ra ở mô-típ quen | Tự nhận ra ở mô-típ lạ (chi phí, diện tích, số nguyên) |
| **T2. Đặt ẩn** | Không đặt được / đặt sai đối tượng | Đặt là "số lần" nhưng thiếu điều kiện | Đủ ẩn + điều kiện x ∈ ℕ | Đủ, và chặn được cả cận trên của x |
| **T3. Lập hàm mục tiêu** | Không lập được | Lập được với bảng gợi ý 2 dòng | Tự lập, khai triển đúng | Tự lập cả ở bài **lợi nhuận** (có bước trừ giá vốn) |
| **T4. Kỹ thuật hằng đẳng thức** | Không đưa được về bình phương | Làm được với hệ số k = 1 | Làm được với k bất kỳ | Làm gọn, không sai dấu, kể cả hệ số thập phân |
| **T5. Lập luận chặn + dấu "="** | Thiếu cả hai | Có một trong hai | Có đủ hai dòng | Có đủ, và **đối chiếu điều kiện** ở dấu "=" |
| **T6. Quy đổi & kết luận** | Trả lời bằng x | Trả lời đúng đại lượng nhưng thiếu đơn vị | Đủ, đúng đơn vị | Đủ, kèm giá trị tối ưu (doanh thu bao nhiêu) |

**Ngưỡng kết luận "HS làm được dạng này":**
- **Đạt chuẩn** = T2, T3, T4, T5 đều ở mức ≥ 3 trên **hai** bài khuôn "mỗi lần tăng a giảm b" khác nhau, trong ≤ 12 phút/bài.
- **Chưa nên luyện dạng này** nếu HS chưa vững kỹ thuật đưa tam thức về dạng bình phương (T4 ≤ 2) — luyện T4 riêng bằng bài đại số thuần trước.

### 4.3. Bộ 3 câu kiểm tra nhanh (20 phút)

| Câu | Lấy từ | Kiểm tra |
|---|---|---|
| 1 | `gk1-ngo-gia-tu-6` (HCN chu vi 60 m) | T4 thuần — không có lời văn phức tạp |
| 2 | `gk1-thai-thinh-5` (nhà hát 150 ghế) | T1 → T6 khuôn chuẩn, x* = 13 (không phải 5 như 3 bài kia — chống học vẹt) |
| 3 | `ck1-chu-van-an-V` (điện thoại — **lợi nhuận**) | T3 mức 4: có bẫy giá vốn |

> HS làm đúng câu 1 và 2 → đạt. Đúng cả câu 3 → vững, đủ sức ăn câu 0,5đ cuối đề.
