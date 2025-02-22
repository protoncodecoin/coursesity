from rest_framework import serializers
from .models import Quiz, Question, Answer, Score


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.HyperlinkedRelatedField(
        view_name="courses:course-detail", read_only=True
    )
    # questions = serializers.HyperlinkedRelatedField(
    #     many=True, view_name="question-detail", read_only=True
    # )
    instructor = serializers.ReadOnlyField(source="course.owner.get_full_name")

    class Meta:
        model = Quiz
        fields = [
            "url",
            "id",
            "course",
            "title",
            "description",
            "pass_score",
            "created_at",
            "instructor",
        ]


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    # question = serializers.HyperlinkedRelatedField(
    #     view_name="question-detail", read_only=True
    # )

    class Meta:
        model = Answer
        fields = [
            # "url",
            "id",
            # "question",
            "text",
            "is_correct",
        ]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    quiz = serializers.HyperlinkedRelatedField(view_name="quiz-detail", read_only=True)
    # answers = serializers.HyperlinkedRelatedField(
    #     many=True, view_name="answer-detail", read_only=True
    # )
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            # "url",
            "id",
            "quiz",
            "question_text",
            "score",
            "created_at",
            "answers",
        ]


class SaveScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score

        fields = [
            "id",
            "user",
            "score",
            "taken_at",
        ]
