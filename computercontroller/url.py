from django.contrib import admin
from django.urls import path,include,re_path

from . import api
from . import screen

urlpatterns=[
    re_path(r"^signin$",api.signin,name="signin"),
    re_path(r"^screen/(?P<screenid>[^\/]+)$",screen.getscreen,name="screen"),
]