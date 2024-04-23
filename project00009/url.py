from django.contrib import admin
from django.urls import path,include,re_path

from . import api
from . import user

urlpatterns=[
    re_path(r"^signin$",user.signin,name="signin"),
    re_path(r"^signup$",user.signup,name="signup"),
    re_path(r"^signout$",user.signout,name="signout"),
]