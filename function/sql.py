# import pymysql
import datetime
import MySQLdb
import mysql.connector as mysql
from mysql.connector import Error
from django.http import JsonResponse

# 自創
from function.thing import printcolor,printcolorhaveline,time,switch_key

# main START

def createdb(dbname,host="localhost",username="root",password=""):
    return MySQLdb.connect(host=host,db=dbname,user=username,passwd=password)

def query(dbname,query,data=None,host="localhost",username="root",password=""):
    respone=None
    try:
        db=MySQLdb.connect(host=host,db=dbname,user=username,passwd=password)
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