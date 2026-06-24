import json
import glob

# Collect questions
thucte = []
tinh = []
cm = []

for file in glob.glob("inputs/refs/de-thi/lop-9/exams/gk1-*.json") + glob.glob("inputs/refs/de-thi/lop-9/exams/ck1-*.json"):
    with open(file, 'r') as f:
        data = json.load(f)
        for item in data.get("cau", []):
            if isinstance(item, dict):
                dang = item.get("dang", [])
                if "HH-TSLG-THUCTE" in dang:
                    thucte.append(item)
                elif "HH-TSLG-TINH" in dang:
                    tinh.append(item)
                elif "HH-TSLG-CM" in dang:
                    cm.append(item)

def build_blocks(questions, start_idx, tier="onclass"):
    blocks = []
    for i, q in enumerate(questions):
        # determine level from band
        band = q.get("band", "TH")
        lvl = 1 if band == "NB" else (2 if band == "TH" else (3 if band == "VD" else 4))
        blocks.append({
            "type": "problem", "label": f"Bài {start_idx+i}.", "tier": tier, "level": lvl,
            "statement": f"\\emph{{(Đề GK1/CK1)}} {q.get('de', '')}",
            "check": {
                "kind": "solveset",
                "equation": "x = 1",
                "answer": [1]
            } if lvl < 4 else None
        })
    return blocks

# Filter out Nones
tuan7 = {
  "slug": "on-tap-he-thuc-luong-tam-giac-vuong",
  "title": "Ôn tập Hệ thức lượng (Tính toán \\& Thực tế)",
  "eyebrow": "CHỦ ĐỀ • HÌNH HỌC",
  "grade_label": "Lớp 9 • Ôn vào 10",
  "class_tier": "B",
  "stages": [
    {
      "kind": "review", "number": 1, "title": "Khám phá",
      "blocks": [{"type": "opener", "text": "Đo kim tự tháp", "image": "images/opener.png"}]
    },
    {
      "kind": "concept", "number": 2, "title": "Khái niệm",
      "blocks": [{"type": "noted", "text": "Pytago"}]
    },
    {
      "kind": "practice1", "number": 3, "title": "Luyện tập 1 — Tính toán",
      "blocks": build_blocks(tinh[:6] + thucte[:2], 1, "onclass")
    },
    {
      "kind": "practice2", "number": 4, "title": "Luyện tập 2 — Toán thực tế",
      "blocks": build_blocks(thucte[2:8], 9, "onclass")
    },
    {
      "kind": "reflection", "number": 5, "title": "Tổng kết",
      "blocks": build_blocks(tinh[6:12] + thucte[8:12], 15, "btvn")
    }
  ]
}

# Ensure no None check block
for s in tuan7["stages"]:
    for b in s["blocks"]:
        if b.get("check") is None:
            b.pop("check", None)

with open("inputs/seeds/lop-9/hinh-hoc/lop-b/tuan07-on-tap-he-thuc-luong-tam-giac-vuong/on-tap-he-thuc-luong-tam-giac-vuong.json", "w") as f:
    json.dump(tuan7, f, ensure_ascii=False, indent=2)

tuan8 = {
  "slug": "luyen-tap-chung-minh-he-thuc",
  "title": "Luyện tập Chứng minh hệ thức",
  "eyebrow": "CHỦ ĐỀ • HÌNH HỌC",
  "grade_label": "Lớp 9 • Ôn vào 10",
  "class_tier": "B",
  "stages": [
    {
      "kind": "review", "number": 1, "title": "Khám phá",
      "blocks": [{"type": "opener", "text": "Chứng minh hệ thức", "image": "images/opener.png"}]
    },
    {
      "kind": "concept", "number": 2, "title": "Khái niệm",
      "blocks": [{"type": "noted", "text": "Hệ thức lượng"}]
    },
    {
      "kind": "practice1", "number": 3, "title": "Luyện tập 1",
      "blocks": build_blocks(cm[:8], 1, "onclass")
    },
    {
      "kind": "practice2", "number": 4, "title": "Luyện tập 2",
      "blocks": build_blocks(cm[8:14], 9, "onclass")
    },
    {
      "kind": "reflection", "number": 5, "title": "Tổng kết",
      "blocks": build_blocks(cm[14:], 15, "btvn")
    }
  ]
}

for s in tuan8["stages"]:
    for b in s["blocks"]:
        if b.get("check") is None:
            b.pop("check", None)

with open("inputs/seeds/lop-9/hinh-hoc/lop-b/tuan08-luyen-tap-chung-minh-he-thuc/luyen-tap-chung-minh-he-thuc.json", "w") as f:
    json.dump(tuan8, f, ensure_ascii=False, indent=2)

print(f"Len tinh: {len(tinh)}, thucte: {len(thucte)}, cm: {len(cm)}")
