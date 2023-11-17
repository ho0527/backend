# import
import json
import math
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import query,createdb
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START
db="51regional"

@api_view(["GET"])
def getproduct(request):
    try:
        id=request.GET.get("id")
        if id:
            row=query(db,"SELECT*FROM `coffee` WHERE `id`=%s",[id])
            return Response({
                "success": True,
                "data": row
            },status.HTTP_200_OK)
        else:
            page=request.GET.get("page")
            keyword=request.GET.get("keyword")
            start=request.GET.get("start")
            end=request.GET.get("end")
            if not keyword:
                keyword=""
            if not start:
                start=0
            if not end:
                end=999999999999
            row=query(
                db,
                "SELECT*FROM `coffee` WHERE (`name`LIKE%sOR`description`LIKE%sOR`cost`LIKE%sOR`date`LIKE%sOR`link`LIKE%s)AND(%s<=`cost`AND`cost`<=%s) ORDER BY `date` DESC LIMIT %s OFFSET %s",
                ["%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%",float(start),float(end),4,int(page)*4]
            )
            countrow=query(
                db,
                "SELECT*FROM `coffee` WHERE (`name`LIKE%sOR`description`LIKE%sOR`cost`LIKE%sOR`date`LIKE%sOR`link`LIKE%s)AND(%s<=`cost`AND`cost`<=%s)",
                ["%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%","%"+str(keyword)+"%",float(start),float(end)]
            )
            product=query(db,"SELECT*FROM `product`")
            return Response({
                "success": True,
                "data": {
                    "maxcount": len(countrow),
                    "data": row,
                    "product": product
                }
            },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def gettemplate(request):
    try:
        id=request.GET.get("id")
        row=query(db,"SELECT*FROM `product`")
        if id:
            row=query(db,"SELECT*FROM `product` WHERE `id`=%s",[id])
        return Response({
            "success": True,
            "data": row
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def newproduct(request):
    try:
        data=json.loads(request.body)
        file=data.get("file")
        name=data.get("name")
        description=data.get("description")
        cost=data.get("cost")
        link=data.get("link")
        version=data.get("version")
        edit=data.get("edit")
        if edit=="true":
            id=data.get("id")
            query(db,"UPDATE `coffee` SET `picture`=%s,`name`=%s,`description`=%s,`cost`=%s,`date`=%s,`link`=%s,`product`=%s WHERE `id`=%s",[file,name,description,cost,time(),link,version,id])
            data="修改成功"
        else:
            query(db,"INSERT INTO `coffee`(`picture`,`name`,`description`,`cost`,`date`,`link`,`product`)VALUES(%s,%s,%s,%s,%s,%s,%s)",[file,name,description,cost,time(),link,version])
            data="新增成功"
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

@api_view(["POST"])
def newtemplate(request):
    try:
        data=json.loads(request.body)
        name=data.get("name")
        cost=data.get("cost")
        date=data.get("date")
        link=data.get("link")
        description=data.get("description")
        picture=data.get("picture")
        query(db,"INSERT INTO `product`(`name`,`cost`,`date`,`link`,`introduction`,`picture`)VALUES(%s,%s,%s,%s,%s,%s)",[name,cost,date,link,description,picture])
        row=query(db,"SELECT*FROM `product`")
        return Response({
            "success": True,
            "data": row[-1][0]
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail",error,"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)