import os
import shutil
import re
from pathlib import Path

# Paths
SOURCE_DIR = Path("inputs/seeds/lop-8/toan-8-cu")
DEST_DAI_SO = Path("inputs/seeds/lop-8/dai-so/kntt")
DEST_HINH_HOC = Path("inputs/seeds/lop-8/hinh-hoc/kntt")
DEST_DE_THI = Path("inputs/refs/de-thi/lop-8")

# Chapter mapping
CHAPTER_MAP = {
    "CHƯƠNG 1": (DEST_DAI_SO, "chuong-1-da-thuc"),
    "CHƯƠNG 2": (DEST_DAI_SO, "chuong-2-hang-dang-thuc"),
    "CHƯƠNG 3": (DEST_HINH_HOC, "chuong-3-tu-giac"),
    "CHƯƠNG 4": (DEST_HINH_HOC, "chuong-4-dinh-li-thales"),
    "CHƯƠNG 5": (DEST_DAI_SO, "chuong-5-du-lieu-va-bieu-do"),
    "CHƯƠNG 6": (DEST_DAI_SO, "chuong-6-phan-thuc-dai-so"),
    "CHƯƠNG 7": (DEST_DAI_SO, "chuong-7-phuong-trinh-bac-nhat"),
    "CHƯƠNG 8": (DEST_DAI_SO, "chuong-8-tinh-xac-suat"),
    "CHƯƠNG 9": (DEST_HINH_HOC, "chuong-9-tam-giac-dong-dang"),
    "CHƯƠNG 10": (DEST_HINH_HOC, "chuong-10-hinh-khoi-thuc-tien"),
    "CHƯƠNG 1": (DEST_DAI_SO, "chuong-1-da-thuc"),
    "CHƯƠNG 2": (DEST_DAI_SO, "chuong-2-hang-dang-thuc"),
    "CHƯƠNG 3": (DEST_HINH_HOC, "chuong-3-tu-giac"),
    "CHƯƠNG 4": (DEST_HINH_HOC, "chuong-4-dinh-li-thales"),
    "CHƯƠNG 5": (DEST_DAI_SO, "chuong-5-du-lieu-va-bieu-do"),
    "CHƯƠNG 6": (DEST_DAI_SO, "chuong-6-phan-thuc-dai-so"),
    "CHƯƠNG 7": (DEST_DAI_SO, "chuong-7-phuong-trinh-bac-nhat"),
    "CHƯƠNG 8": (DEST_DAI_SO, "chuong-8-tinh-xac-suat"),
    "CHƯƠNG 9": (DEST_HINH_HOC, "chuong-9-tam-giac-dong-dang"),
    "CHƯƠNG 10": (DEST_HINH_HOC, "chuong-10-hinh-khoi-thuc-tien"),
}

EXAM_MAP = {
    "KT GK1": (DEST_DE_THI, "giua-ki-1/kntt"),
    "KT GKI": (DEST_DE_THI, "giua-ki-1/kntt"),
    "KT CK1": (DEST_DE_THI, "cuoi-ki-1/kntt"),
    "KT CKI": (DEST_DE_THI, "cuoi-ki-1/kntt"),
    "KT HKI": (DEST_DE_THI, "cuoi-ki-1/kntt"),
    "KT GK2": (DEST_DE_THI, "giua-ki-2/kntt"),
    "KT GKII": (DEST_DE_THI, "giua-ki-2/kntt"),
    "KT CK2": (DEST_DE_THI, "cuoi-ki-2/kntt"),
    "KT CKII": (DEST_DE_THI, "cuoi-ki-2/kntt"),
    "KT HK2": (DEST_DE_THI, "cuoi-ki-2/kntt"),
    "KT HKII": (DEST_DE_THI, "cuoi-ki-2/kntt"),
}

def normalize_text(text):
    return text.upper().replace("  ", " ")

def determine_target_dir(path_str):
    path_str_norm = normalize_text(path_str)
    
    # Check for KNTT program only
    if "KNTT" not in path_str_norm and "KẾT NỐI TRI THỨC" not in path_str_norm and "KẾT NỐI TRI THỨC" not in path_str_norm:
        return None
        
    # Exclude other programs if mentioned just in case
    if "CÁNH DIỀU" in path_str_norm or "CÁNH DIỀU" in path_str_norm or "CHAN TRAI" in path_str_norm or "CHÂN TRỜI" in path_str_norm:
        if "KNTT" not in path_str_norm.split('/')[-1] and "KNTT" not in path_str_norm.split('/')[-2]:
            return None
    
    # Check for Exams
    for key, (base_dest, sub_dir) in EXAM_MAP.items():
        if key in path_str_norm:
            return base_dest / sub_dir
            
    # Check for Chapters
    # Also handle normalized names with/without special unicode
    for key, (base_dest, sub_dir) in CHAPTER_MAP.items():
        if key in path_str_norm:
            return base_dest / sub_dir
            
    # If it has "KNTT" but doesn't match above, let's put it in unclassified
    return Path("inputs/seeds/lop-8/kntt-khac")

def run():
    copied_count = 0
    skipped_count = 0
    unclassified_count = 0
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if not file.lower().endswith('.pdf'):
                continue
                
            file_path = Path(root) / file
            target_dir = determine_target_dir(str(file_path))
            
            if target_dir is None:
                skipped_count += 1
                continue
                
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file_path = target_dir / file
            
            # Handle duplicate filenames
            counter = 1
            original_stem = target_file_path.stem
            while target_file_path.exists():
                target_file_path = target_dir / f"{original_stem}_{counter}.pdf"
                counter += 1
                
            shutil.copy2(file_path, target_file_path)
            copied_count += 1
            if "kntt-khac" in str(target_dir):
                unclassified_count += 1
            
            print(f"Copied: {file_path.name} -> {target_dir}")
            
    print(f"Done! Copied {copied_count} files ({unclassified_count} unclassified). Skipped {skipped_count} files.")

if __name__ == '__main__':
    run()
