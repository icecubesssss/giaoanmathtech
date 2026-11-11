#!/usr/bin/env python3
"""Sinh Đề 2, Đề 3 CK1 Toán 4 theo barem đề trung tâm (8 TN × 0,5 + TL 1,5/2/2/0,5), khung trang lấy từ Đề 1.

Câu bốc từ đề TRƯỜNG THẬT trong ngân hàng (inputs/refs/ngan-hang-sheet/tieu-hoc/lop-4/ban-ghi), nguồn ghi ở lời giải GV.
    .venv/bin/python scripts/de_ck1_lop4.py
"""
import copy, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "inputs/seeds/lop-4/de-cuoi-ki-1"
BASE = json.loads((DIR / "de-kiem-tra-cuoi-ki-1-de-1.json").read_text(encoding="utf-8"))


def tn(label, level, stmt, opts, ans, sol, src):
    return {"type": "problem", "label": label, "level": level, "statement": stmt + "\\par\\vspace{2pt}",
            "options": opts, "answer": ans, "solution": sol + f" \\textit{{(Nguồn: {src}.)}}", "tier": "onclass"}


def tl(label, level, diem, stmt, sol, src):
    return {"type": "problem", "label": label, "level": level, "statement": f"\\textbf{{({diem} điểm)}} " + stmt,
            "solution": sol + f" [[br]] \\textit{{(Nguồn: {src}.)}}", "tier": "onclass"}


def ds(label, level, stmt, items, ans, sol, src):
    """Câu Đúng/Sai: mỗi ý một dòng có ô vuông."""
    body = " [[br]] ".join(f"{chr(97 + i)}) {x} \\hfill $\\square$" for i, x in enumerate(items))
    return {"type": "problem", "label": label, "level": level, "statement": stmt + " [[br]] " + body, "answer": ans,
            "solution": sol + f" \\textit{{(Nguồn: {src}.)}}", "tier": "onclass"}


def hai_cot(a, b):
    return ("[[br]]\n\\noindent\\begin{minipage}[t]{0.48\\linewidth}\n\\textbf{a)} " + a +
            "\n\\end{minipage}\\hfill\n\\begin{minipage}[t]{0.48\\linewidth}\n\\textbf{b)} " + b + "\n\\end{minipage}")


def dung(so, tns, b1, b2, b3, b4, kiem, p1=6):
    """p1 = số câu TN ở trang 1 (5 khi đáp án dài làm tràn trang)."""
    d = copy.deepcopy(BASE)
    if isinstance(so, int):
        d["slug"] = f"de-kiem-tra-cuoi-ki-1-de-{so}"
        d["title"] = f"Đề kiểm tra cuối học kì I — Đề {so} (40 phút)"
    else:  # "on1".."on3" = đề ôn tập
        d["slug"] = f"de-on-tap-cuoi-ki-1-so-{so[2:]}"
        d["title"] = f"Đề ôn tập cuối học kì I — Đề ôn số {so[2:]} (40 phút)"
        d["eyebrow"] = "ĐỀ ÔN TẬP CUỐI HỌC KÌ I · TOÁN 4 · NĂM HỌC 2026 – 2027"
    s = d["stages"]
    s[0]["blocks"] = s[0]["blocks"][:2] + tns[:p1] + [{"type": "para", "text": "\\newpage"}]
    blk = s[1]["blocks"]
    oly = dict(blk[4], count=blk[4]["count"] - 2 * (6 - p1))
    s[1]["blocks"] = tns[p1:8] + [blk[2], b1, oly] + blk[5:]
    blk = s[2]["blocks"]
    s[2]["blocks"] = [b2, blk[1], b3] + blk[3:]
    blk = s[3]["blocks"]
    s[3]["blocks"] = [blk[0], b4] + blk[2:]
    r = s[4]["blocks"]
    r[0] = dict(r[0], text=r[0]["text"].split("\\begin{tabular}")[0] + "\\begin{tabular}{p{7.5cm}p{7.5cm}}\n" + kiem + "\n\\end{tabular}\n\\end{tcolorbox}")
    (DIR / (d["slug"] + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("✓ Đề", so)


HQ = "Đề CK1 TH Hồng Quang, Ứng Hòa, Hà Nội 2024-2025"
# ---------------- ĐỀ 2
dung(2, [
    tn("Câu 1.", 1, "Số $38\\,189\\,000$ được đọc là:", ["Ba mươi tám nghìn một trăm tám mươi chín", "Ba mươi tám triệu một trăm tám mươi chín", "Ba mươi tám triệu một trăm chín mươi tám", "Ba mươi tám triệu một trăm tám mươi chín nghìn"], "D",
       "Chọn \\textbf{D}. Tách lớp: $38 \\mid 189 \\mid 000$ — lớp triệu là $38$, lớp nghìn là $189$, lớp đơn vị là $000$.", "Đề CK1 TH Tân Liễu, Bắc Giang 2024-2025"),
    tn("Câu 2.", 1, "Trong số $34\\,652\\,471$, chữ số $3$ thuộc hàng nào, lớp nào?", ["Hàng trăm, lớp đơn vị", "Hàng nghìn, lớp nghìn", "Hàng trăm nghìn, lớp nghìn", "Hàng chục triệu, lớp triệu"], "D",
       "Chọn \\textbf{D}. $34 \\mid 652 \\mid 471$: chữ số $3$ đứng đầu lớp triệu có hai chữ số nên thuộc hàng chục triệu.", "Đề CK1 TH Phúc Ninh, Tuyên Quang 2024-2025; TH Hùng Lợi 1"),
    tn("Câu 3.", 1, "Nhà toán học Lê Văn Thiêm là tiến sĩ toán học đầu tiên của Việt Nam, ông sinh năm $1917$. Năm $1917$ thuộc thế kỉ:", ["XIX", "XV", "XX", "XXI"], "C",
       "Chọn \\textbf{C}. Thế kỉ XX gồm các năm từ $1901$ đến $2000$.", "Đề CK1 TH Hùng Lợi 1, Tuyên Quang 2024-2025"),
    tn("Câu 4.", 1, "Số $12\\,346\\,700$ làm tròn đến hàng trăm nghìn là:", ["$12\\,340\\,000$", "$12\\,440\\,000$", "$12\\,300\\,000$", "$12\\,350\\,000$"], "C",
       "Chọn \\textbf{C}. Chữ số hàng chục nghìn là $4 < 5$ nên giữ nguyên hàng trăm nghìn: $12\\,300\\,000$.", "Đề CK1 TH Hải Long, Nam Định 2024-2025"),
    tn("Câu 5.", 2, "$3$ tấn $50$ kg $= \\dots$ kg. Số cần điền vào chỗ chấm là:", ["$3\\,050$", "$300\\,050$", "$350$", "$30\\,050$"], "A",
       "Chọn \\textbf{A}. $3$ tấn $= 3\\,000$ kg nên $3$ tấn $50$ kg $= 3\\,050$ kg.", "Đề CK1 TH Tiên Phú 2025-2026"),
    tn("Câu 6.", 2, "Lúc $9$ giờ đúng, góc tạo bởi kim giờ và kim phút có số đo là:", ["$70^\\circ$", "$60^\\circ$", "$90^\\circ$", "$360^\\circ$"], "C",
       "Chọn \\textbf{C}. Lúc $9$ giờ, kim phút chỉ số $12$, kim giờ chỉ số $9$: hai kim tạo thành góc vuông ($90^\\circ$).", "Đề CK1 TH Vĩnh Bảo, Hải Phòng 2025-2026"),
    tn("Câu 7.", 2, "Giá trị của biểu thức $a \\times b + 567$ với $a = 11$ và $b = 9$ là:", ["$789$", "$678$", "$666$", "$782$"], "C",
       "Chọn \\textbf{C}. $11 \\times 9 + 567 = 99 + 567 = 666$.", "Đề CK1 TH Tân Liễu, Bắc Giang 2024-2025"),
    tn("Câu 8.", 3, "Tổng của hai số lẻ liên tiếp là số bé nhất có bốn chữ số. Hai số đó là:", ["$489$ và $501$", "$498$ và $502$", "$499$ và $501$", "$497$ và $503$"], "C",
       "Chọn \\textbf{C}. Số bé nhất có bốn chữ số là $1\\,000$; hai số lẻ liên tiếp hơn kém nhau $2$. Số lớn: $(1\\,000 + 2) : 2 = 501$, số bé: $499$.", "Đề CK1 TH Đồng Hòa, Hải Phòng 2025-2026"),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$274\\,806 + 351\\,457$", "$167\\,285 - 96\\,546$"),
      "\\textbf{a) (0,75đ)} $274\\,806 + 351\\,457 = 626\\,263$. [[br]] \\textbf{b) (0,75đ)} $167\\,285 - 96\\,546 = 70\\,739$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ.", HQ),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$2\\,023 + 1\\,736 - 23 + 1\\,264$", "$1\\,537 + 576 - 537 + 424$"),
      "\\textbf{a) (1,0đ)} $= (2\\,023 - 23) + (1\\,736 + 1\\,264) = 2\\,000 + 3\\,000 = 5\\,000$. [[br]] \\textbf{b) (1,0đ)} $= (1\\,537 - 537) + (576 + 424) = 1\\,000 + 1\\,000 = 2\\,000$. [[br]] \\textit{Nhóm đúng $0,5$đ, kết quả đúng $0,5$đ mỗi ý.}", "a) TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025; b) TH Trần Quốc Toản, Đắk Lắk 2025-2026"),
   tl("Bài 3.", 2, "2,0", "Một mảnh vườn hình chữ nhật có nửa chu vi là $24$ m, chiều dài hơn chiều rộng $8$ m. Tính diện tích mảnh vườn đó.",
      "Chiều dài mảnh vườn là: $(24 + 8) : 2 = 16$ (m) \\hfill \\textit{(0,75đ)} [[br]] Chiều rộng mảnh vườn là: $16 - 8 = 8$ (m) \\hfill \\textit{(0,5đ)} [[br]] Diện tích mảnh vườn là: $16 \\times 8 = 128$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] Đáp số: $128$ m$^2$. \\hfill \\textit{(0,25đ)} [[br]] \\textit{Bẫy: chia đôi $24$ thêm một lần nữa (đề đã cho NỬA chu vi).}", HQ),
   tl("Bài 4.", 3, "0,5", "Để cắt một tấm vải dài $20$ m thành các mảnh vải dài $2$ m thì phải cắt bao nhiêu lần? [[br]] \\textit{Trả lời:} Phải cắt \\makebox[3.2cm]{\\dotfill} lần.",
      "Tấm vải được chia thành $20 : 2 = 10$ mảnh. Cắt $1$ lần được $2$ mảnh, mỗi lần cắt thêm được thêm $1$ mảnh, nên số lần cắt là $10 - 1 = 9$ (lần). \\hfill \\textit{(0,5đ)} [[br]] \\textit{Bẫy: trả lời $10$ lần.}", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề B)"),
   "$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã khoanh đủ 8 câu trắc nghiệm \\\\\n$\\square$ Đã đặt tính thẳng cột (Bài 1) & $\\square$ Đã nhóm số tròn nghìn (Bài 2) \\\\\n$\\square$ Đã đọc kĩ \\textit{nửa chu vi} (Bài 3) & $\\square$ Đã ghi đơn vị m$^2$ và đáp số", p1=5)

# ---------------- ĐỀ 3
dung(3, [
    tn("Câu 1.", 1, "Số \"Tám trăm hai mươi ba nghìn không trăm mười tám\" viết là:", ["$812\\,308$", "$823\\,108$", "$832\\,008$", "$823\\,018$"], "D",
       "Chọn \\textbf{D}. Lớp nghìn là $823$, lớp đơn vị là \"không trăm mười tám\" $= 018$: viết là $823\\,018$.", "Đề CK1 TH Hải Long 2024-2025; TH Tiên Phú 2025-2026"),
    tn("Câu 2.", 1, "Trong các số dưới đây, số có chữ số $3$ mang giá trị $3\\,000$ là:", ["$36\\,512$", "$54\\,312$", "$53\\,724$", "$54\\,832$"], "C",
       "Chọn \\textbf{C}. Trong $53\\,724$, chữ số $3$ ở hàng nghìn nên có giá trị $3\\,000$.", "Đề CK1 TH Tân Thuận 1 2025-2026"),
    tn("Câu 3.", 1, "$7$ tạ $3$ kg $= \\dots$ kg. Số thích hợp điền vào chỗ chấm là:", ["$73$", "$703$", "$730$", "$7\\,003$"], "B",
       "Chọn \\textbf{B}. $7$ tạ $= 700$ kg nên $7$ tạ $3$ kg $= 703$ kg.", "Đề CK1 TH Hùng Lợi 1, Tuyên Quang 2024-2025"),
    tn("Câu 4.", 1, "Làm tròn số $73\\,523\\,625$ đến hàng trăm nghìn ta được số:", ["$73\\,500\\,000$", "$73\\,600\\,000$", "$73\\,400\\,000$", "$73\\,520\\,000$"], "A",
       "Chọn \\textbf{A}. Chữ số hàng chục nghìn là $2 < 5$ nên giữ nguyên: $73\\,500\\,000$.", "Đề CK1 TH Hùng Lợi 1, Tuyên Quang 2024-2025"),
    tn("Câu 5.", 2, "Chiều dài phòng học lớp em khoảng:", ["$80$ dm", "$80$ m", "$800$ mm", "$8$ dm"], "A",
       "Chọn \\textbf{A}. $80$ dm $= 8$ m, phù hợp với chiều dài một phòng học.", "Đề CK1 TH Liên Bảo 2025-2026"),
    tn("Câu 6.", 2, "Phát biểu nào dưới đây là \\textbf{sai} về hình thoi?", ["Hình thoi có bốn góc vuông", "Hình thoi có bốn cạnh bằng nhau", "Hình thoi có hai cặp cạnh đối diện song song", "Hình thoi là một tứ giác"], "A",
       "Chọn \\textbf{A}. Hình thoi có bốn cạnh bằng nhau và hai cặp cạnh đối diện song song, nhưng nói chung không có góc vuông.", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề B)"),
    tn("Câu 7.", 2, "Giá trị của biểu thức $24 : (7 - m)$ với $m = 1$ là:", ["$6$", "$4$", "$2$", "$3$"], "B",
       "Chọn \\textbf{B}. $24 : (7 - 1) = 24 : 6 = 4$. Tính trong ngoặc trước.", "Đề CK1 TH Tân Liễu, Bắc Giang 2024-2025 (đề B)"),
    tn("Câu 8.", 3, "Năm $1996$, cả nước kỉ niệm $200$ năm ngày sinh của Đại thi hào Nguyễn Du. Vậy Nguyễn Du sinh vào thế kỉ:", ["XX", "XIX", "XVII", "XVIII"], "D",
       "Chọn \\textbf{D}. Nguyễn Du sinh năm $1996 - 200 = 1796$, thuộc thế kỉ XVIII (từ $1701$ đến $1800$).", "Đề CK1 TH Liên Bảo 2025-2026"),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$425\\,684 + 138\\,230$", "$968\\,531 - 176\\,340$"),
      "\\textbf{a) (0,75đ)} $425\\,684 + 138\\,230 = 563\\,914$. [[br]] \\textbf{b) (0,75đ)} $968\\,531 - 176\\,340 = 792\\,191$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ.", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề A)"),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$29\\,100 + 35\\,487 - 19\\,100 - 5\\,487$", "$59\\,000 - 2\\,406 - 6\\,594$"),
      "\\textbf{a) (1,0đ)} $= (29\\,100 - 19\\,100) + (35\\,487 - 5\\,487) = 10\\,000 + 30\\,000 = 40\\,000$. [[br]] \\textbf{b) (1,0đ)} $= 59\\,000 - (2\\,406 + 6\\,594) = 59\\,000 - 9\\,000 = 50\\,000$.", "Đề CK1 TH Liên Bảo 2025-2026"),
   tl("Bài 3.", 2, "2,0", "Một mảnh vườn hình chữ nhật có nửa chu vi bằng $28$ m. Tính diện tích mảnh vườn đó, biết chiều rộng kém chiều dài $10$ m.",
      "Chiều dài mảnh vườn là: $(28 + 10) : 2 = 19$ (m) \\hfill \\textit{(0,75đ)} [[br]] Chiều rộng mảnh vườn là: $19 - 10 = 9$ (m) \\hfill \\textit{(0,5đ)} [[br]] Diện tích mảnh vườn là: $19 \\times 9 = 171$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] Đáp số: $171$ m$^2$. \\hfill \\textit{(0,25đ)}", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề B)"),
   tl("Bài 4.", 3, "0,5", "Cho dãy số: $1; 4; 7; 10; \\dots; 100$. Dãy số trên có bao nhiêu số? [[br]] \\textit{Trả lời:} Dãy số có \\makebox[3.2cm]{\\dotfill} số.",
      "Hai số liền nhau hơn kém nhau $3$ đơn vị. Số các số là: $(100 - 1) : 3 + 1 = 34$ (số). \\hfill \\textit{(0,5đ)}", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề B)"),
   "$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã khoanh đủ 8 câu trắc nghiệm \\\\\n$\\square$ Đã đặt tính thẳng cột (Bài 1) & $\\square$ Đã nhóm số tròn chục nghìn (Bài 2) \\\\\n$\\square$ Đã đọc kĩ \\textit{chiều rộng kém chiều dài} (Bài 3) & $\\square$ Đã ghi đơn vị m$^2$ và đáp số")

# =====================================================================
# ĐỀ 1 (dựng lại 11/11: 100% câu bốc từ đề trường, ghi nguồn) + 3 ĐỀ ÔN TẬP
# Không câu nào trùng Đề 2, Đề 3. "Phỏng theo" = đổi số liệu, ghi rõ trong nguồn.
# =====================================================================
DC = "Đề CK1 TH Đồng Cấm, Hải Phòng 2025-2026"
TH_ = "Đề CK1 TH Tây Hưng, Hải Phòng 2025-2026"
MK = "Đề CK1 TH Minh Khôi 2025-2026"
DH = "Đề CK1 TH Đồng Hòa, Kiến An, Hải Phòng 2025-2026"
DT = "Đề GK1 TH Đồng Thái, An Hải, Hải Phòng 2025-2026"
YT = "Đề CK1 TH Yên Thọ, Đông Triều, Quảng Ninh 2023-2024"
KS = "Đề CK1 TH Kim Sơn, Đông Triều, Quảng Ninh 2023-2024"
HL1 = "Đề CK1 TH Hùng Lợi 1, Yên Sơn, Tuyên Quang 2024-2025"
HLg = "Đề CK1 TH Hải Long, Hải Hậu, Nam Định 2024-2025"
PN = "Đề CK1 TH Phúc Ninh, Tuyên Quang 2024-2025"
VB = "Đề CK1 TH Vĩnh Bảo, Hải Phòng 2025-2026"
KIEM = ("$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã khoanh đủ 8 câu trắc nghiệm \\\\\n"
        "$\\square$ Đã đặt tính thẳng cột (Bài 1) & $\\square$ Đã nhóm các số tròn (Bài 2) \\\\\n")

# ---------------- ĐỀ 1 (chính thức, dựng lại)
dung(1, [
    tn("Câu 1.", 1, "Số $38\\,000\\,189$ được đọc là:", ["Ba mươi tám nghìn một trăm tám mươi chín", "Ba mươi tám triệu một trăm tám mươi chín nghìn", "Ba mươi tám triệu không nghìn một trăm tám mươi chín", "Ba mươi tám triệu một trăm tám mươi chín nghìn đơn vị"], "C",
       "Chọn \\textbf{C}. Tách lớp: $38 \\mid 000 \\mid 189$ — lớp triệu $38$, lớp nghìn $000$ (đọc \"không nghìn\"), lớp đơn vị $189$.", DC),
    tn("Câu 2.", 1, "Trong số $398\\,105\\,462$, chữ số $5$ thuộc hàng nào, lớp nào?", ["Hàng nghìn, lớp nghìn", "Hàng chục, lớp đơn vị", "Hàng triệu, lớp triệu", "Hàng đơn vị, lớp đơn vị"], "A",
       "Chọn \\textbf{A}. $398 \\mid 105 \\mid 462$: chữ số $5$ đứng cuối lớp nghìn nên thuộc hàng nghìn.", "Đề CK1 TH Trần Quốc Toản, Eadrông, Đắk Lắk 2025-2026"),
    tn("Câu 3.", 1, "Năm $2024$ thuộc thế kỉ nào?", ["Thế kỉ XIX", "Thế kỉ XX", "Thế kỉ XXI", "Thế kỉ XXII"], "C",
       "Chọn \\textbf{C}. Thế kỉ XXI gồm các năm từ $2001$ đến $2100$.", MK + " (đề A)"),
    tn("Câu 4.", 1, "Làm tròn số $12\\,645\\,300$ đến hàng trăm nghìn ta được số:", ["$12\\,600\\,000$", "$12\\,700\\,000$", "$12\\,640\\,000$", "$12\\,645\\,000$"], "A",
       "Chọn \\textbf{A}. Chữ số hàng chục nghìn là $4 < 5$ nên giữ nguyên hàng trăm nghìn: $12\\,600\\,000$.", "Đề CK1 TH Liên Bảo 2025-2026 (đề chính thức)"),
    tn("Câu 5.", 2, "$4$ tấn $2$ tạ $= \\dots$ yến. Số thích hợp điền vào chỗ chấm là:", ["$4\\,200$", "$420$", "$402$", "$4\\,002$"], "B",
       "Chọn \\textbf{B}. $4$ tấn $2$ tạ $= 42$ tạ $= 420$ yến. \\textit{Bẫy: đổi ra kg ($4\\,200$) rồi quên đổi sang yến.}", TH_),
    tn("Câu 6.", 2, "Góc có số đo $120^\\circ$ là:", ["Góc nhọn", "Góc vuông", "Góc tù", "Góc bẹt"], "C",
       "Chọn \\textbf{C}. $90^\\circ < 120^\\circ < 180^\\circ$ nên đó là góc tù.", TH_),
    tn("Câu 7.", 2, "Giá trị của biểu thức $a \\times 234 + b$, với $a$ là số lớn nhất có một chữ số và $b$ là số bé nhất có hai chữ số, là:", ["$2\\,106$", "$2\\,116$", "$2\\,340$", "$2\\,350$"], "B",
       "Chọn \\textbf{B}. $a = 9$, $b = 10$: $9 \\times 234 + 10 = 2\\,106 + 10 = 2\\,116$.", "Đề CK1 TH\\&THCS Chu Văn An, Ea Súp, Đắk Lắk 2024-2025 (chuyển sang trắc nghiệm)"),
    tn("Câu 8.", 3, "Nếu viết thêm chữ số $9$ vào bên trái một số có sáu chữ số thì được số mới lớn hơn số đã cho bao nhiêu đơn vị?", ["$9$", "$900\\,000$", "$9\\,000\\,000$", "$90\\,000\\,000$"], "C",
       "Chọn \\textbf{C}. Số mới có bảy chữ số, chữ số $9$ đứng ở hàng triệu nên số mới bằng $9\\,000\\,000$ cộng với số đã cho.", DH + " (chuyển sang trắc nghiệm)"),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$538\\,042 + 142\\,378$", "$729\\,062 - 68\\,504$"),
      "\\textbf{a) (0,75đ)} $538\\,042 + 142\\,378 = 680\\,420$. [[br]] \\textbf{b) (0,75đ)} $729\\,062 - 68\\,504 = 660\\,558$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ. \\textit{Bẫy ý b: số trừ có năm chữ số, phải đặt thẳng hàng đơn vị.}", TH_),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19$", "$125 + 130 + 135 + 140 + 145 + 150 + 155 + 160 + 165 + 170 + 175$"),
      "\\textbf{a) (1,0đ)} $= (11 + 19) + (12 + 18) + (13 + 17) + (14 + 16) + 15 = 30 \\times 4 + 15 = 135$. [[br]] \\textbf{b) (1,0đ)} $= (125 + 175) + (130 + 170) + (135 + 165) + (140 + 160) + (145 + 155) + 150 = 300 \\times 5 + 150 = 1\\,650$. [[br]] \\textit{Nhóm đúng $0,5$đ, kết quả đúng $0,5$đ mỗi ý.}", "a) " + HLg + " (câu trắc nghiệm, chuyển sang tự luận); b) Đề CK1 TH Hồng Quang, Ứng Hòa, Hà Nội 2024-2025"),
   tl("Bài 3.", 3, "2,0", "Một trường tiểu học có $578$ học sinh. Trong đó số học sinh nữ ít hơn số học sinh nam là $12$ em. Hỏi trường tiểu học đó có bao nhiêu học sinh nam, bao nhiêu học sinh nữ?",
      "Số học sinh nam là: $(578 + 12) : 2 = 295$ (học sinh) \\hfill \\textit{(0,75đ)} [[br]] Số học sinh nữ là: $295 - 12 = 283$ (học sinh) \\hfill \\textit{(0,75đ)} [[br]] Đáp số: Nam $295$ học sinh; nữ $283$ học sinh. \\hfill \\textit{(0,5đ)}", VB),
   tl("Bài 4.", 3, "0,5", "Rô-bốt dùng $7$ tấm thẻ $0$, $0$, $0$, $2$, $3$, $3$, $3$ để lập một số có bảy chữ số. Biết rằng lớp nghìn không chứa chữ số $0$ và chữ số $2$. Hỏi Rô-bốt đã lập được số nào? [[br]] \\textit{Trả lời:} Rô-bốt lập được số \\makebox[4.5cm]{\\dotfill}",
      "Lớp nghìn gồm ba chữ số khác $0$ và $2$ nên là $333$. Còn lại các thẻ $0, 0, 0, 2$: hàng triệu không thể là $0$ nên là $2$, lớp đơn vị là $000$. Số lập được: $2\\,333\\,000$. \\hfill \\textit{(0,5đ)}", DH),
   KIEM + "$\\square$ Đã tìm số nam trước, số nữ sau (Bài 3) & $\\square$ Đã ghi đáp số đủ hai số")

# ---------------- ĐỀ ÔN 1
dung("on1", [
    tn("Câu 1.", 1, "Số \"Sáu mươi hai triệu năm trăm bảy mươi nghìn ba trăm\" được viết là:", ["$62\\,300$", "$62\\,300\\,000$", "$6\\,270\\,300$", "$62\\,570\\,300$"], "D",
       "Chọn \\textbf{D}. Lớp triệu $62$, lớp nghìn $570$, lớp đơn vị $300$.", PN),
    tn("Câu 2.", 1, "Giá trị của chữ số $5$ trong số $3\\,705\\,328$ là:", ["$5$", "$50$", "$500$", "$5\\,000$"], "D",
       "Chọn \\textbf{D}. $3 \\mid 705 \\mid 328$: chữ số $5$ ở hàng nghìn nên có giá trị $5\\,000$.", TH_),
    tn("Câu 3.", 1, "Năm $1911$, Bác Hồ ra đi tìm đường cứu nước. Năm đó thuộc thế kỉ:", ["IX", "X", "XI", "XX"], "D",
       "Chọn \\textbf{D}. Thế kỉ XX gồm các năm từ $1901$ đến $2000$. \\textit{(Hướng dẫn chấm của trường ghi C là sai.)}", KS),
    tn("Câu 4.", 1, "Làm tròn số $456\\,789$ đến hàng trăm nghìn ta được số nào?", ["$450\\,000$", "$460\\,000$", "$500\\,000$", "$400\\,000$"], "C",
       "Chọn \\textbf{C}. Chữ số hàng chục nghìn là $5$ nên làm tròn lên: $500\\,000$.", MK + " (đề A)"),
    tn("Câu 5.", 2, "$5$ tạ $20$ kg $= \\dots$ kg. Số thích hợp điền vào chỗ chấm là:", ["$50$", "$52$", "$520$", "$5\\,200$"], "C",
       "Chọn \\textbf{C}. $5$ tạ $= 500$ kg nên $5$ tạ $20$ kg $= 520$ kg.", "Đề CK1 TH\\&THCS Chu Văn An, Ea Súp, Đắk Lắk 2024-2025"),
    tn("Câu 6.", 2, "Trong các góc: góc vuông, góc nhọn, góc tù, góc bẹt, góc lớn nhất là:", ["Góc vuông", "Góc nhọn", "Góc tù", "Góc bẹt"], "D",
       "Chọn \\textbf{D}. Góc bẹt bằng $180^\\circ$, lớn hơn góc tù, góc vuông và góc nhọn.", HLg),
    tn("Câu 7.", 2, "Giá trị của biểu thức $12 : (5 - m)$ với $m = 3$ là:", ["$4$", "$5$", "$6$", "$7$"], "C",
       "Chọn \\textbf{C}. $12 : (5 - 3) = 12 : 2 = 6$.", DT),
    tn("Câu 8.", 3, "Số hạng thứ nhất là số chẵn lớn nhất có sáu chữ số, số hạng thứ hai là số lớn nhất có bốn chữ số. Tổng của hai số đó là:", ["$1\\,009\\,998$", "$1\\,009\\,997$", "$1\\,010\\,997$", "$999\\,997$"], "B",
       "Chọn \\textbf{B}. $999\\,998 + 9\\,999 = 1\\,009\\,997$.", "Đề CK1 TH Tân Thuận 1, Tân Thành 2025-2026 (chuyển sang trắc nghiệm)"),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$548\\,359 + 270\\,523$", "$393\\,754 - 148\\,536$"),
      "\\textbf{a) (0,75đ)} $548\\,359 + 270\\,523 = 818\\,882$. [[br]] \\textbf{b) (0,75đ)} $393\\,754 - 148\\,536 = 245\\,218$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ.", VB),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$67 + 125 + 33 + 75$", "$142 + 236 + 58 + 64$"),
      "\\textbf{a) (1,0đ)} $= (67 + 33) + (125 + 75) = 100 + 200 = 300$. [[br]] \\textbf{b) (1,0đ)} $= (142 + 58) + (236 + 64) = 200 + 300 = 500$.", MK + " (a: đề A; b: đề B)"),
   tl("Bài 3.", 3, "2,0", "Trong một ngày, cửa hàng của cô Tâm bán được $450$ quả dừa, số quả dừa loại to bán được ít hơn số quả dừa loại nhỏ là $150$ quả. Hỏi cửa hàng của cô Tâm bán được bao nhiêu quả dừa mỗi loại?",
      "Số quả dừa loại to là: $(450 - 150) : 2 = 150$ (quả) \\hfill \\textit{(0,75đ)} [[br]] Số quả dừa loại nhỏ là: $150 + 150 = 300$ (quả) \\hfill \\textit{(0,75đ)} [[br]] Đáp số: Dừa to $150$ quả; dừa nhỏ $300$ quả. \\hfill \\textit{(0,5đ)}", "Đề CK1 TH Tân Liễu, Yên Dũng, Bắc Giang 2024-2025 (đề B)"),
   tl("Bài 4.", 3, "0,5", "Viết số lớn nhất có sáu chữ số, biết tổng các chữ số của số đó bằng $15$. [[br]] \\textit{Trả lời:} Số đó là \\makebox[4.5cm]{\\dotfill}",
      "Muốn số lớn nhất thì chữ số hàng cao nhất phải lớn nhất: hàng trăm nghìn là $9$, còn $15 - 9 = 6$ cho hàng chục nghìn, các hàng còn lại là $0$. Số đó là $960\\,000$. \\hfill \\textit{(0,5đ)}", DT),
   KIEM + "$\\square$ Đã tìm số bé trước (Bài 3) & $\\square$ Đã ghi đáp số đủ hai loại")

# ---------------- ĐỀ ÔN 2
dung("on2", [
    tn("Câu 1.", 1, "Số gồm $7$ chục triệu, $6$ triệu, $8$ nghìn, $2$ trăm và $1$ đơn vị là:", ["$76\\,820\\,201$", "$76\\,008\\,201$", "$76\\,800\\,201$", "$76\\,008\\,210$"], "B",
       "Chọn \\textbf{B}. Lớp triệu $76$, lớp nghìn $008$, lớp đơn vị $201$.", DC),
    tn("Câu 2.", 1, "Trong số $8\\,643\\,215$, chữ số $3$ thuộc hàng nào, lớp nào?", ["Hàng chục nghìn, lớp nghìn", "Hàng nghìn, lớp nghìn", "Hàng triệu, lớp triệu", "Hàng chục triệu, lớp triệu"], "B",
       "Chọn \\textbf{B}. $8 \\mid 643 \\mid 215$: chữ số $3$ đứng cuối lớp nghìn nên thuộc hàng nghìn.", VB),
    tn("Câu 3.", 1, "$4$ thế kỉ $= \\dots$ năm. Số thích hợp điền vào chỗ chấm là:", ["$40$", "$400$", "$4\\,000$", "$4$"], "B",
       "Chọn \\textbf{B}. $1$ thế kỉ $= 100$ năm nên $4$ thế kỉ $= 400$ năm.", "Đề CK1 TH Thị trấn Lộc Hà, Hà Tĩnh 2024-2025 (đề A)"),
    tn("Câu 4.", 1, "Làm tròn số $6\\,256\\,080$ đến hàng trăm nghìn ta được:", ["$6\\,200\\,000$", "$6\\,400\\,000$", "$6\\,300\\,000$", "$6\\,260\\,000$"], "C",
       "Chọn \\textbf{C}. Chữ số hàng chục nghìn là $5$ nên làm tròn lên: $6\\,300\\,000$.", "Đề CK1 TH Tân Liễu, Yên Dũng, Bắc Giang 2024-2025 (đề B)"),
    tn("Câu 5.", 2, "$5$ tấn $74$ kg $= \\dots$ kg. Số thích hợp điền vào chỗ chấm là:", ["$5\\,074$", "$574$", "$5\\,704$", "$50\\,074$"], "A",
       "Chọn \\textbf{A}. $5$ tấn $= 5\\,000$ kg nên $5$ tấn $74$ kg $= 5\\,074$ kg. \\textit{Bẫy: viết liền thành $574$.}", YT),
    ds("Câu 6.", 2, "Đúng ghi Đ, sai ghi S vào ô trống:", ["Góc tù lớn hơn góc vuông.", "Góc vuông nhỏ hơn góc nhọn.", "Góc tù lớn hơn góc bẹt.", "Góc bẹt bằng hai lần góc vuông."], "Đ-S-S-Đ",
       "a) \\textbf{Đ}; b) \\textbf{S}; c) \\textbf{S}; d) \\textbf{Đ} (mỗi ý $0{,}125$đ). Góc nhọn $<$ góc vuông $<$ góc tù $<$ góc bẹt; góc bẹt $= 180^\\circ = 2 \\times 90^\\circ$.", HL1),
    tn("Câu 7.", 2, "Giá trị của biểu thức $m + 115 \\times n$ với $m = 75$ và $n = 9$ là:", ["$1\\,710$", "$1\\,110$", "$1\\,035$", "$1\\,100$"], "B",
       "Chọn \\textbf{B}. $75 + 115 \\times 9 = 75 + 1\\,035 = 1\\,110$. \\textit{Bẫy: cộng trước rồi nhân ($190 \\times 9 = 1\\,710$).}", "Đề GK1 TH Long Biên, Hà Nội 2024-2025 (chuyển sang trắc nghiệm)"),
    tn("Câu 8.", 3, "Trong số $2\\,815\\,794$, giá trị của chữ số $8$ hơn giá trị của chữ số $1$ bao nhiêu đơn vị?", ["$7$", "$790\\,000$", "$79\\,000$", "$7\\,900$"], "B",
       "Chọn \\textbf{B}. Chữ số $8$ có giá trị $800\\,000$, chữ số $1$ có giá trị $10\\,000$: $800\\,000 - 10\\,000 = 790\\,000$.", PN),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$578\\,675 + 4\\,035$", "$766\\,346 - 9\\,239$"),
      "\\textbf{a) (0,75đ)} $578\\,675 + 4\\,035 = 582\\,710$. [[br]] \\textbf{b) (0,75đ)} $766\\,346 - 9\\,239 = 757\\,107$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ. \\textit{Bẫy: số thứ hai ít chữ số, phải đặt thẳng hàng đơn vị.}", PN),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$180\\,789 + 37\\,600 + 211$", "$87\\,000 - 3\\,250 - 6\\,750$"),
      "\\textbf{a) (1,0đ)} $= (180\\,789 + 211) + 37\\,600 = 181\\,000 + 37\\,600 = 218\\,600$. [[br]] \\textbf{b) (1,0đ)} $= 87\\,000 - (3\\,250 + 6\\,750) = 87\\,000 - 10\\,000 = 77\\,000$.",
      "a) Đề CK1 TH Hồng Quang, Ứng Hòa, Hà Nội 2024-2025 (câu trắc nghiệm, chuyển sang tự luận); b) PHỎNG THEO dạng trừ một tổng của đề CK1 TH Liên Bảo 2025-2026 (đổi số liệu)"),
   tl("Bài 3.", 3, "2,0", "Một thửa ruộng hình chữ nhật có chu vi là $38$ m, chiều dài hơn chiều rộng $9$ m. [[br]] a) Tính diện tích thửa ruộng đó. [[br]] b) Nếu mỗi mét vuông thu hoạch được $5$ kg thóc thì cả thửa ruộng thu hoạch được bao nhiêu ki-lô-gam thóc?",
      "Nửa chu vi thửa ruộng là: $38 : 2 = 19$ (m) \\hfill \\textit{(0,25đ)} [[br]] Chiều dài thửa ruộng là: $(19 + 9) : 2 = 14$ (m) \\hfill \\textit{(0,5đ)} [[br]] Chiều rộng thửa ruộng là: $14 - 9 = 5$ (m) \\hfill \\textit{(0,25đ)} [[br]] a) Diện tích thửa ruộng là: $14 \\times 5 = 70$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] b) Thửa ruộng thu hoạch được: $5 \\times 70 = 350$ (kg) \\hfill \\textit{(0,25đ)} [[br]] Đáp số: a) $70$ m$^2$; b) $350$ kg thóc. \\hfill \\textit{(0,25đ)}", HL1),
   tl("Bài 4.", 3, "0,5", "Cho các thẻ số: $9$, $3$, $5$, $0$, $2$, $7$. Tìm số nhỏ nhất có sáu chữ số lập được từ cả sáu thẻ số trên mà khi làm tròn số đó đến hàng trăm nghìn thì được số $300\\,000$. [[br]] \\textit{Trả lời:} Số đó là \\makebox[4.5cm]{\\dotfill}",
      "Làm tròn đến hàng trăm nghìn được $300\\,000$ thì số đó từ $250\\,000$ đến $349\\,999$. Muốn nhỏ nhất: hàng trăm nghìn là $2$, hàng chục nghìn phải là $5$ (vì $\\ge 5$), các thẻ còn lại $0, 3, 7, 9$ xếp tăng dần. Số đó là $250\\,379$. \\hfill \\textit{(0,5đ)}", DT),
   KIEM + "$\\square$ Đã chia đôi chu vi trước (Bài 3) & $\\square$ Đã ghi đơn vị m$^2$, kg ở đáp số")

# ---------------- ĐỀ ÔN 3
dung("on3", [
    tn("Câu 1.", 1, "Số gồm $5$ triệu, $2$ chục nghìn và $1$ chục được viết là:", ["$5\\,200\\,010$", "$5\\,020\\,010$", "$520\\,010$", "$5\\,210\\,100$"], "B",
       "Chọn \\textbf{B}. Lớp triệu $5$, lớp nghìn $020$, lớp đơn vị $010$.", YT),
    tn("Câu 2.", 1, "Chữ số $6$ trong số $863\\,274$ có giá trị là:", ["$60\\,000$", "$6\\,000$", "$600$", "$60$"], "A",
       "Chọn \\textbf{A}. Chữ số $6$ ở hàng chục nghìn nên có giá trị $60\\,000$.", YT),
    tn("Câu 3.", 1, "Năm $2017$ thuộc thế kỉ thứ mấy?", ["Thế kỉ XVIII", "Thế kỉ XIX", "Thế kỉ XX", "Thế kỉ XXI"], "D",
       "Chọn \\textbf{D}. Thế kỉ XXI gồm các năm từ $2001$ đến $2100$.", "Đề CK1 TH Đông Quang 2024-2025"),
    tn("Câu 4.", 1, "Số $256\\,378$ làm tròn đến hàng chục nghìn được số:", ["$256\\,000$", "$257\\,000$", "$260\\,000$", "$256\\,400$"], "C",
       "Chọn \\textbf{C}. Chữ số hàng nghìn là $6 > 5$ nên làm tròn lên: $260\\,000$.", YT),
    tn("Câu 5.", 2, "$18$ tấn $550$ kg $= \\dots$ yến. Số thích hợp điền vào chỗ chấm là:", ["$180\\,055$", "$18\\,055$", "$1\\,855$", "$18\\,550$"], "C",
       "Chọn \\textbf{C}. $18$ tấn $550$ kg $= 18\\,550$ kg $= 1\\,855$ yến (vì $10$ kg $= 1$ yến).", KS),
    tn("Câu 6.", 2, "Hình bình hành có đặc điểm nào dưới đây?", ["Có bốn góc vuông", "Có hai cặp cạnh đối diện song song và bằng nhau", "Có bốn cạnh bằng nhau", "Có hai cặp cạnh đối diện vuông góc"], "B",
       "Chọn \\textbf{B}. Hình bình hành có hai cặp cạnh đối diện song song và bằng nhau.", MK + " (đề B)"),
    ds("Câu 7.", 2, "Đúng ghi Đ, sai ghi S vào ô trống:", ["$5$ m$^2 = 500$ dm$^2$", "$2$ phút $10$ giây $= 210$ giây"], "Đ-S",
       "a) \\textbf{Đ} ($1$ m$^2 = 100$ dm$^2$); b) \\textbf{S} ($2$ phút $10$ giây $= 120 + 10 = 130$ giây). Mỗi ý $0{,}25$đ.", MK + " (đề A)"),
    tn("Câu 8.", 3, "Giá một số món đồ: đôi dép $145\\,000$ đồng, đôi giày $225\\,000$ đồng, ô tô đồ chơi $240\\,000$ đồng, thỏ bông $120\\,000$ đồng. Với tờ tiền $500\\,000$ đồng, Nam đủ tiền mua ba món đồ nào dưới đây?", ["Đôi giày, đôi dép, ô tô", "Đôi giày, đôi dép, thỏ bông", "Đôi giày, ô tô, thỏ bông", "Đôi dép, ô tô, thỏ bông"], "B",
       "Chọn \\textbf{B}. $225\\,000 + 145\\,000 + 120\\,000 = 490\\,000 < 500\\,000$. Các phương án khác: A $610\\,000$, C $585\\,000$, D $505\\,000$ đều vượt $500\\,000$.", "Đề CK1 TH Hồng Quang, Ứng Hòa, Hà Nội 2024-2025 (đề gốc có hình giá tiền, 3 phương án; thêm phương án D)"),
], tl("Bài 1.", 1, "1,5", "Đặt tính rồi tính: " + hai_cot("$428\\,458 + 380\\,622$", "$939\\,064 - 546\\,837$"),
      "\\textbf{a) (0,75đ)} $428\\,458 + 380\\,622 = 809\\,080$. [[br]] \\textbf{b) (0,75đ)} $939\\,064 - 546\\,837 = 392\\,227$. [[br]] Mỗi ý: đặt tính đúng $0,25$đ, kết quả đúng $0,5$đ.", HL1),
   tl("Bài 2.", 2, "2,0", "Tính bằng cách thuận tiện: " + hai_cot("$1\\,250 + 3\\,470 + 750 + 530$", "$24\\,680 - 4\\,680 - 7\\,000$"),
      "\\textbf{a) (1,0đ)} $= (1\\,250 + 750) + (3\\,470 + 530) = 2\\,000 + 4\\,000 = 6\\,000$. [[br]] \\textbf{b) (1,0đ)} $= (24\\,680 - 4\\,680) - 7\\,000 = 20\\,000 - 7\\,000 = 13\\,000$.",
      "PHỎNG THEO dạng nhóm số tròn nghìn của đề CK1 TH Minh Khôi 2025-2026 và TH Liên Bảo 2025-2026 (đổi số liệu)"),
   tl("Bài 3.", 3, "2,0", "Chú Hà có $4$ sào đất, mỗi sào có diện tích $360$ m$^2$. Chú trồng cây ăn quả và rau trên $4$ sào đất đó. Diện tích trồng cây ăn quả lớn hơn diện tích trồng rau là $80$ m$^2$. Tính diện tích trồng cây ăn quả và diện tích trồng rau.",
      "Diện tích $4$ sào đất là: $360 \\times 4 = 1\\,440$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] Diện tích trồng cây ăn quả là: $(1\\,440 + 80) : 2 = 760$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] Diện tích trồng rau là: $760 - 80 = 680$ (m$^2$) \\hfill \\textit{(0,5đ)} [[br]] Đáp số: Cây ăn quả $760$ m$^2$; rau $680$ m$^2$. \\hfill \\textit{(0,5đ)}", HLg),
   tl("Bài 4.", 3, "0,5", "Viết tất cả các số tròn chục có bốn chữ số khác nhau, biết tổng các chữ số của mỗi số bằng $6$. [[br]] \\textit{Trả lời:} \\dotfill\\mbox{}",
      "Số tròn chục nên hàng đơn vị là $0$; ba chữ số còn lại khác nhau, khác $0$, có tổng $6$ nên là $1, 2, 3$. Các số: $1\\,230$; $1\\,320$; $2\\,130$; $2\\,310$; $3\\,120$; $3\\,210$. \\hfill \\textit{(0,5đ; đúng 3--5 số: $0{,}25$đ)}", "Đề GK1 TH Gia Trung, Gia Viễn, Ninh Bình 2024-2025"),
   KIEM + "$\\square$ Đã tính tổng diện tích trước (Bài 3) & $\\square$ Đã viết đủ 6 số (Bài 4)")
