from django import forms
from .models import Library

class Memberform(forms.Modelform):
    class Meta:
        model = Library
        fields = ['']