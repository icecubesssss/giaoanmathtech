# MathTech Worksheet Factory

Hệ thống tự sinh **phiếu học tập + slide + sổ tay GV** cho Toán lớp 9 ôn thi vào 10.
Bản đồ codebase (module + symbol, tự sinh bằng `make map`): [PROJECT_MAP.md](PROJECT_MAP.md). Cách dùng nhanh ở dưới.

## Chuẩn bị (1 lần)

```bash
source .venv/bin/activate          # môi trường Python
# Tectonic ở ~/bin/tectonic, font nhúng trong assets/fonts/
```

## Vòng lặp soạn cả năm

```bash
# 1. Xem còn thiếu gì
python -m src.main progress --todo               # chỉ tuần CHƯA build xong
python -m src.main progress --grade lop-9         # lọc theo lớp
python -m src.main progress --subject dai-so     # lọc theo môn

# 2. Bắt đầu một bài: thả PDF nguồn vào folder tuần rồi sinh khung
#    inputs/seeds/<lop>/<mon>/tuanNN-<chu-de>/
python -m src.main new-lesson inputs/seeds/lop-9/dai-so/tuan10-11-bat-phuong-trinh-bac-nhat-mot-an

# 3. Đổ đề vào các block TODO  ← bước này nhờ Claude làm
#    (mở chat, chỉ folder + PDF nguồn; Claude điền đúng convention)
#    Luật soạn bài đầy đủ: HUONG-DAN-SOAN-BAI.md

# 4. Kiểm + duyệt + in 3 bản
python -m src.main validate  <file.json>
python -m src.main approve   <slug>
python -m src.main build     <file.json>
#    → outputs/<lop>/<mon>/<tuan>/<slug>/{handout,guide,slide}.pdf
```

## Bảng lệnh

| Lệnh | Việc |
|------|------|
| `progress [--grade X] [--subject X] [--todo]` | Quét sống cây tuần: có PDF nguồn? có JSON? đã build chưa |
| `new-lesson <folder> [--slug --title --force]` | Sinh khung JSON 5 chặng/4 tầng đầy block TODO |
| `curriculum-sync` | Sinh/cập nhật `config/curriculum.json` (giữ deadline/giờ đã điền) |
| `validate <file.json>` | Trọng tài S2: sanitizer + schema + difficulty_gate + **gradient_gate** (độ dốc mở rộng) + linter (gồm cảnh báo `&`/`%`/`#` chưa escape) |
| `validate-all [--grade X] [--subject X]` | Chạy `validate` trên **toàn bộ** lesson JSON — gác cổng cả kho trước khi build/commit |
| `approve <slug>` | Mở khoá compile |
| `build <file.json>` | Render + compile cả 3 bản PDF |
| `build-handout / build-guide / build-slide <file.json>` | In riêng từng bản |
| `rebuild [--grade X] [--subject X] [--all]` | Build **lại hàng loạt** mọi bài đã có output — lan thay đổi `design_tokens`/template ra mọi phiếu (dùng sau khi sửa màu/font/branding) |
| `new-summary <folder> [--slug --title --force]` | Sinh khung **phiếu tổng kết chương** (tự liệt kê phiếu thành viên trong folder) |
| `build-summary <file.json>` | Render phiếu tổng kết chương 1 trang: bản HS (sơ đồ trống) + bản GV (có đáp án) |
| `status` | Trạng thái mọi bài trong `run_state.json` |

## Dấu ấn giáo viên (luôn có ở mọi phiếu)

Mọi bản in **bắt buộc** mang chữ ký **Thầy Thái MathTech** + SĐT **0386969199**. Đây là
phần cố định của template, nên **mọi `build` về sau tự động có** — không phải thêm tay:

- Phiếu HS / Sổ tay GV / Tổng kết → ở **footer mọi trang**, ngay sau dòng Website:
  `Biên soạn: Thầy Thái MathTech -- ĐT 0386969199`.
- Slide → **slide bìa** ghi `Biên soạn: Thầy Thái MathTech • 0386969199`; **footline mọi slide**
  ghi `• Thầy Thái MathTech` (footline chật nên không kèm SĐT).

Nguồn duy nhất ở các template: `base_handout/base_summary/base_guide.tex.j2` (footer),
`base_slide.tex.j2` (bìa), `preamble/_beamer.tex.j2` (footline). **Sửa SĐT/tên thì sửa ở
cả 5 chỗ này** rồi `build` lại. **Đừng gỡ** chữ ký khi chỉnh template hay khi chạy `evolve`.

## Cấu trúc 1 phiếu — 5 chặng map 4 tầng

1. **review** — Khám phá / KTBC + 1 worked example (có nhịp cầu, không nhảy gấp)
2. **concept** — Khái niệm + **Ví dụ mẫu**, kèm ghi chú *"Đích đến thi vào 10"*
3. **practice1** — Bài tập trên lớp (nền) · `tier: onclass`
4. **practice2** — Bài tập trên lớp (vận dụng, **chạm trần** độ khó vào 10) · `tier: onclass`
5. **reflection** — chặng 5 trên phiếu chỉ là **"Tổng kết"**: 1–2 câu chốt + **Sơ đồ tư duy điền khuyết** (block `mindmap`, thay ô tự chấm). Đặt summary + mindmap Ở ĐẦU danh sách blocks.

**BTVN và Bài tập mở rộng KHÔNG nằm trong hộp chặng 5** — renderer (`split_reflection`) tự tách chúng thành **2 mục riêng có banner** ("BÀI TẬP VỀ NHÀ", "BÀI TẬP MỞ RỘNG"), đồng bộ trên handout + guide + slide. Phân mục **theo `tier`** của block `problem`: `btvn` → mục về nhà; `extend` → mục mở rộng (câu `para` "nhịp cầu" đặt ngay trước cụm extend sẽ thuộc mục mở rộng). KHÔNG cần tự gõ tiêu đề mục — template tự in banner.

**Tầng Mở rộng phải là một THANG, không phải 1 bài dốc đứng:** ≥2 bài, mỗi bài thêm đúng *một* bước kỹ thuật; có **1 nhịp cầu** (block `para`) trước cụm extend chỉ rõ kỹ thuật mới; mỗi bài extend kèm `hints` = 1–2 gợi ý *"mở khi bí"* (in trên phiếu HS, **không** lộ lời giải — lời giải vẫn ở `solution`). Lệnh `validate` chạy `gradient_gate` cảnh báo nếu thiếu thang/nhịp cầu/hints (ngưỡng trong `ramp` của `config/difficulty_profile.json`).

Quy ước trình bày: tách ý/bước bằng `[[br]]` — **kể cả trong `solution`** (mỗi bài/mỗi đáp án một dòng, đừng nhồi `;` vào một dòng); chỗ HS điền dùng `[[blank:3cm]]` / `[[mblank:0.8cm]]`, nhãn nút sơ đồ tư duy cũng dùng `[[blank:W]]`; chú thích GV **chỉ** đặt trong `solution`/`teacher_note`, không lọt vào block HS; đánh số bài **liền mạch** cả phiếu.

Bẫy LaTeX (sanitizer KHÔNG bắt): `&` trong `title`/`eyebrow` phải viết `\&`; **không** dùng mũi tên/ký hiệu unicode thô (`→`, `≥`…) trong text — dùng `$\to$`, `$\ge$`; `^` `\,` `\;` chỉ đặt trong `$...$`.

## Phiếu tổng kết (1 trang, sơ đồ tư duy to)

Hai cấp, **dùng chung lệnh** `new-summary` (1 folder = tổng kết bài; nhiều folder = tổng kết chương):

**(a) Tổng kết BÀI/tuần** — gom các phiếu A/B của một tuần:

```bash
python -m src.main new-summary inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc
#   → tong-ket-<chủ-đề>.json NGAY TRONG folder tuần
python -m src.main build-summary inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc/tong-ket-bat-dang-thuc.json
#   → outputs/.../tong-ket-bat-dang-thuc/tongket-hs.pdf + tongket-gv.pdf
```

**(b) Tổng kết CHƯƠNG** — **1 tuần = 1 bài**, **1 CHƯƠNG = nhiều tuần** (xem cột *"Nội dung đưa cho HS"*
trong `inputs/seeds/lop-9/chuong-trinh-hoc/`, vd chương BĐT–BPT trải tuần 9–12). Làm **sau khi xong hết các tuần của chương**:

```bash
# Truyền TẤT CẢ folder tuần của chương:
python -m src.main new-summary \
  inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc \
  inputs/seeds/lop-9/dai-so/tuan10-11-bat-phuong-trinh-bac-nhat-mot-an \
  inputs/seeds/lop-9/dai-so/tuan12-on-tap-bdt-bpt \
  --slug tong-ket-bdt-bpt --title "Bất đẳng thức & Bất phương trình"
#   → inputs/seeds/lop-9/dai-so/tong-ket-bdt-bpt.json  (đặt ở CẤP MÔN, gom phiếu mọi tuần)
#   Điền sơ đồ (nút trống [[blank:W]]), rồi:
python -m src.main build-summary inputs/seeds/lop-9/dai-so/tong-ket-bdt-bpt.json
#   → outputs/lop-9/dai-so/<slug>/tongket-hs.pdf (sơ đồ trống) + tongket-gv.pdf (kèm đáp án)
```

File tổng kết (`mindmap` ở cấp cao nhất, không có `stages`) được `progress` tự bỏ qua khi đếm bài.

## Kế hoạch (manifest)

`config/curriculum.json` sinh tự động từ cây tuần. Mở file điền tay `deadline`,
`duration_hours`, `target_lessons`, `note` cho từng tuần — chạy `curriculum-sync`
lại **không** ghi đè những gì đã điền. `progress` sẽ hiện ⏰ deadline kèm theo.
