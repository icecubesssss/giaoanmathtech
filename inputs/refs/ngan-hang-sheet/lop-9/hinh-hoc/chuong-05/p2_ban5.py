# Phiếu 2 ch.V 9C — lượt 5 (04/11/2026): căn giờ thực lớp C (Thầy duyệt "oke thế").
# Giờ thực HS C (config/phut_thuc.json): bản lượt 4 cần ~115′ trên lớp + 56′ BTVN.
# Chia lại: bỏ Bài 7 (Chu Văn An ý b — chấm lại còn 5,4 điểm: HS C 24′/định mức 15′, dạng tiếp tuyến 18%)
# và BTVN 4 (đề Lý Sơn, ~36′); đề đích Ái Mộ: ý a làm trên lớp, ý b về nhà (BTVN 4) trên hình HS đã vẽ.
# Chạy SAU p2_ban4.py: python3 p2v5.py <phiếu lượt 4> <out>
import json, sys

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
S = {s["kind"]: s for s in d["stages"]}

# ── Đích của buổi ──
p1 = S["practice1"]["blocks"]
dich = next(b for b in p1 if b.get("type") == "para" and "Đích của buổi" in b.get("text", ""))
dich["text"] = (
    "\\textbf{Đích của buổi học:} đề thi Câu IV.2 (đề Ái Mộ) ở \\textbf{Bài 7} — "
    "ý a chứng minh bốn điểm cùng thuộc một đường tròn (làm trên lớp), ý b chứng minh tiếp tuyến (làm ở nhà, BTVN 4)."
    "[[br]]Mỗi mạch đi ba bậc: \\textbf{nhớ kiến thức} (trắc nghiệm) $\\to$ \\textbf{xem bài mẫu} (ví dụ) "
    "$\\to$ \\textbf{điền khung bài giải} trên hình giống hình đề thi.")
S["practice1"]["teacher_note"] = (
    "Khoảng 49 phút với lớp C (giờ thực đo theo mô hình phút HS C): 3 trắc nghiệm ~10′, 2 ví dụ GV giảng ~18′, "
    "3 khung bài giải ~22′. Mỗi bài một hình riêng, hình gần giống hình đề đích (Bài 4: đề Hoàng Liệt; Bài 6: đề Cụm 14).")

# ── Luyện tập 2: chỉ còn đề đích, ý a ──
p2 = S["practice2"]["blocks"]
old7 = next(b for b in p2 if b.get("label") == "Bài 7.")      # Chu Văn An ý b — bỏ
dich_bai = next(b for b in p2 if b.get("label") == "Bài 8.")
st = dich_bai["statement"]
de, _, _ = st.partition("[[br]]a) [TH]")
y_a = "Chứng minh bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn."
y_b = "Chứng minh $DF$ là tiếp tuyến của $(O; R)$."
assert y_a in st and y_b in st
dich_bai.update(label="Bài 7.", dang_id="TH1", level=3)
dich_bai["statement"] = (de + "[[br]]a) [TH] " + y_a + "[[br]]b) " + y_b
                         + " \\textit{(Làm ở nhà — BTVN 4, trên hình em vẽ hôm nay.)}")
sol = dich_bai["solution"]
sol_a, _, sol_b = sol.partition("[[br]]b) ")
dich_bai["solution"] = sol_a
qt = dich_bai["quy_trinh"]
dich_bai["quy_trinh"] = [q for q in qt if not q.startswith(("Ý b", "$\\triangle OCF", "Kết luận"))]
S["practice2"]["blocks"] = [{"type": "para", "variant": "heading", "text": "Đề thi — đích của buổi học (trên lớp làm ý a)"}, dich_bai]
S["practice2"]["teacher_note"] = (
    "Khoảng 19 phút với lớp C: HS tự vẽ hình đề Ái Mộ (~6′) và trình bày ý a như Bài 4 (~13′). "
    "Còn ~10 phút chữa bài, chốt và giao BTVN. Ý b (tiếp tuyến — như Bài 6) làm ở nhà, chữa đầu buổi 3.")

# ── BTVN: bỏ đề Lý Sơn, thêm ý b của đề đích ──
r = S["reflection"]["blocks"]
r = [b for b in r if b.get("label") != "BTVN 4."]
k4 = {"type": "problem", "label": "BTVN 4.", "level": 3, "tier": "btvn", "dang_id": "VD1",
      "figure_given": False,
      "statement": "Làm tiếp \\textbf{ý b của Bài 7} (đề Ái Mộ, đích của buổi) trên hình em đã vẽ ở lớp: [VD] " + y_b,
      "solution": "b) " + sol_b,
      "quy_trinh": [q for q in qt if q.startswith(("Ý b", "$\\triangle OCF", "Kết luận"))]}
r.append(k4)
S["reflection"]["blocks"] = r
S["reflection"]["teacher_note"] = (
    "BTVN khoảng 40 phút với lớp C, dễ trước khó sau: BTVN 1 trả lời ngắn (~5′), BTVN 2 khung ý a (~6′), "
    "BTVN 3 khung ý b (~9′), BTVN 4 là ý b của đề đích (~19′) — đúng đường Ví dụ 2 và Bài 6. Chữa BTVN 4 đầu buổi 3.")

json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("ok — bỏ", old7["label"], "(Chu Văn An ý b)")
