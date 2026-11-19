# Dựng thuyết minh chương VIII lớp 9C (từ chon-cau.json + Gemini tm-ch8-9c-chu.json).
# 1 phiếu gộp 180′ (luat_16_11 = True, khuon = "khong_vd"):
#   Ví dụ    : 10 NB + 8 TH = 42,0′ (+ 3′ lý thuyết = 45,0′)
#   Trên lớp : 32 NB + 12 TH = 120,0′ (40,0% NB / 60,0% TH)
#   BTVN     : 26 NB + 10 TH = 85,8′  (39,4% NB / 60,6% TH)
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chon_cau_ch8_9c as cc  # noqa: E402

CHU_PATH = Path("storage/gemini/xong/tm-ch8-9c-chu.json")
OUT_PATH = Path("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/thuyet-minh.json")

# Thứ tự 15 dòng bảng nội dung Phiếu 1: (dang, nhom, band, loai, decompose, lythuyet)
NHOM_DONG = [
    ("KTC",   "KTC",     "NB", "NB kiến thức cũ", "none",  0),
    ("C8-01", "NB",      "NB", "NB lẻ LT",        "none",  1),
    ("C8-02", "NB",      "NB", "NB lẻ LT",        "none",  0),
    ("C8-03", "NB",      "NB", "NB lẻ LT",        "none",  1),
    ("C8-03", "TACH",    "NB", "NB tách TH",      "none",  0),
    ("C8-03", "TH",      "TH", "TH lẻ LT",        "none",  0),
    ("C8-04", "TACH",    "NB", "NB tách TH",      "none",  0),
    ("C8-04", "TH",      "TH", "TH lẻ LT",        "none",  0),
    ("C8-05", "NB",      "NB", "NB lẻ LT",        "none",  0),
    ("C8-05", "TACH",    "NB", "NB tách TH",      "none",  0),
    ("C8-05", "TH",      "TH", "TH lẻ LT",        "none",  0),
    ("C8-06", "NB",      "NB", "NB lẻ LT",        "none",  1),
    ("C8-06", "TACH",    "NB", "NB tách TH",      "none",  0),
    ("C8-06", "TH",      "TH", "TH lẻ LT",        "none",  0),
    ("C8-06", "TH_GHEP", "TH", "TH ghép bài",     "th2nb", 0),
]

DONG_MO_TA = {
    "KTC|KTC":      "Ôn lại thống kê chương VII (cỡ mẫu, tần số tương đối) làm cầu nối xác suất từ biểu đồ",
    "C8-01|NB":     "Nhận biết phép thử ngẫu nhiên, kết quả, tính đồng khả năng và biến cố xảy ra hay không",
    "C8-02|NB":     "Mô tả không gian mẫu Ω, đếm n(Ω) một hành động và liệt kê kết quả thuận lợi của biến cố",
    "C8-03|NB":     "Áp dụng công thức xác suất cổ điển một hành động mức nhận biết (1 bước đọc hoặc đếm thẳng)",
    "C8-03|TACH":   "Bước đệm NB tách từ bài TH C8-03: xác định n(Ω), số còn lại hoặc lọc phần tử thoả điều kiện",
    "C8-03|TH":     "Tính xác suất một hành động tập nền cho sẵn (khuôn Câu I.2 Hà Nội: chia có dư, nguyên tố, chính phương, hai điều kiện, làm tròn)",
    "C8-04|TACH":   "Bước đệm NB tách từ bài TH C8-04: liệt kê không gian mẫu Ω và đếm n(Ω) từ điều kiện số",
    "C8-04|TH":     "Tính xác suất một hành động khi tự liệt kê không gian mẫu Ω theo điều kiện chữ số / tính chất số",
    "C8-05|NB":     "Đọc tỉ lệ phần trăm hoặc bảng thống kê hai chiều đơn giản để tính xác suất chọn một đối tượng",
    "C8-05|TACH":   "Bước đệm NB tách từ bài TH C8-05: đọc tổng cỡ mẫu và lọc nhóm thoả mãn trên bảng / biểu đồ",
    "C8-05|TH":     "Tính xác suất chọn một đối tượng từ biểu đồ tần số ghép nhóm, biểu đồ quạt tròn, cột kép hoặc bảng số liệu thô",
    "C8-06|NB":     "Nhẩm số phần tử không gian mẫu hai hành động độc lập (quy tắc nhân) và liệt kê nhanh kết quả tung đồng xu 2 lần",
    "C8-06|TACH":   "Bước đệm NB tách từ bài TH C8-06: nhận dạng phép thử, đếm/mô tả n(Ω) hai hành động, lọc phần tử bẫy (không phải số nguyên tố, phân biệt (a;b) và (b;a))",
    "C8-06|TH":     "Tính xác suất phép thử hai hành động độc lập (bảng hai chiều, sơ đồ cây): đồng xu – xúc xắc – thẻ – hai túi – hai xúc xắc",
    "C8-06|TH_GHEP":"Bài đích hai hành động hoàn chỉnh: xác định phép thử → lập bảng mô tả Ω → tính xác suất nhiều biến cố (chia hết, số nguyên tố, ít nhất một)",
}

THOILUONG = [
    "Buổi 1 (Bài 25. Phép thử ngẫu nhiên và không gian mẫu + Bài 26. Xác suất của biến cố liên quan tới phép thử + Luyện tập chung, Bài tập cuối chương VIII): 1 ca = 180 phút (thực dạy 165 phút + giải lao 15 phút).",
    "\\textbf{Tổng 1 ca = 180 phút} (PPCT SGV chương VIII: 7 tiết; lớp 9C dạy 1 ca gộp toàn chương theo khuôn không VD; buổi ôn tập và kiểm tra gộp chương VII + VIII xếp riêng ở tuần 33).",
]


def _thap_phan(s: str) -> str:
    """Đổi dấu phẩy thập phân trong toán thành {,} chuẩn Việt Nam."""
    return re.sub(r"(?<=\d),(?=\d)", "{,}", s)


def _sua_latex(s: str) -> str:
    s = s.strip()
    s = s.replace("–", "--") if "$" in s and False else s
    # Thay ký tự toán Unicode lọt ngoài $...$ thành LaTeX an toàn
    rep = {
        "≤": r"$\le$",
        "≥": r"$\ge$",
        "≠": r"$\ne$",
        "×": r"$\times$",
        "÷": r"$\div$",
        "∈": r"$\in$",
        "∉": r"$\notin$",
        "Ω": r"$\Omega$",
        "⇒": r"$\Rightarrow$",
        "→": r"$\to$",
    }
    parts = s.split("$")
    for idx in range(0, len(parts), 2):  # ngoài $...$
        parts[idx] = parts[idx].replace("`khong_vd`", "không VD")
        for k, v in rep.items():
            parts[idx] = parts[idx].replace(k, v)
        # escape % & _ trần nếu chưa escape
        parts[idx] = re.sub(r"(?<!\\)%", r"\\%", parts[idx])
        parts[idx] = re.sub(r"(?<!\\)&", r"\\&", parts[idx])
        parts[idx] = re.sub(r"(?<!\\)_", r"\\_", parts[idx])
    for idx in range(1, len(parts), 2):  # trong $...$
        parts[idx] = (
            parts[idx]
            .replace("≤", r"\le ")
            .replace("≥", r"\ge ")
            .replace("≠", r"\ne ")
            .replace("×", r"\times ")
            .replace("÷", r"\div ")
            .replace("∈", r"\in ")
            .replace("∉", r"\notin ")
            .replace("Ω", r"\Omega ")
            .replace("⇒", r"\Rightarrow ")
            .replace("→", r"\to ")
        )
        parts[idx] = _thap_phan(parts[idx])
    out = "$".join(parts)
    # Rút gọn $$ nếu có
    out = out.replace("$$", " ")
    return out


def gom_dong(d_text: dict[str, str]):
    buckets = {
        f"{d}|{nhom}": {
            "dang_key": d,
            "nhom": nhom,
            "band": band,
            "loai": loai,
            "decompose": decomp,
            "lythuyet": lt,
            "vidu": 0,
            "onclass": 0,
            "btvn": 0,
            "source_refs": [],
        }
        for d, nhom, band, loai, decomp, lt in NHOM_DONG
    }
    vai_map = {"Ví dụ": "vidu", "Trên lớp": "onclass", "BTVN": "btvn"}

    for phieu, vai, dang, muc, so_y, so_nb, loai_r, ma, y, ht in cc.R:
        vf = vai_map[vai]
        if dang == "KTC":
            b = buckets["KTC|KTC"]
            b[vf] += so_nb
            if ma not in b["source_refs"]:
                b["source_refs"].append(ma)
            continue
        if muc == "NB":
            b = buckets[f"{dang}|NB"]
            b[vf] += so_nb
            if ma not in b["source_refs"]:
                b["source_refs"].append(ma)
        elif muc == "TH":
            nh = "TH_GHEP" if loai_r == "TH ghép bài" else "TH"
            b_th = buckets[f"{dang}|{nh}"]
            b_th[vf] += so_y
            if ma not in b_th["source_refs"]:
                b_th["source_refs"].append(ma)
            if so_nb > 0:
                b_tach = buckets[f"{dang}|TACH"]
                b_tach[vf] += so_nb
                if ma not in b_tach["source_refs"]:
                    b_tach["source_refs"].append(ma)

    rows = []
    for stt, (d, nhom, band, loai, decomp, lt) in enumerate(NHOM_DONG, 1):
        key = f"{d}|{nhom}"
        b = buckets[key]
        raw_txt = d_text.get(key) or DONG_MO_TA[key]
        # Bảo đảm kết thúc bằng \textit{(C8-xx)} hoặc \textit{(Kiến thức cũ)}
        txt = _sua_latex(raw_txt.rstrip("."))
        tag_suffix = r"\textit{(Kiến thức cũ, C8-05)}" if d == "KTC" else rf"\textit{{({d})}}"
        if f"({d})" not in txt and "Kiến thức cũ" not in txt:
            txt = f"{txt}. {tag_suffix}"
        rows.append({
            "stt": stt,
            "dang": txt,
            "band": b["band"],
            "loai": b["loai"],
            "decompose": b["decompose"],
            "vidu": b["vidu"],
            "onclass": b["onclass"],
            "btvn": b["btvn"],
            "lythuyet": b["lythuyet"],
            "source_refs": b["source_refs"],
            "gian_giao": "",
        })
    return rows


def dung():
    if CHU_PATH.exists():
        raw_chu = json.load(CHU_PATH.open())
        chu = raw_chu.get("ket_qua", raw_chu)
        chu["vidu"] = [
            x.replace(
                "chọn sách trên giá, quay bánh xe $16$ hình quạt",
                "quay bánh xe $10$ ô số và bánh xe $16$ hình quạt",
            ).replace("công thức cơ bản (xúc xắc, $52$ thẻ)", "công thức cơ bản (túi kẹo $60$ viên, $52$ thẻ)")
            for x in chu["vidu"]
        ]
    else:
        chu = {
            "d_text": DONG_MO_TA,
            "kien_thuc_nen": ["(Chưa chạy Gemini tm-ch8-9c-chu)"],
            "lythuyet": ["(Chưa chạy Gemini tm-ch8-9c-chu)"],
            "vidu": ["(Chưa chạy Gemini tm-ch8-9c-chu)"],
            "loisai": ["(Chưa chạy Gemini tm-ch8-9c-chu)"],
            "kienthuc_nb": ["(Chưa chạy Gemini tm-ch8-9c-chu)"],
        }

    rows = gom_dong(chu.get("d_text", {}))
    spec = {
        "slug": "thuyet-minh-lop-9c-chuong-08-xac-suat",
        "title": "Chương VIII. Xác suất của biến cố trong một số mô hình xác suất đơn giản (Bài 25 – Bài 26 SGK)",
        "grade": "lop-9",
        "subject": "dai-so",
        "tier": "C",
        "tuan": "32",
        "chuong": "chuong-08",
        "luat_16_11": True,
        "kiem_tra_gop": "chuong-07-tan-so-va-tan-so-tuong-doi",
        "thoiluong": THOILUONG,
        "kien_thuc_nen": [_sua_latex(x) for x in chu["kien_thuc_nen"]],
        "lythuyet": [_sua_latex(x) for x in chu["lythuyet"]],
        "vidu": [_sua_latex(x) for x in chu["vidu"]],
        "dang_vd": [
            "Không có: Thầy chốt không dạy câu vận dụng (VD) trong chương VIII lớp 9C, tương tự chương VII (phiếu theo khuôn $40\\%$ nhận biết -- $60\\%$ thông hiểu). Ma trận đề vào 10 Hà Nội Câu I.2 chủ yếu ở mức thông hiểu (C8-03 chiếm $57/94$ câu đề thi); $6$ ý VD ở C8-06 và các dạng nâng cao C8-07..13 không đưa vào phiếu."
        ],
        "loisai": [_sua_latex(x) for x in chu["loisai"]],
        "kienthuc_nb": [_sua_latex(x) for x in chu["kienthuc_nb"]],
        "phieu": [
            {
                "code": "1",
                "title": "Phiếu 1 (Bài 25 + Bài 26): Phép thử ngẫu nhiên, không gian mẫu và xác suất của biến cố",
                "khuon": "khong_vd",
                "rows": rows,
            }
        ],
    }
    return spec


def main():
    spec = dung()
    p = spec["phieu"][0]
    tong = Counter()
    lt = 0
    for r in p["rows"]:
        lt += r["lythuyet"]
        for f in ("vidu", "onclass", "btvn"):
            tong[(r["band"], f)] += r[f]
        print(
            f"  #{r['stt']:2d} [{r['band']}] {r['loai']:16s} "
            f"vd={r['vidu']} oc={r['onclass']} bt={r['btvn']} lt={r['lythuyet']} "
            f"refs={len(r['source_refs'])}"
        )
    print(
        f"\nTổng kết P1: lt={lt}′ · "
        + " · ".join(f"{b}: {tong[(b,'vidu')]}/{tong[(b,'onclass')]}/{tong[(b,'btvn')]}" for b in ("NB", "TH", "VD"))
    )
    if "--ghi" in sys.argv:
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
        print("Đã ghi", OUT_PATH)


if __name__ == "__main__":
    main()
