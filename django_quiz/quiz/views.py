from django.shortcuts import render, redirect
from quiz.models import Quizzes, Questions, Progress
from quiz.forms import QuestionForm
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
def start_test(request, quiz_name_slug):
    num_of_questions = request.GET.get('num', '20')
    exam = bool(request.GET.get('exam', '0'))
    current_quiz = Quizzes.objects.get(url_name = quiz_name_slug)
    request.session['exam'] = exam
    request.session['current_test'] = current_quiz.id
    request.session['deck_length'] = num_of_questions
    request.session['answered'] = 0
    request.session['user_answers'] = {}  # {question_id: [answers_id]}
    request.session['current_deck'] = current_quiz.get_deck(num_of_questions, request.user)
    return redirect(f'/quiz/{quiz_name_slug}/exam')


@login_required
def exam(request):
    if request.method == 'GET':
        try:
            question_id = request.session.get('current_deck', []).pop()
            question = Questions.objects.get(id = question_id)
            form = QuestionForm(question)
            answers = question.get_answers()
            context_dict = {'question': question, 'form': form, 'answers': answers,
                            'answered': request.session.get('answered', 0),
                            'deck_length': request.session.get('deck_length', 0)}
            return render(request, 'quiz/question.html', context_dict)
        except IndexError:
            print('deck is empty')
    elif request.method == 'POST':
        pass


