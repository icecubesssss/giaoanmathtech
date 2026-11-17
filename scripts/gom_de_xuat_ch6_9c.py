#!/usr/bin/env python3
"""Gom kết quả Gemini dx-ch6-9c-P1…P5 (cột ĐỀ XUẤT tab "Chọn câu Ch.VI lớp 9C").

Kiểm: đủ mọi mã của chon-cau.json, không thừa/thiếu; lí do ≤ ~25 chữ; dòng có Δ′ phải có
ly_do_cham_moi; ly_do_cham_moi không còn Δ′/b′.
    python3 scripts/gom_de_xuat_ch6_9c.py          (in thống kê + các dòng cần soát)
    python3 scripts/gom_de_xuat_ch6_9c.py --ghi    (ghi de-xuat.json cạnh chon-cau.json)
"""
import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GOC = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06"
XONG = REPO / "storage/gemini/xong"
PHAY = re.compile(r"Δ['′]|Delta'|\bb['′]|nghiệm thu gọn")


def main():
    rows = json.loads((GOC / "chon-cau.json").read_text())
    kq, loi = {}, []
    for p in ("P1", "P2", "P3", "P4", "P5"):
        f = XONG / f"dx-ch6-9c-{p}.json"
        if not f.exists():
            loi.append(f"thiếu kết quả {f.name}")
            continue
        for d in json.loads(f.read_text())["ket_qua"]["dong"]:
            if d["ma"] in kq:
                loi.append(f"mã lặp {d['ma']}")
            kq[d["ma"]] = d | {"phieu": p}
    out = []
    for r in rows:
        d = kq.get(r["ma"])
        if not d:
            loi.append(f"thiếu đề xuất: {r['phieu']} {r['ma']}")
            continue
        if d["phieu"] != r["phieu"]:
            loi.append(f"sai phiếu {r['ma']}")
        if len(d["ly_do"].split()) > 28:
            loi.append(f"lí do dài ({len(d['ly_do'].split())} chữ): {r['ma']}")
        if PHAY.search(r["ly_do"]) and not d["ly_do_cham_moi"].strip():
            loi.append(f"có Δ′ mà chưa viết lại lí do chấm: {r['ma']}")
        if PHAY.search(d["ly_do_cham_moi"]):
            loi.append(f"lí do chấm mới vẫn còn Δ′/b′: {r['ma']}")
        out.append({"ma": r["ma"], "phieu": r["phieu"], "vai": r["vai"], "de_xuat": d["de_xuat"],
                    "ly_do": d["ly_do"].strip(), "ly_do_cham_moi": d["ly_do_cham_moi"].strip(),
                    "nghi_ngo": d["nghi_ngo"].strip()})
    thua = set(kq) - {r["ma"] for r in rows}
    loi += [f"mã lạ: {m}" for m in sorted(thua)]
    dem = collections.Counter((o["phieu"], o["de_xuat"]) for o in out)
    for p in ("P1", "P2", "P3", "P4", "P5"):
        print(p, {k: dem[(p, k)] for k in ("Hay", "Cân nhắc", "Không hay")})
    print("Tổng:", collections.Counter(o["de_xuat"] for o in out))
    print("\n== Không hay / nghi ngờ / lí do chấm mới ==")
    for o in out:
        if o["de_xuat"] == "Không hay" or o["nghi_ngo"] or o["ly_do_cham_moi"]:
            print(f"[{o['phieu']} {o['vai']}] {o['ma']} — {o['de_xuat']}: {o['ly_do']}")
            if o["nghi_ngo"]:
                print("    NGHI NGỜ:", o["nghi_ngo"])
            if o["ly_do_cham_moi"]:
                print("    LÍ DO MỚI:", o["ly_do_cham_moi"])
    if loi:
        print("\nLỖI:\n  " + "\n  ".join(loi))
    if "--ghi" in sys.argv and not loi:
        (GOC / "de-xuat.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        print("Đã ghi", GOC / "de-xuat.json")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
