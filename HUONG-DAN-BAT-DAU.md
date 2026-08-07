# Bắt đầu từ đây — cài 1 lần, rồi soạn bài mỗi ngày

> **Đây là file đọc ĐẦU TIÊN** cho người mới nhận repo (thầy cô lẫn tác nhân AI).
> Chạy được cả **macOS** và **Windows**.
>
> - Luật soạn nội dung: [HUONG-DAN-SOAN-BAI.md](HUONG-DAN-SOAN-BAI.md)
> - Luật cho tác nhân AI: [AGENTS.md](AGENTS.md)
> - Chia sẻ code qua GitHub: [HUONG-DAN-DONG-BO.md](HUONG-DAN-DONG-BO.md)

---

## 1. Cài 1 lần

Cần đúng **2 thứ**: Python 3.9+ và Tectonic (bộ dựng PDF; bản đang dùng: Tectonic 0.16.9).

### macOS

```bash
git clone <địa-chỉ-repo> && cd giaoanMathtech
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
brew install tectonic                 # bộ dựng PDF
```

### Windows

Mở **PowerShell** (không phải Command Prompt cũ):

```powershell
git clone <địa-chỉ-repo> ; cd giaoanMathtech
py -3 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
# Tectonic: tải bản .exe cho Windows ở trang phát hành chính thức
#   https://github.com/tectonic-typesetting/tectonic/releases
# giải nén, để tectonic.exe vào một thư mục rồi thêm thư mục đó vào PATH.
```

**Kiểm tra cài xong chưa** — chạy đúng 1 lệnh, phải thấy `155 passed`:

| macOS | Windows |
|---|---|
| `.venv/bin/python -m pytest -q` | `.venv\Scripts\python -m pytest -q` |

---

## 2. Dùng hằng ngày — chỉ cần nhớ 1 phím

Mở file phiếu JSON trong VS Code → bấm phím tắt → xong 3 bản PDF (~9 giây).

| macOS | Windows |
|---|---|
| **⌘⇧B** | **Ctrl+Shift+B** |

Nó chạy trên **tab đang chọn**, không phải mọi tab đang mở. Mở 5 tab thì chỉ build đúng cái đang nhìn.

Nó **tự nhận loại file**, Thầy không cần biết mình đang mở gì:

| Đang mở | Bấm phím tắt ra gì |
|---|---|
| `phieu-a-….json` (phiếu học tập) | validate → 3 PDF: handout HS / guide GV / slide |
| `thuyet-minh.json` (phiếu thuyết minh) | dựng PDF thuyết minh |
| File khác | báo rõ *"không phải phiếu học tập"*, không nổ lỗi |

Hai việc nữa ở **⌘⇧P** (Win: **Ctrl+Shift+P**) → gõ `Tasks: Run Task`:

- **Xem bản đọc (Markdown)** — đổi JSON sang bản dễ đọc, mở lên bấm ⌘⇧V (Win: Ctrl+Shift+V). Công thức toán hiện ra đẹp, lời giải gập lại.
- **Build CẢ TUẦN** — build mọi phiếu trong cùng thư mục.

Cấu hình phím tắt nằm ở [.vscode/tasks.json](.vscode/tasks.json), đã có sẵn trong repo — clone về là dùng được ngay, không phải cài thêm.

---

## 3. Nếu không dùng VS Code — gõ lệnh

`make` có sẵn trên macOS. **Windows thường KHÔNG có `make`** → dùng cột bên phải.

| Việc | macOS (có `make`) | Windows (PowerShell) |
|---|---|---|
| Build phiếu vừa sửa | `make b` | `.venv\Scripts\python -m scripts.quick build` |
| Build phiếu theo tên | `make b Q="hinh binh hanh"` | `.venv\Scripts\python -m scripts.quick build "hinh binh hanh"` |
| Xem bản đọc | `make md Q="hbh"` | `.venv\Scripts\python -m scripts.quick md "hbh"` |
| Tìm phiếu nằm đâu | `make f Q="hbh"` | `.venv\Scripts\python -m scripts.quick find "hbh"` |
| Kiểm cả kho | `make check` | `.venv\Scripts\python -m src.main validate-all` |
| Chạy test | `make test` | `.venv\Scripts\python -m pytest -q` |
| Dọn bản in cũ mồ côi | `make prune` | `.venv\Scripts\python -m scripts.prune_outputs` |

`Q` là **mẩu tên bất kỳ** trong đường dẫn, **gõ không dấu vẫn ra**: `"hinh binh hanh"`, `"tuan07 phieu-b"`. Khớp nhiều phiếu quá thì nó in danh sách cho chọn chứ không đoán bừa.

---

## 4. Dành cho tác nhân AI chạy trên máy Windows

Đọc kỹ mục này trước khi chạy lệnh, đừng suy từ ví dụ macOS ra.

**Đường dẫn Python.** `.venv/bin/python` là của macOS/Linux. Trên Windows là:

```
.venv\Scripts\python.exe
```

Không có file nào tên `.venv/bin/python` trên Windows — gọi vào là "file not found".

**Không có `make`.** Mọi target trong [Makefile](Makefile) chỉ là vỏ bọc mỏng của một lệnh Python — mở Makefile đọc dòng tương ứng rồi chạy thẳng lệnh đó. Ví dụ `make check` chính là `python -m src.main validate-all`.

**Dấu phân cách đường dẫn.** Trong code luôn dùng `pathlib.Path`, đừng nối chuỗi bằng `"/"`. Muốn biết một đường dẫn có tuyệt đối không thì dùng `Path(x).is_absolute()`, **đừng** dùng `x.startswith("/")` — trên Windows đường dẫn tuyệt đối là `C:\…`.

**Tiếng Việt và ký tự `✓ ⚠ ′` trên console.** Console Windows mặc định là cp1252, in mấy ký tự này sẽ nổ `UnicodeEncodeError` giữa chừng. Các điểm chạy (`src/main.py`, `scripts/quick.py`, `scripts/prune_outputs.py`) đã tự ép `stdout`/`stderr` sang UTF-8. **Viết thêm script mới thì nhớ chép lại đoạn đó**, nếu không script sẽ chết ngang khi in log.

**Đường dẫn có dấu và có ngoặc vuông.** Thư mục phân tầng đặt tên kiểu `[C]tuan10-…`. Trong PowerShell, ngoặc vuông là ký tự đặc biệt — **luôn bọc đường dẫn trong nháy kép**:

```powershell
.venv\Scripts\python -m src.main build-folder "inputs/seeds/lop-9/dai-so/lop-c/[C]tuan10-bpt-quy-ve-bac-nhat-va-toan-thuc-te"
```

**Ảnh trong phiếu.** Trường `"image"` phải ghi **đường dẫn tương đối**, ảnh để trong `images/` cạnh file phiếu. Tuyệt đối không ghi `/Users/…` hay `C:\Users\…` — máy người khác build là gãy ngay. Engine tự nối thành đường dẫn tuyệt đối lúc build (`src/main.py::_neo_anh`), và `figure_gate` sẽ chặn nếu ghi sai.

---

## 5. Hỏng thì xem đây

| Hiện tượng | Nguyên nhân & cách chữa |
|---|---|
| Bấm phím tắt báo *"không phải file JSON"* | Tab đang chọn không phải file phiếu (đang xem file .md chẳng hạn). Click vào tab JSON rồi bấm lại. |
| `✗ TỪ CHỐI BUILD — spec có vấn đề` | **Không phải lỗi máy** — cổng chất lượng chặn vì giờ dạy vô lý (vd nhét 234′ vào buổi 90′). Đọc dòng lý do, sửa số câu trong spec. Muốn xem PDF nháp: thêm `--force`. |
| `Unable to load picture` khi build | Đường dẫn ảnh trong JSON sai (thường do đổi tên thư mục mà quên sửa). Chạy `validate` sẽ chỉ đúng chỗ. |
| `UnicodeEncodeError` trên Windows | Script mới thiếu đoạn ép UTF-8 — xem mục 4. |
| Mở PDF thấy nội dung cũ | Đang xem bản in cũ còn sót. Chạy `make prune` (Win: `python -m scripts.prune_outputs`) để soi, thêm `YES=1` / `--delete` để dọn. |
| `tectonic: command not found` | Chưa cài Tectonic — xem mục 1. |
