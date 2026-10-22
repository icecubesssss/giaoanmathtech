"""PHIẾU THUYẾT MINH (ThuyetMinhSpec) → Word (.docx) A4 ngang — bản sao của
`thuyetminh_renderer.render_thuyetminh` (PDF), cùng thứ tự mục, cùng số liệu.

Số câu / phút / tổng / cân buổi tính bằng CHÍNH các hàm của bản PDF (`row_minutes`,
`session_info`, `he_so_con_lai`, `rates_for_spec`) ⇒ hai bản không thể lệch số.
Bảng nội dung phiếu dựng bằng ô gộp thật (gridSpan/vMerge) thay \\multicolumn/\\multirow.
"""
from __future__ import annotations

from docx import Document

from src.compiler.docx_renderer import Emitter, Report, collect, ensure_template
from src.compiler.docx_text import Cell, Ctx, Fmt, P, PageBreak, Reader, T, Tbl, color_hex, set_palette
from src.compiler.jinja_renderer import load_tokens
from src.compiler.omml import convert_many, is_only_space
from src.compiler.thuyetminh_renderer import _BAND_ORDER, _canbuoi, _has_ve_hinh, _n, _t
from src.schema.thuyetminh_spec import rates_for_spec, row_minutes, session_info
from src.schema.tier_spec import draw_minutes, load_tier_spec

from config import settings

TEMPLATE = settings.TEMPLATES_DIR / "docx" / "mathtech-ngang.docx"
TEXT_W_IN = (29.7 - 2.6) / 2.54                     # 27,1cm
_BAND_HEAD = {"NB": ("NHẬN BIẾT — NB", "stage1", 1), "TH": ("THÔNG HIỂU — TH", "stage2", 2),
              "VD": ("VẬN DỤNG — VD", "stage3", 3), "VDC": ("VẬN DỤNG CAO — VDC", "stage4", 4)}


class _TM:
    def __init__(self, spec, tokens):
        self.S = spec
        self.C = tokens["colors"]
        self.ctx = Ctx(where=f"thuyết minh {spec.slug}")
        self.rd = Reader(self.ctx)
        self.out: list = []

    def inl(self, s: str, fmt: Fmt = Fmt()) -> list:
        return self.rd.inlines(s or "", fmt)

    def sec(self, title: str):
        """\\tmsec — nhãn nền brand chữ trắng (colorbox, KHÔNG kéo hết bề ngang)."""
        f = Fmt(bold=True, sans=True, size=10, color="FFFFFF", shade=self.C["brand"])
        self.out.append(P([T("\u00A0", f)] + self.inl(title, f) + [T("\u00A0", f)],
                          align="left", keep_next=True, space_before=6, space_after=3))

    def lbl(self, s: str) -> P:
        return P(self.inl(s, Fmt(bold=True, sans=True, color=self.C["ink"])), align="left",
                 keep_next=True, space_after=1)

    def items(self, xs: list[str]) -> list:
        return [P([T("• ")] + self.inl(x), align="left", indent_pt=16, hanging_pt=10,
                  space_after=1) for x in xs]

    def lines(self, xs: list[str], plain_first: bool = False) -> list:
        """Ô bảng đầu: mỗi mục MỘT DÒNG (thuyetminh_renderer._cell_lines)."""
        return [P(([] if (plain_first and i == 0) else [T("• ")]) + self.inl(x),
                  align="left", tight=i < len(xs) - 1) for i, x in enumerate(xs)]

    def build(self) -> list:
        S, C = self.S, self.C
        rates, info = rates_for_spec(S), session_info(S)
        badge = f" (LỚP {S.tier})" if S.tier else ""
        tuan = f" • Tuần {S.tuan}" if S.tuan else ""
        khoi = "Lớp 9 (Ôn vào 10)" if S.grade == "lop-9" else S.grade.replace("lop-", "Lớp ")
        self.out.append(P([T("PHIẾU THUYẾT MINH", Fmt(bold=True, sans=True, size=19, color=C["brand"])),
                           T(" ")] + self.inl(f"{S.title} • {khoi}", Fmt(sans=True, color=C["muted"]))
                          + ([T(badge, Fmt(bold=True, sans=True, color=C["muted"]))] if badge else [])
                          + [T(tuan, Fmt(sans=True, color=C["muted"]))], align="left", space_after=4))
        b = info.get("budgets", {})
        thoigian = (f"\\textbf{{1 ca $=$ {info.get('session_minutes')} phút}} (trừ giải lao "
                    f"{info.get('break_minutes')}′): GV giảng $\\approx${round(b.get('vidu', 0))}′ $+$ "
                    f"Luyện tập {round(b.get('onclass', 0))}′. BTVN $\\approx${round(b.get('btvn', 0))}′ ở nhà.")
        lab = lambda s: Cell([P([T(s, Fmt(bold=True, sans=True, color=C["ink"]))], align="left")])
        rows = [[lab("Tên bài"), Cell(self.lines([f"\\textbf{{{S.title}}}{badge}."]
                                                 + [f"\\textbf{{Phiếu {p.code}}} — {p.title}" for p in S.phieu],
                                                 plain_first=True))],
                [lab("Thời gian"), Cell([P(self.inl(thoigian), align="left")])]]
        if S.thoiluong:
            rows.append([lab("Thời lượng"), Cell(self.lines(S.thoiluong))])
        self.out.append(Tbl(rows, widths=[3.82 / 27.1, 22.82 / 27.1], border_color=C["rule"], cell_pad_pt=3,
                            align="left", compact=True))
        if S.kien_thuc_nen:
            self.sec("KIẾN THỨC NỀN (lớp dưới dùng lại)")
            self.out += self.items(S.kien_thuc_nen)
        self.sec("MỤC TIÊU LÝ THUYẾT & CHUẨN ĐẦU RA")
        self.out += self.items(S.lythuyet)
        self.sec("BÀI TẬP")
        two = lambda l1, x1, l2, x2: Tbl([[Cell([self.lbl(l1)] + self.items(x1)),
                                           Cell([self.lbl(l2)] + self.items(x2))]],
                                         widths=[0.485, 0.485], borders=False, cell_pad_pt=0, align="left")
        self.out.append(two("Ví dụ GV làm mẫu:", S.vidu, "Dạng VẬN DỤNG trong đề:", S.dang_vd))
        self.out.append(two("Lỗi sai thường gặp:", S.loisai, "Kiến thức NHẬN BIẾT cần nhớ:", S.kienthuc_nb))
        for p in S.phieu:
            self.out.append(PageBreak())
            self.sec(f"NỘI DUNG PHIẾU — PHIẾU {p.code}: {p.title}")
            self.out.append(self.phieu_table(p, rates, info))
            qt = [r for r in p.rows if r.quy_trinh]
            if qt:
                self.sec(f"QUY TRÌNH GIẢI BÀI — in ngay tại từng bài VẬN DỤNG của phiếu {p.code}")
                for r in qt:
                    self.out.append(self.lbl(f"{r.band} — {r.dang}"))
                    self.out += self.items(r.quy_trinh)
            vqt = [r for r in p.rows if r.viet_quy_trinh]
            if vqt:
                self.out.append(self.lbl("Bài tự viết lại quy trình (ôn tập chương):"))
                self.out += self.items([r.dang for r in vqt])
        note = ("Quy ước đếm: “câu” $=$ ý nhỏ a),b)…; thời gian tự tính theo phút/câu của tier\\_spec.json "
                "(NB/TH/VD/VDC). duration\\_gate chỉ soi Luyện tập trên lớp $+$ BTVN.")
        if _has_ve_hinh(S):
            note += (f" Cột TG đã CỘNG {draw_minutes(load_tier_spec()):.0f}′ cho mỗi hình học sinh phải tự "
                     "vẽ (cột ve\\_hinh của dạng).")
        if any((r.loai or "").strip() for p in S.phieu for r in p.rows):
            note += (" \\textbf{Cột Loại} — câu \\emph{lẻ LT} hỏi thẳng công thức vừa học; câu \\emph{tách TH} "
                     "là bước đệm cắt ra từ chính bài Thông hiểu bên dưới; câu \\emph{ghép bài} là các ý a), b) "
                     "mở đầu của một bài lớn, học sinh làm liền mạch trong CÙNG một bài chứ không phải bài rời.")
        self.out.append(P(self.inl(note, Fmt(italic=True, size=9, color=C["muted"])), align="justify",
                          space_before=8))
        thieu = sum(1 for p in S.phieu for r in p.rows
                    if not (r.loai or "").strip() or (r.loai or "").strip().startswith("TODO"))
        if thieu:
            self.out.append(P([T(f"CHƯA KHAI LOẠI CÂU HỎI (§4b) cho {thieu} dòng — bảng còn thiếu cột Loại "
                                 "(NB lẻ LT / NB tách TH / NB ghép bài / TH lẻ LT / TH ghép bài / TH tách VD / VD lẻ).",
                                 Fmt(bold=True, sans=True, size=10, color=C["brand"]))], align="left"))
        return self.out

    def phieu_table(self, phieu, rates, info) -> Tbl:
        C = self.C
        has_loai = any((r.loai or "").strip() for r in phieu.rows)
        ncol = 10 if has_loai else 9
        small = Fmt(size=9.5)
        neu = C["neutral"]
        hc = lambda s, f=Fmt(bold=True, sans=True, size=9.5): Cell([P([T(s, f)], align="center")], shade=neu)
        h1 = [Cell([P([T("Dạng bài", Fmt(bold=True, sans=True, size=9.5))], align="left")], shade=neu, vspan=2)]
        if has_loai:
            h1.append(Cell([P([T("Loại", Fmt(bold=True, sans=True, size=8.5))], align="center")], shade=neu, vspan=2))
        for g in ("Lý thuyết", "Ví dụ", "Bài tập trên lớp", "BTVN"):
            c = hc(g)
            c.span = 2
            h1.append(c)
        sub_f = Fmt(sans=True, size=8.5)
        h2 = [hc(x, sub_f) for x in ("Số mục", "TG", "Số câu", "TG", "Số câu", "TG", "Số câu", "TG")]
        rows = [h1, h2]
        grand = [0.0] * 8
        lead = ncol - 8
        for band in _BAND_ORDER:
            brows = [r for r in phieu.rows if r.band == band]
            if not brows:
                continue
            label, tint, n_star = _BAND_HEAD[band]
            stars = "★" * n_star
            rows.append([Cell([P([T(f"{label} ({stars})", Fmt(bold=True, sans=True, size=9.5, color=C[tint]))],
                                 align="left")], span=ncol, shade=color_hex(f"{tint}!16"))])
            sub = [0.0] * 8
            for idx, r in enumerate(brows, 1):
                tag = {"ve-hinh": " [giàn giáo: vẽ hình]", "dien-khuyet": " [giàn giáo: điền khuyết]"}.get(r.gian_giao, "")
                if r.source_refs:
                    note, nf = f" [Nguồn: {', '.join(r.source_refs)}]", Fmt(size=8, color=C["muted"])
                elif r.viet_quy_trinh:
                    note, nf = " [HS tự viết quy trình — không bốc từ đề]", Fmt(size=8, color=C["muted"])
                elif (r.loai or "").strip() == "NB lẻ LT":
                    note, nf = " [tự soạn theo lý thuyết]", Fmt(size=8, color=C["muted"])
                else:
                    note, nf = " [CHƯA TRÍCH DẪN NGUỒN]", Fmt(size=8, bold=True, color=C["brand"])
                inl = ([T(f"{band}{idx}.", Fmt(bold=True, sans=True, size=9.5, color=C[tint])), T(" ")]
                       + self.inl(r.dang, small)
                       + ([T(tag, Fmt(size=8, color=C["stage2"]))] if tag else []) + self.inl(note, nf))
                mins = row_minutes(r, rates)
                lt_m = r.lythuyet * rates.get("vidu", {}).get(band, 0)
                vals = [(r.lythuyet, lt_m), (r.vidu, mins["vidu"]), (r.onclass, mins["onclass"]),
                        (r.btvn, mins["btvn"])]
                cells = [Cell([P(inl, align="left")])]
                if has_loai:
                    cells.append(Cell([P([T(r.loai or "", Fmt(size=8))], align="center")]))
                for i, (n, m) in enumerate(vals):
                    cells += [Cell([P([T(_n(n), small)], align="center")]),
                              Cell([P([T(_t(m), small)], align="center")])]
                    sub[2 * i] += n
                    sub[2 * i + 1] += m
                rows.append(cells)
            for i in range(8):
                grand[i] += sub[i]
            cg = [Cell([P([T("Cộng nhóm", Fmt(bold=True, italic=True, size=9.5))], align="right")], span=lead)]
            for i in range(4):
                f = Fmt(italic=True, size=9.5) if i < 2 else Fmt(bold=True, size=9.5)
                cg += [Cell([P([T(_n(int(sub[2 * i])), f)], align="center")]),
                       Cell([P([T(_t(sub[2 * i + 1]), f)], align="center")])]
            rows.append(cg)
        tot_bg = color_hex("brand!12")
        tg = [Cell([P([T("TỔNG", Fmt(bold=True, sans=True, size=9.5, color=C["brand"]))], align="right")],
                   span=lead, shade=tot_bg)]
        for i in range(4):
            tg += [Cell([P([T(_n(int(grand[2 * i])), Fmt(bold=True, size=9.5))], align="center")], shade=tot_bg),
                   Cell([P([T(_t(grand[2 * i + 1]), Fmt(bold=True, size=9.5))], align="center")], shade=tot_bg)]
        rows.append(tg)
        cb = _canbuoi(grand, info, getattr(phieu, "so_ca", 1), getattr(phieu, "kiem_tra_phut", 0))
        rows.append([Cell([P(self.inl(cb), align="left")], span=ncol)])
        dang_cm = 8.3 if has_loai else 10.4
        # p{w} của LaTeX là bề rộng CHỮ — mỗi cột còn 2×\tabcolsep (6pt) đệm ⇒ +0,42cm/cột.
        widths = [w + 0.42 for w in [dang_cm] + ([2.1] if has_loai else []) + [1.45] * 8]
        return Tbl(rows, widths=[w / 27.1 for w in widths], border_color=C["rule"], header_rows=2,
                   cell_pad_pt=1.5, align="left", compact=True)


def render_thuyetminh_docx(spec):
    """→ (Document, Report)."""
    tokens = load_tokens()
    set_palette(tokens["colors"])
    tm = _TM(spec, tokens)
    blocks = tm.build()
    report = Report()
    report.issues += [f"lệnh chưa có luật đổi sang Word — {u}" for u in tm.ctx.unknown]
    maths, _ = collect(blocks)
    maths = [m for m in maths if not is_only_space(m)]
    report.counts["maths"] = len(maths)
    doc = Document(str(ensure_template(TEMPLATE, ngang=True)))
    Emitter(doc, convert_many(maths), {}, report, tokens["colors"]).blocks(doc, blocks, TEXT_W_IN)
    cp = doc.core_properties
    cp.title, cp.author = f"Thuyết minh — {spec.title}", "MathTech"
    return doc, report
