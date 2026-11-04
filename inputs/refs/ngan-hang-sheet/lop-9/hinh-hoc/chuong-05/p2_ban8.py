# Phiếu 2 ch.V 9C — lượt 8 (04/11/2026): bù ~5′ GV hướng dẫn HS vẽ cùng ở hai ví dụ.
# Bỏ Bài 5 (trắc nghiệm d so với R — kiến thức này đã có ở thẻ lý thuyết 2 và BTVN 1 bạn Thanh);
# đánh lại số Bài 6 → 5, Bài 7 → 6 ở MỌI chỗ (đề, quy trình, đích, ghi chú GV) và số hình.
# Chạy SAU p2_ban7.py: python3 p2v8.py <phiếu lượt 7> <out>
import json, re, sys

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
S = {s["kind"]: s for s in d["stages"]}
p1 = S["practice1"]["blocks"]
b5 = next(b for b in p1 if b.get("label") == "Bài 5.")
assert "tiếp xúc" in b5["statement"]
p1.remove(b5)

DOI = {"6": "5", "7": "6"}


def doi(t: str) -> str:
    return re.sub(r"Bài (\d+)", lambda m: "Bài " + DOI.get(m.group(1), m.group(1)), t)


for st in d["stages"]:
    if st["kind"] in ("review", "concept"):
        continue
    for b in st["blocks"]:
        for k in ("label", "text", "statement", "statement_slide", "solution", "answer"):
            if isinstance(b.get(k), str):
                b[k] = doi(b[k])
        if b.get("quy_trinh"):
            b["quy_trinh"] = [doi(q) for q in b["quy_trinh"]]
        if b.get("hints"):
            b["hints"] = [doi(h) for h in b["hints"]]
    if st.get("teacher_note"):
        st["teacher_note"] = doi(st["teacher_note"])
S["practice1"]["teacher_note"] = S["practice1"]["teacher_note"].replace(
    "3 trắc nghiệm ~10′", "2 trắc nghiệm ~6′")

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
d["btvn_phieu_rieng"] = True        # Thầy chốt 04/11/2026: BTVN tách thành file Phiếu BTVN riêng
d["btvn_trang_rieng"] = False
json.dump(d, open(out, "w"), ensure_ascii=False, indent=1)
print("ok")
