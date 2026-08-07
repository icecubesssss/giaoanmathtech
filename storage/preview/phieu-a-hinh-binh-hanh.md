# Hình bình hành

**HÌNH HỌC 8 — PHIẾU A: HÌNH BÌNH HÀNH  ·  Lớp 8  ·  Tầng B**

`phieu-a-hinh-binh-hanh`  ·  nguồn: `inputs/seeds/lop-8/hinh-hoc/lop-b/tuan07-hinh-binh-hanh/phieu-a-hinh-binh-hanh.json`

---

## Chặng 1 · Khởi động / Ôn lại — Khám phá

> 🎬 **Mở màn.** Một chiếc cổng rào sắt xếp tự động được cấu tạo bởi các thanh kim loại nối với nhau bằng các khớp động tạo thành các tứ giác $ABCD$.
> 
> Khi người ta kéo co giãn cổng rào, hình dạng các tứ giác $ABCD$ thay đổi nhưng hai thanh chắn đối diện $AB$ và $CD$ luôn giữ song song với nhau và có độ dài không đổi ($AB = CD = 1{,}2\text{ m}$).
> 
> Quan sát hình vẽ và cho biết: Tứ giác $ABCD$ là hình gì? Khi góc $\widehat{A} = 70^\circ$ thì góc $\widehat{B}$ và góc $\widehat{C}$ bằng bao nhiêu độ?

Để giải thích điều này, ta sử dụng tính chất của **Hình bình hành**:

- Các cạnh đối song song và bằng nhau: $AB \parallel CD$, $AD \parallel BC$ và $AB = CD$, $AD = BC$.

- Hai góc kề một cạnh bù nhau: $\widehat{A} + \widehat{B} = 180^\circ \Rightarrow \widehat{B} = 180^\circ - 70^\circ = 110^\circ$.

- Các góc đối bằng nhau: $\widehat{C} = \widehat{A} = 70^\circ$ và $\widehat{D} = \widehat{B} = 110^\circ$.

<details><summary>✅ <b>Lời giải (chỉ có ở bản GV)</b></summary>

Tứ giác $ABCD$ là hình bình hành. Số đo góc $\widehat{B} = 110^\circ$, góc $\widehat{C} = 70^\circ$.

</details>

> 👩‍🏫 **Ghi chú cho GV.** GV hướng dẫn học sinh liên hệ thực tế cổng xếp tự động và khung giá đỡ laptop có cấu trúc hình bình hành khớp động linh hoạt.

---

## Chặng 2 · Khái niệm — Khái niệm

> **[note]** **1. Định nghĩa và Tính chất**
> 
> *a) Định nghĩa*: Hình bình hành là tứ giác có các cạnh đối song song ($AB \parallel CD$ và $AD \parallel BC$).
> 
> *b) Tính chất*: Trong một hình bình hành:
> 
> - Các cạnh đối bằng nhau ($AB = CD$ và $AD = BC$).
> 
> - Các góc đối bằng nhau ($\widehat{A} = \widehat{C}$ và $\widehat{B} = \widehat{D}$).
> 
> - Hai đường chéo cắt nhau tại trung điểm của mỗi đường ($OA = OC$ và $OB = OD$).
> 
> 🖼 *[hình vẽ TikZ]*
> 
> *\itshapeHình 1: Hình bình hành $ABCD$*

> **[note]** **2. 5 Dấu hiệu nhận biết hình bình hành**
> 
> Tứ giác $ABCD$ là hình bình hành khi thỏa mãn một trong các điều kiện:
> 
> - **Dấu hiệu 1**: Tứ giác có các cạnh đối song song là hình bình hành.
> 
> - **Dấu hiệu 2**: Tứ giác có các cạnh đối bằng nhau là hình bình hành.
> 
> - **Dấu hiệu 3**: Tứ giác có hai cạnh đối song song và bằng nhau là hình bình hành (*Thường dùng nhất*).
> 
> - **Dấu hiệu 4**: Tứ giác có các góc đối bằng nhau là hình bình hành.
> 
> - **Dấu hiệu 5**: Tứ giác có hai đường chéo cắt nhau tại trung điểm của mỗi đường là hình bình hành.

> **[example]** **Ví dụ mẫu 1.** Xét hình bình hành $ABCD$. Gọi $E, F$ lần lượt là trung điểm của $AB$ và $CD$. Chứng minh tứ giác $AECF$ là hình bình hành.
> 
> *Lời giải*:
> 
> Vì $ABCD$ là HBH nên $AB \parallel CD$ và $AB = CD$.
> 
> Vì $E$ là trung điểm $AB \Rightarrow AE = \dfrac{1}{2}AB$.
> 
> Vì $F$ là trung điểm $CD \Rightarrow CF = \dfrac{1}{2}CD$.
> 
> Suy ra $AE = CF$. Mặt khác $E \in AB, F \in CD \Rightarrow AE \parallel CF$.
> 
> Tứ giác $AECF$ có $AE \parallel CF$ và $AE = CF \Rightarrow AECF$ là hình bình hành (Dấu hiệu 3).
> 
> 🖼 *[hình vẽ TikZ]*
> 
> *\itshapeHình 2: Tứ giác $AECF$*

> **[trap]** BẪY ĐIỂM: Tứ giác có một cặp cạnh đối song song và một cặp cạnh đối bằng nhau KHÔNG CHẮC LÀ hình bình hành!
> 
> Ví dụ hình thang cân có $AB \parallel CD$ và hai cạnh bên $AD = BC$ bằng nhau nhưng KHÔNG PHẢI là hình bình hành.
> 
> Do đó, muốn áp dụng Dấu hiệu 3 bắt buộc hai cạnh đó phải VỪA SONG SONG VỪA BẰNG NHAU (cùng một cặp cạnh).

<details><summary>✅ <b>Lời giải (chỉ có ở bản GV)</b></summary>

Nắm vững định nghĩa, 3 tính chất và 5 dấu hiệu nhận biết hình bình hành chuẩn SGK Toán 8.

</details>

> 👩‍🏫 **Ghi chú cho GV.** Nhấn mạnh Dấu hiệu 3 (1 cặp cạnh đối vừa song song vừa bằng nhau) và Dấu hiệu 5 (hai đường chéo cắt nhau tại trung điểm) là hai công cụ chứng minh xuất hiện nhiều nhất trong các đề thi giữa kỳ và cuối kỳ.

---

## Chặng 3 · Luyện tập 1 — Luyện tập 1

**Dạng 1: Nhận biết \& Tính toán trên hình vẽ sẵn (Đề thi GKI/CKI)**

**Bài 1.**  `★ NB · trên lớp · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có $\widehat{A} = 110^\circ$ (hình vẽ). Số đo góc đối $\widehat{C}$ bằng:

\par\parbox[t]{0.30\linewidth}{**A.** $110^\circ$}\parbox[t]{0.30\linewidth}{**B.** $70^\circ$}\par\parbox[t]{0.30\linewidth}{**C.** $180^\circ$}\parbox[t]{0.30\linewidth}{**D.** $90^\circ$}\par

*(chừa 0 dòng cho HS viết)*

**Bài 2.**  `★ NB · trên lớp · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có $AB = 8\text{ cm}$ và $AD = 5\text{ cm}$ (hình vẽ). Độ dài $CD$ và $BC$ lần lượt là:

\par\parbox[t]{0.30\linewidth}{**A.** $8\text{ cm}$ và $5\text{ cm}$}\parbox[t]{0.30\linewidth}{**B.** $5\text{ cm}$ và $8\text{ cm}$}\par\parbox[t]{0.30\linewidth}{**C.** $8\text{ cm}$ và $8\text{ cm}$}\parbox[t]{0.30\linewidth}{**D.** $5\text{ cm}$ và $5\text{ cm}$}\par

*(chừa 0 dòng cho HS viết)*

**Bài 3.**  `★ NB · trên lớp · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có hai đường chéo $AC$ và $BD$ cắt nhau tại $O$ (hình vẽ). Biết $AC = 12\text{ cm}, BD = 8\text{ cm}$. Độ dài $OA$ và $OB$ là:

\par\parbox[t]{0.30\linewidth}{**A.** $6\text{ cm}$ và $4\text{ cm}$}\parbox[t]{0.30\linewidth}{**B.** $12\text{ cm}$ và $8\text{ cm}$}\par\parbox[t]{0.30\linewidth}{**C.** $4\text{ cm}$ và $6\text{ cm}$}\parbox[t]{0.30\linewidth}{**D.** $3\text{ cm}$ và $2\text{ cm}$}\par

*(chừa 0 dòng cho HS viết)*

**Bài 4.**  `★ NB · trên lớp · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có $\widehat{A} = 75^\circ$ (hình vẽ). Số đo góc kề $\widehat{B}$ bằng:

\par\parbox[t]{0.30\linewidth}{**A.** $105^\circ$}\parbox[t]{0.30\linewidth}{**B.** $75^\circ$}\par\parbox[t]{0.30\linewidth}{**C.** $180^\circ$}\parbox[t]{0.30\linewidth}{**D.** $15^\circ$}\par

*(chừa 0 dòng cho HS viết)*

**Dạng 2: Khẳng định Đúng/Sai \& Mẫu trình bày điền khuyết**

**Bài 5.**  `★ NB · trên lớp`

Trong các khẳng định sau, chọn Đúng (Đ) hoặc Sai (S):

a) Tứ giác có 2 cặp cạnh đối bằng nhau là hình bình hành. ………

b) Hình thang có 2 cạnh bên song song là hình bình hành. ………

*(chừa 0 dòng cho HS viết)*

**Bài 6.**  `★ NB · trên lớp`

Khẳng định nào sau đây **KHÔNG ĐÚNG** về dấu hiệu nhận biết hình bình hành?

**A.** Tứ giác có các cạnh đối song song là hình bình hành.

**B.** Tứ giác có các cạnh đối bằng nhau là hình bình hành.

**C.** Tứ giác có 1 cặp cạnh đối song song và 1 cặp cạnh đối bằng nhau là hình bình hành.

**D.** Tứ giác có 2 đường chéo cắt nhau tại trung điểm của mỗi đường là hình bình hành.

*(chừa 0 dòng cho HS viết)*

**Dạng 3: Tính toán góc \& Tự luận chứng minh hình bình hành trọng tâm (Đề thi GKI/CKI)**

**Bài 7.**  `★ NB · trên lớp`

Xét hình bình hành $ABCD$ có $\widehat{A} - \widehat{B} = 40^\circ$. Tính số đo các góc $\widehat{A}, \widehat{B}, \widehat{C}, \widehat{D}$ của hình bình hành.

*(chừa 3 dòng cho HS viết)*

**Bài 8.**  `★★ TH · trên lớp`

Xét hình bình hành $ABCD$. Gọi $M, N$ lần lượt là trung điểm của $AB$ và $CD$. Điền vào chỗ trống để hoàn thiện lời giải chứng minh tứ giác $MBND$ là hình bình hành:

*Lời giải*:

- Vì $ABCD$ là hình bình hành nên $AB \parallel CD$ và $AB =$ …………………

- Vì $M$ là trung điểm $AB$ nên $MB = \dfrac{1}{2}AB$.

- Vì $N$ là trung điểm $CD$ nên $ND = \dfrac{1}{2}$ ………………

- Suy ra $MB =$ ……………… Mặt khác $MB \subset AB, ND \subset CD$ nên $MB \parallel$ ………………

- Xét tứ giác $MBND$ có $MB \parallel ND$ và $MB = ND$ $\Rightarrow MBND$ là hình bình hành (theo Dấu hiệu 3: ……………………………………………… ).

*(chừa 0 dòng cho HS viết)*

**Bài 9.**  `★★ TH · trên lớp`

Xét hình bình hành $ABCD$ có $O$ là giao điểm hai đường chéo. Trên đường chéo $BD$ lấy hai điểm $M, N$ sao cho $BM = DN$.

a) Chứng minh $OM = ON$.

b) Chứng minh rằng tứ giác $AMCN$ là hình bình hành.

*(chừa 4 dòng cho HS viết)*

---

## Chặng 4 · Luyện tập 2 — Luyện tập 2

**Bài 10.**  `★★★ VD · trên lớp`

Cho tam giác $ABC$. Gọi $M$ là trung điểm của cạnh $BC$. Trên tia đối của tia $MA$ lấy điểm $D$ sao cho $MD = MA$. Kẻ $AH \perp BC$ tại $H$, trên tia đối của tia $HA$ lấy điểm $E$ sao cho $HE = HA$.

a) Chứng minh tứ giác $ABDC$ là hình bình hành.

b) Chứng minh $BE = CD$ và tứ giác $BCDE$ là hình thang cân.

*(chừa 6 dòng cho HS viết)*

---

## Chặng 5 · Tổng kết — Tổng kết \& BTVN

🧠 **Sơ đồ tư duy — Hình bình hành**
  - Định nghĩa ………………
    - Tứ giác có các cạnh đối song song ($AB \parallel CD, AD \parallel BC$)
  - 3 Tính chất ………………
    - Cạnh đối bằng nhau: $AB = CD, AD = BC$
    - Góc đối bằng nhau: $\widehat{A} = \widehat{C}, \widehat{B} = \widehat{D}$
    - Hai đường chéo cắt nhau tại trung điểm
  - 5 Dấu hiệu ………………
    - Các cạnh đối song song / Các cạnh đối bằng nhau
    - Hai cạnh đối song song và bằng nhau (DH3 - Trọng tâm)
    - Các góc đối bằng nhau / 2 đường chéo cắt nhau tại trung điểm

**BTVN 1.**  `★ NB · BTVN · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có $\widehat{A} = 120^\circ$ (hình vẽ). Số đo góc đối $\widehat{C}$ và góc kề $\widehat{B}$ lần lượt là:

\par\parbox[t]{0.30\linewidth}{**A.** $120^\circ$ và $60^\circ$}\parbox[t]{0.30\linewidth}{**B.** $60^\circ$ và $120^\circ$}\par\parbox[t]{0.30\linewidth}{**C.** $120^\circ$ và $120^\circ$}\parbox[t]{0.30\linewidth}{**D.** $60^\circ$ và $60^\circ$}\par

*(chừa 0 dòng cho HS viết)*

**BTVN 2.**  `★ NB · BTVN · có hình sẵn`

🖼 *[hình kèm đề]*  Cho hình bình hành $ABCD$ có $AB = 10\text{ cm}$ và $BC = 6\text{ cm}$ (hình vẽ). Chu vi của hình bình hành $ABCD$ bằng:

\par\parbox[t]{0.30\linewidth}{**A.** $32\text{ cm}$}\parbox[t]{0.30\linewidth}{**B.** $16\text{ cm}$}\par\parbox[t]{0.30\linewidth}{**C.** $60\text{ cm}$}\parbox[t]{0.30\linewidth}{**D.** $20\text{ cm}$}\par

*(chừa 0 dòng cho HS viết)*

**BTVN 3.**  `★ NB · BTVN`

Trong các khẳng định sau, chọn Đúng (Đ) hoặc Sai (S):

a) Tứ giác có hai đường chéo cắt nhau tại trung điểm mỗi đường là hình bình hành. ………

b) Tứ giác có hai cạnh đối song song và hai cạnh đối còn lại bằng nhau là hình bình hành. ………

*(chừa 0 dòng cho HS viết)*

**BTVN 4.**  `★ NB · BTVN`

Xét hình bình hành $ABCD$ có $\widehat{A} = 2\widehat{B}$. Tính số đo 4 góc $\widehat{A}, \widehat{B}, \widehat{C}, \widehat{D}$ của hình bình hành.

*(chừa 2 dòng cho HS viết)*

**BTVN 5.**  `★★ TH · BTVN`

Xét hình bình hành $ABCD$. Kẻ $AH \perp BD$ tại $H$ và $CK \perp BD$ tại $K$.

a) Chứng minh $AH \parallel CK$ và $\triangle AHB = \triangle CKD$.

b) Chứng minh rằng tứ giác $AHCK$ là hình bình hành.

*(chừa 4 dòng cho HS viết)*

**BTVN 6.**  `★★★ VD · BTVN`

Xét hình bình hành $ABCD$. Gọi $E, F$ lần lượt là hình chiếu vuông góc của $B, D$ trên đường chéo $AC$. Gọi $O$ là giao điểm hai đường chéo $AC$ và $BD$.

a) Chứng minh tứ giác $BEDF$ là hình bình hành.

b) Chứng minh ba điểm $E, O, F$ thẳng hàng.

*(chừa 5 dòng cho HS viết)*

---
