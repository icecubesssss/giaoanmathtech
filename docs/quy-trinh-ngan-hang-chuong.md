# Bước 0 mỗi chương — NGÂN HÀNG BÀI trên Google Sheets (trước thuyết minh)

> **Cẩm nang 4 Template Sheets chuẩn chi tiết:** xem [`docs/quy-trinh-template-sheets.md`](quy-trinh-template-sheets.md) (đặc tả 47 cột, công thức, mã màu, quy trình 5 bước).

Thầy chốt 22/10/2026: thuyết minh và phiếu **chỉ bốc bài từ tab "Phân dạng" của chương** trên sheet dùng chung
`1ucQH5yw5bn3C1Bh_V4tAToa6NN5-F-nt8_2yxf2LNOM` (cả nhóm dùng — chỉ đụng tab của mình). Tab = ngân hàng đề:
MỌI bài thuộc chương lọc từ đề thi / SGK / tài liệu trong `inputs/`, chép **nguyên văn**.

Ví dụ dưới đây là chương V Hình 9 (`G=lop-9 S=hinh-hoc C=5`). Lệnh nằm trong `scripts/ngan_hang_sheet.py`
(Makefile: `bank-*`).

| # | Việc | Lệnh | Xong khi |
|---|---|---|---|
| 0 | Viết **khung chương** (phạm vi, dấu hiệu, nguồn, luật gán phiếu, số phiếu) | chép `config/khung-phan-dang/lop-9-hinh-hoc-chuong-05.json` | khung có đủ khoá |
| 1 | **Kiểm kê + chia việc**: liệt kê MỌI file phải mở, chia việc, sinh prompt agent | `make bank-giao G=… S=… C=…` | có `outputs/ngan-hang-sheet/<…>/viec/*.md` |
| 2 | **Quét**: mỗi việc một subagent (chạy song song), đọc ẢNH từng trang đề, ghi bản ghi + log | Agent tool, prompt = file `.md` của việc | đủ `ban-ghi/<việc>.json` + `log/<việc>.txt` |
| 3 | **Gộp + soát**: khoá/band/id/file, log phủ HẾT file kiểm kê, gán phiếu theo khung, nén, chia khối | `make bank-gop G=… S=… C=…` | 0 lỗi, có `day/khoi-*.json` + `day/find-replace.json` |
| 4 | **Ghi tab**: mỗi khối một `update_values` (song song bằng subagent, 1 khối/agent), rồi một `batchUpdate` = `find-replace.json`, rồi `sortRange` (C giảm, E tăng, K giảm) | connector Sheets | mọi khối báo success |
| 5 | **Đối chiếu**: `get_values` cả tab → JSON, so từng ô với bản gộp; rồi chụp snapshot | `make bank-doi-chieu RAW=… G=… S=… C=…` | 0 ô lệch, 0 mã `~XX~` sót; snapshot ghi xong |
| 6 | **Soát đủ bài** cho các phiếu của chương | `make du-bai GRADE=… SUBJECT=… CHUONG=… SO_PHIEU=…` | ✓ ĐỦ — THIẾU thì thêm nguồn vào khung, quay lại bước 1 |
| 6b | **Thống kê tỉ lệ dạng trong đề thật, tách riêng câu VD và câu VDC** (Thầy 05/11/2026: làm phân dạng chương thì phải có). Tính % đề theo từng kỳ (Kì I, Kì II, Vào 10). Dạng nào có nhiều cách giải thì đọc từng ý, tách theo **kỹ thuật**; nhãn gộp che mất (ch.V: "Tích 59%" nhưng khuôn hai cát tuyến bắc cầu chỉ 6%). Ghi lên tab "Thống kê dạng <chương>" trước khi dựng thuyết minh | thêm `dang_y`, `ky_thuat` vào khung chương rồi `python scripts/thong_ke_dang_vd.py <lớp> <môn> <chương> --json <file>` (script hiện gộp VD và VDC thành "VD+", tách riêng phải đếm thêm theo cột "Mức độ từng ý") | có bảng %, có kỹ thuật của dạng định làm đích |
| 7 | Dựng **thuyết minh** theo 4 bước A–D bên dưới (quy trình phân dạng 30/10/2026), `source_refs` = Mã câu (cột M); `thuyetminh_gate.check_nguon_sheet` chặn mã ngoài tab | xem mục dưới | `make check-tm` sạch |

Luật cứng:
- **Cấm lọc bằng từ khoá rồi bỏ qua file 0 hit** (22/10 làm vậy sót 12 bài/10 đề thi thử ở chương V). Bước 3 CHẶN nếu
  có file kiểm kê không xuất hiện trong log — file 0 bài vẫn phải có một dòng lý do.
- Không bịa, không sửa số liệu đề; lỗi in trong nguồn thì chép nguyên và ghi `note`.
- Thêm bài cho tab đã có: `bank-gop` tự bỏ mã đã có trên tab (theo snapshot) và đánh số dòng nối tiếp.
- Sửa tab bằng tay (Thầy/nhóm) xong phải chạy lại bước 5 (snapshot) trước khi dùng `du-bai`/thuyết minh.

Tối ưu đã rút ra (chương V 9C, 1083 bài):
- Nén cụm lặp thành `~XX~` giảm ~30–40% chữ phải gõ; khối ≤22 KB; **mỗi subagent ghi đúng MỘT khối** (rate limit
  làm agent chết giữa chừng — 1 khối/agent thì chỉ mất khối đó, chạy lại khối đó).
- Agent quét: ≤20 đề / 1 SGK / ≤4 tài liệu mỗi việc. Đề GK1 lớp 9 = ch.I–IV nên gần như 0 bài — vẫn phải mở.
- Đối chiếu bằng máy (bước 5) thay cho tin báo cáo của agent: agent gõ tay JSON vẫn có thể sai một ký tự.

---

## Sau khi tab đủ bài — TẠO PHIẾU THUYẾT MINH THEO PHIẾU PHÂN DẠNG (sếp chốt 30/10/2026)

Nguồn: tab **"Quy trình tạo phiếu TM theo PPD"** của sheet tiến độ nhóm
(`1ucQH5yw…2LNOM`, gid 2027469515), thống nhất sau họp 30/10/2026. Thay cho bước 7 cũ
("đủ bài ⇒ dựng thuyết minh") — giữa tab và thuyết minh nay có 3 bước:

| # | Việc (nguyên văn sheet) | Làm trong repo | Xong khi |
|---|---|---|---|
| A | **Làm phiếu phân dạng**: đọc trước phiếu phân dạng, phân loại câu | Thêm cột **N "Phân loại câu"** vào tab, mỗi bài/ý một nhãn: `NB kiến thức cũ` · `NB của phiếu` · `NB tách TH` · `TH của phiếu` · `TH ghép VD` (nhiều ý: `a) TH của phiếu · b) TH ghép VD`). Chụp ảnh các hình trong bài vào `inputs/refs/ngan-hang-sheet/<grade>/<subject>/chuong-NN/hinh/<Mã câu>.png` cho AI đọc. Sửa tab xong chạy lại bước 5 (snapshot) | mọi bài có nhãn; snapshot mới có trường `vai` |
| B | **Chạy thử phiếu thuyết minh ra cột đề xuất** | Dựng thuyết minh nháp theo thứ tự **VD → TH → NB** (sinh câu VD trước, rồi TH phục vụ VD, rồi NB). Mỗi câu TH đề xuất phải **tự sinh câu `NB tách TH` trỏ cùng bài gốc** (`source_refs` cùng mã). Rồi `make ppd-de-xuat RAW=<get_values tab> SPEC=<thuyet-minh.json>` ⇒ ghi `de-xuat-cot.json` vào cột **O "Đề xuất thuyết minh"** (đúng hàng theo Mã câu) | lệnh in 0 ✗ |
| C | **Đọc lại đề xuất, từ VD (VDC) → TH → NB; chọn câu không hay để bỏ** | Chưa có câu thay ⇒ nhờ AI đề xuất vài câu thay từ tab rồi chọn; chọn được thì thay trực tiếp trong spec và **ghi mã câu thay thế vào cột "Ghi chú" của tab**. Lớp TiH: chọn đa dạng hình thức (trắc nghiệm, điền khuyết, nối…) | người soạn duyệt xong cột O |
| D | **Chạy lại phiếu thuyết minh** | Sửa spec theo bước C, chạy lại `make ppd-de-xuat` (cột O cập nhật) rồi `make check-tm` | `check-tm` sạch |

Luật đo được — nằm trong `thuyetminh_gate.check_nb_theo_ppd`:
- **`NB tách TH` ≈ 30–40% số câu NB** của mỗi phiếu (đếm trên lớp + BTVN) — sheet ghi "khoảng" nên chỉ
  **cảnh báo**. (31/10/2026: phần lớn phiếu 9C cũ đang 45–85%.)
- **`NB tách TH` phải liên kết với một câu TH/VD của chính phiếu** (cùng bài gốc trong `source_refs`) — cảnh báo.
- **Lớp C phải có cả `NB tách TH` lẫn `NB kiến thức cũ`** — CHẶN với chương đã có tab phân dạng, cảnh báo
  với chương cũ. `NB kiến thức cũ` là nhãn `loai` thứ tám (thêm 30/10/2026); "NB của phiếu" = `NB lẻ LT` + `NB ghép bài`.

---

## QUY TRÌNH BÓC TÁCH HẠ BẬC (VD → TH → NB) TỪ KHÂU PHÂN DẠNG (Thầy chốt)

> **Mục đích:** Để HS lớp C (và các lớp đại trà) tiếp cận và làm được câu hỏi thi vào 10 (bài Vận dụng), tuyệt đối không để HS tự bơi với đề bài thô hay các bước nhảy cóc. Toàn bộ chuỗi bài tập phải được bóc tách có chủ đích theo mô hình leo dốc (Scaffolding Rails) đã thực hiện thành công ở **Chương V (Đường tròn)**.

### 1. Nguyên tắc "Quét cẩn thận — Giải chi tiết luôn — Tách bước sẵn"
1. **Dựa vào 1 bài VD gốc (bài đích đề thi thật):** Khi quét ngân hàng đề thi hoặc tài liệu, chọn bài toán Vận dụng điển hình của buổi học (ví dụ: bài hình chứng minh tiếp tuyến, chứng minh hệ thức tích $OA \cdot OH = R^2$, bài toán thực tế đo lường).
2. **Giải chi tiết luôn từ khâu phân dạng:** KHÔNG chỉ dừng lại ở việc chép đề thô vào tab. Người/Agent làm phân dạng phải đọc và viết **lời giải mẫu hoàn chỉnh từng bước** ngay tại bước này.
3. **Xem đáp án và bóc tách các tầng bậc suy luận:**
   - **Tách VD $\to$ TH:** Nhìn vào lời giải của câu VD, tách các mệnh đề/chứng minh trung gian thành các câu hỏi Thông hiểu độc lập:
     - *Ví dụ Chương V:* Từ bài chứng minh $DB$ là tiếp tuyến (VD) $\to$ Tách thành 2 bài/ý TH: (1) Chứng minh $OD$ là đường trung trực của $MB$; (2) Chứng minh $\triangle ODM = \triangle ODB$ (c.c.c) để suy ra góc vuông.
     - Từ bài chứng minh $OH \cdot OA = R^2$ (VD) $\to$ Tách thành ý TH: Chứng minh hệ thức lượng trong tam giác vuông hoặc cặp tam giác đồng dạng.
   - **Tách TH $\to$ NB:** Từ mỗi bài/ý TH, tiếp tục tách các bước đệm kỹ năng sơ cấp nhất thành các câu hỏi Nhận biết (làm trắc nghiệm hoặc điền khuyết trên hình vẽ sẵn):
     - *Ví dụ Chương V:* Chỉ ra tam giác vuông tại tiếp điểm ($MA \perp OA$), nhận diện cạnh huyền chung ($MO$), nhận diện bán kính bằng nhau ($OA = OB = R$), viết tỉ lệ thức từ tam giác đồng dạng.
4. **Phân loại nhãn chuẩn xác (§4b):** Gán đúng nhãn `loai`: `NB lẻ LT`, `NB tách TH`, `NB ghép bài`, `TH lẻ LT`, `TH ghép bài`, `TH tách VD`, `VD lẻ`.

### 2. Khi soạn phiếu chỉ việc "ghép nối" (Assembly Mode)
- Vì toàn bộ bài đích VD đã được giải chi tiết và chia nhỏ sẵn thành các mảnh ghép kỹ năng (NB, TH) ngay từ khâu phân dạng:
  - Khi soạn phiếu JSON, người soạn **chỉ việc lấy các mảnh ghép này ghép vào các chặng của phiếu**:
    - **Chặng 1 (Khám phá / NB lẻ):** Trắc nghiệm hoặc điền khuyết nhận diện tính chất, công thức từ các ý NB tách ra.
    - **Chặng 2 (Kiến thức trọng tâm):** Ví dụ mẫu có lời giải chuẩn của bài VD/TH.
    - **Chặng 3 (Luyện tập 1):** Bài tập ghép dẫn dắt điền khuyết (`[[blank:...]]`) trên hình in sẵn (`ve_tiep`) từ các bước đệm NB/TH đã tách.
    - **Chặng 4 (Luyện tập 2) & BTVN:** Bài toán trọn vẹn (chỉ có đề, bắt buộc tự vẽ hình `draw: true`), lúc này HS đã có đủ mẫu tư duy từ các bước đệm trước đó để tự giải độc lập.
- **Quy tắc sao & cấp độ bài toán (Level Consistency):**
  - Bài toán tổng thể ở cấp độ nào thì giữ nguyên sao cấp độ đó: Bài thuộc Dạng Thông hiểu thì để `level: 2` (2 sao ★★☆), kể cả khi các ý a), b) bên trong là các bước đệm nhận biết `[NB] ★` (như Bài 3 & BTVN 3 Phiếu 2 Chương V).
  - Không hạ sao của cả bài xuống 1 sao làm sai lệch cấu trúc phiếu.

---

## Bảng quy ước màu sắc chuẩn trên Google Sheets (Thầy chốt 30/10/2026)

Mọi tab **Phân dạng** và **Thuyết minh** khi dựng trên Google Sheets bắt buộc tuân theo bảng mã màu sau:

### 1. Trong tab Phân dạng (Ngân hàng câu hỏi)
- **Cam nhạt (`#FCE4D6`)**:
  - Cột **Mức độ**: Tô các câu mức **`VD`** và **`VDC`** (đỉnh của chặng leo dốc, giúp nhận diện ngay bài chốt).
  - Cột **Ưu tiên**: Tô câu **`Ưu tiên 4`** (Không bám SGK, câu bị gạt/loại bỏ, cảnh báo không chọn).
- **Vàng kem (`#FFF2CC`)**:
  - Cột **THẦY CHỌN**: Vùng dành riêng cho Thầy nhập liệu (`Bỏ`, hoặc gõ vị trí mới `P... · Trên lớp`).
- **Xanh lá nhạt (`#E2EFDA`)**:
  - Cột **CHỐT (tự tính)**: Máy tự tính kết quả, cấm gõ đè.
  - **Câu đang được chọn vào phiếu**: Cột Đề xuất & Chốt (hoặc cả dòng) của câu được phân bổ vào phiếu (`P... · Trên lớp` / `P... · Ví dụ`) mang màu xanh lá nhạt; câu dự phòng để nền trắng bình thường.

### 2. Trong tab Thuyết minh liên kết động (TM)
- **Cột Nhóm câu (Loại câu §4b)** — tô màu theo 4 chặng leo dốc (Scaffolding Rails):
  - **`VD`**: Cam nhạt (`#FCE4D6`)
  - **`TH ghép VD` / `TH tách VD`**: Vàng kem (`#FFF2CC`)
  - **`NB tách TH`**: Xanh lá nhạt (`#E2EFDA`)
  - **`NB kiến thức cũ`**: Tím nhạt Lavender (`#EDE7F6`)
- **Cột Mã câu đề xuất**:
  - **Vàng tươi (`#FFE699`)**: Tô các câu **mới soạn** (`MỚI·...`, `ch...-p...-lt...`) hoặc câu **tách ý con** (`·nb1`, `·th1`) để Thầy phân biệt với câu ngân hàng gốc và kiểm tra đề kỹ hơn.
- **Cột THẦY CHỌN & Mã thay thế**: Vàng kem (`#FFF2CC`).
- **Cột Chốt mã (tự tính)**: Xanh lá nhạt (`#E2EFDA`).
- **Dashboard Tổng hợp**: Xanh lá nhạt (`#E2EFDA`) và Xanh dương nhạt (`#DDEBF7`) cho các ô số liệu tự tính.

---

## Mẫu prompt agent quét (bước 2 — `bank-giao` tự điền các {…})

<!-- MAU-PROMPT-BEGIN -->
Bạn quét nguồn để dựng NGÂN HÀNG BÀI {ten_chuong} lớp {lop} (KNTT). Repo: `{root}` (đường dẫn file tính từ đó).
Phạm vi chương: {pham_vi}

Việc của bạn: **{viec}** — mở ĐỦ {so_file} file sau (không lọc trước bằng từ khoá, không bỏ file nào):
{ds_file}
{ghi_chu_viec}

Cách đọc
- `pdftotext -layout` hay hỏng công thức và nhiều đề là ảnh scan. Render trang: `pdftoppm -r 110 -png -f N -l N file.pdf {work}/pN`
  rồi ĐỌC ẢNH bằng Read tool. pdftotext chỉ để định vị trang; chép đề thì theo ảnh. Ảnh để trong `{work}`.
- Xem hết các trang ĐỀ của mỗi file (một file có thể chứa nhiều mã đề); bỏ trang đáp án/hướng dẫn chấm/ma trận.

Lấy bài nào
- Lấy nếu ÍT NHẤT MỘT ý thuộc chương: {dau_hieu}.
- Bài hình tổng hợp: lấy CẢ BÀI (phần dẫn + mọi ý) vào MỘT bản ghi; ý ngoài chương vẫn chép, ghi trong `note`
  (ngoài chương hay gặp: {ngoai_chuong}).
- KHÔNG lấy: {loai_khi}. Ca sát ranh giới mà vẫn lấy thì `note` bắt đầu bằng "BIÊN:".
- Bài thực tế thuộc chương: lấy. Câu trắc nghiệm: mỗi câu một bản ghi, chép cả phương án.
- Ví dụ trong sách: chỉ chép ĐỀ, `note` = "Ví dụ có lời giải mẫu". Lỗi in trong nguồn: chép nguyên, ghi `note`.

Khuôn bản ghi (mảng JSON, UTF-8)
```json
{{"id": "…", "nguon": "Đề giữa kì II THCS Chương Dương 2024-2025, Bài IV.2", "file": "<đường dẫn tương đối repo>",
 "uu": 1, "bai": "Bài 16 (tổng hợp)", "de": "nguyên văn; mỗi ý một dòng 'a) …'", "y": [["a","TH"],["b","VD"],["c","VDC"]],
 "dang": "mô tả dạng ngắn", "tt": false, "fmt": "Tự luận", "note": ""}}
```
- `id` DUY NHẤT: {quy_uoc_id}
- `uu`: 1 đề thi/kiểm tra/thi thử · 2 SGK · 3 tài liệu khác. `bai`: một trong {ds_bai}; thêm " (tổng hợp)" nếu bài hình ≥3 ý.
- `y`: [nhãn, mức] mỗi ý; câu một ý `[["", "TH"]]`. NB đọc/áp công thức 1 bước · TH vài bước quen thuộc · VD nhiều bước ·
  VDC ý cuối khó nhất (cực trị, cố định…). Đề có ma trận/barem ghi mức thì theo đề.
- `fmt`: Tự luận | Trắc nghiệm chọn đáp án | Trắc nghiệm đúng sai | Trả lời ngắn | Điền khuyết. `tt`: true nếu bài thực tế.
- Ký hiệu Unicode (∠ △ ⊥ ∥ π √ ° ² ·), góc viết ∠AOB.

Đầu ra (chỉ hai file, không đụng Google Sheets, không sửa file khác trong repo)
- `{out_json}` — mảng bản ghi; kiểm bằng `python3 -c "import json;json.load(open(PATH))"`.
- `{out_log}` — MỖI file được giao một dòng: `<tên file> | <số bản ghi> | <lý do nếu 0 / trang đề đã xem>`.
- Báo cáo: số file đã mở, số bản ghi, file 0 bài + lý do, chỗ đọc ảnh không chắc.
<!-- MAU-PROMPT-END -->
