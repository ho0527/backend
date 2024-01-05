from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import game
from . import admin

urlpatterns=[
    re_path("^api/v1/auth/signup$",index.signup,name="signup"),
    re_path("^api/v1/auth/signin$",index.signin,name="signin"),
    re_path("^api/v1/auth/signout$",index.signout,name="signout"),
    re_path("^api/v1/games$",game.game,name="game"),
    re_path("^api/v1/games/(?P<slug>[^\/]+)$",game.gameid,name="getgame"),
    re_path("^api/v1/games/(?P<slug>.+)/upload$",game.uploadgame,name="uploadgame"),
    re_path("^api/v1/users/(?P<username>.+)$",index.getuser,name="signup"),
    re_path("^api/v1/games/(?P<slug>.+)/scores$",game.score,name="signup"),
    re_path(".+",index.error404,name="404"),
]