"""staleness_gate — PDF trong `outputs/` có còn khớp nguồn sinh ra nó không?

Vì sao có cổng này (Thầy bắt 2026-08-19): phiếu thuyết minh chương V trên Drive là bản
build **12/08**, trong khi `thuyetminh_renderer.py` sửa lần cuối **16/08**. Bản Thầy mở ra
đọc có bố cục cũ (ô "Tên bài"/"Thời lượng" chảy liền một khối thay vì xuống dòng từng gạch
đầu dòng) nên trông "khác hẳn chương IV" — mà không cổng nào kêu, `sync-drive` thì chép mù.

CÁCH ĐO: **dựng lại `.tex` từ seed bằng template HIỆN TẠI rồi so hash** với sidecar
`<file>.tex.sha256` mà `latex_builder` đã ghi lúc build. Hash khác ⇒ bản in trong tay Thầy
không còn là thứ seed + template bây giờ sinh ra.

⚠️ CỐ Ý KHÔNG so `mtime`. Bản đầu đo bằng mtime, nhưng `git stash`/`checkout` sờ vào file
là đổi mtime dù nội dung y nguyên ⇒ 4 phiếu chương IV vừa build xong đã bị báo "lỗi thời".
Hash thì miễn nhiễm với chuyện đó, lại bắt được cả trường hợp ngược (file bị chạm nhưng
nội dung không đổi thì KHÔNG kêu).

Ba lý do, tách riêng vì cách chữa khác nhau:
  • `noi-dung`  — .tex dựng lại khác bản đã build ⇒ sửa seed hoặc đổi template mà chưa
                  build lại. Chữa: `make b Q="…"` (một phiếu) hoặc `make rebuild` (cả kho).
  • `thieu-dau` — không có sidecar `.tex.sha256` ⇒ PDF build từ thời chưa có cơ chế hash,
                  không cách nào biết còn khớp không. Coi như phải build lại.
  • `mat-nguon` — không truy được seed theo slug ⇒ output mồ côi (phiếu đã xoá/đổi tên).
                  Chữa: `make prune`.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from config import settings

_SEEDS_DIR = settings.ROOT / "inputs" / "seeds"
_CHUA = {
    "noi-dung": "seed/template đã đổi mà chưa build lại",
    "thieu-dau": "build từ thời chưa ghi hash — không kiểm được",
    "mat-nguon": "không còn seed nào sinh ra nó (output mồ côi)",
}
_CACH = {
    "noi-dung": 'make b Q="…"  hoặc  make rebuild',
    "thieu-dau": "make rebuild",
    "mat-nguon": "make prune",
}


@dataclass
class Stale:
    pdf: Path
    ly_do: str          # "noi-dung" | "thieu-dau" | "mat-nguon"

    def __str__(self) -> str:
        try:
            ten = self.pdf.relative_to(settings.ROOT)
        except ValueError:
            ten = self.pdf
        return f"{ten} — {_CHUA[self.ly_do]}. Chạy `{_CACH[self.ly_do]}`."


@lru_cache(maxsize=1)
def _quet_seed() -> tuple[dict[tuple[str, str], Path], dict[str, Path], frozenset[str]]:
    """Quét một lượt inputs/seeds, trả ba thứ:

    • theo_vi_tri — (đường dẫn thư mục tương đối, slug) → seed. Khoá CHÍNH.
    • theo_slug   — slug → seed, CHỈ giữ slug duy nhất toàn kho.
    • nhap_nhang  — các slug bị trùng ở nhiều tầng/lớp.

    Vì sao cần khoá theo vị trí (bắt 2026-08-22): chương V lớp 9 có **cùng bộ slug**
    ở cả `lop-b` lẫn `lop-c` (`phieu-a-mo-dau-ve-duong-tron`…). Bản đầu chỉ khoá theo
    slug nên bản đồ ghi đè lẫn nhau, PDF tầng C bị đem so với seed tầng B ⇒ 21 PDF vừa
    build xong đã bị báo "lỗi thời" và `sync-drive` từ chối đẩy Drive.
    """
    theo_vi_tri: dict[tuple[str, str], Path] = {}
    theo_slug: dict[str, Path] = {}
    trung: set[str] = set()
    for f in _SEEDS_DIR.rglob("*.json"):
        try:
            slug = json.loads(f.read_text(encoding="utf-8")).get("slug")
        except Exception:  # noqa: BLE001 — seed hỏng là việc của schema_validator
            continue
        if not slug:
            continue
        theo_vi_tri[(f.parent.relative_to(_SEEDS_DIR).as_posix(), slug)] = f
        if slug in theo_slug:
            trung.add(slug)
        theo_slug[slug] = f
    return theo_vi_tri, {k: v for k, v in theo_slug.items() if k not in trung}, frozenset(trung)


def _seed_theo_slug() -> dict[str, Path]:
    """slug phiếu/spec → file JSON nguồn (chỉ slug DUY NHẤT; trùng thì tra theo vị trí)."""
    return _quet_seed()[1]


def _vi_tri(d: Path) -> tuple[str, str] | None:
    """Thư mục output → (đường dẫn thư mục tương đối như bên seeds, slug)."""
    try:
        return d.parent.resolve().relative_to(settings.OUTPUTS_DIR).as_posix(), d.name
    except ValueError:
        return None


def _tex_hien_tai(seed: Path) -> dict[str, str] | None:
    """Dựng lại .tex từ seed bằng template hiện tại → {biến thể: sha256}.

    None = không dựng nổi (seed hỏng / schema đổi) ⇒ để cổng khác lo, đừng báo oan.
    """
    from src.compiler.jinja_renderer import (load_tokens, render_guide, render_handout,
                                             render_slide)
    try:
        data = json.loads(seed.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None

    def _h(s: str) -> str:
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    try:
        if "phieu" in data:                       # phiếu THUYẾT MINH (spec)
            from src.compiler.thuyetminh_renderer import render_thuyetminh
            from src.schema.thuyetminh_spec import ThuyetMinhSpec
            spec = ThuyetMinhSpec.model_validate(data)
            return {"thuyetminh": _h(render_thuyetminh(spec))}
        from src.schema.lesson_package import LessonPackage
        les = LessonPackage.model_validate(data)
        tokens = load_tokens()
        return {"handout": _h(render_handout(les, tokens)),
                "guide": _h(render_guide(les, tokens)),
                "slide": _h(render_slide(les, tokens))}
    except Exception:  # noqa: BLE001
        return None


def _bien_the(pdf: Path) -> str:
    """'ca-01-handout.pdf' → 'handout'; PDF thuyết minh (tên = slug) → 'thuyetminh'."""
    duoi = pdf.stem.rsplit("-", 1)[-1]
    return duoi if duoi in ("handout", "guide", "slide") else "thuyetminh"


def check_stale(out_dirs) -> list[Stale]:
    """Soi mọi PDF trong các thư mục output đã cho. [] = mọi bản in còn khớp nguồn."""
    theo_vi_tri, _, nhap_nhang = _quet_seed()
    seeds = _seed_theo_slug()
    ra: list[Stale] = []
    for d in map(Path, out_dirs):
        pdfs = sorted(d.glob("*.pdf"))
        if not pdfs:
            continue
        vt = _vi_tri(d)
        seed = (theo_vi_tri.get(vt) if vt else None) or seeds.get(d.name)
        if seed is None:
            if d.name in nhap_nhang:
                continue                          # slug trùng, không truy được → đừng báo oan
            ra += [Stale(p, "mat-nguon") for p in pdfs]
            continue
        hien = _tex_hien_tai(seed)
        if hien is None:
            continue                              # không dựng nổi → không kết luận
        for pdf in pdfs:
            sidecar = d / f"{pdf.stem}.tex.sha256"
            if not sidecar.exists():
                ra.append(Stale(pdf, "thieu-dau"))
                continue
            moi = hien.get(_bien_the(pdf))
            if moi and sidecar.read_text(encoding="utf-8").strip() != moi:
                ra.append(Stale(pdf, "noi-dung"))
    return ra


def tom_tat(stales: list[Stale]) -> str:
    """Một dòng đếm theo lý do, để in ở cuối bản audit."""
    if not stales:
        return "không có"
    dem = {k: sum(1 for s in stales if s.ly_do == k) for k in _CHUA}
    chi_tiet = ", ".join(f"{v} {k}" for k, v in dem.items() if v)
    return f"{len(stales)} PDF lỗi thời ({chi_tiet})"
