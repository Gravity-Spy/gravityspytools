from django.conf.urls import url
from . import views
from rest_framework_jwt.views import verify_jwt_token

appname = 'login'
urlpatterns = [
    url(r'^$', views.login, name='login'),
]
