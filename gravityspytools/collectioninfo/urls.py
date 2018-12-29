from django.conf.urls import url

from . import views

app_name = 'collectioninfo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collection-info/$', views.collectioninfo, name='collectioninfo'),
    url(r'^dategraph/$', views.dategraph, name='dategraph'),
]
