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
from .function import *
from .initialize import *

# main START
db=SETTING["dbname"]

@api_view(["POST"])
def signin(request):
    try:
        data=json.loads(request.body)
        email=data.get("email")
        password=data.get("password")

        row=query(db,"SELECT*FROM `users` WHERE `email`=%s",[email])

        if email and password:
            if type(email)==str and type(password)==str:
                if row and checkpassword(password,row[0][2]):
                    token=str(hash(email,"sha256"))
                    query(db,"UPDATE `users` SET `token`=%s WHERE `id`=%s",[token,row[0][0]])
                    return Response({
                        "success": True,
                        "data": {
                            "id": row[0][0],
                            "email": row[0][1],
                            "nickname": row[0][3],
                            "role": row[0][4],
                            "token": token
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_INVALID_LOGIN",
                        "data": ""
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_DATATYPE_ERROR",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "message": "MSG_MISSING_FIELD",
                "data": ""
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signout(request):
    try:
        check=signincheck(request)

        if check["success"]:
            query(db,"UPDATE `users` SET `token`='' WHERE `id`=%s",[check["userid"]])
            return Response({
                "success": True,
                "message": "",
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signup(request):
    try:
        data=json.loads(request.body)
        email=data.get("email")
        password=data.get("password")
        nickname=data.get("nickname")

        row=query(db,"SELECT*FROM `users` WHERE `email`=%s",[email])
        if email and password and nickname:
            if type(email)==str and type(password)==str and type(nickname)==str:
                if not row:
                    query(db,"INSERT INTO `users`(`email`,`password`,`nickname`,`role`)VALUES(%s,%s,%s,%s)",[email,hashpassword(password),nickname,"USER"])
                    return Response({
                        "success": True,
                        "message": "",
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_USER_EXISTS",
                        "data": ""
                    },status.HTTP_409_CONFLICT)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_DATATYPE_ERROR",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "message": "MSG_MISSING_FIELD",
                "data": ""
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)
