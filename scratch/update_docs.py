with open('docs/quy-chuan-hoc-lieu.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '## 14. Quy chuẩn Đề thi & Phiếu học tập Tiểu học (Lớp 5 — Thông tư 27) (Thầy chốt 08/11/2026)'
end_marker = '### 14.3. Ma trận đề kiểm tra Cuối kì 1 Toán 5 (Thông tư 27 — SGK KNTT)'

start_pos = text.find(start_marker)
end_pos = text.find(end_marker)

replacement = '''## 14. Quy chuẩn Đề thi & Phiếu học tập Tiểu học (Lớp 5 — Thông tư 27) (Thầy chốt 08/11/2026)

### 14.1. Triết lý làm bài trực tiếp & Lưới ô ly chuẩn tiểu học
- **Học sinh làm bài ngay vào đề:** Khác với cấp THCS (học sinh làm bài ra giấy thi / vở ghi riêng), ở cấp Tiểu học (đặc biệt Lớp 5), toàn bộ đề thi định kì và phiếu học tập được thiết kế để **học sinh làm bài trực tiếp vào đề** (`Em làm bài ngay vào đề.`).
- **Bắt buộc có lưới ô ly (`variant: "oly"` / `\\olyline`):**
  - Mọi bài tự luận yêu cầu tính toán hoặc trình bày bài giải bắt buộc phải có **khung lưới ô ly chuẩn tiểu học** (ô vuông lớn 10 mm × 10 mm chia lưới 4 × 4 ô nhỏ 2,5 mm × 2,5 mm, nét mực nhạt `ink!15` và `ink!35`).
  - **Yêu cầu không gian viết bài rộng rãi (Thầy chốt 08/11/2026):** Học sinh tiểu học chữ to, nét tròn; phép tính đặt tính số thập phân (đặc biệt nhân và chia) kéo dài nhiều dòng; bài toán có lời văn gồm 2 bước tính cần tối thiểu 6–8 dòng chữ. Nếu ép khung ô ly quá bé (1,5–2 cm) thì học sinh **hoàn toàn không đủ chỗ viết**. Khung ô ly phải rộng rãi, tương ứng với độ dài bài giải thực tế.
  - **Bài 1 (Đặt tính rồi tính — 1,0 điểm):** Đề bài in 2 dòng gọn (a, b dòng trên; c, d dòng dưới). Phía dưới là **khung ô ly toàn trang cao 12 cm (`count: 12`)** để học sinh tự đặt tính 4 phép tính rộng rãi, thẳng hàng dấu phẩy.
  - **Bài 2 (Tính giá trị biểu thức / Phân số — 1,0 điểm):** Khung ô ly cao 4 cm (`count: 4` = 16 dòng caro nhỏ) để trình bày các bước quy đồng, rút gọn.
  - **Bài 3 (Viết số đo thích hợp vào chỗ chấm — 1,0 điểm):** In 2 dòng gọn, điền trực tiếp vào chỗ chấm `\\dots\\dots\\dots\\dots`, không chiếm diện tích ô ly.
  - **Bài 4 (Bài toán có lời văn thực tế — 2,0 điểm):** Khung ô ly cao 8 cm (`count: 8` = 32 dòng caro nhỏ) đủ chỗ cho 2 câu lời giải, 2 phép tính và đáp số.
  - **Bài 5 (Bài toán tư duy nâng cao M3 — 1,0 điểm):** Khung ô ly cao 6 cm (`count: 6` = 24 dòng caro nhỏ) cho các bước suy luận và tính toán.
  - **Dòng kết thúc:** `\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}` kèm lời dặn dò sư phạm: `Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!`.

### 14.2. Chuẩn căn chỉnh vừa khít đúng 4 trang A4 (1 tờ đôi A3 gập đôi)
- **Quy cách in ấn thực tế Tiểu học:** Đề thi định kì tiểu học làm trực tiếp vào đề chuẩn mực của MathTech và các trường tiểu học được in dưới dạng **1 tờ đôi A3 gập đôi tạo thành 4 trang A4** (hoặc 2 tờ A4 in 2 mặt bấm ghim).
- **Số trang cứng:** Đề thi học sinh (`Phieu-HS.pdf`) **BẮT BUỘC ĐẠT ĐÚNG 4 TRANG (Pages: 4)**:
  - **Trang 1 (Bìa trước):**
    * Top Card thông tin học sinh (Tiêu đề đề thi, Họ và tên, Lớp, Thời gian làm bài 40 phút).
    * Khung Điểm (Số & Chữ) + Lời nhận xét của thầy cô giáo (chiều cao 0,6 cm).
    * Phần I. Trắc nghiệm (4,0 điểm): 6 câu đầu tiên (Câu 1 đến Câu 6), dàn 4 cột A, B, C, D cân đối.
    * Ngắt trang sang Trang 2 (`\\newpage`).
  - **Trang 2 (Mặt trong trái):**
    * Trắc nghiệm tiếp theo: Câu 7 và Câu 8.
    * Tiêu đề: `PHẦN II. TỰ LUẬN (6,0 điểm)`.
    * Bài 1 (1,0 điểm) Đặt tính rồi tính (4 phép tính) kèm **khung ô ly cao 12 cm (`count: 12`)** phủ kín toàn bộ nửa dưới trang 2.
    * Ngắt trang sang Trang 3 (`\\newpage`).
  - **Trang 3 (Mặt trong phải):**
    * Bài 2 (1,0 điểm) Tính phân số/hỗn số kèm khung ô ly cao 4 cm (`count: 4`).
    * Bài 3 (1,0 điểm) Viết số đo thích hợp vào chỗ chấm (4 ý điền chấm).
    * Bài 4 (2,0 điểm) Bài toán thực tế hình học kèm **khung ô ly cao 8 cm (`count: 8`)**.
    * Ngắt trang sang Trang 4 (`\\newpage`).
  - **Trang 4 (Bìa sau):**
    * Tiêu đề: `PHẦN II. TỰ LUẬN (tiếp theo)`.
    * Bài 5 (1,0 điểm) Bài toán tư duy nâng cao M3 kèm khung ô ly cao 6 cm (`count: 6`).
    * Dòng kết bài `--- HẾT ---` và Lời dặn dò của giáo viên tiểu học.

'''

new_text = text[:start_pos] + replacement + text[end_pos:]
with open('docs/quy-chuan-hoc-lieu.md', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated docs/quy-chuan-hoc-lieu.md successfully!")

