#!/usr/bin/env python3
"""Ráp 3 kết quả Gemini (gop-9c-ch7-tren-lop + gop-9c-ch7-btvn + gop-9c-ch7-btvn-them) thành seed phiếu ch.VII 9C
(Bài 22–24 một buổi; tên theo dạng bài đích: đọc biểu đồ ghép nhóm, lập bảng, tính tần số tương đối).

    python3 scripts/gemini/lap_gop_phieu_ch7_9c.py

Thay [[HINH:khoá]] bằng bảng/biểu đồ máy dựng (viec_gop_phieu_ch7_9c.HINH), bỏ [[br]] dính sát
bảng/biểu đồ, ép tier theo chặng, bỏ writelines, báo khoá lạ / chỗ còn tabular-tikz tự viết.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from viec_gop_phieu_ch7_9c import D, HINH, SLUG, TITLE  # noqa: E402

OUT = REPO / D / f"{SLUG}.json"
_KHOA = re.compile(r"(?:\[\[br\]\]\s*)*\[\[HINH:([A-Za-z0-9_]+)\]\](?:\s*\[\[br\]\])*")


def lay(vid):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{vid}.json").read_text())
    data = kq.get("ket_qua") or kq
    if data.get("ghi_chu"):
        print(f"[{vid}] ghi_chu Gemini: {data['ghi_chu']}")
    return data["stages"]


def thay(s: str, loi: list[str], dung: set[str]) -> str:
    def _f(m):
        k = m.group(1)
        if k not in HINH:
            loi.append(f"khoá lạ {k}")
            return m.group(0)
        dung.add(k)
        return HINH[k]
    return _KHOA.sub(_f, s)


def duyet(x, loi, dung):
    if isinstance(x, str):
        return thay(x, loi, dung)
    if isinstance(x, list):
        return [duyet(v, loi, dung) for v in x]
    if isinstance(x, dict):
        return {k: duyet(v, loi, dung) for k, v in x.items()}
    return x


def main():
    st = lay("gop-9c-ch7-tren-lop") + lay("gop-9c-ch7-btvn")
    assert [s["number"] for s in st] == [1, 2, 3, 4, 5], [s["number"] for s in st]
    # Thầy 15/11: BTVN thêm 3 bài thật (gop-9c-ch7-btvn-them) — chèn đúng mức NB→TH→VD rồi đánh số lại.
    them = lay("gop-9c-ch7-btvn-them")[0]["blocks"]
    ref = st[4]["blocks"]
    sau = {"Bài 19.": them[0], "Bài 21.": them[1], "Bài 22.": them[2]}   # Hát Môn, Phúc Đồng, bóng đèn
    moi = []
    for b in ref:
        moi.append(b)
        if b.get("label") in sau:
            moi.append(sau[b["label"]])
    so = 17
    for b in moi:
        if b.get("type") == "problem":
            b["label"] = f"Bài {so}."
            so += 1
    st[4]["blocks"] = moi
    st[4]["teacher_note"] = (f"Sơ đồ tư duy điền 5 phút cuối buổi; bài tập về nhà gồm Bài 17 đến Bài {so - 1}, "
                             f"in phiếu riêng; buổi sau chữa Bài {so - 2} và Bài {so - 1} trước.")
    for s in st:
        s["blocks"] = [b for b in s["blocks"] if b.get("type") != "writelines"]
        for b in s["blocks"]:
            if b.get("type") == "problem":
                b["tier"] = "btvn" if s["kind"] == "reflection" else "onclass"
                b.pop("writelines", None)
                b.pop("figure", None)
            for k in ("statement", "text", "solution"):
                v = b.get(k, "")
                if isinstance(v, str) and re.search(r"\\begin\{(?:tabular|tikzpicture|center)\}", v):
                    print("⚠ Gemini tự viết bảng/hình:", b.get("label") or v[:50])
    # Soát tay đầu ra Gemini (Claude, 15/11): sai tên loại sách ở lời giải Bài 2; \\dfrac giữa dòng đè chữ.
    sua = 0
    for s in st:
        for b in s["blocks"]:
            for k in ("statement", "text", "solution"):
                v = b.get(k)
                if not isinstance(v, str):
                    continue
                v2 = v.replace("Sách giáo khoa, Sách bài tập, Sách tham khảo, Truyện thiếu nhi",
                               "Sách giáo khoa, Truyện ngắn, Sách tham khảo, Tiểu thuyết")
                v2 = v2.replace("\\dfrac", "\\frac")
                v2 = v2.replace("Một cửa hàng bán đồ chơi cho trẻ em thống kê", "Một cửa hàng đồ chơi thống kê")
                v2 = v2.replace("Giáo viên chủ nhiệm thông báo", "Cô giáo chủ nhiệm lớp 8A thông báo")
                v2 = v2.replace("thông báo của giáo viên chủ nhiệm", "thông báo của cô giáo chủ nhiệm")
                v2 = v2.replace("khó rút ra nhận xét. Làm thế nào", "khó rút ra nhận xét.[[br]]Làm thế nào")
                if v2 != v:
                    sua += 1
                    b[k] = v2
    # Dãy số liệu dài viết trong MỘT $…$ không ngắt dòng được ⇒ tách mỗi số một $…$.
    day = re.compile(r"\$((?:[0-9{},]+;\\;){5,}[0-9{},]+)\$")
    for s in st:
        for b in s["blocks"]:
            for k in ("statement", "text"):
                v = b.get(k)
                if isinstance(v, str) and day.search(v):
                    b[k] = day.sub(lambda m: "; ".join(f"${x}$" for x in m.group(1).split(";\\;")), v)
                    sua += 1
    print(f"Sửa tay {sua} trường")
    loi: list[str] = []
    dung: set[str] = set()
    st = duyet(st, loi, dung)
    thieu = sorted(set(HINH) - dung)
    lesson = {
        "slug": SLUG,
        "title": TITLE,
        "eyebrow": "ĐẠI SỐ — CHƯƠNG VII · BÀI 22 + 23 + 24",
        "grade_label": "Lớp 9 • Ôn vào 10",
        "class_tier": "C",
        "so_ca": 1,
        "btvn_phieu_rieng": True,
        "stages": st,
    }
    OUT.write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n")
    print(f"Đã ghi {OUT.relative_to(REPO)} — dùng {len(dung)}/{len(HINH)} hình; lỗi: {loi or 'không'}; "
          f"hình chưa dùng: {thieu or 'không'}")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
