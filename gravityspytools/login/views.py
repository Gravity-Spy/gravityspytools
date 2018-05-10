# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from .utils import get_token, get_username
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import requests

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.GET.get('error', ''):
            return HttpResponse(request.GET.get('error'))
        code = request.GET.get('code')
        access_token, expires_in, refresh_token, token_start_time = get_token(code)
        user = authenticate(request,
                            token=access_token)
        if user is not None:
            auth_login(request, user)
            request.session["access_token"] = access_token
            request.session["expires_in"] = expires_in
            request.session["refresh_token"] = refresh_token
            request.session["token_start_time"] = token_start_time
            return redirect('/')
        else:
            return HttpResponse("Logging in Failed")
