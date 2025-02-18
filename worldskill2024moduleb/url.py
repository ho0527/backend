from django.contrib import admin
from django.urls import path,include,re_path

from . import index
from . import company
from . import product
from . import gtin

urlpatterns=[
    re_path("^getdeactivatecompanylist$",company.getdeactivatecompanylist,name="getdeactivatecompanylist"),
    re_path("^getcompanylist$",company.getcompanylist,name="getcompanylist"),
    re_path("^getcompany/(?P<id>.+)$",company.getcompany,name="getcompany"),
    re_path("^newcompany$",company.newcompany,name="newcompany"),
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