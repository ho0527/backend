from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print("[ERROR]", str(error))  # 簡化錯誤輸出
            return Response({
                "success": False,
                "data": "[ERROR] Unknown error, please contact admin. Details:\n" + str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper