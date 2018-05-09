from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do_similarity_search/$', views.do_similarity_search, name='do_similarity_search'),
    url(r'^get_imageids/$', views.get_imageids, name='get_imageids'),
    url(r'^get_zooids/$', views.get_zooids, name='get_zooids'),
    url(r'^get_gpstimes/$', views.get_gpstimes, name='get_gpstimes'),
    url(r'^do_collection_creation/$', views.do_collection_creation, name='do_collection_creation'),
    url(r'^similarity_search_restful_API/$', views.similarity_search_restful_API, name='similarity_search_restful_API'),
    url(r'^histogram/$', views.histogram, name='histogram'),
    url(r'^runhveto/$', views.runhveto, name='runhveto'),
]
