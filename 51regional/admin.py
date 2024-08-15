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
db="51regional"

@api_view(["GET"])
def getuserlist(request):
    try:
        keyword=request.GET.get("keyword")
        orderby=request.GET.get("orderby")
        ordertype=request.GET.get("ordertype")
        if ordertype in ["ASC", "DESC"]:
            row=query(
                db,
                "SELECT*FROM `user` WHERE `username`LIKE%sOR`password`LIKE%sOR`name`LIKE%sOR`number`LIKE%sOR`permission`LIKE%s ORDER BY `"+orderby+"` "+ordertype,
                ["%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%"]
            )
            return Response({
                "success": True,
                "data": row
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "Invalid ordertype value. It should be either 'ASC' or 'DESC'."
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def getuser(request,id):
    try:
        row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[id])
        if row:
            return Response({
                "success": True,
                "data": row[0]
            },status.HTTP_200_OK)
        else:
            return Response({
                "success": False,
                "data": "使用者不存在"
            },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def log(request):
    try:
        row=query(db,"SELECT*FROM `data` ORDER BY `id` DESC")
        return Response({
            "success": True,
            "data": row
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)