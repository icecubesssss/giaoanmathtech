"""Cổng cho `sync-drive` — dịch cây outputs/ sang cây Drive của Thầy (lop → tầng → chương)."""
from pathlib import Path

from src.exporters.drive_sync import bo_dau, ensure_dir, plan_target, sync_dir

OUT = Path("outputs")


def _mk(tmp_path: Path, rel: str, files=("ca-01-handout.pdf",)) -> tuple[Path, Path]:
    root = tmp_path / "outputs"
    d = root / rel
    d.mkdir(parents=True)
    for f in files:
        (d / f).write_bytes(b"%PDF-1.4 fake")
    return root, d


def test_bo_dau_giu_chu_d():
    assert bo_dau("Mở đầu về đường tròn") == "Mo dau ve duong tron"
    assert bo_dau("Độ dài cung tròn") == "Do dai cung tron"


def test_phieu_ra_dung_folder_ca(tmp_path):
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau-ve-duong-tron")
    t = plan_target(d, root, "Mở đầu về đường tròn")
    assert t.parts == ["lop9", "C", "Chuong 5", "Ca-01 - Mo dau ve duong tron"]


def test_thuyet_minh_ra_folder_so_la_ma(tmp_path):
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/thuyet-minh-lop-9c-chuong-05",
                  files=("thuyet-minh-lop-9c-chuong-05.pdf",))
    t = plan_target(d, root)
    assert t.parts == ["lop9", "C", "Chuong 5", "Thuyet-minh-chuong-V"]


def test_khong_suy_duoc_thi_bo_qua(tmp_path):
    root, d = _mk(tmp_path, "linh-tinh/khong-co-lop")
    assert plan_target(d, root) is None


def test_dung_lai_folder_da_co_du_lech_khoang_trang(tmp_path):
    """Thầy tự tạo 'Chuong5'; lệnh KHÔNG được đẻ thêm 'Chuong 5' bên cạnh."""
    drive = tmp_path / "drive"
    (drive / "Chuong5").mkdir(parents=True)
    got = ensure_dir(drive, "Chuong 5")
    assert got.name == "Chuong5"
    assert sorted(p.name for p in drive.iterdir()) == ["Chuong5"]


def test_chi_chep_bo_ten_co_tien_to_ca(tmp_path):
    """Build ghi cả 'handout.pdf' lẫn 'ca-01-handout.pdf' — Drive chỉ nhận bộ Ca."""
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau",
                  files=("handout.pdf", "ca-01-handout.pdf", "guide.pdf", "ca-01-guide.pdf"))
    drive = tmp_path / "drive"
    dest, files = sync_dir(d, root, "Mở đầu về đường tròn", root=drive)
    assert files == ["ca-01-guide.pdf", "ca-01-handout.pdf"]
    assert sorted(p.name for p in dest.iterdir()) == ["ca-01-guide.pdf", "ca-01-handout.pdf"]


def test_sync_tao_du_cay_thu_muc_va_ghi_de(tmp_path):
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau")
    drive = tmp_path / "drive"
    dest, _ = sync_dir(d, root, "Mở đầu về đường tròn", root=drive)
    assert dest == drive / "lop9" / "C" / "Chuong 5" / "Ca-01 - Mo dau ve duong tron"

    # chép lại lần hai: ghi đè, KHÔNG sinh bản trùng
    (d / "ca-01-handout.pdf").write_bytes(b"%PDF-1.4 moi hon")
    dest2, _ = sync_dir(d, root, "Mở đầu về đường tròn", root=drive)
    assert dest2 == dest
    assert len(list(dest.glob("*.pdf"))) == 1
    assert (dest / "ca-01-handout.pdf").read_bytes() == b"%PDF-1.4 moi hon"


def test_dry_run_khong_dung_vao_o_dia(tmp_path):
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau")
    drive = tmp_path / "drive"
    dest, files = sync_dir(d, root, "Mở đầu về đường tròn", dry_run=True, root=drive)
    assert files == ["ca-01-handout.pdf"]
    assert not drive.exists()
