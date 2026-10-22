"""Mảnh OOXML viết tay mà python-docx không có API (trường PAGE, viền đoạn, nền ô,
ảnh neo sau chữ, watermark VML…). Dùng chung cho khuôn (`scripts/make_docx_template`)
và bộ lắp tài liệu (`docx_renderer`).

Luật schema đã học (python-docx analysis + tex2gdoc):
  • Thứ tự con của <w:pPr> là BẮT BUỘC: pStyle, keepNext, keepLines, pageBreakBefore,
    …, pBdr, shd, tabs, …, spacing, ind, …, jc, …, outlineLvl. Chèn sai chỗ ⇒ Word
    báo file hỏng. Vì vậy mọi hàm ở đây chèn ĐÚNG VỊ TRÍ qua `_insert_ordered`.
  • Tab đo bằng twips (1/20 pt), viền đo bằng 1/8 pt, ảnh đo bằng EMU (914400/in).
"""
from __future__ import annotations

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

EMU_PER_IN = 914400
EMU_PER_PT = 12700
TWIP_PER_PT = 20

# Thứ tự phần tử con của w:pPr theo ECMA-376 (CT_PPrBase + pPrChange…).
_PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
    "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
    "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
    "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
    "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
    "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange",
]
# Thứ tự con của w:tcPr.
_TCPR_ORDER = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd",
               "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"]


def _insert_ordered(parent, child, order: list[str]):
    tag = child.tag.split("}")[1]
    old = parent.find(qn(f"w:{tag}"))
    if old is not None:
        parent.replace(old, child)
        return child
    idx = order.index(tag)
    for i, el in enumerate(parent):
        t = el.tag.split("}")[1]
        if t in order and order.index(t) > idx:
            parent.insert(i, child)
            return child
    parent.append(child)
    return child


# Thứ tự con của w:tblPr.
_TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
                "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
                "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription"]
# Thứ tự con của w:rPr.
_RPR_ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
              "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
              "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz", "szCs",
              "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em",
              "lang", "eastAsianLayout", "specVanish", "oMath"]


def tblpr_set(tbl, child):
    return _insert_ordered(tbl.tblPr, child, _TBLPR_ORDER)


def rpr_set(r, child):
    return _insert_ordered(r.get_or_add_rPr(), child, _RPR_ORDER)


def ppr_set(p_or_style_el, child):
    """Đặt một thuộc tính đoạn (child là phần tử w:xxx) đúng thứ tự schema."""
    ppr = p_or_style_el.get_or_add_pPr()
    return _insert_ordered(ppr, child, _PPR_ORDER)


def tcpr_set(tc, child):
    return _insert_ordered(tc.get_or_add_tcPr(), child, _TCPR_ORDER)


# ───────────────────────── viền / nền ─────────────────────────
def border_xml(tag: str, sides: dict[str, tuple[float, str, float]]) -> str:
    """sides = {"top": (bề dày pt, màu hex, khoảng cách pt)}. tag = pBdr | tcBorders | tblBorders."""
    inner = "".join(
        f'<w:{side} w:val="single" w:sz="{round(sz * 8)}" w:space="{round(sp)}" w:color="{col}"/>'
        for side, (sz, col, sp) in sides.items())
    return f"<w:{tag} {nsdecls('w')}>{inner}</w:{tag}>"


def nil_borders_xml(tag: str, sides=("top", "left", "bottom", "right", "insideH", "insideV")) -> str:
    inner = "".join(f'<w:{s} w:val="nil"/>' for s in sides)
    return f"<w:{tag} {nsdecls('w')}>{inner}</w:{tag}>"


def shd(fill_hex: str):
    return parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{fill_hex}"/>')


def mix(hex_color: str, pct: float, base: str = "FFFFFF") -> str:
    """Màu `hex_color!pct` kiểu xcolor (pha với trắng) — để nền hộp khớp bản PDF."""
    a = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(base[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x * pct / 100 + y * (1 - pct / 100)):02X}" for x, y in zip(a, b))


# ───────────────────────── trường (field) ─────────────────────────
def field_runs(instr: str, rpr_xml: str = "", placeholder: str = "1") -> list:
    """Các run của một trường đơn giản (PAGE, NUMPAGES…): begin / instrText / separate / kết quả / end."""
    rpr = f"<w:rPr>{rpr_xml}</w:rPr>" if rpr_xml else ""
    ns = nsdecls("w")
    return [
        parse_xml(f'<w:r {ns}>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'),
        parse_xml(f'<w:r {ns}>{rpr}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'),
        parse_xml(f'<w:r {ns}>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'),
        parse_xml(f'<w:r {ns}>{rpr}<w:t>{placeholder}</w:t></w:r>'),
        parse_xml(f'<w:r {ns}>{rpr}<w:fldChar w:fldCharType="end"/></w:r>'),
    ]


# ───────────────────────── watermark kiểu Word ─────────────────────────
def watermark_vml(rid: str, width_pt: float, height_pt: float, rotation_deg: float,
                  shape_no: int, washout: bool = False) -> str:
    """Watermark ẢNH đúng như Word tự sinh khi bấm Design → Watermark → Picture
    (mổ từ file 'chuẩn hình thức (đã có logo)' của trung tâm): VML <v:shape> id
    `WordPictureWatermark…` trong header, căn giữa, nằm sau chữ (z-index âm).
    Nhờ đúng id/kiểu này, Word NHẬN RA đây là watermark ⇒ Thầy thay/xoá được ngay
    trong menu Design → Watermark. `rotation` theo chiều kim đồng hồ (VML)."""
    gain = ' gain="19661f" blacklevel="22938f"' if washout else ""
    return (
        f'<w:r {nsdecls("w")} xmlns:v="urn:schemas-microsoft-com:vml" '
        f'xmlns:o="urn:schemas-microsoft-com:office:office" '
        f'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<w:rPr><w:noProof/></w:rPr><w:pict>'
        f'<v:shapetype id="_x0000_t75" coordsize="21600,21600" o:spt="75" o:preferrelative="t" '
        f'path="m@4@5l@4@11@9@11@9@5xe" filled="f" stroked="f"><v:stroke joinstyle="miter"/>'
        f'<v:formulas><v:f eqn="if lineDrawn pixelLineWidth 0"/><v:f eqn="sum @0 1 0"/>'
        f'<v:f eqn="sum 0 0 @1"/><v:f eqn="prod @2 1 2"/><v:f eqn="prod @3 21600 pixelWidth"/>'
        f'<v:f eqn="prod @3 21600 pixelHeight"/><v:f eqn="sum @0 0 1"/><v:f eqn="prod @6 1 2"/>'
        f'<v:f eqn="prod @7 21600 pixelWidth"/><v:f eqn="sum @8 21600 0"/>'
        f'<v:f eqn="prod @7 21600 pixelHeight"/><v:f eqn="sum @10 21600 0"/></v:formulas>'
        f'<v:path o:extrusionok="f" gradientshapeok="t" o:connecttype="rect"/>'
        f'<o:lock v:ext="edit" aspectratio="t"/></v:shapetype>'
        f'<v:shape id="WordPictureWatermark{shape_no}" o:spid="_x0000_s{2048 + shape_no}" '
        f'type="#_x0000_t75" style="position:absolute;margin-left:0;margin-top:0;'
        f'width:{width_pt:.2f}pt;height:{height_pt:.2f}pt;rotation:{rotation_deg:g};'
        f'z-index:-251657216;mso-position-horizontal:center;mso-position-horizontal-relative:page;'
        f'mso-position-vertical:center;mso-position-vertical-relative:page" o:allowincell="f">'
        f'<v:imagedata r:id="{rid}" o:title="watermark"{gain}/>'
        f'<w10:wrap anchorx="page" anchory="page"/></v:shape></w:pict></w:r>'
    )


# ───────────────────────── ảnh neo (floating) ─────────────────────────
def anchor_picture_xml(rid: str, cx: int, cy: int, x: int, y: int, pic_id: int,
                       name: str, behind: bool = True, rel: str = "page") -> str:
    """Ảnh NỔI neo theo trang (python-docx chỉ có ảnh inline). Dùng cho khung viền
    trang + 4 góc chữ L: một PNG trong suốt khổ A4 đặt sau chữ trong header."""
    return (
        f'<w:r {nsdecls("w")}><w:rPr><w:noProof/></w:rPr><w:drawing>'
        f'<wp:anchor xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        f'distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="{1 if behind else 251659264}" '
        f'behindDoc="{1 if behind else 0}" locked="1" layoutInCell="1" allowOverlap="1">'
        f'<wp:simplePos x="0" y="0"/>'
        f'<wp:positionH relativeFrom="{rel}"><wp:posOffset>{x}</wp:posOffset></wp:positionH>'
        f'<wp:positionV relativeFrom="{rel}"><wp:posOffset>{y}</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
        f'<wp:docPr id="{pic_id}" name="{name}"/><wp:cNvGraphicFramePr>'
        f'<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        f'</wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{pic_id}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/>'
        f'<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        f'</a:graphicData></a:graphic></wp:anchor></w:drawing></w:r>'
    )
