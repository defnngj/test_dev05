from time import sleep
from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


# class UserModelsTest(TestCase):
#     """模型测试"""
#     def setUp(self):
#         self.q = Question.objects.create(question_text="What's new?", pub_date=timezone.now())
#         self.q_id = self.q.id
#
#     def create_choice(self):
#         c = Choice.objects.create(choice_text='Not much', question=self.q)
#         self.assertEqual(c.choice_text, "Not much")
#
#         c1 = Choice.objects.create(choice_text='new option', question_id=self.q_id)
#         self.assertEqual(c1.choice_text, "new option")
#


class MySeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        self.q = Question.objects.create(question_text="What's new?", pub_date=timezone.now())
        self.q_id = self.q.id
        Choice.objects.create(choice_text='Not much', question=self.q)
        Choice.objects.create(choice_text='new option', question_id=self.q_id)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_polls(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/polls/'))
        sleep(1)
        self.selenium.find_elements_by_class_name("my-li-a")[0].click()
        self.selenium.find_elements_by_css_selector("[type=radio]")[0].click()
        self.selenium.find_element_by_id("voteButton").click()
        sleep(2)
        result = self.selenium.find_elements_by_class_name("result-list")[0].text
        print("result-->",  result)
        self.assertIn("1 vote", result)




