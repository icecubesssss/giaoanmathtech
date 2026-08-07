# Hướng dẫn soạn Phiếu Thuyết minh — Tầng C (HS nền yếu – trung bình)

> **Phạm vi:** Hướng dẫn chuyên biệt cho quy trình soạn phiếu thuyết minh dành cho **Tầng C** (HS nền yếu – trung bình). Bổ trợ [AGENTS.md](AGENTS.md) (nguồn gốc quy trình), [HUONG-DAN-PHAN-TANG-LOP.md](HUONG-DAN-PHAN-TANG-LOP.md) (chuẩn spec giờ), [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md) (luật soạn chi tiết).
>
> **Bản mẫu Thầy đã duyệt** = thuyết minh Lớp 7 Hình — Chương 3 Góc & 2 đường thẳng song song (xuất từ Google Sheets). Mọi thuyết minh mới bám đúng 4 khối của bản đó.

---

## §0 — Mục tiêu & Đối tượng

**Đối tượng HS Tầng C:**
- Nền yếu – trung bình, **thiếu kiến thức nền tảng** từ lớp dưới/chương trước.
- Mục tiêu: thạo **100\% Nhận biết + Thông hiểu**, làm được **1 phần Vận dụng**.
- **KHÔNG có** Vận dụng cao (VDC), `level 4` / kim cương, `tier: extend` / HSG.
- Tỉ lệ thời gian cố định: **40\% NB – 40\% TH – 20\% VD – 0\% VDC**.

**Phiếu thuyết minh dùng để:**
1. **Thầy chốt SỐ CÂU** trước khi soạn phiếu (spec-first).
2. **Đối chiếu thời lượng** giữa SGV (Sách Giáo Viên / PPCT) và thực tế trung tâm.
3. **Phát hiện gap kiến thức** HS C thiếu → sinh dạng NB ôn lại.
4. **Liệt kê dạng đề thi** → đảm bảo phiếu phủ được các dạng ra thi.

---

## §1 — Quy trình 7 bước soạn thuyết minh Tầng C

```
Bước 1 ── AI hỏi Thầy 3 câu (§3)
         │
Bước 2 ── Rà ngân hàng đề thi (§4) & Phân loại 7 loại dạng bài (§4b)
         │
Bước 3 ── Xác định kiến thức nền HS C thiếu (§5)
         │
Bước 4 ── So sánh thời lượng SGV vs thực tế (§6)
         │
Bước 5 ── Điền 4 khối trang đầu (§2) + bảng spec (rows chia nhỏ 10-12 dạng/phiếu)
         │
Bước 6 ── Chạy gác cổng: make check-tm SPEC=<…>/thuyet-minh.json
         │
Bước 7 ── Build PDF thuyết minh → Thầy duyệt → Soạn phiếu
```

**Lệnh CLI:**

```bash
# Tạo khung thuyết minh
make spec FOLDER="inputs/seeds/<lop>/<mon>/[C]<chuong-hoac-tuan>" TIER=C

# Gác cổng (soi giờ vô lý trước khi chốt)
make check-tm SPEC="<…>/thuyet-minh.json"

# Build PDF cho Thầy đọc
make thuyetminh SPEC="<…>/thuyet-minh.json"

# Sau khi Thầy chốt → soạn phiếu bám spec
make new FOLDER="<folder>"
make validate FILE=<file.json>
make build FILE=<file.json>
```

---

## §2 — 4 khối trang đầu thuyết minh (bám bản mẫu Lớp 7 — An)

Mọi thuyết minh Tầng C **BẮT BUỘC** có 4 khối trên trang đầu PDF, **theo đúng thứ tự**:

### ❶ THỜI LƯỢNG

| Bài | Số ca trung tâm | Số tiết SGV/PPCT | Lý do chênh |
|---|---|---|---|
| Bài 7 + Bài 8 (gộp) | 1 ca = 180′ | 4 tiết | HS C cần thêm NB ôn kiến thức nền lớp 8 |
| Bài 9 phần 1 | 1 ca = 180′ | 2 tiết | Scaffolding phân tích nhân tử ẩn $\sqrt{x}$ |
| … | … | … | … |
| **Tổng** | **4 ca = 16 tiết** | **13 tiết SGK** | **+3 tiết**: ôn nền + scaffolding NB |

**Ghi vào field `thoiluong`** của `ThuyetMinhSpec`. Dòng cuối **BẮT BUỘC** có tổng + đối chiếu SGK.

### ❷ MỤC TIÊU + DẠNG ĐỀ THI

Chia 2 cột: **Mức tối thiểu** (cốt lõi) và **Bổ sung** (nâng thêm), kèm **mốc ĐIỂM SỐ** cụ thể.

| | Mức tối thiểu (NB + TH) | Bổ sung (VD) |
|---|---|---|
| **Yêu cầu** | Nhận biết + Thông hiểu các kỹ năng cốt lõi | Làm được 1 phần Vận dụng |
| **Điểm mục tiêu** | 1,5 điểm | 2,0 điểm |
| **Kỹ năng cụ thể** | Tìm ĐKXĐ, phân tích nhân tử, quy đồng, rút gọn B | Tính $A$ tại $x_0$, câu hỏi phụ $P = k$ |

**Dạng đề thi liên quan** (trích từ ngân hàng đề — xem §4):

| Mã dạng | Tên | Tần suất | Điểm TB/đề |
|---|---|---|---|
| `DS-CAN-TINH-RUTGON` | Tính / rút gọn biểu thức chứa căn | 10/11 CK1 | ~2,27đ |
| `DS-CAN-CAUPHU` | Câu hỏi phụ (tìm x, so sánh, GTNN) | 1/10 CK1 | ~0,50đ |

**Ghi vào fields `lythuyet`** (mục tiêu + chuẩn đầu ra) và **`dang_vd`** (dạng đề).

### ❸ VẤN ĐỀ HS (lỗi sai — liệt kê THEO BÀI, không gom chung chương)

| Bài / Buổi | Lỗi sai kinh điển |
|---|---|
| Buổi 1 (Bài 7+8) | Nhầm $\sqrt{A^2}=A$ khi $A<0$; cộng-trừ căn KHÔNG đồng dạng; quên ĐKXĐ |
| Buổi 2 (Bài 9 P1) | Không phân tích được mẫu thành nhân tử; nhầm $\sqrt{a+b}=\sqrt{a}+\sqrt{b}$ |
| Buổi 3 (Bài 9 P2) | Sai dấu phá ngoặc khi quy đồng; gạch ẩu không qua phân tích nhân tử |
| Buổi 4 (Bài 10) | Nhầm $\sqrt[3]{a^3}=|a|$ (không cần trị tuyệt đối) |

**Ghi vào field `loisai`**. Nguồn: AI đề xuất + **Thầy bổ sung** (xem §3).

### ❹ KIẾN THỨC NỀN HS C THIẾU

Liệt kê kiến thức **từ lớp dưới / chương trước** mà HS C hay mất, ảnh hưởng trực tiếp đến chương đang học:

| Kiến thức nền | Nguồn gốc | Dạng NB ôn lại trong phiếu |
|---|---|---|
| HĐT: $A^2-B^2=(A-B)(A+B)$; $(A\pm B)^2$ | Lớp 8 chương 1 | NB: phân tích $x-9 = (\sqrt{x}-3)(\sqrt{x}+3)$ |
| Phân tích nhân tử (đặt chung, nhóm) | Lớp 8 chương 1 | NB: đặt $\sqrt{x}$ nhân tử chung |
| Quy đồng phân thức | Lớp 8 chương 2 | NB: tìm MTC, nhân tử phụ |
| Đổi dấu: $a-b=-(b-a)$ | Lớp 8 chương 2 | NB: đổi dấu mẫu $1-\sqrt{x}=-(\sqrt{x}-1)$ |

**Ghi vào field `kienthuc_nb`**. Mỗi kiến thức nền → **sinh ít nhất 1 dạng NB** trong spec để HS C được ôn lại NGAY TRONG phiếu (không giả định HS đã biết).

---

## §3 — Quy trình AI hỏi Thầy (BẮT BUỘC trước mỗi chương)

**Khi bắt đầu soạn thuyết minh cho 1 chương mới**, AI **PHẢI** dừng lại và hỏi Thầy 3 câu. **KHÔNG được tự soạn thuyết minh mà chưa có câu trả lời.**

### Câu 1 — Dạng đề thi

> "Chương [X] có những dạng nào trong đề thi [GK/CK] năm [Y]?
> Em đã rà ngân hàng đề (`inputs/refs/de-thi/`), thấy các dạng sau:
> - [Mã dạng 1]: [tên], tần suất [N]/[M] đề, điểm TB ~[đ]đ
> - [Mã dạng 2]: …
>
> Thầy xác nhận và bổ sung dạng nào còn thiếu?"

### Câu 2 — Kiến thức nền HS C thiếu

> "HS Tầng C thường thiếu kiến thức nền gì khi học chương [X]?
> Em dự đoán từ chương trước / lớp dưới:
> - [Kiến thức 1] (nguồn: Lớp [N] chương [M])
> - [Kiến thức 2] …
>
> Thầy điều chỉnh / bổ sung?"

### Câu 3 — Lỗi sai kinh điển

> "Lỗi sai kinh điển của HS C ở chương [X] là gì?
> Em liệt kê từ ngân hàng đề + kinh nghiệm:
> - [Buổi 1]: [lỗi 1], [lỗi 2]
> - [Buổi 2]: [lỗi 3]
>
> Thầy bổ sung lỗi nào em chưa liệt kê?"

**Sau khi Thầy trả lời** → điền vào 4 khối trang đầu → build PDF → Thầy duyệt → mới soạn phiếu.

---

## §4 — Phân tích dạng đề thi (BẮT BUỘC trước khi soạn)

### Nguồn dữ liệu

| Nguồn | Đường dẫn | Nội dung |
|---|---|---|
| Ngân hàng đề GK1/CK1 | `inputs/refs/de-thi/lop-9/exams/` | 21 file JSON (10 GK1 + 11 CK1), mỗi câu gắn `dang`, `band`, `phut` |
| Ma trận thống kê | `inputs/refs/de-thi/lop-9/ma-tran-thong-ke.md` | Tần suất + điểm TB theo dạng |
| Taxonomy | `inputs/refs/de-thi/lop-9/taxonomy.json` | Bộ mã dạng chuẩn |
| Exam weights | `inputs/refs/de-thi/lop-9/exam-weights.json` | Trọng số tần suất × điểm TB |

### Lệnh rà nhanh

```bash
make exam-check          # gác Σdiem/band/phut/trùng id
make exam-report         # phút thực vs rate card
make exam-weights        # trọng số tần suất dạng
make coverage            # bank đủ câu cho từng dạng không
```

### Bảng đối chiếu: Dạng đề ↔ Dòng thuyết minh

Mỗi dạng đề thi xuất hiện trong ngân hàng **PHẢI** được phản ánh bằng **ít nhất 1 dòng spec** (NB hoặc TH hoặc VD) trong thuyết minh. Dùng bảng sau để đối chiếu:

| Mã dạng đề | Tần suất | Điểm | Dòng spec tương ứng | Band | Đã có? |
|---|---|---|---|---|---|
| `DS-CAN-TINH-RUTGON` | 10/11 CK1 | ~2,27đ | "Thực hiện phép tính $2\sqrt{48}-3\sqrt{75}+\sqrt{27}$" | TH | ✅ |
| `DS-CAN-TINH-RUTGON` | 10/11 CK1 | ~2,27đ | "Rút gọn $B = \frac{x+15}{x-9}+…$" | VD | ✅ |
| `DS-CAN-CAUPHU` | 1/10 CK1 | ~0,50đ | "Tìm $x$ để $P = k$, $P < k$" | VD | ✅ |
| … | … | … | … | … | … |

Nếu có dạng đề chưa có dòng spec → **thêm dòng spec hoặc hỏi Thầy**.

---

## §4b — Quy chuẩn Phân tách Dạng bài & Phân loại 7 loại Câu hỏi (Thầy chốt 2026-08-05)

Để tránh tình trạng phiếu bị gom thành các khối quá lớn (7–8 câu/dòng), mỗi phiếu thuyết minh **bắt buộc phải chia nhỏ thành 10–12 dạng bài cụ thể** (mỗi dạng 2–3 câu hoặc 1 bài ghép).

### 7 Loại Dạng bài Phân tầng từ Lý thuyết đến Bài thi (Ưu tiên sát Đề Thi):

1. **NB lẻ từ lý thuyết**: Nhận biết 1 bước hỏi trực tiếp định nghĩa / công thức / hình vẽ cơ bản (ví dụ: nhận diện bán kính, dây cung, góc ở tâm, công thức $C = 2\pi R$).
2. **NB lẻ tách từ TH**: Các câu NB trích làm bước đệm kỹ năng trực tiếp từ câu hỏi TH trong đề thi (ví dụ: tìm ĐKXĐ, tính khoảng cách $OH$ từ Pythagore tam giác vuông, chỉ ra tiếp tuyến).
3. **NB ghép bài**: Bài tập ghép nhiều ý (câu a, b, c...) trích từ 1 bài TH/VD đề thi, trong đó các ý đầu là bước đệm NB giúp HS hình thành hướng giải.
4. **TH lẻ từ lý thuyết**: Thông hiểu 1–2 bước áp dụng trực tiếp lý thuyết (ví dụ: giải tam giác vuông, tính diện tích quạt/cung tròn theo công thức).
5. **TH ghép bài**: Bài tập ghép nhiều ý (ghép tiếp vào NB ghép bài ở trên, dẫn dắt từ bước đệm NB $\to$ ý TH của bài thi).
6. **TH tách từ VD**: Bài TH là bước đệm trung gian bóc tách từ câu VD của đề thi (ví dụ: chứng minh $MA = MB$ hay $AO \perp BC$ để chuẩn bị cho ý chứng minh tiếp tuyến/hệ thức).
7. **VD lẻ tương tự bài VD đã tách lẻ bước TH**: Bài Vận dụng hoàn chỉnh sát đề thi Vào 10 (sau khi HS đã được luyện tập qua các bước đệm NB/TH tách lẻ).

> **Nguyên tắc CẤM & ƯU TIÊN:**
> - **Ưu tiên 100% dạng bài có trong Đề thi Vào 10 và Đề thi học kỳ (CK1/GK1).**
> - **CẤM gom quá 3 câu cho 1 dạng bài.** Phải tách nhỏ các dòng spec để phiếu có độ dốc mịn.

---

## §5 — Kiến thức nền HS C thiếu

### Cách xác định gap kiến thức

1. **Xem nội dung chương mới** → liệt kê các kỹ thuật / khái niệm tiên quyết.
2. **Đối chiếu lớp dưới / chương trước** → kỹ thuật nào HS C chưa thạo?
3. **Hỏi Thầy** xác nhận (§3 Câu 2).
4. **Sinh dạng NB** ôn lại trực tiếp trong spec.

### Template field `kienthuc_nb` trong JSON

```json
"kienthuc_nb": [
  "HĐT Lớp 8: $A^2-B^2=(A-B)(A+B)$ và $(A \\pm B)^2$.",
  "Phân tích nhân tử: đặt nhân tử chung, dùng HĐT.",
  "Quy đồng phân thức (Lớp 8 chương 2): tìm MTC, nhân tử phụ.",
  "Đổi dấu: $a-b = -(b-a)$; $1-x = -(x-1)$."
]
```

### Quy tắc sinh NB & Phân loại 3 dạng Nhận biết (NB)

Mọi dòng Nhận biết (NB) trong phiếu thuyết minh phải thuộc đúng 1 trong 3 nhóm sau (khai báo qua trường `"loai_dang"` hoặc `"note"`):

1. **`NB-NEN` (NB Kiến thức cũ / Nền tảng):**
   - *Bản chất:* Ốn lại kỹ năng/công thức lớp dưới hoặc chương trước (như HĐT lớp 8, phân tích nhân tử cơ bản, quy đồng phân thức).
   - *Cách dạy:* Trình bày song song 2 cột `"Lớp 8 đã thạo | Lớp 9 ứng dụng"`.

2. **`NB-MOI` (NB Kiến thức mới):**
   - *Bản chất:* Nhận diện ký hiệu mới, điều kiện xác định cơ bản, công thức mới (ví dụ: nhận biết $\sqrt{A}$, ĐKXĐ $A \ge 0$, $\sqrt{a^2}=|a|$).
   - *Tối đa:* 3 câu/dạng.

3. **`NB-DECOMPOSE` (NB chẻ ra từ Thông hiểu):**
   - *Bản chất:* Ý đệm 1 bước trích trực tiếp từ câu TH (ví dụ: trước khi tính biểu thức $A$ tại $x=9$, dạng NB này đệm ý a) "Tính $\sqrt{9}$" hoặc "Viết ĐKXĐ").

---

### Phân loại 3 dạng Thông hiểu (TH)

Mọi dòng Thông hiểu (TH) trong phiếu thuyết minh thuộc 1 trong 3 nhóm:

1. **`TH-MOI` (TH Kiến thức mới cơ bản):**
   - *Bản chất:* Áp dụng 1–2 bước biến đổi quy tắc mới (ví dụ: khai phương một tích $2\sqrt{48} - 3\sqrt{75}$, giải BPT 2 bước).

2. **`TH-DECOMPOSE` (TH chẻ ra từ Vận dụng):**
   - *Bản chất:* Bước đệm trung gian 2 bước trích từ bài VD đề thi (ví dụ: trong bài rút gọn $B$, ý TH là "Rút gọn từng cụm phân thức sau khi đã quy đồng tử").

3. **`TH-TONGHOP` (TH Luyện tập tổng hợp / Nối bài cũ-mới):**
   - *Bản chất:* Kết hợp 2 kỹ năng TH đơn lẻ hoặc nối kiến thức cũ với mới (ví dụ: tính giá trị biểu thức sau khi đã thu gọn).

---

### Gắn nhãn `loai_dang` & Quy tắc AI GHÉP THÀNH BÀI trên Phiếu

Để Thầy soi phiếu thuyết minh biết ngay các dòng spec sẽ được **ghép thành bài tập như thế nào trên phiếu**, mỗi dòng `rows[]` trong `thuyet-minh.json` bắt buộc ghi rõ `loai_dang` (hoặc `note`):

#### 1. Cấu trúc dòng spec trong JSON:
```json
{
  "dang": "Nhận biết hằng đẳng thức $x - 9 = (\\sqrt{x}-3)(\\sqrt{x}+3)$",
  "band": "NB",
  "loai_dang": "NB-NEN",
  "ghep_bai": "Bai_1_Y_a",
  "lythuyet": 1, "vidu": 0, "onclass": 3, "btvn": 2
}
```

#### 2. Quy tắc ghép dòng Spec thành Bài tập hoàn chỉnh (Mapping Rule):

- **Bài Nhận biết / Ôn tập (LT1):**
  - Gom các dòng `NB-NEN` + `NB-MOI` thành các **Bài 1, Bài 2 dạng chia cột hoặc điền khuyết (a, b, c, d)**.
- **Bài Thông hiểu / Vận dụng có Giàn giáo (LT2):**
  - Gom chuỗi: `[NB-DECOMPOSE]` (ý a) $\to$ `[TH-DECOMPOSE]` (ý b) $\to$ `[VD]` (ý c) thành **1 Bài tập lớn duy nhất**.
  - *Ví dụ:*
    - Ý a) `[NB-DECOMPOSE]`: Tìm ĐKXĐ của biểu thức $B$.
    - Ý b) `[TH-DECOMPOSE]`: Phân tích mẫu $x-9$ và quy đồng tử thức.
    - Ý c) `[VD]`: Rút gọn hoàn chỉnh $B$ và tính $P = A \cdot B$.

Nhờ cờ `ghep_bai` và `loai_dang` trên thuyết minh, Thầy nhìn vào bảng spec là biết chính xác dòng nào là bài rời, dòng nào sẽ chẻ thành ý nhỏ a), b), c) trong bài lớn!

---

## §6 — So sánh thời lượng SGV vs Thực tế

### Bảng mẫu (Lớp 9 Đại số Chương 3)

| Bài SGK | Tiết SGV/PPCT | Ca trung tâm (180′/ca) | Chênh | Lý do |
|---|---|---|---|---|
| Bài 7: Căn bậc hai | 2 tiết | gộp Bài 7+8 = 1 ca | — | — |
| Bài 8: Khai phương tích/thương | 2 tiết | (gộp trên) | — | — |
| Bài 9: Căn thức bậc hai (biến đổi + rút gọn) | 3 tiết | 2 ca | +1 ca | HS C cần scaffolding phân tích nhân tử ẩn $\sqrt{x}$ + ôn HĐT lớp 8 |
| Bài 10: Căn bậc ba | 1 tiết | gộp + luyện tập = 1 ca | — | — |
| Luyện tập chung | 5 tiết | (gộp trên) | — | — |
| **Tổng** | **13 tiết** | **4 ca = 16 tiết** | **+3 tiết** | **Ôn nền + scaffolding + luyện tập thêm cho HS C** |

### Field `thoiluong` trong JSON

```json
"thoiluong": [
  "Buổi 1 (Bài 7 $+$ Bài 8, gộp): 1 ca $=$ 180 phút (SGK 4 tiết)",
  "Buổi 2 (Bài 9 phần 1): 1 ca $=$ 180 phút (SGK 2 tiết)",
  "Buổi 3 (Bài 9 phần 2): 1 ca $=$ 180 phút (SGK 1 tiết)",
  "Buổi 4 (Bài 10 $+$ Luyện tập chung): 1 ca $=$ 180 phút (SGK 1 $+$ 5 tiết)",
  "\\textbf{Tổng 4 ca $=$ 16 tiết} (SGK chương III: 13 tiết) — chênh $+$3 tiết do ôn kiến thức nền $+$ scaffolding NB cho HS C"
]
```

**Lưu ý:** Dòng cuối **BẮT BUỘC** có:
- Tổng số ca + quy đổi tiết
- So sánh với SGK/SGV
- **Lý do chênh** (1 câu ngắn gọn)

---

## §7 — Công thức vàng & Rate card (tóm tắt cho Tầng C)

> Chi tiết đầy đủ tại [config/tier\_spec.json](config/tier_spec.json) và [HUONG-DAN-PHAN-TANG-LOP.md](HUONG-DAN-PHAN-TANG-LOP.md) §2.

### Lớp 9 Đại số — Tầng C

| Thông số | Giá trị |
|---|---|
| Buổi học | 180′ (trừ 15′ giải lao = **165′ học**) |
| Tỉ lệ NB:TH:VD:VDC | **40 : 40 : 20 : 0** |
| `max_level` | 3 (★★★ — KHÔNG có kim cương) |
| `allow_extend` | `false` |

### Rate card (phút/câu)

| Đoạn | NB | TH | VD |
|---|---|---|---|
| Ví dụ GV giảng | 1′ | 4′ | 8′ |
| Luyện tập trên lớp (×1,5) | 1,5′ | 6′ | 12′ |
| BTVN (×1,3) | 1,3′ | 5,2′ | 10,4′ |

### Ngân sách

| Đoạn | Quỹ (phút) | Dung sai |
|---|---|---|
| Ví dụ GV giảng | 45′ | ±10\% |
| Luyện tập trên lớp | 120′ | ±10\% |
| BTVN | 90′ | ±10\% |

### Công thức tính số câu mục tiêu

```
Số câu NB onclass = 120′ × 40% ÷ 1,5′ = 32 câu
Số câu TH onclass = 120′ × 40% ÷ 6′   =  8 câu
Số câu VD onclass = 120′ × 20% ÷ 12′  =  2 câu
```

### Lớp 9 Hình học — Tầng C

| Thông số | Giá trị |
|---|---|
| Buổi học | 90′ (trừ 10′ giải lao = **80′ học**) |
| Tỉ lệ | **40 : 40 : 20 : 0** (giữ như đại số) |
| Rate NB/TH/VD (onclass) | 1,5′ / 6′ / 12′ (KHÔNG nhân đôi — khác lớp 8) |
| Câu NB trên hình vẽ sẵn | `quick_minutes` = 1′/câu |
| Câu tự vẽ hình | +5′ (`draw_minutes`) |

---

## §8 — Checklist trước khi trình Thầy

### A. Checklist thuyết minh (trước khi build PDF)

- [ ] **4 khối trang đầu đủ**: Thời lượng (có so sánh SGV) → Mục tiêu (có điểm số + dạng đề) → Vấn đề HS (theo bài) → Kiến thức nền
- [ ] **AI đã hỏi Thầy 3 câu** (§3) và nhận câu trả lời
- [ ] **Mỗi dạng đề thi** trong ngân hàng → có ít nhất 1 dòng spec tương ứng
- [ ] **Mỗi kiến thức nền** → có ít nhất 1 dạng NB ôn lại
- [ ] **Chuẩn đầu ra** ghi rõ mốc ĐIỂM SỐ (tối thiểu vs mục tiêu)
- [ ] **Tổng thời lượng** đối chiếu SGV, có lý do chênh
- [ ] `make check-tm SPEC=<…>` sạch (0 lỗi, cảnh báo đã xử lý)
- [ ] `make thuyetminh SPEC=<…>` build thành công → PDF cho Thầy đọc

### B. Checklist phiếu (sau khi soạn bám thuyết minh đã duyệt)

- [ ] Số câu NB/TH/VD khớp spec (±1 câu/band — `spec_gate`)
- [ ] `make validate FILE=<…>` sạch (gồm `duration_gate` 40-40-20 ±5\%)
- [ ] `make build FILE=<…>` → 3 PDF (handout/guide/slide)
- [ ] Đọc lại PDF: badge LỚP C hiện, sao theo mức nhận thức, không VDC
- [ ] Trình Thầy → `make approve`

---

## §9 — Ví dụ thực tế: Chương 3 Căn thức (Lớp 9 Đại số, Tầng C)

> Tham chiếu: [thuyet-minh.json](inputs/seeds/lop-9/dai-so/lop-c/chuong-03-can-bac-hai-can-bac-ba/thuyet-minh.json) — thuyết minh đã soạn.

### ❶ Thời lượng

```
Buổi 1 (Bài 7+8):  1 ca = 180′  (SGK 4 tiết)
Buổi 2 (Bài 9 P1): 1 ca = 180′  (SGK 2 tiết)
Buổi 3 (Bài 9 P2): 1 ca = 180′  (SGK 1 tiết)
Buổi 4 (Bài 10+LT): 1 ca = 180′ (SGK 6 tiết)
Tổng: 4 ca = 16 tiết (SGK: 13 tiết) — +3 tiết do ôn nền + scaffolding
```

### ❷ Mục tiêu + Dạng đề

- **Mức tối thiểu**: tính $A$ tại $x_0$, rút gọn $B$ ≈ **1,5 điểm**
- **Bổ sung**: câu hỏi phụ $P = k$, $P < k$ → **2,0 điểm**
- **Dạng đề**: `DS-CAN-TINH-RUTGON` (10/11 CK1, ~2,27đ), `DS-CAN-CAUPHU` (tìm $x$ để $P$ thỏa đk)

### ❸ Vấn đề HS (theo buổi)

- Buổi 1: nhầm $\sqrt{A^2}=A$; cộng-trừ căn không đồng dạng; quên ĐKXĐ
- Buổi 2: không phân tích được nhân tử ẩn $\sqrt{x}$; nhầm $\sqrt{a+b}=\sqrt{a}+\sqrt{b}$
- Buổi 3: sai dấu phá ngoặc trước dấu trừ; gạch ẩu không qua phân tích nhân tử
- Buổi 4: nhầm $\sqrt[3]{a^3}=|a|$ (căn bậc ba không cần trị tuyệt đối)

### ❹ Kiến thức nền

- HĐT lớp 8: $A^2-B^2$, $(A\pm B)^2$ → NB: phân tích $x-9$, $x\pm 2a\sqrt{x}+a^2$
- Phân tích nhân tử → NB: đặt $\sqrt{x}$ nhân tử chung
- Quy đồng phân thức → NB: tìm MTC, nhân tử phụ
- Đổi dấu: $a-\sqrt{x} = -(\sqrt{x}-a)$ → NB: nhận diện đổi dấu mẫu

### Bảng spec mẫu (trích Buổi 1 — Minh họa nhãn `loai_dang` & `ghep_bai`)

| Dạng bài thuyết minh | Band | Loại dạng | Ghép bài (Phiếu) | Ví dụ | Onclass | BTVN |
|---|---|---|---|---|---|---|
| HĐT Lớp 8: $x - 9 = (\sqrt{x}-3)(\sqrt{x}+3)$ | NB | `NB-NEN` | Bài 1a (Ý đệm) | 1 | 3 | 2 |
| ĐKXĐ biểu thức $\sqrt{ax+b}$ | NB | `NB-MOI` | Bài 1b | 1 | 3 | 2 |
| ĐKXĐ của biểu thức $B$ (Đệm cho Bài rút gọn) | NB | `NB-DECOMPOSE` | Bài 3a (Ý đệm) | 0 | 2 | 2 |
| Thực hiện phép tính $2\sqrt{48}-3\sqrt{75}+\sqrt{27}$ | TH | `TH-MOI` | Bài 2 (Bài độc lập) | 1 | 2 | 2 |
| Quy đồng tử thức biểu thức $B$ | TH | `TH-DECOMPOSE` | Bài 3b (Ý trung gian) | 0 | 2 | 2 |
| Rút gọn $B = \frac{x+15}{x-9}+…$ hoàn chỉnh | VD | `VD-CHINH` | Bài 3c (Ý trùm cuối) | 1 | 1 | 1 |

---

## §10 — Hướng dẫn chuyển từ Phiếu Thuyết minh sang Phiếu Bài tập JSON (`phieu-a/b/c.json`)

Sau khi Thầy chốt phiếu Thuyết minh (`thuyet-minh.json`), AI hoặc Giáo viên thực hiện chuyển đổi các dòng spec thành **Phiếu bài tập JSON thực tế** (`phieu-a.json`, `phieu-b.json`...) theo quy trình 4 bước dưới đây:

### Bước 1: Khởi tạo khung bài học bằng CLI

```bash
# Tạo khung phiếu JSON với class_tier="C" và 5 chặng chuẩn
python -m src.main new-lesson "inputs/seeds/lop-9/dai-so/[C]tuan16-can-bac-hai" --tier C
```

### Bước 2: Phân bổ các cột số câu (`vidu`, `onclass`, `btvn`) vào 5 chặng bài học

| Cột số câu trong Spec | Chặng tương ứng trong phiếu lesson JSON | Cách trình bày & Đặc điểm |
|---|---|---|
| **Cột `vidu`** | **Chặng 1 (`review`) & Chặng 2 (`concept`)** | Dạng **Ví dụ mẫu** (`variant: "example"`). Có lời giải từng bước, sử dụng `[[blank:W]]` cho ô trống để GV + HS cùng điền tại lớp. |
| **Cột `onclass`** | **Chặng 3 (`practice1`) & Chặng 4 (`practice2`)** | **Bài tập làm tại lớp**. <br>• Chặng 3 (`practice1`): Gom các dòng `NB-NEN` & `NB-MOI` (nền tảng/dễ). <br>• Chặng 4 (`practice2`): Gom các dòng `NB-DECOMPOSE`, `TH-MOI`, `TH-DECOMPOSE`, `VD-CHINH` (bài tập lớn bám đề thi vào 10, chạm trần `ceiling.level=3`). |
| **Cột `btvn`** | **Chặng 5 (`reflection`)** | Gắn nhãn `"tier": "btvn"`. Renderer sẽ tự động gom và in thành mục **"BÀI TẬP VỀ NHÀ"** riêng biệt trên bản PDF Handout & Guide. |

---

### Bước 3: Thuật toán GHÉP các dòng Spec (`rows[]`) thành BÀI TẬP hoàn chỉnh

Khi tạo các block `problem` trong phiếu bài tập JSON, áp dụng 2 thuật toán ghép bài sau:

#### Quy tắc A: Gom dạng bài độc lập (Dành cho `NB-MOI` và `TH-MOI`)
- **Đặc điểm:** Các câu NB/TH cùng 1 dạng thao tác đơn (ví dụ: tính $\sqrt{81}$, $\sqrt{49}$, $\sqrt{100}$).
- **Cách ghép:** Gom $N$ câu thành **1 Bài tập duy nhất** chứa các ý nhỏ a), b), c), d).
- **Trình bày:** Dàn 2 cột gọn gàng bằng `minipage` trong `text` hoặc `sub-items`:
  ```json
  {
    "type": "problem",
    "level": 1,
    "text": "Bài 1. [NB] Tính giá trị các căn bậc hai số học sau:[[br]]\\begin{minipage}[t]{0.47\\linewidth}a) $\\sqrt{81}$;[[br]]b) $\\sqrt{49}$;\\end{minipage}\\hfill\\begin{minipage}[t]{0.47\\linewidth}c) $\\sqrt{0{,}04}$;[[br]]d) $\\sqrt{\\frac{9}{16}}$.\\end{minipage}"
  }
  ```

#### Quy tắc B: Gom chuỗi Giàn giáo — Scaffolded Chain (Dành cho `DECOMPOSE`)
- **Đặc điểm:** Các dòng spec có chung ký hiệu `ghep_bai` (chuỗi từ NB đệm $\to$ TH đệm $\to$ VD trùm cuối).
- **Cách ghép:** Gom toàn bộ chuỗi thành **1 Bài tự luận lớn duy nhất** bám sát cấu trúc Bài I/Bài II của đề thi Vào 10. Gắn thẻ `level` tương ứng cho từng ý nhỏ:
  - Ý a) `[NB-DECOMPOSE]`: Tìm ĐKXĐ của biểu thức $B$ (`level: 1`).
  - Ý b) `[TH-DECOMPOSE]`: Phân tích mẫu $x-9 = (\sqrt{x}-3)(\sqrt{x}+3)$ và quy đồng tử thức (`level: 2`).
  - Ý c) `[VD-CHINH]`: Rút gọn biểu thức $B$ hoàn chỉnh và tìm $x$ để $B < \frac{1}{2}$ (`level: 3`).

---

### Bước 4: Kiểm tra tự động bằng CLI (`spec_gate` & `duration_gate`)

Sau khi điền phiếu JSON, chạy lệnh `validate` để gác cổng kiểm tra tự động:

```bash
python -m src.main validate inputs/seeds/lop-9/dai-so/[C]tuan16-can-bac-hai/phieu-a-can-bac-hai-phep-khai-phuong.json
```

- **`spec_gate`**: Tự động so sánh tổng số câu NB, TH, VD của phiếu JSON với phiếu `thuyet-minh.json` cạnh bên. Nếu lệch quá $\pm 1$ câu/band sẽ báo lỗi ngay.
- **`duration_gate`**: Tự động tính toán tổng số phút Luyện tập trên lớp (target = 120 phút $\pm 10\%$) và tỷ lệ 40-40-20 ($\pm 5\%$).

---

## Phụ lục — Ánh xạ field JSON ↔ 4 khối trang đầu

| Khối trang đầu | Field trong `ThuyetMinhSpec` |
|---|---|
| ❶ Thời lượng | `thoiluong` (mảng string) |
| ❷ Mục tiêu + Dạng đề | `lythuyet` (mục tiêu + chuẩn đầu ra), `dang_vd` (dạng đề tổng quát), `vidu` (ví dụ cụ thể) |
| ❸ Vấn đề HS | `loisai` (mảng string, liệt kê theo buổi) |
| ❹ Kiến thức nền | `kienthuc_nb` (mảng string) |
| Bảng spec chi tiết | `phieu[].rows[]` (từng dòng dạng bài) |

