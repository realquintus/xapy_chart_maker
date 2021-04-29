import json, re, requests
from auth_lrs import *
from types import SimpleNamespace
from base64 import b64encode

def query_lrs():
    user = user_lrs()
    password = password_lrs()
    endpoint = endpoint_lrs()
    xapi_req = endpoint + "statements?verb=http://vocab.xapi.fr/verbs/navigated-in"
    print(xapi_req)
    headers = {
        "Authorization": "Basic {}".format(
            b64encode(bytes(f"{user}:{password}", "utf-8")).decode("ascii")
        ),
        "X-Experience-API-Version": "1.0.0"
    }
    r = requests.get(xapi_req, headers=headers)
    return r.text

print(query_lrs())
#data_str=''
# JSON file to python object
#with open('test__multiple_data.txt', 'r') as file:
#    for i in file:
#        if re.search("^}",i):
#            data_str += i.replace(' ','')
#        else:
#            data_str += i.replace('\n', '').replace(' ','')
#    print(data_str)
   # data = json.load(file, object_hook=lambda d: SimpleNamespace(**d))
        

#print(data.id)
