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
from src.schema.tier_spec import draw_minutes, load_tier_spec


def _has_ve_hinh(spec: ThuyetMinhSpec) -> bool:
    """Spec có dòng nào khai hình HS phải tự vẽ không (để chú thích cột TG)."""
    return any(sum(r.ve_hinh.values()) for p in spec.phieu for r in p.rows)

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
    # Cột dạng NỚI RỘNG (10,4cm) + cột số HẸP LẠI (1,45cm) — giữ nguyên bề ngang bảng
    # nhưng bớt dòng dạng bị xuống 2 dòng, để mỗi buổi gọn TRONG MỘT TRANG (Thầy đọc
    # 1 buổi = 1 trang, không phải lật sang trang chỉ để xem dòng TỔNG).
    # Cột LOẠI (§4b — 'NB tách TH', 'NB lẻ LT'…) chỉ in khi spec có khai `loai`; spec cũ
    # không khai ⇒ bảng giữ nguyên 9 cột như trước.
    has_loai = any((r.loai or "").strip() for r in phieu.rows)
    ncol = 10 if has_loai else 9
    col = (rf"|>{{\RaggedRight\arraybackslash}}p{{{'8.3cm' if has_loai else '10.4cm'}}}|"
           + (r">{\centering\arraybackslash}p{2.1cm}|" if has_loai else "")
           + r"*{8}{>{\centering\arraybackslash}p{1.45cm}|}")
    lead = r"\rowcolor{neutral} & " if has_loai else r"\rowcolor{neutral} "
    cline = rf"\cline{{{3 if has_loai else 2}-{ncol}}}"
    loai_h = r"& \sffamily\footnotesize\bfseries Loại " if has_loai else ""
    head = [
        lead + r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Lý thuyết} "
               r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Ví dụ} "
               r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries Bài tập trên lớp} "
               r"& \multicolumn{2}{>{\columncolor{neutral}}c|}{\sffamily\bfseries BTVN} \\ " + cline,
        r"\rowcolor{neutral}\multirow{-2}{*}{\sffamily\bfseries Dạng bài} " + loai_h +
        r"& \sffamily\footnotesize Số mục & \sffamily\footnotesize TG "
        r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
        r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG "
        r"& \sffamily\footnotesize Số câu & \sffamily\footnotesize TG \\ \hline",
    ]
    L = [r"\begingroup\footnotesize\renewcommand{\arraystretch}{1.0}", rf"\begin{{longtable}}{{{col}}}", r"\arrayrulecolor{rule}\hline"]
    L += head + [r"\endfirsthead"] + head + [r"\endhead"]

    grand = [0.0] * 8  # xen kẽ (n, phút) ×4 đoạn
    for band in _BAND_ORDER:
        rows = [r for r in phieu.rows if r.band == band]
        if not rows:
            continue
        label, tint, star = _BAND_HEAD[band]
        L.append(rf"\multicolumn{{{ncol}}}{{|l|}}{{\cellcolor{{{tint}!16}}\sffamily\bfseries"
                 rf"\color{{{tint}}}{label} ({star})}} \\ \hline")
        sub = [0.0] * 8
        # Đánh số dạng trong nhóm (NB1, NB2…, TH1…, VD1) — Thầy cần một CÁI TÊN để trỏ
        # khi soi phiếu thật; phiếu in thẻ [NB]/[TH]/[VD] ở từng câu để đối chiếu.
        for idx, r in enumerate(rows, 1):
            r = r.model_copy(update={"dang": rf"{{\sffamily\bfseries\color{{{tint}}}"
                                             rf"{band}{idx}.}}~{r.dang}"})
            mins = row_minutes(r, rates)          # đã gồm phút vẽ hình (ve_hinh)
            lt_m = r.lythuyet * rates.get("vidu", {}).get(band, 0)
            vals = [(r.lythuyet, lt_m), (r.vidu, mins["vidu"]),
                    (r.onclass, mins["onclass"]), (r.btvn, mins["btvn"])]
            cells = []
            for i, (n, m) in enumerate(vals):
                cells += [_n(n), _t(m)]
                sub[2 * i] += n
                sub[2 * i + 1] += m
            lo = (rf"{{\scriptsize {r.loai}}} & " if has_loai else "")
            L.append(f"{r.dang} & " + lo + " & ".join(cells) + r" \\ \hline")
        for i in range(8):
            grand[i] += sub[i]
        subcells = " & ".join(
            (rf"\itshape {_n(int(sub[2*i]))}" if i < 2 else rf"\bfseries {_n(int(sub[2*i]))}") + " & " +
            (rf"\itshape {_t(sub[2*i+1])}" if i < 2 else rf"\bfseries {_t(sub[2*i+1])}")
            for i in range(4)
        )
        L.append(rf"\multicolumn{{{ncol - 8}}}{{|r|}}{{\itshape\bfseries Cộng nhóm}} & {subcells} \\ \hline")

    gcells = " & ".join(rf"\bfseries {_n(int(grand[2*i]))} & \bfseries {_t(grand[2*i+1])}" for i in range(4))
    L.append(rf"\rowcolor{{brand!12}}\multicolumn{{{ncol - 8}}}{{|r|}}"
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
    # Nhãn khối theo spec.grade — trước đây cứng "Lớp 9 (Ôn vào 10)" nên spec lớp 8 in sai khối.
    khoi = "Lớp 9 (Ôn vào 10)" if spec.grade == "lop-9" else spec.grade.replace("lop-", "Lớp ")

    parts = [
        rf"\tmtitle{{PHIẾU THUYẾT MINH}}\quad\tmsub{{{spec.title} • {khoi}{badge}{tuan}}}",
        r"\par\vspace{4pt}",
        _meta_table([
            ("Tên bài", f"\\textbf{{{spec.title}}}{badge}." +
             ("".join(f" \\textbf{{Phiếu {p.code}}} — {p.title};" for p in spec.phieu)).rstrip(";")),
            ("Thời gian", f"\\textbf{{1 ca $=$ {info.get('session_minutes')} phút}} "
                          f"(trừ giải lao {info.get('break_minutes')}′): GV giảng "
                          f"$\\approx${round(info.get('budgets',{}).get('vidu',0))}′ $+$ Luyện tập "
                          f"{round(info.get('budgets',{}).get('onclass',0))}′. "
                          f"BTVN $\\approx${round(info.get('budgets',{}).get('btvn',0))}′ ở nhà."),
        ] + ([("Thời lượng", " \\quad$\\bullet$\\quad ".join(spec.thoiluong))]
             if spec.thoiluong else [])),
        r"\tmsec{MỤC TIÊU LÝ THUYẾT \& CHUẨN ĐẦU RA}", _itemize(spec.lythuyet),
        r"\tmsec{BÀI TẬP}",
        r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Ví dụ GV làm mẫu:}" + _itemize(spec.vidu) +
        r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Dạng VẬN DỤNG trong đề:}" +
        _itemize(spec.dang_vd) + r"\end{minipage}",
        r"\par\vspace{4pt}",
        r"\begin{minipage}[t]{0.485\linewidth}\tmlbl{Lỗi sai thường gặp:}" + _itemize(spec.loisai) +
        r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}\tmlbl{Kiến thức NHẬN BIẾT cần nhớ:}" +
        _itemize(spec.kienthuc_nb) + r"\end{minipage}",
    ]
    for p in spec.phieu:
        table, grand = _phieu_table(p, rates)
        parts += [r"\newpage", rf"\tmsec{{NỘI DUNG PHIẾU — PHIẾU {p.code}: {p.title}}}", table,
                  _canbuoi(grand, info)]
    # Chú thích quy ước ĐẶT CUỐI tài liệu: để cuối phần mục tiêu thì nó hay bị đẩy
    # sang một trang trắng riêng (trang 2 vừa kín) — Thầy nhận được PDF thừa 1 trang.
    parts.append(
        r"\par\vspace{8pt}{\footnotesize\color{muted}\itshape Quy ước đếm: "
        r"``câu'' $=$ ý nhỏ a),b)…; thời gian tự tính theo phút/câu của tier\_spec.json "
        r"(NB/TH/VD/VDC). duration\_gate chỉ soi Luyện tập trên lớp $+$ BTVN."
        + (rf" Cột TG đã CỘNG {draw_minutes(load_tier_spec()):.0f}′ cho mỗi hình học sinh "
           r"phải tự vẽ (cột \texttt{ve\_hinh} của dạng)." if _has_ve_hinh(spec) else "")
        + (r" \textbf{Cột Loại} — câu \emph{lẻ LT} hỏi thẳng công thức vừa học; câu "
           r"\emph{tách TH} là bước đệm cắt ra từ chính bài Thông hiểu bên dưới; câu "
           r"\emph{ghép bài} là các ý a), b) mở đầu của một bài lớn, học sinh làm liền "
           r"mạch trong CÙNG một bài chứ không phải bài rời."
           if any((r.loai or "").strip() for p in spec.phieu for r in p.rows) else "")
        + r"}")

    # Thiếu cột Loại thì phải NHÌN THẤY trên PDF — trước đây cột tự biến mất, Thầy đọc
    # bảng không có gì báo là đang thiếu (xem thuyetminh_gate.check_loai_4b).
    _thieu = sum(1 for p in spec.phieu for r in p.rows
                 if not (r.loai or "").strip() or (r.loai or "").strip().startswith("TODO"))
    if _thieu:
        parts.append(rf"\vspace{{2pt}}{{\color{{brand}}\sffamily\bfseries\footnotesize "
                     rf"CHƯA KHAI LOẠI CÂU HỎI (\S4b) cho {_thieu} dòng — "
                     rf"bảng còn thiếu cột \emph{{Loại}} (NB lẻ LT / NB tách TH / NB ghép bài / "
                     rf"TH lẻ LT / TH ghép bài / TH tách VD / VD lẻ).}}")

    tokens = load_tokens()
    return _env().get_template("base_thuyetminh.tex.j2").render(body="\n\n".join(parts), **tokens)
