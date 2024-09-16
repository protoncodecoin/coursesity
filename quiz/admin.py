from django.contrib import admin

from .models import Question, Answer, Quiz, Score


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["course", "title", "description", "created_at"]
    list_filter = ["created_at"]
    prepopulated_fields = {"slug": ("title",)}


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ["text", "question", "is_correct"]
#     list_filter = ["is_correct"]


class AnswerInline(admin.StackedInline):
    model = Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "quiz", "created_at"]
    list_filter = ["created_at"]
    inlines = [AnswerInline]


@admin.register(Score)
class Score(admin.ModelAdmin):
    list_display = ["user", "score", "taken_at"]
    list_filter = ["score", "taken_at"]
