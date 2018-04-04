
# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import  timedelta
import django.utils.timezone as t
from django.core.exceptions import ObjectDoesNotExist
from BackEnd.models import session,MobileUsers,GasUsers
import json
import time
import uuid

@csrf_exempt
def token(request):
    if request.method == 'POST':
        username = request.GET['username']
        password = request.GET['password']
        uid = str(uuid.uuid4())
        r = MobileUsers.objects.filter(password=password,login=username)
        if r.count()!=0:
            uiduser = r[0]
            dbobjsession = session(access_token=uid, uiduser=uiduser)
            dbobjsession.save()
            responsetext = \
                {
            "access_token" : dbobjsession.access_token,
            "token_type" : "bearer",
            "expires_in" : dbobjsession.expires_in
             }
            resp = HttpResponse(json.dumps(responsetext, ensure_ascii=False), content_type="application/json")
        else:
            resp =HttpResponse(status=401)
    else:
        resp = HttpResponse(status=404)
    return resp

@csrf_exempt
def register(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8-sig"))
        account = received_json_data['account']
        lastname = received_json_data['lastName']
        password = received_json_data['password']
        confirmPassword = received_json_data['confirmPassword']
        email = received_json_data['email']
        mobilePhone = received_json_data['mobilePhone']
        code = 0
        NotExist=False
        try:
            GasUsersQR = GasUsers.objects.get(account=int(account),lastname=lastname)

        except ObjectDoesNotExist:
            NotExist = True
            mess="Связка указанного лицевого счета и фамилии не найдена"
        except Exception:
            NotExist = True
            mess = "Ошибка!Некорректно введены данные"
        if(password!=confirmPassword):
            mess = "Пароль и подтверждение пароля не совпадают"
        elif(GasUsersQR.uiduser!=""):
            mess = "Указанный номер лицевого счета уже зарегистрирован. Если Вы забыли пароль - пройдите процедуру восстановления пароля"
        elif(NotExist==False):
            code=1
            mess="Регистрация произведена"
            userid = str(uuid.uuid4())
            odjMobileUser = MobileUsers(login=account,password=password,uiduser=userid)
            odjMobileUser.save()
            GasUsersQR.uiduser = userid
            GasUsersQR.save()
        resp = {"code" : code,"message" : mess }
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    else:
        return HttpResponse(status=403)
