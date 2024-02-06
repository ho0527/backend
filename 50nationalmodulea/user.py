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
from function.thing import printcolor,printcolorhaveline,time,switch_key,hashpassword,checkpassword,hash
from .function import signincheck
from .initialize import *

# main START
db=SETTING["dbname"]

@api_view(["GET"])
def getuser(request,userid):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[userid])
        check=signincheck(request)
        if check["success"]:
            if row:
                row=row[0]
                if check["data"]==row[0][1] or int(check["permission"])>=4:
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"查詢使用者 id="+str(userid),time()])
                    return Response({
                        "success": True,
                        "data": {
                            "userid": row[0][0],
                            "username": row[0][1],
                            "userpermission": row[0][3],
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "[WARNING]no permission"
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]user not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getuserlist(request):
    try:
        check=signincheck(request)
        if check["success"]:
            if int(check["permission"])>=4:
                row=query(db,"SELECT*FROM `user`")
                data=[]
                for i in range(len(row)):
                    data.push({
                        "userid": row[i][0],
                        "username": row[i][1],
                        "userpermission": row[i][3],
                    })
                query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"查詢使用者列表",time()])
                return Response({
                    "success": True,
                    "data": data
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]no permission"
                },status.HTTP_403_FORBIDDEN)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def edituser(request,userid):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")

        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[userid])
            if row:
                usernameckeck=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                if not usernameckeck or row[0][1]==usernameckeck[0][1]:
                    if check["data"]==userid and 4<=int(check["permission"]):
                        query(db,"UPDATE `user` SET `username`=%s,`password`=%s WHERE `id`=%s",[username,password,userid])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"更新使用者 id="+str(userid),time()])
                        return Response({
                            "success": True,
                            "data": ""
                        },status.HTTP_200_OK)
                    else:
                        return Response({
                            "success": False,
                            "data": "[WARNING]no permission"
                        },status.HTTP_403_FORBIDDEN)
                else:
                    return Response({
                        "success": False,
                        "data": "[WARNING]username already exist"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]user not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def edituserpermission(request,userid):
    try:
        data=json.loads(request.body)
        permission=data.get("permission")

        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[userid])
            if row:
                if 1<=int(permission) and int(permission)<=5:
                    if 4<=int(check["permission"]):
                        query(db,"UPDATE `user` SET `permission`=%s WHERE `id`=%s",[permission,userid])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"更新使用者權限 id="+str(userid),time()])
                        return Response({
                            "success": True,
                            "data": ""
                        },status.HTTP_200_OK)
                    else:
                        return Response({
                            "success": False,
                            "data": "[WARNING]no permission"
                        },status.HTTP_403_FORBIDDEN)
                else:
                    return Response({
                        "success": False,
                        "data": "[WARNING]permission value error"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]user not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deleteuser(request,userid):
    try:
        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[userid])
            if row:
                if check["data"]==userid or int(check["permission"])>=4:
                    query(db,"DELETE FROM `user` WHERE `id`=%s",[userid])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"刪除使用者 id="+str(userid),time()])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "[WARNING]no permission"
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]user not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)