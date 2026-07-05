import json

path = "inputs/seeds/lop-9/dai-so/lop-b/tuan05-pt-va-he-pt-bac-nhat-hai-an/phieu-b-pt-va-he-pt-bac-nhat-hai-an.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

for stage in data["stages"]:
    if stage["kind"] == "practice2":
        stage["solution"] = "\\textbf{Bài 4:} a) $2x+3y$. b) $4x+y$. c) $2x+3y=32$. d) $4x+y=24$. e) Hệ $\\begin{cases} 2x+3y=32 \\\\ 4x+y=24 \\end{cases}$. [[br]] Từ PT hai rút $y=24-4x$ thế vào PT đầu $\\Rightarrow 2x+3(24-4x)=32 \\Rightarrow -10x=-40 \\Rightarrow x=4, y=8$. Giá bút $4$k, vở $8$k. [[br]] \\textbf{Bài 5:} a) $x+y=35$. b) $2x$. c) $4y$. d) $2x+4y=94$. e) Hệ $\\begin{cases} x+y=35 \\\\ 2x+4y=94 \\end{cases}$. [[br]] $\\Rightarrow x=35-y \\Rightarrow 2(35-y)+4y=94 \\Rightarrow y=12, x=23$. Vậy $23$ gà, $12$ chó. [[br]] \\textbf{Bài 6:} a) $x+y=8$. b) Loại A: $6x$, loại B: $10y$. c) $6x+10y=60$. d) Hệ $\\begin{cases} x+y=8 \\\\ 6x+10y=60 \\end{cases}$. [[br]] $\\Rightarrow 6x+10(8-x)=60 \\Rightarrow -4x=-20 \\Rightarrow x=5, y=3$. Mua $5$ gói A, $3$ gói B. [[br]] \\textbf{Bài 7:} a) $x+y=200$. b) Loại I: $0{,}1x$, loại II: $0{,}3y$. c) $200 \\cdot 0{,}25=50$ (g). d) $0{,}1x+0{,}3y=50$. e) Hệ $\\begin{cases} x+y=200 \\\\ 0{,}1x+0{,}3y=50 \\end{cases}$. [[br]] f) Thế $x=200-y \\Rightarrow 0{,}1(200-y)+0{,}3y=50 \\Rightarrow 0{,}2y=30 \\Rightarrow y=150, x=50$. Dùng $50$ g loại I và $150$ g loại II."
    elif stage["kind"] == "reflection":
        stage["solution"] = "\\textbf{Bài 8:} a) Đ; b) S (có $xy$); c) Đ; d) Đ ($2-2=0$); e) Đ; f) Đ ($2$ ✓, $0$ ✓); g) Đ. [[br]] \\textbf{Bài 9:} a) $(x;\\,5-x)$. b) $x=0\\to y=5$; $x=2\\to y=3$; $x=5\\to y=0$. c) $(x;\\,3x-2)$. d) ví dụ $(1;4),(2;2)$. e) đường thẳng $x=4$ (thẳng đứng). [[br]] \\textbf{Bài 10:} a) $x+y$. b) $x+y=100$. c) $x-y=20$. [[br]] d) Hệ $\\begin{cases} x+y=100 \\\\ x-y=20 \\end{cases}$. [[br]] e) Cộng hai vế $\\Rightarrow 2x=120 \\Rightarrow x=60, y=40$. f) Dài $60$ m, rộng $40$ m. [[br]] \\textbf{Bài 11:} a) $x+y=40$. b) $x-y=4$. c) Hệ $\\begin{cases} x+y=40 \\\\ x-y=4 \\end{cases}$. [[br]] d) $2x=44 \\Rightarrow x=22, y=18$. e) Có $22$ nam, $18$ nữ. [[br]] \\textbf{Bài 12:} a) $x+y=300$. b) $0{,}2x$. c) $0{,}5y$. d) $300 \\cdot 0{,}4 = 120$. e) $0{,}2x+0{,}5y=120$. [[br]] f) Hệ $\\begin{cases} x+y=300 \\\\ 0{,}2x+0{,}5y=120 \\end{cases}$. [[br]] g) Thế $x=300-y \\Rightarrow 0{,}2(300-y)+0{,}5y=120 \\Rightarrow y=200, x=100$. Dùng $100$ lít loại I, $200$ lít loại II."

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
