from collections import namedtuple

class TestQuestion:
    def __init__(self):
        self._question = ''
        self._number = ''
        self._answers = []
        self._available_answers_count = 0
        self._pic = None

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, text):
        self._question = str(text)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = str(number)

    @property
    def question_picture(self):
        return self._pic

    @question_picture.setter
    def question_picture(self, pic):
        self._pic = pic

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, answers):
        self._answers = answers
        self._available_answers_count = 0
        for i in self._answers:
            if i[0]: self._available_answers_count += 1

    def add_answer(self, answer, correct = False, pic = None):
        self._answers.append((correct, answer, pic))
        if correct: self._available_answers_count += 1

    def get_correct_answers(self):
        correct_answers = namedtuple('correct_answers', 'tag question question_pic correct_answers')
        return correct_answers(self._number, self._question, self._pic, [i for i in self._answers if i[0]])

    def __repr__(self):
        variants = ''
        for i in self._answers:
            variants += "[{correct}] {variant}\n".format(correct = " + " if i[0] else " - ", variant = i[1])
        return "{number}: \n{question}: \nVariants: \n{vars}".format(question = self._question,
                                                                        number = self._number,
                                                                        vars = variants)


class SpecialFileImporter:
    def __init__(self):
        pass

    def open_file(self, filename):
        counter = 1
        questions = []
        current_question = TestQuestion()
        quest_text = ''
        with open(filename) as file:
            for line in file:
                try:
                    start_of_question = line.index('{count}.'.format(count = str(counter)))
                    if line[:2] == 'Г)':
                        current_question.add_answer(line[2:start_of_question])
                        questions.append(current_question)
                    current_question = TestQuestion()
                    counter += 1
                    num_starts = line.index('[')
                    num_ends = line.index(']')
                    num_of_question = line[(num_starts + 1):num_ends]
                    current_question.number = num_of_question
                    quest_text = line[(num_ends + 1):-1]
                except ValueError:
                    if line[:2] == 'А)':
                        current_question.question = quest_text
                        quest_text = ''
                        current_question.add_answer(line[2:-1], True)
                    elif line[:2] == 'Б)' or line[:2] == 'В)': current_question.add_answer(line[2:-1])
                    elif line[:2] == 'Г)':
                        current_question.add_answer(line[2:-1])
                        questions.append(current_question)
                    else: quest_text = quest_text + ' ' + line[:-1]
        return questions



                    


