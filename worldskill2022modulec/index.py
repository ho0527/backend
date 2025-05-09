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
from function.sql import *
from function.thing import *
from .function import signincheck

# main START
db="worldskill2022modulec"

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
            invaliddata["username"]={
                "message": "required"
            }
            check=False
        else:
            if len(username)<4:
                invaliddata["username"]={
                    "message": "must be at least 4 characters long"
                }
                check=False
            elif len(username)>60:
                invaliddata["username"]={
                    "message": "must be at most 60 characters long"
                }
                check=False

        if not password:
            invaliddata["password"]={
                "message": "required"
            }
            check=False
        else:
            if len(password)<4:
                invaliddata["password"]={
                    "message": "must be at least 4 characters long"
                }
                check=False
            elif len(password)>(2**16):
                invaliddata["password"]={
                    "message": "must be at most 2^16 characters long"
                }
                check=False

        if not row:
            if check:
                query(db,"INSERT INTO `user`(`username`,`password`,`createtime`,`updatetime`,`lastlogintime`,`blocktime`,`blockreason`)VALUES(%s,%s,%s,%s,%s,%s,%s)",[username,password,time(),time(),time(),"",""])
                row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0]["id"],token,time()])

                return Response({
                    "status": "success",
                    "token": token
                },status.HTTP_200_OK)
            else:
                return Response({
                    "status": "invalid",
                    "message": "Request body is not valid",
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
            invaliddata["username"]={
                "message": "required"
            }
            check=False
        else:
            if len(username)<4:
                invaliddata["username"]={
                    "message": "must be at least 4 characters long"
                }
                check=False
            elif len(username)>60:
                invaliddata["username"]={
                    "message": "must be at most 60 characters long"
                }
                check=False

        if not password:
            invaliddata["password"]={
                "message": "required"
            }
            check=False
        else:
            if len(password)<4:
                invaliddata["password"]={
                    "message": "must be at least 4 characters long"
                }
                check=False
            elif len(password)>(2**16):
                invaliddata["password"]={
                    "message": "must be at most 2^16 characters long"
                }
                check=False

        if check:
            if row:
                if password==row[0]["password"]:
                    if row[0]["blocktime"]==None:
                        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
                        token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
                        query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0]["id"],token,time()])

                        return Response({
                            "status": "success",
                            "token": token
                        },status.HTTP_200_OK)
                    else:
                        return Response({
                            "status": "blocked",
                            "message": "User blocked",
                            "reason": row[0]["blockreason"]
                        },status.HTTP_403_FORBIDDEN)
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
        else:
            return Response({
                "status": "invalid",
                "message": "Request body is not valid",
                "violations": invaliddata
            },status.HTTP_400_BAD_REQUEST)
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
                "status": "success",
            },status.HTTP_200_OK)
        else:
            return Response(check["data"],status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getuser(request,username):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
        if row:
            row=row[0]
            authorgamelist=[]
            scorelist=[]

            gamerow=query(db,"SELECT*FROM `game` WHERE `userid`=%s",[row["id"]])
            scorerow=query(db,"""
                SELECT *
                FROM score
                WHERE (userid, gameid, score) IN (
                    SELECT userid, gameid, MAX(score)
                    FROM score
                    WHERE userid=%s
                    GROUP BY userid, gameid
                )
            """,[row["id"]])
            print(scorerow)

            for i in range(len(gamerow)):
                authorgamelist.append({
                    "slug": gamerow[i]["slug"],
                    "title": gamerow[i]["title"],
                    "description": gamerow[i]["description"]
                })

            for i in range(len(scorerow)):
                gamerow=query(db,"SELECT*FROM `game` WHERE `id`=%s",[scorerow[i]["gameid"]])[0]
                scorelist.append({
                    "game":{
                        "slug": gamerow["slug"],
                        "title": gamerow["title"],
                        "description": gamerow["description"]
                    },
                    "score": scorerow[i]["score"],
                    "timestamp": scorerow[i]["createtime"]
                })

            return Response({
                "username": row["username"],
                "registerTimestamp": row["createtime"],
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
            "status": "not found",
            "message": "Not found"
        },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)