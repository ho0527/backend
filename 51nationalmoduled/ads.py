# import
import json
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import query,createdb
from function.thing import *
from .function import *
from .initialize import *
# main START
db=SETTING["dbname"]

@api_view(["GET"])
def getads(request):
    try:
        title=request.GET.get("title")
        minprice=request.GET.get("min_price")
        maxprice=request.GET.get("max_price")
        room=request.GET.get("room")
        minage=request.GET.get("min_age")
        maxage=request.GET.get("max_age")
        sortby=request.GET.get("sort_by")
        order=request.GET.get("order")
        page=request.GET.get("page")

        # init START
        if not title:
            title=""
        if not minprice:
            minprice=0
        if not maxprice:
            maxprice=MAXINT

        if room:
            roommin=room
            roommax=room
        else:
            roommin=0
            roommax=MAXINT

        if not minage:
            minage=0
        if not maxage:
            maxage=MAXINT
        if not sortby:
            sortby="published_at"
        if not order:
            order="asc"
        if not page:
            page=0

        minprice=int(minprice)
        maxprice=int(maxprice)
        roommin=int(roommin)
        roommax=int(roommax)
        minage=int(minage)
        maxage=int(maxage)
        page=int(page)
        # init END

        check=signincheck(request)
        if check["success"]:
            if check["userpermission"]=="ADMIN":
                row=query(db,"""
                SELECT house.*,ads.* FROM `houses` house
                JOIN `ads` ads ON house.id=ads.house_id
                WHERE (house.title LIKE %s)AND(%s<=house.price AND house.price<=%s)AND(%s<=house.room AND house.room<=%s)AND(%s<=house.age AND house.age<=%s) ORDER BY %s %s
                """,["%"+title+"%",minprice,maxprice,roommin,roommax,minage,maxage,sortby,order])

                data=[]

                for i in range(page*10,min((page+1)*10,len(row))):
                    data.append({
                        "id": row[i][12],
                        "expired_at": row[i][14],
                        "house": {
                            "id": row[i][0],
                            "title": row[i][2],
                            "cover_image_url": "https://hiiamchris.ddns.net"+query(db,"SELECT*FROM `images` WHERE `house_id`=%s AND `is_cover`=1",[row[i][0]])[0][2],
                            "price": row[i][4],
                            "square": row[i][5],
                            "room": row[i][6]
                        }
                    })

                return Response({
                    "success": True,
                    "message": "",
                    "data": {
                        "applications": [
                            data
                        ],
                        "total_count": len(row)
                    }
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_PERMISSION_DENY",
                    "data": ""
                },status.HTTP_403_FORBIDDEN)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def deleteads(request,adsid):
    try:
        row=query(db,"SELECT*FROM `ads` WHERE `id`=%s",[adsid])
        check=signincheck(request)
        if check["success"]:
            if row:
                if check["userpermission"]=="ADMIN":
                    query(db,"UPDATE `applications` SET `status`='' WHERE `house_id`=%s",[row[0][1]])
                    query(db,"DELETE FROM `ads` WHERE `id`=%s",[adsid])
                    return Response({
                        "success": True,
                        "message": "",
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_PERMISSION_DENY",
                        "data": ""
                    },status.HTTP_403_FORBIDDEN)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_AD_NOT_EXISTS",
                    "data": ""
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)