from django.contrib import admin
from django.urls import path,include,re_path

from . import api

urlpatterns=[
    re_path(r"^getwarnlist/(?P<guildid>[^\/]+)$",api.getwarnlist,name="getwarnlist"),
]