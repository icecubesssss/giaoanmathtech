#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 2 ch.VIII 9C — Ôn tập chương VII + VIII (19/11/2026). 3 việc: mở đầu + ghi chú GV,
lời giải trên lớp (Bài 1–21, Ví dụ 1–7), lời giải BTVN (Bài 22–42).

Sơ đồ (ĐỀ chốt, hình máy vẽ, thẻ, đáp số máy kiểm) do Claude chốt ở so_do_on_78_9c.py. Kiến thức cần nhớ lấy
nguyên văn từ hai Phiếu 1 (ch.VII, ch.VIII) đã dựng — Gemini KHÔNG viết lại.

    .venv/bin/python scripts/gemini/viec_dung_on_78_9c.py
    python3 scripts/gemini/tho.py --song-song 3 --tien-to dung-on78-9c
    .venv/bin/python scripts/gemini/lap_on_78_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_on_78_9c import KHOI, cho_tho  # noqa: E402

SEED = ("inputs/seeds/lop-9/dai-so/lop-c/chuong-08-xac-suat-cua-bien-co/"
        "phieu-2-on-tap-chuong-vii-viii.json")
VID_LT, VID_LOP, VID_BTVN = "dung-on78-9c-lt", "dung-on78-9c-lop", "dung-on78-9c-btvn"
ANH_LOP = ["storage/gemini/tep/p1-ch7-9c/sgk9t2-tr38.png", "storage/gemini/tep/p1-ch7-9c/sgk9t2-tr47.png",
           "storage/gemini/tep/p1-ch8-9c/sgk9t2-tr61.png", "storage/gemini/tep/p1-ch8-9c/sgk9t2-tr62.png"]
MODEL = "gemini-4-hydrogen-medium"

DE_DICH = cho_tho(next(k[8] for k in KHOI if k[0] == "Bài 21."))

CHUNG = r'''Bạn là thợ soạn PHIẾU ÔN TẬP Toán 9 (ĐẠI SỐ — ôn tập chương VII "Tần số và tần số tương đối" (Bài 22, 23, 24) và chương VIII "Xác suất của biến cố trong một số mô hình xác suất đơn giản" (Bài 25, 26); SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). Phần ôn tập dài 135 phút, ngay sau đó học sinh làm bài kiểm tra 45 phút gộp hai chương. Ôn NHƯ ĐI THI: bài thông hiểu không có câu hỏi dẫn, không gợi ý. Lớp 9C không học: vẽ biểu đồ, giá trị đại diện, lấy đồng thời hai vật, lấy lần lượt không hoàn lại, phép thử ba hành động. KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK nếu được giao — tên file = số trang IN).

## Luật cứng (vi phạm bị trả lại)
- Kí hiệu thống kê theo SGK: cỡ mẫu $n$ (bảng ghi "Tổng" hoặc "Cộng"), tần số $m$, tần số tương đối $f=\dfrac{m}{n}\cdot 100\%$, nhóm $[a; b)$. Bảng tần số tương đối viết phần trăm ($37{,}5\%$). Tính tần số tương đối viết từng phép tính, ví dụ "$f_1=\dfrac{15}{40}\cdot 100\%=37{,}5\%$".
- Kí hiệu xác suất theo SGK: không gian mẫu $\Omega$, số phần tử $n(\Omega)$, số kết quả thuận lợi $n(A)$, xác suất $P(A)=\dfrac{n(A)}{n(\Omega)}$. Kết quả của phép thử hai hành động viết là cặp theo đúng kiểu SGK trong ảnh (ví dụ $(2, 5)$, $(S, 3)$). Tập hợp viết trong $…$ bằng \{ \}, các phần tử cách nhau dấu chấm phẩy như SGK (ví dụ $\Omega=\{1; 2; 3; 4; 5; 6\}$ — dấu ";" CHỈ được dùng bên trong $…$). Xác suất ghi phân số tối giản.
- Phân số \dfrac chỉ đặt ở dòng riêng (dòng con bắt đầu bằng "[[br]]\hspace*{1.4em}"), trong câu chảy dùng \frac.
- KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$. NGOÀI $…$ KHÔNG dấu chấm phẩy ";" (liệt kê dùng dấu phẩy). Số thập phân dấu phẩy $0{,}22$, phần trăm "$35\%$".
- CẤM chữ: "khuôn", "dạng đề", "Câu I", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK (đọc ảnh): mỗi bước một dòng, dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng). Nhịp một bài lập bảng: "Cỡ mẫu là $n=…$." → mỗi tần số tương đối một dòng riêng → dòng bảng "[[bang: …]]" → "Vậy bảng tần số tương đối … như trên." Nhịp một bài tính xác suất: "Có $n(\Omega)=…$ kết quả có thể, các kết quả này đồng khả năng." → "Các kết quả thuận lợi cho biến cố $A$ là …" (liệt kê) → "nên $n(A)=…$" → dòng riêng "$P(A)=\dfrac{…}{…}=…$" → "Vậy …". Nối bằng "nên" trong câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu a), …". Dòng "Vậy …" riêng ở cuối mỗi bài (mỗi ý nếu bài nhiều ý).
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
- "hints" LUÔN là [] (phiếu ôn như đi thi, không gợi ý).
- Lời giải bài thông hiểu là lời giải mẫu HS phải viết được trong bài thi (không lời dẫn kiểu "Ta cần…", "Bước 1").
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
        dau = f"- {nhan} " + ("(VÍ DỤ)" if ht == "vi_du" else f"tier={tier} level={level} hình thức={ht}")
        dong.append(f"{dau} mã={ma}\n    ĐỀ: {cho_tho(de)}\n    GHI CHÚ: {ghi}")
    return "\n".join(dong)


PROMPT_LT = CHUNG + r'''
## Việc A: mở đầu, nhắc lại, ghi chú giáo viên (KHÔNG viết kiến thức cần nhớ)
Đầu ra JSON: {"opener_text","review_note","concept_blocks":[],"mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}.

1. "opener_text" (chặng Khám phá, 4–6 dòng nối [[br]]): chép đề đích (Bài 21 cuối Luyện tập 2 — Câu I đề học kì II THCS Bế Văn Đàn 2025--2026, gồm ý 1 về biểu đồ tần số ghép nhóm và ý 2 về xác suất) ngắn gọn trong \emph{\textquotedblleft…\textquotedblright} (ý 1 chỉ nói "cho biểu đồ tần số ghép nhóm cân nặng của $40$ học sinh", không chép số liệu), rồi nêu: để làm trọn câu này cần đọc được tần số, tính tần số tương đối, viết được không gian mẫu, liệt kê kết quả thuận lợi và tính xác suất. Kết: phiếu ôn lại toàn bộ hai chương theo đúng thứ tự đó, đề này là Bài 21. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (Nhắc lại — kiến thức lớp dưới dùng trong phiếu), mỗi mục một dòng "$\bullet$\; …" nối [[br]], 3 mục: tỉ số phần trăm $\dfrac{a}{b}\cdot 100\%$ và làm tròn (Toán 6, 7) · đọc số liệu trên bảng, biểu đồ cột, biểu đồ cột kép, biểu đồ tranh, biểu đồ đoạn thẳng (Toán 6, 7, 8) · số nguyên tố, số chính phương, ước và bội, số chia cho $k$ dư $r$ có dạng $kq+r$, đếm các số tự nhiên liên tiếp từ $a$ đến $b$ có $b-a+1$ số (Toán 6).
3. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 5 phút — đọc đề đích, chỉ ra các việc cần làm, chưa giải.
   concept: 10 phút — gọi học sinh nhắc lại từng mục kiến thức cần nhớ (công thức tần số tương đối, nhóm $[a; b)$ không chứa $b$, công thức xác suất, viết kết quả hai hành động thành cặp).
   practice1: khoảng 35 phút — Bài 1--13 trả lời nhanh, gọi nhiều học sinh trả lời miệng, chữa nhanh các lỗi: quên nhân $100\%$, lấy cả đầu mút phải vào nhóm, quên số $1$ không phải số nguyên tố.
   practice2: khoảng 80 phút — mỗi mạch giáo viên làm ví dụ cùng lớp (học sinh điền ô), rồi học sinh tự làm bài sau như đi thi, không gợi ý, giáo viên gọi lên bảng chữa. Bài 21 (đề đích) làm cá nhân trong $10$ phút như đi thi.
   reflection: sơ đồ tư duy 5 phút cuối phần ôn tập, sau đó học sinh làm bài kiểm tra $45$ phút. Bài tập về nhà Bài 22--42 in thành phiếu riêng, khoảng 90 phút.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp (Bài 1–21, Ví dụ 1–7)
Được giao ảnh SGK (sgk9t2-tr38, tr47: bảng tần số tương đối / ghép nhóm; tr61, tr62: tính xác suất) để theo đúng nhịp và kí hiệu lời giải SGK.
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 22–42)
Đầu ra {"sua":[21 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", []),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", ANH_LOP),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", ANH_LOP[1:3])]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-on78-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
