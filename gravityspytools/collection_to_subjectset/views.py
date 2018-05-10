# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, redirect

import panoptes_client
import os

from .forms import SearchForm
from .utils import retrieve_subjects_from_collection
from login.utils import make_authorization_url
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated():
        form = SearchForm()
        return render(request, 'subjectset_from_collection_form.html', {'form': form})
    else:
        return redirect(make_authorization_url())


# Create your views here.
def make_subjectset_from_collection(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])
            workflow_name = str(form.cleaned_data['workflow_name'])

            client = panoptes_client.Panoptes()
            client.connect(username=os.environ.get('PANOPTES_USERNAME'), password=os.environ.get('PANOPTES_PASSWORD'))

            subjects_in_collection, collection_display_url = retrieve_subjects_from_collection(username, collection_display_name)
            subject_set = panoptes_client.SubjectSet()

            subject_set.links.project = '6040'
            subject_set.display_name = '{0}'.format(collection_display_name)

            subject_set.save()
            subject_set.add(subjects_in_collection)

            workflow = panoptes_client.Workflow()
            workflow.display_name = '{0}'.format(workflow_name)
            workflow.links.project = '6040'
            workflow.primary_language ='en'
            image_location_str = "![Example Alt Text]({0} =400x275)".format(collection_display_url)
            workflow.tasks = {u'T0': {u'answers': [{u'label': u'Yes'}, {u'label': u'No'}],
              u'help': u'',
              u'question': u'Does this image look like \n{0}'.format(image_location_str),
              u'required': True,
              u'type': u'single'}
            }
            workflow.first_task = "T0"
            workflow.save()

            workflow.add_subject_sets(subject_set)

            return redirect("https://www.zooniverse.org/projects/sbc538/vet-new-classes") 
        else:
            return render(request, 'subjectset_from_collection_form.html', {'form': form})
