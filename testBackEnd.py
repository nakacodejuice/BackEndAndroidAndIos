import requests
URL = 'http://127.0.0.1:8000/api/account'
PARAMS = 'grant_type=password&username=login&password=password'
headers = {'Authorization': '8bbce012-8abb-4669-bb02-d994a70e5b10'}
r = requests.get(url = URL, params = PARAMS,headers=headers)
print (r)
