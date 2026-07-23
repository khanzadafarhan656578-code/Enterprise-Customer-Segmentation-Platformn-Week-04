"""
Logging Infrastructure Module
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from app.core.config import settings

os.makedirs(settings.BASE_DIR / "logs", exist_ok=True)
LOG_FILE = settings.BASE_DIR / "logs" / "app.log"

logger = logging.getLogger("enterprise_app")
logger.setLevel(logging.INFO)

# Console Handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

# File Handler (Rotating)
f_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

if not logger.handlers:
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
