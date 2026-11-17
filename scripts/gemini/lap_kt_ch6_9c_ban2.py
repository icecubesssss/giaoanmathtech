#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ráp 2 kết quả Gemini (kt2-9c-ch6-de + kt2-9c-ch6-dap-an) -> đề kiểm tra chương VI 9C bản 2 (90 phút).

    .venv/bin/python scripts/gemini/lap_kt_ch6_9c_ban2.py          # chỉ soát, in lỗi
    .venv/bin/python scripts/gemini/lap_kt_ch6_9c_ban2.py --ghi    # soát + ghi 3 file

Ghi: kiem-tra-chuong/{de-kiem-tra-chuong-vi, ma-tran-va-dap-an-kiem-tra-chuong-vi}.json (theme de_thi)
     + de-kiem-tra.json (DeSpec 90 phút).
Ma trận sinh từ SO_DO của viec_kt_ch6_9c_ban2.py (một nguồn số liệu).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_kt_ch6_9c_ban2 import D, DIEM_Y, DUNG, SO_DO, VID_DA, VID_DE  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
KT = REPO / D / "kiem-tra-chuong"
CAM = [
    r"\bem\b", r"các em", r"[Hh]ôm nay", r"\bKiểm\b(?! tra)", r"\bSoi\b",
    r"\$S\$", r"\$P\$", r"\bS\s*=", r"\bP\s*=",
    r"\\Leftrightarrow", r"⇔", r"\\Rightarrow", r"⇒",
    r"\\Delta'", r"\\Delta\^\{?\\prime", r"Δ′", r"b'",
    r"TMĐK", r"\(TM\)", r"\(L\)", r"ĐKXĐ", r"chứa ẩn ở mẫu",
]

DAP_KT = {
    "5": ["x_1=1", "x_2=2", "x_1=-1", "-\\dfrac{3}{2}"],
    "6": ["(m-3)^2"],
    "7": ["-60", "\\dfrac{121}{4}"],
    "8": ["\\dfrac{3-\\sqrt{21}}{2}", "21"],
    "9": ["\\sqrt{2}", "\\dfrac{7}{4}"],
    "10": ["x^2+5x-750=0", "25"],
    "11": ["x^2-26x+160=0", "10"],
}


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text(encoding="utf-8"))
    data = kq.get("ket_qua") or kq
    if data.get("ghi_chu"):
        print(f"[{vid}] ghi_chu Gemini: {data['ghi_chu']}")
    return data["stages"]


def so(x):
    return f"{x:g}".replace(".", "{,}")


def chuan(s):
    s = re.sub(r"\s|\\[,;!]|\\left|\\right|\\ ", "", s or "")
    s = s.replace(r"\frac", r"\dfrac")
    s = re.sub(
        r"\\dfrac\{(\d+)\}\{(\d+)\}",
        lambda mm: r"\dfrac"
        + (mm[1] if len(mm[1]) == 1 else "{" + mm[1] + "}")
        + (mm[2] if len(mm[2]) == 1 else "{" + mm[2] + "}"),
        s,
    )
    return re.sub(r"\\sqrt\{(\d+)\}", lambda mm: r"\sqrt" + (mm[1] if len(mm[1]) == 1 else "{" + mm[1] + "}"), s)


def bang_ma_tran():
    bang = (
        "\\begin{center}\\footnotesize\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{9.0cm}|c|c|c|}\n\\hline\n"
        "\\textbf{Câu} & \\textbf{Nội dung kiến thức, kĩ năng} & \\textbf{Mức} & \\textbf{Điểm} & \\textbf{Phút} \\\\ \\hline\n"
        + "".join(
            f"{c.replace('Câu ', '')} & {nd} & {m} & ${so(d)}$ & ${so(ph)}$ \\\\ \\hline\n"
            for c, nd, m, d, ph, _h, _a, _ma in SO_DO
        )
        + "\\end{tabular}\\end{center}"
    )
    tong = {}
    for _c, _n, m, d, ph, _h, _a, _ma in SO_DO:
        a = tong.setdefault(m, [0, 0])
        a[0] += d
        a[1] += ph
    bt = (
        "\\begin{center}\\footnotesize\n\\begin{tabular}{|l|c|c|c|c|}\n\\hline\n"
        "\\textbf{Mức} & \\textbf{NB} & \\textbf{TH} & \\textbf{VD} & \\textbf{Tổng} \\\\ \\hline\n"
        f"Điểm & ${so(tong['NB'][0])}$ & ${so(tong['TH'][0])}$ & ${so(tong['VD'][0])}$ & \\textbf{{10}} \\\\ \\hline\n"
        f"Phút & ${so(tong['NB'][1])}$ & ${so(tong['TH'][1])}$ & ${so(tong['VD'][1])}$ & "
        f"\\textbf{{{so(sum(v[1] for v in tong.values()))}}} \\\\ \\hline\n\\end{{tabular}}\\end{{center}}"
    )
    return bang, bt, tong


def soat(de_st, da_st):
    loi = []
    assert abs(sum(r[3] for r in SO_DO) - 10) < 1e-9 and sum(r[4] for r in SO_DO) <= 90
    if [s["kind"] for s in de_st] != ["review", "concept", "practice1", "practice2", "reflection"]:
        loi.append(f"tờ đề sai thứ tự chặng: {[s['kind'] for s in de_st]}")
    if [s["kind"] for s in da_st] != ["concept", "practice1", "practice2", "reflection"]:
        loi.append(f"đáp án sai thứ tự chặng: {[s['kind'] for s in da_st]}")
    nhan = []
    for s in de_st:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                nhan.append(b.get("label"))
                if b["label"] in DUNG:
                    if len(b.get("options", [])) != 4:
                        loi.append(f"{b['label']} không đủ 4 phương án")
                    if b.get("answer") != DUNG[b["label"]]:
                        loi.append(f"{b['label']} answer={b.get('answer')} != {DUNG[b['label']]}")
                if "solution" in b:
                    loi.append(f"{b['label']} tờ đề có solution")
                if re.search(r"\[(NB|TH|VD|VDC)\]", b.get("statement", "")):
                    loi.append(f"{b['label']} tờ đề có thẻ mức")
    if nhan != [f"Câu {i}." for i in range(1, 12)]:
        loi.append(f"nhãn câu lệch: {nhan}")

    # chữ cái trong đáp án Phần I
    t1 = da_st[0]["blocks"][0]["text"]
    for k, v in DUNG.items():
        if not re.search(rf"{k[4]}\s*[–-]\s*{v}\b", t1):
            loi.append(f"đáp án Phần I thiếu '{k[4]} – {v}'")

    # tổng barem từng ý + đáp số then chốt
    toan = " [[br]] ".join(b.get("text", "") for s in da_st[:3] for b in s["blocks"])
    for cau in ("5", "6", "7", "8", "9", "10", "11"):
        m = re.search(rf"\\textbf{{Câu {cau}\b.*?(?=\\textbf{{Câu {int(cau) + 1}\b|$)", toan, re.S)
        if not m:
            loi.append(f"không thấy đáp án Câu {cau}")
            continue
        khoi = m.group(0)
        if cau in ("5", "7", "9"):
            phan = re.split(r"\[\[br\]\]\s*(?=[ab]\))", khoi)[1:]
            if len(phan) != 2:
                loi.append(f"Câu {cau}: tách được {len(phan)} ý, cần 2")
                continue
            ys = [f"{cau}a", f"{cau}b"]
        else:
            phan = [khoi]
            ys = [cau]
        for y, p in zip(ys, phan):
            tong = sum(float(x.replace(",", ".")) for x in re.findall(r"\((\d+(?:,\d+)?)đ\)", p))
            if abs(tong - DIEM_Y[y]) > 1e-9:
                loi.append(f"barem ý {y}: cộng {tong} != {DIEM_Y[y]}")
        for d in DAP_KT.get(cau, []):
            if chuan(d) not in chuan(khoi):
                loi.append(f"Câu {cau}: thiếu đáp số {d}")

    # từ cấm + chấm phẩy nối công thức
    for s in de_st + da_st:
        for b in s["blocks"]:
            for k in ("statement", "text"):
                v = b.get(k) or ""
                for pat in CAM:
                    if re.search(pat, v):
                        loi.append(f"từ cấm /{pat}/ ở {b.get('label') or v[:40]}")
                if re.search(r"\$\s*;\s*\$", v):
                    loi.append(f"chấm phẩy nối công thức ở {b.get('label') or v[:40]}")
    return loi


def main():
    de_st, da_st = lay(VID_DE), lay(VID_DA)
    loi = soat(de_st, da_st)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} lỗi")
    if "--ghi" not in sys.argv:
        return
    for s in de_st:
        s["title"] = ""
        s.pop("teacher_note", None)
        for b in s["blocks"]:
            if b.get("label") == "Câu 9." and isinstance(b.get("statement"), str):
                b["statement"] = b["statement"].replace("[[br]]", " \\\\*[3pt] ")
    for s in da_st:
        s.pop("teacher_note", None)
        for b in s["blocks"]:
            if isinstance(b.get("text"), str):
                b["text"] = b["text"].replace(
                    r"Theo định lí Viète, tích hai nghiệm là $x_1x_2=-3$, nên $x_2=",
                    r"Theo định lí Viète, tích hai nghiệm là $x_1x_2=-3$[[br]]nên $x_2=",
                )
                b["text"] = b["text"].replace(
                    r"$\dfrac{3}{m-1}=4$, suy ra $m-1=\dfrac{3}{4}$, tức $m=\dfrac{7}{4}$.",
                    r"$\dfrac{3}{m-1}=4$[[br]]$m-1=\dfrac{3}{4}$[[br]]$m=\dfrac{7}{4}$.",
                )
                b["text"] = re.sub(
                    r"(\\textbf\{Câu \d+ \([^)]+\)\.\})\s*\[\[br\]\]\s*",
                    r"\1\\\\*[3pt] ",
                    b["text"],
                )
    bang, bt, tong = bang_ma_tran()
    mas = list(dict.fromkeys(r[7] for r in SO_DO))
    nguon_lines = [
        ", ".join(f"\\texttt{{{m}}}" for m in mas[i : i + 3])
        for i in range(0, len(mas), 3)
    ]
    nguon = "[[br]]".join(nguon_lines)
    head = {
        "kind": "review",
        "number": 1,
        "title": "Ma trận đề",
        "blocks": [
            {
                "type": "para",
                "text": (
                    "\\textbf{ĐỀ KIỂM TRA CHƯƠNG VI — PHƯƠNG TRÌNH BẬC HAI MỘT ẨN (LỚP 9C)} "
                    "($90$ phút, thang điểm $10$). "
                    "\\textbf{Phạm vi:} trọn chương VI bản 2 (Phiếu 1--5) — công thức nghiệm $\\Delta=b^2-4ac$, "
                    "nhẩm nghiệm, chứng minh phương trình luôn có nghiệm, định lí Viète và tìm $m$ theo hệ thức, "
                    "giải bài toán bằng cách lập phương trình. "
                    "KHÔNG có phương trình chứa ẩn ở mẫu (đã bỏ ở Phiếu 4, 5), KHÔNG dùng $\\Delta'$, "
                    "KHÔNG dùng kí hiệu $S$, $P$ cho tổng và tích hai nghiệm."
                ),
            },
            {"type": "para", "text": bang},
            {"type": "para", "text": bt},
        ],
    }
    da_st[-1]["blocks"].append(
        {
            "type": "para",
            "text": "\\textbf{Mã nguồn ngân hàng} (tab Phân dạng Ch.VI):[[br]]" + nguon + ".",
        }
    )

    base = {"grade_label": "Lớp 9 • Đại số", "class_tier": "C", "theme": "de_thi"}
    de = {
        "slug": "de-kiem-tra-chuong-vi-lop-9c",
        "title": "Đề kiểm tra Chương VI — Phương trình bậc hai một ẩn (90 phút)",
        "eyebrow": "LỚP 9C • KIỂM TRA CHƯƠNG VI",
        **base,
        "stages": de_st,
    }
    mt = {
        "slug": "ma-tran-va-dap-an-kiem-tra-chuong-vi-lop-9c",
        "title": "Ma trận và đáp án — Kiểm tra Chương VI",
        "eyebrow": "TÀI LIỆU GIÁO VIÊN • LỚP 9C • KIỂM TRA CHƯƠNG VI",
        **base,
        "stages": [head] + da_st,
    }
    KT.mkdir(parents=True, exist_ok=True)
    (KT / "de-kiem-tra-chuong-vi.json").write_text(json.dumps(de, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (KT / "ma-tran-va-dap-an-kiem-tra-chuong-vi.json").write_text(
        json.dumps(mt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    de_spec = {
        "slug": "thuyet-minh-de-lop-9c-chuong-06-pt-bac-hai",
        "title": "Chương VI. Phương trình bậc hai một ẩn — bản 2 • kiểm tra chương (90 phút)",
        "grade": "lop-9",
        "subject": "dai-so",
        "tier": "C",
        "chuong": "Chương VI (Bài 19 – Bài 21 SGK), bản 2 (5 buổi)",
        "ghi_chu": [
            "Thầy chốt 16/11/2026: đề kiểm tra chương VI 9C làm trong $90$ phút (làm ở phiên Phiếu 5). Tham số $m$ quay lại ở biện luận $\\Delta$ và định lí Viète.",
            "Thầy chốt 17/11/2026: bỏ hẳn phương trình chứa ẩn ở mẫu (C6-17) và công thức nghiệm thu gọn $\\Delta'$, $b'$ khỏi chương VI 9C.",
            "KHÔNG dùng kí hiệu tắt $S$, $P$ cho tổng và tích hai nghiệm; KHÔNG dùng dấu $\\Leftrightarrow$ hay $\\Rightarrow$ trong lời giải.",
            "100\\% câu hỏi lấy từ ngân hàng phân dạng, không trùng số liệu với bài ví dụ hay luyện tập trên lớp của Phiếu 1--5.",
            "Tờ đề học sinh không in đáp số; ma trận và đáp án chi tiết ở thư mục \\texttt{kiem-tra-chuong/}.",
        ],
        "de": [
            {
                "ma": "KT-VI",
                "ten": "Đề kiểm tra Chương VI — Phương trình bậc hai một ẩn (90 phút)",
                "tuan": 26,
                "phut": 90,
                "diem_toi_da": 10.0,
                "pham_vi": (
                    "Trọn chương VI bản 2 (Phiếu 1--5): giải phương trình bậc hai bằng công thức nghiệm $\\Delta$ và nhẩm nghiệm, "
                    "chứng minh phương trình luôn có nghiệm, định lí Viète (tính biểu thức đối xứng, tìm $m$ theo hệ thức), "
                    "giải bài toán bằng cách lập phương trình."
                ),
                "cau": [
                    {"ma": c, "dang": nd, "band": m, "diem": d, "phut": ph, "hinh_thuc": h, "dap_an": a}
                    for c, nd, m, d, ph, h, a, _ma in SO_DO
                ],
            }
        ],
    }
    (REPO / D / "de-kiem-tra.json").write_text(json.dumps(de_spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Đã ghi 3 file:", {k: v for k, v in tong.items()})


if __name__ == "__main__":
    main()
