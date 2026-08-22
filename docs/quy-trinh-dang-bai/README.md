# Quy trình giải toán theo dạng — bản giao 22/8

Bốn dòng được phân công cho **ThaiTD** trong bảng chia việc của tổ. Mỗi tài liệu có đủ 4 phần theo yêu cầu:

1. **Liệt kê** tất cả các câu trong ngân hàng đề liên quan đến dạng đó;
2. **Quy tắc & cách giải mẫu chung**;
3. **Bảng scaffolding** — từng bước, *vì sao* phải làm bước đó, và bước đó **có ăn điểm trong bài thi không**;
4. **Checklist HS tự kiểm + Rubric 4 mức** để đánh giá HS có làm được hay không.

| Tài liệu | Lớp | Vai trò | Số câu rà được | Trọng số trong đề |
|---|---|---|---|---|
| [Giải bài toán bằng cách lập hệ phương trình](lop9-lap-he-phuong-trinh.md) | 9 | Người 1 (cùng BichVN) | **34 câu / 45 đề** | GK1 100% · CK1 82% · Vào 10 82% (1,0đ) |
| [Giải bài toán tối ưu lợi nhuận](lop9-toi-uu-loi-nhuan.md) | 9 | Người 1 (cùng BichVN) | **17 câu** | GK1 90% · CK1 55% · **Vào 10: không có** (0,5đ cuối đề) |
| [Chứng minh tích có tỉ số lượng giác](lop9-chung-minh-tich-tslg.md) | 9 | Người 1 (cùng AnDV) | **23 câu** | GK1 80% · **Vào 10 3/3 đề Sở (1,5đ — ý đắt nhất)** |
| [Tính chất dãy tỉ số bằng nhau có quy luật](lop7-day-ti-so-bang-nhau.md) | 7 | Người 2 (Người 1: AnDV) | **12 câu / 10 đề CK1** | CK1 6/10 trường (~2,0–2,5đ/đề) |

## Nguồn dữ liệu

- **Lớp 9:** `inputs/refs/de-thi/lop-9/exams/*.json` — 45 đề Hà Nội 2025–2026 (10 GK1, 11 CK1, 10 CK2, 3 GK2, 11 Vào 10), 349 câu đã gắn mã dạng.
- **Lớp 7:** `inputs/refs/de-thi/lop-7/**.pdf` — 21 đề (11 GK1, 10 CK1). **Chưa có ngân hàng JSON**; các câu trong tài liệu được đọc trực tiếp từ text layer và từ ảnh scan.

## Sửa lỗi ngân hàng phát hiện trong quá trình rà

Đã đối chiếu ảnh PDF gốc và sửa **11 câu** trong `inputs/refs/de-thi/lop-9/exams/`:

| File | Câu | Lỗi |
|---|---|---|
| `gk1-ngo-gia-tu.json` | `5b` | Đề chép sai điểm chiếu (BC thay vì **BM**) làm hệ thức trở nên **sai về mặt toán học** |
| | `5c` | Chuẩn hoá kí hiệu, ghi rõ hướng chứng minh chưa đối chiếu HDC |
| | `3-2` | Chép theo HDC gốc vốn **tự mâu thuẫn**; theo đề đúng phải là 500 và 250 nghìn |
| `gk1-van-yen.json` | `4b` | Đề chép sai **cả hai** hệ thức (`HM·AC = HA·HN`, `sin³B`) |
| | `4c` | Đề bỏ trống — đã chép lại đầy đủ |
| | `2-1` | "12 bút bi" → **10 bút bi** |
| | `2-2` | Bổ sung đáp số (AB = 300 km) |
| | `5` | "xe 16 chỗ" → **xe 50 chỗ**, bổ sung giá thuê và đáp số |
| `gk1-thai-thinh.json` | `5` | Đề bị cắt giữa chừng — đã chép lại đầy đủ + đáp số 185 nghìn |
| | `3` | Ghi "nghiệm không nguyên" — thực tế nghiệm nguyên (10 và 240) |
| `gk1-phu-dien.json` | `3-1` | Đáp án **đảo** hai đội |

> **Cách phát hiện:** với hệ thức hình học — thay mọi đoạn thẳng bằng biểu thức của a, b, c rồi so hai vế (xem §2.3 tài liệu tỉ số lượng giác). Với bài đại số — giải lại và đối chiếu ảnh PDF gốc ở 130–170 DPI.

## Còn nợ / cần Thầy xác nhận

- `gk1-co-nhue-2-3-2c` (sin(MQN)·cos(MNP) = HI/QP) — chưa có HDC.
- `gk1-dvhau-4` / `ck1-phuong-ha-dong-5` (cực trị hình học khu vườn chữ U) — chưa có HDC.
- `gk1-van-yen-4c`, `gk1-ngo-gia-tu-5c` — đề đã đúng, hướng chứng minh chưa đối chiếu HDC gốc.
- Lớp 7 **chưa có ngân hàng JSON** — nếu tổ dùng thường xuyên thì nên dựng theo mẫu lớp 9.
