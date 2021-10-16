import json
from rest_framework import serializers
from app_api.models import TestCase, TestTask, TaskCaseRelevance
from app_api.serializer.config import CaseDataList
from app_common.utils.base_serializer import check_json


class TaskSerializer(serializers.ModelSerializer):
    """
    测试任务序列化
    """
    cases = serializers.SerializerMethodField()  # 反向获取模块的名称

    class Meta:
        model = TestTask
        fields = ['name', 'describe', 'status', 'cases']  # 要显示的字段

    def get_cases(self, testtask_obj):
        """查询task关联的case id list"""
        tcr = TaskCaseRelevance.objects.filter(task=testtask_obj)
        case_list = []
        for i in tcr:
            case_list.append(i.case_id)
        return case_list


class TaskValidator(serializers.Serializer):
    """
    任务的验证器
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    describe = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)
    cases = serializers.ListField(required=True, error_messages={"required": "case不能为空"}, write_only=True)

    def validate_cases(self, value):
        """ 验证cases是否为list格式 """
        if len(value) == 0:
            raise serializers.ValidationError("cases不能为空list")
        return value

    def create(self, validated_data):
        """
        创建任务
        """
        name = validated_data.get('name')
        describe = validated_data.get('describe')
        status = validated_data.get('status', True)
        # 创建关联数据
        task = TestTask.objects.create(name=name, describe=describe, status=status)
        for case in validated_data.get('cases'):
            TaskCaseRelevance.objects.create(task_id=task.id, case_id=case)
        return task

    def update(self, instance, validated_data):
        """
        更新任务
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        instance.name = validated_data.get('name')
        instance.describe = validated_data.get('describe')
        instance.status = validated_data.get('status', True)
        # 删除任务关联数据，重新创建
        TaskCaseRelevance.objects.filter(task_id=instance.id).delete()
        for case in validated_data.get('cases'):
            TaskCaseRelevance.objects.create(task_id=instance.id, case_id=case)
        instance.save()
        return instance
