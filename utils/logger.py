import logging

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(message):
    logging.info(message)
    logging.shutdown()  # Ensure logs are flushed
