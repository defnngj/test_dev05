import requests
from rest_framework.decorators import action
from app_common.utils.base_view import BaseViewSet
from app_common.utils.pagination import Pagination
from app_api.serializer.case import CaseValidator, CaseSerializer, DebugValidator, AssertValidator
from app_api.models import Project, Module, TestCase
from app_api.serializer.config import AssertType, MethodType, ParamsType


class CaseViewSet(BaseViewSet):
    queryset = TestCase.objects.all()
    # authentication_classes = []

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
            return self.response_success(error=self.CASE_OBJECT_NULL)
        return self.response_success(data=ser.data)

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
        return self.response_success(data=data)

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
        return self.response_success()

    @action(methods=["put"], detail=True, url_path="update")
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        api/v1/case/<pk>/update
        """
        cid = request.data.get("id")
        if cid is None:
            return self.response_success(error=self.CASE_ID_NULL)
        case = TestCase.objects.get(pk=cid, is_delete=False)
        val = CaseValidator(instance=case, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(val.errors)

        return self.response_success(data=val.data)

    @action(methods=["delete"], detail=True, url_path="delete")
    def delete_case(self, request, *args, **kwargs):
        """
        删除一条用例
        api/v1/case/<pk>/delete
        """
        pk = kwargs.get("pk")
        if pk is None:
            return self.response_success(error=self.CASE_ID_NULL)
        case = TestCase.objects.filter(id=pk, is_delete=False).update(is_delete=True)
        if case == 0:
            return self.response_success(error=self.CASE_OBJECT_NULL)

        return self.response_success()

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
        header = request.data.get("header", "{}")
        params_type = request.data.get("params_type")
        params_body = request.data.get("params_body", "{}")

        header = self.json_to_dict(header)
        if header is None:
            return self.response_success(error=self.JSON_TYPE_ERROR)

        params_body = self.json_to_dict(params_body)
        if params_body is None:
            return self.response_success(error=self.JSON_TYPE_ERROR)

        ret_text = "null"
        if method == MethodType.get:
            ret_text = requests.get(url, headers=header, params=params_body)

        if method == MethodType.post:
            if params_type == ParamsType.data:
                ret_text = requests.post(url, headers=header, data=params_body)
            if params_type == ParamsType.json:
                ret_text = requests.post(url, headers=header, json=params_body)

        if method == MethodType.put:
            if params_type == ParamsType.data:
                ret_text = requests.put(url, headers=header, data=params_body)
            if params_type == ParamsType.json:
                ret_text = requests.put(url, headers=header, json=params_body)

        if method == MethodType.delete:
            if params_type == ParamsType.data:
                ret_text = requests.delete(url, headers=header, data=params_body)
            if params_type == ParamsType.json:
                ret_text = requests.delete(url, headers=header, json=params_body)

        return self.response_success(data=ret_text)

    @action(methods=["post"], detail=False, url_path="assert")
    def assert_case(self, request, *args, **kwargs):
        """
        断言用例
        api/v1/case/assert/
        """
        val = AssertValidator(data=request.data)
        if val.is_valid() is False:  # 判断验证的字段是否都对
            return self.response_fail(error=val.errors)
        result = request.data.get("result")
        assert_type = request.data.get("assert_type")
        assert_text = request.data.get("assert_text")
        if assert_type == AssertType.include:
            if assert_text in result:
                return self.response_success(message="断言包含成功")
            else:
                return self.response_success(error=self.ASSERT_INCLUDE_FAIL)
        elif assert_type == AssertType.equal:
            if assert_text == result:
                return self.response_success(message="断言相等成功")
            else:
                return self.response_success(error=self.ASSERT_EQUAL_FAIL)

        return self.response_success()

    @action(methods=["get"], detail=False, url_path="tree")
    def get_case_tree(self, request, *args, **kwargs):
        """
        获取用例的树：项目-> 模型 -> 用例
        api/v1/case/tree/
        """
        projects = Project.objects.filter(is_delete=False)
        data = []
        for project in projects:
            print("project", project.name)
            project_info = {
                "label": project.name,
                "children": []
            }

            modules = Module.objects.filter(is_delete=False, project_id=project.id)
            if len(modules) == 0:
                project_info["disabled"] = True
            for module in modules:
                module_info = {
                    "label": module.name,
                    "children": []
                }

                cases = TestCase.objects.filter(is_delete=False, module_id=module.id)
                if len(cases) == 0:
                    module_info["disabled"] = True
                for case in cases:
                    case_info = {
                        "id": case.id,
                        "label": case.name,
                    }
                    module_info["children"].append(case_info)

                project_info["children"].append(module_info)

            data.append(project_info)

        return self.response_success(data=data)
