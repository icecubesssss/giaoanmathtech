import re
from pathlib import Path

new_render_code = r'''# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────

def format_bai1_4page(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    return (
        f"{intro} [[br]]\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\\\[5pt]\n"
        f"\\textbf{{c)}} {items.get('c)', '')}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{b)}} {items.get('b)', '')} \\\\[5pt]\n"
        f"\\textbf{{d)}} {items.get('d)', '')}\n"
        f"\\end{{minipage}}"
    )


def format_bai2_4page(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    return (
        f"{intro} [[br]]\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{b)}} {items.get('b)', '')}\n"
        f"\\end{{minipage}}"
    )


def format_bai3_4page(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    return (
        f"{intro} [[br]]\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} [[br]]\n"
        f"\\textbf{{b)}} {items.get('b)', '')}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{c)}} {items.get('c)', '')} [[br]]\n"
        f"\\textbf{{d)}} {items.get('d)', '')}\n"
        f"\\end{{minipage}}"
    )


def make_de_json(k, D):
    header_box = (
        "\\begin{tabular}{|p{3.5cm}|p{12.2cm}|}\n"
        "\\hline\n"
        "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
        "\\rule{0pt}{1.8cm} & \\rule{0pt}{1.8cm} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\par\\vspace{6pt}"
    )
    tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}\\par\\vspace{3pt}"

    # ── Trang 1: Top Card + Khung Điểm/Nhận xét + Câu 1..6 ──
    p1_blocks = [
        {"type": "para", "text": header_box},
        {"type": "para", "text": tn_intro}
    ]
    for c in D["tn"][:6]:
        p1_blocks.append({
            "type": "problem",
            "label": f"Câu {c['cau']}.",
            "level": c["level"],
            "statement": c["statement"] + "\\par\\vspace{2pt}",
            "options": c["options"],
            "answer": c["answer"],
            "solution": c["solution"],
            "tier": "onclass"
        })
    p1_blocks.append({"type": "para", "text": "\\newpage"})

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": "",
        "blocks": p1_blocks,
        "teacher_note": f"{D['ten']} ({D.get('truong', 'KNTT')}) - Trang 1: Top Card, khung Điểm và 6 câu trắc nghiệm (Câu 1 đến Câu 6)."
    }

    # ── Trang 2: Câu 7, 8 + Phần II Tự luận: Bài 1 (Đặt tính rồi tính kèm ô ly 12cm) ──
    p2_blocks = []
    for c in D["tn"][6:]:
        p2_blocks.append({
            "type": "problem",
            "label": f"Câu {c['cau']}.",
            "level": c["level"],
            "statement": c["statement"] + "\\par\\vspace{2pt}",
            "options": c["options"],
            "answer": c["answer"],
            "solution": c["solution"],
            "tier": "onclass"
        })

    p2_blocks.append({
        "type": "para",
        "text": "\\par\\vspace{4pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
    })

    b1 = D["bai"][0]
    p2_blocks.append({
        "type": "problem",
        "label": b1["label"],
        "level": b1["level"],
        "statement": format_bai1_4page(b1["statement"]),
        "solution": BR.join(b1["dap_an"]),
        "tier": "onclass"
    })
    p2_blocks.append({"type": "writelines", "variant": "oly", "count": 12})
    p2_blocks.append({
        "type": "para",
        "text": "\\centerline{\\textit{\\footnotesize (Học sinh đặt tính thẳng hàng dấu phẩy và làm bài vào khung ô ly trên)}}"
    })
    p2_blocks.append({"type": "para", "text": "\\newpage"})

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "",
        "blocks": p2_blocks,
        "teacher_note": "Trang 2: Câu 7, Câu 8 và Bài 1 Đặt tính rồi tính với khung ô ly 12cm."
    }

    # ── Trang 3: Bài 2 + Bài 3 + Bài 4 (Lưới ô ly 8cm) ──
    b2 = D["bai"][1]
    b3 = D["bai"][2]
    b4 = D["bai"][3]

    p3_blocks = [
        {
            "type": "problem",
            "label": b2["label"],
            "level": b2["level"],
            "statement": format_bai2_4page(b2["statement"]),
            "solution": BR.join(b2["dap_an"]),
            "tier": "onclass"
        },
        {"type": "writelines", "variant": "oly", "count": 4},
        {
            "type": "problem",
            "label": b3["label"],
            "level": b3["level"],
            "statement": format_bai3_4page(b3["statement"]),
            "solution": BR.join(b3["dap_an"]),
            "tier": "onclass"
        },
        {
            "type": "problem",
            "label": b4["label"],
            "level": b4["level"],
            "statement": b4["statement"],
            "solution": BR.join(b4["dap_an"]),
            "tier": "onclass"
        },
        {"type": "writelines", "variant": "oly", "count": 8},
        {
            "type": "para",
            "text": "\\centerline{\\textit{\\footnotesize (Học sinh trình bày câu lời giải, phép tính và đáp số vào khung ô ly trên)}}"
        },
        {"type": "para", "text": "\\newpage"}
    ]

    stage3 = {
        "kind": "practice1",
        "number": 3,
        "title": "",
        "blocks": p3_blocks,
        "teacher_note": "Trang 3: Bài 2 (ô ly 4cm), Bài 3 (điền khuyết) và Bài 4 (ô ly 8cm)."
    }

    # ── Trang 4: Bài 5 + Bảng tự kiểm tra bài làm + HẾT & Lời dặn dò ──
    b5 = D["bai"][4]
    checklist_box = (
        "\\par\\vspace{8pt}\n"
        "\\noindent\\begin{tcolorbox}[enhanced, colback=neutral!30, colframe=brand!60, boxrule=0.6pt, arc=3pt, left=8pt, right=8pt, top=5pt, bottom=5pt]\n"
        "\\small\n"
        "\\textbf{PHIẾU TỰ KIỂM TRA BÀI LÀM TRƯỚC KHI NỘP} [[br]]\n"
        "\\textit{(Em tự đánh dấu $\\checkmark$ vào ô vuông sau khi hoàn thành):} \\par\\vspace{3pt}\n"
        "\\begin{tabular}{p{7.5cm}p{7.5cm}}\n"
        "$\\square$ Đã ghi đủ Họ tên, Lớp ở Trang 1 & $\\square$ Đã khoanh đủ 8 câu trắc nghiệm \\\\\n"
        "$\\square$ Đã đặt tính thẳng hàng dấu phẩy (Bài 1) & $\\square$ Đã rút gọn kết quả phân số (Bài 2) \\\\\n"
        "$\\square$ Đã điền đủ đơn vị ở Bài 3 và Bài 4 & $\\square$ Đã kiểm tra lại phép tính Bài 5\n"
        "\\end{tabular}\n"
        "\\end{tcolorbox}"
    )

    het_note = (
        "\\par\\vspace{8pt}\n"
        "\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}\n"
        "\\par\\vspace{3pt}\n"
        "\\centerline{\\textit{\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}"
    )

    p4_blocks = [
        {
            "type": "para",
            "text": "\\noindent\\textbf{PHẦN II. TỰ LUẬN (tiếp theo)}"
        },
        {
            "type": "problem",
            "label": b5["label"],
            "level": b5["level"],
            "statement": b5["statement"],
            "solution": BR.join(b5["dap_an"]),
            "tier": "onclass"
        },
        {"type": "writelines", "variant": "oly", "count": 9}
    ]

    stage4 = {
        "kind": "practice2",
        "number": 4,
        "title": "",
        "blocks": p4_blocks,
        "teacher_note": "Trang 4: Bài 5 (ô ly 9cm)."
    }

    p5_blocks = [
        {"type": "para", "text": checklist_box},
        {"type": "para", "text": het_note}
    ]

    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "",
        "blocks": p5_blocks,
        "teacher_note": "Trang 4: Bảng tự kiểm tra bài làm và Lời chúc kết bài."
    }

    title = f"Đề kiểm tra cuối học kì I — Đề {D['so']} (40 phút)" if "Đề" in D.get('ten', '') else f"{D['ten']} (40 phút)"
    return {
        "slug": D["slug_de"],
        "title": title,
        "eyebrow": D["header_eyebrow"],
        "grade_label": "Lớp 5",
        "class_tier": "",
        "theme": "de_thi",
        "stages": [stage1, stage2, stage3, stage4, stage5]
    }


def make_mt_json(k, D):
    # Stage 1: Ma trận đề thi
    rows_tn = ""
    for c in D["tn"]:
        rows_tn += f"Câu {c['cau']} & {c['dang']} ({c['bai']}) & {c['muc']} -- {d(c['diem'])} điểm & {c['phut']} phút \\tabularnewline \\hline\n"

    rows_tl = ""
    for b in D["bai"]:
        rows_tl += f"{b['label']} & {b['dang']} ({b['bai']}) & {b['muc']} -- {d(b['diem'])} điểm & {b['phut']} phút \\tabularnewline \\hline\n"

    table_tn = (
        "\\noindent\\textbf{Bảng phân bố câu hỏi Phần I (Trắc nghiệm):} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{7.5cm}|c|c|}\n"
        "\\hline\n"
        "\\textbf{Phần I} & \\textbf{Dạng bài (bài học trong SGK)} & \\textbf{Mức -- điểm} & \\textbf{Thời lượng} \\tabularnewline\n"
        "\\hline\n"
        + rows_tn +
        "\\multicolumn{2}{|c|}{\\textbf{Cộng Phần I}} & \\textbf{4,0 điểm} & \\textbf{15 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    table_tl = (
        "\\noindent\\textbf{Bảng phân bố câu hỏi Phần II (Tự luận):} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|c|p{7.5cm}|c|c|}\n"
        "\\hline\n"
        "\\textbf{Phần II} & \\textbf{Dạng bài (bài học trong SGK)} & \\textbf{Mức -- điểm} & \\textbf{Thời lượng} \\tabularnewline\n"
        "\\hline\n"
        + rows_tl +
        "\\multicolumn{2}{|c|}{\\textbf{Cộng Phần II}} & \\textbf{6,0 điểm} & \\textbf{25 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\multicolumn{2}{|c|}{\\textbf{TỔNG CỘNG TOÀN ĐỀ}} & \\textbf{10,0 điểm} & \\textbf{40 phút} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    truong_str = D.get('truong', 'Ban Chuyên môn Toán Tiểu học MathTech')
    ti_le_tt27 = (
        f"\\textbf{{Xuất xứ nguồn đề:}} {truong_str}. [[br]]"
        "\\textbf{Tỉ lệ mức độ theo Thông tư 27/2020/TT-BGDĐT:}\n"
        "\\begin{itemize}\n"
        "  \\item \\textbf{Mức 1 (Nhận biết):} $3{,}5$ điểm ($35\\%$) -- gồm Câu 1, 2, 3 Trắc nghiệm ($1{,}5$đ) và Bài 1, 2 Tự luận ($2{,}0$đ).\n"
        "  \\item \\textbf{Mức 2 (Thông hiểu / Kết nối):} $4{,}0$ điểm ($40\\%$) -- gồm Câu 4, 5, 6, 7 Trắc nghiệm ($2{,}0$đ), Bài 3 ($1{,}0$đ) và Bài 4 ý a ($1{,}0$đ).\n"
        "  \\item \\textbf{Mức 3 (Vận dụng):} $2{,}5$ điểm ($25\\%$) -- gồm Câu 8 Trắc nghiệm ($0{,}5$đ), Bài 4 ý b ($1{,}0$đ) và Bài 5 ($1{,}0$đ).\n"
        "\\end{itemize}\n"
        "\\textbf{Phạm vi kiến thức:} Chương trình Toán 5 Kết nối tri thức với cuộc sống (tập 1, Bài 1 đến Bài 35): Ôn tập phân số, hỗn số (CĐ1); Số thập phân, cấu tạo, so sánh, làm tròn (CĐ2); Đơn vị đo diện tích $km^2, ha$ (CĐ3); Các phép tính cộng, trừ, nhân, chia số thập phân, tính thuận tiện (CĐ4); Hình tam giác, hình thang, hình tròn (CĐ5); Ôn tập học kì 1 (CĐ6)."
    )

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": f"Ma trận Đề {D['so']}",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{MA TRẬN ĐỀ KIỂM TRA CHÍNH THỨC CUỐI HỌC KÌ I -- TOÁN 5 -- ĐỀ {D['so']}}} [[br]] {truong_str} [[br]] Thời gian làm bài: 40 phút. Thang điểm: 10,0 điểm (8 câu trắc nghiệm 4,0đ và 5 bài tự luận 6,0đ)."},
            {"type": "para", "text": table_tn},
            {"type": "para", "text": table_tl},
            {"type": "para", "text": ti_le_tt27}
        ]
    }

    # Stage 2: Đáp án Trắc nghiệm
    ans_cells = " & ".join(f"\\textbf{{{c['answer']}}}" for c in D["tn"])
    q_cells = " & ".join(f"Câu {c['cau']}" for c in D["tn"])
    ans_table = (
        "\\begin{center}\\small\\renewcommand{\\arraystretch}{1.2}\n"
        "\\begin{tabular}{|c|" + "c|"*len(D["tn"]) + "}\n"
        "\\hline\n"
        + q_cells + " \\tabularnewline\n"
        "\\hline\n"
        + ans_cells + " \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\\end{center}"
    )

    tn_expl = []
    for c in D["tn"]:
        tn_expl.append(
            f"\\textbf{{Câu {c['cau']} ({d(c['diem'])}đ): Chọn {c['answer']}.}} {c['solution']} [[br]] "
            f"\\textit{{\\footnotesize Phân tích lỗi sai: {c['trap']}}}"
        )

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "Đáp án Phần I — Trắc nghiệm",
        "blocks": [
            {"type": "para", "text": "\\textbf{BẢNG ĐÁP ÁN TRẮC NGHIỆM (4,0 ĐIỂM)}" + BR + ans_table},
            {"type": "para", "text": "\\textbf{GIẢI THÍCH CHI TIẾT VÀ PHÂN TÍCH PHƯƠNG ÁN NHIỄU}" + BR + BR.join(tn_expl)}
        ]
    }

    # Stage 3: Đáp án Bài 1 và Bài 2
    b1 = D["bai"][0]
    b2 = D["bai"][1]
    stage3 = {
        "kind": "practice1",
        "number": 3,
        "title": "Đáp án Bài 1 và Bài 2",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b1['label'].upper()} ({d(b1['diem'])} ĐIỂM) -- {b1['dang'].upper()}}}" + BR + BR.join(b1["dap_an"]) + BR + f"\\textit{{\\footnotesize {b1['note']}}}"},
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b2['label'].upper()} ({d(b2['diem'])} ĐIỂM) -- {b2['dang'].upper()}}}" + BR + BR.join(b2["dap_an"]) + BR + f"\\textit{{\\footnotesize {b2['note']}}}"}
        ]
    }

    # Stage 4: Đáp án Bài 3 và Bài 4
    b3 = D["bai"][2]
    b4 = D["bai"][3]
    stage4 = {
        "kind": "practice2",
        "number": 4,
        "title": "Đáp án Bài 3 và Bài 4",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b3['label'].upper()} ({d(b3['diem'])} ĐIỂM) -- {b3['dang'].upper()}}}" + BR + BR.join(b3["dap_an"]) + BR + f"\\textit{{\\footnotesize {b3['note']}}}"},
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b4['label'].upper()} ({d(b4['diem'])} ĐIỂM) -- {b4['dang'].upper()}}}" + BR + BR.join(b4["dap_an"]) + BR + f"\\textit{{\\footnotesize {b4['note']}}}"}
        ]
    }

    # Stage 5: Đáp án Bài 5, Hướng dẫn chấm và Mẹo sư phạm
    b5 = D["bai"][4]
    huong_dan_cham = (
        "\\textbf{HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM CHI TIẾT (Theo Thông tư 27/2020)} [[br]]\n"
        "\\begin{center}\\footnotesize\\linespread{1.05}\\selectfont\\renewcommand{\\arraystretch}{1.15}\n"
        "\\begin{tabular}{|p{7.5cm}|p{7.5cm}|}\n"
        "\\hline\n"
        "\\textbf{Lỗi thường gặp của học sinh} & \\textbf{Quy định chấm và trừ điểm} \\tabularnewline\n"
        "\\hline\n"
        "Đặt tính không thẳng cột dấu phẩy & Chỉ cho điểm kết quả nếu đúng, trừ 0,25đ kĩ năng đặt tính \\tabularnewline \\hline\n"
        "Phép nhân: tách sai số chữ số ở phần thập phân & Không cho điểm phép tính đó \\tabularnewline \\hline\n"
        "Phép chia: quên gạch dấu phẩy ở số chia & Không cho điểm phần đặt tính, chỉ cho nửa điểm nếu kết quả đúng \\tabularnewline \\hline\n"
        "Kết quả phân số chưa rút gọn về tối giản & Trừ 0,25 điểm cho ý đó \\tabularnewline \\hline\n"
        "Bài có lời văn: thiếu câu lời giải hoặc sai lời giải & Trừ 0,25 điểm cho mỗi ý \\tabularnewline \\hline\n"
        "Viết sai hoặc thiếu tên đơn vị trong bài toán & Trừ 0,25 điểm cho mỗi chỗ sai (tối đa không quá 0,5đ toàn bài) \\tabularnewline \\hline\n"
        "Học sinh giải cách khác đúng & Cho điểm tối đa tương ứng từng bước \\tabularnewline \\hline\n"
        "\\end{tabular}\\end{center}\n"
        "\\noindent\\textit{\\footnotesize Điểm toàn bài là số nguyên từ 0 đến 10, nếu điểm là số thập phân thì làm tròn theo Thông tư 27 (tổng điểm lẻ từ 0,5 trở lên làm tròn thành 1).}"
    )

    meo_su_pham = (
        "\\textbf{MẸO SƯ PHẠM ĐIỀU PHỐI (DÀNH CHO GIÁO VIÊN)}\n"
        "\\begin{itemize}\n"
        "  \\item \\textbf{Điều phối giờ làm bài:} Dành đúng 15 phút cho Phần I và 25 phút cho Phần II. Với bài toán lời văn Bài 4, nhắc học sinh vẽ sơ đồ tóm tắt ra nháp trước khi làm.\n"
        "  \\item \\textbf{Kĩ năng dời dấu phẩy (Bài 5):} Nhắc học sinh phân biệt rõ dời dấu phẩy sang phải (gấp lên 10, 100 lần) và dời dấu phẩy sang trái (giảm đi 10, 100 lần).\n"
        "  \\item \\textbf{Đổi đơn vị đo diện tích:} Rèn thói quen kiểm tra bước nhảy đơn vị: mỗi bước diện tích tương ứng 2 chữ số 0 ($1\\text{ ha} = 100\\text{ dam}^2 = 10\\,000\\text{ m}^2$).\n"
        "  \\item \\textbf{Chấm điểm linh hoạt:} Học sinh có thể tính gộp các bước trong bài toán có lời văn, nếu lập luận đúng và kết quả chính xác vẫn cho điểm trọn vẹn.\n"
        "\\end{itemize}"
    )

    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "Đáp án Bài 5, Biểu điểm và Mẹo sư phạm",
        "blocks": [
            {"type": "para", "text": f"\\textbf{{ĐÁP ÁN {b5['label'].upper()} ({d(b5['diem'])} ĐIỂM) -- {b5['dang'].upper()}}}" + BR + BR.join(b5["dap_an"]) + BR + f"\\textit{{\\footnotesize {b5['note']}}}"},
            {"type": "para", "text": huong_dan_cham}
        ],
        "teacher_note": meo_su_pham
    }

    title = f"Ma trận đề và đáp án chi tiết — {D['ten']}"
    return {
        "slug": D["slug_mt"],
        "title": title,
        "eyebrow": f"SỔ TAY GIÁO VIÊN • LỚP 5 • {D['ten'].upper()}",
        "grade_label": "Lớp 5",
        "class_tier": "",
        "theme": "de_thi",
        "trinh_bay": "thoang",
        "stages": [stage1, stage2, stage3, stage4, stage5]
    }
'''

def update_script(filepath: str):
    p = Path(filepath)
    content = p.read_text(encoding="utf-8")
    
    start_marker = '# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────'
    end_marker = 'if __name__ == "__main__":'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print(f"Error: Markers not found in {filepath} (start: {start_idx}, end: {end_idx})")
        return False
        
    updated_content = content[:start_idx] + new_render_code + "\n\n" + content[end_idx:]
    p.write_text(updated_content, encoding="utf-8")
    print(f"Successfully updated {filepath}")
    return True

update_script("scripts/de_chinh_thuc_ck1_lop5_kntt.py")
update_script("scripts/de_on_tap_ck1_lop5_kntt.py")

