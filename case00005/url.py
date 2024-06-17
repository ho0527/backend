from django.contrib import admin
from django.urls import path,include,re_path

from . import user
from . import post
from . import product
from . import connect

urlpatterns=[
    re_path("signincheck/?",user.signincheck,name="signincheck"),

    re_path("signup/?",user.signup,name="signup"),
    re_path("signin/?",user.signin,name="signin"),
    re_path("signout/?",user.signout,name="signout"),

    re_path("newpost/?",post.newpost,name="newpost"),
    re_path("getpostlist/(?P<name>.+)/?",post.getpostlist,name="getpostlist"),
    re_path("getpost/(?P<id>.+)/?",post.getpost,name="getpost"),
    re_path("uploadfile/?",post.postuploadfile,name="postuploadfile"),

    re_path("newproduct/?",product.newproduct,name="newproduct"),
    re_path("getproductlist/(?P<sorttype>.+)/?",product.getproductlist,name="getproductlist"),
    re_path("getproduct/(?P<id>.+)/?",product.getproduct,name="getproduct"),
    re_path("editproduct/(?P<id>.+)/?",product.editproduct,name="editproduct"),

    re_path("taglist/?",post.gettaglist,name="gettaglist"),
    re_path("addtag/?",post.addtag,name="addtag"),

    re_path("newconnect/?",connect.newconnect,name="newconnect"),
]