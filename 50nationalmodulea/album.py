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
                row=row[0]
                if check["userid"]==row[0][1] or int(check["permission"])>=4:
                    query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢使用者 id="+str(albumid),time()])
                    return Response({
                        "success": True,
                        "data": {
                            "albumid": row[0][0],
                            "albumname": row[0][1],
                            "albumpermission": row[0][3],
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
            if int(check["permission"])>=4:
                row=query(db,"SELECT*FROM `album`")
                data=[]
                for i in range(len(row)):
                    data.push({
                        "albumid": row[i][0],
                        "albumname": row[i][1],
                        "albumpermission": row[i][3],
                    })
                query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[check["userid"],"查詢使用者列表",time()])
                return Response({
                    "success": True,
                    "data": data
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "[WARNING]no permission"
                },status.HTTP_403_FORBIDDEN)
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
            covername=randomname()+os.path.splitext(request.FILES["cover"].name)[1]
            uploadfile("./upload/50nationalmodulea",request.FILES["cover"],covername)
            coverpath="/backend/media/50nationalmodulea/"+covername
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
                    if 4<=int(check["permission"]):
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
                if int(check["permission"])>=4:
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