import json
from rest_framework import serializers
from app_api.models import TestCase, TestTask
from app_api.serializer.config import CaseDataList
from app_common.utils.base_serializer import check_json


class CaseSerializer(serializers.ModelSerializer):
    """
    测试用例序列化
    """
    module_name = serializers.CharField(source="module.name")  # 反向获取模块的名称

    class Meta:
        model = TestCase
        fields = ['name', 'url', 'method', 'header', 'params_type', 'params_body',
                  'result', 'assert_type', 'assert_text', 'module_id', "module_name"]  # 要显示的字段


class TaskValidator(serializers.Serializer):
    """
    创建任务的验证器
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", null=True, default="")
    status = models.IntegerField("状态", default=0)  # 未执行、执行中、执行完成、排队中
    cases = models.TextField("关联用例", default="")  # "[1,2,3,4]"
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    describe = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)
    cases = serializers.CharField(required=True, error_messages={"required": "case不能为空"})

    def create(self, validated_data):
        """
        创建用例
        """
        task = TestTask.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        instance.url = validated_data.get('url')
        instance.method = validated_data.get('method')
        instance.header = validated_data.get('header')
        instance.params_type = validated_data.get('params_type')
        instance.params_body = validated_data.get('params_body')
        instance.result = validated_data.get('result')
        instance.assert_type = validated_data.get('assert_type')
        instance.assert_text = validated_data.get('assert_text')
        instance.module_id = validated_data.get('module_id')
        instance.name = validated_data.get('name')
        instance.save()
        return instance


