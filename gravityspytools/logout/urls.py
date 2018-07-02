from django.conf.urls import url
from . import views

appname = 'logout'
urlpatterns = [
    url(r'^$', views.logout, name='logout'),
]
