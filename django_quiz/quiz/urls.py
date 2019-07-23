from django.urls import path
from . import views


app_name = 'quiz'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('select', views.select, name = 'select'),
    path('upload', views.upload, name = 'upload'),
    path('<quiz_name_slug>', views.statistics),
    path('<quiz_name_slug>/start', views.start_test),
    path('<quiz_name_slug>/exam', views.exam),
    path('<quiz_name_slug>/result', views.result),
]