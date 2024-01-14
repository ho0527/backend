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

@api_view(["GET"])
def getfood(request,id):
    try:
        row=query(db,"SELECT*FROM `food` WHERE `id`=%s",[id])

        if row:
            row=row[0]
            return Response({
                "success": True,
                "data": {
                    "id": row[0],
                    "name": row[1],
                    "price": row[2],
                    "createtime": row[3],
                    "updatetime": row[4]
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
def getfoodlist(request):
    try:
        data=[]
        row=query(db,"SELECT*FROM `food`")

        for i in range(len(row)):
            data.append({
                "id": row[i][0],
                "name": row[i][1],
                "price": row[i][2],
                "createtime": row[i][3],
                "updatetime": row[i][4]
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
def newfood(request):
    try:
        data=json.loads(request.body)
        name=data.get("name")
        price=data.get("price")

        row=query(db,"SELECT*FROM `food` WHERE `name`=%s",[name])

        if not row:
            query(
                db,
                "INSERT INTO `food`(`name`,`price`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s)",
                [name,price,time(),""]
            )

            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "errorkey": "name",
                "data": "名稱已存在"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def editfood(request,id):
    try:
        data=json.loads(request.body)
        name=data.get("name")
        price=data.get("price")

        row=query(db,"SELECT*FROM `food` WHERE `id`=%s",[id])

        if row:
            namcheckrow=query(db,"SELECT*FROM `food` WHERE `name`=%s",[name])
            if not namcheckrow or namcheckrow[0][0]:
                query(db,"UPDATE `food` SET `name`=%s,`price`=%s,`updatetime`=%s WHERE `id`=%s",[name,price,time(),id])

                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "errorkey": "name",
                    "data": "名稱已存在"
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "errorkey": "all",
                "data": "查無此食物"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deletefood(request,id):
    try:
        row=query(db,"SELECT*FROM `food` WHERE `id`=%s",[id])

        if row:
            query(db,"DELETE FROM `food` WHERE `id`=%s",[id])
            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此留言"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)