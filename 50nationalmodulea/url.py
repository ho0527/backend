from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import user
from . import album
from . import music

urlpatterns=[
    re_path("^signin$",index.signin,name="signin"),
    re_path("^signup$",index.signup,name="signup"),
    re_path("^signout$",index.signout,name="signout"),

    re_path("^getuser/(?P<userid>[^\/]+)$",index.signin,name="getuser"),
    re_path("^getuserlist$",index.signin,name="getuserlist"),
    re_path("^edituser/(?P<userid>[^\/]+)$",index.signin,name="edituser"),
    re_path("^edituserpermission/(?P<userid>[^\/]+)$",index.signin,name="edituserpermission"),
    re_path("^deluser/(?P<userid>[^\/]+)$",index.signin,name="deluser"),

    re_path("^newalbum$",index.signin,name="newalbum"),
    re_path("^getalbum/(?P<albumid>[^\/]+)$",index.signin,name="getalbum"),
    re_path("^getalbumlist$",index.signin,name="getalbumlist"),
    re_path("^editalbum/(?P<albumid>[^\/]+)$",index.signin,name="editalbum"),
    re_path("^delalbum/(?P<albumid>[^\/]+)$",index.signin,name="delalbum"),

    re_path("^newmusic$",index.signin,name="newmusic"),
    re_path("^getmusic/(?P<musicid>[^\/]+)$",index.signin,name="getmusic"),
    re_path("^getmusiclist$",index.signin,name="getmusiclist"),
    re_path("^editmusic/(?P<musicid>[^\/]+)$",index.signin,name="editmusic"),
    re_path("^delmusic/(?P<musicid>[^\/]+)$",index.signin,name="delmusic"),

    re_path("^getlog$",album.game,name="getlog"),
    re_path("^getapi$",album.game,name="getapi"),

    re_path(".+",index.error404,name="404"),
]