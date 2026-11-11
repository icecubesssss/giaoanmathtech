#!/usr/bin/env python3
"""Sinh MA TRẬN + ĐÁP ÁN cho 3 đề CK1 Toán 4 (theme de_thi), đọc thẳng từ JSON đề.

% "đề trường có dạng" tính trên ngân hàng CK1 lớp 4 (outputs/ngan-hang-sheet/tieu-hoc/lop-4/pct-ck1.json).
    .venv/bin/python scripts/ma_tran_ck1_lop4.py
"""
import copy, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "inputs/seeds/lop-4/de-cuoi-ki-1"
PCT = json.loads((ROOT / "outputs/ngan-hang-sheet/tieu-hoc/lop-4/pct-ck1.json").read_text(encoding="utf-8"))
SKEL = json.loads((ROOT / "inputs/seeds/lop-5/de-cuoi-ki-1/ma-tran-va-dap-an-cuoi-ki-1-de-1.json").read_text(encoding="utf-8"))
D_DOI, D_TH, D_HANG, D_DAT, D_DOC, D_TT = ("Đổi đơn vị đo đại lượng (khối lượng, diện tích, thời gian, độ dài)", "Tìm hai số khi biết tổng và hiệu",
    "Hàng và lớp; giá trị chữ số", "Đặt tính rồi tính (+, − số có nhiều chữ số; ×, : cho số có một chữ số)", "Đọc, viết số có nhiều chữ số",
    "Tính thuận tiện (tính chất giao hoán, kết hợp, phân phối)")
D_LT, D_GOC, D_BT, D_CL, D_HBH, D_CV = "Làm tròn số", "Đo góc; góc nhọn, tù, bẹt", "Biểu thức chứa chữ", "Số chẵn, số lẻ; dãy số tự nhiên", "Hình bình hành, hình thoi", "Bài toán thực tế về chu vi, diện tích"
# (nhãn, nội dung ngắn, bài SGK, chủ đề, dạng ngân hàng, mức, điểm, phút)
META = {
 1: [("Câu 1", "Đọc số có nhiều chữ số", "Bài 10", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Hàng và lớp của một chữ số", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Năm thuộc thế kỉ nào", "Bài 19", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng trăm nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Đổi tấn, tạ – yến", "Bài 17", 4, D_DOI, 2, .5, 2), ("Câu 6", "Nhận biết góc tù theo số đo", "Bài 8", 2, D_GOC, 2, .5, 2),
     ("Câu 7", "Giá trị biểu thức chứa chữ", "Bài 4", 1, D_BT, 2, .5, 2), ("Câu 8", "Viết thêm chữ số $\\to$ số tăng bao nhiêu", "Bài 11", 3, D_HANG, 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ số có 6 chữ số", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện: tổng dãy cách đều (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Tìm hai số khi biết tổng và hiệu", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Lập số theo điều kiện về lớp", "Bài 10", 3, "Cấu tạo số theo điều kiện", 3, .5, 4)],
 2: [("Câu 1", "Đọc số có nhiều chữ số", "Bài 12", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Hàng và lớp của một chữ số", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Năm thuộc thế kỉ nào", "Bài 19", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng trăm nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Đổi tấn – kg", "Bài 17", 4, D_DOI, 2, .5, 2), ("Câu 6", "Góc tạo bởi hai kim đồng hồ", "Bài 7", 2, D_GOC, 2, .5, 2),
     ("Câu 7", "Giá trị biểu thức chứa hai chữ", "Bài 4", 1, D_BT, 2, .5, 2), ("Câu 8", "Tổng hai số lẻ liên tiếp", "Bài 25", 5, D_TH, 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ số có 6 chữ số", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Nửa chu vi $\\to$ tổng – hiệu $\\to$ diện tích", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Bài toán cắt vải (bẫy số lần cắt)", "—", 0, "Suy luận logic", 3, .5, 4)],
 3: [("Câu 1", "Viết số có nhiều chữ số", "Bài 10", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Giá trị của chữ số theo hàng", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Đổi tạ – kg", "Bài 17", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng trăm nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Ước lượng độ dài (dm, m)", "Bài 20", 4, D_DOI, 2, .5, 2), ("Câu 6", "Đặc điểm hình thoi", "Bài 31", 6, D_HBH, 2, .5, 2),
     ("Câu 7", "Biểu thức chứa chữ có ngoặc", "Bài 4", 1, D_BT, 2, .5, 2), ("Câu 8", "Năm sinh từ năm kỉ niệm $\\to$ thế kỉ", "Bài 19", 4, D_DOI, 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ số có 6 chữ số", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Nửa chu vi $\\to$ tổng – hiệu $\\to$ diện tích", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Đếm số hạng của dãy cách đều", "Bài 15", 0, "Dãy số theo quy luật", 3, .5, 4)],
 "on1": [("Câu 1", "Viết số có nhiều chữ số", "Bài 10", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Giá trị của chữ số theo hàng", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Năm thuộc thế kỉ nào", "Bài 19", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng trăm nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Đổi tạ – kg", "Bài 17", 4, D_DOI, 2, .5, 2), ("Câu 6", "So sánh các loại góc", "Bài 8", 2, D_GOC, 2, .5, 2),
     ("Câu 7", "Biểu thức chứa chữ có ngoặc", "Bài 4", 1, D_BT, 2, .5, 2), ("Câu 8", "Số chẵn lớn nhất, số lớn nhất $\\to$ tổng", "Bài 15", 3, D_CL, 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ số có 6 chữ số", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Tìm hai số khi biết tổng và hiệu", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Số lớn nhất có tổng chữ số cho trước", "Bài 10", 3, "Cấu tạo số theo điều kiện", 3, .5, 4)],
 "on2": [("Câu 1", "Viết số theo các hàng", "Bài 10", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Hàng và lớp của một chữ số", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Đổi thế kỉ – năm", "Bài 19", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng trăm nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Đổi tấn – kg (bẫy viết liền)", "Bài 17", 4, D_DOI, 2, .5, 2), ("Câu 6", "Đúng/sai: so sánh các loại góc", "Bài 8", 2, D_GOC, 2, .5, 2),
     ("Câu 7", "Giá trị biểu thức chứa hai chữ", "Bài 4", 1, D_BT, 2, .5, 2), ("Câu 8", "Hiệu giá trị hai chữ số", "Bài 11", 3, D_HANG, 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ (số có ít chữ số hơn)", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Chu vi $\\to$ tổng – hiệu $\\to$ diện tích, thóc", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Lập số từ thẻ + làm tròn", "Bài 13", 3, D_LT, 3, .5, 4)],
 "on3": [("Câu 1", "Viết số theo các hàng", "Bài 10", 3, D_DOC, 1, .5, 1.5), ("Câu 2", "Giá trị của chữ số theo hàng", "Bài 11", 3, D_HANG, 1, .5, 1.5),
     ("Câu 3", "Năm thuộc thế kỉ nào", "Bài 19", 4, D_DOI, 1, .5, 1.5), ("Câu 4", "Làm tròn đến hàng chục nghìn", "Bài 13", 3, D_LT, 1, .5, 1.5),
     ("Câu 5", "Đổi tấn, kg – yến", "Bài 17", 4, D_DOI, 2, .5, 2), ("Câu 6", "Đặc điểm hình bình hành", "Bài 31", 6, D_HBH, 2, .5, 2),
     ("Câu 7", "Đúng/sai: đổi m$^2$, phút – giây", "Bài 18, 19", 4, D_DOI, 2, .5, 2), ("Câu 8", "Chọn phương án mua hàng đủ tiền", "Bài 23", 5, "Bài toán thực tế chọn phương án (tiền, mua bán)", 3, .5, 3),
     ("Bài 1", "Đặt tính cộng, trừ số có 6 chữ số", "Bài 22, 23", 5, D_DAT, 1, 1.5, 5), ("Bài 2", "Tính thuận tiện (2 ý)", "Bài 24", 5, D_TT, 2, 2, 6),
     ("Bài 3", "Tổng diện tích $\\to$ tổng – hiệu", "Bài 25", 5, D_TH, 3, 2, 8), ("Bài 4", "Lập số tròn chục theo tổng chữ số", "Bài 10", 3, "Cấu tạo số theo điều kiện", 3, .5, 4)],
}
CHU_DE = {0: "Toán tư duy", 1: "CĐ1 Ôn tập và bổ sung", 2: "CĐ2 Góc và đơn vị đo góc", 3: "CĐ3 Số có nhiều chữ số", 4: "CĐ4 Đơn vị đo đại lượng",
          5: "CĐ5 Phép cộng và phép trừ", 6: "CĐ6 Đường vuông góc, song song"}


def so(x):
    return f"{x:g}".replace(".", "{,}")


def tab(rows, head, cols):
    out = ["\\begin{center}\\scriptsize\\renewcommand{\\arraystretch}{1.1}", "\\begin{tabular}{" + cols + "}", "\\hline",
           " & ".join(f"\\textbf{{{h}}}" for h in head) + " \\tabularnewline \\hline"]
    out += [" & ".join(map(str, r)) + " \\tabularnewline \\hline" for r in rows]
    return "\n".join(out + ["\\end{tabular}", "\\end{center}"])


def nguon(sol):
    m = re.search(r"\(Nguồn: (.*?)\.\)", sol)
    return m.group(1) if m else "Tự ra theo dạng đề trường"


def build(n):
    on = isinstance(n, str)
    slug_de = f"de-on-tap-cuoi-ki-1-so-{n[2:]}" if on else f"de-kiem-tra-cuoi-ki-1-de-{n}"
    loai = "ĐỀ ÔN TẬP" if on else "ĐỀ KIỂM TRA"
    ten = f"ĐỀ ÔN TẬP SỐ {n[2:]}" if on else f"ĐỀ {n}"
    ten_t = f"Đề ôn tập cuối học kì I — Đề ôn số {n[2:]}" if on else f"Đề kiểm tra cuối học kì I — Đề {n}"
    slug_mt = f"ma-tran-va-dap-an-on-tap-cuoi-ki-1-so-{n[2:]}" if on else f"ma-tran-va-dap-an-cuoi-ki-1-de-{n}"
    de = json.loads((DIR / f"{slug_de}.json").read_text(encoding="utf-8"))
    probs = {b["label"].rstrip("."): b for s in de["stages"] for b in s["blocks"] if b["type"] == "problem"}
    meta = META[n]
    rows = []
    for lab, nd, bai, cd, dang, muc, d, ph in meta:
        p = PCT["pct"].get(dang)
        rows.append([lab, f"{nd} ({bai})", f"M{muc} -- {so(d)}đ", f"{so(ph)}′", f"{p}\\%" if p is not None else "--",
                     "\\tiny " + nguon(probs[lab]["solution"])])
    tong = {m: (sum(1 for x in meta if x[5] == m), sum(x[6] for x in meta if x[5] == m)) for m in (1, 2, 3)}
    rows_m = [[f"Mức {m}", c, so(d) + "đ", f"{round(d*10)}\\%"] for m, (c, d) in tong.items()]
    cds = {}
    for x in meta:
        cds.setdefault(x[3], [0, 0]); cds[x[3]][0] += 1; cds[x[3]][1] += x[6]
    rows_cd = [[CHU_DE[k], v[0], so(v[1]) + "đ"] for k, v in sorted(cds.items())]
    tg = sum(x[7] for x in meta)
    head = (f"\\textbf{{MA TRẬN {loai} CUỐI HỌC KÌ I -- TOÁN 4 -- {ten}}} [[br]] Barem theo đề trung tâm lớp 4 (KNTT): 40 phút, "
            "8 câu trắc nghiệm $4{,}0$đ + 4 bài tự luận $6{,}0$đ (1,5 -- 2 -- 2 -- 0,5). Không ra Chủ đề 8 (đúng tiến độ 4C). [[br]] "
            f"Cột \\textit{{\\% đề trường}}: tỉ lệ trong {PCT['so_de']} đề CK1 Toán 4 của các trường (2023--2026) có dạng đó. "
            f"Tổng thời lượng ước tính: {so(tg)} phút.")
    s = copy.deepcopy(SKEL)
    s.update({"slug": slug_mt, "title": f"Ma trận đề và đáp án — {ten_t}",
              "eyebrow": f"SỔ TAY GIÁO VIÊN • LỚP 4 • {ten_t.upper()}", "grade_label": "Lớp 4"})
    st = s["stages"]
    st[0]["title"] = f"Ma trận {ten_t.split(' — ')[1]}"
    st[0]["blocks"] = [{"type": "para", "text": head + " [[br]] \\textbf{Bảng phân bố câu hỏi:}\n" + tab(rows, ["Câu", "Dạng bài (bài SGK KNTT)", "Mức -- điểm", "Phút", "\\% đề trường", "Nguồn câu"], "|c|p{4.7cm}|c|c|c|p{6.3cm}|")},
        {"type": "para", "text": "\\noindent\\begin{minipage}[t]{0.42\\linewidth}\\textbf{Tổng hợp theo mức (Thông tư 27):}\n" + tab(rows_m, ["Mức", "Số câu", "Điểm", "Tỉ lệ"], "|c|c|c|c|") + "\\end{minipage}\\hfill\\begin{minipage}[t]{0.55\\linewidth}\\textbf{Tổng hợp theo chủ đề SGK:}\n" + tab(rows_cd, ["Chủ đề", "Số câu", "Điểm"], "|p{4.2cm}|c|c|") + "\\end{minipage}"}]
    tn = [probs[f"Câu {i}"] for i in range(1, 9)]
    st[1]["title"] = "Đáp án Phần I — Trắc nghiệm"
    st[1]["blocks"] = [{"type": "para", "text": "\\textbf{BẢNG ĐÁP ÁN TRẮC NGHIỆM (4,0 ĐIỂM, mỗi câu 0,5 điểm)} [[br]]\n" + tab([[f"\\textbf{{{p['answer']}}}" for p in tn]], [f"Câu {i}" for i in range(1, 9)], "|" + "c|" * 8)},
        {"type": "para", "text": "\\textbf{GIẢI THÍCH CHI TIẾT} [[br]] " + " [[br]] ".join(f"\\textbf{{Câu {i}.}} {p['solution']}" for i, p in enumerate(tn, 1))}]
    for k, (a, b) in ((2, ("Bài 1", "Bài 2")), (3, ("Bài 3", "Bài 4"))):
        st[k]["title"] = f"Đáp án {a} và {b}"
        st[k]["blocks"] = [{"type": "para", "text": f"\\textbf{{ĐÁP ÁN {x.upper()}.}} {probs[x]['statement']} [[br]] {probs[x]['solution']}"} for x in (a, b)]
    st[4]["title"] = "Hướng dẫn chấm"
    st[4]["blocks"] = [{"type": "para", "text": "\\textbf{HƯỚNG DẪN CHẤM CHUNG} \\begin{itemize}"
        "\\item Bài 1: mỗi phép tính $0{,}75$đ (đặt tính thẳng cột $0{,}25$đ, kết quả $0{,}5$đ); đặt tính lệch cột nhưng đúng kết quả: $0{,}5$đ."
        "\\item Bài 2: mỗi ý $1{,}0$đ; tính lần lượt từ trái sang phải đúng kết quả: $0{,}5$đ."
        "\\item Bài 3: câu lời giải sai nhưng phép tính đúng vẫn cho điểm phép tính; thiếu hoặc sai đơn vị ở đáp số: trừ $0{,}25$đ."
        "\\item Bài 4: chỉ cần ghi đúng đáp số là đủ $0{,}5$đ."
        "\\item Điểm toàn bài làm tròn thành số nguyên theo Thông tư 27 ($\\ge 0{,}5$ làm tròn lên)."
        "\\end{itemize}"}]
    (DIR / f"{slug_mt}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ ma trận Đề {n}: M1 {tong[1][1]}đ · M2 {tong[2][1]}đ · M3 {tong[3][1]}đ · {tg} phút")


for n in (1, 2, 3, "on1", "on2", "on3"):
    build(n)
