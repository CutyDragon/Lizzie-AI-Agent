import schedule
import time

def schedule_posts(task_function, interval_hours=1):
    schedule.every(interval_hours).hours.do(task_function)
    print(f"Scheduled to run every {interval_hours} hours.")

    while True:
        schedule.run_pending()
        time.sleep(1)
