#!/usr/bin/env python3
"""Tạo & đổ dữ liệu tab 'Chọn câu Ch.VIII lớp 9C' (sheetId=9084) trên sheet Phân dạng lớp 9.

Clone giao diện chuẩn từ tab 'Chọn câu Ch.VII lớp 9C' (9074), mở rộng đủ 68 dòng,
đổ 64 dòng chon-cau.json (dòng 5..68), và kiểm lại toàn bộ công thức không lỗi.
"""
import json
import subprocess
import sys
from pathlib import Path

SHEET_ID = "1OuzuBOhfWQu5RQJ7BxRRpP98bs6aOin2xvN0udz8yqg"
SRC_GID = 9074
NEW_GID = 9084
TAB_NAME = "Chọn câu Ch.VIII lớp 9C"
CHON_CAU_PATH = Path("inputs/refs/ngan-hang-sheet/lop-9/dai-so/chuong-08/chon-cau.json")
PD_TAB = "Phân dạng Ch.VIII lớp 9C"

HEADERS_ROW1 = (
    "CHỌN CÂU CHƯƠNG VIII LỚP 9C (18/11/2026). Bốc từ tab 'Phân dạng Ch.VIII lớp 9C' "
    "(203 câu / 376 ý) theo 6 dạng Thầy tick ở tab 'Dạng Ch.VIII lớp 9C': C8-01…C8-06; "
    "KTC = 2 câu NB kiến thức cũ (thống kê Ch.VII). Không dạy C8-07…C8-13 và không dạy VD. "
    "Chấm T1–T8 trọng số lớp C (Gemini chấm & tự giải độc lập, Claude soát). "
    "Thầy chọn ở cột AB: Chờ duyệt / Hay / Không hay; ghi mã thay ở cột AC."
)
HEADERS_ROW2 = (
    "Khung: MỘT phiếu 180′ trọn buổi tuần 32 (Thầy chốt 18/11), khuôn không VD (40% NB – 60% TH – 0% VD): "
    "ví dụ 42′ (10 NB + 8 TH, cộng 3′ lý thuyết = 45′) · trên lớp 120′ = 32 NB + 12 TH · BTVN 85,8′ = 26 NB + 10 TH. "
    "Đích = Chu Văn An ĐN Câu 5 + Phan Đình Phùng Câu TL4. Ôn tập & KT gộp VII+VIII ở tuần 33. "
    "Không bốc 5 mã đề KT, không bốc trùng STK chép SGK/đề thi, mỗi nhóm trùng bốc tối đa 1. "
    "Cột M, N tự tra từ tab Phân dạng (hiện CẢ BÀI, chỉ dùng các ý ở cột K). Cột AE: nghi ngờ / lưu ý của Gemini."
)
HEADERS_ROW4 = [
    "Phiếu",
    "STT",
    "Vai trò",
    "Mã dạng",
    "Mức",
    "Số ý ở mức đó",
    "Số câu NB (tách từ đề / câu nhỏ)",
    "Phút (theo định mức)",
    "Loại câu §4b",
    "Mã câu",
    "Ý bốc",
    "Hình thức",
    "Đề bài gốc (tự tra)",
    "Nguồn (tự tra)",
    "Loại nguồn",
    "T1 Trọng tâm SGK",
    "T2 Ý toán",
    "T3 Bối cảnh",
    "T4 Phân hoá ý con",
    "T5 Lỗi sai kinh điển",
    "T6 Vừa sức, nghiệm đẹp",
    "T7 Dạng đề thi",
    "T8 Mở rộng",
    "Điểm (thang 10)",
    "Ngưỡng",
    "Kết luận máy",
    "Lí do chấm",
    "THẦY DUYỆT (Chờ duyệt / Hay / Không hay)",
    "Ghi chú của Thầy (mã thay, chuyển phiếu…)",
    "ĐỀ XUẤT (Gemini, Claude soát 18/11)",
    "Lí do đề xuất",
]


def run_gs(*args):
    cmd = ["gsheets"] + list(args)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{cmd} failed:\n{p.stderr}\n{p.stdout}")
    return p.stdout


def main():
    rows = json.loads(CHON_CAU_PATH.read_text())
    total_rows = 4 + len(rows)  # 68

    info = json.loads(run_gs("readonly", "info", SHEET_ID, "--json"))
    sheets = {s["properties"]["sheetId"]: s for s in info["sheets"]}
    existing_by_title = {s["properties"]["title"]: s["properties"]["sheetId"] for s in info["sheets"]}

    if TAB_NAME in existing_by_title and existing_by_title[TAB_NAME] != NEW_GID:
        run_gs("mutate", "delete-sheet", SHEET_ID, str(existing_by_title[TAB_NAME]))

    if NEW_GID not in sheets:
        # Đặt tab ngay sau Ý Ch.VIII lớp 9C
        idx_max = max(
            s["properties"]["index"]
            for s in info["sheets"]
            if "Ch.VIII" in s["properties"]["title"]
        ) + 1
        req = {
            "requests": [
                {
                    "duplicateSheet": {
                        "sourceSheetId": SRC_GID,
                        "insertSheetIndex": idx_max,
                        "newSheetId": NEW_GID,
                        "newSheetName": TAB_NAME,
                    }
                }
            ]
        }
        Path("/tmp/cc8_dup.json").write_text(json.dumps(req))
        run_gs("mutate", "raw-batch", SHEET_ID, "-f", "/tmp/cc8_dup.json")
        info = json.loads(run_gs("readonly", "info", SHEET_ID, "--json"))
        sheets = {s["properties"]["sheetId"]: s for s in info["sheets"]}

    cur_rows = sheets[NEW_GID]["properties"]["gridProperties"]["rowCount"]
    reqs = []
    if cur_rows < total_rows:
        reqs.append(
            {
                "appendDimension": {
                    "sheetId": NEW_GID,
                    "dimension": "ROWS",
                    "length": total_rows - cur_rows,
                }
            }
        )
    elif cur_rows > total_rows:
        reqs.append(
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": NEW_GID,
                        "dimension": "ROWS",
                        "startIndex": total_rows,
                        "endIndex": cur_rows,
                    }
                }
            }
        )

    # Copy định dạng + data validation từ dòng 60 (index 59) sang các dòng mới 61..68
    if total_rows > 61:
        reqs.append(
            {
                "copyPaste": {
                    "source": {
                        "sheetId": NEW_GID,
                        "startRowIndex": 59,
                        "endRowIndex": 60,
                        "startColumnIndex": 0,
                        "endColumnIndex": 32,
                    },
                    "destination": {
                        "sheetId": NEW_GID,
                        "startRowIndex": 60,
                        "endRowIndex": total_rows,
                        "startColumnIndex": 0,
                        "endColumnIndex": 32,
                    },
                    "pasteType": "PASTE_FORMAT",
                }
            }
        )
        reqs.append(
            {
                "copyPaste": {
                    "source": {
                        "sheetId": NEW_GID,
                        "startRowIndex": 59,
                        "endRowIndex": 60,
                        "startColumnIndex": 0,
                        "endColumnIndex": 32,
                    },
                    "destination": {
                        "sheetId": NEW_GID,
                        "startRowIndex": 60,
                        "endRowIndex": total_rows,
                        "startColumnIndex": 0,
                        "endColumnIndex": 32,
                    },
                    "pasteType": "PASTE_DATA_VALIDATION",
                }
            }
        )

    # Mở rộng basicFilter + conditionalFormats tới total_rows
    reqs.append(
        {
            "setBasicFilter": {
                "filter": {
                    "range": {
                        "sheetId": NEW_GID,
                        "startRowIndex": 3,
                        "endRowIndex": total_rows,
                        "startColumnIndex": 0,
                        "endColumnIndex": 31,
                    }
                }
            }
        }
    )
    sh_obj = sheets[NEW_GID]
    for cf_idx, cf in enumerate(sh_obj.get("conditionalFormats", [])):
        new_cf = json.loads(json.dumps(cf))
        for rg in new_cf.get("ranges", []):
            rg["sheetId"] = NEW_GID
            rg["endRowIndex"] = total_rows
        reqs.append({"updateConditionalFormatRule": {"sheetId": NEW_GID, "index": cf_idx, "rule": new_cf}})

    if reqs:
        Path("/tmp/cc8_prep.json").write_text(json.dumps({"requests": reqs}, ensure_ascii=False))
        run_gs("mutate", "raw-batch", SHEET_ID, "-f", "/tmp/cc8_prep.json")

    # Xoá sạch nội dung cũ trước khi ghi mới
    run_gs("mutate", "clear", SHEET_ID, f"'{TAB_NAME}'!A5:AF{total_rows}")

    # Chuẩn bị các dòng dữ liệu (dòng 5..total_rows)
    data_rows = []
    for stt, d in enumerate(rows, 1):
        r = 4 + stt
        T = d["T"]
        f_h = (
            f'=IF(C{r}="Ví dụ",IF(E{r}="NB",G{r},F{r}*IF(E{r}="TH",4,8)),'
            f'IF(C{r}="Trên lớp",G{r}*1.5+IF(E{r}="NB",0,F{r}*IF(E{r}="TH",6,12)),'
            f'G{r}*1.3+IF(E{r}="NB",0,F{r}*IF(E{r}="TH",5.2,10.4))))'
        )
        f_m = f'=IFERROR(INDEX(\'{PD_TAB}\'!A:A,MATCH(J{r},\'{PD_TAB}\'!M:M,0)),"")'
        f_n = f'=IFERROR(INDEX(\'{PD_TAB}\'!B:B,MATCH(J{r},\'{PD_TAB}\'!M:M,0)),"")'
        f_x = f"=ROUND(SUMPRODUCT(P{r}:W{r},$P$3:$W$3)/(2*SUM($P$3:$W$3))*10,1)"
        f_z = f'=IF(X{r}>=Y{r},"Đạt","Dưới ngưỡng")'
        data_rows.append([
            d["phieu"],
            stt,
            d["vai"],
            d["dang"],
            d["muc"],
            d["so_y"],
            d["so_nb"],
            f_h,
            d["loai"],
            d["ma"],
            d["y"],
            d["hinh_thuc"],
            f_m,
            f_n,
            d["loai_nguon"],
            T[0], T[1], T[2], T[3], T[4], T[5], T[6], T[7],
            f_x,
            d["nguong"],
            f_z,
            d["ly_do"],
            "Chờ duyệt",
            "",
            d["de_xuat"],
            d["nghi_ngo"],
        ])

    batch_ops = [
        {"op": "write", "range": f"'{TAB_NAME}'!A1", "data": [[HEADERS_ROW1]]},
        {"op": "write", "range": f"'{TAB_NAME}'!A2", "data": [[HEADERS_ROW2]]},
        {"op": "write", "range": f"'{TAB_NAME}'!O3", "data": [["Trọng số lớp C →", 3, 1, 2, 1, 2, 2, 2, 0]]},
        {"op": "write", "range": f"'{TAB_NAME}'!A4", "data": [HEADERS_ROW4] + data_rows},
    ]
    Path("/tmp/cc8_values.json").write_text(json.dumps(batch_ops, ensure_ascii=False))
    run_gs("mutate", "batch", SHEET_ID, "-f", "/tmp/cc8_values.json")

    # Kiểm tra đọc lại toàn bộ công thức & phát hiện lỗi công thức / ngày tháng
    check_raw = run_gs("readonly", "read", SHEET_ID, f"'{TAB_NAME}'!A1:AE{total_rows}", "--json")
    grid = json.loads(check_raw)
    errs = []
    for r_idx, row in enumerate(grid, 1):
        for c_idx, val in enumerate(row, 1):
            s = str(val)
            if any(e in s for e in ("#REF!", "#NAME?", "#ERROR!", "#VALUE!", "#N/A", "#DIV/0!")):
                errs.append((r_idx, c_idx, s))
    assert not errs, f"Lỗi công thức: {errs}"
    # Kiểm tra tổng phút trên tab khớp chon-cau.json
    phut_sum = {"Ví dụ": 0.0, "Trên lớp": 0.0, "BTVN": 0.0}
    empty_de = []
    for r_idx, row in enumerate(grid[4:], 5):
        phut_sum[row[2]] += float(row[7])
        if not str(row[12]).strip():
            empty_de.append((r_idx, row[9]))
    assert not empty_de, f"Không tra được đề: {empty_de}"
    print(f"OK tab '{TAB_NAME}' (gid={NEW_GID}), {len(rows)} dòng, 0 lỗi công thức.")
    print("Tổng phút đọc từ Sheet:", phut_sum)


if __name__ == "__main__":
    main()
