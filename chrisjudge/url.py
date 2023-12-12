from django.contrib import admin
from django.urls import path,include

from . import index
from . import user
from . import admin

urlpatterns=[
    path("login",index.login,name="login"),
    path("login/thirdpartylogin/<str:type>",index.thirdpartylogin,name="thirdpartylogin"),
    path("signup",index.signup,name="signup"),
    path("logout/<str:token>",index.logout,name="logout"),
    path("logincheck",index.logincheck,name="logincheck"),

    path("getuser/<str:token>",user.getuser,name="getuser"),
    path("edituser",user.edituser,name="edituser"),
    path("newresponse/<str:questionid>",user.newresponse,name="newresponse"),
    path("getresponse",user.getresponse,name="getresponse"),
    path("getresponselist",user.getresponselist,name="getresponselist"),
    path("getscorelist",user.getscorelist,name="getscorelist"),

    path("getquestionlist",admin.getquestionlist,name="getquestionlist"),
    path("getquestion/<str:id>",admin.getquestion,name="getquestion"),
    path("newquestion",admin.newquestion,name="newquestion"),
    path("editquestion/<str:id>",admin.editquestion,name="editquestion"),
    path("delquestion/<str:id>",admin.delquestion,name="delquestion"),
    path("getuserlist",admin.getuserlist,name="getuserlist"),
    path("getlog",admin.getlog,name="getlog"),
]