from django import forms


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        answers = question.get_answers()
        self.choices = [(a.id, a.answer_text) for a in answers]
        self.answers = forms.ChoiceField(choices = self.choices)



