# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

from matplotlib import use
use('agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from login.utils import make_authorization_url
from .forms import SearchForm
from collection_to_subjectset.utils import retrieve_subjects_from_collection
from gwpy.table import EventTable
from .utils import obtain_figure

import io
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        form = SearchForm()
        return render(request, 'collectioninfo.html', {'form': form})
    else:
        return redirect(make_authorization_url())


def collectioninfo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])

            subjects_in_collection, tmp = retrieve_subjects_from_collection(username, collection_display_name)
            subjects_in_collection = [str(isubject) for isubject in subjects_in_collection]
            SI_glitches = EventTable.fetch('gravityspy', 'glitches_v2d0 WHERE CAST(links_subjects AS FLOAT) IN ({0})'.format(str(",".join(subjects_in_collection)))).to_pandas() 
            dategraph_url = request.get_full_path()[::-1].replace('collection-info'[::-1], 'dategraph'[::-1], 1)[::-1] 

            return render(request, 'collection_results.html', {'results': SI_glitches.to_dict(orient='records'), 'dategraph_url' : dategraph_url})
        else:
            return render(request, 'collectioninfo.html', {'form': form})

def dategraph(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])

            subjects_in_collection, tmp = retrieve_subjects_from_collection(username, collection_display_name)
            subjects_in_collection = [str(isubject) for isubject in subjects_in_collection]
            SI_glitches = EventTable.fetch('gravityspy', 'glitches_v2d0 WHERE CAST(links_subjects AS FLOAT) IN ({0})'.format(str(",".join(subjects_in_collection)))).to_pandas()
            fig = obtain_figure(SI_glitches)
            canvas = FigureCanvas(fig)
            buf = io.BytesIO()
            canvas.print_png(buf)
            response=HttpResponse(buf.getvalue(),content_type='image/png')
            fig.clear()
            return response
