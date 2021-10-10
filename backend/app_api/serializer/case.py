import json
from rest_framework import serializers
from app_api.models import TestCase
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


class CaseValidator(serializers.Serializer):
    """
    创建用例的验证器
    """
    module_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    url = serializers.CharField(required=True, error_messages={"required": "url不能为空"})
    method = serializers.ChoiceField(required=True, choices=CaseDataList.methods,
                                     error_messages={"required": "method不能为空",
                                                     "invalid_choice": "只支持GET/POST/DELETE/PUT类型"})

    header = serializers.JSONField(required=True, error_messages={"required": "header不能为空，而且JSON格式"})
    params_type = serializers.ChoiceField(required=True, choices=CaseDataList.params_type,
                                          error_messages={"required": "params_type不能为空",
                                                          "invalid_choice": "只支持params/form/json类型"})
    params_body = serializers.CharField(required=True, error_messages={"required": "params_body不能为空，而且JSON格式"})
    result = serializers.CharField(required=True, error_messages={"required": "result不能为空"})
    assert_type = serializers.ChoiceField(required=True, choices=CaseDataList.assert_type,
                                          error_messages={"required": "assert_type不能为空",
                                                          "invalid_choice": "只支持include/equal类型"})
    assert_text = serializers.CharField(required=True, error_messages={"required": "assert_text不能为空"})

    def validate_header(self, value):
        """ 验证header是否为JSON格式 """
        if check_json(value) is False:
            raise serializers.ValidationError("JSON格式错误")
        return value

    def validate_params_body(self, value):
        """ 验证params_body是否为JSON格式 """
        if check_json(value) is False:
            raise serializers.ValidationError("JSON格式错误")
        return value

    def create(self, validated_data):
        """
        创建用例
        """
        case = TestCase.objects.create(**validated_data)
        return case

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


class DebugValidator(serializers.Serializer):
    """
    调试用例验证器
    """

    url = serializers.CharField(required=True, error_messages={"required": "url不能为空"})
    method = serializers.ChoiceField(required=True, choices=CaseDataList.methods,
                                     error_messages={"required": "method不能为空",
                                                     "invalid_choice": "只支持GET/POST/DELETE/PUT类型"})
    header = serializers.JSONField(required=True, error_messages={"required": "header不能为空"})
    params_type = serializers.ChoiceField(required=True, choices=CaseDataList.params_type,
                                          error_messages={"required": "params_type不能为空",
                                                          "invalid_choice": "只支持params/form/json类型"})
    params_body = serializers.JSONField(required=True, error_messages={"required": "params_body不能为空"})


class AssertValidator(serializers.Serializer):
    """
    断言用例验证器
    """

    result = serializers.CharField(required=True, error_messages={"required": "result不能为空"})
    assert_type = serializers.ChoiceField(required=True, choices=CaseDataList.assert_type,
                                          error_messages={"required": "assert_type不能为空",
                                                          "invalid_choice": "只支持include/equal类型"})
    assert_text = serializers.CharField(required=True, error_messages={"required": "assert_text不能为空"})

    def validate_header(self, value):
        """ 验证header是否为JSON格式 """
        if check_json(value) is False:
            raise serializers.ValidationError("JSON格式错误")
        return value

    def validate_params_body(self, value):
        """ 验证params_body是否为JSON格式 """
        if check_json(value) is False:
            raise serializers.ValidationError("JSON格式错误")
        return value
