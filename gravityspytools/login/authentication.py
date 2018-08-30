import requests
import sys
from django.contrib.auth.models import User


class ZooAuthenticationBackend:

    def authenticate(self, request, token=None):
        headers = {'Accept': 'application/vnd.api+json; version=1',
               'Content-Type': 'application/json',
               "Authorization": "Bearer " + str(token)}

        response = requests.get("https://panoptes.zooniverse.org/api/me", headers=headers)
        # Did the verifier respond?
        if response.ok:
            # Parse the response
            verification_data = response.json()

            # Check if the assertion was valid
            if verification_data['users'][0]['login']:
                zooniverse_username = verification_data['users'][0]['login']
                email = verification_data['users'][0]['email']
                user, created  = User.objects.get_or_create(username=zooniverse_username)
                if created:
                    user.email = email
                    user.save()
                else:
                    user.email = email
                    user.save()
                return user
            else:
                return None
        else:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
