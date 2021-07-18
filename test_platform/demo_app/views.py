from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.  非常重要一部分：拿到请求 ，处理， 返回接过
def hello(request):
    print(request.scheme)
    print(request.body)
    print(request.method)
    if request.method == "GET":
        return render(request, "demo_app/hello.html")
    if request.method == "POST":
        user = request.POST.get("username")
        pswd = request.POST.get("password")
        print(user, pswd)
        if user == "admin" and pswd == "admin123456":
            return render(request, "demo_app/hello.html", {"hint": "登录成功"})
            # return JsonResponse({"success": True, "message": "登录成功"})
        else:
            # return JsonResponse({"success": False, "message": "登录失败"})
            return render(request, "demo_app/hello.html", {"hint": "登录失败"})


def calculator(request):
    """
    计算器
    """
    if request.method == "GET":
        return render(request, "demo_app/calculator.html")
    if request.method == "POST":
        a = request.POST.get("number_a")
        b = request.POST.get("number_b")
        count = int(a) + int(b)
        return render(request, "demo_app/calculator.html", {"result": count})
