#!/usr/bin/env python3
"""THỐNG KÊ TẦN SUẤT DẠNG Ý trong đề thi thật của một chương — bước 2a của quy trình dựng bài.

Thầy 04/11/2026 (phiếu 2 ch.V 9C): *"Ví dụ 2 và bài 7 có phải là những bài hay thi … hướng đến
mục tiêu các bài vận dụng không nhỉ? … thêm 1 bước thống kê tỉ lệ các câu VD vào tab phân dạng
và ưu tiên bốc các bài đó"*.

Đầu vào: snapshot tab phân dạng (`inputs/refs/ngan-hang-sheet/<lop>/<mon>/chuong-NN.json`) và
luật dạng ý trong khung chương (`config/khung-phan-dang/<lop>-<mon>-chuong-NN.json`, khoá
`dang_y`: danh sách {ma, ten, re}; tuỳ chọn `ky_thuat` gắn tay cho một dạng).

Cách đếm (không suy diễn):
  1. Chỉ lấy câu có nguồn là ĐỀ THI THẬT (mã bắt đầu ck1/gk1/ck2/gk2/v10), bài tự luận nhiều ý.
  2. Gộp đề trùng nguyên văn (trường chép lại đề trường khác — ví dụ Hát Môn = Ái Mộ).
  3. Tách bài thành từng ý theo nhãn a), b), 1), c.i)…; mức của ý lấy ở cột "Mức độ từng ý".
  4. Gắn dạng cho ý bằng luật từ khoá của khung chương (một ý có thể mang hai dạng).
  5. Tần suất một dạng = số ĐỀ có ít nhất một ý dạng đó / số đề trong nhóm kỳ — tính riêng
     cho ý mức VD trở lên (đúng câu hỏi "dạng vận dụng hay thi") và cho mọi ý.
  6. Mỗi dòng của tab (cả SGK, sách tham khảo) được gắn dạng chính + tần suất để khi bốc câu
     ưu tiên dạng hay thi: T7 ("Dạng hay gặp trong đề thi thật") = 2 nếu ≥ 30%, 1 nếu 10–30%, 0 nếu < 10%.

Đây là phân loại TỰ ĐỘNG theo từ khoá trên đề đã chép tay từ ảnh (độ tin cậy cao hơn OCR);
dạng "tiếp tuyến" có thêm cột kỹ thuật gắn tay.

Dùng:
    .venv/bin/python scripts/thong_ke_dang_vd.py lop-9 hinh-hoc 5            # in báo cáo
    .venv/bin/python scripts/thong_ke_dang_vd.py lop-9 hinh-hoc 5 --json OUT # ghi JSON cho sheet
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DE_THI = ("ck1", "gk1", "ck2", "gk2", "v10")
NHOM_KY = {"Kì I (GK1 + CK1)": ("gk1", "ck1"), "Vào 10": ("v10",), "Kì II (GK2 + CK2)": ("gk2", "ck2")}
MUC = ("NB", "TH", "VD", "VDC")
_Y = re.compile(r"(?m)^\s*((?:[a-e]|[1-5])(?:\.(?:i{1,3}))?)\)\s*")


def tach_y(de: str, muc_y: str) -> list[tuple[str, str, str]]:
    """[(nhãn, mức, chữ của ý)] — bài không có nhãn ý thì cả bài là một ý."""
    muc = {}
    for m in re.finditer(r"([a-e1-5](?:\.i{1,3})?)\)\s*(NB|TH|VDC|VD)", muc_y or ""):
        muc[m.group(1)] = m.group(2)
    moc = list(_Y.finditer(de))
    if not moc:
        return [("", (muc_y or "").strip() if (muc_y or "").strip() in MUC else "", de)]
    out = []
    for i, m in enumerate(moc):
        nhan = m.group(1)
        chu = de[m.end(): moc[i + 1].start() if i + 1 < len(moc) else len(de)]
        out.append((nhan, muc.get(nhan, muc.get(nhan.split(".")[0], "")), chu))
    return out


_HOI = re.compile(r"(?:Chứng minh|chứng minh|Chứng tỏ|Tính|tính|Tìm|So sánh|Xác định|Hỏi)")


def phan_hoi(chu: str) -> str:
    """Phần CÂU HỎI của một ý (bỏ câu dựng hình phía trước: "Qua O kẻ đường thẳng vuông góc…")."""
    m = _HOI.search(chu)
    return chu[m.start():] if m else chu


def gan_dang(chu: str, luat: list[dict]) -> list[str]:
    hoi = phan_hoi(chu)
    return [l["ma"] for l in luat if re.search(l["re"], hoi, re.IGNORECASE)] or ["khac"]


_HU_TU = r"\b(điểm|đường|tròn|thẳng|hai|của|là|giao|gọi|lấy|kẻ|cho|tại|và|các|một|nhau|cắt|thuộc|sao)\b"


def gop_trung(rows: list[dict], nguong: float = 0.9) -> dict[str, str]:
    """mã → mã đại diện (đề trùng nguyên văn gộp về một)."""
    dai_dien: dict[str, str] = {}
    goc: list[dict] = []
    for r in rows:
        # so phần giả thiết + hai ý đầu: trường chép đề thường đổi ý cuối (Hát Môn = Ái Mộ trừ ý c)
        chuan = re.split(r"\n\s*(?:c|3)\)", r["de"])[0].lower()
        chuan = re.sub(r"[^\w]", "", re.sub(_HU_TU, " ", chuan))   # bỏ hư từ: "(O; R)" ≡ "đường tròn (O; R)"
        hit = next((g for g in goc if difflib.SequenceMatcher(None, g["_c"], chuan).ratio() >= nguong), None)
        if hit:
            dai_dien[r["ma"]] = hit["ma"]
        else:
            goc.append({**r, "_c": chuan})
            dai_dien[r["ma"]] = r["ma"]
    return dai_dien


def thong_ke(lop: str, mon: str, chuong: int) -> dict:
    khung = json.loads((ROOT / f"config/khung-phan-dang/{lop}-{mon}-chuong-{chuong:02d}.json").read_text("utf-8"))
    luat = khung["dang_y"]
    ten = {l["ma"]: l["ten"] for l in luat} | {"khac": "Khác"}
    ky_thuat = khung.get("ky_thuat", {})
    snap = json.loads((ROOT / f"inputs/refs/ngan-hang-sheet/{lop}/{mon}/chuong-{chuong:02d}.json").read_text("utf-8"))
    rows = snap["rows"]

    de = [r for r in rows if r["ma"].startswith(DE_THI) and len(tach_y(r["de"], r.get("muc_y", ""))) >= 2]
    dd = gop_trung(de)
    rieng = [r for r in de if dd[r["ma"]] == r["ma"]]

    # dạng của từng đề (đã gộp trùng): {mã: {"vd": set, "moi": set}}
    dang_de: dict[str, dict] = {}
    for r in rieng:
        vd, moi = set(), set()
        for _n, muc, chu in tach_y(r["de"], r.get("muc_y", "")):
            ds = gan_dang(chu, luat)
            moi.update(ds)
            if muc in ("VD", "VDC"):
                vd.update(ds)
        dang_de[r["ma"]] = {"vd": vd, "moi": moi}

    bang = []
    for nhom, tien_to in NHOM_KY.items():
        ma_nhom = [m for m in dang_de if m.startswith(tien_to)]
        n = len(ma_nhom)
        for l in luat + [{"ma": "khac"}]:
            k = l["ma"]
            co_moi = [m for m in ma_nhom if k in dang_de[m]["moi"]]
            co_vd = [m for m in ma_nhom if k in dang_de[m]["vd"]]
            bang.append({"nhom": nhom, "so_de": n, "dang": k, "ten": ten[k],
                         "de_co": len(co_moi), "pct": round(100 * len(co_moi) / n) if n else 0,
                         "de_co_vd": len(co_vd), "pct_vd": round(100 * len(co_vd) / n) if n else 0,
                         "vi_du": co_moi[:6]})

    # Tần suất để ưu tiên: nhóm kỳ mà chương được kiểm tra (khung `ky_thi`, mặc định Kì I)
    ky_chinh = khung.get("ky_thi", "Kì I (GK1 + CK1)")
    ten_ngan = {l["ma"]: l.get("ngan", l["ten"]) for l in luat}

    def pct(k: str) -> int:
        if k == "khac":
            return 0
        return next((b["pct"] for b in bang if b["dang"] == k and b["nhom"] == ky_chinh), 0)

    dong = []
    for r in rows:
        ys = tach_y(r["de"], r.get("muc_y", ""))
        y_out = []
        for nhan, muc, chu in ys:
            ds = [x for x in gan_dang(chu, luat) if x != "khac"]
            if not ds:
                continue
            ds = sorted(ds, key=pct, reverse=True)       # ý hỏi hai việc ⇒ ghi đủ hai dạng
            y_out.append({"y": nhan, "muc": muc, "dang": ds, "pct": pct(ds[0])})
        cao = max(y_out, key=lambda y: (MUC.index(y["muc"]) if y["muc"] in MUC else -1, y["pct"]), default=None)
        p = cao["pct"] if cao else None
        dong.append({"ma": r["ma"], "y": y_out,
                     "chu": " · ".join((f"{y['y']}) " if y["y"] else "")
                                       + " + ".join(f"{ten_ngan[k]} {pct(k)}%" for k in y["dang"]) for y in y_out),
                     "pct": p, "t7": None if p is None else (2 if p >= 30 else (1 if p >= 10 else 0)),
                     "ky_thuat": ky_thuat.get(r["ma"], "")})
    # Kỹ thuật (gắn tay trong khung) cho các đề có dạng được gắn kỹ thuật — đếm trên đề đã gộp trùng
    kt: dict[str, dict[str, list]] = {}
    for m, v in dang_de.items():
        if m in ky_thuat:
            nhom = next(n for n, tt in NHOM_KY.items() if m.startswith(tt))
            kt.setdefault(ky_thuat[m], {}).setdefault(nhom, []).append(m)
    return {"chuong": chuong, "so_de_rieng": len(rieng), "ky_thuat_dem": kt, "trung": {m: g for m, g in dd.items() if m != g},
            "bang": bang, "dong": dong, "ky_thuat_ten": khung.get("ky_thuat_ten", {})}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lop"); ap.add_argument("mon"); ap.add_argument("chuong", type=int)
    ap.add_argument("--json")
    a = ap.parse_args()
    kq = thong_ke(a.lop, a.mon, a.chuong)
    print(f"Đề thi thật nhiều ý (đã gộp trùng): {kq['so_de_rieng']} · gộp: {kq['trung']}")
    for nhom in NHOM_KY:
        b = [x for x in kq["bang"] if x["nhom"] == nhom]
        print(f"\n== {nhom} — {b[0]['so_de']} đề")
        for x in sorted(b, key=lambda x: -x["pct"]):
            print(f"  {x['pct']:3d}% ({x['de_co']:2d} đề) · ý VD+: {x['pct_vd']:3d}% ({x['de_co_vd']:2d}) · {x['ten']}")
    if kq["ky_thuat_dem"]:
        print("\n== Kỹ thuật (gắn tay)")
        for k, v in kq["ky_thuat_dem"].items():
            print(f"  {kq['ky_thuat_ten'].get(k, k)}: " + " · ".join(f"{n} {len(ms)} đề" for n, ms in v.items()))
    if a.json:
        Path(a.json).write_text(json.dumps(kq, ensure_ascii=False, indent=1), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
