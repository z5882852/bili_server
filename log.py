import os
import sys
from loguru import logger
from utils import config


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_CONFIG = config.get("log", {})

# =======日志相关配置=======
SHOW_LOG = LOG_CONFIG.get("show", True)
SAVE_LOG = LOG_CONFIG.get("save", True)
DEBUG = LOG_CONFIG.get("debug", False)

logger.remove(0)
level = "DEBUG" if DEBUG else "INFO"
if SHOW_LOG:
    console_log_handler = logger.add(sys.stderr, level=level, enqueue=True)
if SAVE_LOG:
    LOG_DIR = os.path.join(CURRENT_PATH, str(LOG_CONFIG.get("dir", "logs")))
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    LOG_PATH = os.path.join(LOG_DIR, "log_{time}.log")
    file_log_handler = logger.add(LOG_PATH, level=level, encoding="utf-8", enqueue=True)

logger.debug("日志初始化成功!")

