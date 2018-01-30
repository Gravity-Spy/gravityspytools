from django.conf.urls import url
  
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^make_subjectset_from_collection/$', views.make_subjectset_from_collection, name='make_subjectset_from_collection'),
]
