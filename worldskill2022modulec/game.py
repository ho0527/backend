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
from .function import signincheck

# main START
db="worldskill2022modulec"

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
                row=query(db,"SELECT*FROM `game` WHERE `deletetime` IS NULL",[])
                totalcount=0

                for i in range(len(row)):
                    userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[i]["userid"]])[0]
                    scorerow=query(db,"SELECT*FROM `score` WHERE `gameid`=%s",[row[i]["id"]])
                    gameversionrow=query(db,"SELECT*FROM `gameversion` WHERE `gameid`=%s",[row[i]["id"]])
                    if gameversionrow:
                        gameversionrow=gameversionrow[-1]
                        data.append({
                            "author": userrow["username"],
                            "slug": row[i]["slug"],
                            "title": row[i]["title"],
                            "description": row[i]["description"],
                            "thumbnail": gameversionrow["thumbnailpath"],
                            "scoreCount": len(scorerow),
                            "uploadTimestamp": gameversionrow["createtime"]
                        })
                        totalcount=totalcount+1

                if sortby=="popular":
                    data.sort(key=lambda data:data["scoreCount"],reverse=True if sorttype=="desc" else False)
                elif sortby=="title":
                    data.sort(key=lambda data:data["title"],reverse=True if sorttype=="desc" else False)
                else:
                    data.sort(key=lambda data:data["uploadTimestamp"],reverse=True if sorttype=="desc" else False)

                data=data[page*size:(page+1)*size]

                return Response({
                    "page": page,
                    "size": len(data),
                    "totalElements": totalcount,
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
                invaliddata["title"]={
                    "message": "required"
                }
                check=False
            else:
                slug=title.lower().replace(" ","-")
                if len(title)<3:
                    invaliddata["title"]={
                        "message": "must be at least 3 characters long"
                    }
                    check=False
                elif len(title)>60:
                    invaliddata["title"]={
                        "message": "must be at most 60 characters long"
                    }
                    check=False

            if description==None:
                invaliddata["description"]={
                    "message": "required"
                }
                check=False
            else:
                if len(description)>200:
                    invaliddata["description"]={
                        "message": "must be at most 200 characters long"
                    }
                    check=False

            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
            usercheck=signincheck(request)
            if usercheck["success"]:
                if not row:
                    if check:
                        query(db,
                            "INSERT INTO `game`(`userid`,`title`,`slug`,`description`,`createtime`,`updatetime`,`deletetime`)VALUES(%s,%s,%s,%s,%s,%s,%s)",
                            [usercheck["data"],title,slug,description,time(),time(),None]
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
                    "zipfile":{
                        "message": "required"
                    }
                }
            },status.HTTP_401_UNAUTHORIZED)

        try:
            token=request.POST["token"]
        except Exception as error:
            return Response({
                "status": "unauthenticated",
                "message": "missing token"
            },status.HTTP_401_UNAUTHORIZED)


        if token and token!="":
            tokenrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
            if tokenrow:
                if file:
                    row=query(db,"SELECT*FROM `game` WHERE `slug`=%s",[slug])
                    if row:
                        row=row[0]
                        if tokenrow[0]["userid"]==row["userid"]:
                            try:
                                gameversionrow=query(db,"SELECT*FROM `gameversion` WHERE `gameid`=%s",[row["id"]])

                                # 上傳zip到./temp資料夾
                                zipname=randomname()+os.path.splitext(file.name)[1]
                                uploadfile("./upload/worldskill2022modulec",file,zipname)
                                ziplink="./upload/worldskill2022modulec/"+zipname

                                # 解壓zip
                                if gameversionrow:
                                    version=str(int(gameversionrow[-1]["version"])+1)
                                else:
                                    version=1

                                with ZipFile(ziplink,"r") as zipfile:
                                    zipfile.extractall("./upload/worldskill2022modulec/"+(slug+"/"+version))
                                    filelist=zipfile.namelist()

                                if os.path.getsize(ziplink)<=1048576:
                                    os.remove(ziplink)
                                    if "index.html" in filelist:
                                        thumbnailpath=None
                                        if "thumbnail.png" in filelist:
                                            thumbnailpath="/backend/media/worldskill2022modulec/"+(slug+"/"+version)+"/thumbnail.png"

                                        query(db,"INSERT INTO `gameversion` (`gameid`,`thumbnailpath`,`gamepath`,`version`,`createtime`)VALUES(%s,%s,%s,%s,%s)",[row["id"],thumbnailpath,"/backend/media/worldskill2022modulec/"+(slug+"/"+version),version,time()])

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
                            "zipfile": {
                                "message": "required"
                            }
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
                userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row["userid"]])
                gameversionrow=query(db,"SELECT*FROM `gameversion` WHERE `gameid`=%s",[row["id"]])
                scorerow=query(db,"SELECT*FROM `score` WHERE `gameid`=%s",[row["id"]])

                if gameversionrow:
                    gameversionrow=gameversionrow[-1]
                    return Response({
                        "author": userrow[0]["username"],
                        "slug": row["slug"],
                        "title": row["title"],
                        "description": row["description"],
                        "gamePath": gameversionrow["gamepath"],
                        "thumbnail": gameversionrow["thumbnailpath"],
                        "scoreCount": len(scorerow),
                        "uploadTimestamp": row["createtime"],
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "invaled",
                        "message": "Game not found"
                    },status.HTTP_404_NOT_FOUND)
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
                    if usercheck["data"]==row[0]["userid"]:
                        invaliddata={}
                        check=True
                        if title==None or title=="":
                            title=row[0]["title"]
                        else:
                            if len(title)<3:
                                invaliddata["title"]="must be at least 3 characters long"
                                check=False
                            elif len(title)>60:
                                invaliddata["title"]="must be at most 60 characters long"
                                check=False

                        if description==None or description=="":
                            description=row[0]["description"]
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
            row=query(db,"SELECT*FROM `game` WHERE `slug`=%s AND `deletetime` IS NULL",[slug])
            usercheck=signincheck(request)
            if usercheck["success"]:
                if row:
                    if usercheck["data"]==row[0]["userid"]:
                        query(db,"UPDATE `game` SET `deletetime`=%s WHERE `slug`=%s",[nowtime(),slug])
                        query(db,"DELETE FROM `score` WHERE `gameid`=%s",[row[0]["id"]])

                        return Response("",status.HTTP_204_NO_CONTENT)
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
                scorerow=query(db,"""
                    SELECT
                        u.username,
                        MAX(s.score) AS score,
                        MAX(s.createtime) AS timestamp
                    FROM score s
                    JOIN user u ON s.userid=u.id
                    WHERE s.gameid=%s
                    GROUP BY s.userid
                    ORDER BY score DESC
                """,[row[0]["id"]])

                data=[]
                for i in range(len(scorerow)):
                    data.append({
                        "username": scorerow[i]["username"],
                        "score": scorerow[i]["score"],
                        "timestamp": scorerow[i]["timestamp"]
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