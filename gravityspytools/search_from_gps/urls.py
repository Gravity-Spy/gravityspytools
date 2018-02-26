from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^similarity-search-with-GPS/$', views.similarity_search_with_GPS, name='similarity_search_with_GPS'),
    url(r'^similarity-search-with-GPS-restful-API/$', views.similarity_search_with_GPS_restful_API, name='similarity_search_with_GPS_restful_API'),
]
