#!/usr/bin/env python3
"""PHÂN DẠNG ĐỀ CUỐI HỌC KÌ I TOÁN 6 (Hà Nội, 2025-2026, KNTT) → một file .xlsx để tải lên Google Sheets.

Thầy chốt 11/11/2026: chỉ ĐỀ THI, chỉ Hà Nội; ban đầu chỉ 2025-2026 (15 đề), sau Thầy cho thêm 2024-2025 (9 đề) ⇒ 24 đề,
bám tiến độ KNTT (Kì I = Chương I–V). Bước 1 của việc dựng 3 đề ôn + 3 đề CK1 chính thức lớp 6.

Vào:  config/khung-phan-dang/lop-6-ck1-kntt.json                (chương/bài KNTT + danh mục dạng D01–D27)
      inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi/*.json        (mỗi đề một tệp, mỗi ý một bản ghi, đã soi ảnh)
Ra:   outputs/ngan-hang-sheet/lop-6/ck1/Phan-dang-CK1-Toan6-Ha-Noi.xlsx

    .venv/bin/python scripts/lop6_ck1_phan_dang.py           # kiểm + ghi xlsx
    .venv/bin/python scripts/lop6_ck1_phan_dang.py --kiem    # chỉ kiểm

Số trong tab Thống kê là SỐ TĨNH do script tính (sửa bản ghi rồi chạy lại), không phải công thức.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KHUNG = ROOT / "config/khung-phan-dang/lop-6-ck1-kntt.json"
BG = ROOT / "inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi"
OUT = ROOT / "outputs/ngan-hang-sheet/lop-6/ck1/Phan-dang-CK1-Toan6-Ha-Noi.xlsx"
HT = {"TN": "Trắc nghiệm", "Đ-S": "Đúng sai", "Điền": "Trả lời ngắn", "TL": "Tự luận"}
MUC = ["NB", "TH", "VD", "VDC"]


def doc() -> tuple[dict, list[dict], list[str]]:
    khung = json.loads(KHUNG.read_text(encoding="utf-8"))
    des = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(BG.glob("*.json"))]
    loi = []
    ma_dang = {d["ma"]: d for d in khung["dang"]}
    bai_cd = {b[0]: c["so"] for c in khung["chuong"] for b in c["bai"]}
    for d in des:
        tong = round(sum(c["diem"] for c in d["cau"]), 2)
        if tong != 10:
            loi.append(f"{d['de']}: tổng điểm {tong} ≠ 10")
        for c in d["cau"]:
            if c["dang"] not in ma_dang:
                loi.append(f"{d['de']} {c['cau']}: dạng {c['dang']} không có trong khung")
            if c["muc"] not in MUC:
                loi.append(f"{d['de']} {c['cau']}: mức {c['muc']}")
            if bai_cd.get(c["bai"], c["cd"]) != c["cd"] and c["bai"] not in (2,):
                loi.append(f"{d['de']} {c['cau']}: bài {c['bai']} không thuộc chương {c['cd']}")
    return khung, des, loi


def bang(khung: dict, des: list[dict]) -> dict[str, list[list]]:
    N = len(des)
    ten_dang = {d["ma"]: d["ten"] for d in khung["dang"]}
    ten_bai = {b[0]: b[1] for c in khung["chuong"] for b in c["bai"]}
    ten_cd = {c["so"]: c["ten"] for c in khung["chuong"]}

    dt = [["Mã đề", "Năm học", "Trường / đơn vị ra đề", "Địa bàn (phường/xã mới — quận/huyện cũ)", "Thời gian",
           "Cấu trúc đề", "Số ý đã bóc", "Có HDC", "Đề gốc (toanmath)", "File PDF trong repo", "Ghi chú"]]
    pd = [["Mã câu", "Mã đề", "Năm học", "Trường", "Câu", "Bài cụ thể (đã soi ảnh)", "Hình thức", "Điểm", "Mức độ",
           "Mã dạng", "Dạng bài", "Chương", "Bài SGK", "Tên bài SGK", "Đáp án", "Có hình", "Điểm là ước tính",
           "Cần soát", "Đề gốc"]]
    for d in des:
        lk = f'=HYPERLINK("{d["url"]}","Mở đề gốc")'
        dt.append([d["de"], d["nam_hoc"], d["truong"], d["dia_ban"], f"{d['thoi_gian']} phút", d["khung"],
                   len(d["cau"]), "Có" if d["co_hdc"] else "Không", lk,
                   f"inputs/refs/de-thi/lop-6/cuoi-ki-1/{d['pdf']}", d.get("ghi_chu_de", "")])
        for c in d["cau"]:
            pd.append([f"{d['de']}-{c['cau']}", d["de"], d["nam_hoc"], d["truong"], c["cau"], c["nd"], HT.get(c["ht"], c["ht"]),
                       c["diem"], c["muc"], c["dang"], ten_dang[c["dang"]], c["cd"], c["bai"],
                       ten_bai.get(c["bai"], ""), c["dap_an"], "Có" if c.get("co_hinh") else "",
                       "Ước" if c.get("diem_uoc") else "", c.get("can_soat", "") if c.get("can_soat") is not True else "Cần soát",
                       lk])

    # Thống kê dạng
    co, diem, so_y = Counter(), Counter(), Counter()
    muc = defaultdict(Counter)
    vi_du = defaultdict(list)
    for d in des:
        for c in d["cau"]:
            diem[c["dang"]] += c["diem"]; so_y[c["dang"]] += 1; muc[c["dang"]][c["muc"]] += 1
            if len(vi_du[c["dang"]]) < 3:
                vi_du[c["dang"]].append(f"{d['truong']} {c['cau']}")
        for k in {c["dang"] for c in d["cau"]}:
            co[k] += 1
    nam = Counter(d["nam_hoc"] for d in des)
    co_nam = defaultdict(Counter)
    for d in des:
        for k in {c["dang"] for c in d["cau"]}:
            co_nam[k][d["nam_hoc"]] += 1
    tk = [["Số đề", N, "Đề CK1 Toán 6 Hà Nội: " + "; ".join(f"{v} đề {k}" for k, v in sorted(nam.items(), reverse=True))
           + " (toàn bộ đề Hà Nội có trên toanmath / VietJack)"], [],
          ["Mã dạng", "Dạng bài", "Chương", "Số đề có dạng", "% đề có dạng", "Số ý", "Điểm TB mỗi đề",
           "NB", "TH", "VD", "VDC", "Bậc tần suất", "Ví dụ (trường – câu)", "% đề 2025-2026", "% đề 2024-2025"]]
    for k in sorted(ten_dang, key=lambda k: (-co[k], -diem[k])):
        p = co[k] / N
        bac = "Top 1 (≥ 80%)" if p >= .8 else "Top 2 (40–79%)" if p >= .4 else "Ít gặp (20–39%)" if p >= .2 else "Hiếm (< 20%)"
        cd = next(x["cd"] for x in khung["dang"] if x["ma"] == k)
        tk.append([k, ten_dang[k], cd, co[k], round(p, 3), so_y[k], round(diem[k] / N, 2),
                   *[muc[k][m] for m in MUC], bac, "; ".join(vi_du[k]),
                   round(co_nam[k]["2025-2026"] / max(nam["2025-2026"], 1), 3), round(co_nam[k]["2024-2025"] / max(nam["2024-2025"], 1), 3)])

    # Thống kê chương + mức
    cdd, cdco, md = Counter(), Counter(), Counter()
    for d in des:
        for c in d["cau"]:
            cdd[c["cd"]] += c["diem"]; md[c["muc"]] += c["diem"]
        for k in {c["cd"] for c in d["cau"]}:
            cdco[k] += 1
    tc = [["Chương", "Tên chương", "Số đề có chương", "% đề", "Điểm TB mỗi đề", "% điểm"]]
    for c in khung["chuong"]:
        s = c["so"]
        tc.append([s, ten_cd[s], cdco[s], round(cdco[s] / N, 3), round(cdd[s] / N, 2), round(cdd[s] / N / 10, 3)])
    tc += [[], ["Mức độ", "", "", "", "Điểm TB mỗi đề", "% điểm"]]
    for m in MUC:
        tc.append([m, "", "", "", round(md[m] / N, 2), round(md[m] / N / 10, 3)])

    # Khung đề các trường (cấu trúc phần/bài)
    kh = [["Cấu trúc", "Số đề", "Các đề"]]
    nhom = defaultdict(list)
    for d in des:
        tn = sum(c["diem"] for c in d["cau"] if c["ht"] != "TL")
        nhom["Không trắc nghiệm (thuần tự luận)" if tn == 0 else f"Trắc nghiệm {tn:g}đ + tự luận {10 - tn:g}đ"].append(d["truong"])
    for k, v in sorted(nhom.items(), key=lambda x: -len(x[1])):
        kh.append([k, len(v), "; ".join(v)])
    kh += [[], ["Tự luận: dạng bài theo vị trí", "Số đề", "Ghi chú"],
           ["Thực hiện phép tính (cộng trừ hợp lí, phân phối, biểu thức ngoặc + luỹ thừa)", sum(1 for d in des if any(c["dang"] in ("D12", "D13", "D03") and c["ht"] == "TL" for c in d["cau"])), "3–4 ý, ~2đ"],
           ["Tìm x (số nguyên; có ý tích = 0 / luỹ thừa / chia hết)", sum(1 for d in des if any(c["dang"] in ("D14", "D15", "D04", "D08") and c["ht"] == "TL" for c in d["cau"])), "3–4 ý, 1,5–2đ"],
           ["Bài thực tế BCNN (xếp hàng vừa đủ, trong khoảng)", co["D10"], "1,5đ"],
           ["Bài thực tế ƯCLN (chia đều nhiều nhất)", co["D09"], "1,5đ (thay cho BCNN ở 6/15 đề)"],
           ["Bài hình thực tế: chu vi, diện tích mảnh vườn + chi phí", co["D22"], "2–2,5đ, 2–3 ý, luôn có hình"],
           ["Câu cuối VDC 0,5đ", sum(1 for d in des if any(c["muc"] == "VDC" for c in d["cau"])), "chia hết / nguyên tố cùng nhau / tìm x, y nguyên / tổng luỹ thừa / suy luận"]]

    td = [["Chương", "Tên chương", "Bài", "Tên bài", "Học kì (SGK KNTT)"]]
    for c in khung["chuong"]:
        for b in c["bai"]:
            td.append([c["so"], c["ten"], b[0], b[1], "Kì I"])
    return {"Đề thi và nguồn": dt, "Phân dạng": pd, "Thống kê dạng": tk, "Thống kê chương - mức": tc,
            "Khung đề các trường": kh, "Tiến độ KNTT": td}


def ghi(tabs: dict[str, list[list]]) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    rong = {"Đề thi và nguồn": {"A": 26, "C": 30, "D": 34, "F": 40, "I": 14, "J": 50, "K": 60},
            "Phân dạng": {"A": 28, "B": 22, "D": 22, "F": 70, "K": 46, "N": 34, "O": 34, "R": 30},
            "Thống kê dạng": {"B": 60, "L": 18, "M": 60},
            "Thống kê chương - mức": {"B": 46},
            "Khung đề các trường": {"A": 70, "C": 90},
            "Tiến độ KNTT": {"B": 44, "D": 56}}
    dau = {"Thống kê dạng": 3}
    wb = Workbook(); wb.remove(wb.active)
    for ten, rows in tabs.items():
        ws = wb.create_sheet(ten)
        for r in rows:
            ws.append(r)
        h = dau.get(ten, 1)
        ws.freeze_panes = ws.cell(row=h + 1, column=1)
        for c in ws[h]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F3864")
        for row in ws.iter_rows(min_row=h + 1):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        for col in range(1, ws.max_column + 1):
            L = get_column_letter(col)
            ws.column_dimensions[L].width = rong.get(ten, {}).get(L, 12)
        if ten == "Thống kê dạng":
            for r in range(4, ws.max_row + 1):
                for col in (5, 14, 15):
                    ws.cell(row=r, column=col).number_format = "0%"
        if ten == "Thống kê chương - mức":
            for r in range(2, ws.max_row + 1):
                for col in (4, 6):
                    ws.cell(row=r, column=col).number_format = "0%"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--kiem", action="store_true"); a = ap.parse_args()
    khung, des, loi = doc()
    for x in loi:
        print("✗", x)
    if loi:
        return 1
    tabs = bang(khung, des)
    print(f"✓ {len(des)} đề, {len(tabs['Phân dạng']) - 1} ý, {len(khung['dang'])} dạng")
    if not a.kiem:
        ghi(tabs)
        print("✓ ghi", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
