# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render, redirect

from login.utils import make_authorization_url
from collection_to_subjectset.utils import retrieve_subjects_from_collection

from .forms import NewClassForm
from .models import NewClass

from gwpy.table import EventTable

def index(request):
    if request.user.is_authenticated:
        form = NewClassForm()
        return render(request, 'retrain-model-form.html', {'form': form})
    else:
        return redirect(make_authorization_url())


def retrain_model(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = NewClassForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            collection_owner = str(form.cleaned_data['collection_owner'])
            collection_name = str(form.cleaned_data['collection_name'])
            new_class_name = str(form.cleaned_data['new_class_name'])

            # First determine the subjects attempting to be added to the training set
            subjects_in_collection, tmp = retrieve_subjects_from_collection(collection_owner, collection_name)
            subjects_in_collection = [str(isubject) for isubject in subjects_in_collection]

            new_subjects = list(EventTable.fetch('gravityspy',
                                                 'glitches WHERE CAST(links_subjects AS FLOAT) IN ({0})'.format(str(",".join(subjects_in_collection))),
                                                  columns=["gravityspy_id"], host='gravityspyplus.ciera.northwestern.edu')['gravityspy_id'])

            requested_model, created = NewClass.objects.get_or_create(collection_owner=collection_owner,
                                                                      collection_name=collection_name,
                                                                      new_class_name=new_class_name,
                                                                      new_subjects=new_subjects,
                                                                      user=request.user)
            requested_model.save()

            return render(request, 'temp.html') 
        else:
            return render(request, 'retrain-model-form.html', {'form': form})
