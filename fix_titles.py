import json
import glob

files = glob.glob('/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an/*.json')
for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for stage in data.get('stages', []):
        old_title = stage.get('title', '')
        # Check all possible dashes: em-dash, en-dash, hyphen
        for dash in ['—', '–', '-', '\\&']:
            if f' {dash} ' in old_title or f'{dash} ' in old_title:
                new_title = old_title.split(dash)[0].strip()
                print(f"[{path.split('/')[-1]}] {old_title} -> {new_title}")
                stage['title'] = new_title
                modified = True
                break
            
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

