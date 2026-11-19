# Chọn câu chương X lớp 9C (19/11/2026) — làm lại theo quy trình mới (như ch.VI–VIII), giữ 2 buổi:
#   P1 = t32 trụ + nón + cầu (90′) · P2 = t33 luyện tập 45′ + kiểm tra chương X 45′.
# Dạng dạy = Thầy tick tab "Dạng Ch.X" (9103): C10-01 … C10-09; KHÔNG dạy C10-10, 11, 12.
#   C10-03 nón Pythagore, C10-04 tính ngược, C10-08 lật ngược chai (0–7% đề) ⇒ dạy trong khung, KHÔNG làm đích/VD.
# Luật: AGENTS.md "LUẬT HÌNH THỨC CÂU + BẢN CHẤT 40-40-20" — NB = MỘT bước · TH = bài gọn + gợi ý bước · VD = chỉ đề.
# Rate hình lớp 9 tầng C (config/tier_spec.json, Thầy duyệt 04/11): ví dụ 1,5/7/10 · trên lớp 2,5/10/16 · BTVN 2,2/8,7/14.
# Quỹ buổi hình 90′: ví dụ 25′ + trên lớp 55′ + giải lao 10′, BTVN 40′; P2 có KT 45′ ⇒ còn một nửa.
#   P1 trên lớp: 9 NB + 2 TH + 1 VD = 58,5′ (NB 38% / TH 34% / VD 27%) · ví dụ 27′ (gồm 1,5′ lý thuyết) · BTVN 41,5′.
#   P2 trên lớp: 5 NB + 1 VD = 28,5′ · ví dụ 15,5′ (tổng 44′ ≤ 40′ × 1,12 còn lại) · BTVN 44,5′ (tỉ lệ không soi: buổi có KT).
# Đích: P1 = Đoàn Thị Điểm CK2 2025–26 Bài 5 (khuôn ly + 5 bi của đề minh họa Sở, ý b hỏi BÁN KÍNH bi ⇒ VD);
#       P2 = Câu IV.1 đề Sở Hà Nội 2026 (xô 17 lần, làm tròn lên).
# Vai Claude: chốt mã câu / vai / mức / số câu. Gemini (scripts/gemini/viec_chon_cau_ch10_9c.py): chấm T1–T7 + lí do
# + đề xuất + nghi ngờ (cc-ch10-9c) và viết chữ TM (tm-ch10-9c-chu).
# Chạy:  python3 scripts/chon_cau_ch10_9c.py            (in bảng phút + kiểm trùng)
#        python3 scripts/chon_cau_ch10_9c.py --ghi      (ghi chon-cau.json)
import json, re, sys, collections
from pathlib import Path

GOC = "inputs/refs/ngan-hang-sheet/lop-9/hinh-hoc/chuong-10"
GEM = [Path("storage/gemini/xong/cc-ch10-9c.json"), Path("storage/gemini/xong/cc-ch10-9c-b.json"),
       Path("storage/gemini/xong/cc-ch10-9c-c.json")]  # b = chấm lại 3 dòng đổi 19/11
W = [3, 1, 2, 1, 2, 2, 2, 0]          # trọng số lớp C (T1..T8), tổng 13
NGUONG = {"NB": 5, "TH": 6, "VD": 7}
RATE = {  # phút/câu theo vai — hình lớp 9 tầng C
    "Ví dụ": {"NB": 1.5, "TH": 7.0, "VD": 10.0},
    "Trên lớp": {"NB": 2.5, "TH": 10.0, "VD": 16.0},
    "BTVN": {"NB": 2.2, "TH": 8.7, "VD": 14.0},
}
TN, TLN = "Trắc nghiệm A–D", "Trả lời ngắn"
TH_GY = "Tự luận + câu hỏi gợi ý bước"
VD_DE = "Chỉ đề, HS tự giải"
VDK = "Ví dụ điền khuyết"
PHIEU = {
    "P1": "Phiếu 1 — Bài 31, 32: Hình trụ, hình nón, hình cầu (t32, 90′)",
    "P2": "Phiếu 2 — Luyện tập chung + Bài tập cuối chương X (t33, 45′ + kiểm tra chương 45′)",
}

# (phiếu, vai, dạng, mức, số ý ở mức đó, số câu NB, loại §4b, mã, ý, hình thức)
# Mức NB: số ý = 0, "số câu NB" là số câu nhỏ. Mức TH/VD: "số câu NB" là câu NB tách từ chính đề đó.
R = [
# ======================= P1 — trụ, nón, cầu (90′) =======================
# --- Ví dụ (GV làm mẫu): mỗi khối một mẫu công thức + mẫu TH cho C10-03, C10-05, C10-07 ---
("P1","Ví dụ","C10-01","NB",0,1,"NB lẻ LT","sgk-b31-vd3","",VDK),          # đỉnh, đường cao, bán kính, đường sinh hình nón
("P1","Ví dụ","C10-02","NB",0,2,"NB lẻ LT","sgk-b32-vd3","",VDK),          # cầu R = 10: S = 400π, V = 4000π/3
("P1","Ví dụ","C10-05","TH",1,0,"TH lẻ LT","sgk-b31-lt2","a-b",VDK),       # thùng h 1,6 m r 0,5 m: Sxq ≈ 5,03 m², V ≈ 1257 lít
("P1","Ví dụ","C10-03","TH",1,0,"TH lẻ LT","sgk-b31-vd4","a-b",VDK),       # nón l 10 r 6: Sxq = 60π; h = 8 ⇒ V = 96π
("P1","Ví dụ","C10-07","TH",1,0,"TH lẻ LT","ck2-ngoc-thuy-2024-IV1","a-b",VDK),  # cốc r 5, nước 10 → dâng tới miệng 15: V đá = π·25·5
# --- Trên lớp: NB lẻ + NB kiến thức cũ ---
("P1","Trên lớp","C10-03","NB",0,1,"NB kiến thức cũ","sgk-10.18","CHỈ bước Pythagore",TLN),   # lớp 8: tính AC = 3 (Gemini 19/11: đề gốc 2 bước ⇒ phiếu chỉ hỏi AC)
("P1","Trên lớp","C10-01","NB",0,1,"NB lẻ LT","sgk-10.17","",TN),          # quay HCN quanh AB ⇒ bán kính đáy = AD
("P1","Trên lớp","C10-02","NB",0,1,"NB lẻ LT","ck2-phuc-dong-2024-902-IV1","",TLN),  # lon trụ d 6 h 11 (bẫy đường kính)
("P1","Trên lớp","C10-02","NB",0,1,"NB lẻ LT","ck2-be-van-dan-2025-IV1","",TLN),     # kem nón d 5,8 h 12,5 ⇒ V ≈ 110 cm³
("P1","Trên lớp","C10-02","NB",0,1,"NB lẻ LT","ck2-trung-vuong-2025-IV1","a",TLN),   # bóng d 22 ⇒ S ≈ 1519,76 cm²
("P1","Trên lớp","C10-04","NB",0,1,"NB lẻ LT","ck2-phuc-dong-2024-901-IV1","",TLN),  # V 1800 m³, dài 30 m ⇒ S đáy 60 m²
# --- Trên lớp: TH (bài gọn + gợi ý bước) và VD đích ---
("P1","Trên lớp","C10-05","TH",1,1,"TH lẻ LT","so-hn-2025-IV1","a-b",TH_GY),         # đề Sở 2025: Sxq thùng (NB tách) + nước đã dùng khi mực hạ 40 cm
("P1","Trên lớp","C10-03","TH",1,1,"TH lẻ LT","sgk-10.3","a-b",TH_GY),               # OA 8, SA 17: Sxq = 136π (NB tách); h = 15 ⇒ V = 320π
("P1","Trên lớp","C10-07","VD",1,1,"VD lẻ","ck2-doan-thi-diem-2025-5","a-b",VD_DE),  # ĐÍCH: ly d 5, nước 10 (NB tách) → 5 bi dâng tới miệng ⇒ bán kính bi
# --- BTVN ---
("P1","BTVN","C10-01","NB",0,1,"NB lẻ LT","sgk-b32-vd1","",TLN),
("P1","BTVN","C10-02","NB",0,1,"NB lẻ LT","gk2-tay-mo-3-2025-IV1","",TLN),          # thùng d 40 h 60 (bẫy đường kính)
("P1","BTVN","C10-02","NB",0,1,"NB lẻ LT","sgk-10.19","",TN),                       # mặt cầu đường kính 10 ⇒ 100π
("P1","BTVN","C10-02","NB",0,1,"NB lẻ LT","gk2-trung-vuong-2024-IV1","a",TLN),       # vỏ ốc quế nón r 2,5 h 6 ⇒ V = 39,25 cm³ (19/11 thay sgk-10.20 cho đủ 50% đề thi)
("P1","BTVN","C10-05","TH",1,1,"TH lẻ LT","ck2-xuan-dinh-2025-IV1","a-b",TH_GY),     # bồn 1,75 m r 0,5 m, tháo còn 1 m (khuôn Sở 2025 b)
("P1","BTVN","C10-03","TH",1,1,"TH lẻ LT","tl-tcnc-23-tr9","a-b",TH_GY),            # 19/11 Thầy đổi sgk-10.23 (giống VD4 77%): AB 5 BC 13 quay quanh AC ⇒ h 12, V = 100π ≈ 314,16
("P1","BTVN","C10-07","TH",1,1,"TH lẻ LT","ck2-thai-thinh-2025-IV1","a-b",TH_GY),    # cốc d 10, bi r 2 ⇒ nước dâng ≈ 4 mm
# ======================= P2 — luyện tập 45′ + KT chương X 45′ =======================
# --- Ví dụ ---
("P2","Ví dụ","C10-06","TH",1,1,"TH lẻ LT","ck2-hoai-duc-2024-IV1","a-b",VDK),      # thùng r 15 h 40 (ý a = NB mẫu, giàn giáo điền khuyết) → bồn r 60 h 150: đúng 60 thùng
("P2","Ví dụ","C10-09","TH",1,0,"TH lẻ LT","sgk-ltc-vd1","",VDK),                   # trụ r 1 h 2 khoan nón ⇒ còn 4π/3
# --- Trên lớp ---
("P2","Trên lớp","C10-06","NB",0,1,"NB kiến thức cũ","tl-dongda-39-tr17","a",TLN),  # lớp 7: thể tích hộp chữ nhật 8·12·20 = 1920 cm³
("P2","Trên lớp","C10-08","NB",0,1,"NB lẻ LT","tl-tcnc-20-tr8","",TLN),             # CHỈ bước đầu: lật ngược ⇒ phần trống là trụ cao 8 cm
("P2","Trên lớp","C10-09","NB",0,1,"NB lẻ LT","v10-my-dinh-2-2026-IV1","a",TLN),    # CHỈ bước tách khối: ly = trụ cao 3 + nửa cầu r 3
("P2","Trên lớp","C10-06","VD",1,2,"VD lẻ","so-hn-2026-IV1","a-b",VD_DE),            # ĐÍCH đề Sở 2026: Sxq xô + đổi 150 lít (2 NB tách) → số xô, làm tròn LÊN
# --- BTVN ---
("P2","BTVN","C10-06","TH",1,1,"TH lẻ LT","tl-hkgvao10-14-tr4","a-b",TH_GY),         # lọ r 7 h 8 đầy → lọ r 8 h 6: 392π > 384π ⇒ tràn (19/11 thay tl-hkgvao10-5: trùng cỡ xô r 15 h 40 với Hoài Đức)
("P2","BTVN","C10-09","TH",1,0,"TH lẻ LT","sgk-10.12","",TH_GY),                    # vòng bi: hiệu hai trụ r 7, r 5, cao 10 ⇒ 240π
("P2","BTVN","C10-09","TH",1,0,"TH lẻ LT","tl-hkgvao10-12-tr4","",TH_GY),           # quả dọi: trụ d 3,6 h 4 + nón h 3,5
("P2","BTVN","C10-08","TH",1,1,"TH lẻ LT","tl-dongda-54-tr23","a-b",TH_GY),          # chai d 6, nước 12, lật ngược trống 9 ⇒ V = 189π ≈ 594 cm³ (19/11 hạ VD → TH: C10-08 không làm VD)
]

# Bài gốc trùng số liệu / cùng khung (mã khác) — mỗi nhóm bốc tối đa một. Dò tay 19/11 trên bảng ứng viên.
TRUNG = [
    {"so-hn-minhhoa-IV1", "tl-hkgvao10-7-tr2", "tl-mhhn2018-4-tr3", "ck2-dai-ang-2025-IV1",
     "ck2-doan-thi-diem-2025-5", "tl-tulap26-7-tr2"},                       # ly d 5, nước 10 của đề minh họa
    {"so-hn-2025-IV1", "tl-cthn2526-4-tr2", "tl-hkgvao10-21-tr6"},           # Sở 2025 + bản chép + cùng khuôn ý b
    {"so-hn-2026-IV1", "tl-cthn2627-4-tr2"},                                 # Sở 2026 + bản chép
    {"ck2-xuan-dinh-2025-IV1", "ck2-thach-that-2024-4-1"},                   # bồn 1,75 m r 0,5 m
    {"ck2-hoai-duc-2024-IV1", "tl-hkgvao10-15-tr5"},
    {"v10-thanh-oai-l2-2025-IV1", "tl-hkgvao10-3-tr1"},
    {"tl-dongda-4-tr2", "tl-hkgvao10-8-tr3", "sgk-ltc-vd2", "tl-dongda-74-tr32"},  # hộp 3 bóng tennis
    {"tl-dongda-44-tr19", "tl-hkgvao10-9-tr3"},
    {"tl-hkgvao10-2-tr1", "v10-chuong-my-l5-2025-IV1"},
    {"gk2-ba-dinh-2024-IV1", "gk2-ban-mai-2025-4.1"},
    {"sgk-10.3", "tl-tcnc-27-tr10"}, {"sgk-10.2", "tl-tcnc-6-tr5"}, {"sgk-10.8", "tl-tcnc-53-tr16"},
    {"sgk-10.15", "tl-tcnc-67-tr19"}, {"tl-dongda-59-tr25", "tl-tcnc-64-tr18"}, {"sgk-10.5", "tl-tcnc-40-tr13"},
    {"sgk-10.13", "tl-tcnc-39-tr13"}, {"sgk-10.6", "tl-tcnc-29-tr10"}, {"sgk-10.14", "tl-tcnc-69-tr19"},
    {"sgk-10.9", "tl-tcnc-68-tr19"}, {"ck2-phuc-dong-2024-901-IV1", "tl-tcnc-14-tr7"},
    {"tl-dongda-49-tr21", "tl-hkgvao10-10-tr3"}, {"tl-hkgvao10-14-tr4", "tl-dongda-64-tr28"},
    {"ck2-hoai-duc-2024-IV1", "tl-hkgvao10-5-tr2"},                          # cùng thùng/xô r 15 h 40 (Gemini 19/11)
    {"ck2-lomonoxop-2024-IV1", "sgk-b31-vd2"},                               # thùng rác r 11 h 30
    {"ck2-trung-vuong-2025-IV1", "sgk-b32-vdg1"},                            # bóng đường kính 22 cm
    {"tl-hkgvao10-4-tr1", "tl-unghoa25l3-4-tr1"},                            # 5 bi r 1, cốc d 6
    {"tl-hkgvao10-18-tr5", "tl-dongda-5-tr2"},                               # thúng gạo nửa cầu d 50 + nón
    {"tl-dongda-9-tr4", "ck2-be-van-dan-2025-IV1"},                          # kem ốc quế nón (cùng bối cảnh)
]

# Đề kiểm tra chương X cũ (12/11, kiem-tra-chuong/) — phiếu không bốc lại câu của đề, phòng khi Thầy giữ đề.
MA_DE_KT_CU = {"sgk-10.1", "sgk-b31-lt4", "sgk-10.7", "sgk-10.24", "ck2-le-hong-phong-2025-V1",
               "tl-dongda-14-tr6", "ck2-nguyen-du-2025-IV1"}


# Thầy duyệt tab 9104 ngày 19/11/2026: cả 31 dòng "Hay"; ghi chú cột AC (áp khi dựng phiếu)
THAY_DUYET = "Hay"
GHI_CHU_THAY = {"tl-dongda-54-tr23": "Nhớ vẽ đầy đủ hình nhé",
                "tl-tcnc-23-tr9": "Thay sgk-10.23 (Phiếu 1: giống Ví dụ 4 SGK, Thầy 19/11 \"đổi đi\")"}   # hình a (nước cao 12) + hình b (lật ngược, trống 9)


def _bank():
    b = {r["ma"]: r for r in json.load(open(f"{GOC}.json"))["rows"]}
    for r in json.load(open(f"{GOC}/bo-sung-so.json"))["rows"]:   # 3 câu IV.1 đề Sở (tab thiếu)
        b[r["ma"]] = r
    return b


def loai_nguon(uu, ma):
    if ma.startswith("sgk-"):
        return "SGK"
    if ma.startswith("so-hn-") or uu.startswith("Ưu tiên 1"):
        return "Đề thi"
    return "Sách tham khảo"


def phut(vai, muc, n, nb):
    r = RATE[vai]
    if vai == "Ví dụ":   # ví dụ TH/VD có ý a mẫu NB (giàn giáo điền khuyết) thì cộng phút NB
        return r["NB"] * nb if muc == "NB" else r[muc] * n + r["NB"] * nb
    return r["NB"] * nb + (r[muc] * n if muc != "NB" else 0)


def _gem():
    out = {}
    for f in GEM:
        if f.exists():
            d = json.loads(f.read_text())
            d = d.get("ket_qua") or d.get("structured_output") or d.get("json") or d
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
            "loai_nguon": loai_nguon(q.get("uu", ""), ma), "T": T8, "diem": diem, "nguong": NGUONG[muc],
            "ket_luan": "" if diem is None else ("Đạt" if diem >= NGUONG[muc] else "Dưới ngưỡng"),
            "thay_duyet": THAY_DUYET, "ghi_chu_thay": GHI_CHU_THAY.get(ma, ""),
            "ly_do": g.get("ly_do", ""), "de_xuat": g.get("de_xuat", ""), "nghi_ngo": g.get("nghi_ngo", ""),
        })
    dem = collections.Counter(r["ma"] for r in out)
    loi += [f"bốc hai lần: {m}" for m, k in dem.items() if k > 1]
    chon = set(dem)
    loi += [f"câu đã nằm trong đề KT chương X cũ: {m}" for m in sorted(chon & MA_DE_KT_CU)]
    for nhom in TRUNG:
        g = nhom & chon
        if len(g) > 1:
            loi.append(f"trùng đề: {sorted(g)}")
    loi += [f"dạng không dạy: {r['ma']} {r['dang']}" for r in out if r["dang"] in ("C10-10", "C10-11", "C10-12")]
    loi += [f"C10-03/04/08 không làm VD: {r['ma']}" for r in out
            if r["dang"] in ("C10-03", "C10-04", "C10-08") and r["muc"] == "VD" and r["vai"] == "Trên lớp"]
    return out, loi


def bao_cao(out):
    print(f"{'Phiếu':5} {'Vai':10} {'NB':>4} {'TH':>4} {'VD':>4} {'phút':>6}")
    for p in PHIEU:
        for vai in ("Ví dụ", "Trên lớp", "BTVN"):
            rs = [r for r in out if r["phieu"] == p and r["vai"] == vai]
            nb = sum(r["so_nb"] for r in rs if vai != "Ví dụ" or r["muc"] == "NB")
            th = sum(r["so_y"] for r in rs if r["muc"] == "TH")
            vd = sum(r["so_y"] for r in rs if r["muc"] == "VD")
            tong = sum(r["phut"] for r in rs)
            print(f"{p:5} {vai:10} {nb:4} {th:4} {vd:4} {tong:6.1f}")
            if vai == "Trên lớp" and tong:
                rt = RATE[vai]
                print(f"      tỉ lệ phút NB {nb*rt['NB']/tong*100:.0f}% · TH {th*rt['TH']/tong*100:.0f}% · "
                      f"VD {vd*rt['VD']/tong*100:.0f}%")
            src = collections.Counter(r["loai_nguon"] for r in rs)
            print("      nguồn: " + ", ".join(f"{k} {v}/{len(rs)}" for k, v in src.items()))
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
