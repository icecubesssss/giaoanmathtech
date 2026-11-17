#!/usr/bin/env python3
"""Việc Gemini: viết lại CHỮ cho phiếu 8.2 (phiếu B ch.VIII 9C) sau khi cắt về 135′ (15/11/2026).

Phần cơ học đã làm bằng cat_phieu_8b_9c.py (bỏ Bài 5/14/17 cũ, chia mạch LT1, Bài 27 cũ lên đầu BTVN,
đánh số lại, kiem_tra_phut 45, btvn_phieu_rieng). Gemini viết:
  TN:0..TN:4   teacher_note 5 chặng (phút mới, nhãn bài mới)
  DICH         đoạn "Đích của buổi học" (para đầu Luyện tập 1, trỏ Bài 14 trước tiên)
  MACH:1..3    chữ ba tiêu đề mạch Luyện tập 1
  Bài 7., Bài 10., Bài 13., Bài 14.   statement bỏ \\dots/\\ldots (cổng đọc là ô điền khuyết)
  QT:Bài 14.   quy_trinh của Bài 14 (đang sai: ghi "hai hành động" cho bài MỘT hành động)

    python3 scripts/gemini/viec_cat_phieu_8b_9c.py            # sinh việc
    python3 scripts/gemini/tho.py --mot cat-phieu-8b-9c
    python3 scripts/gemini/viec_cat_phieu_8b_9c.py --ap [--ghi]
"""
import difflib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
        "phieu-b-phep-thu-hai-hanh-dong-va-luyen-tap-chung.json")
VID = "cat-phieu-8b-9c"
MODEL = "gemini-4-hydrogen-medium"
NHAN_BAI = ["Bài 7.", "Bài 10.", "Bài 13.", "Bài 14."]
NHAN = ["TN:0", "TN:1", "TN:2", "TN:3", "TN:4", "DICH", "MACH:1", "MACH:2", "MACH:3"] + NHAN_BAI + ["QT:Bài 14."]


def mot_dong(b):
    t = b.get("statement") or b.get("text") or b.get("caption") or ""
    return t[:160].replace("\n", " ")


def so_do(d):
    out = []
    for i, s in enumerate(d["stages"]):
        out.append(f"CHẶNG {i} — {s['title']} (kind {s['kind']})")
        for b in s["blocks"]:
            nhan = b.get("label") or b.get("variant") or ""
            muc = {1: "NB", 2: "TH", 3: "VD"}.get(b.get("level"), "")
            tier = b.get("tier", "")
            out.append(f"   [{b['type']}] {nhan} {muc} {tier} | {mot_dong(b)}")
    return "\n".join(out)


def prompt(d):
    st = d["stages"]
    tn = "\n".join(f"- TN:{i} (chặng {s['title']}): {s.get('teacher_note', '')}" for i, s in enumerate(st))
    dich = next(b["text"] for b in st[0]["blocks"] if "Đích của buổi" in b.get("text", ""))
    bai = []
    for s in st:
        for b in s["blocks"]:
            if b.get("label") in NHAN_BAI:
                bai.append(json.dumps({k: b.get(k) for k in ("label", "level", "statement", "quy_trinh")},
                                      ensure_ascii=False, indent=1))
    return r'''Bạn là thợ soạn học liệu Toán lớp 9 (Việt Nam, SGK Kết nối tri thức). Viết LaTeX trong chuỗi JSON (dấu \ viết một lần như trong dữ liệu mẫu; xuống dòng bằng [[br]]).

## Bối cảnh
Phiếu 8.2 lớp 9C (HS trung bình–yếu): "Phép thử gồm hai hành động, Luyện tập chung và Bài tập cuối chương VIII".
Buổi 31/01/2027 (tuần 33), ca 180′ = phiếu 135′ (120′ học + 15′ giải lao) + 45′ KIỂM TRA GỘP CHƯƠNG VII và VIII ở cuối ca.
Trước đây phiếu soạn cho cả ca 165′ học. Giám đốc đã CẮT: bỏ bài "đếm nhanh n(Ω) bằng phép nhân" (BTVN vẫn có),
bỏ bài TH "ghép hai thẻ thành số có hai chữ số" (BTVN vẫn có), bỏ bài VD "lấy đồng thời hai viên bi" (trùng nguyên văn Ví dụ 8;
BTVN vẫn có một bài lấy đồng thời hai thẻ), chia Luyện tập 1 thành 3 mạch, đánh số lại toàn bộ bài (31 bài: 14 trên lớp, 17 BTVN).
BTVN nay in thành phiếu riêng (Phiếu BTVN).

## Sơ đồ phiếu SAU khi cắt (nhãn mới)
''' + so_do(d) + r'''

## Phân phút đã chốt (tổng 120′ học, giải lao 15′ giữa Luyện tập 1 và Luyện tập 2)
- Chặng Khám phá 5′ (gieo thật hai xúc xắc vài lần, chốt câu "công thức không đổi, chỉ cách đếm $n(\Omega)$ đổi"; phần nhắc buổi trước 1–2′, không giảng lại).
- Kiến thức cần nhớ 12′ (đọc nhanh 4 mục, nhấn hai bẫy; ví dụ để dành cho chặng luyện tập).
- Luyện tập 1 — Nhận biết 45′: Mạch 1 (Ví dụ 1, Bài 1–2, Ví dụ 2, Bài 3–4) ~18′ · Mạch 2 (Ví dụ 3, Bài 5–7) ~15′ · Mạch 3 (Bài 8 điền khuyết bài giải mẫu, Bài 9 ba câu bắt buộc, Bài 10 chọn mô hình) ~12′.
- Luyện tập 2 — Thông hiểu \& Vận dụng 53′: Ví dụ 4 + bảng so sánh, Bài 11 (hai xúc xắc, Bài 8{.}16), Ví dụ 5 + Bài 12 (tích), Ví dụ 6, Ví dụ 7, Bài 13 (ôn một hành động), Ví dụ 8 (chỉ giới thiệu lấy đồng thời, 3′), Bài 14 (VD đề cuối kì II THCS Chu Văn An, chấm như bài thi).
- Tổng kết 5′ (sơ đồ tư duy). BTVN 17 bài (Bài 15–31) ≈ 96′ — giao Phiếu BTVN riêng. Dặn: cuối ca hôm nay làm bài kiểm tra 45′ gộp chương VII và VIII, nên phần luyện tập phải giữ đúng giờ; đây là buổi CUỐI chương trình SGK lớp 9, giữ lại cả hai phiếu chương VIII cho phần luyện đề Câu I.2.

## Bản hiện tại (CŨ, nhãn bài cũ) của 5 teacher_note
''' + tn + r'''

## Bản hiện tại (CŨ) của đoạn Đích
''' + dich + r'''

## Bản hiện tại của các bài cần sửa câu chữ (nhãn MỚI)
''' + "\n".join(bai) + r'''

## Việc — trả ĐÚNG các nhãn sau
1. "TN:0" … "TN:4": viết lại teacher_note từng chặng theo phân phút mới và NHÃN BÀI MỚI. Giữ giọng văn, ý sư phạm hay của bản cũ (gọi HS lên điền ô, tô khối $5\cdot 5$ để thấy phần bù, Bài 14 chấm như bài thi thiếu câu đồng khả năng hoặc thiếu "Vậy" là trừ điểm…). Mỗi note mở đầu bằng "<Tên việc> <N> phút." như bản cũ (vd "Luyện 45 phút."). Không nhắc tới bài đã bỏ. TN:3 nhắc: chỉ giới thiệu Ví dụ 8, không ra bài lấy đồng thời trên lớp. TN:4 nhắc kiểm tra 45′ cuối ca và Phiếu BTVN riêng.
2. "DICH": đoạn mở đầu bằng "\textbf{Đích của buổi học.}" (sẽ đặt ở đầu Luyện tập 1). Câu đầu tiên phải nêu Bài 14 là bài chốt buổi (đề cuối kì II THCS Chu Văn An — mô hình MỘT hành động giống Câu I.2 Vào 10) — chuỗi "Bài <số>" ĐẦU TIÊN xuất hiện trong đoạn PHẢI là "Bài 14". Sau đó nói: Mạch 1–2 Luyện tập 1 cho bảng hai chiều và $n(\Omega)$, $n(E)$; Mạch 3 ráp thành ba câu trình bày; Luyện tập 2 tính xác suất hai hành động (đề trường có hỏi) và ôn lại một hành động ở Bài 13. Giữ ý: hết buổi là hết chương trình SGK lớp 9. Tối đa 4 câu.
3. "MACH:1", "MACH:2", "MACH:3": chữ tiêu đề mạch, dạng "Mạch 1. <tên ngắn>" (≤ 9 chữ, không LaTeX phức tạp, không dấu chấm cuối). Gợi ý nội dung: 1 = lập bảng hai chiều, đếm $n(\Omega)$; 2 = đếm kết quả thuận lợi trên bảng; 3 = ráp ba câu trình bày.
4. "Bài 7.", "Bài 10.", "Bài 13.", "Bài 14.": trả "statement" sửa câu chữ sao cho KHÔNG còn chuỗi \dots hoặc \ldots (cổng máy đọc hai lệnh này là ô điền khuyết). Cách sửa: "ghi các số $1;2;\dots;10$" → "ghi các số từ 1 đến 10"; "có ít nhất một\ldots" → "có ít nhất một" (giữ ngoặc kép \textquotedblleft…\textquotedblright). Mọi chữ khác, bảng, hình TikZ, số liệu GIỮ NGUYÊN TỪNG KÝ TỰ. "solution" trả chuỗi rỗng "" (máy giữ lời giải cũ).
5. "QT:Bài 14.": Bài 14 là bài MỘT hành động (lấy một viên bi) nhưng quy_trinh hiện ghi "sơ đồ hình cây/bảng… phép thử hai hành động" — SAI. Trả "hints" = mảng 4 bước quy trình đúng cho bài một hành động: viết không gian mẫu và $n(\Omega)$ → khẳng định các kết quả đồng khả năng (nêu lí do) → liệt kê, đếm kết quả thuận lợi → tính $P=\dfrac{n(A)}{n(\Omega)}$ và viết câu "Vậy". Mỗi bước 1 câu, không lộ đáp số. "statement" và "solution" trả "".
Với nhãn TN/DICH/MACH: chữ đặt ở "statement", "solution" = "".

## Tự soát trước khi trả
- Mọi $ mở có $ đóng; % & # phải có \ đứng trước. Không dùng ký tự toán unicode ngoài $…$ (viết $\Omega$, không viết Ω).
- Nhãn bài trong teacher_note khớp sơ đồ mới (vd ô "Bài 11" là hai xúc xắc, "Bài 12" là tích hai thẻ).
- Không xưng "em"/"các em" trong DICH và MACH.
- Nghi ngờ gì ghi vào "ghi_chu".

## Đầu ra
JSON đúng schema: {"sua": [{"label","statement","solution","hints"?} cho ĐÚNG các nhãn: ''' + ", ".join(NHAN) + r'''], "ghi_chu": "…"}.
'''


def sinh():
    d = json.loads((REPO / SEED).read_text())
    p = prompt(d)
    v = {"id": VID, "model": MODEL, "prompt": p, "files": [],
         "schema": "scripts/gemini/schema/sua-bai-phieu.json", "timeout": "1200s",
         "meta": {"loai": "cat-phieu", "seed": SEED, "labels": NHAN}}
    out = REPO / "storage/gemini/hang-doi" / f"{VID}.json"
    out.write_text(json.dumps(v, ensure_ascii=False, indent=2))
    print("→", out.relative_to(REPO), MODEL, f"{len(p) // 1000}k ký tự")


def diff(nhan, cu, moi):
    print(f"--- {nhan}")
    for x in difflib.ndiff((cu or "").split("[[br]]"), (moi or "").split("[[br]]")):
        if x[0] in "+-":
            print("  ", x)


def ap(ghi):
    kq = json.loads((REPO / "storage/gemini/xong" / f"{VID}.json").read_text())
    data = kq.get("ket_qua") or kq.get("json") or kq
    sua = {x["label"]: x for x in data["sua"]}
    if set(sua) != set(NHAN):
        print("Nhãn lệch: thừa", sorted(set(sua) - set(NHAN)), "thiếu", sorted(set(NHAN) - set(sua)))
        return 1
    seed_p = REPO / SEED
    d = json.loads(seed_p.read_text())
    st = d["stages"]
    for i in range(5):
        diff(f"TN:{i}", st[i].get("teacher_note"), sua[f"TN:{i}"]["statement"])
        st[i]["teacher_note"] = sua[f"TN:{i}"]["statement"]
    # Đích: bỏ noted ở chặng 0, đặt para đầu Luyện tập 1
    i0 = next(i for i, b in enumerate(st[0]["blocks"]) if "Đích của buổi" in b.get("text", ""))
    cu = st[0]["blocks"].pop(i0)
    diff("DICH", cu["text"], sua["DICH"]["statement"])
    st[2]["blocks"].insert(0, {"type": "para", "text": sua["DICH"]["statement"]})
    k = 0
    for b in st[2]["blocks"]:
        if b.get("type") == "para" and b.get("variant") == "heading":
            k += 1
            moi = sua[f"MACH:{k}"]["statement"]
            assert moi.startswith(f"Mạch {k}."), moi
            diff(f"MACH:{k}", b["text"], moi)
            b["text"] = moi
    for s in st:
        for b in s["blocks"]:
            if b.get("label") in NHAN_BAI:
                moi = sua[b["label"]]["statement"]
                assert "\\dots" not in moi and "\\ldots" not in moi, b["label"]
                diff(b["label"], b["statement"], moi)
                b["statement"] = moi
            if b.get("label") == "Bài 14.":
                q = sua["QT:Bài 14."].get("hints") or []
                assert len(q) >= 3
                diff("QT:Bài 14.", "[[br]]".join(b.get("quy_trinh") or []), "[[br]]".join(q))
                b["quy_trinh"] = q
    print("Ghi chú Gemini:", data.get("ghi_chu", ""))
    if ghi:
        seed_p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        print("Đã ghi", SEED)
    return 0


if __name__ == "__main__":
    if "--ap" in sys.argv:
        sys.exit(ap("--ghi" in sys.argv))
    sinh()
