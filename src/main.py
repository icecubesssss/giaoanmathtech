"""Điểm chạy CLI trung tâm — MathTech Engine đầy đủ.

Luồng soạn cả năm (xem README.md; luật soạn: HUONG-DAN-SOAN-BAI.md):
    python -m src.main progress  --todo          # còn thiếu bài nào
    python -m src.main new-lesson <folder tuần>  # sinh khung JSON 5 chặng/4 tầng
    # → đổ đề vào các block TODO (Claude điền theo HUONG-DAN-SOAN-BAI.md)
    python -m src.main validate  <file.json>
    python -m src.main validate-all              # gác cổng cả kho
    python -m src.main approve   <slug>
    python -m src.main build     <file.json>     # ra 3 PDF ở outputs/<mon>/<tuan>/

Tiện ích kế hoạch:
    python -m src.main curriculum-sync           # sinh/cập nhật config/curriculum.json
    python -m src.main rebuild                    # build lại hàng loạt (sau khi đổi design_tokens)
    python -m src.main status                    # trạng thái trong run_state.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

from src.schema import LessonPackage, ChapterSummary
from src.compiler import render_handout, render_guide, render_slide, render_summary, build_pdf
from src.validators import (
    sanitize,
    UnsafeLatexError,
    validate_lesson_structure,
    check_difficulty,
    check_ramp,
    find_presentation_warnings,
)
from config import settings

# ── Checkpoint helpers ─────────────────────────────────────────────────────────

STATE_PATH = settings.STORAGE_DIR / "run_state.json"


def _load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print(f"⚠ {STATE_PATH.name} hỏng/không đọc được — khởi tạo lại checkpoint mới.",
                  file=sys.stderr)
    return {"_doc": "checkpoint", "lessons": {}}


def _save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _set_lesson_status(slug: str, status: str, extra: dict | None = None):
    state = _load_state()
    entry = state.setdefault("lessons", {}).setdefault(slug, {})
    entry["status"] = status
    entry["updated_at"] = datetime.now().isoformat(timespec="seconds")
    if extra:
        entry.update(extra)
    _save_state(state)


# ── Shared helper ──────────────────────────────────────────────────────────────

def _load(lesson_path: str) -> LessonPackage:
    path = Path(lesson_path)
    if not path.exists():
        print(f"✗ Không tìm thấy file lesson: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"✗ JSON lesson sai cú pháp ({path}): {e}", file=sys.stderr)
        sys.exit(1)
    return LessonPackage.model_validate(data)


def _out_root(lesson_path: str) -> Path:
    """Output mirror theo cây inputs/seeds: nếu file lesson nằm trong inputs/seeds/...
    thì PDF ra outputs/<đường dẫn tương ứng>/; ngược lại về thẳng OUTPUTS_DIR."""
    seeds = settings.ROOT / "inputs" / "seeds"
    parent = Path(lesson_path).resolve().parent
    try:
        return settings.OUTPUTS_DIR / parent.relative_to(seeds.resolve())
    except ValueError:
        return settings.OUTPUTS_DIR


def _iter_text(lesson: LessonPackage):
    for stage in lesson.stages:
        yield f"stage[{stage.kind}].title", stage.title
        for attr in ("solution", "teacher_note"):
            v = getattr(stage, attr, None)
            if v:
                yield f"stage[{stage.kind}].{attr}", v
        for i, b in enumerate(stage.blocks):
            for attr in ("text", "latex", "statement", "caption", "tikz", "image"):
                v = getattr(b, attr, None)
                if v:
                    yield f"stage[{stage.kind}].block[{i}].{attr}", v
            # Ô bảng (TableBlock) cũng phải qua sanitizer.
            if getattr(b, "type", "") == "table":
                for h in getattr(b, "headers", []) or []:
                    if h:
                        yield f"stage[{stage.kind}].block[{i}].header", h
                for r, row in enumerate(getattr(b, "rows", []) or []):
                    for c, cell in enumerate(row):
                        if cell:
                            yield f"stage[{stage.kind}].block[{i}].cell[{r}][{c}]", cell


# ── Curriculum / cây tuần helpers ───────────────────────────────────────────────

SEEDS_DIR = settings.ROOT / "inputs" / "seeds"
CURRICULUM_PATH = settings.CONFIG_DIR / "curriculum.json"
SUBJECT_LABELS = {"dai-so": "ĐẠI SỐ", "hinh-hoc": "HÌNH HỌC"}
GRADE_LABELS = {"lop-9": "Lớp 9 • Ôn vào 10"}
_BUILD_KINDS = ("handout", "guide", "slide")


def _grade_label(grade_slug: str) -> str:
    """`lop-9` → 'Lớp 9 • Ôn vào 10' (đặc thù), `lop-8` → 'Lớp 8' (suy từ số)."""
    if grade_slug in GRADE_LABELS:
        return GRADE_LABELS[grade_slug]
    m = re.match(r"lop-?(\d+)", grade_slug)
    return f"Lớp {m.group(1)}" if m else "Lớp 9 • Ôn vào 10"


def _week_nums(folder_name: str) -> list[int]:
    """`tuan10-11-...` → [10, 11]; trả [] nếu không khớp tiền tố tuần."""
    m = re.match(r"tuan(\d+(?:-\d+)*)", folder_name)
    return [int(x) for x in m.group(1).split("-")] if m else []


def _topic_slug(folder_name: str) -> str:
    """Bỏ tiền tố `tuanNN[-NN]-` để lấy phần chủ đề."""
    return re.sub(r"^tuan\d+(?:-\d+)*-", "", folder_name)


def _week_folders(subject_dir: Path) -> list[Path]:
    return sorted(
        (d for d in subject_dir.iterdir() if d.is_dir()),
        key=lambda d: (_week_nums(d.name) or [999], d.name),
    )


def _is_summary_json(json_path: Path) -> bool:
    """Phân biệt file ChapterSummary (phiếu tổng kết) với lesson thường: có khóa
    'mindmap' ở cấp cao nhất và không có 'stages'."""
    try:
        d = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return isinstance(d, dict) and "mindmap" in d and "stages" not in d


def _build_status(json_path: Path) -> dict:
    """Đọc slug từ lesson JSON, soi outputs mirror xem 3 bản PDF đã build chưa."""
    try:
        slug = json.loads(json_path.read_text(encoding="utf-8")).get("slug", "")
    except (json.JSONDecodeError, OSError):
        return {"slug": "?", "ok_json": False, "pdfs": {}}
    try:
        rel = json_path.resolve().parent.relative_to(SEEDS_DIR.resolve())
    except ValueError:
        rel = Path()
    out_dir = settings.OUTPUTS_DIR / rel / slug
    pdfs = {fn: (out_dir / f"{fn}.pdf").exists() for fn in _BUILD_KINDS}
    return {"slug": slug, "ok_json": True, "pdfs": pdfs}


# ── S4 commands ────────────────────────────────────────────────────────────────

def cmd_approve(args: argparse.Namespace) -> int:
    """Đánh dấu APPROVE để mở khoá compile PDF."""
    slug = args.slug
    state = _load_state()
    entry = state.get("lessons", {}).get(slug, {})

    if entry.get("status") not in ("woven", "validated"):
        print(f"✗ Bài '{slug}' chưa ở trạng thái 'woven' hoặc 'validated' (hiện: {entry.get('status', 'chưa có')})", file=sys.stderr)
        return 1

    _set_lesson_status(slug, "approved")
    print(f"✓ '{slug}' đã được APPROVE. Bước tiếp: python -m src.main build <lesson.json>")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Xem tình trạng tất cả bài trong run_state.json."""
    state = _load_state()
    lessons = state.get("lessons", {})
    if not lessons:
        print("(Chưa có bài nào được theo dõi. Bắt đầu bằng lệnh `new-lesson`.)")
        return 0
    print(f"{'SLUG':<30} {'STATUS':<15} {'CẬP NHẬT'}")
    print("─" * 65)
    for slug, info in lessons.items():
        print(f"{slug:<30} {info.get('status','?'):<15} {info.get('updated_at','')}")
    return 0


def cmd_evolve(args: argparse.Namespace) -> int:
    """Đọc active_feedback.md và tiến hóa style/prompt có kiểm soát."""
    from src.agents.feedback_parser import parse_feedback
    from src.agents.evolution_engine import evolve_from_feedback

    fb_path = Path(args.feedback)
    if not fb_path.exists():
        print(f"✗ Không tìm thấy file phản hồi: {fb_path}", file=sys.stderr)
        return 1

    print(f"▶ Đọc phản hồi từ {fb_path} …")
    feedback = parse_feedback(fb_path)

    if feedback.is_empty():
        print("  (Không có nhận xét mới để áp dụng.)")
        return 0

    result = evolve_from_feedback(feedback)
    print(f"  • Snapshot đã lưu trước khi sửa.")
    if result["applied_changes"]:
        for change in result["applied_changes"]:
            print(f"  ✓ {change}")
    else:
        print("  (Không có quy tắc nào thay đổi.)")
    return 0


# ── S2/S3 commands (giữ nguyên từ trước) ──────────────────────────────────────

def cmd_build_handout(args: argparse.Namespace) -> int:
    lesson = _load(args.lesson)
    pdf = build_pdf(render_handout(lesson), slug=lesson.slug, filename="handout", out_root=_out_root(args.lesson))
    print(f"OK → {pdf}")
    return 0


def cmd_build_guide(args: argparse.Namespace) -> int:
    lesson = _load(args.lesson)
    pdf = build_pdf(render_guide(lesson), slug=lesson.slug, filename="guide", out_root=_out_root(args.lesson))
    print(f"OK → {pdf}")
    return 0


def cmd_build_slide(args: argparse.Namespace) -> int:
    lesson = _load(args.lesson)
    pdf = build_pdf(render_slide(lesson), slug=lesson.slug, filename="slide", out_root=_out_root(args.lesson))
    print(f"OK → {pdf}")
    return 0


def cmd_build_all(args: argparse.Namespace) -> int:
    """Sinh đồng thời cả 3 bản từ cùng một gói bài."""
    lesson = _load(args.lesson)
    out_root = _out_root(args.lesson)
    for fn, render in (("handout", render_handout), ("guide", render_guide), ("slide", render_slide)):
        pdf = build_pdf(render(lesson), slug=lesson.slug, filename=fn, out_root=out_root)
        print(f"OK → {pdf}")
    _set_lesson_status(lesson.slug, "built")
    return 0


def cmd_build_summary(args: argparse.Namespace) -> int:
    """Sinh phiếu TỔNG KẾT CHƯƠNG 1 trang: bản HS (sơ đồ trống) + bản GV (có đáp án)."""
    data = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    summary = ChapterSummary.model_validate(data)
    out_root = _out_root(args.summary)
    pdf = build_pdf(render_summary(summary, show_solution=False), slug=summary.slug,
                    filename="tongket-hs", out_root=out_root)
    print(f"OK → {pdf}")
    pdf = build_pdf(render_summary(summary, show_solution=True), slug=summary.slug,
                    filename="tongket-gv", out_root=out_root)
    print(f"OK → {pdf}")
    return 0


def _run_validation(lesson: LessonPackage) -> tuple[list[str], list[str], list[str]]:
    """Chạy toàn bộ trọng tài S2 trên 1 gói bài. Trả về (vi phạm chặn, cảnh báo
    trình bày, cảnh báo độ dốc). Dùng chung cho `validate` lẫn `validate-all`."""
    violations: list[str] = []
    for loc, text in _iter_text(lesson):
        try:
            sanitize(text)
        except UnsafeLatexError as e:
            violations.append(f"[latex_sanitizer] {loc}: {e}")

    sch = validate_lesson_structure(lesson)
    for e in sch.errors:
        violations.append(f"[schema_validator] {e}")

    diff = check_difficulty(lesson)
    for r in diff.reasons:
        violations.append(f"[difficulty_gate] {r}")

    warns = find_presentation_warnings(lesson)
    ramp_warns = check_ramp(lesson)
    return violations, warns, ramp_warns


def cmd_validate(args: argparse.Namespace) -> int:
    lesson = _load(args.lesson)
    print(f"▶ Đang trọng tài '{lesson.slug}' — {lesson.title}")
    violations, warns, ramp_warns = _run_validation(lesson)

    n_unsafe = sum(1 for v in violations if v.startswith("[latex_sanitizer]"))
    n_schema = sum(1 for v in violations if v.startswith("[schema_validator]"))
    n_diff = sum(1 for v in violations if v.startswith("[difficulty_gate]"))
    print(f"  • latex_sanitizer:  {'OK' if n_unsafe == 0 else f'{n_unsafe} vi phạm'}")
    print(f"  • schema_validator: {'OK' if n_schema == 0 else f'{n_schema} lỗi'}")
    print(f"  • difficulty_gate:  {'OK' if n_diff == 0 else f'{n_diff} lý do từ chối'}")
    print(f"  • visual_linter:    {'OK' if not warns else f'{len(warns)} cảnh báo trình bày'}")
    for w in warns:
        print(f"    ⚠ {w}")
    print(f"  • gradient_gate:    {'OK' if not ramp_warns else f'{len(ramp_warns)} cảnh báo độ dốc'}")
    for w in ramp_warns:
        print(f"    ⚠ {w}")

    if violations:
        print("\n✗ TỪ CHỐI — vi phạm cần dệt lại:")
        for v in violations:
            print(f"  {v}")
        _set_lesson_status(lesson.slug, "validation_failed")
        return 1

    _set_lesson_status(lesson.slug, "validated")
    print("\n✓ Gói bài qua cổng S2. Bước kế tiếp: approve → build")
    return 0


def _is_lesson_json(json_path: Path) -> bool:
    """Lesson thường: có 'stages' ở cấp cao nhất (phân biệt với phiếu tổng kết /
    file metadata chương trình)."""
    try:
        d = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return isinstance(d, dict) and "stages" in d


def _iter_lesson_files(grade: str | None, subject: str | None):
    """Duyệt mọi file lesson JSON dưới inputs/seeds (bỏ chuong-trinh-hoc, bỏ tổng kết
    & metadata). Trả về Path, lọc theo --grade/--subject nếu có."""
    if not SEEDS_DIR.exists():
        return
    for j in sorted(SEEDS_DIR.rglob("*.json")):
        rel = j.resolve().relative_to(SEEDS_DIR.resolve())
        if "chuong-trinh-hoc" in rel.parts or not _is_lesson_json(j):
            continue
        g = rel.parts[0] if len(rel.parts) >= 1 else ""
        s = rel.parts[1] if len(rel.parts) >= 2 else ""
        if grade and g != grade:
            continue
        if subject and s != subject:
            continue
        yield j


def cmd_validate_all(args: argparse.Namespace) -> int:
    """Chạy trọng tài S2 trên TẤT CẢ lesson JSON — gác cổng cả kho trước khi build/commit."""
    files = list(_iter_lesson_files(args.grade, args.subject))
    if not files:
        print("(Không thấy lesson JSON nào khớp bộ lọc.)")
        return 0

    n_fail = n_warn = 0
    for j in files:
        try:
            lesson = LessonPackage.model_validate(json.loads(j.read_text(encoding="utf-8")))
        except Exception as e:  # noqa: BLE001 — báo file hỏng, không dừng cả mẻ
            n_fail += 1
            print(f"  ✗ {j.name:<40} [KHÔNG LOAD ĐƯỢC] {e}")
            continue
        violations, warns, ramp_warns = _run_validation(lesson)
        nw = len(warns) + len(ramp_warns)
        if violations:
            n_fail += 1
            print(f"  ✗ {lesson.slug:<40} {len(violations)} vi phạm")
            for v in violations:
                print(f"        {v}")
        else:
            if nw:
                n_warn += 1
            tag = "OK" if not nw else f"OK ({nw} cảnh báo)"
            print(f"  ✓ {lesson.slug:<40} {tag}")

    print(f"\n{'─'*60}")
    print(f"Tổng: {len(files)} bài | {len(files) - n_fail} qua | {n_fail} TỪ CHỐI | {n_warn} có cảnh báo")
    return 1 if n_fail else 0


def cmd_rebuild(args: argparse.Namespace) -> int:
    """Build LẠI mọi bài ĐÃ CÓ output (đủ 3 PDF) — để lan thay đổi design_tokens /
    template ra toàn bộ phiếu, không sót. Dùng --all để build cả bài chưa từng build."""
    files = list(_iter_lesson_files(args.grade, args.subject))
    if not files:
        print("(Không thấy lesson JSON nào khớp bộ lọc.)")
        return 0

    n_ok = n_skip = n_err = 0
    for j in files:
        status = _build_status(j)
        if not args.all and not (status["ok_json"] and all(status["pdfs"].values())):
            n_skip += 1
            continue
        try:
            lesson = _load(str(j))
            out_root = _out_root(str(j))
            for fn, render in (("handout", render_handout), ("guide", render_guide), ("slide", render_slide)):
                build_pdf(render(lesson), slug=lesson.slug, filename=fn, out_root=out_root)
            _set_lesson_status(lesson.slug, "built")
            n_ok += 1
            print(f"  ✓ {lesson.slug}")
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001 — 1 bài lỗi không chặn cả mẻ
            n_err += 1
            print(f"  ✗ {j.name}: {e}")

    print(f"\n{'─'*60}")
    print(f"Rebuild: {n_ok} bài OK | {n_skip} bỏ qua (chưa từng build) | {n_err} lỗi")
    return 1 if n_err else 0


# ── Curriculum / progress / scaffold commands ───────────────────────────────────

def _load_curriculum_meta() -> dict:
    """Đọc curriculum.json → {folder: row}, chấp nhận cả schema cũ (`subjects`)
    lẫn mới (`grades` → `subjects`). Dùng để giữ metadata Thầy điền tay khi sync."""
    meta: dict = {}
    if not CURRICULUM_PATH.exists():
        return meta
    try:
        data = json.loads(CURRICULUM_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return meta
    subject_blocks = (
        [s for g in data["grades"].values() for s in g.values()]
        if "grades" in data
        else list(data.get("subjects", {}).values())
    )
    for rows in subject_blocks:
        for wk in rows:
            meta[wk.get("folder", "")] = wk
    return meta


def _scan_tree() -> dict:
    """Quét inputs/seeds/<lớp>/<môn>/<tuần>/ → {grade: {subject: [ {folder, weeks,
    topic, has_source_pdf, lessons:[{file, slug, ok_json, pdfs}]} ]}}.
    Bỏ folder chuong-trinh-hoc (ở cấp môn)."""
    tree: dict = {}
    if not SEEDS_DIR.exists():
        return tree
    for grade_dir in sorted(d for d in SEEDS_DIR.iterdir() if d.is_dir()):
        subjects: dict = {}
        for subject_dir in sorted(d for d in grade_dir.iterdir() if d.is_dir()):
            if subject_dir.name == "chuong-trinh-hoc":
                continue
            weeks = []
            for wf in _week_folders(subject_dir):
                lessons = [
                    {"file": j.name, **_build_status(j)}
                    for j in sorted(wf.glob("*.json")) if not _is_summary_json(j)
                ]
                weeks.append({
                    "folder": wf.name,
                    "weeks": _week_nums(wf.name),
                    "topic": _topic_slug(wf.name),
                    "has_source_pdf": any(wf.glob("*.pdf")),
                    "lessons": lessons,
                })
            subjects[subject_dir.name] = weeks
        tree[grade_dir.name] = subjects
    return tree


def cmd_curriculum_sync(args: argparse.Namespace) -> int:
    """Sinh/cập nhật config/curriculum.json từ cây tuần — giữ lại metadata Thầy
    đã điền tay (deadline, duration_hours, target_lessons, note) theo folder."""
    old = _load_curriculum_meta()

    tree = _scan_tree()
    manifest = {
        "_doc": "Manifest chương trình — sinh tự động từ inputs/seeds bởi `curriculum-sync`. "
                "Cấu trúc: grades → subjects → tuần. "
                "Các trường deadline/duration_hours/target_lessons/note được giữ nguyên khi sync lại; "
                "Thầy điền tay vào đây.",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "grades": {},
    }
    n_weeks = n_subjects = 0
    for grade, subjects in tree.items():
        grade_block: dict = {}
        for subject, weeks in subjects.items():
            rows = []
            for wk in weeks:
                prev = old.get(wk["folder"], {})
                rows.append({
                    "folder": wk["folder"],
                    "weeks": wk["weeks"],
                    "topic": wk["topic"],
                    "deadline": prev.get("deadline"),
                    "duration_hours": prev.get("duration_hours"),
                    "target_lessons": prev.get("target_lessons"),
                    "note": prev.get("note", ""),
                })
                n_weeks += 1
            grade_block[subject] = rows
            n_subjects += 1
        manifest["grades"][grade] = grade_block

    CURRICULUM_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"✓ Manifest → {CURRICULUM_PATH}  ({len(tree)} lớp, {n_subjects} môn, {n_weeks} tuần)")
    print("  Mở file để điền deadline/duration_hours/target_lessons cho từng tuần.")
    return 0


def cmd_progress(args: argparse.Namespace) -> int:
    """Quét sống cây tuần, báo trạng thái: PDF nguồn? lesson JSON? đã build chưa?"""
    tree = _scan_tree()
    if not tree:
        print("(Chưa có cây seeds. Tạo inputs/seeds/<lớp>/<mon>/tuanNN-<chu-de>/ trước.)")
        return 0

    meta = _load_curriculum_meta()

    tot = dict(weeks=0, src=0, json=0, built=0)
    for grade, subjects in tree.items():
        if args.grade and args.grade != grade:
            continue
        print(f"\n{'═'*60}\n{_grade_label(grade)}  [{grade}]")
        for subject, weeks in subjects.items():
            if args.subject and args.subject != subject:
                continue
            print(f"\n{SUBJECT_LABELS.get(subject, subject.upper())}")
            for wk in weeks:
                tot["weeks"] += 1
                has_src = wk["has_source_pdf"]
                lessons = wk["lessons"]
                n_built = sum(1 for l in lessons if l["ok_json"] and all(l["pdfs"].values()))
                if has_src:
                    tot["src"] += 1
                if lessons:
                    tot["json"] += 1
                if lessons and n_built == len(lessons):
                    tot["built"] += 1

                done = bool(lessons) and n_built == len(lessons)
                if args.todo and done:
                    continue

                src_tag = "PDF✓" if has_src else "PDF✗"
                md = meta.get(wk["folder"], {})
                extra = ""
                if md.get("deadline"):
                    extra += f"  ⏰{md['deadline']}"
                if md.get("duration_hours"):
                    extra += f"  {md['duration_hours']}h"
                print(f"  {wk['folder']:<42} [{src_tag}] {len(lessons)} bài{extra}")
                for l in lessons:
                    if not l["ok_json"]:
                        print(f"      • {l['file']:<36} [JSON LỖI]")
                        continue
                    b = l["pdfs"]
                    btag = " ".join(f"{k}{'✓' if v else '✗'}" for k, v in b.items())
                    print(f"      • {l['slug']:<36} [build: {btag}]")

    print(f"\n{'─'*60}")
    print(f"Tổng: {tot['weeks']} tuần | {tot['src']} có nguồn | "
          f"{tot['json']} có JSON | {tot['built']} build xong cả phiếu")
    if not CURRICULUM_PATH.exists():
        print("Gợi ý: chạy `python -m src.main curriculum-sync` để có manifest + deadline.")
    return 0


def _skeleton(slug: str, title: str, eyebrow: str, grade: str) -> dict:
    """Khung 5 chặng map 4 tầng: concept=Ví dụ mẫu, practice1/2=BT trên lớp,
    reflection=BTVN + Bài tập mở rộng. Đánh số bài LIỀN MẠCH cả phiếu khi điền."""
    def stage(kind, number, title, blocks, solution="", note=""):
        return {"kind": kind, "number": number, "title": title,
                "blocks": blocks, "solution": solution, "teacher_note": note}

    return {
        "slug": slug,
        "title": title,
        "eyebrow": eyebrow,
        "grade_label": grade,
        "stages": [
            stage("review", 1, "Khám phá — KTBC / nhịp cầu vào bài", [
                # MỞ MÀN THỰC TẾ (đặc sản): hook đời thực kéo HS vào bài. Xoá nếu bài
                # thuần kỹ thuật không hợp. Thêm "tikz":"\\begin{tikzpicture}…" để có TRANH
                # MINH HOẠ nét vẽ ở cột phải (vd vòi nước/thuyền/thang) — ưu tiên hơn "image".
                {"type": "opener", "text": "TODO: MỞ MÀN THỰC TẾ — một tình huống/bài toán đời thực hấp dẫn dẫn vào bài (vd hai vòi nước, quãng đường đi học, lãi suất…)."},
                {"type": "para", "text": "TODO: ôn nhanh kiến thức nền sẽ dùng + 1 worked example GV làm mẫu trọn vẹn (đừng nhảy thẳng sang lý thuyết mới)."},
                {"type": "noted", "text": "TODO: các sự thật nền, tách ý bằng [[br]]; chỗ HS điền dùng [[blank:3cm]] hoặc [[mblank:0.8cm]]."},
            ], solution="TODO: đáp án phần ôn.", note="TODO: mẹo điều phối 3–5 phút."),
            stage("concept", 2, "Khái niệm — kèm Ví dụ mẫu", [
                {"type": "noted", "text": "\\textbf{Khái niệm.} TODO: phát biểu khái niệm/định lí trọng tâm."},
                {"type": "noted", "variant": "example", "text": "TODO: 1–2 ví dụ GV làm mẫu cùng kỹ thuật với bài luyện tập (KHÔNG ghi chú \"GV\" trong block HS)."},
                # Thẻ callout có nhãn màu: variant "trap" = bẫy điểm; "target" = đích thi.
                {"type": "noted", "variant": "trap", "text": "TODO: BẪY ĐIỂM — lỗi HS hay mất điểm oan ở dạng này (vd quên ĐKXĐ, quên dấu, quên loại nghiệm)."},
                {"type": "noted", "variant": "target", "text": "TODO: ĐÍCH THI VÀO 10 — kỹ thuật này tái xuất ở câu nào của đề vào 10; mục tiêu buổi học."},
            ], solution="TODO: lời giải đầy đủ ví dụ mẫu.", note="TODO: trọng tâm buổi học, lỗi sai phổ biến."),
            stage("practice1", 3, "Luyện tập 1 — BÀI TẬP TRÊN LỚP (nền)", [
                {"type": "problem", "label": "Bài 1.", "statement": "TODO: bài nền, dạng cơ bản từ nguồn.", "tier": "onclass"},
                {"type": "para", "text": "TODO: chỗ trống cho HS [[blank:3cm]], nhiều ý a)b)c) tách bằng [[br]]."},
            ], solution="TODO: lời giải Bài 1…", note="TODO: phần nền, làm nhanh."),
            stage("practice2", 4, "Luyện tập 2 — BÀI TẬP TRÊN LỚP (vận dụng, trọng tâm thi)", [
                {"type": "para", "text": "\\textbf{Ví dụ mẫu.} TODO: nhịp cầu trước khi HS tự làm bài khó hơn."},
                {"type": "problem", "label": "Bài 2.", "statement": "TODO: bài vận dụng, mức CHẠM TRẦN độ khó vào 10 (theo difficulty_gate).", "tier": "onclass"},
            ], solution="TODO: lời giải đầy đủ Bài 2…", note="TODO: kỹ thuật mới so với Luyện tập 1."),
            # Chặng 5 = TỔNG KẾT (tóm tắt + sơ đồ tư duy). BTVN & Mở rộng tự tách
            # thành 2 MỤC RIÊNG nhờ tier (renderer.split_reflection) — không cần
            # tự đặt tiêu đề mục, chỉ cần gắn tier="btvn"/"extend".
            stage("reflection", 5, "Tổng kết", [
                {"type": "para", "text": "TODO: tóm tắt 1–2 câu vũ khí/kỹ thuật chính của buổi."},
                # --- Sơ đồ tư duy điền khuyết (thuộc Tổng kết): thay ô tự chấm nhàm. ---
                {"type": "mindmap", "caption": "Sơ đồ tư duy — em điền các ô trống để chốt kiến thức bài học",
                 "root": "TODO: chủ đề bài",
                 "branches": [
                     {"label": "TODO: nhánh 1 (vd Khái niệm) [[blank:2.5cm]]",
                      "children": [{"label": "[[blank:2cm]]"}]},
                     {"label": "TODO: nhánh 2 (vd Kỹ thuật chính) [[blank:2.5cm]]",
                      "children": [{"label": "TODO: bước 1"}, {"label": "[[blank:2cm]]"}]},
                     {"label": "TODO: nhánh 3 (vd Dấu \"=\" / điều kiện) [[blank:2.5cm]]"},
                 ]},
                # --- Mục BÀI TẬP VỀ NHÀ (gắn tier="btvn"). ---
                {"type": "problem", "label": "Bài 3.", "statement": "TODO: BTVN cùng kiểu (BẮT BUỘC có lời giải đầy đủ trong solution).", "tier": "btvn"},
                # --- Mục BÀI TẬP MỞ RỘNG = THANG 2–3 bậc (đừng để 1 bài dốc đứng). ---
                {"type": "para", "text": "\\textbf{Nhịp cầu.} TODO: chỉ rõ kỹ thuật mới ở mở rộng khác bài trên lớp ở đâu (vd: 2 biến đã quen, lên 3 biến cần tổng ba bình phương)."},
                {"type": "problem", "label": "Bài 4.", "statement": "TODO: mở rộng bậc 1 — biến thể Bài 2 thêm 1 yếu tố.", "tier": "extend",
                 "hints": ["TODO: gợi ý định hướng (KHÔNG lộ lời giải).", "TODO: gợi ý thứ 2 nếu vẫn bí."]},
                {"type": "problem", "label": "Bài 5.", "statement": "TODO: mở rộng bậc 2 — nâng cao nhất, vẫn không vượt tầm vào 10.", "tier": "extend",
                 # QR video lời giải (DÀNH BẢN THƯƠNG MẠI): thêm "video":"https://…" vào
                 # problem để in QR cạnh bài. Mặc định KHÔNG bật (bản hiện tại bỏ QR).
                 "hints": ["TODO: gợi ý mở dần cho bài khó nhất."]},
            ], solution="TODO: LỜI GIẢI ĐẦY ĐỦ mọi bài BTVN + mở rộng (để GV ứng phó HS giỏi) + ĐÁP ÁN các ô trống của sơ đồ tư duy.",
               note="TODO: gợi ý chữa BTVN buổi sau; chốt sơ đồ tư duy cùng HS."),
        ],
    }


def cmd_new_lesson(args: argparse.Namespace) -> int:
    """Sinh khung lesson JSON 5 chặng/4 tầng trong folder tuần để đổ đề vào."""
    folder = Path(args.folder)
    if not folder.exists() or not folder.is_dir():
        print(f"✗ Không thấy folder: {folder}", file=sys.stderr)
        return 1

    topic = _topic_slug(folder.name)
    slug = args.slug or topic or folder.name
    out_path = folder / f"{slug}.json"
    if out_path.exists() and not args.force:
        print(f"✗ Đã tồn tại {out_path} — dùng --force để ghi đè.", file=sys.stderr)
        return 1

    # Suy ra eyebrow/grade từ vị trí folder dưới seeds (<lớp>/<môn>/<tuần>).
    grade = subject = ""
    try:
        rel = folder.resolve().relative_to(SEEDS_DIR.resolve())
        grade = rel.parts[0] if rel.parts else ""
        subject = rel.parts[1] if len(rel.parts) >= 2 else ""
    except ValueError:
        pass
    subj_label = SUBJECT_LABELS.get(subject, "")
    title = args.title or topic.replace("-", " ").strip().capitalize() or slug
    eyebrow = f"CHỦ ĐỀ • {subj_label}".rstrip(" •") if subj_label else "CHỦ ĐỀ"

    skeleton = _skeleton(slug, title, eyebrow, _grade_label(grade))
    out_path.write_text(
        json.dumps(skeleton, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    srcs = [p.name for p in folder.glob("*.pdf")]
    print(f"✓ Khung bài → {out_path}")
    if srcs:
        print(f"  Nguồn trong folder: {', '.join(srcs)}")
    print("  Đổ đề vào các block TODO, rồi: "
          f"validate → approve → build {out_path}")
    return 0


def _summary_skeleton(slug: str, title: str, eyebrow: str, grade: str, lessons: list[str]) -> dict:
    """Khung ChapterSummary: sơ đồ tư duy TO gom cả chương, đầy nút TODO để điền."""
    return {
        "slug": slug,
        "title": title,
        "eyebrow": eyebrow,
        "grade_label": grade,
        "intro": "TODO: 1–2 câu chốt mạch kiến thức cả chương (cho HS hệ thống lại).",
        "lessons": lessons,
        "mindmap": {
            "type": "mindmap",
            "size": "large",
            "caption": "Sơ đồ tư duy TỔNG KẾT CHƯƠNG — em điền các ô trống để nối các phiếu lại",
            "root": "TODO: tên chương",
            "branches": [
                {"label": "TODO: nhánh từ Phiếu 1 [[blank:2.5cm]]",
                 "children": [{"label": "TODO: ý chính"}, {"label": "[[blank:2cm]]"}]},
                {"label": "TODO: nhánh từ Phiếu 2 [[blank:2.5cm]]",
                 "children": [{"label": "TODO: ý chính"}, {"label": "[[blank:2cm]]"}]},
                {"label": "TODO: cầu nối / đích thi vào 10 [[blank:2.5cm]]"},
            ],
        },
        "solution": "TODO: ĐÁP ÁN đầy đủ mọi ô trống của sơ đồ (mỗi ý một dòng [[br]]).",
    }


def cmd_new_summary(args: argparse.Namespace) -> int:
    """Sinh khung phiếu TỔNG KẾT CHƯƠNG. Một chương = NHIỀU tuần (mỗi tuần 1 bài,
    xem cột 'Nội dung đưa cho HS' của tiến độ); truyền TẤT CẢ folder tuần của chương
    để gom phiếu thành viên. File tổng kết đặt ở cấp môn (cha chung) khi >1 tuần."""
    folders = [Path(f) for f in args.folders]
    for folder in folders:
        if not folder.exists() or not folder.is_dir():
            print(f"✗ Không thấy folder: {folder}", file=sys.stderr)
            return 1

    # Nhiều tuần → đặt ở thư mục cha chung (cấp môn); một tuần → chính folder đó.
    base = folders[0] if len(folders) == 1 else folders[0].parent
    if args.slug:
        slug = args.slug
    elif len(folders) == 1:
        slug = f"tong-ket-{_topic_slug(folders[0].name) or folders[0].name}"
    else:
        slug = "tong-ket-chuong"
    out_path = base / f"{slug}.json"
    if out_path.exists() and not args.force:
        print(f"✗ Đã tồn tại {out_path} — dùng --force để ghi đè.", file=sys.stderr)
        return 1

    grade = subject = ""
    try:
        rel = base.resolve().relative_to(SEEDS_DIR.resolve())
        grade = rel.parts[0] if rel.parts else ""
        subject = rel.parts[1] if len(rel.parts) >= 2 else ""
    except ValueError:
        pass
    eyebrow = SUBJECT_LABELS.get(subject, "")
    title = args.title or slug.replace("tong-ket-", "").replace("-", " ").strip().capitalize() or slug

    # Gom phiếu thành viên qua TẤT CẢ folder tuần (bỏ file tổng kết).
    members = []
    for folder in folders:
        for j in sorted(folder.glob("*.json")):
            if _is_summary_json(j) or j.resolve() == out_path.resolve():
                continue
            try:
                members.append(json.loads(j.read_text(encoding="utf-8")).get("slug", j.stem))
            except Exception:
                members.append(j.stem)

    skeleton = _summary_skeleton(slug, title, eyebrow, _grade_label(grade), members)
    out_path.write_text(json.dumps(skeleton, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Khung phiếu tổng kết → {out_path}")
    print(f"  {len(folders)} tuần → phiếu thành viên: {', '.join(members) if members else '(chưa có)'}")
    if not args.slug and len(folders) > 1:
        print("  ⚠ Nên đặt --slug --title cho chương (vd --slug tong-ket-bdt-bpt).")
    print(f"  Điền sơ đồ rồi: build-summary {out_path}")
    return 0


# ── Main ───────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="mathtech",
        description="MathTech Engine — Hệ thống soạn phiếu học tập tự động"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # Soạn bài (human-in-the-loop)
    ap = sub.add_parser("approve", help="Đánh dấu APPROVE để mở khoá compile")
    ap.add_argument("slug", help="Mã bài học cần duyệt")
    ap.set_defaults(func=cmd_approve)

    st = sub.add_parser("status", help="Xem trạng thái tất cả bài trong run_state.json")
    st.set_defaults(func=cmd_status)

    ev = sub.add_parser("evolve", help="Áp dụng phản hồi của Thầy để tiến hóa style/prompt")
    ev.add_argument("feedback", nargs="?", default="feedback/active_feedback.md")
    ev.set_defaults(func=cmd_evolve)

    # S3 commands
    b = sub.add_parser("build-handout", help="Render + compile phiếu HS từ file lesson JSON")
    b.add_argument("lesson", help="Đường dẫn file lesson .json")
    b.set_defaults(func=cmd_build_handout)

    g = sub.add_parser("build-guide", help="Render + compile Sổ tay GV (có đáp án + mẹo)")
    g.add_argument("lesson", help="Đường dẫn file lesson .json")
    g.set_defaults(func=cmd_build_guide)

    s = sub.add_parser("build-slide", help="Render + compile Slide TV (Beamer 16:9)")
    s.add_argument("lesson", help="Đường dẫn file lesson .json")
    s.set_defaults(func=cmd_build_slide)

    a = sub.add_parser("build", help="Sinh đồng thời cả 3 bản (handout, guide, slide)")
    a.add_argument("lesson", help="Đường dẫn file lesson .json")
    a.set_defaults(func=cmd_build_all)

    bs = sub.add_parser("build-summary", help="Render phiếu TỔNG KẾT CHƯƠNG 1 trang (bản HS + GV)")
    bs.add_argument("summary", help="Đường dẫn file ChapterSummary .json")
    bs.set_defaults(func=cmd_build_summary)

    # S2 command
    v = sub.add_parser("validate", help="Chạy trọng tài S2: sanitizer + schema + difficulty_gate")
    v.add_argument("lesson", help="Đường dẫn file lesson .json")
    v.set_defaults(func=cmd_validate)

    va = sub.add_parser("validate-all", help="Chạy trọng tài S2 trên TẤT CẢ lesson JSON (gác cổng cả kho)")
    va.add_argument("--grade", help="Lọc theo lớp (vd lop-9)")
    va.add_argument("--subject", help="Lọc theo môn (vd dai-so, hinh-hoc)")
    va.set_defaults(func=cmd_validate_all)

    rb = sub.add_parser("rebuild", help="Build LẠI mọi bài đã có output (lan thay đổi design_tokens/template)")
    rb.add_argument("--grade", help="Lọc theo lớp (vd lop-9)")
    rb.add_argument("--subject", help="Lọc theo môn (vd dai-so, hinh-hoc)")
    rb.add_argument("--all", action="store_true", help="Build cả bài CHƯA từng build (không chỉ bài đã có PDF)")
    rb.set_defaults(func=cmd_rebuild)

    # Curriculum / kế hoạch cả năm
    cs = sub.add_parser("curriculum-sync", help="Sinh/cập nhật config/curriculum.json từ cây tuần")
    cs.set_defaults(func=cmd_curriculum_sync)

    pr = sub.add_parser("progress", help="Báo trạng thái từng tuần: PDF nguồn / JSON / build")
    pr.add_argument("--grade", help="Lọc theo lớp (vd lop-9, lop-8)")
    pr.add_argument("--subject", help="Lọc theo môn (vd dai-so, hinh-hoc)")
    pr.add_argument("--todo", action="store_true", help="Chỉ hiện tuần CHƯA build xong")
    pr.set_defaults(func=cmd_progress)

    nl = sub.add_parser("new-lesson", help="Sinh khung lesson JSON 5 chặng/4 tầng vào folder tuần")
    nl.add_argument("folder", help="Folder tuần dưới inputs/seeds/<lop>/<mon>/")
    nl.add_argument("--slug", help="Mã bài (mặc định = chủ đề trong tên folder)")
    nl.add_argument("--title", help="Tiêu đề bài (mặc định suy từ chủ đề)")
    nl.add_argument("--force", action="store_true", help="Ghi đè nếu file đã tồn tại")
    nl.set_defaults(func=cmd_new_lesson)

    ns = sub.add_parser("new-summary", help="Sinh khung phiếu TỔNG KẾT CHƯƠNG (truyền các folder tuần của chương)")
    ns.add_argument("folders", nargs="+", help="Các folder tuần của chương dưới inputs/seeds/<lop>/<mon>/")
    ns.add_argument("--slug", help="Mã phiếu tổng kết (nên đặt cho chương nhiều tuần)")
    ns.add_argument("--title", help="Tiêu đề chương")
    ns.add_argument("--force", action="store_true", help="Ghi đè nếu đã tồn tại")
    ns.set_defaults(func=cmd_new_summary)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
