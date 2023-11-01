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

# main START
db="chrisjudge"

@api_view(["POST"])
def login(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
        if row:
            if checkpassword(password,row[0][2]):
                row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][0],"使用者登入",time()])
                return Response({
                    "success": True,
                    "data": {
                        "token": token,
                        "permission": row[0][4]
                    }
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "密碼錯誤"
                },status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                "success": False,
                "data": "帳號錯誤"
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def thirdpartylogin(request,type):
    try:
        if type=="google":
            data=json.loads(request.body)
            print(data)
            row=query("thirdpartylogin","SELECT*FROM `google` WHERE `email`=%s",[data["email"]])
            if not row:
                query("thirdpartylogin","INSERT INTO `google`(`iss`,`azp`,`aud`,`sub`,`email`,`emailverified`,`nbf`,`name`,`picture`,`givenname`,`familyname`,`locale`,`iat`,`exp`,`jti`,`createtime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[data["iss"],data["azp"],data["aud"],data["sub"],data["email"],data["email_verified"],data["nbf"],data["name"],data["picture"],data["given_name"],data["family_name"],data["locale"],data["iat"],data["exp"],data["jti"],time()])
            row=query("chrisjudge","SELECT*FROM `user` WHERE `email`=%s",[data["email"]])
            if not row:
                query("chrisjudge","INSERT INTO `user`(`username`,`password`,`nickname`,`permission`,`email`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s)",["","","","1",data["email"],time(),time()])
            row=query(db,"SELECT*FROM `user` WHERE `email`=%s",[data["email"]])
            token=str(hash(data["email"],"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
            query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",["google_"+str(row[0][0]),token,time()])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][0],"使用者登入_google",time()])
            return Response({
                "success": True,
                "data": {
                    "token": token,
                    "permission": row[0][4]
                }
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "無此第三方登入資料"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
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
        nickname=data.get("nickname")
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
        if username:
            if len(password)>6:
                if nickname:
                    if not row:
                        query(db,"INSERT INTO `user`(`username`,`password`,`nickname`,`permission`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s)",[username,hashpassword(password),nickname,"1",time(),time()])
                        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                        token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                        query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][0],"使用者註冊",time()])

                        print("username: "+str(username))
                        print("logintoken: "+str(token))
                        return Response({
                            "success": True,
                            "data": {
                                "token": token
                            }
                        },status.HTTP_200_OK)
                    else:
                        return Response({
                            "success": False,
                            "data": "使用者以存在"
                        },status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "success": False,
                        "data": "請輸入暱稱"
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "data": "密碼長度不得小於大於6"
                },status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "success": False,
                "data": "請輸入帳號"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def logout(request,token):
    try:
        row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if row:
            query(db,"DELETE FROM `token` WHERE `token`=%s",[token])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][1],"使用者登出",time()])
            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "token不存在"
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)