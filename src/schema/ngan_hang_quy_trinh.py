"""Quy trình dựng NGÂN HÀNG BÀI theo chương (Bước 0, trước thuyết minh — Thầy chốt 22/10/2026).

Hàm thuần (không gọi mạng) cho `scripts/ngan_hang_sheet.py`:
  kiểm kê inputs → chia việc cho agent quét → soát bản ghi → gán phiếu theo KHUNG chương
  → dựng hàng tab phân dạng → nén + chia khối để ghi Sheets → đối chiếu sau khi ghi.

KHUNG chương: `config/khung-phan-dang/<grade>-<subject>-chuong-NN.json` (phạm vi, nguồn, luật gán phiếu).
Bản ghi agent: `inputs/refs/ngan-hang-sheet/<grade>/<subject>/chuong-NN/ban-ghi/*.json` (+ `log/*.txt`).
"""
from __future__ import annotations

import json
import re
import string
import unicodedata
from collections import Counter
from pathlib import Path

from config import settings
from src.schema import ngan_hang_sheet as nhs

ROOT = settings.ROOT
KHUNG_DIR = ROOT / "config" / "khung-phan-dang"
OUT_DIR = ROOT / "outputs" / "ngan-hang-sheet"

ORDER = {"VDC": 0, "VD": 1, "TH": 2, "NB": 3}
# Phút/ý tự luận theo ngân hàng đề (exams/: NB 5, TH 6, VD 10, VDC 13); câu ngắn TN/điền/trả lời ngắn
PHUT_TL = {"NB": 5, "TH": 6, "VD": 10, "VDC": 13}
PHUT_NGAN = {"NB": 1, "TH": 2, "VD": 3, "VDC": 4}
PHUT_DUNG_SAI = 4
PHUT_VE_HINH = 5          # bài hình tổng hợp tự luận: HS tự vẽ hình
UU = {1: "Ưu tiên 1: Đề thi chính thức", 2: "Ưu tiên 2: SGK", 3: "Ưu tiên 3: nguồn khác: Sách tham khảo"}
FMTS = ("Tự luận", "Trắc nghiệm chọn đáp án", "Trắc nghiệm đúng sai", "Trả lời ngắn", "Điền khuyết")
KEYS = ("id", "nguon", "file", "uu", "bai", "de", "y", "dang", "tt", "fmt")
SO_FILE_MOI_VIEC = {"de": 20, "sgk": 1, "tai_lieu": 4}


# ── khung & thư mục ──────────────────────────────────────────────────────────
def khung_path(grade: str, subject: str, chuong: int) -> Path:
    return KHUNG_DIR / f"{grade}-{subject}-chuong-{int(chuong):02d}.json"


def load_khung(grade: str, subject: str, chuong: int) -> dict:
    p = khung_path(grade, subject, chuong)
    if not p.exists():
        raise FileNotFoundError(f"chưa có khung {p.relative_to(ROOT)} — chép từ chương V làm mẫu")
    return json.loads(p.read_text(encoding="utf-8"))


def chuong_dir(grade: str, subject: str, chuong: int) -> Path:
    return nhs.SNAP_DIR / grade / subject / f"chuong-{int(chuong):02d}"


def out_dir(grade: str, subject: str, chuong: int) -> Path:
    return OUT_DIR / f"{grade}-{subject}-chuong-{int(chuong):02d}"


# ── ① kiểm kê inputs ─────────────────────────────────────────────────────────
def kiem_ke(khung: dict) -> list[dict]:
    """Mọi file nguồn phải mở cho chương: [{file, nhom, viec}]. Không lọc trước bằng từ khoá."""
    items: list[dict] = []
    for d in khung.get("nguon_de", []):
        for f in sorted((ROOT / d).glob("*.pdf")):
            items.append({"file": str(f.relative_to(ROOT)), "nhom": "de", "goc": Path(d).name})
    sgk = khung.get("sgk")
    if sgk:
        items.append({"file": sgk["file"], "nhom": "sgk", "goc": "sgk"})
    for t in khung.get("tai_lieu", []):
        p = ROOT / t
        fs = sorted(p.glob("*.pdf")) if p.is_dir() else [p]
        for f in fs:
            items.append({"file": str(f.relative_to(ROOT)), "nhom": "tai_lieu", "goc": p.name if p.is_dir() else "tl"})
    # chia việc: cùng (nhóm, gốc), mỗi việc ≤ SO_FILE_MOI_VIEC[nhóm] file
    by: dict[tuple, list[dict]] = {}
    for it in items:
        by.setdefault((it["nhom"], it["goc"]), []).append(it)
    for (nhom, goc), lst in by.items():
        n = SO_FILE_MOI_VIEC[nhom]
        for k in range(0, len(lst), n):
            ten = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", goc).encode("ascii", "ignore").decode().lower()).strip("-")
            viec = f"{nhom}-{ten or 'x'}-{k // n + 1}"
            for it in lst[k:k + n]:
                it["viec"] = viec
    return items


# ── ② soát bản ghi ───────────────────────────────────────────────────────────
def kiem_ban_ghi(recs: list[dict], co_san: set[str] = frozenset()) -> list[str]:
    """Lỗi chặn: thiếu khoá, band lạ, fmt lạ, uu lạ, id trùng (trong lô hoặc với tab), file không tồn tại."""
    loi, seen = [], Counter(r.get("id") for r in recs)
    for r in recs:
        rid = r.get("id", "?")
        miss = [k for k in KEYS if k not in r]
        if miss:
            loi.append(f"{rid}: thiếu {miss}")
            continue
        if not r["y"] or any(b not in ORDER for _, b in r["y"]):
            loi.append(f"{rid}: mức ý lạ {r['y']}")
        if r["fmt"] not in FMTS:
            loi.append(f"{rid}: fmt lạ '{r['fmt']}'")
        if r["uu"] not in UU:
            loi.append(f"{rid}: uu lạ {r['uu']}")
        if seen[rid] > 1:
            loi.append(f"{rid}: id trùng trong lô ({seen[rid]} lần)")
        if rid in co_san:
            loi.append(f"{rid}: id đã có trên tab")
        if not (ROOT / unicodedata.normalize("NFC", r["file"])).exists() and not (ROOT / unicodedata.normalize("NFD", r["file"])).exists():
            loi.append(f"{rid}: file không tồn tại {r['file']}")
        if not str(r["de"]).strip():
            loi.append(f"{rid}: đề rỗng")
    return loi


def kiem_log(items: list[dict], logs: dict[str, str]) -> list[str]:
    """Mỗi file kiểm kê phải có dòng trong log của việc (kể cả 0 bài + lý do)."""
    thieu = []
    for it in items:
        txt = logs.get(it["viec"], "")
        ten = Path(it["file"]).name
        if ten not in txt and unicodedata.normalize("NFD", ten) not in txt and it["file"] not in txt:
            thieu.append(it["file"])
    return thieu


# ── ③ gán phiếu + dựng hàng ─────────────────────────────────────────────────
def tong_hop(r: dict) -> bool:
    return "tổng hợp" in r.get("bai", "")


def gan_phieu(r: dict, khung: dict) -> str:
    """Luật trong khung: chạy theo thứ tự; luật `dung` khớp ⇒ trả ngay nhãn đó; còn lại GOM nhiều nhãn
    (một bài dùng được cho nhiều phiếu); `mac_dinh` luôn có khi không nhãn nào khớp."""
    bai, dang = r.get("bai", ""), r.get("dang", "")
    text = f"{dang}\n{r.get('de', '')}"
    tags: list[tuple[int, str]] = []
    mac_dinh = None
    for k, lu in enumerate(khung.get("luat_phieu", [])):
        if lu.get("bai") and not any(bai.startswith(b) for b in lu["bai"]):
            continue
        if "tong_hop" in lu and lu["tong_hop"] != tong_hop(r):
            continue
        if lu.get("regex_dang") and not re.search(lu["regex_dang"], dang.lower()):
            continue
        hit = not lu.get("regex") or re.search(lu["regex"], text)
        if lu.get("dung"):
            if hit:
                return lu["nhan"]
            continue
        if lu.get("mac_dinh"):
            mac_dinh = (lu.get("so", k), lu["nhan"], bool(hit))
            continue
        if hit:
            tags.append((lu.get("so", k), lu["nhan"]))
    if mac_dinh and (mac_dinh[2] or not tags):
        tags.append(mac_dinh[:2])
    s = "; ".join(n for _, n in sorted(set(tags)))
    if khung.get("nhan_luyen_tap") and (tong_hop(r) or len(r["y"]) >= 3):
        s += f"; {khung['nhan_luyen_tap']}"
    return s or "Chưa có phiếu"


def phut(r: dict) -> float:
    if r.get("phut"):
        return r["phut"]
    if r.get("fmt") == "Trắc nghiệm đúng sai":
        return PHUT_DUNG_SAI
    bang = PHUT_TL if r.get("fmt", "Tự luận") == "Tự luận" else PHUT_NGAN
    t = sum(bang[b] for _, b in r["y"])
    if tong_hop(r) and r.get("fmt", "Tự luận") == "Tự luận":
        t += PHUT_VE_HINH
    return t


def dung_hang(recs: list[dict], khung: dict) -> list[list]:
    """Bản ghi → hàng 13 cột của tab (A Bài cụ thể … M Mã câu), sắp mức cao trước rồi ưu tiên nguồn."""
    out = []
    for r in recs:
        top = min((b for _, b in r["y"]), key=ORDER.get)
        tung = " · ".join(f"{l}) {b}" if l else b for l, b in r["y"])
        row = [r["de"], r["nguon"], top, r["dang"], UU[r["uu"]], gan_phieu(r, khung), phut(r),
               "Có" if r.get("tt") else "Không", r.get("fmt", "Tự luận"), tung,
               r.get("bai", ""), r.get("note", "") or "", r["id"]]
        out.append(((ORDER[top], r["uu"]), row))
    out.sort(key=lambda x: x[0])
    # ô bắt đầu bằng = + - bị Sheets hiểu là công thức ⇒ thêm nháy đơn
    return [[("'" + c) if isinstance(c, str) and c[:1] in "=+-" else c for c in row] for _, row in out]


# ── ④ nén + chia khối để ghi Sheets ─────────────────────────────────────────
def nen(rows: list[list], *, nguong: int = 3, min_len: int = 10,
        tu_them: tuple[str, ...] = ()) -> tuple[list[list], list[tuple[str, str]]]:
    """Thay cụm lặp bằng mã `~XX~` (gõ ít token hơn khi ghi), trả (rows_nen, [(mã, chữ)]).
    Ghi xong chạy findReplace mã→chữ là ra đúng bản gốc."""
    cnt = Counter(c for r in rows for c in r[1:12] if isinstance(c, str) and len(c) >= 18)
    subs = {k for k, v in cnt.items() if v >= nguong}
    for frag in tu_them:
        if sum(c.count(frag) for r in rows for c in r if isinstance(c, str)) >= nguong and len(frag) >= min_len:
            subs.add(frag)
    subs = sorted(subs, key=lambda s: -len(s))
    if any("~" in c for r in rows for c in r if isinstance(c, str)):
        raise ValueError("dữ liệu có sẵn ký tự '~' — không nén được")
    codes = ["~" + a + b + "~" for a in string.ascii_uppercase for b in string.ascii_uppercase]
    m = dict(zip(subs, codes))
    out = []
    for r in rows:
        y = []
        for c in r:
            if isinstance(c, str):
                for s in subs:
                    c = c.replace(s, m[s])
            y.append(c)
        out.append(y)
    pairs = [(m[s], s) for s in subs]
    if giai_nen(out, pairs) != rows:
        raise AssertionError("nén–giải nén không khớp")
    return out, pairs


def giai_nen(rows: list[list], pairs: list[tuple[str, str]]) -> list[list]:
    out = []
    for r in rows:
        y = []
        for c in r:
            if isinstance(c, str):
                for code, s in pairs:
                    c = c.replace(code, s)
            y.append(c)
        out.append(y)
    return out


def chia_khoi(rows: list[list], start_row: int, max_bytes: int = 22000) -> list[dict]:
    ch, cur, s = [], [], 0
    for x in rows:
        z = len(json.dumps(x, ensure_ascii=False).encode())
        if s + z > max_bytes and cur:
            ch.append(cur); cur, s = [], 0
        cur.append(x); s += z
    if cur:
        ch.append(cur)
    out, r0 = [], start_row
    for c in ch:
        out.append({"start": r0, "end": r0 + len(c) - 1, "rows": c}); r0 += len(c)
    return out


def find_replace_requests(pairs, sheet_tab_id: int, r0: int, r1: int) -> list[dict]:
    """Lệnh batchUpdate bung mã → chữ, chỉ trong vùng dòng [r0, r1] (đánh số 1 như Sheets)."""
    rng = {"sheetId": sheet_tab_id, "startRowIndex": r0 - 1, "endRowIndex": r1,
           "startColumnIndex": 0, "endColumnIndex": 13}
    return [{"findReplace": {"find": c, "replacement": s, "range": rng, "matchCase": True}} for c, s in pairs]


# ── ⑤ đối chiếu sau khi ghi ─────────────────────────────────────────────────
def _chuan(v) -> str:
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    s = unicodedata.normalize("NFC", str(v)).strip()
    return s[1:] if s.startswith("'") else s


def doi_chieu(values: list[list], expected: list[list]) -> list[str]:
    """So tab (get_values, hàng 1 = tiêu đề) với hàng mong đợi THEO MÃ CÂU (tab có thể đã sắp lại)."""
    tab = {}
    for r in values[1:]:
        r = list(r) + [""] * (13 - len(r))
        if r[12]:
            tab[r[12]] = r
    loi = []
    for e in expected:
        g = tab.get(_chuan(e[12]))
        if g is None:
            loi.append(f"{e[12]}: không thấy trên tab")
            continue
        for j in range(13):
            if _chuan(g[j]) != _chuan(e[j]):
                loi.append(f"{e[12]} cột {'ABCDEFGHIJKLM'[j]}: tab '{_chuan(g[j])[:40]}' ≠ '{_chuan(e[j])[:40]}'")
    return loi


def ma_con_sot(values: list[list]) -> int:
    return sum(1 for r in values for c in r if isinstance(c, str) and re.search(r"~[A-Z]{2}~", c))
