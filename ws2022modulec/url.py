from django.contrib import admin
from django.urls import path,include

from . import index
from . import user
from . import admin

urlpatterns=[
    path("login",index.login,name="login"),
    path("login/google",index.logingoogle,name="logingoogle"),
    path("signup",index.signup,name="signup"),
    path("logout/<str:token>",user.logout,name="logout"),

    path("getuser/<str:token>",user.getuser,name="getuser"),
    path("edituser",user.edituser,name="edituser"),
    path("newans/<str:questionid>",user.newans,name="newans"),

    path("getquestionlist",admin.getquestionlist,name="getquestionlist"),
    path("getquestion/<str:id>",admin.getquestion,name="getquestion"),
    path("newquestion",admin.newquestion,name="newquestion"),
    path("editquestion/<str:id>",admin.editquestion,name="editquestion"),
    path("delquestion/<str:id>",admin.delquestion,name="delquestion"),
    path("getuserlist",admin.getuserlist,name="getuserlist"),
    path("getlog",admin.getlog,name="getlog"),
]