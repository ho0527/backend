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

@api_view(["GET","POST"])
def getpostapplication(request):
    try:
        if request.method=="GET":
            title=request.GET.get("title")
            minprice=request.GET.get("min_price")
            maxprice=request.GET.get("max_price")
            room=request.GET.get("room")
            minage=request.GET.get("min_age")
            maxage=request.GET.get("max_age")
            sortby=request.GET.get("sort_by")
            order=request.GET.get("order")
            page=request.GET.get("page")
            applicationstatus=request.GET.get("status")

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
            if not applicationstatus:
                applicationstatus=""

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
                    SELECT house.*,application.* FROM `houses` house
                    JOIN `applications` application ON house.id=application.house_id
                    WHERE (house.title LIKE %s)AND(%s<=house.price AND house.price<=%s)AND(%s<=house.room AND house.room<=%s)AND(%s<=house.age AND house.age<=%s)AND(application.status=%s) ORDER BY %s %s
                    """,["%"+title+"%",minprice,maxprice,roommin,roommax,minage,maxage,applicationstatus,sortby,order])

                    data=[]

                    for i in range(page*10,min((page+1)*10,len(row))):
                        applicationstatus=row[i][14]
                        if applicationstatus=="":
                            applicationstatus=None

                        data.append({
                            "id": row[i][12],
                            "status": applicationstatus,
                            "applied_at": row[i][15],
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
                            "applications": data,
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
        else:
            data=json.loads(request.body)
            houseid=data.get("house_id")

            row=query(db,"SELECT*FROM `houses` WHERE `id`=%s",[houseid])
            check=signincheck(request)
            if houseid:
                if type(houseid)==int:
                    if check["success"]:
                        if row:
                            if check["userid"]==row[0][1] or check["userpermission"]=="ADMIN":
                                applicationrow=query(db,"SELECT*FROM `applications` WHERE `house_id`=%s",[houseid])
                                adsrow=query(db,"SELECT*FROM `ads` WHERE `house_id`=%s",[houseid])
                                if not applicationrow:
                                    if not adsrow:
                                        query(db,"INSERT INTO `applications`(`house_id`,`status`,`applied_at`)VALUES(%s,%s,%s)",[houseid,"",time()])
                                        return Response({
                                            "success": True,
                                            "message": "",
                                            "data": {
                                                "application": {
                                                    "id": query(db,"SELECT*FROM `applications`")[-1][0]
                                                }
                                            }
                                        },status.HTTP_200_OK)
                                    else:
                                        return Response({
                                            "success": False,
                                            "message": "MSG_HOUSE_ADVERTISED",
                                            "data": ""
                                        },status.HTTP_409_CONFLICT)
                                else:
                                    return Response({
                                        "success": False,
                                        "message": "MSG_HOUSE_APPLIED",
                                        "data": ""
                                    },status.HTTP_409_CONFLICT)
                            else:
                                return Response({
                                    "success": False,
                                    "message": "MSG_PERMISSION_DENY",
                                    "data": ""
                                },status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({
                                "success": False,
                                "message": "MSG_HOUSE_NOT_EXISTS",
                                "data": ""
                            },status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(check,status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_WRONG_DATA_TYPE",
                        "data": ""
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_MISSING_FILED",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","DELETE"])
def editdeleteapplication(request,applicationid):
    try:
        if request.method=="PUT":
            data=json.loads(request.body)
            approve=data.get("approve")

            if approve!=None:
                if type(approve)==bool:
                    row=query(db,"SELECT*FROM `applications` WHERE `id`=%s",[applicationid])
                    check=signincheck(request)
                    if check["success"]:
                        if row:
                            if check["userpermission"]=="ADMIN":
                                if row[0][2]=="":
                                    if approve:
                                        data="APPROVE"
                                        query(db,"INSERT INTO `ads`(`house_id`,`expired_at`)VALUES(%s,%s)",[row[0][1],time()])
                                    else:
                                        data="REJECT"
                                    query(db,"UPDATE `applications` SET `status`=%s WHERE `id`=%s",[data,applicationid])
                                    return Response({
                                        "success": True,
                                        "message": "",
                                        "data": ""
                                    },status.HTTP_200_OK)
                                else:
                                    return Response({
                                        "success": False,
                                        "message": "MSG_ALREADY_ADVERISED",
                                        "data": ""
                                    },status.HTTP_409_CONFLICT)
                            else:
                                return Response({
                                    "success": False,
                                    "message": "MSG_PERMISSION_DENY",
                                    "data": ""
                                },status.HTTP_403_FORBIDDEN)
                        else:
                            return Response({
                                "success": False,
                                "message": "MSG_APPLICATION_NOT_EXISTS",
                                "data": ""
                            },status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(check,status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_WRONG_DATA_TYPE",
                        "data": ""
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "message": "MSG_MISSING_FILED",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)
        else:
            row=query(db,"SELECT*FROM `applications` WHERE `id`=%s",[applicationid])
            check=signincheck(request)
            if check["success"]:
                if row:
                    houserow=query(db,"SELECT*FROM `houses` WHERE `id`=%s",[row[0][1]])
                    if check["userid"]==houserow[0][1] or check["userpermission"]=="ADMIN":
                        if row[0][2]=="":
                            query(db,"DELETE FROM `applications` WHERE `id`=%s",[applicationid])
                            return Response({
                                "success": True,
                                "message": "",
                                "data": ""
                            },status.HTTP_200_OK)
                        else:
                            return Response({
                                "success": False,
                                "message": "MSG_ALREADY_ADVERISED",
                                "data": ""
                            },status.HTTP_409_CONFLICT)
                    else:
                        return Response({
                            "success": False,
                            "message": "MSG_PERMISSION_DENY",
                            "data": ""
                        },status.HTTP_403_FORBIDDEN)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_APPLICATION_NOT_EXISTS",
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