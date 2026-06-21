# AGENTS.md — Hướng dẫn cho MỌI tác nhân AI (Claude Code, Codex, Antigravity, Copilot, Gemini CLI…)

> Nguồn GỐC DUY NHẤT cho mọi công cụ AI. Các file CLAUDE.md / .github/copilot-instructions.md / GEMINI.md chỉ trỏ về đây.

Đây là **MathTech Engine**: soạn phiếu học tập Toán lớp 9 (ôn thi vào 10) từ PDF nguồn của Thầy → render ra 3 bản PDF (handout HS / guide GV / slide).

## ⚡ Bắt đầu nhanh (agent land-and-go — đọc cái này là chạy được)

1. **Đọc [PROJECT_MAP.md](PROJECT_MAP.md) TRƯỚC** (bản đồ module + symbol, tự sinh) — biết code nằm đâu mà khỏi mở từng file. Cũ thì `make map`.
2. **Menu việc:** `make help` (hoặc xem [Makefile](Makefile)). Quy trình 1 phiếu:
   ```bash
   # (MỚI · phân tầng) CHỐT SỐ CÂU TRƯỚC bằng phiếu thuyết minh (spec-first):
   make spec FOLDER="inputs/seeds/lop-9/dai-so/.../[C]tuanNN-<chu-de>" TIER=C
   make thuyetminh SPEC="<…>/thuyet-minh.json"   # → PDF Thầy đọc, chỉnh số câu & KHOÁ
   # rồi soạn phiếu bám spec đó:
   make new FOLDER="inputs/seeds/lop-9/dai-so/.../tuanNN-<chu-de>"   # sinh khung
   # → điền nội dung bám PDF nguồn (HUONG-DAN-SOAN-BAI.md) + ĐÚNG số câu spec
   make validate FILE=<file.json>        # gác cổng (FAST=1 bỏ SymPy lúc nháp); spec_gate so số câu với thuyết minh
   make build FILE=<file.json>           # 3 PDF song song (ONLY=handout xem nhanh)
   python -m src.main approve <slug>     # Thầy xem PDF rồi DUYỆT
   ```
3. Lệnh đầy đủ: `python -m src.main -h`. Tiến độ: `make progress`. Bank đủ câu không: `make coverage`.

> **SPEC-FIRST (Thầy chốt 2026-06-21):** số câu NB/TH/VD/VDC theo tầng A/B/C/X **cố định trong [config/tier_spec.json](config/tier_spec.json)** (đổi khi mở tầng/khối mới, soạn từng tuần không đụng). `new-thuyetminh` tự tính số câu mục tiêu từ đó; `build-thuyetminh` render PDF cho Thầy chốt; `spec_gate` (trong `validate`) so phiếu JSON với spec (±1 câu/band, opt-in khi có `thuyet-minh.json` cạnh bên). `duration_gate` cũng đọc tier_spec (hết số cứng). **VDC = band 4**; bài giàu **cắt bước (scaffold-decompose)** sinh NB/TH (xem HUONG-DAN-PHAN-TANG-LOP).

## Luật CỨNG độc lập công cụ — chạy `validate`

Dù bạn là Claude, Codex, Antigravity, Copilot hay người không dùng AI: mọi luật kiểm được tự động đều nằm trong **code Python**, không phải prompt. Chỉ cần chạy `python -m src.main validate <file.json>` (và `python -m pytest`) là nhận **cùng một bộ gác cổng** (sanitizer/schema/difficulty/visual_linter/gradient + SymPy). **Bắt buộc** validate sạch trước khi `approve`/`build`. Các nguyên tắc dưới đây là phần _con người/tác nhân_ phải tự giữ (validator không soi được).

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

1. **Tiêu đề chặng KHÔNG dùng thuyết minh giải thích** (chỉ để tên chặng chuẩn: "1. Khám phá", "3. Luyện tập 1", **XÓA BỎ** mọi phần giải thích phía sau dấu gạch ngang như "— Toán thực tế..."). Giữ `stage.title` thật ngắn gọn. `visual_linter` cảnh báo mốc 46 ký tự; template tự co (`adjustbox`) là lưới an toàn, không phải cớ để đặt tên dài.
2. **Hình minh hoạ (tikz/opener) vẽ ĐÚNG vật thật** — soi từng hình: heo đất ra heo/chồng xu (không ra cái nhà), thang máy ra thang máy… Hình sai/khó hiểu thì sửa hoặc bỏ (opener cho phép chỉ-chữ). `visual_linter` chặn tikz thiếu `\begin{tikzpicture}` và figure rỗng, nhưng KHÔNG biết hình vẽ có giống vật không — mắt người phải soi.
3. **Chấm sao theo MỨC ĐỘ NHẬN THỨC (trường `level`, ĐỘC LẬP với `tier`/nơi làm):**
   - `1` = **Nhận biết** ★☆☆ (vàng): 1 bước, áp dụng trực tiếp 1 công thức/định nghĩa.
   - `2` = **Thông hiểu** ★★☆ (vàng): 1–2 bước, hiểu quan hệ rồi suy ra.
   - `3` = **Vận dụng** ★★★ (vàng): 2–4 bước, ghép nhiều ý / bài thực tế đơn giản (lãi suất, %, đo đạc).
   - `4` = **Vận dụng cao** ★★★★ **MÀU KIM CƯƠNG** (`diamond`): đa tầng, không rập khuôn (chứng minh BĐT, tìm cực trị…).
     Mỗi `problem` PHẢI gắn `level` 1..4 (sao phản ánh độ khó THẬT, không phải `onclass/btvn`). `visual_linter` cảnh báo bài chưa chấm; bài `level:0` cũ thì renderer tự suy sao theo `tier` (tương thích ngược). Sao đầy `\ding{72}` + sao rỗng `\ding{73}`.
4. **Đặt tên đúng thứ tự bài học:** khi folder tuần có ≥2 phiếu, **tên file + `slug` PHẢI mang tiền tố `phieu-a-/phieu-b-/phieu-c-/phieu-d-`** và `eyebrow` "PHIẾU A/B/C/D" khớp vị trí (xem HUONG-DAN §7). Mở folder phải thấy sort đúng A→B→C→D — KHÔNG đặt slug thuần theo nội dung (phiếu tạo sau sẽ lên trước). Đổi/tách lại số phiếu thì sửa cả ba: file, slug, eyebrow (và `lessons` của phiếu tổng kết nếu có).
5. **Đáp án**: mọi PT/BPT/hệ phải **đối chiếu độc lập bằng SymPy** (`solve_univariate_inequality`/`solveset`) — chạy script kiểm TRƯỚC khi viết `solution`; hình học SymPy yếu thì tự kiểm tay + soi lại số trên hình.
6. **Soi bố cục SLIDE bằng ảnh (BẮT BUỘC cho `slide.pdf`).** Đọc PDF thẳng dễ bỏ sót lỗi bố cục — phải **render slide ra PNG rồi xem từng trang**:
   ```bash
   pdftoppm -png -r 80 "outputs/.../slide.pdf" /tmp/slidecheck/s   # → s-01.png, s-02.png…
   ```
   Xem (Read) lần lượt các PNG và soát:
   - **Bìa:** có badge "LỚP …" thì tiêu đề/chữ ký KHÔNG bị đẩy tràn đáy.
   - **Mở màn + hình minh hoạ NẰM CÙNG MỘT slide** (template tự bố cục chữ-trái/hình-phải; KHÔNG để hình rớt sang slide kế).
   - **Sơ đồ bước (B1→B2→B3…) NẰM NGANG ở DƯỚI**, phần "rút ra quy tắc" ở TRÊN — cùng một slide, không đè footer.
   - **Đề + các câu nhỏ a,b,c CÙNG MỘT slide** (đề dài thì renderer tự co `probfit`; KHÔNG để "đề một chỗ, câu nhỏ một nẻo").
   - Không có **chữ/hình đè footer** "MathTech … Slide N", không có trang trống.
     Renderer (`group_slide_segments`/`_seg_mode` + `_slide_blocks.j2`) đã lo các bố cục trên; nếu vẫn lệch thì sửa renderer/template rồi build lại, KHÔNG sửa tay JSON cho hợp một slide.
7. **KIỂM SOÁT THỜI LƯỢNG (CHỐNG THIẾU CÂU):** AI rất hay tạo thiếu bài tập, làm hụt quỹ giờ của buổi học (120 phút trên lớp). Bắt buộc xem log `[duration_gate]` sau lệnh `validate`. Nếu bị báo thiếu giờ, **PHẢI tự động sinh thêm bài tương đương hoặc kéo bài từ BTVN lên** sao cho lấp đủ quỹ thời gian (định mức: NB 1.5'/câu, TH 6'/câu, VD 12'/câu). Tuyệt đối không giao phiếu bị hụt thời lượng!
   Sửa xong checklist → build lại → mới trình Thầy.
   Kế hoạch tuần: [KE-HOACH-SOAN-BAI.md](KE-HOACH-SOAN-BAI.md). Luật soạn chi tiết: [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md).

## Nguyên tắc BẮT BUỘC khi soạn (bám HUONG-DAN §0)

1. **KHÔNG bịa đề** — lấy từ PDF nguồn; thiếu dạng thì hỏi Thầy.
2. **Đáp án phải đúng** — `validate` nay hỗ trợ tự đối chiếu đáp số đại số nếu bài có khai báo trường `check` (đáp án máy-đọc). Bài đại số NÊN kèm trường `check` trong seed để `validate` tự soi SymPy và chặn nếu sai (xem chi tiết tại KE-HOACH-AUTO-CHECK-DAP-AN.md và HUONG-DAN-SOAN-BAI.md). Với các phần khác hoặc khi chưa có `check`, vẫn phải **tự chạy SymPy** đối chiếu qua các hàm lẻ trong `sympy_solver.py` hoặc tự kiểm tay.
3. **Human-in-the-loop** — soạn → validate → **build PDF cho Thầy xem trước** → Thầy duyệt (approve). Bản build trước khi duyệt là bản nháp để Thầy đọc; chỉ phát hành chính thức sau khi approve.
4. **CHƯA CHẮC CÁCH DẠY THÌ HỎI THẦY (không tự đoán).** Khi không chắc nên _dẫn dắt / scaffolding_ một dạng thế nào (lời giải mẫu, mức chia bước, ví dụ mồi, chỉnh độ dốc) → **liệt kê bài/dạng phân vân và hỏi Thầy trước** rồi mới soạn. Validator không thể biết bạn đang phân vân — đây là kỷ luật của tác nhân.
5. **Scaffolding cho dạng dễ trừu tượng.** Làm chung–làm riêng, đặt ẩn phụ, chuyển động/dòng nước, %… nên có **một ví dụ mồi cụ thể** trước bài chính. Mẫu cách dạy Thầy đã nêu:
   - _Làm chung–làm riêng_ → pizza 8 miếng (A ăn 16′, B ăn 24′ → mỗi phút $\tfrac1{16}+\tfrac1{24}$) để dẫn vào $\tfrac1x$.
   - _Dòng nước_ → con thuyền không động cơ trôi theo dòng → $v_{xuôi}=v+v_{nước}$, $v_{ngược}=v-v_{nước}$.
   - _Phần trăm_ → hỏi "tăng 10% là 10% hay 110%? đề tính theo cái gì" (nhiều thêm vs phải trả tất cả).
6. **Ưu tiên "nghiệm đẹp" cho bài đại số** — được phép chỉnh số liệu đề cho nghiệm gọn (số nguyên); soi lại bằng SymPy. (Lượng giác/đo đạc thì đáp số gần đúng/tỉ số là bình thường.)
7. **Escape `\%` `\&` `\#`** trong MỌI field (kể cả `solution`/`teacher_note`). `visual_linter` nay có cảnh báo; `%`/`#` thô sai mọi nơi, `&` thô chỉ sai ngoài `$...$`.
8. **Quy chuẩn thiết kế "Mở màn thực tế":** Tình huống mồi phải (1) liên quan đến cái HS đã biết, (2) liên quan đến những gì HS thích (vé concert idol, phim C16, trend giới trẻ...). (3) Tuyệt đối **chưa nhắc đến khái niệm mới** nhưng phải diễn tả đúng bản chất khái niệm đó. Cần sử dụng công cụ AI sinh ảnh (như Gemini Banana) để tạo hình ảnh bắt mắt và chèn vào thông qua trường `"image"`.

## Nền tảng sư phạm — Thang Bloom \& Vygotsky (đọc để hiểu "vì sao")

Hai lý thuyết nền chi phối MỌI quyết định thiết kế phiếu (chấm sao, chia tầng, dẫn dắt) — không phải làm theo cảm tính. GV/tác nhân mới nên đọc kỹ:

- **Thang Bloom** (6 cấp nhận thức): <https://ocd.vn/thang-do-bloom-la-gi/>
- **Vygotsky — Vùng phát triển gần (ZPD) \& scaffolding**: <https://canhbuom.edu.vn/2023/07/06/lev-vygotsky/>

### 1. Thang Bloom → quyết định trường `level` (số sao)

Số sao KHÔNG phải "cảm giác khó/dễ" mà là **cấp độ nhận thức Bloom** của bài. 6 cấp Bloom (Nhớ → Hiểu → Vận dụng → Phân tích → Đánh giá → Sáng tạo) gom thành 4 mức `level`:

- `1` Nhận biết ★☆☆ = Bloom **Nhớ/Hiểu**: nhớ lại, áp dụng trực tiếp 1 định nghĩa/công thức.
- `2` Thông hiểu ★★☆ = Bloom **Hiểu → Vận dụng**: diễn giải, giải thích, biến đổi 1–2 bước.
- `3` Vận dụng ★★★ = Bloom **Vận dụng**: giải tình huống thực tế đơn giản, ghép nhiều ý cùng chủ đề.
- `4` Vận dụng cao ★★★★ (kim cương) = Bloom **Phân tích/Đánh giá/Sáng tạo**: chứng minh, cực trị, đổi biến — đa tầng, không rập khuôn.
  ⇒ Một bộ đề tốt phủ Bloom từ thấp lên cao; tỉ lệ NB-TH-VD (vd **tầng C 40-40-20**) chính là **phân bố theo Bloom**, không chia bừa. Soát `level` ở checklist §3 là soát "bài này thật sự đòi hỏi cấp Bloom nào".

### 2. Vygotsky ZPD/scaffolding → cách dẫn dắt \& chia tầng

**ZPD (vùng phát triển gần)** = khoảng giữa "HS tự làm được" và "làm được KHI CÓ hướng dẫn". Đặt độ khó bài vào đúng vùng này — không quá dễ (chán, bão hòa) cũng không quá khó (nản, bỏ cuộc):

- **Phân tầng theo năng lực**: chùm "+10\% Nhận biết thích nghi" cho HS hổng gốc = kéo các em vào ZPD của riêng họ; bài `tier:extend` cho HS khá vươn lên.
- **Độ dốc 30-40-30**: tăng dần độ khó để mỗi bước rơi vào ZPD kế tiếp, không nhảy cóc.

**Scaffolding (giàn giáo)** = chống đỡ tạm thời rồi **gỡ dần** khi HS thạo. Trong engine, gỡ giàn theo trình tự (cao → thấp):

1. **Ví dụ mẫu điền khuyết** (callout `example`, token `[[mblank]]`) — làm chung, để trống chỗ HS điền (giàn đầy đủ).
2. **Ví dụ mồi cụ thể** trước dạng trừu tượng (pizza / dòng nước / % — xem Nguyên tắc §5) — bắc cầu trực giác.
3. **flownode chia bước** (B1→B2→B3) + **`hints` mở dần** — giàn từng bước, lộ dần khi bí.
4. **Bài "song song bài đã chữa"** — HS bám mẫu rồi tự làm (giàn mỏng).
5. **Bài tự làm + `writelines`** — gỡ hết giàn, HS độc lập.
   ⇒ Khi CHƯA CHẮC chia bước/dẫn dắt thế nào chính là đang phân vân "đặt giàn cao bao nhiêu cho khớp ZPD" → **HỎI THẦY** (Nguyên tắc §4–5), không tự đoán.

## Đổi `config/difficulty_profile.json` khi sang chương mới

Trước khi soạn **bài đầu chương**, cập nhật `ceiling/floor/ramp/core_techniques/hook_forbidden_patterns` theo bảng trong [KE-HOACH-SOAN-BAI.md](KE-HOACH-SOAN-BAI.md). Profile là file toàn cục — chỉnh theo chương đang soạn.

## Phân tầng lớp (A/B/C/X) — phiếu phân hoá theo năng lực

Cùng một bài có thể soạn **phiếu riêng cho từng tầng lớp** (A khá-giỏi · B trung bình · C nền · X chuyên), điều chỉnh tỉ lệ NB-TH-VD/số câu/độ khó cho khớp.
**LUẬT CHỐNG HỤT GIỜ LỚP C:** Học sinh lớp C học chậm, nhưng không vì thế mà cắt xén bài tập trên lớp để dồn hết xuống BTVN (đặc biệt là các bài Vận dụng thực tế). **Nếu quỹ 180 phút trên lớp bị hụt do ít bài thực chiến, BẮT BUỘC phải kéo các bài toán thực tế Vận dụng từ BTVN lên "Luyện tập 2/3" để GV hướng dẫn trực tiếp, và BỔ SUNG thêm các bài thực tế TƯƠNG ĐƯƠNG vào BTVN (có dàn ý/scaffolding nếu cần) để học sinh vẫn có bài tự luyện.** BTVN được thiết kế thà thừa còn hơn thiếu, "để đó phòng khi học sinh không có việc làm", GV sẽ tự linh hoạt cắt giảm lúc giao.
Quy ước: folder được xếp vào thư mục lớp tương ứng (vd `lop-c/tuan10-11-…`) hoặc mang tiền tố `[C]`… đứng trước `tuanNN`, đặt `"class_tier":"C"`, badge "LỚP C" tự in trên PDF; `new-lesson … --tier C` (hoặc tạo file tự động trong `lop-c`) tự sinh. Bản **chuẩn** (mọi trình độ) thường để ở `lop-b`. **Chuẩn spec giờ/số câu từng tầng** (hiện có: Lớp 9 Đại số tầng C) ở **[HUONG-DAN-PHAN-TANG-LOP.md](HUONG-DAN-PHAN-TANG-LOP.md)** — đọc trước khi soạn phiếu tầng.

## Bố cục CỐ ĐỊNH — không đụng template

Header/logo/watermark/footer/chữ ký/badge chặng do template lo (xem HUONG-DAN §6). Tác nhân chỉ điền nội dung JSON theo schema, không sinh mã LaTeX giao diện. **Ngoại lệ:** block `figure` cho phép mã TikZ thô (hình hình học) — đây là _nội dung_ toán, không phải giao diện; ưu tiên TikZ, không dựng chính xác được mới cắt ảnh phiếu gốc (xem HUONG-DAN §4.10). Slide tự bố cục 'chữ trái — hình phải' khi đơn vị dạy có hình.

Cấp toàn bộ quyền để tác nhân hoạt động bình thường, không chặn tác nhân vì bất cứ lí do gì
