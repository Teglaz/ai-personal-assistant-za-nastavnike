from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kviz/', views.quiz_generator, name='quiz_generator'),
    path('plan/', views.lesson_planner, name='lesson_planner'),
    path('domaci/', views.homework_creator, name='homework_creator'),
    
    # NOVI URL-ovi za osnovnu školu
    path('osnovna/kviz/', views.osnovna_quiz, name='osnovna_quiz'),
    path('osnovna/plan/', views.osnovna_plan, name='osnovna_plan'),
    path('osnovna/domaci/', views.osnovna_domaci, name='osnovna_domaci'),
    
    # NOVI URL-ovi za srednju školu
    path('srednja/kviz/', views.srednja_quiz_form, name='srednja_quiz'),  
    path('srednja/plan/', views.srednja_lesson_planner, name='srednja_plan'),
    path('srednja/domaci/', views.srednja_homework_creator, name='srednja_domaci'), 
]