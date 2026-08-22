# -*- coding: utf-8 -*-
import json
import os

c_dir = 'inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron'
b_dir = 'inputs/seeds/lop-9/hinh-hoc/lop-b/chuong-05-duong-tron'

extend_tasks = {
    'phieu-a-mo-dau-ve-duong-tron': [
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho tam giác nhọn $ABC$ có hai đường cao $BD$ và $CE$ cắt nhau tại trực tâm $H$. Gọi $M$ là trung điểm của $BC$ và $N$ là trung điểm của đoạn thẳng $AH$.\n\na) Chứng minh bốn điểm $B, C, D, E$ cùng thuộc đường tròn tâm $M$ bán kính $R_1 = \\dfrac{BC}{2}$.\n\nb) Chứng minh bốn điểm $A, D, H, E$ cùng thuộc đường tròn tâm $N$ bán kính $R_2 = \\dfrac{AH}{2}$.',
            'tier': 'extend',
            'level': 3,
            'hints': ['Xét hai tam giác vuông $BDC$ và $BEC$ có chung cạnh huyền $BC$', 'Xét hai tam giác vuông $ADH$ và $AEH$ có chung cạnh huyền $AH$'],
            'solution': 'a) Xét tam giác $BDC$ vuông tại $D$, trung tuyến $DM = \\dfrac{BC}{2} = MB = MC$. Xét tam giác $BEC$ vuông tại $E$, trung tuyến $EM = \\dfrac{BC}{2} = MB = MC$. Suy ra $MD = ME = MB = MC = \\dfrac{BC}{2}$. Vậy bốn điểm $B, C, D, E$ cùng thuộc đường tròn tâm $M$, bán kính $R_1 = \\dfrac{BC}{2}$.\n\nb) Xét tam giác $ADH$ vuông tại $D$ và tam giác $AEH$ vuông tại $E$ có $N$ là trung điểm cạnh huyền chung $AH$, suy ra $NA = ND = NH = NE = \\dfrac{AH}{2}$. Vậy bốn điểm $A, D, H, E$ cùng thuộc đường tròn tâm $N$, bán kính $R_2 = \\dfrac{AH}{2}$.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 12*.',
            'statement': '\\textbf{(Mở rộng)} Cho hình chữ nhật $ABCD$ có $AB = a, BC = b$. Một điểm $M$ di động trên đường tròn ngoại tiếp hình chữ nhật $ABCD$. Chứng minh rằng tổng bình phương khoảng cách $MA^2 + MB^2 + MC^2 + MD^2$ luôn không đổi khi $M$ thay đổi.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Gọi $O$ là giao điểm của $AC$ và $BD$', 'Sử dụng công thức tính độ dài đường trung tuyến trong tam giác $MAC$ và tam giác $MBD$'],
            'solution': 'Gọi $O = AC \\cap BD$. Khi đó $O$ là tâm đường tròn ngoại tiếp hình chữ nhật $ABCD$ với bán kính $R = \\dfrac{\\sqrt{a^2+b^2}}{2}$.\n\nVì điểm $M$ thuộc đường tròn $(O; R)$ nên $MO = R$.\n\nTrong tam giác $MAC$ có trung tuyến $MO$, ta có: $MA^2 + MC^2 = 2MO^2 + \\dfrac{AC^2}{2} = 2R^2 + 2R^2 = 4R^2$.\n\nTrong tam giác $MBD$ có trung tuyến $MO$, ta có: $MB^2 + MD^2 = 2MO^2 + \\dfrac{BD^2}{2} = 2R^2 + 2R^2 = 4R^2$.\n\nCộng vế theo vế: $MA^2 + MB^2 + MC^2 + MD^2 = 8R^2 = 2(a^2 + b^2)$ (hằng số không đổi).\n\nVậy tổng bình phương khoảng cách luôn bằng $2(a^2+b^2)$.',
            'hinh_san': False,
            'writelines': 8
        }
    ],
    'phieu-b-cung-va-day-cua-mot-duong-tron': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Cho đường tròn $(O; R)$ và hai dây cung $AB, CD$ vuông góc với nhau tại $I$. Chứng minh hệ thức: $IA^2 + IB^2 + IC^2 + ID^2 = 4R^2$.',
            'tier': 'extend',
            'level': 3,
            'hints': ['Kẻ đường kính $AE$ của đường tròn $(O)$', 'Sử dụng tam giác vuông nội tiếp đường kính để chứng minh $BE = AD$'],
            'solution': 'Kẻ đường kính $AE$. Vì $\\widehat{ABE} = 90^\\circ$ nên $AB^2 + BE^2 = AE^2 = (2R)^2 = 4R^2$.\n\nVì $AB \\perp CD$ tại $I$ nên trong các tam giác vuông $IAD$ và $IBC$ ta có: $IA^2 + ID^2 = AD^2$ và $IB^2 + IC^2 = BC^2$.\n\nMặt khác ta chứng minh được $AD = BE$ (hai dây chắn hai cung bằng nhau), do đó: $IA^2 + IB^2 + IC^2 + ID^2 = AD^2 + BC^2 = BE^2 + AB^2 = 4R^2$.\n\nVậy đẳng thức được chứng minh.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho đường tròn $(O; R)$ và dây $AB < 2R$ cố định. Điểm $M$ di động trên cung lớn $AB$. Tìm vị trí của điểm $M$ để diện tích tam giác $MAB$ đạt giá trị lớn nhất.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Biểu diễn diện tích $S_{MAB} = \\dfrac{1}{2} AB \\cdot d(M, AB)$', 'Khoảng cách từ $M$ đến dây $AB$ lớn nhất khi $M$ ở vị trí nào trên cung lớn?'],
            'solution': 'Kẻ $MH \\perp AB$ tại $H$. Khi đó diện tích tam giác $MAB$ là: $S_{MAB} = \\dfrac{1}{2} AB \\cdot MH$.\n\nVì độ dài dây $AB$ cố định nên diện tích tam giác $MAB$ đạt giá trị lớn nhất khi và chỉ khi khoảng cách $MH$ lớn nhất.\n\nKhoảng cách từ điểm $M$ trên cung lớn $AB$ đến đoạn thẳng $AB$ lớn nhất khi $M$ là điểm chính giữa của cung lớn $AB$ (khi đó bán kính $OM \\perp AB$ tại trung điểm của $AB$).\n\nVậy khi $M$ là điểm chính giữa của cung lớn $AB$ thì diện tích tam giác $MAB$ đạt giá trị lớn nhất.',
            'hinh_san': False,
            'writelines': 8
        }
    ],
    'phieu-c-do-dai-cung-dien-tich-quat-vanh-khuyen': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Một ròng rọc kép gồm hai bánh xe đồng trục có bán kính lần lượt là $R_1 = 18\\text{ cm}$ và $R_2 = 12\\text{ cm}$. Khi bánh xe lớn quay một góc $100^\\circ$ làm dây kéo di chuyển một đoạn $l$, hỏi bánh xe nhỏ phải quay một góc bao nhiêu độ để kéo được cùng đoạn dây có độ dài $l$ đó?',
            'tier': 'extend',
            'level': 3,
            'hints': ['Áp dụng công thức tính độ dài cung tròn $l = \\dfrac{\\pi R n}{180}$', 'Cho hai độ dài cung $l_1 = l_2$ để tìm số đo góc quay $n_2$'],
            'solution': 'Độ dài đoạn dây kéo do bánh xe lớn nhả ra khi quay góc $100^\\circ$ là:\n\n$l_1 = \\dfrac{\\pi \\cdot 18 \\cdot 100}{180} = 10\\pi\\text{ cm}$.\n\nĐể bánh xe nhỏ nhả ra cùng độ dài $l_2 = 10\\pi\\text{ cm}$, ta có phương trình:\n\n$\\dfrac{\\pi \\cdot 12 \\cdot n_2}{180} = 10\\pi \\implies n_2 = \\dfrac{10 \\cdot 180}{12} = 150^\\circ$.\n\nVậy bánh xe nhỏ phải quay một góc $150^\\circ$.',
            'hinh_san': False,
            'writelines': 6
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho hình vuông $ABCD$ có cạnh bằng $a$. Vẽ bốn cung tròn tâm lần lượt là $A, B, C, D$ bán kính $R = \\dfrac{a}{2}$ nằm phía trong hình vuông. Tính diện tích phần mặt phẳng hình vuông nằm ngoài bốn hình quạt tròn đó theo $a$.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Tổng diện tích 4 hình quạt tròn $90^\\circ$ bằng diện tích của một hình tròn có cùng bán kính $R = a/2$', 'Lấy diện tích hình vuông trừ đi tổng diện tích 4 hình quạt tròn'],
            'solution': 'Diện tích hình vuông $ABCD$ là: $S_{\\text{hv}} = a^2$.\n\nBốn hình quạt tròn tại bốn góc vuông có góc ở tâm bằng $90^\\circ$, bán kính $R = \\dfrac{a}{2}$.\n\nTổng diện tích của bốn hình quạt tròn bằng diện tích của một hình tròn bán kính $R = \\dfrac{a}{2}$:\n\n$S_{\\text{tròn}} = \\pi R^2 = \\pi \\left(\\dfrac{a}{2}\\right)^2 = \\dfrac{\\pi a^2}{4}$.\n\nDiện tích phần hình vuông nằm ngoài bốn hình quạt tròn là:\n\n$S = S_{\\text{hv}} - S_{\\text{tròn}} = a^2 - \\dfrac{\\pi a^2}{4} = a^2\\left(1 - \\dfrac{\\pi}{4}\\right)$.\n\nVậy diện tích cần tìm là $a^2\\left(1 - \\dfrac{\\pi}{4}\\right)$.',
            'hinh_san': False,
            'writelines': 6
        }
    ],
    'phieu-d-luyen-tap-chung-bai-13-14-15': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Cho nửa đường tròn tâm $O$ đường kính $AB = 2R$. Lấy điểm $C$ bất kì trên nửa đường tròn ($C \\ne A, B$). Kẻ đường cao $CH \\perp AB$ tại $H$. Gọi $I$ và $K$ lần lượt là tâm đường tròn nội tiếp các tam giác $CHA$ và $CHB$. Chứng minh rằng tam giác $CIK$ vuông cân tại $C$.',
            'tier': 'extend',
            'level': 3,
            'hints': ['Tính góc $\\widehat{ICK}$ bằng tổng hai góc phân giác của $\\widehat{ACH}$ và $\\widehat{BCH}$', 'Chứng minh $CI = CK$ từ tỉ số đồng dạng của hai tam giác vuông $CHA$ và $CHB$'],
            'solution': 'Vì $C$ thuộc nửa đường tròn đường kính $AB$ nên $\\widehat{ACB} = 90^\\circ$.\n\nDo $CI$ và $CK$ lần lượt là tia phân giác của $\\widehat{ACH}$ và $\\widehat{BCH}$ nên:\n\n$\\widehat{ICK} = \\widehat{ICH} + \\widehat{KCH} = \\dfrac{\\widehat{ACH} + \\widehat{BCH}}{2} = \\dfrac{90^\\circ}{2} = 45^\\circ$.\n\nMặt khác xét $\\triangle CHA \\sim \\triangle BHC$ (g.g) suy ra tỉ số bán kính nội tiếp $\\dfrac{r_1}{r_2} = \\dfrac{AC}{BC}$, từ đó suy ra $CI = CK$.\n\nTam giác $CIK$ có $CI = CK$ và $\\widehat{ICK} = 45^\\circ$ nên là tam giác vuông cân tại $C$.\n\nVậy tam giác $CIK$ vuông cân tại $C$.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho nửa đường tròn $(O; R)$ đường kính $AB$. Tìm vị trí của điểm $C$ trên nửa đường tròn để chu vi tam giác $ABC$ đạt giá trị lớn nhất.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Chu vi $P = AB + AC + BC = 2R + (AC + BC)$', 'Áp dụng bất đẳng thức Bunhiacopxki cho $(1 \\cdot AC + 1 \\cdot BC)^2 \\le 2(AC^2 + BC^2)$'],
            'solution': 'Chu vi tam giác $ABC$ là: $P = AB + AC + BC = 2R + (AC + BC)$.\n\nÁp dụng bất đẳng thức Bunhiacopxki cho hai bộ số $(1, 1)$ và $(AC, BC)$:\n\n$(1 \\cdot AC + 1 \\cdot BC)^2 \\le (1^2 + 1^2)(AC^2 + BC^2) = 2 \\cdot AB^2 = 2 \\cdot (2R)^2 = 8R^2$.\n\nSuy ra: $AC + BC \\le \\sqrt{8R^2} = 2R\\sqrt{2}$.\n\nDo đó: $P \\le 2R + 2R\\sqrt{2} = 2R(1 + \\sqrt{2})$.\n\nDấu đẳng thức xảy ra khi và chỉ khi $AC = BC$, tức là tam giác $ABC$ vuông cân tại $C$, tương đương $C$ là điểm chính giữa của nửa đường tròn.\n\nVậy khi $C$ là điểm chính giữa của nửa đường tròn thì chu vi tam giác $ABC$ lớn nhất bằng $2R(1+\\sqrt{2})$.',
            'hinh_san': False,
            'writelines': 8
        }
    ],
    'phieu-e-vi-tri-duong-thang-va-duong-tron-tiep-tuyen': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Từ điểm $A$ nằm ngoài đường tròn $(O; R)$, kẻ tiếp tuyến $AB$ ($B$ là tiếp điểm) và cát tuyến $ACD$ ($C$ nằm giữa $A$ và $D$). Chứng minh hệ thức tiếp tuyến – cát tuyến: $AB^2 = AC \\cdot AD$.',
            'tier': 'extend',
            'level': 3,
            'hints': ['Xét hai tam giác $ABC$ và $ADB$', 'Chứng minh góc tạo bởi tiếp tuyến và dây cung bằng góc nội tiếp: $\\widehat{ABC} = \\widehat{ADB}$'],
            'solution': 'Xét tam giác $ABC$ và tam giác $ADB$ có:\n\n$\\widehat{A}$ là góc chung;\n\n$\\widehat{ABC} = \\widehat{ADB}$ (góc tạo bởi tia tiếp tuyến và dây cung bằng góc nội tiếp cùng chắn cung $BC$).\n\nSuy ra $\\triangle ABC \\sim \\triangle ADB$ (g.g).\n\nTừ đó ta có tỉ lệ cạnh tương ứng:\n\n$\\dfrac{AB}{AD} = \\dfrac{AC}{AB} \\implies AB^2 = AC \\cdot AD$.\n\nVậy hệ thức được chứng minh.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài $(O)$. Kẻ hai tiếp tuyến $AB, AC$ ($B, C$ là các tiếp điểm). Gọi $H$ là giao điểm của $AO$ và $BC$. Kẻ cát tuyến $ADE$ ($D$ nằm giữa $A$ và $E$). Chứng minh hệ thức: $AH \\cdot AO = AD \\cdot AE$.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Áp dụng hệ thức lượng $AB^2 = AH \\cdot AO$ trong tam giác vuông $ABO$', 'Sử dụng hệ thức cát tuyến $AB^2 = AD \\cdot AE$'],
            'solution': 'Xét tam giác $ABO$ vuông tại $B$ có đường cao $BH \\perp AO$ (do $AO$ là đường trung trực của $BC$).\n\nTheo hệ thức lượng về cạnh và đường cao trong tam giác vuông: $AB^2 = AH \\cdot AO$ (1).\n\nMặt khác, chứng minh tương tự bài trên ta có $\\triangle ABD \\sim \\triangle AEB$ (g.g), suy ra: $AB^2 = AD \\cdot AE$ (2).\n\nTừ (1) và (2) suy ra: $AH \\cdot AO = AD \\cdot AE$.\n\nVậy hệ thức được chứng minh.',
            'hinh_san': False,
            'writelines': 8
        }
    ],
    'phieu-f-vi-tri-hai-duong-tron-va-luyen-tap-chung': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Cho hai đường tròn $(O_1; R_1)$ và $(O_2; R_2)$ tiếp xúc ngoài tại $A$. Kẻ tiếp tuyến chung ngoài $BC$ ($B \\in (O_1), C \\in (O_2)$).\n\na) Chứng minh tam giác $ABC$ vuông tại $A$.\n\nb) Chứng minh độ dài đoạn tiếp tuyến chung ngoài $BC = 2\\sqrt{R_1R_2}$.',
            'tier': 'extend',
            'level': 3,
            'hints': ['Kẻ tiếp tuyến chung trong tại $A$ cắt $BC$ tại $M$', 'Kẻ $O_2H \\perp O_1B$ để tính độ dài đoạn thẳng $BC$ theo định lí Pythagore'],
            'solution': 'a) Kẻ tiếp tuyến chung trong tại $A$ cắt đoạn thẳng $BC$ tại $M$.\n\nTheo tính chất hai tiếp tuyến cắt nhau ta có: $MB = MA$ và $MC = MA$, suy ra $MB = MC = MA = \\dfrac{BC}{2}$.\n\nTam giác $ABC$ có đường trung tuyến $AM = \\dfrac{BC}{2}$ nên tam giác $ABC$ vuông tại $A$, tức là $\\widehat{BAC} = 90^\\circ$.\n\nb) Kẻ $O_2H \\perp O_1B$ tại $H$. Tứ giác $BCHO_2$ là hình chữ nhật nên $BC = HO_2$.\n\nTrong tam giác vuông $O_1HO_2$ tại $H$ ta có:\n\n$HO_2 = \\sqrt{O_1O_2^2 - O_1H^2} = \\sqrt{(R_1+R_2)^2 - (R_1-R_2)^2} = \\sqrt{4R_1R_2} = 2\\sqrt{R_1R_2}$.\n\nVậy $BC = 2\\sqrt{R_1R_2}$.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho hai đường tròn $(O_1; R)$ và $(O_2; r)$ cắt nhau tại hai điểm $A$ và $B$. Kẻ cát tuyến chung $CAD$ đi qua $A$ ($C \\in (O_1), D \\in (O_2)$). Tìm vị trí của cát tuyến $CD$ để độ dài đoạn thẳng $CD$ đạt giá trị lớn nhất.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Kẻ $O_1H \\perp CD$ tại $H$ và $O_2K \\perp CD$ tại $K$', 'Nhận xét tứ giác $O_1HKO_2$ là hình thang vuông và so sánh $HK$ với $O_1O_2$'],
            'solution': 'Kẻ $O_1H \\perp CD$ tại $H$ và $O_2K \\perp CD$ tại $K$.\n\nTheo quan hệ vuông góc giữa đường kính và dây: $H$ là trung điểm của $AC$ nên $AC = 2AH$; $K$ là trung điểm của $AD$ nên $AD = 2AK$.\n\nSuy ra: $CD = AC + AD = 2(AH + AK) = 2HK$.\n\nVì $O_1H \\parallel O_2K$ (cùng vuông góc với $CD$) nên tứ giác $O_1HKO_2$ là hình thang vuông, suy ra $HK \\le O_1O_2$.\n\nDo đó: $CD = 2HK \\le 2O_1O_2$.\n\nDấu đẳng thức xảy ra khi và chỉ khi $HK = O_1O_2$, tức là cát tuyến $CD$ song song với đường nối tâm $O_1O_2$.\n\nVậy khi cát tuyến $CD$ song song với $O_1O_2$ thì $CD$ đạt giá trị lớn nhất bằng $2O_1O_2$.',
            'hinh_san': False,
            'writelines': 8
        }
    ],
    'phieu-g-bai-tap-cuoi-chuong-v-luyen-dang-cau-iv-2': [
        {
            'type': 'problem',
            'label': 'Bài 10*.',
            'statement': '\\textbf{(Mở rộng)} Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Kẻ hai tiếp tuyến $AB, AC$ ($B, C$ là các tiếp điểm). Kẻ đường kính $BD$. Đoạn thẳng $AD$ cắt đường tròn $(O)$ tại điểm thứ hai là $E$. Gọi $H$ là giao điểm của $AO$ và $BC$. Chứng minh ba điểm $E, H, C$ thẳng hàng.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Chứng minh $\\triangle AHE \\sim \\triangle ADO$ (c.g.c)', 'Sử dụng góc nội tiếp chắn nửa đường tròn $\\widehat{BED} = 90^\\circ$'],
            'solution': 'Trong tam giác vuông $ABO$ tại $B$ có đường cao $BH$: $AB^2 = AH \\cdot AO$.\n\nXét hai tam giác $ABE$ và $ADB$ có $\\widehat{A}$ chung và $\\widehat{ABE} = \\widehat{ADB}$ nên $\\triangle ABE \\sim \\triangle ADB$ (g.g), suy ra $AB^2 = AE \\cdot AD$.\n\nTừ đó suy ra $AH \\cdot AO = AE \\cdot AD \\implies \\dfrac{AH}{AD} = \\dfrac{AE}{AO}$.\n\nXét tam giác $AHE$ và tam giác $ADO$ có góc $\\widehat{A}$ chung và $\\dfrac{AH}{AD} = \\dfrac{AE}{AO}$ nên $\\triangle AHE \\sim \\triangle ADO$ (c.g.c), suy ra $\\widehat{AHE} = \\widehat{ADO}$.\n\nMặt khác $BD$ là đường kính nên $\\widehat{BED} = 90^\\circ \\implies BE \\perp AD$. Tứ giác $BHOE$ có $\\widehat{BHO} = \\widehat{BEO} = 90^\\circ$ nên nội tiếp, từ đó suy ra ba điểm $E, H, C$ thẳng hàng.\n\nVậy ba điểm $E, H, C$ thẳng hàng.',
            'hinh_san': False,
            'writelines': 8
        },
        {
            'type': 'problem',
            'label': 'Bài 11*.',
            'statement': '\\textbf{(Mở rộng)} Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Kẻ hai tiếp tuyến $AB, AC$ và đường kính $BD$. Đoạn thẳng $AD$ cắt đường tròn $(O)$ tại $E$. Kẻ $CK \\perp BD$ tại $K$. Gọi $I$ là giao điểm của $AD$ và $CK$. Chứng minh $I$ là trung điểm của đoạn thẳng $CK$.',
            'tier': 'extend',
            'level': 4,
            'hints': ['Kéo dài $DC$ cắt tiếp tuyến tại $B$ của đường tròn $(O)$ tại $P$', 'Sử dụng hệ quả định lí Thales cho các đoạn thẳng song song $CK \\parallel BP$'],
            'solution': 'Kéo dài $DC$ cắt đường thẳng $AB$ tại điểm $P$.\n\nVì $\\widehat{BCD} = 90^\\circ$ (góc nội tiếp chắn nửa đường tròn) nên tam giác $BDP$ vuông tại $B$ có đường cao $BC$.\n\nTheo tính chất tiếp tuyến ta có $AB = AC$, suy ra $\\triangle ABC$ cân tại $A$, từ đó chứng minh được $A$ là trung điểm của đoạn thẳng $BP$, tức $AB = AP$.\n\nVì $CK \\perp BD$ và $AB \\perp BD$ nên $CK \\parallel AB \\parallel BP$.\n\nÁp dụng định lí Thales trong tam giác $DAP$ có $CI \\parallel AP$: $\\dfrac{CI}{AP} = \\dfrac{DI}{DA}$.\n\nÁp dụng định lí Thales trong tam giác $DAB$ có $IK \\parallel AB$: $\\dfrac{IK}{AB} = \\dfrac{DI}{DA}$.\n\nSuy ra: $\\dfrac{CI}{AP} = \\dfrac{IK}{AB}$. Mà $AP = AB$ nên $CI = IK$.\n\nVậy $I$ là trung điểm của đoạn thẳng $CK$.',
            'hinh_san': False,
            'writelines': 8
        }
    ]
}

def generate_all():
    for filename, ext_problems in extend_tasks.items():
        src_file = os.path.join(c_dir, filename + '.json')
        dst_file = os.path.join(b_dir, filename + '.json')
        
        with open(src_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['class_tier'] = 'B'
        if 'eyebrow' in data:
            data['eyebrow'] = data['eyebrow'].replace('LỚP C', 'LỚP B').replace('TẦNG C', 'TẦNG B')
        
        # Thêm vào stage cuối cùng
        target_stage = data['stages'][-1]
        
        # Lọc bỏ các bài problem tier extend cũ nếu có
        target_stage['blocks'] = [b for b in target_stage['blocks'] if not (b.get('type') == 'problem' and b.get('tier') == 'extend')]
        # Lọc bỏ tiêu đề mở rộng cũ nếu có
        target_stage['blocks'] = [b for b in target_stage['blocks'] if not (b.get('type') == 'para' and 'Mở rộng' in b.get('text', ''))]
        
        # Thêm các bài problem mới
        for prob in ext_problems:
            target_stage['blocks'].append(prob)
            
        with open(dst_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'Done: {dst_file}')

if __name__ == '__main__':
    generate_all()
