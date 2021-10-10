import os
from time import sleep
from celery import shared_task
from backend.settings import BASE_DIR

TEST_FILE = os.path.join(BASE_DIR, "app_api", "running_tests.py")


@shared_task
def running():
    os.system(TEST_FILE)
    return
