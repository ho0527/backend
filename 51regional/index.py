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
db="51regional"

@api_view(["POST"])
def signin(request):
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

@api_view(["POST"])
def signup(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        name=data.get("name")
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
        if username:
            if not row:
                if permission:
                    permission="管理者"
                else:
                    permission="一般使用者"
                query(db,"INSERT INTO `user`(`username`,`password`,`name`,`permission`)VALUES(%s,%s,%s,%s)",[username,password,name,permission])
                row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])[0]
                number=str(row[0]-1).zfill(5)
                query(db,"UPDATE `user` SET `number`=%s WHERE `id`=%s",[number,row[0]])
                return Response({
                    "success": True,
                    "data": "新增成功"
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "使用者以存在"
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "data": "請輸入帳號"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","DELETE"])
def editdeluser(request,id):
    try:
        if request.method=="PUT":
            if id!="1":
                data=json.loads(request.body)
                password=data.get("password")
                name=data.get("name")
                permission=data.get("permission")
                if permission:
                    permission="管理者"
                else:
                    permission="一般使用者"
                query(db,"UPDATE `user` SET `password`=%s,`name`=%s,`permission`=%s WHERE `id`=%s",[password,name,permission,id])
                return Response({
                    "success": True,
                    "data": "修改成功"
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "禁止修改管理者帳號!"
                },status.HTTP_400_BAD_REQUEST)
        else:
            if id!="1":
                query(db,"DELETE FROM `user` WHERE `id`=%s",[id])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "禁止刪除管理者帳號!"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def signout(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
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