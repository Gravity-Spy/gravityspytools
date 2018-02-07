from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do_DB_search/$', views.do_DB_search, name='do_DB_search'),
]
