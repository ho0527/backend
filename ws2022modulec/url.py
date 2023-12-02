from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import game
from . import admin

urlpatterns=[
    re_path("api/v1/auth/signup",index.signup,name="signup"),
    re_path("api/v1/auth/signin",index.signin,name="signin"),
    re_path("api/v1/auth/signout",index.signout,name="signout"),
    re_path("api/v1/games",game.getgamelist,name="getgamelist"),
    re_path("api/v1/games",game.newgame,name="newgame"),
    re_path("api/v1/games/<str:slug>",game.getgame,name="getgame"),
    # path("api/v1/games/:slug/upload",index.signup,name="signup"),
    # path("games/:slug/:version",index.signup,name="signup"),
    re_path("api/v1/games/<str:slug>",game.editgame,name="editgame"),
    re_path("api/v1/games/<str:slug>",game.delgame,name="delgame"),
    re_path("api/v1/users/<str:username>",index.signup,name="signup"),
    re_path("api/v1/games/<str:slug>/scores",index.signup,name="signup"),
    re_path(".+",index.error404,name="404"),
]