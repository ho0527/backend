# import
import bcrypt
import hashlib
import json
import mss
import mss.tools
import random
import re
import os
import os.path
import pyautogui
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
from function.sql import *
from function.thing import *
from .initialize import *

# main START
db=SETTING["dbname"]

@api_view(["GET"])
def gettodo(request,id):
    try:
        row=query(db,"SELECT*FROM `todo` WHERE `id`=%s",[id])

        return Response({
            "success": True,
            "data": row[0]
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def edittodo(request,id):
    try:
        data=json.loads(request.body)
        tododata=data.get("tododata")

        query(db,"UPDATE `todo` SET `tododata`=%s,`updatetime`=%s WHERE `id`=%s",[tododata,time(),id])
        row=query(db,"SELECT*FROM `todo` WHERE `id`=%s",[id])

        return Response({
            "success": True,
            "data": row[0]
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)