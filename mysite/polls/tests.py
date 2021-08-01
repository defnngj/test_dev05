from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone


class UserModelsTest(TestCase):
    """模型测试"""
    def setUp(self):
        self.q = Question.objects.create(question_text="What's new?", pub_date=timezone.now())
        self.q_id = self.q.id

    def create_choice(self):
        c = Choice.objects.create(choice_text='Not much', question=self.q)
        self.assertEqual(c.choice_text, "Not much")

        c1 = Choice.objects.create(choice_text='new option', question_id=self.q_id)
        self.assertEqual(c1.choice_text, "new option")


