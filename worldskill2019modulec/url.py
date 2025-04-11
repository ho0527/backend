from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import event
from . import user

urlpatterns=[
    re_path("^api/v1/event$",event.geteventlist,name="geteventlist"),
    re_path("^api/v1/organizers/(?P<organizer-slug>.+)/event/(?P<event-slug>.+)$",event.getevent,name="getevent"),

    re_path("^api/v1/login$",user.login,name="login"),
    re_path("^api/v1/logout$",user.logout,name="logout"),
    re_path("^editcompany/(?P<id>.+)$",company.editcompany,name="editcompany"),
    re_path("^deactivatecompany/(?P<id>.+)$",company.deactivatecompany,name="deactivatecompany"),

    re_path("^getcompanyproductlist/(?P<companyid>.+)$",product.getcompanyproductlist,name="getcompanyproductlist"),
    re_path("^getdeactivateproductlist/(?P<companyid>.+)$",product.getdeactivateproductlist,name="getdeactivateproductlist"),
    re_path("^getproduct/(?P<gtin>.+)$",product.getproduct,name="getproduct"),
    re_path("^newproduct/(?P<companyid>.+)$",product.newproduct,name="newproduct"),
    re_path("^editproduct/(?P<id>.+)$",product.editproduct,name="editproduct"),
    re_path("^deactivateproduct/(?P<id>.+)$",product.deactivateproduct,name="deactivateproduct"),
    re_path("^deleteproduct/(?P<id>.+)$",product.deleteproduct,name="deleteproduct"),

    re_path("^gtintest$",gtin.gtintest,name="gtintest"),

    re_path(".+",index.error404,name="404"),
]