import logging
import os

LOG_FILE = "bot.log"

log_dir = os.path.dirname(LOG_FILE)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("bot_logger")

def log_message(level, message):
    level = level.upper()
    if level == "SUCCESS":
        logger.info(message)
    elif level == "INFO":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    else:
        logger.debug(message)
