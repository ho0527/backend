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

@api_view(["PUT"])
def edituser(request,id):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        password=data.get("password")

        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
            if row:
                usernameckeck=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                if not usernameckeck or row[0][1]==usernameckeck[0][1]:
                    if check["data"]==id:
                        query(db,"UPDATE `user` SET `username`=%s,`password`=%s WHERE `id`=%s",[username,password,id])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"更新使用者",time()])
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
                return Response({
                    "success": False,
                    "data": "[WARNING]user not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deleteuser(request,id):
    try:
        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
            if row:
                if check["data"]==id or int(check["permission"])>=4:
                    query(db,"DELETE FROM `user` WHERE `id`=%s",[id])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["data"],"刪除使用者",time()])
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
            return Response(check,status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)