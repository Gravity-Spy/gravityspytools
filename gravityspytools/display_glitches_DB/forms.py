from django import forms

STATUS_CHOICES = (
    ("Blip", "Blip"), ("Whistle", "Whistle"), ("1080Lines", "1080Lines"), ("Wandering_Line", "Wandering_Line"),
    ("1400Ripples", "1400Ripples")
)

class SearchDBForm(forms.Form):
    glitchclass = forms.ChoiceField(choices=STATUS_CHOICES, label = 'The class') 
