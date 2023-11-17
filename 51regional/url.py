from django.contrib import admin
from django.urls import path,include

from . import index
from . import admin
from . import form

urlpatterns=[
    path("signin",index.signin,name="signin"),
    path("signup",index.signup,name="signup"),
    path("signout",index.signout,name="signout"),

    path("getuserlist",admin.getuserlist,name="getuserlist"),
    path("getuser/<str:id>",admin.getuser,name="getuser"),
    path("getlog",admin.log,name="getlog"),

    # path("editdeluser/<str:id>",admin.edituser,name="editdeluser"),
]