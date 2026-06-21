# PROJECT_MAP — bản đồ codebase (tự sinh bởi `make map`)
> Đọc file này TRƯỚC để biết module nào làm gì, khỏi mở từng file. Sinh từ `scripts/repomap.py`; KHÔNG sửa tay.


## src/

### `src/__init__.py`
- _(không có symbol công khai)_

### `src/agents/__init__.py`
- _(không có symbol công khai)_

### `src/agents/evolution_engine.py`
_Engine tiến hóa có kiểm soát — đọc FeedbackSchema và cập nhật style/prompt,_
- `evolve_from_feedback(feedback)` — Áp dụng phản hồi của Thầy vào bộ quy tắc style.

### `src/agents/feedback_parser.py`
_Đọc và phân tích `feedback/active_feedback.md` của Thầy,_
- **class FeedbackSchema** — Cấu trúc phản hồi đã được phân tích từ file Markdown của Thầy.
- `parse_feedback(feedback_path)` — Đọc file feedback Markdown và rút trích phân loại từng nhận xét.

### `src/compiler/__init__.py`
- _(không có symbol công khai)_

### `src/compiler/jinja_renderer.py`
_Đổ dữ liệu JSON sạch (LessonPackage) vào template Jinja2 → mã LaTeX._
- `split_reflection(blocks)` — Chia blocks chặng reflection thành 3 mục để tách BTVN/Mở rộng khỏi 'Tổng kết'.
- `group_slide_segments(blocks)` — Gom blocks của một frame slide thành các "đơn vị dạy" để bố cục đẹp.
- `load_tokens()`
- `render_handout(lesson, tokens)` — Mã LaTeX phiếu HS (A4 dọc, ẩn lời giải).
- `render_guide(lesson, tokens)` — Mã LaTeX Sổ tay GV (A4 dọc, hiện lời giải đỏ trầm + mẹo sư phạm).
- `render_slide(lesson, tokens)` — Mã LaTeX Slide TV (Beamer 16:9, font sans to, ẩn lời giải).
- `render_summary(summary, tokens, show_solution)` — Mã LaTeX phiếu TỔNG KẾT CHƯƠNG (A4 1 trang, sơ đồ tư duy to).

### `src/compiler/latex_builder.py`
_Gọi Tectonic (engine XeLaTeX) biên dịch mã LaTeX → PDF._
- **class LatexBuildError**
- `build_pdf(tex_source, slug, filename, out_root, force)` — Ghi .tex vào <out_root>/<slug>/ rồi compile ra PDF. Trả về đường dẫn PDF.

### `src/compiler/thuyetminh_renderer.py`
_Render PHIẾU THUYẾT MINH (spec) → LaTeX (A4 ngang) dùng base_thuyetminh.tex.j2._
- `render_thuyetminh(spec)`

### `src/main.py`
_Điểm chạy CLI trung tâm — MathTech Engine đầy đủ._
- `cmd_approve(args)` — Đánh dấu APPROVE để mở khoá compile PDF.
- `cmd_status(args)` — Xem tình trạng tất cả bài trong run_state.json.
- `cmd_evolve(args)` — Đọc active_feedback.md và tiến hóa style/prompt có kiểm soát.
- `cmd_build_handout(args)`
- `cmd_build_guide(args)`
- `cmd_build_slide(args)`
- `cmd_build_all(args)` — Sinh cả 3 bản SONG SONG từ cùng một gói bài (validate sạch trước).
- `cmd_build_folder(args)` — Build MỌI phiếu trong một folder tuần (vd folder có phieu-a + phieu-b).
- `cmd_build_summary(args)` — Sinh phiếu TỔNG KẾT CHƯƠNG 1 trang: bản HS (sơ đồ trống) + bản GV (có đáp án).
- `cmd_build_thuyetminh(args)` — Render PHIẾU THUYẾT MINH (spec) → PDF cho Thầy xem & chốt số câu (spec-first).
- `cmd_validate(args)`
- `cmd_validate_all(args)` — Chạy trọng tài S2 trên TẤT CẢ lesson JSON — gác cổng cả kho trước khi build/commit.
- `cmd_rebuild(args)` — Build LẠI mọi bài ĐÃ CÓ output (đủ 3 PDF) — để lan thay đổi design_tokens /
- `cmd_curriculum_sync(args)` — Sinh/cập nhật config/curriculum.json từ cây tuần — giữ lại metadata Thầy
- `cmd_progress(args)` — Quét sống cây tuần, báo trạng thái: PDF nguồn? lesson JSON? đã build chưa?
- `cmd_new_lesson(args)` — Sinh khung lesson JSON 5 chặng/4 tầng trong folder tuần để đổ đề vào.
- `cmd_new_summary(args)` — Sinh khung phiếu TỔNG KẾT CHƯƠNG. Một chương = NHIỀU tuần (mỗi tuần 1 bài,
- `main(argv)`

### `src/schema/__init__.py`
- _(không có symbol công khai)_

### `src/schema/base_schema.py`
_Định dạng của 1 bài toán — đơn vị Ground Truth nhỏ nhất._
- **class MathProblem**

### `src/schema/feedback_schema.py`
_Định dạng cấu trúc tệp phản hồi (feedback_parser.py sẽ map từ active_feedback.md sang đây)._
- **class FeedbackItem**
- **class FeedbackBundle**

### `src/schema/lesson_package.py`
_Cấu trúc tích hợp cả 5 chặng của buổi học — khóa cứng giữa AI và template Jinja2._
- **class ParaBlock**
- **class MathBlock**
- **class NotedBlock**
- **class WriteLinesBlock**
- **class SolvesetCheck** — Kiểm nghiệm phương trình một ẩn (→ sympy_solver.check_solution_set).
- **class IdentityCheck** — Kiểm đẳng thức hai vế (→ sympy_solver.verify_identity).
- **class NonnegCheck** — Kiểm 'biểu thức bậc hai >= 0 với mọi biến thực' (→ sympy_solver.prove_quadratic_nonneg).
- **class ProblemBlock**
- **class TableBlock** — Bảng (vd bảng đại lượng $s=v\cdot t$) — IN RA BẢNG THẬT cho HS điền.
- **class FigureBlock** — Hình minh hoạ hình học — VECTOR TikZ (ưu tiên) hoặc ảnh cắt từ phiếu gốc.
- **class OpenerBlock** — Thẻ "MỞ MÀN THỰC TẾ" — hook đời thực mở đầu phiếu (đặc sản nhận diện).
- **class MindmapNode** — Một nút trong sơ đồ tư duy điền khuyết. label có thể chứa [[blank:W]] để HS điền.
- **class MindmapBlock** — Sơ đồ tư duy điền khuyết — khung kiến thức bài học, HS điền các nút trống.
- **class Stage**
- **class LessonPackage**
- **class ChapterSummary** — Phiếu TỔNG KẾT CHƯƠNG (1 trang) — gom nhiều phiếu của một chương/tuần thành

### `src/schema/thuyetminh_spec.py`
_PHIẾU THUYẾT MINH (spec) — artifact MÁY-ĐỌC, là HỢP ĐỒNG chốt số câu trước khi soạn._
- **class SpecRow** — Một DẠNG bài trong phiếu, gắn band + số câu mỗi đoạn. Thời gian tự tính.
- **class SpecPhieu** — Một phiếu trong buổi (A = kỹ thuật, B = thực tế…).
- **class ThuyetMinhSpec** — Đặc tả 1 buổi học (≥1 phiếu) — hợp đồng số câu + nội dung khung.
- `row_minutes(row, rates)` — Phút mỗi đoạn của 1 dòng = số câu × phút/câu(đoạn, band).
- `phieu_band_counts(phieu)` — Tổng số câu theo {đoạn: {band: count}} của 1 phiếu (để so spec_gate sau).
- `phieu_totals(phieu, rates)` — Tổng số câu + phút mỗi đoạn của phiếu.
- `rates_for_spec(spec)` — Phút/câu áp cho spec này (theo lớp/môn của spec).
- `session_info(spec)` — Thông tin buổi (phút buổi, giải lao, ngân sách) từ tier_spec.

### `src/schema/tier_spec.py`
_Đọc `config/tier_spec.json` — RATE CARD cố định theo tầng lớp._
- `load_tier_spec(path)` — Đọc (và cache) tier_spec.json.
- `subject_block(spec, grade, subject)` — Khối cấu hình của (lớp, môn), vd ('lop-9','dai-so'). KeyError nếu chưa khai báo.
- `rates_for(spec, grade, subject)` — Phút/câu mỗi đoạn×band cho (lớp, môn): gộp `rates` toàn cục với
- `tier_ratio(spec, grade, subject, tier)` — Tỉ lệ NB-TH-VD-VDC (%) của tầng; None nếu tầng chưa chốt (vd X chuyên).
- `target_counts(spec, grade, subject, tier)` — Số câu MỤC TIÊU mỗi đoạn×band cho (lớp, môn, tầng). {} nếu tầng chưa có tỉ lệ.

### `src/validators/__init__.py`
_Tầng trọng tài — kiểm thử KHÔNG ba phải trước khi cho compile._
- _(không có symbol công khai)_

### `src/validators/answer_gate.py`
_Cổng đáp án — chạy SymPy đối chiếu trường `check` (máy-đọc) của từng ProblemBlock._
- `check_answers(lesson)` — Trả (fails, inconclusive). `fails` CHẶN build; `inconclusive` chỉ cảnh báo.

### `src/validators/difficulty_gate.py`
_Cổng gác SÀN độ khó — chống đẻ ra phiếu ngây ngô dưới tầm học sinh._
- **class DifficultyProfile**
- **class DifficultyReject**
- `load_profile(path)`
- `check_difficulty(lesson, profile)`
- `check_ramp(lesson, profile)` — Cổng ĐỘ DỐC (cảnh báo, KHÔNG chặn build): tầng Mở rộng phải là thang nhiều

### `src/validators/duration_gate.py`
_duration_gate — kiểm thời lượng & tỉ lệ NB-TH-VD cho phiếu PHÂN TẦNG._
- `check_duration(lesson)` — Cảnh báo khi phiếu tầng lệch quỹ phút hoặc tỉ lệ 40-40-20 (±5%).

### `src/validators/geometry_gate.py`
_Cổng hình học — SymPy YẾU với hình học tổng hợp nên KHÔNG được "duyệt mù"._
- `is_geometry(problem)`
- **class GeometryViolation**
- `check_geometry_problems(problems)` — Trả về danh sách vi phạm: bài hình chưa có nhãn human_verified (rỗng = đạt).

### `src/validators/latex_sanitizer.py`
_Chốt bảo mật LaTeX — quét và TỪ CHỐI mọi lệnh có thể thực thi mã / đọc-ghi file._
- **class UnsafeLatexError** — Phát hiện lệnh LaTeX nguy hiểm trong nội dung — từ chối, không tự sửa.
- `find_unsafe(text)` — Trả về danh sách tên lệnh nguy hiểm tìm thấy (rỗng nếu sạch).
- `sanitize(text)` — Trả lại `text` y nguyên nếu an toàn; ném UnsafeLatexError nếu phát hiện vi phạm.

### `src/validators/schema_validator.py`
_Kiểm toàn vẹn cấu trúc GÓI BÀI ngoài Pydantic._
- **class SchemaReport**
- `validate_lesson_structure(lesson)`

### `src/validators/sympy_solver.py`
_Trọng tài Đại số — giải ĐỘC LẬP bằng SymPy rồi đối chiếu với đáp án con người._
- **class VerdictStatus**
- **class Verdict**
- `to_expr(latex_or_text)` — Phân tích LaTeX (hoặc biểu thức sympy text) thành biểu thức SymPy.
- `solve_equation(equation, symbol)` — Giải độc lập phương trình một ẩn. Chấp nhận 'lhs = rhs' hoặc biểu thức = 0.
- `check_solution_set(equation, claimed, symbol)` — So khớp tập nghiệm SymPy giải được với tập nghiệm con người tuyên bố.
- `verify_identity(lhs, rhs)` — Chứng minh đẳng thức: rút gọn (lhs - rhs) về 0 thì OK.
- `prove_quadratic_nonneg(expr, symbols)` — Chứng minh `expr >= 0 với mọi biến thực` cho biểu thức BẬC HAI thuần nhất.

### `src/validators/visual_linter.py`
_Trọng tài Thị giác — xử lý BẰNG CODE XÁC ĐỊNH (không giao LLM)._
- `find_presentation_warnings(lesson)` — Cảnh báo trình bày (không chặn build): chú thích GV lọt phiếu HS; nhiều ý
- `wrap_long_math(latex, max_len)` — Nếu công thức dài hơn `max_len` ký tự, bẻ tại quan hệ thành aligned.
- **class BuildLogReport**
- `scan_build_log(log_text)`


## config/

### `config/settings.py`
_Cấu hình tập trung — đọc biến môi trường từ .env (KHÔNG hardcode key)._
- _(không có symbol công khai)_


## scripts/

### `scripts/build_thuyetminh_tuan10_11.py`
_Dựng PHIẾU THUYẾT MINH (đặc tả) cho [C]tuần 10-11 — BPT bậc nhất một ẩn._
- `esc(s)`
- `itemize(items)`
- `meta_table(rows)`
- `phieu_table(groups, total)`

### `scripts/organize_lop8_kntt.py`
- `normalize_text(text)`
- `determine_target_dir(path_str)`
- `run()`

### `scripts/repomap.py`
_Sinh PROJECT_MAP.md — bản đồ codebase TIẾT KIỆM TOKEN cho agent/người._
- `main()`

### `scripts/spike_coverage.py`
_SPIKE de-risk (Bước 2): bank có đủ câu để 'bốc' cho 1 phiếu tầng không?_
- `load_bank_cau()`
- `main()`

### `scripts/update_phieu_b.py`
- _(không có symbol công khai)_
