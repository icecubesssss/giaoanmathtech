# Vị trí tương đối của hai đường tròn. Luyện tập chung

**PHIẾU 6 • HÌNH HỌC 9 · CHƯƠNG V — BÀI 17  ·  Lớp 9 • Hình học  ·  Tầng C**

`phieu-6-vi-tri-hai-duong-tron-va-luyen-tap-chung`  ·  nguồn: `inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-6-vi-tri-hai-duong-tron-va-luyen-tap-chung.json`

---

## Chặng 1 · Khởi động / Ôn lại — Khám phá

**Hai bánh xe chạm nhau kiểu nào?**

> **[note]** Hai bánh xe tròn tâm $O$, $O'$ có bán kính $R = 5$ cm và $R' = 3$ cm; $d = OO'$ là khoảng cách giữa hai tâm (Hình 1).
> 
> **a)** Khi $d = 10$ cm, hai bánh xe có chạm nhau không?
> 
> **b)** Đẩy lại gần đến $d = 8$ cm thì hai đường tròn có mấy điểm chung? So sánh $8$ với $5 + 3$.
> 
> **c)** Đẩy tiếp đến $d = 6$ cm thì hai đường tròn có mấy điểm chung?

> 👩‍🏫 **Ghi chú cho GV.** Phần Bài 17 chỉ chạy khoảng 30 phút (Bài 1–4). Thời gian còn lại dành cho khuôn hai tiếp tuyến — phần vào đề thi.

---

## Chặng 2 · Khái niệm — Kiến thức cần nhớ

1. Vị trí tương đối của hai đường tròn $(O; R)$ và $(O'; R')$, $R \ge R'$

*(block `deflist` — xem JSON)*

🖼 *[hình vẽ TikZ — Ngoài nhau · tiếp xúc ngoài · cắt nhau · tiếp xúc trong]*

2. Hai tiếp tuyến: $AO$ là đường trung trực của $BC$

Từ điểm $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$.

$AB = AC$ (Định lí 2) $\Rightarrow A$ cách đều $B$, $C$; $OB = OC = R$ $\Rightarrow O$ cách đều $B$, $C$.

$\Rightarrow AO$ là đường trung trực của $BC$ $\Rightarrow AO \perp BC$ tại trung điểm $H$ của $BC$.

🖼 *[hình vẽ TikZ — $AO$ là trung trực của $BC$, $AO \perp BC$ tại $H$]*

3. Hệ thức $AB^2 = AH \cdot AO$ — phải chứng minh lại mỗi lần dùng

$\triangle AHB$ và $\triangle ABO$: $\widehat{A}$ chung, $\widehat{AHB} = \widehat{ABO} = 90^\circ$ $\Rightarrow \triangle AHB \backsim \triangle ABO$ (g.g) $\Rightarrow \dfrac{AH}{AB} = \dfrac{AB}{AO} \Rightarrow AB^2 = AH \cdot AO$.

> 👩‍🏫 **Ghi chú cho GV.** Mục 2 dùng tính chất đường trung trực (lớp 7): điểm cách đều hai đầu mút thì nằm trên trung trực. Mục 3: hệ thức $AB^2 = AH \cdot AO$ KHÔNG có sẵn trong SGK — mỗi lần dùng phải chứng minh lại bằng tam giác đồng dạng.

---

## Chặng 3 · Luyện tập 1 — Luyện tập 1

> **[example]** **Ví dụ 1.** Cho $(O; 5\text{ cm})$ và $(O'; 3\text{ cm})$. Xác định vị trí tương đối của hai đường tròn khi $OO'$ bằng $9$ cm, $6$ cm, $1$ cm (Hình 2 vẽ trường hợp $OO' = 6$ cm).
> 
> {\bfseriesLời giải}
> 
> $R + R' = $ cm, $R - R' = $ cm.
> 
> $OO' = 9 > 8$ $\Rightarrow$ ở ngoài nhau.
> 
> $2 < OO' = 6 < 8$ $\Rightarrow$ .
> 
> $OO' = 1 < 2$ $\Rightarrow (O)$  $(O')$.
> 
> Vậy lần lượt: ở ngoài nhau, cắt nhau, $(O)$ đựng $(O')$.

**Bài 1.**  `★ NB · trên lớp · có hình sẵn`

[NB] Hai đường tròn $(O; R)$ và $(O'; R')$ ($R \ge R'$) **cắt nhau** khi:

**Bài 2.**  `★ NB · trên lớp · có hình sẵn`

[NB] Hai đường tròn ở **ngoài nhau** có số điểm chung là:

> **[example]** **Ví dụ 2.** Hai đường tròn $(O; 7\text{ cm})$ và $(O'; 4\text{ cm})$ tiếp xúc với nhau (Hình 3). Tính $OO'$ trong hai trường hợp tiếp xúc ngoài và tiếp xúc trong.
> 
> {\bfseriesLời giải}
> 
> Tiếp xúc ngoài $\Rightarrow OO' =  = 7 + 4 = 11$ (cm).
> 
> Tiếp xúc trong $\Rightarrow OO' =  = 7 - 4 = $ (cm).
> 
> Vậy $OO' = 11$ cm hoặc $OO' = 3$ cm.

**Bài 3.**  `★ NB · trên lớp · có hình sẵn`

[NB] Hai đường tròn $(O; R)$ và $(O'; R')$ **tiếp xúc ngoài** khi:

**Bài 4.**  `★ NB · trên lớp · có hình sẵn`

[NB] Hai đường tròn $(O; R)$ và $(O'; R')$ ($R > R'$) **tiếp xúc trong** khi:

> **[example]** **Ví dụ 3.** Trên Hình 4, $MA$, $MB$ là hai tiếp tuyến của $(O; R)$ tại $A$, $B$. Chỉ ra các đoạn bằng nhau và các góc vuông có trên hình.
> 
> {\bfseriesLời giải}
> 
> $MA = $ (Định lí 2); $OA = OB = $.
> 
> $MA \perp OA$, $MB \perp OB$ (tiếp tuyến $\perp$ bán kính) $\Rightarrow \widehat{MAO} = \widehat{MBO} = ^\circ$.
> 
> Vậy $MA = MB$, $OA = OB$, $\widehat{MAO} = \widehat{MBO} = 90^\circ$.

**Bài 5.**  `★ NB · trên lớp · HS tự vẽ hình`

Vẽ hình vào vở theo các bước:

a) [NB] Vẽ $(O; 2\text{ cm})$ và điểm $A$ với $OA = 4$ cm; vẽ đường tròn đường kính $OA$ cắt $(O)$ tại $B$, $C$.

b) [NB] Vẽ hai tiếp tuyến $AB$, $AC$; nối $BC$, $AO$ cắt $BC$ tại $H$.

c) [NB] Đánh dấu hai đoạn bằng nhau $AB = AC$ và hai góc vuông tại $B$, $C$.

**Bài 6.**  `★ NB · trên lớp · có hình sẵn`

Trên Hình 5, $AB$, $AC$ là hai tiếp tuyến của $(O)$ tại $B$, $C$. Điền vào chỗ chấm:

a) [NB] $AB$ là tiếp tuyến tại $B$ $\Rightarrow AB \perp \ldots\ldots$

b) [NB] $\Rightarrow \widehat{ABO} = \ldots\ldots$

c) [NB] Tương tự $\widehat{ACO} = \ldots\ldots$

**Bài 7.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 5 — Bước 1. Điền vào chỗ chấm:

a) [NB] $AB$, $AC$ là hai tiếp tuyến cắt nhau tại $A$ $\Rightarrow AB \ldots\ldots AC$ (Định lí 2).

b) [NB] $\Rightarrow A$ cách đều hai điểm \ldots\ldots và \ldots\ldots

c) [NB] $\Rightarrow A$ nằm trên đường \ldots\ldots\ldots\ldots của đoạn $BC$.

**Bài 8.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 5 — Bước 2. Điền vào chỗ chấm:

a) [NB] $OB = OC = \ldots\ldots$

b) [NB] $\Rightarrow O$ cách đều hai điểm \ldots\ldots và \ldots\ldots

c) [NB] $\Rightarrow O$ nằm trên đường trung trực của đoạn \ldots\ldots

**Bài 9.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 5 — Bước 3. Điền vào chỗ chấm:

a) [NB] Hai điểm phân biệt $A$, $O$ cùng nằm trên đường trung trực của $BC$ $\Rightarrow AO$ là \ldots\ldots\ldots\ldots của $BC$.

b) [NB] $\Rightarrow AO \ldots\ldots BC$ tại $H$.

**Bài 10.**  `★ NB · trên lớp · có hình sẵn`

Vẫn trên Hình 5 — Bước 4. Điền vào chỗ chấm:

a) [NB] Đường trung trực $AO$ đi qua trung điểm của $BC$ $\Rightarrow H$ là \ldots\ldots\ldots\ldots của $BC$.

b) [NB] Biết $BC = 12$ cm $\Rightarrow BH = \ldots\ldots = \ldots\ldots$ cm.

> 👩‍🏫 **Ghi chú cho GV.** Bài 1–4 là phần Bài 17, chạy nhanh 10 phút. Bài 5–10 là bốn bước của khuôn $AO \perp BC$ — chữa kĩ, Bài 15 dùng lại nguyên xi.

---

## Chặng 4 · Luyện tập 2 — Luyện tập 2

> **[example]** **Ví dụ 4.** Một ròng rọc hình tròn tâm $O$ bán kính $4$ cm. Hai đoạn dây $AB$, $AC$ xuất phát từ móc $A$ cách tâm $8$ cm, căng tiếp xúc với ròng rọc tại $B$, $C$; đoạn $BC$ vuông góc với $AO$ tại $H$ (Hình 6). Tính $\widehat{AOB}$ rồi tính $OH$.
> 
> {\bfseriesLời giải}
> 
> $\triangle ABO$ vuông tại $B$ (tiếp tuyến): $\cos \widehat{AOB} = \dfrac{OB}{OA} = \dfrac{4}{8} =  \Rightarrow \widehat{AOB} = ^\circ$.
> 
> $\triangle OHB$ vuông tại $H$ ($AO \perp BC$): $OH = OB \cdot \cos 60^\circ = 4 \cdot \dfrac{1}{2} = $ (cm).
> 
> Vậy $\widehat{AOB} = 60^\circ$, $OH = 2$ cm.

**Bài 11.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$, biết $OA = 2R$ và $AO \perp BC$. Tính $OH$ và $AH$ theo $R$.

> 💡 Trong $\triangle ABO$ vuông, tỉ số $\dfrac{OB}{OA}$ cho biết góc nào? / Tam giác vuông nào chứa $OH$? Có $OH$ rồi thì $AH$ bằng hiệu nào?

> **[example]** **Ví dụ 5.** Từ điểm $M$ ngoài $(O; 3\text{ cm})$ kẻ tiếp tuyến $MA$ ($A$ là tiếp điểm) sao cho $\widehat{AMO} = 30^\circ$; $K$ là chân đường vuông góc hạ từ $A$ xuống $MO$ (Hình 7). Tính $MA$ và $MK$.
> 
> {\bfseriesLời giải}
> 
> $\triangle MAO$ vuông tại $A$ (tiếp tuyến): $MA = \dfrac{OA}{\tan 30^\circ} = $ (cm).
> 
> $\triangle MKA$ vuông tại $K$: $MK = MA \cdot \cos 30^\circ = 3\sqrt{3} \cdot \dfrac{\sqrt{3}}{2} = $ (cm).
> 
> Vậy $MA = 3\sqrt{3}$ cm, $MK = 4{,}5$ cm.

**Bài 12.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$, biết $OA = 2R$ và $AO \perp BC$. Tính $AB$ và $AH$ theo $R$.

> 💡 $\triangle ABO$ vuông ở đâu? Tính $AB$ bằng định lí nào? / Góc $BAO$ bằng bao nhiêu? Tam giác vuông nào chứa $AH$?

**Bài 13.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ ngoài $(O; 5\text{ cm})$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$, biết $OA = 10$ cm và $AO \perp BC$. Tính $AB$ và $AH$.

> 💡 $\triangle ABO$ vuông ở đâu? Tính $AB$ bằng định lí nào? / Góc $BAO$ bằng bao nhiêu? Tam giác vuông nào chứa $AH$?

> **[example]** **Ví dụ 6.** Tam giác $MPQ$ vuông tại $P$ có đường cao $PK$ ($K$ thuộc cạnh huyền $MQ$) (Hình 8). Chứng minh $QP^2 = QK \cdot QM$.
> 
> {\bfseriesLời giải}
> 
> Xét $\triangle QKP$ và $\triangle QPM$: $\widehat{Q}$ , $\widehat{QKP} = \widehat{QPM} = 90^\circ$.
> 
> $\Rightarrow \triangle QKP \backsim \triangle QPM$ () $\Rightarrow \dfrac{QK}{QP} = $.
> 
> Vậy $QP^2 = QK \cdot QM$.

**Bài 14.**  `★★ TH · trên lớp`

[TH] Từ điểm $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$. Biết $AO \perp BC$, chứng minh $AB^2 = AH \cdot AO$.

> 💡 Hai tam giác vuông nào cùng chứa góc $A$? / Hai tam giác đồng dạng cho tỉ số nào có mặt $AB$ hai lần?

> **[example]** **Ví dụ 7.** Hai đường tròn $(O; 5\text{ cm})$ và $(O')$ cắt nhau tại $A$, $B$; $OO'$ cắt $AB$ tại $I$ và $OI = 3$ cm (Hình 9). Chứng minh $OO' \perp AB$ tại $I$, $I$ là trung điểm $AB$, rồi tính $AB$.
> 
> {\bfseriesLời giải}
> 
> $OA = OB$ $\Rightarrow O$ cách đều $A$, $B$; $O'A = O'B$ $\Rightarrow O'$ cách đều $A$, $B$.
> 
> $\Rightarrow OO'$ là  của $AB$ $\Rightarrow OO' \perp AB$ tại trung điểm $I$ của $AB$.
> 
> $\triangle OIA$ vuông tại $I$: $AI^2 = OA^2 - OI^2 = 5^2 - 3^2 =  \Rightarrow AI = 4$ (cm).
> 
> $\Rightarrow AB = 2AI = $ (cm). Vậy $AB = 8$ cm.

**Bài 15.**  `★★★ VD · trên lớp`

[VD] Cho $(O; 6\text{ cm})$ và điểm $A$ với $OA = 12$ cm. Kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$ (Hình 10).

a) Chứng minh $AO \perp BC$ tại $H$ và $H$ là trung điểm $BC$.

b) Tính $AB$ và $BC$.

> 👩‍🏫 **Ghi chú cho GV.** Bài 14 bắt HS viết TRỌN chứng minh hai tam giác đồng dạng rồi mới nhân chéo — cấm viết thẳng hệ thức. Bài 15 là bài hình trọn vẹn, chỉ làm tại lớp.

---

## Chặng 5 · Tổng kết — Sơ đồ tư duy

🧠 **Sơ đồ tư duy — BUỔI 6**
  - HAI ĐƯỜNG TRÒN — so $OO'$ với $R \pm R'$
    - $OO' > R + R'$: ngoài nhau
    - $OO' = R + R'$: tiếp xúc ngoài
    - $R - R' < OO' < R + R'$: cắt nhau
    - $OO' = R - R'$: tiếp xúc trong
    - $OO' < R - R'$: đựng nhau
  - HÌNH CHUẨN HAI TIẾP TUYẾN
    - $\widehat{ABO} = 90^\circ$, huyền $AO$
    - $AB = AC$, $AO$ phân giác $\widehat{BAC}$
    - $A$, $O$ cách đều $B$, $C$ $\Rightarrow AO$ trung trực $BC$
    - $BH$ là ĐƯỜNG CAO ứng cạnh huyền $AO$
  - HỆ THỨC $AB^2 = AH \cdot AO$
    - PHẢI chứng minh lại mỗi lần dùng
    - $\widehat{A}$ chung $+$ hai góc $90^\circ$
    - $\triangle AHB \backsim \triangle ABO$ (g.g)
    - $\dfrac{AH}{AB} = \dfrac{AB}{AO}$ rồi nhân chéo
  - TÍNH ĐỘ DÀI
    - $\triangle ABO$ vuông tại $B$: Pythagore
    - $\dfrac{OB}{OA}$ cho $\widehat{AOB}$ (tỉ số lượng giác)
    - $OH$, $BH$ trong $\triangle OHB$ vuông tại $H$

**BÀI TẬP VỀ NHÀ (Vị trí tương đối của hai đường tròn. Luyện tập chung).**

**BTVN 1.**  `★ NB · BTVN · có hình sẵn`

[NB] Cho $(O; 10\text{ cm})$ và $(O'; 4\text{ cm})$ với $OO' = 16$ cm. Hai đường tròn:

**BTVN 2.**  `★ NB · BTVN · có hình sẵn`

[NB] Cho $(O; 6\text{ cm})$ và $(O'; 2\text{ cm})$ với $OO' = 5$ cm. Hai đường tròn:

**BTVN 3.**  `★ NB · BTVN · có hình sẵn`

[NB] Hai đường tròn cắt nhau có số điểm chung là:

**BTVN 4.**  `★ NB · BTVN · có hình sẵn`

[NB] Cho $(O; 8\text{ cm})$ và $(O'; 3\text{ cm})$ với $OO' = 11$ cm. Hai đường tròn:

**BTVN 5.**  `★ NB · BTVN · có hình sẵn`

[NB] Cho $(O; 10\text{ cm})$ và $(O'; 4\text{ cm})$ với $OO' = 6$ cm. Hai đường tròn:

**BTVN 6.**  `★ NB · BTVN · có hình sẵn`

[NB] Hai đường tròn tiếp xúc nhau có số điểm chung là:

**BTVN 7.**  `★ NB · BTVN · HS tự vẽ hình`

Vẽ hình vào vở theo các bước:

a) [NB] Vẽ $(O; 3\text{ cm})$ và điểm $A$ với $OA = 6$ cm; vẽ đường tròn đường kính $OA$ cắt $(O)$ tại $B$, $C$.

b) [NB] Vẽ hai tiếp tuyến $AB$, $AC$; nối $BC$, $AO$ cắt $BC$ tại $H$.

c) [NB] Đánh dấu $AB = AC$ và các góc vuông tại $B$, $C$, $H$.

**BTVN 8.**  `★ NB · BTVN · có hình sẵn`

Cho $AB$, $AC$ là hai tiếp tuyến của $(O)$ tại $B$, $C$. Điền vào chỗ chấm:

a) [NB] $AB \perp \ldots\ldots$ và $AC \perp \ldots\ldots$

b) [NB] $\widehat{ABO} = \ldots\ldots$

c) [NB] $\widehat{ACO} = \ldots\ldots$

**BTVN 9.**  `★ NB · BTVN · có hình sẵn`

Cho $AB$, $AC$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A$. Điền vào chỗ chấm:

a) [NB] $AB \ldots\ldots AC$ (Định lí 2).

b) [NB] $\Rightarrow A$ cách đều \ldots\ldots và \ldots\ldots

c) [NB] $\Rightarrow A$ thuộc đường trung trực của \ldots\ldots

**BTVN 10.**  `★ NB · BTVN · có hình sẵn`

Vẫn với hình ở BTVN 9. Điền vào chỗ chấm:

a) [NB] $OB = OC = \ldots\ldots \Rightarrow O$ cách đều $B$ và $C$.

b) [NB] $\Rightarrow O$ thuộc đường \ldots\ldots\ldots\ldots của $BC$.

**BTVN 11.**  `★ NB · BTVN · có hình sẵn`

Vẫn với hình ở BTVN 9. Điền vào chỗ chấm:

a) [NB] $A$, $O$ cùng thuộc đường trung trực của $BC$ $\Rightarrow AO$ là \ldots\ldots\ldots\ldots của $BC$.

b) [NB] $\Rightarrow AO \ldots\ldots BC$ tại $H$.

**BTVN 12.**  `★ NB · BTVN · có hình sẵn`

Vẫn với hình ở BTVN 9, $AO$ cắt $BC$ tại $H$. Điền vào chỗ chấm:

a) [NB] Đường trung trực $AO$ đi qua trung điểm của $BC$ $\Rightarrow H$ là \ldots\ldots của $BC$.

b) [NB] $BC = 10$ cm $\Rightarrow BH = \ldots\ldots = \ldots\ldots$ cm.

**BTVN 13.**  `★★ TH · BTVN`

[TH] Từ điểm $A$ ngoài $(O; 6\text{ cm})$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$, biết $OA = 12$ cm và $AO \perp BC$. Tính $OH$ và $AH$.

> 💡 Tỉ số $\dfrac{OB}{OA}$ cho biết góc nào? / Tam giác vuông nào chứa $OH$?

**BTVN 14.**  `★★ TH · BTVN`

[TH] Từ điểm $A$ ngoài $(O; 4\text{ cm})$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$, biết $OA = 8$ cm và $AO \perp BC$. Tính $AB$ và $AH$.

> 💡 Tính $AB$ trong tam giác vuông nào? / Góc $BAO$ bằng bao nhiêu?

**BTVN 15.**  `★★ TH · BTVN`

[TH] Từ điểm $A$ ngoài $(O; R)$ kẻ hai tiếp tuyến $AB$, $AC$ ($B$, $C$ là tiếp điểm), $AO$ cắt $BC$ tại $H$. Biết $AO \perp BC$, chứng minh $AC^2 = AH \cdot AO$.

> 💡 Hai tam giác vuông nào cùng chứa góc $A$ và cạnh $AC$? / Viết tỉ số đồng dạng rồi nhân chéo.

> 👩‍🏫 **Ghi chú cho GV.** BTVN soạn dày hơn quỹ, giao thì Thầy tự cắt. Nhắc HS: dùng $AB^2 = AH \cdot AO$ ở đâu cũng phải chứng minh lại.

---
