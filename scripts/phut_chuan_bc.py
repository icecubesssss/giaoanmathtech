#!/usr/bin/env python3
"""PHÚT THỰC HS B / HS C TỰ LÀM TỪNG BÀI của tab phân dạng — và phản biện rate card.

Thầy 04/11/2026: *"thống kê và chấm lại số phút chuẩn trung bình cho HS B và HS C xử lý các bài này
hết tầm bao nhiêu phút vào tab phân dạng và chia lại số phút cho hợp lý, cảm nhận là dạy k kịp …
bạn phản biện con số nhé?"*

Mô hình (tham số ở config/phut_thuc.json, có căn cứ):
    phút bài = đọc đề (số kí tự / tốc độ đọc)
             + vẽ hình (bài tự luận có hình: cơ bản + số điểm × phút/điểm)
             + Σ ý [ nghĩ(mức ý) + số dòng lời giải đi thi(dạng ý) × phút/dòng ]
    câu trắc nghiệm / Đúng-Sai / trả lời ngắn: đọc + phút/câu theo mức (Đ/S: mỗi khẳng định một câu).
Dạng ý lấy bằng chính luật của bước 2a (scripts/thong_ke_dang_vd.py).

Đối chiếu: giờ phòng thi CK1 Hà Nội 90′/10 điểm = 9′/điểm (điểm từng ý lấy ở inputs/refs/de-thi/lop-9/exams).

Dùng:
    .venv/bin/python scripts/phut_chuan_bc.py lop-9 hinh-hoc 5               # báo cáo + đối chiếu
    .venv/bin/python scripts/phut_chuan_bc.py lop-9 hinh-hoc 5 --json OUT    # phút từng mã cho sheet
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import thong_ke_dang_vd as tk  # noqa: E402

P = json.loads((ROOT / "config/phut_thuc.json").read_text("utf-8"))
_DIEM = re.compile(r"\b[A-Z]\b|(?<![A-Za-z])[A-Z](?=[\s,.;:)∈≠⊥∥=]|$)")


def so_diem_hinh(de: str) -> int:
    """Số điểm (chữ in hoa đứng riêng) xuất hiện trong đề — ước độ phức tạp của hình."""
    return len(set(re.findall(r"(?<![A-Za-zÀ-ỹ])([A-Z])(?![a-zà-ỹ])", de)) - {"R"})


def la_trac_nghiem(r: dict) -> bool:
    return any(k in (r.get("fmt") or "") for k in ("Trắc nghiệm", "Trả lời ngắn", "Điền", "Nối"))


def phut_bai(r: dict, tang: str, luat: list[dict]) -> dict:
    t = P["tang"][tang]
    de = r["de"]
    doc = len(de) / t["doc_ky_tu_phut"]
    ys = tk.tach_y(de, r.get("muc_y", ""))
    muc_bai = (r.get("band") or "TH")
    if la_trac_nghiem(r):
        n = max(1, len(ys)) if (r.get("fmt") or "").startswith("Trắc nghiệm đúng sai") else max(1, len(ys))
        y_ph = [t["trac_nghiem"].get(m or muc_bai, t["trac_nghiem"]["TH"]) for _n, m, _c in ys] or [t["trac_nghiem"][muc_bai]]
        tong = doc + sum(y_ph)
        return {"phut": round(tong), "doc": round(doc, 1), "ve": 0, "y": [round(x, 1) for x in y_ph]}
    co_hinh = "Chứng minh" in de or "chứng minh" in de
    ve = (t["ve_hinh_co_ban"] + t["ve_hinh_moi_diem"] * so_diem_hinh(de)) if co_hinh and so_diem_hinh(de) >= 4 else 0.0
    y_ph = []
    for _n, m, chu in ys:
        m = m or muc_bai
        ds = [x for x in tk.gan_dang(chu, luat) if x != "khac"] or ["khac"]
        dong = P["so_dong_NB"] if m == "NB" else sum(P["so_dong"][d] for d in ds[:2])
        y_ph.append(t["nghi"].get(m, t["nghi"]["TH"]) + dong * t["phut_moi_dong"])
    tong = doc + ve + sum(y_ph)
    return {"phut": round(tong), "doc": round(doc, 1), "ve": round(ve, 1), "y": [round(x, 1) for x in y_ph]}


def doi_chieu_de_thi(luat: list[dict], rows_by_ma: dict) -> list[dict]:
    """Mô hình B cho ý a, b (và c) bài hình CK1 so với giờ phòng thi (9′/điểm)."""
    out = []
    for f in sorted(glob.glob(str(ROOT / "inputs/refs/de-thi/lop-9/exams/ck1-*.json"))):
        d = json.loads(Path(f).read_text("utf-8"))
        x = d["xuat_xu"]
        ppd = (x.get("thoi_gian_phut") or 90) / (x.get("tong_diem") or 10)
        cau = [c for c in d["cau"] if c.get("chuong") == "C5" and re.search(r"[.-](IV|4)\.?2|IV2|42", c["id"])]
        if not cau:
            continue
        diem = sum(c.get("diem") or 0 for c in cau)
        ma = next((m for m in rows_by_ma if m.startswith(Path(f).stem) and any(k in m for k in ("IV2", "4.2", "42", "III2", "-7", "IV"))
                   and len(tk.tach_y(rows_by_ma[m]["de"], rows_by_ma[m].get("muc_y", ""))) >= 2), None)
        if not ma or diem < 2:          # đề chỉ trích được một ý thì không so được cả bài
            continue
        r = rows_by_ma[ma]
        b, c = phut_bai(r, "B", luat), phut_bai(r, "C", luat)
        out.append({"ma": ma, "diem": diem, "phut_thi": round(diem * ppd), "B": b["phut"], "C": c["phut"],
                    "B_ab": round(b["doc"] + b["ve"] + sum(b["y"][:2])), "C_ab": round(c["doc"] + c["ve"] + sum(c["y"][:2]))})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lop"); ap.add_argument("mon"); ap.add_argument("chuong", type=int)
    ap.add_argument("--json")
    a = ap.parse_args()
    khung = json.loads((ROOT / f"config/khung-phan-dang/{a.lop}-{a.mon}-chuong-{a.chuong:02d}.json").read_text("utf-8"))
    luat = khung["dang_y"]
    snap = json.loads((ROOT / f"inputs/refs/ngan-hang-sheet/{a.lop}/{a.mon}/chuong-{a.chuong:02d}.json").read_text("utf-8"))
    rows = snap["rows"]
    by = {r["ma"]: r for r in rows}
    kq = []
    for r in rows:
        b, c = phut_bai(r, "B", luat), phut_bai(r, "C", luat)
        try:
            g = float(str(r.get("phut") or "").replace(",", "."))
        except ValueError:
            g = None
        kq.append({"ma": r["ma"], "band": r.get("band"), "fmt": r.get("fmt"), "cu": g, "B": b["phut"], "C": c["phut"],
                   "chi_tiet_C": f"đọc {c['doc']}′ + vẽ {c['ve']}′ + ý " + " + ".join(f"{x}′" for x in c["y"])})
    dc = doi_chieu_de_thi(luat, by)
    print("== Đối chiếu giờ phòng thi CK1 (bài hình Câu IV.2, 9′/điểm)")
    for x in dc:
        print(f"  {x['ma']:32s} {x['diem']}đ → thi {x['phut_thi']}′ · B cả bài {x['B']}′ (a+b {x['B_ab']}′) · C cả bài {x['C']}′ (a+b {x['C_ab']}′)")
    if dc:
        print(f"  TRUNG VỊ: thi {st.median(x['phut_thi'] for x in dc)}′ · B {st.median(x['B'] for x in dc)}′ "
              f"(a+b {st.median(x['B_ab'] for x in dc)}′) · C {st.median(x['C'] for x in dc)}′ (a+b {st.median(x['C_ab'] for x in dc)}′)")
    for band in ("NB", "TH", "VD", "VDC"):
        xs = [x for x in kq if x["band"] == band and x["cu"]]
        if xs:
            print(f"  {band}: cột G cũ {st.median(x['cu'] for x in xs)}′ · B {st.median(x['B'] for x in xs)}′ · C {st.median(x['C'] for x in xs)}′  (n={len(xs)})")
    if a.json:
        Path(a.json).write_text(json.dumps({"bai": kq, "doi_chieu": dc}, ensure_ascii=False, indent=1), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
