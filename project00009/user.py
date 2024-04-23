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

@api_view(["POST"])
def signin(request):
	try:
		data=json.loads(request.body)
		username=data.get("username")
		password=data.get("password")

		if username and password:
			if type(username)==str and type(password)==str:
				row=query(db,"SELECT*FROM `user` WHERE (`username`=%s OR `no`=%s) AND `deletetime`=''",[username,username])
				if row and checkpassword(password,row[0][4]):
					token=str(hash(username,"sha256"))
					query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
					return Response({
						"success": True,
						"data": {
							"id": row[0][0],
							"username": row[0][1],
							"name": row[0][3],
							"permission": row[0][4],
							"token": token
						}
					},status.HTTP_200_OK)
				else:
					return Response({
						"success": False,
						"data": "[ERROR]user or password error"
					},status.HTTP_401_UNAUTHORIZED)
			else:
				return Response({
					"success": False,
					"data": "[ERROR]request data data-type error"
				},status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				"success": False,
				"data": "[ERROR]request data not found"
			},status.HTTP_400_BAD_REQUEST)
	except Exception as error:
		return Response({
			"success": False,
			"data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
		},status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signout(request):
	try:
		check=signincheck(request)

		if check["success"]:
			query(db,"DELETE FROM `token` WHERE `userid`=%s",[check["id"]])
			return Response({
				"success": True,
				"data": ""
			},status.HTTP_200_OK)
		else:
			return Response(check,status.HTTP_401_UNAUTHORIZED)
	except Exception as error:
		return Response({
			"success": False,
			"data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
		},status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def signup(request):
	try:
		data=json.loads(request.body)
		username=data.get("username")
		password=data.get("password")
		name=data.get("name")

		if username and password and name:
			if type(username)==str and type(password)==str and type(name)==str:
				row=query(db,"SELECT*FROM `user` WHERE `username`=%s AND `deletetime`=''",[username])
				if not row:
					query(db,"INSERT INTO `user`(`no`,`username`,`name`,`password`,`permission`,`createtime`,`updatetime`,`deletetime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",["",username,name,hashpassword(password),"1",time(),time(),""])
					row=query(db,"SELECT*FROM `user` WHERE `username`=%s",[username])
					token=str(hash(username,"sha256"))+str(str(random.randint(0,99999999)).zfill(8))
					query(db,"UPDATE `user` SET `no`=%s WHERE `id`=%s",["1"+(str(row[0][0]).zfill(5)),row[0][0]])
					query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
					# query(db,"INSERT INTO `log`(`userid`,`move`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],"註冊系統",time()])
					# query(db,"INSERT INTO `users`(`username`,`password`,`name`)VALUES(%s,%s,%s)",[username,hashpassword(password),name])
					return Response({
						"success": True,
						"data": {
							"userid": row[0][0],
							"name": row[0][3],
							"token": token
						}
					},status.HTTP_200_OK)
				else:
					return Response({
						"success": False,
						"data": "[ERROR]username already exist"
					},status.HTTP_409_CONFLICT)
			else:
				return Response({
					"success": False,
					"data": "[ERROR]request data data-type error"
				},status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				"success": False,
				"data": "[ERROR]request data not found"
			},status.HTTP_400_BAD_REQUEST)
	except Exception as error:
		printcolorhaveline("fail","[ERROR] "+str(error),"")
		return Response({
			"success": False,
			"data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
		},status.HTTP_500_INTERNAL_SERVER_ERROR)
