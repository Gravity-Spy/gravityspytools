# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from login.utils import make_authorization_url

# Create your views here.
def index(request):
    return render(request, 'index.html', context={'loginurl': make_authorization_url()})
