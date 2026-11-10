# -*- coding: utf-8 -*-
"""
Script dựng file Beamer LaTeX và biên dịch ra PDF cho bài thuyết trình hướng dẫn Giáo viên mới.
Đã căn chỉnh hoàn hảo kích thước từng slide, chống tràn viền (vertical & horizontal).
"""

import subprocess
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

logo_path = (ASSETS_DIR / "logo_mathtech_compact.png").as_posix()
watermark_path = (ASSETS_DIR / "Watermark_Opacity_20.png").as_posix()
fonts_dir_str = FONTS_DIR.as_posix() + "/"

tex_source = r"""\documentclass[aspectratio=169,11pt]{beamer}

\usefonttheme{professionalfonts}
\usepackage{fontspec}
\usepackage{unicode-math}

\def\FONTDIR{""" + fonts_dir_str + r"""}
\setmainfont{BeVietnamPro}[Path=\FONTDIR, Extension=.ttf,
  UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic, FontFace={sb}{n}{*-SemiBold} ]
\setsansfont{BeVietnamPro}[Path=\FONTDIR, Extension=.ttf,
  UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic ]
\setmathfont{STIXTwoMath-Regular.otf}[Path=\FONTDIR]

\usepackage{tikz}
\usetikzlibrary{calc,positioning,arrows.meta,shapes.geometric}
\usepackage{adjustbox}
\usepackage[most]{tcolorbox}
\usepackage{colortbl}
\usepackage{hyperref}

% Màu sắc nhận diện
\usepackage{xcolor}
\definecolor{brand}{HTML}{1E3A8A}      % Xanh Navy chủ đạo
\definecolor{accent}{HTML}{D97706}     % Vàng Cam nhấn
\definecolor{ink}{HTML}{1E293B}        % Chữ đậm
\definecolor{neutral}{HTML}{F8FAFC}    % Nền phụ
\definecolor{rule}{HTML}{E2E8F0}       % Kẻ ngang
\definecolor{muted}{HTML}{64748B}      % Chữ mờ
\definecolor{info}{HTML}{2563EB}       % Link xanh
\definecolor{success}{HTML}{15803D}    % Xanh lá
\definecolor{successbg}{HTML}{DCFCE7}  % Nền xanh lá
\definecolor{cardbg}{HTML}{F1F5F9}     % Nền card
\definecolor{danger}{HTML}{DC2626}     % Đỏ cảnh báo

\hypersetup{
  colorlinks=true,
  urlcolor=info,
  linkcolor=brand
}

\usetheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{normal text}{fg=ink}
\setbeamercolor{structure}{fg=brand}
\setbeamercolor{frametitle}{fg=brand}
\setbeamerfont{frametitle}{series=\bfseries, size=\large}
\setbeamerfont{normal text}{size=\small}

% Watermark
\newif\ifwatermark\watermarktrue
\setbeamertemplate{background}{%
  \ifwatermark
    \begin{tikzpicture}[remember picture,overlay]
      \node[opacity=0.15] at (current page.center)
        {\includegraphics[width=0.42\paperwidth]{""" + watermark_path + r"""}};
    \end{tikzpicture}%
  \fi}

% Header frametitle gọn gàng, tiết kiệm chiều cao
\setbeamertemplate{frametitle}{%
  \vspace*{4pt}\hspace*{0.1cm}{\usebeamerfont{frametitle}\usebeamercolor[fg]{frametitle}\insertframetitle}\par
  \vspace{1pt}\hspace*{0.1cm}{\color{accent}\rule{36pt}{1.8pt}}\par\vspace{1pt}}

% Footer
\setbeamertemplate{footline}{%
  \leavevmode%
  \hspace*{0.6cm}{\color{rule}\rule{\dimexpr\paperwidth-1.2cm\relax}{0.4pt}}\par\vspace{2pt}%
  \hbox to \paperwidth{%
    \hspace*{0.6cm}%
    \raisebox{-1pt}{\includegraphics[height=9pt]{""" + logo_path + r"""}}%
    \hspace*{6pt}{\scriptsize\color{muted}MathTech Engine • Thầy Trương Đình Thái}%
    \hfill%
    {\scriptsize\color{muted}Slide \insertframenumber{} / \inserttotalframenumber}%
    \hspace*{0.6cm}%
  }%
  \vskip3pt}

% Card styles - tối ưu đệm (padding) để không bao giờ tràn đáy
\tcbset{
  slidecard/.style={
    colback=neutral, colframe=rule, boxrule=0.7pt, arc=3pt,
    left=5pt, right=5pt, top=3pt, bottom=3pt,
    fonttitle=\bfseries\sffamily\footnotesize, coltitle=brand
  },
  accentcard/.style={
    colback=accent!6, colframe=accent, boxrule=0.7pt, arc=3pt,
    left=5pt, right=5pt, top=3pt, bottom=3pt,
    fonttitle=\bfseries\sffamily\footnotesize, coltitle=accent
  },
  successcard/.style={
    colback=successbg, colframe=success, boxrule=0.7pt, arc=3pt,
    left=5pt, right=5pt, top=3pt, bottom=3pt,
    fonttitle=\bfseries\sffamily\footnotesize, coltitle=success
  },
  quotecard/.style={
    colback=white, colframe=brand!40, boxrule=0.6pt, arc=2pt,
    left=4pt, right=4pt, top=3pt, bottom=3pt
  }
}

\begin{document}

% ========================================================
% SLIDE 1: TIÊU ĐỀ
% ========================================================
\watermarkfalse
\begin{frame}[plain]
  \begin{tikzpicture}[remember picture,overlay]
    \fill[color=brand] (current page.north west) rectangle ([xshift=0.35in]current page.south west);
    \fill[color=accent] ([xshift=0.35in]current page.north west) rectangle ([xshift=0.38in]current page.south west);
  \end{tikzpicture}

  \vspace*{0.25in}
  \begin{flushleft}
    \hspace*{0.55in}
    \begin{minipage}{0.85\textwidth}
      \includegraphics[height=28pt]{""" + logo_path + r"""}\par\vspace{12pt}
      {\setlength{\fboxsep}{3pt}\colorbox{brand}{\color{white}\sffamily\bfseries\scriptsize\strut\,CẨM NANG NỘI BỘ GIÁO VIÊN MỚI\,}}\par\vspace{8pt}
      {\bfseries\LARGE\color{brand}HƯỚNG DẪN CÁCH SỬ DỤNG AI\\SOẠN PHIẾU HỌC TẬP}\par\vspace{8pt}
      {\color{accent}\rule{130pt}{2.5pt}}\par\vspace{8pt}
      {\color{muted}\small\sffamily Tư duy phân tầng sư phạm \& Quy trình 5 bước phối hợp cùng Trợ lý AI}\par
      \vspace{14pt}
      {\color{ink}\small\sffamily Người thuyết trình: \textbf{Trương Đình Thái} • Tổ Học Liệu MathTech}
    \end{minipage}
  \end{flushleft}
  \vfill
\end{frame}
\watermarktrue

% ========================================================
% SLIDE 2: TẢI TOOL, CÀI EXTENSION & MỞ CHAT AI
% ========================================================
\begin{frame}{Khởi Động Nhanh (3 Phút): Tải Tool, Extension \& Mở AI}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=1. Tải Mã Nguồn \& Antigravity]
        \scriptsize
        • \textbf{Codebase MathTech (GitHub):}\\
        \href{https://github.com/icecubesssss/giaoanmathtech}{\textbf{\color{info}github.com/icecubesssss/giaoanmathtech}}\\
        {\color{muted}(Bấm Code $\to$ Download ZIP $\to$ Giải nén)}\\[4pt]
        • \textbf{Ứng dụng AI Antigravity:}\\
        \href{https://antigravity.google/download}{\textbf{\color{info}antigravity.google/download}}
      \end{tcolorbox}
      \vspace{1pt}
      \begin{tcolorbox}[slidecard, title=2. Mở Thư Mục \& Nhắn Kích Hoạt]
        \scriptsize
        Mở Antigravity $\to$ \textbf{Open Folder} trỏ vào thư mục code vừa giải nén $\to$ Mở chat AI và nhắn:
        \vspace{2pt}
        \begin{center}
          \colorbox{white}{\color{accent}\bfseries "Cài đặt môi trường giúp tôi"}
        \end{center}
        {\color{success}\textbf{👉 AI tự cài Python \& thư viện từ A – Z!}}
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[accentcard, title=3. Cài 2 Extension Thiết Yếu (Trong VS Code)]
        \scriptsize
        Mở mục \textbf{Extensions} (\texttt{Ctrl+Shift+X} / \texttt{Cmd+Shift+X}):\\[3pt]
        \textbf{1. Extension Claude (Claude Code):}\\
        Dùng Claude tương tác trực tiếp, chạy lệnh soạn bài và phân dạng cùng AI.\\[5pt]
        \textbf{2. Extension vscode-pdf:}\\
        Mở và xem trực tiếp 3 bản PDF (Handout HS, Guide GV, Slide) ngay trong cửa sổ làm việc mà không cần cài thêm app ngoài.\\[5pt]
        {\color{brand}\textbf{Lợi ích:}} Toàn bộ thao tác chỉ diễn ra trong 1 màn hình!
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 3: CƠ CHẾ HOẠT ĐỘNG
% ========================================================
\begin{frame}{Cơ Chế Hoạt Động: Inputs $\to$ Process $\to$ Outputs}
  \vspace{-3pt}
  \begin{center}
    \begin{tikzpicture}[node distance=0.55cm, auto]
      \node[draw=brand, fill=neutral, rounded corners=3pt, line width=0.8pt, text width=3.3cm, align=center, inner sep=4pt] (in) {
        {\bfseries\color{brand}\small INPUTS}\\[1pt]
        {\tiny (Nguyên liệu thô)}\\[2pt]
        {\tiny • Đề thi thật chính thức Hà Nội\\• SGK, SGV Kết nối tri thức\\• Sách bài tập chọn lọc}
      };
      \node[draw=accent, fill=accent!8, rounded corners=3pt, line width=0.8pt, text width=3.4cm, align=center, inner sep=4pt, right=of in] (pro) {
        {\bfseries\color{accent}\small PROCESS}\\[1pt]
        {\tiny (MathTech Engine + AI)}\\[2pt]
        {\tiny • Giải toán kiểm thử (SymPy)\\• Dựng hình TikZ chính xác\\• Cân đối thời lượng 90' \& dàn trang}
      };
      \node[draw=success, fill=successbg, rounded corners=3pt, line width=0.8pt, text width=3.4cm, align=center, inner sep=4pt, right=of pro] (out) {
        {\bfseries\color{success}\small OUTPUTS}\\[1pt]
        {\tiny (Bộ 3 PDF Song Song)}\\[2pt]
        {\tiny 1. \textbf{Handout HS:} Khung làm bài\\2. \textbf{Guide GV:} Lời giải + Sư phạm\\3. \textbf{Slide 16:9:} Tự ẩn giải tương tác}
      };
      \draw[-{Stealth[length=4pt]}, line width=1pt, draw=brand!70] (in) -- (pro);
      \draw[-{Stealth[length=4pt]}, line width=1pt, draw=accent!70] (pro) -- (out);
    \end{tikzpicture}
  \end{center}
  \vspace{2pt}
  \begin{tcolorbox}[slidecard]
    \scriptsize\centering
    💡 \textbf{Giáo viên chỉ cần tập trung vào sư phạm} — AI tự động giải toán, vẽ hình và xuất trọn bộ PDF!
  \end{tcolorbox}
\end{frame}

% ========================================================
% SLIDE 4: PHÂN TẦNG NĂNG LỰC HỌC SINH
% ========================================================
\begin{frame}{Phân Tầng Năng Lực Học Sinh (A – B – C – X)}
  \vspace{-4pt}
  \begin{center}
    \renewcommand{\arraystretch}{0.92}
    \scriptsize
    \begin{tabular}{|c|p{5.1cm}|p{3.2cm}|p{2.6cm}|}
      \hline
      \rowcolor{brand}\color{white}\bfseries Tầng & \color{white}\bfseries Chân dung học sinh & \color{white}\bfseries Đích điểm số & \color{white}\bfseries Trần bài tập \\
      \hline
      \rowcolor{accent!12}\textbf{\color{accent}C} & \textbf{Nền tảng trung bình – yếu}, hay quên kiến thức cũ & Chắc SGK, kéo điểm kiểm tra lên \textbf{7 – 8 điểm} & \textbf{\color{danger}Trần: VD (CẤM VDC)} \\
      \hline
      \textbf{B} & Trung bình – khá, tiếp thu tốt & Kỳ I: 9,5 – 10đ; Kỳ II: 9 – 9,5đ & Có VDC nhẹ \\
      \hline
      \textbf{A} & Khá – giỏi, tư duy tốt & Điểm tối đa trên trường & VDC dày dặn \\
      \hline
      \textbf{X} & Giỏi xuất sắc, thi Chuyên/CLC & Chinh phục câu cuối đề & VDC chuyên sâu \\
      \hline
    \end{tabular}
  \end{center}
  \vspace{1pt}
  \begin{tcolorbox}[accentcard]
    \scriptsize
    🎯 \textbf{Trọng tâm hiện tại:} Toàn bộ đợt soạn này phục vụ mục tiêu \textbf{LỚP C}. Tuyệt đối không đưa bài VDC vào phiếu để tránh gây quá tải cho học sinh!
  \end{tcolorbox}
\end{frame}

% ========================================================
% SLIDE 5: 4 CẤP ĐỘ CÂU HỎI
% ========================================================
\begin{frame}{4 Cấp Độ Câu Hỏi (NB – TH – VD – VDC)}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=1. NHẬN BIẾT (NB) — 1 Bước]
        \scriptsize
        Áp dụng trực tiếp công thức, định nghĩa:\\
        • \textbf{Lớp 3:} Tính nhẩm: $7 \times 4 = ?$\\
        • \textbf{Lớp 6:} Tính giá trị: $2^3 = ?$
      \end{tcolorbox}
      \vspace{1pt}
      \begin{tcolorbox}[slidecard, title=2. THÔNG HIỂU (TH) — 1–2 Bước]
        \scriptsize
        Áp dụng quy tắc vào bài toán cơ bản:\\
        • \textbf{Lớp 3:} "1 hộp có 8 cái bánh, 3 hộp có mấy cái?"\\
        • \textbf{Lớp 6:} Tính: $A = 2^3 \cdot 5 - 3^2$
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[accentcard, title=3. VẬN DỤNG (VD) — 2–3 Bước]
        \scriptsize
        Bài toán thực tế, liên kết dữ kiện:\\
        • \textbf{Lớp 3:} "Có 35 quả cam chia 5 túi, bán 2 túi, còn mấy?"\\
        • \textbf{Lớp 6:} Tìm số tự nhiên $x$: $2(x - 3)^2 = 32$
      \end{tcolorbox}
      \vspace{1pt}
      \begin{tcolorbox}[colback=danger!4, colframe=danger!80, title=4. VẬN DỤNG CAO (VDC) — $\ge 4$ Bước]
        \scriptsize
        Phân hóa điểm 9,5 – 10 (Cực trị, logic, BĐT):\\
        • \textbf{Lớp 6:} Tìm chữ số tận cùng của tổng lũy thừa.\\
        • \textbf{\color{danger}Lớp C: 0\% VDC (Không đưa vào phiếu).}
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 6: KỸ THUẬT "NB TÁCH CÂU"
% ========================================================
\begin{frame}{Kỹ Thuật "NB Tách Câu" (Giàn Giáo Sư Phạm Lớp C)}
  \begin{tcolorbox}[accentcard]
    \scriptsize\bfseries
    NGUYÊN TẮC VÀNG: Cấm dùng câu NB rời rạc! Mọi câu NB phải là bước đệm kỹ năng trích từ chính bài toán thi thật.
  \end{tcolorbox}
  \vspace{1pt}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[colback=danger!4, colframe=danger!60, title=Cách Ra Đề Cũ (HS Yếu Bỏ Trắng)]
        \scriptsize
        \textbf{Bài toán Thông hiểu [TH]:}\\
        Tính giá trị biểu thức:
        \[ M = 150 - [100 - (3^2 \cdot 5)] \]
        {\tiny \color{muted}(HS yếu nhìn ngoặc vuông và lũy thừa thường hoảng sợ và tính sai thứ tự).}
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[successcard, title=Chuẩn Giàn Giáo MathTech (NB Tách Bước)]
        \scriptsize
        \textbf{Chẻ nhỏ thành 2 bước đệm:}\\[2pt]
        • \textbf{Ý a [NB đệm]:} Tính $3^2$ và $3^2 \cdot 5$.\\
        • \textbf{Ý b [TH]:} Tính $[100 - (3^2 \cdot 5)]$ rồi tính $M$.\\[2pt]
        {\color{success}\textbf{👉 HS tự tin làm được ý đầu, tạo đà làm cả bài!}}
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 7: TỈ LỆ CHUẨN LỚP C: 40 - 40 - 20
% ========================================================
\begin{frame}{Tỉ Lệ Chuẩn Vàng Lớp C: 40\% – 40\% – 20\%}
  \begin{columns}[T]
    \begin{column}{0.31\textwidth}
      \begin{tcolorbox}[slidecard]
        \centering
        {\large\bfseries\color{brand} 40\%}\\[1pt]
        {\bfseries\color{brand}\scriptsize NHẬN BIẾT}\\[1pt]
        {\tiny Xây chắc nền móng, củng cố kỹ năng tiên quyết}
      \end{tcolorbox}
    \end{column}
    \begin{column}{0.31\textwidth}
      \begin{tcolorbox}[accentcard]
        \centering
        {\large\bfseries\color{accent} 40\%}\\[1pt]
        {\bfseries\color{accent}\scriptsize THÔNG HIỂU}\\[1pt]
        {\tiny Thành thạo dạng toán trọng tâm đề thi}
      \end{tcolorbox}
    \end{column}
    \begin{column}{0.31\textwidth}
      \begin{tcolorbox}[successcard]
        \centering
        {\large\bfseries\color{success} 20\%}\\[1pt]
        {\bfseries\color{success}\scriptsize VẬN DỤNG}\\[1pt]
        {\tiny Bài toán thực tế vừa sức, không đánh đố (0\% VDC)}
      \end{tcolorbox}
    \end{column}
  \end{columns}
  \vspace{3pt}
  \begin{tcolorbox}[slidecard, title=Phân Bổ Thời Lượng Trong Ca Học Chuẩn 90 Phút]
    \scriptsize
    • \textbf{Khối 3:} GV giảng \& làm mẫu: 30' $\to$ HS luyện tại lớp: 45' $\to$ BTVN: 60' (8–10 NB + 4–5 TH + 1–2 VD).\\[2pt]
    • \textbf{Khối 6:} GV giảng: 25' $\to$ HS luyện tại lớp: 55' (nghỉ 10') $\to$ BTVN: 40' (10–12 NB đệm + 4 TH + 1–2 VD).
  \end{tcolorbox}
\end{frame}

% ========================================================
% SLIDE 8: CẤU TRÚC 4 CHẶNG TRÊN PHIẾU HỌC TẬP
% ========================================================
\begin{frame}{Cấu Trúc 4 Chặng Sư Phạm Của 1 Phiếu Học Tập}
  \begin{columns}[T]
    \begin{column}{0.24\textwidth}
      \begin{tcolorbox}[slidecard]
        \centering
        {\bfseries\color{brand}\scriptsize 1. NỀN TẢNG}\\[2pt]
        {\tiny Ôn nhanh kỹ năng lớp dưới hoặc bài trước}
      \end{tcolorbox}
    \end{column}
    \begin{column}{0.24\textwidth}
      \begin{tcolorbox}[slidecard]
        \centering
        {\bfseries\color{brand}\scriptsize 2. KIẾN THỨC}\\[2pt]
        {\tiny Công thức mới ngắn gọn, đóng khung nhớ}
      \end{tcolorbox}
    \end{column}
    \begin{column}{0.24\textwidth}
      \begin{tcolorbox}[accentcard]
        \centering
        {\bfseries\color{accent}\scriptsize 3. VÍ DỤ MẪU}\\[2pt]
        {\tiny GV làm mẫu cùng HS (có khung điền khuyết)}
      \end{tcolorbox}
    \end{column}
    \begin{column}{0.24\textwidth}
      \begin{tcolorbox}[successcard]
        \centering
        {\bfseries\color{success}\scriptsize 4. LUYỆN TẬP}\\[2pt]
        {\tiny HS tự làm giàn giáo (NB $\to$ TH $\to$ VD)}
      \end{tcolorbox}
    \end{column}
  \end{columns}
  \vspace{5pt}
  \begin{tcolorbox}[slidecard]
    \scriptsize
    💬 \textbf{Quy tắc đứng lớp:} GV chỉ cần dẫn dắt đúng theo 4 chặng này trên bản in Handout hoặc Slide Beamer. Mọi bước đi đều đã được dàn xếp tự nhiên để HS tiếp thu dễ dàng nhất.
  \end{tcolorbox}
\end{frame}

% ========================================================
% SLIDE 9: QUY TRÌNH 5 BƯỚC SOẠN PHIẾU CÙNG AI
% ========================================================
\begin{frame}{Quy Trình 5 Bước Soạn Phiếu Cùng AI}
  \vspace{-3pt}
  \begin{center}
    \begin{tikzpicture}[node distance=0.3cm, auto]
      \tikzset{
        wfstep/.style={draw=brand, fill=neutral, rounded corners=3pt, line width=0.7pt, text width=2.2cm, align=center, inner sep=3pt, font=\sffamily\tiny},
        wfarrow/.style={-{Stealth[length=3.5pt]}, line width=0.9pt, draw=brand!70}
      }
      \node[wfstep] (s1) {\textbf{1. Tìm Nguồn}\\TOANMATH, SGK, SGV};
      \node[wfstep, right=of s1] (s2) {\textbf{2. AI Phân Dạng}\\Sheet ma trận \& ra phiếu};
      \node[wfstep, draw=accent, fill=accent!8, right=of s2] (s3) {\textbf{3. GV Đọc Duyệt}\\Thẩm định sư phạm};
      \node[wfstep, draw=success, fill=successbg, right=of s3] (s5) {\textbf{5. Đóng Gói}\\Lên Drive \& Sheet C};
      \node[wfstep, below=0.4cm of s3] (s4) {\textbf{4. Đổi Câu}\\Báo AI tinh chỉnh};

      \draw[wfarrow] (s1) -- (s2);
      \draw[wfarrow] (s2) -- (s3);
      \draw[wfarrow, draw=success] (s3) -- node[above, font=\tiny\bfseries\color{success}] {Chuẩn} (s5);
      \draw[wfarrow, draw=accent] (s3) -- node[right, font=\tiny\color{accent}] {Chưa ưng} (s4);
      \draw[wfarrow, draw=accent] (s4) -| (s2);
    \end{tikzpicture}
  \end{center}
  \vspace{1pt}
  \begin{tcolorbox}[slidecard]
    \scriptsize
    \textbf{Tách bạch vai trò:} Con người kiểm soát mục tiêu sư phạm \& chất lượng đề $\longleftrightarrow$ AI phụ trách quét dữ liệu, tính toán định mức và biên dịch tài liệu.
  \end{tcolorbox}
\end{frame}

% ========================================================
% SLIDE 10: BƯỚC 1 & 2
% ========================================================
\begin{frame}{Bước 1 \& 2: Tìm Nguồn \& AI Phân Dạng}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=BƯỚC 1: Tìm Inputs Nguồn Uy Tín]
        \scriptsize
        • Nguồn đề thi chính thức Hà Nội:\\
        \href{https://thcs.toanmath.com}{\textbf{\color{info}thcs.toanmath.com}}\\[4pt]
        • Ảnh scan SGK, SGV Kết nối tri thức (có sẵn trong kho tham khảo).\\[4pt]
        • Sách bài tập và đề thi học kỳ chuẩn hóa các năm gần nhất.
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[accentcard, title=BƯỚC 2: AI Phân Dạng \& Thuyết Minh]
        \scriptsize
        Đưa đề cho AI quét vào Google Sheet:\\
        \href{https://docs.google.com/spreadsheets/d/1NCJHzp0cU9zUaJIkw47UfLzrPUj09P-5prgiGG6erDs/edit}{\textbf{\color{info}Google Sheet: Các Đầu Việc Học Liệu}}\\[4pt]
        • AI chấm mã câu (NB, TH, VD).\\
        • Đánh dấu năm đề \& trường ra đề.\\
        • Thống kê dạng bài \& xuất Phiếu nháp.
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 11: BƯỚC 3 & 4
% ========================================================
\begin{frame}{Bước 3 \& 4: Thẩm Định Sư Phạm \& Đổi Câu}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[accentcard, title=BƯỚC 3: GV Thẩm Định Sư Phạm]
        \scriptsize
        Cầm bản in PDF và tự trả lời 2 câu hỏi:\\[3pt]
        1. \textit{"Trên lớp thực tế 90', mình có dẫn dắt HS lớp C học kịp phiếu này không?"}\\[4pt]
        2. \textit{"Các câu NB đệm có dẫn dắt mượt mà đến câu VD đích không?"}
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=BƯỚC 4: Báo AI Đổi Câu (Vòng Lặp)]
        \scriptsize
        Nếu câu quá khó hoặc chưa ưng ý, chỉ cần nhắn cho AI trong ô chat:
        \vspace{3pt}
        \begin{tcolorbox}[quotecard]
          \color{brand}\itshape\tiny
          "Câu 3 phần Luyện tập hơi khó so với lớp C, hãy chọn câu khác cùng dạng từ ngân hàng đề để HS hứng thú hơn."
        \end{tcolorbox}
        \vspace{2pt}
        {\color{success}\textbf{👉 AI tự đọc lại ngân hàng $\to$ đổi câu $\to$ xuất lại PDF trong 10 giây!}}
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 12: BƯỚC 5
% ========================================================
\begin{frame}{Bước 5: Đóng Gói, Lên Drive \& Cập Nhật Tiến Độ}
  \begin{tcolorbox}[successcard]
    \scriptsize\centering
    \textbf{KHI PHIẾU ĐÃ CHUẨN 100\% — GV CHỈ CẦN RA LỆNH TRONG CHAT:}\\
    \colorbox{white}{\color{success}\bfseries\scriptsize "Phiếu đã duyệt xong, hãy đưa lên Drive và cập nhật sheet Tiến độ giúp tôi."}
  \end{tcolorbox}
  \vspace{1pt}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=1. Đồng Bộ Lên Google Drive]
        \scriptsize
        AI tự động đẩy trọn bộ 3 bản PDF vào đúng thư mục khối/lớp trên Drive:
        \begin{itemize}
          \setlength{\itemsep}{0pt}
          \item Bản Học sinh (Handout)
          \item Bản Giáo viên (Guide)
          \item Bản Trình chiếu (Slide 16:9)
        \end{itemize}
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=2. Cập Nhật Sheet TIẾN ĐỘ C]
        \scriptsize
        AI tự động điền link sản phẩm và đánh dấu hoàn thành vào:
        \vspace{3pt}
        \begin{center}
          \href{https://docs.google.com/spreadsheets/d/1fH7vl99bXoV8AQ9xqnXOsVAC5XQ3ESWk5zM7APd1o4k/edit?gid=1752741035\#gid=1752741035}{\textbf{\color{info}Google Sheet: TIẾN ĐỘ C}}
        \end{center}
        \vspace{1pt}
        {\tiny (Bấm link trên để xem bảng theo dõi tiến độ chi tiết của tổ).}
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

% ========================================================
% SLIDE 13: TỔNG KẾT
% ========================================================
\begin{frame}{Tổng Kết: Hệ Sinh Thái Sản Phẩm Hoàn Thành (Ví Dụ Lớp 9)}
  \vspace{-3pt}
  \begin{columns}[T]
    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[slidecard, title=1. Sheet Phân Dạng Chương]
        \scriptsize
        • Hàng trăm bài toán từ đề thi thật Hà Nội đã bóc tách ý a/b/c.\\
        • Chấm điểm L1–L5, tiêu chí T1–T8, gắn nhãn NB, TH, VD.
      \end{tcolorbox}
      \vspace{1pt}
      \begin{tcolorbox}[slidecard, title=2. Phiếu Thuyết Minh Chương (PDF)]
        \scriptsize
        • Ma trận 10–12 dạng bài/buổi, chuẩn thời lượng 90' hoặc 120'.\\
        • Bản thiết kế sư phạm được Thầy duyệt trước khi viết.
      \end{tcolorbox}
    \end{column}

    \begin{column}{0.48\textwidth}
      \begin{tcolorbox}[successcard, title=3. Kho Google Drive Hoàn Chỉnh]
        \scriptsize
        • Từng buổi: \textbf{Handout HS + Sổ tay GV + Slide Beamer}.\\
        • Cuối chương: \textbf{Đề kiểm tra 45' + Ma trận đáp án chuẩn thi}.
      \end{tcolorbox}
      \vspace{1pt}
      \begin{tcolorbox}[accentcard, title=4. Google Sheet TIẾN ĐỘ C]
        \scriptsize
        • Toàn bộ tiến độ được tích xanh hoàn thành kèm link trực tiếp.\\
        • Sẵn sàng in ấn phát cho học sinh và bàn giao cơ sở.
      \end{tcolorbox}
    \end{column}
  \end{columns}
\end{frame}

\end{document}
"""

tex_path = DOCS_DIR / "slide_huong_dan_gv.tex"
pdf_path = DOCS_DIR / "slide_huong_dan_gv.pdf"

tex_path.write_text(tex_source, encoding="utf-8")
print(f"Generated LaTeX at: {tex_path}")

cmd = ["tectonic", "-X", "compile", str(tex_path), "--outdir", str(DOCS_DIR)]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Compilation failed!")
    print(res.stderr)
else:
    print(f"Compilation succeeded! PDF generated at: {pdf_path}")
