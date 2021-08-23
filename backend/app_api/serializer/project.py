from rest_framework import serializers
from app_api.models.project_model import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']  # 要显示的字段

# aatype = [1, 2, 3]


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
    # aatype = serializers.ChoiceField(choices=aatype)  # 枚举

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



















