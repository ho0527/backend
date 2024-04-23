# import
import base64
import bcrypt
import cv2
import hashlib
import io
import json
import mss
import mss.tools
import numpy
import os
import os.path
import random
import re
import pyautogui
import pytesseract
import google.oauth2.id_token
from PIL import Image
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

@api_view(["POST"])
def imageresult(request):
    try:
        data=json.loads(request.body)

        return Response({
            "success": True,
            "data": str(data)
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)