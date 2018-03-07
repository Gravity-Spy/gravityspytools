# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from .utils import get_token, get_username
from django.http import HttpResponse
from home.views import index

# Create your views here.
def login(request):
    if request.method == 'GET':
        if request.GET.get('error', ''):
            return HttpResponse(request.GET.get('error'))
        code = request.GET.get('code')
        access_token = get_token(code)
        request.user.is_authenticated = True
        # Note: In most cases, you'll want to store the access token, in, say,
        # a session for use in other parts of your web app.
        return index(request)
