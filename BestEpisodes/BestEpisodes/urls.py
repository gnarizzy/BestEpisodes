"""BestEpisodes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^songs/$', core_views.rankings, name='rankings'),
    url(r'^song/(?P<song_id>\d+)/$', core_views.song_detail_no_slug, name='song_detail_no_slug'),
    url(r'^song/(?P<song_id>\d+)/(?P<song_slug>[\w\-]+)/$', core_views.song_detail, name='song_detail'),
    url(r'^about/$',core_views.about, name='about'),
    url(r'^album/(?P<album_id>\d+)/$', core_views.album_detail, name='album_detail'),
    url(r'^albums/$', core_views.album_rankings, name='album_rankings'),

]
