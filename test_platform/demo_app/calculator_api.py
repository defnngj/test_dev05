from django.http import JsonResponse


def add(request):
    """
    计算加法
    """
    if request.method == "POST":
        a = request.POST.get("number_a", "")
        b = request.POST.get("number_b", "")
        print("ab", a, b)
        if a == "" or b == "":
            return JsonResponse({"success": False, "message": "参数错误"})
        count = int(a) + int(b)
        return JsonResponse({"success": True, "message": "", "data": {"count": count}})
    else:
        return JsonResponse({"success": False, "message": "请求方法错误"})
