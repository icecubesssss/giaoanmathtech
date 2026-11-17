#!/usr/bin/env python3
"""Thử gọt trang trên BẢN NHÁP (17/11/2026, Phiếu 2 ch.VI 9C): áp vài phương án thay chữ vào bản sao seed, build
handout (slug zz-thu-…, xoá ngay), đo trắng đáy từng trang. Dùng: python scripts/gemini/thu_gon_trang_p2_ch6_9c.py <thư mục nháp>
(thư mục nháp cần thư mục con thu/). Sửa SEED + bảng TH cho phiếu khác."""
import json, subprocess, sys, os, glob, shutil
from PIL import Image
S=sys.argv[1]; REPO=os.getcwd()
SEED="inputs/seeds/lop-9/dai-so/lop-c/chuong-06-ham-so-va-pt-bac-hai/phieu-2-dinh-li-viete-bieu-thuc-doi-xung.json"
C1=(r"Giải ra được $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$.[[br]]\hspace*{1.4em}Đối chiếu điều kiện $m\ne -1$, cả hai giá trị đều thỏa mãn.",
    r"Giải ra được $m=[[fill:2]]$ hoặc $m=[[fill:-2]]$, cả hai đều thỏa mãn $m\ne -1$.")
C3=(r"a) [NB] Thay $x=\dfrac{3-\sqrt5}{2}$ vào phương trình, tìm $a$.", r"a) [NB] Thay nghiệm đã cho vào phương trình, tìm $a$.")
C4=(r"Gọi $x_1=1-\sqrt{2}$ và $x_2$ là nghiệm còn lại của phương trình.[[br]]\hspace*{1.4em}Theo định lí Viète, $x_1+x_2=[[fill:2]]$, không phụ thuộc vào $m$.",
    r"Gọi $x_2$ là nghiệm còn lại. Theo định lí Viète, $x_1+x_2=[[fill:2]]$, không phụ thuộc vào $m$.")
C5=(r"Theo đề bài, $x_1^2+x_2^2=5$ nên $[[fill:m^2+1]]=5$, hay $m^2=[[fill:4]]$.", r"Theo đề bài, $[[fill:m^2+1]]=5$, hay $m^2=[[fill:4]]$.")
TH={"c1":[C1],"c3":[C3],"c1+c3":[C1,C3],"c1+c3+c5":[C1,C3,C5],"c1+c3+c4":[C1,C3,C4],"all":[C1,C3,C4,C5]}
def do(pdf):
    for x in glob.glob(S+'/thu/dt-*.png'): os.remove(x)
    subprocess.run(['pdftoppm','-r','30','-png',pdf,S+'/thu/dt'],check=True)
    gaps=[]
    for p in sorted(glob.glob(S+'/thu/dt-*.png')):
        im=Image.open(p).convert('L');W,H=im.size;px=im.load()
        top,bot=int(H*0.12),int(H*0.86);last=top
        for y in range(top,bot):
            if sum(1 for x in range(int(W*0.08),int(W*0.92),2) if px[x,y]<200)>2: last=y
        gaps.append(round((bot-last)/H*29.7,1))
    return gaps
env=dict(os.environ,TECTONIC_BIN=REPO+"/scripts/tectonic_xelatex.sh")
raw=open(SEED).read()
for ten,ds in TH.items():
    f=json.loads(raw)
    for s in f["stages"]:
        for b in s["blocks"]:
            for k in ("text","statement"):
                if isinstance(b.get(k),str):
                    for cu,moi in ds: b[k]=b[k].replace(cu,moi)
    f["slug"]="zz-thu-p2-"+ten.replace("+","-")
    path=f"{S}/thu/{f['slug']}.json"; json.dump(f,open(path,"w"),ensure_ascii=False)
    subprocess.run([".venv/bin/python","-m","src.main","build-handout",path],env=env,capture_output=True)
    pdf=glob.glob(f"outputs/{f['slug']}/*.pdf")[0]; g=do(pdf)
    print(ten, len(g),"trang", g, "tổng", round(sum(g),1)); shutil.rmtree(f"outputs/{f['slug']}")
