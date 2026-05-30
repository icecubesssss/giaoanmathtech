# Hướng dẫn đồng bộ MathTech Engine giữa các thầy cô

Tài liệu này thay cho cách gửi file zip. Mục tiêu: **một kho chung trên GitHub**, ai
cập nhật engine cũng đẩy lên được, mọi người kéo về là có bản mới — không gửi zip lần nào nữa.

> Dành cho thầy cô **không rành kỹ thuật**: cứ làm theo phần "Cài 1 lần" rồi mỗi buổi
> chỉ cần nhớ **tạo nhánh phụ, làm xong bấm Commit & Push rồi gửi Pull Request** để Admin duyệt.

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

## 3. Vòng lặp mỗi buổi làm việc

### ⬇️ TRƯỚC khi làm: **Lấy bản mới nhất & Tạo nhánh phụ**
1. Mở GitHub Desktop $\rightarrow$ chọn Current Branch (nhánh hiện tại) ở thanh công cụ phía trên là **`main`**.
2. Bấm **“Fetch origin”** rồi **“Pull origin”** để tải bản mới nhất về máy.
3. Bấm lại vào nút **Current Branch** $\rightarrow$ chọn **New branch** $\rightarrow$ đặt tên cho nhánh của mình (vd: `bai-tuan-12` hoặc tên của mình) $\rightarrow$ bấm **Create branch** (để tạo nhánh từ `main`).

### ✍️ Làm việc như bình thường
- Soạn bài bằng các lệnh trong [README.md](README.md). `build` ra PDF trong `outputs/` để in.

### ⬆️ SAU khi làm: **Gửi yêu cầu duyệt (Pull Request)**
1. Quay lại GitHub Desktop $\rightarrow$ ô bên trái hiện các file đã đổi.
2. Gõ một dòng mô tả ngắn ở ô **“Summary”** (vd: *“Thêm bài bất phương trình tuần 11”*).
3. Bấm **“Commit to [tên-nhánh-của-bạn]”**.
4. Bấm **“Publish branch”** (hoặc **Push origin**) để đưa nhánh lên GitHub.
5. GitHub Desktop sẽ hiện ra nút màu xanh **“Create Pull Request”** $\rightarrow$ bấm vào đó để mở trang web GitHub $\rightarrow$ bấm nút **“Create pull request”** trên web để gửi yêu cầu cho Admin duyệt.

> Quy tắc vàng: **Luôn cập nhật `main` trước, tạo nhánh riêng để làm, và gửi Pull Request sau cùng.**

---

## 4. Việc của Thầy Thái (người quản kho)

Repo: <https://github.com/icecubesssss/giaoanmathtech>

### a) Tạo kho và đẩy code lên (làm 1 lần)
1. Tạo kho trên GitHub: github.com → **New repository** → đặt tên `giaoanmathtech` →
   **Create**. (Đừng tick "Add README".) *Lúc đầu để Private cũng được, sau muốn chia sẻ
   rộng thì chuyển sang Public ở mục (a-bis).*
2. Liên kết kho đã có ở máy (đã `git init` + commit sẵn) lên GitHub. Trong GitHub Desktop:
   **File → Add local repository →** chọn thư mục `giaoan` → **Publish repository**.
3. Mời thầy cô khác: trên GitHub vào kho → **Settings → Collaborators → Add people** →
   nhập **username hoặc email GitHub** của họ. Họ bấm **Accept invitation** trong email là vào được.
   *(Mỗi thầy cô cần có sẵn một tài khoản GitHub.)*

### a-bis) Chuyển kho thành Public (khi muốn chia sẻ rộng)
Public = ai trên Internet cũng **xem và clone** được code, nhưng **chỉ collaborator mới sửa được**.

1. Vào kho trên GitHub → **Settings**.
2. Kéo xuống cuối cùng, mục **Danger Zone**.
3. Dòng **Change repository visibility** → bấm **Change visibility** → chọn **Make public**.
4. Gõ xác nhận tên kho → xác nhận.

> ⚠️ Khi đã Public: tuyệt đối **không commit file nhạy cảm** (mật khẩu, API key, thông tin
> học sinh). File `.env` đã bị chặn sẵn nên key vẫn an toàn — nhưng hãy kiểm tra kỹ trước khi commit.

### b) Bật chế độ kiểm duyệt (Branch Protection — làm 1 lần)
Mục đích: **chặn không cho ai push thẳng vào `main`** (kể cả lỡ tay xoá/ghi đè), bắt buộc
phải tạo Pull Request và được Admin duyệt thì bài mới được gộp vào.

> Lưu ý: tính năng này dùng được khi kho **Public**, hoặc kho Private với gói **GitHub Pro/Team**.

1. Trên GitHub, vào kho `giaoanmathtech` → **Settings** (thanh menu phía trên).
2. Cột bên trái chọn **Branches**.
3. Mục **Branch protection rules** → bấm **Add branch protection rule** (hoặc **Add rule** /
   **Add ruleset** ở giao diện mới).
4. Ô **Branch name pattern** → gõ: `main`.
5. Tích chọn các mục khuyến nghị:
   - ☑ **Require a pull request before merging** — bắt buộc tạo Pull Request, cấm push thẳng.
     - ☑ **Require approvals** — chọn số người duyệt là **1** (chính là Admin).
   - ☑ **Require conversation resolution before merging** — phải xử lý hết comment review.
   - ☑ **Block force pushes** — cấm ghi đè lịch sử.
   - ☑ **Restrict deletions** — cấm xoá branch `main`.
6. Kéo xuống cuối trang → bấm **Create** (hoặc **Save changes**).

Sau bước này, không ai (kể cả Admin) có thể push thẳng vào `main` nữa. Mọi thay đổi đều
phải đi qua Pull Request.

> 💡 Mẹo: nếu chỉ có mình Admin làm và muốn nhanh, có thể **không** tích "Require approvals"
> để tự merge Pull Request của mình mà không cần người khác duyệt — vẫn giữ được lịch sử
> sạch và tránh push nhầm vào `main`.

### c) Duyệt bài mỗi ngày (quy trình của Admin)
1. Khi giáo viên gửi Pull Request, Admin nhận được **email thông báo** từ GitHub.
2. Vào GitHub → mở tab **Pull requests** → bấm vào yêu cầu đang chờ.
3. Chuyển sang tab **Files changed** để xem họ thêm/sửa gì.
4. Nếu ổn → bấm **Review changes** → chọn **Approve** → bấm **Submit review**.
5. Bấm nút xanh **Merge pull request** → **Confirm merge** để gộp bài vào `main`.
6. Xong! Từ giờ mọi người khác Pull về sẽ có bài mới.

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
Không. `.env` bị chặn đẩy lên. Mỗi người tự giữ key riêng. *(Kể cả khi kho để Public.)*

**Hỏi: Một người dùng Mac, một người dùng Windows thì có bị lỗi khi gộp không?**
Không. Dự án đã được cấu hình để hoạt động chéo nền tảng:
- Có file `.gitattributes` tự chuẩn hóa dấu xuống dòng (LF/CRLF) tránh lỗi lệch định dạng.
- Các file rác hệ điều hành (`.DS_Store` của Mac, `Thumbs.db` của Win) đã bị chặn trong `.gitignore`.
- Mỗi máy tự giữ cấu hình đường dẫn và môi trường ảo riêng (`.env`, `.venv`), không chia sẻ lên GitHub.

---

*Cần tôi (Claude/Antigravity) làm hộ bất kỳ bước nào ở trên — cứ mở chat trong thư mục dự
án và nói rõ đang kẹt ở đâu.*
