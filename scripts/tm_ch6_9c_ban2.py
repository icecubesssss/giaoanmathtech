# Thuyết minh chương VI lớp 9C — BẢN 2 (16/11/2026), sinh từ bảng chọn câu.
# Nguồn: inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06/chon-cau.json (scripts/chon_cau_ch6_9c.py)
#        = tab "Chọn câu Ch.VI lớp 9C" (sheetId 9064, file Phân dạng lớp 9).
# Số câu từng dòng ĐẾM từ bảng chọn câu; chữ mô tả dạng viết tay ở D_TEXT.
# Chạy:  python3 scripts/tm_ch6_9c_ban2.py [--ghi]
import json, sys, collections

GOC = "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06/chon-cau.json"
OUT = "inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/thuyet-minh.json"

PHIEU = [
    ("1", "P1", "Phiếu 1 — Bài 19: Phương trình bậc hai một ẩn, biện luận số nghiệm theo $\\Delta$", 0),
    ("2", "P2", "Phiếu 2 — Bài 20: Định lí Viète, biểu thức đối xứng của hai nghiệm, tìm $m$ theo hệ thức đối xứng", 0),
    ("3", "P3", "Phiếu 3 — Bài 20 (tiếp): Biểu thức không đối xứng của hai nghiệm, tìm $m$ theo hệ thức không đối xứng", 0),
    ("4", "P4", "Phiếu 4 — Bài 21: Giải bài toán bằng cách lập phương trình", 0),
    ("5", "P5", "Phiếu 5 — Luyện tập chung, bài tập cuối chương VI và kiểm tra chương", 90),
]

# Câu NB kiến thức cũ (lớp C bắt buộc): (phiếu, mã bài gốc, số câu lấy từ phần NB tách của bài đó, chữ)
KTC = {
    "P1": ("sgk-6.8", "NB", 2, "Ôn lớp 8: khai triển hằng đẳng thức, chuyển vế, thu gọn để đưa phương trình về dạng $ax^2+bx+c=0$ rồi đọc $a$, $b$, $c$ (SGK 6.8)"),
    "P2": ("v10-thai-thinh-2025-III3", "TH", 1, "Ôn lớp 8: quy đồng mẫu hai phân thức $\\dfrac{1}{x_1+3}+\\dfrac{1}{x_2+3}$ trước khi thay tổng, tích"),
    # 17/11 Thầy: "ôn giải hpt làm chi" ⇒ đổi sang √(A²)=|A| (bước bỏ căn của đề Tự Lập), HS hay quên ở Mạch 4.
    "P3": ("v10-tu-lap-2026-III3", "TH", 1, "Ôn chương III (Toán 9 tập một): hằng đẳng thức $\\sqrt{A^2}=|A|$, bỏ dấu căn của $\\sqrt{(x-3)^2}$ khi $x<0$"),
    # P4, P5: bài gốc RIÊNG (Thầy 16/11 — không mượn chung bài gốc với dòng TH)
    "P4": ("gk2-cau-dien-2025-2", "NB", 1, "Ôn khử mẫu: nhân hai vế phương trình $\\dfrac{240}{x}-\\dfrac{240}{x+10}=2$ ($x>0$) với mẫu chung $x(x+10)$ — bước có ở mọi bài lập phương trình"),
    # 17/11 phiên P5 (Thầy bỏ hẳn C6-17): kiến thức cũ = hằng đẳng thức (a+b)², bước HS vướng khi tính x₁² + x₂²
    "P5": ("gk2-duc-giang-2025-III2", "TH", 1, "Ôn lớp 8: hằng đẳng thức $(a+b)^2=a^2+2ab+b^2$, khai triển $(x_1+x_2)^2$ trước khi viết $x_1^2+x_2^2$ theo tổng, tích"),
}

# Chữ mô tả từng dòng: khoá (phiếu, dạng, nhóm) với nhóm ∈ NB | TACH | TH | VD
D_TEXT = {
    ("P1", "C6-01", "NB"): "Nhận biết phương trình bậc hai (điều kiện $a\\ne 0$), đọc hệ số $a$, $b$, $c$; tính $\\Delta$ rồi kết luận số nghiệm không cần giải; $a$, $c$ trái dấu thì có hai nghiệm phân biệt",
    ("P1", "C6-02", "NB"): "Giải phương trình khuyết $c$ (đặt nhân tử chung) và khuyết $b$ (đưa về $x^2=k$ hoặc $(x+m)^2=k$)",
    ("P1", "C6-03", "NB"): "Nhẩm nghiệm khi $a+b+c=0$ hoặc $a-b+c=0$ — nêu như nhận xét khi kiểm nghiệm bằng máy tính, không thành dạng bài",
    ("P1", "C6-01", "TACH"): "Câu nhỏ tách từ đề giải phương trình: chỉ ra $a$, $b$, $c$; đưa về dạng chuẩn; $\\Delta<0$ thì kết luận gì",
    ("P1", "C6-04", "TACH"): "Câu nhỏ tách từ đề tìm $m$: hai nghiệm phân biệt / nghiệm kép / vô nghiệm ứng với điều kiện nào của $\\Delta$; viết $\\Delta$ theo $m$",
    ("P1", "C6-05", "TACH"): "Câu nhỏ tách từ đề chứng minh luôn có nghiệm: thay giá trị $m$; viết $\\Delta$ theo $m$; dấu của $ac$; $(m-2)^2\\ge 0$ cho kết luận gì",
    ("P1", "C6-06", "TACH"): "Câu nhỏ tách từ đề biết một nghiệm: thay $x=x_0$ vào phương trình để được phương trình ẩn $m$",
    ("P1", "C6-01", "TH"): "Giải phương trình bằng công thức nghiệm: hai nghiệm phân biệt, nghiệm kép, vô nghiệm, nghiệm chứa căn, hệ số chứa căn; phương trình phải biến đổi về dạng chuẩn",
    ("P1", "C6-04", "TH"): "Tìm $m$ để phương trình có hai nghiệm phân biệt, có nghiệm kép, vô nghiệm",
    ("P1", "C6-05", "TH"): "Chứng minh phương trình luôn có nghiệm (hai nghiệm phân biệt) với mọi $m$: $\\Delta$ là bình phương, hoặc $ac<0$",
    ("P1", "C6-06", "TH"): "Biết một nghiệm, tìm $m$ rồi giải phương trình tìm nghiệm còn lại (chưa dùng Viète)",

    ("P2", "C6-07", "NB"): "Kiểm điều kiện có nghiệm ($\\Delta\\ge 0$ hoặc $ac<0$) rồi viết tổng, tích hai nghiệm; Đ/S với phương trình vô nghiệm; trắc nghiệm $x_1^2+x_2^2$",
    ("P2", "C6-06", "NB"): "Biết một nghiệm, tìm nghiệm còn lại bằng tích hai nghiệm",
    ("P2", "C6-03", "NB"): "Ôn nhẩm nghiệm (BTVN): hệ số chứa căn",
    ("P2", "C6-10", "NB"): "Hai nghiệm trái dấu $\\Leftrightarrow ac<0$ (chỉ lấy ý trái dấu)",
    ("P2", "C6-07", "TACH"): "Câu nhỏ tách từ đề tính biểu thức: điều kiện có nghiệm; $x_1+x_2=?$, $x_1x_2=?$; viết biểu thức theo tổng, tích; hai nghiệm khác $0$",
    ("P2", "C6-08", "TACH"): "Câu nhỏ tách từ đề biết một nghiệm dạng căn: thay nghiệm tìm hệ số, tính $\\Delta$, tổng hai nghiệm bằng bao nhiêu",
    ("P2", "C6-11", "TACH"): "Câu nhỏ tách từ đề tìm $m$: thay $m$ để giải; điều kiện có nghiệm theo $m$; viết hệ thức theo tổng, tích",
    ("P2", "C6-07", "TH"): "Tính biểu thức đối xứng: $x_1^2+x_2^2$, $x_1^2+x_2^2-kx_1x_2$, $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$, $x_1^3+x_2^3$, $\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$, $\\dfrac{1}{x_1+a}+\\dfrac{1}{x_2+a}$, biểu thức phải khai triển",
    ("P2", "C6-08", "TH"): "Biết một nghiệm dạng căn, tính biểu thức đối xứng (đề minh họa của Sở)",
    ("P2", "C6-11", "TH"): "Tìm $m$ theo hệ thức đối xứng, hạ thành các bước có câu hỏi định hướng: điều kiện $\\Delta$, viết hệ thức theo tổng-tích, giải, đối chiếu",
    ("P2", "C6-11", "VD"): "Tìm $m$ để hai nghiệm thỏa hệ thức đối xứng (chỉ đề, học sinh tự giải)",

    ("P3", "C6-13", "TACH"): "Câu nhỏ tách từ đề hạ bậc: $x_1$ là nghiệm nên $x_1^2=?$; $x_1^3=?$; biểu thức còn lại theo tổng, tích",
    ("P3", "C6-14", "TACH"): "Câu nhỏ tách từ đề chứa $|x|$, căn: dấu hai nghiệm ($ac$, tổng); biểu thức dưới căn là bình phương của gì",
    ("P3", "C6-15", "TACH"): "Câu nhỏ tách từ đề hệ thức bậc nhất: kết hợp với $x_1+x_2$ thành hệ; thay $x_1$, $x_2$ vào tích để tìm $m$; đối chiếu $\\Delta$",
    ("P3", "C6-16", "TACH"): "Câu nhỏ tách từ đề tìm $m$ bằng hạ bậc: thay $x_1^2$ theo $x_1$; rút gọn về tổng, tích; điều kiện có nghiệm",
    ("P3", "C6-13", "TH"): "Hạ bậc: tính biểu thức không đối xứng bậc hai, bậc ba (bài VD tách lẻ thành các bước)",
    ("P3", "C6-14", "TH"): "Biểu thức chứa $|x|$, căn của một nghiệm: xét dấu hai nghiệm rồi biến đổi",
    ("P3", "C6-15", "TH"): "Tìm $m$ theo hệ thức bậc nhất không đối xứng $ax_1+bx_2=c$, $x_1=kx_2$",
    ("P3", "C6-16", "TH"): "Tìm $m$ theo hệ thức không đối xứng bằng hạ bậc",
    ("P3", "C6-13", "VD"): "Hạ bậc rồi quy đồng (đề chính thức Hà Nội 2026) — chỉ đề",
    ("P3", "C6-14", "VD"): "Biểu thức chứa căn và trị tuyệt đối của một nghiệm (ví dụ mẫu)",
    ("P3", "C6-15", "VD"): "Tìm $m$ theo hệ thức bậc nhất (nghiệm này gấp $k$ lần nghiệm kia) — chỉ đề",
    ("P3", "C6-16", "VD"): "Tìm $m$ theo hệ thức không đối xứng (đề chính thức Hà Nội 2025) — chỉ đề",
    ("P3", "C6-07", "TACH"): "Câu nhỏ tách từ đề ôn Phiếu 2: viết biểu thức đối xứng theo tổng, tích để được phương trình ẩn $m$",
    ("P3", "C6-07", "TH"): "Ôn Phiếu 2: phương trình ẩn $m$ có chứa biểu thức đối xứng của hai nghiệm",
    ("P3", "C6-08", "TACH"): "Câu nhỏ tách từ đề biết một nghiệm dạng căn (ôn Phiếu 2): tổng hai nghiệm, tích hai nghiệm",
    ("P3", "C6-08", "TH"): "Ôn Phiếu 2: biết một nghiệm dạng căn, tính tổng lập phương, bình phương hiệu",
    ("P3", "C6-11", "TACH"): "Câu nhỏ tách từ đề tìm tham số (BTVN): điều kiện có nghiệm, hai nghiệm khác $0$; dùng tích $x_1x_2$ để đưa hệ thức về tổng, tích",
    ("P3", "C6-11", "TH"): "Tìm tham số theo hệ thức có $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$ hoặc hệ thức lệch đưa được về tổng nhờ tích $x_1x_2$ (đề thi, BTVN)",

    ("P4", "C6-18", "TACH"): "Câu nhỏ tách từ đề lập phương trình: nhắc công thức (diện tích hình chữ nhật, số ngày $=\\dfrac{\\text{khối lượng}}{\\text{năng suất}}$, chia đều, $t=\\dfrac{s}{v}$, phần việc trong 1 giờ $=\\dfrac{1}{t}$); biểu diễn thời gian, số ngày, khối lượng mỗi xe theo ẩn; đổi phút ra giờ",
    ("P4", "C6-18", "TH"): "Giải bài toán bằng cách lập phương trình bậc hai: chuyển động, năng suất, hình học, phần trăm, mô hình cho sẵn công thức",
    ("P4", "C6-18", "VD"): "Bài toán hai giai đoạn (dừng giữa đường rồi tăng tốc; làm được một phần rồi tăng năng suất), làm chung – làm riêng — chỉ đề",

    ("P5", "C6-01", "NB"): "Khởi động: nhẩm nghiệm, giải phương trình bằng công thức nghiệm",
    ("P5", "C6-07", "NB"): "Trắc nghiệm đọc ngược Viète: phương trình có hai nghiệm cho trước",
    ("P5", "C6-18", "NB"): "Biểu thị số tiền sau một, hai kì gửi lãi kép theo lãi suất $x$ (ví dụ SGK); trắc nghiệm một bước của bài lập phương trình: biểu diễn đại lượng theo ẩn, phương trình lập được; hình chữ nhật biết chu vi và diện tích",
    ("P5", "C6-04", "TACH"): "Câu nhỏ tách từ đề: điều kiện hai nghiệm phân biệt, tổng-tích khi thay $m$",
    ("P5", "C6-11", "TACH"): "Câu nhỏ tách từ đề tìm $m$: điều kiện có nghiệm, viết hệ thức theo tổng, tích",

    ("P5", "C6-18", "TACH"): "Câu nhỏ tách từ đề lập phương trình: biểu diễn đại lượng theo ẩn, câu quan hệ",
    ("P5", "C6-07", "TACH"): "Câu nhỏ tách từ đề tính biểu thức: tổng, tích; đưa hệ thức về tổng, tích",
    ("P5", "C6-08", "TACH"): "Câu nhỏ tách từ đề biết một nghiệm dạng căn: tổng, tích hai nghiệm",
    ("P5", "C6-01", "TACH"): "Câu nhỏ tách từ đề: đưa về dạng chuẩn, nhận ra bình phương",
    ("P5", "C6-04", "TH"): "Điều kiện hai nghiệm phân biệt rồi tính biểu thức đối xứng khi cho $m$",
    ("P5", "C6-18", "TH"): "Giải bài toán bằng cách lập phương trình (năng suất, chuyển động)",

    ("P5", "C6-05", "TACH"): "Câu nhỏ tách từ đề chứng minh luôn có hai nghiệm phân biệt: đọc $a$, $b$, $c$; viết $\\Delta$ theo $m$",
    ("P5", "C6-06", "TACH"): "Câu nhỏ tách từ đề biết một nghiệm: đưa phương trình về dạng chuẩn; tổng hai nghiệm theo Viète",
    ("P5", "C6-05", "TH"): "Chứng minh phương trình luôn có hai nghiệm phân biệt với mọi $m$ (viết $\\Delta$ thành tổng bình phương cộng số dương)",
    ("P5", "C6-06", "TH"): "Biết một nghiệm dạng căn, dùng Viète tìm nghiệm còn lại",
    ("P5", "C6-07", "TH"): "Biểu thức của hai nghiệm, hệ thức ẩn $m$ đưa về tổng, tích",
    ("P5", "C6-08", "TH"): "Biết một nghiệm dạng căn, tính tổng nghịch đảo bình phương",
    ("P5", "C6-01", "TH"): "Biến đổi về dạng chuẩn rồi giải",
    ("P5", "C6-11", "VD"): "Tìm $m$ theo hệ thức đối xứng (cấu trúc Bài III.2b đề thi) — chỉ đề",
}
LAM_THEM_TEXT = {
    "gk2-ba-dinh-2025-I": "Bài làm thêm (không tính giờ, GV tùy chọn): tìm $m$ để parabol qua một điểm rồi tìm tọa độ giao điểm với đường thẳng",
    "tl-ptb2-23-tr8": "Bài làm thêm (không tính giờ, GV tùy chọn): đường thẳng cắt parabol tại hai điểm phân biệt $\\Leftrightarrow$ phương trình hoành độ có $\\Delta>0$",
    "v10-quoc-oai-l2-2024-3.2": "Bài làm thêm (không tính giờ, GV tùy chọn): giao điểm khi $m=3$; hai giao điểm khác phía trục tung và hệ thức hạ bậc",
}
LYTHUYET_ROW = {("P1", "C6-01", "NB"), ("P1", "C6-02", "NB"), ("P1", "C6-03", "NB"),
                ("P2", "C6-07", "NB"), ("P2", "C6-10", "NB"),
                ("P3", "C6-13", "TH"), ("P4", "C6-18", "TH")}


def _dem(rs, vai, f):
    return sum(r[f] for r in rs if r["vai"] == vai)


def dung_phieu(rows, pk):
    rs = [r for r in rows if r["phieu"] == pk and r["vai"] in ("Ví dụ", "Trên lớp", "BTVN")]
    ktc_ma, ktc_muc, ktc_n, ktc_txt = KTC[pk]
    out = []
    order = []
    nhom = collections.OrderedDict()

    def add(key, r, f_vidu, f_lop):
        nhom.setdefault(key, []).append((r, f_vidu, f_lop))

    for r in rs:
        if r["muc"] == "NB":
            add((r["dang"], "NB"), r, "so_nb", "so_nb")
        else:
            if r["so_nb"] and r["vai"] != "Ví dụ":
                add((r["dang"], "TACH"), r, None, "so_nb")
            add((r["dang"], r["muc"]), r, "so_y", "so_y")
    # NB trước, rồi TH, rồi VD (đúng thứ tự dạy)
    rank = {"NB": 0, "TACH": 1, "TH": 2, "VD": 3}
    keys = sorted(nhom, key=lambda k: (rank[k[1]], list(nhom).index(k)))
    da_tru_ktc = False
    for key in keys:
        dang, g = key
        items = nhom[key]
        vidu = sum(r[fv] for r, fv, fl in items if r["vai"] == "Ví dụ" and fv)
        lop = sum(r[fl] for r, fv, fl in items if r["vai"] == "Trên lớp")
        btvn = sum(r[fl] for r, fv, fl in items if r["vai"] == "BTVN")
        refs = []
        for r, _, _ in items:
            ref = r["ma"] if r["y"] in ("", "(cả bài)") or "-" not in r["y"] and len(r["y"]) > 1 else r["ma"]
            if ref not in refs:
                refs.append(ref)
        # trừ câu NB kiến thức cũ khỏi nhóm chứa bài gốc của nó
        if not da_tru_ktc and any(r["ma"] == ktc_ma for r, _, _ in items) and \
                ((ktc_muc == "NB" and g == "NB") or (ktc_muc != "NB" and g == "TACH")):
            ktc_r = [r for r, _, _ in items if r["ma"] == ktc_ma][0]
            if ktc_r["vai"] == "Trên lớp":
                lop -= ktc_n
            else:
                btvn -= ktc_n
            da_tru_ktc = ("Trên lớp" if ktc_r["vai"] == "Trên lớp" else "BTVN")
            if ktc_muc == "NB" and ktc_r["ma"] in refs and ktc_r["so_nb"] == ktc_n:
                refs.remove(ktc_r["ma"])   # mọi câu của bài đã chuyển sang dòng kiến thức cũ
        if g == "NB":
            band, loai, dec = "NB", "NB lẻ LT", "none"
        elif g == "TACH":
            band, loai, dec = "NB", "NB tách TH", "none"
        elif g == "TH":
            ls = [r["loai"] for r, _, _ in items]
            loai = "TH tách VD" if "TH tách VD" in ls else ("TH ghép bài" if "TH ghép bài" in ls else "TH lẻ LT")
            band, dec = "TH", ("th2nb" if loai != "TH lẻ LT" else "none")
        else:
            band, loai, dec = "VD", "VD lẻ", "vd"
        if vidu + lop + btvn == 0:
            continue
        row = {
            "dang": D_TEXT[(pk, dang, g)] + f" \\textit{{({dang})}}",
            "band": band, "loai": loai, "decompose": dec,
            "vidu": vidu, "onclass": lop, "btvn": btvn,
            "lythuyet": 1 if (pk, dang, g) in LYTHUYET_ROW else 0,
            "source_refs": refs,
            "gian_giao": "dien-khuyet" if (g == "NB" and vidu > 0) else "",
        }
        out.append(row)
    # dòng NB kiến thức cũ, đặt đầu phiếu
    ktc = {"dang": ktc_txt, "band": "NB", "loai": "NB kiến thức cũ", "decompose": "none",
           "vidu": 0, "onclass": ktc_n if da_tru_ktc == "Trên lớp" else 0,
           "btvn": ktc_n if da_tru_ktc == "BTVN" else 0, "lythuyet": 0,
           "source_refs": [ktc_ma], "gian_giao": ""}
    assert da_tru_ktc, f"{pk}: không tìm thấy bài gốc kiến thức cũ {ktc_ma}"
    out.insert(0, ktc)
    # bài làm thêm (không tính giờ)
    for r in rows:
        if r["phieu"] == pk and r["vai"] == "Làm thêm":
            out.append({"dang": LAM_THEM_TEXT[r["ma"]] + f" \\textit{{({r['dang']})}}",
                        "band": r["muc"], "loai": r["loai"],
                        "decompose": "vd" if r["muc"] == "VD" else "none",
                        "vidu": 0, "onclass": 0, "btvn": 0, "lythuyet": 0,
                        "source_refs": [r["ma"]], "gian_giao": ""})
    for i, r in enumerate(out, 1):
        r["stt"] = i
    return out


THOILUONG = [
    "Buổi 1 (Bài 19. Phương trình bậc hai một ẩn — biện luận số nghiệm theo $\\Delta$): 1 ca = 180 phút.",
    "Buổi 2 (Bài 20. Định lí Viète — biểu thức đối xứng, tìm $m$ theo hệ thức đối xứng): 1 ca = 180 phút.",
    "Buổi 3 (Bài 20, tiếp — biểu thức không đối xứng, tìm $m$ theo hệ thức không đối xứng): 1 ca = 180 phút.",
    "Buổi 4 (Bài 21. Giải bài toán bằng cách lập phương trình): 1 ca = 180 phút.",
    "Buổi 5 (Luyện tập chung, bài tập cuối chương VI): 1 ca = 180 phút (90 phút kiểm tra chương; phần còn lại là ví dụ chữa mẫu, luyện tập và nghỉ giữa giờ).",
    "\\textbf{Tổng 5 ca = 900 phút} (PPCT SGV chương VI: 16 tiết, trừ 3 tiết Bài 18 Hàm số $y=ax^2$ không dạy lớp C, còn 13 tiết; trong đó 90 phút kiểm tra chương).",
]

KIEN_THUC_NEN = [
    "\\textbf{Bảy hằng đẳng thức đáng nhớ} (Lớp 8): khai triển để đưa phương trình về dạng $ax^2+bx+c=0$; biến đổi $x_1^2+x_2^2=(x_1+x_2)^2-2x_1x_2$, $x_1^3+x_2^3=(x_1+x_2)^3-3x_1x_2(x_1+x_2)$.",
    "\\textbf{Phân tích đa thức thành nhân tử} (Lớp 8): giải phương trình khuyết $c$, phân tích mẫu thức khi tìm điều kiện xác định.",
    "\\textbf{Quy đồng mẫu thức và điều kiện xác định của phân thức} (Lớp 8): biểu thức $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$, $\\dfrac{x_1}{x_2}+\\dfrac{x_2}{x_1}$; khử mẫu khi lập phương trình (Phiếu 4).",
    "\\textbf{Giải hệ hai phương trình bậc nhất hai ẩn} (Chương I lớp 9): tìm $x_1$, $x_2$ từ hệ thức bậc nhất và tổng hai nghiệm (Phiếu 3).",
    "\\textbf{Giải bài toán bằng cách lập hệ phương trình} (Chương I lớp 9): học sinh đã luyện chọn ẩn, biểu diễn đại lượng, lập phương trình — Phiếu 4 chỉ nhắc công thức $s=vt$, năng suất $=\\dfrac{\\text{khối lượng}}{\\text{thời gian}}$.",
    "\\textbf{Căn thức bậc hai, $\\sqrt{A^2}=|A|$} (Chương III lớp 9): biểu thức chứa căn, trị tuyệt đối của một nghiệm (Phiếu 3).",
]

LYTHUYET = [
    "\\textbf{Mục tiêu chương}: giải được phương trình bậc hai (dạng khuyết, công thức nghiệm); biện luận số nghiệm theo tham số $m$; dùng định lí Viète tính biểu thức của hai nghiệm và tìm $m$ theo hệ thức của hai nghiệm; giải bài toán bằng cách lập phương trình bậc hai.",
    "\\textbf{Chuẩn đầu ra}: làm được trọn Bài III đề kiểm tra học kì II và đề tuyển sinh vào 10 phần phương trình bậc hai: giải phương trình, chứng minh luôn có nghiệm, tính biểu thức đối xứng, tìm $m$ theo hệ thức đối xứng, bài toán lập phương trình.",
    "\\textbf{Tham số $m$ có trong chương} (Thầy chốt 16/11/2026): biện luận theo $\\Delta$ ở Phiếu 1, Viète có $m$ ở Phiếu 2, 3. Năm dạng tần suất cao nhất trong đề thật (40 đề Vào 10, 30 đề CK2, 25 đề GK2): lập phương trình 70\\% / 80\\% / 96\\%; tìm $m$ theo hệ thức đối xứng 8\\% / 40\\% / 36\\%; giải phương trình 3\\% / 30\\% / 48\\%; biểu thức đối xứng 28\\% / 27\\% / 12\\%; chứng minh luôn có nghiệm 13\\% / 17\\% / 12\\%.",
    "\\textbf{Hình thức câu hỏi} (luật 16/11/2026): câu NB là câu nhỏ gắn với đề (nhắc công thức, điều kiện, bước làm) dạng trắc nghiệm, Đúng/Sai, trả lời ngắn; câu TH là bài gọn có câu hỏi gợi ý bước; câu VD chỉ có đề. Điền khuyết chỉ dùng trong Ví dụ. Bài đã tách chỉ tính giờ các câu nhỏ.",
    "\\textbf{Phiếu 3 có bài làm thêm} (Thầy chốt 16/11/2026): parabol và đường thẳng (C6-28) — ghi trong thuyết minh nhưng không tính giờ, GV dạy khi còn giờ.",
    "\\textbf{Không dạy ở lớp C}: hàm số $y=ax^2$ và đồ thị (Bài 18), tìm hai số biết tổng và tích, hệ thức không phụ thuộc $m$, phương trình chứa ẩn ở mẫu quy về bậc hai (C6-17, Thầy bỏ 17/11/2026), giải phương trình bằng máy tính cầm tay, công thức nghiệm thu gọn $\\Delta'$ (Thầy bỏ 16/11/2026), các dạng VDC.",
]

VIDU = [
    "Buổi 1: $3x^2+7x-1=0$ đủ ba bước $a$, $b$, $c$ $\\to$ $\\Delta$ $\\to$ công thức nghiệm (SGK Ví dụ 5); $x^2-6x+9=0$ nghiệm kép và $2x^2+3x+5=0$ vô nghiệm; $x^2-2(m+3)x+m^2-5=0$ biện luận theo $\\Delta$; $x^2+ax-1=0$ luôn có hai nghiệm phân biệt.",
    "Buổi 2: kiểm $\\Delta$ rồi viết tổng, tích (SGK Ví dụ 1 Bài 20); $x_1^2+x_2^2$, $\\dfrac{1}{x_1}+\\dfrac{1}{x_2}$, $x_1^3+x_2^3$, $(x_1-x_2)^2$; biết nghiệm $1-\\sqrt2$ tính tổng bình phương; $x^2+(1-m)x-m=0$ tìm $m$ để $x_1^2+x_2^2=5$.",
    "Buổi 3: hạ bậc $4x_1^2=2x_1+1$; $x_1+2026=(x_1-1)^2$ nên căn bằng $|x_1-1|$; $3x_1+2x_2=1$ kết hợp tổng hai nghiệm; thay $x_1^2=2mx_1+4m+5$ để tìm $m$.",
    "Buổi 4: sân bóng hình chữ nhật, tàu du lịch xuôi ngược có nghỉ, đội xe bớt xe (SGK Bài 21), xưởng in sách, hai ô tô; xe dừng giữa đường rồi tăng tốc; làm chung – làm riêng.",
    "Buổi 5: chữa mẫu Bài III.3 (chứng minh hai nghiệm phân biệt, tính $x_1^2+x_2^2-6x_1x_2$) và Bài III.2b (tìm $m$ để $x_1^2+x_2^2=x_1x_2+46$); một bài năng suất, một bài chuyển động và bài toán lãi kép gửi tiết kiệm (SGK Bài 21 HĐ1--HĐ3).",
]

DANG_VD = [
    "Bài III.2b — tìm $m$ để hai nghiệm thỏa hệ thức đối xứng (CK2 40\\%, GK2 36\\%): Phiếu 2 trên lớp Hoài Đức, Lômônôxốp; BTVN Mai Dịch, Thanh Oai.",
    "Bài III.3 — hạ bậc, biểu thức không đối xứng (đề chính thức Hà Nội 2026, 2025): Phiếu 3.",
    "Bài III.1 — lập phương trình hai giai đoạn, làm chung (thi thử Tự Lập 2026, Quốc Oai; BTVN Thọ Lộc, Đống Đa -- Khương Thượng): Phiếu 4.",
    "Ôn tổng hợp Bài III.2b — tìm $m$ theo hệ thức đối xứng (Hà Đông; BTVN Nghĩa Tân, Tây Mỗ 3): Phiếu 5.",
]

LOISAI = [
    "Chưa đưa phương trình về dạng $ax^2+bx+c=0$ đã đọc hệ số, tính $\\Delta$.",
    "Sai dấu $-4ac$ khi $c$ âm.",
    "Khuyết $b$: quên nghiệm âm khi khai căn; khuyết $c$: chia hai vế cho $x$ làm mất nghiệm $x=0$.",
    "Chứng minh luôn có nghiệm: $\\Delta=(m-2)^2\\ge 0$ mà kết luận có hai nghiệm phân biệt.",
    "Viết tổng, tích hai nghiệm khi chưa kiểm tra phương trình có nghiệm; nhầm dấu tổng $x_1+x_2=\\dfrac{b}{a}$.",
    "Tính tổng nghịch đảo mà quên hai nghiệm khác $0$; tìm $m$ xong không đối chiếu điều kiện $\\Delta$.",
    "Hạ bậc sai dấu khi chuyển vế: từ $x_1^2-3x_1+1=0$ viết $x_1^2=-3x_1+1$.",
    "Bài toán lập phương trình: không đổi phút ra giờ; quên điều kiện của ẩn, không loại nghiệm âm.",
]

KIENTHUC_NB = [
    "Phương trình bậc hai một ẩn: $ax^2+bx+c=0$ với $a\\ne 0$ (SGK Toán 9 tập hai, Bài 19).",
    "Công thức nghiệm: $\\Delta=b^2-4ac$; $\\Delta>0$ thì $x_{1,2}=\\dfrac{-b\\pm\\sqrt{\\Delta}}{2a}$; $\\Delta=0$ thì $x_1=x_2=-\\dfrac{b}{2a}$; $\\Delta<0$ thì vô nghiệm.",
    "Nếu $a$ và $c$ trái dấu thì phương trình có hai nghiệm phân biệt.",
    "Định lí Viète: nếu $x_1$, $x_2$ là hai nghiệm thì $x_1+x_2=-\\dfrac{b}{a}$, $x_1x_2=\\dfrac{c}{a}$ (SGK Bài 20); $a+b+c=0$ thì $x_1=1$, $x_2=\\dfrac{c}{a}$; $a-b+c=0$ thì $x_1=-1$, $x_2=-\\dfrac{c}{a}$.",
    "Giải bài toán bằng cách lập phương trình: lập phương trình (chọn ẩn, điều kiện, biểu diễn đại lượng), giải phương trình, trả lời (SGK Bài 21, ba bước).",
]


def dung():
    rows = json.load(open(GOC))
    spec = {
        "slug": "thuyet-minh-lop-9c-chuong-06-pt-bac-hai",
        "title": "Chương VI. Phương trình bậc hai một ẩn (Bài 19 – Bài 21 SGK) — bản 2",
        "grade": "lop-9", "subject": "dai-so", "tier": "C", "tuan": "22-26",
        "chuong": "chuong-06",
        "luat_16_11": True,   # luật hình thức câu 16/11/2026 (AGENTS.md khối đầu file)
        "thoiluong": THOILUONG, "kien_thuc_nen": KIEN_THUC_NEN, "lythuyet": LYTHUYET,
        "vidu": VIDU, "dang_vd": DANG_VD, "loisai": LOISAI, "kienthuc_nb": KIENTHUC_NB,
        "phieu": [],
    }
    for code, pk, title, kt in PHIEU:
        p = {"code": code, "title": title, "rows": dung_phieu(rows, pk)}
        if code == "1":       # P1 không VD (Thầy chốt 16/11): 32 NB + 12 TH ⇒ soi 40-60-0
            p = {"code": code, "title": title, "khuon": "khong_vd", "rows": p["rows"]}
        if code == "3":       # Thầy 17/11: "K sao nhé" — tab không có câu SGK ở dạng không đối xứng
            p["mien_sgk"] = ("Thầy đồng ý 17/11/2026: tab phân dạng không có câu SGK nào ở các dạng biểu thức "
                             "không đối xứng (C6-13…C6-16).")
        if kt:
            p["kiem_tra_phut"] = kt
        spec["phieu"].append(p)
    return spec


if __name__ == "__main__":
    spec = dung()
    for p in spec["phieu"]:
        tong = collections.Counter()
        for r in p["rows"]:
            for f in ("vidu", "onclass", "btvn"):
                tong[(r["band"], f)] += r[f]
        print(p["code"], len(p["rows"]), "dòng ·",
              " ".join(f"{b}:{tong[(b,'vidu')]}/{tong[(b,'onclass')]}/{tong[(b,'btvn')]}" for b in ("NB", "TH", "VD")))
    if "--ghi" in sys.argv:
        json.dump(spec, open(OUT, "w"), ensure_ascii=False, indent=2)
        print("Đã ghi", OUT)
