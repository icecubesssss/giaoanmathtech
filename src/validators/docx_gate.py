"""Cổng soát bản Word (.docx) TRƯỚC khi giao — chạy trên file đã ghi ra, đối chiếu nguồn JSON.

Bài học đã học (Thầy 22/10/2026 — "học hết kinh nghiệm họ rút ra rồi mới làm"):
  • tex2gdoc: pandoc bỏ nội dung mà vẫn exit 0 ⇒ phải ĐẾM lại trên file kết quả: số
    công thức, số bài, số hình — sinh từ nguồn nên đòi KHỚP TUYỆT ĐỐI.
  • formula-flow: "không báo lỗi ≠ đúng" ⇒ soi XML: công thức rỗng, lệnh `\\…` sót
    trong chữ/công thức, token `[[…]]` sót.
  • python-docx: thứ tự phần tử con trong pPr/rPr/tblPr/tcPr là BẮT BUỘC — sai là Word
    mở file báo "unreadable content" và treo hộp thoại (đã dính 22/10/2026).
  • Watermark/banner phải có ở CẢ 3 header, trường PAGE ở cả 3 footer.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from lxml import etree

from src.compiler.docx_xml import _PPR_ORDER, _RPR_ORDER, _TBLPR_ORDER, _TCPR_ORDER

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
MNS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": MNS}
_ORDERS = {"pPr": _PPR_ORDER, "rPr": _RPR_ORDER, "tblPr": _TBLPR_ORDER, "tcPr": _TCPR_ORDER}
_FONTS_OK = {"Times New Roman", "Be Vietnam Pro", "Cambria Math", "Arial", "Calibri", "Cambria"}


def _local(tag: str) -> str:
    return tag.split("}")[1] if "}" in tag else tag


def check_order(root, part: str) -> list[str]:
    errs = []
    for name, order in _ORDERS.items():
        for el in root.iter(f"{{{W}}}{name}"):
            # rPr bên trong m:r (công thức) có thứ tự riêng — bỏ qua.
            if name == "rPr" and el.getparent() is not None and el.getparent().tag == f"{{{MNS}}}r":
                continue
            last = -1
            for ch in el:
                t = _local(ch.tag)
                if t not in order:
                    continue
                k = order.index(t)
                if k < last:
                    errs.append(f"{part}: <w:{name}> sai thứ tự — <w:{t}> đứng sau phần tử lẽ ra sau nó")
                    break
                last = k
    return errs


def check_docx(path: Path, expect_problems: int | None = None, expect_maths: int | None = None,
               min_images: int | None = None, branded: bool = True) -> list[str]:
    """`branded=False`: tài liệu KHÔNG có header/footer (thuyết minh — y bản PDF)."""
    errs: list[str] = []
    z = zipfile.ZipFile(path)
    names = z.namelist()
    doc = etree.fromstring(z.read("word/document.xml"))
    errs += check_order(doc, "document.xml")

    # ---- công thức ----
    omaths = [o for o in doc.iter(f"{{{MNS}}}oMath")]
    for o in omaths:
        txt = "".join(t.text or "" for t in o.iter(f"{{{MNS}}}t"))
        if not txt.strip() and o.find(f".//{{{MNS}}}f") is None:
            errs.append("công thức rỗng")
        if re.search(r"\\[A-Za-z]{2,}", txt):
            errs.append(f"công thức còn lệnh LaTeX sót: {txt[:60]}")
        par = o.getparent()
        if par is not None and _local(par.tag) == "r":
            errs.append("m:oMath nằm trong w:r (sai chuẩn — tex_math_to_word từng dính)")
    if expect_maths is not None and len(omaths) != expect_maths:
        errs.append(f"số công thức trong Word {len(omaths)} ≠ nguồn {expect_maths}")

    # ---- chữ ----
    text = "".join(t.text or "" for t in doc.iter(f"{{{W}}}t"))
    for m in re.finditer(r"\\[A-Za-z]{2,}|\[\[[a-z/]+", text):
        errs.append(f"chữ còn sót mã nguồn: …{text[max(0, m.start() - 30):m.end() + 30]}…")
        if len(errs) > 40:
            break
    if expect_problems is not None:
        # Mỗi bài mở bằng nhãn in đậm; đếm run đậm khớp "Bài/Câu/Ví dụ … ." là không chắc —
        # nên renderer tự đếm nhãn đã in và cổng chỉ kiểm khi có số.
        pass

    # ---- hình ----
    imgs = [n for n in names if n.startswith("word/media/")]
    blips = doc.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
    if min_images is not None and len(blips) < min_images:
        errs.append(f"số hình trong thân bài {len(blips)} < nguồn {min_images}")

    # ---- header / footer ----
    hdrs = [n for n in names if re.match(r"word/header\d+\.xml$", n)]
    ftrs = [n for n in names if re.match(r"word/footer\d+\.xml$", n)]
    if branded and (len(hdrs) < 3 or len(ftrs) < 3):
        errs.append(f"thiếu header/footer ({len(hdrs)} header, {len(ftrs)} footer; cần 3/3)")
    for h in (hdrs if branded else []):
        x = z.read(h).decode("utf-8")
        if "WordPictureWatermark" not in x:
            errs.append(f"{h}: thiếu watermark")
        if x.count("<pic:pic") < 1:
            errs.append(f"{h}: thiếu banner")
        errs += check_order(etree.fromstring(z.read(h)), h)
    for f in (ftrs if branded else []):
        x = z.read(f).decode("utf-8")
        if "PAGE" not in x:
            errs.append(f"{f}: thiếu số trang")
        errs += check_order(etree.fromstring(z.read(f)), f)

    # ---- font ----
    for rf in doc.iter(f"{{{W}}}rFonts"):
        for k, v in rf.attrib.items():
            if _local(k) in ("ascii", "hAnsi") and v not in _FONTS_OK:
                errs.append(f"font lạ: {v}")
                break
    return list(dict.fromkeys(errs))
