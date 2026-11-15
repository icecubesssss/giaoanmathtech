#!/usr/bin/env python3
"""Ráp 3 việc Gemini dung-9c-ch6-phieu-d-{lt,lop,btvn} thành seed phiếu D mới.

    python3 scripts/gemini/lap_dung_lai_phieu_d_9c.py          # soát
    python3 scripts/gemini/lap_dung_lai_phieu_d_9c.py --ghi    # ghi seed mới (slug mới), bỏ seed cũ

Seed cũ: …/phieu-d-luyen-khuon-cau-iii-3.json (có trong git HEAD). Seed mới đổi slug để tên PDF
không còn chữ "khuôn": Toan9C-Tinh-gia-tri-bieu-thuc-chua-hai-nghiem-Phieu-HS.pdf.
Soát: từ cấm, dấu ";", đáp số sơ đồ (SymPy) có mặt trong lời giải, ví dụ đủ ô fill, NB có chỗ chấm.
"""
import json
import re
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_phieu_d_9c import BAI, VI_DU, gia_tri  # noqa: E402
from viec_dung_lai_phieu_d_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

SEED_MOI = SEED.replace("phieu-d-luyen-khuon-cau-iii-3", "phieu-d-tinh-gia-tri-bieu-thuc-chua-hai-nghiem")
CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"điểm oan", r"mất \$0", r"tầng C", r"\bem\b", r"các em",
       r"[Hh]ôm nay", r"buổi này", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bép\b", r"Do đó", r"[Ss]uy ra", r"Như vậy",
       r"Mặt khác", r"\$S\s*=", r"\$P\s*=\s*x_1\s*x_2", r"mẹo", r"chìa khóa", r"có hai nghiệm phân biệt \$x_1"]
# "có hai nghiệm phân biệt $x_1" chỉ được phép ở hai đề thật (Bài 9, 10).
DE_THAT = {"Bài 9.", "Bài 10."}


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def latex_so(v):
    v = sp.nsimplify(v)
    if isinstance(v, sp.Rational) and v.q != 1:
        return rf"\dfrac{{{v.p}}}{{{v.q}}}"
    return str(v)


def dap_so():
    """nhãn → các đáp số cuối (chuỗi LaTeX) phải xuất hiện trong lời giải."""
    out = {}
    for nhan, muc, tier, nguon, abc0, y in BAI:
        ds = []
        for loai, abc, bt in y:
            if loai == "gt":
                ds.append(latex_so(gia_tri(abc or abc0, bt)))
        out[nhan] = ds
    for nhan, (abc, viec) in VI_DU.items():
        out[nhan] = [latex_so(gia_tri(abc, bt)) for loai, bt, _ in viec if loai == "gt"]
    return out


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:2000])
    p = REPO / SEED
    f = json.loads(p.read_text())
    f["slug"] = Path(SEED_MOI).stem
    f["title"] = "Tính giá trị biểu thức chứa hai nghiệm"
    f["eyebrow"] = "ĐẠI SỐ — CHƯƠNG VI · PHIẾU D"
    f["btvn_phieu_rieng"] = True
    st = {s["kind"]: s for s in f["stages"]}
    tn = lt["teacher_notes"]

    # Khám phá: opener + nhắc lại
    rv = st["review"]
    for b in rv["blocks"]:
        if b.get("type") == "opener":
            b["text"] = lt["opener_text"]
            b["tikz"] = (r"\begin{tikzpicture}[node distance=5mm and 6mm, font=\small]" "\n"
                         r"  \node[flownode](a){Định lí Viète\\$x_1+x_2$, $x_1x_2$};" "\n"
                         r"  \node[flownode,right=of a](b){Hạ bậc\\$x_1^2$, $x_1^3$ theo $x_1$};" "\n"
                         r"  \node[flowkey,right=of b](c){Giá trị\\của $Q$};" "\n"
                         r"  \draw[flowarrow](a)--(b);" "\n" r"  \draw[flowarrow](b)--(c);" "\n"
                         r"\end{tikzpicture}")
    cu_note = next(b["text"] for b in rv["blocks"] if b.get("type") == "noted")
    rv["blocks"] = [b for b in rv["blocks"] if b.get("type") == "opener"] + [
        {"type": "para", "text": r"\textbf{Nhắc lại kiến thức của Bài 20.}"},
        {"type": "noted", "variant": "note", "text": lt.get("review_note") or cu_note}]
    rv["teacher_note"] = tn["review"]
    # Kiến thức cần nhớ
    st["concept"]["blocks"] = lt["concept_blocks"]
    st["concept"]["teacher_note"] = tn["concept"]
    # Luyện tập
    moi = {s["kind"]: s for s in lop["stages"] + btvn["stages"]}
    for k in ("practice1", "practice2"):
        st[k]["title"] = moi[k]["title"]
        st[k]["blocks"] = moi[k]["blocks"]
        st[k]["teacher_note"] = tn[k]
    # Tổng kết: sơ đồ tư duy + tiêu đề BTVN + bài
    rf = st["reflection"]
    mm = dict(lt["mindmap"], type="mindmap")
    rf["blocks"] = [mm, {"type": "para", "text": r"\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."}] \
        + moi["reflection"]["blocks"]
    rf["teacher_note"] = tn.get("reflection") or (
        "Sơ đồ tư duy điền 5 phút cuối buổi. Bài tập về nhà gồm Bài 11 đến Bài 20, in thành phiếu riêng, "
        "khoảng 85 phút. Buổi sau chữa Bài 19 và Bài 20 trước.")

    ds = dap_so()
    loi, nhan_ds = [], []
    for s in f["stages"]:
        for b in s["blocks"]:
            nh = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, b.get("type")])[1]
            if b.get("type") == "problem":
                b.setdefault("writelines", 0)
                nhan_ds.append((nh, b.get("level"), b.get("tier")))
                for d in ds.get(nh, []):
                    if f"={d}" not in re.sub(r"\s", "", b.get("solution", "")):
                        loi.append(f"{nh}: lời giải không thấy đáp số ={d}")
                if b.get("level") == 1 and not re.search(r"\\ldots", b.get("statement", "")):
                    loi.append(f"{nh}: NB không có chỗ chấm")
                if b.get("level", 1) >= 2 and re.search(r"\\ldots|\[\[fill", b.get("statement", "")):
                    loi.append(f"{nh}: TH/VD có chỗ chấm (phải tự trình bày)")
            if b.get("type") == "noted" and b.get("variant") == "example":
                if b["text"].count("[[fill:") < 3:
                    loi.append(f"{nh}: ví dụ ít ô fill ({b['text'].count('[[fill:')})")
                for d in ds.get(nh, []):
                    if d not in b["text"]:
                        loi.append(f"{nh}: ví dụ không thấy đáp số {d}")
            txt = json.dumps(b, ensure_ascii=False)
            for pat in CAM:
                if nh in DE_THAT and "phân biệt" in pat:
                    continue
                for m in re.finditer(pat, txt):
                    loi.append(f"[{s['kind']}] {nh} /{pat}/: …{txt[max(0, m.start() - 50): m.end() + 30]}…")
            for k in ("statement", "solution", "text"):
                c = len(re.findall(r"(?<!\\);", b.get(k) or ""))
                if c:
                    loi.append(f"[{s['kind']}] {nh} {k}: {c} dấu ';'")
        for pat in CAM[:12]:
            if re.search(pat, s.get("teacher_note") or ""):
                loi.append(f"[{s['kind']}] teacher_note /{pat}/")
    print("bài:", nhan_ds)
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        q = REPO / SEED_MOI
        q.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED_MOI)
        if p != q and p.exists():
            p.unlink()
            print("đã bỏ seed cũ (còn trong git HEAD):", SEED)


if __name__ == "__main__":
    main()
