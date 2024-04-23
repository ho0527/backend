# import
import asyncio
import bcrypt
import base64
import hashlib
import json
import mss
import mss.tools
import random
import re
import os
import os.path
import pyautogui
import google.oauth2.id_token
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from google.oauth2 import id_token
from google.auth.transport import requests
from PIL import Image
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
db=SETTING["dbname"]

async def getscreen(scope,receive,send):
	while True:
		event = await receive()

		if event['type'] == 'websocket.connect':
			await send({
				'type': 'websocket.accept'
			})

		if event['type'] == 'websocket.disconnect':
			break

		if event['type'] == 'websocket.receive':
			if event['text'] == 'ping':
				await send({
					'type': 'websocket.send',
					'text': 'pong!'
				})

# async def getscreen(websocket):
# 	await websocket.accept()
# 	screenid=websocket.query_params.get("screenid")

# 	if screenid:
# 		try:
# 			screenid=int(screenid)
# 			i=0

# 			while i<1:
# 				data=await websocket.receive()

# 				if data:
# 					pass
# 					# handle data
# 				else:
# 					break

# 				i=i+1
# 		except ValueError:
# 			await websocket.close()
# 	else:
# 		await websocket.close()

@api_view(["GET"])
def getscreen(request,screenid):
	try:
		with mss.mss() as sct:
			screennumber=int(screenid)

			screen={
				"top": sct.monitors[screennumber]["top"],
				"left": sct.monitors[screennumber]["left"],
				"width": sct.monitors[screennumber]["width"],
				"height": sct.monitors[screennumber]["height"],
				"mon": screennumber,
			}

			sct_img=sct.grab(screen)

			path="./upload/computercontroller/"+screenid+".png"

			mss.tools.to_png(sct_img.rgb,sct_img.size,output=path)

		# 網址列轉碼
		with open(path,"rb") as file:
			base64string=base64.b64encode(file.read()).decode('ascii') # 將圖片內容轉換為Base64編碼

		return Response({
			"success": True,
			"data": "data:image/jpeg;base64,"+base64string
		},status.HTTP_200_OK)
	except Exception as error:
		printcolorhaveline("fail","[ERROR] "+str(error),"")
		return Response({
			"success": False,
			"data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
		},status.HTTP_500_INTERNAL_SERVER_ERROR)