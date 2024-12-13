from flask import Flask, render_template
from threading import Thread
import time
import schedule
from content_generator import generate_content
from platforms.twitter import post_to_twitter
from platforms.discord import post_to_discord
from utils.logger import log_message

app = Flask(__name__)
MAX_LOG_LINES = 10
LOG_FILE = "bot.log" 

prompt = "Write a financial tweet that captures your best financial perspective in 40 words or less."

def post_task():
    content = generate_content(prompt)
    print(f"Generated content: {content}")
    post_to_twitter(content)
    post_to_discord(content)

def schedule_posts(task_function, interval_hours=1):
    schedule.every(interval_hours).hours.do(task_function)
    print(f"Scheduled to run every {interval_hours} hours.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/log")
def api_log():
    try:
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
        recent_logs = lines[-MAX_LOG_LINES:][::-1]
        log_content = "".join(recent_logs) 
    except FileNotFoundError:
        log_content = "Log file not found."
    return log_content

def run_web_server():
    app.run(debug=False, host="0.0.0.0", port=5000)

def run_scheduler():
    schedule_posts(post_task, interval_hours=1)

if __name__ == "__main__":
    web_thread = Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    print("Web server is running.")

    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    print("Post scheduler is running.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Main program stopped.")
