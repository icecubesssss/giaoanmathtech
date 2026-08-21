"""Seed band (NB/TH/VD/VDC) + phut (thời gian HS làm, ước) cho ngân hàng đề lớp 9.

RUBRIC (AI đọc 252 câu rồi đúc kết — Thầy rà lại qua cờ `_band_auto`/`_phut_auto`):

  band = MAX( sàn-theo-DẠNG , band-theo-do_kho ), chặn trần cho dạng "nhẹ".
    • sàn-theo-DẠNG: bản chất nhận thức của LOẠI bài (cực trị→VDC, câu phụ rút gọn
      →VD floor, thực tế lập hệ→TH floor…) — phần phán đoán từ đọc đề.
    • band-theo-do_kho: 1→NB 2→TH 3→VD 4→VDC (độ khó người ra đề gắn).
    ⇒ lấy mức CAO hơn: câu cực trị 0,5đ vẫn VDC; rút gọn dù dk cao vẫn ≤TH.

  phut = theo band (NB4/TH8/VD12/VDC14), điều chỉnh cho dạng:
    • thực tế lập hệ/pt: dài hơn (TH 11′, VD 14′).
    • tỉ số lượng giác thực tế / hình tròn thực tế: nhanh (1 phép, TH 6′).
    • VDC (cực trị/BĐT/hình khó): GIỮ 13–14′ DÙ điểm thấp — đây là điểm mấu chốt
      mà cách suy-giờ-từ-điểm bỏ sót.

Chạy:  python -m scripts.seed_exam_bands > /tmp/j.json && python -m scripts.exam_annotate apply /tmp/j.json
"""
from __future__ import annotations

import json
import sys

from scripts.exam_annotate import _cau_id, _exam_files, _load, EXAMS_GLOB

_LADDER = ["NB", "TH", "VD", "VDC"]
_DOKHO_BAND = {1: "NB", 2: "TH", 3: "VD", 4: "VDC"}

# Sàn band theo DẠNG (bản chất nhận thức của loại bài).
DANG_FLOOR = {
    "DS-PT-QUYVE": "NB", "DS-PT-BAC2": "NB", "DS-PT-PHANTHUC": "TH",
    "DS-PT-VO_TY": "TH", "DS-PT-VO_TY-NANGCAO": "VDC",
    "DS-BPT-GIAI": "NB", "DS-BPT-QUYVE": "TH",
    "DS-HEPT-GIAI": "NB", "DS-HPT-QUYVE": "TH",
    "DS-CAN-TINH-RUTGON": "NB", "DS-CAN-CAUPHU": "VD",
    "DS-THUCTE-LAPHE": "TH", "DS-THUCTE-LAPPT": "TH", "DS-THUCTE-LAPPT-BPT": "TH",
    "DS-BPT-THUCTE": "TH", "DS-DT-THUCTE": "TH", "DS-PT-THUCTE": "VDC",
    "DS-BDT-CM": "NB", "DS-CUCTRI": "VDC", "DS-BĐT-COSI": "VDC",
    "DS-THONGKE": "NB", "DS-XACSUAT": "TH",
    "TK-TANSO-BIEUDO": "NB", "TK-XACSUAT-TINH": "TH",
    # Chương VII (tần số) — Sở xếp cả Câu I.1 vào cột NHẬN BIẾT của ma trận.
    "TK-TANSO-DOC": "NB", "TK-TANSO-LAP": "TH", "TK-TANSO-VE": "TH",
    "TK-TANSO-SUYLUAN": "NB",
    # Chương VIII (xác suất) — Câu I.2 của Sở là NB/TH, KHÔNG có ý vận dụng.
    "TK-KHONGGIANMAU": "NB", "TK-XACSUAT-2HD": "VD",
    "HH-TSLG-THUCTE": "TH", "HH-TSLG-TINH": "TH", "HH-TSLG-CM": "VD",
    "HH-HTL-THUCTE": "TH", "HH-TRON-THUCTE": "NB", "HH-TRON-CM": "TH",
    "HH-TRON-CUNG": "VD",
}
# Trần band cho dạng "nhẹ" (do_kho cao cũng không vượt) — rút gọn/tính/đọc số liệu.
DANG_CAP = {
    "DS-CAN-TINH-RUTGON": "TH", "HH-TRON-THUCTE": "TH",
    "DS-THONGKE": "TH", "TK-TANSO-BIEUDO": "TH", "DS-DT-THUCTE": "VD",
    "TK-TANSO-DOC": "TH", "TK-TANSO-LAP": "TH", "TK-TANSO-VE": "TH",
    "TK-TANSO-SUYLUAN": "VD",
    "TK-XACSUAT-TINH": "TH", "TK-KHONGGIANMAU": "NB",
}

_PHUT_BAND = {"NB": 4, "TH": 8, "VD": 12, "VDC": 14}
# Override phút theo (dạng, band) — phản ánh dạng dài/ngắn từ đọc đề.
_PHUT_DANG = {
    ("DS-THUCTE-LAPHE", "TH"): 11, ("DS-THUCTE-LAPHE", "VD"): 14,
    ("DS-THUCTE-LAPPT", "TH"): 11, ("DS-THUCTE-LAPPT", "VD"): 14,
    ("DS-THUCTE-LAPPT-BPT", "TH"): 10, ("DS-THUCTE-LAPPT-BPT", "VD"): 13,
    ("DS-BPT-THUCTE", "TH"): 10, ("DS-BPT-THUCTE", "VD"): 12,
    ("HH-TSLG-THUCTE", "TH"): 6, ("HH-TSLG-THUCTE", "VD"): 8,
    ("HH-HTL-THUCTE", "TH"): 7,
    ("HH-TRON-THUCTE", "NB"): 5, ("HH-TRON-THUCTE", "TH"): 6,
    ("HH-TRON-CM", "TH"): 6, ("HH-TRON-CM", "VD"): 10, ("HH-TRON-CM", "VDC"): 13,
    ("HH-TSLG-CM", "VD"): 10, ("HH-TSLG-CM", "VDC"): 12,
    ("HH-TSLG-TINH", "TH"): 8, ("HH-TSLG-TINH", "VD"): 10,
    ("DS-CAN-CAUPHU", "VD"): 8,
    ("DS-HEPT-GIAI", "NB"): 5,
    # Đọc bảng/biểu đồ tần số: NB là một phép chia, TH là lập cả bảng.
    ("TK-TANSO-DOC", "NB"): 4, ("TK-TANSO-DOC", "TH"): 6,
    ("TK-TANSO-LAP", "TH"): 8, ("TK-TANSO-VE", "TH"): 8,
    ("TK-TANSO-SUYLUAN", "NB"): 4, ("TK-TANSO-SUYLUAN", "TH"): 8,
    ("TK-TANSO-SUYLUAN", "VD"): 10,
    # Xác suất: NB là đếm thẳng một điều kiện; TH phải tự liệt kê tập nền;
    # hai hành động phải lập cả bảng nên lâu hơn.
    ("TK-KHONGGIANMAU", "NB"): 3,
    ("TK-XACSUAT-TINH", "NB"): 4, ("TK-XACSUAT-TINH", "TH"): 6,
    ("TK-XACSUAT-2HD", "TH"): 8, ("TK-XACSUAT-2HD", "VD"): 10,
}
# Override band/phut theo từng câu (đọc đề thấy đặc biệt so với dạng/do_kho).
ID_OVERRIDE: dict[str, dict] = {
    # "làm chung – làm riêng" chia giai đoạn → vận dụng, tốn giờ.
    "ck1-ai-mo-3-1": {"phut": 14}, "gk1-phu-dien-3-1": {"phut": 14},
    # dòng nước (xuôi/ngược) → vận dụng nhiều bước.
    "ck1-trung-vuong-II2": {"phut": 14},
    # hệ đặt ẩn phụ.
    "gk1-dvhau-1-4": {"band": "VD", "phut": 10},
    # giải tam giác + đường cao nhiều ý nhỏ trong 1 câu.
}


def _higher(a: str, b: str) -> str:
    return a if _LADDER.index(a) >= _LADDER.index(b) else b


def _cap(b: str, cap: str | None) -> str:
    return b if cap is None or _LADDER.index(b) <= _LADDER.index(cap) else cap


def judge(dangs: list[str], do_kho: int) -> tuple[str, float]:
    dk_band = _DOKHO_BAND.get(do_kho or 2, "TH")
    band = "NB"
    cap = None
    for d in dangs or []:
        floor = DANG_FLOOR.get(d, "TH")
        band = _higher(band, _higher(floor, dk_band))
        if d in DANG_CAP:  # trần của dạng nhẹ nhất quyết định
            cap = DANG_CAP[d] if cap is None else _higher(cap, DANG_CAP[d])
    if cap and all(d in DANG_CAP for d in (dangs or [])):
        band = _cap(band, cap)
    phut = _PHUT_BAND[band]
    for d in dangs or []:
        if (d, band) in _PHUT_DANG:
            phut = _PHUT_DANG[(d, band)]
            break
    return band, float(phut)


def main() -> int:
    out: dict[str, dict] = {}
    for f in _exam_files(EXAMS_GLOB):
        for c in _load(f).get("cau", []):
            cid = _cau_id(f.stem, c)
            band, phut = judge(c.get("dang") or [], c.get("do_kho"))
            ov = ID_OVERRIDE.get(cid, {})
            out[cid] = {"band": ov.get("band", band), "phut": ov.get("phut", phut)}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
