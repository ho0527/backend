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
db="dcbot"

@api_view(["GET"])
def getwarnlist(request,guildid):
    try:
        data=[]
        totalwarndata=[]
        row=query(db,"SELECT*FROM `warn` WHERE `guildid`=%s",[guildid])

        for i in range(len(row)):
            usercheck=False
            userrow=query(db,"SELECT*FROM `user` WHERE `userid`=%s",[row[0][3]])

            for j in range(len(totalwarndata)):
                if totalwarndata[j]["userid"]==row[i][3]:
                    totalwarndata[j]["totalwarn"]=totalwarndata[j]["totalwarn"]+int(row[i][4])
                    totalwarn=totalwarndata[j]["totalwarn"]
                    usercheck=True
                    break

            if not usercheck:
                totalwarndata.append({
                    "userid": row[i][3],
                    "totalwarn": int(row[i][4])
                })
                totalwarn=int(row[i][4])

            data.append({
                "userid": row[i][3],
                "name": userrow[0][2],
                "warntime": row[i][4],
                "warnreason": row[i][5],
                "totalwarn": totalwarn,
                "createtime": row[i][6]
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