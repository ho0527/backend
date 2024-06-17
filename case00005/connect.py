# import
import bcrypt
import hashlib
import json
import random
import re
import google.oauth2.id_token
import smtplib
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 自創
from function.sql import query,createdb
from function.thing import *

# main START
db="case00005"

@api_view(["POST"])
def newconnect(request):
    try:
        data=json.loads(request.body)
        companyname=data.get("companyname")
        name=data.get("name")
        phone=data.get("phone")
        email=data.get("email")
        content=data.get("content")
        # password="lryw vreq vfau vuxb"

        mimetext=MIMEText(f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>
                <body>
                    <h1>companyname: {companyname}</h1>
                    <h2>name: {name}</h2>
                    <h3>phone: {phone} | email: {email}</h3>
                    <p>content: {content}</p>
                </body>
            </html>
        ""","html","utf-8")
        mimetext["Subject"]="新的聯絡" #撰寫郵件標題
        mimetext["From"]="web.clelereve@gmail.com" #撰寫你的暱稱或是信箱
        mimetext["To"]="clelereve@gmail.com" #撰寫你要寄的人

        smtp=smtplib.SMTP("smtp.gmail.com",587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login("web.clelereve@gmail.com","lxbx bwnk rjhm jmwz") # 帳號,應用程式密碼
        if smtp.sendmail("web.clelereve@gmail.com",["clelereve@gmail.com"],mimetext.as_string())=={}:
            printcolorhaveline("green","郵件傳送成功!","")
        else:
            printcolorhaveline("fail","[ERROR]郵件傳送失敗!","")
        smtp.quit()

        return Response({
            "success": True,
            "data": ""
        },status.HTTP_200_OK)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] "+str(error),"")
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)