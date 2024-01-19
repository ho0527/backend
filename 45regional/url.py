from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import admin
from . import todo

urlpatterns=[
    re_path(r"^login$",index.login,name="login"),
    re_path(r"^logout/(?P<id>.+)$",index.logout,name="logout"),

    re_path(r"^getuser/(?P<id>.+)$",admin.getuser,name="getuser"),
    re_path(r"^getuserlist$",admin.getuserlist,name="getuserlist"),
    re_path(r"^getlog$",admin.log,name="getlog"),
    re_path(r"^signup$",admin.signup,name="signup"),
    re_path(r"^editdeluser/(?P<id>.+)$",admin.editdeluser,name="editdeluser"),

    re_path(r"^gettodo/(?P<id>.+)$",todo.gettodo,name="gettodo"),
    re_path(r"^gettodolist$",todo.gettodolist,name="gettodolist"),
    re_path(r"^newtodo$",todo.newtodo,name="newtodo"),
    re_path(r"^edittodo/(?P<id>.+)$",todo.edittodo,name="edittodo"),
    re_path(r"^deletetodo/(?P<id>.+)$",todo.deletetodo,name="deletetodo"),
]