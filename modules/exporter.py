import random


class SimpleExporter:
    def __init__(self):
        self._marks = ['А','Б','В','Г']

    def _mix(self, length = 4):
        dec_counter = length
        sequence = []
        while dec_counter:
            dec_counter -= 1
            added = False
            while not added:
                rand = random.randint(0, length - 1)
                if rand not in sequence:
                    sequence.append(rand)
                    added = True
        return sequence

    def export(self, filename, questions):
        questions_text = ''
        questions_keys = ''
        for current_question in questions:
            sequence = self._mix(4)
            text = '  ' + current_question.number + '\n' + current_question.question + '\n\n'
            variants = ''
            key = ''
            for i in range(4):
                variants += '{mark} - {variant}\n'.format(mark = self._marks[i], variant = current_question.answers[sequence[i]][1])
                if current_question.answers[sequence[i]][0]: key = '{tag} - {mark}\n'.format(tag = current_question.number, mark = self._marks[i])
            questions_text += text + variants + '\n\n'
            questions_keys += key + '\n'
        with open(filename + '_test.txt', 'w') as test:
            test.write(questions_text)
        with open(filename + '_keys.txt', 'w') as keys:
            keys.write(questions_keys)
