import json

data = {
  "slug": "phieu-b-on-tap-tong-hop-dai-so",
  "title": "Ôn hè 04 — Ôn tập tổng hợp Đại số 7",
  "eyebrow": "PHIẾU B",
  "grade_label": "Lớp 8",
  "class_tier": "B",
  "stages": [
    {
      "kind": "review",
      "number": 1,
      "title": "Khám phá",
      "blocks": [
        {
          "type": "opener",
          "text": "MỞ MÀN: Chúng ta đã đi qua một mùa hè với những mảng ghép rực rỡ của Đại số: Số hữu tỉ, Tỉ lệ thức và Đa thức. Hôm nay, hãy cùng ghép những mảng nhỏ đó thành một bức tranh tổng thể hoàn chỉnh để sẵn sàng bước vào năm học mới!"
        },
        {
          "type": "para",
          "text": "Ôn tập nhanh:[[br]]- Thứ tự thực hiện phép tính: Ngoặc trước, Lũy thừa, Nhân/Chia, Cộng/Trừ.[[br]]- Dãy tỉ số bằng nhau: Công cụ giải quyết các bài toán chia phần.[[br]]- Đa thức một biến: Nhân chia đa thức, cộng trừ đa thức và tìm nghiệm của đa thức (giá trị làm cho đa thức bằng 0)."
        }
      ],
      "solution": "1. Mở màn:[[br]]2. Ôn tập:[[br]]Học sinh nghe và ghi nhớ.",
      "teacher_note": "Buổi tổng hợp, khuyến khích HS làm nhanh."
    },
    {
      "kind": "concept",
      "number": 2,
      "title": "Hệ thống kiến thức và Ví dụ mẫu",
      "blocks": [
        {
          "type": "noted",
          "text": "\\textbf{1. Thực hiện phép tính số hữu tỉ và Tỉ lệ thức}[[br]]Luôn ưu tiên làm trong ngoặc trước, nhân chia trước, cộng trừ sau.[[br]]Với tỉ lệ thức, ta dùng tính chất nhân chéo hoặc dãy tỉ số bằng nhau."
        },
        {
          "type": "noted",
          "variant": "example",
          "text": "\\textbf{Ví dụ 1 (NB):} Thực hiện phép tính:[[br]]a) \\( \\left( \\dfrac{1}{2} - \\dfrac{1}{3} \\right)^2 : \\dfrac{1}{36} \\)[[br]]b) \\( \\dfrac{3}{4} \\cdot \\dfrac{2}{5} - \\dfrac{1}{4} \\cdot \\dfrac{2}{5} \\)"
        },
        {
          "type": "noted",
          "text": "\\textbf{2. Dãy tỉ số bằng nhau}[[br]]Là công cụ mạnh mẽ để tìm nhiều số khi biết tổng hoặc hiệu của chúng."
        },
        {
          "type": "noted",
          "variant": "example",
          "text": "\\textbf{Ví dụ 2 (NB):} Tìm \\( x, y \\) biết \\( \\dfrac{x}{3} = \\dfrac{y}{5} \\) và \\( x + y = 16 \\)."
        },
        {
          "type": "noted",
          "text": "\\textbf{3. Đa thức một biến và Nghiệm}[[br]]Thực hiện cộng, trừ, nhân, chia đa thức.[[br]]Nghiệm của đa thức \\( P(x) \\) là giá trị \\( x \\) sao cho \\( P(x) = 0 \\)."
        },
        {
          "type": "noted",
          "variant": "example",
          "text": "\\textbf{Ví dụ 3 (TH):} Cho đa thức \\( P(x) = x^2 - 3x + 2 \\).[[br]]a) Tính \\( P(1) \\) và \\( P(2) \\).[[br]]b) Chứng tỏ \\( x = 1 \\) và \\( x = 2 \\) là các nghiệm của đa thức \\( P(x) \\)."
        },
        {
          "type": "noted",
          "variant": "example",
          "text": "\\textbf{Ví dụ 4 (VD):} Tìm \\( x \\) thỏa mãn: \\( 2|x - 1| - 3 = 5 \\)."
        }
      ],
      "solution": "Ví dụ 1:[[br]]a) \\( (1/6)^2 : 1/36 = (1/36) : (1/36) = 1 \\).[[br]]b) \\( (2/5)(3/4 - 1/4) = (2/5)(2/4) = 1/5 \\).[[br]]Ví dụ 2:[[br]]\\( x/3 = y/5 = (x+y)/8 = 16/8 = 2 \\) nên \\( x=6 \\), \\( y=10 \\).[[br]]Ví dụ 3:[[br]]a) \\( P(1) = 1 - 3 + 2 = 0 \\). \\( P(2) = 4 - 6 + 2 = 0 \\).[[br]]b) Vì \\( P(1)=0 \\) và \\( P(2)=0 \\) nên \\( x=1 \\), \\( x=2 \\) là nghiệm.[[br]]Ví dụ 4:[[br]]\\( 2|x-1| = 8 \\Rightarrow |x-1| = 4 \\Rightarrow x-1=4 \\) hoặc \\( x-1=-4 \\Rightarrow x=5 \\) hoặc \\( x=-3 \\).",
      "teacher_note": "Hệ thống lại 4 mảng chính: Số hữu tỉ, Tỉ lệ, Đa thức, Bài toán tìm x."
    },
    {
      "kind": "practice1",
      "number": 3,
      "title": "Luyện tập 1",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 1.",
          "level": 1,
          "tier": "onclass",
          "statement": "Thực hiện phép tính (tính hợp lý nếu có thể):[[br]]a) \\( \\dfrac{2}{5} + \\dfrac{3}{5} : \\dfrac{3}{4} \\)[[br]]b) \\( \\left( \\dfrac{-1}{2} \\right)^3 \\cdot 8 + \\dfrac{3}{4} \\)[[br]]c) \\( \\dfrac{5}{7} \\cdot \\dfrac{2}{11} + \\dfrac{5}{7} \\cdot \\dfrac{9}{11} \\)[[br]]d) \\( \\dfrac{4}{9} - \\dfrac{5}{9} \\cdot \\dfrac{3}{5} \\)[[br]]e) \\( | -\\dfrac{1}{2} | - \\dfrac{3}{2} \\)[[br]]f) \\( \\left( 1 - \\dfrac{1}{3} \\right)^2 + \\dfrac{5}{9} \\)[[br]]g) \\( 2^3 - 3 \\cdot \\left( \\dfrac{1}{2} \\right)^0 \\)[[br]]h) \\( \\dfrac{15}{4} : \\dfrac{5}{2} - \\dfrac{1}{2} \\)"
        },
        {
          "type": "problem",
          "label": "Bài 2.",
          "level": 1,
          "tier": "onclass",
          "statement": "Tìm \\( x \\) biết:[[br]]a) \\( x - \\dfrac{1}{3} = \\dfrac{2}{3} \\)[[br]]b) \\( 2x + \\dfrac{1}{2} = \\dfrac{5}{2} \\)[[br]]c) \\( \\dfrac{x}{4} = \\dfrac{-3}{2} \\)[[br]]d) \\( \\dfrac{3}{5}x - 1 = \\dfrac{1}{5} \\)[[br]]e) \\( 5(x - 2) = 15 \\)[[br]]f) \\( -3x + 4 = 10 \\)[[br]]g) \\( x(x - 3) = 0 \\)[[br]]h) \\( x^2 - 16 = 0 \\)"
        },
        {
          "type": "problem",
          "label": "Bài 3.",
          "level": 1,
          "tier": "onclass",
          "statement": "Áp dụng dãy tỉ số bằng nhau và tính toán đa thức:[[br]]a) Tìm \\( x, y \\) biết \\( \\dfrac{x}{2} = \\dfrac{y}{7} \\) và \\( x + y = 18 \\) (Tìm x).[[br]]b) (Tìm y của câu a).[[br]]c) Cho \\( A(x) = 2x + 1 \\), tính \\( A(1) \\).[[br]]d) Tính \\( A(-2) \\).[[br]]e) Cho \\( B(x) = x^2 - 2x \\), tính \\( B(0) \\).[[br]]f) Tính \\( B(2) \\).[[br]]g) Tính tổng hai đa thức \\( (x^2 + 2x) + (x^2 - x) \\).[[br]]h) Thực hiện phép nhân \\( x(2x - 3) \\)."
        }
      ],
      "solution": "Bài 1: a) \\( 6/5 \\). b) \\( -1/4 \\). c) \\( 5/7 \\). d) \\( 1/9 \\). e) \\( -1 \\). f) \\( 1 \\). g) \\( 5 \\). h) \\( 1 \\).[[br]]Bài 2: a) \\( 1 \\), b) \\( 1 \\), c) \\( -6 \\), d) \\( 2 \\), e) \\( 5 \\), f) \\( -2 \\), g) \\( 0 \\) hoặc \\( 3 \\), h) \\( 4 \\) hoặc \\( -4 \\).[[br]]Bài 3: a) \\( x=4 \\), b) \\( y=14 \\). c) \\( 3 \\). d) \\( -3 \\). e) \\( 0 \\). f) \\( 0 \\). g) \\( 2x^2+x \\). h) \\( 2x^2-3x \\).",
      "teacher_note": "24 câu NB."
    },
    {
      "kind": "practice2",
      "number": 4,
      "title": "Luyện tập 2",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 4.",
          "level": 2,
          "tier": "onclass",
          "statement": "Giải bài toán thực tế và tìm nghiệm đa thức:[[br]]a) Số học sinh giỏi, khá, trung bình của khối 7 tỉ lệ với 5, 4, 2. Tổng số học sinh giỏi và khá là 180 em. Tính số học sinh giỏi.[[br]]b) Tính số học sinh khá.[[br]]c) Tính số học sinh trung bình.[[br]]d) Cho đa thức \\( M(x) = 3x - 6 \\). Tìm nghiệm của đa thức \\( M(x) \\).[[br]]e) Cho đa thức \\( N(x) = (x - 2)(2x + 1) \\). Tìm nghiệm của đa thức \\( N(x) \\)."
        },
        {
          "type": "problem",
          "label": "Bài 5.",
          "level": 2,
          "tier": "onclass",
          "statement": "Thực hiện phép chia đa thức và rút gọn:[[br]]a) \\( (x^2 + 4x + 3) : (x + 1) \\)[[br]]b) \\( (2x^3 - x^2 + 4x - 2) : (2x - 1) \\)[[br]]c) Rút gọn: \\( x(x - 3) - (x + 1)(x - 1) \\)[[br]]d) Rút gọn: \\( (2x - 1)^2 - 4x(x - 1) \\)"
        },
        {
          "type": "para",
          "text": "\\textbf{Nhịp cầu.} Để giải bài toán có chứa giá trị tuyệt đối, ta cần xét hai trường hợp (sau khi đã cô lập phần chứa giá trị tuyệt đối)."
        },
        {
          "type": "problem",
          "label": "Bài 6.",
          "level": 3,
          "tier": "onclass",
          "statement": "Giải bài toán nâng cao:[[br]]a) Tìm \\( x \\) biết: \\( 3|x - 2| - 5 = 10 \\).[[br]]b) Cho đa thức \\( P(x) = ax^2 + bx + c \\). Biết \\( P(0) = 1, P(1) = 3 \\) và \\( P(-1) = 3 \\). Tìm \\( a, b, c \\)."
        }
      ],
      "solution": "Bài 4: a) \\( G/5 = K/4 = TB/2 \\). \\( G+K = 180 \\). \\( (G+K)/9 = 20 \\). \\( G=100 \\). b) \\( K=80 \\). c) \\( TB=40 \\). d) \\( 3x-6=0 \\Rightarrow x=2 \\). e) \\( x=2 \\) hoặc \\( x=-1/2 \\).[[br]]Bài 5: a) \\( x+3 \\). b) \\( x^2+2 \\). c) \\( x^2-3x-x^2+1 = -3x+1 \\). d) \\( 4x^2-4x+1 - 4x^2+4x = 1 \\).[[br]]Bài 6: a) \\( 3|x-2| = 15 \\Rightarrow |x-2|=5 \\Rightarrow x=7 \\) hoặc \\( x=-3 \\). b) \\( P(0)=c=1 \\). \\( P(1)=a+b+1=3 \\Rightarrow a+b=2 \\). \\( P(-1)=a-b+1=3 \\Rightarrow a-b=2 \\). Suy ra \\( a=2, b=0, c=1 \\).",
      "teacher_note": "Bài 5d có HĐT nhưng HS lớp 7 có thể nhân bung (2x-1)(2x-1) để rút gọn."
    },
    {
      "kind": "reflection",
      "number": 5,
      "title": "Tổng kết và BTVN",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 7.",
          "level": 1,
          "tier": "btvn",
          "statement": "Thực hiện phép tính:[[br]]a) \\( \\dfrac{-3}{4} + \\dfrac{5}{4} \\)[[br]]b) \\( \\dfrac{2}{7} \\cdot \\dfrac{14}{5} \\)[[br]]c) \\( \\dfrac{4}{9} : \\dfrac{2}{3} \\)[[br]]d) \\( ( -2 )^3 + 10 \\)[[br]]e) \\( | -5 | - 2 \\)[[br]]f) \\( \\dfrac{1}{2} - \\dfrac{1}{3} \\cdot \\dfrac{3}{4} \\)[[br]]g) \\( \\left( \\dfrac{2}{3} \\right)^2 - \\dfrac{1}{9} \\)[[br]]h) \\( 3x(x - 2) \\)[[br]]i) \\( (x^2 + 3x) : x \\)"
        },
        {
          "type": "problem",
          "label": "Bài 8.",
          "level": 1,
          "tier": "btvn",
          "statement": "Tìm \\( x \\) và tính đa thức:[[br]]a) \\( 2x - 3 = 7 \\)[[br]]b) \\( 4 - 3x = 10 \\)[[br]]c) \\( \\dfrac{x}{5} = \\dfrac{-2}{10} \\)[[br]]d) Tìm \\( x \\): \\( \\dfrac{x}{3} = \\dfrac{y}{4} \\) và \\( x+y=14 \\).[[br]]e) Tìm y của câu d.[[br]]f) Cho \\( M(x) = x^2 - 1 \\), tính \\( M(2) \\).[[br]]g) Tính \\( M(-2) \\).[[br]]h) Tìm nghiệm của \\( M(x) \\)."
        },
        {
          "type": "problem",
          "label": "Bài 9.",
          "level": 2,
          "tier": "btvn",
          "statement": "Rút gọn biểu thức và tìm \\( x \\):[[br]]a) \\( x(x+5) - x(x-2) \\)[[br]]b) \\( (x-3)(x+3) - (x^2 - 9) \\)[[br]]c) Tìm \\( x \\): \\( 2(x+1) - 3(x-2) = 10 \\)"
        },
        {
          "type": "problem",
          "label": "Bài 10.",
          "level": 2,
          "tier": "btvn",
          "statement": "Giải toán thực tế và tìm nghiệm:[[br]]a) Ba miếng đất có diện tích tỉ lệ 2:3:5. Tổng diện tích là 100 ha. Tính diện tích miếng đất lớn nhất.[[br]]b) Tìm nghiệm của đa thức \\( Q(x) = x^2 - 5x + 6 \\).[[br]]c) Tìm nghiệm của đa thức \\( R(x) = x^3 - 4x \\)."
        },
        {
          "type": "problem",
          "label": "Bài 11.",
          "level": 3,
          "tier": "btvn",
          "statement": "Nâng cao:[[br]]a) Tìm \\( x \\) biết \\( |x - 1| + |2x - 2| = 9 \\).[[br]]b) Cho đa thức \\( f(x) \\) thỏa mãn \\( x \\cdot f(x+1) = (x-2) \\cdot f(x) \\). Chứng minh đa thức \\( f(x) \\) có ít nhất 2 nghiệm."
        }
      ],
      "solution": "Bài 7: Tính toán. a) \\( 1/2 \\). b) \\( 4/5 \\). c) \\( 2/3 \\). d) \\( 2 \\). e) \\( 3 \\). f) \\( 1/4 \\). g) \\( 1/3 \\). h) \\( 3x^2-6x \\). i) \\( x+3 \\).[[br]]Bài 8: a) \\( 5 \\). b) \\( -2 \\). c) \\( -1 \\). d) \\( 6 \\). e) \\( 8 \\). f) \\( 3 \\). g) \\( 3 \\). h) \\( 1 \\) và \\( -1 \\).[[br]]Bài 9: a) \\( 7x \\). b) \\( 0 \\). c) \\( 2x+2-3x+6=10 \\Rightarrow -x+8=10 \\Rightarrow x=-2 \\).[[br]]Bài 10: a) \\( 50 \\) ha. b) \\( x=2 \\), \\( x=3 \\). c) \\( x(x-2)(x+2)=0 \\Rightarrow x=0, 2, -2 \\).[[br]]Bài 11: a) \\( |x-1| + 2|x-1| = 9 \\Rightarrow 3|x-1|=9 \\Rightarrow |x-1|=3 \\Rightarrow x=4 \\), \\( x=-2 \\). b) Thay \\( x=0 \\Rightarrow 0 = -2\\cdot f(0) \\Rightarrow f(0)=0 \\). Thay \\( x=2 \\Rightarrow 2\\cdot f(3) = 0 \\Rightarrow f(3)=0 \\). Vậy \\( x=0 \\), \\( x=3 \\) là nghiệm.",
      "teacher_note": "Bài 11b là bài kinh điển."
    }
  ]
}

with open("/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-8/dai-so/lop-b/on-he-04-on-tap-tong-hop-dai-so/phieu-b-on-tap-tong-hop-dai-so.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
