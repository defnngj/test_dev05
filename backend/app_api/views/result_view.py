import os
import json
import requests
from rest_framework.decorators import action
from app_common.utils.base_view import BaseViewSet
from app_common.utils.pagination import Pagination
from app_api.serializer.task import TaskValidator, TaskSerializer
from app_api.serializer.result import ResultSerializer
from app_api.models import Project, Module, TestTask, TestCase, TestResult, TaskCaseRelevance
from app_api.serializer.config import AssertType, MethodType, ParamsType
from app_api.tasks import running
from app_common.utils.response import Error
from backend.settings import BASE_DIR
from app_api.task_thread import TaskThread


DATA_FILE_PATH = os.path.join(BASE_DIR, "app_api", "data", "test_data.json")


class ResultViewSet(BaseViewSet):
    queryset = TestTask.objects.all()
    # authentication_classes = []

    @action(methods=["get"], detail=True, url_path="info")
    def get_result_info(self, request, *args, **kwargs):
        """
        获取一条结果信息
        api/v1/case/<result_id>/info
        """
        rid = kwargs.get("pk")
        try:
            result = TestResult.objects.get(pk=rid)
            ser = ResultSerializer(instance=result, many=False)
        except TestTask.DoesNotExist:
            return self.response_success(error=self.RESULT_ID_NULL)
        return self.response_success(data=ser.data)

    @action(methods=["get"], detail=False, url_path="list")
    def get_result_list(self, request, *args, **kwargs):
        """
        获取结果列表
        api/v1/result/list
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        tid = request.query_params.get("taskId", "")
        if tid == "":
            print("null string ", tid)
            results = TestResult.objects.filter().all()
        else:
            print("number", tid)
            results = TestResult.objects.filter(task_id=tid).all()
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=results, request=request, view=self)
        ser = ResultSerializer(instance=page_data, many=True)
        data = {
            "total": len(results),
            "page": int(page),
            "size": int(size),
            "resultList": ser.data
        }
        return self.response_success(data=data)

    @action(methods=["delete"], detail=True, url_path="delete")
    def delete_task(self, request, *args, **kwargs):
        """
        删除一条结果
        api/v1/result/<pk>/delete
        """
        pk = kwargs.get("pk")
        if pk is None:
            return self.response_success(error=self.TASK_ID_NULL)
        result = TestResult.objects.filter(id=pk).delete()
        if result == 0:
            return self.response_success(error=self.RESULT_ID_NULL)

        return self.response_success()

