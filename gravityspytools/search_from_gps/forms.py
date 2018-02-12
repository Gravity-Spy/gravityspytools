from django import forms


class SearchFormGPS(forms.Form):
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    gps = forms.CharField(label = 'GPS time of excess noise source')
    ifo = forms.CharField(label = 'The interferometer where this exces noise occured')
