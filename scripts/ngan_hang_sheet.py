#!/usr/bin/env python3
"""Ngân hàng bài theo chương = tab phân dạng trên Google Sheets (Thầy chốt 22/10/2026).

QUY TRÌNH MỖI CHƯƠNG (thay cho bốc bài thẳng từ exams/*.json):
  ① Dựng tab "Phân dạng Ch.<N> lớp <K>" trên sheet dùng chung: đọc HẾT đề thi / SGK /
     tài liệu tham khảo trong inputs/, lọc bài thuộc chương, chép NGUYÊN VĂN
     (bài hình lấy cả bài, mọi ý vào một ô; cột "Phân loại vào phiếu nào?" ghi "Phiếu N").
  ② Chụp tab về repo:  agent đọc tab bằng connector Sheets (get_values A1:M…), lưu JSON thô,
        python scripts/ngan_hang_sheet.py nap RAW.json --sheet-id … --tab "…" \
            --grade lop-9 --subject hinh-hoc --chuong 5
  ③ Soát ĐỦ BÀI chưa:
        python scripts/ngan_hang_sheet.py du --grade lop-9 --subject hinh-hoc --chuong 5 --so-phieu 6 --tier C
        (hoặc --spec <thuyet-minh.json> khi đã có thuyết minh)
     THIẾU ⇒ quay lại ① tìm thêm inputs (đừng bịa, đừng hạ chuẩn). ĐỦ ⇒ dựng thuyết minh,
     source_refs = Mã câu của tab; thuyetminh_gate.check_nguon_sheet CHẶN mã ngoài tab.

Cách đếm "đủ" (đơn vị = Ý, khớp cách đếm câu của spec):
  • VD cần ý VD/VDC;  TH cần ý TH (thiếu thì lấy ý VD còn dư);
  • NB lấy ý NB, thiếu thì cắt bước từ ý TH/VD còn dư (mỗi ý ≤2 NB — decompose th2nb);
  • dòng 'NB lẻ LT' được tự soạn (câu hỏi thẳng lý thuyết) ⇒ không tính vào phần thiếu;
  • mỗi ý chỉ dùng MỘT lần cho cả chương; bốc đề thi (Ưu tiên 1) trước, rồi SGK, rồi STK.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.schema import ngan_hang_sheet as nhs  # noqa: E402

NB_MOI_Y = 2  # một ý TH/VD cắt ra tối đa ngần này câu NB đệm


def cmd_nap(a) -> None:
    raw = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    values = raw["values"] if isinstance(raw, dict) else raw
    snap = nhs.from_values(values, sheet_id=a.sheet_id, tab=a.tab,
                           pulled_at=a.pulled_at or datetime.now().isoformat(timespec="minutes"))
    out = nhs.snapshot_path(a.grade, a.subject, a.chuong)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    c = Counter(r["band"] for r in snap["rows"])
    print(f"✓ {out.relative_to(nhs.settings.ROOT)}: {len(snap['rows'])} bài · "
          + " · ".join(f"{b} {c[b]}" for b in nhs.BANDS_ORDER))


def _demand_from_spec(path: str) -> dict[int, dict]:
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for k, p in enumerate(spec["phieu"], 1):
        need = Counter()
        tu_soan = 0
        for r in p["rows"]:
            n = r.get("onclass", 0) + r.get("btvn", 0) + r.get("vidu", 0)
            b = "VD" if r["band"] == "VDC" else r["band"]
            if (r.get("loai") or "").strip() == "NB lẻ LT":
                tu_soan += n
                continue
            need[b] += n
        out[k] = {"title": p.get("title", ""), "need": need, "tu_soan": tu_soan}
    return out


def _demand_from_tier(grade, subject, tier, so_phieu) -> dict[int, dict]:
    from src.schema.tier_spec import load_tier_spec, target_counts
    tc = target_counts(load_tier_spec(), grade, subject, tier)
    per = Counter()
    for seg in tc.values():
        for b, n in seg.items():
            per["VD" if b == "VDC" else b] += n
    return {k: {"title": f"phiếu {k} (chuẩn tầng {tier})", "need": Counter(per), "tu_soan": 0}
            for k in range(1, so_phieu + 1)}


def _units(snap) -> list[dict]:
    """Mỗi ý của mỗi bài = 1 đơn vị {ma, uu, band, phieu}."""
    out = []
    for r in snap["rows"]:
        ph = nhs.phieu_so(r.get("phieu", ""))
        if not ph:
            continue
        ys = nhs.parse_muc_y(r.get("muc_y", "")) or [("", r.get("band", "TH"))]
        for lab, b in ys:
            out.append({"ma": r["ma"], "y": lab, "uu": nhs.uu_so(r.get("uu", "")),
                        "band": "VD" if b == "VDC" else b, "phieu": ph})
    out.sort(key=lambda u: u["uu"])
    return out


def cmd_du(a) -> int:
    snap = nhs.load(a.grade, a.subject, a.chuong)
    if not snap:
        print(f"✗ chưa có snapshot {nhs.snapshot_path(a.grade, a.subject, a.chuong)} — chạy `nap` trước")
        return 2
    demand = (_demand_from_spec(a.spec) if a.spec
              else _demand_from_tier(a.grade, a.subject, a.tier, a.so_phieu))
    units = _units(snap)
    used: set[int] = set()
    bo = sum(1 for r in snap["rows"] if not nhs.phieu_so(r.get("phieu", "")))
    print(f"Tab '{snap['tab']}' (chụp {snap['pulled_at']}): {len(snap['rows'])} bài, "
          f"{len(units)} ý dùng được ({bo} bài 'Chưa có phiếu' không tính)\n")
    print(f"{'phiếu':6s} {'kho NB/TH/VD':14s} {'cần NB/TH/VD':14s} {'bốc được NB/TH/VD':19s} {'thiếu':12s} nguồn VD+TH (đề/SGK/STK)")
    tong_thieu = Counter()
    for k in sorted(demand):
        need = demand[k]["need"]
        pool = [i for i, u in enumerate(units) if k in u["phieu"] and i not in used]
        kho = Counter(units[i]["band"] for i in pool)
        got = Counter()
        src = Counter()

        def take(band_ok, n):
            nonlocal pool
            picked = []
            for i in pool:
                if len(picked) >= n:
                    break
                if units[i]["band"] in band_ok:
                    picked.append(i)
            used.update(picked)
            pool = [i for i in pool if i not in used]
            return picked

        for i in take({"VD"}, need["VD"]):
            got["VD"] += 1; src[units[i]["uu"]] += 1
        th = take({"TH"}, need["TH"])
        th += take({"VD"}, need["TH"] - len(th))
        got["TH"] = len(th); src.update(units[i]["uu"] for i in th)
        nb = take({"NB"}, need["NB"])
        con = need["NB"] - len(nb)
        cut = take({"TH", "VD"}, -(-con // NB_MOI_Y)) if con > 0 else []
        got["NB"] = min(need["NB"], len(nb) + NB_MOI_Y * len(cut))
        thieu = Counter({b: max(0, need[b] - got[b]) for b in ("NB", "TH", "VD")})
        tong_thieu += thieu
        tt = " ".join(f"{b}{thieu[b]}" for b in ("NB", "TH", "VD") if thieu[b]) or "—"
        print(f"P{k:<5d} {kho['NB']:>3}/{kho['TH']:>3}/{kho['VD']:>3}    {need['NB']:>3}/{need['TH']:>2}/{need['VD']:>2}       "
              f"{got['NB']:>3}/{got['TH']:>2}/{got['VD']:>2}            {tt:12s} "
              f"{src[1]}/{src[2]}/{src[3]}"
              + (f"   (+{demand[k]['tu_soan']} câu NB lẻ LT tự soạn)" if demand[k]["tu_soan"] else ""))
    du = not +tong_thieu
    print("\n" + ("✓ ĐỦ BÀI — dựng thuyết minh, source_refs = Mã câu của tab."
                  if du else
                  "✗ THIẾU: " + ", ".join(f"{b} {n} ý" for b, n in tong_thieu.items() if n)
                  + " — tìm thêm inputs, bổ sung tab, nạp lại rồi soát lại."))
    return 0 if du else 1


# ── Bước 0 tự động hoá: giao → (agent quét) → gop → (ghi tab) → doi-chieu ─────────────
DOC = nhs.settings.ROOT / "docs" / "quy-trinh-ngan-hang-chuong.md"
KY = {"cuoi-ki-1": "ck1", "giua-ki-1": "gk1", "giua-ki-2": "gk2", "de-cuoi-ki-2": "ck2", "thi-thu-vao-10": "v10"}
SHEET_ID = "1ucQH5yw5bn3C1Bh_V4tAToa6NN5-F-nt8_2yxf2LNOM"


def _mau_prompt() -> str:
    t = DOC.read_text(encoding="utf-8")
    return t.split("<!-- MAU-PROMPT-BEGIN -->", 1)[1].split("<!-- MAU-PROMPT-END -->", 1)[0].strip()


def _quy_uoc_id(it: dict, kh: dict) -> str:
    if it["nhom"] == "de":
        k = KY.get(it["goc"], it["goc"])
        return f"`{k}-<trường-không-dấu>-<năm bắt đầu>-<số câu>` (vd `{k}-chuong-duong-2024-IV2`)"
    if it["nhom"] == "sgk":
        return "`sgk-<bài>-<vd|lt|vdg|tt|tl|hd|bt><số>` (vd `sgk-b16-lt2`, bài tập cuối bài `sgk-5.12`)"
    return "`tl-<tên file viết tắt>-<số thứ tự bài trong file>-tr<trang>` (số thứ tự đếm liên tục cả file vì sách đánh lại 'Bài 1' mỗi dạng)"


def cmd_giao(a) -> None:
    from src.schema import ngan_hang_quy_trinh as q
    kh = q.load_khung(a.grade, a.subject, a.chuong)
    items = q.kiem_ke(kh)
    od, cd = q.out_dir(a.grade, a.subject, a.chuong), q.chuong_dir(a.grade, a.subject, a.chuong)
    (od / "viec").mkdir(parents=True, exist_ok=True)
    (cd / "ban-ghi").mkdir(parents=True, exist_ok=True); (cd / "log").mkdir(parents=True, exist_ok=True)
    (od / "kiem-ke.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    mau = _mau_prompt()
    viec: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        viec[it["viec"]].append(it)
    da_co = {p.stem for p in (cd / "ban-ghi").glob("*.json")}
    for v, lst in viec.items():
        sgk = kh.get("sgk") or {}
        note = ""
        if lst[0]["nhom"] == "sgk":
            tr = sgk.get("trang_pdf", ["?", "?"])
            note = (f"Chỉ trang PDF {tr[0]}–{tr[1]}. Lấy MỌI mục có câu hỏi cụ thể: Ví dụ (chỉ đề), Luyện tập, Vận dụng, "
                    f"Thử thách, Tranh luận, HĐ là bài chứng minh/tính cụ thể, bài tập cuối bài ({sgk.get('bai_tap', '')}), "
                    f"luyện tập chung, bài tập cuối chương.")
        work = od / "anh" / v
        txt = mau.format(
            ten_chuong=kh["ten_chuong"], lop=kh["grade"].split("-")[-1], root=nhs.settings.ROOT,
            pham_vi=kh["pham_vi"], viec=v, so_file=len(lst),
            ds_file="\n".join(f"- `{it['file']}`" for it in lst), ghi_chu_viec=note, work=work,
            dau_hieu=kh["dau_hieu_trong_chuong"], ngoai_chuong=kh.get("ngoai_chuong_hay_gap", ""),
            loai_khi=kh.get("loai_khi", ""), quy_uoc_id=_quy_uoc_id(lst[0], kh),
            ds_bai=", ".join(f'"{b}"' for b in kh.get("id_prefix_bai", {})),
            out_json=cd / "ban-ghi" / f"{v}.json", out_log=cd / "log" / f"{v}.txt")
        (od / "viec" / f"{v}.md").write_text(txt + "\n", encoding="utf-8")
    c = Counter(it["nhom"] for it in items)
    print(f"Kiểm kê {len(items)} file (đề {c['de']} · SGK {c['sgk']} · tài liệu {c['tai_lieu']}) → {len(viec)} việc:")
    for v, lst in sorted(viec.items()):
        print(f"  {'✓' if v in da_co else '·'} {v:32s} {len(lst):3d} file   {(od / 'viec' / (v + '.md')).relative_to(nhs.settings.ROOT)}")
    print("\nMỗi việc ⇒ một subagent, prompt = nội dung file .md (chạy song song). Xong hết ⇒ make bank-gop.")


def _doc_ban_ghi(cd: Path) -> tuple[list[dict], dict[str, str]]:
    recs, logs = [], {}
    for f in sorted((cd / "ban-ghi").glob("*.json")):
        recs += json.loads(f.read_text(encoding="utf-8"))
    for f in sorted((cd / "log").glob("*.txt")):
        logs[f.stem] = f.read_text(encoding="utf-8")
    return recs, logs


def cmd_gop(a) -> int:
    from src.schema import ngan_hang_quy_trinh as q
    kh = q.load_khung(a.grade, a.subject, a.chuong)
    cd, od = q.chuong_dir(a.grade, a.subject, a.chuong), q.out_dir(a.grade, a.subject, a.chuong)
    recs, logs = _doc_ban_ghi(cd)
    snap = nhs.load(a.grade, a.subject, a.chuong)
    co_san = {r["ma"] for r in snap["rows"]} if snap else set()
    moi = [r for r in recs if r.get("id") not in co_san]
    loi = q.kiem_ban_ghi(moi)
    # Phủ kiểm kê: file có bài thì hiển nhiên đã mở; file 0 bài phải có dòng log.
    items = q.kiem_ke(kh)
    co_bai = {unicodedata.normalize("NFC", r.get("file", "")) for r in recs}
    tat_ca_log = "\n".join(logs.values())
    sot = [it["file"] for it in items if unicodedata.normalize("NFC", it["file"]) not in co_bai
           and q.kiem_log([dict(it, viec="*")], {"*": tat_ca_log})]
    print(f"Bản ghi {len(recs)} (đã có trên tab {len(recs) - len(moi)}, mới {len(moi)}) · kiểm kê {len(items)} file")
    if sot:
        loi += [f"chưa mở / thiếu log: {f}" for f in sot]
    if loi:
        print(f"✗ {len(loi)} lỗi — sửa bản ghi/log rồi chạy lại:")
        for m in loi[:40]:
            print("   ", m)
        return 1
    if not moi:
        print("✓ Không có bài mới — tab đã đủ mọi bản ghi.")
        return 0
    rows = q.dung_hang(moi, kh)
    start = (len(snap["rows"]) if snap else 0) + 2
    nen, pairs = q.nen(rows, tu_them=tuple(kh.get("tu_nen", ())) + q_TU_NEN)
    khoi = q.chia_khoi(nen, start)
    day = od / "day"
    if day.exists():
        for f in day.glob("*"):
            f.unlink()
    day.mkdir(parents=True, exist_ok=True)
    (day / "rows-moi.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    for i, k in enumerate(khoi):
        (day / f"khoi-{i:02d}.json").write_text(json.dumps(k, ensure_ascii=False), encoding="utf-8")
    end = khoi[-1]["end"]
    fr = q.find_replace_requests(pairs, kh["sheet_tab_id"], start, end)
    (day / "find-replace.json").write_text(json.dumps(fr, ensure_ascii=False), encoding="utf-8")
    sort = [{"sortRange": {"range": {"sheetId": kh["sheet_tab_id"], "startRowIndex": 1, "endRowIndex": end,
                                     "startColumnIndex": 0, "endColumnIndex": 13},
                           "sortSpecs": [{"dimensionIndex": 2, "sortOrder": "DESCENDING"},
                                         {"dimensionIndex": 4, "sortOrder": "ASCENDING"},
                                         {"dimensionIndex": 10, "sortOrder": "DESCENDING"}]}}]
    (day / "sort.json").write_text(json.dumps(sort, ensure_ascii=False), encoding="utf-8")
    raw = sum(len(json.dumps(r, ensure_ascii=False).encode()) for r in rows)
    nn = sum(len(json.dumps(r, ensure_ascii=False).encode()) for r in nen)
    c = Counter(r[2] for r in rows)
    print(f"✓ {len(rows)} hàng mới ({' · '.join(f'{b} {c[b]}' for b in ('VDC', 'VD', 'TH', 'NB'))}) → dòng {start}–{end}; "
          f"nén {raw // 1024}→{nn // 1024} KB, {len(pairs)} mã, {len(khoi)} khối:")
    for i, k in enumerate(khoi):
        print(f"   khoi-{i:02d}.json → '{kh['tab']}'!A{k['start']}:M{k['end']}")
    print(f"\nGhi: mỗi khối một subagent (prompt mẫu dưới) → batchUpdate {(day / 'find-replace.json').name} → "
          f"batchUpdate {(day / 'sort.json').name} → get_values A1:M{end} → make bank-doi-chieu RAW=…\n")
    print(f"Prompt ghi khối: \"Load ToolSearch 'select:mcp__claude_ai_Google_Sheets__update_values,"
          f"mcp__claude_ai_Google_Sheets__get_values'. Print rows of {day}/khoi-NN.json with "
          f"python3 -c \\\"import json;print(json.dumps(json.load(open(P))['rows'],ensure_ascii=False))\\\" and call "
          f"update_values spreadsheetId {SHEET_ID}, range '{kh['tab']}'!A<start>:M<end>, values = rows EXACTLY. "
          f"Touch nothing else. Verify column M ids, report.\"")
    return 0


q_TU_NEN = ("đường tròn", "tiếp tuyến", "Chứng minh", "đường thẳng", "đường kính", "bán kính", " lần lượt ",
            "Bài hình tổng hợp: ", "Ví dụ có lời giải", "Trắc nghiệm", "Tính độ dài", "tam giác", "phương trình",
            "Giải phương trình", "hệ phương trình", "Tính giá trị", "biểu thức", "Đề cuối kì", "Đề giữa kì",
            "Đề thi thử vào 10", "SGK Toán ")


def cmd_doi_chieu(a) -> int:
    from src.schema import ngan_hang_quy_trinh as q
    kh = q.load_khung(a.grade, a.subject, a.chuong)
    raw = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    values = raw["values"] if isinstance(raw, dict) else raw
    day = q.out_dir(a.grade, a.subject, a.chuong) / "day"
    moi = json.loads((day / "rows-moi.json").read_text(encoding="utf-8")) if (day / "rows-moi.json").exists() else []
    loi = q.doi_chieu(values, moi)
    snap = nhs.load(a.grade, a.subject, a.chuong)
    if snap:   # bài cũ không được mất
        ma_tab = {(r + [""] * 13)[12] for r in values[1:]}
        loi += [f"{r['ma']}: bài cũ biến mất khỏi tab" for r in snap["rows"] if r["ma"] not in ma_tab]
    sot = q.ma_con_sot(values)
    if sot:
        loi.append(f"{sot} ô còn mã nén ~XX~ — chưa chạy find-replace.json")
    if loi:
        print(f"✗ {len(loi)} chỗ lệch (chưa chụp snapshot):")
        for m in loi[:40]:
            print("   ", m)
        return 1
    snap2 = nhs.from_values(values, sheet_id=a.sheet_id, tab=kh["tab"],
                            pulled_at=datetime.now().isoformat(timespec="minutes"))
    out = nhs.snapshot_path(a.grade, a.subject, a.chuong)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap2, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    nhs._CACHE.clear()
    print(f"✓ Khớp {len(moi)} hàng mới từng ô, 0 mã sót; snapshot {out.relative_to(nhs.settings.ROOT)}: "
          f"{len(snap2['rows'])} bài. Bước kế: make du-bai.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    for name in ("giao", "gop", "doi-chieu"):
        p = sp.add_parser(name)
        p.add_argument("--grade", required=True)
        p.add_argument("--subject", required=True)
        p.add_argument("--chuong", required=True, type=int)
        if name == "doi-chieu":
            p.add_argument("raw", help="JSON thô get_values cả tab (A1:M…)")
            p.add_argument("--sheet-id", default=SHEET_ID)
    for name in ("nap", "du"):
        p = sp.add_parser(name)
        p.add_argument("--grade", required=True)
        p.add_argument("--subject", required=True)
        p.add_argument("--chuong", required=True)
        if name == "nap":
            p.add_argument("raw", help="JSON thô từ get_values ({values:[[…]]})")
            p.add_argument("--sheet-id", required=True)
            p.add_argument("--tab", required=True)
            p.add_argument("--pulled-at", default="")
        else:
            p.add_argument("--spec", help="thuyet-minh.json (nếu đã có)")
            p.add_argument("--so-phieu", type=int, default=0, help="số phiếu của chương (khi chưa có spec)")
            p.add_argument("--tier", default="C")
    a = ap.parse_args()
    if a.cmd == "giao":
        cmd_giao(a)
        return 0
    if a.cmd == "gop":
        return cmd_gop(a)
    if a.cmd == "doi-chieu":
        return cmd_doi_chieu(a)
    if a.cmd == "nap":
        cmd_nap(a)
        return 0
    if not a.spec and not a.so_phieu:
        ap.error("du: cần --spec hoặc --so-phieu")
    return cmd_du(a)


if __name__ == "__main__":
    sys.exit(main())
