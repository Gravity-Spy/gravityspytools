from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do_similarity_search/$', views.do_similarity_search, name='do_similarity_search'),
    url(r'^get_imageids/$', views.get_imageids, name='get_imageids'),
    url(r'^get_zooids/$', views.get_zooids, name='get_zooids'),
    url(r'^do_collection_creation/$', views.do_collection_creation, name='do_collection_creation'),
]
