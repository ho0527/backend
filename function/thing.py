import bcrypt
import hashlib
import json
import random
import re
import os
import datetime

# printcolor 函式：在終端機中以不同顏色打印文字
def printcolor(color,text):
    # 根据传入的颜色选择相应的 ANSI 转义码
    if color=="header": # 目前無用
        colorcode="\033[95m"
    elif color=="blue": # 目前無用
        colorcode="\033[94m"
    elif color=="green": # 用於通過 完成 成功 等等
        colorcode="\033[92m"
    elif color=="warning": # 用於用戶驗證失敗 用戶導致的錯誤 等等
        colorcode="\033[93m"
    elif color=="fail": # 用於程式錯誤 重大錯誤 驗證錯誤 等等
        colorcode="\033[91m"
    else:
        printcolor("fail","color error")
        colorcode="\033[95m"
        # raise ValueError("Unsupported color.")

    # 打印带有颜色的文本
    print(str(colorcode)+str(text)+str("\033[0m"))

# printcolorhaveline 函式：在終端機中打印分隔線並打印文字
def printcolorhaveline(color="green",text="",linestyle="-"):
    print(linestyle*30)
    printcolor(color,text)

# switch_key 函式：根據鍵的格式返回對應的鍵值
def switch_key(tkey):
    if tkey.startswith("#"):
        key=tkey[1:]
    else:
        key=tkey.split("@")[0]
    return key

def time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def hashpassword(password):
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode()

def checkpassword(password,dbpassword):
    return bcrypt.checkpw(password.encode("utf-8"),dbpassword.encode("utf-8"))

def hash(text,hashname):
    text=text.encode("utf-8")
    if hashname=="md5":
        return hashlib.md5(text).hexdigest()
    elif hashname=="sha1":
        return hashlib.sha1(text).hexdigest()
    elif hashname=="sha224":
        return hashlib.sha224(text).hexdigest()
    elif hashname=="sha256":
        return hashlib.sha256(text).hexdigest()
    elif hashname=="sha384":
        return hashlib.sha384(text).hexdigest()
    elif hashname=="sha512":
        return hashlib.sha512(text).hexdigest()
    elif hashname=="sha3_224":
        return hashlib.sha3_224(text).hexdigest()
    elif hashname=="sha3_256":
        return hashlib.sha3_256(text).hexdigest()
    elif hashname=="sha3_384":
        return hashlib.sha3_384(text).hexdigest()
    elif hashname=="sha3_512":
        return hashlib.sha3_512(text).hexdigest()
    else:
        return "error no this hashname"

def uploadfile(path,file,name):
    try:
        with open(os.path.join(path,name),"wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
    except Exception as error:
        printcolorhaveline("fail","[ERROR] function uploadfile error: "+str(error),"")

def randomname():
    name=""
    for i in range(50):
        name=name+str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[random.randint(0,61)])
    return name

def deletefile(path):
    if os.path.exists(path):
        os.remove(path)