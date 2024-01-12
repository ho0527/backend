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
def getleftroom(request,date,month):
    try:
        data=[]
        row=query(db,"SELECT*FROM `roomorder` WHERE `startdate`LIKE%s",["%"+date+"/"+month.zfill(2)+"%"])

        for i in range(31):
            data.append({
                "1": False,
                "2": False,
                "3": False,
                "4": False,
                "5": False,
                "6": False,
                "7": False,
                "8": False,
            })

            for j in range(len(row)):
                startdate=int(row[j][2].split("/")[2])
                enddate=int(row[j][3].split("/")[2])
                if startdate<=i+1 and i+1<=enddate:
                    bookroomlist=row[j][4].split(",")
                    for k in range(len(bookroomlist)):
                        data[i][bookroomlist[k]]=True

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

@api_view(["GET"])
def getroomorder(request,id):
    try:
        row=query(db,"SELECT*FROM `roomorder` WHERE `id`=%s",[id])

        if row:
            row=row[0]
            return Response({
                "success": True,
                "data": {
                    "id": row[0],
                    "no": row[1],
                    "startdate": row[2],
                    "enddate": row[3],
                    "roomno": row[4],
                    "username": row[5],
                    "email": row[6],
                    "phone": row[7],
                    "totalprice": row[8],
                    "deposit": row[9],
                    "ps": row[10],
                    "createtime": row[11],
                    "updatetime": row[12]
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
def getroomorderlist(request):
    try:
        data=[]
        row=query(db,"SELECT*FROM `roomorder`")

        for i in range(len(row)):
            data.append({
                "id": row[i][0],
                "no": row[i][1],
                "startdate": row[i][2],
                "enddate": row[i][3],
                "roomno": row[i][4],
                "username": row[i][5],
                "email": row[i][6],
                "phone": row[i][7],
                "totalprice": row[i][8],
                "deposit": row[i][9],
                "ps": row[i][10],
                "createtime": row[i][11],
                "updatetime": row[i][12]
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
def newroomorder(request):
    try:
        data=json.loads(request.body)
        startdate=data.get("startdate")
        enddate=data.get("enddate")
        roomno=data.get("roomno")
        username=data.get("username")
        email=data.get("email")
        phone=data.get("phone")
        totalprice=data.get("totalprice")
        deposit=data.get("deposit")
        ps=data.get("ps")

        row=query(db,"SELECT*FROM `roomorder`")

        no=datetime.datetime.now().strftime("%Y%m%d")+str(len(row)+1).zfill(4)

        query(
            db,
            "INSERT INTO `roomorder`(`no`,`startdate`,`enddate`,`roomno`,`username`,`email`,`phone`,`totalprice`,`deposit`,`ps`,`createtime`,`updatetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [no,startdate,enddate,roomno,username,email,phone,totalprice,deposit,ps,time(),""]
        )

        return Response({
            "success": True,
            "data": no
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def editroomorder(request,id):
    try:
        data=json.loads(request.body)
        startdate=data.get("startdate")
        enddate=data.get("enddate")
        roomno=data.get("roomno")
        username=data.get("username")
        email=data.get("email")
        phone=data.get("phone")
        totalprice=data.get("totalprice")
        deposit=data.get("deposit")
        ps=data.get("ps")

        row=query(db,"SELECT*FROM `roomorder` WHERE `id`=%s",[id])

        if row:
            query(
                db,
                "UPDATE `roomorder` SET `startdate`=%s,`enddate`=%s,`roomno`=%s,`username`=%s,`email`=%s,`phone`=%s,`totalprice`=%s,`deposit`=%s,`ps`=%s,`updatetime`=%s WHERE `id`=%s",
                [startdate,enddate,roomno,username,email,phone,totalprice,deposit,ps,time(),id]
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
def deleteroomorder(request,id):
    try:
        row=query(db,"SELECT*FROM `roomorder` WHERE `id`=%s",[id])

        if row:
            query(db,"DELETE FROM `roomorder` WHERE `id`=%s",[id])
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