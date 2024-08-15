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
from function.sql import *
from function.thing import *

# main START
db="46nationalmoduled"

@api_view(["GET","POST"])
def getposttraintype(request):
    try:
        if request.method=="GET":
            row=query(db,"SELECT*FROM `type`")

            return Response({
                "success": True,
                "data": row
            },status.HTTP_200_OK)
        else:
            data=json.loads(request.body)
            name=data.get("name")
            passenger=data.get("passenger")
            row=query(db,"SELECT*FROM `type` WHERE `name`=%s",[name])
            if not row:
                if re.search("^[0-9]+$",passenger):
                    query(db,"INSERT INTO `type`(`name`,`passenger`)VALUES(%s,%s)",[name,passenger])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "乘載量必須為整數"
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "data": "車種已存在"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","DELETE"])
def putdeletetraintype(request,id):
    try:
        if request.method=="PUT":
            data=json.loads(request.body)
            name=data.get("name")
            passenger=data.get("passenger")
            row=query(db,"SELECT*FROM `type` WHERE `name`=%s",[name])
            if not row or row[0][0]==int(id):
                if re.search("^[0-9]+$",passenger):
                    query(db,"UPDATE `type` SET `name`=%s,`passenger`=%s WHERE `id`=%s",[name,passenger,id])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "乘載量必須為整數"
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "data": "車種已存在"
                },status.HTTP_400_BAD_REQUEST)
        else:
            if not query(db,"SELECT*FROM `train` WHERE `traintypeid`=%s",[id]):
                row=query(db,"DELETE FROM `type` WHERE `id`=%s",[id])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "列車被使用"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET","POST"])
def getposttrain(request):
    try:
        if request.method=="GET":
            row=query(db,"SELECT*FROM `train` WHERE `ps`!='DELETE'")
            stoprow=query(db,"SELECT*FROM `stop`")
            stationrow=query(db,"SELECT*FROM `station`")

            return Response({
                "success": True,
                "data": [row,stoprow,stationrow]
            },status.HTTP_200_OK)
        else:
            data=json.loads(request.body)
            name=data.get("name")
            passenger=data.get("passenger")
            row=query(db,"SELECT*FROM `type` WHERE `name`=%s",[name])
            if not row:
                if re.search("^[0-9]+$",passenger):
                    query(db,"INSERT INTO `type`(`name`,`passenger`)VALUES(%s,%s)",[name,passenger])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "乘載量必須為整數"
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "data": "車種已存在"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","DELETE"])
def putdeletetrain(request,id):
    try:
        if request.method=="PUT":
            data=json.loads(request.body)
            name=data.get("name")
            passenger=data.get("passenger")
            row=query(db,"SELECT*FROM `type` WHERE `name`=%s",[name])
            if not row or row[0][0]==int(id):
                if re.search("^[0-9]+$",passenger):
                    query(db,"UPDATE `type` SET `name`=%s,`passenger`=%s WHERE `id`=%s",[name,passenger,id])
                    return Response({
                        "success": True,
                        "data": ""
                    },status.HTTP_200_OK)
                else:
                    return Response({
                        "success": False,
                        "data": "乘載量必須為整數"
                    },status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "data": "車種已存在"
                },status.HTTP_400_BAD_REQUEST)
        else:
            if not query(db,"SELECT*FROM `train` WHERE `traintypeid`=%s",[id]):
                row=query(db,"DELETE FROM `type` WHERE `id`=%s",[id])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "列車被使用"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def adminsearchticket(request):
    try:
        page=request.GET.get("page")
        type=request.GET.get("type")
        value=request.GET.get("value")
        offset=int((int(page)-1)*3)
        row=query(db,"SELECT*FROM `ticket` LIMIT 5 OFFSET %s",[offset])
        if type=="phone":
            row=query(db,"SELECT*FROM `ticket` WHERE `phone`=%s LIMIT 5 OFFSET %s",[value,offset])
        elif type=="code":
            row=query(db,"SELECT*FROM `ticket` WHERE `code`=%s LIMIT 5 OFFSET %s",[value,offset])

        maindata=[]
        maxtotal=len(query(db,"SELECT*FROM `ticket`"))
        for i in range(len(row)):
            trainname=query(db,"SELECT*FROM `train` WHERE `id`=%s",[row[i][1]])[0][2]
            arrivetime=query(db,"SELECT*FROM `stop` WHERE `trainid`=%sAND`stationid`=%s",[row[i][1],row[i][3]])[0][4]
            startstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[row[i][3]])[0][2]
            endstation=query(db,"SELECT*FROM `station` WHERE `id`=%s",[row[i][4]])[0][2]
            delinnerhtml="<input type='button' class='bluebutton cancel' id='"+str(row[i][0])+"' value='取消'>"
            if row[i][8]==0:
                delinnerhtml="該列車已完成發車"
            elif row[i][8]==-1:
                delinnerhtml="<div class='cancel'>已取消 取消時間:<br>"+str(row[i]["deletetime"])+"</div>"
            maindata.append({
                "code": row[i][5],
                "createdate": row[i][9],
                "arrivetime": arrivetime,
                "trainname": trainname,
                "startstation": startstation+"站",
                "endstation": endstation+"站",
                "count": row[i][7],
                "delinnerhtml": delinnerhtml
            })
        return Response({
            "success": True,
            "data": {
                "maxtotal": maxtotal,
                "data": maindata
            }
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET","POST"])
def getpoststation(request):
    try:
        if request.method=="GET":
            row=query(db,"SELECT*FROM `station`")

            return Response({
                "success": True,
                "data": row
            },status.HTTP_200_OK)
        else:
            data=json.loads(request.body)
            name=data.get("name")
            englishname=data.get("englishname")
            row=query(db,"SELECT*FROM `station` WHERE `englishname`=%sOR`name`=%s",[englishname,name])
            if not row:
                query(db,"INSERT INTO `station`(`englishname`,`name`)VALUES(%s,%s)",[englishname,name])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "站點已存在"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT","DELETE"])
def putdeletestation(request,id):
    try:
        if request.method=="PUT":
            data=json.loads(request.body)
            name=data.get("name")
            englishname=data.get("englishname")
            row=query(db,"SELECT*FROM `station` WHERE `englishname`=%sOR`name`=%s",[englishname,name])
            if not row or row[0][0]==int(id):
                query(db,"UPDATE `station` SET `englishname`=%s,`name`=%s WHERE `id`=%s",[englishname,name,id])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "站點已存在"
                },status.HTTP_400_BAD_REQUEST)
        else:
            if not query(db,"SELECT*FROM `stop` WHERE `stationid`=%s",[id]):
                row=query(db,"DELETE FROM `station` WHERE `id`=%s",[id])
                return Response({
                    "success": True,
                    "data": ""
                },status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "data": "站點正在被使用 無法刪除!"
                },status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")

        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)