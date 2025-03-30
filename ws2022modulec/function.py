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

db="ws2022modulec"

def signincheck(data):
    try:
        header=data.headers.get("Authorization")
        if header:
            tokenrow=query(db,"SELECT*FROM `token` WHERE `token`=%s",[header.split("Bearer ")[1]])
            if tokenrow:
                if (datetime.datetime.now()-datetime.datetime.strptime(tokenrow[0]["starttime"],'%Y-%m-%d %H:%M:%S')).total_seconds()<3600:
                    userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[tokenrow[0]["userid"]])
                    if userrow:
                        userrow=userrow[0]
                        if userrow["blocktime"]==None:
                            return {
                                "success": True,
                                "tokenid": tokenrow[0]["id"],
                                "data": tokenrow[0]["userid"]
                            }
                        else:
                            return {
                                "success": False,
                                "data": {
                                    "status": "blocked",
                                    "message": "User blocked",
                                    "reason": userrow["blockreason"]
                                }
                            }
                    else:
                        return {
                            "success": False,
                            "data": {
                                "status": "unauthenticated",
                                "message": "invalid token"
                            }
                        }
                else:
                    return {
                        "success": False,
                        "data": {
                            "status": "unauthenticated",
                            "message": "invalid token"
                        }
                    }
            else:
                return {
                    "success": False,
                    "data": {
                        "status": "unauthenticated",
                        "message": "invalid token"
                    }
                }
        else:
            return {
                "success": False,
                "data":{
                    "status": "unauthenticated",
                    "message": "missing token"
                }
            }
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)
