#!/usr/bin/env python3
"""Áp kết quả việc Gemini "sửa bài phiếu" vào seed.

    python3 scripts/gemini/ap_sua_phieu.py <id-viec> [--ghi] [--soat-cong-thuc]

Đọc storage/gemini/xong/<id>.json, lấy danh sách {label, statement, solution}:
  - label "Bài N."    → thay statement + solution (+ hints nếu Gemini trả, không rỗng) của block problem cùng label;
  - label "Ví dụ N."  → thay trường text của block noted mở đầu \\textbf{Ví dụ N.} (solution bỏ qua).
Không có --ghi thì chỉ in diff để Claude soát. Label lạ / thiếu ⇒ dừng.
--soat-cong-thuc: việc chỉ dàn trang ⇒ so "nguyên tử công thức" trước/sau (bỏ cases, \\\\, ;),
in mọi khối lệch để soát bằng mắt (không chặn).
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def nguyen_tu(s: str) -> Counter:
    """Các mẩu công thức: $…$ bỏ cases/khoảng trắng, tách theo \\\\ và ;."""
    c = Counter()
    for m in re.findall(r"\$([^$]*)\$", s):
        m = re.sub(r"\\(?:begin|end)\{cases\}|\s+", "", m)
        for p in re.split(r"\\\\|;", m):
            p = p.strip(".,")
            if p:
                c[p] += 1
    return c


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    vid, ghi, soat = sys.argv[1], "--ghi" in sys.argv, "--soat-cong-thuc" in sys.argv
    hd = REPO / "storage/gemini/hang-doi"
    f = hd / f"{vid}.json.da-chay"
    viec = json.loads((f if f.exists() else hd / f"{vid}.json").read_text())
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    data = kq.get("ket_qua") or kq.get("json") or kq
    seed_p = REPO / viec["meta"]["seed"]
    seed = json.loads(seed_p.read_text())
    can_sua = set(viec["meta"]["labels"])

    khoi: dict[str, tuple[dict, list[str]]] = {}
    for s in seed["stages"]:
        for b in s.get("blocks", []):
            if b.get("type") == "problem":
                khoi[b["label"]] = (b, ["statement", "solution"])
            elif b.get("type") == "noted":
                m = re.match(r"\\textbf\{(Ví dụ \d+\.)\}", b.get("text", ""))
                if m and m.group(1) not in khoi:
                    khoi[m.group(1)] = (b, ["text"])

    nhan = {x["label"] for x in data["sua"]}
    if nhan - can_sua:
        print("Gemini sửa ngoài phạm vi:", sorted(nhan - can_sua)); return 1
    if can_sua - nhan:
        print("Gemini bỏ sót:", sorted(can_sua - nhan)); return 1

    lech = 0
    for x in data["sua"]:
        b, truong = khoi[x["label"]]
        moi = {"statement": x["statement"], "solution": x["solution"], "text": x["statement"]}
        for k in truong:
            cu = b.get(k, "")
            if cu == moi[k]:
                continue
            if soat:
                a, z = nguyen_tu(cu), nguyen_tu(moi[k])
                if a != z:
                    lech += 1
                    print(f"!!! {x['label']} {k}: công thức lệch  mất={dict(a - z)}  thêm={dict(z - a)}")
            else:
                print(f"--- {x['label']} {k}")
                for d in difflib.ndiff(cu.split("[[br]]"), moi[k].split("[[br]]")):
                    if d[0] in "+-":
                        print("  ", d)
            b[k] = moi[k]
        if x.get("hints") and b.get("type") == "problem" and x["hints"] != b.get("hints"):
            if not soat:
                print(f"--- {x['label']} hints")
                for h in x["hints"]:
                    print("   +", h)
            b["hints"] = x["hints"]
    if soat:
        print(f"Soát công thức: {lech} trường lệch / {len(data['sua'])} khối.")
    print("Ghi chú Gemini:", data.get("ghi_chu", ""))
    if ghi:
        seed_p.write_text(json.dumps(seed, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi", seed_p.relative_to(REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
