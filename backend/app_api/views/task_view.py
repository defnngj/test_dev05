import os
import json
import requests
from rest_framework.decorators import action
from app_common.utils.base_view import BaseViewSet
from app_common.utils.pagination import Pagination
from app_api.serializer.task import TaskValidator, TaskSerializer
from app_api.models import Project, Module, TestTask, TestCase, TestResult, TaskCaseRelevance
from app_api.serializer.config import AssertType, MethodType, ParamsType
from app_api.tasks import running
from app_common.utils.response import Error
from backend.settings import BASE_DIR


DATA_FILE_PATH = os.path.join(BASE_DIR, "app_api", "data", "test_data.json")


class TaskViewSet(BaseViewSet):
    queryset = TestTask.objects.all()
    authentication_classes = []

    @action(methods=["get"], detail=True, url_path="info")
    def get_task_info(self, request, *args, **kwargs):
        """
        获取一条任务信息
        api/v1/case/<task_id>/info
        """
        tid = kwargs.get("pk")
        try:
            task = TestTask.objects.get(pk=tid, is_delete=False)
            ser = TaskSerializer(instance=task, many=False)
        except TestTask.DoesNotExist:
            return self.response(error=self.TASK_OBJECT_NULL)
        return self.response(data=ser.data)

    @action(methods=["get"], detail=False, url_path="list")
    def get_task_list(self, request, *args, **kwargs):
        """
        获取任务列表
        api/v1/task/list
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        tasks = TestTask.objects.filter(is_delete=False).all()
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=tasks, request=request, view=self)
        ser = TaskSerializer(instance=page_data, many=True)
        data = {
            "total": len(tasks),
            "page": int(page),
            "size": int(size),
            "taskList": ser.data
        }
        return self.response(data=data)

    @action(methods=["delete"], detail=True, url_path="delete")
    def delete_task(self, request, *args, **kwargs):
        """
        删除一条任务
        api/v1/case/<pk>/delete
        """
        pk = kwargs.get("pk")
        if pk is None:
            return self.response(error=self.TASK_ID_NULL)
        task = TestTask.objects.filter(id=pk, is_delete=False).update(is_delete=True)
        if task == 0:
            return self.response(error=self.TASK_OBJECT_NULL)

        return self.response()

    @action(methods=["post"], detail=False, url_path="create")
    def create_task(self, request, *args, **kwargs):
        """
        创建一条任务
        api/v1/task/create
        """
        val = TaskValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response(data=val.data)

    @action(methods=["put"], detail=False, url_path="update")
    def update_task(self, request, *args, **kwargs):
        """
        更新一条任务
        api/v1/task/update
        """
        tid = request.data.get("id")
        if tid is None:
            return self.response(error=self.CASE_ID_NULL)

        task = TestTask.objects.get(pk=tid, is_delete=False)
        val = TaskValidator(instance=task, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response(data=val.data)

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




