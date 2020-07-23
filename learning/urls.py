from django.urls import path, include

from . views import HomePageView
from .views.quiz import QuizList, CreateQuizView, QuizDetailView, QuizUpdateView,QuizDeleteView, \
                        quiz_taking, quiz_results,quiz_results_chart, QuizTake, \
                        generate_results_pdf
from .views.questions import (QuestionList, CreateQuestionView, QuestionDetailView,
                            QuestionUpdateView,QuestionDeleteView )
from .views.answers import (AnswerList,CreateAnswerView, AnswerDetailView,
                            AnswerUpdateView, AnswerDeleteView
                            )


urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('quiz/', QuizList.as_view(), name='quiz_list'),
    path('quiz/add/', CreateQuizView.as_view(), name='create_quiz'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(),name="quiz_detail"),
    path('quiz/<int:pk>/update/', QuizUpdateView.as_view(),name="quiz_update"),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(),name="quiz_delete"),
    path('quiz/<int:pk>/take/', quiz_taking, name="take_quiz"),
    # path('quiz/<int:pk>/take/', QuizTake.as_view(), name="take_quiz"),
    path('quiz/<int:pk>/result/', quiz_results, name="quiz_result"),
    path('quiz/<int:pk>/result-chart/', quiz_results_chart, name="result-chart"),
    path('quiz/<int:pk>/result/pdf/', generate_results_pdf, name="results_pdf"),

    path('question/', QuestionList.as_view(), name='question_list'),
    path('question/add/', CreateQuestionView.as_view(), name='create_question'),
    path('question/<int:pk>/', QuestionDetailView.as_view(),name="question_detail"),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(),name="question_update"),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(),name="question_delete"),

    path('answer/', AnswerList.as_view(), name='answer_list'),
    path('answer/add/', CreateAnswerView.as_view(), name='create_answer'),
    path('answer/<int:pk>/', AnswerDetailView.as_view(),name="answer_detail"),
    path('answer/<int:pk>/update/', AnswerUpdateView.as_view(),name="answer_update"),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(),name="answer_delete"),
]
