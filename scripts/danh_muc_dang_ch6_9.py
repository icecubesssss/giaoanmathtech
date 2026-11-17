#!/usr/bin/env python3
"""Danh mục dạng ĐÓNG chương VI Đại số 9 — phân dạng theo PHƯƠNG PHÁP (Thầy 16/11/2026).

Vì sao: tab "Phân dạng Ch.VI lớp 9C" có 385 tên dạng / 565 câu (agent viết chữ tự do, bài nhiều ý
ghép tên dạng, mức độ lệch nhau) ⇒ Pivot mảnh, không chọn được dạng để dạy.
Luật: một dạng = một phương pháp (một chuỗi bước). Bối cảnh, số liệu, hình thức = biến thể.
Thầy 16/11: đối xứng / bất đối xứng phải tách theo kiểu biến đổi; danh mục GIỮ cả dạng VDC (cho lớp
B, A sau này) nhưng lớp C không dạy VDC; P1 nhẩm nghiệm là câu NB.

Chạy:  .venv/bin/python scripts/danh_muc_dang_ch6_9.py [--ghi]
       ghi khoá `danh_muc_dang` vào config/khung-phan-dang/lop-9-dai-so-chuong-06.json
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-06.json"

# (mã, nhóm, cấp 1 ở tab "Danh mục dạng chuẩn", phiếu 9C, mức gốc, tên, cách làm, dấu hiệu)
# phiếu 9C: "P1".."P5" hoặc "ngoài 9C" (vẫn gán để không mất câu; dùng cho lớp B/A).
NHOM = {
    "N01": "PT bậc hai: nhận biết và giải",
    "N02": "PT bậc hai chứa tham số: biện luận theo Δ",
    "N03": "Viète cơ bản",
    "N04": "Viète: tính biểu thức đối xứng",
    "N05": "Viète: tìm m theo hệ thức đối xứng",
    "N06": "Viète: tính biểu thức không đối xứng",
    "N07": "Viète: tìm m theo hệ thức không đối xứng",
    "N08": "Viète nâng cao",
    "N09": "Phương trình quy về bậc hai",
    "N10": "Giải bài toán bằng cách lập phương trình bậc hai",
    "N11": "Hàm số y = ax² và parabol",
}

DANG = [
    # --- N01 ---
    ("VI-01", "N01", "D27", "P1", "NB", "Nhận biết phương trình bậc hai, chỉ ra hệ số a, b, c",
     "đưa về dạng ax² + bx + c = 0 → đọc a, b, c (a ≠ 0)", "là phương trình bậc hai không; xác định hệ số"),
    ("VI-02", "N01", "D27", "P1", "NB", "Tính Δ (Δ′), kết luận số nghiệm (không giải)",
     "a, b, c → Δ → so sánh với 0 → kết luận", "không giải, cho biết số nghiệm"),
    ("VI-03", "N01", "D27", "P1", "NB", "Giải phương trình khuyết b hoặc khuyết c",
     "khuyết c: đặt nhân tử chung x(ax + b) = 0; khuyết b: x² = −c/a", "ax² + bx = 0, ax² + c = 0, (x + m)² = k"),
    ("VI-04", "N01", "D27", "P1", "TH", "Giải phương trình bậc hai bằng công thức nghiệm (Δ hoặc Δ′)",
     "a, b, c → Δ (Δ′) → xét dấu → công thức nghiệm → kết luận",
     "hai nghiệm phân biệt, nghiệm kép, vô nghiệm, nghiệm xấu, hệ số chứa căn/thập phân"),
    ("VI-05", "N01", "D27", "P1", "NB", "Nhẩm nghiệm khi a + b + c = 0 hoặc a − b + c = 0",
     "tính a + b + c (a − b + c) → x₁ = ±1, x₂ = c/a (−c/a)", "tính nhẩm nghiệm, không tính Δ"),
    ("VI-06", "N01", "D27", "P1", "TH", "Biến đổi về dạng ax² + bx + c = 0 rồi giải",
     "khai triển, chuyển vế, thu gọn → VI-04", "phương trình có ngoặc, A² = B², phương trình tích bậc hai"),
    ("VI-07", "N01", "D27", "ngoài 9C", "NB", "Giải phương trình bậc hai bằng máy tính cầm tay",
     "nhập hệ số → đọc nghiệm (làm tròn nếu cần)", "máy tính cầm tay, nghiệm gần đúng"),
    # --- N02 ---
    ("VI-08", "N02", "D27", "P1", "TH", "Giải phương trình chứa tham số khi cho giá trị m cụ thể",
     "thay m → phương trình số → VI-04/VI-05", "giải phương trình khi m = …"),
    ("VI-09", "N02", "D27", "P1", "TH", "Tìm m để phương trình có nghiệm / hai nghiệm phân biệt / nghiệm kép / vô nghiệm",
     "Δ (Δ′) theo m → điều kiện (≥ 0, > 0, = 0, < 0) → giải bất phương trình/phương trình ẩn m",
     "hệ số a là số; tìm điều kiện của m để phương trình có nghiệm"),
    ("VI-10", "N02", "D27", "P1", "TH", "Chứng minh phương trình luôn có nghiệm / hai nghiệm phân biệt với mọi m",
     "Δ (Δ′) theo m → viết thành bình phương + số dương (hoặc ac < 0) → kết luận",
     "chứng minh với mọi giá trị của m"),
    ("VI-11", "N02", "D27", "P1", "TH", "Biết một nghiệm, tìm m (thay nghiệm vào phương trình)",
     "thay x = x₀ → phương trình ẩn m → tìm m (rồi nghiệm còn lại nếu hỏi)",
     "phương trình có một nghiệm bằng …, tìm m — không dùng Viète"),
    ("VI-12", "N02", "D27", "ngoài 9C", "VD", "Biện luận khi hệ số a chứa m",
     "xét a = 0 (bậc nhất) và a ≠ 0 (Δ) → gộp kết luận", "(m − 1)x² + …, mx² + …"),
    # --- N03 ---
    ("VI-13", "N03", "D28", "P2", "NB", "Kiểm điều kiện có nghiệm rồi tính tổng, tích hai nghiệm",
     "Δ ≥ 0 (hoặc ac < 0) → x₁ + x₂ = −b/a, x₁x₂ = c/a", "không giải, tính tổng và tích các nghiệm"),
    ("VI-14", "N03", "D28", "P2", "TH", "Biết một nghiệm, dùng Viète tìm nghiệm còn lại (và hệ số còn thiếu)",
     "x₂ = −b/a − x₁ (hoặc c/(a·x₁)) → hệ số = tích/tổng", "biết một nghiệm, tìm nghiệm còn lại bằng Viète"),
    ("VI-15", "N03", "D28", "P2", "TH", "Tìm hai số biết tổng và tích",
     "u, v là nghiệm của X² − SX + P = 0 → điều kiện S² ≥ 4P → giải",
     "tìm hai số u, v; kích thước hình chữ nhật biết chu vi và diện tích"),
    ("VI-16", "N03", "D28", "P2", "TH", "Lập phương trình bậc hai biết hai nghiệm (số cụ thể)",
     "tính tổng S, tích P → x² − Sx + P = 0", "lập phương trình có hai nghiệm là 8 và −3"),
    ("VI-17", "N03", "D28", "P2", "TH", "Xét dấu hai nghiệm của phương trình số (không giải)",
     "ac < 0 ⇒ trái dấu; Δ ≥ 0, P > 0, S > 0 (< 0) ⇒ cùng dương (âm)", "không giải, xét dấu các nghiệm"),
    # --- N04 ---
    ("VI-18", "N04", "D28", "P2", "TH", "Biểu thức đối xứng bậc hai: x₁² + x₂², x₁² + x₂² + k·x₁x₂",
     "Δ → Viète → x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂ → thay số", "tổng bình phương các nghiệm"),
    ("VI-19", "N04", "D28", "P2", "TH", "Tổng nghịch đảo 1/x₁ + 1/x₂ (và biểu thức có x₁x₂ ở mẫu)",
     "chứng minh x₁, x₂ ≠ 0 (c ≠ 0) → (x₁ + x₂)/(x₁x₂)", "tổng nghịch đảo hai nghiệm"),
    ("VI-20", "N04", "D28", "P2", "TH", "Biểu thức đối xứng bậc ba: x₁³ + x₂³, x₁²x₂ + x₁x₂²",
     "x₁³ + x₂³ = (x₁ + x₂)³ − 3x₁x₂(x₁ + x₂); x₁²x₂ + x₁x₂² = x₁x₂(x₁ + x₂)", "tổng lập phương các nghiệm"),
    ("VI-21", "N04", "D28", "P2", "TH", "Bình phương hiệu, hiệu hai nghiệm: (x₁ − x₂)², |x₁ − x₂|",
     "(x₁ − x₂)² = (x₁ + x₂)² − 4x₁x₂ → khai căn, xét dấu nếu cần", "bình phương của hiệu hai nghiệm"),
    ("VI-22", "N04", "D28", "P2", "TH", "Phân thức đối xứng cần quy đồng: x₁/x₂ + x₂/x₁, 1/(x₁ + a) + 1/(x₂ + a)",
     "quy đồng → tử, mẫu là biểu thức đối xứng → Viète", "x₁/x₂ + x₂/x₁, x₂/(x₁ + 3) + x₁/(x₂ + 3)"),
    ("VI-23", "N04", "D28", "P2", "TH", "Khai triển rồi đưa về đối xứng: (x₁ − 1)(x₂ − 1), x₁(1 − x₂) + x₂(1 − x₁)",
     "nhân phá ngoặc, thu gọn → biểu thức đối xứng → Viète",
     "biểu thức trông lệch nhưng khai triển ra đối xứng"),
    ("VI-24", "N04", "D28", "P2", "TH", "Biết một nghiệm (dạng căn) → tính biểu thức đối xứng",
     "Viète: x₂ = tổng − x₁ → hệ số → biểu thức đối xứng", "đề minh họa Sở: biết một nghiệm (3 − √5)/2, tính tổng bình phương"),
    ("VI-25", "N04", "D28", "ngoài 9C", "VD", "Biểu thức đối xứng bậc cao hoặc chứa căn của nghiệm",
     "tách theo lũy thừa nhỏ hơn / đặt √x₁ + √x₂ → Viète nhiều lần", "1/x₁⁴ + 1/x₂⁴, (x₁² + x₂²)/(√x₁ + √x₂)"),
    # --- N05 ---
    ("VI-26", "N05", "D28", "P2", "VD", "Tìm m để hai nghiệm thoả một đẳng thức đối xứng",
     "điều kiện có nghiệm (Δ theo m) → Viète theo m → thay vào hệ thức → giải phương trình ẩn m → đối chiếu",
     "tìm m để x₁² + x₂² = …, 1/x₁ + 1/x₂ = …"),
    ("VI-27", "N05", "D28", "ngoài 9C", "VD", "Tìm m để biểu thức đối xứng thoả một bất đẳng thức",
     "như VI-26 nhưng giải bất phương trình ẩn m, giao với điều kiện Δ", "x₁²x₂ + x₁x₂² ≥ 36"),
    ("VI-28", "N05", "D28", "P2", "TH", "Tìm m theo dấu nghiệm (trái dấu, cùng dương, cùng âm)",
     "trái dấu: ac < 0; cùng dấu: Δ ≥ 0, P > 0, S > 0 (< 0) → giải hệ điều kiện ẩn m",
     "tìm m để phương trình có hai nghiệm trái dấu / dương phân biệt"),
    ("VI-29", "N05", "D28", "P2", "VD", "Biểu thức (hệ thức) giữa hai nghiệm không phụ thuộc m",
     "Viète theo m → thay vào biểu thức → m triệt tiêu (hoặc khử m giữa tổng và tích)",
     "chứng minh giá trị biểu thức không phụ thuộc vào m"),
    # --- N06 ---
    ("VI-30", "N06", "D28", "P3", "VD", "Hạ bậc hai: thay x₁² theo x₁ rồi về Viète",
     "x₁ là nghiệm ⇒ ax₁² = −bx₁ − c → thay vào biểu thức → tổng/tích", "A = x₁² + 3x₂, x₁(x₁ − 1/2) + …"),
    ("VI-31", "N06", "D28", "P3", "VD", "Hạ bậc ba: x₁³ theo x₁ rồi về Viète",
     "x₁² = … ⇒ x₁³ = x₁·x₁² = … → thay vào biểu thức", "H = x₁³ + 10x₂ + 1992, x₁³ − 10x₁ + …"),
    ("VI-32", "N06", "D28", "P3", "VD", "Biểu thức chứa |x|, √ của một nghiệm: xét dấu rồi biến đổi",
     "xét dấu hai nghiệm (tích, tổng) → bỏ dấu |·| / đưa về √(A²) = |A| → Viète", "|x₁| − |x₂|, √(−16x₁ + 5) − x₂"),
    # --- N07 ---
    ("VI-33", "N07", "D28", "P3", "VD", "Tìm m theo hệ thức bậc nhất không đối xứng (a·x₁ + b·x₂ = c, x₁ = k·x₂)",
     "điều kiện Δ → ghép hệ thức với x₁ + x₂ → giải hệ tìm x₁, x₂ → thay vào x₁x₂ → m → đối chiếu",
     "x₁ − 2x₂ = 6, 2x₁ + 3x₂ = 1, nghiệm này gấp 4 lần nghiệm kia"),
    ("VI-34", "N07", "D28", "P3", "VD", "Tìm m (hoặc tham số) theo hệ thức không đối xứng bằng hạ bậc",
     "thay x₁² (x₂²) theo phương trình → hệ thức về đối xứng → Viète → m", "đề Sở 2025: (70 − mx₁²)/x₂ = x₁ + mx₂"),
    ("VI-35", "N07", "D28", "ngoài 9C", "VDC", "Tìm m theo hệ thức chứa |x| hoặc √ của nghiệm",
     "xét dấu nghiệm theo m → bỏ |·|, bình phương → Viète → đối chiếu", "√x₁ = √(2x₂), |x₁| − |x₂| = −6"),
    # --- N08 ---
    ("VI-36", "N08", "D28", "ngoài 9C", "VDC", "Cực trị biểu thức của hai nghiệm theo m",
     "Viète theo m → biểu thức theo m → hằng đẳng thức tìm GTLN/GTNN → đối chiếu điều kiện Δ",
     "tìm m để x₁² + x₂² nhỏ nhất"),
    ("VI-37", "N08", "D28", "ngoài 9C", "VDC", "So sánh nghiệm với một số (x₁ < α < x₂, x₁ ≤ x₂ < α)",
     "đặt t = x − α / xét (x₁ − α)(x₂ − α) → Viète → điều kiện", "x₁ < 1 < x₂"),
    ("VI-38", "N08", "D28", "ngoài 9C", "VDC", "Nghiệm nguyên, tự nhiên, nguyên tố",
     "Viète → khử m → phương trình nghiệm nguyên / xét ước", "hai nghiệm là các số nguyên tố"),
    ("VI-39", "N08", "D28", "ngoài 9C", "VD", "Lập phương trình có hai nghiệm là biểu thức của x₁, x₂",
     "tính tổng, tích hai nghiệm mới qua Viète → X² − SX + P = 0", "hai nghiệm là 2x₁ − x₂ và 2x₂ − x₁"),
    ("VI-40", "N08", "D28", "ngoài 9C", "TH", "Câu lý thuyết SGK: chứng minh công thức nghiệm, Viète, phân tích tam thức",
     "theo các bước SGK", "hoạt động, chứng tỏ ax² + bx + c = a(x − x₁)(x − x₂)"),
    # --- N09 ---
    ("VI-41", "N09", "D08", "P4", "TH", "Phương trình chứa ẩn ở mẫu quy về bậc hai",
     "ĐKXĐ → quy đồng, khử mẫu → ax² + bx + c = 0 → giải → đối chiếu ĐKXĐ", "ẩn ở mẫu"),
    ("VI-42", "N09", "D27", "ngoài 9C", "VD", "Phương trình trùng phương, đặt ẩn phụ, phương trình chứa căn",
     "đặt t = x² (t ≥ 0) / ẩn phụ → bậc hai theo t → trả về x", "x⁴, đặt ẩn phụ, căn thức"),
    # --- N10 ---
    ("VI-43", "N10", "D29", "P4", "TH", "Lập phương trình bậc hai: chuyển động",
     "ẩn + điều kiện → bảng s, v, t → quan hệ thời gian → phương trình → giải → đối chiếu → trả lời",
     "chênh thời gian, đi và về, nghỉ giữa đường, xuôi ngược dòng"),
    ("VI-44", "N10", "D29", "P4", "TH", "Lập phương trình bậc hai: năng suất, kế hoạch",
     "ẩn → bảng khối lượng, năng suất, thời gian (số xe, số ghế…) → quan hệ → phương trình → giải → trả lời",
     "xong sớm, vượt mức, bớt xe/thêm xe, chia đều, xếp ghế"),
    ("VI-45", "N10", "D29", "P4", "VD", "Lập phương trình bậc hai: làm chung, làm riêng",
     "ẩn = thời gian làm riêng → phần việc trong 1 giờ (1/t) → tổng phần việc → phương trình",
     "hai người/hai vòi làm chung, làm riêng"),
    ("VI-46", "N10", "D29", "P4", "TH", "Lập phương trình bậc hai: hình học",
     "ẩn = một kích thước → biểu diễn kích thước còn lại → công thức diện tích/chu vi/Pythagore → phương trình",
     "hình chữ nhật, tam giác vuông, thể tích hình hộp"),
    ("VI-47", "N10", "D29", "P4", "TH", "Lập phương trình bậc hai: dạng khác (%, số, nồng độ, mô hình cho sẵn công thức)",
     "ẩn → quan hệ theo đề → phương trình → giải → trả lời", "phần trăm, tìm số, khối lượng riêng, doanh thu"),
    # --- N11 ---
    ("VI-48", "N11", "D25", "ngoài 9C", "TH", "Hàm số y = ax²: bảng giá trị, đồ thị, điểm thuộc, tìm a, bài thực tế",
     "thay toạ độ / lập bảng / vẽ parabol", "y = ax², parabol, rơi tự do"),
    ("VI-49", "N11", "D26", "ngoài 9C", "TH", "Parabol và đường thẳng: giao điểm, tiếp xúc",
     "phương trình hoành độ giao điểm → giải / Δ = 0", "(P) cắt (d) — KHÔNG gồm ý Viète trên hoành độ (gán dạng Viète tương ứng)"),
]


# Thầy 16/11 (lượt 4): 49 mã trên vẫn mảnh ⇒ đó là KỸ THUẬT; gộp thành DẠNG (tiêu chí: chỉ tách khi biết làm
# dạng này vẫn KHÔNG tự làm được dạng kia; khác công thức cần nhớ = cùng dạng). 9C 18 dạng, ngoài 9C 10 dạng.
# (mã dạng, tên dạng, phiếu 9C, [kỹ thuật])
DANG_GOP = [
    ("C6-01", "Giải phương trình bậc hai bằng công thức nghiệm (đọc hệ số, tính Δ là bước NB)", "P1",
     ["VI-01", "VI-02", "VI-04", "VI-06", "VI-08"]),
    ("C6-02", "Giải phương trình khuyết b hoặc khuyết c", "P1", ["VI-03"]),
    ("C6-03", "Nhẩm nghiệm a + b + c = 0, a − b + c = 0", "P1", ["VI-05"]),
    ("C6-04", "Tìm m để phương trình có nghiệm / hai nghiệm phân biệt / nghiệm kép / vô nghiệm", "P1", ["VI-09"]),
    ("C6-05", "Chứng minh phương trình luôn có nghiệm với mọi m", "P1", ["VI-10"]),
    ("C6-06", "Biết một nghiệm: tìm hệ số, nghiệm còn lại", "P1", ["VI-11", "VI-14"]),
    ("C6-07", "Tính giá trị biểu thức đối xứng của hai nghiệm", "P2",
     ["VI-13", "VI-18", "VI-19", "VI-20", "VI-21", "VI-22", "VI-23"]),
    ("C6-08", "Biết một nghiệm dạng căn → tính biểu thức đối xứng", "P2", ["VI-24"]),
    ("C6-09", "Tìm hai số biết tổng và tích; lập phương trình biết hai nghiệm", "P2", ["VI-15", "VI-16"]),
    ("C6-10", "Xét dấu hai nghiệm (phương trình số hoặc theo m)", "P2", ["VI-17", "VI-28"]),
    ("C6-11", "Tìm m để hai nghiệm thoả hệ thức đối xứng", "P2", ["VI-26"]),
    ("C6-12", "Hệ thức giữa hai nghiệm không phụ thuộc m", "P2", ["VI-29"]),
    ("C6-13", "Hạ bậc: tính biểu thức không đối xứng (bậc 2 là TH, bậc 3 là VD)", "P3", ["VI-30", "VI-31"]),
    ("C6-14", "Biểu thức chứa |x|, căn của một nghiệm (xét dấu rồi biến đổi)", "P3", ["VI-32"]),
    ("C6-15", "Tìm m theo hệ thức bậc nhất không đối xứng", "P3", ["VI-33"]),
    ("C6-16", "Tìm m theo hệ thức không đối xứng bằng hạ bậc", "P3", ["VI-34"]),
    ("C6-17", "Phương trình chứa ẩn ở mẫu quy về bậc hai", "P4", ["VI-41"]),
    ("C6-18", "Giải bài toán bằng cách lập phương trình bậc hai (bối cảnh ở cột Biến thể)", "P4",
     ["VI-43", "VI-44", "VI-45", "VI-46", "VI-47"]),
    ("C6-19", "Giải phương trình bậc hai bằng máy tính cầm tay", "ngoài 9C", ["VI-07"]),
    ("C6-20", "Biện luận khi hệ số a chứa m", "ngoài 9C", ["VI-12"]),
    ("C6-21", "Biểu thức đối xứng bậc cao hoặc chứa căn của nghiệm", "ngoài 9C", ["VI-25"]),
    ("C6-22", "Tìm m để biểu thức đối xứng thoả bất đẳng thức", "ngoài 9C", ["VI-27"]),
    ("C6-23", "Viète nâng cao (VDC): hệ thức có |x|/căn theo m, cực trị, so sánh nghiệm, nghiệm nguyên", "ngoài 9C",
     ["VI-35", "VI-36", "VI-37", "VI-38"]),
    ("C6-24", "Lập phương trình có hai nghiệm là biểu thức của x₁, x₂", "ngoài 9C", ["VI-39"]),
    ("C6-25", "Câu lý thuyết SGK (chứng minh công thức nghiệm, Viète, phân tích tam thức)", "ngoài 9C", ["VI-40"]),
    ("C6-26", "Phương trình trùng phương, đặt ẩn phụ, chứa căn", "ngoài 9C", ["VI-42"]),
    ("C6-27", "Hàm số y = ax² và đồ thị", "ngoài 9C", ["VI-48"]),
    ("C6-28", "Parabol và đường thẳng", "ngoài 9C", ["VI-49"]),
]


def danh_muc():
    out = []
    for ma, nhom, cap1, phieu, muc, ten, cach, dau_hieu in DANG:
        assert nhom in NHOM, ma
        out.append({"ma": ma, "nhom": nhom, "ten_nhom": NHOM[nhom], "cap1": cap1, "phieu_9c": phieu,
                    "muc_goc": muc, "ten": ten, "cach_lam": cach, "dau_hieu": dau_hieu})
    mas = [d["ma"] for d in out]
    assert len(mas) == len(set(mas))
    ve = {kt: g[0] for g in DANG_GOP for kt in g[3]}
    assert sorted(ve) == sorted(mas), set(mas) ^ set(ve)  # mỗi kỹ thuật thuộc đúng một dạng
    for d in out:
        d["dang"] = ve[d["ma"]]
        assert (d["phieu_9c"] == "ngoài 9C") == (dict((g[0], g[2]) for g in DANG_GOP)[d["dang"]] == "ngoài 9C"), d["ma"]
    return out


def main():
    dm = danh_muc()
    khung = json.loads(KHUNG.read_text(encoding="utf-8"))
    khung["danh_muc_dang"] = {
        "_mo_ta": "Thầy 16/11/2026: phân dạng theo PHƯƠNG PHÁP; mỗi ý một mã; sinh bởi scripts/danh_muc_dang_ch6_9.py",
        "nhom": NHOM, "dang": dm,
        "dang_gop": [{"ma": m, "ten": t, "phieu_9c": p, "ky_thuat": k} for m, t, p, k in DANG_GOP],
    }
    print(f"{len(dm)} kỹ thuật / {len(DANG_GOP)} dạng ({sum(g[2] != 'ngoài 9C' for g in DANG_GOP)} dạng 9C) / {len(NHOM)} nhóm")
    if "--ghi" in sys.argv:
        KHUNG.write_text(json.dumps(khung, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Đã ghi", KHUNG.relative_to(REPO))


if __name__ == "__main__":
    main()
