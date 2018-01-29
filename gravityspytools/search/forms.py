from django import forms
from gwpy.table import EventTable


def get_imageid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarityindex WHERE \"uniqueID\" ~ \'{0}\' LIMIT 100'.format(name), columns=["uniqueID"]).to_pandas().rename(columns={'uniqueID': 'value'}).to_json(orient='records')


def get_zooid_json(name=''):
    return EventTable.fetch('gravityspy', 'similarityindex WHERE CAST(links_subjects AS TEXT) ~ \'{0}\' LIMIT 100'.format(name), columns=["links_subjects"]).to_pandas().astype(str).rename(columns={'links_subjects': 'value'}).to_json(orient='records')


class SearchForm(forms.Form):
    username = forms.CharField(label='Your Zooniverse Username', max_length=100)
    howmany = forms.IntegerField(label='How many similar images would you like to return', max_value=200, min_value=1)
    zooid = forms.CharField(label = 'This is the Zooniverse assigned random ID of the image (an integer value)', max_length=10, initial='0')
    imageid = forms.CharField(label='The GravitySpy uniqueid (this is the 10 character hash that uniquely identifies all gravity spy images)', max_length=10, initial='0')
