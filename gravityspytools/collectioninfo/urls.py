from django.conf.urls import url

from . import views

app_name = 'collectioninfo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collectioninfo/$', views.collectioninfo, name='collectioninfo'),
]
