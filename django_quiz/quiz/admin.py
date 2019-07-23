from django.contrib import admin
from quiz.models import Quizzes, Questions, Progress, Answers


# Register your models here.
admin.site.register(Quizzes)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Progress)