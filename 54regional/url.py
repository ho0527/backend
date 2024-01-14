from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import admin
from . import comment
from . import room
from . import food

urlpatterns=[
    # question/
    # comment
    re_path(r"^getcommentlist$",comment.getcommentlist,name="getcommentlist"),
    re_path(r"^getcomment/(?P<id>[^\/]+)$",comment.getcomment,name="getcomment"),
    re_path(r"^newcomment$",comment.newcomment,name="newcomment"),
    re_path(r"^editcomment/(?P<id>[^\/]+)$",comment.editcomment,name="editcomment"),
    re_path(r"^deletecomment/(?P<id>[^\/]+)$",comment.deletecomment,name="deletecomment"),

    # roomorder
    re_path(r"^getleftroom/(?P<date>[^\/]+)/(?P<month>[^\/]+)$",room.getleftroom,name="getleftroom"),
    re_path(r"^getroomorderlist$",room.getroomorderlist,name="getroomorderlist"),
    re_path(r"^getroomorder/(?P<id>[^\/]+)$",room.getroomorder,name="getroomorder"),
    re_path(r"^newroomorder$",room.newroomorder,name="newroomorder"),
    re_path(r"^editroomorder/(?P<id>[^\/]+)$",room.editroomorder,name="editroomorder"),
    re_path(r"^deleteroomorder/(?P<id>[^\/]+)$",room.deleteroomorder,name="deleteroomorder"),

    # food
    re_path(r"^getfoodlist$",food.getfoodlist,name="getfoodlist"),
    re_path(r"^getfood/(?P<id>[^\/]+)$",food.getfood,name="getfood"),
    re_path(r"^newfoodorder$",food.newfoodorder,name="newfoodorder"),
    re_path(r"^editfood/(?P<id>[^\/]+)$",food.editfood,name="editfood"),
    re_path(r"^deletefood/(?P<id>[^\/]+)$",food.deletefood,name="deletefood"),

    # admin
    re_path(r"^admindeletecomment/(?P<id>[^\/]+)$",admin.deletecomment,name="admindeletecomment"),
    re_path(r"^adminresponsecomment/(?P<id>[^\/]+)$",admin.responsecomment,name="adminresponsecomment"),
    re_path(r"^adminpincomment/(?P<id>[^\/]+)$",admin.pincomment,name="adminpincomment"),

    # self/
]