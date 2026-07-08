"""Render PHIẾU THUYẾT MINH (spec) → LaTeX (A4 ngang) dùng base_thuyetminh.tex.j2.

Tổng quát hoá script một-lần scripts/build_thuyetminh_tuan10_11.py: số câu lấy từ
ThuyetMinhSpec, THỜI GIAN + tổng + cân buổi TỰ TÍNH từ config/tier_spec.json
(không gõ tay). Bảng nhóm theo band NB/TH/VD/VDC.
"""
from __future__ import annotations

from src.compiler.jinja_renderer import _env, load_tokens
from src.schema.thuyetminh_spec import (
    ThuyetMinhSpec, rates_for_spec, row_minutes, session_info,
)

# band → (nhãn, màu tint, sao)
_BAND_HEAD = {
    "NB":  ("NHẬN BIẾT — NB", "stage1", r"$\bigstar$"),
    "TH":  ("THÔNG HIỂU — TH", "stage2", r"$\bigstar\bigstar$"),
    "VD":  ("VẬN DỤNG — VD", "stage3", r"$\bigstar\bigstar\bigstar$"),
    "VDC": ("VẬN DỤNG CAO — VDC", "stage4", r"$\bigstar\bigstar\bigstar\bigstar$"),
}
_BAND_ORDER = ["NB", "TH", "VD", "VDC"]


def _n(x: int) -> str:
    return str(x) if x else "—"


def _t(m: float) -> str:
    return f"{round(m)}′" if m else "—"


def _itemize(items: list[str]) -> str:
    if not items:
        return ""
    body = "\n".join(rf"  \item {x}" for x in items)
    return "\\begin{itemize}\n" + body + "\n\\end{itemize}"


def _meta_table(rows: list[tuple[str, str]]) -> str:
    out = [r"\begin{tabular}{|>{\sffamily\bfseries\color{ink}}p{3.4cm}|"
           r">{\RaggedRight\arraybackslash}p{22.4cm}|}", r"\arrayrulecolor{rule}\hline"]
    for lbl, val in rows:
        out.append(f"{lbl} & {val} \\\\ \\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def _phieu_table(phieu, rates):
    col = (r"|>{\RaggedRight\arraybackslash}p{8.4cm}|"
           r"*{8}{>{\centering\arraybackslash}p{1.7cm}|}")
    L = [r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.06}", rf"\begin{{longtable}}{{{col}}}", r"\arrayrulecolor{rule}\hline"]
    L.append(r"\rowcolor{neutral} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Lý thuyết} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Ví dụ} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Bài tập trên lớp} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries BTVN} \\ \cline{2-9}")
    L.append(r"\rowcolor{neutral}\multirow{-2}{*}{\sffamily\bfseries Dạng bài} "
             r"& \sffamily\footnotesize Số mục & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG \\ \hline")
    L.append(r"\endfirsthead")
    L.append(r"\rowcolor{neutral} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Lý thuyết} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Ví dụ} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Bài tập trên lớp} "
             r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries BTVN} \\ \cline{2-9}")
    L.append(r"\rowcolor{neutral}\multirow{-2}{*}{\sffamily\bfseries Dạng bài} "
             r"& \sffamily\footnotesize Số mục & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
             r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG \\ \hline")
    L.append(r"\endhead")

    grand = [0.0] * 8  # xen kẽ (n, phút) ×4 đoạn
    for band in _BAND_ORDER:
        rows = [r for r in phieu.rows if r.band == band]
        if not rows:
            continue
        label, tint, star = _BAND_HEAD[band]
        L.append(rf"\multicolumn{{9}}{{|l|}}{{\cellcolor{{{tint}!16}}\sffamily\bfseries"
                 rf"\color{{{tint}}}{label} ({star})}} \\ \hline")
        sub = [0.0] * 8
        for r in rows:
            mins = row_minutes(r, rates)
            lt_m = r.lythuyet * rates.get("vidu", {}).get(band, 0)
            ex_m = r.vidu * rates.get("vidu", {}).get(band, 0)
            vals = [(r.lythuyet, lt_m), (r.vidu, ex_m), (r.onclass, mins["onclass"]), (r.btvn, mins["btvn"])]
            cells = []
            for i, (n, m) in enumerate(vals):
                cells += [_n(n), _t(m)]
                sub[2 * i] += n
                sub[2 * i + 1] += m
            L.append(f"{r.dang} & " + " & ".join(cells) + r" \\ \hline")
        for i in range(8):
            grand[i] += sub[i]
        subcells = " & ".join(
            (rf"\itshape {_n(int(sub[2*i]))}" if i < 2 else rf"\bfseries {_n(int(sub[2*i]))}") + " & " +
            (rf"\itshape {_t(sub[2*i+1])}" if i < 2 else rf"\bfseries {_t(sub[2*i+1])}")
            for i in range(4)
        )
        L.append(rf"\multicolumn{{1}}{{|r|}}{{\itshape\bfseries Cộng nhóm}} & {subcells} \\ \hline")

    gcells = " & ".join(rf"\bfseries {_n(int(grand[2*i]))} & \bfseries {_t(grand[2*i+1])}" for i in range(4))
    L.append(rf"\rowcolor{{brand!12}}\multicolumn{{1}}{{|r|}}"
             rf"{{\sffamily\bfseries\color{{brand}}TỔNG}} & {gcells} \\ \hline")
    L.append(r"\end{longtable}\endgroup")
    return "\n".join(L), grand


def _canbuoi(grand, info) -> str:
    """Dòng cân buổi: GV giảng (lý thuyết+ví dụ) + luyện tập + BTVN."""
    gv = grand[1] + grand[3]
    onclass, btvn = grand[5], grand[7]
    b = info.get("budgets", {})
    return (rf"\par\vspace{{3pt}}{{\small\textbf{{\color{{brand}}Cân buổi:}} "
            rf"Ví dụ/lý thuyết (GV giảng) $\approx${round(gv)}′ (quỹ {round(b.get('vidu',0))}′) "
            rf"$+$ Luyện tập {round(onclass)}′ (quỹ {round(b.get('onclass',0))}′) tại lớp. "
            rf"BTVN $\approx${round(btvn)}′ (quỹ {round(b.get('btvn',0))}′) ở nhà.}}")


def render_thuyetminh(spec: ThuyetMinhSpec) -> str:
    rates = rates_for_spec(spec)
    info = session_info(spec)
    badge = f" \\textbf{{(LỚP {spec.tier})}}" if spec.tier else ""
    tuan = f" • Tuần {spec.tuan}" if spec.tuan else ""

    parts = [
        rf"\tmtitle{{PHIẾU THUYẾT MINH}}\quad\tmsub{{{spec.title} • Lớp 9 (Ôn vào 10){badge}{tuan}}}",
        r"\par\vspace{4pt}",
        _meta_table([
            ("Tên bài", f"\\textbf{{{spec.title}}}{badge}." +
             ("".join(f" \\textbf{{Phiếu {p.code}}} — {p.title};" for p in spec.phieu)).rstrip(";")),
            ("Thời gian", f"\\textbf{{1 ca $=$ {info.get('session_minutes')} phút}} "
                          f"(trừ giải lao {info.get('break_minutes')}′): GV giảng "
                          f"$\\approx${round(info.get('budgets',{}).get('vidu',0))}′ $+$ Luyện tập "
                          f"{round(info.get('budgets',{}).get('onclass',0))}′. "
                          f"BTVN $\\approx${round(info.get('budgets',{}).get('btvn',0))}′ ở nhà."),
        ]),
        r"\tmsec{MỤC TIÊU LÝ THUYẾT \& CHUẨN ĐẦU RA}", _itemize(spec.lythuyet),
        r"\tmsec{BÀI TẬP}",
        r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Ví dụ GV làm mẫu:}" + _itemize(spec.vidu) +
        r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Dạng VẬN DỤNG trong đề:}" +
        _itemize(spec.dang_vd) + r"\end{minipage}",
        r"\par\vspace{4pt}",
        r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Lỗi sai thường gặp:}" + _itemize(spec.loisai) +
        r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Kiến thức NHẬN BIẾT cần nhớ:}" +
        _itemize(spec.kienthuc_nb) + r"\end{minipage}",
        r"\par\vspace{8pt}{\footnotesize\color{muted}\itshape Quy ước đếm: "
        r"``câu'' $=$ ý nhỏ a),b)…; thời gian tự tính theo phút/câu của tier\_spec.json "
        r"(NB/TH/VD/VDC). duration\_gate chỉ soi Luyện tập trên lớp $+$ BTVN.}"
    ]
    for p in spec.phieu:
        table, grand = _phieu_table(p, rates)
        parts += [r"\newpage", rf"\tmsec{{NỘI DUNG PHIẾU — PHIẾU {p.code}: {p.title}}}", table,
                  _canbuoi(grand, info)]

    tokens = load_tokens()
    return _env().get_template("base_thuyetminh.tex.j2").render(body="\n\n".join(parts), **tokens)
