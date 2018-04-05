# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import  timedelta
import django.utils.timezone as t
from django.core.exceptions import ObjectDoesNotExist
from BackEnd.models import session,MobileUsers,GasUsers
import requests
import json
import time
import uuid

UrlTrains = "http://h044-sqa-05/"

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
            odjMobileUser = MobileUsers(login=account,password=password,uiduser=userid, mobilePhone= mobilePhone, email= email)
            odjMobileUser.save()
            GasUsersQR.uiduser = userid
            GasUsersQR.save()
        resp = {"code" : code,"message" : mess }
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    else:
        return HttpResponse(status=403)

@csrf_exempt
def account(request):
    if request.method == 'GET':
        token = request.META['Authorization: Bearer']
        try:
            objsession = session.objects.get(access_token=token)
            if(objsession.datetimecreate>=t.now()-timedelta(seconds=objsession.expires_in)):
                objMobileUser = MobileUsers.objects.get(uiduser=objsession.uiduser)
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
                response = {
                      "account" : objMobileUser.uiduser,
                      "lastName" : objGasUsers.lastname,
                      "address" : objGasUsers.address,
                      "email" : objMobileUser.email,
                      "mobilePhone" : objMobileUser.mobilePhone,
                      "inform": objMobileUser.inform
                    }
                resp = HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

        except Exception:
            resp = HttpResponse(status=403)
    elif request.method == 'POST':
        token = request.META['Authorization: Bearer']
        try:
            objsession = session.objects.get(access_token=token)
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            password = received_json_data['password']
            email = received_json_data['email']
            mobilePhone = received_json_data['mobilePhone']
            inform = received_json_data['inform']
            MobileUsers.objects.filter(uiduser=objsession.uiduser).update(password=password,email=email,inform=inform,mobilePhone=mobilePhone)
            resp = HttpResponse(status=200)
        except Exception:
            resp = HttpResponse(status=400)
    return resp


@csrf_exempt
def forgot(request):
    return ""

@csrf_exempt
def device(request):
    return HttpResponse(status=200)

@csrf_exempt
def Сhar(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_GetCharacters",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def MetersCharge(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_MetersCharge",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)


@csrf_exempt
def Meters(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_Meters",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def Pay(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_Pay",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def Saldo(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_Saldo",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def SaldoCurrent(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            res = SendRequestTrains("Mobile_SaldoCurrent",{"account":objGasUsers.account},True)
            return res['SaldoCurrent']
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def SaldoCurrentServiceId(request):
    token = request.META['Authorization: Bearer']
    ServiceId='01'
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            res = SendRequestTrains("Mobile_SaldoCurrentServiceId",{"account":objGasUsers.account,"ServiceId":ServiceId},True)
            return res['SaldoCurrent']
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def notification(request):
    token = request.META['Authorization: Bearer']
    if request.method == 'GET':
        try:
            objsession = session.objects.get(access_token=token)
            if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
                return SendRequestTrains("Mobile_notification",{"account":objGasUsers.account})
        except Exception:
            return HttpResponse(status=403)
    elif request.method == 'POST':
        # Всегда нет
        return HttpResponse(json.dumps({"code":"0", "message":"Сообщение не удалено!"}, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def notificationnew(request):
    token = request.META['Authorization: Bearer']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_NotificationNew",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def notificationid(request):
    token = request.META['Authorization: Bearer']
    Id='01'
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_notificationid",{"account":objGasUsers.account,"Id":Id})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

#-----------------------------------------------------
def SendRequestTrains(id,params,retjson=False):
    data={"id":id,"params":params}
    requestTrain = {
                "event": "SetNewRequest",
                "data": data
    }
    headers = {'content-type': 'application/json'}
    res = requests.post(UrlTrains + 'rest/', json=requestTrain, headers=headers)
    received_json_data = json.loads(res.content.decode("utf-8-sig"))
    if(retjson==False):
        resp = HttpResponse(json.dumps(received_json_data, ensure_ascii=False), content_type="application/json")
    else:
        resp = received_json_data
    return resp















