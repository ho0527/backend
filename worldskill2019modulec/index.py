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

# main START
db="worldskill2024moduleb"

@api_view(["GET","POST","PUT","DELETE","PATCH"])
@exceptionhandler
def error404(request):
    return Response({
        "success": False,
        "data": "api not found"
    },status.HTTP_404_NOT_FOUND)