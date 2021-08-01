from django.http import JsonResponse


def hello(request):
    return JsonResponse({"code": 10200, "message": "Welcome to API testing"})


def one_add(request):
    return JsonResponse({"code": 10200, "data": {"age": 22, "id": 1, "name": "tom"}, "message": "success"})