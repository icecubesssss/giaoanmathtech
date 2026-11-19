# Thuyết minh chương X lớp 9C (19/11/2026, làm lại theo quy trình mới) — sinh từ bảng chọn câu.
# Nguồn số: inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/chon-cau.json (scripts/chon_cau_ch10_9c.py).
# Nguồn chữ (luật giao Gemini 16/11): storage/gemini/xong/tm-ch10-9c-chu.json
#   (scripts/gemini/viec_chon_cau_ch10_9c.py) — Claude chỉ viết khung số, thời lượng, giàn giáo.
# Chạy:  python3 scripts/tm_ch10_9c.py [--ghi]
import json, re, sys, collections
from pathlib import Path

GOC = "inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10/chon-cau.json"
OUT = "inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/thuyet-minh.json"
CHU = Path("storage/gemini/xong/tm-ch10-9c-chu.json")
PHIEU = {
    "P1": {"code": "1", "title": "Phiếu 1 — Bài 31, Bài 32: Hình trụ, hình nón, hình cầu",
           "dich": "Bài 5 đề kiểm tra cuối học kì II THCS Đoàn Thị Điểm 2025--2026 (khuôn Câu IV.1 đề minh họa "
                   "của Sở: ly hình trụ đường kính 5 cm, nước cao 10 cm, thả 5 viên bi làm nước dâng tới miệng ly; "
                   "ý b hỏi bán kính mỗi viên bi)"},
    "P2": {"code": "2", "title": "Phiếu 2 — Luyện tập chung, Bài tập cuối chương X (45 phút) $+$ Kiểm tra chương X (45 phút)",
           "kiem_tra_phut": 45,
           "mien_sgk": "Buổi luyện tập 45 phút trước kiểm tra chương bám đề thi (đích Câu IV.1 đề Sở 2026); "
                       "SGK có ở ví dụ mẫu (Luyện tập chung, Ví dụ 1) và bài tập về nhà (10.12).",
           "dich": "Câu IV.1 đề chính thức vào 10 Hà Nội năm 2026 (xô nước hình trụ: ý a diện tích xung quanh, "
                   "ý b đếm số xô ít nhất để đổ đầy bể 150 lít, làm tròn LÊN)"},
}
# dòng TM mở thẻ lý thuyết: một dòng cho sáu công thức (C10-02), một dòng cho yếu tố các khối (C10-01)
LYTHUYET_ROW = {"C10-02|NB"}
# giàn giáo bắt buộc mỗi phiếu (check_scaffold_rails): dòng NB có ví dụ ⇒ điền khuyết; dòng vẽ phác + ghi số đo ⇒ vẽ hình
VE_HINH_ROW = {"C10-07|TACH", "C10-08|NB"}
RANK = {"KTC": 0, "NB": 1, "TACH": 2, "TH": 3, "VD": 4}

THOILUONG = [
    "Buổi 1 (tuần 32 — Bài 31 $+$ Bài 32 gộp: hình trụ, hình nón, hình cầu): 1 ca $=$ 90 phút "
    "(giáo viên giảng 25 phút $+$ luyện tập trên lớp 55 phút $+$ giải lao 10 phút; bài tập về nhà 40 phút).",
    "Buổi 2 (tuần 33 — Luyện tập chung $+$ Bài tập cuối chương X): 1 ca $=$ 90 phút "
    "(45 phút luyện tập $+$ 45 phút kiểm tra chương X).",
    "\\textbf{Tổng 2 ca $=$ 180 phút} trên PPCT SGV 7 tiết $\\Rightarrow$ chương dạy nén (Thầy chốt 19/11/2026: "
    "làm lại theo quy trình phân dạng mới, giữ hai buổi).",
    "\\textbf{Dạng dạy} (tổ trưởng tick 19/11/2026 trên tab phân dạng): C10-01 đến C10-09. "
    "Không dạy C10-10, C10-11, C10-12 (nâng cao).",
    "Ba dạng C10-03 (hình nón cần định lí Pythagore), C10-04 (tính ngược), C10-08 (lật ngược chai) chỉ có "
    "$0$--$7\\%$ đề thi nên dạy trong khung, không làm đích hay câu vận dụng.",
    "Cột bài tập về nhà cố ý dôi so với quỹ 40 phút (thà thừa còn hơn thiếu), giáo viên linh hoạt cắt bớt lúc giao bài.",
]


def _chu():
    if not CHU.exists():
        return {}
    d = json.loads(CHU.read_text())
    return sua_chu(d.get("ket_qua") or d.get("structured_output") or d.get("json") or d)


# Claude soát đầu ra Gemini: (trường, chuỗi cũ, chuỗi mới) — assert để biết khi Gemini viết lại khác đi.
SUA = [
    ("dang_vd", "", ""),   # giữ chỗ — xem sua_chu: bỏ gạch lật ngược chai (C10-08 hạ TH 19/11)
]
# chữ dòng viết lại sau khi đổi câu 19/11 (Gemini viết trước lượt đổi)
D_TEXT = {
    "C10-03|TH": "Học sinh dùng định lí Pythagore tìm chiều cao hình nón (biết bán kính đáy và đường sinh, hoặc "
                 "hình nón tạo thành khi quay tam giác vuông) rồi tính thể tích hình nón.",
    "C10-03|TACH": "Câu nhỏ tách từ đề thông hiểu: Học sinh thay bán kính đáy và đường sinh vào công thức diện tích "
                   "xung quanh hình nón, hoặc tính chiều cao hình nón tạo thành khi quay tam giác vuông.",   # 19/11 đổi BTVN
    "C10-05|TACH": "Câu nhỏ tách từ đề thông hiểu: Học sinh tính diện tích xung quanh hoặc thể tích của thùng nước, "
                   "bồn nước hình trụ ở ý đầu bài toán.",
    "C10-06|TH": "Học sinh so sánh, chia thể tích hai vật chứa theo gợi ý: đếm số thùng múc đầy bồn, xét đổ nước "
                 "sang lọ khác có bị tràn hay không.",
    "C10-08|TACH": "Câu nhỏ tách từ đề thông hiểu: Học sinh đổi đường kính đáy chai ra bán kính và tính thể tích "
                   "lượng nước đang có trong chai hình trụ.",
    "C10-08|TH": "Học sinh giải bài toán lật ngược chai theo gợi ý: thể tích chai bằng thể tích phần trụ chứa nước "
                 "cộng thể tích phần trụ không chứa nước khi lật ngược.",
}


def sua_chu(d):
    d = dict(d)
    d["d_text"] = {(k.replace("_", "-", 1).replace("_", "|") if "|" not in k else k): v
                   for k, v in d.get("d_text", {}).items()}
    d["d_text"].update(D_TEXT)
    d["dang_vd"] = [x for x in d.get("dang_vd", []) if "lật ngược" not in x]
    for f, cu, moi in SUA:
        if not cu:
            continue
        hit = [i for i, s in enumerate(d.get(f, [])) if cu in s]
        assert hit, f"{f}: không thấy {cu!r}"
        for i in hit:
            d[f][i] = d[f][i].replace(cu, moi)
    return d


def nhom_dong(rows):
    """Gom dòng chọn câu thành nhóm (dạng, KTC|NB|TACH|TH|VD) theo thứ tự dạy."""
    nhom = collections.OrderedDict()
    for r in rows:
        if r["loai"] == "NB kiến thức cũ":
            nhom.setdefault((r["dang"], "KTC"), []).append((r, "so_nb"))
        elif r["muc"] == "NB":
            nhom.setdefault((r["dang"], "NB"), []).append((r, "so_nb"))
        else:
            if r["so_nb"]:
                nhom.setdefault((r["dang"], "TACH"), []).append((r, "so_nb"))
            nhom.setdefault((r["dang"], r["muc"]), []).append((r, "so_y"))
    keys = sorted(nhom, key=lambda k: (RANK[k[1]], list(nhom).index(k)))
    return [(k, nhom[k]) for k in keys]


def dung_phieu(rows, chu):
    dt = chu.get("d_text", {})
    out = []
    for (dang, g), items in nhom_dong(rows):
        vidu = sum(r[f] for r, f in items if r["vai"] == "Ví dụ")
        lop = sum(r[f] for r, f in items if r["vai"] == "Trên lớp")
        btvn = sum(r[f] for r, f in items if r["vai"] == "BTVN")
        refs = list(dict.fromkeys(r["ma"] for r, _ in items))
        if g == "KTC":
            band, loai, dec = "NB", "NB kiến thức cũ", "none"
        elif g == "NB":
            band, loai, dec = "NB", "NB lẻ LT", "none"
        elif g == "TACH":
            band, loai, dec = "NB", "NB tách TH", "none"
        elif g == "VD":
            band, loai, dec = "VD", "VD lẻ", "vd"
        else:
            band, loai, dec = "TH", "TH lẻ LT", "none"
        k = f"{dang}|{g}"
        txt = dt.get(k, f"[chưa có chữ {k}]")
        gg = "ve-hinh" if k in VE_HINH_ROW else ("dien-khuyet" if band == "NB" and vidu > 0 else "")
        out.append({
            "dang": txt if g == "KTC" else txt + f" \\textit{{({dang})}}",
            "band": band, "loai": loai, "decompose": dec,
            "vidu": vidu, "onclass": lop, "btvn": btvn,
            "lythuyet": 1 if k in LYTHUYET_ROW else 0,
            "source_refs": refs,
            "gian_giao": gg,
        })
    for i, r in enumerate(out, 1):
        r["stt"] = i
    return out


def dung():
    rows = json.load(open(GOC))
    chu = _chu()
    phieu = []
    for p, meta in PHIEU.items():
        ph = {"code": meta["code"], "title": meta["title"], "so_ca": 1, "dich": meta["dich"],
              "rows": dung_phieu([r for r in rows if r["phieu"] == p], chu)}
        if meta.get("kiem_tra_phut"):
            ph["kiem_tra_phut"] = meta["kiem_tra_phut"]
        if meta.get("mien_sgk"):
            ph["mien_sgk"] = meta["mien_sgk"]
        phieu.append(ph)
    return {
        "slug": "thuyet-minh-lop-9c-chuong-10-hinh-khoi-trong-thuc-tien",
        "title": "Chương X. Một số hình khối trong thực tiễn (Bài 31 – Bài 32 SGK)",
        "grade": "lop-9", "subject": "hinh-hoc", "tier": "C", "tuan": "32-33",
        "chuong": "chuong-10",
        "luat_16_11": True,
        "thoiluong": THOILUONG,
        "kien_thuc_nen": chu.get("kien_thuc_nen", []),
        "lythuyet": chu.get("lythuyet", []),
        "vidu": chu.get("vidu", []),
        "dang_vd": chu.get("dang_vd", []),
        "loisai": chu.get("loisai", []),
        "kienthuc_nb": chu.get("kienthuc_nb", []),
        "phieu": phieu,
    }


if __name__ == "__main__":
    spec = dung()
    for p in spec["phieu"]:
        t = collections.Counter()
        for r in p["rows"]:
            for f in ("vidu", "onclass", "btvn"):
                t[(r["band"], f)] += r[f]
            print(f"  {r['stt']:2} {r['band']} {r['loai']:16} {r['vidu']:2} {r['onclass']:3} {r['btvn']:3} "
                  f"{r['gian_giao']:11} {r['dang'][:60]}")
        print(p["code"], " ".join(f"{b}:{t[(b,'vidu')]}/{t[(b,'onclass')]}/{t[(b,'btvn')]}" for b in ("NB", "TH", "VD")))
    if "--ghi" in sys.argv:
        json.dump(spec, open(OUT, "w"), ensure_ascii=False, indent=2)
        print("Đã ghi", OUT)
