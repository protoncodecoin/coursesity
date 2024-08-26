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
