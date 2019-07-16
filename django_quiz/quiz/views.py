from django.http import HttpResponse
from django.shortcuts import render, redirect
from quiz.models import Quizzes, Questions, Progress, Answers
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
    num_of_questions = int(request.GET.get('num', '20'))
    is_exam = bool(int(request.GET.get('exam', '0')))
    current_quiz = Quizzes.objects.get(url_name = quiz_name_slug)
    request.session['exam'] = is_exam
    request.session['current_test'] = current_quiz.id
    request.session['deck_length'] = num_of_questions
    request.session['answered'] = 0
    request.session['user_answers'] = {}  # {question_id: [answers_id]}
    request.session['current_deck'] = current_quiz.get_deck(num_of_questions, request.user)
    return redirect(f'/quiz/{quiz_name_slug}/exam')


@login_required
def exam(request, quiz_name_slug):
    if request.method == 'GET':
        try:
            question_id = request.session.get('current_deck', []).pop()
            request.session['current_question'] = question_id
            question = Questions.objects.get(id = question_id)
            form = QuestionForm(question = question)
            answers = question.get_answers()
            pics = {a.id: f"<img src='/static/{a.answer_pic}'>" if a.answer_pic else "" for a in answers}
            context_dict = {'question': question, 'form': form, 'answers': answers, 'pics': pics,
                            'quiz_name_slug': quiz_name_slug,
                            'answered': request.session.get('answered', 0),
                            'deck_length': request.session.get('deck_length', 0)}
            return render(request, 'quiz/question.html', context_dict)
        except IndexError: # questions in deck are finished
            print('deck is empty')
            return redirect(f'/quiz/{quiz_name_slug}/result')
    elif request.method == 'POST':
        question_id = request.session.get('current_question', 0)
        question = Questions.objects.get(id = question_id)
        form = QuestionForm(request.POST, question = question)
        answered = request.session.get('answered', 0)
        deck = request.session.get('current_deck', [])
        if form.is_valid():
            user_answers = set(form.cleaned_data['answers'])
            correct_answers = set(str(answer.id) for answer in question.get_right_answer())
            user_answer_is_correct = user_answers == correct_answers
            question.user_answered(request.user, user_answer_is_correct)
            if not user_answer_is_correct:
                request.session['user_answers'][question_id] = list(user_answers)
            # in learning mode show right answer after each question, exam mode shows answers only in the end
            if request.session.get('exam', False) or user_answer_is_correct:
                request.session['answered'] = answered + 1
                return redirect(f'/quiz/{quiz_name_slug}/exam')
            else:
                deck.append(question_id)
                request.session['current_deck'] = deck
                return redirect(f'/quiz/{quiz_name_slug}/result')

@login_required
def result(request, quiz_name_slug):
    try:
        question_id, answer_ids = request.session['user_answers'].popitem()
        request.session.save()
        # request.session['user_answers'].pop(question_id)
        question = Questions.objects.get(id = question_id)
        user_answers = [Answers.objects.get(id = answer_id) for answer_id in answer_ids]
        right_answers = question.get_right_answer()
        context_dict = {'question': question, 'user_answers': user_answers,
                        'right_answers': right_answers, 'quiz_name_slug': quiz_name_slug}
        return render(request, 'quiz/result.html', context_dict)
    except KeyError:
        progress = Progress.objects.get(user_id = request.user,
                                        quiz_id = request.session['current_test'])
        progress.update_percentage()
        return redirect(f"/quiz/{quiz_name_slug}")





