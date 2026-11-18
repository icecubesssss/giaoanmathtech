#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p1-ch7-9c-{lt,lop,btvn} vào seed Phiếu 1 ch.VII 9C + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p1_ch7_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p1_ch7_9c.py --ghi    # ghi seed (tạo mới nếu chưa có)

ĐỀ bài + hình lấy từ sơ đồ của Claude (so_do_p1_ch7_9c.KHOI — nguồn sự thật), Gemini góp LỜI GIẢI, lời giải ví dụ,
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
from so_do_p1_ch7_9c import DAP_DS, DAP_TN, KHOI, OPTIONS, latex  # noqa: E402
NGAN = set(DAP_TN) | set(DAP_DS)   # bài toàn câu ngắn (18/11): không đòi dòng Vậy
from viec_dung_p1_ch7_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

KHUNG = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-1-phuong-trinh-bac-hai-bien-luan-so-nghiem.json"
CAM = [r"[Kk]huôn", r"Câu I\b", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"\\Rightarrow", r"⇒", r"dạng đề", r"TODO", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ",
       r"\d–\d ô", r"MỘT bước", r"Dòng Vậy", r"tabular", r"HÌNH/BẢNG", r"\]\]\]\]\]", r"\[\[fill:\$", r"sơ đồ"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá)
    "Bài 1.": ["Chọn B"], "Ví dụ 1.": ["38"], "Bài 3.": ["6", "9", "5"], "Ví dụ 2.": ["33"],
    "Bài 2.": ["31", "14"], "Ví dụ 3.": ["chọnB", "75", "300", "25\\%"], "Bài 4.": ["14", "28\\%"],
    "Bài 5.": ["5", "12{,}5\\%"], "Bài 6.": ["10", "12", "25\\%"], "Bài 7.": ["86", "17{,}2\\%"],
    "Bài 8.": ["1190", "10\\%"], "Bài 9.": ["100", "35\\%"], "Bài 10.": ["15{,}63\\%", "6{,}25\\%"],
    "Bài 11.": ["4", "8\\%"], "Ví dụ 4.": ["15", "chọnB"], "Bài 12.": ["50"],
    "Ví dụ 5.": ["30\\%", "40\\%"], "Ví dụ 6.": ["32{,}5\\%"], "Bài 14.": ["20", "45\\%"],
    "Bài 13.": ["40", "30\\%"], "Ví dụ 7.": ["116", "58\\%"], "Bài 15.": ["21", "52{,}5\\%"], "Bài 16.": ["51", "34\\%"],
    "Bài 17.": ["5", "25\\%"], "Ví dụ 8.": ["33{,}75\\%", "54"], "Bài 18.": ["40\\%", "80"],
    "Ví dụ 9.": ["43{,}75\\%", "105"], "Bài 19.": ["60\\%", "120"], "Ví dụ 10.": ["37{,}5\\%", "12"],
    "Bài 20.": ["19", "30\\%"], "Bài 21.": ["7"], "Ví dụ 11.": ["15\\%", "42", "70\\%"],
    "Bài 22.": ["37{,}5\\%", "50\\%"], "Bài 23.": ["17{,}5\\%", "25\\%", "8"],
    "Bài 24.": ["13", "11"], "Bài 25.": ["50", "40\\%"], "Bài 26.": ["9", "8"], "Bài 27.": ["1440", "19{,}44\\%"],
    "Bài 28.": ["25\\%"], "Bài 29.": ["25\\%"], "Bài 30.": ["20\\%"], "Bài 31.": ["6", "15\\%"],
    "Bài 32.": ["40\\%"], "Bài 33.": ["70"], "Bài 34.": ["18"], "Bài 35.": ["37{,}5\\%", "12{,}5\\%"],
    "Bài 36.": ["32{,}5\\%", "17{,}5\\%"], "Bài 37.": ["35\\%", "40\\%"], "Bài 38.": ["39", "28"],
    "Bài 39.": ["8"], "Bài 40.": ["48", "31{,}25\\%"], "Bài 41.": ["105", "90"], "Bài 42.": ["33\\%", "200"],
    "Bài 43.": ["5", "4"], "Bài 44.": ["9", "18{,}75\\%"],
}

for _n, _c in DAP_TN.items():          # 18/11 câu NB đổi trắc nghiệm / Đúng–Sai: soát chữ cái + Đúng/Sai
    DAP[_n] = [x for x in DAP.get(_n, []) if False] + [f"Chọn{c}" for c in _c]
for _n, _c in DAP_DS.items():
    DAP[_n] = DAP.get(_n, []) + sorted({"Đúng" if c == "Đ" else "Sai" for c in _c})

MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"Tần số và tần số tương đối",
    "branches": [
        {"label": "Bảng tần số", "children": [
            {"label": r"Tần số: số [[blank:2.2cm]] của giá trị"},
            {"label": r"Tổng các tần số $=$ [[blank:1.8cm]]"}]},
        {"label": "Tần số tương đối", "children": [
            {"label": r"$f=[[blank:1.4cm]]\cdot 100\%$"},
            {"label": r"Biết $f$ và $n$: $m=[[blank:1.4cm]]$"}]},
        {"label": "Ghép nhóm", "children": [
            {"label": r"Nhóm $[a; b)$: $a\le x[[blank:0.8cm]]b$"},
            {"label": r"Giá trị đại diện: [[blank:1.8cm]]"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: lần xuất hiện · cỡ mẫu $n$ · $\dfrac{m}{n}$ · $n\cdot f$ · $<$ · "
             r"$\dfrac{a+b}{2}$.")

VID_SUA = ("sua-p1-ch7-9c", "sua2-p1-ch7-9c", "sua3-p1-ch7-9c")   # việc sửa nhỏ đợt sau (đè theo nhãn)
SUA = {}              # nhãn → [(cũ, mới)] trong solution
SUA_VD = {}           # nhãn → [(cũ, mới)] trong lời giải ví dụ
TN_SUA = []           # [(khoá teacher_notes, cũ, mới)]
LT_SUA = [(r"\textit{(suy ra từ công thức)}", r"\textit{(từ công thức tần số tương đối)}")]   # [(cũ, mới)] trong opener/review/concept


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
    s = re.sub(r"(\[\[br\]\]\s*)*(\\hspace\*\{1\.4em\}\s*)?(\\par\\nopagebreak)", r"\3", s)
    s = re.sub(r"(\\smallskip )\s*(\[\[br\]\]\s*)+", r"\1", s)
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
    """18/11: tách Ví dụ 5 gộp (B23 VD1 + 7.19) thành Ví dụ 5, Ví dụ 6, đổi chỗ Bài 13 ↔ 14, ví dụ sau +1.
    Lời giải Gemini (viết theo nhãn cũ) được tách / chuyển nhãn ở đây, không chạy lại thợ."""
    if "Ví dụ 11." in sua:
        return sua
    moi = dict(sua)
    tieu = r"{\sffamily\bfseries\color{brand}Lời giải}[[br]]"
    v5 = sua["Ví dụ 5."]["statement"]
    a, b = v5.split("[[br]]b) ", 1)
    a = a.replace(tieu + "a) ", tieu + r"\hspace*{1.4em}")
    assert a.startswith(tieu), a[:80]
    moi["Ví dụ 5."] = dict(sua["Ví dụ 5."], statement=a)
    moi["Ví dụ 6."] = dict(sua["Ví dụ 5."], label="Ví dụ 6.", statement=tieu + r"\hspace*{1.4em}" + b)
    for n in range(6, 11):
        moi[f"Ví dụ {n + 1}."] = dict(sua[f"Ví dụ {n}."], label=f"Ví dụ {n + 1}.")
    moi["Bài 13."], moi["Bài 14."] = sua["Bài 14."], sua["Bài 13."]
    moi["Bài 2."], moi["Bài 3."] = sua["Bài 3."], sua["Bài 2."]     # 18/11 đổi chỗ 7.4 ↔ 7.2 (căn trang 5)
    return moi


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
            x[k] = re.sub(r"\b7\.(\d\d?)\b", r"7{.}\1", x[k].replace("–", "--"))
    sua = doi_nhan(sua)
    khoi, loi = dung(sua)

    p = REPO / SEED
    f = json.loads(p.read_text()) if p.exists() else khung()
    f["slug"] = Path(SEED).stem
    f["title"] = "Bài 22--24. Bảng tần số, tần số tương đối, ghép nhóm"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VII · PHIẾU 1"
    f["chuong"] = "chuong-07-tan-so-va-tan-so-tuong-doi"
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
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 23 — đề giữa kì II THCS Nam Từ Liêm 2025--2026: "
            r"đọc biểu đồ để lập bảng tần số ghép nhóm, tính tần số tương đối của một nhóm, đếm theo một điều kiện."
            r"[[br]]Mạch 1--3 luyện đọc bảng, đọc biểu đồ và tính tần số tương đối, Mạch 4--8 luyện các bài tự trình "
            r"bày dẫn tới Bài 23."}
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
