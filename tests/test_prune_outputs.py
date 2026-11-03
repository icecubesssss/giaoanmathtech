"""prune_outputs: giữ thư mục có NGUON.txt, báo bản in lạc ngoài outputs/ (03/11/2026)."""
from scripts import prune_outputs as po


def test_giu_thu_muc_co_nguon_va_bao_file_lac(tmp_path, monkeypatch):
    root = tmp_path
    (root / "inputs" / "seeds").mkdir(parents=True)
    out = root / "outputs"
    giu = out / "lop-8" / "de-thang-09"
    giu.mkdir(parents=True)
    (giu / "De-HS.pdf").write_bytes(b"%PDF")
    (giu / "NGUON.txt").write_text("dựng ngoài engine", encoding="utf-8")
    mo_coi = out / "demo"
    mo_coi.mkdir()
    (mo_coi / "x.pdf").write_bytes(b"%PDF")
    (root / "De_lac.pdf").write_bytes(b"%PDF")
    (root / "inputs" / "nguon.pdf").write_bytes(b"%PDF")      # nguồn đề: không tính
    monkeypatch.setattr(po, "ROOT", root)
    monkeypatch.setattr(po, "SEEDS", root / "inputs" / "seeds")
    monkeypatch.setattr(po, "OUTPUTS", out)
    _, gone = po.scan()
    assert gone == [mo_coi]                                   # thư mục có NGUON.txt không bị xoá
    assert po.scan_stray() == [root / "De_lac.pdf"]
