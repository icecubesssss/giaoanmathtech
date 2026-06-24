import json

tuan7 = {
  "slug": "on-tap-he-thuc-luong-tam-giac-vuong",
  "title": "Ôn tập Hệ thức lượng trong tam giác vuông (Tính toán & Thực tế)",
  "eyebrow": "CHỦ ĐỀ • HÌNH HỌC",
  "grade_label": "Lớp 9 • Ôn vào 10",
  "class_tier": "B",
  "stages": [
    {
      "kind": "review",
      "number": 1,
      "title": "Khám phá — Toán thực tế",
      "blocks": [
        {
          "type": "opener",
          "text": "Bạn có biết người xưa đã đo chiều cao của các Kim tự tháp bằng cách nào không? Chỉ bằng một cây gậy và bóng nắng mặt trời! Hãy cùng ôn lại các công cụ Hệ thức lượng để tính toán những khoảng cách không thể đo trực tiếp.",
          "image": "images/opener.png"
        },
        {
          "type": "noted",
          "text": "\\textbf{Nhắc lại kiến thức:}\n1. Định lý Pytago: $BC^2 = AB^2 + AC^2$.\n2. Tỉ số lượng giác: $\\sin = \\frac{\\text{đối}}{\\text{huyền}}$, $\\cos = \\frac{\\text{kề}}{\\text{huyền}}$, $\\tan = \\frac{\\text{đối}}{\\text{kề}}$, $\\cot = \\frac{\\text{kề}}{\\text{đối}}$."
        }
      ],
      "solution": "Học sinh ghi nhớ kiến thức.",
      "teacher_note": "GV cho học sinh thảo luận nhanh về ứng dụng thực tế."
    },
    {
      "kind": "practice1",
      "number": 2,
      "title": "Luyện tập 1 — Tính toán giải tam giác vuông",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 1.",
          "statement": "\\emph{(Bài tập ôn cũ)} Cho tam giác $ABC$ vuông tại $A$, biết $\\sin B = \\frac{3}{5}$. Tính $\\cos B, \\tan B, \\cot B$.",
          "tier": "onclass",
          "level": 1
        },
        {
          "type": "problem",
          "label": "Bài 2.",
          "statement": "\\emph{(Đề GK1 - Nguyễn Bỉnh Khiêm)} Tam giác $ABC$ vuông tại $A$, đường cao $AH$. Biết $AB = 6$ cm, $AC = 8$ cm. Tính độ dài $BC$ và số đo các góc $B, C$ (làm tròn đến độ).",
          "tier": "onclass",
          "level": 2
        }
      ],
      "solution": "Bài 1: $\\cos B = \\frac{4}{5}, \\tan B = \\frac{3}{4}, \\cot B = \\frac{4}{3}$.\nBài 2: $BC = 10$ cm, $\\widehat B \\approx 53^\\circ, \\widehat C \\approx 37^\\circ$.",
      "teacher_note": "Nhấn mạnh việc sử dụng máy tính cầm tay."
    },
    {
      "kind": "practice2",
      "number": 3,
      "title": "Luyện tập 2 — Toán thực tế (Trọng tâm đề thi)",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 3.",
          "statement": "\\emph{(Đề GK1 - Nguyễn Bỉnh Khiêm)} Tia nắng mặt trời tạo với mặt đất một góc xấp xỉ $34^\\circ$. Bóng của một tòa tháp trên mặt đất dài $8{,}6$ m. Tính chiều cao của tòa tháp (làm tròn đến mét).",
          "tier": "onclass",
          "level": 3
        },
        {
          "type": "problem",
          "label": "Bài 4.",
          "statement": "\\emph{(Đề GK1 - Địch Vọng Hậu)} Một chiếc thang dài $4$ m dựa vào tường. Góc tạo bởi thang và mặt đất là $65^\\circ$. Tính khoảng cách từ chân thang đến chân tường (làm tròn đến chữ số thập phân thứ hai).",
          "tier": "home",
          "level": 3
        }
      ],
      "solution": "Bài 3: Chiều cao tháp $h = 8{,}6 \\cdot \\tan 34^\\circ \\approx 6$ m.\nBài 4: Khoảng cách $d = 4 \\cdot \\cos 65^\\circ \\approx 1{,}69$ m.",
      "teacher_note": "Vẽ hình minh hoạ cho học sinh."
    }
  ]
}

with open("inputs/seeds/lop-9/hinh-hoc/lop-b/tuan07-on-tap-he-thuc-luong-tam-giac-vuong/on-tap-he-thuc-luong-tam-giac-vuong.json", "w") as f:
    json.dump(tuan7, f, ensure_ascii=False, indent=2)

tuan8 = {
  "slug": "luyen-tap-chung-minh-he-thuc",
  "title": "Luyện tập Chứng minh hệ thức trong tam giác vuông",
  "eyebrow": "CHỦ ĐỀ • HÌNH HỌC",
  "grade_label": "Lớp 9 • Ôn vào 10",
  "class_tier": "B",
  "stages": [
    {
      "kind": "review",
      "number": 1,
      "title": "Khám phá",
      "blocks": [
        {
          "type": "opener",
          "text": "Các bài toán chứng minh hệ thức luôn là thử thách lớn nhất trong đề thi Giữa Kì 1. Hãy cùng rèn luyện tư duy phân tích ngược từ kết luận về giả thiết để chinh phục dạng bài này.",
          "image": "images/opener.png"
        }
      ],
      "solution": "Khởi động tư duy.",
      "teacher_note": "Tạo động lực."
    },
    {
      "kind": "practice1",
      "number": 2,
      "title": "Luyện tập 1 — Vận dụng trực tiếp",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 1.",
          "statement": "\\emph{(Bài tập ôn cũ)} Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HE \\perp AB$ tại $E$, $HF \\perp AC$ tại $F$. Chứng minh rằng: $AE \\cdot AB = AF \\cdot AC$.",
          "tier": "onclass",
          "level": 2
        }
      ],
      "solution": "Dùng hệ thức lượng cho tam giác $AHB$ vuông tại $H$ có đường cao $HE$: $AE \\cdot AB = AH^2$.\nTương tự cho $\\Delta AHC$: $AF \\cdot AC = AH^2$. Từ đó suy ra đpcm.",
      "teacher_note": "Cầu nối kiến thức."
    },
    {
      "kind": "practice2",
      "number": 3,
      "title": "Luyện tập 2 — Biến đổi TSLG",
      "blocks": [
        {
          "type": "problem",
          "label": "Bài 2.",
          "statement": "\\emph{(Đề GK1 - Nguyễn Bỉnh Khiêm)} Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HE \\perp AB$ tại $E$, $HF \\perp AC$ tại $F$. Chứng minh rằng: $\\sin^2 B = \\frac{CF}{AC}$.",
          "tier": "onclass",
          "level": 3
        },
        {
          "type": "problem",
          "label": "Bài 3.",
          "statement": "\\emph{(Đề GK1 - Địch Vọng Hậu)} Cho tam giác $MNP$ vuông tại $M$, đường cao $MH$. Chứng minh rằng: $\\frac{NH}{PH} = \\left(\\frac{MN}{MP}\\right)^2$.",
          "tier": "home",
          "level": 3
        }
      ],
      "solution": "Bài 2: $CF = HC \\cdot \\cos C \\dots$ dùng hệ thức lượng suy ra đpcm.\nBài 3: $MN^2 = NH \\cdot NP$, $MP^2 = PH \\cdot NP$, lập tỉ số suy ra đpcm.",
      "teacher_note": "Phân tích ngược cho HS hiểu."
    }
  ]
}

with open("inputs/seeds/lop-9/hinh-hoc/lop-b/tuan08-luyen-tap-chung-minh-he-thuc/luyen-tap-chung-minh-he-thuc.json", "w") as f:
    json.dump(tuan8, f, ensure_ascii=False, indent=2)

