#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 1 ch.VIII 9C (19/11/2026) — 3 việc: lý thuyết + mở đầu, trên lớp, BTVN.

Sơ đồ (ĐỀ chốt, hình máy vẽ, thẻ, dang_id, đáp số máy kiểm) do Claude chốt ở so_do_p1_ch8_9c.py.
Gemini viết: lời giải, ví dụ điền khuyết, mở đầu / nhắc lại / kiến thức cần nhớ (đọc ảnh SGK) / ghi chú GV.

    .venv/bin/python scripts/gemini/viec_dung_p1_ch8_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p1-ch8-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p1_ch8_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch8_9c import KHOI, cho_tho  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
        "phieu-1-phep-thu-khong-gian-mau-xac-suat-cua-bien-co.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p1-ch8-9c-lt", "dung-p1-ch8-9c-lop", "dung-p1-ch8-9c-btvn"
TEP = "storage/gemini/tep/p1-ch8-9c"
TRANG_LT = [56, 57, 58, 59, 60, 61, 62]
TRANG_LOP = [57, 58, 60, 61, 62]
TRANG_BTVN = [61, 62]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = cho_tho(next(k[8] for k in KHOI if k[0] == "Bài 24."))

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (ĐẠI SỐ — chương VIII "Xác suất của biến cố trong một số mô hình xác suất đơn giản", một buổi 180 phút gồm Bài 25 Phép thử ngẫu nhiên và không gian mẫu, Bài 26 Xác suất của biến cố liên quan tới phép thử; SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Lớp 9C không học: lấy đồng thời hai vật, lấy lần lượt không hoàn lại, phép thử ba hành động. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao — tên file = số trang IN).

## Luật cứng (vi phạm bị trả lại)
- Kí hiệu theo SGK: không gian mẫu $\Omega$, số phần tử $n(\Omega)$, số kết quả thuận lợi $n(A)$, xác suất $P(A)=\dfrac{n(A)}{n(\Omega)}$. Kết quả của phép thử hai hành động viết là cặp theo đúng kiểu SGK trong ảnh (ví dụ $(2, 5)$, $(S, 3)$). Tập hợp viết trong $…$ bằng \{ \}, các phần tử cách nhau dấu chấm phẩy như SGK (ví dụ $\Omega=\{1; 2; 3; 4; 5; 6\}$ — dấu ";" CHỈ được dùng bên trong $…$). Xác suất ghi phân số tối giản.
- Phân số \dfrac chỉ đặt ở dòng riêng (dòng con bắt đầu bằng "[[br]]\hspace*{1.4em}"), trong câu chảy dùng \frac.
- KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$. NGOÀI $…$ KHÔNG dấu chấm phẩy ";" (liệt kê dùng dấu phẩy). Số thập phân dấu phẩy $0{,}22$, phần trăm "$35\%$".
- CẤM chữ: "khuôn", "dạng đề", "Câu I", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK (đọc ảnh): mỗi bước một dòng, dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng). Nhịp một bài tính xác suất: "Có $n(\Omega)=…$ kết quả có thể, các kết quả này đồng khả năng." → "Các kết quả thuận lợi cho biến cố $A$ là …" (liệt kê) → "nên $n(A)=…$" → dòng riêng "$P(A)=\dfrac{…}{…}=…$" → "Vậy …". Nối bằng "nên" trong câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu a), …". Dòng "Vậy …" riêng ở cuối mỗi bài (mỗi ý nếu bài nhiều ý).
- BẢNG trong lời giải (bảng hai chiều liệt kê không gian mẫu): KHÔNG viết tabular. Viết đúng một dòng riêng "[[bang: Lần 1 \textbackslash{} Lần 2 | 1 | 2 | 3 / 1 | $(1, 1)$ | $(1, 2)$ | $(1, 3)$ / …]]" (các ô cách nhau " | ", các hàng cách nhau " / ", ô đầu mỗi hàng là tên hàng, ô có công thức bọc $…$). Ô góc trên trái viết "Lần 1, Lần 2" hoặc "Túi I, Túi II" (KHÔNG dùng dấu "/" hay "\" trong ô). Dòng chứa bảng KHÔNG có chữ nào khác.
- Toán trong $…$, chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy kiểm — dùng ĐÚNG. Vẫn tự đếm lại; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "7–9 ô", "Vậy", "hints", "Thầy 19/11", "đổi tên", "ĐỌC ẢNH", "sơ đồ", "lời thừa") là cho người soạn, KHÔNG in.
- Trong đề, chỗ "[HÌNH/BẢNG: …]" là mô tả hình/bảng đã vẽ sẵn trên phiếu — đọc số liệu ở đó, KHÔNG chép mô tả vào lời giải.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — người lắp tự in đề, bạn KHÔNG chép đề)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác. Ý [NB] 1–2 dòng. Ý [TH] làm đủ theo nhịp bài thi, mở đầu "Theo câu a), …" khi dùng kết quả ý trước, KHÔNG chép lại dòng của ý trước.
- Liệt kê kết quả thuận lợi luôn viết rõ (không chỉ ghi số lượng), ví dụ "Các kết quả thuận lợi cho biến cố $A$ là $3$, $6$ nên $n(A)=2$."
- Trắc nghiệm: solution 1–2 dòng, kết "Chọn B." Đúng/Sai: mỗi ý một dòng "a) Đúng. …" / "b) Sai. …" (một lí do ngắn). Bài trắc nghiệm, Đúng/Sai, trả lời ngắn KHÔNG cần dòng "Vậy".
- "hints" (mảng chuỗi): chỉ điền khi GHI CHÚ có "hints:" — câu hỏi gợi ý ngắn đúng như ghi chú, KHÔNG gọi tên công thức thay học sinh. Bài khác để [].
- Đầu ra mỗi bài: {"label":"Bài N.","statement":"","solution":"a) …[[br]]\hspace*{1.4em}…[[br]]b) …","hints":[]}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}. CHỈ phần lời giải — người lắp tự in "Ví dụ N." và đề phía trước.
- Ví dụ nhiều ý: mỗi ý bắt đầu dòng "a) …", "b) …".
- Khoét đúng số ô [[fill:đáp án]] ghi trong ghi chú (ít nhất 4), ở chỗ giáo viên hỏi lớp: $n(\Omega)$, các kết quả thuận lợi, $n(A)$, tử/mẫu của xác suất, kết quả rút gọn, cụm kết luận (xảy ra / không xảy ra, đồng khả năng / không). Ô có thể nằm trong bảng "[[bang: … ]]", khoét MỘT số trong cặp, vd "[[bang: Túi I, Túi II | 5 | 6 / 2 | $(2, 5)$ | $(2, [[fill:6]])$]]" (chú ý cuối là "]]" của ô rồi "]]" của bảng).
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$n(\Omega)=[[fill:20]]$", "$P(A)=\dfrac{[[fill:3]]}{[[fill:20]]}$"). Ô ngoài $…$ mà chứa công thức thì viết "$[[fill:\frac{1}{3}]]$" (dấu $ bọc NGOÀI ô, không bao giờ "[[fill:$…$]]").
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


def anh(ds):
    return [f"{TEP}/sgk9t2-tr{p}.png" for p in ds]


PROMPT_LT = CHUNG + r'''
## Việc A: mở đầu, nhắc lại, KIẾN THỨC CẦN NHỚ (đọc ảnh SGK), ghi chú giáo viên
Được giao ảnh SGK Toán 9 tập hai: ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_LT) + r'''. ĐỌC ẢNH để chép đúng chữ SGK và ghi đúng trang.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối [[br]]): chép đề đích (Bài 24 cuối Luyện tập 2, đề tuyển sinh lớp 10 Hà Nội 2025--2026, chỉ phần chữ trước "Xét biến cố", rồi hỏi "Tính xác suất của biến cố $A$: …") trong \emph{\textquotedblleft…\textquotedblright}, rồi nêu: để làm bài cần biết phép thử là gì, không gian mẫu có bao nhiêu phần tử, các kết quả thuận lợi cho biến cố là những kết quả nào, và công thức tính xác suất. Kết: đó là nội dung buổi học, đề này là Bài 24. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (Nhắc lại — chỉ kiến thức ĐÃ HỌC ở lớp dưới, dùng trong buổi), mỗi mục một dòng "$\bullet$\; …" nối [[br]]: biến cố, kết quả thuận lợi, công thức xác suất của biến cố khi các kết quả đồng khả năng (Toán 8) · số nguyên tố (số $1$ không phải số nguyên tố, $2$ là số nguyên tố chẵn duy nhất), số chính phương, ước và bội, số chia cho $k$ dư $r$ có dạng $kq+r$ (Toán 6) · đếm các số tự nhiên liên tiếp từ $a$ đến $b$: có $b-a+1$ số · tần số tương đối của một giá trị (chương VII).
3. "concept_blocks" (Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT ĐÚNG CHỮ SGK (chép khung định nghĩa / kết luận trong ảnh), mỗi mục hai khối {"type":"para","variant":"heading","text":"N. Tên"} rồi {"type":"para","text":"<nội dung>"}; cuối nội dung ghi "\textit{(SGK Toán 9 tập hai, tr.N)}" theo tên file ảnh có chữ đó. 4 mục:
   1. Phép thử ngẫu nhiên và không gian mẫu (Bài 25): khái niệm phép thử ngẫu nhiên, không gian mẫu $\Omega$ (chép khung SGK).
   2. Cách mô tả không gian mẫu của phép thử hai hành động: kết quả là cặp, liệt kê bằng bảng (theo SGK Bài 25, chỉ nói cách làm SGK nêu, không thêm mẹo).
   3. Kết quả thuận lợi cho biến cố (Bài 26, chép khung SGK).
   4. Cách tính xác suất của một biến cố khi các kết quả của phép thử đồng khả năng: công thức $P(E)=\dfrac{k}{n}$ hoặc kí hiệu SGK dùng (chép đúng khung và các bước SGK nêu, ghi trang).
   KHÔNG thêm mẹo, lỗi hay gặp, cấu trúc đề thi. Nhiều ý xuống dòng bằng [[br]], không dùng ";" ngoài $…$.
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 10 phút — đọc đề đích, chỉ ra các việc cần làm, chưa giải. Nhắc nhanh mục Nhắc lại (số nguyên tố, chia có dư).
   concept: 15 phút — mục 1, 3, 4 là trọng tâm. Hỏi ngay: gieo một con xúc xắc có bao nhiêu kết quả, các kết quả có đồng khả năng không, gieo hai lần thì kết quả viết thế nào.
   practice1: khoảng 45 phút — câu nhỏ trắc nghiệm, Đúng/Sai, trả lời ngắn, gọi nhiều học sinh trả lời miệng, chữa nhanh. Ví dụ 1–7 giáo viên làm cùng lớp, học sinh điền ô.
   practice2: khoảng 90 phút — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm ngay bài sau, câu hỏi dẫn trả lời miệng, ý chính tự trình bày vào vở. Mạch 7 nhấn bảng hai chiều. Bài 24 (đề đích) làm cá nhân như đi thi rồi gọi lên bảng.
   reflection: sơ đồ tư duy 5 phút cuối buổi. Bài tập về nhà Bài 25--49 in thành phiếu riêng, khoảng 90 phút. Buổi sau chữa Bài 42, Bài 48 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp (Bài 1–24, Ví dụ 1–13)
Được giao ảnh SGK ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_LOP) + r''' để theo đúng nhịp và kí hiệu lời giải SGK.
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 25–49)
Được giao ảnh SGK ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_BTVN) + r''' để theo đúng nhịp lời giải SGK.
Đầu ra {"sua":[25 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", anh(TRANG_LT)),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", anh(TRANG_LOP)),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", anh(TRANG_BTVN))]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p1-ch8-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
