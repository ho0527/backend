from django.contrib import admin
from django.urls import path,include,re_path

from . import api

urlpatterns=[
    re_path(r"^gettodo/(?P<id>.+)$",api.gettodo,name="gettodo"),
    re_path(r"^edittodo/(?P<id>.+)$",api.edittodo,name="edittodo"),
    re_path(r"^getcalendar/(?P<id>.+)$",api.getcalendar,name="getcalendar"),
    re_path(r"^editcalendar/(?P<id>.+)$",api.editcalendar,name="editcalendar"),
]