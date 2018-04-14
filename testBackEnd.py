import requests
import json

URLServer = "http://10.4.144.101:8000/";
#регистрация л/с
datajson = {
  "account" : "36966",
  "lastName" : "Кузьмин",
  "password" : "password",
  "confirmPassword" : "password",
  "email" : "test",
  "mobilePhone" : "89536424056"
}
URL = URLServer+'api/Account/Register'
headers = {'content-type': 'application/json'}
r = requests.post(url = URL, json = datajson,headers= headers)
print (r.content)

#получили токен
URL = URLServer+'token'
PARAMS = 'grant_type=password&username=36966&password=password'
r = requests.post(url = URL, params = PARAMS)
print (r.content)

#данные по л/с
received_json_data = json.loads(r.content.decode("utf-8-sig"))
access_token = received_json_data['access_token']
URL = URLServer+'api/account'
headers = {'Authorization': received_json_data['access_token']}
r = requests.get(url = URL,headers=headers)
print (r.content)

#изменить данные л/с
received_json_data = json.loads(r.content.decode("utf-8-sig"))
data = {"password":"password",
        "confirmPassword":'password',
        "email":"oleg.kashin.rootkit@gmail.com",
        "mobilePhone":"79203879371",
        "inform":3}
URL = URLServer+'api/account'
headers = {'content-type': 'application/json',
           'Authorization': access_token}
r = requests.post(url = URL, json = data,headers= headers)
print (r)

#получить характеристики абонента
URL = URLServer+'api/Char'
headers = {'Authorization': access_token}
r = requests.get(url = URL,headers=headers)
print (r.content)

#ПолучитьСчетчикиАбонента
URL = URLServer+'api/Counter'
headers = {'Authorization': access_token}
r = requests.get(url = URL,headers=headers)
print (r.content)

#ПолучитьНачисленияПоСчетчикам
URL = URLServer+'api/CounterCharge'
headers = {'Authorization': access_token}
r = requests.get(url = URL,headers=headers)
print (r.content)


