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
from .utils import exception_handler

# 自創
from function.sql import *
from function.thing import *

# main START
db="worldskill2024moduleb"

@api_view(["GET","POST","PUT","DELETE","PATCH"])
@exception_handler
def error404(request):
    return Response({
        "success": False,
        "data": "api not found"
    },status.HTTP_404_NOT_FOUND)