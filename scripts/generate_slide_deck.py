# -*- coding: utf-8 -*-
"""
Script sinh file slide trình chiếu HTML tương tác và Markdown cho buổi hướng dẫn Giáo viên mới:
"HƯỚNG DẪN CÁCH SỬ DỤNG AI SOẠN PHIẾU HỌC TẬP & HỆ THỐNG TEMPLATE SHEETS"
"""

import base64
import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"

# Đọc logo compact và encode base64
logo_file = ASSETS_DIR / "logo_mathtech_compact.png"
if logo_file.exists():
    with open(logo_file, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    logo_b64 = ""

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hướng Dẫn Cách Sử Dụng AI Soạn Phiếu & Hệ Thống Template Sheets — MathTech</title>
    <!-- KaTeX CSS & JS for Math rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-slide: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --primary: #1e3a8a;
            --primary-light: #eff6ff;
            --accent: #d97706;
            --accent-light: #fef3c7;
            --border: #e2e8f0;
            --success: #15803d;
            --success-bg: #dcfce7;
            --card-bg: #f8fafc;
            --danger: #b91c1c;
            --danger-bg: #fee2e2;
            --purple: #7e22ce;
            --purple-bg: #ede7f6;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }}

        /* Slide Container */
        #presentation {{
            position: relative;
            width: 94vw;
            max-width: 1280px;
            height: 84vh;
            max-height: 740px;
            background: var(--bg-slide);
            border-radius: 18px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        /* Slide header & footer */
        .slide-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 32px 10px;
            border-bottom: 2px solid #f1f5f9;
            background: #ffffff;
        }}

        .slide-header .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .slide-header img.logo {{
            height: 34px;
            width: auto;
        }}

        .slide-header .tag {{
            font-size: 12px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            background: #eff6ff;
            padding: 4px 10px;
            border-radius: 6px;
        }}

        .slide-header-desc {{
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .slide-content {{
            flex: 1;
            padding: 24px 40px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: #ffffff;
        }}

        .slide-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 32px;
            border-top: 1px solid #f1f5f9;
            font-size: 12px;
            color: var(--text-muted);
            background: #f8fafc;
        }}

        /* Navigation Controls */
        .controls {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 12px;
            color: #ffffff;
        }}

        .controls button {{
            background: #1e293b;
            color: #ffffff;
            border: 1px solid #334155;
            border-radius: 8px;
            width: 40px;
            height: 36px;
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }}

        .controls button:hover {{
            background: var(--primary);
            border-color: var(--primary);
            transform: translateY(-1px);
        }}

        .controls .counter {{
            font-size: 14px;
            font-weight: 600;
            min-width: 80px;
            text-align: center;
            color: #cbd5e1;
        }}

        /* Slide Visibilities */
        .slide {{
            display: none;
            width: 100%;
            height: 100%;
            flex-direction: column;
            justify-content: center;
            animation: fadeIn 0.25s ease-out;
        }}

        .slide.active {{
            display: flex;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Typography */
        h1.title {{
            font-size: 32px;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.25;
            margin-bottom: 12px;
        }}

        h2.subtitle {{
            font-size: 18px;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 24px;
        }}

        h3.section-title {{
            font-size: 22px;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }}

        /* Grids & Cards */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.08);
        }}

        .card-primary {{
            border-left: 5px solid var(--primary);
            background: #eff6ff;
        }}

        .card-accent {{
            border-left: 5px solid var(--accent);
            background: #fffbeb;
        }}

        .card-success {{
            border-left: 5px solid var(--success);
            background: var(--success-bg);
        }}

        .card-danger {{
            border-left: 5px solid var(--danger);
            background: var(--danger-bg);
        }}

        .card-purple {{
            border-left: 5px solid var(--purple);
            background: var(--purple-bg);
        }}

        /* Buttons & Badges */
        .pill-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 14px;
            background: var(--primary);
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .pill-btn:hover {{
            background: #172554;
            transform: translateY(-1px);
        }}

        .pill-btn.secondary {{
            background: #e2e8f0;
            color: #1e293b !important;
        }}

        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .badge-cam {{ background: #fce4d6; color: #c2410c; }}
        .badge-vang {{ background: #fff2cc; color: #854d0e; }}
        .badge-xanh {{ background: #e2efda; color: #15803d; }}
        .badge-tim {{ background: #ede7f6; color: #6b21a8; }}
        .badge-do {{ background: #fee2e2; color: #b91c1c; }}
        .badge-lam {{ background: #dbeafe; color: #1d4ed8; }}

        /* Step containers */
        .step-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-top: 10px;
        }}

        .step-card {{
            flex: 1;
            background: var(--card-bg);
            border: 2px solid var(--border);
            border-radius: 10px;
            padding: 12px 14px;
            text-align: center;
        }}

        .step-card.active-step {{
            border-color: var(--primary);
            background: #eff6ff;
        }}

        .step-num {{
            width: 28px;
            height: 28px;
            background: var(--primary);
            color: #ffffff;
            font-weight: 800;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 8px;
            font-size: 14px;
        }}

        .step-arrow {{
            font-size: 20px;
            color: #94a3b8;
            font-weight: 800;
        }}

        /* Tables */
        table.custom-table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            font-size: 13px;
        }}

        table.custom-table th {{
            background: var(--primary);
            color: #ffffff;
            padding: 10px 12px;
            text-align: left;
            font-weight: 700;
        }}

        table.custom-table td {{
            padding: 8px 12px;
            border-bottom: 1px solid var(--border);
        }}

        table.custom-table tr:last-child td {{
            border-bottom: none;
        }}

        /* Sheet Table */
        table.sheet-table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            font-size: 12px;
            border: 1px solid #cbd5e1;
        }}

        table.sheet-table th {{
            background: #f1f5f9;
            color: #475569;
            padding: 6px 10px;
            border: 1px solid #cbd5e1;
            text-align: center;
            font-weight: 700;
        }}

        table.sheet-table td {{
            padding: 6px 10px;
            border: 1px solid #cbd5e1;
        }}

        .formula-box {{
            background: #f8fafc;
            border: 1px dashed #94a3b8;
            border-radius: 6px;
            padding: 8px 12px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 12px;
            color: #0f172a;
            margin-top: 6px;
        }}

        /* Dashboard Widget */
        .dashboard-banner {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px;
            margin-top: 12px;
        }}

        .dash-item {{
            text-align: center;
            padding: 8px;
            background: #ffffff;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }}

        .dash-val {{
            font-size: 20px;
            font-weight: 800;
            color: var(--primary);
        }}

        .dash-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 2px;
        }}

        /* Chat Bubbles */
        .chat-bubble-primary {{
            background: #ffffff;
            padding: 10px 14px;
            border-radius: 8px;
            font-style: italic;
            color: #1e3a8a;
            border: 1px dashed var(--primary);
            margin: 8px 0;
            font-size: 14px;
        }}

        .chat-bubble-success {{
            background: #ffffff;
            padding: 12px 16px;
            border-radius: 8px;
            font-weight: 700;
            color: #166534;
            font-size: 15px;
            border: 1px dashed var(--success);
            margin: 8px 0;
        }}

        .cover-box {{
            text-align: center;
            max-width: 820px;
            margin: 0 auto;
        }}

        .cover-tag {{
            display: inline-block;
            background: #eff6ff;
            color: var(--primary);
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }}

        .cover-meta {{
            display: flex;
            justify-content: center;
            gap: 24px;
            margin-top: 28px;
        }}

        .cover-meta-card {{
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 12px 24px;
            border-radius: 10px;
        }}

        .text-sm {{ font-size: 13px; line-height: 1.5; }}
        .text-xs {{ font-size: 11px; line-height: 1.4; }}
        .text-primary {{ color: var(--primary); }}
        .text-accent {{ color: var(--accent); }}
        .text-success {{ color: var(--success); }}
        .text-danger {{ color: var(--danger); }}
        .font-bold {{ font-weight: 700; }}
        .mb-4 {{ margin-bottom: 4px; }}
        .mb-8 {{ margin-bottom: 8px; }}
        .mb-12 {{ margin-bottom: 12px; }}
        .mb-16 {{ margin-bottom: 16px; }}
    </style>
</head>
<body>

    <div id="presentation">

        <!-- HEADER -->
        <div class="slide-header">
            <div class="brand">
                <img src="data:image/png;base64,{logo_b64}" class="logo" alt="MathTech Logo">
                <span class="tag">MathTech Learning Engine 2026</span>
            </div>
            <div class="slide-header-desc">
                Cẩm nang Giáo viên: Tư duy Sư phạm, 3 Template Sheets & Quy trình 5 bước AI
            </div>
        </div>

        <!-- SLIDE CONTENT -->
        <div class="slide-content">

            <!-- SLIDE 1: TIÊU ĐỀ -->
            <div class="slide active" id="slide-1">
                <div class="cover-box">
                    <div class="cover-tag">CẨM NANG NỘI BỘ DÀNH CHO GIÁO VIÊN MỚI</div>
                    <h1 class="title">HƯỚNG DẪN CÁCH SỬ DỤNG AI<br/>SOẠN PHIẾU HỌC TẬP & HỆ THỐNG TEMPLATE SHEETS</h1>
                    <h2 class="subtitle">
                        Tư duy phân tầng sư phạm, Hệ thống 3 Template Sheets liên kết động & Quy trình 5 bước phối hợp cùng Trợ lý AI
                    </h2>
                    <div class="cover-meta">
                        <div class="cover-meta-card">
                            <div class="dash-label">NGƯỜI THUYẾT TRÌNH</div>
                            <div class="font-bold text-primary" style="font-size: 16px; margin-top: 4px;">Trương Đình Thái</div>
                        </div>
                        <div class="cover-meta-card">
                            <div class="dash-label">ĐƠN VỊ</div>
                            <div class="font-bold text-accent" style="font-size: 16px; margin-top: 4px;">Tổ Học Liệu MathTech</div>
                        </div>
                        <div class="cover-meta-card">
                            <div class="dash-label">PHIÊN BẢN</div>
                            <div class="font-bold text-success" style="font-size: 16px; margin-top: 4px;">GDPT 2018 (Cập nhật 11/2026)</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 2: KHỞI ĐỘNG 3 PHÚT -->
            <div class="slide" id="slide-2">
                <h3 class="section-title">⚡ Khởi Động Nhanh (3 Phút): Tải Tool, Cài Extension & Mở AI</h3>
                <div class="grid-2">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8" style="font-size: 16px;">1. Tải Mã Nguồn & Antigravity</h4>
                        <ul style="padding-left: 20px; line-height: 1.6;" class="text-sm mb-12">
                            <li><strong>Mã nguồn MathTech:</strong> Tải ZIP về máy tính và giải nén.</li>
                            <li><strong>Ứng dụng AI Antigravity:</strong> Tải và cài đặt vào máy.</li>
                        </ul>
                        <div style="display: flex; gap: 10px;">
                            <a href="https://github.com/icecubesssss/giaoanmathtech" target="_blank" rel="noopener noreferrer" class="pill-btn">
                                📦 GitHub Codebase
                            </a>
                            <a href="https://antigravity.google/download" target="_blank" rel="noopener noreferrer" class="pill-btn secondary">
                                🚀 Tải Antigravity
                            </a>
                        </div>
                    </div>

                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8" style="font-size: 16px;">2. Cài 2 Extension Thiết Yếu & Mở AI</h4>
                        <ul style="padding-left: 20px; line-height: 1.6;" class="text-sm mb-12">
                            <li><strong>Claude Code Extension:</strong> Tương tác và gửi lệnh cho Trợ lý AI.</li>
                            <li><strong>vscode-pdf Extension:</strong> Xem trực tiếp 3 bản PDF (Handout HS, Guide GV, Slide) ngay trong cửa sổ làm việc.</li>
                        </ul>
                        <div class="chat-bubble-primary" style="margin: 0;">
                            💬 <strong>Kích hoạt môi trường (GV không cần gõ lệnh terminal):</strong><br/>
                            Chỉ cần mở ô chat AI và nhắn: <em>"Cài đặt môi trường giúp tôi"</em> $\to$ AI tự chạy 100%.
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 3: CƠ CHẾ HOẠT ĐỘNG -->
            <div class="slide" id="slide-3">
                <h3 class="section-title">🔄 Cơ Chế Hoạt Động: Inputs ➔ Process ➔ Outputs</h3>
                <div class="grid-3 mb-16">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">1. INPUTS (Nguyên liệu)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li>Đề thi thật Hà Nội các năm học gần nhất (2024–2025 trở đi).</li>
                            <li>Ảnh scan SGK, SGV Kết nối tri thức.</li>
                            <li>Sách bài tập chuẩn & chuyên đề thi vào 10.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8">2. PROCESS (AI Engine)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li>Tự động giải kiểm tra nghiệm bằng SymPy.</li>
                            <li>Vẽ hình học giải tích chuẩn xác bằng TikZ.</li>
                            <li>Cân đối quỹ thời lượng 90' hoặc 120'.</li>
                            <li>Gác cổng tự động (không trùng đề, đủ giờ).</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8">3. OUTPUTS (Bộ 3 PDF)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Handout HS:</strong> Thoáng, có khung làm bài.</li>
                            <li><strong>Guide GV:</strong> Đáp án chi tiết + gợi ý sư phạm.</li>
                            <li><strong>Slide Trình Chiếu:</strong> Tự ẩn lời giải, 16:9 Beamer.</li>
                        </ul>
                    </div>
                </div>
                <div class="formula-box text-center">
                    $$\\text{{INPUTS (Nguyên liệu sạch)}} \\xrightarrow[\\text{{SymPy + TikZ + Spec Gate}}]{{\\text{{MathTech AI Engine}}}} \\text{{OUTPUTS (Bộ 3 PDF Song Song + Đề Kiểm Tra)}}$$
                </div>
            </div>

            <!-- SLIDE 4: PHÂN TẦNG NĂNG LỰC -->
            <div class="slide" id="slide-4">
                <h3 class="section-title">🎯 Phân Tầng Năng Lực Học Sinh (A – B – C – X)</h3>
                <table class="custom-table mb-12">
                    <thead>
                        <tr>
                            <th style="width: 10%;">Tầng</th>
                            <th style="width: 35%;">Đối tượng học sinh</th>
                            <th style="width: 25%;">Mục tiêu điểm số</th>
                            <th style="width: 30%;">Giới hạn bài tập</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background: #eff6ff;">
                            <td class="font-bold text-primary" style="font-size: 16px;">C</td>
                            <td><strong>Nền tảng trung bình – yếu</strong>, hay quên kiến thức, sợ toán</td>
                            <td>Chắc SGK, đạt <strong>7,0 – 8,0 điểm</strong> trên trường</td>
                            <td><strong class="text-danger">Trần: Vận dụng (VD) — CẤM TUYỆT ĐỐI VDC</strong></td>
                        </tr>
                        <tr>
                            <td class="font-bold" style="font-size: 15px;">B</td>
                            <td>Trung bình – khá, nắm được kiến thức cơ bản</td>
                            <td>Kỳ I: 9,5 – 10đ; Kỳ II: 9,0 – 9,5đ</td>
                            <td>Có VDC nhẹ (ít câu VDC hơn lớp A)</td>
                        </tr>
                        <tr>
                            <td class="font-bold" style="font-size: 15px;">A</td>
                            <td>Khá – giỏi, tư duy toán tốt</td>
                            <td>Đạt điểm tối đa trên trường (10đ)</td>
                            <td>VDC dày dặn, mở rộng cấu hình hình học</td>
                        </tr>
                        <tr>
                            <td class="font-bold text-accent" style="font-size: 15px;">X</td>
                            <td>Chuyên Toán / Chất lượng cao</td>
                            <td>Chinh phục trọn vẹn câu cuối đề thi vào 10</td>
                            <td>VDC chuyên sâu, bất đẳng thức, cực trị</td>
                        </tr>
                    </tbody>
                </table>
                <div class="card card-primary text-sm">
                    📌 <strong>Quy chuẩn sư phạm:</strong> Trọng tâm hiện tại tập trung hoàn thiện 100% tài liệu cho <strong>LỚP C</strong> — nơi học sinh cần giàn giáo sư phạm vững chắc nhất để không bị bỏ lại phía sau.
                </div>
            </div>

            <!-- SLIDE 5: 4 CẤP ĐỘ CÂU HỎI -->
            <div class="slide" id="slide-5">
                <h3 class="section-title">📊 4 Cấp Độ Câu Hỏi (NB – TH – VD – VDC)</h3>
                <div class="grid-2">
                    <div class="card card-primary">
                        <div class="badge badge-lam mb-8">NB (Nhận biết — 1 bước)</div>
                        <p class="text-sm mb-8">Nhận diện công thức, định nghĩa, tính toán 1 bước trực tiếp:</p>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><em>Khối 3:</em> Tính nhẩm $7 \times 4 = 28$.</li>
                            <li><em>Khối 6:</em> Tính giá trị $2^3 = 8$.</li>
                            <li><em>Khối 9:</em> Tìm ĐKXĐ của $\\sqrt{{x-3}}$; nhận diện góc vuông tại tiếp điểm.</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <div class="badge badge-xanh mb-8">TH (Thông hiểu — 1–2 bước)</div>
                        <p class="text-sm mb-8">Áp dụng quy tắc, định lý vào bài toán cơ bản:</p>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><em>Khối 3:</em> "1 hộp có 8 cái bánh, 3 hộp có bao nhiêu cái?"</li>
                            <li><em>Khối 6:</em> Tính $A = 2^3 \cdot 5 - 3^2$.</li>
                            <li><em>Khối 9:</em> Rút gọn biểu thức chứa căn; chứng minh tam giác bằng nhau.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <div class="badge badge-cam mb-8">VD (Vận dụng — 2–3 bước)</div>
                        <p class="text-sm mb-8">Bài toán thực tế, phối hợp nhiều bước biến đổi:</p>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><em>Khối 3:</em> "35 quả cam chia 5 túi, đã bán 2 túi, còn lại bao nhiêu quả?"</li>
                            <li><em>Khối 6:</em> Tìm $x$ biết $2(x-3)^2 = 32$.</li>
                            <li><em>Khối 9:</em> Chứng minh tiếp tuyến $DB \perp OB$; tính chiều cao bằng TSLG.</li>
                        </ul>
                    </div>
                    <div class="card card-danger">
                        <div class="badge badge-do mb-8">VDC (Vận dụng cao — $\ge 4$ bước)</div>
                        <p class="text-sm mb-8">Phân hóa điểm 9,5 – 10; cực trị, hình phụ phức tạp:</p>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li>Dành riêng cho Lớp A, Lớp B và Lớp X.</li>
                            <li><strong class="text-danger">LỚP C: 0% — TUYỆT ĐỐI CẤM ĐƯA VÀO PHIẾU!</strong></li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- SLIDE 6: KỸ THUẬT NB TÁCH CÂU -->
            <div class="slide" id="slide-6">
                <h3 class="section-title">🧱 Kỹ Thuật Then Chốt: "NB Tách Câu" (Giàn Giáo Lớp C)</h3>
                <div class="card card-danger mb-12">
                    <strong class="text-danger">⚠️ NGUYÊN TẮC VÀNG: CẤM DÙNG CÂU NB RỜI RẠC, VÔ BỔ!</strong>
                    <p class="text-sm" style="margin-top: 4px;">
                        Không ra các câu nhận diện hình thức kiểu "đây có phải là phương trình không?" hoặc tính toán máy móc không xuất hiện trong đề thi. Mọi câu NB bắt buộc phải là <strong>bước đệm kỹ năng trích từ chính bài toán thi thật</strong>.
                    </p>
                </div>
                <div class="grid-2">
                    <div class="card">
                        <h4 class="font-bold text-primary mb-8">Bài Toán Đích Trong Đề Thi Thật</h4>
                        <div class="formula-box mb-8">
                            <strong>Bài toán [TH]:</strong> Tính giá trị biểu thức:<br/>
                            $$M = 150 - [100 - (3^2 \cdot 5)]$$
                        </div>
                        <p class="text-sm text-muted">
                            Học sinh lớp C thường lúng túng khi gặp ngoặc lồng ngoặc và lũy thừa dồn dập $\to$ dễ bỏ cuộc.
                        </p>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8">Chẻ Giàn Giáo Leo Dốc (Scaffolding)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Ý a [NB đệm]:</strong> Tính giá trị $3^2$ và $3^2 \cdot 5$.</li>
                            <li><strong>Ý b [TH]:</strong> Tính ngoặc vuông $[100 - (3^2 \cdot 5)]$ rồi tính $M$.</li>
                        </ul>
                        <p class="text-sm text-success font-bold" style="margin-top: 8px;">
                            👉 Hiệu quả: HS làm được ngay ý a, tự tin giải quyết trọn vẹn cả bài!
                        </p>
                    </div>
                </div>
            </div>

            <!-- SLIDE 7: TỈ LỆ CHUẨN LỚP C -->
            <div class="slide" id="slide-7">
                <h3 class="section-title">⚖️ Tỉ Lệ Chuẩn Lớp C: 40% NB – 40% TH – 20% VD</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">Công Thức Phân Bổ Năng Lực</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.7;">
                            <li><strong>40% Nhận biết (NB):</strong> Xây chắc kỹ năng cơ bản, tạo đà tâm lý.</li>
                            <li><strong>40% Thông hiểu (TH):</strong> Áp dụng công thức, rèn tính cẩn thận.</li>
                            <li><strong>20% Vận dụng (VD):</strong> Va chạm bài toán thực tế vừa sức.</li>
                            <li><strong>0% Vận dụng cao (VDC):</strong> Tránh gây quá tải và sợ hãi.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8">Định Mức Thời Lượng Ca Học 90 Phút</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.7;">
                            <li><strong>GV Giảng & Ví dụ mẫu:</strong> 25 phút.</li>
                            <li><strong>HS Luyện tập trên lớp:</strong> 55 phút (nghỉ giải lao 10 phút).</li>
                            <li><strong>BTVN tự luyện tại nhà:</strong> 40 phút.</li>
                            <li><em>(Định mức Khối 9: 1,5'/câu NB · 6'/câu TH · 12'/câu VD · Vẽ hình +5').</em></li>
                        </ul>
                    </div>
                </div>
                <div class="dashboard-banner">
                    <div class="dash-item"><div class="dash-val text-primary">40%</div><div class="dash-label">Nhận Biết (48')</div></div>
                    <div class="dash-item"><div class="dash-val text-success">40%</div><div class="dash-label">Thông Hiểu (48')</div></div>
                    <div class="dash-item"><div class="dash-val text-accent">20%</div><div class="dash-label">Vận Dụng (24')</div></div>
                    <div class="dash-item"><div class="dash-val text-danger">0%</div><div class="dash-label">VDC (Cấm Lớp C)</div></div>
                </div>
            </div>

            <!-- SLIDE 8: CẤU TRÚC 4 CHẶNG TRÊN PHIẾU -->
            <div class="slide" id="slide-8">
                <h3 class="section-title">📖 Cấu Trúc 4 Chặng Sư Phạm Của 1 Phiếu Học Tập</h3>
                <div class="step-container mb-16">
                    <div class="step-card active-step">
                        <div class="step-num">1</div>
                        <strong class="text-primary" style="font-size: 13px;">KIẾN THỨC NỀN</strong>
                        <p class="text-xs" style="margin-top: 4px;">Ôn lại kỹ năng lớp dưới hoặc bài trước (NB nền)</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card active-step">
                        <div class="step-num">2</div>
                        <strong class="text-primary" style="font-size: 13px;">KIẾN THỨC MỚI</strong>
                        <p class="text-xs" style="margin-top: 4px;">Định nghĩa, công thức ngắn gọn, dễ nhớ, có đóng khung</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card active-step">
                        <div class="step-num">3</div>
                        <strong class="text-primary" style="font-size: 13px;">VÍ DỤ MẪU</strong>
                        <p class="text-xs" style="margin-top: 4px;">GV cùng làm mẫu với HS (có khung điền khuyết làm mẫu)</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card active-step">
                        <div class="step-num">4</div>
                        <strong class="text-primary" style="font-size: 13px;">LUYỆN TẬP</strong>
                        <p class="text-xs" style="margin-top: 4px;">HS tự làm từ dễ đến khó (Luyện tập 1 $\to$ Luyện tập 2)</p>
                    </div>
                </div>
                <div class="card card-primary text-sm">
                    💬 <strong>Tư duy dạy học:</strong> Thầy cô lên lớp chỉ cần giảng đúng theo thứ tự 4 chặng này — tài liệu đã được dàn trang và lập trình sẵn để học sinh tiếp thu một cách tự nhiên nhất.
                </div>
            </div>

            <!-- SLIDE 9: QUY TRÌNH 5 BƯỚC SOẠN PHIẾU CÙNG AI -->
            <div class="slide" id="slide-9">
                <h3 class="section-title">🚀 Quy Trình 5 Bước Soạn Phiếu Cùng AI</h3>
                <div class="step-container mb-16">
                    <div class="step-card">
                        <div class="step-num">1</div>
                        <strong class="text-primary" style="font-size: 13px;">Tìm Nguồn Đề</strong>
                        <p class="text-xs" style="margin-top: 4px;">Đề thi Hà Nội, SGK, SGV</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card">
                        <div class="step-num">2</div>
                        <strong class="text-primary" style="font-size: 13px;">AI Phân Dạng</strong>
                        <p class="text-xs" style="margin-top: 4px;">Nạp Sheet & ra Thuyết minh</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card" style="border-color: var(--accent); background: #fffbeb;">
                        <div class="step-num" style="background: var(--accent);">3</div>
                        <strong class="text-accent" style="font-size: 13px;">GV Đọc Duyệt</strong>
                        <p class="text-xs" style="margin-top: 4px;">Kiểm tra sư phạm & thời lượng</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card">
                        <div class="step-num">4</div>
                        <strong class="text-primary" style="font-size: 13px;">Đổi Câu Phù Hợp</strong>
                        <p class="text-xs" style="margin-top: 4px;">Báo AI tinh chỉnh câu mới</p>
                    </div>
                    <div class="step-arrow">➔</div>
                    <div class="step-card" style="border-color: var(--success); background: #dcfce7;">
                        <div class="step-num" style="background: var(--success);">5</div>
                        <strong class="text-success" style="font-size: 13px;">Đóng Gói & Drive</strong>
                        <p class="text-xs" style="margin-top: 4px;">Xuất 3 PDF & cập nhật Sheet</p>
                    </div>
                </div>
                <div class="card card-accent text-sm">
                    🔄 <strong>Vòng lặp chất lượng:</strong> Nếu ở Bước 3 GV chưa ưng ý $\to$ Bước 4 yêu cầu AI đổi câu $\to$ AI xuất lại bản PDF mới trong 10 giây $\to$ Quay lại Bước 3 duyệt tiếp.
                </div>
            </div>

            <!-- SLIDE 10: HỆ THỐNG 3 TEMPLATE SHEETS -->
            <div class="slide" id="slide-10">
                <h3 class="section-title">📑 Hệ Thống 3 Template Sheets Liên Kết Động Trong MathTech</h3>
                <div style="margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; background: #eff6ff; padding: 10px 16px; border-radius: 8px; border: 1px solid #bfdbfe;">
                    <div style="font-size: 13px; font-weight: 700; color: #1e3a8a;">
                        📊 Link Google Sheets Mẫu (Đầy đủ 3 Tab Chuẩn):
                    </div>
                    <a href="https://docs.google.com/spreadsheets/d/1ARD_4AKM_aXlyGz3tOCoUYjOEnlOgXCmcO0ISeK6boY/edit" target="_blank" rel="noopener noreferrer" class="pill-btn">
                        🚀 Mở Spreadsheet Mẫu (Click để Tạo bản sao)
                    </a>
                </div>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">Template 1 & 2: Thiết Kế & Phân Dạng</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Template 1 (Tab Phân Dạng 47 Cột):</strong> Ngân hàng đề thi quét sạch từ nguồn, tự động lọc L1–L5 và chấm điểm T1–T8.</li>
                            <li><strong>Template 2 (Tab Thuyết Minh Động):</strong> Bản spec buổi học, cân đối chuẩn 40-40-20 và quỹ thời lượng 90'.</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8">Template 3: Bàn Giao & Tiến Độ Drive</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Template 3 (Sheet Quản Trị Tiến Độ):</strong> Quản lý tiến độ tuần, đồng bộ trọn bộ link Drive (Handout HS, Guide GV, Slide).</li>
                            <li><strong>Quy chuẩn Đề thi:</strong> <span class="text-muted">Đề thi do Thầy tạo riêng. GV và AI tập trung hoàn thiện 3 template bài giảng.</span></li>
                        </ul>
                    </div>
                </div>
                <div class="formula-box text-center text-sm">
                    <strong>Nguyên tắc cốt lõi:</strong> [Template 1: Ngân hàng 47 cột] $\\xrightarrow{{\\text{{Mã câu}}}}$ [Template 2: Thuyết minh spec] $\\xrightarrow{{\\text{{Duyệt}}}}$ [Bộ 3 PDF Song Song] $\\xrightarrow{{\\text{{Đóng gói}}}}$ [Template 3: Drive]
                </div>
            </div>

            <!-- SLIDE 11: TEMPLATE 1 - 47 CỘT CHUẨN -->
            <div class="slide" id="slide-11">
                <h3 class="section-title">📊 Template 1: Tab Phân Dạng Chương (47 Cột Chuẩn)</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8" style="font-size: 15px;">Phân Khu I, II, III: Thiết Kế & Giàn Giáo</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong class="text-primary">I. Dữ liệu đề thô (Cột A – M):</strong> Chép nguyên văn từ đề thật; gồm <em>Bài cụ thể</em>, <em>Nguồn</em>, <em>Mức độ</em>, <em>Dạng bài</em>, <em>Thời lượng</em>, <strong>Mã câu (M)</strong> (khóa định danh duy nhất).</li>
                            <li><strong class="text-accent">II. Giàn giáo §4b (Cột N – X):</strong> Gán 7 loại câu §4b (NB lẻ LT, NB tách TH, TH tách VD...); tự động xếp C/B/X; bộ lọc <strong>Loại ngay (L1–L5)</strong>; vùng <em>Chọn tay</em>.</li>
                            <li><strong>III. Bóc tách ý con (Cột Y – AE):</strong> Tách bài VD thành chuỗi bước đệm TH $\to$ NB; <em>Mã bài gốc</em>, <em>Kỹ thuật giải</em>, <em>Chương ([V])</em>, <em>Nhóm trùng</em>.</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8" style="font-size: 15px;">Phân Khu IV, V: Đánh Giá & Kết Luận</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong class="text-success">IV. Chấm 8 tiêu chí chất lượng (Cột AF – AM):</strong> Chấm 0, 1, 2 cho T1 Trọng tâm SGK $\dots$ T8 Mở rộng: Đánh giá ý toán trong sáng, nghiệm đẹp, bẫy lỗi sai kinh điển.</li>
                            <li><strong class="text-danger">V. Đánh giá phân tầng (Cột AN – AU):</strong> Tính điểm C/B/X, so ngưỡng mức AQ $\to$ Kết luận: <em>Đưa vào bài / Dự phòng / Loại</em>. <strong>THẦY DUYỆT</strong> chốt chặn.</li>
                        </ul>
                        <div style="border-top: 1px dashed var(--success); margin-top: 10px; padding-top: 8px;" class="text-xs">
                            💡 <strong>Mã màu nhận diện:</strong> <span class="badge badge-cam">Cam: VD/VDC</span> | <span class="badge badge-vang">Vàng: Thầy chọn</span> | <span class="badge badge-xanh">Xanh: Vào bài</span> | <span class="badge badge-tim">Tím: NB cũ</span> | <span class="badge badge-do">Đỏ: Loại</span>.
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 12: CƠ CHẾ LỌC L1-L5 VÀ CHẤM T1-T8 -->
            <div class="slide" id="slide-12">
                <h3 class="section-title">⚙️ Cơ Chế Lọc Loại Ngay (L1–L5) & Chấm Điểm (T1–T8) Tự Động</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-danger">
                        <h4 class="font-bold text-danger mb-8">Bộ Lọc Loại Ngay L1–L5 (Cột Q)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>L1:</strong> Sai kiến thức toán học / giả thiết ngớ ngẩn.</li>
                            <li><strong>L2:</strong> Lệch chuẩn chương trình SGK GDPT 2018.</li>
                            <li><strong>L3:</strong> Nghiệm số cồng kềnh, số lẻ vô tỉ xấu.</li>
                            <li><strong>L4:</strong> Quá 4 bước suy luận không thể tách giàn giáo.</li>
                            <li><strong>L5:</strong> Trùng ý chỉ đổi số trên lớp (chỉ cho phép ở BTVN).</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8">Công Thức Chấm Điểm Lớp C (Cột AN & AR)</h4>
                        <div class="formula-box mb-8">
                            $$\\text{{Điểm}}_C = \\frac{{3T_1 + 1T_2 + 2T_3 + 1T_4 + 2T_5 + 2T_6 + 2T_7 + 0T_8}}{{2 \\times 13}} \\times 10$$
                        </div>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><strong>Ngưỡng đưa vào bài (AQ):</strong> $\\text{{VD}} \\ge 7{{,}}0$ · $\\text{{TH}} \\ge 6{{,}}0$ · $\\text{{NB}} \\ge 5{{,}}0$.</li>
                            <li><strong>Công thức tự động (AR):</strong><br/>
                            <code>=IF(Q6<>"","LOẠI",IF(V6<>"","CHỌN TAY",IF(AN6>=AQ6,"ĐƯA VÀO BÀI","DỰ PHÒNG")))</code></li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- SLIDE 13: TEMPLATE 2 - THUYẾT MINH SPEC ĐỘNG -->
            <div class="slide" id="slide-13">
                <h3 class="section-title">📋 Template 2: Tab Thuyết Minh Liên Kết Động (Spec Dynamic Sheet)</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">Cấu Trúc Ma Trận Dạng Bài</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Loại câu (§4b):</strong> 7 nhãn chuẩn (NB lẻ LT, NB tách TH, NB ghép bài, TH lẻ LT, TH ghép bài, TH tách VD, VD lẻ) + NB kiến thức cũ.</li>
                            <li><strong>Dạng bài:</strong> Tên dạng toán chuẩn (bọc trong <code>$ ... $</code>).</li>
                            <li><strong>Mã câu đề xuất:</strong> Trỏ trực tiếp cột Mã câu (M) của Template 1.</li>
                            <li><strong>THẦY CHỌN & ĐỔI CÂU:</strong> Vùng Thầy nhập mã câu mới.</li>
                            <li><strong>Chốt mã:</strong> <code>=IF(Thầy_Chọn<>"", Thầy_Chọn, Đề_Xuất)</code>.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8">Gác Cổng Tự Động (thuyetminh_gate)</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li>Tự động chặn nếu quỹ giờ trên lớp lệch quá $\pm 10\%$.</li>
                            <li>Tự động chặn nếu xuất hiện câu VDC ở Lớp C.</li>
                            <li>Cảnh báo nếu thiếu khai báo nhãn Loại câu §4b.</li>
                            <li>Tự động kiểm tra liên kết mã câu với Tab Phân dạng.</li>
                        </ul>
                    </div>
                </div>
                <div class="dashboard-banner">
                    <div class="dash-item"><div class="dash-val text-primary">25.0'</div><div class="dash-label">GV Giảng & Mẫu</div></div>
                    <div class="dash-item"><div class="dash-val text-success">55.0'</div><div class="dash-label">HS Làm Trên Lớp</div></div>
                    <div class="dash-item"><div class="dash-val text-accent">40.0'</div><div class="dash-label">BTVN Tự Luyện</div></div>
                    <div class="dash-item"><div class="dash-val text-primary">PASS</div><div class="dash-label">Thuyết Minh Gate</div></div>
                </div>
            </div>

            <!-- SLIDE 14: TEMPLATE 3 - SHEET TIẾN ĐỘ & DRIVE -->
            <div class="slide" id="slide-14">
                <h3 class="section-title">📈 Template 3: Sheet Quản Trị Tiến Độ & Đồng Bộ Google Drive</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">Cấu Trúc Quản Trị Tiến Độ Tuần</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Thông tin ca học:</strong> Tuần / Ca $\to$ Mã phiếu $\to$ Tên bài SGK.</li>
                            <li><strong>Hồ sơ gốc:</strong> Link Sheet Phân dạng $\to$ Link Thuyết minh PDF.</li>
                            <li><strong>Trạng thái duyệt:</strong> 🟡 Đang soạn $\to$ 🟠 Chờ duyệt $\to$ 🟢 **ĐÃ DUYỆT**.</li>
                            <li><strong>Nghiệm thu:</strong> Tích xanh checkbox khi bàn giao in ấn cho cơ sở.</li>
                        </ul>
                    </div>
                    <div class="card card-success">
                        <h4 class="font-bold text-success mb-8">Đồng Bộ 100% Lên Google Drive</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li><strong>Link Handout Học Sinh:</strong> Bản in HS có khung làm bài.</li>
                            <li><strong>Link Sổ Tay Giáo Viên:</strong> Bản GV có đáp án + gợi ý.</li>
                            <li><strong>Link Slide Trình Chiếu:</strong> File Beamer 16:9 tương tác.</li>
                            <li><strong>Link File Nguồn:</strong> Mã nguồn phiếu JSON + TeX lưu trữ.</li>
                        </ul>
                    </div>
                </div>
                <div class="chat-bubble-success text-center">
                    💬 Khi GV duyệt xong, chỉ cần nhắn AI: <em>"Hãy đưa lên Drive và cập nhật Sheet Tiến độ giúp tôi"</em> $\to$ AI tự làm 100%!
                </div>
            </div>

            <!-- SLIDE 15: THỰC HÀNH BƯỚC 1 & 2 -->
            <div class="slide" id="slide-15">
                <h3 class="section-title">📂 Thực Hành Bước 1 & 2: Tìm Nguồn & AI Phân Dạng</h3>
                <div class="grid-2">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">BƯỚC 1: Chuẩn Bị Inputs Nguồn</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.6;">
                            <li>Đề thi chính thức các trường Hà Nội: <a href="https://thcs.toanmath.com" target="_blank" rel="noopener noreferrer" class="font-bold text-primary">thcs.toanmath.com</a>.</li>
                            <li>Ảnh scan SGK, SGV Kết nối tri thức có sẵn trong kho.</li>
                            <li>Sách bài tập & đề thi chọn lọc các năm học gần nhất.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8">BƯỚC 2: AI Quét Đề & Lập Template 1 & 2</h4>
                        <p class="text-sm mb-8">Đưa đề cho AI đọc và quét trực tiếp vào Google Sheets:</p>
                        <div class="chat-bubble-primary mb-8">
                            "Hãy quét các file đề thi HK1 trong thư mục inputs và điền vào Template 1 phân dạng Chương 5 giúp tôi. Chấm điểm T1-T8 cho lớp C."
                        </div>
                        <p class="text-xs text-muted">
                            👉 AI tự động chấm mã câu, gán nhãn §4b, chấm T1–T8, tính kết luận Lớp C và tạo dự thảo Template 2 (Thuyết minh).
                        </p>
                    </div>
                </div>
            </div>

            <!-- SLIDE 16: THỰC HÀNH BƯỚC 3 & 4 -->
            <div class="slide" id="slide-16">
                <h3 class="section-title">🔍 Thực Hành Bước 3 & 4: Thẩm Định Sư Phạm & Đổi Câu</h3>
                <div class="grid-2">
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-8">BƯỚC 3: GV Thẩm Định Sư Phạm</h4>
                        <p class="text-sm mb-8">Mở bản in PDF Thuyết minh và đối chiếu 2 câu hỏi lớn:</p>
                        <ol class="text-sm" style="padding-left: 20px; line-height: 1.6;">
                            <li><em>"Trên lớp thực tế 90', mình có dẫn dắt HS lớp C học kịp phiếu này không?"</em></li>
                            <li><em>"Các câu NB đệm có dẫn dắt mượt mà đến câu VD đích không?"</em></li>
                        </ol>
                    </div>
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-8">BƯỚC 4: Đổi Câu Linh Hoạt</h4>
                        <p class="text-sm mb-8">Nếu câu quá khó hoặc bài khô khan, có 2 cách đổi:</p>
                        <ul class="text-sm mb-8" style="padding-left: 18px; line-height: 1.5;">
                            <li><strong>Cách 1:</strong> Gõ mã câu mới vào cột <em>THẦY CHỌN</em> ở Template 2.</li>
                            <li><strong>Cách 2:</strong> Nhắn trực tiếp trong ô chat AI:</li>
                        </ul>
                        <div class="chat-bubble-primary">
                            "Câu 3 phần Luyện tập hơi khó so với lớp C, hãy chọn câu khác cùng dạng từ ngân hàng đề giúp tôi."
                        </div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 17: THỰC HÀNH BƯỚC 5 -->
            <div class="slide" id="slide-17">
                <h3 class="section-title">☁️ Thực Hành Bước 5: Đóng Gói, Lên Drive & Cập Nhật Tiến Độ</h3>
                <div class="card card-success mb-16">
                    <h4 class="font-bold text-success mb-6" style="font-size: 15px;">Khi Phiếu Đã Chuẩn 100% — GV Ra Lệnh Một Chạm Cho AI:</h4>
                    <div class="chat-bubble-success text-center">
                        "Phiếu 2 Chương 5 đã duyệt xong, hãy đưa lên Drive và cập nhật Template 3 (Sheet Tiến độ) giúp tôi."
                    </div>
                </div>
                <div class="grid-2">
                    <div class="card">
                        <h4 class="font-bold text-primary mb-6">1. Tự Động Build & Xuất Bản</h4>
                        <p class="text-sm">AI tự chạy gác cổng nghiệm (SymPy) $\to$ render song song 3 bản PDF (Handout HS, Guide GV, Slide Beamer) $\to$ tải lên đúng thư mục Google Drive.</p>
                    </div>
                    <div class="card">
                        <h4 class="font-bold text-primary mb-6">2. Cập Nhật Sheet Tiến Độ</h4>
                        <p class="text-sm">AI tự động điền URL Google Drive vào các cột Handout, Guide, Slide và tích xanh nghiệm thu hoàn thành.</p>
                    </div>
                </div>
            </div>

            <!-- SLIDE 18: TỔNG KẾT & CHEAT-SHEET -->
            <div class="slide" id="slide-18">
                <h3 class="section-title">🏆 Tổng Kết: Hệ Sinh Thái Sản Phẩm & Cheat-Sheet Lệnh AI</h3>
                <div class="grid-2 mb-12">
                    <div class="card card-primary">
                        <h4 class="font-bold text-primary mb-6">Hệ Sinh Thái Hoàn Thành Mỗi Chương</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><strong>Template 1:</strong> Ngân hàng đề 47 cột chấm điểm T1–T8.</li>
                            <li><strong>Template 2:</strong> Phiếu Thuyết minh cân đối 40-40-20.</li>
                            <li><strong>Bộ 3 PDF Song Song:</strong> Handout HS + Guide GV + Slide.</li>
                            <li><strong>Template 3:</strong> Sheet Tiến độ tích xanh đồng bộ Drive.</li>
                        </ul>
                    </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-6">Cheat-Sheet Câu Lệnh Cho Giáo Viên</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><code>make b</code>: Build 3 PDF cho phiếu vừa làm (~9s).</li>
                            <li><code>make check-tm SPEC=...</code>: Gác cổng thời lượng.</li>
                            <li><em>"Cài đặt môi trường giúp tôi"</em>: Cài đặt tự động.</li>
                            <li><em>"Đổi câu X sang câu Y"</em>: Đổi câu tức thì.</li>
                            <li><em>"Đưa lên Drive và cập nhật Sheet"</em>: Hoàn tất buổi học.</li>
                        </ul>
                    </div>
                </div>
                <div class="formula-box text-center text-xs">
                    MathTech Engine 2026 — Đồng hành cùng Thầy Cô kiến tạo học liệu chuẩn mực, truyền cảm hứng cho mọi học sinh!
                </div>
            </div>
                    <div class="card card-accent">
                        <h4 class="font-bold text-accent mb-6">Cheat-Sheet Câu Lệnh Cho Giáo Viên</h4>
                        <ul class="text-sm" style="padding-left: 18px; line-height: 1.5;">
                            <li><code>make b</code>: Build 3 PDF cho phiếu vừa làm (~9s).</li>
                            <li><code>make check-tm SPEC=...</code>: Gác cổng thời lượng.</li>
                            <li><em>"Cài đặt môi trường giúp tôi"</em>: Cài đặt tự động.</li>
                            <li><em>"Đổi câu X sang câu Y"</em>: Đổi câu tức thì.</li>
                            <li><em>"Đưa lên Drive và cập nhật Sheet"</em>: Hoàn tất buổi học.</li>
                        </ul>
                    </div>
                </div>
                <div class="formula-box text-center text-xs">
                    MathTech Engine 2026 — Đồng hành cùng Thầy Cô kiến tạo học liệu chuẩn mực, truyền cảm hứng cho mọi học sinh!
                </div>
            </div>

        </div>

        <!-- FOOTER -->
        <div class="slide-footer">
            <div>MathTech AI Engine © 2026 — Trương Đình Thái</div>
            <div>Bấm phím mũi tên ⬅️ ➡️ để chuyển slide | Phím <strong>F</strong>: Toàn màn hình</div>
        </div>

    </div>

    <!-- FLOATING CONTROLS -->
    <div class="controls">
        <button id="prevBtn" title="Slide trước (Phím ⬅️)">❮</button>
        <div class="counter" id="slideCounter">1 / 18</div>
        <button id="nextBtn" title="Slide sau (Phím ➡️)">❯</button>
        <button id="fsBtn" title="Toàn màn hình (Phím F)">⛶</button>
    </div>

    <script>
        const slides = document.querySelectorAll('.slide');
        let currentSlide = 0;
        const totalSlides = slides.length;

        const slideCounter = document.getElementById('slideCounter');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const fsBtn = document.getElementById('fsBtn');

        function updateSlide(index) {{
            slides.forEach((s, i) => {{
                s.classList.toggle('active', i === index);
            }});
            slideCounter.textContent = `${{index + 1}} / ${{totalSlides}}`;
        }}

        function nextSlide() {{
            if (currentSlide < totalSlides - 1) {{
                currentSlide++;
                updateSlide(currentSlide);
            }}
        }}

        function prevSlide() {{
            if (currentSlide > 0) {{
                currentSlide--;
                updateSlide(currentSlide);
            }}
        }}

        nextBtn.addEventListener('click', nextSlide);
        prevBtn.addEventListener('click', prevSlide);

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
                prevSlide();
            }} else if (e.key === 'f' || e.key === 'F') {{
                toggleFullScreen();
            }}
        }});

        function toggleFullScreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(() => {{}});
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        fsBtn.addEventListener('click', toggleFullScreen);

        // Render KaTeX after DOM loaded
        document.addEventListener("DOMContentLoaded", function() {{
            if (window.renderMathInElement) {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: "$$", right: "$$", display: true}},
                        {{left: "$", right: "$", display: false}}
                    ],
                    throwOnError: false
                }});
            }}
        }});
    </script>
</body>
</html>
"""

with open(DOCS_DIR / "slide_huong_dan_gv.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML slide deck (18 slides) at: {DOCS_DIR / 'slide_huong_dan_gv.html'}")
