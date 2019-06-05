from django.urls import path
from . import views


app_name = 'quiz'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('select', views.select, name = 'select'),
]