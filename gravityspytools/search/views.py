# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, redirect
import os
import subprocess
from django.http import HttpResponse
from django.http import JsonResponse
from matplotlib import use
use('agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from .forms import SearchForm, LIGOSearchForm
from .forms import get_imageid_json
from .forms import get_zooid_json
from .forms import get_gpstimes_json

from .utils import similarity_search
from .utils import create_collection
from .utils import histogram as make_histogram
from login.utils import make_authorization_url

import pandas as pd
from sqlalchemy.engine import create_engine


# Create your views here.
def get_imageids(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        data = get_imageid_json(name=q)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_zooids(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        data = get_zooid_json(name=q)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_gpstimes(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        data = get_gpstimes_json(name=q)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def index(request):
    if request.user.is_authenticated():
        request.session['auth_user_backend'] = request.session['_auth_user_backend']
        if request.session['auth_user_backend'] == 'django.contrib.auth.backends.RemoteUserBackend':
            form = LIGOSearchForm()
        else:
            form = SearchForm()
        return render(request, 'form.html', {'form': form})
    else:
        return redirect(make_authorization_url())


def do_similarity_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        if request.session['_auth_user_backend'] == 'django.contrib.auth.backends.RemoteUserBackend':
            form = LIGOSearchForm(request.GET)
        else:
            form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            SI_glitches = similarity_search(form)
            histogramurl = request.get_full_path().replace('do_similarity_search', 'histogram')

            return render(request, 'searchresults.html', {'results': SI_glitches.to_dict(orient='records'), 'histogramurl' : histogramurl})
        else:
            return render(request, 'form.html', {'form': form}) 


def similarity_search_restful_API(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            SI_glitches = similarity_search(form)
            SI_glitches = SI_glitches[['ifo', 'peak_frequency', 'links_subjects', 'Label', 'searchedID', 'snr', 'uniqueID', 'searchedzooID', 'imgUrl4', 'imgUrl3', 'imgUrl2', 'imgUrl1']]

            return JsonResponse(SI_glitches.to_dict(orient='list'))


def do_collection_creation(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            SI_glitches = similarity_search(form)
            howmany = int(form.cleaned_data['howmany'])
            collection_url = create_collection(request, SI_glitches)

            engine = create_engine('postgresql://{0}:{1}@gravityspy.ciera.northwestern.edu:5432/gravityspy'.format(os.environ['GRAVITYSPY_DATABASE_USER'], os.environ['GRAVITYSPY_DATABASE_PASSWD']))
            searchquery = pd.DataFrame({'search_created_at' : pd.to_datetime('now'), 'uniqueid_searched' : SI_glitches['searchedID'].iloc[0], 'zooid_searched' : int(SI_glitches['searchedzooID'].iloc[0]), 'user': request.user.username, 'returned_ids' : ','.join(SI_glitches.links_subjects.apply(str).tolist()), 'howmany': howmany}, index=[0])
            searchquery.to_sql('searchlog', engine, if_exists='append', index=False)

            return render(request, 'createcollection.html', {'urls' : {collection_url}, 'results': SI_glitches.to_dict(orient='records')})
        else:
            return render(request, 'form.html', {'form': form})


def histogram(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['imageid']:
                uniqueID = str(form.cleaned_data['imageid'])
            else:
                uniqueID = form.cleaned_data['imageid']
            if form.cleaned_data['zooid']:
                zooID = float(str(form.cleaned_data['zooid']))
            else:
                zooID = form.cleaned_data['zooid']
            database = str(form.cleaned_data['database'])
            fig = make_histogram(uniqueID, zooID, database)
            canvas = FigureCanvas(fig)
            response = HttpResponse(content_type='image/png')
            canvas.print_png(response)
            fig.clear()
            return response


def runhveto(request):
    import os, string, random

    def id_generator(size=5, chars=string.ascii_uppercase + string.digits +string.ascii_lowercase):
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    ID = id_generator(size=10)
    os.makedirs(os.path.join('static', 'hveto', ID))
    imagepath = os.path.join('static', 'hveto', ID, ID + '.log')
    proc = subprocess.Popen(
        ["ligo-proxy-init --help"],
        #["gsissh ldas-pcdev2.ligo.caltech.edu '. /home/scoughlin/Project/opt/GravitySpy-py27/bin/activate; hveto 1131580817 1131667217 --ifo L1 --config-file /home/scoughlin/hveto/h1l1-hveto-daily-o2.ini -p /home/scoughlin/hveto/cache.lcf -o ~/public_html/HVeto/L1/Blip/1131580817-1131667217 --nproc 10 -a /home/scoughlin/hveto/l1-01.lcf'"],             #call something with a lot of output so we can see it
        stdout=open(imagepath, 'a+'),
        stderr=open(imagepath, 'a+'),
    )

    return redirec('https://ldas-jobs.ligo.caltech.edu/~scoughlin/HVeto/L1/Blip/1131580817-1131667217/')
