from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from api_app.serializer import UserSerializer


# 视图类
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # users = User.objects.all()
    # users_list = []
    # for user in users:
    #     user_dict = {
    #         "url": "http://127.0.0.1/users/"+ user.id + "/",
    #         "username": user.username,
    #         "email": user.email,
    #     }
    #     users_list.append(user_dict)
    #
    # return JsonResponse({"userlist":users_list})

