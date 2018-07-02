from django.conf.urls import url

from . import views

app_name = 'display_glitches_DB'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do-db-search/$', views.do_DB_search, name='do_DB_search'),
]
