import os
import json
from time import sleep
from celery import shared_task
from backend.settings import BASE_DIR
from app_api.models import TestCase, TestResult
from xml.dom.minidom import parse

# 运行测试用例文件
TEST_FILE = os.path.join(BASE_DIR, "app_api", "running_tests.py")

"""
eelery 启动方式
celery -A backend worker --loglevel=info -P eventlet
"""


@shared_task
def running():
    """
    todo
    问题：不能存在数据库的操作
    """
    # 2.执行测试用例
    os.system(TEST_FILE)
    return
