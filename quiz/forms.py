from django.forms.models import inlineformset_factory
from .models import Quiz, Question

QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    fields=[
        "question_text",
        "score",
    ],
    extra=5,
    can_delete=True,
)
