from typing import Any
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Quiz, Question, Answer, Score
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    SaveScoreSerializer,
)

# Create your views here.


class QuizViewSet(viewsets.ModelViewSet):
    """
    View to list all quizes related to a course
    """

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    View to list all questions related to quiz
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    View to list all anwers related to question
    """

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class SaveScoreView(APIView):

    def get(self, request, format=None):
        scores = Score.objects.filter(user=request.user)
        serializer = SaveScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def post(self, request):

        score = request.data.get("score", 0)
        # save the score in a database model
        # to be implemented later
        return Response({"score": score}, status=status.HTTP_200_OK)


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerQuizMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Quiz
    fields = [
        "course",
        "title",
        "description",
        "pass_score",
    ]
    success_url = reverse_lazy("manage_quiz_list")


class OwnerQuizEditMixin(OwnerQuizMixin, OwnerEditMixin):
    template_name = "quiz/manage/quiz/form.html"


class ManageQuizListView(OwnerQuizMixin, ListView):
    template_name = "quiz/manage/quiz/list.html"
    permission_required = "quiz.view_quiz"

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class QuizCreateView(OwnerQuizEditMixin, CreateView):
    permission_required = "quiz.add_quiz"


class QuizUpdateView(OwnerQuizEditMixin, UpdateView):
    permission_required = "quiz.change_quiz"


class QuizDeleteView(OwnerQuizEditMixin, DeleteView):
    template_name = "quiz/manage/quiz/delete.html"
    permission_required = "quiz.delete_quiz"
