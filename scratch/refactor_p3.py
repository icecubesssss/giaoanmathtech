import json

path = 'inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for st in data.get('stages', []):
    for b in st.get('blocks', []):
        if 'so_do_nguoc' in b:
            del b['so_do_nguoc']
        if 'phut_so_do' in b:
            del b['phut_so_do']
        
        lbl = b.get('label', '')
        if lbl == 'Bài 3.':
            b['statement'] = 'Cho nửa đường tròn $(O; R)$ đường kính $BC$. Trên nửa đường tròn $(O)$ vẽ tiếp tuyến $Bx$ của đường tròn $(O)$, $A$ là điểm bất kì thuộc nửa đường tròn sao cho $AB < AC$ ($A$ khác $B$, $A$ khác $C$). Tiếp tuyến tại $A$ của nửa đường tròn $(O)$ cắt tia $Bx$ tại $D$ (Hình 4).[[br]]a) ★★ Chứng minh $DA = DB$ và $OA = OB$.[[br]]b) ★★ Chứng minh $OD$ là đường trung trực của đoạn thẳng $AB$, từ đó suy ra $OD \\perp AB$.'
            b['answer'] = 'a) $DA$, $DB$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D \\Rightarrow DA = DB$ (tính chất hai tiếp tuyến cắt nhau).[[br]]$OA = OB = R$ (bán kính của $(O)$).[[br]]b) $DA = DB$ và $OA = OB \\Rightarrow OD$ là đường trung trực của đoạn thẳng $AB$.[[br]]Vậy $OD \\perp AB$ (tính chất đường trung trực).'
        elif lbl == 'Bài 4.':
            b['statement'] = 'Cho đường tròn $(O)$, đường kính $MN$. Trên đường tròn $(O)$ lấy điểm $I$. Hai tiếp tuyến của đường tròn $(O)$ tại $M$ và $I$ cắt nhau ở $K$ (Hình 6).[[br]]a) ★★ Chứng minh $KO$ là đường trung trực của đoạn thẳng $MI$.[[br]]b) ★★ Chứng minh tam giác $MIN$ vuông tại $I$.[[br]]c) ★★ Chứng minh $KO \\parallel NI$.'
            b['answer'] = 'a) $KM$, $KI$ là hai tiếp tuyến của $(O)$ cắt nhau tại $K \\Rightarrow KM = KI$.[[br]]$OM = OI = R \\Rightarrow KO$ là đường trung trực của đoạn thẳng $MI \\Rightarrow KO \\perp MI$.[[br]]b) Xét $\\triangle MIN$ có $IO$ là đường trung tuyến ứng với cạnh $MN$ ($O$ là trung điểm của $MN$).[[br]]$OI = OM = ON = R \\Rightarrow IO = \\dfrac{MN}{2} \\Rightarrow \\triangle MIN$ vuông tại $I \\Rightarrow NI \\perp MI$.[[br]]c) $KO \\perp MI$ và $NI \\perp MI \\Rightarrow KO \\parallel NI$ (hai đường thẳng phân biệt cùng vuông góc với $MI$).[[br]]Vậy $KO \\parallel NI$.'
        elif lbl == 'BTVN 3.':
            b['statement'] = 'Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn $(O)$. Từ $A$ vẽ hai tiếp tuyến $AM$ và $AN$ với $(O)$ ($M$, $N$ là hai tiếp điểm) (Hình 10).[[br]]a) ★★ Chứng minh $AM = AN$ và $OM = ON$.[[br]]b) ★★ Chứng minh $OA \\perp MN$.'
            b['answer'] = 'a) $AM$, $AN$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A \\Rightarrow AM = AN$ (tính chất hai tiếp tuyến cắt nhau).[[br]]$OM = ON = R$ (bán kính của $(O)$).[[br]]b) $AM = AN$ và $OM = ON \\Rightarrow OA$ là đường trung trực của đoạn thẳng $MN$.[[br]]Vậy $OA \\perp MN$ (tính chất đường trung trực).'
        elif lbl == 'BTVN 4.':
            b['statement'] = 'Cho đường tròn $(O; R)$, đường kính $AB$. Trên đường tròn $(O)$ lấy điểm $M$ ($MA < MB$). Tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ và $B$ lần lượt là $C$ và $D$ (Hình 11).[[br]]a) ★★ Chứng minh $OC$ là đường trung trực của đoạn thẳng $AM$.[[br]]b) ★★ Chứng minh tam giác $AMB$ vuông tại $M$.[[br]]c) ★★ Chứng minh $OC \\parallel MB$.'
            b['answer'] = 'a) $CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C \\Rightarrow CA = CM$.[[br]]$OA = OM = R \\Rightarrow OC$ là đường trung trực của đoạn thẳng $AM \\Rightarrow OC \\perp AM$.[[br]]b) Xét $\\triangle AMB$ có $MO$ là đường trung tuyến ứng với cạnh $AB$ ($O$ là trung điểm của $AB$).[[br]]$OM = OA = OB = R \\Rightarrow MO = \\dfrac{AB}{2} \\Rightarrow \\triangle AMB$ vuông tại $M \\Rightarrow BM \\perp AM$.[[br]]c) $OC \\perp AM$ và $BM \\perp AM \\Rightarrow OC \\parallel MB$ (hai đường thẳng phân biệt cùng vuông góc với $AM$).[[br]]Vậy $OC \\parallel MB$.'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Done refactoring phieu-3')
