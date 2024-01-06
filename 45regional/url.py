from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import admin
from . import todo

urlpatterns=[
    re_path("^login$",index.login,name="login"),
    re_path("^logout/(?P<id>.+)$",index.logout,name="logout"),

    re_path("^getuserlist$",admin.getuserlist,name="getuserlist"),
    re_path("^getuser/(?P<id>.+)$",admin.getuser,name="getuser"),
    re_path("^getlog$",admin.log,name="getlog"),
    re_path("^signup$",admin.signup,name="signup"),
    re_path("^editdeluser/(?P<id>.+)$",admin.editdeluser,name="editdeluser"),

    re_path("^newtodo$",todo.newtodo,name="newtodo"),
    re_path("^gettodolist$",todo.gettodolist,name="gettodolist"),
    re_path("^edittodo/(?P<id>.+)$",todo.edittodo,name="edittodo"),
    re_path("^deletetodo/(?P<id>.+)$",todo.deletetodo,name="deletetodo"),
]