#!/usr/bin/env python3
"""Claude soát đầu ra Gemini dx-ch6-9c-* (16/11/2026): ghi đè các đề xuất thợ hiểu sai luật,
rồi xuất mảng giá trị cho tab Sheets (AD:AE đề xuất, AA lí do chấm) theo thứ tự mã cột J.
    python3 scripts/gom_de_xuat_ch6_9c_soat.py <file-ma-cot-J.json>   (in JSON {AD_AE, AA})"""
import glob, json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
GOC = REPO / "inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-06"
# (đề xuất, lí do) — lí do Claude sửa sau khi soát
SUA = {
    "sgk-b19-vd7": ("Không hay", "ĐÃ BỎ khỏi chọn câu: đề bắt buộc công thức nghiệm thu gọn Δ′ (Thầy bỏ 16/11)."),
    # chỉ vướng Δ′ ở lí do chấm — đã đổi sang Δ nên không còn vấn đề
    "ck2-ba-dinh-2024-II2": ("Hay", "Đề CK2 nghiệm chứa căn, Δ = 92; câu NB tách đổi thành tính Δ."),
    "gk2-dong-anh-2025-12": ("Hay", "Đề GK2 hai ý, Δ = 40; câu NB tách đổi thành tính Δ."),
    "gk2-nguyen-truong-to-2025-2": ("Hay", "Mẫu chứng minh luôn có nghiệm, Δ = 4(m − 2)², bẫy ≥ với >."),
    "tl-ptb2-08-tr6": ("Hay", "Nghiệm kép, Δ = 16(m² − m − 6) = 0 cho m = 3, m = −2 đẹp."),
    "tl-ptb2-18-tr6": ("Hay", "Hai nghiệm phân biệt, Δ = 24m + 24 > 0 ⇒ m > −1, gọn."),
    "gk2-mai-dich-2024-32": ("Hay", "BTVN chuẩn C6-11, Δ = 8m + 24; m = −5/2 thỏa điều kiện."),
    "v10-thanh-oai-l2-2025-III3": ("Hay", "BTVN chuẩn C6-11, Δ = 4(m − 2)²; m = 0 hoặc m = 2."),
    # thợ hiểu sai luật nhẩm nghiệm: Thầy 16/11 cho nhẩm nghiệm là câu NB nghiệm đẹp
    "sgk-6.24": ("Hay", "Nhẩm a + b + c = 0, a − b + c = 0 là câu NB nghiệm đẹp (Thầy 16/11)."),
    "tl-viete-47-tr8": ("Cân nhắc", "BTVN P1 đã có sgk-b20-vd2, sgk-b20-hd3 nhẩm nghiệm; thêm 3 câu là nhiều."),
    "sgk-b20-vd2": ("Không hay", "Ý a trùng PT x² − 6x + 5 = 0 với gk2-my-dinh-2-2025-21 (cùng BTVN P1)."),
    # P5 là luyện tập chung: C6-08 đã học ở P2
    "v10-luyen-de-23-2025-III3": ("Hay", "Luyện tập chung ôn C6-08 (đã học ở P2), nghiệm 3 − √6."),
    # Claude giải lại: x₁ = x₂ = −1 ⇒ m = 1 nhưng Δ = 4 − 4m = 0, không có m
    "tl-viete-39-tr6": ("Không hay", "Không có m: giải ra x₁ = x₂ = −1, m = 1 nhưng Δ = 0 (cần phân biệt)."),
}
def main():
    ma_j = [r[0] for r in json.load(open(sys.argv[1]))]
    gm = {}
    for f in glob.glob(str(REPO / "storage/gemini/xong/dx-ch6-9c-P*.json")):
        for d in json.loads(Path(f).read_text())["ket_qua"]["dong"]:
            gm[d["ma"]] = (d["de_xuat"], d["ly_do"].strip())
    gm.update(SUA)
    cc = {r["ma"]: r["ly_do"] for r in json.loads((GOC / "chon-cau.json").read_text())}
    ad = [list(gm[m]) for m in ma_j]
    aa = [[cc.get(m, "Đã bỏ (Δ′).")] for m in ma_j]
    json.dump({"AD_AE": ad, "AA": aa}, sys.stdout, ensure_ascii=False)
    import collections; print("\n", collections.Counter(a[0] for a in ad), file=sys.stderr)
main()
