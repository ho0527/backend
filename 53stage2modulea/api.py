# import
import bcrypt
import graphene
import hashlib
import json
import os
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils.text import get_valid_filename
from django.views.decorators.http import require_http_methods
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# 自創
from function.sql import *
from function.thing import *

# main START
db="53stage2modulea"

def signincheck(token):
    row=query(db,"SELECT*FROM `token` WHERE `token`=%s",[token])
    if row:
        return {
            "id": row[0][0],
            "userid": row[0][1],
            "token": row[0][2]
        }
    else:
        return None

# --------------- api 01 ---------------
class signin(graphene.Mutation):
    usertoken=graphene.String()
    message=graphene.String()

    class Arguments:
        email=graphene.String(required=True)
        password=graphene.String(required=True)

    def mutate(self,info,email,password):
        row=query(db,"SELECT*FROM `user` WHERE `email`=%sAND`password`=%s",[email,password])
        if row:
            token=hash(email,"sha256")+str(random.randint(0,99999999)).zfill(8)
            query(db,"INSERT INTO `token`(`userid`,`token`,`createtime`)VALUES(%s,%s,%s)",[row[0][0],token,time()])
            return signin(usertoken=token)
        else:
            raise Exception("user not found")

# --------------- api 02 ---------------
class signout(graphene.Mutation):
    message=graphene.String()

    class Arguments:
        pass

    def mutate(self,info):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            query(db,"DELETE FROM `token` WHERE `token`=%s",[token["token"]])
            return signout(message="user logout success")
        else:
            raise Exception("unauthorized user")

# --------------- api 03 ---------------
class signup(graphene.Mutation):
    message=graphene.String()

    class Arguments:
        email=graphene.String(required=True)
        password=graphene.String(required=True)
        username=graphene.String(required=True)

    def mutate(self,info,email,password,username):
        row=query(db,"SELECT*FROM `user` WHERE `email`=%s",[email])
        if not row:
            query(db,"INSERT INTO `user`(`email`,`password`,`username`,`role`,`createtime`)VALUES(%s,%s,%s,%s,%s)",[email,password,username,"USER",time()])
            return signout(message="user register success")
        else:
            raise Exception("user already exists")

# --------------- api 04 ---------------
class getuser(graphene.Mutation):
    id=graphene.String()
    email=graphene.String()
    username=graphene.String()
    role=graphene.String()

    class Arguments:
        pass

    def mutate(self,info):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[token["id"]])[0]
            return getuser(id=row[0],email=row[1],username=row[3],role=row[4])
        else:
            raise Exception("unauthorized user")

# --------------- api 05 ---------------
class getbooklist(graphene.Mutation):
    pass
    id=graphene.String()
    email=graphene.String()
    username=graphene.String()
    role=graphene.String()

    class Arguments:
        pass

    def mutate(self,info):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            row=query(db,"SELECT*FROM `user` WHERE `id`=%s",[token["id"]])[0]
            return getuser(id=row[0],email=row[1],username=row[3],role=row[4])
        else:
            raise Exception("unauthorized user")

# --------------- api 06 ---------------
class newbook(graphene.Mutation):
    id=graphene.String()

    class Arguments:
        name=graphene.String(required=True)
        isbn=graphene.String(required=True)
        author=graphene.String(required=True)

    def mutate(self,info,name,isbn,author):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[token["userid"]])[0]
            if userrow[4]=="ADMIN":
                check=True
                isbn=isbn.replace("-","")

                if re.match(r"^[0-9]{13}$",isbn):
                    isbntotal=0
                    for i in range(12):
                        if i%2==0:
                            isbntotal=isbntotal+(int(isbn[i])*1)
                        else:
                            isbntotal=isbntotal+(int(isbn[i])*3)
                else:
                    check=False

                if check and -isbntotal%10==int(isbn[12]):
                    row=query(db,"SELECT*FROM `book` WHERE `isbn`=%s",[isbn])
                    if not row:
                        query(db,"INSERT INTO `book`(`name`,`isbn`,`author`,`createtime`)VALUES(%s,%s,%s,%s)",[name,isbn,author,time()])
                        row=query(db,"SELECT*FROM `book` WHERE `isbn`=%s",[isbn])[0]
                        return newbook(id=row[0])
                    else:
                        raise Exception("book already exists")
                else:
                    raise Exception("invaild isbn")
            else:
                raise Exception("permission denied")
        else:
            raise Exception("unauthorized user")

# --------------- api 07 ---------------
class deletebook(graphene.Mutation):
    message=graphene.String()

    class Arguments:
        id=graphene.Int(required=True)

    def mutate(self,info,id):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            userrow=query(db,"SELECT*FROM `user` WHERE `id`=%s",[token["userid"]])[0]
            if userrow[4]=="ADMIN":
                row=query(db,"SELECT*FROM `bookborrow` WHERE `bookid`=%s AND `returntime`IS NULL",[id])
                if not row:
                    row=query(db,"SELECT*FROM `book` WHERE `id`=%s",[id])
                    if row:
                        query(db,"DELETE FROM `book` WHERE `id`=%s",[id])
                        return deletebook(message="book delete success")
                    else:
                        raise Exception("book not exists")
                else:
                    raise Exception("book is rental")
            else:
                raise Exception("permission denied")
        else:
            raise Exception("unauthorized user")

# --------------- api 09 ---------------
class borrowbook(graphene.Mutation):
    id=graphene.String()

    class Arguments:
        bookId=graphene.Int(required=True)

    def mutate(self,info,bookId):
        id=bookId

        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            row=query(db,"SELECT*FROM `bookborrow` WHERE `bookid`=%s AND `returntime`IS NULL",[id])
            print("id="+str(id))
            print("row="+str(row))
            print(row)
            print(not row)
            if not row:
                row=query(db,"SELECT*FROM `book` WHERE `id`=%s",[id])
                if row:
                    query(db,"INSERT INTO `bookborrow`(`userid`,`bookid`,`createtime`)VALUES(%s,%s,%s)",[token["userid"],id,time()])
                    row=query(db,"SELECT*FROM `bookborrow` WHERE `bookid`=%s",[id])
                    return borrowbook(id=row[-1][0])
                else:
                    raise Exception("book not exists")
            else:
                raise Exception("book is rental")
        else:
            raise Exception("unauthorized user")

# --------------- api 10 ---------------
class returnbook(graphene.Mutation):
    message=graphene.String()

    class Arguments:
        id=graphene.Int(required=True)

    def mutate(self,info,id):
        authorization=info.context.headers.get("Authorization")
        token=None
        if authorization and authorization.startswith("Bearer "):
            token=signincheck(authorization.split(" ")[1])

        if token:
            row=query(db,"SELECT*FROM `bookborrow` WHERE `bookid`=%s AND `returntime`IS NULL",[id])
            if row:
                if row[0][1]==token["userid"]:
                    query(db,"UPDATE `bookborrow` SET `returntime`=%s WHERE `id`=%s",[time(),row[0][0]])
                    return returnbook(message="rent delete success")
                else:
                    raise Exception("permission denied")
            else:
                raise Exception("rent not exists")
        else:
            raise Exception("unauthorized user")


#######################################################

class Query(graphene.ObjectType):
    hello=graphene.String()

class Mutation(graphene.ObjectType):
    login=signin.Field()
    logout=signout.Field()
    register=signup.Field()
    user=getuser.Field()
    # user=getbooklist.Field()
    insertBook=newbook.Field()
    removeBook=deletebook.Field()
    insertRent=borrowbook.Field()
    removeRent=returnbook.Field()

schema=graphene.Schema(query=Query,mutation=Mutation)