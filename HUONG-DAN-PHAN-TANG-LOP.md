# Phân tầng lớp & chuẩn spec phiếu theo năng lực HS

> Nguồn sự thật cho việc soạn phiếu **phân hoá theo tầng lớp**. Bổ trợ [AGENTS.md](AGENTS.md) (nguồn gốc quy trình) và [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md) (luật soạn chi tiết).

Trung tâm chia HS theo năng lực thành các **tầng lớp**. Mỗi tầng nhận **cùng một bài** nhưng phiếu được **điều chỉnh thông số** (độ khó, tỉ lệ NB-TH-VD, số câu) cho khớp năng lực.

| Tầng | Đối tượng | Yêu cầu cốt lõi | Tỉ lệ NB-TH-VD |
|---|---|---|---|
| **A** | Khá – giỏi | *(chuẩn hoá sau)* | *(sau)* |
| **B** | Trung bình – khá | Nắm chắc NB, TH, rèn luyện tư duy VD và cọ xát 1 phần VDC. **Đích: trần 10,0 kỳ I · 9,5 kỳ II** | **theo CHƯƠNG** (xem §2): chương có VD **15 – 30 – 55 (VD+VDC)**, khối 55 chia lại theo **tần suất VDC**; chương không VD **30 – 70**, gộp 2 phiếu. Quy trình: [HUONG-DAN-SOAN-PHIEU-B.md](HUONG-DAN-SOAN-PHIEU-B.md) |
| **C** | Nền (yếu – trung bình) | Thạo **100% Nhận biết + Thông hiểu**, làm được **1 phần Vận dụng** | **40 – 40 – 20** |
| **X** | HS chuyên | *(chuẩn hoá sau)* | *(sau)* |

> Hiện đã chuẩn hoá **tầng C cho Lớp 9 – Đại số**. Các tầng A/B/X và môn/khối khác sẽ chuẩn hoá khi soạn tới.

---

## 1. Quy ước đặt tên & dấu hiệu (áp dụng MỌI tầng)

- **Folder phiếu theo tầng:** thêm tiền tố `[A]`/`[B]`/`[C]`/`[X]` **đứng TRƯỚC** `tuanNN`, ví dụ:
  `inputs/seeds/lop-9/dai-so/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an/`.
  Tiền tố đặt trước để **không nhầm với hệ đếm tuần** (`tuanNN-`). Tool đã hiểu tiền tố này (`new-lesson`, `build`, `progress`… vẫn đọc đúng số tuần/chủ đề).
- **Phiếu bản chuẩn** (mọi trình độ) **không** mang tiền tố — giữ nguyên `tuanNN-<chủ đề>/`.
- **Trong folder tầng** vẫn theo quy ước `phieu-a-/phieu-b-/…` (HUONG-DAN §7).
- **Trường máy-đọc:** đặt `"class_tier": "C"` trong JSON phiếu. `new-lesson` tự suy từ tiền tố folder (hoặc cờ `--tier C`).
- **Hiển thị trên PDF:** badge **"LỚP C"** (hộp đậm) tự in ở header cả 3 bản (handout/guide/slide) khi có `class_tier` — KHÔNG nhồi "LỚP C" vào `eyebrow` nữa (tránh lặp). `eyebrow` giữ phần chủ đề như thường (vd `ĐẠI SỐ — PHIẾU A: …`). Cầm tờ in ra biết ngay tờ nào cho lớp nào.

---

## 2. Chuẩn SPEC giờ — **Lớp 9 · Đại số · tầng C**

> **MÁY-ĐỌC (2026-06-21):** mọi con số dưới đây nay nằm trong **[config/tier_spec.json](config/tier_spec.json)** (phút/câu, ngân sách, tỉ lệ theo tầng). `duration_gate` + `new-thuyetminh` + `spec_gate` đọc chung từ đó — sửa số ở 1 chỗ. Đã chốt: **C 40-40-20-0 · A 20-35-30-15**; **B theo chương** (xem khung dưới); **X** (chuyên) chưa chốt tỉ lệ. **VDC = band 4** (phút/câu 12/18/15,6). Bài giàu (VD/VDC) **cắt bước scaffold-decompose** → sinh câu NB/TH *từ chính bài* (vì bank đề hầu như không có câu NB rời — xem `make coverage`).

> **TẦNG B ĐỔI LUẬT (Thầy chốt 2026-08-30) — tỉ lệ chọn THEO CHƯƠNG, không còn 30-40-20-10:**
> - Chương **KHÔNG** có bài VD/VDC trong đề thi → **NB 30% · TH 70%**; phần NB gồm **~5 dạng, mỗi dạng 2 câu** (≈10 câu — đây là ràng buộc **cứng**, 30% chỉ để tham chiếu). **GỘP 2 PHIẾU THÀNH 1** (`so_ca: 2`) — buổi 1 gánh 15% NB + 35% TH, buổi 2 gánh 15% NB + 35% TH (anh An chốt 30/08).
> - Chương **CÓ** VD/VDC trong đề thi → **NB 15% · TH 30% · VD+VDC 55%** (VD và VDC **gộp chung**, cổng soi tổng).
> - **CẬP NHẬT 04/09/2026 — khối 55% CHIA THEO TẦN SUẤT VDC của chương** (Thầy: *"câu VDC có tần suất nhiều trong đề thi thì ưu tiên cho nhiều hơn"*): `p ≥ 0,50` → **VD 35 · VDC 20**; `0,20 ≤ p < 0,50` → **43 · 12**; `0 < p < 0,20` → **50 · 5** (5% của 120′ là 6′, chưa đủ một câu VDC 18′ ⇒ dồn VDC vào **phiếu ôn tập chương**); `p = 0` → **55 · 0**. Tổng vẫn luôn là 55. Số ở `vdc.phan_bo_55` trong bản đồ, đo bằng `scripts/tan_suat_vdc.py`.
> - **CHỈ Ý CUỐI MỚI LÀ VDC:** một bài nhiều ý chỉ được MỘT thẻ `[VDC]`, ở ý cuối (cổng `duration_gate.check_vdc_cuoi_bai`, áp mọi tầng).
> - **TRẦN ĐIỂM là đích của phiếu:** GK1/CK1 → **10,0** (dạy hết, kể cả 0,5đ cuối đề); GK2/CK2 → **9,5** (nhường 0,5đ ở ý cuối bài hình, đích là **ăn điểm từng phần**).
> - 👉 Quy trình soạn đầy đủ (Polya, chọn dạng theo kho đề, khác tầng C ở đâu): **[HUONG-DAN-SOAN-PHIEU-B.md](HUONG-DAN-SOAN-PHIEU-B.md)**.
> - Tra chương nào thuộc nhóm nào ở **[config/ban_do_vd_vdc.json](config/ban_do_vd_vdc.json)** (dựng từ ma trận trường công bố kèm đề GK1/CK1/GK2/CK2 Hà Nội, khối 6–9; xem PDF `outputs/ban-do-vd-vdc/`). Chương còn ghi `"bien"` = **Thầy chưa chốt → chưa soạn phiếu**; cổng sẽ không soi tỉ lệ và cảnh báo.
> - Spec/phiếu tầng B **phải khai `chuong`** (slug chương) thì cổng mới soi được tỉ lệ và số ca.
> - **Quy ước chấm mức độ (anh An chốt 30/08, ĐÈ LÊN mức trường ghi trong ma trận):** dạng toán **thực tế chỉ 2–3 bước** (thay số vào một công thức rồi kết luận: bóng tháp, máy bay cất cánh, thang dựa tường, Sxq/thể tích hình chóp, tần số tương đối, xác suất một biến cố) là **THÔNG HIỂU**, không phải Vận dụng. **VDC chỉ ở hai chỗ**: câu cuối của bài hình và câu nâng cao cuối đề — **riêng lớp 6 chỉ có câu cuối đề**.
> - Mỗi dạng **VẬN DỤNG** phải khai `quy_trinh` ở **cả hai nơi**: dòng spec (`SpecRow.quy_trinh`) và **bài trong phiếu** (`ProblemBlock.quy_trinh`, level 3) — phiếu HS in hộp *Quy trình giải* ngay dưới đề, khác hộp *Gợi ý*.
> - Phiếu tầng B **phải khai `chuong`** ở cả `thuyet-minh.json` lẫn file phiếu; `new-thuyetminh`/`new-lesson` tự lấy từ đường dẫn `…/chuong-NN-…`, hoặc truyền `--chuong`.
> - Phiếu **ôn tập chương** phải có ít nhất một dòng `viet_quy_trinh: true` — bài cho HS **tự viết lại và giải thích** quy trình làm bài.

**Buổi học Lớp 9 Đại số = 3 tiếng = 180′.** Trừ **15′ giải lao** → **165′ học trên lớp** = *Ví dụ GV giảng* + *Luyện tập trên lớp*. **BTVN** làm ở nhà, tính riêng. **Mỗi buổi = 1 phiếu.**

Số câu suy từ: chia thời lượng mỗi đoạn theo **40-40-20** (NB-TH-VD), rồi chia cho **thời lượng ước tính mỗi câu** (theo bảng Thầy chốt):

| Đoạn | Ngân sách | Phút/câu NB / TH / VD | **Câu NB** | **Câu TH** | **Câu VD** |
|---|---|---|---|---|---|
| Ví dụ GV giảng | 45′ | 1 / 4 / 8 | 18 | 4 | 1 |
| Luyện tập trên lớp (×1,5) | 120′ | 1,5 / 6 / 12 | 32 | 8 | 2 |
| BTVN (ở nhà) (×1,3) | 90′ | 1,3 / 5,2 / 10,4 ¹ | 28 | 7 | 2 |
| **Tổng / phiếu** | | | **≈ 78** | **≈ 19** | **≈ 5** |

¹ Thầy chốt 2026-06-11 (khi lập bảng thống kê số câu/thời gian chung các lớp): hệ số gốc **1/4/8** là nhịp **GV hướng dẫn (Ví dụ)**; HS tự làm **trên lớp ×1,5** → 1,5/6/12; **BTVN ×1,3** → 1,3/5,2/10,4.

**Cách hiểu & áp dụng (quan trọng — kẻo over/under soạn; Thầy chốt thêm 2026-06-11):**
- "Câu" là **đơn vị tính giờ**, KHÔNG phải số đề rời. Gom thành *Bài* nhiều ý — vd 1 Bài liệt kê a)–f) tính là **6 câu NB**. Bài VD đã tách ý thì đếm **theo thẻ `[NB]/[TH]/[VD]` từng ý** (4 ý = 1 NB + 2 TH + 1 VD, KHÔNG phải 1 VD).
- **KHÔNG đếm phần Khám phá/Khái niệm** vào quỹ câu — đó là **giờ GV giảng**, với một bài bình thường nhắm **~20–30′** (đừng phình to hơn).
- **40-40-20 áp cho TỪNG PHIẾU, theo THỜI GIAN, sai số ±5 điểm %, và CHỈ tính giờ LUYỆN TẬP TRÊN LỚP** (không cân theo cụm tuần; **BTVN KHÔNG thuộc tỉ lệ này** — nó là thời lượng trên lớp). BTVN chỉ cần giữ quỹ phút. Quỹ mỗi đoạn (Luyện tập 120′ · BTVN 90′) cho lệch **±10%**.
- **`validate` tự soi tất cả** các mục trên qua `duration_gate` (cảnh báo khi lệch — phải xử lý hết trước khi trình Thầy, như mọi cảnh báo khác).
- **VD ≈ 5 câu/phiếu** đúng tinh thần "làm được **1 phần** VD" của lớp C (1 ví dụ + 2 luyện + 2 BTVN).
- Chấm `level`: NB → `1` (★☆☆), TH → `2` (★★☆), VD → `3` (★★★). **Tầng C KHÔNG có** `level 4`/kim cương, KHÔNG có `tier:extend`/HSG.
- Giữ **khung 5 chặng** chuẩn (review→concept→practice1→practice2→reflection); cắt phần nâng cao, dồn giàn giáo (ví dụ mẫu điền khuyết, chia bước) cho NB-TH thật chắc.

> Bảng gốc Thầy gửi (tham chiếu nhanh, "buổi thường" của trung tâm ≈ 1h30): ví dụ ~17′ · luyện tập ~45′ · BTVN ~60′. Bảng trên là bản **scale cho buổi 3 tiếng của Lớp 9 Đại số**.

---

## 3. Nguồn đề khi soạn phiếu tầng (BẮT BUỘC — không bịa)

Chỉ lấy từ ngân hàng đề **không đủ dạng** để dẫn dắt scaffolding. Phối hợp nguồn theo **tỉ trọng ~70% đề GKI + ~30% phiếu BT bổ trợ** (tương đối), **ưu tiên bê được HẾT / gần hết các dạng có trong đề GKI**:
1. **Ngân hàng đề GKI** `inputs/refs/de-thi/` (~70%) — bê NGUYÊN câu hay ra thi, ghi `(GKI)` / `(GKI — <trường>)` cuối đề để truy nguồn (vd với BPT: `DS-BPT-GIAI` 9/10 đề, `DS-THUCTE-LAPPT-BPT` 8/10 đề; xem `ma-tran-thong-ke.md`).
2. **Phiếu BT bổ trợ / SGK** trong folder bài (~30%) — bù dạng/đa dạng số liệu cho đủ scaffolding (vd file *Phiếu bài tập Toán 9 … TOANMATH* trong folder tuần).
3. **Phiếu bản chuẩn đã soạn** (cùng bài, folder không tiền tố) — *tận dụng đề & đáp án ĐÃ kiểm SymPy*, chỉ re-level + regroup.

Đáp án mọi PT/BPT vẫn phải **đối chiếu SymPy** + nên kèm trường `check` để `validate` tự soi (AGENTS §2).

**Trình bày (rút từ góp ý của Thầy):**
- Bài có **nhiều ý nhỏ a),b),c)…** dàn **2 cột** cho gọn — dùng `\begin{minipage}[t]{0.47\linewidth} … [[br]] … \end{minipage}\hfill\begin{minipage}[t]{0.47\linewidth} … \end{minipage}` trong block `para` (minipage qua được sanitizer; [[br]] vẫn xuống dòng trong minipage).
- **Hình minh hoạ KHÔNG được lộ đáp án** ô điền (vd opener thang máy chỉ ghi `630 kg`, không ghi `≤630`).
- Hộp **"VÍ DỤ MẪU"** (`variant:"example"`) chỉ dán lên **ví dụ thật**; định nghĩa/quy tắc để hộp thường (`variant:""`).
- Ví dụ giải: bước biến đổi nói **"chuyển vế đổi dấu"** (đừng máy móc "cộng … vào hai vế"); câu **"Vậy nghiệm …"** xuống dòng riêng (`[[br]]`).
- Chấm sao theo **mức nhận thức TỪNG CÂU** (giải BPT 1 bước là TH ★★☆, không phải NB).

---

## 4. Quy trình soạn phiếu tầng (tóm tắt)

```bash
mkdir "inputs/seeds/<lop>/<mon>/[C]tuanNN-<chu-de>"        # tiền tố [C] trước tuanNN
python -m src.main new-lesson "<folder [C]…>" --tier C      # khung + class_tier="C" (badge LỚP C tự in trên PDF)
# → điền nội dung bám 3 nguồn (§3), số câu theo bảng SPEC (§2), chấm level 1–3
python -m src.main validate <file.json>                     # cổng sạch (gồm SymPy)
python -m src.main build-folder "<folder [C]…>"             # 3 PDF/phiếu — badge LỚP C hiện ở header
# → Thầy xem PDF rồi approve
```

## 5. Công thức soạn NỘI DUNG phiếu lớp C (checklist sư phạm — Thầy chốt qua nhiều vòng)

> Đây là "quy trình riêng cho phiếu lớp [C]". Làm đúng từng mục để khỏi soạn lại.

**A. Mạch dẫn dắt = QUY NẠP + ĐÚNG THỨ TỰ LOGIC** (HS bình thường/yếu học từ cụ thể → trừu tượng):
1. **Khám phá**: mở bằng **ÔN KIẾN THỨC CŨ liên quan trực tiếp** (vd giải lại 1 PT trước khi học BPT) — khái niệm mới trình bày như **MỞ RỘNG của cái đã thạo**, không phải chủ đề lạ. Rồi cho HS *GẶP* đối tượng qua **ví dụ/tình huống thật** (chưa định nghĩa hình thức, chưa nói khái niệm phụ, chưa giải). **Tình huống mở màn phải GẮN LIỀN ĐỜI SỐNG HS** (góp ý 2026-06-11): điểm trung bình xét HSG, tiền tiêu vặt, vé concert, nạp game… — bối cảnh "người lớn/kỹ thuật" (thang máy chở hàng, lãi suất, trả góp) KHÔNG đặt ở mở màn, để dành cho bài luyện theo đề GKI.
2. **Khái niệm**: HS **quan sát & phân nhóm ví dụ TRƯỚC** → chốt **định nghĩa NGẮN** sau (mục tiêu là **NHẬN BIẾT**, không bắt thuộc câu chữ; kèm "mẹo soi" 1 dòng). Định nghĩa GỐC trước khái niệm phụ thuộc (vd "BPT" *trước* "nghiệm của BPT"). Với cách giải/quy tắc: **VÍ DỤ MẪU trước → RÚT RA quy tắc sau**; nếu có kiến thức cũ tương đồng thì đặt **SONG SONG 2 cột "đã thạo | mới"** (vd giải PT | giải BPT cùng một bài).
3. **"HS thấy CẦN mới đưa công cụ":** hộp BẪY ĐIỂM/quy tắc/bảng ôn **KHÔNG đặt trước** khi HS gặp tình huống dùng nó (đừng ôn "4 tính chất BĐT" ở Khám phá khi chưa giải gì). Bẫy hay nhất là để HS **tự đụng**: **cài LỖI SAI có giàn giáo** — nhân vật "bạn Minh/bạn Lan" giải sai kiểu kinh điển → HS kiểm tra bằng **thử số chỉ định sẵn** (vd x=0) thấy mâu thuẫn → tự rút ra quy tắc → hộp **BẪY ĐIỂM chốt NGAY SAU** (lớp C: không để quy tắc ở dạng "tự hiểu").
4. **Luyện tập 1 = dồn NHẬN BIẾT** (nhận biết dạng, điền dấu, tìm điều kiện hệ số, thử nghiệm thay số). Đây là phần lớp C cần thạo 100%. **NB phải BÁM DẠNG THI** (góp ý 2026-06-11): chỉ giữ **MỘT** bài nhận-biết-dạng (không đặt 2 bài trùng kiểu); chỗ còn lại dồn cho NB là *viên gạch của kỹ năng được chấm điểm* (vd drill ĐIỀN CHIỀU khi nhân/chia hai vế — nuôi thẳng câu "giải BPT" của đề).
5. **Luyện tập 2 = GIẢI (Thông hiểu)** — kỹ năng trục của bài.
6. **Tổng kết + BTVN**. **Sơ đồ Tổng kết phải BÁM MỤC TIÊU + ĐI SÁT BÀI ĐỀ GKI** (góp ý 2026-06-11): vẽ **đường đi ĐỦ BƯỚC của một câu thi** (vd BPT: khử mẫu $\to$ mở ngoặc $\to$ chuyển vế đổi dấu $\to$ thu gọn $\to$ chia hệ số), **mỗi ô ghi rõ Bài tương ứng vừa luyện** để HS tra ngược; KHÔNG vẽ quy trình rút gọn sai bản chất (BPT thuần không có bước "thu gọn" đứng riêng).
7. **Buổi đôi (2 phiếu/tuần): phân công RÕ** (góp ý 2026-06-11) — phiếu A gom **toàn bộ kỹ thuật giải** (kể cả quy đồng khử mẫu); **toán lời văn dồn hết** sang phiếu B.

**B. Độ khó:** **BỎ HẲN vận dụng cao** (vô nghiệm/đúng-mọi-x, tích-thương, HSG, kỹ thuật lạ). Lớp C = thạo NB+TH + làm được **1 phần VD**.

**C. Tách bài VẬN DỤNG thành chuỗi câu nhỏ** (gỡ giàn — HS yếu vẫn ăn điểm từng phần):
`a) [NB] từ khoá → dấu (≤/≥)` → `b) [TH] viết biểu thức theo ẩn` → `c) [TH] lập BPT` → `d) [VD] giải & trả lời`. Gắn thẻ `[NB]/[TH]/[VD]` ở đầu mỗi ý để truy tỉ lệ.
**Gỡ giàn DẦN qua CHUỖI BÀI** (góp ý 2026-06-11 — scaffolding fade): bài VD đầu chẻ NHỎ NHẤT (vd 8 câu a–h, có Ô ĐIỀN từng bước, hỏi cả chiều làm tròn trước khi kết luận) → bài sau còn 4 ý không ô điền → bài kế còn 2 ý (tự gọi ẩn, tự giải) → BTVN gần đề trần (chỉ 1 gợi ý móc về bài đã luyện). TRƯỚC chuỗi VD, LT1 drill rời từng "viên gạch" NB (từ khoá → dấu; viết biểu thức theo $x$) rồi 1 bài TH lập-BPT-chưa-giải nối chúng lại.

**D. Cân tỉ lệ:** hiểu **40-40-20 là tỉ lệ THỜI GIAN, không phải số câu** (câu NB làm nhanh 1,5′, TH 6′, VD 12′ → muốn cân thì NB phải đông câu hơn). Thực tế: dồn NB vào LT1 cho **NB ≈ TH về số câu** (≈40-40); VD ít và đã tách bước. Buổi luyện kỹ năng tự nhiên hơi nặng TH — chấp nhận, defend bằng "đây là buổi luyện GIẢI".

**E. Trình bày (lỗi đã từng bị bắt — tránh):**
- **Phiếu HS chỉ in ĐỀ + HOẠT ĐỘNG** (góp ý 2026-06-11): câu thuyết minh/dẫn dắt dài KHÔNG in lên phiếu — GV nói miệng; chuyển vào `teacher_note` (hiện ở guide) dưới mục "KỊCH BẢN LỜI DẪN GV" để GV nào cầm phiếu cũng giảng được.
- **`teacher_note` phải là DÀN Ý ĐIỀU PHỐI có cấu trúc, XUỐNG DÒNG bằng `[[br]]`** (góp ý 2026-06-11 — không viết thành một khối văn): mỗi chặng luyện tập tối thiểu 3 mục gạch đầu dòng: **DẠNG & MỨC** (bài nào NB/TH/VD, kỹ năng gì, nguồn GKI nào), **KHI HS BÍ — câu hỏi gợi mở** (chuỗi câu hỏi dẫn từng nấc, kiểu "MỘT quyển bao nhiêu? HAI quyển? vậy x quyển?"), **BIẾN THỂ CHO THÊM** (GV đổi hệ số/bối cảnh tại chỗ cho HS yếu luyện thêm hoặc HS nhanh làm tiếp). GV cầm guide phải điều phối được mà không cần người soạn.
- **Công thức toán PHẢI XUỐNG DÒNG riêng** (góp ý 2026-06-11): mọi PT/BPT/biểu thức HS cần đọc-giải không để dính giữa câu văn — câu dẫn kết thúc bằng dấu hai chấm rồi `[[br]] \quad $...$` (áp cho cả đề bài, ví dụ mẫu, hộp bẫy, opener).
- Bài nhiều ý a)b)c)… → xếp **2 cột** (`minipage`).
- Trong một câu mà liệt kê **nhiều BPT** → mỗi BPT **xuống dòng riêng** (`[[br]] \quad $\bullet$\;`), đừng để cùng dòng (rối).
- **Hình minh hoạ KHÔNG được lộ đáp án** ô điền — kể cả **chú thích dưới hình**: thang máy ghi `630 kg` (không `≤630`); heo đất ghi `tiền để dành` (KHÔNG `≤ 50k`). Soi lại tikz: nếu có `\node` chú thích trùng với đáp số ô điền thì **xoá node đó**.
- **VÍ DỤ MẪU phải điền khuyết HẾT** — Thầy + HS cùng làm: blank cả **bước biến đổi LẪN câu kết luận** ("Vậy nghiệm là $x\ \rule{}{}$"), KHÔNG ghi sẵn đáp số. Đáp án dồn về trường `solution` (answer key, chỉ hiện ở bản GV). Ví dụ NHẬN BIẾT cũng để ô điền cho TỪNG ý (đừng `\underline{là}` sẵn).
- **KHÔNG dùng dấu suy ra `⇒` (`\Rightarrow`) trong nội dung HS đọc** — THCS chưa dạy ký hiệu này. Thay bằng **xuống dòng từng bước** (`[[br]]`) hoặc chữ "nên/được". (Trường `solution`/`teacher_note` của bản GV thì chấp nhận `⇒` cho gọn.)
- **Khai triển giữ dấu trung gian** — đừng nhảy tắt nuốt dấu: `$3(x+1)-6$` phải qua `$3x+3-6$` rồi mới gộp `$3x-3$` (viết thẳng `3x-3` khiến Thầy tưởng sai dấu `+1`).
- **Lớp C: HS trình bày VÀO VỞ → KHÔNG kẻ dòng** trên phiếu. Dùng `{"type":"writelines","count":0}` = chỉ chừa **một dòng trắng** sau mỗi bài (không vẽ `\fillline`). `count≥1` mới ra dòng kẻ (dành tầng/bài cần viết tại chỗ).
- **Không thêm chữ thừa** kiểu "— cùng làm", "— xem ví dụ trước" vào tiêu đề ví dụ; để tiêu đề gọn ("(4) Cách giải.").
- **Câu dẫn viết bằng TỪ KHÓA, không viết văn** — bỏ hẳn câu đưa đẩy/động viên ("Đây là điểm ăn chắc của lớp mình", "(lớp 8 đã thạo)", "bộ áo mới", "Bảng này dùng suốt buổi hôm nay…", "— chắc điểm tuyệt đối"). Diễn đạt dạng đẳng thức/mệnh đề ngắn: *"BPT = PT thay dấu = bằng dấu so sánh"*, *"Dịch sai dấu = sai cả bài!"*. Hộp bẫy/chốt = **gạch đầu dòng từ khóa**, không đoạn văn.
- **Chuỗi biến đổi nhiều bước trong phần HS đọc → MỖI BƯỚC MỘT DÒNG** kèm chú thích trong ngoặc (kể cả khi viết lời giải sai của "bạn Minh") — không viết chuỗi ngang một dòng; chuỗi ngang chỉ dành cho `solution`/`teacher_note` bản GV.
- **Sơ đồ Tổng kết: mọi Ô ĐIỀN phải có "móc treo" đã dạy trong phiếu** — không bắt HS điền khái niệm chưa gặp (muốn có ô "ẩn ở mẫu" thì phải cài ví dụ $2/x$ vào hoạt động phân nhóm trước). Câu dẫn phía trên sơ đồ **không lặp ý** với caption của sơ đồ.
- Hộp **"VÍ DỤ MẪU"** (`variant:"example"`) chỉ dán lên **ví dụ thật**; định nghĩa/quy tắc để hộp thường (`variant:""`).
- **Sơ đồ tư duy** phải **nói rõ mục đích** ngay trên nó (vd "tự điền để hệ thống lại cả buổi — bản tóm tắt mang về ôn"), đừng để HS không biết để làm gì.
- Bước giải nói **"chuyển vế đổi dấu"** (đừng máy móc "cộng … vào hai vế"); câu **"Vậy nghiệm …"** xuống dòng riêng.
- **KHÔNG dùng ký hiệu vòng tròn ①②③** (font thiếu glyph → ô vuông) — dùng `(1)(2)(3)`. Mũi tên `→` trong text phải bọc `$\to$`.

**H. Cân thời lượng — đếm theo "câu" (đơn vị giờ), không theo số đề rời:** mỗi phiếu A/B đều **3 tiếng** ⇒ đoạn *Luyện tập trên lớp* phải lấp **~120′** (xem bảng §2). Khử mẫu/thực-tế ăn nhiều phút mỗi bài (TH 6′, VD 12′) nên **ít đề mà vẫn đủ giờ**; buổi nhận-biết thì cần **đông đề NB** (1,5′/câu). Khi soạn xong: nhẩm `Σ(số câu × phút/câu)` cho LT1+LT2 ≈ 120′ — thiếu thì thêm bài, dư thì bớt. Đừng nhìn "phiếu này ít bài hơn" mà vội thêm: so bằng **thời gian**, không bằng **đếm đề**.

**F. Nguồn & đáp án:** ~70% bê NGUYÊN câu GKI (ghi `(GKI — trường)`) + ~30% phiếu BT bổ trợ; phủ gần hết dạng GKI. Mọi BPT **đối chiếu SymPy** trước khi viết đáp án.

**G. Sau build (BẮT BUỘC):** đọc lại PDF — soát mạch dẫn dắt đúng thứ tự, 2 cột/xuống dòng, badge LỚP C, sao theo từng câu, không còn VDC, đáp án khớp. Rồi mới trình Thầy.
