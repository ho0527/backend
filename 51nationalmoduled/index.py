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
from function.thing import printcolor,printcolorhaveline,time,switch_key,hashpassword,checkpassword,hash
from .initialize import *

# main START
db="51nationalmoduled"

@api_view(["GET"])
def searchtrain(request,startstaion,endstaion,traintype,getgodate):
    try:
        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def searchtraincode(request,traincode):
    try:
        row=query(db,"SELECT*FROM `train` WHERE `code`=%sAND`ps`!='DELETE'",[traincode])
        stoprow=query(db,"SELECT*FROM `stop`")
        stationrow=query(db,"SELECT*FROM `station`")

        return Response({
            "success": True,
            "data": [row,stoprow,stationrow]
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newticket(request):
    try:
        data=json.loads(request.body)
        trainid=data.get("trainid")
        typeid=data.get("typeid")
        startstationid=data.get("startstationid")
        endstationid=data.get("endstationid")
        phone=data.get("phone")
        count=int(data.get("count"))
        getgodate=data.get("getgodate")

        # 製作 ticket code
        code=""
        while True:
            for i in range(12):
                key=random.randrange(0,3)
                if key==0:
                    code=code+str(chr(random.randrange(ord("a"),ord("z"))))
                elif key==1:
                    code=code+str(chr(random.randrange(ord("A"),ord("Z"))))
                else:
                    code=code+str(random.randrange(0,9))
            if not query(db,"SELECT*FROM `ticket` WHERE `code`=%s",[code]):
                break

        query(
            db,
            "INSERT INTO `ticket`(`trainid`,`typeid`,`startstationid`,`endstationid`,`code`,`phone`,`count`,`statu`,`createdate`,`getgodate`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [trainid,typeid,startstationid,endstationid,code,phone,count,"1",time(),getgodate]
        )

        startstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[startstationid])[0][2]
        endstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[endstationid])[0][2]
        startstop=query(db,"SELECT*FROM `stop` WHERE `stationid`=%s",[startstationid])[0]
        endstop=query(db,"SELECT*FROM `stop` WHERE `stationid`=%s",[endstationid])[0]
        traincode=query(db,"SELECT*FROM `train` WHERE `id`=%s",[trainid])[0][2]
        stop=query(db,"SELECT*FROM `stop` WHERE %s<=`id`AND`id`<=%s",[startstop[0],endstop[0]])

        price=0
        for i in range(len(stop)):
            price=price+int(stop[i][3])
        total=count*(price)
        return Response({
            "success": True,
            "data": {
                "code": code,
                "startstation": startstation,
                "endstation": endstation,
                "traincode": traincode,
                "startstop": startstop[4],
                "price": price,
                "total": total
            }
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def searchticket(request):
    try:
        page=request.GET.get("page")
        type=request.GET.get("type")
        value=request.GET.get("value")
        offset=int((int(page)-1)*3)
        row=query(db,"SELECT*FROM `ticket` LIMIT 3 OFFSET %s",[offset])
        if type=="phone":
            row=query(db,"SELECT*FROM `ticket` WHERE `phone`=%s LIMIT 3 OFFSET %s",[value,offset])
        elif type=="code":
            row=query(db,"SELECT*FROM `ticket` WHERE `code`=%s LIMIT 3 OFFSET %s",[value,offset])

        maindata=[]
        maxtotal=len(query(db,"SELECT*FROM `ticket`"))
        for i in range(len(row)):
            traincode=query(db,"SELECT*FROM `train` WHERE `id`=%s",[row[i][1]])[0][2]
            arrivetime=query(db,"SELECT*FROM `stop` WHERE `trainid`=%sAND`stationid`=%s",[row[i][1],row[i][3]])[0][4]
            startstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[row[i][3]])[0][2]
            endstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[row[i][4]])[0][2]
            delinnerhtml="<input type='button' class='bluebutton cancel' id='"+str(row[i][0])+"' value='取消'>"
            if row[i][8]==0:
                delinnerhtml="該列車已完成發車"
            elif row[i][8]==-1:
                delinnerhtml="<div class='cancel'>已取消 取消時間:<br>"+str(row[i]["deletetime"])+"</div>"
            maindata.append({
                "code": row[i][5],
                "createdate": row[i][9],
                "arrivetime": arrivetime,
                "traincode": traincode,
                "startstation": startstation+"站",
                "endstation": endstation+"站",
                "count": row[i][7],
                "delinnerhtml": delinnerhtml
            })
        return Response({
            "success": True,
            "data": {
                "maxtotal": maxtotal,
                "data": maindata
            }
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def login(request):
    try:
        data=json.loads(request.body)

        row=query(db,"SELECT*FROM `user` WHERE `username`=%s AND `password`=%s",[data.get("username"),data.get("password")])

        if row:
            return Response({
                "success": True,
                "data": row[0][0]
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "username or password error"
            },status.HTTP_403_FORBIDDEN)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)