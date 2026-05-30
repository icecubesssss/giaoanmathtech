"""Định dạng của 1 bài toán — đơn vị Ground Truth nhỏ nhất.

Mọi bài toán phải có lời giải thực tế của con người (không để AI bịa).
Trường `human_verified` phục vụ geometry_gate.py (SymPy yếu với hình học).
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class MathProblem(BaseModel):
    source: str = Field(..., description="Nguồn: 'seed' hoặc URL/ID trong verified_scraped_bank")
    topic: str = Field(..., description="Mã node trong taxonomy_matrix, vd 'bdt.xet_hieu'")
    difficulty: int = Field(..., ge=1, le=10, description="Thang độ khó 1..10")
    statement: str = Field(..., description="Đề bài (LaTeX inline math cho phép)")
    solution: str = Field(..., description="Lời giải đầy đủ (Ground Truth của con người)")
    answer: str = Field("", description="Đáp số rút gọn nếu có")
    human_verified: bool = Field(False, description="True nếu đã được người kiểm (bắt buộc cho hình học)")
