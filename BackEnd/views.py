# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import django.utils.timezone as t
from django.core.exceptions import ObjectDoesNotExist
from BackEnd.models import session,MobileUsers,GasUsers,News,tarifs,Uchastok
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
            uiduser = r[0].uiduser
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
            odjMobileUser = MobileUsers(login=account,password=password,uiduser=userid, mobilePhone= mobilePhone, email= email, inform=0)
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
        token = request.META['HTTP_AUTHORIZATION']
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
            else:
                resp = HttpResponse(status=403)
        except Exception:
            resp = HttpResponse(status=403)
    elif request.method == 'POST':
        token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
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
def SaldoCurrentServiceId(request,ServiceId=0):
    token = request.META['HTTP_AUTHORIZATION']
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
    token = request.META['HTTP_AUTHORIZATION']
    if request.method == 'GET':
        try:
            objsession = session.objects.get(access_token=token)
            if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
                return SendRequestTrains("Mobile_notification",{"account":objGasUsers.account})
        except Exception:
            return HttpResponse(status=403)
    elif request.method == 'POST':
        # Всегда нет на удаление
        return HttpResponse(json.dumps({"code":"0", "message":"Сообщение не удалено!"}, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def notificationnew(request):
    token = request.META['HTTP_AUTHORIZATION']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_NotificationNew",{"account":objGasUsers.account})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)

@csrf_exempt
def notificationid(request,Id):
    token = request.META['HTTP_AUTHORIZATION']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
            return SendRequestTrains("Mobile_notificationid",{"account":objGasUsers.account,"Id":Id})
    except Exception:
        return HttpResponse(status=403)

    return HttpResponse(status=403)


@csrf_exempt
def news(request):
    token = request.META['HTTP_AUTHORIZATION']
    objGasUsers= None
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
    except Exception:
        objGasUsers = None
    if(objGasUsers!=None):
        resp = GetNews(True)
    else:
        resp = GetNews(False)
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def newsid(request,Id):
    token = request.META['HTTP_AUTHORIZATION']
    objGasUsers= None
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
    except Exception:
        objGasUsers = None
    if(objGasUsers!=None):
        resp = GetNewsById(True)
    else:
        resp = GetNewsById(False)
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def tariffdate(request):
    d = t.now()
    tarifsres = tarifs.objects.filter(dateStart=d)
    if tarifsres.count()>0:
        tarifstring = tarifsres[0].tariff
    else:
        tarifstring = ""
    return HttpResponse(json.dumps({"tariff":tarifstring}, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def tarifflist(request):
    tarifsres = tarifs.objects.all()
    list =[]
    for tarif in tarifsres:
        list.append({"dateStart":tarif.dateStart.strftime("%d.%m.%Y"),"dateEnd":tarif.dateEnd.strftime("%d.%m.%Y")})
    return HttpResponse(json.dumps(list, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def uchastoklist(request):
    Uchres = Uchastok.objects.all()
    punkts = []
    for uch in Uchres:
        punkts.append({"id":uch.id,
                       "parentId":uch.parentid,
                       "name":uch.name,
                       "text":uch.text})
    return HttpResponse(json.dumps({"date":t.now().strftime("%d.%m.%Y"),"punkts":punkts}, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def uchastokById(request,id=0):
    try:
        Uchres = Uchastok.objects.get(id=id)
        SubUchs = Uchastok.objects.filter(parentid=id)
        punkts = []
        for SubUch in SubUchs:
            punkts.append({"id":SubUch.id,
                           "name":SubUch.name
                           })
        res = {
            "id": Uchres.id,
            "parentId": Uchres.parentid,
            "name": Uchres.name,
            "text": Uchres.text,
            "punkts": punkts
        }
        return HttpResponse(json.dumps(res, ensure_ascii=False),content_type="application/json")

    except Exception:
        return HttpResponse(status=404)

@csrf_exempt
def delivery(request):
    Id = 1
    objGasUsers = None
    token = request.META['HTTP_AUTHORIZATION']
    if request.method == 'GET':
        try:
            objsession = session.objects.get(access_token=token)
            if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
        except Exception:
            objGasUsers = None
        if (objGasUsers != None):
            resp = SendRequestTrains(("Mobile_deliveryget",{"account":objGasUsers.account},True))
            resp = resp['type']
        else:
            resp = HttpResponse(status=403)
    elif request.method == 'POST':
        type = request.body.decode("utf-8-sig")
        try:
            objsession = session.objects.get(access_token=token)
            if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
        except Exception:
            objGasUsers = None
        if (objGasUsers != None):
            resp = SendRequestTrains(("Mobile_deliveryset",{"account":objGasUsers.account,"type":type},True))
            result = resp['result']
            if(result=="OK"):
                resp = HttpResponse(status=200)
            else:
                resp = HttpResponse(status=500)
        else:
            resp = HttpResponse(status=403)
    return resp

@csrf_exempt
def ReadingsReceived(request):
    token = request.META['HTTP_AUTHORIZATION']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
    except Exception:
        objGasUsers = None
    if (objGasUsers != None):
        resp = SendRequestTrains(("Mobile_ReadingsReceived", {"account": objGasUsers.account}))
    else:
        resp = HttpResponse(status=403)
    return resp

@csrf_exempt
def ReadingsAccepted(request):
    token = request.META['HTTP_AUTHORIZATION']
    try:
        objsession = session.objects.get(access_token=token)
        if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
            objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
    except Exception:
        objGasUsers = None
    if (objGasUsers != None):
        resp = SendRequestTrains(("Mobile_ReadingsAccepted", {"account": objGasUsers.account}))
    else:
        resp = HttpResponse(status=403)
    return resp

@csrf_exempt
def SetReadings(request):
    token = request.META['HTTP_AUTHORIZATION']
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8-sig"))
        try:
            objsession = session.objects.get(access_token=token)
            if (objsession.datetimecreate >= t.now() - timedelta(seconds=objsession.expires_in)):
                objGasUsers = GasUsers.objects.get(uiduser=objsession.uiduser)
        except Exception:
            objGasUsers = None
        if (objGasUsers != None):
            resp = SendRequestTrains(("Mobile_SetReadings", {"account": objGasUsers.account,"sn":received_json_data['sn'],"value":received_json_data['value']}))
        else:
            resp = HttpResponse(status=403)
    else:
        resp = HttpResponse(status=404)
    return resp

#-----------------------------------------------------
def SendRequestTrains(id,params,retjson=False):
    data={"id":id,"params":params}
    requestTrain = {
                "event": "SetNewRequest",
                "data": data
                 }
    headers = {'content-type': 'application/json'}
    res = requests.post(UrlTrains + 'rest/', json=requestTrain, headers=headers,auth=('root', '95174837my'))
    received_json_data = json.loads(res.content.decode("utf-8-sig"))
    if(retjson==False):
        resp = HttpResponse(json.dumps(received_json_data, ensure_ascii=False), content_type="application/json")
    else:
        resp = received_json_data
    return resp

def Question(request):

    return HttpResponse(status=20000)

def Inform(request):

    return "Тестовое информирование"

def GetNews(auth):
    NewRes = News.objects.filter(auth=auth)
    newslist = []
    for New in NewRes:
        newslist.append({"id": New.id, "subj": New.subj, "date": New.date.strftime("%d.%m.%Y")})
    return {"code": 1, "news": newslist}

def GetNewsById(auth,id):
    try:
        NewRes = News.objects.get(auth=auth,id=id)
        return {"code": 1, "id": id, "subj": NewRes.subj, "date": NewRes.date,"news": NewRes.news }
    except Exception:
        return {"code": 1, "id": id, "subj": "", "date": "","news": ""}















