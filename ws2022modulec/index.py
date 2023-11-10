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
from ws2022modulec.function import usercheck

# main START
db="ws2022modulec"

@api_view(["POST"])
def signup(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        invaliddata={}

        check=True
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])

        if not username:
            invaliddata["username"]="required"
            check=False
        else:
            if len(username)<4:
                invaliddata["username"]="must be at least 4 characters long"
                check=False
            elif len(username)>60:
                invaliddata["username"]="must be at most 60 characters long"
                check=False

        if not password:
            invaliddata["password"]="required"
            check=False
        else:
            if len(password)<4:
                invaliddata["password"]="must be at least 4 characters long"
                check=False
            elif len(password)>(2**16):
                invaliddata["password"]="must be at most 2^16 characters long"
                check=False

        if not row:
            if check:
                query(db,"INSERT INTO `user`(`username`,`password`,`createtime`,`updatetime`,`lastlogintime`,`deltime`,`delreason`)VALUES(%s,%s,%s,%s,%s,%s,%s)",[username,hashpassword(password),time(),time(),time(),"",""])
                row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])

                return Response({
                    "status": "success",
                    "token": token
                },status.HTTP_200_OK)
            else:
                return Response({
                    "status": "invalid",
                    "message": "request body is not valid",
                    "violations": invaliddata
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "invalid",
                "message": "user exist"
            },status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signin(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        invaliddata={}

        check=True
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])

        if not username:
            invaliddata["username"]="required"
            check=False
        else:
            if len(username)<4:
                invaliddata["username"]="must be at least 4 characters long"
                check=False
            elif len(username)>60:
                invaliddata["username"]="must be at most 60 characters long"
                check=False

        if not password:
            invaliddata["password"]="required"
            check=False
        else:
            if len(password)<4:
                invaliddata["password"]="must be at least 4 characters long"
                check=False
            elif len(password)>(2**16):
                invaliddata["password"]="must be at most 2^16 characters long"
                check=False

        if row:
            if checkpassword(password,row[0][2]):
                if check:
                    row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                    token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                    query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])

                    return Response({
                        "status": "success",
                        "token": token
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "invalid",
                        "message": "request body is not valid",
                        "violations": invaliddata
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status": "invalid",
                    "message": "Wrong username or password"
                },status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "status": "invalid",
                "message": "Wrong username or password"
            },status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signout(request):
    try:
        check=usercheck(request)
        if check["status"]=="success":
            query(db,"DELETE FROM `token` WHERE `token`=%s",[request.headers.get("Authorization").split("Bearer ")[1]])
            return Response(check,status.HTTP_200_OK)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)