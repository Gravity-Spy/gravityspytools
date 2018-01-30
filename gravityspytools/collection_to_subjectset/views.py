# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render

import panoptes_client

from .forms import SearchForm
from .utils import retrieve_subjects_from_collection


def index(request):
    form = SearchForm()
    return render(request, 'subjectset_from_collection_form.html', {'form': form})


# Create your views here.
def make_subjectset_from_collection(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            project = panoptes_client.Project.find(1104)
            username = str(form.cleaned_data['username'])
            collection_display_name = str(form.cleaned_data['collection_display_name'])

            subjects_in_collection = retrieve_subjects_from_collection(username, collection_display_name)
            subject_set = panoptes_client.SubjectSet()

            subject_set.links.project = project
            subject_set.display_name = '{0}'.format(collection_display_name)

            subject_set.save()
            subject_set.add(subjects_in_collection)

            #workflow = panoptes_client.Workflow()
            #workflow.display_name = '{0}'.format(collection_display_name)
            #project.add_workflows(workflow)
            #workflow.add_subject_sets(subject_set)

            return HttpResponse('Success!', content_type="text/plain")
