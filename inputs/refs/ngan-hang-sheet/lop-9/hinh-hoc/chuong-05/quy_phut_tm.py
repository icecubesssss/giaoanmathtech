import json,sys
sys.path.insert(0,'.')
from src.schema.thuyetminh_spec import ThuyetMinhSpec, rates_for_spec, phieu_band_minutes, phieu_totals
for f in sys.argv[1:]:
    s=ThuyetMinhSpec(**json.load(open(f)))
    r=rates_for_spec(s)
    print('##',f.split('/')[-1], {k:v for k,v in r.items() if not isinstance(v,dict)} if isinstance(r,dict) else r)
    for p in s.phieu:
        bm=phieu_band_minutes(p,r)
        t=phieu_totals(p,r)
        print(p.code,{seg:{b:round(v,1) for b,v in d.items()} for seg,d in bm.items()}, {k:(round(v,1) if isinstance(v,float) else v) for k,v in t.items()})
