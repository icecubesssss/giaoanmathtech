# Ma trận thống kê — 10 đề GIỮA KÌ I Toán 9 (2025–2026)

> Tổng hợp tự động từ 10 file trong `exams/gk1-*.json`. Sinh lại bằng script ở cuối phần xử lý.
> `điểm TB/đề` = điểm trung bình của dạng đó, **chỉ tính trên các đề có xuất hiện dạng**.

**10 đề:** Bát Tràng, Trưng Vương, Ngô Gia Tự, Nguyễn Du *(có biểu điểm gốc)* · Cổ Nhuế 2, Dịch Vọng Hậu, Phú Diễn, Thái Thịnh, Vân Yên, Nguyễn Bình Khiêm *(scan, đáp án tự dựng — chờ Thầy duyệt)*.

## Theo chương

| Chương | Tần suất | Điểm TB/đề | Nội dung |
|---|---|---|---|
| **C1** | **10/10 (100%)** | ~4,17đ | Phương trình & hệ phương trình bậc nhất |
| **C2** | **10/10 (100%)** | ~2,12đ | Bất đẳng thức & **bất phương trình bậc nhất một ẩn** |
| **C4** | **9/10 (90%)** | ~3,58đ | Hệ thức lượng trong tam giác vuông |
| C3 | 1/10 (10%) | ~3,00đ | Căn thức *(chỉ Thái Thịnh — thường là chủ đề CK1)* |
| C6 | 1/10 (10%) | ~1,50đ | Thống kê & xác suất *(chỉ Phú Diễn)* |

→ **Đề GK1 = C1 + C2 + C4 gần như 100%.** Căn thức (C3) và thống kê-xác suất (C6) hiếm khi vào GK1 — để dành CK1.

## Theo dạng bài (xếp theo tần suất)

| Mã dạng | Tần suất | Số câu | Điểm TB/đề |
|---|---|---|---|
| `DS-THUCTE-LAPHE` — toán thực tế lập hệ | 10/10 (100%) | 12 | ~1,85đ |
| `DS-PT-QUYVE` — giải PT quy về bậc nhất (tích, chứa mẫu) | 10/10 (100%) | 19 | ~1,40đ |
| `HH-TSLG-THUCTE` — ứng dụng tỉ số lượng giác | 9/10 (90%) | 13 | ~0,94đ |
| `DS-HEPT-GIAI` — giải hệ phương trình | 9/10 (90%) | 10 | ~0,86đ |
| **`DS-BPT-GIAI` — giải bất phương trình bậc nhất 1 ẩn** | **9/10 (90%)** | **11** | **~0,86đ** |
| `DS-CUCTRI` — cực trị (câu vận dụng cao cuối đề) | 9/10 (90%) | 9 | ~0,50đ |
| `HH-TSLG-CM` — chứng minh hình tam giác vuông | 8/10 (80%) | 17 | ~1,78đ |
| **`DS-THUCTE-LAPPT-BPT` — toán thực tế lập PT/BPT** | **8/10 (80%)** | **8** | **~1,31đ** |
| `HH-TSLG-TINH` — tính cạnh/góc, giải tam giác vuông | 8/10 (80%) | 11 | ~1,19đ |
| `DS-CAN-TINH-RUTGON` — rút gọn căn | 1/10 (10%) | 4 | ~2,50đ |
| `DS-THONGKE` — đọc biểu đồ | 1/10 (10%) | 1 | ~1,00đ |
| `DS-BDT-CM` — so sánh / chứng minh BĐT | 1/10 (10%) | 1 | ~0,50đ |
| `DS-CAN-CAUPHU` — câu hỏi phụ rút gọn | 1/10 (10%) | 1 | ~0,50đ |
| `DS-XACSUAT` — xác suất biến cố | 1/10 (10%) | 1 | ~0,50đ |

## Chốt cho việc dựng bài "Bất phương trình bậc nhất một ẩn"

Hai dạng liên quan trực tiếp tới bài sắp dạy, **cộng lại ~2 điểm/đề** và xuất hiện ở hầu hết đề:

1. **`DS-BPT-GIAI` (9/10 đề)** — giải BPT thuần. Các kiểu thực tế gặp trong đề:
   - BPT có ngoặc/khai triển: `3x(x−1) − (x+2)(2−x) > (2x+1)² − 7x` (Trưng Vương — ra **vô nghiệm**, dạng bẫy).
   - BPT chứa phân số mẫu số: `1/2 − 3(x+2)/4 ≤ 3 − (x−4)/6` (Trưng Vương, Dịch Vọng Hậu, Phú Diễn…).
   - BPT cơ bản 1 bước: `7x − 14 ≥ 0`, `2(x−3) < 5x` (Bát Tràng, Ngô Gia Tự).
   - **Lưu ý sư phạm:** đề rất hay gài chỗ **đổi chiều khi nhân/chia số âm** (nghiệm `x ≥ −8`, `x ≤ −2`) — cần nhấn mạnh.

2. **`DS-THUCTE-LAPPT-BPT` (8/10 đề)** — lập BPT từ bài toán thực tế (giá trị/điểm nặng hơn, ~1,3đ). Mô-típ:
   - "mua nhiều nhất / ít nhất bao nhiêu" (vở, bút, thùng hàng) → `ax + b ≤ S`.
   - "ít nhất bao nhiêu tháng/ngày" (trả góp, tiết kiệm) → `a·x ≥ S`.
   - "tối thiểu đúng bao nhiêu câu" (thi điểm cộng/trừ) → `5x − 2(20−x) ≥ 74`.

→ Bài mới nên có: 2–3 câu giải BPT (1 câu có phân số, 1 câu khai triển có bẫy dấu/vô nghiệm) + 1–2 bài toán thực tế lập BPT theo mô-típ trên.
