#!/usr/bin/env python3
"""PHÂN DẠNG ĐỀ CUỐI HỌC KÌ I TOÁN 7 (Hà Nội, 2024-2025 + 2025-2026, KNTT) → .xlsx để tải lên Google Sheets.

Khuôn: scripts/lop6_ck1_phan_dang.py. Khác lớp 6:
  - bản ghi do Gemini bóc, Claude soát theo nhóm cờ (trường `nguon`, `da_soat`, `can_soat`);
  - 19/30 đề LỆCH KNTT (ra thêm Ch.VI đại lượng tỉ lệ / Ch.X hình khối) — vẫn thống kê, cột "Lệch KNTT";
  - ý ngoài phạm vi CK1 của trung tâm gắn `ngoai_pham_vi` (D23 tỉ lệ thuận/nghịch, D24 hình khối, D99 Ch.IX):
    tab "Thống kê dạng" có cả hai thước đo (mọi ý / chỉ ý trong phạm vi).

Vào:  config/khung-phan-dang/lop-7-ck1-kntt.json
      inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi/*.json
Ra:   outputs/ngan-hang-sheet/lop-7/ck1/Phan-dang-CK1-Toan7-Ha-Noi.xlsx

    .venv/bin/python scripts/lop7_ck1_phan_dang.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import lop6_ck1_phan_dang as L6  # noqa: E402
from de_ck1_lop7 import TEN_TRUONG  # noqa: E402

KHUNG = ROOT / "config/khung-phan-dang/lop-7-ck1-kntt.json"
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-7/ck1/ban-ghi"
OUT = ROOT / "outputs/ngan-hang-sheet/lop-7/ck1/Phan-dang-CK1-Toan7-Ha-Noi.xlsx"
HT, MUC = L6.HT, L6.MUC


def truong(d):
    k = d["de"].split("-")[-1]
    return TEN_TRUONG.get(k, k).replace("\\&", "&")


def doc():
    khung = json.loads(KHUNG.read_text(encoding="utf-8"))
    des = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(BG.glob("l7-ck1-*.json"))]
    loi = []
    ma = {d["ma"] for d in khung["dang"]} | {"D99"}
    for d in des:
        t = round(sum(c["diem"] for c in d["cau"]), 2)
        if t != 10:
            loi.append(f"{d['de']}: tổng {t}")
        for c in d["cau"]:
            if c["dang"] not in ma:
                loi.append(f"{d['de']} {c['cau']}: dạng {c['dang']}")
            if c["muc"] not in MUC:
                loi.append(f"{d['de']} {c['cau']}: mức {c['muc']}")
    return khung, des, loi


def bang(khung, des):
    N = len(des)
    ten_dang = {d["ma"]: d["ten"] for d in khung["dang"]}
    ten_dang["D99"] = "Ngoài khung (Ch.IX quan hệ trong tam giác…)"
    cd_dang = {d["ma"]: d["cd"] for d in khung["dang"]}
    ten_cd = {c["so"]: c["ten"] for c in khung["chuong"]}
    url = lambda d: f"https://thcs.toanmath.com/thcs-pdf/{d['pdf'][:-4]}.pdf"
    ngoai = lambda c: bool(c.get("ngoai_pham_vi"))

    dt = [["Mã đề", "Năm học", "Trường / đơn vị ra đề", "Lệch KNTT", "Cấu trúc đề", "Số ý đã bóc",
           "Số ý ngoài phạm vi", "Đề gốc (toanmath)", "File PDF trong repo", "Ghi chú"]]
    pd = [["Mã câu", "Mã đề", "Năm học", "Trường", "Câu", "Nội dung tóm tắt", "Hình thức", "Điểm", "Mức độ",
           "Mã dạng", "Dạng bài", "Chương", "Đáp án", "Có hình", "Điểm là ước tính", "Ngoài phạm vi CK1 trung tâm",
           "Cần soát / ghi chú soát", "Đề gốc"]]
    for d in des:
        lk = f'=HYPERLINK("{url(d)}","Mở đề gốc")'
        tn = sum(c["diem"] for c in d["cau"] if c["ht"] != "TL")
        dt.append([d["de"], d["nam_hoc"], truong(d), "Lệch" if d.get("lech_kntt") else "",
                   "Thuần tự luận" if tn == 0 else f"TN {tn:g}đ + TL {10 - tn:g}đ", len(d["cau"]),
                   sum(ngoai(c) for c in d["cau"]), lk, f"{d['thu_muc']}/{d['pdf']}", d.get("ghi_chu_de", "")])
        for c in d["cau"]:
            cs = c.get("can_soat") or ""
            cs = "Cần soát" if cs is True else cs
            if c.get("ghi_chu_soat"):
                cs = (cs + "; " if cs else "") + c["ghi_chu_soat"]
            pd.append([f"{d['de']}-{c['cau']}", d["de"], d["nam_hoc"], truong(d), c["cau"],
                       c["nd"].replace("\\\\", "\\"), HT.get(c["ht"], c["ht"]), c["diem"], c["muc"], c["dang"],
                       ten_dang.get(c["dang"], ""), c["cd"], c.get("dap_an", ""), "Có" if c.get("co_hinh") else "",
                       "Ước" if c.get("diem_uoc") else "", "Ngoài" if ngoai(c) else "", cs, lk])

    co, co_pv, diem, so_y = Counter(), Counter(), Counter(), Counter()
    muc, vi_du, co_nam = defaultdict(Counter), defaultdict(list), defaultdict(Counter)
    nam = Counter(d["nam_hoc"] for d in des)
    for d in des:
        for c in d["cau"]:
            diem[c["dang"]] += c["diem"]; so_y[c["dang"]] += 1; muc[c["dang"]][c["muc"]] += 1
            if len(vi_du[c["dang"]]) < 3:
                vi_du[c["dang"]].append(f"{truong(d)} {c['cau']}")
        for k in {c["dang"] for c in d["cau"]}:
            co[k] += 1; co_nam[k][d["nam_hoc"]] += 1
        for k in {c["dang"] for c in d["cau"] if not ngoai(c)}:
            co_pv[k] += 1
    tk = [["Số đề", N, "Đề CK1 Toán 7 Hà Nội: " + "; ".join(f"{v} đề {k}" for k, v in sorted(nam.items(), reverse=True))
           + f" — {sum(1 for d in des if d.get('lech_kntt'))} đề lệch KNTT (ra thêm đại lượng tỉ lệ / hình khối)"], [],
          ["Mã dạng", "Dạng bài", "Chương", "Số đề có dạng", "% đề có dạng", "% đề (chỉ ý trong phạm vi)", "Số ý",
           "Điểm TB mỗi đề", "NB", "TH", "VD", "VDC", "Bậc tần suất", "Trong phạm vi CK1 trung tâm",
           "Ví dụ (trường – câu)", "% đề 2025-2026", "% đề 2024-2025"]]
    loai = khung.get("pham_vi_ck1", {}).get("loai", {})
    for k in sorted(ten_dang, key=lambda k: (-co[k], -diem[k])):
        if not co[k]:
            continue
        p = co_pv[k] / N
        bac = "Top 1 (≥ 80%)" if p >= .8 else "Top 2 (40–79%)" if p >= .4 else "Ít gặp (20–39%)" if p >= .2 else "Hiếm (< 20%)"
        pv = "Không — " + loai[k].split("—")[1].split(";")[0].strip() if k in loai else ("Không" if k == "D99" else "Có")
        tk.append([k, ten_dang[k], cd_dang.get(k, ""), co[k], round(co[k] / N, 3), round(p, 3), so_y[k],
                   round(diem[k] / N, 2), *[muc[k][m] for m in MUC], bac, pv, "; ".join(vi_du[k]),
                   round(co_nam[k]["2025-2026"] / max(nam["2025-2026"], 1), 3),
                   round(co_nam[k]["2024-2025"] / max(nam["2024-2025"], 1), 3)])

    cdd, cdco, md = Counter(), Counter(), Counter()
    for d in des:
        for c in d["cau"]:
            cdd[c["cd"]] += c["diem"]; md[c["muc"]] += c["diem"]
        for k in {c["cd"] for c in d["cau"]}:
            cdco[k] += 1
    tc = [["Chương", "Tên chương", "Số đề có chương", "% đề", "Điểm TB mỗi đề", "% điểm"]]
    for s in sorted(cdd, key=lambda s: (s == 0, s)):
        tc.append([s, ten_cd.get(s, "Vận dụng cao tổng hợp" if s == 0 else ""), cdco[s], round(cdco[s] / N, 3),
                   round(cdd[s] / N, 2), round(cdd[s] / N / 10, 3)])
    tc += [[], ["Mức độ", "", "", "", "Điểm TB mỗi đề", "% điểm"]]
    for m in MUC:
        tc.append([m, "", "", "", round(md[m] / N, 2), round(md[m] / N / 10, 3)])

    kh = [["Cấu trúc", "Số đề", "Các đề"]]
    nhom = defaultdict(list)
    for d in des:
        tn = sum(c["diem"] for c in d["cau"] if c["ht"] != "TL")
        nhom["Thuần tự luận" if tn == 0 else f"Trắc nghiệm {tn:g}đ + tự luận {10 - tn:g}đ"].append(truong(d) + f" ({d['nam_hoc']})")
    for k, v in sorted(nhom.items(), key=lambda x: -len(x[1])):
        kh.append([k, len(v), "; ".join(v)])
    tl = lambda ks: sum(1 for d in des if any(c["dang"] in ks and c["ht"] == "TL" for c in d["cau"]))
    kh += [[], ["KHUNG ĐỀ TRUNG TÂM chốt từ dữ liệu (bộ 3 ôn + 3 chính thức)", "Điểm", "Căn cứ"],
           ["Phần I trắc nghiệm 8 câu", 2, "mọi đề trường có TN 2–3đ"],
           ["Bài 1 thực hiện phép tính", 1.5, f"{tl(('D02', 'D05', 'D09'))}/{N} đề có ý tính ở phần TL"],
           ["Bài 2 tìm x", 1.5, f"{tl(('D04', 'D06', 'D10', 'D21'))}/{N} đề"],
           ["Bài 3 chia theo tỉ lệ (dãy tỉ số bằng nhau)", 1.5, f"D22 có ở {co['D22']}/{N} đề"],
           ["Bài 4 hai đường thẳng song song, tính góc", 1.5, f"D13 có ở {co['D13']}/{N} đề"],
           ["Bài 5 tam giác bằng nhau", 1.5, "bài hình chứng minh cuối đề"],
           ["Bài 6 vận dụng cao", 0.5, f"{sum(1 for d in des if any(c['muc'] == 'VDC' for c in d['cau']))}/{N} đề có ý VDC"],
           [], ["Phạm vi (chốt 11/11/2026)", "", khung.get("pham_vi_ck1", {}).get("chot", "")]]

    td = [["Chương", "Tên chương", "Bài", "Tên bài", "Trong CK1 trung tâm"]]
    for c in khung["chuong"]:
        for b in c["bai"]:
            trong = c["so"] <= 5 or (c["so"] == 6 and b[0] in (20, 21))
            td.append([c["so"], c["ten"], b[0], b[1], "Có" if trong else "Không"])
    return {"Đề thi và nguồn": dt, "Phân dạng": pd, "Thống kê dạng": tk, "Thống kê chương - mức": tc,
            "Khung đề các trường": kh, "Tiến độ KNTT": td}


def main():
    khung, des, loi = doc()
    for x in loi:
        print("✗", x)
    if loi:
        return 1
    tabs = bang(khung, des)
    L6.OUT = OUT
    L6.ghi(tabs)
    from openpyxl import load_workbook  # cột % riêng lớp 7 (E, F, P, Q) — ghi() lớp 6 chỉ biết E, N, O
    wb = load_workbook(OUT); ws = wb["Thống kê dạng"]
    for r in range(4, ws.max_row + 1):
        for col in (5, 6, 16, 17):
            ws.cell(row=r, column=col).number_format = "0%"
        for col in (14,):
            ws.cell(row=r, column=col).number_format = "General"
    wb.save(OUT)
    print(f"✓ {len(des)} đề, {len(tabs['Phân dạng']) - 1} ý ⇒ {OUT.relative_to(ROOT)}")
    for r in tabs["Thống kê dạng"][3:13]:
        print("  ", r[0], f"{r[4]:.0%}", f"{r[5]:.0%}", r[1][:50])
    return 0


if __name__ == "__main__":
    sys.exit(main())
