# backend/app/utils/logger.py

import logging
from ..config import settings

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger configured with the level from settings.LOG_LEVEL
    and a simple console handler if none exists.
    """
    logger = logging.getLogger(name)
    # Use the level from your settings (e.g. "INFO", "DEBUG", etc.)
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    # Only add a handler if the logger has no handlers already
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        fmt = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)

    return logger
