from django import forms

from my_store.models import BoardGame

DISPLAY_CHOICES = (
    ("1", "1"),
    ("2", "2")
)


class ComplexityForm(forms.Form):
    complexity = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=DISPLAY_CHOICES, required=False)
