from django.urls import path

from . import views

urlpatterns = [
    path("mine/", views.ManageQuizListView.as_view(), name="manage_quiz_list"),
    path("create/", views.QuizCreateView.as_view(), name="quiz_create"),
    path("<pk>/edit/", views.QuizUpdateView.as_view(), name="quiz_edit"),
    path("<pk>/delete/", views.QuizDeleteView.as_view(), name="quiz_delete"),
    path(
        "<pk>/mdoule/",
        views.QuizQuestionUpdateView.as_view(),
        name="quiz_question_update",
    ),
    path(
        "answer/<int:quiz_id>/<int:question_id>/create/",
        views.AnswerCreateUpdateView.as_view(),
        name="answer_content_create",
    ),
    path(
        "answer/<int:quiz_id>/update/<int:id>/<int:question_id>/",
        views.AnswerCreateUpdateView.as_view(),
        name="answer_content_update",
    ),
    path(
        "questions/<int:quiz_id>/",
        views.AnswerContentListView.as_view(),
        name="quiz_answer_list",
    ),
]
