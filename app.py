from flask import Flask, jsonify
import schedule
import time
import threading
import asyncio
from bot.social_bot import SocialBot
from bot.utils.logger import server_logger
import os

app = Flask(__name__)
bot = SocialBot()

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def schedule_tasks():
    # Generate new content daily at midnight
    schedule.every().day.at("00:00").do(bot.generate_daily_contents)
    
    # Schedule 6 posts per day
    schedule.every().day.at("09:00").do(lambda: run_async(bot.post_scheduled_content(0)))
    schedule.every().day.at("11:30").do(lambda: run_async(bot.post_scheduled_content(1)))
    schedule.every().day.at("13:19").do(lambda: run_async(bot.post_scheduled_content(2)))
    schedule.every().day.at("14:02").do(lambda: run_async(bot.post_scheduled_content(3)))
    schedule.every().day.at("18:00").do(lambda: run_async(bot.post_scheduled_content(4)))
    schedule.every().day.at("21:00").do(lambda: run_async(bot.post_scheduled_content(5)))

    # Check for replies every hour
    schedule.every(1).hours.do(lambda: run_async(bot.check_and_reply_to_comments()))

    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/api/logs')
def get_logs():
    try:
        with open('logs/bot.log', 'r') as f:
            logs = f.readlines()
        return jsonify({'logs': logs})
    except Exception as e:
        server_logger.error(f"Error reading logs: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Generate initial content
    bot.generate_daily_contents()
    # bot.check_and_reply_to_comments()
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_tasks)
    scheduler_thread.start()
    
    # Start Discord client in a separate thread
    # discord_thread = threading.Thread(target=bot.discord_client.start)
    # discord_thread.start()
    
    # Start Telegram client
    # asyncio.run(bot.telegram_client.start())
    
    # Start the Flask app
    server_logger.info("Server started")
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)  # Disable debug mode