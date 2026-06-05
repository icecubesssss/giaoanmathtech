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
python -m src.main build <file.json>           # validate sạch → BUILD PDF (3 bản) cho Thầy XEM TRƯỚC
python -m src.main build-folder <folder-tuần>  # build MỌI phiếu trong folder (phieu-a+phieu-b…), không sót
python -m src.main approve <slug>              # Thầy xem PDF rồi DUYỆT (sửa lại thì build lại)
```
> **Build để xem trước (Thầy yêu cầu):** soạn xong thì build ngay ra PDF cho Thầy xem (JSON Thầy không đọc được). `build`/`build-folder` nay **tự chạy `validate` trước, còn vi phạm thì chặn** (đúng luật "validate sạch trước build") — cần build nháp khi chưa sạch thì thêm `--force`. `build` KHÔNG bị chặn bởi `approve`; `approve` là dấu Thầy chốt sau khi xem PDF. Folder nhiều phiếu thì dùng `build-folder` để khỏi sót phiếu nào.

## Kiểm duyệt SAU build (BẮT BUỘC — `validate` sạch chưa đủ)
`validate` chỉ soi văn bản/cấu trúc; **lỗi trình bày + đáp án sai chỉ lộ ra trên PDF**. Trước khi trình Thầy, tác nhân PHẢI tự **đọc lại file PDF** (dùng Read trên `outputs/.../handout.pdf|guide.pdf`) và soát checklist sau — đây là kỷ luật, không lách:
1. **Tiêu đề chặng không tràn** thanh header (không bị cắt chữ). Giữ `stage.title` ≤ 46 ký tự — `visual_linter` nay cảnh báo; template tự co (`adjustbox`) là lưới an toàn, không phải cớ để đặt tên dài.
2. **Hình minh hoạ (tikz/opener) vẽ ĐÚNG vật thật** — soi từng hình: heo đất ra heo/chồng xu (không ra cái nhà), thang máy ra thang máy… Hình sai/khó hiểu thì sửa hoặc bỏ (opener cho phép chỉ-chữ). `visual_linter` chặn tikz thiếu `\begin{tikzpicture}` và figure rỗng, nhưng KHÔNG biết hình vẽ có giống vật không — mắt người phải soi.
3. **Sao độ khó đúng tier**: btvn ★☆☆, onclass ★★☆, extend ★★★ (sao đầy `\ding{72}` + sao rỗng `\ding{73}`).
4. **Đặt tên đúng thứ tự bài học:** khi folder tuần có ≥2 phiếu, **tên file + `slug` PHẢI mang tiền tố `phieu-a-/phieu-b-/phieu-c-/phieu-d-`** và `eyebrow` "PHIẾU A/B/C/D" khớp vị trí (xem HUONG-DAN §7). Mở folder phải thấy sort đúng A→B→C→D — KHÔNG đặt slug thuần theo nội dung (phiếu tạo sau sẽ lên trước). Đổi/tách lại số phiếu thì sửa cả ba: file, slug, eyebrow (và `lessons` của phiếu tổng kết nếu có).
5. **Đáp án**: mọi PT/BPT/hệ phải **đối chiếu độc lập bằng SymPy** (`solve_univariate_inequality`/`solveset`) — chạy script kiểm TRƯỚC khi viết `solution`; hình học SymPy yếu thì tự kiểm tay + soi lại số trên hình.
Sửa xong checklist → build lại → mới trình Thầy.
Kế hoạch tuần: [KE-HOACH-SOAN-BAI.md](KE-HOACH-SOAN-BAI.md). Luật soạn chi tiết: [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md).

## Nguyên tắc BẮT BUỘC khi soạn (bám HUONG-DAN §0)
1. **KHÔNG bịa đề** — lấy từ PDF nguồn; thiếu dạng thì hỏi Thầy.
2. **Đáp án phải đúng** — `validate` nay hỗ trợ tự đối chiếu đáp số đại số nếu bài có khai báo trường `check` (đáp án máy-đọc). Bài đại số NÊN kèm trường `check` trong seed để `validate` tự soi SymPy và chặn nếu sai (xem chi tiết tại KE-HOACH-AUTO-CHECK-DAP-AN.md và HUONG-DAN-SOAN-BAI.md). Với các phần khác hoặc khi chưa có `check`, vẫn phải **tự chạy SymPy** đối chiếu qua các hàm lẻ trong `sympy_solver.py` hoặc tự kiểm tay.
3. **Human-in-the-loop** — soạn → validate → **build PDF cho Thầy xem trước** → Thầy duyệt (approve). Bản build trước khi duyệt là bản nháp để Thầy đọc; chỉ phát hành chính thức sau khi approve.
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
