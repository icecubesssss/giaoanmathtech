"""Đọc chuỗi nội dung JSON (chữ + `$…$`/`\\(…\\)`/`\\[…\\]` + token [[…]] + lệnh LaTeX dàn
trang) thành CÂY KHỐI trung gian (IR) để `docx_renderer` dựng ra Word.

Vì sao phải tự đọc (không đưa pandoc): chữ trong seed là một "ngôn ngữ dàn trang" nhỏ —
thống kê 22/10/2026 trên 367 seed: `minipage` đôi 1.178 chỗ (đề trái – hình phải),
`tabular` 247, `\\parbox` dựng phương án trắc nghiệm 303, hộp hình treo `[[wrap]]` 84…
pandoc đọc LaTeX gặp mấy thứ này thì BỎ IM LẶNG (tex2gdoc: "exit 0, log rỗng, tài liệu
trông như xong"; tabular lồng nhau ⇒ mất cả bảng).

Nguyên tắc: KHÔNG BAO GIỜ âm thầm vứt lệnh lạ. Lệnh chưa có luật ⇒ giữ chữ trong
ngoặc của nó + ghi tên vào `ctx.unknown` để cổng `docx_gate` chặn ghi file.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, replace

# ═══════════════════════════════ IR ═══════════════════════════════


@dataclass(frozen=True)
class Fmt:
    bold: bool = False
    italic: bool = False
    underline: bool = False
    sans: bool = False
    smallcaps: bool = False
    sup: bool = False
    boxed: bool = False
    color: str | None = None      # hex
    size: float | None = None     # pt
    shade: str | None = None      # nền run (hex)


@dataclass
class T:                    # run chữ
    text: str
    fmt: Fmt = Fmt()


@dataclass
class M:                    # công thức trong dòng
    tex: str


@dataclass
class Tab:                  # \hfill / \dotfill ⇒ tab (tab dấu chấm nếu dots)
    dots: bool = False


@dataclass
class Img:                  # ảnh trong dòng (QR, badge…)
    snippet: str = ""           # mã LaTeX cần vẽ (tikz_raster)
    path: str = ""              # hoặc ảnh có sẵn
    h_pt: float = 12.0


Inline = (T, M, Tab, Img)


@dataclass
class P:                    # đoạn
    inl: list = field(default_factory=list)
    align: str = "justify"      # left | center | right | justify
    tight: bool = False         # dòng của một đoạn nhiều dòng ([[br]]) ⇒ cách sau 0
    style: str | None = None    # style Word riêng (MT …)
    indent_pt: float = 0.0      # thụt trái
    hanging_pt: float = 0.0     # thụt treo (deflist, gạch đầu dòng)
    keep_next: bool = False
    border_bottom: str | None = None   # gạch dưới tiêu đề phần (hex)
    space_before: float | None = None
    space_after: float | None = None


@dataclass
class DMath:                # công thức đứng riêng dòng
    tex: str
    align: str = "center"


@dataclass
class Fig:                  # hình (TikZ hoặc ảnh), căn giữa
    snippet: str = ""
    image: str = ""
    caption: list = field(default_factory=list)   # inline
    max_w_frac: float = 1.0       # theo bề ngang khung chứa
    force_w_frac: float | None = None   # ÉP bề ngang (\figbelow: width=0.44\linewidth)
    max_h_cm: float | None = None
    align: str = "center"


@dataclass
class Cell:
    blocks: list = field(default_factory=list)
    span: int = 1
    align: str | None = None
    shade: str | None = None
    vspan: int = 1                # gộp DỌC bấy nhiêu hàng (hàng dưới KHÔNG khai ô ở cột đó)


@dataclass
class Tbl:
    rows: list = field(default_factory=list)       # list[list[Cell]]
    widths: list | None = None                     # tỉ lệ bề ngang từng cột (tổng ≤ 1)
    borders: bool = True
    border_color: str = "1B1B2A"
    header_rows: int = 0
    font_pt: float | None = None
    cell_pad_pt: float = 2.0
    align: str = "center"
    compact: bool = False         # ô khít: đoạn trong ô cách 0, giãn dòng 1,0 (bảng TM, arraystretch<1)


@dataclass
class Box:                  # hộp có viền (callout, gợi ý, quy trình, thẻ tiêu đề…)
    blocks: list = field(default_factory=list)
    frame: str = "E1E4EA"
    back: str | None = None
    frame_pt: float = 0.6
    title: str = ""
    title_fg: str = "FFFFFF"
    title_bg: str | None = None
    left_only_pt: float | None = None    # hộp chỉ có vạch trái (answerbox)
    pad_pt: float = 6.0


@dataclass
class PageBreak:
    pass


@dataclass
class WriteLines:
    count: int
    variant: str = ""


Block = (P, DMath, Fig, Tbl, Box, PageBreak, WriteLines)


@dataclass
class Ctx:
    """Ngữ cảnh đọc: bản in (HS/GV) + nơi gom lệnh lạ cho cổng."""
    show_solution: bool = False
    unknown: list = field(default_factory=list)
    where: str = ""

    def lạ(self, what: str):
        self.unknown.append(f"{self.where}: {what}" if self.where else what)


# ═══════════════════════════════ token [[…]] ═══════════════════════════════
_THE_MUC_DO = re.compile(r"\[(?:NB|TH|VD|VDC)\]\s*")
_TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
_MM_PER_DOT = 1.06      # bề ngang dấu "." cỡ 12pt Times ≈ 1,06mm
LINEWIDTH_CM = 17.2     # bề ngang cột chữ (đổi \linewidth trong \hspace)


def to_cm(dim: str, default: float = 5.0) -> float:
    m = re.match(r"\s*(-?[\d.]*)\s*\\?(cm|mm|in|pt|em|ex|linewidth|textwidth)?", dim or "")
    if not m or not (m.group(1) or m.group(2)):
        return default
    v = float(m.group(1)) if m.group(1) not in ("", "-", ".") else 1.0
    u = m.group(2) or "cm"
    return v * {"cm": 1, "mm": .1, "in": 2.54, "pt": 1 / 28.45, "em": .42, "ex": .19,
                "linewidth": LINEWIDTH_CM, "textwidth": LINEWIDTH_CM}[u]


def dots(cm: float) -> str:
    return "." * max(4, round(cm * 10 / _MM_PER_DOT))


def fill_width_cm(answer: str, explicit: str | None) -> float:
    """CÙNG công thức với `jinja_renderer._be_rong_o` để ô Word dài như ô PDF."""
    if explicit:
        return to_cm(explicit)
    plain = re.sub(r"\\[a-zA-Z]+|\[\[[^\]]*\]\]|[{}$]", "", answer or "").strip()
    n = len(plain) or 3
    return min(max(0.34 * n + 0.45, 0.9), 4.5)


# ═══════════════════════════════ tách công thức ═══════════════════════════════
def split_math_raw(s: str) -> list[tuple[str, str]]:
    """[('text'|'math'|'dmath', chuỗi)]. Hiểu `$…$`, `\\(…\\)`, `\\[…\\]`; `\\\\[3pt]`
    (xuống dòng) KHÔNG bị nhầm với `\\[`. Token [[…]] ngoài công thức được nhảy qua
    nguyên khối (token có thể chứa `$`, vd [[fill:$x=2$]])."""
    out: list[tuple[str, str]] = []
    buf: list[str] = []
    mode = "text"
    close = ""
    i, n = 0, len(s)

    def push(kind):
        nonlocal buf
        out.append((kind, "".join(buf)))
        buf = []

    while i < n:
        if mode == "text" and s.startswith("[[", i):
            j = s.find("]]", i)
            if j != -1:
                buf.append(s[i:j + 2])
                i = j + 2
                continue
        c = s[i]
        if mode == "text":
            if c == "\\" and i + 1 < n:
                nx = s[i + 1]
                if nx in "([":
                    push("text")
                    mode, close = ("math", "\\)") if nx == "(" else ("dmath", "\\]")
                    i += 2
                    continue
                buf.append(s[i:i + 2])
                i += 2
                continue
            if c == "$":
                push("text")
                mode, close = "math", "$"
                i += 1
                continue
            buf.append(c)
            i += 1
        else:
            # Trong công thức: `\\x` là một cặp (nên `\\$` không đóng công thức),
            # trừ khi chính cặp đó là dấu đóng `\\)` / `\\]`.
            if s.startswith(close, i):
                push(mode)
                mode = "text"
                i += len(close)
                continue
            if c == "\\" and i + 1 < n:
                buf.append(s[i:i + 2])
                i += 2
                continue
            buf.append(c)
            i += 1
    push(mode)
    return [(k, v) for k, v in out if v or k != "text"]


_TOKEN = re.compile(r"\[\[(/?[a-z]+)(?::((?:[^\[\]]|\[(?!\[)|\](?!\]))*))?\]\]")


def _token_dots(name: str, arg: str | None) -> str | None:
    if name == "blank":
        return dots(to_cm(arg) if arg else 5.0)
    if name == "mblank":
        return dots(to_cm(arg) if arg else 2.0)
    if name == "fill":
        ans, _, w = (arg or "").partition("|")
        return dots(fill_width_cm(ans, w or None))
    if name == "oly":
        return dots(to_cm(arg) if arg else 5.0)
    return None


def tokens_in_math(s: str, ctx: Ctx | None = None) -> str:
    """Token ô trống NẰM TRONG công thức ⇒ \\text{……}: giữ công thức nguyên khối (cắt đôi
    `\\dfrac{[[mblank]]}{3}` là vỡ cú pháp), ô trống vẫn hiện thành chấm trong Equation.
    Bản GV: [[fill:x]] trong công thức ⇒ in đáp án (đã là LaTeX toán)."""
    res = []
    for kind, chunk in split_math_raw(s):
        if kind == "text":
            res.append(chunk)
            continue

        def sub(m):
            name, arg = m.group(1), m.group(2)
            if name == "fill" and ctx is not None and ctx.show_solution:
                ans = (arg or "").partition("|")[0].strip().strip("$")
                return "\\underline{" + ans + "}"
            d = _token_dots(name, arg)
            return "\\text{" + d + "}" if d else ""
        chunk = _TOKEN.sub(sub, chunk)
        res.append(("$" + chunk + "$") if kind == "math" else ("\\[" + chunk + "\\]"))
    return "".join(res)


def formulas_in(s: str) -> list[str]:
    """Mọi công thức của một chuỗi nội dung (bỏ tikz) — để gom lô cho omml / audit."""
    s = _TIKZ.sub("", s or "")
    s = tokens_in_math(s)
    out: list[str] = []
    for kind, chunk in split_math_raw(s):
        if kind != "text" and chunk.strip():
            out.append(chunk)
        elif kind == "text":
            for m in _TOKEN.finditer(chunk):
                if m.group(2) and ("$" in m.group(2) or "\\(" in m.group(2)):
                    out.extend(formulas_in(m.group(2).partition("|")[0]))
    return out


# ═══════════════════════════════ bộ đọc ═══════════════════════════════
DING = {41: "\u2709", 42: "\u261B", 43: "\u261E", 44: "\u270C", 45: "\u270D", 46: "\u270E",
        51: "\u2713", 52: "\u2714", 55: "\u2717", 56: "\u2718", 72: "\u2605", 73: "\u2606",
        108: "\u25CF", 110: "\u25A0", 117: "\u25C6"}
SIZES = {"tiny": 7, "scriptsize": 8, "footnotesize": 10, "small": 11, "normalsize": 12,
         "large": 14.4, "Large": 17.3, "LARGE": 20.7, "huge": 24.9}
TEXT_SYMBOLS = {
    "ldots": "\u2026", "dots": "\u2026", "textquotedblleft": "\u201C", "textquotedblright": "\u201D",
    "textquoteleft": "\u2018", "textquoteright": "\u2019", "textendash": "\u2013",
    "textemdash": "\u2014", "textdegree": "\u00B0", "S": "\u00A7", "textbullet": "\u2022",
    "quad": "\u2003", "qquad": "\u2003\u2003", "enspace": "\u2002", "thinspace": "\u2009",
    "textellipsis": "\u2026", "copyright": "\u00A9", "%": "%", "&": "&", "#": "#", "_": "_",
    "$": "$", "{": "{", "}": "}", ",": "\u2009", ";": "\u2005", ":": "\u2005", "!": "",
    " ": " ", "textbackslash": "\\", "slash": "/", "LaTeX": "LaTeX", "textasciitilde": "~",
    "times": "\u00D7", "checkmark": "\u2713", "square": "\u25A1",
}
# Lệnh dàn trang KHÔNG mang nội dung — bỏ (kèm đối số nếu có).
NOOP0 = {"par", "noindent", "indent", "nopagebreak", "pagebreak", "smallskip", "medskip",
         "bigskip", "nobreak", "justifying", "raggedright", "raggedleft", "selectfont",
         "relax", "strut", "leavevmode", "protect", "allowbreak", "break", "newline",
         "normalfont", "upshape", "mdseries", "rmfamily", "hfil", "vfill", "null",
         "clearpage", "centering", "unskip", "ignorespaces", "linebreak", "item"}
NOOP1 = {"vspace", "addvspace", "stageneedspace", "label", "linespread", "pagestyle",
         "thispagestyle", "setcounter", "needspace", "phantom", "vphantom"}
# Lệnh 1 đối số chỉ là VỎ — lấy nội dung.
WRAP1 = {"mbox", "hbox", "vbox", "vtop", "smash", "text", "textrm", "textnormal",
         "textup", "centerline", "leftline", "rightline", "ensuremath", "makecell", "shortstack"}


def _read_group(s: str, i: int) -> tuple[str, int]:
    """s[i] == '{' ⇒ (nội dung, chỉ số sau '}'). Nhảy qua cặp thoát `\\x`."""
    assert s[i] == "{"
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def _skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i] in " \t\n":
        i += 1
    return i


def _read_opt(s: str, i: int) -> tuple[str | None, int]:
    j = _skip_ws(s, i)
    if j < len(s) and s[j] == "[":
        depth, k = 0, j
        while k < len(s):
            if s[k] == "{":
                depth += 1
            elif s[k] == "}":
                depth -= 1
            elif s[k] == "]" and depth == 0:
                return s[j + 1:k], k + 1
            k += 1
    return None, i


def _read_arg(s: str, i: int) -> tuple[str, int]:
    j = _skip_ws(s, i)
    if j < len(s) and s[j] == "{":
        return _read_group(s, j)
    if j < len(s) and s[j] == "\\":
        m = re.match(r"\\[A-Za-z]+|\\.", s[j:])
        return m.group(0), j + len(m.group(0))
    return (s[j], j + 1) if j < len(s) else ("", j)


def _find_end(s: str, i: int, env: str) -> tuple[str, int]:
    """Nội dung môi trường `env` bắt đầu tại i (sau \\begin{env}…) tới \\end{env} khớp lồng."""
    depth, j = 1, i
    pat = re.compile(r"\\(begin|end)\{" + re.escape(env) + r"\}")
    while True:
        m = pat.search(s, j)
        if not m:
            return s[i:], len(s)
        depth += 1 if m.group(1) == "begin" else -1
        if depth == 0:
            return s[i:m.start()], m.end()
        j = m.end()


class Reader:
    """Đọc một chuỗi ra list[Block]. Dùng đệ quy cho ngoặc, môi trường, ô bảng."""

    def __init__(self, ctx: Ctx):
        self.ctx = ctx

    # ---------- API ----------
    def blocks(self, s: str, fmt: Fmt = Fmt(), align: str = "justify") -> list:
        s = _THE_MUC_DO.sub("", s or "")
        s = tokens_in_math(s, self.ctx)
        st = _State(self, fmt, align)
        st.run(s)
        return st.finish()

    def inlines(self, s: str, fmt: Fmt = Fmt()) -> list:
        """Đọc ra một dòng chữ (gộp các đoạn nếu có, ngăn bằng khoảng trắng)."""
        out: list = []
        for b in self.blocks(s, fmt):
            if isinstance(b, P):
                if out:
                    out.append(T(" ", fmt))
                out.extend(b.inl)
            elif isinstance(b, DMath):
                out.append(M(b.tex))
            else:
                self.ctx.lạ(f"khối {type(b).__name__} nằm trong dòng chữ")
        return out


class _State:
    def __init__(self, rd: Reader, fmt: Fmt, align: str):
        self.rd = rd
        self.ctx = rd.ctx
        self.fmt = fmt
        self.align = align
        self.out: list = []
        self.cur: list = []
        self.lines: list[list] = []     # các dòng [[br]] của đoạn hiện tại

    # ---------- gom chữ ----------
    def text(self, t: str, fmt: Fmt | None = None):
        fmt = fmt or self.fmt
        if self.cur and isinstance(self.cur[-1], T) and self.cur[-1].fmt == fmt:
            self.cur[-1].text += t
        else:
            self.cur.append(T(t, fmt))

    def br(self):
        self.lines.append(self.cur)
        self.cur = []

    def par(self):
        lines = self.lines + [self.cur]
        self.lines, self.cur = [], []
        lines = [_trim(l) for l in lines]
        while lines and not lines[-1]:
            lines.pop()
        while lines and not lines[0]:
            lines.pop(0)
        for k, l in enumerate(lines):
            self.out.append(P(l, align=self.align, tight=k < len(lines) - 1))

    def block(self, b):
        self.par()
        self.out.append(b)

    def finish(self) -> list:
        self.par()
        return self.out

    # ---------- vòng đọc ----------
    def run(self, s: str):
        i, n = 0, len(s)
        while i < n:
            c = s[i]
            if s.startswith("[[", i):
                i = self.token(s, i)
            elif c == "$":
                j = i + 1
                while j < n and not (s[j] == "$" and s[j - 1] != "\\"):
                    j += 2 if s[j] == "\\" else 1
                self.cur.append(M(s[i + 1:j]))
                i = j + 1
            elif c == "\\":
                i = self.command(s, i)
            elif c == "{":
                inner, i = _read_group(s, i)
                self.group(inner)
            elif c == "}":
                i += 1
            elif c == "~":
                self.text("\u00A0")
                i += 1
            elif c == "%":
                j = s.find("\n", i)
                i = n if j == -1 else j + 1
            elif c == "\n":
                if s.startswith("\n\n", i):
                    self.par()
                    i = _skip_ws(s, i)
                else:
                    self.text(" ")
                    i += 1
            elif s.startswith("---", i):
                self.text("\u2014")
                i += 3
            elif s.startswith("--", i):
                self.text("\u2013")
                i += 2
            elif s.startswith("``", i):
                self.text("\u201C")
                i += 2
            elif s.startswith("''", i):
                self.text("\u201D")
                i += 2
            elif c == "&":
                # `&` trần ngoài bảng làm LaTeX dừng hẳn ⇒ dữ liệu thật không có; gặp ở chữ do
                # chính renderer ghép (vd "MỤC TIÊU … & CHUẨN ĐẦU RA") ⇒ in đúng ký tự.
                self.text("&")
                i += 1
            else:
                self.text(c)
                i += 1

    def group(self, inner: str):
        """{…}: lệnh khai báo (\\bfseries, \\color…) bên trong chỉ có hiệu lực trong ngoặc."""
        sub = _State(self.rd, self.fmt, self.align)
        sub.run(inner)
        if not sub.out and not sub.lines:
            self.cur.extend(sub.cur)
            return
        # Ngoặc chứa cả đoạn/khối: nối dòng đầu vào đoạn đang dở, phần còn lại theo sau.
        sub.par()
        last = len(sub.out) - 1
        for k, b in enumerate(sub.out):
            if isinstance(b, P):
                self.cur.extend(b.inl)
                if b.tight:
                    self.br()
                elif k < last:          # hết một đoạn trong ngoặc; đoạn cuối nối tiếp chữ sau ngoặc
                    self.par()
            else:
                self.block(b)

    def token(self, s: str, i: int) -> int:
        m = _TOKEN.match(s, i)
        if not m:
            self.text("[")
            return i + 1
        name, arg = m.group(1), m.group(2)
        if name == "br":
            self.br()
        elif name == "fill" and self.ctx.show_solution:
            ans = (arg or "").partition("|")[0]
            f = replace(self.fmt, color="C0392B", underline=True)
            self.cur.extend(self.rd.inlines(ans, f))
        elif name in ("blank", "mblank", "fill", "oly"):
            self.text(_token_dots(name, arg))
        elif name in ("wrap", "/wrap"):
            pass          # hộp wrap đã được tách ở tầng bài (docx_renderer)
        else:
            self.ctx.lạ(f"token [[{name}]]")
        return m.end()

    # ---------- lệnh ----------
    def command(self, s: str, i: int) -> int:
        n = len(s)
        if i + 1 >= n:
            return n
        nx = s[i + 1]
        if nx == "\\":                                  # \\ hoặc \\[3pt] hoặc \\*
            j = i + 2
            if j < n and s[j] == "*":
                j += 1
            _, j = _read_opt(s, j)
            self.br()
            return j
        if nx == "(":
            j = s.find("\\)", i + 2)
            j = n if j == -1 else j
            self.cur.append(M(s[i + 2:j]))
            return j + 2
        if nx == "[":
            j = s.find("\\]", i + 2)
            j = n if j == -1 else j
            self.block(DMath(s[i + 2:j]))
            return j + 2
        if not nx.isalpha():
            sym = TEXT_SYMBOLS.get(nx)
            if sym is None:
                self.ctx.lạ(f"\\{nx}")
                sym = nx
            self.text(sym)
            return i + 2
        m = re.match(r"[A-Za-z]+\*?", s[i + 1:])
        name = m.group(0)
        star = name.endswith("*")
        name = name.rstrip("*")
        j = i + 1 + m.end()
        # Như TeX: khoảng trắng sau một lệnh chữ cái bị nuốt ("\\ldots xem" ⇒ "…xem").
        while j < len(s) and s[j] in " \t":
            j += 1
        return self.dispatch(name, star, s, j)

    def dispatch(self, name: str, star: bool, s: str, j: int) -> int:
        f = self.fmt
        # ---- ký hiệu chữ ----
        if name in TEXT_SYMBOLS:
            self.text(TEXT_SYMBOLS[name])
            return j
        if name in NOOP0:
            if name == "par":
                self.par()
            elif name == "centering":
                self.align = "center"
            elif name == "raggedright":
                self.align = "left"
            elif name == "newline" or name == "linebreak":
                self.br()
            elif name == "item":
                _, j = _read_opt(s, j)
                self.par()
                self.text("\u2022 ")
            return j
        if name in NOOP1:
            _, j = _read_opt(s, j)
            _, j = _read_arg(s, j)
            return j
        if name in ("newpage", "clearpage"):
            self.block(PageBreak())
            return j
        if name == "renewcommand":                       # \renewcommand{\arraystretch}{1.2}
            _, j = _read_arg(s, j)
            _, j = _read_arg(s, j)
            return j
        if name in ("hspace", "hskip", "kern"):
            arg, j = _read_arg(s, j)
            cm = to_cm(arg, 0.4)
            if cm > 0.05:
                self.text("\u2002" * max(1, round(cm / 0.21)))
            return j
        if name in ("hfill", "hfil"):
            self.cur.append(Tab())
            return j
        if name == "dotfill":
            self.cur.append(Tab(dots=True))
            return j
        # ---- khai báo kiểu chữ (tác dụng tới hết ngoặc) ----
        if name in ("bfseries",):
            self.fmt = replace(f, bold=True); return j
        if name in ("itshape", "slshape", "em"):
            self.fmt = replace(f, italic=not f.italic if name == "em" else True); return j
        if name == "sffamily":
            self.fmt = replace(f, sans=True); return j
        if name == "scshape":
            self.fmt = replace(f, smallcaps=True); return j
        if name in SIZES:
            self.fmt = replace(f, size=SIZES[name] if name != "normalsize" else None); return j
        if name == "color":
            arg, j = _read_arg(s, j)
            self.fmt = replace(f, color=color_hex(arg, self.ctx)); return j
        # ---- lệnh có đối số, nội dung đi qua ----
        styled = {"textbf": dict(bold=True), "textit": dict(italic=True), "textsl": dict(italic=True),
                  "emph": dict(italic=not f.italic), "underline": dict(underline=True),
                  "uline": dict(underline=True), "textsf": dict(sans=True), "textsc": dict(smallcaps=True),
                  "texttt": {}, "textsuperscript": dict(sup=True), "fbox": dict(boxed=True),
                  "framebox": dict(boxed=True)}
        if name in styled:
            if name == "framebox":
                _, j = _read_opt(s, j); _, j = _read_opt(s, j)
            arg, j = _read_arg(s, j)
            self.group_fmt(arg, replace(f, **styled[name]))
            return j
        if name == "textcolor":
            c, j = _read_arg(s, j)
            arg, j = _read_arg(s, j)
            self.group_fmt(arg, replace(f, color=color_hex(c, self.ctx)))
            return j
        if name == "colorbox":
            c, j = _read_arg(s, j)
            arg, j = _read_arg(s, j)
            self.group_fmt(arg, replace(f, shade=color_hex(c, self.ctx)))
            return j
        if name in WRAP1:
            if name in ("centerline",):
                arg, j = _read_arg(s, j)
                self.par()
                old = self.align
                self.align = "center"
                self.group(arg)
                self.par()
                self.align = old
                return j
            if name in ("hbox", "vbox", "vtop") and s.startswith(" to", j):
                mm = re.match(r"\s*to\s*[-\d.]*\\?[A-Za-z]*", s[j:])
                j += mm.end()
            arg, j = _read_arg(s, j)
            self.group(arg)
            return j
        if name in ("makebox", "parbox", "raisebox", "resizebox", "scalebox", "adjustbox"):
            return self.box_cmd(name, s, j)
        if name == "ding":
            arg, j = _read_arg(s, j)
            self.text(DING.get(int(re.sub(r"\D", "", arg) or 0), "\u2022"))
            return j
        if name == "diffstars":
            arg, j = _read_arg(s, j)
            self.cur.extend(stars(int(re.sub(r"\D", "", arg) or 0)))
            return j
        if name in ("blank", "fillblank"):
            w, j = _read_opt(s, j) if name == "blank" else _read_arg(s, j)
            self.text(dots(to_cm(w) if w else 5.0))
            return j
        if name == "fillans":
            arg, j = _read_arg(s, j)
            if self.ctx.show_solution:
                self.group_fmt(arg, replace(f, color="C0392B", underline=True))
            else:
                self.text(dots(2.5))
            return j
        if name in ("href",):
            _, j = _read_arg(s, j)
            arg, j = _read_arg(s, j)
            self.group(arg)
            return j
        if name == "url":
            arg, j = _read_arg(s, j)
            self.text(arg)
            return j
        if name == "includegraphics":
            opt, j = _read_opt(s, j)
            path, j = _read_arg(s, j)
            self.block(Fig(image=path, max_w_frac=_frac(opt, "width") or 0.55))
            return j
        if name == "begin":
            env, j = _read_arg(s, j)
            return self.env(env, s, j)
        if name == "end":
            _, j = _read_arg(s, j)
            return j
        if name in ("tikz",):
            self.ctx.lạ("\\tikz trong dòng")
            _, j = _read_opt(s, j)
            _, j = _read_arg(s, j)
            return j
        if name in ("videoqr",):
            arg, j = _read_arg(s, j)
            return j
        # ---- chưa có luật ⇒ giữ chữ trong ngoặc + báo ----
        self.ctx.lạ(f"\\{name}")
        _, j = _read_opt(s, j)
        jj = _skip_ws(s, j)
        if jj < len(s) and s[jj] == "{":
            arg, j = _read_group(s, jj)
            self.group(arg)
        return j

    def group_fmt(self, inner: str, fmt: Fmt):
        old = self.fmt
        self.fmt = fmt
        self.group(inner)
        self.fmt = old

    def box_cmd(self, name: str, s: str, j: int) -> int:
        if name == "makebox":
            _, j = _read_opt(s, j)
            _, j = _read_opt(s, j)
            arg, j = _read_arg(s, j)
            self.group(arg)
            return j
        if name == "raisebox":
            _, j = _read_arg(s, j)
            _, j = _read_opt(s, j)
            _, j = _read_opt(s, j)
            arg, j = _read_arg(s, j)
            self.group(arg)
            return j
        if name in ("resizebox", "scalebox"):
            _, j = _read_arg(s, j)
            if name == "resizebox":
                _, j = _read_arg(s, j)
            arg, j = _read_arg(s, j)
            self.group(arg)
            return j
        if name == "adjustbox":
            opts, j = _read_arg(s, j)
            arg, j = _read_arg(s, j)
            if "tikzpicture" in arg or "\\begin{forest}" in arg:
                tk = arg.strip()
                self.block(Fig(snippet=tk, max_w_frac=_frac(opts, "max width") or _frac(opts, "width") or 1.0,
                               force_w_frac=_frac(opts, "width") if "max width" not in opts else None,
                               max_h_cm=_cm_opt(opts, "max totalheight") or _cm_opt(opts, "max height")))
            else:
                self.group(arg)
            return j
        if name == "parbox":                                 # \parbox[t]{w}{…} ⇒ ô bảng
            return self.parbox_row(s, j - len("\\parbox"))
        return j

    def parbox_row(self, s: str, i: int) -> int:
        """Chuỗi \\parbox liền nhau (phương án trắc nghiệm dựng tay) ⇒ bảng không viền.
        `\\par` giữa các parbox ⇒ sang hàng mới."""
        rows: list[list[Cell]] = [[]]
        widths: list[float] = []
        j = i
        pat_gap = re.compile(r"(?:\s|\\hspace\*?\{[^{}]*\}|\\hfill|\\quad|\\qquad|~|\\par\b|\\vspace\*?\{[^{}]*\}|\\smallskip|\\medskip|\[\[br\]\])*")
        while True:
            m = re.match(r"\\parbox", s[j:])
            if not m:
                break
            j += m.end()
            _, j = _read_opt(s, j)
            w, j = _read_arg(s, j)
            body, j = _read_arg(s, j)
            frac = to_cm(w) / LINEWIDTH_CM
            rows[-1].append(Cell(self.rd.blocks(body, self.fmt, "left")))
            if len(rows) == 1:
                widths.append(frac)
            g = pat_gap.match(s, j)
            gap = g.group(0)
            if ("\\par" in gap or "[[br]]" in gap) and re.match(r"\\parbox", s[g.end():]):
                rows.append([])
            j = g.end()
            if not re.match(r"\\parbox", s[j:]):
                break
        ncol = max(len(r) for r in rows)
        for r in rows:
            while len(r) < ncol:
                r.append(Cell([]))
        widths = (widths + [widths[-1] if widths else 1 / ncol] * ncol)[:ncol]
        self.block(Tbl(rows, widths=widths, borders=False, cell_pad_pt=1, align="left"))
        return j

    # ---------- môi trường ----------
    def env(self, env: str, s: str, j: int) -> int:
        if env == "tikzpicture":
            body, k = _find_end(s, j, env)
            self.block(Fig(snippet="\\begin{tikzpicture}" + body + "\\end{tikzpicture}"))
            return k
        if env == "forest":
            body, k = _find_end(s, j, env)
            self.block(Fig(snippet="\\begin{forest}" + body + "\\end{forest}"))
            return k
        if env == "center":
            body, k = _find_end(s, j, env)
            self.par()
            for b in self.rd.blocks(body, self.fmt, "center"):
                if isinstance(b, P) and b.align == "justify":
                    b.align = "center"
                self.out.append(b)
            return k
        if env in ("flushleft", "flushright"):
            body, k = _find_end(s, j, env)
            self.par()
            self.out.extend(self.rd.blocks(body, self.fmt, "left" if env == "flushleft" else "right"))
            return k
        if env == "minipage":
            return self.minipage_row(s, j)
        if env in ("tabular", "tabularx", "array"):
            if env == "tabularx":
                _, j = _read_arg(s, j)
            _, j = _read_opt(s, j)
            spec, j = _read_arg(s, j)
            body, k = _find_end(s, j, env)
            self.block(tabular(self.rd, spec, body, self.fmt))
            return k
        if env in ("itemize", "enumerate"):
            body, k = _find_end(s, j, env)
            self.par()
            items = re.split(r"\\item\b", body)[1:]
            for no, it in enumerate(items, 1):
                bl = self.rd.blocks(it.strip(), self.fmt)
                lead = "\u2022 " if env == "itemize" else f"{no}. "
                if bl and isinstance(bl[0], P):
                    bl[0].inl.insert(0, T(lead, self.fmt))
                for b in bl:
                    if isinstance(b, P):
                        b.indent_pt, b.hanging_pt, b.align = 18, 12, "left"
                self.out.extend(bl)
            return k
        if env in ("cases", "aligned", "align", "align*", "equation", "equation*", "gather", "gather*"):
            body, k = _find_end(s, j, env)
            self.block(DMath(f"\\begin{{{env.rstrip('*')}}}{body}\\end{{{env.rstrip('*')}}}"
                             if env in ("cases", "aligned") else body))
            return k
        body, k = _find_end(s, j, env)
        self.ctx.lạ(f"môi trường {env}")
        self.par()
        self.out.extend(self.rd.blocks(body, self.fmt, self.align))
        return k

    def minipage_row(self, s: str, j: int) -> int:
        """Các minipage liền nhau (ngăn bởi \\hfill, \\hspace…) ⇒ MỘT hàng bảng không viền.
        Khuôn phổ biến nhất kho: đề trái 0,58–0,64 · hình phải 0,31–0,36."""
        cells: list[Cell] = []
        widths: list[float] = []
        k = j
        while True:
            _, k = _read_opt(s, k)            # [t]
            _, k = _read_opt(s, k)            # [height]
            _, k = _read_opt(s, k)            # [inner pos]
            w, k = _read_arg(s, k)
            body, k = _find_end(s, k, "minipage")
            bl = self.rd.blocks(body, self.fmt, "justify")
            # Ô CHỈ có hình (+ chú thích) ⇒ căn giữa như \centering của PDF.
            if any(isinstance(b, Fig) for b in bl):
                for b in bl:
                    if isinstance(b, P):
                        b.align = "center"
            cells.append(Cell(bl))
            widths.append(to_cm(w) / LINEWIDTH_CM)
            g = re.match(r"(?:\s|\\hfill|\\hfil|\\hspace\*?\{[^{}]*\}|\\quad|\\qquad|%[^\n]*\n|~)*", s[k:])
            nk = k + g.end()
            if s.startswith("\\begin{minipage}", nk):
                k = nk + len("\\begin{minipage}")
                continue
            break
        self.block(Tbl([cells], widths=widths, borders=False, cell_pad_pt=0, align="left"))
        return k


def _trim(line: list) -> list:
    """Bỏ khoảng trắng đầu/cuối một dòng."""
    while line and isinstance(line[0], T) and not line[0].text.strip(" \u2002\u2003"):
        line.pop(0)
    while line and isinstance(line[-1], T) and not line[-1].text.strip(" \u2002\u2003"):
        line.pop()
    if line and isinstance(line[0], T):
        line[0] = T(line[0].text.lstrip(" "), line[0].fmt)
    if line and isinstance(line[-1], T):
        line[-1] = T(line[-1].text.rstrip(" "), line[-1].fmt)
    return line


def _frac(opts: str | None, key: str) -> float | None:
    if not opts:
        return None
    m = re.search(re.escape(key) + r"\s*=\s*([\d.]*)\s*\\(?:linewidth|textwidth)", opts)
    if m:
        return float(m.group(1) or 1)
    m = re.search(re.escape(key) + r"\s*=\s*([\d.]+\s*(?:cm|mm|in|pt))", opts)
    if m:
        return to_cm(m.group(1)) / LINEWIDTH_CM
    return None


def _cm_opt(opts: str | None, key: str) -> float | None:
    m = re.search(re.escape(key) + r"\s*=\s*([\d.]+\s*(?:cm|mm|in|pt))", opts or "")
    return to_cm(m.group(1)) if m else None


# ───────────────────────── màu ─────────────────────────
_COLORS: dict[str, str] = {}


def set_palette(colors: dict[str, str]):
    _COLORS.clear()
    _COLORS.update({k: v.upper() for k, v in colors.items()})
    _COLORS.update({"black": "000000", "white": "FFFFFF", "red": "FF0000", "blue": "0000FF",
                    "gray": "808080", "green": "008000", "orange": "FF8000"})


def color_hex(spec: str, ctx: Ctx | None = None) -> str | None:
    """'brand' · 'brand!40' · 'black!60' · 'brand!85!black' ⇒ hex (pha như xcolor)."""
    spec = (spec or "").strip()
    parts = spec.split("!")
    base = _COLORS.get(parts[0])
    if base is None:
        if re.fullmatch(r"[0-9A-Fa-f]{6}", parts[0]):
            base = parts[0].upper()
        else:
            if ctx:
                ctx.lạ(f"màu {spec}")
            return None
    if len(parts) >= 2:
        pct = float(parts[1])
        other = _COLORS.get(parts[2], "FFFFFF") if len(parts) >= 3 else "FFFFFF"
        from src.compiler.docx_xml import mix
        base = mix(base, pct, other)
    return base


def stars(level: int) -> list:
    """\\diffstars: 1–3 ★ vàng đủ/rỗng, 4 = ◆◆◆◆ màu kim cương (y bản PDF)."""
    gold, dia = _COLORS.get("gold", "F39C12"), _COLORS.get("diamond", "06B6D4")
    if level >= 4:
        return [T("\u2605\u2605\u2605\u2605", Fmt(color=dia, size=10))]
    full = max(1, level)
    return [T("\u2605" * full + "\u2606" * (3 - full), Fmt(color=gold, size=10))]


# ───────────────────────── tabular ─────────────────────────
def _split_top(s: str, sep: str) -> list[str]:
    """Tách theo `sep` ở tầng ngoài cùng (không trong {}, không trong $…$)."""
    out, buf, depth, i, math = [], [], 0, 0, False
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            if sep == "\\\\" and s[i + 1] == "\\" and depth == 0 and not math:
                out.append("".join(buf))
                buf = []
                i += 2
                _, i = _read_opt(s, i)
                continue
            buf.append(s[i:i + 2])
            i += 2
            continue
        if c == "$":
            math = not math
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == sep and depth == 0 and not math:
            out.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    out.append("".join(buf))
    return out


def _colspec(spec: str) -> tuple[list[str], list[float | None], bool]:
    """'|c|p{7.4cm}|c|' ⇒ (căn lề từng cột, bề rộng cm|None, có kẻ dọc?)."""
    aligns, widths = [], []
    vbar = "|" in spec
    i = 0
    while i < len(spec):
        c = spec[i]
        if c in "lcr":
            aligns.append({"l": "left", "c": "center", "r": "right"}[c])
            widths.append(None)
        elif c in "pmbX":
            if c == "X":
                aligns.append("left"); widths.append(None)
            else:
                w, i = _read_group(spec, i + 1)
                aligns.append("left"); widths.append(to_cm(w))
                continue
        elif c in "@>!<":
            if i + 1 < len(spec) and spec[i + 1] == "{":
                _, i = _read_group(spec, i + 1)
                continue
        elif c == "*":
            cnt, i = _read_group(spec, i + 1)
            rep, i = _read_group(spec, i)
            a, w, v = _colspec(rep)
            aligns += a * int(cnt); widths += w * int(cnt)
            continue
        i += 1
    return aligns, widths, vbar


def tabular(rd: Reader, spec: str, body: str, fmt: Fmt) -> Tbl:
    aligns, wcm, vbar = _colspec(spec)
    ncol = max(1, len(aligns))
    hline = "\\hline" in body
    rows: list[list[Cell]] = []
    for raw in _split_top(body, "\\\\"):
        raw = re.sub(r"\\(?:hline|cline\{[^{}]*\}|toprule|midrule|bottomrule)", "", raw)
        raw = re.sub(r"\\(?:rowcolor)\{[^{}]*\}", "", raw)
        if not raw.strip():
            continue
        cells = []
        for k, c in enumerate(_split_top(raw, "&")):
            span, al = 1, None
            c = c.strip()
            m = re.match(r"\\multicolumn\s*\{(\d+)\}", c)
            if m:
                span = int(m.group(1))
                rest = c[m.end():]
                sp, p2 = _read_arg(rest, 0)
                content, _ = _read_arg(rest, p2)
                a, _, _ = _colspec(sp)
                al = a[0] if a else None
                c = content
            col = sum(x.span for x in cells)
            bl = rd.blocks(c, fmt, al or (aligns[col] if col < len(aligns) else "left"))
            for b in bl:
                if isinstance(b, P):
                    b.align = al or (aligns[col] if col < len(aligns) else "left")
            cells.append(Cell(bl, span=span, align=al))
        rows.append(cells)
    widths = None
    if any(w is not None for w in wcm):
        known = sum(w for w in wcm if w)
        free = [i for i, w in enumerate(wcm) if w is None]
        rest_cm = max(0.0, LINEWIDTH_CM - known)
        each = rest_cm / len(free) if free else 0
        each = min(each, 2.5)
        widths = [(w if w else each) / LINEWIDTH_CM for w in wcm]
    return Tbl(rows, widths=widths, borders=vbar or hline, header_rows=0)
