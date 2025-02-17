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

# main START
db="54regional"

@api_view(["GET"])
def getcomment(request,id):
    try:
        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            row=row[0]
            return Response({
                "success": True,
                "data": {
                    "id": row[0],
                    "image": row[1],
                    "code": row[2],
                    "username": row[3],
                    "content": row[4],
                    "email": row[5],
                    "emailshow": row[6],
                    "phone": row[7],
                    "phoneshow": row[8]
                }
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此留言"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getcommentlist(request):
    try:
        data=[]
        row=query(db,"SELECT*FROM `comment` ORDER BY `createtime` DESC")

        for i in range(len(row)):
            email=row[i][5]
            phone=row[i][7]
            timedata="發表於: "+row[i][11]
            delete=False

            if row[i][6]=="":
                email="未顯示"

            if row[i][8]=="":
                phone="未顯示"

            if row[i][13]!=None:
                delete=True
                timedata=timedata+"，刪除於: "+row[i][13]
            elif row[i][12]!="":
                timedata=timedata+"，修改於: "+row[i][12]

            data.append({
                "id": row[i][0],
                "image": row[i][1],
                "code": row[i][2],
                "username": row[i][3],
                "content": row[i][4],
                "email": email,
                "phone": phone,
                "adminresponse": row[i][9],
                "pin": row[i][10],
                "timedata": timedata,
                "delete": delete
            })

        return Response({
            "success": True,
            "data": data
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newcomment(request):
    try:
        data=json.loads(request.body)
        image=data.get("image")
        username=data.get("username")
        email=data.get("email")
        content=data.get("content")
        phone=data.get("phone")
        code=data.get("code")

        row=query(db,"SELECT*FROM `comment` WHERE `code`=%s",[code])

        if not re.match(r"^.+@.+\..+((\..+)+)?$",email):
            return Response({
                "success": False,
                "errorkey": "email",
                "data": "email輸入錯誤(需要一個'@'及至少一個'.')"
            },status.HTTP_400_BAD_REQUEST)
        if not re.match(r"^[0-9]+((-([0-9]+)?)+)?$",phone):
            return Response({
                "success": False,
                "errorkey": "phone",
                "data": "電話號碼輸入錯誤(只能為數字(或包含'-'))"
            },status.HTTP_400_BAD_REQUEST)
        elif not re.match(r"^[0-9]{4}$",code):
            return Response({
                "success": False,
                "errorkey": "code",
                "data": "序號輸入錯誤(四碼數字)"
            },status.HTTP_400_BAD_REQUEST)
        elif row:
            return Response({
                "success": False,
                "errorkey": "code",
                "data": "序號已存在"
            },status.HTTP_409_CONFLICT)
        else:
            query(
                db,
                "INSERT INTO `comment`(`image`,`code`,`username`,`content`,`email`,`emailshow`,`phone`,`phoneshow`,`adminresponse`,`pin`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [image,code,username,content,email,"checked",phone,"checked","","",time(),""]
            )

            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def editcomment(request,id):
    try:
        data=json.loads(request.body)
        image=data.get("image")
        username=data.get("username")
        email=data.get("email")
        emailshow=data.get("emailshow")
        content=data.get("content")
        phone=data.get("phone")
        phoneshow=data.get("phoneshow")

        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            if not re.match(r"^.+@.+\..+((\..+)+)?$",email):
                return Response({
                    "success": False,
                    "errorkey": "email",
                    "data": "email輸入錯誤(需要一個'@'及至少一個'.')"
                },status.HTTP_400_BAD_REQUEST)
            if not re.match(r"^[0-9]+((-([0-9]+)?)+)?$",phone):
                return Response({
                    "success": False,
                    "errorkey": "phone",
                    "data": "電話號碼輸入錯誤(只能為數字(或包含'-'))"
                },status.HTTP_400_BAD_REQUEST)
            else:
                if emailshow:
                    emailshow="checked"
                else:
                    emailshow=""

                if phoneshow:
                    phoneshow="checked"
                else:
                    phoneshow=""
                query(
                    db,
                    "UPDATE `comment` SET `image`=%s,`username`=%s,`content`=%s,`email`=%s,`emailshow`=%s,`phone`=%s,`phoneshow`=%s,`updatetime`=%s WHERE `id`=%s",
                    [image,username,content,email,emailshow,phone,phoneshow,time(),id]
                )

                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此留言"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deletecomment(request,id):
    try:
        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            query(db,"UPDATE `comment` SET `deletetime`=%s WHERE `id`=%s",[time(),id])
            return Response({
                "success": True,
                "data": ""
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "查無此留言"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)