from rest_framework.response import Response


class Error:
    """
    子定义错误码与错误信息
    """
    USER_OR_PAWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}

    ParamsTypeError = {"30020": "参数类型错误"}
    JSON_TYPE_ERROR = {"30030": "JSON格式错误"}

    USER_ID_NULL = {"40010": "用户id不存在"}

    PROJECT_ID_NULL = {"10020": "项目id不存在"}
    PROJECT_OBJECT_NULL = {"10021": "通过id查询项目不存在"}
    PROJECT_DELETE_ERROR = {"10023": "项目删除失败"}

    MODULE_ID_NULL = {"10030": "模块id不存在"}
    MODULE_OBJECT_NULL = {"10031": "模块对象不存在"}
    MODULE_DELETE_ERROR = {"10032": "模块删除失败"}

    CASE_ID_NULL = {"10040": "用例id不存在"}
    CASE_OBJECT_NULL = {"10041": "通过id查询用例不存在"}
    CASE_HEADER_ERROR = {"10042": "header类型错误，不是json"}
    CASE_PARAMS_BODY_ERROR = {"10043": "params_body类型错误，不是json"}
    ASSERT_INCLUDE_FAIL = {"10044": "断言包含失败"}
    ASSERT_EQUAL_FAIL = {"10045": "断言相等失败"}

    TASK_ID_NULL = {"10051", "task ID不存在"}
    TASK_OBJECT_NULL = {"10041": "通过id查询任务不存在"}

    RESULT_ID_NULL = {"10061", "task ID不存在"}
    RESULT_OBJECT_NULL = {"10061": "通过id查询任务不存在"}


def response_fail(error=""):
    """
    返回失败, 主要用于参数验证失败
    """
    error_msg = {
        "30010": str(error)
    }
    return response_success(success=False, error=error_msg, result=[])


def response_success(success: bool = True, error={}, data: any = []) -> Response:
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
    return Response(resp)

