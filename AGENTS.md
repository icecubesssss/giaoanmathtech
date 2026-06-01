# AGENTS.md — Hướng dẫn cho MỌI tác nhân AI (Claude Code, Codex, Antigravity, Copilot, Gemini CLI…)

> Nguồn GỐC DUY NHẤT cho mọi công cụ AI. Các file CLAUDE.md / .github/copilot-instructions.md / GEMINI.md chỉ trỏ về đây.

Đây là **MathTech Engine**: soạn phiếu học tập Toán lớp 9 (ôn thi vào 10) từ PDF nguồn của Thầy → render ra 3 bản PDF (handout HS / guide GV / slide).

## Luật CỨNG độc lập công cụ — chạy `validate`
Dù bạn là Claude, Codex, Antigravity, Copilot hay người không dùng AI: mọi luật kiểm được tự động đều nằm trong **code Python**, không phải prompt. Chỉ cần chạy `python -m src.main validate <file.json>` (và `python -m pytest`) là nhận **cùng một bộ gác cổng** (sanitizer/schema/difficulty/visual_linter/gradient + SymPy). **Bắt buộc** validate sạch trước khi `approve`/`build`. Các nguyên tắc dưới đây là phần *con người/tác nhân* phải tự giữ (validator không soi được).

## Quy trình mỗi phiếu
```bash
python -m src.main new-lesson <folder-tuần>   # sinh khung 5 chặng
# → điền nội dung BÁM PDF nguồn trong folder (xem HUONG-DAN-SOAN-BAI.md)
python -m src.main validate <file.json>        # cổng: sanitizer/schema/difficulty/linter/gradient
python -m src.main approve <slug>              # Thầy duyệt
python -m src.main build <file.json>           # 3 PDF
```
Kế hoạch tuần: [KE-HOACH-SOAN-BAI.md](KE-HOACH-SOAN-BAI.md). Luật soạn chi tiết: [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md).

## Nguyên tắc BẮT BUỘC khi soạn (bám HUONG-DAN §0)
1. **KHÔNG bịa đề** — lấy từ PDF nguồn; thiếu dạng thì hỏi Thầy.
2. **Đáp án phải đúng** — `validate` chạy SymPy đối chiếu (đại số); hình học tự kiểm tay.
3. **Human-in-the-loop** — soạn → validate → Thầy duyệt → build. Không in khi chưa approve.
4. **CHƯA CHẮC CÁCH DẠY THÌ HỎI THẦY (không tự đoán).** Khi không chắc nên *dẫn dắt / scaffolding* một dạng thế nào (lời giải mẫu, mức chia bước, ví dụ mồi, chỉnh độ dốc) → **liệt kê bài/dạng phân vân và hỏi Thầy trước** rồi mới soạn. Validator không thể biết bạn đang phân vân — đây là kỷ luật của tác nhân.
5. **Scaffolding cho dạng dễ trừu tượng.** Làm chung–làm riêng, đặt ẩn phụ, chuyển động/dòng nước, %… nên có **một ví dụ mồi cụ thể** trước bài chính. Mẫu cách dạy Thầy đã nêu:
   - *Làm chung–làm riêng* → pizza 8 miếng (A ăn 16′, B ăn 24′ → mỗi phút $\tfrac1{16}+\tfrac1{24}$) để dẫn vào $\tfrac1x$.
   - *Dòng nước* → con thuyền không động cơ trôi theo dòng → $v_{xuôi}=v+v_{nước}$, $v_{ngược}=v-v_{nước}$.
   - *Phần trăm* → hỏi "tăng 10% là 10% hay 110%? đề tính theo cái gì" (nhiều thêm vs phải trả tất cả).
6. **Ưu tiên "nghiệm đẹp" cho bài đại số** — được phép chỉnh số liệu đề cho nghiệm gọn (số nguyên); soi lại bằng SymPy. (Lượng giác/đo đạc thì đáp số gần đúng/tỉ số là bình thường.)
7. **Escape `\%` `\&` `\#`** trong MỌI field (kể cả `solution`/`teacher_note`). `visual_linter` nay có cảnh báo; `%`/`#` thô sai mọi nơi, `&` thô chỉ sai ngoài `$...$`.

## Đổi `config/difficulty_profile.json` khi sang chương mới
Trước khi soạn **bài đầu chương**, cập nhật `ceiling/floor/ramp/core_techniques/hook_forbidden_patterns` theo bảng trong [KE-HOACH-SOAN-BAI.md](KE-HOACH-SOAN-BAI.md). Profile là file toàn cục — chỉnh theo chương đang soạn.

## Bố cục CỐ ĐỊNH — không đụng template
Header/logo/watermark/footer/chữ ký/badge chặng do template lo (xem HUONG-DAN §6). Tác nhân chỉ điền nội dung JSON theo schema, không sinh mã LaTeX giao diện. **Ngoại lệ:** block `figure` cho phép mã TikZ thô (hình hình học) — đây là *nội dung* toán, không phải giao diện; ưu tiên TikZ, không dựng chính xác được mới cắt ảnh phiếu gốc (xem HUONG-DAN §4.10). Slide tự bố cục 'chữ trái — hình phải' khi đơn vị dạy có hình.
