import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


# ORM
class Question(models.Model):
    """
    问题列表
    """
    question_text = models.CharField("问题", max_length=200)
    pub_date = models.DateTimeField("时间")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    问题选项列表
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


# class Person(models.Model):
#     LastName = models.CharField("last name", max_length=30, default="admin", null=False)
#     FirstName = models.CharField("first name")
#     Address = models.CharField("address", default="北京")
#     Age = models.IntegerField(default=0)
#     Status = models.BooleanField(default=True)
#     CreateTime = models.DateTimeField(auto_now_add=True)
#     UpdateTime = models.DateTimeField(auto_now=True)

