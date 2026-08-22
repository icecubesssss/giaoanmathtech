"""Test cho scripts/quick.py (tìm phiếu + đổi JSON→Markdown) và scripts/prune_outputs.py."""
from __future__ import annotations

import json

import pytest

from scripts import prune_outputs, quick


# ───────────────────────── tìm phiếu theo mẩu tên ─────────────────────────

def test_fold_bo_dau_tieng_viet():
    assert quick._fold("Hình Bình Hành") == "hinh binh hanh"
    assert quick._fold("[C]tuần04-đại-số") == "c tuan04 dai so"


def test_resolve_khop_dung_mot_phieu():
    p = quick.resolve("phieu-a-hinh-binh-hanh")
    assert p.name == "phieu-a-hinh-binh-hanh.json"
    assert p.exists()


def test_resolve_khong_dau_van_tim_ra():
    """Thầy gõ không dấu / gõ thiếu — vẫn phải ra đúng phiếu."""
    assert quick.resolve("tuan07 hinh binh hanh").name == "phieu-a-hinh-binh-hanh.json"


def test_resolve_mo_ho_thi_dung_lai_chu_khong_doan_bua():
    with pytest.raises(SystemExit):
        quick.resolve("phieu")


def test_resolve_khong_thay_thi_bao_loi():
    with pytest.raises(SystemExit):
        quick.resolve("khong-he-ton-tai-xyz")


def test_resolve_ghi_nho_phieu_vua_lam(tmp_path, monkeypatch):
    monkeypatch.setattr(quick, "LAST", tmp_path / "last.txt")
    p = quick.resolve("phieu-a-hinh-binh-hanh")
    assert quick.LAST.read_text().strip() == str(p)
    assert quick.resolve("") == p          # gõ `make b` trống = lặp lại phiếu đó


# ───────────────────────── JSON → Markdown ─────────────────────────

def test_text_doi_token_engine():
    assert quick._text("a [[br]] b") == "a\n\nb"
    assert "……" in quick._text("Điền: [[blank]]")


def test_text_giu_nguyen_cong_thuc_toan():
    """Công thức phải còn nguyên $...$ để preview render được."""
    out = quick._text(r"Góc $\widehat{A} = 60^\circ$ nên $x > 0$")
    assert r"$\widehat{A} = 60^\circ$" in out and "$x > 0$" in out


def test_text_bo_ma_latex_bo_cuc():
    raw = "\\vspace{4pt}\n\\centering\n\\adjustbox{max width=\\linewidth}{Nội dung}"
    out = quick._text(raw)
    for rac in ("vspace", "centering", "adjustbox"):
        assert rac not in out
    assert "Nội dung" in out


def test_text_thay_tikz_bang_cho_danh_dau():
    out = quick._text(r"Xem hình: \begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture} rồi làm")
    assert "tikzpicture" not in out and "🖼" in out


def test_text_bo_goi_wrap_hinh_canh_de():
    """[[wrap]]…[[/wrap]] gói LaTeX thô để thả hình cạnh đề — đọc thì chỉ cần biết 'có hình'."""
    out = quick._text(r"[[wrap]]\makebox[0pt][l]{\smash{\vtop{...}}}[[/wrap]] Cho $ABCD$…")
    assert "makebox" not in out and "[[wrap]]" not in out
    assert "🖼" in out and "Cho $ABCD$" in out


def test_dots_theo_be_rong_latex():
    assert len(quick._dots("2cm")) > len(quick._dots("1cm")) >= 3
    assert quick._dots("linh tinh")            # bề rộng lạ vẫn phải ra dấu chấm, không nổ


def test_text_doi_textbf_sang_markdown():
    assert "**Bài 1:**" in quick._text(r"\textbf{Bài 1:} nội dung")


def test_to_markdown_du_phan_chinh():
    p = quick.resolve("phieu-a-hinh-binh-hanh")
    md = quick.to_markdown(p)
    d = json.loads(p.read_text(encoding="utf-8"))
    assert md.startswith(f"# {d['title']}")
    assert d["slug"] in md
    assert "## Chặng 1" in md
    # lời giải phải gập lại, không lộ ngay trên màn hình
    assert "<details>" in md


def test_to_markdown_khong_con_token_engine():
    md = quick.to_markdown(quick.resolve("phieu-a-hinh-binh-hanh"))
    assert "[[br]]" not in md and "[[blank" not in md


# ───────────────────────── prune outputs ─────────────────────────

def test_expected_dirs_mirror_cay_seeds():
    exp = prune_outputs.expected_dirs()
    p = quick.resolve("phieu-a-hinh-binh-hanh")
    slug = json.loads(p.read_text(encoding="utf-8"))["slug"]
    duong_dan = prune_outputs.OUTPUTS / p.parent.relative_to(prune_outputs.SEEDS) / slug
    assert duong_dan in exp[slug]


def test_scan_khong_bao_nham_thu_muc_dung_cho():
    """Mọi thư mục bị gắn cờ phải THẬT SỰ không nằm trong danh sách hợp lệ."""
    exp = prune_outputs.expected_dirs()
    hop_le = {d for v in exp.values() for d in v}
    misplaced, gone = prune_outputs.scan()
    for d in misplaced + gone:
        assert d not in hop_le


def test_prune_xoa_duoc_khi_ca_cha_lan_con_deu_mo_coi(tmp_path, monkeypatch):
    """Cha lẫn con cùng mồ côi: phải xoá sâu-trước, không được nổ FileNotFoundError."""
    out = tmp_path / "outputs"
    cha = out / "tuan-cu"
    con = cha / "phieu-cu"
    con.mkdir(parents=True)
    (cha / "lac.pdf").write_bytes(b"%PDF")
    (con / "handout.pdf").write_bytes(b"%PDF")
    seeds = tmp_path / "inputs" / "seeds"
    seeds.mkdir(parents=True)

    monkeypatch.setattr(prune_outputs, "OUTPUTS", out)
    monkeypatch.setattr(prune_outputs, "SEEDS", seeds)
    monkeypatch.setattr(prune_outputs, "ROOT", tmp_path)

    assert prune_outputs.main(["--delete"]) == 0
    assert not cha.exists()


# ───── nhận thẳng đường dẫn (VS Code truyền ${file} = tab đang mở) ─────

def test_resolve_nhan_duong_dan_tuong_doi():
    """VS Code / make đều có thể đưa đường dẫn thẳng; phải ra tuyệt đối để in log không nổ."""
    p = quick.resolve("inputs/seeds/lop-8/hinh-hoc/lop-b/chuong-03-tu-giac/tuan07-hinh-binh-hanh/phieu-a-hinh-binh-hanh.json")
    assert p.is_absolute() and p.exists()
    p.relative_to(quick.ROOT)          # trước đây nổ ValueError ở đây


def test_resolve_bam_nham_file_khong_phai_json():
    with pytest.raises(SystemExit) as e:
        quick.resolve("AGENTS.md")
    assert "không phải file JSON" in str(e.value)


def test_bam_phim_tat_tren_thuyet_minh_thi_nhan_ra_la_spec():
    """Thầy bấm ⌘⇧B khi đang mở thuyet-minh.json → phải TỰ dựng PDF thuyết minh,
    KHÔNG được đá ra bắt gõ lệnh khác (lỗi thiết kế đã sửa 2026-08-07)."""
    p = quick.resolve("inputs/seeds/lop-8/hinh-hoc/lop-b/chuong-03-tu-giac/tuan07-hinh-binh-hanh/thuyet-minh.json")
    assert quick.loai_file(p) == "spec"


def test_phan_biet_dung_phieu_va_spec():
    phieu = quick.resolve("phieu-a-hinh-binh-hanh")
    assert quick.loai_file(phieu) == "phieu"
    assert quick.loai_file(quick.ROOT / "config" / "tier_spec.json") == ""


def test_resolve_bam_nham_json_cau_hinh():
    with pytest.raises(SystemExit) as e:
        quick.resolve("config/tier_spec.json")
    assert "không phải phiếu học tập" in str(e.value)
