import json
from django.test import TestCase

# Create your tests here.

# from myapp.models import Animal
from app_api.models import TestTask, Project


class ProjectTest(TestCase):

    def setUp(self):
        Project.objects.create(id=1, name="项目名称1", describe="项目描述")
        Project.objects.create(id=2, name="项目名称2", describe="项目描述")

    def test_project_query(self):
        project = Project.objects.get(id=2)
        self.assertEqual(project.name, "项目名称2")
        projects = Project.objects.filter(name__contains="项目名称")
        self.assertEqual(len(projects), 2)
        for project in projects:
            self.assertIn("项目名称", project.name)

    def test_project_create(self):
        Project.objects.create(id=3, name="接口项目", describe="这是接口自动化平台")
        project = Project.objects.get(name="接口项目")
        self.assertEqual(project.describe, "这是接口自动化平台")

    def test_project_update(self):
        project = Project.objects.get(id=1)
        project.name = "postman"
        project.save()
        project = Project.objects.get(id=1)
        self.assertEqual(project.name, "postman")

    def test_project_delete(self):
        Project.objects.get(id=1).delete()
        project = Project.objects.all()
        self.assertEqual(len(project), 1)


class TestAPI(TestCase):

    def setUp(self):
        TestTask.objects.create(id=1, name="task name", describe="describe ", status=0)

    def bytes_to_dict(self, data):
        content_str = str(data, encoding="utf-8")
        res = json.loads(content_str)
        return res

    def test_task_query(self):
        """
        查询一条任务
        """
        # from django.test import Client
        # c = Client()
        response = self.client.get('/api/v1/task/1/info/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        res = self.bytes_to_dict(response.content)
        print(res)
        self.assertEqual(res["success"], True)
        self.assertEqual(res["data"]["id"], 1)
        self.assertEqual(res["data"]["name"], "task name")

    def test_task_create(self):
        """
        创建一个任务
        """
        task = {"name": "task name3"}
        response = self.client.post('/api/v1/task/create/', data=task)
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        # response = self.client.get('/api/v1/task/1/info/')
        # print(response.status_code)
        # print(response.content)

    def test_task_update(self):
        """
        更新一个任务
        """
        task = {"id": 1, "name": "task name3", "describe": "task3 describe"}
        response = self.client.put('/api/v1/task/update/', data=task,
                                   content_type='application/json')
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_task_delete(self):
        """
        删除一个任务
        """
        response = self.client.delete('/api/v1/task/1/delete/')
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, 200)




