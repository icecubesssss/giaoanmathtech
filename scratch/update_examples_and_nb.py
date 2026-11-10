import json

# Phiếu 4
p4_path = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json"
with open(p4_path) as f:
    d4 = json.load(f)

for st in d4["stages"]:
    for b in st["blocks"]:
        var = b.get("variant")
        if var == "example" and "Ví dụ 1." in b.get("text", ""):
            b["text"] = (
                r"\textbf{Ví dụ 1.} Cho $\triangle ABC$ nhọn có ba đỉnh nằm trên $(O)$ và $AB < AC$. "
                r"Các đường cao $BD$, $CE$ cắt nhau tại $H$ (Hình 2). Vẽ tiếp vào Hình 2 các yếu tố còn thiếu theo đề.[[br]]"
                r"a) Chứng minh $\triangle BEH \backsim \triangle BDA$.[[br]]"
                r"b) Chứng minh hệ thức $BE \cdot BA = BH \cdot BD$.[[br]]"
                r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
                r"a) Xét $\triangle BEH$ và $\triangle BDA$ có:[[br]]"
                r"$\widehat{BEH} = \widehat{BDA} = [[fill:90^\circ]]$ ($CE \perp AB$, $BD \perp AC$)[[br]]"
                r"$[[fill:\widehat{ABD}]]$ chung[[br]]"
                r"$\Rightarrow \triangle BEH \backsim \triangle [[fill:BDA]]$ (g.g).[[br]]"
                r"b) Từ $\triangle BEH \backsim \triangle BDA \Rightarrow \dfrac{BE}{BD} = [[fill:\dfrac{BH}{BA}|1.3cm]]$.[[br]]"
                r"Vậy $BE \cdot BA = BH \cdot BD$ (nhân [[fill:chéo]] hai vế)."
            )
        if var == "example" and "Ví dụ 2." in b.get("text", ""):
            b["text"] = (
                r"\textbf{Ví dụ 2.} Cho đường tròn $(O; R)$. Từ điểm $A$ nằm ngoài đường tròn kẻ các tiếp tuyến $AB$, $AC$ với đường tròn ($B$, $C$ là các tiếp điểm). "
                r"Gọi $H$ là giao điểm của $OA$ và $BC$ (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề.[[br]]"
                r"a) Chứng minh $OA \perp BC$ tại $H$.[[br]]"
                r"b) Chứng minh $OH \cdot OA = R^2$.[[br]]"
                r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
                r"a) $AB$, $AC$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A \Rightarrow AB = [[fill:AC]]$.[[br]]"
                r"$OB = OC$ ([[fill:bán kính]] của $(O)$)[[br]]"
                r"$\Rightarrow OA$ là [[fill:đường trung trực]] của đoạn thẳng $BC \Rightarrow OA \perp BC$ tại $H$.[[br]]"
                r"b) Xét $\triangle OHB$ và $\triangle OBA$ có:[[br]]"
                r"$\widehat{OHB} = \widehat{OBA} = 90^\circ$ ($OA \perp BC$ tại $H$, $AB$ là [[fill:tiếp tuyến]] của $(O)$ tại $B$)[[br]]"
                r"$[[fill:\widehat{AOB}]]$ chung[[br]]"
                r"$\Rightarrow \triangle OHB \backsim \triangle [[fill:OBA]]$ (g.g)[[br]]"
                r"$\Rightarrow \dfrac{OH}{OB} = [[fill:\dfrac{OB}{OA}|1.3cm]] \Rightarrow OH \cdot OA = [[fill:OB^2]]$.[[br]]"
                r"Vậy $OA \perp BC$ và $OH \cdot OA = R^2$ (vì $OB = [[fill:R]]$)."
            )

with open(p4_path, "w") as f:
    json.dump(d4, f, ensure_ascii=False, indent=2)

# Phiếu 5
p5_path = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-5-luyen-tap-chung.json"
with open(p5_path) as f:
    d5 = json.load(f)

for st in d5["stages"]:
    for b in st["blocks"]:
        var = b.get("variant")
        if var == "example" and "Ví dụ 1." in b.get("text", ""):
            b["text"] = (
                r"\textbf{Ví dụ 1.} Cho đường tròn $(O)$ đường kính $AB$, tiếp tuyến $xx'$ tại $A$ và tiếp tuyến $yy'$ tại $B$ của $(O)$. "
                r"Một tiếp tuyến thứ ba của $(O)$ tại điểm $P$ ($P$ khác $A$ và $B$) cắt $xx'$ tại $M$ và cắt $yy'$ tại $N$ (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề.[[br]]"
                r"a) Chứng minh $MA = MP$ và $NB = NP$.[[br]]"
                r"b) Chứng minh rằng $MN = MA + NB$.[[br]]"
                r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
                r"a) $MA$, $MP$ là hai [[fill:tiếp tuyến]] của $(O)$ cắt nhau tại $M \Rightarrow MA = [[fill:MP]]$.[[br]]"
                r"$NB$, $NP$ là hai tiếp tuyến của $(O)$ cắt nhau tại $N \Rightarrow NB = [[fill:NP]]$.[[br]]"
                r"b) Vì $P$ nằm giữa $M$ và $N \Rightarrow MN = [[fill:MP + PN|1.8cm]] = MA + [[fill:NB]]$.[[br]]"
                r"Vậy $MN = MA + NB$."
            )
        if var == "example" and "Ví dụ 2." in b.get("text", ""):
            b["text"] = (
                r"\textbf{Ví dụ 2.} Cho nửa đường tròn tâm $O$, đường kính $AB$. Kẻ các tiếp tuyến $Ax$, $By$ cùng phía với nửa đường tròn đối với $AB$. "
                r"Từ điểm $M$ trên nửa đường tròn kẻ tiếp tuyến thứ ba với đường tròn, nó cắt $Ax$ và $By$ lần lượt tại $C$ và $D$ (Hình 6). Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề.[[br]]"
                r"a) Chứng minh tam giác $COD$ là tam giác vuông.[[br]]"
                r"b) Chứng minh $MC \cdot MD = OM^2$.[[br]]"
                r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
                r"a) $CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C \Rightarrow OC$ là [[fill:tia phân giác]] của $\widehat{AOM}$[[br]]"
                r"$\Rightarrow \widehat{COM} = [[fill:\dfrac{1}{2}\widehat{AOM}|1.6cm]]$.[[br]]"
                r"$DB$, $DM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D \Rightarrow OD$ là tia phân giác của $\widehat{MOB}$[[br]]"
                r"$\Rightarrow \widehat{MOD} = [[fill:\dfrac{1}{2}\widehat{MOB}|1.6cm]]$.[[br]]"
                r"$\widehat{COD} = \widehat{COM} + \widehat{MOD} = \dfrac{1}{2}(\widehat{AOM} + \widehat{MOB})$.[[br]]"
                r"$\widehat{AOM}$, $\widehat{MOB}$ là hai góc [[fill:kề bù]] $\Rightarrow \widehat{AOM} + \widehat{MOB} = 180^\circ \Rightarrow \widehat{COD} = \dfrac{1}{2} \cdot 180^\circ = [[fill:90^\circ]]$.[[br]]"
                r"$\Rightarrow \triangle COD$ vuông tại $O$.[[br]]"
                r"b) $\widehat{MCO} = [[fill:\widehat{MOD}]]$ (cùng phụ với $\widehat{COM}$).[[br]]"
                r"Xét $\triangle MCO$ và $\triangle MOD$ có:[[br]]"
                r"$\widehat{CMO} = \widehat{OMD} = 90^\circ$ ($CD$ là [[fill:tiếp tuyến]] của $(O)$ tại $M$)[[br]]"
                r"$\widehat{MCO} = \widehat{MOD}$ (chứng minh trên)[[br]]"
                r"$\Rightarrow \triangle MCO \backsim \triangle [[fill:MOD]]$ (g.g)[[br]]"
                r"$\Rightarrow \dfrac{MC}{MO} = [[fill:\dfrac{MO}{MD}|1.3cm]]$[[br]]"
                r"Vậy $\triangle COD$ vuông tại $O$ và $MC \cdot MD = [[fill:OM^2]]$."
            )

with open(p5_path, "w") as f:
    json.dump(d5, f, ensure_ascii=False, indent=2)

print("Updated Phieu 4 and 5 with split examples successfully!")

