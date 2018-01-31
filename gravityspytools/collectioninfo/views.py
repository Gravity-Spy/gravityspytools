# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render

from collection_to_subjectset.forms import SearchForm
from collection_to_subjectset.utils import retrieve_subjects_from_collection
from gwpy.table import EventTable

# Create your views here.

def index(request):
    form = SearchForm()
    return render(request, 'collectioninfo.html', {'form': form})


def collectioninfo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])

            subjects_in_collection = retrieve_subjects_from_collection(username, collection_display_name)
            subjects_in_collection = [str(isubject) for isubject in subjects_in_collection]
            SI_glitches = EventTable.fetch('gravityspy', 'glitches WHERE CAST(links_subjects AS FLOAT) IN ({0})'.format(str(",".join(subjects_in_collection)))).to_pandas() 

            return render(request, 'searchresults.html', {'results': SI_glitches.to_dict(orient='records')})
