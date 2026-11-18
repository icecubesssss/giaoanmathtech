#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 1 ch.VII 9C (18/11/2026) — 3 việc: lý thuyết + mở đầu, trên lớp, BTVN.

Sơ đồ (ĐỀ nguyên văn, bảng/biểu đồ máy vẽ, thẻ, dang_id, đáp số máy đếm) do Claude chốt ở so_do_p1_ch7_9c.py.
Gemini viết: lời giải, ví dụ điền khuyết, mở đầu / nhắc lại / kiến thức cần nhớ (đọc ảnh SGK) / ghi chú GV.

    .venv/bin/python scripts/gemini/viec_dung_p1_ch7_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p1-ch7-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p1_ch7_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch7_9c import KHOI, cho_tho  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-07-tan-so-va-tan-so-tuong-doi/"
        "phieu-1-bang-tan-so-tan-so-tuong-doi-ghep-nhom.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p1-ch7-9c-lt", "dung-p1-ch7-9c-lop", "dung-p1-ch7-9c-btvn"
TRANG = [33, 34, 35, 36, 37, 38, 39, 40, 41, 46, 47, 48, 49, 50, 51]
ANH = [f"storage/gemini/tep/p1-ch7-9c/sgk9t2-tr{p}.png" for p in TRANG]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = cho_tho(next(k[8] for k in KHOI if k[0] == "Bài 23."))

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VII "Tần số và tần số tương đối", một buổi 180 phút gồm Bài 22 Bảng tần số và biểu đồ tần số, Bài 23 Bảng tần số tương đối và biểu đồ tần số tương đối, Bài 24 Bảng tần số, tần số tương đối ghép nhóm và biểu đồ; SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Lớp 9C KHÔNG học vẽ biểu đồ (chỉ đọc biểu đồ). KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao).

## Luật cứng (vi phạm bị trả lại)
- Tần số tương đối viết theo SGK: $f=\dfrac{m}{n}\cdot 100\%$ ($m$ là tần số, $n$ là cỡ mẫu). Phân số \dfrac chỉ đặt ở dòng riêng (dòng con bắt đầu bằng "[[br]]\hspace*{1.4em}"), trong câu chảy dùng \frac.
- KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$. KHÔNG dấu chấm phẩy ";" (liệt kê dùng dấu phẩy). Số thập phân dấu phẩy $12{,}5\%$, phần trăm "$25\%$".
- CẤM chữ: "khuôn", "dạng đề", "Câu I", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK: mỗi bước một dòng; dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng); nối bằng "nên" trong cùng câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu a), …", "Cỡ mẫu là …", "Tần số tương đối của … là". Dòng "Vậy …" riêng ở cuối mỗi bài (mỗi ý nếu bài nhiều ý).
- BẢNG trong lời giải: KHÔNG viết tabular. Viết đúng một dòng riêng "[[bang: Cỡ giày | 36 | 37 | 38 / Tần số | 5 | 4 | 8]]" (các ô cách nhau " | ", các hàng cách nhau " / ", ô đầu mỗi hàng là tên hàng; ô có công thức thì bọc $…$, ví dụ "$[13; 15)$", "$12{,}5\%$"). Người lắp tự chuyển thành bảng. Dòng chứa bảng KHÔNG có chữ nào khác.
- Toán trong $…$, chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy đếm — dùng ĐÚNG. Vẫn tự đếm lại; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "7–9 ô", "MỘT bước", "Dòng Vậy", "tabular", "sơ đồ đã viết rõ") là cho người soạn, KHÔNG in.
- Trong đề, chỗ "[HÌNH/BẢNG: …]" là mô tả hình/bảng đã vẽ sẵn trên phiếu — đọc số liệu ở đó, KHÔNG chép mô tả vào lời giải.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — người lắp tự in đề, bạn KHÔNG chép đề)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác. Ý [NB] 1–2 dòng. Ý [TH] làm đủ, mở đầu "Theo câu a), …" khi dùng kết quả ý trước, KHÔNG chép lại dòng của ý trước.
- Đếm theo điều kiện thì viết rõ những giá trị / nhóm được lấy, ví dụ "Số học sinh đạt từ điểm $8$ trở lên gồm các điểm $8$, $9$, $10$ nên có $10+7+4=21$ học sinh."
- Trắc nghiệm (Bài 1): solution 1 dòng, kết "Chọn B."
- Đầu ra mỗi bài: {"label":"Bài N.","statement":"","solution":"a) …[[br]]\hspace*{1.4em}…[[br]]b) …"}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}. CHỈ phần lời giải — người lắp tự in "Ví dụ N." và đề phía trước.
- Ví dụ nhiều ý: mỗi ý bắt đầu dòng "a) …", "b) …".
- Khoét đúng số ô [[fill:đáp án]] ghi trong ghi chú, ở chỗ giáo viên hỏi lớp: tần số đếm được, cỡ mẫu, phép tính tần số tương đối, kết quả phần trăm, nhóm / giá trị được lấy theo điều kiện, kết luận. Ô có thể nằm trong bảng "[[bang: … ]]" (vd "[[bang: Cỡ giày | 36 | 37 / Tần số | [[fill:5]] | [[fill:4]]]]" — chú ý cuối là "]]" của ô rồi "]]" của bảng).
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$n=[[fill:40]]$", "$f=[[fill:25]]\%$"). Ô ngoài $…$ mà chứa công thức thì viết "$[[fill:12{,}5\%]]$" (dấu $ bọc NGOÀI ô, không bao giờ "[[fill:$…$]]").
- Một số đã nằm trong ô thì KHÔNG in sẵn (ngoài ô) ở dòng nào phía DƯỚI ô đó trong cùng ví dụ.
- Kết bằng dòng riêng "Vậy …" có ô ở giá trị kết luận. Ví dụ không có thẻ [NB]/[TH].
'''


def so_do(chang):
    dong = []
    for k in KHOI:
        if k[1] not in chang:
            continue
        if len(k) == 3:
            dong.append(f"- [TIÊU ĐỀ MẠCH — người lắp tự chèn] {k[0]}")
            continue
        nhan, _, tier, dang, level, ma, _, ht, de, ghi = k
        dau = f"- {nhan} " + ("(VÍ DỤ)" if ht == "vi_du" else f"tier={tier} dang_id={dang} level={level} hình thức={ht}")
        dong.append(f"{dau} mã={ma}\n    ĐỀ: {cho_tho(de)}\n    GHI CHÚ: {ghi}")
    return "\n".join(dong)


PROMPT_LT = CHUNG + r'''
## Việc A: mở đầu, nhắc lại, KIẾN THỨC CẦN NHỚ (đọc ảnh SGK), ghi chú giáo viên
Được giao ảnh SGK Toán 9 tập hai: ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG) + r'''. Tên file = số trang IN. ĐỌC ẢNH để chép đúng chữ SGK và ghi đúng trang.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối [[br]]): chép đề đích (Bài 23 cuối Luyện tập 2, đề giữa kì II THCS Nam Từ Liêm 2025--2026, phần chữ, KHÔNG chép mô tả biểu đồ — viết "(biểu đồ ở Bài 23)") trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: bài cần đọc biểu đồ để lập bảng tần số ghép nhóm, tính tần số tương đối của một nhóm, và đếm theo một điều kiện (trước khi hết giờ trên $20$ phút). Kết: ba việc đó là nội dung buổi học, đề này là Bài 23. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (Nhắc lại — chỉ kiến thức ĐÃ HỌC ở lớp dưới, dùng trong buổi), mỗi mục một dòng "$\bullet$\; …" nối [[br]]: đọc biểu đồ tranh, biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ hình quạt tròn (Toán 6, 7, 8) · tỉ số phần trăm của $a$ và $b$ là $\frac{a}{b}\cdot 100\%$, giá trị $p\%$ của số $N$ là $N\cdot p\%$ (Toán 6) · đọc điều kiện "ít hơn", "nhiều hơn", "từ … trở lên", "ít nhất", "dưới" (có lấy hay không lấy số mốc).
3. "concept_blocks" (Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT ĐÚNG CHỮ SGK (chép khung định nghĩa / kết luận trong ảnh), mỗi mục hai khối {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi "\textit{(SGK Toán 9 tập hai, tr.N)}" theo tên file ảnh có chữ đó. 5 mục:
   1. Mẫu dữ liệu, cỡ mẫu, tần số, bảng tần số (Bài 22). Bảng mẫu viết bằng "[[bang: Giá trị | $x_1$ | $x_2$ | $\ldots$ | $x_k$ / Tần số | $m_1$ | $m_2$ | $\ldots$ | $m_k$]]".
   2. Biểu đồ tần số dạng cột, dạng đoạn thẳng (Bài 22) — chỉ nói biểu đồ biểu diễn gì và cách ĐỌC tần số từ biểu đồ (không dạy vẽ).
   3. Tần số tương đối, công thức, bảng tần số tương đối (Bài 23). Thêm một dòng (ghi "\textit{(suy ra từ công thức)}"): biết $f$ và $n$ thì $m=n\cdot f$.
   4. Mẫu số liệu ghép nhóm: nhóm $[a; b)$ (gồm các giá trị $x$ với $a\le x<b$, đầu mút phải không thuộc nhóm), tần số ghép nhóm, bảng tần số ghép nhóm, tần số tương đối ghép nhóm, bảng tần số tương đối ghép nhóm (Bài 24).
   5. Giá trị đại diện của nhóm $[a; b)$ là $\dfrac{a+b}{2}$ (chép đúng chỗ SGK nói, ghi trang).
   KHÔNG thêm mẹo, các bước làm bài, lỗi hay gặp, cấu trúc đề thi, cách vẽ biểu đồ. Nhiều ý xuống dòng bằng [[br]], không dùng ";".
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 10 phút — đọc đề đích, chỉ ra ba việc, chưa giải. Nhắc nhanh mục Nhắc lại.
   concept: 15 phút — mục 1, 3, 4 là trọng tâm. Hỏi ngay: tần số tương đối tính thế nào, giá trị $160$ thuộc nhóm $[150; 160)$ hay $[160; 170)$.
   practice1: khoảng 45 phút — câu nhỏ đọc bảng, đọc biểu đồ, gọi nhiều học sinh trả lời miệng, chữa nhanh. Ví dụ 1–4 giáo viên làm cùng lớp, học sinh điền ô.
   practice2: khoảng 105 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm ngay bài sau, câu hỏi dẫn trả lời miệng, ý chính tự trình bày vào vở. Bài 23 (đề đích) làm cá nhân như đi thi rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 24--44 in thành phiếu riêng, khoảng 85 phút. Buổi sau chữa Bài 40, Bài 42 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp (Bài 1–23, Ví dụ 1–10)
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 24–44)
Đầu ra {"sua":[21 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", ANH),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", []),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", [])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p1-ch7-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
