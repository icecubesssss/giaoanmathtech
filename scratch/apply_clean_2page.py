import re

def format_bai1_columns(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    
    # Grid cao 2.5cm (10 dòng caro) cho mỗi phép tính
    grid_box = (
        "\\begin{tikzpicture}\n"
        "  \\draw[step=0.25cm,ink!15,line width=0.3pt] (0,0) grid (\\linewidth, 2.5);\n"
        "  \\draw[step=1cm,ink!35,line width=0.5pt] (0,0) grid (\\linewidth, 2.5);\n"
        "\\end{tikzpicture}"
    )
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.23\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.23\\linewidth}}\n"
        f"\\textbf{{b)}} {items.get('b)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.23\\linewidth}}\n"
        f"\\textbf{{c)}} {items.get('c)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.23\\linewidth}}\n"
        f"\\textbf{{d)}} {items.get('d)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}"
    )

def format_bai2_columns(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    grid_box = (
        "\\begin{tikzpicture}\n"
        "  \\draw[step=0.25cm,ink!15,line width=0.3pt] (0,0) grid (\\linewidth, 1.8);\n"
        "  \\draw[step=1cm,ink!35,line width=0.5pt] (0,0) grid (\\linewidth, 1.8);\n"
        "\\end{tikzpicture}"
    )
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{b)}} {items.get('b)', '')}\\par\\vspace{{1pt}}\n"
        f"{grid_box}\n"
        f"\\end{{minipage}}"
    )

def format_bai3_dots(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\noindent\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')}\\\\[4pt]\n[[br]]"
        f"\\textbf{{b)}} {items.get('b)', '')}\n"
        f"\\end{{minipage}}\\hfill\n"
        f"\\begin{{minipage}}[t]{{0.48\\linewidth}}\n"
        f"\\textbf{{c)}} {items.get('c)', '')}\\\\[4pt]\n[[br]]"
        f"\\textbf{{d)}} {items.get('d)', '')}\n"
        f"\\end{{minipage}}"
    )

code_template = r'''# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────
''' + '''
def format_bai1_columns(statement: str) -> str:
    parts = re.split(r"\\[\\[br\\]\\]\\s*([a-d]\\))\\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    
    # Grid cao 2.5cm (10 dòng caro) cho mỗi phép tính
    grid_box = (
        "\\\\begin{tikzpicture}\\n"
        "  \\\\draw[step=0.25cm,ink!15,line width=0.3pt] (0,0) grid (\\\\linewidth, 2.5);\\n"
        "  \\\\draw[step=1cm,ink!35,line width=0.5pt] (0,0) grid (\\\\linewidth, 2.5);\\n"
        "\\\\end{tikzpicture}"
    )
    return (
        f"{intro}\\\\par\\\\vspace{{2pt}}\\n"
        f"\\\\noindent\\\\begin{{minipage}}[t]{{0.23\\\\linewidth}}\\n"
        f"\\\\textbf{{a)}} {items.get('a)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}\\\\hfill\\n"
        f"\\\\begin{{minipage}}[t]{{0.23\\\\linewidth}}\\n"
        f"\\\\textbf{{b)}} {items.get('b)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}\\\\hfill\\n"
        f"\\\\begin{{minipage}}[t]{{0.23\\\\linewidth}}\\n"
        f"\\\\textbf{{c)}} {items.get('c)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}\\\\hfill\\n"
        f"\\\\begin{{minipage}}[t]{{0.23\\\\linewidth}}\\n"
        f"\\\\textbf{{d)}} {items.get('d)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}"
    )


def format_bai2_columns(statement: str) -> str:
    parts = re.split(r"\\[\\[br\\]\\]\\s*([a-d]\\))\\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    grid_box = (
        "\\\\begin{tikzpicture}\\n"
        "  \\\\draw[step=0.25cm,ink!15,line width=0.3pt] (0,0) grid (\\\\linewidth, 1.8);\\n"
        "  \\\\draw[step=1cm,ink!35,line width=0.5pt] (0,0) grid (\\\\linewidth, 1.8);\\n"
        "\\\\end{tikzpicture}"
    )
    return (
        f"{intro}\\\\par\\\\vspace{{2pt}}\\n"
        f"\\\\noindent\\\\begin{{minipage}}[t]{{0.48\\\\linewidth}}\\n"
        f"\\\\textbf{{a)}} {items.get('a)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}\\\\hfill\\n"
        f"\\\\begin{{minipage}}[t]{{0.48\\\\linewidth}}\\n"
        f"\\\\textbf{{b)}} {items.get('b)', '')}\\\\par\\\\vspace{{1pt}}\\n"
        f"{grid_box}\\n"
        f"\\\\end{{minipage}}"
    )


def format_bai3_dots(statement: str) -> str:
    parts = re.split(r"\\[\\[br\\]\\]\\s*([a-d]\\))\\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()

    return (
        f"{intro}\\\\par\\\\vspace{{2pt}}\\n"
        f"\\\\noindent\\\\begin{{minipage}}[t]{{0.48\\\\linewidth}}\\n"
        f"\\\\textbf{{a)}} {items.get('a)', '')}\\\\[4pt]\\n[[br]]"
        f"\\\\textbf{{b)}} {items.get('b)', '')}\\n"
        f"\\\\end{{minipage}}\\\\hfill\\n"
        f"\\\\begin{{minipage}}[t]{{0.48\\\\linewidth}}\\n"
        f"\\\\textbf{{c)}} {items.get('c)', '')}\\\\[4pt]\\n[[br]]"
        f"\\\\textbf{{d)}} {items.get('d)', '')}\\n"
        f"\\\\end{{minipage}}"
    )


def make_de_json(k, D):
    header_box = (
        "\\\\begin{tabular}{|p{3.2cm}|p{12.4cm}|}\\n"
        "\\\\hline\\n"
        "\\\\centering\\\\textbf{Điểm} & \\\\centering\\\\textbf{Lời nhận xét của thầy cô} \\\\tabularnewline\\n"
        "\\\\vspace{0.4cm} & \\\\vspace{0.4cm} \\\\tabularnewline\\n"
        "\\\\hline\\n"
        "\\\\end{tabular}\\n"
        "\\\\par\\\\vspace{3pt}"
    )
    tn_intro = "\\\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\\\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}"

    # ── Trang 1: Khung Điểm/Nhận xét + Toàn bộ 8 câu TN trọn vẹn Trang 1 ──
    p1_blocks = [
        {"type": "para", "text": header_box},
        {"type": "para", "text": tn_intro}
    ]
    for c in D["tn"]:
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
    # Ngắt trang dứt khoát sang Trang 2
    p1_blocks.append({"type": "para", "text": "\\\\newpage"})

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": "",
        "blocks": p1_blocks,
        "teacher_note": f"{D['ten']} ({D.get('truong', 'KNTT')}) - Trang 1: 8 câu trắc nghiệm (4,0 điểm). Thời gian: 15 phút."
    }

    # ── Trang 2: Phần II Tự luận (Toàn bộ 5 bài tự luận kèm ô ly, vừa khít Trang 2) ──
    tl_intro = "\\\\par\\\\vspace{2pt}\\\\noindent\\\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
    b1 = D["bai"][0]
    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "",
        "blocks": [
            {"type": "para", "text": tl_intro},
            {
                "type": "problem",
                "label": b1["label"],
                "level": b1["level"],
                "statement": format_bai1_columns(b1["statement"]),
                "solution": BR.join(b1["dap_an"]),
                "tier": "onclass"
            }
        ],
        "teacher_note": "Trang 2: Bài 1 (1,0đ) Đặt tính rồi tính 4 phép tính cơ bản có 4 khung ô ly 2.5cm."
    }

    # Bài 2 và Bài 3
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
                "statement": format_bai2_columns(b2["statement"]),
                "solution": BR.join(b2["dap_an"]),
                "tier": "onclass"
            },
            {
                "type": "problem",
                "label": b3["label"],
                "level": b3["level"],
                "statement": format_bai3_dots(b3["statement"]),
                "solution": BR.join(b3["dap_an"]),
                "tier": "onclass"
            }
        ],
        "teacher_note": "Trang 2: Bài 2 (1,0đ) phân số (2 khung ô ly 1.8cm) và Bài 3 (1,0đ) đổi đơn vị đo."
    }

    # Bài 4 (Bài toán thực tế kèm ô ly cao 4.0cm)
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
            {"type": "writelines", "variant": "oly", "count": 4}
        ],
        "teacher_note": "Trang 2: Bài 4 (2,0đ) Bài toán thực tế hình học kèm khung ô ly 4.0cm."
    }

    # Bài 5 (Toán tư duy kèm ô ly cao 2.0cm) + HẾT & Lời dặn dò
    b5 = D["bai"][4]
    het_note = (
        "\\\\par\\\\vspace{3pt}\\n"
        "\\\\nopagebreak\\\\centerline{\\\\textbf{--- HẾT ---}}\\n"
        "\\\\par\\\\vspace{1pt}\\n"
        "\\\\centerline{\\\\textit{\\\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}\"
    )
    stage5 = {
        "kind": "reflection",
        "number": 5,
        "title": "",
        "blocks": [
            {
                "type": "problem",
                "label": b5["label"],
                "level": b5["level"],
                "statement": b5["statement"],
                "solution": BR.join(b5["dap_an"]),
                "tier": "onclass"
            },
            {"type": "writelines", "variant": "oly", "count": 2},
            {"type": "para", "text": het_note}
        ],
        "teacher_note": "Trang 2: Bài 5 (1,0đ) Vận dụng tư duy cao kèm khung ô ly 2.0cm và Lời dặn dò."
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

    new_text = text[:start_pos] + code_template + '\n\n' + text[end_pos:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"Updated {path} successfully!")

update_file('scripts/de_chinh_thuc_ck1_lop5_kntt.py')
update_file('scripts/de_on_tap_ck1_lop5_kntt.py')

