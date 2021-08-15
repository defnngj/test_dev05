from rest_framework import serializers
from django.contrib.auth.models import User


# 序列化
# 1.验证入参的参数
# 2.指定了返回的数据
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

