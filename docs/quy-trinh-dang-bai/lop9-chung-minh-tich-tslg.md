# Lớp 9 — CHỨNG MINH TÍCH / HỆ THỨC CÓ TỈ SỐ LƯỢNG GIÁC

> Người 1: **ThaiTD** · Người 2: AnDV · Deadline 22/8
> Nguồn dữ liệu: `inputs/refs/de-thi/lop-9/exams/` — mã dạng `HH-TSLG-CM` (chương IV) và `HH-HETHUC-DONGDANG` (chương IX, khuôn Câu IV.2b đề Vào 10).

---

## 0. Vị trí của dạng trong đề thi

| Kỳ thi | Tần suất | Điểm | Vị trí |
|---|---|---|---|
| Giữa kì I | **8/10 đề (80%)** — 17 câu | ~1,78đ/đề | Ý b của bài hình (VD) + ý c (VDC) |
| Cuối kì I | 1/11 đề | 0,5đ | — |
| Cuối kì II | 3/10 đề | 1,0–1,5đ | Bài IV.2b — chuyển sang khuôn đường tròn |
| **Vào 10** | **3/3 đề Sở (100%)** | **1,5đ** | **Câu IV.2 ý b — ý đắt nhất đề** |

**Kết luận nghiệp vụ:** dạng này có **hai mặt**:
- **Mặt chương IV (GK1):** hệ thức có sin/cos trong tam giác vuông — *HN = AB·sin²B*.
- **Mặt chương IX (Vào 10):** hệ thức **dạng tích** trong bài đường tròn — *AB·AC = AE·AS*.

Hai mặt dùng **chung một kỹ thuật lõi**: đưa hệ thức về tỉ số → tìm hai tam giác đồng dạng → nhân chéo. Vì vậy nên dạy như **một dạng duy nhất**, mặt chương IV trước (làm bàn đạp), mặt Vào 10 sau.

---

## 1. LIỆT KÊ TOÀN BỘ CÂU TRONG NGÂN HÀNG ĐỀ

### 1.1. Nhóm A — Hệ thức có tỉ số lượng giác trong tam giác vuông (chương IV, 10 câu cốt lõi)

Cấu hình lặp lại: **ΔABC vuông tại A, đường cao AH; M, N (hoặc E, F) là hình chiếu của H trên AB, AC.**

| # | Mã câu | Trường / Kỳ | Điểm | Hệ thức phải chứng minh | Trạng thái |
|---|---|---|---|---|---|
| 1 | `gk1-trung-vuong-4-2` | Trưng Vương · GK1 | 1,5 | ΔAMN ∽ ΔACB và **HN = AB·sin²B** | ✅ đã kiểm chứng |
| 2 | `gk1-van-yen-4b` | Vân Yên · GK1 | 1,0 | **HN·AC = HA·HC** và **HN = AB·sin²B** | ⚠️ **đã sửa lại đề** |
| 3 | `gk1-nbk-5b` | Nguyễn Bỉnh Khiêm · GK1 | 1,0 | **sin²B = CF/AC** | ✅ đã kiểm chứng |
| 4 | `gk1-ngo-gia-tu-5b` | Ngô Gia Tự · GK1 | 1,0 | ΔAMB ∽ ΔIMA và **sin²(ABM) = IM/BM** (I là hình chiếu của A trên **BM**) | ⚠️ **đã sửa lại đề** |
| 5 | `gk1-nguyen-du-4b` | Nguyễn Du · GK1 | 0,75 | AM/BM = HM/AM và **cos²(AMB) = HM/BM** | ✅ đã kiểm chứng |
| 6 | `gk1-phu-dien-4-2b` | Phú Diễn · GK1 | 1,0 | ΔBHA ∽ ΔBAC và **KH = KC·sin(BAH)** (AK là phân giác góc HAC) | ✅ đã kiểm chứng |
| 7 | `gk1-dvhau-3-2b` | Dịch Vọng Hậu · GK1 | 1,0 | **AE·AB = AH²** và ΔABC ∽ ΔAFE | ✅ đã kiểm chứng |
| 8 | `gk1-co-nhue-2-3-2b` | Cổ Nhuế 2 · GK1 | 1,0 | **ME·MN = MF·MP** và góc MEF = góc MPN | ✅ đã kiểm chứng |
| 9 | `gk1-dvhau-3-2c` | Dịch Vọng Hậu · GK1 | 1,0 | K là trung điểm BC và **cos³B·sinB = IF/BC** | ✅ đã kiểm chứng (VDC) |
| 10 | `gk1-co-nhue-2-3-2c` | Cổ Nhuế 2 · GK1 | 1,0 | **sin(MQN)·cos(MNP) = HI/QP** | ⚠️ chưa có HDC — cần Thầy xác nhận |

### 1.2. Nhóm B — Ý c vận dụng cao đi kèm (7 câu, cùng bài hình nhưng chuyển sang thẳng hàng / vuông góc)

| # | Mã câu | Trường | Điểm | Yêu cầu |
|---|---|---|---|---|
| 11 | `gk1-trung-vuong-4-1` | Trưng Vương | 1,0 | A, M, H, N cùng thuộc một đường tròn |
| 12 | `gk1-trung-vuong-4-3` | Trưng Vương | 0,5 | AI ⊥ CK |
| 13 | `gk1-ngo-gia-tu-5c` | Ngô Gia Tự | 0,5 | M, K, N thẳng hàng |
| 14 | `gk1-nguyen-du-4c` | Nguyễn Du | 0,5 | A, H, K thẳng hàng |
| 15 | `gk1-van-yen-4c` | Vân Yên | 0,5 | M, I, N thẳng hàng ⚠️ *đã chép lại đề đầy đủ* |
| 16 | `gk1-phu-dien-4-2c` | Phú Diễn | 0,5 | CM ⊥ MP |
| 17 | `ck1-phuong-ha-dong-5` / `gk1-dvhau-4` | Phương Hà Đông / DVH | 0,5 | Cực trị hình học (diện tích tam giác vuông nhỏ nhất) |

> Nhóm B **không phải trọng tâm dòng phân công này** (không có tỉ số lượng giác trong kết luận) nhưng luôn đi kèm nhóm A trong cùng một bài hình — liệt kê để biết toàn cảnh bài 2,5đ.

### 1.3. Nhóm C — Khuôn Câu IV.2b đề Vào 10: hệ thức **dạng tích** trong đường tròn (6 câu)

| # | Mã câu | Nguồn | Điểm | Hệ thức | Cặp tam giác đồng dạng |
|---|---|---|---|---|---|
| 18 | `v10-so-2025-IV2b` | **Sở Hà Nội 2025 (chính thức)** | 1,5 | **AB·AC = AE·AS** | ΔABE ∽ ΔASC (góc A chung + góc nội tiếp cùng chắn cung) |
| 19 | `v10-so-2026-IV2b` | **Sở Hà Nội 2026 (chính thức)** | 1,5 | **AE·BC = EH·AB** | Hai tam giác vuông đồng dạng (g.g) |
| 20 | `v10-so-minh-hoa-IV2b` | **Sở Hà Nội (minh họa)** | 1,5 | **ME·MH = BE·HC** | Góc nội tiếp cùng chắn cung của đường tròn đường kính MB |
| 21 | `ck2-dai-ang-IV2b` | Đại Áng · CK2 | 1,5 | **AB·AC = AD·AT** | ΔABD ∽ ΔATC (góc chắn nửa đường tròn + cùng chắn cung AC) — 🔑 **bản mẫu đầy đủ nhất** |
| 22 | `ck2-mai-dich-IV2b` | Mai Dịch · CK2 | 1,0 | ΔOIA ∽ ΔOAM và **OH·OK = R²** | Góc O chung + hai góc vuông — **dễ nhất, dạy trước** |
| 23 | `ck2-chu-van-an-IV2b` | Chu Văn An · CK2 | 1,5 | ΔNMC ∽ ΔABC (phát biểu thẳng dạng đồng dạng) | Tứ giác nội tiếp chuyển góc |

> **3/3 đề chính thức của Sở đều có vế hệ thức tích ở Câu IV.2b.** Đây là bằng chứng mạnh nhất cho việc luyện dạng này thành khuôn.

### 1.4. Ghi chú kiểm chứng — 2 câu trong ngân hàng chép sai, đã sửa

| Mã câu | Bản cũ (sai) | Bản đúng (đối chiếu ảnh PDF gốc) |
|---|---|---|
| `gk1-van-yen-4b` | "HM·AC = HA·HN và **HN = AB·sin³B**" | **HN·AC = HA·HC** và **HN = AB·sin²B** |
| `gk1-ngo-gia-tu-5b` | "I là hình chiếu của A trên **BC**; ΔABC ∽ ΔIMA; sin²(ABC) = IM/**BC**" | I là hình chiếu của A trên **BM**; **ΔAMB ∽ ΔIMA**; **sin²(ABM) = IM/BM** |

**Cách phát hiện:** đặt AB = c, AC = b, BC = a rồi tính hai vế bằng a, b, c.
Với bản cũ của Vân Yên: HN = b²c/a² nhưng AB·sin³B = b³c/a³ — **không bằng nhau**, nên đề chép sai.
Với bản cũ của Ngô Gia Tự: nếu I trên BC thì MI = MA (trung tuyến ứng với cạnh huyền của ΔAIC) nên ΔIMA **cân**, không thể đồng dạng với tam giác vuông ABC.

> 📌 **Đây chính là "vũ khí kiểm tra" nên dạy cho cả GV lẫn HS khá:** mọi hệ thức trong dạng này đều **kiểm chứng được bằng a, b, c** trước khi đi chứng minh hình học. Xem §2.3.

---

## 2. QUY TẮC & CÁCH GIẢI MẪU CHUNG

### 2.1. Kho công thức nền (HS phải thuộc nằm lòng trước khi vào dạng này)

Với ΔABC vuông tại A, đường cao AH, đặt BC = a, AC = b, AB = c, AH = h:

| # | Hệ thức | Tên gọi | Dùng để |
|---|---|---|---|
| H1 | b² = a·CH và c² = a·BH | Cạnh góc vuông – hình chiếu | Đổi **bình phương** thành **tích** |
| H2 | h² = BH·CH | Đường cao | Đổi tích hai hình chiếu |
| H3 | a·h = b·c | Diện tích hai cách | Đổi tích chéo |
| H4 | 1/h² = 1/b² + 1/c² | Nghịch đảo | Hiếm dùng trong dạng này |
| H5 | b = a·sinB = a·cosC = c·tanB | Cạnh và góc | **Cầu nối cạnh ⟷ góc** |

**Bảng quy đổi góc phụ nhau (dùng liên tục):**

&nbsp;&nbsp;&nbsp;&nbsp;sin B = cos C = b/a &nbsp;&nbsp;·&nbsp;&nbsp; cos B = sin C = c/a &nbsp;&nbsp;·&nbsp;&nbsp; tan B = cot C = b/c

**Và một hệ quả cực kỳ hay dùng, xuất hiện ở #1, #2, #3, #4:**

&nbsp;&nbsp;&nbsp;&nbsp;**AM = AB·sin²B** &nbsp;&nbsp;và&nbsp;&nbsp; **AN = AC·sin²C**
&nbsp;&nbsp;&nbsp;&nbsp;(với M, N là hình chiếu của H trên AB, AC — vì AM·AB = AH² và AH = AB·sinB)

### 2.2. Quy trình 5 bước — dùng chung cho cả chương IV và Vào 10

```
B1. ĐỌC KẾT LUẬN NGƯỢC : Nhìn hệ thức phải chứng minh, KHÔNG nhìn hình vội.
B2. ĐƯA VỀ TỈ SỐ       : Tích = tích  ⟶  tỉ số = tỉ số   (chia chéo)
                          Có sin/cos   ⟶  thay bằng tỉ số hai cạnh (dùng H5)
B3. ĐỌC TÊN 2 TAM GIÁC : Bốn đoạn trong hai tỉ số nằm trong hai tam giác nào?
B4. CHỨNG MINH ĐỒNG DẠNG: Chỉ ra 2 cặp góc bằng nhau (g.g).
B5. NHÂN CHÉO & KẾT     : Từ tỉ số đồng dạng, nhân chéo ra đúng hệ thức đề cho.
```

**Nguyên tắc lõi — "ĐI NGƯỢC":** dạng này **không giải xuôi được**. HS nhìn hình rồi loay hoay sẽ không bao giờ ra. Phải xuất phát từ **kết luận**, biến đổi nó về tỉ số, rồi mới quay lại hình tìm tam giác.

**Mẹo đặt tên tam giác ở B3 (dạy thành thao tác máy móc):**
Từ tỉ số **AB/AE = AS/AC**, đọc: tử trái + mẫu phải + đỉnh chung = tam giác 1 (ΔABE... ) — thực tế cách chắc chắn nhất là:

> Viết tỉ số sao cho **hai đoạn cùng xuất phát từ một điểm** đứng cùng một vế.
> AB·AC = AE·AS ⟺ AB/AE = AS/AC ⟹ hai tam giác là **ΔABE** và **ΔASC** (đều có đỉnh A).

### 2.3. Kiểm chứng bằng a, b, c — công cụ tự soát (GV bắt buộc, HS khá nên biết)

Trước khi chứng minh, **thay mọi đoạn thẳng bằng biểu thức của a, b, c** rồi so hai vế:

| Đoạn | Biểu thức theo a, b, c |
|---|---|
| AH | bc/a |
| BH | c²/a &nbsp;&nbsp;·&nbsp;&nbsp; CH = b²/a |
| AM (hình chiếu H trên AB) | b²c/a² &nbsp;&nbsp;·&nbsp;&nbsp; AN = bc²/a² |
| HN (= AM) | b²c/a² &nbsp;&nbsp;·&nbsp;&nbsp; HM (= AN) = bc²/a² |
| MN (= AH) | bc/a |
| sin B | b/a &nbsp;&nbsp;·&nbsp;&nbsp; cos B = c/a |

Ví dụ soát #1: HN = b²c/a²; AB·sin²B = c·(b/a)² = b²c/a². **Bằng nhau ⟹ đề đúng.**
Ví dụ soát #9: IF = AF²/EF = (bc²/a²)²/(bc/a) = bc³/a³; cos³B·sinB·BC = (c/a)³·(b/a)·a = bc³/a³. **Bằng nhau ⟹ đề đúng.**

### 2.4. Bài giải mẫu 1 — mặt chương IV (`gk1-trung-vuong-4-2`, 1,5đ)

> **Đề:** Cho tam giác ABC vuông tại A (AB < AC), đường cao AH (H ∈ BC). M, N lần lượt là chân đường vuông góc hạ từ H xuống AB, AC. Chứng minh ΔAMN ∽ ΔACB và HN = AB·sin²B.

**Lời giải**

*Ý 1 — Chứng minh ΔAMN ∽ ΔACB.*

Xét ΔAHB vuông tại H có HM ⊥ AB tại M, theo hệ thức lượng trong tam giác vuông:

&nbsp;&nbsp;&nbsp;&nbsp;AM·AB = AH²&nbsp;&nbsp;(1)

Xét ΔAHC vuông tại H có HN ⊥ AC tại N, theo hệ thức lượng trong tam giác vuông:

&nbsp;&nbsp;&nbsp;&nbsp;AN·AC = AH²&nbsp;&nbsp;(2)

Từ (1) và (2) suy ra AM·AB = AN·AC, do đó AM/AC = AN/AB.

Xét ΔAMN và ΔACB có:
&nbsp;&nbsp;&nbsp;&nbsp;góc A chung;
&nbsp;&nbsp;&nbsp;&nbsp;AM/AC = AN/AB (chứng minh trên).

Vậy **ΔAMN ∽ ΔACB (c.g.c)**.

*Ý 2 — Chứng minh HN = AB·sin²B.*

Tứ giác AMHN có ba góc vuông (tại A, M, N) nên là hình chữ nhật, suy ra **HN = AM**.

Trong ΔAHB vuông tại H có góc B: AH = AB·sin B.

Từ (1): AM = AH²/AB = (AB·sin B)²/AB = AB·sin²B.

**Vậy** HN = AM = AB·sin²B.&nbsp;&nbsp;∎

### 2.5. Bài giải mẫu 2 — mặt Vào 10 (`ck2-dai-ang-IV2b`, khuôn Câu IV.2b, 1,5đ)

> **Đề:** … Kẻ đường kính AT của đường tròn (O). Chứng minh rằng AB·AC = AD·AT.

**Lời giải theo đúng 5 bước**

*B2 — Đưa tích về tỉ số:*&nbsp;&nbsp; AB·AC = AD·AT ⟺ **AB/AD = AT/AC**

*B3 — Đọc tên hai tam giác:*&nbsp;&nbsp; AB, AD cùng xuất phát từ A → ΔABD; AT, AC cùng xuất phát từ A → ΔATC.

*B4 — Chứng minh ΔABD ∽ ΔATC:*

Xét ΔABD và ΔATC có:
&nbsp;&nbsp;&nbsp;&nbsp;góc ADB = góc ACT = 90° (góc nội tiếp chắn nửa đường tròn);
&nbsp;&nbsp;&nbsp;&nbsp;góc ABD = góc ATC (hai góc nội tiếp cùng chắn cung AC).

Vậy ΔABD ∽ ΔATC (g.g).

*B5 — Nhân chéo:*&nbsp;&nbsp; Suy ra AB/AT = AD/AC, do đó **AB·AC = AD·AT**.&nbsp;&nbsp;∎

> **Khuôn hai cặp góc của Câu IV.2b lặp lại ở cả 6 bài nhóm C — chỉ có 3 nguồn góc:**
> 1. Góc nội tiếp **chắn nửa đường tròn** = 90°;
> 2. Hai góc nội tiếp **cùng chắn một cung**;
> 3. Góc **chung** của hai tam giác (hoặc góc đối đỉnh).
>
> HS chỉ cần tìm được **hai** trong ba nguồn này là xong ý 1,5đ.

### 2.6. Bốn cái bẫy

| Bẫy | Biểu hiện | Cách chặn |
|---|---|---|
| **Giải xuôi từ hình** | HS vẽ hình rồi ngồi nhìn, 10 phút không viết được dòng nào | Bắt buộc dòng đầu tiên là biến đổi **kết luận**, chưa động đến hình |
| **Viết tỉ số sai thứ tự** | AB/AC = AD/AT (sai) thay vì AB/AD = AT/AC | Luật: hai đoạn **cùng gốc** phải ở **cùng một vế** |
| **Ghi đồng dạng sai thứ tự đỉnh** | "ΔABD ∽ ΔACT" thay vì "ΔABD ∽ ΔATC" | Đỉnh tương ứng phải khớp với cặp góc đã chứng minh — đọc lại một lượt trước khi nhân chéo |
| **Nhầm sin B với sin C** | HN = AB·sin²C | Viết ra bảng góc phụ (sin B = cos C) ở góc nháp mỗi bài |

---

## 3. BẢNG SCAFFOLDING — TỪNG BƯỚC & LÝ DO

| Bước | HS làm gì | **Vì sao phải làm bước này** | Trong bài thi? |
|---|---|---|---|
| **S0. Vẽ hình đúng** | Vẽ theo thứ tự đề cho, ký hiệu vuông góc, ký hiệu bằng nhau | Hình sai thì mọi lập luận sau vô nghĩa. HDC luôn tách riêng dòng này. | ✅ **Có — 0,25đ**, có HDC ghi rõ *"Vẽ hình đúng đến câu a) — 0,25"* |
| **S1. Chép kết luận cần chứng minh** | Viết lại hệ thức xuống dưới, chưa làm gì | Tách "cái phải chứng minh" khỏi "cái đã cho". HS yếu hay lẫn hai thứ và "chứng minh vòng tròn". | ❌ Nháp (nhưng nên khuyến khích viết ra) |
| **S2. Biến đổi tương đương về tỉ số** | Tích = tích ⟶ tỉ số = tỉ số. Có sin/cos ⟶ thay bằng tỉ số hai cạnh. | **Đây là bước then chốt.** Không có nó, HS không biết phải tìm tam giác nào. Đồng thời viết bằng dấu ⟺ cho thấy phép biến đổi hợp lệ. | ✅ **Có** — nhiều HDC cho 0,25–0,5đ cho riêng dòng "⟺ tỉ số" |
| **S3. Gọi tên hai tam giác** | *"Xét ΔABD và ΔATC có:"* | Buộc HS cam kết một hướng cụ thể thay vì thử mò. Nếu chọn sai, phát hiện ngay ở S4 và đổi được. | ✅ Có (gộp với S4) |
| **S4. Chỉ ra hai cặp góc** | Mỗi cặp góc **một dòng riêng**, kèm **căn cứ trong ngoặc** | Căn cứ ("góc nội tiếp cùng chắn cung AC") **chính là thứ được chấm điểm**, không phải kết luận. Bỏ căn cứ = mất điểm dù đúng. | ✅ **Có — 0,5đ đến 1,0đ**, phần đắt nhất |
| **S5. Kết luận đồng dạng** | *"Vậy ΔABD ∽ ΔATC (g.g)"* — nhớ ghi trường hợp | Ghi rõ (g.g)/(c.g.c) là quy ước trình bày bắt buộc ở THCS. | ✅ Có |
| **S6. Nhân chéo về đúng hệ thức đề** | Viết tỉ số đồng dạng → nhân chéo → hệ thức ban đầu | Nhiều HS dừng ở "đồng dạng" mà quên quay về hệ thức — mất 0,25–0,5đ cuối. | ✅ **Có — 0,25đ đến 0,5đ** |
| **S7. Với ý có sin/cos: quy đổi lần cuối** | Thay tỉ số cạnh về sin/cos bằng bảng góc phụ | Đề hỏi hệ thức có sin, đáp án phải có sin. | ✅ Có |

**Trả lời trực tiếp câu hỏi "có giải thích được trong các bài thi không?"**

→ **Có, và đây là dạng giải thích được rõ ràng nhất trong ba dạng lớp 9 được phân công.** Lý do:

1. **Barem tách theo ý — có bằng chứng từ HDC gốc.** Trích nguyên văn barem của ba đề GK1 (nguồn: HDC gốc kèm đề):

   | Câu | Dòng barem | Điểm |
   |---|---|---|
   | `gk1-trung-vuong-4-2` (1,5đ) | "Chỉ ra AM/AC = AN/AB; góc BAC chung ⟹ ΔAMN ∽ ΔACB" | 0,75 |
   | | "Dùng AH = MN, AM = HN ⟹ HN = AB·sin²B" | 0,75 |
   | `gk1-nguyen-du-4b` (0,75đ) | "Chứng minh AM/BM = HM/AM" | 0,25 |
   | | "Suy ra cos²(AMB) = HM/BM" | 0,5 |
   | `gk1-ngo-gia-tu-5b` (1,0đ) | "Chứng minh ΔAMB ∽ ΔIMA (g.g)" | 0,5 |
   | | "Suy ra AM² = IM·BM rồi kết luận sin²(ABM) = IM/BM" | 0,5 |

   → **HS chỉ chứng minh được phần đồng dạng, chưa ra hệ thức, vẫn ăn 50% điểm ý.** Cộng thêm 0,25đ vẽ hình (HDC Ngô Gia Tự ghi rõ *"Vẽ hình đúng đến câu a) — 0,25"*) thì HS trung bình vẫn có phần điểm chắc chắn ở bài hình.

   *Lưu ý:* với Câu IV.2b của đề Sở Vào 10 (1,5đ), HDC chính thức **không tách** hai vế của ý b — nên ở đó phải làm trọn ý mới ăn đủ điểm. Vì vậy khuôn luyện phải nhắm **làm xong**, không nhắm "ăn điểm thành phần".
2. **Khuôn lặp 3/3 đề Sở.** Không phải "may thì trúng" — cấu trúc Câu IV.2b của Hà Nội ổn định qua đề 2025, 2026 và đề minh họa.
3. **Có công cụ tự kiểm chứng** (§2.3) — HS khá tự biết mình làm đúng hay sai trước khi nộp bài.

Điểm phải nói thật với HS: **ý c (nhóm B) thì không giải thích được thành khuôn** — mỗi bài một cách, phụ thuộc ý tưởng. Đó là 0,5đ dành cho HS giỏi, không phải mục tiêu đại trà.

### 3.1. Lộ trình luyện

| Buổi | Nội dung | Bài lấy từ ngân hàng |
|---|---|---|
| 1 | Thuộc 5 hệ thức lượng + bảng góc phụ. Bài tập điền khuyết, chưa chứng minh | Bài nền tự soạn |
| 2 | **Tích ⟶ tỉ số** thuần đại số (chưa có hình): cho AB·AC = AD·AT, viết mọi tỉ số tương đương | Bài nền tự soạn |
| 3 | Cấu hình "đường cao + hai hình chiếu": AM·AB = AH², AMHN hình chữ nhật | #7, #8 |
| 4 | **Hệ thức có sin/cos** — khuôn AM = AB·sin²B | #1, #2, #3 |
| 5 | Biến thể "trung điểm + hình chiếu" | #4, #5 |
| 6 | **Khuôn Câu IV.2b Vào 10** — góc chung + hai góc vuông (dễ nhất) | #22 |
| 7 | Khuôn Câu IV.2b — góc nội tiếp cùng chắn cung | #21, #18, #19, #20 |
| 8 | (Lớp A/B) Ý c vận dụng cao | #9, #12, #13, #14 |

---

## 4. CHECKLIST & RUBRIC

### 4.1. Checklist HS tự kiểm

- [ ] Tôi đã **vẽ hình** đúng thứ tự đề, có ký hiệu góc vuông.
- [ ] Dòng đầu tiên của bài là **biến đổi kết luận về tỉ số**, không phải ngắm hình.
- [ ] Trong tỉ số của tôi, hai đoạn **cùng gốc** nằm cùng một vế.
- [ ] Tôi đã thay hết sin/cos thành **tỉ số hai cạnh** (hoặc ngược lại) trước khi tìm tam giác.
- [ ] Mỗi cặp góc bằng nhau của tôi đều có **căn cứ ghi trong ngoặc**.
- [ ] Tôi ghi rõ **trường hợp đồng dạng** (g.g) hay (c.g.c).
- [ ] Thứ tự đỉnh trong "ΔXYZ ∽ ΔX'Y'Z'" **khớp** với các cặp góc tôi đã chứng minh.
- [ ] Tôi đã **nhân chéo quay về đúng hệ thức đề cho**, không dừng ở "hai tam giác đồng dạng".
- [ ] (HS khá) Tôi đã thử kiểm chứng bằng a, b, c.

### 4.2. Rubric chấm — thang 4 mức

| Tiêu chí | Mức 1 — Chưa đạt | Mức 2 — Đạt | Mức 3 — Khá | Mức 4 — Tốt |
|---|---|---|---|---|
| **T1. Vẽ hình** | Sai cấu hình | Đúng nhưng thiếu ký hiệu | Đúng, đủ ký hiệu | Đúng, và **vẽ đúng cả điểm phụ của ý c** |
| **T2. Đưa hệ thức về tỉ số** | Không làm được | Làm được khi GV viết sẵn dạng tích | Tự làm đúng thứ tự "cùng gốc" | Tự làm cả khi hệ thức có sin/cos hoặc bình phương |
| **T3. Xác định hai tam giác** | Không chọn được | Chọn được sau gợi ý | Tự chọn đúng ở cấu hình quen | Tự chọn đúng ở cấu hình lạ (đường tròn) |
| **T4. Nêu căn cứ hai cặp góc** | Không nêu / nêu sai | Nêu đúng 1 cặp | Nêu đúng 2 cặp có căn cứ | Nêu đúng, gọn, và biết **chuyển góc** qua tứ giác nội tiếp |
| **T5. Nhân chéo & kết luận** | Dừng ở đồng dạng | Nhân chéo nhưng sai thứ tự đỉnh | Đúng hoàn toàn | Đúng, kèm câu kết luận đúng dạng đề hỏi |
| **T6. Trình bày hình học** | Không có "Xét… có…" | Có nhưng thiếu căn cứ | Đủ cấu trúc "Xét – có – vậy" | Chuẩn mực, dùng đúng thuật ngữ (∽, ⊥, chắn cung) |

**Ngưỡng kết luận "HS làm được dạng này":**
- **Đạt tối thiểu** = T1, T2, T4 ở mức ≥ 2 → ăn được ~0,5/1,5đ Câu IV.2b (điểm hình vẽ + một cặp góc).
- **Đạt chuẩn Vào 10** = T2, T3, T4, T5 đều ≥ 3 trên **hai** cấu hình khác nhau (một chương IV, một đường tròn), trong ≤ 12 phút.
- **Vững** = T3 và T4 ở mức 4 → tự xử lý được cấu hình chưa gặp.

### 4.3. Bộ 3 câu kiểm tra nhanh (25 phút)

| Câu | Lấy từ | Kiểm tra |
|---|---|---|
| 1 | `gk1-dvhau-3-2b` (AE·AB = AH² và ΔABC ∽ ΔAFE) | T2, T3 ở cấu hình đường cao — nền tảng |
| 2 | `gk1-trung-vuong-4-2` (HN = AB·sin²B) | T2 mức 4: có sin trong kết luận |
| 3 | `v10-so-2025-IV2b` (AB·AC = AE·AS — **đề Sở 2025**) | Toàn bộ khuôn Câu IV.2b |

> HS làm đúng câu 1 và 2 → nắm chương IV. Đúng câu 3 → **ăn được 1,5đ đắt nhất của đề Vào 10**.
