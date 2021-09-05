from rest_framework import serializers
from app_api.models import TestCase


class CaseData:
    methods = ["POST", "GET", "DELETE", "PUT"]
    params_type = ["params", "data", "json"]
    assert_type = ["include", "equal"]


class CaseSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source="module.name")  # 反向获取模块的名称

    class Meta:
        model = TestCase
        fields = ['name', 'url', 'method', 'header', 'params_type', 'params_body',
                  'result', 'assert_type', 'assert_text', 'module_id', "module_name"]  # 要显示的字段
        # fields = "__all__"


class CaseValidator(serializers.Serializer):
    """
    用例的验证器
    """
    module_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    url = serializers.CharField(required=True, error_messages={"required": "url不能为空"})
    method = serializers.ChoiceField(required=True, choices=CaseData.methods,
                                     error_messages={"required": "method不能为空",
                                                     "invalid_choice": "只支持GET/POST/DELETE/PUT类型"})

    header = serializers.JSONField(required=True, error_messages={"required": "header不能为空，而且JSON格式"})
    params_type = serializers.ChoiceField(required=True, choices=CaseData.params_type,
                                          error_messages={"required": "params_type不能为空",
                                                          "invalid_choice": "只支持params/form/json类型"})
    params_body = serializers.CharField(required=True, error_messages={"required": "params_body不能为空，而且JSON格式"})
    result = serializers.CharField(required=True, error_messages={"required": "result不能为空"})
    assert_type = serializers.ChoiceField(required=True, choices=CaseData.assert_type,
                                          error_messages={"required": "assert_type不能为空",
                                                          "invalid_choice": "只支持include/equal类型"})
    assert_text = serializers.CharField(required=True, error_messages={"required": "assert_text不能为空"})

    def create(self, validated_data):
        """
        创建
        """
        project = TestCase.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        # instance.name = validated_data.get("name")
        # instance.describe = validated_data.get("describe")
        # instance.project_id = validated_data.get("project_id")
        instance.save()
        return instance


class DebugValidator(serializers.Serializer):
    """
    用例调试的验证器
    """

    url = serializers.CharField(required=True, error_messages={"required": "url不能为空"})
    method = serializers.ChoiceField(required=True, choices=CaseData.methods,
                                     error_messages={"required": "method不能为空",
                                                     "invalid_choice": "只支持GET/POST/DELETE/PUT类型"})
    header = serializers.JSONField(required=True, error_messages={"required": "header不能为空，而且JSON格式"})
    params_type = serializers.ChoiceField(required=True, choices=CaseData.params_type,
                                          error_messages={"required": "params_type不能为空",
                                                          "invalid_choice": "只支持params/form/json类型"})
    params_body = serializers.CharField(required=True, error_messages={"required": "params_body不能为空，而且JSON格式"})


