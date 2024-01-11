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
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START
db="53regional"

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
            if row[0][2]==password:
                if verifycodeans==verifycodeuserans:
                    return Response({
                        "success": True,
                        "data": {
                            "id": row[0][0],
                            "permission": row[0][5]
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": {
                            "message": "驗證碼有誤",
                            "id": row[0][0]
                        }
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "data": {
                        "message": "密碼有誤",
                        "id": row[0][0]
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

@api_view(["GET"])
def logindatatodb(request):
    try:
        key=request.GET.get("key")
        id=request.GET.get("id")
        if key=="success":
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])[0]
            query(db,"INSERT INTO `data`(`number`,`username`,`password`,`name`,`permission`,`move1`,`move2`,`movetime`)VALUES(%s,%s,%s,%s,%s,'登入','成功',%s)",[row[4],row[1],row[2],row[3],row[5],time()])
        else:
            if id=="未知":
                query(db,"INSERT INTO `data`(`number`,`username`,`password`,`name`,`permission`,`move1`,`move2`,`movetime`)VALUES('N/A','','','','','登入','失敗',%s)",[time()])
            else:
                row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])[0]
                query(db,"INSERT INTO `data`(`number`,`username`,`password`,`name`,`permission`,`move1`,`move2`,`movetime`)VALUES(%s,%s,%s,%s,%s,'登入','成功',%s)",[row[4],row[1],row[2],row[3],row[5],time()])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def logout(request,id):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
        if len(row)>0:
            row=row[0]
            query(db,"INSERT INTO `data`(`number`,`username`,`password`,`name`,`permission`,`move1`,`move2`,`movetime`)VALUES(%s,%s,%s,%s,%s,'登出','成功',%s)",[row[4],row[1],row[2],row[3],row[5],time()])
        else:
            query(db,"INSERT INTO `data`(`number`,`username`,`password`,`name`,`permission`,`move1`,`move2`,`movetime`)VALUES('N/A','','','','','登入','失敗',%s)",[time()])
        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)