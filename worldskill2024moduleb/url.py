from django.contrib import admin
from django.urls import path,include,re_path

from . import company
from . import index
from . import admin

urlpatterns=[
    re_path("^getdeactivatecompanylist$",company.getdeactivatecompanylist,name="getdeactivatecompanylist"),
    re_path("^getcompanylist$",company.getcompanylist,name="getcompanylist"),
    re_path("^getcompany/(?P<id>.+)$",company.getcompany,name="getcompany"),
    re_path("^newcompany$",company.newcompany,name="newcompany"),
    re_path("^editcompany/(?P<id>.+)$",company.editcompany,name="editcompany"),
    re_path("^deactivatecompany/(?P<id>.+)$",company.deactivatecompany,name="deactivatecompany"),
    # re_path("^api/v1/auth/signin$",index.signin,name="signin"),
    # re_path("^api/v1/auth/signout$",index.signout,name="signout"),
    # re_path("^api/v1/games$",game.game,name="game"),
    # re_path("^api/v1/games/(?P<slug>[^\/]+)$",game.gameid,name="getgame"),
    # re_path("^api/v1/games/(?P<slug>.+)/upload$",game.uploadgame,name="uploadgame"),
    # re_path("^api/v1/users/(?P<username>.+)$",index.getuser,name="getuser"),
    # re_path("^api/v1/games/(?P<slug>.+)/scores$",game.score,name="score"),
    re_path(".+",index.error404,name="404"),
]