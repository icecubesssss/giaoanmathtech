"""Render THUYẾT MINH ĐỀ KIỂM TRA (DeSpec) → LaTeX (A4 ngang).

Dùng LẠI `base_thuyetminh.tex.j2` (template chỉ nhận `body` thô) nên không phải thêm
template mới — Thầy đọc hai tài liệu cùng một bộ mặt.

Mỗi đề = một bảng: Câu | Dạng | Hình thức | Mức | Điểm | Phút | Đáp số, kèm dòng cộng
theo mức và dòng cân đề. Cuối tài liệu là MA TRẬN gộp cả chương (điểm theo mức × đề).
"""
from __future__ import annotations

from src.compiler.jinja_renderer import _env, load_tokens
from src.schema.de_spec import DeSpec, band_share, de_totals
from src.schema.tier_spec import load_tier_spec, tier_ratio

_BAND_HEAD = {
    "NB":  ("NHẬN BIẾT — NB", "stage1", r"$\bigstar$"),
    "TH":  ("THÔNG HIỂU — TH", "stage2", r"$\bigstar\bigstar$"),
    "VD":  ("VẬN DỤNG — VD", "stage3", r"$\bigstar\bigstar\bigstar$"),
    "VDC": ("VẬN DỤNG CAO — VDC", "stage4", r"$\bigstar\bigstar\bigstar\bigstar$"),
}
_BAND_ORDER = ["NB", "TH", "VD", "VDC"]


def _d(x: float) -> str:
    """Điểm: bỏ số 0 thừa, dùng dấu phẩy thập phân kiểu Việt."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return (s or "0").replace(".", ",")


def _t(m: float) -> str:
    """Phút: giữ nửa phút (2,5′). Làm tròn về số nguyên thì cột con cộng lại
    KHÔNG khớp dòng tổng — Thầy đọc bảng thấy lệch ngay."""
    if not m:
        return "—"
    s = f"{m:.1f}".rstrip("0").rstrip(".")
    return s.replace(".", ",") + "′"


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


def _de_table(de) -> str:
    col = (r"|>{\centering\arraybackslash}p{1.9cm}"
           r"|>{\RaggedRight\arraybackslash}p{12.2cm}"
           r"|>{\centering\arraybackslash}p{2.6cm}"
           r"|>{\centering\arraybackslash}p{1.6cm}"
           r"|>{\centering\arraybackslash}p{1.6cm}"
           r"|>{\RaggedRight\arraybackslash}p{4.6cm}|")
    head = (r"\rowcolor{neutral}\sffamily\bfseries Câu & \sffamily\bfseries Dạng bài "
            r"& \sffamily\bfseries Hình thức & \sffamily\bfseries Điểm "
            r"& \sffamily\bfseries Phút & \sffamily\bfseries Đáp số \\ \hline")
    L = [r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.0}",
         rf"\begin{{longtable}}{{{col}}}", r"\arrayrulecolor{rule}\hline",
         head, r"\endfirsthead", head, r"\endhead"]

    for band in _BAND_ORDER:
        rows = [c for c in de.cau if c.band == band]
        if not rows:
            continue
        label, tint, star = _BAND_HEAD[band]
        L.append(rf"\multicolumn{{6}}{{|l|}}{{\cellcolor{{{tint}!16}}\sffamily\bfseries"
                 rf"\color{{{tint}}}{label} ({star})}} \\ \hline")
        sd = sp = 0.0
        for c in rows:
            sd += c.diem
            sp += c.phut
            L.append(rf"{{\sffamily\bfseries\color{{{tint}}}{c.ma}}} & {c.dang} & "
                     rf"{{\scriptsize {c.hinh_thuc}}} & {_d(c.diem)} & {_t(c.phut)} & "
                     rf"{{\scriptsize {c.dap_an or '—'}}} \\ \hline")
        L.append(rf"\multicolumn{{3}}{{|r|}}{{\itshape\bfseries Cộng mức}} & "
                 rf"\bfseries {_d(sd)} & \bfseries {_t(sp)} & \\ \hline")

    t = de_totals(de)
    L.append(rf"\rowcolor{{brand!12}}\multicolumn{{3}}{{|r|}}"
             rf"{{\sffamily\bfseries\color{{brand}}TỔNG}} & \bfseries {_d(t['tong_diem'])} & "
             rf"\bfseries {_t(t['tong_phut'])} & \\ \hline")
    L.append(r"\end{longtable}\endgroup")
    return "\n".join(L)


def _cande(de) -> str:
    """Dòng cân đề: điểm theo mức + giờ làm bài so thời gian đề."""
    t = de_totals(de)
    s = band_share(de)
    phan = " · ".join(f"{b} {_d(t['diem'][b])}đ ({s[b]:.0f}\\%)"
                      for b in _BAND_ORDER if t["diem"][b])
    return (rf"\par\vspace{{3pt}}{{\small\textbf{{\color{{brand}}Cân đề:}} "
            rf"{phan}. Học sinh làm $\approx${_t(t['tong_phut'])} "
            rf"trong {de.phut}′ đề — dư {_t(de.phut - t['tong_phut'])} đọc đề và soát lại.}}")


def _ma_tran(spec: DeSpec) -> str:
    """Bảng gộp cả chương: mỗi đề một dòng, điểm theo mức."""
    col = (r"|>{\RaggedRight\arraybackslash}p{9.0cm}"
           r"|>{\centering\arraybackslash}p{1.7cm}"
           r"|>{\centering\arraybackslash}p{1.7cm}"
           r"|*{4}{>{\centering\arraybackslash}p{1.9cm}|}")
    L = [r"\begingroup\footnotesize", rf"\begin{{tabular}}{{{col}}}", r"\arrayrulecolor{rule}\hline",
         r"\rowcolor{neutral}\sffamily\bfseries Đề & \sffamily\bfseries Tuần "
         r"& \sffamily\bfseries Phút & \sffamily\bfseries NB & \sffamily\bfseries TH "
         r"& \sffamily\bfseries VD & \sffamily\bfseries Tổng \\ \hline"]
    tot = {b: 0.0 for b in _BAND_ORDER}
    for de in spec.de:
        t = de_totals(de)
        for b in _BAND_ORDER:
            tot[b] += t["diem"][b]
        L.append(f"{de.ten} & {de.tuan} & {de.phut}′ & "
                 + " & ".join(_d(t["diem"][b]) for b in ("NB", "TH", "VD"))
                 + rf" & \bfseries {_d(t['tong_diem'])} \\ \hline")
    grand = sum(tot.values())
    pct = " & ".join(rf"\bfseries {tot[b]/grand*100:.0f}\%" if grand else "—"
                     for b in ("NB", "TH", "VD"))
    L.append(rf"\rowcolor{{brand!12}}\multicolumn{{3}}{{|r|}}"
             rf"{{\sffamily\bfseries\color{{brand}}Tỉ trọng điểm cả chương}} & {pct} & "
             rf"\bfseries {_d(grand)} \\ \hline")
    L += [r"\end{tabular}", r"\endgroup"]
    return "\n".join(L)


def render_de(spec: DeSpec) -> str:
    badge = f" \\textbf{{(LỚP {spec.tier})}}" if spec.tier else ""
    khoi = "Lớp 9 (Ôn vào 10)" if spec.grade == "lop-9" else spec.grade.replace("lop-", "Lớp ")
    ratio = tier_ratio(load_tier_spec(), spec.grade, spec.subject, spec.tier) or {}
    chuan = " · ".join(f"{b} {ratio[b]:.0f}\\%" for b in ("NB", "TH", "VD") if ratio.get(b))

    tong_phut = sum(d.phut for d in spec.de)
    parts = [
        rf"\tmtitle{{THUYẾT MINH ĐỀ KIỂM TRA}}\quad\tmsub{{{spec.title} • {khoi}{badge}}}",
        r"\par\vspace{4pt}",
        _meta_table([
            ("Phạm vi", f"\\textbf{{{spec.chuong or spec.title}}}{badge} — "
                        f"{len(spec.de)} đề, tổng {tong_phut} phút làm bài."),
            ("Chuẩn tầng", f"Tỉ lệ mục tiêu của tầng {spec.tier}: {chuan}. "
                           f"Đề kiểm tra được dồn VD nhiều hơn phiếu tối đa 10 điểm phần trăm."),
        ] + ([("Danh sách đề", " \\quad$\\bullet$\\quad ".join(
            f"\\textbf{{{d.ma}}} (tuần {d.tuan}, {d.phut}′) — {d.ten}" for d in spec.de))]
            if spec.de else [])),
        r"\tmsec{NGUYÊN TẮC RA ĐỀ}", _itemize(spec.ghi_chu),
        r"\tmsec{MA TRẬN ĐIỂM CẢ CHƯƠNG}", _ma_tran(spec),
    ]
    for de in spec.de:
        parts += [r"\newpage",
                  rf"\tmsec{{ĐỀ {de.ma} — {de.ten} · tuần {de.tuan} · {de.phut} phút · "
                  rf"thang {_d(de.diem_toi_da)} điểm}}"]
        if de.pham_vi:
            parts.append(rf"{{\small\tmlbl{{Phạm vi:}} {de.pham_vi}}}\par\vspace{{3pt}}")
        parts += [_de_table(de), _cande(de)]

    parts.append(
        r"\par\vspace{8pt}{\footnotesize\color{muted}\itshape Quy ước: cột "
        r"\textbf{Phút} là thời gian ước cho học sinh tầng " + spec.tier +
        r" làm bài, đã trừ phần đọc đề; de\_gate chặn khi tổng phút vượt thời gian đề "
        r"hoặc tổng điểm lệch thang điểm. Cột \textbf{Đáp số} để Thầy soát nhanh, "
        r"KHÔNG in vào đề của học sinh.}")

    tokens = load_tokens()
    return _env().get_template("base_thuyetminh.tex.j2").render(body="\n\n".join(parts), **tokens)
