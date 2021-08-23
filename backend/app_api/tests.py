from django.test import TestCase

# Create your tests here.

from random import randint

import requests

for i in range(20):
    data = {
        "name": "接口项目"+str(i),
        "describe": "描述信息"+str(i),
        "status": True
    }
    r = requests.post("http://127.0.0.1:8000/api/v1/project/", json=data)
    print(r.json())

