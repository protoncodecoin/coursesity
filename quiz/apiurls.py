from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"quizzes", views.QuizViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"answers", views.AnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("mine/quiz/", views.ManageQuizListView.as_view(), name="manage_quiz_list"),
    path("save-score/", views.SaveScoreView.as_view(), name="save-score"),
]
