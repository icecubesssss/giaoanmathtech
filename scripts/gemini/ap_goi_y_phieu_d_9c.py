#!/usr/bin/env python3
"""Áp việc goi-y-9c-ch6-phieu-d (hints Polya) vào seed phiếu D.   [--ghi]"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_goi_y_phieu_d_9c import SEED, VID  # noqa: E402

CAM = [r"[Áá]p dụng", r"\bDùng\b", r"\bem\b", r"hãy", r";", r"\(x_1-\d\)\^2", r"x_1\^3\+x_2\^3"]


def main():
    kq = json.loads((REPO / "storage/gemini/xong" / f"{VID}.json").read_text())["ket_qua"]
    moi = {g["label"]: g["hints"] for g in kq["goi_y"]}
    p = REPO / SEED
    f = json.loads(p.read_text())
    loi = []
    for s in f["stages"]:
        for b in s["blocks"]:
            if b.get("type") == "problem" and b.get("level", 1) >= 2:
                h = moi.get(b["label"])
                if not h:
                    loi.append(f"thiếu {b['label']}")
                    continue
                for t in h:
                    for pat in CAM:
                        if re.search(pat, t):
                            loi.append(f"{b['label']} /{pat}/: {t}")
                b["hints"] = h
    print("\n".join(loi) or "soát gợi ý: SẠCH")
    if "--ghi" in sys.argv and not loi:
        p.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("đã ghi", SEED)


if __name__ == "__main__":
    main()
