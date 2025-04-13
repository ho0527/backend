from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import event
from . import user

urlpatterns=[
    re_path("^api/v1/event$",event.geteventlist,name="geteventlist"),
    re_path("^api/v1/organizers/(?P<organizer-slug>.+)/event/(?P<event-slug>.+)$",event.getevent,name="getevent"),
    re_path("^api/v1/organizers/(?P<organizer-slug>.+)/event/(?P<event-slug>.+)/registration$",event.newevent,name="newevent"),
    re_path("^api/v1/organizers/registration$",event.getuserevent,name="getuserevent"),

    re_path("^api/v1/login$",user.login,name="login"),
    re_path("^api/v1/logout$",user.logout,name="logout"),

    re_path(".+",index.error404,name="404"),
]