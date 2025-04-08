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
from function.thing import *
from ws2022modulec.function import signincheck

# main START
db="ws2022modulec"

@api_view(["GET","POST"])
def game(request):
    try:
        if request.method=="GET":
            page=request.GET.get("page")
            size=request.GET.get("size")
            sortby=request.GET.get("sortBy")
            sorttype=request.GET.get("sortDir")

            check=True
            data=[]

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

            if sortby!="title" and sortby!="popular" and sortby!="uploaddate":
                check=False

            if sorttype!="asc" and sorttype!="desc":
                check=False
            # 驗證 END

            if check:
                row=query(db,"SELECT*FROM `gameversion` WHERE `deletetime` IS NULL ORDER BY `%s` %s LIMIT %s,%s",[sortby,sorttype,page*size,size])

                for i in range(len(row)):
                    gamerow=query(db,"SELECT*FROM `game` WHERE `id`=%s",[row[i]["gameid"]])[0]
                    userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[i][gamerow["userid"]]])[0]
                    scorerow=query(db,"SELECT*FROM `score` WHERE `gameid`=%s",[row[i]["gameid"]])
                    data.append({
                        "author": userrow["username"],
                        "slug": game[i]["slug"],
                        "title": game[i]["title"],
                        "description": game[i]["desciption"],
                        "thumbnail": row[i]["thumbnailpath"],
                        "scoreCount": len(scorerow),
                        "uploadTimestamp": row[i]["createtime"]
                    })

                return Response({
                    "page": page,
                    "size": len(data),
                    "totalElements": len(query(db,"SELECT*FROM `gameversion` WHERE `deletetime` IS NULL",[])),
                    "content": data
                },status.HTTP_200_OK)
            else:
                return Response({
                    "status": "invaled",
                    "message": "data error"
                },status.HTTP_400_BAD_REQUEST)
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
                            [usercheck["data"],None,"",title,slug,description,"0",time(),time(),None]
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
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def uploadgame(request,slug):
    try:
        try:
            file=request.FILES["zipfile"]
        except Exception as error:
            return Response({
                "status": "invalid",
                "message": "request body is not valid",
                "violations": {
                    "zipfile": "required"
                }
            },status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            token=request.POST["token"]
        except Exception as error:
            return Response({
                "status": "unauthenticated",
                "message": "missing token"
            },status.HTTP_500_INTERNAL_SERVER_ERROR)


        if token and token!="":
            tokenrow=query("ws2022modulec","SELECT*FROM `token` WHERE `token`=%s",[token])
            if tokenrow:
                if file:
                    row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
                    if row:
                        row=row[0]
                        if tokenrow[0][1]==row[1]:
                            try:
                                # 上傳zip到./temp資料夾
                                zipname=randomname()+os.path.splitext(file.name)[1]
                                uploadfile("./upload/ws2022modulec",file,zipname)
                                ziplink="./upload/ws2022modulec/"+zipname

                                # 解壓zip
                                version=str(int(row[7])+1)
                                with ZipFile(ziplink,"r") as zipfile:
                                    zipfile.extractall("./upload/ws2022modulec/"+(slug+"/"+version))
                                    filelist=zipfile.namelist()
                                if os.path.getsize(ziplink)<=1048576:
                                    os.remove(ziplink)
                                    if "index.html" in filelist:
                                        thumbnailpath=None
                                        if "thumbnail.png" in filelist:
                                            thumbnailpath="/backend/media/ws2022modulec/"+(slug+"/"+version)+"/thumbnail.png"

                                        query(db,"UPDATE `game` SET `thumbnailpath`=%s,`gamepath`=%s,`version`=%s,`updatetime`=%s WHERE `slug`=%s",[thumbnailpath,"/backend/media/ws2022modulec/"+(slug+"/"+version),version,time(),slug])

                                        return Response({
                                            "status": "success"
                                        },status.HTTP_200_OK)
                                    else:
                                        return Response("Zip file extraction fails",status.HTTP_400_BAD_REQUEST)
                                else:
                                    return Response("File size to big",status.HTTP_400_BAD_REQUEST)
                            except FileNotFoundError:
                                return Response("Zip file extraction fails",status.HTTP_400_BAD_REQUEST)
                            except BadZipFile:
                                return Response("Zip file extraction fails",status.HTTP_400_BAD_REQUEST)
                            except Exception as e:
                                return Response("Unspecified IO error",status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response("User is not the author of the game",status.HTTP_401_UNAUTHORIZED)
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
                return Response({
                    "status": "unauthenticated",
                    "message": "invalid token"
                },status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "status": "unauthenticated",
                "message": "missing token"
            },status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET","PUT","DELETE"])
def gameid(request,slug):
    try:
        if request.method=="GET":
            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])

            if row:
                row=row[0]
                userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[1]])
                scorerow=query(db,"SELECT*FROM `score` WHERE `gameid`=%s",[row[0]])

                return Response({
                    "author": userrow[0][1],
                    "slug": row[5],
                    "title": row[4],
                    "description": row[6],
                    "gamePath": row[3],
                    "thumbnail": row[2],
                    "scoreCount": len(scorerow),
                    "uploadTimestamp": row[9],
                },status.HTTP_200_OK)
            else:
                return Response({
                    "status": "invaled",
                    "message": "Game not found"
                },status.HTTP_404_NOT_FOUND)

        elif request.method=="PUT":
            data=json.loads(request.body)
            title=data.get("title")
            description=data.get("description")

            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            usercheck=signincheck(request)
            if usercheck["success"]:
                if row:
                    if usercheck["data"]==row[0][1]:
                        invaliddata={}
                        check=True
                        if title==None or title=="":
                            title=row[0][4]
                        else:
                            if len(title)<3:
                                invaliddata["title"]="must be at least 3 characters long"
                                check=False
                            elif len(title)>60:
                                invaliddata["title"]="must be at most 60 characters long"
                                check=False

                        if description==None or description=="":
                            description=row[0][6]
                        else:
                            if len(description)>200:
                                invaliddata["description"]="must be at most 200 characters long"
                                check=False

                        if check:
                            query(db,"UPDATE `game` SET `title`=%s,`description`=%s,`updatetime`=%s WHERE `slug`=%s",[title,description,time(),slug])

                            return Response({
                                "status": "success"
                            },status.HTTP_200_OK)
                        else:
                            return Response({
                                "status": "invalid",
                                "message": "request body is not valid",
                                "violations": invaliddata
                            },status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({
                            "status": "forbidden",
                            "slug": "You are not the game author."
                        },status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "status": "invalid",
                        "slug": "Game not exists."
                    },status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(usercheck["data"],status.HTTP_401_UNAUTHORIZED)

        else:
            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            usercheck=signincheck(request)
            if usercheck["success"]:
                if row:
                    if usercheck["data"]==row[0][1]:
                        query(db,"DELETE FROM `game` WHERE `slug`=%s",[slug])
                        query(db,"DELETE FROM `score` WHERE `gameid`=%s",[row[0]["id"]])

                        return Response("",status.HTTP_200_OK)
                    else:
                        return Response({
                            "status": "forbidden",
                            "slug": "You are not the game author."
                        },status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "status": "invalid",
                        "slug": "Game not exists."
                    },status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(usercheck["data"],status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET","POST"])
def score(request,slug):
    try:
        if request.method=="GET":
            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            if row:
                data=[]
                scorerow=query(db,"SELECT*FROM `score` WHERE `gameid`=%s",[row[0]["id"]])
                for i in range(len(scorerow)):
                    userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[scorerow[i]["userid"]])[0]
                    data.append({
                        "username": userrow["username"],
                        "score": scorerow[i]["score"],
                        "timestamp": scorerow[i]["createtime"]
                    })

                return Response({
                    "scores": data
                },status.HTTP_200_OK)
            else:
                return Response({
                    "status": "invalid",
                    "slug": "Game not exists."
                },status.HTTP_401_UNAUTHORIZED)
        else:
            data=json.loads(request.body)
            score=data.get("score")

            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            usercheck=signincheck(request)
            print(usercheck)
            if usercheck["success"]:
                if row:
                    query(db,"INSERT INTO `score`(`userid`,`gameid`,`score`,`createtime`)VALUES(%s,%s,%s,%s)",[usercheck["data"],row[0]["id"],score,time()])

                    return Response({
                        "status": "success"
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "invalid",
                        "slug": "Game not exists."
                    },status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(usercheck["data"],status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)