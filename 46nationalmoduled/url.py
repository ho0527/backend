from django.contrib import admin
from django.urls import path,include

from . import index
from . import manger

urlpatterns=[
    # question/
    path("searchtrain/<str:startstaion>/<str:endstaion>/<str:traintype>/<str:getgodate>",index.searchtrain,name="searchtrain"),
    path("searchtrain/<str:traincode>",index.searchtraincode,name="searchtraincode"),
    path("newticket/",index.newticket,name="newticket"),
    path("searchticket",index.searchticket,name="searchticket"),
    path("login",index.login,name="login"),

    path("mangertraintype/",manger.getposttraintype,name="getposttraintype"),
    path("mangertraintype/<str:id>",manger.putdeletetraintype,name="putdeletetraintype"),

    path("mangertrain/",manger.getposttrain,name="getposttrain"),
    path("mangertrain/<str:id>",manger.putdeletetrain,name="putdeletetrain"),
    path("adminsearchticket",manger.adminsearchticket,name="adminsearchticket"),

    # self/
    path("mangerstation/",manger.getpoststation,name="getpoststation"),
    path("mangerstation/<str:id>",manger.putdeletestation,name="putdeletestation"),
]