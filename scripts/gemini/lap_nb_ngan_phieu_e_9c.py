#!/usr/bin/env python3
"""Áp việc nb-ngan-9c-ch6-phieu-e: thay chặng Luyện tập 1 + 2 bài NB của BTVN, đánh lại số bài.

    python3 scripts/gemini/lap_nb_ngan_phieu_e_9c.py [--ghi]
Chạy trên seed sau lượt "khuôn 3 bước" (BTVN đang có Bài 9, 10 là NB khung — bị thay).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_nb_ngan_phieu_e_9c import SEED, VID  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"chưa cần giải", r"\bem\b", r"[Hh]ôm nay", r"Do đó", r"[Ss]uy ra", r"mathbb"]


def main():
    kq = json.loads((REPO / "storage/gemini/xong" / f"{VID}.json").read_text())
    g = kq.get("ket_qua") or kq.get("json") or kq
    print("ghi_chu:", g.get("ghi_chu", "")[:2000])
    moi = {s["kind"]: s for s in g["stages"]}
    p = REPO / SEED
    f = json.loads(p.read_text())
    st = {s["kind"]: s for s in f["stages"]}
    st["practice1"]["blocks"] = moi["practice1"]["blocks"]
    st["practice1"]["teacher_note"] = moi["practice1"]["teacher_note"]
    rf = st["reflection"]["blocks"]
    cu_nb = [i for i, b in enumerate(rf) if b.get("type") == "problem" and b.get("level") == 1]
    assert len(cu_nb) == 2, cu_nb
    nb = [dict(b, tier="btvn", level=1) for b in moi["btvn_nb"]["blocks"]]
    st["reflection"]["blocks"] = rf[:cu_nb[0]] + nb + [b for i, b in enumerate(rf) if i > cu_nb[1]]
    n = 0
    ds = {}
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem":
                n += 1
                b["label"] = f"Bài {n}."
                ds.setdefault((s["kind"], b.get("tier"), b.get("level")), []).append(n)
    lt2 = ds[("practice2", "onclass", 2)] + ds[("practice2", "onclass", 3)]
    bt = [x for k, v in ds.items() if k[1] == "btvn" for x in v]
    bt_vd = ds[("reflection", "btvn", 3)]
    st["practice2"]["teacher_note"] = (
        f"Khoảng 60 phút. Bài {lt2[0]}–{lt2[2]} học sinh tự kẻ bảng và trình bày đủ 3 bước (mỗi bài khoảng 10 phút), "
        f"giáo viên chấm khâu bảng và phương trình trước. Bài {lt2[3]}, {lt2[4]} khoảng 15 phút mỗi bài. "
        f"Bài {lt2[4]} đề hỏi vận tốc lúc tăng tốc $x+6$ và câu hỏi phụ về giới hạn tốc độ.")
    st["reflection"]["teacher_note"] = (
        f"Sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà là Bài {min(bt)} đến Bài {max(bt)}, in thành phiếu riêng. "
        f"Buổi sau chữa Bài {bt_vd[0]} và Bài {bt_vd[1]} trước.")
    loi = []
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") != "problem":
                continue
            t = b["statement"] + b.get("solution", "")
            loi += [f"{b['label']} /{c}/" for c in CAM if re.search(c, t)]
            if len(re.findall(r"(?<!\\);", t)):
                loi.append(f"{b['label']} có ';'")
            if b.get("level") == 1 and b["statement"].count("[NB]") > 2:
                loi.append(f"{b['label']} NB > 2 thẻ")
    print("bài:", {f"{k[0]}/{k[1]}/{k[2]}": v for k, v in ds.items()})
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ")
    if "--ghi" in sys.argv:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi")


if __name__ == "__main__":
    main()
