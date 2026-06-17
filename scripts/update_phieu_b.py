import json

path = '/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an/phieu-b-toan-thuc-te-lap-bpt.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find Luyện tập 2
for stage in data['stages']:
    if stage['number'] == 4:
        stage['title'] = 'Luyện tập 2 — Toán thực tế: gỡ giàn dần \\& các dạng bài'
        practice2 = stage
    elif stage['number'] == 5:
        reflection = stage

# Move Bài 11 (Lãi suất) and Bài 13 (Tuyển dụng) from reflection to practice2
btvn_blocks = reflection['blocks']
bai11_idx = next(i for i, b in enumerate(btvn_blocks) if b.get('label') == 'Bài 11.')
bai13_idx = next(i for i, b in enumerate(btvn_blocks) if b.get('label') == 'Bài 13.')

bai11_problem = btvn_blocks.pop(bai11_idx)
bai13_problem = btvn_blocks.pop(bai13_idx - 1)  # offset because of pop

# Change tier
bai11_problem['tier'] = 'onclass'
bai11_problem['label'] = 'Bài 7.'
bai13_problem['tier'] = 'onclass'
bai13_problem['label'] = 'Bài 8.'

# Add them to practice2
practice2['blocks'].extend([
    bai11_problem,
    {"type": "writelines", "count": 0},
    bai13_problem,
    {"type": "writelines", "count": 0}
])

# Now rename BTVN problems: 7->9, 8->10, 9->11, 10->12, 12->13
for block in btvn_blocks:
    if block.get('type') == 'problem':
        num = int(block['label'].replace('Bài ', '').replace('.', ''))
        if num == 7: block['label'] = 'Bài 9.'
        elif num == 8: block['label'] = 'Bài 10.'
        elif num == 9: block['label'] = 'Bài 11.'
        elif num == 10: block['label'] = 'Bài 12.'
        elif num == 12: block['label'] = 'Bài 13.'

# Add Bài 14 and 15
btvn_blocks.extend([
    {
        "type": "problem",
        "label": "Bài 14.",
        "tier": "btvn",
        "level": 3,
        "statement": "\\textbf{(GKI — Taxi)} Một hãng taxi quy định giá cước như sau: $15\\,000$ đồng cho $1$ km đầu tiên; từ km thứ $2$ trở đi giá $12\\,000$ đồng/km. Bạn An có không quá $200\\,000$ đồng. Gọi quãng đường An có thể đi là $x$ (km), $x>1$. [[br]] a) \\;[TH] Viết biểu thức tính số tiền An phải trả theo $x$. [[br]] b) \\;[VD] Lập bất phương trình, giải và trả lời: An có thể đi được tối đa bao nhiêu km?"
    },
    {
        "type": "writelines",
        "count": 0
    },
    {
        "type": "problem",
        "label": "Bài 15.",
        "tier": "btvn",
        "level": 2,
        "statement": "\\textbf{(Năng suất)} Một tổ công nhân dự định may $1\\,200$ chiếc áo. Mỗi ngày tổ may được $50$ chiếc áo. Gọi số ngày tổ làm việc là $x$ ($x>0$, nguyên). [[br]] a) \\;[NB] Viết biểu thức số áo may được sau $x$ ngày. [[br]] b) \\;[TH] Lập bất phương trình, giải và trả lời: tổ phải làm ít nhất bao nhiêu ngày để hoàn thành kế hoạch?"
    },
    {
        "type": "writelines",
        "count": 0
    }
])

# Update solution and teacher note in Luyện tập 2
practice2['solution'] = practice2['solution'] + "\\par\\smallskip \\textbf{Bài 7.} a) ``ít nhất'' $\\to$ dấu $\\ge$. [[br]] b) Tiền lãi $=4{,}5\\%\\cdot x=0{,}045x$ (triệu đồng). [[br]] c) $0{,}045x\\ge1{,}8 \\Rightarrow x\\ge40$. Vậy bác Hoàng phải gửi \\emph{ít nhất $40$ triệu đồng}.\\par\\smallskip \\textbf{Bài 8.} a) Số câu sai $=25-x$. [[br]] b) Điểm $=5+2x-(25-x)=3x-20$. [[br]] c) $3x-20\\ge25 \\Rightarrow 3x\\ge45 \\Rightarrow x\\ge15$. Vậy phải đúng \\emph{ít nhất $15$ câu}."

practice2['teacher_note'] = practice2['teacher_note'] + " [[br]] $\\bullet$ CÁC DẠNG BÀI MỚI (Từ BTVN đẩy lên): Bài 7 (Lãi suất Bát Tràng — lưu ý $4,5\\% = 0,045$), Bài 8 (Tuyển dụng tính điểm — gỡ rối số câu sai $= 25-x$)."

# Update solution in reflection
import re
sol = reflection['solution']
# Remove Bài 11 and 13 from reflection solution
sol = re.sub(r'\\par\\smallskip \\textbf{Bài 11.*?triệu đồng}\.', '', sol)
sol = re.sub(r'\\par\\smallskip \\textbf{Bài 13.*?15 câu}\.', '', sol)
# Rename others
sol = sol.replace('Bài 7.', 'Bài 9.')
sol = sol.replace('Bài 8.', 'Bài 10.')
sol = sol.replace('Bài 9.', 'Bài 11.')
sol = sol.replace('Bài 10.', 'Bài 12.')
sol = sol.replace('Bài 12.', 'Bài 13.')
# Append 14 and 15 before "Đáp án sơ đồ"
sol = sol.replace('\\par\\medskip \\textbf{Đáp án sơ đồ', '\\par\\smallskip \\textbf{Bài 14.} a) Tiền trả $=15\\,000+12\\,000(x-1)$. b) $15\\,000+12\\,000(x-1)\\le200\\,000 \\Rightarrow 12\\,000x+3\\,000\\le200\\,000 \\Rightarrow 12\\,000x\\le197\\,000 \\Rightarrow x\\le\\dfrac{197}{12}\\approx16{,}4$. Vậy đi được tối đa $16$ km.\\par\\smallskip \\textbf{Bài 15.} a) Số áo $=50x$. b) $50x\\ge1\\,200 \\Rightarrow x\\ge24$. Vậy phải làm ít nhất $24$ ngày.\\par\\medskip \\textbf{Đáp án sơ đồ')
reflection['solution'] = sol

# Update teacher note in reflection
tn = reflection['teacher_note']
tn = tn.replace('Bài 7-10', 'Bài 9-12')
tn = tn.replace('Bài 11 lãi suất Bát Tràng (NB + TH + VD — nghiệm tròn 40 triệu, không cần làm tròn); ', '')
tn = tn.replace('Bài 12 CHỈ LẬP', 'Bài 13 CHỈ LẬP')
tn = tn.replace('Bài 13 tuyển dụng (TH + TH + VD, ra $x\\ge15$ — gợi ý móc Bài 2f).', 'Bài 14 (Taxi) và Bài 15 (Năng suất).')
tn = tn.replace('Bài 12 thì tự hỏi lại', 'Bài 13 thì tự hỏi lại')
tn = tn.replace('bí Bài 13 thì mở lại', 'bí Bài 14 thì mở lại')
tn = tn.replace('tiết sau GV chữa trọn Bài 12', 'tiết sau GV chữa trọn Bài 13')
tn = tn.replace('và Bài 13.', 'và Bài 14, 15.')
tn = tn.replace('Bài 11 còn 3 ý', 'Bài 13 chỉ đề')
tn = tn.replace('$\\to$ Bài 12 chỉ đề + yêu cầu lập $\\to$ Bài 13 gần đề trần', '$\\to$ Bài 14, 15 gần đề trần')
reflection['teacher_note'] = tn

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Updated Phiếu B JSON.")
