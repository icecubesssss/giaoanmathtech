# KẾ HOẠCH SOẠN BÀI — Lớp 9 (xen kẽ Đại số + Hình học theo tuần)

> Bám [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md). Nguồn PDF đã quy hoạch sẵn trong từng thư mục tuần ở `inputs/seeds/lop-9/dai-so/` và `inputs/seeds/lop-9/hinh-hoc/`. Kho gốc hợp nhất: `inputs/seeds/lop-9/toan-9-cu/`.
>
> **Bắt đầu từ Tuần 4** (Đại tuần 4 đã xong). Làm **đúng thứ tự tuần**, mỗi tuần soạn cả phiếu Đại lẫn Hình.

## Quy trình mỗi phiếu (lặp lại)

```bash
python -m src.main new-lesson <folder-tuần>      # sinh khung 5 chặng (đặt slug + eyebrow "PHIẾU A/B" nếu tách)
# → điền nội dung BÁM PDF nguồn trong folder; KHÔNG bịa đề/đáp án
python -m src.main validate <file.json>          # gác cổng: schema/độ khó/gradient/linter + SymPy
python -m src.main approve <slug>                # Thầy duyệt
python -m src.main build <file.json>             # ra 3 PDF: handout / guide / slide
```

**Nguyên tắc:** không bịa đề · đáp án phải đúng (validate) · không in khi chưa approve · core `onclass` vừa một buổi, bài dư đẩy xuống `btvn`/`extend`.

## Đổi `config/difficulty_profile.json` khi sang chương mới

| Áp dụng từ | Đại số | Hình học |
|---|---|---|
| Tuần 4 | C1 PT & hệ PT bậc nhất | C4 Hệ thức lượng trong tam giác |
| Tuần 9 | C2 Bất đẳng thức / BPT | C5 Đường tròn |
| Tuần 16 | C3 Căn thức | *(C5 tiếp)* |
| Tuần 24 | C6 Thống kê – Xác suất | — |
| Tuần 27 | C7 Hàm số y=ax², PT bậc hai | C8 Đường tròn nội/ngoại tiếp |
| Tuần 31 | — | C9 Đa giác đều → C10 Hình trực quan |

→ Cập nhật trần (`ceiling`), sàn (`floor`), `ramp`, `core_techniques` **trước khi soạn bài đầu chương**.

---

## Checklist theo tuần

Ký hiệu: ☐ chưa làm · ✅ xong · ⏭ để sau (chưa có nguồn) · 🔶 track riêng (phiếu ôn/đề, không theo khung 5 chặng).
Mỗi ô tick gồm: `new-lesson → điền → validate → approve → build`.

### Tuần 4 — *(Đại đã xong)*
- ✅ **Đại** [tuan04-pt-quy-ve-pt-bac-nhat-mot-an](inputs/seeds/lop-9/dai-so/tuan04-pt-quy-ve-pt-bac-nhat-mot-an) — 2 phiếu (A: PT tích & ẩn ở mẫu · B: lập PT) — *đã build*
- ✅ **Hình** [tuan04-ti-so-luong-giac-goc-nhon](inputs/seeds/lop-9/hinh-hoc/tuan04-ti-so-luong-giac-goc-nhon) — 1 phiếu · *(đã set profile C4 · đã build)*

### Tuần 5
- ✅ **Đại** [tuan05-pt-va-he-pt-bac-nhat-hai-an](inputs/seeds/lop-9/dai-so/tuan05-pt-va-he-pt-bac-nhat-hai-an) — 1 phiếu (PT & hệ PT bậc nhất 2 ẩn) — *đã build*
- ✅ **Hình** [tuan05-he-thuc-canh-goc-tam-giac-vuong](inputs/seeds/lop-9/hinh-hoc/tuan05-he-thuc-canh-goc-tam-giac-vuong) — 1 phiếu — *đã build*

### Tuần 6–7
- ✅ **Đại** [tuan06-07-giai-he-pt-bac-nhat-hai-an](inputs/seeds/lop-9/dai-so/tuan06-07-giai-he-pt-bac-nhat-hai-an) — **2 phiếu** (A: giải hệ thế/cộng đại số · B: giải toán bằng lập hệ) — *đã build*
- ✅ **Hình T6** [tuan06-ung-dung-ti-so-luong-giac](inputs/seeds/lop-9/hinh-hoc/tuan06-ung-dung-ti-so-luong-giac) — 1 phiếu — *đã build*
- ⏭ **Hình T7** [tuan07-on-tap-he-thuc-luong-tam-giac-vuong](inputs/seeds/lop-9/hinh-hoc/tuan07-on-tap-he-thuc-luong-tam-giac-vuong) — *trống, bổ sung nguồn sau*

### Tuần 9
- ☐ **Đại** [tuan09-bat-dang-thuc](inputs/seeds/lop-9/dai-so/tuan09-bat-dang-thuc) — **đã có 3 JSON draft** → chỉ cần `validate → approve → build` (kiểm tra đủ 5 chặng) · *(mở chương: set profile C2)*
- ☐ **Hình** [tuan09-10-duong-tron-vi-tri-tuong-doi-hai-duong-tron](inputs/seeds/lop-9/hinh-hoc/tuan09-10-duong-tron-vi-tri-tuong-doi-hai-duong-tron) — 1–2 phiếu (Đường tròn · vị trí 2 đường tròn) · *(mở chương: set profile C5)*

### Tuần 10–11
- ✅ **Đại** [tuan10-11-bat-phuong-trinh-bac-nhat-mot-an](inputs/seeds/lop-9/dai-so/tuan10-11-bat-phuong-trinh-bac-nhat-mot-an) — **4 phiếu** phủ kín nguồn (A: nhận biết+giải BPT bậc nhất · B: phân thức/khai triển/rút gọn · C: tích/thương+dạng đặc biệt HSG · D: lập BPT) — *validate sạch + đã build, chờ Thầy duyệt* · *(mở chương: set profile C2 BPT)*
- ☐ **Hình** [tuan11-12-vi-tri-tuong-doi-duong-thang-duong-tron](inputs/seeds/lop-9/hinh-hoc/tuan11-12-vi-tri-tuong-doi-duong-thang-duong-tron) — đã chốt 2 phiếu A/B (xác định vị trí · tính độ dài+tiếp tuyến), *tạm hoãn theo yêu cầu Thầy* · *(mở chương: set profile C5)*

### Tuần 12
- ⏭ **Đại** [tuan12-on-tap-bdt-bpt](inputs/seeds/lop-9/dai-so/tuan12-on-tap-bdt-bpt) — *trống, bổ sung nguồn sau*
- *(Hình: tuần 11–12 đã tính ở trên)*

### Tuần 13–14
- 🔶 **Đại** [tuan13-14-on-tap-giua-hk1](inputs/seeds/lop-9/dai-so/tuan13-14-on-tap-giua-hk1) — phiếu ôn GK1 từ 17 đề (track riêng)
- ☐ **Hình** [tuan13-14-tiep-tuyen-duong-tron](inputs/seeds/lop-9/hinh-hoc/tuan13-14-tiep-tuyen-duong-tron) — 1 phiếu

### Tuần 15
- ☐ **Hình** [tuan15-goc-o-tam-goc-noi-tiep](inputs/seeds/lop-9/hinh-hoc/tuan15-goc-o-tam-goc-noi-tiep) — 1 phiếu
- *(Đại: tuần 15 là kiểm tra/đề tham khảo theo tiến độ)*

### Tuần 16
- ☐ **Đại** [tuan16-can-bac-hai-can-bac-ba](inputs/seeds/lop-9/dai-so/tuan16-can-bac-hai-can-bac-ba) — 1–2 phiếu (căn bậc hai + căn bậc ba) · *(mở chương: set profile C3)*
- 🔶 **Hình** [tuan16-on-tap-gk1](inputs/seeds/lop-9/hinh-hoc/tuan16-on-tap-gk1) — phiếu ôn GK1 (track riêng, dùng chung bộ đề với Đại T13–14)

### Tuần 17
- ☐ **Đại** [tuan17-lien-he-nhan-chia-khai-phuong](inputs/seeds/lop-9/dai-so/tuan17-lien-he-nhan-chia-khai-phuong) — 1 phiếu
- *(Hình: kiểm tra GK1 theo tiến độ)*

### Tuần 18
- ☐ **Đại** [tuan18-bien-doi-bieu-thuc-chua-can](inputs/seeds/lop-9/dai-so/tuan18-bien-doi-bieu-thuc-chua-can) — 1 phiếu

### Tuần 19
- ☐ **Đại** [tuan19-rut-gon-bieu-thuc-chua-can](inputs/seeds/lop-9/dai-so/tuan19-rut-gon-bieu-thuc-chua-can) — 1 phiếu (bám "câu 2 đề vào 10")
- ☐ **Hình** [tuan19-goc-o-tam-goc-noi-tiep-tt](inputs/seeds/lop-9/hinh-hoc/tuan19-goc-o-tam-goc-noi-tiep-tt) — 1 phiếu (tiếp T15)

### Tuần 20–21
- ☐ **Đại T20** [tuan20-luyen-tap-rut-gon-va-cau-hoi-phu](inputs/seeds/lop-9/dai-so/tuan20-luyen-tap-rut-gon-va-cau-hoi-phu) — 1 phiếu luyện tập (gộp 4a giải PT · 4b GTLN/GTNN · 4c P nguyên), trần cao
- ☐ **Hình** [tuan20-21-do-dai-cung-dien-tich-quat-tron](inputs/seeds/lop-9/hinh-hoc/tuan20-21-do-dai-cung-dien-tich-quat-tron) — 1 phiếu
- 🔶 **Đại T21** [tuan21-on-tap-hk1](inputs/seeds/lop-9/dai-so/tuan21-on-tap-hk1) — phiếu ôn HK1 từ 21 đề (track riêng)

### Tuần 22–23
- ☐ **Hình** [tuan22-23-on-tap-chuong-duong-tron](inputs/seeds/lop-9/hinh-hoc/tuan22-23-on-tap-chuong-duong-tron) — phiếu ôn tập chương đường tròn
- *(Đại: kiểm tra HK1 theo tiến độ)*

### Tuần 24
- ☐ **Đại (a)** [tuan24-mo-ta-bieu-dien-du-lieu](inputs/seeds/lop-9/dai-so/tuan24-mo-ta-bieu-dien-du-lieu) — 1 phiếu · *(mở chương: set profile C6)*
- ☐ **Đại (b)** [tuan24-tan-so-tan-so-tuong-doi](inputs/seeds/lop-9/dai-so/tuan24-tan-so-tan-so-tuong-doi) — 1 phiếu
- 🔶 **Hình** [tuan24-on-tap-hk1](inputs/seeds/lop-9/hinh-hoc/tuan24-on-tap-hk1) — phiếu ôn HK1 (track riêng)

### Tuần 25–26
- ☐ **Đại (a)** [tuan25-tan-so-ghep-nhom](inputs/seeds/lop-9/dai-so/tuan25-tan-so-ghep-nhom) — 1 phiếu
- ☐ **Đại (b)** [tuan25-26-phep-thu-ngau-nhien-xac-suat](inputs/seeds/lop-9/dai-so/tuan25-26-phep-thu-ngau-nhien-xac-suat) — 1 phiếu

### Tuần 27
- ☐ **Đại** [tuan27-ham-so-y-ax2](inputs/seeds/lop-9/dai-so/tuan27-ham-so-y-ax2) — 1 phiếu · *(mở chương: set profile C7)*
- ☐ **Hình** [tuan27-duong-tron-ngoai-tiep-noi-tiep-tam-giac](inputs/seeds/lop-9/hinh-hoc/tuan27-duong-tron-ngoai-tiep-noi-tiep-tam-giac) — 1 phiếu · *(mở chương: set profile C8)*

### Tuần 28–30
- ☐ **Đại T28** [tuan28-phuong-trinh-bac-hai-mot-an](inputs/seeds/lop-9/dai-so/tuan28-phuong-trinh-bac-hai-mot-an) — 1 phiếu
- ☐ **Đại T29–30** [tuan29-30-dinh-li-viet-va-ung-dung](inputs/seeds/lop-9/dai-so/tuan29-30-dinh-li-viet-va-ung-dung) — 1–2 phiếu (B nặng đề vào 10)
- ☐ **Hình** [tuan28-30-tu-giac-noi-tiep](inputs/seeds/lop-9/hinh-hoc/tuan28-30-tu-giac-noi-tiep) — 1 phiếu

### Tuần 31
- ☐ **Đại** [tuan31-giai-toan-bang-lap-phuong-trinh](inputs/seeds/lop-9/dai-so/tuan31-giai-toan-bang-lap-phuong-trinh) — 1 phiếu (toán đố → dùng block `table`)
- ☐ **Hình** [tuan31-da-giac-deu](inputs/seeds/lop-9/hinh-hoc/tuan31-da-giac-deu) — 1 phiếu · *(mở chương: set profile C9)*

### Tuần 32–33
- ☐ **Hình T32** [tuan32-hinh-tru-non-cau](inputs/seeds/lop-9/hinh-hoc/tuan32-hinh-tru-non-cau) — 1 phiếu · *(mở chương: set profile C10)*
- ☐ **Hình T33** [tuan33-on-tap-hhkg](inputs/seeds/lop-9/hinh-hoc/tuan33-on-tap-hhkg) — 1 phiếu ôn tập

---

## Việc còn treo (mục c — bạn xử lý sau)
- ⏭ [dai-so/tuan12-on-tap-bdt-bpt](inputs/seeds/lop-9/dai-so/tuan12-on-tap-bdt-bpt) — chưa có nguồn ôn tập chương BĐT/BPT phù hợp.
- ⏭ [hinh-hoc/tuan07-on-tap-he-thuc-luong-tam-giac-vuong](inputs/seeds/lop-9/hinh-hoc/tuan07-on-tap-he-thuc-luong-tam-giac-vuong) — chương 4 không có file ôn tập chương.
