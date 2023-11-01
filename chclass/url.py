from django.contrib import admin
from django.urls import path,include

from . import view

urlpatterns=[
    path("log/",view.getlog,name="log"), # log
]