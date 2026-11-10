import json

base_dir = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"

# 1. Update phieu-5
with open(f"{base_dir}/phieu-5-luyen-tap-chung.json") as f:
    d5 = json.load(f)

v1_text_5 = (
    r"\textbf{Ví dụ 1.} Cho đường tròn $(O)$ đường kính $AB$, tiếp tuyến $xx'$ tại $A$ và tiếp tuyến $yy'$ tại $B$ của $(O)$. Một tiếp tuyến thứ ba của $(O)$ tại điểm $P$ ($P$ khác $A$ và $B$) cắt $xx'$ tại $M$ và cắt $yy'$ tại $N$ (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề.[[br]]"
    r"a) Chứng minh $MA = MP$ và $NB = NP$.[[br]]"
    r"b) Chứng minh rằng $MN = MA + NB$.[[br]]"
    r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    r"a) $MA$, $MP$ là hai [[fill:tiếp tuyến]] của $(O)$ cắt nhau tại $M$ $\Rightarrow MA = [[fill:MP]]$.[[br]]"
    r"$NB$, $NP$ là hai tiếp tuyến của $(O)$ cắt nhau tại $N$ $\Rightarrow NB = [[fill:NP]]$.[[br]]"
    r"b) $P$ nằm giữa $M$ và $N$ $\Rightarrow MN = [[fill:MP + PN|1.8cm]] = MA + [[fill:NB]]$.[[br]]"
    r"Vậy $MN = MA + NB$."
)
d5["stages"][2]["blocks"][5]["text"] = v1_text_5

v2_text_5 = (
    r"\textbf{Ví dụ 2.} Cho nửa đường tròn tâm $O$, đường kính $AB$. Kẻ các tiếp tuyến $Ax$, $By$ cùng phía với nửa đường tròn đối với $AB$. Từ điểm $M$ trên nửa đường tròn kẻ tiếp tuyến thứ ba với đường tròn, nó cắt $Ax$ và $By$ lần lượt tại $C$ và $D$ (Hình 6). Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề.[[br]]"
    r"a) Chứng minh tam giác $COD$ vuông tại $O$.[[br]]"
    r"b) Chứng minh $MC \cdot MD = OM^2$.[[br]]"
    r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    r"a) $CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$ $\Rightarrow OC$ là [[fill:tia phân giác]] của $\widehat{AOM}$[[br]]"
    r"$\Rightarrow \widehat{COM} = [[fill:\dfrac{1}{2}\widehat{AOM}|1.6cm]]$.[[br]]"
    r"$DB$, $DM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D$ $\Rightarrow OD$ là tia phân giác của $\widehat{MOB}$[[br]]"
    r"$\Rightarrow \widehat{MOD} = [[fill:\dfrac{1}{2}\widehat{MOB}|1.6cm]]$.[[br]]"
    r"$\widehat{COD} = \widehat{COM} + \widehat{MOD} = \dfrac{1}{2}(\widehat{AOM} + \widehat{MOB})$.[[br]]"
    r"$\widehat{AOM}$, $\widehat{MOB}$ là hai góc [[fill:kề bù]] $\Rightarrow \widehat{AOM} + \widehat{MOB} = 180^\circ$.[[br]]"
    r"$\Rightarrow \widehat{COD} = \dfrac{1}{2} \cdot 180^\circ = [[fill:90^\circ]] \Rightarrow \triangle COD$ vuông tại $O$.[[br]]"
    r"b) $\widehat{MCO} = [[fill:\widehat{MOD}]]$ (cùng phụ với $\widehat{COM}$).[[br]]"
    r"Xét $\triangle MCO$ và $\triangle MOD$ có:[[br]]"
    r"$\widehat{CMO} = \widehat{OMD} = 90^\circ$ ($CD$ là [[fill:tiếp tuyến]] của $(O)$ tại $M$)[[br]]"
    r"$\widehat{MCO} = \widehat{MOD}$ (chứng minh trên)[[br]]"
    r"$\Rightarrow \triangle MCO \backsim \triangle [[fill:MOD]]$ (g.g)[[br]]"
    r"$\Rightarrow \dfrac{MC}{MO} = [[fill:\dfrac{MO}{MD}|1.3cm]] \Rightarrow MC \cdot MD = [[fill:OM^2]]$."
)
d5["stages"][2]["blocks"][8]["text"] = v2_text_5

with open(f"{base_dir}/phieu-5-luyen-tap-chung.json", "w") as f:
    json.dump(d5, f, ensure_ascii=False, indent=2)

print("Updated phieu-5 Vi du 1 & 2!")

# 2. Update phieu-6
with open(f"{base_dir}/phieu-6-bai-tap-cuoi-chuong-v.json") as f:
    d6 = json.load(f)

v1_text_6 = (
    r"\textbf{Ví dụ 1.} Cho $\triangle ABC$ có ba góc nhọn, $AB > AC$, hai đường cao $BD$ và $CE$ cắt nhau tại $H$ (Hình 2). Vẽ tiếp vào Hình 2 các yếu tố còn thiếu theo đề.[[br]]"
    r"a) Chứng minh rằng bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn. Hãy chỉ rõ tâm $O$ của đường tròn này.[[br]]"
    r"b) Chứng minh $AB \cdot AE = AC \cdot AD$.[[br]]"
    r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    r"a) $CE$ là đường cao của $\triangle ABC$ $\Rightarrow \triangle BEC$ vuông tại $[[fill:E]]$[[br]]"
    r"$\Rightarrow B, E, C$ cùng thuộc đường tròn đường kính $[[fill:BC]]$.[[br]]"
    r"$BD$ là đường cao của $\triangle ABC$ $\Rightarrow \triangle BDC$ vuông tại $[[fill:D]]$[[br]]"
    r"$\Rightarrow B, D, C$ cùng thuộc đường tròn đường kính $BC$.[[br]]"
    r"Vậy bốn điểm $B, E, D, C$ cùng thuộc đường tròn đường kính $BC$, tâm $O$ là [[fill:trung điểm]] của $BC$.[[br]]"
    r"b) Xét $\triangle ABD$ và $\triangle ACE$ có:[[br]]"
    r"$\widehat{ADB} = \widehat{AEC} = [[fill:90^\circ]]$ ($BD$, $CE$ là đường cao của $\triangle ABC$)[[br]]"
    r"$\widehat{BAC}$ [[fill:chung]][[br]]"
    r"$\Rightarrow \triangle ABD \backsim \triangle [[fill:ACE]]$ (g.g)[[br]]"
    r"$\Rightarrow \dfrac{AB}{AC} = [[fill:\dfrac{AD}{AE}|1.3cm]]$[[br]]"
    r"Vậy $AB \cdot AE = [[fill:AC \cdot AD|1.8cm]]$."
)
d6["stages"][2]["blocks"][4]["text"] = v1_text_6

with open(f"{base_dir}/phieu-6-bai-tap-cuoi-chuong-v.json", "w") as f:
    json.dump(d6, f, ensure_ascii=False, indent=2)

print("Updated phieu-6 Vi du 1!")
