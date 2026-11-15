r"""BỔ SUNG CÂU CĂN THỨC DẠNG SỐ cho 6 đề CK1 lớp 9 (3 đề ôn + 3 đề chính thức).

Vì sao (11/11/2026, góp ý cô Vũ Minh Anh, Thầy đồng ý): HS lớp C học ở nhiều trường mà đề
CK1 của trường hỏi cả căn thức DẠNG SỐ (tính giá trị biểu thức số, giải phương trình chứa căn)
ngoài bài rút gọn biểu thức chứa $x$. Ví dụ: Phòng VH-XH Ba Đình, THCS Nguyễn Du,
THCS-THPT Tạ Quang Bửu (2025–2026). Bộ đề cũ chỉ có Bài I rút gọn ⇒ thêm 2 ý vào Bài III.

Khung điểm mới (tổng vẫn 10):
  Bài I 2,0 (giữ) · Bài II lập hệ 2,0 → 1,5 (như câu lập hệ của đề vào 10 Hà Nội:
  2 dòng lập phương trình 0,5 → 0,25) · Bài III 2,0 → 2,5 (thêm ý 4, ý 5, mỗi ý 0,5)
  · Bài IV 3,5 · Bài V 0,5.

Mọi câu chép NGUYÊN VĂN từ đề thật (đã soi ảnh PDF ở inputs/refs/de-thi/lop-9/cuoi-ki-1 và
ảnh Thầy gửi); đáp số kiểm bằng SymPy.
"""
import re

# Quận/phường của các trường nguồn mới (dùng cho cổng rải nguồn kiem_nguon).
QUAN_MOI = {
    "Phòng VH-XH Ba Đình (2025–2026)": "Ba Đình",
    "THCS Nguyễn Du (2025–2026)": "Hoàn Kiếm",
    "THCS-THPT Tạ Quang Bửu (2025–2026)": "Hai Bà Trưng",
    "THCS Ngọc Thụy (2025–2026)": "Long Biên",
    "THCS Đức Giang (2025–2026)": "Long Biên",
    "THCS Hoàng Liệt (2025–2026)": "Hoàng Mai",
    "THCS Lý Sơn (2025–2026)": "Long Biên",
    "THCS Ngô Sĩ Liên (2025–2026)": "Hoàn Kiếm",
}

# Mỗi ý: (đề bài, các bước lời giải, (nội dung ma trận, mức, phút, nguồn))
CAN = {
    # ───────────── ĐỀ ÔN 1: dễ nhất ─────────────
    "on-1": [
        (
            "Rút gọn biểu thức: $\\dfrac{2}{3}\\sqrt{9} - \\dfrac{3}{2}\\sqrt{(-6)^2} + 7$.",
            [
                ("$\\dfrac{2}{3}\\sqrt{9} - \\dfrac{3}{2}\\sqrt{(-6)^2} + 7 = \\dfrac{2}{3} \\cdot 3 - \\dfrac{3}{2} \\cdot |-6| + 7$", 0.25),
                ("$= 2 - 9 + 7 = 0$."),
                ("Vậy giá trị của biểu thức bằng $0$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: khai phương, $\\sqrt{A^2} = |A|$", "NB", 4, "THCS Lý Sơn (2025–2026)"),
        ),
        (
            "Giải phương trình: $\\sqrt{x-2} + 3\\sqrt{9x-18} = 10$.",
            [
                ("Điều kiện xác định: $x \\ge 2$."),
                ("Ta có $\\sqrt{9x-18} = \\sqrt{9(x-2)} = 3\\sqrt{x-2}$."),
                ("Phương trình trở thành: $\\sqrt{x-2} + 9\\sqrt{x-2} = 10$", 0.25),
                ("$10\\sqrt{x-2} = 10$"),
                ("$\\sqrt{x-2} = 1$"),
                ("$x - 2 = 1$"),
                ("$x = 3$ (thoả mãn ĐKXĐ)."),
                ("Vậy phương trình có nghiệm $x = 3$.", 0.25),
            ],
            ("Giải phương trình chứa căn: đưa thừa số ra ngoài dấu căn", "TH", 6, "THCS Ngọc Thụy (2025–2026)"),
        ),
    ],
    # ───────────── ĐỀ ÔN 2 ─────────────
    "on-2": [
        (
            "Tính: $\\sqrt{98} - \\sqrt{32} + \\sqrt{2}\\left(\\sqrt{8} - 3\\right)$.",
            [
                ("$\\sqrt{98} - \\sqrt{32} + \\sqrt{2}\\left(\\sqrt{8} - 3\\right) = 7\\sqrt{2} - 4\\sqrt{2} + \\sqrt{16} - 3\\sqrt{2}$", 0.25),
                ("$= 7\\sqrt{2} - 4\\sqrt{2} + 4 - 3\\sqrt{2}$"),
                ("$= 4$."),
                ("Vậy giá trị của biểu thức bằng $4$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: đưa thừa số ra ngoài dấu căn", "TH", 5, "THCS Hoàng Liệt (2025–2026)"),
        ),
        (
            "Giải phương trình: $\\sqrt{x-1} + \\dfrac{3}{2}\\sqrt{4x-4} - \\sqrt{\\dfrac{18x-18}{2}} = 5$.",
            [
                ("Điều kiện xác định: $x \\ge 1$."),
                ("Ta có $\\sqrt{4x-4} = 2\\sqrt{x-1}$ và $\\sqrt{\\dfrac{18x-18}{2}} = \\sqrt{9(x-1)} = 3\\sqrt{x-1}$."),
                ("Phương trình trở thành: $\\sqrt{x-1} + 3\\sqrt{x-1} - 3\\sqrt{x-1} = 5$", 0.25),
                ("$\\sqrt{x-1} = 5$"),
                ("$x - 1 = 25$"),
                ("$x = 26$ (thoả mãn ĐKXĐ)."),
                ("Vậy phương trình có nghiệm $x = 26$.", 0.25),
            ],
            ("Giải phương trình chứa căn: đưa thừa số ra ngoài dấu căn", "TH", 6, "THCS-THPT Tạ Quang Bửu (2025–2026)"),
        ),
    ],
    # ───────────── ĐỀ ÔN 3 ─────────────
    "on-3": [
        (
            "Tính giá trị biểu thức: $M = \\dfrac{1}{\\sqrt{2}-1} - \\sqrt{8} + \\sqrt{(2-\\sqrt{2})^2} - 3$.",
            [
                ("Ta có: $\\dfrac{1}{\\sqrt{2}-1} = \\dfrac{\\sqrt{2}+1}{(\\sqrt{2}-1)(\\sqrt{2}+1)} = \\sqrt{2}+1$."),
                ("Vì $2 > \\sqrt{2}$ nên $\\sqrt{(2-\\sqrt{2})^2} = |2-\\sqrt{2}| = 2-\\sqrt{2}$.", 0.25),
                ("$M = \\sqrt{2} + 1 - 2\\sqrt{2} + 2 - \\sqrt{2} - 3$"),
                ("$M = -2\\sqrt{2}$."),
                ("Vậy $M = -2\\sqrt{2}$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: trục căn thức ở mẫu, $\\sqrt{A^2} = |A|$", "TH", 5, "Phòng VH-XH Ba Đình (2025–2026)"),
        ),
        (
            "Giải phương trình: $2\\sqrt{x^2-6x+9} - 1 = 5$.",
            [
                ("Ta có $\\sqrt{x^2-6x+9} = \\sqrt{(x-3)^2} = |x-3|$."),
                ("Phương trình trở thành: $2|x-3| - 1 = 5$"),
                ("$|x-3| = 3$", 0.25),
                ("Trường hợp 1: $x - 3 = 3$, suy ra $x = 6$."),
                ("Trường hợp 2: $x - 3 = -3$, suy ra $x = 0$."),
                ("Vậy phương trình có hai nghiệm $x = 6$ và $x = 0$.", 0.25),
            ],
            ("Giải phương trình chứa căn dạng $\\sqrt{A^2} = |A|$", "TH", 6, "THCS Đức Giang (2025–2026)"),
        ),
    ],
    # ───────────── ĐỀ CHÍNH THỨC 1 ─────────────
    "ct1": [
        (
            "Tính giá trị biểu thức: $A = \\left(8\\sqrt{3} - 2\\sqrt{75} + \\sqrt{27}\\right) \\cdot \\sqrt{3}$.",
            [
                ("$A = \\left(8\\sqrt{3} - 2 \\cdot 5\\sqrt{3} + 3\\sqrt{3}\\right) \\cdot \\sqrt{3}$", 0.25),
                ("$A = \\sqrt{3} \\cdot \\sqrt{3}$"),
                ("$A = 3$."),
                ("Vậy $A = 3$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: đưa thừa số ra ngoài dấu căn", "NB", 4, "THCS Ngô Sĩ Liên (2025–2026)"),
        ),
        (
            "Tính: $5 - 2\\sqrt{27} + \\sqrt{(\\sqrt{3}-2)^2}$.",
            [
                ("Ta có $\\sqrt{27} = 3\\sqrt{3}$."),
                ("Vì $2 > \\sqrt{3}$ nên $\\sqrt{(\\sqrt{3}-2)^2} = |\\sqrt{3}-2| = 2 - \\sqrt{3}$.", 0.25),
                ("$5 - 2\\sqrt{27} + \\sqrt{(\\sqrt{3}-2)^2} = 5 - 6\\sqrt{3} + 2 - \\sqrt{3}$"),
                ("$= 7 - 7\\sqrt{3}$."),
                ("Vậy giá trị của biểu thức bằng $7 - 7\\sqrt{3}$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: $\\sqrt{A^2} = |A|$, xét dấu $A$", "TH", 5, "THCS Ngọc Thụy (2025–2026)"),
        ),
    ],
    # ───────────── ĐỀ CHÍNH THỨC 2 ─────────────
    "ct2": [
        (
            "Rút gọn biểu thức: $\\sqrt{(1-\\sqrt{3})^2} - \\sqrt{48} + \\dfrac{9}{\\sqrt{3}}$.",
            [
                ("Vì $\\sqrt{3} > 1$ nên $\\sqrt{(1-\\sqrt{3})^2} = |1-\\sqrt{3}| = \\sqrt{3} - 1$.", 0.25),
                ("Ta có $\\sqrt{48} = 4\\sqrt{3}$ và $\\dfrac{9}{\\sqrt{3}} = \\dfrac{9\\sqrt{3}}{3} = 3\\sqrt{3}$."),
                ("$\\sqrt{(1-\\sqrt{3})^2} - \\sqrt{48} + \\dfrac{9}{\\sqrt{3}} = \\sqrt{3} - 1 - 4\\sqrt{3} + 3\\sqrt{3}$"),
                ("$= -1$."),
                ("Vậy giá trị của biểu thức bằng $-1$.", 0.25),
            ],
            ("Rút gọn biểu thức số: $\\sqrt{A^2} = |A|$, trục căn thức ở mẫu", "TH", 5, "THCS-THPT Tạ Quang Bửu (2025–2026)"),
        ),
        (
            "Tìm $x$ biết: $\\sqrt{x^2-6x+9} = 2x - 1$.",
            [
                ("Ta có $\\sqrt{x^2-6x+9} = \\sqrt{(x-3)^2} = |x-3|$."),
                ("Phương trình trở thành: $|x-3| = 2x - 1$. Điều kiện: $2x - 1 \\ge 0$, suy ra $x \\ge \\dfrac{1}{2}$.", 0.25),
                ("Trường hợp 1: $x - 3 = 2x - 1$, suy ra $x = -2$ (không thoả mãn $x \\ge \\dfrac{1}{2}$, loại)."),
                ("Trường hợp 2: $x - 3 = -(2x - 1)$"),
                ("$3x = 4$"),
                ("$x = \\dfrac{4}{3}$ (thoả mãn $x \\ge \\dfrac{1}{2}$)."),
                ("Vậy $x = \\dfrac{4}{3}$.", 0.25),
            ],
            ("Giải phương trình chứa căn $\\sqrt{A^2} = B$ (có bước loại nghiệm)", "VD", 7, "THCS Nguyễn Du (2025–2026)"),
        ),
    ],
    # ───────────── ĐỀ CHÍNH THỨC 3 ─────────────
    "ct3": [
        (
            "Tính giá trị biểu thức: $A = \\left(\\sqrt{8} - 2\\sqrt{18} + 3\\sqrt{50}\\right)\\sqrt{2}$.",
            [
                ("$A = \\left(2\\sqrt{2} - 2 \\cdot 3\\sqrt{2} + 3 \\cdot 5\\sqrt{2}\\right)\\sqrt{2}$", 0.25),
                ("$A = 11\\sqrt{2} \\cdot \\sqrt{2}$"),
                ("$A = 22$."),
                ("Vậy $A = 22$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: đưa thừa số ra ngoài dấu căn", "NB", 4, "THCS Nguyễn Du (2025–2026)"),
        ),
        (
            "Tính giá trị biểu thức: $B = \\dfrac{14}{3+\\sqrt{2}} + \\sqrt{(1-2\\sqrt{2})^2}$.",
            [
                ("Ta có: $\\dfrac{14}{3+\\sqrt{2}} = \\dfrac{14(3-\\sqrt{2})}{(3+\\sqrt{2})(3-\\sqrt{2})} = \\dfrac{14(3-\\sqrt{2})}{7} = 6 - 2\\sqrt{2}$."),
                ("Vì $2\\sqrt{2} = \\sqrt{8} > 1$ nên $\\sqrt{(1-2\\sqrt{2})^2} = |1-2\\sqrt{2}| = 2\\sqrt{2} - 1$.", 0.25),
                ("$B = 6 - 2\\sqrt{2} + 2\\sqrt{2} - 1$"),
                ("$B = 5$."),
                ("Vậy $B = 5$.", 0.25),
            ],
            ("Tính giá trị biểu thức số: trục căn thức ở mẫu, $\\sqrt{A^2} = |A|$", "TH", 6, "THCS Ngô Sĩ Liên (2025–2026)"),
        ),
    ],
}

# Bẫy thêm vào bảng "bẫy tử huyệt" của từng đề
BAY = {
    "on-1": ("Bài III.5", "Căn có thừa số chung $\\sqrt{9x-18}$", "Giải ra $x = 3$ nhưng không ghi ĐKXĐ $x \\ge 2$.", "Đặt ĐKXĐ trước, đưa $\\sqrt{9x-18} = 3\\sqrt{x-2}$ rồi gom các căn giống nhau."),
    "on-2": ("Bài III.5", "Căn chứa phân thức $\\sqrt{\\dfrac{18x-18}{2}}$", "Tách sai $\\sqrt{\\dfrac{18x-18}{2}} = \\dfrac{\\sqrt{18x-18}}{2}$.", "Rút gọn trong căn trước: $\\dfrac{18x-18}{2} = 9(x-1)$."),
    "on-3": ("Bài III.5", "$\\sqrt{(x-3)^2} = |x-3|$", "Viết $\\sqrt{(x-3)^2} = x-3$, mất nghiệm $x = 0$.", "Luôn viết trị tuyệt đối rồi xét hai trường hợp."),
    "ct1": ("Bài III.5", "Khai căn $\\sqrt{(\\sqrt{3}-2)^2}$", "Viết $\\sqrt{(\\sqrt{3}-2)^2} = \\sqrt{3}-2$ (sai dấu).", "So sánh $2 > \\sqrt{3}$ để phá trị tuyệt đối: kết quả $2 - \\sqrt{3}$."),
    "ct2": ("Bài III.5", "$|x-3| = 2x-1$ có điều kiện vế phải", "Nhận cả nghiệm $x = -2$ (vế phải âm).", "Đặt điều kiện $2x - 1 \\ge 0$ trước, đối chiếu từng nghiệm."),
    "ct3": ("Bài III.5", "Khai căn $\\sqrt{(1-2\\sqrt{2})^2}$", "Viết $1 - 2\\sqrt{2}$ (là số âm).", "So sánh $2\\sqrt{2} = \\sqrt{8} > 1$, kết quả $2\\sqrt{2} - 1$."),
}

# Đề mà Bài III sau khi thêm 2 ý tràn 1 dòng khỏi trang 1 (soi PDF 11/11/2026)
GOP_DONG_12 = {"on-2", "ct3"}

_DIEM = re.compile(r"\\textit\{\((\d+(?:,\d+)?)đ\)\}")


def tong_diem(chuoi):
    return sum(float(m.replace(",", ".")) for m in _DIEM.findall(chuoi))


def ap_dung(DE, y, BR):
    """Sửa tại chỗ từng đề trong DE (dict khoá on-1…/ct1…)."""
    for k, D in DE.items():
        bai = D["bai"]
        b2, b3 = bai[1], bai[2]
        assert b2["label"] == "Bài II." and b3["label"] == "Bài III.", k

        # Bài II: 2,0 → 1,5 (hai dòng lập phương trình (1), (2): 0,5 → 0,25)
        assert "\\textbf{(2,0 điểm)}" in b2["statement"], k
        b2["statement"] = b2["statement"].replace("\\textbf{(2,0 điểm)}", "\\textbf{(1,5 điểm)}", 1)
        moi = []
        for a in b2["dap_an"]:
            a2, n = re.subn(r"(\((?:1|2)\)\s*\\hfill \\textit\{)\(0,5đ\)\}", r"\1(0,25đ)}", a)
            assert n == 2, f"{k}: Bài II cần đúng 2 dòng lập phương trình 0,5đ, thấy {n}"
            moi.append(a2)
        assert abs(sum(tong_diem(a) for a in moi) - 1.5) < 1e-9, k
        b2["dap_an"] = moi
        (r,) = b2["mt"]
        b2["mt"] = [(r[0], r[1], r[2], r[3], 1.5, r[5] - 3, r[6])]

        # Bài III: 2,0 → 2,5 = 5 ý × 0,5. Ý 1 (hệ), ý 2 (phương trình) 0,75 → 0,5:
        # bỏ mốc 0,25 ở GIỮA, giữ mốc bước biến đổi đầu và mốc kết luận.
        assert [r[4] for r in b3["mt"]] == [0.75, 0.75, 0.5], (k, b3["mt"])
        for j in (0, 1):
            a = b3["dap_an"][j]
            moc = list(re.finditer(r" \\hfill \\textit\{\(0,25đ\)\}", a))
            assert len(moc) == 3 and "(0,75đ)}" in a, (k, j, len(moc))
            m = moc[1]
            a = a[: m.start()] + a[m.end():]
            b3["dap_an"][j] = a.replace("(0,75đ)}", "(0,5đ)}", 1)
            assert abs(tong_diem(b3["dap_an"][j]) - 0.5) < 1e-9, (k, j)
            r = b3["mt"][j]
            b3["mt"][j] = (r[0], r[1], r[2], r[3], 0.5, r[5], r[6])
        assert b3["statement"].count("\\textbf{(0,75 điểm)}") == 2, k
        b3["statement"] = b3["statement"].replace("\\textbf{(0,75 điểm)}", "\\textbf{(0,5 điểm)}")
        assert "\\textbf{(2,0 điểm)}" in b3["statement"], k
        st = b3["statement"].replace("\\textbf{(2,0 điểm)}", "\\textbf{(2,5 điểm)}", 1)
        for i, (de_bai, buoc, (nd, muc, phut, nguon)) in enumerate(CAN[k], 4):
            st += BR + f"{i}) \\textbf{{(0,5 điểm)}} " + de_bai
            loi_giai = y(f"{i})", 0.5, buoc)
            assert abs(tong_diem(loi_giai) - 0.5) < 1e-9, (k, i)
            b3["dap_an"].append(loi_giai)
            b3["mt"].append((f"III{'abcde'[i - 1]}", nd, "ĐS III", muc, 0.5, phut, nguon))
        if k in GOP_DONG_12:  # tờ đề tràn 1 dòng sang trang 2 ⇒ ý 1 và ý 2 chung một dòng
            assert st.count(BR + "2) \\textbf") == 1, k
            st = st.replace(BR + "2) \\textbf", " \\qquad 2) \\textbf", 1)
        b3["statement"] = st
        b3["note"] = b3["note"] + " Ý 4, 5 (căn thức dạng số): luôn viết $\\sqrt{A^2} = |A|$ rồi xét dấu $A$; phương trình chứa căn phải có ĐKXĐ hoặc điều kiện vế phải."
        D["bay"].append(BAY[k])

        tong = sum(r[4] for b in bai for r in b["mt"])
        assert abs(tong - 10) < 1e-9, f"{k}: tổng điểm {tong}"


NHOM_BAN_DO = [
    ("Căn thức \\& câu phụ (2,0đ)", ("Ia", "Ib", "Ic")),
    ("Toán thực tế lập hệ (1,5đ)", ("II",)),
    ("Giải PT, BPT, hệ, căn số (2,5đ)", ("IIIa", "IIIb", "IIIc", "IIId", "IIIe")),
    ("Lượng giác thực tế (0,5đ)", ("IVa",)),
    ("Hình học đường tròn (3,0đ)", ("IVb1", "IVb2", "IVb3")),
    ("Câu cuối tối ưu / VDC (0,5đ)", ("V",)),
]


def ban_do_dang(DE, nhom=None):
    """Bảng 'bản đồ dạng bài qua 3 đề' sinh thẳng từ ma trận ⇒ không bao giờ lệch đề.
    nhom: bảng nhóm mã ý (mặc định NHOM_BAN_DO; đề ôn sau phủ dạng dùng NHOM_BAN_DO_ON)."""
    rows = []
    for ten, ma in nhom or NHOM_BAN_DO:
        o = []
        for D in DE.values():
            mt = {r[0]: r[1] for b in D["bai"] for r in b["mt"]}
            o.append("; ".join((f"{c}: " if len(ma) > 1 else "") + mt[c] for c in ma if c in mt))  # đề ôn 3: hình chỉ 3 ý
        rows.append((ten, *o))
    return rows
