#!/usr/bin/env python3
"""SOÁT LỆCH TIẾN ĐỘ KNTT — đánh dấu đề Hà Nội có CHƯƠNG KNTT dạy ở kỳ khác (trường đảo PPCT
hoặc dùng bộ sách khác). Luật dò từ khoá đã hiệu chỉnh tay qua 3 đợt (30/09–01/10/2026) — mỗi
báo oan đã gặp ghi ở memory `gk1-2025-2026-tien-do-kntt` ("đơn thức ĐỒNG DẠNG", "phân số tối
giản" của bài ƯCLN, "một SỐ ĐỐI tượng", "số nguyên\\n tố").

Đọc kho text của scripts/ocr_kho_de.py. In danh sách đề bị cờ + ghi {OUT}. KHÔNG tự xoá:
người chạy đọc lại từng cờ (đề scan thì xem ẢNH), rồi mới chuyển đề sang
inputs/refs/de-thi-lech-kntt/ (kèm ly-do.json) — chuyển, không xoá, vì PDF không nằm trong git.

Chạy:  .venv/bin/python scripts/soat_lech_kntt.py
"""
import json, re
from pathlib import Path

OUT = "storage/cache/soat-lech-kntt.json"

# GK1: dấu hiệu theo khối — "B" = chương KNTT kế tiếp của kỳ I (VƯỢT MỐC, vẫn giữ), "C" = kỳ II (LỆCH)
M={
"6":[("B","Ch.III số nguyên",r"số\s+nguyên\s+(âm|dương|lớn|nhỏ|được\s+kí)|tập\s+hợp\s+(các\s+)?số\s+nguyên(?!\s*tố)|−\s*\(\s*−|\bsố\s+đối\s+(của|là)"),
     ("B","Ch.V tính đối xứng",r"trục\s+đối\s+xứng|tâm\s+đối\s+xứng"),
     ("C","Ch.VI phân số (HK2)",r"hỗn\s+số|phân\s+số\s+đối|số\s+nghịch\s+đảo|so\s+sánh\s+(hai\s+)?phân\s+số"),
     ("C","Ch.VII số thập phân (HK2)",r"số\s+thập\s+phân\s+âm|phép\s+(cộng|nhân|chia)\s+số\s+thập\s+phân"),
     ("C","Ch.VIII điểm-đường thẳng-tia (HK2)",r"\btia\s+[A-Z]{1,2}\b|\bhai\s+tia\b|trung\s+điểm\s+(của\s+)?đoạn|ba\s+điểm\s+thẳng\s+hàng"),
     ("C","Ch.IX dữ liệu-xác suất (HK2)",r"biểu\s+đồ|xác\s+suất|thu\s+thập\s+dữ\s+liệu")],
"7":[("B","Ch.IV tam giác bằng nhau",r"tam\s+giác\s+bằng\s+nhau|trường\s+hợp\s+bằng\s+nhau|tổng\s+(ba|3|các)\s+góc\s+(trong\s+)?(của\s+)?(một\s+)?tam\s+giác"),
     ("B","Ch.V thu thập dữ liệu, biểu đồ",r"biểu\s+đồ|thu\s+thập.{0,20}dữ\s+liệu"),
     ("C","Ch.VI tỉ lệ thức, đại lượng tỉ lệ (HK2)",r"tỉ\s+lệ\s+thức|dãy\s+tỉ\s+số|tỉ\s+lệ\s+thuận|tỉ\s+lệ\s+nghịch"),
     ("C","Ch.X hình hộp, lăng trụ (HK2)",r"hình\s+hộp|hình\s+lập\s+phương|lăng\s+trụ"),
     ("C","Ch.VII biểu thức đại số, đa thức (HK2)",r"đa\s+thức\s+một\s+biến|biểu\s+thức\s+đại\s+số")],
"8":[("B","Ch.IV định lí Thalès",r"thal[eè]s|ta-?\s?lét|đường\s+trung\s+bình"),
     ("B","Ch.V dữ liệu, biểu đồ",r"biểu\s+đồ|thu\s+thập.{0,20}dữ\s+liệu"),
     ("C","Ch.VI phân thức (HK2)",r"phân\s+thức"),
     ("C","Ch.VII PT bậc nhất, hàm số (HK2)",r"hàm\s+số|đồ\s+thị|phương\s+trình\s+bậc\s+nhất"),
     ("C","Ch.IX Pythagore, đồng dạng (HK2)",r"pythagor|pi-?\s?ta-?\s?go|py-?\s?ta-?\s?go|tam\s+giác\s+đồng\s+dạng|hai\s+tam\s+giác.{0,40}đồng\s+dạng"),
     ("C","Ch.X hình chóp (HK2)",r"hình\s+chóp")],
"9":[("B","Ch.V đường tròn",r"đường\s+tròn|tiếp\s+tuyến"),
     ("C","Ch.VI hàm số y=ax², PT bậc hai (HK2)",r"y\s*=\s*ax\s*\^?\s*2|vi-?\s?ét|viète|biệt\s+thức|công\s+thức\s+nghiệm"),
     ("C","Ch.VII-VIII tần số, xác suất (HK2)",r"tần\s+số|xác\s+suất"),
     ("C","Ch.IX-X nội tiếp, hình khối (HK2)",r"tứ\s+giác\s+nội\s+tiếp|góc\s+nội\s+tiếp|đường\s+tròn\s+nội\s+tiếp|hình\s+trụ|hình\s+nón|hình\s+cầu")],
}

# CK1: chỉ nội dung KNTT dạy ở KỲ II
M_CK1={  # chỉ nội dung KNTT dạy ở KỲ II
"6":[("C","Ch.VI phân số",r"hỗn\s+số|phân\s+số\s+đối|số\s+nghịch\s+đảo|so\s+sánh\s+(hai\s+)?phân\s+số|phép\s+(nhân|chia)\s+phân\s+số"),
     ("C","Ch.VII số thập phân",r"số\s+thập\s+phân\s+âm|phép\s+(cộng|nhân|chia)\s+số\s+thập\s+phân|tỉ\s+số\s+phần\s+trăm"),
     ("C","Ch.VIII điểm-đường thẳng-tia-góc",r"\btia\s+[A-Z]{1,2}\b|\bhai\s+tia\b|trung\s+điểm\s+(của\s+)?đoạn|ba\s+điểm\s+thẳng\s+hàng|góc\s+(nhọn|tù|bẹt)"),
     ("C","Ch.IX dữ liệu-xác suất",r"biểu\s+đồ|xác\s+suất|thu\s+thập\s+dữ\s+liệu")],
"7":[("C","Ch.VI tỉ lệ thức, đại lượng tỉ lệ",r"tỉ\s+lệ\s+thức|dãy\s+tỉ\s+số|tỉ\s+lệ\s+thuận|tỉ\s+lệ\s+nghịch"),
     ("C","Ch.VII biểu thức đại số, đa thức",r"đa\s+thức\s+một\s+biến|nghiệm\s+của\s+đa\s+thức|biểu\s+thức\s+đại\s+số"),
     ("C","Ch.VIII xác suất",r"xác\s+suất|biến\s+cố"),
     ("C","Ch.IX quan hệ trong tam giác",r"trọng\s+tâm|bất\s+đẳng\s+thức\s+tam\s+giác|đường\s+xiên|đồng\s+quy"),
     ("C","Ch.X hình hộp, lăng trụ",r"hình\s+hộp|hình\s+lập\s+phương|lăng\s+trụ")],
"8":[("C","Ch.VI phân thức",r"phân\s+thức"),
     ("C","Ch.VII PT bậc nhất, hàm số",r"hàm\s+số|đồ\s+thị|phương\s+trình\s+bậc\s+nhất|hệ\s+số\s+góc"),
     ("C","Ch.VIII xác suất",r"xác\s+suất|biến\s+cố"),
     ("C","Ch.IX đồng dạng, Pythagore",r"pythagor|pi-?\s?ta-?\s?go|py-?\s?ta-?\s?go|tam\s+giác\s+đồng\s+dạng|hai\s+tam\s+giác.{0,40}đồng\s+dạng"),
     ("C","Ch.X hình chóp",r"hình\s+chóp")],
"9":[("C","Ch.VI y=ax², PT bậc hai",r"y\s*=\s*ax\s*\^?\s*2|vi-?\s?ét|viète|biệt\s+thức|công\s+thức\s+nghiệm"),
     ("C","Ch.VII-VIII tần số, xác suất",r"tần\s+số|xác\s+suất"),
     ("C","Ch.IX-X nội tiếp, hình khối",r"tứ\s+giác\s+nội\s+tiếp|góc\s+nội\s+tiếp|đường\s+tròn\s+nội\s+tiếp|hình\s+trụ|hình\s+nón|hình\s+cầu")],
}

# GK2/CK2: nội dung KNTT dạy ở KỲ I mà bộ khác dạy kỳ II (lớp 8: Thalès, dữ liệu)
C_K2={"6":[],"7":[],
      "8":[("Thalès/đường trung bình (KNTT Ch.IV kỳ I)",r"thal[eè]s|ta-?\s?lét|đường\s+trung\s+bình"),
           ("dữ liệu, biểu đồ (KNTT Ch.V kỳ I)",r"thu\s+thập.{0,20}dữ\s+liệu|biểu\s+đồ\s+(cột|tranh|hình\s+quạt|đoạn)")],
      "9":[]}

def luat(lop,ky):
    if ky=="GK1": return [(n,rx) for m,n,rx in M[lop] if m=="C"]
    if ky=="CK1": return [(n,rx) for m,n,rx in M_CK1[lop]]
    return list(C_K2[lop])

KY={"giua-ki-1":"GK1","cuoi-ki-1":"CK1","giua-ki-2":"GK2","cuoi-ki-2":"CK2","de-cuoi-ki-2":"CK2"}
GIU={"de-hoc-ky-1-toan-6-nam-2025-2026-cum-chuyen-mon-so-14-ha-noi"}   # Thầy/đã soát: ghi KNTT
TXT=Path("storage/cache/de-txt-all"); DE=Path("inputs/refs/de-thi")
ra=[]
for f in sorted(TXT.rglob("*.txt")):
    rel=f.relative_to(TXT); lop=rel.parts[0][-1]; ky=next((KY[p] for p in rel.parts if p in KY),None)
    pdf=DE/rel.with_suffix(".pdf")
    if not ky or not pdf.exists() or f.stem in GIU: continue
    t=f.read_text(errors="ignore"); t=re.sub(r"(?i)toanmath\.com","",t)
    ca=re.search(r"(?i)cánh\s*diều|chân\s*trời\s*sáng\s*tạo",t[:3000])
    hits=[]
    for n,rx in luat(lop,ky):
        ms=list(re.finditer(rx,t,re.I))
        if ms:
            a=ms[0].start(); hits.append((n,len(ms),re.sub(r"\s+"," ",t[max(0,a-60):a+70])))
    if hits or ca:
        ra.append(dict(file=str(pdf),lop=lop,ky=ky,ocr=t.startswith("#NGUON:ocr"),bo=ca.group(0) if ca else "",hits=hits))
Path(OUT).write_text(json.dumps(ra,ensure_ascii=False,indent=1),encoding="utf-8")
print(len(ra),"đề bị cờ")
for r in ra:
    print(r["lop"],r["ky"],"OCR" if r["ocr"] else "   ",r["bo"],Path(r["file"]).stem.split("nam-")[-1][:55])
    for n,k,v in r["hits"]: print("      ",n,k,"|",v[:120])
