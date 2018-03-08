import os
import requests
import requests.auth
import urllib

def make_authorization_url(
    REDIRECT_URI=os.environ['REDIRECT_URI'],
    CLIENT_ID=os.environ['PANOPTES_CLIENT_ID'],
    BASE_URL='https://panoptes.zooniverse.org/oauth/authorize'):

    params = {"client_id": CLIENT_ID,
        "response_type" : "code",
        "redirect_uri" : REDIRECT_URI,
        "scope" : 'user',
        "scope" : 'public',
             }
    return BASE_URL + '?' + urllib.urlencode(params)


def get_token(code,
    REDIRECT_URI=os.environ['REDIRECT_URI'],
    CLIENT_ID=os.environ['PANOPTES_CLIENT_ID'],
    CLIENT_SECRET=os.environ['PANOPTES_CLIENT_SECRET']):

    #client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI,
                 "client_id" : CLIENT_ID,
                 "client_secret" : CLIENT_SECRET,
                 }
    response = requests.post("https://panoptes.zooniverse.org/oauth/token",
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]


def get_username(access_token):
    headers = {'Accept': 'application/vnd.api+json; version=1',
           'Content-Type': 'application/json',
           "Authorization": "Bearer " + str(access_token)}
    response = requests.get("https://panoptes.zooniverse.org/api/me", headers=headers)
    if response.ok:
        me_json = response.json()
        return me_json['users'][0]['display_name']
