# QUY TRÌNH & HỆ THỐNG TEMPLATE SHEETS MẪU CHUẨN MATHTECH

> **Tài liệu đặc tả kỹ thuật & hướng dẫn nghiệp vụ dành cho Giáo viên và Trợ lý AI**  
> **Người biên soạn:** Trương Đình Thái — Tổ Học Liệu MathTech  
> **Link Google Sheets trực tiếp (Template Mẫu Chuẩn 4 Tab):**  
> 👉 [**docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY/edit**](https://docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY/edit)  
> *(Bấm link trên $\to$ Chọn **Tệp** $\to$ **Tạo bản sao** để bắt đầu chương mới hoặc ca học mới)*  
> **Nguồn quy chuẩn gốc:** Google Sheet *"Các đầu việc học liệu"* (`1NCJHzp0cU9zUaJIkw47UfLzrPUj09P-5prgiGG6erDs`) và các quyết định Thầy chốt (22/10, 30/10, 03/11, 05/11/2026).  
> **Tài liệu liên quan:** [`docs/quy-chuan-hoc-lieu.md`](quy-chuan-hoc-lieu.md), [`docs/quy-trinh-ngan-hang-chuong.md`](quy-trinh-ngan-hang-chuong.md), [`docs/quy-trinh-bo-de-on-tap.md`](quy-trinh-bo-de-on-tap.md).

---

## TỔNG QUAN HỆ THỐNG 4 TEMPLATE SHEETS

Trong hệ sinh thái MathTech, dữ liệu học liệu được quản trị tập trung và liên kết chặt chẽ qua **4 Template Google Sheets chuẩn**:

```
[1. NGÂN HÀNG & PHÂN DẠNG CHƯƠNG] ──(Mã câu cột M)──► [2. THUYẾT MINH LIÊN KẾT ĐỘNG]
      (47 cột chuẩn: L1-L5, T1-T8)                             (Ma trận dạng bài, quỹ 90')
                                                                           │
                                                                           ▼
[4. QUẢN TRỊ TIẾN ĐỘ & DRIVE] ◄──────(Link PDF & Drive)────── [3. MA TRẬN ĐỀ KIỂM TRA & THI]
   (Tích xanh nghiệm thu tuần)                                  (3 hình thức, rải ≥4 quận)
```

1. **Template 1 — Tab Phân dạng chương & Ngân hàng câu hỏi (Master / Chapter Bank Sheet)**: Chứa toàn bộ câu hỏi quét từ đề thi thật Hà Nội và SGK, chuẩn hóa 47 cột, tự động chấm điểm L1–L5, T1–T8 và phân tầng A/B/C/X.
2. **Template 2 — Tab Thuyết minh liên kết động (Dynamic Spec Sheet)**: Bản thiết kế sư phạm của từng buổi học (spec-first), cân đối quỹ thời lượng 90'/120' và tỉ lệ 40-40-20, liên kết động với cột Mã câu của Template 1.
3. **Template 3 — Tab Ma trận & Đặc tả Đề kiểm tra chương 45' & Đề thi GK/CK (Exam Matrix & Spec Sheet)**: Ma trận chuẩn 3 hình thức (Trắc nghiệm - Điền khuyết - Tự luận), kiểm soát rải nguồn ≥ 4 quận/huyện Hà Nội từ năm học 2024–2025.
4. **Template 4 — Tab Quản trị Tiến độ & Bàn giao sản phẩm (Progress & Delivery Sheet)**: Quản lý toàn bộ vòng đời sản phẩm từ khâu soạn, thẩm định, duyệt đến xuất bản trọn bộ 3 bản PDF (Handout HS, Guide GV, Slide) lên Google Drive.

---

## TEMPLATE 1: TAB PHÂN DẠNG CHƯƠNG & NGÂN HÀNG CÂU HỎI (47 CỘT CHUẨN)

### 1. Ý nghĩa & Vai trò
* Là **nguồn sự thật duy nhất (Single Source of Truth)** cho mọi bài toán trong chương.
* Cung cấp nguyên liệu đã bóc tách ý con sẵn sàng theo kỹ thuật giàn giáo (Scaffolding Rails) từ bài Vận dụng (VD) $\to$ Thông hiểu (TH) $\to$ Nhận biết (NB).
* Mọi câu hỏi đưa vào phiếu học tập hoặc đề kiểm tra bắt buộc phải có **Mã câu** xuất phát từ tab này.

### 2. Cấu trúc 47 cột chia theo 5 Phân khu Chức năng

```
┌─────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────┐
│  PHÂN KHU I (A–M)   │  PHÂN KHU II (N–X)   │ PHÂN KHU III (Y–AE)  │  PHÂN KHU IV (AF–AM) │ PHÂN KHU V (AN–AU)  │
│  Dữ liệu bài toán   │ Phân loại sư phạm    │ Bóc tách ý con       │ Chấm 8 tiêu chí      │ Đánh giá & Kết luận │
│  & Mô tả đề thô     │ & Giàn giáo leo dốc  │ & Kỹ thuật đề thật   │ chất lượng (T1–T8)   │ phân tầng tự động   │
└─────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────┘
```

#### Phân khu I: Dữ liệu bài toán & Mô tả đề thô (Cột A – M)
| Cột | Tên trường | Kiểu dữ liệu | Ý nghĩa sư phạm & Quy chuẩn điền |
|:---:|:---|:---:|:---|
| **A** | `Bài cụ thể` | Text | Đề bài nguyên văn rõ ràng, mỗi ý xuống dòng bằng `a) ...`, `b) ...`. Giữ nguyên số liệu gốc, không bịa đề. |
| **B** | `Nguồn trong input` | Text | Tên đề thi/sách gốc, ví dụ: *Đề thi HK1 THCS Trưng Vương 2024–2025, Bài IV.2*. |
| **C** | `Mức độ` | Text | Mức độ tổng thể của dòng: `NB`, `TH`, `VD`, `VDC`. |
| **D** | `Dạng bài` | Text | Tên dạng bài toán chuẩn trong phân phối chương (ví dụ: *Chứng minh tiếp tuyến của đường tròn*). |
| **E** | `Ưu tiên` | Text | `Ưu tiên 1` (Đề thi chính thức), `Ưu tiên 2` (SGK/SGV), `Ưu tiên 3` (SBT/Tham khảo), `Ưu tiên 4` (Cũ/lệch chuẩn SGK mới). |
| **F** | `Phân loại vào phiếu` | Text | Gán vị trí dự kiến: *Phiếu 2 (bốn điểm, tiếp tuyến); Trên lớp* hoặc *BTVN*. |
| **G** | `Thời lượng (phút)` | Number | Thời lượng giải chuẩn. Công thức tính tự động dựa trên mức độ và số ý. |
| **H** | `Thực tế` | Boolean | `TRUE` nếu là bài toán ứng dụng thực tế có lời văn; `FALSE` nếu là toán thuần túy. |
| **I** | `Format` | Text | `Tự luận` \| `Trắc nghiệm chọn đáp án` \| `Điền khuyết` \| `Đúng sai` \| `Nối cột`. |
| **J** | `Mức độ từng ý` | Text | Phân rã mức độ từng ý: `a) TH · b) VD · c) VDC`. |
| **K** | `Bài học SGK` | Text | Tên bài SGK Kết nối tri thức tương ứng (ví dụ: *Bài 15: Tiếp tuyến của đường tròn*). |
| **L** | `Ghi chú` | Text | Ghi chú kỹ thuật, lưu ý hình vẽ, bẫy sai lầm của học sinh. |
| **M** | `Mã câu` | Text (Unique) | Mã định danh duy nhất của câu (ví dụ: `9H5-P02-001`, `9H5-P02-002-nb1`). Khóa liên kết với phiếu. |

#### Phân khu II: Phân loại sư phạm & Giàn giáo leo dốc (Cột N – X)
| Cột | Tên trường | Kiểu dữ liệu | Ý nghĩa sư phạm & Quy chuẩn điền |
|:---:|:---|:---:|:---|
| **N** | `Phân loại câu` | Text | 7 loại câu hỏi §4b: `NB lẻ LT`, `NB tách TH`, `NB ghép bài`, `TH lẻ LT`, `TH ghép bài`, `TH tách VD`, `VD lẻ` + `NB kiến thức cũ`. |
| **O** | `Đề xuất thuyết minh` | Text | Máy tự động điền: Câu đang được phiếu nào dùng (`P02 · Ví dụ`, `P02 · Trên lớp`). |
| **P** | `Trạng thái` | Text | `Đang dùng` \| `Dự phòng` \| `Bỏ` (kèm lý do tại sao bỏ, tuyệt đối không xóa dòng). |
| **Q** | `Loại ngay (L1-L5)` | Text | Ghi mã vi phạm nếu câu dính bộ lọc: `L1` (sai kiến thức), `L2` (lệch SGK), `L3` (nghiệm xấu), `L4` (cồng kềnh), `L5` (trùng đề trên lớp). |
| **R** | `Đã soi ảnh` | Text | `Đã soi` (đã đối chiếu ảnh scan đề gốc rõ nét) \| `Chưa` (mới lấy từ text cần rà soát lại). |
| **S** | `Lớp C` | Text | `Phù hợp` \| `Không` (Đánh dấu mức độ phù hợp với đối tượng học sinh trung bình - yếu). |
| **T** | `Lớp B` | Text | `Phù hợp` \| `Không` (Phù hợp học sinh khá). |
| **U** | `Lớp X` | Text | `Phù hợp` \| `Không` (Phù hợp lớp chuyên / chất lượng cao). |
| **V** | `Chọn tay` | Text | Vùng Giáo viên/Thầy nhập tay: `Bắt buộc chọn` \| `Bỏ` \| `Đổi vị trí` (Đè lên kết luận của máy). |
| **W** | `Loại nguồn` | Text | `Đề thi thật Hà Nội` \| `SGK KNTT` \| `SBT KNTT` \| `Thi thử chất lượng`. |
| **X** | `Có hình · ảnh chụp` | Text | Đường dẫn file ảnh hình vẽ hoặc ghi chú `TikZ vẽ sẵn`. |

#### Phân khu III: Bóc tách ý con & Kỹ thuật đề thật (Cột Y – AE)
| Cột | Tên trường | Kiểu dữ liệu | Ý nghĩa sư phạm & Quy chuẩn điền |
|:---:|:---|:---:|:---|
| **Y** | `Mã bài gốc` | Text | Mã câu của bài toán gốc trước khi bóc tách (dùng liên kết chuỗi câu hạ bậc). |
| **Z** | `Dạng từng ý trong đề thật` | Text | Mô tả chi tiết yêu cầu toán học của từng ý trong đề thi thật. |
| **AA** | `T7 gợi ý` | Text | Gợi ý mức độ bám sát cấu trúc đề thi tuyển sinh vào 10 Hà Nội. |
| **AB** | `Kỹ thuật giải` | Text | Kỹ thuật trọng tâm (ví dụ: *Tam giác đồng dạng c-g-c*, *Hệ thức lượng*, *Bắc cầu góc nội tiếp*). |
| **AC** | `Chương` | Text | Ký hiệu nhãn chương dạng chuẩn: `[I]`, `[II]`, `[V]`, `[IX]` (có ngoặc vuông để tránh trùng chuỗi). |
| **AD** | `Nhóm nghi trùng` | Text | Nhóm các bài có cùng cấu hình hình học hoặc bối cảnh để tránh chọn trùng đề. |
| **AE** | `Cần soát đề` | Text | Đánh dấu cảnh báo các câu cần kiểm tra lại nghiệm hoặc hình vẽ. |

#### Phân khu IV: Chấm 8 Tiêu chí chất lượng T1 – T8 (Cột AF – AM)
> Thang điểm cho từng tiêu chí: `0` (Chưa đạt), `1` (Đạt mức cơ bản), `2` (Rất tốt, xuất sắc).
| Cột | Tiêu chí | Điểm tối đa | Nội dung đánh giá |
|:---:|:---|:---:|:---|
| **AF** | `T1 Trọng tâm SGK` | 2 | Bám sát yêu cầu cần đạt của chuẩn chương trình SGK GDPT 2018. |
| **AG** | `T2 Ý toán` | 2 | Tính trong sáng, mạch lạc về mặt tư duy toán học, không mẹo vặt đánh đố. |
| **AH** | `T3 Bối cảnh` | 2 | Bối cảnh thực tế tự nhiên hoặc cấu hình hình học đẹp, chuẩn mực. |
| **AI** | `T4 Phân hoá ý con` | 2 | Phân hóa rõ ràng từ câu dễ (NB/TH) đến câu chốt chặn (VD/VDC). |
| **AJ** | `T5 Lỗi sai kinh điển` | 2 | Giúp phát hiện và khắc phục các bẫy sai lầm điển hình của học sinh. |
| **AK** | `T6 Vừa sức, nghiệm đẹp` | 2 | Tính toán vừa phải, nghiệm số nguyên hoặc phân số gọn gàng, không số lẻ vô tỉ xấu. |
| **AL** | `T7 Dạng đề thi` | 2 | Trùng khớp với khuôn dạng bài xuất hiện thường xuyên trong đề thi thật Hà Nội. |
| **AM** | `T8 Mở rộng` | 2 | Có khả năng phát triển mở rộng cho các bài toán tiếp theo. |

#### Phân khu V: Đánh giá & Kết luận phân tầng tự động (Cột AN – AU)
| Cột | Tên trường | Công thức Google Sheets chuẩn | Ý nghĩa sư phạm |
|:---:|:---|:---|:---|
| **AN** | `Điểm lớp C` | `=ROUND((AF6*3 + AG6*1 + AH6*2 + AI6*1 + AJ6*2 + AK6*2 + AL6*2 + AM6*0)/(2*13)*10, 1)` | Chuẩn hóa điểm thang 10 theo trọng số Lớp C (Tổng $W_C = 13$). |
| **AO** | `Điểm lớp B` | `=ROUND((AF6*2 + AG6*2 + AH6*2 + AI6*2 + AJ6*2 + AK6*2 + AL6*2 + AM6*2)/(2*16)*10, 1)` | Chuẩn hóa điểm thang 10 theo trọng số Lớp B (Tổng $W_B = 16$). |
| **AP** | `Điểm lớp X` | `=ROUND((AF6*1 + AG6*2 + AH6*1 + AI6*2 + AJ6*2 + AK6*2 + AL6*2 + AM6*2)/(2*14)*10, 1)` | Chuẩn hóa điểm thang 10 theo trọng số Lớp X (Tổng $W_X = 14$). |
| **AQ** | `Ngưỡng theo mức` | `=IF(OR(C6="VD",C6="VDC"), 7.0, IF(C6="TH", 6.0, 5.0))` | Ngưỡng điểm tối thiểu để được chọn vào bài dạy: VD/VDC $\ge 7.0$; TH $\ge 6.0$; NB $\ge 5.0$. |
| **AR** | `Kết luận lớp C` | `=IF(Q6<>"","LOẠI", IF(V6<>"","CHỌN TAY", IF(AN6>=AQ6,"ĐƯA VÀO BÀI","DỰ PHÒNG")))` | Tự động phân loại: Đưa vào bài chính, Đưa vào kho dự phòng hoặc Loại bỏ. |
| **AS** | `THẦY DUYỆT` | Dropdown (`Chờ duyệt`, `Hay`, `Không hay`) | Quyết định sư phạm cuối cùng của Thầy phụ trách chuyên môn. |
| **AT** | `Lí do chấm` | Text | Tóm tắt lý do chấm điểm và ưu thế vượt trội của câu hỏi. |
| **AU** | `Năm đầu của năm học đề` | Number (ví dụ: `2024`) | Lọc chuẩn niên giám: Ưu tiên tuyển sinh từ năm học 2024 trở đi. |

### 3. Bảng quy chuẩn mã màu trực quan (Conditional Formatting)
Nhằm giúp Giáo viên nhận biết tức thì trạng thái câu hỏi khi mở Sheet, toàn bộ hàng hoặc ô được tự động tô màu theo quy chuẩn:

| Mã màu Hex | Tên màu | Vùng áp dụng | Ý nghĩa nghiệp vụ |
|:---:|:---|:---|:---|
| `#FCE4D6` | Cam nhạt | Cột `Mức độ` (VD/VDC) & Cột `Ưu tiên` (Ưu tiên 4) | Nhận diện ngay bài chốt đích buổi học hoặc câu cảnh báo loại bỏ. |
| `#FFF2CC` | Vàng kem | Cột `THẦY CHỌN` & Cột `Ghi chú thay thế` | Vùng nhập liệu dành riêng cho con người, máy không được đè lên. |
| `#E2EFDA` | Xanh lá nhạt | Cột `Kết luận lớp C` ("Đưa vào bài") & Câu đã chọn vào phiếu | Câu đạt chuẩn chất lượng cao, đang được sử dụng chính thức. |
| `#FFE699` | Vàng tươi | Cột `Mã câu` cho câu mới soạn (`MỚI·...`, `·nb1`, `·th1`) | Cảnh báo câu do người/AI mới biên soạn, cần rà soát kỹ tính chính xác. |
| `#EDE7F6` | Tím Lavender | Cột `Phân loại câu` mang nhãn `NB kiến thức cũ` | Câu đệm kiểm tra kỹ năng lớp dưới/bài trước (Chặng Khám phá). |
| `#FCE4EC` | Hồng phấn | Cột `Kết luận lớp C` mang nhãn `LOẠI` (dính L1–L5) | Câu vi phạm nguyên tắc sư phạm, loại bỏ khỏi ngân hàng bài giảng. |

---

## TEMPLATE 2: TAB THUYẾT MINH LIÊN KẾT ĐỘNG (DYNAMIC SPEC SHEET)

### 1. Ý nghĩa & Vai trò
* Là **bản kiến trúc sư phạm (Blue-print)** của buổi học trước khi biên soạn mã code JSON/LaTeX.
* Tuân thủ triệt để nguyên lý **Spec-First**: Thầy chốt khung dạng bài và số phút trước, người soạn chỉ việc bốc câu theo đúng mã đã duyệt.
* Tự động cân đối quỹ thời lượng (90' hoặc 120') và cơ cấu tỉ lệ năng lực (40% NB - 40% TH - 20% VD).

### 2. Cấu trúc bảng thuyết minh chi tiết
Mỗi dòng trong tab Thuyết minh tương ứng với một Dạng bài toán cụ thể:

| Cột | Tên trường | Ý nghĩa & Cách điền | Ví dụ mẫu |
|:---:|:---|:---|:---|
| **A** | `STT` | Thứ tự xuất hiện trong buổi học. | `1`, `2`, `3`... |
| **B** | `Loại câu (§4b)` | 1 trong 7 nhãn chuẩn: `NB lẻ LT`, `NB tách TH`, `NB ghép bài`, `TH lẻ LT`, `TH ghép bài`, `TH tách VD`, `VD lẻ` + `NB kiến thức cũ`. | `NB tách TH` |
| **C** | `Dạng bài` | Tên dạng bài toán cụ thể (Mọi công thức toán bắt buộc kẹp `$ ... $`). | `Chứng minh $DB$ là tiếp tuyến của $(O)$` |
| **D** | `Mục tiêu kiến thức` | Yêu cầu cần đạt về mặt năng lực và chuẩn đầu ra điểm số. | `Nhận diện góc vuông tại tiếp điểm; áp dụng c.c.c` |
| **E** | `Lý thuyết (phút)` | Số phút GV nhắc lại kiến thức (Chỉ điền cho vài dạng cốt lõi, không điền tràn lan). | `2` |
| **F** | `Ví dụ mẫu (câu)` | Số câu GV chữa mẫu cùng học sinh tại Chặng 2. | `1` |
| **G** | `Trên lớp (câu)` | Số câu học sinh tự làm trên lớp (Chặng 1, Chặng 3, Chặng 4). | `2` |
| **H** | `BTVN (câu)` | Số câu giao về nhà tự luyện (gương 1-1 với bài trên lớp). | `2` |
| **I** | `Mã câu đề xuất` | Mã câu lấy từ Cột M của Template 1 (`source_refs`). | `9H5-P02-003-nb1` |
| **J** | `THẦY CHỌN & ĐỔI CÂU` | Vùng Thầy nhập mã câu khác nếu muốn thay đổi đề bài. | `9H5-P02-015` |
| **K** | `Chốt mã` | Công thức: `=IF(J6<>"", J6, I6)`. | `9H5-P02-003-nb1` |
| **L** | `Phút trên lớp` | Tự động tính theo rate: $NB = 1.5'$, $TH = 6.0'$, $VD = 12.0'$, $Vẽ hình = +5.0'$. | `3.0` |
| **M** | `Phút BTVN` | Tự động tính thời gian học sinh làm tại nhà. | `2.4` |

### 3. Khối Dashboard Tổng hợp & Cân đối quỹ giờ (Tự tính bằng công thức)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                       DASHBOARD CÂN ĐỐI THỜI LƯỢNG CA HỌC 90 PHÚT (LỚP C)                         │
├────────────────────────────────┬─────────────────────────────────┬────────────────────────────────┤
│ 1. TỈ LỆ NĂNG LỰC HỌC SINH     │ 2. PHÂN BỔ THỜI LƯỢNG BUỔI HỌC  │ 3. TRẠNG THÁI GÁC CỔNG         │
│ • Nhận biết (NB):   40% (48')  │ • GV Giảng & Mẫu:    25.0 phút  │ • Tỉ lệ phân tầng:  ✓ ĐẠT      │
│ • Thông hiểu (TH):  40% (48')  │ • HS Luyện trên lớp: 55.0 phút  │ • Giờ trên lớp:     ✓ ĐẠT (80')│
│ • Vận dụng (VD):    20% (24')  │ • Nghỉ giải lao:     10.0 phút  │ • Giờ BTVN:         ✓ ĐẠT (42')│
│ • Vận dụng cao:      0% (CẤM)  │ • BTVN tự luyện:     42.0 phút  │ • Thuyết minh Gate: PASS       │
└────────────────────────────────┴─────────────────────────────────┴────────────────────────────────┘
```

* **Công thức phân bổ vàng Lớp C (120 phút)**: 16 dạng NB cụ thể (48') + 4 dạng TH cụ thể (48') + 2 dạng VD cụ thể (24') = Đúng 120.0 phút.
* **Cổng tự động kiểm tra (`thuyetminh_gate`)**: Tự động chặn và báo đỏ nếu:
  1. Quỹ giờ trên lớp vượt quá $\pm 10\%$ so với chuẩn.
  2. Xuất hiện câu VDC ở lớp C.
  3. Quá 3 câu NB cho 1 dạng bài vụn vặt.
  4. Thiếu cột nhãn Loại câu §4b hoặc dòng đỏ cảnh báo chưa khai.

---

## TEMPLATE 3: MA TRẬN & ĐẶC TẢ ĐỀ KIỂM TRA CHƯƠNG 45' & ĐỀ THI GK/CK

### 1. Ý nghĩa & Vai trò
* Đảm bảo tính khoa học của đề kiểm tra đánh giá theo nguyên lý khảo thí hiện đại (CTT Parallel Forms).
* Kiểm soát chặt chẽ cơ cấu **3 hình thức câu hỏi bắt buộc** và **luật rải nguồn đề thật Hà Nội**.
* Nghiêm cấm tuyệt đối việc trùng lặp số liệu với bài tập đã học trên lớp.

### 2. Cấu trúc Tab Ma trận đề chuẩn 3 hình thức (L_KTC 3 / L_GKCK)
Thang điểm chuẩn 10,0 điểm được cơ cấu như sau:

| STT | Phần / Hình thức câu hỏi | Mức độ | Số câu | Điểm từng câu | Tổng điểm | Mục tiêu đánh giá |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **Phần I** | **Trắc nghiệm 4 lựa chọn (A/B/C/D)** | NB & TH | 4 – 8 câu | 0,25đ – 0,5đ | **2,0 điểm** | Quét nhanh toàn bộ định nghĩa, tính chất, công thức cốt lõi của chương. |
| **Phần II** | **Điền khuyết / Trả lời ngắn** | NB & TH | 2 – 4 chỗ điền | 0,25đ – 0,5đ | **1,0 điểm** | Kiểm tra ĐKXĐ, giá trị biên, số mũ, tên định lý, bù trừ lỗi sai kinh điển. |
| **Phần III** | **Tự luận ngắn** | TH & VD | 3 – 4 bài toán | 1,5đ – 3,0đ | **7,0 điểm** | Đánh giá năng lực suy luận logic, lập luận hình học hoặc giải bài toán thực tế. |
| **TỔNG** | **Toàn bộ đề thi (45' hoặc 90')** | **NB 40% - TH 40% - VD 20%** | **10,0 điểm** | Đánh giá chẩn đoán toàn diện lỗ hổng kiến thức. |

### 3. Bảng Kiểm soát Rải nguồn Đề thi thật Hà Nội (T_GKCK 5)
Để tránh thiên vị phong cách ra đề của một trường/quận cụ thể, mỗi đề thi phải được đối chiếu qua bảng rải nguồn:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           BẢNG KIỂM SOÁT PHÂN BỔ NGUỒN ĐỀ THI HÀ NỘI                             │
├────────────────────┬──────────────────┬──────────────┬─────────────┬─────────────────────────────┤
│ Quận / Huyện       │ Trường THCS      │ Năm học      │ Số điểm     │ Tỉ lệ % (Giới hạn: ≤ 40%)   │
├────────────────────┼──────────────────┼──────────────┼─────────────┼─────────────────────────────┤
│ Hoàn Kiếm          │ THCS Trưng Vương │ 2024–2025    │ 2,5 điểm    │ 25.0%  [✓ Hợp lệ]           │
│ Cầu Giấy           │ THCS Cầu Giấy    │ 2024–2025    │ 3,0 điểm    │ 30.0%  [✓ Hợp lệ]           │
│ Long Biên          │ THCS Ái Mộ       │ 2024–2025    │ 2,5 điểm    │ 25.0%  [✓ Hợp lệ]           │
│ Ba Đình            │ THCS Giảng Võ    │ 2024–2025    │ 2,0 điểm    │ 20.0%  [✓ Hợp lệ]           │
├────────────────────┴──────────────────┴──────────────┼─────────────┼─────────────────────────────┤
│ TỔNG SỐ QUẬN: 4 quận (Quy chuẩn: ≥ 4 quận)           │ 10,0 điểm   │ 100.0% [✓ ĐẠT CHUẨN]        │
└──────────────────────────────────────────────────────┴─────────────┴─────────────────────────────┘
```

* **Luật cứng (05/11/2026)**:
  * 100% đề lấy từ năm học **2024–2025 trở đi** (chương trình GDPT 2018 hoàn tất cuốn chiếu).
  * 100% đề thi của các trường/phòng GD&ĐT thuộc **Hà Nội**.
  * Cấm copy text OCR; 100% đối soát từ ảnh scan gốc.

---

## TEMPLATE 4: TAB QUẢN TRỊ TIẾN ĐỘ & BÀN GIAO HỌC LIỆU

### 1. Ý nghĩa & Vai trò
* Giúp Tổ trưởng học liệu, Giáo viên và Trợ lý AI đồng bộ trạng thái làm việc theo thời gian thực.
* Lưu trữ vĩnh viễn đường link các sản phẩm đã hoàn thiện và được Thầy phê duyệt.

### 2. Cấu trúc Tab Tiến độ chuẩn (Khuôn mẫu TIẾN ĐỘ 9C / 8C / 7C)
Mỗi dòng đại diện cho một Buổi học (Phiếu học tập):

| Cột | Tên trường | Định dạng | Trạng thái / Cách hiển thị |
|:---:|:---|:---:|:---|
| **A** | `Tuần / Ca` | Text | `Tuần 01 · Ca 1`, `Tuần 01 · Ca 2`... |
| **B** | `Mã phiếu` | Text | `9C-H5-P01`, `9C-H5-P02`... |
| **C** | `Tên bài học SGK` | Text | Tên chính thức theo SGK Kết nối tri thức. |
| **D** | `Link Sheet Phân dạng` | Hyperlink | Link trực tiếp đến Tab Phân dạng chương trên Google Sheets. |
| **E** | `Link Spec Thuyết minh` | Hyperlink | Link mở bản PDF Thuyết minh đã được Thầy duyệt. |
| **F** | `Trạng thái Thẩm định` | Dropdown | `🟡 Đang soạn` $\to$ `🟠 Chờ Thầy duyệt` $\to$ `🟢 ĐÃ DUYỆT`. |
| **G** | `Link Handout Học sinh` | Hyperlink | Link file PDF phát cho học sinh trên Google Drive. |
| **H** | `Link Sổ tay Giáo viên` | Hyperlink | Link file PDF có đáp án chi tiết và gợi ý sư phạm. |
| **I** | `Link Slide Trình chiếu` | Hyperlink | Link file Beamer PDF / Slide HTML tương tác 16:9. |
| **J** | `Link Đề kiểm tra 45'` | Hyperlink | Link tờ đề và ma trận đáp án bài kiểm tra cuối chương. |
| **K** | `Nghiệm thu & Bàn giao` | Checkbox | Tích xanh `TRUE` khi đã tải và in ấn bàn giao cho cơ sở đào tạo. |

---

## QUY TRÌNH PHỐI HỢP 5 BƯỚC GIỮA GIÁO VIÊN VÀ AI TRÊN CÁC TEMPLATE SHEETS

```
[BƯỚC 1: Quét đề nguồn vào Template 1]
   │
   ▼
[BƯỚC 2: AI phân loại, chấm T1-T8 & Lập Template 2 (Spec)]
   │
   ▼
[BƯỚC 3: GV thẩm định sư phạm trên Template 2 & PDF] ◄──┐
   │                                                    │
   ├── (Chưa ưng: Gõ đổi câu ở cột J) ──────────────────┘
   │
   ▼ (Đạt chuẩn: Báo AI Approve)
[BƯỚC 4: AI xuất bộ 3 PDF & Soạn Đề kiểm tra ở Template 3]
   │
   ▼
[BƯỚC 5: AI đồng bộ lên Drive & Tích xanh hoàn thành ở Template 4]
```

### Hướng dẫn câu lệnh mẫu (Prompt) GV giao tiếp với AI:
1. **Lệnh phân dạng & nạp ngân hàng:**  
   > *"Hãy quét các file đề thi HK1 trong thư mục inputs và điền vào Template 1 phân dạng Chương 5 giúp tôi. Chấm điểm T1-T8 cho lớp C."*
2. **Lệnh tạo thuyết minh từ ngân hàng:**  
   > *"Dựa vào các câu đạt điểm trên 7.0 ở Template 1, hãy lập Template 2 thuyết minh cho Phiếu 2 với tỉ lệ 40-40-20 và thời lượng 90 phút."*
3. **Lệnh đổi câu theo thẩm định của Thầy:**  
   > *"Tôi đã nhập mã câu mới `9H5-P02-015` vào cột THẦY CHỌN ở Template 2. Hãy cập nhật lại spec và build lại 3 bản PDF."*
4. **Lệnh đóng gói & đồng bộ:**  
   > *"Phiếu 2 đã hoàn thiện. Hãy đẩy toàn bộ sản phẩm lên Google Drive và cập nhật link vào Template 4 (Sheet Tiến độ) giúp tôi."*

