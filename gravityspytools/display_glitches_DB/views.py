# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render

from .forms import SearchDBForm
from .utils import searchDB


def index(request):
    form = SearchDBForm()
    return render(request, 'form_for_DB.html', {'form': form})


# Create your views here.
def do_DB_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchDBForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            SI_glitches = searchDB(form)

            return render(request, 'searchDBresults.html', {'results': SI_glitches.to_dict(orient='records')})
