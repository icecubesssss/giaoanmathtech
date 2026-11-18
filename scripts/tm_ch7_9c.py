# Thuyết minh chương VII lớp 9C (18/11/2026) — sinh từ bảng chọn câu, khuôn như tm_ch6_9c_ban2.py.
# Nguồn số: inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/chon-cau.json (scripts/chon_cau_ch7_9c.py).
# Nguồn chữ (luật giao Gemini 16/11): storage/gemini/xong/tm-ch7-9c-chu.json
#   (scripts/gemini/viec_chon_cau_ch7_9c.py) — Claude chỉ viết khung số + thời lượng.
# Chạy:  python3 scripts/tm_ch7_9c.py [--ghi]
import json, sys, collections
from pathlib import Path

GOC = "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/chon-cau.json"
OUT = "inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/thuyet-minh.json"
CHU = Path("storage/gemini/xong/tm-ch7-9c-chu.json")
TITLE_P1 = ("Phiếu 1 — Bài 22, 23, 24: Bảng tần số, tần số tương đối; "
            "bảng tần số và tần số tương đối ghép nhóm")
# dòng TM mở thẻ lý thuyết (một dòng/mạch kiến thức chính)
LYTHUYET_ROW = {"C7-01|NB", "C7-02|NB", "C7-05|NB"}
RANK = {"KTC": 0, "NB": 1, "TACH": 2, "TH": 3}

THOILUONG = [
    "Buổi 1 (Bài 22, 23, 24 — bảng tần số, tần số tương đối, bảng tần số và tần số tương đối ghép nhóm): "
    "1 ca = 180 phút, tuần 31 (Thầy chốt 17/11/2026: một phiếu trọn buổi).",
    "\\textbf{Tổng 1 ca = 180 phút} (PPCT SGV chương VII: 10 tiết $\\Rightarrow$ chương dạy nén; "
    "phần vẽ biểu đồ không dạy ở lớp 9C).",
    "Kiểm tra chương: không kiểm tra riêng — bài kiểm tra chương gộp chương VII và chương VIII "
    "(Xác suất của biến cố) ở buổi sau chương VIII.",
]


def _chu():
    if not CHU.exists():
        return {}
    d = json.loads(CHU.read_text())
    return sua_chu(d.get("ket_qua") or d.get("json") or d)


# Claude soát đầu ra Gemini (18/11): thay đúng chuỗi, assert để biết khi Gemini viết lại khác đi.
SUA = {
    "kienthuc_nb": [
        ("$f=\\dfrac{m}{N}\\cdot 100\\%$", "$f=\\dfrac{m}{n}\\cdot 100\\%$"),   # SGK Bài 23 tr.38 dùng n
        ("$N$ là cỡ mẫu", "$n$ là cỡ mẫu"),
        ("bằng cỡ mẫu $N$", "bằng cỡ mẫu $n$"),
        ("và cỡ mẫu $N$", "và cỡ mẫu $n$"),
        ("Bài 22)", "Bài 22, tr.33)"), ("Bài 23)", "Bài 23, tr.38)"), ("Bài 24)", "Bài 24, tr.47)"),
    ],
    "vidu": [("$[155; 158)$ đến $[164; 167)$",
              "$[150; 158)$ đến $[164; 167)$ (SGK tr.47 ghi nhóm đầu $[155; 158)$ nhưng dãy có $154$ và lời giải dùng $[150; 158)$)")],
    "kien_thuc_nen": [("So sánh số thập phân và bất đẳng thức nửa khoảng", "So sánh số, đọc điều kiện $a\\le x<b$")],
}


def sua_chu(d):
    d = dict(d)
    d["d_text"] = {(k.replace("_", "-", 1).replace("_", "|") if "|" not in k else k): v
                   for k, v in d.get("d_text", {}).items()}
    for f, cap in SUA.items():
        for cu, moi in cap:
            hit = [i for i, s in enumerate(d.get(f, [])) if cu in s]
            assert hit, f"{f}: không thấy {cu!r}"
            for i in hit:
                d[f][i] = d[f][i].replace(cu, moi)
    # 4 ví dụ bù quỹ 45′ thêm sau lượt Gemini (18/11), số đã soát bằng tay
    d["vidu"] = d.get("vidu", []) + [
        "Buổi 1: ví dụ bổ sung — lập bảng tần số từ biểu đồ cột phương tiện đến trường ($9$; $5$; $8$ ngày, SGK 7.3); "
        "đối chiếu biểu đồ cột và đoạn thẳng của cùng một dữ liệu (SGK Bài 22 HĐ2); bảng tần số tương đối ghép nhóm "
        "thời gian chạy $100$ m ($12{,}5\\%$; $50\\%$; $32{,}5\\%$; $5\\%$, SGK 7.19); tính ngược tần số nhóm "
        "$[25;35)$: $33{,}75\\%\\cdot 160=54$ đại biểu (đề minh họa Láng Thượng)."]
    return d


def nhom_dong(rows):
    """Gom dòng chọn câu thành nhóm (dạng, NB|TACH|TH|KTC) theo thứ tự dạy."""
    nhom = collections.OrderedDict()
    for r in rows:
        if r["loai"] == "NB kiến thức cũ":
            nhom.setdefault((r["dang"], "KTC"), []).append((r, "so_nb"))
        elif r["muc"] == "NB":
            nhom.setdefault((r["dang"], "NB"), []).append((r, "so_nb"))
        else:
            if r["so_nb"] and r["vai"] != "Ví dụ":
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
        else:
            ls = [r["loai"] for r, _ in items]
            loai = "TH ghép bài" if "TH ghép bài" in ls else "TH lẻ LT"
            band, dec = "TH", ("th2nb" if loai != "TH lẻ LT" else "none")
        k = f"{dang}|{g}"
        txt = dt.get(k, f"[chưa có chữ {k}]")
        out.append({
            "dang": txt if g == "KTC" else txt + f" \\textit{{({dang})}}",
            "band": band, "loai": loai, "decompose": dec,
            "vidu": vidu, "onclass": lop, "btvn": btvn,
            "lythuyet": 1 if k in LYTHUYET_ROW else 0,
            "source_refs": refs,
            "gian_giao": "dien-khuyet" if (band == "NB" and vidu > 0) else "",
        })
    for i, r in enumerate(out, 1):
        r["stt"] = i
    return out


def dung():
    rows = json.load(open(GOC))
    chu = _chu()
    spec = {
        "slug": "thuyet-minh-lop-9c-chuong-07-tan-so-va-tan-so-tuong-doi",
        "title": "Chương VII. Tần số và tần số tương đối (Bài 22 – Bài 24 SGK)",
        "grade": "lop-9", "subject": "dai-so", "tier": "C", "tuan": "31",
        "chuong": "chuong-07",
        "luat_16_11": True,
        "kiem_tra_gop": "chuong-08-xac-suat-cua-bien-co",
        "thoiluong": THOILUONG,
        "kien_thuc_nen": chu.get("kien_thuc_nen", []),
        "lythuyet": chu.get("lythuyet", []),
        "vidu": chu.get("vidu", []),
        "dang_vd": ["Không có: ma trận đề vào 10 của Sở ghi mạch Thống kê không có câu vận dụng; tab phân dạng "
                    "chấm 375 ý, không ý nào ở mức vận dụng (phiếu theo khuôn 40\\% nhận biết, 60\\% thông hiểu)."],
        "loisai": chu.get("loisai", []),
        "kienthuc_nb": chu.get("kienthuc_nb", []),
        "phieu": [{"code": "1", "title": TITLE_P1, "khuon": "khong_vd",
                   "rows": dung_phieu([r for r in rows if r["phieu"] == "P1"], chu)}],
    }
    return spec


if __name__ == "__main__":
    spec = dung()
    for p in spec["phieu"]:
        t = collections.Counter()
        for r in p["rows"]:
            for f in ("vidu", "onclass", "btvn"):
                t[(r["band"], f)] += r[f]
            print(f"  {r['stt']:2} {r['band']} {r['loai']:16} {r['vidu']:2} {r['onclass']:3} {r['btvn']:3}  {r['dang'][:70]}")
        print(p["code"], " ".join(f"{b}:{t[(b,'vidu')]}/{t[(b,'onclass')]}/{t[(b,'btvn')]}" for b in ("NB", "TH")))
    if "--ghi" in sys.argv:
        json.dump(spec, open(OUT, "w"), ensure_ascii=False, indent=2)
        print("Đã ghi", OUT)
