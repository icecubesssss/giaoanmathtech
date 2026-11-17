#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p2-ch6-9c-{lt,lop,btvn} vào seed Phiếu 2 ch.VI 9C bản 2 + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p2_ch6_9c.py --ghi    # ghi seed

Soát: thứ tự + nhãn + dang_id + level + tier + thẻ từng bài khớp sơ đồ (so_do_p2_ch6_9c.KHOI);
từ cấm, ";", ⇔, Δ′; ví dụ đủ ô [[fill:]]; bài tập không ô điền; ý [VD] không gợi ý; đáp số then chốt có mặt.
Khuôn từ lap_p1_ch6_9c.py.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p2_ch6_9c import KHOI  # noqa: E402
from viec_dung_p2_ch6_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"iff\b", r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'", r"thu gọn", r"dạng đề", r"TODO", r"Viete\b",
       r"CHỈ ĐỀ", r"ý [ab] của đề", r"LƯU Ý", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác", r"Như vậy"]

# đáp số then chốt phải có trong lời giải / ví dụ (so sau khi bỏ khoảng trắng)
DAP = {
    "Ví dụ 1.": ["65", r"-\dfrac{11}{2}", r"\dfrac72", r"\dfrac94"], "Ví dụ 2.": ["29", "39", "13"],
    "Ví dụ 3.": ["21", r"-\dfrac1{10}", r"-\dfrac{13}{6}"], "Ví dụ 4.": [r"\dfrac{16}{87}"],
    "Ví dụ 5.": ["341", r"\dfrac{23}{4}"], "Ví dụ 6.": [r"1+\sqrt2", "6"], "Ví dụ 7.": ["(m+1)^2", "m^2+1"],
    "Bài 1.": ["-3"], "Bài 2.": ["(x_1+x_2)^2-2x_1x_2"], "Bài 3.": ["-3"], "Bài 4.": [r"-\dfrac{11}{2}", r"-\dfrac{10}{3}"],
    "Bài 5.": ["2"], "Bài 7.": [r"-\sqrt2"], "Bài 8.": ["m<0"], "Bài 9.": ["(x_1+3)(x_2+3)"],
    "Bài 10.": ["17", "21"], "Bài 11.": ["53", "52"], "Bài 12.": ["8", "4"], "Bài 13.": ["41", r"-\dfrac{21}{10}"],
    "Bài 14.": ["40", r"-\dfrac29"], "Bài 15.": ["29", "-140"], "Bài 16.": ["a=1", "5", "7"],
    "Bài 17.": ["9-4m", r"\dfrac94", "-1008"], "Bài 18.": ["(m-2)^2", "m=-1", "m=3"], "Bài 19.": ["m=2", "m=-2"],
    "Bài 20.": [r"\dfrac4{25}", r"-\sqrt2"], "Bài 21.": [r"\dfrac72"], "Bài 22.": [r"\dfrac{3-\sqrt3}{2}"],
    "Bài 23.": ["m<-1"], "Bài 24.": [r"96\sqrt3"], "Bài 25.": [r"-\dfrac{22}9"], "Bài 26.": [r"-\dfrac37"],
    "Bài 27.": [r"\dfrac{157}4"], "Bài 28.": ["53"], "Bài 29.": ["19"], "Bài 30.": ["-9"],
    "Bài 31.": [r"4\sqrt3-3", "39"], "Bài 32.": ["8m+24", r"-\dfrac52"], "Bài 33.": ["4(m-2)^2", "m=0", "m=2"],
}

# Thầy 16/11 (Phiếu 1): sơ đồ tư duy chỉ kiến thức lõi của buổi ⇒ Viète + điều kiện + công thức đối xứng gốc.
MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"$ax^2+bx+c=0$ ($a\ne 0$)[[br]]có hai nghiệm $x_1$, $x_2$",
    "branches": [
        {"label": "Điều kiện", "children": [{"label": r"$\Delta[[blank:0.8cm]]0$ hoặc $a\cdot c[[blank:0.8cm]]0$"}]},
        {"label": "Định lí Viète", "children": [{"label": r"$x_1+x_2=[[blank:1.6cm]]$"},
                                                {"label": r"$x_1x_2=[[blank:1.6cm]]$"}]},
        {"label": "Theo tổng và tích", "children": [{"label": r"$x_1^2+x_2^2=[[blank:3.4cm]]$"},
                                                    {"label": r"$\dfrac1{x_1}+\dfrac1{x_2}=[[blank:1.8cm]]$"}]},
    ],
}
GIAI_BTVN = (r"Đáp án sơ đồ tư duy: $\Delta\ge0$ hoặc $a\cdot c<0$ · $x_1+x_2=-\dfrac ba$, $x_1x_2=\dfrac ca$ · "
             r"$x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$, $\dfrac1{x_1}+\dfrac1{x_2}=\dfrac{x_1+x_2}{x_1x_2}$.")

LT_SUA = [(", suy ra ", ", ta có "), ("(suy ra từ định lí Viète)", "(hệ quả của định lí Viète)")]
# Claude soát đợt 2 (16/11): bỏ "Do đó/Suy ra" còn sót ở bài NB (cổng nhịp chỉ soi level ≥ 2).
SUA = {  # nhãn → [(cũ, mới)] — sửa tay nhỏ sau khi đọc đầu ra (có assert)
    # Đúng/Sai: bảng đã in khẳng định ⇒ câu dẫn không chép lại (soi PDF 16/11).
    "Bài 1.": [(r"[NB] Bạn An nói: \textquotedblleft Không cần giải, tổng và tích hai nghiệm của phương trình $x^2-x+1=0$ đều bằng $1$.\textquotedblright\ Bạn An nói đúng hay sai? Vì sao?",
                r"[NB] Bạn An đưa ra khẳng định trong bảng dưới đây. Bạn An nói đúng hay sai? Vì sao?")],
    "Bài 2.": [(r"[NB] Có bạn cho rằng phương trình $x^2+x+1=0$ có tổng và tích các nghiệm là hai số đối nhau. Ý kiến đó đúng hay sai? Vì sao?",
                r"[NB] Bạn Bình tìm một phương trình bậc hai có tổng và tích các nghiệm là hai số đối nhau và đưa ra ý kiến trong bảng dưới đây. Ý kiến đó đúng hay sai? Vì sao?")],
    "Bài 3.": [(r"Suy ra $A=x_1^2+x_2^2", r"Ta có $A=x_1^2+x_2^2")],
    "Bài 5.": [(r"Do đó $x_1+x_2-x_1x_2", r"Ta có $x_1+x_2-x_1x_2")],
    "Bài 8.": [(r", tức là $1\cdot m<0$, suy ra $m<0$.", r", tức là $1\cdot m<0$.")],
    "Bài 12.": [(r"=\dfrac{2}{\frac{1}{2}}=4$", r"=2:\dfrac{1}{2}=4$")],
    "Bài 29.": [(r"a) Vì phương trình bậc hai với hệ số thực đã có một nghiệm $x_1=\dfrac{-\sqrt{13}-5}{2}$ nên phương trình có hai nghiệm $x_1$, $x_2$.[[br]]\hspace*{1.4em}Theo định lí Viète, ta có $x_1+x_2=-5$.",
                 r"a) Gọi $x_1=\dfrac{-\sqrt{13}-5}{2}$ và $x_2$ là nghiệm còn lại của phương trình.[[br]]\hspace*{1.4em}Theo định lí Viète, ta có $x_1+x_2=-5$.")],
    "Bài 22.": [(r"Suy ra phương trình có hai nghiệm $x_1=1$", r"Phương trình có hai nghiệm $x_1=1$"),
                (r"Suy ra phương trình có hai nghiệm $x_1=-1$", r"Phương trình có hai nghiệm $x_1=-1$")],
}
# Ví dụ 7: ô bọc $ đứng ngoài công thức ⇒ trinh_bay_gate cảnh báo math lồng math ⇒ đưa ô vào trong $…$.
SUA_VD = {  # nhãn ví dụ → [(cũ, mới)]
    "Ví dụ 4.": [(r"Quy đồng biểu thức $A$, ta được $A=\dfrac{x_2(x_2+3)+x_1(x_1+3)}{(x_1+3)(x_2+3)}=\dfrac{[[fill:x_1^2+x_2^2+3(x_1+x_2)]]}{x_1x_2+3(x_1+x_2)+9}$.",
                  r"Quy đồng, ta được $A=\dfrac{x_2(x_2+3)+x_1(x_1+3)}{(x_1+3)(x_2+3)}$[[br]]\hspace*{1.4em}$A=\dfrac{[[fill:x_1^2+x_2^2+3(x_1+x_2)]]}{x_1x_2+3(x_1+x_2)+9}$.")],
    # 17/11 gọn trang: Ví dụ 6 bớt 2 dòng tràn (giữ ý "không phụ thuộc m").
    "Ví dụ 6.": [(r"Vì phương trình đã có nghiệm nên theo định lí Viète, ta có $x_1+x_2=[[fill:2]]$ (không phụ thuộc vào $m$).",
                  r"Theo định lí Viète, $x_1+x_2=[[fill:2]]$, không phụ thuộc vào $m$."),
                 (r"Ta có tổng bình phương các nghiệm của phương trình là:[[br]]\hspace*{1.4em}$x_1^2+x_2^2=",
                  r"Ta có $x_1^2+x_2^2="),
                 (r"=[[fill:3-2\sqrt{2}]]+([[fill:3+2\sqrt{2}]])=", r"=[[fill:3-2\sqrt{2}]]+[[fill:3+2\sqrt{2}]]=")],
    "Ví dụ 7.": [
        (r"khi $\Delta>0$, tức là [[fill:$m\ne -1$]].", r"khi $\Delta>0$, tức là $m\ne [[fill:-1]]$."),
        (r"Đối chiếu điều kiện [[fill:$m\ne -1$]], cả hai", r"Đối chiếu điều kiện $m\ne -1$, cả hai"),
        (r"Vậy [[fill:$m=2$ hoặc $m=-2$]].", r"Vậy $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$."),
    ],
}
# 17/11 gọn trang (quét thử trên bản nháp: cùng với Bài 16a ⇒ phiếu HS 11 → 10 trang, trắng đáy 48 → 27cm).
GON_VD_SAU = {
    "Ví dụ 7.": [
        (r"Giải ra được $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$.[[br]]\hspace*{1.4em}Đối chiếu điều kiện $m\ne -1$, cả hai giá trị đều thỏa mãn.",
         r"Giải ra được $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$, cả hai đều thỏa mãn $m\ne -1$."),
    ],
}


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right", "", s or "")
    s = s.replace(r"\frac", r"\dfrac")
    s = re.sub(r"\\dfrac\{(\d+)\}\{(\d+)\}", lambda mm: r"\dfrac" + (mm[1] if len(mm[1]) == 1 else "{" + mm[1] + "}")
               + (mm[2] if len(mm[2]) == 1 else "{" + mm[2] + "}"), s)
    s = re.sub(r"\\dfrac\{([^{}]+)\}(\d)\b", r"\\dfrac{\1}\2", s)
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
            nf = b.get("text", "").count("[[fill:")
            if nf < 6:
                loi.append(f"{nh}: ví dụ ít ô fill ({nf})")
            if re.search(r"\[(NB|TH|VD)\]", b.get("text", "")):
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
            if ht == "vd_de":
                y_vd = b.get("statement", "").split("[VD]")[-1]
                if re.search(r"[Gg]ợi ý|[Hh]ướng dẫn|Bước", y_vd) or b.get("hints"):
                    loi.append(f"{nh}: ý [VD] có gợi ý")
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
    tat_ca = [("lt", json.dumps({k: v for k, v in lt.items() if k != "ghi_chu"}, ensure_ascii=False))] + \
             [(s["kind"], json.dumps(s, ensure_ascii=False)) for s in stages]
    for ten, txt in tat_ca:
        for pat in CAM:
            for mm in re.finditer(pat, txt):
                loi.append(f"[{ten}] /{pat}/: …{txt[max(0, mm.start() - 50): mm.end() + 30]}…")
        for mm in re.finditer(r"(?<!\\);", txt):
            loi.append(f"[{ten}] dấu ';': …{txt[max(0, mm.start() - 40): mm.end() + 20]}…")
    return loi


# 17/11 Thầy "nhiều khoảng trắng quá": hộp ví dụ lồng trong hộp chặng = khối cứng, nhảy nguyên khối ⇒ gọt đuôi
# thừa làm dòng tràn sang dòng thứ hai (vừa gọn chữ vừa hạ chiều cao hộp). Áp cho MỌI ví dụ.
GON_VD = [
    (r"hai nghiệm phân biệt \$x_1\$, \$x_2\$\.", "hai nghiệm phân biệt."),
    (r"hai nghiệm \[\[fill:trùng nhau\]\] \$x_1=x_2\$", "hai nghiệm [[fill:trùng nhau]]"),
    (r" \(nên \$x_1\\ne ?0\$ và \$x_2\\ne ?0\$\)", ""),
    (r"Thay \$x=-3\$ vào vế trái của phương trình, ta được (\$[^$]*=-29\\ne 0\$) nên \$x_1\\ne -3\$ và \$x_2\\ne -3\$\.",
     r"Vì \1 nên $x=-3$ không là nghiệm."),
]


def gon_vd(t):
    for pat, moi in GON_VD:
        t = re.sub(pat, moi, t)
    return t


def thay(nhan, s, bang):
    for cu, moi in bang.get(nhan, []):
        assert s.count(cu) == 1, (nhan, cu[:70])
        s = s.replace(cu, moi)
    return s


def dung_theo_so_do(moi):
    """Xếp khối practice1/2 đúng thứ tự KHOI (bài theo nhãn, ví dụ theo "Ví dụ N.")."""
    bai, vd = {}, {}
    for k in ("practice1", "practice2"):
        for b in moi[k]["blocks"]:
            nh = nhan_cua(b)
            if b.get("type") == "problem":
                bai[nh] = b
            elif nh and nh.startswith("Ví dụ"):
                vd[nh] = b
    dich = next(b for b in moi["practice1"]["blocks"] if "Đích của buổi học" in b.get("text", ""))
    out = {"practice1": [dich], "practice2": []}
    for k in KHOI:
        chang = k[1]
        if chang not in out:
            continue
        if len(k) == 3:
            out[chang].append({"type": "para", "variant": "heading", "text": k[0].replace("Đích + ", "")})
        elif k[7] == "vi_du":
            out[chang].append({"type": "noted", "variant": "example",
                               "text": thay(k[0], gon_vd(thay(k[0], vd[k[0]]["text"], SUA_VD)), GON_VD_SAU)})
        else:
            out[chang].append(bai[k[0]])
    return out


def ap_sua(stages):
    for s in stages:
        for b in s["blocks"]:
            for k in ("text", "statement", "solution"):
                if isinstance(b.get(k), str):
                    b[k] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", b[k].replace("–", "--"))
                    b[k] = b[k].replace("đề minh hoạ tuyển sinh 10", "minh hoạ vào 10")   # 17/11 gọn dòng nguồn
            for k in ("statement", "solution"):
                for cu, moi in SUA.get(b.get("label"), []):
                    if isinstance(b.get(k), str) and cu in b[k]:
                        assert b[k].count(cu) == 1, (b["label"], cu[:60])
                        b[k] = b[k].replace(cu, moi)


VID_DOT2 = ("sua-p2-ch6-9c-lop", "sua-p2-ch6-9c-btvn",   # viec_sua_p2_ch6_9c.py
            "sua3-p2-ch6-9c",                         # viec_sua3_p2_ch6_9c.py (17/11: NB một bước)
            "clean-p2-ch6-9c-lop", "clean-p2-ch6-9c-btvn",   # viec_clean_p2_ch6_9c.py (17/11: bỏ lời thừa)
            "delta-p2-ch6-9c")                         # viec_delta_p2_ch6_9c.py (17/11: Bài 11–16 tính Δ trước)


def ap_de_moi(stages):
    """Đề do Claude chốt (viec_clean_p2_ch6_9c.DE_MOI) là nguồn sự thật cho statement / dung_sai / options."""
    from viec_clean_p2_ch6_9c import DE_MOI, khoi_moi
    for s in stages:
        for b in s["blocks"]:
            if b.get("type") == "problem" and b.get("label") in DE_MOI:
                b.pop("dung_sai", None)          # khối lượt 1 có thể mang kiểu câu cũ (Bài 2/3 đổi kiểu 17/11)
                b.pop("options", None)
                b.update(khoi_moi(b["label"]))


def ap_dot2(stages):
    """Đè bản đợt 2 (Gemini sửa theo validate lượt 1) lên bài/ví dụ cùng nhãn; giữ dung_sai, options cũ."""
    sua = {}
    for vid in VID_DOT2:
        if (REPO / "storage/gemini/xong" / f"{vid}.json").exists():
            sua.update({x["label"]: x for x in lay(vid)["sua"]})
    for s in stages:
        for b in s["blocks"]:
            nh = nhan_cua(b)
            if nh not in sua:
                continue
            if b.get("type") == "problem":
                b["statement"], b["solution"] = sua[nh]["statement"], sua[nh]["solution"]
                if sua[nh].get("options"):
                    b["options"] = sua[nh]["options"]
            else:
                b["text"] = sua[nh]["statement"]


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    p = REPO / SEED
    f = json.loads(p.read_text())
    f["title"] = "Bài 20. Định lí Viète — biểu thức đối xứng của hai nghiệm"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU 2"
    ap_dot2(lop["stages"] + btvn["stages"])
    ap_de_moi(lop["stages"] + btvn["stages"])
    ap_sua(lop["stages"] + btvn["stages"])
    moi ={s["kind"]: s for s in lop["stages"] + btvn["stages"]}
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
    for b in lt["concept_blocks"]:            # Claude soát 16/11: lý thuyết không dùng "suy ra"
        for cu, thay_bang in LT_SUA:
            b["text"] = b["text"].replace(cu, thay_bang)
    cp["blocks"] = lt["concept_blocks"]
    cp["teacher_note"] = tn["concept"]
    cp.pop("solution", None)
    for k, bl in dung_theo_so_do(moi).items():
        st[k]["title"] = moi[k]["title"]
        st[k]["blocks"] = bl
        st[k]["teacher_note"] = tn[k]
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
