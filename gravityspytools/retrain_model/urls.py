from django.conf.urls import url

from . import views

app_name = 'retrain_model'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^retrain-model/$', views.retrain_model, name='retrain_model'),
]
