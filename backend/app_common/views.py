from django.contrib.auth.models import User, Group
from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from app_common.utils.response import response, Error


class LoginView(APIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def post(self, request):
        """
        登录账号，并获取token
        """
        login_username = request.POST.get("username", "")
        login_password = request.POST.get("password", "")
        print(login_password, login_username)
        if login_username == '' or login_password == '':
            return response(error=Error.USER_OR_PAWD_NULL)
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            print(user)
            if user is not None and user.is_active:
                auth.login(request, user)  # 验证登录
                # update the token
                token = Token.objects.filter(user=user)
                token.delete()
                token = Token.objects.create(user=user)
                return response(data={"Token": str(token)})
            else:
                return response(error=Error.USER_OR_PAWD_ERROR)

    def delete(self, request):
        """
        退出账号，并删除token
        """
        userId = request.POST.get("user")
        token = Token.objects.filter(user=userId)
        token.delete()
        return response()













