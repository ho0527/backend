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
from .function import signincheck
from .initialize import *

# main START
db=SETTING["dbname"]

@api_view(["GET"])
def getmusic(request,musicid):
    try:
        row=query(db,"SELECT*FROM `music` WHERE `id`=%s",[musicid])
        check=signincheck(request)
        if check["success"]:
            if row:
                if row[0][1]==check["userid"] or 4<=int(check["permission"]):
                    row=row[0]

                    if row[4]!=None:
                        subtitle={
                            "type": row[8],
                            "path": row[4]
                        }
                    else:
                        subtitle=None

                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢歌曲 id="+str(musicid),time()])
                    return Response({
                        "success": True,
                        "data": {
                            "musicid": row[0],
                            "albumid": row[2],
                            "musicpath": row[3],
                            "title": row[5],
                            "artist": row[6].split(","),
                            "duration": row[7],
                            "subtitle": subtitle
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
                    "data": "[WARNING]music not found"
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
def getmusiclist(request):
    try:
        check=signincheck(request)
        if check["success"]:
            if 4<=int(check["permission"]):
                row=query(db,"SELECT*FROM `music`")
            else:
                row=query(db,"SELECT*FROM `music` WHERE `userid`=%s",check["userid"])

            data=[]
            for i in range(len(row)):
                if row[i][4]!=None:
                    subtitle={
                        "type": row[i][8],
                        "path": row[i][4]
                    }
                else:
                    subtitle=None

                data.push({
                    "musicid": row[i][0],
                    "albumid": row[i][2],
                    "musicpath": row[i][3],
                    "title": row[i][5],
                    "artist": row[i][6].split(","),
                    "duration": row[i][7],
                    "subtitle": subtitle
                })

            query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢歌曲列表",time()])
            return Response({
                "success": True,
                "data": data
            },status.HTTP_200_OK)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newmusic(request):
    try:
        title=request.POST["title"]
        albumid=request.POST["albumid"]
        artist=request.POST["artist"]
        duration=request.POST["duration"]

        check=signincheck(request)
        if check["success"]:
            albumckeck=query(db,"SELECT*FROM `album` WHERE `id`=%s AND `deletetime` IS NULL",[albumid])
            if albumckeck:
                musicnameckeck=query(db,"SELECT*FROM `music` WHERE `title`=%sAND`albumid`=%s AND `deletetime` IS NULL",[title,albumid])
                if not musicnameckeck:
                    musicname=randomname()+os.path.splitext(request.FILES["music"].name)[1]
                    uploadfile("./upload/50nationalmodulea",request.FILES["music"],musicname)
                    musicpath="/backend/media/50nationalmodulea/"+musicname

                    try:
                        subtitlename=randomname()+os.path.splitext(request.FILES["subtitle"].name)[1]
                        uploadfile("./upload/50nationalmodulea",request.FILES["subtitle"],subtitlename)
                        subtitlepath="/backend/media/50nationalmodulea/"+subtitlename
                        subtitletype=request.POST["subtitletype"]
                    except Exception as error:
                        subtitlepath=None
                        subtitletype=None

                    query(db,"INSERT INTO `music`(`userid`,`albumid`,`muiscpath`,`subtitlepath`,`title`,`artist`,`duration`,`subtitletype`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[check["userid"],albumid,musicpath,subtitlepath,title,artist,duration,subtitletype,time(),""])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"新增歌曲",time()])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "[WARNING]music already exist"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]album not exist"
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
def editmusic(request,musicid):
    try:
        title=request.POST["title"]
        artist=request.POST["artist"]
        duration=request.POST["duration"]

        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `music` WHERE `id`=%s",[musicid])
            if row:
                musicnameckeck=query(db,"SELECT*FROM `music` WHERE `title`=%s AND `deletetime` IS NULL",[title])
                if not musicnameckeck or row[0][0]==musicnameckeck[0][0]:
                    if check["userid"]==row[0][1] or 4<=int(check["permission"]):
                        try:
                            musicname=randomname()+os.path.splitext(request.FILES["music"].name)[1]
                            uploadfile("./upload/50nationalmodulea",request.FILES["music"],musicname)
                            musicpath="/backend/media/50nationalmodulea/"+musicname
                        except Exception as error:
                            musicpath=request.POST["music"]

                        try:
                            subtitlename=randomname()+os.path.splitext(request.FILES["subtitle"].name)[1]
                            uploadfile("./upload/50nationalmodulea",request.FILES["subtitle"],subtitlename)
                            subtitlepath="/backend/media/50nationalmodulea/"+subtitlename
                            subtitletype=request.POST["subtitletype"]
                        except Exception as error:
                            subtitlepath=request.POST["subtitle"]
                            subtitletype=request.POST["subtitletype"]
                            if subtitlepath=="":
                                subtitlepath=None
                                subtitletype=None

                        query(db,"UPDATE `music` SET `muiscpath`=%s,`subtitlepath`=%s,`title`=%s,`artist`=%s,`duration`=%s,`subtitletype`=%s,`updatetime`=%s WHERE `id`=%s",[musicpath,subtitlepath,title,artist,artist,duration,subtitletype,time(),musicid])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"更新歌曲 id="+str(musicid),time()])
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
                        "data": "[WARNING]musicname already exist"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]album not exist"
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
def deletemusic(request,musicid):
    try:
        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `music` WHERE `id`=%s AND `deletetime` IS NULL",[musicid])
            if row:
                if check["userid"]==row[0][1] or int(check["permission"])>=4:
                    query(db,"UPDATE `music` SET `deletetime`=%s WHERE `id`=%s",[time(),musicid])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"刪除歌曲 id="+str(musicid),time()])
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
                    "data": "[WARNING]music not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)