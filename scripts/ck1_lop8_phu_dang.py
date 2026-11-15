"""Lớp vá CK1 lớp 8 — BỎ PHÂN THỨC, khung 6 bài theo đề thật (Thầy chốt 13/11/2026).

Dữ liệu: scripts/ck1_lop8_phu_dang.json = {mã đề: kết quả việc Gemini de8-ck1-<mã>} đã Claude soát.
Việc sinh: scripts/gemini/viec_de_ck1_lop8_bo_phan_thuc.py. Gọi từ de_on_tap_ck1_lop8.py và
de_chinh_thuc_ck1_lop8.py ngay trước khi sinh seed: ap_dung(DE, QUAN).

Khung: TN 8 × 0,25 · Bài 1 (1,5) 3 ý · Bài 2 (1,0) tìm x · Bài 3 (1,0) thống kê · Bài 4 (1,0) Thalès thực tế
(có hình) · Bài 5 (3,0) hình tứ giác · Bài 6 (0,5) VDC.
"""
import json
from pathlib import Path

DATA = Path(__file__).with_name("ck1_lop8_phu_dang.json")

# Tên nguồn Gemini có thể viết ⇒ (tên chuẩn in ở ma trận, quận/huyện cũ)
NGUON_MOI = {
    "Phòng GD\\&ĐT Ứng Hòa": "Ứng Hoà", "Phòng GD\\&ĐT Ứng Hoà": "Ứng Hoà",
    "Phòng GD\\&ĐT Thường Tín": "Thường Tín", "Phòng GD\\&ĐT Thanh Oai": "Thanh Oai",
    "Phòng GD\\&ĐT Thanh Trì": "Thanh Trì", "Quận Tây Hồ": "Tây Hồ",
    "THCS Mỹ Đình 1": "Nam Từ Liêm", "THCS Thăng Long": "Ba Đình", "THCS Tam Hiệp": "Thanh Trì",
    "THCS Hát Môn": "Phúc Thọ", "THCS Giảng Võ 2": "Ba Đình", "THCS Đông Mỹ": "Thanh Trì",
    "THCS Tân Triều": "Thanh Trì", "THCS Nguyễn Công Trứ": "Ba Đình", "THCS Nguyễn Trường Tộ": "Đống Đa",
    "THCS Phan Chu Trinh": "Ba Đình", "THCS Phan Đình Giót": "Thanh Xuân", "THCS Phúc Diễn": "Bắc Từ Liêm",
    "THCS Lê Quý Đôn": "Cầu Giấy", "THCS Nghĩa Tân": "Cầu Giấy", "THCS Giảng Võ": "Ba Đình",
    "THCS \\& THPT Lương Thế Vinh": "Cầu Giấy", "THCS Đa Tốn": "Gia Lâm",
}


def ap_dung(DE, QUAN):
    if not DATA.exists():
        return
    data = json.loads(DATA.read_text())
    for k, R in data.items():
        if k not in DE or k.startswith("_"):
            continue
        D = DE[k]
        cu = next((b for b in D["bai"] if b.get("hinh_da")), None)

        def ng(t):
            if t not in QUAN:
                assert t in NGUON_MOI, f"{k}: nguồn lạ {t!r} — thêm vào NGUON_MOI"
                QUAN[t] = NGUON_MOI[t]
            return t

        D["gioi_thieu"] = R["gioi_thieu"]
        D["cach_dung"] = R["cach_dung"]
        D["bay"] = [(x["vi_tri"], x["noi_dung"], x["loi"], x["cach"]) for x in R["bay"]]
        assert len(R["tn"]) == 8, k
        D["tn"] = [dict(cau=c["cau"], de=c["de"], options=c["options"], dap=c["dap"], giai=c["giai"], nd=c["nd"],
                        ch=c["ch"], muc=c["muc"], nguon=ng(c["nguon"]), level=1) for c in R["tn"]]
        bai = []
        for b in R["bai"]:
            nb = dict(label=b["label"], level=b["level"], statement=b["statement"], dap_an=b["dap_an"], note=b["note"],
                      mt=[(r["ma"], r["nd"], r["chu_de"], r["muc"], r["diem"], r["phut"], ng(r["nguon"])) for r in b["mt"]])
            if b["hinh"] == "giu_hinh_cu":
                nb["hinh_da"] = cu["hinh_da"]
                if cu.get("figure"):
                    nb["figure"] = cu["figure"]
                if b.get("bo_diem"):  # điểm của ý cũ không còn trong đề ⇒ vẽ lại không có điểm đó
                    import de_ck1_lop8_hinh as H
                    t = getattr(H, "get_tikz_" + k.replace("-", ""))(bo=tuple(b["bo_diem"]))
                    nb["hinh_da"] = t
                    if cu.get("figure"):
                        nb["figure"] = dict(cu["figure"], tikz=t)
            elif b["hinh"] == "moi":
                nb["figure"] = dict(tikz=b["tikz"], width=b.get("width", "0.42"))
                nb["hinh_da"] = b["tikz"]
            bai.append(nb)
        assert [b["label"] for b in bai] == [f"Bài {i}." for i in range(1, 7)], (k, [b["label"] for b in bai])
        tong = 0.25 * 8 + sum(r[4] for b in bai for r in b["mt"])
        assert abs(tong - 10) < 1e-9, (k, tong)
        D["bai"] = bai


TEN_BAI = [
    "Phép tính đa thức, HĐT, phân tích nhân tử (1,5đ)", "Tìm $x$ (1,0đ)", "Thống kê (1,0đ)",
    "Thalès, đường trung bình -- thực tế (1,0đ)", "Hình học tứ giác (3,0đ)", "VDC đại số (0,5đ)",
]


DANG_NGAN = {
    "D01": "đơn thức, đa thức", "D02": "cộng, trừ đa thức", "D03": "nhân, chia đa thức", "D04": "không phụ thuộc biến",
    "D05": "hằng đẳng thức", "D06": "rút gọn có HĐT", "D07": "tính nhanh bằng HĐT", "D08": "phân tích nhân tử",
    "D09": "tìm $x$: khai triển", "D10": "tìm $x$: tích bằng 0", "D11": "thực tế đại số", "D12": "góc tứ giác",
    "D13": "nhận biết tứ giác", "D14": "CM hình thang", "D15": "CM hình bình hành", "D16": "CM hình chữ nhật",
    "D17": "CM hình thoi, vuông", "D18": "tính độ dài, góc", "D19": "CM song song, vuông góc, trung điểm",
    "D20": "điều kiện, ý khó", "D21": "Thalès", "D22": "đường trung bình", "D23": "đường phân giác",
    "D24": "Thalès, đường TB thực tế", "D25": "tứ giác thực tế", "D26": "thu thập, phân loại dữ liệu",
    "D27": "đọc, lập bảng, biểu đồ", "D28": "phân tích số liệu, tỉ lệ \\%", "D29": "GTNN, GTLN",
    "D30": "đẳng thức có điều kiện",
}


def bang_moi(DE, tien_bo, theo_doi):
    """Bảng 'Bản đồ dạng bài' + 'Phiếu theo dõi' trong ma trận: dựng lại theo khung 6 bài (đề cũ viết cứng phân thức).
    Ô bảng = tên dạng ngắn theo mã dạng từng ý (mô tả dài làm bảng nhảy trang, bỏ tiêu đề lại một mình)."""
    if not DATA.exists():
        return tien_bo, theo_doi
    data = json.loads(DATA.read_text())
    ma = [k for k in DE if k in data]
    rows = [("Trắc nghiệm (2,0đ)", *[", ".join(dict.fromkeys(DANG_NGAN[c["dang"]] for c in data[k]["tn"])) for k in ma])]
    for j, ten in enumerate(TEN_BAI):
        o = []
        for k in ma:
            mt = data[k]["bai"][j]["mt"]
            o.append("; ".join((r["ma"].split(".")[-1] + ") " if len(mt) > 1 else "") + DANG_NGAN[r["dang"]] for r in mt))
        rows.append((ten, *o))
    td = ["Phần I -- Trắc nghiệm 8 câu (2,0đ)"] + [f"Bài {j + 1} -- {t}" for j, t in enumerate(TEN_BAI)] + [
        "\\textbf{Tổng điểm (10,0đ)}"]
    return rows, td


def ghi_bo_de():
    """Mã dạng từng ý (Gemini gắn khi dựng, Claude soát) ⇒ bo-de.json cho phu_dang_gate --khoi 8."""
    data = json.loads(DATA.read_text())
    bo = {}
    for k, R in data.items():
        if k.startswith("_"):
            continue
        bo[k.replace("-", "")] = [f"={c['dang']}" for c in R["tn"]] + [f"={r['dang']}" for b in R["bai"] for r in b["mt"]]
    p = Path(__file__).resolve().parents[1] / "inputs/refs/ngan-hang-sheet/lop-8/ck1/bo-de.json"
    p.write_text(json.dumps(bo, ensure_ascii=False, indent=1))
    print("ghi", p, {k: len(v) for k, v in bo.items()})


if __name__ == "__main__":
    ghi_bo_de()
