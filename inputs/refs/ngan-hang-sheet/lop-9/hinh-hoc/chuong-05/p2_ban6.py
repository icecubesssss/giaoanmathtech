# Phiếu 2 ch.V 9C — lượt 6 (04/11/2026). Thầy: "ra đề thì cần đầy đủ … bỏ những lời kiểu em làm cái này
# cái nọ … các hình trong bài chỉ để tam giác, điểm nằm ngoài đường tròn… còn các yếu tố phải vẽ thì để HS
# tự vẽ vào hình trên phiếu, thêm 2-4 phút mỗi câu".
# Hình nền (figure.tikz) cùng khung toạ độ với hình đầy đủ (figure.tikz_gv — chỉ in ở Sổ tay GV).
# Cân giờ: bỏ BTVN hai đường cao (cùng hình Ví dụ 1); đề đích dùng hình nền thay vì vẽ từ đầu.
# Chạy SAU p2_ban5.py: python3 p2v6.py <phiếu lượt 5> <out>
import json, math, re, sys
sys.path.insert(0, ".")
from scripts.tikz_geo import Fig, polar

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
S = {s["kind"]: s for s in d["stages"]}
R_ = "\\Rightarrow"


def khung_toa_do(tikz: str) -> str:
    """\\path bao đúng khung của hình đầy đủ — hình nền giữ chỗ cho HS vẽ tiếp."""
    xy = [(float(a), float(b)) for a, b in re.findall(r"\((-?\d+\.\d+),(-?\d+\.\d+)\)", tikz)]
    xs, ys = [p[0] for p in xy], [p[1] for p in xy]
    return f"  \\path ({min(xs) - 0.15:.4f},{min(ys) - 0.15:.4f}) rectangle ({max(xs) + 0.15:.4f},{max(ys) + 0.15:.4f});"


def nen(f: Fig, full_tikz: str) -> str:
    t = f.tikz()
    return t.replace("\\end{tikzpicture}", khung_toa_do(full_tikz) + "\n\\end{tikzpicture}")


# ── hình nền, cùng toạ độ với hình đầy đủ ở p2_ban4.py ──
def n_hinhchieu():
    f = Fig()
    for n, p in [("A", (1.6, 2.4)), ("B", (0, 0)), ("C", (3.6, 0))]:
        f.pt(n, p)
    f.poly("A", "B", "C")
    return f


def n_hoangliet():
    f = Fig(); f.circle((0, 0), 1.2)
    f.pt("O", (0, 0)); f.pt("A", (3.0, 0)); f.seg("O", "A")
    return f


def n_cum14():
    f = Fig(); R = 1.5
    f.circle((0, 0), R)
    for n, p in [("O", (0, 0)), ("A", (-R, 0)), ("B", (R, 0)), ("M", polar(70, R))]:
        f.pt(n, p)
    f.seg("A", "B")
    return f


def n_dongda04():
    f = Fig(); R = 1.5
    f.arc((0, 0), R, 0, 180)
    for n, p in [("O", (0, 0)), ("A", (-R, 0)), ("B", (R, 0)), ("C", polar(100, R))]:
        f.pt(n, p)
    f.seg("A", "B")
    return f


def h_aimo():                                  # hình đầy đủ đề Ái Mộ (Sổ tay GV)
    f = Fig(); R = 1.5
    O, A, B = (0, 0), (-R, 0), (R, 0)
    C = polar(60, R); H = (C[0], 0); D = (C[0], -C[1])
    M = polar(120, R / math.cos(math.radians(60))); F = (R * R / C[0], 0)
    f.circle(O, R)
    for n, p in [("O", O), ("A", A), ("B", B), ("C", C), ("D", D), ("H", H), ("M", M), ("F", F)]:
        f.pt(n, p)
    f.seg("A", "F"); f.seg("C", "D"); f.seg("M", "A"); f.seg("M", "F")
    f.seg("O", "C"); f.seg("O", "D"); f.seg("D", "F")
    f.right("H", "C", "B")
    return f


def n_aimo():
    f = Fig(); R = 1.5
    f.circle((0, 0), R)
    for n, p in [("O", (0, 0)), ("A", (-R, 0)), ("B", (R, 0)), ("C", polar(60, R))]:
        f.pt(n, p)
    f.seg("A", "B")
    return f


VE = "Vẽ tiếp vào Hình 0 các yếu tố còn thiếu theo đề"


def ha_hinh_nen(b, f_nen, phut, them=""):
    """Hình đầy đủ → tikz_gv; hình nền → tikz; câu dẫn vẽ tiếp; cộng phút vẽ tiếp."""
    full = b["figure"]["tikz"]
    b["figure"].update(tikz=nen(f_nen, full), tikz_gv=full)
    b["ve_tiep"] = phut
    for k in ("statement", "statement_slide"):
        if not b.get(k):
            continue
        s = b[k]
        s = s.replace("Đánh dấu hai góc vuông lên hình, rồi điền vào chỗ chấm để hoàn thành bài giải:",
                      VE + ", đánh dấu hai góc vuông, rồi điền vào chỗ chấm để hoàn thành bài giải:")
        if VE not in s:
            s = s.replace("Điền vào chỗ chấm để hoàn thành bài giải:",
                          VE + ", rồi điền vào chỗ chấm để hoàn thành bài giải:")
        b[k] = s
    assert VE in b["statement"], b["label"]


p1 = S["practice1"]["blocks"]
lab = {b.get("label"): b for b in p1 if b.get("type") == "problem"}
ha_hinh_nen(lab["Bài 3."], n_hinhchieu(), 2)      # vẽ AD, DE, DF
ha_hinh_nen(lab["Bài 4."], n_hoangliet(), 3)      # vẽ d ⊥ OA, M, tiếp tuyến MB
ha_hinh_nen(lab["Bài 6."], n_cum14(), 4)          # hai tiếp tuyến, C, đường ⊥ MB, H, D

dich = next(b for b in p1 if b.get("type") == "para" and "Đích của buổi" in b.get("text", ""))
dich["text"] = ("\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Ái Mộ) — ý a chứng minh bốn điểm cùng thuộc "
                "một đường tròn (Bài 7), ý b chứng minh tiếp tuyến (BTVN 3).")

# ── Đề đích: ghi ĐỦ đề, hình nền, ý a trên lớp ──
p2 = S["practice2"]["blocks"]
b7 = next(b for b in p2 if b.get("label") == "Bài 7.")
GT = ("Cho đường tròn $(O; R)$ đường kính $AB$. Lấy điểm $C$ thuộc $(O; R)$ sao cho $AC > BC$. Kẻ đường cao $CH$ của "
      "$\\triangle ABC$ ($H \\in AB$), kéo dài $CH$ cắt $(O; R)$ tại $D$ ($D \\ne C$). Tiếp tuyến tại $A$ và tiếp tuyến tại $C$ "
      "của $(O; R)$ cắt nhau tại $M$. Gọi $F$ là giao điểm của $MC$ và $AB$ (Hình 0). " + VE + ".")
assert b7["statement"].startswith("[VD] Cho đường tròn $(O; R)$ đường kính $AB$.") or b7["statement"].startswith("Cho đường tròn")
b7["statement"] = GT + "[[br]][TH] Chứng minh bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn."
b7.pop("draw", None)
b7["figure_given"] = False                 # hình nền thôi — ý TH vẫn tính đủ phút tự trình bày
full = h_aimo().tikz()
b7["figure"] = {"tikz": nen(n_aimo(), full), "tikz_gv": full, "caption": "Hình 0", "pos": "right"}
b7["ve_tiep"] = 3
b7["solution"] = re.sub(r"^a\) ", "", b7["solution"])
b7["quy_trinh"] = (["Vẽ tiếp hình: đường cao $CH$ kéo dài cắt $(O)$ tại $D$; tiếp tuyến tại $A$, tại $C$ cắt nhau ở $M$; $MC$ cắt $AB$ tại $F$; đánh dấu các góc vuông"]
                   + [q for q in b7["quy_trinh"] if q.startswith("Ý a")])
for b in p2:
    if b.get("type") == "para":
        b["text"] = "Đề thi — đích của buổi học"
S["practice2"]["teacher_note"] = (
    "Khoảng 17 phút với lớp C: HS vẽ tiếp hình đề Ái Mộ trên hình nền (~3′), trình bày ý a như Bài 4 (~14′). "
    "Ý b của đề này là BTVN 3 (ghi lại đủ đề), chữa đầu buổi 3.")

# ── BTVN: bỏ hai đường cao; Đống Đa hình nền; đề đích ý b ghi đủ đề ──
r = S["reflection"]["blocks"]
r = [b for b in r if not (b.get("type") == "problem" and b.get("label") == "BTVN 2.")]   # hai đường cao (trùng hình Ví dụ 1)
lb = {b.get("label"): b for b in r if b.get("type") == "problem"}
ha_hinh_nen(lb["BTVN 3."], n_dongda04(), 3)       # vẽ K, tiếp tuyến tại B, tia OK, D
k4 = lb["BTVN 4."]
k4["statement"] = GT + "[[br]][VD] Chứng minh $DF$ là tiếp tuyến của $(O; R)$."
k4["figure"] = {"tikz": nen(n_aimo(), full), "tikz_gv": full, "caption": "Hình 0", "pos": "right"}
k4["ve_tiep"] = 4
k4["figure_given"] = False
k4["solution"] = re.sub(r"^b\) ", "", k4["solution"])
k4["quy_trinh"] = (["Vẽ tiếp hình: đường cao $CH$ kéo dài cắt $(O)$ tại $D$; tiếp tuyến tại $A$, tại $C$ cắt nhau ở $M$; $MC$ cắt $AB$ tại $F$; nối $DF$, $OC$, $OD$"]
                   + [re.sub(r"^Ý b: ", "", q) for q in k4["quy_trinh"]])
n = 0
for b in r:
    if b.get("type") == "problem":
        n += 1
        b["label"] = f"BTVN {n}."
S["reflection"]["blocks"] = r
S["reflection"]["teacher_note"] = (
    "BTVN khoảng 40 phút với lớp C: BTVN 1 trả lời ngắn (~5′), BTVN 2 vẽ tiếp hình + khung ý b đề Đống Đa (~12′), "
    "BTVN 3 là ý b của đề đích Ái Mộ, vẽ tiếp hình rồi tự trình bày như Ví dụ 2 và Bài 6 (~25′).")
S["practice1"]["teacher_note"] = (
    "Khoảng 58 phút với lớp C: 3 trắc nghiệm ~10′, 2 ví dụ GV giảng ~18′, 3 khung bài giải ~22′ cộng ~9′ HS vẽ tiếp "
    "lên hình nền (Bài 3: đường cao và hai hình chiếu; Bài 4: đường thẳng $d$, điểm $M$, tiếp tuyến $MB$; "
    "Bài 6: hai tiếp tuyến và đường vuông góc với $MB$).")

# ── đánh số hình theo thứ tự xuất hiện; mỗi bài chỉ trỏ hình của chính nó ──
n = sum(1 for k in ("review", "concept") for b in S[k]["blocks"]
        if isinstance(b.get("figure"), dict) and str(b["figure"].get("caption", "")).startswith("Hình"))
for kind in ("practice1", "practice2", "reflection"):
    for b in S[kind]["blocks"]:
        f = b.get("figure")
        if isinstance(f, dict) and str(f.get("caption", "")).startswith("Hình"):
            n += 1
            for k in ("statement", "text", "statement_slide"):
                if isinstance(b.get(k), str):
                    b[k] = re.sub(r"Hình \d+", f"Hình {n}", b[k])
            f["caption"] = f"Hình {n}"

# ── mã dạng sau khi bỏ dòng hai đường cao khỏi thuyết minh (NB4 cũ) ──
MA = {"Bài 3.": "NB4", "Bài 4.": "NB5", "Bài 6.": "NB6", "BTVN 2.": "NB6", "BTVN 3.": "VD1", "Bài 7.": "TH1"}
for st in d["stages"]:
    for b in st["blocks"]:
        if b.get("type") == "problem" and b.get("label") in MA:
            b["dang_id"] = MA[b["label"]]
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("ok")
