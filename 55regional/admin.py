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
db="54regional"

@api_view(["DELETE"])
def deletecomment(request,id):
    try:
        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            query(db,"DELETE FROM `comment` WHERE `id`=%s",[id])
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

@api_view(["POST"])
def responsecomment(request,id):
    try:
        data=json.loads(request.body)
        response=data.get("response")

        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            query(db,"UPDATE `comment` SET `adminresponse`=%s WHERE `id`=%s",[response,id])
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

@api_view(["POST"])
def pincomment(request,id):
    try:
        row=query(db,"SELECT*FROM `comment` WHERE `id`=%s",[id])

        if row:
            if row[0][10]=="":
                query(db,"UPDATE `comment` SET `pin`=''")
                query(db,"UPDATE `comment` SET `pin`='true' WHERE `id`=%s",[id])
            else:
                query(db,"UPDATE `comment` SET `pin`='' WHERE `id`=%s",[id])

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