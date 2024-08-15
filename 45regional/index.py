# import
import json
import math
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import *
from function.thing import *

# main START
db="45regional"

@api_view(["POST"])
def login(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        verifycodeans=data.get("verifycodeans")
        verifycodeuserans=data.get("verifycodeuserans")

        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])

        if row:
            row=row[0]
            if row[2]==password:
                if verifycodeans==verifycodeuserans:
                    query(db,"INSERT INTO `data`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0],"登入",time()])
                    return Response({
                        "success": True,
                        "data": {
                            "id": row[0],
                            "permission": row[5]
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": {
                            "message": "驗證碼有誤",
                            "id": row[0]
                        }
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "data": {
                        "message": "密碼有誤",
                        "id": row[0]
                    }
                },status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                "success": False,
                "data": {
                    "message": "帳號有誤",
                    "id": "未知"
                }
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def logout(request,id):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
        if len(row)>0:
            query(db,"INSERT INTO `data`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0],"登出",time()])
        else:
            query(db,"INSERT INTO `data`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",["N/A","登出",time()])
        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)