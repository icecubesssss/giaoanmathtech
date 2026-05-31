# Kịch bản Slide — Thuyết phục Ban lãnh đạo: Chuyển từ soạn Word sang LaTeX tự động xuất PDF

> **Mục đích tài liệu:** Đây là kịch bản chi tiết để dựng bộ slide PowerPoint. Mỗi slide gồm: **Tiêu đề**, **Nội dung hiển thị** (bullet ngắn, đúng tinh thần "ít chữ — nói nhiều"), **Speaker notes** (lời người trình bày), và **Gợi ý hình ảnh/bố cục**. Người dựng slide (Claude trên PowerPoint) hãy bám sát phần này.
>
> **Bối cảnh thực tế (đã kiểm chứng trong codebase ngày 30/05/2026):** Hệ thống đã chạy thật, build ra PDF thật. Số liệu trong slide lấy từ codebase `giaoanMathtech`, không bịa. Phần ước tính thời gian/chi phí được **ghi rõ là ước tính**.
>
> **Bảng màu đề xuất cho slide** (đồng bộ thương hiệu MathTech, lấy từ `config/design_tokens.json`):
> - Mực chính (ink): `#1B1B2A` · Đỏ thương hiệu (brand): `#C0392B` · Nền nhạt: `#F4F6F8` · Chữ phụ: `#6B7280`
> - Font: tiêu đề **Be Vietnam Pro** (đậm), nội dung **Be Vietnam Pro / Inter**. Quy tắc 60-30-10 (nền trắng — mực than — 1 màu nhấn).
> - Tỉ lệ **16:9**. Tối đa ~5 dòng/slide. Không Comic Sans, không gradient loè loẹt, không emoji rải rác.

---

## SLIDE 1 — Bìa

**Tiêu đề:** Nhà máy Học liệu MathTech
**Phụ đề:** Từ "gõ Word từng phiếu" → "một nguồn, ba bản in chuyên nghiệp, tự động"

**Nội dung hiển thị:**
- Một câu định vị: *Soạn một lần — xuất Phiếu học sinh, Sổ tay giáo viên và Slide trình chiếu cùng lúc, đồng bộ tuyệt đối.*
- Dòng nhỏ: Toán Lớp 9 • Ôn thi vào 10 — đã chạy thật cho 41 tuần chương trình.

**Speaker notes:** "Hôm nay tôi xin trình bày một thay đổi về cách chúng ta sản xuất học liệu. Không phải đổi công cụ vì thích công nghệ, mà vì nó giải quyết đúng những điểm đau chúng ta đang gặp mỗi tuần: tốn thời gian, thiếu nhất quán, và khó nhân rộng."

**Gợi ý hình ảnh:** Bên trái logo MathTech; bên phải mock-up 3 trang PDF xếp chồng (handout, guide, slide) — có thể chụp thật từ `outputs/lop-9/dai-so/tuan09-bat-dang-thuc/`.

---

## SLIDE 2 — Vấn đề: Soạn bằng Word đang tốn kém ở đâu

**Tiêu đề:** Quy trình Word — 1 bài, làm tay 3 lần

**Nội dung hiển thị:**
- **Tốn 3 lần công:** phiếu HS, bản có đáp án cho GV, slide trình chiếu — mỗi thứ gõ lại từ đầu.
- **Lệch nhau:** sửa 1 chỗ trên phiếu, quên sửa ở slide → sai khác giữa các bản.
- **Toán xấu & dễ vỡ:** công thức MathType/Equation rớt font, lệch dòng khi đổi máy.
- **Khó nhân rộng:** đổi logo/hotline/độ khó → mở từng file sửa tay hàng trăm bài.
- **Không có "người gác cổng" chất lượng:** sai đề, sai đáp án chỉ phát hiện khi đã in.

**Speaker notes:** "Ai đã từng soạn đều biết: một bài tử tế cho HS, rồi phải làm bản đáp án cho GV, rồi lại dựng slide. Ba sản phẩm, ba lần công, và mỗi lần chỉnh sửa là một lần rủi ro lệch nhau. Chưa kể công thức toán trên Word đổi máy là vỡ."

**Gợi ý hình ảnh:** Sơ đồ 1 bài → mũi tên rẽ 3 nhánh (HS/GV/Slide), mỗi nhánh có biểu tượng "gõ tay" + đồng hồ. Tông xám để gợi "nỗi đau".

---

## SLIDE 3 — Lời giải: Một nguồn dữ liệu, máy lo phần in

**Tiêu đề:** Soạn 1 lần → máy tự xuất 3 bản đồng bộ

**Nội dung hiển thị:**
- Giáo viên chỉ điền **nội dung** (đề, lời giải, gợi ý) vào **một file nguồn**.
- Máy tự dựng và in: **Phiếu HS · Sổ tay GV · Slide TV** — luôn khớp nhau 100%.
- Sửa nội dung 1 chỗ → cả 3 bản cập nhật. Đổi thương hiệu 1 chỗ → toàn bộ phiếu đổi theo.

**Speaker notes:** "Ý tưởng cốt lõi: tách *nội dung* khỏi *trình bày*. Giáo viên lo nội dung — cái họ giỏi. Máy lo phần trình bày, in ấn, đồng bộ — cái máy giỏi. Một nguồn ra ba bản, không bao giờ lệch."

**Gợi ý hình ảnh:** 1 ô "Nguồn (nội dung)" ở giữa → 3 mũi tên ra 3 PDF. Tông màu thương hiệu (đỏ #C0392B cho mũi tên).

---

## SLIDE 4 — Hệ thống đã có thật, không phải ý tưởng

**Tiêu đề:** "Nhà máy Học liệu" — đã vận hành

**Nội dung hiển thị:**
- Đã phủ **khung 41 tuần** cả năm: **22 tuần Đại số + 19 tuần Hình học** (Lớp 9 ôn vào 10).
- Mỗi bài theo **5 chặng sư phạm × 4 tầng độ khó** (chuẩn hoá cách dạy).
- Đã build ra **PDF thật**: phiếu HS, sổ tay GV, slide, và phiếu tổng kết chương.
- Có **chữ ký giáo viên cố định** trên mọi bản in (Thầy Thái MathTech • 0386969199).

**Speaker notes:** "Đây không phải slide bán giấc mơ. Hệ thống đã chạy: khung chương trình cả năm đã dựng, và những bài đầu tiên đã ra PDF hoàn chỉnh mà lát nữa tôi sẽ cho xem. Mọi bản in đều tự động mang thương hiệu và chữ ký giáo viên — không phải dán tay."

**Gợi ý hình ảnh:** Ảnh chụp màn hình lệnh `progress` (cây tuần) + 3 thumbnail PDF thật.

---

## SLIDE 5 — Dây chuyền hoạt động (đơn giản hoá)

**Tiêu đề:** Quy trình 5 bước, phần "máy làm" chỉ tính bằng giây

**Nội dung hiển thị (đánh số):**
1. **`progress`** — máy quét xem tuần nào còn thiếu bài.
2. **`new-lesson`** — máy sinh sẵn khung bài (5 chặng) để điền.
3. **Điền nội dung** — giáo viên (có **Claude** hỗ trợ) đổ đề & lời giải vào khung.
4. **`validate`** — "trọng tài" tự kiểm: an toàn, cấu trúc, độ khó, trình bày, toán học.
5. **`approve` → `build`** — duyệt rồi xuất **3 PDF** trong vài giây.

**Speaker notes:** "Năm bước. Bước tốn chất xám là bước 3 — nội dung — và đó là việc của giáo viên. Tất cả phần còn lại máy lo. Đặc biệt bước 4: trước khi in, hệ thống tự kiểm tra chất lượng, điều mà Word không có."

**Gợi ý hình ảnh:** Pipeline ngang 5 hộp, mũi tên nối. Hộp 3 tô đậm (con người) — các hộp khác xám nhạt (máy).

---

## SLIDE 6 — DEMO: Một bài → ba bản in

**Tiêu đề:** Cùng một nguồn, ba sản phẩm — xem tận mắt

**Nội dung hiển thị:**
- **Phiếu HS:** sạch, có chỗ trống điền, ẩn lời giải.
- **Sổ tay GV:** y hệt phiếu HS + **lời giải** + mẹo điều phối.
- **Slide TV:** Beamer 16:9, chữ to đọc từ cuối lớp.
- Cả ba **tự khớp** số bài, đề bài, ký hiệu toán.

**Speaker notes (kèm thao tác):** "Đây là bài *Bất đẳng thức* tuần 9 — đã build thật. [Mở 3 PDF cạnh nhau.] Để ý: cùng Bài 1, cùng công thức, nhưng phiếu HS để trống, sổ tay GV có lời giải đỏ, slide thì chữ to. Tôi không làm 3 lần — tôi làm 1 lần."

**Gợi ý hình ảnh:** 3 ảnh PDF thật cạnh nhau, lấy từ:
`outputs/lop-9/dai-so/tuan09-bat-dang-thuc/bdt-tinh-chat-va-so-sanh/{handout,guide,slide}.pdf`
(Chèn ảnh trang đầu mỗi bản; khoanh đỏ chỗ "HS để trống vs GV có đáp án".)

---

## SLIDE 7 — Khác biệt 1: Chất lượng in ấn chuyên nghiệp

**Tiêu đề:** Đẹp như sách xuất bản — nhờ XeLaTeX, không phải Word

**Nội dung hiển thị:**
- **Toán học chuẩn nhà in:** typesetting LaTeX, công thức không vỡ, không lệch.
- **Hệ thiết kế thống nhất** (`design_tokens`): font, màu, lề, giãn dòng — một bộ chuẩn.
- **Font tiếng Việt nhúng sẵn** (STIX Two + Be Vietnam Pro) → mở máy nào cũng giống.
- **Quy tắc 60-30-10**, lề rộng, tương phản đạt chuẩn dễ đọc.

**Speaker notes:** "LaTeX là chuẩn typesetting của giới xuất bản học thuật toàn cầu — sách giáo khoa, tạp chí toán đều dùng. Công thức đẹp, nhất quán, và vì font nhúng sẵn nên bản in trên máy nào cũng y hệt. Không còn cảnh 'máy em mở ra bị lỗi font'."

**Gợi ý hình ảnh:** So sánh cận cảnh một công thức phân thức/căn: bản Word (lệch, xấu) vs bản LaTeX (sắc nét). Trích từ phiếu thật.

---

## SLIDE 8 — Khác biệt 2: Sư phạm được "đóng khung"

**Tiêu đề:** Mỗi phiếu đi đúng 5 chặng — không phụ thuộc tay nghề từng người

**Nội dung hiển thị:**
- **5 chặng:** Khám phá → Khái niệm (ví dụ mẫu) → Luyện tập nền → Luyện tập vận dụng (chạm trần thi vào 10) → Tổng kết (sơ đồ tư duy).
- **4 tầng độ khó** rõ ràng: ví dụ mẫu · trên lớp · BTVN · mở rộng.
- **Tầng mở rộng là "thang", không dốc đứng** — mỗi bài khó hơn đúng một bước, kèm gợi ý.

**Speaker notes:** "Cấu trúc này không phải để cho đẹp — nó ép mọi phiếu, dù ai soạn, đều có cùng một mạch sư phạm chuẩn. Bài mới vào nghề hay giáo viên kỳ cựu, đầu ra vẫn đồng đều. Đây là cách chúng ta đảm bảo *chất lượng dạy học* chứ không chỉ chất lượng hình thức."

**Gợi ý hình ảnh:** Băng ngang 5 chặng với icon; phía dưới là "thang độ khó" 4 bậc đi lên.

---

## SLIDE 9 — Khác biệt 3: Có "trọng tài" gác cổng chất lượng

**Tiêu đề:** Máy tự bắt lỗi trước khi in — Word không làm được

**Nội dung hiển thị:**
- **Kiểm an toàn** (sanitizer): chặn mã LaTeX nguy hiểm.
- **Kiểm cấu trúc** (schema): đủ 5 chặng, đúng định dạng.
- **Kiểm độ khó** (difficulty + gradient): bài khó nhất phải chạm trần thi; mở rộng phải có thang & gợi ý.
- **Kiểm trình bày** (visual linter): cảnh báo ghi chú GV lọt phiếu HS, dòng quá dài, **ký tự `&`/`%`/`#` chưa escape** (lỗi làm vỡ bản in).
- **Kiểm TOÁN HỌC** (SymPy): máy **giải lại độc lập** để đối chiếu đáp án.
- **Gác cổng cả kho** (`validate-all`): kiểm **toàn bộ** phiếu một lượt trước khi in/bàn giao.

**Speaker notes:** "Đây là thứ tôi tâm đắc nhất. Trước khi một phiếu được in, nó phải qua một loạt 'trọng tài' tự động — và có thể quét sạch cả kho bằng một lệnh. Đặc biệt, hệ thống dùng SymPy *giải lại bài toán* một cách độc lập rồi so với đáp án — bắt được lỗi toán mà mắt người dễ bỏ sót. Với Word, lỗi chỉ lộ ra khi học sinh đã cầm phiếu."

**Gợi ý hình ảnh:** Ảnh chụp output lệnh `validate` thật (các dòng `latex_sanitizer: OK`, `difficulty_gate: OK`, …). Icon khiên/checkmark.

---

## SLIDE 10 — Khác biệt 4: Sửa một chỗ, đổi toàn hệ thống

**Tiêu đề:** Thương hiệu & thiết kế: quản lý tập trung

**Nội dung hiển thị:**
- Logo, hotline, tên công ty, màu, font → nằm ở **một file cấu hình duy nhất**.
- Đổi số hotline? Sửa 1 dòng → một lệnh **`rebuild`** in lại **toàn bộ** phiếu đồng loạt, không sót bản nào.
- Chữ ký giáo viên là phần cố định của khuôn in → **không bao giờ quên, không in thiếu**.

**Speaker notes:** "Hãy tưởng tượng phải đổi hotline trên 300 file Word. Ở đây, sửa một dòng là xong. Nhận diện thương hiệu được đảm bảo tuyệt đối trên mọi sản phẩm — điều rất quan trọng nếu ta muốn học liệu mang dấu ấn trung tâm một cách chuyên nghiệp."

**Gợi ý hình ảnh:** 1 file config ở giữa → toả ra nhiều phiếu đều mang cùng logo/màu.

---

## SLIDE 11 — Cộng tác & an toàn dữ liệu

**Tiêu đề:** Nhiều giáo viên cùng soạn — có lịch sử, không đè nhau

**Nội dung hiển thị:**
- Lưu trên **Git/GitHub**: nhiều người soạn song song, có **lịch sử chỉnh sửa**, hoàn tác được.
- Không còn "phieu_final_v3_sửa_lần_cuối_thật.docx".
- **Bảo mật:** trình biên dịch chạy chế độ an toàn (không cho lệnh hệ thống), key cấu hình không lên mạng.
- Hướng dẫn đồng bộ đa trung tâm đã có sẵn (`HUONG-DAN-DONG-BO.md`).

**Speaker notes:** "Vì học liệu là file văn bản thuần, ta quản lý nó như mã nguồn: ai sửa gì, khi nào, đều có dấu vết; cần thì quay lại bản cũ trong vài giây. Nhiều trung tâm/giáo viên cùng đóng góp vào một kho chung mà không giẫm chân nhau."

**Gợi ý hình ảnh:** Sơ đồ nhiều người → 1 kho GitHub → mọi người kéo bản mới nhất.

---

## SLIDE 12 — Word vs LaTeX tự động (bảng so sánh)

**Tiêu đề:** Đặt lên bàn cân

**Nội dung hiển thị (dạng bảng):**

| Tiêu chí | Soạn Word | LaTeX tự động (hệ thống này) |
|---|---|---|
| Số lần làm cho 1 bài | 3 (HS/GV/slide) | **1 nguồn → 3 bản** |
| Đồng bộ giữa các bản | Làm tay, dễ lệch | **Tự động, luôn khớp** |
| Chất lượng công thức toán | Dễ vỡ, lệch font | **Chuẩn nhà in** |
| Đổi thương hiệu hàng loạt | Sửa từng file | **Sửa 1 chỗ** |
| Kiểm tra chất lượng | Bằng mắt | **Trọng tài tự động + SymPy** |
| Cộng tác & lịch sử | File rời, dễ trùng | **Git: có vết, hoàn tác** |
| Thời gian phần "in/ráp" | Tính bằng giờ | **Tính bằng giây** |

**Speaker notes:** "Cột phải không phải là lời hứa — đó là những gì hệ thống đang làm hôm nay. Điểm mấu chốt không phải 'LaTeX xịn hơn Word', mà là *chúng ta chuyển phần lặp đi lặp lại cho máy*, giữ lại cho giáo viên đúng phần sáng tạo."

**Gợi ý hình ảnh:** Bảng 2 cột, cột phải tô nền nhạt màu thương hiệu, các ô "thắng" có dấu ✓.

---

## SLIDE 13 — Lợi ích kinh tế (ROI) — *ước tính*

**Tiêu đề:** Tiết kiệm thời gian = tiết kiệm chi phí, và nhân rộng được

**Nội dung hiển thị:**
- **Mỗi bài:** phần ráp/định dạng/làm slide từ ~**60–90 phút** (Word) → gần **0** (máy build vài giây). *(ước tính)*
- Giáo viên dồn thời gian vào **nội dung & học sinh**, không vào căn lề.
- **Nhân rộng:** khung đã dựng cho cả năm → mỗi tuần thêm bài là tận dụng lại toàn bộ hạ tầng.
- **Tài sản tích luỹ:** mỗi phiếu là tài sản số tái dùng, không phải file rời dễ thất lạc.

**Speaker notes:** "Xin nhấn mạnh đây là *ước tính* để hình dung quy mô, không phải con số quyết toán. Điểm cốt lõi: chi phí lớn nhất trong soạn học liệu là thời gian con người làm việc lặp lại. Hệ thống cắt gần hết phần đó. Càng nhiều bài, càng nhiều giáo viên, lợi ích càng nhân lên — vì hạ tầng chỉ dựng một lần."

**Gợi ý hình ảnh:** Biểu đồ cột so sánh "giờ công/bài" Word vs Hệ thống; chú thích nhỏ "*ước tính*". (Số liệu chi tiết ở Phụ lục A.)

---

## SLIDE 14 — Lường trước băn khoăn

**Tiêu đề:** "Thế còn…?" — và câu trả lời

**Nội dung hiển thị:**
- *"Giáo viên phải học LaTeX?"* → **Không.** Giáo viên điền nội dung vào khung; **Claude hỗ trợ** chuyển nội dung đúng định dạng.
- *"Lỡ máy sinh sai?"* → Có **trọng tài tự động** + bước **giáo viên duyệt** (`approve`) trước khi in.
- *"Phụ thuộc một người kỹ thuật?"* → Quy trình & tài liệu đã chuẩn hoá; kho dùng chung, ai cũng chạy được vài lệnh.
- *"Chi phí công cụ?"* → Dùng phần mềm **mã nguồn mở, miễn phí** (XeLaTeX/Tectonic, Python). **Không phụ thuộc API trả phí** (đã gỡ pipeline OCR/LLM trả phí — dùng Claude để soạn nội dung).

**Speaker notes:** "Băn khoăn lớn nhất thường là 'giáo viên có phải thành lập trình viên không'. Không. Họ làm đúng việc chuyên môn — ra đề, giải, gợi ý — và có Claude đỡ phần định dạng. Hệ thống cũng vừa được tinh gọn: bỏ các thành phần phụ thuộc dịch vụ trả tiền, giữ lại lõi chạy hoàn toàn bằng công cụ miễn phí."

**Gợi ý hình ảnh:** 4 cặp "câu hỏi → trả lời", icon dấu hỏi chuyển thành dấu tích.

---

## SLIDE 15 — Đề xuất & lộ trình

**Tiêu đề:** Kiến nghị Ban lãnh đạo

**Nội dung hiển thị:**
- **Phê duyệt** chọn quy trình LaTeX tự động làm **chuẩn sản xuất học liệu** cho Toán 9.
- **Giai đoạn 1 (đang chạy):** hoàn thiện trọn vẹn các tuần Đại số/Hình học còn lại.
- **Giai đoạn 2:** tập huấn ngắn cho nhóm giáo viên cốt cán + quy trình duyệt.
- **Giai đoạn 3:** mở rộng sang lớp/môn khác bằng chính khung này.
- **Đề nghị nguồn lực:** 1 đầu mối kỹ thuật + thời gian tập huấn; công cụ miễn phí.

**Speaker notes:** "Cụ thể tôi xin ba điều: một, chấp thuận đây là chuẩn sản xuất; hai, cho phép nhóm cốt cán dành thời gian tập huấn; ba, duy trì một đầu mối kỹ thuật. Đổi lại, ta có dây chuyền học liệu nhất quán, chất lượng cao, và nhân rộng được mà gần như không tốn chi phí phần mềm."

**Gợi ý hình ảnh:** Timeline 3 giai đoạn, mốc "đang ở đây" tại Giai đoạn 1.

---

## SLIDE 16 — Kết

**Tiêu đề:** Giáo viên lo nội dung. Máy lo phần còn lại.

**Nội dung hiển thị:**
- Một nguồn → ba bản in chuyên nghiệp, đồng bộ, có kiểm soát chất lượng.
- Đã chạy thật, miễn phí công cụ, nhân rộng được.
- *Sẵn sàng để duyệt và mở rộng.*

**Speaker notes:** "Tóm lại một câu: chúng ta để giáo viên làm điều họ giỏi nhất — dạy và ra đề — còn việc lặp lại, định dạng, đồng bộ thì giao cho máy. Hệ thống đã sẵn sàng. Rất mong nhận được sự ủng hộ của Ban lãnh đạo. Xin cảm ơn."

**Gợi ý hình ảnh:** Logo MathTech lớn + chữ ký "Thầy Thái MathTech • 0386969199". Nền sạch.

---

# PHỤ LỤC A — Số liệu ROI để dựng biểu đồ

> Người dựng slide có thể chèn biểu đồ từ bảng này. **Mọi con số thời gian là ƯỚC TÍNH** để minh hoạ quy mô; số liệu cấu trúc (tuần, bản in, chặng) là **thực tế trong codebase**.

**Dữ kiện thực tế (chắc chắn):**
- 41 tuần khung chương trình = 22 Đại số + 19 Hình học (Lớp 9 ôn vào 10).
- Mỗi bài xuất 3 bản: `handout.pdf`, `guide.pdf`, `slide.pdf`. Mỗi chương thêm phiếu tổng kết (bản HS + bản GV).
- Thời gian máy build 3 bản: cỡ **vài giây/bài** (engine Tectonic/XeLaTeX).
- 7 lớp kiểm tra chất lượng tự động khi `validate` (sanitizer, schema, difficulty, gradient, visual linter, SymPy, geometry).

**Bảng ước tính giờ công cho phần "ráp & định dạng" (KHÔNG tính thời gian nghĩ nội dung — phần đó như nhau ở cả hai cách):**

| Hạng mục | Word (ước tính) | Hệ thống (ước tính) |
|---|---|---|
| Định dạng phiếu HS | 20–30 phút | ~0 (máy) |
| Tạo bản GV có đáp án | 15–25 phút | ~0 (đồng bộ tự động) |
| Dựng slide trình chiếu | 25–35 phút | ~0 (đồng bộ tự động) |
| Đồng bộ khi sửa nội dung | 10–20 phút/lần sửa | ~0 (build lại vài giây) |
| **Tổng phần ráp/định dạng** | **~60–90 phút/bài** | **~vài phút (điền khung + build)** |

**Cách quy đổi gợi ý (người trình bày tự điền theo thực tế trung tâm):**
- Tiết kiệm/bài × số bài/năm × số giáo viên = tổng giờ tiết kiệm.
- Ví dụ minh hoạ: 70 phút/bài × 100 bài/năm ≈ **~116 giờ/năm/giáo viên** dành lại cho chuyên môn. *(ước tính)*

**Biểu đồ đề xuất:**
1. Cột đôi "Giờ công ráp/bài: Word vs Hệ thống".
2. Cột chồng "1 bài = 3 sản phẩm" cho thấy Word nhân 3 công, hệ thống giữ 1.
3. Đường tích luỹ "Tổng giờ tiết kiệm theo số bài" (dốc lên nhanh).

---

# PHỤ LỤC B — Bảng lệnh (nếu lãnh đạo muốn xem quy trình thật)

```text
progress [--grade lop-9] [--subject dai-so] [--todo]   # quét tuần còn thiếu
new-lesson <folder tuần>                                # sinh khung 5 chặng để điền
validate <file.json>                                    # trọng tài chất lượng tự động (1 bài)
validate-all [--grade --subject]                        # gác cổng CẢ KHO trước khi in/bàn giao
approve  <slug>                                         # giáo viên duyệt
build    <file.json>                                    # xuất 3 PDF: handout, guide, slide
build-summary <file.json>                               # phiếu tổng kết chương (HS + GV)
rebuild  [--grade --subject --all]                      # build lại HÀNG LOẠT sau khi đổi thiết kế/thương hiệu
```

> Luật soạn bài (để Claude/giáo viên điền nội dung đúng chuẩn) nằm ở `HUONG-DAN-SOAN-BAI.md`.

Đầu ra nằm ở: `outputs/<lớp>/<môn>/<tuần>/<slug>/{handout,guide,slide}.pdf`

---

# PHỤ LỤC C — Ảnh/PDF thật để chèn vào slide

Lấy trực tiếp từ thư mục `outputs/` (đã build thật, đã kiểm chứng chạy được):
- `outputs/lop-9/dai-so/tuan09-bat-dang-thuc/bdt-tinh-chat-va-so-sanh/handout.pdf`
- `.../bdt-tinh-chat-va-so-sanh/guide.pdf`
- `.../bdt-tinh-chat-va-so-sanh/slide.pdf`
- `outputs/lop-9/dai-so/tuan09-bat-dang-thuc/tong-ket-bat-dang-thuc/tongket-hs.pdf` (sơ đồ trống)
- `.../tong-ket-bat-dang-thuc/tongket-gv.pdf` (kèm đáp án)

> Mẹo dựng slide: chụp trang 1 mỗi PDF làm ảnh nền minh hoạ; với cặp HS/GV hãy đặt cạnh nhau và khoanh đỏ vùng "để trống vs có đáp án" để làm bật tính đồng bộ.
