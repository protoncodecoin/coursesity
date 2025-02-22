from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import modelform_factory
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions

from courses.models import Course
from .models import Quiz, Question, Answer, Score
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    SaveScoreSerializer,
)
from .forms import QuestionFormSet

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

    permission_classes = [permissions.IsAuthenticated]

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quiz"]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    View to list all anwers related to question
    """

    permission_classes = [permissions.IsAuthenticated]

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class SaveScoreView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        scores = Score.objects.filter(user=request.user)
        serializer = SaveScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def post(self, request):

        score = request.data.get("score", 0)
        quiz_id = request.data.get("quiz")
        user = request.user
        # save the score in a database model

        quiz_obj = Quiz.objects.get(id=quiz_id)

        saved_score_obj, created = Score.objects.update_or_create(
            user=user,
            quiz=quiz_obj,
            defaults={"score": score, "user": user, "quiz": quiz_obj},
        )

        # score = Score.objects.create(user=user, quiz=quiz_obj, score=score)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["course"].queryset = Course.objects.filter(owner=self.request.user)
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["style"] = "create_form"
        return context


class ManageQuizListView(OwnerQuizMixin, ListView):
    template_name = "quiz/manage/quiz/list.html"
    permission_required = "quiz.view_quiz"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["style"] = "manage_course"
        return context

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class QuizCreateView(OwnerQuizEditMixin, CreateView):
    permission_required = "quiz.add_quiz"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the course field to show only courses created by the current user
        form.fields["course"].queryset = Course.objects.filter(owner=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["style"] = "create_form"
        return context


class QuizUpdateView(OwnerQuizEditMixin, UpdateView):
    permission_required = "quiz.change_quiz"


class QuizDeleteView(OwnerQuizEditMixin, DeleteView):
    template_name = "quiz/manage/quiz/delete.html"
    permission_required = "quiz.delete_quiz"


class QuizQuestionUpdateView(TemplateResponseMixin, View):
    template_name = "quiz/manage/question/formset.html"
    quiz = None

    def get_formset(self, data=None):
        """
        Build formset for questions
        """
        return QuestionFormSet(instance=self.quiz, data=data)

    def dispatch(self, request, pk):
        # build course object and set in self.quiz
        self.quiz = get_object_or_404(Quiz, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {"quiz": self.quiz, "formset": formset, "style": "course_form"}
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_quiz_list")
        return self.render_to_response(
            {
                "quiz": self.quiz,
                "formset": formset,
                # "style": "form_course",
            }
        )


class AnswerCreateUpdateView(TemplateResponseMixin, View):
    quiz = None
    answer = None
    question = None
    template_name = "quiz/manage/quiz/form.html"

    def get_form(self, *args, **kwargs):
        Form = modelform_factory(Answer, exclude=["question"])
        return Form(*args, **kwargs)

    def dispatch(self, request, quiz_id, question_id, id=None, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, id=quiz_id)
        self.question = get_object_or_404(Question, id=question_id)
        if id:  # id of the answer if it's none then we are creating a new answer
            self.answer = get_object_or_404(Answer, pk=id)

        return super().dispatch(request, quiz_id, question_id, id)

    def get(self, request, quiz_id, question_id, id=None):
        form = self.get_form(instance=self.answer)
        return self.render_to_response(
            {
                "form": form,
                "object": self.answer,
                "question_object": self.question,
                "style": "create_form",
            }
        )

    def post(self, request, quiz_id, question_id, id=None):
        form = self.get_form(instance=self.answer, data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.question = self.question
            obj.save()

            return redirect("quiz_answer_list", quiz_id)
        return self.render_to_response(
            {
                "form": form,
                "object": self.answer,
                "style": "create_form",
            }
        )


class AnswerContentListView(TemplateResponseMixin, View):
    template_name = "quiz/manage/quiz/answer_list.html"

    def get(self, request, quiz_id):
        quiz_obj = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz_obj.questions.all()

        return self.render_to_response(
            {
                "questions": questions,
                "quiz": quiz_obj,
                "style": "answer_list",
            }
        )


class DeleteQuizAnswerView(View):
    def post(self, request, quiz_id, id):
        quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)
        answer_obj = Answer.objects.filter(question__quiz=quiz, id=id)
        answer_obj.delete()
        return redirect("quiz_answer_list", quiz.id)
