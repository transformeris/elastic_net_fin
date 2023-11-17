from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_MISSED
import time

# 创建调度器
scheduler = BackgroundScheduler()

def my_listener(event):
    print('cu')

    if event.code == EVENT_JOB_MISSED:
        print(f"Job {event.job_id} was missed!")
        # 重新安排任务
        scheduler.add_job(my_task, 'interval', seconds=5)

def my_task():
    print("Running task...")
    time.sleep(9)  # 使任务执行时间超过预定的间隔，从而导致miss

scheduler.add_listener(my_listener)
scheduler.add_job(my_task, 'interval', seconds=5)

scheduler.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()