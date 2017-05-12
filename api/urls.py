from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.match_list),
    url(r'^matches/?$', views.match_list),
    url(r'^matches/(?P<pk>[0-9]+)$', views.match_detail),
    url(r'^players/?$', views.player_list),
    url(r'^players/(?P<pk>[0-9]+)$', views.player_detail),
    url(r'^matches/create/$', views.create_random_matches)
    #ladder
]

urlpatterns = format_suffix_patterns(urlpatterns)