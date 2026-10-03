#!/usr/bin/env python3
"""OCR KHO ĐỀ — dựng kho text cho mọi đề hợp lệ ở inputs/refs/de-thi/lop-{6..9}/<kỳ>/.

Đề có lớp text → `pdftotext -layout`; đề scan (< 1500 kí tự) → OCR tiếng Việt: `pdftoppm -r 300
-gray` rồi `tesseract -l vie --psm 4` (tối đa 6 trang). Kết quả: storage/cache/de-txt-all/<cùng cây>.txt,
dòng đầu `#NGUON:text|ocr`. File đã có thì bỏ qua (chạy lại chỉ OCR đề mới).

Cần model `vie` ở storage/cache/tessdata/ (KHÔNG cài vào hệ thống):
    mkdir -p storage/cache/tessdata && cp /opt/homebrew/share/tessdata/{eng,osd}.traineddata storage/cache/tessdata/
    curl -L -o storage/cache/tessdata/vie.traineddata https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata
Chạy:  .venv/bin/python scripts/ocr_kho_de.py      (~15 phút cho 670 đề, 8 tiến trình)
"""
import sys, subprocess, re, os, json, tempfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0,"scripts")
from trich_cau_cuoi_de import hop_le_de_thi, KY_DIR
ROOT=Path(".").resolve(); DE=ROOT/"inputs/refs/de-thi"; OUT=ROOT/"storage/cache/de-txt-all"
os.environ["TESSDATA_PREFIX"]=str(ROOT/"storage/cache/tessdata")
def job(p):
    rel=p.relative_to(DE); dest=OUT/rel.with_suffix(".txt")
    if dest.exists() and dest.stat().st_size>0: return str(rel),"cache"
    dest.parent.mkdir(parents=True,exist_ok=True)
    t=subprocess.run(["pdftotext","-layout",str(p),"-"],capture_output=True,text=True).stdout
    nguon="text"
    if len(re.sub(r"\s","",t))<1500:
        nguon="ocr"; parts=[]
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["pdftoppm","-r","300","-gray","-png","-l","6",str(p),f"{td}/p"],capture_output=True)
            for img in sorted(Path(td).glob("p-*.png")):
                parts.append(subprocess.run(["tesseract",str(img),"-","-l","vie","--psm","4"],capture_output=True,text=True).stdout)
        t="\n\f".join(parts)
    dest.write_text(f"#NGUON:{nguon}\n"+t,encoding="utf-8")
    return str(rel),nguon
if __name__=="__main__":
    ds=[]
    for p in sorted(DE.rglob("*.pdf")):
        g=next((x for x in p.parts if x.startswith("lop-")),"?"); k=next((KY_DIR[x] for x in p.parts if x in KY_DIR),"?")
        if g in ("lop-6","lop-7","lop-8","lop-9") and k!="?" and hop_le_de_thi(p): ds.append(p)
    print(len(ds),"đề",flush=True)
    from collections import Counter; c=Counter()
    with ProcessPoolExecutor(8) as ex:
        for i,(rel,ng) in enumerate(ex.map(job,ds),1):
            c[ng]+=1
            if i%50==0: print(i,dict(c),flush=True)
    print("XONG",dict(c))
