"""Dựng THỬ bản Word cho MỌI phiếu trong kho (không ghi vào outputs/), gom lỗi cổng.

    .venv/bin/python -m scripts.docx_audit_all [--root inputs/seeds] [--jobs 4] [--out DIR]

Chạy trước khi bật Word mặc định cho cả kho (bài học: "không báo lỗi ≠ đúng" — phải
soi trên CHÍNH file kết quả của từng phiếu).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import tempfile
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from config import settings


def one(path: str, out_dir: str) -> tuple[str, list[str]]:
    try:
        from src.compiler.docx_renderer import render_lesson_docx
        from src.main import _load
        from src.validators.docx_gate import check_docx
        lesson = _load(path)
        doc, rep = render_lesson_docx(lesson, Path(path).resolve().parent)
        out = Path(out_dir) / (lesson.slug + ".docx")
        doc.save(out)
        return path, list(rep.issues) + check_docx(out, expect_maths=rep.counts.get("maths"))
    except SystemExit:
        return path, ["không load được JSON"]
    except Exception as e:  # noqa: BLE001
        return path, [f"CRASH {type(e).__name__}: {e}", traceback.format_exc(limit=3)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(settings.ROOT / "inputs" / "seeds"))
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default=tempfile.mkdtemp(prefix="docx_audit_"))
    a = ap.parse_args(argv)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    files = []
    for f in sorted(Path(a.root).rglob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and "stages" in d and "slug" in d:
            files.append(str(f))
    print(f"{len(files)} phiếu → {a.out}", flush=True)
    bad = {}
    kinds = collections.Counter()
    with ProcessPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(one, f, a.out) for f in files]
        for k, fu in enumerate(as_completed(futs), 1):
            p, errs = fu.result()
            if errs:
                bad[p] = errs
                for e in errs:
                    kinds[e.split(":")[0][:60]] += 1
            if k % 20 == 0:
                print(f"  {k}/{len(files)} — lỗi ở {len(bad)} phiếu", flush=True)
    print(f"\nSẠCH {len(files) - len(bad)}/{len(files)}")
    print("\nNhóm lỗi:")
    for k, n in kinds.most_common(30):
        print(f"  {n:4d}  {k}")
    print("\nChi tiết (tối đa 4 lỗi/phiếu):")
    for p, errs in sorted(bad.items()):
        print(f"- {Path(p).relative_to(settings.ROOT)}")
        for e in errs[:4]:
            print(f"    {e[:220]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
