#!/usr/bin/env python3
"""quick — gõ ngắn cho 2 việc làm nhiều nhất: build lại nhanh & đọc phiếu dạng dễ nhìn.

    python -m scripts.quick find  <chữ bất kỳ>   # tìm phiếu, không cần gõ đủ đường dẫn
    python -m scripts.quick build <chữ bất kỳ>   # validate + build (bỏ trống = phiếu vừa làm)
    python -m scripts.quick md    <chữ bất kỳ>   # đổi JSON → Markdown để bấm xem preview

`<chữ bất kỳ>` là mẩu tên bất kỳ trong đường dẫn: "hinh binh hanh", "t7 hbh", "phieu-b nhan da thuc".
Khớp nhiều phiếu quá thì in danh sách ra cho chọn, không đoán bừa.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = ROOT / "inputs" / "seeds"
LAST = ROOT / "storage" / "last_quick.txt"

# Không phải phiếu học tập: spec thuyết minh, ngân hàng đề, cấu hình.
SKIP_STEMS = {"thuyet-minh"}


def _fold(s: str) -> str:
    """Bỏ dấu tiếng Việt + hạ chữ thường + gom mọi ký tự lạ thành khoảng trắng."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _lessons() -> list[Path]:
    out = []
    for p in sorted(SEEDS.rglob("*.json")):
        if p.stem in SKIP_STEMS or p.stem.startswith("thuyet-minh"):
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — file hỏng thì bỏ qua, việc của validate
            continue
        if isinstance(d, dict) and "stages" in d and "slug" in d:
            out.append(p)
    return out


def loai_file(p: Path) -> str:
    """'phieu' (gói bài học) | 'spec' (phiếu thuyết minh) | '' (không phải cả hai).

    Dùng để ⌘⇧B tự chọn đúng lệnh build theo file Thầy đang mở, khỏi phải nhớ.
    """
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return ""
    if not isinstance(d, dict) or "slug" not in d:
        return ""
    if "stages" in d:
        return "phieu"
    if p.name.startswith("thuyet-minh") or "phieu" in d or "lythuyet" in d:
        return "spec"
    return ""


def _la_phieu(p: Path) -> bool:
    return loai_file(p) == "phieu"


def resolve(query: str) -> Path:
    """Mẩu chữ HOẶC đường dẫn file → đúng 1 file phiếu.

    Nhận thẳng đường dẫn để VS Code truyền `${file}` (file đang mở) vào được —
    xem .vscode/tasks.json.
    """
    # Đường dẫn có thật → dùng luôn, nhưng phải chắc đó là phiếu học tập.
    ung_vien = Path(query.strip())
    if query.strip() and ung_vien.exists() and ung_vien.is_file():
        if ung_vien.suffix.lower() != ".json":
            sys.exit(f"✗ '{ung_vien.name}' không phải file JSON. Hãy mở đúng file phiếu "
                     "(vd phieu-a-….json) rồi bấm lại.")
        if not loai_file(ung_vien):
            sys.exit(f"✗ '{ung_vien.name}' không phải phiếu học tập lẫn phiếu thuyết minh "
                     "(thiếu 'slug'). Mở đúng file phiếu rồi bấm lại.")
        ung_vien = ung_vien.resolve()   # luôn trả tuyệt đối: gọi từ thư mục nào cũng chạy
        LAST.parent.mkdir(parents=True, exist_ok=True)
        LAST.write_text(str(ung_vien), encoding="utf-8")
        return ung_vien

    if not query.strip():
        if LAST.exists() and (p := Path(LAST.read_text().strip())).exists():
            print(f"↻ Dùng lại phiếu lần trước: {p.relative_to(ROOT)}")
            return p
        sys.exit("✗ Chưa có phiếu nào làm gần đây. Gõ kèm tên, vd: make b Q=\"hinh binh hanh\"")

    words = _fold(query).split()
    hits = [p for p in _lessons() if all(w in _fold(str(p.relative_to(SEEDS))) for w in words)]

    if not hits:
        sys.exit(f"✗ Không thấy phiếu nào khớp '{query}'. Thử ít chữ hơn, vd chỉ 'hbh' hoặc 'tuan07'.")
    if len(hits) > 1:
        # Trùng tên file chính xác thì ưu tiên nó (vd gõ đúng slug).
        exact = [p for p in hits if _fold(p.stem) == _fold(query)]
        if len(exact) == 1:
            hits = exact
        else:
            print(f"⚠ '{query}' khớp {len(hits)} phiếu — gõ thêm chữ cho rõ:", file=sys.stderr)
            for p in hits[:12]:
                print(f"    {p.relative_to(SEEDS)}", file=sys.stderr)
            sys.exit(1)

    LAST.parent.mkdir(parents=True, exist_ok=True)
    LAST.write_text(str(hits[0]), encoding="utf-8")
    return hits[0]


# ─────────────────────────── JSON → Markdown ───────────────────────────

STAGE_VN = {
    "review": "Chặng 1 · Khởi động / Ôn lại",
    "concept": "Chặng 2 · Khái niệm",
    "practice1": "Chặng 3 · Luyện tập 1",
    "practice2": "Chặng 4 · Luyện tập 2",
    "reflection": "Chặng 5 · Tổng kết",
}
TIER_VN = {"onclass": "trên lớp", "btvn": "BTVN", "extend": "mở rộng", "": "—"}
LEVEL_VN = {0: "—", 1: "★ NB", 2: "★★ TH", 3: "★★★ VD", 4: "◆ VDC"}


# Mã LaTeX chỉ phục vụ dàn trang PDF — đọc trên màn hình thì bỏ, kẻo rối mắt.
_LAYOUT = [
    # [[wrap]]…[[/wrap]] = hình thả cạnh đề bài (xem templates/_blocks.j2) — gói LaTeX thô.
    (r"\[\[wrap\]\].*?\[\[/wrap\]\]", "🖼 *[hình kèm đề]* "),
    (r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "\n\n🖼 *[hình vẽ TikZ]*\n\n"),
    (r"\\adjustbox\{[^}]*\}\{", ""),
    (r"\\(?:vspace|hspace)\*?\{[^}]*\}", ""),
    (r"\\(?:centering|raggedright|small|footnotesize|normalsize|linebreak)\b", ""),
    (r"\\color\{[^}]*\}", ""),
    (r"\\(?:sffamily|rmfamily|ttfamily|itshape|bfseries|upshape|scriptsize|tiny|large|Large|huge)\b", ""),
    (r"\\par\s*\{([^{}]*)\}", r"\n\n*\1*\n\n"),   # chú thích hình
]


def _cm(width: str, ky_tu: str, moi_cm: float, it_nhat: int = 3) -> str:
    """Bề rộng LaTeX ('1.2cm') → chuỗi ký tự dài tương ứng, để nhìn ra chỗ chừa cho HS."""
    m = re.match(r"\s*([\d.]+)", width)
    try:
        so_cm = float(m.group(1)) if m else 2.0
    except ValueError:
        so_cm = 2.0
    return ky_tu * max(it_nhat, round(so_cm * moi_cm))


def _dots(width: str) -> str:
    return _cm(width, "…", 4)


def _text(s: str) -> str:
    """Đổi token của engine sang Markdown. Giữ nguyên $...$ để preview render công thức."""
    for pat, rep in _LAYOUT:
        s = re.sub(pat, rep, s, flags=re.DOTALL)
    s = re.sub(r"^\s*\}\s*$", "", s, flags=re.MULTILINE)   # ngoặc đóng mồ côi của adjustbox
    s = s.replace("[[br]]", "\n\n")
    # [[blank:W]] với W là bề rộng LaTeX ("1.2cm", "2cm"…) — xem jinja_renderer._BLANK_W
    s = re.sub(r"\[\[m?blank:([^\]]+)\]\]", lambda m: _dots(m.group(1)), s)
    s = s.replace("[[blank]]", "…" * 10)
    # [[oly:W]] = ô ly kẻ sẵn cho HS tiểu học viết (jinja_renderer._OLY_W)
    s = re.sub(r"\[\[oly:([^\]]+)\]\]", lambda m: _cm(m.group(1), "▢", 2), s)
    # lưới an toàn: token mới của engine sau này cũng không lọt mã thô ra bản đọc
    s = re.sub(r"\[\[/?[a-z]+(?::[^\]]*)?\]\]", "", s)
    # minipage 2 cột chỉ để dàn trang PDF — đọc trên màn hình thì bỏ đi cho sạch.
    s = re.sub(r"\\begin\{minipage\}(\[[^\]]*\])?\{[^}]*\}", "", s)
    s = s.replace(r"\end{minipage}", "").replace(r"\hfill", "\n\n")
    # \textbf{...} → **...** (chỉ khi ngoặc không lồng nhau, tránh phá công thức)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"**\1**", s)
    s = re.sub(r"\\textit\{([^{}]*)\}", r"*\1*", s)
    s = re.sub(r"[ \t]*\n[ \t]*", "\n", s)     # bỏ khoảng trắng thừa quanh chỗ xuống dòng
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _block_md(b: dict) -> list[str]:
    t = b.get("type", "")
    if t == "problem":
        head = f"**{b.get('label', 'Bài.')}**"
        tags = []
        if b.get("level"):
            tags.append(LEVEL_VN.get(b["level"], str(b["level"])))
        if b.get("tier"):
            tags.append(TIER_VN.get(b["tier"], b["tier"]))
        if b.get("draw"):
            tags.append("HS tự vẽ hình")
        if b.get("figure_given"):
            tags.append("có hình sẵn")
        if b.get("check"):
            tags.append("có `check` SymPy")
        if tags:
            head += "  `" + " · ".join(tags) + "`"
        out = [head, "", _text(b.get("statement", ""))]
        if b.get("hints"):
            out += ["", "> 💡 " + " / ".join(b["hints"])]
        return out
    if t == "para":
        return [_text(b.get("text", ""))]
    if t == "math":
        return ["$$" + b.get("latex", "") + "$$"]
    if t == "noted":
        v = b.get("variant") or "note"
        return [f"> **[{v}]** " + _text(b.get("text", "")).replace("\n", "\n> ")]
    if t == "opener":
        return ["> 🎬 **Mở màn.** " + _text(b.get("text", "")).replace("\n", "\n> ")]
    if t == "writelines":
        return [f"*(chừa {b.get('count', 2)} dòng cho HS viết)*"]
    if t == "figure":
        what = "ảnh `" + b["image"] + "`" if b.get("image") else "hình vẽ TikZ"
        cap = " — " + _text(b["caption"]) if b.get("caption") else ""
        return [f"🖼 *[{what}{cap}]*"]
    if t == "table":
        rows = b.get("rows", [])
        heads = b.get("headers", []) or ([""] * len(rows[0]) if rows else [])
        md = ["| " + " | ".join(_text(h) for h in heads) + " |",
              "|" + "---|" * len(heads)]
        md += ["| " + " | ".join(_text(c) for c in r) + " |" for r in rows]
        return ([_text(b["caption"])] if b.get("caption") else []) + md
    if t == "mindmap":
        out = [f"🧠 **Sơ đồ tư duy — {_text(b.get('root', ''))}**"]

        def walk(nodes, depth=1):
            for n in nodes:
                out.append("  " * depth + "- " + _text(n.get("label", "")))
                walk(n.get("children", []), depth + 1)

        walk(b.get("branches", []))
        return out
    return [f"*(block `{t}` — xem JSON)*"]


def to_markdown(path: Path) -> str:
    d = json.loads(path.read_text(encoding="utf-8"))
    L = [f"# {d.get('title', path.stem)}", ""]
    meta = [x for x in (d.get("eyebrow"), d.get("grade_label"),
                        f"Tầng {d['class_tier']}" if d.get("class_tier") else "") if x]
    if meta:
        L += ["**" + "  ·  ".join(meta) + "**", ""]
    L += [f"`{d.get('slug', '')}`  ·  nguồn: `{path.relative_to(ROOT)}`", "", "---", ""]

    for st in d.get("stages", []):
        L += [f"## {STAGE_VN.get(st.get('kind'), st.get('kind', ''))} — {st.get('title', '')}", ""]
        for b in st.get("blocks", []):
            L += _block_md(b) + [""]
        if st.get("solution"):
            L += ["<details><summary>✅ <b>Lời giải (chỉ có ở bản GV)</b></summary>", "",
                  _text(st["solution"]), "", "</details>", ""]
        if st.get("teacher_note"):
            L += ["> 👩‍🏫 **Ghi chú cho GV.** " + _text(st["teacher_note"]).replace("\n", "\n> "), ""]
        L += ["---", ""]
    return "\n".join(L)


# ────────────────────────────── lệnh ──────────────────────────────

def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    cmd, query = argv[0], " ".join(argv[1:])

    if cmd == "find":
        p = resolve(query)
        print(p.relative_to(ROOT))
        return 0

    if cmd == "build":
        p = resolve(query)
        py = sys.executable
        print(f"→ Kiểm: {p.relative_to(ROOT)}")

        # Thuyết minh là loại file khác, build bằng lệnh khác — tự nhận, khỏi bắt Thầy nhớ.
        # (cmd_build_thuyetminh đã tự gác giờ vô lý bên trong, không cần validate riêng.)
        if loai_file(p) == "spec":
            print("→ Đây là phiếu THUYẾT MINH — dựng PDF thuyết minh…")
            return subprocess.run([py, "-m", "src.main", "build-thuyetminh", str(p)],
                                  cwd=ROOT).returncode

        if subprocess.run([py, "-m", "src.main", "validate", str(p)], cwd=ROOT).returncode:
            print("✗ Chưa qua cổng validate — sửa xong chạy lại.", file=sys.stderr)
            return 1
        print(f"→ Build 3 bản PDF…")
        return subprocess.run([py, "-m", "src.main", "build", str(p)], cwd=ROOT).returncode

    if cmd == "md":
        p = resolve(query)
        if loai_file(p) == "spec":
            sys.exit("✗ Bản đọc Markdown mới chỉ làm cho phiếu học tập. Với phiếu thuyết "
                     "minh, bấm ⌘⇧B là ra thẳng PDF rồi.")
        out = ROOT / "storage" / "preview" / (p.stem + ".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(to_markdown(p), encoding="utf-8")
        print(f"✓ {out.relative_to(ROOT)}")
        print("  Mở file rồi bấm ⌘⇧V (Cmd+Shift+V) để xem bản dễ đọc.")
        return 0

    sys.exit(f"✗ Không rõ lệnh '{cmd}'. Có: find | build | md")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
