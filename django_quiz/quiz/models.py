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
                                                               quiz_id = self.id,
                                                               question_id = question.id,
                                                               defaults = {'weight': self.initial_weight})[0])
        TestProgress.save()
        total_weight = sum([i.weight for i in progress])
        weights = [i.weight/total_weight for i in progress]
        deck_progress = choice(a = progress, size = num_of_questions, replace = False, p = weights)
        deck = [i.question_id for i in deck_progress]
        return deck


class Questions(models.Model):
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    question_tag = models.TextField()
    question_text = models.TextField()
    question_pic = models.TextField(default = '')

    def get_answers(self):
        return Answers.objects.get(question_id = self.question_id)[0]

    def get_right_answer(self):  # maybe it's not necessary
        return Answers.objects.filter(question_id = self.question_id,
                                      answer_correct = True)

    def right_answered(self, user):
        progress = TestProgress.objects.get(user_id = user,
                                 quiz_id = self.quiz_id,
                                 question_id = self.id)
        progress.weight = progress.weight - 0.5 * (progress.weight - 1)
        progress.save()

    def wrong_answered(self, user):
        max_weight = Quizzes.objects.get(id = self.quiz_id).max_weight
        progress = TestProgress.objects.get(user_id = user,
                                            quiz_id = self.quiz_id,
                                            question_id = self.id)
        progress.weight = progress.weight + 0.5 * (max_weight - progress.weight)
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


class TestProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    quiz_id = models.ForeignKey(Quizzes, on_delete = models.CASCADE)
    question_id = models.ForeignKey(Questions, on_delete = models.CASCADE)
    weight = models.FloatField(default = 0)
    seen_times = models.IntegerField(default = 0)
    last_seen = models.DateField()




