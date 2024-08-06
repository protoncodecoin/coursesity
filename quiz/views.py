from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Quiz, Question, Answer
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
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
    def post(self, request):
        score = request.data.get("score")
        # save the score in a database model
        # to be implemented later
        return Response({"score": score}, status=status.HTTP_200_OK)
