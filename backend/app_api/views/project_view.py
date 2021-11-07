from django.shortcuts import render
from django.http import JsonResponse
# from rest_framework.views import APIView
from app_api.models.project_model import Project
from app_api.serializer.project import ProjectValidator, ProjectSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import BaseAPIView
from app_common.utils.response import response, Error
from app_common.utils.token_auth import TokenAuthentication


class ProjectView(BaseAPIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        pid = kwargs.get("pk")
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        if pid is not None:  # 查询单条数据
            try:
               project = Project.objects.get(pk=pid, is_delete=False)
               ser = ProjectSerializer(instance=project, many=False)
            except Project.DoesNotExist:
                # return response(error=Error.PROJECT_OBJECT_NULL)

                return self.response(error=self.PROJECT_OBJECT_NULL)
            return self.response(data=ser.data)
        else:   # 查询all数据
            project = Project.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ProjectSerializer(instance=page_data, many=True)
            data = {
                "total": len(project),
                "page": int(page),
                "size": int(size),
                "projectList": ser.data
            }
            return self.response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加项目
        """
        val = ProjectValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response()

    def put(self, request, *args, **kwargs):
        """
        更新
        """
        pid = kwargs.get("pk")
        if pid is None:
            pid = request.data.get("id", "")
            if pid == "":
                return self.response(error=self.PROJECT_ID_NULL)
        try:
           project = Project.objects.get(pk=pid, is_delete=False)
        except Project.DoesNotExist:
            return self.response(error=self.PROJECT_OBJECT_NULL)
        # 更新
        val = ProjectValidator(instance=project, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response()

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        pid = kwargs.get("pk")
        if pid is not None:  # 查询单条数据
            project = Project.objects.filter(pk=pid, is_delete=False).update(is_delete=True)
            if project == 0:
                return self.response(error=self.PROJECT_DELETE_ERROR)

        return self.response()




















