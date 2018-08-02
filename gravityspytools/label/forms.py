from django import forms
from .models import Label

# Create your models here.
class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['agreed', 'label', 'uniqueID']
