#!/usr/bin/env python3
"""TẦN SUẤT VDC theo chương — đếm ở ĐÚNG HAI VỊ TRÍ, mỗi bài chỉ tính CÂU CUỐI.

VÌ SAO (Thầy chốt 04/09/2026): bản 0.3 của `config/ban_do_vd_vdc.json` ghi `so_cau_vdc`
là SỐ CÂU thô — đếm cả những ý giữa bài hình. Thầy yêu cầu "bài VDC thì chỉ câu cuối mới
tính thôi", và muốn xếp ưu tiên theo TẦN SUẤT: chương nào có câu VDC xuất hiện trong
NHIỀU ĐỀ hơn thì phiếu tầng B dành nhiều thời lượng VDC hơn.

Cách đếm (không suy diễn):
  * Mẫu HK1  = 21 đề lớp 9 ĐỦ 9–10,5 điểm trong `inputs/refs/de-thi/lop-9/exams/`
               (24 file còn lại chỉ trích một phần đề → không xác định được câu cuối).
  * Mẫu HK2  = `inputs/refs/de-thi/lop-9/vdc-phan-loai-hk2.json` — người đọc gán chương
               cho từng câu trích được từ text PDF (bank chưa chấm band cho GK2/CK2).
  * Mỗi đề đóng góp ĐÚNG MỘT câu cho mỗi vị trí:
      - "câu cuối đề"      = phần tử cuối của danh sách câu;
      - "ý cuối bài hình"  = ý cuối của BÀI có chương hình (C4/C5/C9/C10).
  * Tần suất của một chương = (số đề mà chương đó chiếm vị trí VDC) / (số đề của các KỲ
    mà chương đó được kiểm tra). Lấy MAX của hai vị trí.

Dùng:
    .venv/bin/python scripts/tan_suat_vdc.py            # in báo cáo
    .venv/bin/python scripts/tan_suat_vdc.py --json     # xuất JSON để dán vào bản đồ
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMS = ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "exams"
HK2 = ROOT / "inputs" / "refs" / "de-thi" / "lop-9" / "vdc-phan-loai.json"
K678 = ROOT / "inputs" / "refs" / "de-thi" / "vdc-phan-loai-khoi-678.json"
CAU_CUOI = ROOT / "inputs" / "refs" / "de-thi" / "cau-cuoi-de.json"

# Bài HÌNH của mỗi (khối, kỳ) thuộc chương nào — theo tiến độ SGK KNTT. Cùng bảng với
# scripts/build_trich_vdc.py. LỚP 6 không có mặt: anh An chốt lớp 6 chỉ có câu cuối đề.
HINH_THEO_KY = {
    ("lop-7", "gk1"): "III", ("lop-7", "ck1"): "IV",
    ("lop-7", "gk2"): "IX",  ("lop-7", "ck2"): "IX",
    ("lop-8", "gk1"): "III", ("lop-8", "ck1"): "III",
    ("lop-8", "gk2"): "IX",  ("lop-8", "ck2"): "IX",
}

# Kỳ nào kiểm tra chương nào, khối 6/7/8 — mẫu số của tần suất.
KY_678 = {
    "lop-6": {"I": ("gk1",), "II": ("gk1", "ck1"), "III": ("ck1",), "IV": ("ck1",),
              "V": ("ck1",), "VI": ("gk2", "ck2"), "VII": ("ck2",), "VIII": ("gk2", "ck2"),
              "IX": ("ck2",)},
    "lop-7": {"I": ("gk1", "ck1"), "II": ("ck1",), "III": ("gk1", "ck1"), "IV": ("ck1",),
              "V": ("ck1", "gk2"), "VI": ("gk2", "ck2"), "VII": ("gk2", "ck2"),
              "VIII": ("gk2", "ck2"), "IX": ("gk2", "ck2"), "X": ("ck2",)},
    "lop-8": {"I": ("gk1", "ck1"), "II": ("gk1", "ck1"), "III": ("gk1", "ck1"),
              "IV": ("ck1",), "V": ("ck1",), "VI": ("gk2", "ck2"), "VII": ("gk2", "ck2"),
              "VIII": ("gk2", "ck2"), "IX": ("gk2", "ck2"), "X": ("ck2",)},
}


def tan_suat_678(lop: str) -> dict:
    """Tần suất VDC theo chương cho khối 6/7/8 — cùng luật với lớp 9.

    Câu cuối đề lấy chương từ file phân loại bằng mắt; ý cuối bài hình lấy chương từ
    HINH_THEO_KY (tiến độ SGK). Bản ghi "hong" (script trích sai) KHÔNG vào mẫu số;
    bản ghi "?" (bài đếm/logic không thuộc chương nào) CÓ vào mẫu số."""
    cls = json.loads(K678.read_text(encoding="utf-8"))["khoi"][lop]
    rows = [r for r in cls["cau_cuoi_de"] if r.get("hop_le") is not False]
    mau_cuoi = Counter(r["ky"] for r in rows)
    # Bản ghi trong kho mà CHƯA phân loại thì KHÔNG vào mẫu số — nếu tính, mọi chương
    # đều bị pha loãng và tụt nhóm một cách giả tạo. Số nợ báo riêng ở `con_no`.
    cuoi: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        cuoi[r["ky"]][r["chuong"]] += 1

    hinh: dict[str, Counter] = defaultdict(Counter)
    mau_hinh = Counter()
    if lop != "lop-6":                     # anh An: lớp 6 chỉ có câu cuối đề
        for x in json.loads(CAU_CUOI.read_text(encoding="utf-8")):
            if x["lop"] != lop or x["vitri"] != "ý cuối bài hình":
                continue
            ch = HINH_THEO_KY.get((lop, x["ky"]))
            if ch:
                hinh[x["ky"]][ch] += 1
                mau_hinh[x["ky"]] += 1

    ket = {}
    for ma, kys in KY_678[lop].items():
        m_c = sum(mau_cuoi.get(k, 0) for k in kys)
        m_h = sum(mau_hinh.get(k, 0) for k in kys)
        n_c = sum(cuoi.get(k, {}).get(ma, 0) for k in kys)
        n_h = sum(hinh.get(k, {}).get(ma, 0) for k in kys)
        p_c = n_c / m_c if m_c else 0.0
        p_h = n_h / m_h if m_h else 0.0
        pmax = max(p_c, p_h)
        nhom, vd, vdc = nhom_va_phan_bo(pmax)
        ket[ma] = {
            "ky_kiem_tra": list(kys),
            "tan_suat": {
                "cau_cuoi_de": {"so_de": n_c, "tong_de": m_c, "ty_le": round(p_c, 3)},
                "y_cuoi_bai_hinh": {"so_de": n_h, "tong_de": m_h, "ty_le": round(p_h, 3)},
            },
            "p": round(pmax, 3), "nhom_uu_tien": nhom,
            "phan_bo_55": {"VD": vd, "VDC": vdc},
            "mau_qua_nho": (m_c + m_h) < 6,
        }
    da = {r.get("file") for r in cls["cau_cuoi_de"]}
    kho = {x["file"][:52] for x in json.loads(CAU_CUOI.read_text(encoding="utf-8"))
           if x["lop"] == lop and x["vitri"] == "câu cuối đề"}
    ket["_con_no"] = {"da_phan_loai": len(da), "trong_kho": len(kho),
                      "chua_phan_loai": len(kho - da)}
    return ket

CHUONG_HINH = {"C4", "C5", "C9", "C10"}
MA = {f"C{i}": r for i, r in enumerate(
    ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"], start=1)}

# Kỳ nào kiểm tra chương nào (dùng làm MẪU SỐ của tần suất) — theo phân phối chương
# trình KNTT lớp 9 và chính kho đề: GK1 = chương I–IV, CK1 = I–V, GK2/CK2 = VI–X.
KY_CUA_CHUONG = {
    "I": ("gk1", "ck1"), "II": ("gk1", "ck1"), "III": ("gk1", "ck1"),
    "IV": ("gk1",), "V": ("ck1",),
    "VI": ("gk2", "ck2"), "VII": ("gk2", "ck2"), "VIII": ("gk2", "ck2"),
    "IX": ("gk2", "ck2"), "X": ("gk2", "ck2"),
}

# Nhóm ưu tiên theo tần suất → phần trăm thời lượng chia trong khối 55% VD+VDC.
NGUONG = [(0.50, "cao", 35, 20), (0.20, "vua", 43, 12), (0.01, "thap", 50, 5)]


def nhom_va_phan_bo(p: float) -> tuple[str, int, int]:
    for nguong, ten, vd, vdc in NGUONG:
        if p >= nguong:
            return ten, vd, vdc
    return "khong", 55, 0


def _bai_of(c: dict) -> str:
    """Số hiệu BÀI của một câu — hai schema cùng tồn tại trong bank."""
    if "vi_tri" in c:
        m = re.match(r"\s*(?:Bài|Câu)\s*([IVX0-9]+)", c["vi_tri"])
        return m.group(1) if m else "?"
    return str(c.get("bai", "?"))


def de_du_diem() -> list[tuple[str, str, dict]]:
    """(tên đề, kỳ, dữ liệu) của các đề TỔNG 9–10,5đ — chỉ đề đủ mới biết câu nào cuối."""
    out = []
    for f in sorted(EXAMS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if 9.0 <= sum(c.get("diem") or 0 for c in d["cau"]) <= 10.5:
            out.append((f.stem, f.stem.split("-")[0], d))
    return out


def _chuong_hk1_theo_cach_giai() -> dict:
    """{tên đề: chương} cho CÂU CUỐI ĐỀ của mẫu HK1 — lấy từ file phân loại vì bank
    gắn `chuong` theo NỘI DUNG đề bài, còn ở đây phải gán theo CÁCH GIẢI mức lớp 9."""
    d = json.loads(HK2.read_text(encoding="utf-8"))
    return {r["nguon"]: r["chuong"] for r in d["cau_cuoi_de_hk1"]}


_CHUONG_HK1 = _chuong_hk1_theo_cach_giai()


def dem_hk1() -> tuple[dict, dict, Counter, list]:
    """Đếm hai vị trí VDC trên mẫu HK1. Trả (cuối đề, ý cuối hình, số đề mỗi kỳ, chi tiết)."""
    cuoi: dict[str, Counter] = defaultdict(Counter)
    hinh: dict[str, Counter] = defaultdict(Counter)
    so_de = Counter()
    chi_tiet = []
    for ten, ky, d in de_du_diem():
        so_de[ky] += 1
        last = d["cau"][-1]
        cuoi[ky][_CHUONG_HK1.get(ten, MA.get(last["chuong"], last["chuong"]))] += 1
        chi_tiet.append((ten, "câu cuối đề", MA.get(last["chuong"], "?"),
                         last.get("band"), last.get("diem"), last.get("de", "")))
        bai = None
        for c in d["cau"]:
            if c.get("chuong") in CHUONG_HINH:
                bai = _bai_of(c)
        if bai:
            y = [c for c in d["cau"] if _bai_of(c) == bai][-1]
            hinh[ky][MA.get(y["chuong"], y["chuong"])] += 1
            chi_tiet.append((ten, "ý cuối bài hình", MA.get(y["chuong"], "?"),
                             y.get("band"), y.get("diem"), y.get("de", "")))
    return cuoi, hinh, so_de, chi_tiet


def dem_hk2() -> tuple[dict, dict, Counter, Counter]:
    """Đếm hai vị trí VDC trên mẫu HK2 (file phân loại bằng mắt) + xếp hạng DẠNG."""
    d = json.loads(HK2.read_text(encoding="utf-8"))
    cuoi: dict[str, Counter] = defaultdict(Counter)
    hinh: dict[str, Counter] = defaultdict(Counter)
    so_de = Counter()
    dang = Counter()
    for r in d["cau_cuoi_de_hk2"]:
        if not r.get("hop_le"):
            continue
        so_de[r["ky"]] += 1
        # Chương gán theo CÁCH GIẢI ở mức lớp 9, không theo "bài này nằm ở kỳ nào"
        # (Thầy chốt 04/09/2026 — xem quy_uoc_gan_chuong trong file phân loại).
        cuoi[r["ky"]][r["chuong"]] += 1
        dang["cuoi-de:" + r["cach_giai"]] += 1
    for r in d["y_cuoi_bai_hinh_hk2"]:
        hinh[r["ky"]][r["chuong"]] += 1
        dang["hinh:" + r["dang"]] += 1
    return cuoi, hinh, so_de, dang


def cach_giai_toan_bo() -> tuple[Counter, list]:
    """Xếp hạng CÁCH GIẢI của mọi câu cuối đề (HK1 + HK2) + danh sách câu NGOÀI SGK."""
    d = json.loads(HK2.read_text(encoding="utf-8"))
    rows = d["cau_cuoi_de_hk1"] + [r for r in d["cau_cuoi_de_hk2"] if r.get("hop_le")]
    ngoai = [(r.get("nguon") or r.get("truong"), r["cach_giai"]) for r in rows
             if r.get("ngoai_sgk")]
    return Counter(r["cach_giai"] for r in rows), ngoai


def tong_hop() -> dict:
    c1, h1, n1, chi_tiet = dem_hk1()
    c2, h2, n2, dang2 = dem_hk2()
    cuoi = {**c1, **c2}
    hinh = {**h1, **h2}
    # mẫu số của HK2 = số ý cuối bài hình đọc được (14) — nhiều hơn số câu cuối hợp lệ
    so_de = Counter(n1)
    for k in ("gk2", "ck2"):
        so_de[k] = max(n2.get(k, 0), sum(v for kk, v in hinh.get(k, {}).items()))

    ket = {}
    for ma, kys in KY_CUA_CHUONG.items():
        mau = sum(so_de.get(k, 0) for k in kys)
        n_cuoi = sum(cuoi.get(k, {}).get(ma, 0) for k in kys)
        n_hinh = sum(hinh.get(k, {}).get(ma, 0) for k in kys)
        # mẫu số của vị trí "ý cuối bài hình" = số đề CÓ bài hình đọc được
        mau_hinh = sum(sum(hinh.get(k, {}).values()) for k in kys) or mau
        p_cuoi = n_cuoi / mau if mau else 0.0
        p_hinh = n_hinh / mau_hinh if mau_hinh else 0.0
        p = max(p_cuoi, p_hinh)
        nhom, vd, vdc = nhom_va_phan_bo(p)
        ket[ma] = {
            "ky_kiem_tra": list(kys),
            "tan_suat": {
                "cau_cuoi_de": {"so_de": n_cuoi, "tong_de": mau, "ty_le": round(p_cuoi, 3)},
                "y_cuoi_bai_hinh": {"so_de": n_hinh, "tong_de": mau_hinh, "ty_le": round(p_hinh, 3)},
            },
            "p": round(p, 3),
            "nhom_uu_tien": nhom,
            "phan_bo_55": {"VD": vd, "VDC": vdc},
        }
    return {"chuong": ket, "so_de_moi_ky": dict(so_de), "dang_hk2": dict(dang2),
            "cuc_tri_ca_4_ky": cuc_tri_ca_4_ky(chi_tiet, dang2),
            "chi_tiet_hk1": chi_tiet}


def cuc_tri_ca_4_ky(chi_tiet: list, dang2: Counter) -> dict:
    """Câu cuối đề là bài CỰC TRỊ/TỐI ƯU trong bao nhiêu đề của cả bốn kỳ?

    Đếm từ trường `cach_giai` của file phân loại: mọi cách giải TRỪ `hinh-thuan`
    (bài hình thuần, không phải cực trị) đều là bài đánh giá bất đẳng thức. Riêng
    ck1-ngoc-thuy là phương trình vô tỉ nên cũng không tính."""
    d = json.loads(HK2.read_text(encoding="utf-8"))
    rows = d["cau_cuoi_de_hk1"] + [r for r in d["cau_cuoi_de_hk2"] if r.get("hop_le")]
    khong_phai = {"hinh-thuan"}
    ct = [r for r in rows
          if r["cach_giai"] not in khong_phai and r.get("nguon") != "ck1-ngoc-thuy"]
    hk1 = [r for r in rows if "nguon" in r]
    return {"hk1": {"cuc_tri": sum(1 for r in ct if "nguon" in r), "tong": len(hk1)},
            "hk2": {"cuc_tri": sum(1 for r in ct if "ky" in r),
                    "tong": len(rows) - len(hk1)},
            "tong": {"cuc_tri": len(ct), "tong": len(rows),
                     "ty_le": round(len(ct) / len(rows), 3)}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="xuất JSON thay vì báo cáo chữ")
    a = ap.parse_args()
    r = tong_hop()
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k != "chi_tiet_hk1"},
                         ensure_ascii=False, indent=2))
        return
    print("SỐ ĐỀ MỖI KỲ (mẫu):", dict(r["so_de_moi_ky"]))
    print(f"\n{'Ch':4s} {'kỳ':10s} {'cuối đề':>12s} {'ý cuối hình':>14s} {'p':>6s} "
          f"{'nhóm':6s} {'VD/VDC':>8s}")
    for ma, v in r["chuong"].items():
        t = v["tan_suat"]
        print(f"{ma:4s} {'+'.join(v['ky_kiem_tra']):10s} "
              f"{t['cau_cuoi_de']['so_de']:3d}/{t['cau_cuoi_de']['tong_de']:<3d} "
              f"{t['cau_cuoi_de']['ty_le']:5.2f} "
              f"{t['y_cuoi_bai_hinh']['so_de']:3d}/{t['y_cuoi_bai_hinh']['tong_de']:<3d} "
              f"{t['y_cuoi_bai_hinh']['ty_le']:5.2f} "
              f"{v['p']:6.2f} {v['nhom_uu_tien']:6s} "
              f"{v['phan_bo_55']['VD']:2d}/{v['phan_bo_55']['VDC']:<2d}")
    ct = r["cuc_tri_ca_4_ky"]
    print(f"\nCÂU CUỐI ĐỀ LÀ BÀI CỰC TRỊ/TỐI ƯU: HK1 {ct['hk1']['cuc_tri']}/{ct['hk1']['tong']}"
          f" · HK2 {ct['hk2']['cuc_tri']}/{ct['hk2']['tong']}"
          f" · CẢ 4 KỲ {ct['tong']['cuc_tri']}/{ct['tong']['tong']} = {ct['tong']['ty_le']:.0%}")
    cg, ngoai = cach_giai_toan_bo()
    print("\nCÁCH GIẢI của CÂU CUỐI ĐỀ (HK1 + HK2, mức lớp 9 — không dùng đạo hàm):")
    for k, n in cg.most_common():
        print(f"   {n:3d}  {k}")
    print(f"\nNGOÀI SGK lớp 9 ({len(ngoai)} câu — phải dạy thêm hoặc chấp nhận mất):")
    for ten, k in ngoai:
        print(f"        {ten} ({k})")
    print("\nDẠNG Ý CUỐI BÀI HÌNH — HK2:")
    for k, n in sorted(r["dang_hk2"].items(), key=lambda x: -x[1]):
        if k.startswith("hinh:"):
            print(f"   {n:3d}  {k[5:]}")


if __name__ == "__main__":
    main()
