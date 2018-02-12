# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation

from .forms import SearchFormGPS
from .utils import make_gravityspy_image
from .utils import search_si_database

import pandas as pd
from sqlalchemy.engine import create_engine


def index(request):
    form = SearchFormGPS()
    return render(request, 'form_search_gps.html', {'form': form})


def similarity_search_with_GPS_restful_API(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchFormGPS(request.GET)
        # check whether it's valid:
        if form.is_valid():
            gps = float(form.cleaned_data['gps'])
            howmany = int(form.cleaned_data['howmany'])
            ifo = str(form.cleaned_data['ifo'])

            imagepath, ID = make_gravityspy_image(eventTime=gps, ifo=ifo, sampleFrequency=16384, blockTime=64)

            SI_glitches = search_si_database(ID, howmany)

            return JsonResponse(SI_glitches.to_dict(orient='list'))


def similarity_search_with_GPS(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchFormGPS(request.GET)
        # check whether it's valid:
        if form.is_valid():
            gps = float(form.cleaned_data['gps'])
            howmany = int(form.cleaned_data['howmany'])
            ifo = str(form.cleaned_data['ifo'])

            imagepath, ID = make_gravityspy_image(eventTime=gps, ifo=ifo, sampleFrequency=16384, blockTime=64)

            SI_glitches = search_si_database(ID, howmany)

            return render(request, 'searchGPSresults.html', {'results': SI_glitches.to_dict(orient='records'), 'ID' : imagepath})
