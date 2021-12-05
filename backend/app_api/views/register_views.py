import json
from django.contrib.auth.models import User, Group
from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from app_common.utils.response import response_success, Error


class RegisterView(APIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def post(self, request):
        """
        登录账号，并获取token
        """
        username = request.data.get("username", "")
        password1 = request.data.get("password1", "")
        password2 = request.data.get("password2", "")

        if username == '' or password1 == '' or password2 == '':
            return response_success(error=Error.USER_OR_PAWD_NULL)
        elif password1 != password2:
            return response_success(error=Error.PAWD_ERROR)
        else:
            user = User.objects.create_user(username=username, password=password1)
            return response_success()





