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

### `src/compiler/de_renderer.py`
_Render THUYẾT MINH ĐỀ KIỂM TRA (DeSpec) → LaTeX (A4 ngang)._
- `render_de(spec)`

### `src/compiler/jinja_renderer.py`
_Đổ dữ liệu JSON sạch (LessonPackage) vào template Jinja2 → mã LaTeX._
- `strip_example_solution(text)` — Trên slide TV: ví dụ mẫu CHỈ CẦN ĐỀ BÀI + HÌNH VẼ, không in phần 'Lời giải'.
- `split_reflection(blocks)` — Chia blocks chặng reflection thành 3 mục để tách BTVN/Mở rộng khỏi 'Tổng kết'.
- **class _WrapFigure** — Hình bóc ra từ cờ `[[wrap]]` của `statement`, đủ giống FigureBlock để
- `split_wrap(statement)` — Tách hộp hình `[[wrap]]…[[/wrap]]` khỏi đề → (figure|None, đề còn lại).
- `group_slide_segments(blocks)` — Gom blocks của một frame slide thành các "đơn vị dạy" để bố cục đẹp.
- `plainlen(s)` — Độ dài CHỮ THẬT (bỏ lệnh LaTeX, token [[…]], ngoặc, $) — thước đo bố cục.
- `mcq_cols(options)` — SỐ CỘT xếp phương án trắc nghiệm, chọn theo phương án DÀI NHẤT.
- `tach_loi_giai(text)` — Cắt hộp ví dụ thành (ĐỀ, LỜI GIẢI) ở tiêu đề "Lời giải".
- `tach_y_con(statement)` — Cắt đề thành (ĐỀ CHUNG, CÁC Ý a) b) c)…) ở ý đầu tiên.
- `fig_side(prob)` — Chỗ đặt hình: 'below' | 'none'. KHÔNG còn 'right'.
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

### `src/exporters/__init__.py`
- _(không có symbol công khai)_

### `src/exporters/drive_sync.py`
_drive_sync — chép PDF thành phẩm từ `outputs/` sang Google Drive đã đồng bộ trên máy._
- `drive_root()`
- `ensure_khoi(root, name, tao)` — Thư mục KHỐI ('lop9') — khớp RỘNG TAY hơn `ensure_dir`: nhận cả tên có đuôi.
- `ensure_dir(parent, name, tao)` — Trả thư mục con `name` dưới `parent`, dùng lại thư mục đã có nếu chỉ khác
- `di_toi(root, parts, tao)` — Lần theo `parts` từ gốc Drive. Khúc ĐẦU (khối) khớp rộng tay, các khúc sau khớp chặt.
- **class DriveTarget** — Chỗ đến trên Drive của một thư mục output.
- `plan_target(out_dir, outputs_root, tieu_de)` — Dịch một thư mục trong `outputs/` sang danh sách thư mục trên Drive.
- `sync_dir(out_dir, outputs_root, tieu_de, dry_run, root)` — Chép mọi PDF trong `out_dir` sang đúng chỗ trên Drive. Trả (thư mục đích, tên file đã chép).

### `src/exporters/ten_file.py`
_ten_file — đặt TÊN PDF thành phẩm tự nói ra mình là bài gì._
- `bo_dau(s)` — 'Mở đầu về đường tròn' → 'Mo dau ve duong tron' (Drive/Finder dễ đọc, khỏi lệch NFC/NFD).
- `ten_ban_in(lesson, json_path, kind, ca_pre)` — Tên file (không đuôi) cho một bản in. Lùi về '{ca_pre}{kind}' khi thiếu dữ kiện.

### `src/main.py`
_Điểm chạy CLI trung tâm — MathTech Engine đầy đủ._
- `cmd_approve(args)` — Đánh dấu APPROVE để mở khoá compile PDF.
- `cmd_status(args)` — Xem tình trạng tất cả bài trong run_state.json.
- `cmd_evolve(args)` — Đọc active_feedback.md và tiến hóa style/prompt có kiểm soát.
- `get_ca_prefix(lesson, json_path)` — Xác định tiền tố Ca ('ca-01-', 'ca-02-'...) cho phiếu học tập.
- `cmd_build_handout(args)`
- `cmd_build_guide(args)`
- `cmd_build_slide(args)`
- `cmd_build_all(args)` — Sinh cả 3 bản SONG SONG từ cùng một gói bài (validate sạch trước).
- `cmd_build_folder(args)` — Build MỌI phiếu trong một folder tuần (vd folder có phieu-a + phieu-b).
- `cmd_build_summary(args)` — Sinh phiếu TỔNG KẾT CHƯƠNG 1 trang: bản HS (sơ đồ trống) + bản GV (có đáp án).
- `cmd_validate_thuyetminh(args)` — Gác cổng PHIẾU THUYẾT MINH (spec) — soi giờ vô lý TRƯỚC khi Thầy chốt số câu.
- `cmd_build_thuyetminh(args)` — Render PHIẾU THUYẾT MINH (spec) → PDF cho Thầy xem & chốt số câu (spec-first).
- `cmd_validate_de(args)` — Gác cổng THUYẾT MINH ĐỀ — soi điểm/giờ vô lý TRƯỚC khi Thầy chốt cấu trúc đề.
- `cmd_build_de(args)` — Render THUYẾT MINH ĐỀ (DeSpec) → PDF cho Thầy xem & chốt trước khi ra đề thật.
- `cmd_validate(args)`
- `cmd_validate_all(args)` — Chạy trọng tài S2 trên TẤT CẢ lesson JSON — gác cổng cả kho trước khi build/commit.
- `cmd_audit(args)` — SOI CẢ KHO — ba thứ mà `validate` từng phiếu KHÔNG bao giờ thấy.
- `cmd_rebuild(args)` — Build LẠI mọi bài ĐÃ CÓ output (đủ 3 PDF) — để lan thay đổi design_tokens /
- `cmd_curriculum_sync(args)` — Sinh/cập nhật config/curriculum.json từ cây tuần — giữ lại metadata Thầy
- `cmd_progress(args)` — Quét sống cây tuần, báo trạng thái: PDF nguồn? lesson JSON? đã build chưa?
- `cmd_new_lesson(args)` — Sinh khung lesson JSON 5 chặng/4 tầng trong folder tuần để đổ đề vào.
- `cmd_new_summary(args)` — Sinh khung phiếu TỔNG KẾT CHƯƠNG. Một chương = NHIỀU tuần (mỗi tuần 1 bài,
- `cmd_sync_drive(args)` — Chép PDF từ outputs/ sang Google Drive, tạo thư mục còn thiếu.
- `cmd_new_thuyetminh(args)` — Sinh khung PHIẾU THUYẾT MINH (spec) — số câu mục tiêu auto từ tier_spec.
- `main(argv)`

### `src/schema/__init__.py`
- _(không có symbol công khai)_

### `src/schema/base_schema.py`
_Định dạng của 1 bài toán — đơn vị Ground Truth nhỏ nhất._
- **class MathProblem**

### `src/schema/de_spec.py`
_THUYẾT MINH ĐỀ KIỂM TRA (đặc tả đề) — artifact MÁY-ĐỌC, chốt cấu trúc đề TRƯỚC khi ra đề._
- **class DeCau** — Một câu (hoặc một ý) trong đề — đơn vị chấm điểm.
- **class De** — Một đề kiểm tra.
- **class DeSpec** — Đặc tả TOÀN BỘ đề kiểm tra của một chương.
- `de_totals(de)` — Tổng điểm / phút của một đề, kèm phân rã theo band.
- `band_share(de)` — Tỉ trọng % mỗi band theo PHÚT làm bài (khớp cách soi tỉ lệ của phiếu).

### `src/schema/exam_bank.py`
_Loader ngân hàng đề (đã gắn band/phut) — tra cứu câu theo id cho gate/spec._
- `load_bank(force)` — id câu → {band, phut, diem, dang, chuong, de}. Cache; rỗng nếu chưa có bank.
- `lookup(ids)` — Các (id, record) có thật trong bank (bỏ qua id không khớp — opt-in, không báo lỗi).

### `src/schema/feedback_schema.py`
_Định dạng cấu trúc tệp phản hồi (feedback_parser.py sẽ map từ active_feedback.md sang đây)._
- **class FeedbackItem**
- **class FeedbackBundle**

### `src/schema/lesson_package.py`
_Cấu trúc tích hợp cả 5 chặng của buổi học — khóa cứng giữa AI và template Jinja2._
- **class ParaBlock**
- **class MathBlock**
- **class DefItem** — MỘT mục của danh sách định nghĩa: thuật ngữ + phần giải thích.
- **class DefListBlock** — DANH SÁCH ĐỊNH NGHĨA — mỗi mục MỘT DÒNG RIÊNG, thuật ngữ nổi bật, phần giải
- **class ProblemFigure** — HÌNH ĐI KÈM MỘT BÀI — tách khỏi `statement` để template tự canh chỗ.
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
- `row_minutes(row, rates)` — Phút mỗi đoạn của 1 dòng = số câu × phút/câu(đoạn, band) + số hình HS tự vẽ
- `phieu_band_counts(phieu)` — Tổng số câu theo {đoạn: {band: count}} của 1 phiếu (để so spec_gate sau).
- `phieu_band_minutes(phieu, rates)` — Phút theo {đoạn: {band: phút}} — ĐÃ gồm phút vẽ hình (`ve_hinh`), cộng vào
- `phieu_totals(phieu, rates)` — Tổng số câu + phút mỗi đoạn của phiếu.
- `rates_for_spec(spec)` — Phút/câu áp cho spec này (theo lớp/môn của spec).
- `he_so_con_lai(session_minutes, so_ca, kiem_tra_phut)` — Phần buổi CÒN LẠI cho phiếu sau khi cắt giờ kiểm tra chương (1.0 = cả buổi).
- `session_info(spec)` — Thông tin buổi (phút buổi, giải lao, ngân sách) từ tier_spec.

### `src/schema/tier_spec.py`
_Đọc `config/tier_spec.json` — RATE CARD cố định theo tầng lớp._
- `load_tier_spec(path)` — Đọc (và cache) tier_spec.json.
- `subject_block(spec, grade, subject)` — Khối cấu hình của (lớp, môn), vd ('lop-9','dai-so'). KeyError nếu chưa khai báo.
- `rates_for(spec, grade, subject)` — Phút/câu mỗi đoạn×band cho (lớp, môn): gộp `rates` toàn cục với
- `draw_minutes(spec)` — Phút CỘNG THÊM cho mỗi hình HS phải TỰ VẼ (Thầy chốt 2026-07-26: 5′).
- `quick_minutes(spec)` — Phút/câu cho câu NHẬN BIẾT trắc nghiệm / điền chỗ chấm trên HÌNH VẼ SẴN
- `load_ban_do(path)` — Đọc (và cache) `config/ban_do_vd_vdc.json` — chương nào CÓ bài VD/VDC trong đề.
- `phan_bo_vdc(grade, chuong)` — Chia khối 55% VD+VDC theo TẦN SUẤT VDC của chương (Thầy chốt 04/09/2026).
- `muc_tieu_vdc(grade, chuong)` — (mục tiêu VDC, trần điểm) của chương — "an-tron" cho kỳ I (trần 10,0),
- `chuong_co_vd(grade, chuong)` — Chương này có bài VD/VDC trong đề kiểm tra định kì không?
- `so_ca_yeu_cau(spec, grade, subject, tier, chuong)` — Số CA (buổi) mà một phiếu của tầng này phải trải, theo chương.
- `gop_vd_vdc(spec, grade, subject, tier)` — Tầng này soi tỉ lệ với VD và VDC GỘP làm một khối (Thầy chốt 30/08/2026)?
- `tier_ratio(spec, grade, subject, tier, chuong)` — Tỉ lệ NB-TH-VD-VDC (%) của tầng; None nếu tầng chưa chốt (vd X chuyên).
- `target_counts(spec, grade, subject, tier, chuong)` — Số câu MỤC TIÊU mỗi đoạn×band cho (lớp, môn, tầng). {} nếu tầng chưa có tỉ lệ.

### `src/validators/__init__.py`
_Tầng trọng tài — kiểm thử KHÔNG ba phải trước khi cho compile._
- _(không có symbol công khai)_

### `src/validators/answer_gate.py`
_Cổng đáp án — chạy SymPy đối chiếu trường `check` (máy-đọc) của từng ProblemBlock._
- `check_answers(lesson)` — Trả (fails, inconclusive). `fails` CHẶN build; `inconclusive` chỉ cảnh báo.

### `src/validators/de_gate.py`
_de_gate — soi ĐỀ VÔ LÝ trong thuyết minh đề TRƯỚC khi Thầy chốt & người ra đề viết đề._
- `check_de(spec)` — Trả (errors, warnings). errors CHẶN build; warnings chỉ cảnh báo.

### `src/validators/difficulty_gate.py`
_Cổng gác SÀN độ khó — chống đẻ ra phiếu ngây ngô dưới tầm học sinh._
- **class DifficultyProfile**
- **class DifficultyReject**
- `load_profile(path)`
- `check_difficulty(lesson, profile)`
- `check_ramp(lesson, profile)` — Cổng ĐỘ DỐC (cảnh báo, KHÔNG chặn build): tầng Mở rộng phải là thang nhiều

### `src/validators/duration_gate.py`
_duration_gate — kiểm thời lượng & tỉ lệ NB-TH-VD(-VDC) cho phiếu PHÂN TẦNG._
- `band_counts(lesson)` — Đếm số câu LUYỆN TẬP theo {onclass|btvn: {band: n}} — đơn vị ý nhỏ/thẻ mức.
- `figure_given_counts(lesson)` — Trong số câu trên, bao nhiêu câu làm trên HÌNH VẼ SẴN (`figure_given`) —
- `draw_counts(lesson)` — Đếm số BÀI phải TỰ VẼ HÌNH theo {onclass|btvn: {band: n}} — mỗi bài 1 hình
- `check_vdc_cuoi_bai(lesson)` — VDC chỉ được nằm ở Ý CUỐI của bài — mỗi bài tối đa MỘT thẻ [VDC].
- `check_duration(lesson)` — Cảnh báo khi phiếu tầng lệch quỹ phút hoặc tỉ lệ (đọc chuẩn từ tier_spec).

### `src/validators/figure_gate.py`
_Cổng gác ĐỀ ↔ HÌNH — chặn hai lỗi đã lọt tới Thầy ở phiếu B/C chương III lớp 7._
- **class FigureViolation**
- `check_figure_symbols(lesson)` — Đề nhắc ký hiệu nào thì hình phải dán đủ ký hiệu đó.
- `check_clone_problems(lesson, max_clones)` — Cùng một đề chép quá `max_clones` lần → lấp chỗ, phải dệt lại.
- `check_hinh_thieu(lesson)` — Hai lỗi Thầy đã bắt ở phiếu B, còn sót ở phiếu E:
- `check_image_paths(lesson_path)` — Ảnh phải trỏ ĐƯỜNG DẪN TƯƠNG ĐỐI theo folder phiếu, và file phải có thật.
- `check_figures(lesson)` — VI PHẠM CHẶN — hai lỗi đã có bằng chứng Thầy trả phiếu, kho hiện sạch nên
- `warn_figures(lesson)` — CẢNH BÁO (chưa chặn) — `check_hinh_thieu` bắt đúng nhưng đang dính ~60 chỗ ở

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

### `src/validators/nhan_hinh_gate.py`
_Cổng NHÃN HÌNH BỊ NÉT VẼ ĐÈ — góp ý chương V lớp 9C (26/09/2026)._
- `nhan_bi_de(tikz)` — Danh sách nhãn (chữ) bị nét vẽ cắt ngang trong một hình TikZ.
- `check_nhan_hinh(lesson)` — Cảnh báo nhãn điểm bị đoạn thẳng / đường tròn cắt ngang.

### `src/validators/print_gate.py`
_print_gate — soi BẢN IN sau khi build: trang loãng, tiêu đề chặng mồ côi._
- `check_print_layout(pdf, dau_muc)` — Cảnh báo bố cục bản in. [] khi sạch hoặc không soi được.

### `src/validators/schema_validator.py`
_Kiểm toàn vẹn cấu trúc GÓI BÀI ngoài Pydantic._
- **class SchemaReport**
- `check_khoa_la(raw)` — Soi JSON THÔ tìm trường không có trong schema — pydantic sẽ ÂM THẦM VỨT ĐI.
- `validate_lesson_structure(lesson)`

### `src/validators/sgk_style_gate.py`
_sgk_style_gate — soi LỜI GIẢI có trình bày theo đúng khuôn SGK không._
- `check_sgk_style(lesson)` — Cảnh báo trình bày lệch chuẩn SGK. Trả list chuỗi (rỗng = sạch).
- `check_vi_du_style(lesson)` — Mỗi khối `noted variant=example` chứa "Ví dụ N." phải là một BÀI GIẢI đầy đủ:
- `check_goi_ten_canh(lesson)` — Cảnh báo dòng vừa gọi tên cạnh đối/kề/huyền vừa viết tỉ số lượng giác.

### `src/validators/spec_gate.py`
_spec_gate — so số câu phiếu (JSON) với HỢP ĐỒNG thuyet-minh.json cạnh bên._
- `check_spec_conformance(lesson, lesson_path)` — [] nếu không có spec cạnh bên (opt-in) hoặc khớp; ngược lại list cảnh báo.
- `check_dang_mapping(lesson, phieu, tol)` — Soi phiếu thật có TƯƠNG ỨNG THẬT RÕ với thuyết minh không (Thầy chốt 14/08/2026).

### `src/validators/staleness_gate.py`
_staleness_gate — PDF trong `outputs/` có còn khớp nguồn sinh ra nó không?_
- **class Stale**
- `check_stale(out_dirs)` — Soi mọi PDF trong các thư mục output đã cho. [] = mọi bản in còn khớp nguồn.
- `tom_tat(stales)` — Một dòng đếm theo lý do, để in ở cuối bản audit.

### `src/validators/sympy_solver.py`
_Trọng tài Đại số — giải ĐỘC LẬP bằng SymPy rồi đối chiếu với đáp án con người._
- **class VerdictStatus**
- **class Verdict**
- `to_expr(latex_or_text)` — Phân tích LaTeX (hoặc biểu thức sympy text) thành biểu thức SymPy.
- `solve_equation(equation, symbol)` — Giải độc lập phương trình một ẩn. Chấp nhận 'lhs = rhs' hoặc biểu thức = 0.
- `check_solution_set(equation, claimed, symbol)` — So khớp tập nghiệm SymPy giải được với tập nghiệm con người tuyên bố.
- `verify_identity(lhs, rhs)` — Chứng minh đẳng thức: rút gọn (lhs - rhs) về 0 thì OK.
- `prove_quadratic_nonneg(expr, symbols)` — Chứng minh `expr >= 0 với mọi biến thực` cho biểu thức BẬC HAI thuần nhất.

### `src/validators/thuyetminh_gate.py`
_thuyetminh_gate — soi GIỜ VÔ LÝ trong phiếu THUYẾT MINH (spec) TRƯỚC khi Thầy chốt._
- `check_thuyetminh(spec)` — Trả (errors, warnings). errors CHẶN build; warnings chỉ cảnh báo.
- `check_scaffold_rails(spec)` — Mỗi phiếu phải có ĐỦ hai giàn giáo NB: 've-hinh' (môn hình) và 'dien-khuyet'.
- `check_source_refs(spec)` — KHÔNG BỊA ĐỀ: mọi dòng phải trỏ nguồn, TRỪ dòng loại 'NB lẻ LT' (câu hỏi thẳng
- `check_chuong_level(spec)` — Thầy chốt 14/08/2026: TỪ GIỜ CHỈ LÀM THUYẾT MINH CẤP CHƯƠNG, mọi khối.
- `check_kiem_tra_chuong(spec)` — Spec cả chương phải chừa ≥45′ kiểm tra chương ở PHIẾU CUỐI (`kiem_tra_phut`)
- `check_meta_wrap(tex)` — Soi BẢNG ĐẦU của thuyết minh ĐÃ RENDER: ô nào nhiều mục mà không xuống dòng,
- `check_loai_4b(spec)` — Cảnh báo dòng spec chưa khai `loai`, hoặc khai nhãn không thuộc 7 loại §4b,
- `goi_y_kien_thuc_nen(spec)` — Nền mà spec CÓ DÙNG nhưng CHƯA KHAI. Bỏ qua thứ chính là nội dung của chương
- `check_kien_thuc_nen(spec)` — Spec CÓ nội dung thì bắt buộc có khối KIẾN THỨC NỀN (bản mẫu chương IV/V).
- `check_thoiluong(spec)` — Khối THỜI LƯỢNG phải có, không giả định kiểm tra 15′, và TỔNG phải khớp phép cộng.

### `src/validators/trinh_bay_gate.py`
_trinh_bay_gate — gác CÁCH TRÌNH BÀY phiếu (Thầy chốt 24/09/2026)._
- `check_lenh_dinh_chu(lesson)` — CHẶN: lệnh LaTeX trần dính liền chữ → Tectonic gãy ngay lúc build.
- `check_trinh_bay(lesson)` — Cảnh báo về cách trình bày (không chặn).

### `src/validators/vi_du_gate.py`
_Cổng VÍ DỤ MẪU ↔ BÀI TẬP — Thầy chốt 21/09/2026 (chấm phiếu chương V Hình 9B)._
- `check_vi_du_trung_bai(lesson, nguong)` — Ví dụ mẫu KHÔNG được là bài tập chép lại đổi số.
- `check_vi_du_di_cung_bai(lesson)` — Mỗi ví dụ phải đứng NGAY TRƯỚC nhóm bài của dạng đó (Thầy chốt 08/09 + 21/09).
- `check_vi_du_dien_khuyet(lesson, toi_thieu)` — Ví dụ mẫu = BÀI ĐIỀN KHUYẾT thầy trò cùng làm (Thầy chốt 21/09/2026).
- `check_goi_y_thong_hieu(lesson)` — Phiếu luyện tập chương: MỌI câu Thông hiểu (level 2) phải có `hints`.
- `check_fill_math_long_nhau(lesson)` — Ô nằm TRONG $…$ mà đáp án lại tự bọc $…$ ⇒ Tectonic chết "Missing } inserted".
- `check_so_tren_hinh_vi_du(lesson)` — Viết lại đề ví dụ mà quên sửa số ghi trên hình ⇒ đề một đằng, hình một nẻo.
- `check_vi_du_ket_luan(lesson)` — Câu "Vậy …" của ví dụ phải có ô [[fill:]] — kết luận là thứ HS cần điền.
- `check_vi_du_lo_dap_an(lesson)` — Ô [[fill:số]] ở trên mà dòng dưới (kể cả câu "Vậy") lại in trần con số đó.
- `check_vi_du(lesson)` — Chạy cả bốn luật một lượt (dùng trong `validate` / `audit`).

### `src/validators/visual_linter.py`
_Trọng tài Thị giác — xử lý BẰNG CODE XÁC ĐỊNH (không giao LLM)._
- `find_text_escape_issues(text, loc)` — Cảnh báo escape (%/# thô mọi nơi, & thô ngoài $...$, glyph tofu) cho MỘT chuỗi
- `find_presentation_warnings(lesson)` — Cảnh báo trình bày (không chặn build): chú thích GV lọt phiếu HS; nhiều ý
- `wrap_long_math(latex, max_len)` — Nếu công thức dài hơn `max_len` ký tự, bẻ tại quan hệ thành aligned.
- **class BuildLogReport**
- `scan_build_log(log_text)`


## config/

### `config/settings.py`
_Cấu hình tập trung — đọc biến môi trường từ .env (KHÔNG hardcode key)._
- _(không có symbol công khai)_


## scripts/

### `scripts/build_ban_do_vd_vdc.py`
_Dựng PDF 'BẢN ĐỒ VD/VDC THEO CHƯƠNG' từ config/ban_do_vd_vdc.json — cho Thầy & sếp duyệt._
- `tex(s, n)` — Escape sang LaTeX; `n` cắt bớt độ dài (trích dẫn đề bài in trong ô bảng).
- `bang_khoi(ma_khoi, khoi, so_mt)`
- `main()`

### `scripts/build_exam_weights.py`
_Sinh file WEIGHT dẫn xuất từ ngân hàng đề (đã gắn band/phut) — "trọng số tần suất"._
- `build()`
- `main()`

### `scripts/build_lop9b_geometry.py`
- `generate_all()`

### `scripts/build_on_tap_thi_thu.py`
_ÔN TẬP THEO PHẦN — gom đề bài từ CÁC ĐỀ THI THỬ VÀO 10 Hà Nội, mỗi phần một tệp._
- `tex(s)`
- `phan_de(t)`
- `cat_anh(pdf, i_moc, moc, cao, het)` — Cắt dải ảnh của bài thứ `i_moc` — một tệp PNG cho mỗi trang mà bài đó trải qua.
- `tach_bai(pdf)` — [(nhãn bài, nguyên văn)] của phần ĐỀ. [] nếu PDF không có lớp text.
- `gan_phan(bais)` — (phần, nhãn, nguyên văn). Đề đúng 5 bài thì gán theo THỨ TỰ (khuôn đề Sở);
- `gom()` — Gom theo phần, LẤY MỐC TỪ BBOX làm nguồn duy nhất.
- `render(ph, muc)`
- `main()`

### `scripts/build_trich_vdc.py`
_Dựng PDF 'TRÍCH XUẤT CÂU VDC' — in NGUYÊN VĂN đề bài để Thầy kiểm có thật là VDC không._
- `tex(s, n)`
- `tu_bank()` — Câu VDC của lớp 9 HK1 từ ngân hàng — chỉ lấy ĐỀ ĐẦY ĐỦ (tổng 9-10,5đ).
- `tu_text()` — Câu cuối đề của cả 4 khối, trích từ text PDF.
- `bang_trich(rows)`
- `bang_phan_loai(rows)` — Chương nào chỉ TH · TH+VD · TH+VD+VDC — VDC lấy từ chính bảng trích trên.
- `main()`

### `scripts/exam_annotate.py`
_Gắn `band` (NB/TH/VD/VDC) + `phut` (thời gian HS làm, ước) vào từng câu trong_
- `cmd_ensure_ids(args)` — Ghi trường `id` (tổng hợp từ bai+y) vào câu nào còn thiếu — chuẩn hoá bank.
- `cmd_extract(args)` — In mọi câu CHƯA có band (hoặc --all) để chấm. Mặc định format người-đọc;
- `cmd_apply(args)` — Đổ phán đoán {id: {band, phut}} vào các đề; gắn cờ _band_auto/_phut_auto.
- `cmd_report(args)` — Phút/câu THỰC theo band (đối chiếu tier_spec) + độ phủ band/phut.
- `cmd_check(args)` — Gác cổng ngân hàng đề: Σdiem≠tong_diem, thiếu band/phut, trùng id, band lạ.
- `cmd_fix_headers(args)` — Backfill thoi_gian_phut/tong_diem còn thiếu; cảnh báo Σdiem ≠ tong_diem.
- `main(argv)`

### `scripts/fetch_de_thi.py`
_Tải ĐỀ THI Toán 9 HÀ NỘI (giữa kì II / cuối kì II) từ TOANMATH về inputs/refs/de-thi/._
- `thu_thap()` — Quét sitemap → (danh sách slug giữa kì 2, danh sách slug cuối kì 2).
- `tai(urls, thu_muc, so)`
- `main(argv)`

### `scripts/fetch_de_thi_khoi.py`
_Tải ĐỀ THI Toán HÀ NỘI cho CẢ 4 KHỐI 6-7-8-9 × 4 KỲ (GK1, CK1, GK2, CK2) từ TOANMATH._
- `quet_sitemap(dung_cache)` — Danh sách URL bài viết của thcs.toanmath.com (cache ra file cho lần sau).
- `phan_loai(url)` — (lớp, kỳ, năm) của một URL đề, hoặc None nếu không phải đề định kì Hà Nội hợp lệ.
- `phan_loai_thi_thu(url)` — Năm học của một URL ĐỀ THI THỬ VÀO 10 Hà Nội, hoặc None nếu không phải.
- `dem_hien_co(lop, ky)`
- `tai(urls, thu_muc, so)` — Tải tối đa `so` PDF vào thư mục; bỏ qua file đã có.
- `main(argv)`

### `scripts/fetch_sgv.py`
_Tải SÁCH GIÁO VIÊN (SGV) Toán Kết nối tri thức khối 6-12 về inputs/refs/sgv/._
- `jpeg_size(data)` — (rộng, cao) tính bằng pixel, đọc từ marker SOF của JPEG.
- `jpegs_to_pdf(pages, dest)` — Ghép danh sách ảnh JPEG thành PDF, mỗi ảnh một trang, khổ ngang A4.
- `fetch_grade(grade)`
- `main(argv)`

### `scripts/prune_outputs.py`
_prune_outputs — soi thư mục `outputs/` mồ côi (bản in cũ của phiếu đã đổi tên/xoá)._
- `expected_dirs()` — slug → các thư mục output hợp lệ (mirror cây seeds, xem src/main.py::_out_root).
- `scan()` — (lạc chỗ — seed còn nhưng đã chuyển folder, mất gốc — không seed nào khớp).
- `main(argv)`

### `scripts/quick.py`
_quick — gõ ngắn cho 2 việc làm nhiều nhất: build lại nhanh & đọc phiếu dạng dễ nhìn._
- `loai_file(p)` — 'phieu' (gói bài học) | 'spec' (phiếu thuyết minh) | '' (không phải cả hai).
- `resolve(query)` — Mẩu chữ HOẶC đường dẫn file → đúng 1 file phiếu.
- `to_markdown(path)`
- `main(argv)`

### `scripts/repomap.py`
_Sinh PROJECT_MAP.md — bản đồ codebase TIẾT KIỆM TOKEN cho agent/người._
- `main()`

### `scripts/seed_exam_bands.py`
_Seed band (NB/TH/VD/VDC) + phut (thời gian HS làm, ước) cho ngân hàng đề lớp 9._
- `judge(dangs, do_kho)`
- `main()`

### `scripts/soi_ma_tran_de.py`
_Trích MA TRẬN (bảng 'câu → kiến thức → mức độ') từ kho đề THCS đã tải về._
- `bo_sach(t)`
- `ky_thi(pdf)`
- `trich_ma_tran(t)` — Các dòng ma trận khuôn (1). Trả [] nếu đề không kèm ma trận.
- `quet()`
- `main(argv)`

### `scripts/spike_coverage.py`
_SPIKE de-risk (Bước 2): bank có đủ câu để 'bốc' cho 1 phiếu tầng không?_
- `load_bank_cau()`
- `main()`

### `scripts/tan_suat_vdc.py`
_TẦN SUẤT VDC theo chương — đếm ở ĐÚNG HAI VỊ TRÍ, mỗi bài chỉ tính CÂU CUỐI._
- `tan_suat_678(lop)` — Tần suất VDC theo chương cho khối 6/7/8 — cùng luật với lớp 9.
- `nhom_va_phan_bo(p)`
- `de_du_diem()` — (tên đề, kỳ, dữ liệu) của các đề TỔNG 9–10,5đ — chỉ đề đủ mới biết câu nào cuối.
- `dem_hk1()` — Đếm hai vị trí VDC trên mẫu HK1. Trả (cuối đề, ý cuối hình, số đề mỗi kỳ, chi tiết).
- `dem_hk2()` — Đếm hai vị trí VDC trên mẫu HK2 (file phân loại bằng mắt) + xếp hạng DẠNG.
- `cach_giai_toan_bo()` — Xếp hạng CÁCH GIẢI của mọi câu cuối đề (HK1 + HK2) + danh sách câu NGOÀI SGK.
- `tong_hop()`
- `cuc_tri_ca_4_ky(chi_tiet, dang2)` — Câu cuối đề là bài CỰC TRỊ/TỐI ƯU trong bao nhiêu đề của cả bốn kỳ?
- `main()`

### `scripts/tien-do-lop-c/_data.py`
_Tiến độ tầng C — Lớp 9. Đại số 180′ · Hình học 90′._
- `t15(what, n)`
- `kt45(ch)`
- `sundays(n)`

### `scripts/tien-do-lop-c/audit.py`
_Soi lỗi logic tiến độ tầng C — CHẠY TRƯỚC KHI XUẤT FILE cho Thầy._
- `add(k, s)`
- `muc_day(r)`
- `ch_of(nd)`

### `scripts/tien-do-lop-c/gen_xlsx.py`
_Xuất tiến độ tầng C ra .xlsx — định dạng bám file PDF gốc của trung tâm._
- `muc_day(r)` — Mức dạy — chỉ có nghĩa với dòng có tiết SGK. Mặc định 'Đầy đủ'.
- `fill(c)`
- `style_row(ws, r, ncol, bg, bold, color, size)`
- `banner(ws, r, text, bg, ncol, color)`
- `row_bg(hm, lkt, nd)`
- `build(weeks, path, title, buoi_label)`

### `scripts/trich_cau_cuoi_de.py`
_Trích CÂU CUỐI ĐỀ (ứng viên VDC) từ kho đề đã tải — để Thầy soi đề bài thật._
- `phan_de(t)` — Phần ĐỀ: cắt trước mốc đáp án/ma trận đầu tiên nằm sau 20% đầu văn bản.
- `cau_cuoi(t)` — Mốc cuối cùng của phần tự luận. Ưu tiên 'Bài' — phần trắc nghiệm đánh 'Câu 1..12'
- `y_cuoi_bai_hinh(t)` — Ý CUỐI của BÀI HÌNH — vị trí VDC thứ hai theo quy ước anh An.
- `hop_le_de_thi(pdf)` — File này có phải ĐỀ THI định kì dùng để chấm mức độ được không?
- `quet(lop, ky, so)`
- `main(argv)`
