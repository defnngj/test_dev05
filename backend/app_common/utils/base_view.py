from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from app_common.utils.response import Error


class BaseResponse:

    def response_fail(self, error=""):
        """
        返回失败, 主要用于参数验证失败
        """
        error_msg = {
            "30010": str(error)
        }
        return self.response(success=False, error=error_msg, data=[])

    @staticmethod
    def response(success: bool = True, error={}, data: any = []) -> Response:
        """
        自定义接口返回格式
        """
        if error == {}:
            error_code = ""
            error_msg = ""
        else:
            success = False
            error_code = list(error.keys())[0]
            error_msg = list(error.values())[0]

        resp = {
            "success": success,
            "error": {
                "code": error_code,
                "message": error_msg
            },
            "data": data
        }
        print("---->", resp)
        return Response(resp)


class BaseAPIView(APIView, BaseResponse, Error):
    """
    继承APIView，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


class BaseViewSet(ViewSet, BaseResponse, Error):
    """
    继承ViewSet，
    Response：自定义返回格式
    Error: 自定义错误信息
    """
    pass


