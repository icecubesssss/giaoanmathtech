# Quy trình soạn KHỐI 6, 7, 8 — lớp B và lớp C (đội agent)

> Dựng 15/10/2026. Mọi agent soạn/tra nguồn/kiểm duyệt khối 6-8 ĐỌC FILE NÀY TRƯỚC, rồi
> [AGENTS.md](../AGENTS.md), [HUONG-DAN-SOAN-PHIEU-B.md](../HUONG-DAN-SOAN-PHIEU-B.md) (tầng B),
> [HUONG-DAN-THUYET-MINH-LOP-C.md](../HUONG-DAN-THUYET-MINH-LOP-C.md) (tầng C).

## 1. Nguồn sự thật

| Cái gì | Ở đâu |
|---|---|
| Tiến độ lớp B (Thầy chốt 15/09/2026, tuần 1 = CN 21/06/2026) | `inputs/seeds/chuong-trinh-hoc-2026/Tien-do-lop-B-Toan-6-9-chot.xlsx` → `config/tien_do/B-lop-N.json` |
| Tiến độ lớp C (tuần 1 = 29/06/2026) | `…/Tien-do-hoc-lieu-C-Toan-6-9-chot.xlsx` → `config/tien_do/C-lop-N.json` |
| Việc cần soạn (tầng × lớp × môn × chương → các buổi + thư mục) | `config/tien_do/hang-doi.json` (sinh lại: `.venv/bin/python scripts/tien_do_2026.py`) |
| Chương có VD/VDC không, phân bổ 55, trần điểm | `config/ban_do_vd_vdc.json` |
| Khung giờ + tỉ lệ | `config/tier_spec.json` (lớp 6/7: ca 90′ = giảng 25 + luyện 55 + nghỉ 10, BTVN 40) |
| SGK/SGV KNTT (ảnh scan — đọc bằng mắt, pdftotext RỖNG) | `inputs/refs/sgk/lop-N/`, `inputs/refs/sgv/lop-N/` |
| Đề thật Hà Nội 4 kì (ngân hàng tầng 1, CHƯA người duyệt) | `inputs/refs/de-thi/lop-N/exams/*.json` + PDF gốc |
| Hồ sơ chương (Pha 1 dựng) | `inputs/refs/ho-so-chuong/lop-N/chuong-NN.{json,md}` |

Hai file tiến độ **lệch số tuần**: thư mục/slug `tuanNN` của tầng nào ghi theo file của tầng đó.

**Quyết định Thầy 15/10/2026:** mỗi tầng 1 file tiến độ · tầng **B soạn RIÊNG** theo luật 15-30-55 / 30-70
(không phải "B = C + VDC") · soạn **đủ cả năm theo chương** · phiếu 8B cũ (theo tiến độ cũ) tái dùng làm
nền, map sang buổi mới. **KT chương 45′ vẫn giữ cho cả B và C** (Thầy chốt 08/10 cho 8B, sau file B).

Chốt thêm 15/10/2026:
- Rate phút/câu lớp 6, 7: rate GỐC cho cả Đại lẫn Hình. Lớp 8 khung 25/55/40 (như 6, 7). Tầng C lớp 8 = 40-40-20.
- Bản đồ VD/VDC: lớp 7 ch.III CÓ VD (B dùng 15-30-55); lớp 8 ch.VIII không VD.
- **8B**: bảng map `config/tien_do/map-8b-cu.{json,md}`. Ch.I-III **dựng lại** theo quy trình phiếu B (phiếu cũ
  chỉ là nguồn đề — trống đáp án, writelines, Pythagore sớm). KT 45′ 8B chỉ ở ch.III (t10), IV (t13),
  VI (t29), VII (t33), IX (t33); bỏ I, II, V, VIII, X; đề KT gộp VII+VIII cũ → đề luyện CK2.
  Ca "gộp" (nhiều bài SGV/1 ca) **nén về đúng 1 ca**; phần dư → BTVN hoặc ca luyện dạng kế tiếp.
- **KT 45′ tầng B lớp 6, 7**: như 8B — chỉ chương có VD lớn và còn đất (đặt ở ca luyện dạng cuối chương);
  agent đề xuất trong TM để Thầy duyệt. Tầng C: ca "Luyện tập chương" = 45′ luyện + 45′ KT.
- **Lớp 6**: ch.I tầng B CÓ VDC phần luỹ thừa (tổng luỹ thừa cùng cơ số, tìm x ở số mũ); phần chứng minh
  chia hết để ch.II. "Số phần tử của tập hợp" đưa vào mức NB nhẹ (cả B, C; không tập con/giao).
  **Tìm x trình bày theo quan hệ thành phần phép tính** (không "chuyển vế") cho mọi phiếu lớp 6.
- Trưởng nhóm tự chốt theo luật sẵn có (Thầy sửa nếu khác ý):
  - Ca luyện dạng sau khi đã sang chương mới được dùng kiến thức đã học tới tuần đó.
  - Câu NB nhận dạng hình thức ("$-\frac13 \in \mathbb{Q}$") GIỮ cho lớp 6-8 (luật cấm 07/07 là của lớp 9).
  - Lớp 7: $|x|$ + luỹ thừa chẵn chuyển sang ch.II/ca VDC GK1 (|x| là Bài 7); tính hợp lí có luỹ thừa chỉ
    từ sau Bài 3; tìm x 1-2 bước theo quan hệ thành phần dùng được từ Bài 1+2, chuyển vế từ Bài 4;
    tổng dãy có quy luật (SGK không dạy) chỉ tầng B ở ca VDC GK1; % ngược ở tầng C thì chẻ thang.
  - Lớp 8: "Tìm x" dạy từ tuần 6 cả 2 tầng; tích nhân trực tiếp có dáng HĐT giữ ở ch.I (trừ $(a\pm b)^2$);
    KT 45′ tầng C theo khuôn GK1 trường thu nhỏ; "đa thức dư" không dạy (ngoài KNTT 8).
- Bank `inputs/refs/de-thi/lop-N/exams/`: nhãn `chuong` và id vị trí câu nhiều chỗ SAI — đừng lọc chỉ bằng
  `chuong`; thống kê máy thiếu dạng luỹ thừa. `build_ngan_hang_678.py` nay GIỮ trường tầng 2 khi dựng lại.

## 2. Cây thư mục

```
inputs/seeds/lop-N/<dai-so|hinh-hoc>/lop-<b|c>/chuong-NN-<slug ban_do>/
    thuyet-minh.json                       # TM CẤP CHƯƠNG (mọi phiếu của chương)
    phieu-K-tuanNN-<ten-bai>.json          # 1 phiếu / buổi (hoặc / 2 ca nếu so_ca 2)
    de-kiem-tra.json                       # ma trận KT 45′ (make check-de / make de)
    kiem-tra-chuong/                       # tờ đề HS + ma trận-đáp án (theme de_thi)
```
- Ca "Đại số (mượn ca Hình)" → nằm ở thư mục **dai-so**.
- Ôn hè / ôn-kiểm tra theo kì: `…/lop-x/on-he/`, `…/lop-x/on-tap-kiem-tra/<gk1|ck1|gk2|ck2>/` (Pha 4).
- Slug `phieu-a-`/`phieu-b-` CẤM (từ 12/09) — dùng `phieu-K-`.
- LUÔN sinh khung bằng `make spec FOLDER=… TIER=B|C` và `make new FOLDER=…` (grade/subject/tier/chuong
  suy từ đường dẫn; tự gõ JSON thì `grade` mặc định "lop-9" → chấm sai rate).

## 3. Pipeline một chương (mỗi tầng)

1. Đọc hồ sơ chương + các dòng của chương trong `config/tien_do/{B,C}-lop-N.json`
   (loại buổi: Bài mới / Bài mới (gộp) / Luyện dạng / Luyện tập chương; "Dạng thi trọng tâm" + điểm TB).
2. `make spec FOLDER=<thư mục chương> TIER=<B|C>` → điền TM: `thoiluong` (khớp số buổi của tiến độ),
   `kien_thuc_nen`, `lythuyet`, `vidu`, `dang_vd`, `loisai`, `kienthuc_nb`, `phieu[]` (mỗi buổi 1 phiếu:
   `code`, `so_ca`, `kiem_tra_phut`, `rows[]` có `dang`, `band`, `loai`, `decompose`, `vidu/onclass/btvn`,
   `source_refs`, `gian_giao`, `hinh_san`, `ve_hinh`, `quy_trinh`…).
3. `make check-tm SPEC=…/thuyet-minh.json` sạch → `make thuyetminh SPEC=…`.
4. Mỗi buổi: `make new FOLDER=…` → đổi tên `phieu-K-tuanNN-<bai>.json` → đổ đề →
   `make validate FILE=…` (bản cuối KHÔNG dùng FAST=1) → `make build-folder FOLDER=…`.
5. Buổi luyện tập chương: `kiem_tra_phut: 45` ở CẢ spec lẫn lesson; dòng thoiluong ghi
   "45 phút luyện tập $+$ 45 phút kiểm tra chương"; `de-kiem-tra.json` → `make check-de` → `make de`;
   `kiem-tra-chuong/` dựng tờ đề + ma trận-đáp án. Chương đơn giản không có ca luyện tập chương
   (C: 6-V,IX; 7-V,VIII,X; 8-V,VIII,X) → không KT riêng (khai `kiem_tra_gop` nếu gộp chương khác).
6. Tự soát: `pdftoppm -r 60 -png` vài trang soi mắt; `pdftotext | grep` từ cấm; `check_khoa_la`.

## 4. Khác biệt B / C

| | Tầng C | Tầng B |
|---|---|---|
| Tỉ lệ (phút trên lớp) | 40-40-20 (±10), không VDC, level ≤ 3 | theo chương: `co_vd` → 15-30-55 (55 chia VD/VDC theo `phan_bo_55`), không VD → 30-70 và **gộp 2 ca/1 phiếu** (`so_ca: 2`) |
| Đích | chắc 8 điểm; bỏ câu 0,5đ cuối đề + ý cuối hình; ý phụ trong bài biểu thức vẫn luyện | lớp 6: 10đ cả 4 kì; lớp 7-8: 10đ GK1, 9,5đ CK1/GK2/CK2 (bỏ ý cuối hình kì 9,5) |
| VDC | không có | chỉ ý CUỐI của bài (cổng `check_vdc_cuoi_bai`); lớp 6 chỉ câu cuối đề; KT tầng B ghi "VD" + "câu cuối đề 0,5đ" |
| Giàn giáo | dày (tới 8 ý con, điền khuyết) | `quy_trinh` cho mọi bài VD; ca ôn chương có dòng `viet_quy_trinh: true`; dạy lồng tư duy xuôi/ngược/phân tích đề |
| Mở bài | bài đời sống của HS | — |

Chung: 7 loại câu §4b (`loai` + `decompose`); ≤3 câu/loại; 2 giàn giáo bắt buộc (`ve-hinh`, `dien-khuyet`);
trộn 5 hình thức (TN, điền khuyết, Đ/S, nối, tự luận ngắn); câu thực tế 2-3 bước thay số = **TH**.

## 5. Luật nội dung (đã từng bị Thầy bác — đừng tái phạm)

- **KHÔNG bịa đề.** Mọi dòng `source_refs` trỏ SGK (`SGK 6T1 tr.x Bài y`), SGV, hoặc đề thật
  (`GK1 2025 <trường> Câu n`). Chỉ "NB lẻ LT" được tự viết. Câu bank `can_doc_anh: true` → mở PDF gốc,
  đọc bằng mắt, gõ lại LaTeX (pdftotext phá công thức, mất dấu + − =).
- **Đáp án phải đúng**: giải lại + SymPy (validate không FAST). Ưu tiên nghiệm đẹp.
- **Phạm vi theo tuần**: phiếu tuần N chỉ dùng kiến thức đã dạy tới tuần N theo file tiến độ của tầng
  (Thầy từng bác phiếu hình lớp 8 tuần 5 vì dùng Pythagore — bài đó dạy muộn hơn nhiều). TRA tiến độ, đừng đoán.
- **Suy luận chỉ từ giả thiết**: dò từng ⇒ về giả thiết; thiếu thì sửa ĐỀ, không lén thêm điều kiện.
- **Không văn nói, không tắt**; nhịp lời giải đi thi: nêu cấu hình → ⇒ → chuỗi đẳng thức → dừng.
  Mỗi bước 1 dòng (`[[br]]`), không ⇔, không "Do đó/Mặt khác".
- **Ví dụ** = bài điền khuyết `[[fill:]]` (≥2 ô, dòng "Vậy …" có ô), KHÔNG giống hệt bài tập
  (≥75% giống bị chặn), đặt ngay trước nhóm bài nó dẫn. TH có `hints` (trừ phiếu ôn GK/CK và đề KT).
- **Phiếu hình**: NB = bài trình bày hoàn chỉnh + khung bài giải điền khuyết; hình vẽ sẵn cho NB
  (`hinh_san` ×0,5 phút), mỗi buổi chỉ 1-2 bài hình HS tự vẽ (+5′); hình phải khớp kết luận (toạ độ TikZ đúng).
  Phiếu dạy chứng minh cấm bài thay số; lý thuyết chương hình cũng phải có hình.
- **Không chừa chỗ trống** (HS làm vào VỞ): không `writelines`, khung vẽ, `\vspace` chừa chỗ.
- Không unicode toán ngoài `$…$`; escape `\% \& \#`; không LaTeX trong `title`; cấm `\needspace`.
- Chưa chắc cách dạy → ghi vào "Câu hỏi cho Thầy" trong báo cáo, KHÔNG tự quyết.

## 6. Luật an toàn khi chạy song song

- CẤM `git checkout/restore/stash/reset` (seed thường CHƯA COMMIT — mất trắng). CẤM `make rebuild`,
  `make prune --delete`, `make drive`.
- Chỉ ghi trong thư mục được giao. KHÔNG sửa `config/`, `src/`, `templates/`, `difficulty_profile.json`,
  `docs/` — cần đổi thì ghi vào báo cáo cho trưởng nhóm.
- Khoá lạ trong JSON bị Pydantic NUỐT im lặng → chạy `check_khoa_la` (validate có in cảnh báo).
- Build từng file/thư mục của mình (`make build FILE=` / `make build-folder FOLDER=`), không build cả kho.
- Cổng báo oan đã biết: "Cho hình thang/chóp…" làm `figure_gate` kêu (viết "Xét…"); `nhan_hinh` hiểu
  nhầm `align=left`, `anchor=`.

## 7. Báo cáo cuối của mỗi agent (bắt buộc)

1. Danh sách file đã tạo/sửa. 2. Kết quả cổng (check-tm, validate, check-de, build) — dán dòng lỗi nếu còn.
3. Bảng buổi tiến độ ↔ phiếu (tuần, loại buổi, file). 4. Câu hỏi cho Thầy. 5. Việc cần trưởng nhóm làm
(sửa config/template…).
