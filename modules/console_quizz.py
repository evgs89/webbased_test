import npyscreen
import random
from modules.quiz_engine import Engine



class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self._engine = Engine()
        self._current_test = ''
        self.numOfQuestions = 0
        self.numOfQuestionsAnswered = 0
        self.deck = {}
        self.addForm('MAIN', LoginForm)
        self.addForm('LOGIN_ERROR', LoginErrorForm)
        self.addForm('SELECT_TEST', SelectTestForm)
        self.addForm('SELECT_MODE', SelectModeForm)
        self.addFormClass('QUESTION', TestForm)
        self.addForm()



class LoginForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.FixedText(value = "Please input your username and password"))
        self._login = self.add(npyscreen.TitleText(name = "Username: "))
        self._password = self.add(npyscreen.TitlePassword(name = "Password: "))
        self.nextrely += 1
        self.add(npyscreen.FixedText(value = 'For exiting app press Ctrl+C'))

    def afterEditing(self):
        userId = self.parentApp._engine.validateUser(self._login, self._password)
        if userId: self.parentApp.setNextForm('SELECT_TEST')
        else: self.parentApp.setNextForm('LOGIN_ERROR')


class LoginErrorForm(npyscreen.fmPopup.Popup):
    def create(self):
        self.add(npyscreen.FixedText(value = "Login error. Username and/or password incorrect."))

    def afterEditing(self):
        self.parentApp.setNextForm('LOGIN')


class SelectTestForm(npyscreen.Form):
    def create(self):
        self._available_tests = self.parentApp._engine.get_available_tests() # [[id, name, description]]
        tests = [str(i[0]) + ' - ' + str(i[1]) for i in self._available_tests]
        self.test_selector = self.add(npyscreen.MultiLine(values = tests))

    def afterEditing(self):
        if self.test_selector.value:
            self.parentApp._engine.select_test(self._available_tests[self.test_selector.value][0])
            self.parentApp.setNextForm('SELECT_MODE')


class SelectModeForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.FixedText(value = "Ваш прогресс в выбранном тесте:"))
        self.add(npyscreen.FixedText(value = self.parentApp._engine.get_progress()))
        self.nextrely += 1
        self.add(npyscreen.FixedText(value = "Выберите режим прохождения:"))
        values = ['20 вопросов, обучение',
                  '50 вопросов, обучение',
                  '20 вопросов, экзамен',
                  '50 вопросов, экзамен',]
        self.selectedMode = self.add(npyscreen.MultiLine(values = values))

    def afterEditing(self):
        num = 20
        exam = False
        if self.selectedMode.value == 1 or self.selectedMode.value == 3: num = 50
        if self.selectedMode.value > 1: exam = True
        self.parentApp.numOfQuestions, self.parentApp.numOfQuestionsAnswered = num, 0
        if self.parentApp._engine.select_mode(num, exam):
            self.parentApp.setNextForm('QUESTION')


class TestForm(npyscreen.Form):
    def create(self):
        question = self.parentApp._engine.get_random_question_from_deck()
        self.name = question.tag
        self.progressbar = self.add(npyscreen.SliderNoLabel(out_of = len(self.parentApp._engine.deck_weights),
                                                   step = 0,
                                                   value = len(self.parentApp._engine.deck)))
        self.add(npyscreen.Pager(value = question.question, autowrap = True))
        self.answer = self.add(npyscreen.MultiLine(values = question.answers))


    def afterEditing(self):
        "validate user's answer and set next form"
        exam, correct, correct_keys = self.parentApp._engine.user_answered_question(self.name, self.answer,)
        if not exam and not correct:
            npyscreen.notify_confirm(f'Ответ неверный. Верные варианты: {", ".join(correct_keys)}')
        if not len(self.parentApp._engine.deck): self.parentApp.setNextForm('RESULT')


class ResultForm(npyscreen.Form):
    def create(self):
        self.name = "Result"
        correct_answers = self.parentApp._engine.test_finished()
        correct_answers_text = ''
        for answer in correct_answers:
            answers = "\n".join([j[1] for j in answer.correct_answers])
            correct_answers_text += f'Вопрос: {answer.tag}\n{answer.question}\nВерный ответ:\n{answers}\n'
        if self.parentApp._engine.exam:
            text = f'Тест окончен. Ознакомьтесь с вопросами, на которые Вы ответили неверно:\n{correct_answers_text}'
        else:
            text = 'Тест окончен.'
        self.add(npyscreen.Pager(value = text, autowrap = True))

    def afterEditing(self):
        self.parentApp.setNextForm(None)