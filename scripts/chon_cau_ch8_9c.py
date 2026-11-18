# Chọn câu chương VIII lớp 9C (18/11/2026) — khuôn không VD (40% NB – 60% TH – 0% VD), 1 phiếu gộp 180′.
# Mục tiêu:
#   Ví dụ    : 10 NB + 8 TH = 42,0′ (+ 3′ lý thuyết = 45,0′)
#   Trên lớp : 32 NB + 12 TH = 120,0′ (đúng 40,0% NB / 60,0% TH)
#   BTVN     : 26 NB + 10 TH = 85,8′  (39,4% NB / 60,6% TH)
# Tỉ lệ nguồn trên lớp (bài gốc duy nhất): Đề thi ≥ 50% · SGK ≥ 20% · STK ≤ 30%.
import json
import sys
from collections import Counter
from pathlib import Path

BANK_PATH = Path("inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08.json")
PDY_PATH = Path("inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08/phan-dang-y.json")
KT_PATH = Path(
    "inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
    "kiem-tra-chuong/ma-tran-va-dap-an-kiem-tra-chuong-vii-viii.json"
)
CH7_PATH = Path("inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07/chon-cau.json")
GEM_PATH = Path("storage/gemini/xong/cc-ch8-9c.json")
OUT_PATH = Path("inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08/chon-cau.json")

RATE = {
    "Ví dụ": {"NB": 1.0, "TH": 4.0, "VD": 8.0},
    "Trên lớp": {"NB": 1.5, "TH": 6.0, "VD": 12.0},
    "BTVN": {"NB": 1.3, "TH": 5.2, "VD": 10.4},
}
# Trọng số T1..T8 chuẩn lớp C (docs/quy-chuan-hoc-lieu.md §1)
W = [3, 1, 2, 1, 2, 2, 2, 0]
NGUONG = {"NB": 5, "TH": 6, "VD": 7}

# Bản chép nguyên văn từ SGK / đề thi trong tài liệu STK → CẤM bốc bản STK
KHONG_BOC = {
    "tl-ptnn-xsbc-3-tr3",    # == sgk-b25-vd1
    "tl-ptnn-xsbc-8-tr4",    # == sgk-b25-lt1
    "tl-ptnn-xsbc-11-tr4",   # == sgk-8.3
    "tl-ptnn-xsbc-19-tr5",   # == sgk-b26-lt1
    "tl-ptnn-xsbc-20-tr6",   # == sgk-b26-hd1
    "tl-ptnn-xsbc-34-tr9",   # == ck2-phuc-dong-2025-I2 (+ a,b)
    "tl-ptnn-xsbc-35-tr9",   # == gk2-nghia-tan-2025-I2 + v10-dong-da-de18-2025-I2
    "tl-ptnn-xsbc-46-tr11",  # == v10-lang-thuong-2025-II2
    "tl-ptnn-xsbc-48-tr11",  # == sgk-8.5
    "tl-ptnn-xsbc-49-tr11",  # == sgk-8.11
    "tl-ptnn-xsbc-54-tr12",  # == sgk-8.6
    "tl-ptnn-xsbc-55-tr12",  # == sgk-8.10
    "tl-ptnn-xsbc-57-tr12",  # == sgk-b26-lt2
    "tl-ptnn-xsbc-58-tr13",  # == sgk-8.8
    "tl-ptnn-xsbc-59-tr13",  # == sgk-8.9
    "tl-ptnn-xsbc-60-tr13",  # == sgk-8.15
    "tl-ptnn-xsbc-61-tr13",  # == sgk-8.17
    "tl-ptnn-xsbc-66-tr14",  # == sgk-8.7
    # Bối cảnh trùng đề kiểm tra chương VII+VIII (v10-phuong-mai-2025-II2):
    "ck2-phan-dinh-phung-2025-TN9",
}

# Các nhóm trùng số liệu / cùng khung bài gần như y hệt — mỗi nhóm bốc tối đa 1
TRUNG = [
    ("sgk-b26-lt2", "v10-ha-dong-2025-I2"),
    ("so-hn-minhhoa-I2", "v10-thai-thinh-2025-I2", "v10-nguyen-truong-to-2025-I2", "v10-tam-khuong-2025-I2"),
    ("ck2-ngoc-lam-2024-T902-I2", "gk2-thanh-my-2024-12"),
    ("ck2-thang-long-2025-I2", "v10-chuong-my-l5-2025-I2"),
    ("ck2-hoai-duc-2024-I2", "gk2-trung-vuong-2025-I2"),
    ("ck2-lomonoxop-2025-I2", "v10-be-van-dan-2025-I2"),
    ("ck2-ngo-gia-tu-2025-d1-2", "ck2-nghia-tan-2025-I2"),
    ("v10-huy-van-2024-I2", "tl-ptnn-xsbc-69-tr14"),
    ("sgk-8.1", "sgk-8.5", "v10-ly-thuong-kiet-2025-I2"),
    ("gk2-nghia-tan-2025-I2", "v10-dong-da-de18-2025-I2"),
]

# Tuple: (phieu, vai, dang, muc, so_y, so_nb, loai, ma, y, hinh_thuc)
R = [
    # ── VÍ DỤ (10 NB + 8 TH = 42,0′) ──
    ("P1", "Ví dụ", "C8-01", "NB", 0, 2, "NB lẻ LT", "sgk-b26-hd1", "a-b", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-01", "NB", 0, 2, "NB lẻ LT", "tl-ptnn-xsbc-16-tr5", "a,c", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-02", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-12-tr4", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-02", "NB", 0, 2, "NB lẻ LT", "tl-ptnn-xsbc-22-tr6", "A-B", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-03", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-2-tr2", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-03", "NB", 0, 1, "NB lẻ LT", "gk2-nghia-tan-2025-I2", "a", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-05", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-74-tr15", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-03", "TH", 1, 0, "TH lẻ LT", "gk2-kieu-ky-2025-I2", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-03", "TH", 1, 0, "TH lẻ LT", "ck2-phuc-dong-2025-I2", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-03", "TH", 1, 0, "TH lẻ LT", "ck2-ngoc-thuy-2024-I2", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-04", "TH", 1, 0, "TH lẻ LT", "ck2-ngo-gia-tu-2025-d1-2", "a-b", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-05", "TH", 1, 0, "TH lẻ LT", "tl-ptnn-xsbc-31-tr8", "a-b", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-06", "TH", 1, 0, "TH lẻ LT", "sgk-b25-vd1", "a-b", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-06", "TH", 1, 0, "TH lẻ LT", "v10-ha-dong-2025-I2", "", "Ví dụ điền khuyết"),
    ("P1", "Ví dụ", "C8-06", "TH", 1, 0, "TH lẻ LT", "sgk-8.15", "A,D", "Ví dụ điền khuyết"),

    # ── TRÊN LỚP (32 NB + 12 TH = 120,0′) ──
    # NB kiến thức cũ (Ch.VII → Ch.VIII)
    ("P1", "Trên lớp", "KTC", "NB", 0, 2, "NB kiến thức cũ", "ck2-doan-thi-diem-2025-3", "a", "Trả lời ngắn"),
    # NB lẻ LT: C8-01 (2), C8-02 (5), C8-03 (5), C8-05 (1), C8-06 (1) -> 14; + KTC 2 + tách TH 16?
    # Kiểm đúng: C8-01 (4 NB lẻ), C8-02 (5 NB lẻ), C8-03 (5 NB lẻ), C8-05 (1 NB lẻ), C8-06 (1 NB lẻ) = 16 NB lẻ
    ("P1", "Trên lớp", "C8-01", "NB", 0, 1, "NB lẻ LT", "ck2-phan-dinh-phung-2025-TN8", "", "Trắc nghiệm 4 lựa chọn"),
    ("P1", "Trên lớp", "C8-01", "NB", 0, 1, "NB lẻ LT", "sgk-8.3", "a", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-01", "NB", 0, 2, "NB lẻ LT", "tl-ptnn-xsbc-27-tr7", "", "Đúng / Sai + trả lời ngắn"),
    ("P1", "Trên lớp", "C8-02", "NB", 0, 1, "NB lẻ LT", "ck2-gia-lam-2024-I2", "a", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-02", "NB", 0, 2, "NB lẻ LT", "sgk-b26-lt1", "b-E,b-F", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-02", "NB", 0, 2, "NB lẻ LT", "sgk-b26-vd1", "b-c", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-03", "NB", 0, 1, "NB lẻ LT", "so-hn-2026-I2", "", "Trắc nghiệm 4 lựa chọn"),
    ("P1", "Trên lớp", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-thach-that-2024-1-2", "", "Trắc nghiệm 4 lựa chọn"),
    ("P1", "Trên lớp", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-ba-dinh-2024-I2", "", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-hai-ba-trung-2024-I2", "", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-03", "NB", 0, 1, "NB lẻ LT", "v10-chuong-my-l4-2025-I2", "", "Trắc nghiệm / Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-05", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-43-tr10", "a", "Trả lời ngắn"),
    ("P1", "Trên lớp", "C8-06", "NB", 0, 1, "NB lẻ LT", "ck2-phan-dinh-phung-2025-TN11", "", "Trắc nghiệm 4 lựa chọn"),
    # TH trên lớp (+ 14 NB tách TH = 16 + 2 + 14 = 32 NB, 12 TH)
    ("P1", "Trên lớp", "C8-03", "TH", 1, 1, "TH lẻ LT", "so-hn-2025-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-03", "TH", 1, 1, "TH lẻ LT", "ck2-phuc-loi-2024-1-2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-03", "TH", 1, 1, "TH lẻ LT", "v10-tu-lap-2026-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-04", "TH", 1, 1, "TH lẻ LT", "gk2-nam-tu-liem-2025-I2", "a-b", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-04", "TH", 1, 1, "TH lẻ LT", "v10-tho-loc-l3-2025-I2", "M,b", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-05", "TH", 1, 1, "TH lẻ LT", "gk2-chuong-duong-2025-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-05", "TH", 1, 1, "TH lẻ LT", "tl-ptnn-xsbc-45-tr11", "a,c", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-b25-lt1", "a-b", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.6", "E-F", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.7", "F-G", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-06", "TH", 1, 2, "TH ghép bài", "ck2-chu-van-an-dn-2025-5", "a,M,N", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "Trên lớp", "C8-06", "TH", 1, 2, "TH ghép bài", "ck2-phan-dinh-phung-2025-TL4", "a-b,M,N", "Tự luận + câu hỏi gợi ý bước"),

    # ── BTVN (26 NB + 10 TH = 85,8′) ──
    # NB lẻ LT: C8-01 (3), C8-02 (4), C8-03 (6), C8-05 (1), C8-06 (2) = 16 NB lẻ
    ("P1", "BTVN", "C8-01", "NB", 0, 1, "NB lẻ LT", "sgk-8.1", "a", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-01", "NB", 0, 2, "NB lẻ LT", "tl-ptnn-xsbc-17-tr5", "a,c", "Đúng / Sai + giải thích ngắn"),
    ("P1", "BTVN", "C8-02", "NB", 0, 1, "NB lẻ LT", "gk2-nguyen-binh-khiem-2024-I2", "a", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-02", "NB", 0, 1, "NB lẻ LT", "v10-lang-thuong-2025-II2", "a", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-02", "NB", 0, 2, "NB lẻ LT", "tl-ptnn-xsbc-21-tr6", "M,N", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-thai-thinh-2025-I2", "", "Trắc nghiệm 4 lựa chọn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-lomonoxop-2024-I2", "", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-ngoc-lam-2024-T901-I2", "", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "ck2-phuc-dong-2024-902-I2", "", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "gk2-nhat-tan-2024-I2", "", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-03", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-38-tr9", "a", "Trả lời ngắn"),
    ("P1", "BTVN", "C8-05", "NB", 0, 1, "NB lẻ LT", "tl-ptnn-xsbc-76-tr15", "", "Trắc nghiệm 4 lựa chọn"),
    ("P1", "BTVN", "C8-06", "NB", 0, 2, "NB lẻ LT", "v10-be-van-dan-2025-I2-md2", "a,b-A,b-B", "Trả lời ngắn"),
    # TH BTVN (+ 10 NB tách TH = 16 + 10 = 26 NB, 10 TH)
    ("P1", "BTVN", "C8-03", "TH", 1, 1, "TH lẻ LT", "gk2-trung-vuong-2025-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-03", "TH", 1, 1, "TH lẻ LT", "v10-khuong-thuong-2025-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-03", "TH", 1, 1, "TH lẻ LT", "v10-cau-giay-lan1-2026-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-04", "TH", 1, 1, "TH lẻ LT", "ck2-trung-vuong-2025-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-04", "TH", 1, 1, "TH lẻ LT", "tl-ptnn-xsbc-51-tr12", "a,B", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-05", "TH", 1, 1, "TH lẻ LT", "gk2-chuong-duong-2024-I2", "", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.8", "A-B", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.9", "a-b", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.10", "G-H", "Tự luận + câu hỏi gợi ý bước"),
    ("P1", "BTVN", "C8-06", "TH", 1, 1, "TH lẻ LT", "sgk-8.11", "a,b-F,b-G", "Tự luận + câu hỏi gợi ý bước"),
]


def load_bank():
    raw = json.load(BANK_PATH.open())
    rows = raw["rows"] if isinstance(raw, dict) else raw
    return {r["ma"]: r for r in rows}


def ma_de_kt() -> set[str]:
    kt = json.load(KT_PATH.open())
    out = set()
    for b in kt.get("ma_tran", kt.get("cau", [])):
        if isinstance(b, dict) and b.get("ma"):
            out.add(b["ma"])
    # Quét mọi chuỗi khớp mã trong file KT cho chắc
    txt = KT_PATH.read_text()
    bank = load_bank()
    for ma in bank:
        if ma in txt:
            out.add(ma)
    return out


def loai_nguon(uu: str) -> str:
    if uu.startswith("Ưu tiên 1"):
        return "Đề thi"
    if uu.startswith("Ưu tiên 2"):
        return "SGK"
    return "Sách tham khảo"


def diem_tu_T(T: list[int]) -> float:
    return round(sum(t * w for t, w in zip(T, W)) / (2 * sum(W)) * 10, 1)


def check():
    bank = load_bank()
    kt_set = ma_de_kt()
    ch7 = {r["ma"] for r in json.load(CH7_PATH.open())}
    pdy = json.load(PDY_PATH.open())
    clean_pdy_mas = set()
    by_ma = {}
    for it in pdy["y"]:
        by_ma.setdefault(it["ma_cau"], []).append(it)
    taught = {f"C8-0{i}" for i in range(1, 7)} | {"NGOAI"}
    for ma, its in by_ma.items():
        if all(i["dang_gop"] in taught for i in its):
            clean_pdy_mas.add(ma)

    mas = [r[7] for r in R]
    assert len(R) == len(set(mas)), f"Trùng mã: {[m for m, c in Counter(mas).items() if c > 1]}"
    missing = [m for m in mas if m not in bank]
    assert not missing, f"Thiếu trong bank: {missing}"
    banned = [m for m in mas if m in KHONG_BOC]
    assert not banned, f"Bốc mã cấm: {banned}"
    in_kt = [m for m in mas if m in kt_set]
    assert not in_kt, f"Trùng đề KT: {in_kt}"
    in_ch7 = [m for m in mas if m in ch7]
    assert not in_ch7, f"Trùng Ch.7: {in_ch7}"
    not_clean = [m for m in mas if m not in clean_pdy_mas]
    assert not not_clean, f"Có kỹ thuật ngoài 6 dạng dạy: {not_clean}"
    for grp in TRUNG:
        hit = [m for m in mas if m in grp]
        assert len(hit) <= 1, f"Trùng nhóm {grp}: {hit}"

    for vai in ("Ví dụ", "Trên lớp", "BTVN"):
        sub = [r for r in R if r[1] == vai]
        nb = sum(r[5] for r in sub)
        th = sum(r[4] for r in sub if r[3] == "TH")
        vd = sum(r[4] for r in sub if r[3] == "VD")
        p_nb = nb * RATE[vai]["NB"]
        p_th = th * RATE[vai]["TH"]
        p_vd = vd * RATE[vai]["VD"]
        tong = p_nb + p_th + p_vd
        nguon_cnt = Counter(loai_nguon(bank[r[7]]["uu"]) for r in sub)
        n = len(sub)
        print(
            f"{vai:9s}: {n:2d} câu gốc · {nb:2d} NB ({p_nb:4.1f}′={p_nb/tong*100:4.1f}%) + "
            f"{th:2d} TH ({p_th:4.1f}′={p_th/tong*100:4.1f}%) = {tong:5.1f}′ · "
            f"Đề={nguon_cnt['Đề thi']}/{n} ({nguon_cnt['Đề thi']/n*100:.0f}%), "
            f"SGK={nguon_cnt['SGK']}/{n} ({nguon_cnt['SGK']/n*100:.0f}%), "
            f"STK={nguon_cnt['Sách tham khảo']}/{n} ({nguon_cnt['Sách tham khảo']/n*100:.0f}%)"
        )

    # Kiểm tra cột band hiện có trong chuong-08.json (để biết gate có cảnh báo band không)
    print("\nTổng số dòng chọn câu:", len(R))
    for r in R:
        phieu, vai, dang, muc, so_y, so_nb, loai, ma, y, ht = r
        b_sheet = bank[ma].get("band", "")
        if b_sheet and b_sheet != muc:
            print(f"  [note bank.band] {vai:8s} {dang} chọn={muc} vs sheet={b_sheet}: {ma}")


def ghi():
    check()
    bank = load_bank()
    gem = {}
    if GEM_PATH.exists():
        raw_gem = json.load(GEM_PATH.open())
        gdata = raw_gem.get("ket_qua", raw_gem)
        gem = {d["ma"]: d for d in gdata.get("dong", [])}
        lai_path = GEM_PATH.with_name("cc-ch8-9c-lai.json")
        if lai_path.exists():
            raw_lai = json.load(lai_path.open())
            ldata = raw_lai.get("ket_qua", raw_lai)
            for d in ldata.get("dong", []):
                gem[d["ma"]] = d
        print("Đã nạp điểm Gemini:", len(gem), "mã")
    out = []
    for phieu, vai, dang, muc, so_y, so_nb, loai, ma, y, ht in R:
        r = bank[ma]
        g = gem.get(ma, {})
        T = g.get("T", [])
        diem = diem_tu_T(T) if len(T) == 8 else 0.0
        ng = NGUONG[muc]
        out.append({
            "phieu": phieu,
            "vai": vai,
            "dang": dang,
            "muc": muc,
            "so_y": so_y,
            "so_nb": so_nb,
            "phut": round(
                (so_nb * RATE[vai]["NB"]) + (so_y * RATE[vai][muc] if muc in ("TH", "VD") else 0.0),
                1,
            ),
            "loai": loai,
            "ma": ma,
            "y": y,
            "hinh_thuc": ht,
            "de": r["de"],
            "nguon": r["nguon"],
            "loai_nguon": loai_nguon(r["uu"]),
            "T": T,
            "diem": diem,
            "nguong": ng,
            "ket_luan": ("Đạt" if diem >= ng else "Dưới ngưỡng") if T else "",
            "ly_do": g.get("ly_do", ""),
            "de_xuat": g.get("de_xuat", ""),
            "nghi_ngo": g.get("nghi_ngo", ""),
        })
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, OUT_PATH.open("w"), ensure_ascii=False, indent=2)
    print("Đã ghi", OUT_PATH, f"({len(out)} dòng)")


if __name__ == "__main__":
    if "--ghi" in sys.argv:
        ghi()
    else:
        check()
