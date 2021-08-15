from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'  # 所有的字段
        fields = ['username', 'email', 'is_staff']  # 要显示的字段
        # exclude = ['users']  # 不要显示的字段
