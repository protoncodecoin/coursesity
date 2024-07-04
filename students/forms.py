from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput
    )

    # def __init__(self, form):
    #     super(CourseEnrollForm, self).__init__()
    #     self.fields["course"].queryset = Course.objects.all()
