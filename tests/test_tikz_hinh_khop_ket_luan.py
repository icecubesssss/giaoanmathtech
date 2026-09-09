r"""Đề bắt chứng minh tứ giác $XYZW$ là hình gì thì HÌNH VẼ phải đúng là hình ấy.

Thầy bắt 06/09/2026 ở phiếu tuần 10 lớp 8: "bài 6 hình vẽ với lời giải vô lý nhé".
Bài đó bắt HS chứng minh $EFGH$ là hình chữ nhật, nhưng toạ độ $E,F,G,H$ đặt bằng mắt
nên tứ giác vẽ ra có góc $97{,}8^\circ$ và $82{,}2^\circ$ — HS nhìn hình thấy ngay nó
không vuông, mà vẫn phải chứng minh nó vuông.

`figure_gate` soi đề ↔ hình có nhắc đủ kí hiệu của nhau không, KHÔNG đọc toạ độ.
`test_tikz_goc_vuong` chỉ soi chỗ đã VẼ ô ký hiệu góc vuông. Lỗi này lọt cả hai vì
hình chẳng vẽ ô nào cả — bằng chứng nằm ở chính KẾT LUẬN của đề.

Quét lần đầu bắt thêm một ca nữa: tuần 15 lớp 8 Bài 14, điểm $H$ khai là chân đường
cao mà đặt lệch nên $AH$ không vuông góc $BC$, kéo theo $I$, $K$ sai và $AIHK$ ra
$126{,}9^\circ$. Cả hai đã sửa bằng toạ độ TÍNH.

Bài "TÌM ĐIỀU KIỆN để tứ giác là hình chữ nhật" được miễn: ở đó hình vẽ KHÔNG vuông
mới là đúng, vì góc vuông chính là thứ HS phải đi tìm.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pytest

SEEDS = Path(__file__).resolve().parents[1] / "inputs" / "seeds"

_NUM = r"-?\d+(?:\.\d+)?"
_COORD = re.compile(rf"\\coordinate\s*\((\w+)\)\s*at\s*\(\s*({_NUM})\s*,\s*({_NUM})\s*\)")
_NODE = re.compile(r"\\node\[[^\]]*\]\s*at\s*\(([^)]+)\)\s*\{\$([A-Z])(?:_\d)?\$\}")
_KET_LUAN = re.compile(
    r"[Cc]h[ứu]ng minh(?:\s+rằng)?\s+tứ giác\s+\$([A-Z]{4})\$\s+là\s+"
    r"(hình chữ nhật|hình bình hành)")
_MIEN = re.compile(r"điều kiện", re.IGNORECASE)

TOL = 3.0      # độ — nới tay, chỉ bắt hình đặt bằng mắt chứ không bắt làm tròn


def _diem(tikz: str) -> dict[str, tuple[float, float]]:
    """{nhãn: toạ độ} — giải qua bảng `\\coordinate (vA) at (x,y)` rồi mới đọc `\\node`.

    Không giải bảng này thì chỉ soi được 1/15 bài: gần như mọi hình trong kho đều đặt
    tên toạ độ chứ không viết số thẳng vào `\\node`.
    """
    ten = {n: (float(x), float(y)) for n, x, y in _COORD.findall(tikz)}
    ra: dict[str, tuple[float, float]] = {}
    for tro, nhan in _NODE.findall(tikz):
        tro = tro.strip()
        m = re.fullmatch(rf"\s*({_NUM})\s*,\s*({_NUM})\s*", tro)
        if m:
            ra[nhan] = (float(m.group(1)), float(m.group(2)))
        elif tro in ten:
            ra[nhan] = ten[tro]
    return ra


def _goc(p, q, r) -> float | None:
    u = (p[0] - q[0], p[1] - q[1])
    w = (r[0] - q[0], r[1] - q[1])
    lu, lw = math.hypot(*u), math.hypot(*w)
    if lu < 1e-9 or lw < 1e-9:
        return None
    return math.degrees(math.acos(max(-1.0, min(1.0, (u[0] * w[0] + u[1] * w[1]) / (lu * lw)))))


def _phieu_files():
    return sorted(SEEDS.rglob("phieu-*.json"))


@pytest.mark.parametrize("path", _phieu_files(), ids=lambda p: p.stem[:38])
def test_hinh_ve_dung_la_hinh_de_bat_chung_minh(path: Path):
    loi: list[str] = []
    d = json.loads(path.read_text(encoding="utf-8"))
    for st_ in d.get("stages", []):
        for b in st_.get("blocks", []):
            text = b.get("statement") or b.get("text") or ""
            if "tikzpicture" not in text or _MIEN.search(text):
                continue
            pts = _diem(text)
            for m in _KET_LUAN.finditer(text):
                ten, loai = m.group(1), m.group(2)
                if not all(c in pts for c in ten):
                    continue                    # hình không dán đủ 4 nhãn — không kết luận
                P = [pts[c] for c in ten]
                gs = [_goc(P[(i - 1) % 4], P[i], P[(i + 1) % 4]) for i in range(4)]
                if any(g is None for g in gs):
                    continue
                if loai == "hình chữ nhật":
                    lech, mo_ta = max(abs(g - 90) for g in gs), "lệch khỏi góc vuông"
                else:                           # hình bình hành: hai cặp góc đối bằng nhau
                    lech = max(abs(gs[0] - gs[2]), abs(gs[1] - gs[3]))
                    mo_ta = "hai góc đối lệch nhau"
                if lech > TOL:
                    loi.append(
                        f"{b.get('label')}: đề bắt chứng minh {ten} là {loai}, nhưng hình vẽ "
                        f"{mo_ta} {lech:.1f}° (bốn góc: "
                        + ", ".join(f"{g:.1f}°" for g in gs) + ") — toạ độ đặt bằng mắt.")
    assert not loi, path.name + "\n" + "\n".join(loi)
