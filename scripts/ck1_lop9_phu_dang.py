r"""PHỦ DẠNG cho 3 đề ÔN TẬP CK1 lớp 9 (lớp vá thứ ba, chạy SAU ck1_lop9_can_bo_sung.ap_dung).

Vì sao (12/11/2026): Thầy yêu cầu đề ôn phủ hết các dạng dễ có thể thi; cổng
`scripts/phu_dang_gate.py --khoi 9` (thống kê 41 đề thật) báo đề ôn thiếu: PT tích (on2, on3),
căn dạng số (on3), tính chất hai tiếp tuyến (on1, on2), cung/quạt/vành khuyên (cả 3).

Khung Thầy chốt 12/11/2026 (tổng vẫn 10):
  Bài III 2,5 = 6 ý: 4 ý × 0,5 + 2 ý một bước × 0,25 (PT tích, căn dạng số).
  Bài IV 3,5: IV.1 (1,0) = a) lượng giác 0,5 + b) cung/quạt/vành khuyên 0,5; IV.2 bài hình 2,5.

Nội dung do Gemini viết (việc `phu-dang-l9-on-N`, sinh bởi scripts/gemini/viec_phu_dang_on_ck1_lop9.py),
câu mới chép nguyên văn đề thật; Claude soát rồi lưu bản đã duyệt vào ck1_lop9_phu_dang.json cạnh file này.
"""
import json
import re
from pathlib import Path

DATA = Path(__file__).with_suffix(".json")

QUAN_PHU = {
    "Phòng GD\\&ĐT Quốc Oai (2024–2025)": "Quốc Oai",
    "THCS Phan Đình Giót (2024–2025)": "Thanh Xuân",
}

NHOM_BAN_DO_ON = [
    ("Căn thức \\& câu phụ (2,0đ)", ("Ia", "Ib", "Ic")),
    ("Toán thực tế lập hệ (1,5đ)", ("II",)),
    ("Giải PT, BPT, hệ, căn số (2,5đ)", ("IIIa", "IIIb", "IIIc", "IIId", "IIIe", "IIIf")),
    ("Lượng giác, cung -- quạt (1,0đ)", ("IVa", "IVa2")),
    ("Hình học đường tròn (2,5đ)", ("IVb1", "IVb2", "IVb3", "IVb4")),
    ("Câu cuối tối ưu / VDC (0,5đ)", ("V",)),
]

_DIEM = re.compile(r"\\textit\{\((\d+(?:,\d+)?)đ\)\}")
_DAU = re.compile(r"^\\textbf\{[^}]*\((\d+(?:,\d+)?)đ\)\}")


def _so(x):
    return float(x.replace(",", "."))


def kiem_y(k, a):
    """Tổng mốc chấm của một ý = điểm ghi ở đầu ý."""
    m = _DAU.match(a)
    assert m, f"{k}: ý không có nhãn điểm: {a[:60]}"
    tong = sum(_so(x) for x in _DIEM.findall(a))
    assert abs(tong - _so(m.group(1))) < 1e-9, f"{k}: {a[:40]} mốc {tong} ≠ {m.group(1)}"
    return _so(m.group(1))


def ap_dung_phu_dang(DE, QUAN):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    QUAN.update(QUAN_PHU)
    for k, kq in data.items():
        D = DE[k]
        b3, b4 = D["bai"][2], D["bai"][3]
        assert (b3["label"], b4["label"]) == ("Bài III.", "Bài IV."), k
        for b, moi, diem in ((b3, kq["bai3"], 2.5), (b4, kq["bai4"], 3.5)):
            b["statement"] = moi["statement"]
            b["dap_an"] = moi["dap_an"]
            b["mt"] = [(r["ma"], r["nd"], r["chu_de"], r["muc"], r["diem"], r["phut"], r["nguon"]) for r in moi["mt"]]
            b["note"] = moi["note"]
            assert abs(sum(kiem_y(k, a) for a in b["dap_an"]) - diem) < 1e-9, (k, b["label"])
            assert abs(sum(r[4] for r in b["mt"]) - diem) < 1e-9, (k, b["label"], "ma trận")
            assert len(b["mt"]) == len(b["dap_an"]), (k, b["label"], "số dòng ma trận ≠ số ý")
        if "hinh_da_bo" in kq:  # điểm/đoạn của ý đã bỏ (vd cát tuyến AMN ở on-1)
            for dong in kq["hinh_da_bo"]:
                assert dong in b4["hinh_da"], (k, dong)
                b4["hinh_da"] = b4["hinh_da"].replace(dong, "")
        if kq.get("hinh_canh"):  # 12/11: IV.1 thêm ý b ⇒ hình IV.1a đặt CẠNH chữ (hai minipage) cho tờ đề vừa 2 trang
            st = b4["statement"]
            dau, sau = st.split(" [[br]] 1) ", 1)
            ytren, yduoi = sau.split(" [[br]] 2) ", 1)
            diem1, ytren = ytren.split(" [[br]] ", 1)  # "1) (1,0 điểm)" lên cùng dòng tiêu đề Bài IV
            hinh = b4.pop("figure")
            b4["statement"] = (
                dau + " 1) " + diem1 + " \\par\\nopagebreak\\noindent"
                "\\begin{minipage}[t]{0.64\\linewidth}\\vspace{0pt}" + ytren + "\\end{minipage}\\hfill"
                "\\begin{minipage}[t]{0.33\\linewidth}\\vspace{0pt}\\centering"
                "\\adjustbox{max width=\\linewidth}{" + hinh["tikz"] + "}\\par{\\scriptsize " + hinh["caption"] + "}"
                "\\end{minipage}\\par\\smallskip 2) " + yduoi)
        D["bay"] = [x for x in D["bay"] if not x[0].startswith(("Bài III", "Bài IV"))] + [
            (x["vi_tri"], x["noi_dung"], x["loi"], x["cach"]) for x in kq["bay"]]
        tong = sum(r[4] for b in D["bai"] for r in b["mt"])
        assert abs(tong - 10) < 1e-9, f"{k}: tổng điểm {tong}"
