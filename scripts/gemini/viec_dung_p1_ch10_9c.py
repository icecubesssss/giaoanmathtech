#!/usr/bin/env python3
"""Giao Gemini dựng Phiếu 1 ch.X 9C (19/11/2026) — 3 việc: lý thuyết + mở đầu, trên lớp, BTVN.

Sơ đồ (ĐỀ chốt, hình máy vẽ, thẻ, dang_id, hints, đáp số máy kiểm) do Claude chốt ở so_do_p1_ch10_9c.py.
Gemini viết: lời giải, ví dụ điền khuyết, mở đầu / nhắc lại / thẻ lý thuyết (đọc ảnh SGK) / ghi chú GV.

    .venv/bin/python scripts/gemini/viec_dung_p1_ch10_9c.py
    python3 scripts/gemini/tho.py --song-song 3     (dung-p1-ch10-9c-lt / -lop / -btvn)
    .venv/bin/python scripts/gemini/lap_p1_ch10_9c.py [--ghi]
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_do_p1_ch10_9c import cho_tho, danh_so_hinh, khoi_bai, KHOI  # noqa: E402

SEED = ("inputs/seeds/lop-9/hinh-hoc/lop-c/chuong-10-hinh-khoi-trong-thuc-tien/"
        "phieu-1-hinh-tru-hinh-non-hinh-cau.json")
VID_LT, VID_LOP, VID_BTVN = "dung-p1-ch10-9c-lt", "dung-p1-ch10-9c-lop", "dung-p1-ch10-9c-btvn"
TEP = "storage/gemini/tep/p1-ch10-9c"
TRANG_LT = [94, 95, 96, 97, 98, 99, 101, 102, 103, 104]
TRANG_LOP = [96, 97, 99, 103, 104]
TRANG_BTVN = [96, 99, 102, 103]
MODEL = "gemini-4-hydrogen-medium"

SO = danh_so_hinh()
DE_DICH = cho_tho(next(k for k in khoi_bai() if k["nhan"] == "Bài 9."), SO)

CHUNG = r'''Bạn là thợ soạn phiếu học tập Toán 9 (HÌNH HỌC — chương X "Một số hình khối trong thực tiễn", một buổi 90 phút gồm Bài 31 Hình trụ và hình nón, Bài 32 Hình cầu; SGK Kết nối tri thức với cuộc sống, tập hai) cho học sinh lớp 9 TẦNG C (học lực trung bình yếu). KHÔNG chạy lệnh. Mọi dữ liệu nằm trong prompt (và các ảnh trang SGK được giao — tên file = số trang IN).

## Luật cứng (vi phạm bị trả lại)
- Kí hiệu theo SGK: bán kính đáy $r$ (hình cầu $R$), chiều cao $h$, đường sinh $l$, diện tích xung quanh $S_{xq}$, diện tích mặt cầu $S$, thể tích $V$. Công thức: $S_{xq}=2\pi rh$, $V=\pi r^2h$ (trụ) · $S_{xq}=\pi rl$, $V=\frac{1}{3}\pi r^2h$ (nón) · $S=4\pi R^2$, $V=\frac{4}{3}\pi R^3$ (cầu).
- Đơn vị ghi trong ngoặc sau kết quả như SGK: "$=310{,}86$ (cm$^3$)". Phép nhân viết \cdot. Số thập phân dấu phẩy $3{,}14$, $0{,}5$. Đề cho "lấy $\pi\approx 3{,}14$" thì thay $3{,}14$ và dùng \approx. Đề KHÔNG cho giá trị $\pi$ thì giữ $\pi$ (vd $400\pi$), chỉ làm tròn khi đề yêu cầu.
- Phân số \dfrac chỉ đặt ở dòng riêng (dòng con bắt đầu bằng "[[br]]\hspace*{1.4em}"), trong câu chảy dùng \frac.
- KHÔNG dấu $\Leftrightarrow$, $\Rightarrow$. NGOÀI $…$ KHÔNG dấu chấm phẩy ";" (liệt kê dùng dấu phẩy).
- CẤM chữ: "khuôn", "dạng đề", "Câu IV", điểm số, "thang điểm", "tầng C", "mẹo", "chìa khóa", "bẫy", "Do đó", "do đó", "Suy ra", "suy ra", "Mặt khác", "Như vậy". CẤM xưng hô và văn nói: "em", "các em", "ta đi", "hôm nay", "buổi này", "Kiểm" (viết "Kiểm tra"), "Soi", "nhé", "nào". Không chữ IN HOA để nhấn.
- Lời giải theo NHỊP BÀI THI giống SGK (đọc ảnh): mỗi bước một dòng, dòng con mở đầu "[[br]]\hspace*{1.4em}" ("\hspace*" chỉ đứng ĐẦU dòng). Nhịp một bài tính: (đổi đường kính nếu cần) "Bán kính đáy của … là $r=6:2=3$ (cm)." → "Thể tích của … là" rồi dòng "$V=\pi r^2h\approx 3{,}14\cdot 3^2\cdot 11=310{,}86$ (cm$^3$)." → "Vậy …". Nối bằng "nên" trong câu, hoặc mở dòng bằng "Ta có …", "Khi đó …", "Theo câu a), …". Dòng "Vậy …" riêng ở cuối mỗi bài (mỗi ý nếu bài nhiều ý).
- Toán trong $…$, chuỗi JSON hợp lệ (gạch chéo ngược nhân đôi). Escape \& trong "GD\&ĐT". "2024--2025" giữ hai gạch.
- Số liệu và đáp số trong GHI CHÚ của sơ đồ đã được máy kiểm — dùng ĐÚNG. Vẫn tự tính lại; thấy lệch thì ghi vào "ghi_chu", không tự sửa số. Chữ trong ghi chú (như "4 ô", "Vậy", "ĐỌC ẢNH", "sơ đồ", "1–2 dòng", "⇒", "·") là cho người soạn, KHÔNG in.
- Trong đề, chỗ "[HÌNH ĐÃ VẼ SẴN: …]" là mô tả hình đã vẽ trên phiếu — đọc số liệu ở đó, KHÔNG chép mô tả vào lời giải.
'''

LUAT_LOI_GIAI = r'''
## Luật lời giải của BÀI (đề đã chốt — người lắp tự in đề, bạn KHÔNG chép đề)
- Mỗi ý trả lời ĐÚNG cái được hỏi, không thêm việc khác. Ý [NB] 1–3 dòng. Ý [TH], [VD] làm đủ theo nhịp bài thi, mở đầu "Theo câu a), …" khi dùng kết quả ý trước, KHÔNG chép lại dòng của ý trước.
- Trắc nghiệm: solution 1–2 dòng, kết "Chọn B." Bài trắc nghiệm KHÔNG cần dòng "Vậy".
- "hints": trả [] (người lắp đã có câu hỏi gợi ý).
- Đầu ra mỗi bài: {"label":"Bài N.","statement":"","solution":"a) …[[br]]\hspace*{1.4em}…[[br]]b) …","hints":[]}.
'''

LUAT_VI_DU = r'''
## Luật VÍ DỤ (giáo viên làm cùng lớp — CHỈ ví dụ được điền khuyết)
- Đầu ra: {"label":"Ví dụ N.","statement":"{\\sffamily\\bfseries\\color{brand}Lời giải}[[br]]\\hspace*{1.4em}<dòng 1>[[br]]\\hspace*{1.4em}<dòng 2>…[[br]]\\hspace*{1.4em}Vậy …","solution":""}. CHỈ phần lời giải — người lắp tự in "Ví dụ N.", đề và hình phía trước.
- Ví dụ nhiều ý: mỗi ý bắt đầu dòng "a) …", "b) …".
- Khoét đúng số ô [[fill:đáp án]] ghi trong ghi chú (ít nhất 4), ở chỗ giáo viên hỏi lớp: công thức, số thay vào (bán kính sau khi chia đôi đường kính, chiều cao phần nước), kết quả, số đổi đơn vị.
- Ô trong $…$ thì đáp án KHÔNG bọc $ (vd "$V=[[fill:\pi r^2h]]$", "$r=6:2=[[fill:3]]$"). Ô ngoài $…$ mà chứa công thức thì viết "$[[fill:400\pi]]$" (dấu $ bọc NGOÀI ô, không bao giờ "[[fill:$…$]]").
- Một số đã nằm trong ô thì KHÔNG in sẵn (ngoài ô) ở dòng nào phía DƯỚI ô đó trong cùng ví dụ.
- Kết bằng dòng riêng "Vậy …" có ô ở giá trị kết luận. Ví dụ không có thẻ [NB]/[TH]/[VD].
'''


def so_do(chang):
    dong = []
    for k in KHOI:
        if k.get("chang") not in chang:
            continue
        if "tieu_de" in k:
            dong.append(f"- [TIÊU ĐỀ MẠCH — người lắp tự chèn] {k['tieu_de']}")
            continue
        dau = f"- {k['nhan']} " + ("(VÍ DỤ)" if k["ht"] == "vi_du" else
                                   f"tier={k['tier']} dang_id={k['dang']} level={k['level']} hình thức={k['ht']}")
        dong.append(f"{dau} mã={k['ma']}\n    ĐỀ: {cho_tho(k, SO)}\n    GHI CHÚ: {k['ghi']}")
    return "\n".join(dong)


def anh(ds):
    return [f"{TEP}/sgk9t2-tr{p}.png" for p in ds]


PROMPT_LT = CHUNG + r'''
## Việc A: mở đầu, nhắc lại, THẺ LÝ THUYẾT (đọc ảnh SGK), ghi chú giáo viên
Được giao ảnh SGK Toán 9 tập hai: ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_LT) + r'''. ĐỌC ẢNH để chép đúng chữ SGK và ghi đúng trang.
Đầu ra JSON: {"opener_text","review_note","concept_blocks","mindmap":{},"teacher_notes":{"review","concept","practice1","practice2","reflection"},"ghi_chu"}. ("mindmap" trả {} — người lắp tự dựng.)

1. "opener_text" (chặng Khám phá, 4–6 dòng nối [[br]]): chép phần đầu đề đích (Bài 9 cuối Luyện tập 2, đề kiểm tra học kì II THCS Đoàn Thị Điểm 2025--2026: ly hình trụ, nước cao $10$ cm, thả $5$ viên bi, tính bán kính mỗi viên bi) trong \emph{\textquotedblleft…\textquotedblright} (rút gọn, không chép phần công thức cho sẵn, không chép mô tả hình), rồi nêu: để làm bài cần biết hình trụ có thể tích tính thế nào, thể tích phần nước dâng lên liên hệ với thể tích các viên bi ra sao, và thể tích hình cầu tính thế nào. Kết: đó là nội dung buổi học, đề này là Bài 9. Không xưng hô, không điểm số.
   Đề đích: ''' + DE_DICH + r'''
2. "review_note" (Nhắc lại — chỉ kiến thức ĐÃ HỌC ở lớp dưới, dùng trong buổi), mỗi mục một dòng "$\bullet$\; …" nối [[br]]: bán kính bằng nửa đường kính $r=\frac{d}{2}$ · chu vi và diện tích hình tròn bán kính $r$: $C=2\pi r$, $S=\pi r^2$ (lớp 6) · định lí Pythagore trong tam giác vuông (lớp 8) · đổi đơn vị: $1$ m$^3=1000$ dm$^3=1000$ lít, $1$ dm$^3=1$ lít $=1000$ cm$^3$, $1$ cm $=10$ mm · làm tròn số đến hàng đơn vị, hàng phần mười, hàng phần trăm (lớp 7).
3. "concept_blocks" (Kiến thức cần nhớ) — CHỈ LÀ LÝ THUYẾT ĐÚNG CHỮ SGK, đúng 3 THẺ, mỗi thẻ một khối {"type":"noted","variant":"theory","title":"1. Hình trụ","text":"…"} (title "1. Hình trụ", "2. Hình nón", "3. Hình cầu"). Người lắp tự gắn hình (trụ có $r$, $h$ · nón có $S$, $O$, $A$, $r$, $h$, $l$ · cầu tâm $O$ bán kính $R$) bên phải mỗi thẻ — chữ viết gọn để vừa cột 63\% bề ngang.
   "text" mỗi thẻ gồm các dòng nối [[br]], mở mỗi dòng bằng nhãn "\nhanly{Tên.} " (có dấu cách sau "}"):
   - Thẻ 1: \nhanly{Tạo thành.} quay hình chữ nhật $ABCD$ một vòng quanh cạnh $AB$ cố định (chép ý SGK: đáy, bán kính đáy, chiều cao, đường sinh) · \nhanly{Diện tích xung quanh.} $S_{xq}=2\pi rh$ · \nhanly{Thể tích.} $V=\pi r^2h$ (SGK có $V=S_{\text{đáy}}\cdot h$ thì ghi cả hai).
   - Thẻ 2: \nhanly{Tạo thành.} quay tam giác $SOA$ vuông tại $O$ một vòng quanh $SO$ (đỉnh, bán kính đáy, đường sinh, đường cao — chép ý SGK) · \nhanly{Liên hệ.} $l^2=r^2+h^2$ (tam giác $SOA$ vuông tại $O$) · \nhanly{Diện tích xung quanh.} $S_{xq}=\pi rl$ · \nhanly{Thể tích.} $V=\frac{1}{3}\pi r^2h$.
   - Thẻ 3: \nhanly{Tạo thành.} quay nửa hình tròn tâm $O$, bán kính $R$ một vòng quanh đường kính cố định (tâm, bán kính, mặt cầu — chép ý SGK) · \nhanly{Diện tích mặt cầu.} $S=4\pi R^2$ · \nhanly{Thể tích.} $V=\frac{4}{3}\pi R^3$.
   Cuối mỗi thẻ một dòng "\textit{(SGK Toán 9 tập hai, tr.N)}" theo tên file ảnh có chữ đó. KHÔNG thêm mẹo, lỗi hay gặp, cấu trúc đề thi. Trong thẻ chỉ dùng \frac (không \dfrac).
4. "teacher_notes" (ngắn, cách tổ chức dạy, không điểm số):
   review: 3 phút — đọc đề đích Bài 9, chỉ ra các việc cần làm, chưa giải. Nhắc nhanh mục Nhắc lại (đường kính, đổi đơn vị).
   concept: 5 phút — ba thẻ: gọi học sinh đọc công thức, chỉ trên hình đâu là $r$, $h$, $l$. Phân biệt chiều cao $h$ với đường sinh $l$ của hình nón.
   practice1: khoảng 20 phút — Ví dụ 1, 2 giáo viên làm cùng lớp, học sinh điền ô. Bài 1–6 trắc nghiệm và trả lời ngắn, gọi nhiều học sinh trả lời miệng, chữa nhanh, nhắc đổi đường kính ra bán kính.
   practice2: khoảng 50 phút (giải lao 10 phút giữa hai chặng luyện tập) — mỗi mạch giáo viên làm ví dụ cùng lớp rồi học sinh làm ngay bài sau, ý [NB] trả lời miệng, ý [TH] tự trình bày vào vở theo câu hỏi gợi ý. Mạch 5 nhấn: thể tích vật chìm bằng thể tích phần nước dâng lên. Bài 9 (đề đích) làm cá nhân như đi thi rồi gọi lên bảng.
   reflection: sơ đồ tư duy 2 phút cuối buổi. Bài tập về nhà Bài 10--16 in thành phiếu riêng, khoảng 40 phút. Buổi sau chữa Bài 14, Bài 16 trước.
'''

PROMPT_LOP = CHUNG + LUAT_LOI_GIAI + LUAT_VI_DU + r'''
## Việc B: lời giải các bài và ví dụ của 2 chặng LUYỆN TẬP trên lớp (Bài 1–9, Ví dụ 1–5)
Được giao ảnh SGK ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_LOP) + r''' để theo đúng nhịp và kí hiệu lời giải SGK.
Đầu ra {"sua":[…mọi Ví dụ và Bài theo đúng thứ tự sơ đồ…],"ghi_chu":"…"}. Không trả tiêu đề mạch.

## Sơ đồ (đúng thứ tự)
''' + so_do({"practice1", "practice2"}) + "\n"

PROMPT_BTVN = CHUNG + LUAT_LOI_GIAI + r'''
## Việc C: lời giải BÀI TẬP VỀ NHÀ (Bài 10–16)
Được giao ảnh SGK ''' + ", ".join(f"sgk9t2-tr{p}.png" for p in TRANG_BTVN) + r''' để theo đúng nhịp lời giải SGK.
Đầu ra {"sua":[7 bài theo đúng thứ tự],"ghi_chu":"…"}. Lời giải đầy đủ như trên lớp. Học sinh làm vào vở.

## Sơ đồ (đúng thứ tự)
''' + so_do({"reflection"}) + "\n"


def main():
    viec = [(VID_LT, PROMPT_LT, "scripts/gemini/schema/ly-thuyet-phieu.json", anh(TRANG_LT)),
            (VID_LOP, PROMPT_LOP, "scripts/gemini/schema/sua-bai-phieu.json", anh(TRANG_LOP)),
            (VID_BTVN, PROMPT_BTVN, "scripts/gemini/schema/sua-bai-phieu.json", anh(TRANG_BTVN))]
    for vid, prompt, schema, files in viec:
        v = {"id": vid, "model": MODEL, "prompt": prompt, "files": files, "schema": schema,
             "timeout": "1800s", "meta": {"loai": "dung-p1-ch10-9c", "seed": SEED}}
        out = REPO / "storage/gemini/hang-doi" / f"{vid}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, ensure_ascii=False, indent=1))
        print("Đã ghi", out.relative_to(REPO), f"({len(prompt) // 1000}k ký tự, {len(files)} ảnh)")


if __name__ == "__main__":
    main()
