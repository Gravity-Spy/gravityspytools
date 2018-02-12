from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^similarity_search_with_GPS/$', views.similarity_search_with_GPS, name='similarity_search_with_GPS'),
    url(r'^similarity_search_with_GPS_restful_API/$', views.similarity_search_with_GPS_restful_API, name='similarity_search_with_GPS_restful_API'),
]
