import json
import glob
import os

folder = '/Users/admin/Documents/thaitd/Code/giaoanMathtech/inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-11-bat-phuong-trinh-bac-nhat-mot-an'
files = glob.glob(os.path.join(folder, '*.json'))

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for stage in data.get('stages', []):
        old_title = stage.get('title', '')
        if '—' in old_title:
            new_title = old_title.split('—')[0].strip()
            print(f"[{os.path.basename(path)}] {old_title} -> {new_title}")
            stage['title'] = new_title
            modified = True
        elif ' - ' in old_title:
            new_title = old_title.split(' - ')[0].strip()
            print(f"[{os.path.basename(path)}] {old_title} -> {new_title}")
            stage['title'] = new_title
            modified = True
            
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

