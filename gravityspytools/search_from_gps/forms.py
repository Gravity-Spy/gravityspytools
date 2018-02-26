from django import forms

STATUS_CHOICES = (
    ("H1", "H1"), ("L1", "L1"), ("V1", "V1")
)

class SearchFormGPS(forms.Form):
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    gps = forms.CharField(label = 'GPS time of excess noise source')
    ifo = forms.ChoiceField(choices=STATUS_CHOICES, label = 'The interferometer where this exces noise occured')
