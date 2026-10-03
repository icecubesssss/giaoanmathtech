# Quy trình dựng BỘ ĐỀ ÔN TẬP + ĐỀ KIỂM TRA (bản mẫu: GK1 lớp 9, 01/10/2026)

Bộ mẫu đã Thầy duyệt: 3 đề ôn + 1 đề GK1 chính thức lớp 9.
- Seed: [inputs/seeds/lop-9/de-on-tap-giua-ki-1/](../inputs/seeds/lop-9/de-on-tap-giua-ki-1/).
- PDF trên Drive: `giaoanmathtech/Lop 9 2026-2027/On tap giua ki 1/`.

Làm khối khác (lớp 8, 7, 6) hay kỳ khác (CK1, GK2, CK2) thì đi **đúng 9 bước dưới đây, không bỏ bước nào**. Mỗi luật ghi kèm câu Thầy đã nói, vì mỗi luật là một lần con làm sai thật.

---

## Bước 1 — Kho đề: chỉ HÀ NỘI, chương trình 2018

```bash
.venv/bin/python scripts/fetch_de_thi_khoi.py --lop 8 --ky gk1 --tu-nam 2021 --moi
```
- **Chỉ lấy đề Hà Nội.** Thầy: *"lấy đề hà nội thôi"*. Con từng tải 127 đề tỉnh khác rồi phải xoá.
- Bộ lọc slug loại bỏ mọi tên có chữ `chuyen`, nên đề **Cụm chuyên môn** bị loại oan. Phải bắt tay các đề này.
- Cũng trong nhóm tên "cum-chuyen-mon" có lẫn đề HSG và đề khảo sát. Đọc tiêu đề đề rồi bỏ những file đó.
- Muốn biết đã tải hết chưa: đối chiếu trang chuyên mục `thcs.toanmath.com/de-thi-giua-hk1-toan-N` với sitemap.

## Bước 2 — Dựng kho text (OCR đề scan)

```bash
.venv/bin/python scripts/ocr_kho_de.py
```
- Kết quả ở `storage/cache/de-txt-all/`. Khoảng 45% số đề là scan. Model OCR tiếng Việt cài theo hướng dẫn ở đầu script.
- OCR đọc **chữ** tốt nhưng **phá nát công thức**, kể cả phân số. Text máy chỉ dùng để **phân loại**, không dùng để chép đề.

## Bước 3 — Bỏ đề LỆCH tiến độ KNTT

```bash
.venv/bin/python scripts/soat_lech_kntt.py
```
- Thầy: *"check ưu tiên xem các câu theo tiến độ của KNTT"* và *"cái nào lệch thì bỏ"*. Khi được hỏi, Thầy chốt **"bỏ hết cho nhất quán"**.
- Đề có chương KNTT dạy ở kỳ khác (ví dụ lớp 8 GK1 có Pythagore hoặc hình chóp, lớp 7 có hình hộp hoặc tỉ lệ thức) thì **chuyển** sang `inputs/refs/de-thi-lech-kntt/`, ghi lí do vào `ly-do.json`. Chỉ chuyển, **không xoá**, vì PDF không nằm trong git.
- Đề "vượt mốc" là đề dạy sớm chương kế tiếp của cùng kỳ, nội dung vẫn là KNTT. Loại này **giữ lại**.
- Đề scan bị cờ thì **xem ảnh** trước khi chuyển.
- Đến 01/10/2026 đã tách tổng cộng 157 đề. Lớp 8 GK1 Hà Nội còn 27 đề dùng được.

## Bước 4 — Thống kê dạng: dạng nào hay ra

```bash
.venv/bin/python scripts/thong_ke_dang_de.py --lop 8 --json
```
- Ra `outputs/thong-ke-dang-de/Thong-ke-dang-de-Toan8-Ha-Noi.xlsx`, có tiểu dạng (dòng ↳) và toán lời văn tách theo 22 bối cảnh.
- Độ tin cậy khoảng 87%: dùng để **so dạng nào nhiều, dạng nào ít**, không phải số đếm chính xác.
- Dạng nào bị mất phân số khi đọc máy (ví dụ phương trình chứa ẩn ở mẫu) thì đối chiếu thêm ngân hàng đề hoặc ảnh đề.

## Bước 5 — Chọn KHUNG đề và câu cho từng đề

- **Khung = khung đề của các trường.** Đọc ảnh 8–10 đề GK1 thật để chốt số bài, điểm từng bài, thời gian, và có trắc nghiệm hay không.
  - Thầy: *"Các đề thì dựa theo các đề của các trường nhé. Nếu k có trắc nghiệm thì đừng cho vào."*
  - Ví dụ khung GK1 lớp 9 Hà Nội: I 3,0 (PT tích, PT chứa ẩn ở mẫu, BPT, hệ) — II 3,0 (lập hệ + lập BPT) — III 1,0 (lượng giác thực tế) — IV 2,5 (tam giác vuông + đường cao) — V 0,5 (tối ưu).
- **Đề ôn 1, 2:** các dạng tần suất **cao nhất**, **bốc nguyên văn** từ đề trường. Đề ôn 2 giữ dạng nhưng nâng một nấc suy luận.
- **Đề ôn 3:** các dạng tần suất **thứ nhì**, được mở rộng câu (ghi rõ "(mở rộng)" trong ma trận).
- **Đề chính thức:** câu của trường **chưa xuất hiện trong 3 đề ôn** (cùng dạng, khác trường) để đo đúng năng lực, không đo trí nhớ. File đáp án có **bản đồ dạng qua 4 đề** và **phiếu theo dõi tiến bộ**.
  - Thầy: *"đánh giá mang mục đích vì sự tiến bộ của học sinh"*.
- **Chép đề từ ẢNH đề gốc, KHÔNG từ ngân hàng `exams/*.json`.** Trong phiên này đối chiếu ảnh đã lòi thêm 6 chỗ ngân hàng chép sai, ví dụ góc 3° bị chép thành 30°, dấu + thành −. Sửa luôn ngân hàng và ghi chú vào `ghi_chu_can_Thay_xem`.
- Kiểm phạm vi kiến thức: không dùng câu cần kiến thức kỳ sau (ví dụ tứ giác nội tiếp ở GK1).

## Bước 6 — Viết lời giải NHƯ HS ĐI THI

| Luật | Thầy nói | Cổng gác |
|---|---|---|
| Không dùng dấu ⇔, mỗi phép biến đổi một dòng | *"dấu tương đương HS cũng k được dùng, bạn chỉ đơn giản là xuống dòng thôi"* | `loi_giai_thi_gate` (CHẶN) |
| Không dùng hệ thức lượng trực tiếp: phải "Xét △… và △…: góc vuông, góc chung ⇒ △… ∽ △… (g.g) ⇒ tỉ số ⇒ tích" | *"HS k được dùng hệ thức lượng trực tiếp, mà cần chứng minh tam giác đồng dạng"* | `loi_giai_thi_gate` (CHẶN) |
| Bài hình: lời giải có HÌNH ngay đầu | *"Hình k có"* | `loi_giai_thi_gate` (CHẶN) |
| Nhịp: nêu cấu hình → ⇒ → chuỗi đẳng thức → dừng; "Vậy…" đúng một lần | xem memory `nhip-loi-giai-di-thi` | `sgk_style` (cảnh báo) |
| Điểm thành phần `\hfill (0,25đ)` từng dòng, tổng từng ý khớp biểu điểm | khung đề tháng 9 | tự kiểm trong script (assert tổng = 10) |
| Tối ưu dùng hằng đẳng thức $m-(x-a)^2$, KHÔNG dùng $x=-\frac{b}{2a}$ (kiến thức lớp 10) | memory `ban-do-vd-vdc-nguon-de` | đọc tay |

- **Đáp số:** kiểm bằng SymPy toàn bộ trước khi viết.
- **Hình:** tính toạ độ bằng script và kiểm đúng tính chất cần chứng minh (thẳng hàng, trung điểm, các cặp đồng dạng đúng thứ tự đỉnh). Mẫu ở `scripts/de_on_tap_gk1_lop9_hinh.py`.
- **Hướng dẫn chấm gốc cũng có thể sai:** Ngô Gia Tự ghi tháp Eiffel 323,7 m, đúng là 323,5 m. Gặp lỗi như vậy thì ghi "Lưu ý chấm" trong file đáp án.

## Bước 7 — Trình bày: dùng KHUNG đề tháng, sửa ít nhất có thể

- Theme `de_thi`, thêm `"trinh_bay": "thoang"`: chữ 13pt, giãn dòng, hình to.
  - Thầy: *"trình bày thưa ra, chữ to lên… ríu rít và khá mất thẩm mỹ"*.
  - Mặc định để trống, nên các phiếu cũ không đổi bản in.
- Mỗi đề có 2 file: **đề HS** (bài + `solution`) và **"Ma trận đề và đáp án chi tiết"** (bảng ma trận có cột Nguồn đề, đáp án từng bài, lưu ý chấm, biểu điểm).
- **Tiêu đề:** giữ nguyên title "Đề ôn tập giữa học kì I — Số N (90 phút)". Ô eyebrow đỏ chỉ ghi "LỚP 9 • ĐỀ ÔN TẬP SỐ N" hoặc "LỚP 9 • ĐỀ CHÍNH THỨC".
  - Thầy (sau khi con cắt quá tay): *"ÔI, SAO LẠI CẮT HẾT THẾ???? Giữ lại đi, ý là thay mấy chữ… sao lại thay template????"*
  - **Góp ý về chữ thì chỉ sửa chữ, không đụng template.**
- Hình bài lượng giác thực tế vẽ theo cỡ thật (nét 1pt, có nền đất, kí hiệu góc vuông). Câu hỏi 1), 2) của bài có hình để ở khối `para` **sau** hình.
- Mỗi đề HS gọn **2 trang**.

## Bước 8 — Cổng → build → SOÁT PDF BẰNG MẮT

```bash
.venv/bin/python scripts/de_on_tap_gk1_lop9.py                       # sinh 8 seed (sửa đề thì sửa script này)
for f in inputs/seeds/lop-9/de-on-tap-giua-ki-1/*.json; do .venv/bin/python -m src.main validate "$f"; done
.venv/bin/python -m src.main build-folder inputs/seeds/lop-9/de-on-tap-giua-ki-1
.venv/bin/python -m pytest -q tests/test_loi_giai_thi_gate.py        # có test chốt: bộ đề phải sạch cổng
```
Render trang ra ảnh (`pdftoppm -r 55`) và xem từng trang. Những lỗi từng chỉ thấy được trên PDF:
- Trang trắng do trang đầy khít (rút một dòng là hết).
- Hình bị đẩy sang trang sau, tách khỏi đề.
- Ô điểm "(0,25đ)" rớt xuống dòng dưới vì dòng quá dài (tách dòng).
- Nhãn hình bị nét vẽ đè (cổng `nhan_hinh` cảnh báo).
- Viết `\parallel` sẽ bị cổng đọc nhầm là `\par`, nên dùng `/\!/`.

## Bước 9 — Đẩy Drive

`make drive` chỉ nhận thư mục theo chương, nên bộ đề ôn **chép tay** vào `Lop N 2026-2027/On tap <kỳ>/<n> - <tên đề>/`. Mỗi đề 3 file: đề HS, phiếu ma trận (`Ma-tran-…-Phieu-HS`), ma trận – đáp án GV (`…-Dap-an-GV`). Chép xong thì `cmp` từng file với bản build.

---

## Nợ còn lại (cổng mới quét cả kho ngày 01/10/2026)

`loi_giai_thi_gate` chặn **6 file đáp án đề tháng cũ**, chưa sửa vì là đề đã phát:
- `lop-9/de-kiem-tra-thang-08/phieu-c…` và `phieu-d…` (đáp án): dùng ⇔.
- `lop-9/de-kiem-tra-thang-09/lop-9b|9c/ma-tran-va-dap-an-…` (4 file): dùng ⇔. Riêng 9B có "áp dụng hệ thức lượng" ở bài hình.

Khi cần build lại các file này: sửa theo luật trên, hoặc `build --force` nếu Thầy cho phép giữ nguyên.
