# MathTech Engine — menu việc (gõ `make` hoặc `make help`).
# Quy trình soạn 1 phiếu:  make new FOLDER=... → (điền) → make check FILE=... → make build FILE=...
PY := .venv/bin/python
.DEFAULT_GOAL := help

help: ## Hiện danh sách việc
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

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

coverage: ## Spike: bank đủ câu để bốc không (BPT lớp C)
	@$(PY) scripts/spike_coverage.py

deadcode: ## Soi code chết (cần: pip install vulture)
	@$(PY) -m vulture src/ --min-confidence 80 || echo "  (cài vulture: .venv/bin/pip install vulture)"

.PHONY: help map test progress check new validate build spec thuyetminh coverage deadcode
