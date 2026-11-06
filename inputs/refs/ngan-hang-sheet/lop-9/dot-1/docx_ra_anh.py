#!/usr/bin/env python3
"""Docx có công thức MathType (WMF) → một ảnh PNG dài: chữ đoạn văn + công thức render đúng thứ tự.
Dùng: docx_ra_anh.py file.docx thu_muc_ra   (ra trang-01.png, trang-02.png ...)"""
import sys,struct,zipfile,re,io,os
from PIL import Image,ImageDraw,ImageFont
import xml.etree.ElementTree as ET
F='/System/Library/Fonts/Supplemental/'
TNR={(0,0):F+'Times New Roman.ttf',(1,0):F+'Times New Roman Bold.ttf',(0,1):F+'Times New Roman Italic.ttf',(1,1):F+'Times New Roman Bold Italic.ttf'}
SYM={0x22:'∀',0x24:'∃',0x27:'∋',0x2d:'−',0x2a:'∗',0x40:'≅',0x5e:'⊥',0x60:' ',0xa2:'′',0xa3:'≤',0xa5:'∞',0xb0:'°',0xb1:'±',0xb2:'″',0xb3:'≥',0xb4:'×',0xb5:'∝',0xb6:'∂',0xb7:'•',0xb8:'÷',0xb9:'≠',0xba:'≡',0xbb:'≈',0xbc:'…',0xbd:'|',0xc6:'∅',0xc7:'∩',0xc8:'∪',0xc9:'⊃',0xca:'⊇',0xcb:'⊄',0xcc:'⊂',0xcd:'⊆',0xce:'∈',0xcf:'∉',0xd0:'∠',0xd6:'√',0xd7:'·',0xd8:'¬',0xd9:'∧',0xda:'∨',0xdc:'⇐',0xde:'⇒',0xdb:'⇔',0xe0:'◊',0xe1:'⟨',0xe6:'(',0xe7:'|',0xe8:'(',0xe9:'⎡',0xea:'⎢',0xeb:'⎣',0xec:'⎧',0xed:'⎨',0xee:'⎩',0xef:'|',0xf1:'⟩',0xf2:'∫',0xf6:')',0xf7:'|',0xf8:')',0xf9:'⎤',0xfa:'⎥',0xfb:'⎦',0xfc:'⎫',0xfd:'⎬',0xfe:'⎭'}
GREEK=dict(zip('abcdefghiklmnopqrstuwxyzABDFGLPQRSTWXY','αβχδεφγηικλμνοπθρστυωξψζΑΒΔΦΓΛΠΘΡΣΤΩΞΨ'))
def fnt(sz,b=0,i=0): return ImageFont.truetype(TNR[(b,i)],max(6,int(sz)))
def wmf_png(data,scale=None,target_h=None):
    off=22 if data[:4]==b'\xd7\xcd\xc6\x9a' else 0
    pos=off+18; recs=[]
    while pos+6<=len(data):
        sz,fn=struct.unpack('<IH',data[pos:pos+6])
        if sz==0 or fn==0: break
        recs.append((fn,data[pos+6:pos+sz*2])); pos+=sz*2
    ext=None;org=(0,0)
    for fn,b in recs:
        if fn==0x020C: h,w=struct.unpack('<hh',b[:4]);ext=(abs(w),abs(h))
        if fn==0x020B: y,x=struct.unpack('<hh',b[:4]);org=(x,y)
    if not ext: return None
    W,H=ext
    s=(scale or 1)
    # chọn tỉ lệ: font chính ≈ 34px
    import collections
    hs=[abs(struct.unpack('<h',b[:2])[0]) for fn,b in recs if fn==0x02FB and len(b)>=2 and b[18:24]!=b'System']
    hs=[h for h in hs if h]
    base=collections.Counter(hs).most_common(1)[0][0] if hs else H
    s=34/float(base or 1)
    im=Image.new('RGB',(max(4,int(W*s)+8),max(4,int(H*s)+8)),'white');d=ImageDraw.Draw(im)
    objs={};cur={};fontobj=None;pt=(0,0)
    def alloc(o):
        i=0
        while i in objs:i+=1
        objs[i]=o
    X=lambda v:(v-org[0])*s+4;Y=lambda v:(v-org[1])*s+4
    align=0;pen=1
    for fn,b in recs:
        if fn==0x02FB:
            h=struct.unpack('<h',b[:2])[0];wg=struct.unpack('<h',b[8:10])[0];it=b[10];nm=b[18:50].split(b'\0')[0].decode('latin1')
            alloc(('f',abs(h),wg>=600,bool(it),nm))
        elif fn==0x02FA: alloc(('p',))
        elif fn==0x02FC: alloc(('b',))
        elif fn in(0x0142,0x06FF,0x00F7): alloc(('x',))
        elif fn==0x012D:
            i=struct.unpack('<H',b[:2])[0]
            if i in objs and objs[i][0]=='f': fontobj=objs[i]
        elif fn==0x01F0:
            i=struct.unpack('<H',b[:2])[0];objs.pop(i,None)
        elif fn==0x012E: align=struct.unpack('<H',b[:2])[0]
        elif fn==0x0214: y,x=struct.unpack('<hh',b[:4]);pt=(x,y)
        elif fn==0x0213:
            y,x=struct.unpack('<hh',b[:4]);d.line([X(pt[0]),Y(pt[1]),X(x),Y(y)],fill='black',width=2);pt=(x,y)
        elif fn==0x0325 or fn==0x0324:
            n=struct.unpack('<H',b[:2])[0];ps=[struct.unpack('<hh',b[2+4*i:6+4*i]) for i in range(n)]
            P=[(X(a),Y(c)) for a,c in ps]
            if fn==0x0324: d.polygon(P,fill='black')
            else: d.line(P,fill='black',width=2)
        elif fn in(0x0521,0x0A32):
            if fn==0x0521:
                n=struct.unpack('<H',b[:2])[0];t=b[2:2+n];rest=b[2+n+(n&1):];y,x=struct.unpack('<hh',rest[:4])
            else:
                y,x,n,o=struct.unpack('<hhHH',b[:8]);j=8+(8 if o&6 else 0);t=b[j:j+n]
                dxb=b[j+n+(n&1):];dx=[struct.unpack('<h',dxb[2*i:2*i+2])[0] for i in range(min(n,len(dxb)//2))]
            if align&1: x,y=pt
            f=fontobj or ('f',H,False,False,'Times New Roman');sz=f[1]*s
            name=f[4].lower();out=''
            if 'symbol' in name:
                for c in t: out+=SYM.get(c,GREEK.get(chr(c),chr(c)))
            elif 'extra' in name:
                for c in t: out+={0x4b:'…',0x68:'ℏ',0x6c:'…',0x51:'',0x3e:'⟩',0x5e:'^',0x7e:'~',0x65:'̂',0xa2:'°',0x47:'∠',0x50:'∥',0x2f:'∥',0xd0:'∠'}.get(c,'?%02x?'%c)
            else:
                try: out=t.decode('cp1258')
                except Exception: out=t.decode('latin1')
            ft=fnt(sz,f[2],f[3])
            if 'symbol' in name or 'extra' in name or any(ord(c)>0x2000 for c in out): ft=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf',max(6,int(sz)))
            bb=ft.getbbox(out or ' ');asc=ft.getmetrics()[0]
            xx=X(x);yy=Y(y)
            if align&6==6: xx-=bb[2]/2
            elif align&2: xx-=bb[2]
            if (align&24)!=24: pass
            else: yy-=asc
            if fn==0x0A32 and dx and len(out)==len(dx):
                cx=xx
                for ch,dd in zip(out,dx):
                    d.text((cx,yy),ch,font=ft,fill='black');cx+=dd*s
                if align&1: pt=(pt[0]+sum(dx),pt[1])
            else:
                d.text((xx,yy),out,font=ft,fill='black')
    return im
def run(path,outdir):
    os.makedirs(outdir,exist_ok=True)
    z=zipfile.ZipFile(path)
    rels=ET.fromstring(z.read('word/_rels/document.xml.rels'));RM={r.get('Id'):r.get('Target') for r in rels}
    W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';R='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    A='{http://schemas.openxmlformats.org/drawingml/2006/main}';V='{urn:schemas-microsoft-com:vml}'
    doc=ET.fromstring(z.read('word/document.xml'))
    PW=1500;pages=[];pg=Image.new('RGB',(PW,2000),'white');y=20
    fb=fnt(32);fbb=fnt(32,1);
    def flush():
        nonlocal pg,y
        pages.append(pg.crop((0,0,PW,y+20)));pg=Image.new('RGB',(PW,2000),'white');y=20
    def line(items):
        nonlocal y
        lh=max([i[1].height if i[0]=='i' else 44 for i in items]+[44])
        if y+lh+20>2000: flush()
        x=20
        for it in items:
            if it[0]=='i':
                pg.paste(it[1],(int(x),int(y+(lh-it[1].height)/2)));x+=it[1].width+4
            else:
                ImageDraw.Draw(pg).text((x,y+(lh-40)/2),it[1],font=it[2],fill='black');x+=it[2].getlength(it[1])
        y+=lh+6
    def wrap(items):
        cur=[];x=0
        for it in items:
            if it[0]=='i':
                if x+it[1].width>PW-60 and cur: line(cur);cur=[];x=0
                cur.append(it);x+=it[1].width+4
            else:
                for w in re.findall(r'\S+\s*|\s+',it[1]):
                    l=it[2].getlength(w)
                    if x+l>PW-60 and cur: line(cur);cur=[];x=0
                    cur.append(('t',w,it[2]));x+=l
        if cur: line(cur)
    def emit_para(p):
        items=[]
        for el in p.iter():
            if el.tag==W+'r':
                bold=el.find(W+'rPr/'+W+'b') is not None
                for c in el:
                    if c.tag==W+'t' and c.text: items.append(('t',c.text,fbb if bold else fb))
                    elif c.tag==W+'tab': items.append(('t','    ',fb))
                    elif c.tag in (W+'object',W+'pict',W+'drawing'):
                        rid=None
                        for s in c.iter():
                            if s.tag==V+'imagedata': rid=s.get(R+'id')
                            if s.tag==A+'blip': rid=s.get(R+'embed')
                        if rid and rid in RM:
                            data=z.read('word/'+RM[rid]) if not RM[rid].startswith('/') else z.read(RM[rid][1:])
                            try:
                                if RM[rid].lower().endswith('.wmf'): im=wmf_png(data)
                                else:
                                    im=Image.open(io.BytesIO(data)).convert('RGB')
                                    if im.width>900: im=im.resize((900,int(im.height*900/im.width)))
                                if im: items.append(('i',im))
                            except Exception as e: items.append(('t',f'[ẢNH LỖI {RM[rid]}]',fb))
        if items: wrap(items)
        else: line([('t',' ',fb)])
    for ch in doc.find(W+'body'):
        if ch.tag==W+'p': emit_para(ch)
        elif ch.tag==W+'tbl':
            for tr in ch.iter(W+'tr'):
                its=[]
                for tc in tr.findall(W+'tc'):
                    for p in tc.iter(W+'p'):
                        for r in p.iter(W+'t'):
                            if r.text: its.append(('t',r.text+'  ',fb))
                        for s in p.iter(V+'imagedata'):
                            rid=s.get(R+'id')
                            if rid in RM and RM[rid].lower().endswith('.wmf'):
                                im=wmf_png(z.read('word/'+RM[rid]))
                                if im: its.append(('i',im))
                    its.append(('t',' | ',fb))
                wrap(its)
    flush()
    for i,p in enumerate(pages,1): p.save(f'{outdir}/trang-{i:02d}.png')
    print(len(pages),'trang',outdir)
run(sys.argv[1],sys.argv[2])
