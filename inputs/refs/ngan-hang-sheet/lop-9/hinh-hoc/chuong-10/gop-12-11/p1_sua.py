#!/usr/bin/env python3
"""Sửa phiếu A gộp ch.X 9C sau khi ráp kết quả Gemini (12/11/2026). Chạy từ gốc repo, chạy MỘT lần
ngay sau scripts/gemini/lap_gop_phieu_ch10_9c.py.
1) Thứ tự theo dan_dat_gate: trắc nghiệm → điền khuyết → tự trình bày (LT1 Mạch 3, BTVN).
2) Hai chỗ trùng đề: BTVN 2 (r=12,h=25 = Ví dụ 2) → r=6,h=15; BTVN 7 (ly 2,5/10 = đề đích ý a) → r=4, nước 12.
3) Ví dụ có ô [[fill:]] (luật ví dụ điền khuyết); hints cho Bài 8 / BTVN 8; dời nhãn hình Bài 2, 3.
4) Đánh số lại Bài/BTVN/Hình."""
import json, re
from pathlib import Path
P = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/phieu-a-hinh-tru-hinh-non-hinh-cau.json")
d = json.loads(P.read_text())
S = {s["kind"]: s for s in d["stages"]}

def by_label(stage, lab):
    return next(b for b in stage["blocks"] if b.get("label") == lab)

# ---- 1) thứ tự
lt1 = S["practice1"]["blocks"]
i3 = next(i for i, b in enumerate(lt1) if b.get("type") == "para" and b.get("text", "").startswith("Mạch 3"))
m3 = {b["label"]: b for b in lt1[i3 + 1:]}
lt1[i3 + 1:] = [m3["Bài 5."], m3["Bài 7."], m3["Bài 4."], m3["Bài 6."]]
bt = S["reflection"]["blocks"]
mm = [b for b in bt if b["type"] != "problem"]
pb = {b["label"]: b for b in bt if b["type"] == "problem"}
bt[:] = mm + [pb[f"BTVN {n}."] for n in (3, 5, 6, 1, 7, 2, 4, 8, 9)]

# ---- 2) trùng đề
b = pb["BTVN 2."]
b["statement"] = b["statement"].replace("$r = 12$ cm và chiều cao $h = 25$ cm", "$r = 6$ cm và chiều cao $h = 15$ cm")
b["solution"] = ("a) Diện tích xung quanh của hình trụ là[[br]]$S_{xq} = 2\\pi r h \\approx 2\\cdot 3{,}14\\cdot 6\\cdot 15 = 565{,}2$ (cm$^2$).[[br]]"
                 "Vậy diện tích xung quanh của hình trụ khoảng $565{,}2$ cm$^2$.[[br]]b) Thể tích của hình trụ là[[br]]"
                 "$V = \\pi r^2 h \\approx 3{,}14\\cdot 6^2\\cdot 15 = 1695{,}6$ (cm$^3$).[[br]]Vậy thể tích của hình trụ khoảng $1695{,}6$ cm$^3$.")
b = pb["BTVN 7."]
b["statement"] = b["statement"].replace("bán kính đáy $2{,}5$ cm và chiều cao cột nước là $10$ cm", "bán kính đáy $4$ cm và chiều cao cột nước là $12$ cm")
b["solution"] = ("Thể tích nước trong ly là:[[br]]$V = \\pi r^2 h \\approx 3{,}14\\cdot 4^2\\cdot 12 = 602{,}88$ (cm$^3$).[[br]]"
                 "Vậy thể tích nước trong ly khoảng $602{,}88$ cm$^3$.[[br]](Các chỗ cần điền lần lượt là: $\\pi r^2 h$; $3{,}14$; $4$; $12$; $602{,}88$; cm$^3$; $602{,}88$.)")
b = pb["BTVN 3."]
b["statement"] = "[NB] Hình nón có bán kính đáy $r = 4$ cm và chiều cao $h = 3$ cm. Đường sinh $l$ của hình nón bằng"

# ---- 3) ví dụ điền cùng GV
def ex(stage, n):
    return next(x for x in stage["blocks"] if x.get("variant") == "example" and x["text"].startswith(f"\\textbf{{Ví dụ {n}.}}"))
rep = [
  (S["practice1"], 1, [("$r = 5 : 2 = 2{,}5$ (cm)", "$r = 5 : 2 = [[fill:2{,}5]]$ (cm)"),
                        ("Vậy phải thay $r = 2{,}5$ cm vào công thức, không được thay $5$ cm.", "Vậy phải thay $r = [[fill:2{,}5]]$ cm vào công thức, không được thay $5$ cm."),
                        ("$r = 0{,}4 : 2 = 0{,}2$ (m)", "$r = 0{,}4 : 2 = [[fill:0{,}2]]$ (m)"),
                        ("Vậy phải thay $r = 0{,}2$ m vào công thức.", "Vậy phải thay $r = [[fill:0{,}2]]$ m vào công thức.")]),
  (S["practice2"], 2, [("$S_{xq} = 2\\pi rh \\approx", "$S_{xq} = [[fill:2\\pi rh]] \\approx"),
                        ("$V = \\pi r^2h \\approx", "$V = [[fill:\\pi r^2h]] \\approx"),
                        ("Vậy $S_{xq} \\approx 1884$ cm$^2$ và $V \\approx 11\\,304$ cm$^3$.", "Vậy $S_{xq} \\approx [[fill:1884]]$ cm$^2$ và $V \\approx [[fill:11\\,304]]$ cm$^3$.")]),
  (S["practice2"], 3, [("$V_{\\text{nặng}} = \\dfrac{4}{3}\\pi R^3", "$V_{\\text{nặng}} = [[fill:\\dfrac{4}{3}\\pi R^3]]"),
                        ("thể tích lượng nước tràn ra ngoài đúng bằng thể tích quả nặng", "thể tích lượng nước tràn ra ngoài đúng bằng [[fill:thể tích quả nặng]]"),
                        ("Vậy trong cốc còn lại khoảng $249{,}11$ cm$^3$ nước.", "Vậy trong cốc còn lại khoảng $[[fill:249{,}11]]$ cm$^3$ nước.")]),
]
for st, n, pairs in rep:
    x = ex(st, n)
    for a, z in pairs:
        assert a in x["text"], (n, a)
        x["text"] = x["text"].replace(a, z, 1)

by_label(S["practice2"], "Bài 8.")["hints"] = ["Đề cho ĐƯỜNG KÍNH: chia đôi trước khi thay vào công thức thể tích.", "Kết quả ra m$^3$; $1$ m$^3 = 1000$ lít."]
pb["BTVN 8."]["hints"] = ["Đề cho ĐƯỜNG KÍNH: chia đôi trước khi thay số.", "Đơn vị dm$^3$ đổi ra lít theo $1$ dm$^3 = 1$ lít."]

# nhãn hình
f = m3_b2 = by_label(S["practice1"], "Bài 2.")["figure"]
f["tikz"] = f["tikz"].replace("\\node[right, font=\\scriptsize] at (0.12,1) {$10$ cm};", "\\node[right, font=\\scriptsize] at (1.02,1) {$10$ cm};")
f = by_label(S["practice1"], "Bài 3.")["figure"]
f["tikz"] = (f["tikz"].replace("\\node[left, font=\\scriptsize] at (-0.1,0.95) {$4$ cm};", "\\node[right, font=\\scriptsize] at (0.02,0.42) {$4$ cm};")
             .replace("\\node[right, font=\\scriptsize] at (0.585,0.95) {$l$};", "\\node[right, font=\\scriptsize] at (0.6,1.05) {$l$};"))

# ---- 4) đánh số lại
n = 0
for s in d["stages"]:
    k = 0
    for b in s["blocks"]:
        if b.get("type") == "problem":
            k += 1
            b["label"] = (f"BTVN {k}." if s["kind"] == "reflection" else None) or b["label"]
    if s["kind"] in ("practice1", "practice2"):
        pass
k = 0
for s in d["stages"]:
    if s["kind"] in ("practice1", "practice2"):
        for b in s["blocks"]:
            if b.get("type") == "problem":
                k += 1; b["label"] = f"Bài {k}."
mapping = {}
for s in d["stages"]:
    for b in s["blocks"]:
        fg = b.get("figure")
        if isinstance(fg, dict) and fg.get("caption"):
            n += 1
            old = fg["caption"]; new = f"Hình {n}"
            fg["caption"] = new
            for key in ("statement", "text", "solution"):
                if isinstance(b.get(key), str):
                    b[key] = re.sub(rf"{re.escape(old)}(?!\d)", f"@@{n}@@", b[key])
for s in d["stages"]:
    for b in s["blocks"]:
        for key in ("statement", "text", "solution"):
            if isinstance(b.get(key), str):
                b[key] = re.sub(r"@@(\d+)@@", r"Hình \1", b[key])
P.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("ok", n, "hình")
