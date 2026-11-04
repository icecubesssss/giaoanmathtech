# Phiếu 2 ch.V 9C — lượt 4 (04/11/2026). Thầy: "sắp xếp lộn xộn, bài dưới dùng hình bài trên,
# chọn bài có hình tương tự; dẫn dắt dễ → khó; HS lớp C không kịp học — căn lại thời gian".
# Nguyên tắc: MỖI BÀI MỘT HÌNH RIÊNG (bài cùng khuôn với đề đích, không mượn hình bài trên),
# mỗi mạch ba bậc nhớ (trắc nghiệm) → mẫu (ví dụ) → điền khung bài giải; LT2 tự trình bày;
# cắt tải cho vừa 90′ thực của lớp C.
# Chạy từ gốc repo: python3 p2_ban4.py <phiếu lượt 3 (backup)> <out>. Từ 04/11/2026 JSON phiếu là nguồn sự thật; script giữ để truy vết.
import json, math, re, sys
sys.path.insert(0, ".")
from scripts.tikz_geo import Fig, polar, tangent_points, foot

src, out = sys.argv[1], sys.argv[2]
old = json.load(open(src))
ST = {s["kind"]: s for s in old["stages"]}

BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"
KG = "Điền vào chỗ chấm để hoàn thành bài giải:"
DD = "Đánh dấu hai góc vuông lên hình, rồi điền vào chỗ chấm để hoàn thành bài giải:"


def by_label(kind, label):
    return json.loads(json.dumps(next(b for b in ST[kind]["blocks"] if b.get("label") == label)))


def by_vidu(kind, n):
    return json.loads(json.dumps(next(b for b in ST[kind]["blocks"]
                                      if b.get("variant") == "example" and f"Ví dụ {n}." in b["text"])))


def fig(f, cap):
    return {"tikz": f.tikz(), "caption": cap, "pos": "right"}


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def mcq(stem, opts, tag="[NB] ", cols=1):
    body = "".join(f"\\mcqitem{{{k}}}{{{v}}}" for k, v in zip("ABCD", opts))
    st = f"{tag}{stem} \\begin{{mcq}}{{{cols}}}{body}\\end{{mcq}}"
    sl = f"{tag}{stem}{BR}" + " \\quad ".join(f"\\textbf{{{k}.}} {v}" for k, v in zip("ABCD", opts))
    return st, sl


def P(label, dang, tier, statement, answer=None, level=1, figure=None, slide=None, draw=False,
      hints=None, quy_trinh=None):
    b = {"type": "problem", "label": label, "level": level, "tier": tier, "dang_id": dang,
         "statement": statement, "figure_given": not draw}
    if draw:
        b["draw"] = True
    if hints:
        b["hints"] = hints
    if answer:
        b["answer"] = answer
    if quy_trinh:
        b["quy_trinh"] = quy_trinh
    if figure:
        b["figure"] = figure
    if slide:
        b["statement_slide"] = slide
    return b


def H(text, variant="heading"):
    return {"type": "para", "variant": variant, "text": text}


# ───────────────────────────── HÌNH (mỗi bài một hình) ─────────────────────────────
def h_hinhchieu():                       # Lương Thế Vinh: đường cao AD, hình chiếu E, F của D
    f = Fig()
    A, B, C = (1.6, 2.4), (0, 0), (3.6, 0)
    D = (1.6, 0)
    E = foot(D, A, B); F = foot(D, A, C)
    for n, p in [("A", A), ("B", B), ("C", C), ("D", D), ("E", E), ("F", F)]:
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("A", "D"); f.seg("D", "E"); f.seg("D", "F")
    f.right("D", "A", "C")
    return f


def h_hoangliet():                       # Hoàng Liệt: d ⊥ OA tại A, tiếp tuyến MB
    f = Fig(); R = 1.2
    O, A = (0, 0), (3.0, 0)
    M = (3.0, 1.9)
    Bp = max(tangent_points(O, R, M), key=lambda p: p[1])
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("M", M), ("B", Bp)]:
        f.pt(n, p)
    f.seg("O", "A"); f.seg("O", "B"); f.seg("M", "B")
    f.seg((3.0, -0.6), (3.0, 2.4))
    f.text((3.0, -0.65), "$d$", near=0)
    f.right("A", "O", "M")
    return f


def h_daycung(names=("O", "A", "B", "C", "H"), vuong=True):
    """Dây AB, đường qua O vuông góc (hoặc qua trung điểm) AB cắt tiếp tuyến tại A ở C."""
    o, a, b, c, h = names
    f = Fig(); R = 1.5
    O = (0, 0); A = polar(240, R); B = polar(300, R)
    C = (0, A[1] + A[0] ** 2 / A[1])
    Hh = (0, A[1])
    f.circle(O, R)
    for n, p in [(o, O), (a, A), (b, B), (c, C), (h, Hh)]:
        f.pt(n, p)
    f.seg(a, b); f.seg(o, c); f.seg(o, a); f.seg(o, b); f.seg(c, a)
    if vuong:
        f.seg(c, b)
        f.right(h, o, b)
    else:
        f.seg(c, b, style="ink, dashed")
        f.tick(a, h, 1); f.tick(h, b, 1)
    return f


def h_cum14():                           # Cụm 14: tiếp tuyến tại A, M cắt ở C; OD ⊥ MB tại H
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    th = 70
    M = polar(th, R)
    C = polar((180 + th) / 2, R / math.cos(math.radians((180 - th) / 2)))
    D = polar(th / 2, R / math.cos(math.radians(th / 2)))
    Hh = mid(M, B)
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("B", B), ("M", M), ("C", C), ("D", D), ("H", Hh)]:
        f.pt(n, p)
    f.seg("A", "B"); f.seg("C", "A"); f.seg("C", "D"); f.seg("M", "B"); f.seg("O", "D")
    f.seg("O", "M"); f.seg("D", "B", style="ink, dashed")
    f.right("H", "O", "B")
    return f


def h_haiduongcao():                     # tam giác có hai đường cao BD, CE
    f = Fig()
    A, B, C = (1.3, 2.5), (0, 0), (3.4, 0)
    D = foot(B, A, C); E = foot(C, A, B)
    for n, p in [("A", A), ("B", B), ("C", C), ("D", D), ("E", E)]:
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("B", "D"); f.seg("C", "E")
    f.right("D", "B", "C"); f.right("E", "C", "B")
    return f


def h_dongda04():                        # Đống Đa 04: K trung điểm dây BC, OK cắt tiếp tuyến tại B ở D
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    C = polar(100, R)
    K = mid(B, C)
    D = (R, K[1] * R / K[0])
    f.arc(O, R, 0, 180)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("K", K), ("D", D)]:
        f.pt(n, p)
    f.seg("A", "B"); f.seg("B", "C"); f.seg("O", "D"); f.seg("B", "D"); f.seg("O", "C")
    f.seg("D", "C", style="ink, dashed")
    f.tick("B", "K", 1); f.tick("K", "C", 1)
    return f


# ───────────────────────────── LUYỆN TẬP 1 ─────────────────────────────
MUC_TIEU = {"type": "para", "text": (
    "\\textbf{Đích của buổi học:} tự giải trọn \\textbf{Bài 8} — đề thi Câu IV.2 (đề Ái Mộ): "
    "ý a chứng minh bốn điểm cùng thuộc một đường tròn, ý b chứng minh tiếp tuyến." + BR
    + "Mỗi mạch đi ba bậc: \\textbf{nhớ kiến thức} (trắc nghiệm) $\\to$ \\textbf{xem bài mẫu} (ví dụ) "
    "$\\to$ \\textbf{điền khung bài giải} trên hình giống hình đề thi. Luyện tập 2: tự trình bày như đi thi.")}
M1 = H("Mạch 1. Ý a — Bốn điểm cùng thuộc một đường tròn")
M2 = H("Mạch 2. Ý b — Chứng minh một đường thẳng là tiếp tuyến")

b1 = by_label("practice1", "Bài 1.")                         # NB kiến thức cũ (stk C17)
b1["dang_id"] = "NB1"
b2 = by_label("practice1", "Bài 3.")                         # tiếp tuyến ⊥ bán kính tại tiếp điểm (stk C4)
b2.update(label="Bài 2.", dang_id="NB2")

vd1 = by_vidu("practice1", 2)                                # hai đường cao BE, CF — khuôn mẫu
vd1["text"] = vd1["text"].replace("Ví dụ 2.", "Ví dụ 1.").replace("(Hình 3)", "(Hình 2)")
vd1["figure"] = dict(vd1["figure"]); vd1["figure"]["caption"] = "Hình 2"

b3 = P("Bài 3.", "NB5", "onclass",
       "Cho tam giác $ABC$ nhọn, đường cao $AD$. Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$, $AC$ (Hình 3). "
       "Chứng minh bốn điểm $A$, $E$, $D$, $F$ cùng thuộc một đường tròn. " + DD + BR
       + "a) [NB] $DE \\perp AB$ tại $E$ $\\Rightarrow \\triangle AED$ vuông tại [[blank:1.1cm]]" + BR
       + "$\\Rightarrow A$, $E$, $D$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]." + BR
       + "b) [NB] $DF \\perp AC$ tại $F$ $\\Rightarrow \\triangle AFD$ vuông tại $F$" + BR
       + "$\\Rightarrow A$, $F$, $D$ cùng thuộc đường tròn đường kính $AD$." + BR
       + "Vậy $A$, $E$, $D$, $F$ cùng thuộc đường tròn đường kính [[blank:1.1cm]].",
       "a) $E$; $AD$.[[br]]b) $AD$.", figure=fig(h_hinhchieu(), "Hình 3"))

b4 = by_label("practice1", "Bài 4.")                          # Hoàng Liệt ý a — khung, hình riêng
b4.update(dang_id="NB6", figure=fig(h_hoangliet(), "Hình 4"))
b4["statement"] = re.sub(r"\(Hình \d+\)", "(Hình 4)", b4["statement"]).replace(KG, DD)
assert DD in b4["statement"]

s5, sl5 = mcq("Tiếp tuyến là đường thẳng \\textbf{tiếp xúc} với đường tròn. Cho đường tròn $(O; R)$ và hai đường thẳng $a_1$, $a_2$. "
              "Gọi $d_1$, $d_2$ lần lượt là khoảng cách từ $O$ đến $a_1$, $a_2$. Biết $(O)$ cắt $a_1$ và tiếp xúc với $a_2$ (Hình 5). Khi đó:",
              ["$d_1 < R$, $d_2 = R$", "$d_1 = R$, $d_2 < R$", "$d_1 > R$, $d_2 = R$", "$d_1 < R$, $d_2 < R$"], cols=4)
_old6 = by_label("practice1", "Bài 6.")
b5 = P("Bài 5.", "NB3", "onclass", s5, "\\textbf{A}.", slide=sl5,
       figure={"tikz": _old6["figure"]["tikz"], "caption": "Hình 5", "pos": "right"})

vd2 = by_vidu("practice1", 3)                                # SGK Ví dụ 1 Bài 16 — trung trực → c.c.c
vd2["text"] = (
    "\\textbf{Ví dụ 2.} Cho $AB$ là một dây không đi qua tâm của đường tròn $(O)$. Đường thẳng qua $O$ và vuông góc với $AB$ tại $H$ "
    "cắt tiếp tuyến tại $A$ của $(O)$ ở điểm $C$ (Hình 5). Chứng minh rằng $CB$ là tiếp tuyến của $(O)$." + BR + LG + BR
    + "$OA = OB = R$ $\\Rightarrow \\triangle OAB$ cân tại $O$." + BR
    + "$OH \\perp AB$ $\\Rightarrow$ đường cao $OH$ đồng thời là đường trung tuyến" + BR
    + "$\\Rightarrow OC$ là đường trung trực của $AB$" + BR
    + "$\\Rightarrow CA = [[fill:CB]]$." + BR
    + "Xét $\\triangle OAC$ và $\\triangle OBC$ có: $OA = OB$, $CA = CB$, $OC$ chung" + BR
    + "$\\Rightarrow \\triangle OAC = \\triangle OBC$ ([[fill:c.c.c]])" + BR
    + "$\\Rightarrow \\widehat{OBC} = \\widehat{OAC} = [[fill:90^\\circ]]$ ($CA$ là tiếp tuyến tại $A$)" + BR
    + "$\\Rightarrow CB \\perp OB$ tại $B \\in (O)$." + BR
    + "Vậy $CB$ là [[fill:tiếp tuyến]] của $(O)$.")
vd2["figure"] = fig(h_daycung(), "Hình 5")

b6 = P("Bài 6.", "NB7", "onclass",
       "Cho đường tròn $(O; R)$ đường kính $AB$, điểm $M$ thuộc đường tròn ($M \\ne A$, $M \\ne B$); tiếp tuyến tại $A$ và tại $M$ cắt nhau tại $C$. "
       "Qua $O$ kẻ đường thẳng vuông góc với dây $MB$ tại $H$, cắt tia $CM$ tại $D$ (Hình 6). Chứng minh $DB$ là tiếp tuyến của $(O)$. " + KG + BR
       + "a) [NB] $OM = OB = R$ $\\Rightarrow \\triangle OMB$ cân tại $O$." + BR
       + "$OH \\perp MB$ $\\Rightarrow$ đường cao $OH$ đồng thời là đường trung tuyến" + BR
       + "$\\Rightarrow OD$ là đường trung trực của $MB$" + BR
       + "$\\Rightarrow DM = [[blank:1.1cm]]$." + BR
       + "b) [NB] Xét $\\triangle ODM$ và $\\triangle ODB$ có: $OM = OB$, $DM = DB$, $OD$ chung" + BR
       + "$\\Rightarrow \\triangle ODM = \\triangle ODB$ ([[blank:1.1cm]])" + BR
       + "$\\Rightarrow \\widehat{OBD} = \\widehat{OMD} = [[blank:1.1cm]]$ ($CM$ là tiếp tuyến tại $M$)" + BR
       + "$\\Rightarrow DB \\perp OB$ tại $B \\in (O)$." + BR
       + "Vậy $DB$ là [[blank:2.4cm]] của $(O)$.",
       "a) $DB$.[[br]]b) c.c.c; $90^\\circ$; tiếp tuyến.", figure=fig(h_cum14(), "Hình 6"))

# ───────────────────────────── LUYỆN TẬP 2 ─────────────────────────────
L1 = H("Bậc 1. Tự trình bày một ý (không còn khung)")
L2 = H("Bậc 2. Đề thi trọn hai ý — đích của buổi học")

b7 = P("Bài 7.", "TH1", "onclass",
       "[TH] Cho đường tròn $(O; R)$ và dây $AB$ bất kì ($AB < 2R$). Gọi $I$ là trung điểm của $AB$. "
       "Tia $OI$ cắt tiếp tuyến tại $A$ của $(O)$ ở $D$ (Hình 7). Chứng minh $DB$ là tiếp tuyến của $(O)$.",
       "$OA = OB = R$ $\\Rightarrow \\triangle OAB$ cân tại $O$.[[br]]"
       "$I$ là trung điểm $AB$ $\\Rightarrow$ trung tuyến $OI$ đồng thời là đường cao[[br]]"
       "$\\Rightarrow OD$ là đường trung trực của $AB$[[br]]"
       "$\\Rightarrow DA = DB$.[[br]]"
       "Xét $\\triangle OAD$ và $\\triangle OBD$ có: $OA = OB$, $DA = DB$, $OD$ chung[[br]]"
       "$\\Rightarrow \\triangle OAD = \\triangle OBD$ (c.c.c)[[br]]"
       "$\\Rightarrow \\widehat{OBD} = \\widehat{OAD} = 90^\\circ$ ($DA$ là tiếp tuyến tại $A$)[[br]]"
       "$\\Rightarrow DB \\perp OB$ tại $B \\in (O)$.[[br]]"
       "Vậy $DB$ là tiếp tuyến của $(O)$.",
       level=2, figure=fig(h_daycung(("O", "A", "B", "D", "I"), vuong=False), "Hình 7"),
       hints=["Muốn $DB$ là tiếp tuyến, cần góc nào bằng $90^\\circ$?",
              "Góc ấy bằng góc nào đã biết bằng $90^\\circ$? Hai góc đó nằm trong hai tam giác nào?"])

b8 = by_label("practice2", "Bài 13.")                         # ĐÍCH: đề Ái Mộ, HS tự vẽ
b8.update(label="Bài 8.", dang_id="TH2+VD1")
b8["statement"] = (b8["statement"].replace("[VD] Cho", "Cho")
                   .replace("[[br]]a) Chứng minh", "[[br]]a) [TH] Chứng minh")
                   .replace("[[br]]b) Chứng minh", "[[br]]b) [VD] Chứng minh"))
assert "[TH]" in b8["statement"] and "[VD]" in b8["statement"]
b8["quy_trinh"] = [
    "Vẽ hình theo đề: đường tròn, đường kính $AB$, điểm $C$, hai tiếp tuyến tại $A$ và tại $C$; đánh dấu các góc vuông đã biết",
    "Ý a: $MA$, $MC$ là tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$ (như Bài 4)",
    "Ý b: $\\triangle OCD$ cân tại $O$, $OH \\perp CD$ $\\Rightarrow AB$ là đường trung trực của $CD$ $\\Rightarrow FC = FD$ (như Bài 6)",
    "$\\triangle OCF = \\triangle ODF$ (c.c.c) $\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$",
    "Kết luận theo dấu hiệu nhận biết tiếp tuyến"]
b8["solution"] = (
    "a) $MA$ là tiếp tuyến của $(O)$ tại $A$ $\\Rightarrow \\triangle MAO$ vuông tại $A$[[br]]"
    "$\\Rightarrow M$, $A$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
    "$MC$ là tiếp tuyến của $(O)$ tại $C$ $\\Rightarrow \\triangle MCO$ vuông tại $C$[[br]]"
    "$\\Rightarrow M$, $C$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
    "Vậy $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
    "b) $OC = OD = R$ $\\Rightarrow \\triangle OCD$ cân tại $O$.[[br]]"
    "$OH \\perp CD$ ($CH \\perp AB$) $\\Rightarrow$ đường cao $OH$ đồng thời là đường trung tuyến[[br]]"
    "$\\Rightarrow AB$ là đường trung trực của $CD$.[[br]]"
    "$F \\in AB$ $\\Rightarrow FC = FD$.[[br]]"
    "Xét $\\triangle OCF$ và $\\triangle ODF$ có: $OC = OD$, $FC = FD$, $OF$ chung[[br]]"
    "$\\Rightarrow \\triangle OCF = \\triangle ODF$ (c.c.c)[[br]]"
    "$\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$ ($MC$ là tiếp tuyến tại $C$)[[br]]"
    "$\\Rightarrow DF \\perp OD$ tại $D \\in (O)$.[[br]]"
    "Vậy $DF$ là tiếp tuyến của $(O; R)$.")

# ───────────────────────────── BTVN (≤ 40′ thực) ─────────────────────────────
k0 = P("BTVN 1.", "NB3", "btvn",
       "Bạn Thanh cắt $4$ hình tròn bằng giấy có bán kính $4$ cm, $6$ cm, $7$ cm và $8$ cm, dán lên một mảnh giấy có hai đường thẳng "
       "song song $a$, $b$ cách nhau $6$ cm sao cho tâm cả $4$ hình tròn đều nằm trên $b$. Trả lời ngắn:" + BR
       + "a) [NB] Khoảng cách từ tâm mỗi hình tròn đến đường thẳng $a$ là $d = [[blank:1.1cm]]$ cm." + BR
       + "b) [NB] Hình tròn bán kính [[blank:1.1cm]] cm tiếp xúc với $a$ ($a$ là tiếp tuyến)." + BR
       + "c) [NB] Các hình tròn bán kính [[blank:2.4cm]] che khuất một phần đường thẳng $a$ (cắt $a$).",
       "a) $6$.[[br]]b) $6$.[[br]]c) $7$ cm và $8$ cm ($R > d$).")
k0["figure_given"] = False                   # không in hình — HS tự hình dung
k1 = P("BTVN 2.", "NB4", "btvn",
       "Cho tam giác $ABC$ có các đường cao $BD$, $CE$ và $BC = 2026$ mm (Hình 8). Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn "
       "và tính bán kính của đường tròn đó. " + KG + BR
       + "a) [NB] $BD \\perp AC$ tại $D$ $\\Rightarrow \\triangle BDC$ vuông tại $D$" + BR
       + "$\\Rightarrow B$, $D$, $C$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]." + BR
       + "b) [NB] $CE \\perp AB$ tại $E$ $\\Rightarrow \\triangle BEC$ vuông tại [[blank:1.1cm]]" + BR
       + "$\\Rightarrow B$, $E$, $C$ cùng thuộc đường tròn đường kính $BC$." + BR
       + "Vậy $B$, $E$, $D$, $C$ cùng thuộc đường tròn đường kính $BC$, bán kính $R = \\dfrac{BC}{2} = [[blank:1.6cm]]$ mm.",
       "a) $BC$.[[br]]b) $E$; $1013$.", figure=fig(h_haiduongcao(), "Hình 8"))
k2 = P("BTVN 3.", "NB7", "btvn",
       "Cho nửa đường tròn $(O)$ đường kính $AB$, điểm $C$ thuộc nửa đường tròn, $K$ là trung điểm của dây $BC$. "
       "Tiếp tuyến tại $B$ cắt tia $OK$ tại $D$ (Hình 9). Chứng minh $DC$ là tiếp tuyến của $(O)$. " + KG + BR
       + "a) [NB] $OB = OC = R$ $\\Rightarrow \\triangle OBC$ cân tại $O$." + BR
       + "$K$ là trung điểm $BC$ $\\Rightarrow$ trung tuyến $OK$ đồng thời là đường cao" + BR
       + "$\\Rightarrow OD$ là đường trung trực của $BC$" + BR
       + "$\\Rightarrow DC = [[blank:1.1cm]]$." + BR
       + "b) [NB] Xét $\\triangle ODC$ và $\\triangle ODB$ có: $OC = OB$, $DC = DB$, $OD$ chung" + BR
       + "$\\Rightarrow \\triangle ODC = \\triangle ODB$ ([[blank:1.1cm]])" + BR
       + "$\\Rightarrow \\widehat{OCD} = \\widehat{OBD} = [[blank:1.1cm]]$ ($DB$ là tiếp tuyến tại $B$)" + BR
       + "$\\Rightarrow DC \\perp OC$ tại $C \\in (O)$." + BR
       + "Vậy $DC$ là [[blank:2.4cm]] của $(O)$.",
       "a) $DB$.[[br]]b) c.c.c; $90^\\circ$; tiếp tuyến.", figure=fig(h_dongda04(), "Hình 9"))
k3 = P("BTVN 4.", "TH2+VD1", "btvn",
       "Cho đường tròn $(O)$, đường kính $AB$. Kẻ tiếp tuyến $Ax$ với đường tròn $(O)$. Lấy điểm $C$ thuộc đường tròn $(O)$ ($AC < CB$). "
       "Kẻ tiếp tuyến tại $C$ của đường tròn $(O)$ cắt $Ax$ tại điểm $M$." + BR
       + "a) [TH] Chứng minh bốn điểm $M$, $A$, $C$, $O$ cùng thuộc một đường tròn." + BR
       + "b) [VD] Qua điểm $O$ kẻ đường thẳng vuông góc với $BC$ tại $H$, cắt đường thẳng $MC$ tại $K$. Chứng minh $KB$ là tiếp tuyến của đường tròn $(O)$.",
       "a) $MA$ là tiếp tuyến của $(O)$ tại $A$ $\\Rightarrow \\triangle MAO$ vuông tại $A$[[br]]"
       "$\\Rightarrow M$, $A$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
       "$MC$ là tiếp tuyến của $(O)$ tại $C$ $\\Rightarrow \\triangle MCO$ vuông tại $C$[[br]]"
       "$\\Rightarrow M$, $C$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
       "Vậy $M$, $A$, $C$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
       "b) $OB = OC = R$ $\\Rightarrow \\triangle OBC$ cân tại $O$.[[br]]"
       "$OH \\perp BC$ $\\Rightarrow$ đường cao $OH$ đồng thời là đường trung tuyến[[br]]"
       "$\\Rightarrow OK$ là đường trung trực của $BC$[[br]]"
       "$\\Rightarrow KB = KC$.[[br]]"
       "Xét $\\triangle OBK$ và $\\triangle OCK$ có: $OB = OC$, $KB = KC$, $OK$ chung[[br]]"
       "$\\Rightarrow \\triangle OBK = \\triangle OCK$ (c.c.c)[[br]]"
       "$\\Rightarrow \\widehat{OBK} = \\widehat{OCK} = 90^\\circ$ ($MC$ là tiếp tuyến tại $C$)[[br]]"
       "$\\Rightarrow KB \\perp OB$ tại $B \\in (O)$.[[br]]"
       "Vậy $KB$ là tiếp tuyến của $(O)$.",
       level=3, draw=True,
       quy_trinh=["Vẽ hình theo đề, đánh dấu các góc vuông đã biết",
                  "Ý a: hai tiếp tuyến $\\Rightarrow$ hai tam giác vuông chung cạnh huyền $MO$ (như Bài 8 ý a)",
                  "Ý b: $\\triangle OBC$ cân, $OH \\perp BC$ $\\Rightarrow OK$ là đường trung trực của $BC$ $\\Rightarrow KB = KC$",
                  "$\\triangle OBK = \\triangle OCK$ (c.c.c) $\\Rightarrow \\widehat{OBK} = 90^\\circ$ $\\Rightarrow KB$ là tiếp tuyến"])

# ───────────────────────────── LẮP ─────────────────────────────
new = json.loads(json.dumps(old))
S = {s["kind"]: s for s in new["stages"]}
# Thẻ Dạng 2 đi đúng MỘT đường mà cả phiếu dùng: tam giác cân → đường trung trực → c.c.c
_d2 = S["concept"]["blocks"][-1]
assert _d2["title"].startswith("DẠNG 2")
_d2["text"] = (
    "\\nhanly{Phương pháp.} dùng dấu hiệu nhận biết tiếp tuyến.[[br]]"
    "\\nhanly{Bước 1:} Chỉ ra điểm $C$ thuộc đường tròn $(O)$.[[br]]"
    "\\nhanly{Bước 2:} Chỉ ra $AC \\perp OC$ tại $C$. Góc $90^\\circ$ lấy qua \\textbf{hai tam giác bằng nhau}: "
    "$OB = OC$ $\\Rightarrow$ $\\triangle OBC$ cân; đường cao $OH$ đồng thời là trung tuyến $\\Rightarrow$ $OA$ là đường trung trực của $BC$ "
    "$\\Rightarrow AB = AC$ $\\Rightarrow$ $\\triangle AOB = \\triangle AOC$ (c.c.c) $\\Rightarrow \\widehat{ACO} = \\widehat{ABO} = 90^\\circ$.[[br]]"
    "\\nhanly{Bước 3:} Kết luận $AC$ là tiếp tuyến của $(O)$ tại $C$ (dấu hiệu nhận biết tiếp tuyến).")
_d2["figure"]["caption"] = "$OA$ là đường trung trực của $BC$ $\\Rightarrow \\triangle AOB = \\triangle AOC$ (c.c.c) $\\Rightarrow \\widehat{ACO} = \\widehat{ABO} = 90^\\circ$"
S["practice1"]["blocks"] = [MUC_TIEU, M1, b1, b2, vd1, b3, b4, M2, b5, vd2, b6]
S["practice1"]["teacher_note"] = (
    "Khoảng 35 phút. Hai mạch cùng một nhịp: trắc nghiệm nhớ kiến thức (1--2 phút/câu) $\\to$ GV giảng ví dụ "
    "(4 phút) $\\to$ HS điền khung bài giải (5--8 phút/bài). Mỗi bài có hình riêng, hình gần giống hình đề đích "
    "(Bài 4: đề Hoàng Liệt; Bài 6: đề Cụm 14) để HS nhận ra khuôn khi gặp đề Ái Mộ ở Bài 8.")
S["practice2"]["blocks"] = [L1, b7, L2, b8]
S["practice2"]["teacher_note"] = (
    "Khoảng 33 phút. Bài 7 (8 phút, hình in sẵn): tự trình bày lại đúng đường của Ví dụ 2 và Bài 6, không còn khung. "
    "Bài 8 (25 phút, HS tự vẽ hình): đề Ái Mộ trọn hai ý — ý a đi như Bài 4, ý b đi như Bài 6. "
    "Còn khoảng 10 phút cho chữa bài và chốt. Không đủ giờ thì Bài 8 ý b chuyển thành bài về nhà, chữa đầu buổi 3.")
mm = S["reflection"]["blocks"][0]
mm["branches"][3]["children"] = [{"label": "Tam giác cân: đường cao đồng thời là trung tuyến $\\Rightarrow$ đường trung trực"},
                                 {"label": "Hai tam giác bằng nhau (c.c.c)"}]
S["reflection"]["blocks"] = [mm, k0, k1, k2, k3]
S["reflection"]["teacher_note"] = (
    "BTVN khoảng 40 phút, dễ trước khó sau: BTVN 1 (3 phút) trả lời ngắn — hình tròn dán giấy, $d$ so với $R$; "
    "BTVN 2 (6 phút) điền khung ý a; BTVN 3 (8 phút) điền khung ý b; "
    "BTVN 4 (25 phút, tự vẽ hình) là đề Lý Sơn — cùng khuôn đề Ái Mộ, trình bày như đi thi, chữa đầu buổi 3.")

n = sum(1 for kind in ("review", "concept") for b in S[kind]["blocks"]
        if isinstance(b.get("figure"), dict) and str(b["figure"].get("caption", "")).startswith("Hình"))
for kind in ("practice1", "practice2", "reflection"):
    for b in S[kind]["blocks"]:
        f = b.get("figure")
        if isinstance(f, dict) and str(f.get("caption", "")).startswith("Hình"):
            n += 1
            for k in ("statement", "text", "statement_slide"):
                if isinstance(b.get(k), str):
                    b[k] = re.sub(r"\(Hình \d+\)", f"(Hình {n})", b[k])
            f["caption"] = f"Hình {n}"
json.dump(new, open(out, "w"), ensure_ascii=False, indent=1)
print("ok")
