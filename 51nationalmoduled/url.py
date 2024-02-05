from django.contrib import admin
from django.urls import path,include,re_path

from . import ads
from . import application
from . import user
from . import house

urlpatterns=[
    re_path(r"^api/user/login$",user.signin,name="signin"),
    re_path(r"^api/user/logout$",user.signout,name="signout"),
    re_path(r"^api/user/register$",user.signup,name="signup"),

    re_path(r"^api/house$",house.getposthouse,name="getposthouse"),
    re_path(r"^api/house/(?P<houseid>[^\/]+)$",house.gedhouse,name="geteditdeletehouse"),
    re_path(r"^api/user/house$",house.getuserhouse,name="getuserhouse"),

    re_path(r"^api/application$",application.getpostapplication,name="getpostapplication"),
    re_path(r"^api/application/(?P<applicationid>[^\/]+)$",application.editdeleteapplication,name="editdeleteapplication"),

    re_path(r"^api/ads$",ads.getads,name="getads"),
    re_path(r"^api/ads/(?P<adsid>[^\/]+)$",ads.deleteads,name="deleteads"),
]