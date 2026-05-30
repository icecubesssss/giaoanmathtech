"""Trình lập lịch tự động kích hoạt Worker cào đề lúc 0h đêm hằng ngày.

Sử dụng vòng lặp an toàn hoặc APScheduler nếu có để lập lịch.
"""
from __future__ import annotations

import logging
import time
from threading import Thread

from src.scrapers.offline_worker import run_scraping_job

logger = logging.getLogger("mathtech.scheduler")


def start_scheduler_thread():
    """Bắt đầu luồng lập lịch cào đề chạy ngầm hằng ngày."""
    def _loop():
        logger.info("Scheduler cào đề ngầm bắt đầu khởi động.")
        # Lần chạy đầu tiên để nạp đầy đủ ngân hàng đề thi
        try:
            stats = run_scraping_job()
            logger.info(f"Nạp dữ liệu đề thi thành công: {stats}")
        except Exception as e:
            logger.error(f"Lỗi khởi tạo ngân hàng đề thi: {e}")
            
        while True:
            # Lập lịch chạy hằng ngày (khoảng 86400 giây)
            time.sleep(86400)
            try:
                logger.info("Kích hoạt phiên cào đề định kỳ lúc 0h...")
                stats = run_scraping_job()
                logger.info(f"Hoàn thành cào đề định kỳ: {stats}")
            except Exception as e:
                logger.error(f"Lỗi trong phiên cào đề định kỳ: {e}")

    thread = Thread(target=_loop, daemon=True, name="MathScraperScheduler")
    thread.start()
    return thread
