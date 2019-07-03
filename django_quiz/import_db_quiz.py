import os
import sqlite3


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_quiz.settings')


import django
django.setup()
from quiz.models import Quizzes, Questions, Answers


filename = 'medtest.db'


def importer(filename, quiz_name, quiz_description = ''):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM questions")
    num_of_questions = int(cur.fetchone()[0])
    quiz = Quizzes.objects.get_or_create(name = quiz_name,
                                  description = quiz_description,
                                  max_weight = num_of_questions,
                                  initial_weight = num_of_questions/2)[0]
    quiz.save()
    cur.execute("SELECT * FROM questions")
    for row in cur.fetchall():
        question = Questions.objects.get_or_create(quiz_id = quiz,
                                                   question_id = row[0],
                                                   question_text = row[1])[0]
        question.save()
        cur.execute("SELECT * FROM answers WHERE tag = ?", (row[0], ))
        for ans in cur.fetchall():
            answer = Answers.objects.get_or_create(question_id = question,
                                           answer_text = ans[2],
                                           answer_correct = bool(ans[1]))[0]
            answer.save()
        print("created: ", str(row[0]))


if __name__ == "__main__":
    print("Start import")
    importer(filename, "Акушерство", "Выпускной тест")






