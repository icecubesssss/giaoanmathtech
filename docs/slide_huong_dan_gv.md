# HƯỚNG DẪN CÁCH SỬ DỤNG AI SOẠN PHIẾU HỌC TẬP & HỆ THỐNG TEMPLATE SHEETS
> **Tài liệu trình chiếu & cẩm nang nội bộ dành cho Giáo viên mới**  
> **Người biên soạn:** Trương Đình Thái — Tổ Học Liệu MathTech  
> **Tệp trình chiếu HTML tương tác:** [`docs/slide_huong_dan_gv.html`](slide_huong_dan_gv.html)  
> **Tệp trình chiếu Beamer PDF:** [`docs/slide_huong_dan_gv.pdf`](slide_huong_dan_gv.pdf)  
> **Quy chuẩn 3 Template Sheets chi tiết:** [`docs/quy-trinh-template-sheets.md`](quy-trinh-template-sheets.md)

---

## SLIDE 1: TRANG TIÊU ĐỀ
* **Tiêu đề chính:** HƯỚNG DẪN CÁCH SỬ DỤNG AI SOẠN PHIẾU HỌC TẬP
* **Phụ đề:** Tư duy phân tầng sư phạm, Hệ thống 3 Template Sheets & Quy trình 5 bước phối hợp cùng Trợ lý AI
* **Người thuyết trình:** Trương Đình Thái
* **Đơn vị:** Tổ Học Liệu MathTech

---

## SLIDE 2: TẢI TOOL, CÀI EXTENSION & MỞ CHAT AI (3 PHÚT)
1. **Tải Codebase & Antigravity:**  
   * Link GitHub: [github.com/icecubesssss/giaoanmathtech](https://github.com/icecubesssss/giaoanmathtech) *(Bấm Code $\rightarrow$ Download ZIP $\rightarrow$ Giải nén)*  
   * Link Antigravity: [antigravity.google/download](https://antigravity.google/download)
2. **Cài 2 Extension thiết yếu (Trong VS Code / Antigravity):**  
   * **Extension Claude (Claude Code):** Dùng Claude tương tác trực tiếp, chạy lệnh soạn bài và phân dạng cùng AI.  
   * **Extension vscode-pdf:** Mở và xem trực tiếp 3 bản PDF (Handout HS, Guide GV, Slide) ngay trong cửa sổ làm việc mà không cần cài thêm app ngoài.
3. **Mở & Kích hoạt:**  
   * Mở Antigravity $\rightarrow$ Chọn `Open Folder` mở thư mục `giaoanMathtech` $\rightarrow$ Mở ô chat AI bên phải.  
   * **Cài đặt môi trường:** Chỉ cần nhắn đúng 1 câu vào ô chat:  
     > *"Cài đặt môi trường giúp tôi"*  
     *(AI sẽ tự cài đặt 100% từ A – Z, GV không cần gõ lệnh terminal nào cả).*

---

## SLIDE 3: CƠ CHẾ HOẠT ĐỘNG
$$\text{INPUTS (Nguyên liệu)} \longrightarrow \text{PROCESS (MathTech + AI)} \longrightarrow \text{OUTPUTS (Thành phẩm)}$$

* **INPUTS:** Đề thi thật chính thức Hà Nội, ảnh scan SGK, SGV Kết nối tri thức.
* **PROCESS:** AI tự động kiểm tra nghiệm (SymPy), vẽ hình chuẩn (TikZ), dàn trang, cân đối thời lượng 90'.
* **OUTPUTS (Bộ 3 PDF Song Song):**
  1. **Handout Học sinh:** Thoáng, đẹp, có sẵn khung làm bài.
  2. **Guide Giáo viên:** Có đáp án chi tiết, gợi ý sư phạm và định mức phút.
  3. **Slide Trình chiếu (16:9):** Tự động ẩn lời giải để GV tương tác trên bảng.

---

## SLIDE 4: PHÂN TẦNG NĂNG LỰC HỌC SINH (A – B – C – X)

| Tầng | Đối tượng học sinh | Mục tiêu điểm số | Giới hạn bài tập |
| :---: | :--- | :---: | :---: |
| **C** | **Nền tảng trung bình – yếu**, hay quên kiến thức | Chắc SGK, đạt **7 – 8 điểm** trên trường | **Trần: Vận dụng (VD)<br/>(CẤM TUYỆT ĐỐI VDC)** |
| **B** | Trung bình – khá | Kỳ I: 9,5 – 10đ; Kỳ II: 9 – 9,5đ | Có VDC nhẹ |
| **A** | Khá – giỏi | Đạt điểm tối đa trên trường | VDC dày dặn |
| **X** | Chuyên / Chất lượng cao | Chinh phục trọn vẹn câu cuối đề thi | VDC nâng cao |

> 📌 **Trọng tâm hiện tại:** Toàn bộ phiếu học tập tập trung thiết kế cho **LỚP C**.

---

## SLIDE 5: 4 CẤP ĐỘ CÂU HỎI (NB – TH – VD – VDC)
* **NB (Nhận biết — 1 bước):** Công thức, định nghĩa, tính nhẩm trực tiếp.
  * *Khối 3:* Tính nhẩm $7 \times 4 = ?$
  * *Khối 6:* Tính giá trị $2^3 = ?$
  * *Khối 9:* Tìm ĐKXĐ của $\sqrt{x - 3}$; nhận diện góc vuông tại tiếp điểm.
* **TH (Thông hiểu — 1–2 bước):** Áp dụng quy tắc vào bài toán cơ bản.
  * *Khối 3:* "1 hộp có 8 cái bánh, 3 hộp có bao nhiêu cái?"
  * *Khối 6:* Tính $A = 2^3 \cdot 5 - 3^2$.
  * *Khối 9:* Rút gọn biểu thức chứa căn; chứng minh tam giác bằng nhau (c.c.c).
* **VD (Vận dụng — 2–3 bước):** Bài toán thực tế, kết hợp nhiều phép tính.
  * *Khối 3:* "35 quả cam chia 5 túi, đã bán 2 túi, còn lại bao nhiêu quả?"
  * *Khối 6:* Tìm $x$ biết: $2(x - 3)^2 = 32$.
  * *Khối 9:* Chứng minh tiếp tuyến $DB \perp OB$; tính khoảng cách thực tế bằng TSLG.
* **VDC (Vận dụng cao — $\ge 4$ bước):** Phân hóa 9,5 – 10 điểm $\rightarrow$ **Lớp C: 0% (Không đưa vào phiếu)**.

---

## SLIDE 6: KỸ THUẬT THEN CHỐT: "NB TÁCH CÂU" (GIÀN GIÁO LỚP C)
* **Nguyên tắc vàng:** **Cấm dùng câu NB rời rạc, vô bổ.** Mọi câu NB phải là bước đệm trích từ chính bài toán thi thật.
* **Ví dụ trực quan:**
  * *Bài toán gốc [TH]:* "Tính giá trị biểu thức: $M = 150 - [100 - (3^2 \cdot 5)]$."
  * *Chẻ giàn giáo:*
    * **Ý a [NB đệm]:** "Tính giá trị của $3^2$ và $3^2 \cdot 5$."
    * **Ý b [TH]:** "Tính ngoặc vuông $[100 - (3^2 \cdot 5)]$ rồi tính $M$."
  * 👉 **Hiệu quả:** HS trung bình – yếu tự tin làm được ý đầu, có đà giải quyết trọn vẹn cả bài.

---

## SLIDE 7: TỈ LỆ CHUẨN LỚP C: 40% – 40% – 20%
* **Công thức phân bổ:**
  * **40% NB + 40% TH** (= 80% Cơ bản): Xây chắc nền móng, HS không sợ học.
  * **20% VD:** Va chạm bài toán thực tế vừa sức.
  * **0% VDC:** Tránh gây quá tải.
* **Thời lượng ca học chuẩn 90 phút (Khối 9):**
  * **GV giảng & ví dụ mẫu:** 25 phút.
  * **HS luyện tập trên lớp:** 55 phút (nghỉ giải lao 10 phút).
  * **BTVN tự luyện tại nhà:** 40 phút.

---

## SLIDE 8: CẤU TRÚC 4 CHẶNG TRÊN PHIẾU HỌC TẬP
1. **Chặng 1 — Kiến thức nền (Khám phá):** Ôn nhanh kỹ năng lớp dưới/bài trước (NB kiến thức cũ, trắc nghiệm nhanh).
2. **Chặng 2 — Kiến thức mới:** Quy tắc, công thức mới ngắn gọn, dễ nhớ.
3. **Chặng 3 — Ví dụ mẫu:** GV làm mẫu cùng HS (có khung điền khuyết, sơ đồ suy luận).
4. **Chặng 4 — Luyện tập:** HS tự làm từ dễ đến khó theo giàn giáo (Luyện tập 1 điền khuyết $\rightarrow$ Luyện tập 2 tự giải tự vẽ hình).

---

## SLIDE 9: QUY TRÌNH 5 BƯỚC SOẠN PHIẾU CÙNG AI
```
[1. Tìm nguồn đề] ➔ [2. AI phân dạng & ra phiếu] ➔ [3. GV đọc duyệt sư phạm]
                                                        │
                      [5. Đóng gói & cập nhật Sheet] ⮜──┴─ (Đạt chuẩn)
                                                        │
                      [4. Báo AI đổi câu phù hợp] ⮜─────┘  (Chưa ưng)
                                │
                                └──────────────➔ Quay lại Bước 3
```

---

## SLIDE 10: HỆ THỐNG 3 TEMPLATE SHEETS LIÊN KẾT ĐỘNG
> 📊 **Link Google Sheets Mẫu (Đầy đủ 3 Tab Chuẩn):** [docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY](https://docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY/edit)  
> *(Giáo viên bấm vào link trên $\to$ Chọn **Tệp** $\to$ **Tạo bản sao** để bắt đầu chương mới).*

Trong hệ sinh thái MathTech, mọi khâu xây dựng học liệu được chuẩn hóa qua **3 Template Sheets cốt lõi**:

```
[Template 1: Ngân hàng đề & Phân dạng (47 cột)] ──(Mã câu cột M)──► [Template 2: Thuyết minh spec động]
      • Lọc L1–L5 & Chấm điểm T1–T8 tự động                            • Ma trận dạng bài & Quỹ 90'
                                                                                   │
                                                                                   ▼
                                                                     [BỘ 3 BẢN PDF SONG SONG]
                                                                     (Handout HS, Guide GV, Slide)
                                                                                   │
                                                                                   ▼
                                                                     [Template 3: Sheet Quản trị Tiến độ]
                                                                     • Tích xanh nghiệm thu, link Drive
```

* **Nguyên tắc cốt lõi:**
  * **Spec-First:** Khóa khung dạng bài và thời lượng trước khi bắt tay viết code.
  * **Single Source of Truth:** Mọi câu hỏi trên phiếu đều trỏ về **Mã câu** trên Tab Phân dạng, không bịa đề ngoài sheet.
  * **Phân công rõ ràng:** Đề thi và bài kiểm tra do Thầy tạo riêng. GV và AI tập trung xây dựng bài học và học liệu trên lớp.

---

## SLIDE 11: TEMPLATE 1 — TAB PHÂN DẠNG CHƯƠNG & NGÂN HÀNG CÂU HỎI (47 CỘT CHUẨN)
Tab Ngân hàng bài được chia thành **5 Phân khu chức năng** hoàn chỉnh:

1. **Phân khu I (Cột A–M) — Dữ liệu bài toán & Đề thô:**
   * `Bài cụ thể` (A), `Nguồn input` (B), `Mức độ` (C), `Dạng bài` (D), `Ưu tiên 1-4` (E), `Thời lượng phút` (G), `Mã câu duy nhất` (M).
2. **Phân khu II (Cột N–X) — Phân loại sư phạm & Giàn giáo §4b:**
   * `Phân loại câu` (N: 7 loại câu §4b), `Đề xuất thuyết minh` (O), `Trạng thái` (P), `Loại ngay L1–L5` (Q), `Lớp C/B/X` (S–U), `Chọn tay` (V).
3. **Phân khu III (Cột Y–AE) — Bóc tách ý con & Kỹ thuật đề thật:**
   * `Mã bài gốc` (Y), `Kỹ thuật giải` (AB), `Nhãn chương` (AC: `[V]`), `Nhóm nghi trùng` (AD).
4. **Phân khu IV (Cột AF–AM) — Chấm 8 Tiêu chí chất lượng (T1–T8):**
   * Chấm điểm 0, 1, 2 cho: `T1 Trọng tâm SGK`, `T2 Ý toán`, `T3 Bối cảnh`, `T4 Phân hoá`, `T5 Lỗi sai`, `T6 Nghiệm đẹp`, `T7 Dạng đề thi`, `T8 Mở rộng`.
5. **Phân khu V (Cột AN–AU) — Đánh giá & Kết luận phân tầng tự động:**
   * `Điểm Lớp C` (AN), `Ngưỡng mức` (AQ), `Kết luận tự động` (AR: *Đưa vào bài / Dự phòng / Loại*), `THẦY DUYỆT` (AS).

---

## SLIDE 12: CƠ CHẾ LỌC LOẠI NGAY (L1–L5) & CHẤM ĐIỂM (T1–T8) TỰ ĐỘNG
* **Bộ lọc Loại ngay L1–L5 (Cột Q):**
  * **L1:** Sai kiến thức toán học / dữ liệu ngớ ngẩn.
  * **L2:** Lệch chương trình SGK KNTT GDPT 2018.
  * **L3:** Nghiệm cồng kềnh, số lẻ vô tỉ xấu.
  * **L4:** Dài quá 4 bước suy luận không tách được giàn giáo.
  * **L5:** Trùng ý chỉ đổi số trên lớp (chỉ cho phép ở BTVN gương 1-1).
* **Công thức tính điểm chuẩn hóa Lớp C (Cột AN):**
  $$\text{Điểm}_C = \frac{3 \cdot T_1 + 1 \cdot T_2 + 2 \cdot T_3 + 1 \cdot T_4 + 2 \cdot T_5 + 2 \cdot T_6 + 2 \cdot T_7 + 0 \cdot T_8}{2 \times 13} \times 10$$
* **Ngưỡng điểm đưa vào bài chính (Cột AQ):**
  * $\text{VD} \ge 7{,}0$ điểm · $\text{TH} \ge 6{,}0$ điểm · $\text{NB} \ge 5{,}0$ điểm.
* **Quy chuẩn mã màu trực quan:**
  * **Cam nhạt (`#FCE4D6`):** Bài VD/VDC & Ưu tiên 4.  
  * **Vàng kem (`#FFF2CC`):** Vùng Thầy nhập tay (`THẦY CHỌN`).  
  * **Xanh lá nhạt (`#E2EFDA`):** Máy tự tính (`ĐƯA VÀO BÀI` & Câu đã vào phiếu).  
  * **Tím Lavender (`#EDE7F6`):** Câu `NB kiến thức cũ`.

---

## SLIDE 13: TEMPLATE 2 — PHIẾU THUYẾT MINH LIÊN KẾT ĐỘNG (SPEC DYNAMIC SHEET)
* **Bảng Ma trận dạng bài theo ca học:**
  * Khai báo chuẩn 7 loại câu §4b (`NB lẻ LT`, `NB tách TH`, `NB ghép bài`, `TH lẻ LT`, `TH ghép bài`, `TH tách VD`, `VD lẻ`) + `NB kiến thức cũ`.
  * Cột `Mã câu đề xuất` liên kết trực tiếp với cột Mã câu (M) của Template 1.
  * Cột `THẦY CHỌN & ĐỔI CÂU`: Vùng Thầy duyệt hoặc thay đổi mã câu trực tiếp trên Sheet.
  * Cột `Chốt mã`: Tự động cập nhật `=IF(Thầy_Chọn<>"", Thầy_Chọn, Đề_Xuất)`.
* **Dashboard Cân đối quỹ giờ & Tỉ lệ vàng:**
  * **Tỉ lệ năng lực:** 40% NB (48') – 40% TH (48') – 20% VD (24') – 0% VDC.
  * **Thời lượng:** GV giảng $\le 25'$, HS làm trên lớp $55'$, BTVN $40'$.
* **Gác cổng tự động (`thuyetminh_gate`):**
  * Tự động chặn và báo đỏ nếu lệch quỹ giờ $>\pm 10\%$, xuất hiện VDC, hoặc thiếu nhãn §4b.

---

## SLIDE 14: TEMPLATE 3 — SHEET TIẾN ĐỘ & VÒNG LẶP ĐỒNG BỘ GOOGLE DRIVE
* **Khung Quản trị tiến độ tuần (Khuôn mẫu TIẾN ĐỘ 9C / 8C / 7C):**
  * `Tuần / Ca` $\rightarrow$ `Mã phiếu` $\rightarrow$ `Tên bài SGK` $\rightarrow$ `Link Sheet Phân dạng` $\rightarrow$ `Link Thuyết minh PDF`.
  * `Trạng thái Thẩm định:` 🟡 Đang soạn $\rightarrow$ 🟠 Chờ duyệt $\rightarrow$ 🟢 **ĐÃ DUYỆT**.
  * `Link Sản phẩm trên Google Drive:` Handout HS + Sổ tay GV + Slide Beamer + File Word.
  * `Nghiệm thu:` Tích xanh checkbox hoàn thành khi bàn giao cơ sở.
* **Cơ chế đồng bộ tự động một chạm:**
  * Khi GV gõ lệnh duyệt, AI tự động biên dịch, đẩy file lên đúng thư mục Drive và điền link vào sheet.

---

## SLIDE 15: BƯỚC 1 & 2 — TÌM NGUỒN & AI PHÂN DẠNG VÀO SHEET (THỰC HÀNH)
* **Bước 1: Chuẩn bị nguồn đề uy tín**
  * Nguồn đề thi thật Hà Nội: các trường THCS và Phòng GD&ĐT (2024–2025 trở đi).
  * Nguồn sách: SGK, SGV Kết nối tri thức.
* **Bước 2: AI quét đề & điền Template 1**
  * Đưa đề ảnh cho AI quét vào Tab Phân dạng của chương.
  * AI tự động: Chấm mã câu, gán nhãn §4b, chấm điểm T1–T8, tính kết luận Lớp C và tạo dự thảo Template 2 (Thuyết minh).
* **Câu lệnh mẫu cho GV:**
  > *"Hãy quét các đề thi HK1 trong thư mục inputs và nạp vào Template 1 phân dạng Chương 5 giúp tôi. Chấm điểm T1-T8 cho lớp C."*

---

## SLIDE 16: BƯỚC 3 & 4 — THẨM ĐỊNH SƯ PHẠM & ĐỔI CÂU TRÊN SHEET (THỰC HÀNH)
* **Bước 3: GV thẩm định sư phạm**
  * GV mở bản PDF Thuyết minh và Tab Template 2 để rà soát:
    * *Các bước đệm NB có khớp với bài toán VD đích không?*
    * *Thời lượng 90' học sinh lớp C có kịp hoàn thành không?*
* **Bước 4: Đổi câu linh hoạt**
  * Cách 1: GV nhập trực tiếp mã câu thay thế vào cột **`THẦY CHỌN & ĐỔI CÂU`** trên Sheet.
  * Cách 2: Nhắn trực tiếp trong ô chat AI:
    > *"Câu 3 phần Luyện tập hơi khó so với lớp C, hãy đổi câu khác cùng dạng từ ngân hàng Template 1."*
  * AI tự động cập nhật spec $\rightarrow$ xuất lại bản PDF mới trong 10 giây.

---

## SLIDE 17: BƯỚC 5 — ĐÓNG GÓI, LÊN DRIVE & CẬP NHẬT TIẾN ĐỘ (THỰC HÀNH)
* Khi phiếu học tập đã hoàn thiện đạt chuẩn, GV chỉ cần nhắn 1 câu:
  > *"Phiếu 2 Chương 5 đã duyệt xong, hãy đưa lên Drive và cập nhật Template 3 (Sheet Tiến độ) giúp tôi."*
* **AI tự động thực thi chuỗi tác vụ:**
  1. Kiểm tra nghiệm và cấu trúc lần cuối bằng các cổng gác tự động (`validate`).
  2. Biên dịch song song trọn bộ 3 bản PDF: **Handout HS + Guide GV + Slide Trình chiếu**.
  3. Tải lên đúng thư mục chương trên Google Drive của khối/lớp.
  4. Cập nhật link sản phẩm và tích xanh hoàn thành vào Sheet Tiến độ.

---

## SLIDE 18: TỔNG KẾT: HỆ SINH THÁI HỌC LIỆU & CHEAT-SHEET CÂU LỆNH
* **Hệ sinh thái sản phẩm hoàn thành mỗi chương:**
  1. **Template 1:** Ngân hàng bài phân dạng 47 cột chấm điểm T1–T8 chi tiết.
  2. **Template 2:** Phiếu Thuyết minh cân đối chuẩn 40-40-20 và quỹ 90'.
  3. **Bộ 3 PDF Song Song:** Handout HS + Sổ tay GV + Slide Beamer 16:9.
  4. **Template 3:** Sheet Tiến độ tích xanh hoàn thành, đồng bộ Google Drive.
* **Bảng câu lệnh mẫu (Cheat-sheet) cho Giáo viên mới:**
  * `make b`: Build nhanh 3 bản PDF cho phiếu vừa sửa (~9 giây).
  * `make check-tm SPEC=...`: Kiểm tra gác cổng thời lượng và số câu thuyết minh.
  * *"Cài đặt môi trường giúp tôi"*: AI tự động thiết lập toàn bộ công cụ.
  * *"Đổi câu X sang câu Y"*: AI tự đổi câu và cập nhật tài liệu.
  * *"Đưa lên Drive và cập nhật Sheet"*: AI tự động xuất bản và đóng gói.
