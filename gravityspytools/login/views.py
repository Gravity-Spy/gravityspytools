# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import redirect
from .utils import get_token, get_username
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from home.views import index
import requests

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.GET.get('error', ''):
            return HttpResponse(request.GET.get('error'))
        code = request.GET.get('code')
        access_token = get_token(code)
        try:
            headers = {'Accept': 'application/vnd.api+json; version=1',
                   'Content-Type': 'application/json',
                   "Authorization": "bearer " + str(access_token)}
            response = requests.get("https://panoptes.zooniverse.org/api/me", headers=headers)
            print response
            response.json()
        except:
            headers = {"Authorization": "bearer " + str(access_token)}
            print headers
            response = requests.get("https://panoptes.zooniverse.org/api/me", headers=headers)

        print(response)
        if response.ok:
            me_json = response.json()
            return HttpResponse(me_json['name'])
        else:
            return HttpResponse("Failed")
        #headers = {'Accept': 'application/vnd.api+json; version=1',
        #           'Content-Type': 'application/json'}
        #headers = {}
        #headers.update({"Authorization": "Bearer " + access_token})
        #response = requests.get("https://www.zooniverse.org/api/me", headers=headers)
        #print response
        #request.session["access_token"] = access_token
        #user = authenticate(access_token=access_token)
        #print user
        #if user is not None:
        #    login(request, user)
        #return redirect('/')


def logout(request):
    logout(request)
    return redirect('/')
