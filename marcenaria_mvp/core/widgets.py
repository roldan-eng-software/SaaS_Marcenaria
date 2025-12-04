from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
