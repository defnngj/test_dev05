from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from app_api.models.project_model import Project
from app_api.serializer.project import ProjectValidator, ProjectSerializer
from app_common.utils.pagination import Pagination


class ProjectView(APIView):

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        pid = kwargs.get("pk")
        if pid is not None:  # 查询单条数据
            try:
               project = Project.objects.get(pk=pid, is_delete=False)
               print("project object", project)
               ser = ProjectSerializer(instance=project, many=False)
            except Project.DoesNotExist:
                return JsonResponse({"meg": "project object is null"})
            return JsonResponse({"msg": "查询", "data": ser.data})
        else:   # 查询一组数据
            project = Project.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ProjectSerializer(instance=page_data, many=True)
            return JsonResponse({"msg": "查询", "data": ser.data})

    def post(self, request, *args, **kwargs):
        """
        添加项目
        """
        val = ProjectValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return JsonResponse({"msg": "添加", "error": val.errors})
        return JsonResponse({"msg": "添加成功"})

    def put(self, request, *args, **kwargs):
        """
        更新
        """
        pid = kwargs.get("pk")
        if pid is None:
            pid = request.data.get("id", "")
            if pid == "":
               return JsonResponse({"meg": "project id is null"})
        try:
           project = Project.objects.get(pk=pid, is_delete=False)
        except Project.DoesNotExist:
            return JsonResponse({"meg": "project object is null"})
        # 更新
        val = ProjectValidator(instance=project, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return JsonResponse({"msg": "添加", "error": val.errors})

        return JsonResponse({"msge": "更新"})

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        pid = kwargs.get("pk")
        if pid is not None:  # 查询单条数据
            project = Project.objects.filter(pk=pid, is_delete=False).update(is_delete=True)
            if project == 0:
                return JsonResponse({"msge": "删除失败"})

        return JsonResponse({"msge": "删除成功"})



















