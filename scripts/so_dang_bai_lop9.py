"""NỘI DUNG SỔ DẠNG BÀI TOÁN 9 (Hà Nội, KNTT) — dữ liệu cho scripts/build_so_dang_bai.py.

Mỗi mục = một (tiểu) dạng: tên, cách nhận dạng, các bước giải, lỗi hay gặp, và bài mẫu lấy
từ ĐỀ THẬT (mã câu ngân hàng `inputs/refs/de-thi/lop-9/exams/` hoặc đề PDF ghi ở `nguon`).

Lời giải viết theo NHỊP ĐI THI Thầy chốt 24/09/2026: nêu cấu hình → ⇒ → chuỗi đẳng thức →
dừng; mỗi bước có căn cứ ngắn; "Vậy …" đúng một lần ở cuối. Đáp số đã kiểm bằng máy
(scripts/build_so_dang_bai.py --kiem) và đối chiếu barem gốc khi đề có hướng dẫn chấm.

`tan_suat` trỏ vào tên dạng/tiểu dạng/bối cảnh trong scripts/thong_ke_dang_de.py để in tần
suất xuất hiện theo kỳ (đo trên kho đề Hà Nội đã bỏ đề lệch KNTT).
"""

# ─────────────────────────── HÌNH VẼ (toạ độ đã tính & kiểm bằng máy) ───────────────────────────
HINH_AI_MO = r"""
\begin{tikzpicture}[scale=0.62,font=\small]
\coordinate (O) at (0,0); \coordinate (A) at (-2.6,0); \coordinate (B) at (2.6,0);
\coordinate (C) at (1.221,2.296); \coordinate (H) at (1.221,0); \coordinate (D) at (1.221,-2.296);
\coordinate (M) at (-2.6,4.327); \coordinate (F) at (5.538,0);
\draw (O) circle (2.6);
\draw (A)--(F); \draw (C)--(D); \draw (A)--(M)--(F); \draw (D)--(F); \draw (O)--(C); \draw (O)--(D);
\draw (A)--(C)--(B); \draw[dashed] (O)--(M);
\foreach \p/\q in {O/below,A/left,B/below right,C/above right,H/below left,D/below,M/left,F/below}
  {\fill (\p) circle (1.3pt); \node[\q] at (\p) {$\p$};}
\end{tikzpicture}"""

HINH_SO_2026 = r"""
\begin{tikzpicture}[scale=0.75,font=\small]
\coordinate (O) at (0,0); \coordinate (B) at (-2.6,0); \coordinate (C) at (2.6,0);
\coordinate (A) at (-1.221,2.296); \coordinate (H) at (-1.745,1.423); \coordinate (D) at (-1.745,0);
\coordinate (E) at (-1.745,2.611);
\draw (O) circle (2.6); \draw (B)--(C)--(A)--cycle; \draw (E)--(D); \draw (A)--(E); \draw[dashed] (H)--(C);
\draw ($(D)+(0.22,0)$)--++(0,0.22)--++(-0.22,0);
\foreach \p/\q in {O/below,B/left,C/right,A/above,H/left,D/below,E/above left}
  {\fill (\p) circle (1.3pt); \node[\q] at (\p) {$\p$};}
\end{tikzpicture}"""

HINH_THAP = r"""
\begin{tikzpicture}[scale=0.55,font=\small]
\coordinate (A) at (0,0); \coordinate (B) at (0,3.4); \coordinate (C) at (5.0,0);
\draw (A)--(B)--(C)--cycle; \draw (0.3,0)--(0.3,0.3)--(0,0.3);
\draw (C)++(180:0.9) arc (180:146:0.9); \node at ($(C)+(158:1.35)$) {$34^\circ$};
\node[below] at ($(A)!0.5!(C)$) {$8{,}6$ m}; \node[left] at (B) {$B$}; \node[below left] at (A) {$A$}; \node[below right] at (C) {$C$};
\end{tikzpicture}"""

HINH_NUI = r"""
\begin{tikzpicture}[scale=0.85,font=\small]
\coordinate (H) at (0,0); \coordinate (D) at (0,4.2); \coordinate (A) at (5.005,0); \coordinate (B) at (6.721,0);
\draw (H)--(D); \draw (H)--(B); \draw (A)--(D)--(B); \draw (0.25,0)--(0.25,0.25)--(0,0.25);
\draw (A)++(180:0.7) arc (180:140:0.7); \draw (B)++(180:1.25) arc (180:148:1.25);
\node[left] at (D) {$D$}; \node[below left] at (H) {$H$}; \node[below] at (A) {$A$}; \node[below] at (B) {$B$};
\node[font=\scriptsize] at ($(A)+(162:1.0)$) {$40^\circ$}; \node[font=\scriptsize] at ($(B)+(166:1.55)$) {$32^\circ$};
\draw[decorate,decoration={brace,mirror,amplitude=4pt}] ($(A)+(0,-0.5)$)--($(B)+(0,-0.5)$) node[midway,below=4pt] {$1000$ m};
\end{tikzpicture}"""

HINH_BO = r"""
\begin{tikzpicture}[scale=0.55,font=\small]
\draw (0,0) rectangle (5,5); \fill[gray!25] (0,0)--(1.5,0) arc (0:90:1.5)--cycle; \draw (1.5,0) arc (0:90:1.5);
\fill (0,0) circle (1.6pt); \node[below left] at (0,0) {cột};
\node[below] at (2.5,0) {$5$ m}; \draw[->] (0,0)--(1.06,1.06); \node at (1.25,0.55) {\scriptsize $1{,}5$};
\end{tikzpicture}"""

HINH_PARABOL = r"""
\begin{tikzpicture}[xscale=0.85,yscale=0.4,font=\small]
\draw[->] (-3,0)--(3,0) node[right] {$x$}; \draw[->] (0,-0.6)--(0,8.8) node[above] {$y$};
\draw[thick,domain=-2.05:2.05,samples=60] plot (\x,{2*\x*\x});
\foreach \x/\y in {-2/8,-1/2,0/0,1/2,2/8} {\fill (\x,\y) circle (2.5pt);}
\foreach \x in {-2,-1,1,2} {\draw[dashed,gray] (\x,0)--(\x,{2*\x*\x}); \node[below] at (\x,0) {\scriptsize $\x$};}
\node[left] at (0,2) {\scriptsize $2$}; \node[left] at (0,8) {\scriptsize $8$}; \node[below left] at (0,0) {\scriptsize $O$};
\end{tikzpicture}"""

# ─────────────────────────── NỘI DUNG ───────────────────────────
MUC = [
# ═══════════════════ CHƯƠNG I ═══════════════════
dict(chuong="I. Phương trình và hệ hai phương trình bậc nhất hai ẩn",
     ten="Giải hệ hai phương trình bậc nhất hai ẩn",
     tan_suat=("Giải hệ phương trình", "hệ hai PT bậc nhất hai ẩn (thế / cộng đại số)"),
     nhan_dang=r"Đề cho sẵn hệ $\begin{cases}ax+by=c\\a'x+b'y=c'\end{cases}$, yêu cầu \emph{giải hệ}.",
     buoc=[r"Chọn phương pháp: hệ số của một ẩn bằng/đối nhau $\Rightarrow$ cộng/trừ vế; có ẩn hệ số $1$ $\Rightarrow$ thế.",
           r"Khử một ẩn, giải ra ẩn còn lại, thay ngược để tìm ẩn kia.",
           r"Kết luận nghiệm dạng cặp $(x;y)$."],
     loi=r"Nhân hai vế nhưng quên nhân vế phải; viết kết luận $x=\ldots,\ y=\ldots$ mà không ghi thành cặp nghiệm.",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 1b (0,75 điểm)", ma="gk1-bat-trang-1b",
               de=r"Giải hệ phương trình $\begin{cases}5x+7y=-1\\3x+2y=-5\end{cases}$.",
               loi_giai=[r"$\begin{cases}5x+7y=-1\\3x+2y=-5\end{cases}\Leftrightarrow\begin{cases}10x+14y=-2\\21x+14y=-35\end{cases}$ (nhân phương trình thứ nhất với $2$, thứ hai với $7$).",
                         r"Trừ vế: $11x=-33\Rightarrow x=-3$.",
                         r"Thay $x=-3$ vào $3x+2y=-5$: $-9+2y=-5\Rightarrow y=2$.",
                         r"Vậy hệ có nghiệm duy nhất $(x;y)=(-3;2)$."],
               kiem=dict(he=["5*x+7*y+1", "3*x+2*y+5"], nghiem={"x": -3, "y": 2}))]),

dict(chuong="I. Phương trình và hệ hai phương trình bậc nhất hai ẩn",
     ten="Hệ phải khai triển rồi mới về bậc nhất",
     tan_suat=("Giải hệ phương trình", "hệ quy về bậc nhất (khai triển có xy, đặt ẩn phụ 1/x…)"),
     nhan_dang=r"Mỗi phương trình là tích hai ngoặc bằng một biểu thức có $xy$ (hoặc chứa $\tfrac1x,\ \tfrac1y$): khai triển thì $xy$ triệt tiêu.",
     buoc=[r"Khai triển từng phương trình, rút gọn về dạng $ax+by=c$.",
           r"Giải hệ bậc nhất vừa nhận được.",
           r"Kết luận nghiệm."],
     loi=r"Khai triển sai dấu ở tích $(4x+5)(y-5)$ (bỏ sót $-25$).",
     bai=[dict(nguon="THCS Ái Mộ · CK1 2025–2026 · Bài 2.1 (0,5 điểm, có barem gốc)", ma="ck1-ai-mo-2-1",
               de=r"Giải hệ phương trình $\begin{cases}(3x+2)(2y-3)=6xy\\(4x+5)(y-5)=4xy\end{cases}$.",
               loi_giai=[r"$(3x+2)(2y-3)=6xy\Leftrightarrow 6xy-9x+4y-6=6xy\Leftrightarrow -9x+4y=6$.",
                         r"$(4x+5)(y-5)=4xy\Leftrightarrow 4xy-20x+5y-25=4xy\Leftrightarrow -4x+y=5$.",
                         r"$-4x+y=5\Rightarrow y=4x+5$. Thay vào $-9x+4y=6$: $-9x+16x+20=6\Rightarrow x=-2\Rightarrow y=-3$.",
                         r"Vậy hệ có nghiệm duy nhất $(x;y)=(-2;-3)$."],
               kiem=dict(he=["(3*x+2)*(2*y-3)-6*x*y", "(4*x+5)*(y-5)-4*x*y"], nghiem={"x": -2, "y": -3}))]),

dict(chuong="I. Phương trình và hệ hai phương trình bậc nhất hai ẩn",
     ten="Giải bài toán bằng cách lập hệ phương trình",
     tan_suat=("Giải bài toán bằng cách lập hệ phương trình", None),
     nhan_dang=r"Bài lời văn có \textbf{hai đại lượng chưa biết} và \textbf{hai dữ kiện} ($\;$\emph{nếu \ldots thì \ldots}$\;$). Bối cảnh hay ra nhất: mua bán có khuyến mãi \%, làm chung -- làm riêng, hình chữ nhật đổi kích thước, chuyển động (xuôi -- ngược dòng), kế hoạch -- thực tế.",
     buoc=[r"Gọi ẩn: ghi rõ \emph{đơn vị} và \emph{điều kiện}.",
           r"Biểu diễn các đại lượng còn lại theo ẩn; lập hai phương trình từ hai dữ kiện.",
           r"Giải hệ; đối chiếu điều kiện; trả lời đúng câu hỏi (có đơn vị)."],
     loi=r"Quên điều kiện của ẩn; giảm $20\%$ mà viết $0{,}2x$ thay vì $0{,}8x$; đổi $2$ giờ $45$ phút thành $2{,}45$ giờ.",
     xem_them="docs/quy-trinh-dang-bai/lop9-lap-he-phuong-trinh.md (34 câu, scaffolding, rubric)",
     bai=[
       dict(boi_canh="Mua bán: giá niêm yết, khuyến mãi, giảm giá %",
            nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 3.1 (1,5 điểm, có barem gốc)", ma="gk1-bat-trang-3-1",
            de=r"Bạn Khánh mua $2$ cuốn sách với tổng giá niêm yết là $460$ nghìn đồng. Cuốn thứ nhất được giảm $20\%$, cuốn thứ hai được giảm $25\%$ nên Khánh chỉ phải trả $358$ nghìn đồng. Tính giá niêm yết của mỗi cuốn sách.",
            loi_giai=[r"Gọi giá niêm yết cuốn thứ nhất, cuốn thứ hai lần lượt là $x$, $y$ (nghìn đồng; $0<x,y<460$).",
                      r"Tổng giá niêm yết: $x+y=460$. \hfill (1)",
                      r"Sau giảm giá, cuốn thứ nhất còn $80\%$, cuốn thứ hai còn $75\%$: $0{,}8x+0{,}75y=358$. \hfill (2)",
                      r"Từ (1): $y=460-x$. Thay vào (2): $0{,}8x+0{,}75(460-x)=358\Rightarrow 0{,}05x=13\Rightarrow x=260$ (TMĐK) $\Rightarrow y=200$ (TMĐK).",
                      r"Vậy giá niêm yết cuốn thứ nhất là $260$ nghìn đồng, cuốn thứ hai là $200$ nghìn đồng."],
            kiem=dict(he=["x+y-460", "0.8*x+0.75*y-358"], nghiem={"x": 260, "y": 200})),
       dict(boi_canh="Làm chung – làm riêng (hai đội, hai vòi nước)",
            nguon="THCS Ái Mộ · CK1 2025–2026 · Bài 3.1 (2,0 điểm, có barem gốc)", ma="ck1-ai-mo-3-1",
            de=r"Hai người thợ cùng quét sơn một ngôi nhà thì sau $6$ ngày xong việc. Nếu người thứ nhất làm một mình $5$ ngày rồi nghỉ, người thứ hai làm tiếp $4$ ngày thì cả hai làm được $\dfrac79$ công việc. Hỏi nếu làm riêng thì mỗi người mất bao nhiêu ngày để xong việc?",
            loi_giai=[r"Gọi thời gian người thứ nhất, người thứ hai làm một mình xong việc lần lượt là $x$, $y$ (ngày; $x,y>6$).",
                      r"Mỗi ngày người thứ nhất làm được $\dfrac1x$, người thứ hai làm được $\dfrac1y$ công việc.",
                      r"Cùng làm $6$ ngày xong việc: $\dfrac1x+\dfrac1y=\dfrac16$. \hfill (1)",
                      r"Người thứ nhất làm $5$ ngày, người thứ hai làm $4$ ngày được $\dfrac79$ công việc: $\dfrac5x+\dfrac4y=\dfrac79$. \hfill (2)",
                      r"Đặt $u=\dfrac1x$, $v=\dfrac1y$: $\begin{cases}u+v=\frac16\\5u+4v=\frac79\end{cases}\Rightarrow 5u+4\left(\dfrac16-u\right)=\dfrac79\Rightarrow u=\dfrac19\Rightarrow v=\dfrac1{18}$.",
                      r"$\Rightarrow x=9$, $y=18$ (TMĐK).",
                      r"Vậy làm riêng thì người thứ nhất mất $9$ ngày, người thứ hai mất $18$ ngày."],
            kiem=dict(he=["1/x+1/y-Rational(1,6)", "5/x+4/y-Rational(7,9)"], nghiem={"x": 9, "y": 18})),
       dict(boi_canh="Hình học thực tế: vườn, ruộng, sân, phòng (chu vi – diện tích – kích thước)",
            nguon="THCS Nguyễn Du · GK1 2025–2026 · Bài 2.1 (1,5 điểm, có barem gốc)", ma="gk1-nguyen-du-2-1",
            de=r"Một mảnh đất hình chữ nhật có chiều dài hơn chiều rộng $5$ m. Nếu giảm chiều rộng $4$ m và giảm chiều dài $5$ m thì diện tích mảnh đất giảm $180\ \text{m}^2$. Tính chiều dài và chiều rộng của mảnh đất.",
            loi_giai=[r"Gọi chiều dài, chiều rộng của mảnh đất lần lượt là $x$, $y$ (m; $x>5$, $y>4$).",
                      r"Chiều dài hơn chiều rộng $5$ m: $x-y=5$. \hfill (1)",
                      r"Diện tích giảm $180\ \text{m}^2$: $(x-5)(y-4)=xy-180\Leftrightarrow -4x-5y+20=-180\Leftrightarrow 4x+5y=200$. \hfill (2)",
                      r"Từ (1): $x=y+5$. Thay vào (2): $4(y+5)+5y=200\Rightarrow 9y=180\Rightarrow y=20$ (TMĐK) $\Rightarrow x=25$ (TMĐK).",
                      r"Vậy mảnh đất dài $25$ m, rộng $20$ m."],
            kiem=dict(he=["x-y-5", "(x-5)*(y-4)-(x*y-180)"], nghiem={"x": 25, "y": 20})),
       dict(boi_canh="Chuyển động trên dòng nước (ca nô, xuôi – ngược dòng)",
            nguon="THCS Trưng Vương · CK1 2025–2026 · Bài II.2 (1,5 điểm)", ma="ck1-trung-vuong-II2",
            de=r"Tour \emph{``Chào đón ánh dương''}: du thuyền xuôi dòng $25$ km, ngược dòng $15$ km hết $2$ giờ $45$ phút. Tour \emph{``Vệt nắng hoàng hôn''}: du thuyền xuôi dòng $30$ km, ngược dòng $20$ km hết $3$ giờ $30$ phút. Tính vận tốc riêng của du thuyền và vận tốc dòng nước (biết hai vận tốc này không đổi).",
            loi_giai=[r"Gọi vận tốc xuôi dòng, ngược dòng của du thuyền lần lượt là $x$, $y$ (km/h; $x>y>0$).",
                      r"$2$ giờ $45$ phút $=\dfrac{11}4$ giờ; $3$ giờ $30$ phút $=\dfrac72$ giờ.",
                      r"Ta có hệ $\begin{cases}\dfrac{25}x+\dfrac{15}y=\dfrac{11}4\\[4pt]\dfrac{30}x+\dfrac{20}y=\dfrac72\end{cases}$. Đặt $u=\dfrac1x$, $v=\dfrac1y$: $\begin{cases}100u+60v=11\\90u+60v=\frac{21}2\end{cases}\Rightarrow 10u=\dfrac12\Rightarrow u=\dfrac1{20}\Rightarrow v=\dfrac1{10}$.",
                      r"$\Rightarrow x=20$, $y=10$ (TMĐK).",
                      r"Vận tốc riêng $=\dfrac{x+y}2=15$ (km/h); vận tốc dòng nước $=\dfrac{x-y}2=5$ (km/h).",
                      r"Vậy vận tốc riêng của du thuyền là $15$ km/h, vận tốc dòng nước là $5$ km/h."],
            kiem=dict(he=["25/x+15/y-Rational(11,4)", "30/x+20/y-Rational(7,2)"], nghiem={"x": 20, "y": 10})),
       dict(boi_canh="Năng suất – kế hoạch (dự định/thực tế, vượt mức, cải tiến kĩ thuật)",
            nguon="THCS Trưng Vương · GK1 2025–2026 · Bài 2.2 (1,5 điểm, có barem gốc)", ma="gk1-trung-vuong-2-2",
            de=r"An đọc cuốn tiểu thuyết \emph{``Mưa đỏ''}, mỗi ngày đọc số trang như nhau. Nếu mỗi ngày đọc nhiều hơn dự định $9$ trang thì xong sớm $2$ ngày; nếu mỗi ngày đọc ít hơn dự định $12$ trang thì xong chậm $5$ ngày. Hỏi cuốn sách dày bao nhiêu trang?",
            loi_giai=[r"Gọi số trang An dự định đọc mỗi ngày là $x$ (trang, $x>12$), số ngày dự định là $y$ (ngày, $y>2$). Số trang của sách là $xy$.",
                      r"Đọc thêm $9$ trang/ngày, xong sớm $2$ ngày: $(x+9)(y-2)=xy\Leftrightarrow -2x+9y=18$. \hfill (1)",
                      r"Đọc bớt $12$ trang/ngày, xong chậm $5$ ngày: $(x-12)(y+5)=xy\Leftrightarrow 5x-12y=60$. \hfill (2)",
                      r"$5\cdot(1)+2\cdot(2)$: $21y=210\Rightarrow y=10$ (TMĐK) $\Rightarrow -2x+90=18\Rightarrow x=36$ (TMĐK).",
                      r"Số trang của sách: $36\cdot 10=360$ (trang).",
                      r"Vậy cuốn sách dày $360$ trang."],
            kiem=dict(he=["(x+9)*(y-2)-x*y", "(x-12)*(y+5)-x*y"], nghiem={"x": 36, "y": 10})),
     ]),

# ═══════════════════ CHƯƠNG II ═══════════════════
dict(chuong="II. Phương trình và bất phương trình bậc nhất một ẩn",
     ten="Phương trình tích",
     tan_suat=("Phương trình quy về bậc nhất (tích, chứa ẩn ở mẫu)", "phương trình tích"),
     nhan_dang=r"Vế trái là tích các nhân tử bậc nhất, vế phải bằng $0$ (hoặc đặt nhân tử chung được về dạng đó).",
     buoc=[r"Đưa về dạng $A\cdot B=0$.", r"$A\cdot B=0\Leftrightarrow A=0$ hoặc $B=0$; giải từng phương trình.", r"Kết luận tập nghiệm."],
     loi=r"Chia hai vế cho nhân tử chứa ẩn (làm mất nghiệm).",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 2a (0,5 điểm, có barem gốc)", ma="gk1-bat-trang-2a",
               de=r"Giải phương trình $(2x+1)(5-x)=0$.",
               loi_giai=[r"$(2x+1)(5-x)=0\Leftrightarrow 2x+1=0$ hoặc $5-x=0\Leftrightarrow x=-\dfrac12$ hoặc $x=5$.",
                         r"Vậy phương trình có hai nghiệm $x=-\dfrac12$; $x=5$."],
               kiem=dict(pt="(2*x+1)*(5-x)", nghiem=["-1/2", "5"]))]),

dict(chuong="II. Phương trình và bất phương trình bậc nhất một ẩn",
     ten="Phương trình chứa ẩn ở mẫu",
     tan_suat=("Phương trình quy về bậc nhất (tích, chứa ẩn ở mẫu)", "phương trình chứa ẩn ở mẫu"),
     nhan_dang=r"Ẩn nằm dưới mẫu, thường có mẫu $x^2-a^2=(x-a)(x+a)$. \emph{Dòng tần suất trên do máy đếm bị thấp vì phân số mất khi đọc đề; trong ngân hàng 10 đề GK1 đã gõ lại, \textbf{10/10 đề} có câu dạng này.}",
     buoc=[r"Phân tích mẫu thành nhân tử, tìm ĐKXĐ.", r"Quy đồng, khử mẫu; giải phương trình nhận được.", r"Đối chiếu ĐKXĐ rồi kết luận."],
     loi=r"Quên ĐKXĐ hoặc quên đối chiếu nghiệm với ĐKXĐ; khai triển $(x-1)(x+5)$ sai dấu.",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 2b (0,5 điểm, có barem gốc)", ma="gk1-bat-trang-2b",
               de=r"Giải phương trình $\dfrac{x-1}{x-5}-\dfrac{x}{x+5}=\dfrac{10x-12}{x^2-25}$.",
               loi_giai=[r"ĐKXĐ: $x\neq 5$, $x\neq -5$ (vì $x^2-25=(x-5)(x+5)$).",
                         r"Quy đồng, khử mẫu: $(x-1)(x+5)-x(x-5)=10x-12\Leftrightarrow x^2+4x-5-x^2+5x=10x-12\Leftrightarrow 9x-5=10x-12\Leftrightarrow x=7$ (TMĐK).",
                         r"Vậy phương trình có nghiệm $x=7$."],
               kiem=dict(pt="(x-1)/(x-5)-x/(x+5)-(10*x-12)/(x**2-25)", nghiem=["7"]))]),

dict(chuong="II. Phương trình và bất phương trình bậc nhất một ẩn",
     ten="Giải bất phương trình bậc nhất một ẩn",
     tan_suat=("Giải bất phương trình bậc nhất một ẩn", None),
     nhan_dang=r"Có dấu $<,\ >,\ \le,\ \ge$; hai dạng hay gặp: \emph{khai triển ngoặc} (hạng tử $x^2$ triệt tiêu) và \emph{có mẫu số}.",
     buoc=[r"Khai triển / quy đồng khử mẫu (mẫu là số dương nên giữ chiều).", r"Chuyển vế, thu gọn về $ax<b$.",
           r"Chia hai vế cho $a$: $a<0$ thì \textbf{đổi chiều}. Kết luận nghiệm."],
     loi=r"Chia cho số âm mà không đổi chiều; quy đồng nhưng quên nhân số hạng không có mẫu.",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 2d (0,5 điểm, có barem gốc)", ma="gk1-bat-trang-2d",
               de=r"Giải bất phương trình $(x+1)(2x-1)<2x^2-4x-1$.",
               loi_giai=[r"$(x+1)(2x-1)<2x^2-4x-1\Leftrightarrow 2x^2+x-1<2x^2-4x-1\Leftrightarrow 5x<0\Leftrightarrow x<0$.",
                         r"Vậy nghiệm của bất phương trình là $x<0$."],
               kiem=dict(bpt="(x+1)*(2*x-1) < 2*x**2-4*x-1", nghiem="x < 0")),
          dict(nguon="THCS Ái Mộ · CK1 2025–2026 · Bài 2.2 (0,5 điểm, có barem gốc)", ma="ck1-ai-mo-2-2",
               de=r"Giải bất phương trình $\dfrac{8-3x}2-x<5$.",
               loi_giai=[r"$\dfrac{8-3x}2-x<5\Leftrightarrow 8-3x-2x<10\Leftrightarrow -5x<2\Leftrightarrow x>-\dfrac25$ (chia cho $-5<0$, đổi chiều).",
                         r"Vậy nghiệm của bất phương trình là $x>-\dfrac25$."],
               kiem=dict(bpt="(8-3*x)/2 - x < 5", nghiem="x > -2/5"))]),

dict(chuong="II. Phương trình và bất phương trình bậc nhất một ẩn",
     ten="So sánh hai biểu thức từ một bất đẳng thức cho trước",
     tan_suat=("Bất đẳng thức, so sánh", None),
     nhan_dang=r"``Cho $a<b$. So sánh \ldots'' — dùng tính chất liên hệ thứ tự với phép cộng, phép nhân.",
     buoc=[r"Nhân hai vế với cùng số: số dương giữ chiều, số âm đổi chiều.", r"Cộng cùng số vào hai vế: giữ chiều."],
     loi=r"Nhân với số âm mà giữ nguyên chiều.",
     bai=[dict(nguon="THCS Nguyễn Bỉnh Khiêm · GK1 2025–2026 · Bài 3.1 (0,5 điểm)", ma="gk1-nbk-3-1",
               de=r"Cho $a<b$. Hãy so sánh $-4a+3$ và $-4b+3$.",
               loi_giai=[r"$a<b\Rightarrow -4a>-4b$ (nhân hai vế với $-4<0$) $\Rightarrow -4a+3>-4b+3$ (cộng $3$ vào hai vế).",
                         r"Vậy $-4a+3>-4b+3$."])]),

dict(chuong="II. Phương trình và bất phương trình bậc nhất một ẩn",
     ten="Toán thực tế lập bất phương trình",
     tan_suat=("Toán thực tế lập bất phương trình", None),
     nhan_dang=r"Câu hỏi có \emph{ít nhất / nhiều nhất / tối thiểu / tối đa}; ẩn thường là số nguyên (số câu, số tuần, số sản phẩm).",
     buoc=[r"Gọi ẩn (đơn vị, điều kiện nguyên).", r"Lập bất phương trình từ ràng buộc ``ít nhất'' ($\ge$) / ``không quá'' ($\le$).",
           r"Giải, rồi chọn giá trị nguyên phù hợp."],
     loi=r"Ra $x\ge 16{,}3$ rồi trả lời $16$ câu (phải làm tròn \emph{lên} theo nghĩa bài).",
     bai=[dict(boi_canh="Điểm thi: trả lời đúng/sai (cộng – trừ điểm), điểm trung bình hệ số",
               nguon="THCS Trưng Vương · CK1 2025–2026 · Bài II.1 (1,5 điểm)", ma="ck1-trung-vuong-II1",
               de=r"Cuộc thi \emph{``Rung chuông vàng''}: mỗi thí sinh trả lời $20$ câu hỏi; mỗi câu đúng được cộng $5$ điểm, mỗi câu sai hoặc không trả lời bị trừ $2$ điểm. Thí sinh đạt ít nhất $74$ điểm thì được vào vòng trường. Hỏi thí sinh cần trả lời đúng tối thiểu bao nhiêu câu?",
               loi_giai=[r"Gọi số câu trả lời đúng là $x$ (câu; $x\in\mathbb N$, $x\le 20$) $\Rightarrow$ số câu sai hoặc không trả lời là $20-x$.",
                         r"Số điểm đạt được: $5x-2(20-x)=7x-40$.",
                         r"Đạt ít nhất $74$ điểm: $7x-40\ge 74\Leftrightarrow x\ge\dfrac{114}7\approx 16{,}3$.",
                         r"$x$ là số tự nhiên nhỏ nhất thoả mãn $\Rightarrow x=17$.",
                         r"Vậy thí sinh cần trả lời đúng tối thiểu $17$ câu."])]),

# ═══════════════════ CHƯƠNG III ═══════════════════
dict(chuong="III. Căn bậc hai và căn bậc ba",
     ten="Tính giá trị biểu thức số chứa căn",
     tan_suat=("Căn bậc hai, căn bậc ba: tính, điều kiện xác định", "tính, rút gọn biểu thức số có căn"),
     nhan_dang=r"Biểu thức chỉ có số dưới dấu căn: đưa thừa số ra ngoài dấu căn để làm xuất hiện căn đồng dạng.",
     buoc=[r"Phân tích số dưới căn thành tích có số chính phương: $\sqrt{48}=\sqrt{16\cdot 3}=4\sqrt3$.", r"Cộng/trừ các căn đồng dạng."],
     loi=r"Viết $\sqrt{a+b}=\sqrt a+\sqrt b$.",
     bai=[dict(nguon="THCS Cầu Diễn · CK1 2025–2026 · Bài 1a (0,75 điểm)", ma="ck1-cau-dien-1a",
               de=r"Thực hiện phép tính $2\sqrt{48}-3\sqrt{75}+\sqrt{27}$.",
               loi_giai=[r"$2\sqrt{48}-3\sqrt{75}+\sqrt{27}=2\cdot 4\sqrt3-3\cdot 5\sqrt3+3\sqrt3=8\sqrt3-15\sqrt3+3\sqrt3=-4\sqrt3$.",
                         r"Vậy giá trị biểu thức là $-4\sqrt3$."],
               kiem=dict(bt="2*sqrt(48)-3*sqrt(75)+sqrt(27)", gia_tri="-4*sqrt(3)"))]),

dict(chuong="III. Căn bậc hai và căn bậc ba",
     ten="Phương trình chứa căn (đưa về căn đồng dạng)",
     tan_suat=("Căn bậc hai, căn bậc ba: tính, điều kiện xác định", "giải phương trình chứa căn"),
     nhan_dang=r"Các căn có biểu thức dưới căn tỉ lệ với nhau: $\sqrt{9x-18}=3\sqrt{x-2}$.",
     buoc=[r"Tìm ĐKXĐ.", r"Đưa các căn về cùng một căn, thu gọn về $\sqrt{A}=m$ ($m\ge0$).", r"Bình phương, giải, đối chiếu ĐKXĐ."],
     loi=r"Bỏ qua ĐKXĐ $x\ge 2$.",
     bai=[dict(nguon="THCS Ngọc Thụy · CK1 2025–2026 · Bài I.2a (0,75 điểm)", ma="ck1-ngoc-thuy-I2.a",
               de=r"Giải phương trình $\sqrt{x-2}+3\sqrt{9x-18}=10$.",
               loi_giai=[r"ĐKXĐ: $x\ge 2$.",
                         r"$\sqrt{9x-18}=\sqrt{9(x-2)}=3\sqrt{x-2}$ $\Rightarrow$ phương trình $\Leftrightarrow\sqrt{x-2}+9\sqrt{x-2}=10\Leftrightarrow\sqrt{x-2}=1\Leftrightarrow x-2=1\Leftrightarrow x=3$ (TMĐK).",
                         r"Vậy phương trình có nghiệm $x=3$."],
               kiem=dict(pt="sqrt(x-2)+3*sqrt(9*x-18)-10", nghiem=["3"]))]),

dict(chuong="III. Căn bậc hai và căn bậc ba",
     ten="Bài rút gọn biểu thức chứa căn (3 ý)",
     tan_suat=("Rút gọn biểu thức chứa căn", None),
     nhan_dang=r"Cho hai biểu thức $A$, $B$ chứa $\sqrt x$, kèm điều kiện $x\ge 0,\ x\ne\ldots$ Khuôn 3 ý: (1) tính giá trị tại $x=$ số; (2) rút gọn / chứng minh; (3) câu phụ — tìm $x$ để $P$ thoả bất phương trình, nhận giá trị nguyên, so sánh, GTLN.",
     buoc=[r"Ý 1: kiểm $x$ thoả ĐK, tính $\sqrt x$, thay vào.",
           r"Ý 2: phân tích mẫu ($x-1=(\sqrt x-1)(\sqrt x+1)$), quy đồng, rút gọn.",
           r"Ý 3: lập bất phương trình theo $\sqrt x$; giải; \textbf{kết hợp ĐK} rồi mới kết luận."],
     loi=r"Ý 3 quên loại $x=1$ (ĐK); nhân chéo bất phương trình mà chưa xét dấu mẫu.",
     bai=[dict(nguon="THCS Chu Văn An · CK1 2025–2026 · Bài I (2,0 điểm)", ma="ck1-chu-van-an-I1 / I2 / I3",
               de=r"Cho hai biểu thức $A=\dfrac{\sqrt x+2}{\sqrt x-1}$ và $B=\dfrac{\sqrt x+2}{\sqrt x+1}-\dfrac2{1-x}$ với $x\ge0$, $x\ne1$.\\ 1) Tính giá trị của $A$ khi $x=4$.\quad 2) Chứng minh $B=\dfrac{\sqrt x}{\sqrt x-1}$.\quad 3) Cho $P=\dfrac BA$. Tìm các giá trị nguyên của $x$ để $P<\dfrac12$.",
               loi_giai=[r"1) $x=4$ (TMĐK) $\Rightarrow\sqrt x=2\Rightarrow A=\dfrac{2+2}{2-1}=4$.",
                         r"2) $B=\dfrac{\sqrt x+2}{\sqrt x+1}+\dfrac2{x-1}=\dfrac{(\sqrt x+2)(\sqrt x-1)+2}{(\sqrt x-1)(\sqrt x+1)}=\dfrac{x+\sqrt x}{(\sqrt x-1)(\sqrt x+1)}=\dfrac{\sqrt x(\sqrt x+1)}{(\sqrt x-1)(\sqrt x+1)}=\dfrac{\sqrt x}{\sqrt x-1}$.",
                         r"3) $P=\dfrac{\sqrt x}{\sqrt x-1}:\dfrac{\sqrt x+2}{\sqrt x-1}=\dfrac{\sqrt x}{\sqrt x+2}$.",
                         r"$P<\dfrac12\Leftrightarrow 2\sqrt x<\sqrt x+2$ (vì $\sqrt x+2>0$) $\Leftrightarrow\sqrt x<2\Leftrightarrow x<4$.",
                         r"Kết hợp $x\ge0$, $x\ne1$, $x\in\mathbb Z$ $\Rightarrow x\in\{0;2;3\}$.",
                         r"Vậy $A=4$ khi $x=4$; $B=\dfrac{\sqrt x}{\sqrt x-1}$; $x\in\{0;2;3\}$."],
               kiem=dict(rut_gon=["(sqrt(x)+2)/(sqrt(x)+1)-2/(1-x)", "sqrt(x)/(sqrt(x)-1)"]))]),

# ═══════════════════ CHƯƠNG IV ═══════════════════
dict(chuong="IV. Hệ thức lượng trong tam giác vuông",
     ten="Giải tam giác vuông",
     tan_suat=("Tỉ số lượng giác của góc nhọn", "tính cạnh, góc (giải tam giác vuông)"),
     nhan_dang=r"Biết hai yếu tố của tam giác vuông (một cạnh + một góc nhọn, hoặc hai cạnh); \emph{giải tam giác} = tìm tất cả cạnh, góc còn lại.",
     buoc=[r"Góc nhọn còn lại $=90^\circ-$ góc đã biết.", r"Cạnh góc vuông $=$ cạnh kia $\times\tan$ góc đối; cạnh huyền $=$ cạnh góc vuông $:\cos$ góc kề.",
           r"Làm tròn đúng yêu cầu đề."],
     loi=r"Dùng nhầm $\sin/\cos$ (góc kề với góc đối); làm tròn giữa chừng.",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 4.2a (0,75 điểm, có barem gốc)", ma="gk1-bat-trang-4-2a",
               de=r"Cho $\triangle ABC$ vuông tại $A$ ($AB<AC$), $AB=6$ cm, $\widehat{ABC}=53^\circ$. Giải tam giác vuông $ABC$ (độ dài làm tròn đến chữ số thập phân thứ hai, góc làm tròn đến độ).",
               loi_giai=[r"Xét $\triangle ABC$ vuông tại $A$: $\widehat{ACB}=90^\circ-53^\circ=37^\circ$.",
                         r"$AC=AB\cdot\tan B=6\cdot\tan 53^\circ\approx 7{,}96$ (cm).",
                         r"$BC=\dfrac{AB}{\cos B}=\dfrac6{\cos 53^\circ}\approx 9{,}97$ (cm).",
                         r"Vậy $\widehat{ACB}=37^\circ$, $AC\approx 7{,}96$ cm, $BC\approx 9{,}97$ cm."],
               kiem=dict(so=[("6*tan(53*pi/180)", 7.96), ("6/cos(53*pi/180)", 9.97)]))]),

dict(chuong="IV. Hệ thức lượng trong tam giác vuông",
     ten="Chứng minh hệ thức có tỉ số lượng giác",
     tan_suat=("Tỉ số lượng giác của góc nhọn", "chứng minh hệ thức lượng giác"),
     nhan_dang=r"Đường cao $AH$ chia tam giác vuông thành các tam giác vuông nhỏ; đề yêu cầu chứng minh đẳng thức có $\sin,\ \cos$.",
     buoc=[r"Chọn tam giác vuông \emph{chứa đúng đoạn cần tính}.", r"Viết đoạn đó theo tỉ số lượng giác của góc nhọn trong tam giác ấy.",
           r"Ghép các đẳng thức lại."],
     loi=r"Dùng tỉ số lượng giác trong tam giác không vuông.",
     xem_them="docs/quy-trinh-dang-bai/lop9-chung-minh-tich-tslg.md (23 câu, kỹ thuật đưa về tam giác đồng dạng)",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 4.2b (0,75 điểm, có barem gốc)", ma="gk1-bat-trang-4-2b",
               de=r"Cho $\triangle ABC$ vuông tại $A$, đường cao $AH$ ($H\in BC$). Chứng minh $BC=AB\cdot\cos\widehat{ABC}+AC\cdot\cos\widehat{ACB}$.",
               loi_giai=[r"$\widehat{B}$, $\widehat{C}$ nhọn $\Rightarrow H$ nằm giữa $B$ và $C$ $\Rightarrow BC=BH+CH$.",
                         r"Xét $\triangle ABH$ vuông tại $H$: $BH=AB\cdot\cos\widehat{ABC}$.",
                         r"Xét $\triangle ACH$ vuông tại $H$: $CH=AC\cdot\cos\widehat{ACB}$.",
                         r"Vậy $BC=AB\cdot\cos\widehat{ABC}+AC\cdot\cos\widehat{ACB}$."])]),

dict(chuong="IV. Hệ thức lượng trong tam giác vuông",
     ten="Ứng dụng thực tế: tính chiều cao, khoảng cách",
     tan_suat=("Ứng dụng thực tế (đo chiều cao, khoảng cách, góc nghiêng)", None),
     nhan_dang=r"Tia nắng, bóng cây, góc nâng, máy bay cất cánh, thang dựa tường: vẽ tam giác vuông, đánh dấu góc đã biết.",
     buoc=[r"Vẽ hình, chỉ rõ tam giác vuông và góc đã biết.", r"Chọn tỉ số lượng giác nối cạnh đã biết với cạnh cần tìm.",
           r"Tính, làm tròn, ghi đơn vị."],
     loi=r"Lấy góc giữa tia nắng và \emph{tháp} thay vì góc với \emph{mặt đất}.",
     bai=[dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 4.1 (1,0 điểm, có barem gốc)", ma="gk1-bat-trang-4-1", hinh=HINH_THAP,
               de=r"Tia nắng mặt trời tạo với mặt đất một góc $34^\circ$, bóng của một toà tháp trên mặt đất dài $8{,}6$ m. Tính chiều cao của toà tháp (làm tròn đến chữ số thập phân thứ nhất).",
               loi_giai=[r"Gọi $AB$ là chiều cao tháp, $AC=8{,}6$ m là bóng tháp; $\triangle ABC$ vuông tại $A$, $\widehat{ACB}=34^\circ$.",
                         r"$AB=AC\cdot\tan C=8{,}6\cdot\tan 34^\circ\approx 5{,}8$ (m).",
                         r"Vậy toà tháp cao khoảng $5{,}8$ m."],
               kiem=dict(so=[("8.6*tan(34*pi/180)", 5.8)])),
          dict(nguon="THCS Bát Tràng · GK1 2025–2026 · Bài 5 (0,5 điểm, câu cuối đề, có barem gốc)", ma="gk1-bat-trang-5", hinh=HINH_NUI,
               de=r"Tại hai điểm $A$, $B$ trên mặt đất cách nhau $1000$ m (thẳng hàng với chân núi $H$) người ta nhìn thấy đỉnh núi $D$ với góc nâng lần lượt là $40^\circ$ và $32^\circ$. Tính chiều cao $DH$ của ngọn núi (làm tròn đến hàng đơn vị).",
               loi_giai=[r"Đặt $DH=h$ (m). Xét $\triangle DHA$ vuông tại $H$: $HA=\dfrac{h}{\tan 40^\circ}$. Xét $\triangle DHB$ vuông tại $H$: $HB=\dfrac{h}{\tan 32^\circ}$.",
                         r"$HB-HA=AB\Rightarrow h\left(\dfrac1{\tan32^\circ}-\dfrac1{\tan40^\circ}\right)=1000\Rightarrow h=\dfrac{1000\cdot\tan40^\circ\cdot\tan32^\circ}{\tan40^\circ-\tan32^\circ}\approx 2447$ (m).",
                         r"Vậy ngọn núi cao khoảng $2447$ m."],
               kiem=dict(so=[("1000*tan(40*pi/180)*tan(32*pi/180)/(tan(40*pi/180)-tan(32*pi/180))", 2447)]))]),

# ═══════════════════ CHƯƠNG V ═══════════════════
dict(chuong="V. Đường tròn",
     ten="Chứng minh bốn điểm cùng thuộc một đường tròn · chứng minh tiếp tuyến",
     tan_suat=("Chứng minh 3–4 điểm cùng thuộc một đường tròn", None),
     nhan_dang=r"Ý a bài hình: tìm \emph{hai góc vuông cùng nhìn một đoạn}. Ý b: chứng minh $d\perp$ bán kính tại điểm thuộc đường tròn.",
     buoc=[r"4 điểm: chỉ ra hai tam giác vuông có chung cạnh huyền $\Rightarrow$ cùng thuộc đường tròn đường kính cạnh huyền đó.",
           r"Tiếp tuyến: chứng minh $\widehat{ODF}=90^\circ$ (thường qua hai tam giác bằng nhau) $\Rightarrow DF\perp OD$ tại $D\in(O)$."],
     loi=r"Dùng điều đề không cho (``đường kính vuông góc dây thì đi qua trung điểm'' — SGK KNTT không có, phải qua tam giác cân).",
     bai=[dict(nguon="THCS Ái Mộ · CK1 2025–2026 · Bài 4.2a, b (2,0 điểm, có barem gốc)", ma="ck1-ai-mo-4-2a / 4-2b", hinh=HINH_AI_MO,
               de=r"Cho $(O;R)$ đường kính $AB$. Lấy $C\in(O)$ sao cho $AC>BC$. Kẻ đường cao $CH$ của $\triangle ABC$ ($H\in AB$), tia $CH$ cắt $(O)$ tại $D$ ($D\ne C$). Tiếp tuyến tại $A$ và tiếp tuyến tại $C$ của $(O)$ cắt nhau tại $M$; $MC$ cắt $AB$ tại $F$.\\ a) Chứng minh bốn điểm $A$, $C$, $M$, $O$ cùng thuộc một đường tròn.\quad b) Chứng minh $DF$ là tiếp tuyến của $(O)$.",
               loi_giai=[r"a) $MA$ là tiếp tuyến tại $A$ $\Rightarrow\widehat{OAM}=90^\circ\Rightarrow A$ thuộc đường tròn đường kính $OM$.",
                         r"$MC$ là tiếp tuyến tại $C$ $\Rightarrow\widehat{OCM}=90^\circ\Rightarrow C$ thuộc đường tròn đường kính $OM$.",
                         r"$\Rightarrow A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính $OM$.",
                         r"b) $\triangle OCD$ có $OC=OD=R$ $\Rightarrow$ cân tại $O$; $OH\perp CD$ $\Rightarrow OH$ là đường cao, đồng thời là trung tuyến $\Rightarrow HC=HD$.",
                         r"$\triangle FHC$ và $\triangle FHD$: $HC=HD$, $\widehat{FHC}=\widehat{FHD}=90^\circ$, $FH$ chung $\Rightarrow\triangle FHC=\triangle FHD$ (c.g.c) $\Rightarrow FC=FD$.",
                         r"$\triangle OCF$ và $\triangle ODF$: $OC=OD$, $FC=FD$, $OF$ chung $\Rightarrow\triangle OCF=\triangle ODF$ (c.c.c) $\Rightarrow\widehat{ODF}=\widehat{OCF}=90^\circ$.",
                         r"$\Rightarrow DF\perp OD$ tại $D\in(O)$.",
                         r"Vậy $A$, $C$, $M$, $O$ cùng thuộc đường tròn đường kính $OM$ và $DF$ là tiếp tuyến của $(O)$."])]),

dict(chuong="V. Đường tròn",
     ten="Diện tích hình quạt, hình tròn trong bài thực tế",
     tan_suat=("Độ dài cung, diện tích hình quạt, hình vành khuyên", "diện tích hình tròn, hình quạt"),
     nhan_dang=r"Con vật buộc dây vào cột, vòi tưới quay, bánh pizza cắt miếng: vùng tạo ra là \emph{hình quạt} bán kính bằng độ dài dây.",
     buoc=[r"Xác định tâm, bán kính, số đo cung $n^\circ$.", r"Dùng công thức gốc: $S_{\text{quạt}}=\dfrac{n}{360}\cdot\pi R^2$ (độ dài cung $=\dfrac{n}{360}\cdot 2\pi R$).",
           r"Trả lời đúng phần đề hỏi (phần ăn được hay phần còn lại)."],
     loi=r"Lấy cả hình tròn thay vì góc phần tư khi cột ở góc vườn.",
     bai=[dict(nguon="THCS Ái Mộ · CK1 2025–2026 · Bài 4.1 (1,0 điểm, có barem gốc)", ma="ck1-ai-mo-4-1", hinh=HINH_BO,
               de=r"Một con bò bị nhốt trong mảnh vườn cỏ hình vuông cạnh $5$ m, buộc bằng sợi dây dài $1{,}5$ m vào một cái cột ở góc vườn. Nếu diện tích cỏ con bò ăn được là nhiều nhất thì diện tích phần cỏ còn lại là bao nhiêu? (Lấy $\pi\approx 3{,}14$.)",
               loi_giai=[r"Phần cỏ bò ăn được nhiều nhất là hình quạt tâm là cột, bán kính $1{,}5$ m, số đo cung $90^\circ$:",
                         r"$S_{\text{quạt}}=\dfrac{90}{360}\cdot\pi\cdot 1{,}5^2=\dfrac{9\pi}{16}\approx 1{,}77\ (\text{m}^2)$.",
                         r"Diện tích vườn: $5^2=25\ (\text{m}^2)$. Phần còn lại: $25-\dfrac{9\pi}{16}\approx 23{,}23\ (\text{m}^2)$.",
                         r"Vậy diện tích phần cỏ còn lại khoảng $23{,}23\ \text{m}^2$."],
               kiem=dict(so=[("25-9*3.14/16", 23.23)]))]),

# ═══════════════════ CHƯƠNG VI ═══════════════════
dict(chuong="VI. Hàm số $y=ax^2$. Phương trình bậc hai một ẩn",
     ten="Hàm số $y=ax^2$: tìm hệ số, vẽ đồ thị",
     tan_suat=("Hàm số y = ax², đồ thị parabol", None),
     nhan_dang=r"Cho điểm thuộc đồ thị để tìm $a$, rồi vẽ parabol.",
     buoc=[r"Thay toạ độ điểm vào $y=ax^2$, tìm $a$.", r"Lập bảng giá trị $5$ điểm $x=-2;-1;0;1;2$.", r"Vẽ parabol đi qua $5$ điểm, đối xứng qua $Oy$."],
     loi=r"Vẽ thành đường gấp khúc; bảng giá trị thiếu điểm $O$.",
     bai=[dict(nguon="Phòng GD\\&ĐT Ba Đình · CK2 2024–2025 · Bài II.1 (1,5 điểm, có barem gốc)", ma="(đề PDF)", hinh=HINH_PARABOL,
               de=r"Trong mặt phẳng toạ độ $Oxy$, cho điểm $M(1;2)$ thuộc đồ thị của hàm số $y=kx^2$. a) Tìm hệ số $k$.\quad b) Vẽ đồ thị của hàm số.",
               loi_giai=[r"a) $M(1;2)$ thuộc đồ thị $\Rightarrow 2=k\cdot 1^2\Rightarrow k=2$.",
                         r"b) Với $k=2$: $y=2x^2$. Bảng giá trị: \begin{tabular}{c|ccccc}$x$&$-2$&$-1$&$0$&$1$&$2$\\\hline $y=2x^2$&$8$&$2$&$0$&$2$&$8$\end{tabular}",
                         r"Đồ thị là parabol đi qua $5$ điểm $(-2;8)$, $(-1;2)$, $(0;0)$, $(1;2)$, $(2;8)$ (hình bên).",
                         r"Vậy $k=2$."])]),

dict(chuong="VI. Hàm số $y=ax^2$. Phương trình bậc hai một ẩn",
     ten="Giải phương trình bậc hai bằng công thức nghiệm",
     tan_suat=("Giải phương trình bậc hai", "giải PT bậc hai (công thức nghiệm, nhẩm nghiệm)"),
     nhan_dang=r"$ax^2+bx+c=0$ ($a\ne0$); $b$ chẵn thì dùng công thức nghiệm thu gọn với $b'=\dfrac b2$.",
     buoc=[r"Xác định $a$, $b$ (hoặc $b'$), $c$.", r"Tính $\Delta$ (hoặc $\Delta'$), xét dấu.", r"Viết nghiệm theo công thức."],
     loi=r"Sai dấu khi tính $\Delta'=b'^2-ac$ với $c<0$.",
     bai=[dict(nguon="Phòng GD\\&ĐT Ba Đình · CK2 2024–2025 · Bài II.2 (0,75 điểm, có barem gốc)", ma="(đề PDF)",
               de=r"Sử dụng công thức nghiệm để giải phương trình $x^2-6x-14=0$.",
               loi_giai=[r"$a=1$, $b'=-3$, $c=-14$; $\Delta'=(-3)^2-1\cdot(-14)=23>0$.",
                         r"$\Rightarrow$ phương trình có hai nghiệm phân biệt $x_1=3+\sqrt{23}$; $x_2=3-\sqrt{23}$.",
                         r"Vậy phương trình có hai nghiệm $x=3\pm\sqrt{23}$."],
               kiem=dict(pt="x**2-6*x-14", nghiem=["3+sqrt(23)", "3-sqrt(23)"]))]),

dict(chuong="VI. Hàm số $y=ax^2$. Phương trình bậc hai một ẩn",
     ten="Định lí Viète: tính biểu thức của hai nghiệm",
     tan_suat=("Định lí Viète", "không giải PT, tính biểu thức của hai nghiệm"),
     nhan_dang=r"``Không giải phương trình, tính \ldots'' — biểu thức đối xứng của $x_1$, $x_2$.",
     buoc=[r"Chứng tỏ phương trình có hai nghiệm ($\Delta>0$ hoặc $ac<0$).", r"Viết $S=x_1+x_2=-\dfrac ba$, $P=x_1x_2=\dfrac ca$.",
           r"Biến đổi biểu thức về $S$ và $P$: $x_1^2+x_2^2=S^2-2P$, $x_1^3+x_2^3=S^3-3PS$."],
     loi=r"Không kiểm tra phương trình có nghiệm trước khi dùng Viète.",
     bai=[dict(nguon="Phòng GD\\&ĐT Ba Đình · CK2 2024–2025 · Bài II.3 (0,75 điểm, có barem gốc)", ma="(đề PDF)",
               de=r"Gọi $x_1$, $x_2$ là hai nghiệm của phương trình $2x^2-x-5=0$. Không giải phương trình, hãy tính giá trị biểu thức $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}$.",
               loi_giai=[r"$ac=2\cdot(-5)<0$ $\Rightarrow$ phương trình có hai nghiệm phân biệt trái dấu (khác $0$).",
                         r"Theo định lí Viète: $x_1+x_2=\dfrac12$; $x_1x_2=-\dfrac52$.",
                         r"$\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}=\dfrac{x_1^2+x_2^2}{x_1x_2}=\dfrac{(x_1+x_2)^2-2x_1x_2}{x_1x_2}=\dfrac{\frac14+5}{-\frac52}=-\dfrac{21}{10}$.",
                         r"Vậy $\dfrac{x_1}{x_2}+\dfrac{x_2}{x_1}=-\dfrac{21}{10}$."],
               kiem=dict(viete=dict(pt="2*x**2-x-5", bt="x1/x2+x2/x1", gia_tri="-21/10")))]),

dict(chuong="VI. Hàm số $y=ax^2$. Phương trình bậc hai một ẩn",
     ten="Giải bài toán bằng cách lập phương trình bậc hai",
     tan_suat=("Giải bài toán bằng cách lập phương trình (bậc nhất ở kỳ I, bậc hai ở kỳ II)", None), chi_ky=["GK2", "CK2"],
     nhan_dang=r"Một ẩn, hai đại lượng nằm ở \emph{mẫu} (thời gian $=\dfrac{\text{quãng đường}}{\text{vận tốc}}$, mỗi xe chở $=\dfrac{\text{tổng}}{\text{số xe}}$) $\Rightarrow$ khử mẫu ra phương trình bậc hai.",
     buoc=[r"Gọi ẩn, điều kiện.", r"Lập phương trình chứa ẩn ở mẫu từ dữ kiện ``hơn / kém''.", r"Đưa về $ax^2+bx+c=0$, giải, loại nghiệm không thoả ĐK."],
     loi=r"Trừ ngược hai thời gian (ra phương trình vô nghiệm); quên loại nghiệm âm.",
     bai=[dict(boi_canh="Bài toán hai loại (xe lớn/nhỏ, vé loại I/II, hai loại hàng)",
               nguon="Thi thử vào 10 lần 4, Phòng GD\\&ĐT Chương Mỹ · 2025–2026 · Bài III.2 (1,0 điểm)", ma="v10-chuong-my-4-III2",
               de=r"Để chở hết $60$ tấn hàng, một đội xe dự định dùng một số xe cùng loại. Trước khi khởi hành có hai xe được điều đi làm việc khác, vì vậy mỗi xe còn lại phải chở nhiều hơn dự định $1$ tấn hàng. Hỏi lúc đầu đội dự định dùng bao nhiêu xe?",
               loi_giai=[r"Gọi số xe dự định là $x$ (xe; $x\in\mathbb N$, $x>2$). Mỗi xe dự định chở $\dfrac{60}x$ tấn; thực tế mỗi xe chở $\dfrac{60}{x-2}$ tấn.",
                         r"$\dfrac{60}{x-2}-\dfrac{60}x=1\Rightarrow 60x-60(x-2)=x(x-2)\Rightarrow x^2-2x-120=0$.",
                         r"$\Delta'=1+120=121\Rightarrow x_1=1+11=12$ (TMĐK); $x_2=1-11=-10$ (loại).",
                         r"Vậy lúc đầu đội dự định dùng $12$ xe."],
               kiem=dict(pt="60/(x-2)-60/x-1", nghiem=["12", "-10"])),
          dict(boi_canh="Chuyển động: vận tốc – quãng đường – thời gian",
               nguon="Thi thử vào 10 lần 5, Phòng GD\\&ĐT Chương Mỹ · 2025–2026 · Bài III.1 (1,0 điểm)", ma="v10-chuong-my-5-III1",
               de=r"Bố chở Nam bằng xe máy, các bạn đi ô tô, cùng đi quãng đường $50$ km đến khu du lịch. Để đến nơi cùng lúc, bố Nam phải xuất phát trước $25$ phút. Tính vận tốc mỗi xe, biết vận tốc ô tô lớn hơn vận tốc xe máy $20$ km/h.",
               loi_giai=[r"Gọi vận tốc xe máy là $x$ (km/h; $x>0$) $\Rightarrow$ vận tốc ô tô là $x+20$ (km/h).",
                         r"Thời gian xe máy đi: $\dfrac{50}x$ giờ; ô tô: $\dfrac{50}{x+20}$ giờ; $25$ phút $=\dfrac5{12}$ giờ.",
                         r"$\dfrac{50}x-\dfrac{50}{x+20}=\dfrac5{12}\Rightarrow 600(x+20)-600x=5x(x+20)\Rightarrow x^2+20x-2400=0$.",
                         r"$\Delta'=100+2400=2500\Rightarrow x_1=-10+50=40$ (TMĐK); $x_2=-10-50=-60$ (loại).",
                         r"Vậy vận tốc xe máy là $40$ km/h, vận tốc ô tô là $60$ km/h."],
               kiem=dict(pt="50/x-50/(x+20)-Rational(5,12)", nghiem=["40", "-60"]))]),

# ═══════════════════ CHƯƠNG VII ═══════════════════
dict(chuong="VII. Tần số và tần số tương đối",
     ten="Lập bảng tần số ghép nhóm và tần số tương đối",
     tan_suat=("Bảng tần số, tần số tương đối, biểu đồ", "bảng / biểu đồ tần số ghép nhóm"),
     nhan_dang=r"Cho mẫu số liệu và các nhóm $[a;b)$; lập bảng hai dòng (tần số) hoặc ba dòng (thêm tần số tương đối).",
     buoc=[r"Đếm số giá trị rơi vào từng nhóm (\emph{chú ý nửa khoảng} $[a;b)$: lấy $a$, không lấy $b$).", r"Kiểm tổng tần số $=$ cỡ mẫu.",
           r"Tần số tương đối $=\dfrac{\text{tần số}}{\text{cỡ mẫu}}\cdot 100\%$."],
     loi=r"Đếm giá trị $6{,}5$ vào nhóm $[5;6{,}5)$; tổng tần số tương đối không bằng $100\%$.",
     bai=[dict(nguon="Phòng GD\\&ĐT Ba Đình · CK2 2024–2025 · Bài I.1 (có barem gốc)", ma="(đề PDF)",
               de=r"Bảng dưới đây ghi lại điểm kiểm tra học kì I môn Toán của lớp 9A:\par\begin{center}\small\begin{tabular}{|*{10}{c|}}\hline $8{,}5$&$8$&$8$&$7{,}5$&$9$&$8{,}5$&$7$&$9$&$8$&$8$\\\hline $6{,}5$&$9{,}3$&$8{,}5$&$8{,}5$&$6$&$9$&$7{,}5$&$8{,}5$&$8{,}5$&$8$\\\hline $8$&$6$&$9{,}3$&$6{,}5$&$8$&$5{,}5$&$5$&$8$&$8$&$8{,}5$\\\hline $8{,}5$&$7{,}5$&$8{,}5$&$7{,}5$&$8$&$8{,}5$&$9$&$8$&$8{,}5$&$9$\\\hline\end{tabular}\end{center}Hãy lập bảng tần số ghép nhóm và tần số tương đối ghép nhóm cho mẫu số liệu trên với các nhóm $[5;6{,}5)$, $[6{,}5;8)$, $[8;9{,}5)$.",
               loi_giai=[r"Đếm theo từng nhóm: $[5;6{,}5)$ có $4$ giá trị ($5;\ 5{,}5;\ 6;\ 6$); $[6{,}5;8)$ có $7$ giá trị; $[8;9{,}5)$ có $29$ giá trị. Tổng $4+7+29=40$ đúng cỡ mẫu.",
                         r"\begin{tabular}{l|ccc}Nhóm&$[5;6{,}5)$&$[6{,}5;8)$&$[8;9{,}5)$\\\hline Tần số $n$&$4$&$7$&$29$\\ Tần số tương đối $f$&$10\%$&$17{,}5\%$&$72{,}5\%$\end{tabular}",
                         r"Vậy bảng tần số và tần số tương đối ghép nhóm như trên."],
               kiem=dict(tan_so=dict(du_lieu=[8.5,8,8,7.5,9,8.5,7,9,8,8,6.5,9.3,8.5,8.5,6,9,7.5,8.5,8.5,8,8,6,9.3,6.5,8,5.5,5,8,8,8.5,8.5,7.5,8.5,7.5,8,8.5,9,8,8.5,9],
                                         nhom=[[5,6.5],[6.5,8],[8,9.5]], dap=[4,7,29])))]),

# ═══════════════════ CHƯƠNG VIII ═══════════════════
dict(chuong="VIII. Xác suất của biến cố",
     ten="Xác suất của biến cố: một hành động (rút thẻ, lấy bi, gieo xúc xắc)",
     tan_suat=("Phép thử, không gian mẫu, xác suất của biến cố", "một hành động: xúc xắc, rút thẻ, lấy bóng"),
     nhan_dang=r"Một lần rút/lấy/gieo; các kết quả \emph{đồng khả năng}.",
     buoc=[r"Mô tả không gian mẫu $\Omega$, đếm $n(\Omega)$.", r"Liệt kê các kết quả thuận lợi cho biến cố, đếm.", r"$P=\dfrac{\text{số kết quả thuận lợi}}{n(\Omega)}$."],
     loi=r"Không ghi ``các kết quả đồng khả năng''; liệt kê thiếu kết quả thuận lợi.",
     bai=[dict(nguon="THCS Chu Văn An (Tây Hồ) · CK2 2024–2025 · Bài I.2 (0,5 điểm)", ma="ck2-chu-van-an-I2",
               de=r"Một hộp có $20$ viên bi cùng kích thước, khối lượng, ghi các số $1;2;\ldots;20$ (hai viên khác nhau ghi hai số khác nhau). Lấy ngẫu nhiên một viên bi. Tính xác suất của biến cố $A$: ``Số trên viên bi chia $6$ dư $2$''.",
               loi_giai=[r"$\Omega=\{1;2;\ldots;20\}$, $n(\Omega)=20$; các kết quả đồng khả năng.",
                         r"Các kết quả thuận lợi cho $A$: $2;\ 8;\ 14;\ 20$ $\Rightarrow$ có $4$ kết quả.",
                         r"$P(A)=\dfrac4{20}=\dfrac15$.",
                         r"Vậy $P(A)=\dfrac15$."],
               kiem=dict(dem=dict(tap="range(1,21)", dk="k%6==2", dap=4)))]),

dict(chuong="VIII. Xác suất của biến cố",
     ten="Xác suất của biến cố: chọn hai đối tượng / hai lần",
     tan_suat=("Phép thử, không gian mẫu, xác suất của biến cố", "hai hành động / chọn hai đối tượng"),
     nhan_dang=r"Lấy \emph{đồng thời} hai vật, chọn hai bạn, gieo hai lần: kết quả là \emph{cặp} — phải liệt kê đủ các cặp.",
     buoc=[r"Đặt tên từng đối tượng ($X_1,X_2,\ldots$) để liệt kê không trùng.", r"Liệt kê không gian mẫu (các cặp), đếm.", r"Đếm cặp thuận lợi, tính xác suất."],
     loi=r"Coi ba viên bi xanh là ``một kết quả'' (không đặt tên) nên đếm thiếu.",
     bai=[dict(nguon="THCS Nguyễn Du · CK2 2025–2026 · Bài III.2 (0,5 điểm)", ma="ck2-nguyen-du-III2",
               de=r"Một hộp đựng ba viên bi xanh và một viên bi đỏ (cùng kích thước, khối lượng). Lấy ngẫu nhiên đồng thời hai viên bi. Tính xác suất của biến cố $A$: ``Lấy được một viên bi xanh và một viên bi đỏ''.",
               loi_giai=[r"Gọi ba bi xanh là $X_1$, $X_2$, $X_3$, bi đỏ là $D$.",
                         r"$\Omega=\{X_1X_2;\ X_1X_3;\ X_2X_3;\ X_1D;\ X_2D;\ X_3D\}$, $n(\Omega)=6$; các kết quả đồng khả năng.",
                         r"Kết quả thuận lợi cho $A$: $X_1D;\ X_2D;\ X_3D$ $\Rightarrow$ có $3$ kết quả $\Rightarrow P(A)=\dfrac36=\dfrac12$.",
                         r"Vậy $P(A)=\dfrac12$."])]),

# ═══════════════════ CHƯƠNG IX ═══════════════════
dict(chuong="IX. Đường tròn ngoại tiếp và đường tròn nội tiếp",
     ten="Chứng minh tứ giác nội tiếp (khuôn ý a đề vào 10)",
     tan_suat=("Góc nội tiếp, tứ giác nội tiếp, đường tròn ngoại/nội tiếp", "chứng minh tứ giác nội tiếp / 4 điểm cùng thuộc đường tròn"),
     nhan_dang=r"Có hai đường vuông góc (đường cao, hình chiếu, tiếp tuyến) tạo \emph{hai góc vuông cùng nhìn một đoạn}.",
     buoc=[r"Chỉ ra góc vuông thứ nhất $\Rightarrow$ điểm thuộc đường tròn đường kính $XY$.", r"Chỉ ra góc vuông thứ hai cùng nhìn $XY$.",
           r"Kết luận bốn điểm cùng thuộc đường tròn đường kính $XY$."],
     loi=r"Nêu ``hai góc vuông'' nhưng không cùng nhìn một đoạn.",
     bai=[dict(nguon="Đề tuyển sinh vào 10 Hà Nội năm học 2026–2027 (Sở GD\\&ĐT) · Câu IV.2a (1,0 điểm)", ma="v10-so-2026-IV2a", hinh=HINH_SO_2026,
               de=r"Cho $\triangle ABC$ vuông tại $A$ ($AB<AC$) nội tiếp đường tròn tâm $O$, đường kính $BC$. Lấy điểm $H$ thuộc đoạn $AB$ sao cho $HB>HA$ ($H\ne A$). Đường thẳng qua $H$ vuông góc với $BC$ tại $D$ và cắt đường thẳng $AC$ tại $E$. Chứng minh bốn điểm $A$, $H$, $D$, $C$ cùng thuộc một đường tròn.",
               loi_giai=[r"$\triangle ABC$ vuông tại $A$ $\Rightarrow\widehat{HAC}=90^\circ\Rightarrow A$ thuộc đường tròn đường kính $HC$.",
                         r"$HD\perp BC$ $\Rightarrow\widehat{HDC}=90^\circ\Rightarrow D$ thuộc đường tròn đường kính $HC$.",
                         r"Vậy bốn điểm $A$, $H$, $D$, $C$ cùng thuộc đường tròn đường kính $HC$."])]),

# ═══════════════════ CHƯƠNG X ═══════════════════
dict(chuong="X. Một số hình khối trong thực tiễn",
     ten="Hình trụ: diện tích xung quanh, thể tích trong bài thực tế",
     tan_suat=("Hình trụ, hình nón, hình cầu", "hình trụ"),
     nhan_dang=r"Thùng, xô, bể, cốc, ống: hình trụ bán kính $R$, chiều cao $h$.",
     buoc=[r"$S_{xq}=2\pi Rh$; $V=\pi R^2h$ (đường kính thì chia đôi lấy $R$).", r"Phần nước dùng / dâng là một hình trụ cùng đáy, chiều cao bằng độ chênh mực nước.",
           r"Đổi đơn vị ($1$ lít $=1\ \text{dm}^3=1000\ \text{cm}^3$)."],
     loi=r"Lấy đường kính làm bán kính; quên đổi $\text{cm}^3$ sang lít.",
     bai=[dict(nguon="Đề tuyển sinh vào 10 Hà Nội năm học 2025–2026 (Sở GD\\&ĐT) · Câu IV.1 (1,0 điểm)", ma="v10-so-2025-IV1a / IV1b",
               de=r"Một thùng đựng nước dạng hình trụ có bán kính đáy $50$ cm, chiều cao $150$ cm, đặt thẳng đứng trên sàn. a) Tính diện tích xung quanh của thùng.\quad b) Sau một thời gian sử dụng, mực nước trong thùng thấp hơn $40$ cm so với ban đầu. Tính thể tích nước đã dùng. (Lấy $\pi\approx3{,}14$, coi chiều dày thùng không đáng kể.)",
               loi_giai=[r"a) $S_{xq}=2\pi Rh\approx 2\cdot 3{,}14\cdot 50\cdot 150=47\,100\ (\text{cm}^2)$.",
                         r"b) Phần nước đã dùng là hình trụ bán kính $50$ cm, cao $40$ cm: $V=\pi R^2h\approx 3{,}14\cdot 50^2\cdot 40=314\,000\ (\text{cm}^3)=314$ (lít).",
                         r"Vậy diện tích xung quanh là $47\,100\ \text{cm}^2$; đã dùng $314$ lít nước."],
               kiem=dict(so=[("2*3.14*50*150", 47100), ("3.14*50**2*40/1000", 314)]))]),

dict(chuong="X. Một số hình khối trong thực tiễn",
     ten="Hình cầu: diện tích mặt cầu, thể tích",
     tan_suat=("Hình trụ, hình nón, hình cầu", "hình cầu"),
     nhan_dang=r"Quả bóng, viên bi, quả nặng: hình cầu bán kính $R$.",
     buoc=[r"$S=4\pi R^2$; $V=\dfrac43\pi R^3$.", r"Bài ghép: vật hình cầu thả vào cốc trụ $\Rightarrow$ thể tích nước dâng/tràn bằng thể tích vật."],
     loi=r"Dùng $\pi R^2$ cho diện tích mặt cầu.",
     bai=[dict(nguon="THCS Trưng Vương · CK2 2025–2026 · Bài IV.1 (1,0 điểm)", ma="ck2-trung-vuong-IV1a / IV1b",
               de=r"Quả bóng đá hình cầu đường kính $22$ cm. a) Tính diện tích da để làm quả bóng (bỏ qua hao hụt).\quad b) Máy bơm mỗi giây đưa được $0{,}5$ lít không khí vào bóng. Hỏi sau bao nhiêu giây quả bóng (đang xẹp hoàn toàn) đầy hơi? (Lấy $\pi\approx3{,}14$, làm tròn đến chữ số thập phân thứ nhất.)",
               loi_giai=[r"a) $R=22:2=11$ (cm); $S=4\pi R^2\approx 4\cdot 3{,}14\cdot 11^2=1519{,}76\ (\text{cm}^2)$.",
                         r"b) $V=\dfrac43\pi R^3\approx\dfrac43\cdot 3{,}14\cdot 11^3\approx 5572{,}45\ (\text{cm}^3)\approx 5{,}57$ (lít).",
                         r"Thời gian bơm: $5{,}57:0{,}5\approx 11{,}1$ (giây).",
                         r"Vậy cần khoảng $1519{,}76\ \text{cm}^2$ da; bơm khoảng $11{,}1$ giây thì bóng đầy hơi."],
               kiem=dict(so=[("4*3.14*11**2", 1519.76), ("4/3*3.14*11**3/1000/0.5", 11.1)]))]),

# ═══════════════════ CÂU CUỐI ĐỀ ═══════════════════
dict(chuong="Câu cuối đề (0,5 điểm)",
     ten="Bài toán tối ưu thực tế (doanh thu, lợi nhuận, diện tích lớn nhất)",
     tan_suat=("Giá trị lớn nhất / nhỏ nhất, bài toán tối ưu thực tế", "tối ưu trong bài thực tế (lợi nhuận, diện tích, chi phí…)"),
     nhan_dang=r"``Cứ tăng/giảm \ldots thì \ldots'', hỏi để doanh thu/lợi nhuận \emph{cao nhất}. Khuôn lặp ở phần lớn đề kỳ I.",
     buoc=[r"Gọi ẩn là \emph{số lần} tăng/giảm (điều kiện).", r"Lập biểu thức đại lượng cần tối ưu (tích hai thừa số).",
           r"Đưa về $m-(x-a)^2$ bằng hằng đẳng thức $\Rightarrow$ GTLN là $m$ khi $x=a$ (\textbf{không} dùng công thức đỉnh parabol)."],
     loi=r"Dùng $x=-\dfrac b{2a}$ (kiến thức lớp 10); quên trả lời giá trị thực tế (giá thuê) mà chỉ trả lời $x$.",
     xem_them="docs/quy-trinh-dang-bai/lop9-toi-uu-loi-nhuan.md (17 câu)",
     bai=[dict(nguon="THCS Nguyễn Du · GK1 2025–2026 · Bài 5 (0,5 điểm, có barem gốc)", ma="gk1-nguyen-du-5",
               de=r"Một công ty có $40$ căn hộ. Nếu giá thuê mỗi căn là $5$ triệu đồng/tháng thì cho thuê kín. Cứ mỗi lần tăng giá thêm $500$ nghìn đồng/căn thì có thêm $2$ căn bị bỏ trống. Hỏi công ty cho thuê mỗi căn bao nhiêu để doanh thu cao nhất?",
               loi_giai=[r"Gọi số lần tăng giá là $x$ ($x\in\mathbb N$, $x<20$). Giá thuê mỗi căn: $5+0{,}5x$ (triệu đồng); số căn được thuê: $40-2x$.",
                         r"Doanh thu: $T=(5+0{,}5x)(40-2x)=-x^2+10x+200=225-(x-5)^2\le 225$.",
                         r"Dấu ``$=$'' xảy ra khi $x=5$ $\Rightarrow$ giá thuê $5+0{,}5\cdot 5=7{,}5$ (triệu đồng).",
                         r"Vậy cho thuê mỗi căn $7{,}5$ triệu đồng/tháng thì doanh thu cao nhất ($225$ triệu đồng)."],
               kiem=dict(toi_uu=dict(bt="(5+0.5*x)*(40-2*x)", x=5, gtln=225)))]),
]
