from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        fields = [
            "first",
            "last_name",
            "email",
        ]
