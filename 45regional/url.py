from django.contrib import admin
from django.urls import path,include

from . import index
from . import admin
from . import todo

urlpatterns=[
    path("login",index.login,name="login"),
    path("logout/<str:id>",index.logout,name="logout"),

    path("getuserlist",admin.getuserlist,name="getuserlist"),
    path("getuser/<str:id>",admin.getuser,name="getuser"),
    path("getlog",admin.log,name="getlog"),
    path("signup",admin.signup,name="signup"),
    path("editdeluser/<str:id>",admin.editdeluser,name="editdeluser"),

    path("newtodo",todo.newtodo,name="newtodo"),
    path("gettodolist",todo.gettodolist,name="gettodolist"),
]