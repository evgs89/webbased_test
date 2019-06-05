from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'quiz/index.html')


def select(reqest):
    return render(request, 'quiz/select.html')
