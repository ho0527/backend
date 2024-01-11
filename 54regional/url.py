from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import admin
from . import comment
from . import room

urlpatterns=[
    # question/
    # comment
    re_path(r"^getcommentlist$",comment.getcommentlist,name="getcommentlist"),
    re_path(r"^getcomment/(?P<id>[^\/]+)$",comment.getcomment,name="getcomment"),
    re_path(r"^newcomment$",comment.newcomment,name="newcomment"),
    re_path(r"^editcomment/(?P<id>[^\/]+)$",comment.editcomment,name="editcomment"),
    re_path(r"^deletecomment/(?P<id>[^\/]+)$",comment.deletecomment,name="deletecomment"),

    # room
    re_path(r"^getleftroom/(?P<date>[^\/]+)/(?P<month>[^\/]+)$",room.getleftroom,name="getleftroom"),
    re_path(r"^getroomlist$",room.getroomlist,name="getroomlist"),
    re_path(r"^getroom/(?P<id>[^\/]+)$",room.getroom,name="getroom"),
    re_path(r"^newroom$",room.newroom,name="newroom"),
    re_path(r"^editroom/(?P<id>[^\/]+)$",room.editroom,name="editroom"),
    re_path(r"^deleteroom/(?P<id>[^\/]+)$",room.deleteroom,name="deleteroom"),

    # admin
    re_path(r"^admindeletecomment/(?P<id>[^\/]+)$",admin.deletecomment,name="admindeletecomment"),
    re_path(r"^adminresponsecomment/(?P<id>[^\/]+)$",admin.responsecomment,name="adminresponsecomment"),
    re_path(r"^adminpincomment/(?P<id>[^\/]+)$",admin.pincomment,name="adminpincomment"),

    # self/
]