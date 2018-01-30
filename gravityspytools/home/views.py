# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', context={'apps': {('search', 'Similarity Search'), ('collection_to_subjectset', 'Create a Workflow to Vet a Collection')}})
