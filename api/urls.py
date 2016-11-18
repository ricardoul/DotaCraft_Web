from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.match_list),
    url(r'^(?P<pk>[0-9]+)$', views.match_detail),

    #ladder
    #player
]

urlpatterns = format_suffix_patterns(urlpatterns)