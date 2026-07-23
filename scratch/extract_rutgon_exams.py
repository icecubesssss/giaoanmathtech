import json
import glob
import os

exam_files = sorted(glob.glob("inputs/refs/de-thi/lop-9/exams/*.json"))

results = []

for filepath in exam_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    xuat_xu = data.get("xuat_xu", {})
    truong = xuat_xu.get("truong", "")
    ky = xuat_xu.get("ky", "")
    nam = xuat_xu.get("nam", "")
    title = f"{truong} ({ky} {nam})"
    
    c3_questions = []
    for cau in data.get("cau", []):
        chuong = cau.get("chuong", "")
        dang = cau.get("dang", [])
        vi_tri = cau.get("vi_tri", "")
        de = cau.get("de", "")
        dap_an = cau.get("dap_an", "")
        
        # Check if it's C3 or DS-CAN-TINH-RUTGON or contains căn / rút gọn
        if chuong == "C3" or "DS-CAN-TINH-RUTGON" in dang or "Câu II" in vi_tri:
            c3_questions.append({
                "id": cau.get("id"),
                "vi_tri": vi_tri,
                "de": de,
                "dap_an": dap_an,
                "band": cau.get("band", "NB"),
                "diem": cau.get("diem", 0.5)
            })
    
    if c3_questions:
        results.append({
            "title": title,
            "filename": os.path.basename(filepath),
            "questions": c3_questions
        })

print(f"Found {len(results)} exams with C3 / Rút gọn questions.")
total_q = sum(len(r["questions"]) for r in results)
print(f"Total questions extracted: {total_q}")

# Save to Markdown
md_out = "# THƯ VIỆN ĐỀ THI THỬ VÀO 10 — CHUYÊN ĐỀ BÀI II: RÚT GỌN BIỂU THỨC VÀ CÂU HỎI PHỤ\n\n"
md_out += "> Tổng hợp từ 21 đề thi GK1/CK1/Thi thử của các trường THCS tại Hà Nội (Thái Thịnh, Trưng Vương, Dịch Vọng, Cầu Diễn, Ái Mộ, Chu Văn An, Phú Diễn, Nguyễn Bỉnh Khiêm...)\n\n"

for item in results:
    md_out += f"## {item['title']}\n"
    for q in item["questions"]:
        md_out += f"- **[{q['vi_tri']}]** ({q['diem']}đ - Band {q['band']}): {q['de']}\n"
        if q['dap_an']:
            md_out += f"  *Đáp án:* {q['dap_an']}\n"
    md_out += "\n---\n\n"

with open("outputs/tong-hop-de-rut-gon-can-thuc-vao-10.md", "w", encoding="utf-8") as f:
    f.write(md_out)

print("Saved to outputs/tong-hop-de-rut-gon-can-thuc-vao-10.md")
