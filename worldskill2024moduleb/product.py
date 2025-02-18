# import
import bcrypt
import hashlib
import json
import random
import re
import google.oauth2.id_token
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from pathlib import Path
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from .utils import exception_handler

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
@api_view(["GET"])
@exception_handler
def getcompanyproductlist(request,companyid):
    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `companyid`=%s AND `deactivatetime` IS NOT  NULL",[companyid],SETTING["dbsetting"])

    return Response({
        "success": True,
        "data": row
    },status.HTTP_200_OK)

@api_view(["GET"])
@exception_handler
def getdeactivateproductlist(request,companyid):
    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `companyid`=%s AND `deactivatetime` IS NOT  NULL",[companyid],SETTING["dbsetting"])

    return Response({
        "success": True,
        "data": row
    },status.HTTP_200_OK)

@api_view(["GET"])
@exception_handler
def getproduct(request,gtin):
    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `gtin`=%s AND `deactivatetime` IS NULL",[gtin],SETTING["dbsetting"])

    if row:
        return Response({
            "success": True,
            "data": row[0]
        },status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "data": "company not found"
        },status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@exception_handler
def newproduct(request,companyid):
    file=request.FILES.get("file")
    gtin=request.POST.get("gtin")
    name=request.POST.get("name")
    engname=request.POST.get("engname")
    gtin=request.POST.get("gtin")
    description=request.POST.get("description")
    engdescription=request.POST.get("engdescription")
    brandname=request.POST.get("brandname")
    country=request.POST.get("country")
    grossweight=request.POST.get("grossweight")
    contentweight=request.POST.get("contentweight")

    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `gtin`=%s AND `deactivatetime` IS NULL",[gtin],SETTING["dbsetting"])

    if pregmatch(gtin,"[0-9]{13,14}") and row:
        filename="/upload/default.png"

        if file:
            filename=randomtext()+Path(file.name).suffix

            uploadfile("/upload/",file[0],filename)

        query(
            SETTING["dbname"],
            "INSERT INTO `product`(`id`,`compantid`,`imagelink`,`gtin`,`name`,`enname`,`description`,`endescription`,`brandname`,`country`,`grossweight`,`contentweight`,`unit`,`createtime`,`updatetime`,`deactivatetime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [None,companyid,"/upload/"+filename,gtin,name,engname,gtin,description,engdescription,brandname,country,grossweight,contentweight,nowtime(),None,None],
            SETTING["dbsetting"]
        )

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    else:
        return Response({
            "success": True,
            "data": "gtin error"
        },status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@exception_handler
def editproduct(request,id):
    file=request.FILES.get("file")
    gtin=request.POST.get("gtin")
    name=request.POST.get("name")
    engname=request.POST.get("engname")
    gtin=request.POST.get("gtin")
    description=request.POST.get("description")
    engdescription=request.POST.get("engdescription")
    brandname=request.POST.get("brandname")
    country=request.POST.get("country")
    grossweight=request.POST.get("grossweight")
    contentweight=request.POST.get("contentweight")

    filename="/upload/default.png"

    if file:
        filename=randomtext()+Path(file.name).suffix

        uploadfile("/upload/",file[0],filename)

    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `id`=%s AND `deactivatetime` IS NULL",[id],SETTING["dbsetting"])

    if row:
        query(
            SETTING["dbname"],
            "UPDATE `product` SET `imagelink`=%s,`gtin`=%s,`name`=%s,`enname`=%s,`description`=%s,`endescription`=%s,`brandname`=%s,`country`=%s,`grossweight`=%s,`contentweight`=%s,`unit`=%s,`updatetime`=%s WHERE `id`=%s",
            ["/upload/"+filename,gtin,name,engname,gtin,description,engdescription,brandname,country,grossweight,contentweight,nowtime(),id],
            SETTING["dbsetting"]
        )

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "data": "company not found"
        },status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@exception_handler
def deactivateproduct(request,id):
    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `id`=%s AND `deactivatetime` IS NULL",[id],SETTING["dbsetting"])

    if row:
        query(SETTING["dbname"],"UPDATE `product` SET `deactivatetime`=%s WHERE `id`=%s",[nowtime(),id],SETTING["dbsetting"])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "data": "company not found"
        },status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@exception_handler
def deleteproduct(request,id):
    row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `id`=%s AND `deactivatetime` IS NOT NULL",[id],SETTING["dbsetting"])

    if row:
        query(SETTING["dbname"],"DELETE FROM `product` WHERE `compantid`=%s",[id],SETTING["dbsetting"])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "data": "company not found"
        },status.HTTP_404_NOT_FOUND)