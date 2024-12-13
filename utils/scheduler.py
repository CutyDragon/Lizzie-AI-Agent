import schedule
import time

def schedule_posts(task_function, interval_hours=1):
    schedule.every(interval_hours).hours.do(task_function)
    print(f"Scheduled to run every {interval_hours} hours.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")
