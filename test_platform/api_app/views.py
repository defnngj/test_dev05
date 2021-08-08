import os
import json
import base64
from django.http import JsonResponse
from test_platform.settings import BASE_DIR

UPLOAD = os.path.join(BASE_DIR, "api_app", "upload")

class Number:
    num = 0


def ping(request):
    """
    测试 api  json = dict
    """
    return JsonResponse({"code": 10200, "message": "Welcome to API testing"})


def add_one(request):
    """
    累加器
    """
    Number.num += 1
    return JsonResponse({"code": 10200, "data": {"number": Number.num}, "message": "success"})


def get_user(request, uid):
    """
    GET /user/1/
    """
    if uid != 1:
        return JsonResponse({"code": 10101, "message": "user id null"})

    data = {"age": 22, "id": 1, "name": "tom"}
    return JsonResponse({"code": 10200, "data": data, "message": "success"})


def get_user2(request):
    """
    GET /user?uid=1
    """
    # uid = request.GET["uid"]
    uid = request.GET.get("uid", "")
    if uid == "":
        return JsonResponse({"code": 10101, "message": "user id null"})

    data = {"age": 22, "id": 1, "name": "tom"}
    return JsonResponse({"code": 10200, "data": data, "message": "success"})


def user_login(request):
    """
    POST
    * form-data VS x-www-form-urlencode
    """
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    print(type(password))
    if username == "" or password == "":
        return JsonResponse({"code": 10103, "message": "username or password is null"})

    if username != "admin" or password != "123":
        return JsonResponse({"code": 10104, "message": "username or password error"})

    return JsonResponse({"code": 10200, "message": "login success"})


def add_user(request):
    """ json byte str dict list
    POST : raw(postman) ==> b''  /HTML/JSON/Text/JS/XML...
    """
    text = request.body
    text_str = str(text, encoding="utf8")
    text_dict = json.loads(text_str)

    uid = text_dict.get("id")
    name = text_dict.get("name")
    user = {
        "id": uid,
        "name": name
    }
    return JsonResponse({"code": 10200,
                         "message": "add successful",
                         "data": user})


def header(request):
    """
    Header
    """
    token = request.headers.get("token", "")
    print(token)
    if token == "":
        return JsonResponse({"code": 10102,
                             "message": "token is null"})

    return JsonResponse({"code": 10200,
                         "message": "successful"})


def auth(request):
    """
    auth Basic
    """
    auth_str = request.headers.get("Authorization", "")
    if auth_str == "":
        return JsonResponse({"code": 10102,
                             "message": "auth is null"})

    auth_ = auth_str.split(" ")[1]
    auth_user = base64.b64decode(auth_).decode("utf8")
    user = auth_user.split(":")[0]
    pawd = auth_user.split(":")[1]

    if user != "admin" or pawd != "admin123456":
        return JsonResponse({"code": 10104, "message": "auth fail"})

    return JsonResponse({"code": 10200, "message": "auth success"})


FILE_TYPE = ["csv", "txt", "gif", "jpg", "jpeg"]


def upload(request):
    print(request.FILES)
    file = request.FILES["file"]
    print(type(file))
    print(type(file.name))
    file_name = file.name
    file_type = file_name.split(".")[-1]

    print(file.size)

    if file_type not in FILE_TYPE:
        return JsonResponse({"code": 10200, "message": "file type error"})
    if file.size > 1048576:
        return JsonResponse({"code": 10200, "message": "File size greater than 1MB"})

    with(open(os.path.join(UPLOAD,  file.name), 'wb')) as f:
        for chunk in file.chunks():
            f.write(chunk)

    return JsonResponse({"code": 10200, "message": "success"})







