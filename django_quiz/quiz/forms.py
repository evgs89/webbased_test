from django import forms


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        answers = self.question.get_answers()
        self.choices = [(a.id, a.answer_text) for a in answers]
        self.fields['answers'] = forms.MultipleChoiceField(choices = self.choices,
                                                           widget = forms.CheckboxSelectMultiple)


class UploadTestForm(forms.Form):
    file = forms.FileField(label = "Select a file", required = True)




