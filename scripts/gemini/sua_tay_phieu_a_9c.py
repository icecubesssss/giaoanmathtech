#!/usr/bin/env python3
"""Sửa tay phiếu A ch.VI 9C sau khi ráp Gemini (13/11/2026). Idempotent — chạy lại không hỏng.

    python3 scripts/gemini/sua_tay_phieu_a_9c.py [--ghi]

1. Khung NB ("hoàn thành bài giải"): chuỗi \\ldots → [[blank:…]] (cổng mật độ ô chỉ đếm [[blank]]/[[fill]],
   phiếu D dùng y vậy).
2. Ô [[fill:…]] bọc $ (math lồng math): tách — $lhs=rhs$ → $lhs=[[fill:rhs]]$, chữ giữ in sẵn.
3. Ví dụ: dòng nghiệm "=…=N$" → "=[[fill:N]]$" (nghiệm cũng là chỗ điền, không in sẵn trên câu Vậy).
4. Ca riêng: Ví dụ 5b, Ví dụ 8 (b' lộ số ở dòng dưới), "nhận/loại", câu dẫn Ví dụ 5 (giống Bài 18).
5. Hints Bài 7, Bài 8 hỏi kiểu Polya, không gọi tên công thức.
6. Thêm Bài 7 d), Bài 8 c) (TH 28% → ~35% giờ trên lớp). Nghiệm kiểm SymPy ở so_do_phieu_a_9c.py.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_sua_phieu_a_9c import SEED  # noqa: E402

FILL = re.compile(r"\[\[fill:((?:[^\[\]]|\[\[[^\]]*\]\])*)\]\]")
H = r"\hspace*{1.4em}"


def tach_fill(m):
    noi = m.group(1)
    if "$" not in noi:
        return m.group(0)

    def seg(mm):
        s = mm.group(1)
        if "=" in s:
            i = s.rfind("=")
            return f"${s[:i + 1]}[[fill:{s[i + 1:]}]]$"
        return f"$[[fill:{s}]]$"
    return re.sub(r"\$([^$]+)\$", seg, noi)


def blank(m):
    n = m.group(0).count(r"\ldots")
    return "[[blank:1.6cm]]" if n <= 2 else "[[blank:6cm]]"


THAY = [
    # Ví dụ 5
    (r"\textbf{Ví dụ 5.} Tính $\Delta$ rồi giải các phương trình sau:",
     r"\textbf{Ví dụ 5.} Mỗi phương trình sau có mấy nghiệm? Dùng biệt thức $\Delta$ để trả lời và tìm nghiệm (nếu có)."),
    (r"Vì $\Delta<0$ nên phương trình vô nghiệm.[[br]]" + H + r"Vậy [[fill:phương trình vô nghiệm]].",
     r"Vì $\Delta[[fill:<]]0$ nên phương trình vô nghiệm.[[br]]" + H + r"Vậy phương trình đã cho [[fill:vô nghiệm]]."),
    (r"Vì $\Delta[[fill:<]]0$ nên phương trình [[fill:vô nghiệm]].[[br]]" + H + r"Vậy phương trình đã cho vô nghiệm.",
     r"Vì $\Delta[[fill:<]]0$ nên phương trình vô nghiệm.[[br]]" + H + r"Vậy phương trình đã cho [[fill:vô nghiệm]]."),
    # Ví dụ 3: thêm ô (mật độ ≥ 0,6 ô/dòng)
    (r"$\Leftrightarrow x=3$ hoặc $x=-3$.", r"$\Leftrightarrow x=[[fill:3]]$ hoặc $x=[[fill:-3]]$."),
    (r"$x^2+4=0 \Leftrightarrow x^2=-4$.", r"$x^2+4=0 \Leftrightarrow x^2=[[fill:-4]]$."),
    (r"mà $-4<0$ nên phương trình vô nghiệm.[[br]]" + H + r"Vậy [[fill:phương trình vô nghiệm]].",
     r"mà $-4<0$ nên phương trình [[fill:vô nghiệm]].[[br]]" + H + r"Vậy phương trình đã cho vô nghiệm."),
    (r"mà $-4<0$ nên phương trình [[fill:vô nghiệm]].[[br]]" + H + r"Vậy phương trình đã cho vô nghiệm.",
     r"mà $-4[[fill:<]]0$ nên phương trình vô nghiệm.[[br]]" + H + r"Vậy phương trình đã cho [[fill:vô nghiệm]]."),
    (r"$\Delta=(-6)^2-4\cdot 9\cdot 1=36-36=0$", r"$\Delta=(-6)^2-4\cdot 9\cdot 1=36-36=[[fill:0]]$"),
    (r"là $30+6=36$ (km/h)", r"là $30+6=[[fill:36]]$ (km/h)"),
    (r"Vì $36<40$ nên", r"Vì $36[[fill:<]]40$ nên"),
    (r"Số tự nhiên chẵn liền sau là $x+2$.", r"Số tự nhiên chẵn liền sau là $[[fill:x+2]]$."),
    (r"Vì $\Delta=0$ nên phương trình có nghiệm kép", r"Vì $\Delta=[[fill:0]]$ nên phương trình có nghiệm kép"),
    (r"=-1+13=12$", r"=-1+[[fill:13]]=12$"),
    (r"Số chẵn thứ hai là $12+2=14$.", r"Số chẵn thứ hai là $12+2=[[fill:14]]$."),
    # Ví dụ 8: b' lộ ở dòng Δ'
    (r"$a=1$, $b'=[[fill:3]]$, $c=-1080$", r"$a=1$, $b'=3$, $c=-1080$"),
    (r"[[fill:loại $x_2=-36$, nhận $x=30$]]", r"[[fill:loại]] $x_2=-36$, [[fill:nhận]] $x=30$"),
    (r"[[fill:vận tốc của Nam hôm tăng tốc là $36$ km/h và Nam không vượt quá $40$ km/h]]",
     r"vận tốc của Nam hôm tăng tốc là $[[fill:36]]$ km/h và Nam [[fill:không vượt quá]] $40$ km/h"),
    # Ví dụ 9
    (r"[[fill:nhận $x=12$, loại $x=-14$]]", r"[[fill:nhận]] $x=12$, [[fill:loại]] $x=-14$"),
]

HINTS = {
    "Bài 9.": ["Hệ số $b$ của phương trình là số chẵn hay số lẻ?",
               "Số xe phải thỏa điều kiện nào? Nghiệm nào của phương trình thỏa điều kiện đó?"],
    "Bài 7.": ["Các hệ số $a$, $b$, $c$ của mỗi phương trình là những số nào?",
               "Hệ số $b$ là số chẵn hay số lẻ? Điều đó giúp tính gọn hơn ở bước nào?"],
    "Bài 8.": ["Phương trình đã có dạng $ax^2+bx+c=0$ chưa? Cần làm gì với hai vế trước khi tính $\\Delta$?",
               "Sau khi thu gọn, hệ số $b$ là số chẵn hay số lẻ?"],
}

THEM = {
    "Bài 7.": (
        r"[[br]]d) [TH] $3x^2+5x-2=0$",
        r"[[br]]d) Ta có $a=3$, $b=5$, $c=-2$.[[br]]" + H
        + r"$\Delta=b^2-4ac=5^2-4\cdot 3\cdot (-2)=25+24=49>0$.[[br]]" + H
        + r"Vì $\Delta>0$ nên phương trình có hai nghiệm phân biệt[[br]]" + H
        + r"$x_1=\dfrac{-b+\sqrt{\Delta}}{2a}=\dfrac{-5+7}{6}=\dfrac{1}{3}$ và "
          r"$x_2=\dfrac{-b-\sqrt{\Delta}}{2a}=\dfrac{-5-7}{6}=-2$.[[br]]" + H
        + r"Vậy phương trình có hai nghiệm $x_1=\dfrac{1}{3}$ và $x_2=-2$."),
    "Bài 8.": (
        r"[[br]]c) [TH] $(x-3)(x+1)=2x+9$",
        r"[[br]]c) $(x-3)(x+1)=2x+9$[[br]]" + H + r"$\Leftrightarrow x^2-2x-3=2x+9$[[br]]" + H
        + r"$\Leftrightarrow x^2-4x-12=0$.[[br]]" + H + r"Ta có $a=1$, $b'=-2$, $c=-12$.[[br]]" + H
        + r"$\Delta'=b'^2-ac=(-2)^2-1\cdot (-12)=4+12=16>0$.[[br]]" + H
        + r"Vì $\Delta'>0$ nên phương trình có hai nghiệm phân biệt[[br]]" + H
        + r"$x_1=\dfrac{-b'+\sqrt{\Delta'}}{a}=\dfrac{2+4}{1}=6$ và $x_2=\dfrac{-b'-\sqrt{\Delta'}}{a}=\dfrac{2-4}{1}=-2$.[[br]]"
        + H + r"Vậy phương trình có hai nghiệm $x_1=6$ và $x_2=-2$."),
}


def main():
    p = REPO / SEED
    f = json.loads(p.read_text())
    n = 0
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                st = b["statement"]
                if "hoàn thành bài giải" in st:
                    st2 = re.sub(r"(?:\\ldots)+", blank, st)
                    n += st2 != st
                    b["statement"] = st2
                lb = b.get("label")
                if lb in HINTS:
                    b["hints"] = HINTS[lb]
                if lb in THEM and THEM[lb][0] not in b["statement"]:
                    b["statement"] += THEM[lb][0]
                    b["solution"] += THEM[lb][1]
                    n += 1
            if b.get("type") == "para" and b.get("text", "").startswith(r"\textbf{Đích của buổi học:}"):
                b["text"] = re.sub(r"\.\s+(?=Mạch)", ".[[br]]", b["text"])
            if b.get("type") == "noted" and b.get("variant") == "example":
                t = b["text"]
                for cu, moi in THAY:
                    t = t.replace(cu, moi)
                t = FILL.sub(tach_fill, t)
                # nghiệm cuối dòng x_1=…=N$ và x_2=…=M$ (chưa có ô)
                if "Ví dụ 8." not in t and "Ví dụ 9." not in t:
                    t = re.sub(r"(\$x_[12]=[^$]*?=)(-?(?:\\dfrac\{\d+\}\{\d+\}|\d+))\$",
                               lambda m: m.group(0) if "[[fill" in m.group(0) else f"{m.group(1)}[[fill:{m.group(2)}]]$", t)
                else:   # VD8, VD9: nghiệm in sẵn (dòng dưới dùng lại), ô ở nhận/loại + Vậy
                    t = re.sub(r"=\[\[fill:(-?\d+)\]\]\$", r"=\1$", t)
                n += t != b["text"]
                b["text"] = t
    print("đổi", n, "khối")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
