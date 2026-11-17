#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p3-ch6-9c-{lt,lop,btvn} vào seed Phiếu 3 ch.VI 9C bản 2 + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p3_ch6_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p3_ch6_9c.py --ghi    # ghi seed

ĐỀ bài lấy từ sơ đồ của Claude (so_do_p3_ch6_9c.KHOI — nguồn sự thật), Gemini chỉ góp LỜI GIẢI, text ví dụ, lý thuyết.
Soát: đủ nhãn, từ cấm, ";", ⇔, Δ′; ví dụ đủ ô [[fill:]] và đề ví dụ khớp sơ đồ; đáp số then chốt có mặt.
Khuôn từ lap_p2_ch6_9c.py. Bảng SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p3_ch6_9c import KHOI, OPTIONS  # noqa: E402
from viec_dung_p3_ch6_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"iff\b", r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'", r"thu gọn", r"dạng đề", r"TODO", r"Viete\b",
       r"[Cc]hỉ đề", r"BÀI ĐÍCH", r"\d–\d ô", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy", r"GHI CHÚ"]

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá)
    "Ví dụ 1.": ["m=0", "-35"], "Ví dụ 2.": ["4(m-2)^2", r"\dfrac53"], "Bài 4.": ["Chọn A", "3-x"],
    "Bài 1.": ["9-4m", "m=-4"], "Bài 2.": ["13-4m", "x_2=2", "m=3"], "Bài 3.": ["(m-2)^2", r"-\dfrac53", r"-\dfrac72"],
    "Ví dụ 3.": [r"\dfrac54", r"\dfrac14"], "Bài 5.": ["3x_1+5", "14"], "Bài 6.": ["10x_1+3", "A=3"],
    "Ví dụ 4.": ["(x_1-1)^2", "-2029"], "Bài 7.": ["-16x_1+5", "13"], "Bài 8.": ["74", r"\dfrac4{37}"],
    "Ví dụ 5.": [r"-\dfrac56"], "Bài 9.": ["2mx_1-m+1", "m=2", "m=-1"], "Bài 10.": ["76", "m=1"],
    "Bài 11.": ["x_2^2", "18"], "Bài 12.": [r"\dfrac{1+\sqrt5}{2}", "4"], "Bài 13.": [r"\dfrac{3+\sqrt{13}}{2}", "13"],
    "Bài 14.": ["-4", "m=20"], "Bài 15.": ["k=5", "-485"], "Bài 16.": ["2x_1+1", "m=4"],
    "Bài 17.": ["-3x_2", r"\dfrac12"], "Bài 18.": ["40-4m", "m=3", "m=-2"], "Bài 19.": ["4m^2+1", "-3"],
    "Bài 20.": ["(2m+1)^2", "m=1", r"-\dfrac78"], "Bài 21.": ["m<-3"], "Bài 22.": ["m=4", r"\dfrac92"],
    "Bài 23.": ["m>-2"], "Bài 24.": ["m=-1"],
}

# Sơ đồ tư duy: chỉ kiến thức lõi của buổi (Thầy 16/11).
MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"Biểu thức không đối xứng[[br]]của hai nghiệm $x_1$, $x_2$",
    "branches": [
        {"label": "Hệ thức bậc nhất", "children": [
            {"label": r"Ghép với $x_1+x_2=[[blank:1.4cm]]$ thành hệ"},
            {"label": r"Thay $x_1$, $x_2$ vào $x_1x_2=[[blank:1.2cm]]$"}]},
        {"label": r"$x_1$ là nghiệm", "children": [
            {"label": r"$ax_1^2=[[blank:2.2cm]]$"}]},
        {"label": "Căn, giá trị tuyệt đối", "children": [
            {"label": r"$\sqrt{A^2}=[[blank:1cm]]$"},
            {"label": r"$a\cdot c<0$: hai nghiệm [[blank:1.6cm]]"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $x_1+x_2=-\dfrac ba$, $x_1x_2=\dfrac ca$ · $ax_1^2=-bx_1-c$ · "
             r"$\sqrt{A^2}=|A|$ · $a\cdot c<0$ thì hai nghiệm trái dấu.")

# Claude soát 17/11: lặp "nên …, nên …" ⇒ "hay" (như phần BTVN); Ví dụ 4 ô "4[(m+2)^2+1]]]" vỡ cú pháp [[fill:]].
VID_SUA = ("sua-p3-ch6-9c-b15", "sua2-p3-ch6-9c")   # viec_sua_p3_ch6_9c.py
# 17/11 Thầy "ôn giải hpt làm chi": bỏ Bài 1 cũ (giải hệ) ⇒ bản dựng đầu đổi nhãn Bài 2→1, Bài 4→3 (Bài 3 cũ = Bài 2 mới,
# lời giải viết lại ở sua2). Bài 4 mới (√(A²)=|A|) và Bài 7 (bớt câu dẫn) cũng lấy từ sua2.
DOI_NHAN_LOP = {"Bài 1.": None, "Bài 2.": "Bài 1.", "Bài 3.": None, "Bài 4.": "Bài 3."}   # 17/11: Bài 15 thay câu (viec_sua_p3_ch6_9c.py)
SUA = {  # nhãn bài → [(cũ, mới)] trong solution
    "Bài 10.": [(r"ta được $70=-6+76m$, nên $76m=76$, nên $m=1$.", r"ta được $70=-6+76m$, nên $m=1$.")],
    "Bài 15.": [(r"Kiểm tra lại với $k=5$: phương trình có $\Delta=", r"Với $k=5$, phương trình là $x^2+5x-24=0$ có $\Delta=")],
}
SUA_VD = {  # nhãn ví dụ → [(cũ, mới)] trong text
    "Ví dụ 3.": [(r"nên $4x_1^2-2x_1-1=0$, nên $4x_1^2-2x_1=1$, tức là ", r"nên $4x_1^2-2x_1-1=0$, hay $4x_1^2-2x_1=1$.[[br]]\hspace*{1.4em}Chia hai vế cho $4$, ta được ")],
    "Ví dụ 5.": [(r"=[[fill:4[(m+2)^2+1]]]>0", r"=4\big[(m+2)^2+[[fill:1]]\big]>0")],
}
# Bài làm thêm mức TH (gradient_gate/vi_du_gate đòi gợi ý); Bài 24 là VD ⇒ chỉ đề.
HINTS_LAM_THEM = {
    "Bài 22.": [r"Điểm thuộc đồ thị thì tọa độ của điểm thỏa mãn công thức của hàm số. Hoành độ giao điểm là nghiệm "
                r"của phương trình hoành độ giao điểm."],
    "Bài 23.": [r"Hai đồ thị cắt nhau tại hai điểm phân biệt khi phương trình hoành độ giao điểm có hai nghiệm phân biệt."],
}
TN_SUA = [  # 17/11: bỏ bài giải hệ, thêm Bài 4 ôn √(A²)=|A|
    ("practice1", "Bài 1 gọi một học sinh lên bảng giải hệ. ", ""),
    ("practice1", "Bài 2--4 phần", "Bài 1--3 phần"),
    ("practice2", "mỗi mạch giáo viên làm ví dụ", "Bài 4 hỏi nhanh cả lớp (ôn $\\sqrt{A^2}=|A|$, dùng lại ở Mạch 4). "
     "Từ Mạch 3, mỗi mạch giáo viên làm ví dụ"),
]
NEN_NEN = (r"=0$, nên $", r"=0$, hay $")   # "Vì x1 là nghiệm nên …=0, nên x1²=…" ⇒ "…=0, hay x1²=…"
LT_SUA = []   # [(cũ, mới)] trong concept/review/opener


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right", "", s or "")
    s = s.replace(r"\frac", r"\dfrac")
    s = re.sub(r"\\dfrac\{(\d+)\}\{(\d+)\}", lambda mm: r"\dfrac" + (mm[1] if len(mm[1]) == 1 else "{" + mm[1] + "}")
               + (mm[2] if len(mm[2]) == 1 else "{" + mm[2] + "}"), s)
    s = re.sub(r"\\dfrac\{([^{}]+)\}(\d)\b", r"\\dfrac{\1}\2", s)
    s = s.replace("[[fill:", "").replace("]]", "")
    return re.sub(r"\\sqrt\{(\d)\}", r"\\sqrt\1", s)


def thay(nhan, s, bang):
    for cu, moi in bang.get(nhan, []):
        assert s.count(cu) == 1, (nhan, cu[:70])
        s = s.replace(cu, moi)
    return s


def tach_vd1(sua):
    """17/11 soi PDF: Gemini trả Ví dụ 1 ba ý ⇒ tách ý c thành Ví dụ 2, các ví dụ sau +1."""
    if "Ví dụ 5." in sua or "Ví dụ 4." not in sua:
        return
    for n in (4, 3, 2):
        g = sua.pop(f"Ví dụ {n}.")
        g["statement"] = g["statement"].replace(rf"\textbf{{Ví dụ {n}.}}", rf"\textbf{{Ví dụ {n + 1}.}}", 1)
        sua[f"Ví dụ {n + 1}."] = g
    txt = sua["Ví dụ 1."]["statement"]
    assert txt.count("[[br]]c) ") == 2, txt.count("[[br]]c) ")
    de, giai = txt.split("{\\sffamily", 1)
    de_ab, de_c = de.split("[[br]]c) ")
    giai_ab, giai_c = giai.split("[[br]]c) ")
    dau_giai = "{\\sffamily" + giai.split("[[br]]", 1)[0] + "[[br]]"
    sua["Ví dụ 1."]["statement"] = de_ab + "[[br]]{\\sffamily" + giai_ab
    sua["Ví dụ 2."] = {"label": "Ví dụ 2.", "solution": "",
                       "statement": r"\textbf{Ví dụ 2.} " + de_c.rstrip().removesuffix("[[br]]") + "[[br]]" + dau_giai
                       + r"\hspace*{1.4em}" + giai_c}


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
                 "statement": de, "solution": thay(nhan, g["solution"], SUA).replace(*NEN_NEN),
                 "hints": HINTS_LAM_THEM.get(nhan, [])}
            if nhan in OPTIONS:
                b["options"] = OPTIONS[nhan]
            if g["statement"].strip() != de.strip():
                loi.append(f"{nhan}: (nhắc) Gemini chép đề khác sơ đồ — đã lấy đề sơ đồ")
            out[chang].append(b)
    return out, loi


def soat(stages, lt):
    loi = []
    for s in stages:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                nh, txt = b["label"], b["solution"]
                if not txt.strip():
                    loi.append(f"{nh}: thiếu lời giải")
                if b["level"] == 3 and b["tier"] != "extend":
                    y_vd = b["statement"].split("[VD]")[-1]
                    if re.search(r"[Gg]ợi ý|[Hh]ướng dẫn|Bước", y_vd):
                        loi.append(f"{nh}: ý [VD] có gợi ý")
                if not b.get("options") and not re.search(r"Vậy", txt):
                    loi.append(f"{nh}: lời giải không có dòng Vậy")
            elif b.get("variant") == "example":
                nh = re.match(r"\\textbf\{([^}]*)\}", b["text"]).group(1)
                txt = b["text"]
                nf = txt.count("[[fill:")
                if nf < 6:
                    loi.append(f"{nh}: ví dụ ít ô fill ({nf})")
                if re.search(r"\[(NB|TH|VD)\]", txt):
                    loi.append(f"{nh}: ví dụ có thẻ mức")
            else:
                continue
            for d in DAP.get(nh, []):
                if chuan(d) not in chuan(txt):
                    loi.append(f"{nh}: không thấy đáp số {d}")
    tat_ca = [("lt", json.dumps({k: v for k, v in lt.items() if k != "ghi_chu"}, ensure_ascii=False))] + \
             [(s["kind"], json.dumps(s, ensure_ascii=False)) for s in stages]
    for ten, txt in tat_ca:
        for pat in CAM:
            for mm in re.finditer(pat, txt):
                loi.append(f"[{ten}] /{pat}/: …{txt[max(0, mm.start() - 50): mm.end() + 30]}…")
        for mm in re.finditer(r"(?<![\\(\d]);(?!\\,)", txt):
            ctx = txt[max(0, mm.start() - 40): mm.end() + 20]
            if not re.search(r"\(\s*-?[\\\w{}]+\s*$", txt[max(0, mm.start() - 15): mm.start()]):   # tọa độ (a; b)
                loi.append(f"[{ten}] dấu ';': …{ctx}…")
    return loi


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    sua = {}
    for x in lop["sua"]:
        nh = DOI_NHAN_LOP.get(x["label"], x["label"])
        if nh:
            sua[nh] = dict(x, label=nh)
    sua.update({x["label"]: x for x in btvn["sua"]})
    sua.pop("Bài 7.", None)                   # bản cũ có câu dẫn c) đã bỏ ⇒ bắt buộc lấy từ sua2
    for vid in VID_SUA:                       # việc nhỏ đợt sau đè theo nhãn
        if (REPO / "storage/gemini/xong" / f"{vid}.json").exists():
            sua.update({x["label"]: x for x in lay(vid)["sua"]})
    tach_vd1(sua)
    for x in sua.values():
        for k in ("statement", "solution"):
            x[k] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", x[k].replace("–", "--"))
    khoi, loi = dung(sua)

    p = REPO / SEED
    f = json.loads(p.read_text())
    f["title"] = "Bài 20 (tiếp). Định lí Viète — biểu thức không đối xứng của hai nghiệm"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU 3"
    tn = lt["teacher_notes"]
    for k, cu, moi in TN_SUA:
        assert tn[k].count(cu) == 1, (k, cu)
        tn[k] = tn[k].replace(cu, moi)
    st = {s["kind"]: s for s in f["stages"]}
    for k in ("opener_text", "review_note"):
        for cu, moi in LT_SUA:
            lt[k] = lt[k].replace(cu, moi)
    for b in lt["concept_blocks"]:
        for cu, moi in LT_SUA:
            b["text"] = b["text"].replace(cu, moi)

    rv = st["review"]
    rv.update(title="Khám phá", solution="", teacher_note=tn["review"])
    rv["blocks"] = [{"type": "opener", "text": lt["opener_text"]},
                    {"type": "para", "text": r"\textbf{Nhắc lại kiến thức đã học.}"},
                    {"type": "noted", "variant": "note", "text": lt["review_note"]}]
    cp = st["concept"]
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"], blocks=lt["concept_blocks"])
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 11 — đề tuyển sinh lớp 10 THPT Hà Nội "
            r"2026--2027: tính giá trị một biểu thức không đối xứng của hai nghiệm.[[br]]Mạch 1 luyện hệ thức bậc nhất "
            r"giữa hai nghiệm, Mạch 2 ôn $\sqrt{A^2}=|A|$, Mạch 3–5 luyện cách dùng $x_1$ là nghiệm để hạ bậc, Mạch 6 là hai đề "
            r"tuyển sinh."}
    for k, ten in (("practice1", "Luyện tập 1 — Hệ thức bậc nhất giữa hai nghiệm"),
                   ("practice2", "Luyện tập 2 — Hạ bậc, căn và đề tuyển sinh")):
        st[k].update(title=ten, teacher_note=tn[k], blocks=([dich] if k == "practice1" else []) + khoi[k])
        st[k].pop("solution", None)
    rf = st["reflection"]
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
