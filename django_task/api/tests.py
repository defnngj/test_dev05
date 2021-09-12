import os
import unittest
import requests
import xmlrunner
from ddt import ddt, data, file_data, unpack
# from django_task.settings import BASE_DIR

TEST_DIR  = os.path.dirname(os.path.abspath(__file__))

# DATA_FILE_PATH = os.path.join(BASE_DIR, "api", "data", "test_data.json")
DATA_FILE_PATH = os.path.join(TEST_DIR, "data", "test_data.json")
REPORT_FILE_PATH = os.path.join(TEST_DIR, "data", "report.xml")


@ddt
class MyTest(unittest.TestCase):

    #@unpack
    # @data(
    #     {'url': "http://httpbin.org/post", 'method': "POST", 'params_type': "json", 'params_body': {"id": 11}},
    #     {'url': "http://httpbin.org/post", 'method': "POST", 'params_type': "data", 'params_body': {"name": "tom"}},
    #     {'url': "https://httpbin.org/get", 'method': "GET",  'params_type': "params", 'params_body': {"key": "value"}}
    # )
    @file_data(DATA_FILE_PATH)
    def test_case(self, url, method, params_type, params_body):
        # print("url", url)
        # print("method", method)
        # print("params_body", params_body)
        if method == "GET":
            r = requests.get(url, params=params_body)
        elif method == "POST":
            if params_type == "json":
                r = requests.post(url, json=params_body)
            elif params_type == "data":
                r = requests.post(url, data=params_body)
            else:
                r = "{}"
        else:
            r = "{}"
        # print(r.json())


if __name__ == '__main__':
    with open(REPORT_FILE_PATH, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


