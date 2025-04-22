# import
import bcrypt
import hashlib
import json
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .utils import exceptionhandler

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
@api_view(["GET"])
@exceptionhandler
def login(request):
    data=json.loads(request.body)
    lastname=data.get("lastname")
    registrationcode=data.get("registration_code")

    if lastname and registrationcode:
        row=query(SETTING["dbname"],"SELECT*FROM `attendees` WHERE `lastname`=%s AND `registration_code`=%s)",[lastname,registrationcode],SETTING["dbsetting"])

        if row:
            row=row[0]
            token=hash(row["username"],"md5")
            query(SETTING["dbname"],"UPDATE `attendees` SET `login_token`=%s WHERE `id`=%s",[token,row["id"]],SETTING["dbsetting"])

            return Response({
                "firstname": row["firstname"],
                "lastname": row["lastname"],
                "username": row["username"],
                "email": row["email"],
                "token": token,
            },status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid login"
            },status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            "success": False,
            "message": "ERROR_request_data_not_found"
        },status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@exceptionhandler
def logout(request,companyid):
    token=request.GET.get("token")
    if token:
        tokenrow=query(SETTING["dbname"],"SELECT*FROM `attendees` WHERE `login_token`=%s",[token])
        if tokenrow:
            tokenrow=tokenrow[0]
            query(SETTING["dbname"],"UPDATE `attendees` SET `login_token`=NULL WHERE `id`=%s",[tokenrow["id"]])
            return Response({
                "message": "logout success",
            },status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid token"
            },status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            "message": "Invalid token"
        },status.HTTP_401_UNAUTHORIZED)