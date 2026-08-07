# MathTech Engine — menu việc (gõ `make` hoặc `make help`).
# Quy trình soạn 1 phiếu:  make new FOLDER=... → (điền) → make check FILE=... → make build FILE=...
# SỬA NHANH 1-2 CHỖ:      make md Q="hinh binh hanh"  (đọc) → sửa → make b  (build lại)
# Python trong .venv nằm khác chỗ giữa 2 hệ: macOS/Linux `bin/`, Windows `Scripts/`.
ifeq ($(OS),Windows_NT)
PY := .venv/Scripts/python.exe
else
PY := .venv/bin/python
endif
.DEFAULT_GOAL := help

b: ## Sửa xong build lại NGAY: make b Q="hinh binh hanh"  ·  make b (lặp phiếu vừa làm)
	@$(PY) -m scripts.quick build $(Q)

md: ## Đọc phiếu dạng dễ nhìn (sinh .md, bấm ⌘⇧V): make md Q="hinh binh hanh"
	@$(PY) -m scripts.quick md $(Q)

f: ## Tìm đường dẫn phiếu theo mẩu tên: make f Q="hbh"
	@$(PY) -m scripts.quick find $(Q)

prune: ## Liệt kê outputs/ mồ côi (thêm YES=1 để xoá thật)
	@$(PY) -m scripts.prune_outputs $(if $(YES),--delete,)

help: ## Hiện danh sách việc
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

map: ## Cập nhật PROJECT_MAP.md (bản đồ codebase, đọc trước cho đỡ token)
	@$(PY) scripts/repomap.py

test: ## Chạy toàn bộ pytest
	@$(PY) -m pytest tests/ -q

progress: ## Tiến độ các tuần còn thiếu (PDF nguồn / JSON / build)
	@$(PY) -m src.main progress --todo

check: ## Gác cổng cả kho (validate-all)
	@$(PY) -m src.main validate-all

new: ## Sinh khung phiếu:  make new FOLDER="inputs/seeds/.../tuanNN-..."
	@$(PY) -m src.main new-lesson "$(FOLDER)"

validate: ## Validate 1 phiếu:  make validate FILE=path.json  [FAST=1 bỏ SymPy]
	@$(PY) -m src.main validate "$(FILE)" $(if $(FAST),--fast,)

build: ## Build 3 PDF song song:  make build FILE=path.json  [ONLY=handout]
	@$(PY) -m src.main build "$(FILE)" $(if $(ONLY),--only $(ONLY),)

spec: ## Sinh khung THUYẾT MINH (số câu auto):  make spec FOLDER="..." TIER=C
	@$(PY) -m src.main new-thuyetminh "$(FOLDER)" $(if $(TIER),--tier $(TIER),)

thuyetminh: ## Render thuyết minh ra PDF:  make thuyetminh SPEC=path/thuyet-minh.json
	@$(PY) -m src.main build-thuyetminh "$(SPEC)"

check-tm: ## Soi giờ vô lý trong spec:  make check-tm SPEC=path/thuyet-minh.json
	@$(PY) -m src.main validate-thuyetminh "$(SPEC)"

coverage: ## Spike: bank đủ câu để bốc không (BPT lớp C)
	@$(PY) scripts/spike_coverage.py

exam-report: ## Phút/câu thực theo band trong ngân hàng đề (đối chiếu rate card)
	@$(PY) -m scripts.exam_annotate report

exam-check: ## Gác cổng ngân hàng đề: Σdiem, band/phut, trùng id
	@$(PY) -m scripts.exam_annotate check

exam-weights: ## Sinh file trọng số tần suất dạng (từ bank đã gắn band/phut)
	@$(PY) -m scripts.build_exam_weights

deadcode: ## Soi code chết (cần: pip install vulture)
	@$(PY) -m vulture src/ --min-confidence 80 || echo "  (cài vulture: .venv/bin/pip install vulture)"

build-folder: ## Build MỌI phiếu trong 1 folder:  make build-folder FOLDER=path/folder
	@$(PY) -m src.main build-folder "$(FOLDER)"

c3-c: ## Build nhanh toàn bộ 5 phiếu Lớp 9 [C] Chương 3 (PDF Handout/Guide/Slide)
	@$(PY) -m src.main build-folder "inputs/seeds/lop-9/dai-so/lop-c/chuong-03-can-bac-hai-can-bac-ba"

tm-c3: ## Render Thuyết Minh PDF Chương 3 Lớp 9 [C]
	@$(PY) -m src.main build-thuyetminh "inputs/seeds/lop-9/dai-so/lop-c/chuong-03-can-bac-hai-can-bac-ba/thuyet-minh.json"

.PHONY: b md f prune help map test progress check new validate build spec thuyetminh check-tm coverage exam-report exam-check exam-weights deadcode build-folder c3-c tm-c3
