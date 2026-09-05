# Quy trình soạn phiếu **tầng B**

> Nguồn sự thật cho phiếu tầng B. Bổ trợ [AGENTS.md](AGENTS.md) (gốc quy trình),
> [HUONG-DAN-PHAN-TANG-LOP.md](HUONG-DAN-PHAN-TANG-LOP.md) (phân tầng & chuẩn giờ) và
> [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md) (luật soạn chi tiết).
> Tầng C có quy trình riêng ở HUONG-DAN-PHAN-TANG-LOP §5 — mục §7 dưới đây nói rõ
> chỗ nào bê nguyên từ C sang, chỗ nào phải làm khác.

**HS tầng B = trung bình–khá.** Khác tầng C ở một chỗ duy nhất nhưng quyết định tất cả:
tầng C chỉ cần *làm được một phần Vận dụng*, còn **tầng B phải đi tới tận câu cuối đề**.

---

## 1. ĐÍCH CỦA PHIẾU — trần điểm (Thầy chốt 04/09/2026)

| Kỳ | Trần | Nghĩa là |
|---|---|---|
| **GK1, CK1** | **10,0** | Phiếu phải dạy **HẾT**, kể cả câu nâng cao 0,5đ cuối đề và ý cuối bài hình. Không được bỏ dạng nào. |
| **GK2, CK2** | **9,5** | Nhường **0,5đ ở Ý CUỐI BÀI HÌNH** — câu c)/d) quá nhiều bước, có bước HS chưa được học. |

> "HS có thể không đạt được hết, nhưng **mình cần dạy hết đến các phần đó**."
> Trần điểm là đích của PHIẾU, không phải dự đoán điểm của HS.

**Nhường 0,5đ nghĩa là gì — đọc kỹ, đây là chỗ dễ làm sai nhất:**
- **KHÔNG** phải bỏ câu đó ra khỏi phiếu.
- Là đổi **mục tiêu**: từ `an-tron` (giải trọn) sang `cham-diem-tung-phan` (ăn điểm từng phần).
  HS vẫn phải **vẽ được hình, viết được giả thiết–kết luận, làm xong ý a) b), và viết được
  bước đầu của ý c)** — barem đề Hà Nội chấm từng bước nên phần đó vẫn có điểm.
- Trường máy-đọc: `vdc.muc_tieu_vdc` trong [config/ban_do_vd_vdc.json](config/ban_do_vd_vdc.json),
  đọc bằng `tier_spec.muc_tieu_vdc(grade, chuong)`.

---

## 2. ĐỀ THI THẬT HỎI GÌ Ở CHỖ VDC — số liệu, không phải cảm giác

Đo bằng `.venv/bin/python scripts/tan_suat_vdc.py`. Mẫu: **21 đề GK1/CK1 lớp 9 đủ 9–10,5 điểm**
(bank đã chấm band từng câu) $+$ **14 đề GK2/CK2** phân loại bằng mắt
([inputs/refs/de-thi/lop-9/vdc-phan-loai-hk2.json](inputs/refs/de-thi/lop-9/vdc-phan-loai-hk2.json)).

### 2.1. Câu cuối đề — **một dạng duy nhất, lặp lại 82%**

> **27/33 đề (82%) kết thúc bằng BÀI CỰC TRỊ / TỐI ƯU 0,5đ.**

Khung vàng, giống nhau từ GK1 tới CK2:

```
gọi ẩn x (kèm điều kiện)  →  lập biểu thức theo x  →  đưa về (x − a)² + b  hoặc  Cô-si
                          →  dấu "=" xảy ra khi nào  →  kết luận + trả lời đúng câu hỏi
```

Bối cảnh chỉ đổi lớp áo: khung ảnh 384 cm² · rạp/nhà hát tăng giá vé · khách sạn 50 phòng ·
khu đất chu vi 60 m · trồng đậu–cà · bể lọc nước · tấm tôn uốn máng · sân hình vuông nội tiếp.
**Cùng một quy trình.** Đây là lý do trần 10,0 của kỳ I là *đạt được*: 0,5đ cuối đề có khuôn lặp.

### 2.2. Ý cuối bài hình — **34/34 đề đều là câu CHỨNG MINH nhiều bước**

Xếp hạng dạng (gộp cả 4 kỳ) — **soạn theo đúng thứ tự này**:

| # | Dạng | Số đề | Ưu tiên |
|---|---|---|---|
| 1 | Chứng minh **ba điểm thẳng hàng** | 8 | ★★★ |
| 2 | Chứng minh **vuông góc** | 5 | ★★★ |
| 3 | Chứng minh **song song / đồng dạng** | 4 | ★★☆ |
| 4 | Chứng minh **hệ thức** (tích đoạn thẳng, tỉ số lượng giác) | 4 | ★★☆ |
| 5 | Chứng minh **trung điểm** · tính **diện tích quạt / viên phân** | 2 + 2 | ★☆☆ |
| 6 | Lẻ: đồng quy · tam giác cân · thuộc $(O)$ · góc bằng nhau · trực tâm · phân giác | 1 mỗi loại | ★☆☆ |

### 2.3. Tần suất VDC theo chương (lớp 9) — cột `p`

| Ch | Kỳ | Câu cuối đề | Ý cuối bài hình | `p` | Nhóm | VD/VDC | Trần |
|---|---|---|---|---|---|---|---|
| I | GK1+CK1 | 0/21 | – | 0 | không | 55 / 0 | 10,0 |
| **II** | GK1+CK1 | **15/21** | – | **0,71** | **cao** | 35 / 20 | 10,0 |
| III | GK1+CK1 | 1/21 | – | 0,05 | thấp | 50 / 5 | 10,0 |
| **IV** | GK1 | 3/10 | **9/9** | **1,00** | **cao** | 35 / 20 | 10,0 |
| **V** | CK1 | 2/11 | **11/11** | **1,00** | **cao** | 35 / 20 | 10,0 |
| VI | GK2+CK2 | – | – | 0 | không | 55 / 0 | 9,5 |
| VII, VIII, X | GK2+CK2 | – | – | 0 | không | 55 / 0 | 9,5 |
| **IX** | GK2+CK2 | – | **14/14** | **1,00** | **cao** | 35 / 20 | **9,5** ⚠ |

⚠ Chương IX là chương duy nhất **tần suất cao NHƯNG mục tiêu là ăn điểm từng phần** —
đây chính là 0,5đ Thầy nhường ở kỳ II.

### 2.4. Khối 6, 7, 8 — đã đo (bản 0.6)

Cùng luật, cùng hai vị trí. Câu cuối đề phân loại **bằng mắt** 123 bản ghi
([vdc-phan-loai-khoi-678.json](inputs/refs/de-thi/vdc-phan-loai-khoi-678.json)); ý cuối bài hình
lấy chương theo **tiến độ SGK** (bảng `HINH_THEO_KY`). Lớp 6 **không có** vị trí "ý cuối bài
hình" (quy ước anh An).

| Khối | Chương giữ VDC | `p` | Khuôn lặp của câu cuối đề |
|---|---|---|---|
| **6** | **II** Tính chia hết | 0,84 | Chứng minh tổng luỹ thừa chia hết ($A=3+3^2+\dots+3^n \vdots 13$), hai số nguyên tố cùng nhau, phân số tối giản |
| **6** | **VI** Phân số | 0,77 | Gần như MỘT dạng: **tính tổng dãy phân số bằng sai phân** $\frac{1}{n(n+2)}$ |
| **7** | **I** Số hữu tỉ | 0,78 | Luỹ thừa, so sánh luỹ thừa, giá trị tuyệt đối, tổng luỹ thừa chẵn $\ge 0$ |
| **7** | **IX** Quan hệ trong tam giác | 1,00 | Giữ **toàn bộ** ý cuối bài hình HK2 (bất đẳng thức tam giác, trung tuyến, phân giác) |
| **7** | **VII** Đa thức một biến | 0,36 (vừa) | Nghiệm đa thức, dấu của tích $P(a)\cdot P(b)$, tách hệ số — riêng CK2 là 11/15 |
| **8** | **II** Hằng đẳng thức | 0,67 | Nhóm về **tổng bình phương bằng 0** rồi thay số; tìm GTNN/GTLN bằng HĐT |
| **8** | **III** Tứ giác | 1,00 | Giữ toàn bộ ý cuối bài hình HK1 (thẳng hàng, đồng quy) |

⚠️ **Lớp 8 kỳ II: MẪU QUÁ NHỎ** — kho chỉ có **2 đề** GK2/CK2 lớp 8 đọc được lớp text. Các
chương IV–X lớp 8 để `nhom_uu_tien: "mau-qua-nho"`, `phan_bo_55: null` ⇒ **giữ 15-30-55 mặc
định**, cổng không soi. Muốn dùng thì phải tải thêm đề. Luật chung: **mẫu dưới 6 đề thì không
áp tỉ lệ** — thà không soi còn hơn soi theo 2 đề.

**Chú ý khi soạn khối 6, 7:** câu cuối đề của hai khối này **KHÔNG phải bài thực tế** như lớp 9
mà là bài số học/đại số thuần. Nhưng nó **có khuôn lặp còn chặt hơn lớp 9** — riêng lớp 6 thì
27/63 câu là "tổng luỹ thừa chia hết" và 24/63 là "tổng dãy sai phân". Dạy trúng hai khuôn đó
là gần như phủ hết vị trí VDC. Ngoài ra 7/63 câu lớp 6 là **bài đếm / suy luận logic** (chia
bánh, bèo phủ ao, thi đấu vòng tròn) không thuộc chương nào — đừng cố nhét vào chương.

---

## 3. TỈ LỆ THỜI GIAN — chia khối 55% theo tần suất

Tổng vẫn là **NB 15% · TH 30% · (VD + VDC) 55%** như luật 30/08/2026. Cái mới: **khối 55%
không chia đều nữa.**

| Nhóm | `p` | VD | VDC | Ý nghĩa khi soạn |
|---|---|---|---|---|
| **cao** | ≥ 0,50 | 35% | 20% | Mỗi phiếu có **1 bài VDC trọn vẹn** (ví dụ 1 · trên lớp 1 · BTVN 1) |
| **vừa** | 0,20 – 0,49 | 43% | 12% | Mỗi phiếu 1 câu VDC, thường đặt ở BTVN |
| **thấp** | 0 < `p` < 0,20 | 50% | 5% | **Không có câu VDC trong phiếu thường** — 5% của 120′ là 6′, chưa đủ một câu 18′. Dồn VDC vào **phiếu ôn tập chương** |
| **không** | 0 | 55% | 0% | Không soạn VDC. (Chương `co_vd = false` thì về 30-70 và **gộp 2 phiếu**) |

Số câu mục tiêu máy tự tính (`tier_spec.target_counts`), lớp 9 đại số, buổi 180′:

| Nhóm | Ví dụ GV giảng (45′) | Luyện trên lớp (120′) | BTVN (90′) |
|---|---|---|---|
| **cao** (35/20) | 7 NB · 3 TH · 2 VD · **1 VDC** | 12 NB · 6 TH · 4 VD · **1 VDC** | 10 NB · 5 TH · 3 VD · **1 VDC** |
| **thấp** (50/5) | 7 NB · 3 TH · 3 VD | 12 NB · 6 TH · 5 VD | 10 NB · 5 TH · 4 VD |
| **không VD** (30/70) | 14 NB · 8 TH | 24 NB · 14 TH | 21 NB · 12 TH |

---

## 4. LUẬT "CHỈ Ý CUỐI MỚI LÀ VDC" (Thầy chốt 04/09/2026)

Một **bài** nhiều ý chỉ có **ĐÚNG MỘT** ý mức VDC — **ý cuối**. Các ý trước là TH hoặc VD.

```
Bài IV.2  a) [TH]  Chứng minh bốn điểm cùng thuộc một đường tròn
          b) [VD]  Chứng minh DF là tiếp tuyến của (O)
          c) [VDC] Chứng minh BC = 2·IO và AF·BH = BF·AH      ← chỉ ý này
```

**Vì sao bắt chặt:** VDC ăn 18′/câu so với TH 6′ — gắn thừa hai thẻ là phiếu phồng 24′ mà
Thầy không nhìn ra; và nó sai so với chính đề thi (đề nào cũng chỉ có một ý phân loại).

**Cổng:** `duration_gate.check_vdc_cuoi_bai` — cảnh báo khi một bài có ≥ 2 thẻ `[VDC]`,
hoặc khi sau thẻ `[VDC]` còn ý khác. Chạy trong `make validate`, áp cho **mọi tầng**.

---

## 5. PHƯƠNG PHÁP — Polya, "Giải một bài toán như thế nào?"

Nguồn: [inputs/refs/phuongphap/](inputs/refs/phuongphap/) — bản dịch tiếng Việt, 2 tập
(PDF ảnh, không có lớp text → đọc bằng mắt qua `pdftoppm`). Phần thứ nhất *Trong lớp học*
(§1–20), Phần thứ hai *Đối thoại* (bảng 4 bước), Phần thứ ba *Tự điển con* (64 mục).

### 5.1. Bốn bước → bốn thứ phải có mặt trên phiếu

| Bước Polya | Câu hỏi gốc | Chỗ nó nằm trên phiếu B |
|---|---|---|
| **1. Hiểu bài toán** | *Cái gì chưa biết? Cái gì đã cho? Điều kiện là gì?* | Ý a) của bài VD/VDC: **gọi ẩn + đặt điều kiện**, hoặc **vẽ hình + ghi GT/KL**. Bài hình bắt buộc vẽ hình trước. |
| **2. Xây dựng chương trình** | *Đã gặp bài toán nào gần giống chưa? Định lí nào dùng được? Đã dùng hết dữ kiện chưa?* | Hộp **`quy_trinh`** in ngay dưới đề bài VD (`ProblemBlock.quy_trinh`). Đây là chỗ Polya trở thành thứ HS cầm được. |
| **3. Thực hiện** | *Em thấy rõ bước này đúng không? Em chứng minh được nó đúng không?* | Các ý b), c) — **mỗi bước một dòng**, có căn cứ đi kèm. |
| **4. Nhìn lại** | *Thử lại kết quả được không? Có cách khác không? Dùng kết quả này cho bài khác được không?* | Câu **"Vậy…"** bắt buộc + sơ đồ **Tổng kết** cuối phiếu + bài `viet_quy_trinh` ở phiếu ôn tập chương. |

### 5.2. §17 "Câu hỏi tốt và câu hỏi tồi" — **luật viết `hints` và `quy_trinh`**

Polya bác thẳng gợi ý kiểu *"Em có thể áp dụng định lí Pi-ta-go ở đây được không?"*, vì:
① HS gần ra thì gợi ý thừa · ② HS hiểu gợi ý thì **chẳng còn gì để làm** · ③ quá đặc biệt nên
**không rút được gì cho bài sau** · ④ HS không hiểu tại sao thầy lại hỏi thế.

**Áp vào phiếu B:**
- ❌ **CẤM** gợi ý gọi thẳng tên công cụ: *"Dùng hệ thức $b^2 = a\cdot b'$"*, *"Áp dụng Cô-si"*.
- ✅ Gợi ý đi **từ tổng quát tới đặc biệt**, mỗi nấc một dòng:
  *"Cái phải tìm là gì?"* → *"Nó nằm trong tam giác nào?"* → *"Tam giác đó vuông ở đâu?"*
- Quy tắc thực dụng: gợi ý phải là câu **HS tự đặt lại được cho bài sau**. Nếu nó chỉ đúng
  cho đúng bài này thì đó là **câu hỏi tồi** — viết lại.
- **`quy_trinh` là quy trình của DẠNG, không phải lời giải của BÀI.** Viết được cho bài khác
  cùng dạng thì mới đạt.

### 5.3. §1 "Giúp đỡ vừa phải" → **giàn giáo thưa dần**

> *"không nhiều quá, cũng không ít quá… làm sao để học sinh có một phần công việc hợp lí"*
> và *"có cảm giác rằng anh ta tự làm lấy"*.

Chuỗi bài VD/VDC trong một phiếu B phải **gỡ giàn dần** (giống tầng C nhưng bắt đầu thưa hơn):

```
bài 1: 5–6 ý, có ô điền   →   bài 2: 3–4 ý, không ô điền
   →   bài 3: 2 ý (tự gọi ẩn, tự giải)   →   BTVN: gần đề trần, chỉ 1 móc về bài đã luyện
```

### 5.4. §18 **Bỏ bớt một phần điều kiện** — vũ khí cho câu VDC hình

Polya dựng hình vuông nội tiếp tam giác bằng cách **giữ 3 đỉnh trên cạnh, bỏ điều kiện đỉnh
thứ tư**, giải bài dễ hơn rồi khôi phục. Đây là cách duy nhất chẻ được câu VDC hình thành
bậc thang mà **không biến nó thành bài giải sẵn**:

| Ý | Việc của HS | Mức |
|---|---|---|
| a) | Vẽ hình, ghi GT–KL | TH |
| b) | Chứng minh **kết quả trung gian** (tứ giác nội tiếp / hai tam giác đồng dạng) | VD |
| c) | Dùng kết quả b) để ra kết luận cuối | **VDC** |

**"Phần tử phụ"** (§10, §12 — kẻ thêm đường phụ) là bước HS tầng B hay tắc nhất. Đừng cho
sẵn đường phụ trong đề; cho ở **hộp `quy_trinh`** dưới dạng câu hỏi tổng quát:
*"Muốn có hai tam giác đồng dạng thì cần thêm đoạn nào?"*

### 5.5. §5 "Bắt chước và thực hành"

Cùng một câu hỏi phải **lặp lại qua nhiều bài khác nhau** cho tới khi thành *thói quen của trí óc*.
Cụ thể: câu **"Cái phải tìm là gì?"** và **"Đã dùng hết giả thiết chưa?"** phải xuất hiện
trong `quy_trinh` của **mọi** bài VD trong phiếu — không đổi cách diễn đạt cho "đỡ lặp".

---

## 6. CÔNG THỨC SOẠN NỘI DUNG PHIẾU B

**A. Chọn dạng — bám bảng §2.2 và §2.1, không bịa dạng.**
1. Câu VDC của phiếu (nếu chương thuộc nhóm *cao*) lấy đúng **dạng đứng đầu bảng xếp hạng**
   của chương đó: đại số → **cực trị/tối ưu**; hình → **thẳng hàng**, rồi **vuông góc**.
2. Bê **nguyên câu** từ kho đề, ghi nguồn cuối đề: `(CK1 — THCS Ái Mộ)`. Không sửa số liệu
   trừ khi đề gốc sai (thì ghi rõ ở `ghi_chu`).
3. Mỗi dạng **tối đa 3 câu** (luật AGENTS §9, áp mọi tầng).

**B. Cắt bước theo 7 loại câu hỏi §4b** — bắt buộc, xem
[HUONG-DAN-THUYET-MINH-LOP-C.md §4b](HUONG-DAN-THUYET-MINH-LOP-C.md) (tên file là "LOP-C"
nhưng **luật áp mọi tầng**). Khai `loai` + `decompose` cho **từng dòng spec**.
NB **không phải bài rời** — nó là *bước* cắt ra từ chính bài TH/VD/VDC.

**C. Bài VD phải in `quy_trinh` ngay tại bài** (`ProblemBlock.quy_trinh`, level 3) — cổng
`_luat_tang_b` chặn nếu thiếu. Phiếu **ôn tập chương** phải có ≥ 1 dòng `viet_quy_trinh: true`
(HS **tự viết lại và giải thích** quy trình — chính là bước 4 của Polya).

**D. Bài VDC (level 4) — khuôn bắt buộc:**
- Chẻ theo §5.4, thẻ `[VDC]` **chỉ ở ý cuối**.
- Chương `muc_tieu_vdc = "cham-diem-tung-phan"` (kỳ II): thêm một dòng ở `teacher_note` nói rõ
  **HS ăn được mấy phần điểm nếu chỉ làm tới bước 2** — GV phải biết để không ép HS giải trọn.
- **KHÔNG** dùng kỹ thuật ngoài chương trình (bất đẳng thức 3 biến kiểu HSG, quy nạp…).

**E. Trình bày — bê nguyên từ tầng C** (HUONG-DAN-PHAN-TANG-LOP §5E), các mục hay bị bắt lỗi:
- HS làm vào **VỞ** → `writelines count 0`, không kẻ dòng, không chừa khung ([[khong-chua-cho-trong]]).
- Công thức toán **xuống dòng riêng**; mỗi bước biến đổi một dòng, giữ dấu trung gian.
- **KHÔNG** dùng `⇒` trong phần HS đọc; **KHÔNG** dùng ①②③; **CẤM** `\needspace`.
- Ví dụ mẫu viết theo khuôn **đề → "Lời giải" → dòng thụt lề → "Vậy…"**, không viết như lời
  hướng dẫn (cổng `check_vi_du_style`).
- Bài nhiều ý → 2 cột `minipage`; hình ngang đặt **dưới** đề.

**F. Khác tầng C ở đâu** — xem §7.

---

## 7. PHIẾU B KHÁC PHIẾU C CHỖ NÀO

| | Tầng **C** | Tầng **B** |
|---|---|---|
| Tỉ lệ | 40-40-20 cố định | **Theo chương** — 15-30-55 chia lại theo tần suất VDC, hoặc 30-70 (gộp 2 phiếu) |
| Mức cao nhất | level 3 (VD), **bỏ hẳn VDC** | **level 4 (VDC)** ở chương nhóm *cao* |
| Đích | thạo 100% NB+TH, làm được **một phần** VD | **trần 10,0 kỳ I · 9,5 kỳ II** |
| Giàn giáo | dày nhất (8 ý, ô điền từng bước) | bắt đầu **5–6 ý**, thưa nhanh hơn, BTVN gần đề trần |
| `quy_trinh` | không bắt buộc | **bắt buộc ở mọi bài VD** (cổng chặn) |
| Bài toán mở màn | phải gắn đời sống HS (tiền tiêu vặt, vé concert) | như C, nhưng **được dùng bối cảnh đề thi** từ bài luyện trở đi |
| Số ca | 1 phiếu = 1 buổi | chương không VD thì **`so_ca: 2`** (gộp 2 phiếu) |

**Bê nguyên từ C, không phải nghĩ lại:** mạch dẫn dắt quy nạp 6 bước (§5A của
HUONG-DAN-PHAN-TANG-LOP), luật "HS thấy CẦN mới đưa công cụ", hộp BẪY ĐIỂM cài lỗi sai của
"bạn Minh/bạn Lan", `teacher_note` là dàn ý điều phối có `[[br]]`, sơ đồ Tổng kết bám một câu
thi có đủ bước, và **toàn bộ mục Trình bày §5E**.

---

## 8. QUY TRÌNH CHẠY

```bash
mkdir "inputs/seeds/lop-9/dai-so/lop-b/chuong-02-bat-dang-thuc-bat-phuong-trinh/[B]tuanNN-<chu-de>"
.venv/bin/python -m src.main new-lesson "<folder>" --tier B --chuong chuong-02-bat-dang-thuc-bat-phuong-trinh
# → soạn nội dung theo §6; số câu theo bảng §3; thẻ [NB]/[TH]/[VD]/[VDC] ở TỪNG Ý
.venv/bin/python -m src.main validate <file.json>     # phải SẠCH trước khi build
.venv/bin/python -m src.main build-folder "<folder>"  # 3 PDF: handout / guide / slide
# → soi PDF bằng mắt (pdftoppm) rồi mới trình Thầy
```

**Kiểm trước khi trình Thầy:**

| Kiểm | Lệnh / cổng |
|---|---|
| Đã khai `chuong` chưa (thiếu là cổng tỉ lệ **im lặng bỏ qua**) | `_luat_tang_b` cảnh báo |
| Mỗi bài chỉ **một** `[VDC]`, ở **ý cuối** | `check_vdc_cuoi_bai` |
| Mọi bài VD có `quy_trinh` | `_luat_tang_b` |
| Tỉ lệ NB-TH-(VD+VDC) và quỹ phút | `check_duration` (±5 điểm %, ±10% quỹ) |
| Phiếu khớp hợp đồng thuyết minh | `spec_gate` (cần `thuyet-minh.json` **cùng folder**) |
| Đề ↔ hình khớp, không bài nhân bản | `figure_gate` |
| Đáp án PT/BPT | `answer_gate` (SymPy) |
| Tần suất VDC còn đúng sau khi thêm đề mới | `.venv/bin/python scripts/tan_suat_vdc.py` |

---

## 9. CÒN NỢ / CHỜ THẦY CHỐT

1. **Bản đồ 0.4 chờ Thầy duyệt** — nhất là file phân loại HK2 lớp 9 do con đọc bằng mắt
   (`vdc-phan-loai-hk2.json`, `da_duyet: false`).
2. **Bài tối ưu quy về tam thức bậc hai tính cho chương nào?** Con xếp cả 12 câu cuối đề HK2
   vào **chương II** (kĩ thuật là "đưa về $(x-a)^2+b$"), nhưng 5 bài trong đó cũng có thể tính
   cho **chương VI**. Ghi ở `chuong_khac`. **Cần Thầy chốt** — nó đổi tỉ lệ của cả hai chương.
3. **Lớp 8 kỳ II chỉ có 2 đề đọc được** (§2.4) — chưa kết luận được cho chương IV–X. Cần tải
   thêm đề GK2/CK2 lớp 8 có lớp text.
4. **Lớp 8 chương VIII (Xác suất) đang để `"bien"`** — bằng chứng mới ủng hộ hạ xuống `chi-TH`:
   câu cuối đề GK2 *"cần bốc ít nhất bao nhiêu viên bi để CHẮC CHẮN có 13 vàng, 10 xanh, 9 đỏ"*
   là bài **nguyên lí Dirichlet**, không phải xác suất. **Cần Thầy chốt.**
5. **Nợ cũ chưa trả:** 25 spec tầng B bị chặn vì 64 dòng VD thiếu `quy_trinh`; 12 phiếu ôn tập
   chương thiếu `viet_quy_trinh`; 199 bài VD trong 63 phiếu thật chưa có quy trình.
