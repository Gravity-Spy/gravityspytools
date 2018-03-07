from django.conf.urls import url
from . import views

appname = 'login'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
]
