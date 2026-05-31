# Hướng dẫn soạn bài (Authoring Guide) — luật điền lesson JSON

> **Tài liệu này thay cho prompt `WEAVER_PROMPT`/`SEED_PARSER_PROMPT` cũ.** Trước đây các luật soạn bài nằm trong chuỗi prompt Python gửi cho OpenAI (`content_weaver.py`, `seed_parser.py`). Nhánh tự động đó đã được rút gọn (xem [plan.md](plan.md) §"v1 vision"). Giờ **người soạn + Claude trong chat** điền trực tiếp khung `new-lesson`, nên các luật đó được kết tinh ở đây để **dùng sống** — Claude và giáo viên bám theo file này khi soạn.
>
> Quy ước kỹ thuật (token `[[br]]`, `[[blank:W]]`, escape `&`…) cũng có trong [README.md](README.md); file này tập trung vào **luật sư phạm + trình bày** ở mức chi tiết.

## 0. Nguyên tắc tối cao

- **KHÔNG bịa đề (no-fabrication).** Bài toán phải lấy từ **PDF nguồn của Thầy** trong folder tuần (hoặc đề thi thật đã có đáp án). Trước đây cổng `weave` ép điều này bằng `verified_scraped_bank`; giờ nó là **kỷ luật con người**: nếu nguồn thiếu dạng cần, **hỏi Thầy**, đừng tự chế đề/đáp án.
- **Đáp án phải đúng.** Sau khi điền, chạy `validate` — `sympy_solver` sẽ giải lại đại số độc lập để đối chiếu. Hình học SymPy yếu → tự kiểm tay.
- **Human-in-the-loop:** soạn → `validate` → Thầy xem → `approve` → `build`. Không tự ý in khi chưa duyệt.

## 1. Bám đúng tầm — chống "đần", chống "trẻ con hoá"

Nguồn chân lý độ khó: `config/difficulty_profile.json` (giờ **chỉnh tay**/để Claude điền theo chương, không còn `seed_parser` sinh tự động). Các khóa quan trọng:

- `ceiling.level` + `ceiling.exemplars`: **trần độ khó** — bài khó nhất (Luyện tập 2 / "trùm cuối") **phải chạm trần** này (`boss_must_hit_ceiling`).
- `floor.level` + `floor.note`: **sàn** — KHÔNG đi dưới sàn. Mức thấp nhất là "tự dựng lời giải có giàn giáo", **không nhắc lại định nghĩa vỡ lòng**.
- `hook_forbidden_patterns`: chặng Khám phá (Hook) **không** được là câu hỏi định nghĩa kiểu "… là gì", "thế nào là …". Hook là **câu đố/thách thức** đánh thức trực giác.
- `ramp`: luật tầng Mở rộng (xem §3).

`difficulty_gate` (chặn) + `gradient_gate` (cảnh báo) khi `validate` sẽ soi các luật này.

## 2. Cấu trúc 5 chặng × 4 tầng

Mỗi bài đúng **5 chặng** (kind cố định), mỗi chặng mang các block phù hợp. 4 tầng độ khó: **Ví dụ mẫu → Bài tập trên lớp → BTVN → Mở rộng**.

| # | `kind` | Vai trò | Ghi chú |
|---|--------|---------|---------|
| 1 | `review` | Khám phá / KTBC | Ôn nhanh kiến thức nền + 1 worked example trọn vẹn. Có nhịp cầu, **không nhảy gấp** sang lý thuyết mới. |
| 2 | `concept` | Khái niệm + Ví dụ mẫu | Phát biểu khái niệm/định lí cốt lõi; **≥1 "Ví dụ mẫu"** làm theo từng bước. Kèm ghi chú *"Đích đến thi vào 10"* (kỹ năng này tái xuất ở câu nào của đề vào 10). |
| 3 | `practice1` | Luyện tập 1 — BT trên lớp (nền) | Bài đại diện, làm cùng GV. `tier="onclass"`. |
| 4 | `practice2` | Luyện tập 2 — BT trên lớp (vận dụng) | Ưu tiên dạng **có trong đề vào 10**; bài khó dần, **chạm trần** `ceiling.level`. `tier="onclass"`. |
| 5 | `reflection` | Tổng kết | Trên phiếu **chỉ** là "Tổng kết": 1–2 câu chốt + **sơ đồ tư duy điền khuyết** (`mindmap`) đặt **ở đầu** blocks. BTVN/Mở rộng gắn tier ở **sau** (xem §3). |

**Đánh số bài LIỀN MẠCH** cả phiếu (Bài 1, 2, 3, …), không đánh lại theo từng dạng. **Không bỏ bài nào của nguồn** — chỉ phân tầng lại.

## 3. Chặng 5 — BTVN & Mở rộng tự tách; tầng Mở rộng là "THANG"

- Trên phiếu chặng 5 chỉ hiện **Tổng kết + sơ đồ tư duy**. Renderer `split_reflection` **tự tách** các block `problem` có `tier="btvn"` thành mục **"BÀI TẬP VỀ NHÀ"** và `tier="extend"` thành **"BÀI TẬP MỞ RỘNG"** (banner tự in trên cả handout/guide/slide). **ĐỪNG tự gõ tiêu đề mục** — chỉ cần gắn đúng `tier`.
- Câu **"nhịp cầu"** (block `para` có chữ "nhịp cầu"/"mở rộng") đặt **ngay trước** cụm extend → sẽ thuộc mục Mở rộng.
- **Mở rộng phải là một THANG 2–3 bậc, KHÔNG phải 1 bài dốc đứng:**
  - `ramp.extend_min_problems` (thường 2): ít nhất 2 bài extend, mỗi bài cao hơn bài trước **đúng một bước kỹ thuật**.
  - `require_bridge_before_extend`: phải có **1 nhịp cầu** (`para`) trước cụm extend, chỉ rõ kỹ thuật mới khác bài trên lớp ở đâu.
  - `require_hints_on_extend`: mỗi bài extend kèm **`hints`** = 1–2 gợi ý "mở khi bí" (ĐỊNH HƯỚNG, **tuyệt đối không phải lời giải**) — in trên phiếu HS để hạ ngưỡng nhập. Lời giải đầy đủ chỉ nằm trong `solution`.

## 4. Quy tắc trình bày (bắt buộc — để phiếu chỉn chu)

1. **Không để chú thích GV lọt phiếu HS.** Tuyệt đối không viết "(GV làm)", "GV chốt", "GV hỏi"… vào `para/math/noted/problem` — đó là phiếu phát cho HS. Mọi hướng dẫn cho GV đặt trong `teacher_note`; lời giải đặt trong `solution` (cả hai chỉ in ở Sổ tay GV). `visual_linter` sẽ cảnh báo nếu phát hiện chữ "GV"/"giáo viên".
2. **Tách ý/bước bằng `[[br]]`.** Khi 1 block có nhiều ý a) b) c) hoặc nhiều bước (Bước 1, 2…), chèn `[[br]]` giữa các ý để mỗi ý xuống dòng riêng. **KHÔNG** đặt `[[br]]` ở cuối block.
3. **Ví dụ mẫu hiển thị cho HS** (bỏ nhãn "GV") và phải trình bày **từng bước** — tách bằng `[[br]]` hoặc đặt phép biến đổi chính trong block `math` riêng; không dồn cả lời giải vào một dòng dài. → **Để CHỖ ĐIỀN, KHÔNG in sẵn đáp số:** kết quả/đáp án trong ví dụ mẫu dùng `[[mblank:W]]` để **thầy + trò cùng làm tại lớp**; đáp án đầy đủ **chỉ ghi trong `solution`** (bản GV). Áp cho cả bảng ở ví dụ mẫu.
4. **Giao chỗ làm bài:** dùng block `writelines` (count phù hợp) sau cụm bài để HS có chỗ trình bày; chỗ điền ngắn dùng `[[blank:3cm]]`, chỗ điền trong công thức dùng `[[mblank:0.8cm]]`.
5. **Không dùng ký hiệu unicode thô** (→, ⟹, ≥, ≤, …) trong `text`/`title` — font có thể thiếu glyph (ra ô vuông). Dùng lệnh LaTeX trong `$...$`: `$\to$`, `$\Rightarrow$`, `$\ge$`, `$\le$`.
6. **Escape ký tự đặc biệt ở field văn bản thuần:** `&` → `\&`, `%` → `\%`, `#` → `\#` trong `title`/`eyebrow`/`label`. Sanitizer **không** bắt lỗi này nhưng nó **làm vỡ build** (lỗi "Misplaced alignment tab"). `validate` nay có cảnh báo riêng cho nó.
7. **Sơ đồ tư duy (`mindmap`):** nhãn nút ngắn gọn; chừa chỗ điền bằng `[[blank:W]]`; cây 3–5 nhánh, mỗi nhánh tối đa 2 cấp để không tràn trang.
8. **`solution` cũng phải xuống dòng (BẮT BUỘC):** mỗi bài một đoạn (dùng `\par\smallskip` giữa các bài); **mỗi bước biến đổi / mỗi dòng `⇒`** đặt trên dòng riêng bằng `[[br]]`. **Không** dồn cả lời giải thành một khối chữ. `solution` phải gồm **cả đáp án các ô trống của sơ đồ tư duy**. → **Cổng tự kiểm:** `validate` (visual_linter) **cảnh báo** nếu một đoạn lời giải dài hơn ~220 ký tự mà không có `[[br]]` — đó là dấu hiệu "bức tường chữ", phải tách bước.
9. **Nhắc "lập bảng / kẻ bảng" thì PHẢI có bảng thật** — dùng block `table` (`headers` + `rows`; mỗi ô cho phép `$...$` và `[[blank:W]]` để HS điền), **KHÔNG nói suông**. Ví dụ bảng đại lượng cho toán chuyển động:
   ```json
   {"type": "table", "caption": "Em điền bảng rồi lập phương trình",
    "headers": ["", "Tốc độ", "Quãng đường", "Thời gian"],
    "rows": [["Dự định", "[[blank:2.2cm]]", "$30$", "[[blank:2.4cm]]"],
             ["Thực tế", "[[blank:2.2cm]]", "$30$", "[[blank:2.4cm]]"]]}
   ```
   Số cột lấy theo `headers`; cột đầu canh trái, các cột sau canh giữa; renderer tự kẻ khung (handout/guide/slide đều hiện).
   **Quy ước điền bảng theo vị trí:**
   - Bảng ở **ví dụ mẫu (chặng `concept`)** → để **TRỐNG cho thầy + trò cùng điền** tại lớp; đáp án (giá trị đúng của từng ô) ghi trong `solution` để GV tham chiếu.
   - Bảng ở **luyện tập (`practice1/2`)** → để **TRỐNG HẲN các ô đại lượng** (cả số đã cho lẫn ẩn) cho HS tự điền; chỉ giữ tiêu đề cột + nhãn hàng làm giàn giáo.
9. **Ký hiệu cực trị: GHI RÕ BIẾN** — viết `$\min A=1$` / `$\max B=\tfrac94$` (KHÔNG viết trống "min = 1"). Nêu rõ điều kiện đạt cực trị qua bước bình phương: "dấu $=$ xảy ra khi $(x-3)^2=0$, tức $x=3$" (đừng nhảy thẳng "khi $x=3$"). Áp cho cả ví dụ mẫu lẫn `solution`.

## 5. Quy trình lệnh (nhắc lại)

```bash
python -m src.main new-lesson <folder tuần>     # sinh khung 5 chặng đầy block TODO
#   → điền nội dung theo guide này (Claude hỗ trợ, bám PDF nguồn)
python -m src.main validate <file.json>         # trọng tài: sanitizer/schema/difficulty/gradient/linter + SymPy
python -m src.main validate-all                 # (tuỳ chọn) gác cổng cả kho trước khi commit
python -m src.main approve <slug>               # Thầy duyệt
python -m src.main build <file.json>            # ra 3 PDF: handout, guide, slide
```

Sau khi sửa `config/design_tokens.json` (màu/font/branding) → chạy `python -m src.main rebuild` để lan thay đổi ra **mọi** phiếu đã build, không sót.

## 6. Bố cục CỐ ĐỊNH (bất biến) — người soạn chỉ điền nội dung, KHÔNG đụng template

Các phần này do template lo, **luôn ở yên một chỗ**; AI/người soạn tuyệt đối không chèn/sửa chúng trong lesson JSON:

- **Header phiếu** (handout/guide/summary) theo đúng 3 tầng bất biến:
  1. *nhãn* — "PHIẾU HỌC TẬP" / "SỔ TAY GIÁO VIÊN" / "… TỔNG KẾT CHƯƠNG";
  2. *tiêu đề bài* — **tự co cỡ chữ** qua macro `\titlefit` (`max width=\linewidth`): tên dài → thu nhỏ cho khít **một dòng**, tên ngắn → giữ cỡ gốc 18pt. **Không** wrap nhiều dòng làm xô lệch cấu trúc;
  3. *hàng cố định bên dưới* — handout & bản HS: `Họ và tên: ____    Lớp: ____`; guide: `Tài liệu lưu hành nội bộ … Đáp án & Mẹo sư phạm điều phối`; bản GV tổng kết: `Bản Giáo viên — có đáp án sơ đồ`.
- **Logo** (góc trái header), **watermark**, **khung viền brand 4 góc** — cố định mọi trang.
- **Footer**: tên công ty + bảng hotline + Website + **chữ ký `Biên soạn: Thầy Thái MathTech — ĐT 0386969199`** — cố định mọi trang (xem README §"Dấu ấn giáo viên"). **Đừng gỡ.**
- **Badge số chặng** (huy hiệu tròn), thanh nhấn trái khối chặng — cố định.
- **Slide**: mỗi `problem` / mỗi `noted` **tự tách một slide riêng** (chiếu từng bài như đang dạy); slide bìa + footline chữ ký cố định.

→ Tên bài **dài bao nhiêu cũng được** — template tự co, không vỡ layout. Nguồn chỉnh các phần cố định: `templates/base_*.tex.j2` + `templates/preamble/_macros.tex.j2` (`\titlefit`) + `_beamer.tex.j2`. Sửa xong một chỗ → `rebuild` để áp cho tất cả.

## 7. Lượng bài, phân tầng \& tách phiếu (KHÔNG ăn xén, KHÔNG quá tải)

**Nguyên tắc vàng:** "đầy đủ, không ăn xén" **≠** "nhồi hết vào giờ trên lớp". Hai việc khác tầng:

- **Tầng `onclass` (core trên lớp)** — giữ **vừa đủ một buổi**. Mốc tham khảo buổi **3 giờ**: ~**12–14 phương trình / 10–12 bài toán đố** (gồm cả ví dụ mẫu). Đừng nhồi thêm onclass → HS yếu sẽ đuối.
- **Tầng `btvn` + `extend` (đệm)** — đây mới là chỗ chứa **toàn bộ bài dư của nguồn** + thang nâng cao. In **ngay trên phiếu** để HS giỏi/try-hard **làm xong core là lật tiếp, tự chạy, không phải đợi** bạn yếu. Đây là cách "không bỏ phí bài nguồn".
- **Bài `★` Thử thách (tự chọn)** — 1–2 bài khó nhất của nguồn (đặt ẩn phụ bậc cao, tình huống lạ); gắn `tier="extend"`, `statement` mở đầu `"\\textbf{Thử thách (tự chọn) —} …"`. Dành cho nhóm cày tới kiệt.

**Tách phiếu khi nguồn giàu / nhiều dạng:** một folder tuần được phép chứa **nhiều lesson JSON** (mỗi file = một phiếu, slug riêng, output riêng). Quy ước:
- Đặt `eyebrow` có hậu tố **"PHIẾU A" / "PHIẾU B"** và `slug` mô tả nội dung (vd `pt-tich-va-an-o-mau`, `giai-bai-toan-lap-pt`).
- Chia theo **mạch sư phạm**, không chia ngẫu nhiên: vd tuần "PT quy về bậc nhất" → **Phiếu A** (PT tích + ẩn ở mẫu) · **Phiếu B** (giải bài toán bằng lập PT). Mỗi phiếu tự đủ 5 chặng + core + đệm cho một buổi.
- `progress` tự đếm từng phiếu là một bài; build từng phiếu độc lập.

**Slide:** vì mỗi `problem` đã tách một slide riêng (mục 6), HS giỏi trên màn chiếu cũng theo nhịp từng bài — phần BTVN/mở rộng nằm ở các slide "Bài tập về nhà"/"Bài tập mở rộng (tự chọn)" cuối, lật tới khi cần.
