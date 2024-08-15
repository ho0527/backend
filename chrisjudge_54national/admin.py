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

# main START
db="chrisjudge_54national"

@api_view(["GET"])
def getquestionlist(request):
    try:
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[request.headers.get("Authorization").split("Bearer ")[1]])
        if userrow:
            userid=userrow[0][1]
            row=query(db,"SELECT*FROM `question`")
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"查詢題目",time()])

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
def getquestion(request,id):
    try:
        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[request.headers.get("Authorization").split("Bearer ")[1]])
        if userrow:
            userid=userrow[0][1]
            row=query(db,"SELECT*FROM `question` WHERE `id`=%s",[id])
            if row:
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"查詢題目id: "+str(id),time()])

                return Response({
                    "success": True,
                    "data": row[0]
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "查無此題目!"
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

@api_view(["POST"])
def newquestion(request):
    try:
        data=json.loads(request.body)
        title=data.get("title")
        print("title="+str(title))
        description=data.get("description")
        tag=data.get("tag")
        input=data.get("input")
        output=data.get("output")
        maxruntime=data.get("maxruntime")

        token=None
        if request.headers.get("Authorization"):
            token=request.headers.get("Authorization").split("Bearer ")[1]

        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if userrow and token!=None:
            userid=userrow[0][1]
            query(db,"INSERT INTO `question`(`userid`,`title`,`description`,`tag`,`input`,`output`,`maxruntime`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[userid,title,description,tag,input,output,maxruntime,time(),time()])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"新增題目",time()])

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

@api_view(["PUT"])
def editquestion(request,id):
    try:
        data=json.loads(request.body)
        title=data.get("title")
        description=data.get("description")
        tag=data.get("tag")
        input=data.get("input")
        output=data.get("output")
        maxruntime=data.get("maxruntime")

        userrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[request.headers.get("Authorization").split("Bearer ")[1]])
        if userrow:
            userid=userrow[0][1]
            query(db,"UPDATE `question` SET `title`=%s,`description`=%s,`tag`=%s,`input`=%s,`output`=%s,`maxruntime`=%s,`updatetime`=%s WHERE `id`=%s",[title,description,tag,input,output,maxruntime,time(),id])
            query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[userid,"修改題目id: "+id,time()])

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
def delquestion(request,id):
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

@api_view(["GET"])
def getuserlist(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if row:
            loginuserrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[0][1]])
            if loginuserrow:
                userrow=query(db,"SELECT*FROM `user`")
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][1],"查詢使用者列表",time()])
                return Response({
                    "success": True,
                    "data": userrow
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "權限不足"
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

@api_view(["GET"])
def getlog(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if row:
            loginuserrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[0][1]])
            if int(loginuserrow[0][4])>=4:
                log=query(db,"SELECT*FROM `log`")
                query(db,"INSERT INTO `log`(`userid`,`move`,`movetime`)VALUES(%s,%s,%s)",[row[0][1],"獲取伺服器紀錄",time()])
                return Response({
                    "success": True,
                    "data": log
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "權限不足"
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

@api_view(["POST"])
def refdb(request):
    try:
        token=request.headers.get("Authorization").split("Bearer ")[1]
        row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
        if row:
            loginuserrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[row[0][1]])
            if int(loginuserrow[0][4])>=4:
                insertdata=[
                    ["web01",hashpassword("web01pass"),"web01",1,"",time(),time(),None],
                    ["web02",hashpassword("web02pass"),"web02",1,"",time(),time(),None],
                    ["web03",hashpassword("web03pass"),"web03",1,"",time(),time(),None],
                    ["web04",hashpassword("web04pass"),"web04",1,"",time(),time(),None],
                    ["web05",hashpassword("web05pass"),"web05",1,"",time(),time(),None],
                    ["web06",hashpassword("web06pass"),"web06",1,"",time(),time(),None],
                    ["web07",hashpassword("web07pass"),"web07",1,"",time(),time(),None],
                    ["web08",hashpassword("web08pass"),"web08",1,"",time(),time(),None],
                    ["web09",hashpassword("web09pass"),"web09",1,"",time(),time(),None],
                    ["web10",hashpassword("web10pass"),"web10",1,"",time(),time(),None],
                    # ["web11",hashpassword("web11pass"),"web11",1,"",time(),time(),None],
                    # ["web12",hashpassword("web12pass"),"web12",1,"",time(),time(),None],
                    ["backup",hashpassword("backuppass"),"backup",1,"",time(),time(),None],
                    ["admin",hashpassword("123456789"),"admin",5,"",time(),time(),None]
                ]

                query(db,"TRUNCATE TABLE `log`")
                query(db,"TRUNCATE TABLE `token`")
                query(db,"TRUNCATE TABLE `response`")
                query(db,"TRUNCATE TABLE `user`")
                query(db,"TRUNCATE TABLE `user`")

                for i in range(len(insertdata)):
                    query(db,"INSERT INTO `user`(`username`,`password`,`nickname`,`permission`,`email`,`createtime`,`updatetime`,`deletetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",insertdata[i])

                return Response({
                    "success": True,
                    "data": "更新成功"
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "權限不足"
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