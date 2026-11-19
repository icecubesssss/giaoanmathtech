#!/usr/bin/env python3
"""Ráp kết quả Gemini (storage/gemini/xong/checklist-<k>.json) thành lô lệnh Sheets cho tab checklist 4C/5C/7C.

    python3 scripts/gemini/lap_checklist_c.py 5c            # soát + in bảng dòng
    python3 scripts/gemini/lap_checklist_c.py 5c --lo       # ghi storage/gemini/soat/checklist-5c-lo.json
                                                            #  (requests cho update_spreadsheet)

Soát: mọi dòng CU/NX có nhận xét được gắn ĐÚNG MỘT lần; mã link_tu có thật và có link.
Cột W (nhận xét cũ) ghi bằng CÔNG THỨC trỏ về ô gốc ở tab ẩn rồi dán-giá-trị tại chỗ
⇒ chữ nguyên văn, không gõ lại. File kỳ vọng storage/gemini/soat/checklist-<k>-W.json dùng để so sau khi ghi.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_checklist_c import KHOI, NX_NGUOI, TEP  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
XONG = REPO / "storage" / "gemini" / "xong"
SOAT = REPO / "storage" / "gemini" / "soat"
SRC_SHEET = 1186092271           # tab ThaiTD - Checklist … 9C (mẫu bố cục)
NEW_ID = {"4c": 40400, "5c": 50500, "7c": 70700}
INDEX = {"4c": 11, "5c": 12, "7c": 13}
COT_NX = list("EFGHIJKLMNOPQR")


def bang(cu, moi, cfg):
    t = {"TD": moi[cfg["td"]], "CU": cu[cfg["cu"]], "NX": cu["NHẬN XÉT"]}
    if cfg["lk"]:
        t["LK"] = moi[cfg["lk"]]
    return {ma: {r["row"]: r["cells"] for r in rows} for ma, rows in t.items()}


def ngay(v):
    if isinstance(v, (int, float)) and 40000 < v < 60000:
        return (dt.date(1899, 12, 30) + dt.timedelta(days=int(v))).strftime("%d/%m/%Y")
    if isinstance(v, str) and "/" in v:
        return v
    return ""


def cot_cu(cu_rows):
    """Tên cột tab cũ theo dòng 4 → chữ cột."""
    td = {c: v.get("v", "") for c, v in cu_rows.get(4, {}).items()}
    tim = lambda s: next((c for c, v in td.items() if v == s), None)  # noqa: E731
    return dict(nd1=tim("Ngày duyệt 1"), kq1=tim("Kết quả DUYỆT 1"), ct1=tim("Chi tiết nội dung DUYỆT 1"),
                nd2=tim("Ngày duyệt 2"), kq2=tim("Kết quả DUYỆT 2"), ph2=tim("Phản hồi DUYỆT 2"),
                kq=tim("Kết quả"), ht=tim("Ngày hoàn thành"))


def co_chu(c):
    v = c.get("v", "")
    return isinstance(v, str) and v.strip() != "" and not v.startswith("=")


def manh_cu(cells, cc):
    """Các mảnh nhận xét của một dòng CU: [(nhãn, cột)] + chuỗi kết quả ngắn."""
    manh, kq = [], []
    g = lambda c: cells.get(c, {}) if c else {}  # noqa: E731
    if co_chu(g(cc["kq1"])):
        kq.append(f"Duyệt 1{' (' + ngay(g(cc['nd1']).get('v')) + ')' if ngay(g(cc['nd1']).get('v')) else ''}: {g(cc['kq1'])['v'].strip()}")
    if co_chu(g(cc["kq2"])):
        kq.append(f"Duyệt 2{' (' + ngay(g(cc['nd2']).get('v')) + ')' if ngay(g(cc['nd2']).get('v')) else ''}: {g(cc['kq2'])['v'].strip()}")
    if co_chu(g(cc["kq"])) and len(g(cc["kq"])["v"]) <= 30:
        kq.append(f"Kết quả: {g(cc['kq'])['v'].strip()}")
    for nhan, c in (("Duyệt 1", cc["ct1"]), ("Duyệt 2", cc["ph2"])):
        if co_chu(g(c)):
            manh.append((nhan, c))
    if co_chu(g(cc["kq"])) and len(g(cc["kq"])["v"]) > 30:
        manh.append(("Kết quả", cc["kq"]))
    if co_chu(g(cc["ht"])):
        manh.append(("Ghi chú hoàn thành", cc["ht"]))
    for c in sorted(cells):
        if len(c) == 1 and c > "O" and co_chu(cells[c]):
            manh.append((f"Nhận xét thêm (cột {c})", c))
    return manh, kq


def nhan_cu(cells):
    for c in ("C", "B", "D", "A"):
        if co_chu(cells.get(c, {})):
            return " ".join(cells[c]["v"].split())
    return ""


def can_gan(ma, so, T, cc):
    cells = T[ma].get(so, {})
    if ma == "CU":
        if so <= 5:
            return False
        m, k = manh_cu(cells, cc)
        return bool(m or k)
    if ma == "NX":
        return any(co_chu(cells.get(c, {})) for c in COT_NX)
    return False


def gom_theo_chuong(dong):
    """7C dạy xen ĐS/HH ⇒ gom lại: ôn hè đầu · chương 1→10 (phiếu theo số) · ôn/KT theo kì · ôn hè cuối."""
    import re
    dau, cuoi, ky, chuong = [], [], {}, {}
    da_co_chuong = False
    for d in dong:
        m = re.match(r"Phiếu (\d+)\.(\d+)", d["cot_B"])
        if d["loai"] == "chuong":
            n = int(re.search(r"\d+", d["cot_A"]).group())
            chuong.setdefault(n, [None, []])[0] = d
            da_co_chuong = True
        elif m:
            chuong.setdefault(int(m.group(1)), [None, []])[1].append((int(m.group(2)), d))
        elif d["loai"] == "kiem_tra" and da_co_chuong:
            ky.setdefault(d["cot_A"].split()[-1], []).append(d)
        else:
            (cuoi if da_co_chuong else dau).append(d)
    out = list(dau)
    for n in sorted(chuong):
        tieu, ds = chuong[n]
        out += ([tieu] if tieu else []) + [d for _, d in sorted(ds, key=lambda x: x[0])]
    for nhom in ky.values():
        out += nhom
    return out + cuoi


def q(s):
    return '"' + s.replace('"', '""') + '"'


def main():
    k = sys.argv[1]
    cfg = KHOI[k]
    cu = json.loads((TEP / "cu.json").read_text())
    moi = json.loads((TEP / "moi.json").read_text())
    T = bang(cu, moi, cfg)
    cc = cot_cu(T["CU"])
    kq = json.loads((XONG / f"checklist-{k}.json").read_text())["ket_qua"]
    if isinstance(kq, str):
        kq = json.loads(kq)
    dong = kq["dong"]
    if k == "7c":
        dong = gom_theo_chuong(dong)
    loi = []

    # 1. dòng NX nằm trong dải của khối
    a, b = cfg["nx"]
    dem = {}
    for i, d in enumerate(dong):
        for ref in d["gan_cu"]:
            ma, _, so = ref.partition(":")
            so = int(so) if so.isdigit() else -1
            if ma not in ("CU", "NX") or so not in T[ma] or (ma == "NX" and not a <= so <= b):
                loi.append(f"dòng {i}: mã gắn lạ {ref}")
            dem[ref] = dem.get(ref, 0) + 1
        lt = d["link_tu"]
        if lt:
            ma, _, so = lt.partition(":")
            c = T.get(ma, {}).get(int(so) if so.isdigit() else -1)
            if not c or not any("link" in v for v in c.values()):
                loi.append(f"dòng {i} ({d['cot_B']}): link_tu {lt} không có link")
    for ma in ("CU", "NX"):
        for so in T[ma]:
            if ma == "NX" and not a <= so <= b:
                continue
            ref = f"{ma}:{so}"
            if can_gan(ma, so, T, cc) and dem.get(ref, 0) != 1:
                loi.append(f"{ref} ({nhan_cu(T[ma][so])[:40]}) gắn {dem.get(ref, 0)} lần — phải đúng 1")
    for x in loi:
        print("LỖI:", x)

    # 2. dựng dòng
    tab_cu, tab_nx = cfg["cu"], "NHẬN XÉT"
    hang, ky_vong = [], []
    for d in dong:
        url = ""
        if d["link_tu"]:
            ma, _, so = d["link_tu"].partition(":")
            url = next((v["link"] for v in T[ma][int(so)].values() if "link" in v), "")
        ket_qua, cong_thuc, mong = [], [], []
        for ref in d["gan_cu"]:
            ma, _, so = ref.partition(":")
            so = int(so)
            cells = T[ma][so]
            if ma == "CU":
                manh, kqs = manh_cu(cells, cc)
                tieu = f"[{tab_cu} · {nhan_cu(cells)}]"
                if kqs:
                    ket_qua.append((tieu + " " if len(d["gan_cu"]) > 1 else "") + " · ".join(kqs))
                pieces = [(nhan, f"'{tab_cu}'!{c}{so}", cells[c]["v"]) for nhan, c in manh]
            else:
                ten_p = nhan_cu({"D": cells.get("D", {})}) or "nhận xét tiếp dòng trên"
                tieu = f"[{tab_nx} · {ten_p}]"
                pieces = [(NX_NGUOI[c], f"'{tab_nx}'!{c}{so}", cells[c]["v"]) for c in COT_NX if co_chu(cells.get(c, {}))]
            if not pieces:
                continue
            ct = [q(tieu)]
            mg = [tieu]
            for nhan, o, v in pieces:
                ct.append(q(f"\n{nhan}:\n") + "&" + o)
                mg.append(f"\n{nhan}:\n{v}")
            cong_thuc.append("&".join(ct))
            mong.append("".join(mg))
        W = ("=" + "&CHAR(10)&CHAR(10)&".join(c.replace('\n', '"&CHAR(10)&"') for c in cong_thuc)) if cong_thuc else ""
        hang.append(dict(loai=d["loai"], A=d["cot_A"], B=d["cot_B"], ten=d["ten"], url=url,
                         V="\n".join(ket_qua), W=W))
        ky_vong.append("\n\n".join(mong))

    for i, h in enumerate(hang):
        print(f"{i + 4:>3} {h['loai'][:6]:6} {h['A'][:12]:12} {h['B'][:14]:14} {h['ten'][:55]:55} "
              f"{'L' if h['url'] else '-'} V={h['V'][:40]!r} W={len(ky_vong[i])}")
    print("ghi_chu Gemini:", kq.get("ghi_chu", ""))
    if "--lo" not in sys.argv:
        return
    if loi:
        sys.exit("Còn lỗi — không lập lô.")
    SOAT.mkdir(parents=True, exist_ok=True)
    (SOAT / f"checklist-{k}-W.json").write_text(json.dumps(ky_vong, ensure_ascii=False, indent=1))
    (SOAT / f"checklist-{k}-lo.json").write_text(json.dumps(lo_lenh(k, cfg, hang), ensure_ascii=False))
    print("đã ghi lô", SOAT / f"checklist-{k}-lo.json")


def gr(sid, r0, r1, c0, c1):
    return {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1}


def lo_lenh(k, cfg, hang):
    sid, n = NEW_ID[k], len(hang)
    ten_tab = f"{cfg['ten']} - Checklist duyệt phiếu chi tiết {k.upper()}"
    R = [{"duplicateSheet": {"sourceSheetId": SRC_SHEET, "insertSheetIndex": INDEX[k], "newSheetId": sid,
                             "newSheetName": ten_tab}},
         {"deleteConditionalFormatRule": {"sheetId": sid, "index": 0}},
         {"deleteDimension": {"range": {"sheetId": sid, "dimension": "ROWS", "startIndex": 3, "endIndex": 60}}}]
    # định dạng: mọi dòng chép NGUYÊN dòng 5 tab mẫu (ô tích FALSE + validation); dòng chương chép nguyên dòng 4
    R.append({"copyPaste": {"source": gr(SRC_SHEET, 4, 5, 0, 21), "destination": gr(sid, 3, 3 + n, 0, 21),
                            "pasteType": "PASTE_NORMAL"}})
    for i, h in enumerate(hang):
        if h["loai"] == "chuong":
            R.append({"copyPaste": {"source": gr(SRC_SHEET, 3, 4, 0, 21), "destination": gr(sid, 3 + i, 4 + i, 0, 21),
                                    "pasteType": "PASTE_NORMAL"}})
    # 2 cột duyệt cũ V, W
    R += [
        {"copyPaste": {"source": gr(SRC_SHEET, 1, 2, 3, 4), "destination": gr(sid, 1, 2, 21, 23), "pasteType": "PASTE_FORMAT"}},
        {"mergeCells": {"range": gr(sid, 1, 2, 21, 23), "mergeType": "MERGE_ALL"}},
        {"copyPaste": {"source": gr(SRC_SHEET, 2, 3, 6, 7), "destination": gr(sid, 2, 3, 21, 23), "pasteType": "PASTE_FORMAT"}},
        {"copyPaste": {"source": gr(SRC_SHEET, 4, 5, 20, 21), "destination": gr(sid, 3, 3 + n, 21, 23), "pasteType": "PASTE_FORMAT"}},
        {"repeatCell": {"range": gr(sid, 3, 3 + n, 21, 23), "cell": {"userEnteredFormat": {
            "wrapStrategy": "CLIP", "verticalAlignment": "TOP",
            "backgroundColor": {"red": 0.96, "green": 0.96, "blue": 0.96}}},
            "fields": "userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment,userEnteredFormat.backgroundColor"}},
        {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 21, "endIndex": 22},
                                       "properties": {"pixelSize": 230}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 22, "endIndex": 23},
                                       "properties": {"pixelSize": 520}, "fields": "pixelSize"}},
        {"updateCells": {"start": {"sheetId": sid, "rowIndex": 0, "columnIndex": 0}, "fields": "userEnteredValue",
                         "rows": [{"values": [{"userEnteredValue": {"stringValue": f"CHECKLIST DUYỆT PHIẾU – TOÁN {k.upper()}"}}]}]}},
        {"updateCells": {"start": {"sheetId": sid, "rowIndex": 1, "columnIndex": 21}, "fields": "userEnteredValue", "rows": [
            {"values": [{"userEnteredValue": {"stringValue": f"Duyệt cũ (chép từ tab ẩn {cfg['cu']} và NHẬN XÉT)"}}]},
            {"values": [{"userEnteredValue": {"stringValue": "Kết quả duyệt cũ"}},
                        {"userEnteredValue": {"stringValue": "Nhận xét duyệt cũ (nguyên văn, bấm vào ô để đọc hết)"}}]}]}},
    ]
    abc, vw = [], []
    for h in hang:
        c = ({"userEnteredValue": {"formulaValue": f"=HYPERLINK({q(h['url'])};{q(h['ten'])})"}} if h["url"]
             else {"userEnteredValue": {"stringValue": h["ten"]}})
        abc.append({"values": [{"userEnteredValue": {"stringValue": h["A"]}}, {"userEnteredValue": {"stringValue": h["B"]}}, c]})
        vw.append({"values": [{"userEnteredValue": {"stringValue": h["V"]}},
                              {"userEnteredValue": {"formulaValue": h["W"]}} if h["W"] else {"userEnteredValue": {"stringValue": ""}}]})
    R.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 3, "columnIndex": 0}, "fields": "userEnteredValue", "rows": abc}})
    R.append({"updateCells": {"start": {"sheetId": sid, "rowIndex": 3, "columnIndex": 21}, "fields": "userEnteredValue", "rows": vw}})
    R.append({"addConditionalFormatRule": {"index": 0, "rule": {
        "ranges": [gr(sid, 3, 3 + n, a, b) for a, b in ((3, 6), (7, 9), (10, 13), (14, 16), (17, 20))],
        "booleanRule": {"condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": "=D4=TRUE"}]},
                        "format": {"backgroundColor": {"red": 0.7137255, "green": 0.88235295, "blue": 0.8}}}}}})
    # dán-giá-trị tại chỗ cho cột W (bỏ phụ thuộc tab ẩn)
    R.append({"copyPaste": {"source": gr(sid, 3, 3 + n, 22, 23), "destination": gr(sid, 3, 3 + n, 22, 23), "pasteType": "PASTE_VALUES"}})
    return R


if __name__ == "__main__":
    main()
