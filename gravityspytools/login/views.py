# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .utils import get_token, get_username
# Create your views here.
def login(request):
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your reddit username is: %s" % get_username(access_token)
