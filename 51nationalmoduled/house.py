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

# 自創
from function.sql import query,createdb
from function.thing import *
from .function import *
from .initialize import *

# main START
db=SETTING["dbname"]

@api_view(["GET","POST"])
def getposthouse(request):
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

            row=query(db,"SELECT*FROM `houses` WHERE (`title`LIKE%s)AND(%s<=`price`AND`price`<=%s)AND(%s<=`room`AND`room`<=%s)AND(%s<=`age`AND`age`<=%s) ORDER BY "+sortby+" "+order,["%"+title+"%",minprice,maxprice,roommin,roommax,minage,maxage])

            data=[]

            for i in range(page*10,min((page+1)*10,len(row))):
                adsrow=query(db,"SELECT*FROM `ads` WHERE `house_id`=%s",[row[i][0]])
                if len(adsrow)>0:
                    isads=True
                else:
                    isads=False

                data.append({
                    "id": row[i][0],
                    "title": row[i][1],
                    "cover_image_url": "https://hiiamchris.ddns.net"+query(db,"SELECT*FROM `images` WHERE `house_id`=%s AND `is_cover`=1",[row[i][0]])[0][2],
                    "price": row[i][4],
                    "square": row[i][5],
                    "room": row[i][6],
                    "is_ads": isads
                })

            return Response({
                "success": True,
                "message": "",
                "data": {
                    "house": [
                        data
                    ],
                    "total_count": len(row)
                }
            },status.HTTP_200_OK)
        else:
            try:
                title=request.POST["title"]
                description=request.POST["description"]
                image=request.FILES.getlist("image")
                coverindex=request.POST["cover_index"]
                price=request.POST["price"]
                square=request.POST["square"]
                room=request.POST["room"]
                floor=request.POST["floor"]
                totalfloor=request.POST["total_floor"]
                age=request.POST["age"]
                address=request.POST["address"]
            except Exception as error:
                return Response({
                    "success": False,
                    "message": "MSG_MISSING_FILED",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)

            try:
                coverindex=int(coverindex)
                price=int(price)
                square=int(square)
                room=int(room)
                floor=int(floor)
                totalfloor=int(totalfloor)
                age=int(age)
            except ValueError as error:
                return Response({
                    "success": False,
                    "message": "MSG_WRONG_DATA_TYPE",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)

            check=signincheck(request)

            if check["success"]:
                filelist=[]
                for i in range(len(image)):
                    filename=randomname()
                    extension=os.path.splitext(image[i].name)[1]
                    if extension in [".jpg",".jpeg",".png",".gif"]:
                        with open(os.path.join("./upload/51nationalmoduled",filename+extension),"wb") as file:
                            filelist.append(filename+extension)
                            for chunk in image[i].chunks():
                                file.write(chunk)
                    else:
                        return Response({
                            "success": False,
                            "message": "MSG_IMAGE_CAN_NOT_PROCESS",
                            "data": ""
                        },status.HTTP_400_BAD_REQUEST)

                if coverindex>=0 and coverindex-1<len(filelist):
                    query(db,"INSERT INTO `houses`(`user_id`,`title`,`description`,`price`,`square`,`room`,`floor`,`total_floor`,`age`,`address`,`published_at`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[check["userid"],title,description,price,square,room,floor,totalfloor,age,address,time()])

                    row=query(db,"SELECT*FROM `houses`")[-1]

                    for i in range(len(filelist)):
                        iscover=0
                        if coverindex==i:
                            iscover=1
                        query(db,"INSERT INTO `images`(`house_id`,`sort_order`,`path`,`is_cover`)VALUES(%s,%s,%s,%s)",[row[0],i,"/backend/media/51nationalmoduled/"+filelist[i],iscover])

                    return Response({
                        "success": True,
                        "message": "",
                        "data": {
                            "id": row[0]
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_INVALID_COVER_INDEX",
                        "data": ""
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response(check,status.HTTP_401_UNAUTHORIZED)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET","PUT","DELETE"])
def gedhouse(request):
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

            row=query(db,"SELECT*FROM `houses` WHERE (`title`LIKE%s)AND(%s<=`price`AND`price`<=%s)AND(%s<=`room`AND`room`<=%s)AND(%s<=`age`AND`age`<=%s) ORDER BY "+sortby+" "+order,["%"+title+"%",minprice,maxprice,roommin,roommax,minage,maxage])

            data=[]

            for i in range(page*10,min((page+1)*10,len(row))):
                adsrow=query(db,"SELECT*FROM `ads` WHERE `house_id`=%s",[row[i][0]])
                if len(adsrow)>0:
                    isads=True
                else:
                    isads=False

                data.append({
                    "id": row[i][0],
                    "title": row[i][1],
                    "cover_image_url": "https://hiiamchris.ddns.net"+query(db,"SELECT*FROM `images` WHERE `house_id`=%s AND `is_cover`=1",[row[i][0]])[0][2],
                    "price": row[i][4],
                    "square": row[i][5],
                    "room": row[i][6],
                    "is_ads": isads
                })

            return Response({
                "success": True,
                "message": "",
                "data": {
                    "house": [
                        data
                    ],
                    "total_count": len(row)
                }
            },status.HTTP_200_OK)
        elif request.method=="PUT":
            try:
                title=request.POST["title"]
                description=request.POST["description"]
                image=request.FILES.getlist("image")
                coverindex=request.POST["cover_index"]
                price=request.POST["price"]
                square=request.POST["square"]
                room=request.POST["room"]
                floor=request.POST["floor"]
                totalfloor=request.POST["total_floor"]
                age=request.POST["age"]
                address=request.POST["address"]
            except Exception as error:
                return Response({
                    "success": False,
                    "message": "MSG_MISSING_FILED",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)

            try:
                coverindex=int(coverindex)
                price=int(price)
                square=int(square)
                room=int(room)
                floor=int(floor)
                totalfloor=int(totalfloor)
                age=int(age)
            except ValueError as error:
                return Response({
                    "success": False,
                    "message": "MSG_WRONG_DATA_TYPE",
                    "data": ""
                },status.HTTP_400_BAD_REQUEST)

            check=signincheck(request)

            if check["success"]:
                filelist=[]
                for i in range(len(image)):
                    filename=randomname()
                    extension=os.path.splitext(image[i].name)[1]
                    if extension in [".jpg",".jpeg",".png",".gif"]:
                        with open(os.path.join("./upload/51nationalmoduled",filename+extension),"wb") as file:
                            filelist.append(filename+extension)
                            for chunk in image[i].chunks():
                                file.write(chunk)
                    else:
                        return Response({
                            "success": False,
                            "message": "MSG_IMAGE_CAN_NOT_PROCESS",
                            "data": ""
                        },status.HTTP_400_BAD_REQUEST)

                if coverindex>=0 and coverindex-1<len(filelist):
                    query(db,"INSERT INTO `houses`(`user_id`,`title`,`description`,`price`,`square`,`room`,`floor`,`total_floor`,`age`,`address`,`published_at`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[check["userid"],title,description,price,square,room,floor,totalfloor,age,address,time()])

                    row=query(db,"SELECT*FROM `houses`")[-1]

                    for i in range(len(filelist)):
                        iscover=0
                        if coverindex==i:
                            iscover=1
                        query(db,"INSERT INTO `images`(`house_id`,`sort_order`,`path`,`is_cover`)VALUES(%s,%s,%s,%s)",[row[0],i,"/backend/media/51nationalmoduled/"+filelist[i],iscover])

                    return Response({
                        "success": True,
                        "message": "",
                        "data": {
                            "id": row[0]
                        }
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "message": "MSG_INVALID_COVER_INDEX",
                        "data": ""
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response(check,status.HTTP_401_UNAUTHORIZED)
        else:
            pass
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)