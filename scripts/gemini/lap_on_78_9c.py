#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-on78-9c-{lt,lop,btvn} vào seed Phiếu 2 ch.VIII 9C — Ôn tập chương VII + VIII (19/11/2026).

    .venv/bin/python scripts/gemini/lap_on_78_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_on_78_9c.py --ghi    # ghi seed (tạo mới nếu chưa có)

ĐỀ bài + hình lấy từ sơ đồ của Claude (so_do_on_78_9c.KHOI — nguồn sự thật), Gemini góp LỜI GIẢI, lời giải ví dụ,
mở đầu, ghi chú GV. Kiến thức cần nhớ chép nguyên văn từ hai Phiếu 1 (ch.VII mục 1, 3, 4 + ch.VIII mục 1–4). Bảng trong chữ Gemini viết "[[bang: a | b / c | d]]" ⇒ đổi sang tabular ở đây.
Bảng SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert). VID_SUA = việc nhỏ đợt sau, đè theo nhãn.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinh_thong_ke as HT  # noqa: E402
from so_do_on_78_9c import DAP_DS, DAP_TN, KHOI, NGAN as _NGAN, OPTIONS, latex  # noqa: E402
NGAN = set(DAP_TN) | set(DAP_DS) | _NGAN   # bài toàn câu ngắn: không đòi dòng Vậy
from viec_dung_on_78_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

P1_CH7 = "inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/phieu-1-bang-tan-so-tan-so-tuong-doi-ghep-nhom.json"
P1_CH8 = "inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/phieu-1-phep-thu-khong-gian-mau-xac-suat-cua-bien-co.json"
KHUNG = P1_CH8
CAM = [r"[Kk]huôn", r"Câu I\b", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"\\Rightarrow", r"⇒", r"dạng đề", r"TODO", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ",
       r"\d–\d ô", r"MỘT bước", r"Dòng Vậy", r"tabular", r"HÌNH/BẢNG", r"\]\]\]\]\]", r"\[\[fill:\$", r"sơ đồ"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá) — đã máy kiểm ở so_do.kiem()
    "Bài 1.": ["9", "22{,}5"], "Bài 2.": ["40", "17{,}5"], "Bài 3.": ["450", "42"], "Bài 4.": ["61"],
    "Bài 5.": ["20", "40"], "Bài 6.": ["10", "20"], "Bài 7.": ["40"], "Bài 9.": ["9"],
    "Bài 11.": ["\\dfrac{1}{5}"], "Bài 12.": ["\\dfrac{32}{81}"], "Bài 13.": ["\\dfrac{7}{34}", "\\dfrac{27}{34}"],
    "Ví dụ 1.": ["32{,}5", "12{,}5", "75"], "Bài 14.": ["37{,}5", "17{,}5"], "Ví dụ 2.": ["12", "40"],
    "Bài 15.": ["17", "42{,}5", "22{,}5"], "Ví dụ 3.": ["27{,}5", "67{,}5"], "Bài 16.": ["65", "81{,}25"],
    "Ví dụ 4.": ["\\dfrac{1}{2}"], "Bài 17.": ["\\dfrac{1}{5}"], "Ví dụ 5.": ["45", "\\dfrac{1}{9}"],
    "Bài 18.": ["500", "\\dfrac{1}{100}", "\\dfrac{1}{250}"], "Ví dụ 6.": ["46", "\\dfrac{7}{46}", "\\dfrac{7}{23}"],
    "Bài 19.": ["66", "\\dfrac{17}{33}", "\\dfrac{4}{11}"], "Ví dụ 7.": ["15", "\\dfrac{2}{15}", "\\dfrac{3}{5}"],
    "Bài 20.": ["36", "\\dfrac{1}{18}", "\\dfrac{5}{18}"], "Bài 21.": ["50", "\\dfrac{1}{6}"],
    "Bài 22.": ["12"], "Bài 23.": ["30"], "Bài 24.": ["10"], "Bài 25.": ["18{,}3"], "Bài 26.": ["25"],
    "Bài 27.": ["50", "40"], "Bài 28.": ["30", "50", "20"], "Bài 29.": ["36"], "Bài 30.": ["140", "75"],
    "Bài 31.": ["\\dfrac{1}{2}"], "Bài 32.": ["\\dfrac{1}{6}", "\\dfrac{1}{3}"],
    "Bài 33.": ["15", "55", "30"], "Bài 34.": ["33", "15"], "Bài 35.": ["27"], "Bài 36.": ["540", "460", "340"],
    "Bài 37.": ["27{,}5", "7{,}5"], "Bài 38.": ["\\dfrac{1}{2}", "\\dfrac{7}{60}"], "Bài 39.": ["\\dfrac{2}{5}"], "Bài 40.": ["\\dfrac{3}{10}"],
    "Bài 41.": ["\\dfrac{2}{15}", "\\dfrac{23}{30}"], "Bài 42.": [],
}

for _n, _c in DAP_TN.items():          # 18/11 câu NB đổi trắc nghiệm / Đúng–Sai: soát chữ cái + Đúng/Sai
    DAP[_n] = [x for x in DAP.get(_n, []) if False] + [f"Chọn{c}" for c in _c]
for _n, _c in DAP_DS.items():
    DAP[_n] = DAP.get(_n, []) + sorted({"Đúng" if c == "Đ" else "Sai" for c in _c})

MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt phần ôn tập",
    "root": r"Thống kê và xác suất",
    "branches": [
        {"label": "Tần số", "children": [
            {"label": r"Tần số tương đối $f=[[blank:2.2cm]]$"},
            {"label": r"Nhóm $[a; b)$ không chứa [[blank:1.2cm]]"}]},
        {"label": "Không gian mẫu", "children": [
            {"label": r"$\Omega$: tập hợp tất cả các [[blank:2.4cm]]"},
            {"label": r"Hai hành động: kết quả là một [[blank:1.4cm]]"}]},
        {"label": "Xác suất", "children": [
            {"label": r"Các kết quả [[blank:2.2cm]]"},
            {"label": r"$P(A)=[[blank:1.4cm]]$"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $\dfrac{m}{n}\cdot 100\%$ · đầu mút phải $b$ · kết quả có thể của phép thử · cặp · "
             r"đồng khả năng · $\dfrac{n(A)}{n(\Omega)}$.")

VID_SUA = ("sua-on78-9c", "sua2-on78-9c")   # việc sửa nhỏ đợt sau (đè theo nhãn)
SUA = {}              # nhãn → [(cũ, mới)] trong solution
SUA_VD = {  # nhãn → [(cũ, mới)] trong lời giải ví dụ (vi_du_gate: ô trên, số in sẵn dưới)
    "Ví dụ 5.": [("Các bội của $9$ có hai chữ số là $18, 27, 36, 45, 54, 63, 72, 81, 90, 99$, trong đó các số lẻ là",
                  "Các số lẻ có hai chữ số là bội của $9$ là")],
    "Ví dụ 7.": [("Vậy $P(E)=\\frac{2}{15}$", "Vậy $P(E)=[[fill:\\frac{2}{15}]]$")],
}
TN_SUA = []           # [(khoá teacher_notes, cũ, mới)]
LT_SUA = []   # [(cũ, mới)] trong opener/review/concept


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def doi_bang(s):
    """[[bang: a | b / c | d]] → tabular (đếm cặp [[ ]] để ô [[fill:…]] lồng bên trong không làm gãy)."""
    out, i = [], 0
    while True:
        j = s.find("[[bang:", i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k, sau = j + 2, 1
        while sau:
            a, b = s.find("[[", k), s.find("]]", k)
            if a != -1 and a < b:
                sau, k = sau + 1, a + 2
            else:
                sau, k = sau - 1, b + 2
        noi = s[j + 7:k - 2].strip()
        hang = [[c.strip() for c in h.split(" | ")] for h in re.split(r"\s+/\s+(?![^\[]*\]\])", noi)]
        out.append(HT.bang(hang))
        i = k
    return "".join(out)


def gian_phan_so(s):
    """Dòng có \\dfrac (ô điền ở tử/mẫu) bị sát dòng trên dưới (Thầy 18/11) ⇒ thêm thanh chống vô hình CUỐI dòng
    (cuối dòng để không đụng luật \\hspace* đầu dòng của trinh_bay_gate)."""
    return "[[br]]".join(d + r"\rule[-1.2ex]{0pt}{3.7ex}" if "\\dfrac" in d and "tabular" not in d else d
                         for d in s.split("[[br]]"))


def sach(s):
    """Bỏ [[br]] / \\hspace* sát khối center (TeX: "There's no line here to end")."""
    s = gian_phan_so(doi_bang(s))
    s = s.replace("); (", r"); \allowbreak (")   # 19/11: tập Ω 16 cặp trong $…$ không ngắt được ⇒ tràn lề
    s = re.sub(r"(\[\[br\]\]\s*)*(\\hspace\*\{1\.4em\}\s*)?(\\par\\nopagebreak)", r"\3", s)
    s = re.sub(r"(\\smallskip )\s*(\[\[br\]\]\s*)+", r"\1", s)
    s = re.sub(r"(\\smallskip )\s*\\hspace\*\{1\.4em\}", r"\1", s)   # trinh_bay_gate: \hspace* giữa dòng sau bảng
    return s


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right|\\ |\\text\{|\\mathrm\{", "", s or "")
    s = s.replace(r"\frac", r"\dfrac").replace("[[fill:", "").replace("]]", "").replace("[[bang:", "")
    return s


def thay(nhan, s, bang):
    for cu, moi in bang.get(nhan, []):
        assert s.count(cu) == 1, (nhan, cu[:70])
        s = s.replace(cu, moi)
    return s


def doi_nhan(sua):
    """Gemini viết theo nhãn cũ; sơ đồ đã đổi thứ tự BTVN (DOI_NHAN_BTVN)."""
    from so_do_on_78_9c import DOI_NHAN_BTVN
    out = {}
    for nh, x in sua.items():
        m = re.match(r"Bài (\d+)\.", nh)
        moi = f"Bài {DOI_NHAN_BTVN.get(int(m[1]), int(m[1]))}." if m else nh
        out[moi] = dict(x, label=moi)
    return out


def dung(sua):
    out = {"practice1": [], "practice2": [], "reflection": []}
    loi = []
    for k in KHOI:
        chang = k[1]
        if len(k) == 3:
            out[chang].append({"type": "para", "variant": "heading", "text": k[0]})
            continue
        nhan, _, tier, dang, level, _, _, ht, de, _ = k
        g = sua.get(nhan)
        if not g:
            loi.append(f"{nhan}: Gemini không trả")
            continue
        de_tex = latex(de, nhan)
        if ht == "vi_du":
            giai = thay(nhan, g["statement"].strip(), SUA_VD)
            if not giai.startswith("{\\sffamily"):
                loi.append(f"{nhan}: lời giải ví dụ không mở bằng tiêu đề Lời giải: {giai[:80]}")
            noi = "" if de_tex.rstrip().endswith(r"\smallskip") else "[[br]]"
            out[chang].append({"type": "noted", "variant": "example",
                               "text": sach(r"\textbf{" + nhan + "} " + de_tex + noi + giai)})
        else:
            b = {"type": "problem", "label": nhan, "level": level, "tier": tier, "dang_id": dang,
                 "statement": sach(de_tex), "solution": sach(thay(nhan, g["solution"], SUA)),
                 "hints": list(g.get("hints") or [])}
            if nhan in OPTIONS:
                b["options"] = OPTIONS[nhan]
            out[chang].append(b)
    return out, loi


def soat(stages, lt, tho):
    loi = []
    phan_gemini = [("lt", json.dumps({k: v for k, v in lt.items() if k != "ghi_chu"}, ensure_ascii=False))]
    phan_gemini += [(nh, x["solution"] + x["statement"]) for nh, x in tho.items()]
    for s in stages:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                nh, txt = b["label"], b["solution"]
                if not txt.strip():
                    loi.append(f"{nh}: thiếu lời giải")
                if not b.get("options") and nh not in NGAN and not re.search(r"Vậy", txt):
                    loi.append(f"{nh}: lời giải không có dòng Vậy")
            elif b.get("variant") == "example":
                nh = re.match(r"\\textbf\{([^}]*)\}", b["text"]).group(1)
                txt = b["text"].split("{\\sffamily", 1)[-1]
                nf = txt.count("[[fill:")
                if nf < 4:
                    loi.append(f"{nh}: ví dụ ít ô fill ({nf})")
                if re.search(r"\[(NB|TH|VD)\]", txt):
                    loi.append(f"{nh}: ví dụ có thẻ mức")
                if not re.search(r"Vậy", txt):
                    loi.append(f"{nh}: ví dụ không có dòng Vậy")
            else:
                continue
            for d in DAP.get(nh, []):
                if chuan(d) not in chuan(txt):
                    loi.append(f"{nh}: không thấy đáp số {d}")
    for ten, txt in phan_gemini:
        for pat in CAM:
            for mm in re.finditer(pat, txt):
                loi.append(f"[{ten}] /{pat}/: …{txt[max(0, mm.start() - 50): mm.end() + 30]}…")
        chu = re.sub(r"\$[^$]*\$", "", txt)          # dấu ";" trong nửa khoảng $[a; b)$ là đúng SGK
        for mm in re.finditer(r"(?<!\\);", chu):
            loi.append(f"[{ten}] dấu ';': …{chu[max(0, mm.start() - 40): mm.end() + 20]}…")
    return loi


def kien_thuc():
    """Kiến thức cần nhớ = nguyên văn SGK đã dựng ở hai Phiếu 1: ch.VII mục 1, 3, 4 + ch.VIII mục 1–4 (đánh số lại)."""
    def cap(path):
        b = json.loads((REPO / path).read_text())["stages"][1]["blocks"]
        return [(b[i], b[i + 1]) for i in range(0, len(b), 2)]
    c7, c8 = cap(P1_CH7), cap(P1_CH8)
    chon = [c7[0], c7[2], c7[3]] + c8
    out = []
    for i, (h, nd) in enumerate(chon, 1):
        assert h.get("variant") == "heading", h
        ten = re.sub(r"^\d+\.\s*", "", h["text"])
        out += [dict(h, text=f"{i}. {ten}"), dict(nd)]
    return out


def khung():
    p = json.loads((REPO / KHUNG).read_text())
    f = {k: v for k, v in p.items() if k != "stages"}
    f["stages"] = [{"kind": st["kind"], "number": st["number"], "title": st["title"], "blocks": []}
                   for st in p["stages"]]
    return f


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    sua = {x["label"]: x for x in lop["sua"] + btvn["sua"]}
    for vid in VID_SUA:
        if (REPO / "storage/gemini/xong" / f"{vid}.json").exists():
            for x in lay(vid)["sua"]:
                cu = sua.get(x["label"], {})
                sua[x["label"]] = {"label": x["label"], "statement": x["statement"] or cu.get("statement", ""),
                                   "solution": x["solution"] or cu.get("solution", ""),
                                   "hints": x.get("hints") or cu.get("hints", [])}
    for x in sua.values():
        for k in ("statement", "solution"):
            x[k] = re.sub(r"\b([78])\.(\d\d?)\b", r"\1{.}\2", x[k].replace("–", "--"))
    sua = doi_nhan(sua)
    khoi, loi = dung(sua)

    p = REPO / SEED
    f = json.loads(p.read_text()) if p.exists() else khung()
    f["slug"] = Path(SEED).stem
    f["title"] = "Ôn tập chương VII và VIII. Tần số, tần số tương đối và xác suất của biến cố"
    f["eyebrow"] = "ĐẠI SỐ — ÔN TẬP CHƯƠNG VII + VIII · PHIẾU 2"
    f["chuong"] = "chuong-08-xac-suat-cua-bien-co"
    f["kiem_tra_phut"] = 45
    f["luat_16_11"], f["khuon"], f["btvn_phieu_rieng"] = True, "khong_vd", True
    tn = lt["teacher_notes"]
    for k, cu, moi in TN_SUA:
        assert tn[k].count(cu) == 1, (k, cu)
        tn[k] = tn[k].replace(cu, moi)
    for cu, moi in LT_SUA:
        for k in ("opener_text", "review_note"):
            lt[k] = lt[k].replace(cu, moi)
        for b in lt["concept_blocks"]:
            b["text"] = b["text"].replace(cu, moi)
    st = {s["kind"]: s for s in f["stages"]}
    rv = st["review"]
    rv.update(title="Khám phá", solution="", teacher_note=tn["review"])
    rv["blocks"] = [{"type": "opener", "text": lt["opener_text"]},
                    {"type": "noted", "variant": "note",
                     "text": r"\textbf{Nhắc lại kiến thức đã học.}[[br]]" + lt["review_note"]}]
    cp = st["concept"]
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"], blocks=kien_thuc())
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 21 — Câu I đề học kì II THCS Bế Văn Đàn "
            r"2025--2026: đọc biểu đồ tần số ghép nhóm, tính tần số tương đối và tính xác suất của biến cố."
            r"[[br]]Mạch 1--4 ôn nhanh các câu nhận biết của hai chương, Mạch 5--8 luyện các bài tự trình bày như "
            r"đi thi, không gợi ý, dẫn tới Bài 21."}
    for k, ten in (("practice1", "Luyện tập 1 — Nhận biết"), ("practice2", "Luyện tập 2 — Thông hiểu (như đi thi)")):
        st[k].update(title=ten, teacher_note=tn[k], blocks=([dich] if k == "practice1" else []) + khoi[k])
        st[k].pop("solution", None)
    rf = st["reflection"]
    rf["title"] = "Tổng kết"
    rf["blocks"] = [MINDMAP, {"type": "para", "text": r"\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."}] \
        + khoi["reflection"]
    rf["solution"] = GIAI_BTVN
    rf["teacher_note"] = tn.get("reflection", "")

    loi += soat([st[k] for k in ("practice1", "practice2", "reflection")], lt, sua)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
