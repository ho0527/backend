# import pymysql
import datetime
import MySQLdb
import mysql.connector as mysql
from mysql.connector import Error
from django.http import JsonResponse

# 自創
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START

def createdb(dbname):
    return MySQLdb.connect(host="localhost",db=dbname,user="root",passwd="")

def query(dbname,query,data=None):
    respone=None
    try:
        db=createdb(dbname)
        cursor=db.cursor()
        cursor.execute(query,data)
        respone=cursor.fetchall()
        db.commit()
        printcolorhaveline("green","use query function SUCCESS","")
    except Exception as error:
        printcolorhaveline("fail","[ERROR] use query function error "+str(error),"")
        db=createdb(dbname)
    if cursor:
        cursor.close()
    if db:
        db.close()
    return respone