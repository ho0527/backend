from django.contrib import admin
from django.urls import path,include,re_path

from . import api

urlpatterns=[
    re_path(r"^gettodo/(?P<id>.+)$",api.gettodo,name="gettodo"),
    re_path(r"^edittodo/(?P<id>.+)$",api.edittodo,name="edittodo"),
]