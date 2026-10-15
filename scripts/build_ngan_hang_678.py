#!/usr/bin/env python3
"""NGÂN HÀNG CÂU lớp 6-7-8 (TẦNG 1 — máy dựng) từ kho đề Hà Nội đã tải.

Cùng khuôn `inputs/refs/de-thi/lop-9/exams/` (mỗi ĐỀ một file, mỗi Ý một bản ghi) nhưng ở mức
THÔ: chữ lấy từ lớp text PDF hoặc OCR nên MẤT số mũ / phân số / kí hiệu (pdftotext đọc
"88² + 24·88 + 12²" thành "882 + 24.88 + 122"). Vì vậy mỗi bản ghi mang:
  • `trang` — số trang PDF chứa câu, để TẦNG 2 cắt ảnh đọc bằng mắt rồi gõ LaTeX;
  • `can_doc_anh` — True khi chữ chắc chắn vỡ (OCR, kí tự rác, mũ dính liền);
  • `chuong`/`dang` — gắn theo từ khoá của `thong_ke_dang_de.py` (~87% đúng);
  • `band` (+ `_band_auto`) — luật vị trí: trắc nghiệm NB · câu cuối đề và ý cuối bài hình
    VDC (quy ước anh An) · lời văn VD · còn lại NB/TH theo động từ;
  • `barem_tho` — khối hướng dẫn chấm gốc của cả Bài (nếu PDF có HDC lớp text), CHƯA tách ý;
    trắc nghiệm thì `dap_an` lấy từ bảng đáp án.
`da_duyet: false` toàn bộ. Câu nào được bốc vào phiếu thì PHẢI qua tầng 2 (đọc ảnh, LaTeX,
kiểm đáp án) — tầng 1 chỉ để TÌM câu theo chương/dạng/mức độ.

Nguồn nhận: đề định kì (`hop_le_de_thi`) + đề tham khảo bộ KNTT gom tay (tên có "KNTT", không
phải Cánh Diều/đề cương/đáp án rời). Trùng byte hoặc trùng chữ ⇒ giữ một bản.

Dùng:
    .venv/bin/python scripts/build_ngan_hang_678.py            # cả 3 khối
    .venv/bin/python scripts/build_ngan_hang_678.py --lop 8
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thong_ke_dang_de as T                      # noqa: E402
from trich_cau_cuoi_de import hop_le_de_thi       # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DE = ROOT / "inputs" / "refs" / "de-thi"
TXT = ROOT / "storage" / "cache" / "de-txt-all"
VDC_MAT = DE / "vdc-phan-loai-khoi-678.json"
# Đề ĐẢO CHƯƠNG (trường dạy KNTT khác thứ tự) — Thầy tách khỏi thống kê theo kỳ 30/09–01/10.
# Câu trong đó vẫn đúng nội dung KNTT nên VẪN vào ngân hàng tra theo chương, gắn cờ `lech_kntt`
# và KHÔNG giới hạn chương theo kỳ. Đề ghi bộ sách khác (Cánh Diều) thì loại hẳn.
LECH = ROOT / "inputs" / "refs" / "de-thi-lech-kntt"
LY_DO = {e["file"]: e["ly_do"] for e in json.loads((LECH / "ly-do.json").read_text(encoding="utf-8"))["de"]} \
    if (LECH / "ly-do.json").exists() else {}
KY_DIR = {"giua-ki-1": "gk1", "cuoi-ki-1": "ck1", "giua-ki-2": "gk2", "cuoi-ki-2": "ck2"}
PHUT = {"NB": 1.5, "TH": 6.0, "VD": 12.0, "VDC": 18.0}     # config/tier_spec.json rates.onclass

_KNTT_THAM_KHAO = re.compile(r"\bKNTT\b", re.I)
_LOAI = re.compile(r"\bCD\b|cánh diều|canh-dieu|đề\s*cương|de-cuong|đáp\s*án|\bDA\b|dap-an|"
                   r"thu thập|full_", re.I)


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def nhan_file(p: Path) -> bool:
    if hop_le_de_thi(p):
        return True
    s = nfc(p.stem)
    return bool(_KNTT_THAM_KHAO.search(s) and not _LOAI.search(s))


def duong_txt(p: Path) -> Path:
    base = LECH if LECH in p.parents else DE
    return TXT / p.relative_to(base).with_suffix(".txt")


def tao_text(p: Path) -> str:
    """Như ocr_kho_de.job nhưng nhận cả đề ở de-thi-lech-kntt/ (cùng cây lop-N/<kỳ>/)."""
    import subprocess, tempfile, os
    os.environ["TESSDATA_PREFIX"] = str(ROOT / "storage" / "cache" / "tessdata")
    dest = duong_txt(p)
    dest.parent.mkdir(parents=True, exist_ok=True)
    t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    nguon = "text"
    if len(re.sub(r"\s", "", t)) < 1500:
        nguon, parts = "ocr", []
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["pdftoppm", "-r", "300", "-gray", "-png", "-l", "6", str(p), f"{td}/p"],
                           capture_output=True)
            for img in sorted(Path(td).glob("p-*.png")):
                parts.append(subprocess.run(["tesseract", str(img), "-", "-l", "vie", "--psm", "4"],
                                            capture_output=True, text=True).stdout)
        t = "\n\f".join(parts)
    dest.write_text(f"#NGUON:{nguon}\n" + t, encoding="utf-8")
    return str(p.name)


def lay_text(p: Path) -> tuple[str, str] | None:
    t = duong_txt(p)
    if not t.exists():
        tao_text(p)
    if not t.exists():
        return None
    raw = t.read_text(encoding="utf-8", errors="ignore")
    nguon = "ocr" if raw.startswith("#NGUON:ocr") else "text"
    return nguon, raw.split("\n", 1)[1] if "\n" in raw else ""


# ───────────────────────── tách câu / ý ─────────────────────────
_Y = re.compile(r"^\s{0,10}([a-e])\s*[\)\.]\s*(?=\S)", re.M)
_PHAN_SO = re.compile(r"^\s{0,6}([1-4])\s*[\.\)]\s+(?=[A-ZĐÀ-Ỹ])", re.M)
_TN_OPT = re.compile(r"(?:^|\s)([A-D])\s*[\.\)]\s*", re.M)
_HINH = re.compile(r"tam giác|tứ giác|lục giác|hình (thang|bình hành|chữ nhật|thoi|vuông|tròn|hộp|"
                   r"lập phương|lăng trụ|ch[óố]p)|đường tròn|\btia\b|\bgóc\b|đoạn thẳng|đường thẳng|"
                   r"vuông góc|song song|//|⊥|△|∆", re.I)
_LOI_VAN = re.compile(r"giải bài toán|bằng cách lập|người ta|một (cửa hàng|người|ô tô|xe|đội|"
                      r"công ty|bác|mảnh|khu)|bác \w+|bạn \w+ (mua|đi|có)|giá (bán|niêm yết)|"
                      r"đồng\b|km/h|\bkm\b|lãi|giảm giá|khuyến mãi", re.I)
_NB_DONG_TU = re.compile(r"^(?:\W{0,3})(tính|thực hiện|thu gọn|viết|liệt kê|đọc|kể tên|nêu|"
                         r"phân tích|khai triển|tìm bậc|cho biết|xác định|vẽ)", re.I)
_RAC = re.compile(r"[-�]|[\U0001d400-\U0001d7ff]|(?<=[a-z])\d(?=\s*[+\-–=)])")


def tach_y(text: str) -> list[tuple[str, str]]:
    """[(nhãn ý, đoạn)] — '' khi bài không có ý. Hỗ trợ bài chia phần 1., 2. rồi a), b)."""
    phan = list(_PHAN_SO.finditer(text))
    khoi = ([(m.group(1), text[m.start(): phan[i + 1].start() if i + 1 < len(phan) else len(text)])
             for i, m in enumerate(phan)] if len(phan) >= 2 else [("", text)])
    ra: list[tuple[str, str]] = []
    for so, k in khoi:
        ys = list(_Y.finditer(k))
        # ý phải tăng dần a, b, c… — chặn "a)" lạc trong đáp án trắc nghiệm hay trong câu chữ
        hop: list[re.Match] = []
        for m in ys:
            if ord(m.group(1)) - ord("a") == len(hop):
                hop.append(m)
        if len(hop) < 2:
            ra.append((so, k))
            continue
        for i, m in enumerate(hop):
            ra.append((f"{so}{m.group(1)}", k[m.start(): hop[i + 1].start() if i + 1 < len(hop) else len(k)]))
    return ra


def dong_dau(text: str, n: int = 600) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()[:n]


# ───────────────────────── đáp án ─────────────────────────
_MOC_HDC = re.compile(r"hướng\s*d[ẫa]n\s*ch[ấa]m|đáp\s*án\s*(và|&|-)?\s*(biểu|hướng)|"
                      r"^\s*(i\.?\s*)?đáp\s*án\b|biểu\s*điểm|lời\s*giải", re.I | re.M)
_BAI_HDC = re.compile(r"^\s{0,8}(?:câu|bài)\s*(\d{1,2}|[IVX]{1,4})\b", re.I | re.M)


def phan_hdc(raw: str, het_de: int) -> str:
    m = _MOC_HDC.search(raw, het_de)
    return raw[m.start():] if m else ""


def dap_an_tn(hdc: str) -> dict[str, str]:
    """{số câu: chữ} từ bảng 'Câu 1 2 3…' / 'Đáp án B C A…' hoặc dạng '1.B 2.C'."""
    ra: dict[str, str] = {}
    dong = hdc.splitlines()
    for i, d in enumerate(dong[:-1]):
        so = re.findall(r"\b(\d{1,2})\b", d) if re.match(r"^\s*câu\b", d, re.I) else []
        if len(so) >= 4:
            for d2 in dong[i + 1: i + 4]:
                ch = re.findall(r"\b([ABCD])\b", d2)
                if len(ch) >= len(so) - 1:
                    ra.update(dict(zip(so, ch)))
                    break
    for so, ch in re.findall(r"\b(\d{1,2})\s*[\.\-:]\s*([ABCD])\b", hdc):
        ra.setdefault(so, ch)
    return ra


def barem_bai(hdc: str) -> dict[str, str]:
    """{số bài: khối HDC thô} — chỉ phần sau bảng trắc nghiệm, cắt theo mốc Bài/Câu."""
    ms = list(_BAI_HDC.finditer(hdc))
    ra: dict[str, str] = {}
    for i, m in enumerate(ms):
        k = hdc[m.start(): ms[i + 1].start() if i + 1 < len(ms) else len(hdc)]
        so = m.group(1).upper()
        if len(k.strip()) > 30:
            ra[so] = ra.get(so, "") + k.strip()[:3000]
    return ra


# ───────────────────────── một đề ─────────────────────────
def doc_vdc_mat() -> dict[tuple[str, str, str], str]:
    """(lớp, kỳ, 50 kí tự đầu tên file) → chương (số La Mã) của CÂU CUỐI ĐỀ đã phân loại bằng mắt."""
    if not VDC_MAT.exists():
        return {}
    d = json.loads(VDC_MAT.read_text(encoding="utf-8"))
    return {(lop[-1], r["ky"], r["file"][:50]): r.get("chuong", "")
            for lop, v in d.get("khoi", {}).items() for r in v.get("cau_cuoi_de", [])}


VDC_TAY = doc_vdc_mat()


# ───────────────────────── chương theo kỳ ─────────────────────────
# Chương KNTT có thể có trong đề mỗi kỳ (đề lệch KNTT đã tách sang de-thi-lech-kntt/).
# (đại số, hình) — số La Mã khớp nhãn chương trong thong_ke_dang_de.DANG.
CHUONG_KY = {
    "6": {"gk1": ("I II", "IV"), "ck1": ("I II III", "IV V"),
          "gk2": ("VI VII IX", "VIII"), "ck2": ("VI VII IX", "VIII")},
    "7": {"gk1": ("I II", "III IV"), "ck1": ("I II V", "III IV"),
          "gk2": ("VI VII VIII V", "IX"), "ck2": ("VI VII VIII V", "IX X")},   # biểu đồ ở đề kỳ II = công cụ ch.V
    "8": {"gk1": ("I II", "III"), "ck1": ("I II V", "III IV"),
          "gk2": ("VI VII", "IX"), "ck2": ("VI VII VIII", "IX X")},
}
# Từ khoá PHỤ để chọn giữa các chương được phép (thứ tự = ưu tiên). Áp lên chữ đã chuan().
GOI_Y = {
    "6": [("IX", r"biểu đồ|bảng (số liệu|thống kê)|dữ liệu|xác suất|gieo|tung đồng xu|rút (thẻ|bóng)"),
          ("VI", r"phân số|\d\s*/\s*\d|hỗn số"), ("VII", r"\d,\d|%|phần trăm|làm tròn|số thập phân"),
          ("III", r"số nguyên|[-−]\s?\d|nhiệt độ|âm"),
          ("II", r"chia hết|ước|bội|nguyên tố|ưcln|bcnn|hợp số"),
          ("V", r"đối xứng"), ("VIII", r"điểm|đường thẳng|đoạn thẳng|\btia\b|góc|trung điểm"),
          ("IV", r"tam giác|hình (vuông|chữ nhật|thoi|bình hành|thang)|lục giác|chu vi|diện tích"),
          ("I", r".")],
    "7": [("V", r"biểu đồ|bảng (số liệu|thống kê)|dữ liệu"), ("VIII", r"xác suất|biến cố|gieo|ngẫu nhiên"),
          ("II", r"√|căn|vô tỉ|\||giá trị tuyệt đối|làm tròn|\bv\d"),   # OCR đọc √9 thành V9 ("VI", r"tỉ lệ|tỉ số|chia .{0,30}theo"),
          ("VII", r"đa thức|đơn thức|bậc|nghiệm|hệ số"),
          ("X", r"hình hộp|lăng trụ|lập phương"),
          ("IX", r"trọng tâm|trung tuyến|đường cao|trung trực|đồng quy|đường xiên|bất đẳng thức tam giác|lớn hơn"),
          ("IV", r"bằng nhau|cân|c\.g\.c|g\.c\.g|c\.c\.c|tam giác|∆|△|δ"),   # tổng ba góc = Bài 12, ch.IV
          ("III", r"song song|so le|đồng vị|kề bù|đối đỉnh|phân giác|góc"),
          ("I", r".")],
    "8": [("V", r"biểu đồ|bảng (số liệu|thống kê)|dữ liệu"), ("VIII", r"xác suất|biến cố|ngẫu nhiên|gieo"),
          ("VI", r"phân thức|mẫu thức|điều kiện xác định|đkxđ|rút gọn biểu thức"),
          ("VII", r"phương trình|hàm số|đồ thị|y ?= ?|hệ số góc"),
          ("II", r"hằng đẳng|nhân tử|bình phương|lập phương|tính nhanh|\(.{1,12}\)\s?[23²³]"),
          ("X", r"ch[óố]p"), ("IX", r"đồng dạng|∽|pythagore|py-?ta-?go|tỉ số đồng dạng"),
          ("IV", r"thal[eè]s|ta-?lét|đường trung bình|phân giác|song song .{0,40}(tính|độ dài)"),
          ("III", r"tứ giác|hình (thang|bình hành|chữ nhật|thoi|vuông)"),
          ("I", r".")],
}


def nhan_chuong(lop: str) -> dict[str, str]:
    """số La Mã → nhãn đầy đủ ('II' → 'II. Chia hết')."""
    return {ch.split(".")[0]: ch for ch, _, _ in T._bo_ma(lop) if "." in ch}


def chon_chuong(lop: str, ky: str, thuong: str, la_hinh: bool, chs: list[str],
                nhan: dict[str, str]) -> tuple[str, str]:
    """(nhãn chương, cờ đoán). Ưu tiên chương từ khoá NẰM TRONG phạm vi kỳ; không có thì
    đoán bằng từ khoá phụ trong phạm vi kỳ ('theo-ky'); kỳ chỉ còn 1 chương thì lấy luôn."""
    if ky == "*":
        dai = " ".join(sorted({c for a, _ in CHUONG_KY[lop].values() for c in a.split()}, key=list(nhan).index))
        hinh = " ".join(sorted({c for _, b in CHUONG_KY[lop].values() for c in b.split()}, key=list(nhan).index))
    else:
        dai, hinh = CHUONG_KY[lop][ky]
    duoc = (hinh if la_hinh else dai).split()
    tat_ca = (dai + " " + hinh).split()
    that = [c for c in chs if c not in ("Chung", "Nâng cao")]
    # Khớp nhiều chương trong phạm vi kỳ ⇒ lấy chương HỌC SAU: bài tam giác bằng nhau nào cũng
    # có chữ "góc" (ch.III), bài hằng đẳng thức nào cũng có "đa thức" (ch.I).
    thu_tu = list(nhan)
    trong = sorted({c for c in that if c.split(".")[0] in tat_ca},
                   key=lambda c: thu_tu.index(c.split(".")[0]), reverse=True)
    if trong:
        return trong[0], ""
    for so, rx in GOI_Y[lop]:
        if so in duoc and re.search(rx, thuong):
            return nhan[so], "theo-ky"
    if duoc:
        return nhan[duoc[0]], "theo-ky"
    return (that[0] if that else "?"), ""


def so_trang(raw: str, doan: str) -> int:
    k = raw.find(doan.strip().splitlines()[0][:60]) if doan.strip() else -1
    return raw.count("\f", 0, k) + 1 if k >= 0 else 0


def dung_mot_de(lop: str, ky: str, p: Path, nguon: str, raw: str, lech: str = "") -> dict | None:
    dong = T.khoi_de(raw)
    cau = []
    for phan, d in dong:
        m = T._CAU.match(d)
        if m or not cau:
            cau.append({"so": m.group(1).upper() if m else "?", "phan": phan, "text": d})
        else:
            cau[-1]["text"] += "\n" + d
    if len(cau) < 3:
        return None
    het_de = raw.find(cau[-1]["text"].splitlines()[-1]) if cau[-1]["text"] else 0
    hdc = phan_hdc(raw, max(het_de, 0))
    da_tn, bm = dap_an_tn(hdc), barem_bai(hdc)
    rx = [(ch, ten, re.compile(pt, re.I)) for ch, ten, pt in T._bo_ma(lop)]
    nhan_lop = {lop: nhan_chuong(lop)}
    nam, truong = T.ten_de(nfc(p.stem))
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", nfc(truong).replace("Đ", "D")
                  .replace("đ", "d")).encode("ascii", "ignore").decode().lower()).strip("-")[:40]
    ma_de = f"{ky}-{nam[:4] if nam != '?' else 'x'}-{slug}"

    tl = [c for c in cau if c["phan"] != "TN"] or [c for c in cau if not re.search(
        r"\bA\s*[\.\)].{0,300}\bB\s*[\.\)]", c["text"], re.S)]
    bai_cuoi = tl[-1]["so"] if tl else None
    ban_ghi = []
    for c in cau:
        tn = c["phan"] == "TN" and len(_TN_OPT.findall(c["text"])) >= 3
        # đề mẫu 2025: phần trắc nghiệm ĐÚNG/SAI a)–d) và TRẢ LỜI NGẮN — không phải bài tự luận
        ds = c["phan"] == "TN" and not tn
        diem = None
        md = re.search(r"\(\s*(\d+(?:[,.]\d+)?)\s*(?:điểm|đ)\s*\)", c["text"].split("\n")[0][:80])
        if md:
            diem = float(md.group(1).replace(",", "."))
        ys = [("", c["text"])] if tn else tach_y(c["text"])
        chung = c["text"][: c["text"].find(ys[0][1])] if len(ys) > 1 else ""
        la_hinh = bool(_HINH.search(c["text"])) and not tn
        for j, (nhan, doan) in enumerate(ys):
            thuong = T.chuan((chung + "\n" + doan) if chung else doan).replace("\n", " ")   # regex dạng không vượt dòng
            dang = [(ch, ten) for ch, ten, r in rx if r.search(thuong)]
            chuong, doan_ch = chon_chuong(lop, "*" if lech else ky, thuong, la_hinh or bool(_HINH.search(thuong)),
                                          [ch for ch, _ in dang], nhan_lop[lop])
            cuoi_bai = j == len(ys) - 1
            nhieu_y = len(ys) >= 3
            if tn:
                band = "NB"
            elif ds:
                band = "NB" if j < 2 else "TH"
            elif c["so"] == bai_cuoi and cuoi_bai and (diem is None or diem <= 1.0):
                band = "VDC"
                tay = VDC_TAY.get((lop, ky, p.stem[:50]), "")
                nhan_ch = nhan_lop[lop].get(tay)
                if nhan_ch:
                    chuong, doan_ch = nhan_ch, ""   # chương phân loại bằng mắt thắng từ khoá
            elif la_hinh and cuoi_bai and nhieu_y:
                band = "VDC"                        # ý cuối bài hình (quy ước anh An)
            elif la_hinh and nhieu_y and j == len(ys) - 2:
                band = "VD"                         # ý áp chót bài hình
            elif _LOI_VAN.search(thuong) and not la_hinh:
                band = "VD"
            elif not la_hinh and nhieu_y and cuoi_bai:
                band = "VD"                         # ý c) bài đại số nhiều ý
            elif _NB_DONG_TU.search(T.chuan(re.sub(r"^\s*[a-e]\s*[\)\.]\s*", "", doan.strip()))) and j == 0:
                band = "NB"
            else:
                band = "TH"
            bg = {
                "id": f"l{lop}-{ma_de}-{'c' if tn or ds else 'b'}{c['so']}{nhan}".lower(),   # cùng trường ra đề nhiều khối
                "vi_tri": f"{'Câu' if tn else 'Bài'} {c['so']}{('.' + nhan) if nhan else ''}",
                "loai": "TN" if tn else ("TN-DS" if ds else "TL"),
                "chuong": chuong,
                **({"_chuong_doan": doan_ch} if doan_ch else {}),
                "dang": [ten for _, ten in dang],
                "band": band, "_band_auto": True,
                "phut": PHUT[band], "_phut_auto": True,
                "diem_bai": diem,
                "de_chung": dong_dau(chung, 900) if chung else "",
                "de": dong_dau(doan, 900),
                "trang": so_trang(raw, doan),
                "co_hinh": bool(re.search(r"hình vẽ|như hình|hình bên|hình dưới|biểu đồ", thuong)),
                "can_doc_anh": nguon == "ocr" or bool(_RAC.search(doan)),
                "da_duyet": False,
            }
            if tn and c["so"] in da_tn:
                bg["dap_an"] = da_tn[c["so"]]
                bg["barem_nguon"] = "goc_tho"
            elif not tn and c["so"] in bm:
                bg["barem_tho"] = bm[c["so"]] if j == 0 else f"(xem l{lop}-{ma_de}-b{c['so']}{ys[0][0]})".lower()
                bg["barem_nguon"] = "goc_tho"
            else:
                bg["barem_nguon"] = "chua_co"
            ban_ghi.append(bg)
    # đề hai mã / đề tách hai phần đánh lại từ Câu 1 ⇒ id vẫn có thể trùng: đánh số phụ
    dem: Counter = Counter()
    for bg in ban_ghi:
        dem[bg["id"]] += 1
        if dem[bg["id"]] > 1:
            bg["id"] += f"-{dem[bg['id']]}"
    return {
        "xuat_xu": {"lop": lop, "ky": ky.upper(), "nam": nam, "truong": truong,
                    "nguon": str(p.relative_to(ROOT)), "loai_pdf": nguon,
                    "co_bieu_diem": bool(hdc),
                    **({"lech_kntt": lech} if lech else {})},
        "tang": 1,
        "da_duyet": False,
        "ghi_chu": "TẦNG 1 máy dựng — chữ thô, chưa LaTeX, band/chương tự động. "
                   "Bốc vào phiếu phải đọc ảnh trang `trang` và kiểm đáp án.",
        "cau": ban_ghi,
    }


# Trường do người/agent thêm sau khi máy dựng (tầng 2: đọc ảnh, gõ lại LaTeX, giải) — dựng lại
# KHÔNG được xoá (15/10/2026: agent hồ sơ chương đã gõ lại 136 câu lớp 6 vào exam JSON).
TRUONG_TANG2 = ("de_latex", "dap_an_kiem", "da_duyet")


def giu_tang2(dich: Path, d: dict) -> None:
    """Chép trường tầng 2 của bản cũ (cùng id câu) sang bản vừa dựng."""
    if not dich.exists():
        return
    try:
        cu = {c.get("id"): c for c in json.loads(dich.read_text(encoding="utf-8")).get("cau", [])}
    except (ValueError, OSError):
        return
    for c in d["cau"]:
        old = cu.get(c["id"])
        if not old:
            continue
        for k, v in old.items():
            if (k in TRUONG_TANG2 or k.startswith("tang2")) and v not in (None, "", False):
                c[k] = v


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lop", default="6,7,8")
    a = ap.parse_args(argv[1:])
    tong = {}
    for lop in a.lop.split(","):
        out = DE / f"lop-{lop}" / "exams"
        out.mkdir(exist_ok=True)
        for f in out.glob("*.json"):
            f.unlink()                       # tầng 1 sinh lại toàn bộ — không ai sửa tay
        seen_b, seen_t = set(), set()
        st = Counter(); bang = defaultdict(Counter); ids = Counter()
        ds = []
        for p in sorted((DE / f"lop-{lop}").rglob("*.pdf")):
            if nhan_file(p):
                ds.append((p, ""))
        for p in sorted((LECH / f"lop-{lop}").rglob("*.pdf")):
            ly = LY_DO.get(str(p.relative_to(LECH)), "lệch KNTT")
            if not re.search(r"cánh diều|bộ sách|ctst|chân trời", ly, re.I):
                ds.append((p, ly))
        thieu = [p for p, _ in ds if not duong_txt(p).exists()]
        if thieu:
            from concurrent.futures import ProcessPoolExecutor
            print(f"  lớp {lop}: tạo text cho {len(thieu)} đề…", flush=True)
            with ProcessPoolExecutor(8) as ex:
                list(ex.map(tao_text, thieu))
        for p, lech in ds:
            ky = next((KY_DIR[x] for x in p.parts if x in KY_DIR), None)
            if not ky:
                continue
            h = hashlib.sha1(p.read_bytes()).hexdigest()
            if h in seen_b:
                st["trung_byte"] += 1
                continue
            seen_b.add(h)
            tx = lay_text(p)
            if not tx:
                st["khong_text"] += 1
                continue
            nguon, raw = tx
            ht = hashlib.sha1(re.sub(r"\W", "", raw[:4000]).encode()).hexdigest()
            if ht in seen_t:
                st["trung_chu"] += 1
                continue
            seen_t.add(ht)
            d = dung_mot_de(lop, ky, p, nguon, raw, lech)
            if not d:
                st["khong_tach_duoc"] += 1
                continue
            ma = d["cau"][0]["id"].rsplit("-", 1)[0]
            ids[ma] += 1
            ten = ma if ids[ma] == 1 else f"{ma}-{ids[ma]}"
            if ids[ma] > 1:
                for c in d["cau"]:
                    c["id"] = c["id"].replace(ma, ten, 1)
                    if c.get("barem_tho", "").startswith("(xem "):
                        c["barem_tho"] = c["barem_tho"].replace(ma, ten, 1)
            dich = out / f"{ten.split('-', 1)[1]}.json"
            giu_tang2(dich, d)
            dich.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            st["de"] += 1; st[f"de_{nguon}"] += 1; st["cau"] += len(d["cau"])
            if lech:
                st["de_lech_kntt"] += 1; st["cau_lech_kntt"] += len(d["cau"])
            st["co_dap_an"] += sum(1 for c in d["cau"] if c["barem_nguon"] != "chua_co")
            st["can_doc_anh"] += sum(1 for c in d["cau"] if c["can_doc_anh"])
            for c in d["cau"]:
                bang[(ky.upper(), c["chuong"])][c["band"]] += 1
        tong[lop] = st
        (DE / f"lop-{lop}" / "ngan-hang-tong-hop.json").write_text(json.dumps({
            "_doc": "Sinh bởi scripts/build_ngan_hang_678.py — đếm bản ghi tầng 1 theo (kỳ, chương) × band.",
            "thong_ke": dict(st),
            "bang": {f"{k[0]}|{k[1]}": dict(v) for k, v in sorted(bang.items())},
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"lớp {lop}: {dict(st)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
