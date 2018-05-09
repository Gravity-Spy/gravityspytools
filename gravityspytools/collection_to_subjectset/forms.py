from django import forms


class SearchForm(forms.Form):
    username = forms.CharField(label='Your Zooniverse Username', max_length=100)
    collection_display_name = forms.CharField(label='The display name of your subject set as it shows in the URL')
    workflow_name = forms.CharField(label='The name of the workflow. Should include the name of the category')
