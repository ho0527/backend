# import pymysql
import datetime
import MySQLdb
from MySQLdb.cursors import DictCursor

# 自創
from function.thing import *

# main START

def createdb(dbname,host="127.0.0.1",username="root",password="",port="3306"):
    return MySQLdb.connect(host=host,db=dbname,user=username,passwd=password,port=port)

def query(dbname,query,data=None,setting={"host": "127.0.0.1","username": "root","password": "","port": 3306}):
    response=None
    try:
        db=MySQLdb.connect(host=setting["host"],db=dbname,user=setting["username"],passwd=setting["password"],port=setting["port"])
        cursor=db.cursor(DictCursor)
        cursor.execute(query,data)
        response=cursor.fetchall()
        db.commit()
        printcolorhaveline("green","use query function SUCCESS","")
    except Exception as error:
        printcolorhaveline("fail","[ERROR] use query function error "+str(error),"")
        db=MySQLdb.connect(host=setting["host"],db=dbname,user=setting["username"],passwd=setting["password"],port=setting["port"])
    if cursor:
        cursor.close()
    if db:
        db.close()
    return response


# import datetime
# import mysql.connector as mysql
# from mysql.connector import Error

# # 自創
# from function.thing import *

# # main START

# def createdb(dbname,host="localhost",username="root",password="",port=3306):
#     return mysql.connect(host=host,database=dbname,user=username,password=password,port=port)

# def query(dbname,query,data=None,setting={"host": "localhost","username": "root","password": "","port": 3306}):
#     response=None
#     db=None
#     cursor=None
#     try:
#         db=mysql.connect(host=setting["host"],database=dbname,user=setting["username"],password=setting["password"],port=setting["port"])
#         cursor=db.cursor(dictionary=True)  # 使用字典形式的游標
#         cursor.execute(query,data)
#         if query.strip().upper().startswith("SELECT"):
#             response=cursor.fetchall()
#             # 將 bytes 類型的欄位轉換為字串
#             for row in response:
#                 for key,value in row.items():
#                     if isinstance(value,bytes):
#                         row[key] = value.decode()  # 將 bytes 轉換為字符串
#                     elif isinstance(value,bytearray):
#                         row[key] = value.decode()  # 將 bytes 轉換為字符串
#         db.commit()
#         printcolorhaveline("green","use query function SUCCESS","")
#     except Exception as error:
#         printcolorhaveline("fail","[ERROR] use query function error " + str(error),"")
#     finally:
#         if cursor:
#             cursor.close()
#         if db:
#             db.close()
#     return response
