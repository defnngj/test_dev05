import os
import json
import unittest
import requests
import xmlrunner
from ddt import ddt, data, file_data, unpack

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# DATA_FILE_PATH = os.path.join(BASE_DIR, "api", "data", "test_data.json")
DATA_FILE_PATH = os.path.join(TEST_DIR, "data", "test_data.json")
REPORT_FILE_PATH = os.path.join(TEST_DIR, "data", "report.xml")


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


def json_to_dict(json_str):
    """
    json to dict
    """
    if json_str == "":
        ret = dict()
        return ret

    try:
        ret = json.loads(json_str)
        if isinstance(ret, dict) is False:
            return None
    except json.decoder.JSONDecodeError as e:
        print("error", e)
        return None
    return ret


@ddt
class MyTest(unittest.TestCase):
    """
    "url": "http://httpbin.org/get",
    "method": "GET",
    "header": "{}",
    "params_type": "",
    "params_body": "{}",
    "assert_type": "include",
    "assert_text": "httpbin.org"
    """
    @file_data(DATA_FILE_PATH)
    def test_case(self, url, method, header, params_type, params_body, assert_type, assert_text):
        print("url", url)
        print("method", method)
        print("header", header)
        print("params_type", params_type)
        print("params_body", params_body)
        print("assert_type", assert_type)
        print("assert_text", assert_text)

        header = json_to_dict(header)
        if header is None:
            header = {}

        params_body = json_to_dict(params_body)
        if params_body is None:
            params_body = {}

        if method == MethodType.get:
            ret_text = requests.get(url, headers=header, params=params_body)
            if assert_type == AssertType.include:
                self.assertIn(assert_text, ret_text)
            elif assert_type == AssertType.equal:
                self.assertEqual(assert_text, ret_text)
            else:
                pass

        if method == MethodType.post:
            if params_type == ParamsType.data:
                ret_text = requests.post(url, headers=header, data=params_body)
                if assert_type == AssertType.include:
                    print("ret_text--->", ret_text)
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass
            if params_type == ParamsType.json:
                ret_text = requests.post(url, headers=header, json=params_body)
                if assert_type == AssertType.include:
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass

        if method == MethodType.put:
            if params_type == ParamsType.data:
                ret_text = requests.put(url, headers=header, data=params_body)
                if assert_type == AssertType.include:
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass

            if params_type == ParamsType.json:
                ret_text = requests.put(url, headers=header, json=params_body)
                if assert_type == AssertType.include:
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass

        if method == MethodType.delete:
            if params_type == ParamsType.data:
                ret_text = requests.delete(url, headers=header, data=params_body)
                if assert_type == AssertType.include:
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass
            if params_type == ParamsType.json:
                ret_text = requests.delete(url, headers=header, json=params_body)
                if assert_type == AssertType.include:
                    self.assertIn(assert_text, ret_text)
                elif assert_type == AssertType.equal:
                    self.assertEqual(assert_text, ret_text)
                else:
                    pass


if __name__ == '__main__':
    with open(REPORT_FILE_PATH, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


