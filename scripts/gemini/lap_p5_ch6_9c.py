#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p5-ch6-9c-{lt,lop,btvn} vào seed Phiếu 5 ch.VI 9C bản 2 + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p5_ch6_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p5_ch6_9c.py --ghi    # ghi seed (tạo mới nếu chưa có)

ĐỀ bài lấy từ sơ đồ của Claude (so_do_p5_ch6_9c.KHOI — nguồn sự thật), Gemini chỉ góp LỜI GIẢI, text ví dụ, mở đầu.
Kiến thức cần nhớ = chép các khối lý thuyết đã qua cổng của Phiếu 1, 2, 4 (đánh số lại), không giao viết mới.
Soát: đủ nhãn, từ cấm, ";", ⇔, Δ′, ô "]]]", "[[fill:$"; ví dụ đủ ô và đề khớp sơ đồ; đáp số then chốt có mặt.
Bảng SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert). VID_SUA = việc nhỏ đợt sau, đè theo nhãn.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p5_ch6_9c import KHOI, OPTIONS  # noqa: E402
from viec_dung_p5_ch6_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

THU_MUC = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai"
CAM = [r"[Kk]huôn", r"Câu III", r"Bài III", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay",
       r"buổi này", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow",
       r"⇔", r"\\Rightarrow", r"⇒", r"iff\b", r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'", r"dạng đề", r"TODO",
       r"[Cc]hỉ đề", r"BÀI ĐÍCH", r"\d–\d ô", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ",
       r"ĐỌC ẢNH", r"MỘT bước", r"TMĐK", r"\(TM\)", r"\(L\)", r"\]\]\]", r"\[\[fill:\$", r"ĐKXĐ",
       r"[Đđ]iều kiện xác định", r"chứa ẩn ở mẫu", r"KHÔNG ghi"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá)
    "Bài 2.": ["x_2=\\dfrac32", "41", "\\sqrt{41}"], "Bài 1.": ["Chọn C"], "Bài 3.": ["Chọn B"],
    "Ví dụ 1.": ["13", "\\dfrac53", "\\dfrac13", "\\dfrac19"],
    "Bài 4.": ["4m^2+4m+20", "(2m+1)^2+19"], "Bài 5.": ["8m-4", "m>\\dfrac12", "A=4"],
    "Ví dụ 2.": ["x^2+20x-8000", "32400", "80"], "Bài 6.": ["Chọn B"],
    "Ví dụ 3.": ["\\dfrac12", "x^2-31x-180", "1681", "36"], "Bài 7.": ["Chọn A"], "Bài 8.": ["Chọn B"],
    "Ví dụ 4.": ["100(1+x)", "100(1+x)^2", "1{,}09", "9\\%"],
    "Bài 9.": ["50(1+x)", "50x^2+125x-13", "18225", "10\\%"],
    "Ví dụ 5.": ["28", "1+\\sqrt7", "4m+16", "m^2-m-30", "m=6"],
    "Bài 10.": ["-3", "-(m+1)", "m=5"],
    "Bài 11.": ["x^2+6x+9", "(x+3)^2", "x=-3"], "Bài 12.": ["2x^2-2x+2-a=0", "\\dfrac{1-\\sqrt7}{2}"],
    "Bài 13.": ["3+\\sqrt6", "30", "\\dfrac{10}3"], "Bài 14.": ["22", "-\\dfrac{11}2"],
    "Bài 15.": ["\\dfrac13", "\\dfrac{40}{x+5}", "x^2+35x-450", "3025", "10"],
    "Bài 16.": ["x-3", "x^2-3x-180", "729", "15"], "Bài 17.": ["\\dfrac14", "x^2+50x-3600", "16900", "40"],
    "Bài 18.": ["\\dfrac65", "5x^2-7x-6", "169"], "Bài 19.": ["-4", "m^2+8", "m=1"],
    "Bài 20.": ["17-4m", "\\dfrac{17}4", "m=4"],
}

# Sơ đồ tư duy: chỉ kiến thức lõi của chương (Thầy 16/11: không nhồi mọi dạng bài).
MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt chương VI",
    "root": r"Phương trình bậc hai[[br]]$ax^2+bx+c=0$ ($a\ne0$)",
    "branches": [
        {"label": "Công thức nghiệm", "children": [
            {"label": r"$\Delta=[[blank:1.8cm]]$"},
            {"label": r"$\Delta>0$: hai nghiệm phân biệt"},
            {"label": r"$\Delta<0$: [[blank:1.8cm]]"},
            {"label": r"$ac<0$: luôn có [[blank:2.4cm]]"}]},
        {"label": "Định lí Viète", "children": [
            {"label": r"$x_1+x_2=[[blank:1.2cm]]$, \ $x_1x_2=[[blank:1.2cm]]$"},
            {"label": r"$x_1^2+x_2^2=(x_1+x_2)^2-[[blank:1.4cm]]$"}]},
        {"label": "Lập phương trình", "children": [
            {"label": r"Chọn ẩn, đặt điều kiện"},
            {"label": r"Đối chiếu nghiệm với [[blank:1.8cm]] rồi trả lời"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $b^2-4ac$ · vô nghiệm · hai nghiệm phân biệt · $-\dfrac{b}{a}$, $\dfrac{c}{a}$ · "
             r"$2x_1x_2$ · điều kiện của ẩn.")

# Kiến thức cần nhớ: (file seed, chữ đầu tiêu đề) — chép khối đã qua cổng, đánh số lại.
CONCEPT_NGUON = [
    ("phieu-1-phuong-trinh-bac-hai-bien-luan-so-nghiem.json", "3. Công thức nghiệm", "Công thức nghiệm của phương trình bậc hai"),
    ("phieu-1-phuong-trinh-bac-hai-bien-luan-so-nghiem.json", "4. Nhận xét khi", "Nhận xét khi $a$ và $c$ trái dấu"),
    ("phieu-2-dinh-li-viete-bieu-thuc-doi-xung.json", "1. Định lí Viète", "Định lí Viète"),
    ("phieu-2-dinh-li-viete-bieu-thuc-doi-xung.json", "2. Biết một nghiệm", "Biết một nghiệm, tìm nghiệm còn lại"),
    ("phieu-2-dinh-li-viete-bieu-thuc-doi-xung.json", "4. Biểu thức đối xứng", "Biểu thức đối xứng của hai nghiệm viết theo tổng và tích"),
    ("phieu-4-giai-bai-toan-bang-cach-lap-phuong-trinh.json", "Các bước giải bài toán", "Các bước giải bài toán bằng cách lập phương trình"),
]

VID_SUA = ()          # việc sửa nhỏ đợt sau (đè theo nhãn)
SUA = {  # nhãn → [(cũ, mới)] trong solution
    "Bài 11.": [(r"a) $2x(x+3)-x^2+9=0$", r"a) Ta có $2x(x+3)-x^2+9=0$")],
}
SUA_VD = {  # nhãn → [(cũ, mới)] trong text ví dụ
    # soát 17/11: hai ô dính liền "[[fill:13]][[fill:>]]0" ⇒ tách dòng so sánh với 0
    "Ví dụ 1.": [(r"=[[fill:13]][[fill:>]]0$.[[br]]\hspace*{1.4em}Phương trình luôn có hai nghiệm phân biệt $x_1$, $x_2$.",
                  r"=[[fill:13]]$.[[br]]\hspace*{1.4em}Vì $\Delta[[fill:>]]0$ nên phương trình luôn có hai nghiệm phân biệt $x_1$, $x_2$.")],
    # soi PDF 17/11: "nên … , nên x =" hai chữ "nên" liền nhau ⇒ tách dòng
    "Ví dụ 4.": [(r"$1+x=[[fill:1{,}09]]$, nên $x=[[fill:0{,}09]]$.",
                  r"$1+x=[[fill:1{,}09]]$.[[br]]\hspace*{1.4em}Khi đó $x=[[fill:0{,}09]]$.")],
}
TN_SUA = []           # [(khoá teacher_notes, cũ, mới)]
LT_SUA = []           # [(cũ, mới)] trong opener/review


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right|\\ ", "", s or "")
    s = s.replace(r"\frac", r"\dfrac")
    s = re.sub(r"\\dfrac\{(\d+)\}\{(\d+)\}", lambda mm: r"\dfrac" + (mm[1] if len(mm[1]) == 1 else "{" + mm[1] + "}")
               + (mm[2] if len(mm[2]) == 1 else "{" + mm[2] + "}"), s)
    s = s.replace("[[fill:", "").replace("]]", "")
    return re.sub(r"\\sqrt\{(\d)\}", r"\\sqrt\1", s)


def thay(nhan, s, bang):
    for cu, moi in bang.get(nhan, []):
        assert s.count(cu) == 1, (nhan, cu[:70])
        s = s.replace(cu, moi)
    return s


def concept():
    out = []
    for i, (f, dau, ten) in enumerate(CONCEPT_NGUON, 1):
        s = json.loads((REPO / THU_MUC / f).read_text())
        bl = next(st for st in s["stages"] if st["kind"] == "concept")["blocks"]
        k = next(j for j, b in enumerate(bl) if b.get("variant") == "heading" and b["text"].startswith(dau))
        out += [{"type": "para", "variant": "heading", "text": f"{i}. {ten}"}, dict(bl[k + 1])]
    return out


def dung(sua):
    """Khối theo KHOI: đề Claude + lời giải Gemini."""
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
        if ht == "vi_du":
            txt = thay(nhan, g["statement"], SUA_VD)
            dau = txt.split("{\\sffamily")[0]
            if chuan(de) not in chuan(dau):
                loi.append(f"{nhan}: đề ví dụ lệch sơ đồ:\n   có  {dau[:300]}")
            out[chang].append({"type": "noted", "variant": "example", "text": txt})
        else:
            b = {"type": "problem", "label": nhan, "level": level, "tier": tier, "dang_id": dang,
                 "statement": de, "solution": thay(nhan, g["solution"], SUA), "hints": []}
            if nhan in OPTIONS:
                b["options"] = OPTIONS[nhan]
            if g["statement"].strip() != de.strip():
                loi.append(f"{nhan}: (nhắc) Gemini chép đề khác sơ đồ — đã lấy đề sơ đồ")
            out[chang].append(b)
    return out, loi


def soat(stages, lt):
    loi = []
    phan_gemini = [("lt", json.dumps({k: v for k, v in lt.items() if k != "ghi_chu"}, ensure_ascii=False))]
    for s in stages:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                nh, txt = b["label"], b["solution"]
                phan_gemini.append((nh, txt))
                if not txt.strip():
                    loi.append(f"{nh}: thiếu lời giải")
                if not b.get("options") and nh not in ("Bài 2.",) and not re.search(r"Vậy", txt):   # Bài 2 toàn câu NB một dòng
                    loi.append(f"{nh}: lời giải không có dòng Vậy")
            elif b.get("variant") == "example":
                nh = re.match(r"\\textbf\{([^}]*)\}", b["text"]).group(1)
                txt = b["text"]
                phan_gemini.append((nh, txt.split("{\\sffamily", 1)[-1]))
                nf = txt.count("[[fill:")
                if nf < 6:
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
        for mm in re.finditer(r"(?<!\\);", txt):
            loi.append(f"[{ten}] dấu ';': …{txt[max(0, mm.start() - 40): mm.end() + 20]}…")
    return loi


def khung():
    """Seed mới theo khung Phiếu 4 (cùng cờ luat_16_11, btvn_phieu_rieng)."""
    p4 = json.loads((REPO / THU_MUC / "phieu-4-giai-bai-toan-bang-cach-lap-phuong-trinh.json").read_text())
    f = {k: v for k, v in p4.items() if k != "stages"}
    f["stages"] = [{"kind": st["kind"], "number": st["number"], "title": st["title"], "blocks": []}
                   for st in p4["stages"]]
    return f


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    sua = {x["label"]: x for x in lop["sua"] + btvn["sua"]}
    sua["Bài 1."], sua["Bài 2."] = sua["Bài 2."], sua["Bài 1."]   # 17/11 đổi chỗ 6.42 ↔ Cầu Diễn (dan_dat_gate)
    for vid in VID_SUA:
        if (REPO / "storage/gemini/xong" / f"{vid}.json").exists():
            sua.update({x["label"]: x for x in lay(vid)["sua"]})
    for x in sua.values():
        for k in ("statement", "solution"):
            x[k] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", x[k].replace("–", "--"))
    khoi, loi = dung(sua)
    for k in khoi.values():                    # đề sơ đồ cũng đổi số bài tập SGK 6.42 → 6{.}42
        for b in k:
            if b.get("type") == "problem":
                b["statement"] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", b["statement"])

    p = REPO / SEED
    f = json.loads(p.read_text()) if p.exists() else khung()
    f["slug"] = Path(SEED).stem
    f["title"] = "Luyện tập chung và bài tập cuối chương VI"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU 5"
    f["kiem_tra_phut"] = 90
    tn = lt["teacher_notes"]
    for k, cu, moi in TN_SUA:
        assert tn[k].count(cu) == 1, (k, cu)
        tn[k] = tn[k].replace(cu, moi)
    for k in ("opener_text", "review_note"):
        for cu, moi in LT_SUA:
            lt[k] = lt[k].replace(cu, moi)
    st = {s["kind"]: s for s in f["stages"]}
    rv = st["review"]
    rv.update(title="Khám phá", solution="", teacher_note=tn["review"])
    rv["blocks"] = [{"type": "opener", "text": lt["opener_text"]},
                    {"type": "noted", "variant": "note",
                     "text": r"\textbf{Nhắc lại kiến thức đã học.}[[br]]" + lt["review_note"]}]
    cp = st["concept"]
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"], blocks=concept())
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 10 — đề kiểm tra học kì II Phòng GD\&ĐT Hà Đông "
            r"2024--2025: chứng tỏ phương trình luôn có hai nghiệm phân biệt, rồi tìm $m$ theo hệ thức giữa hai "
            r"nghiệm.[[br]]Mạch 1 ôn công thức nghiệm và định lí Viète, Mạch 2 ôn giải bài toán bằng cách lập phương "
            r"trình, Mạch 3 là tìm $m$ theo hệ thức."}
    for k, ten in (("practice1", "Luyện tập 1 — Phương trình bậc hai, Viète"),
                   ("practice2", r"Luyện tập 2 — Lập phương trình, tìm $m$")):
        st[k].update(title=ten, teacher_note=tn[k], blocks=([dich] if k == "practice1" else []) + khoi[k])
        st[k].pop("solution", None)
    rf = st["reflection"]
    rf["title"] = "Tổng kết"
    rf["blocks"] = [MINDMAP, {"type": "para", "text": r"\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."}] \
        + khoi["reflection"]
    rf["solution"] = GIAI_BTVN
    rf["teacher_note"] = tn.get("reflection", "")

    loi += soat([st[k] for k in ("practice1", "practice2", "reflection")], lt)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
