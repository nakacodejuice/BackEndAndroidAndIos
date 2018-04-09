import requests
import json


#регистрация л/с
datajson = {
  "account" : "36966",
  "lastName" : "Кузьмин",
  "password" : "password",
  "confirmPassword" : "password",
  "email" : "test",
  "mobilePhone" : "89536424056"
}
URL = 'http://127.0.0.1:8000/api/Account/Register'
headers = {'content-type': 'application/json'}
r = requests.post(url = URL, json = datajson,headers= headers)
print (r.content)

#получили токен
URL = 'http://127.0.0.1:8000/token'
PARAMS = 'grant_type=password&username=login&password=password'
r = requests.post(url = URL, params = PARAMS)
print (r.content)

#данные по л/с
received_json_data = json.loads(r.content.decode("utf-8-sig"))
access_token = received_json_data['access_token']
URL = 'http://127.0.0.1:8000/api/account'
PARAMS = 'grant_type=password&username=login&password=password'
headers = {'Authorization': received_json_data['access_token']}
r = requests.get(url = URL, params = PARAMS,headers=headers)
print (r.content)

#изменить данные л/с
received_json_data = json.loads(r.content.decode("utf-8-sig"))
data = {"password":"password",
        "confirmPassword":'password',
        "email":"oleg.kashin.rootkit@gmail.com",
        "mobilePhone":"79203879371",
        "inform":3}
URL = 'http://127.0.0.1:8000/api/account'
headers = {'content-type': 'application/json',
           'Authorization': access_token}
r = requests.post(url = URL, json = data,headers= headers)
print (r)

