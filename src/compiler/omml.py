"""Đổi công thức LaTeX → OMML (Equation gốc của Word) — dùng cho bản Word (.docx).

Vì sao pandoc/texmath: mọi công cụ LaTeX→Word miễn phí đáng kể (typ2docx, tex2gdoc,
tex_math_to_word…) đều dựa vào texmath của pandoc — bộ đọc LaTeX toán trưởng thành
nhất hiện có. Ở đây CHỈ mượn pandoc phần công thức; phần lắp tài liệu (bảng, hộp,
header/footer/watermark) do `docx_renderer` tự làm để nắm trọn bố cục.

Bài học đã học từ các repo kia (Thầy 22/10/2026: "học hết kinh nghiệm họ rút ra"):
  • GHÉP THEO ID, không theo thứ tự chạy — tex_math_to_word ghép theo chỉ số, hỏng
    một công thức là lệch tất cả công thức phía sau.
  • 1 lần gọi pandoc cho CẢ LÔ (khởi động pandoc ~0,2s; kho có hàng chục nghìn công thức).
  • "Không báo lỗi ≠ đúng" (formula-flow): pandoc đổi hỏng thì vẫn exit 0 và in sống
    mã TeX ra chữ ⇒ coi là HỎNG khi đoạn kết quả không có <m:oMath> hoặc oMath rỗng
    hoặc còn sót lệnh `\\…` trong <m:t>.
  • Đưa thẳng AST JSON cho pandoc (không qua Markdown) ⇒ không có chuyện bộ đọc
    Markdown hiểu nhầm dấu `$`, `*`, `_` trong công thức.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from functools import lru_cache
from pathlib import Path

from lxml import etree

from config import settings

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"m": M_NS, "w": W_NS}

# Đổi số này khi đổi tiền xử lý/hậu xử lý ⇒ cache cũ tự vô hiệu.
_CACHE_VER = "2"

_MARK = "\u27e6{}\u27e7"            # ⟦id⟧ — ký tự không bao giờ có trong đề
_MARK_RE = re.compile("\u27e6(\\d+)\u27e7")


class PandocMissing(RuntimeError):
    """Máy chưa cài pandoc — build vẫn ra PDF, chỉ bỏ qua bản Word."""


@lru_cache(maxsize=1)
def pandoc_bin() -> str:
    exe = shutil.which("pandoc")
    if not exe:
        raise PandocMissing("chưa cài pandoc (Mac: brew install pandoc · Windows: winget install JohnMacFarlane.Pandoc)")
    return exe


@lru_cache(maxsize=1)
def _api_version() -> list[int]:
    out = subprocess.run([pandoc_bin(), "-f", "markdown", "-t", "json"], input="x",
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["pandoc-api-version"]


# ───────────────────────── tiền xử lý LaTeX trước texmath ─────────────────────────
# Mỗi luật đều có lý do từ thống kê kho (232 lệnh, 367 seed) hoặc lỗi texmath đã biết.
_PRE = [
    # \color{x} trong công thức: texmath#225 bỏ qua màu — bỏ hẳn cho sạch.
    (re.compile(r"\\color\{[^{}]*\}"), ""),
    (re.compile(r"\\textcolor\{[^{}]*\}"), ""),
    # Lệnh dàn trang không mang nghĩa toán.
    (re.compile(r"\\(?:smash|vphantom|hphantom|phantom)\b(\[[a-z]\])?"), ""),
    (re.compile(r"\\(?:displaystyle|textstyle|scriptstyle|nolimits|limits)\b"), ""),
    (re.compile(r"\\(?:big|Big|bigg|Bigg)[lrm]?\b"), ""),
    # Cây chống chiều cao (strut) trong ô điền phân thức lớp 8 ch.VI: `\rule[-0.9ex]{0pt}{2.6ex}`.
    # Bề rộng 0 ⇒ chỉ để dàn dòng ở bản PDF; texmath không hiểu \rule (82 công thức hỏng).
    (re.compile(r"\\rule(\[[^\]]*\])?\{0(?:pt|em|ex|mm|cm)?\}\{[^{}]*\}"), ""),
    (re.compile(r"\\(?:strut|mathstrut)\b"), ""),
    # \boxed lỗi texmath#294 ⇒ thay bằng \fbox (texmath hiểu \fbox thành m:borderBox).
    (re.compile(r"\\boxed\b"), r"\\fbox"),
    # Dấu cung "\overset{\frown}{AB}" (64 chỗ): giữ — texmath ra m:limUpp, xử lý ở hậu kỳ.
]


def preprocess(tex: str) -> str:
    s = tex.strip()
    for pat, rep in _PRE:
        s = pat.sub(rep, s)
    return s


# ───────────────────────── hậu xử lý trên XML đã parse ─────────────────────────
def _m(tag: str) -> str:
    return f"{{{M_NS}}}{tag}"


def postprocess(omath: etree._Element) -> etree._Element:
    """Sửa OMML texmath sinh ra cho Word hiển thị đúng.

    - \\overset{\\frown}{AB} (cung AB): texmath ra m:limUpp (chữ ⌢ treo cao như giới hạn).
      Đổi thành m:acc chr=⌒ để dấu cung ÔM sát chữ như SGK (bài học formula-flow:
      mover phải là accent, nếu không dấu bay xa)."""
    for lu in list(omath.iter(_m("limUpp"))):
        lim = lu.find(_m("lim"))
        e = lu.find(_m("e"))
        if lim is None or e is None:
            continue
        txt = "".join(lim.itertext()).strip()
        if txt in ("\u2322", "\u2312", "\u23dc", "\u0311", "\u2040"):
            acc = etree.Element(_m("acc"))
            pr = etree.SubElement(acc, _m("accPr"))
            etree.SubElement(pr, _m("chr")).set(_m("val"), "\u23dc")
            acc.append(e)
            lu.getparent().replace(lu, acc)
    # \setminus: texmath ra dấu gạch chéo ngược "\" thường ⇒ đổi đúng ký hiệu hiệu tập hợp ∖.
    for t in omath.iter(_m("t")):
        if t.text == "\\":
            t.text = "\u2216"
    return omath


# Công thức CHỈ gồm khoảng trắng (`$\quad$`) — không phải công thức, renderer in khoảng trắng.
_ONLY_SPACE = re.compile(r"^(?:\s|\\(?:quad|qquad|,|;|:|!| )|~|\\hspace\{[^{}]*\})*$")


def is_only_space(tex: str) -> bool:
    return bool(_ONLY_SPACE.match(tex or ""))


# ───────────────────────── chuyển cả lô ─────────────────────────
def _key(tex: str) -> str:
    return hashlib.sha1(f"{_CACHE_VER}\0{tex}".encode()).hexdigest()


# Cache = MỘT file SQLite (trước 22/10/2026 là một file .xml mỗi công thức ⇒ 56 nghìn file,
# 221MB, lỡ bị commit lên git). Khoá đã gồm _CACHE_VER nên đổi phiên bản không cần xoá tay;
# `prune_cache()` dọn bản cũ. Nằm trong storage/cache/ — .gitignore, máy nào tự sinh lại.
CACHE_DB = Path(settings.ROOT) / "storage" / "cache" / "omml.sqlite"


def _db():
    import sqlite3
    CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(CACHE_DB), timeout=30)
    con.execute("PRAGMA journal_mode=WAL")          # nhiều tiến trình (docx_audit_all) cùng đọc/ghi
    con.execute("CREATE TABLE IF NOT EXISTS omml (k TEXT PRIMARY KEY, ver TEXT, xml BLOB)")
    return con


def _cache_get_many(texs: list[str]) -> dict[str, bytes]:
    if not texs:
        return {}
    con = _db()
    try:
        keys = {_key(t): t for t in texs}
        out: dict[str, bytes] = {}
        ks = list(keys)
        for i in range(0, len(ks), 900):            # giới hạn số tham số của SQLite
            chunk = ks[i:i + 900]
            q = f"SELECT k, xml FROM omml WHERE k IN ({','.join('?' * len(chunk))})"
            for k, xml in con.execute(q, chunk):
                out[keys[k]] = xml
        return out
    finally:
        con.close()


def _cache_put_many(items: dict[str, bytes]) -> None:
    if not items:
        return
    con = _db()
    try:
        with con:
            con.executemany("INSERT OR REPLACE INTO omml VALUES (?, ?, ?)",
                            [(_key(t), _CACHE_VER, x) for t, x in items.items()])
    finally:
        con.close()


def prune_cache() -> int:
    """Xoá bản cache của phiên bản cũ; trả số dòng đã xoá."""
    con = _db()
    try:
        with con:
            n = con.execute("DELETE FROM omml WHERE ver != ?", (_CACHE_VER,)).rowcount
        con.execute("VACUUM")
        return n
    finally:
        con.close()


def _bad(omath: etree._Element) -> str:
    """Lý do công thức HỎNG (rỗng / còn lệnh sót), '' nếu ổn."""
    txt = "".join(t.text or "" for t in omath.iter(_m("t")))
    if not txt.strip() and omath.find(".//" + _m("f")) is None and omath.find(".//" + _m("rad")) is None:
        return "công thức rỗng"
    left = re.search(r"\\[A-Za-z]+", txt)
    if left:
        return f"còn sót lệnh {left.group(0)}"
    return ""


def _run_pandoc(items: list[tuple[int, str]]) -> dict[int, tuple[bytes | None, str]]:
    """Chạy pandoc 1 lần cho cả lô. Trả {id: (xml m:oMath | None, lý do lỗi)}."""
    blocks = []
    for i, tex in items:
        blocks.append({"t": "Para", "c": [
            {"t": "Str", "c": _MARK.format(i)},
            {"t": "Math", "c": [{"t": "InlineMath"}, tex]},
        ]})
    doc = {"pandoc-api-version": _api_version(), "meta": {}, "blocks": blocks}
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "m.docx"
        r = subprocess.run([pandoc_bin(), "-f", "json", "-t", "docx", "-o", str(out)],
                           input=json.dumps(doc), capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"pandoc lỗi: {r.stderr[:500]}")
        xml = zipfile.ZipFile(out).read("word/document.xml")
    root = etree.fromstring(xml)
    res: dict[int, tuple[bytes | None, str]] = {}
    for p in root.iter(f"{{{W_NS}}}p"):
        mk = _MARK_RE.search("".join(t.text or "" for t in p.iter(f"{{{W_NS}}}t")))
        if not mk:
            continue
        i = int(mk.group(1))
        oms = p.findall(_m("oMath"))
        if len(oms) != 1:
            res[i] = (None, "texmath không đọc được (ra chữ thô)")
            continue
        om = postprocess(oms[0])
        why = _bad(om)
        res[i] = (None, why) if why else (etree.tostring(om), "")
    for i, _ in items:
        res.setdefault(i, (None, "pandoc làm rơi công thức"))
    return res


def convert_many(formulas: list[str]) -> dict[str, tuple[etree._Element | None, str]]:
    """{LaTeX gốc: (phần tử <m:oMath> | None, lý do lỗi)}. Có cache SQLite."""
    out: dict[str, tuple[etree._Element | None, str]] = {}
    texs = [t for t in dict.fromkeys(formulas) if not is_only_space(t)]
    pre = {t: preprocess(t) for t in texs}
    hits = _cache_get_many(list(set(pre.values())))
    todo: list[tuple[int, str]] = []
    idx: dict[int, str] = {}
    for tex in texs:
        if pre[tex] in hits:
            out[tex] = (etree.fromstring(hits[pre[tex]]), "")
            continue
        i = len(idx)
        idx[i] = tex
        todo.append((i, pre[tex]))
    # Lô cỡ vừa phải: một công thức làm pandoc chết thì chỉ phải chạy lại lô đó.
    for k in range(0, len(todo), 2000):
        chunk = todo[k:k + 2000]
        fresh: dict[str, bytes] = {}
        for i, (xml, why) in _run_pandoc(chunk).items():
            tex = idx[i]
            if xml is not None:
                fresh[pre[tex]] = xml
                out[tex] = (etree.fromstring(xml), "")
            else:
                out[tex] = (None, why)
        _cache_put_many(fresh)
    return out


def wrap_display(omath: etree._Element) -> etree._Element:
    """Công thức đứng riêng dòng ⇒ <m:oMathPara> (Word hiển thị cỡ display, căn giữa)."""
    para = etree.Element(_m("oMathPara"), nsmap={"m": M_NS})
    para.append(omath)
    return para
