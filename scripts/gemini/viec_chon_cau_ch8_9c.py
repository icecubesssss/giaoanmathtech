"""Sinh việc Gemini cho Bước Chọn câu + Thuyết minh chương VIII lớp 9C (18/11/2026).

  1) cc-ch8-9c      : chấm T1..T7 (T8=0), lí do, đề xuất, và SOI TOÁN ĐỘC LẬP cho 64 câu đã chọn.
  2) tm-ch8-9c-chu  : viết chữ cho thuyet-minh.json (15 dòng mô tả phương pháp + kiến thức nền + mục tiêu/chuẩn đầu ra + ví dụ + lỗi sai + kiến thức nhớ).

Chạy:
  .venv/bin/python scripts/gemini/viec_chon_cau_ch8_9c.py
  python3 scripts/gemini/tho.py --mot cc-ch8-9c
  python3 scripts/gemini/tho.py --mot tm-ch8-9c-chu
Nếu thay vài câu rồi muốn chấm lại riêng mã mới:
  .venv/bin/python scripts/gemini/viec_chon_cau_ch8_9c.py --lai ma1,ma2
  python3 scripts/gemini/tho.py --mot cc-ch8-9c-lai
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import chon_cau_ch8_9c as cc  # noqa: E402
import tm_ch8_9c as tm  # noqa: E402

OUT_DIR = REPO / "storage/gemini/hang-doi"
MODEL = "gemini-4-hydrogen-medium"

SO_LIEU_DE_THI = """Thống kê 94 câu đề thi chính thức (Ưu tiên 1) trong ngân hàng chương VIII (40 Vào 10, 31 CK2, 23 GK2):
- C8-03 (xác suất 1 hành động tập nền cho sẵn — khuôn Câu I.2 Sở HN): 57/94 (61% · Vào 10: 57%, CK2: 61%, GK2: 65%).
- C8-02 (mô tả Ω, đếm n(Ω) và kết quả thuận lợi): 12/94 (13% · Vào 10: 12%, CK2: 13%, GK2: 13%).
- C8-06 (2 hành động độc lập — bảng 2 chiều, sơ đồ cây): 9/94 (10% · Vào 10: 15%, CK2: 10%).
- C8-04 (1 hành động tự liệt kê Ω từ điều kiện số): 7/94 (7% · CK2: 13%, Vào 10: 5%).
- C8-01 (phép thử ngẫu nhiên, đồng khả năng, biến cố): 4/94 (4%).
- C8-05 (xác suất từ bảng thống kê, biểu đồ, tỉ lệ %): 3/94 (3%).
Nhóm KHÔNG dạy ở 9C: C8-07 lấy đồng thời (6%), C8-09 bài toán ngược (3%), C8-10 không hoàn lại (3%), C8-11 xếp thứ tự (2%), C8-12 XS thực nghiệm (2%), C8-08/13 (≤1%)."""

PROMPT_CC = r'''Bạn là chuyên gia thẩm định học liệu Toán lớp 9 lớp C (lớp 9C, ôn thi vào 10 — mục tiêu 6–7 điểm, nắm chắc khuôn Câu I.2 Sở Hà Nội và bài xác suất hai hành động cơ bản), ĐỒNG THỜI là người TỰ GIẢI ĐỘC LẬP để kiểm tra đề có bẫy / sai sót toán học nào không.
KHÔNG chạy lệnh, KHÔNG mở file ngoài. Đọc đúng dữ liệu JSON dưới đây.

## Bối cảnh chương VIII lớp 9C (18/11/2026)
- Một phiếu gộp cả chương 180′ (Bài 25 + Bài 26 KNTT), khuôn KHÔNG VD (`40% NB – 60% TH – 0% VD`).
- Luật hình thức câu 16/11/2026: điền khuyết chỉ trong Ví dụ; NB = câu nhỏ gắn với đề (trắc nghiệm, Đúng/Sai, trả lời ngắn); TH = bài gọn kèm câu hỏi gợi ý bước / bước đệm NB tách từ bài.
- 6 dạng dạy ở 9C: C8-01 (phép thử, đồng khả năng), C8-02 (mô tả $\Omega$, $n(\Omega)$, kết quả thuận lợi), C8-03 (XS 1 hành động tập nền cho sẵn), C8-04 (XS 1 hành động tự liệt kê $\Omega$), C8-05 (XS từ bảng / biểu đồ / %), C8-06 (2 hành động độc lập bảng 2 chiều / sơ đồ cây). KHÔNG dạy: lấy đồng thời 2 vật, không hoàn lại, xếp thứ tự, bài toán ngược, $\ge 3$ hành động, XS thực nghiệm.

## Tiêu chí chấm T1..T8 (cho điểm nguyên 0, 1 hoặc 2 cho T1..T7; T8 luôn = 0 với lớp C)
Trọng số lớp C: T1×3 + T2×1 + T3×2 + T4×1 + T5×2 + T6×2 + T7×2 + T8×0 (tổng 26 → quy về thang 10; ngưỡng NB ≥ 5, TH ≥ 6).
- T1 (×3) Trọng tâm SGK / chuẩn kiến thức KNTT Bài 25–26: 2 nếu bám sát phép thử, $\Omega$, công thức $P(A)=n(A)/n(\Omega)$ hoặc cầu nối Ch.VII → Ch.VIII.
- T2 (×1) Ý toán: 2 nếu luyện đúng một kỹ năng trọng tâm (chia hết, chia $k$ dư $r$, nguyên tố/chính phương, hai điều kiện, bảng 2 chiều, phần bù "ít nhất một").
- T3 (×2) Bối cảnh & lời văn: 2 nếu diễn đạt rõ ràng, đơn nghĩa (rõ có hoàn lại/đồng thời, phân biệt thứ tự hay không, ghi rõ các phần bằng nhau/cân đối đồng chất).
- T4 (×1) Phân hoá ý con / bước đệm: 2 nếu hợp vai trò (ý a dẫn nhập NB/$\Omega$ cho ý b, hoặc 1 ý gọn cho trắc nghiệm/NB); 1 nếu đơn ý chuẩn Câu I.2; 0 nếu rườm rà hoặc mất cân đối cho vai trò đó.
- T5 (×2) Bắt lỗi sai kinh điển: 2 nếu đánh trúng chỗ HS 9C hay vấp (số $1$ không phải số nguyên tố; quên số $r$ đầu dãy chia $k$ dư $r$ như `1 chia 7 dư 1`; quên đầu/cuối khi đếm; nhầm $n(\Omega)$ 2 hành động bằng phép cộng; gộp $(a;b)$ với $(b;a)$; quên rút gọn phân số).
- T6 (×2) Vừa sức, số liệu đẹp, vừa thời gian vai trò (Ví dụ / Trên lớp / BTVN) và đúng `muc` đã gán: 2 nếu chuẩn 9C; hạ 1 hoặc 0 nếu quá dễ cho TH, hoặc quá dài/khó cho NB, hoặc số quá xấu không cần thiết.
- T7 (×2) Mức độ giống đề thi thật vào 10 / CK2 / GK2 gần đây: 2 nếu là đề thi thật đúng khuôn Sở HN / đề chuẩn; 1 nếu bài SGK hoặc bài luyện tập chuẩn; 0 nếu quá xa khuôn thi.
- T8 = 0 (bắt buộc luôn ghi `0`).

## Nhiệm vụ TỰ GIẢI & BẮT LỖI (bắt buộc làm nghiêm túc cho TỪNG câu!)
- Đọc ĐÚNG các ý `y_boc` được chọn. TỰ TÍNH rõ $n(\Omega)$, tập thuận lợi, $P(A)$ tối giản (chỉ cần kiểm nháp trong đầu rồi ghi kết quả ngắn vào `ly_do` hoặc `nghi_ngo`).
- Nếu phát hiện bất kì vấn đề nào (đề thiếu giả thiết "cân đối/cùng loại/ngẫu nhiên", đề in sai chữ, ý `y_boc` dính phần không dạy như đồng thời / không hoàn lại / VD quá sức 9C, đáp số xấu/mơ hồ ngữ nghĩa "lớn hơn/nhỏ hơn/tích/tổng", hoặc mức `muc` + `so_y`/`so_nb` lệch thực tế sức làm của HS 9C), PHẢI ghi cụ thể vào `nghi_ngo` và cân nhắc `de_xuat` = `"Cân nhắc"` hoặc `"Không hay"`. Nếu hoàn toàn chuẩn sạch, `nghi_ngo = ""`.
- `ly_do`: tối đa 25 chữ tiếng Việt, nêu kết quả chính ($n(\Omega)$, $P$, điểm hay hoặc cảnh báo).

## Đầu ra
Đúng schema `cham-chon-cau.json`: `{"dong": [{"ma", "T": [T1..T8], "ly_do", "de_xuat": "Hay|Cân nhắc|Không hay", "nghi_ngo"}], "ghi_chu": ""}`. Đủ đúng thứ tự mọi `ma` trong dữ liệu đầu vào.

## Danh sách {SO} câu cần chấm (JSON)
'''

PROMPT_CHU = r'''Bạn là giáo viên Toán 9 giàu kinh nghiệm, viết phần chữ tiếng Việt sạch, chính xác, súc tích cho `thuyet-minh.json` Chương VIII lớp 9C (Sách KNTT Toán 9 tập 2: Bài 25 + Bài 26).
KHÔNG chạy lệnh, KHÔNG mở file ngoài. Dùng ĐÚNG dữ liệu và số liệu thực tế trong prompt.

## Quy định hình thức & LaTeX
- Mọi biểu thức toán bọc trong `$ ... $`; dấu phẩy thập phân viết `{,}` bên trong `$ ... $` (ngoài công thức viết dấu phẩy thường). KHÔNG để ký tự Unicode toán học (`≤ ≥ ≠ × ÷ ∈ Ω → ⇒`) nằm ngoài `$ ... $`. Dấu `%` trong văn bản phải viết `\%` hoặc viết chữ "phần trăm" / let JSON writer escape cleanly (tốt nhất viết `\%` trong string JSON để ra PDF chuẩn LaTeX).
- Văn phong thuyết minh giáo án: rõ ràng, thực tế, không tâng bốc, không hứa điểm ảo.

## Đầu ra JSON (đúng schema `chu-tm-chuong.json`)
1. `"d_text"`: object có ĐÚNG {SO_DONG} key như danh sách `KEY_ORDER` bên dưới. Mỗi value là MỘT câu mô tả phương pháp giải + phạm vi bài cho dòng đó trong bảng nội dung thuyết minh (12–28 chữ, kết thúc bằng `\textit{(C8-0x)}` hoặc `\textit{(Kiến thức cũ, C8-05)}`, khớp đúng loại câu §4b và các `source_refs` đi kèm).
2. `"kien_thuc_nen"`: list 4–5 chuỗi, nêu rõ kiến thức lớp dưới dùng lại ở Chương VIII:
   - Thống kê Chương VII (lớp 9, vừa học): cỡ mẫu $N$, tần số, tần số tương đối từ bảng/biểu đồ (nối trực tiếp qua câu KTC và dạng C8-05).
   - Xác suất thực nghiệm và xác suất biến cố đơn giản (Toán 8 KNTT, Bài 30–31): khái niệm biến cố, dự đoán khả năng xảy ra.
   - Tập hợp, phép chia hết, phép chia có dư ($a = kq + r$ với $0 \le r < k$), ước và bội (Toán 6): xác định tập kết quả từ điều kiện số, chú ý cả số đầu/cuối.
   - Số nguyên tố, hợp số, số chính phương (Toán 6): nhắc cứng $1$ không phải số nguyên tố, $2$ là số nguyên tố chẵn duy nhất; các số chính phương thường gặp ($1; 4; 9; 16; 25; \dots$).
   - Rút gọn phân số tối giản và tính phần trăm (Toán 6): đưa $P(A)$ về phân số tối giản hoặc làm tròn theo đúng yêu cầu đề.
3. `"lythuyet"`: list 4–5 chuỗi cho khối MỤC TIÊU – CHUẨN ĐẦU RA – HÌNH THỨC CÂU HỎI – PHẠM VI KHÔNG DẠY:
   - Mục tiêu chương (Bài 25, Bài 26 KNTT).
   - Chuẩn đầu ra gắn với đề thi thật (dùng ĐÚNG số liệu 94 câu đề thi đã cung cấp trong prompt, không bịa thêm số!). Lưu ý thực tế: Chương VIII trên lớp C làm trọn Câu I.2 đề thi vào 10 (~0,5–1 điểm) và các câu tương ứng trong đề CK2/GK2; kiểm tra chương gộp VII + VIII xếp riêng ở tuần 33.
   - Hình thức câu hỏi (luật 16/11/2026, khuôn `khong_vd` 40% NB – 60% TH – 0% VD): NB = 1,5′/câu nhỏ trắc nghiệm / Đúng-Sai / trả lời ngắn; TH = 6′/bài gọn kèm bước đệm `NB tách TH`; điền khuyết chỉ dùng trong Ví dụ.
   - Không dạy ở lớp 9C: liệt kê đúng các dạng thầy không chọn (lấy đồng thời 2 vật C8-07, xếp thứ tự C8-08, bài toán ngược C8-09, lấy lần lượt không hoàn lại C8-10, phép thử từ 3 hành động / đếm nâng cao C8-11, xác suất thực nghiệm Toán 8 C8-12, so sánh khả năng C8-13) và không dạy câu VD.
4. `"vidu"`: list 3–4 chuỗi ngắn gọn tóm tắt mạch Ví dụ trên lớp (~42′ bài mẫu + 3′ lý thuyết = 45′):
   - Nhóm Bài 25 + đầu Bài 26 (C8-01, C8-02): phép thử, đồng khả năng, biến cố xảy ra/không, $\Omega$ và kết quả thuận lợi.
   - Nhóm tính xác suất 1 hành động (C8-03, C8-04, C8-05): công thức cơ bản, bài 30 bi tìm bi trắng, chia $7$ dư $1$ (bẫy số $1$), điều kiện kép "và", tự liệt kê $\Omega$ hai chữ số $< 30$, đọc tỉ lệ % & biểu đồ quạt tròn.
   - Nhóm 2 hành động (C8-06): lập bảng 2 chiều (xúc xắc + đồng xu, 12 cặp), hai túi thẻ $\{2;3;7\}$ ghép số nguyên tố, hai túi $\{2;3;4\}\times\{5;6\}$ (6 cặp).
5. `"loisai"`: list 6–7 chuỗi nêu đúng các lỗi sai kinh điển học sinh 9C hay mắc trong Chương VIII:
   - Quên số dư nhỏ nhất $r$ ở đầu dãy "chia $k$ dư $r$" (vd chia $7$ dư $1$ bỏ sót $1$; chia $5$ dư $2$ bỏ sót $2$ hoặc chọn nhầm $1$).
   - Nhầm $1$ là số nguyên tố, hoặc sót số nguyên tố lớn ($59$, bỏ nhầm hợp số $51=3\cdot 17$, $91=7\cdot 13$).
   - Đếm sót phần tử biên hoặc ghép nhầm dấu "$<$", "$\le$", "không nhỏ hơn", quên $+1$ khi đếm số phần tử liên tiếp $b - a + 1$.
   - Quên kiểm tra điều kiện "đồng khả năng" (lấy từ hộp có số lượng các loại không đều khi xét theo màu mà tưởng đồng khả năng).
   - Phép thử 2 hành động: cộng thay vì nhân khi đếm $n(\Omega)$ (vd đồng xu + 4 bóng ra $2+4=6$ thay vì $8$); gộp $(a;b)$ và $(b;a)$ thành 1 kết quả khi tung 2 xúc xắc hoặc quay 2 lần (làm $n(\Omega)$ còn $21$ thay vì $36$!).
   - Tính ra xác suất $P > 1$ (do đếm nhầm $n(A) > n(\Omega)$ hoặc lấy nghịch đảo $\frac{n(\Omega)}{n(A)}$) hoặc quên rút gọn phân số tối giản / làm tròn sai chữ số thập phân đề hỏi.
6. `"kienthuc_nb"`: list 4–5 chuỗi công thức/khái niệm cốt lõi SGK Toán 9 tập 2 KNTT (Bài 25, Bài 26):
   - Phép thử ngẫu nhiên và kết quả; tính đồng khả năng; tập hợp $\Omega$ (không gian mẫu) và số phần tử $n(\Omega)$.
   - Biến cố $A$, kết quả thuận lợi cho $A$ và số kết quả thuận lợi $n(A)$; biến cố chắc chắn ($P=1$), biến cố không thể ($P=0$).
   - Công thức xác suất cổ điển: khi các kết quả đồng khả năng thì $P(A)=\dfrac{n(A)}{n(\Omega)}$ ($0 \le P(A) \le 1$).
   - Cách lập không gian mẫu 2 hành động độc lập (bảng hai chiều hàng $\times$ cột hoặc sơ đồ cây) và quy tắc đếm $n(\Omega)=m\cdot n$; phân biệt cặp có thứ tự $(a;b)$ với $(b;a)$.

## Dữ liệu đầu vào
'''


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bank = cc.load_bank()
    lai = None
    if "--lai" in sys.argv:
        idx = sys.argv.index("--lai")
        lai = set(sys.argv[idx + 1].split(","))

    cau_data = []
    for phieu, vai, dang, muc, so_y, so_nb, loai_r, ma, y, ht in cc.R:
        if lai is not None and ma not in lai:
            continue
        r = bank[ma]
        cau_data.append({
            "ma": ma,
            "vai_tro": vai,
            "dang": dang,
            "muc": muc,
            "so_y": so_y,
            "so_nb": so_nb,
            "loai": loai_r,
            "y_boc": y,
            "hinh_thuc": ht,
            "loai_nguon": cc.loai_nguon(r["uu"]),
            "nguon": r["nguon"],
            "de": r["de"],
        })

    vid_cc = "cc-ch8-9c-lai" if lai is not None else "cc-ch8-9c"
    if "--ten" in sys.argv:  # đợt chấm lại thứ 2 trở đi: không ghi đè file lai cũ
        vid_cc = sys.argv[sys.argv.index("--ten") + 1]
    viec_cc = {
        "id": vid_cc,
        "model": MODEL,
        "prompt": PROMPT_CC.replace("{SO}", str(len(cau_data)))
        + json.dumps(cau_data, ensure_ascii=False, indent=1)
        + "\n",
        "files": [],
        "schema": "scripts/gemini/schema/cham-chon-cau.json",
        "timeout": "1500s",
        "meta": {"loai": "cham-chon-cau", "chuong": "lop-9-dai-so-08", "ma": [d["ma"] for d in cau_data]},
    }
    (OUT_DIR / f"{vid_cc}.json").write_text(json.dumps(viec_cc, ensure_ascii=False, indent=1))
    print(vid_cc, len(cau_data), "câu", len(viec_cc["prompt"]), "kí tự")

    if lai is None:
        key_order = [
            {
                "key": f"{d}|{nhom}",
                "band": band,
                "loai": loai,
                "goi_y": tm.DONG_MO_TA[f"{d}|{nhom}"],
            }
            for d, nhom, band, loai, decomp, lt in tm.NHOM_DONG
        ]
        # Gửi kèm tóm tắt bảng chọn câu để Gemini viết vidu / d_text chính xác
        tm_input = {
            "KEY_ORDER": key_order,
            "SO_LIEU_DE_THI": SO_LIEU_DE_THI,
            "VI_DU_CHON": [
                {"dang": r[2], "muc": r[3], "so_y": r[4], "so_nb": r[5], "ma": r[7], "y": r[8], "de": bank[r[7]]["de"]}
                for r in cc.R
                if r[1] == "Ví dụ"
            ],
            "TREN_LOP_VA_BTVN": [
                {"vai": r[1], "dang": r[2], "muc": r[3], "so_y": r[4], "so_nb": r[5], "loai": r[6], "ma": r[7], "y": r[8]}
                for r in cc.R
                if r[1] != "Ví dụ"
            ],
        }
        vid_chu = "tm-ch8-9c-chu"
        viec_chu = {
            "id": vid_chu,
            "model": MODEL,
            "prompt": PROMPT_CHU.replace("{SO_DONG}", str(len(key_order)))
            + json.dumps(tm_input, ensure_ascii=False, indent=1)
            + "\n",
            "files": [],
            "schema": "scripts/gemini/schema/chu-tm-chuong.json",
            "timeout": "1500s",
            "meta": {"loai": "chu-tm-chuong", "chuong": "lop-9-dai-so-08"},
        }
        (OUT_DIR / f"{vid_chu}.json").write_text(json.dumps(viec_chu, ensure_ascii=False, indent=1))
        print(vid_chu, len(key_order), "dòng", len(viec_chu["prompt"]), "kí tự")


if __name__ == "__main__":
    main()
