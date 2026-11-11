#!/usr/bin/env python3
"""Soát tự động kết quả bóc đề của thợ Gemini + ghi bản ghi nháp cho Claude duyệt.

    python3 scripts/gemini/soat_boc_de.py --lop 7 --ky ck1 \
        --khung config/khung-phan-dang/lop-7-ck1-kntt.json

Đọc storage/gemini/xong/l<lop>-<ky>-*.json. Mỗi đề:
  • CỔNG CỨNG (đề hỏng, phải chạy lại/đọc tay): tổng điểm ≠ 10, đọc thiếu trang, nhãn trùng, 0 ý.
  • CỜ (Claude xem đúng ý đó trên ảnh): D99/mã lạ, can_soat, diem_uoc, "chọn 1 trong 2",
    TN không phải A–D, ý VDC > 1đ, ý > 2đ.
Ghi:
  inputs/refs/ngan-hang-sheet/lop-<lop>/<ky>/ban-ghi/<ma>.json   (nguon "gemini", da_soat false;
      KHÔNG ghi đè bản đã có da_soat true)
  storage/gemini/soat/<lop>-<ky>.md   (danh sách cần xem)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
XONG = REPO / "storage/gemini/xong"
HANG_DOI = REPO / "storage/gemini/hang-doi"


def so_trang(pdf: Path) -> int | None:
    try:
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        return int(re.search(r"Pages:\s+(\d+)", out).group(1))
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True)
    ap.add_argument("--ky", required=True)
    ap.add_argument("--khung", required=True)
    a = ap.parse_args()
    khung = json.loads((REPO / a.khung).read_text())
    dang = {d["ma"]: d for d in khung["dang"]}
    ra_bg = REPO / f"inputs/refs/ngan-hang-sheet/lop-{a.lop}/{a.ky}/ban-ghi"
    ra_bg.mkdir(parents=True, exist_ok=True)
    (REPO / "storage/gemini/soat").mkdir(parents=True, exist_ok=True)

    md, n_hong, n_co, n_y = [], 0, 0, 0
    for f in sorted(XONG.glob(f"l{a.lop}-{a.ky}-*.json")):
        r = json.loads(f.read_text())
        kq = r.get("ket_qua") or {}
        cau = kq.get("cau") or []
        viec_p = next((p for p in (HANG_DOI / f"{r['id']}.json", HANG_DOI / f"{r['id']}.json.da-chay") if p.exists()), None)
        meta = json.loads(viec_p.read_text()).get("meta", {}) if viec_p else {}
        pdf = REPO / meta.get("thu_muc", "") / meta.get("pdf", "")
        trang = so_trang(pdf) if meta else None

        hong, co = [], []
        tong = round(sum(float(q.get("diem") or 0) for q in cau), 2)
        if not cau:
            hong.append("0 ý")
        if abs(tong - 10) > 0.01:
            hong.append(f"tổng {tong}đ")
        if trang and (kq.get("so_trang_da_doc") or 0) < trang:
            hong.append(f"đọc {kq.get('so_trang_da_doc')}/{trang} trang")
        nhan = [q.get("cau") for q in cau]
        trung = sorted({x for x in nhan if nhan.count(x) > 1})
        if trung:
            hong.append(f"nhãn trùng {trung}")
        for q in cau:
            lydo = []
            if q.get("dang") not in dang or q.get("dang") == "D99":
                lydo.append(f"mã {q.get('dang')}")
            if q.get("can_soat"):
                lydo.append(f"thợ ghi: {q['can_soat']}")
            if q.get("dang") == "D23" and not re.search(r"tỉ lệ (thuận|nghịch)", q.get("nd", ""), re.I):
                lydo.append("D23 không nhắc tỉ lệ thuận/nghịch — có phải 'chia theo tỉ lệ' (giữ, chuyển D22)?")
            if q.get("diem_uoc") and q.get("ht") == "TL":
                lydo.append("điểm ước")
            if re.search(r"chọn\s*(1|một)", q.get("nd", ""), re.I):
                lydo.append("chọn 1 trong 2")
            if q.get("ht") == "TN" and not re.fullmatch(r"[A-D]", str(q.get("dap_an", "")).strip()):
                lydo.append(f"TN đáp án '{q.get('dap_an')}'")
            if q.get("muc") == "VDC" and float(q.get("diem") or 0) > 1:
                lydo.append("VDC > 1đ")
            if float(q.get("diem") or 0) > 2:
                lydo.append("ý > 2đ")
            if lydo:
                co.append(f"{q.get('cau')}: {'; '.join(lydo)}")
        n_hong += bool(hong)
        n_co += len(co)
        n_y += len(cau)

        # bản ghi nháp (cùng khuôn lớp 6) — không ghi đè bản Claude đã soát
        dich = ra_bg / f"{r['id']}.json"
        cu = json.loads(dich.read_text()) if dich.exists() else {}
        if not cu or (str(cu.get("nguon", "")).startswith("gemini") and not cu.get("da_soat")):
            bg = {
                "de": r["id"], "pdf": meta.get("pdf"), "thu_muc": meta.get("thu_muc"),
                "nam_hoc": "20" + r["id"].split("-")[2][:2] + "-20" + r["id"].split("-")[2][2:],
                "ghi_chu_de": kq.get("ghi_chu_de", ""), "tong_diem_ban_ghi": tong,
                "nguon": f"gemini:{r.get('model')}", "da_soat": False,
                "lech_kntt": "de-thi-lech-kntt" in meta.get("thu_muc", ""),
                "cau": [{**{k: q[k] for k in ("cau", "ht", "diem", "muc", "dang") if k in q},
                         "cd": dang.get(q.get("dang"), {}).get("cd"),
                         **{k: q[k] for k in ("nd", "dap_an", "diem_uoc", "co_hinh", "can_soat") if k in q}}
                        for q in cau],
            }
            dich.write_text(json.dumps(bg, ensure_ascii=False, indent=1) + "\n")

        uoc = sum(1 for q in cau if q.get("diem_uoc"))
        dong = (f"### {r['id']} — {len(cau)} ý, {tong}đ, trang {kq.get('so_trang_da_doc')}/{trang}"
                + (f", {uoc} ý điểm ước (đề không có HDC?)" if uoc else ""))
        md.append(dong + (" — **HỎNG: " + "; ".join(hong) + "**" if hong else ""))
        md += [f"- {c}" for c in co]
        md.append("")

    dau = [f"# Soát bóc đề lớp {a.lop} {a.ky.upper()} — {len(list(XONG.glob(f'l{a.lop}-{a.ky}-*.json')))} đề, "
           f"{n_y} ý, {n_hong} đề hỏng, {n_co} ý cần xem", ""]
    out = REPO / f"storage/gemini/soat/{a.lop}-{a.ky}.md"
    out.write_text("\n".join(dau + md) + "\n")
    print("\n".join(dau + md))
    print(f"Báo cáo: {out.relative_to(REPO)} · bản ghi nháp: {ra_bg.relative_to(REPO)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
