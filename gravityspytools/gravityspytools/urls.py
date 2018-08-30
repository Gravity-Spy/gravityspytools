"""gravityspytools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from home import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/', include('login.urls'), name='login'),
    url(r'^logout/', include('logout.urls'), name='logout'),
    url(r'^label/', include('label.urls'), name='label'),
    url(r'^retrain-model/', include('retrain_model.urls'), name='retrain_model'),
    url(r'^search/', include('search.urls'), name='search'),
    url(r'^display-glitches-db/', include('display_glitches_DB.urls'), name='display_glitches_DB'),
    url(r'^collection-info/', include('collectioninfo.urls'), name='collectioninfo'),
    url(r'^collection-to-subject-set/', include('collection_to_subjectset.urls'), name='collection_to_subjectset'),
    url(r'^admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns+= static(settings.STATIC_URL)
