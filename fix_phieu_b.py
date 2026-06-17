import json

path = '/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an/phieu-b-toan-thuc-te-lap-bpt.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for stage in data['stages']:
    if stage['number'] == 4:
        stage['title'] = 'Luyện tập 2 — Toán thực tế: gỡ giàn \& các dạng'
        
    elif stage['number'] == 5:
        blocks = stage['blocks']
        blocks.extend([
            {
                "type": "problem",
                "label": "Bài 16.",
                "tier": "btvn",
                "level": 3,
                "statement": "\\textbf{(Phí ship)} Một tiệm trà sữa bán $30\\,000$ đồng/cốc. Phí giao hàng là $15\\,000$ đồng/lần. Bạn Linh có nhiều nhất $200\\,000$ đồng. Gọi số cốc trà sữa Linh mua là $x$ ($x>0$, nguyên). [[br]] a) \\;[TH] Viết biểu thức tổng số tiền Linh phải trả theo $x$. [[br]] b) \\;[VD] Lập bất phương trình, giải và trả lời: Linh mua được tối đa bao nhiêu cốc?"
            },
            {
                "type": "writelines",
                "count": 0
            }
        ])
        
        sol = stage['solution']
        sol = sol.replace('\\par\\medskip \\textbf{Đáp án sơ đồ', '\\par\\smallskip \\textbf{Bài 16.} a) Tổng tiền $=30\\,000x+15\\,000$. [[br]] b) $30\\,000x+15\\,000\\le200\\,000 \\Rightarrow 30\\,000x\\le185\\,000 \\Rightarrow x\\le\\dfrac{37}{6}\\approx6{,}16$. Vậy mua được tối đa $6$ cốc.\\par\\medskip \\textbf{Đáp án sơ đồ')
        stage['solution'] = sol

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

