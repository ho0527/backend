from django.contrib import admin
from django.urls import path,include,re_path
from graphene_django.views import GraphQLView

from .api import schema

urlpatterns=[
    re_path("api/?",GraphQLView.as_view(graphiql=True,schema=schema)),
]