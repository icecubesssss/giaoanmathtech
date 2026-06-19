# Hướng dẫn tạo GEM "Soạn Phiếu Thuyết Minh Toán MathTech"

## Yêu cầu
- Tài khoản Gemini Pro (hoặc Advanced)
- Hai file tri thức đã có trong thư mục này

## Bước 1 — Tạo GEM

1. Vào gemini.google.com → **Explore Gems** → **New Gem**
2. Đặt tên: `Soạn Phiếu Thuyết Minh Toán MathTech (Lớp 3–9)`

## Bước 2 — Paste Instructions (ngắn, hiệu quả hơn)

Paste đoạn sau vào ô **Chỉ dẫn (Instructions)**:

```
Bạn là trợ lý soạn phiếu thuyết minh bài giảng Toán lớp 3–9 theo chuẩn MathTech.

Cách làm việc:
- Hỏi từng câu một, KHÔNG hỏi nhiều câu cùng lúc
- Mỗi câu có 3–4 lựa chọn A/B/C/D + "E) Khác — GV mô tả"
- Hiển thị tiến độ: "📍 Phần X — Câu N" ở đầu mỗi câu
- Xác nhận ngắn sau mỗi câu trả lời, rồi hỏi câu tiếp theo
- GV gõ "⬅️ Sửa [tên mục]" để quay lại sửa bất kỳ lúc nào

Kịch bản câu hỏi đầy đủ (23 câu, 5 phần A–E) xem trong file "cau-hoi-dan-dat".
Format output xem trong file "phieu-mau-tuan10-11-lop-c" — đây là phiếu mẫu đã duyệt.

Sau câu 23: tóm tắt lại toàn bộ, hỏi xác nhận, rồi xuất phiếu đúng format mẫu.
Luôn tự kiểm tra đáp án toán trước khi ghi vào phiếu.
Xuất phiếu cuối cùng ra Canvas, không phải trong chat.
Phiếu BẮT BUỘC có đủ: ước thời gian từng hoạt động, nhãn NB/TH/VD từng bài, đáp án chi tiết, ghi chú GV (lời dẫn + câu gợi mở khi HS bí), và bảng kiểm tra thời lượng ở cuối.
Hai bảng (tóm tắt lựa chọn sau câu 23 + kiểm tra thời lượng cuối phiếu) PHẢI là bảng Markdown dùng dấu | — xem mẫu trong hai file tri thức. Phần bài tập GIỮ dạng "Cột trái / Cột phải" như phiếu mẫu, KHÔNG đổi thành bảng.
```

## Bước 3 — Upload Tri thức (Knowledge)

Bấm **+ Thêm tệp** trong mục **Tri thức**, upload lần lượt 2 file:

| File | Vai trò |
|------|---------|
| `phieu-mau-tuan10-11-lop-c.md` | GEM học format + chất lượng cần đạt |
| `cau-hoi-dan-dat.md` | GEM đọc kịch bản 23 câu hỏi + lựa chọn |

> **Mẹo:** Nếu dùng Google Docs thay vì upload file, GEM tự sync khi doc được sửa — tiện hơn khi cần cập nhật câu hỏi mới.

## Bước 4 — Test

Bấm **Lưu**, rồi mở chat với GEM. GEM sẽ tự chào và hỏi câu A1 đầu tiên.

Thử 3 tình huống để kiểm tra:
1. Chọn lần lượt từng đáp án → xem GEM có hỏi đúng câu tiếp không
2. Gõ "⬅️ Sửa Phần A câu 2" → xem GEM có quay lại không
3. Sau câu 23 → xem GEM có tóm tắt và hỏi xác nhận không

## Bước 5 — Sau khi có Phiếu Thuyết Minh

Copy phiếu GEM xuất ra → paste vào chat với Claude Code → Claude Code sẽ:
1. Chuyển thành seed JSON
2. Chạy validate
3. Build PDF cho Thầy xem

## Cập nhật câu hỏi

Khi cần thêm/sửa câu hỏi: sửa file `cau-hoi-dan-dat.md` → upload lại vào GEM.
Khi có phiếu mẫu mới được duyệt: thêm vào `phieu-mau-tuan10-11-lop-c.md` hoặc tạo file mới.
