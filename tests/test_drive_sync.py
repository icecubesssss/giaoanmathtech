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


def test_ten_pdf_moi_lay_so_ca_tu_slug_phieu_n(tmp_path):
    """PDF tên Toan9C-… không còn tiền tố ca-NN: số ca lấy từ slug 'phieu-3-' để thư mục
    Drive vẫn là 'Ca-03 - …' (không đẻ thư mục song sinh, giữ thứ tự buổi)."""
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-3-do-dai-cung",
                  files=("Toan9C-Do-dai-cung-Phieu-HS.pdf",))
    t = plan_target(d, root, "Độ dài cung tròn")
    assert t.parts[-1] == "Ca-03 - Do dai cung tron"


def test_ban_2_cua_chuong_ra_folder_rieng(tmp_path):
    """Bản 2 của chương V (6 buổi) không được đổ chung 'Chuong 5' với bản cũ 7 buổi."""
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/phieu-1-do-dai-cung",
                  files=("Toan9C-Do-dai-cung-Phieu-HS.pdf",))
    t = plan_target(d, root, "Độ dài cung tròn")
    assert t.parts == ["lop9", "C", "Chuong 5 - Ban 2", "Ca-01 - Do dai cung tron"]
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron-ban-2/kiem-tra-chuong/de-x",
                  files=("x.pdf",))
    assert plan_target(d, root).parts[:3] == ["lop9", "C", "Chuong 5 - Ban 2"]


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


def test_chep_ca_ban_ten_tu_mo_ta(tmp_path):
    """Từ 06/09/2026 bản in mang tên tự mô tả, KHÔNG còn tiền tố 'ca-' — vẫn phải chép.

    Cổng cũ lọc `ca-*.pdf` (thời build ghi song song 'handout.pdf' và 'ca-01-handout.pdf');
    giữ nguyên bộ lọc đó thì đồng bộ Drive bỏ sót sạch bản in tên mới.
    """
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/phieu-a-mo-dau",
                  files=("Toan9C-Tuan05-Mo-dau-Phieu-HS.pdf",
                         "Toan9C-Tuan05-Mo-dau-Dap-an-GV.pdf"))
    drive = tmp_path / "drive"
    dest, files = sync_dir(d, root, "Mở đầu về đường tròn", root=drive)
    assert files == ["Toan9C-Tuan05-Mo-dau-Dap-an-GV.pdf",
                     "Toan9C-Tuan05-Mo-dau-Phieu-HS.pdf"]
    assert sorted(p.name for p in dest.iterdir()) == files


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


def test_kiem_tra_chuong_ra_mot_folder_rieng_va_bo_slide(tmp_path):
    """Luật cứng 26/09/2026: đề + đáp án kiểm tra chương vào chung 'Kiem-tra-chuong-V', không chép Slide."""
    files = ("Toan9C-De-kiem-tra-chuong-v-Phieu-HS.pdf", "Toan9C-De-kiem-tra-chuong-v-Slide.pdf")
    root, d = _mk(tmp_path, "lop-9/hinh-hoc/lop-c/chuong-05-duong-tron/kiem-tra-chuong/de-kiem-tra-chuong-v-lop-9c", files)
    t = plan_target(d, root, "Đề kiểm tra Chương V")
    assert t.parts == ["lop9", "C", "Chuong 5", "Kiem-tra-chuong-V"]
    dest, chep = sync_dir(d, root, "Đề kiểm tra Chương V", root=tmp_path / "drive")
    assert chep == ["Toan9C-De-kiem-tra-chuong-v-Phieu-HS.pdf"]
