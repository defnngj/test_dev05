import json
from rest_framework import serializers
from app_api.models import TestCase, TestTask, TaskCaseRelevance, TestResult
from app_api.serializer.config import CaseDataList
from app_common.utils.base_serializer import check_json


class ResultSerializer(serializers.ModelSerializer):
    """
    测试任务序列化
    """
    # cases = serializers.SerializerMethodField()  # 反向获取模块的名称
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化
    task_name = serializers.CharField(source="task.name")  # 反向获取模块的名称

    class Meta:
        model = TestResult
        fields = ['id', 'name', 'error', 'failure', 'skipped', 'tests',
                  'run_time', 'task_name', 'result', 'create_time']   # 要显示的字段
