#!/usr/bin/env python3
"""Việc Gemini: PHỦ DẠNG cho 3 đề ÔN TẬP CK1 lớp 6 (phu_dang_gate --khoi 6 đang ❌ 10 lỗi).

Thầy chốt 13/11/2026 khung đề ÔN (đề chính thức giữ nguyên):
  Phần I trắc nghiệm 10 câu × 0,25 = 2,5đ · Bài 1 còn 3 ý × 0,5 = 1,5đ (bỏ ý trùng dạng) · Bài 2 tìm x 1,5đ ·
  Bài 3 (1,5đ) = 3.1 thực tế số nguyên 0,5 + 3.2 BCNN/ƯCLN 1,0 (đề thật: Cụm 14, Lômônôxốp, Phúc Đồng,
  Ngọc Lâm 24-25, Nguyễn Bỉnh Khiêm) · Bài 4 2,5đ · Bài 5 0,5đ.
Claude chốt câu (ngân hàng 24 đề, bản ghi); Gemini chép nguyên văn + giải; Claude vá scripts/de_ck1_lop6.py.

    .venv/bin/python scripts/gemini/viec_phu_dang_on_ck1_lop6.py
    python3 scripts/gemini/tho.py --song-song 4      (chỉ chạy các việc pd6-*)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts/gemini"))
from viec_chep_cau import MAU  # noqa: E402  (khuôn "chép nguyên văn + giải" đã chạy ổn ở lớp 7)

BG = REPO / "inputs/refs/ngan-hang-sheet/lop-6/ck1/ban-ghi"
PDF = REPO / "inputs/refs/de-thi/lop-6/cuoi-ki-1"
HANG_DOI = REPO / "storage/gemini/hang-doi"

# mã đề bản ghi -> {nhãn ý: (đề ôn, vị trí trong đề mới, điểm trong đề mới)}
CAU = {
    "l6-ck1-2526-aimo": {"II.2c": ("on1", "Bài 2c — tìm x có luỹ thừa", 0.5)},
    "l6-ck1-2526-cum14": {"II.3.1": ("on1", "Bài 3.1 — thực tế số nguyên", 0.5)},
    "l6-ck1-2526-lyson": {"I.4": ("on1", "trắc nghiệm — rút gọn phân số", 0.25)},
    "l6-ck1-2526-nguyenbinhkhiem": {"I.1": ("on1", "trắc nghiệm — luỹ thừa", 0.25)},
    "l6-ck1-2425-phucdien": {"I.4": ("on1", "trắc nghiệm — ước số nguyên", 0.25)},
    "l6-ck1-2425-ngoclam": {"II.3.2": ("on2", "Bài 3.1 — thực tế số nguyên", 0.5)},
    "l6-ck1-2425-phucdong": {"I.6": ("on2", "trắc nghiệm — ước chung", 0.25),
                             "I.3": ("on2", "trắc nghiệm — luỹ thừa", 0.25)},
    "l6-ck1-2425-phandinhgiot": {"1a": ("on3", "Bài 1a — cộng trừ số nguyên, tính hợp lí", 0.5),
                                 "2a": ("on3", "Bài 2a — tìm số nguyên x", 0.5)},
    "l6-ck1-2425-banmai": {"II.6": ("on3", "Bài 3.1 — thực tế số nguyên (đề gốc 1,0đ, đề mới CHỈ 0,5đ)", 0.5),
                           "I.5": ("on3", "trắc nghiệm — tổng các số nguyên trong khoảng", 0.25)},
    "l6-ck1-2425-quocoai": {"I.1": ("on3", "trắc nghiệm — tập hợp", 0.25)},
    "l6-ck1-2425-lomonoxop": {"I.4": ("on3", "trắc nghiệm — dấu hiệu chia hết", 0.25)},
    "l6-ck1-2526-giangbien": {"I.3": ("on3", "trắc nghiệm — phân tích ra thừa số nguyên tố", 0.25)},
}

THEM = r"""
BỔ SUNG CHO ĐỀ ÔN TẬP LỚP 6 (giáo viên đã chốt — ưu tiên hơn quy tắc 5 ở trên về điểm):
- Mỗi ý trên được đưa vào một ĐỀ ÔN MỚI với số điểm ghi trong ngoặc "điểm trong đề mới". Tự luận: chia
  "diem" các bước theo SỐ ĐIỂM MỚI (bội của 0,25, cộng lại đúng bằng điểm mới), dù HDC gốc chấm khác.
- Lời giải trình bày như bài thi lớp 6: mỗi dòng một bước, dòng cuối "Vậy …". Không văn nói, không xưng
  hô ("em", "ta thấy dễ dàng"), không viết tắt. Số nguyên âm trong phép tính đặt trong ngoặc: $(-9)+4$.
  Nhiệt độ viết $-5^\circ$C. Số có từ 4 chữ số trở lên ngăn nhóm bằng \, (ví dụ $3\,143$).
- Trắc nghiệm: chép đủ 4 phương án đúng thứ tự in trong đề; "dap_an" là chữ cái đúng THEO ĐỀ IN.
  Nếu nhiều phương án cùng đúng / đề in sai ⇒ ghi rõ vào "can_soat", KHÔNG tự sửa đề.
- TỰ TÍNH LẠI mọi đáp số; HDC sai ⇒ theo đề in, ghi "can_soat".
"""


def main() -> None:
    HANG_DOI.mkdir(parents=True, exist_ok=True)
    n = 0
    for ma, cs in CAU.items():
        bg = json.loads((BG / f"{ma}.json").read_text())
        nhan = {q["cau"]: q for q in bg["cau"]}
        thieu = set(cs) - set(nhan)
        assert not thieu, f"{ma}: nhãn không có trong bản ghi {thieu}"
        pdf = PDF / bg["pdf"]
        assert pdf.exists(), pdf
        ds = "\n".join(f"  - {c}: (tóm tắt để nhận ra) {nhan[c]['nd'][:160]} — dùng ở {v[1]}, "
                       f"điểm trong đề mới: {str(v[2]).replace('.', ',')}" for c, v in cs.items())
        viec = {
            "id": f"pd6-{ma}", "model": "gemini-3.8-flash-high",
            "prompt": MAU.format(lop="6", txt=pdf.stem + ".txt", ds=ds, ma=ma) + THEM,
            "files": [str(pdf.relative_to(REPO))], "render": True,
            "schema": "scripts/gemini/schema/chep-cau.json", "timeout": "1200s",
            "meta": {"loai": "chep", "de": ma, "cau": sorted(cs), "phu_dang": {c: v[0] for c, v in cs.items()}},
        }
        (HANG_DOI / f"{viec['id']}.json").write_text(json.dumps(viec, ensure_ascii=False, indent=1))
        n += len(cs)
        print(f"ghi pd6-{ma}: {len(cs)} ý")
    print(f"{len(CAU)} việc chép, {n} ý")


if __name__ == "__main__":
    main()
