from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('match/', views.match, name='match-list'),
    path('question_page/<int:questionId>/', views.question_page, name='question_page' ),
    path('quiz_intro', views.quiz_intro, name='quiz_intro')
]

