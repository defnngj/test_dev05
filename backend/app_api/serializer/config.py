"""
所有常量配置文件
"""


class AssertType:
    """断言类型"""
    include = "include"
    equal = "equal"


class MethodType:
    """http请求方法"""
    post = "POST"
    get = "GET"
    delete = "DELETE"
    put = "PUT"


class ParamsType:
    """请求类型"""
    params = "params"
    data = "data"
    json = "json"


class CaseDataList:
    methods = [MethodType.get, MethodType.post, MethodType.delete, MethodType.put]
    params_type = [ParamsType.params, ParamsType.data, ParamsType.json]
    assert_type = [AssertType.include, AssertType.equal]
