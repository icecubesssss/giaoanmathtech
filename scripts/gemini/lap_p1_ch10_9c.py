#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p1-ch10-9c-{lt,lop,btvn} vào seed Phiếu 1 ch.X 9C (19/11/2026) + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p1_ch10_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p1_ch10_9c.py --ghi    # ghi seed (tạo mới nếu chưa có)

ĐỀ bài + hình + hints lấy từ sơ đồ của Claude (so_do_p1_ch10_9c.KHOI — nguồn sự thật), Gemini góp LỜI GIẢI,
lời giải ví dụ, mở đầu, thẻ lý thuyết. SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import so_do_p1_ch10_9c as SD  # noqa: E402
from viec_dung_p1_ch10_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

KHUNG = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
         "phieu-1-phep-thu-khong-gian-mau-xac-suat-cua-bien-co.json")
CAM = [r"[Kk]huôn", r"Câu IV\b", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"\\Rightarrow", r"⇒", r"dạng đề", r"TODO", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ",
       r"\d–\d (ô|dòng)", r"Dòng Vậy", r"HÌNH ĐÃ VẼ", r"\]\]\]\]\]", r"\[\[fill:\$", r"sơ đồ", r"ĐỌC ẢNH", r"·"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá) — đã máy kiểm ở so_do.kiem()
    "Ví dụ 1.": ["SO", "OM", "SM"], "Bài 1.": ["ChọnC"], "Bài 2.": ["ChọnB", "3"],
    "Ví dụ 2.": ["400\\pi", "4000\\pi"], "Bài 3.": ["310{,}86"], "Bài 4.": ["110"], "Bài 5.": ["1519{,}76"],
    "Bài 6.": ["60"], "Ví dụ 3.": ["1{,}6\\pi", "0{,}4\\pi", "1257"], "Bài 7.": ["47100", "314000"],
    "Ví dụ 4.": ["60\\pi", "96\\pi"], "Bài 8.": ["136\\pi", "15", "320\\pi"], "Ví dụ 5.": ["785", "392{,}5"],
    "Bài 9.": ["196{,}35", "1{,}67"], "Bài 10.": ["O"], "Bài 11.": ["75360"], "Bài 12.": ["ChọnD"],
    "Bài 13.": ["39{,}25"], "Bài 14.": ["1{,}37", "588{,}75"], "Bài 15.": ["12", "100\\pi", "314{,}16"],
    "Bài 16.": ["1177{,}5", "4"],
}
NGAN = {k for k, v in SD.DAP_TN.items()} | {"Bài 1.", "Bài 2.", "Bài 10.", "Bài 12."}

MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"Hình trụ, hình nón, hình cầu",
    "branches": [
        {"label": "Hình trụ", "children": [
            {"label": r"$S_{xq}=[[blank:1.6cm]]$"}, {"label": r"$V=[[blank:1.6cm]]$"}]},
        {"label": "Hình nón", "children": [
            {"label": r"$S_{xq}=[[blank:1.6cm]]$"}, {"label": r"$V=[[blank:1.6cm]]$"},
            {"label": r"$l^2=[[blank:1.6cm]]$"}]},
        {"label": "Hình cầu", "children": [   # 19/11: gộp một dòng cho sơ đồ lọt trang 8 (Thầy "đẩy sơ đồ lên")
            {"label": r"$S=[[blank:1.6cm]]$, \ $V=[[blank:1.6cm]]$"}]},
        {"label": "Vật chìm hẳn", "children": [
            {"label": r"Thể tích vật bằng thể tích phần nước [[blank:1.6cm]]"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $2\pi rh$ · $\pi r^2h$ · $\pi rl$ · $\frac{1}{3}\pi r^2h$ · $r^2+h^2$ · "
             r"$4\pi R^2$ · $\frac{4}{3}\pi R^3$ · dâng lên.")
HINH_LT = {  # thẻ lý thuyết → hình bên phải
    "1": SD._dau(*SD.tru(r="$r$", h="$h$")),
    "2": SD._dau(*SD.non(r="$r$", h="$h$", l="$l$", dinh="$S$", tam="$O$", A="$A$")),
    "3": SD.cau(R_chu="$R$"),
}

VID_SUA = ("sua-p1-ch10-9c",)   # việc sửa nhỏ đợt sau (đè theo nhãn)
SUA = {  # nhãn → [(cũ, mới)] trong solution (cổng sgk_style/trinh_bay 19/11)
    "Bài 7.": [(r"(cm).[[br]]\hspace*{1.4em}Thể tích nước đã sử dụng là", r"(cm) nên thể tích nước đã sử dụng là")],
    "Bài 14.": [(r"(m).[[br]]Thể tích phần nước đã tháo ra ngoài là", r"(m) nên thể tích phần nước đã tháo ra ngoài là")],
}
SUA_VD = {  # nhãn → [(cũ, mới)] trong lời giải ví dụ
    "Ví dụ 1.": [(r"nên $SN$, $SP$ cũng là đường sinh.", r"nên $[[fill:SN]]$, $[[fill:SP]]$ cũng là đường sinh.")],
}
TN_SUA = []           # [(khoá teacher_notes, cũ, mới)]
LT_SUA = []           # [(cũ, mới)] trong opener/review/concept


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def gian_phan_so(s):
    """Dòng có \\dfrac (ô điền ở tử/mẫu) bị sát dòng trên dưới ⇒ thanh chống vô hình CUỐI dòng."""
    return "[[br]]".join(d + r"\rule[-1.2ex]{0pt}{3.7ex}" if "\\dfrac" in d else d for d in s.split("[[br]]"))


def thut_dong(s):
    """BTVN Gemini để dòng chữ sát lề, dòng công thức thụt ⇒ đồng bộ kiểu trên lớp: mọi dòng con thụt 1,4em
    (trừ dòng mở ý "a)", "b)")."""
    d = s.split("[[br]]")
    return "[[br]]".join([d[0]] + [x if re.match(r"\\hspace\*|[a-d]\)", x) else r"\hspace*{1.4em}" + x
                                   for x in d[1:]])


def nhom_so(s):
    """Số nguyên ≥ 5 chữ số trong $…$ ⇒ tách lớp nghìn bằng \\, như SGK (75360 → 75\\,360); bỏ phần thập phân."""
    def tach(m):
        x = m.group(0)
        out = ""
        while len(x) > 3:
            out, x = r"\," + x[-3:] + out, x[:-3]
        return x + out
    # CHỈ trong $…$ (19/11: ăn cả \interlinepenalty=10000 ⇒ in "000" đầu đề)
    return re.sub(r"\$[^$]*\$", lambda m: re.sub(r"(?<![\d}])\d{5,}(?!\d)", tach, m.group(0)), s)


def sach(s):
    return gian_phan_so(nhom_so(s))


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right|\\ |\\text\{|\\mathrm\{|\\approx", "", s or "")
    s = s.replace(r"\frac", r"\dfrac").replace("[[fill:", "").replace("]]", "").replace(".", "")
    return s


def thay(nhan, s, bang):
    for cu, moi in bang.get(nhan, []):
        assert s.count(cu) == 1, (nhan, cu[:70])
        s = s.replace(cu, moi)
    return s


GIU_ON = r"\interlinepenalty=10000\clubpenalty=10000\widowpenalty=10000 "
GIU_OFF = r"\interlinepenalty=0\clubpenalty=150\widowpenalty=150 "
RONG_HINH = 0.34      # cột hình khi kê cạnh ý a), b)
CAO_DUOI = "3.8cm"    # hình đặt dưới đề một đoạn: trần chiều cao


def _chu_hinh(cap):
    return (r"\par\vspace{2pt}{\sffamily\scriptsize\itshape\color{muted}" + cap + "}") if cap else ""


def nhung(de, fig):
    """Renderer luôn hạ `figure` xuống dưới đề trọn ngang (luật 22/09) ⇒ hình khối nhỏ để trơ trắng, hộp ví dụ có
    hình thành khối cứng (trang 6, 8 trắng nửa dưới, 19/11). Nhúng hình vào đề như ch.VII/VIII:
    thân đề trọn ngang, phần sau (a), b)…) minipage trái + hình phải; đề một đoạn ⇒ hình nhỏ căn giữa dưới đề."""
    if not fig:
        return de
    tikz, cap = fig["tikz"], fig.get("caption", "")
    if fig.get("pos") == "below":            # đích: hai ly cạnh nhau, nhãn trong hình
        tr, sau = de.split("[[br]]", 1)
        return (GIU_ON + tr + r"\par\nopagebreak\smallskip\nopagebreak{\centering\adjustbox{width="
                + fig["width"] + r"\linewidth}{" + tikz + r"}\par}\smallskip " + GIU_OFF + sau)
    if "[[br]]" in de:
        tr, sau = de.split("[[br]]", 1)
        rt = 0.97 - RONG_HINH
        return (GIU_ON + tr + r"\par\nopagebreak\smallskip\noindent\begin{minipage}[t]{" + f"{rt:.2f}"
                + r"\linewidth}\vspace{0pt}" + sau + r"\end{minipage}\hfill\begin{minipage}[t]{" + f"{RONG_HINH:.2f}"
                + r"\linewidth}\vspace{0pt}\centering\adjustbox{max width=\linewidth,max totalheight=4.2cm}{"
                + tikz + "}" + _chu_hinh(cap) + r"\end{minipage}\par\smallskip " + GIU_OFF)
    return (GIU_ON + de + r"\par\nopagebreak\smallskip\nopagebreak{\centering\adjustbox{totalheight=" + CAO_DUOI
            + r",max width=0.45\linewidth}{" + tikz + "}" + _chu_hinh(cap) + r"\par}\smallskip " + GIU_OFF)


def dung(sua):
    so = SD.danh_so_hinh()
    out = {"practice1": [], "practice2": [], "reflection": []}
    loi = []
    for k in SD.KHOI:
        chang = k["chang"]
        if "tieu_de" in k:
            out[chang].append({"type": "para", "variant": "heading", "text": k["tieu_de"]})
            continue
        nhan = k["nhan"]
        g = sua.get(nhan)
        if not g:
            loi.append(f"{nhan}: Gemini không trả")
            continue
        de_tex = SD.de_in(k, so)
        fig = SD.hinh_in(k, so)
        if k["ht"] == "vi_du":
            giai = thay(nhan, g["statement"].strip(), SUA_VD)
            if not giai.startswith("{\\sffamily"):
                loi.append(f"{nhan}: lời giải ví dụ không mở bằng tiêu đề Lời giải: {giai[:80]}")
            de_v = nhung(de_tex, fig)
            noi = "" if de_v.rstrip().endswith((r"\smallskip", GIU_OFF.strip())) else "[[br]]"
            out[chang].append({"type": "noted", "variant": "example",
                               "text": sach(r"\textbf{" + nhan + "} " + de_v + noi + giai)})
        else:
            b = {"type": "problem", "label": nhan, "level": k["level"], "tier": k["tier"], "dang_id": k["dang"],
                 "statement": sach(nhung(de_tex, fig)), "solution": sach(thut_dong(thay(nhan, g["solution"], SUA))),
                 "hints": list(k.get("hints", []))}
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
                if nh not in NGAN and not re.search(r"Vậy", txt):
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
        chu = re.sub(r"\$[^$]*\$", "", txt)
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
                                   "solution": x["solution"] or cu.get("solution", "")}
    for x in sua.values():
        for k in ("statement", "solution"):
            x[k] = re.sub(r"\b10\.(\d\d?)\b", r"10{.}\1", x[k].replace("–", "--"))
    khoi, loi = dung(sua)

    p = REPO / SEED
    f = json.loads(p.read_text()) if p.exists() else khung()
    f["slug"] = Path(SEED).stem
    f["title"] = "Bài 31--32. Hình trụ, hình nón, hình cầu"
    f["eyebrow"] = "HÌNH HỌC — CHƯƠNG X · PHIẾU 1"
    f["grade_label"] = "Lớp 9 • Hình học"
    f["chuong"] = "chuong-10-hinh-khoi-trong-thuc-tien"
    f.pop("khuon", None)
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
    the = []
    for b in lt["concept_blocks"]:
        so = re.match(r"\s*(\d)", b.get("title", ""))
        t = {"type": "noted", "variant": "theory", "title": b["title"], "text": b["text"]}
        if so and so[1] in HINH_LT:
            t["figure"] = {"type": "tikz", "tikz": HINH_LT[so[1]], "caption": "", "pos": "right"}
        else:
            loi.append(f"thẻ lý thuyết lạ: {b.get('title')}")
        the.append(t)
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"], blocks=the)
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 9 — Bài 5 đề kiểm tra học kì II THCS Đoàn Thị "
            r"Điểm 2025--2026: tính thể tích nước trong ly hình trụ, rồi từ phần nước dâng lên tìm bán kính viên bi."
            r"[[br]]Mạch 1--2 luyện nhận biết các yếu tố và thay số vào từng công thức, Mạch 3--5 luyện các bài tự "
            r"trình bày dẫn tới Bài 9."}
    for k, ten in (("practice1", "Luyện tập 1 — Nhận biết"), ("practice2", "Luyện tập 2 — Thông hiểu, vận dụng")):
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
