#!/usr/bin/env python3
"""Gom kết quả Gemini phân dạng theo ý (chương VI Đại số 9) → kiểm → bảng ý + thống kê.

    .venv/bin/python scripts/gom_phan_dang_y.py [--lo 01,02] [--ghi]

Kiểm (CHẶN): thiếu câu, mã ngoài danh mục, mức ngoài NB/TH/VD/VDC.
Cảnh báo: mức khác mức gốc mà không ghi lý do; câu có ghi_chu phân vân (in ra để Claude soát).
--ghi ⇒ inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06/phan-dang-y.json
Thống kê % ĐỀ (không phải % câu): một đề = một nguồn "Ưu tiên 1" (trước dấu phẩy đầu của cột nguồn).
"""
import collections
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KHUNG = REPO / "config/khung-phan-dang/lop-9-dai-so-chuong-06.json"
BANK = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06.json"
XONG = REPO / "storage/gemini/xong"
OUT = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06/phan-dang-y.json"
TIEN_TO = "pd-y-ch6-9-"
MUC = ("NB", "TH", "VD", "VDC")


def ky_thi(ma: str) -> str:
    for tien, ten in (("so-hn", "Vào 10"), ("v10", "Vào 10"), ("ck2", "CK2"), ("gk2", "GK2"),
                      ("ck1", "CK1"), ("gk1", "GK1")):
        if ma.startswith(tien):
            return ten
    return ""


def de_id(r) -> str:
    return r["nguon"].split(",")[0].strip()


def doc_ket_qua(lo):
    kq = {}
    for p in sorted(XONG.glob(f"{TIEN_TO}*.json")):
        k = p.stem.removeprefix(TIEN_TO)
        if lo and k not in lo:
            continue
        obj = json.loads(p.read_text())
        data = obj.get("ket_qua") or obj.get("json") or obj.get("structured_output") or obj
        for c in data.get("cau", []):
            kq[c["ma"]] = c
    return kq


def main():
    lo = None
    if "--lo" in sys.argv:
        lo = set(sys.argv[sys.argv.index("--lo") + 1].split(","))
    dm = json.loads(KHUNG.read_text())["danh_muc_dang"]
    dang = {d["ma"]: d for d in dm["dang"]}
    rows = json.loads(BANK.read_text())["rows"]
    kq = doc_ket_qua(lo)
    can = [r for r in rows if not lo or r["ma"] in kq]
    loi, canh = [], []
    bang = []
    for r in can:
        c = kq.get(r["ma"])
        if not c:
            loi.append(f"thiếu câu {r['ma']}")
            continue
        if c.get("ghi_chu"):
            canh.append(f"{r['ma']}: {c['ghi_chu']}")
        for y in c["y"]:
            if y["ma_dang"] != "NGOAI" and y["ma_dang"] not in dang:
                loi.append(f"{r['ma']} {y['nhan']}: mã lạ {y['ma_dang']}")
                continue
            if y["muc"] not in MUC:
                loi.append(f"{r['ma']} {y['nhan']}: mức lạ {y['muc']}")
            d = dang.get(y["ma_dang"])
            if d and y["muc"] != d["muc_goc"] and not y.get("ly_do_muc"):
                canh.append(f"{r['ma']} {y['nhan']}: {y['ma_dang']} mức {y['muc']} ≠ gốc {d['muc_goc']} không lý do")
            bang.append({
                "ma_cau": r["ma"], "nhan": y["nhan"], "tom_tat": y["tom_tat"], "ma_dang": y["ma_dang"],
                "dang_gop": d.get("dang", "") if d else "NGOAI",
                "ten_dang": d["ten"] if d else "Ngoài chương VI", "nhom": d["ten_nhom"] if d else "Ngoài chương",
                "phieu_9c": d["phieu_9c"] if d else "", "muc": y["muc"], "bien_the": y.get("bien_the", ""),
                "ly_do_muc": y.get("ly_do_muc", ""), "nguon": r["nguon"], "uu": r["uu"], "ky_thi": ky_thi(r["ma"]),
                "de_id": de_id(r) if r["uu"].startswith("Ưu tiên 1") else "",
            })
    for x in loi:
        print("LỖI", x)
    for x in canh:
        print("cảnh báo", x)
    print(f"\n{len(kq)} câu → {len(bang)} ý; lỗi {len(loi)}, cảnh báo {len(canh)}")

    # Thống kê
    tong_de = {k: len({b["de_id"] for b in bang if b["de_id"] and b["ky_thi"] == k}) for k in ("Vào 10", "CK2", "GK2")}
    print("Số đề có câu chương VI:", tong_de)
    theo = collections.defaultdict(list)
    for b in bang:
        theo[b["ma_dang"]].append(b)
    print(f"\n{'mã':6} {'ý':>4} {'NB':>3} {'TH':>3} {'VD':>3} {'VDC':>3} {'%V10':>5} {'%CK2':>5} {'%GK2':>5}  tên")
    for ma in [d["ma"] for d in dm["dang"]] + ["NGOAI"]:
        ys = theo.get(ma, [])
        m = collections.Counter(y["muc"] for y in ys)
        pct = []
        for k in ("Vào 10", "CK2", "GK2"):
            n = len({y["de_id"] for y in ys if y["de_id"] and y["ky_thi"] == k})
            pct.append(f"{100 * n / tong_de[k]:4.0f}%" if tong_de[k] else "   -")
        ten = dang[ma]["ten"][:60] if ma in dang else "Ngoài chương VI"
        print(f"{ma:6} {len(ys):4} {m['NB']:3} {m['TH']:3} {m['VD']:3} {m['VDC']:3} {pct[0]:>5} {pct[1]:>5} {pct[2]:>5}  {ten}")

    print(f"\n{'nhóm':4} {'ý':>4} {'%V10':>5} {'%CK2':>5} {'%GK2':>5}  tên nhóm")
    for nh, ten in list(dm["nhom"].items()) + [("NGOAI", "Ngoài chương VI")]:
        ys = [b for b in bang if (dang[b["ma_dang"]]["nhom"] if b["ma_dang"] in dang else "NGOAI") == nh]
        pct = []
        for k in ("Vào 10", "CK2", "GK2"):
            n = len({y["de_id"] for y in ys if y["de_id"] and y["ky_thi"] == k})
            pct.append(f"{100 * n / tong_de[k]:4.0f}%" if tong_de[k] else "   -")
        print(f"{nh:4} {len(ys):4} {pct[0]:>5} {pct[1]:>5} {pct[2]:>5}  {ten}")

    print(f"\n{'dạng':6} {'ý':>4} {'NB':>3} {'TH':>3} {'VD':>3} {'VDC':>3} {'%V10':>5} {'%CK2':>5} {'%GK2':>5}  tên dạng (gộp)")
    for g in dm.get("dang_gop", []):
        ys = [b for b in bang if b["dang_gop"] == g["ma"]]
        m = collections.Counter(y["muc"] for y in ys)
        pct = []
        for k in ("Vào 10", "CK2", "GK2"):
            n = len({y["de_id"] for y in ys if y["de_id"] and y["ky_thi"] == k})
            pct.append(f"{100 * n / tong_de[k]:4.0f}%" if tong_de[k] else "   -")
        print(f"{g['ma']:6} {len(ys):4} {m['NB']:3} {m['TH']:3} {m['VD']:3} {m['VDC']:3} {pct[0]:>5} {pct[1]:>5} {pct[2]:>5}  {g['ten'][:60]}")

    if "--ghi" in sys.argv:
        if loi:
            sys.exit("Còn lỗi — không ghi.")
        OUT.write_text(json.dumps({"nguon": str(BANK.relative_to(REPO)), "tong_de": tong_de, "y": bang},
                                  ensure_ascii=False, indent=1) + "\n")
        print("Đã ghi", OUT.relative_to(REPO))


if __name__ == "__main__":
    main()
