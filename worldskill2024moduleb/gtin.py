# import
import bcrypt
import hashlib
import json
import random
import re
import google.oauth2.id_token
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from pathlib import Path
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from .utils import exception_handler

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
@api_view(["POST"])
@exception_handler
def gtintest(request):
    data=json.loads(request.body)
    input=data.get("input").split("\n")

    response=[]

    for gtin in input:
        row=query(SETTING["dbname"],"SELECT*FROM `product` WHERE `gtin`=%s AND `deactivatetime` IS NOT  NULL",[companyid],SETTING["dbsetting"])

    return Response({
        "success": True,
        "data": row
    },status.HTTP_200_OK)