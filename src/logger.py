from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

_DEFAULT_LOG_DIR = Path(__file__).resolve().parents[1] / "data" / "logs"


def setup_logging(log_dir: str | Path | None = None) -> None:
    """Configure root logger with a console handler and a dated file handler.

    Safe to call multiple times; subsequent calls are no-ops once handlers exist.
    """
    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(fmt)
        root.addHandler(console_handler)

        log_path = Path(log_dir) if log_dir else _DEFAULT_LOG_DIR
        log_path.mkdir(parents=True, exist_ok=True)
        date_stamp = datetime.now().strftime("%Y%m%d")
        file_handler = logging.FileHandler(
            log_path / f"literary_analysis_{date_stamp}.log", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)

    # Keep external libraries from flooding logs while preserving local debug detail.
    for noisy_logger in (
        "httpx",
        "httpcore",
        "openai",
        "openai._base_client",
        "asyncio",
    ):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
