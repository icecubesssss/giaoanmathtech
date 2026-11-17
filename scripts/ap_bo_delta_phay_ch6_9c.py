#!/usr/bin/env python3
"""Áp kết quả Gemini "bỏ Δ′" (Thầy 16/11/2026) vào hai script nguồn ch.VI 9C bản 2.

- scripts/tm_ch6_9c_ban2.py  ← storage/gemini/xong/tm-ch6-9c-bo-delta-phay.json (7 đoạn)
  + chèn "công thức nghiệm thu gọn Δ′" vào dòng "Không dạy ở lớp C".
- scripts/chon_cau_ch6_9c.py ← lí do chấm mới (storage/gemini/xong/dx-ch6-9c-P*.json),
  bỏ dòng sgk-b19-vd7 (đề bắt buộc dùng công thức nghiệm thu gọn).
Mỗi chuỗi cũ phải xuất hiện đúng một lần, không thì dừng.
    python3 scripts/ap_bo_delta_phay_ch6_9c.py        (thử, in số chỗ thay)
    python3 scripts/ap_bo_delta_phay_ch6_9c.py --ghi
"""
import glob
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TM = REPO / "scripts/tm_ch6_9c_ban2.py"
CC = REPO / "scripts/chon_cau_ch6_9c.py"
PHAY = re.compile(r"Δ['′]|\bb['′]")


def thay(src, cu, moi, ten):
    n = src.count(cu)
    if n != 1:
        sys.exit(f"[{ten}] chuỗi cũ xuất hiện {n} lần: {cu[:80]}")
    return src.replace(cu, moi)


def esc(s):  # chuỗi Python thường trong nguồn: \ viết thành \\
    return s.replace("\\", "\\\\")


def main():
    tm = TM.read_text()
    k = json.loads((REPO / "storage/gemini/xong/tm-ch6-9c-bo-delta-phay.json").read_text())["ket_qua"]
    for s in k["sua"]:
        cu, moi = esc(s["cu"]), esc(s["moi"])
        if moi:
            tm = thay(tm, f'"{cu}"', f'"{moi}"', s["khoa"])
        else:  # xoá cả phần tử danh sách (một dòng)
            tm = thay(tm, f'    "{cu}",\n', "", s["khoa"])
    cu = "giải phương trình bằng máy tính cầm tay, các dạng VDC."
    tm = thay(tm, cu, "giải phương trình bằng máy tính cầm tay, công thức nghiệm thu gọn "
              "$\\\\Delta'$ (Thầy bỏ 16/11/2026), các dạng VDC.", "Không dạy")

    cc = CC.read_text()
    moi = {}
    for f in glob.glob(str(REPO / "storage/gemini/xong/dx-ch6-9c-P*.json")):
        for d in json.loads(Path(f).read_text())["ket_qua"]["dong"]:
            if d["ly_do_cham_moi"].strip():
                moi[d["ma"]] = d["ly_do_cham_moi"].strip()
    dong = [l for l in cc.splitlines(keepends=True) if '"sgk-b19-vd7"' in l]
    if len(dong) != 1:
        sys.exit("không thấy đúng một dòng sgk-b19-vd7")
    cc = cc.replace(dong[0], "")
    for ma, ly in moi.items():
        if ma == "sgk-b19-vd7":
            continue
        m = re.search(r'^\(.*"' + re.escape(ma) + r'".*,"(.*)"\),\n', cc, re.M)
        if not m:
            sys.exit(f"không thấy dòng {ma}")
        cc = cc.replace(m.group(0), m.group(0).replace(f'"{m.group(1)}"),', f'"{ly}"),'))
    con = [l for l in cc.splitlines() if l.startswith('("') and PHAY.search(l)]
    print("TM: thay", len(k["sua"]), "đoạn + dòng Không dạy · chọn câu: bỏ vd7, thay lí do", len(moi) - 1, "dòng")
    if con:
        print("CÒN Δ′ trong chọn câu:\n  " + "\n  ".join(con))
    if "--ghi" in sys.argv:
        TM.write_text(tm)
        CC.write_text(cc)
        print("Đã ghi hai script.")


if __name__ == "__main__":
    main()
