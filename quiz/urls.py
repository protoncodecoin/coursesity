from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, AnswerViewSet, SaveScoreView

router = DefaultRouter()
router.register(r"quizzes", QuizViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"answers", AnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("save-score/", SaveScoreView.as_view(), name="save-score"),
]
