#!/usr/bin/env python3
"""Chấm bài chạy thử của thợ Gemini (bóc đề CK1 Toán 6) so với bản ghi chuẩn.

    python3 scripts/gemini/cham_ck1_lop6.py            # chấm mọi việc trong storage/gemini/xong/
    python3 scripts/gemini/cham_ck1_lop6.py --chi-tiet # in từng ý lệch

Tiêu chí (Thầy chốt ngưỡng ~90% trước khi xây hệ thật):
  phủ ý      — ý của bản chuẩn mà thợ có ghi (khớp nhãn)          ≥ 95%
  tổng 10đ   — tổng điểm thợ ghi = 10                             mọi đề
  điểm ý     — điểm khớp (bỏ qua ý bản chuẩn ghi diem_uoc)          ≥ 90%
  dạng       — mã D khớp                                          ≥ 90%
  mức        — NB/TH/VD/VDC khớp                                  (tham khảo, ≥ 75%)
  đáp án TN  — chữ cái khớp                                       ≥ 95%
Báo cáo ghi ra storage/gemini/cham/ck1-lop6.md (+ .json).
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BAN_GHI = REPO / "inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi"
XONG = REPO / "storage/gemini/xong"
LOI = REPO / "storage/gemini/loi"
RA = REPO / "storage/gemini/cham"
NGUONG = {"phu": 0.95, "diem": 0.90, "dang": 0.90, "muc": 0.75, "tn": 0.95}


def nhan(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s)).upper()
    s = re.sub(r"^(CÂU|BÀI|CAU|BAI)\s*", "", s)
    s = re.sub(r"(PHẦN|PHAN)\s*", "", s)
    return re.sub(r"[\s.)(:]", "", s)


def ty_le(a: int, b: int) -> float | None:
    return a / b if b else None


def pct(x: float | None) -> str:
    return "—" if x is None else f"{x*100:.0f}%"


def cham_de(chuan: dict, tho: dict) -> dict:
    c_map = {nhan(q["cau"]): q for q in chuan["cau"]}
    t_list = tho.get("cau") or []
    t_map = {}
    for q in t_list:
        t_map.setdefault(nhan(q.get("cau", "")), q)
    chung = [k for k in c_map if k in t_map]
    thieu = [c_map[k]["cau"] for k in c_map if k not in t_map]
    thua = [t_map[k].get("cau") for k in t_map if k not in c_map]
    dem = Counter()
    lech = []
    for k in chung:
        c, t = c_map[k], t_map[k]
        if not c.get("diem_uoc"):
            dem["diem_n"] += 1
            if abs(float(t.get("diem", -1)) - c["diem"]) < 1e-6:
                dem["diem_ok"] += 1
            else:
                lech.append((c["cau"], "điểm", c["diem"], t.get("diem")))
        dem["dang_n"] += 1
        if t.get("dang") == c["dang"]:
            dem["dang_ok"] += 1
        else:
            lech.append((c["cau"], "dạng", c["dang"], t.get("dang")))
        dem["muc_n"] += 1
        if t.get("muc") == c["muc"]:
            dem["muc_ok"] += 1
        else:
            lech.append((c["cau"], "mức", c["muc"], t.get("muc")))
        if c["ht"] == "TN" and re.fullmatch(r"[A-D]", str(c.get("dap_an", "")).strip()):
            dem["tn_n"] += 1
            ta = str(t.get("dap_an", "")).strip().upper()[:1]
            if ta == c["dap_an"].strip():
                dem["tn_ok"] += 1
            else:
                lech.append((c["cau"], "đáp án TN", c["dap_an"], t.get("dap_an")))
    tong = round(sum(float(q.get("diem", 0) or 0) for q in t_list), 2)
    return {
        "de": chuan["de"], "so_y_chuan": len(c_map), "so_y_tho": len(t_list),
        "phu": ty_le(len(chung), len(c_map)), "thieu": thieu, "thua": thua,
        "tong_diem_tho": tong, "tong_ok": abs(tong - 10) < 0.01,
        "diem": ty_le(dem["diem_ok"], dem["diem_n"]),
        "dang": ty_le(dem["dang_ok"], dem["dang_n"]),
        "muc": ty_le(dem["muc_ok"], dem["muc_n"]),
        "tn": ty_le(dem["tn_ok"], dem["tn_n"]),
        "dem": dict(dem), "lech": lech,
        "so_trang_da_doc": tho.get("so_trang_da_doc"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi-tiet", action="store_true")
    a = ap.parse_args()
    RA.mkdir(parents=True, exist_ok=True)
    chuan = {json.loads(f.read_text())["de"]: json.loads(f.read_text()) for f in BAN_GHI.glob("*.json")}
    kq, meta = [], {}
    for f in sorted(XONG.glob("*.json")):
        r = json.loads(f.read_text())
        if r["id"] not in chuan or not isinstance(r.get("ket_qua"), dict):
            continue
        kq.append(cham_de(chuan[r["id"]], r["ket_qua"]))
        meta[r["id"]] = {"model": r.get("model"), "giay": r.get("giay")}
    loi = sorted(p.stem for p in LOI.glob("*.json")) if LOI.exists() else []
    if not kq:
        print("Chưa có bài nào trong storage/gemini/xong/." + (f" Lỗi: {loi}" if loi else ""))
        return 1

    tong = Counter()
    for r in kq:
        for k, v in r["dem"].items():
            tong[k] += v
    phu_n = sum(r["so_y_chuan"] for r in kq)
    phu_ok = sum(r["so_y_chuan"] - len(r["thieu"]) for r in kq)
    toan = {
        "phu": ty_le(phu_ok, phu_n),
        "diem": ty_le(tong["diem_ok"], tong["diem_n"]),
        "dang": ty_le(tong["dang_ok"], tong["dang_n"]),
        "muc": ty_le(tong["muc_ok"], tong["muc_n"]),
        "tn": ty_le(tong["tn_ok"], tong["tn_n"]),
    }
    tong10 = sum(r["tong_ok"] for r in kq)
    dat = all((toan[k] or 0) >= v for k, v in NGUONG.items() if k != "muc") and tong10 == len(kq)

    md = [f"# Chấm thợ Gemini — bóc đề CK1 Toán 6 ({len(kq)} đề, lỗi {len(loi)})", ""]
    md.append(f"Model: {sorted({m['model'] for m in meta.values()})} · tổng thời gian {sum(m['giay'] or 0 for m in meta.values()):.0f}s")
    md.append("")
    md.append("| Tiêu chí | Kết quả | Ngưỡng |")
    md.append("|---|---|---|")
    ten = {"phu": "Phủ ý", "diem": "Điểm ý", "dang": "Dạng", "muc": "Mức", "tn": "Đáp án TN"}
    for k in ten:
        md.append(f"| {ten[k]} | {pct(toan[k])} | {pct(NGUONG[k])} |")
    md.append(f"| Tổng = 10đ | {tong10}/{len(kq)} đề | mọi đề |")
    md.append("")
    md.append(f"**KẾT LUẬN: {'ĐẠT — có thể xây hệ' if dat else 'CHƯA ĐẠT'}**")
    md.append("")
    md.append("| Đề | ý chuẩn/thợ | phủ | tổng | điểm | dạng | mức | TN | trang |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for r in kq:
        md.append(f"| {r['de']} | {r['so_y_chuan']}/{r['so_y_tho']} | {pct(r['phu'])} | {r['tong_diem_tho']} | "
                  f"{pct(r['diem'])} | {pct(r['dang'])} | {pct(r['muc'])} | {pct(r['tn'])} | {r['so_trang_da_doc']} |")
    if loi:
        md += ["", f"Việc lỗi (xem storage/gemini/loi/): {', '.join(loi)}"]
    md += ["", "## Ý lệch"]
    for r in kq:
        if r["thieu"] or r["thua"] or r["lech"]:
            md.append(f"\n**{r['de']}**")
            if r["thieu"]:
                md.append(f"- thiếu: {', '.join(r['thieu'])}")
            if r["thua"]:
                md.append(f"- thừa: {', '.join(map(str, r['thua']))}")
            for cau, loai, c, t in r["lech"]:
                md.append(f"- {cau} {loai}: chuẩn {c} · thợ {t}")
    (RA / "ck1-lop6.md").write_text("\n".join(md) + "\n")
    (RA / "ck1-lop6.json").write_text(json.dumps({"toan": toan, "de": kq, "loi": loi}, ensure_ascii=False, indent=1))
    in_ra = md if a.chi_tiet else md[: md.index("## Ý lệch")]
    print("\n".join(in_ra))
    print(f"\nBáo cáo: {(RA / 'ck1-lop6.md').relative_to(REPO)}")
    return 0 if dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
