from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import user
from . import album
from . import music

urlpatterns=[
    re_path(r"^signin$",index.signin,name="signin"),
    re_path(r"^signup$",index.signup,name="signup"),
    re_path(r"^signout$",index.signout,name="signout"),

    re_path(r"^getuser/(?P<userid>[^\/]+)$",user.getuser,name="getuser"),
    re_path(r"^getuserlist$",user.getuserlist,name="getuserlist"),
    re_path(r"^edituser/(?P<userid>[^\/]+)$",user.edituser,name="edituser"),
    re_path(r"^edituserpermission/(?P<userid>[^\/]+)$",user.edituserpermission,name="edituserpermission"),
    re_path(r"^deluser/(?P<userid>[^\/]+)$",user.deleteuser,name="deluser"),

    re_path(r"^newalbum$",index.signin,name="newalbum"),
    re_path(r"^getalbum/(?P<albumid>[^\/]+)$",index.signin,name="getalbum"),
    re_path(r"^getalbumlist$",index.signin,name="getalbumlist"),
    re_path(r"^editalbum/(?P<albumid>[^\/]+)$",index.signin,name="editalbum"),
    re_path(r"^delalbum/(?P<albumid>[^\/]+)$",index.signin,name="delalbum"),

    re_path(r"^newmusic$",index.signin,name="newmusic"),
    re_path(r"^getmusic/(?P<musicid>[^\/]+)$",index.signin,name="getmusic"),
    re_path(r"^getmusiclist$",index.signin,name="getmusiclist"),
    re_path(r"^editmusic/(?P<musicid>[^\/]+)$",index.signin,name="editmusic"),
    re_path(r"^delmusic/(?P<musicid>[^\/]+)$",index.signin,name="delmusic"),

    re_path(r"^getlog$",album.getalbum,name="getlog"),
    re_path(r"^getapi$",album.getalbum,name="getapi"),

    re_path(r".+",index.error404,name="404"),
]