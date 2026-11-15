#!/usr/bin/env python3
"""Áp 2 việc dung-9c-ch6-phieu-e-{lop,btvn}: thay chặng practice1, practice2 và phần BTVN của reflection.

    python3 scripts/gemini/lap_dung_lai_phieu_e_9c.py          # soát
    python3 scripts/gemini/lap_dung_lai_phieu_e_9c.py --ghi    # ghi seed

Giữ: opener, nhắc lại, Kiến thức cần nhớ, sơ đồ tư duy (đã sửa lượt trước). Thêm `check` (SymPy) theo đáp số Claude đã kiểm.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_dung_lai_phieu_e_9c import SEED, VID_BTVN, VID_LOP  # noqa: E402

CHECK = {  # phương trình bậc hai sau khử mẫu, đáp số đã kiểm SymPy
    "Bài 1.": ("x**2 + 10*x - 3000 = 0", [50, -60]),
    "Bài 2.": ("x**2 + 20*x - 2400 = 0", [40, -60]),
    "Bài 3.": ("5*x**2 - 21*x - 54 = 0", [6, -9/5]),
    "Bài 4.": ("x**2 - 2*x - 120 = 0", [12, -10]),
    "Bài 5.": ("x**2 + 20*x - 4800 = 0", [60, -80]),
    "Bài 6.": ("x**2 - 7*x - 30 = 0", [10, -3]),
    "Bài 7.": ("x**2 - 3*x - 28 = 0", [7, -4]),
    "Bài 8.": ("x**2 + 6*x - 1080 = 0", [30, -36]),
    "Bài 9.": ("x**2 - 2*x - 80 = 0", [10, -8]),
    "Bài 10.": ("x**2 + 4*x - 96 = 0", [8, -12]),
    "Bài 12.": ("x**2 - 2*x - 24 = 0", [6, -4]),
    "Bài 13.": ("x**2 - 50*x - 5000 = 0", [100, -50]),
    "Bài 14.": ("x**2 + 8*x - 240 = 0", [12, -20]),
    "Bài 15.": ("x**2 + 10*x - 1200 = 0", [30, -40]),
}
DAP_SO = {"Bài 1.": "50", "Bài 2.": "40", "Bài 3.": "6", "Bài 4.": "12", "Bài 5.": "60", "Bài 6.": "10", "Bài 7.": "7",
          "Bài 8.": "36", "Bài 9.": "10", "Bài 10.": "8", "Bài 11.": "90", "Bài 12.": "6", "Bài 13.": "100",
          "Bài 14.": "12", "Bài 15.": "30"}
CAM = [r"[Kk]huôn", r"Câu III(?!\.\d đề)", r"thang điểm", r"chưa cần giải", r"\bem\b", r"các em", r"[Hh]ôm nay",
       r"\bKiểm\b(?! tra)", r"\bSoi\b", r"Do đó", r"[Ss]uy ra", r"Như vậy", r">\s*0\$,? nên \$\\sqrt"]


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def main():
    lop, btvn = lay(VID_LOP), lay(VID_BTVN)
    for g in (lop, btvn):
        if g.get("ghi_chu"):
            print("ghi_chu:", g["ghi_chu"][:1500])
    p = REPO / SEED
    f = json.loads(p.read_text())
    st = {s["kind"]: s for s in f["stages"]}
    moi = {s["kind"]: s for s in lop["stages"] + btvn["stages"]}
    for k in ("practice1", "practice2"):
        for kk in ("title", "teacher_note", "blocks"):
            st[k][kk] = moi[k][kk]
    rf = st["reflection"]
    giu = [b for b in rf["blocks"] if b.get("type") == "mindmap"
           or (b.get("type") == "para" and "Bài tập về nhà" in b.get("text", ""))]
    rf["blocks"] = giu + moi["reflection"]["blocks"]
    rf["teacher_note"] = moi["reflection"]["teacher_note"]
    st["review"]["teacher_note"] = ("Mở màn 8 phút. Chỉ hỏi ẩn là gì và thời gian hai xe chênh nhau bao nhiêu, chưa lập "
                                    "phương trình. Tình huống này chính là Bài 2 nên không chữa vội.")
    st["concept"]["teacher_note"] = ("Giảng 15 phút: đọc lại 3 bước SGK, công thức chuyển động, năng suất, làm chung và "
                                     "điều kiện của ẩn. Ba ví dụ mẫu nằm ở đầu từng mạch của Luyện tập 1.")

    loi = []
    nhan = []
    for s in f["stages"]:
        for b in s["blocks"]:
            nh = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, b.get("type")])[1]
            if b.get("type") == "problem":
                nhan.append((nh, b.get("level"), b.get("tier")))
                if nh in CHECK:
                    eq, ans = CHECK[nh]
                    b["check"] = {"kind": "solveset", "equation": eq, "answer": ans, "symbol": "x"}
                if DAP_SO.get(nh) and f"${DAP_SO[nh]}$" not in b.get("solution", ""):
                    loi.append(f"{nh}: lời giải không thấy đáp số ${DAP_SO[nh]}$")
                if b.get("level") == 1 and "hoàn thành bài giải" not in b.get("statement", ""):
                    loi.append(f"{nh}: NB thiếu 'hoàn thành bài giải'")
            if b.get("type") == "noted" and b.get("variant") == "example":
                if b["text"].count("[[fill:") < 2:
                    loi.append(f"{nh}: ví dụ ít ô fill")
            txt = json.dumps(b, ensure_ascii=False)
            for pat in CAM:
                for m in re.finditer(pat, txt):
                    loi.append(f"[{s['kind']}] {nh} /{pat}/: …{txt[max(0, m.start() - 40): m.end() + 30]}…")
            for k in ("statement", "solution", "text"):
                c = len(re.findall(r"(?<!\\);", b.get(k) or ""))
                if c:
                    loi.append(f"[{s['kind']}] {nh} {k}: {c} dấu ';'")
    print("bài:", nhan)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
