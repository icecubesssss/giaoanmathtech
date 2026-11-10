# Bộ quy chuẩn học liệu — bản tóm tắt trong repo

> **Nguồn sự thật:** Google Sheet "Các đầu việc học liệu"
> (`1NCJHzp0cU9zUaJIkw47UfLzrPUj09P-5prgiGG6erDs`). Các tab: _Xây dựng nguyên tắc học liệu_,
> _Xây dựng bộ quy chuẩn học liệu_ (L1–L5, T1–T8, Quy chuẩn 1–4, Cấu trúc 1–5),
> _Quy trình chuẩn AI dựng bài_,
> _Nguyên tắc xây dựng đề KT chương_, _Bộ quy chuẩn xây dựng đề KT chương_, _Quy trình AI soạn/dựng đề KT chương_,
> _Nguyên tắc xây dựng đề thi GK, CK_, _Bộ quy chuẩn xây dựng đề thi GK, CK_, _Quy trình AI soạn/dựng đề thi GK, CK_,
> _Điểm cần chốt_, _Từ điển nhãn_, _Định mức thời lượng_,
> _Trọng số chấm câu_, _Cột chuẩn tab phân dạng_, _Lịch sử thay đổi_.
>
> File này chỉ chép lại các quyết định Thầy đã chốt ngày 03/11/2026 (12 mục ở tab _Điểm cần chốt_)
> để tác nhân đọc repo là thấy. Sheet và file này lệch nhau thì **theo sheet**, rồi sửa file này.
> Thứ tự ưu tiên khi hai tài liệu nói khác nhau: **Sheet quy chuẩn > file này > AGENTS.md > HUONG-DAN-\*.md**.

## 1. Chấm câu (L1–L5, T1–T8)

- **L1–L5 lọc mọi câu** của tab phân dạng. Câu dính một mã thì ghi mã vào cột "Loại ngay".
- **L5 (trùng ý, chỉ đổi số) chỉ áp cho câu TRÊN LỚP.** BTVN gương 1–1 được đổi số từ bài trên lớp
  (ghi mã câu gốc). Ví dụ mẫu phải cùng dạng nhưng **khác bài** (khác bối cảnh hoặc cấu hình), không chỉ đổi số.
- **Trọng số giữ như sheet:** tổng lớp C = 13, B = 16, X = 14.
  Điểm = Σ(Tᵢ × Wᵢ) / (2 × tổng trọng số của lớp) × 10 — câu 2 điểm mọi tiêu chí luôn được đúng 10.
- **Ngưỡng đưa vào bài dạy chính theo mức của câu:** VD/VDC ≥ 7 · TH ≥ 6 · NB ≥ 5.
  Dưới ngưỡng của mức mình: dự phòng hoặc sửa. Dưới 5 ở mọi mức: loại hoặc sửa.
- Câu **NB kiến thức cũ** chấm T1 theo bài nền nó phục vụ, không chấm 0.

## 2. Hình thức câu hỏi

- **Tiểu học:** bắt buộc đan xen đủ 5 hình thức (trắc nghiệm, điền khuyết, Đúng/Sai, nối cột, tự luận ngắn)
  trên **mọi phiếu**.
- **THCS:** 5 hình thức dùng ở **chặng Khám phá và phiếu ôn tập**. Các chặng Luyện tập giữ luật
  **không dùng câu NB rời rạc** — NB là bước của một bài lớn (giàn giáo), hoặc NB kiến thức cũ.
- Khai trong `problem` (từ 03/11/2026): `options` (trắc nghiệm A–D), `dung_sai` (danh sách khẳng định, HS đánh Đ/S),
  `noi_cot_trai` + `noi_cot_phai` (bảng nối, cột B đã xáo); đáp án ghi ở `answer` ("a) Đ · b) S", "1 – b · 2 – c").
  Template tự kẻ bảng ở phiếu HS, sổ tay GV, slide và bản Word. Mỗi khẳng định / mỗi dòng cột A tính là một câu
  khi đếm quỹ phút.

## 3. Thời lượng

- **Một bảng định mức duy nhất:** `config/tier_spec.json` (chép sang tab _Định mức thời lượng_).
  Phút/câu theo khối × vai trò (GV giảng ví dụ / HS làm trên lớp / BTVN) × mức.
- **Bài nhiều ý:** mỗi ý là một câu theo mức của ý đó, cộng lại. HS tự vẽ hình: +5′ một lần cho cả bài.
  Ví dụ lớp 9, trên lớp, "a) NB · b) TH · c) VD" = 1,5 + 6 + 12 = 19,5′.
- Cột "Thời lượng" trên tab phân dạng tính bằng công thức theo mức độ, không ước lượng tay.

## 4. Nguồn câu

- Thứ tự ưu tiên 1 → 4 (đề thi chính thức → SGK → nguồn khác → không bám SGK mới).
- **Tiểu học:** không đặt tỉ lệ cứng, theo cách lớp 5 đang làm.
- **THCS lớp C:** tính theo **bài gốc** (câu NB tách từ bài đề thi vẫn tính là đề thi), áp cho câu trên lớp:
  **đề thi thật ≥ 50% · SGK ≥ 20% · sách tham khảo ≤ 30%**.

## 5. Tab phân dạng

- Cột A–M dùng chung mọi khối (tab _Cột chuẩn tab phân dạng_); từ cột N: Phân loại câu, Đề xuất thuyết minh,
  Trạng thái, Loại ngay, Đã soi ảnh, Lớp C/B/X, Chọn tay, Loại nguồn, Có hình, **Mã bài gốc**.
- **Dòng cộng dồn là chuẩn cho tab mới:** bài nhiều ý tăng mức có thêm dòng "… - a", "… - a - b", mỗi dòng chép đủ
  giả thiết. Tab lớp 9 đã có (một dòng mỗi bài + cột "Mức độ từng ý") giữ nguyên, repo tự suy ra dòng cộng dồn.
- **Bốc câu liền mạch:** mỗi bài gốc chỉ bốc **một** dòng; các câu trong phiếu đi theo mạch kiến thức của bài,
  cùng mục tiêu, từ dạng nền đến dạng đích; không bốc câu lẻ ngoài mục tiêu chỉ để đủ số.
- **Không xoá dòng:** bỏ câu thì ghi "Bỏ" (kèm lí do) ở cột Trạng thái. Mã câu không sửa sau khi cấp.
- **Ô "Chọn tay" của Thầy đè lên luật xếp lớp của máy.**
- Quét đề bằng **ảnh**; không lấy chữ pdftotext/OCR làm đề (vụ chương IV 9C, 03/11/2026).
- File phân dạng phải là **Google Sheet gốc**, không dùng .xlsx (connector không đọc được).

## 6. Câu lấy kết quả ý trước làm giả thiết

Chỉ làm ý VDC, kết quả ý a, b ghi thành giả thiết. Điều kiện: (1) chỉ ghi kết quả của a, b, không ghi cách làm;
(2) là câu soạn mới, mã `MỚI·<mã gốc>`, phút tính bằng một câu VDC; (3) dùng ở phiếu ôn, chuyên đề VDC hoặc BTVN
sau khi HS đã làm trọn bài đó ít nhất một lần; (4) lớp C không dùng.

## 7. Lớp

| Lớp | Học sinh                                 | Đích                                                             | Trần                                                     |
| --- | ---------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------- |
| C   | nền trung bình – yếu                     | chắc kiến thức SGK, điểm kiểm tra trên trường                    | VD                                                       |
| B   | trung bình – khá                         | kỳ I (GK1, CK1) trần **9,5–10**; kỳ II (GK2, CK2) trần **9–9,5** | VDC, ít câu VDC hơn lớp A; câu cuối dạy theo tỉ lệ ra đề |
| A   | khá – giỏi                               | điểm tối đa trên trường                                          | VDC, dày hơn lớp B                                       |
| X   | giỏi, thi trường chất lượng cao / chuyên | làm được cả câu cuối đề                                          | VDC                                                      |

## 8. Nơi làm việc

| Việc                      | Làm ở đâu                                                               | Duyệt ở đâu |
| ------------------------- | ----------------------------------------------------------------------- | ----------- |
| Luật                      | Sheet quy chuẩn                                                         | Sheet       |
| Phân dạng, chọn câu, chấm | Google Sheet gốc, mỗi khối một file, mỗi chương một tab                 | Sheet       |
| Thuyết minh               | repo (`thuyet-minh.json`) → PDF; số câu/phút xem trước trên Sheet       | **PDF**     |
| Phiếu                     | repo → 3 PDF → Drive (chỉ sau approve)                                  | PDF         |
| Tiến độ                   | sheet tiến độ nhóm, tab theo khuôn 7C (vd "TIẾN ĐỘ 9C - 2026 - ThaiTD") | Sheet       |

## 9. Bài hình chứng minh & Tiêu chuẩn khung vẽ hình (Thầy chốt 04/11/2026)

- **Luyện tập 2 & BTVN tự luận:**
  - **Chỉ có đề:** Bắt buộc trình bày trọn vẹn từng bước như đi thi, tuyệt đối KHÔNG có khung điền khuyết (`[[blank:...]]`). Ở BTVN, HS phải tự đọc lại bài học trên lớp để làm độc lập.
  - **Khung vẽ hình chuẩn 5.0 cm (`\drawbox[5.0]`):** Các bài hình chứng minh bắt buộc phải có `draw: true` (+5′). Trên bản in Handout HS và Phiếu BTVN, render khung vẽ hình chuẩn cao 5.0 cm (không dùng khung 3.5 cm quá bé cho compa và thước kẻ).
  - **In sẵn đường tròn nền $(O)$:** Đối với các bài toán hình đường tròn thi vào 10 (ở Luyện tập 2 và BTVN tự luận), in sẵn đường tròn nền $(O)$ và tâm $O$ cố định vùng vẽ trong khung (`\drawbox[5.0]{...}`) để HS không vẽ lệch ra ngoài lề giấy hay vẽ quá to/nhỏ. Sổ tay GV in hình vẽ đầy đủ hoàn chỉnh (`tikz_gv`).
  - **Tiêu đề nguồn đề thi:** Tiêu đề trước bài Luyện tập 2 phải ghi rõ nguồn đề thi thật (ví dụ: `Đề thi Học kì I — THCS Ái Mộ (Long Biên)`), BỎ HOÀN TOÀN cụm từ nội bộ `— đích của buổi học`.
- **Tiêu chuẩn kích thước hình nền cố định ($R = 1.5$ cm, độ rộng $0.5\linewidth$ — Thầy chốt 04/11/2026):**
  - **Chỉ áp dụng cho các bài HS phải vẽ hình:**
    1. Các bài Ví dụ mẫu vẽ cùng GV và các bài điền khuyết Luyện tập 1 / BTVN mà HS phải vẽ tiếp vào hình nền (`b.figure.tikz_gv`): Bán kính đường tròn nền cố định chuẩn **$R = 1.5$ cm** (đường kính $3.0$ cm, không dùng $R = 1.2$ cm bé tí). Khi render dọc dưới đề, dùng tỉ lệ chuẩn **`[5cm]{0.5}`** ($0.5\linewidth$) để hình mở rộng thoáng đạt, đủ diện tích cho học sinh đặt compa, thước kẻ, vẽ thêm tiếp tuyến, dây cung, góc vuông và điểm giao.
    2. Các bài Luyện tập 2 và BTVN tự luận (`draw: true` trong khung `\drawbox[5.0]`): Đường tròn nền $(O)$ in sẵn trong khung cũng có bán kính chuẩn **$R = 1.5$ cm**, cố định tâm $O(0,0)$ và vùng vẽ để HS tự tay dựng hình chuẩn xác.
  - **Với bài KHÔNG phải vẽ hình (hình cho sẵn hoàn chỉnh):** Như bài trắc nghiệm nhận biết (Bài 1, Bài 2), bài hình thực tế đo lường... giữ nguyên kích thước nhỏ gọn (`0.44\linewidth` hoặc cột phải) để tiết kiệm trang in.

## 10. Không trùng đề, hình nền, ô trống (Thầy chốt 04/11/2026)

- **Mỗi bài, ví dụ trong phiếu một đề gốc khác.** Luyện cùng khuôn thì bốc đề khác trong tab phân dạng, kể cả câu khung bài giải và phần BTVN. Cổng `check_khong_trung_de` chặn.
- **Hình nền đúng thứ tự vẽ:** chỉ in yếu tố đề cho trước bước dựng đầu tiên. Cổng `check_hinh_nen_thu_tu` chặn.
- **Ô trống** rơi vào từ khoá cần nhớ hoặc chỗ phải suy ra, ít nhất 6 ô cho 10 dòng, và đáp án không được in sẵn ở đề ý hoặc dòng dưới. Cổng `check_mat_do_o_trong` cảnh báo mật độ; chỗ khoét vẫn phải đọc.

## 11. Sơ đồ ngược cho phiếu chứng minh (Thầy chốt 05/11/2026)

- **Ba chỗ dùng:** thẻ phương pháp (dưới các bước); ví dụ mẫu (trước Lời giải, ô trống trùng ô của lời giải để không lộ đáp án); bài HS trình bày vào vở ở Luyện tập 1 và BTVN (đề, hình, sơ đồ đầy đủ, không khung điền khuyết). Bản mẫu: phiếu 2 chương V lớp 9C.
- **Cách đọc:** ô trên cùng là điều cần chứng minh, mũi tên đi từ ô dưới lên ô trên, ô xám là điều có ngay từ giả thiết.
- **Mức:** sơ đồ được tính là giàn giáo điền khuyết, bài vẫn là câu TH vì HS còn phải đọc sơ đồ. Phiếu lớp C có bài theo sơ đồ thì không bắt buộc câu NB tách TH.
- **Phút tính từ chính bài đó, không theo cảm nhận:** có sơ đồ = đọc đề + đọc sơ đồ + số dòng lời giải × phút/dòng, bỏ phần nghĩ của mô hình `config/phut_thuc.json`; vẽ hình cộng riêng. Lệnh: `python scripts/phut_so_do.py <phiếu.json> --ghi`.
- **Cột Đề xuất thuyết minh ghi rõ ý:** mỗi mã ghi ý a, ý b, ý a-b hoặc cả bài.

## 12. Quy chuẩn và Quy trình Đề kiểm tra chương 45 phút (Thầy chốt 26/09/2026 & 05/11/2026)

> Tra cứu chi tiết tại 3 tab chuyên biệt trên Google Sheet:
>
> 1. **Nguyên tắc xây dựng đề KT chương** (8 nguyên tắc khảo thí học chẩn đoán quá trình)
> 2. **Bộ quy chuẩn xây dựng đề KT chương** (Bộ lọc Loại ngay L_KTC 1–5, Tiêu chí T_KTC 1–3, Quy chuẩn hồ sơ QC_KTC 1)
> 3. **Quy trình AI soạn/dựng đề KT chương** (Tiến trình 6 bước phối hợp giữa Thầy và AI)

### 12.1. Quy chuẩn cốt lõi (L_KTC 1–5 & T_KTC 1–3 & QC_KTC 1)

- **Mục tiêu khảo thí & Thời lượng:** Đánh giá quá trình (Diagnostic / Formative Assessment), rà soát lỗ hổng kiến thức ngay cuối chương trước khi chuyển sang chương mới. Thời lượng chuẩn **45 phút**, nằm ở buổi cuối của mỗi chương (spec ≥ 3 phiếu).
- **Cân buổi học:** Quỹ buổi cuối co theo `he_so_con_lai`: 45' luyện tập tổng kết + 45' kiểm tra độc lập (Thầy chốt 26/09/2026).
- **Cơ cấu hình thức câu hỏi (Bắt buộc đủ 3 hình thức — L_KTC 3):**
  - **Trắc nghiệm 4 lựa chọn (A/B/C/D):** 2,0 điểm (khoảng 4–8 câu NB/TH nhanh).
  - **Điền khuyết / Trả lời ngắn:** 1,0 điểm (khoảng 2–4 chỗ điền kiểm tra công thức, số mũ, ĐKXĐ, giá trị biên).
  - **Tự luận ngắn:** 7,0 điểm (các bài toán cốt lõi của chương, có phân rã ý a/b/c).
  - Đề thiếu 1 trong 3 hình thức bị **LOẠI NGAY** (L_KTC 3).
- **Nghiêm cấm trùng đề trên lớp (LUẬT CỨNG — L_KTC 1):** 100% câu hỏi trong đề kiểm tra chương phải dùng số liệu mới, tuyệt đối **KHÔNG trùng số liệu** với các bài ví dụ mẫu hoặc bài luyện tập trên lớp của phiếu học tập trong chương.
- **Bám sát tiến độ SGK KNTT (L_KTC 2):** 100% nội dung đề kiểm tra nằm trọn vẹn trong phạm vi chương vừa học theo phân phối SGK Kết nối tri thức. CẤM đưa kiến thức vượt trước hoặc đảo chương.
- **Khung phân tầng năng lực theo lớp (T_KTC 3):**
  - **Tầng C:** 40% NB (4,0đ) - 40% TH (4,0đ) - 20% VD (2,0đ) - **0% VDC** (CẤM câu VDC). Có phần TN và điền khuyết nhận biết rõ ràng giúp HS nắm chắc điểm cơ bản.
  - **Tầng B:** 30% NB (3,0đ) - 40% TH (4,0đ) - 20% VD (2,0đ) - 10% VDC (1,0đ).
  - **Tầng A/X:** 20% NB (2,0đ) - 30% TH (3,0đ) - 30% VD (3,0đ) - 20% VDC (2,0đ).
- **Lời giải chuẩn thi (`loi_giai_thi_gate` — L_KTC 5):** CẤM dấu $\Leftrightarrow$, CẤM dùng hệ thức lượng trực tiếp (phải chứng minh tam giác đồng dạng), bài hình BẮT BUỘC có hình vẽ TikZ ở đầu lời giải.
- **Hồ sơ đóng gói chuẩn (QC_KTC 1):**
  - File `de-kiem-tra.json` (DeSpec) đặt cạnh `thuyet-minh.json`.
  - Thư mục `kiem-tra-chuong/` chứa tờ đề HS + ma trận-đáp án GV (`theme: de_thi`).

### 12.2. Tiến trình 6 bước AI & Giáo viên soạn Đề kiểm tra chương

1. **Bước 1 (Khởi tạo hồ sơ & Cấu hình giờ):** Khai báo `kiem_tra_phut: 45` trong `thuyet-minh.json` (buổi cuối chương ≥ 3 phiếu); sinh khung `de-kiem-tra.json` cạnh spec.
2. **Bước 2 (Thiết kế ma trận 45 phút):** Lập ma trận kiến thức bám sát SGK KNTT; phối hợp chuẩn 3 hình thức (TN 2,0đ + Điền 1,0đ + Tự luận 7,0đ); cân đối tỉ lệ theo tầng C/B/A/X.
3. **Bước 3 (Soạn câu hỏi & Lời giải chuẩn thi):** Soạn câu hỏi với số liệu mới 100%; giải kiểm thử bằng SymPy; viết lời giải chuẩn thi (bỏ $\Leftrightarrow$, bỏ HTL trực tiếp, vẽ TikZ chuẩn giải tích).
4. **Bước 4 (Gác cổng tự động):** Chạy kiểm tra qua 3 cổng gác: `loi_giai_thi_gate` (luật trình bày), `de_gate.check_de` (ma trận, thang điểm 10, thời lượng 45'), `thuyetminh_gate.check_kiem_tra_chuong`.
5. **Bước 5 (Render PDF & Soát thẩm mỹ):** Build 2 bản PDF (`theme: de_thi`): tờ đề HS (vừa khít 1–2 trang A4) và ma trận-đáp án GV. Soát PDF bằng mắt (không trang mồ côi, không tràn lề).
6. **Bước 6 (Thầy duyệt & Đóng gói):** Thầy xem PDF, đánh giá độ phủ và chất lượng chẩn đoán; duyệt bằng `approve`; lưu trữ đồng bộ trong thư mục `kiem-tra-chuong/`.

---

## 13. Quy chuẩn và Quy trình Đề thi Giữa kì, Cuối kì (Thầy chốt 05/11/2026)

> Tra cứu chi tiết tại 3 tab chuyên biệt trên Google Sheet:
>
> 1. **Nguyên tắc xây dựng đề thi GK, CK** (9 nguyên tắc khảo thí tổng kết chuẩn CTT Parallel Forms)
> 2. **Bộ quy chuẩn xây dựng đề thi GK, CK** (Bộ lọc Loại ngay L_GKCK 1–5, Tiêu chí T_GKCK 1–6, Quy chuẩn hồ sơ QC_GKCK 1–4)
> 3. **Quy trình AI soạn/dựng đề thi GK, CK** (Tiến trình 7 bước phối hợp giữa Thầy và AI + 2 luật cứng)

### 13.1. Quy chuẩn cốt lõi (L_GKCK 1–5 & T_GKCK 1–6 & QC_GKCK 1–4)

- **Nguồn đề & Năm học (LUẬT CỨNG 05/11/2026 — L_GKCK 1 & L_GKCK 2):**
  - **Chỉ lấy đề thi từ năm học 2024–2025 trở đi** (2024–2025, 2025–2026...) vì đây là năm học chính thức toàn bộ các khối THCS hoàn tất chu trình cuốn chiếu và thi theo Chương trình GDPT 2018. Tuyệt đối **LOẠI BỎ** toàn bộ đề thuộc năm học 2023-2024 trở về trước (L_GKCK 1).
  - **100% đề thi thật các trường THCS và Phòng GD&ĐT thuộc HÀ NỘI**. CẤM lấy đề tỉnh khác (L_GKCK 2).
  - **100% bóc tách từ ảnh scan đề gốc rõ nét**. CẤM copy trực tiếp từ text OCR/pdftotext làm đề (L_GKCK 4).
- **Lọc lệch tiến độ SGK KNTT (L_GKCK 3):** Rà soát kho đề, loại bỏ 100% đề có kiến thức kỳ sau hoặc đảo kỳ so với SGK Kết nối tri thức (Thầy chốt: "bỏ hết cho nhất quán"). Chuyển đề lệch sang `inputs/refs/de-thi-lech-kntt/` kèm `ly-do.json`.
- **Mô hình Bộ 4 đề — 3 Đề ôn tương đương + 1 Đề thi chính thức (CTT Parallel Forms — T_GKCK 3 & T_GKCK 4):**
  - Mỗi đợt thi xây dựng **3 đề ôn tập tương đương nhau + 1 đề thi chính thức**.
  - **Đề ôn 1, 2:** Chứa các dạng bài top 1 (tần suất xuất hiện cao nhất trong đề thi thật Hà Nội).
  - **Đề ôn 3:** Mở rộng sang dạng bài top 2 (tần suất thấp hơn hoặc cấu hình bài toán phong phú hơn).
  - **Đề thi chính thức:** Cùng ma trận, cấu trúc và thang điểm với 3 đề ôn, nhưng lấy câu hỏi từ trường/quận khác chưa xuất hiện trong 3 đề ôn để đo năng lực thực chất, chống học vẹt.
- **Luật Rải nguồn quận/trường (Chống thiên vị cục bộ — T_GKCK 5):**
  - Mỗi đề lấy câu từ **≥ 4 quận/huyện** khác nhau tại Hà Nội.
  - Không quận/huyện nào chiếm **quá 40%** tổng số điểm của 1 đề.
  - Cả bộ 4 đề: không quận nào chiếm **quá 25%**, không trường nào chiếm **quá 15%** tổng số điểm.
  - Hàm `kiem_nguon()` trong script đề tự kiểm soát luật rải nguồn.
- **Khung ma trận & Phân tầng năng lực (T_GKCK 6):**
  - **Tầng C:** 40% NB (4,0đ) - 40% TH (4,0đ) - 20% VD (2,0đ) - **0% VDC** (CẤM VDC). Bắt buộc có phần trắc nghiệm/điền khuyết nhận biết rõ ràng để HS gỡ điểm.
  - **Tầng B:** 20-30% NB (2-3đ) - 40-50% TH (4-5đ) - 20-30% VD (2-3đ) - 5-10% VDC (0,5-1,0đ). Đích trần 9,5-10 (Kỳ I), 9-9,5 (Kỳ II).
  - **Tầng A/X:** Tăng cường câu phân hóa sâu, bài hình đa bước, cực trị thực tế.
- **Lời giải chuẩn thi (`loi_giai_thi_gate` — L_GKCK 5):**
  - **CẤM dấu $\Leftrightarrow$**: Mỗi phép biến đổi viết một dòng ngắt bằng `[[br]]`.
  - **CẤM dùng hệ thức lượng trực tiếp**: Bắt buộc chứng minh 2 tam giác đồng dạng (g.g) rồi mới suy ra tỉ số và tích hình học.
  - **Bài hình BẮT BUỘC có HÌNH VẼ TikZ chuẩn ở đầu lời giải**.
  - Phân rã điểm thành phần đến 0,25đ từng dòng (`\hfill (0,25đ)`), tổng khớp biểu điểm câu.
  - BĐT/Cực trị: Dùng $m - (x-a)^2 \le m$ hoặc Cauchy lớp 9; CẤM dùng công thức đỉnh parabol $x = -b/(2a)$ của lớp 10.
- **Hình thức in ấn & Bàn giao (QC_GKCK 3 & QC_GKCK 4):**
  - Theme `de_thi`, `"trinh_bay": "thoang"` (font 13pt, hình to rõ). Đề HS in vừa khít 2 trang A4.
  - Bản GV có ma trận kiến thức + nguồn đề + lời giải chi tiết + lưu ý chấm. Kèm phiếu theo dõi tiến bộ.
  - Bộ 8 file PDF đồng bộ lên đúng thư mục Google Drive của trung tâm.

### 13.2. Tiến trình 7 bước AI & Giáo viên soạn Đề thi Giữa kì, Cuối kì

1. **Bước 1 (Thu thập & Kiểm kê):** Thu thập đề thi thật Hà Nội năm học 2024–2025 trở đi theo khối/kỳ (`fetch_de_thi_khoi.py --tu-nam 2024`); lập kho ảnh scan rõ nét và kho text tra cứu.
2. **Bước 2 (Lọc lệch KNTT):** Quét từ khóa đối chiếu SGK KNTT (`soat_lech_kntt.py`); chuyển đề lệch sang kho riêng kèm lý do (`inputs/refs/de-thi-lech-kntt/`).
3. **Bước 3 (Lập lưới dạng & Thống kê):** Gắn mã dạng bằng tay từng bài/ý con vào `luoi-dang/<ky>.json`; thống kê tần suất dạng bài (% xuất hiện) để chốt khung đề (`thong_ke_luoi_dang.py`).
4. **Bước 4 (Thiết kế ma trận & Rải nguồn):** Lập `de-kiem-tra.json` (DeSpec); rải nguồn ≥ 4 quận (hàm `kiem_nguon()`); render PDF Thuyết minh ma trận đề bằng `make de` để Thầy duyệt.
5. **Bước 5 (Soạn đề & Lời giải chuẩn thi):** Chép đề từ ảnh scan gốc; giải thử 100% bằng SymPy; viết lời giải chuẩn thi (bỏ $\Leftrightarrow$, bỏ HTL trực tiếp, tính toạ độ vẽ TikZ chuẩn giải tích).
6. **Bước 6 (Gác cổng & Soát PDF bằng mắt):** Chạy `loi_giai_thi_gate` và `de_gate`; build 8 file PDF (4 đề HS + 4 đáp án GV); soát PDF bằng mắt (không trang mồ côi, không tràn lề); Thầy gõ `approve`.
7. **Bước 7 (Đóng gói & Lên Drive):** Đồng bộ trọn bộ 8 file PDF và hồ sơ học liệu lên đúng thư mục Google Drive của trung tâm (`sync-drive`).

## 14. Quy chuẩn Đề thi & Phiếu học tập Tiểu học (Lớp 5 — Thông tư 27) (Thầy chốt 08/11/2026)

### 14.1. Triết lý làm bài trực tiếp & Lưới ô ly chuẩn tiểu học
- **Học sinh làm bài ngay vào đề:** Khác với cấp THCS (học sinh làm bài ra giấy thi / vở ghi riêng), ở cấp Tiểu học (đặc biệt Lớp 5), toàn bộ đề thi định kì và phiếu học tập được thiết kế để **học sinh làm bài trực tiếp vào đề** (`Em làm bài ngay vào đề.`).
- **Bắt buộc có lưới ô ly (`variant: "oly"` / `\olyline`):**
  - Mọi bài tự luận yêu cầu tính toán hoặc trình bày bài giải bắt buộc phải có **khung lưới ô ly chuẩn tiểu học** (ô vuông lớn 10 mm × 10 mm chia lưới 4 × 4 ô nhỏ 2,5 mm × 2,5 mm, nét mực nhạt `ink!15` và `ink!35`).
  - **Không gian viết bài rộng rãi cho học sinh tiểu học:**
    - **Bài 1 (Đặt tính rồi tính — 1,0 điểm):** Đề bài chia 2 cột thoáng. Phía dưới là **khung ô ly toàn trang cao 12 cm (`count: 12` = 48 hàng caro)** để học sinh đặt tính cả 4 phép tính thoải mái, thẳng hàng dấu phẩy.
    - **Bài 2 (Tính phân số / giá trị biểu thức — 1,0 điểm):** Khung ô ly cao 4 cm (`count: 4` = 16 hàng caro) đủ cho các bước quy đồng, tính toán và rút gọn.
    - **Bài 3 (Viết số đo thích hợp vào chỗ chấm — 1,0 điểm):** Dàn 2 cột gọn gàng, điền trực tiếp vào dấu chấm `\dots\dots\dots\dots`.
    - **Bài 4 (Bài toán thực tế hình học — 2,0 điểm):** Khung ô ly cao 8 cm (`count: 8` = 32 hàng caro), đủ chỗ cho 2 câu lời giải, 2 phép tính và đáp số.
    - **Bài 5 (Toán tư duy nâng cao M3 — 1,0 điểm):** Khung ô ly cao 9 cm (`count: 9` = 36 hàng caro) cho các bước suy luận tỉ mỉ.
    - **Phiếu tự kiểm tra bài làm trước khi nộp:** Bảng tự đánh giá của học sinh (đánh dấu $\checkmark$ vào các tiêu chí hoàn thành) theo đúng tinh thần Thông tư 27.
    - **Dòng kết thúc:** `\nopagebreak\centerline{\textbf{--- HẾT ---}}` kèm lời dặn dò sư phạm: `Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!`.

### 14.2. Chuẩn căn chỉnh vừa khít đúng 4 trang A4 (1 tờ đôi A3 gập đôi — Giới hạn tiểu học)
- **Quy cách in ấn chuẩn:** Đề thi học sinh (`Phieu-HS.pdf`) **BẮT BUỘC ĐẠT ĐÚNG 4 TRANG A4 (Pages: 4)**:
  - **Trang 1 (Mặt bìa trước):**
    * Top Card thông tin học sinh (Tiêu đề đề thi, Họ và tên, Lớp, Thời gian làm bài 40 phút).
    * Khung Điểm (Số & Chữ) + Lời nhận xét của thầy cô giáo: mở rộng chiều dọc đạt chuẩn 1.8 cm (`\rule{0pt}{1.8cm}`) để thầy cô phê nhận xét chi tiết và ghi điểm thoải mái, cân đối hoàn hảo trang 1.
    * Phần I. Trắc nghiệm (4,0 điểm): 6 câu đầu tiên (Câu 1 đến Câu 6), dàn trải đều đặn, cách dòng thoáng.
    * Ngắt trang sang Trang 2 (`\newpage`).
  - **Trang 2 (Mặt trong trái):**
    * Trắc nghiệm tiếp theo: Câu 7 và Câu 8.
    * Tiêu đề: `PHẦN II. TỰ LUẬN (6,0 điểm)`.
    * Bài 1: Đặt tính rồi tính kèm **khung ô ly lớn cao 12 cm (`count: 12`)** phủ kín trang.
    * Dòng chỉ dẫn: `(Học sinh đặt tính thẳng hàng dấu phẩy và làm bài vào khung ô ly trên)`.
    * Ngắt trang sang Trang 3 (`\newpage`).
  - **Trang 3 (Mặt trong phải):**
    * Bài 2: Tính phân số kèm khung ô ly cao 4 cm (`count: 4`).
    * Bài 3: Điền số thích hợp vào chỗ chấm (4 ý đổi đơn vị đo đại lượng).
    * Bài 4: Bài toán thực tế hình học kèm **khung ô ly cao 8 cm (`count: 8`)**.
    * Dòng chỉ dẫn: `(Học sinh trình bày câu lời giải, phép tính và đáp số vào khung ô ly trên)`.
    * Ngắt trang sang Trang 4 (`\newpage`).
  - **Trang 4 (Mặt bìa sau):**
    * Tiêu đề: `PHẦN II. TỰ LUẬN (tiếp theo)`.
    * Bài 5: Toán tư duy nâng cao M3 kèm **khung ô ly cao 9 cm (`count: 9`)**.
    * Hộp Phiếu tự kiểm tra bài làm trước khi nộp (tcolorbox bo tròn màu chuẩn MathTech).
    * Dòng kết thúc `--- HẾT ---` và Lời dặn dò của thầy cô giáo nằm êm ái ở chân trang.
- **Tiêu chuẩn kiểm duyệt:** Đúng 4 trang A4 (1 tờ đôi A3 gập đôi), 0 lỗi build, 0 cảnh báo `print_gate`, không gian viết bài rộng rãi và không có khoảng trắng thừa.


