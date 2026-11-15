#!/usr/bin/env python3
"""Sinh 3 ĐỀ ÔN TẬP + 3 ĐỀ CHÍNH THỨC cuối HK1 Toán 5 (KNTT) và MA TRẬN kèm đáp án (dựng lại 15/11/2026).

Khung + kế hoạch câu: scripts/ck1_lop5_ke_hoach.py (mọi câu bốc từ đề TRƯỜNG THẬT, ngân hàng
inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi). Nội dung từng ô (chép nguyên văn + lời giải) do Gemini soạn
(scripts/gemini/viec_de_ck1_lop5.py), Claude soát và vá trong scripts/ck1_lop5_de.json (VA bên dưới).
Khuôn trang = đề lớp 3/4 đã sửa ô điểm \\rule{0pt}{2.4cm}, chỗ chấm \\makebox{\\dotfill}.

    .venv/bin/python scripts/de_ck1_lop5.py --gom     # gom storage/gemini/xong/de5-*.json → scripts/ck1_lop5_de.json
    .venv/bin/python scripts/de_ck1_lop5.py           # dựng 12 seed vào inputs/seeds/lop-5/de-cuoi-ki-1/
"""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from ck1_lop5_ke_hoach import DE as KH, DIEM, MUC, PHUT  # noqa: E402

DIR = ROOT / "inputs/seeds/lop-5/de-cuoi-ki-1"
BG = ROOT / "inputs/refs/ngan-hang-sheet/tieu-hoc/lop-5/ban-ghi"
DATA = ROOT / "scripts/ck1_lop5_de.json"
KHUNG = json.loads((ROOT / "config/khung-phan-dang/tieu-hoc-lop-5-kntt.json").read_text(encoding="utf-8"))
BASE = json.loads((ROOT / "inputs/seeds/lop-3/de-cuoi-ki-1/de-on-tap-cuoi-ki-1-so-1.json").read_text(encoding="utf-8"))
SKEL_MT = json.loads((ROOT / "inputs/seeds/lop-3/de-cuoi-ki-1/ma-tran-va-dap-an-on-tap-cuoi-ki-1-so-1.json").read_text(encoding="utf-8"))
NAM = "NĂM HỌC 2026 – 2027"

BANK = {f.stem[3:]: json.loads(f.read_text(encoding="utf-8")) for f in sorted(BG.glob("l5-*.json"))}
CK1 = [k for k in BANK if k.startswith("ck1-")]
TEN_DANG = {d["ma"]: d["ten"] for d in KHUNG["dang"]}
TEN_CD = {c["so"]: c["ten"] for c in KHUNG["chu_de"]}
TEN = {"on1": "Đề ôn số 1", "on2": "Đề ôn số 2", "on3": "Đề ôn số 3", "ct1": "Đề 1", "ct2": "Đề 2", "ct3": "Đề 3"}


def cau(ref):
    de, c = ref.split("#")
    return next(x for x in BANK[de]["cau"] if x["cau"] == c)


def nguon(ref):
    de, c = ref.split("#")
    g = BANK[de].get("ghi_chu_de", "")
    m = re.search(r"(Trường\s+)?(Tiểu học|TH&THCS|PTDTBT TH&THCS|TH)\s+([^,.;(]+)", g)
    truong = ("TH " + m.group(3).strip()) if m else de.split("-")[-1]
    if "myanhung" in de:
        truong = "TH xã Mỹ An Hưng, Đồng Tháp"
    ky = "CK1" if de.startswith("ck1") else "GK1"
    nam = "20" + de.split("-")[1][:2] + "-20" + de.split("-")[1][2:]
    return f"Đề {ky} {truong} {nam}, câu {c}".replace("&", "\\&")


# ------------------------------------------------------------------ dựng câu
def ops(opts):
    n = 4 if max(len(re.sub(r"\\[a-z]+|[{}$]", "", o)) for o in opts) <= 22 else (2 if max(len(o) for o in opts) <= 60 else 1)
    w = {4: "3.9cm", 2: "7.9cm", 1: "15.8cm"}[n]
    cells = [f"\\textbf{{{'ABCD'[i]}.}} {o}" for i, o in enumerate(opts)]
    rows = [" & ".join(cells[i:i + n]) for i in range(0, len(cells), n)]
    return "\\par\\noindent\\begin{tabular}{@{}" + f"p{{{w}}}" * n + "@{}}" + " \\\\[2pt] ".join(rows) + "\\end{tabular}"


def fig(text, tikz, w=0.62):
    return (f"\\par\\noindent\\begin{{minipage}}[c]{{{w}\\linewidth}}\\raggedright {text}\\end{{minipage}}\\hfill"
            f"\\begin{{minipage}}[c]{{{0.97 - w:.2f}\\linewidth}}\\centering {tikz}\\end{{minipage}}")


def cot(ys, n, chu=True):
    w = {2: "7.9cm", 4: "3.9cm", 1: "15.8cm"}[n]
    cells = [(f"\\textbf{{{'abcd'[i]})}} " if chu else "") + y for i, y in enumerate(ys)]
    rows = [" & ".join(cells[i:i + n]) for i in range(0, len(cells), n)]
    return "\\par\\noindent\\begin{tabular}{@{}" + f"p{{{w}}}" * n + "@{}}" + " \\\\[6pt] ".join(rows) + "\\end{tabular}"


def so(x):
    return f"{x:g}".replace(".", ",")


def than(o, q):
    """Thân câu (statement) theo hình thức. Câu có hình: chỉ lời dẫn đặt cạnh hình, ý/phương án xuống dưới."""
    dau = q["de_bai"].strip()
    if q.get("tikz"):
        dau = fig(dau, q["tikz"], 0.58 if o.startswith("B") else 0.62)
    ys = q.get("y") or []
    if o == "B1":
        return dau + cot([f"${y.strip('$')}$" for y in ys], 4)
    if o == "B2":
        return dau + cot(ys, 2)
    if o in ("B3", "B4") and ys:
        return dau + cot(ys, 2 if o == "B3" and all(len(y) < 45 for y in ys) else 1)
    if q["hinh_thuc"] == "TN":
        return dau + ops(q["phuong_an"])
    if q["hinh_thuc"] == "Đ-S":
        return dau + "".join(f"\\par\\noindent {'abcd'[i]}) {y} \\hfill $\\square$" for i, y in enumerate(ys))
    return dau + (cot(ys, 1) if ys else "")


def lam_cau(k, o, q, so_cau):
    refs = next(r for oo, r, _ in KH[k] if oo == o)
    nhan = f"Câu {so_cau}." if o.startswith("C") else f"Bài {o[1]}."
    src = "; ".join(nguon(r) for r in refs)
    g = (q.get("doi_so_voi_goc") or "").lower()
    nhan_doi = [t for k_, t in (("trắc nghiệm", "chuyển sang trắc nghiệm"), ("thêm phương án", "thêm phương án nhiễu"),
                                ("bổ sung phương án", "thêm phương án nhiễu"), ("tách", "tách ý"),
                                ("thang điểm", "đổi điểm")) if k_ in g]
    if nhan_doi:
        src += " (" + ", ".join(dict.fromkeys(nhan_doi)) + ")"
    return {"blk": {"type": "problem", "label": nhan, "level": MUC[o],
                    "statement": f"\\textbf{{({so(DIEM[o])} điểm)}} " + than(o, q),
                    "answer": q["dap_an"], "solution": q["loi_giai"] + f" [[br]] \\textit{{(Nguồn: {src}.)}}",
                    "tier": "onclass"}, "o": o, "refs": refs, "diem": DIEM[o], "nguon": src}


# ------------------------------------------------------------------ trang
def slug_de(k):
    return f"de-on-tap-cuoi-ki-1-so-{k[2:]}" if k.startswith("on") else f"de-kiem-tra-cuoi-ki-1-de-{k[2:]}"


def slug_mt(k):
    return f"ma-tran-va-dap-an-on-tap-so-{k[2:]}" if k.startswith("on") else f"ma-tran-va-dap-an-cuoi-ki-1-de-{k[2:]}"


P1 = {"on1": 6, "on2": 5, "on3": 6, "ct1": 5, "ct2": 6, "ct3": 6}  # số câu TN trang 1 (soát PDF rồi chỉnh)
OLY = {"B1": 7, "B23": 8, "B4": 6, "B5": 3}


def dung_de(k, qs):
    b = {q["o"]: q["blk"] for q in qs}
    on = k.startswith("on")
    d = copy.deepcopy(BASE)
    d.update({"slug": slug_de(k), "grade_label": "Lớp 5",
              "title": (f"Đề ôn tập cuối học kì I — {TEN[k]} (40 phút)" if on else f"Đề kiểm tra cuối học kì I — {TEN[k]} (40 phút)"),
              "eyebrow": ("ĐỀ ÔN TẬP" if on else "ĐỀ KIỂM TRA ĐỊNH KÌ") + f" CUỐI HỌC KÌ I · TOÁN 5 · {NAM}"})
    s = d["stages"]
    the = s[0]["blocks"][0]
    np_ = {"type": "para", "text": "\\newpage"}
    tn = [b[f"C{i}"] for i in range(1, 9)]
    p1 = P1[k]
    h1 = {"type": "para", "text": "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Khoanh vào chữ cái đặt trước câu trả lời đúng hoặc làm theo yêu cầu.}\\par\\vspace{3pt}"}
    s[0]["blocks"] = [the, h1] + tn[:p1] + [np_]
    s[0]["teacher_note"] = f"Trang 1: khung Điểm, Câu 1 đến Câu {p1}."
    s[1]["blocks"] = tn[p1:] + [{"type": "para", "text": "\\par\\vspace{4pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"}, b["B1"],
                                {"type": "writelines", "variant": "oly", "count": OLY["B1"]},
                                {"type": "para", "text": "\\centerline{\\textit{\\footnotesize (Học sinh đặt tính thẳng cột và làm bài vào khung ô ly trên)}}"}, np_]
    s[1]["teacher_note"] = f"Trang 2: Câu {p1 + 1} đến Câu 8, Bài 1 đặt tính (ô ly)."
    s[2]["blocks"] = [b["B2"], b["B3"], {"type": "writelines", "variant": "oly", "count": OLY["B23"]}, np_]
    s[2]["teacher_note"] = "Trang 3: Bài 2 viết số đo, Bài 3 (ô ly)."
    s[3]["blocks"] = [b["B4"], {"type": "writelines", "variant": "oly", "count": OLY["B4"]}, b["B5"],
                      {"type": "writelines", "variant": "oly", "count": OLY["B5"]}]
    s[3]["teacher_note"] = "Trang 4: Bài 4 bài toán thực tế, Bài 5 tư duy, phiếu tự kiểm tra."
    r = s[4]["blocks"]
    kiem = ("$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã làm đủ 8 câu Phần I \\\\\n"
            "$\\square$ Đã đặt tính thẳng cột, thẳng dấu phẩy (Bài 1) & $\\square$ Đã kiểm tra đơn vị khi đổi (Bài 2) \\\\\n"
            "$\\square$ Bài 4 có câu lời giải, phép tính, đáp số & $\\square$ Đã ghi đơn vị m$^2$ và đáp số")
    r[0] = dict(r[0], text=r[0]["text"].split("\\begin{tabular}")[0] + "\\begin{tabular}{p{7.5cm}p{7.5cm}}\n" + kiem + "\n\\end{tabular}\n\\end{tcolorbox}")
    (DIR / f"{slug_de(k)}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ ma trận
def pct(refs):
    dang = cau(refs[0])["dang"]
    co = sum(1 for de in CK1 if any(x["dang"] == dang for x in BANK[de]["cau"]))
    return round(100 * co / len(CK1)), dang


def tab(rows, head, cols):
    out = ["\\begin{center}\\scriptsize\\renewcommand{\\arraystretch}{1.1}", "\\begin{tabular}{" + cols + "}", "\\hline",
           " & ".join(f"\\textbf{{{h}}}" for h in head) + " \\tabularnewline \\hline"]
    out += [" & ".join(map(str, r)) + " \\tabularnewline \\hline" for r in rows]
    return "\n".join(out + ["\\end{tabular}", "\\end{center}"])


def dung_ma_tran(k, qs):
    on = k.startswith("on")
    ten_t = f"Đề ôn tập cuối học kì I — {TEN[k]}" if on else f"Đề kiểm tra cuối học kì I — {TEN[k]}"
    rows, tong, cds = [], {1: [0, 0], 2: [0, 0], 3: [0, 0]}, {}
    for q in qs:
        o, refs = q["o"], q["refs"]
        c0 = cau(refs[0])
        bais = sorted({cau(r).get("bai") for r in refs if cau(r).get("bai")})
        p, dg = pct(refs)
        muc = MUC[o]
        rows.append([q["blk"]["label"].rstrip("."), f"{TEN_DANG[dg]} (Bài " + ", ".join(map(str, bais)) + ")",
                     f"M{muc} -- {so(q['diem'])}đ", f"{so(PHUT[o])}′", f"{p}\\%", "\\tiny " + q["nguon"]])
        tong[muc][0] += 1
        tong[muc][1] += q["diem"]
        cd = c0.get("cd") or 0
        cds.setdefault(cd, [0, 0])
        cds[cd][0] += 1
        cds[cd][1] += q["diem"]
    rows_m = [[f"Mức {m}", c, so(dd) + "đ", f"{round(dd * 10)}\\%"] for m, (c, dd) in tong.items()]
    rows_cd = [[f"CĐ{c} {TEN_CD.get(c, '')}", v[0], so(v[1]) + "đ"] for c, v in sorted(cds.items())]
    tg = sum(PHUT.values())
    head = (f"\\textbf{{MA TRẬN {'ĐỀ ÔN TẬP' if on else 'ĐỀ KIỂM TRA'} CUỐI HỌC KÌ I -- TOÁN 5 -- {TEN[k].upper()}}} [[br]] "
            "Khung theo 8 đề CK1 Toán 5 của các trường (2024--2026) và mẫu đề ôn trung tâm: 40 phút; Phần I $4{,}0$đ (8 câu × $0{,}5$đ); "
            "Phần II $6{,}0$đ (Bài 1 đặt tính 2đ, Bài 2 viết số đo dạng số thập phân 1đ, Bài 3 biểu thức/tìm $x$/thuận tiện 1đ, "
            "Bài 4 bài toán thực tế về diện tích $1{,}5$đ, Bài 5 tư duy $0{,}5$đ). Chỉ ra Chủ đề 1--6 (kiến thức kì I). [[br]] "
            f"Cột \\textit{{\\% đề trường}}: tỉ lệ trong {len(CK1)} đề CK1 Toán 5 của các trường có dạng của câu. 100\\% câu bốc từ đề trường (cột Nguồn). "
            f"Tổng thời lượng ước tính: {so(tg)} phút.")
    s = copy.deepcopy(SKEL_MT)
    s.update({"slug": slug_mt(k), "title": f"Ma trận đề và đáp án — {ten_t}", "grade_label": "Lớp 5",
              "eyebrow": f"SỔ TAY GIÁO VIÊN • LỚP 5 • {ten_t.upper()}"})
    st = s["stages"]
    st[0]["title"] = f"Ma trận {TEN[k]}"
    st[0]["blocks"] = [
        {"type": "para", "text": head + " [[br]] \\textbf{Bảng phân bố câu hỏi:}\n" + tab(rows, ["Câu", "Dạng bài (bài SGK KNTT)", "Mức -- điểm", "Phút", "\\% đề trường", "Nguồn câu"], "|c|p{4.6cm}|c|c|c|p{6.4cm}|")},
        {"type": "para", "text": "\\noindent\\begin{minipage}[t]{0.42\\linewidth}\\textbf{Tổng hợp theo mức (Thông tư 27):}\n" + tab(rows_m, ["Mức", "Số câu", "Điểm", "Tỉ lệ"], "|c|c|c|c|") + "\\end{minipage}\\hfill\\begin{minipage}[t]{0.55\\linewidth}\\textbf{Tổng hợp theo chủ đề SGK (theo ý đầu):}\n" + tab(rows_cd, ["Chủ đề", "Số câu", "Điểm"], "|p{5cm}|c|c|") + "\\end{minipage}"}]
    p1 = qs[:8]
    st[1]["title"] = "Đáp án Phần I"
    st[1]["blocks"] = [
        {"type": "para", "text": "\\textbf{BẢNG ĐÁP ÁN PHẦN I (4,0 ĐIỂM)} [[br]]\n" + tab([[q["blk"]["label"].rstrip("."), q["blk"]["answer"], so(q["diem"]) + "đ"] for q in p1], ["Câu", "Đáp án", "Điểm"], "|c|p{9cm}|c|")},
        {"type": "para", "text": "\\textbf{GIẢI THÍCH CHI TIẾT} [[br]] " + " [[br]] ".join(f"\\textbf{{{q['blk']['label']}}} {q['blk']['solution']}" for q in p1)}]
    for i, (ten_st, os_) in ((2, ("Đáp án Bài 1 -- Bài 3", ("B1", "B2", "B3"))), (3, ("Đáp án Bài 4 và Bài 5", ("B4", "B5")))):
        st[i]["title"] = ten_st
        st[i]["blocks"] = [{"type": "para", "text": f"\\textbf{{ĐÁP ÁN {q['blk']['label'].rstrip('.').upper()}.}} {q['blk']['statement']} [[br]] {q['blk']['solution']}"}
                           for q in qs if q["o"] in os_]
    st[4]["title"] = "Hướng dẫn chấm"
    st[4]["blocks"] = [{"type": "para", "text": "\\textbf{HƯỚNG DẪN CHẤM CHUNG} \\begin{itemize}"
                        "\\item Phần I: mỗi câu đúng $0{,}5$đ; câu có 2 chỗ trống hoặc 2 ý Đúng/Sai: mỗi chỗ đúng $0{,}25$đ."
                        "\\item Bài 1: mỗi phép tính $0{,}5$đ (đặt tính thẳng cột, thẳng dấu phẩy $0{,}25$đ; kết quả đúng $0{,}25$đ)."
                        "\\item Bài 2: mỗi chỗ điền đúng $0{,}25$đ. Bài 3: mỗi ý $0{,}5$đ, làm đúng bước đầu được $0{,}25$đ."
                        "\\item Bài 4: câu lời giải sai nhưng phép tính đúng vẫn cho điểm phép tính; thiếu hoặc sai đơn vị ở đáp số trừ $0{,}25$đ."
                        "\\item Điểm toàn bài làm tròn thành số nguyên theo Thông tư 27 ($\\ge 0{,}5$ làm tròn lên)."
                        "\\end{itemize}"}]
    (DIR / f"{slug_mt(k)}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    return tong, tg


# ------------------------------------------------------------------ gom + vá + chạy
def gom():
    xong = ROOT / "storage/gemini/xong"
    data = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    for k in KH:
        f = xong / f"de5-{k}.json"
        if f.exists():
            kq = json.loads(f.read_text())["ket_qua"]
            data[k] = {"o_cau": {q["o"]: q for q in kq["o_cau"]}, "ghi_chu": kq.get("ghi_chu", "")}
            print(f"gom {k}: {len(kq['o_cau'])} ô — ghi chú: {kq.get('ghi_chu', '')[:300]}")
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# VÁ CỦA CLAUDE sau khi soát (k, ô, trường, giá trị) — không sửa ck1_lop5_de.json tay, để còn gom lại được.
VA = [
    ("on1", "B4", "y", ["Tính diện tích thửa ruộng.",  # bỏ "Em hãy giúp An" (cấm xưng hô em, Thầy 04/11)
                         "Hỏi thửa ruộng thu được mấy tạ thóc, biết rằng mỗi mét vuông thu được $0{,}6$ kg thóc?"]),
    ("on2", "B5", "de_bai", "Tính nhanh: $0{,}1 + 0{,}2 + 0{,}3 + 0{,}4 + \\cdots + 9{,}6 + 9{,}7 + 9{,}8 + 9{,}9 + 10$"),
    ("on2", "C6", "tikz", "\\begin{tikzpicture}[scale=0.42]\\draw[step=1,gray!35,very thin] (0,0) grid (11,6);\\draw[thick] (0,0)--(10.5,0)--(7,5)--cycle;\\draw[thick] (7,5)--(7,0);\\draw (7,0) rectangle (7.5,0.5);\\node[below] at (0,0) {$B$};\\node[below] at (10.5,0) {$C$};\\node[below] at (7,0) {$H$};\\node[above] at (7,5) {$A$};\\node[below] at (3.5,-0.9) {\\small $7$ dm};\\node[below] at (8.9,-0.9) {\\small $3{,}5$ dm};\\node[left] at (7,2.3) {\\small $5$ dm};\\end{tikzpicture}"),  # vẽ lại: nhãn H đè "3,5 dm" (soi PDF 15/11)
    ("ct2", "B2", "de_bai", "Viết số thích hợp vào chỗ chấm:"),  # ý c đề gốc ra 424 ha (số tự nhiên)
    ("ct1", "B5", "de_bai", "An đi từ $A$ đến $B$ theo đường như hình vẽ. Tính độ dài quãng đường An đi, biết độ dài quãng đường $AB$ là $24$ m."),
    ("ct2", "B4", "dap_an", "a) $6\\,000$ m$^2$; b) $36$ tạ"),
    ("ct2", "B1", "dap_an", "$604{,}7$; $37{,}71$; $37{,}284$; $60$"),
    ("ct2", "B2", "dap_an", "$12{,}8$; $7{,}125$; $424$; $0{,}177$"),
]


def main():
    if "--gom" in sys.argv:
        gom()
        return
    data = json.loads(DATA.read_text(encoding="utf-8"))
    for k, o, truong, gt in VA:
        data[k]["o_cau"][o][truong] = gt
    DIR.mkdir(parents=True, exist_ok=True)
    for k in KH:
        if k not in data:
            print(f"thiếu dữ liệu {k}")
            continue
        qs = []
        for i, (o, _, _) in enumerate(KH[k]):
            qs.append(lam_cau(k, o, data[k]["o_cau"][o], i + 1))
        assert abs(sum(q["diem"] for q in qs) - 10) < 1e-9
        dung_de(k, qs)
        tong, tg = dung_ma_tran(k, qs)
        print(f"✓ {TEN[k]}: M1 {so(tong[1][1])}đ · M2 {so(tong[2][1])}đ · M3 {so(tong[3][1])}đ · {so(tg)} phút")


if __name__ == "__main__":
    main()
