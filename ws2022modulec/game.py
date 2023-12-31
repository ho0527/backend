# import
import bcrypt
import hashlib
import json
import os
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils.text import get_valid_filename
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from zipfile import *

# 自創
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key,hashpassword,checkpassword,hash,uploadfile
from ws2022modulec.function import signincheck

# main START
db="ws2022modulec"

@api_view(["GET","POST","PUT","DELETE"])
def game(request):
    try:
        if request.method=="GET":
            page=request.GET.get("page")
            size=request.GET.get("size")
            sortby=request.GET.get("sortBy")
            sorttype=request.GET.get("sortDir")
            check=True

            # 初始化 START
            if not page:
                page=0

            if not size:
                size=10

            if not sortby:
                sortby="title"

            if not sorttype:
                sorttype="asc"

            page=int(page)
            size=int(size)
            # 初始化 END

            # 驗證 START
            if page<0:
                check=False

            if size<1:
                check=False

            if sortby!="title" or sortby!="popular" or sortby!="uploaddate":
                check=False

            if sorttype!="asc" or sorttype!="desc":
                check=False
            # 驗證 END

            if check:
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
        elif request.method=="POST":
            data=json.loads(request.body)
            title=data.get("title")
            description=data.get("description")

            slug=""
            invaliddata={}

            check=True

            if title==None:
                invaliddata["title"]="required"
                check=False
                print("in")
            else:
                slug=title.lower().replace(" ","-")
                if len(title)<3:
                    invaliddata["title"]="must be at least 3 characters long"
                    check=False
                elif len(title)>60:
                    invaliddata["title"]="must be at most 60 characters long"
                    check=False

            if description==None:
                invaliddata["description"]="required"
                check=False
            else:
                if len(description)>200:
                    invaliddata["description"]="must be at most 200 characters long"
                    check=False

            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            usercheck=signincheck(request)
            if usercheck["success"]:
                if not row:
                    if check:
                        query(db,
                            "INSERT INTO `game`(`userid`,`thumbnailpath`,`gamepath`,`title`,`slug`,`description`,`version`,`createtime`,`updatetime`,`deletetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [usercheck["data"],None,"",title,slug,description,"",time(),time(),None]
                        )

                        return Response({
                            "status": "success",
                            "slug": slug
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
                        "slug": "Game title already exists."
                    },status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(usercheck["data"],status.HTTP_401_UNAUTHORIZED)
        elif request.method=="PUT":
            pass
        else:
            pass
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def uploadgame(request,slug):
    try:
        file=request.FILES["zipfile"]
        token=request.FILES["token"]

        if token:
            userrow=query("ws2022modulec","SELECT*FROM `token` WHERE `token`=%s",[token])
            if userrow:
                userid=userrow[0][0]
                if not file:
                    row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
                    if row:
                        if userid!=row[0][1]:
                            query(db,
                                "INSERT INTO `game`(`userid`,`thumbnailpath`,`gamepath`,`title`,`slug`,`description`,`version`,`createtime`,`updatetime`,`deletetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ["",None,"",title,slug,description,"",time(),time(),None]
                            )

                            return Response({
                                "status": "success",
                                "slug": slug
                            },status.HTTP_200_OK)
                        else:
                            return "User is not the author of the game."
                    else:
                        return Response({
                            "status": "invalid",
                            "slug": "Game not exists."
                        },status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "status": "invalid",
                        "message": "request body is not valid",
                        "violations": {
                            "zipfile": "required"
                        }
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return {
                    "success": False,
                    "data": {
                        "status": "unauthenticated",
                        "message": "invalid token"
                    }
                }
        else:
            return {
                "success": False,
                "data":{
                    "status": "unauthenticated",
                    "message": "missing token"
                }
            }
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def getgame(request):
    pass