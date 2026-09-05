#!/usr/bin/env python3
"""ÔN TẬP THEO PHẦN — gom đề bài từ CÁC ĐỀ THI THỬ VÀO 10 Hà Nội, mỗi phần một tệp.

VÌ SAO (Thầy chốt 04/09/2026): *"xây dựng các file ôn tập các phần chỉ toàn các đề thi
thử thôi cho dễ"*. Đề thi thử bám khuôn đề Sở nên gom theo phần là ra ngay bộ luyện cho
từng mạch kiến thức.

Cấu trúc đề Vào 10 Hà Nội (5 bài, xem [[ma-tran-vao-10-ha-noi]]):
  I   (2,0đ) Rút gọn biểu thức chứa căn + câu hỏi phụ
  II  (2,0đ) Giải bài toán bằng cách lập phương trình / hệ · hình khối
  III (2,0đ) Hệ phương trình · parabol và đường thẳng · phương trình bậc hai
  IV  (3,0đ) Hình học đường tròn
  V   (0,5đ) Cực trị / bất đẳng thức

CẮT ẢNH VÙNG ĐỀ TỪ PDF GỐC, không in lại bằng chữ. Lý do: `pdftotext` phá nát công thức
của các đề này (phân số, căn thức bị tãi thành "A = và B = + + với x > 0") vì chúng được
soạn bằng đối tượng công thức rồi dàn theo cột. Cắt ảnh giữ nguyên bản in — đúng lối
AGENTS §4.10 "không dựng chính xác được thì cắt ảnh đề gốc".

KHÔNG kèm đáp án: đáp án chưa được đối chiếu (AGENTS §2 cấm bịa đáp án). Thầy duyệt xong
mới dựng thành phiếu có lời giải.

Dùng:
    .venv/bin/python scripts/build_on_tap_thi_thu.py            # 5 PDF + 1 JSON
    .venv/bin/python scripts/build_on_tap_thi_thu.py --phan IV  # chỉ một phần
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import settings                                    # noqa: E402
from src.compiler.jinja_renderer import _env, load_tokens      # noqa: E402
from src.compiler.latex_builder import build_pdf               # noqa: E402

NGUON = ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "thi-thu-vao-10"
OUT_JSON = ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "on-tap-thi-thu.json"

PHAN = {
    "I":   ("Rút gọn biểu thức chứa căn", "2,0đ"),
    "II":  ("Giải bài toán bằng cách lập phương trình / hệ · hình khối", "2,0đ"),
    "III": ("Hệ phương trình · parabol và đường thẳng · phương trình bậc hai", "2,0đ"),
    "IV":  ("Hình học đường tròn", "3,0đ"),
    "V":   ("Cực trị · bất đẳng thức", "0,5đ"),
}
THU_TU = ["I", "II", "III", "IV", "V"]

_HET = re.compile(r"HƯỚNG\s*DẪN\s*CHẤM|ĐÁP\s*ÁN|BIỂU\s*ĐIỂM|MA\s*TRẬN|ĐẶC\s*TẢ|Xem\s*thêm", re.I)
_MOC = re.compile(r"(?:^|(?<=[.:;\)\]]\s)|(?<=\s{2}))(Bài|Câu)[ \t]*([0-9]{1,2}|[IVX]{1,5})"
                  r"[ \t]*[\.:\)\(]", re.M)

# Nhận PHẦN theo NỘI DUNG — dùng để đối chiếu với thứ tự, và để cứu đề đánh số lệch.
_DAU_HIEU = {
    "I":   re.compile(r"rút\s*gọn|biểu\s*thức\s*[AB]\b|với\s*x\s*>\s*0", re.I),
    "II":  re.compile(r"lập\s*phương\s*trình|lập\s*hệ|hình\s*(?:nón|trụ|cầu|chóp)|"
                      r"thể\s*tích|diện\s*tích\s*xung\s*quanh", re.I),
    "III": re.compile(r"hệ\s*phương\s*trình|parabol|\(\s*P\s*\)\s*:|đường\s*thẳng\s*\(\s*d",
                      re.I),
    "IV":  re.compile(r"đường\s*tròn|tiếp\s*tuyến|nội\s*tiếp|dây\s*cung", re.I),
    "V":   re.compile(r"giá\s*trị\s*(?:nhỏ|lớn)\s*nhất|GTNN|GTLN|chứng\s*minh\s*rằng.{0,40}≥",
                      re.I),
}
_ESC = {"\\": " ", "&": r"\&", "%": r"\%", "$": " ", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_PUA = re.compile(r"[-]")
_GLYPH = {"∆": "tam giác ", "−": "-", "⋅": ".", "≤": " <= ",
          "≥": " >= ", "≠": " != ", "√": "căn ", "°": " độ"}


def tex(s: str) -> str:
    s = str(s)
    for a, b in _GLYPH.items():
        s = s.replace(a, b)
    s = _PUA.sub("", s)
    return "".join(_ESC.get(c, c) for c in s)


def phan_de(t: str) -> str:
    m = _HET.search(t)
    return t[: m.start()] if m and m.start() > len(t) * 0.15 else t


_LINE = re.compile(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">'
                   r'(.*?)</line>', re.S)
_WORD = re.compile(r'<word[^>]*>(.*?)</word>', re.S)
_PAGE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">')
_NHAN = re.compile(r"^(Bài|Câu)\s*([0-9]{1,2}|[IVX]{1,5})\s*[\.:\)]?$")
DPI = 150
ANH = ROOT / "outputs" / "on-tap-thi-thu" / "anh"


# Dòng báo HẾT PHẦN ĐỀ — bài cuối phải cắt tại đây, không kéo xuống hết trang, kẻo
# lôi theo "ĐÁP ÁN VÀ THANG ĐIỂM" và bảng barem rỗng.
_HET_DE_DONG = re.compile(r"^-*\s*H[EẾ]T|ĐÁP\s*ÁN|HƯỚNG\s*DẪN\s*CHẤM|Giám\s*thị|"
                          r"Cán\s*bộ\s*coi\s*thi|Họ\s*(?:và\s*)?tên\s*thí\s*sinh|"
                          r"Học\s*sinh\s*không\s*được", re.I)


def _moc_theo_toa_do(pdf: Path) -> tuple[list[tuple[int, float, str]], list[float]]:
    """Vị trí các mốc bài trong PDF: [(trang, y, nhãn)] + chiều cao mỗi trang (điểm).

    Đọc `pdftotext -bbox-layout` để lấy toạ độ THẬT của dòng "Bài N" — nhờ đó cắt được
    đúng dải ảnh của từng bài. TÁCH TRANG TRƯỚC rồi mới dò dòng: gộp hai mẫu vào một
    regex thì nhánh `<line>…(.*?)…</line>` nuốt qua cả thẻ `<page>` kế tiếp, làm số
    trang đếm ra 0.
    """
    x = subprocess.run(["pdftotext", "-bbox-layout", str(pdf), "-"],
                       capture_output=True).stdout.decode("utf-8", "ignore")
    cao: list[float] = []
    moc: list[tuple[int, float, str]] = []
    het: list[tuple[int, float]] = []
    khuc = re.split(r'<page width="([\d.]+)" height="([\d.]+)">', x)
    # khuc = [đầu, w1, h1, thân1, w2, h2, thân2, …]
    for k in range(1, len(khuc), 3):
        cao.append(float(khuc[k + 1]))
        trang = len(cao)
        for m in re.finditer(r'<line[^>]*yMin="([\d.]+)"[^>]*>(.*?)</line>',
                             khuc[k + 2], re.S):
            y = float(m.group(1))
            tu = [re.sub(r"<[^>]+>", "", w).strip() for w in _WORD.findall(m.group(2))]
            tu = [t for t in tu if t]
            if len(tu) < 2 or tu[0] not in ("Bài", "Câu"):
                continue
            so = tu[1].rstrip(".:)")
            if re.fullmatch(r"[0-9]{1,2}|[IVX]{1,5}", so):
                moc.append((trang, y, f"{tu[0]} {so}"))
        for m in re.finditer(r'<line[^>]*yMin="([\d.]+)"[^>]*>(.*?)</line>',
                             khuc[k + 2], re.S):
            tu = " ".join(re.sub(r"<[^>]+>", "", w).strip()
                          for w in _WORD.findall(m.group(2))).strip()
            if tu and _HET_DE_DONG.match(tu):
                het.append((trang, float(m.group(1))))
    return moc, cao, het


def cat_anh(pdf: Path, i_moc: int, moc: list, cao: list[float],
            het: list[tuple[int, float]] | None = None) -> list[Path]:
    """Cắt dải ảnh của bài thứ `i_moc` — một tệp PNG cho mỗi trang mà bài đó trải qua."""
    trang, y0, nhan = moc[i_moc]
    if i_moc + 1 < len(moc):
        t1, y1, _ = moc[i_moc + 1]
    else:
        t1, y1 = len(cao), cao[-1] if cao else 792.0
    # Cắt sớm tại dòng "Hết"/"ĐÁP ÁN" đầu tiên nằm SAU mốc này.
    for tr, y in (het or []):
        if (tr, y) > (trang, y0) and (tr, y) < (t1, y1):
            t1, y1 = tr, y
            break
    ANH.mkdir(parents=True, exist_ok=True)
    ra = []
    for tr in range(trang, min(t1, len(cao)) + 1):
        dau = y0 if tr == trang else 0.0
        cuoi = y1 if tr == t1 else cao[tr - 1]
        if cuoi - dau < 12:                      # dải quá mỏng, không có nội dung
            continue
        ten = ANH / f"{pdf.stem[:60]}-{i_moc:02d}-{tr}.png"
        r = DPI / 72.0
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-f", str(tr), "-l", str(tr),
                        "-x", "0", "-y", str(int(dau * r)),
                        "-W", "9999", "-H", str(int((cuoi - dau) * r)),
                        "-singlefile", str(pdf), str(ten.with_suffix(""))],
                       capture_output=True)
        if ten.exists() and ten.stat().st_size > 2000:
            ra.append(ten)
    return ra


def tach_bai(pdf: Path) -> list[tuple[str, str]]:
    """[(nhãn bài, nguyên văn)] của phần ĐỀ. [] nếu PDF không có lớp text."""
    t = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                       capture_output=True).stdout.decode("utf-8", "ignore")
    if len(t.replace(" ", "")) < 400:
        return []
    de = phan_de(t)
    ms = list(_MOC.finditer(de))
    ra = []
    for i, m in enumerate(ms):
        khoi = de[m.start(): ms[i + 1].start() if i + 1 < len(ms) else len(de)]
        ra.append((f"{m.group(1)} {m.group(2)}", khoi.strip()))
    return ra


def gan_phan(bais: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(phần, nhãn, nguyên văn). Đề đúng 5 bài thì gán theo THỨ TỰ (khuôn đề Sở);
    còn lại gán theo DẤU HIỆU nội dung, không khớp thì bỏ (không đoán bừa)."""
    ra = []
    if len(bais) == 5:
        for ph, (nhan, van) in zip(THU_TU, bais):
            ra.append((ph, nhan, van))
        return ra
    for nhan, van in bais:
        hit = [p for p in THU_TU if _DAU_HIEU[p].search(van)]
        if len(hit) == 1:
            ra.append((hit[0], nhan, van))
    return ra


def _van_ban_dai(pdf: Path, moc, cao, k: int) -> str:
    """Nguyên văn (thô) của bài thứ k — chỉ dùng để GÁN PHẦN, không in ra."""
    t = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                       capture_output=True).stdout.decode("utf-8", "ignore")
    de = phan_de(t)
    ms = list(_MOC.finditer(de))
    if k < len(ms):
        return de[ms[k].start(): ms[k + 1].start() if k + 1 < len(ms) else len(de)]
    return ""


def gom() -> dict[str, list[dict]]:
    """Gom theo phần, LẤY MỐC TỪ BBOX làm nguồn duy nhất.

    Bản trước ghép chéo hai nguồn mốc (regex trên text phẳng ↔ toạ độ bbox) rồi khớp
    theo nhãn — lệch nhau là rụng gần hết bài. Nay chỉ dùng bbox: nó vừa cho nhãn vừa
    cho toạ độ để cắt ảnh."""
    kho: dict[str, list[dict]] = {p: [] for p in THU_TU}
    bo_qua: list[str] = []
    for pdf in sorted(NGUON.glob("*.pdf")):
        moc, cao, het = _moc_theo_toa_do(pdf)
        # Chỉ giữ LƯỢT ĐẦU của chuỗi mốc (phần đề); lượt sau là hướng dẫn chấm.
        dau: list[int] = []
        for k, (_, _, nhan) in enumerate(moc):
            if dau and nhan == moc[dau[0]][2]:
                break                      # gặp lại nhãn đầu ⇒ đã sang phần đáp án
            dau.append(k)
        if len(dau) < 4:
            bo_qua.append(pdf.stem)
            continue
        van = [_van_ban_dai(pdf, moc, cao, k) for k in range(len(dau))]
        for k in dau:
            # Đề Vào 10 có đúng 5 bài theo khuôn Sở ⇒ gán theo THỨ TỰ; đề lệch khuôn thì
            # gán theo DẤU HIỆU nội dung, không khớp rõ thì bỏ (không đoán bừa).
            if len(dau) == 5:
                ph = THU_TU[k]
            else:
                hit = [q for q in THU_TU if _DAU_HIEU[q].search(van[k] if k < len(van) else "")]
                if len(hit) != 1:
                    continue
                ph = hit[0]
            anh = cat_anh(pdf, k, moc, cao, het)
            if not anh:
                continue
            kho[ph].append({"nguon": pdf.stem, "nhan": moc[k][2],
                            "anh": [str(a) for a in anh]})
    if bo_qua:
        print(f"  ⚠ {len(bo_qua)} đề KHÔNG tách được (PDF ảnh, không có lớp text ở trang đề):")
        for b in bo_qua:
            print(f"      {b}")
    return kho


def _ten_truong(slug: str) -> str:
    m = re.search(r"(?:truong|phong-gddt|cum)-(.+?)-ha-noi$", slug)
    ten = m.group(1).replace("-", " ").title() if m else slug
    lan = re.search(r"lan-(\d)", slug)
    nam = re.search(r"nam-(\d{4})-(\d{4})", slug)
    p = [ten]
    if lan:
        p.append(f"lần {lan.group(1)}")
    if nam:
        p.append(f"{nam.group(1)}–{nam.group(2)}")
    return " · ".join(p)


def render(ph: str, muc: list[dict]) -> Path:
    ten, diem = PHAN[ph]
    body = [
        f"\\tmtitle{{ÔN TẬP VÀO 10 — PHẦN {ph}}}\\par",
        f"\\tmsub{{{tex(ten)} \;·\; {tex(diem)} \;·\; {len(muc)} đề "
        f"thi thử Hà Nội}}\\par\\vspace{{4pt}}",
        "{\\setlength{\\fboxsep}{5pt}\\colorbox{stage1!12}{\\parbox{\\linewidth}{"
        "\\bfseries CHỈ IN ĐỀ BÀI — chưa kèm đáp án. Nguồn ghi ngay dưới mỗi bài để "
        "truy ngược. Thầy duyệt xong con mới dựng thành phiếu có lời giải.}}}\\par",
    ]
    for i, m in enumerate(muc, 1):
        anh = "\n".join(
            f"\\noindent\\includegraphics[width=\\linewidth]{{{a}}}\\par" for a in m["anh"])
        body.append(f"\\tmsec{{Bài {i} \;—\; {tex(_ten_truong(m['nguon']))}}}\n" + anh)
    src = _env().get_template("base_on_tap.tex.j2").render(
        body="\n\n".join(body), **load_tokens())
    slug = f"on-tap-vao-10-phan-{ph.lower()}"
    return build_pdf(src, slug="on-tap-thi-thu", filename=slug,
                     out_root=settings.OUTPUTS_DIR, force=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phan", help="chỉ dựng một phần (I…V)")
    a = ap.parse_args()
    kho = gom()
    OUT_JSON.write_text(json.dumps(
        {"_doc": "Đề bài gom từ đề thi thử vào 10 Hà Nội, nhóm theo phần của đề Sở. "
                 "Sinh bởi scripts/build_on_tap_thi_thu.py — CẮT ẢNH từ PDF gốc "
                 "(pdftotext phá nát công thức), CHƯA có đáp án. `de_text` chỉ để tra cứu.",
         "phan": {p: kho[p] for p in THU_TU}}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    for ph in THU_TU:
        if a.phan and ph != a.phan:
            continue
        if not kho[ph]:
            print(f"  phần {ph}: (rỗng)")
            continue
        print(f"✓ phần {ph}: {len(kho[ph])} bài →", render(ph, kho[ph]).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
