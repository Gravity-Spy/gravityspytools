from django import forms


class SearchDBForm(forms.Form):
    zooid = forms.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', required=False)
    imageid = forms.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', required=False)
