from django.contrib import admin
from django.urls import path,include

from . import index
from . import game
from . import admin

urlpatterns=[
    path("api/v1/auth/signup",index.signup,name="signup"),
    path("api/v1/auth/signin",index.signin,name="signin"),
    path("api/v1/auth/signout",index.signout,name="signout"),
    path("api/v1/games",game.getgamelist,name="getgamelist"),
    path("api/v1/games",game.newgame,name="newgame"),
    path("api/v1/games/<str:slug>",game.getgame,name="getgame"),
    # path("api/v1/games/:slug/upload",index.signup,name="signup"),
    # path("games/:slug/:version",index.signup,name="signup"),
    path("api/v1/games/<str:slug>",game.editgame,name="editgame"),
    path("api/v1/games/<str:slug>",game.delgame,name="delgame"),
    path("api/v1/users/<str:username>",index.signup,name="signup"),
    path("api/v1/games/<str:slug>/scores",index.signup,name="signup"),
]