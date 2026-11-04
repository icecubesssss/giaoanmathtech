# CLAUDE.md

> **Hướng dẫn tác nhân của repo này nằm ở [AGENTS.md](AGENTS.md)** (nguồn gốc duy nhất, dùng chung cho mọi công cụ AI). Hãy đọc và bám theo AGENTS.md.

> **Chạy trên máy Windows?** Đọc [HUONG-DAN-BAT-DAU.md](HUONG-DAN-BAT-DAU.md) §4 trước khi gõ lệnh — `.venv/bin/python` là của macOS, Windows là `.venv\Scripts\python.exe`, và KHÔNG có `make`.

Tóm tắt tối quan trọng (chi tiết xem AGENTS.md):
- **Luật cứng: một cuộc trò chuyện = một phiếu** (Thầy chốt 04/11/2026). Phiếu thứ hai ⇒ ghi bàn giao memory, nhắc Thầy mở phiên mới.
- Quy trình: `new-lesson → validate → build (PDF xem trước) → Thầy duyệt (approve)`. **Bắt buộc `validate` sạch** trước khi build. Thầy không đọc JSON — luôn build PDF cho Thầy xem.
- KHÔNG bịa đề · đáp án phải đúng · **chưa chắc cách dạy thì HỎI Thầy** · ưu tiên nghiệm đẹp · escape `\% \& \#`.
