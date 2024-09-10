from django.urls import path

from . import views

urlpatterns = [
    path("mine/", views.ManageQuizListView.as_view(), name="manage_quiz_list"),
    path("create/", views.QuizCreateView.as_view(), name="quiz_create"),
    path("<pk>/edit/", views.QuizUpdateView.as_view(), name="quiz_edit"),
    path("<pk>/delete/", views.QuizDeleteView.as_view(), name="quiz_delete"),
]
