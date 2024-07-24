from django import forms


class CartAddCourseForm(forms.Form):

    quantity = forms.IntegerField(default=1)
