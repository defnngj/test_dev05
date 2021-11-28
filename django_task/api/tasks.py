import os
from time import sleep
from celery import shared_task
from django_task.settings import BASE_DIR

TEST_FILE = os.path.join(BASE_DIR, "api", "running_tests.py")


@shared_task
def running():
    os.system(TEST_FILE)
    return


@shared_task
def add(x, y):
    sleep(10)
    return x + y

