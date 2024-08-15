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
from function.sql import *
from function.thing import *
from .test import checkfile

# main START
db="chrisjudge_54national"

@api_view(["GET"])
def getuser(request,token):
    try:
        # token=request.headers.get("Authorization").split("Bearer ")[1]
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
        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            data=json.loads(request.body)
            username=data.get("username")
            nickname=data.get("nickname")

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
def newresponse(request,questionid):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            userid=userrow[0][1]

            responserow=query(db,"SELECT*FROM `response` WHERE `userid`=%sAND`questionid`=%s",[userid,questionid])
            questionrow=query(db,"SELECT*FROM `question` WHERE `id`=%s",[questionid])
            fileextension=os.path.splitext(request.FILES["file"].name)[1]
            if fileextension==".php":
                filename=str(userid).zfill(5)+"_"+str(questionid).zfill(5)+"_testfile"+"_"+"v"+(str(len(responserow)+1).zfill(4))+fileextension
                rpath="C:/nginx/python/backend/"
                fileurl=rpath+"chrisjudge_54national/upload/"+str(filename)

                uploadfile("./chrisjudge_54national/upload",request.FILES["file"],filename)

                response=checkfile(fileurl,questionrow[0])

                query(
                    db,
                    "INSERT INTO `response`(`userid`,`questionid`,`fileurl`,`fileextension`,`version`,`result`,`response`,`runtime`,`createtime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [userid,questionid,fileurl,fileextension,len(responserow)+1,response["result"],response["response"],response["runtime"],time()]
                )
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"回應題目: "+questionid,time()])

                return Response({
                    "success": True,
                    "data": response["result"]
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "檔案不支援!"
                },status.HTTP_400_BAD_REQUEST)
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

@api_view(["GET"])
def getresponse(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            userid=userrow[0][1]
            if request.GET.get("userid"):
                userid=request.GET.get("userid")
            row=query(db,"SELECT*FROM `response` WHERE `userid`=%s",[userid])
            return Response({
                "success": True,
                "data": row
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

@api_view(["GET"])
def getresponselist(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            row=query(db,"SELECT*FROM `response` WHERE `userid`=%s",[userrow[0][1]])
            return Response({
                "success": True,
                "data": row
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

@api_view(["GET"])
def getscorelist(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow:
            userrow=query(db,"SELECT*FROM `user`")
            questionrow=query(db,"SELECT*FROM `question`")
            data=[]
            questionidlist=[]
            for i in range(len(userrow)):
                responserow=query(db,"SELECT*FROM `response` WHERE `userid`=%s",[userrow[i][0]])
                responselist=[]
                for j in range(len(questionrow)):
                    response=""
                    for k in range(len(responserow)):
                        if responserow[k][2]==questionrow[j][0]:
                            response=responserow[k][6]
                    responselist.append({
                        "questionid": questionrow[j][0],
                        "result": response
                    })
                if int(userrow[i][4])>=4:
                    data.append({
                        "userid": userrow[i][0],
                        "nickname": userrow[i][3],
                        "responselist": None,
                        "reason": "user is admin"
                    })
                else:
                    data.append({
                        "userid": userrow[i][0],
                        "nickname": userrow[i][3],
                        "responselist": responselist
                    })

            for i in range(len(questionrow)):
                questionidlist.append(questionrow[i][0])

            return Response({
                "success": True,
                "data": data,
                "questionidlist": questionidlist
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