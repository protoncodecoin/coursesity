from django.db import models
from django.conf import settings

from courses.models import Module, Subject, Course

from django.utils.text import slugify


# Create your models here.
class Quiz(models.Model):
    # subject = models.ForeignKey(
    #     Subject, on_delete=models.CASCADE, related_name="quizes"
    # )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes_created",
    )
    slug = models.SlugField(max_length=300, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    # module = models.ForeignKey(+++
    #     Module, on_delete=models.CASCADE, related_name="quiz_module"
    # )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    pass_score = models.IntegerField(default=90)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)

        super(Quiz, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    # module = models.ForeignKey(
    #     Module, on_delete=models.CASCADE, related_name="quiz_module"
    # )
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
