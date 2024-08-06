from django.contrib import admin

from .models import Question, Answer, Quiz, Score


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["course", "title", "description", "created_at"]
    list_filter = ["created_at"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "quiz", "created_at"]
    list_filter = ["created_at"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["text", "question", "is_correct"]
    list_filter = ["is_correct"]


@admin.register(Score)
class Score(admin.ModelAdmin):
    list_display = ["user", "score", "taken_at"]
    list_filter = ["score", "taken_at"]
