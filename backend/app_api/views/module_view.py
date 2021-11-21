from app_api.models import Module
from app_api.serializer.module import ModuleValidator, ModuleSerializer
from app_common.utils.pagination import Pagination
from app_common.utils.base_view import BaseAPIView


class ModuleView(BaseAPIView):

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        mid = kwargs.get("pk")
        page = request.query_params.get("page", "1")
        size = request.query_params.get("size", "5")
        if mid is not None:  # 查询单条数据
            try:
               module = Module.objects.get(pk=mid, is_delete=False)
               ser = ModuleSerializer(instance=module, many=False)
            except Module.DoesNotExist:
                return self.response_success(error=self.MODULE_OBJECT_NULL)
            return self.response_success(data=ser.data)
        else:   # 查询一组数据
            project = Module.objects.filter(is_delete=False).all()
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ModuleSerializer(instance=page_data, many=True)
            data = {
                "total": len(project),
                "page": int(page),
                "size": int(size),
                "moduleList": ser.data
            }
            return self.response_success(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加
        /module/abc/
        """
        val = ModuleValidator(data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    def put(self, request, *args, **kwargs):
        """
        更新
        """
        pid = kwargs.get("pk")
        if pid is None:
            pid = request.data.get("id", "")
            if pid == "":
                return self.response_success(error=self.MODULE_ID_NULL)
        try:
           module = Module.objects.get(pk=pid, is_delete=False)
        except Module.DoesNotExist:
            return self.response_success(error=self.MODULE_OBJECT_NULL)
        # 更新
        val = ModuleValidator(instance=module, data=request.data)
        if val.is_valid():  # 判断验证的字段是否都对
            val.save()  # 保存这个数据
        else:
            return self.response_fail(error=val.errors)
        return self.response_success()

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        mid = kwargs.get("pk")
        if mid is not None:  # 查询单条数据

            module = Module.objects.filter(pk=mid, is_delete=False).update(is_delete=True)
            if module == 0:
                return self.response_success(error=self.MODULE_DELETE_ERROR)

        return self.response_success()


class ModuleTreeView(BaseAPIView):

    def get(self, request,  *args, **kwargs):
        """
        获取模块树：项目->模块
        """















