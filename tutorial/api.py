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
db="tutorial"

@api_view(["POST"])
def response(request):
    try:
        data=json.loads(request.body)
        link=data.get("link")
        subject=data.get("subject")
        id=data.get("id")
        title=data.get("title")
        description=data.get("description")
        connecttype=data.get("connecttype")
        connectdata=data.get("connectdata")

        query(db,"INSERT INTO `response`(`link`,`subject`,`subjectid`,`title`,`description`,`connecttype`,`connectdata`,`createtime`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",[link,subject,id,title,description,connecttype,connectdata,time()])

        mimetext=MIMEText(f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                </head>
                <body>
                    <h1><a href="{link}">網站連結</div></h1>
                    <h2>subject: {subject} | id: {id}</h2>
                    <h4>description: {description}</h4>
                    <h3>{connecttype} | {connectdata}</h3>
                </body>
            </html>
        ""","html","utf-8")
        mimetext["Subject"]=title #撰寫郵件標題
        mimetext["From"]="chris960527ho@gmail.com" #撰寫你的暱稱或是信箱
        mimetext["To"]="chris960527ho@gmail.com" #撰寫你要寄的人

        smtp=smtplib.SMTP("smtp.gmail.com",587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login("chris960527ho@gmail.com","yxyk pgsk pyxb zcsj") # 帳號,應用程式密碼
        if smtp.sendmail("chris960527ho@gmail.com",["chris960527ho@gmail.com"],mimetext.as_string())=={}:
            printcolorhaveline("green","郵件傳送成功!","")
        else:
            printcolorhaveline("fail","[ERROR]郵件傳送失敗!","")
        smtp.quit()

        return Response({
            "success": True,
            "data": "新增成功"
        },status.HTTP_200_OK)
    except Exception as error:
        return Response({
            "success": False,
            "data": "[ERROR] unknow error pls tell the admin error:\n"+str(error)
        },status.HTTP_500_INTERNAL_SERVER_ERROR)