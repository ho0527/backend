# import
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# 自創
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START
db="chclass"

# get log
@require_http_methods(["GET"])
def getlog(request):
    row=query(db,"SELECT*FROM `log`")
    print(time())

    return JsonResponse({
        "success": True,
        "data": row
    })