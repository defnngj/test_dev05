from rest_framework import serializers
from app_api.models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # 日期格式化

    class Meta:
        model = Project
        fields = ['id', 'name', 'describe', 'status', 'create_time']  # 要显示的字段


class ProjectValidator(serializers.Serializer):
    """
    项目的验证器
    """
    name = serializers.CharField(required=True, max_length=50,
                                 error_messages={"required": "name不能为空",
                                                 "invalid": "类型不对",
                                                 "max_length": "长度不能大于50"})
    describe = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)

    # def validate_name(self, value):
    #     """ 验证项目名称不能重复 """
    #     project = Project.objects.filter(name=value).count()
    #     if project > 0:
    #         raise serializers.ValidationError("项目名称已经存在")
    #     return value

    def create(self, validated_data):
        """
        创建
        """
        project = Project.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        """
        更新
        instance - 更新的对象 - 从数据库里查出来的
        validated_data - 更新的数据 - 从request 里面
        """
        instance.name = validated_data.get("name")
        instance.describe = validated_data.get("describe")
        instance.status = validated_data.get("status")
        instance.save()
        return instance



















