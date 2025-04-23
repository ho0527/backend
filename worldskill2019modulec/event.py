# import
import bcrypt
import hashlib
import json
import random
import re
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .utils import exceptionhandler

# 自創
from function.sql import *
from function.thing import *
from .initialize import *

# main START
@api_view(["GET"])
@exceptionhandler
def geteventlist(request):
    data=[]
    eventsrow=query(SETTING["dbname"],"SELECT*FROM `events`",[],SETTING["dbsetting"])

    for event in eventsrow:
        organizersrow=query(SETTING["dbname"],"SELECT*FROM `organizers` WHERE `id`=%s",[event["organizer_id"]],SETTING["dbsetting"])[0]
        data.append({
            "id": event["id"],
            "name": event["name"],
            "slug": event["slug"],
            "date": event["date"],
            "organizer": {
                "id": organizersrow["id"],
                "name": organizersrow["name"],
                "slug": organizersrow["slug"],
            },
        })

    return Response({
        "events": data
    },status.HTTP_200_OK)

@api_view(["GET"])
@exceptionhandler
def getevent(request,organizerslug,eventslug):
    data=[]
    row=query(SETTING["dbname"],"SELECT*FROM `events` WHERE `slug`=%s",[eventslug],SETTING["dbsetting"])

    if row:
        row=row[0]
        organizersrow=query(SETTING["dbname"],"SELECT*FROM `organizers` WHERE `id`=%s AND `slug`=%s",[row["organizer_id"],organizerslug],SETTING["dbsetting"])[0]
        if organizersrow:
            organizersrow=organizersrow[0]
            channeldata=[]
            ticketdata=[]
            channelsrow=query(SETTING["dbname"],"SELECT*FROM `channels` WHERE `event_id`=%s",[row["id"]],SETTING["dbsetting"])
            eventticketsrow=query(SETTING["dbname"],"SELECT*FROM `event_tickets` WHERE `event_id`=%s",[row["id"]],SETTING["dbsetting"])

            for channel in channelsrow:
                roomdata=[]
                roomsrow=query(SETTING["dbname"],"SELECT*FROM `rooms` WHERE `channel_id`=%s",[channel["id"]],SETTING["dbsetting"])

                for room in roomsrow:
                    sessiondata=[]
                    sessionsrow=query(SETTING["dbname"],"SELECT*FROM `sessions` WHERE `room_id`=%s",[room["id"]],SETTING["dbsetting"])

                    for session in sessionsrow:
                        sessiondata.append({
                            "id": session["id"],
                            "name": session["name"],
                            "description": session["description"],
                            "speaker": session["speaker"],
                            "start": session["start"],
                            "end": session["end"],
                            "type": session["type"],
                            "cost": session["cost"]
                        })

                    roomdata.append({
                        "id": room["id"],
                        "name": room["name"],
                        "sessions": sessiondata
                    })

                channeldata.append({
                    "id": channel["id"],
                    "name": channel["name"],
                    "rooms": roomdata
                })

            for ticket in eventticketsrow:
                description=None
                available=True

                if ticket["special_validity"]==None:
                    descriptiondata=json.loads(ticket["special_validity"])

                    if descriptiondata["type"]=="date":
                        date=descriptiondata["date"].split("-")
                        description="Available until "+date[1]+" "+date[2]+","+date[3]
                        if datetime.datetime.now() > datetime.datetime.strptime(date,"%Y-%m-%d 23:59:59"):
                            available=False

                    elif descriptiondata["type"]=="amount":
                        amount=descriptiondata["amount"]
                        description=amount+" tickets available"
                        registrationsrow=query(SETTING["dbname"],"SELECT*FROM `registrations` WHERE `ticket_id`=%s",[ticket["id"]],SETTING["dbsetting"])
                        if len(registrationsrow)>=amount:
                            available=False


                ticketdata.append({
                    "id": ticket["id"],
                    "name": ticket["name"],
                    "description": description,
                    "cost": ticket["cost"],
                    "available": available
                })

            return Response({
                "id": row["id"],
                "name": row["name"],
                "slug": row["slug"],
                "date": row["date"],
                "channels": channeldata,
                "tickets": ticketdata
            },status.HTTP_200_OK)
        else:
            return Response({
                "message": "Organizer not found"
            },status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            "message": "Event not found"
        },status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@exceptionhandler
def newevent(request,organizerslug,eventslug):
    token=request.GET.get("token")
    if token:
        tokenrow=query(SETTING["dbname"],"SELECT*FROM `attendees` WHERE `login_token`=%s",[token])
        if tokenrow:
            tokenrow=tokenrow[0]
            data=json.loads(request.body)
            ticketid=data.get("ticket_id")
            sessionidlist=data.get("session_ids")
            data=[]
            row=query(SETTING["dbname"],"SELECT*FROM `events` WHERE `slug`=%s",[eventslug],SETTING["dbsetting"])

            if row:
                row=row[0]
                organizersrow=query(SETTING["dbname"],"SELECT*FROM `organizers` WHERE `id`=%s AND `slug`=%s",[row["organizer_id"],organizerslug],SETTING["dbsetting"])[0]
                if organizersrow:
                    organizersrow=organizersrow[0]
                    registrationsrow=query(SETTING["dbname"],"SELECT*FROM `registrations` WHERE `attendee_id`=%s AND `ticket_id`=%s",[tokenrow["id"],ticketid],SETTING["dbsetting"])
                    if registrationsrow:
                        eventticketsrow=query(SETTING["dbname"],"SELECT*FROM `event_tickets` WHERE `id`=%s",[ticketid],SETTING["dbsetting"])

                        if eventticketsrow:
                            eventticketsrow=eventticketsrow[0]
                            available=True

                            if eventticketsrow["special_validity"]==None:
                                descriptiondata=json.loads(eventticketsrow["special_validity"])

                                if descriptiondata["type"]=="date":
                                    date=descriptiondata["date"].split("-")
                                    if datetime.datetime.now() > datetime.datetime.strptime(date,"%Y-%m-%d 23:59:59"):
                                        available=False

                                elif descriptiondata["type"]=="amount":
                                    amount=descriptiondata["amount"]
                                    registrationsrow=query(SETTING["dbname"],"SELECT*FROM `registrations` WHERE `ticket_id`=%s",[eventticketsrow["id"]],SETTING["dbsetting"])
                                    if len(registrationsrow)>=amount:
                                        available=False

                            if available:
                                query(SETTING["dbname"],"INSERT INTO `registrations` (`attendee_id`,`ticket_id`,`registration_time`) VALUES (%s,%s,%s)",[tokenrow["id"],ticketid,nowtime()],SETTING["dbsetting"])

                                registrationsrow=query(SETTING["dbname"],"SELECT*FROM `registrations` WHERE `attendee_id`=%s AND `ticket_id`=%s",[tokenrow["id"],ticketid],SETTING["dbsetting"])
                                registrationsrow=registrationsrow[-1]

                                for sessionid in sessionidlist:
                                    query(SETTING["dbname"],"INSERT INTO `session_registrations` (`registration_id`,`session_id`) VALUES (%s,%s)",[registrationsrow["id"],sessionid],SETTING["dbsetting"])

                                return Response({
                                    "message": "Registration successful"
                                },status.HTTP_200_OK)
                            else:
                                return Response({
                                    "message": "Ticket is no longer available"
                                },status.HTTP_401_UNAUTHORIZED)
                        else:
                            return Response({
                                "message": "Tickets not found"
                            },status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({
                            "message": "User already registered"
                        },status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        "message": "Organizer not found"
                    },status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "message": "Event not found"
                },status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "User not logged in"
            },status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            "message": "User not logged in"
        },status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
@exceptionhandler
def getuserevent(request):
    token=request.GET.get("token")
    if token:
        tokenrow=query(SETTING["dbname"],"SELECT*FROM `attendees` WHERE `login_token`=%s",[token])
        if tokenrow:
            tokenrow=tokenrow[0]
            data=[]
            row=query(SETTING["dbname"],"SELECT*FROM `registrations` WHERE `attendee_id`=%s",[tokenrow["id"]],SETTING["dbsetting"])

            for registration in row:
                eventsrow=query(SETTING["dbname"],"SELECT*FROM `events` WHERE `id`=%s",[registration["event_id"]],SETTING["dbsetting"])
                event=eventsrow[0]
                organizersrow=query(SETTING["dbname"],"SELECT*FROM `organizers` WHERE `id`=%s",[event["organizer_id"]],SETTING["dbsetting"])
                organizer=organizersrow[0]
                sessionregistrationsrow=query(SETTING["dbname"],"SELECT*FROM `session_registrations` WHERE `registration_id`=%s",[registration["id"]],SETTING["dbsetting"])
                sessionidlist=[]

                for sessionregistration in sessionregistrationsrow:
                    sessionidlist.append(sessionregistration["session_id"])

                data.append({
                    "event": {
                        "id": event["id"],
                        "name": event["name"],
                        "slug": event["slug"],
                        "date": event["date"],
                    },
                    "organizer": {
                        "id": organizer["id"],
                        "name": organizer["name"],
                        "slug": organizer["slug"]
                    },
                    "session_ids": sessionidlist
                })

            return Response({
                "registrations": data
            },status.HTTP_200_OK)
        else:
            return Response({
                "message": "User not logged in"
            },status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            "message": "User not logged in"
        },status.HTTP_401_UNAUTHORIZED)