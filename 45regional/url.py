from django.contrib import admin
from django.urls import path,include

from . import index
from . import admin
from . import product

urlpatterns=[
    path("login",index.login,name="login"),
    path("logout/<str:id>",index.logout,name="logout"),

    path("getuserlist",admin.getuserlist,name="getuserlist"),
    path("getuser/<str:id>",admin.getuser,name="getuser"),
    path("getlog",admin.log,name="getlog"),
    path("newuser",admin.newuser,name="newuser"),
    path("editdeluser/<str:id>",admin.editdeluser,name="editdeluser"),

    path("getproduct",product.getproduct,name="getproduct"),
    path("gettemplate",product.gettemplate,name="gettemplate"),
    path("newproduct",product.newproduct,name="newproduct"),
    path("newtemplate",product.newtemplate,name="newtemplate"),
]