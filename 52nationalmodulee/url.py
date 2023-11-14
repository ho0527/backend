from django.contrib import admin
from django.urls import path,include

from . import api

urlpatterns=[
    path("newclass",api.newclass,name="newclass"),
    path("getclasslist",api.getclasslist,name="getclasslist"),
    path("getclass/<str:classid>",api.getclass,name="getclass"),
    path("newstudent",api.newstudent,name="newstudent"),
    path("getstudentlist",api.getstudentlist,name="getstudentlist"),
    path("getstudent/<str:studentid>",api.getstudent,name="getstudent"),
    path("trashstudent/<str:studentid>",api.trashstudent,name="trashstudent"),
    path("delstudent/<str:studentid>",api.delstudent,name="delstudent"),
    path("getrash",api.getrash,name="getrash"),
]