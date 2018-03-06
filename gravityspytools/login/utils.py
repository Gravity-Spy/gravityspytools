import os
import requests
import urllib

def make_authorization_url(
    REDIRECT_URI="https://gravityspytools.ciera.northwestern.edu/login",
    CLIENT_ID=os.environ['PANOPTES_CLIENT_ID'],
    BASE_URL='https://panoptes.zooniverse.org/oauth/authorize'):

    params = {"client_id": CLIENT_ID,
        "response_type" : "code",
        "redirect_uri" : REDIRECT_URI,
        "scope" : 'user'
             }
    return BASE_URL + '?' + urllib.urlencode(params)


def get_token(code, REDIRECT_URI,
    CLIENT_ID=os.environ['PANOPTES_CLIENT_ID'],
    CLIENT_SECRET=os.environ['PANOPTES_CLIENT_SECRET']):

    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://panoptes.zooniverse.org/oauth/token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]
    
    
def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://panoptes.zooniverse.org/api/me", headers=headers)
    me_json = response.json()
    return me_json['name']
