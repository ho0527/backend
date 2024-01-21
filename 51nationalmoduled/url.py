from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import user
from . import house

urlpatterns=[
    re_path(r"^api/user/login$",user.signin,name="signin"),
    re_path(r"^api/user/logout$",user.signout,name="signout"),
    re_path(r"^api/user/register$",user.signup,name="signup"),

    re_path(r"^api/house$",house.getposthouse,name="getposthouse"),
    re_path(r"^api/house/:house_id$",index.searchtrain,name=""),
    re_path(r"^api/user/house$",index.searchtrain,name=""),
    re_path(r"^api/application$",index.searchtrain,name=""),
    re_path(r"^api/application/:application_id$",index.searchtrain,name=""),

    re_path(r"^api/ads$",index.searchtrain,name=""),
    re_path(r"^api/ads/:ad_id$",index.searchtrain,name=""),
]