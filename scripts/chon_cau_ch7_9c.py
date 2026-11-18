# Chọn câu chương VII lớp 9C (17/11/2026) — Thầy: "đi quy trình như chương 6".
# Khung: MỘT phiếu 180′ trọn buổi t31 (Thầy chốt 17/11), khuôn `khong_vd` (ma trận Sở: mạch Thống kê VD = 0;
# tab: 375 ý, 0 ý VD). Dạng dạy = Thầy tick tab "Dạng Ch.VII" (9073): C7-01…05, 09; C7-10 = NB kiến thức cũ lớp 8.
# KHÔNG dạy C7-06 vẽ cột/đoạn thẳng, C7-07 vẽ quạt, C7-08 chọn biểu đồ. KT gộp VII+VIII ở buổi khác.
# Luật: AGENTS.md "LUẬT HÌNH THỨC CÂU + BẢN CHẤT 40-40-20" — NB = MỘT bước (1,5′) · TH = bài gọn + gợi ý bước (6′).
# Quỹ trên lớp 120′ = 32 NB + 12 TH (như P1 ch.VI). Ví dụ ~35–40′, BTVN ~86′ (26 NB + 10 TH).
# Vai Claude: chốt mã câu / vai / mức / số câu (phần cần phán đoán). Gemini: chấm T1–T7 + lí do + đề xuất
# (scripts/gemini/viec_chon_cau_ch7_9c.py) → storage/gemini/xong/cc-ch7-9c.json → cột T, ly_do ở đây.
# Chạy:  python3 scripts/chon_cau_ch7_9c.py            (in bảng phút + kiểm trùng)
#        python3 scripts/chon_cau_ch7_9c.py --ghi      (ghi chon-cau.json)
import json, sys, collections
from pathlib import Path

GOC = "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-07"
GEM = [Path("storage/gemini/xong/cc-ch7-9c.json"), Path("storage/gemini/xong/cc-ch7-9c-b.json"),
       Path("storage/gemini/xong/cc-ch7-9c-c.json"), Path("storage/gemini/xong/cc-ch7-9c-d.json"),
       Path("storage/gemini/xong/cc-ch7-9c-e.json")]  # b = lượt chấm câu thay 18/11
W = [3, 1, 2, 1, 2, 2, 2, 0]          # trọng số lớp C (T1..T8), tổng 13
NGUONG = {"NB": 5, "TH": 6, "VD": 7}
RATE = {  # phút/câu theo vai (config/tier_spec.json, đại số lớp 9)
    "Ví dụ": {"NB": 1.0, "TH": 4.0, "VD": 8.0},
    "Trên lớp": {"NB": 1.5, "TH": 6.0, "VD": 12.0},
    "BTVN": {"NB": 1.3, "TH": 5.2, "VD": 10.4},
}
TN, DS, TLN = "Trắc nghiệm A–D", "Đúng/Sai", "Trả lời ngắn"
TH_GY = "Tự luận + câu hỏi gợi ý bước"
VDK = "Ví dụ điền khuyết"
PHIEU = {"P1": "Phiếu 1 — Bảng tần số, tần số tương đối, ghép nhóm (Bài 22–24), không VD"}

# (phiếu, vai, dạng, mức, số ý ở mức đó, số câu NB, loại §4b, mã, ý, hình thức)
# Mức NB: số ý = 0, "số câu NB" là số câu nhỏ. Mức TH: "số câu NB" là câu NB tách từ chính đề đó.
R = [
# --- Ví dụ (GV làm mẫu, điền khuyết), mỗi mạch một mẫu ---
("P1","Ví dụ","C7-01","NB",0,2,"NB lẻ LT","sgk-b22-vd1","a-b",VDK),          # dãy cỡ giày → bảng tần số
("P1","Ví dụ","C7-01","NB",0,1,"NB lẻ LT","sgk-7.22","",VDK),                 # tần số còn thiếu khi biết cỡ mẫu
# 18/11 bù quỹ ví dụ 45′ (check-tm: 33′): biểu đồ → bảng, bảng f ghép nhóm, tính ngược n = f·N
("P1","Ví dụ","C7-01","NB",0,1,"NB lẻ LT","sgk-7.3","",VDK),
("P1","Ví dụ","C7-01","NB",0,2,"NB lẻ LT","sgk-b22-hd2","a-b",VDK),
("P1","Ví dụ","C7-02","TH",1,0,"TH lẻ LT","sgk-7.19","a-b",VDK),
("P1","Ví dụ","C7-04","TH",1,0,"TH lẻ LT","v10-lang-thuong-2025-II1","",VDK),
("P1","Ví dụ","C7-02","TH",1,0,"TH lẻ LT","sgk-b23-vd1","a",VDK),             # dãy thô → bảng tần số tương đối
("P1","Ví dụ","C7-02","NB",0,2,"NB lẻ LT","so-hn-2025-I1","",VDK),            # khuôn Câu I.1 đề Sở (bảng)
("P1","Ví dụ","C7-03","TH",1,0,"TH lẻ LT","v10-tho-loc-l2-2025-I1","a",VDK),   # % đại biểu dùng ít nhất 2 ngoại ngữ (Lômônôxốp 2025 trùng số liệu bài đích)
("P1","Ví dụ","C7-04","TH",2,0,"TH lẻ LT","v10-thai-thinh-2025-I1","a-b",VDK),# bảng f từ biểu đồ + ước lượng 240 xe
("P1","Ví dụ","C7-05","TH",1,0,"TH lẻ LT","sgk-b24-vd1","",VDK),              # ghép nhóm số liệu thô + f ghép nhóm
# ↑ SGK tr.47 tự lệch: đề ghi nhóm [155; 158) mà số liệu có 154, lời giải SGK dùng [150; 158) ⇒ phiếu dùng [150; 158)
("P1","Ví dụ","C7-05","NB",0,1,"NB lẻ LT","sgk-7.25","",VDK),                 # giá trị đại diện
("P1","Ví dụ","C7-09","TH",1,0,"TH lẻ LT","v10-cum-thcs-cong-lap-2026-I1","a-b",VDK),  # f nhóm + kiểm tra nhận định
# --- Trên lớp: NB lẻ (LT1) ---
("P1","Trên lớp","C7-10","NB",0,1,"NB kiến thức cũ","v10-be-van-dan-2025-I1-md2","c",TLN),  # lớp 8: đọc số trên biểu đồ cột
("P1","Trên lớp","C7-01","NB",0,2,"NB lẻ LT","gk2-le-ngoc-han-2025-I","1-2",TLN),   # 18/11 Thầy đánh "Không hay" Trung Vương GK2 (bảng cho sẵn, không lập bảng) ⇒ Lê Ngọc Hân: dãy 30 số liệu → bảng tần số
("P1","Trên lớp","C7-01","NB",0,1,"NB lẻ LT","sgk-7.2","",TLN),          # biểu đồ tranh → bảng tần số (TN3 Phan Đình Phùng trùng số liệu SGK 7.22)
("P1","Trên lớp","C7-01","NB",0,2,"NB lẻ LT","sgk-7.4","a-b",TLN),
("P1","Trên lớp","C7-01","NB",0,2,"NB lẻ LT","ck2-hat-mon-2025-I1","a-b",TLN),
("P1","Trên lớp","C7-01","NB",0,2,"NB lẻ LT","ck2-xuan-dinh-2025-I","1-2",TLN),
("P1","Trên lớp","C7-02","NB",0,2,"NB lẻ LT","so-hn-2026-I1","",TLN),
("P1","Trên lớp","C7-02","NB",0,2,"NB lẻ LT","so-hn-minhhoa-I1","",TLN),
("P1","Trên lớp","C7-02","NB",0,2,"NB lẻ LT","ck2-gia-lam-2024-I1","a-b",TLN),
("P1","Trên lớp","C7-02","NB",0,2,"NB lẻ LT","v10-tu-lap-2026-I1","",TLN),
("P1","Trên lớp","C7-03","NB",0,2,"NB lẻ LT","ck2-chu-van-an-2024-I1","",TLN),
("P1","Trên lớp","C7-05","NB",0,1,"NB lẻ LT","sgk-b24-lt1","a",TLN),   # 18/11: ý b lập cả bảng f = TH ⇒ chỉ lấy ý a
# --- Trên lớp: TH (LT2, bài gọn + gợi ý bước); đích = Nam Từ Liêm (khuôn đủ 4 ý Câu I.1) ---
("P1","Trên lớp","C7-02","TH",1,1,"TH lẻ LT","v10-khuong-thuong-2025-I1","",TH_GY),  # cỡ mẫu + bảng f ghép nhóm (Chương Dương 2025 trùng số liệu bài đích)
("P1","Trên lớp","C7-02","TH",1,1,"TH lẻ LT","v10-ha-dong-2025-I1","",TH_GY),   # NB tách: cỡ mẫu 40 (đề không ghi)
("P1","Trên lớp","C7-05","TH",1,1,"TH lẻ LT","v10-cat-linh-2025-I1","a-b",TH_GY),
("P1","Trên lớp","C7-05","TH",1,0,"TH lẻ LT","v10-thanh-oai-l2-2025-I1","",TH_GY),
("P1","Trên lớp","C7-04","TH",1,1,"TH lẻ LT","v10-chuong-my-l2-2025-I1","a-b",TH_GY),
("P1","Trên lớp","C7-04","TH",1,1,"TH lẻ LT","ck2-lomonoxop-2024-I1","a-b",TH_GY),
("P1","Trên lớp","C7-03","TH",1,1,"TH lẻ LT","v10-thai-thinh-2026-I1","a-b",TH_GY),
("P1","Trên lớp","C7-03","TH",1,1,"TH lẻ LT","ck2-cau-giay-2024-I","1-2",TH_GY),
("P1","Trên lớp","C7-03","TH",1,1,"TH lẻ LT","v10-tho-loc-l5-2025-I1","a-b",TH_GY),
("P1","Trên lớp","C7-09","TH",2,0,"TH lẻ LT","gk2-duc-giang-2025-I1","a-b",TH_GY),
("P1","Trên lớp","C7-03","TH",1,3,"TH ghép bài","gk2-nam-tu-liem-2025-I1","a-d",TH_GY),  # ĐÍCH
# --- BTVN (cùng dạng đã học, đề ngắn gọn) ---
("P1","BTVN","C7-01","NB",0,2,"NB lẻ LT","sgk-7.1","a-b",TLN),
("P1","BTVN","C7-01","NB",0,2,"NB lẻ LT","ck2-nguyen-du-2025-III1","a-b",TLN),
("P1","BTVN","C7-01","NB",0,1,"NB lẻ LT","v10-tho-loc-l3-2026-I1","",TLN),
("P1","BTVN","C7-01","NB",0,2,"NB lẻ LT","v10-chuong-my-l4-2025-I1","a-b",TLN),
("P1","BTVN","C7-02","NB",0,2,"NB lẻ LT","v10-be-van-dan-2025-I1","",TLN),
("P1","BTVN","C7-02","NB",0,2,"NB lẻ LT","gk2-nguyen-binh-khiem-2024-I1","a-b",TLN),
("P1","BTVN","C7-02","NB",0,2,"NB lẻ LT","ck2-ngo-gia-tu-2025-d1-1","a-b",TLN),   # 18/11 thay Mai Dịch (đề ghi 5 dấu huyền, đoạn thơ có 6)
("P1","BTVN","C7-02","NB",0,2,"NB lẻ LT","ck2-van-dien-2024-I","1-2",TLN),
("P1","BTVN","C7-02","NB",0,2,"NB lẻ LT","ck2-ngoc-thuy-2024-I1","",TLN),   # 18/11 thay Huy Văn (gần trùng Nguyễn Du: N = 50, đáp số 40%)
("P1","BTVN","C7-05","NB",0,1,"NB lẻ LT","sgk-7.30","a",TLN),
("P1","BTVN","C7-03","NB",0,1,"NB lẻ LT","v10-dong-da-2025-I1-md2","b",TLN),   # số xe chạy dưới 50 km/h
("P1","BTVN","C7-02","TH",1,0,"TH lẻ LT","gk2-le-hong-phong-2025-21","a-b",TH_GY),   # 18/11 thay Ngọc Lâm 2025 (đã ở đề KT gộp VII+VIII)
("P1","BTVN","C7-02","TH",1,0,"TH lẻ LT","sgk-7.6","",TH_GY),
("P1","BTVN","C7-02","TH",1,1,"TH lẻ LT","gk2-ngoc-lam-2024-I1","a-b",TH_GY),
("P1","BTVN","C7-03","TH",1,2,"TH lẻ LT","tl-tanso-5-tr4","a-c",TH_GY),
("P1","BTVN","C7-03","TH",1,1,"TH lẻ LT","ck2-hoai-duc-2024-I1","1-2",TH_GY),
("P1","BTVN","C7-03","TH",1,1,"TH lẻ LT","gk2-le-ngoc-han-2024-I1","a-b",TH_GY),
("P1","BTVN","C7-04","TH",1,0,"TH lẻ LT","sgk-7.12","",TH_GY),
("P1","BTVN","C7-04","TH",1,1,"TH lẻ LT","ck2-trung-vuong-2025-I1","a-b",TH_GY),
("P1","BTVN","C7-05","TH",1,0,"TH lẻ LT","sgk-b24-lt2","",TH_GY),
("P1","BTVN","C7-09","TH",1,1,"TH lẻ LT","ck2-cau-dien-2025-I1","a-b",TH_GY),
]

# Bài gốc trùng số liệu (mã khác) — bốc một thì cái kia phải nằm ngoài. Dò bằng dãy số trong đề (ratio ≥ 0,88) 17/11.
TRUNG = [
    {"v10-tho-loc-l2-2025-I1", "v10-tho-loc-l4-2026-I1"},
    {"tl-tsgn-6-tr4", "sgk-7.18"},
    {"sgk-7.9", "tl-tanso-17-tr8"},
    {"sgk-7.8", "tl-tanso-16-tr8"},
    {"ck2-ngo-gia-tu-2025-d2-1", "tl-tsgn-11-tr6"},
    {"ck2-le-hong-phong-2025-I1", "ck2-thach-that-2024-1-1", "ck2-gia-lam-2024-I1"},
    {"tl-tsgn-3-tr3", "tl-tanso-2-tr3"},
    {"tl-tsgn-17-tr7", "ck2-phuc-dong-2024-901-I1", "ck2-phuc-dong-2024-902-I1", "ck2-thang-long-2025-I1"},
    {"ck2-thai-thinh-2025-I1", "tl-tsgn-4-tr3"},
    {"gk2-phuc-loi-2024-2", "gk2-nam-tu-liem-2025-I1", "v10-dong-da-2025-I1", "ck2-lomonoxop-2025-I1",
     "gk2-chuong-duong-2025-I1"},
    # dò lần 2 (dãy tần số liên tiếp chung ≥ 4, bỏ nhãn nhóm): cùng dãy tần số, khác nhãn nhóm
    {"ck2-phuc-dong-2025-I1", "gk2-duc-giang-2025-I1", "v10-ung-hoa-lan3-2025-I1"},
    {"gk2-kieu-ky-2025-I1", "v10-cum-thcs-cong-lap-2026-I1", "tl-tsgn-17-tr7", "ck2-thang-long-2025-I1",
     "ck2-phuc-dong-2024-901-I1", "ck2-phuc-dong-2024-902-I1"},
    {"ck2-phan-dinh-phung-2025-TN7", "v10-lang-thuong-2025-II1"},
    {"gk2-nhat-tan-2024-I1", "sgk-b24-vd1"},
    {"ck2-ngoc-lam-2024-T901-I1", "ck2-ngoc-lam-2024-T902-I1"},
    {"v10-chuong-my-l4-2025-I1", "v10-tho-loc-l3-2025-I1"},
    {"gk2-le-ngoc-han-2025-I", "v10-my-dinh-2-2026-I1"},
    {"tl-tsgn-19-tr8", "ck2-phuc-loi-2024-1-1"},
    {"sgk-7.4", "tl-tanso-12-tr6"},
    {"sgk-7.14", "v10-dong-da-de18-2025-I1", "tl-tanso-14-tr7"},
    {"ck2-phan-dinh-phung-2025-TN3", "ck2-phan-dinh-phung-2025-TN4", "ck2-phan-dinh-phung-2025-TN5",
     "ck2-phan-dinh-phung-2025-TN6", "sgk-7.22", "sgk-7.23", "sgk-7.24"},
    {"gk2-phuc-dong-2024-I-md2", "tl-tanso-22-tr9"},
    {"sgk-b23-hd2", "tl-tanso-15-tr7"},
    {"sgk-7.3", "tl-tanso-11-tr6"},
    {"gk2-ngoc-lam-2024-I1", "ck2-dai-ang-2025-I"},
    {"gk2-le-ngoc-han-2024-I1", "gk2-ban-mai-2025-1"},
    {"sgk-b22-lt1", "tl-tanso-4-tr3"},
    {"sgk-7.2", "tl-tanso-3-tr3"},
]


# bank_gate 18/11: hai cặp trùng NGUYÊN VĂN ⇒ như ch.VI (Thầy 16/11 "bốc lại"): không bốc bản nào,
# bản phái sinh (tài liệu Mathtech) ghi trang_thai "Bỏ" trong snapshot chuong-07.json
KHONG_BOC = {"sgk-b22-lt1", "tl-tanso-4-tr3", "sgk-7.8", "tl-tanso-16-tr8"}


KT_GOP = "inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/kiem-tra-chuong/ma-tran-va-dap-an-kiem-tra-chuong-vii-viii.json"


def ma_de_kt():
    """Mã câu đề KT gộp VII+VIII (dựng 16/11) dùng — phiếu không được dùng lại (18/11)."""
    import re
    p = Path(KT_GOP)
    if not p.exists():
        return set()
    return set(re.findall(r"\(((?:v10|ck2|gk2|sgk|so-hn|tl)-[A-Za-z0-9.-]+)\)", p.read_text()))


def _bank():
    return {r["ma"]: r for r in json.load(open(f"{GOC}.json"))["rows"]}


def loai_nguon(uu, ma):
    if ma.startswith("sgk-"):
        return "SGK"
    if uu.startswith("Ưu tiên 1"):
        return "Đề thi"
    return "Sách tham khảo"


def phut(vai, muc, n, nb):
    r = RATE[vai]
    if vai == "Ví dụ":
        return r["NB"] * nb if muc == "NB" else r[muc] * n
    return r["NB"] * nb + (r[muc] * n if muc != "NB" else 0)


def _gem():
    out = {}
    for f in GEM:
        if f.exists():
            d = json.loads(f.read_text())
            d = d.get("ket_qua") or d.get("json") or d
            out.update({x["ma"]: x for x in d.get("dong", [])})
    return out


def dung():
    bank, gem = _bank(), _gem()
    out, loi = [], []
    for (p, vai, dang, muc, n, nb, loai, ma, y, ht) in R:
        if ma not in bank:
            loi.append(f"thiếu mã trong ngân hàng: {ma}")
            continue
        q, g = bank[ma], gem.get(ma, {})
        T8 = list(g.get("T", [0] * 7)) + [0]
        diem = round(sum(t * w for t, w in zip(T8, W)) / (2 * sum(W)) * 10, 1) if g else None
        out.append({
            "phieu": p, "vai": vai, "dang": dang, "muc": muc, "so_y": n, "so_nb": nb,
            "phut": round(phut(vai, muc, n, nb), 1), "loai": loai, "ma": ma, "y": y,
            "hinh_thuc": ht, "de": q["de"], "nguon": q["nguon"],
            "loai_nguon": loai_nguon(q["uu"], ma), "T": T8, "diem": diem, "nguong": NGUONG[muc],
            "ket_luan": "" if diem is None else ("Đạt" if diem >= NGUONG[muc] else "Dưới ngưỡng"),
            "ly_do": g.get("ly_do", ""), "de_xuat": g.get("de_xuat", ""), "nghi_ngo": g.get("nghi_ngo", ""),
        })
    dem = collections.Counter(r["ma"] for r in out)
    loi += [f"bốc hai lần: {m}" for m, k in dem.items() if k > 1]
    chon = set(dem)
    loi += [f"bốc câu trùng nguyên văn (không bốc): {m}" for m in sorted(chon & KHONG_BOC)]
    loi += [f"câu đã nằm trong đề KT gộp VII+VIII: {m}" for m in sorted(chon & ma_de_kt())]
    for nhom in TRUNG:
        g = nhom & chon
        if len(g) > 1:
            loi.append(f"trùng đề: {sorted(g)}")
    return out, loi


def bao_cao(out):
    print(f"{'Phiếu':5} {'Vai':10} {'NB':>4} {'TH':>4} {'phút':>6}")
    for p in PHIEU:
        for vai in ("Ví dụ", "Trên lớp", "BTVN"):
            rs = [r for r in out if r["phieu"] == p and r["vai"] == vai]
            nb = sum(r["so_nb"] for r in rs if vai != "Ví dụ" or r["muc"] == "NB")
            th = sum(r["so_y"] for r in rs if r["muc"] == "TH")
            print(f"{p:5} {vai:10} {nb:4} {th:4} {sum(r['phut'] for r in rs):6.1f}")
            src = collections.Counter(r["loai_nguon"] for r in rs)
            print("      nguồn: " + ", ".join(f"{k} {v}/{len(rs)}" for k, v in src.items()))
        d = collections.Counter((r["dang"], r["vai"]) for r in out if r["phieu"] == p)
        print("      dạng×vai:", dict(sorted(d.items())))
    duoi = [(r["ma"], r["diem"]) for r in out if r["ket_luan"] == "Dưới ngưỡng"]
    if duoi:
        print("Dưới ngưỡng:", duoi)


if __name__ == "__main__":
    out, loi = dung()
    bao_cao(out)
    if loi:
        print("LỖI:\n  " + "\n  ".join(loi))
        sys.exit(1)
    if "--ghi" in sys.argv:
        json.dump(out, open(f"{GOC}/chon-cau.json", "w"), ensure_ascii=False, indent=1)
        print(f"Đã ghi {GOC}/chon-cau.json ({len(out)} dòng)")
