from flask import Flask, jsonify
from flask_cors import CORS
import schedule
import time
import threading
import asyncio
from bot.social_bot import SocialBot
from bot.utils.logger import server_logger
import os

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"]
    }
})


bot = SocialBot()

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def schedule_tasks():
    print("schedule_tasks is called.")
    schedule.every().day.at("00:00").do(bot.generate_daily_contents)
    
    schedule.every().day.at("09:00").do(lambda: run_async(bot.post_scheduled_content(0)))
    schedule.every().day.at("11:30").do(lambda: run_async(bot.post_scheduled_content(1)))
    schedule.every().day.at("13:19").do(lambda: run_async(bot.post_scheduled_content(2)))
    schedule.every().day.at("14:02").do(lambda: run_async(bot.post_scheduled_content(3)))
    schedule.every().day.at("18:00").do(lambda: run_async(bot.post_scheduled_content(4)))
    schedule.every().day.at("21:00").do(lambda: run_async(bot.post_scheduled_content(5)))

    schedule.every(1).hours.do(lambda: run_async(bot.check_and_reply_to_comments()))

    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route("/api/logs")
def get_logs():
    print("get_logs is called.")
    try:
        with open('logs/bot.log', 'r') as f:
            logs = f.readlines()
        
        print("request is received.")
        filtered_logs = [log for log in logs if "N/A" not in log]
        last_10_logs = filtered_logs[-10:]
        
        print(f"Found {len(logs)} log entries, sending last 10 (excluding N/A)")
        return jsonify({'logs': last_10_logs})
    except Exception as e:
        print(f"Error: {str(e)}")
        server_logger.error(f"Error reading logs: {str(e)}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    bot.generate_daily_contents()
    scheduler_thread = threading.Thread(target=schedule_tasks)
    scheduler_thread.start()
    # discord_thread = threading.Thread(target=bot.discord_client.start)
    # discord_thread.start()
    # asyncio.run(bot.telegram_client.start())
    
    server_logger.info("Server started")
    # debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=False, host='0.0.0.0', port=5000)