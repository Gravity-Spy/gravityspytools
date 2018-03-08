# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from .utils import get_token, get_username
from django.http import HttpResponse
import requests

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.GET.get('error', ''):
            return HttpResponse(request.GET.get('error'))
        code = request.GET.get('code')
        access_token = get_token(code)
        request.session["access_token"] = access_token
        return HttpResponse(get_username(access_token))
