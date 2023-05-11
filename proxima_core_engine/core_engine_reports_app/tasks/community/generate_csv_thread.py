
from celery import shared_task
import time

@shared_task
def generate_csv_thread(task_type):
    time.sleep(int(task_type) * 10)
    return True