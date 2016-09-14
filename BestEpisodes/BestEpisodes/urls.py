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
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^rankings/$', core_views.rankings, name='rankings'),
    url(r'^episode/(?P<episode_id>\d+)/$', core_views.episode_detail_no_slug, name='episode_detail_no_slug'),
    url(r'^episode/(?P<episode_id>\d+)/(?P<episode_slug>[\w\-]+)/$', core_views.episode_detail, name='episode_detail'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^season/(?P<season_id>\d+)/$', core_views.season_detail, name='season_detail'),
    url(r'^rankings/season/$', core_views.season_rankings, name='season_rankings'),

]
