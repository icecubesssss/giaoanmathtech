with open('AGENTS.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '> 3. **LUẬT CỨNG ĐỀ THI & PHIẾU TIỂU HỌC: LÀM TRỰC TIẾP VÀO ĐỀ + LƯỚI Ô LY'
end_marker = '> **NGÂN HÀNG ĐỀ có band + phút (2026-06-21):**'

start_pos = text.find(start_marker)
end_pos = text.find(end_marker)

replacement = '''> 3. **LUẬT CỨNG ĐỀ THI & PHIẾU TIỂU HỌC: LÀM TRỰC TIẾP VÀO ĐỀ + LƯỚI Ô LY RỘNG RÃI + GỌN TRONG ĐÚNG 4 TRANG A4 (TỜ ĐÔI A3) (Thầy chốt 08/11/2026):**
>    - **Làm bài trực tiếp vào đề:** Khác với THCS, học sinh Tiểu học (Lớp 1–5) làm bài trực tiếp vào đề (`Em làm bài ngay vào đề.`).
>    - **Bắt buộc có lưới ô ly (`variant: "oly"` / `\\olyline`):** Mọi bài tự luận bắt buộc chèn lưới ô ly caro nhỏ $2{,}5\\text{ mm}$ bên trong ô vuông lớn $10\\text{ mm}$.
>    - **Đảm bảo không gian viết bài rộng rãi cho HS tiểu học:** Học sinh tiểu học chữ to, đặt tính phép tính số thập phân (cộng, trừ, nhân, chia) kéo dài nhiều dòng; bài toán lời văn 2 bước cần 6–8 dòng; toán tư duy cần 5–6 dòng. Cấm ép khung ô ly quá bé khiến học sinh thiếu chỗ viết.
>      * *Bài 1 (Đặt tính rồi tính — 1,0đ):* Đề in 2 dòng gọn, phía dưới là **khung ô ly cao $12\\text{ cm}$ (`count: 12`)** phủ kín nửa dưới trang cho HS đặt tính thẳng cột 4 phép tính.
>      * *Bài 2 (Tính giá trị / Phân số — 1,0đ):* Khung ô ly cao $4\\text{ cm}$ (`count: 4` = 16 dòng caro).
>      * *Bài 3 (Viết số đo thích hợp vào chỗ chấm — 1,0đ):* 4 ý chia 2 cột điền thẳng vào chỗ chấm `\\dots\\dots\\dots\\dots` (không tốn ô ly).
>      * *Bài 4 (Bài toán lời văn thực tế hình học/sản lượng — 2,0đ):* Khung ô ly cao $8\\text{ cm}$ (`count: 8` = 32 dòng caro) cho 2 lời giải, 2 phép tính và đáp số.
>      * *Bài 5 (Bài toán tư duy nâng cao M3 — 1,0đ):* Khung ô ly cao $6\\text{ cm}$ (`count: 6` = 24 dòng caro).
>      * Cuối đề: `\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}` và lời dặn dò `Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!`.
>    - **CĂN CHỈNH VỪA KHÍT ĐÚNG 4 TRANG A4 (1 TỜ ĐÔI A3 GẬP ĐÔI):** Bản in HS (`Phieu-HS.pdf`) BẮT BUỘC đạt **đúng 4 trang (Pages: 4)**:
>      * *Trang 1 (Bìa trước):* Top Card + Khung Điểm/Nhận xét + Phần I Trắc nghiệm 6 câu đầu tiên (Câu 1 đến Câu 6).
>      * *Trang 2 (Mặt trong trái):* Trắc nghiệm Câu 7, 8 + Phần II Tự luận Bài 1 kèm khung ô ly cao 12 cm.
>      * *Trang 3 (Mặt trong phải):* Bài 2 (ô ly 4 cm) + Bài 3 (điền chỗ chấm) + Bài 4 (ô ly 8 cm).
>      * *Trang 4 (Bìa sau):* Bài 5 (ô ly 6 cm) + Dòng Hết + Lời dặn dò sư phạm.
>      * Ma trận đề theo Thông tư 27 (M1 35% - M2 40% - M3 25%, 40 phút, thang 10 điểm, chỉ lấy SGK Kết nối tri thức).

'''

new_text = text[:start_pos] + replacement + text[end_pos:]
with open('AGENTS.md', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated AGENTS.md successfully!")

