import os
import json
import threading
import time
from time import sleep
from xml.dom.minidom import parse
from backend.settings import BASE_DIR
from app_api.models import TestCase, TestTask, TaskCaseRelevance, TestResult
from app_api.tasks import running

# 测试数据文件
DATA_FILE_PATH = os.path.join(BASE_DIR, "app_api", "data", "test_data.json")
# 测试报告文件
REPORT_PATH = os.path.join(BASE_DIR, "app_api", "data", "report.xml")


class TaskThread:

    def __init__(self, task_id, cases):
        self.tid = task_id
        self.cases = cases

    def run_cases(self):
        # 1. 读取测试用例，写入测试文件表
        print("1. 读取测试用例，写入测试文件")
        cases_dict = {}
        for case in self.cases:
            case = TestCase.objects.get(id=case)
            cases_dict["case" + str(case.id)] = {
                "url": case.url,
                "method": case.method,
                "header": case.header,
                "params_type": case.params_type,
                "params_body": case.params_body,
                "assert_type": case.assert_type,
                "assert_text": case.assert_text
            }

        cases_json = json.dumps(cases_dict)
        with(open(DATA_FILE_PATH, "w")) as f:
            f.write(cases_json)

        # 3.执行运行测试用例的文件， 它会生成 result.xml 文件
        print("3.运行用例前---》", time.ctime())
        running.delay()
        # os.system()
        print("3.运行用例后---》", time.ctime())

        # 4. 读取report.xml文件，把这里面的结果放到表里面。
        print("4. 读取report.xml文件")
        self.save_result()
        print("4. 保存完成")

        # 5. 任务->已执行
        print("5.任务->已执行")
        TestTask.objects.select_for_update().filter(id=self.tid).update(status=2)

    def save_result(self):
        """
        保存测试结果到数据库
        """
        # 打开xml文档
        dom = parse(REPORT_PATH)
        # 得到文档元素对象
        root = dom.documentElement
        # 获取(一组)标签
        testsuite = root.getElementsByTagName('testsuite')
        errors = testsuite[0].getAttribute("errors")
        failures = testsuite[0].getAttribute("failures")
        name = testsuite[0].getAttribute("name")
        skipped = testsuite[0].getAttribute("skipped")
        tests = testsuite[0].getAttribute("tests")
        run_time = testsuite[0].getAttribute("time")

        f = open(REPORT_PATH, "r", encoding="utf-8")
        result = f.read()
        f.close()

        TestResult.objects.create(
            task_id=self.tid,
            name=name,
            error=int(errors),
            failure=int(failures),
            skipped=int(skipped),
            tests=int(tests),
            run_time=float(run_time),
            result=result
        )

    def run_tasks(self):
        print("创建线程任务...")
        sleep(2)
        threads = []
        t1 = threading.Thread(target=self.run_cases)
        threads.append(t1)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_tasks)
        threads.append(t)

        for t in threads:
            t.start()


if __name__ == '__main__':
    print("开始")
    # run()  # 丢给线程去运行任务
    TaskThread(1, [1, 2]).run()
    print("结束")
    #上班 ....
    #（下班）接孩子