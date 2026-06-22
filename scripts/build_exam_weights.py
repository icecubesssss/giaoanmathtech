"""Sinh file WEIGHT dẫn xuất từ ngân hàng đề (đã gắn band/phut) — "trọng số tần suất".

Tầm nhìn Thầy (2026-06-21): dạng nào HAY RA & NHIỀU ĐIỂM trong đề thi thì đáng được
nhiều giờ ôn hơn. File này gom MỌI đề (GK1+CK1) theo từng kỳ → mỗi chương/dạng có:
  so_de_xuat_hien, ty_le_de(%), so_cau, diem_tb_moi_de, phut_tb, phut_tong, band_dist,
  weight_diem = ty_le_de/100 × diem_tb (kỳ vọng điểm dạng đó đóng góp 1 đề).

KHÔNG sửa tay — chạy lại khi bank đổi:  python -m scripts.build_exam_weights
Ghi ra: inputs/refs/de-thi/lop-9/exam-weights.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from scripts.exam_annotate import EXAMS_GLOB, _exam_files, _load

OUT = Path("inputs/refs/de-thi/lop-9/exam-weights.json")
TAXO = Path("inputs/refs/de-thi/lop-9/taxonomy.json")
BANDS = ("NB", "TH", "VD", "VDC")


def _ky(stem: str) -> str:
    return stem.split("-", 1)[0].upper()  # 'gk1-bat-trang' → 'GK1'


def _agg(rows: list[dict]) -> dict:
    """Gom 1 nhóm record câu (cùng dạng hoặc cùng chương) thành thống kê."""
    de_set = {r["_de"] for r in rows}
    diem_by_de: dict[str, float] = defaultdict(float)
    for r in rows:
        diem_by_de[r["_de"]] += r.get("diem", 0) or 0
    phut = [r["phut"] for r in rows if r.get("phut") is not None]
    band_dist = {b: sum(1 for r in rows if r.get("band") == b) for b in BANDS}
    return {
        "so_de_xuat_hien": len(de_set),
        "so_cau": len(rows),
        "diem_tb_moi_de": round(sum(diem_by_de.values()) / len(de_set), 2) if de_set else 0,
        "phut_tb": round(sum(phut) / len(phut), 1) if phut else None,
        "phut_tong": round(sum(phut), 1) if phut else None,
        "band_dist": band_dist,
    }


def build() -> dict:
    taxo = json.loads(TAXO.read_text(encoding="utf-8")) if TAXO.exists() else {}
    dang_ten = {k: v.get("ten", "") for k, v in taxo.get("dang", {}).items()}
    chuong_ten = taxo.get("chuong", {})

    by_ky_records: dict[str, list[dict]] = defaultdict(list)
    for f in _exam_files(EXAMS_GLOB):
        ky = _ky(f.stem)
        for c in _load(f).get("cau", []):
            for dg in (c.get("dang") or ["?"]):
                by_ky_records[ky].append({**c, "_de": f.stem, "_dang": dg,
                                          "_chuong": c.get("chuong", "?")})

    out_ky = {}
    for ky, recs in sorted(by_ky_records.items()):
        n_de = len({r["_de"] for r in recs})
        # gom theo dạng
        by_dang: dict[str, list[dict]] = defaultdict(list)
        by_chuong: dict[str, list[dict]] = defaultdict(list)
        for r in recs:
            by_dang[r["_dang"]].append(r)
            by_chuong[r["_chuong"]].append(r)

        def _emit(group: dict, name_map: dict) -> dict:
            res = {}
            for key, rows in group.items():
                a = _agg(rows)
                a["ty_le_de"] = round(a["so_de_xuat_hien"] / n_de * 100) if n_de else 0
                a["weight_diem"] = round(a["ty_le_de"] / 100 * a["diem_tb_moi_de"], 2)
                a["ten"] = name_map.get(key, "")
                res[key] = a
            # xếp theo weight_diem giảm dần (dạng đáng giờ nhất lên đầu)
            return dict(sorted(res.items(), key=lambda kv: kv[1]["weight_diem"], reverse=True))

        out_ky[ky] = {
            "so_de": n_de,
            "chuong": _emit(by_chuong, chuong_ten),
            "dang": _emit(by_dang, dang_ten),
        }
    return {
        "_doc": "WEIGHT dẫn xuất từ exams/*.json (đã gắn band/phut). Sinh bởi "
                "scripts/build_exam_weights.py — KHÔNG sửa tay. weight_diem = "
                "ty_le_de/100 × diem_tb_moi_de (kỳ vọng điểm dạng đóng góp 1 đề).",
        "by_ky": out_ky,
    }


def main() -> int:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for ky, blk in data["by_ky"].items():
        top = list(blk["dang"].items())[:3]
        print(f"{ky}: {blk['so_de']} đề · top dạng: "
              + ", ".join(f"{k}({v['weight_diem']})" for k, v in top))
    print(f"→ {OUT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
