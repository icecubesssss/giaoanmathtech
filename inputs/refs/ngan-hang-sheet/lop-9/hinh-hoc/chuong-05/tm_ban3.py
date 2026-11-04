# Dựng lại thuyết minh ch.V 9C (03/11/2026) từ tab "Chọn câu Ch.V lớp 9C".
# Giữ P1 (đã duyệt) + khối chữ đầu; viết lại P2–P6 theo câu đã chọn.
# Chạy: python3 tm.py <backup thuyet-minh.json> <out thuyet-minh.json>
import json, sys

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))


def R(band, loai, dang, refs, vidu=0, onclass=0, btvn=0, lythuyet=0, hinh_san=False,
      ve=None, gian_giao="", quy_trinh=None):
    dec = {"VD": "vd", "TH": "th2nb"}.get(band, "none")
    if band == "TH" and loai == "TH lẻ LT":
        dec = "none"
    r = dict(band=band, loai=loai, dang=dang, source_refs=refs, vidu=vidu, onclass=onclass,
             btvn=btvn, lythuyet=lythuyet, decompose=dec, hinh_san=hinh_san)
    if ve:
        r["ve_hinh"] = ve
    if gian_giao:
        r["gian_giao"] = gian_giao
    if quy_trinh:
        r["quy_trinh"] = quy_trinh
    return r


VE = {"onclass": 0, "btvn": 1}

P2 = [
    R("NB", "NB kiến thức cũ",
      "Tam giác vuông: trung tuyến ứng với cạnh huyền bằng nửa cạnh huyền $\\Rightarrow$ đỉnh góc vuông thuộc đường tròn đường kính cạnh huyền (ví dụ điền khuyết, trắc nghiệm)",
      ["sgk-b13-lt1", "stk-b13-I-C17-tr8"], vidu=1, onclass=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT",
      "Vị trí tương đối của đường thẳng và đường tròn theo $d$ và $R$: trắc nghiệm, bài thực tế dán bốn hình tròn lên hai đường thẳng song song, bảng điền $d$ – $R$",
      ["sgk-5.35", "sgk-b16-lt1", "sgk-5.20"], onclass=5, btvn=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Vị trí của một điểm đối với đường tròn (so $OM$ với $R$, trắc nghiệm)",
      ["stk-b13-I-C7-tr5"], btvn=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Tiếp tuyến vuông góc với bán kính \\textbf{tại tiếp điểm} (trắc nghiệm — bẫy \\textquotedblleft tại $O$\\textquotedblright)",
      ["stk-b16-I-C4-tr232"], onclass=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Tam giác có hai đường cao $BD$, $CE$ $\\Rightarrow$ bốn điểm $B$, $E$, $D$, $C$ cùng thuộc đường tròn đường kính $BC$ (trắc nghiệm, trả lời ngắn bán kính)",
      ["tl-1-19", "stk-b13-III-C33-tr13"], onclass=1, btvn=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Đúng/Sai trên hình hai đường cao in sẵn: điểm thuộc đường tròn đường kính $AH$, $DE$ là tiếp tuyến (4 khẳng định)",
      ["stk-b16-II-C45-tr246"], onclass=4, hinh_san=True),
    R("NB", "NB ghép bài", "Hình vẽ sẵn (đề Lý Sơn): điền \\textquotedblleft$\\widehat{MAO} = 90^\\circ$ vì $Ax$ là tiếp tuyến\\textquotedblright, góc vuông thứ hai, tâm và bán kính đường tròn qua bốn điểm",
      ["ck1-ly-son-2025-IV2.a"], onclass=3, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Bốn điểm: đánh dấu hai góc vuông (do tiếp tuyến, do đường vuông góc), chỉ cạnh huyền chung, nêu tâm là trung điểm cạnh huyền (điền trên hình)",
      ["ck1-hoang-liet-2025-4.2.a", "gk1-trung-vuong-2025-IV"], onclass=3, btvn=1, hinh_san=True, gian_giao="ve-hinh"),
    R("NB", "NB tách TH", "Chứng minh tiếp tuyến: $OC \\perp AB$ $\\Rightarrow$ $OC$ là đường trung trực của $AB$ $\\Rightarrow \\triangle OAC = \\triangle OBC$ (c.c.c) $\\Rightarrow \\widehat{OBC} = 90^\\circ$ (điền khung)",
      ["sgk-b16-vd1", "v10-dong-da-de04-IV2.b"], onclass=3, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Tam giác cân $OCD$ có $OH$ là đường cao $\\Rightarrow AB$ là đường trung trực của $CD$ $\\Rightarrow FC = FD$ (bước đầu ý b đề Ái Mộ, điền)",
      ["ck1-ai-mo-2.b"], onclass=2, hinh_san=True),
    R("TH", "TH ghép bài", "Chứng minh bốn điểm cùng thuộc một đường tròn (Câu IV.2 ý a — 38/46 đề cuối kì I): HS tự vẽ hình, hai tam giác vuông chung cạnh huyền, nêu tâm và bán kính",
      ["ck1-hoang-liet-2025-4.2.a", "gk1-trung-vuong-2025-IV", "gk1-luong-the-vinh-2025-4.2.a"], onclass=2, btvn=1, ve=VE),
    R("TH", "TH tách VD", "Chứng minh một đường thẳng là tiếp tuyến: hai tam giác bằng nhau cho góc $90^\\circ$, rồi dấu hiệu nhận biết (SGK Ví dụ 1, đề Đống Đa 04, đề Chu Văn An)",
      ["sgk-5.21", "sgk-b16-vd1", "v10-dong-da-de04-IV2", "ck1-chu-van-an-2024-IV2"], vidu=1, onclass=3, btvn=2, ve=VE),
    R("VD", "VD lẻ", "Đề thi Câu IV.2 hai ý (đề Ái Mộ): bốn điểm $A$, $C$, $M$, $O$; $DF$ là tiếp tuyến (tam giác cân $\\to$ hai tam giác bằng nhau $\\to$ dấu hiệu nhận biết) — HS tự vẽ hình, trình bày trọn. Ví dụ đề mẫu: đề Tân Triều. BTVN: đề Hát Môn (đề song song)",
      ["ck1-ai-mo-2", "ck1-tan-trieu-42", "ck1-hat-mon-2025-IV2"], vidu=1, onclass=1, btvn=1, ve=VE,
      quy_trinh=["Ý a: hai góc vuông tại hai tiếp điểm có chung cạnh huyền $OM$ $\\Rightarrow$ bốn điểm, nêu tâm và bán kính",
                 "Ý b: $\\triangle OCD$ cân, $OH \\perp CD$ $\\Rightarrow AB$ là đường trung trực của $CD$ $\\Rightarrow FC = FD$",
                 "$\\triangle OCF = \\triangle ODF$ (c.c.c) $\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$",
                 "Kết luận theo dấu hiệu nhận biết tiếp tuyến"]),
]

P3 = [
    R("NB", "NB kiến thức cũ", "Đường trung trực của một đoạn thẳng (Lớp 7): điểm cách đều hai đầu mút thuộc đường trung trực (trắc nghiệm chọn khẳng định sai)",
      ["stk-b13-I-C13-tr6"], onclass=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Định lí hai tiếp tuyến cắt nhau: chọn khẳng định sai, điền cụm từ (góc tạo bởi hai tiếp tuyến / hai bán kính)",
      ["stk-b16-I-C7-tr232", "stk-b16-I-C8-tr232"], onclass=2, btvn=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Tính góc trên hình hai tiếp tuyến bằng tính chất tia phân giác: $\\widehat{AMO}$, $\\widehat{MOB}$, số đo cung nhỏ $CD$ (trắc nghiệm, trả lời ngắn)",
      ["stk-b16-I-C19-tr235", "stk-b16-III-C60-tr252", "stk-b16-III-C58-tr252"], onclass=3, btvn=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Đúng/Sai trên hình hai tiếp tuyến in sẵn: $AM = AN$, $OA \\perp MN$, so sánh góc, chu vi (4 khẳng định)",
      ["stk-b16-II-C30-tr239"], onclass=4, hinh_san=True),
    R("NB", "NB ghép bài", "Hình vẽ sẵn (đề Giảng Võ): điền $AB = AC$ (hai tiếp tuyến), $OB = OC = R$ $\\Rightarrow OA$ là đường trung trực của $BC$",
      ["ck1-giang-vo-2025-IV2.a"], onclass=4, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Hình hai tiếp tuyến vẽ sẵn: $SA = SB$, $OA = OB$ $\\Rightarrow SO$ là đường trung trực của $AB$ $\\Rightarrow SO \\perp AB$ tại trung điểm $H$ (điền)",
      ["ck1-phuc-dong-IV2.b", "sgk-b16-vd2.a"], vidu=1, onclass=2, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Có đường kính: $BD$ là đường kính $\\Rightarrow \\triangle BCD$ vuông tại $C$ (trung tuyến bằng nửa cạnh); hai đường cùng vuông góc với $BC$ $\\Rightarrow OA \\parallel CD$ (điền)",
      ["ck1-phuc-dong-IV2.b"], onclass=2, hinh_san=True),
    R("NB", "NB tách TH", "Nửa đường tròn, tiếp tuyến tại $A$ và $D$ cắt nhau tại $C$: $OC$ là đường trung trực của $AD$; $BD \\perp AD$ $\\Rightarrow OC \\parallel BD$ (điền)",
      ["ck1-ba-dinh-2024-IV2.b", "ck1-dong-da-2025-IV2.b"], vidu=1, onclass=2, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("TH", "TH lẻ LT", "Chứng minh hai tiếp tuyến cắt nhau và dùng tính chất của chúng (SGK HĐ4, 5.22, 5.23, 5.39): hai tam giác bằng nhau, cộng đoạn tính chu vi",
      ["sgk-b16-hd4", "sgk-5.22", "sgk-5.23", "sgk-5.39"], vidu=1, onclass=2, btvn=2, ve=VE),
    R("TH", "TH tách VD", "Chứng minh $OA \\perp BC$ (đường trung trực) và song song khi có đường kính đi qua tiếp điểm (Câu IV.2 ý b — 24/46 và 10/46 đề)",
      ["sgk-b16-vd2.a", "ck1-dong-da-2025-IV2"], vidu=1, btvn=2, ve=VE),
    R("VD", "VD lẻ", "Đề thi Câu IV.2 hai ý (đề Phúc Đồng): bốn điểm $A$, $B$, $C$, $O$; $OA \\perp BC$ tại $H$ và $OA \\parallel CD$ (trung trực $\\to$ đường kính cho góc vuông $\\to$ cùng vuông góc). Ví dụ đề mẫu: đề Ba Đình 2024. BTVN: đề Ngọc Lâm cùng khuôn",
      ["ck1-phuc-dong-IV2", "ck1-ba-dinh-2024-IV2", "ck1-ngoc-lam-IV2"], vidu=1, onclass=1, btvn=1, ve=VE,
      quy_trinh=["Ý a: hai góc vuông tại hai tiếp điểm có chung cạnh huyền $OA$ $\\Rightarrow$ bốn điểm, nêu tâm và bán kính",
                 "Ý b: $AB = AC$ (Định lí 2), $OB = OC = R$ $\\Rightarrow OA$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$ tại $H$",
                 "$BD$ là đường kính $\\Rightarrow \\triangle BCD$ vuông tại $C$ $\\Rightarrow CD \\perp BC$",
                 "Hai đường thẳng cùng vuông góc với $BC$ $\\Rightarrow OA \\parallel CD$"]),
]

P4 = [
    R("NB", "NB kiến thức cũ", "Hai tam giác vuông có chung một góc nhọn thì đồng dạng (Lớp 8) — Đúng/Sai trên hình in sẵn: $\\triangle OIC \\backsim \\triangle OCE$, bẫy $OI \\cdot OE = 2R$",
      ["stk-b16-II-C35-tr241"], onclass=4, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Đúng/Sai không số trên hình hai tiếp tuyến (bốn điểm, góc đồng vị, $MB \\cdot BC = BK \\cdot MO$; $OH \\cdot OM = R^2$, $\\triangle ODM \\backsim \\triangle OHD$)",
      ["stk-b16-II-C47-tr247", "stk-b16-II-C49-tr248"], onclass=4, btvn=4, hinh_san=True),
    R("NB", "NB ghép bài", "Hình vẽ sẵn: điền cặp góc bằng nhau để có $\\triangle DBC \\backsim \\triangle BAH$ (đề Ngôi Sao), $OH \\cdot OA = R^2$ (đề Marie Curie) — đúng thứ tự đỉnh tương ứng",
      ["ck1-ngoi-sao-2024-4.2.b", "ck1-marie-curie-2025-4.b"], onclass=3, btvn=2, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Hình hai tiếp tuyến vẽ sẵn: $\\triangle OHB \\backsim \\triangle OBA$ (g.g) $\\Rightarrow \\dfrac{OH}{OB} = \\dfrac{OB}{OA} \\Rightarrow OH \\cdot OA = R^2$ (điền)",
      ["ck1-ngo-gia-tu-2025-IV2.b", "ck1-cum-14-2025-4.2.b"], vidu=1, onclass=3, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Có đường kính: $\\triangle AKB$ vuông tại $K$ rồi $\\triangle BKA \\backsim \\triangle BAC$ $\\Rightarrow BK \\cdot BC = AB^2$ (điền)",
      ["ck1-cau-giay-2024-IV2.b", "ck1-dich-vong-42.b"], vidu=1, onclass=2, btvn=1, hinh_san=True),
    R("NB", "NB tách TH", "Bắc cầu qua $MA^2$: $MA^2 = MH \\cdot MO$ và $MA^2 = MC \\cdot MD$ $\\Rightarrow MH \\cdot MO = MC \\cdot MD$ (điền)",
      ["ck1-ta-quang-buu-2025-IV2.b", "ck1-ngoc-thuy-III2.b"], onclass=2, hinh_san=True),
    R("TH", "TH tách VD", "Chứng minh $OA \\perp BC$ và $OH \\cdot OA = R^2$ trên hình hai tiếp tuyến (Câu IV.2 ý b — đẳng thức tích gặp nhiều nhất)",
      ["ck1-cum-14-2025-4.2", "ck1-ngo-gia-tu-2025-IV2", "ck1-gia-lam-2024-4.2"], vidu=1, onclass=2, btvn=2, ve=VE),
    R("TH", "TH tách VD", "Có đường kính: chứng minh tam giác vuông rồi đẳng thức tích ($CH \\cdot CA = 2R^2$, $CE \\cdot CB = CA^2$, $CA \\cdot CE = 4R^2$)",
      ["ck1-dich-vong-42", "ck1-cau-giay-2024-IV2", "ck1-thanh-tri-2024-IV2", "ck1-nguyen-binh-khiem-2025-4.2"], vidu=1, onclass=2, btvn=2, ve=VE),
    R("VD", "VD lẻ", "Đề thi Câu IV.2 hai ý (đề Tạ Quang Bửu): bốn điểm $M$, $A$, $O$, $B$; $AB \\perp OM$ và $MH \\cdot MO = MC \\cdot MD$ (hai cặp tam giác đồng dạng, bắc cầu qua $MA^2$). Ví dụ đề mẫu: đề Ngọc Thụy. BTVN: đề Xuân La",
      ["ck1-ta-quang-buu-2025-IV2", "ck1-ngoc-thuy-III2", "ck1-xuan-la-2024-4.2"], vidu=1, onclass=1, btvn=1, ve=VE,
      quy_trinh=["Ý a: hai góc vuông tại hai tiếp điểm có chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm, nêu tâm và bán kính",
                 "Ý b: $MA = MB$, $OA = OB$ $\\Rightarrow OM$ là đường trung trực của $AB$ $\\Rightarrow AB \\perp OM$ tại $H$",
                 "$\\triangle MHA \\backsim \\triangle MAO$ (g.g) $\\Rightarrow MA^2 = MH \\cdot MO$",
                 "$AD$ là đường kính $\\Rightarrow \\triangle ACD$ vuông tại $C$; $\\triangle MCA \\backsim \\triangle MAD$ (g.g) $\\Rightarrow MA^2 = MC \\cdot MD$",
                 "Bắc cầu qua $MA^2$"]),
]

P5 = [
    R("NB", "NB kiến thức cũ", "Hai tia phân giác của hai góc kề bù thì vuông góc (Lớp 7) — Đúng/Sai trên hình ba tiếp tuyến: $\\widehat{MON} = 90^\\circ$, $MN = AM + BN$, $AM \\cdot BN = R^2$",
      ["stk-b16-II-C31-tr239"], onclass=4, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Câu IV.1 khởi động: độ dài cung (con lắc), diện tích hình quạt, hình vành khuyên (đèn thả) — trắc nghiệm, trả lời ngắn có hình",
      ["ck1-ban-mai-2024-6a", "ck1-hai-ba-trung-2024-IV1", "ck1-ngoi-sao-2024-4.1"], onclass=2, btvn=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Hai tiếp tuyến cắt nhau tạo góc $50^\\circ$ $\\Rightarrow$ số đo cung nhỏ, cung lớn (trắc nghiệm)",
      ["stk-b16-I-C20-tr235"], onclass=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Đúng/Sai trên hình ba tiếp tuyến: $\\widehat{COD} = 90^\\circ$, $MC \\cdot MD$ so với $OM^2$, độ dài theo $R$",
      ["stk-b16-II-C50-tr249"], btvn=4, hinh_san=True),
    R("NB", "NB ghép bài", "Hình nửa đường tròn in sẵn (đề Quốc Oai): điền hai góc vuông tại $A$, $M$ $\\Rightarrow$ bốn điểm $A$, $O$, $M$, $C$",
      ["ck1-quoc-oai-2024-4.2.a"], onclass=3, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Ba tiếp tuyến: $CA = CM$, $DB = DM$ (Định lí 2) $\\Rightarrow CD = AC + BD$ (điền trên hình)",
      ["ck1-cau-dien-42.a", "sgk-5.30.a"], onclass=2, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Hình ba tiếp tuyến: $OD$ là trung trực của $MB$, $OC$ là trung trực của $AM$, $\\triangle AMB$ vuông tại $M$ $\\Rightarrow MB \\perp OD$, $MB \\parallel OC$ (điền)",
      ["ck1-ngo-si-lien-2024-7.b"], onclass=3, btvn=1, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Bài gương treo: dây tiếp xúc viền gương $\\Rightarrow OA \\perp MA$, chọn tỉ số lượng giác của $\\widehat{AMO}$ (điền)",
      ["ck1-phuong-ba-dinh-2025-IV1"], onclass=1, hinh_san=True),
    R("TH", "TH tách VD", "Hình ba tiếp tuyến của nửa đường tròn: $CD = AC + BD$, $OC \\parallel MB$, đẳng thức tích (đề Cầu Diễn, đề Marie Curie 2024)",
      ["ck1-cau-dien-42", "ck1-marie-curie-2024-4"], onclass=2, btvn=2, ve=VE),
    R("TH", "TH ghép bài", "Bài thực tế Câu IV.1 hai ý: chiều dài hàng rào (cung $+$ hai bán kính) và diện tích phần còn lại (bồn cây, công viên hình quạt)",
      ["gk2-nam-tu-liem-2025-IV1", "v10-tho-loc-3-2025-IV1"], onclass=2, btvn=2),
    R("TH", "TH lẻ LT", "Bài thực tế tiếp tuyến: gương treo bằng hai dây tiếp xúc ($MA = 25\\sqrt{3} \\approx 43$ cm); ví dụ tầm nhìn từ độ cao $5$ m; BTVN tính bán kính gương",
      ["ck1-phuong-ba-dinh-2025-IV1", "stk-b16-III-C56-tr251", "stk-b16-III-C57-tr252"], vidu=1, onclass=1, btvn=1, hinh_san=False),
    R("VD", "VD lẻ", "Đề thi Câu IV.2 (đề Ngô Sĩ Liên 2024): hình ba tiếp tuyến của nửa đường tròn — bốn điểm $C$, $M$, $O$, $A$ thuộc đường tròn đường kính $OC$; $MB \\perp OD$ và $MB \\parallel OC$; $BK$ là tia phân giác của $\\widehat{MBD}$. Ví dụ đề mẫu: SGK 5.30. BTVN: đề Lý Thánh Tông",
      ["ck1-ngo-si-lien-2024-7", "sgk-5.30", "ck1-ly-thanh-tong-7"], vidu=1, onclass=1, btvn=1, ve=VE,
      quy_trinh=["Ý a: hai góc vuông tại $A$, $M$ có chung cạnh huyền $OC$ $\\Rightarrow$ bốn điểm thuộc đường tròn tâm $I$ đường kính $OC$",
                 "Ý b: $DM = DB$, $OM = OB$ $\\Rightarrow OD$ là đường trung trực của $MB$ $\\Rightarrow MB \\perp OD$",
                 "$CA = CM$, $OA = OM$ $\\Rightarrow OC \\perp AM$; $\\triangle AMB$ vuông tại $M$ $\\Rightarrow MB \\parallel OC$",
                 "Ý c: $\\triangle OBK$ cân tại $O$; $OD \\perp MB$ $\\Rightarrow \\widehat{MBK} = 90^\\circ - \\widehat{OKB} = 90^\\circ - \\widehat{OBK} = \\widehat{KBD}$"]),
]

P6 = [
    R("NB", "NB lẻ LT", "Trắc nghiệm ôn chương: vị trí điểm và đường thẳng đối với đường tròn, số đo cung, trục đối xứng",
      ["sgk-5.32", "stk-b16-I-C9-tr232", "sgk-5.33", "stk-b16-I-C10-tr233", "tl-1-35"], onclass=3, btvn=2, hinh_san=True),
    R("NB", "NB kiến thức cũ", "Hai góc so le trong và tam giác cân (Lớp 7) trên hình hai tiếp tuyến: đường thẳng qua $I$ song song $OA$ $\\Rightarrow KI = KO$ (trắc nghiệm)",
      ["stk-b16-I-C25-tr237"], onclass=1, hinh_san=True),
    R("NB", "NB tách TH", "Tam giác có hai đường cao vẽ sẵn: hai tam giác vuông chung cạnh huyền $BC$ $\\Rightarrow$ bốn điểm, tâm là trung điểm $BC$ (điền)",
      ["gk1-thanh-quan-2024-IV"], onclass=1, hinh_san=True, gian_giao="ve-hinh"),
    R("NB", "NB tách TH", "Hình hai tiếp tuyến in sẵn: điền ý 1 (bốn điểm) và nửa đầu ý 2 ($OA \\perp BC$) của đề mẫu",
      ["ck1-nguyen-truong-to-2025-IV"], onclass=2, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "BTVN: $OI \\cdot OM = R^2$ trên hình hai tiếp tuyến (đề Ban Mai, điền)",
      ["ck1-ban-mai-2024-3.b"], btvn=1, hinh_san=True),
    R("TH", "TH ghép bài", "Bài thực tế Câu IV.1 có hình minh hoạ: diện tích hình vành khuyên (long đen, khăn trải bàn)",
      ["v10-chuong-my-l4-2025-IV1", "ck1-cum-14-2025-4.1"], onclass=2, btvn=1),
    R("TH", "TH tách VD", "Tam giác có hai đường cao: chứng minh bốn điểm cùng thuộc một đường tròn và $AB \\cdot AE = AC \\cdot AD$",
      ["gk1-thanh-quan-2024-IV"], onclass=1, ve={"onclass": 1}),
    R("VD", "VD lẻ", "Đề mẫu Câu IV.2 trọn ba ý (đề Nguyễn Trường Tộ, hình in sẵn, điền khuyết): bốn điểm; $OA \\perp BC$ và $OA \\cdot OH = R^2$; $AM \\cdot AN = AH \\cdot AO$. BTVN: đề Ban Mai (bốn điểm, $OI \\cdot OM = R^2$, $OAHB$ là hình thoi)",
      ["ck1-nguyen-truong-to-2025-IV", "ck1-ban-mai-2024-3"], onclass=1, btvn=1, hinh_san=True,
      quy_trinh=["Ý 1: hai góc vuông tại $B$, $C$ có chung cạnh huyền $AO$ $\\Rightarrow$ bốn điểm, nêu tâm và bán kính",
                 "Ý 2: $AO$ là đường trung trực của $BC$ $\\Rightarrow OA \\perp BC$; $\\triangle OHB \\backsim \\triangle OBA$ (g.g) $\\Rightarrow OA \\cdot OH = R^2$",
                 "Ý 3: $\\triangle AHB \\backsim \\triangle ABO$ $\\Rightarrow AB^2 = AH \\cdot AO$; $AM \\cdot AN = (AO - R)(AO + R) = AO^2 - R^2 = AB^2$",
                 "Bắc cầu qua $AB^2$"]),
]

# ---- Cân quỹ phút (03/11 lượt 2): (vidu, onclass, btvn) theo chỉ số dòng ----
CAN = {
 0: {0:(1,1,0),1:(0,4,1),2:(0,0,1),3:(0,1,0),4:(0,1,1),5:(0,4,0),6:(0,3,0),7:(1,2,2),8:(1,2,1),9:(0,2,1),10:(0,2,1),11:(2,2,1),12:(1,1,1)},
 1: {0:(1,1,0),1:(0,2,1),2:(0,3,1),3:(0,4,0),4:(0,4,0),5:(1,2,1),6:(0,2,1),7:(1,2,1),8:(1,2,2),9:(1,2,2),10:(1,1,1)},
 2: {0:(1,4,0),1:(0,4,4),2:(0,4,2),3:(1,3,1),4:(1,2,1),5:(0,3,0),6:(1,2,2),7:(1,2,2),8:(1,1,1)},
 3: {0:(1,4,0),1:(0,2,1),2:(0,1,0),3:(0,0,4),4:(0,3,0),5:(1,3,1),6:(0,3,1),7:(1,1,0),8:(0,2,2),9:(0,2,2),10:(1,1,1),11:(1,1,1)},
 4: {0:(0,4,3),1:(0,1,0),2:(0,2,0),3:(0,2,0),4:(0,0,1),5:(0,1,1),6:(0,1,4),7:(1,1,1)},
}
for k, rows in enumerate([P2, P3, P4, P5, P6]):
    for i, (v, o, b) in CAN[k].items():
        rows[i].update(vidu=v, onclass=o, btvn=b)
P3[5]["gian_giao"] = "ve-hinh"
P4[0]["gian_giao"] = "ve-hinh"
P5[4]["gian_giao"] = "ve-hinh"
P3[9]["source_refs"] = ["sgk-b16-vd2.a", "ck1-dong-da-2025-IV2", "ck1-lomonoxop-2024-IV2"]
P3[9]["dang"] = ("Chứng minh song song khi có đường kính đi qua tiếp điểm trên hình nửa đường tròn ($OP \\perp AM$, $OP \\parallel MB$; "
                 "$KO \\parallel NI$) — Câu IV.2 ý b, 10/46 đề; HS tự vẽ hình")
P4[7]["source_refs"] = ["ck1-dich-vong-42", "ck1-cau-giay-2024-IV2", "ck1-thanh-tri-2024-IV2"]
P6[5]["source_refs"] = ["v10-chuong-my-l4-2025-IV1", "ck1-cum-14-2025-4.1"]
P6[6].update(source_refs=["gk1-thanh-quan-2024-IV", "ck1-chuong-my-2024-4.2", "ck1-hoai-duc-2024-4.2"],
             dang="Tam giác có hai đường cao: bốn điểm cùng thuộc một đường tròn và đẳng thức tích $AB \\cdot AE = AC \\cdot AD$; BTVN thêm ý tiếp tuyến bằng cộng góc (đề Chương Mỹ, Hoài Đức)",
             ve_hinh={"onclass": 1, "btvn": 2})
P6[7]["source_refs"] = ["ck1-nguyen-truong-to-2025-IV", "ck1-ban-mai-2024-3"]

# ---- Tinh chỉnh P5, P6 (câu thực tế trả lời ngắn trên hình in sẵn ⇒ hinh_san) ----
P5[1].update(onclass=3, btvn=0)          # Câu IV.1 khởi động: Ban Mai, HBT, Ngôi Sao đều trên lớp
P5[6].update(onclass=4)                  # tách MB ⊥ OD, MB ∥ OC
P5[8].update(vidu=1)                     # ví dụ ý a SGK 5.30 cho bài Cầu Diễn
P5[9].update(hinh_san=True)              # bồn cây: trả lời ngắn trên hình in sẵn
P5[10].update(hinh_san=True)             # gương treo: trả lời ngắn trên hình in sẵn
P6[5].update(hinh_san=True, onclass=1, btvn=1)
P6[6].update(vidu=1, onclass=1, btvn=4, ve_hinh={"btvn": 2})
P6[0].update(onclass=4, btvn=1)
P6[3].update(onclass=2)
P6[0].update(onclass=5, btvn=1)
P6[2].update(onclass=1)

for p, rows in zip(d["phieu"][1:], [P2, P3, P4, P5, P6]):
    p["rows"] = rows

d["title"] = "Chương V. Đường tròn — sáu buổi theo dạng đề (Bài 13 – Bài 16 SGK), dựng lại 03/11/2026 từ tab chọn câu"
d["dang_vd"][2] = ("Buổi 3 — Câu IV.2 hai ý (đề Phúc Đồng): bốn điểm $A$, $B$, $C$, $O$; $OA \\perp BC$ tại $H$ và $OA \\parallel CD$ "
                   "(trung trực $\\to$ đường kính cho góc vuông $\\to$ cùng vuông góc). BTVN: đề Ngọc Lâm cùng khuôn.")
d["dang_vd"][3] = d["dang_vd"][3]  # Tạ Quang Bửu / Xuân La — giữ
d["dang_vd"][4] = d["dang_vd"][4].replace("BTVN: đề Cầu Diễn.", "BTVN: đề Lý Thánh Tông (luyện tập chung, có ý diện tích).")
d["vidu"][1:] = [
    "Buổi 2: $\\triangle ABC$ vuông tại $A$ — $A$ thuộc đường tròn đường kính $BC$ (SGK Luyện tập 1). Tam giác cân $ABC$ nội tiếp $(O)$ — đường qua $A$ song song $BC$ là tiếp tuyến (SGK 5.21). Đề mẫu (Tân Triều): tiếp tuyến tại $A$, $M$ cắt nhau tại $C$ — bốn điểm $O$, $A$, $C$, $M$; $OH = \\frac{1}{2}AM$ và $BD$ là tiếp tuyến.",
    "Buổi 3: Hai tiếp tuyến $MA$, $MB$ — $\\triangle OMA = \\triangle OMB$ nên $MA = MB$, $MO$ là phân giác (SGK HĐ4); $OM \\perp AB$ (SGK Ví dụ 2a). Đề mẫu (Ba Đình 2024): nửa đường tròn, tiếp tuyến tại $A$ và $D$ cắt nhau tại $C$ — bốn điểm, $OC \\perp AD$ và $OC \\parallel BD$.",
    "Buổi 4: Đề mẫu (Cụm 14): nửa đường tròn — $OH \\cdot OD = R^2$ và $DB$ là tiếp tuyến. Đề mẫu (Dịch Vọng): $\\triangle AKB$ vuông, $BK \\cdot BC = 4R^2$. Đề mẫu (Ngọc Thụy): $AM \\cdot AN = (AO - R)(AO + R) = AB^2 = AH \\cdot AO$.",
    "Buổi 5: Đề mẫu (SGK 5.30): ba tiếp tuyến — $MN = MA + NB$, $Q$ là trung điểm $MN$. Thực tế: tầm nhìn từ độ cao $5$ m tới đường chân trời $\\approx 8$ km (tiếp tuyến vuông góc bán kính).",
    "Buổi 6: không có ví dụ riêng (45 phút) — đề mẫu Nguyễn Trường Tộ in sẵn hình, HS điền khuyết trọn ba ý.",
]
d["lythuyet"].insert(3, "\\textbf{Hình thức câu (Thầy chốt 03/11/2026):} câu nào không phải bài trình bày đi thi thì là trắc nghiệm, điền khuyết, Đúng/Sai hoặc trả lời ngắn trên hình in sẵn — HS trả lời gọn; chỉ ý a, b của đề Câu IV.2 là tự luận, HS tự vẽ hình. Câu được bốc từ tab \\textquotedblleft Chọn câu Ch.V lớp 9C\\textquotedblright{} (chấm T1–T8 trọng số lớp C, mỗi bài gốc một dòng).")

json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)

for p in d["phieu"]:
    nb = [r for r in p["rows"] if r["band"] == "NB"]
    tong = sum(r["onclass"] + r["btvn"] for r in nb)
    tach = sum(r["onclass"] + r["btvn"] for r in nb if r["loai"] == "NB tách TH")
    print(p["code"], "NB", tong, "tách", tach, f"{tach / tong * 100:.0f}%" if tong else "")

# ---- Khuôn bốn điểm mới (Thầy 03/11/2026): "△ABC vuông tại A ⇒ A, B, C cùng thuộc đường tròn đường kính BC" ----
d = json.load(open(out))
KH = "tam giác vuông $\\Rightarrow$ đỉnh góc vuông thuộc đường tròn đường kính cạnh huyền"
def _sub(x):
    return (x.replace("$\\Rightarrow$ bốn điểm, nêu tâm và bán kính", "$\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính cạnh huyền chung")
             .replace(", nêu tâm và bán kính", ", kết luận đường tròn đường kính cạnh huyền")
             .replace("nêu tâm là trung điểm cạnh huyền", "kết luận đường tròn đường kính cạnh huyền"))
for p in d["phieu"]:
    for r in p["rows"]:
        r["dang"] = _sub(r["dang"])
        if r.get("quy_trinh"):
            r["quy_trinh"] = [_sub(q) for q in r["quy_trinh"]]
d["lythuyet"] = [x.replace("chỉ ra một điểm cách đều bốn điểm; hay gặp nhất là hai tam giác vuông có chung cạnh huyền $\\Rightarrow$ trung điểm cạnh huyền cách đều bốn đỉnh, nêu đủ tâm và bán kính.",
                           "\\textbf{khuôn duy nhất (Thầy chốt 03/11/2026):} $\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ ba điểm $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$; hai tam giác vuông chung cạnh huyền $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính cạnh huyền đó. Không gọi trung điểm, không viết lại trung tuyến.")
                 for x in d["lythuyet"]]
d["kienthuc_nb"] = [x.replace("Tam giác vuông: trung điểm cạnh huyền cách đều ba đỉnh, là tâm đường tròn đi qua ba đỉnh.",
                              "$\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$.")
                    for x in d["kienthuc_nb"]]
d["loisai"] = [x.replace("mà không chỉ ra hai tam giác vuông chung cạnh huyền, không nêu tâm và bán kính",
                         "mà không chỉ ra hai tam giác vuông chung cạnh huyền, không nói rõ đường tròn đường kính nào")
               for x in d["loisai"]]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)

# ---- Phiếu 2 dựng theo THANG (03/11 lượt 2): đích đề Ái Mộ, NB7/NB10 làm trên hình đề ấy ----
d = json.load(open(out))
r2 = d["phieu"][1]["rows"]
for i, (v, o, b) in {1: (0, 3, 2), 6: (0, 3, 0), 8: (1, 2, 0), 9: (0, 3, 1)}.items():
    r2[i].update(vidu=v, onclass=o, btvn=b)
r2[1]["source_refs"] = ["sgk-5.35", "sgk-b16-lt1", "sgk-5.20", "tl-3b-7"]
r2[6].update(source_refs=["ck1-ai-mo-2.a"],
             dang="Hình đề Ái Mộ in sẵn (ý a): điền hai góc vuông do tiếp tuyến tại $A$, tại $C$ $\\Rightarrow$ $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính $MO$")
r2[9].update(source_refs=["ck1-ai-mo-2.b", "ck1-hat-mon-2025-IV2.b"],
             dang="Hình đề Ái Mộ (ý b): $\\triangle OCD$ cân, $OH$ là trung trực của $CD$ $\\Rightarrow FC = FD$ $\\Rightarrow \\triangle OCF = \\triangle ODF$ (c.c.c) $\\Rightarrow DF$ là tiếp tuyến (điền)")
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
d = json.load(open(out))
r = d["phieu"][1]["rows"][11]
r.update(vidu=1, source_refs=[x for x in r["source_refs"] if x != "sgk-5.21"])
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
d = json.load(open(out))
d["phieu"][1]["rows"][2].update(source_refs=["stk-b13-I-C8-tr6"], dang="Đường tròn $(O; OA)$ với $O$ là trung điểm $AB$ — chính là đường tròn đường kính $AB$ (vị trí điểm, trắc nghiệm)")
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
# ---- BTVN trình bày như đi thi (03/11 lượt 3) ----
d = json.load(open(out))
r = d["phieu"][1]["rows"]
r[1]["source_refs"] = ["sgk-5.35", "sgk-b16-lt1", "sgk-5.20"]
r[8].update(btvn=1, source_refs=["sgk-b16-vd1", "v10-dong-da-de04-IV2.b", "ck1-chu-van-an-2024-IV2.b"])
r[9].update(btvn=0)
r[10].update(btvn=1, source_refs=["ck1-hoang-liet-2025-4.2.a", "gk1-trung-vuong-2025-IV", "v10-dong-da-de08-IV2"])
r[11].update(btvn=1, source_refs=["sgk-b16-vd1", "v10-dong-da-de04-IV2", "ck1-hoang-liet-2025-4.2.b"],
             dang="Chứng minh một đường thẳng là tiếp tuyến: hai tam giác bằng nhau (c.c.c qua trung trực, hoặc c.g.c qua tia phân giác) cho góc $90^\\circ$, rồi dấu hiệu nhận biết")
d["lythuyet"] = [x.replace("câu nào không phải bài trình bày đi thi thì là trắc nghiệm, điền khuyết, Đúng/Sai hoặc trả lời ngắn trên hình in sẵn",
                           "câu nào không phải bài trình bày đi thi thì là trắc nghiệm, Đúng/Sai hoặc trả lời ngắn; câu ĐIỀN KHUYẾT (trên lớp và BTVN) luôn là khung bài giải trình bày như đi thi") for x in d["lythuyet"]]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
# ---- Phiếu 2 lượt 4 (04/11/2026): mỗi bài một hình riêng, dễ → khó, căn giờ thực lớp C ----
d = json.load(open(out))
d["phieu"][1]["rows"] = [
    R("NB", "NB kiến thức cũ",
      "Tam giác vuông $\\Rightarrow$ đỉnh góc vuông thuộc đường tròn đường kính cạnh huyền (trắc nghiệm)",
      ["stk-b13-I-C17-tr8", "sgk-b13-lt1"], onclass=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Tiếp tuyến vuông góc với bán kính \\textbf{tại tiếp điểm} (trắc nghiệm — bẫy \\textquotedblleft tại $O$\\textquotedblright)",
      ["stk-b16-I-C4-tr232"], onclass=1, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Vị trí tương đối theo $d$ và $R$: cắt $\\Leftrightarrow d < R$, tiếp xúc (tiếp tuyến) $\\Leftrightarrow d = R$ (trắc nghiệm trên hình in sẵn; BTVN: bài thực tế dán bốn hình tròn lên hai đường thẳng song song, trả lời ngắn)",
      ["sgk-5.35", "sgk-5.20"], onclass=1, btvn=3, lythuyet=1, hinh_san=True),
    R("NB", "NB lẻ LT", "Tam giác có hai đường cao $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính cạnh chung (BTVN khung bài giải, tính bán kính $BC = 2026$ mm)",
      ["stk-b13-III-C33-tr13"], btvn=2, hinh_san=True),
    R("NB", "NB ghép bài", "Đánh dấu hai góc vuông lên hình in sẵn rồi điền khung bài giải: hai hình chiếu vuông góc (đề Lương Thế Vinh ý a) $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính cạnh huyền chung",
      ["gk1-luong-the-vinh-2025-4.2.a"], onclass=2, hinh_san=True, gian_giao="ve-hinh"),
    R("NB", "NB tách TH", "Ý a đề thi tách thành khung bài giải: góc vuông do đường vuông góc và do tiếp tuyến, chung cạnh huyền $MO$ (đề Hoàng Liệt ý a — hình gần giống đề đích)",
      ["ck1-hoang-liet-2025-4.2.a"], onclass=2, hinh_san=True, gian_giao="dien-khuyet"),
    R("NB", "NB tách TH", "Khung bài giải chứng minh tiếp tuyến: tam giác cân $\\to$ đường trung trực $\\to$ c.c.c $\\to$ góc $90^\\circ$ (trên lớp đề Cụm 14; BTVN đề Đống Đa 04)",
      ["ck1-cum-14-2025-4.2.b", "v10-dong-da-de04-IV2.b"], onclass=2, btvn=2, hinh_san=True, gian_giao="dien-khuyet"),
    R("TH", "TH tách VD", "Tự trình bày không còn khung: chứng minh tiếp tuyến trên hình in sẵn (đề Chu Văn An ý b) — đi đúng đường ví dụ mẫu SGK Ví dụ 1 Bài 16",
      ["sgk-b16-vd1", "ck1-chu-van-an-2024-IV2.b", "ck1-cum-14-2025-4.2", "v10-dong-da-de04-IV2"], vidu=1, onclass=1, hinh_san=True),
    R("TH", "TH ghép bài", "Ý a của đề thi (bốn điểm, hai tam giác vuông chung cạnh huyền): ví dụ mẫu tam giác có hai đường cao; đề đích Ái Mộ trên lớp, đề Lý Sơn ở nhà — HS tự vẽ hình (phút vẽ tính ở dòng VD)",
      ["tl-1-19", "ck1-ai-mo-2.a", "ck1-ly-son-2025-IV2.a", "ck1-hoang-liet-2025-4.2.a"], vidu=1, onclass=1, btvn=1),
    R("VD", "VD lẻ", "Đề thi Câu IV.2 hai ý (đề Ái Mộ — đích của buổi): ý a bốn điểm (mức TH), ý b $DF$ là tiếp tuyến (mức VD). HS tự vẽ hình từ giả thiết, trình bày trọn. BTVN: đề Lý Sơn cùng khuôn ($KB$ là tiếp tuyến)",
      ["ck1-ai-mo-2", "ck1-ly-son-2025-IV2"], onclass=1, btvn=1, ve={"onclass": 1, "btvn": 1}, gian_giao="ve-hinh",
      quy_trinh=["Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$",
                 "Ý b: $\\triangle OCD$ cân, $OH \\perp CD$ $\\Rightarrow AB$ là đường trung trực của $CD$ $\\Rightarrow FC = FD$",
                 "$\\triangle OCF = \\triangle ODF$ (c.c.c) $\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$",
                 "Kết luận theo dấu hiệu nhận biết tiếp tuyến"]),
]
for _i in (3, 4, 5, 6):   # NB4 hai đường cao (BTVN), NB5, NB6 — khung bài giải
    d["phieu"][1]["rows"][_i]["khung"] = True
d["dang_vd"][1] = ("Buổi 2 — Câu IV.2 hai ý (đề Ái Mộ): bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn; $DF$ là tiếp tuyến "
                   "(tam giác cân $\\to$ đường trung trực $\\to$ c.c.c $\\to$ dấu hiệu nhận biết). BTVN: đề Lý Sơn cùng khuôn.")
d["vidu"][1] = ("Buổi 2: Tam giác nhọn có hai đường cao $BE$, $CF$ — bốn điểm $B$, $C$, $E$, $F$ cùng thuộc đường tròn đường kính $BC$ (khuôn tam giác vuông). "
                "SGK Ví dụ 1 Bài 16: dây $AB$, đường qua $O$ vuông góc $AB$ cắt tiếp tuyến tại $A$ ở $C$ — $CB$ là tiếp tuyến (trung trực $\\to$ c.c.c).")
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("P2 lượt 4 xong")
# ---- Kịch bản giờ thực buổi 2 (Thầy 04/11: "HS không kịp học, tôi không kịp dạy — lớp C") ----
d = json.load(open(out))
d["thoiluong"][1:2] = [
    "Buổi 2 (Bài 13: bốn điểm cùng thuộc một đường tròn $+$ Bài 16: chứng minh tiếp tuyến): 1 ca $=$ 90 phút",
    "\\quad Giờ thực lớp C (căn lại 04/11/2026): Khám phá $+$ Kiến thức 13′ · Luyện tập 1 khoảng 35′ (3 trắc nghiệm, 2 ví dụ, 3 khung bài giải)",
    "\\quad Luyện tập 2 khoảng 33′ (Bài 7 tự trình bày 8′, Bài 8 đề đích tự vẽ hình 25′) · chữa bài, chốt 9′ · BTVN khoảng 40′",
    "\\quad Khung bài giải tính 3′/thẻ (không phải 1′ như trắc nghiệm) nên bảng ghi ít câu hơn bản trước",
]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
# ---- Phiếu 2 lượt 5 (04/11/2026): căn giờ thực lớp C — bỏ Chu Văn An ý b + đề Lý Sơn; ý b đề đích về nhà ----
d = json.load(open(out))
rows = d["phieu"][1]["rows"]
rows[:] = [r for r in rows if not (r["band"] == "TH" and r["loai"] == "TH tách VD")]
th = next(r for r in rows if r["band"] == "TH" and r["loai"] == "TH ghép bài")
th.update(onclass=1, btvn=0, source_refs=["tl-1-19", "ck1-ai-mo-2.a", "ck1-hoang-liet-2025-4.2.a"],
          dang="Ý a của đề thi (bốn điểm, hai tam giác vuông chung cạnh huyền $MO$): ví dụ mẫu tam giác có hai đường cao; đề đích Ái Mộ trên lớp — HS tự vẽ hình (phút vẽ tính ở dòng VD)")
vd = next(r for r in rows if r["band"] == "VD")
vd.update(vidu=1, onclass=0, btvn=1, ve_hinh={"onclass": 1},
          source_refs=["ck1-ai-mo-2.b", "sgk-b16-vd1", "ck1-cum-14-2025-4.2", "v10-dong-da-de04-IV2"],
          dang="Ý b của đề thi (đề Ái Mộ — đích của buổi): $DF$ là tiếp tuyến (tam giác cân $\\to$ đường trung trực $\\to$ c.c.c). Ví dụ mẫu SGK Ví dụ 1 Bài 16; HS làm ở nhà trên hình đã vẽ ở lớp (giờ thực lớp C không đủ làm trên lớp)")
d["dang_vd"][1] = ("Buổi 2 — Câu IV.2 hai ý (đề Ái Mộ): bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn (trên lớp); $DF$ là tiếp tuyến "
                   "(ở nhà; tam giác cân $\\to$ đường trung trực $\\to$ c.c.c $\\to$ dấu hiệu nhận biết).")
i = next(k for k, x in enumerate(d["thoiluong"]) if "Giờ thực lớp C" in x)
d["thoiluong"][i:i + 3] = [
    "\\quad Giờ thực lớp C (căn lại 04/11/2026, rate lớp C mới): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 49′ (3 trắc nghiệm, 2 ví dụ, 3 khung bài giải)",
    "\\quad Luyện tập 2 khoảng 19′ (đề đích Ái Mộ ý a, HS tự vẽ hình) · chữa bài, chốt 10′ · BTVN khoảng 40′ (ý b đề đích làm ở nhà)",
    "\\quad Bỏ khỏi bản lớp C: Chu Văn An ý b (chấm lại 5,4 điểm) và đề Lý Sơn (BTVN 36′)",
]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("P2 lượt 5 xong")
# ---- Phiếu 2 lượt 6 (04/11/2026): hình nền + HS vẽ tiếp (+2–4′/câu), đề đầy đủ, bỏ BTVN hai đường cao ----
d = json.load(open(out))
rows = d["phieu"][1]["rows"]
rows[:] = [r for r in rows if not (r["band"] == "NB" and "hai đường cao" in r["dang"] and r["onclass"] == 0)]
for r in rows:
    if r["band"] == "NB" and r["loai"] == "NB ghép bài":
        r["ve_tiep"] = {"onclass": 2}
        r["dang"] = "Vẽ tiếp lên hình nền (tam giác), đánh dấu hai góc vuông rồi điền khung bài giải: hai hình chiếu vuông góc (đề Lương Thế Vinh ý a) $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính cạnh huyền chung"
    elif r["band"] == "NB" and r["loai"] == "NB tách TH" and r["onclass"] == 2 and r["btvn"] == 0:
        r["ve_tiep"] = {"onclass": 3}
    elif r["band"] == "NB" and r["loai"] == "NB tách TH":
        r["ve_tiep"] = {"onclass": 4, "btvn": 3}
    elif r["band"] == "VD":
        r.pop("ve_hinh", None)
        r["ve_tiep"] = {"onclass": 3, "btvn": 4}
        r["gian_giao"] = "ve-hinh"
        r["dang"] = ("Ý b của đề thi (đề Ái Mộ — đích của buổi): $DF$ là tiếp tuyến (tam giác cân $\\to$ đường trung trực $\\to$ c.c.c). "
                     "Ví dụ mẫu SGK Ví dụ 1 Bài 16; BTVN ghi lại đủ đề, HS vẽ tiếp hình nền. Phút vẽ tiếp hình đề đích trên lớp tính ở dòng này")
i = next(k for k, x in enumerate(d["thoiluong"]) if "Giờ thực lớp C" in x)
d["thoiluong"][i:i + 3] = [
    "\\quad Giờ thực lớp C (04/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 58′ (3 trắc nghiệm, 2 ví dụ, 3 khung bài giải $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 17′ (đề đích Ái Mộ ý a trên hình nền) · chữa bài, chốt 5′ · BTVN khoảng 42′ (ý b đề đích ghi đủ đề)",
    "\\quad Hình in sẵn chỉ là hình nền (tam giác, đường tròn, điểm ngoài đường tròn); HS vẽ tiếp $+$2–4′ mỗi bài",
]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("P2 lượt 6 xong")
# ---- Phiếu 2 lượt 7–8 (04/11/2026): HS vẽ cùng GV ở hai ví dụ (+2′, +3′); bỏ trắc nghiệm d so với R trên lớp ----
d = json.load(open(out))
rows = d["phieu"][1]["rows"]
for r in rows:
    if r["band"] == "NB" and "sgk-5.35" in r["source_refs"]:
        r.update(onclass=0, source_refs=["sgk-5.20"],
                 dang="Vị trí tương đối theo $d$ và $R$: tiếp xúc (tiếp tuyến) $\\Leftrightarrow d = R$ — BTVN bài thực tế dán bốn hình tròn lên hai đường thẳng song song, trả lời ngắn")
    elif r["band"] == "TH":
        r["ve_tiep"] = {"vidu": 2}
    elif r["band"] == "VD":
        r["ve_tiep"] = dict(r.get("ve_tiep", {}), vidu=3)
i = next(k for k, x in enumerate(d["thoiluong"]) if "Giờ thực lớp C" in x)
d["thoiluong"][i:i + 3] = [
    "\\quad Giờ thực lớp C (04/11/2026): Khám phá $+$ Kiến thức 12′ · Luyện tập 1 khoảng 59′ (2 trắc nghiệm, 2 ví dụ HS vẽ cùng GV, 3 khung bài giải $+$ vẽ tiếp hình)",
    "\\quad Luyện tập 2 khoảng 17′ (đề đích Ái Mộ ý a trên hình nền) · chữa bài, chốt khoảng 5′ · BTVN khoảng 42′ (ý b đề đích ghi đủ đề)",
    "\\quad Hình in sẵn chỉ là hình nền (tam giác, đường tròn, điểm ngoài đường tròn), kể cả ở ví dụ; HS vẽ tiếp $+$2–4′ mỗi bài",
]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("P2 lượt 7–8 xong")
