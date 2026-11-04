# Dựng phiếu 2 ch.V 9C (03/11/2026) theo thuyết minh dựng lại từ tab chọn câu.
# Chạy từ gốc repo: python3 p2.py <phiếu cũ backup> <out>
import json, math, sys
sys.path.insert(0, ".")
from scripts.tikz_geo import Fig, polar, tangent_points, foot

src, out = sys.argv[1], sys.argv[2]
old = json.load(open(src))
ST = {s["kind"]: s for s in old["stages"]}
OLD_P1 = ST["practice1"]["blocks"]
OLD_P2 = ST["practice2"]["blocks"]

BR = "[[br]]"
LG = "{\\sffamily\\bfseries\\color{brand}Lời giải}"


def fig(f, cap, scale=None):
    t = f.tikz()
    return {"tikz": t, "caption": cap, "pos": "right"}


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def inter(p1, d1, p2, d2):
    """Giao hai đường p1 + t d1, p2 + s d2."""
    det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])
    rx, ry = p2[0] - p1[0], p2[1] - p1[1]
    t = (rx * (-d2[1]) - ry * (-d2[0])) / det
    return (p1[0] + t * d1[0], p1[1] + t * d1[1])


def mcq(stem, opts, tag="[NB] "):
    body = "".join(f"\\mcqitem{{{k}}}{{{v}}}" for k, v in zip("ABCD", opts))
    st = f"{tag}{stem} \\begin{{mcq}}{{{4 if max(len(o) for o in opts) < 22 else 1}}}{body}\\end{{mcq}}"
    sl = f"{tag}{stem}{BR}" + " \\quad ".join(f"\\textbf{{{k}.}} {v}" for k, v in zip("ABCD", opts))
    return st, sl


def P(label, dang, tier, statement, answer=None, level=1, figure=None, slide=None, draw=False,
      hints=None, solution=None, quy_trinh=None, options=None):
    b = {"type": "problem", "label": label, "level": level, "tier": tier, "dang_id": dang,
         "statement": statement, "figure_given": not draw}
    if draw:
        b["draw"] = True
    if hints:
        b["hints"] = hints
    if options:
        b["options"] = options
    if answer:
        b["answer"] = answer
    if solution:
        b["solution"] = solution
    if quy_trinh:
        b["quy_trinh"] = quy_trinh
    if figure:
        b["figure"] = figure
    if slide:
        b["statement_slide"] = slide
    return b


def VDU(text, figure=None):
    b = {"type": "noted", "variant": "example", "text": text}
    if figure:
        b["figure"] = figure
    return b


# ───────────────────────────── HÌNH ─────────────────────────────
def h_c45():
    f = Fig()
    A, B, C = (0, 2.3), (-1.4, 0), (1.4, 0)
    D = (0, 0)
    E = foot(B, A, C)
    H = inter(B, (E[0] - B[0], E[1] - B[1]), A, (0, -1))
    O = mid(A, H)
    r = (A[1] - H[1]) / 2
    f.circle(O, r)
    for n, p in [("A", A), ("B", B), ("C", C), ("D", D), ("E", E), ("H", H), ("O", O)]:
        f.pt(n, p)
    f.poly("A", "B", "C")
    f.seg("A", "D"); f.seg("B", "E"); f.seg("D", "E")
    f.right("D", "A", "C"); f.right("E", "B", "C")
    return f


def h_lyson():
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    C = polar(120, R)
    M = polar(150, R / math.cos(math.radians(30)))
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("M", M)]:
        f.pt(n, p)
    f.seg("A", "B"); f.seg("O", "C")
    f.seg((-R, -0.3), (-R, M[1] + 0.35))
    f.text((-R - 0.05, M[1] + 0.4), "$x$", near=180)
    f.seg("M", "C")
    return f


def h_hoangliet():
    f = Fig(); R = 1.2
    O, A = (0, 0), (3.0, 0)
    M = (3.0, 1.9)
    T = tangent_points(O, R, M)
    Bp = max(T, key=lambda p: p[1])
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("M", M), ("B", Bp)]:
        f.pt(n, p)
    f.seg("O", "A"); f.seg("O", "B"); f.seg("M", "B")
    f.seg((3.0, -0.6), (3.0, 2.4))
    f.text((3.0, -0.65), "$d$", near=0)
    f.right("A", "O", "M")
    return f


def h_daycung(names=("O", "A", "B", "C", "H")):
    """Dây AB, đường qua O vuông góc AB cắt tiếp tuyến tại A ở C (SGK Ví dụ 1)."""
    o, a, b, c, h = names
    f = Fig(); R = 1.5
    O = (0, 0); A = polar(240, R); B = polar(300, R)
    C = (0, A[1] + A[0] ** 2 / A[1])
    H = (0, A[1])
    f.circle(O, R)
    for n, p in [(o, O), (a, A), (b, B), (c, C), (h, H)]:
        f.pt(n, p)
    f.seg(a, b); f.seg(o, c); f.seg(o, a); f.seg(o, b); f.seg(c, a); f.seg(c, b)
    f.right(h, o, b)
    return f


def h_dongda04():
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    C = polar(100, R)
    K = mid(B, C)
    D = (R, K[1] * R / K[0])
    f.arc(O, R, 0, 180)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("K", K), ("D", D)]:
        f.pt(n, p)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("B", "C"); f.seg("O", "D"); f.seg("B", "D"); f.seg("O", "C")
    f.seg("D", "C")
    return f


def h_aimo():
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    C = polar(60, R)
    H = (C[0], 0); D = (C[0], -C[1])
    M = polar(120, R / math.cos(math.radians(60)))
    F = (R * R / C[0], 0)
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("D", D), ("H", H), ("M", M), ("F", F)]:
        f.pt(n, p)
    f.seg("A", "F"); f.seg("C", "D"); f.seg("M", "A"); f.seg("M", "F")
    f.seg("O", "C"); f.seg("O", "D"); f.seg("D", "F")
    f.right("H", "C", "B")
    return f


def h_521():
    f = Fig(); R = 1.5
    O = (0, 0); A = (0, R); B = polar(215, R); C = polar(325, R)
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C)]:
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("O", "A")
    f.seg((-1.9, R), (1.9, R))
    f.text((-1.95, R), "$x$", near=180); f.text((1.95, R), "$y$", near=0)
    return f


def h_tantrieu():
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    M = polar(65, R)
    C = polar(122.5, R / math.cos(math.radians(57.5)))
    dAM = (M[0] - A[0], M[1] - A[1])
    tM = (-M[1], M[0])
    H = mid(M, B)
    D = inter(O, dAM, M, tM)
    f.arc(O, R, 0, 180)
    for n, p in [("O", O), ("A", A), ("B", B), ("M", M), ("C", C), ("H", H), ("D", D)]:
        f.pt(n, p)
    f.seg("A", "B"); f.seg("A", "C"); f.seg("C", "D"); f.seg("A", "M"); f.seg("M", "B")
    f.seg("O", "D"); f.seg("B", "D")
    return f


def h_ltv():
    f = Fig()
    A, B, C = (1.6, 2.4), (0, 0), (3.6, 0)
    D = (1.6, 0)
    E = foot(D, A, B); F = foot(D, A, C)
    for n, p in [("A", A), ("B", B), ("C", C), ("D", D), ("E", E), ("F", F)]:
        f.pt(n, p)
    f.poly("A", "B", "C"); f.seg("A", "D"); f.seg("D", "E"); f.seg("D", "F")
    f.right("D", "A", "C")
    return f


# ───────────────────────────── LUYỆN TẬP 1 ─────────────────────────────
OLD_H2 = dict(OLD_P1[0]["figure"]); OLD_H2["caption"] = "Hình 2"
OLD_H3 = dict(OLD_P1[2]["figure"]); OLD_H3["caption"] = "Hình 3"
VIDU2 = json.loads(json.dumps(OLD_P1[3])); VIDU2["figure"]["caption"] = "Hình 4"
VIDU2["text"] = VIDU2["text"].replace("Ví dụ 1.", "Ví dụ 2.").replace("(Hình 4)", "(Hình 4)")

vd1 = VDU("\\textbf{Ví dụ 1.} Cho tam giác $ABC$ vuông tại $A$, $M$ là trung điểm của $BC$ (Hình 2). Chứng minh rằng điểm $A$ thuộc đường tròn đường kính $BC$." + BR + LG + BR
          + "Xét $\\triangle ABC$ vuông tại $A$, trung tuyến $AM$" + BR
          + "$\\Rightarrow AM = [[fill:\\dfrac{BC}{2}]] = MB = MC$." + BR
          + "Vậy $A$ thuộc đường tròn tâm $[[fill:M]]$, đường kính $[[fill:BC]]$.", OLD_H2)

s1, sl1 = mcq("Cho tam giác $ABC$ vuông tại $A$. Nhận xét nào sau đây đúng?",
              ["Điểm $A$ thuộc đường tròn đường kính $BC$.", "Điểm $B$ thuộc đường tròn đường kính $AC$.",
               "Điểm $C$ thuộc đường tròn đường kính $AB$.", "Ba điểm $A$, $B$, $C$ thuộc đường tròn đường kính $AC$."])
b1 = P("Bài 1.", "NB1", "onclass", s1, "\\textbf{A}.", slide=sl1)

s2a, sl2a = mcq("Cho đường tròn $(O; R)$ và hai đường thẳng $a_1$, $a_2$. Gọi $d_1$, $d_2$ lần lượt là khoảng cách từ $O$ đến $a_1$, $a_2$. Biết $(O)$ cắt $a_1$ và tiếp xúc với $a_2$ (Hình 3). Khi đó:",
                ["$d_1 < R$, $d_2 = R$", "$d_1 = R$, $d_2 < R$", "$d_1 > R$, $d_2 = R$", "$d_1 < R$, $d_2 < R$"], tag="a) [NB] ")
b2 = P("Bài 2.", "NB2", "onclass",
       "Chọn đáp án đúng." + BR + s2a + "Đường thẳng $a$ cách điểm $O$ một khoảng $4$ cm. Điền \\textbf{cắt}, \\textbf{tiếp xúc} hoặc \\textbf{không cắt} vào chỗ chấm:" + BR
       + "b) [NB] Đường tròn $(O; 3\\text{ cm})$ [[blank:2.4cm]] đường thẳng $a$." + BR
       + "c) [NB] Đường tròn $(O; 5\\text{ cm})$ [[blank:2.4cm]] đường thẳng $a$." + BR
       + "d) [NB] Đường tròn $(O; 4\\text{ cm})$ [[blank:2.4cm]] đường thẳng $a$.",
       "a) \\textbf{A}.[[br]]b) Không cắt ($d = 4 > 3$).[[br]]c) Cắt ($d = 4 < 5$).[[br]]d) Tiếp xúc ($d = 4 = R$).",
       figure=OLD_H3,
       slide="Chọn đáp án đúng." + BR + sl2a + BR + "Đường thẳng $a$ cách $O$ một khoảng $4$ cm. Điền cắt / tiếp xúc / không cắt:" + BR
       + "b) [NB] $(O; 3\\text{ cm})$ \\dots{} $a$. \\quad c) [NB] $(O; 5\\text{ cm})$ \\dots{} $a$. \\quad d) [NB] $(O; 4\\text{ cm})$ \\dots{} $a$.")

s3, sl3 = mcq("Nếu đường thẳng $d$ là tiếp tuyến của đường tròn $(O)$ tại $A$ thì:",
              ["$d \\parallel OA$", "$d$ trùng $OA$", "$d \\perp OA$ tại $A$", "$d \\perp OA$ tại $O$"])
b3 = P("Bài 3.", "NB4", "onclass", s3, "\\textbf{C}.", slide=sl3)

s4, sl4 = mcq("Cho tam giác $ABC$ có các đường cao $BD$, $CE$. Chọn khẳng định đúng.",
              ["Bốn điểm $B$, $E$, $D$, $C$ cùng nằm trên một đường tròn.", "Năm điểm $A$, $B$, $E$, $D$, $C$ cùng nằm trên một đường tròn.",
               "Cả A, B đều sai.", "Cả A, B đều đúng."])
b4 = P("Bài 4.", "NB5", "onclass", s4, "\\textbf{A} (đường tròn đường kính $BC$).", slide=s4.split(" \\begin{mcq}")[0] + BR + sl4.split(BR, 1)[1])

b5 = P("Bài 5.", "NB6", "onclass",
       "Cho tam giác $ABC$ cân tại $A$, các đường cao $AD$ và $BE$ cắt nhau tại $H$. Vẽ đường tròn $(O)$ đường kính $AH$ (Hình 5). Mỗi khẳng định sau \\textbf{đúng} hay \\textbf{sai}? Điền Đ hoặc S vào chỗ chấm." + BR
       + "a) [NB] Điểm $E$ nằm trên đường tròn $(O)$. \\quad [[blank:1.1cm]]" + BR
       + "b) [NB] $BD = CD$. \\quad [[blank:1.1cm]]" + BR
       + "c) [NB] $DE > \\frac{1}{2}BC$. \\quad [[blank:1.1cm]]" + BR
       + "d) [NB] $DE$ là tiếp tuyến của đường tròn $(O)$. \\quad [[blank:1.1cm]]",
       "a) Đ ($\\widehat{AEH} = 90^\\circ$).[[br]]b) Đ (đường cao $AD$ của tam giác cân đồng thời là trung tuyến).[[br]]c) S ($ED$ là trung tuyến của $\\triangle BEC$ vuông tại $E$ nên $DE = \\frac{1}{2}BC$).[[br]]d) Đ.",
       figure=fig(h_c45(), "Hình 5"))

b6 = P("Bài 6.", "NB7", "onclass",
       "Cho đường tròn $(O)$ đường kính $AB$, $Ax$ là tiếp tuyến của $(O)$ tại $A$. Tiếp tuyến tại $C$ của $(O)$ cắt $Ax$ tại $M$ (Hình 6). Điền vào chỗ chấm:" + BR
       + "a) [NB] $\\widehat{MAO} = [[blank:1.1cm]]$ vì $Ax$ là tiếp tuyến của $(O)$ tại $A$." + BR
       + "b) [NB] $\\widehat{MCO} = 90^\\circ$ vì [[blank:4.5cm]]." + BR
       + "c) [NB] Bốn điểm $M$, $A$, $C$, $O$ cùng thuộc đường tròn tâm là trung điểm của [[blank:1.1cm]], bán kính bằng [[blank:1.6cm]].",
       "a) $90^\\circ$.[[br]]b) $MC$ là tiếp tuyến của $(O)$ tại $C$.[[br]]c) $MO$; $\\dfrac{MO}{2}$.",
       figure=fig(h_lyson(), "Hình 6"))

b7 = P("Bài 7.", "NB8", "onclass",
       "Cho đường tròn $(O)$ và điểm $A$ nằm ngoài đường tròn. Qua $A$ kẻ đường thẳng $d \\perp OA$, lấy điểm $M$ trên $d$, kẻ tiếp tuyến $MB$ của $(O)$ ($B$ là tiếp điểm) (Hình 7). Điền vào chỗ chấm:" + BR
       + "a) [NB] $\\widehat{MAO} = [[blank:1.1cm]]$ và $\\widehat{MBO} = [[blank:1.1cm]]$." + BR
       + "b) [NB] Hai tam giác vuông $MAO$ và $MBO$ có chung cạnh huyền [[blank:1.1cm]] nên bốn điểm $A$, $M$, $O$, $B$ cùng thuộc đường tròn tâm là trung điểm của cạnh huyền ấy.",
       "a) $90^\\circ$; $90^\\circ$.[[br]]b) $MO$.",
       figure=fig(h_hoangliet(), "Hình 7"))

vd3 = VDU("\\textbf{Ví dụ 3.} Cho $AB$ là một dây không đi qua tâm của đường tròn $(O)$. Đường thẳng qua $O$ và vuông góc với $AB$ tại $H$ cắt tiếp tuyến tại $A$ của $(O)$ ở điểm $C$ (Hình 8). Chứng minh rằng $CB$ là tiếp tuyến của $(O)$." + BR + LG + BR
          + "$OA = OB = R$ $\\Rightarrow \\triangle OAB$ cân tại $O$." + BR
          + "$OH \\perp AB$ $\\Rightarrow OC$ là đường trung trực của $AB$" + BR
          + "$\\Rightarrow CA = [[fill:CB]]$." + BR
          + "Xét $\\triangle OAC$ và $\\triangle OBC$ có: $OA = OB$, $CA = CB$, $OC$ chung" + BR
          + "$\\Rightarrow \\triangle OAC = \\triangle OBC$ ([[fill:c.c.c]])" + BR
          + "$\\Rightarrow \\widehat{OBC} = \\widehat{OAC} = [[fill:90^\\circ]]$." + BR
          + "Vậy $CB \\perp OB$ tại $B \\in (O)$ nên $CB$ là [[fill:tiếp tuyến]] của $(O)$.",
          fig(h_daycung(), "Hình 8"))

b8 = P("Bài 8.", "NB9", "onclass",
       "Cho nửa đường tròn $(O)$ đường kính $AB$, điểm $C$ thuộc nửa đường tròn, $K$ là trung điểm của dây $BC$. Tiếp tuyến tại $B$ cắt tia $OK$ tại $D$ (Hình 9). Điền vào chỗ chấm:" + BR
       + "a) [NB] $\\triangle OBC$ cân tại $O$ có $OK$ là đường trung tuyến nên $OK \\perp [[blank:1.1cm]]$; do đó $OD$ là đường trung trực của $BC$ và $DC = [[blank:1.1cm]]$." + BR
       + "b) [NB] $\\triangle ODC = \\triangle ODB$ (c.c.c) $\\Rightarrow \\widehat{OCD} = \\widehat{OBD} = [[blank:1.1cm]]$, nên $DC$ là [[blank:2.4cm]] của $(O)$.",
       "a) $BC$; $DB$.[[br]]b) $90^\\circ$; tiếp tuyến.",
       figure=fig(h_dongda04(), "Hình 9"))

b9 = P("Bài 9.", "NB10", "onclass",
       "Cho đường tròn $(O; R)$ đường kính $AB$, dây $CD \\perp AB$ tại $H$. Tiếp tuyến tại $A$ và tại $C$ cắt nhau ở $M$, $MC$ cắt $AB$ tại $F$ (Hình 10). Điền vào chỗ chấm:" + BR
       + "a) [NB] $OC = OD = [[blank:1.1cm]]$ nên $\\triangle OCD$ cân tại $O$; $OH \\perp CD$ nên $OH$ là đường trung trực của [[blank:1.1cm]]." + BR
       + "b) [NB] $F$ nằm trên đường trung trực đó nên $FC = [[blank:1.1cm]]$.",
       "a) $R$; $CD$.[[br]]b) $FD$.",
       figure=fig(h_aimo(), "Hình 10"))

# ───────────────────────────── LUYỆN TẬP 2 ─────────────────────────────
HINT_4D = ["Hai góc nào bằng $90^\\circ$? Vì sao?", "Hai tam giác vuông đó có chung cạnh huyền nào? Đỉnh góc vuông thuộc đường tròn đường kính nào?"]
b10 = P("Bài 10.", "TH1", "onclass",
        "[TH] Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài đường tròn. Qua $A$ kẻ đường thẳng $d \\perp OA$. Lấy điểm $M$ bất kì trên $d$. Kẻ tiếp tuyến $MB$ với đường tròn $(O)$ ($B$ là tiếp điểm). Chứng minh bốn điểm $A$, $M$, $O$, $B$ cùng thuộc một đường tròn (dùng Hình 7 ở Bài 7).",
        "$d \\perp OA$ tại $A$ $\\Rightarrow \\widehat{MAO} = 90^\\circ$.[[br]]$MB$ là tiếp tuyến tại $B$ $\\Rightarrow \\widehat{MBO} = 90^\\circ$.[[br]]Gọi $I$ là trung điểm $MO$.[[br]]Xét $\\triangle MAO$ vuông tại $A$, trung tuyến $AI$ $\\Rightarrow AI = \\dfrac{MO}{2} = IM = IO$.[[br]]Xét $\\triangle MBO$ vuông tại $B$, trung tuyến $BI$ $\\Rightarrow BI = \\dfrac{MO}{2}$.[[br]]Vậy $A$, $M$, $O$, $B$ cùng thuộc đường tròn tâm $I$, bán kính $\\dfrac{MO}{2}$.",
        level=2, hints=HINT_4D)
b11 = P("Bài 11.", "TH1", "onclass",
        "[TH] Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$ ($H \\in BC$). Gọi $M$, $N$ lần lượt là chân đường vuông góc hạ từ $H$ xuống hai đường thẳng $AB$, $AC$. Chứng minh bốn điểm $A$, $M$, $H$, $N$ cùng thuộc một đường tròn.",
        "$HM \\perp AB$ $\\Rightarrow \\widehat{AMH} = 90^\\circ$.[[br]]$HN \\perp AC$ $\\Rightarrow \\widehat{ANH} = 90^\\circ$.[[br]]Gọi $O$ là trung điểm $AH$.[[br]]Xét $\\triangle AMH$ vuông tại $M$, trung tuyến $MO$ $\\Rightarrow MO = \\dfrac{AH}{2} = OA = OH$.[[br]]Xét $\\triangle ANH$ vuông tại $N$, trung tuyến $NO$ $\\Rightarrow NO = \\dfrac{AH}{2}$.[[br]]Vậy $A$, $M$, $H$, $N$ cùng thuộc đường tròn tâm $O$, bán kính $\\dfrac{AH}{2}$.",
        level=2, draw=True, hints=HINT_4D)

vd4 = VDU("\\textbf{Ví dụ 4.} Cho đường tròn $(O)$ đi qua ba đỉnh $A$, $B$, $C$ của tam giác $ABC$ cân tại $A$. Chứng minh rằng đường thẳng $xy$ đi qua $A$ và song song với $BC$ là một tiếp tuyến của $(O)$ (Hình 11)." + BR + LG + BR
          + "$AB = AC$ và $OB = OC = R$" + BR
          + "$\\Rightarrow A$, $O$ cùng nằm trên đường trung trực của $BC$" + BR
          + "$\\Rightarrow OA \\perp [[fill:BC]]$." + BR
          + "$xy \\parallel BC$ $\\Rightarrow OA \\perp xy$ tại $[[fill:A]]$." + BR
          + "Vậy $xy$ đi qua $A \\in (O)$ và vuông góc với bán kính $OA$ tại $A$ nên $xy$ là [[fill:tiếp tuyến]] của $(O)$.",
          fig(h_521(), "Hình 11"))

b12 = P("Bài 12.", "TH2", "onclass",
        "Cho nửa đường tròn $(O)$ đường kính $AB$. Lấy điểm $C$ nằm trên nửa đường tròn. Gọi $K$ là trung điểm của dây cung $BC$. Qua $B$ dựng tiếp tuyến với $(O)$ cắt tia $OK$ tại $D$ (dùng Hình 9 ở Bài 8)." + BR
        + "a) [TH] Chứng minh rằng $DO \\perp BC$ và $\\triangle ABC$ vuông." + BR
        + "b) [TH] Chứng minh $DC$ là tiếp tuyến của đường tròn $(O)$.",
        "a) $OB = OC$ $\\Rightarrow \\triangle OBC$ cân tại $O$, trung tuyến $OK$ đồng thời là đường cao $\\Rightarrow DO \\perp BC$.[[br]]$OC = OA = OB = \\dfrac{AB}{2}$ $\\Rightarrow \\triangle ABC$ có trung tuyến $CO$ bằng nửa cạnh $AB$[[br]]$\\Rightarrow \\triangle ABC$ vuông tại $C$.[[br]]b) $OD$ là đường trung trực của $BC$ $\\Rightarrow DC = DB$.[[br]]Xét $\\triangle ODC$ và $\\triangle ODB$ có: $OC = OB$, $DC = DB$, $OD$ chung[[br]]$\\Rightarrow \\triangle ODC = \\triangle ODB$ (c.c.c) $\\Rightarrow \\widehat{OCD} = \\widehat{OBD} = 90^\\circ$.[[br]]Vậy $DC \\perp OC$ tại $C \\in (O)$ nên $DC$ là tiếp tuyến của $(O)$.",
        level=2,
        hints=["Tam giác $OBC$ là tam giác gì? Trung tuyến $OK$ còn là đường gì?", "So sánh $DC$ và $DB$, rồi xét hai tam giác $ODC$, $ODB$."])

vd5 = VDU("\\textbf{Ví dụ 5.} \\textbf{Đề mẫu.} Cho nửa đường tròn tâm $O$, bán kính $R$, đường kính $AB$. Lấy điểm $M$ trên nửa đường tròn ($M$ khác $A$, $B$). Các tiếp tuyến của $(O)$ tại $A$ và tại $M$ cắt nhau tại $C$ (Hình 12)." + BR
          + "a) Chứng minh bốn điểm $O$, $A$, $C$, $M$ cùng thuộc một đường tròn." + BR
          + "b) Qua $O$ kẻ đường thẳng song song với $AM$, cắt $MB$ tại $H$ và cắt đường thẳng $CM$ tại $D$. Chứng minh $OH = \\frac{1}{2}AM$ và $BD$ là tiếp tuyến của $(O)$." + BR + LG + BR
          + "a) $\\widehat{CAO} = \\widehat{CMO} = [[fill:90^\\circ]]$ (tính chất tiếp tuyến)." + BR
          + "Gọi $I$ là trung điểm $CO$ $\\Rightarrow IA = IM = \\dfrac{CO}{2} = IC = IO$." + BR
          + "Vậy $O$, $A$, $C$, $M$ cùng thuộc đường tròn tâm $I$, bán kính $[[fill:\\dfrac{CO}{2}]]$." + BR
          + "b) $O$ là trung điểm $AB$, $OH \\parallel AM$" + BR
          + "$\\Rightarrow H$ là trung điểm $MB$ và $OH = [[fill:\\frac{1}{2}AM]]$ (đường trung bình)." + BR
          + "$OM = OA = OB$ $\\Rightarrow \\triangle AMB$ vuông tại $M$ $\\Rightarrow AM \\perp MB$" + BR
          + "$\\Rightarrow OH \\perp MB$." + BR
          + "$H$ là trung điểm $MB$ nên $OD$ là đường trung trực của $MB$ $\\Rightarrow DM = DB$." + BR
          + "$\\triangle ODM = \\triangle ODB$ (c.c.c) $\\Rightarrow \\widehat{OBD} = \\widehat{OMD} = [[fill:90^\\circ]]$." + BR
          + "Vậy $BD$ là [[fill:tiếp tuyến]] của $(O)$ tại $B$.",
          fig(h_tantrieu(), "Hình 12"))

b13 = json.loads(json.dumps(OLD_P2[5]))
b13["label"] = "Bài 13."
b13["dang_id"] = "VD1"

KH_A = ("a) $MA$, $MC$ là tiếp tuyến $\\Rightarrow \\widehat{MAO} = \\widehat{MCO} = 90^\\circ$.[[br]]"
        "$\\Rightarrow \\triangle MAO$ vuông tại $A$, $\\triangle MCO$ vuông tại $C$, có chung cạnh huyền $MO$.[[br]]"
        "Vậy $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]b)")
_s = b13["solution"]; b13["solution"] = KH_A + _s.split("[[br]]b)", 1)[1]
b13["quy_trinh"][0] = "Ý a: chỉ ra hai tam giác vuông có chung cạnh huyền $MO$ $\\Rightarrow$ bốn điểm cùng thuộc đường tròn đường kính $MO$"

_s = b13["solution"].split("[[br]]b)", 1)[0]
b13["solution"] = _s + ("[[br]]b) $OC = OD = R$ $\\Rightarrow \\triangle OCD$ cân tại $O$.[[br]]"
    "$OH \\perp CD$ ($CH \\perp AB$) $\\Rightarrow$ đường cao $OH$ đồng thời là đường trung tuyến[[br]]"
    "$\\Rightarrow AB$ là đường trung trực của $CD$.[[br]]"
    "$F \\in AB$ $\\Rightarrow FC = FD$.[[br]]"
    "Xét $\\triangle OCF$ và $\\triangle ODF$ có: $OC = OD$, $FC = FD$, $OF$ chung[[br]]"
    "$\\Rightarrow \\triangle OCF = \\triangle ODF$ (c.c.c)[[br]]"
    "$\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$ ($MC$ là tiếp tuyến tại $C$).[[br]]"
    "$\\Rightarrow DF \\perp OD$ tại $D$, mà $D \\in (O)$.[[br]]"
    "Vậy $DF$ là tiếp tuyến của $(O; R)$ tại $D$.")
b13["quy_trinh"] = [b13["quy_trinh"][0],
    "Ý b: $\\triangle OCD$ cân tại $O$, $OH \\perp CD$ $\\Rightarrow AB$ là đường trung trực của $CD$ $\\Rightarrow FC = FD$ (như Bài 8)",
    "$\\triangle OCF = \\triangle ODF$ (c.c.c) $\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = 90^\\circ$",
    "Kết luận theo dấu hiệu nhận biết tiếp tuyến"]

# ───────────────────────────── BTVN ─────────────────────────────
MINDMAP = ST["reflection"]["blocks"][0]
t1 = P("BTVN 1.", "NB2", "btvn",
       "[NB] Bạn Thanh cắt $4$ hình tròn bằng giấy có bán kính lần lượt là $4$ cm, $6$ cm, $7$ cm và $8$ cm để dán lên một mảnh giấy có vẽ sẵn hai đường thẳng song song $a$ và $b$ cách nhau $6$ cm. Bạn dán sao cho tâm của cả $4$ hình tròn đều nằm trên $b$. Hình tròn nào che khuất một phần đường thẳng $a$? Trả lời: [[blank:4.5cm]]",
       "Khoảng cách từ tâm đến $a$ là $d = 6$ cm. Hình tròn bán kính $7$ cm và $8$ cm ($R > d$) che khuất một phần $a$; hình tròn $4$ cm không chạm $a$, hình tròn $6$ cm chỉ tiếp xúc $a$.")
t2 = P("BTVN 2.", "NB3", "btvn",
       "[NB] Cho đường tròn $(O)$ bán kính $5$ cm và bốn điểm $A$, $B$, $C$, $D$ thoả mãn $OA = 3$ cm, $OB = 4$ cm, $OC = 7$ cm, $OD = 5$ cm. Trong bốn điểm đó có bao nhiêu điểm nằm \\textbf{trong} đường tròn?",
       options=["$1$.", "$2$.", "$3$.", "$4$."], solution="Đáp án \\textbf{B} ($A$, $B$; điểm $D$ nằm \\textbf{trên} đường tròn).")
t3 = P("BTVN 3.", "NB5", "btvn",
       "[NB] Cho tam giác $ABC$ có các đường cao $BD$, $CE$ và $BC = 2026$ mm. Bán kính đường tròn đi qua bốn điểm $B$, $E$, $D$, $C$ bằng bao nhiêu milimét? Trả lời: [[blank:2.4cm]]",
       "$1013$ mm (đường tròn đường kính $BC$).")
t4 = P("BTVN 4.", "NB8", "btvn",
       "Cho tam giác $ABC$ nhọn, đường cao $AD$. Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$, $AC$ (Hình 13). Điền vào chỗ chấm:" + BR
       + "a) [NB] $\\widehat{AED} = [[blank:1.1cm]]$ và $\\widehat{AFD} = [[blank:1.1cm]]$." + BR
       + "b) [NB] Bốn điểm $A$, $E$, $D$, $F$ cùng thuộc đường tròn tâm là trung điểm của [[blank:1.1cm]].",
       "a) $90^\\circ$; $90^\\circ$.[[br]]b) $AD$.", figure=fig(h_ltv(), "Hình 13"))
t5 = P("BTVN 5.", "NB9", "btvn",
       "[NB] Cho đường tròn $(O)$, dây $AB$ có trung điểm $I$. Tia $OI$ cắt tiếp tuyến tại $A$ của $(O)$ ở $D$ (Hình 14). Điền vào chỗ chấm: $OD$ là đường trung trực của $AB$ nên $DA = DB$; $\\triangle OAD = \\triangle OBD$ (c.c.c) nên $\\widehat{OBD} = [[blank:1.1cm]]$.",
       "$90^\\circ$ (bằng $\\widehat{OAD}$).", figure=fig(h_daycung(("O", "A", "B", "D", "I")), "Hình 14"))
t6 = P("BTVN 6.", "NB10", "btvn",
       "[NB] Cho đường tròn $(O; R)$ đường kính $AB$, dây $CD \\perp AB$ tại $H$; tiếp tuyến tại $A$ và tại $C$ cắt nhau ở $M$, $MC$ cắt $AB$ tại $F$ (Hình 15). Điền vào chỗ chấm: $AB$ là đường trung trực của $CD$ nên $FD = [[blank:1.1cm]]$ và $\\triangle OCF = \\triangle ODF$ (c.c.c).",
       "$FC$.", figure=fig(h_aimo(), "Hình 15"))
t7 = P("BTVN 7.", "TH1", "btvn",
       "[TH] Cho tam giác $ABC$ nhọn ($AB < AC$), đường cao $AD$ ($D \\in BC$). Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$ và $AC$. Chứng minh bốn điểm $A$, $E$, $D$, $F$ cùng thuộc một đường tròn, chỉ rõ tâm $O$ và bán kính của đường tròn này.",
       "$\\widehat{AED} = \\widehat{AFD} = 90^\\circ$.[[br]]Gọi $O$ là trung điểm $AD$.[[br]]Xét $\\triangle AED$ vuông tại $E$, trung tuyến $EO$ $\\Rightarrow EO = \\dfrac{AD}{2} = OA = OD$.[[br]]Xét $\\triangle AFD$ vuông tại $F$, trung tuyến $FO$ $\\Rightarrow FO = \\dfrac{AD}{2}$.[[br]]Vậy $A$, $E$, $D$, $F$ cùng thuộc đường tròn tâm $O$ (trung điểm $AD$), bán kính $\\dfrac{AD}{2}$.",
       level=2, draw=True, hints=HINT_4D)
t8 = P("BTVN 8.", "TH2", "btvn",
       "[TH] Cho đường tròn $(O; R)$ và dây $AB$ bất kì ($AB < 2R$). Gọi $I$ là trung điểm của $AB$. Tia $OI$ cắt tiếp tuyến tại $A$ của đường tròn $(O)$ ở $D$. Chứng minh $DB$ là tiếp tuyến của đường tròn $(O)$.",
       "$OA = OB$ $\\Rightarrow \\triangle OAB$ cân tại $O$, trung tuyến $OI$ đồng thời là đường cao $\\Rightarrow OD \\perp AB$ tại trung điểm $I$.[[br]]$\\Rightarrow OD$ là đường trung trực của $AB$ $\\Rightarrow DA = DB$.[[br]]Xét $\\triangle OAD$ và $\\triangle OBD$ có: $OA = OB$, $DA = DB$, $OD$ chung[[br]]$\\Rightarrow \\triangle OAD = \\triangle OBD$ (c.c.c) $\\Rightarrow \\widehat{OBD} = \\widehat{OAD} = 90^\\circ$.[[br]]Vậy $DB \\perp OB$ tại $B \\in (O)$ nên $DB$ là tiếp tuyến của $(O)$.",
       level=2, draw=True, hints=["$OI$ còn là đường gì của tam giác cân $OAB$?", "So sánh $DA$, $DB$ rồi xét hai tam giác $OAD$, $OBD$."])
t9 = json.loads(json.dumps(b13))
t9.update(label="BTVN 9.", tier="btvn")
t9["statement"] = ("[VD] Cho đường tròn $(O; R)$, đường kính $AB$. Lấy điểm $C$ thuộc $(O; R)$ sao cho $AC > BC$. Kẻ đường cao $CH$ của $\\triangle ABC$ ($H \\in AB$), kéo dài $CH$ cắt $(O; R)$ tại điểm $D$ ($D \\ne C$). Tiếp tuyến tại điểm $A$ và tiếp tuyến tại điểm $C$ của đường tròn $(O; R)$ cắt nhau tại điểm $M$. Hai đường thẳng $MC$ và $AB$ cắt nhau tại $F$." + BR
                   + "a) Chứng minh bốn điểm $A$, $M$, $C$, $O$ cùng nằm trên một đường tròn." + BR
                   + "b) Chứng minh $DF$ là tiếp tuyến của $(O; R)$.")
t9.pop("quy_trinh", None)

# ───── KHUÔN BỐN ĐIỂM MỚI (Thầy 03/11/2026): "△ABC vuông tại A ⇒ A, B, C cùng thuộc đường tròn đường kính BC" ─────
vd1["text"] = ("\\textbf{Ví dụ 1.} Cho tam giác $ABC$ vuông tại $A$, $M$ là trung điểm của $BC$ (Hình 2). Chứng minh ba điểm $A$, $B$, $C$ cùng thuộc một đường tròn. Đường tròn đó có đường kính là đoạn nào?" + BR + LG + BR
               + "Xét $\\triangle ABC$ vuông tại $A$, trung tuyến $AM$" + BR
               + "$\\Rightarrow AM = [[fill:\\dfrac{BC}{2}]] = MB = MC$." + BR
               + "Vậy $A$, $B$, $C$ cùng thuộc đường tròn đường kính $[[fill:BC]]$." + BR
               + "\\textbf{Ghi nhớ (dùng thẳng từ nay):} $\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$.")
VIDU2["text"] = ("\\textbf{Ví dụ 2.} Cho tam giác nhọn $ABC$ có hai đường cao $BE$, $CF$ (Hình 4). Chứng minh bốn điểm $B$, $C$, $E$, $F$ cùng thuộc một đường tròn." + BR + LG + BR
                 + "$BE \\perp AC$ tại $E$ $\\Rightarrow \\triangle BEC$ vuông tại $E$" + BR
                 + "$\\Rightarrow B$, $E$, $C$ cùng thuộc đường tròn đường kính $[[fill:BC]]$." + BR
                 + "$CF \\perp AB$ tại $F$ $\\Rightarrow \\triangle BFC$ vuông tại $[[fill:F]]$" + BR
                 + "$\\Rightarrow B$, $F$, $C$ cùng thuộc đường tròn đường kính $BC$." + BR
                 + "Vậy $B$, $C$, $E$, $F$ cùng thuộc đường tròn đường kính $[[fill:BC]]$.")
b6["statement"] = b6["statement"].split("c) [NB]")[0] + "c) [NB] Hai tam giác vuông $MAO$ và $MCO$ có chung cạnh huyền $MO$ nên bốn điểm $M$, $A$, $C$, $O$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]."
b6["answer"] = "a) $90^\\circ$.[[br]]b) $MC$ là tiếp tuyến của $(O)$ tại $C$.[[br]]c) $MO$."
b7["statement"] = b7["statement"].split("b) [NB]")[0] + "b) [NB] $\\triangle MAO$ vuông tại $A$, $\\triangle MBO$ vuông tại $B$ nên bốn điểm $A$, $M$, $O$, $B$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]."
b7["answer"] = "a) $90^\\circ$; $90^\\circ$.[[br]]b) $MO$."
b10["answer"] = ("$d \\perp OA$ tại $A$ $\\Rightarrow \\triangle MAO$ vuông tại $A$[[br]]$\\Rightarrow M$, $A$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
                 "$MB$ là tiếp tuyến tại $B$ $\\Rightarrow \\triangle MBO$ vuông tại $B$[[br]]$\\Rightarrow M$, $B$, $O$ cùng thuộc đường tròn đường kính $MO$.[[br]]"
                 "Vậy $A$, $M$, $O$, $B$ cùng thuộc đường tròn đường kính $MO$.")
b11["answer"] = ("$HM \\perp AB$ $\\Rightarrow \\triangle AMH$ vuông tại $M$[[br]]$\\Rightarrow A$, $M$, $H$ cùng thuộc đường tròn đường kính $AH$.[[br]]"
                 "$HN \\perp AC$ $\\Rightarrow \\triangle ANH$ vuông tại $N$[[br]]$\\Rightarrow A$, $N$, $H$ cùng thuộc đường tròn đường kính $AH$.[[br]]"
                 "Vậy $A$, $M$, $H$, $N$ cùng thuộc đường tròn đường kính $AH$.")
_t = vd5["text"]; _a, _rest = _t.split("a) $\\widehat{CAO}", 1); _b = _rest.split("b) $O$ là trung điểm", 1)[1]
vd5["text"] = (_a + "a) $\\widehat{CAO} = \\widehat{CMO} = [[fill:90^\\circ]]$ (tính chất tiếp tuyến)" + BR
               + "$\\Rightarrow \\triangle CAO$ vuông tại $A$, $\\triangle CMO$ vuông tại $M$, có chung cạnh huyền $CO$." + BR
               + "Vậy $O$, $A$, $C$, $M$ cùng thuộc đường tròn đường kính $[[fill:CO]]$." + BR + "b) $O$ là trung điểm" + _b)
t4["statement"] = t4["statement"].split("b) [NB]")[0] + "b) [NB] Bốn điểm $A$, $E$, $D$, $F$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]."
t7["answer"] = ("$DE \\perp AB$ $\\Rightarrow \\triangle AED$ vuông tại $E$[[br]]$\\Rightarrow A$, $E$, $D$ cùng thuộc đường tròn đường kính $AD$.[[br]]"
                "$DF \\perp AC$ $\\Rightarrow \\triangle AFD$ vuông tại $F$[[br]]$\\Rightarrow A$, $F$, $D$ cùng thuộc đường tròn đường kính $AD$.[[br]]"
                "Vậy $A$, $E$, $D$, $F$ cùng thuộc đường tròn đường kính $AD$: tâm $O$ là trung điểm $AD$, bán kính $\\dfrac{AD}{2}$.")
MINDMAP = json.loads(json.dumps(MINDMAP))
MINDMAP["branches"][0]["children"] = [{"label": "Hai góc vuông chung cạnh huyền"},
                                      {"label": "Tam giác vuông $\\Rightarrow$ đỉnh thuộc đường tròn đường kính cạnh huyền"},
                                      {"label": "Kết luận: đường tròn đường kính cạnh huyền"}]

# ═════ THANG DẪN DẮT (Thầy 03/11: "các bài cứ không liên quan đến nhau") ═════
import re as _re
def H(text, variant="heading"):
    return {"type": "para", "variant": variant, "text": text}

MUC_TIEU = {"type": "para", "text": ("\\textbf{Đích của buổi học:} tự giải trọn \\textbf{Bài 13} — đề thi Câu IV.2 (đề Ái Mộ): "
            "ý a chứng minh bốn điểm cùng thuộc một đường tròn, ý b chứng minh tiếp tuyến.[[br]]"
            "\\textbf{Mạch 1} luyện ý a, \\textbf{Mạch 2} luyện ý b; Bài 5 và Bài 8 làm ngay trên hình của đề ấy.")}
M1 = H("Mạch 1. Ý a — Bốn điểm cùng thuộc một đường tròn")
M2 = H("Mạch 2. Ý b — Chứng minh một đường thẳng là tiếp tuyến")
M3 = H("Kiểm tra nhanh")
L1 = H("Bậc 1. Tự trình bày lại (bỏ giàn giáo)")
L2 = H("Bậc 2. Trọn đề thi")

# Mạch 1
bA1 = b1; bA1["label"] = "Bài 1."
bA2 = b4; bA2["label"] = "Bài 2."; bA2["statement"] = bA2["statement"].replace("Chọn khẳng định đúng.", "Góc vuông lấy từ \\textbf{đường cao}. Chọn khẳng định đúng.")
bA3 = b3; bA3["label"] = "Bài 3."; bA3["statement"] = bA3["statement"].replace("[NB] Nếu", "[NB] Góc vuông lấy từ \\textbf{tiếp tuyến}. Nếu")
bA4 = b7; bA4["label"] = "Bài 4."
bA5 = P("Bài 5.", "NB7", "onclass",
        "\\textbf{Đề Ái Mộ — ý a.} Cho $(O; R)$ đường kính $AB$, $C \\in (O)$ với $AC > BC$; đường cao $CH$ của $\\triangle ABC$ kéo dài cắt $(O)$ tại $D$; tiếp tuyến tại $A$ và tại $C$ cắt nhau ở $M$; $MC$ cắt $AB$ tại $F$ (Hình 5). Điền vào chỗ chấm:" + BR
        + "a) [NB] $\\widehat{MAO} = [[blank:1.1cm]]$ vì $MA$ là tiếp tuyến của $(O)$ tại $A$." + BR
        + "b) [NB] $\\widehat{MCO} = 90^\\circ$ vì [[blank:4.5cm]]." + BR
        + "c) [NB] $\\triangle MAO$, $\\triangle MCO$ vuông có chung cạnh huyền $MO$ nên $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính [[blank:1.1cm]].",
        "a) $90^\\circ$.[[br]]b) $MC$ là tiếp tuyến của $(O)$ tại $C$.[[br]]c) $MO$.",
        figure=fig(h_aimo(), "Hình 5"))
# Mạch 2
bB1 = b2; bB1["label"] = "Bài 6."
bB1["statement"] = (bB1["statement"].split("d) [NB]")[0].rstrip()).replace("(Hình 3)", "(Hình 6)")
bB1["statement"] = bB1["statement"].rsplit("[[br]]", 1)[0] if bB1["statement"].endswith("[[br]]") else bB1["statement"]
bB1["answer"] = "a) \\textbf{A}.[[br]]b) Không cắt ($d = 4 > 3$).[[br]]c) Cắt ($d = 4 < 5$)."
bB1["statement_slide"] = bB1["statement_slide"].split(" \\quad d) [NB]")[0]
bB1["figure"] = dict(bB1["figure"]); bB1["figure"]["caption"] = "Hình 6"
vdB1 = vd4
vdB1["text"] = vdB1["text"].replace("Ví dụ 4.", "Ví dụ 3.").replace("(Hình 11)", "(Hình 7)") .replace("\\textbf{Ví dụ 3.}", "\\textbf{Ví dụ 3.} \\textit{(Dấu hiệu nhận biết dùng trực tiếp.)}")
vdB1["figure"] = dict(vdB1["figure"]); vdB1["figure"]["caption"] = "Hình 7"
vdB2 = vd3
vdB2["text"] = vdB2["text"].replace("Ví dụ 3.", "Ví dụ 4.").replace("(Hình 8)", "(Hình 8)").replace("\\textbf{Ví dụ 4.}", "\\textbf{Ví dụ 4.} \\textit{(Lấy góc $90^\\circ$ qua hai tam giác bằng nhau.)}")
bB2 = b8; bB2["label"] = "Bài 7."; bB2["statement"] = bB2["statement"].replace("(Hình 9)", "(Hình 9)").replace("Cho nửa đường tròn", "Làm như Ví dụ 4. Cho nửa đường tròn")
bB3 = P("Bài 8.", "NB10", "onclass",
        "\\textbf{Đề Ái Mộ — ý b} (tiếp tục với Hình 5 ở Bài 5). Điền vào chỗ chấm:" + BR
        + "a) [NB] $OC = OD = R$ nên $\\triangle OCD$ cân tại $O$; $OH \\perp CD$ nên $OH$ là đường trung trực của $CD$, do đó $FC = [[blank:1.1cm]]$." + BR
        + "b) [NB] $\\triangle OCF = \\triangle ODF$ theo trường hợp [[blank:1.6cm]]." + BR
        + "c) [NB] $\\widehat{ODF} = \\widehat{OCF} = [[blank:1.1cm]]$, mà $D \\in (O)$ nên $DF$ là [[blank:2.4cm]] của $(O)$.",
        "a) $FD$.[[br]]b) c.c.c.[[br]]c) $90^\\circ$; tiếp tuyến.")
bC = b5; bC["label"] = "Bài 9."; bC["statement"] = bC["statement"].replace("(Hình 5)", "(Hình 10)")
bC["figure"] = dict(bC["figure"]); bC["figure"]["caption"] = "Hình 10"
# Luyện tập 2
b10["statement"] = b10["statement"].replace("(dùng Hình 7 ở Bài 7)", "(tự trình bày lại Bài 4, dùng Hình 4)")
b12["statement"] = b12["statement"].replace("(dùng Hình 9 ở Bài 8)", "(tự trình bày lại Bài 7, dùng Hình 9)")
vd5["text"] = vd5["text"].replace("(Hình 12)", "(Hình 11)")
vd5["figure"] = dict(vd5["figure"]); vd5["figure"]["caption"] = "Hình 11"
b11["statement"] = b11["statement"].replace("[TH] Cho", "[TH] (Hình mới, cùng cách.) Cho")
# BTVN
t4["statement"] = t4["statement"].replace("(Hình 13)", "(Hình 12)"); t4["figure"]["caption"] = "Hình 12"
t6["statement"] = t6["statement"].replace("(Hình 15)", "(Hình 13)").replace("Điền vào chỗ chấm: $AB$ là đường trung trực của $CD$ nên $FD = [[blank:1.1cm]]$ và $\\triangle OCF = \\triangle ODF$ (c.c.c).",
                                                                      "Điền vào chỗ chấm: $AB$ là đường trung trực của $CD$ nên $FD = [[blank:1.1cm]]$; $\\triangle OCF = \\triangle ODF$ (c.c.c) nên $\\widehat{ODF} = 90^\\circ$ và $DF$ là tiếp tuyến của $(O)$.")
t6["figure"]["caption"] = "Hình 13"
t2b = P("BTVN 2.", "NB2", "btvn",
        "[NB] Điền vào bảng ($R$ là bán kính đường tròn, $d$ là khoảng cách từ tâm đến đường thẳng):" + BR
        + "\\begin{tabular}{|c|c|c|}\\hline $R$ & $d$ & Vị trí tương đối \\\\ \\hline $5$ cm & $3$ cm & [[blank:2.4cm]] \\\\ \\hline $6$ cm & [[blank:1.1cm]] & Tiếp xúc nhau \\\\ \\hline $4$ cm & $7$ cm & [[blank:2.4cm]] \\\\ \\hline \\end{tabular}",
        "$R = 5$, $d = 3$: cắt nhau; $d = 6$ cm; $R = 4$, $d = 7$: không giao nhau.")
VIDU2["figure"]["caption"] = "Hình 3"; VIDU2["text"] = VIDU2["text"].replace("(Hình 4)", "(Hình 3)")
bA4["figure"] = dict(bA4["figure"]); bA4["figure"]["caption"] = "Hình 4"; bA4["statement"] = bA4["statement"].replace("(Hình 7)", "(Hình 4)")
TS = [t1, t2b, t2, t3, t4, t6, t7, t8, t9]
for k, t in enumerate(TS, 1):
    t["label"] = f"BTVN {k}."

# ───────────────────────────── LẮP ─────────────────────────────
new = json.loads(json.dumps(old))
S = {s["kind"]: s for s in new["stages"]}
# ───── Kiến thức trọng tâm: Dạng 1 theo khuôn mới ─────
CB = S["concept"]["blocks"]
CB[13]["items"][0]["desc"] = ("Trong tam giác vuông, đường trung tuyến ứng với cạnh huyền bằng nửa cạnh huyền. "
                              "Do đó: $\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ ba điểm $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$.")
CB[14]["caption"] = "$\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$"
CB[17]["text"] = ("\\textbf{Phương pháp:} dùng tam giác vuông — $\\triangle ABC$ vuông tại $A$ $\\Rightarrow$ $A$, $B$, $C$ cùng thuộc đường tròn đường kính $BC$. "
                  "Trường hợp hay gặp: \\textbf{hai tam giác vuông có chung cạnh huyền}.")
CB[18]["items"] = [{"term": "Bước 1:", "desc": "Chỉ ra hai góc vuông (từ đường cao, đường vuông góc, hoặc tính chất tiếp tuyến)."},
                   {"term": "Bước 2:", "desc": "Mỗi tam giác vuông $\\Rightarrow$ đỉnh góc vuông thuộc đường tròn đường kính cạnh huyền chung."},
                   {"term": "Bước 3:", "desc": "Kết luận bốn điểm cùng thuộc đường tròn \\textbf{đường kính} là cạnh huyền chung."}]
CB[19]["caption"] = "Hai tam giác vuông chung cạnh huyền $AC$ $\\Rightarrow$ $A$, $B$, $C$, $D$ cùng thuộc đường tròn đường kính $AC$"

# ───── Kiến thức trọng tâm dạng THẺ (03/11/2026, Thầy: "thiết kế đẹp và chuyên nghiệp hơn") ─────
def _lines(items):
    return "[[br]]".join(f"\\nhanly{{{it['term']}}} {it['desc']}" for it in items)
def CARD(title, text, fig_block, cap=None):
    f = {"tikz": fig_block["tikz"], "caption": cap if cap is not None else fig_block.get("caption", ""), "pos": "right"}
    return {"type": "noted", "variant": "theory", "title": title, "text": text, "figure": f}
CB = S["concept"]["blocks"]
CARDS = [
    {"type": "para", "variant": "part", "text": "A. Lý thuyết"},
    CARD("1. ĐƯỜNG TRÒN", "\\nhanly{Định nghĩa.} " + CB[2]["text"].replace("Cho điểm $M$:", "").strip() + "[[br]]" + _lines(CB[3]["items"]), CB[4]),
    CARD("2. VỊ TRÍ TƯƠNG ĐỐI CỦA ĐƯỜNG THẲNG VÀ ĐƯỜNG TRÒN", _lines(CB[6]["items"]) + "[[br]]\\nhanly{Gọi $d$ là khoảng cách từ $O$ đến $a$:} " + CB[7]["text"].split(":", 1)[1].strip(), CB[8]),
    CARD("3. TIẾP TUYẾN — TÍNH CHẤT VÀ DẤU HIỆU NHẬN BIẾT", _lines(CB[10]["items"]), CB[11]),
    CARD("4. KIẾN THỨC LỚP DƯỚI THƯỜNG DÙNG", _lines(CB[13]["items"]), CB[14]),
    {"type": "para", "variant": "part", "text": "B. Phương pháp chứng minh — các dạng quen thuộc"},
    CARD("DẠNG 1. BỐN ĐIỂM CÙNG THUỘC MỘT ĐƯỜNG TRÒN", CB[17]["text"].replace("\\textbf{Phương pháp:}", "\\nhanly{Phương pháp.}") + "[[br]]" + _lines(CB[18]["items"]), CB[19]),
    CARD("DẠNG 2. CHỨNG MINH MỘT ĐƯỜNG THẲNG LÀ TIẾP TUYẾN", CB[21]["text"].replace("\\textbf{Phương pháp:}", "\\nhanly{Phương pháp.}") + "[[br]]" + _lines(CB[22]["items"]), CB[23]),
]
S["concept"]["blocks"] = CARDS
S["practice1"]["blocks"] = [MUC_TIEU, M1, vd1, bA1, bA2, VIDU2, bA3, bA4, bA5, M2, bB1, vdB2, bB2, bB3, M3, bC]
S["practice1"]["teacher_note"] = (
    "20 câu nhận biết trên hình in sẵn, khoảng 1 phút một câu: trắc nghiệm, Đúng/Sai, điền ngắn. "
    "Bài 1--4 ôn lý thuyết (vị trí tương đối, tính chất tiếp tuyến, hai đường cao); Bài 5 Đúng/Sai gom bốn điểm + tiếp tuyến; "
    "Bài 6, 7 là các bước của ý a đề thi (Bài 10); Bài 8 là các bước của Bài 12 (đề Đống Đa); Bài 9 là bước đầu ý b của Bài 13 (đề Ái Mộ).")
S["practice2"]["blocks"] = [L1, b10, b11, b12, L2, vd5, b13]
S["practice2"]["teacher_note"] = (
    "Thông hiểu trước, vận dụng sau. Bài 10, 11, 12, 13 KHÔNG in hình: HS tự vẽ (đã tính $+5$ phút mỗi hình). "
    "Bài 13 là đề Ái Mộ (ý a và b) — HS trình bày trọn như đi thi, GV chỉ nhắc quy trình. Ví dụ 5 (đề Tân Triều) cùng cách chứng minh tiếp tuyến nhưng khác hình.")


# ═════ KHUNG BÀI GIẢI ĐI THI (Thầy 03/11: "HS điền khuyết thì cũng điền khuyết bài trình bày như đi thi", cả BTVN) ═════
KG = "Điền vào chỗ chấm để hoàn thành bài giải:"
R_ = "\\Rightarrow"
bA4["statement"] = ("Cho đường tròn $(O)$ và điểm $A$ nằm ngoài đường tròn. Qua $A$ kẻ đường thẳng $d \\perp OA$, lấy điểm $M$ trên $d$, kẻ tiếp tuyến $MB$ của $(O)$ ($B$ là tiếp điểm) (Hình 7). Chứng minh bốn điểm $A$, $M$, $O$, $B$ cùng thuộc một đường tròn. " + KG + BR
    + "a) [NB] $d \\perp OA$ tại $A$ $\\Rightarrow \\triangle MAO$ vuông tại [[blank:1.1cm]]" + BR + "$\\Rightarrow M$, $A$, $O$ cùng thuộc đường tròn đường kính $MO$." + BR
    + "b) [NB] $MB$ là tiếp tuyến của $(O)$ tại $B$ $\\Rightarrow \\triangle MBO$ vuông tại [[blank:1.1cm]]" + BR + "$\\Rightarrow M$, $B$, $O$ cùng thuộc đường tròn đường kính $MO$." + BR
    + "Vậy $A$, $M$, $O$, $B$ cùng thuộc đường tròn đường kính [[blank:1.1cm]].")
bA4["answer"] = "a) $A$.[[br]]b) $B$; $MO$."
bA5["statement"] = ("\\textbf{Đề Ái Mộ — ý a.} Cho $(O; R)$ đường kính $AB$, $C \\in (O)$ với $AC > BC$; đường cao $CH$ của $\\triangle ABC$ kéo dài cắt $(O)$ tại $D$; tiếp tuyến tại $A$ và tại $C$ cắt nhau ở $M$; $MC$ cắt $AB$ tại $F$ (Hình 5). Chứng minh bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn. " + KG + BR
    + "a) [NB] $MA$ là tiếp tuyến của $(O)$ tại $A$ $\\Rightarrow \\widehat{MAO} = [[blank:1.1cm]]$" + BR + "$\\Rightarrow \\triangle MAO$ vuông tại $A$" + BR + "$\\Rightarrow M$, $A$, $O$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]." + BR
    + "b) [NB] $MC$ là [[blank:2.4cm]] của $(O)$ tại $C$ $\\Rightarrow \\triangle MCO$ vuông tại $C$" + BR + "$\\Rightarrow M$, $C$, $O$ cùng thuộc đường tròn đường kính $MO$." + BR
    + "c) [NB] Vậy $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính [[blank:1.1cm]].")
bA5["answer"] = "a) $90^\\circ$; $MO$.[[br]]b) tiếp tuyến.[[br]]c) $MO$."
bB1["statement"] = bB1["statement"].replace("b) [NB] Đường tròn $(O; 3\\text{ cm})$ [[blank:2.4cm]] đường thẳng $a$.",
    "b) [NB] Với $(O; 3\\text{ cm})$: $d = 4$ [[blank:0.8cm]] $R = 3$ nên đường thẳng $a$ và đường tròn [[blank:2.4cm]].").replace(
    "c) [NB] Đường tròn $(O; 5\\text{ cm})$ [[blank:2.4cm]] đường thẳng $a$.",
    "c) [NB] Với $(O; 5\\text{ cm})$: $d = 4$ [[blank:0.8cm]] $R = 5$ nên đường thẳng $a$ và đường tròn [[blank:2.4cm]].").replace(
    "Điền \\textbf{cắt}, \\textbf{tiếp xúc} hoặc \\textbf{không cắt} vào chỗ chấm:", "Điền vào chỗ chấm ($>$, $<$, $=$; cắt nhau, tiếp xúc, không giao nhau):")
bB1["answer"] = "a) \\textbf{A}.[[br]]b) $>$; không giao nhau.[[br]]c) $<$; cắt nhau."
bB2["statement"] = ("Làm như Ví dụ 3. Cho nửa đường tròn $(O)$ đường kính $AB$, điểm $C$ thuộc nửa đường tròn, $K$ là trung điểm của dây $BC$. Tiếp tuyến tại $B$ cắt tia $OK$ tại $D$ (Hình 9). Chứng minh $DC$ là tiếp tuyến của $(O)$. " + KG + BR
    + "a) [NB] $OB = OC$ $\\Rightarrow \\triangle OBC$ cân tại $O$." + BR + "Trung tuyến $OK$ đồng thời là đường cao $\\Rightarrow OD \\perp [[blank:1.1cm]]$" + BR
    + "$\\Rightarrow OD$ là đường trung trực của $BC$ $\\Rightarrow DC = [[blank:1.1cm]]$." + BR
    + "b) [NB] Xét $\\triangle ODC$ và $\\triangle ODB$ có: $OC = OB$, $DC = DB$, $OD$ chung" + BR
    + "$\\Rightarrow \\triangle ODC = \\triangle ODB$ ([[blank:1.1cm]])" + BR + "$\\Rightarrow \\widehat{OCD} = \\widehat{OBD} = [[blank:1.1cm]]$" + BR
    + "$\\Rightarrow DC \\perp OC$ tại $C \\in (O)$." + BR + "Vậy $DC$ là [[blank:2.4cm]] của $(O)$.")
bB2["answer"] = "a) $BC$; $DB$.[[br]]b) c.c.c; $90^\\circ$; tiếp tuyến."
bB3["statement"] = ("\\textbf{Đề Ái Mộ — ý b} (tiếp tục với Hình 5 ở Bài 5). Chứng minh $DF$ là tiếp tuyến của $(O; R)$. " + KG + BR
    + "a) [NB] $OC = OD = R$ $\\Rightarrow \\triangle OCD$ cân tại $O$." + BR
    + "$OH \\perp CD$ $\\Rightarrow$ đường cao $OH$ đồng thời là trung tuyến" + BR + "$\\Rightarrow AB$ là đường trung trực của $CD$." + BR
    + "$F \\in AB$ $\\Rightarrow FC = [[blank:1.1cm]]$." + BR
    + "b) [NB] Xét $\\triangle OCF$ và $\\triangle ODF$ có: $OC = OD$, $FC = FD$, $OF$ chung" + BR + "$\\Rightarrow \\triangle OCF = \\triangle ODF$ ([[blank:1.1cm]])." + BR
    + "c) [NB] $\\Rightarrow \\widehat{ODF} = \\widehat{OCF} = [[blank:1.1cm]]$ ($MC$ là tiếp tuyến tại $C$)" + BR
    + "$\\Rightarrow DF \\perp OD$ tại $D \\in (O)$." + BR + "Vậy $DF$ là [[blank:2.4cm]] của $(O; R)$.")
bB3["answer"] = "a) $FD$.[[br]]b) c.c.c.[[br]]c) $90^\\circ$; tiếp tuyến."

# ── BTVN: mọi câu nhận biết là KHUNG BÀI GIẢI đi thi ──
k1 = P("BTVN 1.", "NB3", "btvn",
       "Gọi $O$ là trung điểm của đoạn thẳng $AB$. Vẽ đường tròn $(O; OA)$. Chứng minh đường tròn $(O; OA)$ đi qua $B$ và có đường kính là $AB$. " + KG + BR
       + "[NB] $O$ là trung điểm $AB$ $\\Rightarrow OB = [[blank:1.1cm]]$" + BR + "$\\Rightarrow B$ thuộc đường tròn $(O; OA)$." + BR
       + "Vậy $(O; OA)$ đi qua $A$, $B$ và có đường kính [[blank:1.1cm]].",
       "$OA$; $AB$.")
k2 = P("BTVN 2.", "NB5", "btvn",
       "Cho tam giác $ABC$ có các đường cao $BD$, $CE$ và $BC = 2026$ mm. Chứng minh bốn điểm $B$, $E$, $D$, $C$ cùng thuộc một đường tròn và tính bán kính của đường tròn đó. " + KG + BR
       + "[NB] $BD \\perp AC$ tại $D$ $\\Rightarrow \\triangle BDC$ vuông tại $D$" + BR + "$\\Rightarrow B$, $D$, $C$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]." + BR
       + "$CE \\perp AB$ tại $E$ $\\Rightarrow \\triangle BEC$ vuông tại $E$" + BR + "$\\Rightarrow B$, $E$, $C$ cùng thuộc đường tròn đường kính $BC$." + BR
       + "Vậy $B$, $E$, $D$, $C$ cùng thuộc đường tròn đường kính $BC$, bán kính $R = \\dfrac{BC}{2} = [[blank:1.6cm]]$ mm.",
       "$BC$; $1013$.")
k3 = t4
k3["statement"] = ("Cho tam giác $ABC$ nhọn, đường cao $AD$. Gọi $E$, $F$ lần lượt là hình chiếu vuông góc của $D$ lên $AB$, $AC$ (Hình 11). Chứng minh bốn điểm $A$, $E$, $D$, $F$ cùng thuộc một đường tròn. " + KG + BR
    + "a) [NB] $DE \\perp AB$ tại $E$ $\\Rightarrow \\triangle AED$ vuông tại [[blank:1.1cm]]" + BR + "$\\Rightarrow A$, $E$, $D$ cùng thuộc đường tròn đường kính [[blank:1.1cm]]." + BR
    + "b) [NB] $DF \\perp AC$ tại $F$ $\\Rightarrow \\triangle AFD$ vuông tại $F$" + BR + "$\\Rightarrow A$, $F$, $D$ cùng thuộc đường tròn đường kính $AD$." + BR
    + "Vậy $A$, $E$, $D$, $F$ cùng thuộc đường tròn đường kính [[blank:1.1cm]].")
k3["answer"] = "a) $E$; $AD$.[[br]]b) $AD$."
k3["figure"] = dict(k3["figure"]); k3["figure"]["caption"] = "Hình 11"
k4 = P("BTVN 4.", "NB2", "btvn",
       "Bạn Thanh cắt $4$ hình tròn bằng giấy có bán kính $4$ cm, $6$ cm, $7$ cm và $8$ cm, dán lên một mảnh giấy có hai đường thẳng song song $a$, $b$ cách nhau $6$ cm sao cho tâm cả $4$ hình tròn đều nằm trên $b$. Hình tròn nào che khuất một phần đường thẳng $a$? " + KG + BR
       + "Tâm các hình tròn nằm trên $b$ $\\Rightarrow$ khoảng cách từ tâm đến $a$ là $d = [[blank:1.1cm]]$ cm." + BR
       + "a) [NB] Hình tròn bán kính $4$ cm: $R < d$ $\\Rightarrow$ hình tròn và $a$ [[blank:2.4cm]]." + BR + "Hình tròn bán kính $6$ cm: $R = d$ $\\Rightarrow$ hình tròn [[blank:2.4cm]] với $a$." + BR
       + "b) [NB] Hình tròn bán kính $7$ cm, $8$ cm: $R$ [[blank:0.8cm]] $d$ $\\Rightarrow$ cắt $a$." + BR
       + "Vậy hình tròn bán kính [[blank:2.4cm]] che khuất một phần đường thẳng $a$.",
       "$6$.[[br]]a) không giao nhau; tiếp xúc.[[br]]b) $>$.[[br]]$7$ cm và $8$ cm.")
k5 = P("BTVN 5.", "NB9", "btvn",
       "Cho đường tròn $(O; R)$ và dây $AB$ bất kì ($AB < 2R$). Gọi $I$ là trung điểm của $AB$. Tia $OI$ cắt tiếp tuyến tại $A$ của $(O)$ ở $D$ (Hình 12). Chứng minh $DB$ là tiếp tuyến của $(O)$. " + KG + BR
       + "a) [NB] $OA = OB$ $\\Rightarrow \\triangle OAB$ cân tại $O$; trung tuyến $OI$ đồng thời là đường cao" + BR
       + "$\\Rightarrow OD$ là đường trung trực của $AB$ $\\Rightarrow DA = DB$." + BR
       + "b) Xét $\\triangle OAD$ và $\\triangle OBD$ có: $OA = OB$, $DA = DB$, $OD$ chung" + BR
       + "$\\Rightarrow \\triangle OAD = \\triangle OBD$ (c.c.c)" + BR + "$\\Rightarrow \\widehat{OBD} = \\widehat{OAD} = [[blank:1.1cm]]$" + BR
       + "$\\Rightarrow DB \\perp OB$ tại $B \\in (O)$." + BR + "Vậy $DB$ là [[blank:2.4cm]] của $(O)$.",
       "$90^\\circ$; tiếp tuyến.", figure=fig(h_daycung(("O", "A", "B", "D", "I")), "Hình 12"))
k6 = P("BTVN 6.", "TH1", "btvn",
       "[TH] Cho $\\triangle ABC$ nhọn nội tiếp đường tròn $(O)$, hai đường cao $AN$, $CK$ cắt nhau tại $H$. Chứng minh bốn điểm $B$, $K$, $H$, $N$ cùng thuộc một đường tròn. Xác định tâm $I$ của đường tròn đó.",
       "$CK \\perp AB$ tại $K$ $\\Rightarrow \\triangle BKH$ vuông tại $K$[[br]]$\\Rightarrow B$, $K$, $H$ cùng thuộc đường tròn đường kính $BH$.[[br]]$AN \\perp BC$ tại $N$ $\\Rightarrow \\triangle BNH$ vuông tại $N$[[br]]$\\Rightarrow B$, $N$, $H$ cùng thuộc đường tròn đường kính $BH$.[[br]]Vậy $B$, $K$, $H$, $N$ cùng thuộc đường tròn đường kính $BH$, tâm $I$ là trung điểm $BH$.",
       level=2, draw=True, hints=HINT_4D)
k7 = P("BTVN 7.", "TH2", "btvn",
       "[TH] Cho đường tròn $(O; R)$ và điểm $M$ nằm ngoài đường tròn, $MB$ là tiếp tuyến của $(O)$ ($B$ là tiếp điểm). Trên đường tròn $(O)$ lấy điểm $C$ sao cho $OM$ là tia phân giác của $\\widehat{BOC}$. Chứng minh $MC$ là tiếp tuyến của đường tròn $(O)$.",
       "Xét $\\triangle OBM$ và $\\triangle OCM$ có: $OB = OC = R$, $\\widehat{BOM} = \\widehat{COM}$ ($OM$ là tia phân giác), $OM$ chung[[br]]$\\Rightarrow \\triangle OBM = \\triangle OCM$ (c.g.c)[[br]]$\\Rightarrow \\widehat{OCM} = \\widehat{OBM} = 90^\\circ$ ($MB$ là tiếp tuyến tại $B$)[[br]]$\\Rightarrow MC \\perp OC$ tại $C \\in (O)$.[[br]]Vậy $MC$ là tiếp tuyến của $(O)$.",
       level=2, draw=True, hints=["$OM$ là tia phân giác cho ta hai góc nào bằng nhau?", "Xét hai tam giác $OBM$, $OCM$ (c.g.c)."])
k8 = t9
TS = [k1, k2, k3, k4, k5, k6, k7, k8]
for k, t in enumerate(TS, 1):
    t["label"] = f"BTVN {k}."

S["reflection"]["blocks"] = [MINDMAP] + TS
S["reflection"]["teacher_note"] = (
    "BTVN trình bày như đi thi: BTVN 1--3 điền khung bài giải mạch 1 (ý a), BTVN 4--5 điền khung bài giải mạch 2 (ý b); "
    "BTVN 6, 7 HS tự trình bày trên hình mới (bốn điểm; tiếp tuyến qua c.g.c); BTVN 8 là đề Hát Môn — đề song song với Bài 13. Chữa BTVN 8 đầu buổi 3.")

# ───── đánh lại số Hình / Ví dụ theo thứ tự xuất hiện ─────
def _renum(stages):
    blocks = [b for st in stages for b in st["blocks"]]
    hmap, vmap, h, v = {}, {}, 1, 0
    for b in blocks:
        if b.get("type") == "noted" and b.get("variant") == "example":
            m = _re.search(r"Ví dụ (\d+)\.", b["text"]); v += 1
            if m: vmap[m.group(1)] = str(v)
        f = b.get("figure")
        if isinstance(f, dict) and str(f.get("caption", "")).startswith("Hình "):
            h += 1; hmap[f["caption"].split()[1]] = str(h); f["caption"] = f"Hình {h}"
    def fix(t):
        t = _re.sub(r"Hình (\d+)", lambda m: "Hình @" + hmap.get(m.group(1), m.group(1)), t)
        t = _re.sub(r"Ví dụ (\d+)", lambda m: "Ví dụ @" + vmap.get(m.group(1), m.group(1)), t)
        return t.replace("Hình @", "Hình ").replace("Ví dụ @", "Ví dụ ")
    for b in blocks:
        for k in ("text", "statement", "statement_slide"):
            if isinstance(b.get(k), str):
                b[k] = fix(b[k])
    return hmap, vmap
print(_renum([S["practice1"], S["practice2"], S["reflection"]]))
json.dump(new, open(out, "w"), ensure_ascii=False, indent=1)
print("ok")
