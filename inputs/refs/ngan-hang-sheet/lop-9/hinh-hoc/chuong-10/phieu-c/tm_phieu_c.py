"""Cập nhật dòng phiếu C trong thuyết minh chương X 9C (12/11/2026) cho khớp phiếu C dựng lại.

Thầy chốt: đích = Câu IV.1 đề 2026 trọn; hiệu hai khối + ghép khối chỉ ở BTVN. Chạy từ gốc repo.
"""
import json
from pathlib import Path

P = Path("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/thuyet-minh.json")
d = json.loads(P.read_text(encoding="utf-8"))
c = next(p for p in d["phieu"] if p["code"] == "C")
c["title"] = "Buổi 2 — Luyện tập chung (45 phút) $+$ Kiểm tra chương X (45 phút)"
c["dich"] = "Câu IV.1 đề chính thức Vào 10 năm 2026 (xô nước hình trụ: ý a $S_{xq}$, ý b múc $80\\%$ thể tích xô, đếm số xô, làm tròn LÊN)"
c["kiem_tra_phut"] = 45
c["rows"] = [
    {"band": "NB", "loai": "NB lẻ LT", "lythuyet": 1, "vidu": 0, "onclass": 2, "btvn": 2,
     "dang": "Chọn đúng công thức trong sáu công thức của chương (trắc nghiệm) — bẫy đường kính ở mặt cầu, $S_{xq}$ hình nón",
     "source_refs": ["sgk-10.19", "sgk-10.20", "sgk-10.18", "sgk-10.21"], "decompose": "none", "hinh_san": True},
    {"band": "NB", "loai": "NB tách TH", "lythuyet": 0, "vidu": 0, "onclass": 1, "btvn": 1,
     "dang": "Điền khuyết bài giải thể tích hình trụ (đề cho ĐƯỜNG KÍNH, chiều cao theo mực nước) — tách từ ý a Câu IV.1",
     "source_refs": ["ck2-thai-thinh-2025-IV1", "ck2-lomonoxop-2024-IV1"], "decompose": "none", "hinh_san": True,
     "gian_giao": "dien-khuyet"},
    {"band": "NB", "loai": "NB tách TH", "lythuyet": 1, "vidu": 1, "onclass": 1, "btvn": 1,
     "dang": "Chiều cao lấy theo PHẦN NƯỚC ĐANG XÉT: mực nước cho bằng phân số, phần còn trống, độ hạ của mực nước (điền khuyết; về nhà HS tự vẽ phác bồn, tô phần nước đã tháo)",
     "source_refs": ["ck2-mai-dich-2025-4.1", "ck2-pgd-hai-ba-trung-2024-IV1", "ck2-xuan-dinh-2025-IV1"],
     "decompose": "none", "hinh_san": True, "gian_giao": "ve-hinh", "ve_hinh": {"onclass": 0, "btvn": 1}},
    {"band": "NB", "loai": "NB kiến thức cũ", "lythuyet": 1, "vidu": 0, "onclass": 1, "btvn": 0,
     "dang": "Ôn Lớp 6: phần trăm của một số, đổi lít $\\leftrightarrow$ cm$^3$, chia rồi làm tròn LÊN — bước của ý b đề 2026",
     "source_refs": ["tl-cthn2627-4-tr2.b"], "decompose": "none"},
    {"band": "TH", "loai": "TH lẻ LT", "lythuyet": 0, "vidu": 1, "onclass": 1, "btvn": 1,
     "dang": "Khuôn ĐẾM SỐ LẦN / SO SÁNH THỂ TÍCH: thể tích một lần (có phần trăm), cùng đơn vị, chia, làm tròn LÊN — ví dụ mẫu Minh Trí (Hoài Đức), trên lớp Láng Thượng, về nhà Cầu Diễn",
     "source_refs": ["ck2-hoai-duc-2024-IV1", "tl-dongda-39-tr17", "ck2-cau-dien-2025-IV1"], "decompose": "none"},
    {"band": "TH", "loai": "TH ghép bài", "lythuyet": 0, "vidu": 0, "onclass": 0, "btvn": 1,
     "dang": "Khuôn HIỆU HAI KHỐI TRỤ (đề trường, chỉ BTVN): bê tông $=$ khối trụ ngoài $-$ lòng bể, so với số tiền có",
     "source_refs": ["ck2-pgd-ba-dinh-2024-III"], "decompose": "none"},
    {"band": "TH", "loai": "TH ghép bài", "lythuyet": 0, "vidu": 0, "onclass": 0, "btvn": 1,
     "dang": "Khuôn GHÉP HAI KHỐI (đề trường, chỉ BTVN): kho ngũ cốc $=$ hình trụ $+$ nửa hình cầu",
     "source_refs": ["tl-tcnc-64-tr18"], "decompose": "none"},
    {"band": "VD", "loai": "VD lẻ", "lythuyet": 0, "vidu": 0, "onclass": 1, "btvn": 1,
     "dang": "Trọn Câu IV.1 đề chính thức Vào 10 năm 2026 (xô nước, ý b đếm số xô) — chấm chéo 0,5 $+$ 0,5; về nhà trọn đề Văn Điển (vòi chảy đầy bể)",
     "source_refs": ["tl-cthn2627-4-tr2", "ck2-van-dien-2024-IV1"], "decompose": "vd", "hinh_san": True},
]
# Dòng thời lượng cũ "Tổng 3 ca" và "hết chương trình ở tuần 30" là của kế hoạch trước 12/11 — bỏ.
d["thoiluong"] = [t for t in d["thoiluong"]
                  if "Tổng 3 ca" not in t and "hết chương trình ở tuần 30" not in t]
P.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", len(c["rows"]), "dòng")
