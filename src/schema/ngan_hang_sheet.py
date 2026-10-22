"""NGÂN HÀNG ĐỀ THEO CHƯƠNG = tab "Phân dạng …" trên Google Sheets (Thầy chốt 22/10/2026).

Quy trình mới: mỗi chương có MỘT tab phân dạng trên sheet dùng chung của nhóm, chứa
MỌI bài lọc từ đề thi / SGK / tài liệu tham khảo trong `inputs/` (chép nguyên văn).
Thuyết minh và phiếu CHỈ được bốc bài từ tab đó — `SpecRow.source_refs` phải là
"Mã câu" (cột M) của tab.

Repo không gọi được Google API, nên tab được chụp thành SNAPSHOT JSON trong repo:
    inputs/refs/ngan-hang-sheet/<grade>/<subject>/chuong-NN.json
(agent đọc tab bằng connector Sheets `get_values`, lưu JSON thô, rồi
`python scripts/ngan_hang_sheet.py nap …` chuyển thành snapshot). Sheet là nguồn
sự thật; snapshot chỉ là bản chụp để gate/tool đọc offline — sửa sheet xong phải nạp lại.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from config import settings

SNAP_DIR = settings.ROOT / "inputs" / "refs" / "ngan-hang-sheet"
BANDS_ORDER = ("NB", "TH", "VD", "VDC")

# Cột của tab phân dạng (khớp "Mẫu phiếu phân dạng" + 4 cột thêm J–M). Đổi thứ tự cột
# trên sheet thì đổi ở đây; `nap` đối chiếu theo TIÊU ĐỀ chứ không theo vị trí.
COLS = {
    "de": "Bài cụ thể",
    "nguon": "Nguồn trong input",
    "band": "Mức độ",
    "dang": "Dạng bài",
    "uu": "Ưu tiên",
    "phieu": "Phân loại vào phiếu",
    "phut": "Thời lượng",
    "thuc_te": "thực tế",
    "fmt": "Format",
    "muc_y": "Mức độ từng ý",
    "bai": "Bài học SGK",
    "note": "Ghi chú",
    "ma": "Mã câu",
}


def snapshot_path(grade: str, subject: str, chuong: str | int) -> Path:
    n = int(re.sub(r"\D", "", str(chuong)) or 0)
    return SNAP_DIR / grade / subject / f"chuong-{n:02d}.json"


def chuong_of_slug(text: str) -> int | None:
    """'thuyet-minh-lop-9c-chuong-05-duong-tron-ban-2' → 5."""
    m = re.search(r"chuong-(\d{1,2})", text or "")
    return int(m.group(1)) if m else None


def parse_muc_y(s: str) -> list[tuple[str, str]]:
    """'a) TH · b) VD · c) VDC' → [('a','TH'),('b','VD'),('c','VDC')]; 'TH' → [('', 'TH')]."""
    out = []
    for part in re.split(r"\s*·\s*", (s or "").strip()):
        m = re.match(r"^(?:([a-z0-9.]+)\)\s*)?(NB|TH|VDC|VD)$", part.strip())
        if m:
            out.append((m.group(1) or "", m.group(2)))
    return out


def phieu_so(s: str) -> set[int]:
    """'Phiếu 2 (bốn điểm, tiếp tuyến); luyện tập P5–P6' → {2, 5, 6}. 'Chưa có phiếu' → {}."""
    s = s or ""
    if s.lower().startswith("chưa"):
        return set()
    out = {int(x) for x in re.findall(r"Phiếu\s*(\d+)", s)}
    for a, b in re.findall(r"P(\d+)\s*[–-]\s*P(\d+)", s):
        out |= set(range(int(a), int(b) + 1))
    out |= {int(x) for x in re.findall(r"\bP(\d+)\b", s)}
    return out


def uu_so(s: str) -> int:
    m = re.search(r"Ưu tiên\s*(\d)", s or "")
    return int(m.group(1)) if m else 9


def from_values(values: list[list[str]], *, sheet_id: str, tab: str, pulled_at: str) -> dict:
    """Bảng `get_values` thô (hàng 1 = tiêu đề) → snapshot dict. Bỏ hàng không có Mã câu."""
    if not values:
        raise ValueError("bảng rỗng")
    head = values[0]
    idx = {}
    for key, label in COLS.items():
        hit = [i for i, h in enumerate(head) if label.lower() in (h or "").lower()]
        if not hit:
            raise ValueError(f"không thấy cột '{label}' trong tiêu đề tab")
        idx[key] = hit[0]
    rows, seen, dup = [], set(), []
    for r in values[1:]:
        r = list(r) + [""] * (len(head) - len(r))
        rec = {k: (r[i] or "").strip() if isinstance(r[i], str) else r[i] for k, i in idx.items()}
        if not rec["ma"]:
            continue
        if rec["ma"] in seen:
            dup.append(rec["ma"])
        seen.add(rec["ma"])
        try:
            rec["phut"] = float(str(rec["phut"]).replace(",", "."))
        except ValueError:
            rec["phut"] = None
        rows.append(rec)
    if dup:
        raise ValueError(f"Mã câu trùng trong tab: {sorted(set(dup))[:10]}")
    return {"sheet_id": sheet_id, "tab": tab, "pulled_at": pulled_at, "rows": rows}


_CACHE: dict[Path, dict | None] = {}


def load(grade: str, subject: str, chuong: str | int) -> dict | None:
    """Snapshot của chương, hoặc None nếu chương chưa có tab phân dạng."""
    p = snapshot_path(grade, subject, chuong)
    if p not in _CACHE:
        _CACHE[p] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    return _CACHE[p]


def index(snap: dict) -> dict[str, dict]:
    return {r["ma"]: r for r in snap.get("rows", [])}


def resolve(ma: str, idx: dict[str, dict]) -> dict | None:
    """Tìm 1 ref trong tab. Cho phép trỏ một Ý của bài: 'ck1-ai-mo-2.b' / 'ck1-ai-mo-2b'."""
    if ma in idx:
        return idx[ma]
    m = re.match(r"^(.*?)(?:\.|-)?([a-e])$", ma)
    if m and m.group(1) in idx:
        return idx[m.group(1)]
    return None
