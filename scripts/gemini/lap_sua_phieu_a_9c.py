#!/usr/bin/env python3
"""Ráp 3 việc Gemini sua-9c-ch6-phieu-a-{lt,lop,btvn} vào seed phiếu A ch.VI 9C.

    python3 scripts/gemini/lap_sua_phieu_a_9c.py          # soát
    python3 scripts/gemini/lap_sua_phieu_a_9c.py --ghi    # ghi seed

CHỈ chạy trên seed CŨ (bản HEAD) — sau khi ghi, seed là nguồn sự thật, sửa tiếp bằng tay/việc khác.
Bản cũ lấy lại: git show HEAD:<SEED>.
Soát: từ cấm, dấu ";", $ lẻ, nghiệm nguyên của sơ đồ có mặt trong lời giải, ví dụ đủ ô fill, NB có chỗ chấm.
"""
import json
import re
import sys
from pathlib import Path

import sympy as sp

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_phieu_a_9c import SO_DO, chuan, x  # noqa: E402
from viec_sua_phieu_a_9c import SEED, VID_BTVN, VID_LOP, VID_LT  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"mất điểm", r"điểm oan", r"tầng C", r"\bem\b", r"các em",
       r"[Hh]ôm nay", r"buổi này", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"\bép\b", r"Do đó", r"[Ss]uy ra", r"Như vậy",
       r"Mặt khác", r"mẹo", r"chìa khóa", r"nhanh nhất", r"vừa khít", r"ăn may"]


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def nghiem_nguyen(nhan):
    out = []
    for vt, vp, loai, _ in SO_DO.get(nhan, (0, 0, 0, []))[3]:
        p = chuan(vt, vp)
        if p.degree() == 2:
            out += [int(r) for r in sp.solve(p.as_expr(), x) if r.is_integer]
    return out


def le_dola(s):
    return len(re.findall(r"(?<!\\)\$", s or "")) % 2


def soat(f):
    loi = []
    for s in f["stages"]:
        for b in s["blocks"]:
            nh = b.get("label") or (re.match(r"\\textbf\{([^}]*)\}", b.get("text", "")) or [0, b.get("type")])[1]
            if b.get("type") == "problem":
                sol = re.sub(r"\s", "", b.get("solution", ""))
                for r in nghiem_nguyen(nh):
                    if f"={r}" not in sol and f"{r}" not in sol:
                        loi.append(f"{nh}: lời giải không thấy nghiệm {r}")
                if b.get("level") == 1 and not re.search(r"\\ldots", b.get("statement", "")):
                    loi.append(f"{nh}: NB không có chỗ chấm")
                if b.get("level", 1) >= 2:
                    if re.search(r"\\ldots|\[\[fill", b.get("statement", "")):
                        loi.append(f"{nh}: TH/VD có chỗ chấm (phải tự trình bày)")
                    if not b.get("hints"):
                        loi.append(f"{nh}: TH/VD thiếu hints")
            if b.get("type") == "noted" and b.get("variant") == "example":
                n = b["text"].count("[[fill:")
                if n < 3:
                    loi.append(f"{nh}: ví dụ ít ô fill ({n})")
            for k in ("statement", "solution", "text"):
                v = b.get(k) or ""
                c = len(re.findall(r"(?<!\\);", v))
                if c:
                    loi.append(f"[{s['kind']}] {nh} {k}: {c} dấu ';'")
                for i, dong in enumerate(v.split("[[br]]")):
                    if le_dola(dong):
                        loi.append(f"[{s['kind']}] {nh} {k} dòng {i}: $ lẻ: {dong[:90]}")
            txt = json.dumps(b, ensure_ascii=False)
            for pat in CAM:
                for m in re.finditer(pat, txt):
                    loi.append(f"[{s['kind']}] {nh} /{pat}/: …{txt[max(0, m.start() - 50): m.end() + 30]}…")
        for pat in CAM:
            if re.search(pat, s.get("teacher_note") or ""):
                loi.append(f"[{s['kind']}] teacher_note /{pat}/")
    return loi


def main():
    lt, lop, btvn = lay(VID_LT), lay(VID_LOP), lay(VID_BTVN)
    for ten, g in (("lt", lt), ("lop", lop), ("btvn", btvn)):
        if g.get("ghi_chu"):
            print(f"ghi_chu [{ten}]:", g["ghi_chu"][:2000])
    p = REPO / SEED
    f = json.loads(p.read_text())
    f["btvn_phieu_rieng"] = True
    st = {s["kind"]: s for s in f["stages"]}
    tn = lt["teacher_notes"]

    rv = st["review"]
    op = next(b for b in rv["blocks"] if b.get("type") == "opener")
    op["text"] = lt["opener_text"]
    rv["blocks"] = [op, {"type": "para", "text": r"\textbf{Nhắc lại kiến thức Lớp 8.}"},
                    {"type": "noted", "variant": "note", "text": lt["review_note"]}]
    rv["teacher_note"] = tn["review"]
    st["concept"]["blocks"] = lt["concept_blocks"]
    st["concept"]["teacher_note"] = tn["concept"]
    moi = {s["kind"]: s for s in lop["stages"] + btvn["stages"]}
    for k in ("practice1", "practice2"):
        st[k]["title"] = moi[k]["title"]
        st[k]["blocks"] = moi[k]["blocks"]
        st[k]["teacher_note"] = tn[k]
    rf = st["reflection"]
    rf["blocks"] = [dict(lt["mindmap"], type="mindmap"),
                    {"type": "para", "text": r"\textbf{Bài tập về nhà} — làm vào vở, buổi sau nộp."}] \
        + moi["reflection"]["blocks"]
    rf["teacher_note"] = tn.get("reflection") or (
        "Sơ đồ tư duy điền 5 phút cuối buổi. Bài tập về nhà Bài 11–20 in thành phiếu riêng, khoảng 85 phút.")
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                b.setdefault("writelines", 0)

    loi = soat(f)
    print("bài:", [(b["label"], b.get("level"), b.get("tier")) for s in f["stages"] for b in s["blocks"]
                   if b.get("type") == "problem"])
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
