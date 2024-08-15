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
db="53regional"

@api_view(["GET"])
def getuserlist(request):
    try:
        keyword=request.GET.get("keyword")
        orderby=request.GET.get("orderby")
        ordertype=request.GET.get("ordertype")
        if ordertype in ["ASC", "DESC"]:
            row=query(
                db,
                "SELECT*FROM `user` WHERE `username`LIKE%sOR`password`LIKE%sOR`name`LIKE%sOR`number`LIKE%sOR`permission`LIKE%s ORDER BY `"+orderby+"` "+ordertype,
                ["%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%"]
            )
            return Response({
                "success": True,
                "data": row
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "Invalid ordertype value. It should be either 'ASC' or 'DESC'."
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getuser(request,id):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
        if row:
            return Response({
                "success": True,
                "data": row[0]
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "使用者不存在"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newuser(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        name=data.get("name")
        permission=data.get("permission")
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
def log(request):
    try:
        row=query(db,"SELECT*FROM `data` ORDER BY `id` DESC")
        return Response({
            "success": True,
            "data": row
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)