from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from numpy.random import choice


# Create your models here.
class Quizzes(models.Model):
    name = models.TextField(unique = True, max_length = 250)
    url_name = models.SlugField(unique = True)
    description = models.TextField()
    max_weight = models.FloatField()
    initial_weight = models.FloatField()

    def get_deck(self, num_of_questions: int, user):
        """
        :param num_of_questions: number of questions to choose
        :param user: current user id
        :return: list of selected questions' ids
        """
        questions = Questions.objects.filter(quiz_id = self.id)
        progress = []
        for question in questions:
            progress.append(TestProgress.objects.get_or_create(user_id = user,
                                                               quiz_id = self,
                                                               question_id = question,
                                                               defaults = {'weight': self.initial_weight})[0])
        total_weight = sum([i.weight for i in progress])
        weights = [i.weight/total_weight for i in progress]
        deck_progress = choice(a = progress, size = num_of_questions, replace = False, p = weights)
        deck = [i.question_id.id for i in deck_progress]
        return deck


class Questions(models.Model):
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    question_tag = models.TextField()
    question_text = models.TextField()
    question_pic = models.TextField(default = '')

    def get_answers(self):
        return Answers.objects.filter(question_id = self.id)

    def get_right_answer(self):
        return Answers.objects.filter(question_id = self.id,
                                      answer_correct = True)

    def user_answered(self, user, correct: bool):
        if correct:
            progress = TestProgress.objects.get(user_id = user,
                                                quiz_id = self.quiz_id,
                                                question_id = self.id)
            progress.weight = progress.weight - 0.5 * (progress.weight - 1)
        else:
            max_weight = self.quiz_id.max_weight # Quizzes.objects.get(id = self.quiz_id.id).max_weight
            progress = TestProgress.objects.get(user_id = user,
                                                quiz_id = self.quiz_id,
                                                question_id = self.id)
            progress.weight = progress.weight + 0.5 * (max_weight - progress.weight)
        progress.last_seen = now()
        progress.seen_times += 1
        progress.save()


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

    def update_percentage(self):
        progress_rows = TestProgress.objects.filter(user_id = self.user_id,
                                                    quiz_id = self.quiz_id,)
        # quiz_row = Quizzes.objects.get(id = self.quiz_id.id)
        # max_weight = quiz_row.max_weight
        max_weight = self.quiz_id.max_weight
        num_of_rows = len(progress_rows)
        seen = 0
        learned = 0
        last_use = datetime(year = 1970, month = 1, day = 1)
        for row in progress_rows:
            if row.weight > max_weight / 3 and row.seen_times >= 2:
                learned += 1
            if row.seen_times:
                seen += 1
            try:
                if row.last_seen > last_use:
                    last_use = row.last_seen
            except TypeError:
                pass
        self.learned_percent = (learned / num_of_rows) * 100
        self.seen_percent = (seen / num_of_rows) * 100
        return self.save()


class TestProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    question_id = models.ForeignKey(Questions, on_delete = models.CASCADE)
    weight = models.FloatField(default = 0)
    seen_times = models.IntegerField(default = 0)
    last_seen = models.DateField(null = True)




