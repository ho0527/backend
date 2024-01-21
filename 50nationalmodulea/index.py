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

@api_view(["POST"])
def signin(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")

        row=query(db,"SELECT*FROM `user` WHERE `username`=%sAND`password`=%s",[username,password])

        if row:
            token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
            query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
            query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],"登入系統",time()])

            return Response({
                "success": True,
                "data": {
                    0: row[0][0],
                    1: row[0][1],
                    2: row[0][3],
                    "token": token,
                }
            },status.HTTP_200_OK)
        else:
            return Response({
                "status": "invalid",
                "message": "[WARNING]username or password error"
            },status.HTTP_401_UNAUTHORIZED)
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

        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])

        if not row:
            query(db,"INSERT INTO `user`(`username`,`password`,`permission`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s)",[username,password,"1",time(),time()])
            row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
            token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
            query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
            query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],"註冊系統",time()])

            return Response({
                "status": "success",
                "token": token
            },status.HTTP_200_OK)
        else:
            return Response({
                "status": "invalid",
                "message": "[WARNING]user already exist"
            },status.HTTP_409_CONFLICT)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signout(request):
    try:
        check=signincheck(request)
        if check["success"]:
            query(db,"DELETE FROM `token` WHERE `id`=%s",[check["tokenid"]])
            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getuser(request,username):
    try:
        check=signincheck(request)
        if check["success"]:
            self=True
        else:
            self=False

        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
        if row:
            row=row[0]
            authorgamelist=[]
            scorelist=[]
            if self:
                gamerow=query(db,"SELECT*FROM `game` WHERE `userid`=%s",[row[0]])
                scorerow=query(db,"SELECT*FROM `score` WHERE (`gameid`,`score`)IN(SELECT `gameid`,MAX(`score`)FROM`score`GROUP BY`gameid`) AND `userid`=%s",[row[0]])
            else:
                gamerow=query(db,"SELECT*FROM `game` WHERE `userid`=%s AND `version`!='0'",[row[0]])
                scorerow=query(db,"SELECT*FROM `score` WHERE (`gameid`,`score`)IN(SELECT`gameid`,MAX(`score`)FROM`score`GROUP BY`gameid`) AND `userid`=%s",[row[0]])

            for i in range(len(gamerow)):
                authorgamelist.append({
                    "slug": gamerow[i][5],
                    "title": gamerow[i][4],
                    "description": gamerow[i][6]
                })

            for i in range(len(scorerow)):
                gamerow=query(db,"SELECT*FROM `game` WHERE `id`=%s",[scorerow[i][2]])
                scorelist.append({
                    "game":{
                        "slug": gamerow[0][5],
                        "title": gamerow[0][4],
                        "description": gamerow[0][6]
                    },
                    "score": scorerow[i][3],
                    "timestamp": scorerow[i][4]
                })

            return Response({
                "username": row[1],
                "registerTimestamp": row[3],
                "authoredGames": authorgamelist,
                "highscores": scorelist
            },status.HTTP_200_OK)
        else:
            return Response({
                "status": "invalid",
                "message": "user not found"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET","POST","PUT","DELETE"])
def error404(request):
    try:
        return Response({
            "success": False,
            "data": "page not found"
        },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)