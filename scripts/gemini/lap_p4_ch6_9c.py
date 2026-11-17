#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-p4-ch6-9c-{lt,lop,btvn} vào seed Phiếu 4 ch.VI 9C bản 2 + soát đầu ra.

    .venv/bin/python scripts/gemini/lap_p4_ch6_9c.py          # soát, không ghi
    .venv/bin/python scripts/gemini/lap_p4_ch6_9c.py --ghi    # ghi seed

ĐỀ bài lấy từ sơ đồ của Claude (so_do_p4_ch6_9c.KHOI — nguồn sự thật), Gemini chỉ góp LỜI GIẢI, text ví dụ, lý thuyết.
Soát: đủ nhãn, từ cấm (chỉ trong phần Gemini viết — vài đề gốc có sẵn "Do đó"), ";", ⇔, Δ′, ô "]]]"; ví dụ đủ ô
[[fill:]] và đề ví dụ khớp sơ đồ; đáp số then chốt có mặt. Khuôn từ lap_p3_ch6_9c.py.
Bảng SUA/SUA_VD = Claude sửa tay nhỏ sau khi đọc đầu ra (có assert). VID_SUA = việc nhỏ đợt sau, đè theo nhãn.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p4_ch6_9c import KHOI, OPTIONS  # noqa: E402
from viec_dung_p4_ch6_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"tầng C", r"\bem\b", r"[Cc]ác em", r"[Hh]ôm nay", r"buổi này",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bnhé\b", r"mẹo", r"chìa khóa", r"\bbẫy\b", r"Leftrightarrow", r"⇔",
       r"\\Rightarrow", r"⇒", r"iff\b", r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'", r"thu gọn \$\\Delta",
       r"dạng đề", r"TODO", r"[Cc]hỉ đề", r"BÀI ĐÍCH", r"\d–\d ô", r"[Dd]o đó", r"[Ss]uy ra", r"Mặt khác",
       r"Như vậy", r"GHI CHÚ", r"ĐỌC ẢNH", r"TMĐK", r"\(TM\)", r"\(L\)", r"\]\]\]",
       r"ĐKXĐ", r"[Đđ]iều kiện xác định", r"chứa ẩn ở mẫu"]   # 17/11 lượt 3: bỏ hẳn phần ẩn ở mẫu

# 17/11 lượt 3 (bỏ phần phương trình chứa ẩn ở mẫu): nhãn MỚI → nhãn ở bản dựng đầu (dung-p4-ch6-9c-lop/-btvn).
# Bài 1, 7, 9, 14, 19 là bài mới — lấy từ việc sua-p4-ch6-9c-bai.
NHAN_CU = {"Ví dụ 1.": "Ví dụ 3.", "Bài 2.": "Bài 4.", "Ví dụ 2.": "Ví dụ 4.", "Bài 3.": "Bài 5.",
           "Ví dụ 3.": "Ví dụ 5.", "Bài 4.": "Bài 6.", "Ví dụ 4.": "Ví dụ 6.", "Bài 5.": "Bài 7.", "Bài 6.": "Bài 8.",
           "Ví dụ 5.": "Ví dụ 7.", "Bài 8.": "Bài 9.", "Ví dụ 6.": "Ví dụ 8.", "Bài 10.": "Bài 10.",
           "Ví dụ 7.": "Ví dụ 9.", "Bài 11.": "Bài 11.", "Bài 12.": "Bài 14.", "Bài 13.": "Bài 15.",
           "Bài 15.": "Bài 16.", "Bài 16.": "Bài 17.", "Bài 17.": "Bài 18.", "Bài 18.": "Bài 19.",
           "Bài 20.": "Bài 20.", "Bài 21.": "Bài 21."}

DAP = {  # đáp số then chốt (so sau khi chuẩn hoá) — theo nhãn mới
    "Bài 1.": ["Chọn A"], "Ví dụ 1.": ["8100", "30", "60"], "Bài 2.": ["1156", "14", "20"],
    "Ví dụ 2.": ["810000", "400"], "Bài 3.": ["12100", "50"], "Ví dụ 3.": ["324", "10"], "Bài 4.": ["484", "12"],
    "Ví dụ 4.": ["6084", "15"], "Bài 5.": ["x^2-15x-16", "16"], "Bài 6.": [r"\dfrac85", "6100", "500"],
    "Ví dụ 5.": ["12996", "54", "60"], "Bài 7.": ["x^2+20x-4800", "19600", "60", "80"],
    "Bài 8.": [r"\dfrac12", "8100", "40"], "Ví dụ 6.": ["x^2-2x-24", "x_1=6", "12"],
    "Bài 9.": [r"\dfrac{1}{t}", r"\dfrac{18}5", r"\dfrac5{18}", "5x^2-21x-54", "1521", "9"],
    "Bài 10.": [r"\dfrac83", r"\dfrac38", "3x^2-4x-32", "400"],
    "Ví dụ 7.": ["x^2+42x-4320", "48"], "Bài 11.": [r"\dfrac1{20}", "x^2+6x-1080", "4356", "36"],
    "Bài 12.": ["h=0", "t=4"], "Bài 13.": ["x^2+3x-270", "15", "24"], "Bài 14.": ["x^2+11x-180", "841", "9", "20"],
    "Bài 15.": ["72900", "120"], "Bài 16.": ["x^2-3x-108", "12"], "Bài 17.": ["11025", "45", "60"],
    "Bài 18.": [r"\dfrac35", "x^2+3x-180", "12"], "Bài 19.": ["x^2+25x-3750", "15625", "50", "75"],
    "Bài 20.": [r"\dfrac{420}{x+5}", "x^2+5x-1050", "30"], "Bài 21.": [r"\dfrac25", "x^2+5x-2250", "45"],
}

# Sơ đồ tư duy: chỉ kiến thức lõi của buổi (Thầy 16/11).
MINDMAP = {
    "type": "mindmap", "caption": "Điền các ô trống để tự tóm tắt buổi học",
    "root": r"Giải bài toán[[br]]bằng cách lập phương trình",
    "branches": [
        {"label": "Bước 1. Lập phương trình", "children": [
            {"label": r"Chọn ẩn, đặt [[blank:1.8cm]] cho ẩn"},
            {"label": r"Thời gian $=\dfrac{\text{quãng đường}}{[[blank:1.4cm]]}$"}]},
        {"label": "Bước 2. Giải phương trình", "children": [
            {"label": r"Nhân hai vế với [[blank:1.6cm]] để khử mẫu"},
            {"label": r"Giải phương trình bậc hai bằng công thức nghiệm"}]},
        {"label": "Bước 3. Trả lời", "children": [
            {"label": r"Đối chiếu nghiệm với [[blank:1.8cm]] rồi kết luận"}]},
    ],
}
GIAI_BTVN = r"Đáp án sơ đồ tư duy: điều kiện · vận tốc · mẫu chung · điều kiện của ẩn."

VID_SUA = ("sua-p4-ch6-9c-bai",)   # việc sửa (đè theo nhãn MỚI)
VID_LT_MOI = "sua-p4-ch6-9c-lt"     # lý thuyết bản bỏ ẩn ở mẫu
SUA = {  # nhãn MỚI → [(cũ, mới)] trong solution
    # soi PDF GV 17/11: "PT dài nên PT" ngắt giữa biểu thức ⇒ hai dòng
    "Bài 6.": [(r"=6$ nên $\dfrac{1\,200}{x}", r"=6$[[br]]\hspace*{1.4em}$\dfrac{1\,200}{x}")],
    "Bài 11.": [(r"=\dfrac{12}{x}$ nên $\dfrac{9}{x}", r"=\dfrac{12}{x}$[[br]]\hspace*{1.4em}$\dfrac{9}{x}")],
    # 17/11 Thầy "Các câu NB nhắc lại các công thức của tôi đâu?" ⇒ ý a) "Nêu điều kiện" thành câu nhắc công thức
    # (điều kiện chuyển vào lời ý b) của đề), đáp án ý a) sửa tay theo.
    "Bài 2.": [(r"a) $x>0$.", r"a) $S=a\cdot b$.")],
    "Bài 3.": [(r"a) $x\in\mathbb N^*$.", r"a) Thời gian hoàn thành $=\dfrac{\text{khối lượng công việc}}{\text{năng suất}}$.")],
    "Bài 4.": [(r"a) $x\in\mathbb N$, $x>2$.", r"a) Mỗi xe chở $\dfrac{A}{k}$ (tấn).")],
    "Bài 5.": [(r"a) $x>4$.", r"a) $t=\dfrac{s}{v}$.")],
    "Bài 15.": [(r"a) Điều kiện: $x\in\mathbb N^*$.", r"a) Năng suất $=\dfrac{\text{khối lượng công việc}}{\text{thời gian}}$.")],
    "Bài 16.": [(r"a) Điều kiện: $x\in\mathbb N$, $x>3$.", r"a) Mỗi người phải làm $\dfrac{A}{k}$ dụng cụ.")],
}
SUA_VD = {  # nhãn MỚI → [(cũ, mới)] trong text
    # 17/11 trinh_bay_gate: ô [[fill:$…$]] lồng math ⇒ Tectonic chết
    "Ví dụ 1.": [(r"chiều dài là [[fill:$x+30$]] (m)", r"chiều dài là $[[fill:x+30]]$ (m)"),
                 (r"chiều dài của sân bóng là [[fill:$x+30$]] (m)", r"chiều dài của sân bóng là $[[fill:x+30]]$ (m)"),
                 (r"Câu nào cho phương trình? [[fill:diện tích bằng $1\,800\ \text{m}^2$]]",
                  r"Đại lượng nào cho phương trình? [[fill:diện tích]] bằng $1\,800\ \text{m}^2$"),
                 # soi PDF: "… $=$ ô hay ô dài" xuống dòng, giãn chữ ⇒ tách hai dòng
                 (r"$x(x+30)=[[fill:1\,800]]$ hay $[[fill:x^2+30x-1\,800=0]]$.",
                  r"$x(x+30)=[[fill:1\,800]]$.[[br]]\hspace*{1.4em}Thu gọn: $[[fill:x^2+30x-1\,800=0]]$.")],
}
TN_SUA = []             # [(khoá teacher_notes, cũ, mới)]
LT_SUA = [  # [(cũ, mới)] trong concept/review/opener — 17/11 dan_dat_gate cấm "Hôm nay" trong đề đích
    ("Hôm nay, vẫn trên đoạn đường đó", "Một hôm, vẫn trên đoạn đường đó"),
    # 17/11 Thầy "Mấy cái công thức năng suất đâu?" ⇒ dòng gộp ở Nhắc lại chuyển thành bảng công thức (CONG_THUC)
    (r"[[br]]$\bullet$\; Quãng đường $=$ vận tốc $\times$ thời gian, khối lượng công việc $=$ năng suất $\times$ "
     r"thời gian (Toán 5).", ""),
]
CONG_THUC = [  # mục 2 Kiến thức cần nhớ — Claude chốt (công thức phải đúng tuyệt đối)
    {"type": "para", "variant": "heading", "text": "Các công thức thường dùng"},
    {"type": "para", "text":
     r"\textit{Năng suất.} Khối lượng công việc $=$ năng suất $\times$ thời gian.[[br]]"
     r"\hspace*{1.4em}Năng suất $=\dfrac{\text{khối lượng công việc}}{\text{thời gian}}$, "
     r"\quad thời gian $=\dfrac{\text{khối lượng công việc}}{\text{năng suất}}$.[[br]]"
     r"\hspace*{1.4em}Chia đều: tổng khối lượng $A$ chia đều cho $k$ xe (người) thì mỗi xe (người) làm $\dfrac{A}{k}$.[[br]]"
     r"\textit{Làm chung, làm riêng.} Làm một mình xong công việc trong $t$ giờ thì trong $1$ giờ làm được "
     r"$\dfrac{1}{t}$ công việc.[[br]]"
     r"\textit{Chuyển động.} $s=v\cdot t$, \quad $v=\dfrac{s}{t}$, \quad $t=\dfrac{s}{v}$ "
     r"($s$ quãng đường, $v$ vận tốc, $t$ thời gian).[[br]]"
     r"\hspace*{1.4em}Trên dòng nước: vận tốc xuôi dòng $=$ vận tốc thực $+$ vận tốc dòng nước, "
     r"vận tốc ngược dòng $=$ vận tốc thực $-$ vận tốc dòng nước.[[br]]"
     r"\textit{Hình chữ nhật.} Chiều dài $a$, chiều rộng $b$: diện tích $S=a\cdot b$, chu vi $P=2(a+b)$. "
     r"\textit{(Toán 4, Toán 5, SGK Toán 9 tập hai tr.26)}"},
]


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
                if b["level"] == 3:
                    y_vd = b["statement"].split("[VD]")[-1]
                    if re.search(r"[Gg]ợi ý|[Hh]ướng dẫn|Bước", y_vd):
                        loi.append(f"{nh}: ý [VD] có gợi ý")
                if not b.get("options") and not re.search(r"Vậy", txt):
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


def main():
    lop, btvn = lay(VID_LOP), lay(VID_BTVN)
    lt = lay(VID_LT_MOI) if (REPO / "storage/gemini/xong" / f"{VID_LT_MOI}.json").exists() else lay(VID_LT)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:1500])
    cu = {x["label"]: x for x in lop["sua"] + btvn["sua"]}
    sua = {}
    for moi, nh_cu in NHAN_CU.items():        # bản dựng đầu → nhãn mới (17/11 lượt 3)
        g = dict(cu[nh_cu], label=moi)
        if moi.startswith("Ví dụ"):
            g["statement"] = g["statement"].replace(rf"\textbf{{{nh_cu}}}", rf"\textbf{{{moi}}}", 1)
        sua[moi] = g
    for vid in VID_SUA:
        if (REPO / "storage/gemini/xong" / f"{vid}.json").exists():
            sua.update({x["label"]: x for x in lay(vid)["sua"]})
    for x in sua.values():
        for k in ("statement", "solution"):
            x[k] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", x[k].replace("–", "--"))
    khoi, loi = dung(sua)
    for k in khoi.values():                    # đề sơ đồ cũng đổi số bài tập SGK 6.15 → 6{.}15
        for b in k:
            if b.get("type") == "problem":
                b["statement"] = re.sub(r"\b6\.(\d\d)\b", r"6{.}\1", b["statement"])

    p = REPO / SEED
    f = json.loads(p.read_text())
    f["title"] = "Bài 21. Giải bài toán bằng cách lập phương trình"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU 4"
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
    # soi PDF 17/11: tiêu đề "Nhắc lại" đứng riêng rơi lẻ cuối trang 1 ⇒ gộp vào hộp
    rv["blocks"] = [{"type": "opener", "text": lt["opener_text"]},
                    {"type": "noted", "variant": "note",
                     "text": r"\textbf{Nhắc lại kiến thức đã học.}[[br]]" + lt["review_note"]}]
    cp = st["concept"]
    cp.update(title="Kiến thức cần nhớ", teacher_note=tn["concept"], blocks=lt["concept_blocks"] + CONG_THUC)
    cp.pop("solution", None)
    dich = {"type": "para", "text": r"\textbf{Đích của buổi học:} Bài 11 — đề thi thử vào 10 THCS Tự Lập 2025--2026: "
            r"bài toán chuyển động hai giai đoạn, phương trình lập được đưa về phương trình bậc hai.[[br]]Mạch 1--4 luyện "
            r"ba bước giải bài toán bằng cách lập phương trình (hình chữ nhật, năng suất, chuyển động, làm chung), Mạch 5 "
            r"là bài toán hai giai đoạn."}
    for k, ten in (("practice1", "Luyện tập 1 — Hình chữ nhật, năng suất"),
                   ("practice2", "Luyện tập 2 — Chuyển động, làm chung")):
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
