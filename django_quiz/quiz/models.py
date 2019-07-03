from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Quizzes(models.Model):
    name = models.TextField(unique = True, max_length = 250)
    url_name = models.SlugField(unique = True)
    description = models.TextField()
    max_weight = models.FloatField()
    initial_weight = models.FloatField()


class Questions(models.Model):
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    question_id = models.TextField()
    question_text = models.TextField()
    question_pic = models.TextField(default = '')


class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete = models.CASCADE)
    answer_text = models.TextField()
    answer_pic = models.TextField(default = '')
    answer_correct = models.BooleanField()


class Progress(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    last_use = models.DateTimeField(default = now)
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    learned_percent = models.FloatField(default = 0)
    seen_percent = models.FloatField(default = 0)

