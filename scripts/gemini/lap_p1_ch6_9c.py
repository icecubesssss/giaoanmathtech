#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p1-ch6-9c-{lt,lop,btvn} vào seed Phiếu 1 ch.VI 9C bản 2 + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p1_ch6_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p1_ch6_9c.py --ghi    # ghi seed

Soát: thứ tự + nhãn + dang_id + level + tier + thẻ từng bài khớp sơ đồ (so_do_p1_ch6_9c.KHOI);
từ cấm, ";", ⇔, Δ′; ví dụ đủ ô [[fill:]]; bài tập không ô điền; đáp số then chốt có mặt trong lời giải.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch6_9c import KHOI  # noqa: E402
from viec_dung_p1_ch6_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"iff\b", r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'", r"thu gọn", r"dạng đề", r"TODO"]

# đáp số then chốt phải có trong lời giải (so sau khi bỏ khoảng trắng)
DAP = {
    "Bài 4.": ["2x^2+3x-1=0", "3x^2+4x=0"], "Bài 5.": ["213", "-8"],
    "Bài 7.": [r"\dfrac12", r"-3+\sqrt5", r"-3-\sqrt5"], "Bài 8.": [r"\dfrac72", r"-\dfrac83"],
    "Bài 9.": ["-44"], "Bài 10.": ["92", r"3+\sqrt{23}", r"3-\sqrt{23}"], "Bài 11.": [r"-\dfrac{\sqrt{10}}{5}"],
    "Bài 12.": ["40", r"\sqrt{10}", r"\sqrt3-1"], "Bài 13.": ["x^2-8x+16=0"], "Bài 14.": ["-4m+5", r"m<\dfrac54"],
    "Bài 15.": ["-4m+9", r"m>\dfrac94"], "Bài 16.": ["(m+1)^2", "m=-1"], "Bài 17.": ["m=-2", "-2026"],
    "Bài 19.": ["x^2+4x-5=0", "=-5", "4(m-2)^2"], "Bài 22.": [r"-\dfrac{11}{5}", r"-\dfrac16"],
    "Bài 23.": [r"-\dfrac95", r"-\dfrac23", r"\dfrac54", r"\sqrt2"], "Bài 24.": ["25", r"-\dfrac13"],
    "Bài 25.": ["61", r"\sqrt{61}"], "Bài 26.": ["x^2+3x+2=0"], "Bài 27.": ["x^2-3x+2=0"],
    "Bài 28.": ["3x^2+22x-16=0", "676", r"\dfrac23", "-8"], "Bài 29.": ["-12"], "Bài 30.": ["m^2-m-6", "m=3", "m=-2"],
    "Bài 31.": ["24m+24", "m>-1"], "Bài 33.": ["(m-2)^2"],
    "Ví dụ 3.": ["61", "-31"], "Ví dụ 5.": ["24m+56", r"\dfrac73"], "Ví dụ 6.": ["4m^2+9"],
}

# Thầy 16/11 khuya: "sơ đồ tư duy chỉ cần các TH của Delta thôi, kèm nghiệm của các TH đó là đủ".
MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"$ax^2+bx+c=0$ ($a\ne 0$)[[br]]$\Delta=b^2-4ac$",
    "branches": [
        {"label": r"$\Delta>0$", "children": [{"label": r"Phương trình có [[blank:3cm]]"},
                                              {"label": r"$x_1=[[blank:2.2cm]]$, $x_2=[[blank:2.2cm]]$"}]},
        {"label": r"$\Delta=0$", "children": [{"label": r"Phương trình có [[blank:3cm]]"},
                                              {"label": r"$x_1=x_2=[[blank:2cm]]$"}]},
        {"label": r"$\Delta<0$", "children": [{"label": r"Phương trình [[blank:3cm]]"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $\Delta>0$: hai nghiệm phân biệt, $x_1=\dfrac{-b+\sqrt{\Delta}}{2a}$, "
             r"$x_2=\dfrac{-b-\sqrt{\Delta}}{2a}$ · $\Delta=0$: nghiệm kép, $x_1=x_2=-\dfrac{b}{2a}$ · "
             r"$\Delta<0$: vô nghiệm.")


# Claude soát đầu ra 16/11: ý [TH] phải đi đúng đường câu dẫn [NB] (dấu của ac), không đổi sang Δ.
SUA = {
    "Bài 18.": (r"b) Ta có $\Delta=(-2m)^2-4\cdot 1\cdot(-1)=4m^2+4$.[[br]]\hspace*{1.4em}Vì $4m^2\ge 0$ với mọi $m$ nên $\Delta=4m^2+4>0$ với mọi $m$.",
                r"b) Vì $a\cdot c=-1<0$ nên $a$ và $c$ trái dấu với mọi $m$."),
    "Bài 32.": (r"b) Ta có $\Delta=(-2m)^2-4\cdot 1\cdot(-3)=4m^2+12$.[[br]]\hspace*{1.4em}Vì $4m^2\ge 0$ với mọi $m$ nên $\Delta=4m^2+12>0$ với mọi $m$.",
                r"b) Vì $a\cdot c=-3<0$ nên $a$ và $c$ trái dấu với mọi $m$."),
}


def ap_sua(stages):
    for s in stages:
        for b in s["blocks"]:
            for k in ("text", "statement", "solution"):
                if isinstance(b.get(k), str):
                    b[k] = b[k].replace("–", "--").replace("SGK 6.41", "SGK 6{.}41")
            if b.get("label") in SUA:
                cu, moi = SUA[b["label"]]
                assert b["solution"].count(cu) == 1, b["label"]
                b["solution"] = b["solution"].replace(cu, moi)


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right", "", s or "")
    s = s.replace(r"\frac", r"\dfrac")
    s = re.sub(r"\\dfrac\{(\d)\}\{(\d)\}", r"\\dfrac\1\2", s)
    return re.sub(r"\\sqrt\{(\d)\}", r"\\sqrt\1", s)


def nhan_cua(b):
    if b.get("type") == "problem":
        return b.get("label")
    m = re.match(r"\\textbf\{([^}]*)\}", b.get("text", ""))
    return m.group(1) if m else ("[tiêu đề] " + b.get("text", "")[:40] if b.get("variant") == "heading" else None)


def soat(stages, lt):
    loi = []
    mong = [k for k in KHOI if len(k) > 3]
    co = []
    for s in stages:
        for b in s["blocks"]:
            nh = nhan_cua(b)
            if nh and not nh.startswith("[tiêu đề]") and nh not in ("Đích của buổi học:", "Bài tập về nhà"):
                co.append((nh, s["kind"], b))
    if [c[0] for c in co] != [k[0] for k in mong]:
        loi.append(f"thứ tự/nhãn lệch sơ đồ:\n   có  {[c[0] for c in co]}\n   cần {[k[0] for k in mong]}")
    for (nh, kind, b), k in zip(co, mong):
        _, chang, tier, dang, level, *_ = k
        ht, noi = k[7], k[8]
        if kind != chang:
            loi.append(f"{nh}: nằm ở {kind}, sơ đồ {chang}")
        if ht == "vi_du":
            if b.get("variant") != "example":
                loi.append(f"{nh}: ví dụ không phải noted/example")
            if b.get("text", "").count("[[fill:") < 3:
                loi.append(f"{nh}: ví dụ ít ô fill ({b.get('text', '').count('[[fill:')})")
            if "[NB]" in b.get("text", "") or "[TH]" in b.get("text", ""):
                loi.append(f"{nh}: ví dụ có thẻ mức")
        else:
            for f, v in (("tier", tier), ("dang_id", dang), ("level", level)):
                if b.get(f) != v:
                    loi.append(f"{nh}: {f}={b.get(f)!r}, sơ đồ {v!r}")
            the_co = re.findall(r"\[(NB|TH|VD)\]", b.get("statement", ""))
            the_can = re.findall(r"\[(NB|TH|VD)\]", noi)
            if the_co != the_can:
                loi.append(f"{nh}: thẻ {the_co}, sơ đồ {the_can}")
            if re.search(r"\[\[(fill|blank|mblank)|\\ldots|\\dots|hoàn thành bài giải", b.get("statement", "")):
                loi.append(f"{nh}: bài tập có ô điền/chỗ chấm (luật 16/11: chỉ Ví dụ được điền)")
            if ht == "trac_nghiem" and len(b.get("options") or []) != 4:
                loi.append(f"{nh}: trắc nghiệm cần 4 options")
            if ht == "dung_sai" and not b.get("dung_sai"):
                loi.append(f"{nh}: Đúng/Sai thiếu dung_sai")
            if not (b.get("solution") or "").strip():
                loi.append(f"{nh}: thiếu lời giải")
        txt = chuan(b.get("solution", "") + b.get("text", ""))
        for d in DAP.get(nh, []):
            if chuan(d) not in txt:
                loi.append(f"{nh}: không thấy đáp số {d}")
    # chữ cấm, ;, trên mọi chuỗi
    tat_ca = [("lt", json.dumps({k: v for k, v in lt.items() if k != "ghi_chu"}, ensure_ascii=False))] + \
             [(s["kind"], json.dumps(s, ensure_ascii=False)) for s in stages]
    for ten, txt in tat_ca:
        for pat in CAM:
            for mm in re.finditer(pat, txt):
                loi.append(f"[{ten}] /{pat}/: …{txt[max(0, mm.start() - 50): mm.end() + 30]}…")
        for mm in re.finditer(r"(?<!\\);", txt):
            loi.append(f"[{ten}] dấu ';': …{txt[max(0, mm.start() - 40): mm.end() + 20]}…")
    return loi


# Đợt 2 (sau validate lượt 1): Mạch 1 trắc nghiệm/Đúng–Sai đứng trước trả lời ngắn ⇒ nhãn mới ← nhãn lượt 1.
NHAN_CU = {"Bài 1.": "Bài 2.", "Bài 2.": "Bài 4.", "Bài 3.": "Bài 5.", "Bài 4.": "Bài 1.", "Bài 5.": "Bài 3."}
VID_SUA = "sua-p1-ch6-9c"
VID_SUA2 = "sua2-p1-ch6-9c"


# Claude soát đợt 2: ô điền không được để đáp án in sẵn ở dòng trên (vi_du_gate lộ đáp án).
SUA_VD = {
    "Ví dụ 3.": [
        (r"$\Delta=(-6)^2-4\cdot 1\cdot 9=36-36=0$.[[br]]\hspace*{1.4em}Vì $\Delta=[[fill:0]]$ nên phương trình có nghiệm kép.",
         r"$\Delta=(-6)^2-4\cdot 1\cdot 9=36-36=[[fill:0]]$ nên phương trình có nghiệm kép."),
    ],
    "Ví dụ 6.": [
        (r"\hspace*{1.4em}$m=-2$.[[br]]\hspace*{1.4em}Khi đó phương trình trở thành $x^2-x-6=0$, có $\Delta=(-1)^2-4\cdot 1\cdot(-6)=25>0$.",
         r"\hspace*{1.4em}$m=[[fill:-2]]$.[[br]]\hspace*{1.4em}Khi đó phương trình trở thành $x^2-x-6=0$, có $\Delta=(-1)^2-4\cdot 1\cdot(-6)=25>0$ nên phương trình có hai nghiệm phân biệt[[br]]\hspace*{1.4em}$x_1=\dfrac{1+5}{2}=3$ và $x_2=\dfrac{1-5}{2}=[[fill:-2]]$."),
    ],
    "Ví dụ 7.": [
        (r"Tích hai hệ số đó bằng $1\cdot(-1)=[[fill:-1]]<0$ ([[fill:trái dấu]]) nên phương trình luôn có hai nghiệm phân biệt.",
         r"Tích hai hệ số đó bằng $1\cdot(-1)=[[fill:-1]]<0$, tức là hai hệ số [[fill:trái dấu]]."),
    ],
}


def sua_vd(nhan, text):
    for cu, moi in SUA_VD.get(nhan, []):
        assert text.count(cu) == 1, (nhan, cu[:60])
        text = text.replace(cu, moi)
    return text


def dung_theo_so_do(moi):
    """Xếp khối practice1/2 đúng thứ tự KHOI: bài lấy từ lượt 1 (đổi nhãn Mạch 1), ví dụ + bài sửa lấy từ đợt 2."""
    bai = {b["label"]: b for k in ("practice1", "practice2") for b in moi[k]["blocks"] if b.get("type") == "problem"}
    dich = next(b for b in moi["practice1"]["blocks"] if "Đích của buổi học" in b.get("text", ""))
    sua = {x["label"]: x for x in lay(VID_SUA)["sua"]} if (REPO / "storage/gemini/xong" / f"{VID_SUA}.json").exists() else {}
    # Đợt 3 (Thầy 16/11 "điền khuyết cần nhiều hơn để GV định hướng"): ví dụ đã thêm ô, dựng từ bản sau SUA_VD.
    f2 = REPO / "storage/gemini/xong" / f"{VID_SUA2}.json"
    sua2 = {x["label"]: x for x in lay(VID_SUA2)["sua"]} if f2.exists() else {}
    out = {"practice1": [dich], "practice2": []}
    for k in KHOI:
        chang = k[1]
        if chang not in out:
            continue
        if len(k) == 3:
            out[chang].append({"type": "para", "variant": "heading", "text": k[0].replace("Đích + ", "")})
        elif k[7] == "vi_du":
            text = sua2[k[0]]["statement"] if k[0] in sua2 else sua_vd(k[0], sua[k[0]]["statement"])
            out[chang].append({"type": "noted", "variant": "example", "text": text})
        else:
            b = dict(bai[NHAN_CU.get(k[0], k[0]) if chang == "practice1" else k[0]], label=k[0])
            out[chang].append(b)
    return out


def ap_sua_bai(stages):
    sua = {x["label"]: x for x in lay(VID_SUA)["sua"]} if (REPO / "storage/gemini/xong" / f"{VID_SUA}.json").exists() else {}
    for s in stages:
        for b in s["blocks"]:
            if b.get("type") == "problem" and b.get("label") in sua:
                b["statement"], b["solution"] = sua[b["label"]]["statement"], sua[b["label"]]["solution"]


def gon_mindmap(mm):
    """Thầy 16/11 "gọn được thì gọn": sơ đồ 11 lá đẩy Tổng kết sang trang mới (trắng 8,7cm) ⇒ gộp lá
    nhánh "Công thức nghiệm" (4→2), "Tìm m" (3→2), "Luôn có nghiệm" (2→1), nội dung ô giữ nguyên."""
    for br in mm["branches"]:
        lab = [c["label"] for c in br.get("children", [])]
        if br["label"].startswith("Tìm") and len(lab) == 3:
            br["children"] = [{"label": lab[0] + ", " + lab[1]}, {"label": lab[2]}]
        elif br["label"].startswith("Khuyết") and len(lab) == 2:
            br["children"] = [{"label": lab[0] + ", " + lab[1]}]
        elif br["label"].startswith("Công thức") and len(lab) == 4:
            br["children"] = [{"label": lab[0] + ", " + lab[1]}, {"label": lab[2] + ", " + lab[3]}]
        elif br["label"].startswith("Luôn") and len(lab) == 2:
            br["children"] = [{"label": lab[0] + " hoặc " + lab[1]}]
    return mm


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    p = REPO / SEED
    f = json.loads(p.read_text())
    f["title"] = "Bài 19. Phương trình bậc hai một ẩn — biện luận số nghiệm"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU 1"
    ap_sua_bai(lop["stages"] + btvn["stages"])
    ap_sua(lop["stages"] + btvn["stages"])
    moi = {s["kind"]: s for s in lop["stages"] + btvn["stages"]}
    tn = lt["teacher_notes"]
    st = {s["kind"]: s for s in f["stages"]}

    rv = st["review"]
    rv["title"] = "Khám phá"
    rv["blocks"] = [{"type": "opener", "text": lt["opener_text"]},
                    {"type": "para", "text": r"\textbf{Nhắc lại kiến thức đã học.}"},
                    {"type": "noted", "variant": "note", "text": lt["review_note"]}]
    rv["solution"] = ""
    rv["teacher_note"] = tn["review"]
    cp = st["concept"]
    cp["title"] = "Kiến thức cần nhớ"
    cp["blocks"] = lt["concept_blocks"]
    cp["teacher_note"] = tn["concept"]
    cp.pop("solution", None)
    for k, bl in dung_theo_so_do(moi).items():
        st[k]["title"] = moi[k]["title"]
        st[k]["blocks"] = bl
        st[k]["teacher_note"] = tn[k].replace("Ví dụ 1--3", "Ví dụ 1, 2")
        st[k].pop("solution", None)
    rf = st["reflection"]
    rf["blocks"] = [MINDMAP,
                    {"type": "para", "text": r"\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."}] \
        + moi["reflection"]["blocks"]
    rf["solution"] = GIAI_BTVN
    rf["teacher_note"] = tn.get("reflection", "")

    loi = soat([st[k] for k in ("practice1", "practice2", "reflection")], lt)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
