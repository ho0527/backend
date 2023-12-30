from django.contrib import admin
from django.urls import path,include,re_path
from graphene_django.views import GraphQLView

from . import api

urlpatterns=[
    re_path("response/?",api.response,name="response"),
]