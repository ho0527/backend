# import
import bcrypt
import hashlib
import json
import random
import re
import google.oauth2.id_token
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
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
def getproduct(request,id):
    row=query(SETTING["dbname"],"SELECT*FROM `company` WHERE `id`=%s AND `deactivatetime` IS NULL",[id],SETTING["dbsetting"])

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
    data=json.loads(request.body)
    name=data.get("name")
    address=data.get("address")
    phone=data.get("phone")
    email=data.get("email")
    ownername=data.get("ownername")
    ownerphone=data.get("ownerphone")
    owneraddress=data.get("owneraddress")
    contactname=data.get("contactname")
    contactphone=data.get("contactphone")
    contactaddress=data.get("contactaddress")

    query(
        SETTING["dbname"],
        "INSERT INTO `company`(`id`,`name`,`address`,`phone`,`email`,`ownername`,`ownerphone`,`owneraddress`,`contactname`,`contactphone`,`contactaddress`,`createtime`,`updatetime`,`deactivatetime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [None,name,address,phone,email,ownername,ownerphone,owneraddress,contactname,contactphone,contactaddress,nowtime(),None,None],
        SETTING["dbsetting"]
    )

    return Response({
        "success": True,
        "data": ""
    },status.HTTP_200_OK)

@api_view(["PUT"])
@exception_handler
def editproduct(request,id):
    data=json.loads(request.body)
    name=data.get("name")
    address=data.get("address")
    phone=data.get("phone")
    email=data.get("email")
    ownername=data.get("ownername")
    ownerphone=data.get("ownerphone")
    owneraddress=data.get("owneraddress")
    contactname=data.get("contactname")
    contactphone=data.get("contactphone")
    contactaddress=data.get("contactaddress")

    row=query(SETTING["dbname"],"SELECT*FROM `company` WHERE `id`=%s AND `deactivatetime` IS NULL",[id],SETTING["dbsetting"])

    if row:
        query(
            SETTING["dbname"],
            "UPDATE `company` SET `name`=%s,`address`=%s,`phone`=%s,`email`=%s,`ownername`=%s,`ownerphone`=%s,`owneraddress`=%s,`contactname`=%s,`contactphone`=%s,`contactaddress`=%s,`updatetime`=%s WHERE `id`=%s",
            [name,address,phone,email,ownername,ownerphone,owneraddress,contactname,contactphone,contactaddress,nowtime(),id],
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
    row=query(SETTING["dbname"],"SELECT*FROM `company` WHERE `id`=%s AND `deactivatetime` IS NULL",[id],SETTING["dbsetting"])

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