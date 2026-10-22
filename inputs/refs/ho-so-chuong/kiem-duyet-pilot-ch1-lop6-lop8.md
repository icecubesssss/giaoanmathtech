# Kiểm duyệt độc lập — pilot chương I lớp 6 + lớp 8 (tầng B, C)

> Agent kiểm duyệt (không phải người soạn), soát lại ngày 16/10/2026 trên **bản hiện tại** của seed/PDF
> (seed sửa lúc 00:53–00:56 ngày 16/10, mọi PDF đều build SAU seed → không có PDF lỗi thời).
> Áp luật `docs/quy-trinh-khoi-678.md` §1, gồm mục "Sau pilot ch.I" (rate gốc 8C, VD chỉ khi ≥4 bước/có biến đổi,
> 8B 30-45-25 + `khong_kiem_tra`, 6B 15-50-35 đề xuất + KT t11, dấu × lớp 6 Bài 1-4).

## 0. Kết luận

**CHƯA ĐẠT để đưa Thầy** — còn 1 lỗi CHẶN (hình SGK 1.22 vẽ sai bán kính, ở cả 8B và 8C) và một loạt NÊN SỬA
sửa nhanh (nhãn VD sai ở 8B, "lớp 8C" trong phiếu 8B, chữ "Ta có Số…", ví dụ đặt lệch dạng, ghi chú GV đánh số sai).
Điểm mạnh: **đáp án 100% đúng** (giải lại toàn bộ, SymPy cho phần tính), **nguồn chép đúng** (đối chiếu ảnh),
**không vượt phạm vi tuần**, không còn writelines/⇔/"chuyển vế", lớp 6 dùng × đúng luật.

| Đối tượng | check-tm | validate (không FAST) | check-de | Kết luận |
|---|---|---|---|---|
| 6C (TM 7 buổi, phiếu 1 t4, KT) | qua, 4 cảnh báo cân giờ | qua; ⚠ TH 57%, VD 0% (chuẩn 40-40-20) | qua | Đạt có điều kiện |
| 6B (TM 6 ca, phiếu 1 t5, KT t11) | qua, 5 cảnh báo | qua; ⚠ NB 29% / TH 71% / VD 0% (đề xuất 15-50-35) | qua | Đạt có điều kiện (chờ Thầy về tỉ lệ) |
| 8C (TM 5 buổi rate gốc, phiếu 1 t4, KT) | qua, 2 cảnh báo (P5) | qua sạch | qua | Không đạt (lỗi hình BTVN 11) |
| 8B (TM 5 ca 30-45-25, phiếu 1 t4) | qua sạch | qua sạch | — (khong_kiem_tra) | Không đạt (hình + nhãn VD + "lớp 8C") |

## 1. CHẶN (sai đề / đáp án / phạm vi)

1. **Hình SGK 1.22 không khớp đề** — `lop-8/dai-so/lop-c/.../phieu-1-tuan04-don-thuc-da-thuc.json` BTVN 11 và
   `lop-8/dai-so/lop-b/.../phieu-1-tuan04-don-thuc-da-thuc.json` BTVN 21.
   Đề: hình vuông cạnh $2{,}5y$, cắt hình tròn **bán kính $y$**. TikZ: `\draw (3.25,1.25) circle (1.25)` trong hình vuông
   cạnh 2.5 ⇒ đường tròn nội tiếp, bán kính vẽ $=1{,}25y$, chạm cả 4 cạnh (thấy rõ trên PDF HS 8C tr.8, 8B tr.12).
   SGK Hình 1.2 tr.18 vẽ đường tròn lớn KHÔNG chạm đáy. Lời giải vẫn đúng ($\pi y^2$) nhưng hình nói khác đề — loại lỗi Thầy từng bác.
   **Sửa:** `circle (1)` (tâm giữ ở (3.25,1.25) hoặc hạ xuống (3.25,1.1)) cho đúng tỉ lệ bán kính $y$ = 1, cạnh $2{,}5y$ = 2,5.

Không phát hiện đề chép sai, đáp án sai hay kiến thức vượt tuần (xem §5).

## 2. NÊN SỬA

### 2a. Band theo quy ước VD mới (tiêu chí bổ sung)
2. **8B Bài 22 a) gắn [VD] sai** — "Cách 1: tổng diện tích hai hình chữ nhật ABCD và EFGC" = $4xy + 3xy = 7xy$, 3 phép tính
   trực tiếp, không biến đổi ⇒ theo luật 16/10 là **TH**. Chỉ b) (phải suy $HD=GF$, $DG=DC+CG$, $HA=HD-AD$, ≥4 bước) mới là VD.
   Sau khi sửa nhãn, 8B phiếu 1 chỉ còn 1 câu VD trên lớp ⇒ chạy lại check-tm/validate xem tỉ lệ 25% còn đủ không.
3. Các nhãn khác đã đúng quy ước mới: bác Hoa, kẹo, 1.11, 1.32, 1.16 (lớp 6) = TH; nho/dưa hấu, chôm chôm giảm 10%,
   vở-bút (lớp 8) = TH; 8C Bài 11 (1.7) và BTVN 11/21 (1.22, 4 bước + nhận dạng bậc) = VD chấp nhận được.
   KT: 6C Câu 5d, 6B Câu 5c/6b/6c/8, 8C Câu 11b/13b = VD hợp lệ (≥4 bước hoặc có biến đổi).

### 2b. Nội dung / trình bày
4. **8B mở bài ghi "lớp 8C"** — 8B `stages[0]` opener: "Cuối tuần, lớp 8C đặt đồ…". Sửa thành "lớp em" hoặc "lớp 8B".
5. **Chữ "Ta có" dính câu viết hoa** (văn lỗi, lộ trên bản GV):
   8C Bài 11 "Ta có Cách 1:", BTVN 10 "Ta có Khối lượng", BTVN 11 "Ta có Diện tích";
   8B Bài 21a "Ta có Khối lượng", BTVN 20 "Ta có Số tiền", BTVN 21 "Ta có Diện tích". Bỏ "Ta có" ở các dòng này.
6. **Ví dụ không dẫn đúng dạng bài sau nó** — 8C Ví dụ 5 (bài toán mở đầu: gạo/mì, lập biểu thức tiền) đặt ngay trước
   Bài 11 (diện tích hình ghép 1.7); trên lớp 8C không còn bài lập biểu thức tiền nào ⇒ ví dụ mồ côi.
   **Sửa:** thay bằng ví dụ diện tích hình ghép (như 8B Ví dụ 7 – Hình 1.1, KÈM HÌNH) hoặc đưa Ví dụ 5 lên trước BTVN 10.
7. **8B Ví dụ 7 dựa vào "SGK Hình 1.1 tr.11" nhưng phiếu không có hình** — HS không có SGK trên bàn. Thêm TikZ tam giác
   vuông + 2 hình vuông dựng ngoài (theo Hình 1.1), bỏ chữ "(SGK Hình 1.1 tr.11)".
8. **Quy trình chép nhầm** — 8C BTVN 11 và 8B BTVN 21 (SGK 1.22, chỉ một cách): bước cuối "làm cách thứ hai để kiểm tra lại"
   chép từ bài 1.7. Sửa thành "Kết luận "Vậy …" kèm đơn vị; đa thức bậc mấy?".
9. **Ghi chú GV đánh số sai** (in ra bản Đáp án GV, hộp "Mẹo sư phạm"):
   6C `practice2.teacher_note`: "Bài 10 HS nối … XIIX" → **Bài 11**; "Bài 11 đổi từng số La Mã" → **Bài 12**.
   6B `practice2.teacher_note`: "Ví dụ 8 và Bài 13: chữ số hàng nghìn" — Ví dụ 8 là số ba chữ số ⇒ "hàng cao nhất".
10. **TM ↔ phiếu lệch số ví dụ**: 8C TM phiếu 1 khai `vidu` tổng 7 (dòng r1–r4, r6, r7, r9) nhưng phiếu có 5 ví dụ
    (r2 bậc đơn thức, r7 thu gọn đa thức + giá trị không có ví dụ riêng); 8B TM khai 8, phiếu có 7 (r4 bậc đơn thức không có ví dụ).
    6C (7/7) và 6B (8/8) khớp. spec_gate không soi ví dụ nên không báo.

### 2c. Cân bằng / cấu trúc
11. **Tầng B gần như bản sao tầng C** (Thầy chốt 15/10: "B soạn RIÊNG, không phải B = C + …"):
    - 6B: 23/33 mục (bài + ví dụ) trùng ≥80% chữ với 6C (Ví dụ 1,3,4,5,6,7,8; Bài 2,3,5,6,7,10,11,12; BTVN 2–9).
    - 8B ⊃ 8C: 26/27 mục của 8C có nguyên văn trong 8B (Ví dụ 1–5, Bài 1–11, BTVN 1,3–9,11); 8B chỉ thêm NB.
    Hai lớp khác học sinh nên không sai luật cứng, nhưng rủi ro Thầy bác "phiếu là bản sao" cao. Đề xuất: B thay nửa số bài NB/TH
    bằng câu khác cùng dạng từ kho (hồ sơ chương còn 135 câu dự phòng lớp 6, 101 câu lớp 8).
12. **8B nhiều NB gấp đôi 8C**: 8B phiếu 1 = 33 NB / 8 TH / 2 VD (rate NB 0,5′ cũ); 8C = 15 / 4 / 1 (rate gốc). Lý do Thầy
    đổi 8C ("rate 0,5′ đẻ ra 44 NB/buổi") áp nguyên cho 8B — xem Câu hỏi 1.
13. **Phiếu 1 lớp 6 không có câu VD** (bài cấu tạo số đã hạ TH đúng luật) ⇒ cảnh báo duration_gate:
    6C TH 57% / VD 0% (chuẩn 40-40-20); 6B NB 29% / TH 71% / VD 0% (đề xuất 15-50-35, ghi chú config đã nhận "Ca 1 bản chất không VD").
    Cần Thầy chấp nhận ngoại lệ buổi 1 hoặc thêm 1 bài VD thật (Câu hỏi 2).
14. Cảnh báo cân giờ ở các phiếu sau (chưa soạn): 6C P5 (NB 53%, VD 0%), 6B P5 (TH 32%, VD+VDC 53%), 8C P5 (TH 60%, VD 0%).

### 2d. PDF (render toàn bộ trang Phiếu HS ở 50 dpi + mẫu GV/slide)
Nhãn hộp đích đúng "★ ĐÍCH ĐỀ KIỂM TRA" ở cả 4 phiếu; không thấy chữ đè chữ, ô trống hiển thị đủ, không tràn lề.
Lỗi ngắt trang / trang phí:
15. 8C (8 tr.): BTVN 11 — đề ở cuối tr.7, **hình + quy trình sang tr.8**, tr.8 trống ~70%; Bài 10 a) tr.4, b) tr.5.
16. 8B (12 tr.): BTVN 14 trắc nghiệm — đề cuối tr.10, **4 phương án sang tr.11**; Bài 9 a) tr.3, b) tr.4; tr.8 trống ~40%.
17. 6B (9 tr.): BTVN 12 (cây sào) bị **cắt giữa câu** "…bạn Cường cao 148 | cm." sang tr.9, tr.9 trống ~85%; tr.5 trống ~25%.
18. 6C (9 tr.): gợi ý của BTVN 15 tách sang tr.9 (tr.9 trống ~70%); tr.6 trống ~25%.
Đề xuất: thêm ngắt dòng/đổi thứ tự BTVN để khối đề + phương án/hình/quy trình đi liền (KHÔNG dùng `\needspace`).

## 3. GỢI Ý
19. Ghi nguồn rõ năm: 6C Bài 5a, 6B Bài 1 "(Đề giữa kì I, THCS Nghĩa Tân)" → "Nghĩa Tân 2023-2024" (kho có 3 đề Nghĩa Tân);
    câu đã chế (6C Bài 5a hỏi số phần tử, 6B Ví dụ 1 theo Phú Châu, Ví dụ 4 theo Chúc Sơn) nên ghi "(phỏng theo …)".
20. 6C TM phiếu 1 dòng r5 (La Mã): `source_refs` có Ngô Gia Tự, Phú Châu nhưng phiếu dùng Thanh Am 2024 C2 (BTVN 9) — bổ sung.
21. 6B Bài 8 a), b): phương án TN viết liền trong đề ("A. 24 826; B. …") — khác mọi câu TN khác (dùng `options`); nên tách.
22. Đề KT 6B và 6C trùng 3 câu (Phúc Lợi $4\cdot 3^2-75:5^2$, Ngô Gia Tự $300:[80-(10+5\cdot 3^2)]-9$, Phúc Lợi $3x+27=45$):
    khác lớp nên chấp nhận được, nhưng nếu một HS chuyển tầng sẽ gặp lại đề.
23. 6B BTVN 12 lời giải "Cường lại cho C … là sai" — hơi văn nói; viết "Cường cho C ứng với chiều cao của Cường là sai vì …".
24. 8B dùng C1-72 (Vạn Phúc C5) ở BTVN 11 — câu 8C TM giữ riêng cho đề KT 8C; khác lớp, chỉ lưu ý.
25. 6C TM phiếu 3 (tuần 6) có dòng VD "tìm $x$ ở số mũ" — hồ sơ chương Câu hỏi 6 (dạy ngay tuần 6 hay để tuần 13) chưa có Thầy trả lời.

## 4. Câu hỏi cho Thầy
1. 8B có chuyển sang rate gốc như 8C không? Hiện 8B 33 NB/buổi, 8C 15 NB/buổi (tầng giỏi lại nhiều câu dễ hơn).
2. Buổi 1 chương I lớp 6 (tập hợp, ghi số, thứ tự) không có bài VD thật: chấp nhận buổi này lệch tỉ lệ (C: 40-60-0, B: 29-71-0)
   hay buộc thêm 1 bài VD (ví dụ cấu tạo số $\overline{19ab}$ — nhưng đó là VDC, Nghĩa Tân minh hoạ)?
3. Tầng B và C trùng 60–95% bài ở cùng buổi — Thầy có chấp nhận, hay yêu cầu B dùng bộ đề khác?
4. 6B tỉ lệ đề xuất 15-50-35 (config ghi "chờ Thầy") — xin chốt con số.

## 5. Bằng chứng đã soát

**Đáp án** — giải lại toàn bộ 4 phiếu + 3 đề KT; SymPy kiểm 40+ phép tính (thu gọn, bậc bằng `Poly.total_degree`, giá trị,
tìm $x$, tổng luỹ thừa $\sum_{k=0}^{122}2^k = 2^{123}-1$, 3 825 000, 416 000, 9 990, 492, 2 046/1 357, 909 090…): **0 sai**.

**Nguồn — đối chiếu ảnh** (pdftoppm 70–80 dpi, đọc mắt):
- SGK 6 T1 tr.7–14, 21: 1.1–1.6, 1.8–1.13, 1.15, 1.16, 1.31, 1.32, LT2, LT3, HĐ2, Luyện tập (34 604), Vận dụng (bác Hoa, sáng/chiều/tối),
  câu hỏi tr.11 (14, 27, XVI, XXII), câu hỏi tr.14 — khớp. (6C ≥14 bài, 6B ≥12 bài.)
- Đề lớp 6: Tam Hiệp 25 C1, Ban Mai 24 B6, Mễ Trì 23 C1, Lương Thế Vinh 25 C2, Nghĩa Tân 23 C2, Chúc Sơn 25 C3, Đa Trí Tuệ 25 C1–C3 — khớp.
- SGK 8 T1 tr.5–14, 18: Bài toán mở đầu, Tranh luận tr.6 & tr.14, 1.1–1.13, LT1 tr.12, Vận dụng tr.12, Hình 1.1, 1.22 — khớp chữ
  (lỗi duy nhất: hình 1.22 vẽ lại sai, mục 1). (8C 14/27 mục, 8B ≥15 mục.)
- Đề lớp 8: Bát Tràng 25 C1/C2/C4/C6, Tam Hiệp 25 C1/C2/B3, Chúc Sơn 25 C1–C4, Vạn Phúc TT 24 C5/B3, Nguyễn Công Trứ 24 B1/B4,
  Nguyễn Trãi 25 B1.2 — khớp số liệu, dấu, phương án.

**Phạm vi** — tiến độ `config/tien_do/{B,C}-lop-{6,8}.json`: 6C t4 & 6B t5 = Bài 1–3; 8B/8C t4 = Bài 1–2. Phiếu chỉ dùng tập hợp,
ghi số, thứ tự, số chẵn/lẻ, La Mã (lớp 6) và đơn thức/đa thức, căn, $\pi$ (lớp 8, nền lớp 5–7). Lớp 8 không có HĐT, đặt nhân tử chung,
$(a\pm b)^2$; mở bài $40(x+y)$ là phân phối lớp 7. Đề KT 8C có $(3-x)(x+3)$ — tích có dáng HĐT, được phép theo luật 15/10.

**Trình bày** — không ⇔/"Do đó"/"Mặt khác"/"chuyển vế"/writelines/`\needspace`; lớp 6 không còn `\cdot` (dùng ×); mọi Ví dụ là bài
điền khuyết ≥2 ô, dòng "Vậy" có ô; TH có gợi ý; VD tầng B có quy trình.

**Trùng đề KT ↔ phiếu** — rà nguồn cả 6/7 phiếu trong TM với câu trong đề KT: không trùng ý (chỉ trùng trường, khác câu/ý).
8C phiếu không dùng 13 câu TM giữ riêng cho KT.
