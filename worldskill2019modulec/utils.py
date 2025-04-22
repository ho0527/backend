from functools import wraps
from rest_framework.response import Response
from rest_framework import status

# 自創
from function.sql import *
from function.thing import *

def exceptionhandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            printcolorhaveline("fail","[ERROR] "+str(error),"")
            return Response({
                "success": False,
                "data": "[ERROR] Unknown error, please contact admin. Details:\n" + str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper