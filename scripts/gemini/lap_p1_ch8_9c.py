#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p1-ch8-9c-{lt,lop,btvn} vào seed Phiếu 1 ch.VIII 9C (19/11/2026) + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p1_ch8_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p1_ch8_9c.py --ghi    # ghi seed (tạo mới nếu chưa có)

ĐỀ bài + hình lấy từ sơ đồ của Claude (so_do_p1_ch8_9c.KHOI — nguồn sự thật), Gemini góp LỜI GIẢI, lời giải ví dụ,
mở đầu, kiến thức cần nhớ. Bảng trong chữ Gemini viết "[[bang: a | b / c | d]]" ⇒ đổi sang tabular ở đây.
Bảng SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert). VID_SUA = việc nhỏ đợt sau, đè theo nhãn.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hinh_thong_ke as HT  # noqa: E402
from so_do_p1_ch8_9c import DAP_DS, DAP_TN, KHOI, NGAN as _NGAN, OPTIONS, latex  # noqa: E402
NGAN = set(DAP_TN) | set(DAP_DS) | _NGAN   # bài toàn câu ngắn: không đòi dòng Vậy
from viec_dung_p1_ch8_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

KHUNG = "inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/phieu-1-bang-tan-so-tan-so-tuong-doi-ghep-nhom.json"
CAM = [r"[Kk]huôn", r"Câu I\b", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"\\Rightarrow", r"⇒", r"dạng đề", r"TODO", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ",
       r"\d–\d ô", r"MỘT bước", r"Dòng Vậy", r"tabular", r"HÌNH/BẢNG", r"\]\]\]\]\]", r"\[\[fill:\$", r"sơ đồ"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá) — đã máy kiểm ở so_do.kiem()
    "Ví dụ 2.": ["14"], "Bài 4.": ["6"], "Ví dụ 3.": ["12"], "Bài 6.": ["T},B)", "T},C)"],
    "Bài 7.": ["16", "(2,2)"], "Ví dụ 5.": ["\\dfrac{1}{3}", "\\dfrac{1}{2}"], "Ví dụ 6.": ["12", "\\dfrac{2}{5}"],
    "Bài 11.": ["36"], "Ví dụ 7.": ["\\dfrac{7}{20}"], "Bài 12.": ["\\dfrac{4}{69}"],
    "Ví dụ 8.": ["\\dfrac{3}{20}", "\\dfrac{11}{20}"], "Bài 13.": ["40", "\\dfrac{1}{5}"],
    "Bài 14.": ["42", "\\dfrac{1}{2}", "\\dfrac{3}{14}"], "Bài 15.": ["9"], "Ví dụ 9.": ["\\dfrac{1}{3}", "\\dfrac{1}{6}"],
    "Bài 16.": ["36", "\\dfrac{5}{18}", "\\dfrac{11}{36}"], "Bài 17.": ["10", "\\dfrac{1}{5}", "\\dfrac{3}{5}"],
    "Ví dụ 10.": ["\\dfrac{1}{3}"], "Bài 18.": ["55", "95", "\\dfrac{1}{3}"], "Bài 19.": ["\\dfrac{1}{3}", "\\dfrac{5}{9}"],
    "Ví dụ 11.": ["20", "\\dfrac{3}{20}"], "Bài 20.": ["15", "\\dfrac{2}{15}"], "Bài 21.": ["59", "\\dfrac{30}{59}"],
    "Ví dụ 12.": ["15", "\\dfrac{3}{20}"], "Bài 22.": ["\\dfrac{3}{8}"], "Bài 23.": ["99", "\\dfrac{4}{25}"],
    "Ví dụ 13.": ["\\dfrac{1}{5}"], "Bài 24.": ["8", "\\dfrac{1}{4}"],
    "Bài 28.": ["6"], "Bài 29.": ["10", "7"], "Bài 31.": ["\\dfrac{3}{8}"], "Bài 32.": ["\\dfrac{1}{4}"],
    "Bài 33.": ["\\dfrac{1}{2}"], "Bài 34.": ["\\dfrac{1}{4}"], "Bài 35.": ["\\dfrac{1}{5}"], "Bài 36.": ["\\dfrac{2}{3}"],
    "Bài 37.": ["\\dfrac{3}{4}"], "Bài 40.": ["8", "\\dfrac{3}{5}"], "Bài 41.": ["\\dfrac{3}{20}"],
    "Bài 42.": ["103", "0{,}22"], "Bài 43.": ["15", "\\dfrac{1}{3}"], "Bài 44.": ["20", "\\dfrac{1}{10}"],
    "Bài 45.": ["16", "\\dfrac{2}{5}"], "Bài 46.": ["16", "\\dfrac{1}{4}", "\\dfrac{5}{16}"],
    "Bài 47.": ["\\dfrac{3}{8}", "\\dfrac{7}{8}"], "Bài 48.": ["36", "\\dfrac{1}{6}", "\\dfrac{4}{9}"],
    "Bài 49.": ["\\dfrac{1}{2}", "\\dfrac{2}{3}"],
}

for _n, _c in DAP_TN.items():          # 18/11 câu NB đổi trắc nghiệm / Đúng–Sai: soát chữ cái + Đúng/Sai
    DAP[_n] = [x for x in DAP.get(_n, []) if False] + [f"Chọn{c}" for c in _c]
for _n, _c in DAP_DS.items():
    DAP[_n] = DAP.get(_n, []) + sorted({"Đúng" if c == "Đ" else "Sai" for c in _c})

MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"Xác suất của biến cố",
    "branches": [
        {"label": "Không gian mẫu", "children": [
            {"label": r"$\Omega$: tập hợp tất cả các [[blank:2.4cm]]"},
            {"label": r"Hai hành động: kết quả là một [[blank:1.4cm]], lập bảng"}]},
        {"label": "Biến cố", "children": [
            {"label": r"$n(A)$: số kết quả [[blank:1.8cm]] cho $A$"}]},
        {"label": "Xác suất", "children": [
            {"label": r"Các kết quả [[blank:2.2cm]]"},
            {"label": r"$P(A)=[[blank:1.4cm]]$"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: kết quả có thể của phép thử · cặp · thuận lợi · đồng khả năng · "
             r"$\dfrac{n(A)}{n(\Omega)}$.")

VID_SUA = ("sua-p1-ch8-9c", "sua2-p1-ch8-9c")   # việc sửa nhỏ đợt sau (đè theo nhãn)
SUA = {}              # nhãn → [(cũ, mới)] trong solution
SUA_VD = {  # nhãn → [(cũ, mới)] trong lời giải ví dụ
    "Ví dụ 13.": [("Từ $1$ đến $15$, các số chia hết", "Các số ghi trên thẻ chia hết")],
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
    return sua


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
            x[k] = re.sub(r"\b8\.(\d\d?)\b", r"8{.}\1", x[k].replace("–", "--"))
    sua = doi_nhan(sua)
    khoi, loi = dung(sua)

    p = REPO / SEED
    f = json.loads(p.read_text()) if p.exists() else khung()
    f["slug"] = Path(SEED).stem
    f["title"] = "Bài 25--26. Phép thử ngẫu nhiên, không gian mẫu và xác suất của biến cố"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VIII · PHIẾU 1"
    f["chuong"] = "chuong-08-xac-suat-cua-bien-co"
    f.pop("kiem_tra_phut", None)
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
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"],
              blocks=[dict(b, text=sach(b["text"])) for b in lt["concept_blocks"]])
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 24 — Câu I.2 đề tuyển sinh lớp 10 Hà Nội "
            r"2025--2026: xác định không gian mẫu, liệt kê các kết quả thuận lợi cho biến cố và tính xác suất."
            r"[[br]]Mạch 1--5 luyện nhận biết phép thử, không gian mẫu, kết quả thuận lợi và công thức xác suất, "
            r"Mạch 6--9 luyện các bài tự trình bày dẫn tới Bài 24."}
    for k, ten in (("practice1", "Luyện tập 1 — Nhận biết"), ("practice2", "Luyện tập 2 — Thông hiểu")):
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
