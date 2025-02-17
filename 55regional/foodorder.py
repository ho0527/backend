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

# 自創
from function.sql import query,createdb
from function.thing import *

# main START
db="54regional"

@api_view(["GET"])
def getfoodorder(request,id):
    try:
        row=query(db,"SELECT*FROM `foodorder` WHERE `id`=%s",[id])

        if row:
            row=row[0]
            return Response({
                "success": True,
                "data": {
                    "id": row[0],
                    "username": row[1],
                    "orderdata": row[2],
                    "totalprice": row[3],
                    "createtime": row[4],
                    "updatetime": row[5]
                }
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此食物"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getfoodorderlist(request):
    try:
        data=[]
        row=query(db,"SELECT*FROM `foodorder`")

        for i in range(len(row)):
            data.append({
                    "id": row[i][0],
                    "username": row[i][1],
                    "orderdata": row[i][2],
                    "totalprice": row[i][3],
                    "createtime": row[i][4],
                    "updatetime": row[i][5]
                })

        return Response({
            "success": True,
            "data": data
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newfoodorder(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        orderdata=data.get("orderdata")
        totalprice=data.get("totalprice")

        query(
            db,
            "INSERT INTO `foodorder`(`username`,`orderdata`,`totalprice`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s)",
            [username,orderdata,totalprice,time(),""]
        )

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def editfoodorder(request,id):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        orderdata=data.get("orderdata")
        totalprice=data.get("totalprice")

        query(db,"UPDATE `foodorder` SET `username`=%s,`orderdata`=%s,`totalprice`=%s,`updatetime`=%s WHERE `id`=%s",[username,orderdata,totalprice,time(),id])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deletefoodorder(request,id):
    try:
        row=query(db,"SELECT*FROM `foodorder` WHERE `id`=%s",[id])

        if row:
            query(db,"DELETE FROM `foodorder` WHERE `id`=%s",[id])
            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此訂餐"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)