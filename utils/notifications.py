import threading
import time
import schedule
from plyer import notification
from datetime import datetime

# Keep a map of doc_id to scheduled jobs
scheduled_jobs = {}

def show_notification(title, message="Don't forget!"):
    notification.notify(
        title=title,
        message=message,
        app_name="HomePro",
        timeout=10  # seconds
    )

def schedule_notification(task_title, task_datetime, doc_id):
    # Cancel old one if exists
    if doc_id in scheduled_jobs:
        schedule.cancel_job(scheduled_jobs[doc_id])
        del scheduled_jobs[doc_id]

    def job():
        print(f"[NOTIFY] {task_title} at {task_datetime}")
        show_notification(task_title)

    def match_time_job():
        now = datetime.now()
        delta = abs((task_datetime - now).total_seconds())
        if delta < 60:  # within the same minute
            print(f"[TRIGGERING] Notification for {task_title}")
            job()
            return schedule.CancelJob
        else:
            print(f"[PENDING] {task_title} | now: {now.strftime('%H:%M:%S')} vs target: {task_datetime.strftime('%H:%M:%S')}")


    scheduled_jobs[doc_id] = schedule.every(20).seconds.do(match_time_job)

def cancel_notification(doc_id):
    if doc_id in scheduled_jobs:
        schedule.cancel_job(scheduled_jobs[doc_id])
        del scheduled_jobs[doc_id]

def start_notification_loop():
    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()