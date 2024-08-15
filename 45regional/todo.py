# import
import json
import math
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import *
from function.thing import *

# main START
db="45regional"

@api_view(["GET"])
def gettodo(request,id):
    try:
        row=query(db,"SELECT*FROM `todo` WHERE `id`=%s",[id])

        return Response({
            "success": True,
            "data": row[0]
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def gettodolist(request,deal,priority):
    try:
        if deal!="all" and priority!="all":
            row=query(db,"SELECT*FROM `todo` WHERE `deal`=%sAND`priority`=%s",[deal,priority])
        elif deal!="all" and priority=="all":
            row=query(db,"SELECT*FROM `todo` WHERE `deal`=%s",[deal])
        elif deal=="all" and priority!="all":
            row=query(db,"SELECT*FROM `todo` WHERE `priority`=%s",[priority])
        else:
            row=query(db,"SELECT*FROM `todo`")


        return Response({
            "success": True,
            "data": row
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newtodo(request):
    try:
        data=json.loads(request.body)
        title=data.get("title")
        starttime=data.get("starttime")
        endtime=data.get("endtime")
        deal=data.get("deal")
        priority=data.get("priority")
        description=data.get("description")

        query(db,"INSERT INTO `todo`(`title`,`starttime`,`endtime`,`deal`,`priority`,`description`,`createtime`)VALUES(%s,%s,%s,%s,%s,%s,%s)",[title,starttime,endtime,deal,priority,description,time()])

        return Response({
            "success": True,
            "data": "新增成功"
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def edittodo(request,id):
    try:
        data=json.loads(request.body)
        title=data.get("title")
        starttime=data.get("starttime")
        endtime=data.get("endtime")
        deal=data.get("deal")
        priority=data.get("priority")
        description=data.get("description")

        row=query(db,"SELECT*FROM `todo` WHERE `id`=%s",[id])

        if row:
            row=row[0]
            if not title:
                title=row[1]

            if not starttime:
                starttime=row[2]

            if not endtime:
                endtime=row[3]

            if not deal:
                deal=row[4]

            if not priority:
                priority=row[5]

            if not description:
                description=row[6]

            query(db,"UPDATE `todo` SET `title`=%s,`starttime`=%s,`endtime`=%s,`deal`=%s,`priority`=%s,`description`=%s,`updatetime`=%s WHERE `id`=%s",[title,starttime,endtime,deal,priority,description,time(),id])

            return Response({
                "success": True,
                "data": "edit success:)"
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "todo not found"
            },status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deletetodo(request,id):
    try:
        query(db,"DELETE FROM `todo` WHERE `id`=%s",[id])

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)