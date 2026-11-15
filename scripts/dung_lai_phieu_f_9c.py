# -*- coding: utf-8 -*-
"""Dựng lại phần bài phiếu F chương VI 9C (12/11/2026).

Sửa: cắt dạng "lập PT nhận hai số làm nghiệm" -> "biết một nghiệm, tìm nghiệm còn lại + hệ số";
ví dụ khác bài, không trùng phương trình; khung Viète 4 bước; LT1 + BTVN NB toàn điền khuyết;
bỏ chấm phẩy (mỗi bước một dòng); bỏ "Biết ... có hai nghiệm phân biệt" khỏi câu dẫn;
btvn_phieu_rieng; số ý khớp spec (24/6 trên lớp, 16 NB BTVN).
"""
import json, sys, copy

P = sys.argv[1]
d = json.load(open(P, encoding="utf-8"))
old = {b.get("label"): b for s in d["stages"] for b in s["blocks"] if b.get("type") == "problem"}

H = r"\hspace*{1.4em}"
D = r"\ldots\ldots"
LG = r"{\sffamily\bfseries\color{brand}Lời giải}"


def lines(*ls):
    return "[[br]]".join(H + l for l in ls)


def ex(n, de, *sol):
    return {"type": "noted", "variant": "example",
            "text": rf"\textbf{{Ví dụ {n}.}} " + de + "[[br]]" + LG + "[[br]]" + lines(*sol)}


def pb(n, stmt, sol, tier, level, dang, **kw):
    b = {"type": "problem", "label": f"Bài {n}.", "statement": stmt, "tier": tier, "level": level,
         "solution": sol, "dang_id": dang, "writelines": 0}
    b.update(kw)
    return b


def y(tag, lv, de, *khung):
    """Một ý: 'a) [NB] đề' + các dòng khung thụt vào."""
    s = f"{tag}) [{lv}] {de}"
    if khung:
        s += "[[br]]" + lines(*khung)
    return s


def ys(tag, *ls):
    """Một ý của lời giải: dòng đầu sau 'a)', dòng sau thụt."""
    return f"{tag}) {ls[0]}" + ("[[br]]" + lines(*ls[1:]) if len(ls) > 1 else "")


def br(*parts):
    return "[[br]]".join(parts)


def vi(s, p):
    return rf"Theo định lí Viète, ta có $\begin{{cases}} x_1+x_2={s}\\ x_1x_2={p}\end{{cases}}$"


VI_O = vi(D, D)
CO2 = "nên phương trình có hai nghiệm phân biệt."

# ───────────────────────── LUYỆN TẬP 1 — NB (điền khuyết) ─────────────────────────
lt1 = []
lt1.append(ex(1, r"Mỗi đề sau thuộc khuôn nào của chương VI?[[br]]a) \emph{Giải phương trình $x^2-8x+15=0$.}[[br]]"
               r"b) \emph{Cho phương trình $x^2-7x+3=0$ có hai nghiệm $x_1$, $x_2$. Tính $\dfrac{1}{x_1}+\dfrac{1}{x_2}$.}",
               r"a) Đề yêu cầu giải phương trình.",
               r"Vậy đề a) thuộc khuôn giải phương trình bậc hai.",
               r"b) Đề cho phương trình có hai nghiệm rồi hỏi giá trị một biểu thức của hai nghiệm.",
               r"Vậy đề b) thuộc khuôn tổng và tích hai nghiệm."))
lt1.append(pb(1,
    br(r"Ghi \textbf{A} (giải phương trình), \textbf{B} (tổng và tích hai nghiệm) hoặc \textbf{C} (lập phương trình) vào chỗ chấm.",
       y("a", "NB", r"\emph{Giải phương trình $x^2-6x-14=0$.} \;(Cuối kì II, Phòng GD\&ĐT Ba Đình)", rf"Khuôn {D}"),
       y("b", "NB", r"\emph{Cho phương trình $x^2-3x+1=0$ có hai nghiệm $x_1$, $x_2$. Tính $x_1^2+x_2^2$.}", rf"Khuôn {D}"),
       y("c", "NB", r"\emph{Một tổ làm $300$ sản phẩm. Thực tế mỗi ngày tổ làm nhiều hơn kế hoạch $10$ sản phẩm nên xong sớm $1$ ngày. Hỏi theo kế hoạch mỗi ngày tổ làm bao nhiêu sản phẩm?}", rf"Khuôn {D}")),
    br("a) A.", "b) B.", "c) C."), "onclass", 1, "NB2"))

lt1.append(ex(2, r"Với mỗi phương trình sau nên dùng $\Delta$ hay $\Delta'$?[[br]]a) $3x^2+6x-2=0$[[br]]b) $2x^2-5x+1=0$",
               r"a) Ta có $b=6$ là số chẵn.",
               r"Vậy dùng $\Delta'$ với $b'=3$.",
               r"b) Ta có $b=-5$ là số lẻ.",
               r"Vậy dùng $\Delta$."))
lt1.append(pb(2,
    br(r"Cho biết nên dùng $\Delta$ hay $\Delta'$ với mỗi phương trình sau. Điền vào chỗ chấm.",
       r"(Gợi ý: đưa về dạng $ax^2+bx+c=0$ trước khi đọc $b$.)",
       y("a", "NB", r"$x^2-10x+9=0$", rf"Ta có $b={D}$ là số {D}", rf"Vậy dùng {D}"),
       y("b", "NB", r"$2x^2+3x-4=0$", rf"Ta có $b={D}$ là số {D}", rf"Vậy dùng {D}"),
       y("c", "NB", r"$x(x+8)=240$", rf"Đưa về dạng $ax^2+bx+c=0$, ta được {D}", rf"Ta có $b={D}$ là số {D}", rf"Vậy dùng {D}")),
    br(ys("a", r"Ta có $b=-10$ là số chẵn.", r"Vậy dùng $\Delta'$ với $b'=-5$."),
       ys("b", r"Ta có $b=3$ là số lẻ.", r"Vậy dùng $\Delta$."),
       ys("c", r"Đưa về dạng $ax^2+bx+c=0$, ta được $x^2+8x-240=0$.", r"Ta có $b=8$ là số chẵn.", r"Vậy dùng $\Delta'$ với $b'=4$.")),
    "onclass", 1, "NB3"))

lt1.append(ex(3, r"Giải phương trình $2x^2-5x+3=0$ bằng cách nhẩm nghiệm.",
               r"Ta có $a+b+c=2-5+3=0$.",
               r"Do đó phương trình có hai nghiệm $x_1=1$ và $x_2=\dfrac{c}{a}=\dfrac{3}{2}$.",
               r"Vậy phương trình có hai nghiệm $x_1=1$ và $x_2=\dfrac{3}{2}$."))
NHAM = (rf"Ta có $a+b+c={D}$ và $a-b+c={D}$", rf"Vậy {D}")
lt1.append(pb(3,
    br(r"Thử nhẩm nghiệm mỗi phương trình sau. Nhẩm được thì viết hai nghiệm, không nhẩm được thì ghi \emph{phải tính $\Delta$}.",
       y("a", "NB", r"$x^2-3x+2=0$", *NHAM),
       y("b", "NB", r"$x^2+5x+4=0$", *NHAM),
       y("c", "NB", r"$x^2+2x-6=0$", *NHAM)),
    br(ys("a", r"Ta có $a+b+c=1-3+2=0$ và $a-b+c=1+3+2=6$.", r"Vậy phương trình có hai nghiệm $x_1=1$ và $x_2=2$."),
       ys("b", r"Ta có $a+b+c=1+5+4=10$ và $a-b+c=1-5+4=0$.", r"Vậy phương trình có hai nghiệm $x_1=-1$ và $x_2=-4$."),
       ys("c", r"Ta có $a+b+c=1+2-6=-3$ và $a-b+c=1-2-6=-7$.", r"Vậy không nhẩm được, phải tính $\Delta$.")),
    "onclass", 1, "NB6"))

lt1.append(ex(4, r"Cho phương trình $x^2-6x+2=0$ có hai nghiệm $x_1$, $x_2$. Tính $x_1^2+x_2^2$.",
               r"Ta có $\Delta'=(-3)^2-1\cdot 2=7>0$ " + CO2,
               vi(6, 2),
               r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=6^2-2\cdot 2=32$.",
               r"Vậy $x_1^2+x_2^2=32$."))
lt1.append(pb(4,
    br(r"Cho phương trình $x^2-4x+1=0$ có hai nghiệm $x_1$, $x_2$. Tính giá trị các biểu thức sau. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 4).",
       r"(Gợi ý: đưa mỗi biểu thức về $x_1+x_2$ và $x_1x_2$.)",
       H + rf"Ta có $\Delta'={D}>0$ " + CO2,
       H + VI_O,
       y("a", "NB", rf"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2={D}$", rf"Vậy $x_1^2+x_2^2={D}$"),
       y("b", "NB", r"$\dfrac{1}{x_1}+\dfrac{1}{x_2}$", rf"Vì $x_1x_2={D}\ne 0$ nên $x_1\ne 0$ và $x_2\ne 0$.",
         rf"$\dfrac{{1}}{{x_1}}+\dfrac{{1}}{{x_2}}=\dfrac{{x_1+x_2}}{{x_1x_2}}={D}$", rf"Vậy $\dfrac{{1}}{{x_1}}+\dfrac{{1}}{{x_2}}={D}$"),
       y("c", "NB", rf"$(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2={D}$", rf"Vậy $(x_1-x_2)^2={D}$")),
    br(r"Ta có $\Delta'=(-2)^2-1\cdot 1=3>0$ " + CO2,
       vi(4, 1),
       ys("a", r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=4^2-2\cdot 1=14$.", r"Vậy $x_1^2+x_2^2=14$."),
       ys("b", r"Vì $x_1x_2=1\ne 0$ nên $x_1\ne 0$ và $x_2\ne 0$.", r"$\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{x_1+x_2}{x_1x_2}=\dfrac{4}{1}=4$.",
          r"Vậy $\dfrac{1}{x_1}+\dfrac{1}{x_2}=4$."),
       ys("c", r"$(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2=4^2-4\cdot 1=12$.", r"Vậy $(x_1-x_2)^2=12$.")),
    "onclass", 1, "NB4"))

lt1.append(ex(5, r"Cho $x_1$ là một nghiệm của phương trình $x^2-2x-4=0$. Viết $x_1^2$ và $x_1^3$ theo $x_1$ (hạ bậc).",
               r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-2x_1-4=0$.",
               r"Suy ra $x_1^2=2x_1+4$.",
               r"$x_1^3=x_1\cdot x_1^2=x_1(2x_1+4)=2x_1^2+4x_1$",
               r"$=2(2x_1+4)+4x_1=8x_1+8$.",
               r"Vậy $x_1^2=2x_1+4$ và $x_1^3=8x_1+8$."))
lt1.append(pb(5,
    br(r"Cho $x_1$ là một nghiệm của phương trình $x^2-5x+3=0$. Viết $x_1^2$ và $x_1^3$ theo $x_1$. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 5).",
       y("a", "NB", r"Viết $x_1^2$ theo $x_1$.", rf"Vì $x_1$ là nghiệm của phương trình nên {D}", rf"Vậy $x_1^2={D}$"),
       y("b", "NB", r"Viết $x_1^3$ theo $x_1$.", rf"$x_1^3=x_1\cdot x_1^2=x_1({D})={D}$", rf"$={D}$", rf"Vậy $x_1^3={D}$")),
    br(ys("a", r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-5x_1+3=0$.", r"Vậy $x_1^2=5x_1-3$."),
       ys("b", r"$x_1^3=x_1\cdot x_1^2=x_1(5x_1-3)=5x_1^2-3x_1$", r"$=5(5x_1-3)-3x_1=22x_1-15$.", r"Vậy $x_1^3=22x_1-15$.")),
    "onclass", 1, "NB4"))

lt1.append(pb(6,
    br(r"Tìm điều kiện xác định và chọn nghiệm của phương trình chứa ẩn ở mẫu. Điền vào chỗ chấm.",
       y("a", "NB", r"Phương trình $\dfrac{2}{x-3}+\dfrac{1}{x+4}=\dfrac{7}{(x-3)(x+4)}$",
         rf"Điều kiện xác định là $x\ne{D}$ và $x\ne{D}$"),
       y("b", "NB", r"Phương trình có điều kiện $x\ne 3$ và $x\ne -3$. Giải ra được nghiệm duy nhất $x=3$.",
         rf"Vì $x=3$ {D}\ điều kiện xác định nên {D}", rf"Vậy phương trình {D}"),
       y("c", "NB", r"Phương trình có điều kiện $x\ne 0$ và $x\ne 2$. Giải ra được nghiệm duy nhất $x=\dfrac{4}{3}$.",
         rf"Vì $x=\dfrac{{4}}{{3}}$ {D}\ điều kiện xác định nên {D}", rf"Vậy phương trình {D}")),
    br(ys("a", r"Điều kiện xác định là $x\ne 3$ và $x\ne -4$."),
       ys("b", r"Vì $x=3$ không thỏa mãn điều kiện xác định nên loại.", r"Vậy phương trình vô nghiệm."),
       ys("c", r"Vì $x=\dfrac{4}{3}$ thỏa mãn điều kiện xác định nên nhận.", r"Vậy phương trình có nghiệm $x=\dfrac{4}{3}$.")),
    "onclass", 1, "NB1"))

lt1.append(pb(7,
    br(r"Đặt ẩn kèm đơn vị và điều kiện cho mỗi bài toán lời văn. Điền vào chỗ chấm.",
       y("a", "NB", r"Tìm số áo mỗi ngày một tổ may theo kế hoạch \;(Câu III.1 đề chính thức Vào 10 Hà Nội 2026)",
         rf"Gọi số áo tổ may mỗi ngày theo kế hoạch là $x$ ({D}), điều kiện {D}"),
       y("b", "NB", r"Tìm chiều rộng một mảnh đất hình chữ nhật \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)",
         rf"Gọi chiều rộng mảnh đất là $x$ ({D}), điều kiện {D}"),
       y("c", "NB", r"Tìm độ dài quãng đường Hà Nội $-$ Hải Phòng \;(Câu III.1 đề chính thức Vào 10 Hà Nội 2025)",
         rf"Gọi độ dài quãng đường Hà Nội $-$ Hải Phòng là $x$ ({D}), điều kiện {D}")),
    br(ys("a", r"Gọi số áo tổ may mỗi ngày theo kế hoạch là $x$ (chiếc), điều kiện $x$ nguyên dương."),
       ys("b", r"Gọi chiều rộng mảnh đất là $x$ (m), điều kiện $x>0$."),
       ys("c", r"Gọi độ dài quãng đường Hà Nội $-$ Hải Phòng là $x$ (km), điều kiện $x>0$.")),
    "onclass", 1, "NB8"))

lt1.append(pb(8,
    br(r"Lập phương trình từ cụm chữ in nghiêng. Điền vào chỗ chấm.",
       y("a", "NB", r"\emph{Mỗi xe còn lại phải chở nhiều hơn dự định $1$ tấn}, biết dự định mỗi xe chở $\dfrac{60}{x}$ tấn và thực tế mỗi xe chở $\dfrac{60}{x-2}$ tấn.",
         rf"Phương trình: {D}"),
       y("b", "NB", r"\emph{Xong sớm hơn dự định $30$ phút}, biết thời gian dự định là $\dfrac{60}{x}$ giờ và thời gian thực tế là $\dfrac{63}{x+2}$ giờ.",
         rf"Đổi $30$ phút $={D}$ giờ", rf"Phương trình: {D}"),
       y("c", "NB", r"\emph{Thời gian về nhiều hơn thời gian đi $45$ phút}, biết thời gian đi là $\dfrac{s}{40}$ giờ và thời gian về là $\dfrac{s}{30}$ giờ.",
         rf"Đổi $45$ phút $={D}$ giờ", rf"Phương trình: {D}")),
    br(ys("a", r"Phương trình: $\dfrac{60}{x-2}-\dfrac{60}{x}=1$."),
       ys("b", r"Đổi $30$ phút $=\dfrac{1}{2}$ giờ.", r"Phương trình: $\dfrac{60}{x}-\dfrac{63}{x+2}=\dfrac{1}{2}$."),
       ys("c", r"Đổi $45$ phút $=\dfrac{3}{4}$ giờ.", r"Phương trình: $\dfrac{s}{30}-\dfrac{s}{40}=\dfrac{3}{4}$.")),
    "onclass", 1, "NB5"))

b9 = copy.deepcopy(old["Bài 11."])
b9.update(label="Bài 9.", dang_id="NB2")
lt1.append(b9)

# ───────────────────────── LUYỆN TẬP 2 — TH + VD (tự trình bày) ─────────────────────────
lt2 = []
lt2.append(ex(6, r"Giải phương trình $\dfrac{x}{x-2}+\dfrac{2}{x+2}=\dfrac{8}{x^2-4}$.",
               r"Ta có $x^2-4=(x-2)(x+2)$ nên điều kiện xác định là $x\ne 2$ và $x\ne -2$.",
               r"Quy đồng mẫu hai vế rồi khử mẫu, ta được $x(x+2)+2(x-2)=8$",
               r"$x^2+2x+2x-4=8$",
               r"$x^2+4x-12=0$",
               r"Ta có $\Delta'=2^2-1\cdot(-12)=16>0$ và $\sqrt{\Delta'}=4$.",
               r"$x_1=\dfrac{-2+4}{1}=2$ (loại vì không thỏa mãn điều kiện xác định).",
               r"$x_2=\dfrac{-2-4}{1}=-6$ (thỏa mãn điều kiện xác định).",
               r"Vậy phương trình có nghiệm $x=-6$."))
lt2.append(pb(10,
    r"[TH] Giải phương trình $\dfrac{x+1}{x-1}-\dfrac{1}{x+1}=\dfrac{4}{x^2-1}$.",
    br(r"Ta có $x^2-1=(x-1)(x+1)$ nên điều kiện xác định là $x\ne 1$ và $x\ne -1$.",
       r"Quy đồng mẫu hai vế rồi khử mẫu, ta được $(x+1)^2-(x-1)=4$",
       r"$x^2+2x+1-x+1=4$",
       r"$x^2+x-2=0$",
       r"Ta có $a+b+c=1+1-2=0$ nên $x_1=1$ và $x_2=\dfrac{c}{a}=-2$.",
       r"$x_1=1$ không thỏa mãn điều kiện xác định nên loại.",
       r"$x_2=-2$ thỏa mãn điều kiện xác định.",
       r"Vậy phương trình có nghiệm $x=-2$."),
    "onclass", 2, "NB1",
    hints=[r"Tìm điều kiện xác định trước, mẫu chung là $x^2-1$.",
           r"Giải xong phải đối chiếu từng nghiệm với điều kiện."],
    check={"kind": "solveset", "equation": "x**2 + x - 2 = 0", "answer": [1, -2], "symbol": "x"}))

lt2.append(ex(7, r"Cho phương trình $x^2-5x-3=0$ có hai nghiệm $x_1$, $x_2$. Tính $x_1^2x_2+x_1x_2^2$.",
               r"Ta có $ac=1\cdot(-3)=-3<0$ " + CO2,
               vi(5, -3),
               r"$x_1^2x_2+x_1x_2^2=x_1x_2(x_1+x_2)=(-3)\cdot 5=-15$.",
               r"Vậy $x_1^2x_2+x_1x_2^2=-15$."))
lt2.append(pb(11,
    br(r"Tính giá trị biểu thức của hai nghiệm $x_1$, $x_2$ của mỗi phương trình sau.",
       r"a) [TH] $x^2-8x+3=0$, tính $x_1^2+x_2^2$.",
       r"b) [TH] $x^2+3x-5=0$, tính $\dfrac{1}{x_1}+\dfrac{1}{x_2}$."),
    br(ys("a", r"Ta có $\Delta'=(-4)^2-1\cdot 3=13>0$ " + CO2, vi(8, 3),
          r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=8^2-2\cdot 3=58$.", r"Vậy $x_1^2+x_2^2=58$."),
       ys("b", r"Ta có $ac=1\cdot(-5)=-5<0$ " + CO2, vi(-3, -5),
          r"Vì $x_1x_2=-5\ne 0$ nên $x_1\ne 0$ và $x_2\ne 0$.",
          r"$\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{x_1+x_2}{x_1x_2}=\dfrac{-3}{-5}=\dfrac{3}{5}$.",
          r"Vậy $\dfrac{1}{x_1}+\dfrac{1}{x_2}=\dfrac{3}{5}$.")),
    "onclass", 2, "TH1",
    hints=[r"Trước khi dùng định lí Viète phải chỉ ra phương trình có hai nghiệm.",
           r"Đưa biểu thức về $x_1+x_2$ và $x_1x_2$."]))

lt2.append(ex(8, r"Một mảnh vườn hình chữ nhật có chu vi $34$ m và diện tích $60$ m$^2$. Tính chiều dài và chiều rộng của mảnh vườn.",
               r"Nửa chu vi mảnh vườn là $34:2=17$ (m).",
               r"Gọi chiều dài mảnh vườn là $x$ (m), điều kiện $8{,}5<x<17$.",
               r"Chiều rộng mảnh vườn là $17-x$ (m).",
               r"Vì diện tích bằng $60$ m$^2$ nên ta có phương trình $x(17-x)=60$",
               r"$x^2-17x+60=0$",
               r"Ta có $\Delta=(-17)^2-4\cdot 1\cdot 60=49>0$ và $\sqrt{\Delta}=7$.",
               r"$x_1=\dfrac{17+7}{2}=12$ (thỏa mãn điều kiện).",
               r"$x_2=\dfrac{17-7}{2}=5$ (loại vì $x>8{,}5$).",
               r"Vậy mảnh vườn có chiều dài $12$ m và chiều rộng $17-12=5$ m."))
o14 = old["Bài 14."]
b12 = copy.deepcopy(o14)
b12.update(label="Bài 12.", dang_id="TH2",
    statement=br(r"Lập phương trình và giải mỗi bài toán sau.",
       r"a) [TH] Một mảnh đất hình chữ nhật có chiều rộng ngắn hơn chiều dài $11$ m và diện tích $180$ m$^2$. Tính chiều dài và chiều rộng của mảnh đất. \;(bộ đề Vào 10, Phòng GD\&ĐT Đống Đa)",
       r"b) [TH] Một tổ may áo theo kế hoạch mỗi ngày may được số áo như nhau. Trong $3$ ngày đầu, tổ may đúng kế hoạch. Trong $7$ ngày sau, mỗi ngày tổ may nhiều hơn kế hoạch $5$ chiếc. Sau $10$ ngày tổ may được $335$ chiếc áo. Hỏi theo kế hoạch mỗi ngày tổ may bao nhiêu chiếc áo? \;(Câu III.1 đề chính thức Vào 10 Hà Nội 2026)"),
    solution=br(ys("a", r"Gọi chiều rộng mảnh đất là $x$ (m), điều kiện $x>0$.",
                   r"Chiều dài mảnh đất là $x+11$ (m).",
                   r"Vì diện tích bằng $180$ m$^2$ nên ta có phương trình $x(x+11)=180$",
                   r"$x^2+11x-180=0$",
                   r"Ta có $\Delta=11^2-4\cdot 1\cdot(-180)=841>0$ và $\sqrt{\Delta}=29$.",
                   r"$x_1=\dfrac{-11+29}{2}=9$ (thỏa mãn điều kiện).",
                   r"$x_2=\dfrac{-11-29}{2}=-20$ (loại vì $x>0$).",
                   r"Vậy mảnh đất có chiều rộng $9$ m và chiều dài $9+11=20$ m."),
                ys("b", r"Gọi số áo tổ may mỗi ngày theo kế hoạch là $x$ (chiếc), điều kiện $x$ nguyên dương.",
                   r"Trong $3$ ngày đầu tổ may được $3x$ (chiếc).",
                   r"Trong $7$ ngày sau, mỗi ngày tổ may được $x+5$ (chiếc), nên may được $7(x+5)$ (chiếc).",
                   r"Vì sau $10$ ngày tổ may được $335$ chiếc nên ta có phương trình $3x+7(x+5)=335$",
                   r"$10x+35=335$",
                   r"$x=30$ (thỏa mãn điều kiện).",
                   r"Vậy theo kế hoạch mỗi ngày tổ may $30$ chiếc áo.")),
    hints=[r"Đặt ẩn là đại lượng đề hỏi, nhớ ghi đơn vị và điều kiện.",
           r"Giải xong đối chiếu điều kiện rồi mới kết luận."])

lt2.append(b12)

lt2.append(ex(9, r"Biết phương trình $x^2+bx+6=0$ có một nghiệm $x_1=2$. Tìm nghiệm còn lại và giá trị của $b$.",
               r"Vì phương trình có nghiệm $x_1=2$ nên theo định lí Viète, ta có $\begin{cases} x_1+x_2=-b\\ x_1x_2=6\end{cases}$",
               r"Suy ra $x_2=\dfrac{6}{x_1}=\dfrac{6}{2}=3$.",
               r"$-b=x_1+x_2=2+3=5$ nên $b=-5$.",
               r"Vậy nghiệm còn lại là $x_2=3$ và $b=-5$."))
lt2.append(pb(13,
    r"[TH] Biết phương trình $x^2-8x+c=0$ có một nghiệm là $x_1=4-\sqrt5$. Tìm nghiệm còn lại và giá trị của $c$.",
    br(r"Vì phương trình có nghiệm $x_1=4-\sqrt5$ nên theo định lí Viète, ta có $\begin{cases} x_1+x_2=8\\ x_1x_2=c\end{cases}$",
       r"Suy ra $x_2=8-x_1=8-(4-\sqrt5)=4+\sqrt5$.",
       r"$c=x_1x_2=(4-\sqrt5)(4+\sqrt5)=16-5=11$.",
       r"Vậy nghiệm còn lại là $x_2=4+\sqrt5$ và $c=11$."),
    "onclass", 2, "TH1",
    hints=[r"Hệ số của $x$ đã biết nên tính được tổng hai nghiệm trước."],
    check={"kind": "solveset", "equation": "x**2 - 8*x + 11 = 0", "answer": ["4+sqrt(5)", "4-sqrt(5)"], "symbol": "x"}))

lt2.append(ex(10, r"Cho phương trình $x^2-3x-1=0$ có hai nghiệm $x_1$, $x_2$. Tính $A=x_1^2+3x_2$.",
                r"Ta có $ac=1\cdot(-1)=-1<0$ " + CO2,
                r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-3x_1-1=0$.",
                r"Suy ra $x_1^2=3x_1+1$.",
                r"$A=x_1^2+3x_2=3x_1+1+3x_2=3(x_1+x_2)+1$.",
                r"Theo định lí Viète, ta có $x_1+x_2=3$.",
                r"$A=3\cdot 3+1=10$.",
                r"Vậy $A=10$."))
o16 = old["Bài 16."]
b14 = copy.deepcopy(o16)
b14.update(label="Bài 14.",
    statement=r"[VD] Cho phương trình $x^2-4x-1=0$. Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức $K=x_1^3-17x_1+2025$.",
    solution=br(r"Ta có $ac=1\cdot(-1)=-1<0$ " + CO2,
                r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-4x_1-1=0$.",
                r"Suy ra $x_1^2=4x_1+1$.",
                r"$x_1^3=x_1\cdot x_1^2=x_1(4x_1+1)=4x_1^2+x_1$",
                r"$=4(4x_1+1)+x_1=17x_1+4$.",
                r"$K=(17x_1+4)-17x_1+2025=2029$.",
                r"Vậy $K=2029$."),
    hints=[r"Viết $x_1^2$ theo $x_1$, rồi viết tiếp $x_1^3$ theo $x_1$."])
b14.pop("quy_trinh", None)
lt2.append(b14)

o17 = old["Bài 17."]
b15 = copy.deepcopy(o17)
b15.update(label="Bài 15.",
    statement=r"[VD] Để chở hết $60$ tấn hàng, một đội xe dự định sử dụng một số xe cùng loại. Trước khi khởi hành, có hai xe được điều động đi làm việc khác, vì vậy mỗi xe còn lại phải chở nhiều hơn dự định $1$ tấn hàng. Hỏi lúc đầu đội dự định dùng bao nhiêu xe? \;(Câu III.1 đề thi thử Vào 10 lần 4, Phòng GD\&ĐT Chương Mỹ)",
    solution=br(r"Gọi số xe đội dự định dùng là $x$ (xe), điều kiện $x$ nguyên và $x>2$.",
                r"Theo dự định, mỗi xe chở $\dfrac{60}{x}$ (tấn).",
                r"Thực tế đội còn $x-2$ xe nên mỗi xe chở $\dfrac{60}{x-2}$ (tấn).",
                r"Vì mỗi xe thực tế chở nhiều hơn dự định $1$ tấn nên ta có phương trình $\dfrac{60}{x-2}-\dfrac{60}{x}=1$",
                r"$60x-60(x-2)=x(x-2)$",
                r"$x^2-2x-120=0$",
                r"Ta có $\Delta'=(-1)^2-1\cdot(-120)=121>0$ và $\sqrt{\Delta'}=11$.",
                r"$x_1=\dfrac{1+11}{1}=12$ (thỏa mãn điều kiện).",
                r"$x_2=\dfrac{1-11}{1}=-10$ (loại vì $x>2$).",
                r"Vậy lúc đầu đội dự định dùng $12$ xe."))
b15.pop("quy_trinh", None)
lt2.append(b15)

# ───────────────────────── BTVN ─────────────────────────
bt = []
bt.append(pb(16,
    br(r"Ghi \textbf{A} (giải phương trình), \textbf{B} (tổng và tích hai nghiệm) hoặc \textbf{C} (lập phương trình) vào chỗ chấm.",
       y("a", "NB", r"\emph{Giải phương trình $3x^2-7x+2=0$.}", rf"Khuôn {D}"),
       y("b", "NB", r"\emph{Cho phương trình $x^2-9x+4=0$ có hai nghiệm $x_1$, $x_2$. Tính $x_1^3+x_2^3$.}", rf"Khuôn {D}")),
    br("a) A.", "b) B."), "btvn", 1, "NB2"))
bt.append(pb(17,
    br(r"Cho biết nên dùng $\Delta$ hay $\Delta'$ với mỗi phương trình sau. Điền vào chỗ chấm.",
       y("a", "NB", r"$x^2-12x+7=0$", rf"Ta có $b={D}$ là số {D}", rf"Vậy dùng {D}"),
       y("b", "NB", r"$x(x+5)=84$", rf"Đưa về dạng $ax^2+bx+c=0$, ta được {D}", rf"Ta có $b={D}$ là số {D}", rf"Vậy dùng {D}")),
    br(ys("a", r"Ta có $b=-12$ là số chẵn.", r"Vậy dùng $\Delta'$ với $b'=-6$."),
       ys("b", r"Đưa về dạng $ax^2+bx+c=0$, ta được $x^2+5x-84=0$.", r"Ta có $b=5$ là số lẻ.", r"Vậy dùng $\Delta$.")),
    "btvn", 1, "NB3"))
bt.append(pb(18,
    br(r"Thử nhẩm nghiệm mỗi phương trình sau. Nhẩm được thì viết hai nghiệm, không nhẩm được thì ghi \emph{phải tính $\Delta$}.",
       y("a", "NB", r"$x^2-7x+6=0$", *NHAM),
       y("b", "NB", r"$3x^2+5x+2=0$", *NHAM)),
    br(ys("a", r"Ta có $a+b+c=1-7+6=0$ và $a-b+c=1+7+6=14$.", r"Vậy phương trình có hai nghiệm $x_1=1$ và $x_2=6$."),
       ys("b", r"Ta có $a+b+c=3+5+2=10$ và $a-b+c=3-5+2=0$.", r"Vậy phương trình có hai nghiệm $x_1=-1$ và $x_2=-\dfrac{2}{3}$.")),
    "btvn", 1, "NB6"))
bt.append(pb(19,
    br(r"Cho phương trình $x^2-5x+2=0$ có hai nghiệm $x_1$, $x_2$. Tính giá trị các biểu thức sau. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 4).",
       H + rf"Ta có $\Delta={D}>0$ " + CO2,
       H + VI_O,
       y("a", "NB", rf"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2={D}$", rf"Vậy $x_1^2+x_2^2={D}$"),
       y("b", "NB", rf"$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)={D}$", rf"Vậy $x_1^3+x_2^3={D}$")),
    br(r"Ta có $\Delta=(-5)^2-4\cdot 1\cdot 2=17>0$ " + CO2,
       vi(5, 2),
       ys("a", r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=5^2-2\cdot 2=21$.", r"Vậy $x_1^2+x_2^2=21$."),
       ys("b", r"$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=5^3-3\cdot 2\cdot 5=95$.", r"Vậy $x_1^3+x_2^3=95$.")),
    "btvn", 1, "NB4"))
bt.append(pb(20,
    br(r"Cho $x_1$ là một nghiệm của phương trình $x^2-3x-2=0$. Viết $x_1^2$ và $x_1^3$ theo $x_1$. Điền vào chỗ chấm (làm đủ các bước như Ví dụ 5).",
       y("a", "NB", r"Viết $x_1^2$ theo $x_1$.", rf"Vì $x_1$ là nghiệm của phương trình nên {D}", rf"Vậy $x_1^2={D}$"),
       y("b", "NB", r"Viết $x_1^3$ theo $x_1$.", rf"$x_1^3=x_1\cdot x_1^2=x_1({D})={D}$", rf"$={D}$", rf"Vậy $x_1^3={D}$")),
    br(ys("a", r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-3x_1-2=0$.", r"Vậy $x_1^2=3x_1+2$."),
       ys("b", r"$x_1^3=x_1\cdot x_1^2=x_1(3x_1+2)=3x_1^2+2x_1$", r"$=3(3x_1+2)+2x_1=11x_1+6$.", r"Vậy $x_1^3=11x_1+6$.")),
    "btvn", 1, "NB4"))
bt.append(pb(21,
    br(r"Tìm điều kiện xác định và chọn nghiệm của phương trình chứa ẩn ở mẫu. Điền vào chỗ chấm.",
       y("a", "NB", r"Phương trình $\dfrac{3}{x-4}+\dfrac{x}{x+1}=\dfrac{5}{(x-4)(x+1)}$",
         rf"Điều kiện xác định là $x\ne{D}$ và $x\ne{D}$"),
       y("b", "NB", r"Phương trình có điều kiện $x\ne 5$ và $x\ne -5$. Giải ra được $x=7$ và $x=-5$.",
         rf"Vì $x=7$ {D}\ điều kiện xác định nên {D}", rf"Vì $x=-5$ {D}\ điều kiện xác định nên {D}",
         rf"Vậy phương trình {D}")),
    br(ys("a", r"Điều kiện xác định là $x\ne 4$ và $x\ne -1$."),
       ys("b", r"Vì $x=7$ thỏa mãn điều kiện xác định nên nhận.", r"Vì $x=-5$ không thỏa mãn điều kiện xác định nên loại.",
          r"Vậy phương trình có nghiệm $x=7$.")),
    "btvn", 1, "NB1"))
bt.append(pb(22,
    br(r"Đặt ẩn kèm đơn vị và điều kiện cho mỗi bài toán. Điền vào chỗ chấm.",
       y("a", "NB", r"Tìm số xe dự định của một đội chở hàng, biết sau đó đội bớt đi hai xe.",
         rf"Gọi số xe dự định là $x$ ({D}), điều kiện {D}"),
       y("b", "NB", r"Tìm số sản phẩm một công nhân làm được trong mỗi giờ theo kế hoạch.",
         rf"Gọi số sản phẩm công nhân làm mỗi giờ theo kế hoạch là $x$ ({D}), điều kiện {D}")),
    br(ys("a", r"Gọi số xe dự định là $x$ (xe), điều kiện $x$ nguyên và $x>2$."),
       ys("b", r"Gọi số sản phẩm công nhân làm mỗi giờ theo kế hoạch là $x$ (sản phẩm), điều kiện $x$ nguyên dương.")),
    "btvn", 1, "NB8"))
bt.append(pb(23,
    br(r"Lập phương trình từ cụm chữ in nghiêng. Điền vào chỗ chấm.",
       y("a", "NB", r"\emph{Xong sớm hơn kế hoạch $1$ ngày}, biết số ngày theo kế hoạch là $\dfrac{140}{x}$ và số ngày thực tế là $\dfrac{150}{x+5}$.",
         rf"Phương trình: {D}"),
       y("b", "NB", r"\emph{Thời gian về nhiều hơn thời gian đi $30$ phút}, biết thời gian đi là $\dfrac{s}{50}$ giờ và thời gian về là $\dfrac{s}{40}$ giờ.",
         rf"Đổi $30$ phút $={D}$ giờ", rf"Phương trình: {D}")),
    br(ys("a", r"Phương trình: $\dfrac{140}{x}-\dfrac{150}{x+5}=1$."),
       ys("b", r"Đổi $30$ phút $=\dfrac{1}{2}$ giờ.", r"Phương trình: $\dfrac{s}{40}-\dfrac{s}{50}=\dfrac{1}{2}$.")),
    "btvn", 1, "NB5"))

o29 = old["Bài 29."]
bt.append(pb(24,
    br(r"Giải các phương trình sau.",
       r"a) [TH] $\dfrac{6}{x-2}+\dfrac{2}{x}=\dfrac{5}{x-2}$ \;(Giữa kì I, THCS Thái Thịnh)",
       r"b) [TH] $\dfrac{x}{x+2}+\dfrac{3}{x-2}=\dfrac{12}{x^2-4}$"),
    br(ys("a", r"Điều kiện xác định là $x\ne 0$ và $x\ne 2$.",
          r"Quy đồng mẫu hai vế rồi khử mẫu, ta được $6x+2(x-2)=5x$",
          r"$8x-4=5x$",
          r"$3x=4$",
          r"$x=\dfrac{4}{3}$ (thỏa mãn điều kiện xác định).",
          r"Vậy phương trình có nghiệm $x=\dfrac{4}{3}$."),
       ys("b", r"Ta có $x^2-4=(x+2)(x-2)$ nên điều kiện xác định là $x\ne 2$ và $x\ne -2$.",
          r"Quy đồng mẫu hai vế rồi khử mẫu, ta được $x(x-2)+3(x+2)=12$",
          r"$x^2-2x+3x+6=12$",
          r"$x^2+x-6=0$",
          r"Ta có $\Delta=1^2-4\cdot 1\cdot(-6)=25>0$ và $\sqrt{\Delta}=5$.",
          r"$x_1=\dfrac{-1+5}{2}=2$ (loại vì không thỏa mãn điều kiện xác định).",
          r"$x_2=\dfrac{-1-5}{2}=-3$ (thỏa mãn điều kiện xác định).",
          r"Vậy phương trình có nghiệm $x=-3$.")),
    "btvn", 2, "NB1",
    hints=[r"Tìm điều kiện xác định trước khi khử mẫu.", r"Đối chiếu từng nghiệm với điều kiện rồi mới kết luận."]))
bt.append(pb(25,
    br(r"Tính giá trị biểu thức của hai nghiệm $x_1$, $x_2$ của mỗi phương trình sau.",
       r"a) [TH] $x^2-7x+3=0$, tính $x_1^3+x_2^3$.",
       r"b) [TH] $2x^2-x-5=0$, tính $x_1^2+x_2^2$. \;(Cuối kì II, Phòng GD\&ĐT Ba Đình)"),
    br(ys("a", r"Ta có $\Delta=(-7)^2-4\cdot 1\cdot 3=37>0$ " + CO2, vi(7, 3),
          r"$x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)=7^3-3\cdot 3\cdot 7=280$.", r"Vậy $x_1^3+x_2^3=280$."),
       ys("b", r"Ta có $ac=2\cdot(-5)=-10<0$ " + CO2, vi(r"\dfrac{1}{2}", r"-\dfrac{5}{2}"),
          r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2=\dfrac{1}{4}+5=\dfrac{21}{4}$.", r"Vậy $x_1^2+x_2^2=\dfrac{21}{4}$.")),
    "btvn", 2, "TH1",
    hints=[r"Chỉ ra phương trình có hai nghiệm trước khi dùng định lí Viète.", r"Đưa biểu thức về $x_1+x_2$ và $x_1x_2$."]))
bt.append(pb(26,
    br(r"Lập phương trình và giải mỗi bài toán sau.",
       r"a) [TH] Một mảnh vườn hình chữ nhật có chiều dài hơn chiều rộng $4$ m và diện tích $96$ m$^2$. Tính chiều dài và chiều rộng của mảnh vườn.",
       r"b) [TH] Một ô tô đi từ Hà Nội đến Hải Phòng với vận tốc $60$ km/h. Khi về, ô tô đi với vận tốc $40$ km/h nên thời gian đi ít hơn thời gian về $1$ giờ. Tính độ dài quãng đường Hà Nội $-$ Hải Phòng. \;(Câu III.1 đề chính thức Vào 10 Hà Nội 2025)"),
    br(ys("a", r"Gọi chiều rộng mảnh vườn là $x$ (m), điều kiện $x>0$.",
          r"Chiều dài mảnh vườn là $x+4$ (m).",
          r"Vì diện tích bằng $96$ m$^2$ nên ta có phương trình $x(x+4)=96$",
          r"$x^2+4x-96=0$",
          r"Ta có $\Delta'=2^2-1\cdot(-96)=100>0$ và $\sqrt{\Delta'}=10$.",
          r"$x_1=\dfrac{-2+10}{1}=8$ (thỏa mãn điều kiện).",
          r"$x_2=\dfrac{-2-10}{1}=-12$ (loại vì $x>0$).",
          r"Vậy mảnh vườn có chiều rộng $8$ m và chiều dài $8+4=12$ m."),
       ys("b", r"Gọi độ dài quãng đường Hà Nội $-$ Hải Phòng là $x$ (km), điều kiện $x>0$.",
          r"Thời gian đi là $\dfrac{x}{60}$ (giờ).",
          r"Thời gian về là $\dfrac{x}{40}$ (giờ).",
          r"Vì thời gian đi ít hơn thời gian về $1$ giờ nên ta có phương trình $\dfrac{x}{40}-\dfrac{x}{60}=1$",
          r"$3x-2x=120$",
          r"$x=120$ (thỏa mãn điều kiện).",
          r"Vậy quãng đường Hà Nội $-$ Hải Phòng dài $120$ km.")),
    "btvn", 2, "TH2",
    hints=[r"Đặt ẩn là đại lượng đề hỏi, ghi đơn vị và điều kiện.", r"Giải xong đối chiếu điều kiện rồi mới kết luận."],
    check={"kind": "solveset", "equation": "x**2 + 4*x - 96 = 0", "answer": [8, -12], "symbol": "x"}))
bt.append(pb(27,
    br(r"Tìm nghiệm còn lại của phương trình và giá trị của hệ số còn thiếu.",
       r"a) [TH] Biết phương trình $x^2+bx-12=0$ có một nghiệm là $x_1=-3$.",
       r"b) [TH] Biết phương trình $x^2-2x+c=0$ có một nghiệm là $x_1=1+\sqrt3$."),
    br(ys("a", r"Vì phương trình có nghiệm $x_1=-3$ nên theo định lí Viète, ta có $\begin{cases} x_1+x_2=-b\\ x_1x_2=-12\end{cases}$",
          r"Suy ra $x_2=\dfrac{-12}{x_1}=\dfrac{-12}{-3}=4$.",
          r"$-b=x_1+x_2=-3+4=1$ nên $b=-1$.",
          r"Vậy nghiệm còn lại là $x_2=4$ và $b=-1$."),
       ys("b", r"Vì phương trình có nghiệm $x_1=1+\sqrt3$ nên theo định lí Viète, ta có $\begin{cases} x_1+x_2=2\\ x_1x_2=c\end{cases}$",
          r"Suy ra $x_2=2-x_1=2-(1+\sqrt3)=1-\sqrt3$.",
          r"$c=x_1x_2=(1+\sqrt3)(1-\sqrt3)=1-3=-2$.",
          r"Vậy nghiệm còn lại là $x_2=1-\sqrt3$ và $c=-2$.")),
    "btvn", 2, "TH1",
    hints=[r"Hệ số nào đã biết thì dùng hệ thức Viète chứa hệ số đó trước."],
    check={"kind": "solveset", "equation": "x**2 - 2*x - 2 = 0", "answer": ["1+sqrt(3)", "1-sqrt(3)"], "symbol": "x"}))

o33 = old["Bài 33."]
b28 = copy.deepcopy(o33)
b28.update(label="Bài 28.",
    statement=r"[VD] Cho phương trình $x^2-3x-1=0$. Gọi $x_1$ là một nghiệm của phương trình. Tính giá trị của biểu thức $H=x_1^3-10x_1+1992$. \;(Câu III.3 đề thi thử Vào 10 lần 3, Phòng GD\&ĐT Ứng Hòa)",
    solution=br(r"Ta có $ac=1\cdot(-1)=-1<0$ " + CO2,
                r"Vì $x_1$ là nghiệm của phương trình nên $x_1^2-3x_1-1=0$.",
                r"Suy ra $x_1^2=3x_1+1$.",
                r"$x_1^3=x_1\cdot x_1^2=x_1(3x_1+1)=3x_1^2+x_1$",
                r"$=3(3x_1+1)+x_1=10x_1+3$.",
                r"$H=(10x_1+3)-10x_1+1992=1995$.",
                r"Vậy $H=1995$."),
    hints=[r"Viết $x_1^3$ theo $x_1$ như Bài 14."])
bt.append(b28)

o34 = old["Bài 34."]
b29 = copy.deepcopy(o34)
b29.update(label="Bài 29.",
    statement=r"[VD] Hằng ngày bạn Nam đi học trên quãng đường $12$ km bằng xe máy điện với vận tốc không đổi. Một hôm, $3$ km đầu Nam đi với vận tốc như thường ngày, sau đó dừng $3$ phút để bơm xe. Để đến trường đúng giờ, Nam phải tăng vận tốc thêm $6$ km/h trên quãng đường còn lại. Tính vận tốc xe của Nam khi tăng tốc và cho biết Nam có vượt giới hạn $40$ km/h không. \;(Câu III.1 đề thi thử Vào 10, THCS Tự Lập)",
    solution=br(r"Gọi vận tốc thường ngày của Nam là $x$ (km/h), điều kiện $x>0$.",
                r"Thời gian đi thường ngày là $\dfrac{12}{x}$ (giờ).",
                r"Hôm đó, $3$ km đầu Nam đi hết $\dfrac{3}{x}$ (giờ).",
                r"Thời gian dừng bơm xe là $3$ phút $=\dfrac{1}{20}$ (giờ).",
                r"$9$ km còn lại Nam đi hết $\dfrac{9}{x+6}$ (giờ).",
                r"Vì Nam đến trường đúng giờ nên ta có phương trình $\dfrac{3}{x}+\dfrac{1}{20}+\dfrac{9}{x+6}=\dfrac{12}{x}$",
                r"$\dfrac{9}{x}-\dfrac{9}{x+6}=\dfrac{1}{20}$",
                r"$180(x+6)-180x=x(x+6)$",
                r"$x^2+6x-1080=0$",
                r"Ta có $\Delta'=3^2-1\cdot(-1080)=1089>0$ và $\sqrt{\Delta'}=33$.",
                r"$x_1=\dfrac{-3+33}{1}=30$ (thỏa mãn điều kiện).",
                r"$x_2=\dfrac{-3-33}{1}=-36$ (loại vì $x>0$).",
                r"Vận tốc của Nam khi tăng tốc là $30+6=36$ (km/h).",
                r"Vì $36<40$ nên Nam không vượt giới hạn tốc độ.",
                r"Vậy vận tốc của Nam khi tăng tốc là $36$ km/h và Nam không vượt giới hạn $40$ km/h."),
    check={"kind": "solveset", "equation": "x**2 + 6*x - 1080 = 0", "answer": [30, -36], "symbol": "x"})
bt.append(b29)

# ───────────────────────── ghép lại ─────────────────────────
st = d["stages"]
# Chặng 1, 2: bỏ văn nói "kiểm"
for s in st[:2]:
    for b in s["blocks"]:
        if "text" in b:
            b["text"] = (b["text"].replace(r"kiểm $\Delta \ge 0$ (hoặc $ac<0$)", r"xét $\Delta \ge 0$ (hoặc $ac<0$)")
                         .replace(r"chưa kiểm $\Delta \ge 0$", r"chưa xét $\Delta \ge 0$ hoặc $ac<0$"))
st[2]["blocks"] = lt1
st[2]["teacher_note"] = (r"Luyện 48 phút, nhịp nhanh vì là buổi ôn. Bài 1 chữa miệng trong 2 phút. "
                         r"Bài 4 và Bài 5 điền đủ các bước như Ví dụ 4, Ví dụ 5 (xét $\Delta$ hoặc $ac$ trước khi dùng định lí Viète). "
                         r"Bài 9 là bài về \emph{cách ăn điểm}, không phải về toán, đừng bỏ qua.")
st[3]["blocks"] = lt2
st[3]["teacher_note"] = (r"Luyện 48 phút. Bài 14 và Bài 15 là hai khuôn Câu III.3 và Câu III.1 của đề Vào 10. "
                         r"Dành 20 phút cuối cho hai bài này, chấm chéo theo thang điểm để HS thấy mỗi câu trình bày đáng $0{,}25$ điểm.")
refl = st[4]["blocks"]
keep = [b for b in refl if b.get("type") != "problem"]
st[4]["blocks"] = keep + bt
st[4]["teacher_note"] = (r"Sơ đồ tư duy tổng kết cả chương. HS mang về ôn cho bài kiểm tra một tiết. "
                         r"BTVN 14 bài (Bài 16 đến Bài 29) in thành phiếu riêng, chính là đề cương ôn tập chương VI. Nhắc HS làm hết trước hôm kiểm tra.")

out = {}
for k, v in d.items():
    out[k] = v
    if k == "so_ca":
        out["btvn_phieu_rieng"] = True
json.dump(out, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(P, "a", encoding="utf-8").write("\n")
print("ok", sum(1 for s in st for b in s["blocks"] if b.get("type") == "problem"), "bài")
