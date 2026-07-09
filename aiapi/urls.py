from django.urls import path
from . import views

urlpatterns = [
    path("textquery/", views.text_generator, name="text_generator"),            
    path("generate_quiz/", views.generate_quiz, name="generate_quiz"),           
    path("take_quiz/", views.take_quiz, name="take_quiz"),           
    path("results/", views.quiz_results, name="quiz_results"),           
]