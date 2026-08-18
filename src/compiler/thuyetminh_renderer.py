"""Render PHIẾU THUYẾT MINH (spec) → LaTeX (A4 ngang) dùng base_thuyetminh.tex.j2.

Tổng quát hoá script một-lần scripts/build_thuyetminh_tuan10_11.py: số câu lấy từ
ThuyetMinhSpec, THỜI GIAN + tổng + cân buổi TỰ TÍNH từ config/tier_spec.json
(không gõ tay). Bảng nhóm theo band NB/TH/VD/VDC.
"""
from __future__ import annotations

from src.compiler.jinja_renderer import _env, load_tokens
from src.schema.thuyetminh_spec import (
    META_MARK_BEGIN, META_MARK_END,
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


def _cell_lines(items: list[str], plain_first: bool = False) -> str:
    """Mỗi mục MỘT DÒNG trong ô bảng đầu (có chấm đầu dòng, trừ dòng đầu nếu plain_first).

    VÌ SAO: trước 14/08/2026 sáu phiếu bị nối bằng dấu ';' và `thoiluong` nối bằng
    ' \\quad$\\bullet$\\quad ' nên cả ô dồn thành MỘT ĐOẠN VĂN dài không ngắt dòng —
    Thầy đọc bảng đầu thuyết minh thấy 'có dấu bullet mà lại không xuống dòng, RẤT KHÓ
    ĐỌC'. `thuyetminh_gate.check_meta_wrap` gác để lỗi này không quay lại.
    """
    if not items:
        return ""
    lines = [x if (plain_first and i == 0) else rf"$\bullet$~{x}"
             for i, x in enumerate(items)]
    return r" \newline ".join(lines)


def _meta_table(rows: list[tuple[str, str]]) -> str:
    out = [META_MARK_BEGIN,
           r"\begin{tabular}{|>{\sffamily\bfseries\color{ink}}p{3.4cm}|"
           r">{\RaggedRight\arraybackslash}p{22.4cm}|}", r"\arrayrulecolor{rule}\hline"]
    for lbl, val in rows:
        out.append(f"{lbl} & {val} \\\\ \\hline")
    out += [r"\end{tabular}", META_MARK_END]
    return "\n".join(out)


def _phieu_table(phieu, rates, info):
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
    L = [r"\begingroup\footnotesize\renewcommand{\arraystretch}{0.94}", rf"\begin{{longtable}}{{{col}}}", r"\arrayrulecolor{rule}\hline"]
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
            # Nhãn giàn giáo + TRÍCH DẪN in ngay dưới tên dạng — Thầy chốt 14/08/2026:
            # "KHÔNG BỊA ĐỀ… phải trích dẫn NGAY TRONG phiếu thuyết minh". Trước đây
            # source_refs chỉ nằm trong JSON, Thầy đọc PDF không thấy nguồn đâu cả.
            tag = {"ve-hinh": r"~{\scriptsize\color{stage2}[giàn giáo: vẽ hình]}",
                   "dien-khuyet": r"~{\scriptsize\color{stage2}[giàn giáo: điền khuyết]}",
                   }.get(r.gian_giao, "")
            # Ghi chú nguồn CHẢY TIẾP ngay sau tên dạng (không \newline): mỗi dòng trích
            # dẫn chiếm trọn một dòng thì bảng 12-13 dạng bị tràn trang, dòng TỔNG rơi
            # sang trang sau — hỏng chủ đích "một buổi gọn một trang" của bảng này.
            if r.source_refs:
                src = ", ".join(x.replace("_", r"\_") for x in r.source_refs)
                note = rf"~{{\scriptsize\color{{muted}}[Nguồn: {src}]}}"
            elif (r.loai or "").strip() == "NB lẻ LT":
                note = r"~{\scriptsize\color{muted}[tự soạn theo lý thuyết]}"
            else:
                note = r"~{\scriptsize\color{brand}\bfseries [CHƯA TRÍCH DẪN NGUỒN]}"
            r = r.model_copy(update={"dang": rf"{{\sffamily\bfseries\color{{{tint}}}"
                                             rf"{band}{idx}.}}~{r.dang}{tag}{note}"})
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
    # Cân buổi là DÒNG CUỐI CỦA CHÍNH BẢNG, không phải đoạn văn rời phía dưới: để rời
    # thì gặp bảng vừa kín trang, mỗi dòng này bị đẩy sang một trang trắng riêng
    # (chương IV lớp 9 từng thừa 2 trang chỉ vì vậy).
    L.append(rf"\multicolumn{{{ncol}}}{{|l|}}"
             rf"{{{_canbuoi(grand, info, getattr(phieu, 'so_ca', 1))}}} \\ \hline")
    L.append(r"\end{longtable}\endgroup")
    return "\n".join(L), grand


def _canbuoi(grand, info, so_ca: int = 1) -> str:
    """Dòng cân buổi: GV giảng (lý thuyết+ví dụ) + luyện tập + BTVN.

    Phiếu trải nhiều ca (`SpecPhieu.so_ca`) thì quỹ in ra phải nhân lên bấy nhiêu,
    nếu không Thầy đọc thấy "Luyện tập 252′ (quỹ 120′)" mà tưởng phiếu vống gấp đôi.
    """
    ca = max(1, so_ca or 1)
    gv = grand[1] + grand[3]
    onclass, btvn = grand[5], grand[7]
    b = info.get("budgets", {})
    nhan = f" cho {ca} ca" if ca > 1 else ""
    return (rf"{{\small\textbf{{\color{{brand}}Cân buổi{nhan}:}} "
            rf"Ví dụ/lý thuyết (GV giảng) $\approx${round(gv)}′ (quỹ {round(b.get('vidu',0)*ca)}′) "
            rf"$+$ Luyện tập {round(onclass)}′ (quỹ {round(b.get('onclass',0)*ca)}′) tại lớp. "
            rf"BTVN $\approx${round(btvn)}′ (quỹ {round(b.get('btvn',0)*ca)}′) ở nhà.}}")


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
            # Mỗi phiếu MỘT DÒNG (xem _cell_lines) — 6 phiếu nối bằng ';' đọc không ra.
            ("Tên bài", _cell_lines(
                [f"\\textbf{{{spec.title}}}{badge}."]
                + [f"\\textbf{{Phiếu {p.code}}} — {p.title}" for p in spec.phieu],
                plain_first=True)),
            ("Thời gian", f"\\textbf{{1 ca $=$ {info.get('session_minutes')} phút}} "
                          f"(trừ giải lao {info.get('break_minutes')}′): GV giảng "
                          f"$\\approx${round(info.get('budgets',{}).get('vidu',0))}′ $+$ Luyện tập "
                          f"{round(info.get('budgets',{}).get('onclass',0))}′. "
                          f"BTVN $\\approx${round(info.get('budgets',{}).get('btvn',0))}′ ở nhà."),
        ] + ([("Thời lượng", _cell_lines(spec.thoiluong))] if spec.thoiluong else [])),
    ]
    # KIẾN THỨC NỀN đứng TRƯỚC mục tiêu: đây là thứ HS phải có sẵn mới học nổi chương.
    if spec.kien_thuc_nen:
        parts += [r"\tmsec{KIẾN THỨC NỀN (lớp dưới dùng lại)}", _itemize(spec.kien_thuc_nen)]
    parts += [
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
        table, _ = _phieu_table(p, rates, info)
        parts += [r"\newpage", rf"\tmsec{{NỘI DUNG PHIẾU — PHIẾU {p.code}: {p.title}}}", table]
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
