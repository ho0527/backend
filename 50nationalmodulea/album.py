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
def getalbum(request,albumid):
    try:
        row=query(db,"SELECT*FROM `album` WHERE `id`=%s",[albumid])
        check=signincheck(request)
        if check["success"]:
            if row:
                if row[0][1]==check["userid"] or 4<=int(check["permission"]):
                    row=row[0]

                    musicrow=query(db,"SELECT*FROM `music` WHERE `albumid`=%s",[albumid])
                    musicdata=[]
                    for i in range(len(row)):
                        if musicrow[i][4]!=None:
                            subtitle={
                                "type": musicrow[i][8],
                                "path": musicrow[i][4]
                            }
                        else:
                            subtitle=None

                        musicdata.append({
                            "musicid": musicrow[i][0],
                            "albumid": musicrow[i][2],
                            "musicpath": musicrow[i][3],
                            "title": musicrow[i][5],
                            "artist": musicrow[i][6].split(","),
                            "duration": musicrow[i][7],
                            "subtitle": subtitle
                        })


                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢專輯 id="+str(albumid),time()])
                    return Response({
                        "success": True,
                        "data": {
                            "albumid": row[0],
                            "albumcover": row[2],
                            "title": row[3],
                            "description": row[4],
                            "attr": {
                                "publisher": row[5],
                                "publicdate": row[6]
                            },
                            "albumartist": row[7].split(","),
                            "music": musicdata
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
                    "data": "[WARNING]album not found"
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
def getalbumlist(request):
    try:
        check=signincheck(request)
        if check["success"]:
            if 4<=int(check["permission"]):
                row=query(db,"SELECT*FROM `album`")
            else:
                row=query(db,"SELECT*FROM `album` WHERE `userid`=%s",check["userid"])

            data=[]
            for i in range(len(row)):
                musicrow=query(db,"SELECT*FROM `music` WHERE `albumid`=%s",[row[i][0]])
                musicdata=[]
                for j in range(len(row)):
                    if musicrow[j][4]!=None:
                        subtitle={
                            "type": musicrow[j][8],
                            "path": musicrow[j][4]
                        }
                    else:
                        subtitle=None

                    musicdata.append({
                        "musicid": musicrow[j][0],
                        "albumid": musicrow[j][2],
                        "musicpath": musicrow[j][3],
                        "title": musicrow[j][5],
                        "artist": musicrow[j][6].split(","),
                        "duration": musicrow[j][7],
                        "subtitle": subtitle
                    })


                data.append({
                    "albumid": row[i][0],
                    "albumcover": row[i][2],
                    "title": row[i][3],
                    "description": row[i][4],
                    "attr": {
                        "publisher": row[i][5],
                        "publicdate": row[i][6]
                    },
                    "albumartist": row[i][7].split(","),
                    "music": musicdata
                })

            query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢專輯列表",time()])
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
def newalbum(request):
    try:
        title=request.POST["title"]
        publisher=request.POST["publisher"]
        publicdate=request.POST["publicdate"]
        description=request.POST["description"]
        albumartist=request.POST["albumartist"]

        try:
            extension=os.path.splitext(request.FILES["cover"].name)[1]

            if extension in ["png","jpg","jpeg","gif"]:
                covername=randomname()+os.path.splitext(request.FILES["cover"].name)[1]
                uploadfile("./upload/50nationalmodulea",request.FILES["cover"],covername)
                coverpath="/backend/media/50nationalmodulea/"+covername
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]cover extension not accept"
                },status.HTTP_404_NOT_FOUND)
        except Exception as error:
            coverpath=request.POST["cover"]

        check=signincheck(request)
        if check["success"]:
            albumnameckeck=query(db,"SELECT*FROM `album` WHERE `title`=%s AND `deletetime` IS NULL",[title])
            if not albumnameckeck:
                if 4<=int(check["permission"]):
                    query(db,"INSERT INTO `album`(`userid`,`coverpath`,`title`,`description`,`publisher`,`publicdate`,`albumartist`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[check["userid"],coverpath,title,description,publisher,publicdate,albumartist,time(),""])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"新增專輯",time()])
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
                    "data": "[WARNING]albumname already exist"
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
def editalbum(request,albumid):
    try:
        title=request.POST["title"]
        publisher=request.POST["publisher"]
        publicdate=request.POST["publicdate"]
        description=request.POST["description"]
        albumartist=request.POST["albumartist"]
        try:
            covername=randomname()+os.path.splitext(request.FILES["cover"].name)[1]
            uploadfile("./upload/50nationalmodulea",request.FILES["cover"],covername)
            coverpath="/backend/media/50nationalmodulea/"+covername
        except Exception as error:
            coverpath=request.POST["cover"]

        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `album` WHERE `id`=%s",[albumid])
            if row:
                albumnameckeck=query(db,"SELECT*FROM `album` WHERE `title`=%s AND `deletetime` IS NULL",[title])
                if not albumnameckeck or row[0][1]==albumnameckeck[0][1]:
                    if row[0][0]==check["userid"] or 4<=int(check["permission"]):
                        query(db,"UPDATE `album` SET `coverpath`=%s,`title`=%s,`description`=%s,`publisher`=%s,`publicdate`=%s,`albumartist`=%s,`updatetime`=%s WHERE `id`=%s",[coverpath,title,description,publisher,publicdate,albumartist,time(),albumid])
                        query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"更新專輯 id="+str(albumid),time()])
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
                        "data": "[WARNING]albumname already exist"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]album not found"
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
def deletealbum(request,albumid):
    try:
        check=signincheck(request)
        if check["success"]:
            row=query(db,"SELECT*FROM `album` WHERE `id`=%s AND `deletetime` IS NULL",[albumid])
            if row:
                if row[0][0]==check["userid"] or 4<=int(check["permission"]):
                    query(db,"UPDATE `album` SET `deletetime`=%s WHERE `id`=%s",[time(),albumid])
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"刪除專輯 id="+str(albumid),time()])
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
                    "data": "[WARNING]album not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)