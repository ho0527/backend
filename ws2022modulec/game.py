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

# 自創
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key,hashpassword,checkpassword,hash,uploadfile

# main START
db="chrisjudge"

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

@api_view(["GET"])
def getuser(request,token):
    try:
        row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if row:
            userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[0][1]])
            if userrow:
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][1],"查詢使用者id: "+str(row[0][1]),time()])
                return Response({
                    "success": True,
                    "data": userrow[0]
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "使用者不存在請重新登入"
                },status.HTTP_403_FORBIDDEN)
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

@api_view(["PUT"])
def edituser(request):
    try:
        data=json.loads(request.body)
        username=data.get("username")
        nickname=data.get("nickname")

        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            query(db,"UPDATE `user` SET `username`=%s,`nickname`=%s,`updatetime`=%s WHERE `id`=%s",[username,nickname,time(),userrow[0][1]])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userrow[0][1],"修改使用者id: "+userrow[0][1],time()])

            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "請先登入!"
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deluser(request,id):
    try:
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[request.headers.get("Authorization").split("Bearer ")[1]])
        if userrow:
            userid=userrow[0][1]
            query(db,"DELETE FROM `question` WHERE `id`=%s",[id])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"刪除題目id: "+id,time()])

            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "請先登入!"
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newans(request,questionid):
    try:
        print(request.POST)
        print(request.FILES)
        uploadfile("./chrisjudge/upload",request.FILES["file"])
        # file.save(os.path.join("upload",get_valid_filename(file.filename)))
        # token=request.headers.get("Authorization").split("Bearer ")[1]
        # userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        # if userrow:
        #     userid=userrow[0][1]
        #     query(db,"DELETE FROM `question` WHERE `id`=%s",[id])
        #     query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"刪除題目id: "+id,time()])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
        # else:
        #     return Response({
        #         "success": False,
        #         "data": "請先登入!"
        #     },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)