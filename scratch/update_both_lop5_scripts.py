import re

code_template = r'''# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────
def format_bai1_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{3pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hspace{{3.5cm}} \\textbf{{b)}} {items.get('b)', '')}\\\\[5pt]\n[[br]]"
        f"\\textbf{{c)}} {items.get('c)', '')} \\hspace{{3.5cm}} \\textbf{{d)}} {items.get('d)', '')}"
    )


def format_bai2_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{3pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hspace{{4cm}} \\textbf{{b)}} {items.get('b)', '')}"
    )


def format_bai3_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{3pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hspace{{2.2cm}} \\textbf{{b)}} {items.get('b)', '')}\\\\[5pt]\n[[br]]"
        f"\\textbf{{c)}} {items.get('c)', '')} \\hspace{{2.2cm}} \\textbf{{d)}} {items.get('d)', '')}"
    )


def make_de_json(k, D):
    header_box = (
        "\\begin{tabular}{|p{3.2cm}|p{12.4cm}|}\n"
        "\\hline\n"
        "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
        "\\vspace{0.6cm} & \\vspace{0.6cm} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\par\\vspace{6pt}"
    )
    tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}"

    # Trang 1: Top Card + Bảng Điểm + Trắc nghiệm Câu 1 -> Câu 6
    p1_blocks = [
        {"type": "para", "text": header_box},
        {"type": "para", "text": tn_intro}
    ]
    for c in D["tn"][:6]:
        p1_blocks.append({
            "type": "problem",
            "label": f"Câu {c['cau']}.",
            "level": c["level"],
            "statement": c["statement"],
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
        "teacher_note": f"{D['ten']} ({D.get('truong', 'KNTT')}) - Trang 1: 6 câu trắc nghiệm (3,0 điểm)."
    }

    # Trang 2: Trắc nghiệm Câu 7, 8 + Tự luận Bài 1 (Đặt tính) kèm ô ly cao 12cm
    p2_blocks = []
    for c in D["tn"][6:]:
        p2_blocks.append({
            "type": "problem",
            "label": f"Câu {c['cau']}.",
            "level": c["level"],
            "statement": c["statement"],
            "options": c["options"],
            "answer": c["answer"],
            "solution": c["solution"],
            "tier": "onclass"
        })
    
    tl_intro = "\\par\\vspace{4pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
    p2_blocks.append({"type": "para", "text": tl_intro})
    
    b1 = D["bai"][0]
    p2_blocks.append({
        "type": "problem",
        "label": b1["label"],
        "level": b1["level"],
        "statement": format_bai1_text(b1["statement"]),
        "solution": BR.join(b1["dap_an"]),
        "tier": "onclass"
    })
    p2_blocks.append({"type": "writelines", "variant": "oly", "count": 12})
    p2_blocks.append({"type": "para", "text": "\\newpage"})

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "",
        "blocks": p2_blocks,
        "teacher_note": "Trang 2: Câu 7, 8 và Bài 1 (1,0đ) Đặt tính rồi tính kèm khung ô ly 12cm."
    }

    # Trang 3: Bài 2 (Tính + ô ly 4cm) + Bài 3 (Điền chỗ chấm)
    b2 = D["bai"][1]
    b3 = D["bai"][2]
    stage3 = {
        "kind": "practice1",
        "number": 3,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b2["label"],
                "level": b2["level"],
                "statement": format_bai2_text(b2["statement"]),
                "solution": BR.join(b2["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 4},
            {
                "type": "problem",
                "label": b3["label"],
                "level": b3["level"],
                "statement": format_bai3_text(b3["statement"]),
                "solution": BR.join(b3["dap_an"]),
                "tier": "onclass"
            }
        ],
        "teacher_note": "Trang 3 (phần đầu): Bài 2 (1,0đ) phân số/hỗn số và Bài 3 (1,0đ) đổi đơn vị đo."
    }

    # Trang 3 (tiếp): Bài 4 (Toán thực tế + ô ly 8cm)
    b4 = D["bai"][3]
    stage4 = {
        "kind": "practice2",
        "number": 4,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b4["label"],
                "level": b4["level"],
                "statement": b4["statement"],
                "solution": BR.join(b4["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 8},
            {"type": "para", "text": "\\newpage"}
        ],
        "teacher_note": "Trang 3 (phần cuối): Bài 4 (2,0đ) Bài toán thực tế hình học kèm khung ô ly 8cm."
    }

    # Trang 4: Bài 5 (Toán tư duy + ô ly 6cm) + HẾT & Lời dặn dò
    b5 = D["bai"][4]
    het_note = (
        "\\par\\vspace{14pt}\n"
        "\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}\n"
        "\\par\\vspace{4pt}\n"
        "\\centerline{\\textit{\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}"
    )
    tl_tiep = "\\noindent\\textbf{PHẦN II. TỰ LUẬN (tiếp theo)}"
    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "",
        "blocks": [
            {"type": "para", "text": tl_tiep},
            {
                "type": "problem",
                "label": b5["label"],
                "level": b5["level"],
                "statement": b5["statement"],
                "solution": BR.join(b5["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 6},
            {"type": "para", "text": het_note}
        ],
        "teacher_note": "Trang 4: Bài 5 (1,0đ) Vận dụng tư duy cao kèm khung ô ly 6cm và Lời dặn dò."
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


'''

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    start_marker = '# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────'
    end_marker = 'def make_mt_json(k, D):'

    start_pos = text.find(start_marker)
    end_pos = text.find(end_marker)

    if start_pos == -1 or end_pos == -1:
        print(f"Error: markers not found in {path}")
        return

    new_text = text[:start_pos] + code_template + text[end_pos:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"Updated {path} successfully!")

update_file('scripts/de_chinh_thuc_ck1_lop5_kntt.py')
update_file('scripts/de_on_tap_ck1_lop5_kntt.py')
