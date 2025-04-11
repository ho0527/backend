# import
import bcrypt
import hashlib
import json
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from pathlib import Path
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .utils import exception_handler

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
@api_view(["GET"])
@exception_handler
def geteventlist(request):
    data=json.loads(request.body)
    input=data.get("input").split("\n")

    responsedata={
        data: [],
        allvaild: True
    }

    for gtin in input:
        row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `gtin`=%s AND `deactivatetime` IS NOT  NULL",[gtin],SETTING["dbsetting"])
        if row:
            responsedata["data"].append({
                "gtin": gtin,
                "status": "vaild"
            })
        else:
            responsedata["allvaild"]=False
            responsedata["data"].append({
                "gtin": gtin,
                "status": "Invaild"
            })

    return Response({
        "success": True,
        "data": responsedata
    },status.HTTP_200_OK)

@api_view(["GET"])
@exception_handler
def getevent(request,organizerslug,eventslug):
    data=json.loads(request.body)
    input=data.get("input").split("\n")

    responsedata={
        data: [],
        allvaild: True
    }

    for gtin in input:
        row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `gtin`=%s AND `deactivatetime` IS NOT  NULL",[gtin],SETTING["dbsetting"])
        if row:
            responsedata["data"].append({
                "gtin": gtin,
                "status": "vaild"
            })
        else:
            responsedata["allvaild"]=False
            responsedata["data"].append({
                "gtin": gtin,
                "status": "Invaild"
            })

    return Response({
        "success": True,
        "data": responsedata
    },status.HTTP_200_OK)