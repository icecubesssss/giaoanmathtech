# HƯỚNG DẪN KIẾN TRÚC & PROMPT MASTER ĐIỀU HÀNH AGENT (MATHTECH ENGINE)

> Phiên bản 2.0 — đã vá các lỗ hổng cấu trúc, bổ sung tầng biên dịch, chốt chặn bảo mật LaTeX, và đặc biệt nâng cấp **Hệ Thống Thiết Kế (Design System)** để phiếu in/slide đạt chuẩn xuất bản chuyên nghiệp, không còn "phèn".

> ⚠️ **TRẠNG THÁI HIỆN HÀNH (cập nhật 2026-05-30) — ĐỌC TRƯỚC.**
> Tài liệu này mô tả **tầm nhìn v1**: dây chuyền tự động hoàn toàn `ingest → scrape → weave` (Mathpix OCR + bot cào đề đêm + LLM tự dệt). **Nhánh tự động đó đã được RÚT GỌN/GỠ BỎ.** Thực tế vận hành đã hội tụ về luồng gọn hơn, do **người soạn + Claude** điền nội dung trực tiếp rồi để máy kiểm & in:
> `progress → new-lesson → (Claude điền) → validate → approve → build`.
> - Các phần **không còn trong code:** `ingest/` (Mathpix), `scrapers/` (cào + APScheduler), và các agent `seed_parser.py` / `web_scouter.py` / `content_weaver.py`. Phần lõi vẫn nguyên: `schema/`, `validators/`, `templates/`, `compiler/`, `feedback/` + `evolution_engine.py`.
> - **Luồng & lệnh hiện hành:** xem [README.md](README.md). **Luật soạn bài** (kết tinh từ prompt cũ): xem [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md).
> - Phần dưới giữ nguyên làm **lịch sử thiết kế**; các mục đã đổi được chú thích **[v1 — đã rút gọn]** ngay tại chỗ.

Tài liệu này cung cấp sơ đồ thư mục hoàn chỉnh cùng bộ Master System Prompt để nạp vào Claude (hoặc Cursor/Roo Code) nhằm xây dựng, vận hành và nâng cấp hệ thống phiếu học tập tự động.

---

## I. SƠ ĐỒ THƯ MỤC TOÀN DIỆN (PRODUCTION-GRADE TREE)

Thầy thiết lập đúng cấu trúc này trong không gian làm việc của VS Code:

```
math-worksheet-factory/
├── .env                                # API Keys thật (KHÔNG commit) — Mathpix, LLMs
├── .env.example                        # Mẫu khai báo biến môi trường (commit cái này)
├── .gitignore                          # Bỏ qua .env, outputs/, __pycache__, *.aux, *.log
├── requirements.txt                    # [hiện hành] jinja2, pydantic, sympy, python-dotenv, pytest  (đã bỏ requests/bs4/APScheduler theo nhánh auto v1)
├── pyproject.toml                      # Cấu hình project + pytest + ruff (lint)
├── README.md                           # Hướng dẫn cài đặt TeX Live + chạy hệ thống
│
├── config/
│   ├── settings.py                     # ĐỌC key từ .env qua python-dotenv (KHÔNG hardcode key)
│   ├── taxonomy_matrix.json            # Ma trận kiến thức & mục tiêu toán học cả năm học
│   ├── difficulty_profile.json         # ⭐ "Vân tay độ khó" của seed: trần & sàn độ khó, đối tượng
│   ├── design_tokens.json              # ⭐ NGUỒN CHÂN LÝ THIẾT KẾ: màu, font, lề, spacing scale
│   └── prompts/                        # PROMPTS CON (tách biệt khỏi mã nguồn Python)
│       ├── seed_parser.txt             # Prompt bóc tách "ADN" phiếu mẫu của Thầy
│       ├── web_scouter.txt             # Prompt điều khiển bot quét đề thi thật có đáp án chuẩn
│       ├── content_weaver.txt          # Prompt dệt kịch bản 5 chặng sư phạm
│       └── conflict_resolver.txt       # Bộ lọc phản hồi mâu thuẫn để tiến hóa style
│
├── templates/                          # KHUÔN ĐÚC GIAO DIỆN JINJA2 (Bất biến đối với AI)
│   ├── preamble/
│   │   ├── _fonts.tex.j2               # Khai báo font tiếng Việt (XeLaTeX/fontspec)
│   │   ├── _colors.tex.j2             # Bảng màu sinh từ design_tokens.json
│   │   └── _macros.tex.j2             # Macro toán & lệnh tạo khung tcolorbox dùng chung
│   ├── base_handout.tex.j2            # Phiếu in HS (A4 dọc — chừa trống dòng kẻ)
│   ├── base_slide.tex.j2             # Slide TV (16:9 — Beamer chữ siêu to)
│   ├── base_guide.tex.j2             # Sổ tay GV (hiện đỏ đáp án + mẹo)
│   └── components/                     # Linh kiện giao diện 5 chặng
│       ├── hook.tex.j2                 # Chặng 1 — The Hook
│       ├── discovery.tex.j2            # Chặng 2 — Lý thuyết điền khuyết
│       ├── levelup.tex.j2             # Chặng 3 — Bài tập Level Up
│       ├── boss.tex.j2                 # Chặng 4 — Trùm cuối (Boss Fight)
│       └── reflection.tex.j2           # ⭐ Chặng 5 — Tổng kết & tự phản tỉnh (BỔ SUNG)
│
├── inputs/
│   └── seeds/
│       └── root_document.pdf           # File PDF/ảnh gốc của Thầy làm hạt giống sư phạm
│
├── storage/                            # KHO LƯU TRỮ VĨNH VIỄN (càng dùng càng thông minh)
│   ├── run_state.json                  # ⭐ CHECKPOINT: trạng thái từng bài (resume khi đứt session)
│   ├── verified_scraped_bank/          # Đề cào mạng ĐÃ CÓ ĐÁP ÁN CHUẨN CỦA CON NGƯỜI
│   │   ├── algebra.json                # Ngân hàng đề đại số
│   │   └── geometry.json               # Ngân hàng đề hình học
│   └── evolution_kb/
│       ├── global_style_rules.json     # Luật thiết kế thị giác AI tự tiến hóa
│       ├── style_boundary_limits.json  # Rào chắn (cấm font slide >36pt hoặc <24pt)
│       └── style_history/              # ⭐ Snapshot mỗi lần AI sửa style (để rollback)
│
├── outputs/                            # ⭐ NƠI ĐỔ SẢN PHẨM (BỔ SUNG — không commit)
│   └── <ten_bai>/                      # Mỗi bài 1 thư mục: handout.pdf, slide.pdf, guide.pdf + log
│
├── src/                                # LÕI ĐIỀU HÀNH BẰNG PYTHON
│   ├── __init__.py
│   ├── main.py                         # Điểm chạy CLI trung tâm
│   ├── schema/                         # PYDANTIC SCHEMAS (khóa cứng cấu trúc dữ liệu)
│   │   ├── __init__.py
│   │   ├── base_schema.py              # Định dạng 1 bài toán (đề, lời giải, biến số)
│   │   ├── lesson_package.py           # Cấu trúc tích hợp cả 5 chặng của buổi học
│   │   └── feedback_schema.py          # Cấu trúc tệp phản hồi
│   ├── ingest/                         # ⭐ TẦNG OCR/BÓC TÁCH (BỔ SUNG)
│   │   ├── __init__.py
│   │   └── mathpix_ocr.py              # Gọi Mathpix bóc PDF/ảnh hạt giống → LaTeX
│   ├── agents/                         # BAN ĐIỀU PHỐI AI SIÊU VI MÔ
│   │   ├── __init__.py
│   │   ├── seed_parser.py              # Phân tích file hạt giống của Thầy
│   │   ├── web_scouter.py              # Điều khiển bot quét đề có đáp án tương đồng
│   │   ├── content_weaver.py           # Dệt dữ liệu thô vào đúng 5 chặng + bám taxonomy_matrix
│   │   ├── feedback_parser.py          # ⭐ Parse active_feedback.md → feedback_schema (BỔ SUNG)
│   │   └── evolution_engine.py         # Đọc feedback, nâng cấp prompt/style + lưu snapshot
│   ├── scrapers/                       # TRẠM CÀO CƠ KHÍ KHÔNG DÙNG LLM
│   │   ├── __init__.py
│   │   ├── scheduler.py                # ⭐ APScheduler chạy cào lúc 0h (BỔ SUNG)
│   │   ├── offline_worker.py           # Gom đề về kho lúc nửa đêm; cấm cào trực tiếp khi làm phiếu
│   │   ├── mathjax_parser.py           # Dịch MathJax/KaTeX trên web về LaTeX sạch
│   │   ├── html_cleaner.py             # Lọc mã rác quảng cáo + tôn trọng robots.txt
│   │   └── dedup.py                    # ⭐ Khử trùng lặp đề trong ngân hàng (BỔ SUNG)
│   ├── compiler/                       # ⭐ TẦNG BIÊN DỊCH (BỔ SUNG — đã thiếu ở v1)
│   │   ├── __init__.py
│   │   ├── jinja_renderer.py           # Đổ data JSON sạch vào template Jinja2
│   │   └── latex_builder.py            # Gọi latexmk (XeLaTeX), NO-shell-escape, bắt log
│   └── validators/                     # HỆ THỐNG TRỌNG TÀI KIỂM THỬ KHÔNG BA PHẢI
│       ├── __init__.py
│       ├── schema_validator.py         # Kiểm tra toàn vẹn cấu trúc JSON (ngoài Pydantic)
│       ├── latex_sanitizer.py          # ⭐ CHẶN \write18, \input, \openout… (BẢO MẬT)
│       ├── sympy_solver.py             # Trọng tài Đại số: giải độc lập SymPy so khớp nghiệm
│       ├── difficulty_gate.py          # ⭐ CHỐNG "ĐẦN": chặn nội dung dưới sàn độ khó của seed
│       ├── geometry_gate.py            # ⭐ Cổng hình học: SymPy yếu → đánh dấu human-verified
│       └── visual_linter.py            # Trọng tài Thị giác: bẻ dòng toán dài + check log latexmk
│
├── feedback/
│   └── active_feedback.md              # Thầy gõ nhận xét sau buổi dạy để AI tự học
│
└── tests/                              # KIỂM THỬ UNIT TESTS
    ├── test_sympy_solver.py            # Độ nhạy bộ giải toán độc lập SymPy
    ├── test_latex_sanitizer.py         # ⭐ Đảm bảo chặn được lệnh LaTeX độc hại
    ├── test_render.py                  # ⭐ Render thử template → kiểm cú pháp Jinja2 thật
    └── test_compiler.py                # Compile thử 1 PDF tối giản (smoke test)
```

---

## II. GIẢI THÍCH CHỨC NĂNG CÁC TẦNG TƯƠNG TÁC

### Tầng 0 — `ingest/` (Bóc tách hạt giống) — **[v1 — ĐÃ RÚT GỌN]**
*(Đã gỡ.)* Ý tưởng cũ: `mathpix_ocr.py` gọi Mathpix bóc PDF/ảnh hạt giống thành LaTeX, rồi `seed_parser.py` rút "ADN sư phạm". **Hiện hành:** Thầy để PDF nguồn trong folder tuần; **Claude đọc trực tiếp** đề trong PDF khi soạn (không cần OCR riêng). Hồ sơ độ khó `config/difficulty_profile.json` nay **chỉnh tay**/để Claude điền theo chương.

### Tầng 1 — `scrapers/` (Cào dữ liệu nền) — **[v1 — ĐÃ RÚT GỌN]**
*(Đã gỡ toàn bộ `scrapers/` + APScheduler.)* Ý tưởng cũ: bot cào đề đêm vào `verified_scraped_bank`. **Hiện hành:** nguồn đề là **PDF của Thầy** trong `inputs/seeds/...`.
**Nguyên tắc bất di (vẫn giữ — nay là kỷ luật con người):** Tuyệt đối không bịa số/đề. Mọi bài phải bám PDF nguồn của Thầy (Ground Truth có đáp án); thiếu dạng nào thì **hỏi Thầy**, không tự chế. Xem [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md) §0.

### Tầng 2 — `schema/` & `validators/` (Chốt chặn Logic & Bảo mật)
- Dữ liệu thô ép vào **Pydantic Schema** (đúng cấu trúc).
- `latex_sanitizer.py` **quét và loại bỏ** mọi lệnh LaTeX nguy hiểm trước khi cho phép đưa vào template.
- `sympy_solver.py` giải độc lập bằng máy để đối chiếu đáp án đại số — lệch dù 1 dấu `±` là loại bài đó.
- `geometry_gate.py`: vì SymPy yếu với hình học tổng hợp, bài hình **không** được SymPy "duyệt mù" mà phải mang nhãn `human_verified=true` mới được dùng.

### Tầng 3 — `templates/` & `compiler/` (Đổ khuôn & Xuất bản)
**Cấm AI tự gõ mã LaTeX giao diện.** `jinja_renderer.py` lấy data toán sạch từ Tầng 2 bơm đồng thời vào 3 mẫu. `latex_builder.py` gọi `latexmk` với engine **XeLaTeX** (để hỗ trợ tiếng Việt) và **tắt `-shell-escape`** (chặn thực thi mã). 3 đầu ra: Phiếu in HS, Slide TV, Sổ tay GV — đổ vào `outputs/<ten_bai>/`.

### Tầng 4 — `feedback/` & `evolution_engine.py` (Tiến hóa có kiểm soát)
`feedback_parser.py` chuyển nhận xét markdown tự do của Thầy thành `feedback_schema`. `evolution_engine.py` nâng cấp prompt/style nhưng **mỗi lần sửa đều lưu snapshot** vào `style_history/` để rollback — chống "trôi style".

### Luồng điều hành CLI (`main.py`) — **[CẬP NHẬT]**
Mỗi giai đoạn là một sub-command độc lập, ghi tiến độ vào `storage/run_state.json` để **resume được khi session đứt**. Luồng **hiện hành** (đã bỏ `ingest/scrape/weave`):
```
python -m src.main progress [--grade --subject --todo]  # quét tuần còn thiếu
python -m src.main new-lesson <folder tuần>             # sinh khung 5 chặng đầy block TODO
#   → Claude điền nội dung theo HUONG-DAN-SOAN-BAI.md (bám PDF nguồn của Thầy)
python -m src.main validate <file.json>                # SymPy + sanitizer + schema + difficulty + gradient + linter
python -m src.main validate-all [--grade --subject]    # gác cổng cả kho trước khi build/commit
python -m src.main approve <slug>                       # APPROVE (human-in-the-loop)
python -m src.main build   <file.json>                 # render Jinja + Tectonic → outputs/<...>/<slug>/
python -m src.main rebuild  [--grade --subject --all]  # build lại hàng loạt sau khi đổi design_tokens
python -m src.main status                               # xem run_state.json: bài nào tới bước nào
```

### Đường lui khi nguồn thiếu bài (no-fabrication safe-fail) — **[CẬP NHẬT: kỷ luật con người]**
Nếu PDF nguồn của Thầy **không có** dạng bài đang cần, hệ thống **KHÔNG được bịa**. Trước đây cổng `weave` tự ghi `status="blocked_no_source"`; nay khâu dệt do người + Claude làm nên đây là **kỷ luật bắt buộc khi soạn**: dừng lại, báo Thầy rõ thiếu dạng nào, và đề xuất 1 trong 2 lối: (a) Thầy bổ sung đề/PDF nguồn cho dạng đó, (b) Thầy duyệt tay nới tiêu chí. Tuyệt đối không tự chế đề/đáp án.

---

## III. ⭐ HỆ THỐNG THIẾT KẾ CHUYÊN NGHIỆP (DESIGN SYSTEM) — CHỐNG "PHÈN"

> Đây là tầng được nâng cấp khắt khe nhất. Toàn bộ thẩm mỹ phải tuân `config/design_tokens.json` — **không màu/font/khoảng cách nào được "chế tay"**. Mục tiêu: phiếu trông như sách giáo khoa cao cấp / tài liệu xuất bản, không như file Word in vội.

### 1. Typography (xương sống của sự "sang")
- **Engine bắt buộc: XeLaTeX** (không dùng pdfLaTeX) để nhúng font tiếng Việt thật.
- **Font chữ thường:** một bộ serif nhân văn dễ đọc cho phiếu in (vd *Source Serif 4* / *Noto Serif*); **font sans hình học** cho slide (vd *Inter* / *Be Vietnam Pro*). **Cấm dùng Computer Modern mặc định** — đây là dấu hiệu "phèn" số 1.
- **Font toán:** dùng `unicode-math` với font toán đồng bộ (vd *STIX Two Math* / *Libertinus Math*) — toán và chữ phải cùng "gia đình thị giác".
- **Thang cỡ chữ (type scale) theo tỉ lệ, không tùy hứng:** body 12pt → ratio 1.25 (Major Third). Tiêu đề chặng, đề bài, ghi chú đều phải nằm trên thang này.
- **Cấm tuyệt đối:** in đậm + gạch chân + viết hoa toàn bộ cùng lúc; hơn 2 họ font trên một trang; chữ nghiêng cho cả đoạn dài.

### 2. Bảng màu (palette kỷ luật, tối đa 1 màu nhấn)
- **Quy tắc 60-30-10:** 60% nền trắng/giấy, 30% mực than (`#1A1A2E` thay vì đen tuyền), 10% **một** màu thương hiệu duy nhất.
- Mỗi chặng có **một sắc độ** (tint nhạt ~8-12%) của màu thương hiệu để phân biệt, **không** mỗi chặng một màu cầu vồng.
- Đáp án trong Sổ tay GV: dùng đỏ trầm (`#C0392B`), không đỏ chói.
- **Cấm:** gradient lòe loẹt, đổ bóng đậm, màu bão hòa cao (neon), clip-art.

### 3. Lưới & khoảng trắng (cái khiến mắt thấy "đắt tiền")
- **Khoảng trắng là tính năng, không phải chỗ trống lãng phí.** Lề rộng rãi (handout ≥ 2cm), giãn dòng 1.15–1.3.
- **Spacing scale dạng 4pt** (4/8/12/16/24/32) — mọi `\vspace` phải lấy từ thang này, không gõ số lẻ.
- Khung bài (`tcolorbox`): bo góc nhẹ (2–4pt), viền mảnh 0.5pt **hoặc** nền tint (chọn 1, không cả hai), padding trong khung đều nhau.

### 4. Linh kiện & icon
- Icon dùng bộ thống nhất (vd *Font Awesome* / *Lucide*), nét đồng đều, **cùng kích thước**, đặt canh lề trái tiêu đề chặng. **Cấm trộn emoji với icon vector.**
- Đánh số bài/câu nhất quán (vd huy hiệu tròn cho số chặng).
- Header/footer: tên bài + lớp + số trang, mảnh và mờ (không chiếm spotlight).

### 5. Quy tắc riêng cho Slide TV (chống vỡ khung & chống chữ kiến)
- Font toán ≥ 32pt (rào cứng 24–36pt theo `style_boundary_limits.json`).
- **Một ý / một slide.** Tối đa ~5 dòng nội dung.
- Dòng toán dài: bắt buộc tự bẻ qua `\begin{aligned}` (do `visual_linter.py` xử lý **bằng code xác định**, không giao LLM).
- Tương phản tối thiểu WCAG AA cho chữ trên nền (đọc rõ từ cuối lớp).

### 6. "Smell test" — dấu hiệu phèn cần loại ngay
Comic Sans/Times mặc định • > 2 font • cầu vồng màu • emoji thay icon • viền dày + đổ bóng đậm • chữ ép sát lề • toán dính chữ • căn lề lộn xộn • WordArt/gradient.

---

## III-B. ⭐ KHÓA CHỐNG "ĐẦN" — DIFFICULTY & TONE CALIBRATION

> Rủi ro lớn nhất của hệ thống không phải lỗi kỹ thuật, mà là **đẻ ra phiếu ngây ngô dưới tầm học sinh**. Một AI ráp đúng quy trình vẫn có thể cho ra Hook kiểu "vì sao cần dấu lớn hơn" cho học sinh lớp 9 ôn thi vào 10. Mục này khóa chặt 3 điểm rò rỉ.

> **[v1 — cơ chế đã đổi, LUẬT vẫn giữ]** `seed_parser.py`/`content_weaver.py` đã gỡ; nhưng các LUẬT chống "đần" dưới đây vẫn bắt buộc — nay do **Claude tuân theo khi soạn** ([HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md) §1–§2) và được `difficulty_gate`/`gradient_gate` soi khi `validate`.

### 1. seed_parser phải quét TOÀN BỘ & chốt "trần độ khó" — *(nay: chỉnh `difficulty_profile.json` tay)*
Cấm chỉ đọc trang lý thuyết đầu. Hồ sơ `difficulty_profile.json` (trước do `seed_parser.py` sinh, nay điền tay theo chương) phải chốt:
- **Đối tượng** (vd: HS lớp 9 ôn thi vào 10).
- **Trần độ khó** = bài KHÓ NHẤT trong seed (vd với file Bất đẳng thức: chứng minh $a^2+b^2+c^2\ge ab+bc+ca$, BĐT trong tam giác, GTNN/GTLN của phân thức).
- **Sàn độ khó** = mức thấp nhất được phép xuất hiện (thường là Level Up, KHÔNG phải nhắc lại định nghĩa vỡ lòng).
- **Kỹ thuật cốt lõi** seed dạy (vd: "xét hiệu $A-B$", dùng $M^2\ge0$).

### 2. Bám trần + luật giọng văn (chống trẻ con hoá) — *(nay: Claude tuân khi soạn)*
Khi soạn (Claude điền lesson JSON) phải tuân các luật cứng:
- Mọi chặng bám `difficulty_profile.json`; chặng cuối (Boss) phải chạm **trần** độ khó của seed.
- **Hook KHÔNG được giảng lại khái niệm vỡ lòng.** Hook là một bài toán/tình huống gây tò mò ĐÚNG TẦM (vd "không quy đồng, so sánh $\frac{2024}{2023}$ và $\frac{2025}{2024}$"; hoặc bài thực tế BMI/nồng độ cồn có sẵn trong seed).
- **Giọng văn**: tôn trọng trình độ người học, không hạ cố, không emoji trẻ con, không câu cảm thán thừa.

### 3. difficulty_gate.py — cổng gác sàn
Trước khi cho compile, `difficulty_gate.py` từ chối gói bài nếu **bài khó nhất còn dưới sàn** của `difficulty_profile.json`, hoặc nếu Hook bị phát hiện chỉ là định nghĩa/nhắc lại lý thuyết. Vi phạm → **soạn lại** (sửa lesson JSON) rồi `validate` lại.

### 4. Lưới an toàn cuối: Human-in-the-loop
Thầy luôn thấy **nội dung thô của cả 5 chặng trước khi compile** (Mục IV §5). Bài nào đần → gõ "REJECT", chưa tốn token render. Đây là chốt chặn cuối cùng, đảm bảo không bao giờ in ra phiếu dưới tầm.

## IV. MASTER SYSTEM PROMPT NẠP THẲNG VÀO CLAUDE

Copy toàn bộ khối dưới làm System Prompt / `custom_instructions` cho Claude trong dự án:

```
# MASTER INSTRUCTION FOR MATHTECH ENGINE DEVELOPER

Bạn là Kỹ sư Hệ thống kiêm Trưởng bộ môn Khảo thí cao cấp tại MathTech, đồng thời là
Art Director chịu trách nhiệm thẩm mỹ xuất bản. Bạn thiết kế, lập trình và kiểm soát chất
lượng cho toàn bộ "MathTech Worksheet & Slide Compiler Engine".

## 1. NGUYÊN TẮC VẬN HÀNH TỐI CAO (ZERO-ERROR TOLERANCE)
- KHÔNG BỊA TOÁN: Không tự nghĩ ra số liệu/đề bài từ hư vô. Mọi bài toán phải kế thừa từ
  file hạt giống gốc hoặc trích từ verified_scraped_bank đã có đáp án con người (Ground Truth).
- KHÔNG TỰ VIẾT MÃ GIAO DIỆN LATEX: Toàn bộ thẩm mỹ khóa cứng trong templates/ và
  config/design_tokens.json. Bạn chỉ tạo JSON sạch (đề + lời giải) để nạp vào template.
- KHÔNG TỰ ĐẶT MÀU/FONT/KHOẢNG CÁCH: Mọi giá trị thị giác phải lấy từ design_tokens.json.
  Cấm hardcode mã màu hex hay cỡ chữ rời rạc trong nội dung.

## 2. CHỐT CHẶN BẢO MẬT LATEX (BẮT BUỘC)
- Mọi LaTeX cào từ web phải đi qua latex_sanitizer.py. Loại bỏ/ từ chối mọi lệnh:
  \write18, \input, \include, \openout, \catcode, \def lạ, \immediate.
- latex_builder.py luôn gọi latexmk với XeLaTeX và TUYỆT ĐỐI KHÔNG bật -shell-escape.

## 3. KỶ LUẬT THẨM MỸ — PHẢN BIỆN KHI BỊ ÉP LÀM XẤU (chống "phèn")
Bạn phải chủ động từ chối + đề xuất phương án sang hơn nếu yêu cầu vi phạm Design System:
- Dùng Computer Modern/Times mặc định, hoặc > 2 họ font trên một trang.
- Mỗi chặng một màu rực khác nhau (cầu vồng) thay vì sắc độ của 1 màu thương hiệu.
- Trộn emoji với icon vector; dùng gradient/đổ bóng đậm/WordArt.
- \vspace số lẻ ngoài thang 4pt; lề chật < 2cm cho handout.
- Vi phạm sư phạm: in lời giải lên phiếu HS, hoặc chữ slide < 24pt.

## 4. QUY TRÌNH BIÊN SOẠN SONG SONG 3 PHIÊN BẢN (KHỚP 100% TOÁN HỌC)
Tiến trình kiến tạo 5 chặng: Hook -> Discovery -> Level Up -> Boss Fight -> Reflection.
1. Phiếu HS (A4 dọc): ẩn lời giải, chèn \vspace{} (lấy từ spacing scale) để HS điền khuyết.
2. Slide TV (16:9): font toán >=32pt; dùng \pause của Beamer; dòng toán dài bẻ tự động
   bằng \begin{aligned} (do visual_linter xử lý, không tự tay).
3. Sổ tay GV: đầy đủ đáp án đỏ trầm chính xác 100% + hộp "MẸO SƯ PHẠM ĐIỀU PHỐI" cho GV
   mới nắm trong 3 phút trước giờ lên lớp.

## 5. GIAO THỨC HUMAN-IN-THE-LOOP (GÁC CỔNG KIỂM DUYỆT)
Không tự ý biên dịch PDF ngay. Mỗi bài:
- Bước 1: Trình cấu trúc kịch bản + dữ liệu thô (đề, đáp án) từng chặng lên Terminal.
- Bước 2: Hiển thị kết quả SymPy (TXĐ, tập nghiệm, nghiệm ngoại lai bị loại). Bài HÌNH HỌC
  phải báo rõ "human_verified" — không tự nhận đã kiểm bằng SymPy.
- Bước 3: Chỉ khi nhận lệnh "APPROVE" cho cả 5 chặng mới mở khóa chạy latex_builder.

## 6. TIẾN HÓA CÓ KIỂM SOÁT
Khi evolution_engine sửa prompt/style: luôn lưu snapshot vào storage/evolution_kb/style_history/
trước khi ghi đè, và không được vượt rào style_boundary_limits.json.

## 7. KHÓA CHỐNG "ĐẦN" — BÁM ĐÚNG TẦM HỌC SINH (BẮT BUỘC)
- Trước khi dệt, đọc config/difficulty_profile.json để biết đối tượng + trần/sàn độ khó của seed.
- Mọi chặng phải bám trần; chặng Boss phải chạm trần. CẤM ra nội dung dưới sàn (vd nhắc lại
  định nghĩa vỡ lòng cho HS lớp 9 ôn thi vào 10).
- Hook là bài toán/tình huống gây tò mò ĐÚNG TẦM, KHÔNG phải đoạn giảng khái niệm cơ bản.
- Giọng văn tôn trọng trình độ người học: không hạ cố, không emoji trẻ con, không cảm thán thừa.
- difficulty_gate.py sẽ từ chối gói vi phạm; nếu bị từ chối, dệt lại chứ không hạ tầm để qua cổng.
```

---

## V. BÀI TEST NGHIỆM THU CHO HỆ THỐNG

Chạy `pytest` trong VS Code. Bộ test đã được siết để kiểm **thật**, không chỉ kiểm tồn tại file:

```python
# File: tests/test_compiler.py
import os
import subprocess
import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = ["base_handout.tex.j2", "base_slide.tex.j2", "base_guide.tex.j2"]
COMPONENTS = ["hook", "discovery", "levelup", "boss", "reflection"]  # đủ 5 chặng


def test_template_existence():
    """Khuôn đúc giao diện + đủ 5 linh kiện chặng đã nằm đúng vị trí chưa."""
    for t in TEMPLATES:
        assert os.path.exists(f"templates/{t}"), f"Thiếu template {t}"
    for c in COMPONENTS:
        assert os.path.exists(f"templates/components/{c}.tex.j2"), f"Thiếu chặng {c}"


def test_pydantic_schema_integrity():
    """Import được các khóa định dạng dữ liệu cứng không."""
    try:
        from src.schema.lesson_package import LessonPackage  # noqa: F401
    except ImportError:
        pytest.fail("Thiếu/sai cấu hình lesson_package.py!")


def test_jinja_renders_without_error():
    """Render thật template với data mẫu — bắt lỗi cú pháp Jinja2 (không chỉ import)."""
    env = Environment(loader=FileSystemLoader("templates"))
    tpl = env.get_template("base_handout.tex.j2")
    out = tpl.render(lesson={"title": "Test", "stages": []})
    assert "\\documentclass" in out


def test_no_shell_escape_in_build():
    """latex_builder TUYỆT ĐỐI không được bật -shell-escape (chốt bảo mật)."""
    with open("src/compiler/latex_builder.py", encoding="utf-8") as f:
        assert "-shell-escape" not in f.read(), "Phát hiện -shell-escape: nguy cơ thực thi mã!"
```

```python
# File: tests/test_latex_sanitizer.py
import pytest
from src.validators.latex_sanitizer import sanitize, UnsafeLatexError

DANGEROUS = [r"\write18{rm -rf /}", r"\input{/etc/passwd}", r"\openout1=x", r"\immediate\write18{ls}"]


@pytest.mark.parametrize("payload", DANGEROUS)
def test_blocks_dangerous_commands(payload):
    with pytest.raises(UnsafeLatexError):
        sanitize(payload)


def test_allows_clean_math():
    assert sanitize(r"\frac{1}{2} + \sqrt{x}") == r"\frac{1}{2} + \sqrt{x}"
```

---

## VI. ĐIỀU KIỆN MÔI TRƯỜNG & GIỚI HẠN (PREREQUISITES)

- **TeX Live đầy đủ** (hoặc MacTeX) — chứa `xelatex`, `latexmk`, `tcolorbox`, `unicode-math`, `beamer`.
- **Font tiếng Việt cài sẵn ở hệ điều hành** (vd *Be Vietnam Pro*, *Noto Serif*, *STIX Two Math*). XeLaTeX không tìm thấy font sẽ lỗi compile ngay bài đầu — README phải có bước cài font này.
- **Rate-limit & chi phí cần theo dõi:** Mathpix (theo trang OCR), API LLM (theo token), và scraping (chạy đêm, có độ trễ giữa request + tôn trọng `robots.txt`). Khai báo ngưỡng trong `settings.py`.

## VII. LỘ TRÌNH BUILD THEO SESSION & NGÂN SÁCH TOKEN

Dựng cả engine (~40 file, 3.000–5.000 dòng) trong **một** session là quá nặng, dễ rớt giữa chừng. Chia 4 milestone, mỗi cái gọn trong 1 session:

| Session | Phạm vi | Ghi chú |
|---|---|---|
| **S1 — Khung xương** | `schema/` + `config/` + `templates/` (preamble + 3 base + 5 component) + `design_tokens.json` | Chốt Design System trước |
| **S2 — Trọng tài** | `validators/` (sympy_solver, latex_sanitizer, geometry_gate, visual_linter) + tests | Bảo mật + logic toán |
| **S3 — Biên dịch** | `compiler/` (jinja_renderer, latex_builder) + compile thử 1 PDF "hello" | Xác nhận toolchain XeLaTeX chạy |
| **S4 — Dữ liệu & AI** ~~`ingest/`, `scrapers/`, auto-`agents/`~~ **[v1 — đã rút gọn]** | Nay: người + Claude điền lesson JSON (`new-lesson` → `validate` → `build`) ra **1 phiếu hoàn chỉnh** | Nghiệm thu end-to-end |

### Ngân sách token khi đã build xong (cửa sổ ~200K/session)
Render LaTeX do Python/Jinja2 lo, **không tốn token LLM**. LLM chỉ tốn ở phân tích + dệt nội dung + đối thoại duyệt:

| Phiếu | Token ước tính | Vì sao |
|---|---|---|
| #1 | ~60–80K | nền 30–40K **+** debug template lần đầu **+** calibrate "gu" thiết kế |
| #2–5 | ~35–50K | còn tinh chỉnh style lặt vặt (evolution_engine đang học) |
| #6 trở đi | ~30–40K | ổn định ở mức nền |

→ **Mỗi phiếu thừa sức gọn trong 1 session.** Phiếu đầu đắt nhất vì gánh phần debug + chốt gu; phiếu sau rẻ dần nhưng **không về 0** (vẫn trả ~30–40K nền mỗi cái).

## VIII. TÓM TẮT CÁC ĐIỂM ĐÃ VÁ SO VỚI v1
1. Bổ sung `src/compiler/` (jinja_renderer + latex_builder) — v1 nhắc tới nhưng thiếu trong cây.
2. Bổ sung Chặng 5 `reflection.tex.j2` — đủ 5 chặng như prompt yêu cầu.
3. Bổ sung `outputs/` cho 3 PDF sản phẩm.
4. Thêm quản lý phụ thuộc & bảo mật key: `requirements.txt`, `.env`/`.env.example`, `.gitignore`.
5. Chốt chặn **LaTeX injection**: `latex_sanitizer.py` + cấm `-shell-escape`.
6. Khai báo **engine XeLaTeX + font tiếng Việt** rõ ràng (`preamble/_fonts.tex.j2`).
7. Tách **bẻ dòng toán** thành code xác định trong `visual_linter.py` (không giao LLM).
8. `geometry_gate.py`: thừa nhận SymPy yếu với hình → bắt buộc nhãn human-verified.
9. `taxonomy_matrix.json` được `content_weaver.py` đọc để phủ chương trình.
10. `feedback_parser.py` chuyển markdown tự do → schema; evolution lưu snapshot rollback.
11. Bổ sung `scheduler.py` (cào lúc 0h) và `dedup.py` (khử trùng lặp).
12. ⭐ Thêm hẳn **Mục III — Design System** để phiếu chuyên nghiệp, hết "phèn".
13. Siết bộ test: render thật, chặn shell-escape, chặn LaTeX độc hại.
14. ⭐ Thêm `storage/run_state.json` — checkpoint/resume khi session đứt.
15. ⭐ Định nghĩa luồng CLI trong `main.py`. **[Hiện hành]** progress → new-lesson → (Claude điền) → validate → validate-all → approve → build → rebuild → status (đã bỏ ingest/scrape/weave).
16. ⭐ Đường lui "no-fabrication safe-fail" khi ngân hàng thiếu bài khớp taxonomy.
17. ⭐ Mục VI: điều kiện môi trường (TeX Live + **cài font tiếng Việt**) + lưu ý rate-limit/chi phí.
18. ⭐ Mục VII: lộ trình build 4 session (S1–S4) + ngân sách token + đường cong chi phí phiếu đầu/sau.
19. ⭐ Mục III-B: KHÓA CHỐNG "ĐẦN" — `difficulty_profile.json` + `difficulty_gate.py` + luật bám trần/giọng văn trong Master Prompt, đảm bảo nội dung không dưới tầm học sinh.
