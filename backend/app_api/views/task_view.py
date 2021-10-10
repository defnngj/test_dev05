import os
import json
import requests
from rest_framework.decorators import action
from app_common.utils.base_view import BaseViewSet
from app_common.utils.pagination import Pagination
from app_api.serializer.task import TaskValidator
from app_api.models import Project, Module, TestTask, TestCase, TestResult
from app_api.serializer.config import AssertType, MethodType, ParamsType
from app_api.tasks import running
from app_common.utils.response import Error
from backend.settings import BASE_DIR


DATA_FILE_PATH = os.path.join(BASE_DIR, "app_api", "data", "test_data.json")


class TaskViewSet(BaseViewSet):
    queryset = TestTask.objects.all()
    authentication_classes = []

    @action(methods=["post"], detail=False, url_path="create")
    def create_task(self, request, *args, **kwargs):
        """
        创建一条用例
        api/v1/case/create
        """
        cases = request.data.get("cases")
        print("cases", cases)
        if isinstance(cases, list) is True:
            if len(cases) == 0:
                return self.response(error=Error.CASE_HEADER_ERROR)
            else:
                request.data["cases"] = str(cases)
        else:
            return self.response(error=Error.CASE_HEADER_ERROR)

        val = TaskValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response()

    @action(methods=["get"], detail=True, url_path='running')
    def get_running(self, request, *args, **kwargs):
        """
        运行测试任务
        /api/interface/v1/task/<pk>/running/

        todo:
        1.记录任务状态
        2.读取xml文件的内容，写入表
        """
        pk = kwargs.get("pk")
        if pk is not None:
            try:
                task = TestTask.objects.get(id=pk, is_delete=False)
            except TestTask.DoesNotExist:
                return self.response(error=Error.TASK_ID_NULL)
            print("case list--> ", task.cases)
            b = task.cases.replace("]", "")
            c = b.replace("[", "")
            case_list = c.split(",")

            print("case list-->", case_list)
            cases_dict = {}
            for case in case_list:
                case = TestCase.objects.get(id=int(case))
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

        running.delay()
        return self.response()




