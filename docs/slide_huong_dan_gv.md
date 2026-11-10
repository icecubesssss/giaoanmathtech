# HƯỚNG DẪN CÁCH SỬ DỤNG AI SOẠN PHIẾU
> **Tài liệu trình chiếu dành cho Giáo viên mới**  
> **Người thuyết trình:** Trương Đình Thái — Tổ Học Liệu MathTech  
> **Tệp trình chiếu HTML tương tác:** [`docs/slide_huong_dan_gv.html`](file:///Users/admin/Documents/thaitd/Code/giaoanMathtech/docs/slide_huong_dan_gv.html)

---

## SLIDE 1: TRANG TIÊU ĐỀ
* **Tiêu đề:** HƯỚNG DẪN CÁCH SỬ DỤNG AI SOẠN PHIẾU HỌC TẬP
* **Phụ đề:** Tư duy phân tầng sư phạm & Quy trình 5 bước phối hợp cùng Trợ lý AI
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
* **TH (Thông hiểu — 1–2 bước):** Áp dụng quy tắc vào bài toán cơ bản.
  * *Khối 3:* "1 hộp có 8 cái bánh, 3 hộp có bao nhiêu cái?"
  * *Khối 6:* Tính $A = 2^3 \cdot 5 - 3^2$
* **VD (Vận dụng — 2–3 bước):** Bài toán thực tế, kết hợp nhiều phép tính.
  * *Khối 3:* "35 quả cam chia 5 túi, đã bán 2 túi, còn lại bao nhiêu quả?"
  * *Khối 6:* Tìm $x$ biết: $2(x - 3)^2 = 32$
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
* **Thời lượng ca học chuẩn 90 phút:**
  * **Khối 3:** GV giảng 30' $\rightarrow$ HS làm tại lớp 45' $\rightarrow$ BTVN 60'.
  * **Khối 6:** GV giảng 25' $\rightarrow$ HS làm tại lớp 55' (nghỉ 10') $\rightarrow$ BTVN 40'.

---

## SLIDE 8: CẤU TRÚC 4 CHẶNG TRÊN PHIẾU HỌC TẬP
1. **Chặng 1 — Kiến thức nền:** Ôn nhanh kỹ năng lớp dưới/bài trước (NB nền).
2. **Chặng 2 — Kiến thức mới:** Quy tắc, công thức mới ngắn gọn.
3. **Chặng 3 — Ví dụ mẫu:** GV làm mẫu cùng HS (có khung điền khuyết).
4. **Chặng 4 — Luyện tập:** HS tự làm từ dễ đến khó theo giàn giáo (NB $\rightarrow$ TH $\rightarrow$ VD).

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

## SLIDE 10: BƯỚC 1 & 2 — TÌM NGUỒN & AI PHÂN DẠNG
* **Bước 1: Tìm Inputs nguồn uy tín**
  * Nguồn đề thi chính thức: [thcs.toanmath.com](https://thcs.toanmath.com)
  * Nguồn sách: SGK, SGV Kết nối tri thức, Sách bài tập chuẩn.
* **Bước 2: Nhờ AI phân dạng & lập thuyết minh**
  * Đưa đề cho AI quét vào: [Google Sheet Các Đầu Việc Học Liệu](https://docs.google.com/spreadsheets/d/1NCJHzp0cU9zUaJIkw47UfLzrPUj09P-5prgiGG6erDs/edit)
  * AI tự động: Chấm mã câu (NB/TH/VD), đánh dấu năm đề, thống kê dạng bài, lên Thuyết minh và xuất Phiếu học tập nháp.

---

## SLIDE 11: BƯỚC 3 & 4 — THẨM ĐỊNH SƯ PHẠM & ĐỔI CÂU
* **Bước 3: GV đọc duyệt (Việc của con người)**
  * Tự trả lời: *Trên lớp 90', mình có dẫn dắt HS lớp C học kịp phiếu này không?*
  * *Các câu NB đệm có dẫn tới câu VD đích không? Bài có đủ hứng thú không?*
* **Bước 4: Báo AI đổi câu (Vòng lặp tinh chỉnh)**
  * Nhắn cho AI: *"Câu 3 phần Luyện tập hơi khó so với lớp C, hãy chọn câu khác cùng dạng từ ngân hàng đề để HS hứng thú hơn."*
  * AI tự đọc lại ngân hàng $\rightarrow$ đổi câu $\rightarrow$ xuất lại bản PDF mới trong 10 giây.

---

## SLIDE 12: BƯỚC 5 — ĐÓNG GÓI, LÊN DRIVE & CẬP NHẬT TIẾN ĐỘ
* Khi phiếu đã chuẩn, nhắn cho AI:
  > *"Phiếu đã duyệt xong, hãy đưa lên Drive và cập nhật sheet Tiến độ giúp tôi."*
* AI tự động:
  1. Đẩy trọn bộ 3 bản PDF lên Google Drive khối/lớp.
  2. Điền link sản phẩm và đánh dấu hoàn thành vào:
     👉 [Google Sheet TIẾN ĐỘ C](https://docs.google.com/spreadsheets/d/1fH7vl99bXoV8AQ9xqnXOsVAC5XQ3ESWk5zM7APd1o4k/edit?gid=1752741035#gid=1752741035)

---

## SLIDE 13: TỔNG KẾT: HỆ SINH THÁI SẢN PHẨM HOÀN THÀNH (VÍ DỤ LỚP 9C)
Sau khi hoàn thành 1 chương bài học, hệ sinh thái sản phẩm gồm:
1. **Sheet Phân Dạng Chương & Ngân Hàng Câu Hỏi:**
   * Hàng trăm bài toán từ đề thi thật Hà Nội đã bóc tách ý a/b/c.
   * Đã chấm điểm bộ lọc L1–L5, tiêu chí T1–T8, gắn nhãn NB, TH, VD rõ ràng.
2. **Phiếu Thuyết Minh Chương (PDF / JSON):**
   * Ma trận 10–12 dạng bài/buổi, cân đối chuẩn thời lượng 90' hoặc 120'.
   * Bản thiết kế sư phạm được Thầy duyệt trước khi bắt tay làm phiếu.
3. **Thư Mục Google Drive Hoàn Chỉnh:**
   * Từng buổi học có đủ: **Handout HS + Sổ tay GV + Slide trình chiếu**.
   * Cuối mỗi chương có sẵn **Đề kiểm tra 45 phút + Ma trận đáp án chuẩn thi**.
4. **Google Sheet TIẾN ĐỘ C Quản Trị Tinh Gọn:**
   * Toàn bộ tiến độ được tích xanh hoàn thành kèm link trực tiếp.
   * Sẵn sàng in ấn phát cho học sinh và bàn giao cho cơ sở đào tạo.

