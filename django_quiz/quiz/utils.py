import os, shutil
import string
import random
from zipfile import PyZipFile

from django.core.files import File
from django.core.files.images import ImageFile
from django.db.models import Model

from quiz.models import Quizzes, Questions, Progress, Answers


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Answer(object):
    def __init__(self):
        self.id_ = id_generator(5)
        self.text = ''
        self.pic = ''
        self.correct = False

    def __repr__(self):
        return f"""

            Answer id: {self.id_}
            Answer text: {self.text}
            Answer picture: {self.pic}
            Answer is correct: {self.correct}

        """

    def __str__(self):
        return self.__repr__()



class Question(object):
    def __init__(self, id_):
        self.id_ = id_
        self.text = ''
        self.pic = ''
        self.answers = []

    def __repr__(self):
        answers = '\n'.join([str(i) for i in self.answers])
        return f"""
Question: {self.id_}
Question text: {self.text}
Question picture: {self.pic}
Answers:

{answers}
"""


def import_quiz(file):
    try:
        os.mkdir('tempdir')
    except:
        shutil.rmtree('tempdir')
        os.mkdir('tempdir')
    os.mkdir('tempdir/extracted')
    with open('tempdir/uploaded.zip', 'wb') as quiz_zip:
        for chunk in file.chunks():
            quiz_zip.write(chunk)
    arch = PyZipFile('tempdir/uploaded.zip')
    arch.extractall(path = 'tempdir/extracted')
    try:
        with open('tempdir/extracted/description.txt', 'r') as description:
            info = description.readlines()
            quiz = Quizzes.objects.get_or_create(url_name = info[0].strip(),
                                                 name = info[1].strip(),
                                                 description = info[2].strip(),)[0]
        with open('tempdir/extracted/test.txt', 'r') as test:
            # parse plaintext
            lines = test.readlines()
            tags = []
            tag = ''
            current_text = ''
            for line in lines:
                if tag and current_text:
                    tags.append((tag, current_text.rstrip('\n\r ')))
                if line.startswith("<%%"):
                    tag = line.partition('>')[0] + '>'
                    current_text = line.partition('>')[2]
                else:
                    current_text += line
            # if last line was without tag:
            if tag and current_text:
                tags.append((tag, current_text.rstrip('\n\r ')))
            # handling parsed data to custom classes
            questions = []
            for tag, value in tags:
                if tag == "<%%ID>":
                    questions.append(Question(value))
                elif tag == "<%%Q>":
                    questions[-1].text = value
                elif tag == "<%%QP>":
                    questions[-1].pic = value
                elif tag == "<%%AC>" or tag == "<%%A>":
                    questions[-1].answers.append(Answer())
                    questions[-1].answers[-1].text = value
                    questions[-1].answers[-1].correct = tag == "<%%AC>"
                elif tag == "<%%AP>":
                    questions[-1].answers[-1].pic = value
            # save to db
            for q in questions:
                question = Questions.objects.get_or_create(quiz_id = quiz,
                                                           question_tag = q.id_)[0]
                question.question_text = q.text
                if q.pic: save_pic(q.pic, question)
                question.save()
                for a in q.answers:
                    answer = Answers.objects.get_or_create(question_id = question,
                                                           answer_text = a.text)[0]
                    answer.answer_correct = a.correct
                    if a.pic: save_pic(a.pic, answer)
                    answer.save()
        quiz.calc_weight()
        quiz.save()
        return True
    except Exception as e:
        print(e, str(e))


def save_pic(filename: str, model: Questions or Answers):
    with open(os.path.join('tempdir', 'extracted', filename), 'rb') as file:
        expansion = filename.rpartition('.')[2]
        ID = id_generator(20)
        while os.path.isfile(f'{ID}.{expansion}'):
            ID = id_generator(20)
        new_filename = f'{ID}.{expansion}'
        if type(model) == Questions:
            model.question_pic.save(new_filename, file, True)
        elif type(model) == Answers:
            model.answer_pic.save(new_filename, file, True)
        model.save()
    return True
