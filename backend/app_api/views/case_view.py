import requests
import json
from rest_framework.decorators import action
from app_common.utils.base_view import BaseViewSet
from app_common.utils.pagination import Pagination
from app_api.serializer.case import CaseValidator, CaseSerializer, DebugValidator
from app_api.models import TestCase


class CaseViewSet(BaseViewSet):
    queryset = TestCase.objects.all()
    authentication_classes = []

    @action(methods=["get"], detail=True, url_path="info")
    def get_case_info(self, request, *args, **kwargs):
        """
        获取一条用例信息
        api/v1/case/<case_id>/info
        """
        cid = kwargs.get("pk")
        try:
            case = TestCase.objects.get(pk=cid, is_delete=False)
            ser = CaseSerializer(instance=case, many=False)
        except TestCase.DoesNotExist:
            return self.response(error=self.CASE_OBJECT_NULL)
        return self.response(data=ser.data)

    @action(methods=["get"], detail=False, url_path="list")
    def get_cases_list(self, request, *args, **kwargs):
        """
        获取用例列表
        api/v1/case/list
        """
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        cases = TestCase.objects.filter(is_delete=False).all()
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=cases, request=request, view=self)
        ser = CaseSerializer(instance=page_data, many=True)
        data = {
            "total": len(cases),
            "page": int(page),
            "size": int(size),
            "caseList": ser.data
        }
        return self.response(data=data)

    @action(methods=["post"], detail=False, url_path="create")
    def create_case(self, request, *args, **kwargs):
        """
        创建一条用例
        api/v1/case/create
        """
        val = CaseValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response()

    @action(methods=["put"], detail=True, url_path="update")
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        api/v1/case/<pk>/update
        """
        return self.response()

    @action(methods=["delete"], detail=True, url_path="delete")
    def delete_case(self, request, *args, **kwargs):
        """
        删除一条用例
        api/v1/case/<pk>/delete
        """
        return self.response()

    @action(methods=["post"], detail=False, url_path="debug")
    def debug_case(self, request, *args, **kwargs):
        """
        调试一个接口用例
        api/v1/case/debug/
        """
        val = DebugValidator(data=request.data)
        if val.is_valid() is False:  # 判断验证的字段是否都对
            return self.response_fail(error=val.errors)
        url = request.data.get("url")
        method = request.data.get("method")
        header = request.data.get("header", "")
        params_type = request.data.get("params_type")
        params_body = request.data.get("params_body", "")
        if header == "":
            header = {}
        else:
            try:
                header = json.loads(header)
            except json.decoder.JSONDecodeError:
                return self.response(error=self.CASE_HEADER_ERROR)

        if params_body == "":
            params_body = {}
        else:
            try:
                params_body = json.loads(params_body)
            except json.decoder.JSONDecodeError:
                return self.response(error=self.CASE_PARAMS_BODY_ERROR)

        ret_text = "null"
        if method == "GET":
           ret_text = requests.get(url, headers=header, params=params_body)

        if method == "POST":
            if params_type == "data":
                ret_text = requests.post(url, headers=header, data=params_body)
            if params_type == "json":
                ret_text = requests.post(url, headers=header, json=params_body)

        return self.response(data=ret_text)


    @action(methods=["post"], detail=False, url_path="assert")
    def assert_case(self, request, *args, **kwargs):
        """
        删除一条用例
        api/v1/case/assert/
        """
        return self.response()

    @action(methods=["get"], detail=False, url_path="tree")
    def get_case_tree(self, request, *args, **kwargs):
        """
        获取用例的树：项目-> 模型 -> 用例
        api/v1/case/<case_id>/
        """
        print(request)
        print(args)
        print(kwargs)
        return self.response()




