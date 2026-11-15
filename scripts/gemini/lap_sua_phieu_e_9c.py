#!/usr/bin/env python3
"""Áp 2 việc Gemini sua-9c-ch6-phieu-e-{a,b} vào phiếu E ch.VI 9C + phần máy móc (12/11/2026).

    python3 scripts/gemini/lap_sua_phieu_e_9c.py          # soát, in diff tóm tắt
    python3 scripts/gemini/lap_sua_phieu_e_9c.py --ghi    # ghi seed

Máy móc (Claude): `btvn_phieu_rieng: true`; xoá Bài 18 cũ (sắp thứ tự "bốn bước" — không phải SGK, BTVN dư 3 NB);
xoá 4 bảng đại lượng (sau Bài 3, 4, 20, 21 — ý nay là chỗ chấm, bảng GV kẻ lên bảng); xoá thẻ trap/target ở lý thuyết;
đổi tiêu đề "Nhắc lại hai thứ dùng suốt buổi hôm nay"; đánh lại số BTVN 19..34 → 18..33.
CHỈ chạy trên seed CHƯA áp (so khớp nhãn Bài 34 còn tồn tại).
"""
import difflib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_sua_phieu_e_9c import LABELS_A, LABELS_B, SEED, VID_A, VID_B, khoi  # noqa: E402

CAM = [r"[Kk]huôn", r"Câu III", r"thang điểm", r"điểm oan", r"0\{,\}25", r"lấy chắc", r"\bem\b", r"các em",
       r"[Hh]ôm nay", r"\bKiểm\b(?! tra)", r"\bSoi\b", r"Do đó", r"[Ss]uy ra", r"bốn bước", r"Bốn bước"]


def doc(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    return kq.get("ket_qua") or kq.get("json") or kq


def main():
    ghi = "--ghi" in sys.argv
    a, b = doc(VID_A), doc(VID_B)
    p = REPO / SEED
    f = json.loads(p.read_text())
    assert any(x.get("label") == "Bài 34." for s in f["stages"] for x in s["blocks"]), "seed đã áp rồi"
    st = {s["kind"]: s for s in f["stages"]}

    for vid, g, labels in ((VID_A, a, LABELS_A), (VID_B, b, LABELS_B)):
        nhan = [x["label"] for x in g["sua"]]
        if sorted(nhan) != sorted(labels):
            print(vid, "lệch nhãn: thiếu", sorted(set(labels) - set(nhan)), "thừa", sorted(set(nhan) - set(labels)))
            return 1
        if g.get("ghi_chu"):
            print(f"ghi_chu {vid}:", g["ghi_chu"])

    # 1. nội dung A ngoài bài
    rv = st["review"]["blocks"]
    assert rv[0]["type"] == "opener" and rv[2]["type"] == "noted"
    rv[0]["text"] = a["opener_text"]
    rv[1]["text"] = "\\textbf{Nhắc lại kiến thức đã học.}"
    rv[2]["text"] = a["review_note"]
    st["concept"]["blocks"] = a["concept_blocks"]
    mm = dict(a["mindmap"])
    mm["type"] = "mindmap"
    assert st["reflection"]["blocks"][0]["type"] == "mindmap"
    st["reflection"]["blocks"][0] = mm
    for k, v in a["teacher_notes"].items():
        st[k]["teacher_note"] = v

    # 2. bài + ví dụ
    kh = khoi(f)
    for x in a["sua"] + b["sua"]:
        bl = kh[x["label"]]
        if bl["type"] == "problem":
            for k in ("statement", "solution"):
                if bl.get(k, "") != x[k]:
                    print(f"--- {x['label']} {k}")
                    for d in difflib.ndiff(bl.get(k, "").split("[[br]]"), x[k].split("[[br]]")):
                        if d[0] in "+-":
                            print("  ", d)
                bl[k] = x[k]
            if x.get("hints"):
                bl["hints"] = x["hints"]
                print(f"    hints {x['label']}: {x['hints']}")
        else:
            print(f"--- {x['label']} (ví dụ mới)\n   ", x["statement"].replace("[[br]]", "\n    "))
            bl["text"] = x["statement"]

    # 3. máy móc
    f["btvn_phieu_rieng"] = True
    for s in f["stages"]:
        moi, bo_bang = [], False
        for bl in s["blocks"]:
            if bl.get("type") == "problem":
                bo_bang = bl["label"] in ("Bài 3.", "Bài 4.", "Bài 20.", "Bài 21.")
                if bl["label"] == "Bài 18.":
                    continue
            elif bl.get("type") == "table" and bo_bang:
                bo_bang = False
                continue
            moi.append(bl)
        s["blocks"] = moi
    doi = {}
    n = 0
    for s in f["stages"]:
        for bl in s["blocks"]:
            if bl.get("type") == "problem":
                n += 1
                doi[int(bl["label"][4:-1])] = n
                bl["label"] = f"Bài {n}."
    for s in f["stages"]:
        if s["kind"] not in ("practice1", "practice2", "reflection"):
            continue  # lý thuyết có thể nhắc "Bài 21" của SGK
        for bl in s["blocks"]:
            for k in ("statement", "solution", "text"):
                if isinstance(bl.get(k), str):
                    bl[k] = re.sub(r"Bài (\d+)(?![\d.]\d)", lambda m: f"Bài {doi.get(int(m.group(1)), m.group(1))}"
                                   if int(m.group(1)) >= 18 else m.group(0), bl[k])

    # 4. soát
    loi = []
    for s in f["stages"]:
        for bl in s["blocks"]:
            txt = json.dumps(bl, ensure_ascii=False)
            nhan = bl.get("label") or bl.get("type")
            for pat in CAM:
                for m in re.finditer(pat, txt):
                    loi.append(f"[{s['kind']}] {nhan} /{pat}/: …{txt[max(0, m.start() - 50): m.end() + 30]}…")
            for k in ("statement", "solution", "text"):
                c = len(re.findall(r"(?<!\\);", bl.get(k) or ""))
                if c:
                    loi.append(f"[{s['kind']}] {nhan} {k}: {c} dấu ';'")
        for pat in CAM:
            if re.search(pat, s.get("teacher_note", "")):
                loi.append(f"[{s['kind']}] teacher_note /{pat}/: {s['teacher_note'][:150]}")
    print("đổi số:", {k: v for k, v in doi.items() if k != v})
    for l in loi:
        print("✗", l)
    print("soát:", "SẠCH" if not loi else f"{len(loi)} chỗ cần xem")
    if ghi:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)
    return 0


if __name__ == "__main__":
    sys.exit(main())
