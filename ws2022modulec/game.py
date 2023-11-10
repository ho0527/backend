# import
import bcrypt
import hashlib
import json
import os
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils.text import get_valid_filename
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key,hashpassword,checkpassword,hash,uploadfile
from ws2022modulec.function import usercheck

# main START

@api_view(["GET"])
def getgamelist(request):
    pass

@api_view(["POST"])
def newgame(request):
    pass

@api_view(["GET"])
def getgame(request):
    pass

@api_view(["PUT"])
def editgame(request):
    pass

@api_view(["DELETE"])
def delgame(request):
    pass