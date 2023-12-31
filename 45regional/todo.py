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
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START
db="45regional"

@api_view(["POST"])
def newtodo(request):
    try:
        data=json.loads(request.body)
        title=data.get("title")
        starthour=data.get("starthour")
        endhour=data.get("endhour")
        deal=data.get("deal")
        priority=data.get("priority")
        description=data.get("description")

        query(db,"INSERT INTO `todo`(`title`,`description`,`starttime`,`endtime`,`deal`,`priority`,`createtime`)VALUES(%s,%s,%s,%s,%s,%s,%s)",[title,starthour,endhour,deal,priority,description,time()])

        return Response({
            "success": True,
            "data": "新增成功"
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def gettodolist(request):
    try:
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