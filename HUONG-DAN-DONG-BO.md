# Hướng dẫn đồng bộ MathTech Engine giữa các thầy cô

Tài liệu này thay cho cách gửi file zip. Mục tiêu: **một kho chung trên GitHub**, ai
cập nhật engine cũng đẩy lên được, mọi người kéo về là có bản mới — không gửi zip lần nào nữa.

> Dành cho thầy cô **không rành kỹ thuật**: cứ làm theo phần "Cài 1 lần" rồi mỗi buổi
> chỉ cần nhớ **2 nút: Pull (lấy về) và Push (đẩy lên)** trong GitHub Desktop.

---

## 0. Hiểu nhanh: cái gì chung, cái gì riêng

| Đồng bộ chung qua GitHub (ai sửa cũng thấy) | Máy ai nấy giữ (KHÔNG lên GitHub) |
|---|---|
| `src/` – bộ máy Python | `.env` – API key riêng của mỗi người |
| `templates/` – khung LaTeX phiếu/slide | `.venv/` – môi trường Python (tự cài) |
| `config/` – chương trình, màu, độ khó | `outputs/` – PDF in ra (build lại lúc nào cũng được) |
| `assets/` – font | `storage/run_state.json` – tiến độ build máy mình |
| `inputs/seeds/` – **thư viện bài** + chương trình tham chiếu | cache biên dịch (`.tectonic`, `__pycache__`…) |

→ Vì mỗi bài nằm trong **một thư mục riêng**, nhiều người thêm bài khác nhau **không đụng nhau**.
Chỉ khi hai người sửa **cùng một file** mới cần gộp (hiếm, và GitHub Desktop báo rõ).

---

## ⚠️ 1. Việc QUAN TRỌNG NHẤT trước khi bắt đầu: đưa dự án RA KHỎI OneDrive

Hiện thư mục này nằm trong **OneDrive**. Khi đã dùng GitHub để đồng bộ thì **không nên để
trong OneDrive nữa** — vì OneDrive và Git sẽ cùng tranh nhau đồng bộ thư mục ẩn `.git`,
dễ làm **hỏng kho hoặc tạo file trùng** (`giaoan - Copy`, `run_state (1).json`…).

**Cách làm:** chép cả thư mục dự án sang một nơi **ngoài OneDrive**, ví dụ:
- Windows: `C:\Code\giaoan`
- Mac: `~/Code/giaoan`

Từ giờ GitHub lo việc đồng bộ thay cho OneDrive. (Nếu vẫn muốn giữ bản OneDrive làm dự
phòng cá nhân thì được, nhưng **chỉ làm việc trên bản ngoài OneDrive** đã `git clone` về.)

---

## 2. Cài 1 lần (mỗi thầy cô làm trên máy mình)

### a) Cài công cụ
1. **GitHub Desktop** — tải ở <https://desktop.github.com> (Windows & Mac). Đăng nhập tài
   khoản GitHub. *Đây là cách bấm-nút, không cần gõ lệnh.*
2. **Python 3.9+** — <https://www.python.org/downloads/> (Windows nhớ tick *“Add Python to PATH”*).
3. **Tectonic** (engine in PDF) — tải bản chạy sẵn ở <https://tectonic-typesetting.github.io/>.

### b) Lấy kho về (Clone)
- Trong GitHub Desktop: **File → Clone repository →** chọn kho `giaoan` (Thầy Thái mời bạn
  vào trước, xem mục 4) → chọn nơi lưu **ngoài OneDrive** (mục 1) → **Clone**.

### c) Tạo file key riêng `.env`
- Copy file `.env.example` thành `.env`, mở bằng Notepad và điền key của mình:
  ```
  MATHPIX_APP_ID=...
  MATHPIX_APP_KEY=...
  LLM_API_KEY=...
  TECTONIC_BIN=...đường dẫn tới tectonic...
  ```
- File `.env` **không bao giờ lên GitHub** (đã chặn sẵn) → key của ai người nấy giữ.

### d) Cài thư viện Python (mở Terminal / PowerShell trong thư mục dự án)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

Xong phần cài. Từ giờ chỉ còn vòng lặp hằng ngày ở mục 3.

---

## 3. Vòng lặp mỗi buổi làm việc (chỉ cần nhớ 2 bước)

### ⬇️ TRƯỚC khi làm: **Pull** (lấy bản mới nhất)
- Mở GitHub Desktop → bấm **“Fetch origin”** rồi **“Pull origin”**.
- Mục đích: có ngay mọi cải tiến engine + bài mới mà người khác vừa đẩy lên.

### ✍️ Làm việc như bình thường
- Soạn bài bằng các lệnh trong [README.md](README.md) (nhờ Antigravity/Claude điền block
  cũng được). `build` ra PDF trong `outputs/` để in.

### ⬆️ SAU khi làm: **Push** (đẩy đóng góp lên)
- Quay lại GitHub Desktop → ô bên trái hiện các file đã đổi.
- Gõ một dòng mô tả ngắn ở ô **“Summary”** (vd: *“Thêm bài bất phương trình tuần 11”*).
- Bấm **“Commit to main”** → rồi bấm **“Push origin”**.
- Xong! Người khác Pull là thấy.

> Quy tắc vàng: **Pull đầu buổi, Push cuối buổi.** Làm đúng thứ tự này thì gần như không
> bao giờ gặp xung đột.

---

## 4. Việc của Thầy Thái (người quản kho)

1. Tạo **kho riêng tư (Private)** trên GitHub: github.com → **New repository** → đặt tên
   `giaoan` → chọn **Private** → **Create**. (Đừng tick “Add README”.)
2. Liên kết kho đã có ở máy (đã `git init` + commit sẵn) lên GitHub. Trong GitHub Desktop:
   **File → Add local repository →** chọn thư mục `giaoan` → **Publish repository**
   (nhớ giữ tick **Keep this code private**).
3. Mời thầy cô khác: trên GitHub vào kho → **Settings → Collaborators → Add people** →
   nhập tài khoản/email GitHub của họ. Họ bấm chấp nhận lời mời trong email là vào được.

Với 3 người tin nhau, cho mọi người **push thẳng vào `main`** là đơn giản nhất. Khi nào
muốn “duyệt trước khi gộp” thì chuyển sang dùng nhánh + Pull Request (nhờ tôi hướng dẫn thêm).

---

## 5. Khi GitHub Desktop báo “Conflict” (xung đột)

Xảy ra khi hai người sửa **cùng một dòng của cùng một file** rồi cùng đẩy lên. Hiếm gặp.
- GitHub Desktop sẽ liệt kê file bị xung đột và mở chỗ cần chọn.
- Cứ chụp màn hình gửi cho Thầy Thái hoặc nhờ Antigravity/Claude “giải quyết conflict file
  này” — AI đọc được và xử lý nhanh. **Đừng tự xóa lung tung.**

---

## 6. Câu hỏi hay gặp

**Hỏi: Tôi lỡ sửa hỏng, muốn quay lại bản cũ?**
Git lưu mọi mốc. Vào GitHub Desktop → tab **History** xem lại; cần khôi phục thì nhờ
Thầy Thái/AI — không mất dữ liệu đâu.

**Hỏi: Có cần gửi PDF (`outputs/`) cho nhau không?**
Không. PDF không lên GitHub (cho nhẹ kho); ai cần thì `build` lại từ cùng một bộ engine ra
PDF y hệt.

**Hỏi: API key của tôi có bị lộ cho người khác không?**
Không. `.env` bị chặn đẩy lên. Mỗi người tự giữ key riêng.

---

*Cần tôi (Claude/Antigravity) làm hộ bất kỳ bước nào ở trên — cứ mở chat trong thư mục dự
án và nói rõ đang kẹt ở đâu.*
