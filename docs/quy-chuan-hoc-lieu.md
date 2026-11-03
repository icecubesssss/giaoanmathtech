# Bộ quy chuẩn học liệu — bản tóm tắt trong repo

> **Nguồn sự thật:** Google Sheet "Các đầu việc học liệu"
> (`1NCJHzp0cU9zUaJIkw47UfLzrPUj09P-5prgiGG6erDs`). Các tab: *Xây dựng nguyên tắc học liệu*,
> *Xây dựng bộ quy chuẩn học liệu* (L1–L5, T1–T8, Quy chuẩn 1–4, Cấu trúc 1–5),
> *Quy trình chuẩn AI dựng bài*, *Điểm cần chốt*, *Từ điển nhãn*, *Định mức thời lượng*,
> *Trọng số chấm câu*, *Cột chuẩn tab phân dạng*, *Lịch sử thay đổi*.
>
> File này chỉ chép lại các quyết định Thầy đã chốt ngày 03/11/2026 (12 mục ở tab *Điểm cần chốt*)
> để tác nhân đọc repo là thấy. Sheet và file này lệch nhau thì **theo sheet**, rồi sửa file này.
> Thứ tự ưu tiên khi hai tài liệu nói khác nhau: **Sheet quy chuẩn > file này > AGENTS.md > HUONG-DAN-*.md**.

## 1. Chấm câu (L1–L5, T1–T8)

- **L1–L5 lọc mọi câu** của tab phân dạng. Câu dính một mã thì ghi mã vào cột "Loại ngay".
- **L5 (trùng ý, chỉ đổi số) chỉ áp cho câu TRÊN LỚP.** BTVN gương 1–1 được đổi số từ bài trên lớp
  (ghi mã câu gốc). Ví dụ mẫu phải cùng dạng nhưng **khác bài** (khác bối cảnh hoặc cấu hình), không chỉ đổi số.
- **Trọng số giữ như sheet:** tổng lớp C = 13, B = 16, X = 14.
  Điểm = Σ(Tᵢ × Wᵢ) / (2 × tổng trọng số của lớp) × 10 — câu 2 điểm mọi tiêu chí luôn được đúng 10.
- **Ngưỡng đưa vào bài dạy chính theo mức của câu:** VD/VDC ≥ 7 · TH ≥ 6 · NB ≥ 5.
  Dưới ngưỡng của mức mình: dự phòng hoặc sửa. Dưới 5 ở mọi mức: loại hoặc sửa.
- Câu **NB kiến thức cũ** chấm T1 theo bài nền nó phục vụ, không chấm 0.

## 2. Hình thức câu hỏi

- **Tiểu học:** bắt buộc đan xen đủ 5 hình thức (trắc nghiệm, điền khuyết, Đúng/Sai, nối cột, tự luận ngắn)
  trên **mọi phiếu**.
- **THCS:** 5 hình thức dùng ở **chặng Khám phá và phiếu ôn tập**. Các chặng Luyện tập giữ luật
  **không dùng câu NB rời rạc** — NB là bước của một bài lớn (giàn giáo), hoặc NB kiến thức cũ.
- Khai trong `problem` (từ 03/11/2026): `options` (trắc nghiệm A–D), `dung_sai` (danh sách khẳng định, HS đánh Đ/S),
  `noi_cot_trai` + `noi_cot_phai` (bảng nối, cột B đã xáo); đáp án ghi ở `answer` ("a) Đ · b) S", "1 – b · 2 – c").
  Template tự kẻ bảng ở phiếu HS, sổ tay GV, slide và bản Word. Mỗi khẳng định / mỗi dòng cột A tính là một câu
  khi đếm quỹ phút.

## 3. Thời lượng

- **Một bảng định mức duy nhất:** `config/tier_spec.json` (chép sang tab *Định mức thời lượng*).
  Phút/câu theo khối × vai trò (GV giảng ví dụ / HS làm trên lớp / BTVN) × mức.
- **Bài nhiều ý:** mỗi ý là một câu theo mức của ý đó, cộng lại. HS tự vẽ hình: +5′ một lần cho cả bài.
  Ví dụ lớp 9, trên lớp, "a) NB · b) TH · c) VD" = 1,5 + 6 + 12 = 19,5′.
- Cột "Thời lượng" trên tab phân dạng tính bằng công thức theo mức độ, không ước lượng tay.

## 4. Nguồn câu

- Thứ tự ưu tiên 1 → 4 (đề thi chính thức → SGK → nguồn khác → không bám SGK mới).
- **Tiểu học:** không đặt tỉ lệ cứng, theo cách lớp 5 đang làm.
- **THCS lớp C:** tính theo **bài gốc** (câu NB tách từ bài đề thi vẫn tính là đề thi), áp cho câu trên lớp:
  **đề thi thật ≥ 50% · SGK ≥ 20% · sách tham khảo ≤ 30%**.

## 5. Tab phân dạng

- Cột A–M dùng chung mọi khối (tab *Cột chuẩn tab phân dạng*); từ cột N: Phân loại câu, Đề xuất thuyết minh,
  Trạng thái, Loại ngay, Đã soi ảnh, Lớp C/B/X, Chọn tay, Loại nguồn, Có hình, **Mã bài gốc**.
- **Dòng cộng dồn là chuẩn cho tab mới:** bài nhiều ý tăng mức có thêm dòng "… - a", "… - a - b", mỗi dòng chép đủ
  giả thiết. Tab lớp 9 đã có (một dòng mỗi bài + cột "Mức độ từng ý") giữ nguyên, repo tự suy ra dòng cộng dồn.
- **Bốc câu liền mạch:** mỗi bài gốc chỉ bốc **một** dòng; các câu trong phiếu đi theo mạch kiến thức của bài,
  cùng mục tiêu, từ dạng nền đến dạng đích; không bốc câu lẻ ngoài mục tiêu chỉ để đủ số.
- **Không xoá dòng:** bỏ câu thì ghi "Bỏ" (kèm lí do) ở cột Trạng thái. Mã câu không sửa sau khi cấp.
- **Ô "Chọn tay" của Thầy đè lên luật xếp lớp của máy.**
- Quét đề bằng **ảnh**; không lấy chữ pdftotext/OCR làm đề (vụ chương IV 9C, 03/11/2026).
- File phân dạng phải là **Google Sheet gốc**, không dùng .xlsx (connector không đọc được).

## 6. Câu lấy kết quả ý trước làm giả thiết

Chỉ làm ý VDC, kết quả ý a, b ghi thành giả thiết. Điều kiện: (1) chỉ ghi kết quả của a, b, không ghi cách làm;
(2) là câu soạn mới, mã `MỚI·<mã gốc>`, phút tính bằng một câu VDC; (3) dùng ở phiếu ôn, chuyên đề VDC hoặc BTVN
sau khi HS đã làm trọn bài đó ít nhất một lần; (4) lớp C không dùng.

## 7. Lớp

| Lớp | Học sinh | Đích | Trần |
|---|---|---|---|
| C | nền trung bình – yếu | chắc kiến thức SGK, điểm kiểm tra trên trường | VD |
| B | trung bình – khá | kỳ I (GK1, CK1) trần **9,5–10**; kỳ II (GK2, CK2) trần **9–9,5** | VDC, ít câu VDC hơn lớp A; câu cuối dạy theo tỉ lệ ra đề |
| A | khá – giỏi | điểm tối đa trên trường | VDC, dày hơn lớp B |
| X | giỏi, thi trường chất lượng cao / chuyên | làm được cả câu cuối đề | VDC |

## 8. Nơi làm việc

| Việc | Làm ở đâu | Duyệt ở đâu |
|---|---|---|
| Luật | Sheet quy chuẩn | Sheet |
| Phân dạng, chọn câu, chấm | Google Sheet gốc, mỗi khối một file, mỗi chương một tab | Sheet |
| Thuyết minh | repo (`thuyet-minh.json`) → PDF; số câu/phút xem trước trên Sheet | **PDF** |
| Phiếu | repo → 3 PDF → Drive (chỉ sau approve) | PDF |
| Tiến độ | sheet tiến độ nhóm, tab theo khuôn 7C (vd "TIẾN ĐỘ 9C - 2026 - ThaiTD") | Sheet |
