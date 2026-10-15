# Chứng minh hệ thức tích bằng tam giác đồng dạng

**PHIẾU 4 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 16 (LUYỆN TẬP)  ·  Lớp 9 • Hình học  ·  Tầng C**

`phieu-4-chung-minh-he-thuc-tich-bang-dong-dang`  ·  nguồn: `inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json`

---

## Chặng 1 · Khởi động / Ôn lại — Khám phá

**Hai tích bằng nhau — trùng hợp hay có lí do?**

> **[note]** Tam giác $ABO$ vuông tại $B$ có $AB = 6$ cm, $AO = 10$ cm, đường cao $BH$ và $AH = 3{,}6$ cm (Hình 1).
> 
> **a)** Tính $AB^2$ và $AH \cdot AO$. Em có nhận xét gì?
> 
> **b)** Hai tam giác vuông $AHB$ và $ABO$ có chung góc nào?
> 
> **c)** Hai tam giác đó có quan hệ gì? Viết các tỉ số cạnh tương ứng.

> 👩‍🏫 **Ghi chú cho GV.** Cho HS tính hai tích bằng số trước rồi mới hỏi \textquotedblleft vì sao bằng nhau\textquotedblright. Câu b dẫn thẳng vào trường hợp đồng dạng g.g của hai tam giác vuông (Lớp 8) — công cụ DUY NHẤT của buổi này, vì hệ thức lượng đã giảm tải, HS không được dùng thẳng.

---

## Chặng 2 · Khái niệm — Kiến thức cần nhớ

1. Nhắc lại (Lớp 8): hai tam giác vuông đồng dạng

*(block `deflist` — xem JSON)*

🖼 *[hình vẽ TikZ — $\triangle AHB$ và $\triangle ABO$ vuông, chung góc $A$]*

2. Ba bước chứng minh một đẳng thức tích

*(block `deflist` — xem JSON)*

3. Hai hệ thức trong hình hai tiếp tuyến

Với $AO \perp BC$ tại $H$ ($AO$ là đường trung trực của $BC$) và $AB \perp OB$ tại $B$ ($AB$ là tiếp tuyến):

$\triangle AHB \backsim \triangle ABO$ (g.g, chung góc $A$) $\Rightarrow AB^2 = AH \cdot AO$.

$\triangle OHB \backsim \triangle OBA$ (g.g, chung góc $O$) $\Rightarrow OB^2 = OH \cdot OA$, tức $OH \cdot OA = R^2$.

🖼 *[hình vẽ TikZ — $AO \perp BC$ tại $H$, $AB \perp OB$ tại $B$]*

4. Cát tuyến đi qua đầu đường kính

Vẽ đường kính $BD$, $AD$ cắt $(O)$ tại $E$.

$\triangle BED$ có $EO$ là đường trung tuyến ($O$ là trung điểm của $BD$) và $EO = \dfrac{BD}{2}$ (bán kính bằng nửa đường kính) nên $\triangle BED$ vuông tại $E$ $\Rightarrow BE \perp AD$.

$\triangle AEB \backsim \triangle ABD$ (g.g, chung góc $A$) $\Rightarrow AB^2 = AE \cdot AD$.

Kết hợp với $AB^2 = AH \cdot AO$ (mục 3): $AE \cdot AD = AH \cdot AO$.

🖼 *[hình vẽ TikZ — $BD$ là đường kính, $BE \perp AD$ tại $E$]*

> 👩‍🏫 **Ghi chú cho GV.** Hệ thức lượng trong tam giác vuông đã GIẢM TẢI: mọi đẳng thức tích phải chứng minh qua hai tam giác đồng dạng, đúng ba bước ở mục 2. Mục 3, 4 là các ý b quen thuộc của Câu IV.2 (Lý Thánh Tông, Ngọc Thụy, Phúc Đồng, Dịch Vọng).

---

## Chặng 3 · Luyện tập 1 — Luyện tập 1

> **[example]** **Ví dụ 1.** Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$ (Hình 2). Chứng minh $\triangle HBA \backsim \triangle ABC$.
> 
> {\bfseriesLời giải}
> 
> Xét $\triangle HBA$ và $\triangle ABC$ có:
> 
> $\widehat{BHA} = \widehat{BAC} = $;
> 
> $\widehat{B}$ .
> 
> Vậy $\triangle HBA \backsim \triangle ABC$ ().

**Bài 1.**  `★ NB · trên lớp · có hình sẵn`

Trên Hình 3, tam giác $MNP$ vuông tại $M$, đường cao $MK$. Điền vào chỗ chấm:

a) [NB] $\triangle KNM$ và $\triangle MNP$ có chung góc ………….

b) [NB] $\widehat{MKN} = \widehat{NMP} = ………………$.

c) [NB] $\Rightarrow \triangle KNM \backsim \triangle ………………$ (g.g).

**Bài 2.**  `★ NB · trên lớp · có hình sẵn`

Điền vào chỗ chấm để đổi đẳng thức tích thành tỉ số (bước 1):

a) [NB] $AB^2 = AH \cdot AO \Leftarrow \dfrac{AH}{AB} = \dfrac{…………}{AO}$.

b) [NB] $OB^2 = OH \cdot OA \Leftarrow \dfrac{OH}{OB} = \dfrac{OB}{…………}$.

c) [NB] $AE \cdot AD = AB^2 \Leftarrow \dfrac{AE}{AB} = \dfrac{…………}{AD}$.

**Bài 3.**  `★ NB · trên lớp · có hình sẵn`

Trên Hình 4, $AB$, $AC$ là hai tiếp tuyến của $(O)$; $AO \perp BC$ tại $H$ (đã chứng minh); $BD$ là đường kính, $AD$ cắt $(O)$ tại $E$. Điền vào chỗ chấm để chứng minh $\triangle AHB \backsim \triangle ABO$:

a) [NB] $AO \perp BC$ tại $H$ $\Rightarrow \widehat{AHB} = ………………$.

b) [NB] $AB$ là tiếp tuyến tại $B$ $\Rightarrow \widehat{ABO} = ………………$.

c) [NB] Xét $\triangle AHB$ và $\triangle ABO$: $\widehat{AHB} = \widehat{ABO}$, góc ……………… chung $\Rightarrow \triangle AHB \backsim \triangle ABO$ (…………).

> **[example]** **Ví dụ 2.** Tam giác $DEF$ vuông tại $E$, đường cao $EG$ (Hình 5). Biết $\triangle DGE \backsim \triangle DEF$, chứng minh $DE^2 = DG \cdot DF$.
> 
> {\bfseriesLời giải}
> 
> $\triangle DGE \backsim \triangle DEF$ $\Rightarrow \dfrac{DG}{DE} = $ (tỉ số cạnh tương ứng).
> 
> $\Rightarrow  = DG \cdot DF$ (nhân chéo).
> 
> Vậy $DE^2 = $.

**Bài 4.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 4. Điền vào chỗ chấm:

a) [NB] $\triangle AHB \backsim \triangle ABO$ $\Rightarrow \dfrac{AH}{AB} = \dfrac{…………}{…………}$.

b) [NB] Nhân chéo: $AB^2 = …………………………$.

c) [NB] $\triangle AEB \backsim \triangle ABD$ $\Rightarrow \dfrac{AE}{AB} = \dfrac{AB}{…………} \Rightarrow AB^2 = …………………………$.

**Bài 5.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 4. Điền vào chỗ chấm để chứng minh $OH \cdot OA = R^2$:

a) [NB] Xét $\triangle OHB$ và $\triangle OBA$: $\widehat{OHB} = \widehat{OBA} = ………………$, góc ……………… chung.

b) [NB] $\Rightarrow \triangle OHB \backsim \triangle OBA$ (g.g) $\Rightarrow \dfrac{OH}{OB} = \dfrac{…………}{…………}$.

c) [NB] $\Rightarrow OH \cdot OA = ……………… = R^2$.

**Bài 6.**  `★ NB · trên lớp · có hình sẵn`

Vẽ lại Hình 4 vào vở rồi điền vào chỗ chấm:

a) [NB] Đánh dấu góc vuông tại $B$ của $\triangle ABD$ ($AB$ là tiếp tuyến tại $B$).

b) [NB] $O$ là trung điểm của đường kính $BD$ $\Rightarrow EO$ là đường ………………………… của $\triangle BED$.

c) [NB] $\triangle BED$ có đường trung tuyến $EO = \dfrac{BD}{2}$ (bán kính bằng nửa đường kính) $\Rightarrow \triangle BED$ vuông tại ………… $\Rightarrow BE \perp …………$.

**Bài 7.**  `★ NB · trên lớp · có hình sẵn`

Trên Hình 4, cho $R = 6$ cm, $OA = 10$ cm; đã chứng minh $AB^2 = AH \cdot AO$ và $OH \cdot OA = R^2$. Điền vào chỗ chấm:

a) [NB] Theo định lí Pythagore, $AB = 8$ cm $\Rightarrow AH = \dfrac{AB^2}{AO} = ……………… = …………$ cm.

b) [NB] $OH = \dfrac{R^2}{OA} = ……………… = …………$ cm.

> 👩‍🏫 **Ghi chú cho GV.** 20 câu nhận biết, chẻ đúng ba bước ở mục 2. Bài 3 – 5 cùng một hình: HS điền xong là có trọn bản chứng minh $AB^2 = AH \cdot AO$ và $OH \cdot OA = R^2$ để chép vào vở. Bài 7: nhắc HS kiểm tra lại $AH + OH = AO$.

---

## Chặng 4 · Luyện tập 2 — Luyện tập 2

> **[example]** **Ví dụ 3.** Cho tam giác $ABO$ vuông tại $B$, đường cao $BH$ (Hình 6). Chứng minh $OB^2 = OH \cdot OA$.
> 
> {\bfseriesLời giải}
> 
> Xét $\triangle OHB$ và $\triangle OBA$ có:
> 
> $\widehat{OHB} = \widehat{OBA} = $; \ $\widehat{O}$ chung.
> 
> $\Rightarrow \triangle OHB \backsim \triangle OBA$ ().
> 
> $\Rightarrow \dfrac{OH}{OB} = $.
> 
> Vậy $OB^2 = $.

**Bài 8.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ nằm ngoài $(O)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm); $AO$ cắt $BC$ tại $H$. Biết $AO \perp BC$ tại $H$, chứng minh $AB^2 = AH \cdot AO$.

> 💡 Đổi đẳng thức thành tỉ số. Tỉ số đó gợi ý hai tam giác nào? / Hai tam giác đó có những góc nào bằng nhau? Vì sao?

> **[example]** **Ví dụ 4.** Cho đường tròn $(O)$ đường kính $AB$, tiếp tuyến $Ax$ tại $A$. Lấy điểm $C$ trên $Ax$; $CB$ cắt $(O)$ tại $K$ ($K \ne B$) (Hình 7). Chứng minh $\triangle AKB$ vuông và $BK \cdot BC = AB^2$.
> 
> {\bfseriesLời giải}
> 
> $\triangle AKB$ có $KO$ là đường trung tuyến ($O$ là trung điểm của $AB$) và $KO = $ (bán kính bằng nửa đường kính) nên $\triangle AKB$ vuông tại $K$.
> 
> $Ax$ là tiếp tuyến tại $A$ $\Rightarrow \widehat{BAC} = 90^\circ$.
> 
> Xét $\triangle BKA$ và $\triangle BAC$: $\widehat{BKA} = \widehat{BAC} = 90^\circ$, $\widehat{B}$ chung.
> 
> $\Rightarrow \triangle BKA \backsim \triangle BAC$ () $\Rightarrow \dfrac{BK}{BA} = $.
> 
> Vậy $\triangle AKB$ vuông tại $K$ và $BK \cdot BC = $.

**Bài 9.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ nằm ngoài $(O)$ kẻ tiếp tuyến $AB$ ($B$ là tiếp điểm), vẽ đường kính $BD$; $AD$ cắt $(O)$ tại $E$ ($E \ne D$) (Hình 8). Chứng minh $AE \cdot AD = AB^2$.

> 💡 Tam giác $BED$ là tam giác gì? Căn cứ vào trung tuyến nào? / Đẳng thức cần chứng minh gợi ý cặp tam giác nào? Chúng có chung góc nào?

> **[example]** **Ví dụ 5.** Hai tiếp tuyến $AB$, $AC$ của $(O; 9\text{ cm})$ cắt nhau tại $A$ với $OA = 15$ cm; $AO \perp BC$ tại $H$ (Hình 9). Biết $AB^2 = AH \cdot AO$ và $OH \cdot OA = R^2$ (đã chứng minh), tính $AB$, $AH$ và $OH$.
> 
> {\bfseriesLời giải}
> 
> Xét $\triangle ABO$ vuông tại $B$, theo định lí Pythagore:
> 
> $AB^2 = OA^2 - OB^2 = 15^2 - 9^2 =  \Rightarrow AB = $ (cm).
> 
> $AH = \dfrac{AB^2}{AO} =  = $ (cm).
> 
> $OH = \dfrac{R^2}{OA} = \dfrac{81}{15} = $ (cm).
> 
> Vậy $AB = $ cm, $AH = $ cm, $OH = $ cm.

**Bài 10.**  `★★ TH · trên lớp`

[TH] Với hình của Bài 8 ($AO \perp BC$ tại trung điểm $H$ của $BC$), cho $R = 8$ cm, $OA = 10$ cm. Tính $AB$, $AH$, $BH$ và $BC$.

> 💡 Tính $AB$ trong tam giác vuông nào? Đẳng thức nào ở Bài 8 cho ngay $AH$? / Có $AB$, $AH$ rồi thì $BH$ nằm trong tam giác vuông nào? $BC$ gấp mấy lần $BH$?

> **[example]** **Ví dụ 6.** Từ $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$; $AO$ cắt $BC$ tại $H$; tia $AO$ cắt $(O)$ tại $M$, $N$ ($M$ nằm giữa $A$ và $N$) (Hình 10). Biết $AB^2 = AH \cdot AO$, chứng minh $AM \cdot AN = AH \cdot AO$.
> 
> {\bfseriesLời giải}
> 
> $M$, $N$ thuộc tia $AO$, $OM = ON = R$ $\Rightarrow AM = AO - R$, $AN = AO + R$.
> 
> $\Rightarrow AM \cdot AN = (AO - R)(AO + R) = $.
> 
> Xét $\triangle ABO$ vuông tại $B$, theo định lí Pythagore: $AO^2 - OB^2 = $.
> 
> $\Rightarrow AM \cdot AN = AB^2$, mà $AB^2 = AH \cdot AO$ (gt).
> 
> Vậy $AM \cdot AN = $.

**Bài 11.**  `★★★ VD · trên lớp`

[VD] Từ điểm $A$ nằm ngoài $(O)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm); $AO$ cắt $BC$ tại $H$. Vẽ đường kính $BD$ của $(O)$; $AD$ cắt $(O)$ tại $E$ ($E \ne D$) (Hình 11). Chứng minh $AE \cdot AD = AH \cdot AO$.

> 👩‍🏫 **Ghi chú cho GV.** Bài 8 là ý a đề Lý Thánh Tông, Bài 9 là cấu hình đề Phúc Đồng, Bài 11 là ý b quen thuộc \textquotedblleft $AE \cdot AD = AH \cdot AO$\textquotedblright. Bắt HS viết đủ \textquotedblleft Xét … và … có\textquotedblright, hai cặp góc kèm lí do, rồi mới tỉ số — không chấp nhận dùng thẳng hệ thức lượng.

---

## Chặng 5 · Tổng kết — Sơ đồ tư duy

🧠 **Sơ đồ tư duy — ĐẲNG THỨC TÍCH**
  - BA BƯỚC
    - B1. Đổi tích thành tỉ số
    - B2. Đọc cặp tam giác
    - B3. Đồng dạng g.g $\Rightarrow$ nhân chéo
  - HAI TIẾP TUYẾN
    - $\triangle AHB \backsim \triangle ABO$: $AB^2 = AH \cdot AO$
    - $\triangle OHB \backsim \triangle OBA$: $OH \cdot OA = R^2$
    - Trước đó: chứng minh $AO \perp BC$
  - ĐƯỜNG KÍNH $BD$
    - Trung tuyến $EO = \dfrac{BD}{2}$: $\triangle BED$ vuông
    - $\triangle AEB \backsim \triangle ABD$: $AB^2 = AE \cdot AD$
    - Bắc cầu: $AE \cdot AD = AH \cdot AO$
  - TÍNH ĐỘ DÀI
    - $AB^2 = OA^2 - R^2$
    - $AH = \dfrac{AB^2}{AO}$, $OH = \dfrac{R^2}{OA}$
    - Kiểm tra: $AH + OH = AO$

**BÀI TẬP VỀ NHÀ (Chứng minh hệ thức tích bằng tam giác đồng dạng).**

**BTVN 1.**  `★ NB · BTVN · có hình sẵn`

Tam giác $DEF$ vuông tại $D$, đường cao $DK$. Điền vào chỗ chấm:

a) [NB] $\triangle KED$ và $\triangle DEF$ có chung góc ………….

b) [NB] $\widehat{DKE} = \widehat{EDF} = ………………$.

c) [NB] $\Rightarrow \triangle KED \backsim \triangle ………………$ (g.g).

**BTVN 2.**  `★ NB · BTVN · có hình sẵn`

Điền vào chỗ chấm:

a) [NB] $MA^2 = MK \cdot MO \Leftarrow \dfrac{MK}{MA} = \dfrac{…………}{MO}$.

b) [NB] $OK \cdot OM = OA^2 \Leftarrow \dfrac{OK}{OA} = \dfrac{OA}{…………}$.

**BTVN 3.**  `★ NB · BTVN · có hình sẵn`

Từ $M$ ngoài $(O)$ kẻ hai tiếp tuyến $MA$, $MB$; $MO \perp AB$ tại $K$. Điền vào chỗ chấm:

a) [NB] $\widehat{MKA} = ………………$ vì $MO \perp AB$ tại $K$.

b) [NB] $\widehat{MAO} = ………………$ vì $MA$ là tiếp tuyến tại $A$.

c) [NB] Xét $\triangle MKA$ và $\triangle MAO$: $\widehat{MKA} = \widehat{MAO}$, góc ……………… chung $\Rightarrow \triangle MKA \backsim \triangle MAO$ (…………).

**BTVN 4.**  `★ NB · BTVN · có hình sẵn`

Vẫn với hình ở BTVN 3. Điền vào chỗ chấm:

a) [NB] $\triangle MKA \backsim \triangle MAO \Rightarrow \dfrac{MK}{MA} = \dfrac{…………}{…………}$.

b) [NB] $\Rightarrow MA^2 = …………………………$.

c) [NB] Biết $MA = 4$ cm, $MO = 5$ cm $\Rightarrow MK = \dfrac{MA^2}{MO} = …………$ cm.

**BTVN 5.**  `★ NB · BTVN · có hình sẵn`

Vẫn với hình ở BTVN 3. Điền vào chỗ chấm để chứng minh $OK \cdot OM = R^2$:

a) [NB] Xét $\triangle OKA$ và $\triangle OAM$: $\widehat{OKA} = \widehat{OAM} = ………………$, góc ……………… chung.

b) [NB] $\Rightarrow \triangle OKA \backsim \triangle OAM \Rightarrow \dfrac{OK}{OA} = \dfrac{…………}{…………}$.

c) [NB] $\Rightarrow OK \cdot OM = ……………… = R^2$.

**BTVN 6.**  `★ NB · BTVN · có hình sẵn`

Vẽ lại Hình 4 vào vở. Điền vào chỗ chấm:

a) [NB] $O$ là trung điểm của đường kính $BD$ $\Rightarrow EO$ là đường ………………………… của $\triangle BED$ và $EO = R = ………………$.

b) [NB] $\triangle BED$ có đường trung tuyến $EO$ bằng nửa cạnh $BD$ $\Rightarrow \triangle BED$ vuông tại ………….

**BTVN 7.**  `★ NB · BTVN · có hình sẵn`

Hai tiếp tuyến $AB$, $AC$ của $(O; 12\text{ cm})$ cắt nhau tại $A$, $OA = 20$ cm, $AO \perp BC$ tại $H$; đã chứng minh $AB^2 = AH \cdot AO$, $OH \cdot OA = R^2$. Điền vào chỗ chấm:

a) [NB] $AB = \sqrt{20^2 - 12^2} = …………$ cm $\Rightarrow AH = ………………$ cm.

b) [NB] $OH = \dfrac{12^2}{20} = ………………$ cm.

**BTVN 8.**  `★★ TH · BTVN`

[TH] Từ điểm $M$ nằm ngoài $(O; R)$ kẻ hai tiếp tuyến $MA$, $MB$ ($A$, $B$ là tiếp điểm); $MO$ cắt $AB$ tại $K$. Chứng minh $MO \perp AB$ tại $K$ rồi chứng minh $MA^2 = MK \cdot MO$.

> 💡 Hai điểm nào cùng cách đều $A$ và $B$? / Đổi đẳng thức thành tỉ số rồi đọc ra cặp tam giác.

**BTVN 9.**  `★★ TH · BTVN`

[TH] Từ điểm $A$ nằm ngoài $(O)$ kẻ tiếp tuyến $AC$ ($C$ là tiếp điểm), vẽ đường kính $CD$; $AD$ cắt $(O)$ tại $F$ ($F \ne D$). Chứng minh $AF \cdot AD = AC^2$.

> 💡 Tam giác $CFD$ là tam giác gì? Vì sao? / Cặp tam giác nào cho tỉ số $\dfrac{AF}{AC} = \dfrac{AC}{AD}$?

**BTVN 10.**  `★★ TH · BTVN`

[TH] Cho đường tròn $(O; 6\text{ cm})$, điểm $A$ cách $O$ là $10$ cm. Kẻ hai tiếp tuyến $AB$, $AC$; gọi $H$ là giao điểm của $AO$ và $BC$ (đã biết $AO \perp BC$ tại $H$ và $H$ là trung điểm của $BC$).

a) Chứng minh $AB^2 = AH \cdot AO$.

b) Tính $AH$ và độ dài dây $BC$.

> 💡 Chứng minh đẳng thức như Bài 8. / $BH$ nằm trong tam giác vuông nào có hai cạnh đã biết?

**BTVN 11.**  `★★★ VD · BTVN`

[VD] Từ điểm $M$ nằm ngoài $(O)$ kẻ hai tiếp tuyến $MA$, $MB$ ($A$, $B$ là tiếp điểm); $MO$ cắt $AB$ tại $K$. Vẽ đường kính $AD$; $MD$ cắt $(O)$ tại $E$ ($E \ne D$). Chứng minh $ME \cdot MD = MK \cdot MO$.

> 👩‍🏫 **Ghi chú cho GV.** BTVN 8, 10 là ý b đề thật dạng \textquotedblleft $AB^2 = AH \cdot AO$\textquotedblright{} (Lý Thánh Tông, Ngọc Thụy); BTVN 11 là bài vận dụng đổi tên điểm của Bài 11 — chữa đầu buổi 5.

---
