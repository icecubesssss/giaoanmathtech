#!/usr/bin/env python3
"""Chuyển đổi toàn bộ sơ đồ ngược sang các câu hỏi giàn giáo a), b) (NB, TH) cho Chương V.

Quy định:
- Xóa hoàn toàn sơ đồ ngược (`so_do_nguoc`, `phut_so_do`).
- Các câu trước đây có sơ đồ ngược thì chuyển thành câu hỏi tách ý a), b), c) từ chính lời giải.
- Đánh sao (★, ★★) tương ứng từng ý.
- Bỏ cụm từ "rồi dựa vào sơ đồ ngược để trình bày...".
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH5_DIR = ROOT / "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2"


def clean_so_do_from_blocks(stages):
    for st in stages:
        for b in st.get("blocks", []):
            b.pop("so_do_nguoc", None)
            b.pop("phut_so_do", None)


def update_phieu_3():
    fpath = CH5_DIR / "phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    clean_so_do_from_blocks(data["stages"])

    # Stage 3 B6 (Bài 3)
    b3 = data["stages"][2]["blocks"][5]
    b3["statement"] = (
        r"Cho nửa đường tròn $(O; R)$ đường kính $BC$. Trên nửa đường tròn $(O)$ vẽ tiếp tuyến $Bx$ của đường tròn $(O)$, "
        r"$A$ là điểm bất kì thuộc nửa đường tròn sao cho $AB < AC$ ($A$ khác $B$, $A$ khác $C$). Tiếp tuyến tại $A$ "
        r"của nửa đường tròn $(O)$ cắt tia $Bx$ tại $D$ (Hình 4). Vẽ tiếp vào Hình 4 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $OD$ là đường trung trực của đoạn thẳng $AB$.[[br]]"
        r"b) [TH] ★★ Chứng minh $OD \perp AB$."
    )
    b3["answer"] = (
        r"a) $DA$, $DB$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D$ $\Rightarrow DA = DB$.[[br]]"
        r"$OA = OB$ (bán kính của $(O)$)[[br]]"
        r"$\Rightarrow OD$ là đường trung trực của đoạn thẳng $AB$.[[br]]"
        r"b) Vì $OD$ là đường trung trực của đoạn thẳng $AB$ $\Rightarrow OD \perp AB$.[[br]]"
        r"Vậy $OD \perp AB$."
    )

    # Stage 3 B9 (Bài 4)
    b4 = data["stages"][2]["blocks"][8]
    b4["statement"] = (
        r"Cho đường tròn $(O)$, đường kính $MN$. Trên đường tròn $(O)$ lấy điểm $I$ ($I \ne M, I \ne N$). "
        r"Hai tiếp tuyến của đường tròn $(O)$ tại $M$ và $I$ cắt nhau ở $K$ (Hình 6). "
        r"Vẽ tiếp vào Hình 6 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $KO$ là đường trung trực của đoạn thẳng $MI$ và $KO \perp MI$.[[br]]"
        r"b) [TH] ★★ Chứng minh tam giác $MIN$ vuông tại $I$, từ đó suy ra $KO \parallel NI$."
    )
    b4["answer"] = (
        r"a) $KM$, $KI$ là hai tiếp tuyến của $(O)$ cắt nhau tại $K$ $\Rightarrow KM = KI$.[[br]]"
        r"$OM = OI$ (bán kính của $(O)$)[[br]]"
        r"$\Rightarrow KO$ là đường trung trực của đoạn thẳng $MI \Rightarrow KO \perp MI$.[[br]]"
        r"b) Xét $\triangle MIN$ có $IO$ là đường trung tuyến ứng với cạnh $MN$ ($O$ là trung điểm của $MN$).[[br]]"
        r"$OI = OM = ON = R \Rightarrow IO = \dfrac{MN}{2}$[[br]]"
        r"$\Rightarrow \triangle MIN$ vuông tại $I \Rightarrow NI \perp MI$.[[br]]"
        r"Mà $KO \perp MI$ (theo câu a).[[br]]"
        r"Vậy $KO \parallel NI$."
    )

    # Stage 5 B4 (BTVN 3)
    bt3 = data["stages"][4]["blocks"][3]
    bt3["statement"] = (
        r"Cho đường tròn $(O; R)$ và một điểm $A$ nằm bên ngoài đường tròn sao cho $OA > 2R$. "
        r"Qua $A$ kẻ hai tiếp tuyến $AM$, $AN$ với đường tròn $(O)$ ($M$, $N$ là hai tiếp điểm). "
        r"Gọi $H$ là giao điểm của $OA$ và $MN$ (Hình 10). "
        r"Vẽ tiếp vào Hình 10 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $OA$ là đường trung trực của đoạn thẳng $MN$.[[br]]"
        r"b) [TH] ★★ Chứng minh $OA \perp MN$ tại $H$."
    )
    bt3["answer"] = (
        r"a) $AM$, $AN$ là hai tiếp tuyến của $(O)$ cắt nhau tại $A$ $\Rightarrow AM = AN$.[[br]]"
        r"$OM = ON$ (bán kính của $(O)$)[[br]]"
        r"$\Rightarrow OA$ là đường trung trực của đoạn thẳng $MN$.[[br]]"
        r"b) Vì $OA$ là đường trung trực của đoạn thẳng $MN$ mà $H \in MN$ nên $OA \perp MN$ tại $H$.[[br]]"
        r"Vậy $OA \perp MN$ tại $H$."
    )

    # Stage 5 B5 (BTVN 4)
    bt4 = data["stages"][4]["blocks"][4]
    bt4["statement"] = (
        r"Cho đường tròn $(O; R)$, đường kính $AB$. Trên đường tròn $(O)$ lấy điểm $M$ ($MA < MB$). "
        r"Tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ và $B$ lần lượt là $C$ và $D$ (Hình 11). "
        r"Vẽ tiếp vào Hình 11 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $OC \perp AM$.[[br]]"
        r"b) [TH] ★★ Chứng minh tam giác $AMB$ vuông tại $M$, từ đó suy ra $OC \parallel MB$."
    )
    bt4["answer"] = (
        r"a) $CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$ $\Rightarrow CA = CM$.[[br]]"
        r"$OA = OM$ (bán kính của $(O)$)[[br]]"
        r"$\Rightarrow OC$ là đường trung trực của đoạn thẳng $AM \Rightarrow OC \perp AM$.[[br]]"
        r"b) Xét $\triangle AMB$ có $MO$ là đường trung tuyến ứng với cạnh $AB$ ($O$ là trung điểm của $AB$).[[br]]"
        r"$OM = OA = OB = R \Rightarrow MO = \dfrac{AB}{2}$[[br]]"
        r"$\Rightarrow \triangle AMB$ vuông tại $M \Rightarrow BM \perp AM$.[[br]]"
        r"Mà $OC \perp AM$ (theo câu a).[[br]]"
        r"Vậy $OC \parallel MB$."
    )

    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-3")


def update_phieu_4():
    fpath = CH5_DIR / "phieu-4-chung-minh-he-thuc-tich-bang-dong-dang.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    clean_so_do_from_blocks(data["stages"])

    # Stage 3 B13 (Bài 6 / Bài 8)
    b6 = data["stages"][2]["blocks"][12]
    b6["statement"] = (
        r"Cho đường tròn $(O; R)$ đường kính $AB$, lấy điểm $M$ bất kì trên đường tròn ($M \ne A$, $M \ne B$), "
        r"tiếp tuyến tại $A$ và $M$ cắt nhau tại $C$. Qua $O$ kẻ đường thẳng vuông góc với dây cung $MB$ "
        r"cắt tia $CM$ tại $D$, $OD$ cắt $MB$ tại $H$ (Hình 5). "
        r"Vẽ tiếp vào Hình 5 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh tam giác $OMD$ vuông tại $M$.[[br]]"
        r"b) [TH] ★★ Chứng minh $\triangle OHM \backsim \triangle OMD$ (g.g) và suy ra $OH \cdot OD = R^2$."
    )
    b6["answer"] = (
        r"a) Vì $CD$ là tiếp tuyến của $(O)$ tại $M$ $\Rightarrow CD \perp OM$ tại $M \Rightarrow \triangle OMD$ vuông tại $M$.[[br]]"
        r"b) Xét $\triangle OHM$ và $\triangle OMD$ có:[[br]]"
        r"$\widehat{OHM} = \widehat{OMD} = 90^\circ$ ($OD \perp MB$ tại $H$, $CD \perp OM$ tại $M$)[[br]]"
        r"$\widehat{MOD}$ chung[[br]]"
        r"$\Rightarrow \triangle OHM \backsim \triangle OMD$ (g.g)[[br]]"
        r"$\Rightarrow \dfrac{OH}{OM} = \dfrac{OM}{OD}$[[br]]"
        r"$\Rightarrow OH \cdot OD = OM^2$.[[br]]"
        r"Vậy $OH \cdot OD = R^2$ (vì $OM = R$)."
    )

    # Stage 5 B9 (BTVN 8)
    bt8 = data["stages"][4]["blocks"][8]
    bt8["statement"] = (
        r"Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $AD$ ($D \in BC$). "
        r"Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$ và $AC$ (Hình 8). "
        r"Vẽ tiếp vào Hình 8 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $\triangle AED \backsim \triangle ADB$ và suy ra $AE \cdot AB = AD^2$.[[br]]"
        r"b) [TH] ★★ Chứng minh $\triangle AFD \backsim \triangle ADC$ và suy ra $AE \cdot AB = AF \cdot AC$."
    )
    bt8["answer"] = (
        r"a) Xét $\triangle AED$ và $\triangle ADB$ có:[[br]]"
        r"$\widehat{AED} = \widehat{ADB} = 90^\circ$ ($DE \perp AB$ tại $E$, $AD \perp BC$ tại $D$)[[br]]"
        r"$\widehat{BAD}$ chung[[br]]"
        r"$\Rightarrow \triangle AED \backsim \triangle ADB$ (g.g)[[br]]"
        r"$\Rightarrow \dfrac{AE}{AD} = \dfrac{AD}{AB} \Rightarrow AE \cdot AB = AD^2$.[[br]]"
        r"b) Tương tự, xét $\triangle AFD$ và $\triangle ADC$ có:[[br]]"
        r"$\widehat{AFD} = \widehat{ADC} = 90^\circ$ ($DF \perp AC$ tại $F$, $AD \perp BC$ tại $D$)[[br]]"
        r"$\widehat{CAD}$ chung[[br]]"
        r"$\Rightarrow \triangle AFD \backsim \triangle ADC$ (g.g)[[br]]"
        r"$\Rightarrow \dfrac{AF}{AD} = \dfrac{AD}{AC} \Rightarrow AF \cdot AC = AD^2$.[[br]]"
        r"Từ câu a và câu b suy ra $AE \cdot AB = AF \cdot AC$ ($= AD^2$).[[br]]"
        r"Vậy $AE \cdot AB = AF \cdot AC$."
    )

    # Stage 5 B10 (BTVN 9)
    bt9 = data["stages"][4]["blocks"][9]
    bt9["statement"] = (
        r"Cho nửa đường tròn $(O; R)$, đường kính $AB$. Từ điểm $M$ bất kì trên tiếp tuyến $Ax$ của nửa đường tròn $(O)$ "
        r"vẽ tiếp tuyến thứ hai $MC$ ($C$ là tiếp điểm). Gọi $I$ là giao điểm của $OM$ và $AC$ (Hình 9). "
        r"Vẽ tiếp vào Hình 9 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh $OM \perp AC$ tại $I$.[[br]]"
        r"b) [TH] ★★ Chứng minh $\triangle OIA \backsim \triangle OAM$ (g.g) và suy ra $OI \cdot OM = R^2$."
    )
    bt9["answer"] = (
        r"a) $MA$, $MC$ là hai tiếp tuyến của $(O)$ cắt nhau tại $M$ $\Rightarrow MA = MC$.[[br]]"
        r"$OA = OC$ (bán kính của $(O)$)[[br]]"
        r"$\Rightarrow OM$ là đường trung trực của đoạn thẳng $AC \Rightarrow OM \perp AC$ tại $I$.[[br]]"
        r"b) Xét $\triangle OIA$ và $\triangle OAM$ có:[[br]]"
        r"$\widehat{OIA} = \widehat{OAM} = 90^\circ$ ($OM \perp AC$ tại $I$, $MA$ là tiếp tuyến của $(O)$ tại $A$)[[br]]"
        r"$\widehat{AOM}$ chung[[br]]"
        r"$\Rightarrow \triangle OIA \backsim \triangle OAM$ (g.g)[[br]]"
        r"$\Rightarrow \dfrac{OI}{OA} = \dfrac{OA}{OM}$[[br]]"
        r"$\Rightarrow OI \cdot OM = OA^2$.[[br]]"
        r"Vậy $OI \cdot OM = R^2$ (vì $OA = R$)."
    )

    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-4")


def update_phieu_5():
    fpath = CH5_DIR / "phieu-5-luyen-tap-chung.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    clean_so_do_from_blocks(data["stages"])

    # Stage 3 B7 (Bài 3)
    b3 = data["stages"][2]["blocks"][6]
    b3["statement"] = (
        r"Cho đường tròn $(O; R)$, đường kính $AB$. Trên đường tròn $(O)$ lấy điểm $M$ ($MA < MB$). "
        r"Tiếp tuyến tại $M$ cắt tiếp tuyến tại $A$ và $B$ lần lượt là $C$ và $D$ (Hình 5). "
        r"Vẽ tiếp vào Hình 5 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [NB] ★ Chứng minh $CA = CM$ và $DB = DM$.[[br]]"
        r"b) [TH] ★★ Chứng minh rằng $CD = AC + BD$."
    )
    b3["answer"] = (
        r"a) $CA$, $CM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $C$ $\Rightarrow CA = CM$.[[br]]"
        r"$DB$, $DM$ là hai tiếp tuyến của $(O)$ cắt nhau tại $D$ $\Rightarrow DB = DM$.[[br]]"
        r"b) Vì $M$ nằm giữa $C$ và $D$ nên $CD = CM + DM$.[[br]]"
        r"Mà $CM = AC$ và $DM = BD$ (theo câu a).[[br]]"
        r"Vậy $CD = AC + BD$."
    )

    # Stage 3 B10 (Bài 4)
    b4 = data["stages"][2]["blocks"][9]
    b4["statement"] = (
        r"Cho nửa đường tròn $(O, R)$ đường kính $AB$. Kẻ tiếp tuyến $Ax$ cùng phía với nửa đường tròn. "
        r"Trên tia $Ax$ lấy điểm $C$, kẻ tiếp tuyến thứ hai $CM$ tới nửa đường tròn. "
        r"Đường thẳng vuông góc với $OC$ tại $O$ cắt tiếp tuyến tại $B$ của $(O)$ ở $D$. "
        r"Biết ba điểm $C$, $M$, $D$ thẳng hàng (Hình 7). "
        r"Vẽ tiếp vào Hình 7 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh rằng $\widehat{MCO} = \widehat{MOD}$.[[br]]"
        r"b) [TH] ★★ Chứng minh $\triangle MCO \backsim \triangle MOD$ (g.g) và suy ra $MC \cdot MD = R^2$."
    )
    b4["answer"] = (
        r"a) $\widehat{COD} = 90^\circ$ ($OD \perp OC$ tại $O$) $\Rightarrow \widehat{MCO} = \widehat{MOD}$ (cùng phụ với $\widehat{COM}$).[[br]]"
        r"b) Xét $\triangle MCO$ và $\triangle MOD$ có:[[br]]"
        r"$\widehat{CMO} = \widehat{OMD} = 90^\circ$ ($CD$ là tiếp tuyến của $(O)$ tại $M$)[[br]]"
        r"$\widehat{MCO} = \widehat{MOD}$ (theo câu a)[[br]]"
        r"$\Rightarrow \triangle MCO \backsim \triangle MOD$ (g.g)[[br]]"
        r"$\Rightarrow \dfrac{MC}{MO} = \dfrac{MO}{MD}$[[br]]"
        r"$\Rightarrow MC \cdot MD = OM^2$.[[br]]"
        r"Vậy $MC \cdot MD = R^2$ (vì $OM = R$)."
    )

    # Stage 5 B7 (BTVN 6)
    bt6 = data["stages"][4]["blocks"][6]
    bt6["statement"] = (
        r"Cho đường tròn $(O)$, đường kính $AB$. Kẻ tiếp tuyến $Ax$ với đường tròn $(O)$. "
        r"Lấy điểm $C$ thuộc đường tròn $(O)$ ($AC < CB$). Kẻ tiếp tuyến tại $C$ của đường tròn $(O)$ "
        r"cắt $Ax$ tại điểm $M$ (Hình 12). "
        r"Vẽ tiếp vào Hình 12 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [NB] ★ Chứng minh các tam giác $MAO$ và $MCO$ là các tam giác vuông.[[br]]"
        r"b) [TH] ★★ Chứng minh bốn điểm $M$, $A$, $C$, $O$ cùng thuộc một đường tròn."
    )
    bt6["answer"] = (
        r"a) $MA$ là tiếp tuyến của $(O)$ tại $A$ $\Rightarrow MA \perp OA$ tại $A \Rightarrow \triangle MAO$ vuông tại $A$.[[br]]"
        r"$MC$ là tiếp tuyến của $(O)$ tại $C$ $\Rightarrow MC \perp OC$ tại $C \Rightarrow \triangle MCO$ vuông tại $C$.[[br]]"
        r"b) $\triangle MAO$ vuông tại $A \Rightarrow M, A, O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
        r"$\triangle MCO$ vuông tại $C \Rightarrow M, C, O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
        r"Vậy bốn điểm $M, A, C, O$ cùng thuộc đường tròn đường kính $MO$."
    )

    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-5")


def update_phieu_6():
    fpath = CH5_DIR / "phieu-6-bai-tap-cuoi-chuong-v.json"
    data = json.loads(fpath.read_text(encoding="utf-8"))
    clean_so_do_from_blocks(data["stages"])

    # Stage 5 B7 (BTVN 6)
    bt6 = data["stages"][4]["blocks"][6]
    bt6["statement"] = (
        r"Cho tam giác $ABC$ nhọn ($AB < AC$) có hai đường cao $BD$ và $CE$ cắt nhau tại $H$ (Hình 7). "
        r"Vẽ tiếp vào Hình 7 các yếu tố còn thiếu theo đề:[[br]]"
        r"a) [TH] ★★ Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng nằm trên một đường tròn. Xác định tâm $I$ của đường tròn này.[[br]]"
        r"b) [TH] ★★ Chứng minh $AE \cdot AB = AD \cdot AC$."
    )

    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✓ Updated phieu-6")


if __name__ == "__main__":
    update_phieu_3()
    update_phieu_4()
    update_phieu_5()
    update_phieu_6()
    print("ALL 4 FILES UPDATED SUCCESSFULLY!")

