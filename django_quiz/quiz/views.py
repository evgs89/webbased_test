from django.shortcuts import render
from quiz.models import Quizzes, Questions, Answers, Progress
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'quiz/index.html')


@login_required
def select(request):
    quizzes = Quizzes.objects.all()
    context_dict = {'quizzes': quizzes}
    return render(request, 'quiz/select.html', context_dict)


@login_required
def statistics(request, quiz_name_slug):
    quiz = Quizzes.objects.get(url_name = quiz_name_slug)
    user = request.user
    progress = Progress.objects.get_or_create(user_id = user, quiz_id = quiz)[0]
    context_dict = {'progress': progress, 'quiz': quiz}
    return render(request, 'quiz/statistics.html', context_dict)


@login_required
def start_test(request):
    num_of_questions = request.GET.get('num', '20')
