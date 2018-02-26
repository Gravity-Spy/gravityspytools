from django.conf.urls import url
  
from . import views

app_name = 'collection_to_subjectset'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^make-subjectset-from-collection/$', views.make_subjectset_from_collection, name='make_subjectset_from_collection'),
]
