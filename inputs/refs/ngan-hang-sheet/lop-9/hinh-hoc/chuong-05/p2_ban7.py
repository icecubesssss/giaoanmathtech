# Phiếu 2 ch.V 9C — lượt 7 (04/11/2026). Thầy: "cả ví dụ GV cũng cần hướng dẫn HS vẽ nên chắc là cũng
# làm to cái VD ra rồi cho HS vẽ cùng GV luôn nhé".
# Ví dụ 1, 2: hình nền TO (template: \figbelow[5cm]{0.5} khi có tikz_gv), Sổ tay GV in hình đầy đủ.
# Chạy SAU p2_ban6.py: python3 p2v7.py <phiếu lượt 6> <out>
import json, math, re, sys
sys.path.insert(0, ".")
from scripts.tikz_geo import Fig, polar, foot

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
S = {s["kind"]: s for s in d["stages"]}


def khung(tikz):
    xy = [(float(a), float(b)) for a, b in re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)", tikz)]
    xs, ys = [p[0] for p in xy], [p[1] for p in xy]
    return f"  \\path ({min(xs) - 0.15:.4f},{min(ys) - 0.15:.4f}) rectangle ({max(xs) + 0.15:.4f},{max(ys) + 0.15:.4f});"


def nen(f, full):
    return f.tikz().replace("\\end{tikzpicture}", khung(full) + "\n\\end{tikzpicture}")


# Ví dụ 1 — tam giác nhọn ABC, hai đường cao BE, CF (bỏ điểm M thừa của lời giải trung tuyến cũ)
A, B, C = (0.9, 2.3), (0.0, 0.0), (3.2, 0.0)
E, F = foot(B, A, C), foot(C, A, B)
g = Fig()
for n, p in [("A", A), ("B", B), ("C", C), ("E", E), ("F", F)]:
    g.pt(n, p)
g.poly("A", "B", "C"); g.seg("B", "E"); g.seg("C", "F")
g.right("E", "B", "C"); g.right("F", "C", "B")
full1 = g.tikz()
n1 = Fig()
for n, p in [("A", A), ("B", B), ("C", C)]:
    n1.pt(n, p)
n1.poly("A", "B", "C")

# Ví dụ 2 — dây AB dựng đứng bên phải (40°, −40°): OH nằm ngang, C ở NGANG bên phải đường tròn
# (Thầy 04/11: "để C ngang sang bên tay phải … gọn được") — hình chỉ cao bằng đường tròn.
R = 1.5
O = (0.0, 0.0); A2, B2 = polar(40, R), polar(-40, R)
H2 = (A2[0], 0.0); C2 = (R / math.cos(math.radians(40)), 0.0)
g2 = Fig(); g2.circle(O, R)
for n, p in [("O", O), ("A", A2), ("B", B2), ("C", C2), ("H", H2)]:
    g2.pt(n, p)
g2.seg("A", "B"); g2.seg("O", "C"); g2.seg("O", "A"); g2.seg("O", "B"); g2.seg("C", "A"); g2.seg("C", "B")
g2.right("H", "O", "B")
full2 = g2.tikz()
n2 = Fig(); n2.circle(O, R)
for n, p in [("O", O), ("A", A2), ("B", B2)]:
    n2.pt(n, p)
n2.seg("A", "B")

VE = "Vẽ tiếp vào Hình {n} các yếu tố còn thiếu theo đề."
for b in S["practice1"]["blocks"]:
    if b.get("variant") != "example":
        continue
    so = re.search(r"\(Hình (\d+)\)", b["text"]).group(1)
    if "Ví dụ 1." in b["text"]:
        b["figure"].update(tikz=nen(n1, full1), tikz_gv=full1)
        b["text"] = b["text"].replace(f"(Hình {so}). ", f"(Hình {so}). " + VE.format(n=so) + " ", 1)
    elif "Ví dụ 2." in b["text"]:
        b["figure"].update(tikz=nen(n2, full2), tikz_gv=full2)
        b["text"] = b["text"].replace(f"(Hình {so}). ", f"(Hình {so}). " + VE.format(n=so) + " ", 1)
    assert "Vẽ tiếp vào Hình" in b["text"], b["text"][:80]

S["practice1"]["teacher_note"] = (
    "Hai ví dụ: GV vẽ trên bảng, HS vẽ cùng vào hình nền trên phiếu (Ví dụ 1: hai đường cao và kí hiệu góc vuông; "
    "Ví dụ 2: đường thẳng qua $O$ vuông góc với $AB$, tiếp tuyến tại $A$, điểm $C$, đoạn $CB$) — thêm khoảng 5 phút. "
    + S["practice1"].get("teacher_note", ""))
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("ok")
