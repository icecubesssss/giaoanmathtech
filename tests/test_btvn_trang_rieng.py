"""BTVN tách trang riêng có hộp tiêu đề (Thầy chốt 26/10/2026 — "để đôi lúc tôi có thể in riêng")."""
import json
from pathlib import Path

from src.compiler.jinja_renderer import render_guide, render_handout
from src.schema.lesson_package import LessonPackage

_SEED = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-3-hai-tiep-tuyen-cat-nhau-chung-minh-ao-vuong-goc-bc.json")


def _lesson(bat: bool) -> LessonPackage:
    d = json.loads(_SEED.read_text(encoding="utf-8"))
    d["btvn_trang_rieng"] = bat
    d["btvn_phieu_rieng"] = False
    return LessonPackage.model_validate(d)


def test_bat_co_btvn_sang_trang_moi_co_hop_tieu_de():
    for render in (render_handout, render_guide):
        tex = render(_lesson(True))
        dau = tex.index("BÀI TẬP VỀ NHÀ}")
        truoc = tex[:dau]
        assert "\\clearpage" in truoc[truoc.rindex("\\end{stage}"):]   # sang trang ngay sau chặng 5
        assert "Họ và tên" in tex[dau - 1500:dau + 600]                 # hộp có Họ và tên/Lớp
        assert "\\worksheetsection{BÀI TẬP VỀ NHÀ}" not in tex


def test_tat_co_giu_nguyen_ban_cu():
    tex = render_handout(_lesson(False))
    assert "\\worksheetsection{BÀI TẬP VỀ NHÀ}" in tex
    assert "\\clearpage" not in tex
