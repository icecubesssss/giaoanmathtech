#!/usr/bin/env python3
"""Dựng dữ liệu các tab Sheets PHÂN DẠNG TIỂU HỌC (lớp 3, 4) từ bản ghi đã đọc ảnh.

Vào:
  inputs/refs/de-thi/tieu-hoc-nguon-tai.json                 (manifest tải đề, có link nguồn)
  inputs/refs/ngan-hang-sheet/tieu-hoc/lop-N/ban-ghi/*.json  (mỗi đề một tệp, mỗi ý một bản ghi)
  config/khung-phan-dang/tieu-hoc-lop-N-kntt.json            (mục lục KNTT = khung chủ đề/bài/kì)
Ra (mặc định ở outputs/ngan-hang-sheet/tieu-hoc/lop-N/):
  tab-de-thi.json · tab-phan-dang.json · tab-thong-ke-dang.json · tab-thong-ke-chu-de.json · tab-tien-do.json
  Mỗi tệp là mảng 2D gửi thẳng vào update_values (công thức locale en_US, dấu phẩy).

Dùng:
    .venv/bin/python scripts/tieu_hoc_phan_dang.py --lop 3
    .venv/bin/python scripts/tieu_hoc_phan_dang.py --lop 4 --kiem   # chỉ soát, không ghi
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "inputs/refs/de-thi/tieu-hoc-nguon-tai.json"
KY_TEN = {"gk1": "GK1", "ck1": "CK1", "gk2": "GK2", "ck2": "CK2"}
HT_TEN = {"TN": "Trắc nghiệm", "Điền": "Điền khuyết", "Đ-S": "Đúng sai", "TL": "Tự luận", "Nối": "Nối cột"}
TAB_TD = "'Tiến độ KNTT'"

# Lớp 4: ghi chú tiến độ TRUNG TÂM (sheet TIẾN ĐỘ C, tab "Tiến độ 4C", đọc 10/11/2026)
GHI_CHU_TT = {4: {8: "TT 4C: Bài 38–39 học trước CK1 nhưng đề CK1 của TT không có Chủ đề 8; Bài 40–48 học sau CK1; bỏ Bài 45"}}


def khong_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def ma_de(d: dict) -> str:
    t = khong_dau(d["truong"])
    t = re.sub(r"^(truong\s+)?(pho thong dtbt\s+)?(tieu hoc|th&thcs|th & thcs|th|xa|phuong)\s+", "", t)
    t = re.sub(r"\s*-\s*.*$", "", t)
    t = re.sub(r"\bi\b", "1", t)
    return f"l{d['lop']}-{d['ky']}-{str(d['nam_dau'])[2:]}{str(d['nam_dau'] + 1)[2:]}-{re.sub(r'[^a-z0-9]', '', t)}"


def link(url: str, nhan: str) -> str:
    return f'=HYPERLINK("{url}","{nhan}")' if url else ""


def dung(lop: int) -> dict[str, list[list]]:
    khung = json.loads((ROOT / f"config/khung-phan-dang/tieu-hoc-lop-{lop}-kntt.json").read_text(encoding="utf-8"))
    de_ds = [d for d in json.loads(MANIFEST.read_text(encoding="utf-8")) if d["lop"] == str(lop)]
    for d in de_ds:
        d["ma"] = d.get("ma") or ma_de(d)
    theo_ma = {d["ma"]: d for d in de_ds}
    ban_ghi = []
    for f in sorted((ROOT / f"inputs/refs/ngan-hang-sheet/tieu-hoc/lop-{lop}/ban-ghi").glob("*.json")):
        bg = json.loads(f.read_text(encoding="utf-8"))
        if bg["de"] not in theo_ma:
            sys.exit(f"✗ {f.name}: mã đề {bg['de']} không có trong manifest")
        ban_ghi.append(bg)

    # --- tab Tiến độ KNTT
    td = [["Chủ đề", "Tên chủ đề", "Bài", "Tên bài", "Học kì (SGK)", "Ghi chú tiến độ trung tâm"]]
    bai_hk = {}
    for c in khung["chu_de"]:
        for b in c["bai"]:
            td.append([c["so"], c["ten"], b["so"], b["ten"], c["hoc_ki_sgk"], GHI_CHU_TT.get(lop, {}).get(c["so"], "")])
            bai_hk[b["so"]] = (c["so"], c["hoc_ki_sgk"])

    # --- tab Phân dạng
    pd = [["Mã câu", "Mã đề", "Kì", "Câu", "Bài cụ thể (nguyên văn)", "Hình thức", "Điểm", "Mức độ",
           "Dạng bài", "Chủ đề", "Bài SGK", "Tên bài SGK", "Học kì của bài", "Hợp tiến độ KNTT",
           "Ghi chú tiến độ trung tâm", "Thực tế", "Có hình", "Đáp án", "Ghi chú", "Cần soát",
           "Đã soi ảnh", "Trường (tỉnh)", "Đề gốc", "Ưu tiên"]]
    loi = []
    for bg in ban_ghi:
        d = theo_ma[bg["de"]]
        for c in bg["cau"]:
            r = len(pd) + 1
            if c["bai"] and c["bai"] not in bai_hk:
                loi.append(f"{bg['de']} câu {c['cau']}: bài {c['bai']} không có trong khung")
            elif c["bai"] and bai_hk[c["bai"]][0] != c["cd"]:
                loi.append(f"{bg['de']} câu {c['cau']}: bài {c['bai']} thuộc CĐ{bai_hk[c['bai']][0]} chứ không phải CĐ{c['cd']}")
            pd.append([
                f"{bg['de']}-c{c['cau']}", bg["de"], KY_TEN[d["ky"]], c["cau"], c["nd"], HT_TEN.get(c["ht"], c["ht"]),
                c.get("diem", ""), c["muc"], c["dang"], c["cd"], c["bai"],
                f'=IF(K{r}=0,"(toán tư duy, không thuộc bài SGK)",XLOOKUP(K{r},{TAB_TD}!$C:$C,{TAB_TD}!$D:$D,"?"))',
                f'=IF(K{r}=0,"",XLOOKUP(K{r},{TAB_TD}!$C:$C,{TAB_TD}!$E:$E,"?"))',
                f'=IF(K{r}=0,"Tư duy, ngoài bài SGK",IF(OR(M{r}="Kì I",C{r}="GK2",C{r}="CK2"),"Đúng kì","Kiến thức kì sau"))',
                f'=IF(K{r}=0,"",XLOOKUP(K{r},{TAB_TD}!$C:$C,{TAB_TD}!$F:$F,""))',
                bool(c.get("thuc_te")), bool(c.get("hinh")), c["dap_an"], c.get("ghi_chu", ""),
                "Cần soát" if c.get("can_soat") else "", "Đã soi" if bg.get("da_soi_anh") else "Chưa",
                f"{d['truong']} ({d['tinh']})", link(d.get("url_trang") or d.get("url_thi_online", ""), "Ảnh đề gốc"),
                "Ưu tiên 1: Đề thi chính thức",
            ])
    n_pd = len(pd)

    # --- tab Thống kê dạng (chỉ đếm; mọi số là công thức trên tab Phân dạng)
    P = "'Phân dạng'"
    dang_dem = Counter(r[8] for r in pd[1:])
    dang_cd = {}
    for r in pd[1:]:
        dang_cd.setdefault(r[8], Counter())[r[9]] += 1
    tk = [["Kì đang xét", "CK1", "Gõ GK1, CK1, GK2 hoặc CK2 để đổi kì"],
          ["Số đề của kì đã bóc câu", f"=COUNTUNIQUEIFS({P}!$B$2:$B,{P}!$C$2:$C,$B$1)", ""],
          [],
          ["Dạng bài", "Chủ đề chính", "Số câu", "Số đề có dạng", "% đề có dạng", "Tổng điểm",
           "Điểm TB mỗi đề", "NB", "TH", "VD", "Câu kiến thức kì sau"]]
    for i, (dg, _) in enumerate(sorted(dang_dem.items(), key=lambda x: (-x[1], x[0]))):
        r = len(tk) + 1
        tk.append([dg, dang_cd[dg].most_common(1)[0][0],
                   f"=COUNTIFS({P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=COUNTUNIQUEIFS({P}!$B$2:$B,{P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=IF($B$2=0,0,D{r}/$B$2)",
                   f"=SUMIFS({P}!$G$2:$G,{P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=IF($B$2=0,0,F{r}/$B$2)",
                   f"=COUNTIFS({P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1,{P}!$H$2:$H,H$4)",
                   f"=COUNTIFS({P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1,{P}!$H$2:$H,I$4)",
                   f"=COUNTIFS({P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1,{P}!$H$2:$H,J$4)",
                   f'=COUNTIFS({P}!$I$2:$I,$A{r},{P}!$C$2:$C,$B$1,{P}!$N$2:$N,"Kiến thức kì sau")'])

    # --- tab Thống kê chủ đề
    tc = [["Kì đang xét", "CK1", "Gõ GK1, CK1, GK2 hoặc CK2 để đổi kì"],
          ["Số đề của kì đã bóc câu", f"=COUNTUNIQUEIFS({P}!$B$2:$B,{P}!$C$2:$C,$B$1)", ""],
          [],
          ["Chủ đề", "Tên chủ đề", "Học kì (SGK)", "Số câu", "Số đề có chủ đề", "% đề", "Tổng điểm", "Điểm TB mỗi đề"]]
    for c in [{"so": 0, "ten": "Toán tư duy (không thuộc bài SGK)", "hoc_ki_sgk": ""}] + khung["chu_de"]:
        r = len(tc) + 1
        tc.append([c["so"], c["ten"], c["hoc_ki_sgk"],
                   f"=COUNTIFS({P}!$J$2:$J,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=COUNTUNIQUEIFS({P}!$B$2:$B,{P}!$J$2:$J,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=IF($B$2=0,0,E{r}/$B$2)",
                   f"=SUMIFS({P}!$G$2:$G,{P}!$J$2:$J,$A{r},{P}!$C$2:$C,$B$1)",
                   f"=IF($B$2=0,0,G{r}/$B$2)"])

    # --- tab Đề thi và nguồn
    dt = [["Mã đề", "Kì", "Năm học", "Trường / đơn vị ra đề", "Tỉnh", "Số câu đã bóc", "Trạng thái",
           "Số trang ảnh", "Trang đề (ảnh chụp gốc)", "Bản gõ + đáp án (VietJack)", "PDF gốc",
           "File trong repo", "Ghi chú"]]
    co_bg = {bg["de"]: bg for bg in ban_ghi}
    thu_tu = {"ck1": 0, "gk1": 1, "gk2": 2, "ck2": 3}
    for d in sorted(de_ds, key=lambda x: (thu_tu[x["ky"]], x["ma"])):
        r = len(dt) + 1
        dt.append([d["ma"], KY_TEN[d["ky"]], d["nam_hoc"], d["truong"], d["tinh"],
                   f"=COUNTIF({P}!$B$2:$B,$A{r})",
                   f'=IF(F{r}>0,"Đã bóc câu","Chưa bóc câu")',
                   d.get("so_trang_anh", 0), link(d.get("url_trang", ""), "Mở trang đề"),
                   link(d.get("url_thi_online", ""), "Mở bản gõ"), link(d.get("url_pdf", ""), "Tải PDF"),
                   d.get("file", ""), (co_bg.get(d["ma"], {}).get("ghi_chu_de", "")
                                       or ("Chỉ có bản gõ, chưa có ảnh đề gốc" if not d.get("url_anh") else ""))])
    if loi:
        print("\n".join("✗ " + x for x in loi))
    print(f"lớp {lop}: {len(de_ds)} đề, {len(ban_ghi)} đề đã bóc, {n_pd - 1} câu, {len(dang_dem)} dạng")
    return {"tab-de-thi": dt, "tab-phan-dang": pd, "tab-thong-ke-dang": tk,
            "tab-thong-ke-chu-de": tc, "tab-tien-do": td, "_loi": loi}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", type=int, required=True, choices=[3, 4])
    ap.add_argument("--kiem", action="store_true")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    kq = dung(a.lop)
    if kq.pop("_loi"):
        return 1
    if not a.kiem:
        out = Path(a.out) if a.out else ROOT / f"outputs/ngan-hang-sheet/tieu-hoc/lop-{a.lop}"
        out.mkdir(parents=True, exist_ok=True)
        for k, v in kq.items():
            (out / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        print(f"✓ ghi {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
