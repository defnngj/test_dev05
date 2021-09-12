import os
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django_task.settings import BASE_DIR
from api.tasks import add

TEST_FILE = os.path.join(BASE_DIR, "api", "tests.py")


def task_run(request, tid):
    """运行测试任务
    1. 通过 task id 查询任务下面的用例
    2. 把用例的数据写到 test_data.json
    3. 通过unittest +ddt +xml-report 运行test_data.json 里面的用例，结果写道report.xml
    4. 读取report.xml 文件里面的测试结果，写到数据库。
    ？？
    1. 堵塞的问题： celery + threading
    2. 任务的状态：未执行，执行中，执行完成
    """
    print(tid)
    os.system(TEST_FILE)
    return JsonResponse({"success": "ok"})


def index(request):
    add.delay(1, 2)
    return JsonResponse({'msg': 'This is OK !'})


















