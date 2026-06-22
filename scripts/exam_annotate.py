"""Gắn `band` (NB/TH/VD/VDC) + `phut` (thời gian HS làm, ước) vào từng câu trong
ngân hàng đề thi JSON (inputs/refs/de-thi/.../exams/*.json).

Quy trình tách-bạch (kiểm toán được):
  extract     → in mọi câu CHƯA có band để AI/Thầy đọc & chấm.
  apply FILE  → đổ phán đoán {id: {band, phut}} từ FILE.json vào đề, gắn cờ
                `_band_auto`/`_phut_auto` để Thầy rà lại.
  report      → phút/câu THỰC theo band (đối chiếu rate card tier_spec) + độ phủ.
  fix-headers → backfill thoi_gian_phut/tong_diem còn thiếu (mặc định 90′/10đ),
                cảnh báo đề có Σdiem ≠ tong_diem.

Band CHẤM THEO BLOOM (xem AGENTS §3), KHÔNG suy máy móc từ điểm: câu cực trị 0,5đ
vẫn là VDC dù điểm thấp.
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

BANDS = ("NB", "TH", "VD", "VDC")
EXAMS_GLOB = "inputs/refs/de-thi/lop-9/exams/*.json"
DEFAULT_MINUTES = 90
DEFAULT_POINTS = 10.0


def _exam_files(pattern: str) -> list[Path]:
    return [Path(p) for p in sorted(glob.glob(pattern))]


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _cau_id(stem: str, c: dict) -> str:
    """Khoá ổn định cho 1 câu. GK1 có sẵn `id`; CK1 dùng `bai`+`y` → tổng hợp
    `{tên-đề}-{bai}{y}` cho khớp nếp đặt id của GK1 (vd ck1-cau-dien-1a)."""
    if c.get("id"):
        return c["id"]
    bai = str(c.get("bai", "")).strip()
    y = str(c.get("y", "") or "").strip()
    return f"{stem}-{bai}{y}"


def cmd_ensure_ids(args) -> int:
    """Ghi trường `id` (tổng hợp từ bai+y) vào câu nào còn thiếu — chuẩn hoá bank."""
    n = 0
    for f in _exam_files(args.glob):
        d = _load(f)
        changed = False
        for c in d.get("cau", []):
            if not c.get("id"):
                c["id"] = _cau_id(f.stem, c)
                changed = True
                n += 1
        if changed:
            _save(f, d)
            print(f"  ✓ {f.name}")
    print(f"\nĐã gắn id cho {n} câu.")
    return 0


def cmd_extract(args) -> int:
    """In mọi câu CHƯA có band (hoặc --all) để chấm. Mặc định format người-đọc;
    --json xuất {id: {dang, do_kho, diem, de}} cho công cụ."""
    out: dict[str, dict] = {}
    for f in _exam_files(args.glob):
        d = _load(f)
        for c in d.get("cau", []):
            if "band" in c and not args.all:
                continue
            out[_cau_id(f.stem, c)] = {
                "file": f.name, "dang": c.get("dang"), "chuong": c.get("chuong"),
                "do_kho": c.get("do_kho"), "diem": c.get("diem"), "de": c.get("de", ""),
            }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    cur = None
    for cid, c in out.items():
        if c["file"] != cur:
            cur = c["file"]
            print(f"\n### {cur}")
        dang = ",".join(c["dang"] or [])
        print(f"  {cid:<26} [{dang} dk={c['do_kho']} {c['diem']}đ] {c['de']}")
    print(f"\n— {len(out)} câu cần chấm —", file=sys.stderr)
    return 0


def cmd_apply(args) -> int:
    """Đổ phán đoán {id: {band, phut}} vào các đề; gắn cờ _band_auto/_phut_auto."""
    judg = _load(Path(args.judgments))
    for bad in (k for k, v in judg.items() if v.get("band") not in BANDS):
        print(f"✗ band không hợp lệ ở '{bad}': {judg[bad].get('band')}", file=sys.stderr)
        return 1
    seen: set[str] = set()
    n_set = 0
    for f in _exam_files(args.glob):
        d = _load(f)
        changed = False
        for c in d.get("cau", []):
            cid = _cau_id(f.stem, c)
            j = judg.get(cid)
            if not j:
                continue
            seen.add(cid)
            c["band"] = j["band"]
            c["_band_auto"] = True
            if j.get("phut") is not None:
                c["phut"] = round(float(j["phut"]), 1)
                c["_phut_auto"] = True
            changed = True
            n_set += 1
        if changed:
            _save(f, d)
            print(f"  ✓ {f.name}")
    missing = set(judg.keys()) - seen
    print(f"\nĐã gắn {n_set} câu." + (f" KHÔNG thấy id: {sorted(missing)}" if missing else ""))
    return 1 if missing else 0


def cmd_report(args) -> int:
    """Phút/câu THỰC theo band (đối chiếu tier_spec) + độ phủ band/phut."""
    import statistics as st
    from src.schema.tier_spec import load_tier_spec, rates_for
    rates = rates_for(load_tier_spec(), "lop-9", "dai-so")

    by_band: dict[str, list[float]] = {b: [] for b in BANDS}
    n_cau = n_band = n_phut = 0
    for f in _exam_files(args.glob):
        for c in _load(f).get("cau", []):
            n_cau += 1
            if "band" in c:
                n_band += 1
            if c.get("band") in by_band and c.get("phut") is not None:
                n_phut += 1
                by_band[c["band"]].append(float(c["phut"]))

    print(f"Độ phủ: {n_band}/{n_cau} câu có band · {n_phut}/{n_cau} có phut\n")
    print(f"{'band':<5} {'n':>4} {'phút TB thực':>13} {'onclass rate':>13} {'vidu rate':>10}")
    for b in BANDS:
        xs = by_band[b]
        emp = f"{st.mean(xs):.1f}′" if xs else "—"
        on = rates.get("onclass", {}).get(b, "—")
        vd = rates.get("vidu", {}).get(b, "—")
        print(f"{b:<5} {len(xs):>4} {emp:>13} {str(on):>13} {str(vd):>10}")
    print("\n(phút thực = HS làm dưới áp lực thi; rate onclass/vidu là giờ HỌC trên lớp"
          " — onclass ≈ ×1,5 thời gian giải thô. Dùng để soi rate card có hợp lý.)")
    return 0


def cmd_check(args) -> int:
    """Gác cổng ngân hàng đề: Σdiem≠tong_diem, thiếu band/phut, trùng id, band lạ.
    Câu/đề đã gắn cờ `_diem_lech` (Thầy biết, chờ nguồn) chỉ cảnh báo nhẹ."""
    problems = 0
    seen_ids: dict[str, str] = {}
    for f in _exam_files(args.glob):
        d = _load(f)
        xx = d.get("xuat_xu", {})
        td = xx.get("tong_diem")
        cau = d.get("cau", [])
        sdiem = round(sum(c.get("diem", 0) for c in cau), 3)
        if td and abs(sdiem - td) > 1e-6:
            flagged = "_diem_lech" in xx
            tag = "⚠ (đã gắn cờ)" if flagged else "✗"
            print(f"  {tag} {f.name}: Σdiem={sdiem} ≠ tong_diem={td}")
            problems += 0 if flagged else 1
        for c in cau:
            cid = _cau_id(f.stem, c)
            if cid in seen_ids:
                print(f"  ✗ {f.name}: id trùng '{cid}' (đã ở {seen_ids[cid]})")
                problems += 1
            seen_ids[cid] = f.name
            if c.get("band") not in BANDS:
                print(f"  ✗ {f.name}: '{cid}' band lạ/thiếu: {c.get('band')!r}")
                problems += 1
            if c.get("phut") is None:
                print(f"  ✗ {f.name}: '{cid}' thiếu phut")
                problems += 1
    print(f"\n{'✓ Bank sạch.' if problems == 0 else f'✗ {problems} vấn đề chặn.'} "
          f"({len(seen_ids)} câu)")
    return 1 if problems else 0


def cmd_fix_headers(args) -> int:
    """Backfill thoi_gian_phut/tong_diem còn thiếu; cảnh báo Σdiem ≠ tong_diem."""
    for f in _exam_files(args.glob):
        d = _load(f)
        xx = d.setdefault("xuat_xu", {})
        changed = False
        if not xx.get("thoi_gian_phut"):
            xx["thoi_gian_phut"] = DEFAULT_MINUTES
            changed = True
        if not xx.get("tong_diem"):
            xx["tong_diem"] = DEFAULT_POINTS
            changed = True
        sdiem = round(sum(c.get("diem", 0) for c in d.get("cau", [])), 2)
        if sdiem != xx["tong_diem"]:
            print(f"  ⚠ {f.name}: Σdiem={sdiem} ≠ tong_diem={xx['tong_diem']} (kiểm parse)")
        if changed:
            _save(f, d)
            print(f"  ✓ {f.name}: backfill header")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Gắn band/phut cho ngân hàng đề thi.")
    p.add_argument("--glob", default=EXAMS_GLOB, help="Pattern file đề (mặc định lớp 9)")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="In câu chưa có band để chấm")
    e.add_argument("--all", action="store_true", help="Cả câu đã có band")
    e.add_argument("--json", action="store_true", help="Xuất JSON cho công cụ")
    e.set_defaults(func=cmd_extract)

    a = sub.add_parser("apply", help="Đổ phán đoán {id:{band,phut}} từ file JSON")
    a.add_argument("judgments", help="File JSON phán đoán")
    a.set_defaults(func=cmd_apply)

    sub.add_parser("ensure-ids", help="Ghi id (bai+y) cho câu thiếu — chuẩn hoá bank").set_defaults(func=cmd_ensure_ids)
    sub.add_parser("report", help="Phút/câu thực theo band + độ phủ").set_defaults(func=cmd_report)
    sub.add_parser("check", help="Gác cổng bank: Σdiem, band/phut, trùng id").set_defaults(func=cmd_check)
    sub.add_parser("fix-headers", help="Backfill tg/td thiếu").set_defaults(func=cmd_fix_headers)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
