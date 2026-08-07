# GitHub Copilot — instructions

Hướng dẫn đầy đủ cho tác nhân ở [../AGENTS.md](../AGENTS.md). Hãy đọc và tuân theo.

> **Chạy trên máy Windows?** Đọc [../HUONG-DAN-BAT-DAU.md](../HUONG-DAN-BAT-DAU.md) §4 trước khi gõ lệnh — `.venv/bin/python` là của macOS, Windows là `.venv\Scripts\python.exe`, và KHÔNG có `make`.

Cốt lõi: chạy `python -m src.main validate <file.json>` (phải sạch) trước `approve`/`build`; KHÔNG bịa đề; đáp án phải đúng; chưa chắc cách dạy thì HỎI Thầy; ưu tiên nghiệm đẹp; escape `\% \& \#` ở mọi field.
