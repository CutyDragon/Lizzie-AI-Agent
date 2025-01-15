import logging
import os

def setup_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    handler = logging.FileHandler(f'logs/{log_file}')
    
    if name == 'bot_logger':
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(tweet_id)s|%(type)s|%(content)s|%(content_link)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

bot_logger = setup_logger('bot_logger', 'bot.log')
server_logger = setup_logger('server_logger', 'server.log')