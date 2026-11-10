import re

code_template = r'''# ─────────────────────────── RENDER FUNCTIONS ───────────────────────────
def format_bai1_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hfill \\textbf{{b)}} {items.get('b)', '')} \\hfill "
        f"\\textbf{{c)}} {items.get('c)', '')} \\hfill \\textbf{{d)}} {items.get('d)', '')}"
    )


def format_bai2_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hspace{{4cm}} \\textbf{{b)}} {items.get('b)', '')}"
    )


def format_bai3_text(statement: str) -> str:
    parts = re.split(r"\[\[br\]\]\s*([a-d]\))\s*", statement)
    intro = parts[0].strip()
    items = {}
    for i in range(1, len(parts), 2):
        items[parts[i].strip()] = parts[i+1].strip()
    return (
        f"{intro}\\par\\vspace{{2pt}}\n"
        f"\\textbf{{a)}} {items.get('a)', '')} \\hfill \\textbf{{b)}} {items.get('b)', '')}\\\\[3pt]\n[[br]]"
        f"\\textbf{{c)}} {items.get('c)', '')} \\hfill \\textbf{{d)}} {items.get('d)', '')}"
    )


def make_de_json(k, D):
    header_box = (
        "\\begin{tabular}{|p{3.2cm}|p{12.4cm}|}\n"
        "\\hline\n"
        "\\centering\\textbf{Điểm} & \\centering\\textbf{Lời nhận xét của thầy cô} \\tabularnewline\n"
        "\\vspace{0.35cm} & \\vspace{0.35cm} \\tabularnewline\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\par\\vspace{2pt}"
    )
    tn_intro = "\\textbf{PHẦN I. TRẮC NGHIỆM (4,0 điểm).} \\textit{Em làm bài ngay vào đề. Khoanh vào chữ cái đặt trước câu trả lời đúng (mỗi câu đúng được 0,5 điểm).}"

    # ── Trang 1: Khung Điểm/Nhận xét + Toàn bộ 8 câu TN ──
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

    stage1 = {
        "kind": "review",
        "number": 1,
        "title": "",
        "blocks": p1_blocks,
        "teacher_note": f"{D['ten']} ({D.get('truong', 'KNTT')}) - Trang 1 (Phần I): 8 câu trắc nghiệm (4,0 điểm)."
    }

    # ── Trang 1 (tiếp): Phần II Tự luận + Bài 1 (Đặt tính) kèm ô ly cao 7cm ──
    tl_intro = "\\par\\vspace{2pt}\\noindent\\textbf{PHẦN II. TỰ LUẬN (6,0 điểm)}"
    b1 = D["bai"][0]
    p2_blocks = [
        {"type": "para", "text": tl_intro},
        {
            "type": "problem",
            "label": b1["label"],
            "level": b1["level"],
            "statement": format_bai1_text(b1["statement"]),
            "solution": BR.join(b1["dap_an"]),
            "tier": "onclass"
        },
        # Khung ô ly cao 7cm (28 dòng caro) cho 4 phép tính, vừa vặn Trang 1
        {"type": "writelines", "variant": "oly", "count": 7},
        {"type": "para", "text": "\\newpage"}
    ]

    stage2 = {
        "kind": "concept",
        "number": 2,
        "title": "",
        "blocks": p2_blocks,
        "teacher_note": "Trang 1 (Phần II): Bài 1 (1,0đ) Đặt tính rồi tính kèm khung ô ly 7cm. Kết thúc Trang 1."
    }

    # ── Trang 2: Bài 2 (Tính + ô ly 3.5cm) + Bài 3 (Điền chỗ chấm) ──
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
        "teacher_note": "Trang 2: Bài 2 (1,0đ) phân số/hỗn số (ô ly 4cm) và Bài 3 (1,0đ) đổi đơn vị đo."
    }

    # ── Trang 2 (tiếp): Bài 4 (Toán thực tế + ô ly 6cm) ──
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
            {"type": "writelines", "variant": "oly", "count": 6}
        ],
        "teacher_note": "Trang 2: Bài 4 (2,0đ) Bài toán thực tế hình học kèm khung ô ly 6cm."
    }

    # ── Trang 2 (tiếp): Bài 5 (Toán tư duy + ô ly 3cm) + HẾT & Lời dặn dò ──
    b5 = D["bai"][4]
    het_note = (
        "\\par\\vspace{4pt}\n"
        "\\nopagebreak\\centerline{\\textbf{--- HẾT ---}}\n"
        "\\par\\vspace{2pt}\n"
        "\\centerline{\\textit{\\footnotesize Em nhớ đọc lại bài trước khi nộp nhé. Chúc em làm bài thật tốt!}}"
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
            {"type": "writelines", "variant": "oly", "count": 3},
            {"type": "para", "text": het_note}
        ],
        "teacher_note": "Trang 2: Bài 5 (1,0đ) Vận dụng tư duy cao kèm khung ô ly 3cm và Lời dặn dò."
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

