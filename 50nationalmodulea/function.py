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

def signincheck(data):
    try:
        header=data.headers.get("Authorization")
        if header:
            row=query("ws2022modulec","SELECT*FROM `token` WHERE `token`=%s",[header.split("Bearer ")[1]])
            if row:
                return {
                    "success": True,
                    "tokenid": row[0][0],
                    "data": row[0][1]
                }
            else:
                return {
                    "success": False,
                    "data": "[WARNING]invalid token"
                }
        else:
            return {
                "success": False,
                "data": "[WARNING]no token login first"
            }
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)
