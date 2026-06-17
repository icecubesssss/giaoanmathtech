import json
import glob

files = glob.glob('/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an/*.json')
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for stage in data.get('stages', []):
        print(repr(stage.get('title')))

